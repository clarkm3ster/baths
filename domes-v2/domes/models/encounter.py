"""
DOMES v2 — Encounter Model

An Encounter is any contact between a person and a system — clinical, social,
or justice. DOMES tracks the full spectrum of encounters because the pattern
of encounters IS the digital twin in action.

For Robert Jackson: 47 ER visits/year = 47 Encounters of type ER_VISIT.
These encounters drive the dome assembly and cost calculation.

Types tracked:
- ER visits (emergency department)
- Psychiatric hospitalizations
- Shelter stays (HMIS bed nights)
- Jail bookings / releases
- Mobile crisis responses
- ACT team contacts
- Probation check-ins
- Court appearances
- Clinic visits
- Telehealth calls
- Street outreach contacts

FHIR alignment: Encounter resource
"""
from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any, TYPE_CHECKING

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import ARRAY, JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from domes.enums import EncounterClass, EncounterStatus, EncounterType
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


class Encounter(
    UUIDPrimaryKeyMixin,
    TimestampMixin,
    AuditMixin,
    FHIRMixin,
    DOMESBase,
):
    """A single contact between a person and a system or service.

    FHIR resource type: Encounter

    Encounters are the primary driver of the fragmented cost calculation.
    The pattern of ER visits, hospitalizations, and shelter stays reveals
    the true cost of uncoordinated care.

    Key relationships:
    - Many encounters → one Person
    - Each encounter → one source GovernmentSystem
    - Each encounter → optional originating Fragment
    """

    __tablename__ = "encounter"
    __table_args__ = {
        "comment": (
            "Clinical, social, and justice system contacts. "
            "47 ER visits/year (Robert Jackson) = 47 rows here. "
            "Drives the fragmented cost calculation."
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
    source_system_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("government_system.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
        comment="System that recorded this encounter",
    )

    # ------------------------------------------------------------------
    # FHIR Encounter fields
    # ------------------------------------------------------------------

    status: Mapped[EncounterStatus] = mapped_column(
        Enum(EncounterStatus, name="encounter_status_enum"),
        nullable=False,
        default=EncounterStatus.COMPLETED,
    )
    encounter_class: Mapped[EncounterClass] = mapped_column(
        Enum(EncounterClass, name="encounter_class_enum"),
        nullable=False,
        comment="FHIR v3-ActCode encounter class (AMB, IMP, EMER, etc.)",
    )
    encounter_type: Mapped[EncounterType] = mapped_column(
        Enum(EncounterType, name="encounter_type_enum"),
        nullable=False,
        comment="DOMES-specific encounter type taxonomy",
    )

    # ------------------------------------------------------------------
    # Timing
    # ------------------------------------------------------------------

    period_start: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        index=True,
        comment="Start of the encounter",
    )
    period_end: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        comment="End of the encounter (NULL = still in progress)",
    )
    length_of_stay_days: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
        comment="Length of stay in days (computed from period for inpatient/shelter)",
    )

    # ------------------------------------------------------------------
    # Clinical content
    # ------------------------------------------------------------------

    reason_codes: Mapped[Any | None] = mapped_column(
        JSONB(),
        ARRAY(String),
        nullable=True,
        comment="ICD-10 or SNOMED codes for why this encounter occurred",
    )
    reason_display: Mapped[str | None] = mapped_column(
        String(1000),
        nullable=True,
        comment="Human-readable reason(s) for this encounter",
    )
    chief_complaint: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        comment="Patient's stated chief complaint",
    )
    discharge_disposition_code: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
        comment="FHIR discharge disposition code",
    )
    discharge_disposition_display: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        comment="Human-readable discharge disposition (e.g., 'Returned to homelessness')",
    )

    # ------------------------------------------------------------------
    # Location
    # ------------------------------------------------------------------

    location_name: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        comment="Name of facility or location (e.g., 'Rush University Medical Center ER')",
    )
    location_type: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        comment="Type of location (e.g., 'hospital', 'shelter', 'jail', 'street')",
    )
    location_city: Mapped[str | None] = mapped_column(String(100), nullable=True)
    location_state: Mapped[str | None] = mapped_column(String(2), nullable=True)

    # ------------------------------------------------------------------
    # Cost
    # ------------------------------------------------------------------

    estimated_cost: Mapped[float | None] = mapped_column(
        nullable=True,
        comment="Estimated cost of this encounter (USD) — for fragmented cost calculation",
    )
    actual_cost: Mapped[float | None] = mapped_column(
        nullable=True,
        comment="Actual billed/paid cost if available from claims data",
    )
    payer: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        comment="Primary payer (Medicaid, Medicare, VA, Uninsured, etc.)",
    )

    # ------------------------------------------------------------------
    # Notes and metadata
    # ------------------------------------------------------------------

    clinical_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    case_manager_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    metadata_: Mapped[Any | None] = mapped_column(
        "metadata",
        JSONB(),
        nullable=True,
        comment="Additional encounter-specific data",
    )

    # ------------------------------------------------------------------
    # Relationships
    # ------------------------------------------------------------------

    person: Mapped["Person"] = relationship(
        "Person",
        back_populates="encounters",
        lazy="select",
    )
    fragment: Mapped["Fragment | None"] = relationship(
        "Fragment",
        lazy="select",
    )
    source_system: Mapped["GovernmentSystem | None"] = relationship(
        "GovernmentSystem",
        lazy="select",
    )
