"""Bioluminescent coating driver — read-only health monitoring.

This is a persistent living layer that cannot be reconfigured per-booking.
The driver only monitors health and reports status.
"""

from __future__ import annotations

import random
from typing import Any

from src.materials.drivers.base import (
    DriverResponse, DriverStatus, MaterialDriver, MaterialSystemType,
    ValidationResult,
)


class BioluminescentCoatingDriver(MaterialDriver):
    system_type = MaterialSystemType.BIOLUMINESCENT_COATING
    trl = 4

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._state = {
            "health": 0.95,
            "luminosity": 0.7,
            "culture_age_days": 30,
        }

    async def apply_config(self, config: dict[str, Any]) -> DriverResponse:
        # Read-only — cannot apply new config
        return DriverResponse(
            success=True,
            system_type=self.system_type,
            transition_time_s=0,
            state_snapshot=await self.read_state(),
        )

    async def read_state(self) -> dict[str, Any]:
        # Simulate slight variation in health readings
        self._state["health"] = max(0, min(1, self._state["health"] + random.uniform(-0.01, 0.01)))
        return dict(self._state)

    async def validate_config(self, config: dict[str, Any]) -> ValidationResult:
        return ValidationResult.ok()

    async def emergency_reset(self) -> None:
        # Nothing to reset — living system
        self.status = DriverStatus.IDLE

    def _capabilities(self) -> dict[str, Any]:
        return {"read_only": True, "reconfigurable": False}
