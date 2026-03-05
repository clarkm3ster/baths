"""Haptic surface driver — LRA-based floor/wall arrays."""

from __future__ import annotations

import asyncio
from typing import Any

from src.materials.drivers.base import (
    DriverResponse, DriverStatus, MaterialDriver, MaterialSystemType,
    ValidationIssue, ValidationResult,
)

VALID_PATTERNS = {"off", "gentle_rain", "heartbeat", "earthquake", "ocean_waves", "breathing", "pulse"}


class HapticSurfaceDriver(MaterialDriver):
    system_type = MaterialSystemType.HAPTIC_SURFACE
    trl = 7

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._state = {"floor_haptic_pattern": "off", "floor_haptic_intensity": 0.0}

    async def apply_config(self, config: dict[str, Any]) -> DriverResponse:
        v = await self.validate_config(config)
        if not v.valid:
            return DriverResponse(success=False, system_type=self.system_type, error="; ".join(i.message for i in v.issues))
        self.status = DriverStatus.TRANSITIONING
        await asyncio.sleep(self.sim_delay(0.025))
        self._state["floor_haptic_pattern"] = config.get("floor_haptic_pattern", self._state["floor_haptic_pattern"])
        self._state["floor_haptic_intensity"] = config.get("floor_haptic_intensity", self._state["floor_haptic_intensity"])
        self.status = DriverStatus.ACTIVE
        return DriverResponse(success=True, system_type=self.system_type, transition_time_s=0.025, state_snapshot=dict(self._state))

    async def read_state(self) -> dict[str, Any]:
        return dict(self._state)

    async def validate_config(self, config: dict[str, Any]) -> ValidationResult:
        issues = []
        intensity = config.get("floor_haptic_intensity")
        if intensity is not None and not (0 <= intensity <= 1):
            issues.append(ValidationIssue(field="floor_haptic_intensity", message="Must be 0-1"))
        if intensity is not None and intensity > 0.9:
            issues.append(ValidationIssue(field="floor_haptic_intensity", message="Exceeds safe limit 0.9"))
        return ValidationResult.ok() if not issues else ValidationResult.fail(issues)

    async def emergency_reset(self) -> None:
        self._state = {"floor_haptic_pattern": "off", "floor_haptic_intensity": 0.0}
        self.status = DriverStatus.IDLE
