"""Tests for holdout validation framework."""

import pytest

from dome.validation.holdout_validator import HoldoutValidator


class TestHoldoutValidator:
    def test_synthetic_validation(self):
        """Test that synthetic data generation and validation works."""
        validator = HoldoutValidator()
        predictions, actuals = validator.generate_synthetic_validation(n=200)
        assert len(predictions) == 200
        assert len(actuals) == 200

        report = validator.validate(predictions, actuals)
        assert report.n_samples == 200
        assert report.mae >= 0
        assert report.mape >= 0
        assert report.rmse >= 0
        assert len(report.calibration_by_decile) == 10

    def test_calibration_deciles(self):
        validator = HoldoutValidator()
        predictions, actuals = validator.generate_synthetic_validation(n=500)
        report = validator.validate(predictions, actuals)

        for point in report.calibration_by_decile:
            assert 1 <= point.decile <= 10
            assert point.predicted_mean > 0
            assert point.actual_mean > 0
            assert point.n_in_decile > 0
