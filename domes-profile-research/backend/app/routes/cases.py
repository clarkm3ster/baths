import json
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import DocumentedCase

router = APIRouter(prefix="/api/cases", tags=["cases"])


@router.get("")
def list_cases(
    domain: str | None = None,
    source_type: str | None = None,
    tag: str | None = None,
    db: Session = Depends(get_db),
):
    q = db.query(DocumentedCase)
    if domain:
        q = q.filter(DocumentedCase.domain == domain)
    if source_type:
        q = q.filter(DocumentedCase.source_type == source_type)
    cases = q.all()

    results = []
    for c in cases:
        if tag:
            tags = json.loads(c.circumstance_tags or "[]")
            if tag not in tags:
                continue
        results.append(c.to_dict())
    return results


@router.get("/stats")
def case_stats(db: Session = Depends(get_db)):
    cases = db.query(DocumentedCase).all()
    by_domain = {}
    by_source = {}
    by_type = {}
    for c in cases:
        by_domain[c.domain] = by_domain.get(c.domain, 0) + 1
        by_source[c.source] = by_source.get(c.source, 0) + 1
        by_type[c.source_type] = by_type.get(c.source_type, 0) + 1
    return {
        "total": len(cases),
        "by_domain": by_domain,
        "by_source": by_source,
        "by_type": by_type,
    }


@router.get("/{case_id}")
def get_case(case_id: str, db: Session = Depends(get_db)):
    case = db.query(DocumentedCase).filter(DocumentedCase.id == case_id).first()
    if not case:
        return {"error": "Case not found"}
    return case.to_dict()


@router.post("/search")
def search_cases(body: dict, db: Session = Depends(get_db)):
    tags = body.get("tags", [])
    system_ids = body.get("system_ids", [])
    cases = db.query(DocumentedCase).all()

    results = []
    tag_set = set(tags)
    sys_set = set(system_ids)

    for c in cases:
        case_tags = set(json.loads(c.circumstance_tags or "[]"))
        case_systems = set(json.loads(c.system_ids or "[]"))
        score = len(case_tags & tag_set) + len(case_systems & sys_set)
        if score > 0:
            d = c.to_dict()
            d["relevance_score"] = score
            results.append(d)

    results.sort(key=lambda x: x["relevance_score"], reverse=True)
    return results
