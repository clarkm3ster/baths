"""
DOMES v2 — Data Gap and Provision Models

DataGap: Identifies where data CANNOT flow between two government systems
due to legal, technical, or policy barriers.

Provision: A specific legal provision or policy that governs data sharing
between systems. Multiple provisions can apply to a single gap.

Key legal frameworks:
- 42 CFR Part 2 (SUD treatment records)
- HIPAA Privacy Rule (PHI)
- FERPA (education records)
- Illinois Mental Health and Developmental Disabilities
  Confidentiality Act (IMHDDCA)
- Illinois Juvenile Court Act (sealed juvenile records)

Gap resolution mechanisms:
- Consent-based sharing (patient authorization)
- Minimum necessary standard
- Treatment/payment/operations exceptions
- Law enforcement exceptions
- Emergency exceptions
"""
from __future__ import annotations

import uuid
from typing import Any, TYPE_CHECKING

from sqlalchemy import Boolean, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from domes.enums import DataDomain, GapSeverity, GapStatus
from domes.models.base import (
    AuditMixin,
    DOMESBase,
    TimestampMixin,
    UUIDPrimaryKeyMixin,
)

if TYPE_CHECKING:
    from domes.models.system import GovernmentSystem


class DataGap(
    UUIDPrimaryKeyMixin,
    TimestampMixin,
    AuditMixin,
    DOMESBase,
):
    """A barrier to data flow between two government systems.

    DataGaps are directional: system_a cannot share [data_domain] with system_b.
    Bidirectional barriers require two DataGap records.

    Severity:
        CRITICAL: Legally prohibited, no exception path
        HIGH: Strong prohibition, limited exceptions
        MEDIUM: Prohibited by policy, consent can unlock
        LOW: Technical/procedural barrier, fixable
    """

    __tablename__ = "data_gap"

    system_a_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("government_system.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="Source system (the one holding the data)",
    )
    system_b_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("government_system.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="Receiving system (the one that needs the data)",
    )
    data_domain: Mapped[DataDomain] = mapped_column(
        Enum(DataDomain, name="data_domain_enum", create_type=False),
        nullable=False,
    )
    severity: Mapped[GapSeverity] = mapped_column(
        Enum(GapSeverity, name="gap_severity_enum"),
        nullable=False,
    )
    status: Mapped[GapStatus] = mapped_column(
        Enum(GapStatus, name="gap_status_enum"),
        nullable=False,
        default=GapStatus.ACTIVE,
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    legal_basis: Mapped[str | None] = mapped_column(
        Text, nullable=True, comment="Primary legal authority creating this gap"
    )
    exception_path: Mapped[str | None] = mapped_column(
        Text, nullable=True, comment="How to legally bridge this gap (consent, TPO, emergency)"
    )
    requires_consent: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    requires_court_order: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    estimated_persons_affected: Mapped[int | None] = mapped_column(Integer, nullable=True)
    metadata_: Mapped[Any | None] = mapped_column("metadata", JSONB(), nullable=True)

    system_a: Mapped["GovernmentSystem"] = relationship(
        "GovernmentSystem",
        foreign_keys="DataGap.system_a_id",
        back_populates="gaps_as_source",
        lazy="select",
    )
    system_b: Mapped["GovernmentSystem"] = relationship(
        "GovernmentSystem",
        foreign_keys="DataGap.system_b_id",
        back_populates="gaps_as_target",
        lazy="select",
    )
    provisions: Mapped[list["Provision"]] = relationship(
        "Provision",
        back_populates="gap",
        lazy="select",
    )


class Provision(
    UUIDPrimaryKeyMixin,
    TimestampMixin,
    AuditMixin,
    DOMESBase,
):
    """A specific legal provision governing a data gap.

    A DataGap may have multiple Provisions (e.g., HIPAA + 42 CFR Part 2
    both apply to SUD treatment records shared with corrections).
    """

    __tablename__ = "provision"

    gap_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("data_gap.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    citation: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        comment="Legal citation (e.g., '42 CFR Part 2', 'HIPAA 45 CFR 164.512')",
    )
    provision_type: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
        comment="Type: prohibition/exception/consent_form/court_order/tpo",
    )
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_waivable: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        comment="Can this provision be waived by patient consent?",
    )
    jurisdiction: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        comment="Jurisdiction: 'federal', 'illinois', 'cook_county', etc.",
    )
    effective_date: Mapped[str | None] = mapped_column(String(20), nullable=True)
    notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        comment="Implementation notes, exceptions, state-specific variations",
    )

    gap: Mapped["DataGap"] = relationship("DataGap", back_populates="provisions", lazy="select")
