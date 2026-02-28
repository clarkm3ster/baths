"""
DOMES v2 — Observation Pydantic Schemas

Schemas for FHIR-aligned observations: vitals, labs, surveys, SDOH.
Covers PHQ-9, GAD-7, and key biometric/lab results.
"""
from __future__ import annotations

import uuid
from datetime import datetime
from decimal import Decimal
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from domes.enums import (
    CodeSystem,
    ObservationCategory,
    ObservationStatus,
)


class ObservationBase(BaseModel):
    """Shared fields for observation create/update."""

    model_config = ConfigDict(use_enum_values=True)

    person_id: uuid.UUID
    encounter_id: uuid.UUID | None = None
    status: ObservationStatus = ObservationStatus.FINAL
    category: ObservationCategory | None = None

    # Coding
    code: str | None = Field(None, max_length=64, description="Code value (LOINC, SNOMED, etc.)")
    code_system: CodeSystem | None = None
    code_display: str | None = Field(None, max_length=255)

    # Timing
    effective_datetime: datetime | None = None
    issued: datetime | None = None

    # Value
    value_quantity: Decimal | None = None
    value_unit: str | None = Field(None, max_length=32)
    value_string: str | None = Field(None, max_length=500)
    value_boolean: bool | None = None
    value_integer: int | None = None
    value_codeable_concept: str | None = Field(None, max_length=64)

    # Reference ranges
    reference_range_low: Decimal | None = None
    reference_range_high: Decimal | None = None
    interpretation: str | None = Field(
        None, max_length=64,
        description="FHIR interpretation: 'N', 'H', 'L', 'HH', 'LL', 'A', 'AA'"
    )

    # Source
    source_system_id: uuid.UUID | None = None
    source_fragment_id: uuid.UUID | None = None
    performer_name: str | None = Field(None, max_length=255)
    performer_role: str | None = Field(None, max_length=128)
    performer_organization: str | None = Field(None, max_length=255)

    # Sensitivity
    is_42cfr_protected: bool = False
    is_sensitive: bool = False
    sensitivity_label: str | None = Field(None, max_length=64)

    # Components (for multi-value obs like blood pressure)
    components: list[dict[str, Any]] | None = None
    notes: str | None = Field(None, max_length=2000)


class ObservationCreate(ObservationBase):
    """Create a new observation."""
    pass


class ObservationUpdate(BaseModel):
    """Partial observation update."""

    model_config = ConfigDict(use_enum_values=True)

    status: ObservationStatus | None = None
    value_quantity: Decimal | None = None
    value_string: str | None = None
    interpretation: str | None = None
    notes: str | None = None


class ObservationRead(ObservationBase):
    """Full observation read response."""

    model_config = ConfigDict(from_attributes=True, use_enum_values=True)

    id: uuid.UUID
    fhir_resource_type: str | None
    fhir_resource_id: str | None
    fhir_system: str | None
    created_at: datetime
    updated_at: datetime


class ObservationSummary(BaseModel):
    """Lightweight observation for list/search responses."""

    model_config = ConfigDict(from_attributes=True, use_enum_values=True)

    id: uuid.UUID
    person_id: uuid.UUID
    category: ObservationCategory | None
    code: str | None
    code_display: str | None
    effective_datetime: datetime | None
    value_quantity: Decimal | None
    value_unit: str | None
    value_string: str | None
    interpretation: str | None
    status: ObservationStatus
    is_42cfr_protected: bool
