"""Electrochromic surface driver — switchable glass opacity/color."""

from __future__ import annotations

import asyncio
from typing import Any

from src.materials.drivers.base import (
    DriverResponse, DriverStatus, MaterialDriver, MaterialSystemType,
    ValidationIssue, ValidationResult,
)


class ElectrochromicSurfaceDriver(MaterialDriver):
    system_type = MaterialSystemType.ELECTROCHROMIC_SURFACE
    trl = 8

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._state = {"wall_color_rgb": [200, 200, 200], "wall_opacity": 1.0}

    async def apply_config(self, config: dict[str, Any]) -> DriverResponse:
        v = await self.validate_config(config)
        if not v.valid:
            return DriverResponse(success=False, system_type=self.system_type, error="; ".join(i.message for i in v.issues))
        self.status = DriverStatus.TRANSITIONING
        await asyncio.sleep(self.sim_delay(3.0))
        self._state["wall_color_rgb"] = config.get("wall_color_rgb", self._state["wall_color_rgb"])
        self._state["wall_opacity"] = config.get("wall_opacity", self._state["wall_opacity"])
        self.status = DriverStatus.ACTIVE
        return DriverResponse(success=True, system_type=self.system_type, transition_time_s=3.0, state_snapshot=dict(self._state))

    async def read_state(self) -> dict[str, Any]:
        return dict(self._state)

    async def validate_config(self, config: dict[str, Any]) -> ValidationResult:
        issues = []
        o = config.get("wall_opacity")
        if o is not None and not (0 <= o <= 1):
            issues.append(ValidationIssue(field="wall_opacity", message="Must be 0-1"))
        rgb = config.get("wall_color_rgb")
        if rgb is not None and (len(rgb) != 3 or any(not (0 <= c <= 255) for c in rgb)):
            issues.append(ValidationIssue(field="wall_color_rgb", message="Must be [r,g,b] 0-255"))
        return ValidationResult.ok() if not issues else ValidationResult.fail(issues)

    async def emergency_reset(self) -> None:
        self._state = {"wall_color_rgb": [200, 200, 200], "wall_opacity": 1.0}
        self.status = DriverStatus.IDLE
