"""
DOMES v2 — Flourishing Score Pydantic Schemas

Schemas for per-domain flourishing scores.
These are produced by the dome assembly pipeline and can also be
manually entered by clinicians or case managers.
"""
from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator

from domes.enums import FlourishingDomain, RiskLevel


# ---------------------------------------------------------------------------
# Flourishing score schemas
# ---------------------------------------------------------------------------

class FlourishingScoreCreate(BaseModel):
    """Create a flourishing score (manual entry or assembly-produced)."""

    model_config = ConfigDict(use_enum_values=True)

    person_id: uuid.UUID
    dome_id: uuid.UUID | None = None
    domain: FlourishingDomain
    scored_at: datetime
    score: float = Field(..., ge=0.0, le=100.0)
    score_delta: float | None = None
    trend: str | None = Field(
        None, description="'improving', 'stable', 'declining', 'volatile'"
    )
    risk_level: RiskLevel = RiskLevel.UNKNOWN
    threats: list[str] | None = Field(None, max_length=20)
    supports: list[str] | None = Field(None, max_length=20)
    domain_layer: int | None = Field(None, ge=1, le=3)
    is_foundation_met: bool | None = None
    evidence_sources: list[str] | None = None
    confidence: float | None = Field(None, ge=0.0, le=1.0)
    domain_data: dict[str, Any] | None = None
    recommendations: list[dict[str, Any]] | None = None
    narrative: str | None = Field(None, max_length=5000)

    @field_validator("trend")
    @classmethod
    def validate_trend(cls, v: str | None) -> str | None:
        if v is not None and v not in ("improving", "stable", "declining", "volatile"):
            raise ValueError("trend must be one of: improving, stable, declining, volatile")
        return v


class FlourishingScoreRead(BaseModel):
    """Full flourishing score read response."""

    model_config = ConfigDict(from_attributes=True, use_enum_values=True)

    id: uuid.UUID
    person_id: uuid.UUID
    dome_id: uuid.UUID | None
    domain: FlourishingDomain
    scored_at: datetime
    score: float
    score_delta: float | None
    trend: str | None
    risk_level: RiskLevel
    threats: list[str] | None
    supports: list[str] | None
    domain_layer: int | None
    is_foundation_met: bool | None
    evidence_sources: list[str] | None
    confidence: float | None
    domain_data: dict[str, Any] | None
    recommendations: list[dict[str, Any]] | None
    narrative: str | None
    created_at: datetime
    updated_at: datetime

    # Computed
    score_label: str | None = None
    needs_immediate_attention: bool | None = None


class FlourishingProfile(BaseModel):
    """All 12 domain scores for a person at a point in time (dome view)."""

    model_config = ConfigDict(from_attributes=True, use_enum_values=True)

    person_id: uuid.UUID
    dome_id: uuid.UUID | None
    scored_at: datetime
    scores: dict[str, FlourishingScoreRead]  # keyed by FlourishingDomain.value
    cosm_score: float | None = None  # mean of all 12 scores
    foundation_layer_met: bool | None = None  # all L1 domains >= 50


class FlourishingTrend(BaseModel):
    """Historical trend for a single flourishing domain."""

    model_config = ConfigDict(from_attributes=True)

    person_id: uuid.UUID
    domain: str  # FlourishingDomain enum value
    data_points: list[dict[str, Any]]  # [{scored_at, score, trend, risk_level}, ...]
    current_score: float | None = None
    current_trend: str | None = None
    score_30d_ago: float | None = None
    score_90d_ago: float | None = None
    score_365d_ago: float | None = None
