"""
SPHERES Studio — Element Library Catalog

Defines every placeable element type available in the activation design canvas.
Each element carries dimensional, cost, permit, and permanence metadata used
by the canvas renderer, the cost estimator, and the permit-check pipeline.
"""

from __future__ import annotations

from enum import Enum
from typing import List

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class ElementCategory(str, Enum):
    PERFORMANCE = "performance"
    SEATING = "seating"
    FOOD_VENDOR = "food_vendor"
    GARDENS_NATURE = "gardens_nature"
    ART = "art"
    RECREATION = "recreation"
    INFRASTRUCTURE = "infrastructure"


class ElementLayer(str, Enum):
    TEMPORARY = "temporary"
    PERMANENT = "permanent"
    INFRASTRUCTURE = "infrastructure"


class PermanenceCategory(str, Enum):
    PHYSICAL = "physical"
    COMMUNITY_ASSET = "community_asset"
    KNOWLEDGE = "knowledge"
    ECONOMIC = "economic"
    ENVIRONMENTAL = "environmental"


class PermitType(str, Enum):
    NONE = "none"
    NOISE = "noise_permit"
    FOOD = "food_vendor_permit"
    TEMPORARY_STRUCTURE = "temporary_structure_permit"
    BUILDING = "building_permit"
    ELECTRICAL = "electrical_permit"
    PLUMBING = "plumbing_permit"
    SPECIAL_EVENT = "special_event_permit"
    ENCROACHMENT = "encroachment_permit"
    LAND_USE = "land_use_permit"
    SIGN = "sign_permit"
    TREE = "tree_permit"
    GRADING = "grading_permit"


# ---------------------------------------------------------------------------
# Element definition schema
# ---------------------------------------------------------------------------

class CostRange(BaseModel):
    low: int
    high: int


class ElementDefinition(BaseModel):
    """Complete specification for a single element type in the library."""

    id: str = Field(..., description="Unique slug identifier")
    name: str = Field(..., description="Human-readable name")
    category: ElementCategory
    icon: str = Field(..., description="Lucide icon name")
    footprint_width: float = Field(..., description="Width in feet")
    footprint_height: float = Field(..., description="Height (depth) in feet")
    cost_estimate: CostRange
    permit_requirements: List[PermitType] = Field(default_factory=list)
    permanence_potential: int = Field(
        default=10,
        ge=0,
        le=100,
        description="0-100 score indicating how permanent the element is",
    )
    permanence_category: PermanenceCategory = PermanenceCategory.PHYSICAL
    layer: ElementLayer = ElementLayer.TEMPORARY
    color: str = Field(..., description="Hex colour for canvas rendering")
    description: str = Field(default="", description="Short description of the element")


# ---------------------------------------------------------------------------
# Full element library
# ---------------------------------------------------------------------------

ELEMENT_LIBRARY: List[ElementDefinition] = [
    # ── Performance ───────────────────────────────────────────────────────
    ElementDefinition(
        id="stage_small",
        name="Small Stage",
        category=ElementCategory.PERFORMANCE,
        icon="mic",
        footprint_width=10,
        footprint_height=10,
        cost_estimate=CostRange(low=500, high=2000),
        permit_requirements=[PermitType.TEMPORARY_STRUCTURE, PermitType.NOISE],
        permanence_potential=15,
        permanence_category=PermanenceCategory.COMMUNITY_ASSET,
        layer=ElementLayer.TEMPORARY,
        color="#8B5CF6",
        description="Portable stage platform for small performances and speeches",
    ),
    ElementDefinition(
        id="stage_medium",
        name="Medium Stage",
        category=ElementCategory.PERFORMANCE,
        icon="mic-2",
        footprint_width=20,
        footprint_height=15,
        cost_estimate=CostRange(low=2000, high=8000),
        permit_requirements=[PermitType.TEMPORARY_STRUCTURE, PermitType.NOISE, PermitType.ELECTRICAL],
        permanence_potential=20,
        permanence_category=PermanenceCategory.COMMUNITY_ASSET,
        layer=ElementLayer.TEMPORARY,
        color="#7C3AED",
        description="Mid-size stage with room for a band and basic lighting",
    ),
    ElementDefinition(
        id="stage_large",
        name="Large Stage",
        category=ElementCategory.PERFORMANCE,
        icon="music",
        footprint_width=30,
        footprint_height=20,
        cost_estimate=CostRange(low=5000, high=20000),
        permit_requirements=[
            PermitType.TEMPORARY_STRUCTURE,
            PermitType.NOISE,
            PermitType.ELECTRICAL,
            PermitType.SPECIAL_EVENT,
        ],
        permanence_potential=25,
        permanence_category=PermanenceCategory.COMMUNITY_ASSET,
        layer=ElementLayer.TEMPORARY,
        color="#6D28D9",
        description="Full-size concert/event stage with rigging points",
    ),
    ElementDefinition(
        id="sound_equipment",
        name="Sound Equipment",
        category=ElementCategory.PERFORMANCE,
        icon="speaker",
        footprint_width=5,
        footprint_height=5,
        cost_estimate=CostRange(low=200, high=1000),
        permit_requirements=[PermitType.NOISE],
        permanence_potential=10,
        permanence_category=PermanenceCategory.PHYSICAL,
        layer=ElementLayer.TEMPORARY,
        color="#A78BFA",
        description="PA system, speakers, and mixing board",
    ),
    ElementDefinition(
        id="screening_wall",
        name="Screening Wall",
        category=ElementCategory.PERFORMANCE,
        icon="monitor",
        footprint_width=15,
        footprint_height=8,
        cost_estimate=CostRange(low=1000, high=5000),
        permit_requirements=[PermitType.TEMPORARY_STRUCTURE, PermitType.ELECTRICAL],
        permanence_potential=20,
        permanence_category=PermanenceCategory.COMMUNITY_ASSET,
        layer=ElementLayer.TEMPORARY,
        color="#C4B5FD",
        description="Projection screen or LED wall for outdoor cinema",
    ),

    # ── Seating ───────────────────────────────────────────────────────────
    ElementDefinition(
        id="bench",
        name="Bench",
        category=ElementCategory.SEATING,
        icon="armchair",
        footprint_width=6,
        footprint_height=2,
        cost_estimate=CostRange(low=200, high=800),
        permit_requirements=[],
        permanence_potential=60,
        permanence_category=PermanenceCategory.PHYSICAL,
        layer=ElementLayer.PERMANENT,
        color="#F59E0B",
        description="Standard park bench seating two to three people",
    ),
    ElementDefinition(
        id="picnic_table",
        name="Picnic Table",
        category=ElementCategory.SEATING,
        icon="table",
        footprint_width=6,
        footprint_height=4,
        cost_estimate=CostRange(low=300, high=1200),
        permit_requirements=[],
        permanence_potential=65,
        permanence_category=PermanenceCategory.COMMUNITY_ASSET,
        layer=ElementLayer.PERMANENT,
        color="#FBBF24",
        description="Picnic table with attached bench seating",
    ),
    ElementDefinition(
        id="chair_cluster",
        name="Chair Cluster",
        category=ElementCategory.SEATING,
        icon="sofa",
        footprint_width=8,
        footprint_height=8,
        cost_estimate=CostRange(low=100, high=500),
        permit_requirements=[],
        permanence_potential=10,
        permanence_category=PermanenceCategory.PHYSICAL,
        layer=ElementLayer.TEMPORARY,
        color="#FCD34D",
        description="Movable chairs arranged in a social cluster",
    ),
    ElementDefinition(
        id="bleachers",
        name="Bleachers",
        category=ElementCategory.SEATING,
        icon="rows-3",
        footprint_width=20,
        footprint_height=8,
        cost_estimate=CostRange(low=2000, high=8000),
        permit_requirements=[PermitType.TEMPORARY_STRUCTURE],
        permanence_potential=30,
        permanence_category=PermanenceCategory.PHYSICAL,
        layer=ElementLayer.TEMPORARY,
        color="#F59E0B",
        description="Portable bleacher seating for events",
    ),
    ElementDefinition(
        id="amphitheater_seating",
        name="Amphitheater Seating",
        category=ElementCategory.SEATING,
        icon="theater",
        footprint_width=30,
        footprint_height=20,
        cost_estimate=CostRange(low=10000, high=50000),
        permit_requirements=[PermitType.BUILDING, PermitType.GRADING],
        permanence_potential=95,
        permanence_category=PermanenceCategory.COMMUNITY_ASSET,
        layer=ElementLayer.PERMANENT,
        color="#D97706",
        description="Permanent tiered seating carved into landscape",
    ),

    # ── Food & Vendor ─────────────────────────────────────────────────────
    ElementDefinition(
        id="food_cart",
        name="Food Cart",
        category=ElementCategory.FOOD_VENDOR,
        icon="shopping-cart",
        footprint_width=6,
        footprint_height=4,
        cost_estimate=CostRange(low=100, high=500),
        permit_requirements=[PermitType.FOOD],
        permanence_potential=10,
        permanence_category=PermanenceCategory.ECONOMIC,
        layer=ElementLayer.TEMPORARY,
        color="#EF4444",
        description="Mobile food cart for snacks and beverages",
    ),
    ElementDefinition(
        id="food_truck_space",
        name="Food Truck Space",
        category=ElementCategory.FOOD_VENDOR,
        icon="truck",
        footprint_width=25,
        footprint_height=10,
        cost_estimate=CostRange(low=200, high=800),
        permit_requirements=[PermitType.FOOD, PermitType.ENCROACHMENT],
        permanence_potential=10,
        permanence_category=PermanenceCategory.ECONOMIC,
        layer=ElementLayer.TEMPORARY,
        color="#DC2626",
        description="Designated parking pad for a food truck",
    ),
    ElementDefinition(
        id="market_stall",
        name="Market Stall",
        category=ElementCategory.FOOD_VENDOR,
        icon="store",
        footprint_width=10,
        footprint_height=10,
        cost_estimate=CostRange(low=300, high=1500),
        permit_requirements=[PermitType.FOOD, PermitType.TEMPORARY_STRUCTURE],
        permanence_potential=20,
        permanence_category=PermanenceCategory.ECONOMIC,
        layer=ElementLayer.TEMPORARY,
        color="#F87171",
        description="Covered stall for farmers market or craft fair",
    ),
    ElementDefinition(
        id="vendor_tent",
        name="Vendor Tent",
        category=ElementCategory.FOOD_VENDOR,
        icon="tent",
        footprint_width=10,
        footprint_height=10,
        cost_estimate=CostRange(low=200, high=1000),
        permit_requirements=[PermitType.TEMPORARY_STRUCTURE],
        permanence_potential=10,
        permanence_category=PermanenceCategory.ECONOMIC,
        layer=ElementLayer.TEMPORARY,
        color="#FCA5A5",
        description="Pop-up tent for vendor or information booth",
    ),

    # ── Gardens & Nature ──────────────────────────────────────────────────
    ElementDefinition(
        id="raised_bed",
        name="Raised Bed",
        category=ElementCategory.GARDENS_NATURE,
        icon="sprout",
        footprint_width=8,
        footprint_height=4,
        cost_estimate=CostRange(low=200, high=1000),
        permit_requirements=[],
        permanence_potential=90,
        permanence_category=PermanenceCategory.ENVIRONMENTAL,
        layer=ElementLayer.PERMANENT,
        color="#22C55E",
        description="Raised garden bed for vegetables, herbs, or flowers",
    ),
    ElementDefinition(
        id="tree_planting",
        name="Tree Planting",
        category=ElementCategory.GARDENS_NATURE,
        icon="tree-pine",
        footprint_width=8,
        footprint_height=8,
        cost_estimate=CostRange(low=500, high=2000),
        permit_requirements=[PermitType.TREE],
        permanence_potential=95,
        permanence_category=PermanenceCategory.ENVIRONMENTAL,
        layer=ElementLayer.PERMANENT,
        color="#16A34A",
        description="New tree planting with root ball and mulch ring",
    ),
    ElementDefinition(
        id="flower_garden",
        name="Flower Garden",
        category=ElementCategory.GARDENS_NATURE,
        icon="flower-2",
        footprint_width=10,
        footprint_height=10,
        cost_estimate=CostRange(low=300, high=1500),
        permit_requirements=[],
        permanence_potential=80,
        permanence_category=PermanenceCategory.ENVIRONMENTAL,
        layer=ElementLayer.PERMANENT,
        color="#4ADE80",
        description="Ornamental flower garden with seasonal plantings",
    ),
    ElementDefinition(
        id="native_meadow",
        name="Native Meadow",
        category=ElementCategory.GARDENS_NATURE,
        icon="leaf",
        footprint_width=20,
        footprint_height=20,
        cost_estimate=CostRange(low=500, high=3000),
        permit_requirements=[],
        permanence_potential=95,
        permanence_category=PermanenceCategory.ENVIRONMENTAL,
        layer=ElementLayer.PERMANENT,
        color="#15803D",
        description="Native wildflower and grass meadow for pollinators",
    ),
    ElementDefinition(
        id="water_feature",
        name="Water Feature",
        category=ElementCategory.GARDENS_NATURE,
        icon="droplets",
        footprint_width=10,
        footprint_height=10,
        cost_estimate=CostRange(low=2000, high=10000),
        permit_requirements=[PermitType.PLUMBING, PermitType.BUILDING],
        permanence_potential=85,
        permanence_category=PermanenceCategory.ENVIRONMENTAL,
        layer=ElementLayer.PERMANENT,
        color="#06B6D4",
        description="Fountain, splash pad, or rain garden water feature",
    ),

    # ── Art ────────────────────────────────────────────────────────────────
    ElementDefinition(
        id="mural_wall",
        name="Mural Wall",
        category=ElementCategory.ART,
        icon="paintbrush",
        footprint_width=20,
        footprint_height=10,
        cost_estimate=CostRange(low=1000, high=5000),
        permit_requirements=[PermitType.SIGN],
        permanence_potential=90,
        permanence_category=PermanenceCategory.COMMUNITY_ASSET,
        layer=ElementLayer.PERMANENT,
        color="#EC4899",
        description="Wall surface prepared for community mural painting",
    ),
    ElementDefinition(
        id="sculpture_pad",
        name="Sculpture Pad",
        category=ElementCategory.ART,
        icon="hexagon",
        footprint_width=8,
        footprint_height=8,
        cost_estimate=CostRange(low=500, high=3000),
        permit_requirements=[],
        permanence_potential=50,
        permanence_category=PermanenceCategory.COMMUNITY_ASSET,
        layer=ElementLayer.TEMPORARY,
        color="#F472B6",
        description="Concrete pad for rotating sculpture installations",
    ),
    ElementDefinition(
        id="interactive_art",
        name="Interactive Art",
        category=ElementCategory.ART,
        icon="hand",
        footprint_width=12,
        footprint_height=12,
        cost_estimate=CostRange(low=1000, high=8000),
        permit_requirements=[PermitType.ELECTRICAL],
        permanence_potential=40,
        permanence_category=PermanenceCategory.COMMUNITY_ASSET,
        layer=ElementLayer.TEMPORARY,
        color="#DB2777",
        description="Hands-on art installation that responds to visitors",
    ),
    ElementDefinition(
        id="art_installation",
        name="Art Installation",
        category=ElementCategory.ART,
        icon="palette",
        footprint_width=15,
        footprint_height=15,
        cost_estimate=CostRange(low=2000, high=15000),
        permit_requirements=[PermitType.TEMPORARY_STRUCTURE],
        permanence_potential=35,
        permanence_category=PermanenceCategory.COMMUNITY_ASSET,
        layer=ElementLayer.TEMPORARY,
        color="#BE185D",
        description="Large-scale temporary art installation",
    ),

    # ── Recreation ────────────────────────────────────────────────────────
    ElementDefinition(
        id="play_structure",
        name="Play Structure",
        category=ElementCategory.RECREATION,
        icon="baby",
        footprint_width=20,
        footprint_height=20,
        cost_estimate=CostRange(low=5000, high=25000),
        permit_requirements=[PermitType.BUILDING],
        permanence_potential=90,
        permanence_category=PermanenceCategory.COMMUNITY_ASSET,
        layer=ElementLayer.PERMANENT,
        color="#3B82F6",
        description="Playground equipment with safety surfacing",
    ),
    ElementDefinition(
        id="basketball_half",
        name="Basketball Half Court",
        category=ElementCategory.RECREATION,
        icon="circle-dot",
        footprint_width=30,
        footprint_height=25,
        cost_estimate=CostRange(low=3000, high=15000),
        permit_requirements=[PermitType.BUILDING, PermitType.GRADING],
        permanence_potential=85,
        permanence_category=PermanenceCategory.COMMUNITY_ASSET,
        layer=ElementLayer.PERMANENT,
        color="#2563EB",
        description="Half basketball court with hoop and painted lines",
    ),
    ElementDefinition(
        id="fitness_station",
        name="Fitness Station",
        category=ElementCategory.RECREATION,
        icon="dumbbell",
        footprint_width=10,
        footprint_height=10,
        cost_estimate=CostRange(low=2000, high=8000),
        permit_requirements=[PermitType.BUILDING],
        permanence_potential=90,
        permanence_category=PermanenceCategory.COMMUNITY_ASSET,
        layer=ElementLayer.PERMANENT,
        color="#1D4ED8",
        description="Outdoor fitness equipment station",
    ),
    ElementDefinition(
        id="sports_field",
        name="Sports Field",
        category=ElementCategory.RECREATION,
        icon="trophy",
        footprint_width=60,
        footprint_height=30,
        cost_estimate=CostRange(low=5000, high=20000),
        permit_requirements=[PermitType.GRADING, PermitType.LAND_USE],
        permanence_potential=70,
        permanence_category=PermanenceCategory.COMMUNITY_ASSET,
        layer=ElementLayer.PERMANENT,
        color="#1E40AF",
        description="Multi-purpose sports field with level turf",
    ),

    # ── Infrastructure ────────────────────────────────────────────────────
    ElementDefinition(
        id="pathway",
        name="Pathway",
        category=ElementCategory.INFRASTRUCTURE,
        icon="route",
        footprint_width=20,
        footprint_height=4,
        cost_estimate=CostRange(low=500, high=3000),
        permit_requirements=[PermitType.GRADING],
        permanence_potential=95,
        permanence_category=PermanenceCategory.PHYSICAL,
        layer=ElementLayer.INFRASTRUCTURE,
        color="#6B7280",
        description="Paved or gravel walking path",
    ),
    ElementDefinition(
        id="fencing",
        name="Fencing",
        category=ElementCategory.INFRASTRUCTURE,
        icon="fence",
        footprint_width=20,
        footprint_height=1,
        cost_estimate=CostRange(low=300, high=1500),
        permit_requirements=[PermitType.BUILDING],
        permanence_potential=70,
        permanence_category=PermanenceCategory.PHYSICAL,
        layer=ElementLayer.INFRASTRUCTURE,
        color="#9CA3AF",
        description="Perimeter or decorative fencing",
    ),
    ElementDefinition(
        id="lighting_pole",
        name="Lighting Pole",
        category=ElementCategory.INFRASTRUCTURE,
        icon="lamp",
        footprint_width=3,
        footprint_height=3,
        cost_estimate=CostRange(low=500, high=2000),
        permit_requirements=[PermitType.ELECTRICAL],
        permanence_potential=90,
        permanence_category=PermanenceCategory.PHYSICAL,
        layer=ElementLayer.INFRASTRUCTURE,
        color="#D1D5DB",
        description="Street or pathway lighting pole",
    ),
    ElementDefinition(
        id="power_hookup",
        name="Power Hookup",
        category=ElementCategory.INFRASTRUCTURE,
        icon="plug",
        footprint_width=3,
        footprint_height=3,
        cost_estimate=CostRange(low=500, high=2000),
        permit_requirements=[PermitType.ELECTRICAL],
        permanence_potential=80,
        permanence_category=PermanenceCategory.PHYSICAL,
        layer=ElementLayer.INFRASTRUCTURE,
        color="#E5E7EB",
        description="Electrical junction box for temporary power",
    ),
    ElementDefinition(
        id="water_hookup",
        name="Water Hookup",
        category=ElementCategory.INFRASTRUCTURE,
        icon="droplet",
        footprint_width=3,
        footprint_height=3,
        cost_estimate=CostRange(low=800, high=3000),
        permit_requirements=[PermitType.PLUMBING],
        permanence_potential=85,
        permanence_category=PermanenceCategory.PHYSICAL,
        layer=ElementLayer.INFRASTRUCTURE,
        color="#93C5FD",
        description="Water supply connection point",
    ),
    ElementDefinition(
        id="shade_structure",
        name="Shade Structure",
        category=ElementCategory.INFRASTRUCTURE,
        icon="umbrella",
        footprint_width=15,
        footprint_height=15,
        cost_estimate=CostRange(low=2000, high=8000),
        permit_requirements=[PermitType.TEMPORARY_STRUCTURE],
        permanence_potential=50,
        permanence_category=PermanenceCategory.PHYSICAL,
        layer=ElementLayer.INFRASTRUCTURE,
        color="#A3A3A3",
        description="Canopy, pergola, or sail shade structure",
    ),
    ElementDefinition(
        id="signage",
        name="Signage",
        category=ElementCategory.INFRASTRUCTURE,
        icon="sign-post",
        footprint_width=4,
        footprint_height=2,
        cost_estimate=CostRange(low=200, high=1000),
        permit_requirements=[PermitType.SIGN],
        permanence_potential=85,
        permanence_category=PermanenceCategory.KNOWLEDGE,
        layer=ElementLayer.INFRASTRUCTURE,
        color="#78716C",
        description="Wayfinding, informational, or regulatory signage",
    ),
]


def get_element_by_id(element_id: str) -> ElementDefinition | None:
    """Look up a single element definition by its slug id."""
    for el in ELEMENT_LIBRARY:
        return next((e for e in ELEMENT_LIBRARY if e.id == element_id), None)
    return None


def get_elements_by_category(category: ElementCategory) -> List[ElementDefinition]:
    """Return all elements belonging to a category."""
    return [e for e in ELEMENT_LIBRARY if e.category == category]


def get_element_map() -> dict[str, ElementDefinition]:
    """Return a dict mapping element id -> definition for fast lookup."""
    return {e.id: e for e in ELEMENT_LIBRARY}
