"""SQLAlchemy models and Pydantic schemas for SPHERE/OS production proposals.

A ProductionProposal encodes a film/TV/short-form production where programmable
materials ARE the narrative medium. The material_script field stores a timeline
of MaterialCue dicts — each mapping a story beat to a material state change
with a narrative function.
"""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Literal, TypedDict

from pydantic import BaseModel, Field
from sqlalchemy import ARRAY, ForeignKey, String, text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.shared.database import Base

# ---------------------------------------------------------------------------
# Enums / Literals
# ---------------------------------------------------------------------------

MATERIAL_SYSTEMS = Literal[
    "acoustic_metamaterial",
    "haptic_surface",
    "olfactory_synthesis",
    "electrochromic_surface",
    "projection_mapping",
    "phase_change_panel",
    "shape_memory_element",
    "4d_printed_deployable",
    "bioluminescent_coating",
]

MATERIAL_SYSTEMS_LIST: list[str] = [
    "acoustic_metamaterial",
    "haptic_surface",
    "olfactory_synthesis",
    "electrochromic_surface",
    "projection_mapping",
    "phase_change_panel",
    "shape_memory_element",
    "4d_printed_deployable",
    "bioluminescent_coating",
]

GENRE_OPTIONS = Literal["sci-fi", "drama", "thriller", "experimental"]

FORMAT_OPTIONS = Literal["feature_film", "series", "short", "installation", "hybrid"]

NARRATIVE_FUNCTIONS = Literal[
    "builds_tension",
    "reveals_character",
    "marks_time_passage",
    "establishes_mood",
    "signals_resolution",
    "creates_contrast",
]

LEGACY_MODES = Literal[
    "living_soundstage",
    "public_installation",
    "community_space",
    "research_lab",
]

# ---------------------------------------------------------------------------
# Physical transition-time constraints (seconds) per material system.
# Used by the generator to validate material_script timelines.
# ---------------------------------------------------------------------------

MATERIAL_TRANSITION_TIMES: dict[str, dict[str, float]] = {
    "acoustic_metamaterial": {"min_sec": 0.025, "max_sec": 60},
    "haptic_surface": {"min_sec": 0.025, "max_sec": 5},
    "olfactory_synthesis": {"min_sec": 600, "max_sec": 1200},  # 10-20 min clear
    "electrochromic_surface": {"min_sec": 1, "max_sec": 5},
    "projection_mapping": {"min_sec": 0.1, "max_sec": 10},
    "phase_change_panel": {"min_sec": 300, "max_sec": 1800},
    "shape_memory_element": {"min_sec": 300, "max_sec": 3600},
    "4d_printed_deployable": {"min_sec": 1800, "max_sec": 3600},
    "bioluminescent_coating": {"min_sec": 0, "max_sec": 0},  # persistent, not switchable
}


# ---------------------------------------------------------------------------
# MaterialCue — the building block of a material_script
# ---------------------------------------------------------------------------

class MaterialCue(TypedDict):
    """A single material state change at a specific story beat.

    Stored as dicts inside ProductionProposal.material_script (JSONB column).
    """

    beat_id: str  # e.g. "act1_inciting_incident", "climax", "denouement"
    timestamp_range: list[float] | str  # [start_sec, end_sec] or "persistent"
    material_system: str  # one of MATERIAL_SYSTEMS_LIST
    target_property: str  # the parameter being controlled
    value_curve: list[float]  # keyframe values over the timestamp_range
    narrative_function: str  # e.g. "builds_tension"


# ---------------------------------------------------------------------------
# MaterialPalette — tiered availability
# ---------------------------------------------------------------------------

class MaterialPalette(TypedDict):
    """Material systems available for a Sphere, organized by TRL tier."""

    tier_1_deployable_now: list[str]  # TRL 7-9
    tier_2_near_term: list[str]  # TRL 5-7
    tier_3_long_term: list[str]  # TRL 3-5


DEFAULT_MATERIAL_PALETTE: MaterialPalette = {
    "tier_1_deployable_now": [
        "acoustic_metamaterial",
        "olfactory_synthesis",
        "electrochromic_surface",
        "projection_mapping",
        "phase_change_panel",
    ],
    "tier_2_near_term": [
        "haptic_surface",
        "shape_memory_element",
        "4d_printed_deployable",
    ],
    "tier_3_long_term": [
        "bioluminescent_coating",
    ],
}


# ---------------------------------------------------------------------------
# SQLAlchemy ORM model
# ---------------------------------------------------------------------------

class ProductionProposal(Base):
    """A generated production proposal tying story beats to material cues."""

    __tablename__ = "production_proposals"
    __table_args__ = {"schema": "productions"}

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=text("gen_random_uuid()"),
    )
    parcel_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("land.parcels.id"),
    )

    # Production metadata
    title: Mapped[str]
    logline: Mapped[str]
    genre: Mapped[str]  # GENRE_OPTIONS
    format: Mapped[str]  # FORMAT_OPTIONS

    # Narrative
    narrative_concept: Mapped[str]  # 2-3 paragraph story description

    # Material script — the key innovation
    material_script: Mapped[list[dict]] = mapped_column(JSONB, default=list)

    # Site requirements
    min_area_sqft: Mapped[float]
    required_utilities: Mapped[list[str]] = mapped_column(ARRAY(String), default=list)
    crew_size_estimate: Mapped[int]

    # Budget & timeline
    estimated_budget_low_usd: Mapped[int]
    estimated_budget_high_usd: Mapped[int]
    production_timeline_weeks: Mapped[int]

    # Legacy modes
    legacy_modes: Mapped[list[str]] = mapped_column(ARRAY(String), default=list)

    # AI generation metadata
    generated_by_model: Mapped[str]
    creative_brief: Mapped[str | None] = mapped_column(default=None)
    generated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    # Optional link to parent proposal (for iterations)
    parent_proposal_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), default=None
    )
    iteration_feedback: Mapped[str | None] = mapped_column(default=None)


# ---------------------------------------------------------------------------
# Pydantic schemas (API request / response)
# ---------------------------------------------------------------------------

class GenerateRequest(BaseModel):
    """POST /generate request body."""

    parcel_id: uuid.UUID
    creative_brief: str | None = None
    tier_filter: list[int] | None = Field(
        default=None,
        description="Which TRL tiers to include, e.g. [1, 2]. Default: all tiers.",
    )
    format: str | None = Field(
        default=None,
        description="Production format constraint: feature_film, series, short, installation, hybrid.",
    )


class IterateRequest(BaseModel):
    """POST /{id}/iterate request body."""

    feedback: str = Field(
        ...,
        min_length=1,
        description="User feedback for regeneration, e.g. 'make it darker and more claustrophobic'.",
    )


class MaterialCueSchema(BaseModel):
    """Pydantic representation of a MaterialCue for API responses."""

    beat_id: str
    timestamp_range: list[float] | str
    material_system: str
    target_property: str
    value_curve: list[float]
    narrative_function: str


class ProposalResponse(BaseModel):
    """Full production proposal returned by the API."""

    id: uuid.UUID
    parcel_id: uuid.UUID
    title: str
    logline: str
    genre: str
    format: str
    narrative_concept: str
    material_script: list[MaterialCueSchema]
    min_area_sqft: float
    required_utilities: list[str]
    crew_size_estimate: int
    estimated_budget_low_usd: int
    estimated_budget_high_usd: int
    production_timeline_weeks: int
    legacy_modes: list[str]
    generated_by_model: str
    creative_brief: str | None
    generated_at: datetime
    parent_proposal_id: uuid.UUID | None = None
    iteration_feedback: str | None = None

    model_config = {"from_attributes": True}


class MaterialScriptResponse(BaseModel):
    """Just the material_script timeline (GET /{id}/material-script)."""

    proposal_id: uuid.UUID
    title: str
    material_script: list[MaterialCueSchema]

    model_config = {"from_attributes": True}
