import json
from fastapi import FastAPI, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import init_db, get_db, SessionLocal
from app.models import Provision
from app.seed import seed_provisions
from app.circumstances import PersonProfile, MatchResult, CrossReference
from app.matching import match_provisions
from app.cross_reference import build_cross_references, find_gaps
from app.explain import router as explain_router

app = FastAPI(title="DOMES Legal Provisions API", description="Legal rights research and provision matching", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(explain_router)


@app.get("/api/health")
async def health():
    return {"status": "ok", "app": "domes-legal-research", "port": 8000}


@app.on_event("startup")
def on_startup():
    init_db()
    db = SessionLocal()
    try:
        count = seed_provisions(db)
        if count:
            print(f"Seeded {count} legal provisions.")
    finally:
        db.close()


# -- Output schemas for provisions list / domains --------------------------

class ProvisionOut(BaseModel):
    id: int
    citation: str
    title: str
    full_text: str
    domain: str
    provision_type: str
    applies_when: dict
    enforcement_mechanisms: list[str]
    source_url: str
    cross_references: list[str]

    class Config:
        from_attributes = True


class DomainCount(BaseModel):
    domain: str
    count: int


class MatchResponse(BaseModel):
    matches: list[MatchResult]
    gaps: list[MatchResult]
    cross_references: dict[int, list[CrossReference]]


# -- Helpers ---------------------------------------------------------------

def _provision_to_dict(p: Provision) -> dict:
    """Convert a SQLAlchemy Provision row to a plain dict with parsed JSON."""
    return {
        "id": p.id,
        "citation": p.citation,
        "title": p.title,
        "full_text": p.full_text,
        "domain": p.domain,
        "provision_type": p.provision_type,
        "applies_when": json.loads(p.applies_when),
        "enforcement_mechanisms": json.loads(p.enforcement_mechanisms),
        "source_url": p.source_url,
        "cross_references": json.loads(p.cross_references),
    }


def _to_provision_out(p: Provision) -> ProvisionOut:
    return ProvisionOut(**_provision_to_dict(p))


# -- Endpoints -------------------------------------------------------------

@app.post("/api/match", response_model=MatchResponse)
def match_endpoint(profile: PersonProfile, db: Session = Depends(get_db)):
    """Match a person profile against all provisions and return ranked results,
    identified coverage gaps, and cross-references between matched provisions."""
    rows = db.query(Provision).all()
    provision_dicts = [_provision_to_dict(p) for p in rows]

    matches = match_provisions(profile, provision_dicts)

    gaps = find_gaps(profile, matches, provision_dicts)

    matched_ids = {m.provision_id for m in matches}
    gap_ids = {g.provision_id for g in gaps}
    relevant_ids = matched_ids | gap_ids
    relevant_dicts = [p for p in provision_dicts if p["id"] in relevant_ids]
    xrefs = build_cross_references(relevant_dicts)

    return MatchResponse(
        matches=matches,
        gaps=gaps,
        cross_references=xrefs,
    )


@app.get("/api/provisions", response_model=list[ProvisionOut])
def list_provisions(
    domain: str | None = Query(None),
    provision_type: str | None = Query(None),
    search: str | None = Query(None),
    db: Session = Depends(get_db),
):
    """List and filter provisions by domain, type, or search text."""
    q = db.query(Provision)
    if domain:
        q = q.filter(Provision.domain == domain)
    if provision_type:
        q = q.filter(Provision.provision_type == provision_type)
    if search:
        pattern = f"%{search}%"
        q = q.filter(
            Provision.title.ilike(pattern)
            | Provision.full_text.ilike(pattern)
            | Provision.citation.ilike(pattern)
        )
    return [_to_provision_out(p) for p in q.all()]


@app.get("/api/domains", response_model=list[DomainCount])
def list_domains(db: Session = Depends(get_db)):
    """Return all domains with their provision counts."""
    rows = (
        db.query(Provision.domain, func.count(Provision.id))
        .group_by(Provision.domain)
        .all()
    )
    return [DomainCount(domain=domain, count=count) for domain, count in rows]
