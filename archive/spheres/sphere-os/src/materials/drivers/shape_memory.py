"""Shape memory element driver — SMP textiles and panels."""

from __future__ import annotations

import asyncio
from typing import Any

from src.materials.drivers.base import (
    DriverResponse, DriverStatus, MaterialDriver, MaterialSystemType,
    ValidationIssue, ValidationResult,
)


class ShapeMemoryElementDriver(MaterialDriver):
    system_type = MaterialSystemType.SHAPE_MEMORY_ELEMENT
    trl = 6

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._state = {"elements": []}

    async def apply_config(self, config: dict[str, Any]) -> DriverResponse:
        v = await self.validate_config(config)
        if not v.valid:
            return DriverResponse(success=False, system_type=self.system_type, error="; ".join(i.message for i in v.issues))

        elements = config.get("shape_memory_elements", [])
        self.status = DriverStatus.TRANSITIONING
        await asyncio.sleep(self.sim_delay(1800))  # 30 min activation
        self._state["elements"] = elements
        self.status = DriverStatus.ACTIVE

        return DriverResponse(success=True, system_type=self.system_type, transition_time_s=1800, state_snapshot=dict(self._state))

    async def read_state(self) -> dict[str, Any]:
        return dict(self._state)

    async def validate_config(self, config: dict[str, Any]) -> ValidationResult:
        issues = []
        elements = config.get("shape_memory_elements", [])
        for e in elements:
            c = e.get("target_curvature", 0)
            if not (0 <= c <= 1):
                issues.append(ValidationIssue(field="shape_memory_elements", message=f"Curvature must be 0-1 for {e.get('element_id')}"))
        return ValidationResult.ok() if not issues else ValidationResult.fail(issues)

    async def emergency_reset(self) -> None:
        self._state = {"elements": []}
        self.status = DriverStatus.IDLE
