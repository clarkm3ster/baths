"""Capital Markets / Securitization — Prevention-Backed Securities.

Pools settlement contracts (verified health/social interventions) into
tradable bond instruments.  Each contract represents an intervention whose
expected savings are shared across payers (Medicaid, insurer, employer,
etc.).  Contracts are bundled into tranched bonds priced on weighted
success-rate expectations.

Provides:
- SettlementContract / PreventionBond / BondPricing models
- pool_contracts   — bundle contracts into a bond
- price_bond       — expected return, VaR, default probability
- stress_test      — scenario analysis (recession, moderate, baseline)
- calculate_coupon — coupon from verified savings * payout ratio
"""
from __future__ import annotations

import math
import uuid
from datetime import datetime
from typing import Any, Literal, Optional

from pydantic import BaseModel, Field


# ── Models ────────────────────────────────────────────────────────

class SettlementContract(BaseModel):
    """A single prevention-intervention contract backing a bond."""
    contract_id: str = Field(default_factory=lambda: f"sc-{uuid.uuid4().hex[:12]}")
    person_id: str
    intervention_type: str
    expected_savings: dict[str, float] = Field(
        default_factory=dict,
        description="Mapping of payer -> expected dollar savings, e.g. {'medicaid': 12000, 'employer': 4000}",
    )
    probability_of_success: float = Field(
        ge=0.0, le=1.0,
        description="Estimated probability (0-1) the intervention succeeds",
    )
    verification_method: str = ""
    term_years: int = 1
    status: Literal["active", "verified", "defaulted", "matured"] = "active"


class PreventionBond(BaseModel):
    """A tradable bond backed by a pool of settlement contracts."""
    bond_id: str = Field(default_factory=lambda: f"pb-{uuid.uuid4().hex[:12]}")
    name: str
    contracts: list[str] = Field(
        default_factory=list,
        description="List of contract_ids in this bond pool",
    )
    total_notional: float = 0.0
    coupon_rate: float = 0.0
    expected_yield: float = 0.0
    tranche: Literal["senior", "mezzanine", "equity"] = "mezzanine"
    vintage_year: int = Field(default_factory=lambda: datetime.utcnow().year)
    status: Literal["structuring", "offered", "active", "matured"] = "structuring"


class BondPricing(BaseModel):
    """Pricing output for a prevention bond."""
    bond_id: str
    expected_return: float
    var_95: float = Field(description="Value-at-Risk at 95th percentile")
    default_probability: float
    stress_test_results: dict[str, Any] = Field(default_factory=dict)
    discount_rate: float = 0.05


# ── Tranche multipliers ──────────────────────────────────────────

_TRANCHE_YIELD_MULT: dict[str, float] = {
    "senior":    0.6,   # lower yield, first to be paid
    "mezzanine": 1.0,   # base yield
    "equity":    1.5,   # highest yield, first-loss
}

_TRANCHE_RISK_MULT: dict[str, float] = {
    "senior":    0.4,
    "mezzanine": 1.0,
    "equity":    1.8,
}

PAYOUT_RATIO = 0.70  # fraction of verified savings paid as coupon


# ── Pool contracts into a bond ────────────────────────────────────

def pool_contracts(
    contracts: list[SettlementContract],
    bond_name: str,
    tranche: Literal["senior", "mezzanine", "equity"] = "mezzanine",
) -> PreventionBond:
    """Bundle settlement contracts into a PreventionBond.

    Calculates:
      - total_notional: sum of probability-weighted expected savings
      - expected_yield: weighted average yield adjusted for tranche
      - coupon_rate:    expected yield * payout ratio
    """
    if not contracts:
        return PreventionBond(
            name=bond_name,
            tranche=tranche,
        )

    total_notional = 0.0
    weighted_yield_sum = 0.0

    for c in contracts:
        contract_savings = sum(c.expected_savings.values())
        weighted_savings = contract_savings * c.probability_of_success
        total_notional += weighted_savings

        # Each contract contributes its success-rate as a yield component
        weighted_yield_sum += c.probability_of_success * weighted_savings

    # Weighted average success-rate (acts as base yield)
    base_yield = (
        weighted_yield_sum / total_notional if total_notional > 0 else 0.0
    )

    tranche_mult = _TRANCHE_YIELD_MULT.get(tranche, 1.0)
    expected_yield = base_yield * tranche_mult
    coupon_rate = expected_yield * PAYOUT_RATIO

    return PreventionBond(
        name=bond_name,
        contracts=[c.contract_id for c in contracts],
        total_notional=round(total_notional, 2),
        coupon_rate=round(coupon_rate, 6),
        expected_yield=round(expected_yield, 6),
        tranche=tranche,
    )


# ── Price a bond ──────────────────────────────────────────────────

def price_bond(
    bond: PreventionBond,
    contracts: list[SettlementContract],
    discount_rate: float = 0.05,
) -> BondPricing:
    """Price a prevention bond.

    - expected_return: discounted value of expected cash-flows minus notional
    - var_95: simple parametric Value-at-Risk (95% confidence)
    - default_probability: probability that *all* contracts fail
    """
    if not contracts:
        return BondPricing(
            bond_id=bond.bond_id,
            expected_return=0.0,
            var_95=0.0,
            default_probability=1.0,
            discount_rate=discount_rate,
        )

    # Collect contract-level metrics
    success_rates = [c.probability_of_success for c in contracts]
    savings = [sum(c.expected_savings.values()) for c in contracts]
    terms = [c.term_years for c in contracts]

    # Expected cash-flow per contract (probability * savings), discounted
    expected_cf = 0.0
    for p, s, t in zip(success_rates, savings, terms):
        # discount factor: 1 / (1 + r)^t
        df = 1.0 / ((1.0 + discount_rate) ** t)
        expected_cf += p * s * df

    expected_return = expected_cf - bond.total_notional

    # Simple parametric VaR at 95%
    # Variance of a Bernoulli pool: sum of p*(1-p)*savings^2
    variance = 0.0
    for p, s in zip(success_rates, savings):
        variance += p * (1.0 - p) * (s ** 2)
    std_dev = math.sqrt(variance) if variance > 0 else 0.0
    z_95 = 1.645  # one-tailed 95%
    risk_mult = _TRANCHE_RISK_MULT.get(bond.tranche, 1.0)
    var_95 = z_95 * std_dev * risk_mult

    # Default probability: probability all contracts fail
    # P(all fail) = product of (1 - p_i)
    default_prob = 1.0
    for p in success_rates:
        default_prob *= (1.0 - p)

    return BondPricing(
        bond_id=bond.bond_id,
        expected_return=round(expected_return, 2),
        var_95=round(var_95, 2),
        default_probability=round(default_prob, 8),
        discount_rate=discount_rate,
    )


# ── Stress test ───────────────────────────────────────────────────

_DEFAULT_SCENARIOS: dict[str, float] = {
    "recession": 0.30,   # success rates drop 30%
    "moderate":  0.15,   # success rates drop 15%
    "baseline":  0.00,   # no change
}


def _apply_haircut(
    contracts: list[SettlementContract],
    haircut: float,
) -> list[SettlementContract]:
    """Return copies of contracts with success rates reduced by haircut fraction."""
    stressed: list[SettlementContract] = []
    for c in contracts:
        new_p = max(c.probability_of_success * (1.0 - haircut), 0.0)
        stressed.append(c.model_copy(update={"probability_of_success": new_p}))
    return stressed


def stress_test(
    bond: PreventionBond,
    contracts: list[SettlementContract],
    scenarios: dict[str, float] | None = None,
) -> dict[str, Any]:
    """Run stress scenarios on a bond.

    Each scenario specifies a fractional drop in contract success rates.
    Returns a dict mapping scenario_name -> BondPricing dict.

    Default scenarios:
      - recession: success rates drop 30%
      - moderate:  success rates drop 15%
      - baseline:  no change
    """
    scenarios = scenarios or _DEFAULT_SCENARIOS
    results: dict[str, Any] = {}

    for name, haircut in scenarios.items():
        stressed_contracts = _apply_haircut(contracts, haircut)
        pricing = price_bond(bond, stressed_contracts)
        results[name] = pricing.model_dump()

    return results


# ── Coupon calculation ────────────────────────────────────────────

def calculate_coupon(
    bond: PreventionBond,
    contracts: list[SettlementContract],
) -> float:
    """Calculate coupon payment from verified contract savings.

    Only contracts with status == "verified" contribute.
    Coupon = total_verified_savings * PAYOUT_RATIO (70%).
    """
    verified_savings = 0.0
    contract_ids = set(bond.contracts)

    for c in contracts:
        if c.contract_id in contract_ids and c.status == "verified":
            verified_savings += sum(c.expected_savings.values())

    return round(verified_savings * PAYOUT_RATIO, 2)
