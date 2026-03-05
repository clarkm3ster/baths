"""Tests for individual material drivers."""

import pytest
from src.materials.drivers.acoustic import AcousticMetamaterialDriver
from src.materials.drivers.olfactory import OlfactorySynthesisDriver
from src.materials.drivers.electrochromic import ElectrochromicSurfaceDriver
from src.materials.drivers.haptic import HapticSurfaceDriver
from src.materials.drivers.projection import ProjectionMappingDriver
from src.materials.drivers.thermal import PhaseChangePanelDriver
from src.materials.drivers.shape_memory import ShapeMemoryElementDriver
from src.materials.drivers.deployable_4d import Deployable4DDriver
from src.materials.drivers.bioluminescent import BioluminescentCoatingDriver
from src.materials.drivers.base import DriverStatus


@pytest.fixture
def fast_kwargs():
    return {"simulation_speed": 0.001}


class TestAcousticDriver:
    @pytest.mark.asyncio
    async def test_apply_valid_config(self, fast_kwargs):
        d = AcousticMetamaterialDriver(**fast_kwargs)
        resp = await d.apply_config({"reverb_time_s": 2.5, "absorption_bands": [0.5]*7})
        assert resp.success
        state = await d.read_state()
        assert state["reverb_time_s"] == 2.5

    @pytest.mark.asyncio
    async def test_reject_invalid_reverb(self, fast_kwargs):
        d = AcousticMetamaterialDriver(**fast_kwargs)
        resp = await d.apply_config({"reverb_time_s": 10.0})
        assert not resp.success

    @pytest.mark.asyncio
    async def test_reject_wrong_band_count(self, fast_kwargs):
        d = AcousticMetamaterialDriver(**fast_kwargs)
        v = await d.validate_config({"absorption_bands": [0.5]*3})
        assert not v.valid

    @pytest.mark.asyncio
    async def test_emergency_reset(self, fast_kwargs):
        d = AcousticMetamaterialDriver(**fast_kwargs)
        await d.apply_config({"reverb_time_s": 4.0})
        await d.emergency_reset()
        assert d.status == DriverStatus.IDLE
        state = await d.read_state()
        assert state["reverb_time_s"] == 1.5


class TestOlfactoryDriver:
    @pytest.mark.asyncio
    async def test_apply_blend(self, fast_kwargs):
        d = OlfactorySynthesisDriver(**fast_kwargs)
        resp = await d.apply_config({
            "components": {"0": 0.8, "5": 0.3},
            "intensity": 0.5,
            "blend_name": "cedar",
        })
        assert resp.success
        state = await d.read_state()
        assert state["blend_name"] == "cedar"
        assert state["intensity"] == 0.5

    @pytest.mark.asyncio
    async def test_high_intensity_warning_but_valid(self, fast_kwargs):
        d = OlfactorySynthesisDriver(**fast_kwargs)
        v = await d.validate_config({"intensity": 0.85})
        assert v.valid  # >0.8 is a warning, not error
        assert len(v.issues) > 0

    @pytest.mark.asyncio
    async def test_reject_invalid_intensity(self, fast_kwargs):
        d = OlfactorySynthesisDriver(**fast_kwargs)
        v = await d.validate_config({"intensity": 1.5})
        assert not v.valid

    @pytest.mark.asyncio
    async def test_emergency_reset(self, fast_kwargs):
        d = OlfactorySynthesisDriver(**fast_kwargs)
        await d.apply_config({"components": {"0": 0.8}, "intensity": 0.5})
        await d.emergency_reset()
        state = await d.read_state()
        assert state["intensity"] == 0.0
        assert state["blend_name"] is None


class TestElectrochromicDriver:
    @pytest.mark.asyncio
    async def test_apply_opacity(self, fast_kwargs):
        d = ElectrochromicSurfaceDriver(**fast_kwargs)
        resp = await d.apply_config({"wall_opacity": 0.3, "wall_color_rgb": [255, 100, 50]})
        assert resp.success

    @pytest.mark.asyncio
    async def test_reject_bad_opacity(self, fast_kwargs):
        d = ElectrochromicSurfaceDriver(**fast_kwargs)
        v = await d.validate_config({"wall_opacity": 1.5})
        assert not v.valid


class TestHapticDriver:
    @pytest.mark.asyncio
    async def test_apply_pattern(self, fast_kwargs):
        d = HapticSurfaceDriver(**fast_kwargs)
        resp = await d.apply_config({"floor_haptic_pattern": "heartbeat", "floor_haptic_intensity": 0.5})
        assert resp.success

    @pytest.mark.asyncio
    async def test_reject_high_intensity(self, fast_kwargs):
        d = HapticSurfaceDriver(**fast_kwargs)
        v = await d.validate_config({"floor_haptic_intensity": 0.95})
        assert not v.valid


class TestProjectionDriver:
    @pytest.mark.asyncio
    async def test_apply_lighting(self, fast_kwargs):
        d = ProjectionMappingDriver(**fast_kwargs)
        resp = await d.apply_config({"light_color_temp_kelvin": 3200, "light_intensity_lux": 500})
        assert resp.success

    @pytest.mark.asyncio
    async def test_reject_bad_temp(self, fast_kwargs):
        d = ProjectionMappingDriver(**fast_kwargs)
        v = await d.validate_config({"light_color_temp_kelvin": 10000})
        assert not v.valid


class TestThermalDriver:
    @pytest.mark.asyncio
    async def test_apply_temperature(self, fast_kwargs):
        d = PhaseChangePanelDriver(**fast_kwargs)
        resp = await d.apply_config({"thermal_target_celsius": 25.0})
        assert resp.success
        state = await d.read_state()
        assert state["current_celsius"] == 25.0

    @pytest.mark.asyncio
    async def test_reject_out_of_range(self, fast_kwargs):
        d = PhaseChangePanelDriver(**fast_kwargs)
        v = await d.validate_config({"thermal_target_celsius": 35.0})
        assert not v.valid


class TestShapeMemoryDriver:
    @pytest.mark.asyncio
    async def test_apply_elements(self, fast_kwargs):
        d = ShapeMemoryElementDriver(**fast_kwargs)
        resp = await d.apply_config({"shape_memory_elements": [{"element_id": "panel_1", "target_curvature": 0.7}]})
        assert resp.success


class TestDeployable4DDriver:
    @pytest.mark.asyncio
    async def test_deploy(self, fast_kwargs):
        d = Deployable4DDriver(**fast_kwargs)
        resp = await d.apply_config({"deployed": True, "configuration": "arch"})
        assert resp.success


class TestBioluminescentDriver:
    @pytest.mark.asyncio
    async def test_read_only(self, fast_kwargs):
        d = BioluminescentCoatingDriver(**fast_kwargs)
        resp = await d.apply_config({})
        assert resp.success
        state = await d.read_state()
        assert "health" in state
