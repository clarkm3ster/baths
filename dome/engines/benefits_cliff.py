"""
Benefits Cliff Calculator Engine (Step 7)
============================================

Computes the effective marginal tax rate (EMTR) and net resources at each
income level from $0 to $100,000 in $1,000 increments for a given person
profile.  Identifies **benefits cliff points** where the EMTR exceeds 80%
or net resources actually decrease when income rises.

The calculator models eligibility and phase-out rules for 11 major programs:

1. Medicaid (138% FPL for expansion states)
2. SNAP (130% FPL gross, phase-out)
3. TANF (~50% FPL)
4. Housing assistance (~50% AMI)
5. SSI (income + SGA test)
6. CHIP (200-300% FPL)
7. ACA Marketplace premium subsidy (100-400% FPL, cliff at 400%)
8. EITC (phase-in / plateau / phase-out by filing status and children)
9. Child Tax Credit (phase-out at $200K single / $400K married)
10. CCDF childcare (varies, ~85% SMI)
11. WIOA (not income-tested, but included for completeness)

Usage::

    from dome.engines.benefits_cliff import BenefitsCliffCalculator
    calculator = BenefitsCliffCalculator()
    cliff_points = calculator.analyze(budget_key)
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any

from dome.models.budget_key import PersonBudgetKey


# ---------------------------------------------------------------------------
# Federal Poverty Level (2024)
# ---------------------------------------------------------------------------
_FPL_BASE: float = 15_060.0
_FPL_PER_PERSON: float = 5_380.0


def _fpl(household_size: int) -> float:
    """Compute 2024 FPL for the given household size (contiguous 48 states)."""
    if household_size <= 1:
        return _FPL_BASE
    return _FPL_BASE + _FPL_PER_PERSON * (household_size - 1)


# ---------------------------------------------------------------------------
# Data classes for output
# ---------------------------------------------------------------------------

@dataclass
class BenefitsCliffPoint:
    """A single point on the benefits cliff curve.

    Attributes
    ----------
    income : float
        Annual earned income at this point (USD).
    benefits : dict[str, float]
        Map of program name to annual benefit value at this income.
    total_benefits_value : float
        Sum of all benefit values (USD).
    net_resources : float
        income + total_benefits_value - estimated_taxes (after-tax + benefits).
    effective_marginal_tax_rate : float
        EMTR = 1 - (change_in_net_resources / change_in_income).
        Values > 1.0 mean the person loses more than $1 in benefits/taxes
        for every $1 earned.
    programs_lost : list[str]
        Programs whose benefits dropped to $0 at this income level
        compared to the previous level.
    is_cliff : bool
        True if EMTR > 0.80 or net_resources decreased from the
        previous income level.
    """

    income: float
    benefits: dict[str, float] = field(default_factory=dict)
    total_benefits_value: float = 0.0
    net_resources: float = 0.0
    effective_marginal_tax_rate: float = 0.0
    programs_lost: list[str] = field(default_factory=list)
    is_cliff: bool = False


# ---------------------------------------------------------------------------
# Individual program benefit calculators
# ---------------------------------------------------------------------------
# Each function takes (income, fpl, household_size, num_children, budget_key)
# and returns the estimated annual benefit value.


def _calc_medicaid(
    income: float,
    fpl: float,
    household_size: int,
    num_children: int,
    bk: PersonBudgetKey,
) -> float:
    """Medicaid: 138% FPL cutoff in expansion states.

    Non-expansion states have lower limits, but we model the expansion
    threshold as the default.  Benefit value is the average annual
    per-adult Medicaid cost.
    """
    threshold = fpl * 1.38
    if income <= threshold:
        # Benefit value varies: disabled get more, children get less
        if bk.disability_flag:
            return 22_000.0
        return 7_500.0
    return 0.0


def _calc_snap(
    income: float,
    fpl: float,
    household_size: int,
    num_children: int,
    bk: PersonBudgetKey,
) -> float:
    """SNAP: 130% FPL gross income test, benefit = max_allotment - 0.3 * net_income.

    Maximum monthly allotment (2024):
    - 1 person: $291, 2: $535, 3: $766, 4: $973, ...
    Simplified: we compute a benefit that phases out linearly.
    """
    gross_threshold = fpl * 1.30
    if income > gross_threshold:
        return 0.0

    # Max annual SNAP benefit by household size (approximate 2024)
    max_monthly = {1: 291, 2: 535, 3: 766, 4: 973, 5: 1155, 6: 1386}
    max_month = max_monthly.get(household_size, 291 + (household_size - 1) * 200)
    max_annual = max_month * 12

    # Net income = gross - standard deduction ($198/mo) - 20% earned income deduction
    monthly_income = income / 12
    standard_deduction = 198.0
    earned_income_deduction = monthly_income * 0.20
    net_monthly = max(0.0, monthly_income - standard_deduction - earned_income_deduction)

    benefit_monthly = max(0.0, max_month - 0.30 * net_monthly)
    return round(benefit_monthly * 12, 2)


def _calc_tanf(
    income: float,
    fpl: float,
    household_size: int,
    num_children: int,
    bk: PersonBudgetKey,
) -> float:
    """TANF: ~50% FPL cutoff, requires dependent children.

    Average monthly TANF benefit is ~$540 for a family.
    """
    if num_children == 0:
        return 0.0

    threshold = fpl * 0.50
    if income > threshold:
        return 0.0

    return 6_500.0


def _calc_housing_assistance(
    income: float,
    fpl: float,
    household_size: int,
    num_children: int,
    bk: PersonBudgetKey,
) -> float:
    """Housing assistance: ~50% Area Median Income.

    We approximate 50% AMI as ~$35,000 for a 1-person household, scaling
    with household size.  Benefit = fair market rent - 30% of income.
    """
    ami_50 = 35_000.0 + (household_size - 1) * 5_000.0
    if income > ami_50:
        return 0.0

    # Section 8: tenant pays 30% of adjusted income toward rent
    # Benefit = FMR - tenant_contribution
    fair_market_rent_annual = 14_400.0  # ~$1,200/mo national average
    tenant_contribution = income * 0.30
    benefit = max(0.0, fair_market_rent_annual - tenant_contribution)
    return round(benefit, 2)


def _calc_ssi(
    income: float,
    fpl: float,
    household_size: int,
    num_children: int,
    bk: PersonBudgetKey,
) -> float:
    """SSI: Federal benefit rate $943/month (2024), with income reduction.

    Must be aged, blind, or disabled.  Earned income reduces benefit by
    $1 for every $2 earned above $65/month.  SGA limit ~$1,550/month.
    """
    if not bk.disability_flag:
        return 0.0

    federal_benefit_rate_monthly = 943.0
    sga_monthly = 1_550.0

    monthly_income = income / 12

    # If earnings exceed SGA, generally ineligible
    if monthly_income > sga_monthly:
        return 0.0

    # Earned income exclusion: first $65 + half of remainder
    countable_earned = max(0.0, (monthly_income - 65.0) / 2.0)
    # General income exclusion: $20/month
    countable = max(0.0, countable_earned - 20.0)

    benefit_monthly = max(0.0, federal_benefit_rate_monthly - countable)
    return round(benefit_monthly * 12, 2)


def _calc_chip(
    income: float,
    fpl: float,
    household_size: int,
    num_children: int,
    bk: PersonBudgetKey,
) -> float:
    """CHIP: Covers children in families between 138% and ~300% FPL.

    Benefit value ~$4,000/child/year.
    """
    if num_children == 0:
        return 0.0

    lower = fpl * 1.38
    upper = fpl * 3.00  # varies by state, we use 300%

    if income > lower and income <= upper:
        return 4_000.0 * num_children
    return 0.0


def _calc_marketplace_subsidy(
    income: float,
    fpl: float,
    household_size: int,
    num_children: int,
    bk: PersonBudgetKey,
) -> float:
    """ACA Marketplace premium subsidy: 100-400% FPL, cliff at 400%.

    Premium contribution ranges from 0% of income at 100% FPL to 8.5%
    at 400% FPL.  The subsidy = benchmark_premium - expected_contribution.
    Above 400% FPL, subsidy drops to $0 (the cliff).

    Note: IRA extended enhanced subsidies through 2025, removing the cliff
    temporarily.  We model the statutory 400% FPL cliff for structural
    analysis.
    """
    lower = fpl * 1.00
    upper = fpl * 4.00

    if income < lower or income > upper:
        return 0.0

    # Benchmark silver plan premium (~$7,500/year for individual)
    benchmark = 7_500.0 + (household_size - 1) * 3_000.0

    # Expected contribution as % of income scales with FPL %
    fpl_pct = income / fpl
    if fpl_pct <= 1.50:
        contribution_pct = 0.0
    elif fpl_pct <= 2.00:
        contribution_pct = 0.02 + (fpl_pct - 1.50) * 0.04
    elif fpl_pct <= 2.50:
        contribution_pct = 0.04 + (fpl_pct - 2.00) * 0.04
    elif fpl_pct <= 3.00:
        contribution_pct = 0.06 + (fpl_pct - 2.50) * 0.02
    else:
        contribution_pct = 0.07 + (fpl_pct - 3.00) * 0.015

    contribution_pct = min(contribution_pct, 0.085)
    expected_contribution = income * contribution_pct
    subsidy = max(0.0, benchmark - expected_contribution)
    return round(subsidy, 2)


def _calc_eitc(
    income: float,
    fpl: float,
    household_size: int,
    num_children: int,
    bk: PersonBudgetKey,
) -> float:
    """Earned Income Tax Credit (2024 parameters).

    The EITC has three phases: phase-in, plateau, and phase-out.
    Parameters vary by number of qualifying children.

    For single/head-of-household filers:
    - 0 children: max $632, phase-out ends $17,640
    - 1 child: max $3,995, phase-out ends $46,560
    - 2 children: max $6,604, phase-out ends $52,918
    - 3+ children: max $7,430, phase-out ends $56,838
    """
    # EITC parameters by number of qualifying children
    params = {
        0: {"phase_in_rate": 0.0765, "max_credit": 632,
            "phase_in_end": 8_260, "phase_out_start": 10_330,
            "phase_out_rate": 0.0765, "phase_out_end": 17_640},
        1: {"phase_in_rate": 0.34, "max_credit": 3_995,
            "phase_in_end": 11_750, "phase_out_start": 21_560,
            "phase_out_rate": 0.1598, "phase_out_end": 46_560},
        2: {"phase_in_rate": 0.40, "max_credit": 6_604,
            "phase_in_end": 16_510, "phase_out_start": 21_560,
            "phase_out_rate": 0.2106, "phase_out_end": 52_918},
        3: {"phase_in_rate": 0.45, "max_credit": 7_430,
            "phase_in_end": 16_510, "phase_out_start": 21_560,
            "phase_out_rate": 0.2106, "phase_out_end": 56_838},
    }

    n_kids = min(num_children, 3)
    p = params[n_kids]

    if income <= 0:
        return 0.0

    # Phase-in
    if income <= p["phase_in_end"]:
        return round(min(income * p["phase_in_rate"], p["max_credit"]), 2)

    # Plateau
    if income <= p["phase_out_start"]:
        return float(p["max_credit"])

    # Phase-out
    if income <= p["phase_out_end"]:
        reduction = (income - p["phase_out_start"]) * p["phase_out_rate"]
        return round(max(0.0, p["max_credit"] - reduction), 2)

    return 0.0


def _calc_child_tax_credit(
    income: float,
    fpl: float,
    household_size: int,
    num_children: int,
    bk: PersonBudgetKey,
) -> float:
    """Child Tax Credit: $2,000 per child, phase-out at $200K single / $400K married.

    For this model we assume single filing status.  The phase-out reduces
    the credit by $50 for every $1,000 over the threshold.
    """
    if num_children == 0:
        return 0.0

    max_credit = 2_000.0 * num_children
    threshold = 200_000.0  # single filer

    if income <= threshold:
        return max_credit

    reduction = math.floor((income - threshold) / 1_000) * 50
    return max(0.0, max_credit - reduction)


def _calc_ccdf(
    income: float,
    fpl: float,
    household_size: int,
    num_children: int,
    bk: PersonBudgetKey,
) -> float:
    """CCDF childcare subsidy: ~85% State Median Income.

    Approximate 85% SMI as ~$45,000 for a family of 3.  Benefit = cost of
    care - family copay.
    """
    if num_children == 0:
        return 0.0

    # 85% SMI varies by state; use ~$45,000 as baseline for family of 3
    smi_85 = 45_000.0 + (household_size - 3) * 4_000.0
    smi_85 = max(smi_85, 25_000.0)

    if income > smi_85:
        return 0.0

    # Average childcare cost ~$12,000/year per child; subsidy covers most
    annual_care_cost = 12_000.0 * min(num_children, 3)

    # Copay = sliding scale percentage of income
    copay_pct = max(0.0, min(0.10, income / smi_85 * 0.10))
    copay = income * copay_pct
    benefit = max(0.0, annual_care_cost - copay)
    return round(benefit, 2)


def _calc_wioa(
    income: float,
    fpl: float,
    household_size: int,
    num_children: int,
    bk: PersonBudgetKey,
) -> float:
    """WIOA: Not directly income-tested for basic career services.

    Intensive/training services prioritize low-income.  We model a fixed
    benefit for those under 200% FPL.
    """
    if income <= fpl * 2.00:
        return 3_000.0
    return 0.0


# ---------------------------------------------------------------------------
# Estimated taxes (simplified)
# ---------------------------------------------------------------------------

def _estimate_taxes(
    income: float,
    num_children: int,
) -> float:
    """Estimate combined federal income + FICA taxes.

    Uses simplified 2024 brackets for single filer + standard deduction.
    Does not model state taxes (would vary by jurisdiction).
    """
    # FICA: 7.65% (Social Security 6.2% + Medicare 1.45%) on earned income
    fica = income * 0.0765

    # Federal income tax with 2024 standard deduction ($14,600 single)
    standard_deduction = 14_600.0
    taxable = max(0.0, income - standard_deduction)

    # 2024 brackets for single filer
    brackets = [
        (11_600, 0.10),
        (47_150 - 11_600, 0.12),
        (100_525 - 47_150, 0.22),
        (191_950 - 100_525, 0.24),
        (243_725 - 191_950, 0.32),
        (609_350 - 243_725, 0.35),
        (float("inf"), 0.37),
    ]

    federal_tax = 0.0
    remaining = taxable
    for bracket_size, rate in brackets:
        if remaining <= 0:
            break
        taxed = min(remaining, bracket_size)
        federal_tax += taxed * rate
        remaining -= taxed

    return max(0.0, fica + federal_tax)


# ---------------------------------------------------------------------------
# Program registry
# ---------------------------------------------------------------------------

_PROGRAM_CALCULATORS = {
    "Medicaid": _calc_medicaid,
    "SNAP": _calc_snap,
    "TANF": _calc_tanf,
    "Housing Assistance": _calc_housing_assistance,
    "SSI": _calc_ssi,
    "CHIP": _calc_chip,
    "ACA Marketplace Subsidy": _calc_marketplace_subsidy,
    "EITC": _calc_eitc,
    "Child Tax Credit": _calc_child_tax_credit,
    "CCDF Childcare": _calc_ccdf,
    "WIOA": _calc_wioa,
}


# ---------------------------------------------------------------------------
# Main engine class
# ---------------------------------------------------------------------------

class BenefitsCliffCalculator:
    """Benefits cliff analysis engine.

    Computes net resources and effective marginal tax rates at each
    income level for a given person profile, identifying cliff points
    where benefit loss creates perverse incentives.

    Parameters
    ----------
    income_step : float
        Income increment for analysis (default $1,000).
    income_max : float
        Maximum income to analyze (default $100,000).
    cliff_emtr_threshold : float
        EMTR threshold above which a point is flagged as a cliff
        (default 0.80 = 80%).
    """

    def __init__(
        self,
        income_step: float = 1_000.0,
        income_max: float = 100_000.0,
        cliff_emtr_threshold: float = 0.80,
    ) -> None:
        self.income_step = income_step
        self.income_max = income_max
        self.cliff_emtr_threshold = cliff_emtr_threshold

    def analyze(
        self,
        budget_key: PersonBudgetKey,
    ) -> list[BenefitsCliffPoint]:
        """Compute the benefits cliff curve for a person.

        Parameters
        ----------
        budget_key : PersonBudgetKey
            Person's demographic and economic profile.  Key fields used:
            ``household_size``, ``dependents_ages``, ``disability_flag``.

        Returns
        -------
        list[BenefitsCliffPoint]
            One entry per income level from $0 to ``income_max`` in
            ``income_step`` increments.  Cliff points are marked with
            ``is_cliff=True``.
        """
        household_size = max(1, budget_key.household_size)
        num_children = len([a for a in budget_key.dependents_ages if a < 18])
        fpl = _fpl(household_size)

        points: list[BenefitsCliffPoint] = []
        prev_net_resources: float | None = None

        income_level = 0.0
        while income_level <= self.income_max + 0.01:
            # Compute benefits at this income level
            benefits: dict[str, float] = {}
            for program_name, calc_fn in _PROGRAM_CALCULATORS.items():
                value = calc_fn(
                    income_level, fpl, household_size, num_children, budget_key
                )
                if value > 0:
                    benefits[program_name] = round(value, 2)

            total_benefits = sum(benefits.values())

            # Estimate taxes
            taxes = _estimate_taxes(income_level, num_children)

            # Net resources = income + benefits - taxes
            net_resources = income_level + total_benefits - taxes

            # Compute EMTR relative to previous point
            emtr = 0.0
            programs_lost: list[str] = []
            is_cliff = False

            if prev_net_resources is not None and self.income_step > 0:
                delta_net = net_resources - prev_net_resources
                emtr = 1.0 - (delta_net / self.income_step)

                # Check for cliff conditions
                if emtr > self.cliff_emtr_threshold:
                    is_cliff = True
                if delta_net < 0:
                    is_cliff = True

                # Identify programs lost compared to previous point
                if len(points) > 0:
                    prev_benefits = points[-1].benefits
                    for prog_name in prev_benefits:
                        if prog_name not in benefits or benefits.get(prog_name, 0) == 0:
                            programs_lost.append(prog_name)

            point = BenefitsCliffPoint(
                income=income_level,
                benefits=benefits,
                total_benefits_value=round(total_benefits, 2),
                net_resources=round(net_resources, 2),
                effective_marginal_tax_rate=round(emtr, 4),
                programs_lost=programs_lost,
                is_cliff=is_cliff,
            )
            points.append(point)

            prev_net_resources = net_resources
            income_level += self.income_step

        return points

    def find_cliffs(
        self,
        budget_key: PersonBudgetKey,
    ) -> list[BenefitsCliffPoint]:
        """Return only the cliff points (EMTR > threshold or net loss).

        Convenience method that filters the full analysis to only the
        points where the person faces a benefits cliff.
        """
        all_points = self.analyze(budget_key)
        return [p for p in all_points if p.is_cliff]

    def worst_cliff(
        self,
        budget_key: PersonBudgetKey,
    ) -> BenefitsCliffPoint | None:
        """Return the single worst cliff point (highest EMTR).

        Returns ``None`` if no cliffs are detected.
        """
        cliffs = self.find_cliffs(budget_key)
        if not cliffs:
            return None
        return max(cliffs, key=lambda p: p.effective_marginal_tax_rate)

    def summarize(
        self,
        budget_key: PersonBudgetKey,
    ) -> dict[str, Any]:
        """Return a JSON-serializable summary of the cliff analysis.

        Includes the number of cliff points, worst EMTR, and the income
        ranges where cliffs occur.
        """
        all_points = self.analyze(budget_key)
        cliffs = [p for p in all_points if p.is_cliff]

        worst = max(cliffs, key=lambda p: p.effective_marginal_tax_rate) if cliffs else None

        cliff_ranges: list[dict[str, Any]] = []
        in_cliff = False
        range_start = 0.0
        for p in all_points:
            if p.is_cliff and not in_cliff:
                in_cliff = True
                range_start = p.income
            elif not p.is_cliff and in_cliff:
                in_cliff = False
                cliff_ranges.append({
                    "start_income": range_start,
                    "end_income": p.income - self.income_step,
                })
        if in_cliff:
            cliff_ranges.append({
                "start_income": range_start,
                "end_income": all_points[-1].income,
            })

        return {
            "person_uid": budget_key.person_uid,
            "household_size": budget_key.household_size,
            "num_children": len([a for a in budget_key.dependents_ages if a < 18]),
            "total_income_levels_analyzed": len(all_points),
            "num_cliff_points": len(cliffs),
            "worst_emtr": worst.effective_marginal_tax_rate if worst else 0.0,
            "worst_cliff_income": worst.income if worst else None,
            "cliff_ranges": cliff_ranges,
            "programs_modeled": list(_PROGRAM_CALCULATORS.keys()),
        }
