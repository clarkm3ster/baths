"""
DOMES v2 — Condition Model

Diagnoses, problem list items, and SDOH conditions.
Aligns with FHIR Condition resource and US Core Condition profile.

Covers:
- Clinical diagnoses (ICD-10)
- Chronic conditions (diabetes, hypertension, SMI)
- Mental health/substance use diagnoses (DSM-5/ICD-10)
- SDOH conditions (food insecurity, housing instability, etc.)
- Disabilities (affects program eligibility)

FHIR alignment: https://hl7.org/fhir/R4/condition.html
US Core Condition: https://hl7.org/fhir/us/core/StructureDefinition-us-core-condition.html
"""
from __future__ import annotations

import uuid
from datetime import date, datetime
from typing import Any, TYPE_CHECKING

from sqlalchemy import Date, DateTime, Enum, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
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
    from domes.models.person import Person


class Condition(
    UUIDPrimaryKeyMixin,
    TimestampMixin,
    AuditMixin,
    FHIRMixin,
    DOMESBase,
):
    """A clinical, behavioral, or SDOH condition.

    Maps to FHIR Condition resource. Covers problem list items,
    encounter diagnoses, health concerns, and SDOH conditions.
    """

    __tablename__ = "condition"
    __table_args__ = {
        "comment": (
            "Diagnoses, problem list items, and SDOH conditions. "
            "Follows FHIR Condition R4 / US Core Condition profile."
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

    # ------------------------------------------------------------------
    # FHIR Condition.code
    # ------------------------------------------------------------------

    code: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
        comment="Condition code (ICD-10-CM, SNOMED, or custom)",
    )
    code_system: Mapped[CodeSystem] = mapped_column(
        Enum(CodeSystem, name="condition_code_system_enum"),
        nullable=False,
        default=CodeSystem.ICD_10_CM,
        comment="Coding system for condition code",
    )
    code_display: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
        comment="Human-readable name of the condition",
    )

    # ------------------------------------------------------------------
    # FHIR Condition.category
    # ------------------------------------------------------------------

    category: Mapped[ConditionCategory] = mapped_column(
        Enum(ConditionCategory, name="condition_category_enum"),
        nullable=False,
        default=ConditionCategory.PROBLEM_LIST_ITEM,
        comment="FHIR condition category",
    )

    # ------------------------------------------------------------------
    # FHIR Condition.clinicalStatus / verificationStatus / severity
    # ------------------------------------------------------------------

    clinical_status: Mapped[ConditionClinicalStatus] = mapped_column(
        Enum(ConditionClinicalStatus, name="condition_clinical_status_enum"),
        nullable=False,
        default=ConditionClinicalStatus.ACTIVE,
        comment="FHIR condition-clinical status (active, remission, resolved, etc.)",
    )
    verification_status: Mapped[ConditionVerificationStatus] = mapped_column(
        Enum(ConditionVerificationStatus, name="condition_verification_status_enum"),
        nullable=False,
        default=ConditionVerificationStatus.CONFIRMED,
        comment="FHIR condition-ver-status (confirmed, provisional, refuted, etc.)",
    )
    severity: Mapped[ConditionSeverity | None] = mapped_column(
        Enum(ConditionSeverity, name="condition_severity_enum"),
        nullable=True,
        comment="Condition severity (mild, moderate, severe, critical)",
    )

    # ------------------------------------------------------------------
    # FHIR Condition.onset[x] / abatement[x]
    # ------------------------------------------------------------------

    onset_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
        comment="Date of onset (FHIR onsetDateTime / onsetPeriod.start)",
    )
    abatement_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
        comment="Date condition resolved / went into remission",
    )
    recorded_date: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        comment="When this condition was recorded in the source system",
    )

    # ------------------------------------------------------------------
    # Clinical notes / evidence
    # ------------------------------------------------------------------

    notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        comment="Clinical notes about this condition",
    )
    evidence_summary: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        comment="Summary of evidence supporting this condition",
    )

    # ------------------------------------------------------------------
    # Source provenance
    # ------------------------------------------------------------------

    source_fragment_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        nullable=True,
        comment="Fragment that produced this condition record",
    )
    source_system_name: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    # ------------------------------------------------------------------
    # Relationships
    # ------------------------------------------------------------------

    person: Mapped["Person"] = relationship(
        "Person",
        back_populates="conditions",
        lazy="select",
    )
