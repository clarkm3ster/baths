"""
Bridge API routes — exposes the bridge analysis engine over HTTP.

Prefix: /api/bridges
"""

from typing import Optional

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import Bridge, Gap, System
from app.bridge_engine import (
    rank_bridges,
    get_top_bridges,
    get_consent_pathways,
    build_consent_checklist,
    aggregate_bridge_costs,
    cost_by_category,
    cost_by_barrier,
    sequence_bridges,
    bridges_for_person,
    consent_impact_for_person,
    quick_wins,
)

router = APIRouter(prefix="/api/bridges", tags=["bridges"])


# ---------------------------------------------------------------------------
# Dependency
# ---------------------------------------------------------------------------

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------------------------------------------------------------------
# Request Bodies
# ---------------------------------------------------------------------------

class ConsentPathwayRequest(BaseModel):
    circumstances: list[str]


class BuildPlanRequest(BaseModel):
    bridge_ids: list[int]


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def _bridge_with_gap(bridge: Bridge) -> dict:
    """Serialize a bridge with gap info including system names."""
    data = bridge.to_dict()
    gap = bridge.gap
    if gap:
        data["gap"] = {
            "id": gap.id,
            "system_a_id": gap.system_a_id,
            "system_b_id": gap.system_b_id,
            "system_a_name": gap.system_a.name if gap.system_a else gap.system_a_id,
            "system_b_name": gap.system_b.name if gap.system_b else gap.system_b_id,
            "barrier_type": gap.barrier_type,
            "severity": gap.severity,
            "consent_closable": gap.consent_closable,
        }
    return data


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@router.get("")
def list_bridges(
    bridge_type: Optional[str] = Query(None, description="Filter by bridge type"),
    status: Optional[str] = Query(None, description="Filter by status"),
    min_priority: Optional[float] = Query(None, description="Minimum priority score"),
    gap_id: Optional[int] = Query(None, description="Filter by gap ID"),
    db: Session = Depends(get_db),
):
    """List all bridges matching filters, sorted by priority_score descending.

    Each bridge includes gap info with system names and severity.
    """
    query = db.query(Bridge)

    if bridge_type:
        query = query.filter(Bridge.bridge_type == bridge_type)
    if status:
        query = query.filter(Bridge.status == status)
    if min_priority is not None:
        query = query.filter(Bridge.priority_score >= min_priority)
    if gap_id is not None:
        query = query.filter(Bridge.gap_id == gap_id)

    bridges = query.all()
    ranked = rank_bridges(bridges)

    return [_bridge_with_gap(b) for b in ranked]


@router.get("/priority")
def priority_bridges(
    limit: int = Query(20, ge=1, le=100, description="Number of results"),
    offset: int = Query(0, ge=0, description="Pagination offset"),
    db: Session = Depends(get_db),
):
    """Top bridges by priority_score with pagination.

    Returns the top bridges globally and a total count for pagination.
    """
    # Get total count
    total = db.query(func.count(Bridge.id)).scalar() or 0

    # Get all, rank, then paginate (ranking needs full list for proper sort)
    all_bridges = db.query(Bridge).all()
    ranked = rank_bridges(all_bridges)

    page = ranked[offset : offset + limit]

    return {
        "total": total,
        "limit": limit,
        "offset": offset,
        "bridges": [_bridge_with_gap(b) for b in page],
    }


@router.get("/quick-wins")
def get_quick_wins(
    circumstances: Optional[str] = Query(
        None,
        description="Comma-separated circumstances for filtering",
    ),
    db: Session = Depends(get_db),
):
    """Bridges where effort <= 3 and impact >= 7 (high impact, low effort).

    Optionally filter by circumstances (comma-separated string).
    """
    circ_list = None
    if circumstances:
        circ_list = [c.strip() for c in circumstances.split(",") if c.strip()]

    results = quick_wins(db, circ_list)
    return results


@router.get("/costs")
def get_costs(
    bridge_type: Optional[str] = Query(None, description="Filter by bridge type"),
    db: Session = Depends(get_db),
):
    """Cost breakdown: by type, by barrier, totals.

    Returns a comprehensive cost analysis across all bridges.
    """
    by_type_data = cost_by_category(db, bridge_type)
    by_barrier_data = cost_by_barrier(db)

    return {
        "by_type": by_type_data["by_type"],
        "by_barrier": by_barrier_data["by_barrier"],
        "total_min": by_type_data["total_min"],
        "total_max": by_type_data["total_max"],
        "formatted_total": by_type_data["formatted_total"],
    }


@router.get("/stats")
def get_stats(db: Session = Depends(get_db)):
    """Aggregate statistics across all bridges.

    Returns counts, averages, and breakdowns.
    """
    all_bridges = db.query(Bridge).all()
    total = len(all_bridges)

    if total == 0:
        return {
            "total_bridges": 0,
            "by_type": {},
            "by_status": {},
            "avg_priority": 0,
            "avg_impact": 0,
            "avg_effort": 0,
            "consent_bridge_count": 0,
            "quick_win_count": 0,
        }

    # Count by type
    by_type: dict[str, int] = {}
    by_status: dict[str, int] = {}
    consent_count = 0
    quick_win_count = 0
    priority_sum = 0.0
    impact_sum = 0.0
    effort_sum = 0.0

    for b in all_bridges:
        by_type[b.bridge_type] = by_type.get(b.bridge_type, 0) + 1
        by_status[b.status] = by_status.get(b.status, 0) + 1

        if b.bridge_type == "consent":
            consent_count += 1
        if b.effort_score <= 3.0 and b.impact_score >= 7.0:
            quick_win_count += 1

        priority_sum += b.priority_score
        impact_sum += b.impact_score
        effort_sum += b.effort_score

    return {
        "total_bridges": total,
        "by_type": by_type,
        "by_status": by_status,
        "avg_priority": round(priority_sum / total, 2),
        "avg_impact": round(impact_sum / total, 2),
        "avg_effort": round(effort_sum / total, 2),
        "consent_bridge_count": consent_count,
        "quick_win_count": quick_win_count,
    }


@router.get("/{gap_id}")
def bridges_for_gap(
    gap_id: int,
    db: Session = Depends(get_db),
):
    """All bridges for a specific gap, sorted by priority.

    Includes full gap details and system names.
    """
    gap = db.query(Gap).filter(Gap.id == gap_id).first()
    if not gap:
        return {"error": "Gap not found", "gap_id": gap_id}

    bridges = rank_bridges(list(gap.bridges))

    gap_data = gap.to_dict()
    gap_data["system_a_name"] = gap.system_a.name if gap.system_a else gap.system_a_id
    gap_data["system_b_name"] = gap.system_b.name if gap.system_b else gap.system_b_id

    return {
        "gap": gap_data,
        "bridges": [b.to_dict() for b in bridges],
    }


@router.post("/consent-pathway")
def consent_pathway(
    body: ConsentPathwayRequest,
    db: Session = Depends(get_db),
):
    """Analyze consent pathways for a person's circumstances.

    Returns consent bridges, a checklist of forms to sign, the number of
    closable gaps, and an impact summary.
    """
    circumstances = body.circumstances

    consent_bridges = get_consent_pathways(db, circumstances)
    checklist = build_consent_checklist(db, circumstances)
    impact = consent_impact_for_person(db, circumstances)

    # Build impact summary
    total_bridges_available = sum(len(p["bridges"]) for p in consent_bridges)

    return {
        "consent_bridges": consent_bridges,
        "checklist": checklist,
        "total_gaps_closable": impact["consent_closable_gaps"],
        "total_applicable_gaps": impact["total_applicable_gaps"],
        "percentage_closable": impact["percentage_closable_by_consent"],
        "total_consent_bridges": total_bridges_available,
        "impact_summary": {
            "total_impact_score": impact["total_consent_impact"],
            "description": (
                f"By signing consent forms, {impact['consent_closable_gaps']} of "
                f"{impact['total_applicable_gaps']} data gaps applicable to your "
                f"situation ({impact['percentage_closable_by_consent']}%) could be "
                f"bridged."
            ),
        },
    }


@router.post("/build-plan")
def build_plan(
    body: BuildPlanRequest,
    db: Session = Depends(get_db),
):
    """Build a phased implementation plan for selected bridges.

    Returns phases with bridges grouped by type, per-phase cost and timeline,
    and cumulative impact tracking.
    """
    plan = sequence_bridges(body.bridge_ids, db)
    return plan
