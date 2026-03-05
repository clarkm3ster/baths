"""
DOMES Innovation Laboratory — API Routes.

All endpoints live under the /api prefix and return responses in the
standard envelope format: {"status": "ok", "data": ...}
"""

import json
from datetime import datetime, timezone
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from sqlalchemy import func
from sqlalchemy.orm import Session

from database import get_db
from generator import generate_innovation
from models import Collaboration, Innovation, LabSession, Teammate

router = APIRouter(prefix="/api")


# ── Response helpers ────────────────────────────────────────────────────────

def ok(data: Any) -> dict:
    """Wrap *data* in the standard envelope."""
    return {"status": "ok", "data": data}


def err(message: str, code: int = 400) -> None:
    """Raise an HTTPException with envelope-style detail."""
    raise HTTPException(status_code=code, detail={"status": "error", "message": message})


# ── Pydantic request bodies ────────────────────────────────────────────────

class InnovationCreate(BaseModel):
    teammate_id: int
    title: str
    summary: str = ""
    category: str = "general"
    impact_level: int = Field(3, ge=1, le=5)
    feasibility: int = Field(3, ge=1, le=5)
    novelty: int = Field(3, ge=1, le=5)
    time_horizon: str = "medium"
    status: str = "draft"
    details: dict = Field(default_factory=dict)
    tags: list[str] = Field(default_factory=list)


class InnovationUpdate(BaseModel):
    title: str | None = None
    summary: str | None = None
    category: str | None = None
    impact_level: int | None = Field(None, ge=1, le=5)
    feasibility: int | None = Field(None, ge=1, le=5)
    novelty: int | None = Field(None, ge=1, le=5)
    time_horizon: str | None = None
    status: str | None = None
    details: dict | None = None
    tags: list[str] | None = None


class CollaborationCreate(BaseModel):
    title: str
    summary: str = ""
    teammate_ids: list[int] = Field(default_factory=list)
    innovations: list[dict] = Field(default_factory=list)


class LabSessionCreate(BaseModel):
    name: str
    focus_domain: str = "general"
    participants: list[str] = Field(default_factory=list)


# ── Teammates ───────────────────────────────────────────────────────────────

@router.get("/teammates")
def list_teammates(db: Session = Depends(get_db)):
    """List all teammates with innovation counts."""
    teammates = db.query(Teammate).order_by(Teammate.id).all()
    return ok([t.to_dict() for t in teammates])


@router.get("/teammates/{slug}")
def get_teammate(slug: str, db: Session = Depends(get_db)):
    """Get a single teammate with their innovations."""
    teammate = db.query(Teammate).filter(Teammate.slug == slug).first()
    if not teammate:
        err(f"Teammate '{slug}' not found", 404)
    return ok(teammate.to_dict(include_innovations=True))


# ── Innovations ─────────────────────────────────────────────────────────────

@router.get("/innovations")
def list_innovations(
    domain: str | None = Query(None),
    status: str | None = Query(None),
    impact_level: int | None = Query(None, ge=1, le=5),
    time_horizon: str | None = Query(None),
    db: Session = Depends(get_db),
):
    """List innovations with optional filters."""
    q = db.query(Innovation)

    if domain:
        q = q.filter(Innovation.domain == domain)
    if status:
        q = q.filter(Innovation.status == status)
    if impact_level:
        q = q.filter(Innovation.impact_level >= impact_level)
    if time_horizon:
        q = q.filter(Innovation.time_horizon == time_horizon)

    innovations = q.order_by(Innovation.created_at.desc()).all()
    return ok([i.to_dict() for i in innovations])


@router.get("/innovations/{innovation_id}")
def get_innovation(innovation_id: int, db: Session = Depends(get_db)):
    """Get a single innovation by ID."""
    innovation = db.query(Innovation).filter(Innovation.id == innovation_id).first()
    if not innovation:
        err("Innovation not found", 404)
    return ok(innovation.to_dict())


@router.post("/innovations")
def create_innovation(body: InnovationCreate, db: Session = Depends(get_db)):
    """Create a new innovation."""
    teammate = db.query(Teammate).filter(Teammate.id == body.teammate_id).first()
    if not teammate:
        err(f"Teammate with id {body.teammate_id} not found", 404)

    innovation = Innovation(
        teammate_id=body.teammate_id,
        title=body.title,
        summary=body.summary,
        domain=teammate.domain,
        category=body.category,
        impact_level=body.impact_level,
        feasibility=body.feasibility,
        novelty=body.novelty,
        time_horizon=body.time_horizon,
        status=body.status,
        details=json.dumps(body.details),
        tags=",".join(body.tags),
    )
    db.add(innovation)
    db.commit()
    db.refresh(innovation)
    return ok(innovation.to_dict())


@router.patch("/innovations/{innovation_id}")
def update_innovation(
    innovation_id: int, body: InnovationUpdate, db: Session = Depends(get_db)
):
    """Update an innovation's status, scores, or content."""
    innovation = db.query(Innovation).filter(Innovation.id == innovation_id).first()
    if not innovation:
        err("Innovation not found", 404)

    update_data = body.model_dump(exclude_none=True)

    # Handle special fields
    if "details" in update_data:
        update_data["details"] = json.dumps(update_data["details"])
    if "tags" in update_data:
        update_data["tags"] = ",".join(update_data["tags"])

    for field, value in update_data.items():
        setattr(innovation, field, value)

    innovation.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(innovation)
    return ok(innovation.to_dict())


# ── Collaborations ──────────────────────────────────────────────────────────

@router.get("/collaborations")
def list_collaborations(db: Session = Depends(get_db)):
    """List all cross-domain collaborations."""
    collaborations = db.query(Collaboration).order_by(Collaboration.created_at.desc()).all()
    return ok([c.to_dict() for c in collaborations])


@router.post("/collaborations")
def create_collaboration(body: CollaborationCreate, db: Session = Depends(get_db)):
    """Create a new cross-domain collaboration."""
    collaboration = Collaboration(
        title=body.title,
        summary=body.summary,
        teammate_ids=",".join(str(tid) for tid in body.teammate_ids),
        innovations=json.dumps(body.innovations),
    )
    db.add(collaboration)
    db.commit()
    db.refresh(collaboration)
    return ok(collaboration.to_dict())


# ── Lab Sessions ────────────────────────────────────────────────────────────

@router.get("/sessions")
def list_sessions(db: Session = Depends(get_db)):
    """List all lab sessions."""
    sessions = db.query(LabSession).order_by(LabSession.started_at.desc().nulls_last()).all()
    return ok([s.to_dict() for s in sessions])


@router.post("/sessions")
def create_session(body: LabSessionCreate, db: Session = Depends(get_db)):
    """Create a new lab session."""
    session = LabSession(
        name=body.name,
        focus_domain=body.focus_domain,
        participants=",".join(body.participants),
        started_at=datetime.now(timezone.utc),
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    return ok(session.to_dict())


# ── Stats ───────────────────────────────────────────────────────────────────

@router.get("/stats")
def get_stats(db: Session = Depends(get_db)):
    """Aggregate statistics across the entire lab."""
    total_innovations = db.query(func.count(Innovation.id)).scalar() or 0
    total_teammates = db.query(func.count(Teammate.id)).scalar() or 0
    total_collaborations = db.query(func.count(Collaboration.id)).scalar() or 0
    total_sessions = db.query(func.count(LabSession.id)).scalar() or 0

    avg_impact = db.query(func.avg(Innovation.impact_level)).scalar() or 0
    avg_feasibility = db.query(func.avg(Innovation.feasibility)).scalar() or 0
    avg_novelty = db.query(func.avg(Innovation.novelty)).scalar() or 0

    # Domain breakdown
    domain_rows = (
        db.query(Innovation.domain, func.count(Innovation.id))
        .group_by(Innovation.domain)
        .all()
    )
    domain_breakdown = {row[0]: row[1] for row in domain_rows}

    # Status breakdown
    status_rows = (
        db.query(Innovation.status, func.count(Innovation.id))
        .group_by(Innovation.status)
        .all()
    )
    status_breakdown = {row[0]: row[1] for row in status_rows}

    # Time horizon breakdown
    horizon_rows = (
        db.query(Innovation.time_horizon, func.count(Innovation.id))
        .group_by(Innovation.time_horizon)
        .all()
    )
    horizon_breakdown = {row[0]: row[1] for row in horizon_rows}

    # Recent innovations (last 10)
    recent = (
        db.query(Innovation)
        .order_by(Innovation.created_at.desc())
        .limit(10)
        .all()
    )

    return ok({
        "totals": {
            "innovations": total_innovations,
            "teammates": total_teammates,
            "collaborations": total_collaborations,
            "sessions": total_sessions,
        },
        "averages": {
            "impact_level": round(float(avg_impact), 2),
            "feasibility": round(float(avg_feasibility), 2),
            "novelty": round(float(avg_novelty), 2),
        },
        "domain_breakdown": domain_breakdown,
        "status_breakdown": status_breakdown,
        "horizon_breakdown": horizon_breakdown,
        "recent_innovations": [i.to_dict() for i in recent],
    })


# ── Generator ───────────────────────────────────────────────────────────────

@router.post("/generate/{slug}")
def trigger_generation(slug: str, db: Session = Depends(get_db)):
    """Generate a new innovation for the specified teammate."""
    teammate = db.query(Teammate).filter(Teammate.slug == slug).first()
    if not teammate:
        err(f"Teammate '{slug}' not found", 404)

    # Mark teammate as generating
    teammate.status = "generating"
    db.commit()

    innovation = generate_innovation(db, slug)

    # Reset teammate status
    teammate.status = "active"
    db.commit()

    if not innovation:
        err("Failed to generate innovation — no templates available for this domain", 500)

    return ok(innovation.to_dict())
