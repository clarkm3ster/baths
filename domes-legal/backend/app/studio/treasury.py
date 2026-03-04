"""Dome Treasury -- micro financial infrastructure.

Provides:
- Treasury account management with restricted-use categories
- Real-time disbursement via FedNow / RTP / ACH / check
- Benefits cliff guard analysis (effective marginal tax rate simulation)
- Income bridge suggestions for safe transitions off public assistance

All functions are stdlib-only and operate on Pydantic models.
"""
from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------

class TreasuryAccount(BaseModel):
    """A restricted-use micro treasury account for a person."""
    account_id: str = Field(default_factory=lambda: f"acct-{uuid.uuid4().hex[:12]}")
    person_id: str
    balance: float = 0.0
    restricted_uses: list[str] = Field(
        default_factory=list,
        description="Allowed spending categories, e.g. 'housing', 'food', 'medical', 'transit'",
    )
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Disbursement(BaseModel):
    """A single disbursement from a treasury account."""
    disbursement_id: str = Field(default_factory=lambda: f"disb-{uuid.uuid4().hex[:12]}")
    account_id: str
    amount: float
    category: str
    method: Literal["fednow", "rtp", "ach", "check"] = "ach"
    status: Literal["pending", "completed", "failed", "clawed_back"] = "pending"
    initiated_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: datetime | None = None


class CliffGuard(BaseModel):
    """Benefits cliff analysis for a person.

    Simulates income increases to find where effective marginal tax rates
    spike above 50%, indicating a benefits cliff -- the income zone where
    earning more money actually leaves you worse off.
    """
    person_id: str
    current_benefits: dict[str, float] = Field(
        default_factory=dict,
        description="Map of program name to annual benefit amount, e.g. {'snap': 3600, 'medicaid': 8000}",
    )
    earned_income: float = 0.0
    effective_marginal_tax_rate: float = 0.0
    cliff_zones: list[float] = Field(
        default_factory=list,
        description="Income thresholds where benefits drop sharply",
    )
    max_safe_income: float = 0.0


# ---------------------------------------------------------------------------
# Benefit phase-out schedules
# ---------------------------------------------------------------------------

# Simplified federal phase-out rules: (program, income_floor, income_ceiling, benefit_at_floor)
# Benefits reduce linearly from floor to ceiling, then drop to zero.
_DEFAULT_PHASE_OUTS: dict[str, tuple[float, float]] = {
    "snap":        (18_000, 36_000),
    "medicaid":    (20_000, 40_000),
    "tanf":        (10_000, 24_000),
    "housing":     (15_000, 45_000),
    "ccdf":        (20_000, 50_000),
    "ssi":         (10_000, 28_000),
    "liheap":      (15_000, 30_000),
    "wic":         (22_000, 48_000),
    "eitc":        (15_000, 55_000),
}


def _benefit_at_income(
    program: str,
    base_amount: float,
    income: float,
) -> float:
    """Calculate remaining benefit for a program at a given income level.

    Uses linear phase-out between floor and ceiling thresholds.
    Returns zero if income exceeds the ceiling.
    """
    floor, ceiling = _DEFAULT_PHASE_OUTS.get(program, (15_000, 40_000))

    if income <= floor:
        return base_amount
    if income >= ceiling:
        return 0.0

    # Linear reduction
    fraction_remaining = (ceiling - income) / (ceiling - floor)
    return round(base_amount * fraction_remaining, 2)


# ---------------------------------------------------------------------------
# Account management
# ---------------------------------------------------------------------------

def create_account(
    person_id: str,
    initial_balance: float = 0.0,
    restricted_uses: list[str] | None = None,
) -> TreasuryAccount:
    """Create a new treasury account for a person.

    Args:
        person_id: Unique identifier for the person.
        initial_balance: Starting balance in USD.
        restricted_uses: Allowed spending categories. If empty, account is
            unrestricted.

    Returns:
        A new TreasuryAccount instance.
    """
    return TreasuryAccount(
        person_id=person_id,
        balance=initial_balance,
        restricted_uses=restricted_uses or [],
    )


# ---------------------------------------------------------------------------
# Disbursement
# ---------------------------------------------------------------------------

def disburse(
    account_id: str,
    amount: float,
    category: str,
    method: Literal["fednow", "rtp", "ach", "check"] = "ach",
    *,
    account: TreasuryAccount | None = None,
) -> Disbursement:
    """Create a disbursement from a treasury account.

    Validates:
    - Amount is positive.
    - Category is among the account's restricted_uses (if restrictions exist).
    - Sufficient balance exists in the account.

    When *account* is provided, balance is checked and decremented in place.
    When *account* is None, only the Disbursement record is created with
    status 'pending' (caller is responsible for settlement).

    Args:
        account_id: The treasury account to disburse from.
        amount: Dollar amount to disburse.
        category: Spending category (e.g. 'housing', 'food').
        method: Payment rail -- 'fednow', 'rtp', 'ach', or 'check'.
        account: Optional TreasuryAccount for balance/restriction validation.

    Returns:
        A Disbursement record.

    Raises:
        ValueError: If amount is non-positive, category is restricted, or
            balance is insufficient.
    """
    if amount <= 0:
        raise ValueError(f"Disbursement amount must be positive, got {amount}")

    if account is not None:
        # Validate restricted uses
        if account.restricted_uses and category not in account.restricted_uses:
            raise ValueError(
                f"Category '{category}' is not in account restricted uses: "
                f"{account.restricted_uses}"
            )

        # Validate sufficient balance
        if account.balance < amount:
            raise ValueError(
                f"Insufficient balance: account has ${account.balance:.2f}, "
                f"disbursement requires ${amount:.2f}"
            )

        # Debit the account
        account.balance = round(account.balance - amount, 2)

    disbursement = Disbursement(
        account_id=account_id,
        amount=amount,
        category=category,
        method=method,
        status="completed" if account is not None else "pending",
        completed_at=datetime.utcnow() if account is not None else None,
    )

    return disbursement


# ---------------------------------------------------------------------------
# Cliff guard analysis
# ---------------------------------------------------------------------------

def calculate_cliff_guard(
    benefits: dict[str, float],
    earned_income: float,
    income_step: float = 500.0,
    person_id: str = "",
) -> CliffGuard:
    """Simulate income increases to detect benefits cliffs.

    Walks income upward in *income_step* increments. At each step,
    recalculates total benefits and finds the effective marginal tax rate
    (EMTR). An EMTR above 50% means the person loses more in benefits
    than they gain in wages -- a cliff zone.

    Args:
        benefits: Map of program name to current annual benefit amount.
        earned_income: Current annual earned income.
        income_step: Dollar increment per simulation step (default $500).
        person_id: Optional person identifier.

    Returns:
        CliffGuard with cliff zones, EMTR, and max safe income identified.
    """
    if income_step <= 0:
        raise ValueError("income_step must be positive")

    # Calculate total benefits at current income
    def _total_benefits(income: float) -> float:
        return sum(
            _benefit_at_income(program, amount, income)
            for program, amount in benefits.items()
        )

    current_total = earned_income + _total_benefits(earned_income)

    cliff_zones: list[float] = []
    max_safe_income = earned_income
    worst_emtr = 0.0

    # Simulate up to 3x current income or $150k, whichever is higher
    ceiling = max(earned_income * 3, 150_000)
    income = earned_income

    while income < ceiling:
        next_income = income + income_step
        current_net = income + _total_benefits(income)
        next_net = next_income + _total_benefits(next_income)

        # Effective marginal tax rate: how much of the $step increase is lost
        net_gain = next_net - current_net
        emtr = 1.0 - (net_gain / income_step) if income_step > 0 else 0.0

        if emtr > worst_emtr:
            worst_emtr = emtr

        if emtr > 0.50:
            cliff_zones.append(next_income)
        else:
            # Still safe -- update max_safe_income
            if next_income > max_safe_income and emtr <= 0.50:
                max_safe_income = next_income

        income = next_income

    return CliffGuard(
        person_id=person_id,
        current_benefits=benefits,
        earned_income=earned_income,
        effective_marginal_tax_rate=round(worst_emtr, 4),
        cliff_zones=cliff_zones,
        max_safe_income=max_safe_income,
    )


# ---------------------------------------------------------------------------
# Income bridge suggestion
# ---------------------------------------------------------------------------

def suggest_income_bridge(
    cliff_guard: CliffGuard,
    target_income: float,
) -> dict[str, Any]:
    """Suggest a bridging strategy to move a person past benefits cliffs.

    If the target income falls within or beyond cliff zones, this function
    calculates:
    - bridge_amount: supplemental dollars needed to keep the person whole
      while income transitions past the cliff.
    - phase_out_schedule: step-by-step benefit reduction as income rises.
    - net_benefit: whether the target income leaves the person better off.

    Args:
        cliff_guard: A previously calculated CliffGuard analysis.
        target_income: Desired annual earned income.

    Returns:
        Dict with bridge_amount, phase_out_schedule, and net_benefit.
    """
    benefits = cliff_guard.current_benefits
    current_income = cliff_guard.earned_income

    # Calculate total compensation at current and target incomes
    def _total_at(income: float) -> float:
        total_benefits = sum(
            _benefit_at_income(prog, amt, income)
            for prog, amt in benefits.items()
        )
        return income + total_benefits

    current_total = _total_at(current_income)
    target_total = _total_at(target_income)

    # Bridge amount: if target total < current total, the person needs
    # supplemental funds to avoid net loss during transition
    bridge_amount = max(current_total - target_total, 0.0)

    # Build phase-out schedule: show benefit reduction at each $2,500 step
    phase_out_schedule: list[dict[str, Any]] = []
    step_size = 2_500.0
    income = current_income

    while income <= target_income + step_size:
        step_benefits: dict[str, float] = {}
        for program, amount in benefits.items():
            step_benefits[program] = _benefit_at_income(program, amount, income)

        total_benefits = sum(step_benefits.values())
        phase_out_schedule.append({
            "earned_income": round(income, 2),
            "total_benefits": round(total_benefits, 2),
            "total_compensation": round(income + total_benefits, 2),
            "benefits_by_program": step_benefits,
        })

        income += step_size
        if income > target_income and income - step_size < target_income:
            income = target_income  # include exact target

    # Net benefit analysis
    net_gain = target_total - current_total

    return {
        "bridge_amount": round(bridge_amount, 2),
        "phase_out_schedule": phase_out_schedule,
        "net_benefit": {
            "current_total_compensation": round(current_total, 2),
            "target_total_compensation": round(target_total, 2),
            "net_annual_gain": round(net_gain, 2),
            "person_is_better_off": net_gain > 0,
            "bridge_needed": bridge_amount > 0,
            "bridge_amount": round(bridge_amount, 2),
        },
    }
