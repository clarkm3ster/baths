from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import System, Connection

router = APIRouter(prefix="/api/connections", tags=["connections"])


@router.get("")
def list_connections(
    source_id: Optional[str] = Query(None, description="Filter by source system ID"),
    target_id: Optional[str] = Query(None, description="Filter by target system ID"),
    format: Optional[str] = Query(None, description="Filter by data format"),
    reliability: Optional[str] = Query(None, description="Filter by reliability level"),
    db: Session = Depends(get_db),
):
    """List all connections with optional filtering."""
    query = db.query(Connection)

    if source_id:
        query = query.filter(Connection.source_id == source_id)
    if target_id:
        query = query.filter(Connection.target_id == target_id)
    if format:
        query = query.filter(Connection.format == format)
    if reliability:
        query = query.filter(Connection.reliability == reliability)

    connections = query.all()
    return [c.to_dict() for c in connections]


@router.get("/matrix")
def get_connection_matrix(db: Session = Depends(get_db)):
    """Return a matrix of system-to-system connections for the frontend grid.

    Returns:
        {
            systems: [{ id, name, acronym, domain }, ...],
            matrix: [[connection_or_null, ...], ...]
        }
    where matrix[i][j] represents the connection from systems[i] to systems[j].
    """
    systems = db.query(System).order_by(System.domain, System.name).all()
    connections = db.query(Connection).all()

    # Build lookup: (source_id, target_id) -> connection dict
    conn_lookup: dict[tuple[str, str], dict] = {}
    for c in connections:
        conn_dict = c.to_dict()
        conn_lookup[(c.source_id, c.target_id)] = conn_dict
        # For bidirectional connections, also map the reverse
        if c.direction == "bidirectional":
            conn_lookup[(c.target_id, c.source_id)] = conn_dict

    system_list = [
        {"id": s.id, "name": s.name, "acronym": s.acronym, "domain": s.domain}
        for s in systems
    ]

    matrix = []
    for i, sys_i in enumerate(systems):
        row = []
        for j, sys_j in enumerate(systems):
            if i == j:
                row.append(None)
            else:
                conn = conn_lookup.get((sys_i.id, sys_j.id))
                row.append(conn)
        matrix.append(row)

    return {"systems": system_list, "matrix": matrix}
