"""Tests for the budget engine — THE SKELETON KEY."""

import pytest

from dome.models.budget_key import PersonBudgetKey
from dome.models.fiscal_event import FiscalEvent
from dome.engines.budget_engine import BudgetEngine


class TestBudgetEngine:
    def test_compute_budget_maria(self, sample_budget_key, sample_fiscal_events):
        """Maria (trajectory 3): moderate-cost person should produce realistic budget."""
        key = PersonBudgetKey(**sample_budget_key)
        events = [FiscalEvent(**e) for e in sample_fiscal_events]
        engine = BudgetEngine()
        budget = engine.compute(key, events, iterations=200)

        assert budget.person_uid == "dome-maria-034"
        assert len(budget.horizons) >= 1

        # Check that 1-year horizon exists and has reasonable values
        h1y = next((h for h in budget.horizons if h.label == "1y"), None)
        assert h1y is not None
        assert h1y.payer_view.federal_expected_spend > 0
        # For someone on Medicaid + SNAP, federal spend should be meaningful
        assert h1y.payer_view.federal_expected_spend > 5000

        # Risk profile should have valid percentiles
        assert h1y.risk_profile.p50_total_cost > 0
        assert h1y.risk_profile.p90_total_cost >= h1y.risk_profile.p50_total_cost
        assert h1y.risk_profile.p99_total_cost >= h1y.risk_profile.p90_total_cost

    def test_compute_budget_high_need(self, sample_budget_key, sample_fiscal_events):
        """High-need person should have higher costs."""
        key_data = {**sample_budget_key}
        key_data["high_need_flag"] = True
        key_data["chronic_condition_flags"] = ["diabetes", "heart_disease", "chronic_pain"]
        key_data["housing_status"] = "shelter"
        key_data["homelessness_history_flag"] = True
        key_data["justice_involvement_flag"] = True
        key_data["past_12m_jail_days"] = 30

        key = PersonBudgetKey(**key_data)
        events = [FiscalEvent(**e) for e in sample_fiscal_events]
        engine = BudgetEngine()
        budget = engine.compute(key, events, iterations=200)

        h1y = next((h for h in budget.horizons if h.label == "1y"), None)
        assert h1y is not None
        # High-need person should have significantly elevated costs
        total = (
            h1y.payer_view.federal_expected_spend
            + h1y.payer_view.state_expected_spend
            + h1y.payer_view.local_expected_spend
        )
        assert total > 50000  # substantially above baseline

    def test_compute_has_domain_view(self, sample_budget_key, sample_fiscal_events):
        key = PersonBudgetKey(**sample_budget_key)
        events = [FiscalEvent(**e) for e in sample_fiscal_events]
        engine = BudgetEngine()
        budget = engine.compute(key, events, iterations=100)

        h1y = next((h for h in budget.horizons if h.label == "1y"), None)
        assert h1y is not None
        # Should have domain breakdown
        assert len(h1y.domain_view) > 0
        domains = {d.domain for d in h1y.domain_view}
        assert "healthcare" in domains

    def test_compute_has_mechanism_view(self, sample_budget_key, sample_fiscal_events):
        key = PersonBudgetKey(**sample_budget_key)
        events = [FiscalEvent(**e) for e in sample_fiscal_events]
        engine = BudgetEngine()
        budget = engine.compute(key, events, iterations=100)

        h1y = next((h for h in budget.horizons if h.label == "1y"), None)
        assert len(h1y.mechanism_view) > 0
