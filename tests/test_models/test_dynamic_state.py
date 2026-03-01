"""Tests for dynamic state models."""

from datetime import datetime

import pytest

from dome.models.dynamic_state import (
    BioState,
    MentalState,
    EconState,
    HousingState,
    FamilyState,
    JusticeState,
    EducationState,
    EligibilitySnapshot,
    EnrollmentSnapshot,
    ProgramState,
    DynamicState,
)


class TestBioState:
    def test_defaults(self):
        bio = BioState()
        assert bio.bmi is None
        assert bio.chronic_conditions == []
        assert bio.lipid_profile_known is False

    def test_with_conditions(self):
        bio = BioState(
            bmi=29.5,
            hba1c=6.2,
            chronic_conditions=["pre_diabetes", "hypertension"],
        )
        assert len(bio.chronic_conditions) == 2
        assert bio.hba1c == 6.2


class TestEconState:
    def test_employment_statuses(self):
        for status in ["FT", "PT", "gig", "unemployed", "NILF", "disabled", "retired"]:
            econ = EconState(employment_status=status)
            assert econ.employment_status == status


class TestHousingState:
    def test_all_statuses(self):
        for status in ["stable", "cost_burdened", "doubled_up", "shelter", "street", "institution"]:
            hs = HousingState(housing_status=status)
            assert hs.housing_status == status


class TestEligibilitySnapshot:
    def test_all_false(self):
        snap = EligibilitySnapshot()
        assert snap.medicaid is False
        assert snap.va_benefits is False

    def test_mixed(self, sample_eligibility_snapshot):
        snap = EligibilitySnapshot(**sample_eligibility_snapshot)
        assert snap.medicaid is True
        assert snap.medicare is False
        assert snap.snap is True


class TestDynamicState:
    def test_full_state(self, sample_eligibility_snapshot, sample_enrollment_snapshot):
        state = DynamicState(
            timestamp=datetime(2026, 1, 15, 10, 0),
            age_years=33.8,
            bio_state=BioState(bmi=29.5, chronic_conditions=["pre_diabetes"]),
            mental_state=MentalState(depression_severity=0.55),
            econ_state=EconState(employment_status="gig", current_annual_income=24000),
            housing_state=HousingState(housing_status="cost_burdened"),
            family_state=FamilyState(household_size=3, dependents_ages=[6, 4]),
            justice_state=JusticeState(),
            education_state=EducationState(highest_credential="some_college"),
            program_state=ProgramState(
                eligibility_snapshot=EligibilitySnapshot(**sample_eligibility_snapshot),
                enrollment_snapshot=EnrollmentSnapshot(**sample_enrollment_snapshot),
            ),
        )
        assert state.age_years == 33.8
        assert state.econ_state.employment_status == "gig"
        assert state.program_state.eligibility_snapshot.medicaid is True
