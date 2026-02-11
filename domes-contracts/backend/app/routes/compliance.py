"""Compliance validation routes.

Validate agreements against regulatory rules, browse the rule library,
and generate pre-validation checklists by agreement type.
"""

import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Agreement, ComplianceRule
from app.compliance_validator import validate_agreement, get_rules_for_type

router = APIRouter(prefix="/api", tags=["compliance"])


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

def _rule_dict(rule: ComplianceRule) -> dict:
    """Serialize a ComplianceRule row to a plain dict."""
    return {
        "id": rule.id,
        "law": rule.law,
        "requirement": rule.requirement,
        "description": rule.description,
        "applies_to": json.loads(rule.applies_to),
        "severity": rule.severity,
        "provision_text": rule.provision_text,
    }


# ---------------------------------------------------------------------------
# POST /api/compliance/validate/{agreement_id}
# ---------------------------------------------------------------------------

@router.post("/compliance/validate/{agreement_id}")
def validate_single(agreement_id: str, db: Session = Depends(get_db)):
    """Validate a specific agreement against all applicable compliance rules."""
    agreement = db.query(Agreement).filter(Agreement.id == agreement_id).first()
    if not agreement:
        raise HTTPException(status_code=404, detail=f"Agreement '{agreement_id}' not found")

    result = validate_agreement(agreement, db)
    db.commit()
    return result


# ---------------------------------------------------------------------------
# GET /api/compliance/rules
# ---------------------------------------------------------------------------

@router.get("/compliance/rules")
def list_rules(
    law: str | None = None,
    agreement_type: str | None = None,
    db: Session = Depends(get_db),
):
    """List all compliance rules, optionally filtered by law or agreement type."""
    query = db.query(ComplianceRule)

    if law:
        query = query.filter(ComplianceRule.law == law)

    rules = query.all()

    # Post-filter by agreement_type (stored as JSON list in a text column)
    if agreement_type:
        rules = [
            r for r in rules
            if agreement_type in json.loads(r.applies_to)
        ]

    return {
        "count": len(rules),
        "rules": [_rule_dict(r) for r in rules],
    }


# ---------------------------------------------------------------------------
# GET /api/compliance/rules/{rule_id}
# ---------------------------------------------------------------------------

@router.get("/compliance/rules/{rule_id}")
def get_rule(rule_id: str, db: Session = Depends(get_db)):
    """Get a single compliance rule with full detail."""
    rule = db.query(ComplianceRule).filter(ComplianceRule.id == rule_id).first()
    if not rule:
        raise HTTPException(status_code=404, detail=f"Rule '{rule_id}' not found")
    return _rule_dict(rule)


# ---------------------------------------------------------------------------
# GET /api/compliance/checklist/{agreement_type}
# ---------------------------------------------------------------------------

@router.get("/compliance/checklist/{agreement_type}")
def get_checklist(agreement_type: str, db: Session = Depends(get_db)):
    """Get the compliance checklist for an agreement type (no actual agreement needed)."""
    rules = get_rules_for_type(agreement_type, db)
    return {
        "agreement_type": agreement_type,
        "count": len(rules),
        "checklist": rules,
    }


# ---------------------------------------------------------------------------
# POST /api/compliance/validate-all
# ---------------------------------------------------------------------------

@router.post("/compliance/validate-all")
def validate_all(db: Session = Depends(get_db)):
    """Validate every agreement whose compliance_status is 'unchecked'."""
    unchecked = (
        db.query(Agreement)
        .filter(Agreement.compliance_status == "unchecked")
        .all()
    )

    results = []
    total_passed = 0
    total_failed = 0
    total_warnings = 0

    for agreement in unchecked:
        result = validate_agreement(agreement, db)
        results.append(result)
        total_passed += result["summary"]["passed"]
        total_failed += result["summary"]["failed"]
        total_warnings += result["summary"]["warnings"]

    db.commit()

    valid_count = sum(1 for r in results if r["status"] == "valid")
    issues_count = sum(1 for r in results if r["status"] == "issues_found")

    return {
        "agreements_checked": len(results),
        "valid": valid_count,
        "issues_found": issues_count,
        "total_checks": {
            "passed": total_passed,
            "failed": total_failed,
            "warnings": total_warnings,
        },
        "results": results,
    }
