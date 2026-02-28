"""
DOMES v2 — FlourishingScore Model

Per-domain flourishing scores for a person at a point in time.
A FlourishingScore is linked to a Dome and provides the detailed
breakdown of the overall flourishing score.

The DOMES Flourishing Framework adapts Seligman's PERMA model and the
Capability Approach (Nussbaum/Sen) to the specific domains affecting
vulnerable persons in government systems:

Domains (each scored 0-100):
  1. SAFETY       - Physical safety, freedom from violence
  2. HEALTH       - Physical and mental health status
  3. HOUSING      - Housing stability and quality
  4. INCOME       - Financial security and income adequacy
  5. SOCIAL       - Social connections and community
  6. AUTONOMY     - Self-determination and agency
  7. MEANING      - Purpose, identity, spiritual wellbeing
  8. ENVIRONMENT  - Neighborhood conditions, air quality

Weights are configurable; defaults reflect evidence on SDH impact.

Risk levels per domain:
  CRITICAL: score < 25  (immediate intervention required)
  HIGH:     score < 40  (urgent attention needed)
  MEDIUM:   score < 60  (monitoring and support)
  LOW:      score >= 60 (stable, maintenance)
"""
from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any, TYPE_CHECKING

from sqlalchemy import DateTime, Enum, Float, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from domes.enums import RiskLevel
from domes.models.base import (
    AuditMixin,
    DOMESBase,
    TimestampMixin,
    UUIDPrimaryKeyMixin,
)

if TYPE_CHECKING:
    from domes.models.person import Person


class FlourishingScore(
    UUIDPrimaryKeyMixin,
    TimestampMixin,
    AuditMixin,
    DOMESBase,
):
    """Per-domain flourishing scores for a person.

    One FlourishingScore row = one scored snapshot linked to a Dome.
    The overall score is the weighted average of domain scores.
    """

    __tablename__ = "flourishing_score"
    __table_args__ = {
        "comment": (
            "Per-domain flourishing scores. One row per dome assembly. "
            "Linked to Dome.flourishing_score_id."
        )
    }

    person_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("person.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    scored_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        comment="Timestamp of score computation",
    )

    # ------------------------------------------------------------------
    # Overall score
    # ------------------------------------------------------------------

    overall_score: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        comment="Weighted average of domain scores (0-100)",
    )
    risk_level: Mapped[RiskLevel] = mapped_column(
        Enum(RiskLevel, name="risk_level_enum", create_type=False),
        nullable=False,
    )

    # ------------------------------------------------------------------
    # Domain scores (0-100 each)
    # ------------------------------------------------------------------

    safety_score: Mapped[float | None] = mapped_column(Float, nullable=True, comment="Physical safety domain (0-100)")
    health_score: Mapped[float | None] = mapped_column(Float, nullable=True, comment="Physical/mental health domain (0-100)")
    housing_score: Mapped[float | None] = mapped_column(Float, nullable=True, comment="Housing stability domain (0-100)")
    income_score: Mapped[float | None] = mapped_column(Float, nullable=True, comment="Financial security domain (0-100)")
    social_score: Mapped[float | None] = mapped_column(Float, nullable=True, comment="Social connections domain (0-100)")
    autonomy_score: Mapped[float | None] = mapped_column(Float, nullable=True, comment="Self-determination domain (0-100)")
    meaning_score: Mapped[float | None] = mapped_column(Float, nullable=True, comment="Purpose/meaning domain (0-100)")
    environment_score: Mapped[float | None] = mapped_column(Float, nullable=True, comment="Environmental conditions domain (0-100)")

    # ------------------------------------------------------------------
    # Domain risk levels
    # ------------------------------------------------------------------

    safety_risk: Mapped[RiskLevel | None] = mapped_column(Enum(RiskLevel, name="risk_level_enum", create_type=False), nullable=True)
    health_risk: Mapped[RiskLevel | None] = mapped_column(Enum(RiskLevel, name="risk_level_enum", create_type=False), nullable=True)
    housing_risk: Mapped[RiskLevel | None] = mapped_column(Enum(RiskLevel, name="risk_level_enum", create_type=False), nullable=True)
    income_risk: Mapped[RiskLevel | None] = mapped_column(Enum(RiskLevel, name="risk_level_enum", create_type=False), nullable=True)
    social_risk: Mapped[RiskLevel | None] = mapped_column(Enum(RiskLevel, name="risk_level_enum", create_type=False), nullable=True)
    autonomy_risk: Mapped[RiskLevel | None] = mapped_column(Enum(RiskLevel, name="risk_level_enum", create_type=False), nullable=True)
    meaning_risk: Mapped[RiskLevel | None] = mapped_column(Enum(RiskLevel, name="risk_level_enum", create_type=False), nullable=True)
    environment_risk: Mapped[RiskLevel | None] = mapped_column(Enum(RiskLevel, name="risk_level_enum", create_type=False), nullable=True)

    # ------------------------------------------------------------------
    # Domain drivers (top factors per domain)
    # ------------------------------------------------------------------

    safety_drivers: Mapped[Any | None] = mapped_column(JSONB(), nullable=True)
    health_drivers: Mapped[Any | None] = mapped_column(JSONB(), nullable=True)
    housing_drivers: Mapped[Any | None] = mapped_column(JSONB(), nullable=True)
    income_drivers: Mapped[Any | None] = mapped_column(JSONB(), nullable=True)
    social_drivers: Mapped[Any | None] = mapped_column(JSONB(), nullable=True)
    autonomy_drivers: Mapped[Any | None] = mapped_column(JSONB(), nullable=True)
    meaning_drivers: Mapped[Any | None] = mapped_column(JSONB(), nullable=True)
    environment_drivers: Mapped[Any | None] = mapped_column(JSONB(), nullable=True)

    # ------------------------------------------------------------------
    # Metadata
    # ------------------------------------------------------------------

    scoring_model_version: Mapped[str | None] = mapped_column(String(50), nullable=True)
    weights_used: Mapped[Any | None] = mapped_column(JSONB(), nullable=True, comment="Domain weights used in computation")
    data_completeness: Mapped[float | None] = mapped_column(Float, nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    # ------------------------------------------------------------------
    # Relationships
    # ------------------------------------------------------------------

    person: Mapped["Person"] = relationship("Person", back_populates="flourishing_scores", lazy="select")

    @property
    def is_critical(self) -> bool:
        """True if overall score is critical (<25) or risk level is critical/high."""
        return self.risk_level in (RiskLevel.CRITICAL, RiskLevel.HIGH) or float(self.overall_score) < 25
