"""
DOMES v2 — Consent Model (42 CFR Part 2 compliant)

The consent model is structural, not decorative. It implements the 9-element
42 CFR Part 2 consent requirements and tracks a full audit trail of every
data access under each consent.

42 CFR Part 2 requires the following 9 elements in a valid consent:
1. Name of Part 2 program (FROM — source system)
2. Name of entity receiving disclosure (TO — recipient system)
3. Patient name and identifier
4. Specific purpose of disclosure
5. Amount and kind of information to be disclosed
6. Patient's right to revoke + exceptions
7. Expiration date, event, or condition
8. Patient signature + date
9. Re-disclosure prohibition statement

The 2024 SAMHSA Final Rule (effective April 16, 2024) now allows a single
consent to authorize ALL future TPO (treatment, payment, healthcare operations)
disclosures — meaning DOMES can obtain one consent to integrate all SUD records.

Refs:
- 42 CFR Part 2: https://www.ecfr.gov/current/title-42/chapter-I/subchapter-A/part-2
- 2024 Rule: https://www.federalregister.gov/documents/2024/02/16/2024-03225
- FHIR Consent resource: https://hl7.org/fhir/R4/consent.html
"""
from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from domes.enums import (
    ConsentAuditAction,
    ConsentPurpose,
    DataDomain,
    GrantorRelationship,
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


class Consent(
    UUIDPrimaryKeyMixin,
    TimestampMixin,
    AuditMixin,
    FHIRMixin,
    DOMESBase,
):
    """Consent grant — a single authorization covering one data flow.

    A consent authorizes data to flow FROM a source_system TO a recipient_system
    for a specific data_domain and purpose. Implements the 9-element 42 CFR Part 2
    consent checklist.

    Multiple consents can be active simultaneously for the same person, covering
    different systems or purposes.

    FHIR alignment: maps to FHIR Consent resource.
    """

    __tablename__ = "consent"
    __table_args__ = {
        "comment": (
            "Patient consent records implementing 42 CFR Part 2 (9-element requirement). "
            "Every data ingestion must reference a valid consent."
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
        comment="The person who granted this consent",
    )
    source_system_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("government_system.id", ondelete="SET NULL"),
        nullable=True,
        comment=(
            "42 CFR Part 2 element 1: Name of Part 2 program / source system "
            "from which data may be disclosed. NULL = any system."
        ),
    )
    recipient_system_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("government_system.id", ondelete="SET NULL"),
        nullable=True,
        comment=(
            "42 CFR Part 2 element 2: Name of entity authorized to receive disclosure. "
            "NULL = DOMES platform itself."
        ),
    )

    # ------------------------------------------------------------------
    # 42 CFR Part 2 — Element 3: Patient identification (via person_id)
    # ------------------------------------------------------------------

    # ------------------------------------------------------------------
    # 42 CFR Part 2 — Element 1 & 2: From / To descriptions
    # ------------------------------------------------------------------

    from_program_name: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
        comment=(
            "42 CFR Part 2 element 1: Specific name of the Part 2 program authorizing disclosure. "
            "Must be the exact program name, not just the organization."
        ),
    )
    to_organization_name: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
        default="DOMES Integration Platform",
        comment="42 CFR Part 2 element 2: Name of entity receiving the disclosure.",
    )

    # ------------------------------------------------------------------
    # 42 CFR Part 2 — Element 4: Purpose
    # ------------------------------------------------------------------

    purpose: Mapped[ConsentPurpose] = mapped_column(
        Enum(ConsentPurpose, name="consent_purpose_enum"),
        nullable=False,
        default=ConsentPurpose.CARE_COORDINATION,
        comment="42 CFR Part 2 element 4: Specific purpose of the disclosure",
    )
    purpose_description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        default=(
            "Care coordination and digital twin integration for treatment, "
            "payment, and healthcare operations per 2024 SAMHSA Final Rule"
        ),
        comment="Human-readable description of the purpose",
    )

    # ------------------------------------------------------------------
    # 42 CFR Part 2 — Element 5: Amount and kind of information
    # ------------------------------------------------------------------

    data_domain: Mapped[DataDomain] = mapped_column(
        Enum(DataDomain, name="data_domain_enum"),
        nullable=False,
        comment=(
            "42 CFR Part 2 element 5: The category of information covered by this consent. "
            "SUBSTANCE_USE requires 42 CFR Part 2 consent; others may only require HIPAA."
        ),
    )
    amount_and_kind: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        default=(
            "All records pertaining to this data domain including diagnoses, "
            "medications, lab results, clinical notes, and treatment history"
        ),
        comment="42 CFR Part 2 element 5: Specific types of information covered",
    )
    specific_restrictions: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        comment="Any explicit limitations on what data is covered or how it may be used",
    )

    # ------------------------------------------------------------------
    # 42 CFR Part 2 — Element 6: Right to revoke
    # ------------------------------------------------------------------

    revocation_rights_stated: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        comment=(
            "42 CFR Part 2 element 6: Was the patient informed of their right to revoke? "
            "Must be True for cfr42_compliant to be True."
        ),
    )

    # ------------------------------------------------------------------
    # 42 CFR Part 2 — Element 7: Expiration
    # ------------------------------------------------------------------

    expires_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        comment=(
            "42 CFR Part 2 element 7: When this consent expires. "
            "NULL = no fixed expiration (but revocable at any time)."
        ),
    )
    expiration_event: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        comment=(
            "42 CFR Part 2 element 7 (alternative): Expiration condition "
            "e.g. 'upon discharge from program' or 'upon patient revocation'"
        ),
    )

    # ------------------------------------------------------------------
    # 42 CFR Part 2 — Element 8: Signature
    # ------------------------------------------------------------------

    grantor: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment="42 CFR Part 2 element 8: Name of person who signed the consent",
    )
    grantor_relationship: Mapped[GrantorRelationship] = mapped_column(
        Enum(GrantorRelationship, name="grantor_relationship_enum"),
        nullable=False,
        default=GrantorRelationship.SELF,
        comment="Relationship of the signer to the patient",
    )
    granted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        comment="42 CFR Part 2 element 8: Date and time consent was signed",
    )
    consent_document_url: Mapped[str | None] = mapped_column(
        String(1024),
        nullable=True,
        comment="URL to the signed consent document (PDF) in secure document storage",
    )

    # ------------------------------------------------------------------
    # 42 CFR Part 2 — Element 9: Re-disclosure prohibition
    # ------------------------------------------------------------------

    redisclosure_notice_included: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        comment=(
            "42 CFR Part 2 element 9: Does the consent include the re-disclosure "
            "prohibition notice? Required: '42 CFR Part 2 prohibits unauthorized "
            "use or disclosure of these records.'"
        ),
    )

    # ------------------------------------------------------------------
    # Compliance flags
    # ------------------------------------------------------------------

    cfr42_compliant: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        comment=(
            "True when all 9 elements of 42 CFR Part 2 consent are present and valid. "
            "Required for disclosing substance use disorder treatment records. "
            "Set by the consent validation service, not manually."
        ),
    )
    hipaa_compliant: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        comment="True when consent meets HIPAA authorization requirements",
    )
    covers_tpo: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        comment=(
            "True if this consent covers Treatment, Payment, and Healthcare Operations "
            "per 2024 SAMHSA Final Rule (single TPO consent). Allows downstream "
            "redisclosure for TPO purposes without additional consent."
        ),
    )

    # ------------------------------------------------------------------
    # Revocation
    # ------------------------------------------------------------------

    revoked_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        comment="When the patient revoked this consent; NULL = still active",
    )
    revocation_reason: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        comment="Patient's stated reason for revocation",
    )
    revoked_by: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        comment="Staff member who processed the revocation",
    )

    # ------------------------------------------------------------------
    # Relationships
    # ------------------------------------------------------------------

    person: Mapped["Person"] = relationship(
        "Person",
        back_populates="consents",
        lazy="select",
    )
    source_system: Mapped["GovernmentSystem | None"] = relationship(
        "GovernmentSystem",
        foreign_keys=[source_system_id],
        lazy="select",
    )
    recipient_system: Mapped["GovernmentSystem | None"] = relationship(
        "GovernmentSystem",
        foreign_keys=[recipient_system_id],
        lazy="select",
    )
    audit_entries: Mapped[list["ConsentAuditEntry"]] = relationship(
        "ConsentAuditEntry",
        back_populates="consent",
        cascade="all, delete-orphan",
        order_by="ConsentAuditEntry.occurred_at.desc()",
        lazy="select",
    )
    fragments: Mapped[list["Fragment"]] = relationship(
        "Fragment",
        back_populates="consent",
        lazy="select",
    )

    # ------------------------------------------------------------------
    # Computed properties
    # ------------------------------------------------------------------

    @property
    def is_active(self) -> bool:
        """Return True if this consent is currently valid."""
        from datetime import timezone
        now = datetime.now(timezone.utc)
        if self.revoked_at:
            return False
        if self.expires_at and self.expires_at < now:
            return False
        return True

    @property
    def cfr42_elements_present(self) -> dict[str, bool]:
        """Return a checklist of the 9 required 42 CFR Part 2 elements."""
        return {
            "1_from_program": bool(self.from_program_name),
            "2_to_organization": bool(self.to_organization_name),
            "3_patient_identified": bool(self.person_id),
            "4_purpose": bool(self.purpose),
            "5_amount_and_kind": bool(self.amount_and_kind),
            "6_revocation_rights": self.revocation_rights_stated,
            "7_expiration": bool(self.expires_at or self.expiration_event),
            "8_signature_and_date": bool(self.grantor and self.granted_at),
            "9_redisclosure_notice": self.redisclosure_notice_included,
        }


class ConsentAuditEntry(
    UUIDPrimaryKeyMixin,
    DOMESBase,
):
    """Immutable audit trail entry for a consent.

    Records every significant action taken under a consent:
    - Who accessed what data under this consent
    - When they accessed it
    - Why (purpose)
    - What system they accessed it from/to

    This table is append-only — records are NEVER updated or deleted.
    This is required for 42 CFR Part 2 compliance.
    """

    __tablename__ = "consent_audit_entry"
    __table_args__ = {
        "comment": (
            "Immutable audit log for consent actions. "
            "42 CFR Part 2 requires tracking all accesses under each consent. "
            "This table is append-only."
        )
    }

    # ------------------------------------------------------------------
    # Relations
    # ------------------------------------------------------------------

    consent_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("consent.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    person_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("person.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="Denormalized for query efficiency",
    )

    # ------------------------------------------------------------------
    # Audit fields
    # ------------------------------------------------------------------

    occurred_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        comment="When this action occurred (UTC)",
    )
    action: Mapped[ConsentAuditAction] = mapped_column(
        Enum(ConsentAuditAction, name="consent_audit_action_enum"),
        nullable=False,
        comment="What action was performed",
    )
    actor: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment="User ID, system ID, or service name that performed the action",
    )
    actor_role: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        comment="Role of the actor (e.g., 'case_manager', 'physician', 'etl_service')",
    )
    data_domain: Mapped[DataDomain | None] = mapped_column(
        Enum(DataDomain, name="audit_data_domain_enum"),
        nullable=True,
        comment="What data domain was accessed",
    )
    resource_type: Mapped[str | None] = mapped_column(
        String(64),
        nullable=True,
        comment="FHIR resource type accessed (e.g., 'Observation', 'Condition')",
    )
    resource_id: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        comment="ID of the specific resource accessed",
    )
    recipient_system: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        comment="System or entity the data was shared with (if action=SHARED)",
    )
    purpose: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        comment="Stated purpose for this specific access",
    )
    notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        comment="Additional context",
    )
    ip_address: Mapped[str | None] = mapped_column(
        String(45),
        nullable=True,
        comment="IP address of the requester (IPv4 or IPv6)",
    )

    # ------------------------------------------------------------------
    # Relationships
    # ------------------------------------------------------------------

    consent: Mapped["Consent"] = relationship(
        "Consent",
        back_populates="audit_entries",
        lazy="select",
    )
    person: Mapped["Person"] = relationship(
        "Person",
        back_populates="consent_audit_entries",
        lazy="select",
    )
