"""Tests for production proposal generator."""

import json
import uuid
from pathlib import Path
from unittest.mock import AsyncMock, patch, MagicMock

import pytest

from src.productions.generator import generate_production_proposal, _extract_json
from src.productions.prompts import build_system_prompt, format_material_palette


FIXTURES_PATH = Path(__file__).parent.parent / "fixtures" / "claude_responses.json"


@pytest.fixture
def mock_proposal_data():
    with open(FIXTURES_PATH) as f:
        return json.load(f)["basic_production_proposal"]


class TestExtractJson:
    def test_direct_json(self):
        data = '{"title": "Test"}'
        assert _extract_json(data) == {"title": "Test"}

    def test_json_in_code_fence(self):
        data = 'Some text\n```json\n{"title": "Test"}\n```\nMore text'
        assert _extract_json(data) == {"title": "Test"}

    def test_json_in_text(self):
        data = 'Here is the proposal: {"title": "Test"} and that is all.'
        assert _extract_json(data) == {"title": "Test"}

    def test_invalid_json(self):
        assert _extract_json("not json at all") == {}


class TestBuildSystemPrompt:
    def test_includes_site_context(self):
        prompt = build_system_prompt(
            area_sqft=10000,
            census_block_group="421010100001",
            zoning="CMX-3",
            street_frontage_ft=120,
            tier_filter=None,
            format_constraint=None,
        )
        assert "10000" in prompt
        assert "CMX-3" in prompt
        assert "Material Dramaturgy" in prompt.upper() or "DRAMATURGY" in prompt

    def test_tier_filter(self):
        prompt = build_system_prompt(
            area_sqft=5000, census_block_group=None, zoning=None,
            street_frontage_ft=None, tier_filter=[1], format_constraint="short",
        )
        assert "acoustic_metamaterial" in prompt
        assert "TIER 1" in prompt


class TestFormatMaterialPalette:
    def test_all_tiers(self):
        text = format_material_palette(None)
        assert "TIER 1" in text
        assert "TIER 2" in text
        assert "TIER 3" in text

    def test_single_tier(self):
        text = format_material_palette([1])
        assert "TIER 1" in text
        assert "TIER 2" not in text


class TestGenerateProposal:
    @pytest.mark.asyncio
    async def test_generates_proposal(self, mock_proposal_data):
        mock_response = MagicMock()
        mock_response.content = [MagicMock(text=json.dumps(mock_proposal_data))]

        mock_client = AsyncMock()
        mock_client.messages.create = AsyncMock(return_value=mock_response)

        with patch("src.productions.generator.AsyncAnthropic", return_value=mock_client):
            proposal = await generate_production_proposal(
                parcel_id=uuid.uuid4(),
                area_sqft=10000,
                zoning="CMX-3",
            )

        assert proposal.title == "The Breathing Wall"
        assert len(proposal.material_script) >= 3
        assert proposal.genre == "experimental"

    @pytest.mark.asyncio
    async def test_proposal_has_all_acts(self, mock_proposal_data):
        """Every proposal must have at least 1 MaterialCue per act."""
        beats = {cue["beat_id"] for cue in mock_proposal_data["material_script"]}
        # Should have setup, middle, and resolution beats
        assert any("act1" in b for b in beats)
        assert any("act2" in b or "climax" in b for b in beats)
        assert any("denouement" in b or "resolution" in b for b in beats)

    def test_fixture_has_valid_material_systems(self, mock_proposal_data):
        from src.productions.models import MATERIAL_SYSTEMS_LIST
        for cue in mock_proposal_data["material_script"]:
            assert cue["material_system"] in MATERIAL_SYSTEMS_LIST

    def test_fixture_olfactory_spacing(self, mock_proposal_data):
        """Olfactory changes must be ≥600s apart."""
        olfactory_cues = [
            c for c in mock_proposal_data["material_script"]
            if c["material_system"] == "olfactory_synthesis"
        ]
        for i in range(1, len(olfactory_cues)):
            prev_end = olfactory_cues[i-1]["timestamp_range"][1]
            curr_start = olfactory_cues[i]["timestamp_range"][0]
            assert curr_start - prev_end >= 600, "Olfactory transitions too close"
