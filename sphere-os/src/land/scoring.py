"""Sphere viability scoring engine.

Calculates a 0-1 viability score for each parcel based on lot size, street
visibility, pedestrian traffic proximity, environmental risk, zoning
compatibility, neighborhood density, and cluster potential.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.land.models import ParcelRecord


# ---------------------------------------------------------------------------
# Zoning classification tables (Philadelphia zoning codes)
# ---------------------------------------------------------------------------

# Highly compatible zoning codes: commercial mixed-use, special purpose entertainment, etc.
ZONING_BOOST: set[str] = {
    "CMX-3",
    "CMX-4",
    "CMX-5",
    "SP-ENT",
    "ICMX",
    "SP-INS",
    "SP-STA",
    "I-2",
    "I-3",
    "CA-1",
    "CA-2",
}

# Moderately compatible zoning codes
ZONING_NEUTRAL: set[str] = {
    "CMX-1",
    "CMX-2",
    "CMX-2.5",
    "I-1",
    "IRMX",
    "SP-PO-A",
}

# Residential zoning: penalty (harder to get permits for Sphere activation)
ZONING_PENALTY: set[str] = {
    "RSA-1",
    "RSA-2",
    "RSA-3",
    "RSA-4",
    "RSA-5",
    "RSD-1",
    "RSD-2",
    "RSD-3",
    "RTA-1",
    "RM-1",
    "RM-2",
    "RM-3",
    "RM-4",
}


# ---------------------------------------------------------------------------
# Scoring weight configuration
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class ScoringWeights:
    """Configurable weights for each viability factor. Must sum to 1.0."""

    lot_size: float = 0.20
    street_visibility: float = 0.15
    pedestrian_traffic: float = 0.15
    environmental_risk: float = 0.15
    zoning_compatibility: float = 0.15
    neighborhood_density: float = 0.10
    cluster_potential: float = 0.10

    def total(self) -> float:
        return (
            self.lot_size
            + self.street_visibility
            + self.pedestrian_traffic
            + self.environmental_risk
            + self.zoning_compatibility
            + self.neighborhood_density
            + self.cluster_potential
        )


DEFAULT_WEIGHTS = ScoringWeights()


# ---------------------------------------------------------------------------
# Individual factor scoring functions (each returns 0-1)
# ---------------------------------------------------------------------------

def score_lot_size(area_sqft: float | None) -> float:
    """Score based on lot area.

    < 2000 sqft: very low (micro-sphere barely viable)
    2000-5000: linear ramp (0.2 -> 0.6)
    5000-20000: linear ramp (0.6 -> 0.9)
    20000-50000: linear ramp (0.9 -> 1.0)
    50000+: 1.0 (full sphere site)
    """
    if area_sqft is None or area_sqft <= 0:
        return 0.0
    if area_sqft < 2000:
        return max(0.05, area_sqft / 2000 * 0.2)
    if area_sqft < 5000:
        return 0.2 + (area_sqft - 2000) / 3000 * 0.4
    if area_sqft < 20000:
        return 0.6 + (area_sqft - 5000) / 15000 * 0.3
    if area_sqft < 50000:
        return 0.9 + (area_sqft - 20000) / 30000 * 0.1
    return 1.0


def score_street_visibility(street_frontage_ft: float | None, area_sqft: float | None) -> float:
    """Score based on street frontage-to-area ratio.

    Higher ratio = more visible from the street = better for public activation.
    Uses frontage_ft / sqrt(area_sqft) as a normalized visibility proxy.
    """
    if (
        street_frontage_ft is None
        or area_sqft is None
        or area_sqft <= 0
        or street_frontage_ft <= 0
    ):
        return 0.3  # Unknown defaults to moderate

    ratio = street_frontage_ft / math.sqrt(area_sqft)
    # Typical ratios: 0.3 (deep lot) to 2.0+ (wide shallow lot)
    if ratio < 0.2:
        return 0.1
    if ratio < 0.5:
        return 0.1 + (ratio - 0.2) / 0.3 * 0.3
    if ratio < 1.0:
        return 0.4 + (ratio - 0.5) / 0.5 * 0.4
    if ratio < 2.0:
        return 0.8 + (ratio - 1.0) / 1.0 * 0.2
    return 1.0


def score_pedestrian_traffic(transit_proximity_ft: float | None) -> float:
    """Score based on proximity to nearest transit stop.

    < 500 ft: high score (1.0)
    500-1000 ft: good (0.7-1.0 linear)
    1000-2640 ft (0.5 mile): moderate (0.3-0.7 linear)
    > 2640 ft: low (0.1-0.3 decay)
    """
    if transit_proximity_ft is None:
        return 0.4  # Unknown defaults to moderate-low

    if transit_proximity_ft <= 0:
        return 1.0
    if transit_proximity_ft < 500:
        return 0.85 + (500 - transit_proximity_ft) / 500 * 0.15
    if transit_proximity_ft < 1000:
        return 0.7 + (1000 - transit_proximity_ft) / 500 * 0.15
    if transit_proximity_ft < 2640:
        return 0.3 + (2640 - transit_proximity_ft) / 1640 * 0.4
    # Beyond half-mile, exponential decay
    return max(0.05, 0.3 * math.exp(-(transit_proximity_ft - 2640) / 5000))


def score_environmental_risk(environmental_flags: list[str] | None) -> float:
    """Score based on environmental contamination risk.

    Clean site: 1.0
    flood_zone: 0.6 penalty
    brownfield: 0.3 penalty (significant remediation cost)
    brownfield + flood_zone: 0.15
    Each additional flag reduces score further.
    """
    if not environmental_flags:
        return 1.0

    flags = {f.lower().strip() for f in environmental_flags}
    score = 1.0

    if "brownfield" in flags:
        score *= 0.3
    if "flood_zone" in flags:
        score *= 0.6
    if "superfund" in flags:
        score *= 0.1
    if "wetland" in flags:
        score *= 0.5
    if "underground_storage_tank" in flags:
        score *= 0.7
    if "landfill" in flags:
        score *= 0.2

    # Additional unknown flags get a small penalty each
    known = {"brownfield", "flood_zone", "superfund", "wetland", "underground_storage_tank", "landfill"}
    unknown_count = len(flags - known)
    if unknown_count > 0:
        score *= max(0.5, 1.0 - unknown_count * 0.1)

    return max(0.0, min(1.0, score))


def score_zoning_compatibility(zoning: str | None) -> float:
    """Score based on zoning code compatibility for Sphere activation.

    Commercial mixed-use, entertainment, industrial: high compatibility
    Residential: low compatibility (requires variance)
    Unknown: moderate default
    """
    if zoning is None or zoning.strip() == "":
        return 0.4  # Unknown

    code = zoning.strip().upper()

    if code in ZONING_BOOST:
        return 1.0
    if code in ZONING_NEUTRAL:
        return 0.65
    if code in ZONING_PENALTY:
        return 0.15

    # Partial matching for variant codes
    for prefix in ("CMX", "SP-ENT", "ICMX", "I-"):
        if code.startswith(prefix):
            return 0.8
    for prefix in ("RSA", "RSD", "RTA", "RM-"):
        if code.startswith(prefix):
            return 0.2

    return 0.4  # Unknown zoning code


def score_neighborhood_density(census_block_group: str | None) -> float:
    """Score based on neighborhood density from census block group.

    In a production system this would look up ACS population density data.
    For MVP, we derive a heuristic from the block group code structure.
    Philadelphia block groups with certain tract prefixes are known high-density.
    """
    if census_block_group is None or len(census_block_group) < 5:
        return 0.5  # Unknown defaults to moderate

    # Philadelphia county FIPS: 42101
    # High-density tracts: Center City, University City, etc.
    # In production, we'd query census ACS data for pop density
    # For MVP, use a simple hash-based proxy that produces consistent results
    try:
        # Use last 4 digits of block group as a density proxy
        digits = "".join(c for c in census_block_group if c.isdigit())
        if len(digits) < 4:
            return 0.5
        # Map to 0.2-0.9 range using modular arithmetic for deterministic results
        proxy = int(digits[-4:]) % 1000 / 1000
        return 0.2 + proxy * 0.7
    except (ValueError, IndexError):
        return 0.5


def score_cluster_potential(
    neighbor_count: int = 0,
    combined_area_sqft: float = 0,
) -> float:
    """Score based on number of adjacent parcels within 200ft.

    More neighbors = higher potential for combined Sphere site.
    """
    if neighbor_count <= 0:
        return 0.2  # Isolated parcel

    # Base score from neighbor count
    if neighbor_count == 1:
        base = 0.5
    elif neighbor_count == 2:
        base = 0.7
    elif neighbor_count <= 4:
        base = 0.85
    else:
        base = 1.0

    # Bonus for combined area
    if combined_area_sqft >= 50000:
        area_bonus = 0.15
    elif combined_area_sqft >= 20000:
        area_bonus = 0.10
    elif combined_area_sqft >= 10000:
        area_bonus = 0.05
    else:
        area_bonus = 0.0

    return min(1.0, base + area_bonus)


# ---------------------------------------------------------------------------
# Viability breakdown (detailed factor report)
# ---------------------------------------------------------------------------

@dataclass
class ViabilityBreakdown:
    """Detailed breakdown of viability scoring factors."""

    overall_score: float
    lot_size: float
    lot_size_weighted: float
    street_visibility: float
    street_visibility_weighted: float
    pedestrian_traffic: float
    pedestrian_traffic_weighted: float
    environmental_risk: float
    environmental_risk_weighted: float
    zoning_compatibility: float
    zoning_compatibility_weighted: float
    neighborhood_density: float
    neighborhood_density_weighted: float
    cluster_potential: float
    cluster_potential_weighted: float
    weights: ScoringWeights
    computed_at: str

    def to_dict(self) -> dict:
        return {
            "overall_score": round(self.overall_score, 4),
            "factors": {
                "lot_size": {
                    "raw_score": round(self.lot_size, 4),
                    "weight": self.weights.lot_size,
                    "weighted_score": round(self.lot_size_weighted, 4),
                },
                "street_visibility": {
                    "raw_score": round(self.street_visibility, 4),
                    "weight": self.weights.street_visibility,
                    "weighted_score": round(self.street_visibility_weighted, 4),
                },
                "pedestrian_traffic": {
                    "raw_score": round(self.pedestrian_traffic, 4),
                    "weight": self.weights.pedestrian_traffic,
                    "weighted_score": round(self.pedestrian_traffic_weighted, 4),
                },
                "environmental_risk": {
                    "raw_score": round(self.environmental_risk, 4),
                    "weight": self.weights.environmental_risk,
                    "weighted_score": round(self.environmental_risk_weighted, 4),
                },
                "zoning_compatibility": {
                    "raw_score": round(self.zoning_compatibility, 4),
                    "weight": self.weights.zoning_compatibility,
                    "weighted_score": round(self.zoning_compatibility_weighted, 4),
                },
                "neighborhood_density": {
                    "raw_score": round(self.neighborhood_density, 4),
                    "weight": self.weights.neighborhood_density,
                    "weighted_score": round(self.neighborhood_density_weighted, 4),
                },
                "cluster_potential": {
                    "raw_score": round(self.cluster_potential, 4),
                    "weight": self.weights.cluster_potential,
                    "weighted_score": round(self.cluster_potential_weighted, 4),
                },
            },
            "computed_at": self.computed_at,
        }


# ---------------------------------------------------------------------------
# Main scoring entry points
# ---------------------------------------------------------------------------

def calculate_sphere_viability_score(
    parcel: ParcelRecord,
    neighbor_count: int = 0,
    combined_area_sqft: float = 0,
    weights: ScoringWeights | None = None,
) -> float:
    """Calculate the composite sphere viability score (0-1) for a parcel.

    Args:
        parcel: The ParcelRecord to score.
        neighbor_count: Number of adjacent parcels within 200ft (for cluster scoring).
        combined_area_sqft: Total area of adjacent cluster (for cluster scoring).
        weights: Optional custom weights. Defaults to DEFAULT_WEIGHTS.

    Returns:
        Float between 0 and 1.
    """
    breakdown = calculate_viability_breakdown(
        parcel, neighbor_count, combined_area_sqft, weights
    )
    return breakdown.overall_score


def calculate_viability_breakdown(
    parcel: ParcelRecord,
    neighbor_count: int = 0,
    combined_area_sqft: float = 0,
    weights: ScoringWeights | None = None,
) -> ViabilityBreakdown:
    """Calculate detailed viability breakdown with per-factor scores.

    Args:
        parcel: The ParcelRecord to score.
        neighbor_count: Number of adjacent parcels within 200ft.
        combined_area_sqft: Total area of adjacent cluster.
        weights: Optional custom weights.

    Returns:
        ViabilityBreakdown with factor-level detail.
    """
    w = weights or DEFAULT_WEIGHTS

    # Calculate raw factor scores
    lot = score_lot_size(parcel.area_sqft)
    vis = score_street_visibility(parcel.street_frontage_ft, parcel.area_sqft)
    ped = score_pedestrian_traffic(parcel.transit_proximity_ft)
    env = score_environmental_risk(parcel.environmental_flags)
    zon = score_zoning_compatibility(parcel.zoning)
    den = score_neighborhood_density(parcel.census_block_group)
    clu = score_cluster_potential(neighbor_count, combined_area_sqft)

    # Weighted sum
    overall = (
        lot * w.lot_size
        + vis * w.street_visibility
        + ped * w.pedestrian_traffic
        + env * w.environmental_risk
        + zon * w.zoning_compatibility
        + den * w.neighborhood_density
        + clu * w.cluster_potential
    )
    overall = max(0.0, min(1.0, overall))

    return ViabilityBreakdown(
        overall_score=overall,
        lot_size=lot,
        lot_size_weighted=lot * w.lot_size,
        street_visibility=vis,
        street_visibility_weighted=vis * w.street_visibility,
        pedestrian_traffic=ped,
        pedestrian_traffic_weighted=ped * w.pedestrian_traffic,
        environmental_risk=env,
        environmental_risk_weighted=env * w.environmental_risk,
        zoning_compatibility=zon,
        zoning_compatibility_weighted=zon * w.zoning_compatibility,
        neighborhood_density=den,
        neighborhood_density_weighted=den * w.neighborhood_density,
        cluster_potential=clu,
        cluster_potential_weighted=clu * w.cluster_potential,
        weights=w,
        computed_at=datetime.now(timezone.utc).isoformat(),
    )


def calculate_viability_from_dict(
    area_sqft: float | None = None,
    street_frontage_ft: float | None = None,
    transit_proximity_ft: float | None = None,
    environmental_flags: list[str] | None = None,
    zoning: str | None = None,
    census_block_group: str | None = None,
    neighbor_count: int = 0,
    combined_area_sqft: float = 0,
    weights: ScoringWeights | None = None,
) -> ViabilityBreakdown:
    """Calculate viability from raw values without requiring a ParcelRecord ORM object.

    Useful in ingestion pipelines before persisting to DB.
    """
    w = weights or DEFAULT_WEIGHTS

    lot = score_lot_size(area_sqft)
    vis = score_street_visibility(street_frontage_ft, area_sqft)
    ped = score_pedestrian_traffic(transit_proximity_ft)
    env = score_environmental_risk(environmental_flags)
    zon = score_zoning_compatibility(zoning)
    den = score_neighborhood_density(census_block_group)
    clu = score_cluster_potential(neighbor_count, combined_area_sqft)

    overall = (
        lot * w.lot_size
        + vis * w.street_visibility
        + ped * w.pedestrian_traffic
        + env * w.environmental_risk
        + zon * w.zoning_compatibility
        + den * w.neighborhood_density
        + clu * w.cluster_potential
    )
    overall = max(0.0, min(1.0, overall))

    return ViabilityBreakdown(
        overall_score=overall,
        lot_size=lot,
        lot_size_weighted=lot * w.lot_size,
        street_visibility=vis,
        street_visibility_weighted=vis * w.street_visibility,
        pedestrian_traffic=ped,
        pedestrian_traffic_weighted=ped * w.pedestrian_traffic,
        environmental_risk=env,
        environmental_risk_weighted=env * w.environmental_risk,
        zoning_compatibility=zon,
        zoning_compatibility_weighted=zon * w.zoning_compatibility,
        neighborhood_density=den,
        neighborhood_density_weighted=den * w.neighborhood_density,
        cluster_potential=clu,
        cluster_potential_weighted=clu * w.cluster_potential,
        weights=w,
        computed_at=datetime.now(timezone.utc).isoformat(),
    )
