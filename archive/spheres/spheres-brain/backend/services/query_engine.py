"""
Unified Query Engine for SPHERES Brain.

Fans out a parcel query to every micro-service in the ecosystem and merges
the results into a single UnifiedParcelResult.  Until the downstream apps
are live, the engine returns rich mock data rooted in real Philadelphia
geography.
"""

import hashlib
from datetime import datetime

from models.services import (
    ActivationRecord,
    CommunityDesign,
    EpisodeAssociation,
    LegalPathway,
    ParcelData,
    ParcelQuery,
    UnifiedParcelResult,
)


# ---------------------------------------------------------------------------
# Seed data — Philadelphia neighbourhoods, addresses, parcels
# ---------------------------------------------------------------------------

_MOCK_PARCELS: dict[str, dict] = {
    # Kensington
    "88-2-0347-00": {
        "parcel_id": "88-2-0347-00",
        "address": "2847 Kensington Ave, Philadelphia, PA 19134",
        "owner": "City of Philadelphia — Vacant Land",
        "zoning": "RSA-5",
        "area_sqft": 1_260.0,
        "vacancy_status": "Vacant 3+ years",
        "assessed_value": 18_500.0,
        "last_sale": "2011-06-14",
        "coordinates": {"lat": 39.9943, "lng": -75.1268},
    },
    # Strawberry Mansion
    "32-1-1120-00": {
        "parcel_id": "32-1-1120-00",
        "address": "2510 N 29th St, Philadelphia, PA 19132",
        "owner": "Philadelphia Land Bank",
        "zoning": "RSA-3",
        "area_sqft": 2_400.0,
        "vacancy_status": "Vacant 5+ years",
        "assessed_value": 12_000.0,
        "last_sale": "2019-03-22",
        "coordinates": {"lat": 39.9888, "lng": -75.1865},
    },
    # Point Breeze
    "36-4-0056-00": {
        "parcel_id": "36-4-0056-00",
        "address": "1523 S 22nd St, Philadelphia, PA 19146",
        "owner": "Private — Estate of Williams Family",
        "zoning": "RSA-5",
        "area_sqft": 960.0,
        "vacancy_status": "Vacant 1-3 years",
        "assessed_value": 42_000.0,
        "last_sale": "2017-11-08",
        "coordinates": {"lat": 39.9335, "lng": -75.1812},
    },
    # Germantown
    "22-3-0890-00": {
        "parcel_id": "22-3-0890-00",
        "address": "5401 Germantown Ave, Philadelphia, PA 19144",
        "owner": "Germantown Community Development Corp",
        "zoning": "CMX-2",
        "area_sqft": 3_600.0,
        "vacancy_status": "Vacant 2+ years",
        "assessed_value": 55_000.0,
        "last_sale": "2020-01-15",
        "coordinates": {"lat": 40.0367, "lng": -75.1727},
    },
    # North Philadelphia
    "43-2-0200-00": {
        "parcel_id": "43-2-0200-00",
        "address": "1800 N Broad St, Philadelphia, PA 19121",
        "owner": "City of Philadelphia — Vacant Land",
        "zoning": "CMX-3",
        "area_sqft": 5_200.0,
        "vacancy_status": "Vacant 7+ years",
        "assessed_value": 85_000.0,
        "last_sale": "2008-04-30",
        "coordinates": {"lat": 39.9781, "lng": -75.1596},
    },
}

# Fallback for any address not in the seed set
_DEFAULT_PARCEL_TEMPLATE = {
    "owner": "City of Philadelphia — Vacant Land",
    "zoning": "RSA-5",
    "area_sqft": 1_500.0,
    "vacancy_status": "Vacant 2+ years",
    "assessed_value": 22_000.0,
    "last_sale": "2015-09-01",
    "coordinates": {"lat": 39.9526, "lng": -75.1652},
}


# ---------------------------------------------------------------------------
# Helper: deterministic parcel_id from an address
# ---------------------------------------------------------------------------

def _address_to_parcel_id(address: str) -> str:
    """Generate a plausible OPA-style parcel ID from an address string."""
    h = hashlib.md5(address.lower().encode()).hexdigest()
    seg1 = int(h[:2], 16) % 99 + 1
    seg2 = int(h[2:4], 16) % 9 + 1
    seg3 = int(h[4:8], 16) % 9999 + 1
    return f"{seg1:02d}-{seg2}-{seg3:04d}-00"


# ---------------------------------------------------------------------------
# Mock data generators per service
# ---------------------------------------------------------------------------

def _get_parcel_data(query: ParcelQuery) -> ParcelData:
    """Resolve parcel data from assets service (mocked)."""
    if query.parcel_id and query.parcel_id in _MOCK_PARCELS:
        return ParcelData(**_MOCK_PARCELS[query.parcel_id])

    # Try matching address substring
    if query.address:
        for rec in _MOCK_PARCELS.values():
            if query.address.lower() in rec["address"].lower():
                return ParcelData(**rec)

    # Generate deterministic record for unknown address
    addr = query.address or "Unknown Address, Philadelphia, PA"
    pid = query.parcel_id or _address_to_parcel_id(addr)
    return ParcelData(
        parcel_id=pid,
        address=addr,
        **_DEFAULT_PARCEL_TEMPLATE,
    )


def _get_legal_pathway(parcel: ParcelData) -> LegalPathway:
    """Determine required permits and legal pathway (mocked)."""
    base_permits = [
        "L&I Vacant Lot Clean-Up Permit",
        "Zoning Use Registration Permit",
    ]

    if parcel.zoning.startswith("CMX"):
        base_permits.append("Commercial Mixed-Use Activity License")
        base_permits.append("Streets Department Sidewalk Occupancy Permit")
        timeline = 75
        fees = 1_850.0
    elif parcel.area_sqft > 3_000:
        base_permits.append("Large-Site Stormwater Management Review")
        timeline = 60
        fees = 1_200.0
    else:
        timeline = 30
        fees = 450.0

    contracts = [
        "Community Land Use Agreement (CLUA)",
        "Volunteer Liability Waiver",
    ]
    if "Land Bank" in parcel.owner:
        contracts.append("Philadelphia Land Bank Garden License")
    if parcel.vacancy_status.startswith("Vacant 5") or parcel.vacancy_status.startswith("Vacant 7"):
        contracts.append("Long-Term Stewardship Agreement")

    return LegalPathway(
        required_permits=base_permits,
        estimated_timeline_days=timeline,
        total_fees=fees,
        recommended_contracts=contracts,
        zoning_notes=(
            f"Parcel is zoned {parcel.zoning}. Community garden and "
            f"open-space activations are permitted by-right under "
            f"Philadelphia zoning code \u00a714-603(6)."
        ),
    )


def _get_community_designs(parcel: ParcelData) -> list[CommunityDesign]:
    """Return seeded community designs (mocked from Studio)."""
    neighborhood = parcel.address.split(",")[0].split()[-2] if "," in parcel.address else "Philadelphia"

    designs = [
        CommunityDesign(
            design_id="DSN-001",
            name=f"{neighborhood} Community Garden",
            creator="Maria Santos",
            description=(
                "Raised-bed urban garden with 24 plots, ADA-accessible "
                "pathways, rain-barrel irrigation, and a tool-share shed."
            ),
            cost_estimate=8_500.0,
            rating=4.7,
            category="Garden",
            thumbnail_url="/designs/thumbnails/community-garden.png",
        ),
        CommunityDesign(
            design_id="DSN-002",
            name=f"{neighborhood} Pocket Park & Reading Nook",
            creator="Darius Johnson",
            description=(
                "Shaded pocket park with native plantings, a Little Free "
                "Library, benches built from reclaimed lumber, and solar "
                "phone-charging stations."
            ),
            cost_estimate=14_200.0,
            rating=4.5,
            category="Park",
            thumbnail_url="/designs/thumbnails/pocket-park.png",
        ),
        CommunityDesign(
            design_id="DSN-003",
            name=f"{neighborhood} Mural & Performance Wall",
            creator="Aisha Williams",
            description=(
                "Large-scale community mural on the lot's party wall, "
                "plus a poured-concrete performance stage for open-mic "
                "nights and neighborhood meetings."
            ),
            cost_estimate=6_800.0,
            rating=4.8,
            category="Art & Culture",
            thumbnail_url="/designs/thumbnails/mural-wall.png",
        ),
        CommunityDesign(
            design_id="DSN-004",
            name=f"{neighborhood} Micro-Market Pavilion",
            creator="Tyrone Mitchell",
            description=(
                "Covered market stall structure for weekend produce sales, "
                "food truck hook-ups, and a community bulletin board."
            ),
            cost_estimate=22_000.0,
            rating=4.3,
            category="Economic",
            thumbnail_url="/designs/thumbnails/micro-market.png",
        ),
        CommunityDesign(
            design_id="DSN-005",
            name=f"{neighborhood} Rain Garden & Bio-Swale",
            creator="Dr. Lena Park",
            description=(
                "Green-infrastructure installation that captures stormwater "
                "from adjacent rooftops, reduces combined-sewer overflow, "
                "and creates pollinator habitat."
            ),
            cost_estimate=11_750.0,
            rating=4.6,
            category="Green Infrastructure",
            thumbnail_url="/designs/thumbnails/rain-garden.png",
        ),
    ]
    return designs


_EPISODES = [
    {
        "episode_number": 1,
        "episode_title": "Kensington \u2014 Roots Under the El",
        "neighborhood": "Kensington",
        "viz_url": "/viz/episodes/1",
    },
    {
        "episode_number": 2,
        "episode_title": "Strawberry Mansion \u2014 The Long Hold",
        "neighborhood": "Strawberry Mansion",
        "viz_url": "/viz/episodes/2",
    },
    {
        "episode_number": 3,
        "episode_title": "Point Breeze \u2014 Between Two Rivers",
        "neighborhood": "Point Breeze",
        "viz_url": "/viz/episodes/3",
    },
    {
        "episode_number": 4,
        "episode_title": "Germantown \u2014 Layered Time",
        "neighborhood": "Germantown",
        "viz_url": "/viz/episodes/4",
    },
    {
        "episode_number": 5,
        "episode_title": "North Broad \u2014 The Corridor of Possibility",
        "neighborhood": "North Philadelphia",
        "viz_url": "/viz/episodes/5",
    },
]


def _get_episode_association(parcel: ParcelData) -> EpisodeAssociation:
    """Map a parcel to its nearest spheres-viz episode (mocked)."""
    addr_lower = parcel.address.lower()

    for ep in _EPISODES:
        if ep["neighborhood"].lower() in addr_lower:
            return EpisodeAssociation(relevance_score=0.95, **ep)

    # Default to the geographically closest (Kensington as fallback)
    return EpisodeAssociation(
        episode_number=1,
        episode_title="Kensington \u2014 Roots Under the El",
        neighborhood="Kensington",
        relevance_score=0.42,
        viz_url="/viz/episodes/1",
    )


def _get_activation_history(parcel: ParcelData) -> list[ActivationRecord]:
    """Return past activations for this parcel (mocked)."""
    # Only some parcels have prior activations
    if "Land Bank" in parcel.owner or parcel.vacancy_status.startswith("Vacant 5"):
        return [
            ActivationRecord(
                activation_id="ACT-2024-018",
                date="2024-06-15",
                activation_type="Community Clean-Up",
                description=(
                    "Neighborhood volunteers removed 2.3 tons of debris, "
                    "installed temporary fencing, and planted 12 trees."
                ),
                status="completed",
                participants=34,
                value_created=4_200.0,
            ),
            ActivationRecord(
                activation_id="ACT-2024-041",
                date="2024-09-22",
                activation_type="Pop-Up Market",
                description=(
                    "Weekend pop-up market with 8 local vendors, live music, "
                    "and a voter-registration drive. Over 300 visitors."
                ),
                status="completed",
                participants=312,
                value_created=6_800.0,
            ),
        ]

    if parcel.vacancy_status.startswith("Vacant 7"):
        return [
            ActivationRecord(
                activation_id="ACT-2023-003",
                date="2023-04-10",
                activation_type="Soil Remediation",
                description=(
                    "Environmental assessment and topsoil replacement "
                    "conducted by Philadelphia Horticultural Society."
                ),
                status="completed",
                participants=8,
                value_created=12_500.0,
            ),
            ActivationRecord(
                activation_id="ACT-2024-055",
                date="2024-11-01",
                activation_type="Community Garden Installation",
                description=(
                    "24 raised beds installed with drip irrigation. "
                    "Waiting list of 40+ families for spring planting."
                ),
                status="in-progress",
                participants=56,
                value_created=8_500.0,
            ),
            ActivationRecord(
                activation_id="ACT-2025-012",
                date="2025-03-15",
                activation_type="Public Art Installation",
                description=(
                    "Mural Arts Philadelphia partnership: 60-foot mural "
                    "depicting the neighborhood's history and future."
                ),
                status="planned",
                participants=0,
                value_created=0.0,
            ),
        ]

    return []


# ---------------------------------------------------------------------------
# Query engine
# ---------------------------------------------------------------------------

class UnifiedQueryEngine:
    """
    Fans out a parcel query to all SPHERES services and merges
    the responses into a single UnifiedParcelResult.
    """

    async def query_parcel(self, query: ParcelQuery) -> UnifiedParcelResult:
        """
        Execute a unified query.  In production each section would be an
        async HTTP call to the respective micro-service; for now we return
        carefully crafted mock data.
        """
        parcel = _get_parcel_data(query)
        legal = _get_legal_pathway(parcel)
        designs = _get_community_designs(parcel)
        episode = _get_episode_association(parcel)
        history = _get_activation_history(parcel)

        return UnifiedParcelResult(
            query=query,
            parcel_data=parcel,
            legal_pathway=legal,
            community_designs=designs,
            episode_association=episode,
            activation_history=history,
            queried_at=datetime.utcnow(),
        )
