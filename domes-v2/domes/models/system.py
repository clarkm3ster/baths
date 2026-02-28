"""
DOMES v2 — Government System Model

Registry of all 30 government data systems that touch vulnerable populations.
Used as a reference table by Consent, Fragment, Gap, and other models.

Based on the DOMES architecture's mapping of systems across 7 domains:
Health (8), Justice (4+1), Child Welfare (2), Housing (2),
Income (6), Education (3), Additional (6+).

Each system records the privacy laws that govern it, API availability,
and data held — enabling the gap analysis engine to identify which
system-to-system data flows are legally possible.
"""
from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any, TYPE_CHECKING

from sqlalchemy import Boolean, Enum, String, Text
from sqlalchemy.dialects.postgresql import ARRAY, JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from domes.enums import (
    SystemAPIAvailability,
    SystemDomain,
    SystemPrivacyLaw,
)
from domes.models.base import (
    AuditMixin,
    DOMESBase,
    TimestampMixin,
    UUIDPrimaryKeyMixin,
)

if TYPE_CHECKING:
    from domes.models.consent import Consent
    from domes.models.enrollment import Enrollment
    from domes.models.fragment import Fragment
    from domes.models.gap import DataGap


class GovernmentSystem(
    UUIDPrimaryKeyMixin,
    TimestampMixin,
    AuditMixin,
    DOMESBase,
):
    """A government data system that holds records about people.

    The 30 systems in this registry represent the full landscape of
    government data siloes that DOMES bridges. Each system is an actor in
    the consent and gap models — consents authorize data to flow FROM/TO
    specific systems, and gaps identify where data CANNOT flow between systems.

    Examples:
    - MMIS (Medicaid Management Information System) — governs Medicaid data
    - BHA (Behavioral Health Authority) — 42 CFR Part 2 protected
    - HMIS — homeless management data
    - DOC — Department of Corrections records
    - SACWIS — child welfare records
    """

    __tablename__ = "government_system"
    __table_args__ = {
        "comment": (
            "Registry of the 30 government data systems that touch vulnerable populations. "
            "Used as reference in consent, fragment, gap, and provision models."
        )
    }

    # ------------------------------------------------------------------
    # Identity
    # ------------------------------------------------------------------

    system_key: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        unique=True,
        index=True,
        comment="Short machine-readable key (e.g., 'mmis', 'bha', 'hmis', 'doc')",
    )
    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment="Full system name (e.g., 'Medicaid Management Information System')",
    )
    acronym: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        comment="Common acronym (e.g., 'MMIS', 'BHA', 'HMIS')",
    )
    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        comment="Plain-language description of what this system does and holds",
    )
    domain: Mapped[SystemDomain] = mapped_column(
        Enum(SystemDomain, name="system_domain_enum"),
        nullable=False,
        comment="Primary domain / sector of this system",
    )

    # ------------------------------------------------------------------
    # Privacy / Legal
    # ------------------------------------------------------------------

    primary_privacy_law: Mapped[SystemPrivacyLaw] = mapped_column(
        Enum(SystemPrivacyLaw, name="system_privacy_law_enum"),
        nullable=False,
        comment="Primary privacy law governing this system's data",
    )
    additional_privacy_laws: Mapped[Any | None] = mapped_column(
        JSONB(),
        ARRAY(String),
        nullable=True,
        comment="Additional privacy laws that also apply (stored as array of SystemPrivacyLaw values)",
    )
    requires_42cfr_consent: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        comment=(
            "True if this system holds substance use disorder (SUD) records "
            "requiring 42 CFR Part 2 written consent for disclosure"
        ),
    )
    requires_ferpa_consent: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        comment="True if this system holds student education records protected by FERPA",
    )
    requires_cjis_clearance: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        comment="True if access to this system requires FBI CJIS Security Policy clearance",
    )
    data_sharing_notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        comment="Notes on what data sharing is legally possible with other systems",
    )

    # ------------------------------------------------------------------
    # Technical integration
    # ------------------------------------------------------------------

    api_availability: Mapped[SystemAPIAvailability] = mapped_column(
        Enum(SystemAPIAvailability, name="system_api_availability_enum"),
        nullable=False,
        default=SystemAPIAvailability.NONE,
        comment="Level of API / programmatic access available",
    )
    api_base_url: Mapped[str | None] = mapped_column(
        String(512),
        nullable=True,
        comment="Base URL of the system's API (if available)",
    )
    api_standard: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        comment="API standard (e.g., 'FHIR R4', 'REST', 'SOAP', 'X12 EDI', 'CSV batch')",
    )
    auth_method: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        comment="Authentication method (e.g., 'OAuth 2.0 / SMART on FHIR', 'API Key', 'VPN')",
    )
    data_format: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        comment="Primary data format (e.g., 'FHIR JSON', 'HMIS CSV', 'X12 EDI', 'HL7 v2')",
    )
    vendor: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        comment="Primary software vendor (e.g., 'Bitfocus Clarity', 'Epic', 'Oracle CernerClarity')",
    )

    # ------------------------------------------------------------------
    # Data held
    # ------------------------------------------------------------------

    data_categories: Mapped[Any | None] = mapped_column(
        JSONB(),
        ARRAY(String),
        nullable=True,
        comment=(
            "Categories of data held by this system "
            "(e.g., ['diagnoses', 'medications', 'encounters', 'assessments'])"
        ),
    )
    population_served: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        comment="Description of which populations this system serves",
    )
    geographic_scope: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        comment="Geographic scope: 'federal', 'state', 'county', 'local'",
    )
    governing_agency: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        comment="Federal or state agency that oversees this system",
    )

    # ------------------------------------------------------------------
    # DOMES integration status
    # ------------------------------------------------------------------

    is_integrated: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        comment="Has DOMES successfully integrated with this system?",
    )
    integration_notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        comment="Notes on DOMES integration status, challenges, and workarounds",
    )
    metadata_: Mapped[Any | None] = mapped_column(
        "metadata",
        JSONB(),
        nullable=True,
        comment="Additional system-specific metadata as JSONB",
    )

    # ------------------------------------------------------------------
    # Relationships
    # ------------------------------------------------------------------

    fragments: Mapped[list["Fragment"]] = relationship(
        "Fragment",
        back_populates="source_system",
        lazy="select",
    )
    enrollments: Mapped[list["Enrollment"]] = relationship(
        "Enrollment",
        back_populates="system",
        lazy="select",
    )
    gaps_as_system_a: Mapped[list["DataGap"]] = relationship(
        "DataGap",
        foreign_keys="DataGap.system_a_id",
        back_populates="system_a",
        lazy="select",
    )
    gaps_as_system_b: Mapped[list["DataGap"]] = relationship(
        "DataGap",
        foreign_keys="DataGap.system_b_id",
        back_populates="system_b",
        lazy="select",
    )
