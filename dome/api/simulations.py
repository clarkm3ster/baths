"""Simulation router for THE DOME API.

Provides endpoints to run Path-A vs Path-B Monte Carlo (or deterministic)
simulations for a person and to retrieve stored simulation results.
Simulation delegates to ``LifeSimulator`` (aliased from
``dome.engines.simulator``).
"""

from __future__ import annotations

import logging
import random
from datetime import datetime, timezone
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from dome.db.database import get_session
from dome.db.tables import (
    CascadeAlertTable,
    InterventionPlanTable,
    PersonTable,
    SimulationResultTable,
)
from dome.models.budget_key import PersonBudgetKey
from dome.models.dynamic_state import DynamicState
from dome.schemas.intervention_schemas import SimulationRequest, SimulationSummary

logger = logging.getLogger("dome.api.simulations")

router = APIRouter(prefix="/persons", tags=["simulations"])


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


@router.post(
    "/{uid}/simulate",
    summary="Run Path A vs Path B simulation",
    response_model=SimulationSummary,
)
async def run_simulation(
    uid: str,
    req: SimulationRequest,
    session: AsyncSession = Depends(get_session),
) -> SimulationSummary:
    """Run a Monte Carlo simulation for person *uid*.

    Loads the person's state, budget key, cascade alerts, and
    intervention plans, then invokes ``LifeSimulator.simulate()`` to
    project costs under the do-nothing path (Path A) and the
    intervention path (Path B).

    Results are persisted to ``SimulationResultTable`` and a
    ``SimulationSummary`` is returned.
    """
    row = await _load_person_row(uid, session)

    # Gather context for the simulation
    dynamic_state = DynamicState(**(row.dynamic_state_json or {}))
    budget_key = PersonBudgetKey(**(row.budget_key_json or {})) if row.budget_key_json else None
    budget = row.budget_json

    # Load latest cascade alerts
    alert_stmt = (
        select(CascadeAlertTable)
        .where(CascadeAlertTable.person_uid == uid)
        .order_by(CascadeAlertTable.created_at.desc())
    )
    alert_result = await session.execute(alert_stmt)
    alert_rows = alert_result.scalars().all()

    # Load intervention plans
    plan_stmt = (
        select(InterventionPlanTable)
        .where(InterventionPlanTable.person_uid == uid)
        .order_by(InterventionPlanTable.created_at.desc())
    )
    plan_result = await session.execute(plan_stmt)
    plan_rows = plan_result.scalars().all()

    try:
        from dome.engines.simulator import LifeSimulator

        simulator = LifeSimulator()
        sim_result = simulator.simulate(
            person_uid=uid,
            dynamic_state=dynamic_state,
            budget_key=budget_key,
            budget=budget,
            cascade_alerts=[
                {
                    "alert_id": a.alert_id,
                    "cascade_id": a.cascade_id,
                    "path_a_projected_cost": a.path_a_projected_cost,
                    "path_b_projected_cost": a.path_b_projected_cost,
                }
                for a in alert_rows
            ],
            intervention_plans=[
                {
                    "plan_id": p.plan_id,
                    "total_cost": p.total_cost,
                    "expected_savings": p.expected_savings,
                    "interventions": p.interventions_json,
                }
                for p in plan_rows
            ],
            iterations=req.iterations,
            projection_years=req.projection_years,
            intervention_ids=req.intervention_ids,
        )
    except (ImportError, AttributeError) as exc:
        logger.warning(
            "LifeSimulator unavailable (%s), generating fallback simulation", exc
        )
        sim_result = _fallback_simulation(
            uid, dynamic_state, budget_key, alert_rows, plan_rows, req
        )
    except Exception as exc:
        logger.exception("LifeSimulator.simulate() failed")
        raise HTTPException(
            status_code=500, detail=f"Simulation failed: {exc}"
        ) from exc

    # Normalize result
    if hasattr(sim_result, "model_dump"):
        sr = sim_result.model_dump(mode="json")
    elif isinstance(sim_result, dict):
        sr = sim_result
    else:
        sr = dict(sim_result)

    # Build summary
    summary = SimulationSummary(
        path_a_median_cost=sr.get("path_a_median_cost", 0),
        path_a_p90_cost=sr.get("path_a_p90_cost", 0),
        path_b_median_cost=sr.get("path_b_median_cost", 0),
        path_b_p90_cost=sr.get("path_b_p90_cost", 0),
        dome_intervention_cost=sr.get("dome_intervention_cost", 0),
        net_savings=sr.get("net_savings", 0),
        dome_roi=sr.get("dome_roi", 0),
        iterations_run=sr.get("iterations_run", req.iterations),
    )

    # Persist to DB
    sim_row = SimulationResultTable(
        person_uid=uid,
        simulation_type="monte_carlo",
        path_a_median=summary.path_a_median_cost,
        path_b_median=summary.path_b_median_cost,
        dome_cost=summary.dome_intervention_cost,
        dome_roi=summary.dome_roi,
        results_json=sr,
    )
    session.add(sim_row)
    await session.flush()

    logger.info("Simulation completed for person %s", uid)
    return summary


@router.get("/{uid}/simulation-results", summary="Get simulation results")
async def get_simulation_results(
    uid: str,
    session: AsyncSession = Depends(get_session),
) -> dict:
    """Retrieve the latest simulation results for person *uid*.

    Returns the most recent ``SimulationResultTable`` row as a
    dictionary, including the full results JSON blob.
    """
    await _load_person_row(uid, session)

    stmt = (
        select(SimulationResultTable)
        .where(SimulationResultTable.person_uid == uid)
        .order_by(SimulationResultTable.created_at.desc())
        .limit(1)
    )
    result = await session.execute(stmt)
    row = result.scalar_one_or_none()

    if row is None:
        raise HTTPException(
            status_code=404,
            detail=f"No simulation results found for person {uid!r}",
        )

    return {
        "person_uid": row.person_uid,
        "simulation_type": row.simulation_type,
        "path_a_median": row.path_a_median,
        "path_b_median": row.path_b_median,
        "dome_cost": row.dome_cost,
        "dome_roi": row.dome_roi,
        "results": row.results_json or {},
        "created_at": row.created_at.isoformat() if row.created_at else None,
    }


# ---------------------------------------------------------------------------
# Fallback simulation
# ---------------------------------------------------------------------------


def _fallback_simulation(
    uid: str,
    dynamic_state: DynamicState,
    budget_key: PersonBudgetKey | None,
    alert_rows: list,
    plan_rows: list,
    req: SimulationRequest,
) -> dict:
    """Generate a deterministic fallback simulation when LifeSimulator is unavailable.

    Uses cascade alert projections and intervention plan costs to
    estimate path-A vs path-B outcomes with simple stochastic noise.
    """
    # Aggregate path-A and path-B from cascade alerts
    total_path_a = sum(a.path_a_projected_cost or 0 for a in alert_rows)
    total_path_b = sum(a.path_b_projected_cost or 0 for a in alert_rows)

    # If no alerts, estimate from budget key
    if total_path_a == 0 and budget_key:
        annual_income = budget_key.current_annual_income or 30_000
        # Rough heuristic: lifetime public cost ~ 2x income * projection years
        total_path_a = annual_income * 2 * req.projection_years
        total_path_b = total_path_a * 0.65

    # Intervention costs from plans
    total_intervention_cost = sum(p.total_cost or 0 for p in plan_rows)
    if total_intervention_cost == 0:
        total_intervention_cost = total_path_a * 0.05  # 5% of path-A as default

    # Simple Monte Carlo with noise
    random.seed(42)  # deterministic for reproducibility
    path_a_samples = []
    path_b_samples = []
    for _ in range(req.iterations):
        noise_a = random.gauss(1.0, 0.15)
        noise_b = random.gauss(1.0, 0.10)
        path_a_samples.append(total_path_a * noise_a)
        path_b_samples.append(total_path_b * noise_b)

    path_a_samples.sort()
    path_b_samples.sort()

    p50_idx = len(path_a_samples) // 2
    p90_idx = int(len(path_a_samples) * 0.90)

    path_a_median = path_a_samples[p50_idx]
    path_a_p90 = path_a_samples[p90_idx]
    path_b_median = path_b_samples[p50_idx]
    path_b_p90 = path_b_samples[p90_idx]

    net_savings = path_a_median - path_b_median - total_intervention_cost
    dome_roi = net_savings / total_intervention_cost if total_intervention_cost > 0 else 0

    return {
        "path_a_median_cost": round(path_a_median, 2),
        "path_a_p90_cost": round(path_a_p90, 2),
        "path_b_median_cost": round(path_b_median, 2),
        "path_b_p90_cost": round(path_b_p90, 2),
        "dome_intervention_cost": round(total_intervention_cost, 2),
        "net_savings": round(net_savings, 2),
        "dome_roi": round(dome_roi, 2),
        "iterations_run": req.iterations,
        "projection_years": req.projection_years,
        "note": "Fallback simulation — LifeSimulator engine not available",
    }
