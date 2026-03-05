"""
Discovery Scanner
=================
Continuously scans for new opportunities for public space activation
in Philadelphia.  Each scan method returns seeded, realistic data that
mirrors what an actual integration with city open-data portals, news
APIs, and policy feeds would surface.

All addresses, parcels, and policy references use real Philadelphia
neighborhoods, plausible zoning codes, and actual civic context.
"""

from __future__ import annotations

from datetime import datetime, date, timedelta
from typing import Optional

from models.discovery import (
    ComparableCity,
    Discovery,
    DiscoveryType,
    ImpactLevel,
    Location,
    PolicyUpdate,
    ScanResult,
)


def _now() -> datetime:
    return datetime.utcnow()


def _days_ago(n: int) -> datetime:
    return _now() - timedelta(days=n)


def _date_days_ago(n: int) -> date:
    return date.today() - timedelta(days=n)


class DiscoveryScanner:
    """
    The scanner is the SPHERES system's eyes and ears.  It watches
    Philadelphia's data landscape — parcels, policy, news, and peer
    cities — and surfaces anything relevant to public-space activation.
    """

    # ------------------------------------------------------------------
    # Parcel scanning
    # ------------------------------------------------------------------

    def scan_new_parcels(self) -> list[Discovery]:
        """
        Return 8-10 recently discovered vacant or city-owned parcels
        with realistic Philadelphia addresses, zoning, and area data.
        """
        parcels = [
            Discovery(
                id="disc-parcel-001",
                type=DiscoveryType.new_parcel,
                title="Vacant lot at 2741 N Broad St, North Philadelphia",
                description=(
                    "City-owned vacant parcel, 4,200 sq ft, zoned RSA-5. "
                    "Previously a rowhouse demolished in 2019. Adjacent to "
                    "SEPTA Broad Street Line Erie station. Sidewalk frontage "
                    "on Broad Street with high pedestrian visibility. Soil "
                    "assessment completed — no remediation required."
                ),
                source="Philadelphia Land Bank Inventory",
                url="https://phl.maps.arcgis.com/landbank/2741-n-broad",
                discovered_at=_days_ago(2),
                relevance_score=92,
                tags=["vacant", "city-owned", "transit-adjacent", "north-philly", "no-remediation"],
                location=Location(lat=40.0082, lng=-75.1535, neighborhood="North Philadelphia"),
            ),
            Discovery(
                id="disc-parcel-002",
                type=DiscoveryType.new_parcel,
                title="Double lot at 1823-1825 S 58th St, Kingsessing",
                description=(
                    "Two adjacent vacant lots totaling 5,600 sq ft, zoned "
                    "RSA-3. Former auto repair site cleared by L&I in 2023. "
                    "Located two blocks from Kingsessing Rec Center. "
                    "Community group (Kingsessing Renewal) has expressed "
                    "interest in garden use. Phase I ESA shows minor fill "
                    "material — low-cost remediation possible."
                ),
                source="Philadelphia Land Bank Inventory",
                url="https://phl.maps.arcgis.com/landbank/1823-s-58th",
                discovered_at=_days_ago(5),
                relevance_score=85,
                tags=["vacant", "double-lot", "community-interest", "kingsessing", "garden-candidate"],
                location=Location(lat=39.9411, lng=-75.2375, neighborhood="Kingsessing"),
            ),
            Discovery(
                id="disc-parcel-003",
                type=DiscoveryType.new_parcel,
                title="Corner lot at 3rd & Girard, Fishtown/Northern Liberties",
                description=(
                    "Triangular 2,800 sq ft parcel at busy intersection. "
                    "Zoned CMX-2, allowing commercial mixed use. Previously "
                    "gas station — Phase II ESA cleared in 2024 after tank "
                    "removal. Extremely high foot traffic from Girard Ave "
                    "trolley stop and adjacent restaurants. Ideal for popup "
                    "activation or public art."
                ),
                source="OPA Property Assessment",
                url="https://property.phila.gov/detail/3rd-girard",
                discovered_at=_days_ago(1),
                relevance_score=95,
                tags=["corner-lot", "high-visibility", "cleared-esa", "fishtown", "transit-adjacent"],
                location=Location(lat=39.9714, lng=-75.1363, neighborhood="Fishtown"),
            ),
            Discovery(
                id="disc-parcel-004",
                type=DiscoveryType.new_parcel,
                title="Large vacant at 4512 Lancaster Ave, West Philadelphia",
                description=(
                    "10,400 sq ft lot, zoned CMX-2.5. Former warehouse "
                    "demolished 2021. Flat topography, existing chain-link "
                    "fencing. Three blocks from 46th St Market-Frankford "
                    "station. Neighborhood plan (West Philly Promise Zone) "
                    "identifies site for community space. PRA transfer "
                    "eligible."
                ),
                source="Philadelphia Redevelopment Authority",
                url="https://www.phila.gov/pra/properties/4512-lancaster",
                discovered_at=_days_ago(3),
                relevance_score=88,
                tags=["large-lot", "pra-eligible", "west-philly", "promise-zone", "transit-adjacent"],
                location=Location(lat=39.9622, lng=-75.2185, neighborhood="West Philadelphia"),
            ),
            Discovery(
                id="disc-parcel-005",
                type=DiscoveryType.new_parcel,
                title="Side yard at 2208 E Clearfield St, Kensington",
                description=(
                    "1,400 sq ft narrow side lot between occupied rowhouses. "
                    "Zoned RSA-5. City-owned, currently unmaintained. "
                    "Neighbors have been mowing and using informally as "
                    "gathering space. PHS LandCare expressed interest. "
                    "Strong candidate for community stewardship transfer."
                ),
                source="Philadelphia Land Bank Inventory",
                url="https://phl.maps.arcgis.com/landbank/2208-clearfield",
                discovered_at=_days_ago(7),
                relevance_score=72,
                tags=["side-lot", "community-maintained", "kensington", "phs-landcare", "small"],
                location=Location(lat=39.9931, lng=-75.1178, neighborhood="Kensington"),
            ),
            Discovery(
                id="disc-parcel-006",
                type=DiscoveryType.new_parcel,
                title="Industrial remnant at Aramingo & Lehigh, Port Richmond",
                description=(
                    "8,100 sq ft former industrial pad, zoned IRMX. Concrete "
                    "slab still in place — could serve as hardscape base for "
                    "market or performance space without major grading. "
                    "Adjacent to Aramingo Ave commercial corridor. Bus routes "
                    "25 and 54 stop within one block."
                ),
                source="OPA Property Assessment",
                url="https://property.phila.gov/detail/aramingo-lehigh",
                discovered_at=_days_ago(4),
                relevance_score=79,
                tags=["industrial", "hardscape", "port-richmond", "market-candidate", "bus-accessible"],
                location=Location(lat=39.9932, lng=-75.1120, neighborhood="Port Richmond"),
            ),
            Discovery(
                id="disc-parcel-007",
                type=DiscoveryType.new_parcel,
                title="Schoolyard-adjacent lot at 19th & Tasker, Point Breeze",
                description=(
                    "3,600 sq ft lot directly behind Andrew Jackson School. "
                    "Zoned RSA-5. School district indicated willingness to "
                    "coordinate shared-use agreement. Could extend schoolyard "
                    "green space into block. Active Point Breeze Community "
                    "Development Corporation in area."
                ),
                source="School District of Philadelphia / Land Bank",
                url="https://phl.maps.arcgis.com/landbank/19th-tasker",
                discovered_at=_days_ago(6),
                relevance_score=83,
                tags=["school-adjacent", "shared-use", "point-breeze", "youth-access", "cdc-active"],
                location=Location(lat=39.9328, lng=-75.1724, neighborhood="Point Breeze"),
            ),
            Discovery(
                id="disc-parcel-008",
                type=DiscoveryType.new_parcel,
                title="Stormwater priority site at 6300 Cobbs Creek Pkwy",
                description=(
                    "6,000 sq ft in flood-prone area along Cobbs Creek. "
                    "PWD Green Stormwater Infrastructure plan flags this "
                    "parcel for bioretention. Dual-benefit opportunity: "
                    "stormwater management + community green space. GSI "
                    "grant funding potentially available through PWD."
                ),
                source="PWD Green City Clean Waters",
                url="https://water.phila.gov/gsi/planning/6300-cobbs-creek",
                discovered_at=_days_ago(8),
                relevance_score=90,
                tags=["stormwater", "gsi", "cobbs-creek", "grant-eligible", "dual-benefit"],
                location=Location(lat=39.9475, lng=-75.2533, neighborhood="Cobbs Creek"),
            ),
            Discovery(
                id="disc-parcel-009",
                type=DiscoveryType.new_parcel,
                title="Germantown Ave frontage, 5600 block",
                description=(
                    "3,200 sq ft lot on the Germantown Avenue commercial "
                    "corridor. Zoned CMX-2. Adjacent to Germantown Espresso "
                    "Bar and a barber shop — built-in foot traffic. Historic "
                    "district overlay applies; design review required but "
                    "community support is strong via Germantown United CDC."
                ),
                source="Philadelphia Land Bank Inventory",
                url="https://phl.maps.arcgis.com/landbank/5600-germantown",
                discovered_at=_days_ago(3),
                relevance_score=81,
                tags=["commercial-corridor", "historic-district", "germantown", "cdc-support", "walkable"],
                location=Location(lat=40.0350, lng=-75.1700, neighborhood="Germantown"),
            ),
        ]
        return parcels

    # ------------------------------------------------------------------
    # Policy scanning
    # ------------------------------------------------------------------

    def scan_policy_changes(self) -> list[PolicyUpdate]:
        """
        Return 4-5 recent policy updates affecting public space
        activation in Philadelphia.
        """
        policies = [
            PolicyUpdate(
                id="pol-001",
                title="City Council Bill 240132: Streamlined Vacant Lot Activation Permits",
                body=(
                    "Amends Chapter 9-600 of the Philadelphia Code to create "
                    "a new 'Temporary Activation Permit' category for vacant "
                    "land.  Reduces permitting timeline from 90 days to 21 "
                    "days for community-led activations under 12 months.  "
                    "Eliminates zoning variance requirement for gardens, "
                    "public art, and popup markets on city-owned land.  "
                    "Sponsored by Councilmember Gauthier (3rd District)."
                ),
                source="Philadelphia City Council",
                effective_date=_date_days_ago(14),
                impact_level=ImpactLevel.high,
                affected_areas=[
                    "North Philadelphia", "West Philadelphia", "Kensington",
                    "Point Breeze", "Strawberry Mansion",
                ],
            ),
            PolicyUpdate(
                id="pol-002",
                title="Zoning Code Amendment: CMX-1 Outdoor Community Use By-Right",
                body=(
                    "The Philadelphia City Planning Commission approved an "
                    "amendment making 'outdoor community use' a by-right "
                    "activity in all CMX-1 zones.  Previously required a "
                    "special exception.  This opens hundreds of small "
                    "commercial parcels to activation without ZBA hearings.  "
                    "Effective immediately upon Mayor's signature."
                ),
                source="City Planning Commission",
                effective_date=_date_days_ago(7),
                impact_level=ImpactLevel.high,
                affected_areas=[
                    "Germantown", "Frankford", "East Passyunk",
                    "Italian Market corridor", "Manayunk",
                ],
            ),
            PolicyUpdate(
                id="pol-003",
                title="PWD Green Stormwater Infrastructure Incentive Expansion",
                body=(
                    "Philadelphia Water Department expanded its GSI grant "
                    "program to cover community-managed green infrastructure "
                    "on vacant lots.  Maximum grant increased from $100K to "
                    "$250K per project.  Projects must demonstrate at least "
                    "1,000 sq ft of pervious surface and community maintenance "
                    "commitment.  Applications rolling through FY2027."
                ),
                source="Philadelphia Water Department",
                effective_date=_date_days_ago(21),
                impact_level=ImpactLevel.medium,
                affected_areas=[
                    "Cobbs Creek", "Eastwick", "Tacony Creek watershed",
                    "Mill Creek", "Nicetown",
                ],
            ),
            PolicyUpdate(
                id="pol-004",
                title="Land Bank Disposition Policy Update: Community Garden Priority",
                body=(
                    "The Philadelphia Land Bank Board voted to add 'active "
                    "community garden' as a priority disposition category, "
                    "alongside affordable housing.  Gardens operating for 2+ "
                    "years on Land Bank parcels may now apply for $1 nominal "
                    "transfers.  Retroactive for gardens established before "
                    "January 2024.  Expected to affect 40-60 parcels citywide."
                ),
                source="Philadelphia Land Bank",
                effective_date=_date_days_ago(30),
                impact_level=ImpactLevel.critical,
                affected_areas=[
                    "Kensington", "Strawberry Mansion", "Mantua",
                    "Sharswood", "Grays Ferry", "Point Breeze",
                ],
            ),
            PolicyUpdate(
                id="pol-005",
                title="L&I Enforcement Directive: Accelerated Demolition of Dangerous Vacant Structures",
                body=(
                    "Department of Licenses & Inspections issued a directive "
                    "to accelerate demolition of 1,200 imminently dangerous "
                    "vacant structures over the next 18 months.  Each "
                    "demolition creates a new vacant lot — potential activation "
                    "site.  SPHERES should track these demolitions as they "
                    "create new inventory.  Priority neighborhoods listed in "
                    "the directive align heavily with SPHERES target areas."
                ),
                source="Department of Licenses & Inspections",
                effective_date=_date_days_ago(10),
                impact_level=ImpactLevel.medium,
                affected_areas=[
                    "North Philadelphia", "Kensington", "Nicetown-Tioga",
                    "Strawberry Mansion", "Haddington",
                ],
            ),
        ]
        return policies

    # ------------------------------------------------------------------
    # Comparable cities
    # ------------------------------------------------------------------

    def scan_comparable_cities(self) -> list[ComparableCity]:
        """
        Return 5-6 innovations from other cities that could inform
        Philadelphia's public-space activation strategy.
        """
        comparables = [
            ComparableCity(
                city="Detroit, MI",
                project_name="Detroit Future City Land Use Framework",
                description=(
                    "Detroit's strategic framework reclassifies 15,000 vacant "
                    "lots into 'productive landscapes' — urban farms, carbon "
                    "forests, and stormwater parks.  Their online parcel "
                    "scoring tool lets residents propose activations and "
                    "see real-time cost estimates.  Two years in, 340 lots "
                    "have been activated through the platform."
                ),
                url="https://detroitfuturecity.com/land-use",
                relevance_to_philly=(
                    "Philadelphia has ~40,000 vacant lots — similar scale to "
                    "Detroit.  The parcel-scoring and resident-proposal tools "
                    "directly mirror what SPHERES is building.  Detroit's "
                    "'productive landscape' taxonomy could inform our "
                    "activation type recommendations."
                ),
                date_published=_date_days_ago(45),
            ),
            ComparableCity(
                city="New York, NY",
                project_name="NYC Parks Without Borders",
                description=(
                    "NYC Parks redesigned 8 parks to remove fences and create "
                    "seamless transitions between park and sidewalk.  The "
                    "program expanded to include 'micro-parks' on DOT-owned "
                    "street-end parcels.  Each micro-park costs $50K-$150K "
                    "and takes 60 days to install using modular components."
                ),
                url="https://www.nycgovparks.org/parks-without-borders",
                relevance_to_philly=(
                    "Philadelphia's Streets Department controls hundreds of "
                    "triangle lots and street stubs.  The modular, fast-deploy "
                    "approach fits our budget constraints and seasonal windows.  "
                    "The 60-day timeline aligns with our Temporary Activation "
                    "Permit pathway."
                ),
                date_published=_date_days_ago(60),
            ),
            ComparableCity(
                city="Barcelona, Spain",
                project_name="Superilles (Superblocks) Expansion Phase 3",
                description=(
                    "Barcelona's latest superblock phase converts 21 more "
                    "intersections into community plazas using tactical "
                    "urbanism — paint, planters, and moveable furniture.  "
                    "Average cost per intersection: EUR 45,000.  Resident "
                    "satisfaction surveys show 78%% approval after 6 months.  "
                    "The city now has a standardized 'activation kit' that "
                    "communities can request."
                ),
                url="https://www.barcelona.cat/superilles",
                relevance_to_philly=(
                    "Philadelphia's grid creates natural superblock geometry.  "
                    "The 'activation kit' concept — standardized, low-cost, "
                    "deployable — is exactly what SPHERES Studio should design "
                    "toward.  Particularly relevant for our popup market and "
                    "rest-stop activation types."
                ),
                date_published=_date_days_ago(30),
            ),
            ComparableCity(
                city="Portland, OR",
                project_name="Depave: Parking Lots to Community Spaces",
                description=(
                    "Depave's 2025 campaign removed 62,000 sq ft of asphalt "
                    "from underused parking lots and converted them to "
                    "pollinator gardens and gathering spaces.  Cost offset "
                    "by stormwater fee credits — property owners save $2-5K/yr "
                    "in stormwater fees after depaving.  Each project "
                    "completed in a single weekend with volunteer labor."
                ),
                url="https://depave.org/projects",
                relevance_to_philly=(
                    "PWD's stormwater fee credit program already exists in "
                    "Philadelphia.  Pairing depaving with GSI grants could "
                    "create a self-funding activation model.  The weekend "
                    "volunteer build approach matches Philadelphia's strong "
                    "civic volunteer culture."
                ),
                date_published=_date_days_ago(20),
            ),
            ComparableCity(
                city="Seoul, South Korea",
                project_name="Sewoon Maker City Rooftop Commons",
                description=(
                    "Seoul transformed the rooftops of 1960s-era Sewoon "
                    "Sangga commercial blocks into interconnected public "
                    "gardens and maker spaces.  The 'sky garden' network "
                    "spans 1 km and connects via elevated walkways.  Built "
                    "incrementally over 3 years using community co-design "
                    "process with 8,000 resident participants."
                ),
                url="https://seoulsolution.kr/en/sewoon-maker-city",
                relevance_to_philly=(
                    "Philadelphia's Gallery/Fashion District and Market East "
                    "corridor have similar multi-block commercial structures "
                    "with underused rooftops.  The incremental, co-design "
                    "approach matches SPHERES' community-engagement model.  "
                    "Relevant precedent for non-ground-level activation."
                ),
                date_published=_date_days_ago(90),
            ),
            ComparableCity(
                city="Los Angeles, CA",
                project_name="LA Forwards Lot-to-Spot Micro-Park Program",
                description=(
                    "LA's rec department partnered with community land trusts "
                    "to convert 150 vacant lots into 'micro-parks' with "
                    "shade structures, seating, and native plantings.  Each "
                    "park serves a half-mile radius with no existing green "
                    "space.  Equity mapping tool ensures 80%% of sites are in "
                    "park-poor census tracts.  Maintenance handled by block "
                    "captains with city stipend."
                ),
                url="https://laparks.org/lot-to-spot",
                relevance_to_philly=(
                    "Philadelphia's park equity gap is severe — 15%% of "
                    "residents live more than a 10-minute walk from a park.  "
                    "The equity-mapping approach and block-captain maintenance "
                    "model could be directly adopted.  Stipended community "
                    "maintenance aligns with existing PHS LandCare program."
                ),
                date_published=_date_days_ago(15),
            ),
        ]
        return comparables

    # ------------------------------------------------------------------
    # Media scanning
    # ------------------------------------------------------------------

    def scan_media(self) -> list[Discovery]:
        """
        Return 6-8 recent news items about Philadelphia public space,
        vacant lots, and community development.
        """
        articles = [
            Discovery(
                id="disc-media-001",
                type=DiscoveryType.media_mention,
                title="'The Lot Next Door' Expansion: PHS to Steward 200 More Vacant Lots",
                description=(
                    "Pennsylvania Horticultural Society announces a $3.4M "
                    "expansion of its LandCare program, adding 200 lots to "
                    "its maintenance portfolio in North Philadelphia and "
                    "Kensington.  Lots will receive fencing, monthly mowing, "
                    "and tree planting.  PHS is seeking community partners "
                    "for 'activation upgrades' beyond basic maintenance."
                ),
                source="The Philadelphia Inquirer",
                url="https://inquirer.com/news/phs-landcare-expansion-2026",
                discovered_at=_days_ago(3),
                relevance_score=94,
                tags=["phs", "landcare", "partnership-opportunity", "north-philly", "kensington"],
            ),
            Discovery(
                id="disc-media-002",
                type=DiscoveryType.media_mention,
                title="City Council Hearing on Vacant Land Strategy Draws 200 Residents",
                description=(
                    "Standing-room-only hearing at City Hall as residents "
                    "from Strawberry Mansion, Point Breeze, and Nicetown "
                    "testified about vacant lot conditions.  Common themes: "
                    "illegal dumping, lack of city maintenance, desire for "
                    "community gardens.  Council President Squilla pledged "
                    "a 'comprehensive vacant land action plan' by Q3 2026."
                ),
                source="Billy Penn (WHYY)",
                url="https://billypenn.com/2026/02/vacant-land-hearing",
                discovered_at=_days_ago(5),
                relevance_score=88,
                tags=["city-council", "community-voice", "policy-momentum", "vacant-land-strategy"],
            ),
            Discovery(
                id="disc-media-003",
                type=DiscoveryType.media_mention,
                title="Strawberry Mansion Urban Farm Wins National Award",
                description=(
                    "The farm at 2900 W Dauphin St, operated by the "
                    "Strawberry Mansion Community Development Corporation, "
                    "received the American Community Gardening Association's "
                    "2026 Outstanding Community Garden award.  The 12,000 "
                    "sq ft site produces 4,000 lbs of produce annually and "
                    "employs 6 neighborhood residents.  Model for SPHERES "
                    "urban farm activations."
                ),
                source="Grid Magazine",
                url="https://gridphilly.com/strawberry-mansion-farm-award",
                discovered_at=_days_ago(8),
                relevance_score=82,
                tags=["urban-farm", "strawberry-mansion", "model-project", "award", "food-access"],
            ),
            Discovery(
                id="disc-media-004",
                type=DiscoveryType.media_mention,
                title="SEPTA Broad Street Line Upgrades Create Green Buffer Opportunity",
                description=(
                    "SEPTA's $180M Broad Street Line modernization includes "
                    "surface-level ventilation upgrades at 6 stations.  "
                    "Construction staging areas — typically 3,000-5,000 sq ft "
                    "— will be available for community use after work "
                    "completes at each station.  SEPTA's real estate team "
                    "is open to interim-use agreements."
                ),
                source="Technical.ly Philly",
                url="https://technical.ly/philly/septa-bsl-green-opportunity",
                discovered_at=_days_ago(2),
                relevance_score=86,
                tags=["septa", "transit", "interim-use", "infrastructure-opportunity", "broad-street"],
            ),
            Discovery(
                id="disc-media-005",
                type=DiscoveryType.media_mention,
                title="Rebuild Initiative Completes 50th Project; Announces Next Phase",
                description=(
                    "The City's $400M Rebuild initiative for parks, recreation "
                    "centers, and libraries has completed 50 projects.  Phase "
                    "3 will prioritize 'neighborhood connectors' — small green "
                    "spaces that link larger parks.  RFQ for design teams "
                    "expected in March 2026.  SPHERES designs could feed into "
                    "this pipeline."
                ),
                source="Philadelphia Citizen",
                url="https://thephiladelphiacitizen.org/rebuild-phase-3",
                discovered_at=_days_ago(6),
                relevance_score=91,
                tags=["rebuild", "city-investment", "rfq-opportunity", "neighborhood-connectors"],
            ),
            Discovery(
                id="disc-media-006",
                type=DiscoveryType.media_mention,
                title="Temple University Students Map 300 'Pocket Park' Candidates in North Philly",
                description=(
                    "A Temple Urban Studies capstone project mapped 300 "
                    "vacant lots within a 10-minute walk of North Philadelphia "
                    "schools and scored them for pocket park potential.  "
                    "Dataset is publicly available on OpenDataPhilly.  "
                    "Methodology aligns closely with SPHERES scoring — could "
                    "be ingested as a data source."
                ),
                source="Temple University News",
                url="https://news.temple.edu/pocket-park-mapping",
                discovered_at=_days_ago(10),
                relevance_score=87,
                tags=["academic-research", "data-source", "north-philly", "youth", "open-data"],
            ),
            Discovery(
                id="disc-media-007",
                type=DiscoveryType.media_mention,
                title="Philadelphia Named Bloomberg Philanthropies 'Public Space Challenge' City",
                description=(
                    "Bloomberg Philanthropies selected Philadelphia as one "
                    "of 5 US cities for its 2026 Public Space Challenge, "
                    "providing $1M in grants for innovative public space "
                    "projects.  Applications open April 2026.  Projects "
                    "must demonstrate community co-design and measurable "
                    "social impact.  SPHERES-designed activations would be "
                    "strong candidates."
                ),
                source="The Philadelphia Inquirer",
                url="https://inquirer.com/news/bloomberg-public-space-challenge-philly",
                discovered_at=_days_ago(1),
                relevance_score=96,
                tags=["funding", "bloomberg", "national-recognition", "grant-opportunity", "co-design"],
            ),
            Discovery(
                id="disc-media-008",
                type=DiscoveryType.media_mention,
                title="Illegal Dumping Crisis: 12,000 Complaints in 2025, Mostly on Vacant Lots",
                description=(
                    "City's 311 data shows illegal dumping complaints hit "
                    "12,000 in 2025 — a 15%% increase.  80%% occur on vacant "
                    "lots.  Streets Commissioner acknowledges that 'activation "
                    "is the best prevention' — lots with community gardens or "
                    "maintained green space see 90%% less dumping.  Strong "
                    "policy argument for SPHERES approach."
                ),
                source="WHYY News",
                url="https://whyy.org/illegal-dumping-vacant-lots-2025",
                discovered_at=_days_ago(4),
                relevance_score=85,
                tags=["illegal-dumping", "311-data", "activation-argument", "citywide", "prevention"],
            ),
        ]
        return articles

    # ------------------------------------------------------------------
    # Infrastructure changes
    # ------------------------------------------------------------------

    def scan_infrastructure_changes(self) -> list[Discovery]:
        """
        Return infrastructure changes near potential activation sites.
        """
        changes = [
            Discovery(
                id="disc-infra-001",
                type=DiscoveryType.infrastructure_change,
                title="New protected bike lane on Spring Garden St (Broad to Delaware)",
                description=(
                    "OTIS completing a 2.1-mile protected bike lane on Spring "
                    "Garden Street.  Creates new foot/bike traffic past 4 "
                    "SPHERES candidate parcels.  Bollard-protected with "
                    "raised curb — adjacent lots gain safety and accessibility "
                    "benefits."
                ),
                source="OTIS / Streets Department",
                url="https://www.phila.gov/otis/spring-garden-bike-lane",
                discovered_at=_days_ago(12),
                relevance_score=74,
                tags=["bike-lane", "spring-garden", "accessibility", "connectivity"],
                location=Location(lat=39.9617, lng=-75.1583, neighborhood="Spring Garden"),
            ),
            Discovery(
                id="disc-infra-002",
                type=DiscoveryType.infrastructure_change,
                title="PWD green gutter installations on 52nd Street corridor",
                description=(
                    "Philadelphia Water Department installing green gutters "
                    "and rain gardens along 52nd Street from Market to "
                    "Baltimore Ave.  Adjacent vacant lots could connect to "
                    "this green infrastructure network.  PWD actively seeking "
                    "partner sites for expanded stormwater capture."
                ),
                source="PWD Green City Clean Waters",
                url="https://water.phila.gov/gsi/52nd-street",
                discovered_at=_days_ago(9),
                relevance_score=80,
                tags=["stormwater", "52nd-street", "west-philly", "gsi-network", "partnership"],
                location=Location(lat=39.9562, lng=-75.2255, neighborhood="West Philadelphia"),
            ),
        ]
        return changes

    # ------------------------------------------------------------------
    # Unified scan
    # ------------------------------------------------------------------

    def run_full_scan(self) -> list[ScanResult]:
        """
        Execute all scan types and return summary results.
        """
        next_scan_time = _now() + timedelta(hours=6)

        parcels = self.scan_new_parcels()
        policies = self.scan_policy_changes()
        comparables = self.scan_comparable_cities()
        media = self.scan_media()
        infra = self.scan_infrastructure_changes()

        return [
            ScanResult(
                scan_type="new_parcels",
                items_found=len(parcels),
                timestamp=_now(),
                next_scan=next_scan_time,
            ),
            ScanResult(
                scan_type="policy_changes",
                items_found=len(policies),
                timestamp=_now(),
                next_scan=next_scan_time,
            ),
            ScanResult(
                scan_type="comparable_cities",
                items_found=len(comparables),
                timestamp=_now(),
                next_scan=next_scan_time + timedelta(hours=18),
            ),
            ScanResult(
                scan_type="media_mentions",
                items_found=len(media),
                timestamp=_now(),
                next_scan=next_scan_time,
            ),
            ScanResult(
                scan_type="infrastructure_changes",
                items_found=len(infra),
                timestamp=_now(),
                next_scan=next_scan_time + timedelta(hours=12),
            ),
        ]

    def get_all_discoveries(self) -> list[Discovery]:
        """Return every discovery from all scan types as a flat list."""
        discoveries: list[Discovery] = []
        discoveries.extend(self.scan_new_parcels())
        discoveries.extend(self.scan_media())
        discoveries.extend(self.scan_infrastructure_changes())

        # Convert policy updates and comparable cities into Discovery objects
        for policy in self.scan_policy_changes():
            discoveries.append(
                Discovery(
                    id=f"disc-{policy.id}",
                    type=DiscoveryType.policy_change,
                    title=policy.title,
                    description=policy.body,
                    source=policy.source,
                    discovered_at=datetime.combine(policy.effective_date, datetime.min.time()),
                    relevance_score=_impact_to_score(policy.impact_level),
                    tags=policy.affected_areas,
                    location=None,
                )
            )

        for comp in self.scan_comparable_cities():
            discoveries.append(
                Discovery(
                    id=f"disc-comp-{comp.city.lower().replace(' ', '-').replace(',', '')}",
                    type=DiscoveryType.comparable_city,
                    title=f"{comp.city}: {comp.project_name}",
                    description=comp.description,
                    source=comp.city,
                    url=comp.url,
                    discovered_at=datetime.combine(comp.date_published, datetime.min.time()),
                    relevance_score=75,
                    tags=[comp.city.lower().split(",")[0]],
                    location=None,
                )
            )

        return discoveries


def _impact_to_score(level: ImpactLevel) -> int:
    """Map impact level to a relevance score."""
    return {
        ImpactLevel.low: 50,
        ImpactLevel.medium: 70,
        ImpactLevel.high: 85,
        ImpactLevel.critical: 95,
    }.get(level, 60)
