"""
Hardcoded service registry for the SPHERES ecosystem.

Each entry describes one micro-service: where it lives, what endpoints it
exposes, and what it does.  In production these would come from a discovery
mechanism; for now the brain keeps the canonical list.
"""

from models.services import ServiceEndpoint, ServiceInfo


# ── spheres-assets ─────────────────────────────────────────────────────────

ASSETS_SERVICE = ServiceInfo(
    name="spheres-assets",
    url="http://localhost:8000",
    port=8000,
    status="up",
    description=(
        "Philadelphia parcel & vacancy data engine. Provides real-time "
        "property records, ownership history, zoning classification, and "
        "vacancy status for every parcel in the city."
    ),
    health_endpoint="/health",
    endpoints=[
        ServiceEndpoint(
            path="/api/parcels/{parcel_id}",
            method="GET",
            description="Look up a single parcel by OPA parcel ID",
        ),
        ServiceEndpoint(
            path="/api/parcels/search",
            method="GET",
            description="Search parcels by address, owner, or zoning code",
        ),
        ServiceEndpoint(
            path="/api/vacancy",
            method="GET",
            description="Vacancy data: counts, durations, neighborhood roll-ups",
        ),
        ServiceEndpoint(
            path="/api/ownership/{parcel_id}",
            method="GET",
            description="Full ownership chain for a parcel",
        ),
    ],
)


# ── spheres-legal ──────────────────────────────────────────────────────────

LEGAL_SERVICE = ServiceInfo(
    name="spheres-legal",
    url="http://localhost:8006",
    port=8006,
    description=(
        "Permit navigator and contract generator. Guides users through "
        "Philadelphia's L&I permitting process and produces activation-ready "
        "legal documents."
    ),
    health_endpoint="/health",
    endpoints=[
        ServiceEndpoint(
            path="/api/permits/navigate",
            method="POST",
            description="Determine required permits for a given activation type and parcel",
        ),
        ServiceEndpoint(
            path="/api/contracts/generate",
            method="POST",
            description="Generate a land-use, lease, or cooperation agreement",
        ),
        ServiceEndpoint(
            path="/api/policies",
            method="GET",
            description="Browse the Philadelphia policy library relevant to vacant-lot activation",
        ),
        ServiceEndpoint(
            path="/api/permits/status/{application_id}",
            method="GET",
            description="Check the status of a submitted permit application",
        ),
    ],
)


# ── spheres-studio ─────────────────────────────────────────────────────────

STUDIO_SERVICE = ServiceInfo(
    name="spheres-studio",
    url="http://localhost:8007",
    port=8007,
    description=(
        "Community design studio. Enables residents to create, share, and "
        "vote on activation designs for vacant parcels — gardens, murals, "
        "pocket parks, micro-markets, and more."
    ),
    health_endpoint="/health",
    endpoints=[
        ServiceEndpoint(
            path="/api/designs",
            method="GET",
            description="List community designs, filterable by parcel, creator, or category",
        ),
        ServiceEndpoint(
            path="/api/designs",
            method="POST",
            description="Submit a new activation design",
        ),
        ServiceEndpoint(
            path="/api/designs/{design_id}/cost",
            method="GET",
            description="Get a detailed cost estimate for a design",
        ),
        ServiceEndpoint(
            path="/api/designs/{design_id}/timeline",
            method="GET",
            description="Generate an implementation timeline for a design",
        ),
    ],
)


# ── spheres-viz ────────────────────────────────────────────────────────────

VIZ_SERVICE = ServiceInfo(
    name="spheres-viz",
    url="http://localhost:8008",
    port=8008,
    description=(
        "Cinematic scroll experience with Three.js 3D worlds. Each episode "
        "maps to a Philadelphia neighborhood and tells the story of vacancy, "
        "community, and transformation."
    ),
    health_endpoint="/health",
    endpoints=[
        ServiceEndpoint(
            path="/api/episodes",
            method="GET",
            description="List all available episodes",
        ),
        ServiceEndpoint(
            path="/api/episodes/{episode_id}",
            method="GET",
            description="Get full episode data including 3D scene configuration",
        ),
        ServiceEndpoint(
            path="/api/episodes/{episode_id}/worlds",
            method="GET",
            description="Retrieve Three.js world assets for an episode",
        ),
        ServiceEndpoint(
            path="/api/scroll/{episode_id}",
            method="GET",
            description="Scroll-experience metadata and keyframe definitions",
        ),
    ],
)


# ── spheres-lab ───────────────────────────────────────────────────────────

LAB_SERVICE = ServiceInfo(
    name="spheres-lab",
    url="http://localhost:8010",
    port=8010,
    description=(
        "Innovation and collaboration lab. Manages teammate profiles, "
        "innovation projects, collaborative sessions, and AI-assisted "
        "generation for community activation ideas."
    ),
    health_endpoint="/health",
    endpoints=[
        ServiceEndpoint(
            path="/api/teammates",
            method="GET",
            description="List all teammates and collaborators",
        ),
        ServiceEndpoint(
            path="/api/innovations",
            method="GET",
            description="Browse innovation projects and proposals",
        ),
        ServiceEndpoint(
            path="/api/stats",
            method="GET",
            description="Lab-wide statistics and metrics",
        ),
        ServiceEndpoint(
            path="/api/collaborations",
            method="GET",
            description="Active and past collaboration records",
        ),
        ServiceEndpoint(
            path="/api/sessions",
            method="GET",
            description="Lab working sessions and events",
        ),
        ServiceEndpoint(
            path="/api/generate",
            method="POST",
            description="AI-assisted generation for activation ideas and designs",
        ),
    ],
)


# ── Canonical list ─────────────────────────────────────────────────────────

SPHERES_SERVICES: list[ServiceInfo] = [
    ASSETS_SERVICE,
    LEGAL_SERVICE,
    STUDIO_SERVICE,
    VIZ_SERVICE,
    LAB_SERVICE,
]

# Quick lookup by name
SERVICE_MAP: dict[str, ServiceInfo] = {s.name: s for s in SPHERES_SERVICES}
