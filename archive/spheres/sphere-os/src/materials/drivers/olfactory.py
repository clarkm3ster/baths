"""Olfactory synthesis driver.

Simulates a subtractive digital olfaction system with a 40-component blender.
TRL 6 -- the blender micro-doses from sealed cartridges and an HVAC coupling
clears the space between scent cues.

Key parameters:
- components: dict mapping component index (0-39) to intensity (0.0 - 1.0)
- blend_name: optional human-readable preset name
- intensity: overall intensity multiplier (0.0 - 1.0)
- clearing: True to activate HVAC clearing cycle
- clearing_duration_s: how long to run clearing (600 - 1200 s real-time)
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

_NUM_COMPONENTS = 40


class OlfactorySynthesisDriver(MaterialDriver):
    """Driver for the 40-component digital olfaction blender.

    TRL 6: Engineering prototypes demonstrated.
    Full scent change requires HVAC clearing: 600-1200 s.
    Intensity adjustment within current blend: ~3 s.
    This system is the scheduling bottleneck for rapid scene transitions.
    """

    system_type = MaterialSystemType.OLFACTORY_SYNTHESIS
    trl = 6

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._state: dict[str, Any] = {
            "components": {str(i): 0.0 for i in range(_NUM_COMPONENTS)},
            "intensity": 0.0,
            "blend_name": None,
            "clearing": False,
            "clearing_remaining_s": 0.0,
            "voc_level": 0.0,  # volatile organic compound proxy 0-1
        }

    def _capabilities(self) -> dict[str, Any]:
        return {
            "num_components": _NUM_COMPONENTS,
            "clearing_range_s": [600, 1200],
            "max_intensity": 1.0,
        }

    async def validate_config(self, config: dict[str, Any]) -> ValidationResult:
        issues: list[ValidationIssue] = []

        components = config.get("components")
        if components is not None:
            if not isinstance(components, dict):
                issues.append(
                    ValidationIssue(
                        field="components",
                        message="Must be a dict mapping index (0-39) to intensity",
                    )
                )
            else:
                for k, v in components.items():
                    idx = int(k)
                    if not 0 <= idx < _NUM_COMPONENTS:
                        issues.append(
                            ValidationIssue(
                                field=f"components.{k}",
                                message=f"Index must be 0-{_NUM_COMPONENTS - 1}",
                            )
                        )
                    if not 0.0 <= float(v) <= 1.0:
                        issues.append(
                            ValidationIssue(
                                field=f"components.{k}",
                                message="Intensity must be in [0, 1]",
                            )
                        )

        intensity = config.get("intensity")
        if intensity is not None and not 0.0 <= intensity <= 1.0:
            issues.append(
                ValidationIssue(field="intensity", message="Must be in [0, 1]")
            )

        # Safety warning for high intensity
        if intensity is not None and intensity > 0.8:
            issues.append(
                ValidationIssue(
                    field="intensity",
                    message="Intensity > 0.8 may exceed VOC comfort limits",
                    severity=ValidationSeverity.WARNING,
                )
            )

        clearing_dur = config.get("clearing_duration_s")
        if clearing_dur is not None and not 600 <= clearing_dur <= 1200:
            issues.append(
                ValidationIssue(
                    field="clearing_duration_s",
                    message="Must be between 600 and 1200 s",
                )
            )

        # Only fail on actual errors, not warnings
        has_errors = any(i.severity == ValidationSeverity.ERROR for i in issues)
        if has_errors:
            return ValidationResult.fail(issues)
        return ValidationResult(valid=True, issues=issues)

    async def apply_config(self, config: dict[str, Any]) -> DriverResponse:
        validation = await self.validate_config(config)
        if not validation.valid:
            return DriverResponse(
                success=False,
                system_type=self.system_type,
                error="; ".join(i.message for i in validation.issues),
            )

        self.status = DriverStatus.APPLYING

        # Handle clearing mode
        if config.get("clearing", False):
            clearing_s = config.get("clearing_duration_s", 900.0)
            self.status = DriverStatus.TRANSITIONING
            self._state["clearing"] = True
            self._state["clearing_remaining_s"] = clearing_s
            await asyncio.sleep(self.sim_delay(clearing_s))
            # After clearing, reset to zero
            self._state["components"] = {str(i): 0.0 for i in range(_NUM_COMPONENTS)}
            self._state["intensity"] = 0.0
            self._state["blend_name"] = None
            self._state["clearing"] = False
            self._state["clearing_remaining_s"] = 0.0
            self._state["voc_level"] = 0.0
            self.status = DriverStatus.IDLE
            self._last_applied_at = time.time()
            return DriverResponse(
                success=True,
                system_type=self.system_type,
                transition_time_s=clearing_s,
                state_snapshot=dict(self._state),
            )

        # Blending -- fast micro-dosing (< 5 s real-time)
        self.status = DriverStatus.TRANSITIONING
        blend_time_s = 3.0
        await asyncio.sleep(self.sim_delay(blend_time_s))

        if "components" in config:
            for k, v in config["components"].items():
                self._state["components"][str(k)] = float(v)
        if "intensity" in config:
            self._state["intensity"] = config["intensity"]
        if "blend_name" in config:
            self._state["blend_name"] = config["blend_name"]

        # VOC level is a function of active component intensities and overall intensity
        active_vals = [v for v in self._state["components"].values() if v > 0]
        avg_component = sum(active_vals) / max(len(active_vals), 1)
        self._state["voc_level"] = round(
            avg_component * self._state["intensity"], 3
        )
        self._state["clearing"] = False
        self._state["clearing_remaining_s"] = 0.0

        self._current_config = config
        self._last_applied_at = time.time()
        self.status = DriverStatus.ACTIVE

        return DriverResponse(
            success=True,
            system_type=self.system_type,
            transition_time_s=blend_time_s,
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
            "components": {str(i): 0.0 for i in range(_NUM_COMPONENTS)},
            "intensity": 0.0,
            "blend_name": None,
            "clearing": False,
            "clearing_remaining_s": 0.0,
            "voc_level": 0.0,
        }
        await asyncio.sleep(self.sim_delay(0.5))  # fast HVAC purge
        self.status = DriverStatus.IDLE
