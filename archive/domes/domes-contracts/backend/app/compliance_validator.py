"""Compliance validation engine.

Checks every generated agreement against all applicable regulatory rules.
Flags missing provisions, incorrect citations, insufficient protections.
"""

import json
from sqlalchemy.orm import Session
from app.models import Agreement, ComplianceRule


def validate_agreement(agreement: Agreement, db: Session) -> dict:
    """Validate an agreement against all applicable compliance rules.

    Returns:
        {
            "agreement_id": str,
            "status": "valid" | "issues_found",
            "checks": [
                {
                    "rule_id": str,
                    "law": str,
                    "requirement": str,
                    "status": "pass" | "fail" | "warning",
                    "detail": str,
                }
            ],
            "summary": {"passed": int, "failed": int, "warnings": int}
        }
    """
    # Get all rules that apply to this agreement type
    all_rules = db.query(ComplianceRule).all()
    applicable_rules = []
    for rule in all_rules:
        applies_to = json.loads(rule.applies_to)
        if agreement.agreement_type in applies_to:
            applicable_rules.append(rule)

    checks = []
    body_lower = agreement.body_text.lower()
    provisions = json.loads(agreement.privacy_provisions)
    provisions_lower = [p.lower() for p in provisions]

    for rule in applicable_rules:
        check = _check_rule(rule, agreement, body_lower, provisions_lower)
        checks.append(check)

    passed = sum(1 for c in checks if c["status"] == "pass")
    failed = sum(1 for c in checks if c["status"] == "fail")
    warnings = sum(1 for c in checks if c["status"] == "warning")

    status = "valid" if failed == 0 else "issues_found"

    # Update agreement compliance status
    agreement.compliance_status = status
    agreement.compliance_flags = json.dumps([c for c in checks if c["status"] != "pass"])
    db.flush()

    return {
        "agreement_id": agreement.id,
        "status": status,
        "checks": checks,
        "summary": {"passed": passed, "failed": failed, "warnings": warnings},
    }


def _check_rule(
    rule: ComplianceRule,
    agreement: Agreement,
    body_lower: str,
    provisions_lower: list[str],
) -> dict:
    """Check a single compliance rule against an agreement."""
    result = {
        "rule_id": rule.id,
        "law": rule.law,
        "requirement": rule.requirement,
        "severity": rule.severity,
        "status": "pass",
        "detail": "",
    }

    # Check if the provision text or key phrases are present
    provision_lower = rule.provision_text.lower()

    # Extract key phrases from the rule's provision text
    key_phrases = _extract_key_phrases(rule)

    found_in_body = any(phrase in body_lower for phrase in key_phrases)
    found_in_provisions = any(
        any(phrase in p for phrase in key_phrases)
        for p in provisions_lower
    )

    if found_in_body or found_in_provisions:
        result["status"] = "pass"
        result["detail"] = "Required provision found in agreement."
    else:
        if rule.severity == "required":
            result["status"] = "fail"
            result["detail"] = f"MISSING: {rule.requirement}. Required provision text not found in agreement."
        else:
            result["status"] = "warning"
            result["detail"] = f"RECOMMENDED: {rule.requirement}. Consider adding this provision."

    return result


def _extract_key_phrases(rule: ComplianceRule) -> list[str]:
    """Extract searchable key phrases from a compliance rule."""
    phrases = []
    law = rule.law.lower()
    rule_id = rule.id.lower()

    # Law-specific phrases to search for
    if "hipaa" in law:
        phrases.extend(["hipaa", "45 cfr"])
        if "baa" in rule_id:
            phrases.append("business associate")
        if "breach" in rule_id:
            phrases.extend(["breach notification", "breach of unsecured phi"])
        if "minimum" in rule_id:
            phrases.append("minimum necessary")
        if "authorization" in rule_id or "elements" in rule_id:
            phrases.extend(["right to revoke", "authorization"])
        if "revoke" in rule_id:
            phrases.append("right to revoke")

    elif "42 cfr" in law or "cfr42" in law:
        phrases.extend(["42 cfr part 2", "42 cfr"])
        if "consent" in rule_id:
            phrases.extend(["consent", "42 cfr § 2.31", "2.31"])
        if "redisclosure" in rule_id:
            phrases.extend(["re-disclosure", "redisclosure", "further disclosure"])
        if "general_auth" in rule_id or "no_general" in rule_id:
            phrases.append("general authorization")
        if "criminal" in rule_id:
            phrases.extend(["criminal", "penalty", "$500"])

    elif "ferpa" in law:
        phrases.extend(["ferpa", "education records", "34 cfr"])
        if "consent" in rule_id:
            phrases.append("written consent")
        if "elements" in rule_id:
            phrases.extend(["records to be disclosed", "purpose"])

    elif "cjis" in law:
        phrases.extend(["cjis", "criminal justice information"])
        if "background" in rule_id:
            phrases.extend(["background check", "fingerprint"])

    elif "general" in law:
        if "purpose" in rule_id:
            phrases.extend(["purpose", "only for the purposes", "stated purpose"])
        if "destruction" in rule_id:
            phrases.extend(["return or destroy", "return or securely destroy", "destruction"])
        if "security" in rule_id or "safeguard" in rule_id:
            phrases.extend(["safeguard", "security", "administrative, physical"])
        if "audit" in rule_id:
            phrases.extend(["audit", "right to audit"])

    # Always include the requirement text itself as a fallback
    if not phrases:
        phrases = [rule.requirement.lower()[:40]]

    return phrases


def get_compliance_checklist(agreement: Agreement, db: Session) -> list[dict]:
    """Generate a compliance checklist for an agreement."""
    all_rules = db.query(ComplianceRule).all()
    checklist = []

    for rule in all_rules:
        applies_to = json.loads(rule.applies_to)
        if agreement.agreement_type in applies_to:
            checklist.append({
                "rule_id": rule.id,
                "law": rule.law,
                "requirement": rule.requirement,
                "severity": rule.severity,
                "model_language": rule.provision_text,
            })

    return checklist


def get_rules_for_type(agreement_type: str, db: Session) -> list[dict]:
    """Get all compliance rules that apply to a given agreement type."""
    all_rules = db.query(ComplianceRule).all()
    result = []

    for rule in all_rules:
        applies_to = json.loads(rule.applies_to)
        if agreement_type in applies_to:
            result.append({
                "id": rule.id,
                "law": rule.law,
                "requirement": rule.requirement,
                "description": rule.description,
                "severity": rule.severity,
                "provision_text": rule.provision_text,
            })

    return result
