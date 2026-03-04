"""MaterialOrchestrator — coordinates all material drivers for a Sphere.

Manages configuration application in the correct order, with validation
and rollback on partial failure.
"""

from __future__ import annotations

import logging
import uuid
from typing import Any

from src.materials.drivers.base import (
    DriverResponse,
    DriverStatus,
    MaterialDriver,
    MaterialSystemType,
)

logger = logging.getLogger(__name__)


class MaterialOrchestrationError(Exception):
    """Raised when a material orchestration operation fails."""
    pass


class MaterialOrchestrator:
    """Coordinates all material drivers for a single Sphere."""

    def __init__(
        self,
        sphere_id: uuid.UUID,
        material_inventory: list[str],
        simulation_speed: float = 0.001,
    ) -> None:
        self.sphere_id = sphere_id
        self.drivers: dict[MaterialSystemType, MaterialDriver] = {}

        from src.materials.drivers import DRIVER_REGISTRY

        for system_str in material_inventory:
            try:
                system_type = MaterialSystemType(system_str)
            except ValueError:
                logger.warning("Unknown material system: %s", system_str)
                continue

            driver_cls = DRIVER_REGISTRY.get(system_type)
            if driver_cls:
                self.drivers[system_type] = driver_cls(simulation_speed=simulation_speed)

    async def apply_configuration(
        self,
        target: dict[str, Any],
        transition_plan: list[str] | None = None,
    ) -> dict[str, DriverResponse]:
        """Execute a full material state transition.

        Applies changes in the order specified by transition_plan.
        Implements rollback on partial failure.

        Args:
            target: Full MaterialConfiguration dict.
            transition_plan: Ordered list of system type strings to transition.
                If None, all installed systems are transitioned.

        Returns:
            Dict mapping system type to DriverResponse.
        """
        if transition_plan is None:
            transition_plan = [st.value for st in self.drivers]

        responses: dict[str, DriverResponse] = {}
        applied_types: list[MaterialSystemType] = []

        for system_str in transition_plan:
            try:
                system_type = MaterialSystemType(system_str)
            except ValueError:
                continue

            driver = self.drivers.get(system_type)
            if not driver:
                continue

            # Extract relevant config subset
            driver_config = self._extract_driver_config(target, system_type)
            if not driver_config:
                continue

            # Validate
            validation = await driver.validate_config(driver_config)
            if not validation.valid:
                await self._rollback(applied_types)
                errors = "; ".join(i.message for i in validation.issues)
                raise MaterialOrchestrationError(
                    f"Validation failed for {system_type.value}: {errors}"
                )

            # Apply
            try:
                response = await driver.apply_config(driver_config)
                responses[system_type.value] = response
                if response.success:
                    applied_types.append(system_type)
                else:
                    await self._rollback(applied_types)
                    raise MaterialOrchestrationError(
                        f"Driver {system_type.value} failed: {response.error}"
                    )
            except MaterialOrchestrationError:
                raise
            except Exception as e:
                await self._rollback(applied_types)
                raise MaterialOrchestrationError(
                    f"Driver {system_type.value} raised: {e}"
                )

        return responses

    async def read_all_states(self) -> dict[str, Any]:
        """Read current state from all drivers."""
        state = {}
        for system_type, driver in self.drivers.items():
            state[system_type.value] = await driver.read_state()
        return state

    async def emergency_reset_all(self) -> None:
        """Emergency reset all drivers to safe defaults."""
        for system_type, driver in self.drivers.items():
            try:
                await driver.emergency_reset()
            except Exception as e:
                logger.error("Emergency reset failed for %s: %s", system_type.value, e)

    async def _rollback(self, applied_types: list[MaterialSystemType]) -> None:
        """Rollback all systems that were already transitioned."""
        logger.warning("Rolling back %d systems", len(applied_types))
        for system_type in reversed(applied_types):
            driver = self.drivers.get(system_type)
            if driver:
                try:
                    await driver.emergency_reset()
                except Exception as e:
                    logger.error("Rollback failed for %s: %s", system_type.value, e)

    def _extract_driver_config(
        self,
        full_config: dict[str, Any],
        system_type: MaterialSystemType,
    ) -> dict[str, Any]:
        """Extract the config subset relevant to a specific driver."""
        mapping: dict[MaterialSystemType, list[str]] = {
            MaterialSystemType.ACOUSTIC_METAMATERIAL: [
                "acoustic_reverb_time_seconds", "acoustic_absorption_profile",
                "reverb_time_s", "absorption_bands", "diffusion", "beam_steering_deg",
            ],
            MaterialSystemType.ELECTROCHROMIC_SURFACE: [
                "wall_color_rgb", "wall_opacity",
            ],
            MaterialSystemType.PROJECTION_MAPPING: [
                "light_color_temp_kelvin", "light_intensity_lux",
            ],
            MaterialSystemType.HAPTIC_SURFACE: [
                "floor_haptic_pattern", "floor_haptic_intensity",
            ],
            MaterialSystemType.OLFACTORY_SYNTHESIS: [
                "components", "intensity", "blend_name", "clearing", "clearing_duration_s",
            ],
            MaterialSystemType.PHASE_CHANGE_PANEL: [
                "thermal_target_celsius",
            ],
            MaterialSystemType.SHAPE_MEMORY_ELEMENT: [
                "shape_memory_elements",
            ],
            MaterialSystemType.DEPLOYABLE_4D: [
                "deployed", "configuration",
            ],
            MaterialSystemType.BIOLUMINESCENT_COATING: [],
        }

        keys = mapping.get(system_type, [])
        return {k: full_config[k] for k in keys if k in full_config}

    def get_driver_info(self) -> list[dict[str, Any]]:
        """Return metadata about all registered drivers."""
        return [driver.info().model_dump() for driver in self.drivers.values()]
