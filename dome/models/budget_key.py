"""Budget key models for THE DOME.

A ``PersonBudgetKey`` captures every person-level attribute that the
Whole-Person Budget engine needs to project costs across multiple time
horizons.  ``BudgetHorizon`` defines the time windows over which projections
are computed.
"""

from __future__ import annotations

from datetime import date
from typing import Literal

from pydantic import BaseModel, Field, model_validator

from dome.models.dynamic_state import EligibilitySnapshot, EnrollmentSnapshot


class BudgetHorizon(BaseModel):
    """A single projection window for the Whole-Person Budget.

    Each horizon defines a label (e.g. ``"5y"``), a calendar window, and the
    temporal granularity at which costs are aggregated.
    """

    label: Literal["1y", "5y", "20y", "lifetime"] = Field(
        ..., description="Human-readable horizon label."
    )
    start_date: date = Field(
        ..., description="Inclusive start date of the projection window."
    )
    end_date: date = Field(
        ..., description="Inclusive end date of the projection window."
    )
    time_step: Literal["month", "quarter", "year"] = Field(
        ..., description="Temporal granularity for cost aggregation."
    )

    @model_validator(mode="after")
    def _end_after_start(self) -> "BudgetHorizon":
        if self.end_date < self.start_date:
            raise ValueError("end_date must be on or after start_date")
        return self


class PersonBudgetKey(BaseModel):
    """All person-level inputs the budget engine needs to project costs.

    This key collects demographic, economic, clinical, housing, justice, and
    program-enrollment attributes -- plus the requested projection horizons
    -- so that the engine can produce a ``WholePersonBudget`` in a single
    deterministic call.
    """

    person_uid: str = Field(
        ..., description="Unique person identifier linking to the IdentitySpine."
    )
    age: int = Field(
        ..., ge=0, le=150, description="Current age in whole years."
    )
    sex_at_birth: str = Field(
        ..., description="Sex assigned at birth (e.g. 'male', 'female')."
    )
    current_tract_fips: str = Field(
        ...,
        pattern=r"^\d{11}$",
        description="11-digit Census tract FIPS code of current residence.",
    )
    household_size: int = Field(
        ..., ge=1, description="Number of persons in the household."
    )
    dependents_ages: list[int] = Field(
        default_factory=list,
        description="Ages of dependent children or elders in the household.",
    )
    current_annual_income: float | None = Field(
        default=None, ge=0, description="Estimated current annual income (USD)."
    )
    income_volatility_score: float | None = Field(
        default=None,
        ge=0,
        le=1,
        description="Income volatility index (0=stable, 1=maximally volatile).",
    )
    employment_status: str = Field(
        ...,
        description=(
            "Current employment classification "
            "(e.g. 'FT', 'PT', 'unemployed', 'disabled')."
        ),
    )
    occupation_code: str | None = Field(
        default=None, description="SOC or O*NET occupation code."
    )
    educational_attainment: str = Field(
        ...,
        description=(
            "Highest educational credential "
            "(e.g. '<HS', 'HS', 'some_college', 'BA', 'Grad')."
        ),
    )
    disability_flag: bool = Field(
        default=False,
        description="Whether the person has a qualifying disability.",
    )
    chronic_condition_flags: list[str] = Field(
        default_factory=list,
        description="Active chronic condition codes or labels.",
    )
    high_need_flag: bool = Field(
        default=False,
        description=(
            "Whether the person is classified as high-need "
            "(e.g. top-5%% projected cost)."
        ),
    )
    housing_status: str = Field(
        ...,
        description=(
            "Housing stability classification "
            "(e.g. 'stable', 'cost_burdened', 'shelter')."
        ),
    )
    homelessness_history_flag: bool = Field(
        default=False,
        description="Whether the person has any prior episode of homelessness.",
    )
    area_deprivation_index: float | None = Field(
        default=None,
        ge=0,
        le=100,
        description="Census-tract Area Deprivation Index (0-100 percentile).",
    )
    justice_involvement_flag: bool = Field(
        default=False,
        description="Any lifetime justice-system involvement.",
    )
    past_12m_jail_days: int = Field(
        default=0,
        ge=0,
        description="Days spent in county jail in the past 12 months.",
    )
    past_12m_prison_days: int = Field(
        default=0,
        ge=0,
        description="Days spent in state/federal prison in the past 12 months.",
    )
    past_12m_police_contacts: int = Field(
        default=0,
        ge=0,
        description="Police contacts (stops, arrests) in the past 12 months.",
    )
    eligibility_snapshot: EligibilitySnapshot = Field(
        default_factory=EligibilitySnapshot,
        description="Current program-eligibility flags.",
    )
    enrollment_snapshot: EnrollmentSnapshot = Field(
        default_factory=EnrollmentSnapshot,
        description="Current program-enrollment flags.",
    )
    budget_horizons: list[BudgetHorizon] = Field(
        default_factory=list,
        description="Projection horizons to compute budgets for.",
    )
