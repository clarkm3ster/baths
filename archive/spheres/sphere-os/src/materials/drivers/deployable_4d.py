"""4D printed deployable driver — MIT Self-Assembly Lab model."""

from __future__ import annotations

import asyncio
from typing import Any

from src.materials.drivers.base import (
    DriverResponse, DriverStatus, MaterialDriver, MaterialSystemType,
    ValidationIssue, ValidationResult,
)


class Deployable4DDriver(MaterialDriver):
    system_type = MaterialSystemType.DEPLOYABLE_4D
    trl = 5

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._state = {"deployed": False, "configuration": "flat"}

    async def apply_config(self, config: dict[str, Any]) -> DriverResponse:
        v = await self.validate_config(config)
        if not v.valid:
            return DriverResponse(success=False, system_type=self.system_type, error="; ".join(i.message for i in v.issues))

        self.status = DriverStatus.TRANSITIONING
        await asyncio.sleep(self.sim_delay(3600))  # 60 min
        self._state["deployed"] = config.get("deployed", self._state["deployed"])
        self._state["configuration"] = config.get("configuration", self._state["configuration"])
        self.status = DriverStatus.ACTIVE

        return DriverResponse(success=True, system_type=self.system_type, transition_time_s=3600, state_snapshot=dict(self._state))

    async def read_state(self) -> dict[str, Any]:
        return dict(self._state)

    async def validate_config(self, config: dict[str, Any]) -> ValidationResult:
        return ValidationResult.ok()

    async def emergency_reset(self) -> None:
        self._state = {"deployed": False, "configuration": "flat"}
        self.status = DriverStatus.IDLE
