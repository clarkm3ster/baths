"""Provider Marketplace -- makes recommendations executable.

Provides:
- Provider registry with service types, insurance, languages, and quality scores
- Smart provider matching against person needs (multi-factor scoring)
- Referral lifecycle tracking (created -> sent -> accepted -> completed)
- Outcome tracking to close the feedback loop

All functions are stdlib-only and operate on Pydantic models.
"""
from __future__ import annotations

import math
import uuid
from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------

class Provider(BaseModel):
    """A service provider in the marketplace."""
    provider_id: str = Field(default_factory=lambda: f"prov-{uuid.uuid4().hex[:12]}")
    name: str
    service_types: list[str] = Field(
        default_factory=list,
        description="Services offered, e.g. 'mental_health', 'primary_care', 'housing_assistance'",
    )
    accepts_medicaid: bool = False
    accepts_medicare: bool = False
    sliding_scale: bool = False
    languages: list[str] = Field(default_factory=lambda: ["en"])
    location: dict[str, Any] = Field(
        default_factory=dict,
        description="Location dict with lat, lng, and address fields",
    )
    availability_score: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
        description="Current availability (0 = fully booked, 1 = wide open)",
    )
    quality_score: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
        description="Composite quality score from outcomes and reviews",
    )
    wait_days: int = Field(default=14, ge=0)


class Referral(BaseModel):
    """A referral linking a person to a provider for a specific service."""
    referral_id: str = Field(default_factory=lambda: f"ref-{uuid.uuid4().hex[:12]}")
    person_id: str
    provider_id: str
    service_type: str
    status: Literal[
        "created", "sent", "accepted", "completed", "no_show", "cancelled"
    ] = "created"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    outcome_score: float | None = Field(
        default=None,
        description="Post-service outcome rating (0.0 - 1.0), set after completion",
    )


# ---------------------------------------------------------------------------
# Distance calculation (Haversine)
# ---------------------------------------------------------------------------

_EARTH_RADIUS_MILES = 3_958.8


def _haversine_miles(
    lat1: float, lng1: float,
    lat2: float, lng2: float,
) -> float:
    """Great-circle distance between two lat/lng points in miles."""
    lat1_r, lat2_r = math.radians(lat1), math.radians(lat2)
    dlat = math.radians(lat2 - lat1)
    dlng = math.radians(lng2 - lng1)

    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1_r) * math.cos(lat2_r) * math.sin(dlng / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return _EARTH_RADIUS_MILES * c


# ---------------------------------------------------------------------------
# Provider matching
# ---------------------------------------------------------------------------

def match_providers(
    person_needs: dict[str, Any],
    providers: list[Provider],
    max_results: int = 5,
) -> list[dict[str, Any]]:
    """Score and rank providers against a person's needs.

    Scoring factors (weights sum to 1.0):
    - Service match (0.30): Does the provider offer the needed service type?
    - Insurance acceptance (0.20): Accepts person's insurance (Medicaid/Medicare/sliding)?
    - Language match (0.10): Speaks the person's preferred language?
    - Distance (0.15): Geographic proximity (closer is better).
    - Availability (0.15): How soon can the person be seen?
    - Quality (0.10): Historical outcome and review scores.

    Args:
        person_needs: Dict with keys like:
            - service_type (str): Required service type
            - insurance (str): 'medicaid', 'medicare', 'private', or 'none'
            - language (str): Preferred language code, e.g. 'en', 'es'
            - location (dict): Person's location with lat/lng
            - max_distance_miles (float): Maximum acceptable distance
        providers: List of Provider instances to score.
        max_results: Maximum number of matches to return.

    Returns:
        List of dicts sorted by score (descending), each containing:
        - provider: the Provider model
        - total_score: float 0-1
        - score_breakdown: dict of factor -> score
    """
    needed_service = person_needs.get("service_type", "")
    insurance = (person_needs.get("insurance", "") or "").lower()
    language = (person_needs.get("language", "en") or "en").lower()
    person_loc = person_needs.get("location", {})
    max_dist = float(person_needs.get("max_distance_miles", 25.0))

    person_lat = person_loc.get("lat")
    person_lng = person_loc.get("lng")

    scored: list[dict[str, Any]] = []

    for provider in providers:
        breakdown: dict[str, float] = {}

        # 1. Service match (0.30)
        service_types_lower = [s.lower() for s in provider.service_types]
        if needed_service.lower() in service_types_lower:
            breakdown["service_match"] = 1.0
        else:
            # Partial credit for related services
            breakdown["service_match"] = 0.0

        # 2. Insurance acceptance (0.20)
        insurance_score = 0.0
        if insurance == "medicaid" and provider.accepts_medicaid:
            insurance_score = 1.0
        elif insurance == "medicare" and provider.accepts_medicare:
            insurance_score = 1.0
        elif insurance == "none" and provider.sliding_scale:
            insurance_score = 1.0
        elif insurance == "private":
            insurance_score = 0.8  # most providers accept private
        elif provider.sliding_scale:
            insurance_score = 0.5  # sliding scale is a fallback
        breakdown["insurance_acceptance"] = insurance_score

        # 3. Language match (0.10)
        provider_langs_lower = [lang.lower() for lang in provider.languages]
        if language in provider_langs_lower:
            breakdown["language_match"] = 1.0
        elif "en" in provider_langs_lower:
            breakdown["language_match"] = 0.3  # English as fallback
        else:
            breakdown["language_match"] = 0.0

        # 4. Distance (0.15)
        if person_lat is not None and person_lng is not None:
            prov_lat = provider.location.get("lat")
            prov_lng = provider.location.get("lng")
            if prov_lat is not None and prov_lng is not None:
                dist = _haversine_miles(person_lat, person_lng, prov_lat, prov_lng)
                if dist <= max_dist:
                    # Linear decay: 0 miles = 1.0, max_dist = 0.0
                    breakdown["distance"] = max(1.0 - (dist / max_dist), 0.0)
                else:
                    breakdown["distance"] = 0.0
            else:
                breakdown["distance"] = 0.5  # unknown location, neutral
        else:
            breakdown["distance"] = 0.5

        # 5. Availability (0.15)
        breakdown["availability"] = provider.availability_score

        # 6. Quality (0.10)
        breakdown["quality"] = provider.quality_score

        # Weighted total
        weights = {
            "service_match": 0.30,
            "insurance_acceptance": 0.20,
            "language_match": 0.10,
            "distance": 0.15,
            "availability": 0.15,
            "quality": 0.10,
        }
        total = sum(
            breakdown.get(factor, 0.0) * weight
            for factor, weight in weights.items()
        )

        scored.append({
            "provider": provider,
            "total_score": round(total, 4),
            "score_breakdown": {k: round(v, 4) for k, v in breakdown.items()},
        })

    # Sort by total score descending, then by wait_days ascending as tiebreaker
    scored.sort(key=lambda x: (-x["total_score"], x["provider"].wait_days))

    return scored[:max_results]


# ---------------------------------------------------------------------------
# Referral lifecycle
# ---------------------------------------------------------------------------

def create_referral(
    person_id: str,
    provider_id: str,
    service_type: str,
) -> Referral:
    """Create a new referral linking a person to a provider.

    Args:
        person_id: The person being referred.
        provider_id: The target provider.
        service_type: The service being referred for.

    Returns:
        A new Referral with status 'created'.
    """
    return Referral(
        person_id=person_id,
        provider_id=provider_id,
        service_type=service_type,
        status="created",
    )


def track_outcome(
    referral: Referral,
    outcome_score: float,
    notes: str = "",
) -> Referral:
    """Record the outcome of a completed referral.

    Updates the referral's outcome_score and advances status to 'completed'
    if it is not already in a terminal state.

    Args:
        referral: The Referral to update.
        outcome_score: A score from 0.0 (poor) to 1.0 (excellent).
        notes: Optional freeform notes about the outcome.

    Returns:
        Updated Referral with outcome_score set and status advanced.

    Raises:
        ValueError: If outcome_score is outside [0, 1].
    """
    if not 0.0 <= outcome_score <= 1.0:
        raise ValueError(
            f"outcome_score must be between 0.0 and 1.0, got {outcome_score}"
        )

    # Advance to completed if still in an active state
    terminal_states = {"completed", "no_show", "cancelled"}
    new_status = referral.status
    if referral.status not in terminal_states:
        new_status = "completed"

    return referral.model_copy(update={
        "outcome_score": outcome_score,
        "status": new_status,
    })
