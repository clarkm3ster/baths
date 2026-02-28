"""
DOMES v2 — Compute Budget Tracker
==================================

Models the full 3×10²¹ FLOP / $33–50B, 5-year compute budget directed at
a single person (Robert Jackson) by the DOMES system.

At sustained operation:
    Total FLOPs: 3.0 × 10²¹
    Duration:    5 years  = 157,680,000 seconds
    Sustained:   ~1.9 × 10¹³ FLOPS (peta-class sustained throughput)

Cost mapping (estimated):
    $33B  low  → ~$2.09B / year → ~$5.7M / day  → ~$66 / second
    $50B  high → ~$3.17B / year → ~$8.7M / day  → ~$100 / second

Each FLOP has a marginal value that follows a diminishing returns curve.
This module tracks allocation across four compute-consuming services
(prediction, flourishing, fragment, cosm) and computes:

    - Per-service consumption and utilization
    - Information gain per FLOP (Fisher information analog)
    - Marginal value of next FLOP by service
    - Compute pressure: when to shift allocation between services
    - What-if scenario analysis

Usage
-----
    from domes.services.compute import COMPUTE_BUDGET, ServiceName

    # Consume FLOPs
    COMPUTE_BUDGET.consume(ServiceName.PREDICTION, flops=1e12)

    # Query marginal value
    best_service = COMPUTE_BUDGET.highest_marginal_value()

    # What-if
    report = COMPUTE_BUDGET.what_if_scenario(multiplier=10.0)
"""
from __future__ import annotations

import math
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any

# ---------------------------------------------------------------------------
# Global constants
# ---------------------------------------------------------------------------

#: Total FLOPs committed over the 5-year program.
TOTAL_FLOPS: float = 3.0e21

#: Program duration in years.
BUDGET_YEARS: int = 5

#: Program duration in seconds.
BUDGET_SECONDS: float = BUDGET_YEARS * 365.25 * 24 * 3600  # ≈ 1.577e8 s

#: Sustained FLOPS throughput required.
SUSTAINED_FLOPS_PER_SECOND: float = TOTAL_FLOPS / BUDGET_SECONDS  # ≈ 1.9e13

#: Total dollar budget — conservative end ($33B).
TOTAL_BUDGET_USD_LOW: float = 33.0e9

#: Total dollar budget — high end ($50B).
TOTAL_BUDGET_USD_HIGH: float = 50.0e9

#: Midpoint budget used for per-FLOP cost calculations.
TOTAL_BUDGET_USD_MID: float = (TOTAL_BUDGET_USD_LOW + TOTAL_BUDGET_USD_HIGH) / 2.0

#: Estimated cost per FLOP (midpoint budget / total FLOPs).
COST_PER_FLOP: float = TOTAL_BUDGET_USD_MID / TOTAL_FLOPS  # ≈ $1.4e-11 per FLOP

#: Power Utilization Effectiveness for large-scale AI clusters (typical: 1.2–1.5).
PUE: float = 1.3

#: Approximate energy cost per kWh for a large compute facility (USD).
ENERGY_COST_PER_KWH: float = 0.06

#: Estimated FLOPS per watt for H100-class hardware (BF16 tensor ops).
FLOPS_PER_WATT: float = 3.0e12  # ~3 petaFLOPS per kW


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class ServiceName(str, Enum):
    """Services that consume FLOPs from the DOMES budget."""
    PREDICTION  = "prediction"   # Risk scoring, causal modeling, interventions
    FLOURISHING = "flourishing"  # 12-domain flourishing inference
    FRAGMENT    = "fragment"     # Ingest normalization, embedding, dedup
    COSM        = "cosm"         # Composite Outcome Scoring Model


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class ComputeAllocation:
    """Current allocation and consumption state for a single service.

    Attributes
    ----------
    service:
        The service consuming compute.
    allocated_fraction:
        Share of total FLOP budget allocated to this service (0.0–1.0).
    flops_consumed:
        Cumulative FLOPs consumed by this service since tracking began.
    last_consume_ts:
        Unix timestamp of the most recent consumption event.
    info_gain_alpha:
        Shape parameter α of the diminishing-returns curve.
        Information gain ∝ consumed^α  (0 < α < 1 → concave / diminishing).
    priority_weight:
        Human-assigned priority weight. Used when rebalancing pressure.
    """
    service: ServiceName
    allocated_fraction: float
    flops_consumed: float = 0.0
    last_consume_ts: float = field(default_factory=time.time)
    info_gain_alpha: float = 0.6   # concave exponent — diminishing returns
    priority_weight: float = 1.0

    # --- Derived metrics (updated on each consume) ---

    flops_per_second: float = 0.0        # Instantaneous throughput
    session_start_ts: float = field(default_factory=time.time)

    @property
    def allocated_flops(self) -> float:
        """Total FLOPs allocated to this service over the full budget period."""
        return TOTAL_FLOPS * self.allocated_fraction

    @property
    def utilization(self) -> float:
        """Fraction of allocated FLOPs that have been consumed (0.0–1.0+)."""
        if self.allocated_flops == 0:
            return 0.0
        return self.flops_consumed / self.allocated_flops

    @property
    def flops_remaining(self) -> float:
        """FLOPs still available under this service's allocation."""
        return max(0.0, self.allocated_flops - self.flops_consumed)

    @property
    def cost_consumed_usd(self) -> float:
        """Dollar cost of FLOPs consumed by this service so far."""
        return self.flops_consumed * COST_PER_FLOP

    @property
    def information_gain(self) -> float:
        """Cumulative information gain (arbitrary units, concave in FLOPs).

        Models the intuition that each additional FLOP yields diminishing
        marginal insight once the prediction surface has been explored.

        IG(n) = n^α  where 0 < α < 1
        """
        if self.flops_consumed == 0:
            return 0.0
        return self.flops_consumed ** self.info_gain_alpha

    @property
    def marginal_information_gain(self) -> float:
        """Derivative of information gain at current consumption level.

        dIG/dn = α · n^(α−1)

        Higher value → this service benefits most from the next FLOP.
        Returns 0.0 if no FLOPs have been consumed yet (avoids division by zero
        for α < 1; uses a small epsilon offset instead).
        """
        n = max(self.flops_consumed, 1.0)   # avoid n=0 singularity
        return self.info_gain_alpha * (n ** (self.info_gain_alpha - 1))

    def to_dict(self) -> dict[str, Any]:
        """Serialize to a JSON-safe dictionary."""
        return {
            "service":                    self.service.value,
            "allocated_fraction":         round(self.allocated_fraction, 4),
            "allocated_flops":            self.allocated_flops,
            "flops_consumed":             self.flops_consumed,
            "flops_remaining":            self.flops_remaining,
            "utilization":                round(self.utilization, 6),
            "cost_consumed_usd":          round(self.cost_consumed_usd, 2),
            "flops_per_second":           round(self.flops_per_second, 2),
            "information_gain":           round(self.information_gain, 4),
            "marginal_information_gain":  round(self.marginal_information_gain, 8),
            "priority_weight":            self.priority_weight,
            "info_gain_alpha":            self.info_gain_alpha,
            "last_consume_ts":            self.last_consume_ts,
        }


@dataclass
class InformationGainCurve:
    """Snapshot of the information gain curve at a given FLOP level.

    Used to communicate the shape of the diminishing-returns curve to
    API consumers without exposing the full ComputeAllocation object.
    """
    service: str
    flop_points: list[float]          # FLOP levels sampled
    ig_values: list[float]            # Corresponding IG values
    marginal_values: list[float]      # dIG/dn at each point
    current_flops: float
    current_ig: float
    current_marginal: float
    alpha: float


# ---------------------------------------------------------------------------
# Core tracker
# ---------------------------------------------------------------------------

class ComputeBudgetTracker:
    """Global compute budget tracker for the DOMES v2 system.

    Tracks 3×10²¹ FLOPs across four services over a 5-year period.
    Provides marginal value analysis to guide compute allocation decisions.

    Thread safety
    -------------
    This class is NOT thread-safe. In production, wrap with an asyncio lock
    or use a shared Redis-backed counter. For single-threaded / async use,
    no locking is needed.

    Example
    -------
    ::

        budget = ComputeBudgetTracker()

        # Simulate one hour of prediction service operation at 1e13 FLOPS
        budget.consume(ServiceName.PREDICTION, flops=1e13 * 3600)

        # Query allocation
        print(budget.status_report())

        # Ask: which service would benefit most from the next FLOP?
        print(budget.highest_marginal_value())
    """

    # Default allocation fractions — sum must equal 1.0
    DEFAULT_ALLOCATIONS: dict[ServiceName, float] = {
        ServiceName.PREDICTION:  0.40,   # Largest share — risk + causal modeling
        ServiceName.FLOURISHING: 0.25,   # Multi-tradition inference
        ServiceName.FRAGMENT:    0.20,   # Embedding, dedup, normalization
        ServiceName.COSM:        0.15,   # COSM scoring and trajectory
    }

    # Alpha (diminishing-returns exponent) by service
    SERVICE_ALPHAS: dict[ServiceName, float] = {
        ServiceName.PREDICTION:  0.55,  # Quickly saturates — more data ≠ better risk score
        ServiceName.FLOURISHING: 0.65,  # Rich domain — slower saturation
        ServiceName.FRAGMENT:    0.70,  # Normalization improves with more data
        ServiceName.COSM:        0.50,  # Composite score — fastest saturation
    }

    def __init__(
        self,
        start_time: datetime | None = None,
        allocations: dict[ServiceName, float] | None = None,
    ) -> None:
        """Initialize a new budget tracker.

        Parameters
        ----------
        start_time:
            Program start time. Defaults to now.
        allocations:
            Optional override for initial service allocation fractions.
            Must sum to 1.0.
        """
        self.start_time: datetime = start_time or datetime.now(tz=timezone.utc)
        self._init_ts: float = time.time()

        alloc = allocations or self.DEFAULT_ALLOCATIONS
        assert abs(sum(alloc.values()) - 1.0) < 1e-9, "Allocations must sum to 1.0"

        self.services: dict[ServiceName, ComputeAllocation] = {
            svc: ComputeAllocation(
                service=svc,
                allocated_fraction=alloc[svc],
                info_gain_alpha=self.SERVICE_ALPHAS[svc],
            )
            for svc in ServiceName
        }

        # Running log of allocation changes
        self._rebalance_log: list[dict[str, Any]] = []

        # Running log of consumption events (capped at last 1000 for memory)
        self._consume_log: list[dict[str, Any]] = []

    # ------------------------------------------------------------------
    # Consumption API
    # ------------------------------------------------------------------

    def consume(self, service: ServiceName, flops: float) -> ComputeAllocation:
        """Record FLOP consumption by a service.

        Parameters
        ----------
        service:
            The service consuming compute.
        flops:
            Number of FLOPs consumed in this call.

        Returns
        -------
        ComputeAllocation
            Updated allocation state for the service.
        """
        if flops < 0:
            raise ValueError(f"FLOPs consumed cannot be negative (got {flops})")

        alloc = self.services[service]
        now = time.time()
        elapsed = max(now - alloc.last_consume_ts, 1e-9)   # avoid /0

        alloc.flops_consumed += flops
        alloc.flops_per_second = flops / elapsed
        alloc.last_consume_ts = now

        # Cap consume log
        event = {
            "ts":      now,
            "service": service.value,
            "flops":   flops,
        }
        self._consume_log.append(event)
        if len(self._consume_log) > 1000:
            self._consume_log = self._consume_log[-1000:]

        return alloc

    # ------------------------------------------------------------------
    # Global metrics
    # ------------------------------------------------------------------

    @property
    def total_flops_consumed(self) -> float:
        """Sum of all FLOPs consumed across all services."""
        return sum(a.flops_consumed for a in self.services.values())

    @property
    def total_cost_consumed_usd(self) -> float:
        """Total dollar value of FLOPs consumed so far."""
        return self.total_flops_consumed * COST_PER_FLOP

    @property
    def budget_fraction_consumed(self) -> float:
        """Fraction of the total FLOP budget consumed (0.0–1.0)."""
        return self.total_flops_consumed / TOTAL_FLOPS

    @property
    def elapsed_seconds(self) -> float:
        """Wall-clock seconds elapsed since tracker was created."""
        return time.time() - self._init_ts

    @property
    def program_elapsed_fraction(self) -> float:
        """Fraction of the 5-year program window elapsed."""
        return min(self.elapsed_seconds / BUDGET_SECONDS, 1.0)

    @property
    def overall_utilization(self) -> float:
        """Are we on-pace with consumption relative to program elapsed time?

        A value > 1.0 means we are consuming FLOPs faster than the 5-year
        budget expects; < 1.0 means we are under-pacing.
        """
        if self.program_elapsed_fraction == 0:
            return 0.0
        return self.budget_fraction_consumed / self.program_elapsed_fraction

    def energy_consumed_kwh(self) -> float:
        """Estimated energy consumed (kWh) based on FLOPS consumed.

        Uses FLOPS_PER_WATT and PUE to convert FLOPs → kWh.
        """
        flops_consumed = self.total_flops_consumed
        # watts = flops_per_second / FLOPS_PER_WATT — but we need duration
        # Approximate: energy = (total_flops / FLOPS_PER_WATT) * elapsed_s / 3600
        watts_average = (flops_consumed / max(self.elapsed_seconds, 1)) / FLOPS_PER_WATT
        kwh = watts_average * PUE * self.elapsed_seconds / 3600
        return kwh

    def energy_cost_usd(self) -> float:
        """Estimated electricity cost (USD) so far."""
        return self.energy_consumed_kwh() * ENERGY_COST_PER_KWH

    # ------------------------------------------------------------------
    # Marginal value analysis
    # ------------------------------------------------------------------

    def highest_marginal_value(self) -> ServiceName:
        """Return the service that would benefit most from the next FLOP.

        This is the service with the highest marginal information gain,
        weighted by its priority weight.
        """
        return max(
            self.services.keys(),
            key=lambda s: (
                self.services[s].marginal_information_gain
                * self.services[s].priority_weight
            ),
        )

    def compute_pressure(self) -> dict[str, Any]:
        """Analyze whether to shift compute between services.

        Returns a dict describing:
        - current marginal values per service
        - recommendation: which service is under-served
        - pressure magnitude (0.0 = balanced, 1.0 = extreme imbalance)

        The pressure score is the coefficient of variation (CV) of the
        normalized marginal values across services — high CV → shift compute.
        """
        marginals: dict[str, float] = {
            svc.value: alloc.marginal_information_gain * alloc.priority_weight
            for svc, alloc in self.services.items()
        }
        values = list(marginals.values())
        mean_v = sum(values) / len(values)
        if mean_v == 0:
            return {"pressure": 0.0, "marginals": marginals, "recommendation": None}

        std_v = math.sqrt(sum((v - mean_v) ** 2 for v in values) / len(values))
        cv = std_v / mean_v   # coefficient of variation

        # Normalize CV to 0–1 range (CV=0 is perfect balance, CV=1 is typical imbalance)
        pressure = min(cv / 2.0, 1.0)

        best_service = max(marginals, key=lambda k: marginals[k])
        worst_service = min(marginals, key=lambda k: marginals[k])

        recommendation = None
        if pressure > 0.3:
            recommendation = (
                f"Shift ~5% allocation from '{worst_service}' to '{best_service}' "
                f"(pressure score: {pressure:.2f})"
            )

        return {
            "pressure": round(pressure, 4),
            "marginals": {k: round(v, 8) for k, v in marginals.items()},
            "recommendation": recommendation,
            "best_service": best_service,
            "worst_service": worst_service,
        }

    def information_gain_curve(
        self,
        service: ServiceName,
        n_points: int = 20,
    ) -> InformationGainCurve:
        """Sample the information-gain curve for a service.

        Samples the IG curve from 0 to 2× current allocated FLOPs,
        providing a picture of where we are on the saturation curve.

        Parameters
        ----------
        service:
            The service to model.
        n_points:
            Number of sample points on the curve.
        """
        alloc = self.services[service]
        max_flops = max(alloc.allocated_flops * 2, 1e12)   # at least 1T FLOPs range
        step = max_flops / n_points

        flop_points: list[float] = []
        ig_values: list[float] = []
        marginal_values: list[float] = []

        for i in range(1, n_points + 1):
            n = step * i
            ig = n ** alloc.info_gain_alpha
            dig = alloc.info_gain_alpha * (n ** (alloc.info_gain_alpha - 1))
            flop_points.append(n)
            ig_values.append(ig)
            marginal_values.append(dig)

        return InformationGainCurve(
            service=service.value,
            flop_points=flop_points,
            ig_values=ig_values,
            marginal_values=marginal_values,
            current_flops=alloc.flops_consumed,
            current_ig=alloc.information_gain,
            current_marginal=alloc.marginal_information_gain,
            alpha=alloc.info_gain_alpha,
        )

    # ------------------------------------------------------------------
    # Allocation management
    # ------------------------------------------------------------------

    def rebalance(
        self,
        new_allocations: dict[ServiceName, float],
        reason: str = "manual",
    ) -> None:
        """Shift compute allocations between services.

        Parameters
        ----------
        new_allocations:
            New allocation fractions. Must sum to 1.0.
        reason:
            Human-readable reason for the rebalance (logged).
        """
        total = sum(new_allocations.values())
        if abs(total - 1.0) > 1e-6:
            raise ValueError(
                f"New allocations must sum to 1.0 (got {total:.6f}). "
                "Pass fractions, not percentages."
            )

        old_allocs = {s: a.allocated_fraction for s, a in self.services.items()}

        for svc, fraction in new_allocations.items():
            self.services[svc].allocated_fraction = fraction

        self._rebalance_log.append({
            "ts":            time.time(),
            "reason":        reason,
            "old_allocs":    {s.value: v for s, v in old_allocs.items()},
            "new_allocs":    {s.value: v for s, v in new_allocations.items()},
        })

    def set_priority(self, service: ServiceName, weight: float) -> None:
        """Adjust the priority weight for a service.

        Priority weights scale marginal information gain when computing
        which service benefits most from additional compute. They do NOT
        change allocated fractions; use ``rebalance()`` for that.

        Parameters
        ----------
        service:
            Target service.
        weight:
            New priority weight (> 0). Default is 1.0 for all services.
        """
        if weight <= 0:
            raise ValueError(f"Priority weight must be > 0 (got {weight})")
        self.services[service].priority_weight = weight

    # ------------------------------------------------------------------
    # What-if scenarios
    # ------------------------------------------------------------------

    def what_if_scenario(
        self,
        multiplier: float = 1.0,
        capacity_loss_fraction: float = 0.0,
        horizon_years: float = 5.0,
    ) -> dict[str, Any]:
        """Model alternative compute scenarios.

        Useful for planning questions such as:
        - "What if we had 10× more compute?"
        - "What if we lose 30% of capacity?"
        - "What if we compress the timeline to 3 years?"

        Parameters
        ----------
        multiplier:
            Scale factor on total FLOP budget (e.g., 10.0 = 10× more compute).
        capacity_loss_fraction:
            Fraction of capacity that is unavailable (0.0–1.0).
            For example, 0.3 = lose 30% capacity.
        horizon_years:
            Alternative program duration to model (default: 5 years).

        Returns
        -------
        dict
            Scenario report with projected FLOPs, cost, sustained throughput,
            per-service gains, and interpretation.
        """
        effective_multiplier = multiplier * (1.0 - capacity_loss_fraction)
        new_total_flops = TOTAL_FLOPS * effective_multiplier
        new_budget_seconds = horizon_years * 365.25 * 24 * 3600
        new_sustained_flops_ps = new_total_flops / new_budget_seconds
        new_cost_low = TOTAL_BUDGET_USD_LOW * multiplier
        new_cost_high = TOTAL_BUDGET_USD_HIGH * multiplier
        new_cost_per_flop = ((new_cost_low + new_cost_high) / 2) / new_total_flops

        per_service: dict[str, dict[str, Any]] = {}
        for svc, alloc in self.services.items():
            new_allocated = new_total_flops * alloc.allocated_fraction
            new_ig = new_allocated ** alloc.info_gain_alpha
            current_ig = alloc.information_gain
            ig_gain_factor = (new_ig / current_ig) if current_ig > 0 else float("inf")
            per_service[svc.value] = {
                "new_allocated_flops":  new_allocated,
                "new_information_gain": round(new_ig, 4),
                "ig_gain_factor":       round(ig_gain_factor, 3),
            }

        energy_kwh = (new_total_flops / FLOPS_PER_WATT) / new_budget_seconds / 3600
        cooling_load_mw = (new_total_flops / new_budget_seconds / FLOPS_PER_WATT) * PUE / 1e6

        return {
            "scenario": {
                "multiplier":                multiplier,
                "capacity_loss_fraction":    capacity_loss_fraction,
                "effective_multiplier":      effective_multiplier,
                "horizon_years":             horizon_years,
            },
            "compute": {
                "total_flops":               new_total_flops,
                "sustained_flops_per_second": round(new_sustained_flops_ps, 2),
                "budget_usd_low":            new_cost_low,
                "budget_usd_high":           new_cost_high,
                "cost_per_flop":             new_cost_per_flop,
            },
            "infrastructure": {
                "cooling_load_mw":           round(cooling_load_mw, 2),
                "energy_kwh_total":          round(energy_kwh, 0),
                "energy_cost_usd":           round(energy_kwh * ENERGY_COST_PER_KWH, 0),
            },
            "per_service":                   per_service,
            "interpretation": self._scenario_narrative(
                effective_multiplier, capacity_loss_fraction
            ),
        }

    def _scenario_narrative(
        self,
        effective_multiplier: float,
        capacity_loss_fraction: float,
    ) -> str:
        """Generate a plain-English interpretation of a scenario."""
        if capacity_loss_fraction > 0:
            loss_pct = int(capacity_loss_fraction * 100)
            mult_str = f"{effective_multiplier:.1f}×"
            return (
                f"With {loss_pct}% capacity loss, effective compute drops to "
                f"{mult_str} of baseline. Prediction service (highest α saturation) "
                f"is most resilient; COSM (lowest α) loses proportionally more value."
            )
        if effective_multiplier > 1.0:
            ig_pred = (TOTAL_FLOPS * self.services[ServiceName.PREDICTION].allocated_fraction
                       * effective_multiplier
                       ) ** self.services[ServiceName.PREDICTION].info_gain_alpha
            baseline_ig = self.services[ServiceName.PREDICTION].information_gain or 1.0
            ig_ratio = ig_pred / baseline_ig if baseline_ig > 0 else effective_multiplier
            return (
                f"At {effective_multiplier:.1f}× compute, prediction service information "
                f"gain increases by {ig_ratio:.2f}× — diminishing returns mean you get "
                f"less than {effective_multiplier:.1f}× the insight for {effective_multiplier:.1f}× "
                f"the cost. Flourishing domain modeling benefits most due to higher α."
            )
        return (
            "At baseline compute, the 5-year program allocates 40% to prediction, "
            "25% to flourishing, 20% to fragment normalization, and 15% to COSM scoring."
        )

    # ------------------------------------------------------------------
    # Status reporting
    # ------------------------------------------------------------------

    def status_report(self) -> dict[str, Any]:
        """Full status report suitable for API serialization.

        Returns
        -------
        dict
            Budget status, per-service state, pressure analysis, and
            infrastructure metrics.
        """
        pressure = self.compute_pressure()
        best_svc = self.highest_marginal_value()

        return {
            "program": {
                "total_flops":               TOTAL_FLOPS,
                "budget_years":              BUDGET_YEARS,
                "budget_usd_low":            TOTAL_BUDGET_USD_LOW,
                "budget_usd_high":           TOTAL_BUDGET_USD_HIGH,
                "start_time":                self.start_time.isoformat(),
                "elapsed_seconds":           round(self.elapsed_seconds, 1),
                "program_elapsed_fraction":  round(self.program_elapsed_fraction, 8),
            },
            "consumption": {
                "total_flops_consumed":      self.total_flops_consumed,
                "budget_fraction_consumed":  round(self.budget_fraction_consumed, 8),
                "total_cost_usd":            round(self.total_cost_consumed_usd, 2),
                "sustained_target_flops_ps": SUSTAINED_FLOPS_PER_SECOND,
                "overall_utilization":       round(self.overall_utilization, 4),
                "energy_consumed_kwh":       round(self.energy_consumed_kwh(), 4),
                "energy_cost_usd":           round(self.energy_cost_usd(), 4),
            },
            "services":    {s.value: a.to_dict() for s, a in self.services.items()},
            "pressure":    pressure,
            "next_flop_goes_to": best_svc.value,
        }

    def allocation_report(self, person_id: str) -> dict[str, Any]:
        """Per-person allocation report (DOMES focuses compute on one person).

        Since all compute is directed at Robert Jackson, the per-person
        report is identical to the global report, augmented with
        person-specific metadata.
        """
        report = self.status_report()
        report["person_id"] = person_id
        report["note"] = (
            "All 3×10²¹ FLOPs are directed at this single individual. "
            "This is the most compute ever applied to modeling one human life."
        )
        return report

    # ------------------------------------------------------------------
    # Dunder
    # ------------------------------------------------------------------

    def __repr__(self) -> str:
        consumed_pct = self.budget_fraction_consumed * 100
        return (
            f"<ComputeBudgetTracker "
            f"consumed={consumed_pct:.4f}% of {TOTAL_FLOPS:.1e} FLOPs | "
            f"${self.total_cost_consumed_usd:,.0f} spent>"
        )


# ---------------------------------------------------------------------------
# Module-level singleton
# ---------------------------------------------------------------------------

#: Global compute budget singleton.
#:
#: Import and use this instance everywhere within the DOMES system::
#:
#:     from domes.services.compute import COMPUTE_BUDGET, ServiceName
#:     COMPUTE_BUDGET.consume(ServiceName.PREDICTION, flops=1e12)
COMPUTE_BUDGET: ComputeBudgetTracker = ComputeBudgetTracker()
