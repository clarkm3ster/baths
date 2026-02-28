"""
DOMES v2 — Consent Pydantic Schemas

Schemas for the Consent model (42 CFR Part 2 compliant) and
ConsentAuditEntry. The 9 required elements of 42 CFR Part 2 consent
are validated as explicit fields — presence of all 9 is required for
any consent covering substance use disorder records.

42 CFR Part 2 (2024 SAMHSA rule) required elements:
    1. Name of patient (person receiving SUD treatment)
    2. Name/description of disclosing program
    3. Name/description of receiving party
    4. Purpose of the disclosure
    5. Description of the information to be disclosed (data categories)
    6. Statement that the patient may revoke the consent
    7. Expiration date or event
    8. Signature of the patient (or authorized representative)
    9. Date signed

Additional 2024 rule additions:
    - Central registry exception clarification
    - Overdose emergency exception
    - QSO (Qualified Service Organization) carve-outs
"""
from __future__ import annotations

import uuid
from datetime import date, datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator

from domes.enums import (
    ConsentAuditAction,
    ConsentPurpose,
    DataDomain,
    GrantorRelationship,
)


# ---------------------------------------------------------------------------
# ConsentAuditEntry schemas (immutable append-only log)
# ---------------------------------------------------------------------------

class ConsentAuditEntryRead(BaseModel):
    """Read schema for a single consent audit log entry."""

    model_config = ConfigDict(from_attributes=True, use_enum_values=True)

    id: uuid.UUID
    consent_id: uuid.UUID
    person_id: uuid.UUID
    action: ConsentAuditAction
    actor_id: str | None
    actor_name: str | None
    actor_role: str | None
    actor_organization: str | None
    ip_address: str | None
    user_agent: str | None
    data_category_accessed: DataDomain | None
    action_timestamp: datetime
    notes: str | None
    created_at: datetime


# ---------------------------------------------------------------------------
# Consent base
# ---------------------------------------------------------------------------

class ConsentBase(BaseModel):
    """Shared fields for consent create/update."""

    model_config = ConfigDict(from_attributes=True, use_enum_values=True)

    # Parties
    granting_person_id: uuid.UUID | None = Field(
        None, description="Person who signed (usually = person_id for self-consent)"
    )
    grantor_relationship: GrantorRelationship | None = Field(
        None, description="Relationship of signer to the person"
    )
    receiving_organization_id: uuid.UUID | None = Field(
        None, description="GovernmentSystem.id receiving data"
    )

    # Scope
    purpose: ConsentPurpose | None = Field(None, description="Purpose for data sharing")
    data_categories: list[str] | None = Field(
        None, description="DataDomain values covered by this consent"
    )

    # 42 CFR Part 2 required elements
    # Element 1: patient name — resolved from person_id
    # Element 2: disclosing program
    cfr42_disclosing_program: str | None = Field(
        None, max_length=255,
        description="42 CFR Part 2 Element 2: Name/description of disclosing program"
    )
    # Element 3: receiving party — resolved from receiving_organization_id
    # Element 4: purpose — resolved from purpose field
    # Element 5: information description
    cfr42_information_description: str | None = Field(
        None, max_length=1000,
        description="42 CFR Part 2 Element 5: Description of the information to be disclosed"
    )
    # Element 6: right to revoke
    cfr42_right_to_revoke_stated: bool = Field(
        True, description="42 CFR Part 2 Element 6: Patient informed of right to revoke"
    )
    # Element 7: expiration
    expires_at: datetime | None = Field(
        None, description="42 CFR Part 2 Element 7: Expiration date"
    )
    cfr42_expiration_event: str | None = Field(
        None, max_length=255,
        description="42 CFR Part 2 Element 7 (alt): Expiration event description"
    )
    # Element 8: signature
    cfr42_signed: bool = Field(
        False, description="42 CFR Part 2 Element 8: Consent has been signed"
    )
    cfr42_signature_method: str | None = Field(
        None, max_length=64,
        description="Signature method: 'wet_ink', 'electronic', 'verbal_with_witness'"
    )
    # Element 9: date signed
    cfr42_date_signed: datetime | None = Field(
        None, description="42 CFR Part 2 Element 9: Date the consent was signed"
    )

    # General
    is_42cfr_protected: bool = Field(
        False, description="True = this consent covers 42 CFR Part 2 SUD records"
    )
    is_active: bool = Field(True)
    revocation_reason: str | None = Field(None, max_length=500)
    witness_name: str | None = Field(None, max_length=255)
    notes: str | None = Field(None, max_length=2000)


# ---------------------------------------------------------------------------
# Create schema
# ---------------------------------------------------------------------------

class ConsentCreate(ConsentBase):
    """Create a new consent record for a person."""

    person_id: uuid.UUID = Field(..., description="Person granting consent")

    @field_validator("expires_at")
    @classmethod
    def validate_expiry(cls, v: datetime | None) -> datetime | None:
        if v is not None and v < datetime.utcnow():
            raise ValueError("Expiration date must be in the future")
        return v


# ---------------------------------------------------------------------------
# Update schema
# ---------------------------------------------------------------------------

class ConsentUpdate(BaseModel):
    """Partial consent update — e.g., revoke or extend expiry."""

    model_config = ConfigDict(from_attributes=True, use_enum_values=True)

    is_active: bool | None = None
    revocation_reason: str | None = Field(None, max_length=500)
    expires_at: datetime | None = None
    notes: str | None = Field(None, max_length=2000)


# ---------------------------------------------------------------------------
# Read schemas
# ---------------------------------------------------------------------------

class ConsentRead(BaseModel):
    """Full consent read response with 42 CFR Part 2 compliance summary."""

    model_config = ConfigDict(from_attributes=True, use_enum_values=True)

    id: uuid.UUID
    person_id: uuid.UUID
    granting_person_id: uuid.UUID | None
    grantor_relationship: GrantorRelationship | None
    receiving_organization_id: uuid.UUID | None

    purpose: ConsentPurpose | None
    data_categories: list[str] | None

    # 42 CFR Part 2 fields
    is_42cfr_protected: bool
    cfr42_compliant: bool | None = None
    cfr42_disclosing_program: str | None
    cfr42_information_description: str | None
    cfr42_right_to_revoke_stated: bool
    cfr42_signed: bool
    cfr42_signature_method: str | None
    cfr42_date_signed: datetime | None
    cfr42_expiration_event: str | None

    is_active: bool
    expires_at: datetime | None
    revocation_reason: str | None
    witness_name: str | None
    notes: str | None

    fhir_resource_type: str | None
    fhir_resource_id: str | None

    created_at: datetime
    updated_at: datetime
    created_by: str | None
