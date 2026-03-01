"""Tests for fiscal event model."""

from datetime import date

import pytest

from dome.models.fiscal_event import FiscalEvent


class TestFiscalEvent:
    def test_create_event(self):
        evt = FiscalEvent(
            person_uid="test-001",
            event_date=date(2025, 3, 10),
            payer_level="federal",
            payer_entity="CMS-Medicaid",
            program_or_fund="Medicaid",
            domain="healthcare",
            mechanism="service_utilization",
            service_category="er_visit",
            utilization_unit="visit",
            quantity=1.0,
            amount_paid=2200.0,
            amount_type="actual_claim",
            confidence=0.95,
            data_source_system="state_medicaid",
            attribution_tags=["anxiety"],
        )
        assert evt.amount_paid == 2200.0
        assert evt.event_id  # auto-generated UUID
        assert evt.domain == "healthcare"

    def test_confidence_bounds(self):
        with pytest.raises(Exception):
            FiscalEvent(
                person_uid="test-001",
                event_date=date(2025, 1, 1),
                payer_level="federal",
                payer_entity="test",
                program_or_fund="test",
                domain="healthcare",
                mechanism="cash_transfer",
                service_category="test",
                utilization_unit="test",
                amount_paid=100.0,
                amount_type="actual_claim",
                confidence=1.5,  # invalid
                data_source_system="test",
                attribution_tags=[],
            )

    def test_all_domains(self):
        domains = [
            "healthcare", "income_support", "housing", "food",
            "education", "justice", "child_family", "transport", "other",
        ]
        for d in domains:
            evt = FiscalEvent(
                person_uid="test",
                event_date=date(2025, 1, 1),
                payer_level="federal",
                payer_entity="test",
                program_or_fund="test",
                domain=d,
                mechanism="cash_transfer",
                service_category="test",
                utilization_unit="test",
                amount_paid=100.0,
                amount_type="actual_claim",
                confidence=1.0,
                data_source_system="test",
            )
            assert evt.domain == d
