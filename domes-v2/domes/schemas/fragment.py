"""
DOMES v2 — Fragment Pydantic Schemas

Schemas for raw data fragments — the ingest boundary of DOMES.
Fragments are immutable once created; only lifecycle timestamps are updated.

Fragment lifecycle:
    ingested_at → validated_at → normalized_at → assembled_at

is_superseded=True means a newer version of this fragment has arrived.
"""
from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from domes.enums import DataDomain, FragmentSourceType


# ---------------------------------------------------------------------------
# Fragment schemas
# ---------------------------------------------------------------------------

class FragmentCreate(BaseModel):
    """Schema for ingesting a new raw data fragment."""

    model_config = ConfigDict(use_enum_values=True)

    person_id: uuid.UUID = Field(..., description="Person this fragment belongs to")
    source_system_id: uuid.UUID | None = Field(
        None, description="GovernmentSystem.id that produced this fragment"
    )
    source_type: FragmentSourceType = Field(..., description="Origin system type")
    data_domain: DataDomain = Field(..., description="Data sensitivity domain")
    external_id: str | None = Field(
        None, max_length=255,
        description="ID of this record in the source system (for deduplication)"
    )
    external_version: str | None = Field(
        None, max_length=64,
        description="Version/ETag from source system for change detection"
    )
    raw_payload: dict[str, Any] = Field(..., description="Raw data payload from source system")
    source_format: str | None = Field(
        None, max_length=64,
        description="Format of raw_payload: 'fhir_r4', 'hmis_csv', 'hl7_v2', 'json', 'xml'"
    )
    is_42cfr_protected: bool = Field(
        False, description="True if this fragment contains 42 CFR Part 2 SUD data"
    )
    is_pii: bool = Field(True, description="True if this fragment contains PII")
    consent_id: uuid.UUID | None = Field(
        None, description="Consent that authorized ingest of this fragment"
    )


class FragmentRead(BaseModel):
    """Full fragment read response."""

    model_config = ConfigDict(from_attributes=True, use_enum_values=True)

    id: uuid.UUID
    person_id: uuid.UUID
    source_system_id: uuid.UUID | None
    source_type: FragmentSourceType
    data_domain: DataDomain
    external_id: str | None
    external_version: str | None

    # Lifecycle
    ingested_at: datetime
    validated_at: datetime | None
    normalized_at: datetime | None
    assembled_at: datetime | None

    # Status
    validation_status: str | None
    validation_errors: list[str] | None
    normalization_status: str | None
    is_superseded: bool
    superseded_by_id: uuid.UUID | None

    # Content metadata
    source_format: str | None
    is_42cfr_protected: bool
    is_pii: bool
    consent_id: uuid.UUID | None
    normalized_payload: dict[str, Any] | None

    # Audit
    created_at: datetime
    updated_at: datetime
    created_by: str | None


class FragmentSummary(BaseModel):
    """Lightweight fragment summary for listing."""

    model_config = ConfigDict(from_attributes=True, use_enum_values=True)

    id: uuid.UUID
    person_id: uuid.UUID
    source_type: FragmentSourceType
    data_domain: DataDomain
    external_id: str | None
    ingested_at: datetime
    validation_status: str | None
    is_superseded: bool
    is_42cfr_protected: bool
