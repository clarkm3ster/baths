"""Alert management — queuing, deduplication, and escalation."""

from __future__ import annotations

import logging
import time
from collections import defaultdict
from typing import Any

from src.safety.models import SafetyViolation

logger = logging.getLogger(__name__)


class Alert:
    """An individual safety alert."""
    def __init__(self, violation: SafetyViolation, sphere_id: str) -> None:
        self.violation = violation
        self.sphere_id = sphere_id
        self.created_at = time.time()
        self.acknowledged = False
        self.escalation_count = 0
        self.key = f"{sphere_id}:{violation.system_type}:{violation.parameter}"


class AlertManager:
    """In-memory alert queue with deduplication and escalation.

    In production, this would dispatch to webhooks, email, SMS, etc.
    """

    DEDUP_WINDOW_SEC = 60  # Don't re-alert same violation within 60s
    ESCALATION_DELAY_SEC = 120  # Escalate unresolved alerts after 120s

    def __init__(self) -> None:
        self._active: dict[str, Alert] = {}
        self._history: list[Alert] = []
        self._last_alert_time: dict[str, float] = defaultdict(float)

    def submit(self, violation: SafetyViolation, sphere_id: str) -> Alert | None:
        """Submit a new violation. Returns Alert if dispatched, None if deduplicated."""
        alert = Alert(violation, sphere_id)

        # Deduplication check
        last_time = self._last_alert_time.get(alert.key, 0)
        if time.time() - last_time < self.DEDUP_WINDOW_SEC:
            return None

        self._active[alert.key] = alert
        self._last_alert_time[alert.key] = time.time()
        self._history.append(alert)

        logger.warning(
            "SAFETY ALERT [%s] %s — %s=%s (threshold=%s) on sphere %s",
            violation.severity.upper(),
            violation.system_type,
            violation.parameter,
            violation.value,
            violation.threshold,
            sphere_id,
        )

        return alert

    def acknowledge(self, key: str) -> bool:
        """Acknowledge an active alert."""
        if key in self._active:
            self._active[key].acknowledged = True
            return True
        return False

    def resolve(self, key: str) -> bool:
        """Mark an alert as resolved."""
        if key in self._active:
            del self._active[key]
            return True
        return False

    def check_escalations(self) -> list[Alert]:
        """Check for alerts that need escalation."""
        escalated = []
        now = time.time()
        for alert in self._active.values():
            if not alert.acknowledged and (now - alert.created_at) > self.ESCALATION_DELAY_SEC:
                alert.escalation_count += 1
                escalated.append(alert)
                logger.error(
                    "ESCALATION #%d: [%s] %s on sphere %s unresolved for %ds",
                    alert.escalation_count,
                    alert.violation.severity,
                    alert.violation.parameter,
                    alert.sphere_id,
                    int(now - alert.created_at),
                )
        return escalated

    @property
    def active_alerts(self) -> list[Alert]:
        return list(self._active.values())

    @property
    def history(self) -> list[Alert]:
        return list(self._history)
