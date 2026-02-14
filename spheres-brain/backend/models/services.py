"""
Pydantic models for the SPHERES Brain API gateway.

These models define every data structure that flows through the orchestrator:
service registration, parcel queries, unified results, health checks,
activity tracking, and webhook subscriptions.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Service registry
# ---------------------------------------------------------------------------

class ServiceEndpoint(BaseModel):
    """A single endpoint exposed by a SPHERES micro-service."""
    path: str
    method: str = "GET"
    description: str = ""


class ServiceInfo(BaseModel):
    """Metadata for a registered SPHERES micro-service."""
    name: str
    url: str
    port: int
    status: str = "unknown"           # up | down | degraded | unknown
    last_check: Optional[datetime] = None
    endpoints: list[ServiceEndpoint] = []
    description: str = ""
    health_endpoint: str = "/health"


# ---------------------------------------------------------------------------
# Parcel query / response
# ---------------------------------------------------------------------------

class ParcelQuery(BaseModel):
    """Input for the unified parcel lookup."""
    address: Optional[str] = None
    parcel_id: Optional[str] = None


class ParcelData(BaseModel):
    """Core property record (from spheres-assets)."""
    parcel_id: str
    address: str
    owner: str
    zoning: str
    area_sqft: float
    vacancy_status: str
    assessed_value: float
    last_sale: Optional[str] = None
    coordinates: Optional[dict] = None


class LegalPathway(BaseModel):
    """Permitting / legal roadmap (from spheres-legal)."""
    required_permits: list[str]
    estimated_timeline_days: int
    total_fees: float
    recommended_contracts: list[str]
    zoning_notes: str = ""


class CommunityDesign(BaseModel):
    """A single design concept (from spheres-studio)."""
    design_id: str
    name: str
    creator: str
    description: str
    cost_estimate: float
    rating: float = 0.0
    category: str = ""
    thumbnail_url: str = ""


class EpisodeAssociation(BaseModel):
    """Mapping to the nearest spheres-viz episode."""
    episode_number: int
    episode_title: str
    neighborhood: str
    relevance_score: float
    viz_url: str = ""


class ActivationRecord(BaseModel):
    """Historical activation event on a parcel."""
    activation_id: str
    date: str
    activation_type: str
    description: str
    status: str                      # completed | in-progress | planned
    participants: int = 0
    value_created: float = 0.0


class UnifiedParcelResult(BaseModel):
    """Combined result returned by the orchestrator for a parcel query."""
    query: ParcelQuery
    parcel_data: Optional[ParcelData] = None
    legal_pathway: Optional[LegalPathway] = None
    community_designs: list[CommunityDesign] = []
    episode_association: Optional[EpisodeAssociation] = None
    activation_history: list[ActivationRecord] = []
    queried_at: datetime = Field(default_factory=datetime.utcnow)


# ---------------------------------------------------------------------------
# Health
# ---------------------------------------------------------------------------

class HealthStatus(BaseModel):
    """Health probe result for a single service."""
    service_name: str
    status: str                      # up | down | degraded
    latency_ms: float
    last_check: datetime = Field(default_factory=datetime.utcnow)
    version: str = ""
    details: str = ""


class SystemHealth(BaseModel):
    """Aggregated health of the entire SPHERES ecosystem."""
    overall_status: str
    services: list[HealthStatus]
    checked_at: datetime = Field(default_factory=datetime.utcnow)


# ---------------------------------------------------------------------------
# Activity tracking
# ---------------------------------------------------------------------------

class ActivityEvent(BaseModel):
    """A single event logged across the SPHERES ecosystem."""
    event_id: str = ""
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    source_app: str
    event_type: str
    description: str
    parcel_id: Optional[str] = None
    metadata: dict = {}


# ---------------------------------------------------------------------------
# Subscriptions
# ---------------------------------------------------------------------------

class Subscription(BaseModel):
    """Webhook subscription for ecosystem events."""
    webhook_url: str
    events: list[str] = []           # event types to subscribe to
    created_at: datetime = Field(default_factory=datetime.utcnow)
    active: bool = True
    subscriber_name: str = ""


class SubscriptionResponse(BaseModel):
    subscription_id: str
    webhook_url: str
    events: list[str]
    created_at: datetime


# ---------------------------------------------------------------------------
# Metrics
# ---------------------------------------------------------------------------

class ActivationMetrics(BaseModel):
    """Aggregate metrics across the SPHERES ecosystem."""
    total_designs: int
    permits_pulled: int
    activations_completed: int
    activations_in_progress: int
    permanent_value_installed: float  # USD
    revenue_generated: float          # USD
    active_parcels: int
    community_participants: int
    period: str = "all-time"
    computed_at: datetime = Field(default_factory=datetime.utcnow)
