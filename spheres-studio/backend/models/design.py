"""
SPHERES Studio — Design Pydantic Models

Schemas for the activation design document: the elements placed on a parcel,
the parcel boundary polygon, and all associated metadata.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import List, Optional

from pydantic import BaseModel, Field

from models.elements import ElementLayer


# ---------------------------------------------------------------------------
# Geometry helpers
# ---------------------------------------------------------------------------

class Point(BaseModel):
    """A 2-D coordinate in the canvas's foot-based coordinate system."""
    x: float
    y: float


# ---------------------------------------------------------------------------
# Design element (instance on canvas)
# ---------------------------------------------------------------------------

class DesignElement(BaseModel):
    """A single element placed on the design canvas."""

    instance_id: str = Field(
        default_factory=lambda: uuid.uuid4().hex[:12],
        description="Unique instance identifier on the canvas",
    )
    element_id: str = Field(
        ...,
        description="References an ElementDefinition.id from the element library",
    )
    x: float = Field(default=0, description="X position in feet from canvas origin")
    y: float = Field(default=0, description="Y position in feet from canvas origin")
    rotation: float = Field(
        default=0,
        ge=0,
        lt=360,
        description="Clockwise rotation in degrees",
    )
    scale: float = Field(default=1.0, gt=0, description="Uniform scale factor")
    layer: ElementLayer = Field(
        default=ElementLayer.TEMPORARY,
        description="Rendering layer for this element",
    )
    locked: bool = Field(
        default=False,
        description="Prevent accidental moves when True",
    )
    custom_notes: str = Field(
        default="",
        description="Freeform notes attached to this element instance",
    )


# ---------------------------------------------------------------------------
# Full design document
# ---------------------------------------------------------------------------

class Design(BaseModel):
    """A complete activation design for a parcel."""

    id: str = Field(
        default_factory=lambda: uuid.uuid4().hex,
        description="Unique design identifier",
    )
    name: str = Field(default="Untitled Design", max_length=200)
    description: str = Field(default="", max_length=2000)
    parcel_id: Optional[str] = Field(
        default=None,
        description="Reference to the parcel/lot being designed",
    )
    parcel_footprint: List[Point] = Field(
        default_factory=list,
        description="Polygon vertices (in feet) defining the parcel boundary",
    )
    elements: List[DesignElement] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    author_id: Optional[str] = Field(default=None)
    is_public: bool = Field(default=False)
    tags: List[str] = Field(default_factory=list)
    thumbnail_url: Optional[str] = Field(default=None)


# ---------------------------------------------------------------------------
# Request / response schemas
# ---------------------------------------------------------------------------

class DesignCreate(BaseModel):
    """Payload for creating a new design."""

    name: str = Field(default="Untitled Design", max_length=200)
    description: str = Field(default="", max_length=2000)
    parcel_id: Optional[str] = None
    parcel_footprint: List[Point] = Field(default_factory=list)
    elements: List[DesignElement] = Field(default_factory=list)
    author_id: Optional[str] = None
    is_public: bool = False
    tags: List[str] = Field(default_factory=list)


class DesignUpdate(BaseModel):
    """Payload for updating an existing design. All fields optional."""

    name: Optional[str] = Field(default=None, max_length=200)
    description: Optional[str] = Field(default=None, max_length=2000)
    parcel_id: Optional[str] = None
    parcel_footprint: Optional[List[Point]] = None
    elements: Optional[List[DesignElement]] = None
    is_public: Optional[bool] = None
    tags: Optional[List[str]] = None
    thumbnail_url: Optional[str] = None


class DesignSummary(BaseModel):
    """Lightweight representation used in list endpoints."""

    id: str
    name: str
    description: str
    parcel_id: Optional[str]
    element_count: int
    created_at: datetime
    updated_at: datetime
    author_id: Optional[str]
    is_public: bool
    tags: List[str]
    thumbnail_url: Optional[str]


class PaginatedDesigns(BaseModel):
    """Paginated list of design summaries."""

    items: List[DesignSummary]
    total: int
    page: int
    page_size: int
    total_pages: int
