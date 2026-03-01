"""Request/response schemas for cascade detection endpoints."""

from __future__ import annotations

from pydantic import BaseModel, Field


class CascadeDetectRequest(BaseModel):
    """Request to run cascade detection on a person's current state."""

    lookback_months: int = Field(12, ge=1, le=60)
    min_confidence: float = Field(0.3, ge=0.0, le=1.0)
    cascade_ids: list[str] | None = None  # filter to specific cascades


class CascadeAlertSummary(BaseModel):
    """Summary of an active cascade alert."""

    alert_id: str
    cascade_id: str
    cascade_name: str
    current_link_index: int
    confidence: float
    path_a_projected_cost: float
    path_b_projected_cost: float
    potential_savings: float
    recommended_interventions: list[str]
