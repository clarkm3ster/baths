"""Taxonomy and search routes."""
import json
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import get_db
from ..models import Provision, TaxonomyTag

router = APIRouter(prefix="/api", tags=["taxonomy"])


@router.get("/taxonomy/tags")
def list_tags(category: str | None = None, db: Session = Depends(get_db)):
    query = db.query(TaxonomyTag)
    if category:
        query = query.filter(TaxonomyTag.category == category)
    return [t.to_dict() for t in query.all()]


@router.post("/taxonomy/tags")
def create_tag(body: dict, db: Session = Depends(get_db)):
    tag = TaxonomyTag(
        name=body["name"],
        category=body["category"],
        description=body.get("description", ""),
        parent_tag=body.get("parent_tag"),
    )
    db.add(tag)
    db.commit()
    return tag.to_dict()


@router.get("/taxonomy/tags/{tag_name}/provisions")
def get_tag_provisions(tag_name: str, db: Session = Depends(get_db)):
    provisions = db.query(Provision).filter(
        Provision.tags.like(f'%"{tag_name}"%')
    ).all()
    return [p.to_dict() for p in provisions]


@router.post("/search")
def search_provisions(body: dict, db: Session = Depends(get_db)):
    query = db.query(Provision).filter(Provision.is_current == True)
    q = body.get("query")
    if q:
        pattern = f"%{q}%"
        query = query.filter(
            (Provision.title.ilike(pattern))
            | (Provision.full_text.ilike(pattern))
            | (Provision.citation.ilike(pattern))
            | (Provision.tags.ilike(pattern))
            | (Provision.enforcement_mechanisms.ilike(pattern))
            | (Provision.cross_references.ilike(pattern))
            | (Provision.populations.ilike(pattern))
        )
    domains = body.get("domains", [])
    if domains:
        query = query.filter(Provision.domain.in_(domains))
    ptypes = body.get("provision_types", [])
    if ptypes:
        query = query.filter(Provision.provision_type.in_(ptypes))
    tags = body.get("tags", [])
    for tag in tags:
        query = query.filter(Provision.tags.like(f'%"{tag}"%'))
    populations = body.get("populations", [])
    for pop in populations:
        query = query.filter(Provision.populations.like(f'%"{pop}"%'))
    items = query.all()
    # Score by relevance
    results = []
    for p in items:
        score = p.confidence_score or 1.0
        if q and q.lower() in (p.title or "").lower():
            score += 0.5
        if q and q.lower() in (p.citation or "").lower():
            score += 0.3
        d = p.to_dict()
        d["relevance_score"] = round(score, 2)
        results.append(d)
    results.sort(key=lambda x: -x["relevance_score"])
    return {"total": len(results), "items": results}


@router.post("/match")
def match_circumstances(body: dict, db: Session = Depends(get_db)):
    """Match person circumstances to legal provisions."""
    circumstances = body.get("circumstances", {})
    provisions = db.query(Provision).filter(Provision.is_current == True).all()
    results = []
    for p in provisions:
        aw = json.loads(p.applies_when or "{}")
        score = 0.0
        match_reasons = []
        for key, values in circumstances.items():
            if not isinstance(values, list):
                values = [values]
            if key in aw:
                aw_values = aw[key] if isinstance(aw[key], list) else [aw[key]]
                for v in values:
                    if v in aw_values or "any" in aw_values:
                        score += 1.0
                        match_reasons.append(f"{key}={v}")
        if score > 0:
            type_weights = {"right": 1.0, "protection": 0.95, "obligation": 0.9, "enforcement": 0.85}
            score *= type_weights.get(p.provision_type, 0.8)
            d = p.to_dict()
            d["match_score"] = round(score, 2)
            d["match_reasons"] = match_reasons
            results.append(d)
    results.sort(key=lambda x: -x["match_score"])
    return {"total": len(results), "items": results}


@router.get("/taxonomy/stats")
def get_stats(db: Session = Depends(get_db)):
    total = db.query(Provision).filter(Provision.is_current == True).count()
    domain_counts = dict(
        db.query(Provision.domain, func.count(Provision.id))
        .filter(Provision.is_current == True)
        .group_by(Provision.domain).all()
    )
    type_counts = dict(
        db.query(Provision.provision_type, func.count(Provision.id))
        .filter(Provision.is_current == True)
        .group_by(Provision.provision_type).all()
    )
    source_counts = dict(
        db.query(Provision.source_type, func.count(Provision.id))
        .filter(Provision.is_current == True)
        .group_by(Provision.source_type).all()
    )
    tag_count = db.query(TaxonomyTag).count()
    return {
        "total_provisions": total,
        "domains": domain_counts,
        "provision_types": type_counts,
        "source_types": source_counts,
        "total_tags": tag_count,
    }
