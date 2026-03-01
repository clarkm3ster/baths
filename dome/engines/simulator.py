"""
Monte Carlo Whole-Life Simulator (Step 11)
==========================================

Simulates a person's lifetime costs under two scenarios:

- **Path A (No DOME)**: Natural cascade progression with no coordinated intervention.
- **Path B (DOME Active)**: Coordinated interventions break cascade chains at
  optimal points, with DOME overhead costs.

The simulator runs ``N`` iterations (default 1,000), each projecting year-by-year
costs from the person's current age through a configurable time horizon. At each
year, stochastic cascade transitions and catastrophic events are sampled.

Usage::

    from dome.engines.simulator import LifeSimulator
    sim = LifeSimulator()
    result = sim.simulate(person_state, budget_key, fiscal_history,
                          iterations=1000, projection_years=50)
    print(result.dome_roi)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import numpy as np

from dome.models.budget_key import PersonBudgetKey
from dome.models.fiscal_event import FiscalEvent


# ---------------------------------------------------------------------------
# Result container
# ---------------------------------------------------------------------------

@dataclass
class SimulationResult:
    """Output of a Monte Carlo whole-life simulation."""

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

_BASE_ANNUAL_COST: dict[str, float] = {
    "federal": 20_600.0,
    "state": 10_800.0,
    "local": 7_200.0,
}

_DOME_OVERHEAD_LOW = 2_000.0
_DOME_OVERHEAD_HIGH = 5_000.0

_EVENTS: list[dict[str, Any]] = [
    {
        "name": "hospitalization",
        "base_prob": 0.04,
        "risk_field": "chronic_condition_flags",
        "risk_multiplier": 0.08,
        "cost_mean": 25_000.0,
        "cost_std": 10_000.0,
    },
    {
        "name": "incarceration",
        "base_prob": 0.005,
        "risk_field": "justice_involvement_flag",
        "risk_multiplier": 0.15,
        "cost_mean": 47_500.0,
        "cost_std": 12_000.0,
    },
    {
        "name": "homelessness_episode",
        "base_prob": 0.005,
        "risk_field": "homelessness_history_flag",
        "risk_multiplier": 0.12,
        "cost_mean": 40_000.0,
        "cost_std": 8_000.0,
    },
    {
        "name": "mental_health_crisis",
        "base_prob": 0.03,
        "risk_field": "high_need_flag",
        "risk_multiplier": 0.10,
        "cost_mean": 15_000.0,
        "cost_std": 5_000.0,
    },
    {
        "name": "sud_relapse",
        "base_prob": 0.02,
        "risk_field": "high_need_flag",
        "risk_multiplier": 0.08,
        "cost_mean": 22_000.0,
        "cost_std": 8_000.0,
    },
]

_RISK_ADDERS: dict[str, float] = {
    "chronic_conditions_per": 4_000.0,
    "homelessness_active": 40_000.0,
    "disability": 36_000.0,
    "justice_supervision": 5_000.0,
    "high_need_healthcare_multiplier": 1.5,
}

_DOME_BREAK_PROB = 0.55
_DOME_SEVERITY_REDUCTION = 0.50


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

    def simulate(
        self,
        person_state: Any,
        budget_key: PersonBudgetKey,
        fiscal_history: list[FiscalEvent | dict],
        iterations: int = 1000,
        projection_years: int = 50,
    ) -> SimulationResult:
        """Run the full Path A vs Path B Monte Carlo simulation.

        Parameters
        ----------
        person_state
            Current dynamic state (used for supplemental info).
        budget_key
            Person's budget key with demographics and risk flags.
        fiscal_history
            Historical fiscal events (reserved for calibration).
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
        max_age = min(current_age + projection_years, 85)
        n_years = max(max_age - current_age, 1)

        params = self._build_params(budget_key)

        path_a_yearly = np.zeros((iterations, n_years), dtype=np.float64)
        path_b_yearly = np.zeros((iterations, n_years), dtype=np.float64)
        dome_yearly = np.zeros((iterations, n_years), dtype=np.float64)

        for yr in range(n_years):
            age = current_age + yr
            age_mult = self._age_multiplier(age)
            base_cost = sum(_BASE_ANNUAL_COST.values()) * age_mult
            risk_adjusted = base_cost + params["annual_risk_adder"]
            if params["high_need"]:
                risk_adjusted *= _RISK_ADDERS["high_need_healthcare_multiplier"]

            # Path A: no intervention
            sigma_a = 0.25
            mu_a = np.log(max(risk_adjusted, 1.0)) - 0.5 * sigma_a ** 2
            path_a_base = self._rng.lognormal(mu_a, sigma_a, size=iterations)
            event_costs_a = self._sample_events(params, iterations, dome_active=False)
            path_a_yearly[:, yr] = path_a_base + event_costs_a

            # Path B: DOME active (15% base reduction, lower variance)
            sigma_b = 0.20
            mu_b = np.log(max(risk_adjusted * 0.85, 1.0)) - 0.5 * sigma_b ** 2
            path_b_base = self._rng.lognormal(mu_b, sigma_b, size=iterations)
            event_costs_b = self._sample_events(params, iterations, dome_active=True)
            path_b_yearly[:, yr] = path_b_base + event_costs_b

            # DOME overhead
            dome_yearly[:, yr] = self._rng.uniform(
                _DOME_OVERHEAD_LOW, _DOME_OVERHEAD_HIGH, size=iterations,
            )

        path_a_totals = path_a_yearly.sum(axis=1)
        path_b_totals = path_b_yearly.sum(axis=1) + dome_yearly.sum(axis=1)
        dome_totals = dome_yearly.sum(axis=1)

        path_a_median = float(np.median(path_a_totals))
        path_a_p90 = float(np.percentile(path_a_totals, 90))
        path_a_p99 = float(np.percentile(path_a_totals, 99))
        path_b_median = float(np.median(path_b_totals))
        path_b_p90 = float(np.percentile(path_b_totals, 90))
        path_b_p99 = float(np.percentile(path_b_totals, 99))
        dome_cost_total = float(np.median(dome_totals))

        median_savings = path_a_median - path_b_median
        dome_roi = median_savings / dome_cost_total if dome_cost_total > 0 else 0.0

        return SimulationResult(
            path_a_costs=path_a_totals.tolist(),
            path_b_costs=path_b_totals.tolist(),
            dome_costs=dome_totals.tolist(),
            path_a_median=round(path_a_median, 2),
            path_a_p90=round(path_a_p90, 2),
            path_a_p99=round(path_a_p99, 2),
            path_b_median=round(path_b_median, 2),
            path_b_p90=round(path_b_p90, 2),
            path_b_p99=round(path_b_p99, 2),
            dome_cost_total=round(dome_cost_total, 2),
            dome_roi=round(dome_roi, 2),
            iterations_run=iterations,
            year_by_year_path_a=path_a_yearly.tolist(),
            year_by_year_path_b=path_b_yearly.tolist(),
        )

    def _build_params(self, key: PersonBudgetKey) -> dict[str, Any]:
        """Extract simulation parameters from the budget key."""
        n_chronic = len(key.chronic_condition_flags)
        annual_risk_adder = n_chronic * _RISK_ADDERS["chronic_conditions_per"]

        if key.housing_status in ("shelter", "street"):
            annual_risk_adder += _RISK_ADDERS["homelessness_active"]
        if key.disability_flag:
            annual_risk_adder += _RISK_ADDERS["disability"]
        if key.justice_involvement_flag:
            annual_risk_adder += _RISK_ADDERS["justice_supervision"]

        event_probs: dict[str, float] = {}
        for evt in _EVENTS:
            p = evt["base_prob"]
            rf = evt["risk_field"]
            if rf == "chronic_condition_flags" and n_chronic > 0:
                p += evt["risk_multiplier"] * n_chronic
            elif rf == "justice_involvement_flag" and key.justice_involvement_flag:
                p += evt["risk_multiplier"]
            elif rf == "homelessness_history_flag" and key.homelessness_history_flag:
                p += evt["risk_multiplier"]
            elif rf == "high_need_flag" and key.high_need_flag:
                p += evt["risk_multiplier"]
            event_probs[evt["name"]] = min(p, 0.95)

        return {
            "annual_risk_adder": annual_risk_adder,
            "high_need": key.high_need_flag,
            "event_probs": event_probs,
        }

    def _sample_events(
        self,
        params: dict[str, Any],
        n: int,
        dome_active: bool,
    ) -> np.ndarray:
        """Sample catastrophic event costs for n iterations in one year."""
        total = np.zeros(n, dtype=np.float64)
        for evt in _EVENTS:
            prob = params["event_probs"][evt["name"]]
            if dome_active:
                prob *= (1.0 - _DOME_BREAK_PROB)
            triggers = self._rng.random(n) < prob
            costs = np.abs(self._rng.normal(evt["cost_mean"], evt["cost_std"], size=n))
            if dome_active:
                costs *= _DOME_SEVERITY_REDUCTION
            total += triggers * costs
        return total

    @staticmethod
    def _age_multiplier(age: int) -> float:
        """Cost multiplier by age (healthcare costs rise with age)."""
        if age < 18:
            return 0.6
        if age < 35:
            return 0.8
        if age < 55:
            return 1.0
        if age < 65:
            return 1.4
        if age < 75:
            return 2.0
        return 2.8
