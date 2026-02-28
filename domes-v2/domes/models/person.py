"""
DOMES v2 — Person Model

The Person is the primary key of the universe. Every other table relates back
to a Person. This model is rich — not just demographics but a living entity
that accumulates history across all 9+ government systems.

Key design decisions:
- UUID primary key — never expose SSN or government IDs as the key
- SSN stored only as a salted SHA-256 hash — never plaintext
- Carries identifiers for all major government systems (HMIS, FHIR, Medicaid, etc.)
- FHIR Patient resource type alignment (US Core Patient profile)
"""
from __future__ import annotations

import uuid
from datetime import date, datetime
from typing import Any, TYPE_CHECKING

from sqlalchemy import JSON, Boolean, Date, DateTime, Enum, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from domes.enums import (
    EmploymentStatus,
    Ethnicity,
    Gender,
    HousingStatus,
    ImmigrationStatus,
    Race,
)
from domes.models.base import (
    AuditMixin,
    DOMESBase,
    FHIRMixin,
    SoftDeleteMixin,
    TimestampMixin,
    UUIDPrimaryKeyMixin,
)

if TYPE_CHECKING:
    from domes.models.assessment import Assessment
    from domes.models.biometric import BiometricReading
    from domes.models.condition import Condition
    from domes.models.consent import Consent, ConsentAuditEntry
    from domes.models.dome import Dome
    from domes.models.encounter import Encounter
    from domes.models.enrollment import Enrollment
    from domes.models.environment import EnvironmentReading
    from domes.models.flourishing import FlourishingScore
    from domes.models.fragment import Fragment
    from domes.models.medication import Medication
    from domes.models.observation import Observation


class Person(
    UUIDPrimaryKeyMixin,
    TimestampMixin,
    SoftDeleteMixin,
    AuditMixin,
    FHIRMixin,
    DOMESBase,
):
    """Core person entity — the center of the DOMES universe.

    Implements the FHIR US Core Patient profile conceptually. Every other
    table relates back to this via person_id FK.

    Privacy controls:
    - ssn_hash: SHA-256(salt + SSN) — never store SSN plaintext
    - All government identifiers stored for cross-system matching only
    - fhir_resource_type always = 'Patient' for this model
    """

    __tablename__ = "person"
    __table_args__ = {
        "comment": (
            "Core person entity. The Person is the primary key of the DOMES universe. "
            "Every government system record ultimately relates to a Person."
        )
    }

    # ------------------------------------------------------------------
    # Identity / Demographics
    # ------------------------------------------------------------------

    first_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        comment="Legal first name",
    )
    last_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        comment="Legal last name",
    )
    middle_name: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        comment="Middle name (optional)",
    )
    preferred_name: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        comment="Name the person prefers to be called",
    )
    name_suffix: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
        comment="Jr., Sr., III, etc.",
    )
    date_of_birth: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        comment="Date of birth (YYYY-MM-DD)",
    )
    date_of_death: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
        comment="Date of death if deceased",
    )
    gender: Mapped[Gender] = mapped_column(
        Enum(Gender, name="gender_enum"),
        nullable=False,
        default=Gender.UNKNOWN,
        comment="Gender identity — aligned with HMIS list 3.06.1",
    )
    pronouns: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
        comment="Preferred pronouns (e.g., 'he/him', 'they/them')",
    )
    race: Mapped[Race] = mapped_column(
        Enum(Race, name="race_enum"),
        nullable=False,
        default=Race.UNKNOWN,
        comment="Primary race — OMB/HMIS categories",
    )
    race_additional: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        comment="Additional race identities (comma-separated) for multiracial persons",
    )
    ethnicity: Mapped[Ethnicity] = mapped_column(
        Enum(Ethnicity, name="ethnicity_enum"),
        nullable=False,
        default=Ethnicity.UNKNOWN,
        comment="Hispanic/Latino ethnicity (separate from race per OMB)",
    )
    preferred_language: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
        default="en",
        comment="BCP-47 language code (e.g., 'en', 'es', 'zh')",
    )
    interpreter_needed: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        comment="Does this person require an interpreter?",
    )

    # ------------------------------------------------------------------
    # Security-sensitive identifiers — hashed or opaque
    # ------------------------------------------------------------------

    ssn_hash: Mapped[str | None] = mapped_column(
        String(128),
        nullable=True,
        unique=True,
        comment=(
            "SHA-256(DOMES_SSN_SALT + SSN). NEVER store plaintext SSN. "
            "Used for cross-system identity matching only."
        ),
    )
    ssn_last4: Mapped[str | None] = mapped_column(
        String(4),
        nullable=True,
        comment="Last 4 digits of SSN — stored for manual verification only",
    )
    ssn_data_quality: Mapped[int] = mapped_column(
        nullable=False,
        default=99,
        comment="HMIS SSN data quality code: 1=full, 2=partial, 8=unknown, 99=not collected",
    )

    # ------------------------------------------------------------------
    # Cross-system government identifiers
    # ------------------------------------------------------------------

    fhir_patient_id: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        index=True,
        comment="FHIR Patient.id in the primary EHR system",
    )
    hmis_client_id: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        index=True,
        comment="HMIS PersonalID — primary HMIS unique identifier",
    )
    medicaid_id: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        index=True,
        comment="State Medicaid member ID",
    )
    medicare_id: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
        comment="Medicare Beneficiary Identifier (MBI)",
    )
    va_file_number: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
        comment="Veterans Affairs file number",
    )
    social_security_claim_number: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
        comment="SSA benefit claim number (for SSI/SSDI)",
    )
    doc_inmate_number: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        comment="Department of Corrections inmate/booking number",
    )
    snap_case_number: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        comment="SNAP/EBT case number",
    )
    external_identifiers: Mapped[Any | None] = mapped_column(
        JSONB(),
        nullable=True,
        comment=(
            "JSONB map of additional system identifiers: "
            "{'system_id': 'value', ...}. For systems not covered above."
        ),
    )

    # ------------------------------------------------------------------
    # Current status fields (most recent known state)
    # ------------------------------------------------------------------

    current_housing_status: Mapped[HousingStatus] = mapped_column(
        Enum(HousingStatus, name="housing_status_enum"),
        nullable=False,
        default=HousingStatus.UNKNOWN,
        comment="Most recent known housing status",
    )
    current_housing_status_as_of: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        comment="When current_housing_status was last assessed",
    )
    current_employment_status: Mapped[EmploymentStatus] = mapped_column(
        Enum(EmploymentStatus, name="employment_status_enum"),
        nullable=False,
        default=EmploymentStatus.UNKNOWN,
        comment="Most recent known employment status",
    )
    veteran_status: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        comment="Is this person a US military veteran?",
    )
    dv_survivor: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        comment="Is this person a domestic violence survivor?",
    )
    immigration_status: Mapped[ImmigrationStatus] = mapped_column(
        Enum(ImmigrationStatus, name="immigration_status_enum"),
        nullable=False,
        default=ImmigrationStatus.UNKNOWN,
        comment="Immigration status (affects eligibility for programs)",
    )
    chronic_homelessness: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        comment=(
            "HUD chronic homelessness definition: 12 continuous months or "
            "4 episodes totaling 12 months in the past 3 years, with a disabling condition"
        ),
    )

    # ------------------------------------------------------------------
    # Contact information
    # ------------------------------------------------------------------

    phone_primary: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
        comment="Primary phone number",
    )
    phone_secondary: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )
    email: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )
    current_address_text: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        comment="Free-text address; 'Homeless / No Fixed Address' for unhoused",
    )
    current_city: Mapped[str | None] = mapped_column(String(100), nullable=True)
    current_state: Mapped[str | None] = mapped_column(String(2), nullable=True)
    current_zip: Mapped[str | None] = mapped_column(String(10), nullable=True)
    current_county_fips: Mapped[str | None] = mapped_column(
        String(5),
        nullable=True,
        index=True,
        comment="5-digit FIPS code of the county this person is in",
    )

    # ------------------------------------------------------------------
    # Notes
    # ------------------------------------------------------------------

    clinical_notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        comment="Free-text clinical notes (not structured — use Observation for structured data)",
    )
    case_manager_notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    # ------------------------------------------------------------------
    # Relationships
    # ------------------------------------------------------------------

    consents: Mapped[list["Consent"]] = relationship(
        "Consent",
        back_populates="person",
        cascade="all, delete-orphan",
        lazy="select",
    )
    consent_audit_entries: Mapped[list["ConsentAuditEntry"]] = relationship(
        "ConsentAuditEntry",
        back_populates="person",
        cascade="all, delete-orphan",
        lazy="select",
    )
    fragments: Mapped[list["Fragment"]] = relationship(
        "Fragment",
        back_populates="person",
        cascade="all, delete-orphan",
        lazy="select",
    )
    observations: Mapped[list["Observation"]] = relationship(
        "Observation",
        back_populates="person",
        cascade="all, delete-orphan",
        lazy="select",
    )
    encounters: Mapped[list["Encounter"]] = relationship(
        "Encounter",
        back_populates="person",
        cascade="all, delete-orphan",
        lazy="select",
    )
    conditions: Mapped[list["Condition"]] = relationship(
        "Condition",
        back_populates="person",
        cascade="all, delete-orphan",
        lazy="select",
    )
    medications: Mapped[list["Medication"]] = relationship(
        "Medication",
        back_populates="person",
        cascade="all, delete-orphan",
        lazy="select",
    )
    assessments: Mapped[list["Assessment"]] = relationship(
        "Assessment",
        back_populates="person",
        cascade="all, delete-orphan",
        lazy="select",
    )
    enrollments: Mapped[list["Enrollment"]] = relationship(
        "Enrollment",
        back_populates="person",
        cascade="all, delete-orphan",
        lazy="select",
    )
    biometric_readings: Mapped[list["BiometricReading"]] = relationship(
        "BiometricReading",
        back_populates="person",
        cascade="all, delete-orphan",
        lazy="select",
    )
    environment_readings: Mapped[list["EnvironmentReading"]] = relationship(
        "EnvironmentReading",
        back_populates="person",
        cascade="all, delete-orphan",
        lazy="select",
    )
    domes: Mapped[list["Dome"]] = relationship(
        "Dome",
        back_populates="person",
        cascade="all, delete-orphan",
        order_by="Dome.assembled_at.desc()",
        lazy="select",
    )
    flourishing_scores: Mapped[list["FlourishingScore"]] = relationship(
        "FlourishingScore",
        back_populates="person",
        cascade="all, delete-orphan",
        lazy="select",
    )

    # ------------------------------------------------------------------
    # Computed properties
    # ------------------------------------------------------------------

    @property
    def full_name(self) -> str:
        """Return formatted full name."""
        parts = [self.first_name]
        if self.middle_name:
            parts.append(self.middle_name)
        parts.append(self.last_name)
        if self.name_suffix:
            parts.append(self.name_suffix)
        return " ".join(parts)

    @property
    def display_name(self) -> str:
        """Return preferred or legal name for display."""
        return self.preferred_name or f"{self.first_name} {self.last_name}"
