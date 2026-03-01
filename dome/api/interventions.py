"""Intervention router for THE DOME API.

Provides an endpoint to generate an optimal intervention plan in response
to a detected cascade alert.  Plan generation delegates to
``InterventionRecommender`` which selects interventions from the library,
estimates costs and savings, and computes expected ROI.
"""

from __future__ import annotations

import logging
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from dome.db.database import get_session
from dome.db.tables import CascadeAlertTable, InterventionPlanTable, PersonTable
from dome.schemas.intervention_schemas import (
    InterventionPlanRequest,
    InterventionPlanSummary,
    InterventionSummary,
)

logger = logging.getLogger("dome.api.interventions")

router = APIRouter(prefix="/persons", tags=["interventions"])


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


async def _load_person_row(uid: str, session: AsyncSession) -> PersonTable:
    """Load a ``PersonTable`` row by *person_uid*, raising 404 if absent."""
    stmt = select(PersonTable).where(PersonTable.person_uid == uid)
    result = await session.execute(stmt)
    row = result.scalar_one_or_none()
    if row is None:
        raise HTTPException(status_code=404, detail=f"Person {uid!r} not found")
    return row


async def _load_cascade_alert(
    alert_id: str, uid: str, session: AsyncSession
) -> CascadeAlertTable:
    """Load a ``CascadeAlertTable`` row, ensuring it belongs to *uid*."""
    stmt = select(CascadeAlertTable).where(
        CascadeAlertTable.alert_id == alert_id,
        CascadeAlertTable.person_uid == uid,
    )
    result = await session.execute(stmt)
    row = result.scalar_one_or_none()
    if row is None:
        raise HTTPException(
            status_code=404,
            detail=f"Cascade alert {alert_id!r} not found for person {uid!r}",
        )
    return row


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------


@router.post(
    "/{uid}/intervention-plan",
    summary="Generate intervention plan",
    response_model=InterventionPlanSummary,
)
async def create_intervention_plan(
    uid: str,
    req: InterventionPlanRequest,
    session: AsyncSession = Depends(get_session),
) -> InterventionPlanSummary:
    """Generate an optimal intervention plan for person *uid*.

    Loads the referenced cascade alert, invokes
    ``InterventionRecommender.recommend()`` to select the best
    combination of interventions within budget constraints, persists the
    plan to the ``intervention_plans`` table, and returns an
    ``InterventionPlanSummary``.

    If the InterventionRecommender engine is not available, a fallback
    plan is generated from the cascade alert's recommended interventions.
    """
    await _load_person_row(uid, session)
    alert_row = await _load_cascade_alert(req.cascade_alert_id, uid, session)

    try:
        from dome.engines.intervention_recommender import InterventionRecommender

        recommender = InterventionRecommender()
        plan = recommender.recommend(
            person_uid=uid,
            cascade_alert_id=req.cascade_alert_id,
            path_a_cost=alert_row.path_a_projected_cost or 0,
            path_b_cost=alert_row.path_b_projected_cost or 0,
            recommended_interventions=alert_row.recommended_interventions_json or [],
            max_budget=req.max_budget,
            max_interventions=req.max_interventions,
        )
    except (ImportError, AttributeError) as exc:
        logger.warning(
            "InterventionRecommender unavailable (%s), generating fallback plan",
            exc,
        )
        plan = _fallback_plan(uid, alert_row, req)
    except Exception as exc:
        logger.exception("InterventionRecommender.recommend() failed")
        raise HTTPException(
            status_code=500, detail=f"Intervention planning failed: {exc}"
        ) from exc

    # Normalize to dict
    if hasattr(plan, "model_dump"):
        plan_data = plan.model_dump(mode="json")
    elif isinstance(plan, dict):
        plan_data = plan
    else:
        plan_data = dict(plan)

    plan_id = plan_data.get("plan_id", str(uuid4()))
    interventions_list = plan_data.get("interventions", [])
    total_cost = plan_data.get("total_cost", 0.0)
    expected_savings = plan_data.get("expected_savings", 0.0)
    expected_roi = plan_data.get("expected_roi", 0.0)

    # Persist to DB
    plan_row = InterventionPlanTable(
        plan_id=plan_id,
        person_uid=uid,
        cascade_alert_id=req.cascade_alert_id,
        interventions_json=interventions_list,
        total_cost=total_cost,
        expected_savings=expected_savings,
        expected_roi=expected_roi,
    )
    session.add(plan_row)
    await session.flush()

    # Build response
    intervention_summaries = []
    for iv in interventions_list:
        if isinstance(iv, dict):
            intervention_summaries.append(
                InterventionSummary(
                    intervention_id=iv.get("intervention_id", "unknown"),
                    name=iv.get("name", "Unknown Intervention"),
                    cost_estimate=iv.get("cost_estimate", iv.get("cost_min", 0)),
                    break_probability=iv.get("break_probability", 0.5),
                    time_to_effect_months=iv.get("time_to_effect_months", 3.0),
                )
            )

    summary = InterventionPlanSummary(
        plan_id=plan_id,
        cascade_alert_id=req.cascade_alert_id,
        interventions=intervention_summaries,
        total_cost=total_cost,
        expected_savings=expected_savings,
        expected_roi=expected_roi,
    )

    logger.info("Created intervention plan %s for person %s", plan_id, uid)
    return summary


# ---------------------------------------------------------------------------
# Fallback plan generator
# ---------------------------------------------------------------------------

# Library of known interventions with cost / effectiveness estimates
_INTERVENTION_LIBRARY: dict[str, dict] = {
    "rapid_rehousing": {
        "intervention_id": "rapid_rehousing",
        "name": "Rapid Rehousing",
        "cost_estimate": 8_000.0,
        "cost_min": 5_000.0,
        "cost_max": 15_000.0,
        "break_probability": 0.70,
        "time_to_effect_months": 2.0,
    },
    "care_coordination": {
        "intervention_id": "care_coordination",
        "name": "Care Coordination",
        "cost_estimate": 3_500.0,
        "cost_min": 2_000.0,
        "cost_max": 6_000.0,
        "break_probability": 0.60,
        "time_to_effect_months": 1.0,
    },
    "behavioral_health_referral": {
        "intervention_id": "behavioral_health_referral",
        "name": "Behavioral Health Referral",
        "cost_estimate": 4_000.0,
        "cost_min": 2_500.0,
        "cost_max": 8_000.0,
        "break_probability": 0.55,
        "time_to_effect_months": 3.0,
    },
    "workforce_development": {
        "intervention_id": "workforce_development",
        "name": "Workforce Development Program",
        "cost_estimate": 6_000.0,
        "cost_min": 3_000.0,
        "cost_max": 12_000.0,
        "break_probability": 0.50,
        "time_to_effect_months": 6.0,
    },
    "transitional_employment": {
        "intervention_id": "transitional_employment",
        "name": "Transitional Employment",
        "cost_estimate": 10_000.0,
        "cost_min": 5_000.0,
        "cost_max": 18_000.0,
        "break_probability": 0.65,
        "time_to_effect_months": 3.0,
    },
    "legal_aid": {
        "intervention_id": "legal_aid",
        "name": "Legal Aid Services",
        "cost_estimate": 2_500.0,
        "cost_min": 1_000.0,
        "cost_max": 5_000.0,
        "break_probability": 0.45,
        "time_to_effect_months": 2.0,
    },
    "chronic_care_management": {
        "intervention_id": "chronic_care_management",
        "name": "Chronic Care Management",
        "cost_estimate": 5_000.0,
        "cost_min": 3_000.0,
        "cost_max": 10_000.0,
        "break_probability": 0.65,
        "time_to_effect_months": 3.0,
    },
    "medication_therapy_management": {
        "intervention_id": "medication_therapy_management",
        "name": "Medication Therapy Management",
        "cost_estimate": 2_000.0,
        "cost_min": 800.0,
        "cost_max": 4_000.0,
        "break_probability": 0.60,
        "time_to_effect_months": 1.0,
    },
    "community_health_worker": {
        "intervention_id": "community_health_worker",
        "name": "Community Health Worker",
        "cost_estimate": 4_500.0,
        "cost_min": 2_500.0,
        "cost_max": 8_000.0,
        "break_probability": 0.55,
        "time_to_effect_months": 2.0,
    },
}


def _fallback_plan(
    uid: str,
    alert_row: CascadeAlertTable,
    req: InterventionPlanRequest,
) -> dict:
    """Generate a heuristic intervention plan from the alert data.

    Selects interventions from the built-in library that match the
    cascade alert's recommended list, respecting budget constraints.
    """
    recommended = alert_row.recommended_interventions_json or []
    path_a = alert_row.path_a_projected_cost or 0
    path_b = alert_row.path_b_projected_cost or 0
    potential_savings = path_a - path_b

    # Select interventions from library
    selected: list[dict] = []
    total_cost = 0.0
    for iv_id in recommended:
        if len(selected) >= req.max_interventions:
            break
        iv = _INTERVENTION_LIBRARY.get(iv_id)
        if iv is None:
            # Create a generic intervention for unknown IDs
            iv = {
                "intervention_id": iv_id,
                "name": iv_id.replace("_", " ").title(),
                "cost_estimate": 5_000.0,
                "cost_min": 2_000.0,
                "cost_max": 10_000.0,
                "break_probability": 0.50,
                "time_to_effect_months": 3.0,
            }
        cost = iv["cost_estimate"]
        if req.max_budget is not None and total_cost + cost > req.max_budget:
            continue
        selected.append(iv)
        total_cost += cost

    expected_savings = potential_savings * 0.6 if potential_savings > 0 else 0.0
    expected_roi = expected_savings / total_cost if total_cost > 0 else 0.0

    return {
        "plan_id": str(uuid4()),
        "person_uid": uid,
        "cascade_alert_id": alert_row.alert_id,
        "interventions": selected,
        "total_cost": total_cost,
        "expected_savings": expected_savings,
        "expected_roi": round(expected_roi, 2),
    }
