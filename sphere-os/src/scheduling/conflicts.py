"""Booking conflict detection and resolution.

Handles overlap checking, transition buffer validation, and alternative
slot suggestion when a booking request can't be fulfilled as-is.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timedelta
from typing import Any

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.scheduling.models import Booking, Sphere, TimeSlice
from src.scheduling.transitions import calculate_transition_time


async def find_available_slots(
    sphere_id: uuid.UUID,
    desired_start: datetime,
    desired_end: datetime,
    material_request: dict[str, Any],
    db: AsyncSession,
) -> list[dict[str, Any]]:
    """Check if a booking slot is available and return availability or alternatives.

    Args:
        sphere_id: Target Sphere ID.
        desired_start: Requested start time.
        desired_end: Requested end time.
        material_request: Desired MaterialConfiguration.
        db: Async database session.

    Returns:
        List of availability results or alternative suggestions.
    """
    # Fetch Sphere
    result = await db.execute(select(Sphere).where(Sphere.id == sphere_id))
    sphere = result.scalar_one_or_none()
    if not sphere:
        return [{"available": False, "reason": "sphere_not_found"}]

    # Find existing slices that overlap with the desired window
    conflicts = await _find_overlapping_slices(db, sphere_id, desired_start, desired_end)

    if not conflicts:
        # No overlap — check transition buffer
        prev_slice = await _get_previous_slice(db, sphere_id, desired_start)

        if prev_slice:
            from_config = prev_slice.material_config or {}
            transition_sec = calculate_transition_time(
                from_config, material_request, list(sphere.material_inventory)
            )
            actual_buffer_sec = (desired_start - prev_slice.end_time).total_seconds()

            if actual_buffer_sec < transition_sec:
                suggested_start = prev_slice.end_time + timedelta(seconds=transition_sec)
                return [{
                    "available": False,
                    "reason": "insufficient_transition_buffer",
                    "transition_time_minutes": transition_sec // 60,
                    "actual_buffer_minutes": int(actual_buffer_sec // 60),
                    "suggested_start": suggested_start.isoformat(),
                }]
        else:
            # No previous slice — check transition from base state
            from_config = sphere.base_state or {}
            transition_sec = calculate_transition_time(
                from_config, material_request, list(sphere.material_inventory)
            )

        return [{
            "available": True,
            "transition_time_minutes": transition_sec // 60 if prev_slice else 0,
        }]

    # Conflicts exist — propose alternatives
    return await _suggest_alternatives(
        db, sphere, conflicts, desired_start, desired_end, material_request
    )


async def _find_overlapping_slices(
    db: AsyncSession,
    sphere_id: uuid.UUID,
    start: datetime,
    end: datetime,
) -> list[TimeSlice]:
    """Find all time slices that overlap with the given range."""
    stmt = select(TimeSlice).where(
        and_(
            TimeSlice.sphere_id == sphere_id,
            TimeSlice.start_time < end,
            TimeSlice.end_time > start,
        )
    ).order_by(TimeSlice.start_time)

    result = await db.execute(stmt)
    return list(result.scalars().all())


async def _get_previous_slice(
    db: AsyncSession,
    sphere_id: uuid.UUID,
    before: datetime,
) -> TimeSlice | None:
    """Get the most recent time slice ending before the given time."""
    stmt = (
        select(TimeSlice)
        .where(
            and_(
                TimeSlice.sphere_id == sphere_id,
                TimeSlice.end_time <= before,
            )
        )
        .order_by(TimeSlice.end_time.desc())
        .limit(1)
    )
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def _suggest_alternatives(
    db: AsyncSession,
    sphere: Sphere,
    conflicts: list[TimeSlice],
    desired_start: datetime,
    desired_end: datetime,
    material_request: dict[str, Any],
) -> list[dict[str, Any]]:
    """Generate alternative booking suggestions when there's a conflict."""
    alternatives: list[dict[str, Any]] = []
    duration = desired_end - desired_start

    # Option 1: Shift time to after the last conflict
    last_conflict = max(conflicts, key=lambda s: s.end_time)
    transition_sec = calculate_transition_time(
        last_conflict.material_config or {},
        material_request,
        list(sphere.material_inventory),
    )
    suggested_start = last_conflict.end_time + timedelta(seconds=transition_sec)
    alternatives.append({
        "type": "shift_time",
        "suggested_start": suggested_start.isoformat(),
        "suggested_end": (suggested_start + duration).isoformat(),
        "transition_time_minutes": transition_sec // 60,
    })

    # Option 2: Simplify materials (remove olfactory to reduce transition time)
    scent_profile = material_request.get("scent_profile", {})
    if scent_profile.get("primary"):
        simplified = {**material_request, "scent_profile": {"primary": None, "secondary": None, "intensity": 0.0}}
        simplified_transition = calculate_transition_time(
            (last_conflict.material_config or {}), simplified, list(sphere.material_inventory)
        )
        alternatives.append({
            "type": "simplify_materials",
            "note": "Removing scent reduces transition to ~5 minutes",
            "transition_time_minutes": simplified_transition // 60,
        })

    # Option 3: Suggest different Spheres with availability
    other_spheres = await _find_available_spheres(db, desired_start, desired_end, sphere.id)
    for s in other_spheres[:3]:
        alternatives.append({
            "type": "different_sphere",
            "sphere_id": str(s.id),
            "sphere_name": s.name,
        })

    return alternatives


async def _find_available_spheres(
    db: AsyncSession,
    start: datetime,
    end: datetime,
    exclude_id: uuid.UUID,
) -> list[Sphere]:
    """Find Spheres that have no conflicting time slices in the given range."""
    # Get all sphere IDs that have conflicts
    busy_stmt = select(TimeSlice.sphere_id).where(
        and_(
            TimeSlice.start_time < end,
            TimeSlice.end_time > start,
        )
    ).distinct()
    busy_result = await db.execute(busy_stmt)
    busy_ids = {row[0] for row in busy_result.all()}
    busy_ids.add(exclude_id)

    # Get available Spheres
    stmt = select(Sphere).where(Sphere.id.not_in(busy_ids)).limit(5)
    result = await db.execute(stmt)
    return list(result.scalars().all())
