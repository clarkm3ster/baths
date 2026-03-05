"""Spatial / Mobility Layer — Dynamic Friction-of-Movement Analysis.

Goes beyond static distance to model *actual* accessibility: transit time,
cost, physical constraints, time-of-day windows, and personal barriers.
Produces per-destination access scores and an overall mobility profile
that feeds into settlement and intervention planning.

Provides:
- MobilityProfile / AccessScore / SpatialAnalysis models
- calculate_access_score  — single-destination friction score
- analyze_spatial_access  — full spatial analysis across destinations
- estimate_mobility_cost  — monthly cost feasibility check

Distance approximation uses the Haversine formula (stdlib math only).
Transit time is estimated at 3x straight-line time; driving at 1.5x.
"""
from __future__ import annotations

import math
import uuid
from typing import Any, Optional

from pydantic import BaseModel, Field


# ── Models ────────────────────────────────────────────────────────

class MobilityProfile(BaseModel):
    """A person's transportation capabilities and constraints."""
    person_id: str
    home_location: dict[str, float] = Field(
        default_factory=dict,
        description="{'lat': ..., 'lng': ...}",
    )
    has_vehicle: bool = False
    transit_pass: bool = False
    mobility_constraints: list[str] = Field(
        default_factory=list,
        description="e.g. ['wheelchair', 'no_night_transit', 'child_care_hours']",
    )
    typical_travel_budget_monthly: float = 0.0


class AccessScore(BaseModel):
    """Accessibility evaluation for a single destination."""
    destination_type: str = Field(description="e.g. 'hospital', 'grocery', 'pharmacy'")
    destination_name: str = ""
    straight_line_miles: float = 0.0
    transit_minutes: float = 0.0
    drive_minutes: float = 0.0
    cost_per_trip: float = 0.0
    accessibility_score: float = Field(
        ge=0.0, le=1.0,
        description="Composite score 0 (inaccessible) to 1 (fully accessible)",
    )
    barriers: list[str] = Field(default_factory=list)


class SpatialAnalysis(BaseModel):
    """Full spatial access analysis for a person."""
    person_id: str
    access_scores: list[AccessScore] = Field(default_factory=list)
    overall_mobility_score: float = Field(
        ge=0.0, le=1.0,
        description="Mean accessibility across all destinations",
    )
    critical_gaps: list[str] = Field(default_factory=list)
    recommendations: list[str] = Field(default_factory=list)


# ── Constants ─────────────────────────────────────────────────────

EARTH_RADIUS_MILES = 3958.8

# Average speed assumptions (mph)
_AVG_DRIVE_SPEED_MPH = 30.0
_AVG_TRANSIT_SPEED_MPH = 12.0

# Cost per mile estimates
_COST_PER_MILE_DRIVE = 0.67       # IRS-ish rate
_COST_PER_MILE_TRANSIT = 0.15     # per-trip amortised

# Critical destination types — gaps here are flagged
_CRITICAL_DESTINATION_TYPES = {
    "hospital", "pharmacy", "grocery", "dialysis",
    "primary_care", "mental_health", "wic_office",
}

# Score thresholds
_LOW_ACCESS_THRESHOLD = 0.4
_VERY_LOW_ACCESS_THRESHOLD = 0.2


# ── Haversine ─────────────────────────────────────────────────────

def _haversine_miles(
    lat1: float, lng1: float,
    lat2: float, lng2: float,
) -> float:
    """Great-circle distance between two points in miles."""
    lat1_r, lng1_r = math.radians(lat1), math.radians(lng1)
    lat2_r, lng2_r = math.radians(lat2), math.radians(lng2)

    dlat = lat2_r - lat1_r
    dlng = lng2_r - lng1_r

    a = (
        math.sin(dlat / 2.0) ** 2
        + math.cos(lat1_r) * math.cos(lat2_r) * math.sin(dlng / 2.0) ** 2
    )
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))

    return EARTH_RADIUS_MILES * c


# ── Helpers ───────────────────────────────────────────────────────

def _estimate_drive_minutes(miles: float) -> float:
    """Estimate drive time: 1.5x straight-line distance at avg speed."""
    effective_miles = miles * 1.5
    return (effective_miles / _AVG_DRIVE_SPEED_MPH) * 60.0


def _estimate_transit_minutes(miles: float) -> float:
    """Estimate transit time: 3x straight-line distance at avg speed."""
    effective_miles = miles * 3.0
    return (effective_miles / _AVG_TRANSIT_SPEED_MPH) * 60.0


def _estimate_trip_cost(
    miles: float,
    has_vehicle: bool,
    transit_pass: bool,
) -> float:
    """Estimate single-trip cost based on available transport modes."""
    drive_cost = miles * 1.5 * _COST_PER_MILE_DRIVE if has_vehicle else float("inf")
    transit_cost = (
        miles * 3.0 * _COST_PER_MILE_TRANSIT if transit_pass
        else 2.75  # flat single-ride fare assumption
    )

    if has_vehicle and transit_pass:
        return min(drive_cost, transit_cost)
    elif has_vehicle:
        return drive_cost
    elif transit_pass:
        return transit_cost
    else:
        # Rideshare estimate: base + per-mile
        return 5.0 + miles * 2.0


def _identify_barriers(
    profile: MobilityProfile,
    destination: dict[str, Any],
    miles: float,
    trip_cost: float,
) -> list[str]:
    """Identify specific barriers to reaching a destination."""
    barriers: list[str] = []

    # Distance barrier
    if miles > 25:
        barriers.append("extreme_distance")
    elif miles > 10:
        barriers.append("significant_distance")

    # Cost barrier
    monthly_budget = profile.typical_travel_budget_monthly
    if monthly_budget > 0 and trip_cost > monthly_budget * 0.25:
        barriers.append("cost_prohibitive_single_trip")

    # Vehicle barrier
    if not profile.has_vehicle and not profile.transit_pass:
        barriers.append("no_reliable_transport")

    # Constraint-based barriers
    constraints = {c.lower() for c in profile.mobility_constraints}
    dest_accessible = destination.get("wheelchair_accessible", True)

    if "wheelchair" in constraints and not dest_accessible:
        barriers.append("not_wheelchair_accessible")

    if "no_night_transit" in constraints:
        hours = destination.get("hours", "")
        if "evening" in str(hours).lower() or "night" in str(hours).lower():
            barriers.append("requires_night_transit")

    if "child_care_hours" in constraints:
        # Destinations only open during school hours are problematic
        if destination.get("hours_restricted_daytime", False):
            barriers.append("conflicts_with_child_care")

    if "limited_walking" in constraints and miles > 0.5:
        if not profile.has_vehicle:
            barriers.append("walking_distance_exceeds_ability")

    return barriers


def _score_accessibility(
    miles: float,
    transit_min: float,
    drive_min: float,
    trip_cost: float,
    barriers: list[str],
    has_vehicle: bool,
    transit_pass: bool,
) -> float:
    """Compute composite accessibility score in [0, 1].

    Components (weighted):
      - distance_score    (0.25): decays with distance
      - time_score        (0.30): decays with best available travel time
      - cost_score        (0.20): decays with cost
      - barrier_penalty   (0.25): each barrier reduces score
    """
    # Distance score: 1.0 at 0 mi, decays to ~0.1 at 30 mi
    distance_score = math.exp(-0.08 * miles)

    # Time score: best available mode
    if has_vehicle:
        best_minutes = drive_min
    elif transit_pass:
        best_minutes = transit_min
    else:
        best_minutes = transit_min * 1.3  # rideshare wait overhead
    time_score = math.exp(-0.02 * best_minutes)

    # Cost score
    cost_score = math.exp(-0.15 * trip_cost) if trip_cost < float("inf") else 0.0

    # Barrier penalty: each barrier reduces score by 0.15, min 0
    barrier_score = max(1.0 - len(barriers) * 0.15, 0.0)

    composite = (
        0.25 * distance_score
        + 0.30 * time_score
        + 0.20 * cost_score
        + 0.25 * barrier_score
    )

    return round(max(min(composite, 1.0), 0.0), 4)


# ── Core functions ────────────────────────────────────────────────

def calculate_access_score(
    person_profile: MobilityProfile,
    destination: dict[str, Any],
) -> AccessScore:
    """Calculate accessibility of a single destination for a person.

    The destination dict should contain at minimum:
      - type: str (e.g. "hospital")
      - name: str
      - lat: float
      - lng: float
    Optional keys: wheelchair_accessible, hours, hours_restricted_daytime.
    """
    home = person_profile.home_location
    home_lat = home.get("lat", 0.0)
    home_lng = home.get("lng", 0.0)
    dest_lat = float(destination.get("lat", 0.0))
    dest_lng = float(destination.get("lng", 0.0))

    miles = _haversine_miles(home_lat, home_lng, dest_lat, dest_lng)
    transit_min = _estimate_transit_minutes(miles)
    drive_min = _estimate_drive_minutes(miles)
    trip_cost = _estimate_trip_cost(
        miles, person_profile.has_vehicle, person_profile.transit_pass,
    )

    barriers = _identify_barriers(person_profile, destination, miles, trip_cost)

    score = _score_accessibility(
        miles, transit_min, drive_min, trip_cost,
        barriers,
        person_profile.has_vehicle,
        person_profile.transit_pass,
    )

    return AccessScore(
        destination_type=destination.get("type", "unknown"),
        destination_name=destination.get("name", ""),
        straight_line_miles=round(miles, 2),
        transit_minutes=round(transit_min, 1),
        drive_minutes=round(drive_min, 1),
        cost_per_trip=round(trip_cost, 2),
        accessibility_score=score,
        barriers=barriers,
    )


def analyze_spatial_access(
    person_profile: MobilityProfile,
    destinations: list[dict[str, Any]],
) -> SpatialAnalysis:
    """Score all destinations and produce a full spatial analysis.

    Identifies critical gaps (essential destination types with low access)
    and generates actionable recommendations.
    """
    scores: list[AccessScore] = []
    for dest in destinations:
        scores.append(calculate_access_score(person_profile, dest))

    # Overall mobility score: mean of individual scores
    if scores:
        overall = sum(s.accessibility_score for s in scores) / len(scores)
    else:
        overall = 0.0

    # Critical gaps: essential destinations below threshold
    critical_gaps: list[str] = []
    for s in scores:
        if (
            s.destination_type in _CRITICAL_DESTINATION_TYPES
            and s.accessibility_score < _LOW_ACCESS_THRESHOLD
        ):
            gap_msg = (
                f"{s.destination_type} ({s.destination_name}): "
                f"score {s.accessibility_score:.2f}, "
                f"{s.straight_line_miles:.1f} mi"
            )
            if s.barriers:
                gap_msg += f", barriers: {', '.join(s.barriers)}"
            critical_gaps.append(gap_msg)

    # Recommendations
    recommendations: list[str] = _generate_recommendations(person_profile, scores)

    return SpatialAnalysis(
        person_id=person_profile.person_id,
        access_scores=scores,
        overall_mobility_score=round(overall, 4),
        critical_gaps=critical_gaps,
        recommendations=recommendations,
    )


def _generate_recommendations(
    profile: MobilityProfile,
    scores: list[AccessScore],
) -> list[str]:
    """Generate mobility recommendations based on gaps and barriers."""
    recs: list[str] = []

    # Aggregate barrier types
    all_barriers: list[str] = []
    for s in scores:
        all_barriers.extend(s.barriers)

    barrier_counts: dict[str, int] = {}
    for b in all_barriers:
        barrier_counts[b] = barrier_counts.get(b, 0) + 1

    # No vehicle and no transit
    if not profile.has_vehicle and not profile.transit_pass:
        recs.append(
            "Enroll in transit assistance program or subsidized transit pass"
        )

    if barrier_counts.get("no_reliable_transport", 0) > 0:
        recs.append(
            "Connect with community ride-share or medical transport services"
        )

    if barrier_counts.get("cost_prohibitive_single_trip", 0) >= 2:
        recs.append(
            "Explore consolidated trip scheduling to reduce per-trip costs"
        )

    if barrier_counts.get("not_wheelchair_accessible", 0) > 0:
        recs.append(
            "Identify ADA-compliant alternatives for inaccessible destinations"
        )

    if barrier_counts.get("requires_night_transit", 0) > 0:
        recs.append(
            "Request daytime appointment slots or arrange evening transport"
        )

    if barrier_counts.get("conflicts_with_child_care", 0) > 0:
        recs.append(
            "Coordinate child care support for appointment windows"
        )

    # Very low overall access
    very_low = [
        s for s in scores
        if s.accessibility_score < _VERY_LOW_ACCESS_THRESHOLD
        and s.destination_type in _CRITICAL_DESTINATION_TYPES
    ]
    if very_low:
        dest_names = ", ".join(s.destination_type for s in very_low)
        recs.append(
            f"Investigate telehealth or mobile service alternatives for: {dest_names}"
        )

    # Long distance pattern
    far_dests = [s for s in scores if s.straight_line_miles > 15]
    if len(far_dests) >= 2:
        recs.append(
            "Consider relocation assistance or closer provider network options"
        )

    return recs


def estimate_mobility_cost(
    profile: MobilityProfile,
    destinations_per_month: dict[str, int],
) -> dict[str, Any]:
    """Estimate monthly travel cost and feasibility.

    Args:
        profile: The person's mobility profile.
        destinations_per_month: Mapping of destination_name -> trips/month.
            Destination names are looked up by matching against the profile;
            for simplicity this uses a flat cost-per-trip estimate.

    Returns:
        Dict with monthly_cost, as_percent_of_income (if budget known),
        and feasible (bool — cost within monthly travel budget).
    """
    # Estimate average cost per trip from profile transport modes
    # Use a baseline distance of 5 miles for budgeting when we don't have
    # specific destination data.
    baseline_miles = 5.0
    cost_per_trip = _estimate_trip_cost(
        baseline_miles, profile.has_vehicle, profile.transit_pass,
    )

    total_trips = sum(destinations_per_month.values())
    monthly_cost = round(cost_per_trip * total_trips, 2)

    budget = profile.typical_travel_budget_monthly
    feasible = monthly_cost <= budget if budget > 0 else False

    as_pct = round((monthly_cost / budget) * 100.0, 1) if budget > 0 else 0.0

    return {
        "monthly_cost": monthly_cost,
        "trips_per_month": total_trips,
        "avg_cost_per_trip": round(cost_per_trip, 2),
        "as_percent_of_budget": as_pct,
        "feasible": feasible,
    }
