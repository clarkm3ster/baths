"""
Opportunity Scorer
==================
Multi-factor scoring engine that evaluates vacant parcels for public-space
activation potential.  Each parcel is scored across five dimensions:

  1. **Location**          (0-100) — transit access, foot traffic, visibility
  2. **Permit Readiness**  (0-100) — zoning compatibility, ESA status, ownership
  3. **Community Demand**  (0-100) — CDC activity, 311 complaints, petitions
  4. **Seasonal Fit**      (0-100) — climate readiness for current quarter
  5. **Cost Efficiency**   (0-100) — cost per sq ft vs. activation budget norms

The composite score is a weighted average plus a seasonal bonus/penalty.
The engine is seeded with 15 realistic scored opportunities rooted in real
Philadelphia neighborhoods and streets.
"""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import Optional

from models.discovery import (
    ActivationType,
    Location,
    Opportunity,
    ScoringFactor,
)


def _now() -> datetime:
    return datetime.utcnow()


def _days_ago(n: int) -> datetime:
    return _now() - timedelta(days=n)


# ---------------------------------------------------------------------------
# Weights for composite score
# ---------------------------------------------------------------------------

_WEIGHTS = {
    "location": 0.25,
    "permit_readiness": 0.20,
    "community_demand": 0.25,
    "seasonal_fit": 0.15,
    "cost_efficiency": 0.15,
}


def _composite(factors: list[ScoringFactor], season_bonus: int = 0) -> int:
    """Compute weighted composite score from individual factors."""
    score_map = {f.name: f.score for f in factors}
    weighted = sum(
        score_map.get(name, 50) * weight
        for name, weight in _WEIGHTS.items()
    )
    return max(0, min(100, int(round(weighted)) + season_bonus))


# ---------------------------------------------------------------------------
# Seeded opportunities — 15 realistic Philadelphia parcels
# ---------------------------------------------------------------------------

def _seed_opportunities() -> list[Opportunity]:
    """
    Return 15 pre-scored opportunities spanning Philadelphia neighborhoods.
    Every address, parcel ID, and neighborhood is plausible for Philadelphia.
    """
    seeds: list[Opportunity] = [
        # ── 1. Fishtown / Northern Liberties ─────────────────────────────
        Opportunity(
            id="opp-001",
            parcel_id="31-3-0142-00",
            address="3rd & Girard Ave, Philadelphia, PA 19125",
            neighborhood="Fishtown",
            location=Location(lat=39.9714, lng=-75.1363, neighborhood="Fishtown"),
            recommended_type=ActivationType.popup_market,
            estimated_activation_cost=18_500,
            permit_window_open=True,
            community_demand_score=88,
            season_bonus=8,
            factors=[
                ScoringFactor(name="location", score=96, description="Corner lot at major trolley stop; 15K+ daily pedestrians on Girard Ave"),
                ScoringFactor(name="permit_readiness", score=91, description="Phase II ESA cleared; CMX-2 zoning allows market use by-right"),
                ScoringFactor(name="community_demand", score=88, description="Fishtown Neighbors Assoc formally requested activation; 340 petition signatures"),
                ScoringFactor(name="seasonal_fit", score=80, description="Spring/summer popup market season starting; covered structure extends to fall"),
                ScoringFactor(name="cost_efficiency", score=72, description="$6.61/sq ft — above average due to corner-lot grading and utility hookups"),
            ],
            discovered_at=_days_ago(1),
            score=0,  # placeholder, computed below
        ),

        # ── 2. North Philadelphia / Broad St ─────────────────────────────
        Opportunity(
            id="opp-002",
            parcel_id="43-2-0200-00",
            address="2741 N Broad St, Philadelphia, PA 19132",
            neighborhood="North Philadelphia",
            location=Location(lat=40.0082, lng=-75.1535, neighborhood="North Philadelphia"),
            recommended_type=ActivationType.community_garden,
            estimated_activation_cost=9_200,
            permit_window_open=True,
            community_demand_score=85,
            season_bonus=10,
            factors=[
                ScoringFactor(name="location", score=90, description="Broad Street frontage, 200 ft from Erie BSL station; high visibility corridor"),
                ScoringFactor(name="permit_readiness", score=88, description="City-owned, no remediation needed; RSA-5 allows garden by-right"),
                ScoringFactor(name="community_demand", score=85, description="North Philly Peace Park coalition actively seeking site; 12 volunteer commitments"),
                ScoringFactor(name="seasonal_fit", score=85, description="Soil is prepped; spring planting window ideal for raised-bed installation"),
                ScoringFactor(name="cost_efficiency", score=82, description="$2.19/sq ft — very efficient for 4,200 sq ft garden build"),
            ],
            discovered_at=_days_ago(2),
            score=0,
        ),

        # ── 3. Kingsessing ───────────────────────────────────────────────
        Opportunity(
            id="opp-003",
            parcel_id="40-2-1156-00",
            address="1823-1825 S 58th St, Philadelphia, PA 19143",
            neighborhood="Kingsessing",
            location=Location(lat=39.9411, lng=-75.2375, neighborhood="Kingsessing"),
            recommended_type=ActivationType.urban_farm,
            estimated_activation_cost=14_800,
            permit_window_open=True,
            community_demand_score=79,
            season_bonus=6,
            factors=[
                ScoringFactor(name="location", score=68, description="Residential side street, 2 blocks from Kingsessing Rec Center; moderate foot traffic"),
                ScoringFactor(name="permit_readiness", score=75, description="Low-cost fill remediation needed (~$3K); RSA-3 allows agricultural use"),
                ScoringFactor(name="community_demand", score=79, description="Kingsessing Renewal CDC expressed interest; food desert designation adds urgency"),
                ScoringFactor(name="seasonal_fit", score=78, description="Double lot allows phased build — first beds by April, full farm by June"),
                ScoringFactor(name="cost_efficiency", score=71, description="$2.64/sq ft for 5,600 sq ft — includes soil amendment and water access"),
            ],
            discovered_at=_days_ago(5),
            score=0,
        ),

        # ── 4. West Philadelphia / Lancaster Ave ─────────────────────────
        Opportunity(
            id="opp-004",
            parcel_id="34-1-0488-00",
            address="4512 Lancaster Ave, Philadelphia, PA 19104",
            neighborhood="West Philadelphia",
            location=Location(lat=39.9622, lng=-75.2185, neighborhood="West Philadelphia"),
            recommended_type=ActivationType.performance_space,
            estimated_activation_cost=32_000,
            permit_window_open=True,
            community_demand_score=82,
            season_bonus=5,
            factors=[
                ScoringFactor(name="location", score=85, description="3 blocks from 46th St MFL station; Lancaster Ave commercial corridor; high visibility"),
                ScoringFactor(name="permit_readiness", score=80, description="PRA transfer eligible; CMX-2.5 allows performance use; Promise Zone priority"),
                ScoringFactor(name="community_demand", score=82, description="West Philly Promise Zone plan calls for community space; 3 arts orgs seeking venue"),
                ScoringFactor(name="seasonal_fit", score=70, description="Concrete pad allows year-round use; open-air optimal May-October"),
                ScoringFactor(name="cost_efficiency", score=62, description="$3.08/sq ft — larger site (10,400 sq ft) with stage infrastructure costs"),
            ],
            discovered_at=_days_ago(3),
            score=0,
        ),

        # ── 5. Kensington / Clearfield ───────────────────────────────────
        Opportunity(
            id="opp-005",
            parcel_id="88-2-0347-00",
            address="2208 E Clearfield St, Philadelphia, PA 19134",
            neighborhood="Kensington",
            location=Location(lat=39.9931, lng=-75.1178, neighborhood="Kensington"),
            recommended_type=ActivationType.pocket_park,
            estimated_activation_cost=6_200,
            permit_window_open=True,
            community_demand_score=91,
            season_bonus=4,
            factors=[
                ScoringFactor(name="location", score=62, description="Narrow side lot on residential block; limited visibility but strong neighbor use"),
                ScoringFactor(name="permit_readiness", score=85, description="City-owned, clean; neighbors already maintaining — community stewardship fast-track"),
                ScoringFactor(name="community_demand", score=91, description="Neighbors mow and use as gathering space; PHS LandCare partnership ready"),
                ScoringFactor(name="seasonal_fit", score=75, description="Small scope allows rapid install; benches and plantings in 2 weekends"),
                ScoringFactor(name="cost_efficiency", score=90, description="$4.43/sq ft but only 1,400 sq ft — total cost very low for community impact"),
            ],
            discovered_at=_days_ago(7),
            score=0,
        ),

        # ── 6. Port Richmond / Aramingo ──────────────────────────────────
        Opportunity(
            id="opp-006",
            parcel_id="31-4-0920-00",
            address="Aramingo Ave & Lehigh Ave, Philadelphia, PA 19134",
            neighborhood="Port Richmond",
            location=Location(lat=39.9932, lng=-75.1120, neighborhood="Port Richmond"),
            recommended_type=ActivationType.popup_market,
            estimated_activation_cost=21_000,
            permit_window_open=True,
            community_demand_score=65,
            season_bonus=7,
            factors=[
                ScoringFactor(name="location", score=78, description="Aramingo commercial corridor; bus routes 25 and 54 within 1 block; car traffic high"),
                ScoringFactor(name="permit_readiness", score=70, description="IRMX zone requires special exception for market; concrete pad reduces site prep"),
                ScoringFactor(name="community_demand", score=65, description="Port Richmond Civic Assoc interested but no formal petition; moderate demand"),
                ScoringFactor(name="seasonal_fit", score=82, description="Existing hardscape allows immediate setup; market canopy extends season"),
                ScoringFactor(name="cost_efficiency", score=68, description="$2.59/sq ft for 8,100 sq ft — canopy and electrical add cost over basic activation"),
            ],
            discovered_at=_days_ago(4),
            score=0,
        ),

        # ── 7. Point Breeze / Tasker ─────────────────────────────────────
        Opportunity(
            id="opp-007",
            parcel_id="36-4-0056-00",
            address="19th & Tasker St, Philadelphia, PA 19145",
            neighborhood="Point Breeze",
            location=Location(lat=39.9328, lng=-75.1724, neighborhood="Point Breeze"),
            recommended_type=ActivationType.outdoor_classroom,
            estimated_activation_cost=15_500,
            permit_window_open=True,
            community_demand_score=87,
            season_bonus=8,
            factors=[
                ScoringFactor(name="location", score=80, description="Adjacent to Andrew Jackson School; school-age foot traffic daily; safe walking route"),
                ScoringFactor(name="permit_readiness", score=82, description="School district willing for shared-use agreement; RSA-5 allows educational use"),
                ScoringFactor(name="community_demand", score=87, description="Point Breeze CDC and school PTA both advocating; 60 parent signatures collected"),
                ScoringFactor(name="seasonal_fit", score=76, description="Outdoor classroom optimal April-November; winter requires covered structure add-on"),
                ScoringFactor(name="cost_efficiency", score=73, description="$4.31/sq ft for 3,600 sq ft — includes weather-resistant furniture and teaching wall"),
            ],
            discovered_at=_days_ago(6),
            score=0,
        ),

        # ── 8. Cobbs Creek / Stormwater ──────────────────────────────────
        Opportunity(
            id="opp-008",
            parcel_id="52-3-0278-00",
            address="6300 Cobbs Creek Pkwy, Philadelphia, PA 19151",
            neighborhood="Cobbs Creek",
            location=Location(lat=39.9475, lng=-75.2533, neighborhood="Cobbs Creek"),
            recommended_type=ActivationType.stormwater_garden,
            estimated_activation_cost=28_000,
            permit_window_open=True,
            community_demand_score=72,
            season_bonus=5,
            factors=[
                ScoringFactor(name="location", score=70, description="Cobbs Creek Pkwy frontage; flood-prone area gives dual-benefit justification"),
                ScoringFactor(name="permit_readiness", score=92, description="PWD GSI plan pre-flags parcel; grant funding available; expedited review pathway"),
                ScoringFactor(name="community_demand", score=72, description="Flood-affected residents supportive; Cobbs Creek Neighbors Assoc engaged"),
                ScoringFactor(name="seasonal_fit", score=68, description="Bioretention install best in dry months (June-Sept); native plantings need spring start"),
                ScoringFactor(name="cost_efficiency", score=85, description="$4.67/sq ft but PWD grant covers up to $250K — effective community cost near zero"),
            ],
            discovered_at=_days_ago(8),
            score=0,
        ),

        # ── 9. Germantown / Commercial Corridor ─────────────────────────
        Opportunity(
            id="opp-009",
            parcel_id="22-3-0890-00",
            address="5600 Germantown Ave, Philadelphia, PA 19144",
            neighborhood="Germantown",
            location=Location(lat=40.0350, lng=-75.1700, neighborhood="Germantown"),
            recommended_type=ActivationType.popup_market,
            estimated_activation_cost=19_500,
            permit_window_open=True,
            community_demand_score=83,
            season_bonus=6,
            factors=[
                ScoringFactor(name="location", score=82, description="Germantown Ave commercial corridor; adjacent to coffee shop and barber; built-in traffic"),
                ScoringFactor(name="permit_readiness", score=68, description="Historic district overlay requires design review; CMX-2 allows market by-right otherwise"),
                ScoringFactor(name="community_demand", score=83, description="Germantown United CDC actively championing; 2 existing vendors ready to participate"),
                ScoringFactor(name="seasonal_fit", score=74, description="Weekend market viable April-December with canopy; winter holiday market possible"),
                ScoringFactor(name="cost_efficiency", score=70, description="$6.09/sq ft for 3,200 sq ft — historic compliance adds design/material cost"),
            ],
            discovered_at=_days_ago(3),
            score=0,
        ),

        # ── 10. Strawberry Mansion ───────────────────────────────────────
        Opportunity(
            id="opp-010",
            parcel_id="32-1-1120-00",
            address="2510 N 29th St, Philadelphia, PA 19132",
            neighborhood="Strawberry Mansion",
            location=Location(lat=39.9888, lng=-75.1865, neighborhood="Strawberry Mansion"),
            recommended_type=ActivationType.community_garden,
            estimated_activation_cost=7_200,
            permit_window_open=True,
            community_demand_score=94,
            season_bonus=12,
            factors=[
                ScoringFactor(name="location", score=72, description="Residential block near Fairmount Park edge; moderate foot traffic; park-adjacent benefit"),
                ScoringFactor(name="permit_readiness", score=90, description="Land Bank parcel; garden license pathway clear; $1 nominal transfer eligible"),
                ScoringFactor(name="community_demand", score=94, description="Strawberry Mansion CDC leading effort; 40-family waiting list; national garden award winner nearby"),
                ScoringFactor(name="seasonal_fit", score=88, description="PHS donated materials ready; spring planting window perfect; volunteers committed for March"),
                ScoringFactor(name="cost_efficiency", score=92, description="$3.00/sq ft for 2,400 sq ft — PHS material donation cuts cost 40%"),
            ],
            discovered_at=_days_ago(2),
            score=0,
        ),

        # ── 11. Mantua / 40th St ────────────────────────────────────────
        Opportunity(
            id="opp-011",
            parcel_id="24-2-0335-00",
            address="822 N 40th St, Philadelphia, PA 19104",
            neighborhood="Mantua",
            location=Location(lat=39.9685, lng=-75.1980, neighborhood="Mantua"),
            recommended_type=ActivationType.playground,
            estimated_activation_cost=42_000,
            permit_window_open=False,
            community_demand_score=90,
            season_bonus=3,
            factors=[
                ScoringFactor(name="location", score=76, description="3 blocks from Mantua Haverford Community Center; school bus stop on corner"),
                ScoringFactor(name="permit_readiness", score=55, description="Requires L&I structural review for play equipment; insurance rider needed; 60-day timeline"),
                ScoringFactor(name="community_demand", score=90, description="Mantua Civic Assoc top priority; nearest playground is 0.7 miles; 200+ child households in radius"),
                ScoringFactor(name="seasonal_fit", score=65, description="Equipment install takes 8 weeks; must start by April for summer opening"),
                ScoringFactor(name="cost_efficiency", score=48, description="$8.40/sq ft for 5,000 sq ft — playground equipment and safety surfacing are expensive"),
            ],
            discovered_at=_days_ago(10),
            score=0,
        ),

        # ── 12. Grays Ferry / 29th St ───────────────────────────────────
        Opportunity(
            id="opp-012",
            parcel_id="36-2-0714-00",
            address="1200 S 29th St, Philadelphia, PA 19146",
            neighborhood="Grays Ferry",
            location=Location(lat=39.9380, lng=-75.1880, neighborhood="Grays Ferry"),
            recommended_type=ActivationType.public_art,
            estimated_activation_cost=8_800,
            permit_window_open=True,
            community_demand_score=68,
            season_bonus=2,
            factors=[
                ScoringFactor(name="location", score=65, description="Residential block with party-wall exposure; visible from Grays Ferry Ave intersection"),
                ScoringFactor(name="permit_readiness", score=86, description="Mural Arts pre-approved wall; RSA-5 allows art installation; no variance needed"),
                ScoringFactor(name="community_demand", score=68, description="Grays Ferry Community Council supports; local artist collective has concept ready"),
                ScoringFactor(name="seasonal_fit", score=82, description="Mural painting best in warm dry weather; April-September window"),
                ScoringFactor(name="cost_efficiency", score=88, description="$4.89/sq ft for 1,800 sq ft — Mural Arts provides paint and scaffolding in-kind"),
            ],
            discovered_at=_days_ago(9),
            score=0,
        ),

        # ── 13. Nicetown-Tioga / Germantown Ave ─────────────────────────
        Opportunity(
            id="opp-013",
            parcel_id="43-4-0612-00",
            address="4200 Germantown Ave, Philadelphia, PA 19140",
            neighborhood="Nicetown-Tioga",
            location=Location(lat=40.0120, lng=-75.1640, neighborhood="Nicetown-Tioga"),
            recommended_type=ActivationType.rest_stop,
            estimated_activation_cost=11_000,
            permit_window_open=True,
            community_demand_score=74,
            season_bonus=4,
            factors=[
                ScoringFactor(name="location", score=80, description="Germantown Ave at major bus transfer point; elderly foot traffic from nearby senior center"),
                ScoringFactor(name="permit_readiness", score=78, description="CMX-1 zone — outdoor community use now by-right after recent amendment; quick approval"),
                ScoringFactor(name="community_demand", score=74, description="Senior center director advocating; bus riders need shaded seating; 50 survey responses"),
                ScoringFactor(name="seasonal_fit", score=72, description="Shade structure and benches usable year-round; plantings add spring-summer appeal"),
                ScoringFactor(name="cost_efficiency", score=80, description="$4.40/sq ft for 2,500 sq ft — simple program: shade, seating, signage"),
            ],
            discovered_at=_days_ago(5),
            score=0,
        ),

        # ── 14. Haddington / 60th St ────────────────────────────────────
        Opportunity(
            id="opp-014",
            parcel_id="46-1-0189-00",
            address="6042 Market St, Philadelphia, PA 19151",
            neighborhood="Haddington",
            location=Location(lat=39.9605, lng=-75.2410, neighborhood="Haddington"),
            recommended_type=ActivationType.community_garden,
            estimated_activation_cost=10_500,
            permit_window_open=True,
            community_demand_score=77,
            season_bonus=8,
            factors=[
                ScoringFactor(name="location", score=74, description="Market Street corridor near 60th St MFL station; commercial foot traffic"),
                ScoringFactor(name="permit_readiness", score=80, description="L&I demolition directive creating new inventory; CMX-2 zoning; quick permit path"),
                ScoringFactor(name="community_demand", score=77, description="Haddington Leadership Network collecting interest forms; food desert designation"),
                ScoringFactor(name="seasonal_fit", score=82, description="Demolition clearing site by March; spring planting timeline aligned"),
                ScoringFactor(name="cost_efficiency", score=76, description="$3.00/sq ft for 3,500 sq ft — standard garden build with existing water access"),
            ],
            discovered_at=_days_ago(6),
            score=0,
        ),

        # ── 15. Sharswood / Ridge Ave ────────────────────────────────────
        Opportunity(
            id="opp-015",
            parcel_id="29-1-0445-00",
            address="2300 Ridge Ave, Philadelphia, PA 19121",
            neighborhood="Sharswood",
            location=Location(lat=39.9770, lng=-75.1700, neighborhood="Sharswood"),
            recommended_type=ActivationType.outdoor_classroom,
            estimated_activation_cost=17_000,
            permit_window_open=True,
            community_demand_score=81,
            season_bonus=6,
            factors=[
                ScoringFactor(name="location", score=78, description="Ridge Ave at Sharswood redevelopment zone; PHA investment bringing new families"),
                ScoringFactor(name="permit_readiness", score=84, description="PHA-owned parcel in redevelopment area; cooperative disposition possible; RSA-5 zone"),
                ScoringFactor(name="community_demand", score=81, description="Sharswood/Blumberg Civic Assoc and local school requesting outdoor learning space"),
                ScoringFactor(name="seasonal_fit", score=73, description="Modular design allows phased install; covered pavilion extends to 3-season use"),
                ScoringFactor(name="cost_efficiency", score=69, description="$4.25/sq ft for 4,000 sq ft — weather-resistant teaching wall and seating add cost"),
            ],
            discovered_at=_days_ago(4),
            score=0,
        ),
    ]

    # Compute composite scores
    for opp in seeds:
        opp.score = _composite(opp.factors, opp.season_bonus)

    return seeds


# ---------------------------------------------------------------------------
# Scorer
# ---------------------------------------------------------------------------

class OpportunityScorer:
    """
    Scores vacant parcels across five dimensions and ranks them for
    activation potential.  On construction the scorer seeds itself with
    15 realistic Philadelphia opportunities so the API is never empty.
    """

    def __init__(self) -> None:
        self._opportunities: list[Opportunity] = _seed_opportunities()

    # -- scoring -----------------------------------------------------------

    def score_parcel(
        self,
        parcel_id: str,
        address: str,
        neighborhood: Optional[str] = None,
        location_score: int = 50,
        permit_readiness_score: int = 50,
        community_demand_score: int = 50,
        seasonal_fit_score: int = 50,
        cost_efficiency_score: int = 50,
        season_bonus: int = 0,
        estimated_cost: int = 10_000,
        recommended_type: ActivationType = ActivationType.pocket_park,
    ) -> Opportunity:
        """
        Score a single parcel across all five dimensions and return a
        fully-populated Opportunity.

        In production each factor score would be computed from upstream
        data (transit proximity APIs, zoning databases, 311 feeds, weather
        models, cost databases).  Here callers supply the raw scores and
        the engine assembles the composite.
        """
        factors = [
            ScoringFactor(
                name="location",
                score=max(0, min(100, location_score)),
                description=f"Location score for {address}",
            ),
            ScoringFactor(
                name="permit_readiness",
                score=max(0, min(100, permit_readiness_score)),
                description=f"Permit readiness assessment for parcel {parcel_id}",
            ),
            ScoringFactor(
                name="community_demand",
                score=max(0, min(100, community_demand_score)),
                description=f"Community demand signal for {neighborhood or address}",
            ),
            ScoringFactor(
                name="seasonal_fit",
                score=max(0, min(100, seasonal_fit_score)),
                description=f"Seasonal fit for current quarter",
            ),
            ScoringFactor(
                name="cost_efficiency",
                score=max(0, min(100, cost_efficiency_score)),
                description=f"Cost efficiency at ${estimated_cost:,} estimated activation cost",
            ),
        ]

        composite = _composite(factors, season_bonus)

        opp = Opportunity(
            id=f"opp-{parcel_id}",
            parcel_id=parcel_id,
            address=address,
            score=composite,
            factors=factors,
            season_bonus=season_bonus,
            permit_window_open=permit_readiness_score >= 60,
            community_demand_score=community_demand_score,
            estimated_activation_cost=estimated_cost,
            recommended_type=recommended_type,
            neighborhood=neighborhood,
            location=None,
            discovered_at=_now(),
        )

        # Add to internal store
        self._opportunities.append(opp)
        return opp

    # -- retrieval ---------------------------------------------------------

    def get_top_opportunities(self, limit: int = 10) -> list[Opportunity]:
        """
        Return the top *limit* opportunities sorted by composite score
        (highest first).
        """
        ranked = sorted(
            self._opportunities,
            key=lambda o: o.score,
            reverse=True,
        )
        return ranked[:limit]

    def get_all_opportunities(self) -> list[Opportunity]:
        """Return every scored opportunity, highest score first."""
        return sorted(
            self._opportunities,
            key=lambda o: o.score,
            reverse=True,
        )

    def get_opportunity_by_id(self, opportunity_id: str) -> Optional[Opportunity]:
        """Look up a single opportunity by its ID."""
        for opp in self._opportunities:
            if opp.id == opportunity_id:
                return opp
        return None

    # -- stats -------------------------------------------------------------

    @property
    def total_opportunities(self) -> int:
        return len(self._opportunities)
