"""
DOMES v2 — Condition Model

Diagnoses, problems, and social determinants of health (SDOH conditions).
FHIR-aligned with US Core Condition profile.

ICD-10 codes critical for DOMES (Robert Jackson example):
- F25.0: Schizoaffective disorder, bipolar type
- Z59.0: Homelessness (SDOH condition — Gravity Project)
- F11.20: Opioid use disorder, moderate
- F10.20: Alcohol use disorder, moderate
- F19.20: Multiple substance use disorder
- Z65.3: Problems related to other legal circumstances

42 CFR Part 2 note: ICD-10 F10-F19 (substance use disorders) require
the DS4P security label 'SBUD' or 'ETHUD' / 'OPIOIDUD' to indicate
42 CFR Part 2 protection. These conditions CANNOT be shared without a valid
42 CFR Part 2 consent form.
"""
from __future__ import annotations

import uuid
from datetime import date, datetime
from typing import Any, TYPE_CHECKING

from sqlalchemy import JSON, Boolean, Date, DateTime, Enum, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from domes.enums import (
    CodeSystem,
    ConditionCategory,
    ConditionClinicalStatus,
    ConditionSeverity,
    ConditionVerificationStatus,
)
from domes.models.base import (
    AuditMixin,
    DOMESBase,
    FHIRMixin,
    TimestampMixin,
    UUIDPrimaryKeyMixin,
)

if TYPE_CHECKING:
    from domes.models.fragment import Fragment
    from domes.models.person import Person
    from domes.models.system import GovernmentSystem


class Condition(
    UUIDPrimaryKeyMixin,
    TimestampMixin,
    AuditMixin,
    FHIRMixin,
    DOMESBase,
):
    """A diagnosis, problem, or social determinant of health.

    FHIR resource type: Condition
    US Core profiles:
    - us-core-condition-problems-health-concerns
    - SDOHCC-Condition (Gravity Project SDOH conditions)

    Covers clinical diagnoses (F25.0, F11.20) AND social conditions (Z59.0, Z59.4).
    Both use ICD-10-CM coding but different category flags.

    42 CFR Part 2 sensitivity: Conditions with ICD-10 codes F10-F19 must have
    is_42cfr_protected = True and sensitivity_label set.
    """

    __tablename__ = "condition"
    __table_args__ = {
        "comment": (
            "Clinical diagnoses and SDOH conditions (FHIR Condition). "
            "ICD-10 coded. F10-F19 codes are 42 CFR Part 2 protected."
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
    recording_system_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("government_system.id", ondelete="SET NULL"),
        nullable=True,
        comment="System that recorded this condition",
    )

    # ------------------------------------------------------------------
    # FHIR Condition status
    # ------------------------------------------------------------------

    clinical_status: Mapped[ConditionClinicalStatus] = mapped_column(
        Enum(ConditionClinicalStatus, name="condition_clinical_status_enum"),
        nullable=False,
        default=ConditionClinicalStatus.ACTIVE,
    )
    verification_status: Mapped[ConditionVerificationStatus] = mapped_column(
        Enum(ConditionVerificationStatus, name="condition_verification_status_enum"),
        nullable=False,
        default=ConditionVerificationStatus.CONFIRMED,
    )
    category: Mapped[ConditionCategory] = mapped_column(
        Enum(ConditionCategory, name="condition_category_enum"),
        nullable=False,
        default=ConditionCategory.PROBLEM_LIST_ITEM,
    )
    severity: Mapped[ConditionSeverity | None] = mapped_column(
        Enum(ConditionSeverity, name="condition_severity_enum"),
        nullable=True,
    )

    # ------------------------------------------------------------------
    # Coding
    # ------------------------------------------------------------------

    code_system: Mapped[CodeSystem] = mapped_column(
        Enum(CodeSystem, name="condition_code_system_enum"),
        nullable=False,
        default=CodeSystem.ICD_10_CM,
    )
    code: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
        comment="ICD-10-CM or SNOMED CT code",
    )
    code_display: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
        comment="Human-readable condition name",
    )
    additional_codes: Mapped[Any | None] = mapped_column(
        JSON(),
        ARRAY(String),
        nullable=True,
        comment="Additional coding (e.g., SNOMED codes alongside ICD-10)",
    )

    # ------------------------------------------------------------------
    # Temporal
    # ------------------------------------------------------------------

    onset_datetime: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        comment="When the condition began (if exact time known)",
    )
    onset_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
        comment="When the condition began (date precision)",
    )
    onset_string: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        comment="Free-text onset description (e.g., 'childhood', 'after 2022 incarceration')",
    )
    abatement_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
        comment="When the condition resolved or went into remission",
    )
    recorded_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
        comment="When this condition was entered into the system",
    )

    # ------------------------------------------------------------------
    # Clinical context
    # ------------------------------------------------------------------

    recorder: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        comment="Name / role of the clinician or worker who recorded this condition",
    )
    note: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        comment="Clinical notes about this condition",
    )
    is_primary_diagnosis: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        comment="True if this is the primary/principal diagnosis",
    )
    is_chronic: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        comment="True for chronic conditions (schizoaffective disorder, diabetes, etc.)",
    )

    # ------------------------------------------------------------------
    # Privacy / sensitivity
    # ------------------------------------------------------------------

    is_42cfr_protected: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        comment=(
            "True for ICD-10 F10-F19 (substance use disorders). "
            "Requires 42 CFR Part 2 consent before disclosure. "
            "Should be auto-set by the assembly service based on code."
        ),
    )
    sensitivity_label: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
        comment=(
            "DS4P security label: 'ETHUD', 'OPIOIDUD', 'SBUD' (substance use), "
            "'PSY' (psychiatric), 'HIV'. Set for 42 CFR Part 2 protected conditions."
        ),
    )
    is_mental_health: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        comment="True for mental health diagnoses (F20-F99)",
    )
    is_sdoh: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        comment="True for SDOH conditions (Z-codes: Z59.x housing, Z59.4 food, etc.)",
    )

    # ------------------------------------------------------------------
    # Relationships
    # ------------------------------------------------------------------

    person: Mapped["Person"] = relationship(
        "Person",
        back_populates="conditions",
        lazy="select",
    )
    fragment: Mapped["Fragment | None"] = relationship(
        "Fragment",
        lazy="select",
    )
    recording_system: Mapped["GovernmentSystem | None"] = relationship(
        "GovernmentSystem",
        lazy="select",
    )
