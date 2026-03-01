"""Budget computation router for THE DOME API.

Provides endpoints to compute and retrieve Whole-Person Budgets, classify
fiscal trajectories, and run wrong-pocket analyses.  Budget computation
delegates to ``BudgetEngine``; trajectory classification delegates to
``TrajectoryClassifier``; wrong-pocket analysis delegates to
``WrongPocketAnalyzer``.
"""

from __future__ import annotations

import logging
from datetime import date, datetime, timezone
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from dome.db.database import get_session
from dome.db.tables import FiscalEventTable, PersonTable
from dome.models.budget_key import BudgetHorizon, PersonBudgetKey
from dome.models.budget_output import WholePersonBudget
from dome.models.dynamic_state import DynamicState
from dome.models.identity import IdentitySpine
from dome.models.static_profile import StaticProfile
from dome.models.trajectory import FiscalTrajectoryTag
from dome.schemas.budget_schemas import BudgetComputeRequest, WrongPocketRequest

logger = logging.getLogger("dome.api.budgets")

router = APIRouter(prefix="/persons", tags=["budgets"])


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


async def _load_fiscal_events(uid: str, session: AsyncSession) -> list[dict]:
    """Load all fiscal event rows for a person as dicts."""
    stmt = (
        select(FiscalEventTable)
        .where(FiscalEventTable.person_uid == uid)
        .order_by(FiscalEventTable.event_date.asc())
    )
    result = await session.execute(stmt)
    rows = result.scalars().all()
    events = []
    for row in rows:
        events.append(
            {
                "event_id": row.event_id,
                "person_uid": row.person_uid,
                "event_date": str(row.event_date.date()) if row.event_date else None,
                "payer_level": row.payer_level,
                "payer_entity": row.payer_entity,
                "program_or_fund": row.program_or_fund,
                "domain": row.domain,
                "mechanism": row.mechanism,
                "service_category": row.service_category,
                "utilization_unit": row.utilization_unit,
                "quantity": row.quantity,
                "amount_paid": row.amount_paid,
                "amount_type": row.amount_type,
                "confidence": row.confidence,
                "data_source_system": row.data_source_system,
                "attribution_tags": row.attribution_tags_json or [],
            }
        )
    return events


def _build_budget_key_from_row(row: PersonTable) -> PersonBudgetKey:
    """Reconstruct a ``PersonBudgetKey`` from the stored JSON blob."""
    if row.budget_key_json:
        return PersonBudgetKey(**row.budget_key_json)
    raise HTTPException(
        status_code=400,
        detail="Person has no budget key data — create the person first",
    )


def _compute_horizons(
    req: BudgetComputeRequest,
) -> list[BudgetHorizon]:
    """Build ``BudgetHorizon`` objects from the request's horizon specs."""
    today = date.today()
    horizons: list[BudgetHorizon] = []
    label_years = {"1y": 1, "5y": 5, "20y": 20, "lifetime": 80}
    for h in req.horizons:
        start = h.start_date or today
        end = h.end_date or date(
            today.year + label_years.get(h.label, 1), today.month, today.day
        )
        horizons.append(
            BudgetHorizon(
                label=h.label,
                start_date=start,
                end_date=end,
                time_step=h.time_step,
            )
        )
    return horizons


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------


@router.post("/{uid}/budget", summary="Compute whole-person budget")
async def compute_budget(
    uid: str,
    req: BudgetComputeRequest,
    session: AsyncSession = Depends(get_session),
) -> dict:
    """Compute the Whole-Person Budget for person *uid*.

    Loads the person record and fiscal history from the database, builds
    a ``PersonBudgetKey`` enriched with the requested horizons, calls the
    ``BudgetEngine.compute()`` method, persists the result to
    ``PersonTable.budget_json``, and returns the full
    ``WholePersonBudget``.

    If the BudgetEngine is not available (missing dependencies), a
    deterministic fallback budget is generated from the fiscal history.
    """
    row = await _load_person_row(uid, session)
    fiscal_events = await _load_fiscal_events(uid, session)

    # Build budget key with horizons
    budget_key = _build_budget_key_from_row(row)
    horizons = _compute_horizons(req)
    budget_key = budget_key.model_copy(update={"budget_horizons": horizons})

    # Attempt to use the real BudgetEngine
    try:
        from dome.engines.budget_engine import BudgetEngine

        engine = BudgetEngine()
        budget = engine.compute(budget_key, fiscal_events)
    except (ImportError, AttributeError) as exc:
        logger.warning(
            "BudgetEngine unavailable (%s), generating fallback budget", exc
        )
        budget = _fallback_budget(uid, budget_key, fiscal_events)
    except Exception as exc:
        logger.exception("BudgetEngine.compute() failed")
        raise HTTPException(
            status_code=500, detail=f"Budget computation failed: {exc}"
        ) from exc

    # Persist to DB
    budget_dict = budget.model_dump(mode="json") if hasattr(budget, "model_dump") else budget
    row.budget_json = budget_dict
    await session.flush()

    logger.info("Computed budget for person %s", uid)
    return budget_dict


@router.get("/{uid}/budget", summary="Get stored budget")
async def get_budget(
    uid: str,
    session: AsyncSession = Depends(get_session),
) -> dict:
    """Retrieve the most recently computed budget for person *uid*.

    Returns the stored ``WholePersonBudget`` JSON from the person record.
    Raises 404 if no budget has been computed yet.
    """
    row = await _load_person_row(uid, session)
    if not row.budget_json:
        raise HTTPException(
            status_code=404,
            detail=f"No budget computed yet for person {uid!r}",
        )
    return row.budget_json


@router.get("/{uid}/trajectory", summary="Classify fiscal trajectory")
async def get_trajectory(
    uid: str,
    session: AsyncSession = Depends(get_session),
) -> dict:
    """Classify the lifetime fiscal trajectory for person *uid*.

    Loads the person and their stored budget, runs
    ``TrajectoryClassifier.classify()`` to produce a
    ``FiscalTrajectoryTag``, and returns it.

    If no stored budget exists, a 400 error is raised advising the caller
    to compute the budget first.
    """
    row = await _load_person_row(uid, session)
    if not row.budget_json:
        raise HTTPException(
            status_code=400,
            detail="Compute the budget first before classifying trajectory",
        )

    budget = WholePersonBudget(**row.budget_json)

    try:
        from dome.engines.trajectory_classifier import TrajectoryClassifier

        classifier = TrajectoryClassifier()
        tag = classifier.classify(budget)
    except (ImportError, AttributeError) as exc:
        logger.warning(
            "TrajectoryClassifier unavailable (%s), generating fallback", exc
        )
        tag = _fallback_trajectory(uid, budget)
    except Exception as exc:
        logger.exception("TrajectoryClassifier.classify() failed")
        raise HTTPException(
            status_code=500, detail=f"Trajectory classification failed: {exc}"
        ) from exc

    tag_dict = tag.model_dump(mode="json") if hasattr(tag, "model_dump") else tag
    row.trajectory_json = tag_dict
    await session.flush()

    logger.info("Classified trajectory for person %s", uid)
    return tag_dict


@router.get("/{uid}/wrong-pocket", summary="Wrong-pocket analysis")
async def wrong_pocket_analysis(
    uid: str,
    horizon_label: str = Query("lifetime", description="Time horizon for analysis"),
    session: AsyncSession = Depends(get_session),
) -> dict:
    """Run a wrong-pocket analysis for person *uid*.

    The wrong-pocket problem occurs when the payer who funds an
    intervention is different from the payer who reaps the savings.
    This endpoint loads the person and their budget, runs
    ``WrongPocketAnalyzer.analyze()``, and returns the analysis matrix.
    """
    row = await _load_person_row(uid, session)
    if not row.budget_json:
        raise HTTPException(
            status_code=400,
            detail="Compute the budget first before running wrong-pocket analysis",
        )

    budget = WholePersonBudget(**row.budget_json)

    try:
        from dome.engines.wrong_pocket_analyzer import WrongPocketAnalyzer

        analyzer = WrongPocketAnalyzer()
        matrix = analyzer.analyze(
            person_uid=uid,
            budget=budget,
            horizon_label=horizon_label,
        )
    except (ImportError, AttributeError) as exc:
        logger.warning(
            "WrongPocketAnalyzer unavailable (%s), generating fallback", exc
        )
        matrix = _fallback_wrong_pocket(uid, budget, horizon_label)
    except Exception as exc:
        logger.exception("WrongPocketAnalyzer.analyze() failed")
        raise HTTPException(
            status_code=500, detail=f"Wrong-pocket analysis failed: {exc}"
        ) from exc

    result = matrix.model_dump(mode="json") if hasattr(matrix, "model_dump") else matrix
    logger.info("Wrong-pocket analysis completed for person %s", uid)
    return result


# ---------------------------------------------------------------------------
# Fallback generators — used when engine modules are not yet available
# ---------------------------------------------------------------------------


def _fallback_budget(
    uid: str,
    budget_key: PersonBudgetKey,
    fiscal_events: list[dict],
) -> WholePersonBudget:
    """Generate a deterministic placeholder budget from fiscal history."""
    from dome.models.budget_output import (
        HorizonBudget,
        PayerView,
        RiskProfile,
        WholePersonBudget,
    )

    total_historical = sum(e.get("amount_paid", 0) for e in fiscal_events)
    annual_estimate = total_historical if total_historical > 0 else 25000.0

    horizons_out = []
    for h in budget_key.budget_horizons:
        label_years = {"1y": 1, "5y": 5, "20y": 20, "lifetime": 80}
        years = label_years.get(h.label, 1)
        projected = annual_estimate * years

        payer_view = PayerView(
            federal_expected_spend=projected * 0.45,
            state_expected_spend=projected * 0.25,
            local_expected_spend=projected * 0.15,
            healthcare_delivery_expected_spend=projected * 0.10,
            nonprofit_expected_spend=projected * 0.05,
        )
        risk_profile = RiskProfile(
            p50_total_cost=projected,
            p90_total_cost=projected * 1.5,
            p99_total_cost=projected * 3.0,
        )
        horizons_out.append(
            HorizonBudget(
                label=h.label,
                start_date=h.start_date,
                end_date=h.end_date,
                payer_view=payer_view,
                risk_profile=risk_profile,
            )
        )

    return WholePersonBudget(
        person_uid=uid,
        generated_at=datetime.now(tz=timezone.utc),
        horizons=horizons_out,
    )


def _fallback_trajectory(
    uid: str, budget: WholePersonBudget
) -> FiscalTrajectoryTag:
    """Generate a deterministic placeholder trajectory from a budget."""
    # Find lifetime horizon if available, else use last
    lifetime_cost = 0.0
    for h in budget.horizons:
        if h.label == "lifetime":
            lifetime_cost = h.risk_profile.p50_total_cost
            break
    else:
        if budget.horizons:
            lifetime_cost = budget.horizons[-1].risk_profile.p50_total_cost

    # Simple tier logic
    if lifetime_cost <= 100_000:
        trajectory = "net_contributor"
    elif lifetime_cost <= 500_000:
        trajectory = "break_even"
    elif lifetime_cost <= 2_000_000:
        trajectory = "moderate_net_cost"
    elif lifetime_cost <= 5_000_000:
        trajectory = "high_net_cost"
    else:
        trajectory = "catastrophic_net_cost"

    return FiscalTrajectoryTag(
        person_uid=uid,
        horizon="lifetime",
        trajectory=trajectory,
        net_fiscal_impact_npv=-lifetime_cost,
    )


def _fallback_wrong_pocket(
    uid: str, budget: WholePersonBudget, horizon_label: str
) -> dict[str, Any]:
    """Generate a placeholder wrong-pocket analysis dict."""
    horizon = None
    for h in budget.horizons:
        if h.label == horizon_label:
            horizon = h
            break
    if horizon is None and budget.horizons:
        horizon = budget.horizons[0]

    if horizon is None:
        return {
            "person_uid": uid,
            "horizon_label": horizon_label,
            "analysis": "No budget horizons available",
        }

    pv = horizon.payer_view
    return {
        "person_uid": uid,
        "horizon_label": horizon_label,
        "payer_spending": {
            "federal": pv.federal_expected_spend,
            "state": pv.state_expected_spend,
            "local": pv.local_expected_spend,
            "health_system": pv.healthcare_delivery_expected_spend,
            "nonprofit": pv.nonprofit_expected_spend,
        },
        "wrong_pocket_flags": {
            "federal_pays_state_saves": pv.federal_expected_spend > pv.state_expected_spend * 2,
            "state_pays_local_saves": pv.state_expected_spend > pv.local_expected_spend * 2,
        },
        "note": "Fallback analysis — WrongPocketAnalyzer engine not available",
    }
