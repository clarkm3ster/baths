"""
Bridge Analysis Engine — the intelligence layer of domes-datamap.

Analyzes gaps between government data systems and produces actionable
bridge strategies: what to fix first, what a person can do themselves
via consent, what it costs, and the implementation order.
"""

import re
from typing import Optional

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models import Bridge, Gap, System


# ---------------------------------------------------------------------------
# Helper: Cost Parsing
# ---------------------------------------------------------------------------

_MULTIPLIERS = {
    "K": 1_000,
    "M": 1_000_000,
    "B": 1_000_000_000,
}


def parse_cost(cost_str: str) -> tuple[float, float]:
    """Parse a cost string into (min_dollars, max_dollars).

    Handles formats:
        "$500K"          -> (500000, 500000)
        "$500K-1M"       -> (500000, 1000000)
        "$2-5M"          -> (2000000, 5000000)
        "$200K-500K"     -> (200000, 500000)
        "$1.5M"          -> (1500000, 1500000)
        "Unknown"        -> (0, 0)
        "$0"             -> (0, 0)
    """
    if not cost_str or not isinstance(cost_str, str):
        return (0.0, 0.0)

    cleaned = cost_str.strip().replace(",", "").replace(" ", "")

    # Try range pattern: $NUM[SUFFIX]-NUM[SUFFIX]
    range_pattern = re.compile(
        r"\$?([\d.]+)\s*([KMB])?\s*[-–]\s*\$?([\d.]+)\s*([KMB])?",
        re.IGNORECASE,
    )
    match = range_pattern.search(cleaned)
    if match:
        low_num = float(match.group(1))
        low_suffix = (match.group(2) or "").upper()
        high_num = float(match.group(3))
        high_suffix = (match.group(4) or "").upper()

        # If only the high side has a suffix, the low side inherits it
        # UNLESS the low side already has its own suffix.
        # e.g. "$2-5M" means both are in millions.
        if high_suffix and not low_suffix:
            low_suffix = high_suffix

        low_mult = _MULTIPLIERS.get(low_suffix, 1)
        high_mult = _MULTIPLIERS.get(high_suffix, 1)

        return (low_num * low_mult, high_num * high_mult)

    # Try single value: $NUM[SUFFIX]
    single_pattern = re.compile(r"\$?([\d.]+)\s*([KMB])?", re.IGNORECASE)
    match = single_pattern.search(cleaned)
    if match:
        num = float(match.group(1))
        suffix = (match.group(2) or "").upper()
        mult = _MULTIPLIERS.get(suffix, 1)
        val = num * mult
        return (val, val)

    return (0.0, 0.0)


def format_cost(amount: float) -> str:
    """Format a dollar amount into human-readable string."""
    if amount <= 0:
        return "$0"
    if amount >= 1_000_000_000:
        return f"${amount / 1_000_000_000:.1f}B".rstrip("0").rstrip(".")  + ""
    if amount >= 1_000_000:
        return f"${amount / 1_000_000:.1f}M".rstrip("0").rstrip(".")
    if amount >= 1_000:
        return f"${amount / 1_000:.0f}K"
    return f"${amount:.0f}"


def format_cost_range(min_cost: float, max_cost: float) -> str:
    """Format a min-max cost range into a readable string."""
    if min_cost == 0 and max_cost == 0:
        return "Unknown"
    if min_cost == max_cost:
        return format_cost(min_cost)
    return f"{format_cost(min_cost)}-{format_cost(max_cost)}"


# ---------------------------------------------------------------------------
# Priority Scoring Engine
# ---------------------------------------------------------------------------

def calculate_priority(bridge: Bridge) -> float:
    """Validate and recalculate priority_score from impact and effort scores.

    Priority = impact / effort ratio, scaled to 0-10.
    High impact + low effort = high priority.
    Guards against division by zero — zero effort means max priority.
    """
    impact = max(0.0, min(10.0, bridge.impact_score or 0.0))
    effort = max(0.0, min(10.0, bridge.effort_score or 0.0))

    if effort == 0:
        priority = 10.0
    else:
        # Raw ratio: impact/effort ranges from 0 to infinity.
        # Scale: (impact / effort) capped at 10, but we want nuance.
        # Use: impact * (10 - effort) / 10  — rewards high impact AND low effort
        # Alternative: direct ratio scaled.  impact / effort * (10/10) = impact/effort
        # We use a balanced formula: weighted combination.
        ratio = impact / effort
        # Scale ratio: a 10/1 = 10 (max), 5/5 = 1, 1/10 = 0.1
        # Normalize to 0-10 using: min(10, ratio * 2) gives good spread
        priority = min(10.0, ratio * 2.0)

    return round(priority, 2)


def rank_bridges(bridges: list[Bridge]) -> list[Bridge]:
    """Sort bridges by priority_score descending.

    Tiebreakers:
    1. Consent bridges come first (fastest to implement)
    2. Lower estimated cost comes first
    """
    def sort_key(b: Bridge):
        # Primary: negative priority (descending)
        # Secondary: consent bridges first (0 for consent, 1 for others)
        # Tertiary: lower cost first
        is_consent = 0 if b.bridge_type == "consent" else 1
        min_cost, _ = parse_cost(b.estimated_cost)
        return (-b.priority_score, is_consent, min_cost)

    return sorted(bridges, key=sort_key)


def get_top_bridges(
    db: Session, limit: int = 20, min_priority: float = 0
) -> list[Bridge]:
    """Query top bridges across all gaps, filtered by minimum priority."""
    query = db.query(Bridge)
    if min_priority > 0:
        query = query.filter(Bridge.priority_score >= min_priority)
    bridges = query.all()
    ranked = rank_bridges(bridges)
    return ranked[:limit]


# ---------------------------------------------------------------------------
# Consent Pathway Analysis
# ---------------------------------------------------------------------------

def _gap_applies_to_circumstances(gap: Gap, circumstances: list[str]) -> bool:
    """Check if a gap applies to any of the given circumstances.

    If a gap has no applies_when, it applies to everyone.
    Otherwise, at least one circumstance must overlap.
    """
    gap_applies = gap.applies_when
    if not gap_applies:
        return True
    circumstances_lower = {c.lower().strip() for c in circumstances}
    gap_applies_lower = {a.lower().strip() for a in gap_applies}
    return bool(circumstances_lower & gap_applies_lower)


def get_consent_pathways(
    db: Session, circumstances: Optional[list[str]] = None
) -> list[dict]:
    """Return all consent-closable gaps with their consent bridges.

    If circumstances are provided, filter to gaps that apply to those
    circumstances.
    """
    # Get all consent-closable gaps
    gaps = db.query(Gap).filter(Gap.consent_closable.is_(True)).all()

    if circumstances:
        gaps = [g for g in gaps if _gap_applies_to_circumstances(g, circumstances)]

    pathways = []
    for gap in gaps:
        consent_bridges = [
            b for b in gap.bridges if b.bridge_type == "consent"
        ]
        if not consent_bridges:
            # Gap is consent-closable but no consent bridge defined yet;
            # still include it as a pathway with gap info only.
            consent_bridges = []

        system_a_name = gap.system_a.name if gap.system_a else gap.system_a_id
        system_b_name = gap.system_b.name if gap.system_b else gap.system_b_id

        pathways.append({
            "gap_id": gap.id,
            "system_a_id": gap.system_a_id,
            "system_b_id": gap.system_b_id,
            "system_a_name": system_a_name,
            "system_b_name": system_b_name,
            "consent_mechanism": gap.consent_mechanism,
            "what_data_unlocks": (
                f"Bridges the data gap between {system_a_name} and "
                f"{system_b_name}. {gap.impact}"
            ),
            "impact_description": gap.impact,
            "severity": gap.severity,
            "applies_when": gap.applies_when,
            "bridges": [b.to_dict() for b in rank_bridges(consent_bridges)],
        })

    # Sort by severity (critical first) then by number of bridges available
    severity_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
    pathways.sort(
        key=lambda p: (
            severity_order.get(p["severity"], 99),
            -len(p["bridges"]),
        )
    )
    return pathways


def build_consent_checklist(
    db: Session, circumstances: list[str]
) -> list[dict]:
    """For a person's situation, return an ordered list of consent forms.

    Each entry: what to sign, what it unlocks, and the impact.
    Ordered by impact (highest first).
    """
    pathways = get_consent_pathways(db, circumstances)

    checklist = []
    for pathway in pathways:
        mechanism = pathway["consent_mechanism"]
        if not mechanism:
            mechanism = "Consent form (specific form TBD)"

        # Aggregate impact score from bridges
        bridge_impacts = [b["impact_score"] for b in pathway["bridges"]]
        max_impact = max(bridge_impacts) if bridge_impacts else 5.0

        checklist.append({
            "gap_id": pathway["gap_id"],
            "consent_form": mechanism,
            "systems_connected": (
                f"{pathway['system_a_name']} <-> {pathway['system_b_name']}"
            ),
            "what_it_unlocks": pathway["what_data_unlocks"],
            "impact_score": max_impact,
            "severity": pathway["severity"],
        })

    # Sort by impact_score descending
    checklist.sort(key=lambda c: -c["impact_score"])
    return checklist


# ---------------------------------------------------------------------------
# Cost Aggregation
# ---------------------------------------------------------------------------

def aggregate_bridge_costs(bridges: list[Bridge]) -> dict:
    """Aggregate costs across a list of bridges.

    Returns total min, total max, and formatted string.
    """
    total_min = 0.0
    total_max = 0.0

    for bridge in bridges:
        low, high = parse_cost(bridge.estimated_cost)
        total_min += low
        total_max += high

    return {
        "total_min": total_min,
        "total_max": total_max,
        "formatted_total": format_cost_range(total_min, total_max),
        "bridge_count": len(bridges),
    }


def cost_by_category(
    db: Session, bridge_type: Optional[str] = None
) -> dict:
    """Breakdown of costs by bridge_type.

    If bridge_type is specified, return only that category.
    """
    query = db.query(Bridge)
    if bridge_type:
        query = query.filter(Bridge.bridge_type == bridge_type)

    bridges = query.all()

    categories: dict[str, list[Bridge]] = {}
    for b in bridges:
        categories.setdefault(b.bridge_type, []).append(b)

    result = {}
    grand_min = 0.0
    grand_max = 0.0

    for btype, blist in sorted(categories.items()):
        agg = aggregate_bridge_costs(blist)
        result[btype] = agg
        grand_min += agg["total_min"]
        grand_max += agg["total_max"]

    return {
        "by_type": result,
        "total_min": grand_min,
        "total_max": grand_max,
        "formatted_total": format_cost_range(grand_min, grand_max),
    }


def cost_by_barrier(db: Session) -> dict:
    """Breakdown of bridge costs by the barrier_type of the parent gap."""
    bridges = db.query(Bridge).all()

    barrier_groups: dict[str, list[Bridge]] = {}
    for b in bridges:
        gap = b.gap
        if gap:
            barrier_groups.setdefault(gap.barrier_type, []).append(b)

    result = {}
    grand_min = 0.0
    grand_max = 0.0

    for barrier, blist in sorted(barrier_groups.items()):
        agg = aggregate_bridge_costs(blist)
        result[barrier] = agg
        grand_min += agg["total_min"]
        grand_max += agg["total_max"]

    return {
        "by_barrier": result,
        "total_min": grand_min,
        "total_max": grand_max,
        "formatted_total": format_cost_range(grand_min, grand_max),
    }


# ---------------------------------------------------------------------------
# Implementation Sequencing
# ---------------------------------------------------------------------------

# Phase ordering: consent first, then legal, then technical, then political/funding
_PHASE_ORDER = {
    "consent": 1,
    "legal": 2,
    "technical": 3,
    "political": 4,
    "funding": 4,  # Same phase as political — both need institutional change
}

_PHASE_NAMES = {
    1: "Phase 1: Consent Bridges",
    2: "Phase 2: Legal & Policy Bridges",
    3: "Phase 3: Technical Bridges",
    4: "Phase 4: Political & Funding Bridges",
}

_PHASE_DESCRIPTIONS = {
    1: "Fastest, cheapest, immediate impact. Person signs consent forms.",
    2: "Require inter-agency agreements but no heavy technical development.",
    3: "Require software development, API integration, or infrastructure.",
    4: "Require institutional change, new legislation, or dedicated funding.",
}


def _estimate_phase_timeline(bridges: list[Bridge]) -> str:
    """Estimate the overall timeline for a phase from its bridges."""
    if not bridges:
        return "N/A"

    # Parse timeline strings and find the longest
    # Common formats: "1-3 months", "6-12 months", "1-2 years"
    max_months = 0
    for b in bridges:
        timeline = (b.timeline or "").lower()
        # Try to extract months
        year_match = re.search(r"(\d+)(?:\s*[-–]\s*(\d+))?\s*year", timeline)
        month_match = re.search(r"(\d+)(?:\s*[-–]\s*(\d+))?\s*month", timeline)
        week_match = re.search(r"(\d+)(?:\s*[-–]\s*(\d+))?\s*week", timeline)

        if year_match:
            high = int(year_match.group(2) or year_match.group(1))
            max_months = max(max_months, high * 12)
        elif month_match:
            high = int(month_match.group(2) or month_match.group(1))
            max_months = max(max_months, high)
        elif week_match:
            high = int(week_match.group(2) or week_match.group(1))
            max_months = max(max_months, max(1, high // 4))

    if max_months == 0:
        return "Timeline TBD"
    if max_months <= 1:
        return "~1 month"
    if max_months < 12:
        return f"~{max_months} months"
    years = max_months / 12
    if years == int(years):
        return f"~{int(years)} year{'s' if years > 1 else ''}"
    return f"~{years:.1f} years"


def sequence_bridges(
    selected_bridge_ids: list[int], db: Session
) -> dict:
    """Given bridge IDs, return a phased implementation plan.

    Phase 1: Consent bridges (fastest, cheapest)
    Phase 2: Legal/policy bridges (agreements, no heavy tech)
    Phase 3: Technical bridges (development needed)
    Phase 4: Political/funding bridges (institutional change)

    Within each phase: sorted by priority_score descending.
    """
    bridges = db.query(Bridge).filter(Bridge.id.in_(selected_bridge_ids)).all()

    if not bridges:
        return {
            "phases": [],
            "total_cost": {"total_min": 0, "total_max": 0, "formatted_total": "$0"},
            "total_timeline": "N/A",
            "cumulative_impact": [],
        }

    # Group by phase
    phase_groups: dict[int, list[Bridge]] = {}
    for b in bridges:
        phase_num = _PHASE_ORDER.get(b.bridge_type, 4)
        phase_groups.setdefault(phase_num, []).append(b)

    phases = []
    cumulative_impact = []
    running_impact_total = 0.0
    grand_min = 0.0
    grand_max = 0.0
    max_phase_months = 0

    for phase_num in sorted(phase_groups.keys()):
        phase_bridges = rank_bridges(phase_groups[phase_num])
        phase_cost = aggregate_bridge_costs(phase_bridges)

        # Impact sum for this phase
        phase_impact_sum = sum(b.impact_score for b in phase_bridges)
        running_impact_total += phase_impact_sum

        phase_timeline = _estimate_phase_timeline(phase_bridges)

        phases.append({
            "phase_number": phase_num,
            "phase_name": _PHASE_NAMES.get(phase_num, f"Phase {phase_num}"),
            "phase_description": _PHASE_DESCRIPTIONS.get(phase_num, ""),
            "bridges": [_bridge_with_gap_info(b) for b in phase_bridges],
            "bridge_count": len(phase_bridges),
            "phase_cost": phase_cost,
            "phase_timeline": phase_timeline,
            "phase_impact": round(phase_impact_sum, 2),
        })

        cumulative_impact.append({
            "after_phase": _PHASE_NAMES.get(phase_num, f"Phase {phase_num}"),
            "cumulative_impact_score": round(running_impact_total, 2),
            "bridges_implemented": sum(
                p["bridge_count"] for p in phases
            ),
        })

        grand_min += phase_cost["total_min"]
        grand_max += phase_cost["total_max"]

        # Parse phase timeline to accumulate total
        timeline_str = phase_timeline.lower()
        month_match = re.search(r"([\d.]+)\s*month", timeline_str)
        year_match = re.search(r"([\d.]+)\s*year", timeline_str)
        if year_match:
            max_phase_months += int(float(year_match.group(1)) * 12)
        elif month_match:
            max_phase_months += int(float(month_match.group(1)))

    # Total timeline: phases run sequentially
    if max_phase_months == 0:
        total_timeline = "Timeline TBD"
    elif max_phase_months < 12:
        total_timeline = f"~{max_phase_months} months"
    else:
        years = max_phase_months / 12
        total_timeline = f"~{years:.1f} years"

    return {
        "phases": phases,
        "total_cost": {
            "total_min": grand_min,
            "total_max": grand_max,
            "formatted_total": format_cost_range(grand_min, grand_max),
        },
        "total_timeline": total_timeline,
        "total_bridges": len(bridges),
        "cumulative_impact": cumulative_impact,
    }


# ---------------------------------------------------------------------------
# Person-Specific Bridge Analysis
# ---------------------------------------------------------------------------

def bridges_for_person(
    db: Session, circumstances: list[str]
) -> list[dict]:
    """Given circumstances, find all applicable gaps and their bridges, ranked."""
    # Get all gaps
    all_gaps = db.query(Gap).all()

    # Filter to gaps that apply to this person
    applicable_gaps = [
        g for g in all_gaps
        if _gap_applies_to_circumstances(g, circumstances)
    ]

    # Collect all bridges from applicable gaps
    all_bridges: list[Bridge] = []
    for gap in applicable_gaps:
        all_bridges.extend(gap.bridges)

    # Rank and return with gap info
    ranked = rank_bridges(all_bridges)
    return [_bridge_with_gap_info(b) for b in ranked]


def consent_impact_for_person(
    db: Session, circumstances: list[str]
) -> dict:
    """How many gaps could this person close just by signing consent forms?

    Returns count, percentage, and details.
    """
    all_gaps = db.query(Gap).all()
    applicable_gaps = [
        g for g in all_gaps
        if _gap_applies_to_circumstances(g, circumstances)
    ]

    total_applicable = len(applicable_gaps)
    consent_closable = [g for g in applicable_gaps if g.consent_closable]
    consent_closable_count = len(consent_closable)

    # Percentage of data silos bridgeable by consent
    percentage = (
        round(consent_closable_count / total_applicable * 100, 1)
        if total_applicable > 0
        else 0.0
    )

    # Gather consent bridges for these gaps
    consent_bridges: list[Bridge] = []
    for gap in consent_closable:
        consent_bridges.extend(
            b for b in gap.bridges if b.bridge_type == "consent"
        )

    total_impact = sum(b.impact_score for b in consent_bridges)

    return {
        "total_applicable_gaps": total_applicable,
        "consent_closable_gaps": consent_closable_count,
        "percentage_closable_by_consent": percentage,
        "consent_bridges_available": len(consent_bridges),
        "total_consent_impact": round(total_impact, 2),
        "gaps": [
            {
                "gap_id": g.id,
                "system_a_name": g.system_a.name if g.system_a else g.system_a_id,
                "system_b_name": g.system_b.name if g.system_b else g.system_b_id,
                "consent_mechanism": g.consent_mechanism,
                "severity": g.severity,
            }
            for g in consent_closable
        ],
    }


def quick_wins(
    db: Session, circumstances: Optional[list[str]] = None
) -> list[dict]:
    """Bridges with effort_score <= 3 and impact_score >= 7.

    High impact, low effort. If circumstances provided, filter to
    applicable gaps.
    """
    query = db.query(Bridge).filter(
        Bridge.effort_score <= 3.0,
        Bridge.impact_score >= 7.0,
    )
    bridges = query.all()

    if circumstances:
        bridges = [
            b for b in bridges
            if b.gap and _gap_applies_to_circumstances(b.gap, circumstances)
        ]

    ranked = rank_bridges(bridges)
    return [_bridge_with_gap_info(b) for b in ranked]


# ---------------------------------------------------------------------------
# Internal Helpers
# ---------------------------------------------------------------------------

def _bridge_with_gap_info(bridge: Bridge) -> dict:
    """Serialize a bridge with its parent gap info attached."""
    data = bridge.to_dict()
    gap = bridge.gap
    if gap:
        data["gap"] = {
            "id": gap.id,
            "system_a_id": gap.system_a_id,
            "system_b_id": gap.system_b_id,
            "system_a_name": gap.system_a.name if gap.system_a else gap.system_a_id,
            "system_b_name": gap.system_b.name if gap.system_b else gap.system_b_id,
            "barrier_type": gap.barrier_type,
            "severity": gap.severity,
            "consent_closable": gap.consent_closable,
        }
    return data
