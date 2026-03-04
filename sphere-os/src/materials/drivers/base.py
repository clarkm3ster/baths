"""MaterialDriver abstract base class, enums, and response types.

Every programmable material system in a Sphere is represented by a concrete
subclass of ``MaterialDriver``.  Drivers expose a uniform async interface for
configuration, state readback, validation, and emergency reset.  In simulation
mode (the default until real hardware is connected) each driver models
realistic transition timing scaled by ``simulation_speed``.
"""

from __future__ import annotations

import time
import uuid
from abc import ABC, abstractmethod
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class MaterialSystemType(str, Enum):
    """Canonical identifiers for every material subsystem managed by SPHERE/OS."""

    ACOUSTIC_METAMATERIAL = "acoustic_metamaterial"
    HAPTIC_SURFACE = "haptic_surface"
    OLFACTORY_SYNTHESIS = "olfactory_synthesis"
    ELECTROCHROMIC_SURFACE = "electrochromic_surface"
    PROJECTION_MAPPING = "projection_mapping"
    PHASE_CHANGE_PANEL = "phase_change_panel"
    SHAPE_MEMORY_ELEMENT = "shape_memory_element"
    DEPLOYABLE_4D = "4d_printed_deployable"
    BIOLUMINESCENT_COATING = "bioluminescent_coating"


class DriverStatus(str, Enum):
    """Operational status of a single material driver instance."""

    IDLE = "idle"
    APPLYING = "applying"
    TRANSITIONING = "transitioning"
    ACTIVE = "active"
    ERROR = "error"
    EMERGENCY_RESET = "emergency_reset"


class ValidationSeverity(str, Enum):
    """How serious a validation issue is."""

    INFO = "info"
    WARNING = "warning"
    ERROR = "error"


# ---------------------------------------------------------------------------
# Response / result models
# ---------------------------------------------------------------------------

class ValidationIssue(BaseModel):
    """A single validation finding."""

    field: str
    message: str
    severity: ValidationSeverity = ValidationSeverity.ERROR


class ValidationResult(BaseModel):
    """Outcome of ``MaterialDriver.validate_config``."""

    valid: bool
    issues: list[ValidationIssue] = Field(default_factory=list)

    @classmethod
    def ok(cls) -> ValidationResult:
        return cls(valid=True, issues=[])

    @classmethod
    def fail(cls, issues: list[ValidationIssue]) -> ValidationResult:
        return cls(valid=False, issues=issues)


class DriverResponse(BaseModel):
    """Returned by ``MaterialDriver.apply_config``."""

    success: bool
    system_type: MaterialSystemType
    transition_time_s: float = 0.0
    state_snapshot: dict[str, Any] = Field(default_factory=dict)
    error: str | None = None
    request_id: str = Field(default_factory=lambda: uuid.uuid4().hex[:12])
    timestamp: float = Field(default_factory=time.time)


class DriverInfo(BaseModel):
    """Public metadata about a registered driver."""

    system_type: MaterialSystemType
    trl: int
    status: DriverStatus
    simulation_mode: bool
    simulation_speed: float
    capabilities: dict[str, Any] = Field(default_factory=dict)


# ---------------------------------------------------------------------------
# Abstract base
# ---------------------------------------------------------------------------

class MaterialDriver(ABC):
    """Abstract base class for all material subsystem drivers.

    Parameters
    ----------
    simulation_mode:
        When *True* (default), the driver does not talk to real hardware and
        instead models behaviour with scaled ``asyncio.sleep`` delays.
    simulation_speed:
        Multiplier applied to all simulated durations.  ``1.0`` = real-time,
        ``0.001`` = 1 000x faster (useful for tests).
    """

    # Subclasses MUST set these as class attributes.
    system_type: MaterialSystemType
    trl: int  # Technology Readiness Level (1-9)

    def __init__(
        self,
        *,
        simulation_mode: bool = True,
        simulation_speed: float = 1.0,
    ) -> None:
        self.simulation_mode = simulation_mode
        self.simulation_speed = simulation_speed
        self.status: DriverStatus = DriverStatus.IDLE
        self._current_config: dict[str, Any] = {}
        self._state: dict[str, Any] = {}
        self._last_applied_at: float | None = None
        self._error_message: str | None = None
        self._id: str = uuid.uuid4().hex[:8]

    # -- public helpers ------------------------------------------------------

    def info(self) -> DriverInfo:
        """Return read-only metadata about this driver."""
        return DriverInfo(
            system_type=self.system_type,
            trl=self.trl,
            status=self.status,
            simulation_mode=self.simulation_mode,
            simulation_speed=self.simulation_speed,
            capabilities=self._capabilities(),
        )

    def sim_delay(self, real_seconds: float) -> float:
        """Return the simulated delay for *real_seconds*."""
        return real_seconds * self.simulation_speed

    # -- abstract interface --------------------------------------------------

    @abstractmethod
    async def apply_config(self, config: dict[str, Any]) -> DriverResponse:
        """Apply a new material configuration.

        Implementations MUST:
        1. Call ``validate_config`` first and refuse invalid configs.
        2. Set ``self.status`` through the correct lifecycle states.
        3. Simulate transition timing via ``self.sim_delay``.
        4. Update ``self._state`` to reflect the new steady-state.
        """

    @abstractmethod
    async def read_state(self) -> dict[str, Any]:
        """Return a snapshot of the current driver state."""

    @abstractmethod
    async def validate_config(self, config: dict[str, Any]) -> ValidationResult:
        """Validate a proposed configuration without applying it."""

    @abstractmethod
    async def emergency_reset(self) -> None:
        """Immediately reset to a safe default state.

        Must be fast and must not raise.
        """

    # -- optional overrides --------------------------------------------------

    def _capabilities(self) -> dict[str, Any]:
        """Override to advertise driver-specific capabilities."""
        return {}
