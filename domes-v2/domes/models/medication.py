"""
DOMES v2 — Medication Model

Medication records — prescriptions, fills, and adherence tracking.
Covers psychiatric medications, MAT, and chronic disease management.

FHIR alignment: maps to FHIR MedicationRequest resource.
FHIR MedicationRequest: https://hl7.org/fhir/R4/medicationrequest.html
"""
from __future__ import annotations

import uuid
from datetime import date, datetime
from typing import Any, TYPE_CHECKING

from sqlalchemy import Boolean, Date, DateTime, Enum, Float, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from domes.enums import (
    AdherenceStatus,
    CodeSystem,
    MedicationCategory,
    MedicationStatus,
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


class Medication(
    UUIDPrimaryKeyMixin,
    TimestampMixin,
    AuditMixin,
    FHIRMixin,
    DOMESBase,
):
    """A medication prescription, fill, or active regimen.

    Maps to FHIR MedicationRequest resource. Covers all medication types
    across all system domains: psychiatric, MAT, chronic disease, etc.
    """

    __tablename__ = "medication"
    __table_args__ = {
        "comment": (
            "Medication prescriptions and fills. "
            "Follows FHIR MedicationRequest R4 structure."
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
    # Medication identification
    # ------------------------------------------------------------------

    rxnorm_code: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
        index=True,
        comment="RxNorm code for the medication",
    )
    ndc_code: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
        comment="NDC (National Drug Code) for the specific fill",
    )
    medication_name: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
        comment="Generic or brand name of the medication",
    )
    category: Mapped[MedicationCategory] = mapped_column(
        Enum(MedicationCategory, name="medication_category_enum"),
        nullable=False,
        default=MedicationCategory.OTHER,
        comment="High-level therapeutic category for DOMES analysis",
    )

    # ------------------------------------------------------------------
    # Status and timing
    # ------------------------------------------------------------------

    status: Mapped[MedicationStatus] = mapped_column(
        Enum(MedicationStatus, name="medication_status_enum"),
        nullable=False,
        default=MedicationStatus.ACTIVE,
        comment="FHIR MedicationRequest.status",
    )
    start_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
        comment="When the prescription was started",
    )
    end_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
        comment="When the prescription ended / was discontinued",
    )
    prescribed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        comment="When this prescription was written",
    )

    # ------------------------------------------------------------------
    # Dosing
    # ------------------------------------------------------------------

    dose_quantity: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
        comment="Dose amount",
    )
    dose_unit: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
        comment="Dose unit (mg, mL, units, etc.)",
    )
    frequency: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        comment="Dosing frequency (e.g., 'daily', 'BID', 'as needed')",
    )
    route: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        comment="Route of administration (oral, IM, IV, etc.)",
    )
    days_supply: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
        comment="Days supply per fill",
    )

    # ------------------------------------------------------------------
    # Adherence
    # ------------------------------------------------------------------

    adherence_status: Mapped[AdherenceStatus] = mapped_column(
        Enum(AdherenceStatus, name="adherence_status_enum"),
        nullable=False,
        default=AdherenceStatus.UNABLE_TO_ASSESS,
        comment="Medication adherence classification",
    )
    pdc: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
        comment=(
            "Proportion of Days Covered (0.0-1.0). "
            "PDC >= 0.80 = adherent by standard pharmacy metrics."
        ),
    )
    last_fill_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
        comment="Date of most recent pharmacy fill",
    )
    days_since_last_fill: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
        comment="Days since most recent fill (computed)",
    )

    # ------------------------------------------------------------------
    # MAT-specific fields
    # ------------------------------------------------------------------

    is_mat: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        comment="Is this a Medication Assisted Treatment medication (methadone, buprenorphine, naltrexone)?",
    )
    mat_program_name: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        comment="Name of the MAT program (if applicable)",
    )

    # ------------------------------------------------------------------
    # Prescriber
    # ------------------------------------------------------------------

    prescriber_name: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )
    prescriber_npi: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )

    # ------------------------------------------------------------------
    # Source provenance
    # ------------------------------------------------------------------

    source_fragment_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        nullable=True,
        comment="Fragment that produced this medication record",
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
        back_populates="medications",
        lazy="select",
    )
