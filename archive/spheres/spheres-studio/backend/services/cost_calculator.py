"""
SPHERES Studio — Cost Calculation Engine
==========================================
Production-grade cost estimation for public space activations in Philadelphia.

Calculates material costs, labor, permits, insurance, operations, teardown,
permanence value, and revenue projections. References spheres-legal permit
fee schedules for Philadelphia-specific pricing.

All dollar amounts are USD. All durations are in days unless noted.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any, Optional


# ---------------------------------------------------------------------------
# Philadelphia permit fee schedule (from spheres-legal)
# Keys are permit category tags assigned to design elements.
# Values are (min_fee, max_fee) tuples.
# ---------------------------------------------------------------------------

PERMIT_FEE_SCHEDULE: dict[str, tuple[float, float]] = {
    "special_event":       (150.0,  500.0),
    "food_vending":        (100.0,  300.0),
    "temporary_structure": (200.0,  750.0),
    "public_art":          (50.0,   200.0),
    "park_use":            (100.0,  1000.0),
    "block_party":         (25.0,   100.0),
    "noise_variance":      (50.0,   200.0),
    "street_closure":      (200.0,  500.0),
    "encroachment":        (150.0,  400.0),
    "film":                (200.0,  1000.0),
}


# ---------------------------------------------------------------------------
# Material cost catalog — base unit costs for common activation elements
# ---------------------------------------------------------------------------

MATERIAL_CATALOG: dict[str, dict[str, Any]] = {
    # Seating
    "bench": {
        "unit_cost": 350.0,
        "setup_hours": 0.5,
        "teardown_hours": 0.25,
        "complexity": 1,
        "permits_needed": [],
        "is_permanent": True,
        "permanence_value_pct": 0.85,
        "category": "seating",
    },
    "chair": {
        "unit_cost": 45.0,
        "setup_hours": 0.1,
        "teardown_hours": 0.05,
        "complexity": 1,
        "permits_needed": [],
        "is_permanent": False,
        "permanence_value_pct": 0.0,
        "category": "seating",
    },
    "picnic_table": {
        "unit_cost": 600.0,
        "setup_hours": 1.0,
        "teardown_hours": 0.5,
        "complexity": 2,
        "permits_needed": [],
        "is_permanent": True,
        "permanence_value_pct": 0.80,
        "category": "seating",
    },
    "adirondack_chair": {
        "unit_cost": 250.0,
        "setup_hours": 0.25,
        "teardown_hours": 0.15,
        "complexity": 1,
        "permits_needed": [],
        "is_permanent": True,
        "permanence_value_pct": 0.70,
        "category": "seating",
    },
    "bleachers": {
        "unit_cost": 2500.0,
        "setup_hours": 4.0,
        "teardown_hours": 3.0,
        "complexity": 4,
        "permits_needed": ["temporary_structure"],
        "is_permanent": False,
        "permanence_value_pct": 0.0,
        "category": "seating",
    },

    # Structures
    "stage": {
        "unit_cost": 3500.0,
        "setup_hours": 8.0,
        "teardown_hours": 6.0,
        "complexity": 5,
        "permits_needed": ["temporary_structure", "noise_variance"],
        "is_permanent": False,
        "permanence_value_pct": 0.0,
        "category": "structure",
    },
    "tent_10x10": {
        "unit_cost": 250.0,
        "setup_hours": 1.0,
        "teardown_hours": 0.75,
        "complexity": 2,
        "permits_needed": [],
        "is_permanent": False,
        "permanence_value_pct": 0.0,
        "category": "structure",
    },
    "tent_20x20": {
        "unit_cost": 800.0,
        "setup_hours": 2.5,
        "teardown_hours": 2.0,
        "complexity": 3,
        "permits_needed": ["temporary_structure"],
        "is_permanent": False,
        "permanence_value_pct": 0.0,
        "category": "structure",
    },
    "tent_30x60": {
        "unit_cost": 3000.0,
        "setup_hours": 6.0,
        "teardown_hours": 4.0,
        "complexity": 4,
        "permits_needed": ["temporary_structure"],
        "is_permanent": False,
        "permanence_value_pct": 0.0,
        "category": "structure",
    },
    "pergola": {
        "unit_cost": 4500.0,
        "setup_hours": 12.0,
        "teardown_hours": 8.0,
        "complexity": 5,
        "permits_needed": ["temporary_structure"],
        "is_permanent": True,
        "permanence_value_pct": 0.90,
        "category": "structure",
    },
    "shade_sail": {
        "unit_cost": 1200.0,
        "setup_hours": 3.0,
        "teardown_hours": 2.0,
        "complexity": 3,
        "permits_needed": [],
        "is_permanent": True,
        "permanence_value_pct": 0.75,
        "category": "structure",
    },
    "shipping_container": {
        "unit_cost": 4000.0,
        "setup_hours": 8.0,
        "teardown_hours": 6.0,
        "complexity": 5,
        "permits_needed": ["temporary_structure", "encroachment"],
        "is_permanent": True,
        "permanence_value_pct": 0.85,
        "category": "structure",
    },
    "gazebo": {
        "unit_cost": 5500.0,
        "setup_hours": 16.0,
        "teardown_hours": 10.0,
        "complexity": 5,
        "permits_needed": ["temporary_structure"],
        "is_permanent": True,
        "permanence_value_pct": 0.90,
        "category": "structure",
    },

    # Greenery / gardens
    "raised_bed": {
        "unit_cost": 180.0,
        "setup_hours": 2.0,
        "teardown_hours": 1.0,
        "complexity": 2,
        "permits_needed": [],
        "is_permanent": True,
        "permanence_value_pct": 0.80,
        "category": "greenery",
    },
    "planter_large": {
        "unit_cost": 120.0,
        "setup_hours": 0.5,
        "teardown_hours": 0.25,
        "complexity": 1,
        "permits_needed": [],
        "is_permanent": True,
        "permanence_value_pct": 0.70,
        "category": "greenery",
    },
    "planter_small": {
        "unit_cost": 45.0,
        "setup_hours": 0.25,
        "teardown_hours": 0.1,
        "complexity": 1,
        "permits_needed": [],
        "is_permanent": True,
        "permanence_value_pct": 0.60,
        "category": "greenery",
    },
    "tree": {
        "unit_cost": 350.0,
        "setup_hours": 3.0,
        "teardown_hours": 0.0,
        "complexity": 3,
        "permits_needed": [],
        "is_permanent": True,
        "permanence_value_pct": 1.0,
        "category": "greenery",
    },
    "sod_patch_100sqft": {
        "unit_cost": 80.0,
        "setup_hours": 1.5,
        "teardown_hours": 0.0,
        "complexity": 2,
        "permits_needed": [],
        "is_permanent": True,
        "permanence_value_pct": 0.90,
        "category": "greenery",
    },
    "rain_garden": {
        "unit_cost": 1500.0,
        "setup_hours": 8.0,
        "teardown_hours": 0.0,
        "complexity": 4,
        "permits_needed": [],
        "is_permanent": True,
        "permanence_value_pct": 1.0,
        "category": "greenery",
    },

    # Art
    "mural_wall": {
        "unit_cost": 2000.0,
        "setup_hours": 24.0,
        "teardown_hours": 0.0,
        "complexity": 4,
        "permits_needed": ["public_art"],
        "is_permanent": True,
        "permanence_value_pct": 1.0,
        "category": "art",
    },
    "sculpture_small": {
        "unit_cost": 1500.0,
        "setup_hours": 4.0,
        "teardown_hours": 2.0,
        "complexity": 3,
        "permits_needed": ["public_art"],
        "is_permanent": True,
        "permanence_value_pct": 0.90,
        "category": "art",
    },
    "sculpture_large": {
        "unit_cost": 8000.0,
        "setup_hours": 12.0,
        "teardown_hours": 8.0,
        "complexity": 5,
        "permits_needed": ["public_art", "temporary_structure"],
        "is_permanent": True,
        "permanence_value_pct": 0.90,
        "category": "art",
    },
    "light_installation": {
        "unit_cost": 3000.0,
        "setup_hours": 8.0,
        "teardown_hours": 4.0,
        "complexity": 4,
        "permits_needed": ["public_art"],
        "is_permanent": True,
        "permanence_value_pct": 0.75,
        "category": "art",
    },
    "interactive_display": {
        "unit_cost": 5000.0,
        "setup_hours": 12.0,
        "teardown_hours": 6.0,
        "complexity": 5,
        "permits_needed": ["public_art"],
        "is_permanent": False,
        "permanence_value_pct": 0.0,
        "category": "art",
    },

    # Food / vending
    "food_stall": {
        "unit_cost": 400.0,
        "setup_hours": 2.0,
        "teardown_hours": 1.5,
        "complexity": 2,
        "permits_needed": ["food_vending"],
        "is_permanent": False,
        "permanence_value_pct": 0.0,
        "category": "food",
    },
    "food_truck_pad": {
        "unit_cost": 200.0,
        "setup_hours": 1.0,
        "teardown_hours": 0.5,
        "complexity": 1,
        "permits_needed": ["food_vending"],
        "is_permanent": False,
        "permanence_value_pct": 0.0,
        "category": "food",
    },
    "market_stall": {
        "unit_cost": 300.0,
        "setup_hours": 1.5,
        "teardown_hours": 1.0,
        "complexity": 2,
        "permits_needed": [],
        "is_permanent": False,
        "permanence_value_pct": 0.0,
        "category": "food",
    },
    "community_kitchen": {
        "unit_cost": 12000.0,
        "setup_hours": 40.0,
        "teardown_hours": 20.0,
        "complexity": 5,
        "permits_needed": ["food_vending", "temporary_structure"],
        "is_permanent": True,
        "permanence_value_pct": 0.85,
        "category": "food",
    },

    # Infrastructure
    "lighting_string": {
        "unit_cost": 120.0,
        "setup_hours": 1.0,
        "teardown_hours": 0.5,
        "complexity": 2,
        "permits_needed": [],
        "is_permanent": True,
        "permanence_value_pct": 0.60,
        "category": "infrastructure",
    },
    "lighting_pole": {
        "unit_cost": 800.0,
        "setup_hours": 3.0,
        "teardown_hours": 2.0,
        "complexity": 3,
        "permits_needed": [],
        "is_permanent": True,
        "permanence_value_pct": 0.90,
        "category": "infrastructure",
    },
    "power_distribution": {
        "unit_cost": 600.0,
        "setup_hours": 4.0,
        "teardown_hours": 2.0,
        "complexity": 3,
        "permits_needed": [],
        "is_permanent": False,
        "permanence_value_pct": 0.0,
        "category": "infrastructure",
    },
    "water_station": {
        "unit_cost": 500.0,
        "setup_hours": 3.0,
        "teardown_hours": 2.0,
        "complexity": 3,
        "permits_needed": [],
        "is_permanent": True,
        "permanence_value_pct": 0.80,
        "category": "infrastructure",
    },
    "bike_rack": {
        "unit_cost": 300.0,
        "setup_hours": 1.5,
        "teardown_hours": 1.0,
        "complexity": 2,
        "permits_needed": ["encroachment"],
        "is_permanent": True,
        "permanence_value_pct": 0.90,
        "category": "infrastructure",
    },
    "trash_recycling_station": {
        "unit_cost": 200.0,
        "setup_hours": 0.5,
        "teardown_hours": 0.25,
        "complexity": 1,
        "permits_needed": [],
        "is_permanent": True,
        "permanence_value_pct": 0.80,
        "category": "infrastructure",
    },
    "signage": {
        "unit_cost": 150.0,
        "setup_hours": 1.0,
        "teardown_hours": 0.5,
        "complexity": 1,
        "permits_needed": [],
        "is_permanent": True,
        "permanence_value_pct": 0.70,
        "category": "infrastructure",
    },
    "wayfinding_kiosk": {
        "unit_cost": 2500.0,
        "setup_hours": 4.0,
        "teardown_hours": 2.0,
        "complexity": 3,
        "permits_needed": ["encroachment"],
        "is_permanent": True,
        "permanence_value_pct": 0.85,
        "category": "infrastructure",
    },

    # Play / recreation
    "playground_element": {
        "unit_cost": 5000.0,
        "setup_hours": 16.0,
        "teardown_hours": 8.0,
        "complexity": 5,
        "permits_needed": ["temporary_structure"],
        "is_permanent": True,
        "permanence_value_pct": 0.90,
        "category": "play",
    },
    "sport_court_marking": {
        "unit_cost": 600.0,
        "setup_hours": 4.0,
        "teardown_hours": 0.0,
        "complexity": 2,
        "permits_needed": [],
        "is_permanent": True,
        "permanence_value_pct": 0.70,
        "category": "play",
    },
    "splash_pad": {
        "unit_cost": 15000.0,
        "setup_hours": 40.0,
        "teardown_hours": 0.0,
        "complexity": 5,
        "permits_needed": ["temporary_structure"],
        "is_permanent": True,
        "permanence_value_pct": 0.95,
        "category": "play",
    },

    # Surfaces / paving
    "paver_patio_100sqft": {
        "unit_cost": 1200.0,
        "setup_hours": 8.0,
        "teardown_hours": 0.0,
        "complexity": 3,
        "permits_needed": [],
        "is_permanent": True,
        "permanence_value_pct": 0.95,
        "category": "surface",
    },
    "gravel_path_50ft": {
        "unit_cost": 400.0,
        "setup_hours": 4.0,
        "teardown_hours": 0.0,
        "complexity": 2,
        "permits_needed": [],
        "is_permanent": True,
        "permanence_value_pct": 0.80,
        "category": "surface",
    },
    "temporary_flooring_100sqft": {
        "unit_cost": 350.0,
        "setup_hours": 2.0,
        "teardown_hours": 1.5,
        "complexity": 2,
        "permits_needed": [],
        "is_permanent": False,
        "permanence_value_pct": 0.0,
        "category": "surface",
    },

    # Sound / AV
    "pa_system": {
        "unit_cost": 800.0,
        "setup_hours": 2.0,
        "teardown_hours": 1.0,
        "complexity": 3,
        "permits_needed": ["noise_variance"],
        "is_permanent": False,
        "permanence_value_pct": 0.0,
        "category": "sound",
    },
    "speaker_permanent": {
        "unit_cost": 1200.0,
        "setup_hours": 4.0,
        "teardown_hours": 2.0,
        "complexity": 3,
        "permits_needed": ["noise_variance"],
        "is_permanent": True,
        "permanence_value_pct": 0.75,
        "category": "sound",
    },
    "projector_screen": {
        "unit_cost": 600.0,
        "setup_hours": 2.0,
        "teardown_hours": 1.0,
        "complexity": 2,
        "permits_needed": [],
        "is_permanent": False,
        "permanence_value_pct": 0.0,
        "category": "sound",
    },

    # Fencing / barriers
    "fence_section_8ft": {
        "unit_cost": 85.0,
        "setup_hours": 0.5,
        "teardown_hours": 0.25,
        "complexity": 1,
        "permits_needed": [],
        "is_permanent": False,
        "permanence_value_pct": 0.0,
        "category": "barrier",
    },
    "bollard": {
        "unit_cost": 250.0,
        "setup_hours": 1.5,
        "teardown_hours": 1.0,
        "complexity": 2,
        "permits_needed": ["encroachment"],
        "is_permanent": True,
        "permanence_value_pct": 0.90,
        "category": "barrier",
    },
    "jersey_barrier": {
        "unit_cost": 150.0,
        "setup_hours": 0.5,
        "teardown_hours": 0.5,
        "complexity": 2,
        "permits_needed": ["street_closure"],
        "is_permanent": False,
        "permanence_value_pct": 0.0,
        "category": "barrier",
    },
}


# ---------------------------------------------------------------------------
# Data structures for element input
# ---------------------------------------------------------------------------

@dataclass
class DesignElement:
    """A single element placed on the design canvas."""
    element_type: str
    quantity: int = 1
    custom_unit_cost: Optional[float] = None
    custom_name: Optional[str] = None

    @property
    def catalog_entry(self) -> dict[str, Any]:
        return MATERIAL_CATALOG.get(self.element_type, {})

    @property
    def display_name(self) -> str:
        if self.custom_name:
            return self.custom_name
        return self.element_type.replace("_", " ").title()


@dataclass
class DesignSpec:
    """Complete design specification for cost estimation."""
    elements: list[DesignElement] = field(default_factory=list)
    duration_days: int = 1
    activation_type: str = "event"
    size_sqft: float = 1000.0
    location_score: float = 0.5  # 0-1 scale, 1 = prime location
    expected_attendance: int = 100
    event_type: str = "community"  # community, commercial, nonprofit
    parcel_type: str = "park"
    permanence_score: float = 0.5  # 0-1 scale, how permanent is the design
    equity_score: float = 0.5  # 0-1 scale, equity priority of the location


# ---------------------------------------------------------------------------
# Bulk discount tiers
# ---------------------------------------------------------------------------

def _bulk_discount(quantity: int) -> float:
    """Return the discount multiplier for a given quantity of the same item."""
    if quantity >= 20:
        return 0.75  # 25% off at 20+
    if quantity >= 10:
        return 0.85  # 15% off at 10+
    if quantity >= 5:
        return 0.92  # 8% off at 5+
    return 1.0  # no discount


# ---------------------------------------------------------------------------
# Labor rate constants (Philadelphia prevailing-wage aware)
# ---------------------------------------------------------------------------

LABOR_RATE_PER_HOUR: float = 45.0  # General labor
SKILLED_LABOR_RATE_PER_HOUR: float = 75.0  # Electrician, plumber, welder
CREW_MINIMUM_HOURS: float = 4.0  # Minimum call for a crew

# Complexity-to-labor-rate mapping
# Complexity 1-2 = general labor, 3-5 = skilled labor required
COMPLEXITY_THRESHOLD_SKILLED: int = 3


# ---------------------------------------------------------------------------
# CostCalculator — the core engine
# ---------------------------------------------------------------------------

class CostCalculator:
    """
    Comprehensive cost estimation engine for public space activations.

    All methods are stateless and can be called independently or composed
    through the top-level `estimate` method.
    """

    # -----------------------------------------------------------------------
    # Element / Material costs
    # -----------------------------------------------------------------------

    def calculate_element_costs(
        self,
        elements: list[DesignElement],
    ) -> dict[str, Any]:
        """
        Calculate total material cost for all design elements with
        bulk-discount scaling for quantities of 5+, 10+, and 20+.

        Returns
        -------
        dict with keys: total, line_items (list of per-element breakdowns)
        """
        total: float = 0.0
        line_items: list[dict[str, Any]] = []

        # Group by type for bulk pricing
        type_counts: dict[str, int] = {}
        for el in elements:
            type_counts[el.element_type] = (
                type_counts.get(el.element_type, 0) + el.quantity
            )

        for el in elements:
            catalog = el.catalog_entry
            if not catalog:
                # Unknown element — use custom cost or skip
                unit_cost = el.custom_unit_cost or 0.0
                item_total = unit_cost * el.quantity
                total += item_total
                line_items.append({
                    "category": "custom",
                    "item": el.display_name,
                    "quantity": el.quantity,
                    "unit_cost": unit_cost,
                    "discount": 0.0,
                    "total": round(item_total, 2),
                })
                continue

            base_cost = el.custom_unit_cost if el.custom_unit_cost is not None else catalog["unit_cost"]
            combined_qty = type_counts.get(el.element_type, el.quantity)
            discount_mult = _bulk_discount(combined_qty)
            discounted_cost = base_cost * discount_mult
            item_total = discounted_cost * el.quantity

            total += item_total
            line_items.append({
                "category": catalog.get("category", "general"),
                "item": el.display_name,
                "quantity": el.quantity,
                "unit_cost": round(discounted_cost, 2),
                "discount": round((1.0 - discount_mult) * 100, 1),
                "total": round(item_total, 2),
            })

        return {"total": round(total, 2), "line_items": line_items}

    # -----------------------------------------------------------------------
    # Labor costs
    # -----------------------------------------------------------------------

    def calculate_labor_costs(
        self,
        elements: list[DesignElement],
        duration_days: int,
    ) -> dict[str, Any]:
        """
        Estimate labor costs based on element complexity, setup time,
        and teardown time. Applies minimum call rules.

        Returns
        -------
        dict with keys: setup_cost, daily_cost, teardown_cost, total, line_items
        """
        setup_hours: float = 0.0
        teardown_hours: float = 0.0
        skilled_setup_hours: float = 0.0
        skilled_teardown_hours: float = 0.0
        line_items: list[dict[str, Any]] = []

        for el in elements:
            catalog = el.catalog_entry
            if not catalog:
                continue

            complexity = catalog.get("complexity", 1)
            el_setup = catalog.get("setup_hours", 0.0) * el.quantity
            el_teardown = catalog.get("teardown_hours", 0.0) * el.quantity

            if complexity >= COMPLEXITY_THRESHOLD_SKILLED:
                skilled_setup_hours += el_setup
                skilled_teardown_hours += el_teardown
            else:
                setup_hours += el_setup
                teardown_hours += el_teardown

        # Apply minimum call
        if setup_hours > 0 and setup_hours < CREW_MINIMUM_HOURS:
            setup_hours = CREW_MINIMUM_HOURS
        if teardown_hours > 0 and teardown_hours < CREW_MINIMUM_HOURS:
            teardown_hours = CREW_MINIMUM_HOURS
        if skilled_setup_hours > 0 and skilled_setup_hours < CREW_MINIMUM_HOURS:
            skilled_setup_hours = CREW_MINIMUM_HOURS
        if skilled_teardown_hours > 0 and skilled_teardown_hours < CREW_MINIMUM_HOURS:
            skilled_teardown_hours = CREW_MINIMUM_HOURS

        setup_cost = (
            setup_hours * LABOR_RATE_PER_HOUR
            + skilled_setup_hours * SKILLED_LABOR_RATE_PER_HOUR
        )
        teardown_cost = (
            teardown_hours * LABOR_RATE_PER_HOUR
            + skilled_teardown_hours * SKILLED_LABOR_RATE_PER_HOUR
        )

        # Daily operations staffing: 1 general laborer per 8 hours for
        # maintenance during the activation
        daily_staff_count = max(1, math.ceil(len(elements) / 10))
        daily_cost = daily_staff_count * 8 * LABOR_RATE_PER_HOUR * duration_days

        if setup_hours > 0 or skilled_setup_hours > 0:
            line_items.append({
                "category": "labor",
                "item": "General labor — setup",
                "quantity": 1,
                "unit_cost": round(setup_hours * LABOR_RATE_PER_HOUR, 2),
                "total": round(setup_hours * LABOR_RATE_PER_HOUR, 2),
            })
        if skilled_setup_hours > 0:
            line_items.append({
                "category": "labor",
                "item": "Skilled labor — setup",
                "quantity": 1,
                "unit_cost": round(skilled_setup_hours * SKILLED_LABOR_RATE_PER_HOUR, 2),
                "total": round(skilled_setup_hours * SKILLED_LABOR_RATE_PER_HOUR, 2),
            })
        if daily_cost > 0:
            line_items.append({
                "category": "labor",
                "item": f"Daily operations staff ({daily_staff_count} crew x {duration_days} days)",
                "quantity": duration_days,
                "unit_cost": round(daily_staff_count * 8 * LABOR_RATE_PER_HOUR, 2),
                "total": round(daily_cost, 2),
            })
        if teardown_hours > 0 or skilled_teardown_hours > 0:
            line_items.append({
                "category": "labor",
                "item": "General labor — teardown",
                "quantity": 1,
                "unit_cost": round(teardown_hours * LABOR_RATE_PER_HOUR, 2),
                "total": round(teardown_hours * LABOR_RATE_PER_HOUR, 2),
            })
        if skilled_teardown_hours > 0:
            line_items.append({
                "category": "labor",
                "item": "Skilled labor — teardown",
                "quantity": 1,
                "unit_cost": round(skilled_teardown_hours * SKILLED_LABOR_RATE_PER_HOUR, 2),
                "total": round(skilled_teardown_hours * SKILLED_LABOR_RATE_PER_HOUR, 2),
            })

        total = setup_cost + daily_cost + teardown_cost
        return {
            "setup_cost": round(setup_cost, 2),
            "daily_cost": round(daily_cost, 2),
            "teardown_cost": round(teardown_cost, 2),
            "total": round(total, 2),
            "line_items": line_items,
        }

    # -----------------------------------------------------------------------
    # Permit costs
    # -----------------------------------------------------------------------

    def calculate_permit_costs(
        self,
        elements: list[DesignElement],
    ) -> dict[str, Any]:
        """
        Aggregate unique permits needed across all elements and sum
        application fees using the Philadelphia fee schedule midpoints.

        Returns
        -------
        dict with keys: total, permits (list of permit dicts)
        """
        needed_permits: set[str] = set()
        for el in elements:
            catalog = el.catalog_entry
            if catalog:
                for p in catalog.get("permits_needed", []):
                    needed_permits.add(p)

        permits_list: list[dict[str, Any]] = []
        total: float = 0.0

        for permit_key in sorted(needed_permits):
            fee_range = PERMIT_FEE_SCHEDULE.get(permit_key)
            if fee_range:
                min_fee, max_fee = fee_range
                # Use midpoint as the estimate
                estimated_fee = (min_fee + max_fee) / 2.0
                permits_list.append({
                    "permit": permit_key.replace("_", " ").title(),
                    "permit_key": permit_key,
                    "fee_min": min_fee,
                    "fee_max": max_fee,
                    "estimated_fee": round(estimated_fee, 2),
                })
                total += estimated_fee

        return {"total": round(total, 2), "permits": permits_list}

    # -----------------------------------------------------------------------
    # Insurance
    # -----------------------------------------------------------------------

    def calculate_insurance(
        self,
        total_value: float,
        event_type: str,
        expected_attendance: int,
    ) -> dict[str, Any]:
        """
        Estimate general liability and event insurance costs.

        General liability: $1M policy ~ $300-800 depending on risk
        Event insurance: attendance-based, $1-3 per attendee
        """
        # Risk factor by event type
        risk_factors: dict[str, float] = {
            "community": 1.0,
            "commercial": 1.3,
            "nonprofit": 0.8,
            "festival": 1.5,
            "market": 1.1,
            "garden": 0.6,
            "art": 0.9,
        }
        risk = risk_factors.get(event_type, 1.0)

        # General liability: base $400, scaled by total project value and risk
        gl_base = 400.0
        gl_value_factor = min(total_value / 50000.0, 3.0)  # Cap at 3x for large projects
        general_liability = gl_base * (1.0 + gl_value_factor) * risk
        general_liability = max(300.0, min(general_liability, 2500.0))

        # Event insurance: per-attendee with minimum
        per_attendee_rate = 1.50 * risk
        event_insurance = max(150.0, expected_attendance * per_attendee_rate)
        event_insurance = min(event_insurance, 5000.0)

        total = general_liability + event_insurance
        return {
            "general_liability": round(general_liability, 2),
            "event_insurance": round(event_insurance, 2),
            "total": round(total, 2),
        }

    # -----------------------------------------------------------------------
    # Operations costs
    # -----------------------------------------------------------------------

    def calculate_operations(
        self,
        elements: list[DesignElement],
        duration_days: int,
        expected_attendance: int = 100,
    ) -> dict[str, Any]:
        """
        Estimate operating costs: utilities, portable toilets, waste
        management, and security staffing.
        """
        line_items: list[dict[str, Any]] = []

        # -- Utilities (power) --
        # Elements requiring power: stages, PA, lighting, interactive
        power_elements = sum(
            el.quantity for el in elements
            if el.catalog_entry.get("category") in ("sound", "infrastructure", "structure")
            and el.catalog_entry.get("complexity", 0) >= 3
        )
        daily_power_cost = max(50.0, power_elements * 35.0)
        utilities_total = daily_power_cost * duration_days
        line_items.append({
            "category": "operations",
            "item": f"Power / utilities ({duration_days} days)",
            "quantity": duration_days,
            "unit_cost": round(daily_power_cost, 2),
            "total": round(utilities_total, 2),
        })

        # -- Portable toilets --
        # 1 per 100 attendees, minimum 1 if event > 1 day
        toilet_count = max(1, math.ceil(expected_attendance / 100))
        toilet_daily_rate = 125.0
        toilets_total = toilet_count * toilet_daily_rate * duration_days
        if duration_days > 0 and expected_attendance > 50:
            line_items.append({
                "category": "operations",
                "item": f"Portable toilets ({toilet_count} units)",
                "quantity": duration_days,
                "unit_cost": round(toilet_count * toilet_daily_rate, 2),
                "total": round(toilets_total, 2),
            })
        else:
            toilets_total = 0.0

        # -- Waste management --
        waste_daily = max(75.0, expected_attendance * 0.50)
        waste_total = waste_daily * duration_days
        line_items.append({
            "category": "operations",
            "item": f"Waste management ({duration_days} days)",
            "quantity": duration_days,
            "unit_cost": round(waste_daily, 2),
            "total": round(waste_total, 2),
        })

        # -- Security staffing --
        # 1 guard per 150 attendees, minimum 1 if attendance > 50
        if expected_attendance > 50:
            guard_count = max(1, math.ceil(expected_attendance / 150))
            guard_daily_rate = 320.0  # 8hr shift at $40/hr
            security_total = guard_count * guard_daily_rate * duration_days
            line_items.append({
                "category": "operations",
                "item": f"Security ({guard_count} guards x {duration_days} days)",
                "quantity": duration_days,
                "unit_cost": round(guard_count * guard_daily_rate, 2),
                "total": round(security_total, 2),
            })
        else:
            security_total = 0.0

        total = utilities_total + toilets_total + waste_total + security_total
        return {
            "utilities": round(utilities_total, 2),
            "staffing": round(security_total, 2),
            "security": round(security_total, 2),
            "total": round(total, 2),
            "line_items": line_items,
        }

    # -----------------------------------------------------------------------
    # Teardown
    # -----------------------------------------------------------------------

    def calculate_teardown(
        self,
        elements: list[DesignElement],
    ) -> dict[str, Any]:
        """
        Teardown costs: typically 30-60% of setup labor cost.
        Permanent elements have zero teardown (they stay).
        """
        teardown_hours_general: float = 0.0
        teardown_hours_skilled: float = 0.0

        for el in elements:
            catalog = el.catalog_entry
            if not catalog:
                continue
            # Permanent elements stay — no teardown
            if catalog.get("is_permanent", False):
                continue

            th = catalog.get("teardown_hours", 0.0) * el.quantity
            complexity = catalog.get("complexity", 1)
            if complexity >= COMPLEXITY_THRESHOLD_SKILLED:
                teardown_hours_skilled += th
            else:
                teardown_hours_general += th

        # Apply minimum call
        if teardown_hours_general > 0 and teardown_hours_general < CREW_MINIMUM_HOURS:
            teardown_hours_general = CREW_MINIMUM_HOURS
        if teardown_hours_skilled > 0 and teardown_hours_skilled < CREW_MINIMUM_HOURS:
            teardown_hours_skilled = CREW_MINIMUM_HOURS

        total = (
            teardown_hours_general * LABOR_RATE_PER_HOUR
            + teardown_hours_skilled * SKILLED_LABOR_RATE_PER_HOUR
        )
        return {
            "total": round(total, 2),
            "hours_general": round(teardown_hours_general, 2),
            "hours_skilled": round(teardown_hours_skilled, 2),
        }

    # -----------------------------------------------------------------------
    # Permanence value
    # -----------------------------------------------------------------------

    def calculate_permanence_value(
        self,
        elements: list[DesignElement],
    ) -> dict[str, Any]:
        """
        Calculate the value of permanent improvements left behind after
        the activation ends. This is the community wealth that stays.
        """
        total: float = 0.0
        permanent_items: list[dict[str, Any]] = []

        for el in elements:
            catalog = el.catalog_entry
            if not catalog:
                continue
            if not catalog.get("is_permanent", False):
                continue

            base_cost = el.custom_unit_cost if el.custom_unit_cost is not None else catalog["unit_cost"]
            perm_pct = catalog.get("permanence_value_pct", 0.0)
            item_value = base_cost * el.quantity * perm_pct
            total += item_value

            if item_value > 0:
                permanent_items.append({
                    "item": el.display_name,
                    "quantity": el.quantity,
                    "unit_value": round(base_cost * perm_pct, 2),
                    "total_value": round(item_value, 2),
                    "permanence_pct": round(perm_pct * 100, 0),
                })

        return {
            "total": round(total, 2),
            "items": permanent_items,
        }

    # -----------------------------------------------------------------------
    # Revenue projections
    # -----------------------------------------------------------------------

    def project_revenue(
        self,
        activation_type: str,
        size_sqft: float,
        duration_days: int,
        location_score: float,
        expected_attendance: int = 100,
        elements: list[DesignElement] | None = None,
        permanence_score: float = 0.5,
        equity_score: float = 0.5,
    ) -> dict[str, Any]:
        """
        Estimate revenue streams based on activation type and scale.

        Revenue sources:
        - Events (with stage): ticket sales
        - Markets: vendor fees
        - Gardens: grant eligibility
        - Art: sponsorship potential
        - General: corporate sponsorship
        """
        ticket_sales: float = 0.0
        vendor_fees: float = 0.0
        sponsorship_potential: float = 0.0
        grant_eligibility: float = 0.0

        elements = elements or []

        # -- Ticket sales (events with stage/seating) --
        has_stage = any(
            el.element_type in ("stage", "bleachers", "pa_system")
            for el in elements
        )
        if activation_type in ("event", "performance", "festival") or has_stage:
            # Seating capacity from elements
            seating_capacity = sum(
                el.quantity * (250 if el.element_type == "bleachers" else
                              1 if el.element_type in ("chair", "bench", "adirondack_chair") else
                              6 if el.element_type == "picnic_table" else 0)
                for el in elements
            )
            # If no seating defined, estimate from area
            if seating_capacity == 0:
                seating_capacity = max(50, int(size_sqft / 15))

            # Ticket price range: $15-50 based on location score
            avg_ticket = 15.0 + (50.0 - 15.0) * location_score
            # Fill rate: 60-85% based on location score
            fill_rate = 0.60 + 0.25 * location_score

            ticket_sales = (
                seating_capacity * avg_ticket * fill_rate * duration_days
            )

        # -- Vendor fees (markets) --
        has_market_stalls = any(
            el.element_type in ("food_stall", "food_truck_pad", "market_stall")
            for el in elements
        )
        if activation_type in ("pop_up_market", "market") or has_market_stalls:
            stall_count = sum(
                el.quantity
                for el in elements
                if el.element_type in ("food_stall", "food_truck_pad", "market_stall")
            )
            if stall_count == 0:
                stall_count = max(5, int(size_sqft / 200))

            # Vendor fee: $50-200/day/stall based on location
            daily_fee = 50.0 + 150.0 * location_score
            vendor_fees = stall_count * daily_fee * duration_days

        # -- Grant eligibility (gardens, community projects) --
        if activation_type in ("community_garden", "garden"):
            # $5,000-50,000 based on permanence and equity
            base_grant = 5000.0
            max_grant = 50000.0
            combined_score = (permanence_score * 0.5 + equity_score * 0.5)
            grant_eligibility = base_grant + (max_grant - base_grant) * combined_score
        elif permanence_score > 0.5:
            # Non-garden projects with high permanence can qualify for smaller grants
            grant_eligibility = 2000.0 + 15000.0 * permanence_score * equity_score

        # -- Sponsorship (art, general) --
        has_art = any(
            el.catalog_entry.get("category") == "art"
            for el in elements
        )
        if activation_type in ("art_installation", "art") or has_art:
            # Art sponsorship based on visibility (location_score) and permanence
            art_elements = sum(
                1 for el in elements
                if el.catalog_entry.get("category") == "art"
            )
            sponsorship_potential += (
                500.0 + 4500.0 * location_score
            ) * max(1, art_elements) * min(permanence_score + 0.3, 1.0)

        # General corporate sponsorship: $500-5000 based on activation size
        size_factor = min(size_sqft / 5000.0, 1.0)
        general_sponsorship = 500.0 + 4500.0 * size_factor * location_score
        sponsorship_potential += general_sponsorship

        total = ticket_sales + vendor_fees + sponsorship_potential + grant_eligibility
        return {
            "ticket_sales": round(ticket_sales, 2),
            "vendor_fees": round(vendor_fees, 2),
            "sponsorship_potential": round(sponsorship_potential, 2),
            "grant_eligibility": round(grant_eligibility, 2),
            "total": round(total, 2),
        }

    # -----------------------------------------------------------------------
    # Budget line generation
    # -----------------------------------------------------------------------

    def generate_budget_lines(
        self,
        design: DesignSpec,
    ) -> list[dict[str, Any]]:
        """
        Generate a full line-item budget array from a complete design spec.
        Aggregates all cost categories into a flat list of budget lines.
        """
        lines: list[dict[str, Any]] = []

        # Materials
        mat = self.calculate_element_costs(design.elements)
        for item in mat["line_items"]:
            lines.append({
                "category": "Materials",
                "item": item["item"],
                "quantity": item["quantity"],
                "unit_cost": item["unit_cost"],
                "total": item["total"],
            })

        # Labor
        labor = self.calculate_labor_costs(design.elements, design.duration_days)
        for item in labor["line_items"]:
            lines.append({
                "category": "Labor",
                "item": item["item"],
                "quantity": item.get("quantity", 1),
                "unit_cost": item["unit_cost"],
                "total": item["total"],
            })

        # Permits
        permits = self.calculate_permit_costs(design.elements)
        for p in permits["permits"]:
            lines.append({
                "category": "Permits",
                "item": p["permit"],
                "quantity": 1,
                "unit_cost": p["estimated_fee"],
                "total": p["estimated_fee"],
            })

        # Insurance
        mat_total = mat["total"]
        ins = self.calculate_insurance(
            mat_total + labor["total"],
            design.event_type,
            design.expected_attendance,
        )
        lines.append({
            "category": "Insurance",
            "item": "General liability insurance",
            "quantity": 1,
            "unit_cost": ins["general_liability"],
            "total": ins["general_liability"],
        })
        lines.append({
            "category": "Insurance",
            "item": "Event insurance",
            "quantity": 1,
            "unit_cost": ins["event_insurance"],
            "total": ins["event_insurance"],
        })

        # Operations
        ops = self.calculate_operations(
            design.elements,
            design.duration_days,
            design.expected_attendance,
        )
        for item in ops["line_items"]:
            lines.append({
                "category": "Operations",
                "item": item["item"],
                "quantity": item.get("quantity", 1),
                "unit_cost": item["unit_cost"],
                "total": item["total"],
            })

        # Teardown
        td = self.calculate_teardown(design.elements)
        if td["total"] > 0:
            lines.append({
                "category": "Teardown",
                "item": "Teardown labor",
                "quantity": 1,
                "unit_cost": td["total"],
                "total": td["total"],
            })

        return lines

    # -----------------------------------------------------------------------
    # Full estimate (top-level)
    # -----------------------------------------------------------------------

    def estimate(self, design: DesignSpec) -> dict[str, Any]:
        """
        Perform a complete cost estimate for a design, returning the full
        breakdown including revenue projections and permanence value.
        """
        # -- Cost calculations --
        mat = self.calculate_element_costs(design.elements)
        labor = self.calculate_labor_costs(design.elements, design.duration_days)
        permits = self.calculate_permit_costs(design.elements)
        ins = self.calculate_insurance(
            mat["total"] + labor["total"],
            design.event_type,
            design.expected_attendance,
        )
        ops = self.calculate_operations(
            design.elements,
            design.duration_days,
            design.expected_attendance,
        )
        td = self.calculate_teardown(design.elements)
        perm = self.calculate_permanence_value(design.elements)

        # -- Revenue projections --
        rev = self.project_revenue(
            activation_type=design.activation_type,
            size_sqft=design.size_sqft,
            duration_days=design.duration_days,
            location_score=design.location_score,
            expected_attendance=design.expected_attendance,
            elements=design.elements,
            permanence_score=design.permanence_score,
            equity_score=design.equity_score,
        )

        # -- Budget lines --
        budget_lines = self.generate_budget_lines(design)

        # -- Aggregation --
        total_cost = (
            mat["total"]
            + labor["total"]
            + permits["total"]
            + ins["total"]
            + ops["total"]
            + td["total"]
        )

        net_projection = rev["total"] - total_cost
        permanence_value = perm["total"]

        # ROI with permanence: treat permanence value as a form of return
        effective_return = rev["total"] + permanence_value
        roi_with_permanence = (
            (effective_return - total_cost) / total_cost * 100.0
            if total_cost > 0
            else 0.0
        )

        return {
            "elements_cost": {
                "materials": mat["total"],
                "labor": labor["total"],
                "equipment_rental": round(
                    sum(
                        item["total"]
                        for item in mat["line_items"]
                        if item.get("category") in ("sound", "infrastructure")
                    ),
                    2,
                ),
            },
            "permits_cost": {
                "application_fees": permits["total"],
                "insurance": ins["total"],
            },
            "operations_cost": {
                "utilities": ops["utilities"],
                "staffing": ops["staffing"],
                "security": ops["security"],
            },
            "teardown_cost": td["total"],
            "permanent_improvements_value": permanence_value,
            "total_cost": round(total_cost, 2),
            "cost_breakdown": budget_lines,
            "revenue_projections": {
                "ticket_sales": rev["ticket_sales"],
                "vendor_fees": rev["vendor_fees"],
                "sponsorship_potential": rev["sponsorship_potential"],
                "grant_eligibility": rev["grant_eligibility"],
            },
            "net_projection": round(net_projection, 2),
            "permanence_value": round(permanence_value, 2),
            "roi_with_permanence": round(roi_with_permanence, 2),
        }


# ---------------------------------------------------------------------------
# Benchmark data — reference costs for different activation types
# ---------------------------------------------------------------------------

ACTIVATION_BENCHMARKS: list[dict[str, Any]] = [
    {
        "type": "block_party",
        "label": "Block Party",
        "typical_size_sqft": 3000,
        "typical_duration_days": 1,
        "cost_range": {"min": 500, "max": 3000},
        "typical_elements": ["tent_10x10", "chair", "pa_system", "trash_recycling_station"],
        "description": "Neighborhood block party with basic setup, sound, and seating.",
    },
    {
        "type": "community_garden",
        "label": "Community Garden",
        "typical_size_sqft": 5000,
        "typical_duration_days": 365,
        "cost_range": {"min": 2000, "max": 15000},
        "typical_elements": ["raised_bed", "planter_large", "water_station", "fence_section_8ft", "signage"],
        "description": "Permanent raised-bed garden with fencing, irrigation, and signage.",
    },
    {
        "type": "pop_up_market",
        "label": "Pop-Up Market",
        "typical_size_sqft": 8000,
        "typical_duration_days": 1,
        "cost_range": {"min": 3000, "max": 12000},
        "typical_elements": ["tent_10x10", "market_stall", "food_stall", "signage", "trash_recycling_station"],
        "description": "Weekend market with vendor stalls, food trucks, and basic infrastructure.",
    },
    {
        "type": "art_installation",
        "label": "Art Installation",
        "typical_size_sqft": 2000,
        "typical_duration_days": 90,
        "cost_range": {"min": 5000, "max": 50000},
        "typical_elements": ["sculpture_large", "light_installation", "signage", "planter_large"],
        "description": "Temporary or semi-permanent public art with lighting and landscaping.",
    },
    {
        "type": "event_small",
        "label": "Small Event / Performance",
        "typical_size_sqft": 5000,
        "typical_duration_days": 1,
        "cost_range": {"min": 2000, "max": 8000},
        "typical_elements": ["stage", "chair", "pa_system", "lighting_string", "trash_recycling_station"],
        "description": "Small outdoor concert or community event with stage and seating.",
    },
    {
        "type": "event_large",
        "label": "Large Festival / Event",
        "typical_size_sqft": 20000,
        "typical_duration_days": 3,
        "cost_range": {"min": 15000, "max": 75000},
        "typical_elements": [
            "stage", "tent_30x60", "bleachers", "pa_system", "food_stall",
            "lighting_pole", "power_distribution", "jersey_barrier",
            "trash_recycling_station", "signage",
        ],
        "description": "Multi-day festival with stage, tents, food vendors, and full infrastructure.",
    },
    {
        "type": "pocket_park",
        "label": "Pocket Park / Parklet",
        "typical_size_sqft": 1500,
        "typical_duration_days": 365,
        "cost_range": {"min": 8000, "max": 40000},
        "typical_elements": [
            "bench", "planter_large", "tree", "paver_patio_100sqft",
            "lighting_string", "bike_rack", "trash_recycling_station", "signage",
        ],
        "description": "Permanent small park with seating, trees, paving, and amenities.",
    },
    {
        "type": "playground",
        "label": "Play Space",
        "typical_size_sqft": 4000,
        "typical_duration_days": 365,
        "cost_range": {"min": 20000, "max": 80000},
        "typical_elements": [
            "playground_element", "sod_patch_100sqft", "bench",
            "fence_section_8ft", "shade_sail", "trash_recycling_station", "signage",
        ],
        "description": "Community play space with equipment, safety surfacing, and shade.",
    },
]
