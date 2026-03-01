"""Request/response schemas for person endpoints."""

from __future__ import annotations

from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, Field


# ── Request schemas ──────────────────────────────────────────────────────────


class AddressEntryIn(BaseModel):
    street_hash: str
    city: str
    state: str
    zip5: str
    tract_fips: str
    start_date: date
    end_date: date | None = None


class CrossSystemIdsIn(BaseModel):
    irs_tin_hash: str | None = None
    ssa_beneficiary_id: str | None = None
    medicare_id: str | None = None
    medicaid_id: str | None = None
    chip_id: str | None = None
    snap_case_id: str | None = None
    tanf_case_id: str | None = None
    hud_client_id: str | None = None
    pha_household_id: str | None = None
    hmis_id: str | None = None
    state_prison_id: str | None = None
    county_jail_id: str | None = None
    court_case_ids: list[str] = Field(default_factory=list)
    school_district_student_id: str | None = None
    higher_ed_student_id: str | None = None
    unemployment_insurance_id: str | None = None
    wioa_participant_id: str | None = None
    va_id: str | None = None


class PersonCreateRequest(BaseModel):
    """Payload to create a new Person with full profile."""

    person_uid: str = Field(..., description="Unique person identifier")

    # Identity
    ssn_hash: str | None = None
    name_hash: str
    dob: date
    sex_at_birth: Literal["male", "female", "intersex", "unknown"]
    address_history: list[AddressEntryIn] = Field(default_factory=list)
    cross_system_ids: CrossSystemIdsIn = Field(default_factory=CrossSystemIdsIn)

    # Static profile
    birth_tract_fips: str = ""
    current_tract_fips: str = ""
    parental_income_quintile: int | None = None
    parental_education_level: Literal["<HS", "HS", "some_college", "BA", "Grad"] | None = None
    ace_score_estimate: float | None = None
    birth_weight_grams: float | None = None
    genetics_risk_flags: list[str] = Field(default_factory=list)

    # Dynamic state (simplified — caller can supply full JSON later)
    employment_status: Literal["FT", "PT", "gig", "unemployed", "NILF", "disabled", "retired"] = "FT"
    current_annual_income: float | None = None
    housing_status: Literal["stable", "cost_burdened", "doubled_up", "shelter", "street", "institution"] = "stable"
    household_size: int = 1
    dependents_ages: list[int] = Field(default_factory=list)
    chronic_conditions: list[str] = Field(default_factory=list)
    disability_flag: bool = False
    highest_credential: Literal["<HS", "HS", "some_college", "BA", "Grad"] = "HS"


class PersonSummaryResponse(BaseModel):
    """Lightweight person listing."""

    person_uid: str
    name_hash: str
    dob: date
    sex_at_birth: str
    current_tract_fips: str
    trajectory: str | None = None
    created_at: datetime | None = None


class FiscalEventCreateRequest(BaseModel):
    """Payload to add one fiscal event."""

    event_date: date
    payer_level: Literal["federal", "state", "local", "nonprofit", "health_system"]
    payer_entity: str
    program_or_fund: str
    domain: Literal[
        "healthcare", "income_support", "housing", "food",
        "education", "justice", "child_family", "transport", "other",
    ]
    mechanism: Literal["cash_transfer", "in_kind_benefit", "service_utilization", "tax_expenditure"]
    service_category: str
    utilization_unit: str = "occurrence"
    quantity: float | None = None
    amount_paid: float
    amount_type: Literal["actual_claim", "estimated_unit_cost"] = "actual_claim"
    confidence: float = Field(1.0, ge=0.0, le=1.0)
    data_source_system: str = "manual"
    attribution_tags: list[str] = Field(default_factory=list)
