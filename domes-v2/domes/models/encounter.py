"""
DOMES v2 — Encounter Model

An Encounter is any contact between a person and the service system.
This covers medical, behavioral health, housing, justice, outreach, and
civil encounters — essentially any recorded service interaction.

FHIR alignment: maps to FHIR Encounter resource.
FHIR Encounter: https://hl7.org/fhir/R4/encounter.html
"""
from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any, TYPE_CHECKING

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from domes.enums import (
    EncounterClass,
    EncounterStatus,
    EncounterType,
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


class Encounter(
    UUIDPrimaryKeyMixin,
    TimestampMixin,
    AuditMixin,
    FHIRMixin,
    DOMESBase,
):
    """A service encounter between a person and the service system.

    Covers all encounter types across all 9+ government systems:
    medical, behavioral health, housing, justice, outreach, etc.
    Follows FHIR Encounter R4 structure.
    """

    __tablename__ = "encounter"
    __table_args__ = {
        "comment": (
            "Service encounters across all system types. "
            "Follows FHIR Encounter R4 structure."
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
    # Classification
    # ------------------------------------------------------------------

    encounter_class: Mapped[EncounterClass] = mapped_column(
        Enum(EncounterClass, name="encounter_class_enum"),
        nullable=False,
        comment="FHIR v3-ActCode encounter class (setting)",
    )
    encounter_type: Mapped[EncounterType] = mapped_column(
        Enum(EncounterType, name="encounter_type_enum"),
        nullable=False,
        comment="DOMES-specific encounter type taxonomy",
    )
    status: Mapped[EncounterStatus] = mapped_column(
        Enum(EncounterStatus, name="encounter_status_enum"),
        nullable=False,
        default=EncounterStatus.COMPLETED,
        comment="FHIR Encounter.status",
    )

    # ------------------------------------------------------------------
    # Timing
    # ------------------------------------------------------------------

    start_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        index=True,
        comment="When the encounter started",
    )
    end_time: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        comment="When the encounter ended (NULL if still in progress)",
    )
    length_minutes: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
        comment="Duration in minutes (if known)",
    )

    # ------------------------------------------------------------------
    # Location / provider
    # ------------------------------------------------------------------

    facility_name: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        comment="Name of the facility / location",
    )
    facility_type: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        comment="Type of facility (hospital, clinic, shelter, jail, etc.)",
    )
    city: Mapped[str | None] = mapped_column(String(100), nullable=True)
    state: Mapped[str | None] = mapped_column(String(2), nullable=True)
    provider_name: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        comment="Primary provider name (physician, case manager, officer, etc.)",
    )
    provider_npi: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
        comment="NPI of the provider (for medical encounters)",
    )

    # ------------------------------------------------------------------
    # Clinical content
    # ------------------------------------------------------------------

    chief_complaint: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        comment="Chief complaint or reason for encounter",
    )
    diagnosis_codes: Mapped[Any | None] = mapped_column(
        JSONB(),
        nullable=True,
        comment="Array of ICD-10 diagnosis codes and display names",
    )
    procedure_codes: Mapped[Any | None] = mapped_column(
        JSONB(),
        nullable=True,
        comment="Array of CPT/HCPCS procedure codes",
    )
    disposition: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        comment="Encounter disposition (discharged, admitted, released, etc.)",
    )
    notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        comment="Encounter notes",
    )

    # ------------------------------------------------------------------
    # Source provenance
    # ------------------------------------------------------------------

    source_fragment_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        nullable=True,
        comment="Fragment that produced this encounter record",
    )
    source_system_name: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )
    source_encounter_id: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        comment="Original encounter ID in the source system",
    )

    # ------------------------------------------------------------------
    # Relationships
    # ------------------------------------------------------------------

    person: Mapped["Person"] = relationship(
        "Person",
        back_populates="encounters",
        lazy="select",
    )
