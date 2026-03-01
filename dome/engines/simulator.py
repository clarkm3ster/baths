"""
Monte Carlo Whole-Life Simulator (Step 11)
==========================================

Simulates a person's lifetime costs under two scenarios:

- **Path A (No DOME)**: Natural cascade progression with no coordinated
  intervention.  Each year, stochastic events (job loss, disease progression,
  recidivism, etc.) are drawn according to the person's risk profile, and
  cascade transitions fire at their base probabilities.

- **Path B (DOME Active)**: Same stochastic event model, but at each cascade
  trigger point the DOME system applies the best available intervention.
  If the intervention succeeds (Bernoulli draw at break_probability), the
  cascade halts and only the intervention cost is incurred.  If it fails,
  the cascade continues with 50% severity attenuation.

All random draws use numpy for vectorized performance.

Usage::

    from dome.engines.simulator import LifeSimulator
    sim = LifeSimulator(seed=42)
    result = sim.simulate(person_state, budget_key, fiscal_history,
                          iterations=1000, projection_years=50)
    print(result.dome_roi)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import numpy as np

from dome.data.cascades import CASCADE_DEFINITIONS
from dome.data.interventions import INTERVENTION_INDEX
from dome.data.unit_costs import UNIT_COSTS
from dome.models.budget_key import PersonBudgetKey
from dome.models.dome_metrics import DomeMetrics
from dome.models.fiscal_event import FiscalEvent


# ---------------------------------------------------------------------------
# Result container
# ---------------------------------------------------------------------------

@dataclass
class SimulationResult:
    """Output of a Monte Carlo whole-life simulation.

    Attributes
    ----------
    path_a_costs : list[float]
        Total lifetime cost per iteration under Path A (no intervention).
    path_b_costs : list[float]
        Total lifetime cost per iteration under Path B (DOME active).
    dome_costs : list[float]
        Total DOME intervention + overhead cost per iteration.
    path_a_median, path_a_p90, path_a_p99 : float
        Summary statistics for Path A cost distribution.
    path_b_median, path_b_p90, path_b_p99 : float
        Summary statistics for Path B cost distribution.
    dome_cost_total : float
        Median total DOME cost (intervention + overhead).
    dome_roi : float
        (median_path_a - median_path_b - dome_cost) / dome_cost.
    year_by_year_path_a : list[list[float]]
        Cost matrix [iterations x years] for Path A.
    year_by_year_path_b : list[list[float]]
        Cost matrix [iterations x years] for Path B.
    iterations_run : int
        Number of iterations executed.
    """

    path_a_costs: list[float] = field(default_factory=list)
    path_b_costs: list[float] = field(default_factory=list)
    dome_costs: list[float] = field(default_factory=list)
    path_a_median: float = 0.0
    path_a_p90: float = 0.0
    path_a_p99: float = 0.0
    path_b_median: float = 0.0
    path_b_p90: float = 0.0
    path_b_p99: float = 0.0
    dome_cost_total: float = 0.0
    dome_roi: float = 0.0
    iterations_run: int = 0
    year_by_year_path_a: list[list[float]] = field(default_factory=list)
    year_by_year_path_b: list[list[float]] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

_DOME_OVERHEAD_LOW = 2_000.0
_DOME_OVERHEAD_HIGH = 5_000.0
_DOME_BREAK_PROB_DEFAULT = 0.55
_DOME_SEVERITY_REDUCTION = 0.50
_DISCOUNT_RATE = 0.03
_MAX_AGE = 85


# ---------------------------------------------------------------------------
# Cascade-event annual probabilities
# ---------------------------------------------------------------------------

def _prob_job_loss(employed: bool, income_volatility: float,
                   education: str) -> float:
    """Annual probability of job loss."""
    if not employed:
        return 0.0
    base = 0.04
    base += income_volatility * 0.15
    base += {"<HS": 0.03, "HS": 0.02, "some_college": 0.01}.get(education, 0.0)
    return min(base, 0.30)


def _prob_depression(already_depressed: bool, unemployed: bool,
                     homeless: bool, justice: bool) -> float:
    """Annual probability of depression onset."""
    if already_depressed:
        return 0.0
    base = 0.07
    if unemployed:
        base += 0.15
    if homeless:
        base += 0.10
    if justice:
        base += 0.08
    return min(base, 0.50)


def _prob_chronic(depressed: bool, n_chronic: int, age: int) -> float:
    """Annual probability of new chronic condition."""
    base = 0.02
    if depressed:
        base += 0.04
    base += n_chronic * 0.03
    base += max(0.0, (age - 30) * 0.002)
    return min(base, 0.30)


def _prob_hospitalization(n_chronic: int, has_sud: bool,
                          homeless: bool, age: int) -> float:
    """Annual probability of hospitalization."""
    base = 0.07
    base += n_chronic * 0.05
    if has_sud:
        base += 0.08
    if homeless:
        base += 0.06
    base += max(0.0, (age - 50) * 0.005)
    return min(base, 0.50)


def _prob_homelessness(already_homeless: bool, unemployed: bool,
                       has_sud: bool, depressed: bool,
                       justice: bool) -> float:
    """Annual probability of becoming homeless."""
    if already_homeless:
        return 0.0
    base = 0.003
    if unemployed:
        base += 0.02
    if has_sud:
        base += 0.03
    if depressed:
        base += 0.02
    if justice:
        base += 0.04
    return min(base, 0.20)


def _prob_recidivism(justice_involved: bool, years_since: int,
                     has_sud: bool, homeless: bool,
                     employed: bool) -> float:
    """Annual probability of re-incarceration.

    Base rate 44% within first year, declining by ~35% per year.
    """
    if not justice_involved:
        return 0.0
    if years_since <= 0:
        base = 0.44
    else:
        base = 0.44 * (0.65 ** years_since)
    if has_sud:
        base *= 1.4
    if homeless:
        base *= 1.3
    if not employed:
        base *= 1.2
    return min(base, 0.60)


def _prob_substance_onset(already_sud: bool, depressed: bool,
                          justice: bool, poverty: bool) -> float:
    """Annual probability of SUD onset."""
    if already_sud:
        return 0.0
    base = 0.02
    if depressed:
        base += 0.06
    if justice:
        base += 0.04
    if poverty:
        base += 0.02
    return min(base, 0.25)


# ---------------------------------------------------------------------------
# Year cost computation
# ---------------------------------------------------------------------------

def _age_multiplier(age: int) -> float:
    """Cost multiplier by age bracket."""
    if age < 18:
        return 0.6
    if age < 30:
        return 0.7
    if age < 50:
        return 1.0
    if age < 65:
        return 1.3
    if age < 75:
        return 2.0
    return 2.8


def _compute_year_cost(
    employed: bool, depressed: bool, has_chronic: bool,
    n_chronic: int, hospitalized: bool, homeless: bool,
    incarcerated: bool, has_sud: bool, disabled: bool, age: int,
) -> float:
    """Compute total public cost for one year given state flags."""
    cost = 8_000.0 * _age_multiplier(age)

    if not employed:
        cost += UNIT_COSTS.get("unemployment_insurance_weekly", 380) * 26
        cost += UNIT_COSTS.get("snap_per_person_annual", 3_300)

    if depressed:
        cost += UNIT_COSTS.get("mental_health_session", 175) * 24
        cost += UNIT_COSTS.get("prescription_monthly", 150) * 12

    if has_chronic:
        cost += UNIT_COSTS.get("outpatient_visit", 350) * 6 * n_chronic
        cost += UNIT_COSTS.get("prescription_monthly", 150) * 12 * n_chronic
        cost += UNIT_COSTS.get("er_visit", 2_200) * max(1, n_chronic)

    if hospitalized:
        cost += UNIT_COSTS.get("inpatient_day", 2_883) * 5
        cost += UNIT_COSTS.get("er_visit", 2_200)

    if homeless:
        cost += UNIT_COSTS.get("shelter_night", 103.50) * 200
        cost += UNIT_COSTS.get("er_visit", 2_200) * 4
        cost += UNIT_COSTS.get("mental_health_session", 175) * 12

    if incarcerated:
        cost += UNIT_COSTS.get("jail_day", 160) * 180
        cost += UNIT_COSTS.get("er_visit", 2_200)

    if has_sud:
        cost += UNIT_COSTS.get("substance_abuse_treatment_day", 200) * 90
        cost += UNIT_COSTS.get("er_visit", 2_200) * 2

    if disabled:
        cost += UNIT_COSTS.get("ssdi_annual", 21_000)
        cost += UNIT_COSTS.get("medicaid_per_disabled_annual", 22_000) * 0.5

    return cost


# ---------------------------------------------------------------------------
# Intervention lookup
# ---------------------------------------------------------------------------

def _best_intervention(cause: str, effect: str) -> tuple[float, float]:
    """Return (break_probability, midpoint_cost) for best intervention."""
    label = f"{cause}->{effect}"
    intvs = INTERVENTION_INDEX.get(label, [])
    if not intvs:
        return (0.0, 0.0)
    best = max(intvs, key=lambda i: i.break_probability)
    return (best.break_probability, (best.cost_min + best.cost_max) / 2.0)


# ---------------------------------------------------------------------------
# Engine
# ---------------------------------------------------------------------------

class LifeSimulator:
    """Monte Carlo whole-life simulator comparing Path A vs Path B.

    Parameters
    ----------
    seed : int or None
        Random seed for reproducibility.
    """

    def __init__(self, seed: int | None = None) -> None:
        self._rng = np.random.default_rng(seed)
        self._intv_cache: dict[str, tuple[float, float]] = {}
        for cdef in CASCADE_DEFINITIONS:
            for link in cdef.links:
                key = f"{link.cause}->{link.effect}"
                if key not in self._intv_cache:
                    self._intv_cache[key] = _best_intervention(
                        link.cause, link.effect
                    )

    def simulate(
        self,
        person_state: Any,
        budget_key: PersonBudgetKey,
        fiscal_history: list[FiscalEvent | dict],
        dome_metrics: DomeMetrics | None = None,
        iterations: int = 1000,
        projection_years: int = 50,
    ) -> SimulationResult:
        """Run the full Path A vs Path B Monte Carlo simulation.

        Parameters
        ----------
        person_state
            Current dynamic state or budget key (used for supplemental
            info; budget_key is the primary input).
        budget_key
            Person's budget key with demographics and risk flags.
        fiscal_history
            Historical fiscal events (used for baseline cost calibration).
        dome_metrics
            Optional DOME metrics for richer risk profiling.
        iterations
            Number of Monte Carlo iterations (default 1,000).
        projection_years
            How many years to project forward (default 50).

        Returns
        -------
        SimulationResult
            Complete simulation output with per-iteration costs and
            summary statistics.
        """
        current_age = budget_key.age
        max_age = min(current_age + projection_years, _MAX_AGE)
        n_years = max(max_age - current_age, 1)

        # Extract initial state from budget key
        employed_init = budget_key.employment_status not in (
            "unemployed", "NILF", "disabled",
        )
        depressed_init = False
        if dome_metrics is not None:
            phq = dome_metrics.clinical_layer.get("depression_severity", 0) or 0
            dep_s = dome_metrics.behavioral_layer.get("depression_score", 0) or 0
            depressed_init = phq > 10 or dep_s > 0.5
        has_chronic_init = len(budget_key.chronic_condition_flags) > 0
        n_chronic_init = len(budget_key.chronic_condition_flags)
        has_sud_init = False
        if dome_metrics is not None:
            sud_s = dome_metrics.behavioral_layer.get("sud_severity", 0) or 0
            has_sud_init = sud_s > 0.4
        homeless_init = budget_key.housing_status in (
            "shelter", "street", "doubled_up",
        )
        justice_init = budget_key.justice_involvement_flag
        disabled = budget_key.disability_flag
        poverty_init = (budget_key.current_annual_income or 0) < 15_000
        education = budget_key.educational_attainment
        income_vol = budget_key.income_volatility_score or 0.2

        # Pre-generate random draws for all iterations and years
        rng = self._rng
        u_jl = rng.random((iterations, n_years))
        u_dep = rng.random((iterations, n_years))
        u_chr = rng.random((iterations, n_years))
        u_hosp = rng.random((iterations, n_years))
        u_hom = rng.random((iterations, n_years))
        u_rec = rng.random((iterations, n_years))
        u_sud = rng.random((iterations, n_years))
        u_brk = rng.random((iterations, n_years))
        u_overhead = rng.uniform(
            _DOME_OVERHEAD_LOW, _DOME_OVERHEAD_HIGH,
            size=(iterations, n_years),
        )

        # Allocate output arrays
        costs_a = np.zeros((iterations, n_years), dtype=np.float64)
        costs_b = np.zeros((iterations, n_years), dtype=np.float64)
        dome_total = np.zeros(iterations, dtype=np.float64)

        # Run iterations
        for it in range(iterations):
            self._run_iteration(
                it, n_years, current_age,
                employed_init, depressed_init, has_chronic_init,
                n_chronic_init, has_sud_init, homeless_init,
                justice_init, disabled, poverty_init, education,
                income_vol,
                u_jl, u_dep, u_chr, u_hosp, u_hom, u_rec, u_sud,
                u_brk, u_overhead,
                costs_a, costs_b, dome_total,
            )

        # Apply NPV discounting
        disc = np.array(
            [1.0 / (1 + _DISCOUNT_RATE) ** y for y in range(n_years)],
            dtype=np.float64,
        )
        costs_a_npv = costs_a * disc[np.newaxis, :]
        costs_b_npv = costs_b * disc[np.newaxis, :]

        totals_a = costs_a_npv.sum(axis=1)
        totals_b = costs_b_npv.sum(axis=1)

        pa_med = float(np.median(totals_a))
        pa_90 = float(np.percentile(totals_a, 90))
        pa_99 = float(np.percentile(totals_a, 99))
        pb_med = float(np.median(totals_b))
        pb_90 = float(np.percentile(totals_b, 90))
        pb_99 = float(np.percentile(totals_b, 99))
        dc_total = float(np.median(dome_total))

        roi = (pa_med - pb_med - dc_total) / dc_total if dc_total > 0 else 0.0

        return SimulationResult(
            path_a_costs=totals_a.tolist(),
            path_b_costs=totals_b.tolist(),
            dome_costs=dome_total.tolist(),
            path_a_median=round(pa_med, 2),
            path_a_p90=round(pa_90, 2),
            path_a_p99=round(pa_99, 2),
            path_b_median=round(pb_med, 2),
            path_b_p90=round(pb_90, 2),
            path_b_p99=round(pb_99, 2),
            dome_cost_total=round(dc_total, 2),
            dome_roi=round(roi, 4),
            iterations_run=iterations,
            year_by_year_path_a=costs_a_npv.tolist(),
            year_by_year_path_b=costs_b_npv.tolist(),
        )

    # ------------------------------------------------------------------ #
    # Single iteration
    # ------------------------------------------------------------------ #

    def _run_iteration(
        self, it: int, n_years: int, start_age: int,
        employed_init: bool, depressed_init: bool,
        has_chronic_init: bool, n_chronic_init: int,
        has_sud_init: bool, homeless_init: bool,
        justice_init: bool, disabled: bool,
        poverty_init: bool, education: str, income_vol: float,
        u_jl: np.ndarray, u_dep: np.ndarray, u_chr: np.ndarray,
        u_hosp: np.ndarray, u_hom: np.ndarray, u_rec: np.ndarray,
        u_sud: np.ndarray, u_brk: np.ndarray, u_overhead: np.ndarray,
        costs_a: np.ndarray, costs_b: np.ndarray,
        dome_total: np.ndarray,
    ) -> None:
        """Simulate one iteration for both paths."""
        # ---- Path A state ----
        a_emp = employed_init
        a_dep = depressed_init
        a_chr = has_chronic_init
        a_nc = n_chronic_init
        a_sud = has_sud_init
        a_hom = homeless_init
        a_inc = False
        a_ysr = 1 if justice_init else 100  # years since release

        # ---- Path B state ----
        b_emp = employed_init
        b_dep = depressed_init
        b_chr = has_chronic_init
        b_nc = n_chronic_init
        b_sud = has_sud_init
        b_hom = homeless_init
        b_inc = False
        b_ysr = 1 if justice_init else 100

        d_cost = 0.0  # accumulated dome cost

        for yr in range(n_years):
            age = start_age + yr
            intv_cost = 0.0

            # ============================================================
            # PATH A: no intervention
            # ============================================================

            # Job loss
            if a_emp and u_jl[it, yr] < _prob_job_loss(
                    a_emp, income_vol, education):
                a_emp = False

            # Depression
            if not a_dep and u_dep[it, yr] < _prob_depression(
                    a_dep, not a_emp, a_hom, justice_init):
                a_dep = True

            # Chronic disease
            if u_chr[it, yr] < _prob_chronic(a_dep, a_nc, age):
                a_chr = True
                a_nc += 1

            # Hospitalization
            a_hosp = u_hosp[it, yr] < _prob_hospitalization(
                a_nc, a_sud, a_hom, age)

            # Homelessness
            if not a_hom and u_hom[it, yr] < _prob_homelessness(
                    a_hom, not a_emp, a_sud, a_dep, justice_init):
                a_hom = True

            # Recidivism
            a_inc = False
            if justice_init and a_ysr < 100:
                if u_rec[it, yr] < _prob_recidivism(
                        True, a_ysr, a_sud, a_hom, a_emp):
                    a_inc = True
                    a_ysr = 0
                else:
                    a_ysr += 1

            # SUD onset
            if not a_sud and u_sud[it, yr] < _prob_substance_onset(
                    a_sud, a_dep, justice_init, not a_emp):
                a_sud = True

            costs_a[it, yr] = _compute_year_cost(
                a_emp, a_dep, a_chr, a_nc, a_hosp,
                a_hom, a_inc, a_sud, disabled, age,
            )

            # ============================================================
            # PATH B: DOME active
            # ============================================================

            # Job loss -- DOME applies income bridge
            b_jl_event = False
            if b_emp and u_jl[it, yr] < _prob_job_loss(
                    b_emp, income_vol, education):
                b_jl_event = True
                bp, cost = self._intv_cache.get(
                    "job_loss->depression", (0, 0))
                if bp > 0:
                    intv_cost += cost
                b_emp = False  # job still lost
                # But intervention may prevent depression below

            # Depression -- DOME applies CBT / treatment
            if not b_dep and u_dep[it, yr] < _prob_depression(
                    b_dep, not b_emp, b_hom, justice_init):
                if b_jl_event:
                    bp, cost = self._intv_cache.get(
                        "job_loss->depression", (0, 0))
                    if bp > 0 and u_brk[it, yr] < bp:
                        pass  # cascade broken, depression prevented
                    else:
                        b_dep = True
                        bp2, c2 = self._intv_cache.get(
                            "depression->chronic_disease", (0, 0))
                        if bp2 > 0:
                            intv_cost += c2
                else:
                    b_dep = True
                    bp2, c2 = self._intv_cache.get(
                        "social_isolation->depression", (0, 0))
                    if bp2 > 0:
                        intv_cost += c2

            # Chronic disease -- DOME manages chronic care
            if u_chr[it, yr] < _prob_chronic(b_dep, b_nc, age):
                bp, cost = self._intv_cache.get(
                    "chronic_disease->high_utilization", (0, 0))
                if bp > 0:
                    intv_cost += cost
                b_chr = True
                b_nc += 1

            # Hospitalization (30% reduction from care coordination)
            b_hosp_prob = _prob_hospitalization(
                b_nc, b_sud, b_hom, age) * 0.7
            b_hosp = u_hosp[it, yr] < b_hosp_prob

            # Homelessness -- DOME provides housing intervention
            if not b_hom and u_hom[it, yr] < _prob_homelessness(
                    b_hom, not b_emp, b_sud, b_dep, justice_init):
                bp, cost = self._intv_cache.get(
                    "housing_instability->health_deterioration", (0, 0))
                if bp > 0:
                    intv_cost += cost
                if bp > 0 and u_brk[it, yr] < bp:
                    pass  # housing intervention prevents homelessness
                else:
                    b_hom = True

            # Recidivism -- DOME provides reentry services
            b_inc = False
            if justice_init and b_ysr < 100:
                if u_rec[it, yr] < _prob_recidivism(
                        True, b_ysr, b_sud, b_hom, b_emp):
                    bp, cost = self._intv_cache.get(
                        "incarceration->employment_barrier", (0, 0))
                    if bp > 0:
                        intv_cost += cost
                    if bp > 0 and u_brk[it, yr] < bp:
                        b_ysr += 1  # diversion succeeds
                    else:
                        b_inc = True
                        b_ysr = 0
                else:
                    b_ysr += 1

            # SUD -- DOME provides MAT
            if not b_sud and u_sud[it, yr] < _prob_substance_onset(
                    b_sud, b_dep, justice_init, not b_emp):
                bp, cost = self._intv_cache.get(
                    "substance_use->medical_crisis", (0, 0))
                if bp > 0:
                    intv_cost += cost
                if bp > 0 and u_brk[it, yr] < bp:
                    pass  # SUD prevented
                else:
                    b_sud = True

            # Compute base Path B cost
            b_year = _compute_year_cost(
                b_emp, b_dep, b_chr, b_nc, b_hosp,
                b_hom, b_inc, b_sud, disabled, age,
            )

            # Apply 50% severity reduction for DOME-managed conditions
            conditions_managed = sum([b_dep, b_chr, b_sud, b_hom])
            if conditions_managed > 0:
                baseline = 8_000.0 * _age_multiplier(age)
                incremental = max(0.0, b_year - baseline)
                b_year = baseline + incremental * _DOME_SEVERITY_REDUCTION

            overhead = u_overhead[it, yr]
            costs_b[it, yr] = b_year + intv_cost + overhead
            d_cost += intv_cost + overhead

        dome_total[it] = d_cost

    # ------------------------------------------------------------------ #
    # Static summary helper
    # ------------------------------------------------------------------ #

    @staticmethod
    def summarize(result: SimulationResult) -> dict[str, Any]:
        """Return a JSON-serializable summary of a simulation result."""
        arr_a = np.array(result.path_a_costs)
        arr_b = np.array(result.path_b_costs)
        return {
            "iterations": result.iterations_run,
            "path_a": {
                "median": result.path_a_median,
                "p90": result.path_a_p90,
                "p99": result.path_a_p99,
                "mean": round(float(arr_a.mean()), 2),
                "std": round(float(arr_a.std()), 2),
            },
            "path_b": {
                "median": result.path_b_median,
                "p90": result.path_b_p90,
                "p99": result.path_b_p99,
                "mean": round(float(arr_b.mean()), 2),
                "std": round(float(arr_b.std()), 2),
            },
            "dome": {
                "total_cost": result.dome_cost_total,
                "roi": result.dome_roi,
                "net_savings_median": round(
                    result.path_a_median - result.path_b_median, 2),
            },
        }
