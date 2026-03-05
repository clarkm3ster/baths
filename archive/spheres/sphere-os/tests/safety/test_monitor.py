"""Tests for the safety monitor integration."""

import uuid
import pytest
from src.materials.orchestrator import MaterialOrchestrator
from src.materials.drivers.base import MaterialSystemType
from src.safety.monitor import SafetyMonitor


@pytest.fixture
def orchestrator():
    return MaterialOrchestrator(
        sphere_id=uuid.uuid4(),
        material_inventory=["olfactory_synthesis", "phase_change_panel", "haptic_surface"],
        simulation_speed=0.001,
    )


@pytest.fixture
def monitor():
    return SafetyMonitor()


class TestSafetyMonitorIntegration:
    @pytest.mark.asyncio
    async def test_clean_state_all_clear(self, orchestrator, monitor):
        report = await monitor.check_all_systems("test-sphere", orchestrator)
        assert report.all_clear
        assert len(report.violations) == 0

    @pytest.mark.asyncio
    async def test_olfactory_warning(self, orchestrator, monitor):
        driver = orchestrator.drivers[MaterialSystemType.OLFACTORY_SYNTHESIS]
        driver._state["intensity"] = 0.78
        report = await monitor.check_all_systems("test-sphere", orchestrator)
        assert not report.all_clear
        assert any(v.severity == "warning" for v in report.violations)

    @pytest.mark.asyncio
    async def test_thermal_emergency_triggers_reset(self, orchestrator, monitor):
        driver = orchestrator.drivers[MaterialSystemType.PHASE_CHANGE_PANEL]
        driver._state["current_celsius"] = 30.0  # Way above 28°C emergency
        await monitor.check_all_systems("test-sphere", orchestrator)
        # After emergency, driver should be reset
        state = await driver.read_state()
        assert state["current_celsius"] == 22.0  # Reset to default

    @pytest.mark.asyncio
    async def test_multiple_violations(self, orchestrator, monitor):
        orchestrator.drivers[MaterialSystemType.OLFACTORY_SYNTHESIS]._state["intensity"] = 0.9
        orchestrator.drivers[MaterialSystemType.PHASE_CHANGE_PANEL]._state["current_celsius"] = 29.0
        report = await monitor.check_all_systems("test-sphere", orchestrator)
        assert len(report.violations) >= 2

    @pytest.mark.asyncio
    async def test_alert_deduplication(self, orchestrator, monitor):
        driver = orchestrator.drivers[MaterialSystemType.OLFACTORY_SYNTHESIS]
        driver._state["intensity"] = 0.9
        # Check twice — second should not create new alert (dedup)
        await monitor.check_all_systems("test-sphere", orchestrator)
        await monitor.check_all_systems("test-sphere", orchestrator)
        assert len(monitor.alerts.active_alerts) == 1
