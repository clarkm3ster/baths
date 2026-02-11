"""Agreement generation engine.

Takes a gap from domes-datamap → determines which agreement(s) close it →
generates drafts with correct parties, data elements, and privacy provisions.
"""

import json
import uuid
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models import Agreement, Template


# Map barrier types and laws to required agreement types
GAP_TO_AGREEMENT_MAP: dict[str, list[str]] = {
    # Barrier law → agreement types needed
    "HIPAA": ["BAA", "HIPAA_consent"],
    "42 CFR Part 2": ["QSOA", "42CFR_consent"],
    "42_CFR_Part_2": ["QSOA", "42CFR_consent"],
    "FERPA": ["FERPA_consent"],
    "CJIS_Security_Policy": ["IDSA"],
    "Medicaid Inmate Exclusion Policy": ["IDSA", "HIPAA_consent"],
    "Privacy Act / 42 CFR Part 2": ["42CFR_consent", "DUA"],
}

# Barrier type → fallback agreement types
BARRIER_TYPE_MAP: dict[str, list[str]] = {
    "legal": ["IDSA", "MOU"],
    "technical": ["IDSA", "MOU", "joint_funding"],
    "political": ["MOU", "compact"],
    "funding": ["joint_funding", "MOU"],
    "consent": ["HIPAA_consent"],
}


def determine_agreement_types(gap: dict) -> list[str]:
    """Given a gap dict, return the list of agreement types needed to close it."""
    types: list[str] = []

    # Check specific barrier law first
    barrier_law = gap.get("barrier_law", "")
    if barrier_law in GAP_TO_AGREEMENT_MAP:
        types.extend(GAP_TO_AGREEMENT_MAP[barrier_law])

    # Check barrier type as fallback
    barrier_type = gap.get("barrier_type", "")
    if barrier_type in BARRIER_TYPE_MAP:
        for t in BARRIER_TYPE_MAP[barrier_type]:
            if t not in types:
                types.append(t)

    # If consent-closable, ensure consent form is included
    if gap.get("consent_closable"):
        consent_type = _infer_consent_type(gap)
        if consent_type and consent_type not in types:
            types.append(consent_type)

    # If nothing matched, default to MOU + IDSA
    if not types:
        types = ["MOU", "IDSA"]

    return types


def _infer_consent_type(gap: dict) -> str | None:
    """Infer the appropriate consent form type based on gap details."""
    barrier_law = gap.get("barrier_law", "")
    barrier_desc = gap.get("barrier_description", "").lower()

    if "42 cfr" in barrier_law.lower() or "42 cfr" in barrier_desc:
        return "42CFR_consent"
    if "ferpa" in barrier_law.lower() or "ferpa" in barrier_desc:
        return "FERPA_consent"
    return "HIPAA_consent"


def generate_agreement_from_gap(
    gap: dict,
    template: Template,
    db: Session,
    state: str = "Pennsylvania",
) -> Agreement:
    """Generate a concrete agreement from a gap and template."""
    now = datetime.utcnow().strftime("%Y-%m-%d")
    expiration = (datetime.utcnow() + timedelta(days=365)).strftime("%Y-%m-%d")

    # Extract system info from gap
    sys_a = gap.get("system_a", {}) or {}
    sys_b = gap.get("system_b", {}) or {}
    system_a_id = gap.get("system_a_id", "")
    system_b_id = gap.get("system_b_id", "")
    party_a = sys_a.get("name", system_a_id)
    party_b = sys_b.get("name", system_b_id)

    # Build variable substitutions
    variables = _build_variables(gap, template, party_a, party_b, state, now, expiration)

    # Render the template
    body = template.body_template
    for key, value in variables.items():
        body = body.replace("{{" + key + "}}", value)

    # Determine governing laws
    governing_laws = json.loads(template.governing_laws)

    # Build data elements from gap
    data_elements = _extract_data_elements(gap)

    # Build privacy provisions
    privacy_provisions = _build_privacy_provisions(gap, template.agreement_type)

    agreement = Agreement(
        id=f"agr_{uuid.uuid4().hex[:12]}",
        template_id=template.id,
        agreement_type=template.agreement_type,
        title=f"{template.name}: {party_a} — {party_b}",
        status="draft",
        gap_id=gap.get("id"),
        system_a_id=system_a_id,
        system_b_id=system_b_id,
        party_a_name=party_a,
        party_b_name=party_b,
        governing_laws=json.dumps(governing_laws),
        required_signatories=json.dumps(_get_signatories(template.agreement_type, party_a, party_b)),
        data_elements=json.dumps(data_elements),
        privacy_provisions=json.dumps(privacy_provisions),
        key_terms=json.dumps(_get_key_terms(gap, template)),
        body_text=body,
        compliance_status="unchecked",
        compliance_flags=json.dumps([]),
        created_at=now,
        updated_at=now,
    )

    db.add(agreement)
    db.flush()
    return agreement


def _build_variables(
    gap: dict, template: Template, party_a: str, party_b: str,
    state: str, effective_date: str, expiration: str,
) -> dict[str, str]:
    """Build template variable substitutions based on gap and context."""
    v: dict[str, str] = {
        "effective_date": effective_date,
        "expiration_date": expiration,
        "governing_state": state,
        "term_length": "one (1) year",
    }

    atype = template.agreement_type

    if atype == "BAA":
        v["covered_entity_name"] = party_a
        v["business_associate_name"] = party_b
        v["permitted_uses"] = f"Treatment, payment, and health care operations related to closing the data gap between {party_a} and {party_b}."
        v["data_elements"] = _format_data_elements(gap)
        v["safeguard_requirements"] = "Encryption at rest and in transit (AES-256 / TLS 1.2+), role-based access controls, annual security risk assessment, workforce training."
        v["breach_notification_timeline"] = "10"
    elif atype == "DUA":
        v["data_provider_name"] = party_a
        v["data_recipient_name"] = party_b
        v["data_description"] = _format_data_elements(gap)
        v["permitted_purposes"] = f"Service coordination and closing the identified data gap: {gap.get('impact', '')[:200]}"
        v["security_requirements"] = "Encryption, access controls, annual security assessment, secure disposal upon termination."
    elif atype == "MOU":
        v["agency_a_name"] = party_a
        v["agency_b_name"] = party_b
        v["purpose"] = gap.get("impact", "Closing identified coordination gap between agencies.")
        v["scope"] = gap.get("what_it_would_take", "")
        v["data_to_share"] = _format_data_elements(gap)
        v["responsibilities_a"] = f"Designate liaison, provide data per agreement, maintain security controls"
        v["responsibilities_b"] = f"Designate liaison, use data only for stated purpose, maintain security controls"
        v["privacy_protections"] = "Comply with all applicable federal and state privacy laws. Limit access to authorized personnel. Report breaches within 24 hours."
        v["review_period"] = "quarterly"
    elif atype == "IDSA":
        v["agency_a_name"] = party_a
        v["agency_b_name"] = party_b
        v["legal_authority"] = _get_legal_authority(gap)
        v["purpose"] = gap.get("impact", "")
        v["data_elements_a_to_b"] = _format_data_elements(gap)
        v["data_elements_b_to_a"] = "Confirmation of receipt, data quality feedback, service coordination updates"
        v["transmission_method"] = "Encrypted SFTP or FHIR API with mutual TLS authentication"
        v["security_requirements"] = "NIST 800-53 moderate baseline controls, encryption at rest and in transit, multi-factor authentication, audit logging"
        v["audit_frequency"] = "annually"
        v["breach_notification_timeline"] = "24"
    elif atype == "QSOA":
        v["program_name"] = party_a
        v["qso_name"] = party_b
        v["services_provided"] = f"Data sharing and care coordination services related to substance use disorder treatment continuity"
        v["patient_information_shared"] = _format_data_elements(gap)
    elif atype in ("HIPAA_consent", "42CFR_consent", "FERPA_consent"):
        v["patient_name"] = "[INDIVIDUAL NAME]"
        v["dob"] = "[DATE OF BIRTH]"
        v["disclosing_entity"] = party_a
        v["receiving_entity"] = party_b
        v["program_name"] = party_a
        v["student_name"] = "[STUDENT NAME]"
        v["student_dob"] = "[DATE OF BIRTH]"
        v["school_name"] = party_a
        v["receiving_party"] = party_b
        v["information_description"] = _format_data_elements(gap)
        v["records_description"] = _format_data_elements(gap)
        v["purpose"] = f"Care coordination and service continuity: {gap.get('impact', '')[:200]}"
    elif atype == "compact":
        v["government_a_name"] = party_a
        v["government_b_name"] = party_b
        v["purpose"] = gap.get("impact", "")
        v["scope"] = gap.get("what_it_would_take", "")
        v["governance_structure"] = "Joint oversight committee with equal representation"
        v["funding_arrangement"] = "Costs shared proportionally based on usage"
        v["data_provisions"] = _format_data_elements(gap)
        v["privacy_protections"] = "All applicable federal and state privacy laws"
    elif atype == "joint_funding":
        v["agency_a_name"] = party_a
        v["agency_b_name"] = party_b
        v["project_description"] = gap.get("what_it_would_take", "Technical integration project")
        v["funding_a_amount"] = "[AMOUNT]"
        v["funding_b_amount"] = "[AMOUNT]"
        v["total_budget"] = "[TOTAL]"
        v["deliverables"] = "1. Technical integration between systems\n2. Testing and validation\n3. Staff training\n4. Ongoing maintenance plan"
        v["timeline"] = "Phase 1: Requirements (3 months)\nPhase 2: Development (6 months)\nPhase 3: Testing (2 months)\nPhase 4: Deployment (1 month)"
        v["reporting_requirements"] = "Monthly progress reports, quarterly financial reports, annual audit"
        v["ip_ownership"] = "Joint ownership of all deliverables"

    return v


def _format_data_elements(gap: dict) -> str:
    """Extract and format relevant data elements from a gap description."""
    desc = gap.get("barrier_description", "")
    what = gap.get("what_it_would_take", "")
    impact = gap.get("impact", "")
    combined = f"{desc} {what} {impact}".lower()

    elements = []
    data_keywords = {
        "health records": "Health records and clinical data",
        "medications": "Medication lists and prescribing information",
        "diagnoses": "Diagnosis and condition information",
        "treatment": "Treatment history and plans",
        "eligibility": "Eligibility and enrollment status",
        "claims": "Claims and encounter data",
        "housing": "Housing status and history",
        "substance use": "Substance use disorder treatment records",
        "mental health": "Mental health records and assessments",
        "criminal history": "Criminal justice records",
        "education records": "Education records and IEP information",
        "disability": "Disability status and accommodations",
        "income": "Income and benefits information",
        "demographics": "Demographic information",
    }

    for keyword, label in data_keywords.items():
        if keyword in combined:
            elements.append(label)

    return "\n".join(f"- {e}" for e in elements) if elements else "- As specified in the governing data sharing provisions"


def _extract_data_elements(gap: dict) -> list[str]:
    """Return a list of data elements from gap."""
    desc = gap.get("barrier_description", "").lower()
    elements = []
    mapping = {
        "health records": "health_records",
        "phi": "protected_health_information",
        "medications": "medications",
        "treatment": "treatment_records",
        "eligibility": "eligibility_status",
        "housing": "housing_status",
        "substance use": "sud_records",
        "mental health": "mental_health_records",
        "education": "education_records",
        "criminal": "criminal_justice_records",
        "disability": "disability_information",
    }
    for keyword, element in mapping.items():
        if keyword in desc:
            elements.append(element)
    return elements or ["general_records"]


def _build_privacy_provisions(gap: dict, agreement_type: str) -> list[str]:
    """Build privacy provision requirements based on gap and agreement type."""
    provisions = ["Purpose limitation", "Minimum necessary standard", "Data return/destruction on termination"]
    barrier_law = gap.get("barrier_law", "").lower()
    if "hipaa" in barrier_law or agreement_type in ("BAA", "HIPAA_consent"):
        provisions.extend(["HIPAA Privacy Rule compliance", "HIPAA Security Rule compliance", "Breach notification (60 days)"])
    if "42 cfr" in barrier_law or agreement_type in ("QSOA", "42CFR_consent"):
        provisions.extend(["42 CFR Part 2 compliance", "Re-disclosure prohibition", "Criminal penalty notice"])
    if "ferpa" in barrier_law or agreement_type == "FERPA_consent":
        provisions.extend(["FERPA compliance", "Right to inspect records", "Parental consent"])
    if "cjis" in barrier_law:
        provisions.extend(["CJIS Security Policy compliance", "Fingerprint background checks", "Encryption requirements"])
    return provisions


def _get_signatories(agreement_type: str, party_a: str, party_b: str) -> list[str]:
    """Return required signatories for an agreement type."""
    base = [f"{party_a} — Authorized Official", f"{party_b} — Authorized Official"]
    if agreement_type in ("HIPAA_consent", "42CFR_consent", "FERPA_consent"):
        return ["Individual (or authorized representative)"]
    if agreement_type == "compact":
        return [f"{party_a} — Agency Head or Designee", f"{party_b} — Agency Head or Designee", "Legal Counsel (both parties)"]
    return base


def _get_key_terms(gap: dict, template: Template) -> list[str]:
    """Extract key terms / considerations from the gap."""
    terms = []
    if gap.get("consent_closable"):
        terms.append("Person-authorizable: individual consent can close this gap")
    if gap.get("barrier_law"):
        terms.append(f"Primary legal barrier: {gap['barrier_law']}")
    if gap.get("severity") in ("critical", "high"):
        terms.append(f"Gap severity: {gap['severity']}")
    terms.append(f"Barrier type: {gap.get('barrier_type', 'unspecified')}")
    return terms


def _get_legal_authority(gap: dict) -> str:
    """Determine legal authority citation for an IDSA."""
    law = gap.get("barrier_law", "")
    if law:
        return f"Applicable provisions of {law}, state intergovernmental cooperation statutes, and other applicable federal and state law."
    return "State intergovernmental cooperation statutes and applicable federal law."
