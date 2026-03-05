"""Tests for the safety monitoring system."""

import uuid
import pytest
from src.materials.orchestrator import MaterialOrchestrator
from src.safety.monitor import SafetyMonitor
from src.safety.thresholds import ThresholdConfig, ThresholdRule, Severity
from src.safety.alerts import AlertManager
from src.safety.models import SafetyViolation


@pytest.fixture
def orchestrator():
    return MaterialOrchestrator(
        sphere_id=uuid.uuid4(),
        material_inventory=[
            "olfactory_synthesis",
            "phase_change_panel",
            "haptic_surface",
        ],
        simulation_speed=0.001,
    )


@pytest.fixture
def monitor():
    return SafetyMonitor()


class TestThresholdRule:
    def test_above_warning(self):
        rule = ThresholdRule(
            system_type="test", parameter="val",
            description="test", warning_value=0.7, critical_value=0.85, emergency_value=0.95,
            direction="above",
        )
        assert rule.check(0.5) is None
        assert rule.check(0.75) == Severity.WARNING
        assert rule.check(0.9) == Severity.CRITICAL
        assert rule.check(0.96) == Severity.EMERGENCY

    def test_below_warning(self):
        rule = ThresholdRule(
            system_type="test", parameter="temp",
            description="test", warning_value=17.0, critical_value=16.5, emergency_value=16.0,
            direction="below",
        )
        assert rule.check(20.0) is None
        assert rule.check(16.8) == Severity.WARNING
        assert rule.check(16.2) == Severity.CRITICAL
        assert rule.check(15.5) == Severity.EMERGENCY


class TestAlertManager:
    def test_submit_and_dedup(self):
        mgr = AlertManager()
        v = SafetyViolation(
            system_type="olfactory", parameter="intensity",
            value=0.9, threshold=0.85, severity="critical",
        )
        a1 = mgr.submit(v, "sphere-1")
        assert a1 is not None
        # Immediate resubmit should be deduped
        a2 = mgr.submit(v, "sphere-1")
        assert a2 is None

    def test_active_alerts(self):
        mgr = AlertManager()
        v = SafetyViolation(
            system_type="thermal", parameter="temp",
            value=29, threshold=28, severity="emergency",
        )
        mgr.submit(v, "sphere-1")
        assert len(mgr.active_alerts) == 1

    def test_resolve(self):
        mgr = AlertManager()
        v = SafetyViolation(
            system_type="thermal", parameter="temp",
            value=29, threshold=28, severity="emergency",
        )
        alert = mgr.submit(v, "sphere-1")
        mgr.resolve(alert.key)
        assert len(mgr.active_alerts) == 0


class TestSafetyMonitor:
    @pytest.mark.asyncio
    async def test_all_clear_report(self, orchestrator, monitor):
        report = await monitor.check_all_systems(str(uuid.uuid4()), orchestrator)
        assert report.all_clear

    @pytest.mark.asyncio
    async def test_detects_high_olfactory(self, orchestrator, monitor):
        # Manually set olfactory to high intensity
        from src.materials.drivers.base import MaterialSystemType
        driver = orchestrator.drivers.get(MaterialSystemType.OLFACTORY_SYNTHESIS)
        if driver:
            driver._state["intensity"] = 0.9
            report = await monitor.check_all_systems("test-sphere", orchestrator)
            assert not report.all_clear
            assert any(v.system_type == "olfactory_synthesis" for v in report.violations)

    @pytest.mark.asyncio
    async def test_detects_thermal_violation(self, orchestrator, monitor):
        from src.materials.drivers.base import MaterialSystemType
        driver = orchestrator.drivers.get(MaterialSystemType.PHASE_CHANGE_PANEL)
        if driver:
            driver._state["current_celsius"] = 30.0
            report = await monitor.check_all_systems("test-sphere", orchestrator)
            assert not report.all_clear
            assert any(v.parameter == "current_celsius" for v in report.violations)
