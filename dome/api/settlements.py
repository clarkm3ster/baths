"""Settlement matrix router for THE DOME API.

Provides endpoints to compute settlement matrices (cross-payer cost and
savings redistribution) and to retrieve stored matrices.  Settlement
computation delegates to ``WrongPocketAnalyzer`` which determines
inter-payer transfers needed to align incentives.
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from dome.db.database import get_session
from dome.db.tables import PersonTable, SettlementMatrixTable
from dome.models.budget_output import WholePersonBudget
from dome.models.settlement_matrix import (
    PayerSettlementRow,
    PayerTransfer,
    SettlementMatrix,
)
from dome.schemas.budget_schemas import SettlementComputeRequest

logger = logging.getLogger("dome.api.settlements")

router = APIRouter(prefix="/persons", tags=["settlements"])


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


@router.post("/{uid}/settlement", summary="Compute settlement matrix")
async def compute_settlement(
    uid: str,
    req: SettlementComputeRequest,
    session: AsyncSession = Depends(get_session),
) -> dict:
    """Compute a settlement matrix for person *uid* and scenario *req.scenario_id*.

    Loads the person's stored budget and the specified scenario, then
    uses ``WrongPocketAnalyzer`` to compute the inter-payer settlement
    matrix that redistributes costs and savings equitably.

    The resulting matrix is persisted to ``SettlementMatrixTable`` and
    returned as a ``SettlementMatrix`` dict.
    """
    row = await _load_person_row(uid, session)

    if not row.budget_json:
        raise HTTPException(
            status_code=400,
            detail="Compute the budget first before computing settlement matrix",
        )

    budget = WholePersonBudget(**row.budget_json)

    # Find the matching horizon
    target_horizon = None
    for h in budget.horizons:
        if h.label == req.horizon_label:
            target_horizon = h
            break
    if target_horizon is None and budget.horizons:
        target_horizon = budget.horizons[-1]

    # Find the matching scenario within the horizon
    scenario = None
    if target_horizon and target_horizon.scenarios:
        for s in target_horizon.scenarios:
            if s.scenario_id == req.scenario_id:
                scenario = s
                break

    try:
        from dome.engines.wrong_pocket_analyzer import WrongPocketAnalyzer

        analyzer = WrongPocketAnalyzer()
        matrix = analyzer.compute_settlement(
            person_uid=uid,
            budget=budget,
            scenario_id=req.scenario_id,
            horizon_label=req.horizon_label,
            risk_share_pct=req.risk_share_pct,
            cap_multiple=req.cap_multiple,
        )
    except (ImportError, AttributeError) as exc:
        logger.warning(
            "WrongPocketAnalyzer unavailable (%s), generating fallback settlement",
            exc,
        )
        matrix = _fallback_settlement(
            uid, budget, target_horizon, scenario, req
        )
    except Exception as exc:
        logger.exception("Settlement computation failed")
        raise HTTPException(
            status_code=500, detail=f"Settlement computation failed: {exc}"
        ) from exc

    # Normalize
    if hasattr(matrix, "model_dump"):
        matrix_dict = matrix.model_dump(mode="json")
    elif isinstance(matrix, dict):
        matrix_dict = matrix
    else:
        matrix_dict = dict(matrix)

    # Persist to DB
    settlement_row = SettlementMatrixTable(
        person_uid=uid,
        scenario_id=req.scenario_id,
        horizon_label=req.horizon_label,
        payers_json=matrix_dict.get("payers", []),
        transfers_json=matrix_dict.get("transfers", []),
        assumptions_json=matrix_dict.get("assumptions", {}),
        generated_at=datetime.now(tz=timezone.utc),
        model_version=matrix_dict.get("model_version", "0.1.0-fallback"),
    )
    session.add(settlement_row)
    await session.flush()

    logger.info(
        "Computed settlement matrix for person %s, scenario %s",
        uid,
        req.scenario_id,
    )
    return matrix_dict


@router.get(
    "/{uid}/settlement/{scenario_id}",
    summary="Get stored settlement matrix",
)
async def get_settlement(
    uid: str,
    scenario_id: str,
    session: AsyncSession = Depends(get_session),
) -> dict:
    """Retrieve a stored settlement matrix for person *uid* and *scenario_id*.

    Returns the most recently computed ``SettlementMatrixTable`` row
    matching the person and scenario as a dictionary.
    """
    await _load_person_row(uid, session)

    stmt = (
        select(SettlementMatrixTable)
        .where(
            SettlementMatrixTable.person_uid == uid,
            SettlementMatrixTable.scenario_id == scenario_id,
        )
        .order_by(SettlementMatrixTable.created_at.desc())
        .limit(1)
    )
    result = await session.execute(stmt)
    row = result.scalar_one_or_none()

    if row is None:
        raise HTTPException(
            status_code=404,
            detail=(
                f"No settlement matrix found for person {uid!r} "
                f"and scenario {scenario_id!r}"
            ),
        )

    return {
        "person_uid": row.person_uid,
        "scenario_id": row.scenario_id,
        "horizon_label": row.horizon_label,
        "payers": row.payers_json or [],
        "transfers": row.transfers_json or [],
        "assumptions": row.assumptions_json or {},
        "generated_at": row.generated_at.isoformat() if row.generated_at else None,
        "model_version": row.model_version,
        "created_at": row.created_at.isoformat() if row.created_at else None,
    }


# ---------------------------------------------------------------------------
# Fallback settlement matrix generator
# ---------------------------------------------------------------------------


def _fallback_settlement(
    uid: str,
    budget: WholePersonBudget,
    target_horizon,
    scenario,
    req: SettlementComputeRequest,
) -> SettlementMatrix:
    """Generate a heuristic settlement matrix when WrongPocketAnalyzer is unavailable.

    Distributes costs and savings across the standard five payer levels
    (federal, state, local, health_system, nonprofit) based on the
    budget's payer view.  Computes transfers needed so that payers who
    invest upfront receive fair compensation from payers who save.
    """
    now = datetime.now(tz=timezone.utc)

    # Extract payer spending from the budget
    if target_horizon:
        pv = target_horizon.payer_view
        total_spend = (
            pv.federal_expected_spend
            + pv.state_expected_spend
            + pv.local_expected_spend
            + pv.healthcare_delivery_expected_spend
            + pv.nonprofit_expected_spend
        )
        payer_shares = {
            "federal": pv.federal_expected_spend / total_spend if total_spend > 0 else 0.45,
            "state": pv.state_expected_spend / total_spend if total_spend > 0 else 0.25,
            "local": pv.local_expected_spend / total_spend if total_spend > 0 else 0.15,
            "health_system": pv.healthcare_delivery_expected_spend / total_spend if total_spend > 0 else 0.10,
            "nonprofit": pv.nonprofit_expected_spend / total_spend if total_spend > 0 else 0.05,
        }
    else:
        total_spend = 100_000
        payer_shares = {
            "federal": 0.45,
            "state": 0.25,
            "local": 0.15,
            "health_system": 0.10,
            "nonprofit": 0.05,
        }

    # Estimate total savings from scenario
    if scenario:
        total_savings = scenario.expected_savings_vs_baseline
        intervention_cost = scenario.incremental_cost_of_scenario
    else:
        total_savings = total_spend * 0.20
        intervention_cost = total_savings * 0.25

    # Build payer settlement rows
    # Assume local/nonprofit invest, federal/state save
    payer_names = {
        "federal": "Federal Government (CMS, HHS, IRS)",
        "state": "State Government",
        "local": "County / Local Government",
        "health_system": "Healthcare Delivery System",
        "nonprofit": "Nonprofit / Community Organizations",
    }

    # Investment distribution: local and nonprofit invest more upfront
    investment_shares = {
        "federal": 0.10,
        "state": 0.20,
        "local": 0.35,
        "health_system": 0.15,
        "nonprofit": 0.20,
    }

    # Savings distribution follows spending shares
    savings_shares = payer_shares

    payers: list[PayerSettlementRow] = []
    for payer_level, payer_name in payer_names.items():
        upfront = intervention_cost * investment_shares[payer_level]
        gross_savings = total_savings * savings_shares[payer_level]
        net_position = gross_savings - upfront

        payers.append(
            PayerSettlementRow(
                payer_id=f"{payer_level}_{uid[:8]}",
                payer_level=payer_level,
                payer_name=payer_name,
                upfront_investment=round(upfront, 2),
                expected_gross_savings=round(gross_savings, 2),
                net_position_after_settlement=round(net_position, 2),
            )
        )

    # Compute transfers: payers with positive net position pay
    # payers with negative net position, limited by risk_share and cap
    transfers: list[PayerTransfer] = []
    surplus_payers = [p for p in payers if p.net_position_after_settlement > 0]
    deficit_payers = [p for p in payers if p.net_position_after_settlement < 0]

    for deficit_p in deficit_payers:
        deficit_amount = abs(deficit_p.net_position_after_settlement)
        remaining_deficit = deficit_amount * req.risk_share_pct

        for surplus_p in surplus_payers:
            if remaining_deficit <= 0:
                break
            surplus_available = surplus_p.net_position_after_settlement * req.risk_share_pct
            cap = surplus_p.upfront_investment * req.cap_multiple
            transfer_amount = min(remaining_deficit, surplus_available, cap)

            if transfer_amount > 0:
                transfers.append(
                    PayerTransfer(
                        from_payer_id=surplus_p.payer_id,
                        to_payer_id=deficit_p.payer_id,
                        amount=round(transfer_amount, 2),
                        transfer_schedule="quarterly over 5 years",
                    )
                )
                remaining_deficit -= transfer_amount

    return SettlementMatrix(
        person_uid=uid,
        scenario_id=req.scenario_id,
        horizon_label=req.horizon_label,
        payers=payers,
        transfers=transfers,
        assumptions={
            "discount_rate": 0.03,
            "risk_share_pct": req.risk_share_pct,
            "cap_multiple": req.cap_multiple,
            "attribution_method": "proportional_to_spending",
            "note": "Fallback settlement — WrongPocketAnalyzer engine not available",
        },
        generated_at=now,
        model_version="0.1.0-fallback",
    )
