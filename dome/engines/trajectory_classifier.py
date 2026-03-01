"""Fiscal Trajectory Classifier for THE DOME.

Classifies a person's lifetime net fiscal relationship with the public sector
into one of five tiers by computing:

    net_fiscal_impact_npv = lifetime_taxes_paid - lifetime_government_cost

The classifier uses the person's income, education, age, and the computed
``WholePersonBudget`` to estimate both sides of the equation, then assigns
a ``FiscalTrajectoryTag`` based on threshold boundaries.

Tax estimation follows CBO/Urban Institute methodology:
    - Baseline average lifetime taxes: $524,625
    - Adjusted for current income relative to median
    - Adjusted for educational attainment (strong predictor of lifetime earnings)
    - Adjusted for remaining work years (age-based discount)

Government cost is the NPV sum of the lifetime horizon budget across all
payer levels.

Classification thresholds (NPV, 3% real discount rate):
    net_contributor:        NPV > +$100K
    break_even:             -$50K < NPV < +$100K
    moderate_net_cost:      -$500K < NPV < -$50K
    high_net_cost:          -$2M < NPV < -$500K
    catastrophic_net_cost:  NPV < -$2M
"""

from __future__ import annotations

import math
from typing import Literal

from dome.data.population_baselines import POPULATION_BASELINES
from dome.models.budget_key import PersonBudgetKey
from dome.models.budget_output import WholePersonBudget
from dome.models.trajectory import FiscalTrajectoryTag


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

_BASELINE_LIFETIME_TAXES: float = float(
    POPULATION_BASELINES["average_lifetime_taxes_paid"]
)  # $524,625

_REAL_DISCOUNT_RATE: float = float(
    POPULATION_BASELINES["real_discount_rate"]
)  # 0.03

_LIFE_EXPECTANCY: float = float(
    POPULATION_BASELINES["average_life_expectancy"]
)  # 78.6

# Median household income used for income-ratio adjustment.
_MEDIAN_INCOME: float = 59_540.0  # US median individual income (Census ACS)

# Assumed working-life span for a full career (18-67).
_FULL_CAREER_YEARS: float = 49.0

# Retirement age assumption.
_RETIREMENT_AGE: float = 67.0

# Entry age into workforce.
_WORK_ENTRY_AGE: float = 18.0

# Education multipliers for lifetime earnings capacity.
# Based on BLS/Census lifetime earnings differentials.
_EDUCATION_MULTIPLIERS: dict[str, float] = {
    "<HS": 0.60,
    "HS": 0.80,
    "some_college": 0.90,
    "BA": 1.20,
    "Grad": 1.50,
}
_DEFAULT_EDUCATION_MULTIPLIER: float = 0.85

# Classification threshold boundaries (NPV in USD).
_THRESHOLDS: list[tuple[str, float | None, float | None]] = [
    # (trajectory_label, npv_lower_bound, npv_upper_bound)
    ("catastrophic_net_cost", None, -2_000_000.0),
    ("high_net_cost", -2_000_000.0, -500_000.0),
    ("moderate_net_cost", -500_000.0, -50_000.0),
    ("break_even", -50_000.0, 100_000.0),
    ("net_contributor", 100_000.0, None),
]


# ---------------------------------------------------------------------------
# Helper: NPV of an annuity
# ---------------------------------------------------------------------------

def _npv_annuity(
    annual_amount: float,
    n_years: float,
    rate: float = _REAL_DISCOUNT_RATE,
) -> float:
    """Compute the net present value of a level annuity.

    Parameters
    ----------
    annual_amount : float
        Annual payment (constant in real terms).
    n_years : float
        Duration of the annuity in years.
    rate : float
        Real discount rate per year.

    Returns
    -------
    float
        Present value of the annuity stream.
    """
    if rate == 0.0 or n_years <= 0.0:
        return annual_amount * max(n_years, 0.0)
    return annual_amount * (1.0 - (1.0 + rate) ** (-n_years)) / rate


# ---------------------------------------------------------------------------
# Helper: estimate lifetime taxes
# ---------------------------------------------------------------------------

def _estimate_lifetime_taxes(
    budget_key: PersonBudgetKey,
) -> float:
    """Estimate the NPV of remaining lifetime tax contributions.

    The estimation proceeds in three steps:

    1. **Income adjustment**: Scale the baseline by the ratio of the person's
       current income to the national median.  If income is unknown, use the
       education multiplier as a proxy.

    2. **Education adjustment**: Apply a multiplier reflecting the lifetime
       earnings premium (or penalty) associated with the person's highest
       credential.

    3. **Age adjustment**: Only the *remaining* working years contribute.
       Discount future tax payments at the real discount rate.

    Returns the NPV of estimated remaining lifetime taxes in current USD.
    """
    # --- Education multiplier ---
    edu = budget_key.educational_attainment
    edu_mult = _EDUCATION_MULTIPLIERS.get(edu, _DEFAULT_EDUCATION_MULTIPLIER)

    # --- Income adjustment ---
    if (
        budget_key.current_annual_income is not None
        and budget_key.current_annual_income > 0
    ):
        income_ratio = budget_key.current_annual_income / _MEDIAN_INCOME
    else:
        # No income data: use education as proxy.
        income_ratio = edu_mult

    # --- Remaining working years ---
    age = float(budget_key.age)
    remaining_work_years = max(_RETIREMENT_AGE - age, 0.0)

    # If already past retirement, only Social Security / investment income taxes
    # contribute -- model as 15% of baseline annual rate for remaining life.
    remaining_life = max(_LIFE_EXPECTANCY - age, 0.0)

    # Compute annual tax contribution.
    # The baseline $524,625 is spread over a full 49-year career.
    baseline_annual_tax = _BASELINE_LIFETIME_TAXES / _FULL_CAREER_YEARS  # ~$10,707

    # Adjusted annual tax during working years.
    adjusted_annual_tax = baseline_annual_tax * income_ratio * edu_mult

    # Cap the income-education adjustment to avoid unrealistic extremes.
    adjusted_annual_tax = max(adjusted_annual_tax, 0.0)
    adjusted_annual_tax = min(adjusted_annual_tax, baseline_annual_tax * 8.0)

    # Employment status penalty.
    emp_status = budget_key.employment_status.lower()
    if emp_status in ("disabled",):
        # Disabled persons earn minimal taxable income.
        adjusted_annual_tax *= 0.10
    elif emp_status in ("unemployed", "nilf"):
        # Currently not earning; discount near-term contributions.
        adjusted_annual_tax *= 0.30
    elif emp_status in ("pt", "gig"):
        adjusted_annual_tax *= 0.65

    # NPV of working-year taxes.
    npv_working = _npv_annuity(adjusted_annual_tax, remaining_work_years)

    # NPV of retirement-year taxes (Social Security income tax, RMDs, etc.).
    retirement_years = max(remaining_life - remaining_work_years, 0.0)
    retirement_annual_tax = adjusted_annual_tax * 0.15
    npv_retirement = 0.0
    if retirement_years > 0 and remaining_work_years > 0:
        # Discount retirement taxes to present value, accounting for the
        # delay until retirement starts.
        retirement_pv_at_retirement = _npv_annuity(
            retirement_annual_tax, retirement_years,
        )
        # Discount back from retirement start to today.
        npv_retirement = retirement_pv_at_retirement / (
            (1.0 + _REAL_DISCOUNT_RATE) ** remaining_work_years
        )
    elif retirement_years > 0:
        # Already retired.
        npv_retirement = _npv_annuity(retirement_annual_tax, retirement_years)

    return npv_working + npv_retirement


# ---------------------------------------------------------------------------
# Helper: extract lifetime government cost from budget
# ---------------------------------------------------------------------------

def _extract_lifetime_government_cost(budget: WholePersonBudget) -> float:
    """Extract the total government cost from the lifetime horizon of a budget.

    Searches for the ``"lifetime"`` horizon.  If not found, falls back to
    the longest available horizon and extrapolates.

    Returns the total expected government spend across all payer levels.
    """
    lifetime_hz = None
    longest_hz = None
    longest_years = 0.0

    for hz in budget.horizons:
        if hz.label == "lifetime":
            lifetime_hz = hz
            break
        # Track longest for fallback.
        span_years = (hz.end_date - hz.start_date).days / 365.25
        if span_years > longest_years:
            longest_years = span_years
            longest_hz = hz

    if lifetime_hz is not None:
        pv = lifetime_hz.payer_view
        return (
            pv.federal_expected_spend
            + pv.state_expected_spend
            + pv.local_expected_spend
            + pv.healthcare_delivery_expected_spend
            + pv.nonprofit_expected_spend
        )

    # Fallback: extrapolate from longest horizon.
    if longest_hz is not None and longest_years > 0:
        pv = longest_hz.payer_view
        annual_rate = (
            pv.federal_expected_spend
            + pv.state_expected_spend
            + pv.local_expected_spend
            + pv.healthcare_delivery_expected_spend
            + pv.nonprofit_expected_spend
        ) / longest_years
        # Assume 40 remaining years as a rough lifetime proxy.
        return annual_rate * 40.0

    return 0.0


# ---------------------------------------------------------------------------
# Helper: classify NPV into trajectory tier
# ---------------------------------------------------------------------------

def _classify_npv(
    npv: float,
) -> Literal[
    "net_contributor",
    "break_even",
    "moderate_net_cost",
    "high_net_cost",
    "catastrophic_net_cost",
]:
    """Map a net-fiscal-impact NPV to a trajectory label.

    Thresholds:
        net_contributor:        NPV > +$100K
        break_even:             -$50K <= NPV <= +$100K
        moderate_net_cost:      -$500K <= NPV < -$50K
        high_net_cost:          -$2M <= NPV < -$500K
        catastrophic_net_cost:  NPV < -$2M
    """
    if npv > 100_000.0:
        return "net_contributor"
    if npv > -50_000.0:
        return "break_even"
    if npv > -500_000.0:
        return "moderate_net_cost"
    if npv > -2_000_000.0:
        return "high_net_cost"
    return "catastrophic_net_cost"


# ===========================================================================
# TrajectoryClassifier -- the public API
# ===========================================================================

class TrajectoryClassifier:
    """Classify a person's lifetime net fiscal trajectory.

    Given a ``PersonBudgetKey`` (for income, education, age, employment) and
    a ``WholePersonBudget`` (for projected government costs), computes the
    net present value of the person's fiscal relationship with the public
    sector and assigns a qualitative tier.

    Examples
    --------
    >>> classifier = TrajectoryClassifier()
    >>> tag = classifier.classify("person-001", budget_key, budget)
    >>> tag.trajectory
    'moderate_net_cost'
    >>> tag.net_fiscal_impact_npv
    -187432.56
    """

    def classify(
        self,
        person_uid: str,
        budget_key: PersonBudgetKey,
        budget: WholePersonBudget,
    ) -> FiscalTrajectoryTag:
        """Classify a person's lifetime fiscal trajectory.

        Parameters
        ----------
        person_uid : str
            Unique person identifier.
        budget_key : PersonBudgetKey
            Person-level attributes used for tax estimation.
        budget : WholePersonBudget
            Computed whole-person budget with at least one horizon
            (ideally ``"lifetime"``).

        Returns
        -------
        FiscalTrajectoryTag
            Classification with trajectory label and NPV estimate.
        """
        # Estimate lifetime tax contributions (NPV).
        lifetime_taxes_npv = _estimate_lifetime_taxes(budget_key)

        # Extract lifetime government cost from the budget.
        lifetime_govt_cost = _extract_lifetime_government_cost(budget)

        # Net fiscal impact: positive = net contributor, negative = net cost.
        net_fiscal_impact = lifetime_taxes_npv - lifetime_govt_cost

        # Classify into tier.
        trajectory = _classify_npv(net_fiscal_impact)

        return FiscalTrajectoryTag(
            person_uid=person_uid,
            horizon="lifetime",
            trajectory=trajectory,
            net_fiscal_impact_npv=round(net_fiscal_impact, 2),
        )

    def classify_with_details(
        self,
        person_uid: str,
        budget_key: PersonBudgetKey,
        budget: WholePersonBudget,
    ) -> dict:
        """Classify and return detailed intermediate calculations.

        Returns a dictionary containing the ``FiscalTrajectoryTag`` plus
        the intermediate values used in the computation, useful for
        debugging and audit trails.

        Parameters
        ----------
        person_uid : str
            Unique person identifier.
        budget_key : PersonBudgetKey
            Person-level attributes.
        budget : WholePersonBudget
            Computed whole-person budget.

        Returns
        -------
        dict
            Keys: ``tag``, ``lifetime_taxes_npv``, ``lifetime_govt_cost``,
            ``net_fiscal_impact``, ``income_ratio``, ``education_multiplier``,
            ``remaining_work_years``, ``remaining_life_years``.
        """
        lifetime_taxes_npv = _estimate_lifetime_taxes(budget_key)
        lifetime_govt_cost = _extract_lifetime_government_cost(budget)
        net_fiscal_impact = lifetime_taxes_npv - lifetime_govt_cost
        trajectory = _classify_npv(net_fiscal_impact)

        tag = FiscalTrajectoryTag(
            person_uid=person_uid,
            horizon="lifetime",
            trajectory=trajectory,
            net_fiscal_impact_npv=round(net_fiscal_impact, 2),
        )

        # Compute detail values for transparency.
        edu = budget_key.educational_attainment
        edu_mult = _EDUCATION_MULTIPLIERS.get(edu, _DEFAULT_EDUCATION_MULTIPLIER)

        if (
            budget_key.current_annual_income is not None
            and budget_key.current_annual_income > 0
        ):
            income_ratio = budget_key.current_annual_income / _MEDIAN_INCOME
        else:
            income_ratio = edu_mult

        age = float(budget_key.age)
        remaining_work = max(_RETIREMENT_AGE - age, 0.0)
        remaining_life = max(_LIFE_EXPECTANCY - age, 0.0)

        return {
            "tag": tag,
            "lifetime_taxes_npv": round(lifetime_taxes_npv, 2),
            "lifetime_govt_cost": round(lifetime_govt_cost, 2),
            "net_fiscal_impact": round(net_fiscal_impact, 2),
            "income_ratio": round(income_ratio, 4),
            "education_multiplier": edu_mult,
            "remaining_work_years": remaining_work,
            "remaining_life_years": remaining_life,
        }
