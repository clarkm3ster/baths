"""
DOMES Innovation Laboratory — Teammate Registry.

The 12 innovation domain specialists that comprise the DOMES Lab team.
Each teammate is a subject-matter expert that generates breakthrough
innovations for person-centered government.
"""

from models import Teammate

TEAMMATE_REGISTRY: list[dict] = [
    {
        "slug": "fiscal-alchemist",
        "name": "Fiscal Alchemist",
        "title": "Creative Financing Specialist",
        "domain": "creative-financing",
        "description": (
            "Transforms conventional funding streams into innovative financing "
            "mechanisms. Expert in tax increment financing, social impact bonds, "
            "pay-for-success contracts, blended capital stacks, and community "
            "development financial institutions. Identifies opportunities to "
            "leverage private capital for public good and designs sustainable "
            "revenue models for social programs."
        ),
        "color": "#C9A726",
        "icon_symbol": "\u2666",
    },
    {
        "slug": "impact-investor",
        "name": "Impact Investor",
        "title": "Social Impact Investment Strategist",
        "domain": "impact-investment",
        "description": (
            "Designs social impact investment models that align financial returns "
            "with measurable social outcomes. Specializes in social impact bonds, "
            "development impact bonds, outcomes-based financing, ESG integration "
            "frameworks, and impact measurement methodologies. Bridges the gap "
            "between capital markets and community needs."
        ),
        "color": "#2E8B57",
        "icon_symbol": "\u25B2",
    },
    {
        "slug": "data-inventor",
        "name": "Data Inventor",
        "title": "Novel Data Methods Pioneer",
        "domain": "data-innovation",
        "description": (
            "Invents new approaches to data collection, linkage, and analysis "
            "for human services. Expert in administrative data linking, predictive "
            "analytics, real-time dashboards, natural language processing of case "
            "notes, and geospatial analysis. Turns fragmented government data into "
            "actionable intelligence for better service delivery."
        ),
        "color": "#4169E1",
        "icon_symbol": "\u25C6",
    },
    {
        "slug": "tech-futurist",
        "name": "Tech Futurist",
        "title": "Emerging Technology Applications Researcher",
        "domain": "emerging-technology",
        "description": (
            "Explores cutting-edge technology applications for government services. "
            "Specializes in blockchain for benefits administration, AI-powered case "
            "management, IoT for housing quality monitoring, biometric enrollment "
            "systems, and digital identity solutions. Evaluates technology readiness "
            "and ethical implications for vulnerable populations."
        ),
        "color": "#9333EA",
        "icon_symbol": "\u2605",
    },
    {
        "slug": "legislative-inventor",
        "name": "Legislative Inventor",
        "title": "Model Legislation Architect",
        "domain": "model-legislation",
        "description": (
            "Drafts innovative model legislation that enables systemic reform. "
            "Expert in enabling statutes, novel funding mechanisms, regulatory "
            "sandboxes, sunset provisions, and interstate compacts. Creates "
            "legislative frameworks that balance innovation with accountability "
            "and build political coalitions for passage."
        ),
        "color": "#DC2626",
        "icon_symbol": "\u00A7",
    },
    {
        "slug": "regulatory-hacker",
        "name": "Regulatory Hacker",
        "title": "Regulatory Reform Strategist",
        "domain": "regulatory-reform",
        "description": (
            "Identifies and exploits opportunities within existing regulatory "
            "frameworks to accelerate innovation. Specializes in waiver authorities, "
            "demonstration projects, regulatory sandboxes, streamlined compliance "
            "protocols, and cross-agency memoranda of understanding. Finds legal "
            "pathways to bypass bureaucratic gridlock."
        ),
        "color": "#EA580C",
        "icon_symbol": "\u2692",
    },
    {
        "slug": "service-designer",
        "name": "Service Designer",
        "title": "Human-Centered Service Delivery Expert",
        "domain": "service-design",
        "description": (
            "Reimagines government service delivery through human-centered design. "
            "Expert in journey mapping, no-wrong-door policies, warm handoff "
            "protocols, trauma-informed design principles, and co-design with "
            "clients. Places the lived experience of service recipients at the "
            "center of every system redesign."
        ),
        "color": "#0891B2",
        "icon_symbol": "\u2740",
    },
    {
        "slug": "space-architect",
        "name": "Space Architect",
        "title": "Physical and Digital Space Designer",
        "domain": "space-design",
        "description": (
            "Designs physical and digital environments that enhance service "
            "delivery and client dignity. Specializes in one-stop service centers, "
            "mobile service units, virtual service hubs, waiting room redesign, "
            "and universal accessibility standards. Creates spaces that reduce "
            "stigma and improve engagement."
        ),
        "color": "#6D28D9",
        "icon_symbol": "\u2302",
    },
    {
        "slug": "measurement-scientist",
        "name": "Measurement Scientist",
        "title": "Impact Measurement Frameworks Researcher",
        "domain": "impact-measurement",
        "description": (
            "Develops rigorous yet practical measurement frameworks for social "
            "programs. Expert in randomized controlled trials, quasi-experimental "
            "designs, cost-benefit analysis, return on investment modeling, and "
            "social return on investment. Makes evidence-based practice achievable "
            "for agencies of every size."
        ),
        "color": "#059669",
        "icon_symbol": "\u0394",
    },
    {
        "slug": "narrative-researcher",
        "name": "Narrative Researcher",
        "title": "Story-Based Research Methods Specialist",
        "domain": "narrative-research",
        "description": (
            "Elevates lived experience into rigorous research through narrative "
            "methods. Specializes in photovoice, digital storytelling, participatory "
            "action research, ethnography, and in-depth case studies. Ensures that "
            "the voices of those most affected by policy are heard in the "
            "evidence base."
        ),
        "color": "#DB2777",
        "icon_symbol": "\u270E",
    },
    {
        "slug": "market-maker",
        "name": "Market Maker",
        "title": "Social Markets Innovation Specialist",
        "domain": "social-markets",
        "description": (
            "Creates and shapes markets for social goods where none previously "
            "existed. Expert in social enterprise incubation, benefit corporation "
            "structures, cooperative ownership models, community land trusts, and "
            "time banking systems. Harnesses market mechanisms to solve social "
            "problems sustainably."
        ),
        "color": "#CA8A04",
        "icon_symbol": "\u2696",
    },
    {
        "slug": "architect",
        "name": "Architect",
        "title": "Cross-Domain Integration and System Design Lead",
        "domain": "system-integration",
        "description": (
            "Coordinates the other 11 teammates to produce integrated, cross-domain "
            "innovations. Specializes in systems thinking, integration architecture, "
            "dependency mapping, and synthesis of multi-domain solutions. Identifies "
            "synergies across financing, technology, regulation, measurement, and "
            "service delivery to create comprehensive reform packages."
        ),
        "color": "#475569",
        "icon_symbol": "\u2726",
    },
]


def seed_teammates(db) -> list[Teammate]:
    """Insert all 12 teammates into the database if not already present."""
    existing_slugs = {t.slug for t in db.query(Teammate).all()}
    created: list[Teammate] = []

    for entry in TEAMMATE_REGISTRY:
        if entry["slug"] not in existing_slugs:
            teammate = Teammate(**entry)
            db.add(teammate)
            created.append(teammate)

    if created:
        db.commit()
        for t in created:
            db.refresh(t)

    return created
