"""Phase-change panel driver — thermal regulation panels."""

from __future__ import annotations

import asyncio
from typing import Any

from src.materials.drivers.base import (
    DriverResponse, DriverStatus, MaterialDriver, MaterialSystemType,
    ValidationIssue, ValidationResult,
)


class PhaseChangePanelDriver(MaterialDriver):
    system_type = MaterialSystemType.PHASE_CHANGE_PANEL
    trl = 7

    TEMP_MIN = 16.0
    TEMP_MAX = 28.0

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._state = {"thermal_target_celsius": 22.0, "current_celsius": 22.0}

    async def apply_config(self, config: dict[str, Any]) -> DriverResponse:
        v = await self.validate_config(config)
        if not v.valid:
            return DriverResponse(success=False, system_type=self.system_type, error="; ".join(i.message for i in v.issues))

        target = config.get("thermal_target_celsius", self._state["thermal_target_celsius"])
        delta = abs(target - self._state["current_celsius"])
        transition_sec = 300 + delta * 60 if delta > 0 else 0

        self.status = DriverStatus.TRANSITIONING
        await asyncio.sleep(self.sim_delay(min(transition_sec, 1800)))
        self._state["thermal_target_celsius"] = target
        self._state["current_celsius"] = target
        self.status = DriverStatus.ACTIVE

        return DriverResponse(success=True, system_type=self.system_type, transition_time_s=transition_sec, state_snapshot=dict(self._state))

    async def read_state(self) -> dict[str, Any]:
        return dict(self._state)

    async def validate_config(self, config: dict[str, Any]) -> ValidationResult:
        issues = []
        t = config.get("thermal_target_celsius")
        if t is not None and not (self.TEMP_MIN <= t <= self.TEMP_MAX):
            issues.append(ValidationIssue(field="thermal_target_celsius", message=f"Must be {self.TEMP_MIN}-{self.TEMP_MAX}°C"))
        return ValidationResult.ok() if not issues else ValidationResult.fail(issues)

    async def emergency_reset(self) -> None:
        self._state = {"thermal_target_celsius": 22.0, "current_celsius": 22.0}
        self.status = DriverStatus.IDLE
