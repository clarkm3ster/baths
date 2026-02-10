"""System and connection routes."""

import json
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import System, Connection

router = APIRouter(prefix="/api", tags=["systems"])


def _system_dict(s: System) -> dict:
    return {
        "id": s.id,
        "name": s.name,
        "acronym": s.acronym,
        "agency": s.agency,
        "domain": s.domain,
        "description": s.description,
        "data_standard": s.data_standard,
        "data_held": json.loads(s.data_held),
        "who_can_access": json.loads(s.who_can_access),
        "privacy_law": s.privacy_law,
        "privacy_laws": json.loads(s.privacy_laws),
        "applies_when": json.loads(s.applies_when),
        "is_federal": s.is_federal,
        "state_operated": s.state_operated,
    }


def _connection_dict(c: Connection) -> dict:
    return {
        "id": c.id,
        "source_id": c.source_id,
        "target_id": c.target_id,
        "direction": c.direction,
        "frequency": c.frequency,
        "format": c.format,
        "data_shared": json.loads(c.data_shared),
        "description": c.description,
        "reliability": c.reliability,
    }


@router.get("/systems")
def list_systems(domain: str | None = Query(None), db: Session = Depends(get_db)):
    q = db.query(System)
    if domain:
        q = q.filter(System.domain == domain)
    return [_system_dict(s) for s in q.all()]


@router.get("/systems/{system_id}")
def get_system(system_id: str, db: Session = Depends(get_db)):
    s = db.query(System).filter(System.id == system_id).first()
    if not s:
        return {"error": "Not found"}
    # Include connections
    conns = db.query(Connection).filter(
        (Connection.source_id == system_id) | (Connection.target_id == system_id)
    ).all()
    return {
        **_system_dict(s),
        "connections": [_connection_dict(c) for c in conns],
    }


@router.get("/connections")
def list_connections(db: Session = Depends(get_db)):
    return [_connection_dict(c) for c in db.query(Connection).all()]


@router.post("/systems/for-profile")
def systems_for_profile(profile: dict, db: Session = Depends(get_db)):
    """Given a person profile (same format as DOMES), return which systems have data about them."""
    all_systems = db.query(System).all()
    matched = []

    for s in all_systems:
        applies = json.loads(s.applies_when)
        if _profile_matches(profile, applies):
            matched.append(_system_dict(s))

    return matched


def _profile_matches(profile: dict, applies_when: list[str]) -> bool:
    """Check if any profile circumstance matches the system's applies_when list."""
    if not applies_when:
        return True

    profile_values: set[str] = set()
    for key in ("insurance", "disabilities", "housing", "income", "system_involvement"):
        profile_values.update(profile.get(key, []))
    if profile.get("age_group"):
        profile_values.add(profile["age_group"])
    for boolean_field in ("pregnant", "veteran", "dv_survivor", "immigrant", "lgbtq", "rural"):
        if profile.get(boolean_field):
            profile_values.add(boolean_field)

    return bool(profile_values & set(applies_when))
