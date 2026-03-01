"""Dashboard data router for THE DOME API.

Provides endpoints to assemble a coordinator-facing dashboard view for a
single person and to compute benefits-cliff analysis.  The dashboard
aggregates data from the person record, budget, cascade alerts, and
simulation results into a single payload.
"""

from __future__ import annotations

import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from dome.db.database import get_session
from dome.db.tables import (
    CascadeAlertTable,
    PersonTable,
    SimulationResultTable,
)
from dome.models.budget_key import PersonBudgetKey
from dome.models.budget_output import WholePersonBudget
from dome.models.dynamic_state import DynamicState
from dome.schemas.intervention_schemas import BenefitsCliffPoint, DashboardData

logger = logging.getLogger("dome.api.dashboards")

router = APIRouter(prefix="/persons", tags=["dashboards"])


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


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------


@router.get(
    "/{uid}/dashboard",
    summary="Get dashboard data",
    response_model=DashboardData,
)
async def get_dashboard(
    uid: str,
    session: AsyncSession = Depends(get_session),
) -> DashboardData:
    """Assemble coordinator dashboard data for person *uid*.

    Loads the person record, stored budget, cascade alerts, and latest
    simulation results, then composes a ``DashboardData`` response
    containing the key metrics a coordinator needs for triage.
    """
    row = await _load_person_row(uid, session)

    # --- Person basics ---
    identity = row.identity_spine_json or {}
    dynamic = row.dynamic_state_json or {}
    name_hash = identity.get("name_hash", "unknown")
    age = dynamic.get("age_years", 0.0)

    # --- Trajectory ---
    trajectory = None
    if row.trajectory_json:
        trajectory = row.trajectory_json.get("trajectory")

    # --- Budget ---
    total_lifetime_cost_a: float | None = None
    total_lifetime_cost_b: float | None = None
    potential_savings: float | None = None
    if row.budget_json:
        try:
            budget = WholePersonBudget(**row.budget_json)
            for h in budget.horizons:
                if h.label == "lifetime":
                    total_lifetime_cost_a = h.risk_profile.p50_total_cost
                    # Path B from scenarios if available
                    if h.scenarios:
                        best_scenario = min(
                            h.scenarios,
                            key=lambda s: s.expected_total_cost_under_scenario,
                        )
                        total_lifetime_cost_b = (
                            best_scenario.expected_total_cost_under_scenario
                        )
                        potential_savings = best_scenario.expected_savings_vs_baseline
                    break
        except Exception:
            logger.debug("Could not parse stored budget for dashboard")

    # --- Cascade alerts ---
    alert_stmt = (
        select(CascadeAlertTable)
        .where(CascadeAlertTable.person_uid == uid)
    )
    alert_result = await session.execute(alert_stmt)
    alert_rows = alert_result.scalars().all()
    active_alerts = len(alert_rows)

    # Collect recommended interventions across all alerts
    top_interventions: list[str] = []
    for ar in alert_rows:
        for iv in (ar.recommended_interventions_json or []):
            if iv not in top_interventions:
                top_interventions.append(iv)
                if len(top_interventions) >= 5:
                    break
        if len(top_interventions) >= 5:
            break

    # If we got path-A from alerts but not from budget scenarios
    if total_lifetime_cost_a is None and alert_rows:
        total_lifetime_cost_a = sum(
            a.path_a_projected_cost or 0 for a in alert_rows
        )
        total_lifetime_cost_b = sum(
            a.path_b_projected_cost or 0 for a in alert_rows
        )
        potential_savings = (total_lifetime_cost_a or 0) - (
            total_lifetime_cost_b or 0
        )

    # --- Simulation ---
    dome_roi: float | None = None
    sim_stmt = (
        select(SimulationResultTable)
        .where(SimulationResultTable.person_uid == uid)
        .order_by(SimulationResultTable.created_at.desc())
        .limit(1)
    )
    sim_result = await session.execute(sim_stmt)
    sim_row = sim_result.scalar_one_or_none()
    if sim_row:
        dome_roi = sim_row.dome_roi
        # Override cost projections from simulation if available
        if total_lifetime_cost_a is None and sim_row.path_a_median:
            total_lifetime_cost_a = sim_row.path_a_median
        if total_lifetime_cost_b is None and sim_row.path_b_median:
            total_lifetime_cost_b = sim_row.path_b_median
        if potential_savings is None and sim_row.path_a_median and sim_row.path_b_median:
            potential_savings = sim_row.path_a_median - sim_row.path_b_median

    # --- Benefits cliff detection (lightweight check) ---
    benefits_cliff_detected = False
    if row.budget_key_json:
        try:
            bk = PersonBudgetKey(**row.budget_key_json)
            income = bk.current_annual_income or 0
            # Simple heuristic: cliff risk near Medicaid/SNAP thresholds
            fpl_1person = 15_060  # approximate 2024 FPL for 1-person household
            fpl_household = fpl_1person + 5_380 * max(0, bk.household_size - 1)
            medicaid_threshold = fpl_household * 1.38
            snap_threshold = fpl_household * 1.30
            if income and (
                abs(income - medicaid_threshold) / medicaid_threshold < 0.10
                or abs(income - snap_threshold) / snap_threshold < 0.10
            ):
                benefits_cliff_detected = True
        except Exception:
            pass

    dashboard = DashboardData(
        person_uid=uid,
        name_hash=name_hash,
        age=age,
        trajectory=trajectory,
        active_cascade_alerts=active_alerts,
        total_lifetime_cost_path_a=total_lifetime_cost_a,
        total_lifetime_cost_path_b=total_lifetime_cost_b,
        potential_savings=potential_savings,
        dome_roi=dome_roi,
        top_interventions=top_interventions,
        benefits_cliff_detected=benefits_cliff_detected,
    )

    return dashboard


@router.get(
    "/{uid}/benefits-cliff",
    summary="Benefits cliff analysis",
    response_model=list[BenefitsCliffPoint],
)
async def benefits_cliff_analysis(
    uid: str,
    session: AsyncSession = Depends(get_session),
) -> list[BenefitsCliffPoint]:
    """Compute benefits-cliff analysis for person *uid*.

    Loads the person's budget key and dynamic state, then invokes
    ``BenefitsCliffCalculator.analyze()`` to compute the marginal
    effective tax rate curve across income levels.

    Returns a list of ``BenefitsCliffPoint`` objects showing how
    net resources change as income increases.
    """
    row = await _load_person_row(uid, session)

    if not row.budget_key_json:
        raise HTTPException(
            status_code=400,
            detail="Person has no budget key data for cliff analysis",
        )

    budget_key = PersonBudgetKey(**row.budget_key_json)
    dynamic_state = DynamicState(**(row.dynamic_state_json or {}))

    try:
        from dome.engines.benefits_cliff import BenefitsCliffCalculator

        calculator = BenefitsCliffCalculator()
        cliff_points = calculator.analyze(
            person_uid=uid,
            budget_key=budget_key,
            dynamic_state=dynamic_state,
        )
    except (ImportError, AttributeError) as exc:
        logger.warning(
            "BenefitsCliffCalculator unavailable (%s), generating fallback", exc
        )
        cliff_points = _fallback_benefits_cliff(budget_key)
    except Exception as exc:
        logger.exception("BenefitsCliffCalculator.analyze() failed")
        raise HTTPException(
            status_code=500, detail=f"Benefits cliff analysis failed: {exc}"
        ) from exc

    # Normalize output
    results: list[BenefitsCliffPoint] = []
    for pt in cliff_points:
        if isinstance(pt, BenefitsCliffPoint):
            results.append(pt)
        elif hasattr(pt, "model_dump"):
            results.append(BenefitsCliffPoint(**pt.model_dump()))
        elif isinstance(pt, dict):
            results.append(BenefitsCliffPoint(**pt))

    logger.info("Benefits cliff analysis completed for person %s (%d points)", uid, len(results))
    return results


# ---------------------------------------------------------------------------
# Fallback benefits cliff calculation
# ---------------------------------------------------------------------------


def _fallback_benefits_cliff(budget_key: PersonBudgetKey) -> list[dict]:
    """Generate a heuristic benefits-cliff curve.

    Models the major cliff-inducing programs (Medicaid, SNAP, housing
    assistance, EITC) and computes effective marginal tax rates across
    a range of income levels.
    """
    household_size = budget_key.household_size
    fpl_1person = 15_060
    fpl_household = fpl_1person + 5_380 * max(0, household_size - 1)

    # Program thresholds as % of FPL
    programs = {
        "medicaid": {"threshold_pct": 1.38, "value": 8_000},
        "snap": {"threshold_pct": 1.30, "value": 3_600},
        "housing_assistance": {"threshold_pct": 0.50, "value": 12_000},
        "eitc": {"threshold_pct": 2.50, "value": 3_600},
        "chip": {"threshold_pct": 2.00, "value": 4_000},
        "marketplace_subsidy": {"threshold_pct": 4.00, "value": 6_000},
    }

    # Generate curve from $0 to 4x FPL in steps
    step = max(1_000, fpl_household // 20)
    max_income = int(fpl_household * 4.5)
    points: list[dict] = []

    prev_net = 0.0
    for income in range(0, max_income + step, step):
        total_benefits = 0.0
        programs_lost: list[str] = []

        for prog_name, prog_info in programs.items():
            threshold = fpl_household * prog_info["threshold_pct"]
            if income <= threshold:
                total_benefits += prog_info["value"]
            else:
                programs_lost.append(prog_name)

        net_resources = income + total_benefits
        if prev_net > 0:
            marginal_income_change = step
            marginal_resource_change = net_resources - prev_net
            emtr = 1.0 - (marginal_resource_change / marginal_income_change)
        else:
            emtr = 0.0

        is_cliff = emtr > 0.80

        points.append(
            {
                "income_level": float(income),
                "total_benefits_value": total_benefits,
                "net_resources": net_resources,
                "effective_marginal_tax_rate": round(max(0, min(emtr, 2.0)), 4),
                "programs_lost": programs_lost,
                "is_cliff": is_cliff,
            }
        )
        prev_net = net_resources

    return points
