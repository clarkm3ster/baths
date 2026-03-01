"""Tests for the Monte Carlo whole-life simulator."""

import pytest
from datetime import datetime

from dome.models.dynamic_state import (
    BioState, MentalState, EconState, HousingState, FamilyState,
    JusticeState, EducationState, ProgramState,
    EligibilitySnapshot, EnrollmentSnapshot, DynamicState,
)
from dome.models.budget_key import PersonBudgetKey, BudgetHorizon
from dome.engines.simulator import LifeSimulator


def _maria_state() -> DynamicState:
    return DynamicState(
        timestamp=datetime(2026, 1, 15),
        age_years=34.0,
        bio_state=BioState(bmi=29.5, hba1c=6.2, chronic_conditions=["pre_diabetes"]),
        mental_state=MentalState(depression_severity=0.55),
        econ_state=EconState(employment_status="gig", current_annual_income=24000),
        housing_state=HousingState(housing_status="cost_burdened", rent_to_income_ratio=0.48),
        family_state=FamilyState(household_size=3, dependents_ages=[6, 4]),
        justice_state=JusticeState(),
        education_state=EducationState(highest_credential="some_college"),
        program_state=ProgramState(
            eligibility_snapshot=EligibilitySnapshot(medicaid=True, snap=True),
            enrollment_snapshot=EnrollmentSnapshot(medicaid=True, snap=True),
        ),
    )


class TestLifeSimulator:
    def test_simulate_produces_results(self):
        simulator = LifeSimulator()
        state = _maria_state()
        key = PersonBudgetKey(
            person_uid="dome-maria-034", age=34, sex_at_birth="female",
            current_tract_fips="42101002500", household_size=3,
            dependents_ages=[6, 4], current_annual_income=24000,
            income_volatility_score=0.65, employment_status="gig",
            educational_attainment="some_college", disability_flag=False,
            chronic_condition_flags=["pre_diabetes"],
            high_need_flag=False, housing_status="cost_burdened",
            homelessness_history_flag=False, justice_involvement_flag=False,
            past_12m_jail_days=0, past_12m_prison_days=0, past_12m_police_contacts=0,
            eligibility_snapshot=EligibilitySnapshot(medicaid=True, snap=True),
            enrollment_snapshot=EnrollmentSnapshot(medicaid=True, snap=True),
            budget_horizons=[],
        )
        result = simulator.simulate(state, key, fiscal_history=[], iterations=100, projection_years=30)

        assert result.path_a_median > 0
        assert result.path_b_median > 0
        assert result.path_a_median > result.path_b_median  # dome should save money
        assert result.dome_roi > 0
        assert result.iterations_run == 100

    def test_path_b_cheaper_than_path_a(self):
        """DOME intervention should produce lower costs on path B."""
        simulator = LifeSimulator()
        state = _maria_state()
        key = PersonBudgetKey(
            person_uid="test", age=34, sex_at_birth="female",
            current_tract_fips="42101002500", household_size=3,
            dependents_ages=[6, 4], current_annual_income=24000,
            income_volatility_score=0.65, employment_status="gig",
            educational_attainment="some_college", disability_flag=False,
            chronic_condition_flags=["pre_diabetes", "hypertension"],
            high_need_flag=False, housing_status="cost_burdened",
            homelessness_history_flag=False, justice_involvement_flag=False,
            past_12m_jail_days=0, past_12m_prison_days=0, past_12m_police_contacts=0,
            eligibility_snapshot=EligibilitySnapshot(medicaid=True, snap=True),
            enrollment_snapshot=EnrollmentSnapshot(medicaid=True, snap=True),
            budget_horizons=[],
        )
        result = simulator.simulate(state, key, [], iterations=200, projection_years=40)
        assert result.path_b_median < result.path_a_median
