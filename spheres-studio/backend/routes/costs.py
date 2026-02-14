"""
SPHERES Studio — Cost Estimation API Routes
=============================================
FastAPI router for real-time cost estimation, benchmarks, and budget
generation for public space activations.

Endpoints:
  POST /api/cost/estimate   — Detailed cost breakdown from design elements
  GET  /api/cost/benchmarks — Benchmark costs for different activation types
  POST /api/cost/budget     — Full line-item budget from a design spec
"""

from __future__ import annotations

import math

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Any, Optional

from services.cost_calculator import (
    CostCalculator,
    DesignElement,
    DesignSpec,
    ACTIVATION_BENCHMARKS,
    MATERIAL_CATALOG,
)


router = APIRouter(prefix="/api/cost", tags=["cost"])

calculator = CostCalculator()


# ---------------------------------------------------------------------------
# Request / Response models
# ---------------------------------------------------------------------------

class ElementInput(BaseModel):
    """A single design element for cost estimation."""
    element_type: str = Field(
        ...,
        description="Element type key from the material catalog (e.g. 'bench', 'stage', 'raised_bed')",
    )
    quantity: int = Field(
        default=1,
        ge=1,
        description="Number of this element",
    )
    custom_unit_cost: Optional[float] = Field(
        default=None,
        ge=0,
        description="Override the catalog unit cost with a custom value",
    )
    custom_name: Optional[str] = Field(
        default=None,
        description="Custom display name for the element",
    )


class EstimateRequest(BaseModel):
    """Request body for POST /api/cost/estimate."""
    elements: list[ElementInput] = Field(
        ...,
        min_length=1,
        description="List of design elements to estimate costs for",
    )
    duration_days: int = Field(
        default=1,
        ge=1,
        description="Duration of the activation in days",
    )
    activation_type: str = Field(
        default="event",
        description="Type of activation: event, performance, pop_up_market, community_garden, art_installation, block_party, etc.",
    )
    size_sqft: float = Field(
        default=1000.0,
        ge=100,
        description="Total activation area in square feet",
    )
    location_score: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
        description="Location quality score (0=low visibility, 1=prime location)",
    )
    expected_attendance: int = Field(
        default=100,
        ge=1,
        description="Expected daily attendance",
    )
    event_type: str = Field(
        default="community",
        description="Event type for insurance calculation: community, commercial, nonprofit, festival, market, garden, art",
    )
    parcel_type: str = Field(
        default="park",
        description="Property type: park, vacant_lot, street, sidewalk, plaza, parking_lot",
    )
    permanence_score: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
        description="How permanent the design is (0=fully temporary, 1=fully permanent)",
    )
    equity_score: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
        description="Equity priority score for the location (0=low priority, 1=high priority)",
    )


class BudgetRequest(BaseModel):
    """Request body for POST /api/cost/budget."""
    elements: list[ElementInput] = Field(
        ...,
        min_length=1,
        description="List of design elements",
    )
    duration_days: int = Field(default=1, ge=1)
    activation_type: str = Field(default="event")
    size_sqft: float = Field(default=1000.0, ge=100)
    location_score: float = Field(default=0.5, ge=0.0, le=1.0)
    expected_attendance: int = Field(default=100, ge=1)
    event_type: str = Field(default="community")
    parcel_type: str = Field(default="park")
    permanence_score: float = Field(default=0.5, ge=0.0, le=1.0)
    equity_score: float = Field(default=0.5, ge=0.0, le=1.0)


class EstimateResponse(BaseModel):
    """Response body for POST /api/cost/estimate."""
    elements_cost: dict[str, float]
    permits_cost: dict[str, float]
    operations_cost: dict[str, float]
    teardown_cost: float
    permanent_improvements_value: float
    total_cost: float
    cost_breakdown: list[dict[str, Any]]
    revenue_projections: dict[str, float]
    net_projection: float
    permanence_value: float
    roi_with_permanence: float


class BudgetResponse(BaseModel):
    """Response body for POST /api/cost/budget."""
    budget_lines: list[dict[str, Any]]
    total_cost: float
    revenue_projections: dict[str, float]
    net_projection: float
    permanence_value: float
    roi_with_permanence: float
    permits_required: list[dict[str, Any]]
    summary: dict[str, float]


# ---------------------------------------------------------------------------
# Helper: convert request models to domain objects
# ---------------------------------------------------------------------------

def _to_design_elements(inputs: list[ElementInput]) -> list[DesignElement]:
    """Convert Pydantic ElementInput models to DesignElement dataclass instances."""
    elements: list[DesignElement] = []
    for inp in inputs:
        elements.append(DesignElement(
            element_type=inp.element_type,
            quantity=inp.quantity,
            custom_unit_cost=inp.custom_unit_cost,
            custom_name=inp.custom_name,
        ))
    return elements


def _to_design_spec(
    elements: list[ElementInput],
    duration_days: int = 1,
    activation_type: str = "event",
    size_sqft: float = 1000.0,
    location_score: float = 0.5,
    expected_attendance: int = 100,
    event_type: str = "community",
    parcel_type: str = "park",
    permanence_score: float = 0.5,
    equity_score: float = 0.5,
) -> DesignSpec:
    """Build a DesignSpec from request parameters."""
    return DesignSpec(
        elements=_to_design_elements(elements),
        duration_days=duration_days,
        activation_type=activation_type,
        size_sqft=size_sqft,
        location_score=location_score,
        expected_attendance=expected_attendance,
        event_type=event_type,
        parcel_type=parcel_type,
        permanence_score=permanence_score,
        equity_score=equity_score,
    )


# ---------------------------------------------------------------------------
# POST /api/cost/estimate
# ---------------------------------------------------------------------------

@router.post("/estimate", response_model=EstimateResponse)
def estimate_costs(req: EstimateRequest) -> dict[str, Any]:
    """
    Calculate a detailed cost breakdown from a list of design elements.

    Returns material costs, labor, permits, insurance, operations,
    teardown, permanence value, revenue projections, and net analysis.
    """
    design = _to_design_spec(
        elements=req.elements,
        duration_days=req.duration_days,
        activation_type=req.activation_type,
        size_sqft=req.size_sqft,
        location_score=req.location_score,
        expected_attendance=req.expected_attendance,
        event_type=req.event_type,
        parcel_type=req.parcel_type,
        permanence_score=req.permanence_score,
        equity_score=req.equity_score,
    )

    result = calculator.estimate(design)
    return result


# ---------------------------------------------------------------------------
# GET /api/cost/benchmarks
# ---------------------------------------------------------------------------

@router.get("/benchmarks")
def get_benchmarks() -> dict[str, Any]:
    """
    Return benchmark costs for different activation types.

    Includes typical size, duration, cost range, and common elements
    for each benchmark category.
    """
    benchmarks_with_estimates: list[dict[str, Any]] = []

    for bench in ACTIVATION_BENCHMARKS:
        # Build elements from the benchmark's typical elements
        elements = []
        for etype in bench["typical_elements"]:
            if etype in MATERIAL_CATALOG:
                # Use sensible default quantities based on type
                qty = _benchmark_quantity(etype, bench["typical_size_sqft"])
                elements.append(DesignElement(element_type=etype, quantity=qty))

        # Generate a quick estimate for the benchmark
        if elements:
            design = DesignSpec(
                elements=elements,
                duration_days=bench["typical_duration_days"],
                activation_type=bench["type"].replace("event_small", "event").replace("event_large", "event"),
                size_sqft=bench["typical_size_sqft"],
                location_score=0.5,
                expected_attendance=_benchmark_attendance(bench["type"]),
                event_type="community",
                parcel_type="park",
                permanence_score=0.5,
                equity_score=0.5,
            )
            est = calculator.estimate(design)
            estimated_total = est["total_cost"]
        else:
            estimated_total = (bench["cost_range"]["min"] + bench["cost_range"]["max"]) / 2.0

        benchmarks_with_estimates.append({
            **bench,
            "estimated_total": round(estimated_total, 2),
        })

    return {
        "benchmarks": benchmarks_with_estimates,
        "material_catalog": {
            key: {
                "unit_cost": val["unit_cost"],
                "category": val["category"],
                "is_permanent": val["is_permanent"],
                "complexity": val["complexity"],
            }
            for key, val in MATERIAL_CATALOG.items()
        },
    }


def _benchmark_quantity(element_type: str, size_sqft: float) -> int:
    """Return a sensible default quantity for benchmark estimation."""
    quantity_map: dict[str, int] = {
        "chair": max(10, int(size_sqft / 50)),
        "bench": max(2, int(size_sqft / 500)),
        "picnic_table": max(2, int(size_sqft / 600)),
        "tent_10x10": max(1, int(size_sqft / 1000)),
        "tent_20x20": max(1, int(size_sqft / 2000)),
        "tent_30x60": 1,
        "market_stall": max(5, int(size_sqft / 200)),
        "food_stall": max(2, int(size_sqft / 500)),
        "raised_bed": max(4, int(size_sqft / 200)),
        "planter_large": max(4, int(size_sqft / 300)),
        "planter_small": max(6, int(size_sqft / 150)),
        "fence_section_8ft": max(4, int(math.sqrt(size_sqft) * 4 / 8)),
        "trash_recycling_station": max(2, int(size_sqft / 2000)),
        "lighting_string": max(2, int(size_sqft / 500)),
        "sod_patch_100sqft": max(1, int(size_sqft / 100)),
    }
    return quantity_map.get(element_type, 1)


def _benchmark_attendance(activation_type: str) -> int:
    """Return a sensible default attendance for benchmark estimation."""
    attendance_map: dict[str, int] = {
        "block_party": 80,
        "community_garden": 30,
        "pop_up_market": 200,
        "art_installation": 50,
        "event_small": 150,
        "event_large": 1000,
        "pocket_park": 40,
        "playground": 60,
    }
    return attendance_map.get(activation_type, 100)


# ---------------------------------------------------------------------------
# POST /api/cost/budget
# ---------------------------------------------------------------------------

@router.post("/budget", response_model=BudgetResponse)
def generate_budget(req: BudgetRequest) -> dict[str, Any]:
    """
    Generate a full line-item budget from a design specification.

    Returns budget lines grouped by category, permit requirements,
    revenue projections, and net financial analysis.
    """
    design = _to_design_spec(
        elements=req.elements,
        duration_days=req.duration_days,
        activation_type=req.activation_type,
        size_sqft=req.size_sqft,
        location_score=req.location_score,
        expected_attendance=req.expected_attendance,
        event_type=req.event_type,
        parcel_type=req.parcel_type,
        permanence_score=req.permanence_score,
        equity_score=req.equity_score,
    )

    # Full estimate for totals and revenue
    est = calculator.estimate(design)

    # Detailed budget lines
    budget_lines = est["cost_breakdown"]

    # Permits detail
    permits_detail = calculator.calculate_permit_costs(design.elements)

    # Category summary
    category_totals: dict[str, float] = {}
    for line in budget_lines:
        cat = line.get("category", "Other")
        category_totals[cat] = category_totals.get(cat, 0.0) + line.get("total", 0.0)

    summary = {k: round(v, 2) for k, v in category_totals.items()}
    summary["total"] = est["total_cost"]

    return {
        "budget_lines": budget_lines,
        "total_cost": est["total_cost"],
        "revenue_projections": est["revenue_projections"],
        "net_projection": est["net_projection"],
        "permanence_value": est["permanence_value"],
        "roi_with_permanence": est["roi_with_permanence"],
        "permits_required": permits_detail["permits"],
        "summary": summary,
    }


# ---------------------------------------------------------------------------
# GET /api/cost/catalog
# ---------------------------------------------------------------------------

@router.get("/catalog")
def get_catalog() -> dict[str, Any]:
    """
    Return the full material catalog with unit costs, categories,
    and permanence information for each element type.
    """
    catalog: list[dict[str, Any]] = []
    for key, val in MATERIAL_CATALOG.items():
        catalog.append({
            "element_type": key,
            "display_name": key.replace("_", " ").title(),
            "unit_cost": val["unit_cost"],
            "category": val["category"],
            "is_permanent": val["is_permanent"],
            "permanence_value_pct": val["permanence_value_pct"],
            "complexity": val["complexity"],
            "setup_hours": val["setup_hours"],
            "teardown_hours": val["teardown_hours"],
            "permits_needed": val["permits_needed"],
        })
    return {"catalog": catalog}


