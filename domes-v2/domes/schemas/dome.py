"""
DOMES v2 — Dome Pydantic Schemas

Schemas for the assembled digital twin snapshot.
The Dome is the primary deliverable of the DOMES system.

Key response shapes:
- DomeRead: full dome with all risk scores, domain scores, recommendations
- DomeSummary: lightweight card view for dashboards
- DomeCostAnalysis: financial breakdown only (for finance/admin users)
"""
from __future__ import annotations

import uuid
from datetime import datetime
from decimal import Decimal
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, model_validator

from domes.enums import DomeTrigger, FlourishingDomain, RiskLevel


# ---------------------------------------------------------------------------
# Sub-schemas for structured JSONB fields
# ---------------------------------------------------------------------------

class RiskScoreDetail(BaseModel):
    """Structure of a single risk score within the risk_scores JSONB."""

    score: float = Field(..., ge=0.0, le=1.0, description="Risk probability 0.0–1.0")
    level: RiskLevel
    drivers: list[str] = Field(default_factory=list, description="Top risk factors")
    model_version: str | None = None
    computed_at: datetime | None = None


class DomainScoreDetail(BaseModel):
    """Structure of a single domain score within the domain_scores JSONB."""

    score: float = Field(..., ge=0.0, le=100.0, description="Flourishing score 0-100")
    trend: str | None = Field(
        None, description="'improving', 'stable', 'declining', 'volatile'"
    )
    threats: list[str] = Field(default_factory=list)
    supports: list[str] = Field(default_factory=list)


class RecommendationItem(BaseModel):
    """A single prioritized recommendation in the dome."""

    priority: int = Field(..., ge=1, le=10)
    domain: str | None = None  # FlourishingDomain enum value
    action: str = Field(..., max_length=500)
    rationale: str | None = Field(None, max_length=1000)
    estimated_impact: str | None = Field(None, max_length=255)
    system_responsible: str | None = Field(None, max_length=255)
    urgency: str | None = Field(
        None, description="'immediate', 'soon' (within 30d), 'routine' (90d)"
    )


# ---------------------------------------------------------------------------
# Dome trigger request
# ---------------------------------------------------------------------------

class DomeAssembleRequest(BaseModel):
    """Request to manually trigger a dome assembly for a person."""

    person_id: uuid.UUID
    trigger: DomeTrigger = DomeTrigger.MANUAL
    reason: str | None = Field(None, max_length=500)


# ---------------------------------------------------------------------------
# Dome read schemas
# ---------------------------------------------------------------------------

class DomeSummary(BaseModel):
    """Lightweight dome card for dashboards and lists."""

    model_config = ConfigDict(from_attributes=True, use_enum_values=True)

    id: uuid.UUID
    person_id: uuid.UUID
    assembled_at: datetime
    is_current: bool
    trigger: DomeTrigger
    cosm_score: float | None
    cosm_label: str | None
    cosm_delta: float | None
    overall_risk_level: RiskLevel
    crisis_flags: list[str] | None
    fragment_count: int
    systems_represented: list[str] | None
    fragmented_annual_cost: Decimal | None
    coordinated_annual_cost: Decimal | None
    delta: Decimal | None


class DomeCostAnalysis(BaseModel):
    """Financial analysis component of a dome."""

    model_config = ConfigDict(from_attributes=True, use_enum_values=True)

    id: uuid.UUID
    person_id: uuid.UUID
    assembled_at: datetime
    fragmented_annual_cost: Decimal | None
    coordinated_annual_cost: Decimal | None
    delta: Decimal | None
    lifetime_cost_estimate: Decimal | None
    cost_methodology: str | None
    savings_percentage: float | None = None

    @model_validator(mode="after")
    def compute_savings_pct(self) -> DomeCostAnalysis:
        if (
            self.fragmented_annual_cost
            and self.delta
            and float(self.fragmented_annual_cost) > 0
        ):
            self.savings_percentage = round(
                float(self.delta) / float(self.fragmented_annual_cost) * 100, 1
            )
        return self


class DomeRead(BaseModel):
    """Full dome read response with all computed fields."""

    model_config = ConfigDict(from_attributes=True, use_enum_values=True)

    id: uuid.UUID
    person_id: uuid.UUID
    assembled_at: datetime
    is_current: bool
    trigger: DomeTrigger
    assembly_version: str

    # COSM
    cosm_score: float | None
    cosm_label: str | None
    cosm_delta: float | None
    cosm_tier: str | None = None

    # Risk
    risk_scores: dict[str, Any] | None  # keyed by risk domain
    overall_risk_level: RiskLevel
    crisis_flags: list[str] | None

    # Domains
    domain_scores: dict[str, Any] | None  # keyed by FlourishingDomain

    # Cost
    fragmented_annual_cost: Decimal | None
    coordinated_annual_cost: Decimal | None
    delta: Decimal | None
    lifetime_cost_estimate: Decimal | None
    cost_methodology: str | None

    # Coverage
    systems_represented: list[str] | None
    systems_missing: list[str] | None
    fragment_count: int

    # Actions
    recommendations: list[dict[str, Any]] | None

    # Assembly metadata
    assembly_duration_ms: int | None
    assembly_errors: list[str] | None
    narrative_summary: str | None

    # Standard
    created_at: datetime
    updated_at: datetime
    created_by: str | None
