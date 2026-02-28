"""
DOMES v2 — Person Pydantic Schemas

Input/output schemas for the Person model. These are the primary
API-facing types used for request validation and response serialization.

Note on design:
- PersonBase: shared fields
- PersonCreate: input validation for new persons
- PersonUpdate: partial update (all fields optional)
- PersonRead: full read response (includes computed fields)
- PersonSummary: lightweight list/search response

SSN is never returned in any read schema — only accepted in write schemas
and immediately hashed before storage.
"""
from __future__ import annotations

import hashlib
import re
import uuid
from datetime import date, datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from domes.enums import (
    EmploymentStatus,
    Ethnicity,
    Gender,
    HousingStatus,
    ImmigrationStatus,
    Race,
)


# ---------------------------------------------------------------------------
# Base schema — shared fields
# ---------------------------------------------------------------------------

class PersonBase(BaseModel):
    """Shared fields for Person create/update."""

    model_config = ConfigDict(from_attributes=True, use_enum_values=True)

    # Legal name
    first_name: str | None = Field(None, max_length=100, description="Legal first name")
    middle_name: str | None = Field(None, max_length=100, description="Middle name (optional)")
    last_name: str | None = Field(None, max_length=100, description="Legal last name")
    preferred_name: str | None = Field(None, max_length=100, description="Preferred/chosen name")
    name_suffix: str | None = Field(None, max_length=20, description="Jr., Sr., III, etc.")

    # Demographics
    date_of_birth: date | None = Field(None, description="Date of birth")
    gender: Gender | None = Field(None, description="Gender identity")
    race: Race | None = Field(None, description="Race")
    ethnicity: Ethnicity | None = Field(None, description="Hispanic/Latino ethnicity")
    primary_language: str | None = Field(None, max_length=32, description="Primary language (ISO 639-1)")
    secondary_languages: list[str] | None = Field(None, description="Additional languages spoken")

    # Location
    city: str | None = Field(None, max_length=100)
    state: str | None = Field(None, max_length=2, description="2-letter state code")
    county: str | None = Field(None, max_length=100)
    zip_code: str | None = Field(None, max_length=10)
    census_tract: str | None = Field(None, max_length=16)

    # Situational
    housing_status: HousingStatus | None = Field(None)
    employment_status: EmploymentStatus | None = Field(None)
    immigration_status: ImmigrationStatus | None = Field(None)
    veteran: bool | None = Field(None, description="Self-reported veteran status")
    chronic_homelessness: bool | None = Field(None, description="HUD chronically homeless criteria")

    # Government identifiers (write-only — never returned in reads)
    medicaid_id: str | None = Field(None, max_length=50)
    medicare_id: str | None = Field(None, max_length=50)
    snap_case_number: str | None = Field(None, max_length=50)
    va_patient_id: str | None = Field(None, max_length=50)
    hmis_client_id: str | None = Field(None, max_length=50)
    probation_case_number: str | None = Field(None, max_length=50)


# ---------------------------------------------------------------------------
# Create schema
# ---------------------------------------------------------------------------

class PersonCreate(PersonBase):
    """Schema for creating a new person. SSN accepted here and immediately hashed."""

    # At least one name or DOB required
    first_name: str = Field(..., max_length=100, description="Legal first name")
    last_name: str = Field(..., max_length=100, description="Legal last name")

    # SSN — accepted in plain text, hashed before storage, never stored plaintext
    ssn: str | None = Field(
        None,
        min_length=9,
        max_length=11,
        description="Social Security Number (XXX-XX-XXXX or XXXXXXXXX). Hashed before storage.",
    )

    @field_validator("ssn")
    @classmethod
    def hash_ssn(cls, v: str | None) -> str | None:
        """Validate SSN format and return — the model layer will hash it."""
        if v is None:
            return None
        cleaned = re.sub(r"[^0-9]", "", v)
        if len(cleaned) != 9:
            raise ValueError("SSN must be exactly 9 digits")
        return cleaned

    @field_validator("state")
    @classmethod
    def validate_state(cls, v: str | None) -> str | None:
        if v is not None:
            return v.upper()
        return v

    @field_validator("date_of_birth")
    @classmethod
    def validate_dob(cls, v: date | None) -> date | None:
        if v is not None and v > date.today():
            raise ValueError("Date of birth cannot be in the future")
        return v

    def to_ssn_hash(self) -> str | None:
        """Return SHA-256 hash of the SSN for storage."""
        if self.ssn is None:
            return None
        return hashlib.sha256(self.ssn.encode()).hexdigest()


# ---------------------------------------------------------------------------
# Update schema
# ---------------------------------------------------------------------------

class PersonUpdate(PersonBase):
    """Schema for partial updates — every field optional."""
    pass


# ---------------------------------------------------------------------------
# Read schemas
# ---------------------------------------------------------------------------

class PersonRead(BaseModel):
    """Full person read response — returned by GET /persons/{id}."""

    model_config = ConfigDict(from_attributes=True, use_enum_values=True)

    id: uuid.UUID
    first_name: str | None
    middle_name: str | None
    last_name: str | None
    preferred_name: str | None
    name_suffix: str | None

    date_of_birth: date | None
    age: int | None = None  # Computed on response

    gender: Gender | None
    race: Race | None
    ethnicity: Ethnicity | None
    primary_language: str | None
    secondary_languages: list[str] | None

    city: str | None
    state: str | None
    county: str | None
    zip_code: str | None
    census_tract: str | None

    housing_status: HousingStatus | None
    housing_status_since: date | None = None
    employment_status: EmploymentStatus | None
    immigration_status: ImmigrationStatus | None

    veteran: bool | None
    chronic_homelessness: bool | None
    years_homeless: float | None = None

    # Government IDs included in read (no SSN ever)
    medicaid_id: str | None
    medicare_id: str | None
    snap_case_number: str | None
    va_patient_id: str | None
    hmis_client_id: str | None
    probation_case_number: str | None

    # FHIR
    fhir_resource_type: str | None
    fhir_resource_id: str | None
    fhir_system: str | None

    # Audit
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None

    @model_validator(mode="after")
    def compute_age(self) -> PersonRead:
        """Compute age from date_of_birth."""
        if self.date_of_birth is not None:
            today = date.today()
            self.age = (
                today.year
                - self.date_of_birth.year
                - (
                    (today.month, today.day)
                    < (self.date_of_birth.month, self.date_of_birth.day)
                )
            )
        return self


class PersonSummary(BaseModel):
    """Lightweight person summary for search/list responses."""

    model_config = ConfigDict(from_attributes=True, use_enum_values=True)

    id: uuid.UUID
    first_name: str | None
    last_name: str | None
    preferred_name: str | None
    date_of_birth: date | None
    age: int | None = None
    gender: Gender | None
    race: Race | None
    housing_status: HousingStatus | None
    chronic_homelessness: bool | None
    city: str | None
    state: str | None
    hmis_client_id: str | None
    medicaid_id: str | None

    @model_validator(mode="after")
    def compute_age(self) -> PersonSummary:
        if self.date_of_birth is not None:
            today = date.today()
            self.age = (
                today.year
                - self.date_of_birth.year
                - (
                    (today.month, today.day)
                    < (self.date_of_birth.month, self.date_of_birth.day)
                )
            )
        return self
