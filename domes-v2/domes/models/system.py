"""
DOMES v2 — Government System Model

Registry of all 30 government data systems that touch vulnerable persons
in Cook County (Robert Jackson's 9 systems are the core use case).

Each GovernmentSystem represents:
- A distinct government agency or program
- Its data capabilities and API availability
- Its role in the care coordination ecosystem
- Its data sharing constraints (via DataGap)

The 9 core systems for Robert Jackson:
1. Illinois Medicaid (HFS)
2. Cook County Health (CCH)
3. HMIS (All Chicago)
4. Illinois DCFS
5. Cook County Adult Probation (CCADP)
6. Illinois DOC
7. Illinois DHS (SNAP/TANF/rental assist)
8. SSA (SSI/SSDI)
9. Cook County Assessor / Housing Authority
"""
from __future__ import annotations

import uuid
from typing import Any, TYPE_CHECKING

from sqlalchemy import Boolean, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from domes.enums import DataDomain, SystemTier, SystemType
from domes.models.base import (
    AuditMixin,
    DOMESBase,
    TimestampMixin,
    UUIDPrimaryKeyMixin,
)

if TYPE_CHECKING:
    from domes.models.enrollment import Enrollment
    from domes.models.fragment import Fragment
    from domes.models.gap import DataGap
    from domes.models.person import Person


class GovernmentSystem(
    UUIDPrimaryKeyMixin,
    TimestampMixin,
    AuditMixin,
    DOMESBase,
):
    """A government agency, program, or system in the DOMES ecosystem."""

    __tablename__ = "government_system"
    __table_args__ = {
        "comment": (
            "Registry of government data systems. The 9 core systems for Robert Jackson "
            "are pre-seeded. Total registry: ~30 systems."
        )
    }

    # ------------------------------------------------------------------
    # Identity
    # ------------------------------------------------------------------

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True,
        comment="Official system name (e.g., 'Illinois Medicaid (HFS)')",
    )
    abbreviation: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
        comment="Common abbreviation (e.g., 'HFS', 'CCH', 'HMIS')",
    )
    agency_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    system_type: Mapped[SystemType] = mapped_column(
        Enum(SystemType, name="system_type_enum"),
        nullable=False,
    )
    tier: Mapped[SystemTier] = mapped_column(
        Enum(SystemTier, name="system_tier_enum"),
        nullable=False,
        default=SystemTier.STATE,
        comment="Government tier: federal/state/county/city/ngo",
    )
    jurisdiction: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        comment="Geographic jurisdiction",
    )

    # ------------------------------------------------------------------
    # Data capabilities
    # ------------------------------------------------------------------

    primary_data_domains: Mapped[Any | None] = mapped_column(
        JSONB(),
        nullable=True,
        comment="Primary data domains this system holds (array of DataDomain values)",
    )
    api_available: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    api_type: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
        comment="API type: REST/FHIR/HL7/SOAP/file_transfer/none",
    )
    fhir_base_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    hmis_project_id: Mapped[str | None] = mapped_column(String(100), nullable=True)
    data_standards: Mapped[Any | None] = mapped_column(
        JSONB(),
        nullable=True,
        comment="Standards used: ['HL7_FHIR_R4', 'HMIS_2024', 'X12_837']",
    )

    # ------------------------------------------------------------------
    # Contact / admin
    # ------------------------------------------------------------------

    contact_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    contact_email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    contact_phone: Mapped[str | None] = mapped_column(String(50), nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    # ------------------------------------------------------------------
    # Metrics (denormalized for quick reference)
    # ------------------------------------------------------------------

    estimated_persons_served: Mapped[int | None] = mapped_column(
        Integer, nullable=True,
        comment="Estimated persons served annually in Cook County",
    )
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    metadata_: Mapped[Any | None] = mapped_column("metadata", JSONB(), nullable=True)

    # ------------------------------------------------------------------
    # Relationships
    # ------------------------------------------------------------------

    enrollments: Mapped[list["Enrollment"]] = relationship(
        "Enrollment",
        back_populates="system",
        lazy="select",
    )
    fragments: Mapped[list["Fragment"]] = relationship(
        "Fragment",
        back_populates="source_system",
        lazy="select",
    )
    gaps_as_source: Mapped[list["DataGap"]] = relationship(
        "DataGap",
        foreign_keys="DataGap.system_a_id",
        back_populates="system_a",
        lazy="select",
    )
    gaps_as_target: Mapped[list["DataGap"]] = relationship(
        "DataGap",
        foreign_keys="DataGap.system_b_id",
        back_populates="system_b",
        lazy="select",
    )
