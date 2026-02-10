"""Provisions CRUD routes."""
import json
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import get_db
from ..models import Provision, ProvisionHistory

router = APIRouter(prefix="/api/provisions", tags=["provisions"])


@router.get("")
def list_provisions(
    domain: str | None = None,
    provision_type: str | None = None,
    source_type: str | None = None,
    q: str | None = None,
    limit: int = 100,
    offset: int = 0,
    db: Session = Depends(get_db),
):
    query = db.query(Provision).filter(Provision.is_current == True)
    if domain:
        query = query.filter(Provision.domain == domain)
    if provision_type:
        query = query.filter(Provision.provision_type == provision_type)
    if source_type:
        query = query.filter(Provision.source_type == source_type)
    if q:
        pattern = f"%{q}%"
        query = query.filter(
            (Provision.title.ilike(pattern))
            | (Provision.full_text.ilike(pattern))
            | (Provision.citation.ilike(pattern))
        )
    total = query.count()
    items = query.offset(offset).limit(limit).all()
    return {"total": total, "items": [p.to_dict() for p in items]}


@router.get("/domains")
def get_domains(db: Session = Depends(get_db)):
    rows = (
        db.query(Provision.domain, func.count(Provision.id))
        .filter(Provision.is_current == True)
        .group_by(Provision.domain)
        .all()
    )
    return [{"domain": d, "count": c} for d, c in rows]


@router.get("/hierarchy")
def get_hierarchy(db: Session = Depends(get_db)):
    provisions = db.query(Provision).filter(Provision.is_current == True).all()
    tree = {}
    for p in provisions:
        src = p.source_type or "other"
        title = p.title_number or "general"
        part = p.part or "general"
        tree.setdefault(src, {}).setdefault(title, {}).setdefault(part, []).append({
            "id": p.id,
            "citation": p.citation,
            "title": p.title,
            "domain": p.domain,
            "provision_type": p.provision_type,
        })
    return tree


@router.get("/{provision_id}")
def get_provision(provision_id: int, db: Session = Depends(get_db)):
    p = db.query(Provision).filter(Provision.id == provision_id).first()
    if not p:
        return {"error": "Not found"}
    return p.to_dict()


@router.get("/citation/{citation:path}")
def get_by_citation(citation: str, db: Session = Depends(get_db)):
    p = db.query(Provision).filter(Provision.citation == citation).first()
    if not p:
        return {"error": "Not found"}
    return p.to_dict()


@router.get("/{provision_id}/history")
def get_history(provision_id: int, db: Session = Depends(get_db)):
    items = (
        db.query(ProvisionHistory)
        .filter(ProvisionHistory.provision_id == provision_id)
        .order_by(ProvisionHistory.changed_at.desc())
        .all()
    )
    return [h.to_dict() for h in items]
