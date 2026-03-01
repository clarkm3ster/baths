"""Dynamic state models for THE DOME.

This module captures the *mutable* dimensions of a person's life at a
single point in time.  Eight orthogonal sub-state models cover biology,
mental health, economics, housing, family/social, justice, education,
and program eligibility/enrollment.  ``DynamicState`` composes them into
one timestamped snapshot.
"""

from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


# ------------------------------------------------------------------ #
#  Sub-state 1: Biology / Physical Health
# ------------------------------------------------------------------ #
class BioState(BaseModel):
    """Observable biometric and clinical indicators of physical health."""

    bmi: float | None = Field(default=None, ge=5, le=100, description="Body Mass Index.")
    blood_pressure_systolic: float | None = Field(
        default=None, ge=50, le=300, description="Systolic blood pressure (mmHg)."
    )
    blood_pressure_diastolic: float | None = Field(
        default=None, ge=20, le=200, description="Diastolic blood pressure (mmHg)."
    )
    hba1c: float | None = Field(
        default=None, ge=2.0, le=20.0, description="Hemoglobin A1c percentage."
    )
    lipid_profile_known: bool = Field(
        default=False, description="Whether a recent lipid panel is on file."
    )
    chronic_conditions: list[str] = Field(
        default_factory=list,
        description="ICD-10 or plain-text list of active chronic conditions.",
    )
    functional_limitations_score: float | None = Field(
        default=None,
        ge=0,
        le=100,
        description="Composite functional-limitation score (0=none, 100=total).",
    )


# ------------------------------------------------------------------ #
#  Sub-state 2: Mental / Behavioral Health
# ------------------------------------------------------------------ #
class MentalState(BaseModel):
    """Indicators of mental and behavioral health status."""

    depression_severity: float | None = Field(
        default=None,
        ge=0,
        le=27,
        description="PHQ-9 or equivalent depression severity score.",
    )
    anxiety_severity: float | None = Field(
        default=None,
        ge=0,
        le=21,
        description="GAD-7 or equivalent anxiety severity score.",
    )
    sud_severity: float | None = Field(
        default=None,
        ge=0,
        le=10,
        description="Substance use disorder severity score (0-10 scale).",
    )
    psychosis_flag: bool = Field(
        default=False, description="Active psychotic-spectrum diagnosis flag."
    )
    suicide_risk_score: float | None = Field(
        default=None,
        ge=0,
        le=1,
        description="Calibrated suicide risk probability (0-1).",
    )


# ------------------------------------------------------------------ #
#  Sub-state 3: Economic
# ------------------------------------------------------------------ #
class EconState(BaseModel):
    """Financial and employment indicators."""

    current_annual_income: float | None = Field(
        default=None, ge=0, description="Estimated current annual income (USD)."
    )
    income_volatility_score: float | None = Field(
        default=None,
        ge=0,
        le=1,
        description="Income volatility index (0=perfectly stable, 1=maximally volatile).",
    )
    employment_status: Literal[
        "FT", "PT", "gig", "unemployed", "NILF", "disabled", "retired"
    ] = Field(..., description="Current employment classification.")
    occupation_code: str | None = Field(
        default=None, description="SOC or O*NET occupation code."
    )
    assets_estimate: float | None = Field(
        default=None, description="Estimated total assets (USD)."
    )
    debts_estimate: float | None = Field(
        default=None, description="Estimated total debts (USD)."
    )


# ------------------------------------------------------------------ #
#  Sub-state 4: Housing
# ------------------------------------------------------------------ #
class HousingState(BaseModel):
    """Housing security and quality indicators."""

    housing_status: Literal[
        "stable", "cost_burdened", "doubled_up", "shelter", "street", "institution"
    ] = Field(..., description="Current housing stability classification.")
    rent_to_income_ratio: float | None = Field(
        default=None, ge=0, description="Monthly rent as a fraction of monthly income."
    )
    homelessness_history_flag: bool = Field(
        default=False, description="Whether the person has any prior episode of homelessness."
    )
    nights_homeless_past_year: int | None = Field(
        default=None, ge=0, description="Count of nights spent homeless in the past 12 months."
    )
    housing_quality_score: float | None = Field(
        default=None,
        ge=0,
        le=100,
        description="Composite housing-quality score (0-100).",
    )


# ------------------------------------------------------------------ #
#  Sub-state 5: Family / Social
# ------------------------------------------------------------------ #
class FamilyState(BaseModel):
    """Household composition and social-network indicators."""

    household_size: int = Field(..., ge=1, description="Number of persons in the household.")
    dependents_ages: list[int] = Field(
        default_factory=list,
        description="Ages of dependent children or elders in the household.",
    )
    caregiving_burden_score: float | None = Field(
        default=None,
        ge=0,
        le=100,
        description="Composite caregiving burden score (0-100).",
    )
    social_network_size: int | None = Field(
        default=None, ge=0, description="Estimated count of close social ties."
    )
    social_isolation_score: float | None = Field(
        default=None,
        ge=0,
        le=1,
        description="Social isolation index (0=well-connected, 1=fully isolated).",
    )


# ------------------------------------------------------------------ #
#  Sub-state 6: Justice
# ------------------------------------------------------------------ #
class JusticeState(BaseModel):
    """Criminal-justice involvement indicators."""

    justice_involvement_flag: bool = Field(
        default=False,
        description="Whether the person has any lifetime justice system involvement.",
    )
    past_12m_jail_days: int = Field(
        default=0, ge=0, description="Days spent in county jail in the past 12 months."
    )
    past_12m_prison_days: int = Field(
        default=0, ge=0, description="Days spent in state/federal prison in the past 12 months."
    )
    past_12m_police_contacts: int = Field(
        default=0, ge=0, description="Police contacts (stops, arrests) in the past 12 months."
    )
    current_supervision_status: str | None = Field(
        default=None,
        description="Current community-supervision status, e.g. 'probation', 'parole', 'pretrial'.",
    )


# ------------------------------------------------------------------ #
#  Sub-state 7: Education
# ------------------------------------------------------------------ #
class EducationState(BaseModel):
    """Educational attainment and enrollment indicators."""

    highest_credential: Literal["<HS", "HS", "some_college", "BA", "Grad"] = Field(
        ..., description="Highest educational credential earned."
    )
    currently_enrolled_flag: bool = Field(
        default=False, description="Whether the person is currently enrolled in any educational program."
    )
    special_ed_history_flag: bool = Field(
        default=False, description="Whether the person has any history of special-education services."
    )
    literacy_score: float | None = Field(
        default=None,
        ge=0,
        le=500,
        description="Assessed literacy proficiency score (e.g. PIAAC 0-500 scale).",
    )


# ------------------------------------------------------------------ #
#  Sub-state 8: Program eligibility & enrollment
# ------------------------------------------------------------------ #
class EligibilitySnapshot(BaseModel):
    """Point-in-time eligibility flags for major public programs."""

    medicaid: bool = Field(default=False, description="Eligible for Medicaid.")
    medicare: bool = Field(default=False, description="Eligible for Medicare.")
    marketplace_subsidy: bool = Field(
        default=False, description="Eligible for ACA marketplace premium subsidy."
    )
    snap: bool = Field(default=False, description="Eligible for SNAP (food assistance).")
    tanf: bool = Field(
        default=False,
        description="Eligible for Temporary Assistance for Needy Families.",
    )
    housing_assistance: bool = Field(
        default=False, description="Eligible for federal housing assistance."
    )
    ssi: bool = Field(
        default=False, description="Eligible for Supplemental Security Income."
    )
    ssdi: bool = Field(
        default=False, description="Eligible for Social Security Disability Insurance."
    )
    unemployment_insurance: bool = Field(
        default=False, description="Eligible for unemployment insurance."
    )
    wioa: bool = Field(
        default=False,
        description="Eligible for Workforce Innovation and Opportunity Act services.",
    )
    va_benefits: bool = Field(
        default=False, description="Eligible for VA benefits."
    )


class EnrollmentSnapshot(BaseModel):
    """Point-in-time enrollment flags for major public programs."""

    medicaid: bool = Field(default=False, description="Currently enrolled in Medicaid.")
    medicare: bool = Field(default=False, description="Currently enrolled in Medicare.")
    marketplace_subsidy: bool = Field(
        default=False, description="Currently receiving ACA marketplace premium subsidy."
    )
    snap: bool = Field(default=False, description="Currently enrolled in SNAP.")
    tanf: bool = Field(default=False, description="Currently enrolled in TANF.")
    housing_assistance: bool = Field(
        default=False, description="Currently receiving federal housing assistance."
    )
    ssi: bool = Field(default=False, description="Currently receiving SSI.")
    ssdi: bool = Field(default=False, description="Currently receiving SSDI.")
    unemployment_insurance: bool = Field(
        default=False, description="Currently receiving unemployment insurance."
    )
    wioa: bool = Field(default=False, description="Currently enrolled in WIOA services.")
    va_benefits: bool = Field(
        default=False, description="Currently receiving VA benefits."
    )


class ProgramState(BaseModel):
    """Combined program eligibility and enrollment at a point in time."""

    eligibility_snapshot: EligibilitySnapshot = Field(
        default_factory=EligibilitySnapshot,
        description="Current program eligibility flags.",
    )
    enrollment_snapshot: EnrollmentSnapshot = Field(
        default_factory=EnrollmentSnapshot,
        description="Current program enrollment flags.",
    )


# ------------------------------------------------------------------ #
#  Composite: DynamicState
# ------------------------------------------------------------------ #
class DynamicState(BaseModel):
    """Full mutable state of a person at a single point in time.

    This is the timestamped union of all eight sub-state models.  A new
    ``DynamicState`` is generated on every observation cycle or event
    trigger.
    """

    timestamp: datetime = Field(
        ..., description="UTC timestamp of this state snapshot."
    )
    age_years: float = Field(
        ..., ge=0, description="Exact age in fractional years at snapshot time."
    )
    bio_state: BioState = Field(
        default_factory=BioState, description="Physical-health sub-state."
    )
    mental_state: MentalState = Field(
        default_factory=MentalState, description="Mental/behavioral-health sub-state."
    )
    econ_state: EconState = Field(
        ..., description="Economic sub-state."
    )
    housing_state: HousingState = Field(
        ..., description="Housing sub-state."
    )
    family_state: FamilyState = Field(
        ..., description="Family/social sub-state."
    )
    justice_state: JusticeState = Field(
        default_factory=JusticeState, description="Justice-involvement sub-state."
    )
    education_state: EducationState = Field(
        ..., description="Education sub-state."
    )
    program_state: ProgramState = Field(
        default_factory=ProgramState,
        description="Program eligibility and enrollment sub-state.",
    )
