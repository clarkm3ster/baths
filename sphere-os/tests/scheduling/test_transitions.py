"""Tests for material transition time calculator."""

import pytest
from src.scheduling.transitions import calculate_transition_time, get_bottleneck_systems

ALL_SYSTEMS = [
    "acoustic_metamaterial", "electrochromic_surface", "projection_mapping",
    "haptic_surface", "olfactory_synthesis", "phase_change_panel",
    "shape_memory_element", "4d_printed_deployable",
]


class TestCalculateTransitionTime:
    def test_identical_configs_zero_time(self):
        config = {"wall_opacity": 0.5, "scent_profile": {"primary": "cedar", "intensity": 0.3}}
        assert calculate_transition_time(config, config, ALL_SYSTEMS) == 0

    def test_olfactory_is_bottleneck(self):
        from_c = {"scent_profile": {"primary": "cedar", "intensity": 0.5}}
        to_c = {"scent_profile": {"primary": "lavender", "intensity": 0.5}}
        t = calculate_transition_time(from_c, to_c, ["olfactory_synthesis", "electrochromic_surface"])
        assert t == 1200  # 20 min full scent clearing

    def test_olfactory_intensity_only(self):
        """Intensity-only change: 600 + magnitude * 600."""
        from_c = {"scent_profile": {"primary": "cedar", "intensity": 0.3}}
        to_c = {"scent_profile": {"primary": "cedar", "intensity": 0.8}}
        t = calculate_transition_time(from_c, to_c, ["olfactory_synthesis"])
        # magnitude = |0.3 - 0.8| = 0.5 → 600 + 0.5*600 = 900
        assert t == 900

    def test_electrochromic_proportional(self):
        """Opacity delta 0.7 → 1 + 0.7*4 = 3.8 → ceil = 4."""
        from_c = {"wall_opacity": 0.2}
        to_c = {"wall_opacity": 0.9}
        t = calculate_transition_time(from_c, to_c, ["electrochromic_surface"])
        assert t == 4

    def test_thermal_proportional_to_delta(self):
        """8°C delta / 12°C range = 0.667 → 300 + 0.667*1500 = 1300."""
        from_c = {"thermal_target_celsius": 18}
        to_c = {"thermal_target_celsius": 26}
        t = calculate_transition_time(from_c, to_c, ["phase_change_panel"])
        assert t == 1300

    def test_shape_memory_curvature(self):
        """Curvature delta 0.6 → 300 + 0.6*3300 = 2280."""
        from_c = {"shape_memory_elements": [{"element_id": "a", "target_curvature": 0.2}]}
        to_c = {"shape_memory_elements": [{"element_id": "a", "target_curvature": 0.8}]}
        t = calculate_transition_time(from_c, to_c, ["shape_memory_element"])
        assert t == 2280

    def test_4d_deployable_state_change(self):
        """Deploying a 4D structure is always max time (3600s)."""
        from_c = {"deployed": False}
        to_c = {"deployed": True}
        t = calculate_transition_time(from_c, to_c, ["4d_printed_deployable"])
        assert t == 3600

    def test_4d_deployable_no_change(self):
        """No deployable config change → 0."""
        assert calculate_transition_time({}, {}, ["4d_printed_deployable"]) == 0

    def test_max_of_all_systems(self):
        from_c = {
            "wall_opacity": 0.2,
            "scent_profile": {"primary": "cedar", "intensity": 0.5},
        }
        to_c = {
            "wall_opacity": 0.9,
            "scent_profile": {"primary": "lavender", "intensity": 0.5},
        }
        t = calculate_transition_time(from_c, to_c, ["electrochromic_surface", "olfactory_synthesis"])
        assert t == 1200  # Olfactory dominates

    def test_empty_inventory(self):
        assert calculate_transition_time({"wall_opacity": 0.1}, {"wall_opacity": 0.9}, []) == 0

    def test_olfactory_from_null_to_active(self):
        """Activating scent from nothing: min + intensity * range."""
        from_c = {"scent_profile": {"primary": None, "intensity": 0}}
        to_c = {"scent_profile": {"primary": "cedar", "intensity": 0.5}}
        t = calculate_transition_time(from_c, to_c, ["olfactory_synthesis"])
        # 600 + 0.5 * 600 = 900
        assert t == 900


class TestGetBottleneckSystems:
    def test_identifies_bottleneck(self):
        from_c = {"wall_opacity": 0.2, "scent_profile": {"primary": "a", "intensity": 0.3}}
        to_c = {"wall_opacity": 0.9, "scent_profile": {"primary": "b", "intensity": 0.3}}
        bottlenecks = get_bottleneck_systems(
            from_c, to_c, ["electrochromic_surface", "olfactory_synthesis"]
        )
        assert len(bottlenecks) == 2
        assert bottlenecks[0]["system"] == "olfactory_synthesis"
        assert bottlenecks[0]["is_bottleneck"] is True
