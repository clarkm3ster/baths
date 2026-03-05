"""Information / Cognitive Security — Predatory Exposure Tracking.

Models the digital-environment dimension of a person's wellbeing:
predatory advertising, algorithmic radicalization, doomscrolling,
phishing, misinformation, and scam contacts.  Computes a cognitive
health score and detects cascade risk where digital exposure amplifies
financial or health distress.

Provides:
- ExposureEvent / CognitiveHealthScore / DigitalEnvironmentReport models
- log_exposure               — record a single exposure event
- calculate_cognitive_health — score from recent events
- generate_environment_report— full 30-day digital environment analysis
- detect_cascade_risk        — cross-domain risk amplification detection
"""
from __future__ import annotations

import uuid
from datetime import datetime, timedelta
from typing import Any, Literal, Optional

from pydantic import BaseModel, Field


# ── Models ────────────────────────────────────────────────────────

class ExposureEvent(BaseModel):
    """A single predatory / harmful digital exposure event."""
    event_id: str = Field(default_factory=lambda: f"exp-{uuid.uuid4().hex[:12]}")
    person_id: str
    exposure_type: Literal[
        "predatory_ad",
        "algorithmic_radicalization",
        "doomscrolling",
        "phishing",
        "misinformation",
        "scam_contact",
    ]
    source_platform: str = ""
    severity: float = Field(
        ge=0.0, le=1.0,
        description="Severity of the exposure, 0 (negligible) to 1 (critical)",
    )
    detected_at: datetime = Field(default_factory=datetime.utcnow)
    context: dict[str, Any] = Field(
        default_factory=dict,
        description="Freeform context: ad_category, content_topic, amount_targeted, etc.",
    )
    intervention_triggered: bool = False


class CognitiveHealthScore(BaseModel):
    """Composite cognitive-health assessment based on exposure history."""
    person_id: str
    score: float = Field(
        ge=0.0, le=1.0,
        description="1.0 = excellent cognitive environment, 0.0 = severe exposure",
    )
    exposure_count_30d: int = 0
    high_severity_count: int = 0
    trend: Literal["improving", "stable", "declining"] = "stable"
    risk_factors: list[str] = Field(default_factory=list)


class DigitalEnvironmentReport(BaseModel):
    """Full digital-environment analysis over a reporting period."""
    person_id: str
    period_days: int = 30
    total_exposures: int = 0
    by_type: dict[str, int] = Field(default_factory=dict)
    cognitive_health: CognitiveHealthScore = Field(
        default_factory=lambda: CognitiveHealthScore(person_id="")
    )
    recommended_interventions: list[str] = Field(default_factory=list)


# ── Constants ─────────────────────────────────────────────────────

# Severity weights by exposure type (base multiplier)
_TYPE_SEVERITY_WEIGHT: dict[str, float] = {
    "predatory_ad":                0.6,
    "algorithmic_radicalization":  0.9,
    "doomscrolling":               0.3,
    "phishing":                    0.8,
    "misinformation":              0.5,
    "scam_contact":                0.9,
}

# High-severity threshold
_HIGH_SEVERITY_THRESHOLD = 0.7

# Exposure count thresholds for scoring
_MODERATE_EXPOSURE_COUNT = 5
_HIGH_EXPOSURE_COUNT = 15
_SEVERE_EXPOSURE_COUNT = 30

# Known cascade pathways
_CASCADE_PATHWAYS: list[dict[str, Any]] = [
    {
        "trigger_types": {"predatory_ad", "scam_contact"},
        "financial_stress_threshold": 0.6,
        "pathway": "predatory_ads -> financial_distress -> medication_nonadherence",
        "risk_boost": 0.3,
    },
    {
        "trigger_types": {"doomscrolling", "algorithmic_radicalization"},
        "financial_stress_threshold": 0.0,  # any stress level
        "pathway": "doomscrolling -> anxiety -> sleep_disruption -> cognitive_decline",
        "risk_boost": 0.2,
    },
    {
        "trigger_types": {"phishing", "scam_contact"},
        "financial_stress_threshold": 0.5,
        "pathway": "scam_contact -> financial_loss -> housing_instability",
        "risk_boost": 0.35,
    },
    {
        "trigger_types": {"misinformation"},
        "financial_stress_threshold": 0.0,
        "pathway": "misinformation -> treatment_refusal -> health_deterioration",
        "risk_boost": 0.25,
    },
]


# ── Core functions ────────────────────────────────────────────────

def log_exposure(
    person_id: str,
    exposure_type: Literal[
        "predatory_ad",
        "algorithmic_radicalization",
        "doomscrolling",
        "phishing",
        "misinformation",
        "scam_contact",
    ],
    source_platform: str,
    severity: float,
    context: dict[str, Any] | None = None,
) -> ExposureEvent:
    """Record a single exposure event.

    Automatically flags whether an intervention should be triggered
    based on severity and exposure type.
    """
    severity = max(0.0, min(1.0, severity))
    type_weight = _TYPE_SEVERITY_WEIGHT.get(exposure_type, 0.5)
    weighted_severity = severity * type_weight

    # Auto-trigger intervention for high weighted severity
    trigger = weighted_severity >= 0.6

    return ExposureEvent(
        person_id=person_id,
        exposure_type=exposure_type,
        source_platform=source_platform,
        severity=severity,
        context=context or {},
        intervention_triggered=trigger,
    )


def calculate_cognitive_health(
    person_id: str,
    events_30d: list[ExposureEvent],
) -> CognitiveHealthScore:
    """Calculate cognitive health score from 30-day exposure events.

    Score formula:
      base = 1.0
      - frequency_penalty: scaled by count relative to thresholds
      - severity_penalty:  mean weighted severity of all events
      - type_diversity_penalty: more distinct harmful types = worse

    Trend is determined by comparing first-half vs second-half severity.
    """
    if not events_30d:
        return CognitiveHealthScore(
            person_id=person_id,
            score=1.0,
            exposure_count_30d=0,
            high_severity_count=0,
            trend="stable",
            risk_factors=[],
        )

    count = len(events_30d)
    high_sev_count = sum(
        1 for e in events_30d if e.severity >= _HIGH_SEVERITY_THRESHOLD
    )

    # Frequency penalty: 0 at 0 events, ramps toward 0.4 at SEVERE count
    freq_penalty = min(count / _SEVERE_EXPOSURE_COUNT, 1.0) * 0.4

    # Severity penalty: mean weighted severity, scaled to max 0.35
    weighted_severities = [
        e.severity * _TYPE_SEVERITY_WEIGHT.get(e.exposure_type, 0.5)
        for e in events_30d
    ]
    mean_weighted_sev = sum(weighted_severities) / count
    severity_penalty = mean_weighted_sev * 0.35

    # Type diversity penalty: more distinct types = more pervasive exposure
    distinct_types = len({e.exposure_type for e in events_30d})
    max_types = len(_TYPE_SEVERITY_WEIGHT)
    diversity_penalty = (distinct_types / max_types) * 0.25

    score = max(1.0 - freq_penalty - severity_penalty - diversity_penalty, 0.0)

    # Trend: compare first half vs second half mean severity
    sorted_events = sorted(events_30d, key=lambda e: e.detected_at)
    mid = len(sorted_events) // 2
    if mid > 0 and len(sorted_events) > 1:
        first_half_sev = sum(e.severity for e in sorted_events[:mid]) / mid
        second_half_sev = sum(
            e.severity for e in sorted_events[mid:]
        ) / len(sorted_events[mid:])

        if second_half_sev > first_half_sev * 1.15:
            trend: Literal["improving", "stable", "declining"] = "declining"
        elif second_half_sev < first_half_sev * 0.85:
            trend = "improving"
        else:
            trend = "stable"
    else:
        trend = "stable"

    # Risk factors
    risk_factors = _identify_risk_factors(events_30d, count, high_sev_count)

    return CognitiveHealthScore(
        person_id=person_id,
        score=round(score, 4),
        exposure_count_30d=count,
        high_severity_count=high_sev_count,
        trend=trend,
        risk_factors=risk_factors,
    )


def _identify_risk_factors(
    events: list[ExposureEvent],
    count: int,
    high_sev_count: int,
) -> list[str]:
    """Identify specific risk factors from exposure patterns."""
    factors: list[str] = []

    if count >= _SEVERE_EXPOSURE_COUNT:
        factors.append("extreme_exposure_frequency")
    elif count >= _HIGH_EXPOSURE_COUNT:
        factors.append("high_exposure_frequency")

    if high_sev_count >= 5:
        factors.append("repeated_high_severity_exposure")

    # Platform concentration
    platforms: dict[str, int] = {}
    for e in events:
        p = e.source_platform.lower() if e.source_platform else "unknown"
        platforms[p] = platforms.get(p, 0) + 1

    for platform, pcount in platforms.items():
        if pcount >= count * 0.6 and count >= 3:
            factors.append(f"platform_concentration:{platform}")

    # Type-specific patterns
    type_counts: dict[str, int] = {}
    for e in events:
        type_counts[e.exposure_type] = type_counts.get(e.exposure_type, 0) + 1

    if type_counts.get("predatory_ad", 0) >= 5:
        factors.append("targeted_predatory_advertising")
    if type_counts.get("algorithmic_radicalization", 0) >= 3:
        factors.append("algorithmic_radicalization_pattern")
    if type_counts.get("scam_contact", 0) >= 3:
        factors.append("repeated_scam_targeting")
    if type_counts.get("phishing", 0) >= 3:
        factors.append("phishing_campaign_target")
    if type_counts.get("doomscrolling", 0) >= 10:
        factors.append("chronic_doomscrolling")

    return factors


# ── Environment report ────────────────────────────────────────────

def generate_environment_report(
    person_id: str,
    events: list[ExposureEvent],
    period_days: int = 30,
) -> DigitalEnvironmentReport:
    """Generate a full digital environment report.

    Filters events to the reporting period, computes cognitive health,
    and produces intervention recommendations.
    """
    # Filter events to period
    cutoff = datetime.utcnow() - timedelta(days=period_days)
    period_events = [e for e in events if e.detected_at >= cutoff]

    # Count by type
    by_type: dict[str, int] = {}
    for e in period_events:
        by_type[e.exposure_type] = by_type.get(e.exposure_type, 0) + 1

    # Cognitive health
    cog_health = calculate_cognitive_health(person_id, period_events)

    # Recommendations
    recommendations = _generate_interventions(period_events, cog_health, by_type)

    return DigitalEnvironmentReport(
        person_id=person_id,
        period_days=period_days,
        total_exposures=len(period_events),
        by_type=by_type,
        cognitive_health=cog_health,
        recommended_interventions=recommendations,
    )


def _generate_interventions(
    events: list[ExposureEvent],
    health: CognitiveHealthScore,
    by_type: dict[str, int],
) -> list[str]:
    """Generate recommended interventions based on exposure patterns."""
    recs: list[str] = []

    # Score-based recommendations
    if health.score < 0.3:
        recs.append(
            "URGENT: Initiate comprehensive digital safety intervention"
        )
    elif health.score < 0.5:
        recs.append(
            "Schedule digital literacy and safety assessment"
        )

    # Type-specific interventions
    if by_type.get("predatory_ad", 0) >= 3:
        recs.append(
            "Install ad-blocking tools and review financial product opt-outs"
        )

    if by_type.get("algorithmic_radicalization", 0) >= 2:
        recs.append(
            "Adjust social media algorithm settings; diversify content sources"
        )

    if by_type.get("doomscrolling", 0) >= 5:
        recs.append(
            "Enable screen-time limits and app usage monitoring"
        )

    if by_type.get("phishing", 0) >= 2:
        recs.append(
            "Provide phishing recognition training and enable email filtering"
        )

    if by_type.get("misinformation", 0) >= 3:
        recs.append(
            "Connect with trusted information sources; media literacy resources"
        )

    if by_type.get("scam_contact", 0) >= 2:
        recs.append(
            "Register with Do Not Call list; enable call screening and scam blocking"
        )

    # Trend-based
    if health.trend == "declining":
        recs.append(
            "Exposure trend is worsening — escalate to case manager for review"
        )

    # Platform-specific
    for rf in health.risk_factors:
        if rf.startswith("platform_concentration:"):
            platform = rf.split(":", 1)[1]
            recs.append(
                f"Reduce engagement with platform '{platform}' or adjust privacy settings"
            )

    return recs


# ── Cascade risk detection ────────────────────────────────────────

def detect_cascade_risk(
    person_id: str,
    events: list[ExposureEvent],
    financial_stress_score: float = 0.0,
) -> dict[str, Any]:
    """Detect cross-domain cascade risk.

    When digital exposure patterns intersect with financial stress,
    they can create reinforcing feedback loops (cascades).  This function
    checks known cascade pathways and returns the highest-risk match.

    Args:
        person_id: The person identifier.
        events: Recent exposure events.
        financial_stress_score: 0 (no stress) to 1 (severe) financial stress.

    Returns:
        Dict with risk_level, cascade_pathway, contributing_exposures,
        financial_stress_factor, and recommended_interventions.
    """
    if not events:
        return {
            "person_id": person_id,
            "risk_level": "low",
            "risk_score": 0.0,
            "cascade_pathway": None,
            "contributing_exposures": 0,
            "financial_stress_factor": financial_stress_score,
            "recommended_interventions": [],
        }

    event_types = {e.exposure_type for e in events}
    type_counts: dict[str, int] = {}
    for e in events:
        type_counts[e.exposure_type] = type_counts.get(e.exposure_type, 0) + 1

    best_match: dict[str, Any] | None = None
    best_score = 0.0

    for pathway in _CASCADE_PATHWAYS:
        trigger_types: set[str] = pathway["trigger_types"]
        overlap = event_types & trigger_types

        if not overlap:
            continue

        # Financial stress must meet pathway threshold
        if financial_stress_score < pathway["financial_stress_threshold"]:
            continue

        # Score: count of matching events * risk_boost * (1 + financial_stress)
        matching_count = sum(type_counts.get(t, 0) for t in overlap)
        risk_boost: float = pathway["risk_boost"]
        cascade_score = (
            matching_count * risk_boost * (1.0 + financial_stress_score)
        )

        if cascade_score > best_score:
            best_score = cascade_score
            best_match = {
                "pathway": pathway["pathway"],
                "matching_count": matching_count,
                "risk_boost": risk_boost,
            }

    # Normalize score to 0-1 range (cap at 1.0)
    risk_score = min(best_score / 10.0, 1.0)

    # Risk level thresholds
    if risk_score >= 0.7:
        risk_level = "critical"
    elif risk_score >= 0.4:
        risk_level = "high"
    elif risk_score >= 0.2:
        risk_level = "moderate"
    else:
        risk_level = "low"

    # Interventions
    interventions: list[str] = []
    if risk_level in ("critical", "high"):
        interventions.append(
            "Immediate case manager review for cross-domain risk"
        )
        interventions.append(
            "Coordinate financial counseling with digital safety measures"
        )
    if risk_level == "critical":
        interventions.append(
            "Activate emergency intervention protocol"
        )
    if best_match and "financial" in best_match.get("pathway", ""):
        interventions.append(
            "Review and freeze exposure to financial product advertisements"
        )
    if best_match and "medication" in best_match.get("pathway", ""):
        interventions.append(
            "Verify medication adherence and pharmacy access"
        )
    if best_match and "housing" in best_match.get("pathway", ""):
        interventions.append(
            "Assess housing stability and connect to prevention services"
        )

    return {
        "person_id": person_id,
        "risk_level": risk_level,
        "risk_score": round(risk_score, 4),
        "cascade_pathway": best_match["pathway"] if best_match else None,
        "contributing_exposures": best_match["matching_count"] if best_match else 0,
        "financial_stress_factor": financial_stress_score,
        "recommended_interventions": interventions,
    }
