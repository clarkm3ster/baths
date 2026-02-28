"""
DOMES v2 — Data Gap and Provision Models

DataGap: Identifies where data CANNOT flow between two government systems,
and why. Based on the 9 critical gaps in the DOMES architecture.

Provision: Legal provisions (rights, protections, obligations) that apply to
a person based on their circumstances. Mirrors the DOMES legal matching engine.
"""
from __future__ import annotations

import uuid
from typing import Any, TYPE_CHECKING

from sqlalchemy import Boolean, Enum, Float, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import ARRAY, JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from domes.enums import (
    GapSeverity,
    GapType,
    ProvisionDomain,
    ProvisionType,
)
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
    """A barrier preventing data from flowing between two government systems.

    The 9 critical gaps identified in DOMES represent the most costly data
    barriers for vulnerable populations. Examples:
    - DOC ↔ MMIS: Medicaid Inmate Exclusion Policy (Critical)
    - DOC ↔ BHA: 42 CFR Part 2 (Critical)
    - IEP ↔ MMIS: FERPA (High)

    Gaps drive the delta calculation in the Dome model — the gap between
    fragmented_annual_cost and coordinated_annual_cost.
    """

    __tablename__ = "data_gap"
    __table_args__ = {
        "comment": (
            "Data barriers between government systems. "
            "Identifies where data CANNOT flow and why. "
            "Drives the financial cost-of-fragmentation calculation in the Dome."
        )
    }

    # ------------------------------------------------------------------
    # Systems involved
    # ------------------------------------------------------------------

    system_a_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("government_system.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="First system in the gap pair",
    )
    system_b_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("government_system.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="Second system in the gap pair",
    )

    # ------------------------------------------------------------------
    # Gap details
    # ------------------------------------------------------------------

    gap_type: Mapped[GapType] = mapped_column(
        Enum(GapType, name="gap_type_enum"),
        nullable=False,
        comment="Primary type of barrier (legal, technical, political, structural, resource)",
    )
    severity: Mapped[GapSeverity] = mapped_column(
        Enum(GapSeverity, name="gap_severity_enum"),
        nullable=False,
        default=GapSeverity.HIGH,
        comment="Impact severity of this gap on vulnerable populations",
    )
    barrier_law: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        comment="Specific law or policy creating this barrier (e.g., '42 CFR Part 2', 'FERPA')",
    )
    barrier_description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        comment="Plain-language description of why this gap exists",
    )
    impact_description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        comment="How this gap harms people in practice (clinical, financial, safety impacts)",
    )
    population_affected: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        comment="Which population is most affected by this gap",
    )

    # ------------------------------------------------------------------
    # Proposed bridge / solution
    # ------------------------------------------------------------------

    bridge_exists: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        comment="Is there a known legal/technical solution to this gap?",
    )
    bridge_description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        comment="Description of the proposed bridge / workaround",
    )
    bridge_cost_estimate: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
        comment="Estimated implementation cost of the bridge (USD)",
    )
    bridge_timeline_months: Mapped[int | None] = mapped_column(
        nullable=True,
        comment="Estimated months to implement the bridge",
    )
    example_implementations: Mapped[Any | None] = mapped_column(
        JSONB(),
        ARRAY(String),
        nullable=True,
        comment="States or programs that have successfully bridged this gap",
    )

    # ------------------------------------------------------------------
    # Financial impact
    # ------------------------------------------------------------------

    annual_cost_estimate: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
        comment="Estimated annual cost of this gap per affected person (USD)",
    )
    annual_savings_estimate: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
        comment="Estimated annual savings if this gap were closed (USD per person)",
    )
    references: Mapped[Any | None] = mapped_column(
        JSONB(),
        ARRAY(String),
        nullable=True,
        comment="Citations, source URLs, or policy documents describing this gap",
    )

    # ------------------------------------------------------------------
    # Relationships
    # ------------------------------------------------------------------

    system_a: Mapped["GovernmentSystem"] = relationship(
        "GovernmentSystem",
        foreign_keys=[system_a_id],
        back_populates="gaps_as_system_a",
        lazy="select",
    )
    system_b: Mapped["GovernmentSystem"] = relationship(
        "GovernmentSystem",
        foreign_keys=[system_b_id],
        back_populates="gaps_as_system_b",
        lazy="select",
    )


class Provision(
    UUIDPrimaryKeyMixin,
    TimestampMixin,
    AuditMixin,
    DOMESBase,
):
    """A legal provision (right, protection, or obligation) applicable to a person.

    Provisions are matched to persons based on their circumstances (PersonProfile).
    This is the core output of the DOMES legal matching engine.

    Examples:
    - EMTALA: Right to emergency care regardless of ability to pay
    - ADA Title II: Protection from discrimination in government programs
    - McKinney-Vento: Education rights for homeless youth
    - 42 CFR Part 2: Protection of SUD treatment records

    The matching engine scores provisions based on how many conditions in
    applies_when match the person's current circumstances.
    """

    __tablename__ = "provision"
    __table_args__ = {
        "comment": (
            "Legal provisions that may apply to vulnerable populations. "
            "Matched to persons via the legal matching engine based on PersonProfile circumstances."
        )
    }

    # ------------------------------------------------------------------
    # Identity / Citation
    # ------------------------------------------------------------------

    citation: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True,
        comment="Legal citation (e.g., '42 U.S.C. § 1395dd', '42 CFR § 2.31')",
    )
    title: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
        comment="Human-readable provision title",
    )
    common_name: Mapped[str | None] = mapped_column(
        String(200),
        nullable=True,
        comment="Common name if different from title (e.g., 'EMTALA', 'McKinney-Vento')",
    )
    full_text: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        comment="Actual legal text or authoritative summary",
    )
    plain_language: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        comment="Plain-language explanation of what this provision means for the person",
    )

    # ------------------------------------------------------------------
    # Classification
    # ------------------------------------------------------------------

    domain: Mapped[ProvisionDomain] = mapped_column(
        Enum(ProvisionDomain, name="provision_domain_enum"),
        nullable=False,
        comment="Primary legal domain",
    )
    provision_type: Mapped[ProvisionType] = mapped_column(
        Enum(ProvisionType, name="provision_type_enum"),
        nullable=False,
        comment="Type: right / protection / obligation / enforcement",
    )
    priority: Mapped[int] = mapped_column(
        nullable=False,
        default=5,
        comment="Matching priority 0–10 (lower = higher priority). Health=0, civil_rights=1",
    )

    # ------------------------------------------------------------------
    # Matching criteria
    # ------------------------------------------------------------------

    applies_when: Mapped[Any] = mapped_column(
        JSONB(),
        nullable=False,
        default=dict,
        comment=(
            "Conditions under which this provision applies. "
            "Structure: {'insurance': ['medicaid'], 'disabilities': ['mental_health'], ...}. "
            "Used by the legal matching engine to score applicability."
        ),
    )
    requires_all_conditions: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        comment="True = ALL applies_when conditions must match. False = ANY match is sufficient.",
    )

    # ------------------------------------------------------------------
    # Enforcement and action
    # ------------------------------------------------------------------

    enforcement_mechanisms: Mapped[Any | None] = mapped_column(
        JSONB(),
        ARRAY(String),
        nullable=True,
        comment="How this provision is enforced (e.g., ['HHS Office for Civil Rights', 'private right of action'])",
    )
    action_required: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        comment="What action the person or their advocate should take to invoke this provision",
    )
    source_url: Mapped[str | None] = mapped_column(
        String(1024),
        nullable=True,
        comment="URL to the authoritative text of this provision",
    )
    cross_references: Mapped[Any | None] = mapped_column(
        JSONB(),
        ARRAY(String),
        nullable=True,
        comment="Citations of related provisions that interact with this one",
    )

    # ------------------------------------------------------------------
    # Status
    # ------------------------------------------------------------------

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        comment="False if this provision has been repealed or superseded",
    )
    effective_date: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
        comment="When this provision took effect (ISO date or description)",
    )
    notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        comment="Implementation notes, exceptions, state-specific variations",
    )
