"""Safety threshold definitions for each material system.

Defines limits that trigger warnings, critical alerts, or emergency resets.
"""

from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class Severity(str, Enum):
    WARNING = "warning"
    CRITICAL = "critical"
    EMERGENCY = "emergency"


class ThresholdRule(BaseModel):
    """A single threshold check for a material parameter."""
    system_type: str
    parameter: str
    description: str
    warning_value: float | None = None
    critical_value: float | None = None
    emergency_value: float | None = None
    direction: str = "above"  # "above" or "below"

    def check(self, value: float) -> Severity | None:
        """Check a value against this threshold. Returns severity or None."""
        if self.direction == "above":
            if self.emergency_value is not None and value >= self.emergency_value:
                return Severity.EMERGENCY
            if self.critical_value is not None and value >= self.critical_value:
                return Severity.CRITICAL
            if self.warning_value is not None and value >= self.warning_value:
                return Severity.WARNING
        elif self.direction == "below":
            if self.emergency_value is not None and value <= self.emergency_value:
                return Severity.EMERGENCY
            if self.critical_value is not None and value <= self.critical_value:
                return Severity.CRITICAL
            if self.warning_value is not None and value <= self.warning_value:
                return Severity.WARNING
        return None


# Default threshold configuration
DEFAULT_THRESHOLDS: list[ThresholdRule] = [
    # Olfactory
    ThresholdRule(
        system_type="olfactory_synthesis",
        parameter="intensity",
        description="Scent intensity VOC safety limit",
        warning_value=0.75,
        critical_value=0.85,
        emergency_value=0.95,
        direction="above",
    ),
    # Thermal — too hot
    ThresholdRule(
        system_type="phase_change_panel",
        parameter="current_celsius",
        description="Temperature upper bound",
        warning_value=26.0,
        critical_value=27.5,
        emergency_value=28.0,
        direction="above",
    ),
    # Thermal — too cold
    ThresholdRule(
        system_type="phase_change_panel",
        parameter="current_celsius",
        description="Temperature lower bound",
        warning_value=17.0,
        critical_value=16.5,
        emergency_value=16.0,
        direction="below",
    ),
    # Haptic intensity
    ThresholdRule(
        system_type="haptic_surface",
        parameter="floor_haptic_intensity",
        description="Haptic intensity safety limit",
        warning_value=0.8,
        critical_value=0.9,
        emergency_value=0.95,
        direction="above",
    ),
    # Acoustic SPL equivalent
    ThresholdRule(
        system_type="acoustic_metamaterial",
        parameter="reverb_time_s",
        description="Excessive reverb (high SPL equivalent)",
        warning_value=4.0,
        critical_value=4.5,
        emergency_value=5.0,
        direction="above",
    ),
]


class ThresholdConfig(BaseModel):
    """Full threshold configuration."""
    rules: list[ThresholdRule] = Field(default_factory=lambda: list(DEFAULT_THRESHOLDS))

    def get_rules_for_system(self, system_type: str) -> list[ThresholdRule]:
        return [r for r in self.rules if r.system_type == system_type]
