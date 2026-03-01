"""Tests for benefits cliff calculator."""

import pytest

from dome.models.budget_key import PersonBudgetKey
from dome.models.dynamic_state import EligibilitySnapshot, EnrollmentSnapshot
from dome.engines.benefits_cliff import BenefitsCliffCalculator


class TestBenefitsCliffCalculator:
    def _make_key(self, household_size: int = 1, dependents: list[int] | None = None) -> PersonBudgetKey:
        return PersonBudgetKey(
            person_uid="test",
            age=34,
            sex_at_birth="female",
            current_tract_fips="42101002500",
            household_size=household_size,
            dependents_ages=dependents or [],
            current_annual_income=20000,
            income_volatility_score=0.5,
            employment_status="PT",
            educational_attainment="HS",
            disability_flag=False,
            chronic_condition_flags=[],
            high_need_flag=False,
            housing_status="cost_burdened",
            homelessness_history_flag=False,
            justice_involvement_flag=False,
            past_12m_jail_days=0,
            past_12m_prison_days=0,
            past_12m_police_contacts=0,
            eligibility_snapshot=EligibilitySnapshot(
                medicaid=True, snap=True, tanf=True, housing_assistance=True,
            ),
            enrollment_snapshot=EnrollmentSnapshot(
                medicaid=True, snap=True, tanf=True, housing_assistance=True,
            ),
            budget_horizons=[],
        )

    def test_produces_cliff_points(self):
        calc = BenefitsCliffCalculator()
        key = self._make_key()
        points = calc.analyze(key)
        assert len(points) > 0
        # Points should cover a range of incomes
        incomes = [p.income for p in points]
        assert min(incomes) == 0 or min(incomes) <= 1000
        assert max(incomes) >= 50000

    def test_identifies_cliffs(self):
        """There should be at least one cliff for a person on multiple programs."""
        calc = BenefitsCliffCalculator()
        key = self._make_key(household_size=3, dependents=[6, 4])
        points = calc.analyze(key)
        cliffs = [p for p in points if p.is_cliff]
        # Someone on Medicaid + SNAP + TANF + Housing should have cliffs
        assert len(cliffs) >= 1

    def test_emtr_at_cliff(self):
        """Effective marginal tax rate should exceed 80% at cliff points."""
        calc = BenefitsCliffCalculator()
        key = self._make_key(household_size=3, dependents=[6, 4])
        points = calc.analyze(key)
        cliffs = [p for p in points if p.is_cliff]
        for cliff in cliffs:
            assert cliff.effective_marginal_tax_rate > 0.80

    def test_net_resources_generally_increase(self):
        """Net resources should generally increase with income (ignoring cliffs)."""
        calc = BenefitsCliffCalculator()
        key = self._make_key()
        points = calc.analyze(key)
        # At very high income, net resources should be higher than at zero
        low = next((p for p in points if p.income == 0), None)
        high = next((p for p in points if p.income >= 80000), None)
        if low and high:
            assert high.net_resources > low.net_resources
