"""Tests for bias audit framework."""

import pytest

from dome.validation.bias_audit import BiasAuditor


class TestBiasAuditor:
    def test_synthetic_audit(self):
        """Test that synthetic audit data and auditing works."""
        auditor = BiasAuditor()
        predictions, metadata = auditor.generate_synthetic_audit_data(n=300)
        assert len(predictions) == 300
        assert len(metadata) == 300

        report = auditor.audit(predictions, metadata)
        assert report.overall_assessment in ("pass", "concern", "fail")
        assert len(report.checks) > 0

    def test_all_checks_have_scores(self):
        auditor = BiasAuditor()
        predictions, metadata = auditor.generate_synthetic_audit_data(n=200)
        report = auditor.audit(predictions, metadata)

        for check in report.checks:
            assert check.check_name
            assert isinstance(check.passed, bool)
            assert check.score >= 0  # score is a metric, not necessarily bounded to [0, 1]
            assert check.details
