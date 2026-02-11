"""Consent form routes.

Browse, generate, and manage person-level consent forms that authorise
the disclosure of protected information across system boundaries.
"""

import json
import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import ConsentForm

router = APIRouter(prefix="/api", tags=["consent"])


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

def _consent_dict(form: ConsentForm) -> dict:
    """Serialize a ConsentForm row to a plain dict."""
    return {
        "id": form.id,
        "gap_id": form.gap_id,
        "consent_type": form.consent_type,
        "title": form.title,
        "governing_law": form.governing_law,
        "description": form.description,
        "body_text": form.body_text,
        "required_fields": json.loads(form.required_fields),
        "status": form.status,
        "created_at": form.created_at,
    }


# ---------------------------------------------------------------------------
# request schemas
# ---------------------------------------------------------------------------

class ConsentGenerateRequest(BaseModel):
    gap_id: int | None = None
    consent_type: str  # HIPAA_authorization, CFR42_consent, FERPA_release, general_release
    title: str
    disclosing_party: str
    receiving_party: str
    purpose: str
    data_description: str
    governing_law: str = ""


# ---------------------------------------------------------------------------
# template builders
# ---------------------------------------------------------------------------

_TEMPLATES: dict[str, callable] = {}


def _build_hipaa_authorization(req: ConsentGenerateRequest) -> tuple[str, str, list[str]]:
    description = (
        f"HIPAA authorization for {req.disclosing_party} to disclose "
        f"protected health information to {req.receiving_party}."
    )
    body = f"""AUTHORIZATION FOR DISCLOSURE OF PROTECTED HEALTH INFORMATION

I, _________________________, authorize the following disclosure of my protected health information:

1. ENTITY AUTHORIZED TO DISCLOSE:
{req.disclosing_party}

2. ENTITY AUTHORIZED TO RECEIVE:
{req.receiving_party}

3. INFORMATION TO BE DISCLOSED:
{req.data_description}

4. PURPOSE OF DISCLOSURE:
{req.purpose}

5. EXPIRATION:
This authorization expires on _____________ or upon the following event: ________________

6. YOUR RIGHTS:
- You have the right to revoke this authorization at any time by submitting a written request to the disclosing entity. Revocation will not apply to information already disclosed in reliance on this authorization.
- You are not required to sign this authorization. Your treatment, payment, enrollment, or eligibility for benefits will NOT be conditioned on signing this authorization.
- Information disclosed pursuant to this authorization may be subject to re-disclosure by the recipient and may no longer be protected by federal privacy law.

SIGNATURE:

Patient/Authorized Representative: ________________________________
Printed Name: _________________________
Date: ________________"""
    required_fields = [
        "patient_name", "dob", "expiration_date", "signature", "date",
    ]
    return description, body, required_fields


def _build_cfr42_consent(req: ConsentGenerateRequest) -> tuple[str, str, list[str]]:
    description = (
        f"42 CFR Part 2 consent for {req.disclosing_party} to disclose "
        f"substance use disorder treatment records to {req.receiving_party}."
    )
    body = f"""CONSENT FOR DISCLOSURE OF SUBSTANCE USE DISORDER TREATMENT RECORDS
(42 CFR Part 2)

I, _________________________, authorize:

1. FROM (name or general designation of program):
{req.disclosing_party}

2. TO (name of individual or organization):
{req.receiving_party}

3. INFORMATION TO BE DISCLOSED:
{req.data_description}

4. PURPOSE OF DISCLOSURE:
{req.purpose}

5. EXPIRATION:
This consent expires on _____________ unless revoked earlier.

6. RIGHT TO REVOKE:
I understand that I may revoke this consent at any time, except to the extent that action has been taken in reliance on it. To revoke, I must provide written notice to the program listed above.

7. I understand that my records are protected under the federal regulations governing Confidentiality of Substance Use Disorder Patient Records, 42 CFR Part 2, and cannot be disclosed without my written consent unless otherwise provided for in the regulations.

8. I understand that I may refuse to sign this consent and that my treatment, payment, enrollment, or eligibility for benefits may not be conditioned upon whether I sign this consent.

9. RE-DISCLOSURE NOTICE:
"This information has been disclosed to you from records protected by federal confidentiality rules (42 CFR Part 2). The federal rules prohibit you from making any further disclosure of information in this record that identifies a patient as having or having had a substance use disorder either directly, by reference to publicly available information, or through verification of such identification by another person unless further disclosure is expressly permitted by the written consent of the individual whose information is being disclosed or as otherwise permitted by 42 CFR Part 2. A general authorization for the release of medical or other information is NOT sufficient for this purpose (see \u00a7 2.31)."

SIGNATURE:

Patient: ________________________________
Printed Name: _________________________
Date: ________________"""
    required_fields = [
        "patient_name", "dob", "program_name", "expiration_date", "signature", "date",
    ]
    return description, body, required_fields


def _build_ferpa_release(req: ConsentGenerateRequest) -> tuple[str, str, list[str]]:
    description = (
        f"FERPA consent for {req.disclosing_party} to disclose "
        f"education records to {req.receiving_party}."
    )
    body = f"""CONSENT FOR DISCLOSURE OF EDUCATION RECORDS
(Family Educational Rights and Privacy Act \u2014 FERPA)

Student Name: _________________________
Date of Birth: _________________________
School/District: {req.disclosing_party}

I, the undersigned parent/guardian/eligible student, hereby consent to the disclosure of the following education records:

1. RECORDS TO BE DISCLOSED:
{req.data_description}

2. DISCLOSED TO:
{req.receiving_party}

3. PURPOSE OF DISCLOSURE:
{req.purpose}

4. EXPIRATION:
This consent expires on _____________ or upon the following event: ________________

5. YOUR RIGHTS UNDER FERPA:
- You have the right to inspect and review education records.
- You have the right to request amendment of records you believe are inaccurate.
- You have the right to consent to disclosure of personally identifiable information from education records, except to the extent FERPA authorizes disclosure without consent.
- You have the right to file a complaint with the U.S. Department of Education concerning alleged failures to comply with FERPA.
- This consent is voluntary. You are not required to sign this form.
- You may revoke this consent at any time by providing written notice to the school.

SIGNATURE:

Parent/Guardian/Eligible Student: ________________________________
Printed Name: ________________
Relationship to Student (if parent/guardian): ________________
Date: ________________"""
    required_fields = [
        "student_name", "student_dob", "school_name", "parent_name",
        "expiration_date", "signature", "date",
    ]
    return description, body, required_fields


def _build_general_release(req: ConsentGenerateRequest) -> tuple[str, str, list[str]]:
    description = (
        f"General information release authorizing {req.disclosing_party} and "
        f"{req.receiving_party} to share information for care coordination."
    )
    body = f"""AUTHORIZATION FOR INFORMATION SHARING

I, _________________________, authorize the following organizations to share information about me for the purpose described below:

ORGANIZATION 1: {req.disclosing_party}
ORGANIZATION 2: {req.receiving_party}

INFORMATION THAT MAY BE SHARED:
{req.data_description}

PURPOSE:
{req.purpose}

NOTE: Substance use disorder treatment records are protected by 42 CFR Part 2 and require a separate, specific consent form. This authorization does NOT cover SUD treatment records.

This authorization expires on _____________ or upon written revocation.

I understand I may revoke this authorization at any time in writing. My services will not be conditioned upon signing.

SIGNATURE:

Signature: ________________________________
Printed Name: _________________________
Date: ________________"""
    required_fields = [
        "patient_name", "dob", "expiration_date", "signature", "date",
    ]
    return description, body, required_fields


_BUILDERS = {
    "HIPAA_authorization": _build_hipaa_authorization,
    "CFR42_consent": _build_cfr42_consent,
    "FERPA_release": _build_ferpa_release,
    "general_release": _build_general_release,
}


# ---------------------------------------------------------------------------
# GET /api/consent/forms
# ---------------------------------------------------------------------------

@router.get("/consent/forms")
def list_forms(
    gap_id: int | None = None,
    consent_type: str | None = None,
    status: str | None = None,
    db: Session = Depends(get_db),
):
    """List all consent forms, with optional filters."""
    query = db.query(ConsentForm)

    if gap_id is not None:
        query = query.filter(ConsentForm.gap_id == gap_id)
    if consent_type:
        query = query.filter(ConsentForm.consent_type == consent_type)
    if status:
        query = query.filter(ConsentForm.status == status)

    forms = query.all()
    return {
        "count": len(forms),
        "forms": [_consent_dict(f) for f in forms],
    }


# ---------------------------------------------------------------------------
# GET /api/consent/forms/{form_id}
# ---------------------------------------------------------------------------

@router.get("/consent/forms/{form_id}")
def get_form(form_id: str, db: Session = Depends(get_db)):
    """Get a single consent form with full detail."""
    form = db.query(ConsentForm).filter(ConsentForm.id == form_id).first()
    if not form:
        raise HTTPException(status_code=404, detail=f"Consent form '{form_id}' not found")
    return _consent_dict(form)


# ---------------------------------------------------------------------------
# POST /api/consent/generate
# ---------------------------------------------------------------------------

@router.post("/consent/generate")
def generate_form(req: ConsentGenerateRequest, db: Session = Depends(get_db)):
    """Generate a new consent form from a template pattern based on consent_type."""
    builder = _BUILDERS.get(req.consent_type)
    if not builder:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Unknown consent_type '{req.consent_type}'. "
                f"Supported: {', '.join(_BUILDERS.keys())}"
            ),
        )

    description, body_text, required_fields = builder(req)

    form = ConsentForm(
        id=f"consent_{uuid.uuid4().hex[:12]}",
        gap_id=req.gap_id,
        consent_type=req.consent_type,
        title=req.title,
        governing_law=req.governing_law,
        description=description,
        body_text=body_text,
        required_fields=json.dumps(required_fields),
        status="draft",
        created_at=datetime.now(timezone.utc).strftime("%Y-%m-%d"),
    )

    db.add(form)
    db.commit()

    return _consent_dict(form)


# ---------------------------------------------------------------------------
# GET /api/consent/for-gap/{gap_id}
# ---------------------------------------------------------------------------

@router.get("/consent/for-gap/{gap_id}")
def forms_for_gap(gap_id: int, db: Session = Depends(get_db)):
    """Get all consent forms associated with a specific gap."""
    forms = db.query(ConsentForm).filter(ConsentForm.gap_id == gap_id).all()
    return {
        "gap_id": gap_id,
        "count": len(forms),
        "forms": [_consent_dict(f) for f in forms],
    }


# ---------------------------------------------------------------------------
# GET /api/consent/stats
# ---------------------------------------------------------------------------

@router.get("/consent/stats")
def consent_stats(db: Session = Depends(get_db)):
    """Summary statistics: total forms by consent_type and status."""
    forms = db.query(ConsentForm).all()

    by_type: dict[str, int] = {}
    by_status: dict[str, int] = {}

    for f in forms:
        by_type[f.consent_type] = by_type.get(f.consent_type, 0) + 1
        by_status[f.status] = by_status.get(f.status, 0) + 1

    return {
        "total": len(forms),
        "by_type": by_type,
        "by_status": by_status,
    }
