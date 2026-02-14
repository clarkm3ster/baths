"""
Pydantic models for the SPHERES Studio timeline engine.

Defines the data structures for timeline generation, tasks, phases,
and Philadelphia city event conflict detection.
"""

from __future__ import annotations

import uuid
from datetime import date, datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class Phase(str, Enum):
    PERMITS = "permits"
    PROCUREMENT = "procurement"
    SITE_PREP = "site_prep"
    SETUP = "setup"
    ACTIVATION = "activation"
    TEARDOWN = "teardown"
    PERMANENCE_HANDOFF = "permanence_handoff"


class TaskStatus(str, Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    BLOCKED = "blocked"


class AssignedTeam(str, Enum):
    PERMITS_TEAM = "permits_team"
    PROCUREMENT = "procurement"
    CONSTRUCTION = "construction"
    OPERATIONS = "operations"
    COMMUNITY = "community"


class ActivationType(str, Enum):
    SINGLE_DAY = "single_day"
    WEEKEND = "weekend"
    WEEK = "week"
    MONTH = "month"
    ONGOING = "ongoing"


class ConflictLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Season(str, Enum):
    SPRING = "spring"
    SUMMER = "summer"
    FALL = "fall"
    WINTER = "winter"


# ---------------------------------------------------------------------------
# Design element models (inputs to the timeline generator)
# ---------------------------------------------------------------------------

class DesignElement(BaseModel):
    """A single element within a design that the timeline must account for."""
    id: str = Field(default_factory=lambda: uuid.uuid4().hex[:12])
    name: str
    element_type: str = Field(
        description="Category: garden, stage, market, art_installation, "
                    "seating, lighting, sound, water_feature, playground, "
                    "food_vendor, structure, pathway, fencing, signage"
    )
    is_permanent: bool = False
    permit_requirements: list[str] = Field(
        default_factory=list,
        description="List of permit types needed: park_use, event, "
                    "food_service, amplified_sound, street_closure, "
                    "building, electrical, plumbing, vendor, fire_safety"
    )
    requires_construction: bool = False
    requires_vendors: bool = False
    lead_time_days: int = Field(
        default=7,
        description="Extra procurement lead time in days"
    )
    setup_hours: float = Field(
        default=4.0,
        description="Estimated hours to set up this element"
    )
    teardown_hours: float = Field(
        default=2.0,
        description="Estimated hours to tear down this element"
    )
    notes: str = ""


class DesignInput(BaseModel):
    """The design payload submitted to the timeline generator."""
    id: str = Field(default_factory=lambda: uuid.uuid4().hex[:12])
    name: str = "Untitled Design"
    elements: list[DesignElement] = Field(default_factory=list)
    activation_type: ActivationType = ActivationType.SINGLE_DAY
    location: str = "Philadelphia, PA"
    notes: str = ""


# ---------------------------------------------------------------------------
# Timeline task & timeline models
# ---------------------------------------------------------------------------

class TimelineTask(BaseModel):
    """A single task within the project timeline."""
    id: str = Field(default_factory=lambda: uuid.uuid4().hex[:12])
    name: str
    phase: Phase
    start_date: date
    end_date: date
    duration_days: int = Field(ge=0)
    dependencies: list[str] = Field(
        default_factory=list,
        description="List of task IDs this task depends on"
    )
    assigned_team: AssignedTeam
    status: TaskStatus = TaskStatus.NOT_STARTED
    notes: str = ""
    milestone: bool = False


class Timeline(BaseModel):
    """A complete project timeline consisting of phased tasks."""
    id: str = Field(default_factory=lambda: uuid.uuid4().hex[:12])
    design_id: str
    name: str = "Untitled Timeline"
    tasks: list[TimelineTask] = Field(default_factory=list)
    target_activation_date: date
    activation_end_date: date
    created_at: datetime = Field(default_factory=datetime.utcnow)
    total_duration_days: int = 0
    weather_buffer_days: int = 0
    season_warnings: list[str] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# Request / response schemas
# ---------------------------------------------------------------------------

class TimelineGenerateRequest(BaseModel):
    """Request body for POST /api/timeline/generate."""
    design: DesignInput
    target_activation_date: date
    duration_days: int = Field(
        default=1,
        ge=1,
        description="How many days the activation lasts"
    )


class TimelineUpdateRequest(BaseModel):
    """Request body for PUT /api/timeline/{id}."""
    tasks: Optional[list[TimelineTask]] = None
    target_activation_date: Optional[date] = None
    name: Optional[str] = None


class ConflictCheckRequest(BaseModel):
    """Query parameters for GET /api/timeline/conflicts."""
    start_date: date
    end_date: date
    location: str = "Philadelphia, PA"


# ---------------------------------------------------------------------------
# Philadelphia city event conflict model
# ---------------------------------------------------------------------------

class PhillyEvent(BaseModel):
    """A Philadelphia city event that could conflict with our activation."""
    name: str
    date: date
    end_date: Optional[date] = None
    location: str
    conflict_level: ConflictLevel
    description: str = ""
    impact_notes: str = Field(
        default="",
        description="How this event may affect the activation (parking, "
                    "road closures, noise, crowd overlap)"
    )


class ConflictReport(BaseModel):
    """Response model for the conflict check endpoint."""
    checked_range_start: date
    checked_range_end: date
    conflicts: list[PhillyEvent] = Field(default_factory=list)
    total_conflicts: int = 0
    has_critical: bool = False
    recommendation: str = ""
