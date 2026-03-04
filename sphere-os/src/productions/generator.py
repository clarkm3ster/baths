"""AI production proposal generator using the Anthropic Claude API.

Generates film/TV/short-form production proposals where programmable materials
ARE the narrative medium, using Material Dramaturgy principles.
"""

from __future__ import annotations

import json
import logging
import uuid
from datetime import datetime, timezone

from anthropic import AsyncAnthropic

from src.productions.models import ProductionProposal
from src.productions.prompts import build_system_prompt
from src.shared.settings import settings

logger = logging.getLogger(__name__)

DEFAULT_MODEL = "claude-sonnet-4-20250514"


async def generate_production_proposal(
    parcel_id: uuid.UUID,
    area_sqft: float | None = None,
    census_block_group: str | None = None,
    zoning: str | None = None,
    street_frontage_ft: float | None = None,
    creative_brief: str | None = None,
    tier_filter: list[int] | None = None,
    format_constraint: str | None = None,
    model: str = DEFAULT_MODEL,
) -> ProductionProposal:
    """Generate a production proposal using Claude API.

    Args:
        parcel_id: UUID of the land parcel.
        area_sqft: Parcel area in square feet.
        census_block_group: Census block group code.
        zoning: Philadelphia zoning code.
        street_frontage_ft: Street frontage in feet.
        creative_brief: Optional user creative direction.
        tier_filter: Which TRL tiers to include (e.g., [1, 2]).
        format_constraint: Production format constraint.
        model: Claude model ID.

    Returns:
        A ProductionProposal ready for DB insert.
    """
    system_prompt = build_system_prompt(
        area_sqft=area_sqft,
        census_block_group=census_block_group,
        zoning=zoning,
        street_frontage_ft=street_frontage_ft,
        tier_filter=tier_filter,
        format_constraint=format_constraint,
    )

    user_message = creative_brief or "Propose a production for this site."

    client = AsyncAnthropic(api_key=settings.anthropic_api_key)

    response = await client.messages.create(
        model=model,
        max_tokens=4096,
        system=system_prompt,
        messages=[{"role": "user", "content": user_message}],
    )

    # Extract text content
    raw_text = ""
    for block in response.content:
        if hasattr(block, "text"):
            raw_text += block.text

    # Parse JSON from response
    proposal_data = _extract_json(raw_text)

    # Build the ProductionProposal ORM object
    proposal = ProductionProposal(
        id=uuid.uuid4(),
        parcel_id=parcel_id,
        title=proposal_data.get("title", "Untitled"),
        logline=proposal_data.get("logline", ""),
        genre=proposal_data.get("genre", "experimental"),
        format=proposal_data.get("format", "short"),
        narrative_concept=proposal_data.get("narrative_concept", ""),
        material_script=proposal_data.get("material_script", []),
        min_area_sqft=float(proposal_data.get("min_area_sqft", area_sqft or 5000)),
        required_utilities=proposal_data.get("required_utilities", ["power"]),
        crew_size_estimate=int(proposal_data.get("crew_size_estimate", 10)),
        estimated_budget_low_usd=int(proposal_data.get("estimated_budget_low_usd", 100000)),
        estimated_budget_high_usd=int(proposal_data.get("estimated_budget_high_usd", 500000)),
        production_timeline_weeks=int(proposal_data.get("production_timeline_weeks", 12)),
        legacy_modes=proposal_data.get("legacy_modes", ["living_soundstage"]),
        generated_by_model=model,
        creative_brief=creative_brief,
        generated_at=datetime.now(timezone.utc),
    )

    return proposal


async def iterate_proposal(
    original: ProductionProposal,
    feedback: str,
    model: str = DEFAULT_MODEL,
) -> ProductionProposal:
    """Regenerate a proposal with user feedback, creating a new version.

    The new proposal is linked to the original via parent_proposal_id.
    """
    system_prompt = build_system_prompt(
        area_sqft=original.min_area_sqft,
        census_block_group=None,
        zoning=None,
        street_frontage_ft=None,
        tier_filter=None,
        format_constraint=original.format,
    )

    user_message = f"""Here is the original proposal:
Title: {original.title}
Logline: {original.logline}
Narrative: {original.narrative_concept}

USER FEEDBACK: {feedback}

Please regenerate the proposal incorporating this feedback. Output strict JSON."""

    client = AsyncAnthropic(api_key=settings.anthropic_api_key)

    response = await client.messages.create(
        model=model,
        max_tokens=4096,
        system=system_prompt,
        messages=[{"role": "user", "content": user_message}],
    )

    raw_text = ""
    for block in response.content:
        if hasattr(block, "text"):
            raw_text += block.text

    proposal_data = _extract_json(raw_text)

    new_proposal = ProductionProposal(
        id=uuid.uuid4(),
        parcel_id=original.parcel_id,
        title=proposal_data.get("title", original.title),
        logline=proposal_data.get("logline", original.logline),
        genre=proposal_data.get("genre", original.genre),
        format=proposal_data.get("format", original.format),
        narrative_concept=proposal_data.get("narrative_concept", original.narrative_concept),
        material_script=proposal_data.get("material_script", original.material_script),
        min_area_sqft=float(proposal_data.get("min_area_sqft", original.min_area_sqft)),
        required_utilities=proposal_data.get("required_utilities", list(original.required_utilities)),
        crew_size_estimate=int(proposal_data.get("crew_size_estimate", original.crew_size_estimate)),
        estimated_budget_low_usd=int(proposal_data.get("estimated_budget_low_usd", original.estimated_budget_low_usd)),
        estimated_budget_high_usd=int(proposal_data.get("estimated_budget_high_usd", original.estimated_budget_high_usd)),
        production_timeline_weeks=int(proposal_data.get("production_timeline_weeks", original.production_timeline_weeks)),
        legacy_modes=proposal_data.get("legacy_modes", list(original.legacy_modes)),
        generated_by_model=model,
        creative_brief=original.creative_brief,
        generated_at=datetime.now(timezone.utc),
        parent_proposal_id=original.id,
        iteration_feedback=feedback,
    )

    return new_proposal


def _extract_json(text: str) -> dict:
    """Extract JSON object from Claude's response text."""
    # Try direct parse first
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Try to find JSON block in markdown code fences
    import re
    json_match = re.search(r"```(?:json)?\s*\n?(.*?)\n?```", text, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group(1))
        except json.JSONDecodeError:
            pass

    # Try to find first { ... } block
    brace_start = text.find("{")
    brace_end = text.rfind("}")
    if brace_start >= 0 and brace_end > brace_start:
        try:
            return json.loads(text[brace_start:brace_end + 1])
        except json.JSONDecodeError:
            pass

    logger.error("Failed to parse JSON from Claude response: %s...", text[:200])
    return {}
