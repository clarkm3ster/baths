"""Agreement API routes.

Endpoints for generating, listing, retrieving, and managing
data-sharing agreements and their underlying templates.
"""

import json
import urllib.request
import urllib.error
import uuid
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.models import Agreement, Template
from app.agreement_generator import determine_agreement_types, generate_agreement_from_gap

router = APIRouter(prefix="/api", tags=["agreements"])


# ---------------------------------------------------------------------------
# Request / response schemas
# ---------------------------------------------------------------------------

class GenerateRequest(BaseModel):
    template_id: str
    party_a_name: str
    party_b_name: str
    state: str = "Pennsylvania"
    gap_id: int | None = None
    system_a_id: str = ""
    system_b_id: str = ""
    barrier_description: str = ""
    barrier_law: str = ""
    barrier_type: str = ""
    impact: str = ""
    what_it_would_take: str = ""
    consent_closable: bool = False


class StatusUpdate(BaseModel):
    status: str = Field(..., pattern="^(draft|in_review|executed)$")


# ---------------------------------------------------------------------------
# Serialization helpers
# ---------------------------------------------------------------------------

def _parse_json_col(value: str) -> list | dict:
    """Safely parse a JSON text column, returning [] on failure."""
    if not value:
        return []
    try:
        return json.loads(value)
    except (json.JSONDecodeError, TypeError):
        return []


def _agreement_dict(a: Agreement) -> dict:
    return {
        "id": a.id,
        "template_id": a.template_id,
        "agreement_type": a.agreement_type,
        "title": a.title,
        "status": a.status,
        "gap_id": a.gap_id,
        "system_a_id": a.system_a_id,
        "system_b_id": a.system_b_id,
        "party_a_name": a.party_a_name,
        "party_b_name": a.party_b_name,
        "governing_laws": _parse_json_col(a.governing_laws),
        "required_signatories": _parse_json_col(a.required_signatories),
        "data_elements": _parse_json_col(a.data_elements),
        "privacy_provisions": _parse_json_col(a.privacy_provisions),
        "key_terms": _parse_json_col(a.key_terms),
        "body_text": a.body_text,
        "compliance_status": a.compliance_status,
        "compliance_flags": _parse_json_col(a.compliance_flags),
        "created_at": a.created_at,
        "updated_at": a.updated_at,
    }


def _template_dict(t: Template) -> dict:
    return {
        "id": t.id,
        "agreement_type": t.agreement_type,
        "name": t.name,
        "description": t.description,
        "governing_laws": _parse_json_col(t.governing_laws),
        "required_provisions": _parse_json_col(t.required_provisions),
        "variable_fields": _parse_json_col(t.variable_fields),
        "body_template": t.body_template,
    }


# ---------------------------------------------------------------------------
# Helper: fetch gap from domes-datamap
# ---------------------------------------------------------------------------

DATAMAP_BASE = "http://localhost:8003"


def _fetch_gap(gap_id: int) -> dict:
    """Fetch a gap from the domes-datamap API. Raises HTTPException on failure."""
    url = f"{DATAMAP_BASE}/api/gaps/{gap_id}"
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            raise HTTPException(status_code=404, detail=f"Gap {gap_id} not found in domes-datamap")
        raise HTTPException(
            status_code=502,
            detail=f"domes-datamap returned HTTP {exc.code} for gap {gap_id}",
        )
    except (urllib.error.URLError, OSError) as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Could not reach domes-datamap at {DATAMAP_BASE}: {exc}",
        )


# ---------------------------------------------------------------------------
# Status transition validation
# ---------------------------------------------------------------------------

_VALID_TRANSITIONS: dict[str, list[str]] = {
    "draft": ["in_review"],
    "in_review": ["executed", "draft"],
    "executed": [],
}


# ---------------------------------------------------------------------------
# 1. POST /api/agreements/generate
# ---------------------------------------------------------------------------

@router.post("/agreements/generate")
def generate_agreement(body: GenerateRequest, db: Session = Depends(get_db)):
    """Generate an agreement from a template.

    Accepts party names, an optional gap payload embedded in the body,
    and a template_id.  Returns the rendered agreement.
    """
    template = db.query(Template).filter(Template.id == body.template_id).first()
    if not template:
        raise HTTPException(status_code=404, detail=f"Template '{body.template_id}' not found")

    # Build a gap-like dict from the request body so the generator can work
    gap: dict = {
        "id": body.gap_id,
        "system_a_id": body.system_a_id,
        "system_b_id": body.system_b_id,
        "system_a": {"name": body.party_a_name},
        "system_b": {"name": body.party_b_name},
        "barrier_description": body.barrier_description,
        "barrier_law": body.barrier_law,
        "barrier_type": body.barrier_type,
        "impact": body.impact,
        "what_it_would_take": body.what_it_would_take,
        "consent_closable": body.consent_closable,
    }

    agreement = generate_agreement_from_gap(gap, template, db, state=body.state)
    db.commit()

    return _agreement_dict(agreement)


# ---------------------------------------------------------------------------
# 2. POST /api/agreements/from-gap/{gap_id}
# ---------------------------------------------------------------------------

@router.post("/agreements/from-gap/{gap_id}")
def generate_from_gap(gap_id: int, db: Session = Depends(get_db)):
    """Fetch a gap from domes-datamap, determine which agreement types are
    needed, generate ALL of them, and return the list.
    """
    gap = _fetch_gap(gap_id)

    agreement_types = determine_agreement_types(gap)
    generated: list[dict] = []

    for atype in agreement_types:
        template = db.query(Template).filter(Template.agreement_type == atype).first()
        if not template:
            # Skip types with no template rather than failing the whole batch
            continue
        agreement = generate_agreement_from_gap(gap, template, db)
        generated.append(_agreement_dict(agreement))

    db.commit()

    if not generated:
        raise HTTPException(
            status_code=422,
            detail=f"No templates matched the determined agreement types {agreement_types} for gap {gap_id}",
        )

    return {
        "gap_id": gap_id,
        "agreement_types_needed": agreement_types,
        "agreements_generated": len(generated),
        "agreements": generated,
    }


# ---------------------------------------------------------------------------
# 3. GET /api/agreements  (list)
# ---------------------------------------------------------------------------

@router.get("/agreements")
def list_agreements(
    status: str | None = Query(None, description="Filter by status: draft, in_review, executed"),
    agreement_type: str | None = Query(None, description="Filter by agreement type"),
    gap_id: int | None = Query(None, description="Filter by gap_id"),
    db: Session = Depends(get_db),
):
    """List all agreements with optional filters."""
    q = db.query(Agreement)
    if status:
        q = q.filter(Agreement.status == status)
    if agreement_type:
        q = q.filter(Agreement.agreement_type == agreement_type)
    if gap_id is not None:
        q = q.filter(Agreement.gap_id == gap_id)

    agreements = q.order_by(Agreement.created_at.desc()).all()
    return {
        "count": len(agreements),
        "agreements": [_agreement_dict(a) for a in agreements],
    }


# ---------------------------------------------------------------------------
# 9. GET /api/agreements/stats  (before the /{agreement_id} catch-all)
# ---------------------------------------------------------------------------

@router.get("/agreements/stats")
def agreement_stats(db: Session = Depends(get_db)):
    """Return summary statistics: total agreements, counts by status and type."""
    total = db.query(func.count(Agreement.id)).scalar() or 0

    by_status_rows = (
        db.query(Agreement.status, func.count(Agreement.id))
        .group_by(Agreement.status)
        .all()
    )
    by_status = {row[0]: row[1] for row in by_status_rows}

    by_type_rows = (
        db.query(Agreement.agreement_type, func.count(Agreement.id))
        .group_by(Agreement.agreement_type)
        .all()
    )
    by_type = {row[0]: row[1] for row in by_type_rows}

    return {
        "total": total,
        "by_status": by_status,
        "by_type": by_type,
    }


# ---------------------------------------------------------------------------
# 10. GET /api/agreements/gap-coverage
# ---------------------------------------------------------------------------

@router.get("/agreements/gap-coverage")
def gap_coverage(db: Session = Depends(get_db)):
    """Return coverage status per gap: 'none', 'draft', 'in_review', 'executed'.

    The highest status wins: executed > in_review > draft > none.
    """
    all_agreements = db.query(Agreement).filter(Agreement.gap_id.isnot(None)).all()
    coverage: dict[int, str] = {}
    priority = {"draft": 1, "in_review": 2, "executed": 3}

    for a in all_agreements:
        gap_id = a.gap_id
        current = coverage.get(gap_id, "none")
        current_pri = priority.get(current, 0)
        new_pri = priority.get(a.status, 0)
        if new_pri > current_pri:
            coverage[gap_id] = a.status

    return coverage


# ---------------------------------------------------------------------------
# 11. POST /api/agreements/batch-generate
# ---------------------------------------------------------------------------

@router.post("/agreements/batch-generate")
def batch_generate(body: dict, db: Session = Depends(get_db)):
    """Generate all agreements for gaps matching a set of circumstances.

    Request body: { "circumstances": ["medicaid", "incarcerated", ...] }
    Fetches all gaps from domes-datamap, filters by circumstance overlap,
    generates agreements for each applicable gap that doesn't already have any.
    """
    circumstances = set(body.get("circumstances", []))
    if not circumstances:
        raise HTTPException(status_code=422, detail="No circumstances provided")

    # Fetch all gaps from domes-datamap
    try:
        url = f"{DATAMAP_BASE}/api/gaps"
        req = urllib.request.Request(url, headers={"Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            all_gaps = json.loads(resp.read().decode("utf-8"))
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Could not fetch gaps: {exc}")

    # Filter gaps by circumstance overlap
    matched_gaps = []
    for gap in all_gaps:
        applies = set(gap.get("applies_when", []))
        if not applies or applies & circumstances:
            matched_gaps.append(gap)

    generated_all: list[dict] = []
    skipped = 0

    for gap in matched_gaps:
        gap_id = gap["id"]
        # Check if agreements already exist for this gap
        existing = db.query(Agreement).filter(Agreement.gap_id == gap_id).count()
        if existing > 0:
            skipped += 1
            continue

        # Fetch full gap detail
        try:
            full_gap = _fetch_gap(gap_id)
        except Exception:
            continue

        agreement_types = determine_agreement_types(full_gap)
        for atype in agreement_types:
            template = db.query(Template).filter(Template.agreement_type == atype).first()
            if not template:
                continue
            agreement = generate_agreement_from_gap(full_gap, template, db)
            generated_all.append(_agreement_dict(agreement))

    db.commit()

    return {
        "gaps_matched": len(matched_gaps),
        "gaps_skipped_existing": skipped,
        "agreements_generated": len(generated_all),
        "agreements": generated_all,
    }


# ---------------------------------------------------------------------------
# 6. GET /api/agreements/templates
# ---------------------------------------------------------------------------

@router.get("/agreements/templates")
def list_templates(db: Session = Depends(get_db)):
    """List all available agreement templates."""
    templates = db.query(Template).order_by(Template.agreement_type).all()
    return {
        "count": len(templates),
        "templates": [_template_dict(t) for t in templates],
    }


# ---------------------------------------------------------------------------
# 7. GET /api/agreements/templates/{template_id}
# ---------------------------------------------------------------------------

@router.get("/agreements/templates/{template_id}")
def get_template(template_id: str, db: Session = Depends(get_db)):
    """Get a single template with full detail."""
    template = db.query(Template).filter(Template.id == template_id).first()
    if not template:
        raise HTTPException(status_code=404, detail=f"Template '{template_id}' not found")
    return _template_dict(template)


# ---------------------------------------------------------------------------
# 8. GET /api/agreements/for-gap/{gap_id}
# ---------------------------------------------------------------------------

@router.get("/agreements/for-gap/{gap_id}")
def agreements_for_gap(gap_id: int, db: Session = Depends(get_db)):
    """Get all existing agreements linked to a specific gap."""
    agreements = (
        db.query(Agreement)
        .filter(Agreement.gap_id == gap_id)
        .order_by(Agreement.created_at.desc())
        .all()
    )
    return {
        "gap_id": gap_id,
        "count": len(agreements),
        "agreements": [_agreement_dict(a) for a in agreements],
    }


# ---------------------------------------------------------------------------
# 4. GET /api/agreements/{agreement_id}
# ---------------------------------------------------------------------------

@router.get("/agreements/{agreement_id}")
def get_agreement(agreement_id: str, db: Session = Depends(get_db)):
    """Get a single agreement with full detail."""
    agreement = db.query(Agreement).filter(Agreement.id == agreement_id).first()
    if not agreement:
        raise HTTPException(status_code=404, detail=f"Agreement '{agreement_id}' not found")
    return _agreement_dict(agreement)


# ---------------------------------------------------------------------------
# 5. PATCH /api/agreements/{agreement_id}/status
# ---------------------------------------------------------------------------

@router.patch("/agreements/{agreement_id}/status")
def update_agreement_status(
    agreement_id: str,
    body: StatusUpdate,
    db: Session = Depends(get_db),
):
    """Update agreement status with transition validation.

    Valid transitions:
        draft -> in_review
        in_review -> executed | draft
        executed -> (none -- terminal)
    """
    agreement = db.query(Agreement).filter(Agreement.id == agreement_id).first()
    if not agreement:
        raise HTTPException(status_code=404, detail=f"Agreement '{agreement_id}' not found")

    current = agreement.status
    new_status = body.status

    if current == new_status:
        return _agreement_dict(agreement)

    allowed = _VALID_TRANSITIONS.get(current, [])
    if new_status not in allowed:
        raise HTTPException(
            status_code=422,
            detail=f"Invalid status transition: '{current}' -> '{new_status}'. Allowed transitions from '{current}': {allowed}",
        )

    agreement.status = new_status
    agreement.updated_at = datetime.utcnow().strftime("%Y-%m-%d")
    db.commit()

    return _agreement_dict(agreement)


# ---------------------------------------------------------------------------
# 12. GET /api/agreements/{agreement_id}/export
# ---------------------------------------------------------------------------

@router.get("/agreements/{agreement_id}/export")
def export_agreement(agreement_id: str, db: Session = Depends(get_db)):
    """Export an agreement as plain text, suitable for download."""
    agreement = db.query(Agreement).filter(Agreement.id == agreement_id).first()
    if not agreement:
        raise HTTPException(status_code=404, detail=f"Agreement '{agreement_id}' not found")

    laws = json.loads(agreement.governing_laws)
    signatories = json.loads(agreement.required_signatories)

    header = f"""{'=' * 72}
{agreement.title.upper()}
{'=' * 72}

Agreement Type: {agreement.agreement_type}
Status: {agreement.status.upper()}
Parties: {agreement.party_a_name} — {agreement.party_b_name}
Governing Laws: {', '.join(laws)}
Required Signatories: {', '.join(signatories)}
Date Generated: {agreement.created_at}

{'=' * 72}

"""
    content = header + agreement.body_text

    safe_title = agreement.title.replace(" ", "_").replace("/", "-")[:60]
    filename = f"{safe_title}_{agreement.id}.txt"

    return PlainTextResponse(
        content=content,
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
