"""
Cascade Detector Engine (Step 5)
==================================

Real-time detection of adverse-event cascades for a single person.  The
detector scans the person's current dynamic state, DOME metrics, and fiscal
history against all six canonical cascade definitions and emits
:class:`~dome.models.cascade.CascadeAlert` objects for every cascade in
which the person shows active signals.

The detection algorithm:

1. For each cascade definition, iterate through its ordered links.
2. At each link, evaluate a *signal function* against the person's state
   to determine whether the cause event is currently present.
3. Track the furthest link index for which all preceding causes are active
   (``current_link_index``).
4. Compute a **confidence** score from signal strengths and link-level
   evidence weights.
5. Project **path_a_projected_cost** (do nothing) by rolling forward the
   remaining cascade links at their transition probabilities and applying
   unit costs.
6. Project **path_b_projected_cost** (intervene) by assuming the best
   available intervention breaks the next link.
7. Attach recommended intervention IDs.

Usage::

    from dome.engines.cascade_detector import CascadeDetector
    detector = CascadeDetector()
    alerts = detector.detect(person_state, dome_metrics, fiscal_history)
"""

from __future__ import annotations

import math
from datetime import datetime, timezone
from typing import Any, Callable

from dome.data.cascades import CASCADE_DEFINITIONS
from dome.data.interventions import INTERVENTION_INDEX
from dome.data.unit_costs import UNIT_COSTS
from dome.models.budget_key import PersonBudgetKey
from dome.models.cascade import CascadeAlert, CascadeDefinition, CascadeLink
from dome.models.dome_metrics import DomeMetrics
from dome.models.fiscal_event import FiscalEvent


# ---------------------------------------------------------------------------
# Signal detection functions
# ---------------------------------------------------------------------------
# Each function takes (person_state: PersonBudgetKey, dome_metrics: DomeMetrics,
# fiscal_history: list[FiscalEvent]) and returns a float in [0, 1] representing
# signal strength (0 = absent, 1 = fully present).

SignalFn = Callable[
    [PersonBudgetKey, DomeMetrics, list[FiscalEvent]], float
]


def _signal_job_loss(
    ps: PersonBudgetKey,
    dm: DomeMetrics,
    fh: list[FiscalEvent],
) -> float:
    """Detect job loss: unemployment status or large income drop."""
    score = 0.0

    # Unemployment status is a strong signal
    if ps.employment_status in ("unemployed",):
        score = max(score, 0.9)

    # NILF (not in labor force) can indicate discouraged worker
    if ps.employment_status in ("NILF",):
        score = max(score, 0.5)

    # Income drop > 50% — check economic layer for prior income
    prior_income = dm.economic_layer.get("prior_annual_income")
    if prior_income and prior_income > 0 and ps.current_annual_income is not None:
        drop_ratio = 1.0 - (ps.current_annual_income / prior_income)
        if drop_ratio > 0.5:
            score = max(score, min(1.0, 0.5 + drop_ratio))

    # Income volatility as a supporting signal
    if ps.income_volatility_score is not None and ps.income_volatility_score > 0.7:
        score = max(score, 0.4)

    return score


def _signal_depression(
    ps: PersonBudgetKey,
    dm: DomeMetrics,
    fh: list[FiscalEvent],
) -> float:
    """Detect depression: PHQ-9 > 10 or clinical layer signal > 0.5."""
    score = 0.0

    # Check clinical layer for depression severity (PHQ-9 scale 0-27)
    phq9 = dm.clinical_layer.get("depression_severity")
    if phq9 is not None:
        if phq9 > 10:
            # Moderate to severe depression — map 10-27 to 0.6-1.0
            score = max(score, min(1.0, 0.6 + (phq9 - 10) * 0.4 / 17))
        elif phq9 > 5:
            # Mild depression — partial signal
            score = max(score, 0.3)

    # Behavioral layer may have a normalized depression score
    dep_score = dm.behavioral_layer.get("depression_score")
    if dep_score is not None and dep_score > 0.5:
        score = max(score, min(1.0, dep_score))

    # Check subjective wellbeing
    life_sat = dm.subjective_wellbeing_layer.get("life_satisfaction")
    if life_sat is not None and life_sat < 3.0:
        score = max(score, 0.4)

    return score


def _signal_chronic_disease(
    ps: PersonBudgetKey,
    dm: DomeMetrics,
    fh: list[FiscalEvent],
) -> float:
    """Detect chronic disease: non-empty conditions list or HbA1c > 7."""
    score = 0.0

    if ps.chronic_condition_flags:
        # More conditions = stronger signal, capped at 1.0
        n = len(ps.chronic_condition_flags)
        score = max(score, min(1.0, 0.5 + n * 0.15))

    # HbA1c from biometric layer
    hba1c = dm.biometric_layer.get("hba1c")
    if hba1c is not None and hba1c > 7.0:
        score = max(score, min(1.0, 0.6 + (hba1c - 7.0) * 0.1))

    # High-need flag is a strong indicator
    if ps.high_need_flag:
        score = max(score, 0.8)

    return score


def _signal_social_isolation(
    ps: PersonBudgetKey,
    dm: DomeMetrics,
    fh: list[FiscalEvent],
) -> float:
    """Detect social isolation: score > 0.6 or network size < 3."""
    score = 0.0

    iso_score = dm.social_layer.get("social_isolation_score")
    if iso_score is not None and iso_score > 0.6:
        score = max(score, min(1.0, iso_score))

    network_size = dm.social_layer.get("social_network_size")
    if network_size is not None and network_size < 3:
        # 0 contacts -> 1.0, 1 -> 0.8, 2 -> 0.6
        score = max(score, min(1.0, 1.0 - network_size * 0.2))

    return score


def _signal_housing_instability(
    ps: PersonBudgetKey,
    dm: DomeMetrics,
    fh: list[FiscalEvent],
) -> float:
    """Detect housing instability: shelter/street/doubled_up or homelessness history."""
    score = 0.0

    unstable_statuses = {"shelter", "street", "doubled_up"}
    if ps.housing_status in unstable_statuses:
        severity_map = {"street": 1.0, "shelter": 0.85, "doubled_up": 0.65}
        score = max(score, severity_map.get(ps.housing_status, 0.7))

    if ps.homelessness_history_flag:
        score = max(score, 0.5)

    # Housing quality from environmental layer
    hq = dm.environmental_layer.get("housing_quality_score")
    if hq is not None and hq < 3:
        score = max(score, 0.6)

    return score


def _signal_substance_use(
    ps: PersonBudgetKey,
    dm: DomeMetrics,
    fh: list[FiscalEvent],
) -> float:
    """Detect substance use disorder: SUD severity > 0.4."""
    score = 0.0

    sud = dm.behavioral_layer.get("sud_severity")
    if sud is not None and sud > 0.4:
        score = max(score, min(1.0, sud))

    # Check for SUD-related fiscal events (treatment utilization)
    sud_events = sum(
        1 for e in fh
        if "substance" in e.service_category.lower()
        or "sud" in e.service_category.lower()
    )
    if sud_events > 0:
        score = max(score, min(1.0, 0.3 + sud_events * 0.1))

    return score


def _signal_incarceration(
    ps: PersonBudgetKey,
    dm: DomeMetrics,
    fh: list[FiscalEvent],
) -> float:
    """Detect incarceration: past 12 months jail/prison days > 0."""
    score = 0.0

    total_days = ps.past_12m_jail_days + ps.past_12m_prison_days
    if total_days > 0:
        # Scale: 1-30 days -> 0.5-0.7, 30-365 -> 0.7-1.0
        score = max(score, min(1.0, 0.5 + total_days / 730))

    if ps.justice_involvement_flag:
        score = max(score, 0.4)

    # Police contacts as a weaker signal
    if ps.past_12m_police_contacts > 0:
        score = max(score, min(0.6, 0.2 + ps.past_12m_police_contacts * 0.1))

    return score


def _signal_poverty(
    ps: PersonBudgetKey,
    dm: DomeMetrics,
    fh: list[FiscalEvent],
) -> float:
    """Detect poverty: income < $15,000 or unemployment/NILF."""
    score = 0.0

    if ps.current_annual_income is not None:
        if ps.current_annual_income < 15_000:
            # Deep poverty
            if ps.current_annual_income < 7_500:
                score = max(score, 1.0)
            else:
                score = max(score, 0.6 + 0.4 * (15_000 - ps.current_annual_income) / 7_500)

    if ps.employment_status in ("unemployed", "NILF"):
        score = max(score, 0.7)

    return score


def _signal_environmental_hazard(
    ps: PersonBudgetKey,
    dm: DomeMetrics,
    fh: list[FiscalEvent],
) -> float:
    """Detect environmental hazard: ADI > 80 or housing quality < 3."""
    score = 0.0

    if ps.area_deprivation_index is not None and ps.area_deprivation_index > 80:
        score = max(score, min(1.0, 0.5 + (ps.area_deprivation_index - 80) * 0.025))

    hq = dm.environmental_layer.get("housing_quality_score")
    if hq is not None and hq < 3:
        score = max(score, min(1.0, 1.0 - hq / 5))

    # Lead exposure specifically
    lead = dm.environmental_layer.get("lead_exposure_risk")
    if lead is not None and lead > 0.5:
        score = max(score, min(1.0, lead))

    return score


def _signal_high_utilization(
    ps: PersonBudgetKey,
    dm: DomeMetrics,
    fh: list[FiscalEvent],
) -> float:
    """Detect high healthcare utilization from fiscal history and metrics."""
    score = 0.0

    # Count healthcare fiscal events in past 12 months
    hc_events = sum(1 for e in fh if e.domain == "healthcare")
    if hc_events > 10:
        score = max(score, min(1.0, 0.5 + hc_events * 0.02))

    # Total healthcare spending
    hc_spend = sum(e.amount_paid for e in fh if e.domain == "healthcare")
    if hc_spend > 50_000:
        score = max(score, min(1.0, 0.6 + (hc_spend - 50_000) / 200_000))

    if ps.high_need_flag:
        score = max(score, 0.8)

    return score


def _signal_employment_barrier(
    ps: PersonBudgetKey,
    dm: DomeMetrics,
    fh: list[FiscalEvent],
) -> float:
    """Detect employment barriers: justice history + unemployment."""
    score = 0.0

    if ps.justice_involvement_flag and ps.employment_status in ("unemployed", "NILF"):
        score = max(score, 0.85)
    elif ps.justice_involvement_flag:
        score = max(score, 0.5)
    elif ps.employment_status in ("unemployed", "NILF"):
        score = max(score, 0.4)

    # Low education as barrier
    if ps.educational_attainment in ("<HS",):
        score = max(score, max(score * 1.1, 0.3))

    return min(score, 1.0)


def _signal_cognitive_impairment(
    ps: PersonBudgetKey,
    dm: DomeMetrics,
    fh: list[FiscalEvent],
) -> float:
    """Detect cognitive impairment from clinical/education data."""
    score = 0.0

    cog = dm.clinical_layer.get("cognitive_score")
    if cog is not None and cog < 70:
        score = max(score, min(1.0, (100 - cog) / 50))

    # Special education history
    if dm.institutional_layer.get("special_education_history"):
        score = max(score, 0.5)

    # Lead exposure as a contributing factor
    lead = dm.environmental_layer.get("blood_lead_level")
    if lead is not None and lead > 5:
        score = max(score, min(1.0, 0.3 + lead * 0.05))

    return score


def _signal_educational_failure(
    ps: PersonBudgetKey,
    dm: DomeMetrics,
    fh: list[FiscalEvent],
) -> float:
    """Detect educational failure: less than HS credential."""
    score = 0.0

    if ps.educational_attainment == "<HS":
        score = max(score, 0.9)

    literacy = dm.institutional_layer.get("literacy_score")
    if literacy is not None and literacy < 200:
        score = max(score, min(1.0, (250 - literacy) / 150))

    return score


def _signal_low_earnings(
    ps: PersonBudgetKey,
    dm: DomeMetrics,
    fh: list[FiscalEvent],
) -> float:
    """Detect persistently low earnings."""
    score = 0.0

    if ps.current_annual_income is not None and ps.current_annual_income < 20_000:
        score = max(score, min(1.0, 0.5 + (20_000 - ps.current_annual_income) / 20_000))

    if ps.employment_status in ("PT", "gig"):
        score = max(score, 0.4)

    return score


def _signal_program_dependence(
    ps: PersonBudgetKey,
    dm: DomeMetrics,
    fh: list[FiscalEvent],
) -> float:
    """Detect high program dependence from enrollment and fiscal history."""
    score = 0.0

    # Count distinct programs in fiscal history
    programs = {e.program_or_fund for e in fh if e.domain in (
        "income_support", "food", "housing"
    )}
    if len(programs) >= 3:
        score = max(score, min(1.0, 0.5 + len(programs) * 0.1))

    enrolled_count = sum([
        ps.enrollment_snapshot.medicaid,
        ps.enrollment_snapshot.snap,
        ps.enrollment_snapshot.tanf,
        ps.enrollment_snapshot.housing_assistance,
        ps.enrollment_snapshot.ssi,
        ps.enrollment_snapshot.ssdi,
    ])
    if enrolled_count >= 3:
        score = max(score, min(1.0, 0.5 + enrolled_count * 0.1))

    return score


def _signal_health_deterioration(
    ps: PersonBudgetKey,
    dm: DomeMetrics,
    fh: list[FiscalEvent],
) -> float:
    """Detect health deterioration from biometric and clinical signals."""
    score = 0.0

    if ps.chronic_condition_flags:
        score = max(score, min(1.0, 0.4 + len(ps.chronic_condition_flags) * 0.15))

    hba1c = dm.biometric_layer.get("hba1c")
    if hba1c is not None and hba1c > 8.0:
        score = max(score, min(1.0, 0.5 + (hba1c - 8.0) * 0.1))

    bp_sys = dm.biometric_layer.get("blood_pressure_systolic")
    if bp_sys is not None and bp_sys > 160:
        score = max(score, 0.7)

    return score


def _signal_respiratory_disease(
    ps: PersonBudgetKey,
    dm: DomeMetrics,
    fh: list[FiscalEvent],
) -> float:
    """Detect respiratory disease from conditions list and clinical data."""
    score = 0.0

    respiratory_conditions = {"asthma", "copd", "chronic_bronchitis", "emphysema",
                              "pulmonary_fibrosis", "J44", "J45", "J43"}
    for cond in ps.chronic_condition_flags:
        if cond.lower() in respiratory_conditions or cond.startswith("J4"):
            score = max(score, 0.8)
            break

    fev1 = dm.biometric_layer.get("fev1_pct_predicted")
    if fev1 is not None and fev1 < 60:
        score = max(score, min(1.0, 0.5 + (80 - fev1) / 60))

    return score


def _signal_work_limitation(
    ps: PersonBudgetKey,
    dm: DomeMetrics,
    fh: list[FiscalEvent],
) -> float:
    """Detect work limitation from disability and functional data."""
    score = 0.0

    if ps.disability_flag:
        score = max(score, 0.7)

    func_limit = dm.biometric_layer.get("functional_limitations_score")
    if func_limit is not None and func_limit > 30:
        score = max(score, min(1.0, func_limit / 100))

    if ps.employment_status == "disabled":
        score = max(score, 0.9)

    return score


def _signal_income_loss(
    ps: PersonBudgetKey,
    dm: DomeMetrics,
    fh: list[FiscalEvent],
) -> float:
    """Detect income loss from economic indicators."""
    score = 0.0

    prior_income = dm.economic_layer.get("prior_annual_income")
    if prior_income and prior_income > 0 and ps.current_annual_income is not None:
        drop = 1.0 - (ps.current_annual_income / prior_income)
        if drop > 0.3:
            score = max(score, min(1.0, drop))

    if ps.employment_status in ("unemployed", "NILF", "disabled"):
        score = max(score, 0.6)

    return score


def _signal_family_stress(
    ps: PersonBudgetKey,
    dm: DomeMetrics,
    fh: list[FiscalEvent],
) -> float:
    """Detect family stress from social layer and economic indicators."""
    score = 0.0

    caregiving = dm.social_layer.get("caregiving_burden_score")
    if caregiving is not None and caregiving > 50:
        score = max(score, min(1.0, caregiving / 100))

    # Economic stress with dependents
    if ps.dependents_ages and ps.current_annual_income is not None:
        per_person = ps.current_annual_income / max(1, ps.household_size)
        if per_person < 10_000:
            score = max(score, min(1.0, 0.5 + (10_000 - per_person) / 10_000))

    family_stress = dm.social_layer.get("family_stress_score")
    if family_stress is not None and family_stress > 0.5:
        score = max(score, min(1.0, family_stress))

    return score


def _signal_justice_involvement(
    ps: PersonBudgetKey,
    dm: DomeMetrics,
    fh: list[FiscalEvent],
) -> float:
    """Detect justice involvement from justice indicators."""
    score = 0.0

    if ps.past_12m_jail_days > 0 or ps.past_12m_prison_days > 0:
        score = max(score, 0.8)

    if ps.past_12m_police_contacts > 0:
        score = max(score, min(0.7, 0.3 + ps.past_12m_police_contacts * 0.1))

    if ps.justice_involvement_flag:
        score = max(score, 0.5)

    # Justice-domain fiscal events
    justice_events = sum(1 for e in fh if e.domain == "justice")
    if justice_events > 0:
        score = max(score, min(0.8, 0.3 + justice_events * 0.1))

    return score


def _signal_incarceration_cost(
    ps: PersonBudgetKey,
    dm: DomeMetrics,
    fh: list[FiscalEvent],
) -> float:
    """Detect incarceration-level cost from justice fiscal events."""
    score = 0.0

    total_days = ps.past_12m_jail_days + ps.past_12m_prison_days
    if total_days > 30:
        score = max(score, min(1.0, 0.5 + total_days / 365))

    justice_spend = sum(e.amount_paid for e in fh if e.domain == "justice")
    if justice_spend > 20_000:
        score = max(score, min(1.0, 0.5 + (justice_spend - 20_000) / 100_000))

    return score


def _signal_medical_crisis(
    ps: PersonBudgetKey,
    dm: DomeMetrics,
    fh: list[FiscalEvent],
) -> float:
    """Detect medical crisis from ER visits and inpatient stays."""
    score = 0.0

    er_visits = sum(
        1 for e in fh
        if e.service_category.lower() in ("er", "emergency", "inpatient", "icu")
    )
    if er_visits > 3:
        score = max(score, min(1.0, 0.5 + er_visits * 0.05))

    hc_crisis_spend = sum(
        e.amount_paid for e in fh
        if e.domain == "healthcare"
        and e.service_category.lower() in ("er", "emergency", "inpatient", "icu")
    )
    if hc_crisis_spend > 30_000:
        score = max(score, min(1.0, 0.5 + (hc_crisis_spend - 30_000) / 100_000))

    return score


def _signal_lead_exposure(
    ps: PersonBudgetKey,
    dm: DomeMetrics,
    fh: list[FiscalEvent],
) -> float:
    """Detect lead exposure from environmental data."""
    score = 0.0

    bll = dm.environmental_layer.get("blood_lead_level")
    if bll is not None and bll > 3.5:
        score = max(score, min(1.0, 0.3 + bll * 0.07))

    lead_risk = dm.environmental_layer.get("lead_exposure_risk")
    if lead_risk is not None and lead_risk > 0.5:
        score = max(score, min(1.0, lead_risk))

    # Old housing in high-ADI area
    if (ps.area_deprivation_index is not None and ps.area_deprivation_index > 85):
        housing_year = dm.environmental_layer.get("housing_year_built")
        if housing_year is not None and housing_year < 1978:
            score = max(score, 0.6)

    return score


def _signal_high_cost(
    ps: PersonBudgetKey,
    dm: DomeMetrics,
    fh: list[FiscalEvent],
) -> float:
    """Detect high-cost pattern from total fiscal events."""
    score = 0.0

    total_spend = sum(e.amount_paid for e in fh)
    if total_spend > 80_000:
        score = max(score, min(1.0, 0.5 + (total_spend - 80_000) / 200_000))

    if ps.high_need_flag:
        score = max(score, 0.8)

    return score


# ---------------------------------------------------------------------------
# Signal dispatch table
# ---------------------------------------------------------------------------
# Maps each cascade event label to its signal detection function.

SIGNAL_FUNCTIONS: dict[str, SignalFn] = {
    "job_loss": _signal_job_loss,
    "depression": _signal_depression,
    "chronic_disease": _signal_chronic_disease,
    "high_utilization": _signal_high_utilization,
    "lead_exposure": _signal_lead_exposure,
    "cognitive_impairment": _signal_cognitive_impairment,
    "educational_failure": _signal_educational_failure,
    "low_earnings": _signal_low_earnings,
    "program_dependence": _signal_program_dependence,
    "incarceration": _signal_incarceration,
    "employment_barrier": _signal_employment_barrier,
    "social_isolation": _signal_social_isolation,
    "housing_instability": _signal_housing_instability,
    "health_deterioration": _signal_health_deterioration,
    "high_cost": _signal_high_cost,
    "substance_use": _signal_substance_use,
    "medical_crisis": _signal_medical_crisis,
    "environmental_hazard": _signal_environmental_hazard,
    "respiratory_disease": _signal_respiratory_disease,
    "work_limitation": _signal_work_limitation,
    "income_loss": _signal_income_loss,
    "poverty": _signal_poverty,
    "family_stress": _signal_family_stress,
    "justice_involvement": _signal_justice_involvement,
    "incarceration_cost": _signal_incarceration_cost,
}


# ---------------------------------------------------------------------------
# Unit cost estimates for cascade terminal nodes
# ---------------------------------------------------------------------------
# Maps cascade terminal/intermediate events to estimated annual public cost.

EVENT_ANNUAL_COSTS: dict[str, float] = {
    "job_loss": 9_880.0,              # UI benefits
    "depression": 10_000.0,           # MH treatment + lost productivity
    "chronic_disease": 16_500.0,      # Medicaid cost for chronically ill
    "high_utilization": 55_000.0,     # Super-utilizer annual cost
    "lead_exposure": 5_000.0,         # Remediation + testing
    "cognitive_impairment": 20_000.0, # Special education
    "educational_failure": 16_000.0,  # K-12 per pupil + remediation
    "low_earnings": 8_000.0,          # Transfer payments
    "program_dependence": 25_000.0,   # Multi-program cost
    "incarceration": 47_500.0,        # Prison year
    "employment_barrier": 12_000.0,   # UI + support services
    "social_isolation": 5_000.0,      # Social services
    "housing_instability": 40_000.0,  # Chronic homelessness cost
    "health_deterioration": 30_000.0, # Chronic disease management
    "high_cost": 80_000.0,            # Multi-system super-utilizer
    "substance_use": 20_000.0,        # SUD treatment
    "medical_crisis": 60_000.0,       # ER + inpatient crisis
    "environmental_hazard": 7_500.0,  # Remediation
    "respiratory_disease": 15_000.0,  # Pulmonary treatment
    "work_limitation": 10_500.0,      # SSI/SSDI
    "income_loss": 15_000.0,          # Transfer programs
    "poverty": 12_000.0,              # Multi-benefit cost
    "family_stress": 8_000.0,         # Family services
    "justice_involvement": 20_000.0,  # Court + supervision
    "incarceration_cost": 47_500.0,   # Prison year
}


class CascadeDetector:
    """Real-time cascade detection engine.

    Scans a person's state against all six canonical cascade definitions
    and returns alerts for every cascade where at least the first cause
    event is active.

    Parameters
    ----------
    cascade_definitions : list[CascadeDefinition] | None
        Custom cascade definitions to use.  Defaults to the built-in
        ``CASCADE_DEFINITIONS`` from :mod:`dome.data.cascades`.
    min_confidence : float
        Minimum confidence threshold to emit an alert (default 0.2).
    """

    def __init__(
        self,
        cascade_definitions: list[CascadeDefinition] | None = None,
        min_confidence: float = 0.2,
    ) -> None:
        self.cascade_definitions = cascade_definitions or CASCADE_DEFINITIONS
        self.min_confidence = min_confidence

    # ------------------------------------------------------------------ #
    # Public API
    # ------------------------------------------------------------------ #

    def detect(
        self,
        person_state: PersonBudgetKey,
        dome_metrics: DomeMetrics,
        fiscal_history: list[FiscalEvent],
    ) -> list[CascadeAlert]:
        """Run cascade detection for a single person.

        Parameters
        ----------
        person_state : PersonBudgetKey
            The person's budget-key attributes (demographics, income,
            employment, housing, justice involvement, etc.).
        dome_metrics : DomeMetrics
            Nine-layer DOME metrics snapshot with clinical, behavioral,
            economic, environmental, social, and other indicators.
        fiscal_history : list[FiscalEvent]
            Chronological list of fiscal events for this person.

        Returns
        -------
        list[CascadeAlert]
            Alerts for all cascades in which the person shows active
            signals, sorted by descending confidence.
        """
        alerts: list[CascadeAlert] = []

        for cascade_def in self.cascade_definitions:
            alert = self._evaluate_cascade(
                cascade_def, person_state, dome_metrics, fiscal_history
            )
            if alert is not None and alert.confidence >= self.min_confidence:
                alerts.append(alert)

        # Sort by confidence descending, then by projected savings descending
        alerts.sort(
            key=lambda a: (
                a.confidence,
                a.path_a_projected_cost - a.path_b_projected_cost,
            ),
            reverse=True,
        )
        return alerts

    # ------------------------------------------------------------------ #
    # Internal methods
    # ------------------------------------------------------------------ #

    def _evaluate_cascade(
        self,
        cascade_def: CascadeDefinition,
        ps: PersonBudgetKey,
        dm: DomeMetrics,
        fh: list[FiscalEvent],
    ) -> CascadeAlert | None:
        """Evaluate a single cascade definition against the person's state.

        Returns a ``CascadeAlert`` if the person shows active signals for
        at least the first link's cause event, or ``None`` otherwise.
        """
        links = cascade_def.links
        if not links:
            return None

        # Step 1: Evaluate signal strength at each link position.
        #
        # A link is "active" when its *cause* signal is present.  We track
        # the furthest contiguous link index where the cause is detected.
        signal_strengths: list[float] = []
        current_link_index = -1

        for i, link in enumerate(links):
            cause_signal = self._get_signal(link.cause, ps, dm, fh)
            signal_strengths.append(cause_signal)

            if cause_signal > 0.2:
                current_link_index = i
            else:
                # Chain broken — don't look further ahead for contiguous
                # progression (though isolated signals are still recorded)
                break

        # Also check if the final effect in the chain is already present
        final_effect_signal = self._get_signal(links[-1].effect, ps, dm, fh)
        if final_effect_signal > 0.2 and current_link_index == len(links) - 1:
            # The cascade has fully materialized
            pass

        # No active signals at all — skip this cascade
        if current_link_index < 0:
            return None

        # Step 2: Compute confidence.
        #
        # Confidence = weighted average of (signal_strength × link_strength)
        # for all active links, normalized to [0, 1].
        active_count = current_link_index + 1
        weighted_sum = 0.0
        weight_total = 0.0
        for i in range(active_count):
            w = links[i].strength
            weighted_sum += signal_strengths[i] * w
            weight_total += w

        confidence = weighted_sum / weight_total if weight_total > 0 else 0.0
        confidence = max(0.0, min(1.0, confidence))

        # Step 3: Project Path A cost (do nothing).
        #
        # From the current link onward, compute expected cost using the
        # chain of transition probabilities and per-event annual costs,
        # projected over an estimated cascade horizon (5 years).
        path_a_cost = self._project_path_a_cost(
            links, current_link_index, signal_strengths
        )

        # Step 4: Identify interventions and project Path B cost.
        recommended_interventions: list[str] = []
        path_b_cost = self._project_path_b_cost(
            links, current_link_index, signal_strengths,
            recommended_interventions,
        )

        return CascadeAlert(
            person_uid=ps.person_uid,
            cascade_id=cascade_def.cascade_id,
            current_link_index=current_link_index,
            confidence=round(confidence, 4),
            detected_at=datetime.now(timezone.utc),
            path_a_projected_cost=round(path_a_cost, 2),
            path_b_projected_cost=round(path_b_cost, 2),
            recommended_interventions=recommended_interventions,
        )

    def _get_signal(
        self,
        event_label: str,
        ps: PersonBudgetKey,
        dm: DomeMetrics,
        fh: list[FiscalEvent],
    ) -> float:
        """Look up and invoke the signal function for an event label.

        Returns 0.0 if no signal function is registered for the label.
        """
        fn = SIGNAL_FUNCTIONS.get(event_label)
        if fn is None:
            return 0.0
        return fn(ps, dm, fh)

    def _project_path_a_cost(
        self,
        links: list[CascadeLink],
        current_link_index: int,
        signal_strengths: list[float],
    ) -> float:
        """Project the total public cost if the cascade runs without intervention.

        The projection sums:
        1. Costs already being incurred for active links.
        2. Expected future costs for remaining links, discounted by
           transition probability and time.

        All costs are projected over a default 5-year cascade horizon.
        """
        cascade_horizon_years = 5
        discount_rate = 0.03

        total_cost = 0.0

        # Costs already being incurred (active links)
        for i in range(current_link_index + 1):
            link = links[i]
            cause_cost = EVENT_ANNUAL_COSTS.get(link.cause, 10_000.0)
            # Scale by signal strength — stronger signal means fuller cost
            annual_cost = cause_cost * signal_strengths[i]
            # Project over remaining horizon with discount
            for yr in range(cascade_horizon_years):
                total_cost += annual_cost / (1 + discount_rate) ** yr

        # Costs for the effect of the current active link (partially realized)
        if current_link_index < len(links):
            current_link = links[current_link_index]
            effect_cost = EVENT_ANNUAL_COSTS.get(current_link.effect, 15_000.0)
            prob = current_link.probability
            avg_lag_years = (
                (current_link.lag_months_min + current_link.lag_months_max) / 2 / 12
            )
            for yr in range(cascade_horizon_years):
                if yr >= avg_lag_years:
                    total_cost += (
                        effect_cost * prob / (1 + discount_rate) ** yr
                    )

        # Future cascade links (not yet active)
        cumulative_probability = 1.0
        for i in range(current_link_index + 1, len(links)):
            link = links[i]
            cumulative_probability *= link.probability
            effect_cost = EVENT_ANNUAL_COSTS.get(link.effect, 15_000.0)
            avg_lag_years = (
                (link.lag_months_min + link.lag_months_max) / 2 / 12
            )
            # Project expected cost discounted by cumulative probability
            for yr in range(cascade_horizon_years):
                if yr >= avg_lag_years:
                    total_cost += (
                        effect_cost * cumulative_probability
                        / (1 + discount_rate) ** yr
                    )

        return total_cost

    def _project_path_b_cost(
        self,
        links: list[CascadeLink],
        current_link_index: int,
        signal_strengths: list[float],
        recommended_interventions: list[str],
    ) -> float:
        """Project cost under the intervention path.

        Assumes that the best available intervention targets the current or
        next link, breaking the cascade chain.  If the break succeeds, only
        the intervention cost and already-incurred costs remain.  If it
        fails, costs are reduced by 50% (severity attenuation).

        Populates ``recommended_interventions`` in-place.
        """
        cascade_horizon_years = 5
        discount_rate = 0.03

        # Already-incurred costs (same as Path A for active links)
        total_cost = 0.0
        for i in range(current_link_index + 1):
            link = links[i]
            cause_cost = EVENT_ANNUAL_COSTS.get(link.cause, 10_000.0)
            annual_cost = cause_cost * signal_strengths[i]
            for yr in range(cascade_horizon_years):
                total_cost += annual_cost / (1 + discount_rate) ** yr

        # Identify the best intervention for the current/next link
        target_link_index = min(current_link_index, len(links) - 1)
        target_link = links[target_link_index]
        link_label = f"{target_link.cause}->{target_link.effect}"

        # Also check the next link if available
        next_link_label = None
        if target_link_index + 1 < len(links):
            next_link = links[target_link_index + 1]
            next_link_label = f"{next_link.cause}->{next_link.effect}"

        # Find interventions for the target link
        interventions = INTERVENTION_INDEX.get(link_label, [])
        if not interventions and next_link_label:
            interventions = INTERVENTION_INDEX.get(next_link_label, [])

        best_break_prob = 0.0
        intervention_cost = 0.0

        for intv in interventions:
            recommended_interventions.append(intv.intervention_id)
            if intv.break_probability > best_break_prob:
                best_break_prob = intv.break_probability
                intervention_cost = (intv.cost_min + intv.cost_max) / 2

        # If we also have interventions for the next link, include them
        if next_link_label and link_label != next_link_label:
            next_interventions = INTERVENTION_INDEX.get(next_link_label, [])
            for intv in next_interventions:
                if intv.intervention_id not in recommended_interventions:
                    recommended_interventions.append(intv.intervention_id)

        if best_break_prob > 0:
            # Add intervention cost
            total_cost += intervention_cost

            # If break succeeds: no further cascade costs
            # If break fails: 50% of remaining cascade costs
            path_a_remaining = self._remaining_cascade_cost(
                links, current_link_index, cascade_horizon_years, discount_rate
            )
            expected_remaining = (
                (1 - best_break_prob) * path_a_remaining * 0.5
            )
            total_cost += expected_remaining
        else:
            # No intervention available — same cost as Path A for remaining
            total_cost += self._remaining_cascade_cost(
                links, current_link_index, cascade_horizon_years, discount_rate
            )

        return total_cost

    def _remaining_cascade_cost(
        self,
        links: list[CascadeLink],
        current_link_index: int,
        horizon_years: int,
        discount_rate: float,
    ) -> float:
        """Compute the expected remaining cascade cost from future links."""
        total = 0.0
        cumulative_probability = 1.0

        for i in range(current_link_index, len(links)):
            link = links[i]
            cumulative_probability *= link.probability
            effect_cost = EVENT_ANNUAL_COSTS.get(link.effect, 15_000.0)
            avg_lag_years = (
                (link.lag_months_min + link.lag_months_max) / 2 / 12
            )
            for yr in range(horizon_years):
                if yr >= avg_lag_years:
                    total += (
                        effect_cost * cumulative_probability
                        / (1 + discount_rate) ** yr
                    )

        return total
