"""
Cost engine for DOMES Profiles.

Calculates the full annual cost of government services around a person,
projects savings from cross-domain coordination, and estimates ROI at
individual and population scale.
"""

from __future__ import annotations

from itertools import combinations
from typing import Any

from .benchmarks import (
    ANNUAL_INFLATION_RATE,
    AVOIDABLE_COSTS,
    AVOIDABLE_EVENT_FREQUENCIES,
    CIRCUMSTANCE_CATEGORY_MAP,
    COORDINATION_INVESTMENT_PER_PERSON,
    COORDINATION_SAVINGS,
    DOMAIN_COLORS,
    DOMAIN_LABELS,
    LIFETIME_HORIZONS,
    SYSTEM_COSTS,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _resolve_category(system_id: str, circumstances: dict[str, Any]) -> str | None:
    """Pick the best cost category for a system given a person's circumstances.

    Walks through every key/value in *circumstances* and checks it against the
    CIRCUMSTANCE_CATEGORY_MAP for the given system. Returns the first match, or
    ``None`` when no special category applies (i.e. use the base_cost).
    """
    mapping = CIRCUMSTANCE_CATEGORY_MAP.get(system_id)
    if not mapping:
        return None

    # Circumstances can be {"disabled": True, "substance_use": True, ...}
    # or {"population": "youth", "care_level": "residential", ...}.
    # We check both keys and string values.
    for key, value in circumstances.items():
        # Check the key itself (e.g. "disabled": True)
        if isinstance(value, bool) and value and key in mapping:
            return mapping[key]
        # Check string values (e.g. "population": "youth")
        if isinstance(value, str) and value.lower() in mapping:
            return mapping[value.lower()]
        # Also check the key name even if value is a string
        if key in mapping:
            return mapping[key]

    return None


def _system_annual_cost(system_id: str, circumstances: dict[str, Any]) -> float:
    """Return the annual per-person cost for one system."""
    system = SYSTEM_COSTS.get(system_id)
    if not system:
        return 0.0

    category = _resolve_category(system_id, circumstances)
    categories = system.get("categories")
    if category and categories and category in categories:
        return float(categories[category])

    return float(system["base_cost"])


def _domains_for_systems(system_ids: list[str]) -> set[str]:
    """Return the set of domains represented by the given system IDs."""
    domains: set[str] = set()
    for sid in system_ids:
        system = SYSTEM_COSTS.get(sid)
        if system:
            domains.add(system["domain"])
    return domains


def _domain_pair_key(d1: str, d2: str) -> str | None:
    """Return the COORDINATION_SAVINGS key for a pair of domains, or None."""
    candidates = [f"{d1}_{d2}", f"{d2}_{d1}"]
    for key in candidates:
        if key in COORDINATION_SAVINGS:
            return key
    return None


def _format_currency(amount: float) -> str:
    """Format a dollar amount as a short, human-readable string."""
    abs_amount = abs(amount)
    sign = "-" if amount < 0 else ""
    if abs_amount >= 1_000_000_000:
        return f"{sign}${abs_amount / 1_000_000_000:.1f}B"
    if abs_amount >= 1_000_000:
        return f"{sign}${abs_amount / 1_000_000:.1f}M"
    if abs_amount >= 1_000:
        return f"{sign}${abs_amount / 1_000:.0f}K"
    return f"{sign}${abs_amount:,.0f}"


def _infer_lifetime_horizon(circumstances: dict[str, Any]) -> int:
    """Determine the projection horizon (years) from circumstances."""
    for key in circumstances:
        lower = key.lower()
        if lower in LIFETIME_HORIZONS:
            return LIFETIME_HORIZONS[lower]
        val = circumstances[key]
        if isinstance(val, str) and val.lower() in LIFETIME_HORIZONS:
            return LIFETIME_HORIZONS[val.lower()]

    # Check for age-based hints
    age = circumstances.get("age")
    if isinstance(age, (int, float)):
        if age < 18:
            return LIFETIME_HORIZONS["youth"]
        if age >= 65:
            return LIFETIME_HORIZONS["elderly"]

    return LIFETIME_HORIZONS["default"]


def _project_cost(annual_cost: float, years: int) -> float:
    """Project total cost over *years* with compound inflation."""
    total = 0.0
    for y in range(years):
        total += annual_cost * ((1 + ANNUAL_INFLATION_RATE) ** y)
    return round(total, 2)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def calculate_domain_costs(
    domain: str,
    systems: list[str],
    circumstances: dict[str, Any],
) -> dict[str, Any]:
    """Calculate costs aggregated for a single domain.

    Parameters
    ----------
    domain:
        Domain identifier (e.g. ``"health"``).
    systems:
        System IDs that belong to this domain for the person.
    circumstances:
        Person-level circumstances dict.

    Returns
    -------
    dict with ``domain``, ``label``, ``color``, ``systems`` detail list,
    ``total_annual_cost``, and ``source_citations``.
    """
    system_details: list[dict[str, Any]] = []
    total = 0.0
    citations: list[str] = []

    for sid in systems:
        spec = SYSTEM_COSTS.get(sid)
        if not spec:
            continue
        cost = _system_annual_cost(sid, circumstances)
        category = _resolve_category(sid, circumstances)
        total += cost
        system_details.append(
            {
                "system_id": sid,
                "label": spec["label"],
                "annual_cost": cost,
                "category": category,
                "source": spec["source"],
            }
        )
        citations.append(spec["source"])

    return {
        "domain": domain,
        "label": DOMAIN_LABELS.get(domain, domain.replace("_", " ").title()),
        "color": DOMAIN_COLORS.get(domain, "#666666"),
        "systems": system_details,
        "total_annual_cost": round(total, 2),
        "source_citations": list(set(citations)),
    }


def calculate_coordinated_cost(
    fragmented_cost: float,
    domains_involved: set[str] | list[str],
) -> tuple[float, list[dict[str, Any]]]:
    """Apply coordination savings for every domain pair present.

    For each pair of domains the person spans, the overlap portion is estimated
    as ``min(domain_a_cost, domain_b_cost)`` (conservative) and the savings
    percentage is applied to that overlap.

    In practice we use a simpler model: for every qualifying domain pair, we
    apply the savings percentage to a proportional share of the total cost.
    The share for each pair = ``2 / (N * (N-1))`` where N = number of domains.

    Returns
    -------
    Tuple of (coordinated_total, list of applied savings details).
    """
    domains = set(domains_involved)
    if len(domains) < 2:
        return fragmented_cost, []

    pairs = list(combinations(sorted(domains), 2))
    if not pairs:
        return fragmented_cost, []

    total_savings = 0.0
    savings_details: list[dict[str, Any]] = []

    # Share of total cost attributable to each pair
    pair_share = fragmented_cost / len(pairs)

    for d1, d2 in pairs:
        key = _domain_pair_key(d1, d2)
        if not key:
            continue

        entry = COORDINATION_SAVINGS[key]
        pair_savings = pair_share * entry["savings_pct"]
        total_savings += pair_savings
        savings_details.append(
            {
                "pair": f"{d1}-{d2}",
                "label": entry["label"],
                "savings_pct": entry["savings_pct"],
                "annual_savings": round(pair_savings, 2),
                "mechanisms": entry["mechanisms"],
                "source": entry["source"],
            }
        )

    coordinated = max(fragmented_cost - total_savings, 0.0)
    return round(coordinated, 2), savings_details


def calculate_savings_breakdown(
    systems: list[str],
    circumstances: dict[str, Any],
) -> list[dict[str, Any]]:
    """Return a list of specific, actionable savings opportunities.

    Each item includes the savings category, estimated annual savings, the
    mechanism by which savings are realized, confidence level, and source.
    """
    domains = _domains_for_systems(systems)
    breakdown: list[dict[str, Any]] = []

    # Avoidable-event-based savings
    for domain in domains:
        frequencies = AVOIDABLE_EVENT_FREQUENCIES.get(domain, {})
        for event_id, freq in frequencies.items():
            event = AVOIDABLE_COSTS.get(event_id)
            if not event:
                continue
            # Coordination can prevent roughly 50% of avoidable events
            preventable_fraction = 0.5
            annual_savings = event["cost"] * freq * preventable_fraction
            if annual_savings <= 0:
                continue
            breakdown.append(
                {
                    "category": event["description"],
                    "annual_savings": round(annual_savings, 2),
                    "mechanism": (
                        f"Coordination prevents ~{preventable_fraction * 100:.0f}% "
                        f"of {freq:.1f} annual events "
                        f"(${event['cost']:,}/event)"
                    ),
                    "confidence": "high" if freq >= 1.0 else "moderate",
                    "source": event["source"],
                    "domain": domain,
                }
            )

    # Coordination-pair-based savings
    for d1, d2 in combinations(sorted(domains), 2):
        key = _domain_pair_key(d1, d2)
        if not key:
            continue
        entry = COORDINATION_SAVINGS[key]
        for mechanism in entry["mechanisms"]:
            breakdown.append(
                {
                    "category": entry["label"],
                    "annual_savings": 0,  # included in coordinated cost calc
                    "mechanism": mechanism,
                    "confidence": "high",
                    "source": entry["source"],
                    "domain": f"{d1}+{d2}",
                }
            )

    # Sort by annual_savings descending, then alphabetically
    breakdown.sort(key=lambda x: (-x["annual_savings"], x["category"]))
    return breakdown


def calculate_avoidable_events(
    systems: list[str],
    circumstances: dict[str, Any],
) -> dict[str, Any]:
    """Estimate annual avoidable event costs for a person's profile.

    Returns a dict with per-event breakdowns and totals.
    """
    domains = _domains_for_systems(systems)
    events: list[dict[str, Any]] = []
    total_annual = 0.0

    # Deduplicate events across domains (take highest frequency)
    event_max_freq: dict[str, tuple[float, str]] = {}
    for domain in domains:
        frequencies = AVOIDABLE_EVENT_FREQUENCIES.get(domain, {})
        for event_id, freq in frequencies.items():
            if event_id not in event_max_freq or freq > event_max_freq[event_id][0]:
                event_max_freq[event_id] = (freq, domain)

    for event_id, (freq, domain) in event_max_freq.items():
        event = AVOIDABLE_COSTS.get(event_id)
        if not event:
            continue
        annual_cost = event["cost"] * freq
        total_annual += annual_cost
        events.append(
            {
                "event_id": event_id,
                "description": event["description"],
                "cost_per_event": event["cost"],
                "estimated_annual_frequency": freq,
                "estimated_annual_cost": round(annual_cost, 2),
                "domain": domain,
                "source": event["source"],
            }
        )

    events.sort(key=lambda x: -x["estimated_annual_cost"])

    return {
        "events": events,
        "total_annual_avoidable": round(total_annual, 2),
        "total_annual_avoidable_formatted": _format_currency(total_annual),
    }


def calculate_profile_costs(
    circumstances: dict[str, Any],
    systems_involved: list[str],
) -> dict[str, Any]:
    """Full cost calculation for a person's profile.

    Parameters
    ----------
    circumstances:
        Dict describing the person (e.g. ``{"disabled": True, "age": 34}``).
    systems_involved:
        List of system IDs the person touches (e.g. ``["mmis", "doc"]``).

    Returns
    -------
    Comprehensive cost dict including per-system, per-domain, coordinated,
    savings, projections, and avoidable event estimates.
    """
    # 1. Per-system costs
    system_costs: list[dict[str, Any]] = []
    total_fragmented = 0.0
    for sid in systems_involved:
        spec = SYSTEM_COSTS.get(sid)
        if not spec:
            continue
        cost = _system_annual_cost(sid, circumstances)
        category = _resolve_category(sid, circumstances)
        total_fragmented += cost
        system_costs.append(
            {
                "system_id": sid,
                "label": spec["label"],
                "domain": spec["domain"],
                "annual_cost": round(cost, 2),
                "category": category,
                "source": spec["source"],
            }
        )

    total_fragmented = round(total_fragmented, 2)

    # 2. Per-domain aggregation
    domains_involved = _domains_for_systems(systems_involved)
    domain_costs: list[dict[str, Any]] = []
    for domain in sorted(domains_involved):
        domain_systems = [
            sid
            for sid in systems_involved
            if SYSTEM_COSTS.get(sid, {}).get("domain") == domain
        ]
        dc = calculate_domain_costs(domain, domain_systems, circumstances)
        domain_costs.append(dc)

    # 3. Coordinated cost
    coordinated_total, coordination_details = calculate_coordinated_cost(
        total_fragmented, domains_involved
    )

    annual_savings = round(total_fragmented - coordinated_total, 2)

    # 4. Projections
    horizon = _infer_lifetime_horizon(circumstances)
    five_year_fragmented = _project_cost(total_fragmented, 5)
    five_year_coordinated = _project_cost(coordinated_total, 5)
    five_year_savings = round(five_year_fragmented - five_year_coordinated, 2)

    lifetime_fragmented = _project_cost(total_fragmented, horizon)
    lifetime_coordinated = _project_cost(coordinated_total, horizon)
    lifetime_savings = round(lifetime_fragmented - lifetime_coordinated, 2)

    # 5. Avoidable events
    avoidable = calculate_avoidable_events(systems_involved, circumstances)

    # 6. Savings breakdown
    savings_breakdown = calculate_savings_breakdown(systems_involved, circumstances)

    return {
        "summary": {
            "total_annual_cost": total_fragmented,
            "coordinated_annual_cost": coordinated_total,
            "annual_savings": annual_savings,
            "annual_savings_formatted": _format_currency(annual_savings),
            "five_year_fragmented": five_year_fragmented,
            "five_year_coordinated": five_year_coordinated,
            "five_year_savings": five_year_savings,
            "five_year_savings_formatted": _format_currency(five_year_savings),
            "lifetime_horizon_years": horizon,
            "lifetime_fragmented": lifetime_fragmented,
            "lifetime_coordinated": lifetime_coordinated,
            "lifetime_savings": lifetime_savings,
            "lifetime_savings_formatted": _format_currency(lifetime_savings),
            "domains_involved": sorted(domains_involved),
            "systems_count": len(system_costs),
        },
        "systems": system_costs,
        "domains": domain_costs,
        "coordination": {
            "pairs_applied": len(coordination_details),
            "details": coordination_details,
        },
        "avoidable_events": avoidable,
        "savings_breakdown": savings_breakdown,
    }


def calculate_roi(
    coordination_cost: float,
    annual_savings: float,
    years: int = 5,
) -> dict[str, Any]:
    """Calculate return on investment for coordination infrastructure.

    Parameters
    ----------
    coordination_cost:
        One-time investment in coordination infrastructure.
    annual_savings:
        Expected annual savings from coordination.
    years:
        Projection horizon (default 5).

    Returns
    -------
    Dict with break-even, ROI, and net savings at 5 and 10 years.
    """
    if annual_savings <= 0:
        return {
            "coordination_cost": coordination_cost,
            "annual_savings": annual_savings,
            "break_even_months": None,
            "five_year_roi": 0.0,
            "five_year_net": -coordination_cost,
            "ten_year_net": -coordination_cost,
        }

    break_even_months = (coordination_cost / annual_savings) * 12

    cumulative_savings_at_years = _project_cost(annual_savings, years)
    five_year_net = round(cumulative_savings_at_years - coordination_cost, 2)
    five_year_roi = (
        round(five_year_net / coordination_cost, 2) if coordination_cost > 0 else 0.0
    )

    ten_year_savings = _project_cost(annual_savings, 10)
    ten_year_net = round(ten_year_savings - coordination_cost, 2)

    return {
        "coordination_cost": coordination_cost,
        "annual_savings": annual_savings,
        "break_even_months": round(break_even_months, 1),
        "five_year_roi": five_year_roi,
        "five_year_net": five_year_net,
        "ten_year_net": ten_year_net,
        "formatted": {
            "coordination_cost": _format_currency(coordination_cost),
            "annual_savings": _format_currency(annual_savings),
            "five_year_net": _format_currency(five_year_net),
            "ten_year_net": _format_currency(ten_year_net),
            "roi_pct": f"{five_year_roi * 100:.0f}%",
        },
    }


def scale_savings(
    per_person_savings: float,
    population_sizes: dict[str, int] | None = None,
) -> dict[str, Any]:
    """Scale per-person savings to population levels.

    Parameters
    ----------
    per_person_savings:
        Annual savings for one person.
    population_sizes:
        Optional dict of population label to size. Defaults to standard tiers.

    Returns
    -------
    Dict with raw and formatted savings at each population level.
    """
    if population_sizes is None:
        population_sizes = {
            "city_10k": 10_000,
            "county_50k": 50_000,
            "state_500k": 500_000,
        }

    result: dict[str, Any] = {
        "per_person": round(per_person_savings, 2),
    }
    formatted: dict[str, str] = {
        "per_person": _format_currency(per_person_savings),
    }

    for label, size in population_sizes.items():
        total = round(per_person_savings * size, 2)
        result[label] = total
        formatted[label] = _format_currency(total)

    result["formatted"] = formatted
    return result


def get_benchmarks_summary() -> dict[str, Any]:
    """Return all benchmarks organized by domain for the frontend.

    Every number includes its source citation.
    """
    # Group systems by domain
    by_domain: dict[str, list[dict[str, Any]]] = {}
    for sid, spec in SYSTEM_COSTS.items():
        domain = spec["domain"]
        if domain not in by_domain:
            by_domain[domain] = []
        entry: dict[str, Any] = {
            "system_id": sid,
            "label": spec["label"],
            "base_cost": spec["base_cost"],
            "source": spec["source"],
        }
        if "categories" in spec:
            entry["categories"] = {
                k: {"cost": v, "source": spec["source"]}
                for k, v in spec["categories"].items()
            }
        by_domain[domain].append(entry)

    # Build domain summaries
    domains_summary: list[dict[str, Any]] = []
    for domain in sorted(by_domain.keys()):
        systems_list = by_domain[domain]
        domains_summary.append(
            {
                "domain": domain,
                "label": DOMAIN_LABELS.get(domain, domain.replace("_", " ").title()),
                "color": DOMAIN_COLORS.get(domain, "#666666"),
                "systems": systems_list,
                "system_count": len(systems_list),
            }
        )

    # Coordination savings
    coordination_list: list[dict[str, Any]] = []
    for key, entry in COORDINATION_SAVINGS.items():
        coordination_list.append(
            {
                "pair_key": key,
                "label": entry["label"],
                "savings_pct": entry["savings_pct"],
                "savings_pct_display": f"{entry['savings_pct'] * 100:.0f}%",
                "mechanisms": entry["mechanisms"],
                "source": entry["source"],
            }
        )

    # Avoidable events
    avoidable_list: list[dict[str, Any]] = []
    for eid, entry in AVOIDABLE_COSTS.items():
        avoidable_list.append(
            {
                "event_id": eid,
                "cost": entry["cost"],
                "cost_formatted": _format_currency(entry["cost"]),
                "description": entry["description"],
                "source": entry["source"],
            }
        )

    return {
        "domains": domains_summary,
        "coordination_savings": coordination_list,
        "avoidable_events": avoidable_list,
        "metadata": {
            "total_systems": len(SYSTEM_COSTS),
            "total_domains": len(by_domain),
            "inflation_rate": ANNUAL_INFLATION_RATE,
            "coordination_pairs": len(COORDINATION_SAVINGS),
        },
    }
