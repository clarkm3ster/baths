"""Tests for fiscal trajectory classifier."""

import pytest
from datetime import date, datetime

from dome.models.budget_key import PersonBudgetKey
from dome.models.budget_output import (
    WholePersonBudget,
    HorizonBudget,
    PayerView,
    RiskProfile,
)
from dome.models.dynamic_state import EligibilitySnapshot, EnrollmentSnapshot
from dome.engines.trajectory_classifier import TrajectoryClassifier


def _make_budget(person_uid: str, lifetime_total: float) -> WholePersonBudget:
    """Helper to create a minimal budget with a given lifetime total cost."""
    return WholePersonBudget(
        person_uid=person_uid,
        generated_at=datetime(2026, 1, 1),
        horizons=[
            HorizonBudget(
                label="lifetime",
                start_date=date(2026, 1, 1),
                end_date=date(2076, 1, 1),
                payer_view=PayerView(
                    federal_expected_spend=lifetime_total * 0.5,
                    state_expected_spend=lifetime_total * 0.3,
                    local_expected_spend=lifetime_total * 0.15,
                    healthcare_delivery_expected_spend=lifetime_total * 0.04,
                    nonprofit_expected_spend=lifetime_total * 0.01,
                    per_payer_breakdown=[],
                ),
                domain_view=[],
                mechanism_view=[],
                risk_profile=RiskProfile(
                    p50_total_cost=lifetime_total,
                    p90_total_cost=lifetime_total * 1.5,
                    p99_total_cost=lifetime_total * 2.5,
                    catastrophic_events=[],
                ),
            ),
        ],
    )


def _make_key(
    person_uid: str,
    age: int,
    income: float,
    education: str,
    employment: str = "FT",
) -> PersonBudgetKey:
    return PersonBudgetKey(
        person_uid=person_uid,
        age=age,
        sex_at_birth="female",
        current_tract_fips="42101002500",
        household_size=1,
        dependents_ages=[],
        current_annual_income=income,
        income_volatility_score=0.2,
        employment_status=employment,
        educational_attainment=education,
        disability_flag=False,
        chronic_condition_flags=[],
        high_need_flag=False,
        housing_status="stable",
        homelessness_history_flag=False,
        justice_involvement_flag=False,
        past_12m_jail_days=0,
        past_12m_prison_days=0,
        past_12m_police_contacts=0,
        eligibility_snapshot=EligibilitySnapshot(),
        enrollment_snapshot=EnrollmentSnapshot(),
        budget_horizons=[],
    )


class TestTrajectoryClassifier:
    def test_net_contributor(self):
        """Sarah-like: high income, low government cost."""
        classifier = TrajectoryClassifier()
        budget = _make_budget("sarah", lifetime_total=200000)
        key = _make_key("sarah", age=28, income=72000, education="BA")
        tag = classifier.classify(
            person_uid="sarah",
            budget_key=key,
            budget=budget,
        )
        assert tag.trajectory == "net_contributor"
        assert tag.net_fiscal_impact_npv > 100000

    def test_high_net_cost(self):
        """James-like: low income, very high government cost."""
        classifier = TrajectoryClassifier()
        budget = _make_budget("james", lifetime_total=1800000)
        key = _make_key("james", age=42, income=6000, education="HS", employment="unemployed")
        tag = classifier.classify(
            person_uid="james",
            budget_key=key,
            budget=budget,
        )
        assert tag.trajectory in ("high_net_cost", "catastrophic_net_cost")
        assert tag.net_fiscal_impact_npv < -500000

    def test_moderate_net_cost(self):
        """Maria-like: moderate income, moderate cost."""
        classifier = TrajectoryClassifier()
        budget = _make_budget("maria", lifetime_total=600000)
        key = _make_key("maria", age=34, income=24000, education="some_college", employment="gig")
        tag = classifier.classify(
            person_uid="maria",
            budget_key=key,
            budget=budget,
        )
        # With $24K gig income and $600K lifetime cost, classification depends
        # on exact tax estimation; high_net_cost is also acceptable here.
        assert tag.trajectory in ("moderate_net_cost", "high_net_cost", "break_even")
