from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import System, Connection, Gap

router = APIRouter(prefix="/api/systems", tags=["systems"])


@router.get("")
def list_systems(
    domain: Optional[str] = Query(None, description="Filter by domain (health, justice, housing, income, education)"),
    data_standard: Optional[str] = Query(None, description="Filter by data standard"),
    search: Optional[str] = Query(None, description="Search name, acronym, or description"),
    db: Session = Depends(get_db),
):
    """List all systems with optional filtering."""
    query = db.query(System)

    if domain:
        query = query.filter(System.domain == domain)
    if data_standard:
        query = query.filter(System.data_standard == data_standard)
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            (System.name.ilike(search_term))
            | (System.acronym.ilike(search_term))
            | (System.description.ilike(search_term))
        )

    systems = query.order_by(System.domain, System.name).all()
    return [s.to_dict() for s in systems]


@router.get("/{system_id}")
def get_system(system_id: str, db: Session = Depends(get_db)):
    """Get a single system with its connections and gaps."""
    system = db.query(System).filter(System.id == system_id).first()
    if not system:
        raise HTTPException(status_code=404, detail=f"System '{system_id}' not found")

    # Get connections where this system is source or target
    connections_out = db.query(Connection).filter(Connection.source_id == system_id).all()
    connections_in = db.query(Connection).filter(Connection.target_id == system_id).all()

    # Get gaps involving this system
    gaps = db.query(Gap).filter(
        (Gap.system_a_id == system_id) | (Gap.system_b_id == system_id)
    ).all()

    return {
        **system.to_dict(),
        "connections": [c.to_dict() for c in connections_out + connections_in],
        "gaps": [g.to_dict() for g in gaps],
    }
