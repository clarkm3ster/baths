"""
DOMES v2 — Dome Model (Assembled Digital Twin Snapshot)

The Dome is a computed, point-in-time snapshot of a person's full digital twin.
It is the central artifact that the DOMES system produces.

A Dome assembles data from all sources:
- Clinical: diagnoses, medications, assessments, encounters
- Benefits: enrollments, housing, income support
- Biometrics: real-time vitals, sleep, activity
- Social: relationships, community support, barriers
- Environmental: neighborhood conditions, air quality

Key computed fields:
- flourishing_score: 0-100 composite wellbeing score
- crisis_probability_30d: ML prediction of crisis in next 30 days
- system_involvement_count: number of active government systems
- cosm_score: Coordination of Systems Metric (0-100)

The Dome is recomputed:
- On new fragment ingestion
- On scheduled refresh (daily for high-risk persons)
- On explicit API request
"""
from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any, TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from domes.models.base import (
    AuditMixin,
    DOMESBase,
    TimestampMixin,
    UUIDPrimaryKeyMixin,
)

if TYPE_CHECKING:
    from domes.models.flourishing import FlourishingScore
    from domes.models.person import Person


class Dome(
    UUIDPrimaryKeyMixin,
    TimestampMixin,
    AuditMixin,
    DOMESBase,
):
    """Assembled digital twin snapshot for a person at a point in time.

    A Dome is immutable once created. New data triggers a new Dome version.
    The latest Dome for a person is the current digital twin.

    Storage: The full assembled data is stored in `full_snapshot` JSONB.
    Computed scores are denormalized into columns for fast querying.
    """

    __tablename__ = "dome"
    __table_args__ = {
        "comment": (
            "Assembled digital twin snapshots. One row = one point-in-time view "
            "of a person's full DOMES profile. Immutable after creation."
        )
    }

    # ------------------------------------------------------------------
    # Person link
    # ------------------------------------------------------------------

    person_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("person.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # ------------------------------------------------------------------
    # Version / assembly metadata
    # ------------------------------------------------------------------

    version: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=1,
        comment="Incremental version number for this person's dome sequence",
    )
    assembled_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        comment="Timestamp when this dome was assembled",
    )
    assembly_trigger: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        comment="What triggered assembly: 'fragment_ingestion', 'scheduled', 'api_request'",
    )
    is_current: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        comment="True if this is the most recent dome for this person",
    )
    data_currency_hours: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
        comment="Age of oldest data source used in assembly (hours)",
    )
    fragment_count: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
        comment="Number of fragments incorporated into this dome",
    )

    # ------------------------------------------------------------------
    # Flourishing score (primary output)
    # ------------------------------------------------------------------

    flourishing_score: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
        comment="Overall flourishing score 0-100 (higher = better)",
    )
    flourishing_score_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("flourishing_score.id", ondelete="SET NULL"),
        nullable=True,
        comment="FK to detailed per-domain flourishing score",
    )
    flourishing_delta_7d: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
        comment="Change in flourishing score over past 7 days",
    )
    flourishing_delta_30d: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
        comment="Change in flourishing score over past 30 days",
    )

    # ------------------------------------------------------------------
    # Crisis prediction (ML output)
    # ------------------------------------------------------------------

    crisis_probability_30d: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
        comment="ML probability of crisis event in next 30 days (0.0-1.0)",
    )
    crisis_probability_90d: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
        comment="ML probability of crisis event in next 90 days (0.0-1.0)",
    )
    crisis_risk_level: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
        comment="Risk level: LOW/MEDIUM/HIGH/CRITICAL based on crisis_probability",
    )
    crisis_drivers: Mapped[Any | None] = mapped_column(
        JSONB(),
        nullable=True,
        comment="Top crisis risk factors from ML model",
    )

    # ------------------------------------------------------------------
    # COSM score (system coordination)
    # ------------------------------------------------------------------

    cosm_score: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
        comment="Coordination of Systems Metric 0-100 (higher = better coordination)",
    )
    cosm_components: Mapped[Any | None] = mapped_column(
        JSONB(),
        nullable=True,
        comment="Per-system COSM breakdown",
    )
    system_involvement_count: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
        comment="Number of active government systems",
    )
    active_system_ids: Mapped[Any | None] = mapped_column(
        JSONB(),
        nullable=True,
        comment="Array of UUIDs of active government systems",
    )

    # ------------------------------------------------------------------
    # Data quality
    # ------------------------------------------------------------------

    data_completeness_score: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
        comment="Fraction of expected data domains present (0.0-1.0)",
    )
    gap_count: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
        comment="Number of active data gaps affecting this dome",
    )
    biometric_freshness_hours: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
        comment="Hours since last biometric reading",
    )

    # ------------------------------------------------------------------
    # Key clinical indicators (denormalized for fast access)
    # ------------------------------------------------------------------

    active_diagnoses_count: Mapped[int | None] = mapped_column(Integer, nullable=True)
    active_medications_count: Mapped[int | None] = mapped_column(Integer, nullable=True)
    last_encounter_days_ago: Mapped[float | None] = mapped_column(Float, nullable=True)
    housing_status: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
        comment="Current housing status: housed/unstably_housed/homeless",
    )
    medicaid_active: Mapped[bool | None] = mapped_column(nullable=True)
    suicidality_flag: Mapped[bool | None] = mapped_column(
        nullable=True,
        comment="True if any recent assessment indicates suicidal ideation",
    )

    # ------------------------------------------------------------------
    # Full snapshot (the dome payload)
    # ------------------------------------------------------------------

    full_snapshot: Mapped[Any | None] = mapped_column(
        JSONB(),
        nullable=True,
        comment="Complete assembled digital twin as JSON (for API responses)",
    )
    summary: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        comment="Natural language summary of this person's current state",
    )

    # ------------------------------------------------------------------
    # Relationships
    # ------------------------------------------------------------------

    person: Mapped["Person"] = relationship(
        "Person",
        back_populates="domes",
        lazy="select",
    )
    flourishing_score_obj: Mapped["FlourishingScore | None"] = relationship(
        "FlourishingScore",
        foreign_keys=[flourishing_score_id],
        lazy="select",
    )

    # ------------------------------------------------------------------
    # Computed properties
    # ------------------------------------------------------------------

    @property
    def risk_category(self) -> str:
        """Return human-readable risk category."""
        p = self.crisis_probability_30d or 0.0
        if p >= 0.7:
            return "CRITICAL"
        elif p >= 0.4:
            return "HIGH"
        elif p >= 0.2:
            return "MEDIUM"
        else:
            return "LOW"

    @property
    def flourishing_tier(self) -> str:
        """Return flourishing tier label."""
        score = self.flourishing_score or 0.0
        if score < 25:
            return "Crisis"
        elif score < 50:
            return "Struggling"
        elif score < 75:
            return "Stable"
        else:
            return "Thriving"
