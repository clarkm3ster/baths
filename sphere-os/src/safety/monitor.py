"""Safety monitor — continuous real-time monitoring of material systems."""

from __future__ import annotations

import asyncio
import logging
import uuid
from datetime import datetime, timezone
from typing import Any

from src.materials.orchestrator import MaterialOrchestrator
from src.safety.alerts import AlertManager
from src.safety.models import SafetyReport, SafetyViolation
from src.safety.thresholds import ThresholdConfig

logger = logging.getLogger(__name__)


class SafetyMonitor:
    """Continuous safety monitoring for active Sphere bookings."""

    def __init__(
        self,
        threshold_config: ThresholdConfig | None = None,
        alert_manager: AlertManager | None = None,
    ) -> None:
        self.thresholds = threshold_config or ThresholdConfig()
        self.alerts = alert_manager or AlertManager()
        self._monitoring_tasks: dict[str, asyncio.Task] = {}

    async def start_monitoring(
        self,
        sphere_id: uuid.UUID,
        orchestrator: MaterialOrchestrator,
        check_interval: float = 1.0,
    ) -> None:
        """Start a monitoring loop for a sphere."""
        sid = str(sphere_id)
        if sid in self._monitoring_tasks:
            logger.info("Already monitoring sphere %s", sid)
            return

        task = asyncio.create_task(
            self._monitor_loop(sid, orchestrator, check_interval)
        )
        self._monitoring_tasks[sid] = task
        logger.info("Started safety monitoring for sphere %s", sid)

    async def stop_monitoring(self, sphere_id: uuid.UUID) -> None:
        """Stop monitoring a sphere."""
        sid = str(sphere_id)
        task = self._monitoring_tasks.pop(sid, None)
        if task:
            task.cancel()
            logger.info("Stopped safety monitoring for sphere %s", sid)

    async def check_all_systems(
        self,
        sphere_id: str,
        orchestrator: MaterialOrchestrator,
    ) -> SafetyReport:
        """Run a single safety check cycle across all material systems."""
        violations: list[SafetyViolation] = []
        states = await orchestrator.read_all_states()

        for system_type_str, state in states.items():
            rules = self.thresholds.get_rules_for_system(system_type_str)
            for rule in rules:
                value = state.get(rule.parameter)
                if value is None:
                    continue

                severity = rule.check(float(value))
                if severity is not None:
                    violation = SafetyViolation(
                        system_type=system_type_str,
                        parameter=rule.parameter,
                        value=float(value),
                        threshold=_get_threshold_value(rule, severity),
                        severity=severity.value,
                        description=rule.description,
                    )
                    violations.append(violation)

        report = SafetyReport(
            sphere_id=sphere_id,
            timestamp=datetime.now(timezone.utc).isoformat(),
            all_clear=len(violations) == 0,
            violations=violations,
            system_states=states,
        )

        # Handle violations
        for v in violations:
            await self._handle_violation(sphere_id, v, orchestrator)

        return report

    async def _handle_violation(
        self,
        sphere_id: str,
        violation: SafetyViolation,
        orchestrator: MaterialOrchestrator,
    ) -> None:
        """Handle a safety threshold violation by severity."""
        self.alerts.submit(violation, sphere_id)

        if violation.severity == "emergency":
            logger.error("EMERGENCY: %s on sphere %s — triggering reset", violation.parameter, sphere_id)
            await orchestrator.emergency_reset_all()

        elif violation.severity == "critical":
            logger.warning("CRITICAL: %s on sphere %s", violation.parameter, sphere_id)

    async def _monitor_loop(
        self,
        sphere_id: str,
        orchestrator: MaterialOrchestrator,
        interval: float,
    ) -> None:
        """Continuous monitoring loop."""
        try:
            while True:
                await self.check_all_systems(sphere_id, orchestrator)
                self.alerts.check_escalations()
                await asyncio.sleep(interval)
        except asyncio.CancelledError:
            pass
        except Exception as e:
            logger.error("Monitoring error for sphere %s: %s", sphere_id, e)


def _get_threshold_value(rule, severity) -> float:
    """Get the threshold value for a given severity level."""
    from src.safety.thresholds import Severity
    if severity == Severity.EMERGENCY:
        return rule.emergency_value or 0
    if severity == Severity.CRITICAL:
        return rule.critical_value or 0
    return rule.warning_value or 0
