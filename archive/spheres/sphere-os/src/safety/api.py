"""FastAPI routes for the Safety Monitoring system."""

from __future__ import annotations

import uuid
from typing import Any

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.materials.api import _get_or_create_orchestrator
from src.safety.models import SafetyEvent, SafetyEventResponse, SafetyReport
from src.safety.monitor import SafetyMonitor
from src.safety.thresholds import ThresholdConfig, ThresholdRule
from src.shared.database import get_db

router = APIRouter()

# Singleton monitor instance
_monitor = SafetyMonitor()


@router.get("/events")
async def list_safety_events(
    sphere_id: str | None = Query(None),
    severity: str | None = Query(None),
    limit: int = Query(50, ge=1, le=500),
    db: AsyncSession = Depends(get_db),
) -> list[dict[str, Any]]:
    """Get safety event history."""
    stmt = select(SafetyEvent).order_by(SafetyEvent.timestamp.desc()).limit(limit)
    if sphere_id:
        stmt = stmt.where(SafetyEvent.sphere_id == uuid.UUID(sphere_id))
    if severity:
        stmt = stmt.where(SafetyEvent.severity == severity)

    result = await db.execute(stmt)
    events = result.scalars().all()

    return [
        {
            "id": str(e.id),
            "sphere_id": str(e.sphere_id),
            "timestamp": e.timestamp.isoformat() if e.timestamp else None,
            "system_type": e.system_type,
            "severity": e.severity,
            "parameter": e.parameter,
            "value": e.value,
            "threshold": e.threshold,
            "resolved": e.resolved,
            "acknowledged": e.acknowledged,
        }
        for e in events
    ]


@router.get("/report/{sphere_id}")
async def get_safety_report(sphere_id: str) -> SafetyReport:
    """Get current safety status report for a Sphere."""
    orchestrator = _get_or_create_orchestrator(sphere_id)
    report = await _monitor.check_all_systems(sphere_id, orchestrator)
    return report


@router.post("/acknowledge/{event_id}")
async def acknowledge_event(
    event_id: str,
    db: AsyncSession = Depends(get_db),
) -> dict[str, str]:
    """Acknowledge a safety event."""
    result = await db.execute(
        select(SafetyEvent).where(SafetyEvent.id == uuid.UUID(event_id))
    )
    event = result.scalar_one_or_none()
    if not event:
        return {"status": "not_found"}

    event.acknowledged = True
    await db.flush()
    return {"status": "acknowledged"}


@router.get("/thresholds")
async def get_thresholds() -> list[dict[str, Any]]:
    """Get current threshold configuration."""
    return [r.model_dump() for r in _monitor.thresholds.rules]


@router.put("/thresholds")
async def update_thresholds(rules: list[ThresholdRule]) -> dict[str, str]:
    """Update threshold configuration."""
    _monitor.thresholds = ThresholdConfig(rules=rules)
    return {"status": "updated", "rule_count": str(len(rules))}
