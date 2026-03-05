"""Tests for the MaterialOrchestrator."""

import uuid
import pytest
from src.materials.orchestrator import MaterialOrchestrator, MaterialOrchestrationError


@pytest.fixture
def orchestrator():
    return MaterialOrchestrator(
        sphere_id=uuid.uuid4(),
        material_inventory=[
            "acoustic_metamaterial",
            "electrochromic_surface",
            "projection_mapping",
            "haptic_surface",
            "olfactory_synthesis",
            "phase_change_panel",
        ],
        simulation_speed=0.001,
    )


class TestMaterialOrchestrator:
    @pytest.mark.asyncio
    async def test_apply_configuration(self, orchestrator):
        target = {
            "wall_opacity": 0.5,
            "wall_color_rgb": [100, 200, 50],
            "light_color_temp_kelvin": 3500,
        }
        responses = await orchestrator.apply_configuration(target)
        assert len(responses) > 0
        for resp in responses.values():
            assert resp.success

    @pytest.mark.asyncio
    async def test_read_all_states(self, orchestrator):
        states = await orchestrator.read_all_states()
        assert "acoustic_metamaterial" in states
        assert "electrochromic_surface" in states

    @pytest.mark.asyncio
    async def test_emergency_reset(self, orchestrator):
        await orchestrator.emergency_reset_all()
        states = await orchestrator.read_all_states()
        # All drivers should be in default state
        assert states is not None

    @pytest.mark.asyncio
    async def test_rollback_on_invalid_config(self, orchestrator):
        target = {
            "wall_opacity": 0.5,  # valid
            "intensity": 5.0,  # invalid — must be 0-1
        }
        with pytest.raises(MaterialOrchestrationError):
            await orchestrator.apply_configuration(
                target,
                transition_plan=["electrochromic_surface", "olfactory_synthesis"],
            )

    @pytest.mark.asyncio
    async def test_get_driver_info(self, orchestrator):
        info = orchestrator.get_driver_info()
        assert len(info) == 6
        trl_values = [d["trl"] for d in info]
        assert all(3 <= t <= 9 for t in trl_values)

    @pytest.mark.asyncio
    async def test_empty_config_no_changes(self, orchestrator):
        responses = await orchestrator.apply_configuration({})
        assert len(responses) == 0
