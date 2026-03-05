"""Tests for safety threshold configuration."""

import pytest
from src.safety.thresholds import ThresholdRule, ThresholdConfig, Severity, DEFAULT_THRESHOLDS


class TestThresholdRule:
    def test_above_warning_only(self):
        rule = ThresholdRule(
            system_type="test", parameter="val",
            description="test", warning_value=0.5, direction="above",
        )
        assert rule.check(0.3) is None
        assert rule.check(0.6) == Severity.WARNING

    def test_all_severity_levels(self):
        rule = ThresholdRule(
            system_type="test", parameter="val",
            description="test",
            warning_value=0.5, critical_value=0.7, emergency_value=0.9,
            direction="above",
        )
        assert rule.check(0.4) is None
        assert rule.check(0.6) == Severity.WARNING
        assert rule.check(0.75) == Severity.CRITICAL
        assert rule.check(0.95) == Severity.EMERGENCY

    def test_below_direction(self):
        rule = ThresholdRule(
            system_type="thermal", parameter="temp",
            description="too cold",
            warning_value=18.0, critical_value=17.0, emergency_value=16.0,
            direction="below",
        )
        assert rule.check(20.0) is None
        assert rule.check(17.5) == Severity.WARNING
        assert rule.check(16.5) == Severity.CRITICAL
        assert rule.check(15.5) == Severity.EMERGENCY

    def test_boundary_exact(self):
        rule = ThresholdRule(
            system_type="test", parameter="val",
            description="test", warning_value=0.5, direction="above",
        )
        assert rule.check(0.5) == Severity.WARNING  # equal triggers


class TestThresholdConfig:
    def test_default_thresholds_exist(self):
        assert len(DEFAULT_THRESHOLDS) >= 4

    def test_filter_by_system(self):
        config = ThresholdConfig()
        olfactory = config.get_rules_for_system("olfactory_synthesis")
        assert len(olfactory) >= 1
        assert all(r.system_type == "olfactory_synthesis" for r in olfactory)

    def test_custom_rules(self):
        custom = ThresholdConfig(rules=[
            ThresholdRule(
                system_type="custom", parameter="x",
                description="test", warning_value=0.5, direction="above",
            ),
        ])
        assert len(custom.rules) == 1
