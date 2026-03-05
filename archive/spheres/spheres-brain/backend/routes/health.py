"""
Health-check routes for SPHERES Brain.

Provides a system-wide health overview and per-service probes.  Until the
downstream micro-services are live on their real ports, the health checks
return simulated data with realistic latency values.
"""

from __future__ import annotations

import random
from datetime import datetime

from fastapi import APIRouter, HTTPException

from models.services import HealthStatus, SystemHealth
from models.registry import SPHERES_SERVICES, SERVICE_MAP

router = APIRouter()


# ---------------------------------------------------------------------------
# Simulated health probes
# ---------------------------------------------------------------------------

def _simulate_health(service_name: str) -> HealthStatus:
    """
    Simulate a health probe for a single SPHERES service.

    In production this would make an HTTP GET to the service's
    /health endpoint and measure actual latency.  For now we return
    plausible mock data — mostly 'up' with occasional degraded states.
    """
    # Weighted random: 85% up, 10% degraded, 5% down
    roll = random.random()
    if roll < 0.05:
        status = "down"
        latency = 0.0
        details = "Connection refused — service may be restarting"
    elif roll < 0.15:
        status = "degraded"
        latency = round(random.uniform(200, 800), 1)
        details = "Elevated response latency detected"
    else:
        status = "up"
        latency = round(random.uniform(8, 65), 1)
        details = "All endpoints responding normally"

    return HealthStatus(
        service_name=service_name,
        status=status,
        latency_ms=latency,
        last_check=datetime.utcnow(),
        version="0.1.0",
        details=details,
    )


def _compute_overall(statuses: list[HealthStatus]) -> str:
    """Determine aggregate health from individual service statuses."""
    status_set = {s.status for s in statuses}
    if "down" in status_set:
        return "degraded"
    if "degraded" in status_set:
        return "degraded"
    return "up"


# ---------------------------------------------------------------------------
# GET /api/health — full system health
# ---------------------------------------------------------------------------

@router.get("/api/health", response_model=SystemHealth)
async def system_health():
    """
    Probe every registered SPHERES service and return an aggregated
    health report.  The overall status is 'up' only if every service
    is healthy; otherwise 'degraded'.
    """
    statuses = [_simulate_health(svc.name) for svc in SPHERES_SERVICES]

    # Always report the brain itself as up (if this endpoint responds, it is)
    statuses.append(
        HealthStatus(
            service_name="spheres-brain",
            status="up",
            latency_ms=round(random.uniform(1, 5), 1),
            last_check=datetime.utcnow(),
            version="0.1.0",
            details="Orchestrator online — all routes registered",
        )
    )

    return SystemHealth(
        overall_status=_compute_overall(statuses),
        services=statuses,
        checked_at=datetime.utcnow(),
    )


# ---------------------------------------------------------------------------
# GET /api/health/{service} — single-service health
# ---------------------------------------------------------------------------

@router.get("/api/health/{service}", response_model=HealthStatus)
async def service_health(service: str):
    """
    Probe a single SPHERES service by name and return its health status.

    Valid service names: spheres-assets, spheres-legal, spheres-studio,
    spheres-viz, spheres-brain.
    """
    if service == "spheres-brain":
        return HealthStatus(
            service_name="spheres-brain",
            status="up",
            latency_ms=round(random.uniform(1, 5), 1),
            last_check=datetime.utcnow(),
            version="0.1.0",
            details="Orchestrator online — all routes registered",
        )

    if service not in SERVICE_MAP:
        raise HTTPException(
            status_code=404,
            detail=(
                f"Service '{service}' not found. "
                f"Available services: {', '.join(SERVICE_MAP.keys())}, spheres-brain"
            ),
        )

    return _simulate_health(service)
