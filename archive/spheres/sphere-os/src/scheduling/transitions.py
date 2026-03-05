"""Material transition time calculator for SPHERE/OS scheduling.

Computes the total transition time required to reconfigure a Sphere from one
MaterialConfiguration to another, given the material systems installed in the
Sphere's inventory.

Transition times are governed by physical constraints of each material system.
The total transition time is the MAX across all material axes that need to change,
since material transitions execute in parallel.

Material system naming:
    The canonical short names used in material_inventory are:
        acoustic, electrochromic, projection, haptic, olfactory,
        thermal_pcm, shape_memory, deployable_4d

    Legacy long names are also accepted via SYSTEM_ALIASES:
        acoustic_metamaterial, electrochromic_surface, projection_mapping,
        haptic_surface, olfactory_synthesis, phase_change_panel,
        shape_memory_element, 4d_printed_deployable
"""

from __future__ import annotations

import math
from typing import Any


# ---------------------------------------------------------------------------
# Transition time bounds per material system (seconds)
# ---------------------------------------------------------------------------

TRANSITION_MATRIX: dict[str, dict[str, float]] = {
    "acoustic": {"min_sec": 0.025, "max_sec": 60},
    "electrochromic": {"min_sec": 1, "max_sec": 5},
    "projection": {"min_sec": 0.1, "max_sec": 10},
    "haptic": {"min_sec": 0.025, "max_sec": 5},
    "olfactory": {"min_sec": 600, "max_sec": 1200},
    "thermal_pcm": {"min_sec": 300, "max_sec": 1800},
    "shape_memory": {"min_sec": 300, "max_sec": 3600},
    "deployable_4d": {"min_sec": 1800, "max_sec": 3600},
}

# Legacy name aliases (long form -> canonical short form)
SYSTEM_ALIASES: dict[str, str] = {
    "acoustic_metamaterial": "acoustic",
    "electrochromic_surface": "electrochromic",
    "projection_mapping": "projection",
    "haptic_surface": "haptic",
    "olfactory_synthesis": "olfactory",
    "phase_change_panel": "thermal_pcm",
    "shape_memory_element": "shape_memory",
    "4d_printed_deployable": "deployable_4d",
    "bioluminescent_coating": "_bioluminescent",  # persistent, 0 transition
}

# Maps MaterialConfiguration fields to their governing material system
CONFIG_FIELD_TO_SYSTEM: dict[str, str] = {
    "acoustic_reverb_time_seconds": "acoustic",
    "acoustic_absorption_profile": "acoustic",
    "wall_color_rgb": "electrochromic",
    "wall_opacity": "electrochromic",
    "light_color_temp_kelvin": "projection",
    "light_intensity_lux": "projection",
    "floor_haptic_pattern": "haptic",
    "floor_haptic_intensity": "haptic",
    "scent_profile": "olfactory",
    "thermal_target_celsius": "thermal_pcm",
    "shape_memory_elements": "shape_memory",
}


def _canonicalize(system: str) -> str:
    """Resolve a material system name to its canonical short form."""
    return SYSTEM_ALIASES.get(system, system)


# ---------------------------------------------------------------------------
# Per-system transition time calculators
# ---------------------------------------------------------------------------

def _system_transition_time(
    system: str,
    from_c: dict[str, Any],
    to_c: dict[str, Any],
) -> float:
    """Calculate transition time in seconds for a single material system.

    Uses proportional scaling where possible: interpolates between the
    system's min_sec and max_sec based on the magnitude of the change.
    """
    canonical = _canonicalize(system)
    bounds = TRANSITION_MATRIX.get(canonical)
    if bounds is None:
        return 0.0

    min_s = bounds["min_sec"]
    max_s = bounds["max_sec"]

    if canonical == "acoustic":
        from_reverb = from_c.get("acoustic_reverb_time_seconds", 1.0)
        to_reverb = to_c.get("acoustic_reverb_time_seconds", 1.0)
        from_abs = from_c.get("acoustic_absorption_profile", [])
        to_abs = to_c.get("acoustic_absorption_profile", [])
        if from_reverb == to_reverb and from_abs == to_abs:
            return 0.0
        # Proportional: reverb range is 0.5-5.0, absorption bands are 0-1
        reverb_delta = abs(float(from_reverb) - float(to_reverb)) / 4.5
        abs_delta = 0.0
        if from_abs and to_abs:
            abs_delta = sum(abs(float(a) - float(b)) for a, b in zip(from_abs, to_abs)) / max(len(from_abs), 1)
        elif from_abs != to_abs:
            abs_delta = 1.0
        magnitude = min(max(reverb_delta, abs_delta), 1.0)
        return min_s + magnitude * (max_s - min_s) if magnitude > 0 else 0.0

    if canonical == "electrochromic":
        from_opacity = from_c.get("wall_opacity", 1.0)
        to_opacity = to_c.get("wall_opacity", 1.0)
        from_color = from_c.get("wall_color_rgb", [200, 200, 200])
        to_color = to_c.get("wall_color_rgb", [200, 200, 200])
        if from_opacity == to_opacity and from_color == to_color:
            return 0.0
        opacity_delta = abs(float(from_opacity) - float(to_opacity))
        color_delta = 0.0
        if from_color and to_color:
            max_dist = math.sqrt(3 * (255 ** 2))
            dist = math.sqrt(sum((float(a) - float(b)) ** 2 for a, b in zip(from_color, to_color)))
            color_delta = dist / max_dist
        magnitude = min(max(opacity_delta, color_delta), 1.0)
        return min_s + magnitude * (max_s - min_s) if magnitude > 0 else 0.0

    if canonical == "projection":
        from_temp = from_c.get("light_color_temp_kelvin", 4000)
        to_temp = to_c.get("light_color_temp_kelvin", 4000)
        from_lux = from_c.get("light_intensity_lux", 300)
        to_lux = to_c.get("light_intensity_lux", 300)
        if from_temp == to_temp and from_lux == to_lux:
            return 0.0
        temp_delta = abs(int(from_temp) - int(to_temp)) / 3800  # range 2700-6500
        lux_delta = abs(int(from_lux) - int(to_lux)) / 950  # range 50-1000
        magnitude = min(max(temp_delta, lux_delta), 1.0)
        return min_s + magnitude * (max_s - min_s)

    if canonical == "haptic":
        from_pat = from_c.get("floor_haptic_pattern", "off")
        to_pat = to_c.get("floor_haptic_pattern", "off")
        from_int = from_c.get("floor_haptic_intensity", 0.0)
        to_int = to_c.get("floor_haptic_intensity", 0.0)
        if from_pat == to_pat and float(from_int) == float(to_int):
            return 0.0
        # Pattern change is categorical (full magnitude), intensity is proportional
        if from_pat != to_pat:
            magnitude = 1.0
        else:
            magnitude = min(abs(float(from_int) - float(to_int)), 1.0)
        return min_s + magnitude * (max_s - min_s)

    if canonical == "olfactory":
        from_scent = from_c.get("scent_profile", {}) or {}
        to_scent = to_c.get("scent_profile", {}) or {}
        from_primary = from_scent.get("primary")
        to_primary = to_scent.get("primary")
        from_secondary = from_scent.get("secondary")
        to_secondary = to_scent.get("secondary")
        from_intensity = float(from_scent.get("intensity", 0))
        to_intensity = float(to_scent.get("intensity", 0))

        if from_primary == to_primary and from_secondary == to_secondary and from_intensity == to_intensity:
            return 0.0

        # Full scent identity change requires purge+refill (max time)
        if from_primary != to_primary or from_secondary != to_secondary:
            # If going from active scent to different active scent: full 1200s
            if from_primary is not None and to_primary is not None and from_primary != to_primary:
                return max_s
            # If adding scent where there was none, or removing: proportional
            if from_primary is None and to_primary is not None:
                return min_s + to_intensity * (max_s - min_s)
            if from_primary is not None and to_primary is None:
                return min_s + from_intensity * (max_s - min_s)
            # Secondary changed
            return min_s + 0.5 * (max_s - min_s)

        # Only intensity change
        magnitude = abs(from_intensity - to_intensity)
        return min_s + magnitude * (max_s - min_s)

    if canonical == "thermal_pcm":
        from_temp = float(from_c.get("thermal_target_celsius", 22))
        to_temp = float(to_c.get("thermal_target_celsius", 22))
        delta = abs(from_temp - to_temp)
        if delta == 0:
            return 0.0
        magnitude = min(delta / 12.0, 1.0)  # range 16-28 = 12 degrees
        return min_s + magnitude * (max_s - min_s)

    if canonical == "shape_memory":
        from_elems = {
            e.get("element_id"): float(e.get("target_curvature", 0))
            for e in from_c.get("shape_memory_elements", [])
        }
        to_elems = {
            e.get("element_id"): float(e.get("target_curvature", 0))
            for e in to_c.get("shape_memory_elements", [])
        }
        if from_elems == to_elems:
            return 0.0
        # Structural change (add/remove elements) is full magnitude
        if set(from_elems.keys()) != set(to_elems.keys()):
            return max_s
        # Curvature-only changes: proportional
        if not from_elems:
            return 0.0
        total_delta = sum(
            abs(from_elems[eid] - to_elems[eid]) for eid in from_elems
        )
        magnitude = min(total_delta / max(len(from_elems), 1), 1.0)
        return min_s + magnitude * (max_s - min_s)

    if canonical == "deployable_4d":
        # Structural system — deployment is always expensive when config changes
        from_deployed = from_c.get("deployed")
        to_deployed = to_c.get("deployed")
        from_conf = from_c.get("deployable_configuration")
        to_conf = to_c.get("deployable_configuration")
        if from_deployed == to_deployed and from_conf == to_conf:
            return 0.0
        return max_s

    return 0.0


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def calculate_transition_time(
    from_config: dict[str, Any],
    to_config: dict[str, Any],
    material_inventory: list[str],
) -> int:
    """Calculate minimum transition time in seconds between two MaterialConfigurations.

    Returns the MAX of all individual material transition times because
    transitions execute in parallel — the overall time is limited by the
    slowest system.

    Only material systems present in the Sphere's inventory are considered.
    If a system is not installed, its config axis is skipped.

    Args:
        from_config: Current MaterialConfiguration dict.
        to_config: Target MaterialConfiguration dict.
        material_inventory: List of installed material system names.

    Returns:
        Transition time in seconds (rounded up to nearest integer).
    """
    if not from_config and not to_config:
        return 0

    from_config = from_config or {}
    to_config = to_config or {}

    transition_times: list[float] = []

    for system in material_inventory:
        t = _system_transition_time(system, from_config, to_config)
        if t > 0:
            transition_times.append(t)

    return math.ceil(max(transition_times)) if transition_times else 0


def transition_time_minutes(
    from_config: dict[str, Any],
    to_config: dict[str, Any],
    material_inventory: list[str],
) -> int:
    """Convenience wrapper that returns transition time in minutes (rounded up)."""
    seconds = calculate_transition_time(from_config, to_config, material_inventory)
    return math.ceil(seconds / 60) if seconds > 0 else 0


def get_bottleneck_systems(
    from_config: dict[str, Any],
    to_config: dict[str, Any],
    material_inventory: list[str],
) -> list[dict[str, Any]]:
    """Identify which material systems are bottlenecks for a transition.

    Returns a sorted list (descending by transition_seconds) of dicts:
        [{"system": "olfactory", "transition_seconds": 1200, "is_bottleneck": True}, ...]
    """
    from_config = from_config or {}
    to_config = to_config or {}

    results = []
    for system in material_inventory:
        t = _system_transition_time(system, from_config, to_config)
        if t > 0:
            results.append({
                "system": system,
                "canonical": _canonicalize(system),
                "transition_seconds": math.ceil(t),
                "is_bottleneck": False,
            })

    if results:
        results.sort(key=lambda x: x["transition_seconds"], reverse=True)
        results[0]["is_bottleneck"] = True

    return results


def suggest_simplified_config(
    from_config: dict[str, Any],
    to_config: dict[str, Any],
    material_inventory: list[str],
    max_transition_seconds: int,
) -> dict[str, Any]:
    """Return a modified to_config that fits within the max transition time budget.

    Strategy: iteratively revert changes from the slowest material system
    (inheriting values from from_config) until the transition fits within
    the budget.

    Args:
        from_config: Current configuration.
        to_config: Desired configuration.
        material_inventory: Installed material systems.
        max_transition_seconds: Maximum allowable transition time in seconds.

    Returns:
        Modified configuration dict that respects the time budget.
        May equal to_config unchanged if it already fits.
    """
    simplified = dict(to_config)

    for _ in range(len(TRANSITION_MATRIX) + 1):
        current_time = calculate_transition_time(from_config, simplified, material_inventory)
        if current_time <= max_transition_seconds:
            return simplified

        bottlenecks = get_bottleneck_systems(from_config, simplified, material_inventory)
        if not bottlenecks:
            return simplified

        # Revert fields belonging to the slowest system
        slowest_canonical = bottlenecks[0]["canonical"]
        fields_to_revert = [
            field for field, sys in CONFIG_FIELD_TO_SYSTEM.items()
            if sys == slowest_canonical
        ]
        for field in fields_to_revert:
            if field in from_config:
                simplified[field] = from_config[field]
            elif field in simplified:
                del simplified[field]

    return simplified
