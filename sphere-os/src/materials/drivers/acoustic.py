"""Acoustic metamaterial driver.

Simulates a programmable acoustic metamaterial panel array that can reshape
sound fields in real time.  Based on TRL 7 reconfigurable acoustic
metamaterials with sub-60 ms switching times and 7-band absorption control.

Key parameters:
- reverb_time_s: target reverberation time (0.5 - 5.0 s)
- absorption_bands: 7-element array of absorption coefficients (0-1) for
  frequency bands centred at 125, 250, 500, 1k, 2k, 4k, 8k Hz
- diffusion: 0-1 overall diffusion coefficient
- beam_steering_deg: acoustic beam steering angle (-60 to +60 degrees)
"""

from __future__ import annotations

import asyncio
import time
from typing import Any

from src.materials.drivers.base import (
    DriverResponse,
    DriverStatus,
    MaterialDriver,
    MaterialSystemType,
    ValidationIssue,
    ValidationResult,
    ValidationSeverity,
)

_BAND_CENTRES_HZ = [125, 250, 500, 1000, 2000, 4000, 8000]
_DEFAULT_ABSORPTION = [0.3, 0.3, 0.4, 0.5, 0.5, 0.4, 0.3]  # neutral room


class AcousticMetamaterialDriver(MaterialDriver):
    """Driver for reconfigurable acoustic metamaterial panels."""

    system_type = MaterialSystemType.ACOUSTIC_METAMATERIAL
    trl = 7

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        # Initialise to a neutral acoustic profile
        self._state = {
            "reverb_time_s": 1.5,
            "absorption_bands": list(_DEFAULT_ABSORPTION),
            "diffusion": 0.5,
            "beam_steering_deg": 0.0,
            "switching_time_ms": 0.0,
        }

    # ------------------------------------------------------------------

    def _capabilities(self) -> dict[str, Any]:
        return {
            "reverb_range_s": [0.5, 5.0],
            "bands": _BAND_CENTRES_HZ,
            "max_switching_ms": 60,
            "beam_steering_range_deg": [-60, 60],
        }

    async def validate_config(self, config: dict[str, Any]) -> ValidationResult:
        issues: list[ValidationIssue] = []

        reverb = config.get("reverb_time_s")
        if reverb is not None:
            if not 0.5 <= reverb <= 5.0:
                issues.append(
                    ValidationIssue(
                        field="reverb_time_s",
                        message=f"Must be between 0.5 and 5.0 s, got {reverb}",
                    )
                )

        bands = config.get("absorption_bands")
        if bands is not None:
            if not isinstance(bands, list) or len(bands) != 7:
                issues.append(
                    ValidationIssue(
                        field="absorption_bands",
                        message="Must be a list of exactly 7 floats",
                    )
                )
            elif not all(0.0 <= b <= 1.0 for b in bands):
                issues.append(
                    ValidationIssue(
                        field="absorption_bands",
                        message="Each coefficient must be in [0, 1]",
                    )
                )

        diffusion = config.get("diffusion")
        if diffusion is not None and not 0.0 <= diffusion <= 1.0:
            issues.append(
                ValidationIssue(field="diffusion", message="Must be in [0, 1]")
            )

        steer = config.get("beam_steering_deg")
        if steer is not None and not -60 <= steer <= 60:
            issues.append(
                ValidationIssue(
                    field="beam_steering_deg",
                    message="Must be in [-60, 60] degrees",
                )
            )

        if issues:
            return ValidationResult.fail(issues)
        return ValidationResult.ok()

    async def apply_config(self, config: dict[str, Any]) -> DriverResponse:
        validation = await self.validate_config(config)
        if not validation.valid:
            return DriverResponse(
                success=False,
                system_type=self.system_type,
                error="; ".join(i.message for i in validation.issues),
            )

        self.status = DriverStatus.APPLYING

        # Compute switching time (real hardware: 20-60 ms depending on delta)
        old_bands = self._state["absorption_bands"]
        new_bands = config.get("absorption_bands", old_bands)
        max_delta = max(abs(a - b) for a, b in zip(old_bands, new_bands))
        switching_ms = 20.0 + max_delta * 40.0  # linear interpolation

        self.status = DriverStatus.TRANSITIONING
        await asyncio.sleep(self.sim_delay(switching_ms / 1000.0))

        # Apply new state
        if "reverb_time_s" in config:
            self._state["reverb_time_s"] = config["reverb_time_s"]
        if "absorption_bands" in config:
            self._state["absorption_bands"] = list(config["absorption_bands"])
        if "diffusion" in config:
            self._state["diffusion"] = config["diffusion"]
        if "beam_steering_deg" in config:
            self._state["beam_steering_deg"] = config["beam_steering_deg"]
        self._state["switching_time_ms"] = round(switching_ms, 1)

        self._current_config = config
        self._last_applied_at = time.time()
        self.status = DriverStatus.ACTIVE

        return DriverResponse(
            success=True,
            system_type=self.system_type,
            transition_time_s=switching_ms / 1000.0,
            state_snapshot=dict(self._state),
        )

    async def read_state(self) -> dict[str, Any]:
        return {
            "system_type": self.system_type.value,
            "status": self.status.value,
            "trl": self.trl,
            **self._state,
        }

    async def emergency_reset(self) -> None:
        self.status = DriverStatus.EMERGENCY_RESET
        self._state = {
            "reverb_time_s": 1.5,
            "absorption_bands": list(_DEFAULT_ABSORPTION),
            "diffusion": 0.5,
            "beam_steering_deg": 0.0,
            "switching_time_ms": 0.0,
        }
        await asyncio.sleep(self.sim_delay(0.02))  # 20 ms hard reset
        self.status = DriverStatus.IDLE
