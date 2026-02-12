"""
FastAPI router for the DOMES Discovery Engine.

Prefix: /api/discoveries
All endpoints return the standard envelope: { status, data, meta }.
"""

from __future__ import annotations

import logging
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from discovery_db import (
    create_discovery,
    discovery_url_exists,
    get_db,
    get_discoveries,
    get_discovery_by_id,
    get_queue,
    get_sources,
    get_stats,
    update_discovery_status,
    update_source_last_scanned,
)
from discovery_models import (
    ApiResponse,
    DiscoveryStatus,
    DiscoveryStatusUpdate,
    ImpactLevel,
    ResponseMeta,
    SourceType,
)
from scanners import run_scanner_and_collect

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/discoveries", tags=["discoveries"])


# ---------------------------------------------------------------------------
# GET /api/discoveries — list with filters & pagination
# ---------------------------------------------------------------------------

@router.get("", response_model=ApiResponse)
async def list_discoveries(
    source_type: Optional[SourceType] = Query(None, description="Filter by source type"),
    impact_level: Optional[ImpactLevel] = Query(None, description="Filter by impact level"),
    status: Optional[DiscoveryStatus] = Query(None, description="Filter by status"),
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    """Return a paginated, filterable list of discoveries."""
    records, total = get_discoveries(
        db,
        source_type=source_type.value if source_type else None,
        impact_level=impact_level.value if impact_level else None,
        status=status.value if status else None,
        limit=limit,
        offset=offset,
    )
    return ApiResponse(
        data=[r.to_pydantic().model_dump(mode="json") for r in records],
        meta=ResponseMeta(count=total),
    )


# ---------------------------------------------------------------------------
# GET /api/discoveries/queue — priority queue
# ---------------------------------------------------------------------------

@router.get("/queue", response_model=ApiResponse)
async def discovery_queue(
    limit: int = Query(50, ge=1, le=500),
    db: Session = Depends(get_db),
):
    """
    Priority queue of discoveries pending review, ordered by
    relevance_score descending.
    """
    records = get_queue(db, limit=limit)
    return ApiResponse(
        data=[r.to_pydantic().model_dump(mode="json") for r in records],
        meta=ResponseMeta(count=len(records)),
    )


# ---------------------------------------------------------------------------
# GET /api/discoveries/sources — scanner source configs
# ---------------------------------------------------------------------------

@router.get("/sources", response_model=ApiResponse)
async def list_sources(db: Session = Depends(get_db)):
    """List all scanner sources with last-scan timestamps."""
    records = get_sources(db)
    return ApiResponse(
        data=[r.to_pydantic().model_dump(mode="json") for r in records],
        meta=ResponseMeta(count=len(records)),
    )


# ---------------------------------------------------------------------------
# GET /api/discoveries/stats — aggregate counts
# ---------------------------------------------------------------------------

@router.get("/stats", response_model=ApiResponse)
async def discovery_stats(db: Session = Depends(get_db)):
    """Aggregate discovery counts by source, impact, and status."""
    stats = get_stats(db)
    return ApiResponse(
        data=stats.model_dump(),
        meta=ResponseMeta(count=stats.total),
    )


# ---------------------------------------------------------------------------
# POST /api/discoveries/scan — trigger a scan
# ---------------------------------------------------------------------------

@router.post("/scan", response_model=ApiResponse)
async def trigger_scan(
    source_type: Optional[SourceType] = Query(None, description="Scan a specific source type, or omit for all"),
    db: Session = Depends(get_db),
):
    """
    Trigger a scan.  Optionally scope to a single source_type.
    Persists new (de-duped) discoveries and returns scan result summaries.
    """
    stype = source_type.value if source_type else None
    discoveries, scan_results = await run_scanner_and_collect(stype)

    # Persist discoveries, skipping duplicates by URL
    new_count = 0
    for disc in discoveries:
        if not discovery_url_exists(db, disc.url):
            create_discovery(db, disc)
            new_count += 1

    # Update last_scanned timestamps on sources
    for sr in scan_results:
        update_source_last_scanned(db, sr.source_name)

    # Adjust new_items counts to reflect actual inserts
    result_data = []
    for sr in scan_results:
        result_data.append(sr.model_dump(mode="json"))

    return ApiResponse(
        data={
            "scan_results": result_data,
            "total_found": sum(sr.items_found for sr in scan_results),
            "new_persisted": new_count,
        },
        meta=ResponseMeta(count=len(scan_results)),
    )


# ---------------------------------------------------------------------------
# GET /api/discoveries/{id} — single discovery detail
# ---------------------------------------------------------------------------

@router.get("/{discovery_id}", response_model=ApiResponse)
async def get_single_discovery(
    discovery_id: int,
    db: Session = Depends(get_db),
):
    """Retrieve a single discovery by ID."""
    record = get_discovery_by_id(db, discovery_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Discovery not found")
    return ApiResponse(
        data=record.to_pydantic().model_dump(mode="json"),
        meta=ResponseMeta(count=1),
    )


# ---------------------------------------------------------------------------
# PATCH /api/discoveries/{id} — update status
# ---------------------------------------------------------------------------

@router.patch("/{discovery_id}", response_model=ApiResponse)
async def patch_discovery_status(
    discovery_id: int,
    body: DiscoveryStatusUpdate,
    db: Session = Depends(get_db),
):
    """
    Update a discovery's status.
    Valid transitions: new -> reviewed | queued | dismissed,
    reviewed -> queued | ingested | dismissed, etc.
    """
    record = update_discovery_status(db, discovery_id, body.status.value)
    if record is None:
        raise HTTPException(status_code=404, detail="Discovery not found")
    return ApiResponse(
        data=record.to_pydantic().model_dump(mode="json"),
        meta=ResponseMeta(count=1),
    )
