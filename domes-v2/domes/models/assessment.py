"""
DOMES v2 — Assessment Model

Standardized assessments including PHQ-9, GAD-7, AUDIT-C, VI-SPDAT, C-SSRS,
LOCUS, GAF, PANSS. Both total scores and item-level data.

Key assessments for DOMES population:
- PHQ-9: Depression (0-27; Robert Jackson likely scores 15-19 = moderately severe)
- C-SSRS: Suicide risk (required by Joint Commission)
- AUDIT-C: Alcohol use screening (3 items, 0-12)
- VI-SPDAT: Housing vulnerability (0-17; score 8+ = Permanent Supportive Housing)
- GAF: Global functioning (0-100; Robert Jackson likely 20-30 range)
- PANSS: Psychotic symptoms (30-210; high positive symptoms)

HMIS storage: AssessmentResults.csv with assessment_tool_name, total score, date.
FHIR: Observations with survey category (LOINC 44261-6 for PHQ-9).
"""
from __future__ import annotations

import uuid
from datetime import date, datetime
from typing import Any, TYPE_CHECKING

from sqlalchemy import Date, DateTime, Enum, Float, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from domes.enums import AssessmentStatus, AssessmentType
from domes.models.base import (
    AuditMixin,
    DOMESBase,
    FHIRMixin,
    TimestampMixin,
    UUIDPrimaryKeyMixin,
)

if TYPE_CHECKING:
    from domes.models.encounter import Encounter
    from domes.models.fragment import Fragment
    from domes.models.person import Person
    from domes.models.system import GovernmentSystem


class Assessment(
    UUIDPrimaryKeyMixin,
    TimestampMixin,
    AuditMixin,
    FHIRMixin,
    DOMESBase,
):
    """A standardized assessment administered to a person.

    FHIR alignment: Observation (category=survey) with child Observations
    for each item, or QuestionnaireResponse for full item-level capture.

    Key LOINC panel codes:
    - 44261-6: PHQ-9
    - 69737-5: GAD-7
    - 75626-2: AUDIT-C
    - 89201-6: C-SSRS
    - 98968-2: VI-SPDAT (custom / not yet LOINC-standard)

    Item-level data stored in item_responses JSONB:
    [{"item_code": "44250-9", "display": "Little interest...", "value": 3}, ...]
    """

    __tablename__ = "assessment"
    __table_args__ = {
        "comment": (
            "Standardized assessment results (PHQ-9, VI-SPDAT, C-SSRS, GAF, etc.). "
            "Total scores plus item-level responses."
        )
    }

    # ------------------------------------------------------------------
    # Core relations
    # ------------------------------------------------------------------

    person_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("person.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    fragment_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("fragment.id", ondelete="SET NULL"),
        nullable=True,
    )
    encounter_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("encounter.id", ondelete="SET NULL"),
        nullable=True,
        comment="Encounter during which this assessment was administered",
    )
    administered_by_system_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("government_system.id", ondelete="SET NULL"),
        nullable=True,
    )

    # ------------------------------------------------------------------
    # Assessment identity
    # ------------------------------------------------------------------

    assessment_type: Mapped[AssessmentType] = mapped_column(
        Enum(AssessmentType, name="assessment_type_enum"),
        nullable=False,
        index=True,
    )
    assessment_tool_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        comment="Official tool name (e.g., 'PHQ-9', 'VI-SPDAT v2.0', 'C-SSRS')",
    )
    assessment_version: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
        comment="Version of the assessment tool",
    )
    loinc_code: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
        comment="LOINC panel code for this assessment (e.g., '44261-6' for PHQ-9)",
    )

    # ------------------------------------------------------------------
    # Status and timing
    # ------------------------------------------------------------------

    status: Mapped[AssessmentStatus] = mapped_column(
        Enum(AssessmentStatus, name="assessment_status_enum"),
        nullable=False,
        default=AssessmentStatus.COMPLETED,
    )
    assessment_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        index=True,
        comment="Date assessment was administered",
    )
    assessed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        comment="Exact datetime (if available)",
    )
    administered_by: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        comment="Name / role of person who administered the assessment",
    )

    # ------------------------------------------------------------------
    # Scores
    # ------------------------------------------------------------------

    total_score: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
        comment="Total/composite score",
    )
    score_min: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
        comment="Minimum possible score for this tool",
    )
    score_max: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
        comment="Maximum possible score for this tool",
    )
    severity_classification: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        comment=(
            "Severity based on score thresholds. "
            "PHQ-9: None/Mild/Moderate/Moderately Severe/Severe. "
            "VI-SPDAT: Diversion/Rapid Re-Housing/PSH. "
            "GAF: 0-100 scale."
        ),
    )
    subscale_scores: Mapped[Any | None] = mapped_column(
        JSONB(),
        nullable=True,
        comment=(
            "Subscale scores for multi-domain tools. "
            "PANSS: {'positive': 28, 'negative': 22, 'general': 45}. "
            "VI-SPDAT: {'history': 3, 'risks': 4, 'socialization': 3, 'wellness': 4}."
        ),
    )

    # ------------------------------------------------------------------
    # Item-level responses
    # ------------------------------------------------------------------

    item_responses: Mapped[Any | None] = mapped_column(
        JSONB(),
        nullable=True,
        comment=(
            "Array of individual item responses. "
            "Structure: [{'item_code': '44250-9', 'display': '...', 'value': 3, 'loinc_code': '44250-9'}, ...]. "
            "PHQ-9 item 9 (suicidality = code 44260-8) is flagged separately."
        ),
    )
    suicidality_flag: Mapped[bool | None] = mapped_column(
        nullable=True,
        comment=(
            "True if assessment indicates active suicidal ideation. "
            "PHQ-9 Q9 score > 0 or C-SSRS active ideation = True."
        ),
    )

    # ------------------------------------------------------------------
    # HMIS-specific fields (for VI-SPDAT, SPDAT)
    # ------------------------------------------------------------------

    hmis_assessment_id: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        comment="HMIS AssessmentID (for coordinated entry assessments)",
    )
    prioritization_status: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
        comment="HMIS PrioritizationStatus: 1=Placed on prioritization list",
    )
    housing_recommendation: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        comment="Housing intervention recommendation from VI-SPDAT/SPDAT score",
    )

    # ------------------------------------------------------------------
    # Notes
    # ------------------------------------------------------------------

    clinical_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    metadata_: Mapped[Any | None] = mapped_column(
        "metadata",
        JSONB(),
        nullable=True,
    )

    # ------------------------------------------------------------------
    # Relationships
    # ------------------------------------------------------------------

    person: Mapped["Person"] = relationship(
        "Person",
        back_populates="assessments",
        lazy="select",
    )
    fragment: Mapped["Fragment | None"] = relationship(
        "Fragment",
        lazy="select",
    )
    encounter: Mapped["Encounter | None"] = relationship(
        "Encounter",
        lazy="select",
    )
    administered_by_system: Mapped["GovernmentSystem | None"] = relationship(
        "GovernmentSystem",
        lazy="select",
    )
