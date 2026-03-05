"""Narrative Synthesis -- Automatic Story-Thread Extraction.

Watches the Dome's data flows (assessments, interventions, outcomes,
gaps, appeals, experiments) and distills them into narrative threads
that a Showrunner can use to commission productions.

Key concepts:
    NarrativeThread
        A coherent story arc discovered in a person's data: the tension,
        turning points, stakes, and potential resolution.  Each thread
        has a dramatic-potential score used to prioritize productions.

    ThreadExtractor
        Ingests domain events (financial, health, legal, digital) and
        identifies patterns that map to classic narrative structures:
        - rising tension (cliffs, cascades, denials)
        - turning points (trial results, gap discoveries, appeals won)
        - stakes (dollar amounts, health metrics, housing stability)
        - resolution hooks (bridges, credential pathways, verified outcomes)

    NarrativePackage
        A bundle of threads for a single person, ready for the Showrunner
        to review and optionally commission as a production.

All functions are stdlib-only and operate on Pydantic models.
"""
from __future__ import annotations

import math
import uuid
from datetime import datetime
from typing import Any, Literal, Optional

from pydantic import BaseModel, Field


# ── Models ────────────────────────────────────────────────────────

class NarrativeThread(BaseModel):
    """A single narrative arc discovered in a person's data."""
    thread_id: str = Field(default_factory=lambda: f"thr-{uuid.uuid4().hex[:12]}")
    person_id: str
    title: str
    arc_type: Literal[
        "rising_tension",
        "turning_point",
        "fall_and_recovery",
        "slow_burn",
        "cascade",
        "breakthrough",
    ]
    summary: str
    tension_score: float = Field(
        ge=0.0, le=1.0,
        description="How dramatically charged the thread is (0 = flat, 1 = explosive)",
    )
    stakes: dict[str, Any] = Field(
        default_factory=dict,
        description="What is at risk: {'financial': 12000, 'health': 'A1c 9.2', 'housing': True}",
    )
    events: list[dict[str, Any]] = Field(
        default_factory=list,
        description="Chronological list of events forming this thread",
    )
    turning_points: list[str] = Field(
        default_factory=list,
        description="Key moments where the narrative shifted",
    )
    resolution_hooks: list[str] = Field(
        default_factory=list,
        description="Possible paths to resolution that a production could explore",
    )
    discovered_at: str = Field(
        default_factory=lambda: datetime.utcnow().isoformat()
    )


class NarrativePackage(BaseModel):
    """Bundle of threads for a single person, ready for Showrunner review."""
    package_id: str = Field(default_factory=lambda: f"pkg-{uuid.uuid4().hex[:12]}")
    person_id: str
    threads: list[NarrativeThread] = Field(default_factory=list)
    dramatic_potential: float = Field(
        ge=0.0, le=1.0,
        description="Overall dramatic potential (max tension across threads)",
    )
    recommended_medium: str = ""
    generated_at: str = Field(
        default_factory=lambda: datetime.utcnow().isoformat()
    )


# ── Event type taxonomy ───────────────────────────────────────────

# Events are classified into domains; each has a base tension weight
_DOMAIN_TENSION: dict[str, float] = {
    "financial": 0.7,       # cliff discovered, benefit lost, debt
    "health": 0.8,          # diagnosis, trial result, ER visit
    "legal": 0.6,           # appeal filed, rights request, provision violation
    "housing": 0.9,         # eviction risk, shelter, lease issue
    "employment": 0.5,      # job loss, credential gap, new offer
    "digital": 0.4,         # exposure event, scam, doomscrolling
    "social": 0.3,          # isolation, support network change
}

# Event subtypes that signal turning points
_TURNING_POINT_SIGNALS = {
    "appeal_overturned",
    "trial_decisive_benefit",
    "cliff_bridge_activated",
    "credential_completed",
    "referral_completed",
    "gap_resolved",
    "production_shipped",
    "benefit_restored",
    "housing_secured",
}

# Event subtypes that signal escalation
_ESCALATION_SIGNALS = {
    "cliff_zone_entered",
    "cascade_risk_critical",
    "appeal_denied",
    "trial_stopped_futility",
    "eviction_notice",
    "benefit_cutoff",
    "exposure_critical",
    "readmission",
}


# ── Thread extraction ─────────────────────────────────────────────

def extract_threads(
    person_id: str,
    events: list[dict[str, Any]],
) -> list[NarrativeThread]:
    """Extract narrative threads from a person's event stream.

    Events should be dicts with at minimum:
      - type: str (e.g. "cliff_zone_entered", "trial_decisive_benefit")
      - domain: str (e.g. "financial", "health")
      - timestamp: str (ISO format)
      - details: dict (freeform context)

    The extractor groups events by domain, scores tension within each
    group, identifies turning points and escalations, and produces
    NarrativeThread objects for threads with sufficient dramatic weight.

    Args:
        person_id: The person whose events are being analyzed.
        events: Chronologically ordered list of event dicts.

    Returns:
        List of NarrativeThread objects, sorted by tension_score descending.
    """
    if not events:
        return []

    # Group events by domain
    by_domain: dict[str, list[dict[str, Any]]] = {}
    for evt in events:
        domain = evt.get("domain", "unknown")
        by_domain.setdefault(domain, []).append(evt)

    threads: list[NarrativeThread] = []

    for domain, domain_events in by_domain.items():
        thread = _build_domain_thread(person_id, domain, domain_events)
        if thread and thread.tension_score >= 0.15:
            threads.append(thread)

    # Check for cross-domain cascade threads
    cascade = _detect_cascade_thread(person_id, events, by_domain)
    if cascade:
        threads.append(cascade)

    # Sort by tension descending
    threads.sort(key=lambda t: -t.tension_score)

    return threads


def _build_domain_thread(
    person_id: str,
    domain: str,
    events: list[dict[str, Any]],
) -> NarrativeThread | None:
    """Build a single-domain narrative thread."""
    if not events:
        return None

    base_tension = _DOMAIN_TENSION.get(domain, 0.3)

    # Identify turning points and escalations
    turning_points: list[str] = []
    escalation_count = 0

    for evt in events:
        evt_type = evt.get("type", "")
        if evt_type in _TURNING_POINT_SIGNALS:
            turning_points.append(
                f"{evt_type} at {evt.get('timestamp', 'unknown')}"
            )
        if evt_type in _ESCALATION_SIGNALS:
            escalation_count += 1

    # Calculate tension
    event_density = min(len(events) / 10.0, 1.0)
    escalation_factor = min(escalation_count * 0.15, 0.5)
    turning_factor = min(len(turning_points) * 0.1, 0.3)

    tension = base_tension * 0.4 + event_density * 0.3 + escalation_factor + turning_factor * 0.5
    tension = min(max(tension, 0.0), 1.0)

    # Determine arc type
    arc_type = _classify_arc(events, turning_points, escalation_count)

    # Extract stakes from event details
    stakes = _extract_stakes(events)

    # Resolution hooks
    resolution_hooks = _find_resolution_hooks(events, domain)

    # Generate title and summary
    title = _generate_title(domain, arc_type, len(events))
    summary = _generate_summary(domain, events, turning_points, escalation_count)

    return NarrativeThread(
        person_id=person_id,
        title=title,
        arc_type=arc_type,
        summary=summary,
        tension_score=round(tension, 4),
        stakes=stakes,
        events=events,
        turning_points=turning_points,
        resolution_hooks=resolution_hooks,
    )


def _detect_cascade_thread(
    person_id: str,
    all_events: list[dict[str, Any]],
    by_domain: dict[str, list[dict[str, Any]]],
) -> NarrativeThread | None:
    """Detect cross-domain cascade threads.

    A cascade occurs when events in multiple high-tension domains
    cluster together temporally, suggesting reinforcing crises.
    """
    high_tension_domains = [
        d for d in by_domain
        if _DOMAIN_TENSION.get(d, 0) >= 0.6 and len(by_domain[d]) >= 2
    ]

    if len(high_tension_domains) < 2:
        return None

    # Build cascade thread from all high-tension domain events
    cascade_events = []
    for domain in high_tension_domains:
        cascade_events.extend(by_domain[domain])

    # Sort chronologically
    cascade_events.sort(key=lambda e: e.get("timestamp", ""))

    escalation_count = sum(
        1 for e in cascade_events
        if e.get("type", "") in _ESCALATION_SIGNALS
    )

    tension = min(
        0.5 + len(high_tension_domains) * 0.15 + escalation_count * 0.1,
        1.0,
    )

    domains_str = " + ".join(sorted(high_tension_domains))

    return NarrativeThread(
        person_id=person_id,
        title=f"Cascade: {domains_str}",
        arc_type="cascade",
        summary=(
            f"Cross-domain crisis cascade across {domains_str}. "
            f"{len(cascade_events)} events across {len(high_tension_domains)} domains "
            f"with {escalation_count} escalation signals."
        ),
        tension_score=round(tension, 4),
        stakes=_extract_stakes(cascade_events),
        events=cascade_events,
        turning_points=[],
        resolution_hooks=[
            f"Coordinated cross-domain intervention for {domains_str}",
            "Case conference: identify root-cause domain to break cycle",
        ],
    )


def _classify_arc(
    events: list[dict[str, Any]],
    turning_points: list[str],
    escalation_count: int,
) -> Literal[
    "rising_tension", "turning_point", "fall_and_recovery",
    "slow_burn", "cascade", "breakthrough",
]:
    """Classify the narrative arc type based on event patterns."""
    has_escalation = escalation_count > 0
    has_turning = len(turning_points) > 0

    if has_escalation and has_turning:
        return "fall_and_recovery"
    elif has_escalation and not has_turning:
        return "rising_tension"
    elif has_turning and not has_escalation:
        return "breakthrough"
    elif len(events) >= 8:
        return "slow_burn"
    else:
        return "rising_tension"


def _extract_stakes(events: list[dict[str, Any]]) -> dict[str, Any]:
    """Extract what's at stake from event details."""
    stakes: dict[str, Any] = {}

    for evt in events:
        details = evt.get("details", {})

        # Financial stakes
        for key in ("amount", "savings", "cost", "bridge_amount", "benefit_amount"):
            if key in details:
                current = stakes.get("financial", 0)
                stakes["financial"] = current + float(details[key])

        # Health stakes
        for key in ("metric", "diagnosis", "a1c", "phq9", "bmi"):
            if key in details:
                stakes["health"] = details[key]

        # Housing stakes
        if evt.get("domain") == "housing" or "housing" in str(details):
            stakes["housing"] = True

        # Employment stakes
        if "wage" in details or "job" in str(details):
            stakes["employment"] = True

    return stakes


def _find_resolution_hooks(
    events: list[dict[str, Any]],
    domain: str,
) -> list[str]:
    """Identify possible resolution paths from event data."""
    hooks: list[str] = []

    event_types = {e.get("type", "") for e in events}

    if domain == "financial":
        if "cliff_zone_entered" in event_types:
            hooks.append("Income bridge to navigate benefits cliff")
        hooks.append("Financial counseling and benefits optimization")

    if domain == "health":
        if "trial_decisive_benefit" in event_types:
            hooks.append("Scale successful intervention to full treatment plan")
        hooks.append("Care coordination with evidence-matched providers")

    if domain == "legal":
        if "appeal_overturned" in event_types:
            hooks.append("Document appeal success for systemic change")
        hooks.append("Rights advocacy and policy reform connection")

    if domain == "housing":
        hooks.append("Emergency housing assistance and stabilization")
        hooks.append("Landlord mediation or legal aid referral")

    if domain == "employment":
        hooks.append("Credential pathway to higher-wage employment")
        hooks.append("Job placement with barrier-aware employer")

    if domain == "digital":
        hooks.append("Digital safety intervention and literacy training")
        hooks.append("Platform opt-out and protective technology setup")

    return hooks


def _generate_title(domain: str, arc_type: str, event_count: int) -> str:
    """Generate a narrative title."""
    arc_labels = {
        "rising_tension": "Rising",
        "turning_point": "Turning Point",
        "fall_and_recovery": "Fall & Recovery",
        "slow_burn": "Slow Burn",
        "cascade": "Cascade",
        "breakthrough": "Breakthrough",
    }
    arc_label = arc_labels.get(arc_type, arc_type)
    domain_label = domain.replace("_", " ").title()
    return f"{domain_label}: {arc_label} ({event_count} events)"


def _generate_summary(
    domain: str,
    events: list[dict[str, Any]],
    turning_points: list[str],
    escalation_count: int,
) -> str:
    """Generate a narrative summary."""
    parts = [
        f"{len(events)} events in the {domain} domain.",
    ]
    if escalation_count:
        parts.append(f"{escalation_count} escalation signal(s) detected.")
    if turning_points:
        parts.append(f"{len(turning_points)} turning point(s) identified.")

    return " ".join(parts)


# ── Package assembly ──────────────────────────────────────────────

def assemble_package(
    person_id: str,
    events: list[dict[str, Any]],
) -> NarrativePackage:
    """Assemble a full narrative package for a person.

    Extracts threads, scores overall dramatic potential, and recommends
    the best production medium based on thread characteristics.

    Args:
        person_id: The person whose narrative is being packaged.
        events: Full event stream for the person.

    Returns:
        NarrativePackage ready for Showrunner review.
    """
    threads = extract_threads(person_id, events)

    if not threads:
        return NarrativePackage(
            person_id=person_id,
            threads=[],
            dramatic_potential=0.0,
            recommended_medium="",
        )

    # Dramatic potential: max tension across threads, boosted by thread count
    max_tension = max(t.tension_score for t in threads)
    thread_count_bonus = min(len(threads) * 0.05, 0.2)
    dramatic_potential = min(max_tension + thread_count_bonus, 1.0)

    # Recommend medium based on thread characteristics
    medium = _recommend_medium(threads, dramatic_potential)

    return NarrativePackage(
        person_id=person_id,
        threads=threads,
        dramatic_potential=round(dramatic_potential, 4),
        recommended_medium=medium,
    )


def _recommend_medium(
    threads: list[NarrativeThread],
    dramatic_potential: float,
) -> str:
    """Recommend the best production medium for a narrative package."""
    arc_types = {t.arc_type for t in threads}
    thread_count = len(threads)
    max_events = max(len(t.events) for t in threads) if threads else 0

    # Cascade or multi-thread = series
    if "cascade" in arc_types or thread_count >= 4:
        return "series"

    # High drama with fall-and-recovery = film
    if dramatic_potential >= 0.8 and "fall_and_recovery" in arc_types:
        return "film"

    # Breakthrough = short doc
    if "breakthrough" in arc_types and dramatic_potential >= 0.5:
        return "doc"

    # Slow burn with lots of events = series
    if "slow_burn" in arc_types and max_events >= 10:
        return "series"

    # Single high-tension thread = short
    if thread_count <= 2 and dramatic_potential >= 0.6:
        return "short"

    # Interactive if digital domain is prominent
    digital_threads = [t for t in threads if "digital" in t.title.lower()]
    if digital_threads:
        return "interactive"

    # Default
    if dramatic_potential >= 0.5:
        return "doc"
    return "installation"


# ── Scoring utilities ─────────────────────────────────────────────

def score_production_potential(
    package: NarrativePackage,
    character_consent_tier: str = "tier1_public",
) -> dict[str, Any]:
    """Score a narrative package's potential as a production.

    Factors:
    - dramatic_potential (0.35): raw dramatic charge
    - thread_diversity (0.20): variety of arc types
    - consent_compatibility (0.25): higher consent tiers are harder to produce
    - resolution_hooks (0.20): more hooks = more production options

    Returns:
        Dict with total_score, component_scores, and go/no-go recommendation.
    """
    scores: dict[str, float] = {}

    # Dramatic potential
    scores["dramatic_potential"] = package.dramatic_potential

    # Thread diversity
    if package.threads:
        distinct_arcs = len({t.arc_type for t in package.threads})
        scores["thread_diversity"] = min(distinct_arcs / 4.0, 1.0)
    else:
        scores["thread_diversity"] = 0.0

    # Consent compatibility
    consent_scores = {
        "tier1_public": 1.0,
        "tier2_standard": 0.8,
        "tier3_sensitive": 0.5,
        "tier4_highest": 0.2,
    }
    scores["consent_compatibility"] = consent_scores.get(character_consent_tier, 0.5)

    # Resolution hooks
    total_hooks = sum(len(t.resolution_hooks) for t in package.threads)
    scores["resolution_hooks"] = min(total_hooks / 8.0, 1.0)

    # Weighted total
    weights = {
        "dramatic_potential": 0.35,
        "thread_diversity": 0.20,
        "consent_compatibility": 0.25,
        "resolution_hooks": 0.20,
    }
    total = sum(scores[k] * weights[k] for k in weights)

    # Go/no-go
    if total >= 0.6:
        recommendation = "greenlight"
    elif total >= 0.4:
        recommendation = "develop_further"
    else:
        recommendation = "hold"

    return {
        "total_score": round(total, 4),
        "component_scores": {k: round(v, 4) for k, v in scores.items()},
        "recommendation": recommendation,
        "recommended_medium": package.recommended_medium,
    }
