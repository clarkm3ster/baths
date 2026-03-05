"""FastAPI routes for Sphere scheduling, bookings, and time slices."""

from __future__ import annotations

import math
import uuid
from datetime import datetime
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.scheduling.conflicts import find_available_slots
from src.scheduling.models import Booking, BookingStatus, Sphere, TimeSlice, TimeSliceMode
from src.scheduling.transitions import calculate_transition_time, get_bottleneck_systems
from src.shared.database import get_db

router = APIRouter()


# --- Request/Response schemas ---

class BookingRequest(BaseModel):
    user_id: uuid.UUID
    desired_start: datetime
    desired_end: datetime
    material_request: dict[str, Any] = Field(default_factory=dict)


class MaterialConfigUpdate(BaseModel):
    material_request: dict[str, Any]


class TransitionTimeRequest(BaseModel):
    from_config: dict[str, Any]
    to_config: dict[str, Any]


# --- Routes ---

@router.get("/spheres/{sphere_id}/schedule")
async def get_schedule(
    sphere_id: uuid.UUID,
    start: datetime = Query(..., alias="start"),
    end: datetime = Query(..., alias="end"),
    db: AsyncSession = Depends(get_db),
) -> list[dict[str, Any]]:
    """Get all time slices for a Sphere within a date range."""
    stmt = select(TimeSlice).where(
        and_(
            TimeSlice.sphere_id == sphere_id,
            TimeSlice.start_time < end,
            TimeSlice.end_time > start,
        )
    ).order_by(TimeSlice.start_time)

    result = await db.execute(stmt)
    slices = result.scalars().all()

    return [
        {
            "id": str(s.id),
            "sphere_id": str(s.sphere_id),
            "start_time": s.start_time.isoformat(),
            "end_time": s.end_time.isoformat(),
            "mode": s.mode.value if hasattr(s.mode, "value") else s.mode,
            "material_config": s.material_config,
            "transition_buffer_minutes": s.transition_buffer_minutes,
            "booking_id": str(s.booking_id) if s.booking_id else None,
        }
        for s in slices
    ]


@router.post("/spheres/{sphere_id}/bookings")
async def create_booking(
    sphere_id: uuid.UUID,
    req: BookingRequest,
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    """Create a booking for a Sphere, or return alternatives if conflicting."""
    # Verify sphere exists
    sphere_result = await db.execute(select(Sphere).where(Sphere.id == sphere_id))
    sphere = sphere_result.scalar_one_or_none()
    if not sphere:
        raise HTTPException(status_code=404, detail="Sphere not found")

    # Check availability
    slots = await find_available_slots(
        sphere_id=sphere_id,
        desired_start=req.desired_start,
        desired_end=req.desired_end,
        material_request=req.material_request,
        db=db,
    )

    if slots and slots[0].get("available"):
        # Create the booking
        booking = Booking(
            id=uuid.uuid4(),
            user_id=req.user_id,
            sphere_id=sphere_id,
            material_request=req.material_request,
            material_actual=req.material_request,
            pricing_usd=_calculate_pricing(req.desired_start, req.desired_end, req.material_request),
            status=BookingStatus.confirmed,
        )
        db.add(booking)

        # Create the time slice
        transition_minutes = slots[0].get("transition_time_minutes", 0)
        time_slice = TimeSlice(
            id=uuid.uuid4(),
            sphere_id=sphere_id,
            start_time=req.desired_start,
            end_time=req.desired_end,
            mode=TimeSliceMode.public,
            material_config=req.material_request,
            transition_buffer_minutes=transition_minutes,
            booking_id=booking.id,
        )
        db.add(time_slice)
        await db.flush()

        return {
            "status": "confirmed",
            "booking_id": str(booking.id),
            "pricing_usd": booking.pricing_usd,
            "transition_time_minutes": transition_minutes,
        }
    else:
        return {
            "status": "unavailable",
            "alternatives": slots,
        }


@router.get("/spheres/{sphere_id}/availability")
async def check_availability(
    sphere_id: uuid.UUID,
    duration: str = Query("2h", description="Duration string like '2h', '30m', '1d'"),
    material_complexity: str = Query("medium", description="low|medium|high"),
    limit: int = Query(5, ge=1, le=20),
    db: AsyncSession = Depends(get_db),
) -> list[dict[str, Any]]:
    """Find next available slots for a Sphere."""
    # Parse duration
    duration_minutes = _parse_duration(duration)

    # Get Sphere
    result = await db.execute(select(Sphere).where(Sphere.id == sphere_id))
    sphere = result.scalar_one_or_none()
    if not sphere:
        raise HTTPException(status_code=404, detail="Sphere not found")

    # Get upcoming time slices
    now = datetime.utcnow()
    stmt = (
        select(TimeSlice)
        .where(and_(TimeSlice.sphere_id == sphere_id, TimeSlice.end_time > now))
        .order_by(TimeSlice.start_time)
        .limit(50)
    )
    result = await db.execute(stmt)
    slices = list(result.scalars().all())

    # Find gaps
    available = []
    current_time = now

    for ts in slices:
        gap_minutes = (ts.start_time - current_time).total_seconds() / 60
        if gap_minutes >= duration_minutes:
            available.append({
                "start": current_time.isoformat(),
                "end": (current_time + _minutes_to_td(duration_minutes)).isoformat(),
                "gap_minutes": int(gap_minutes),
            })
        current_time = ts.end_time

        if len(available) >= limit:
            break

    # Always add "after all bookings" slot
    if len(available) < limit:
        available.append({
            "start": current_time.isoformat(),
            "end": (current_time + _minutes_to_td(duration_minutes)).isoformat(),
            "gap_minutes": None,
        })

    return available


@router.put("/bookings/{booking_id}/material-config")
async def update_booking_material(
    booking_id: uuid.UUID,
    req: MaterialConfigUpdate,
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    """Update a booking's material configuration."""
    result = await db.execute(select(Booking).where(Booking.id == booking_id))
    booking = result.scalar_one_or_none()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    # Get sphere for transition calculation
    sphere_result = await db.execute(select(Sphere).where(Sphere.id == booking.sphere_id))
    sphere = sphere_result.scalar_one_or_none()

    booking.material_request = req.material_request
    booking.material_actual = req.material_request

    # Recalculate pricing
    ts = await db.execute(
        select(TimeSlice).where(TimeSlice.booking_id == booking_id).limit(1)
    )
    time_slice = ts.scalar_one_or_none()
    if time_slice:
        booking.pricing_usd = _calculate_pricing(
            time_slice.start_time, time_slice.end_time, req.material_request
        )
        time_slice.material_config = req.material_request

    await db.flush()
    return {"status": "updated", "new_pricing_usd": booking.pricing_usd}


@router.get("/spheres/{sphere_id}/transition-time")
async def get_transition_time(
    sphere_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    """Calculate transition time between current state and target config."""
    result = await db.execute(select(Sphere).where(Sphere.id == sphere_id))
    sphere = result.scalar_one_or_none()
    if not sphere:
        raise HTTPException(status_code=404, detail="Sphere not found")

    # For now, return transition from base state
    from_config = sphere.base_state or {}
    return {
        "from_config": "base_state",
        "material_inventory": list(sphere.material_inventory),
        "base_state": from_config,
    }


# --- Helpers ---

def _calculate_pricing(
    start: datetime,
    end: datetime,
    material_request: dict[str, Any],
) -> float:
    """Calculate booking price based on duration and material complexity."""
    duration_hours = (end - start).total_seconds() / 3600
    base_rate = 50.0  # $50/hour base

    # Material complexity multiplier
    complexity = 1.0
    if material_request.get("scent_profile", {}).get("primary"):
        complexity += 0.5  # olfactory premium
    if material_request.get("shape_memory_elements"):
        complexity += 0.3
    if material_request.get("floor_haptic_pattern", "off") != "off":
        complexity += 0.2

    return round(duration_hours * base_rate * complexity, 2)


def _parse_duration(duration_str: str) -> int:
    """Parse duration string like '2h', '30m', '1d' to minutes."""
    s = duration_str.strip().lower()
    if s.endswith("h"):
        return int(float(s[:-1]) * 60)
    elif s.endswith("m"):
        return int(float(s[:-1]))
    elif s.endswith("d"):
        return int(float(s[:-1]) * 1440)
    return 120  # default 2 hours


def _minutes_to_td(minutes: int):
    from datetime import timedelta
    return timedelta(minutes=minutes)
