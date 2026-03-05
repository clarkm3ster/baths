"""System prompt templates for SPHERE/OS production proposal generation.

These prompts encode the Material Dramaturgy framework: the philosophical
and practical basis for treating programmable materials as narrative characters
whose state changes ARE the story.

Every prompt is built by composing reusable blocks (palette, constraints,
dramaturgy framework) into a final system-prompt string that is sent to the
Anthropic API.
"""

from __future__ import annotations

from src.productions.models import (
    DEFAULT_MATERIAL_PALETTE,
    MATERIAL_TRANSITION_TIMES,
    MaterialPalette,
)

# ---------------------------------------------------------------------------
# Output JSON schema description (passed to Claude so it knows the shape)
# ---------------------------------------------------------------------------

PROPOSAL_OUTPUT_SCHEMA = """\
{
  "title": "string — evocative, specific production title",
  "logline": "string — 1-2 sentence hook",
  "genre": "sci-fi | drama | thriller | experimental",
  "format": "feature_film | series | short | installation | hybrid",
  "narrative_concept": "string — 2-3 paragraphs describing the story and how materials tell it",
  "material_script": [
    {
      "beat_id": "string — e.g. act1_setup, act1_inciting_incident, act2_rising_action, act2_midpoint, act2_crisis, act3_climax, act3_denouement",
      "timestamp_range": [start_seconds, end_seconds] OR "persistent",
      "material_system": "one of the available systems listed above",
      "target_property": "string — the specific physical parameter being controlled",
      "value_curve": [float, ...],
      "narrative_function": "builds_tension | reveals_character | marks_time_passage | establishes_mood | signals_resolution | creates_contrast"
    }
  ],
  "min_area_sqft": float,
  "required_utilities": ["power", "water", ...],
  "crew_size_estimate": int,
  "estimated_budget_low_usd": int,
  "estimated_budget_high_usd": int,
  "production_timeline_weeks": int,
  "legacy_modes": ["living_soundstage", "public_installation", "community_space", "research_lab"]
}"""


# ---------------------------------------------------------------------------
# Material palette formatter
# ---------------------------------------------------------------------------

def format_material_palette(
    tier_filter: list[int] | None = None,
    palette: MaterialPalette | None = None,
) -> str:
    """Render the available material systems as a human-readable block.

    Parameters
    ----------
    tier_filter:
        Which TRL tiers to include.  ``[1]`` = only Tier 1 (deployable now).
        ``[1, 2]`` = Tier 1 + 2.  ``None`` = all tiers.
    palette:
        Override the default palette for custom Spheres.
    """
    pal = palette or DEFAULT_MATERIAL_PALETTE
    tiers = tier_filter or [1, 2, 3]

    sections: list[str] = []

    if 1 in tiers:
        systems = pal["tier_1_deployable_now"]
        lines = _format_tier_systems(systems)
        sections.append(f"TIER 1 — DEPLOYABLE NOW (TRL 7-9):\n{lines}")

    if 2 in tiers:
        systems = pal["tier_2_near_term"]
        lines = _format_tier_systems(systems)
        sections.append(f"TIER 2 — NEAR-TERM (TRL 5-7, 2-4 year horizon):\n{lines}")

    if 3 in tiers:
        systems = pal["tier_3_long_term"]
        lines = _format_tier_systems(systems)
        sections.append(f"TIER 3 — LONG-TERM (TRL 3-5, 5-10 year horizon):\n{lines}")

    return "\n\n".join(sections)


def _format_tier_systems(systems: list[str]) -> str:
    """Format a list of material system names with their transition times."""
    lines: list[str] = []
    for s in systems:
        times = MATERIAL_TRANSITION_TIMES.get(s)
        if times:
            min_t = _human_time(times["min_sec"])
            max_t = _human_time(times["max_sec"])
            lines.append(f"  - {s}  (transition: {min_t} -- {max_t})")
        else:
            lines.append(f"  - {s}")
    return "\n".join(lines)


def _human_time(seconds: float) -> str:
    """Convert seconds to a human-friendly string."""
    if seconds == 0:
        return "instant"
    if seconds < 1:
        return f"{seconds * 1000:.0f}ms"
    if seconds < 60:
        return f"{seconds:.0f}s"
    minutes = seconds / 60
    if minutes < 60:
        return f"{minutes:.0f}min"
    return f"{seconds / 3600:.1f}hr"


# ---------------------------------------------------------------------------
# Transition constraint summary (for system prompt)
# ---------------------------------------------------------------------------

def format_transition_constraints() -> str:
    """Render the physical constraints block for the system prompt."""
    lines = [
        "PHYSICAL TRANSITION-TIME CONSTRAINTS:",
        "(You MUST respect these when spacing material cues in the timeline.)",
        "",
    ]
    for system, times in MATERIAL_TRANSITION_TIMES.items():
        min_t = _human_time(times["min_sec"])
        max_t = _human_time(times["max_sec"])
        note = ""
        if system == "olfactory_synthesis":
            note = "  ** BOTTLENECK -- no olfactory changes closer than 10 min apart **"
        elif system == "bioluminescent_coating":
            note = "  (persistent living layer -- not reconfigurable per-booking)"
        lines.append(f"  {system}: {min_t} -- {max_t}{note}")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main system prompt builder
# ---------------------------------------------------------------------------

def build_system_prompt(
    area_sqft: float | None,
    census_block_group: str | None,
    zoning: str | None,
    street_frontage_ft: float | None,
    tier_filter: list[int] | None = None,
    format_constraint: str | None = None,
) -> str:
    """Build the full system prompt for production proposal generation.

    Parameters
    ----------
    area_sqft:
        Parcel area in square feet.
    zoning:
        Philadelphia zoning code (e.g. ``CMX-3``, ``SP-ENT``).
    street_frontage_ft:
        Street frontage in feet, if known.
    census_block_group:
        Census block group ID for neighborhood context.
    tier_filter:
        Which TRL tiers to include in the palette.
    format_constraint:
        If provided, the model must generate this format.
    """
    palette_block = format_material_palette(tier_filter)
    constraints_block = format_transition_constraints()

    format_instruction = (
        f"You MUST generate a '{format_constraint}' format production."
        if format_constraint
        else "Choose the format (feature_film, series, short, installation, or hybrid) that best fits this site."
    )

    return f"""\
You are a **material dramaturg** -- a new kind of creative professional who designs
film, television, and immersive productions where programmable materials ARE the
narrative medium. You do not use materials as decoration or set dressing. In your
work, a wall that shifts from opaque to transparent over 90 minutes IS the story
of revelation. A floor whose haptic pulse quickens IS rising tension. A scent that
arrives only at the climax IS the emotional payoff.

You work for SPHERE/OS, a platform that transforms vacant public land in Philadelphia
into programmable material environments ("Spheres") for storytelling.

SITE CONTEXT
---------------------------------------------
- City: Philadelphia, Pennsylvania
- Lot size: {area_sqft or 'unknown':,} sqft
- Zoning: {zoning or 'unknown'}
- Street frontage: {street_frontage_ft or 'unknown'} ft
- Census block group: {census_block_group or 'unknown'}

Philadelphia cultural context you should weave into the concept:
- A city of neighborhoods, each with distinct identity (Kensington grit, Rittenhouse
  elegance, North Philly resilience, West Philly creativity, South Philly warmth).
- Deep history of public art (Mural Arts, Magic Gardens), Black cultural innovation,
  immigrant communities, industrial heritage.
- Tension between gentrification and preservation, vacancy and vitality.
- The lot itself is vacant -- your production gives it purpose and then leaves
  lasting infrastructure for the community.

MATERIAL PALETTE
---------------------------------------------
{palette_block}

MATERIAL DRAMATURGY FRAMEWORK
---------------------------------------------
Materials have the same narrative structure as characters:

1. ACT STRUCTURE
   - Setup (Act 1): Establish the baseline material state -- the "normal world."
     The audience learns what each material feels like at rest.
   - Confrontation (Act 2): Disrupt expectations. Materials shift, clash, surprise.
     The space itself becomes unstable, reflecting narrative conflict.
   - Resolution (Act 3): A new equilibrium. Materials settle into a transformed
     state that is DIFFERENT from the setup -- the space has changed irreversibly,
     just as the characters have.

2. CHARACTER ARCS
   Each material system is a character with its own journey:
   - A wall that starts opaque and slowly becomes transparent IS a character arc
     about revelation and vulnerability.
   - A floor whose texture shifts from rough concrete to smooth glass IS a journey
     from hardship to clarity.
   - The olfactory system IS memory -- scent arrives and the audience is transported.

3. RHYTHM & PACING
   - Haptic pulses create heartbeat pacing -- accelerate for tension, decelerate
     for contemplation.
   - Acoustic reverb changes mark scene transitions -- intimate (dry) vs. epic (wet).
   - Electrochromic opacity creates visual breath -- the space inhales (transparent)
     and exhales (opaque).

4. CONTRAST CREATES MEANING
   - warm -> cold = loss, isolation
   - rough -> smooth = resolution, healing
   - silent -> cacophonous = revelation, confrontation
   - dark -> light = hope, but also exposure
   - fragrant -> scentless = forgetting, moving on

{constraints_block}

FORMAT
---------------------------------------------
{format_instruction}

YOUR TASK
---------------------------------------------
Generate a complete production proposal. The story MUST be told THROUGH material
transformations. Every MaterialCue must explain WHAT the material does and WHY
in narrative terms (its narrative_function).

Requirements:
- The material_script MUST contain at least one MaterialCue in each act
  (act1_*, act2_*, act3_*).
- timestamp_ranges must not overlap for the same material_system.
- Olfactory cues must be spaced at least 600 seconds (10 minutes) apart.
- value_curve keyframes should be normalized 0.0-1.0.
- The proposal must be grounded in the physical site constraints.
- legacy_modes must describe how the Sphere persists after production wraps.
- Include at least 3 different material systems.
- Budget should be realistic for a Philadelphia production ($50K-$5M range).

Output ONLY valid JSON matching this exact schema (no markdown, no commentary):

{PROPOSAL_OUTPUT_SCHEMA}
"""


# ---------------------------------------------------------------------------
# Iteration prompt builder
# ---------------------------------------------------------------------------

def build_iteration_system_prompt(
    *,
    original_proposal_json: str,
    feedback: str,
    area_sqft: float | None,
    zoning: str | None,
    street_frontage_ft: float | None,
    census_block_group: str | None,
    tier_filter: list[int] | None = None,
) -> str:
    """Build the system prompt for iterating on an existing proposal.

    Includes the original proposal as context plus the user's feedback.
    """
    base_prompt = build_system_prompt(
        area_sqft=area_sqft,
        zoning=zoning,
        street_frontage_ft=street_frontage_ft,
        census_block_group=census_block_group,
        tier_filter=tier_filter,
    )

    return f"""\
{base_prompt}

ITERATION CONTEXT
---------------------------------------------
You previously generated this proposal:

{original_proposal_json}

The creator has requested changes:

"{feedback}"

Generate an UPDATED proposal that addresses the feedback while preserving the
strengths of the original. Output the complete proposal JSON (not a diff).
"""


def get_available_materials(tier_filter: list[int] | None = None) -> list[str]:
    """Return the flat list of material systems available for the given tiers."""
    palette = DEFAULT_MATERIAL_PALETTE
    tiers = tier_filter or [1, 2, 3]
    materials: list[str] = []
    if 1 in tiers:
        materials.extend(palette["tier_1_deployable_now"])
    if 2 in tiers:
        materials.extend(palette["tier_2_near_term"])
    if 3 in tiers:
        materials.extend(palette["tier_3_long_term"])
    return materials
