"""
Discovery routes for SPHERES Brain.

Exposes the discovery scanner's and opportunity scorer's capabilities
through REST endpoints: discoveries, opportunity scoring, policy changes,
comparable-city innovations, media mentions, infrastructure changes, and
a unified full scan.

Required endpoints
------------------
GET  /api/discoveries         — All discoveries as a flat list
GET  /api/discoveries/feed    — Time-sorted feed (newest first)
GET  /api/opportunities       — Top scored opportunities (default 10)
GET  /api/opportunities/{id}  — Single opportunity by ID
POST /api/scan                — Trigger full scan, return summary
GET  /api/policy              — Recent policy changes
GET  /api/comparable          — Comparable city innovations

Legacy / extra endpoints (from earlier iteration)
-------------------------------------------------
GET  /api/discovery/parcels         — Newly discovered parcels
GET  /api/discovery/policies        — Policy changes (alias)
GET  /api/discovery/comparables     — Comparable cities (alias)
GET  /api/discovery/media           — Media mentions
GET  /api/discovery/infrastructure  — Infrastructure changes
GET  /api/discovery/scan            — Full scan (GET alias)
GET  /api/discovery/all             — All discoveries (alias)
"""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query

from models.discovery import (
    ComparableCity,
    Discovery,
    Opportunity,
    PolicyUpdate,
    ScanResult,
)
from services.discovery_scanner import DiscoveryScanner
from services.opportunity_scorer import OpportunityScorer

router = APIRouter()

_scanner = DiscoveryScanner()
_scorer = OpportunityScorer()


# ===================================================================
# REQUIRED ENDPOINTS
# ===================================================================


# ---------------------------------------------------------------------------
# GET /api/discoveries — all discoveries as a flat list
# ---------------------------------------------------------------------------

@router.get("/api/discoveries", response_model=list[Discovery])
async def list_discoveries(
    min_relevance: int = Query(0, ge=0, le=100, description="Minimum relevance score"),
):
    """
    Return every discovery from all scan types (parcels, policy, media,
    comparable cities, infrastructure) as a single list, sorted by
    relevance score descending.  Optionally filter by minimum relevance.
    """
    discoveries = _scanner.get_all_discoveries()
    if min_relevance > 0:
        discoveries = [d for d in discoveries if d.relevance_score >= min_relevance]
    return sorted(discoveries, key=lambda d: d.relevance_score, reverse=True)


# ---------------------------------------------------------------------------
# GET /api/discoveries/feed — time-sorted feed (newest first)
# ---------------------------------------------------------------------------

@router.get("/api/discoveries/feed", response_model=list[Discovery])
async def discovery_feed(
    limit: int = Query(20, ge=1, le=100, description="Max items to return"),
):
    """
    Time-sorted feed of recent discoveries, newest first.
    Useful for dashboard widgets and notification streams.
    """
    all_discoveries = _scanner.get_all_discoveries()
    sorted_discoveries = sorted(
        all_discoveries,
        key=lambda d: d.discovered_at,
        reverse=True,
    )
    return sorted_discoveries[:limit]


# ---------------------------------------------------------------------------
# GET /api/opportunities — top scored opportunities
# ---------------------------------------------------------------------------

@router.get("/api/opportunities", response_model=list[Opportunity])
async def list_opportunities(
    limit: int = Query(10, ge=1, le=50, description="Max opportunities to return"),
):
    """
    Return the top scored activation opportunities, ranked by composite
    score (highest first).  Default limit is 10.  Each opportunity
    includes five scoring factors: location, permit_readiness,
    community_demand, seasonal_fit, and cost_efficiency.
    """
    return _scorer.get_top_opportunities(limit=limit)


# ---------------------------------------------------------------------------
# GET /api/opportunities/{id} — single opportunity by ID
# ---------------------------------------------------------------------------

@router.get("/api/opportunities/{opportunity_id}", response_model=Opportunity)
async def get_opportunity(opportunity_id: str):
    """
    Look up a single scored opportunity by its ID.  Returns 404 if the
    opportunity does not exist in the scorer's registry.
    """
    opp = _scorer.get_opportunity_by_id(opportunity_id)
    if opp is None:
        raise HTTPException(
            status_code=404,
            detail=f"Opportunity '{opportunity_id}' not found",
        )
    return opp


# ---------------------------------------------------------------------------
# POST /api/scan — trigger a full scan
# ---------------------------------------------------------------------------

@router.post("/api/scan", response_model=list[ScanResult])
async def trigger_scan():
    """
    Execute all scan types (parcels, policies, media, infrastructure,
    comparable cities) and return summary results with item counts and
    next-scan timestamps.
    """
    return _scanner.run_full_scan()


# ---------------------------------------------------------------------------
# GET /api/policy — recent policy changes
# ---------------------------------------------------------------------------

@router.get("/api/policy", response_model=list[PolicyUpdate])
async def list_policy_changes():
    """
    Return recent city policy updates, zoning amendments, and regulatory
    changes that affect public-space activation potential in Philadelphia.
    """
    return _scanner.scan_policy_changes()


# ---------------------------------------------------------------------------
# GET /api/comparable — comparable city innovations
# ---------------------------------------------------------------------------

@router.get("/api/comparable", response_model=list[ComparableCity])
async def list_comparable_cities():
    """
    Return innovations from comparable cities that could inform or
    inspire Philadelphia's public-space activation strategy.
    """
    return _scanner.scan_comparable_cities()


# ===================================================================
# LEGACY / EXTRA ENDPOINTS (preserved from earlier iteration)
# ===================================================================


@router.get("/api/discovery/parcels", response_model=list[Discovery])
async def discover_parcels():
    """Return recently discovered vacant or city-owned parcels."""
    return _scanner.scan_new_parcels()


@router.get("/api/discovery/policies", response_model=list[PolicyUpdate])
async def discover_policies():
    """Return recent policy updates (alias for /api/policy)."""
    return _scanner.scan_policy_changes()


@router.get("/api/discovery/comparables", response_model=list[ComparableCity])
async def discover_comparables():
    """Return comparable city innovations (alias for /api/comparable)."""
    return _scanner.scan_comparable_cities()


@router.get("/api/discovery/media", response_model=list[Discovery])
async def discover_media():
    """Return recent news and media mentions about Philadelphia public space."""
    return _scanner.scan_media()


@router.get("/api/discovery/infrastructure", response_model=list[Discovery])
async def discover_infrastructure():
    """Return infrastructure changes near potential activation sites."""
    return _scanner.scan_infrastructure_changes()


@router.get("/api/discovery/scan", response_model=list[ScanResult])
async def run_full_scan_get():
    """Execute all scan types (GET alias for POST /api/scan)."""
    return _scanner.run_full_scan()


@router.get("/api/discovery/all", response_model=list[Discovery])
async def all_discoveries_legacy(
    min_relevance: int = Query(0, ge=0, le=100, description="Minimum relevance score"),
):
    """Return all discoveries (alias for /api/discoveries)."""
    discoveries = _scanner.get_all_discoveries()
    if min_relevance > 0:
        discoveries = [d for d in discoveries if d.relevance_score >= min_relevance]
    return sorted(discoveries, key=lambda d: d.relevance_score, reverse=True)
