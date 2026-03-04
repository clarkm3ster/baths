"""Projection mapping driver — LED + projectors (baseline visual layer)."""

from __future__ import annotations

import asyncio
from typing import Any

from src.materials.drivers.base import (
    DriverResponse, DriverStatus, MaterialDriver, MaterialSystemType,
    ValidationIssue, ValidationResult,
)


class ProjectionMappingDriver(MaterialDriver):
    system_type = MaterialSystemType.PROJECTION_MAPPING
    trl = 9

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._state = {"light_color_temp_kelvin": 4000, "light_intensity_lux": 300}

    async def apply_config(self, config: dict[str, Any]) -> DriverResponse:
        v = await self.validate_config(config)
        if not v.valid:
            return DriverResponse(success=False, system_type=self.system_type, error="; ".join(i.message for i in v.issues))
        self.status = DriverStatus.TRANSITIONING
        await asyncio.sleep(self.sim_delay(0.5))
        self._state["light_color_temp_kelvin"] = config.get("light_color_temp_kelvin", self._state["light_color_temp_kelvin"])
        self._state["light_intensity_lux"] = config.get("light_intensity_lux", self._state["light_intensity_lux"])
        self.status = DriverStatus.ACTIVE
        return DriverResponse(success=True, system_type=self.system_type, transition_time_s=0.5, state_snapshot=dict(self._state))

    async def read_state(self) -> dict[str, Any]:
        return dict(self._state)

    async def validate_config(self, config: dict[str, Any]) -> ValidationResult:
        issues = []
        temp = config.get("light_color_temp_kelvin")
        if temp is not None and not (2700 <= temp <= 6500):
            issues.append(ValidationIssue(field="light_color_temp_kelvin", message="Must be 2700-6500K"))
        lux = config.get("light_intensity_lux")
        if lux is not None and not (0 <= lux <= 1000):
            issues.append(ValidationIssue(field="light_intensity_lux", message="Must be 0-1000 lux"))
        return ValidationResult.ok() if not issues else ValidationResult.fail(issues)

    async def emergency_reset(self) -> None:
        self._state = {"light_color_temp_kelvin": 4000, "light_intensity_lux": 300}
        self.status = DriverStatus.IDLE
