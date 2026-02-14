"""
SPHERES Innovation Laboratory — API Routes.
All endpoints return {"status": "ok", "data": ...} envelope.
"""

from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import get_db
from generator import generate_innovation
from models import Collaboration, Innovation, LabSession, Teammate

router = APIRouter(prefix="/api")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def ok(data):
    return {"status": "ok", "data": data}


def err(msg: str, code: int = 400):
    raise HTTPException(status_code=code, detail=msg)


# ---------------------------------------------------------------------------
# Request bodies
# ---------------------------------------------------------------------------

class InnovationCreate(BaseModel):
    teammate_id: int
    title: str
    summary: str
    category: str = "general"
    impact_level: int = 3
    feasibility: int = 3
    novelty: int = 3
    time_horizon: str = "medium"
    status: str = "draft"
    details: dict = {}
    tags: list[str] = []


class InnovationUpdate(BaseModel):
    title: str | None = None
    summary: str | None = None
    category: str | None = None
    impact_level: int | None = None
    feasibility: int | None = None
    novelty: int | None = None
    time_horizon: str | None = None
    status: str | None = None
    details: dict | None = None
    tags: list[str] | None = None


class CollaborationCreate(BaseModel):
    title: str
    summary: str
    teammate_ids: list[int] = []
    innovations: list[dict] = []


class LabSessionCreate(BaseModel):
    name: str
    focus_domain: str
    participants: list[str] = []


# ---------------------------------------------------------------------------
# Teammates
# ---------------------------------------------------------------------------

@router.get("/teammates")
def list_teammates(db: Session = Depends(get_db)):
    teammates = db.query(Teammate).all()
    return ok([t.to_dict() for t in teammates])


@router.get("/teammates/{slug}")
def get_teammate(slug: str, db: Session = Depends(get_db)):
    t = db.query(Teammate).filter_by(slug=slug).first()
    if not t:
        err("Teammate not found", 404)
    return ok(t.to_dict(include_innovations=True))


# ---------------------------------------------------------------------------
# Innovations
# ---------------------------------------------------------------------------

@router.get("/innovations")
def list_innovations(
    domain: str | None = Query(None),
    status: str | None = Query(None),
    impact_level: int | None = Query(None),
    time_horizon: str | None = Query(None),
    db: Session = Depends(get_db),
):
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
    i = db.query(Innovation).filter_by(id=innovation_id).first()
    if not i:
        err("Innovation not found", 404)
    return ok(i.to_dict())


@router.post("/innovations")
def create_innovation(body: InnovationCreate, db: Session = Depends(get_db)):
    import json
    innovation = Innovation(
        teammate_id=body.teammate_id,
        title=body.title,
        summary=body.summary,
        domain=db.query(Teammate).filter_by(id=body.teammate_id).first().domain if db.query(Teammate).filter_by(id=body.teammate_id).first() else "unknown",
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
def update_innovation(innovation_id: int, body: InnovationUpdate, db: Session = Depends(get_db)):
    import json
    i = db.query(Innovation).filter_by(id=innovation_id).first()
    if not i:
        err("Innovation not found", 404)
    for field, value in body.model_dump(exclude_none=True).items():
        if field == "details":
            setattr(i, field, json.dumps(value))
        elif field == "tags":
            setattr(i, field, ",".join(value))
        else:
            setattr(i, field, value)
    i.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(i)
    return ok(i.to_dict())


# ---------------------------------------------------------------------------
# Collaborations
# ---------------------------------------------------------------------------

@router.get("/collaborations")
def list_collaborations(db: Session = Depends(get_db)):
    collabs = db.query(Collaboration).all()
    return ok([c.to_dict() for c in collabs])


@router.post("/collaborations")
def create_collaboration(body: CollaborationCreate, db: Session = Depends(get_db)):
    import json
    collab = Collaboration(
        title=body.title,
        summary=body.summary,
        teammate_ids=",".join(str(x) for x in body.teammate_ids),
        innovations=json.dumps(body.innovations),
    )
    db.add(collab)
    db.commit()
    db.refresh(collab)
    return ok(collab.to_dict())


# ---------------------------------------------------------------------------
# Lab Sessions
# ---------------------------------------------------------------------------

@router.get("/sessions")
def list_sessions(db: Session = Depends(get_db)):
    sessions = db.query(LabSession).all()
    return ok([s.to_dict() for s in sessions])


@router.post("/sessions")
def create_session(body: LabSessionCreate, db: Session = Depends(get_db)):
    import json
    session = LabSession(
        name=body.name,
        focus_domain=body.focus_domain,
        participants=",".join(body.participants),
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    return ok(session.to_dict())


# ---------------------------------------------------------------------------
# Stats
# ---------------------------------------------------------------------------

@router.get("/stats")
def get_stats(db: Session = Depends(get_db)):
    innovations = db.query(Innovation).all()
    teammates = db.query(Teammate).all()

    total = len(innovations)
    avg_impact = sum(i.impact_level for i in innovations) / total if total else 0
    avg_feasibility = sum(i.feasibility for i in innovations) / total if total else 0
    avg_novelty = sum(i.novelty for i in innovations) / total if total else 0

    domain_breakdown = {}
    status_breakdown = {}
    horizon_breakdown = {}

    for i in innovations:
        domain_breakdown[i.domain] = domain_breakdown.get(i.domain, 0) + 1
        status_breakdown[i.status] = status_breakdown.get(i.status, 0) + 1
        horizon_breakdown[i.time_horizon] = horizon_breakdown.get(i.time_horizon, 0) + 1

    recent = sorted(innovations, key=lambda x: x.created_at or datetime.min.replace(tzinfo=timezone.utc), reverse=True)[:10]

    return ok({
        "totals": {
            "teammates": len(teammates),
            "innovations": total,
            "collaborations": db.query(Collaboration).count(),
            "sessions": db.query(LabSession).count(),
        },
        "averages": {
            "impact": round(avg_impact, 2),
            "feasibility": round(avg_feasibility, 2),
            "novelty": round(avg_novelty, 2),
        },
        "domain_breakdown": domain_breakdown,
        "status_breakdown": status_breakdown,
        "horizon_breakdown": horizon_breakdown,
        "recent_innovations": [i.to_dict() for i in recent],
    })


# ---------------------------------------------------------------------------
# Generate
# ---------------------------------------------------------------------------

@router.post("/generate/{slug}")
def generate(slug: str, db: Session = Depends(get_db)):
    result = generate_innovation(db, slug)
    if result is None:
        err("Teammate not found or no templates available", 404)
    return ok(result)
