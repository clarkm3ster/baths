"""
Orchestrator routes for SPHERES Brain.

These endpoints are the primary API surface of the brain: unified parcel
queries, service listing, activity feed, webhook subscriptions, and
ecosystem-wide metrics.
"""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Query

from models.services import (
    ActivityEvent,
    ActivationMetrics,
    ParcelQuery,
    ServiceInfo,
    Subscription,
    SubscriptionResponse,
    UnifiedParcelResult,
)
from models.registry import SPHERES_SERVICES
from services.query_engine import UnifiedQueryEngine
from services.activity_tracker import ActivityTracker

router = APIRouter()

# ---------------------------------------------------------------------------
# Singletons (initialised in main.py startup and shared via app.state,
# but we also keep module-level defaults so the router works standalone)
# ---------------------------------------------------------------------------

_query_engine = UnifiedQueryEngine()
_activity_tracker = ActivityTracker()
_subscriptions: list[dict] = []


# ---------------------------------------------------------------------------
# POST /api/query — unified parcel lookup
# ---------------------------------------------------------------------------

@router.post("/api/query", response_model=UnifiedParcelResult)
async def query_parcel(query: ParcelQuery):
    """
    Execute a unified parcel query across all SPHERES services.

    Accepts either an address string, a parcel ID, or both.  The brain
    fans the query out to spheres-assets, spheres-legal, spheres-studio,
    and spheres-viz, then merges the responses into a single result.
    """
    result = await _query_engine.query_parcel(query)

    # Record the query as an activity event
    _activity_tracker.record(
        ActivityEvent(
            source_app="spheres-brain",
            event_type="unified_query",
            description=(
                f"Unified parcel query executed for "
                f"{query.address or query.parcel_id or 'unknown'}"
            ),
            parcel_id=result.parcel_data.parcel_id if result.parcel_data else None,
        )
    )

    return result


# ---------------------------------------------------------------------------
# GET /api/services — list registered services
# ---------------------------------------------------------------------------

@router.get("/api/services", response_model=list[ServiceInfo])
async def list_services():
    """
    Return metadata for every registered SPHERES micro-service,
    including endpoints, ports, and current health status.
    """
    return SPHERES_SERVICES


# ---------------------------------------------------------------------------
# GET /api/activity — recent ecosystem activity
# ---------------------------------------------------------------------------

@router.get("/api/activity", response_model=list[ActivityEvent])
async def get_activity(
    limit: int = Query(50, ge=1, le=200, description="Maximum events to return"),
    source: Optional[str] = Query(None, description="Filter by source app name"),
    parcel_id: Optional[str] = Query(None, description="Filter by parcel ID"),
):
    """
    Return recent activity events from across the SPHERES ecosystem.

    Optionally filter by source app or parcel ID.  Results are always
    sorted newest-first.
    """
    if source:
        return _activity_tracker.get_by_app(source)[:limit]
    if parcel_id:
        return _activity_tracker.get_by_parcel(parcel_id)[:limit]
    return _activity_tracker.get_recent(limit)


# ---------------------------------------------------------------------------
# POST /api/subscribe — webhook subscriptions
# ---------------------------------------------------------------------------

@router.post("/api/subscribe", response_model=SubscriptionResponse)
async def subscribe(subscription: Subscription):
    """
    Register a webhook subscription for ecosystem events.

    The subscriber provides a URL and a list of event types they are
    interested in.  The brain will POST event payloads to the URL
    whenever a matching event is recorded.
    """
    sub_id = f"sub-{uuid.uuid4().hex[:12]}"

    record = {
        "subscription_id": sub_id,
        "webhook_url": subscription.webhook_url,
        "events": subscription.events,
        "created_at": subscription.created_at,
        "active": subscription.active,
        "subscriber_name": subscription.subscriber_name,
    }
    _subscriptions.append(record)

    # Log the subscription as an activity event
    _activity_tracker.record(
        ActivityEvent(
            source_app="spheres-brain",
            event_type="subscription_created",
            description=(
                f"New webhook subscription '{subscription.subscriber_name or sub_id}' "
                f"registered for events: {', '.join(subscription.events) or 'all'}"
            ),
        )
    )

    return SubscriptionResponse(
        subscription_id=sub_id,
        webhook_url=subscription.webhook_url,
        events=subscription.events,
        created_at=subscription.created_at,
    )


# ---------------------------------------------------------------------------
# GET /api/metrics — ecosystem-wide activation metrics
# ---------------------------------------------------------------------------

@router.get("/api/metrics", response_model=ActivationMetrics)
async def get_metrics():
    """
    Return aggregate activation metrics computed from the event stream
    and baseline SPHERES data.
    """
    return _activity_tracker.get_metrics()
