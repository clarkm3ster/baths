"""
Cost API routes for DOMES Profiles.

Provides endpoints for cost calculations, benchmarks, ROI, and scaling.
All cost data includes published source citations.
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from ..benchmarks import AVOIDABLE_COSTS, SYSTEM_COSTS
from ..cost_engine import (
    calculate_profile_costs,
    calculate_roi,
    get_benchmarks_summary,
    scale_savings,
)

router = APIRouter(prefix="/api/cost", tags=["costs"])


# ---------------------------------------------------------------------------
# Request / Response Models
# ---------------------------------------------------------------------------


class CostCalculateRequest(BaseModel):
    """Request body for profile cost calculation."""

    circumstances: dict[str, Any] = Field(
        default_factory=dict,
        description="Person-level circumstances (e.g. disabled, age, substance_use)",
        examples=[{"disabled": True, "substance_use": True, "age": 34}],
    )
    systems: list[str] = Field(
        ...,
        description="List of system IDs the person touches",
        examples=[["mmis", "bha", "doc", "hmis"]],
    )


class ROIRequest(BaseModel):
    """Request body for ROI calculation."""

    coordination_cost: float = Field(
        ...,
        gt=0,
        description="One-time coordination infrastructure investment",
        examples=[150000],
    )
    annual_savings: float = Field(
        ...,
        description="Expected annual savings from coordination",
        examples=[48000],
    )
    years: int = Field(
        default=5,
        ge=1,
        le=30,
        description="Projection horizon in years",
    )


class ScaleRequest(BaseModel):
    """Request body for population-scale savings."""

    per_person_savings: float = Field(
        ...,
        description="Annual savings per person",
        examples=[48000],
    )
    populations: dict[str, int] = Field(
        default_factory=lambda: {
            "city": 10_000,
            "county": 50_000,
            "state": 500_000,
        },
        description="Population labels mapped to sizes",
    )


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------


@router.post("/calculate")
def cost_calculate(body: CostCalculateRequest) -> dict[str, Any]:
    """Calculate full cost profile for a person.

    Given a set of circumstances and the systems they touch, returns:
    - Per-system annual costs (with category selection)
    - Per-domain aggregation
    - Coordinated cost (with savings from domain-pair coordination)
    - 5-year and lifetime projections
    - Avoidable event estimates
    - Savings breakdown with mechanisms and sources
    """
    # Validate that at least one system is recognized
    valid_systems = [s for s in body.systems if s in SYSTEM_COSTS]
    if not valid_systems:
        raise HTTPException(
            status_code=400,
            detail={
                "error": "No recognized systems provided.",
                "valid_systems": sorted(SYSTEM_COSTS.keys()),
            },
        )

    unknown = set(body.systems) - set(valid_systems)
    result = calculate_profile_costs(body.circumstances, valid_systems)

    if unknown:
        result["warnings"] = {
            "unknown_systems": sorted(unknown),
            "message": f"{len(unknown)} system(s) not recognized and were excluded.",
        }

    return result


@router.get("/benchmarks")
def cost_benchmarks() -> dict[str, Any]:
    """Return all cost benchmarks organized by domain.

    Includes system costs, coordination savings percentages, avoidable event
    costs, and source citations for every number.
    """
    return get_benchmarks_summary()


@router.get("/benchmarks/{system_id}")
def cost_benchmark_detail(system_id: str) -> dict[str, Any]:
    """Return benchmark data for a specific system.

    Includes base cost, category breakdowns, domain, and source citation.
    """
    spec = SYSTEM_COSTS.get(system_id)
    if not spec:
        raise HTTPException(
            status_code=404,
            detail={
                "error": f"System '{system_id}' not found.",
                "valid_systems": sorted(SYSTEM_COSTS.keys()),
            },
        )

    result: dict[str, Any] = {
        "system_id": system_id,
        "label": spec["label"],
        "domain": spec["domain"],
        "base_cost": spec["base_cost"],
        "source": spec["source"],
    }

    if "categories" in spec:
        result["categories"] = {
            k: {"cost": v, "source": spec["source"]}
            for k, v in spec["categories"].items()
        }

    return result


@router.post("/roi")
def cost_roi(body: ROIRequest) -> dict[str, Any]:
    """Calculate return on investment for coordination infrastructure.

    Returns break-even time, 5-year and 10-year ROI, and net savings.
    """
    return calculate_roi(body.coordination_cost, body.annual_savings, body.years)


@router.post("/scale")
def cost_scale(body: ScaleRequest) -> dict[str, Any]:
    """Scale per-person savings to population levels.

    Returns both raw numbers and formatted currency strings for each
    population tier.
    """
    return scale_savings(body.per_person_savings, body.populations)


@router.get("/avoidable-events")
def avoidable_events() -> dict[str, Any]:
    """Return all avoidable cost event benchmarks.

    Each event includes per-occurrence cost, description, and published source.
    """
    events: list[dict[str, Any]] = []
    for eid, entry in AVOIDABLE_COSTS.items():
        events.append(
            {
                "event_id": eid,
                "cost": entry["cost"],
                "cost_formatted": f"${entry['cost']:,}",
                "description": entry["description"],
                "source": entry["source"],
            }
        )

    # Sort by cost descending
    events.sort(key=lambda x: -x["cost"])

    return {
        "events": events,
        "count": len(events),
    }
