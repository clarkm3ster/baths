"""Tests for budget key and output models."""

from datetime import date, datetime

import pytest

from dome.models.budget_key import BudgetHorizon, PersonBudgetKey
from dome.models.budget_output import (
    CatastrophicEventRisk,
    DomainBudget,
    HorizonBudget,
    MechanismBudget,
    PayerBreakdown,
    PayerView,
    ProgramSpend,
    RiskProfile,
    ScenarioBudget,
    WholePersonBudget,
)
from dome.models.dynamic_state import EligibilitySnapshot, EnrollmentSnapshot


class TestBudgetHorizon:
    def test_valid_horizon(self):
        h = BudgetHorizon(
            label="1y",
            start_date=date(2026, 1, 1),
            end_date=date(2027, 1, 1),
            time_step="month",
        )
        assert h.label == "1y"

    def test_all_labels(self):
        for label in ["1y", "5y", "20y", "lifetime"]:
            h = BudgetHorizon(
                label=label,
                start_date=date(2026, 1, 1),
                end_date=date(2076, 1, 1),
                time_step="year",
            )
            assert h.label == label


class TestPersonBudgetKey:
    def test_from_dict(self, sample_budget_key):
        key = PersonBudgetKey(**sample_budget_key)
        assert key.person_uid == "dome-maria-034"
        assert key.age == 34
        assert len(key.budget_horizons) == 2
        assert key.eligibility_snapshot.medicaid is True


class TestWholePersonBudget:
    def test_minimal_budget(self):
        budget = WholePersonBudget(
            person_uid="test-001",
            generated_at=datetime(2026, 1, 15, 10, 0),
            horizons=[
                HorizonBudget(
                    label="1y",
                    start_date=date(2026, 1, 1),
                    end_date=date(2027, 1, 1),
                    payer_view=PayerView(
                        federal_expected_spend=20600.0,
                        state_expected_spend=10800.0,
                        local_expected_spend=7200.0,
                        healthcare_delivery_expected_spend=3000.0,
                        nonprofit_expected_spend=500.0,
                        per_payer_breakdown=[],
                    ),
                    domain_view=[
                        DomainBudget(
                            domain="healthcare",
                            expected_spend=18000.0,
                            per_program=[
                                ProgramSpend(program_or_fund="Medicaid", expected_spend=16000.0),
                            ],
                        ),
                    ],
                    mechanism_view=[
                        MechanismBudget(mechanism="service_utilization", expected_spend=18000.0),
                    ],
                    risk_profile=RiskProfile(
                        p50_total_cost=42100.0,
                        p90_total_cost=68000.0,
                        p99_total_cost=120000.0,
                        catastrophic_events=[],
                    ),
                ),
            ],
        )
        assert budget.person_uid == "test-001"
        assert budget.horizons[0].payer_view.federal_expected_spend == 20600.0

    def test_with_scenario(self):
        scenario = ScenarioBudget(
            scenario_id="dome-active",
            description="DOME active intervention",
            incremental_cost_of_scenario=15000.0,
            expected_total_cost_under_scenario=30000.0,
            expected_savings_vs_baseline=12000.0,
            savings_by_payer=[
                PayerBreakdown(payer_level="federal", payer_entity="CMS-Medicaid", expected_spend=-8000.0),
            ],
        )
        assert scenario.expected_savings_vs_baseline == 12000.0
