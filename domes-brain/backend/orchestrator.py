"""Unified query routing engine for DOMES Brain.

The orchestrator is the heart of the brain.  It accepts natural-language
queries (with optional structured circumstances), determines which
downstream DOMES services are relevant, dispatches requests in parallel
via ``httpx.AsyncClient``, and assembles a single unified response.

Every request is wrapped in the standard envelope::

    { "status": "ok", "data": ..., "meta": { "timestamp": ..., "duration_ms": ... } }
"""

from __future__ import annotations

import asyncio
import hashlib
import json
import logging
import time
from datetime import datetime, timezone
from typing import Any

import httpx
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from sqlalchemy import func, desc

from database import get_db
from models import Service, QueryLog, WebhookSubscription, ActivityLog
from services import get_service_registry, get_service_by_slug, check_service_health
from cache import query_cache

logger = logging.getLogger("domes.brain.orchestrator")

router = APIRouter(prefix="/api", tags=["orchestrator"])


# ---------------------------------------------------------------------------
# Response envelope helper
# ---------------------------------------------------------------------------

def _envelope(
    data: Any,
    *,
    status: str = "ok",
    duration_ms: float | None = None,
    warnings: list[str] | None = None,
) -> dict[str, Any]:
    """Wrap *data* in the standard DOMES Brain response envelope."""
    meta: dict[str, Any] = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    if duration_ms is not None:
        meta["duration_ms"] = round(duration_ms, 2)
    if warnings:
        meta["warnings"] = warnings
    return {"status": status, "data": data, "meta": meta}


# ---------------------------------------------------------------------------
# Keyword routing tables
# ---------------------------------------------------------------------------

# Each entry maps a set of keywords to a service slug and the downstream
# endpoint to hit.  The orchestrator scans the query text (lowered) for
# keyword matches and fans out to every matching service.

_ROUTE_TABLE: list[dict[str, Any]] = [
    {
        "slug": "domes-data-research",
        "keywords": [
            "legal", "rights", "law", "privacy", "data system", "government system",
            "constellation", "gap", "barrier", "ferpa", "hipaa", "regulation",
            "data sharing", "system", "connection", "agency", "federal",
        ],
        "endpoint": "/api/systems",
        "query_endpoint": "/api/constellation",
        "method": "POST",
        "label": "Government Data Systems",
    },
    {
        "slug": "spheres-assets",
        "keywords": [
            "property", "parcel", "asset", "land", "building", "real estate",
            "vacant", "vacancy", "zoning", "public property", "city-owned",
            "philadelphia", "address", "map",
        ],
        "endpoint": "/api/parcels",
        "query_endpoint": "/api/parcels",
        "method": "GET",
        "label": "Public Property Assets",
    },
    {
        "slug": "domes-profile-research",
        "keywords": [
            "profile", "person", "individual", "case", "family", "child",
            "welfare", "foster", "cost", "composite", "circumstances",
            "medicaid", "snap", "tanf", "ssi", "disability",
        ],
        "endpoint": "/api/profiles/generate",
        "query_endpoint": "/api/profiles/generate",
        "method": "POST",
        "label": "Composite Profiles",
    },
    {
        "slug": "domes-contracts",
        "keywords": [
            "contract", "agreement", "consent", "mou", "memorandum",
            "data sharing agreement", "compliance", "template", "dsa",
            "baa", "isa", "interagency",
        ],
        "endpoint": "/api/agreements",
        "query_endpoint": "/api/agreements",
        "method": "GET",
        "label": "Agreements & Contracts",
    },
    {
        "slug": "domes-architect",
        "keywords": [
            "architecture", "coordination", "model", "governance",
            "hub", "spine", "backbone", "federated", "centralized",
            "integration", "design", "blueprint", "budget", "stakeholder",
        ],
        "endpoint": "/api/architectures",
        "query_endpoint": "/api/architectures",
        "method": "GET",
        "label": "Coordination Architectures",
    },
]


def _match_services(query_text: str) -> list[dict[str, Any]]:
    """Return the route-table entries whose keywords appear in *query_text*."""
    lower = query_text.lower()
    matched: list[dict[str, Any]] = []
    for route in _ROUTE_TABLE:
        for kw in route["keywords"]:
            if kw in lower:
                matched.append(route)
                break
    # If nothing matched, return all routes so the user gets a broad overview
    if not matched:
        matched = list(_ROUTE_TABLE)
    return matched


# ---------------------------------------------------------------------------
# Pydantic schemas
# ---------------------------------------------------------------------------

class UnifiedQuery(BaseModel):
    query: str = Field(..., min_length=1, max_length=2000, description="Natural language query")
    circumstances: dict[str, Any] = Field(default_factory=dict, description="Structured profile circumstances")


class SubscribeRequest(BaseModel):
    service_slug: str
    event_type: str = "status_change"
    callback_url: str
    secret: str = ""


# ---------------------------------------------------------------------------
# POST /api/query  --  the main orchestration endpoint
# ---------------------------------------------------------------------------

@router.post("/query")
async def unified_query(body: UnifiedQuery, db: Session = Depends(get_db)):
    """Accept a natural-language query, route to relevant services, return
    unified results with graceful degradation when services are offline.
    """
    t0 = time.monotonic()
    warnings: list[str] = []

    # Check cache
    cache_key = hashlib.sha256(
        json.dumps({"q": body.query, "c": body.circumstances}, sort_keys=True).encode()
    ).hexdigest()
    cached = await query_cache.get(cache_key)
    if cached is not None:
        elapsed = round((time.monotonic() - t0) * 1000, 2)
        return _envelope(cached, duration_ms=elapsed, warnings=["cache_hit"])

    # Determine which services to query
    routes = _match_services(body.query)

    # Look up live status for each matched service
    service_rows: dict[str, Service] = {}
    for route in routes:
        row = db.query(Service).filter(Service.slug == route["slug"]).first()
        if row:
            service_rows[route["slug"]] = row

    # Fan out requests in parallel
    results: dict[str, Any] = {}
    slugs_queried: list[str] = []

    async def _call_service(route: dict[str, Any]) -> None:
        slug = route["slug"]
        svc = service_rows.get(slug)
        if svc is None:
            warnings.append(f"{slug}: not registered")
            return

        base_url = svc.base_url
        endpoint = route["query_endpoint"]
        method = route["method"]
        url = f"{base_url}{endpoint}"

        slugs_queried.append(slug)

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                if method == "POST":
                    payload = body.circumstances if body.circumstances else {"query": body.query}
                    resp = await client.post(url, json=payload)
                else:
                    # GET with optional search parameter
                    params: dict[str, str] = {}
                    # For spheres-assets, pass query as address search
                    if slug == "spheres-assets":
                        params["search"] = body.query
                        params["limit"] = "20"
                    resp = await client.get(url, params=params)

                if resp.status_code == 200:
                    results[slug] = {
                        "label": route["label"],
                        "status": "ok",
                        "data": resp.json(),
                    }
                else:
                    warnings.append(f"{slug}: returned HTTP {resp.status_code}")
                    results[slug] = {
                        "label": route["label"],
                        "status": "error",
                        "error": f"HTTP {resp.status_code}",
                        "data": None,
                    }

        except httpx.TimeoutException:
            warnings.append(f"{slug}: request timed out")
            results[slug] = {
                "label": route["label"],
                "status": "timeout",
                "error": "Service did not respond within 10s",
                "data": None,
            }
        except (httpx.ConnectError, httpx.ReadError, OSError) as exc:
            warnings.append(f"{slug}: offline ({type(exc).__name__})")
            results[slug] = {
                "label": route["label"],
                "status": "offline",
                "error": str(exc),
                "data": None,
            }

    # Run all service calls concurrently
    await asyncio.gather(*[_call_service(r) for r in routes])

    # Count total result items across services
    total_results = 0
    for slug, res in results.items():
        if res["data"] is None:
            continue
        data = res["data"]
        if isinstance(data, list):
            total_results += len(data)
        elif isinstance(data, dict):
            # Heuristic: count sub-lists inside the response
            for v in data.values():
                if isinstance(v, list):
                    total_results += len(v)
                    break
            else:
                total_results += 1

    elapsed = round((time.monotonic() - t0) * 1000, 2)

    # Build response payload
    response_data = {
        "query": body.query,
        "circumstances": body.circumstances,
        "services_queried": slugs_queried,
        "results": results,
        "total_results": total_results,
    }

    # Cache the response
    await query_cache.set(cache_key, response_data, ttl=120)

    # Persist query log
    try:
        log = QueryLog(
            query_text=body.query,
            circumstances=json.dumps(body.circumstances),
            duration_ms=elapsed,
            services_queried=json.dumps(slugs_queried),
            result_count=total_results,
        )
        db.add(log)
        db.commit()
    except Exception:
        logger.exception("Failed to persist query log")
        db.rollback()

    return _envelope(response_data, duration_ms=elapsed, warnings=warnings or None)


# ---------------------------------------------------------------------------
# GET /api/services  --  full registry with health
# ---------------------------------------------------------------------------

@router.get("/services")
async def list_services(db: Session = Depends(get_db)):
    t0 = time.monotonic()
    registry = get_service_registry(db)
    online = sum(1 for s in registry if s["status"] == "online")
    elapsed = round((time.monotonic() - t0) * 1000, 2)
    return _envelope(
        {
            "total": len(registry),
            "online": online,
            "offline": len(registry) - online,
            "services": registry,
        },
        duration_ms=elapsed,
    )


# ---------------------------------------------------------------------------
# GET /api/services/{slug}  --  single service detail
# ---------------------------------------------------------------------------

@router.get("/services/{slug}")
async def get_service(slug: str, db: Session = Depends(get_db)):
    t0 = time.monotonic()
    svc = get_service_by_slug(db, slug)
    if svc is None:
        raise HTTPException(status_code=404, detail=f"Service '{slug}' not found")

    # Include recent activity for this service
    activities = (
        db.query(ActivityLog)
        .filter(ActivityLog.service_slug == slug)
        .order_by(desc(ActivityLog.timestamp))
        .limit(20)
        .all()
    )
    svc["recent_activity"] = [
        {
            "event_type": a.event_type,
            "description": a.description,
            "timestamp": a.timestamp.isoformat() if a.timestamp else None,
        }
        for a in activities
    ]

    elapsed = round((time.monotonic() - t0) * 1000, 2)
    return _envelope(svc, duration_ms=elapsed)


# ---------------------------------------------------------------------------
# GET /api/health  --  brain health + service statuses
# ---------------------------------------------------------------------------

@router.get("/health")
async def health_check(db: Session = Depends(get_db)):
    t0 = time.monotonic()

    services = db.query(Service).all()
    service_statuses: dict[str, str] = {}
    for svc in services:
        service_statuses[svc.slug] = svc.status

    online = sum(1 for s in service_statuses.values() if s == "online")
    total = len(service_statuses)

    if online == total and total > 0:
        brain_status = "healthy"
    elif online > 0:
        brain_status = "degraded"
    else:
        brain_status = "ok"  # brain is running even if nothing else is

    elapsed = round((time.monotonic() - t0) * 1000, 2)

    return _envelope(
        {
            "brain": brain_status,
            "services_online": online,
            "services_total": total,
            "services": service_statuses,
            "cache_entries": query_cache.size,
        },
        duration_ms=elapsed,
    )


# ---------------------------------------------------------------------------
# POST /api/subscribe  --  create webhook subscription
# ---------------------------------------------------------------------------

@router.post("/subscribe")
async def create_subscription(body: SubscribeRequest, db: Session = Depends(get_db)):
    t0 = time.monotonic()

    # Validate service exists
    svc = db.query(Service).filter(Service.slug == body.service_slug).first()
    if svc is None:
        raise HTTPException(status_code=404, detail=f"Service '{body.service_slug}' not found")

    sub = WebhookSubscription(
        service_slug=body.service_slug,
        event_type=body.event_type,
        callback_url=body.callback_url,
        secret=body.secret,
        active=True,
    )
    db.add(sub)
    db.commit()
    db.refresh(sub)

    elapsed = round((time.monotonic() - t0) * 1000, 2)
    return _envelope(
        {
            "id": sub.id,
            "service_slug": sub.service_slug,
            "event_type": sub.event_type,
            "callback_url": sub.callback_url,
            "active": sub.active,
            "created_at": sub.created_at.isoformat() if sub.created_at else None,
        },
        duration_ms=elapsed,
    )


# ---------------------------------------------------------------------------
# GET /api/activity  --  recent activity log
# ---------------------------------------------------------------------------

@router.get("/activity")
async def recent_activity(
    limit: int = Query(100, le=500),
    service: str | None = Query(None, description="Filter by service slug"),
    event_type: str | None = Query(None, description="Filter by event type"),
    db: Session = Depends(get_db),
):
    t0 = time.monotonic()

    q = db.query(ActivityLog)
    if service:
        q = q.filter(ActivityLog.service_slug == service)
    if event_type:
        q = q.filter(ActivityLog.event_type == event_type)

    activities = q.order_by(desc(ActivityLog.timestamp)).limit(limit).all()

    elapsed = round((time.monotonic() - t0) * 1000, 2)
    return _envelope(
        [
            {
                "id": a.id,
                "service_slug": a.service_slug,
                "event_type": a.event_type,
                "description": a.description,
                "timestamp": a.timestamp.isoformat() if a.timestamp else None,
                "metadata": json.loads(a.metadata_json) if a.metadata_json else {},
            }
            for a in activities
        ],
        duration_ms=elapsed,
    )


# ---------------------------------------------------------------------------
# GET /api/stats  --  aggregate statistics
# ---------------------------------------------------------------------------

@router.get("/stats")
async def stats(db: Session = Depends(get_db)):
    t0 = time.monotonic()

    # Query volume
    total_queries = db.query(func.count(QueryLog.id)).scalar() or 0
    avg_duration = db.query(func.avg(QueryLog.duration_ms)).scalar() or 0.0
    avg_results = db.query(func.avg(QueryLog.result_count)).scalar() or 0.0

    # Queries in last 24h
    from datetime import timedelta
    day_ago = datetime.now(timezone.utc) - timedelta(hours=24)
    queries_24h = (
        db.query(func.count(QueryLog.id))
        .filter(QueryLog.timestamp >= day_ago)
        .scalar()
        or 0
    )

    # Service uptime (ratio of healthy checks to total checks in activity log)
    services = db.query(Service).all()
    uptime: dict[str, dict[str, Any]] = {}
    for svc in services:
        total_checks = (
            db.query(func.count(ActivityLog.id))
            .filter(
                ActivityLog.service_slug == svc.slug,
                ActivityLog.event_type == "health_check",
            )
            .scalar()
            or 0
        )
        healthy_checks = (
            db.query(func.count(ActivityLog.id))
            .filter(
                ActivityLog.service_slug == svc.slug,
                ActivityLog.event_type == "health_check",
                ActivityLog.description.like("%online%"),
            )
            .scalar()
            or 0
        )
        pct = round((healthy_checks / total_checks * 100), 1) if total_checks > 0 else 0.0
        uptime[svc.slug] = {
            "status": svc.status,
            "uptime_pct": pct,
            "total_checks": total_checks,
            "healthy_checks": healthy_checks,
            "last_checked": svc.last_checked.isoformat() if svc.last_checked else None,
            "response_time_ms": svc.response_time_ms,
            "data_freshness": svc.data_freshness,
        }

    # Most queried services
    query_logs = db.query(QueryLog).all()
    service_hit_counts: dict[str, int] = {}
    for ql in query_logs:
        try:
            slugs = json.loads(ql.services_queried)
        except (json.JSONDecodeError, TypeError):
            continue
        for slug in slugs:
            service_hit_counts[slug] = service_hit_counts.get(slug, 0) + 1

    elapsed = round((time.monotonic() - t0) * 1000, 2)
    return _envelope(
        {
            "queries": {
                "total": total_queries,
                "last_24h": queries_24h,
                "avg_duration_ms": round(avg_duration, 2),
                "avg_result_count": round(avg_results, 1),
            },
            "service_uptime": uptime,
            "service_query_hits": service_hit_counts,
            "cache_size": query_cache.size,
        },
        duration_ms=elapsed,
    )
