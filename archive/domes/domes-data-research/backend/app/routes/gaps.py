"""Gap and consent pathway routes."""

import json
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Gap, System

router = APIRouter(prefix="/api", tags=["gaps"])


def _gap_dict(g: Gap) -> dict:
    return {
        "id": g.id,
        "system_a_id": g.system_a_id,
        "system_b_id": g.system_b_id,
        "barrier_type": g.barrier_type,
        "barrier_law": g.barrier_law,
        "barrier_description": g.barrier_description,
        "impact": g.impact,
        "what_it_would_take": g.what_it_would_take,
        "consent_closable": g.consent_closable,
        "consent_mechanism": g.consent_mechanism,
        "severity": g.severity,
        "applies_when": json.loads(g.applies_when),
    }


@router.get("/gaps")
def list_gaps(db: Session = Depends(get_db)):
    return [_gap_dict(g) for g in db.query(Gap).all()]


@router.get("/gaps/{gap_id}")
def get_gap(gap_id: int, db: Session = Depends(get_db)):
    g = db.query(Gap).filter(Gap.id == gap_id).first()
    if not g:
        return {"error": "Not found"}

    # Include system details
    sys_a = db.query(System).filter(System.id == g.system_a_id).first()
    sys_b = db.query(System).filter(System.id == g.system_b_id).first()

    result = _gap_dict(g)
    result["system_a"] = {"id": sys_a.id, "name": sys_a.name, "acronym": sys_a.acronym, "domain": sys_a.domain} if sys_a else None
    result["system_b"] = {"id": sys_b.id, "name": sys_b.name, "acronym": sys_b.acronym, "domain": sys_b.domain} if sys_b else None
    return result


@router.get("/gaps/{gap_id}/barriers")
def get_gap_barriers(gap_id: int, db: Session = Depends(get_db)):
    g = db.query(Gap).filter(Gap.id == gap_id).first()
    if not g:
        return {"error": "Not found"}
    return {
        "gap_id": g.id,
        "barrier_type": g.barrier_type,
        "barrier_law": g.barrier_law,
        "barrier_description": g.barrier_description,
    }


@router.get("/gaps/{gap_id}/solutions")
def get_gap_solutions(gap_id: int, db: Session = Depends(get_db)):
    g = db.query(Gap).filter(Gap.id == gap_id).first()
    if not g:
        return {"error": "Not found"}
    return {
        "gap_id": g.id,
        "what_it_would_take": g.what_it_would_take,
        "consent_closable": g.consent_closable,
        "consent_mechanism": g.consent_mechanism if g.consent_closable else None,
    }


@router.get("/consent-pathways")
def consent_pathways(db: Session = Depends(get_db)):
    """Return all gaps that a person could close by signing a consent form."""
    closable = db.query(Gap).filter(Gap.consent_closable == True).all()  # noqa: E712
    return [
        {
            **_gap_dict(g),
            "action_label": "You can close this gap",
        }
        for g in closable
    ]


@router.post("/gaps/for-profile")
def gaps_for_profile(profile: dict, db: Session = Depends(get_db)):
    """Return gaps relevant to a person's circumstances."""
    all_gaps = db.query(Gap).all()
    matched = []

    profile_values: set[str] = set()
    for key in ("insurance", "disabilities", "housing", "income", "system_involvement"):
        profile_values.update(profile.get(key, []))
    if profile.get("age_group"):
        profile_values.add(profile["age_group"])
    for bf in ("pregnant", "veteran", "dv_survivor", "immigrant", "lgbtq", "rural"):
        if profile.get(bf):
            profile_values.add(bf)

    for g in all_gaps:
        applies = json.loads(g.applies_when)
        if not applies or profile_values & set(applies):
            matched.append(_gap_dict(g))

    return matched
