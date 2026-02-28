"""
DOMES v2 — Medication Model

Medication records — prescriptions, fills, and adherence tracking.
FHIR-aligned with MedicationRequest resource and US Core Medication profile.

For Robert Jackson, key medications:
- Clozapine or risperidone (antipsychotic — requires regular blood monitoring)
- Lithium or valproate (mood stabilizer)
- Possibly buprenorphine/naloxone (MAT if OUD present)

Medication adherence is critical for schizoaffective disorder management.
Non-adherence is a primary predictor of psychiatric crisis and ER visits.
"""
from __future__ import annotations

import uuid
from datetime import date
from typing import Any, TYPE_CHECKING

from sqlalchemy import Boolean, Date, Enum, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from domes.enums import (
    AdherenceStatus,
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
    from domes.models.fragment import Fragment
    from domes.models.person import Person
    from domes.models.system import GovernmentSystem


class Medication(
    UUIDPrimaryKeyMixin,
    TimestampMixin,
    AuditMixin,
    FHIRMixin,
    DOMESBase,
):
    """A medication prescription record.

    FHIR resource type: MedicationRequest
    US Core profile: us-core-medicationrequest

    Tracks both the prescription (ordered) and adherence (actual taking).
    Links to PDMP (Prescription Drug Monitoring Program) data via fragment.

    MAT (Medication-Assisted Treatment) for opioid use disorder:
    - Methadone (opioid treatment program only)
    - Buprenorphine/naloxone (Suboxone) — office-based
    - Naltrexone (Vivitrol) — monthly injection
    These require special handling under 42 CFR Part 2.
    """

    __tablename__ = "medication"
    __table_args__ = {
        "comment": (
            "Medication prescription records (FHIR MedicationRequest). "
            "Tracks adherence status for schizoaffective disorder management."
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
    prescribing_system_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("government_system.id", ondelete="SET NULL"),
        nullable=True,
    )

    # ------------------------------------------------------------------
    # Medication identity (RxNorm)
    # ------------------------------------------------------------------

    rxnorm_code: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
        index=True,
        comment="RxNorm concept ID (e.g., '1049502' for buprenorphine 8mg)",
    )
    drug_name: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
        comment="Generic drug name",
    )
    brand_name: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        comment="Brand/trade name",
    )
    ndc_code: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
        comment="National Drug Code (11-digit)",
    )
    category: Mapped[MedicationCategory] = mapped_column(
        Enum(MedicationCategory, name="medication_category_enum"),
        nullable=False,
        default=MedicationCategory.OTHER,
    )

    # ------------------------------------------------------------------
    # Dosage
    # ------------------------------------------------------------------

    dose_quantity: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        comment="Dose amount and unit (e.g., '400 mg', '8/2 mg')",
    )
    dose_frequency: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        comment="Dosing frequency (e.g., 'once daily', 'BID', 'monthly injection')",
    )
    route: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        comment="Route of administration (oral, IM, sublingual, transdermal, etc.)",
    )
    instructions: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        comment="Patient instructions / SIG",
    )

    # ------------------------------------------------------------------
    # Status and dates
    # ------------------------------------------------------------------

    status: Mapped[MedicationStatus] = mapped_column(
        Enum(MedicationStatus, name="medication_status_enum"),
        nullable=False,
        default=MedicationStatus.ACTIVE,
    )
    authorized_on: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
        comment="Date prescription was authorized",
    )
    effective_from: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
        comment="Date medication was started",
    )
    effective_to: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
        comment="Date medication was stopped or completed",
    )
    last_fill_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
        comment="Date of last pharmacy fill (from PDMP or pharmacy claims)",
    )
    days_supply: Mapped[int | None] = mapped_column(
        nullable=True,
        comment="Days supply per fill",
    )
    refills_authorized: Mapped[int | None] = mapped_column(
        nullable=True,
        comment="Number of refills authorized on the prescription",
    )

    # ------------------------------------------------------------------
    # Adherence tracking
    # ------------------------------------------------------------------

    adherence_status: Mapped[AdherenceStatus] = mapped_column(
        Enum(AdherenceStatus, name="adherence_status_enum"),
        nullable=False,
        default=AdherenceStatus.UNABLE_TO_ASSESS,
        comment="Current medication adherence classification",
    )
    adherence_score: Mapped[float | None] = mapped_column(
        nullable=True,
        comment=(
            "Medication Possession Ratio (MPR) or similar adherence metric. "
            "0.0-1.0. MPR >= 0.8 = adherent. Computed from fill dates."
        ),
    )
    adherence_notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        comment="Clinical notes about adherence challenges",
    )

    # ------------------------------------------------------------------
    # Prescriber
    # ------------------------------------------------------------------

    prescriber_name: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )
    prescriber_role: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        comment="Prescriber's role (psychiatrist, NP, ACT team physician, etc.)",
    )
    prescriber_npi: Mapped[str | None] = mapped_column(
        String(10),
        nullable=True,
        comment="Prescriber's National Provider Identifier",
    )

    # ------------------------------------------------------------------
    # Privacy
    # ------------------------------------------------------------------

    is_mat: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        comment=(
            "True if this is Medication-Assisted Treatment (methadone, buprenorphine, "
            "naltrexone for OUD). MAT records are 42 CFR Part 2 protected."
        ),
    )
    is_42cfr_protected: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        comment="42 CFR Part 2 protection flag — required for MAT medications",
    )
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
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
        back_populates="medications",
        lazy="select",
    )
    fragment: Mapped["Fragment | None"] = relationship(
        "Fragment",
        lazy="select",
    )
    prescribing_system: Mapped["GovernmentSystem | None"] = relationship(
        "GovernmentSystem",
        lazy="select",
    )
