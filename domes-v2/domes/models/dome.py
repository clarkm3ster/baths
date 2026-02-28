"""
DOMES v2 — Dome Model (Assembled Digital Twin Snapshot)

The Dome is a computed, point-in-time snapshot of a person's complete
digital twin. It assembles data from all underlying tables into a unified
view optimized for care coordination, resource allocation, and crisis prediction.

The Dome is the PRIMARY DELIVERABLE of the DOMES system. It is:
1. Assembled on trigger (new_data, scheduled, manual, crisis_event)
2. Stored as an immutable snapshot — never updated, only superseded
3. Includes cost analysis: fragmented vs. coordinated annual spend delta
4. Contains risk scores, domain scores, and structured recommendations
5. Tracks which fragments / source systems contributed to this assembly

Key financial metrics (Robert Jackson example):
    fragmented_annual_cost  = $112,100  (what the system currently spends)
    coordinated_annual_cost =  $41,200  (what proper coordination would cost)
    delta                   =  $70,900  (annual savings from coordination)
    lifetime_cost_estimate  = $1,446,360 (50-year projection at fragmented rate)

COSM Score (Comprehensive Outcome Stability Metric):
    0-100 composite score across 12 flourishing domains.
    <25 = Crisis  |  25-50 = Fragile  |  50-75 = Stable  |  75-100 = Thriving

Risk scores (stored as JSONB):
    {
        "crisis_30d": {"score": 0.87, "level": "critical", "drivers": [...]},
        "readmission_30d": {"score": 0.73, "level": "high"},
        "housing_loss_90d": {"score": 0.65, "level": "high"},
        "substance_relapse_30d": {"score": 0.45, "level": "moderate"},
        "medication_nonadherence_7d": {"score": 0.92, "level": "critical"}
    }
"""
from __future__ import annotations

import uuid
from datetime import datetime
from decimal import Decimal
from typing import Any, TYPE_CHECKING

from sqlalchemy import (
    Boolean,
    DateTime,
    Enum,
    ForeignKey,
    Index,
    Integer,
    Numeric,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import ARRAY, JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from domes.enums import DomeTrigger, RiskLevel
from domes.models.base import (
    AuditMixin,
    DOMESBase,
    TimestampMixin,
    UUIDPrimaryKeyMixin,
)

if TYPE_CHECKING:
    from domes.models.person import Person


class Dome(
    UUIDPrimaryKeyMixin,
    TimestampMixin,
    AuditMixin,
    DOMESBase,
):
    """
    An immutable assembled digital twin snapshot for a person.

    Each Dome represents the complete view of a person at a specific
    assembled_at timestamp. When new data arrives or a trigger fires,
    a new Dome is assembled and the previous one is marked is_current=False.

    Never update an existing Dome row — always insert a new one and
    flip is_current flags. This preserves the full history of a person's
    digital twin over time.

    Indexes:
        - idx_dome_person_current: (person_id) WHERE is_current = true
          — the most common query: "give me this person's current dome"
        - idx_dome_person_assembled: (person_id, assembled_at DESC)
          — historical dome timeline
        - idx_dome_cosm: (cosm_score) — population-level risk stratification
        - idx_dome_crisis: (overall_risk_level) WHERE = 'critical'
          — crisis response queue
    """

    __tablename__ = "dome"
    __table_args__ = (
        Index(
            "idx_dome_person_current",
            "person_id",
            postgresql_where="is_current = true",
            unique=True,  # Only one current dome per person
        ),
        Index(
            "idx_dome_person_assembled",
            "person_id",
            "assembled_at",
            postgresql_ops={"assembled_at": "DESC"},
        ),
        Index("idx_dome_cosm", "cosm_score"),
        Index(
            "idx_dome_crisis",
            "overall_risk_level",
            postgresql_where="overall_risk_level = 'critical'",
        ),
        {"comment": "Assembled digital twin snapshots — one current per person, full history retained"},
    )

    # ------------------------------------------------------------------
    # Core identity
    # ------------------------------------------------------------------

    person_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("person.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="Person this dome snapshot belongs to",
    )

    assembled_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        comment="UTC timestamp when this dome was assembled",
    )

    is_current: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        comment="True = this is the most recent dome for this person",
    )

    trigger: Mapped[DomeTrigger] = mapped_column(
        Enum(DomeTrigger, name="dome_trigger_enum", create_type=False),
        nullable=False,
        default=DomeTrigger.SCHEDULED,
        comment="What triggered this dome assembly",
    )

    assembly_version: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        default="2.0.0",
        comment="DOMES assembly engine version that produced this snapshot",
    )

    # ------------------------------------------------------------------
    # COSM Score — Comprehensive Outcome Stability Metric
    # ------------------------------------------------------------------

    cosm_score: Mapped[float | None] = mapped_column(
        Numeric(5, 2),
        nullable=True,
        comment=(
            "COSM composite score 0-100. "
            "0-24: Crisis | 25-49: Fragile | 50-74: Stable | 75-100: Thriving. "
            "Weighted mean of 12 flourishing domain scores."
        ),
    )

    cosm_label: Mapped[str | None] = mapped_column(
        String(32),
        nullable=True,
        comment="Human-readable COSM label: 'Crisis', 'Fragile', 'Stable', or 'Thriving'",
    )

    cosm_delta: Mapped[float | None] = mapped_column(
        Numeric(5, 2),
        nullable=True,
        comment="Change in COSM score since previous dome (+positive = improvement)",
    )

    # ------------------------------------------------------------------
    # Risk scores (structured JSONB)
    # ------------------------------------------------------------------

    risk_scores: Mapped[Any | None] = mapped_column(
        JSONB(),
        nullable=True,
        comment=(
            "Computed risk scores by domain. Schema per key: "
            "{'score': float 0-1, 'level': RiskLevel, 'drivers': [str], "
            "'model_version': str, 'computed_at': ISO8601}. "
            "Keys: crisis_30d, readmission_30d, housing_loss_90d, "
            "substance_relapse_30d, medication_nonadherence_7d, "
            "legal_involvement_30d, child_welfare_involvement_90d"
        ),
    )

    overall_risk_level: Mapped[RiskLevel] = mapped_column(
        Enum(RiskLevel, name="risk_level_enum", create_type=False),
        nullable=False,
        default=RiskLevel.UNKNOWN,
        comment="Highest risk level across all risk_scores domains",
    )

    # ------------------------------------------------------------------
    # Domain scores (12 flourishing domains)
    # ------------------------------------------------------------------

    domain_scores: Mapped[Any | None] = mapped_column(
        JSONB(),
        nullable=True,
        comment=(
            "Scores for each of the 12 FlourishingDomain values. Schema per key: "
            "{'score': float 0-100, 'trend': 'improving'|'stable'|'declining', "
            "'threats': [str], 'supports': [str]}. "
            "Keyed by FlourishingDomain enum values."
        ),
    )

    # ------------------------------------------------------------------
    # Cost analysis
    # ------------------------------------------------------------------

    fragmented_annual_cost: Mapped[Decimal | None] = mapped_column(
        Numeric(precision=12, scale=2),
        nullable=True,
        comment=(
            "Estimated annual cost of current fragmented service delivery (USD). "
            "Robert Jackson example: $112,100 (47 ER visits + shelter + justice + BH)."
        ),
    )

    coordinated_annual_cost: Mapped[Decimal | None] = mapped_column(
        Numeric(precision=12, scale=2),
        nullable=True,
        comment=(
            "Projected annual cost under fully coordinated care (USD). "
            "Robert Jackson example: $41,200 (PSH + ACT team + Medicaid MCO)."
        ),
    )

    delta: Mapped[Decimal | None] = mapped_column(
        Numeric(precision=12, scale=2),
        nullable=True,
        comment=(
            "Annual savings from coordination: fragmented - coordinated (USD). "
            "Positive = savings. Robert Jackson example: $70,900."
        ),
    )

    lifetime_cost_estimate: Mapped[Decimal | None] = mapped_column(
        Numeric(precision=15, scale=2),
        nullable=True,
        comment=(
            "50-year lifetime cost projection at current fragmented rate (USD). "
            "Robert Jackson example: $1,446,360."
        ),
    )

    cost_methodology: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        comment="Description of cost calculation methodology and data sources used",
    )

    # ------------------------------------------------------------------
    # System coverage
    # ------------------------------------------------------------------

    systems_represented: Mapped[Any | None] = mapped_column(
        JSONB(),
        ARRAY(String),
        nullable=True,
        comment="List of GovernmentSystem.system_code values that contributed to this dome",
    )

    systems_missing: Mapped[Any | None] = mapped_column(
        JSONB(),
        ARRAY(String),
        nullable=True,
        comment="Expected systems with no data available at assembly time",
    )

    fragment_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
        comment="Number of fragments assembled into this dome",
    )

    # ------------------------------------------------------------------
    # Recommendations
    # ------------------------------------------------------------------

    recommendations: Mapped[Any | None] = mapped_column(
        JSONB(),
        nullable=True,
        comment=(
            "Prioritized action recommendations. Each item: "
            "{'priority': int, 'domain': FlourishingDomain, "
            "'action': str, 'rationale': str, 'estimated_impact': str, "
            "'system_responsible': str, 'urgency': 'immediate'|'soon'|'routine'}"
        ),
    )

    # ------------------------------------------------------------------
    # Crisis / alert flags
    # ------------------------------------------------------------------

    crisis_flags: Mapped[Any | None] = mapped_column(
        JSONB(),
        ARRAY(String),
        nullable=True,
        comment=(
            "Active crisis flags at assembly time. Examples: "
            "'active_suicidal_ideation', 'medication_lapse_7d', "
            "'housing_loss_imminent', 'glucose_critical', 'unseen_30d'"
        ),
    )

    # ------------------------------------------------------------------
    # Assembly metadata
    # ------------------------------------------------------------------

    assembly_duration_ms: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
        comment="Time in milliseconds the assembly pipeline took to compute this dome",
    )

    assembly_errors: Mapped[Any | None] = mapped_column(
        JSONB(),
        ARRAY(String),
        nullable=True,
        comment="Non-fatal errors encountered during assembly (system unavailabilities, parse failures)",
    )

    assembly_metadata: Mapped[Any | None] = mapped_column(
        JSONB(),
        nullable=True,
        comment="Assembly pipeline diagnostics: data freshness, model confidence, etc.",
    )

    narrative_summary: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        comment=(
            "LLM-generated narrative summary of this person's current situation, "
            "risks, and recommended next actions. Plain English for case managers."
        ),
    )

    # ------------------------------------------------------------------
    # Relationships
    # ------------------------------------------------------------------

    person: Mapped[Person] = relationship(
        "Person",
        back_populates="domes",
        lazy="select",
    )

    # ------------------------------------------------------------------
    # Computed properties
    # ------------------------------------------------------------------

    @property
    def is_crisis(self) -> bool:
        """Return True if this dome indicates a crisis situation."""
        return self.overall_risk_level == RiskLevel.CRITICAL or bool(self.crisis_flags)

    @property
    def savings_percentage(self) -> float | None:
        """Return the percentage savings from coordination vs. fragmented care."""
        if (
            self.fragmented_annual_cost
            and self.delta
            and float(self.fragmented_annual_cost) > 0
        ):
            return round(float(self.delta) / float(self.fragmented_annual_cost) * 100, 1)
        return None

    @property
    def cosm_tier(self) -> str:
        """Return the COSM tier label based on the current score."""
        if self.cosm_score is None:
            return "Unknown"
        score = float(self.cosm_score)
        if score < 25:
            return "Crisis"
        elif score < 50:
            return "Fragile"
        elif score < 75:
            return "Stable"
        else:
            return "Thriving"
