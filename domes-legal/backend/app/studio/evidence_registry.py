"""Evidence Registry -- RCT-to-Fiscal Endpoint Mapping.

Translates randomised controlled trial (RCT) clinical endpoints into
fiscal/utilisation endpoints that payers, actuaries, and budget analysts
can use.  This is the bridge between "PHQ-9 dropped by 4 points" and
"ER visits for behavioural health decreased by 18 %, saving $2,340/PMPY".

Key concepts:
    EvidenceEntry
        A single row of clinical evidence with its fiscal translation,
        external-validity score, and cost function.
    OutcomeMapping
        The structural link from a clinical endpoint to a utilisation
        endpoint and then to a payer cost function.
    External validity scoring
        Compares study-population demographics to a specific person's
        context to discount or amplify the applicability of evidence.

All computations use only the standard library (math, statistics).
"""
from __future__ import annotations

import math
from typing import Optional
from uuid import uuid4

from pydantic import BaseModel, Field


# ═══════════════════════════════════════════════════════════════════
# Models
# ═══════════════════════════════════════════════════════════════════

class EvidenceEntry(BaseModel):
    """A single piece of clinical evidence with its fiscal translation."""
    entry_id: str = Field(default_factory=lambda: str(uuid4()))
    source: str                                # e.g. "NEJM 2023; 389:1234"
    population_descriptor: dict = Field(default_factory=dict)
    # demographics, conditions, setting captured as key-value pairs
    endpoint_clinical: str                     # e.g. "PHQ-9"
    endpoint_fiscal: str                       # e.g. "ER_visits"
    effect_size: float                         # standardised or raw
    confidence_interval: tuple[float, float]   # (lower, upper)
    external_validity_score: float = 0.5       # 0-1
    unit_cost_function: str = ""               # e.g. "ER_visit * 1450"


class OutcomeMapping(BaseModel):
    """Structural link: clinical endpoint -> utilisation -> cost function."""
    clinical_endpoint: str
    utilization_endpoint: str
    payer_cost_function: str


# ═══════════════════════════════════════════════════════════════════
# Default outcome mappings
# ═══════════════════════════════════════════════════════════════════

DEFAULT_OUTCOME_MAPPINGS: dict[str, OutcomeMapping] = {
    "A1c": OutcomeMapping(
        clinical_endpoint="A1c",
        utilization_endpoint="diabetes_related_admissions",
        payer_cost_function="admissions * 12500 + rx_fills * 450",
    ),
    "PHQ9": OutcomeMapping(
        clinical_endpoint="PHQ9",
        utilization_endpoint="behavioral_health_ER_visits",
        payer_cost_function="ER_visits * 1450 + crisis_episodes * 3200",
    ),
    "BMI": OutcomeMapping(
        clinical_endpoint="BMI",
        utilization_endpoint="obesity_related_costs",
        payer_cost_function="annual_medical * 0.08 * BMI_change",
    ),
    "SBP": OutcomeMapping(
        clinical_endpoint="SBP",
        utilization_endpoint="cardiovascular_events",
        payer_cost_function="events * 28000 + maintenance_rx * 120",
    ),
    "LDL": OutcomeMapping(
        clinical_endpoint="LDL",
        utilization_endpoint="statin_related_events",
        payer_cost_function="MACE_events * 45000 + rx_fills * 85",
    ),
    "eGFR": OutcomeMapping(
        clinical_endpoint="eGFR",
        utilization_endpoint="renal_progression",
        payer_cost_function="dialysis_months * 7500 + nephrology_visits * 350",
    ),
    "FEV1": OutcomeMapping(
        clinical_endpoint="FEV1",
        utilization_endpoint="respiratory_exacerbations",
        payer_cost_function="exacerbations * 6800 + pulm_rehab_sessions * 250",
    ),
    "pain_VAS": OutcomeMapping(
        clinical_endpoint="pain_VAS",
        utilization_endpoint="opioid_utilization",
        payer_cost_function="opioid_rx * 180 + pain_clinic_visits * 400",
    ),
    "GAD7": OutcomeMapping(
        clinical_endpoint="GAD7",
        utilization_endpoint="anxiety_related_utilization",
        payer_cost_function="psych_visits * 200 + ER_visits * 1450 + rx_fills * 90",
    ),
    "PROMIS_physical": OutcomeMapping(
        clinical_endpoint="PROMIS_physical",
        utilization_endpoint="functional_limitation_costs",
        payer_cost_function="PT_visits * 175 + DME_costs + disability_days * 280",
    ),
    "falls_count": OutcomeMapping(
        clinical_endpoint="falls_count",
        utilization_endpoint="fall_related_costs",
        payer_cost_function="fall_injuries * 35000 + hip_fractures * 42000",
    ),
    "readmission_30d": OutcomeMapping(
        clinical_endpoint="readmission_30d",
        utilization_endpoint="readmission_penalty",
        payer_cost_function="readmissions * 15000 + penalty_adjustment",
    ),
}


# ═══════════════════════════════════════════════════════════════════
# External validity scoring
# ═══════════════════════════════════════════════════════════════════

# Weights for each comparability dimension (sum to 1.0)
_VALIDITY_WEIGHTS: dict[str, float] = {
    "age": 0.20,
    "sex": 0.10,
    "race_ethnicity": 0.10,
    "conditions": 0.25,
    "setting": 0.15,
    "severity": 0.20,
}


def _numeric_similarity(a: float, b: float, tolerance: float) -> float:
    """Score 0-1 for how close two numbers are within a tolerance band."""
    if tolerance <= 0:
        return 1.0 if a == b else 0.0
    distance = abs(a - b)
    return max(0.0, 1.0 - distance / tolerance)


def _set_overlap(set_a: set, set_b: set) -> float:
    """Jaccard similarity between two sets."""
    if not set_a and not set_b:
        return 1.0
    if not set_a or not set_b:
        return 0.0
    intersection = len(set_a & set_b)
    union = len(set_a | set_b)
    return intersection / union if union > 0 else 0.0


def score_external_validity(
    study_population: dict,
    person_context: dict,
) -> float:
    """Score how well a study population matches a person's context.

    Compares demographics (age, sex, race/ethnicity), clinical conditions,
    care setting, and disease severity.  Each dimension is scored 0-1
    and combined via weighted average.

    Args:
        study_population: Dict describing the study cohort, e.g.:
            {
                "mean_age": 55, "age_range": [40, 70],
                "pct_female": 0.52,
                "race_ethnicity": ["white", "black", "hispanic"],
                "conditions": ["diabetes", "hypertension"],
                "setting": "outpatient",
                "severity": "moderate",
            }
        person_context: Dict describing the individual, e.g.:
            {
                "age": 48,
                "sex": "female",
                "race_ethnicity": "hispanic",
                "conditions": ["diabetes", "CKD"],
                "setting": "outpatient",
                "severity": "moderate",
            }

    Returns:
        Float 0-1 representing external validity (higher = better match).
    """
    scores: dict[str, float] = {}

    # ── Age ──
    person_age = person_context.get("age")
    study_mean_age = study_population.get("mean_age")
    age_range = study_population.get("age_range")

    if person_age is not None and study_mean_age is not None:
        tolerance = 20.0  # within 20 years is the scoring window
        if age_range and len(age_range) == 2:
            tolerance = max((age_range[1] - age_range[0]) / 2, 5.0)
        scores["age"] = _numeric_similarity(
            float(person_age), float(study_mean_age), tolerance,
        )
    else:
        scores["age"] = 0.5  # uninformative default

    # ── Sex ──
    person_sex = (person_context.get("sex") or "").lower()
    study_pct_female = study_population.get("pct_female")
    if person_sex and study_pct_female is not None:
        # If the person is female, higher pct_female = better match
        if person_sex in ("female", "f"):
            scores["sex"] = min(study_pct_female * 2, 1.0)
        elif person_sex in ("male", "m"):
            scores["sex"] = min((1.0 - study_pct_female) * 2, 1.0)
        else:
            scores["sex"] = 0.5
    else:
        scores["sex"] = 0.5

    # ── Race / ethnicity ──
    person_re = person_context.get("race_ethnicity")
    study_re = study_population.get("race_ethnicity", [])
    if person_re and study_re:
        person_set = {person_re.lower()} if isinstance(person_re, str) else {
            r.lower() for r in person_re
        }
        study_set = {r.lower() for r in study_re} if isinstance(study_re, list) else {
            study_re.lower(),
        }
        scores["race_ethnicity"] = 1.0 if person_set & study_set else 0.2
    else:
        scores["race_ethnicity"] = 0.5

    # ── Conditions ──
    person_conditions = set(
        c.lower() for c in (person_context.get("conditions") or [])
    )
    study_conditions = set(
        c.lower() for c in (study_population.get("conditions") or [])
    )
    scores["conditions"] = _set_overlap(study_conditions, person_conditions)

    # ── Setting ──
    person_setting = (person_context.get("setting") or "").lower()
    study_setting = (study_population.get("setting") or "").lower()
    if person_setting and study_setting:
        scores["setting"] = 1.0 if person_setting == study_setting else 0.3
    else:
        scores["setting"] = 0.5

    # ── Severity ──
    severity_order = ["mild", "moderate", "severe", "critical"]
    person_severity = (person_context.get("severity") or "").lower()
    study_severity = (study_population.get("severity") or "").lower()
    if person_severity in severity_order and study_severity in severity_order:
        p_idx = severity_order.index(person_severity)
        s_idx = severity_order.index(study_severity)
        max_dist = len(severity_order) - 1
        scores["severity"] = 1.0 - abs(p_idx - s_idx) / max_dist
    else:
        scores["severity"] = 0.5

    # ── Weighted combination ──
    total = 0.0
    for dimension, weight in _VALIDITY_WEIGHTS.items():
        total += scores.get(dimension, 0.5) * weight

    return round(min(max(total, 0.0), 1.0), 4)


# ═══════════════════════════════════════════════════════════════════
# Clinical-to-fiscal translation
# ═══════════════════════════════════════════════════════════════════

# Default per-unit costs for common utilisation categories
_DEFAULT_UNIT_COSTS: dict[str, float] = {
    "ER_visits": 1_450.0,
    "admissions": 12_500.0,
    "diabetes_related_admissions": 12_500.0,
    "behavioral_health_ER_visits": 1_450.0,
    "cardiovascular_events": 28_000.0,
    "MACE_events": 45_000.0,
    "readmissions": 15_000.0,
    "dialysis_months": 7_500.0,
    "exacerbations": 6_800.0,
    "fall_injuries": 35_000.0,
    "hip_fractures": 42_000.0,
    "crisis_episodes": 3_200.0,
    "opioid_rx": 180.0,
    "psych_visits": 200.0,
    "PT_visits": 175.0,
    "rx_fills": 150.0,
}

# Elasticity: how much a 1-SD change in the clinical endpoint shifts
# utilisation (calibrated from meta-analytic evidence)
_CLINICAL_ELASTICITY: dict[str, float] = {
    "A1c": 0.18,            # 1% A1c reduction => ~18% fewer admissions
    "PHQ9": 0.15,           # 5-pt PHQ9 drop => ~15% fewer ER visits
    "BMI": 0.06,            # 1 BMI unit => ~6% cost change
    "SBP": 0.12,            # 10 mmHg SBP drop => ~12% fewer CV events
    "LDL": 0.10,            # per 1 mmol/L => ~10% fewer MACE
    "eGFR": 0.08,           # per 5 mL/min => ~8% renal cost change
    "FEV1": 0.14,           # per 100 mL => ~14% fewer exacerbations
    "pain_VAS": 0.10,       # per 1 cm VAS => ~10% opioid reduction
    "GAD7": 0.12,           # per 4 pts => ~12% utilisation reduction
    "PROMIS_physical": 0.09, # per 5 T-score pts => ~9% cost change
    "falls_count": 0.20,    # per fall averted => ~20% cost reduction
    "readmission_30d": 0.25, # per 1% absolute reduction => cost change
}


def translate_clinical_to_fiscal(
    clinical_endpoint: str,
    effect_size: float,
    person_context: dict,
    baseline_annual_cost: float | None = None,
) -> dict:
    """Translate a clinical effect into a fiscal impact estimate.

    Looks up the clinical endpoint in DEFAULT_OUTCOME_MAPPINGS, applies
    the elasticity and effect size, and estimates cost change.

    Args:
        clinical_endpoint: The clinical endpoint name (e.g. "PHQ9", "A1c").
        effect_size: Observed or expected effect size (in endpoint units
            or standardised).
        person_context: Dict with the person's demographics and conditions,
            used to weight the external validity and look up baseline costs.
        baseline_annual_cost: Optional baseline annual cost. If not
            provided, uses default unit costs for the mapped utilisation
            category.

    Returns:
        Dict with:
            - utilization_endpoint: str
            - utilization_change: float (percent change, e.g. -0.15)
            - cost_change: float (estimated dollar change)
            - cost_function: str (the payer cost formula applied)
            - confidence: float 0-1 (based on effect size magnitude
              and data availability)
            - notes: str
    """
    mapping = DEFAULT_OUTCOME_MAPPINGS.get(clinical_endpoint)
    if mapping is None:
        return {
            "utilization_endpoint": "unknown",
            "utilization_change": 0.0,
            "cost_change": 0.0,
            "cost_function": "",
            "confidence": 0.0,
            "notes": (
                f"No mapping found for clinical endpoint "
                f"'{clinical_endpoint}'. Available endpoints: "
                f"{sorted(DEFAULT_OUTCOME_MAPPINGS.keys())}"
            ),
        }

    # Determine elasticity
    elasticity = _CLINICAL_ELASTICITY.get(clinical_endpoint, 0.10)

    # Utilisation change as a fraction (negative = reduction = savings)
    utilization_change = -effect_size * elasticity

    # Base cost lookup
    if baseline_annual_cost is not None and baseline_annual_cost > 0:
        base_cost = baseline_annual_cost
    else:
        base_cost = _DEFAULT_UNIT_COSTS.get(
            mapping.utilization_endpoint, 5_000.0,
        )

    cost_change = base_cost * utilization_change

    # Confidence: higher effect sizes on well-mapped endpoints get
    # higher confidence; tempered by whether we have person context
    has_conditions = bool(person_context.get("conditions"))
    has_demographics = bool(
        person_context.get("age") and person_context.get("sex")
    )
    context_factor = 0.5 + 0.25 * has_conditions + 0.25 * has_demographics

    effect_factor = min(abs(effect_size) / 1.0, 1.0)  # saturates at 1.0
    confidence = round(context_factor * effect_factor * 0.9, 4)
    confidence = min(confidence, 0.95)

    notes_parts = [
        f"Elasticity for {clinical_endpoint}: {elasticity:.2f}",
        f"Utilization category: {mapping.utilization_endpoint}",
        f"Base cost: ${base_cost:,.0f}",
    ]
    if not has_conditions:
        notes_parts.append(
            "Warning: no conditions in person context; estimate less precise"
        )

    return {
        "utilization_endpoint": mapping.utilization_endpoint,
        "utilization_change": round(utilization_change, 4),
        "cost_change": round(cost_change, 2),
        "cost_function": mapping.payer_cost_function,
        "confidence": confidence,
        "notes": "; ".join(notes_parts),
    }
