"""
SPHERES Innovation Laboratory — Teammate Registry.
12 specialist agents for public space activation innovation.
"""

from models import Teammate

TEAMMATE_REGISTRY = [
    {
        "slug": "sphere-economist",
        "name": "Sphere Economist",
        "title": "Economic Strategist",
        "domain": "space-economics",
        "description": "Designs business models and economic frameworks for sustainable public space activation — community land trusts, cooperative ownership, social enterprises, and neighborhood economic engines.",
        "color": "#C9A726",
        "icon_symbol": "♦",
    },
    {
        "slug": "revenue-architect",
        "name": "Revenue Architect",
        "title": "Financial Engineer",
        "domain": "revenue-architecture",
        "description": "Engineers revenue streams and financing mechanisms — green bonds, impact funds, tax incentives, and public-private partnerships for transforming vacant lots into community assets.",
        "color": "#2E8B57",
        "icon_symbol": "▲",
    },
    {
        "slug": "space-inventor",
        "name": "Space Inventor",
        "title": "Spatial Innovation Designer",
        "domain": "spatial-invention",
        "description": "Invents novel spatial typologies — pop-up parks, modular urban rooms, pocket forests, adaptive reuse patterns, and community infrastructure prototypes for Philadelphia's 40,000 vacant parcels.",
        "color": "#4169E1",
        "icon_symbol": "◆",
    },
    {
        "slug": "culture-engineer",
        "name": "Culture Engineer",
        "title": "Cultural Program Architect",
        "domain": "cultural-engineering",
        "description": "Engineers cultural programming that transforms empty lots into community stages — public art installations, performance series, maker spaces, heritage celebrations, and neighborhood festivals.",
        "color": "#DB2777",
        "icon_symbol": "✦",
    },
    {
        "slug": "platform-inventor",
        "name": "Platform Inventor",
        "title": "Technology Strategist",
        "domain": "platform-invention",
        "description": "Invents technology platforms for space activation — IoT sensor networks, community engagement apps, digital twins, real-time monitoring dashboards, and data-driven decision tools.",
        "color": "#9333EA",
        "icon_symbol": "★",
    },
    {
        "slug": "world-builder",
        "name": "World Builder",
        "title": "Immersive Experience Designer",
        "domain": "immersive-worlds",
        "description": "Builds immersive 3D worlds and AR/VR experiences that let communities visualize transformed spaces before they're built — WebGL installations, projection mapping, and virtual walkthroughs.",
        "color": "#0891B2",
        "icon_symbol": "⌂",
    },
    {
        "slug": "policy-inventor",
        "name": "Policy Inventor",
        "title": "Policy Innovation Specialist",
        "domain": "policy-invention",
        "description": "Invents policy frameworks — zoning reforms, land bank legislation, community benefit agreements, green infrastructure mandates, and anti-displacement protections for equitable space activation.",
        "color": "#DC2626",
        "icon_symbol": "§",
    },
    {
        "slug": "city-replicator",
        "name": "City Replicator",
        "title": "Scaling Strategist",
        "domain": "city-replication",
        "description": "Designs replication frameworks for scaling Philadelphia's public space model to other cities — playbooks, training programs, franchise models, city partnership agreements, and adaptation guides.",
        "color": "#EA580C",
        "icon_symbol": "⚒",
    },
    {
        "slug": "ecosystem-architect",
        "name": "Ecosystem Architect",
        "title": "Systems Integration Specialist",
        "domain": "ecosystem-architecture",
        "description": "Architects cross-sector partnerships and institutional alignment — governance structures, resource flow networks, collaborative frameworks connecting city agencies, nonprofits, and communities.",
        "color": "#6D28D9",
        "icon_symbol": "❀",
    },
    {
        "slug": "impact-scientist",
        "name": "Impact Scientist",
        "title": "Measurement & Evaluation Lead",
        "domain": "impact-science",
        "description": "Designs rigorous impact measurement systems — SROI calculators, health outcome trackers, property value analyses, community wellbeing indices, and environmental benefit metrics.",
        "color": "#059669",
        "icon_symbol": "Δ",
    },
    {
        "slug": "narrative-designer",
        "name": "Narrative Designer",
        "title": "Story Architect",
        "domain": "narrative-design",
        "description": "Crafts compelling narratives that build public will — documentary series, oral histories, data visualization stories, community journalism platforms, and social media campaigns.",
        "color": "#CA8A04",
        "icon_symbol": "✎",
    },
    {
        "slug": "architect",
        "name": "Lab Architect",
        "title": "Systems Architect",
        "domain": "system-integration",
        "description": "Cross-domain synthesis, dependency mapping, portfolio risk analysis, and technology architecture for the SPHERES Innovation Laboratory.",
        "color": "#475569",
        "icon_symbol": "⚙",
    },
]


def seed_teammates(db):
    """Idempotent: insert teammates that don't already exist."""
    for info in TEAMMATE_REGISTRY:
        existing = db.query(Teammate).filter_by(slug=info["slug"]).first()
        if not existing:
            db.add(Teammate(**info))
    db.commit()
