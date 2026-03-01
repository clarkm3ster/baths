"""Whole-Person Budget Engine -- THE SKELETON KEY.

This is the centerpiece computational engine of THE DOME.  Given a
``PersonBudgetKey`` (capturing every person-level attribute the engine needs)
and a ``fiscal_history`` (list of past ``FiscalEvent`` records), it produces a
``WholePersonBudget`` with projections across all requested time horizons.

The engine:

1. Aggregates historical spend by payer, domain, and mechanism.
2. For each horizon, computes population-baseline costs adjusted by individual
   risk multipliers (chronic conditions, justice involvement, homelessness,
   disability, mental health, high-need status).
3. Breaks projected spend into payer, domain, and mechanism views.
4. Runs Monte Carlo simulation to produce p50/p90/p99 risk profiles with
   catastrophic-event modeling.
5. Optionally generates intervention-vs-baseline scenario projections.

Uses ``numpy`` for vectorised Monte Carlo sampling.
"""

from __future__ import annotations

import math
from datetime import date, datetime, timezone
from typing import Any

import numpy as np

from dome.data.population_baselines import POPULATION_BASELINES
from dome.data.unit_costs import UNIT_COSTS
from dome.models.budget_key import BudgetHorizon, PersonBudgetKey
from dome.models.budget_output import (
    CatastrophicEventRisk,
    DomainBudget,
    HorizonBudget,
    MechanismBudget,
    PayerBreakdown,
    PayerView,
    ProgramSpend,
    RiskProfile,
    ScenarioBudget,
    WholePersonBudget,
)
from dome.models.fiscal_event import FiscalEvent


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

_REAL_DISCOUNT_RATE: float = POPULATION_BASELINES["real_discount_rate"]  # 0.03
_LIFE_EXPECTANCY: float = float(POPULATION_BASELINES["average_life_expectancy"])  # 78.6

# Population baseline annual spend per person by payer level (USD).
_FEDERAL_BASELINE: float = float(POPULATION_BASELINES["federal_spend_per_person_annual"])   # 20_600
_STATE_BASELINE: float = float(POPULATION_BASELINES["state_spend_per_person_annual"])       # 10_800
_LOCAL_BASELINE: float = float(POPULATION_BASELINES["local_spend_per_person_annual"])       # 7_200

# Chronic condition healthcare cost multiplier increments.
_CHRONIC_CONDITION_MULTIPLIERS: dict[str, float] = {
    "diabetes": 0.40,
    "heart_disease": 0.50,
    "copd": 0.35,
    "ckd": 0.45,
    "cancer": 0.50,
    "asthma": 0.30,
    "hypertension": 0.30,
    "depression": 0.30,
    "obesity": 0.30,
    "stroke": 0.45,
    "alzheimers": 0.50,
    "hiv": 0.45,
    "hepatitis_c": 0.35,
    "epilepsy": 0.35,
    "arthritis": 0.30,
}
_DEFAULT_CHRONIC_MULTIPLIER: float = 0.35  # for conditions not in the map

# Justice costs per incarceration-year (USD).
_JUSTICE_COST_MIN: float = 35_000.0
_JUSTICE_COST_MAX: float = 60_000.0
_JUSTICE_COST_MID: float = (_JUSTICE_COST_MIN + _JUSTICE_COST_MAX) / 2.0

# Homelessness reactive-service costs per year (USD).
_HOMELESSNESS_COST_MIN: float = 35_000.0
_HOMELESSNESS_COST_MAX: float = 45_000.0
_HOMELESSNESS_COST_MID: float = (_HOMELESSNESS_COST_MIN + _HOMELESSNESS_COST_MAX) / 2.0

# Disability costs (USD).
_SSDI_MIN: float = 18_000.0
_SSDI_MAX: float = 24_000.0
_SSDI_MID: float = (_SSDI_MIN + _SSDI_MAX) / 2.0
_MEDICARE_DISABILITY_ADD: float = float(UNIT_COSTS["medicare_per_beneficiary_annual"])

# Mental health cost ranges (USD per year).
_SUD_COST_MIN: float = 15_000.0
_SUD_COST_MAX: float = 30_000.0
_DEPRESSION_COST_MIN: float = 5_000.0
_DEPRESSION_COST_MAX: float = 10_000.0

# High-need multiplier applied to healthcare portion.
_HIGH_NEED_MULTIPLIER: float = 2.0

# Domain labels used throughout.
_DOMAINS: list[str] = [
    "healthcare",
    "income_support",
    "housing",
    "food",
    "education",
    "justice",
    "child_family",
    "transport",
    "other",
]

# Mechanism labels.
_MECHANISMS: list[str] = [
    "cash_transfer",
    "in_kind_benefit",
    "service_utilization",
    "tax_expenditure",
]

# Horizon label -> approximate number of years.
_HORIZON_YEARS: dict[str, float | None] = {
    "1y": 1.0,
    "5y": 5.0,
    "20y": 20.0,
    "lifetime": None,  # computed from age
}

# ---------------------------------------------------------------------------
# Helper: discount factor
# ---------------------------------------------------------------------------

def _discount_factor(years: float, rate: float = _REAL_DISCOUNT_RATE) -> float:
    """Return the present-value discount factor for *years* at *rate*."""
    return 1.0 / ((1.0 + rate) ** years)


def _npv_annuity(annual_amount: float, n_years: float, rate: float = _REAL_DISCOUNT_RATE) -> float:
    """Compute the NPV of a level annuity of *annual_amount* for *n_years*."""
    if rate == 0.0 or n_years <= 0.0:
        return annual_amount * max(n_years, 0.0)
    # Standard annuity formula: PV = C * [1 - (1+r)^{-n}] / r
    return annual_amount * (1.0 - (1.0 + rate) ** (-n_years)) / rate


# ---------------------------------------------------------------------------
# Helper: aggregate historical fiscal events
# ---------------------------------------------------------------------------

def _aggregate_history(
    fiscal_history: list[FiscalEvent],
) -> dict[str, dict[str, float]]:
    """Aggregate historical spend along three axes.

    Returns a dict with keys ``"payer"``, ``"domain"``, ``"mechanism"``,
    each mapping a category label to total historical spend.
    """
    payer_totals: dict[str, float] = {}
    domain_totals: dict[str, float] = {}
    mechanism_totals: dict[str, float] = {}

    for evt in fiscal_history:
        key_payer = f"{evt.payer_level}:{evt.payer_entity}"
        payer_totals[key_payer] = payer_totals.get(key_payer, 0.0) + evt.amount_paid
        domain_totals[evt.domain] = domain_totals.get(evt.domain, 0.0) + evt.amount_paid
        mechanism_totals[evt.mechanism] = mechanism_totals.get(evt.mechanism, 0.0) + evt.amount_paid

    return {
        "payer": payer_totals,
        "domain": domain_totals,
        "mechanism": mechanism_totals,
    }


# ---------------------------------------------------------------------------
# Core: individual risk-adjusted annual cost computation
# ---------------------------------------------------------------------------

def _compute_annual_costs(key: PersonBudgetKey) -> dict[str, Any]:
    """Compute risk-adjusted annual costs for a person.

    Returns a dictionary with keys:
        - ``federal_annual``, ``state_annual``, ``local_annual``
        - ``healthcare_delivery_annual``, ``nonprofit_annual``
        - ``domain_annual``: dict mapping domain -> annual spend
        - ``mechanism_annual``: dict mapping mechanism -> annual spend
        - ``healthcare_multiplier``: total healthcare multiplier applied
        - ``risk_flags``: summary of which risk factors are active
    """
    # ------------------------------------------------------------------
    # Step 1: start with population baselines
    # ------------------------------------------------------------------
    federal = _FEDERAL_BASELINE
    state = _STATE_BASELINE
    local = _LOCAL_BASELINE

    # Initialize domain-level annual costs (population baseline allocation).
    # Healthcare is ~50% of federal, ~30% of state, ~10% of local.
    domain_annual: dict[str, float] = {
        "healthcare": 0.50 * federal + 0.30 * state + 0.10 * local,
        "income_support": 0.15 * federal + 0.10 * state,
        "housing": 0.02 * federal + 0.05 * state + 0.15 * local,
        "food": 0.04 * federal + 0.02 * state,
        "education": 0.05 * federal + 0.25 * state + 0.40 * local,
        "justice": 0.02 * federal + 0.10 * state + 0.20 * local,
        "child_family": 0.04 * federal + 0.05 * state + 0.05 * local,
        "transport": 0.03 * federal + 0.08 * state + 0.08 * local,
        "other": 0.0,
    }
    # Assign residual to "other" so totals are consistent.
    allocated = sum(domain_annual.values())
    total_baseline = federal + state + local
    domain_annual["other"] = max(total_baseline - allocated, 0.0)

    risk_flags: dict[str, bool] = {}

    # ------------------------------------------------------------------
    # Step 2: chronic condition healthcare multipliers
    # ------------------------------------------------------------------
    healthcare_multiplier = 1.0
    for cond in key.chronic_condition_flags:
        cond_lower = cond.lower().replace(" ", "_").replace("-", "_")
        mult = _CHRONIC_CONDITION_MULTIPLIERS.get(cond_lower, _DEFAULT_CHRONIC_MULTIPLIER)
        healthcare_multiplier += mult
        risk_flags[f"chronic:{cond_lower}"] = True

    # ------------------------------------------------------------------
    # Step 3: justice involvement
    # ------------------------------------------------------------------
    justice_additional = 0.0
    incarceration_days = key.past_12m_jail_days + key.past_12m_prison_days
    if incarceration_days > 0:
        # Annualize: fraction of year incarcerated * per-year cost
        incarceration_fraction = min(incarceration_days / 365.0, 1.0)
        justice_additional = incarceration_fraction * _JUSTICE_COST_MID
        risk_flags["justice_involvement"] = True
    elif key.justice_involvement_flag:
        # Historical involvement but not recent -- add supervision / recidivism costs.
        justice_additional = float(UNIT_COSTS["probation_annual"])
        risk_flags["justice_history"] = True

    domain_annual["justice"] += justice_additional
    # Justice costs split: ~50% state corrections, ~30% county jail, ~20% local.
    state += justice_additional * 0.50
    local += justice_additional * 0.50  # county + local combined

    # ------------------------------------------------------------------
    # Step 4: homelessness
    # ------------------------------------------------------------------
    homelessness_additional = 0.0
    housing_status = key.housing_status.lower()
    if housing_status in ("shelter", "street"):
        homelessness_additional = _HOMELESSNESS_COST_MID
        risk_flags["currently_homeless"] = True
    elif key.homelessness_history_flag or housing_status in ("cost_burdened", "doubled_up"):
        # At-risk: add a fraction of full homelessness cost.
        homelessness_additional = _HOMELESSNESS_COST_MID * 0.25
        risk_flags["homelessness_risk"] = True

    # Homelessness costs are reactive: ER, shelter, police.
    domain_annual["healthcare"] += homelessness_additional * 0.40
    domain_annual["housing"] += homelessness_additional * 0.35
    domain_annual["justice"] += homelessness_additional * 0.25
    # Payer allocation: mostly local/state.
    local += homelessness_additional * 0.50
    state += homelessness_additional * 0.30
    federal += homelessness_additional * 0.20

    # ------------------------------------------------------------------
    # Step 5: disability
    # ------------------------------------------------------------------
    disability_additional = 0.0
    if key.disability_flag:
        disability_additional = _SSDI_MID + _MEDICARE_DISABILITY_ADD
        domain_annual["income_support"] += _SSDI_MID
        domain_annual["healthcare"] += _MEDICARE_DISABILITY_ADD
        federal += disability_additional  # SSDI + Medicare are federal
        risk_flags["disability"] = True

    # ------------------------------------------------------------------
    # Step 6: mental health / SUD
    # ------------------------------------------------------------------
    mental_health_additional = 0.0

    # Check chronic condition flags for SUD indicators.
    sud_conditions = {"sud", "substance_use_disorder", "opioid_use_disorder",
                      "alcohol_use_disorder", "substance_abuse"}
    depression_conditions = {"depression", "major_depression", "mdd",
                             "major_depressive_disorder"}
    has_sud = any(c.lower().replace(" ", "_").replace("-", "_") in sud_conditions
                  for c in key.chronic_condition_flags)
    has_depression = any(c.lower().replace(" ", "_").replace("-", "_") in depression_conditions
                         for c in key.chronic_condition_flags)

    if has_sud:
        sud_cost = (_SUD_COST_MIN + _SUD_COST_MAX) / 2.0
        mental_health_additional += sud_cost
        domain_annual["healthcare"] += sud_cost * 0.70
        domain_annual["justice"] += sud_cost * 0.30
        risk_flags["sud"] = True

    if has_depression:
        dep_cost = (_DEPRESSION_COST_MIN + _DEPRESSION_COST_MAX) / 2.0
        mental_health_additional += dep_cost
        domain_annual["healthcare"] += dep_cost
        risk_flags["depression"] = True

    federal += mental_health_additional * 0.60  # Medicaid/Medicare
    state += mental_health_additional * 0.30    # state mental health block grants
    local += mental_health_additional * 0.10    # community MH centers

    # ------------------------------------------------------------------
    # Step 7: high-need multiplier on healthcare
    # ------------------------------------------------------------------
    if key.high_need_flag:
        # Double the healthcare component.
        pre_hc = domain_annual["healthcare"]
        domain_annual["healthcare"] *= _HIGH_NEED_MULTIPLIER
        hc_increase = domain_annual["healthcare"] - pre_hc
        federal += hc_increase * 0.55
        state += hc_increase * 0.30
        local += hc_increase * 0.15
        healthcare_multiplier *= _HIGH_NEED_MULTIPLIER
        risk_flags["high_need"] = True

    # ------------------------------------------------------------------
    # Step 8: apply chronic-condition multiplier to healthcare domain
    # ------------------------------------------------------------------
    if healthcare_multiplier > 1.0:
        # The multiplier increases the healthcare domain cost.
        base_hc = domain_annual["healthcare"]
        # We already accumulated individual chronic condition additions
        # via homelessness, disability, SUD, depression.  The multiplier
        # is applied to the *baseline* healthcare portion only to avoid
        # double-counting.
        baseline_hc = 0.50 * _FEDERAL_BASELINE + 0.30 * _STATE_BASELINE + 0.10 * _LOCAL_BASELINE
        incremental = baseline_hc * (healthcare_multiplier - 1.0)
        domain_annual["healthcare"] += incremental
        federal += incremental * 0.55
        state += incremental * 0.30
        local += incremental * 0.15

    # ------------------------------------------------------------------
    # Step 9: derive healthcare delivery + nonprofit annual
    # ------------------------------------------------------------------
    total_hc = domain_annual["healthcare"]
    healthcare_delivery = total_hc * 0.15  # uncompensated care / cost-shifting
    nonprofit = (
        domain_annual.get("housing", 0.0) * 0.08
        + domain_annual.get("food", 0.0) * 0.10
        + domain_annual.get("child_family", 0.0) * 0.10
        + total_hc * 0.03
    )

    # ------------------------------------------------------------------
    # Step 10: mechanism allocation
    # ------------------------------------------------------------------
    total_annual = sum(domain_annual.values())
    mechanism_annual: dict[str, float] = {
        "cash_transfer": (
            domain_annual.get("income_support", 0.0) * 0.70
            + domain_annual.get("food", 0.0) * 0.20
        ),
        "in_kind_benefit": (
            domain_annual.get("housing", 0.0) * 0.80
            + domain_annual.get("food", 0.0) * 0.60
            + domain_annual.get("child_family", 0.0) * 0.50
        ),
        "service_utilization": (
            domain_annual.get("healthcare", 0.0) * 0.85
            + domain_annual.get("justice", 0.0) * 0.90
            + domain_annual.get("education", 0.0) * 0.90
            + domain_annual.get("transport", 0.0) * 0.70
        ),
        "tax_expenditure": 0.0,
    }
    # EITC / CTC / mortgage-interest if income present.
    if key.current_annual_income and key.current_annual_income < 60_000:
        mechanism_annual["tax_expenditure"] = min(key.current_annual_income * 0.08, 5_000.0)
    else:
        mechanism_annual["tax_expenditure"] = total_annual * 0.05

    # Normalise mechanisms so they sum to total_annual.
    mech_sum = sum(mechanism_annual.values())
    if mech_sum > 0:
        scale = total_annual / mech_sum
        mechanism_annual = {k: v * scale for k, v in mechanism_annual.items()}

    return {
        "federal_annual": federal,
        "state_annual": state,
        "local_annual": local,
        "healthcare_delivery_annual": healthcare_delivery,
        "nonprofit_annual": nonprofit,
        "domain_annual": domain_annual,
        "mechanism_annual": mechanism_annual,
        "healthcare_multiplier": healthcare_multiplier,
        "risk_flags": risk_flags,
    }


# ---------------------------------------------------------------------------
# Payer breakdown detail builder
# ---------------------------------------------------------------------------

def _build_payer_breakdowns(
    key: PersonBudgetKey,
    annual: dict[str, Any],
    n_years: float,
) -> list[PayerBreakdown]:
    """Build itemised payer breakdown for a horizon."""
    domain = annual["domain_annual"]
    fed = annual["federal_annual"] * n_years
    st = annual["state_annual"] * n_years

    breakdowns: list[PayerBreakdown] = []

    # Federal entities.
    hc_fed = domain.get("healthcare", 0.0) * 0.55 * n_years
    if key.enrollment_snapshot.medicaid:
        medicaid_share = hc_fed * 0.55
        medicare_share = hc_fed * 0.10
    elif key.enrollment_snapshot.medicare:
        medicaid_share = hc_fed * 0.10
        medicare_share = hc_fed * 0.60
    else:
        medicaid_share = hc_fed * 0.30
        medicare_share = hc_fed * 0.20

    breakdowns.append(PayerBreakdown(
        payer_level="federal", payer_entity="CMS-Medicaid",
        expected_spend=round(medicaid_share, 2),
    ))
    breakdowns.append(PayerBreakdown(
        payer_level="federal", payer_entity="CMS-Medicare",
        expected_spend=round(medicare_share, 2),
    ))
    breakdowns.append(PayerBreakdown(
        payer_level="federal", payer_entity="SNAP/FNS",
        expected_spend=round(domain.get("food", 0.0) * 0.80 * n_years, 2),
    ))

    ssi_ssdi = 0.0
    if key.disability_flag:
        ssi_ssdi = _SSDI_MID * n_years
    elif key.enrollment_snapshot.ssi:
        ssi_ssdi = float(UNIT_COSTS["ssi_annual"]) * n_years
    breakdowns.append(PayerBreakdown(
        payer_level="federal", payer_entity="SSA-SSI/SSDI",
        expected_spend=round(ssi_ssdi, 2),
    ))

    fed_tax_exp = annual["mechanism_annual"].get("tax_expenditure", 0.0) * n_years
    breakdowns.append(PayerBreakdown(
        payer_level="federal", payer_entity="IRS-Tax Expenditures",
        expected_spend=round(fed_tax_exp * 0.80, 2),
    ))

    # State entities.
    breakdowns.append(PayerBreakdown(
        payer_level="state", payer_entity="State Medicaid Match",
        expected_spend=round(medicaid_share * 0.40, 2),  # FMAP ~60% fed, ~40% state
    ))
    breakdowns.append(PayerBreakdown(
        payer_level="state", payer_entity="State Corrections",
        expected_spend=round(domain.get("justice", 0.0) * 0.50 * n_years, 2),
    ))
    breakdowns.append(PayerBreakdown(
        payer_level="state", payer_entity="State Education",
        expected_spend=round(domain.get("education", 0.0) * 0.45 * n_years, 2),
    ))

    # Local entities.
    breakdowns.append(PayerBreakdown(
        payer_level="local", payer_entity="County Jail",
        expected_spend=round(domain.get("justice", 0.0) * 0.30 * n_years, 2),
    ))
    breakdowns.append(PayerBreakdown(
        payer_level="local", payer_entity="Homeless Services",
        expected_spend=round(domain.get("housing", 0.0) * 0.30 * n_years, 2),
    ))
    breakdowns.append(PayerBreakdown(
        payer_level="local", payer_entity="Local Schools",
        expected_spend=round(domain.get("education", 0.0) * 0.40 * n_years, 2),
    ))

    # Healthcare delivery (uncompensated care).
    breakdowns.append(PayerBreakdown(
        payer_level="health_system", payer_entity="Hospital Uncompensated Care",
        expected_spend=round(annual["healthcare_delivery_annual"] * n_years, 2),
    ))

    # Nonprofit.
    breakdowns.append(PayerBreakdown(
        payer_level="nonprofit", payer_entity="Charitable Services",
        expected_spend=round(annual["nonprofit_annual"] * n_years, 2),
    ))

    return breakdowns


# ---------------------------------------------------------------------------
# Domain budget builder
# ---------------------------------------------------------------------------

def _build_domain_budgets(
    key: PersonBudgetKey,
    annual: dict[str, Any],
    n_years: float,
) -> list[DomainBudget]:
    """Build per-domain budget projections for a horizon."""
    domain_annual = annual["domain_annual"]
    results: list[DomainBudget] = []

    # Program-level detail mappings for each domain.
    _domain_programs: dict[str, list[tuple[str, float]]] = {
        "healthcare": [
            ("Medicaid", 0.40), ("Medicare", 0.25), ("ACA Marketplace", 0.10),
            ("VA Healthcare", 0.05), ("Uncompensated Care", 0.15),
            ("Community Health Centers", 0.05),
        ],
        "income_support": [
            ("SSDI", 0.35), ("SSI", 0.25), ("TANF", 0.15),
            ("Unemployment Insurance", 0.15), ("General Assistance", 0.10),
        ],
        "housing": [
            ("Section 8 HCV", 0.35), ("Public Housing", 0.20),
            ("Permanent Supportive Housing", 0.15), ("Emergency Shelter", 0.15),
            ("Rapid Rehousing", 0.10), ("LIHEAP", 0.05),
        ],
        "food": [
            ("SNAP", 0.70), ("WIC", 0.10), ("School Meals", 0.10),
            ("Food Banks (nonprofit)", 0.10),
        ],
        "education": [
            ("K-12 Public Education", 0.50), ("Special Education", 0.15),
            ("Head Start", 0.10), ("Pell Grants", 0.10),
            ("Adult Education/WIOA", 0.15),
        ],
        "justice": [
            ("State Prison", 0.35), ("County Jail", 0.25),
            ("Probation/Parole", 0.15), ("Courts", 0.10),
            ("Police/Law Enforcement", 0.15),
        ],
        "child_family": [
            ("Foster Care", 0.30), ("Child Care Subsidies", 0.25),
            ("Child Welfare Services", 0.20), ("Adoption Assistance", 0.10),
            ("Head Start (Family)", 0.15),
        ],
        "transport": [
            ("Public Transit Subsidy", 0.50), ("Medicaid NEMT", 0.30),
            ("Other Transport Aid", 0.20),
        ],
        "other": [
            ("Miscellaneous Services", 1.00),
        ],
    }

    for domain_name in _DOMAINS:
        total = domain_annual.get(domain_name, 0.0) * n_years
        programs = _domain_programs.get(domain_name, [("Other", 1.0)])
        per_program = [
            ProgramSpend(
                program_or_fund=prog_name,
                expected_spend=round(total * share, 2),
            )
            for prog_name, share in programs
            if total * share > 0.01
        ]
        results.append(DomainBudget(
            domain=domain_name,
            expected_spend=round(total, 2),
            per_program=per_program,
        ))

    return results


# ---------------------------------------------------------------------------
# Monte Carlo risk profile
# ---------------------------------------------------------------------------

def _run_monte_carlo(
    key: PersonBudgetKey,
    annual: dict[str, Any],
    n_years: float,
    iterations: int,
    rng: np.random.Generator,
) -> RiskProfile:
    """Run Monte Carlo simulation for cost distribution and catastrophic events.

    Each iteration simulates year-by-year costs with stochastic variation and
    possible catastrophic events (incarceration, hospitalization, homelessness).

    Returns a ``RiskProfile`` with p50/p90/p99 totals and catastrophic event
    descriptions.
    """
    base_annual = sum(annual["domain_annual"].values())
    n_years_int = max(int(math.ceil(n_years)), 1)

    # Determine risk parameters for catastrophic events.
    risk_flags = annual["risk_flags"]

    # Incarceration probability per year.
    if risk_flags.get("justice_involvement"):
        p_incarceration = min(0.15 + key.past_12m_police_contacts * 0.03, 0.40)
    elif risk_flags.get("justice_history"):
        p_incarceration = 0.05
    else:
        p_incarceration = float(POPULATION_BASELINES["incarceration_rate_per_100k"]) / 100_000.0

    # Hospitalization probability per year.
    hc_mult = annual["healthcare_multiplier"]
    p_hospitalization = min(0.04 * hc_mult, 0.35)
    if risk_flags.get("high_need"):
        p_hospitalization = min(p_hospitalization * 1.5, 0.45)

    # Homelessness probability per year.
    if risk_flags.get("currently_homeless"):
        p_homelessness = 0.60  # probability of remaining / cycling
    elif risk_flags.get("homelessness_risk"):
        p_homelessness = 0.15
    else:
        p_homelessness = 0.005

    # Cost of each catastrophic event.
    cost_incarceration = _JUSTICE_COST_MID
    cost_hospitalization = float(UNIT_COSTS["inpatient_day"]) * 14.0  # 14-day stay
    cost_homelessness = _HOMELESSNESS_COST_MID

    # --- Simulation ---
    # Shape: (iterations, n_years_int)
    # Base cost with log-normal noise (CV ~20%).
    log_sigma = 0.20
    log_mu = math.log(base_annual) - 0.5 * log_sigma ** 2
    yearly_base = rng.lognormal(mean=log_mu, sigma=log_sigma, size=(iterations, n_years_int))

    # Catastrophic event draws.
    incarceration_draws = rng.random(size=(iterations, n_years_int)) < p_incarceration
    hospitalization_draws = rng.random(size=(iterations, n_years_int)) < p_hospitalization
    homelessness_draws = rng.random(size=(iterations, n_years_int)) < p_homelessness

    # Catastrophic costs (with some variance).
    incarceration_costs = incarceration_draws * rng.uniform(
        _JUSTICE_COST_MIN, _JUSTICE_COST_MAX, size=(iterations, n_years_int)
    )
    hospitalization_costs = hospitalization_draws * rng.uniform(
        cost_hospitalization * 0.5, cost_hospitalization * 2.0, size=(iterations, n_years_int)
    )
    homelessness_costs = homelessness_draws * rng.uniform(
        _HOMELESSNESS_COST_MIN, _HOMELESSNESS_COST_MAX, size=(iterations, n_years_int)
    )

    # Discount each year to present value.
    discount_factors = np.array([
        _discount_factor(y) for y in range(n_years_int)
    ])  # shape (n_years_int,)

    total_costs = (
        yearly_base
        + incarceration_costs
        + hospitalization_costs
        + homelessness_costs
    )
    # Apply discount factors across years.
    pv_costs = total_costs * discount_factors[np.newaxis, :]

    # Sum across years for each iteration.
    lifetime_pv = pv_costs.sum(axis=1)  # shape (iterations,)

    p50 = float(np.percentile(lifetime_pv, 50))
    p90 = float(np.percentile(lifetime_pv, 90))
    p99 = float(np.percentile(lifetime_pv, 99))

    # Build catastrophic event risk summaries.
    cat_events: list[CatastrophicEventRisk] = []

    # Incarceration event.
    prob_any_incarceration = 1.0 - (1.0 - p_incarceration) ** n_years_int
    if prob_any_incarceration > 0.001:
        cat_events.append(CatastrophicEventRisk(
            event_type="incarceration",
            probability=round(min(prob_any_incarceration, 1.0), 4),
            expected_incremental_cost=round(cost_incarceration, 2),
            payer_distribution=[
                PayerBreakdown(payer_level="state", payer_entity="State Corrections",
                               expected_spend=round(cost_incarceration * 0.50, 2)),
                PayerBreakdown(payer_level="local", payer_entity="County Jail",
                               expected_spend=round(cost_incarceration * 0.30, 2)),
                PayerBreakdown(payer_level="local", payer_entity="Local Police",
                               expected_spend=round(cost_incarceration * 0.20, 2)),
            ],
        ))

    # Hospitalization event (prolonged stay / ICU).
    prob_any_hospitalization = 1.0 - (1.0 - p_hospitalization) ** n_years_int
    if prob_any_hospitalization > 0.001:
        cat_events.append(CatastrophicEventRisk(
            event_type="prolonged_hospitalization",
            probability=round(min(prob_any_hospitalization, 1.0), 4),
            expected_incremental_cost=round(cost_hospitalization, 2),
            payer_distribution=[
                PayerBreakdown(payer_level="federal", payer_entity="CMS-Medicaid",
                               expected_spend=round(cost_hospitalization * 0.40, 2)),
                PayerBreakdown(payer_level="federal", payer_entity="CMS-Medicare",
                               expected_spend=round(cost_hospitalization * 0.30, 2)),
                PayerBreakdown(payer_level="health_system",
                               payer_entity="Hospital Uncompensated Care",
                               expected_spend=round(cost_hospitalization * 0.20, 2)),
                PayerBreakdown(payer_level="state", payer_entity="State Medicaid Match",
                               expected_spend=round(cost_hospitalization * 0.10, 2)),
            ],
        ))

    # Homelessness episode.
    prob_any_homelessness = 1.0 - (1.0 - p_homelessness) ** n_years_int
    if prob_any_homelessness > 0.001:
        cat_events.append(CatastrophicEventRisk(
            event_type="homelessness_episode",
            probability=round(min(prob_any_homelessness, 1.0), 4),
            expected_incremental_cost=round(cost_homelessness, 2),
            payer_distribution=[
                PayerBreakdown(payer_level="local", payer_entity="Homeless Services",
                               expected_spend=round(cost_homelessness * 0.40, 2)),
                PayerBreakdown(payer_level="federal", payer_entity="HUD",
                               expected_spend=round(cost_homelessness * 0.30, 2)),
                PayerBreakdown(payer_level="state", payer_entity="State DHS",
                               expected_spend=round(cost_homelessness * 0.20, 2)),
                PayerBreakdown(payer_level="health_system",
                               payer_entity="Hospital ER",
                               expected_spend=round(cost_homelessness * 0.10, 2)),
            ],
        ))

    return RiskProfile(
        p50_total_cost=round(p50, 2),
        p90_total_cost=round(p90, 2),
        p99_total_cost=round(p99, 2),
        catastrophic_events=cat_events,
    )


# ---------------------------------------------------------------------------
# Scenario generator
# ---------------------------------------------------------------------------

_INTERVENTION_EFFECTS: dict[str, dict[str, float]] = {
    "housing_first": {
        "housing": -0.60,
        "healthcare": -0.40,
        "justice": -0.30,
    },
    "CBT": {
        "healthcare": -0.20,
        "income_support": -0.15,
    },
    "income_bridge": {
        "income_support": -0.40,
        "housing": -0.20,
        "food": -0.30,
    },
    "MAT": {
        "healthcare": -0.50,
        "justice": -0.40,
    },
    "supported_employment": {
        "income_support": -0.60,
        "housing": -0.20,
    },
    "care_coordination": {
        "healthcare": -0.30,
    },
    "reentry_services": {
        "justice": -0.50,
        "housing": -0.20,
        "income_support": -0.20,
    },
}

_INTERVENTION_COSTS: dict[str, float] = {
    "housing_first": 22_000.0,
    "CBT": 6_000.0,
    "income_bridge": 12_000.0,
    "MAT": 8_500.0,
    "supported_employment": 15_000.0,
    "care_coordination": 5_000.0,
    "reentry_services": 10_000.0,
}


def _generate_scenarios(
    key: PersonBudgetKey,
    annual: dict[str, Any],
    n_years: float,
    baseline_total: float,
) -> list[ScenarioBudget]:
    """Generate intervention scenarios based on person risk flags.

    Only generates scenarios for interventions relevant to the person's risk
    profile.
    """
    risk_flags = annual["risk_flags"]
    domain_annual = annual["domain_annual"]
    scenarios: list[ScenarioBudget] = []

    # Determine which interventions are relevant.
    relevant: list[str] = []
    if risk_flags.get("currently_homeless") or risk_flags.get("homelessness_risk"):
        relevant.append("housing_first")
    if risk_flags.get("depression") or risk_flags.get("high_need"):
        relevant.append("CBT")
    if key.current_annual_income is not None and key.current_annual_income < 25_000:
        relevant.append("income_bridge")
    if risk_flags.get("sud"):
        relevant.append("MAT")
    if key.employment_status in ("unemployed", "disabled"):
        relevant.append("supported_employment")
    if len(risk_flags) >= 3:  # multi-system complexity
        relevant.append("care_coordination")
    if risk_flags.get("justice_involvement") or risk_flags.get("justice_history"):
        relevant.append("reentry_services")

    # Always include at least care_coordination if no other interventions matched.
    if not relevant:
        relevant.append("care_coordination")

    for intervention_name in relevant:
        effects = _INTERVENTION_EFFECTS.get(intervention_name, {})
        intervention_cost_annual = _INTERVENTION_COSTS.get(intervention_name, 5_000.0)
        total_intervention_cost = intervention_cost_annual * min(n_years, 5.0)

        # Calculate savings by domain.
        total_savings = 0.0
        savings_by_payer: list[PayerBreakdown] = []

        for domain_name, reduction_pct in effects.items():
            domain_spend = domain_annual.get(domain_name, 0.0) * n_years
            saving = abs(reduction_pct) * domain_spend
            total_savings += saving

        # Distribute savings across payers.
        if total_savings > 0:
            savings_by_payer = [
                PayerBreakdown(
                    payer_level="federal",
                    payer_entity="Federal Programs",
                    expected_spend=round(total_savings * 0.45, 2),
                ),
                PayerBreakdown(
                    payer_level="state",
                    payer_entity="State Programs",
                    expected_spend=round(total_savings * 0.30, 2),
                ),
                PayerBreakdown(
                    payer_level="local",
                    payer_entity="Local Services",
                    expected_spend=round(total_savings * 0.15, 2),
                ),
                PayerBreakdown(
                    payer_level="health_system",
                    payer_entity="Hospitals",
                    expected_spend=round(total_savings * 0.07, 2),
                ),
                PayerBreakdown(
                    payer_level="nonprofit",
                    payer_entity="Nonprofits",
                    expected_spend=round(total_savings * 0.03, 2),
                ),
            ]

        net_savings = total_savings - total_intervention_cost
        new_total = baseline_total - total_savings + total_intervention_cost

        scenarios.append(ScenarioBudget(
            scenario_id=f"scenario_{intervention_name}",
            description=(
                f"Apply {intervention_name.replace('_', ' ').title()} intervention "
                f"over {min(n_years, 5.0):.0f} years"
            ),
            incremental_cost_of_scenario=round(total_intervention_cost, 2),
            expected_total_cost_under_scenario=round(new_total, 2),
            expected_savings_vs_baseline=round(net_savings, 2),
            savings_by_payer=savings_by_payer,
        ))

    return scenarios


# ===========================================================================
# BudgetEngine -- the public API
# ===========================================================================

class BudgetEngine:
    """Whole-Person Budget engine -- THE SKELETON KEY.

    Given a ``PersonBudgetKey`` and historical ``FiscalEvent`` list, produces
    a ``WholePersonBudget`` with per-horizon projections of cost, broken down
    by payer, domain, mechanism, and risk quantile.  Optionally generates
    intervention-vs-baseline scenarios.

    Parameters
    ----------
    seed : int | None
        Random seed for reproducibility of Monte Carlo simulations.
        If ``None``, a non-deterministic seed is used.
    generate_scenarios : bool
        If ``True`` (default), attach intervention scenario projections to
        each horizon budget.

    Examples
    --------
    >>> engine = BudgetEngine(seed=42)
    >>> budget = engine.compute(budget_key, fiscal_history, iterations=2000)
    >>> budget.horizons[0].risk_profile.p50_total_cost
    45230.17
    """

    def __init__(
        self,
        seed: int | None = None,
        generate_scenarios: bool = True,
    ) -> None:
        self._rng = np.random.default_rng(seed)
        self._generate_scenarios = generate_scenarios

    # ----- public ----------------------------------------------------------

    def compute(
        self,
        budget_key: PersonBudgetKey,
        fiscal_history: list[FiscalEvent],
        iterations: int = 1000,
    ) -> WholePersonBudget:
        """Compute the Whole-Person Budget.

        Parameters
        ----------
        budget_key : PersonBudgetKey
            All person-level inputs the engine needs.
        fiscal_history : list[FiscalEvent]
            Historical fiscal events for this person.
        iterations : int
            Number of Monte Carlo iterations (default 1,000).

        Returns
        -------
        WholePersonBudget
            Multi-horizon budget projection.
        """
        # Step (a): aggregate historical spend.
        history_agg = _aggregate_history(fiscal_history)

        # Step (b): compute risk-adjusted annual costs.
        annual = _compute_annual_costs(budget_key)

        # Blend historical data when available.
        # If we have historical data, weight it 30% for the projection
        # (recent actuals inform the forecast).
        if history_agg["domain"]:
            history_years = self._estimate_history_span(fiscal_history)
            if history_years > 0:
                for domain_name in _DOMAINS:
                    hist_annual = history_agg["domain"].get(domain_name, 0.0) / history_years
                    model_annual = annual["domain_annual"].get(domain_name, 0.0)
                    # Weighted blend: 30% historical, 70% model.
                    blended = 0.30 * hist_annual + 0.70 * model_annual
                    annual["domain_annual"][domain_name] = blended

        # Determine remaining life expectancy for "lifetime" horizon.
        remaining_life = max(_LIFE_EXPECTANCY - budget_key.age, 1.0)

        # Default horizons if none specified.
        horizons_to_compute = budget_key.budget_horizons
        if not horizons_to_compute:
            today = date.today()
            horizons_to_compute = [
                BudgetHorizon(label="1y", start_date=today,
                              end_date=date(today.year + 1, today.month, today.day),
                              time_step="month"),
                BudgetHorizon(label="5y", start_date=today,
                              end_date=date(today.year + 5, today.month, today.day),
                              time_step="quarter"),
                BudgetHorizon(label="20y", start_date=today,
                              end_date=date(today.year + 20, today.month, today.day),
                              time_step="year"),
                BudgetHorizon(label="lifetime", start_date=today,
                              end_date=date(today.year + int(remaining_life),
                                            today.month, today.day),
                              time_step="year"),
            ]

        # Step (c): build each horizon.
        horizon_budgets: list[HorizonBudget] = []
        for hz in horizons_to_compute:
            hb = self._build_horizon(
                budget_key, annual, hz, remaining_life, iterations,
            )
            horizon_budgets.append(hb)

        return WholePersonBudget(
            person_uid=budget_key.person_uid,
            generated_at=datetime.now(timezone.utc),
            horizons=horizon_budgets,
        )

    # ----- private ---------------------------------------------------------

    def _build_horizon(
        self,
        key: PersonBudgetKey,
        annual: dict[str, Any],
        horizon: BudgetHorizon,
        remaining_life: float,
        iterations: int,
    ) -> HorizonBudget:
        """Build a single ``HorizonBudget``."""
        # Determine number of years for this horizon.
        label_years = _HORIZON_YEARS.get(horizon.label)
        if label_years is None:
            # Lifetime: use remaining life expectancy.
            n_years = remaining_life
        else:
            n_years = label_years

        # Cap at remaining life.
        n_years = min(n_years, remaining_life)

        # Compute NPV-adjusted total for payer view.
        total_annual = sum(annual["domain_annual"].values())
        npv_total = _npv_annuity(total_annual, n_years)
        nominal_total = total_annual * n_years

        # Use nominal for simplicity in breakdowns (NPV in risk profile).
        fed_spend = annual["federal_annual"] * n_years
        state_spend = annual["state_annual"] * n_years
        local_spend = annual["local_annual"] * n_years
        hc_delivery_spend = annual["healthcare_delivery_annual"] * n_years
        nonprofit_spend = annual["nonprofit_annual"] * n_years

        payer_view = PayerView(
            federal_expected_spend=round(fed_spend, 2),
            state_expected_spend=round(state_spend, 2),
            local_expected_spend=round(local_spend, 2),
            healthcare_delivery_expected_spend=round(hc_delivery_spend, 2),
            nonprofit_expected_spend=round(nonprofit_spend, 2),
            per_payer_breakdown=_build_payer_breakdowns(key, annual, n_years),
        )

        domain_view = _build_domain_budgets(key, annual, n_years)

        mechanism_view = [
            MechanismBudget(
                mechanism=mech,
                expected_spend=round(annual["mechanism_annual"].get(mech, 0.0) * n_years, 2),
            )
            for mech in _MECHANISMS
        ]

        risk_profile = _run_monte_carlo(key, annual, n_years, iterations, self._rng)

        scenarios: list[ScenarioBudget] | None = None
        if self._generate_scenarios:
            scenarios = _generate_scenarios(key, annual, n_years, nominal_total)

        return HorizonBudget(
            label=horizon.label,
            start_date=horizon.start_date,
            end_date=horizon.end_date,
            payer_view=payer_view,
            domain_view=domain_view,
            mechanism_view=mechanism_view,
            risk_profile=risk_profile,
            scenarios=scenarios if scenarios else None,
        )

    @staticmethod
    def _estimate_history_span(fiscal_history: list[FiscalEvent]) -> float:
        """Estimate the number of years covered by the fiscal history."""
        if not fiscal_history:
            return 0.0
        dates = [evt.event_date for evt in fiscal_history]
        earliest = min(dates)
        latest = max(dates)
        span_days = (latest - earliest).days
        return max(span_days / 365.25, 0.5)  # at least half a year if any data
