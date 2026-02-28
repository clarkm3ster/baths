"""
DOMES v2 — FlourishingScore Model

Per-domain flourishing scores for a person at a point in time.
One FlourishingScore row per (person, domain, scored_at) triplet.

The 12 Flourishing Domains — organized in 3 layers:

LAYER 1 — Foundation (survival needs, Maslow levels 1-2):
    health_vitality          Physical and mental health status
    economic_prosperity      Income, benefits, financial stability
    community_belonging      Social connection, belonging, social capital
    environmental_harmony    Safe and healthy physical environment

LAYER 2 — Aspiration (growth, Maslow levels 3-4):
    creative_expression      Arts, self-expression, creativity
    intellectual_growth      Education, learning, cognitive engagement
    physical_space_beauty    Safe, stable, aesthetically adequate housing
    play_joy                 Recreation, fun, rest, leisure

LAYER 3 — Transcendence (meaning, Maslow level 5):
    spiritual_depth          Connection to something larger, faith, practice
    love_relationships       Intimate and family relationships
    purpose_meaning          Sense of purpose, direction, contribution
    legacy_contribution      Impact on community, generativity

Score semantics:
    0    = Total absence / crisis in this domain
    25   = Significant deficits (needs immediate attention)
    50   = Moderate functioning (some needs met, gaps remain)
    75   = Good functioning (most needs met, minor gaps)
    100  = Thriving (domain fully flourishing)

Threats and supports are structured as string lists to enable:
    - Pattern matching across population ("what % face housing threats?")
    - Recommendation engine input
    - Trend analysis over time

Robert Jackson example (health_vitality domain):
    score = 12
    threats = [
        "schizoaffective_disorder_untreated",
        "medication_nonadherence",
        "47_annual_er_visits",
        "unsheltered_7_years",
        "no_primary_care_physician"
    ]
    supports = [
        "medicaid_enrolled",
        "mobile_crisis_contact_history"
    ]
"""
from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any, TYPE_CHECKING

from sqlalchemy import (
    Boolean,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Index,
    Numeric,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import ARRAY, JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from domes.enums import FlourishingDomain, RiskLevel
from domes.models.base import (
    AuditMixin,
    DOMESBase,
    TimestampMixin,
    UUIDPrimaryKeyMixin,
)

if TYPE_CHECKING:
    from domes.models.dome import Dome
    from domes.models.person import Person


class FlourishingScore(
    UUIDPrimaryKeyMixin,
    TimestampMixin,
    AuditMixin,
    DOMESBase,
):
    """
    A single flourishing domain score for a person at a specific time.

    Each Dome assembly produces 12 FlourishingScore rows (one per domain).
    The dome_id FK links these scores back to the Dome that computed them.

    Scores are point-in-time — never updated, only superseded by new
    scores from subsequent dome assemblies. This creates a full history
    of flourishing trajectory across all 12 domains.

    Indexes:
        - idx_flourishing_person_domain_time: (person_id, domain, scored_at DESC)
          — primary access pattern: "trend for this domain for this person"
        - idx_flourishing_dome: (dome_id)
          — all 12 scores for a specific dome assembly
        - idx_flourishing_critical: (domain, risk_level) WHERE = 'critical'
          — population crisis dashboard
    """

    __tablename__ = "flourishing_score"
    __table_args__ = (
        Index(
            "idx_flourishing_person_domain_time",
            "person_id",
            "domain",
            "scored_at",
            postgresql_ops={"scored_at": "DESC"},
        ),
        Index("idx_flourishing_dome", "dome_id"),
        Index(
            "idx_flourishing_critical",
            "domain",
            "risk_level",
            postgresql_where="risk_level = 'critical'",
        ),
        {"comment": "12-domain flourishing scores per person per dome assembly"},
    )

    # ------------------------------------------------------------------
    # Core identity
    # ------------------------------------------------------------------

    person_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("person.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="Person this flourishing score belongs to",
    )

    dome_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("dome.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
        comment="Dome assembly this score was computed from (NULL if standalone assessment)",
    )

    domain: Mapped[FlourishingDomain] = mapped_column(
        Enum(FlourishingDomain, name="flourishing_domain_enum", create_type=False),
        nullable=False,
        comment="Which of the 12 flourishing domains this score covers",
    )

    scored_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        comment="UTC timestamp when this score was computed",
    )

    # ------------------------------------------------------------------
    # Score
    # ------------------------------------------------------------------

    score: Mapped[float] = mapped_column(
        Numeric(5, 2),
        nullable=False,
        comment=(
            "Flourishing score 0-100 for this domain. "
            "0=absent/crisis, 25=significant deficits, 50=moderate, "
            "75=good functioning, 100=thriving."
        ),
    )

    score_delta: Mapped[float | None] = mapped_column(
        Numeric(5, 2),
        nullable=True,
        comment="Change since previous score for this domain (+positive = improvement)",
    )

    trend: Mapped[str | None] = mapped_column(
        String(32),
        nullable=True,
        comment=(
            "Direction of change: 'improving', 'stable', 'declining', 'volatile'. "
            "Computed from last 3 scores."
        ),
    )

    risk_level: Mapped[RiskLevel] = mapped_column(
        Enum(RiskLevel, name="risk_level_enum", create_type=False),
        nullable=False,
        default=RiskLevel.UNKNOWN,
        comment="Risk classification derived from this domain's score",
    )

    # ------------------------------------------------------------------
    # Threats and supports
    # ------------------------------------------------------------------

    threats: Mapped[Any | None] = mapped_column(
        JSONB(),
        ARRAY(String),
        nullable=True,
        comment=(
            "Identified threats in this domain. Machine-readable slugs "
            "(e.g., 'medication_nonadherence', 'housing_loss_imminent', "
            "'food_insecurity', 'social_isolation'). Max 20 items."
        ),
    )

    supports: Mapped[Any | None] = mapped_column(
        JSONB(),
        ARRAY(String),
        nullable=True,
        comment=(
            "Active protective factors in this domain "
            "(e.g., 'medicaid_enrolled', 'act_team_active', 'stable_income')"
        ),
    )

    # ------------------------------------------------------------------
    # Layer metadata
    # ------------------------------------------------------------------

    domain_layer: Mapped[int | None] = mapped_column(
        nullable=True,
        comment=(
            "Flourishing layer: 1=Foundation, 2=Aspiration, 3=Transcendence. "
            "Foundation layers are prerequisites for higher layers."
        ),
    )

    is_foundation_met: Mapped[bool | None] = mapped_column(
        Boolean,
        nullable=True,
        comment=(
            "For Layer 1 domains: True if this domain score meets the minimum "
            "threshold (>=50) required to access Layer 2 domains. NULL for L2/L3."
        ),
    )

    # ------------------------------------------------------------------
    # Assessment evidence
    # ------------------------------------------------------------------

    evidence_sources: Mapped[Any | None] = mapped_column(
        JSONB(),
        ARRAY(String),
        nullable=True,
        comment=(
            "Data sources used to compute this score "
            "(e.g., 'phq_9', 'hmis_enrollment', 'encounter_count', 'biometric')"
        ),
    )

    confidence: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
        comment=(
            "Model confidence 0.0–1.0 in this score. "
            "Low confidence = limited data; high = strong multi-source evidence."
        ),
    )

    # ------------------------------------------------------------------
    # Domain-specific data
    # ------------------------------------------------------------------

    domain_data: Mapped[Any | None] = mapped_column(
        JSONB(),
        nullable=True,
        comment=(
            "Domain-specific structured data used in scoring. Examples: "
            "health_vitality: {phq9_score, gaf_score, er_visits_90d, medication_adherent}, "
            "economic_prosperity: {monthly_income, benefit_programs, debt_amount}, "
            "community_belonging: {social_network_size, isolation_days_30d}"
        ),
    )

    # ------------------------------------------------------------------
    # Recommendations for this domain
    # ------------------------------------------------------------------

    recommendations: Mapped[Any | None] = mapped_column(
        JSONB(),
        nullable=True,
        comment=(
            "Domain-specific action recommendations. Each: "
            "{'action': str, 'priority': int 1-5, 'rationale': str, "
            "'estimated_impact': str, 'owner': str}"
        ),
    )

    narrative: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        comment="Plain-language narrative about this person's status in this domain",
    )

    # ------------------------------------------------------------------
    # Relationships
    # ------------------------------------------------------------------

    person: Mapped[Person] = relationship(
        "Person",
        back_populates="flourishing_scores",
        lazy="select",
    )

    dome: Mapped[Dome | None] = relationship(
        "Dome",
        foreign_keys=[dome_id],
        lazy="select",
    )

    # ------------------------------------------------------------------
    # Computed properties
    # ------------------------------------------------------------------

    @property
    def score_label(self) -> str:
        """Return a human-readable label for this score."""
        if self.score < 25:
            return "Crisis"
        elif self.score < 50:
            return "Fragile"
        elif self.score < 75:
            return "Stable"
        else:
            return "Thriving"

    @property
    def threat_count(self) -> int:
        """Return the number of active threats in this domain."""
        return len(self.threats) if self.threats else 0

    @property
    def needs_immediate_attention(self) -> bool:
        """Return True if this domain requires immediate intervention."""
        return self.risk_level in (RiskLevel.CRITICAL, RiskLevel.HIGH) or float(self.score) < 25
