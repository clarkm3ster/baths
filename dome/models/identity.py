"""Identity models for THE DOME.

This module defines the core identity constructs used to link a single
person across every public-system silo: address history, cross-system
identifiers, and the master IdentitySpine that ties them together.
"""

from __future__ import annotations

from datetime import date
from typing import Literal

from pydantic import BaseModel, Field, model_validator


class AddressEntry(BaseModel):
    """A single geocoded address interval for a person.

    Each entry records a hashed street address, its geographic identifiers, and
    the date window during which the person was known to reside there.
    """

    street_hash: str = Field(
        ..., description="One-way hash of the street-level address for privacy."
    )
    city: str = Field(..., description="City name.")
    state: str = Field(
        ..., min_length=2, max_length=2, description="Two-letter US state code."
    )
    zip5: str = Field(
        ...,
        pattern=r"^\d{5}$",
        description="Five-digit ZIP code.",
    )
    tract_fips: str = Field(
        ...,
        pattern=r"^\d{11}$",
        description="11-digit Census tract FIPS code.",
    )
    start_date: date = Field(
        ..., description="Date the person began residing at this address."
    )
    end_date: date | None = Field(
        default=None,
        description="Date the person left this address.  None means current.",
    )

    @model_validator(mode="after")
    def _end_after_start(self) -> "AddressEntry":
        if self.end_date is not None and self.end_date < self.start_date:
            raise ValueError("end_date must be on or after start_date")
        return self


class CrossSystemIds(BaseModel):
    """Optional identifiers from every major public-system silo.

    All values are either hashed or opaque IDs; no PII is stored in
    clear-text.
    """

    ssn_hash: str | None = Field(
        default=None, description="One-way hash of the Social Security Number."
    )
    irs_tin_hash: str | None = Field(
        default=None,
        description="One-way hash of the IRS Taxpayer Identification Number.",
    )
    ssa_beneficiary_id: str | None = Field(
        default=None, description="Social Security Administration beneficiary ID."
    )
    medicare_id: str | None = Field(
        default=None, description="Medicare Beneficiary Identifier (MBI)."
    )
    medicaid_id: str | None = Field(
        default=None, description="State Medicaid ID."
    )
    chip_id: str | None = Field(
        default=None,
        description="Children's Health Insurance Program ID.",
    )
    snap_case_id: str | None = Field(
        default=None, description="SNAP (food assistance) case ID."
    )
    tanf_case_id: str | None = Field(
        default=None,
        description="Temporary Assistance for Needy Families case ID.",
    )
    hud_client_id: str | None = Field(
        default=None,
        description="HUD housing-assistance client ID.",
    )
    pha_household_id: str | None = Field(
        default=None,
        description="Public Housing Authority household ID.",
    )
    hmis_id: str | None = Field(
        default=None,
        description="Homeless Management Information System ID.",
    )
    state_prison_id: str | None = Field(
        default=None, description="State prison inmate ID."
    )
    county_jail_id: str | None = Field(
        default=None, description="County jail booking ID."
    )
    court_case_ids: list[str] = Field(
        default_factory=list,
        description="Court case identifiers associated with this person.",
    )
    school_district_student_id: str | None = Field(
        default=None,
        description="K-12 school-district student ID.",
    )
    higher_ed_student_id: str | None = Field(
        default=None,
        description="Post-secondary / higher-education student ID.",
    )
    unemployment_insurance_id: str | None = Field(
        default=None,
        description="State unemployment-insurance claimant ID.",
    )
    wioa_participant_id: str | None = Field(
        default=None,
        description="Workforce Innovation and Opportunity Act participant ID.",
    )
    va_id: str | None = Field(
        default=None, description="Department of Veterans Affairs ID."
    )


class IdentitySpine(BaseModel):
    """Master identity record that links a single human being across systems.

    The spine combines privacy-preserving hashes with demographic anchors and
    a confidence score per linked system so that downstream engines can
    reason about linkage quality.
    """

    ssn_hash: str | None = Field(
        default=None, description="One-way hash of SSN, if available."
    )
    name_hash: str = Field(
        ..., description="One-way hash of canonical full name."
    )
    dob: date = Field(..., description="Date of birth.")
    sex_at_birth: Literal["male", "female", "intersex", "unknown"] = Field(
        ..., description="Sex assigned at birth."
    )
    address_history: list[AddressEntry] = Field(
        default_factory=list,
        description="Chronological list of known residential addresses.",
    )
    cross_system_ids: CrossSystemIds = Field(
        default_factory=CrossSystemIds,
        description="Identifiers from every linked public-system silo.",
    )
    linkage_confidence_by_system: dict[str, float] = Field(
        default_factory=dict,
        description=(
            "Map of system name to linkage-confidence score (0-1). "
            "E.g. {'medicaid': 0.97, 'snap': 0.85}."
        ),
    )
