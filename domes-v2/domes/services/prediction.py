"""
DOMES v2 — Crisis Prediction Engine
=====================================

The computational core of "pointing a data center at one human."

This module answers a single question: *what is about to happen to Robert Jackson,
and what is the cheapest intervention to prevent it?*

Design philosophy
-----------------
Every prediction is a **causal claim**, not a statistical curiosity. We don't say
"probability of ER visit = 0.73" and stop. We say *why* — which signals drove it,
which causal pathway is activating, what the leverage point is, and how long the
window for action remains open.

The model is deliberately Bayesian in structure, not because of computational
sophistication but because Bayes forces us to state our priors explicitly. For
a 45-year-old man with schizoaffective disorder, 7+ years of chronic homelessness,
and 47 ER visits per year, our priors are not vague. They are *tragic and precise*.

Compute budget framing
-----------------------
This engine is the thought-experiment instantiation of 3×10²¹ FLOPS over 5 years
directed at one person. At that compute scale, uncertainty about any individual
should collapse toward near-certainty. This engine models that collapse — showing
how each additional observation reduces our uncertainty about Robert Jackson's
next crisis, and therefore increases the precision of our intervention.

The "compute budget tracker" is not aspirational: at frontier model scale (e.g.,
GPT-4 inference ≈ 1×10¹² FLOPS per token), 3×10²¹ FLOPS over 5 years allows
roughly 3×10⁹ full-context inference calls on a model trained specifically on
Robert Jackson's data. That is one inference call every 53 milliseconds, around
the clock, for 5 years. This engine models what that continuous inference yields.

Reference population
---------------------
Robert Jackson: 45yo male, chronically homeless 7+ years, schizoaffective
disorder (bipolar type), 47 ER visits/year, $112,100 fragmented annual cost,
active in 9 government systems (Medicaid, CMHC, HMIS emergency shelter, SNAP,
SSDI, probation, ACT team, county jail, 988 crisis line).
"""
from __future__ import annotations

import math
import uuid
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta, timezone
from enum import Enum
from typing import Any

__all__ = [
    # Output dataclasses
    "CrisisHorizon",
    "RiskPrediction",
    "InterventionOption",
    "CausalSignal",
    "CausalPathway",
    "InterventionScore",
    "ComputeBudgetState",
    "RiskDashboard",
    # Main service
    "CrisisPredictionEngine",
    # Enums
    "CrisisType",
    "InterventionType",
    "SignalStrength",
]

# ---------------------------------------------------------------------------
# Utility constants — Robert Jackson's known epidemiological profile
# ---------------------------------------------------------------------------

# Annual base rates derived from literature on chronically homeless adults
# with schizoaffective disorder and high ER utilization.
# Sources: HCH Clinicians' Network, Medicaid high-utilizer studies, SAMHSA TEDS.
_ANNUAL_ER_VISITS_BASE = 47.0          # Robert Jackson's actual rate
_ANNUAL_PSYCH_CRISIS_BASE = 8.0        # Psychiatric emergencies per year (estimated)
_ANNUAL_HOSP_BASE = 2.3                # Inpatient hospitalizations per year
_ANNUAL_INCARCERATION_BASE = 0.85      # Probability of at least one booking per year
_ANNUAL_MORTALITY_RATE = 0.042         # Premature mortality: ~3–5× population rate
_ANNUAL_HOUSING_LOSS_BASE = 0.65       # Probability of losing temporary shelter per year

# Cost constants (USD, 2024)
_COST_ER_VISIT = 3_200.0
_COST_PSYCH_HOSPITALIZATION = 18_500.0
_COST_MEDICAL_HOSPITALIZATION = 22_800.0
_COST_INCARCERATION_30D = 4_200.0
_COST_CRISIS_TEAM_OUTREACH = 450.0
_COST_ACT_TEAM_VISIT = 280.0
_COST_MEDICATION_RECONCILIATION = 120.0
_COST_SHELTER_PLACEMENT = 85.0         # Per night, emergency shelter
_COST_WARMING_CENTER = 25.0            # Per night, hypothermia prevention

# Days in common horizons
_HOURS_24 = 1 / 365.0
_DAYS_3 = 3 / 365.0
_DAYS_7 = 7 / 365.0
_DAYS_30 = 30 / 365.0
_DAYS_90 = 90 / 365.0
_DAYS_365 = 1.0

# Medication adherence thresholds
_MPR_ADHERENT = 0.80        # Medication Possession Ratio ≥ 0.80 = adherent
_ANTIPSYCHOTIC_GAP_CRISIS_DAYS = 7   # Days without antipsychotic before psychosis risk multiplies
_ANTIPSYCHOTIC_GAP_CRITICAL_DAYS = 14  # Beyond this: high probability of active psychosis

# Temperature danger thresholds (°F, ambient)
_HYPOTHERMIA_RISK_TEMP = 40.0         # Below this: unsheltered person at risk
_HYPOTHERMIA_CRITICAL_TEMP = 28.0     # Below this: life-threatening for unsheltered
_HEAT_RISK_TEMP = 95.0                # Above this: heat illness risk (especially on antipsychotics)
_HEAT_CRITICAL_TEMP = 105.0           # Heat index above this: life-threatening

# Assessment score thresholds
_PHQ9_SEVERE = 20           # PHQ-9 ≥ 20 = severe depression
_PHQ9_MOD_SEVERE = 15       # PHQ-9 15–19 = moderately severe
_CSSRS_ACTIVE_IDEATION = 2  # C-SSRS ideation intensity ≥ 2 = active ideation
_GAF_SEVERE = 30            # GAF ≤ 30 = severely impaired functioning
_PANSS_POSITIVE_HIGH = 28   # PANSS positive subscale ≥ 28 = severe positive symptoms


# ---------------------------------------------------------------------------
# Enums specific to the prediction engine
# ---------------------------------------------------------------------------

class CrisisType(str, Enum):
    """Types of crisis events the prediction engine forecasts."""
    ER_VISIT = "er_visit"
    PSYCHIATRIC_CRISIS = "psychiatric_crisis"
    HOSPITALIZATION_PSYCHIATRIC = "hospitalization_psychiatric"
    HOSPITALIZATION_MEDICAL = "hospitalization_medical"
    INCARCERATION = "incarceration"
    MORTALITY = "mortality"
    HOUSING_LOSS = "housing_loss"


class InterventionType(str, Enum):
    """Intervention modalities — ranked by cost-effectiveness for this population."""
    CRISIS_TEAM_OUTREACH = "crisis_team_outreach"
    ACT_TEAM_CONTACT = "act_team_contact"
    MEDICATION_RECONCILIATION = "medication_reconciliation"
    MEDICATION_DEPOT_INJECTION = "medication_depot_injection"  # Long-acting injectable
    SHELTER_PLACEMENT = "shelter_placement"
    WARMING_CENTER_REFERRAL = "warming_center_referral"
    COOLING_CENTER_REFERRAL = "cooling_center_referral"
    BENEFIT_REINSTATEMENT = "benefit_reinstatement"
    PEER_SUPPORT_CONTACT = "peer_support_contact"
    CARE_COORDINATION_CALL = "care_coordination_call"
    CASE_MANAGEMENT_VISIT = "case_management_visit"
    CRISIS_LINE_CALLBACK = "crisis_line_callback"
    HOSPITAL_DIVERSION = "hospital_diversion"
    LEGAL_AID_REFERRAL = "legal_aid_referral"


class SignalStrength(str, Enum):
    """Confidence in a causal signal."""
    STRONG = "strong"       # Signal clearly present, multiple corroborating sources
    MODERATE = "moderate"   # Signal present, limited corroboration
    WEAK = "weak"           # Signal inferred, not directly observed
    ABSENT = "absent"       # Signal checked and not present


class CrisisHorizon(str, Enum):
    """Prediction time horizons."""
    H24 = "24h"
    H72 = "72h"
    D7 = "7d"
    D30 = "30d"
    D90 = "90d"
    D365 = "365d"


# ---------------------------------------------------------------------------
# Data classes for prediction outputs
# ---------------------------------------------------------------------------

@dataclass
class CausalSignal:
    """
    A single causal signal contributing to a risk prediction.

    A signal is an observable fact about a person's current state that causally
    increases (or decreases) the probability of a downstream crisis event.
    Signals are distinct from correlations: we only include signals for which
    a plausible causal mechanism is known from the clinical literature.
    """
    name: str
    description: str
    strength: SignalStrength
    direction: str          # "increases_risk" | "decreases_risk" | "modulates"
    magnitude: float        # Multiplicative effect on base rate (e.g., 2.3 = 2.3× baseline)
    data_source: str        # Which DOMES table/system this came from
    last_updated: datetime | None = None
    confidence: float = 0.0  # 0.0–1.0: how confident we are this signal is accurately measured


@dataclass
class CausalPathway:
    """
    A causal chain from an upstream condition to a downstream crisis.

    Represents the mechanistic path — the *story* of how a crisis unfolds.
    Each node is an observable or inferable state. The pathway is what separates
    a prediction from a correlation: we can point to exactly where in the chain
    an intervention would break the sequence.
    """
    pathway_id: str
    name: str
    nodes: list[str]            # Ordered list of causal states (→ separated narrative)
    intervention_point: str     # The optimal node to intervene at (lowest cost, highest impact)
    time_to_crisis_days: float  # Expected days from current state to terminal node
    probability_if_no_action: float
    probability_if_intervene: float
    intervention_type: InterventionType
    evidence_quality: str       # "strong_rct" | "observational" | "expert_consensus" | "modeled"


@dataclass
class RiskPrediction:
    """
    A single crisis risk prediction for a specific crisis type and time horizon.

    This is the primary output unit of the prediction engine. Each prediction
    combines a probability estimate with its full causal explanation — the signals
    that drove it, the pathway it follows, and the intervention leverage point.
    """
    person_id: uuid.UUID
    crisis_type: CrisisType
    horizon: CrisisHorizon
    probability: float          # 0.0–1.0
    probability_ci_lower: float # 90% confidence interval lower bound
    probability_ci_upper: float # 90% confidence interval upper bound
    baseline_probability: float # What the probability would be with no signals active
    risk_multiplier: float      # How much above baseline (probability / baseline_probability)
    risk_level: str             # "low" | "moderate" | "high" | "critical"
    primary_signals: list[CausalSignal] = field(default_factory=list)
    active_pathway: CausalPathway | None = None
    computed_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    flops_consumed: float = 0.0  # Estimated FLOPS used to compute this prediction
    narrative: str = ""          # Plain-language explanation for a clinician

    def __post_init__(self):
        """Derive risk level from probability."""
        if self.probability >= 0.75:
            self.risk_level = "critical"
        elif self.probability >= 0.50:
            self.risk_level = "high"
        elif self.probability >= 0.25:
            self.risk_level = "moderate"
        else:
            self.risk_level = "low"


@dataclass
class InterventionOption:
    """
    A ranked intervention option for a predicted crisis.

    Provides not just *what* to do but *who* should do it, *when* the window
    closes, and the expected cost-benefit expressed as a number-needed-to-treat
    equivalent. This is the actionable output that turns a prediction into a
    workflow.
    """
    intervention_type: InterventionType
    description: str
    responsible_system: str       # Which of the 9 systems should act
    responsible_role: str         # Specific role (e.g., "ACT team psychiatrist")
    estimated_cost: float         # USD cost of the intervention
    cost_of_inaction: float       # Expected cost if nothing is done (risk-weighted)
    roi_ratio: float              # cost_of_inaction / estimated_cost
    probability_reduction: float  # Absolute reduction in crisis probability
    nnt: float                    # Number-needed-to-treat equivalent
    action_window_hours: float    # How many hours remain before intervention loses effectiveness
    urgency: str                  # "immediate" | "urgent" | "routine" | "preventive"
    specific_actions: list[str] = field(default_factory=list)
    contraindications: list[str] = field(default_factory=list)


@dataclass
class InterventionScore:
    """
    Complete intervention scoring for a single risk prediction.

    Packages the top 3 interventions with their costs, probabilities, and
    who needs to act. This is the clinical decision support output.
    """
    for_prediction: CrisisType
    horizon: CrisisHorizon
    cost_of_inaction: float
    top_interventions: list[InterventionOption] = field(default_factory=list)
    recommended_intervention: InterventionOption | None = None
    composite_action_window_hours: float = 0.0


@dataclass
class ComputeBudgetState:
    """
    Tracks the 5-year compute budget for one person.

    At 3×10²¹ FLOPS over 5 years, this is the most compute ever directed
    at understanding a single human being. This dataclass models what that
    compute *yields* — how fast uncertainty about this person collapses,
    and what the marginal information gain of the next FLOP looks like.

    Key concept: diminishing returns on uncertainty reduction.
    The first 10¹⁸ FLOPS eliminate most population-level uncertainty (we know
    this person is not average). The next 10²⁰ narrow within-person variance
    (we know their rhythms, triggers, and thresholds). The final 10²¹ FLOPs
    are spent on rare-event prediction — the "long tail" of crises that no
    prior model has ever seen in one person's data.
    """
    person_id: uuid.UUID
    budget_total_flops: float = 3e21        # 3×10²¹ FLOPS total
    budget_duration_years: float = 5.0
    flops_consumed: float = 0.0
    flops_consumed_today: float = 0.0

    # Uncertainty metrics
    initial_entropy_bits: float = 47.3      # Shannon entropy at t=0 (population prior)
    current_entropy_bits: float = 47.3      # Decreases as we learn about this person
    uncertainty_reduction_rate: float = 0.0  # bits per 10¹⁸ FLOPS

    # Marginal information
    marginal_info_gain_per_flop: float = 0.0  # bits per FLOP
    estimated_flops_to_certainty: float = 0.0  # FLOPs needed to reach ~1 bit of entropy

    # Knowledge accumulation
    observations_integrated: int = 0
    models_run: int = 0
    predictions_generated: int = 0
    crises_correctly_predicted: int = 0
    crises_successfully_prevented: int = 0

    # Budget utilization
    budget_fraction_consumed: float = 0.0
    projected_flops_at_completion: float = 0.0
    budget_on_track: bool = True

    computed_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def __post_init__(self):
        self._recalculate()

    def _recalculate(self):
        self.budget_fraction_consumed = self.flops_consumed / self.budget_total_flops
        daily_rate = self.budget_total_flops / (self.budget_duration_years * 365.25)
        self.projected_flops_at_completion = self.flops_consumed + (
            daily_rate * self.budget_duration_years * 365.25
        )
        if self.flops_consumed > 0:
            bits_reduced = self.initial_entropy_bits - self.current_entropy_bits
            self.uncertainty_reduction_rate = bits_reduced / (self.flops_consumed / 1e18)
            self.marginal_info_gain_per_flop = max(
                1e-22,
                bits_reduced / self.flops_consumed * math.exp(-self.budget_fraction_consumed)
            )
            if self.marginal_info_gain_per_flop > 0:
                remaining_entropy = max(0.01, self.current_entropy_bits - 1.0)
                self.estimated_flops_to_certainty = remaining_entropy / self.marginal_info_gain_per_flop


@dataclass
class RiskDashboard:
    """
    Complete risk dashboard for one person — the output of predict_all().

    This is the single object that a care coordinator, ACT team psychiatrist,
    or crisis responder sees. It contains every prediction, every intervention
    recommendation, and every causal explanation in one place.

    The dashboard is also the primary interface for the compute budget tracker:
    it records how many FLOPs were consumed to produce it, and what uncertainty
    was reduced in doing so.
    """
    person_id: uuid.UUID
    person_name: str
    generated_at: datetime
    as_of_date: date

    # All predictions organized by crisis type
    predictions: dict[str, list[RiskPrediction]] = field(default_factory=dict)

    # Intervention scores for highest-priority risks
    intervention_scores: list[InterventionScore] = field(default_factory=list)

    # Top-level summary
    highest_priority_crisis: CrisisType | None = None
    highest_priority_horizon: CrisisHorizon | None = None
    highest_priority_probability: float = 0.0
    immediate_action_required: bool = False
    recommended_immediate_action: str = ""

    # Compute budget
    compute_state: ComputeBudgetState | None = None

    # Active causal pathways
    active_pathways: list[CausalPathway] = field(default_factory=list)

    # Cost summary
    total_cost_of_inaction_30d: float = 0.0
    total_cost_of_recommended_interventions: float = 0.0
    projected_annual_savings: float = 0.0

    # Narrative summary for clinicians
    executive_summary: str = ""


# ---------------------------------------------------------------------------
# Synthetic signal generators — model realistic data for Robert Jackson
# ---------------------------------------------------------------------------

def _make_utc(days_ago: float = 0.0) -> datetime:
    return datetime.now(timezone.utc) - timedelta(days=days_ago)


def _robert_jackson_signals(as_of: datetime) -> dict[str, Any]:
    """
    Synthesize Robert Jackson's current observable state.

    This function models what the DOMES engine would *observe* by reading
    across all 9 government systems. In production, each value here would be
    pulled from the corresponding SQLAlchemy model via async SQLAlchemy session.

    The values are calibrated to represent a person in a "pre-crisis drift" state:
    not acutely decompensating, but with multiple slow-moving risk factors that
    are trending in the wrong direction simultaneously.
    """
    return {
        # --- Medication adherence (from pharmacy claims + PDMP) ---
        "antipsychotic_mpr": 0.61,          # Well below 0.80 threshold → non-adherent
        "antipsychotic_last_fill_days_ago": 11,  # 11 days since last fill; 30-day supply means gap
        "antipsychotic_gap_days": 4,        # 4 consecutive days without medication
        "mood_stabilizer_mpr": 0.72,        # Below threshold but better than antipsychotic
        "depot_injection_overdue_days": 0,  # No depot (long-acting injectable) prescribed

        # --- Biometric signals (from wearable, if device provisioned) ---
        "hrv_rmssd_current": 18.2,          # ms; low HRV = physiological stress (normal: 25-65ms)
        "hrv_rmssd_7d_avg": 22.1,           # Trending down = increasing allostatic load
        "resting_hr_current": 94,           # bpm; elevated (normal: 60-100; >90 in this context = stress)
        "sleep_hours_last_night": 3.5,      # Severely disrupted; sleeping rough
        "sleep_hours_7d_avg": 4.8,          # Below 5h average = chronic sleep deprivation
        "skin_temp_deviation": +0.6,        # °C above baseline; subtle fever or inflammation signal
        "electrodermal_activity": 8.2,      # µS; elevated (normal resting 1-5µS) = autonomic arousal
        "steps_yesterday": 6200,            # Reasonable but dropped from 10k avg = less active
        "readiness_score": 28,              # Oura 0-100; <35 = poor physiological readiness

        # --- Environmental signals (from weather API + location) ---
        "ambient_temp_f": 24.0,             # February night; well below hypothermia risk threshold
        "heat_index_f": 24.0,
        "precipitation_mm_24h": 3.2,        # Light precipitation; wet conditions
        "shelter_nights_last_7d": 3,        # Only 3 of last 7 nights in shelter
        "shelter_nights_last_30d": 11,      # Less than 50% shelter utilization
        "unsheltered_consecutive_nights": 2, # 2 consecutive nights without shelter as of tonight

        # --- Encounter pattern signals (from HMIS + ED claims) ---
        "er_visits_last_30d": 4,            # 4 visits in 30 days; slightly above monthly average
        "er_visits_last_7d": 1,             # 1 in last 7 days
        "er_visits_last_90d": 11,           # 11 in 90 days; accelerating (annualizes to ~44)
        "er_visit_acceleration": 1.15,      # Rate increasing 15% vs prior 90-day period
        "days_since_last_er_visit": 6,      # Last ER visit 6 days ago
        "last_er_chief_complaint": "agitation and command hallucinations",
        "last_er_disposition": "discharged to street",

        # --- Assessment trajectory (from CMHC + ACT team records) ---
        "phq9_latest": 18,                  # Moderately severe depression (15-19 range)
        "phq9_prior": 14,                   # Was moderate; trending worse (+4 points in 6 weeks)
        "phq9_trend": "worsening",
        "phq9_days_ago": 42,                # Assessment 6 weeks old; due for reassessment
        "cssrs_intensity_latest": 2,        # Active suicidal ideation (≥2 = active)
        "cssrs_days_ago": 42,               # Same assessment; no recent re-check
        "gaf_latest": 25,                   # Severely impaired (≤30 = severe)
        "panss_positive_latest": 31,        # Severe positive symptoms (>28)
        "panss_days_ago": 62,               # 2 months old; may be worse now

        # --- Enrollment / program gaps (from 9 government systems) ---
        "act_team_days_since_contact": 9,   # ACT team should contact 3x/week; gap detected
        "cmhc_appointment_status": "missed_last_2",  # Missed 2 consecutive CMHC appointments
        "medicaid_status": "active",
        "ssdi_status": "active",
        "snap_days_since_renewal": 280,     # SNAP renewal due in ~85 days; not yet at risk
        "probation_status": "active",
        "probation_next_checkin_days": 3,   # Probation check-in in 3 days; risk of violation
        "shelter_enrollment_status": "active_but_inconsistent",
        "shelter_program_warning": True,    # Program may drop Robert for missed nights

        # --- System fragmentation score ---
        "active_systems": 9,                # 9 systems; each operates independently
        "fragmentation_score": 0.78,        # 0=unified, 1=fully fragmented; 0.78 = high
        "shared_records_fraction": 0.12,    # Only 12% of records shared across systems
        "last_care_coordination_days": 23,  # No care coordination meeting in 23 days
        "duplicate_assessments_90d": 4,     # 4 redundant assessments in 90 days = assessment fatigue

        # --- Calendar / social context ---
        "day_of_week": as_of.strftime("%A"),
        "is_weekend": as_of.weekday() >= 5,
        "days_until_ssdi_payment": 3,       # SSDI arrives in 3 days; pre-payment vulnerability
        "days_since_ssdi_payment": 25,      # 25 days since last payment; funds likely depleted
        "holidays_next_7d": ["None"],       # No holidays in next 7 days
        "month": as_of.month,
        "is_winter": as_of.month in (12, 1, 2, 3),

        # --- Time since any system contact ---
        "days_since_any_contact": 2,        # Last contact 2 days ago (brief shelter check-in)
        "days_since_clinical_contact": 9,   # Last clinical contact = ACT team 9 days ago
    }


# ---------------------------------------------------------------------------
# Causal pathway library
# ---------------------------------------------------------------------------

def _build_pathway_antipsychotic_gap() -> CausalPathway:
    """
    Pathway: Antipsychotic non-adherence → psychotic symptoms → ER visit.

    Clinical evidence: Antipsychotic discontinuation in schizoaffective disorder
    produces psychotic relapse in ~50% of patients within 2 weeks and ~80% within
    6 months (Robinson et al., Am J Psychiatry, 2004). For individuals who are
    homeless, the relapse-to-ER pipeline is nearly guaranteed: there is no family
    or housing safety net to absorb early decompensation.

    The intervention point is medication reconciliation — the cheapest and most
    effective break in this chain ($120 vs. $3,200 ER visit cost).
    """
    return CausalPathway(
        pathway_id="pw_antipsychotic_gap_er",
        name="Antipsychotic gap → psychotic relapse → ER visit",
        nodes=[
            "Antipsychotic medication gap (>4 days without fill)",
            "Dopaminergic dysregulation resumes within 48-72h of last dose",
            "Positive symptoms emerge: hallucinations, disorganized thinking",
            "Behavioral dysregulation in public setting",
            "Law enforcement / bystander 911 call or self-presentation to ED",
            "ER visit (uncompensated, $3,200 avg cost)",
            "Discharge back to street without medication supply → cycle repeats",
        ],
        intervention_point="Antipsychotic medication gap (>4 days without fill)",
        time_to_crisis_days=5.3,
        probability_if_no_action=0.71,
        probability_if_intervene=0.18,
        intervention_type=InterventionType.MEDICATION_RECONCILIATION,
        evidence_quality="strong_rct",
    )


def _build_pathway_hypothermia() -> CausalPathway:
    """
    Pathway: Temperature drop + unsheltered → hypothermia → ER visit / death.

    Hypothermia is the single most preventable cause of death in unsheltered
    homeless adults. At ambient temperatures below 32°F (0°C), a person sleeping
    rough has a meaningful risk of hypothermia within 4-6 hours. The risk is
    dramatically amplified by antipsychotic medications: phenothiazines and
    atypical antipsychotics impair thermoregulation by blocking hypothalamic
    temperature set-point mechanisms.

    Robert Jackson's antipsychotic medication (likely risperidone or quetiapine)
    may paradoxically increase hypothermia risk by 2.5–4× versus an unmedicated
    person in the same conditions.
    """
    return CausalPathway(
        pathway_id="pw_hypothermia_death",
        name="Temp drop + unsheltered + antipsychotic → hypothermia → ER/death",
        nodes=[
            "Ambient temperature drops below 32°F (0°C)",
            "Robert Jackson is unsheltered (2+ consecutive nights)",
            "Antipsychotic medication impairs thermoregulation (2.5–4× risk multiplier)",
            "Core body temperature begins to fall (<95°F = clinical hypothermia)",
            "Altered mental status — mistaken for psychiatric crisis, delays recognition",
            "Severe hypothermia (<90°F) — cardiac arrhythmia risk",
            "ER visit (hypothermia + rhabdomyolysis workup; avg $4,800 cost)",
            "Or death (found unresponsive; 1 in 6 severe hypothermia cases in this population)",
        ],
        intervention_point="Ambient temperature drops below 32°F (0°C)",
        time_to_crisis_days=1.5,
        probability_if_no_action=0.34,
        probability_if_intervene=0.05,
        intervention_type=InterventionType.WARMING_CENTER_REFERRAL,
        evidence_quality="observational",
    )


def _build_pathway_assessment_fatigue() -> CausalPathway:
    """
    Pathway: System fragmentation → repeated assessments → fatigue → disengagement.

    A person touching 9 independent systems is assessed by each system independently.
    In 90 days, Robert Jackson has received 4 overlapping assessments (VI-SPDAT,
    PHQ-9, GAD-7, intake assessment). Each assessment is administered by a different
    worker who does not have access to the prior results. The cumulative effect:

    Assessment fatigue is a well-documented phenomenon in high-utilizer homeless
    service systems (Tsemberis, 2010; Pleace, 2016). It produces active disengagement —
    the person stops showing up for appointments, stops answering outreach calls, and
    ultimately "falls off the map," at which point crisis prediction becomes impossible
    and crisis occurrence becomes near-certain.
    """
    return CausalPathway(
        pathway_id="pw_fragmentation_disengagement",
        name="System fragmentation → assessment fatigue → disengagement → crisis",
        nodes=[
            "9 independent systems each require separate intake assessments",
            "4+ redundant assessments administered in 90-day period",
            "Each assessment worker lacks access to prior assessment results",
            "Robert Jackson experiences repeated trauma-narrative re-telling",
            "Assessment fatigue: stops attending appointments (2 CMHC misses confirmed)",
            "Reduced system contact → reduced medication oversight → adherence decline",
            "ACT team contact gap (9 days, target: every 2-3 days)",
            "Clinical deterioration undetected until next ER visit",
        ],
        intervention_point="4+ redundant assessments administered in 90-day period",
        time_to_crisis_days=21.0,
        probability_if_no_action=0.58,
        probability_if_intervene=0.22,
        intervention_type=InterventionType.CARE_COORDINATION_CALL,
        evidence_quality="observational",
    )


def _build_pathway_benefit_denial() -> CausalPathway:
    """
    Pathway: Benefit disruption → financial crisis → food insecurity → health decline.

    SSDI provides Robert Jackson with ~$943/month. In months when the payment
    is delayed or disrupted, a domino sequence begins: within 48h of expected
    payment not arriving, he is unable to purchase food, cannot afford phone
    minutes (cutting off outreach contact), and is more likely to engage in
    high-risk coping behaviors. The signal is probabilistic: SSDI is reliable,
    but Robert is currently 25 days post-payment with estimated funds depleted.
    """
    return CausalPathway(
        pathway_id="pw_benefit_financial_crisis",
        name="Benefit exhaustion → financial crisis → food insecurity → health decline",
        nodes=[
            "SSDI payment cycle: 25 days elapsed, funds likely depleted",
            "Food insecurity: unable to purchase adequate nutrition",
            "Medication cost-sharing: may skip fills to save money",
            "Phone minutes exhausted: reduced reachability for outreach",
            "Social isolation increases: less contact with support systems",
            "Nutritional deficiency exacerbates psychiatric symptoms",
            "Health decline → ER visit for combined psychiatric + medical presentation",
        ],
        intervention_point="SSDI payment cycle: 25 days elapsed, funds likely depleted",
        time_to_crisis_days=8.0,
        probability_if_no_action=0.31,
        probability_if_intervene=0.12,
        intervention_type=InterventionType.CASE_MANAGEMENT_VISIT,
        evidence_quality="expert_consensus",
    )


# ---------------------------------------------------------------------------
# Feature engineering helpers
# ---------------------------------------------------------------------------

def _compute_er_probability(signals: dict, horizon_years: float) -> tuple[float, float, list[CausalSignal]]:
    """
    Compute ER visit probability for a given time horizon using multiplicative
    Bayesian risk factors applied to the baseline Poisson rate.

    Model: P(≥1 ER visit in horizon) = 1 - exp(-λ * horizon)
    where λ is the base rate modulated by active risk signals.

    The multiplicative model is appropriate here because the risk factors are
    largely independent of each other mechanistically (medication gap operates
    through dopamine pathways; hypothermia operates through thermoregulation;
    mental status changes operate through behavioral pathways). Independence
    breaks down for pathways that share upstream causes, but the conservative
    direction is to model them as independent multiplicative (overestimates risk,
    better for safety-critical predictions).
    """
    base_lambda = _ANNUAL_ER_VISITS_BASE  # Poisson rate: 47 visits/year
    multiplier = 1.0
    active_signals: list[CausalSignal] = []

    # Signal 1: Antipsychotic medication gap
    gap_days = signals.get("antipsychotic_gap_days", 0)
    if gap_days >= _ANTIPSYCHOTIC_GAP_CRITICAL_DAYS:
        m = 3.8
        active_signals.append(CausalSignal(
            name="Antipsychotic gap ≥14 days (critical)",
            description=f"{gap_days}-day gap in antipsychotic medication. Active psychosis "
                        f"probability >80%. ER visit nearly certain within 7 days.",
            strength=SignalStrength.STRONG,
            direction="increases_risk",
            magnitude=m,
            data_source="pharmacy_claims / pdmp",
            confidence=0.92,
        ))
        multiplier *= m
    elif gap_days >= _ANTIPSYCHOTIC_GAP_CRISIS_DAYS:
        m = 2.1
        active_signals.append(CausalSignal(
            name=f"Antipsychotic gap {gap_days} days (warning)",
            description=f"{gap_days}-day gap approaching critical threshold. Early positive "
                        f"symptom emergence likely. Medication reconciliation urgently needed.",
            strength=SignalStrength.STRONG,
            direction="increases_risk",
            magnitude=m,
            data_source="pharmacy_claims / pdmp",
            confidence=0.88,
        ))
        multiplier *= m
    elif signals.get("antipsychotic_mpr", 1.0) < _MPR_ADHERENT:
        mpr = signals["antipsychotic_mpr"]
        m = 1.0 + (1.0 - mpr) * 1.8  # Partial non-adherence: proportional risk increase
        active_signals.append(CausalSignal(
            name=f"Antipsychotic MPR {mpr:.2f} (sub-therapeutic)",
            description=f"Medication Possession Ratio {mpr:.2f} — below 0.80 adherence threshold. "
                        f"Intermittent dosing produces unpredictable symptom breakthrough.",
            strength=SignalStrength.MODERATE,
            direction="increases_risk",
            magnitude=m,
            data_source="pharmacy_claims",
            confidence=0.79,
        ))
        multiplier *= m

    # Signal 2: Temperature / hypothermia risk
    temp_f = signals.get("ambient_temp_f", 70.0)
    unsheltered_nights = signals.get("unsheltered_consecutive_nights", 0)
    if temp_f < _HYPOTHERMIA_CRITICAL_TEMP and unsheltered_nights >= 1:
        m = 4.2
        active_signals.append(CausalSignal(
            name=f"Critical hypothermia conditions ({temp_f}°F, {unsheltered_nights} unsheltered nights)",
            description=f"Ambient temp {temp_f}°F with {unsheltered_nights} consecutive unsheltered "
                        f"nights. Antipsychotic medication impairs thermoregulation (2.5–4× multiplier). "
                        f"Life-threatening hypothermia within 4-6 hours of outdoor exposure.",
            strength=SignalStrength.STRONG,
            direction="increases_risk",
            magnitude=m,
            data_source="weather_api / hmis_shelter",
            confidence=0.91,
        ))
        multiplier *= m
    elif temp_f < _HYPOTHERMIA_RISK_TEMP and unsheltered_nights >= 1:
        m = 2.3
        active_signals.append(CausalSignal(
            name=f"Hypothermia risk ({temp_f}°F, unsheltered)",
            description=f"Temp {temp_f}°F below 40°F threshold with unsheltered exposure. "
                        f"Antipsychotic-impaired thermoregulation elevates clinical risk.",
            strength=SignalStrength.STRONG,
            direction="increases_risk",
            magnitude=m,
            data_source="weather_api / hmis_shelter",
            confidence=0.86,
        ))
        multiplier *= m

    # Signal 3: ER visit acceleration
    er_acceleration = signals.get("er_visit_acceleration", 1.0)
    if er_acceleration > 1.2:
        m = 1.6
        active_signals.append(CausalSignal(
            name=f"ER utilization accelerating ({er_acceleration:.2f}× prior period)",
            description=f"ER visit rate is {er_acceleration:.0%} of prior 90-day rate. "
                        f"Acceleration signal: crisis spiral underway. Each ER visit that "
                        f"ends in discharge-to-street increases probability of the next visit.",
            strength=SignalStrength.MODERATE,
            direction="increases_risk",
            magnitude=m,
            data_source="hmis / ed_claims",
            confidence=0.74,
        ))
        multiplier *= m

    # Signal 4: HRV depression (physiological stress marker)
    hrv = signals.get("hrv_rmssd_current", 40.0)
    hrv_avg = signals.get("hrv_rmssd_7d_avg", 40.0)
    if hrv < 20.0 and hrv < hrv_avg * 0.85:
        m = 1.4
        active_signals.append(CausalSignal(
            name=f"HRV critically suppressed (RMSSD {hrv:.1f}ms, ↓{(1-hrv/hrv_avg)*100:.0f}% vs 7d avg)",
            description=f"Heart rate variability RMSSD {hrv:.1f}ms (7-day avg: {hrv_avg:.1f}ms). "
                        f"HRV below 20ms indicates high allostatic load, poor vagal tone, and "
                        f"impaired stress recovery — validated physiological precursor to behavioral crisis.",
            strength=SignalStrength.MODERATE,
            direction="increases_risk",
            magnitude=m,
            data_source="wearable / apple_watch",
            confidence=0.66,
        ))
        multiplier *= m

    # Signal 5: Sleep deprivation
    sleep_hrs = signals.get("sleep_hours_7d_avg", 7.0)
    if sleep_hrs < 5.0:
        m = 1.35
        active_signals.append(CausalSignal(
            name=f"Severe sleep deprivation ({sleep_hrs:.1f}h avg/night)",
            description=f"Average {sleep_hrs:.1f}h/night over 7 days. Chronic sleep deprivation "
                        f"<5h/night directly worsens positive and negative symptoms in schizoaffective "
                        f"disorder. Sleep loss also impairs medication self-management.",
            strength=SignalStrength.MODERATE,
            direction="increases_risk",
            magnitude=m,
            data_source="wearable",
            confidence=0.71,
        ))
        multiplier *= m

    # Signal 6: ACT team contact gap
    act_gap = signals.get("act_team_days_since_contact", 0)
    if act_gap > 7:
        m = 1.55
        active_signals.append(CausalSignal(
            name=f"ACT team contact gap ({act_gap} days; target ≤3)",
            description=f"{act_gap} days without ACT team contact. Target frequency is every 2-3 days "
                        f"for high-acuity members. Gap allows clinical deterioration to go undetected "
                        f"and breaks the medication management chain.",
            strength=SignalStrength.STRONG,
            direction="increases_risk",
            magnitude=m,
            data_source="cmhc_act_records",
            confidence=0.83,
        ))
        multiplier *= m
    elif act_gap > 4:
        m = 1.25
        active_signals.append(CausalSignal(
            name=f"ACT team contact delayed ({act_gap} days)",
            description=f"{act_gap} days since last ACT team contact. Approaching threshold for "
                        f"undetected deterioration.",
            strength=SignalStrength.WEAK,
            direction="increases_risk",
            magnitude=m,
            data_source="cmhc_act_records",
            confidence=0.67,
        ))
        multiplier *= m

    # Signal 7: PHQ-9 trajectory
    phq9 = signals.get("phq9_latest", 10)
    phq9_prior = signals.get("phq9_prior", 10)
    phq9_delta = phq9 - phq9_prior
    if phq9 >= _PHQ9_MOD_SEVERE and phq9_delta > 3:
        m = 1.3
        active_signals.append(CausalSignal(
            name=f"PHQ-9 worsening trend ({phq9_prior} → {phq9}, +{phq9_delta} pts in 6 weeks)",
            description=f"PHQ-9 rose from {phq9_prior} (moderate) to {phq9} (moderately severe) "
                        f"over 42 days. Worsening depression in schizoaffective disorder predicts "
                        f"behavioral dysregulation and reduced medication self-management.",
            strength=SignalStrength.MODERATE,
            direction="increases_risk",
            magnitude=m,
            data_source="cmhc_assessment",
            confidence=0.69,
        ))
        multiplier *= m

    # Signal 8: Pre-benefit-payment vulnerability window
    days_since_ssdi = signals.get("days_since_ssdi_payment", 0)
    if 20 <= days_since_ssdi <= 30:
        m = 1.18
        active_signals.append(CausalSignal(
            name=f"Pre-payment vulnerability window (day {days_since_ssdi} of SSDI cycle)",
            description=f"SSDI payment arrives monthly. At day {days_since_ssdi}, funds are typically "
                        f"depleted. Food insecurity, medication cost-sharing stress, and social isolation "
                        f"increase in this window. Modest but consistent risk elevation.",
            strength=SignalStrength.WEAK,
            direction="increases_risk",
            magnitude=m,
            data_source="ssa_ssdi_records",
            confidence=0.54,
        ))
        multiplier *= m

    # Compute final probability using Poisson survival function
    effective_lambda = base_lambda * multiplier
    prob = 1.0 - math.exp(-effective_lambda * horizon_years)
    prob = min(0.99, max(0.01, prob))

    # Confidence interval via bootstrap approximation (± 15% of signal uncertainty)
    signal_uncertainty = 1.0 - (sum(s.confidence for s in active_signals) /
                                 max(1, len(active_signals))) if active_signals else 0.2
    ci_width = prob * signal_uncertainty * 0.4
    ci_lower = max(0.01, prob - ci_width)
    ci_upper = min(0.99, prob + ci_width)

    return prob, multiplier, active_signals, ci_lower, ci_upper


# ---------------------------------------------------------------------------
# Main prediction engine
# ---------------------------------------------------------------------------

class CrisisPredictionEngine:
    """
    The computational core of DOMES v2 crisis prediction.

    This engine consumes observations from across all 9 government systems
    and produces probability estimates for each crisis type at each time horizon,
    together with causal explanations and prioritized intervention recommendations.

    Architecture
    ------------
    The engine is a Bayesian risk modulator, not a trained ML classifier. This
    is intentional: at the thought-experiment scale of 3×10²¹ FLOPS directed
    at one person, the model would eventually converge on a near-deterministic
    causal graph of that person's behavior. We model that endpoint — the fully
    converged state — rather than the intermediate statistical approximation.

    The engine is structured in three layers:
    1. Feature engineering: raw observations → risk signals
    2. Causal inference: signals → causal pathways → probabilities
    3. Intervention scoring: probabilities → cost-weighted action recommendations

    Compute budget tracking runs as a side-channel on every prediction call,
    recording the FLOP cost of each inference and accumulating toward the 5-year
    budget. At full scale, the marginal information gain per FLOP decreases as
    entropy about this specific person approaches zero.
    """

    # FLOP cost estimates for different computational operations
    _FLOPS_SIGNAL_EXTRACTION = 2.4e15    # Per signal (attention over time-series)
    _FLOPS_PATHWAY_INFERENCE = 8.1e15    # Per causal pathway activated
    _FLOPS_PROBABILITY_INTEGRATION = 1.2e15  # Per probability computation
    _FLOPS_INTERVENTION_SCORING = 3.6e15    # Per intervention option scored

    def __init__(self):
        self._compute_state: dict[uuid.UUID, ComputeBudgetState] = {}

    def _get_compute_state(self, person_id: uuid.UUID) -> ComputeBudgetState:
        if person_id not in self._compute_state:
            self._compute_state[person_id] = ComputeBudgetState(person_id=person_id)
        return self._compute_state[person_id]

    def _charge_flops(
        self,
        person_id: uuid.UUID,
        flops: float,
        observations_added: int = 0,
    ) -> None:
        """Record FLOP consumption and update uncertainty metrics."""
        state = self._get_compute_state(person_id)
        state.flops_consumed += flops
        state.flops_consumed_today += flops
        state.models_run += 1
        state.observations_integrated += observations_added
        # Model uncertainty reduction: logarithmic in observations
        if state.observations_integrated > 0:
            bits_reduced = 12.4 * math.log1p(state.observations_integrated / 100.0)
            state.current_entropy_bits = max(
                1.0,
                state.initial_entropy_bits - bits_reduced
            )
        state._recalculate()

    async def predict_er_visit(
        self,
        person_id: uuid.UUID,
        signals: dict[str, Any] | None = None,
        as_of: datetime | None = None,
    ) -> list[RiskPrediction]:
        """
        Predict probability of ≥1 ER visit across four time horizons: 24h, 72h, 7d, 30d.

        ER visits are the primary symptom of system failure for Robert Jackson. Each visit
        costs ~$3,200 and ends with discharge back to the street. The prediction model
        uses a non-homogeneous Poisson process: the arrival rate λ is not constant but
        varies with the active risk signal multiplier, which in turn varies with medication
        adherence, weather, and clinical state.

        Clinical reasoning: An ER visit in this population is almost never random. It follows
        a predictable cascade — medication gap → symptom breakthrough → behavioral crisis →
        call to 911 → transport to ED. The cascade has a characteristic duration of 3-7 days
        from gap initiation to ER arrival. This is why 72h and 7d predictions are the most
        clinically actionable horizons.
        """
        as_of = as_of or datetime.now(timezone.utc)
        signals = signals or _robert_jackson_signals(as_of)

        horizons = [
            (CrisisHorizon.H24, _HOURS_24),
            (CrisisHorizon.H72, _DAYS_3),
            (CrisisHorizon.D7, _DAYS_7),
            (CrisisHorizon.D30, _DAYS_30),
        ]

        predictions = []
        for horizon_enum, horizon_years in horizons:
            prob, multiplier, active_signals, ci_low, ci_high = _compute_er_probability(
                signals, horizon_years
            )
            baseline = 1.0 - math.exp(-_ANNUAL_ER_VISITS_BASE * horizon_years)

            flops = (
                len(active_signals) * self._FLOPS_SIGNAL_EXTRACTION
                + self._FLOPS_PROBABILITY_INTEGRATION
            )
            self._charge_flops(person_id, flops, observations_added=len(signals))

            pathway = _build_pathway_antipsychotic_gap() if any(
                "gap" in s.name.lower() for s in active_signals
            ) else _build_pathway_hypothermia()

            pred = RiskPrediction(
                person_id=person_id,
                crisis_type=CrisisType.ER_VISIT,
                horizon=horizon_enum,
                probability=prob,
                probability_ci_lower=ci_low,
                probability_ci_upper=ci_high,
                baseline_probability=baseline,
                risk_multiplier=multiplier,
                risk_level="",  # set by __post_init__
                primary_signals=active_signals,
                active_pathway=pathway,
                flops_consumed=flops,
                narrative=(
                    f"Robert Jackson has a {prob:.0%} probability of ≥1 ER visit in the next "
                    f"{horizon_enum.value}. This is {multiplier:.1f}× above the baseline rate driven "
                    f"primarily by a {signals.get('antipsychotic_gap_days', 0)}-day antipsychotic "
                    f"medication gap, {signals.get('unsheltered_consecutive_nights', 0)} unsheltered "
                    f"nights at {signals.get('ambient_temp_f', 70):.0f}°F, and a {signals.get('act_team_days_since_contact', 0)}-day "
                    f"ACT team contact gap."
                ),
            )
            predictions.append(pred)

        return predictions

    async def predict_psychiatric_crisis(
        self,
        person_id: uuid.UUID,
        signals: dict[str, Any] | None = None,
        as_of: datetime | None = None,
    ) -> list[RiskPrediction]:
        """
        Predict probability of psychiatric crisis in the next 24h and 72h.

        A psychiatric crisis is defined as a behavioral health emergency requiring
        mobile crisis response, law enforcement, or ED psychiatric evaluation.
        This is distinct from an ER visit (which may be for a medical complaint).

        The 24h and 72h horizons are chosen because antipsychotic medication gaps
        produce psychotic relapse on a 48-96h timescale — making these the clinically
        actionable windows where mobile crisis team outreach can intercept the pathway.

        Key signal: C-SSRS active ideation (score ≥2) combined with antipsychotic gap
        and sleep deprivation creates the highest-risk triadic state. All three are
        currently present for Robert Jackson.
        """
        as_of = as_of or datetime.now(timezone.utc)
        signals = signals or _robert_jackson_signals(as_of)

        horizons = [(CrisisHorizon.H24, _HOURS_24), (CrisisHorizon.H72, _DAYS_3)]
        base_annual_rate = _ANNUAL_PSYCH_CRISIS_BASE

        predictions = []
        for horizon_enum, horizon_years in horizons:
            # Build psychiatric-specific multiplier
            multiplier = 1.0
            active_signals = []

            # CSSRS active ideation
            cssrs = signals.get("cssrs_intensity_latest", 0)
            if cssrs >= _CSSRS_ACTIVE_IDEATION:
                m = 2.8
                active_signals.append(CausalSignal(
                    name=f"C-SSRS active ideation (intensity {cssrs})",
                    description=f"Columbia Suicide Severity Rating Scale intensity score {cssrs} "
                                f"(≥2 = active ideation). Combined with medication gap and sleep "
                                f"deprivation, this triadic state predicts psychiatric crisis with "
                                f"high sensitivity in this population.",
                    strength=SignalStrength.STRONG,
                    direction="increases_risk",
                    magnitude=m,
                    data_source="cmhc_assessment",
                    confidence=0.88,
                ))
                multiplier *= m

            # PANSS positive subscale
            panss = signals.get("panss_positive_latest", 20)
            if panss >= _PANSS_POSITIVE_HIGH:
                m = 2.2
                active_signals.append(CausalSignal(
                    name=f"PANSS positive subscale {panss} (severe)",
                    description=f"PANSS positive symptoms score {panss} (≥28 = severe). "
                                f"Command hallucinations at this severity level frequently precipitate "
                                f"public behavioral crises requiring emergency response.",
                    strength=SignalStrength.STRONG,
                    direction="increases_risk",
                    magnitude=m,
                    data_source="cmhc_assessment",
                    confidence=0.81,
                ))
                multiplier *= m

            # Antipsychotic gap
            gap = signals.get("antipsychotic_gap_days", 0)
            if gap >= 4:
                m = 1.9
                active_signals.append(CausalSignal(
                    name=f"Antipsychotic gap {gap} days",
                    description=f"Ongoing antipsychotic gap increases psychiatric crisis risk "
                                f"independently of current symptom severity.",
                    strength=SignalStrength.STRONG,
                    direction="increases_risk",
                    magnitude=m,
                    data_source="pharmacy_claims",
                    confidence=0.89,
                ))
                multiplier *= m

            # Sleep deprivation as psychosis catalyst
            sleep = signals.get("sleep_hours_last_night", 7.0)
            if sleep < 4.0:
                m = 1.45
                active_signals.append(CausalSignal(
                    name=f"Severe sleep deprivation last night ({sleep:.1f}h)",
                    description=f"Only {sleep:.1f}h of sleep. Acute sleep deprivation in "
                                f"schizoaffective disorder can precipitate rapid psychotic "
                                f"decompensation within 24-48h.",
                    strength=SignalStrength.MODERATE,
                    direction="increases_risk",
                    magnitude=m,
                    data_source="wearable",
                    confidence=0.72,
                ))
                multiplier *= m

            prob = 1.0 - math.exp(-base_annual_rate * multiplier * horizon_years)
            prob = min(0.97, max(0.01, prob))
            baseline = 1.0 - math.exp(-base_annual_rate * horizon_years)

            flops = len(active_signals) * self._FLOPS_SIGNAL_EXTRACTION + self._FLOPS_PROBABILITY_INTEGRATION
            self._charge_flops(person_id, flops)

            ci_width = prob * 0.15
            predictions.append(RiskPrediction(
                person_id=person_id,
                crisis_type=CrisisType.PSYCHIATRIC_CRISIS,
                horizon=horizon_enum,
                probability=prob,
                probability_ci_lower=max(0.01, prob - ci_width),
                probability_ci_upper=min(0.99, prob + ci_width),
                baseline_probability=baseline,
                risk_multiplier=multiplier,
                risk_level="",
                primary_signals=active_signals,
                active_pathway=_build_pathway_antipsychotic_gap(),
                flops_consumed=flops,
                narrative=(
                    f"Psychiatric crisis probability in {horizon_enum.value}: {prob:.0%}. "
                    f"Active C-SSRS ideation (score {cssrs}), PANSS positive symptoms {panss}, "
                    f"and {gap}-day antipsychotic gap form a high-risk triad. "
                    f"Mobile crisis team outreach within the next 12 hours is the critical intervention."
                ),
            ))

        return predictions

    async def predict_hospitalization(
        self,
        person_id: uuid.UUID,
        signals: dict[str, Any] | None = None,
        as_of: datetime | None = None,
    ) -> list[RiskPrediction]:
        """
        Predict psychiatric and medical hospitalization in the next 7d and 30d.

        Hospitalization is the downstream consequence of an ER visit that cannot
        be resolved at the ED level. For Robert Jackson, psychiatric hospitalizations
        are the primary driver — approximately 1 in 5 ER visits results in inpatient
        psychiatric admission. Medical hospitalizations are less frequent but more
        expensive ($22,800 avg vs. $18,500 for psychiatric).

        The LACE score (Length of stay, Acuity of admission, Comorbidities, ER
        visits in prior 6 months) predicts 30-day readmission. Robert Jackson's
        LACE equivalent would be 12-14 out of 19 — in the highest-risk decile.
        """
        as_of = as_of or datetime.now(timezone.utc)
        signals = signals or _robert_jackson_signals(as_of)

        er_preds = await self.predict_er_visit(person_id, signals, as_of)
        er_30d_prob = next((p.probability for p in er_preds if p.horizon == CrisisHorizon.D30), 0.8)

        # P(hospitalization | ER visit) for this population
        p_psych_hosp_given_er = 0.22
        p_med_hosp_given_er = 0.11

        predictions = []
        for horizon_enum, horizon_years in [(CrisisHorizon.D7, _DAYS_7), (CrisisHorizon.D30, _DAYS_30)]:
            er_prob_horizon, mult, sigs, ci_lo, ci_hi = _compute_er_probability(signals, horizon_years)

            psych_prob = min(0.95, er_prob_horizon * p_psych_hosp_given_er * 1.0)
            med_prob = min(0.90, er_prob_horizon * p_med_hosp_given_er * 1.0)

            flops = self._FLOPS_PROBABILITY_INTEGRATION * 2
            self._charge_flops(person_id, flops)

            predictions.append(RiskPrediction(
                person_id=person_id,
                crisis_type=CrisisType.HOSPITALIZATION_PSYCHIATRIC,
                horizon=horizon_enum,
                probability=psych_prob,
                probability_ci_lower=max(0.01, psych_prob * 0.7),
                probability_ci_upper=min(0.99, psych_prob * 1.3),
                baseline_probability=er_prob_horizon * 0.20,
                risk_multiplier=mult,
                risk_level="",
                primary_signals=sigs[:2],
                flops_consumed=flops,
                narrative=(
                    f"Psychiatric hospitalization probability in {horizon_enum.value}: {psych_prob:.0%}. "
                    f"Driven by {er_prob_horizon:.0%} ER visit probability × 22% psychiatric admission rate. "
                    f"Inpatient psychiatric care costs $18,500 avg; prevention via medication reconciliation "
                    f"and ACT team contact costs approximately $400 combined."
                ),
            ))

            predictions.append(RiskPrediction(
                person_id=person_id,
                crisis_type=CrisisType.HOSPITALIZATION_MEDICAL,
                horizon=horizon_enum,
                probability=med_prob,
                probability_ci_lower=max(0.01, med_prob * 0.6),
                probability_ci_upper=min(0.99, med_prob * 1.4),
                baseline_probability=er_prob_horizon * 0.10,
                risk_multiplier=mult,
                risk_level="",
                primary_signals=sigs[:1],
                flops_consumed=flops,
                narrative=(
                    f"Medical hospitalization probability in {horizon_enum.value}: {med_prob:.0%}. "
                    f"Primary pathway: hypothermia → ED admission. Warming center referral "
                    f"($25/night) prevents $22,800 expected medical hospitalization cost."
                ),
            ))

        return predictions

    async def predict_incarceration(
        self,
        person_id: uuid.UUID,
        signals: dict[str, Any] | None = None,
        as_of: datetime | None = None,
    ) -> list[RiskPrediction]:
        """
        Predict incarceration risk in the next 30d and 90d.

        Incarceration is a common downstream consequence of psychiatric crisis for
        people without housing. When a behavioral health crisis occurs in a public space
        and the response is a law enforcement contact rather than a mobile crisis team,
        the outcome is frequently a misdemeanor charge (disorderly conduct, trespassing,
        failure to appear) rather than a mental health diversion.

        Robert Jackson is currently on active probation. A probation check-in is due
        in 3 days. If he is in psychiatric decompensation at the time of the check-in,
        or if he misses it due to crisis, revocation is a significant risk.

        The criminalization of mental illness is not an inevitable outcome — it is
        the specific result of a system design that routes crises to law enforcement
        first and mental health services second. This prediction models that design
        flaw as a quantifiable risk.
        """
        as_of = as_of or datetime.now(timezone.utc)
        signals = signals or _robert_jackson_signals(as_of)

        predictions = []
        for horizon_enum, horizon_years in [
            (CrisisHorizon.D30, _DAYS_30),
            (CrisisHorizon.D90, _DAYS_90),
        ]:
            multiplier = 1.0
            active_signals = []

            # Probation check-in proximity
            prob_checkin_days = signals.get("probation_next_checkin_days", 30)
            if prob_checkin_days <= 5 and horizon_years <= _DAYS_30:
                m = 2.1
                active_signals.append(CausalSignal(
                    name=f"Probation check-in in {prob_checkin_days} days (missed = revocation risk)",
                    description=f"Active probation check-in in {prob_checkin_days} days. If Robert "
                                f"Jackson is in psychiatric decompensation or misses appointment due "
                                f"to crisis, probation revocation → incarceration is automatic.",
                    strength=SignalStrength.STRONG,
                    direction="increases_risk",
                    magnitude=m,
                    data_source="probation_records",
                    confidence=0.84,
                ))
                multiplier *= m

            # Psychiatric crisis increases criminalization risk
            psych_crisis_preds = await self.predict_psychiatric_crisis(person_id, signals, as_of)
            psych_72h = next((p.probability for p in psych_crisis_preds if p.horizon == CrisisHorizon.H72), 0.3)
            if psych_72h > 0.4:
                m = 1.7
                active_signals.append(CausalSignal(
                    name=f"High psychiatric crisis probability ({psych_72h:.0%} in 72h)",
                    description=f"Elevated psychiatric crisis probability ({psych_72h:.0%}) in an environment "
                                f"where law enforcement is the primary first responder to public behavioral "
                                f"health emergencies. Behavioral crisis → 911 call → arrest pathway.",
                    strength=SignalStrength.MODERATE,
                    direction="increases_risk",
                    magnitude=m,
                    data_source="prediction_engine_cross_reference",
                    confidence=0.71,
                ))
                multiplier *= m

            base_prob = 1.0 - math.exp(-_ANNUAL_INCARCERATION_BASE * multiplier * horizon_years)
            base_prob = min(0.90, max(0.01, base_prob))
            baseline = 1.0 - math.exp(-_ANNUAL_INCARCERATION_BASE * horizon_years)

            flops = len(active_signals) * self._FLOPS_SIGNAL_EXTRACTION + self._FLOPS_PROBABILITY_INTEGRATION
            self._charge_flops(person_id, flops)

            predictions.append(RiskPrediction(
                person_id=person_id,
                crisis_type=CrisisType.INCARCERATION,
                horizon=horizon_enum,
                probability=base_prob,
                probability_ci_lower=max(0.01, base_prob * 0.65),
                probability_ci_upper=min(0.90, base_prob * 1.35),
                baseline_probability=baseline,
                risk_multiplier=multiplier,
                risk_level="",
                primary_signals=active_signals,
                flops_consumed=flops,
                narrative=(
                    f"Incarceration probability in {horizon_enum.value}: {base_prob:.0%}. "
                    f"Primary driver: probation check-in in {prob_checkin_days} days combined with "
                    f"active psychiatric decompensation. Mobile crisis diversion (not 911 dispatch) "
                    f"would break the criminalization pathway."
                ),
            ))

        return predictions

    async def predict_mortality(
        self,
        person_id: uuid.UUID,
        signals: dict[str, Any] | None = None,
        as_of: datetime | None = None,
    ) -> list[RiskPrediction]:
        """
        Predict mortality risk at 30d, 90d, and 365d horizons.

        Premature mortality in chronically homeless adults with severe mental illness
        occurs at 3-5× the age-standardized population rate. For Robert Jackson (45yo),
        the annual mortality probability without intervention is approximately 4.2%.
        Over a 5-year DOMES monitoring period, cumulative mortality risk without
        meaningful intervention is approximately 19%.

        Primary mortality pathways for this population:
        1. Hypothermia (acutely weather-dependent; highest signal in winter)
        2. Drug/alcohol-related causes (overdose, aspiration, organ failure)
        3. Cardiovascular disease (accelerated by antipsychotic-associated metabolic syndrome)
        4. Violence (victimization risk for unsheltered individuals)
        5. Suicide (active C-SSRS ideation present; 10× population suicide rate for this diagnosis)

        The 30-day mortality signal is dominated by the hypothermia pathway given current
        conditions (24°F, unsheltered, impaired thermoregulation from antipsychotics).
        """
        as_of = as_of or datetime.now(timezone.utc)
        signals = signals or _robert_jackson_signals(as_of)

        predictions = []
        for horizon_enum, horizon_years in [
            (CrisisHorizon.D30, _DAYS_30),
            (CrisisHorizon.D90, _DAYS_90),
            (CrisisHorizon.D365, _DAYS_365),
        ]:
            multiplier = 1.0
            active_signals = []

            # Hypothermia mortality pathway
            temp_f = signals.get("ambient_temp_f", 70.0)
            unsheltered = signals.get("unsheltered_consecutive_nights", 0)
            if temp_f < _HYPOTHERMIA_CRITICAL_TEMP and unsheltered >= 1:
                m = 6.5  # Antipsychotic-impaired thermoregulation + sub-freezing temp
                active_signals.append(CausalSignal(
                    name=f"Hypothermia mortality risk ({temp_f}°F, {unsheltered} unsheltered nights)",
                    description=f"Sub-freezing temperature ({temp_f}°F) with {unsheltered} consecutive "
                                f"unsheltered nights. Antipsychotic medications impair thermoregulatory "
                                f"response. Severe hypothermia mortality risk: 1 in 6 cases.",
                    strength=SignalStrength.STRONG,
                    direction="increases_risk",
                    magnitude=m,
                    data_source="weather_api / hmis_shelter",
                    confidence=0.88,
                ))
                multiplier *= m

            # Suicide risk
            cssrs = signals.get("cssrs_intensity_latest", 0)
            if cssrs >= _CSSRS_ACTIVE_IDEATION:
                m = 3.2
                active_signals.append(CausalSignal(
                    name=f"Active suicidal ideation (C-SSRS intensity {cssrs})",
                    description=f"Active suicidal ideation present. Schizoaffective disorder carries "
                                f"a lifetime suicide rate of 5-10%. Combined with current social isolation, "
                                f"medication non-adherence, and sub-freezing exposure, this represents "
                                f"an acute suicide risk signal.",
                    strength=SignalStrength.STRONG,
                    direction="increases_risk",
                    magnitude=m,
                    data_source="cmhc_assessment",
                    confidence=0.85,
                ))
                multiplier *= m

            base_prob = 1.0 - math.exp(-_ANNUAL_MORTALITY_RATE * multiplier * horizon_years)
            base_prob = min(0.85, max(0.001, base_prob))
            baseline = 1.0 - math.exp(-_ANNUAL_MORTALITY_RATE * horizon_years)

            flops = len(active_signals) * self._FLOPS_SIGNAL_EXTRACTION + self._FLOPS_PATHWAY_INFERENCE
            self._charge_flops(person_id, flops)

            predictions.append(RiskPrediction(
                person_id=person_id,
                crisis_type=CrisisType.MORTALITY,
                horizon=horizon_enum,
                probability=base_prob,
                probability_ci_lower=max(0.001, base_prob * 0.5),
                probability_ci_upper=min(0.85, base_prob * 2.0),
                baseline_probability=baseline,
                risk_multiplier=multiplier,
                risk_level="",
                primary_signals=active_signals,
                active_pathway=_build_pathway_hypothermia(),
                flops_consumed=flops,
                narrative=(
                    f"Mortality probability in {horizon_enum.value}: {base_prob:.1%}. "
                    f"Dominant pathway: hypothermia at {temp_f:.0f}°F with antipsychotic-impaired "
                    f"thermoregulation. Secondary pathway: suicide risk (C-SSRS score {cssrs}). "
                    f"A $25 warming center referral tonight is the single highest-ROI intervention "
                    f"in the entire DOMES signal space."
                ),
            ))

        return predictions

    async def predict_housing_loss(
        self,
        person_id: uuid.UUID,
        signals: dict[str, Any] | None = None,
        as_of: datetime | None = None,
    ) -> list[RiskPrediction]:
        """
        Predict probability of losing temporary shelter placement in the next 30 days.

        Robert Jackson's shelter enrollment is currently "active but inconsistent" —
        he has only used shelter 11 of the past 30 nights (37%). Emergency shelters
        typically have a 3-strike policy for missed consecutive nights. The shelter
        program warning flag is active, meaning the program may discharge him for
        non-compliance.

        Loss of shelter placement removes the most basic buffer against hypothermia
        mortality. It also removes the shelter address that anchors his Medicaid
        eligibility, SSDI continuation, and probation compliance. Housing loss
        is therefore a force multiplier for every other risk in this model.
        """
        as_of = as_of or datetime.now(timezone.utc)
        signals = signals or _robert_jackson_signals(as_of)

        multiplier = 1.0
        active_signals = []

        shelter_warning = signals.get("shelter_program_warning", False)
        if shelter_warning:
            m = 2.8
            active_signals.append(CausalSignal(
                name="Active shelter program warning flag",
                description="Emergency shelter has issued a warning for inconsistent occupancy. "
                            "Robert Jackson used only 11 of 30 available shelter nights (37%). "
                            "Program may discharge for policy non-compliance.",
                strength=SignalStrength.STRONG,
                direction="increases_risk",
                magnitude=m,
                data_source="hmis_shelter",
                confidence=0.91,
            ))
            multiplier *= m

        shelter_nights_30d = signals.get("shelter_nights_last_30d", 30)
        if shelter_nights_30d < 15:
            utilization = shelter_nights_30d / 30.0
            m = 1.0 + (1.0 - utilization) * 1.5
            active_signals.append(CausalSignal(
                name=f"Low shelter utilization ({shelter_nights_30d}/30 nights, {utilization:.0%})",
                description=f"Only {shelter_nights_30d} shelter nights in past 30 days ({utilization:.0%}). "
                            f"Psychiatric decompensation frequently leads to shelter avoidance — "
                            f"crowded environments exacerbate paranoia and aggression.",
                strength=SignalStrength.MODERATE,
                direction="increases_risk",
                magnitude=m,
                data_source="hmis_shelter",
                confidence=0.78,
            ))
            multiplier *= m

        prob = 1.0 - math.exp(-_ANNUAL_HOUSING_LOSS_BASE * multiplier * _DAYS_30)
        prob = min(0.95, max(0.01, prob))
        baseline = 1.0 - math.exp(-_ANNUAL_HOUSING_LOSS_BASE * _DAYS_30)

        flops = len(active_signals) * self._FLOPS_SIGNAL_EXTRACTION + self._FLOPS_PROBABILITY_INTEGRATION
        self._charge_flops(person_id, flops)

        return [RiskPrediction(
            person_id=person_id,
            crisis_type=CrisisType.HOUSING_LOSS,
            horizon=CrisisHorizon.D30,
            probability=prob,
            probability_ci_lower=max(0.01, prob * 0.7),
            probability_ci_upper=min(0.95, prob * 1.3),
            baseline_probability=baseline,
            risk_multiplier=multiplier,
            risk_level="",
            primary_signals=active_signals,
            active_pathway=_build_pathway_assessment_fatigue(),
            flops_consumed=flops,
            narrative=(
                f"Housing loss probability in 30 days: {prob:.0%}. "
                f"Active shelter program warning with 37% utilization rate. "
                f"If shelter discharges Robert Jackson, this removes the address anchor "
                f"for Medicaid eligibility, SSDI continuation, and probation compliance — "
                f"a cascade that increases every other risk in this model by 2-4×."
            ),
        )]

    async def score_interventions(
        self,
        prediction: RiskPrediction,
    ) -> InterventionScore:
        """
        Compute the top 3 interventions for a predicted crisis, ranked by ROI.

        Intervention scoring uses a simplified cost-effectiveness model:
        ROI = cost_of_inaction / cost_of_intervention
        where cost_of_inaction = P(crisis) × expected_cost_of_that_crisis.

        The number-needed-to-treat (NNT) equivalent is:
        NNT = 1 / absolute_probability_reduction_per_intervention_attempt

        A lower NNT means fewer people need to receive the intervention for one
        crisis to be prevented. For well-targeted interventions like medication
        reconciliation in confirmed non-adherent patients, NNT ≈ 2–4.

        The action window is the time remaining before the intervention loses its
        effect. For hypothermia prevention, the window is the number of hours until
        the person is exposed to sub-freezing temperatures tonight. For medication
        reconciliation, the window is the time remaining before the gap reaches
        critical threshold (14 days).
        """
        flops = self._FLOPS_INTERVENTION_SCORING * 3
        self._charge_flops(prediction.person_id, flops)

        crisis_costs = {
            CrisisType.ER_VISIT: _COST_ER_VISIT,
            CrisisType.PSYCHIATRIC_CRISIS: _COST_PSYCH_HOSPITALIZATION * 0.5,
            CrisisType.HOSPITALIZATION_PSYCHIATRIC: _COST_PSYCH_HOSPITALIZATION,
            CrisisType.HOSPITALIZATION_MEDICAL: _COST_MEDICAL_HOSPITALIZATION,
            CrisisType.INCARCERATION: _COST_INCARCERATION_30D,
            CrisisType.MORTALITY: 450_000.0,  # Actuarial value of statistical life (VSL, USDOT)
            CrisisType.HOUSING_LOSS: 8_500.0,  # Cost of re-entry + cascading benefit disruption
        }

        base_cost = crisis_costs.get(prediction.crisis_type, 5000.0)
        cost_of_inaction = prediction.probability * base_cost

        # Intervention library — calibrated for Robert Jackson specifically
        interventions_by_type: dict[CrisisType, list[InterventionOption]] = {
            CrisisType.ER_VISIT: [
                InterventionOption(
                    intervention_type=InterventionType.MEDICATION_RECONCILIATION,
                    description="Emergency medication reconciliation: ACT team delivers 7-day antipsychotic "
                                "supply and watches first dose. Bridges gap until next pharmacy fill.",
                    responsible_system="ACT Team / CMHC",
                    responsible_role="ACT team psychiatrist or APRN",
                    estimated_cost=_COST_MEDICATION_RECONCILIATION,
                    cost_of_inaction=cost_of_inaction,
                    roi_ratio=cost_of_inaction / _COST_MEDICATION_RECONCILIATION,
                    probability_reduction=0.53,
                    nnt=1.9,
                    action_window_hours=36.0,
                    urgency="urgent",
                    specific_actions=[
                        "Locate Robert Jackson (last known location: shelter + usual encampment)",
                        "Confirm antipsychotic gap via PDMP query (5 minutes)",
                        "Deliver bridge supply (7-day risperidone or equivalent)",
                        "Observed first dose administration",
                        "Schedule pharmacy pickup within 24h",
                        "Document in CMHC + HMIS within 2 hours",
                    ],
                    contraindications=[
                        "Do not administer if patient is in acute medical distress — call 911 instead",
                        "Check for alcohol or benzodiazepine co-ingestion before dosing",
                    ],
                ),
                InterventionOption(
                    intervention_type=InterventionType.WARMING_CENTER_REFERRAL,
                    description="Transport to warming center for overnight shelter (tonight, 24°F ambient). "
                                "Eliminates hypothermia pathway and ER visit risk from thermal exposure.",
                    responsible_system="HMIS / Emergency Shelter Network",
                    responsible_role="Street outreach worker",
                    estimated_cost=_COST_WARMING_CENTER,
                    cost_of_inaction=cost_of_inaction,
                    roi_ratio=cost_of_inaction / _COST_WARMING_CENTER,
                    probability_reduction=0.38,
                    nnt=2.6,
                    action_window_hours=6.0,
                    urgency="immediate",
                    specific_actions=[
                        "Check warming center availability (call 211 or direct HMIS lookup)",
                        "Locate Robert Jackson before 9 PM (temperature drops after midnight)",
                        "Transport or escort to warming center",
                        "Confirm intake at warming center — document bed assignment",
                        "Flag for morning outreach follow-up",
                    ],
                ),
                InterventionOption(
                    intervention_type=InterventionType.ACT_TEAM_CONTACT,
                    description="Urgent ACT team contact to assess current psychiatric status, address "
                                "medication gap, and link to same-day services. Resets contact-gap signal.",
                    responsible_system="CMHC / ACT Team",
                    responsible_role="ACT team case manager or nurse",
                    estimated_cost=_COST_ACT_TEAM_VISIT,
                    cost_of_inaction=cost_of_inaction,
                    roi_ratio=cost_of_inaction / _COST_ACT_TEAM_VISIT,
                    probability_reduction=0.27,
                    nnt=3.7,
                    action_window_hours=24.0,
                    urgency="urgent",
                    specific_actions=[
                        "Call Robert Jackson's known phone number (3 attempts over 2 hours)",
                        "If no answer: street outreach to last known location",
                        "Conduct brief MSE (mental status examination)",
                        "Address medication gap if present",
                        "Connect to warming center if not already sheltered",
                        "Update CMHC + ACT records",
                    ],
                ),
            ],
        }

        top_interventions = interventions_by_type.get(
            prediction.crisis_type,
            interventions_by_type[CrisisType.ER_VISIT]  # default fallback
        )

        recommended = min(top_interventions, key=lambda x: x.nnt) if top_interventions else None

        return InterventionScore(
            for_prediction=prediction.crisis_type,
            horizon=prediction.horizon,
            cost_of_inaction=cost_of_inaction,
            top_interventions=top_interventions,
            recommended_intervention=recommended,
            composite_action_window_hours=min(
                (i.action_window_hours for i in top_interventions), default=24.0
            ),
        )

    async def predict_all(
        self,
        person_id: uuid.UUID,
        person_name: str = "Robert Jackson",
        as_of: datetime | None = None,
    ) -> RiskDashboard:
        """
        Generate the complete risk dashboard for one person.

        This is the primary entry point for the DOMES prediction engine. It runs
        all prediction models in sequence, scores interventions for the highest-risk
        predictions, and assembles the complete RiskDashboard.

        At 3×10²¹ FLOPS over 5 years, this method would run continuously — every
        ~53 milliseconds — producing a fresh prediction as each new observation
        arrives from any of the 9 government systems. The dashboard returned here
        represents a single snapshot of that continuous inference stream.

        The compute budget tracker records total FLOPs consumed for this call,
        updates the marginal information gain estimate, and projects how much
        uncertainty remains about this person's future crises.
        """
        as_of = as_of or datetime.now(timezone.utc)
        signals = _robert_jackson_signals(as_of)

        # Run all prediction models
        er_preds = await self.predict_er_visit(person_id, signals, as_of)
        psych_preds = await self.predict_psychiatric_crisis(person_id, signals, as_of)
        hosp_preds = await self.predict_hospitalization(person_id, signals, as_of)
        incarceration_preds = await self.predict_incarceration(person_id, signals, as_of)
        mortality_preds = await self.predict_mortality(person_id, signals, as_of)
        housing_preds = await self.predict_housing_loss(person_id, signals, as_of)

        all_preds: dict[str, list[RiskPrediction]] = {
            CrisisType.ER_VISIT.value: er_preds,
            CrisisType.PSYCHIATRIC_CRISIS.value: psych_preds,
            CrisisType.HOSPITALIZATION_PSYCHIATRIC.value: [
                p for p in hosp_preds if p.crisis_type == CrisisType.HOSPITALIZATION_PSYCHIATRIC
            ],
            CrisisType.HOSPITALIZATION_MEDICAL.value: [
                p for p in hosp_preds if p.crisis_type == CrisisType.HOSPITALIZATION_MEDICAL
            ],
            CrisisType.INCARCERATION.value: incarceration_preds,
            CrisisType.MORTALITY.value: mortality_preds,
            CrisisType.HOUSING_LOSS.value: housing_preds,
        }

        # Find highest priority prediction
        all_flat = [p for plist in all_preds.values() for p in plist]
        highest = max(all_flat, key=lambda p: p.probability * (
            # Weight by crisis severity: mortality > hospitalization > ER > others
            5.0 if p.crisis_type == CrisisType.MORTALITY else
            4.0 if p.crisis_type in (CrisisType.HOSPITALIZATION_PSYCHIATRIC, CrisisType.HOSPITALIZATION_MEDICAL) else
            3.0 if p.crisis_type == CrisisType.PSYCHIATRIC_CRISIS else
            2.0 if p.crisis_type == CrisisType.ER_VISIT else
            1.0
        )) if all_flat else None

        # Score interventions for top 3 most critical predictions
        critical_preds = sorted(all_flat, key=lambda p: p.probability, reverse=True)[:3]
        intervention_scores = []
        for pred in critical_preds:
            score = await self.score_interventions(pred)
            intervention_scores.append(score)

        # Compute 30-day cost of inaction
        er_30d = next((p for p in er_preds if p.horizon == CrisisHorizon.D30), None)
        hosp_psych_30d = next(
            (p for p in hosp_preds
             if p.crisis_type == CrisisType.HOSPITALIZATION_PSYCHIATRIC and p.horizon == CrisisHorizon.D30),
            None
        )
        total_coi_30d = (
            (er_30d.probability * _COST_ER_VISIT if er_30d else 0) +
            (hosp_psych_30d.probability * _COST_PSYCH_HOSPITALIZATION if hosp_psych_30d else 0)
        )

        intervention_cost_total = sum(
            score.recommended_intervention.estimated_cost
            for score in intervention_scores
            if score.recommended_intervention
        )

        # Active pathways
        active_pathways = [
            _build_pathway_antipsychotic_gap(),
            _build_pathway_hypothermia(),
            _build_pathway_assessment_fatigue(),
            _build_pathway_benefit_denial(),
        ]

        # Compute state
        compute_state = self._get_compute_state(person_id)

        # Determine immediate action
        mortality_24h = next(
            (p for p in mortality_preds if p.horizon == CrisisHorizon.D30), None
        )
        immediate_action = (mortality_24h and mortality_24h.probability > 0.05) or (
            signals.get("ambient_temp_f", 70) < _HYPOTHERMIA_RISK_TEMP
            and signals.get("unsheltered_consecutive_nights", 0) >= 1
        )

        projected_annual_savings = (
            _ANNUAL_ER_VISITS_BASE * _COST_ER_VISIT * 0.60  # 60% reduction with full DOMES
            + _ANNUAL_PSYCH_CRISIS_BASE * _COST_PSYCH_HOSPITALIZATION * 0.50
        )

        dashboard = RiskDashboard(
            person_id=person_id,
            person_name=person_name,
            generated_at=as_of,
            as_of_date=as_of.date(),
            predictions=all_preds,
            intervention_scores=intervention_scores,
            highest_priority_crisis=highest.crisis_type if highest else None,
            highest_priority_horizon=highest.horizon if highest else None,
            highest_priority_probability=highest.probability if highest else 0.0,
            immediate_action_required=immediate_action,
            recommended_immediate_action=(
                f"WARMING CENTER REFERRAL TONIGHT — {signals['ambient_temp_f']:.0f}°F ambient, "
                f"{signals['unsheltered_consecutive_nights']} consecutive unsheltered nights, "
                f"antipsychotic thermoregulation impairment. Window closes at sundown."
                if immediate_action else "No immediate crisis action required — routine monitoring."
            ),
            compute_state=compute_state,
            active_pathways=active_pathways,
            total_cost_of_inaction_30d=total_coi_30d,
            total_cost_of_recommended_interventions=intervention_cost_total,
            projected_annual_savings=projected_annual_savings,
            executive_summary=(
                f"DOMES Crisis Dashboard — {person_name} — {as_of.strftime('%Y-%m-%d %H:%M UTC')}\n\n"
                f"IMMEDIATE RISK: {'YES — See recommended action' if immediate_action else 'No acute crisis'}\n"
                f"Highest priority: {highest.crisis_type.value if highest else 'None'} "
                f"({highest.probability:.0%} probability in {highest.horizon.value if highest else 'N/A'})\n\n"
                f"ACTIVE CAUSAL PATHWAYS:\n"
                f"  1. Antipsychotic gap (4 days) → psychotic relapse → ER visit [5.3 days to crisis]\n"
                f"  2. {signals['ambient_temp_f']:.0f}°F + unsheltered → hypothermia → ER/death [1.5 days]\n"
                f"  3. Assessment fatigue (4 redundant assessments) → disengagement → crisis [21 days]\n"
                f"  4. Benefit exhaustion (day 25 of SSDI cycle) → food insecurity → decline [8 days]\n\n"
                f"COST ANALYSIS (30-day window):\n"
                f"  Cost of inaction: ${total_coi_30d:,.0f}\n"
                f"  Cost of recommended interventions: ${intervention_cost_total:,.0f}\n"
                f"  ROI of acting now: {total_coi_30d / max(1, intervention_cost_total):.0f}×\n"
                f"  Projected annual savings with full DOMES: ${projected_annual_savings:,.0f}\n\n"
                f"COMPUTE BUDGET: {compute_state.flops_consumed:.2e} FLOPs consumed | "
                f"Current entropy: {compute_state.current_entropy_bits:.1f} bits | "
                f"Uncertainty reduction: {compute_state.initial_entropy_bits - compute_state.current_entropy_bits:.1f} bits\n\n"
                f"This dashboard was generated by DOMES v2, a thought experiment modeling the outcome "
                f"of directing 3×10²¹ FLOPS over 5 years at understanding one chronically homeless human "
                f"being. The $112,100 annual fragmented cost of Robert Jackson's current situation is not "
                f"an accident. It is the predictable output of 9 independent systems that were never "
                f"designed to talk to each other. DOMES is what happens when they do."
            ),
        )

        return dashboard
