"""
DOMES v2 — Enrollment Model

Program enrollments track a person's participation in any government program:
- Medicaid / Medicare
- SNAP / TANF / SSI / SSDI
- Section 8 Housing Choice Voucher
- Emergency shelter / transitional housing / PSH (via HMIS)
- ACT team services
- SUD treatment programs
- Veterans programs (HUD-VASH, SSVF)
- Probation / parole
- Foster care

An Enrollment represents an active or historical relationship between
a person and a government program/system. Entry and exit dates track
the arc of service engagement.

HMIS alignment: Each HMIS Enrollment.csv row = one Enrollment record.
"""
from __future__ import annotations

import uuid
from datetime import date, datetime
from typing import Any, TYPE_CHECKING

from sqlalchemy import Boolean, Date, DateTime, Enum, Float, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from domes.enums import EnrollmentStatus, ExitDestination, ProgramType
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


class Enrollment(
    UUIDPrimaryKeyMixin,
    TimestampMixin,
    AuditMixin,
    FHIRMixin,
    DOMESBase,
):
    """A person's enrollment in a government program or service.

    HMIS alignment: Enrollment.csv + Exit.csv (entry and exit in one record).
    FHIR alignment: EpisodeOfCare resource (for care coordination programs)
    or Coverage resource (for insurance programs).

    The Enrollment is the unit of system involvement. Robert Jackson's 9 systems
    = 9+ active Enrollments at any given time.
    """

    __tablename__ = "enrollment"
    __table_args__ = {
        "comment": (
            "Government program enrollments. "
            "Robert Jackson's 9-system involvement = 9+ rows here. "
            "HMIS aligned: Enrollment.csv + Exit.csv combined."
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
    system_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("government_system.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
        comment="Government system managing this program",
    )
    fragment_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("fragment.id", ondelete="SET NULL"),
        nullable=True,
    )

    # ------------------------------------------------------------------
    # Program identification
    # ------------------------------------------------------------------

    program_type: Mapped[ProgramType] = mapped_column(
        Enum(ProgramType, name="program_type_enum"),
        nullable=False,
        index=True,
    )
    program_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment="Specific program name (e.g., 'Cook County Emergency Shelter', 'Illinois Medicaid')",
    )
    program_id: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        comment="Program ID in the source system (HMIS ProjectID, etc.)",
    )
    enrollment_id_external: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        index=True,
        comment="Enrollment ID in the source system (HMIS EnrollmentID, etc.)",
    )

    # ------------------------------------------------------------------
    # Status and dates
    # ------------------------------------------------------------------

    status: Mapped[EnrollmentStatus] = mapped_column(
        Enum(EnrollmentStatus, name="enrollment_status_enum"),
        nullable=False,
        default=EnrollmentStatus.ACTIVE,
    )
    entry_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        index=True,
        comment="Program entry / enrollment date",
    )
    exit_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
        comment="Program exit date (NULL = still enrolled)",
    )
    move_in_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
        comment="Housing move-in date (HMIS 3.20 — for housing programs)",
    )

    # ------------------------------------------------------------------
    # Exit information (HMIS Exit.csv)
    # ------------------------------------------------------------------

    exit_destination: Mapped[ExitDestination | None] = mapped_column(
        Enum(ExitDestination, name="exit_destination_enum"),
        nullable=True,
        comment="HMIS-aligned housing destination at exit",
    )
    exit_reason: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        comment="Reason for exit or disenrollment",
    )
    exit_notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    # ------------------------------------------------------------------
    # Benefit / financial values
    # ------------------------------------------------------------------

    monthly_benefit_amount: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
        comment="Monthly benefit value (USD) — for SNAP, SSI, Section 8, etc.",
    )
    annual_benefit_amount: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
        comment="Annual benefit value (computed or estimated)",
    )
    benefit_category: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        comment="Benefit category: health, housing, nutrition, income, etc.",
    )

    # ------------------------------------------------------------------
    # HMIS-specific fields
    # ------------------------------------------------------------------

    hmis_enrollment_id: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        comment="HMIS EnrollmentID",
    )
    hmis_project_type: Mapped[int | None] = mapped_column(
        nullable=True,
        comment="HMIS project type code (1=ES, 2=TH, 3=PSH, 4=SO, 6=SSO, 13=RRH)",
    )
    living_situation_at_entry: Mapped[int | None] = mapped_column(
        nullable=True,
        comment="HMIS LivingSituation code at program entry (list 3.917)",
    )
    times_homeless_past_3_years: Mapped[int | None] = mapped_column(
        nullable=True,
        comment="HMIS TimesHomelessPastThreeYears (1-4 or 99)",
    )
    months_homeless_past_3_years: Mapped[int | None] = mapped_column(
        nullable=True,
        comment="HMIS MonthsHomelessPastThreeYears",
    )
    disabling_condition: Mapped[bool | None] = mapped_column(
        nullable=True,
        comment="HMIS DisablingCondition flag — required for chronic homelessness determination",
    )
    path_enrolled: Mapped[bool | None] = mapped_column(
        nullable=True,
        comment="HMIS ClientEnrolledInPATH (Projects for Assistance in Transition from Homelessness)",
    )

    # ------------------------------------------------------------------
    # Case management
    # ------------------------------------------------------------------

    case_manager: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        comment="Assigned case manager name",
    )
    case_manager_contact: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )
    next_review_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
        comment="Date of next eligibility review or recertification",
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
        back_populates="enrollments",
        lazy="select",
    )
    system: Mapped["GovernmentSystem | None"] = relationship(
        "GovernmentSystem",
        back_populates="enrollments",
        lazy="select",
    )
    fragment: Mapped["Fragment | None"] = relationship(
        "Fragment",
        lazy="select",
    )

    # ------------------------------------------------------------------
    # Computed properties
    # ------------------------------------------------------------------

    @property
    def is_active(self) -> bool:
        """Return True if this enrollment is currently active."""
        return self.status == EnrollmentStatus.ACTIVE and self.exit_date is None

    @property
    def duration_days(self) -> int | None:
        """Return enrollment duration in days."""
        from datetime import date as date_type
        if not self.entry_date:
            return None
        end = self.exit_date or date_type.today()
        return (end - self.entry_date).days
