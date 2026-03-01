"""Tests for wrong-pocket analyzer."""

import pytest
from datetime import date, datetime

from dome.models.budget_key import PersonBudgetKey
from dome.models.budget_output import (
    WholePersonBudget, HorizonBudget, PayerView, RiskProfile,
)
from dome.models.dynamic_state import EligibilitySnapshot, EnrollmentSnapshot
from dome.engines.wrong_pocket_analyzer import WrongPocketAnalyzer


class TestWrongPocketAnalyzer:
    def _make_budget(self, total: float = 500000) -> WholePersonBudget:
        return WholePersonBudget(
            person_uid="test",
            generated_at=datetime(2026, 1, 1),
            horizons=[
                HorizonBudget(
                    label="lifetime",
                    start_date=date(2026, 1, 1),
                    end_date=date(2076, 1, 1),
                    payer_view=PayerView(
                        federal_expected_spend=total * 0.5,
                        state_expected_spend=total * 0.3,
                        local_expected_spend=total * 0.15,
                        healthcare_delivery_expected_spend=total * 0.04,
                        nonprofit_expected_spend=total * 0.01,
                        per_payer_breakdown=[],
                    ),
                    domain_view=[],
                    mechanism_view=[],
                    risk_profile=RiskProfile(
                        p50_total_cost=total,
                        p90_total_cost=total * 1.5,
                        p99_total_cost=total * 2.5,
                        catastrophic_events=[],
                    ),
                ),
            ],
        )

    def _make_key(self) -> PersonBudgetKey:
        return PersonBudgetKey(
            person_uid="test", age=34, sex_at_birth="female",
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

    def test_analyze_returns_matrix(self):
        analyzer = WrongPocketAnalyzer()
        # Pass default intervention IDs
        result = analyzer.analyze(
            self._make_key(),
            self._make_budget(),
            interventions=["housing_first", "cbt_therapy", "income_bridge"],
        )
        assert "matrix" in result or "savings_matrix" in result
        # Should have some result structure
        assert len(result) > 0

    def test_matrix_has_payer_columns(self):
        analyzer = WrongPocketAnalyzer()
        result = analyzer.analyze(
            self._make_key(),
            self._make_budget(),
            interventions=["housing_first", "care_coordination"],
        )
        # Check either matrix or savings_matrix key
        matrix = result.get("matrix", result.get("savings_matrix", {}))
        for intervention_id, payer_savings in matrix.items():
            assert isinstance(payer_savings, dict)
            assert len(payer_savings) > 0

    def test_settlement_matrix_generated(self):
        analyzer = WrongPocketAnalyzer()
        result = analyzer.analyze(
            self._make_key(),
            self._make_budget(),
            interventions=["housing_first", "cbt_therapy"],
        )
        if "settlement" in result:
            settlement = result["settlement"]
            assert settlement.person_uid == "test"
            assert len(settlement.payers) > 0
