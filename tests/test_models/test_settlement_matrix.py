"""Tests for settlement matrix models."""

from datetime import datetime

import pytest

from dome.models.settlement_matrix import (
    PayerSettlementRow,
    PayerTransfer,
    SettlementMatrix,
)


class TestSettlementMatrix:
    def test_create_matrix(self):
        matrix = SettlementMatrix(
            person_uid="dome-james-042",
            scenario_id="housing_first_intervention",
            horizon_label="lifetime",
            payers=[
                PayerSettlementRow(
                    payer_id="CMS-Medicaid",
                    payer_level="federal",
                    payer_name="CMS Medicaid",
                    upfront_investment=0.0,
                    expected_gross_savings=180000.0,
                    net_position_after_settlement=90000.0,
                ),
                PayerSettlementRow(
                    payer_id="HUD",
                    payer_level="federal",
                    payer_name="HUD Housing Choice Vouchers",
                    upfront_investment=22000.0,
                    expected_gross_savings=0.0,
                    net_position_after_settlement=-11000.0,
                ),
                PayerSettlementRow(
                    payer_id="City-Chicago-HHS",
                    payer_level="local",
                    payer_name="City of Chicago Human Services",
                    upfront_investment=5000.0,
                    expected_gross_savings=30000.0,
                    net_position_after_settlement=17500.0,
                ),
            ],
            transfers=[
                PayerTransfer(
                    from_payer_id="CMS-Medicaid",
                    to_payer_id="HUD",
                    amount=11000.0,
                    transfer_schedule="annual true-up",
                ),
                PayerTransfer(
                    from_payer_id="City-Chicago-HHS",
                    to_payer_id="HUD",
                    amount=2500.0,
                    transfer_schedule="quarterly",
                ),
            ],
            assumptions={
                "discount_rate": 0.03,
                "risk_share_pct": 0.50,
                "cap_multiple": 3.0,
            },
            generated_at=datetime(2026, 1, 15, 12, 0),
            model_version="0.1.0",
        )
        assert len(matrix.payers) == 3
        assert len(matrix.transfers) == 2
        assert matrix.transfers[0].amount == 11000.0
        total_investment = sum(p.upfront_investment for p in matrix.payers)
        assert total_investment == 27000.0

    def test_horizon_labels(self):
        for label in ["1y", "5y", "20y", "lifetime"]:
            matrix = SettlementMatrix(
                person_uid="test",
                scenario_id="test",
                horizon_label=label,
                payers=[],
                transfers=[],
                generated_at=datetime.now(),
                model_version="0.1.0",
            )
            assert matrix.horizon_label == label
