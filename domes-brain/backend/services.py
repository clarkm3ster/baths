"""Service registry and health monitoring for DOMES Brain.

Maintains the canonical list of DOMES micro-services, performs periodic
health checks via ``httpx``, and persists status to SQLite so the
dashboard always has current availability data.
"""

from __future__ import annotations

import json
import logging
import time
from datetime import datetime, timezone
from typing import Any

import httpx
from sqlalchemy.orm import Session

from database import SessionLocal
from models import Service, ActivityLog

logger = logging.getLogger("domes.brain.services")

# ---------------------------------------------------------------------------
# Canonical service registry
# ---------------------------------------------------------------------------

DOMES_SERVICES: list[dict[str, Any]] = [
    {
        "name": "Spheres Assets",
        "slug": "spheres-assets",
        "base_url": "http://localhost:8000",
        "port": 8000,
        "description": "Philadelphia public property map — parcels, ownership, activation scores",
        "endpoint_count": 7,
    },
    {
        "name": "DOMES Data Research",
        "slug": "domes-data-research",
        "base_url": "http://localhost:8001",
        "port": 8001,
        "description": "Government data constellation — systems, connections, gaps, privacy laws",
        "endpoint_count": 6,
    },
    {
        "name": "DOMES Profile Research",
        "slug": "domes-profile-research",
        "base_url": "http://localhost:8002",
        "port": 8002,
        "description": "Composite profile builder — cases, profiles, costs, system involvement",
        "endpoint_count": 8,
    },
    {
        "name": "DOMES Contracts",
        "slug": "domes-contracts",
        "base_url": "http://localhost:8003",
        "port": 8003,
        "description": "Agreement generation engine — templates, agreements, compliance, consent",
        "endpoint_count": 12,
    },
    {
        "name": "DOMES Architect",
        "slug": "domes-architect",
        "base_url": "http://localhost:8004",
        "port": 8004,
        "description": "Coordination architecture designer — models, architectures, comparisons",
        "endpoint_count": 9,
    },
    {
        "name": "DOMES Viz",
        "slug": "domes-viz",
        "base_url": "http://localhost:8005",
        "port": 8005,
        "description": "Public-facing website and visualization layer",
        "endpoint_count": 0,
    },
    {
        "name": "DOMES Legal",
        "slug": "domes-legal",
        "base_url": "http://localhost:8003",
        "port": 8003,
        "health_endpoint": "/api/health",
        "description": "Legal provisions engine — federal/state/local laws, eligibility, and compliance analysis",
        "endpoint_count": 4,
        "key_endpoints": [
            "/api/provisions",
            "/api/provisions/{id}",
            "/api/eligibility",
            "/api/compliance",
        ],
    },
    {
        "name": "DOMES Datamap",
        "slug": "domes-datamap",
        "base_url": "http://localhost:8003",
        "port": 8003,
        "health_endpoint": "/api/health",
        "description": "System-of-systems mapper — person maps, gaps, bridges, consent pathways",
        "endpoint_count": 6,
        "key_endpoints": [
            "/api/person-map",
            "/api/gaps",
            "/api/bridges/priority",
            "/api/bridges/consent-pathway",
            "/api/bridges/quick-wins",
            "/api/systems",
        ],
    },
    {
        "name": "DOMES Profiles",
        "slug": "domes-profiles",
        "base_url": "http://localhost:8004",
        "port": 8004,
        "health_endpoint": "/api/health",
        "description": "Multi-system profile builder — circumstances, needs assessments, and cross-system identity",
        "endpoint_count": 5,
        "key_endpoints": [
            "/api/profiles",
            "/api/profiles/{id}",
            "/api/profiles/generate",
            "/api/circumstances",
            "/api/assessments",
        ],
    },
    {
        "name": "DOMES Flourishing",
        "slug": "domes-flourishing",
        "base_url": "http://localhost:8005",
        "port": 8005,
        "health_endpoint": "/api/health",
        "description": "Outcome tracking and flourishing metrics — wellbeing indicators, progress, and impact",
        "endpoint_count": 5,
        "key_endpoints": [
            "/api/outcomes",
            "/api/indicators",
            "/api/progress",
            "/api/impact",
            "/api/flourishing-score",
        ],
    },
    {
        "name": "DOMES Lab",
        "slug": "domes-lab",
        "base_url": "http://localhost:8007",
        "port": 8007,
        "health_endpoint": "/api/health",
        "description": "Experimentation and innovation lab — pilots, experiments, A/B tests, and research insights",
        "endpoint_count": 5,
        "key_endpoints": [
            "/api/experiments",
            "/api/pilots",
            "/api/results",
            "/api/insights",
            "/api/metrics",
        ],
    },
]


# ---------------------------------------------------------------------------
# Health check
# ---------------------------------------------------------------------------

async def check_service_health(service_row: Service) -> dict[str, Any]:
    """Ping a single service's ``/api/health`` endpoint.

    Updates the database row in-place and returns a status dict.
    """
    url = f"{service_row.base_url}/api/health"
    now = datetime.now(timezone.utc)

    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            t0 = time.monotonic()
            resp = await client.get(url)
            elapsed_ms = round((time.monotonic() - t0) * 1000, 2)

        if resp.status_code == 200:
            body = resp.json()
            if body.get("status") == "ok":
                service_row.status = "online"
                service_row.last_healthy = now
            else:
                service_row.status = "degraded"
            service_row.response_time_ms = elapsed_ms
        else:
            service_row.status = "degraded"
            service_row.response_time_ms = elapsed_ms
            elapsed_ms = elapsed_ms

    except (httpx.ConnectError, httpx.TimeoutException, httpx.ReadError, OSError):
        service_row.status = "offline"
        service_row.response_time_ms = None
        elapsed_ms = None

    service_row.last_checked = now

    return {
        "slug": service_row.slug,
        "status": service_row.status,
        "response_time_ms": elapsed_ms,
        "last_checked": now.isoformat(),
    }


# ---------------------------------------------------------------------------
# Monitor all services (called by scheduler)
# ---------------------------------------------------------------------------

async def monitor_all_services() -> list[dict[str, Any]]:
    """Run health checks against every registered service.

    Opens its own DB session so it can be called from the APScheduler
    background job without depending on a request context.
    """
    db: Session = SessionLocal()
    results: list[dict[str, Any]] = []

    try:
        services = db.query(Service).all()
        for svc in services:
            result = await check_service_health(svc)
            results.append(result)

            # Log status transitions as activity
            db.add(ActivityLog(
                service_slug=svc.slug,
                event_type="health_check",
                description=f"Status: {svc.status} ({svc.response_time_ms or '-'}ms)",
                metadata_json=json.dumps(result),
            ))

        db.commit()
    except Exception:
        logger.exception("Error during service health monitoring")
        db.rollback()
    finally:
        db.close()

    return results


# ---------------------------------------------------------------------------
# Registry helpers
# ---------------------------------------------------------------------------

def seed_service_registry(db: Session) -> int:
    """Ensure every service in ``DOMES_SERVICES`` has a row.

    Idempotent — skips services whose slug already exists.
    Returns the number of newly inserted rows.
    """
    inserted = 0
    for svc_def in DOMES_SERVICES:
        exists = db.query(Service).filter(Service.slug == svc_def["slug"]).first()
        if exists:
            continue
        row = Service(
            name=svc_def["name"],
            slug=svc_def["slug"],
            base_url=svc_def["base_url"],
            port=svc_def["port"],
            description=svc_def["description"],
            status="offline",
            endpoint_count=svc_def.get("endpoint_count", 0),
        )
        db.add(row)
        inserted += 1

    if inserted:
        db.commit()

    return inserted


def get_service_registry(db: Session) -> list[dict[str, Any]]:
    """Return all services with their current status."""
    services = db.query(Service).order_by(Service.port).all()
    return [_service_dict(s) for s in services]


def get_service_by_slug(db: Session, slug: str) -> dict[str, Any] | None:
    """Look up a single service by its URL slug."""
    svc = db.query(Service).filter(Service.slug == slug).first()
    if svc is None:
        return None
    return _service_dict(svc)


def _service_dict(s: Service) -> dict[str, Any]:
    return {
        "id": s.id,
        "name": s.name,
        "slug": s.slug,
        "base_url": s.base_url,
        "port": s.port,
        "description": s.description,
        "status": s.status,
        "last_checked": s.last_checked.isoformat() if s.last_checked else None,
        "last_healthy": s.last_healthy.isoformat() if s.last_healthy else None,
        "response_time_ms": s.response_time_ms,
        "data_freshness": s.data_freshness,
        "endpoint_count": s.endpoint_count,
    }
