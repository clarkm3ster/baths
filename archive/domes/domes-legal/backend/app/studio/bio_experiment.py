"""Biological Experimentation layer -- N-of-1 Trial Framework.

Implements personalised single-subject (N-of-1) trials with an ABAB
crossover design.  Each trial alternates between intervention and control
phases with washout periods, collecting measurements that are analysed
with both frequentist (paired t-test) and Bayesian (beta-posterior)
methods.

Key capabilities:
    - ABAB crossover trial design with configurable cycle count and
      phase duration
    - Real-time measurement recording by phase
    - Paired t-test + Cohen's d effect-size analysis
    - Simple Bayesian posterior (beta distribution) for probability
      of superiority
    - Bayesian stopping rule for early termination when evidence is
      decisive

All computations use only the standard library (math, statistics).
"""
from __future__ import annotations

import math
import statistics
from datetime import datetime
from typing import Literal, Optional
from uuid import uuid4

from pydantic import BaseModel, Field


# ═══════════════════════════════════════════════════════════════════
# Models
# ═══════════════════════════════════════════════════════════════════

class TrialPhase(BaseModel):
    """A single phase within an N-of-1 trial."""
    phase_type: Literal["baseline", "intervention", "washout", "control"]
    start_day: int
    end_day: int
    measurements: list[float] = Field(default_factory=list)


class PersonalTrial(BaseModel):
    """An N-of-1 trial for a single person."""
    trial_id: str = Field(default_factory=lambda: str(uuid4()))
    person_id: str
    hypothesis: str
    intervention: str
    control: str
    metric_name: str
    phases: list[TrialPhase] = Field(default_factory=list)
    status: Literal[
        "designed", "active", "washout", "completed", "stopped"
    ] = "designed"
    created_at: str = Field(
        default_factory=lambda: datetime.utcnow().isoformat()
    )


class TrialResult(BaseModel):
    """Statistical results from a completed (or interim) trial analysis."""
    trial_id: str
    intervention_mean: float
    control_mean: float
    effect_size: float          # Cohen's d
    p_value: float              # from paired t-test
    bayesian_probability: float # posterior P(intervention > control)
    recommendation: str


# ═══════════════════════════════════════════════════════════════════
# Trial design
# ═══════════════════════════════════════════════════════════════════

def design_trial(
    person_id: str,
    hypothesis: str,
    intervention: str,
    control: str,
    metric_name: str,
    n_cycles: int = 3,
    phase_days: int = 14,
) -> PersonalTrial:
    """Design an ABAB crossover trial.

    The design produces alternating control (A) and intervention (B)
    phases with washout periods between each transition.  Washout
    length is one-quarter of phase_days (minimum 1 day).

    Sequence per cycle:
        control -> washout -> intervention -> washout

    Args:
        person_id: Participant identifier.
        hypothesis: What the trial aims to test.
        intervention: Description of the active intervention.
        control: Description of the control condition.
        metric_name: Primary outcome variable name.
        n_cycles: Number of AB cycles (default 3).
        phase_days: Duration of each active phase in days (default 14).

    Returns:
        A fully designed PersonalTrial with phase schedule.
    """
    if n_cycles < 1:
        raise ValueError("n_cycles must be >= 1")
    if phase_days < 2:
        raise ValueError("phase_days must be >= 2")

    washout_days = max(phase_days // 4, 1)
    phases: list[TrialPhase] = []
    day = 0

    for cycle in range(n_cycles):
        # A -- control phase
        phases.append(TrialPhase(
            phase_type="control",
            start_day=day,
            end_day=day + phase_days - 1,
        ))
        day += phase_days

        # Washout
        phases.append(TrialPhase(
            phase_type="washout",
            start_day=day,
            end_day=day + washout_days - 1,
        ))
        day += washout_days

        # B -- intervention phase
        phases.append(TrialPhase(
            phase_type="intervention",
            start_day=day,
            end_day=day + phase_days - 1,
        ))
        day += phase_days

        # Washout (unless last cycle)
        if cycle < n_cycles - 1:
            phases.append(TrialPhase(
                phase_type="washout",
                start_day=day,
                end_day=day + washout_days - 1,
            ))
            day += washout_days

    return PersonalTrial(
        person_id=person_id,
        hypothesis=hypothesis,
        intervention=intervention,
        control=control,
        metric_name=metric_name,
        phases=phases,
        status="designed",
    )


# ═══════════════════════════════════════════════════════════════════
# Measurement recording
# ═══════════════════════════════════════════════════════════════════

def record_measurement(
    trial: PersonalTrial,
    phase_index: int,
    value: float,
) -> PersonalTrial:
    """Record a measurement for a specific phase.

    Args:
        trial: The trial to update.
        phase_index: Zero-based index into trial.phases.
        value: The measurement value to append.

    Returns:
        Updated trial with the new measurement appended.

    Raises:
        IndexError: If phase_index is out of range.
        ValueError: If measurement is NaN.
    """
    if phase_index < 0 or phase_index >= len(trial.phases):
        raise IndexError(
            f"phase_index {phase_index} out of range "
            f"(trial has {len(trial.phases)} phases)"
        )
    if math.isnan(value):
        raise ValueError("Measurement value cannot be NaN")

    # Build updated phases list
    new_phases = []
    for i, phase in enumerate(trial.phases):
        if i == phase_index:
            updated = phase.model_copy(update={
                "measurements": phase.measurements + [value],
            })
            new_phases.append(updated)
        else:
            new_phases.append(phase)

    # Auto-transition status if first measurement recorded
    new_status = trial.status
    if trial.status == "designed":
        new_status = "active"

    return trial.model_copy(update={
        "phases": new_phases,
        "status": new_status,
    })


# ═══════════════════════════════════════════════════════════════════
# Statistical helpers (stdlib only)
# ═══════════════════════════════════════════════════════════════════

def _collect_phase_data(
    trial: PersonalTrial,
    phase_type: str,
) -> list[float]:
    """Collect all measurements from phases of a given type."""
    values: list[float] = []
    for phase in trial.phases:
        if phase.phase_type == phase_type:
            values.extend(phase.measurements)
    return values


def _paired_t_test(group_a: list[float], group_b: list[float]) -> float:
    """Two-sample Welch's t-test, returning a two-tailed p-value.

    Uses the stdlib math module.  Approximates the t-distribution CDF
    via the regularised incomplete beta function for small samples.
    """
    n_a, n_b = len(group_a), len(group_b)
    if n_a < 2 or n_b < 2:
        return 1.0  # insufficient data

    mean_a = statistics.mean(group_a)
    mean_b = statistics.mean(group_b)
    var_a = statistics.variance(group_a)
    var_b = statistics.variance(group_b)

    se = math.sqrt(var_a / n_a + var_b / n_b)
    if se == 0:
        return 1.0

    t_stat = abs(mean_a - mean_b) / se

    # Welch-Satterthwaite degrees of freedom
    num = (var_a / n_a + var_b / n_b) ** 2
    denom = (
        (var_a / n_a) ** 2 / (n_a - 1)
        + (var_b / n_b) ** 2 / (n_b - 1)
    )
    if denom == 0:
        return 1.0
    df = num / denom

    # Approximate p-value using the regularised incomplete beta function
    p = _t_distribution_two_tail_p(t_stat, df)
    return p


def _t_distribution_two_tail_p(t: float, df: float) -> float:
    """Approximate two-tailed p-value from |t| and df.

    Uses the relationship between the t-distribution CDF and the
    regularised incomplete beta function:
        P(T > t) = 0.5 * I_{df/(df+t^2)}(df/2, 0.5)
    """
    x = df / (df + t * t)
    p = _regularised_incomplete_beta(x, df / 2.0, 0.5)
    return min(p, 1.0)


def _regularised_incomplete_beta(
    x: float, a: float, b: float, max_iter: int = 200, tol: float = 1e-12,
) -> float:
    """Regularised incomplete beta function I_x(a, b).

    Uses the continued-fraction expansion (Lentz's method) for numerical
    stability with small sample sizes.
    """
    if x <= 0.0:
        return 0.0
    if x >= 1.0:
        return 1.0

    # Use the symmetry relation when x > (a+1)/(a+b+2) for convergence
    if x > (a + 1.0) / (a + b + 2.0):
        return 1.0 - _regularised_incomplete_beta(1.0 - x, b, a, max_iter, tol)

    # Log-beta coefficient
    ln_prefix = (
        a * math.log(x) + b * math.log(1.0 - x)
        - math.log(a)
        - _log_beta(a, b)
    )
    prefix = math.exp(ln_prefix)

    # Continued fraction (modified Lentz)
    cf = _beta_cf(x, a, b, max_iter, tol)
    return prefix * cf


def _log_beta(a: float, b: float) -> float:
    """Log of the beta function B(a, b) = Gamma(a)*Gamma(b)/Gamma(a+b)."""
    return math.lgamma(a) + math.lgamma(b) - math.lgamma(a + b)


def _beta_cf(
    x: float, a: float, b: float, max_iter: int, tol: float,
) -> float:
    """Evaluate the continued fraction for I_x(a,b) using Lentz's method."""
    tiny = 1e-30
    f = 1.0
    c = 1.0
    d = 1.0 - (a + b) * x / (a + 1.0)
    if abs(d) < tiny:
        d = tiny
    d = 1.0 / d
    f = d

    for m in range(1, max_iter + 1):
        # Even step
        m2 = 2 * m
        numerator = m * (b - m) * x / ((a + m2 - 1.0) * (a + m2))
        d = 1.0 + numerator * d
        if abs(d) < tiny:
            d = tiny
        c = 1.0 + numerator / c
        if abs(c) < tiny:
            c = tiny
        d = 1.0 / d
        f *= c * d

        # Odd step
        numerator = -(a + m) * (a + b + m) * x / ((a + m2) * (a + m2 + 1.0))
        d = 1.0 + numerator * d
        if abs(d) < tiny:
            d = tiny
        c = 1.0 + numerator / c
        if abs(c) < tiny:
            c = tiny
        d = 1.0 / d
        delta = c * d
        f *= delta

        if abs(delta - 1.0) < tol:
            break

    return f


def _cohens_d(group_a: list[float], group_b: list[float]) -> float:
    """Compute Cohen's d (pooled standard deviation)."""
    n_a, n_b = len(group_a), len(group_b)
    if n_a < 2 or n_b < 2:
        return 0.0

    mean_a = statistics.mean(group_a)
    mean_b = statistics.mean(group_b)
    var_a = statistics.variance(group_a)
    var_b = statistics.variance(group_b)

    pooled_var = ((n_a - 1) * var_a + (n_b - 1) * var_b) / (n_a + n_b - 2)
    pooled_sd = math.sqrt(pooled_var)

    if pooled_sd == 0:
        return 0.0

    return (mean_b - mean_a) / pooled_sd


def _bayesian_probability_of_superiority(
    group_a: list[float],
    group_b: list[float],
) -> float:
    """Simple Bayesian posterior probability that intervention > control.

    Uses a normal approximation: the difference in means is compared to
    zero under the posterior, modeled as a beta distribution mapped
    through the effect size.  For simplicity, we use the fraction of
    simulated differences that are positive, using the analytic normal CDF.

    P(B > A) = Phi(d / sqrt(1/nA + 1/nB))

    where d = (mean_B - mean_A) / pooled_sd.
    """
    n_a, n_b = len(group_a), len(group_b)
    if n_a < 2 or n_b < 2:
        return 0.5  # uninformative prior

    d = _cohens_d(group_a, group_b)
    se = math.sqrt(1.0 / n_a + 1.0 / n_b)

    if se == 0:
        return 0.5

    z = d / se
    # Normal CDF approximation via error function
    prob = 0.5 * (1.0 + math.erf(z / math.sqrt(2.0)))
    return round(prob, 4)


# ═══════════════════════════════════════════════════════════════════
# Trial analysis
# ═══════════════════════════════════════════════════════════════════

def analyze_trial(trial: PersonalTrial) -> TrialResult:
    """Analyse an N-of-1 trial using paired t-test and Bayesian posterior.

    Collects all measurements from intervention and control phases,
    computes effect size (Cohen's d), frequentist p-value (Welch's t),
    and Bayesian probability of superiority.

    Args:
        trial: The trial to analyse.

    Returns:
        TrialResult with statistics and a human-readable recommendation.

    Raises:
        ValueError: If insufficient data for analysis (< 2 measurements
            in either arm).
    """
    control_data = _collect_phase_data(trial, "control")
    intervention_data = _collect_phase_data(trial, "intervention")

    if len(control_data) < 2 or len(intervention_data) < 2:
        raise ValueError(
            f"Insufficient data for analysis: "
            f"{len(control_data)} control and "
            f"{len(intervention_data)} intervention measurements "
            f"(need >= 2 each)"
        )

    control_mean = statistics.mean(control_data)
    intervention_mean = statistics.mean(intervention_data)
    effect = _cohens_d(control_data, intervention_data)
    p_val = _paired_t_test(control_data, intervention_data)
    bayes_prob = _bayesian_probability_of_superiority(
        control_data, intervention_data,
    )

    # Generate recommendation
    recommendation = _generate_recommendation(effect, p_val, bayes_prob)

    return TrialResult(
        trial_id=trial.trial_id,
        intervention_mean=round(intervention_mean, 4),
        control_mean=round(control_mean, 4),
        effect_size=round(effect, 4),
        p_value=round(p_val, 4),
        bayesian_probability=bayes_prob,
        recommendation=recommendation,
    )


def _generate_recommendation(
    effect_size: float, p_value: float, bayes_prob: float,
) -> str:
    """Generate a human-readable recommendation from trial statistics."""
    abs_effect = abs(effect_size)

    if abs_effect < 0.2:
        size_label = "negligible"
    elif abs_effect < 0.5:
        size_label = "small"
    elif abs_effect < 0.8:
        size_label = "medium"
    else:
        size_label = "large"

    direction = "favours intervention" if effect_size > 0 else "favours control"

    if p_value < 0.05 and bayes_prob > 0.95 and abs_effect >= 0.5:
        return (
            f"Strong evidence of {size_label} effect ({direction}). "
            f"Consider adopting the intervention."
        )
    elif p_value < 0.05 and abs_effect >= 0.2:
        return (
            f"Statistically significant {size_label} effect ({direction}). "
            f"More cycles recommended to strengthen evidence."
        )
    elif bayes_prob > 0.80 and abs_effect >= 0.2:
        return (
            f"Suggestive {size_label} effect ({direction}), "
            f"Bayesian probability {bayes_prob:.0%}. "
            f"Continue trial for more data."
        )
    elif abs_effect < 0.2:
        return (
            "No meaningful difference detected between intervention "
            "and control. Consider modifying the intervention or "
            "choosing a different outcome metric."
        )
    else:
        return (
            f"Inconclusive results ({size_label} effect, {direction}). "
            f"Continue data collection."
        )


# ═══════════════════════════════════════════════════════════════════
# Bayesian stopping rule
# ═══════════════════════════════════════════════════════════════════

def should_stop_early(
    trial: PersonalTrial,
    min_effect: float = 0.2,
    confidence: float = 0.95,
) -> tuple[bool, str]:
    """Apply a Bayesian stopping rule to decide if the trial can end early.

    The trial should stop if:
    1. The Bayesian probability of superiority exceeds ``confidence``
       AND the effect size exceeds ``min_effect`` (decisive benefit), OR
    2. The Bayesian probability of superiority is below (1 - confidence)
       (decisive futility -- control is better), OR
    3. There are enough measurements and the effect is negligible
       (futility -- no meaningful difference).

    Args:
        trial: The trial to evaluate.
        min_effect: Minimum clinically meaningful effect size (Cohen's d).
        confidence: Required posterior probability threshold.

    Returns:
        Tuple of (should_stop: bool, reason: str).
    """
    control_data = _collect_phase_data(trial, "control")
    intervention_data = _collect_phase_data(trial, "intervention")

    if len(control_data) < 2 or len(intervention_data) < 2:
        return (False, "Insufficient data for stopping decision")

    effect = _cohens_d(control_data, intervention_data)
    bayes_prob = _bayesian_probability_of_superiority(
        control_data, intervention_data,
    )

    total_measurements = len(control_data) + len(intervention_data)

    # Rule 1: decisive benefit
    if bayes_prob >= confidence and abs(effect) >= min_effect:
        return (
            True,
            f"Decisive benefit detected: effect size {effect:.3f}, "
            f"Bayesian P(intervention > control) = {bayes_prob:.3f} "
            f"(threshold {confidence}). Recommend stopping and adopting "
            f"intervention.",
        )

    # Rule 2: decisive futility -- control is clearly better
    if bayes_prob <= (1.0 - confidence):
        return (
            True,
            f"Decisive futility: Bayesian P(intervention > control) = "
            f"{bayes_prob:.3f}, indicating control is superior. "
            f"Recommend stopping.",
        )

    # Rule 3: negligible effect with sufficient data
    if total_measurements >= 20 and abs(effect) < min_effect:
        return (
            True,
            f"Futility: {total_measurements} measurements collected but "
            f"effect size ({effect:.3f}) is below minimum threshold "
            f"({min_effect}). No meaningful difference detected.",
        )

    return (
        False,
        f"Continue trial: effect size {effect:.3f}, "
        f"Bayesian probability {bayes_prob:.3f}, "
        f"{total_measurements} measurements so far.",
    )
