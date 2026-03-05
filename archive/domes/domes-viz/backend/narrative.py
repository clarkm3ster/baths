"""
Narrative content API for domes-viz.

Serves the cinematic scroll narrative: six acts that move from darkness to light,
from one man's impossible day to a national transformation.
"""

from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

# ──────────────────────────────────────────────────────────────
# Pydantic models — mirrors the frontend TypeScript types
# ──────────────────────────────────────────────────────────────


class MarcusStop(BaseModel):
    time: str
    description: str


class AnimatedStat(BaseModel):
    value: int
    prefix: str
    suffix: str
    label: str


class KeyStat(BaseModel):
    value: str
    label: str


class WorldEmbed(BaseModel):
    worldId: str  # "renaissance" | "broken-capitol" | "personal-dome"
    overlayText: str
    buttonText: str


class CTA(BaseModel):
    label: str
    href: str
    description: str


class NarrativeSection(BaseModel):
    id: str
    act: str
    headline: str
    subline: Optional[str] = None
    background: str  # "dark" | "mid" | "light"
    sections: Optional[list[str]] = None
    marcusStops: Optional[list[MarcusStop]] = None
    stats: Optional[list[AnimatedStat]] = None
    keyStats: Optional[list[KeyStat]] = None
    world: Optional[WorldEmbed] = None
    ctas: Optional[list[CTA]] = None


# ──────────────────────────────────────────────────────────────
# Narrative data — the complete cinematic scroll content
# ──────────────────────────────────────────────────────────────

NARRATIVE_SECTIONS: list[NarrativeSection] = [
    # OPENING
    NarrativeSection(
        id="opening",
        act="opening",
        headline="The government spends $79,000 a year on Marcus.",
        subline="Nothing gets better.",
        background="dark",
    ),
    # ACT 1 — THE PROMISE
    NarrativeSection(
        id="promise",
        act="promise",
        headline="The Promise",
        background="dark",
        sections=[
            "The Capitol dome was designed to shelter democracy.",
            "What if government had a dome designed to shelter you?",
            "Not a building. A system. A personal infrastructure that wraps around one person and coordinates everything.",
            "We call it a Dome.",
        ],
        keyStats=[
            KeyStat(value="6", label="systems"),
            KeyStat(value="0", label="coordination"),
        ],
        world=WorldEmbed(
            worldId="renaissance",
            overlayText="This is what government was supposed to feel like.",
            buttonText="Enter the Dome",
        ),
    ),
    # ACT 2 — THE REALITY
    NarrativeSection(
        id="reality",
        act="reality",
        headline="The Reality",
        background="dark",
        marcusStops=[
            MarcusStop(
                time="6:40 AM",
                description="Medicaid office. Take a number. Wait 3 hours. Wrong form.",
            ),
            MarcusStop(
                time="10:15 AM",
                description="Housing authority. Different number. Different wait. Different form.",
            ),
            MarcusStop(
                time="1:00 PM",
                description="Child welfare check-in. 'We need your housing verification.' (Still waiting.)",
            ),
            MarcusStop(
                time="2:30 PM",
                description="Workforce development. 'Do you have your Medicaid card?' (Still processing.)",
            ),
            MarcusStop(
                time="4:00 PM",
                description="Probation office. 'Why did you miss your workforce appointment?' (You were here.)",
            ),
            MarcusStop(
                time="5:30 PM",
                description="Back home. Nothing accomplished. $79,000 spent. Try again tomorrow.",
            ),
        ],
        keyStats=[
            KeyStat(value="$79,000", label="per year spent"),
            KeyStat(value="6", label="agencies"),
            KeyStat(value="0", label="coordination"),
            KeyStat(value="0", label="improvement"),
        ],
        world=WorldEmbed(
            worldId="broken-capitol",
            overlayText="This is what it became.",
            buttonText="See the Wreckage",
        ),
    ),
    # ACT 3 — THE VISION
    NarrativeSection(
        id="vision",
        act="vision",
        headline="The Vision",
        background="mid",
        sections=[
            "What if Marcus had a Dome?",
            "One entry point. One coordinator. One record.",
            "His coordinator sees everything: his health needs, his housing situation, his kids' school records, his job training progress.",
            "No more six stops. No more six waits. No more falling through the cracks.",
            "Cost drops from $79,000 to $31,000.",
            "And outcomes actually improve.",
        ],
        keyStats=[
            KeyStat(value="$31,000", label="per year"),
            KeyStat(value="1", label="coordinator"),
            KeyStat(value="1", label="record"),
            KeyStat(value="Real", label="improvement"),
        ],
        world=WorldEmbed(
            worldId="personal-dome",
            overlayText="This is what we're building.",
            buttonText="Enter the Vision",
        ),
    ),
    # ACT 4 — THE MATH
    NarrativeSection(
        id="math",
        act="math",
        headline="The Math",
        background="light",
        stats=[
            AnimatedStat(
                value=48000,
                prefix="$",
                suffix="",
                label="saved per person per year",
            ),
            AnimatedStat(
                value=10000,
                prefix="",
                suffix="",
                label="people in one state pilot",
            ),
            AnimatedStat(
                value=480,
                prefix="$",
                suffix="M",
                label="saved per year, one state",
            ),
            AnimatedStat(
                value=94,
                prefix="$",
                suffix="B",
                label="saved nationally per year",
            ),
        ],
        sections=[
            "Scale it. 10,000 people \u00d7 $48,000 in savings = $480 million per year. In one state.",
            "National scale: $94 billion per year.",
            "Not by spending more. By spending smarter.",
            "Not by adding programs. By connecting them.",
        ],
    ),
    # ACT 5 — THE CALL
    NarrativeSection(
        id="call",
        act="call",
        headline="Build the Dome.",
        subline="The architecture exists. The math works. The technology is ready.",
        background="light",
        ctas=[
            CTA(
                label="See the Data",
                href="/data",
                description="Explore the government data constellation",
            ),
            CTA(
                label="Build a Profile",
                href="/profile",
                description="See how a Dome works for one person",
            ),
            CTA(
                label="Design an Architecture",
                href="/architect",
                description="Design the coordination system",
            ),
            CTA(
                label="Join Us",
                href="#join",
                description="Help build the Dome",
            ),
        ],
    ),
]

# Build a lookup dict for fast access by act name
_SECTIONS_BY_ACT: dict[str, NarrativeSection] = {s.act: s for s in NARRATIVE_SECTIONS}

# ──────────────────────────────────────────────────────────────
# Router
# ──────────────────────────────────────────────────────────────

router = APIRouter()


@router.get("/narrative/sections", response_model=list[NarrativeSection])
def get_sections():
    """Return all narrative sections in act order."""
    return NARRATIVE_SECTIONS


@router.get("/narrative/sections/{act}", response_model=NarrativeSection)
def get_section_by_act(act: str):
    """Return a single narrative section by its act name."""
    section = _SECTIONS_BY_ACT.get(act)
    if section is None:
        valid = ", ".join(_SECTIONS_BY_ACT.keys())
        raise HTTPException(
            status_code=404,
            detail=f"Act '{act}' not found. Valid acts: {valid}",
        )
    return section
