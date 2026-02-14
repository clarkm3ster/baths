"""
Discovery Engine Models
=======================
Data models for the SPHERES discovery system — the continuous scanner
that finds new opportunities for public space activation in Philadelphia.
"""

from __future__ import annotations

from datetime import datetime, date
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class DiscoveryType(str, Enum):
    new_parcel = "new_parcel"
    policy_change = "policy_change"
    comparable_city = "comparable_city"
    media_mention = "media_mention"
    infrastructure_change = "infrastructure_change"


class ImpactLevel(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"


class ActivationType(str, Enum):
    pocket_park = "pocket_park"
    community_garden = "community_garden"
    urban_farm = "urban_farm"
    public_art = "public_art"
    playground = "playground"
    outdoor_classroom = "outdoor_classroom"
    stormwater_garden = "stormwater_garden"
    popup_market = "popup_market"
    rest_stop = "rest_stop"
    performance_space = "performance_space"


# ---------------------------------------------------------------------------
# Location
# ---------------------------------------------------------------------------

class Location(BaseModel):
    """Geographic coordinates and optional neighborhood label."""
    lat: float = Field(..., ge=-90, le=90)
    lng: float = Field(..., ge=-180, le=180)
    neighborhood: Optional[str] = None


# ---------------------------------------------------------------------------
# Discovery
# ---------------------------------------------------------------------------

class Discovery(BaseModel):
    """
    A single item surfaced by the scanning pipeline.  Could be a new vacant
    parcel, a policy shift, a comparable-city innovation, a media mention,
    or an infrastructure change near a target site.
    """
    id: str = Field(..., description="Unique discovery identifier")
    type: DiscoveryType
    title: str
    description: str
    source: str = Field(..., description="Where this was found (agency, news outlet, etc.)")
    url: Optional[str] = None
    discovered_at: datetime = Field(default_factory=datetime.utcnow)
    relevance_score: int = Field(..., ge=0, le=100, description="0-100 relevance to SPHERES mission")
    tags: list[str] = Field(default_factory=list)
    location: Optional[Location] = None


# ---------------------------------------------------------------------------
# Opportunity scoring factors
# ---------------------------------------------------------------------------

class ScoringFactor(BaseModel):
    """One dimension of the multi-factor opportunity score."""
    name: str
    score: int = Field(..., ge=0, le=100)
    description: str


class Opportunity(BaseModel):
    """
    A scored, actionable activation opportunity for a specific parcel.
    This is the core output of the scoring engine — what the SPHERES
    dashboard surfaces to planners and community members.
    """
    id: str
    parcel_id: str
    address: str
    score: int = Field(..., ge=0, le=100, description="Composite opportunity score")
    factors: list[ScoringFactor] = Field(default_factory=list)
    season_bonus: int = Field(0, ge=-20, le=20, description="Seasonal adjustment points")
    permit_window_open: bool = True
    community_demand_score: int = Field(0, ge=0, le=100)
    estimated_activation_cost: int = Field(..., ge=0, description="Estimated cost in USD")
    recommended_type: ActivationType
    neighborhood: Optional[str] = None
    location: Optional[Location] = None
    discovered_at: datetime = Field(default_factory=datetime.utcnow)


# ---------------------------------------------------------------------------
# Policy updates
# ---------------------------------------------------------------------------

class PolicyUpdate(BaseModel):
    """
    A change in city policy, zoning, or regulation that affects public
    space activation potential.
    """
    id: str
    title: str
    body: str
    source: str
    effective_date: date
    impact_level: ImpactLevel
    affected_areas: list[str] = Field(default_factory=list, description="Neighborhoods or zones affected")


# ---------------------------------------------------------------------------
# Comparable city projects
# ---------------------------------------------------------------------------

class ComparableCity(BaseModel):
    """
    An innovation from another city that could inform or inspire
    Philadelphia public space work.
    """
    city: str
    project_name: str
    description: str
    url: Optional[str] = None
    relevance_to_philly: str = Field(..., description="Why this matters for Philadelphia specifically")
    date_published: date


# ---------------------------------------------------------------------------
# Scan metadata
# ---------------------------------------------------------------------------

class ScanResult(BaseModel):
    """Summary returned after a scan completes."""
    scan_type: str
    items_found: int
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    next_scan: Optional[datetime] = None
