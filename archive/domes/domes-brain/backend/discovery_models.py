"""
Pydantic models for the DOMES Discovery Engine.
Defines schemas for discoveries, sources, scan results, and API request/response envelopes.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class SourceType(str, Enum):
    federal_register = "federal_register"
    ecfr = "ecfr"
    state_legislation = "state_legislation"
    academic = "academic"
    news = "news"
    gap_analysis = "gap_analysis"


class ImpactLevel(str, Enum):
    critical = "critical"
    high = "high"
    medium = "medium"
    low = "low"


class DiscoveryStatus(str, Enum):
    new = "new"
    reviewed = "reviewed"
    queued = "queued"
    ingested = "ingested"
    dismissed = "dismissed"


# ---------------------------------------------------------------------------
# Core Domain Models
# ---------------------------------------------------------------------------

class Discovery(BaseModel):
    """A single discovered item from any scanner source."""
    id: Optional[int] = None
    source_type: SourceType
    title: str
    summary: str
    url: str
    relevance_score: int = Field(ge=0, le=100, description="Relevance score 0-100")
    impact_level: ImpactLevel
    status: DiscoveryStatus = DiscoveryStatus.new
    discovered_at: datetime = Field(default_factory=datetime.utcnow)
    reviewed_at: Optional[datetime] = None
    metadata_json: dict[str, Any] = Field(default_factory=dict)
    tags: list[str] = Field(default_factory=list)

    model_config = {"from_attributes": True}


class DiscoverySource(BaseModel):
    """Configuration for a scanner data source."""
    id: Optional[int] = None
    name: str
    source_type: SourceType
    base_url: str
    last_scanned: Optional[datetime] = None
    scan_frequency_hours: int = 24
    active: bool = True
    description: str = ""

    model_config = {"from_attributes": True}


class ScanResult(BaseModel):
    """Result summary from a single scanner run."""
    source_name: str
    items_found: int
    new_items: int
    scan_duration_ms: int
    timestamp: datetime = Field(default_factory=datetime.utcnow)


# ---------------------------------------------------------------------------
# Request Models
# ---------------------------------------------------------------------------

class DiscoveryStatusUpdate(BaseModel):
    """Request body for updating a discovery's status."""
    status: DiscoveryStatus


class ScanRequest(BaseModel):
    """Request body for triggering a scan."""
    source_type: Optional[SourceType] = None


class DiscoveryFilter(BaseModel):
    """Query parameters for filtering discoveries."""
    source_type: Optional[SourceType] = None
    impact_level: Optional[ImpactLevel] = None
    status: Optional[DiscoveryStatus] = None
    limit: int = Field(default=50, ge=1, le=500)
    offset: int = Field(default=0, ge=0)


# ---------------------------------------------------------------------------
# Response Envelope
# ---------------------------------------------------------------------------

class ResponseMeta(BaseModel):
    """Metadata included in every API response."""
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    count: Optional[int] = None


class ApiResponse(BaseModel):
    """Standard response envelope: { status, data, meta }."""
    status: str = "ok"
    data: Any = None
    meta: ResponseMeta = Field(default_factory=ResponseMeta)


# ---------------------------------------------------------------------------
# Stats Models
# ---------------------------------------------------------------------------

class DiscoveryStats(BaseModel):
    """Aggregate counts by dimension."""
    by_source: dict[str, int] = Field(default_factory=dict)
    by_impact: dict[str, int] = Field(default_factory=dict)
    by_status: dict[str, int] = Field(default_factory=dict)
    total: int = 0
