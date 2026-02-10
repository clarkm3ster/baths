from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import System, Gap, Bridge

router = APIRouter(prefix="/api/gaps", tags=["gaps"])


@router.get("")
def list_gaps(
    barrier_type: Optional[str] = Query(None, description="Filter by barrier type (legal, technical, political, consent, funding)"),
    severity: Optional[str] = Query(None, description="Filter by severity (critical, high, moderate, low)"),
    consent_closable: Optional[bool] = Query(None, description="Filter by whether gap can be closed with consent"),
    domain: Optional[str] = Query(None, description="Filter by domain of either system"),
    db: Session = Depends(get_db),
):
    """List all gaps with optional filtering."""
    query = db.query(Gap)

    if barrier_type:
        query = query.filter(Gap.barrier_type == barrier_type)
    if severity:
        query = query.filter(Gap.severity == severity)
    if consent_closable is not None:
        query = query.filter(Gap.consent_closable == consent_closable)
    if domain:
        # Join to systems to filter by domain
        system_ids = [
            s.id for s in db.query(System).filter(System.domain == domain).all()
        ]
        query = query.filter(
            (Gap.system_a_id.in_(system_ids)) | (Gap.system_b_id.in_(system_ids))
        )

    gaps = query.all()
    return [g.to_dict() for g in gaps]


@router.get("/{gap_id}")
def get_gap(gap_id: int, db: Session = Depends(get_db)):
    """Get a single gap with its systems and bridges."""
    gap = db.query(Gap).filter(Gap.id == gap_id).first()
    if not gap:
        raise HTTPException(status_code=404, detail=f"Gap {gap_id} not found")

    bridges = db.query(Bridge).filter(Bridge.gap_id == gap_id).order_by(Bridge.priority_score.desc()).all()

    return {
        **gap.to_dict(),
        "system_a": gap.system_a.to_dict() if gap.system_a else None,
        "system_b": gap.system_b.to_dict() if gap.system_b else None,
        "bridges": [b.to_dict() for b in bridges],
    }
