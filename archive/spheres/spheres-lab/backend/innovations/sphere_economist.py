"""
SPHERE-ECONOMIST — Sphere Business Model Innovations & Generator Templates.

Six breakthrough business models for transforming Philadelphia's 40,000+ vacant
lots into a self-sustaining network of activated public spaces — branded under
the Sphere platform.  Each model targets real neighborhood geography
(Kensington, Strawberry Mansion, Point Breeze, West Philly, North Philly) and
builds on existing civic infrastructure including the Philadelphia Land Bank,
local CDCs, and anchor institutions.
"""

# ---------------------------------------------------------------------------
# SEED INNOVATIONS (6)
# ---------------------------------------------------------------------------

INNOVATIONS: list[dict] = [
    # 1 — Sphere Exchange
    {
        "title": "Sphere Exchange",
        "summary": (
            "Real-time marketplace for activated public spaces.  Dynamic "
            "pricing model adjusting rates based on demand, season, and space "
            "type.  Revenue projections: $2.1M/year at 200 active parcels.  "
            "Pilot design for 50 parcels across North Philly."
        ),
        "category": "marketplace",
        "impact_level": 5,
        "feasibility": 4,
        "novelty": 5,
        "time_horizon": "near",
        "status": "approved",
        "details": {
            "revenue_model": (
                "Dynamic pricing engine sets per-hour and per-day rates for "
                "each activated parcel based on real-time demand signals, "
                "seasonal patterns, and space typology (green lot, paved "
                "plaza, covered pavilion).  Platform retains a 12% service "
                "fee on every transaction; lot-holding organizations receive "
                "the balance.  Surge pricing during peak weekends and events "
                "captures an additional 15-25% premium."
            ),
            "projected_annual_revenue": "$2.1M/year at 200 active parcels",
            "ownership_structure": (
                "Platform LLC operated by the Sphere team with revenue-"
                "sharing agreements to lot holders (Land Bank, CDCs, private "
                "owners).  Governance advisory board includes neighborhood "
                "representatives from each pilot zone."
            ),
            "pilot_parcels": (
                "50 parcels across North Philly — concentrated along "
                "Germantown Avenue, Broad Street corridor, and the "
                "Strawberry Mansion greenbelt.  Mix of Land Bank transfers "
                "and CDC-managed lots."
            ),
            "roi_analysis": (
                "At 200 parcels with average utilization of 40%, the "
                "exchange generates $2.1M gross revenue.  Platform "
                "operating costs (engineering, support, insurance) run "
                "$620K/year, yielding net operating income of $1.48M.  "
                "Payback on $800K platform build in under 7 months."
            ),
            "beneficiaries": [
                "Event producers and cultural organizations",
                "Micro-retailers and pop-up vendors",
                "Lot-holding organizations earning activation revenue",
                "Neighborhoods gaining foot traffic and economic activity",
                "City of Philadelphia (reduced blight-management costs)",
            ],
        },
        "tags": [
            "sphere-exchange",
            "dynamic-pricing",
            "marketplace",
            "real-time",
            "north-philly",
        ],
    },

    # 2 — Subscription Spheres
    {
        "title": "Subscription Spheres",
        "summary": (
            "$29/month gives access to any activated space citywide — "
            "comparable to a ClassPass model for public space.  Projected "
            "subscriber base: 10,000 in year 1, 45,000 by year 3.  "
            "Revenue: $3.5M/yr at scale.  Includes tiered access "
            "(basic / premium / unlimited)."
        ),
        "category": "subscription",
        "impact_level": 4,
        "feasibility": 4,
        "novelty": 4,
        "time_horizon": "medium",
        "status": "approved",
        "details": {
            "revenue_model": (
                "Three subscription tiers: Basic ($29/month — 4 bookings "
                "per month at any activated space), Premium ($59/month — "
                "12 bookings plus priority reservations), and Unlimited "
                "($99/month — unrestricted access with same-day booking).  "
                "Corporate group plans available at $22/seat/month for 50+ "
                "employees.  Ancillary revenue from equipment add-ons "
                "(chairs, canopies, power hookups) at $15-$50 per session."
            ),
            "projected_annual_revenue": (
                "$3.5M/year at scale (45,000 subscribers by year 3).  "
                "Year 1 target: 10,000 subscribers generating $3.48M "
                "gross across all tiers; net after platform costs ~$1.9M."
            ),
            "ownership_structure": (
                "Sphere platform operates the subscription service.  "
                "Revenue is shared: 70% to Sphere operations and growth, "
                "20% to lot-holding organizations proportional to usage, "
                "10% to a neighborhood reinvestment fund."
            ),
            "pilot_parcels": (
                "Launch with 75 activated parcels across all major "
                "corridors — North Philly, West Philly, Kensington, "
                "Point Breeze, Germantown.  Scale to 200+ parcels by "
                "end of year 2."
            ),
            "roi_analysis": (
                "Customer acquisition cost estimated at $18 per subscriber "
                "via grassroots and social-media campaigns.  Average "
                "subscriber lifetime 14 months.  Lifetime value at Basic "
                "tier: $406.  LTV/CAC ratio of 22.6x makes this a highly "
                "efficient growth model."
            ),
            "beneficiaries": [
                "Residents seeking affordable outdoor gathering spaces",
                "Fitness instructors and wellness practitioners",
                "Community organizations hosting recurring programs",
                "Small businesses testing outdoor retail concepts",
                "Lot-holding organizations earning steady passive revenue",
            ],
        },
        "tags": [
            "subscription-spheres",
            "classpass-model",
            "tiered-access",
            "recurring-revenue",
            "citywide",
        ],
    },

    # 3 — Reverse Spheres
    {
        "title": "Reverse Spheres",
        "summary": (
            "City pays activators a per-parcel monthly subsidy for blight "
            "reduction.  ROI model shows it costs the city $4,200/year per "
            "vacant lot (dumping cleanup, fire response, health costs) vs "
            "$1,800/year for an activation subsidy — 57% cheaper than neglect."
        ),
        "category": "public-subsidy",
        "impact_level": 5,
        "feasibility": 5,
        "novelty": 4,
        "time_horizon": "near",
        "status": "approved",
        "details": {
            "revenue_model": (
                "City of Philadelphia pays Sphere activators $150/month "
                "per parcel ($1,800/year) drawn from existing blight-"
                "remediation and public-health budget lines.  Activators "
                "commit to maintaining safe, clean, publicly accessible "
                "green space with a minimum of 4 programmed events per "
                "month.  Payment is outcome-based: quarterly inspections "
                "confirm compliance before funds are released."
            ),
            "projected_annual_revenue": (
                "$1.8M/year at 1,000 subsidized parcels.  The city saves "
                "$2.4M/year net (difference between $4.2M neglect cost and "
                "$1.8M subsidy cost for the same 1,000 parcels)."
            ),
            "ownership_structure": (
                "Land remains in city or Land Bank ownership.  Sphere "
                "serves as the activation management layer — recruiting, "
                "training, and paying community activators who steward "
                "individual parcels.  Activators retain independence as "
                "neighborhood contractors."
            ),
            "pilot_parcels": (
                "Initial cohort of 200 parcels in the highest-blight "
                "census tracts: North Philly (80 parcels), Kensington "
                "(60 parcels), Strawberry Mansion (40 parcels), and "
                "Nicetown-Tioga (20 parcels)."
            ),
            "roi_analysis": (
                "City currently spends an average of $4,200/year per "
                "vacant lot on illegal-dumping cleanup ($1,800), fire "
                "department responses ($900), rodent abatement ($600), "
                "and public-health interventions ($900).  The $1,800/year "
                "activation subsidy eliminates virtually all of these "
                "costs — a 57% savings per parcel.  At 1,000 parcels the "
                "city nets $2.4M/year in avoided costs."
            ),
            "beneficiaries": [
                "City of Philadelphia (57% cost savings on blight management)",
                "Community activators earning stable income",
                "Residents in high-blight neighborhoods",
                "Philadelphia Fire Department (fewer vacant-lot fires)",
                "Public health system (reduced vector-borne disease exposure)",
            ],
        },
        "tags": [
            "reverse-spheres",
            "blight-reduction",
            "city-subsidy",
            "cost-savings",
            "outcome-based",
        ],
    },

    # 4 — Community Cooperatives
    {
        "title": "Community Cooperatives",
        "summary": (
            "Neighborhood buys ownership of their sphere through community "
            "shares ($25-$500 per resident).  Revenue stays 100% local.  "
            "Governance by elected neighborhood board.  First 3 co-ops: "
            "Strawberry Mansion, Kensington, Point Breeze."
        ),
        "category": "cooperative-ownership",
        "impact_level": 5,
        "feasibility": 3,
        "novelty": 4,
        "time_horizon": "medium",
        "status": "approved",
        "details": {
            "revenue_model": (
                "Community share offerings at $25-$500 per resident raise "
                "acquisition capital.  Once the cooperative owns its sphere "
                "parcels, revenue is generated through space rentals "
                "($50-$300/day), community programming fees, vendor-stall "
                "leases ($200/month), and seasonal event hosting.  All net "
                "revenue is reinvested locally: 60% to parcel maintenance "
                "and improvements, 25% to a community dividend fund, and "
                "15% to an acquisition fund for additional parcels."
            ),
            "projected_annual_revenue": (
                "$120,000-$280,000 per cooperative (5-15 parcels).  "
                "Combined revenue across first 3 co-ops: $500K-$840K/year."
            ),
            "ownership_structure": (
                "Each cooperative is a legally incorporated community "
                "benefit corporation.  One share = one vote regardless of "
                "investment size.  Governance by a 7-member elected "
                "neighborhood board with 2-year terms.  Board seats "
                "reserved: 3 for resident shareholders, 2 for local "
                "business owners, 1 for a youth representative (16-24), "
                "and 1 for a partnering CDC."
            ),
            "pilot_parcels": (
                "Strawberry Mansion: 8 contiguous parcels along Ridge "
                "Avenue forming a community campus.  Kensington: 12 "
                "parcels along Frankford Avenue corridor.  Point Breeze: "
                "6 parcels clustered around the commercial strip on "
                "Point Breeze Avenue."
            ),
            "roi_analysis": (
                "Average community share raise of $75,000-$150,000 per "
                "cooperative covers acquisition and first-year activation.  "
                "Operating surplus begins in month 8-10.  Community "
                "dividend of $5-$15 per share begins in year 2.  Full "
                "return of initial community investment by year 5-7 "
                "through dividends plus appreciated parcel value."
            ),
            "beneficiaries": [
                "Neighborhood residents building collective wealth",
                "Local businesses gaining activated commercial frontage",
                "Youth gaining governance and entrepreneurship experience",
                "CDCs deepening community engagement",
                "Philadelphia Land Bank (parcels transferred to productive use)",
            ],
        },
        "tags": [
            "community-cooperatives",
            "community-shares",
            "local-ownership",
            "neighborhood-governance",
            "wealth-building",
        ],
    },

    # 5 — Sphere Futures Market
    {
        "title": "Sphere Futures Market",
        "summary": (
            "Tradeable activation rights — community groups, artists, and "
            "businesses can buy, sell, and trade future time slots on "
            "activated parcels.  Creates a liquid market for public space.  "
            "Revenue from a 2% transaction fee."
        ),
        "category": "financial-innovation",
        "impact_level": 4,
        "feasibility": 2,
        "novelty": 5,
        "time_horizon": "far",
        "status": "review",
        "details": {
            "revenue_model": (
                "Sphere operates the futures exchange and collects a 2% "
                "transaction fee on every trade of activation rights.  "
                "Rights are tokenized time slots (4-hour blocks) on "
                "specific parcels, purchasable up to 6 months in advance.  "
                "Secondary-market trading allows holders to resell slots "
                "they no longer need, creating price discovery for the "
                "true value of public-space access.  Additional revenue "
                "from a $49/year trader membership fee."
            ),
            "projected_annual_revenue": (
                "$400,000-$900,000/year at maturity.  Based on 200 "
                "parcels averaging 3 traded slots/day at $85 average "
                "slot value = $18.6M gross market volume, yielding "
                "$372K in transaction fees plus $200K in memberships."
            ),
            "ownership_structure": (
                "Sphere operates the exchange as a regulated marketplace.  "
                "Activation rights are issued by lot-holding organizations "
                "and sold into the primary market.  Lot holders receive "
                "100% of primary-sale proceeds.  Sphere earns only on "
                "secondary trades (2% fee) and memberships.  An "
                "independent market-integrity board oversees pricing "
                "fairness and anti-speculation rules."
            ),
            "pilot_parcels": (
                "Beta launch with 30 high-demand parcels in Center City "
                "fringe, Northern Liberties, and Fishtown — locations "
                "with proven demand for event and pop-up space.  Phase 2 "
                "expands to 100 parcels across North and West Philly."
            ),
            "roi_analysis": (
                "Platform development cost: $1.2M (smart-contract "
                "infrastructure, trading interface, compliance layer).  "
                "Break-even at approximately $600K annual transaction "
                "volume, achievable once 80 parcels are actively traded.  "
                "Full ROI in 2.5-3 years.  Key risk: regulatory "
                "classification of activation rights may require state "
                "securities exemption."
            ),
            "beneficiaries": [
                "Community groups securing future space at predictable prices",
                "Artists and cultural producers planning seasonal programs",
                "Small businesses locking in pop-up locations in advance",
                "Lot-holding organizations monetizing underused time slots",
                "City gaining transparent price data on public-space value",
            ],
        },
        "tags": [
            "sphere-futures",
            "tradeable-rights",
            "financial-innovation",
            "liquid-market",
            "activation-rights",
        ],
    },

    # 6 — Anchor Institution Model
    {
        "title": "Anchor Institution Model",
        "summary": (
            "Hospitals, universities, and large employers sponsor nearby lot "
            "activations as employee wellness and community benefit programs.  "
            "Penn Medicine sponsors 12 lots in West Philly, Temple sponsors "
            "8 in North Philly.  $50K/year per anchor."
        ),
        "category": "institutional-sponsorship",
        "impact_level": 4,
        "feasibility": 5,
        "novelty": 3,
        "time_horizon": "near",
        "status": "approved",
        "details": {
            "revenue_model": (
                "Each anchor institution pays $50,000/year for a Sphere "
                "sponsorship package covering activation of 8-15 lots "
                "within a half-mile radius of their campus.  Package "
                "includes branded wellness programming (outdoor yoga, "
                "walking paths, lunchtime green space), community health "
                "events, and employee volunteer coordination.  Sponsorship "
                "qualifies as community-benefit spending under IRS "
                "nonprofit hospital requirements and university PILOT "
                "agreements."
            ),
            "projected_annual_revenue": (
                "$500K/year with 10 anchor partners.  Initial pipeline: "
                "Penn Medicine ($50K — 12 lots, West Philly), Temple "
                "University ($50K — 8 lots, North Philly), Children's "
                "Hospital of Philadelphia ($50K — 6 lots, West Philly), "
                "Drexel University ($50K — 5 lots, Powelton Village), "
                "Jefferson Health ($50K — 7 lots, South Philly fringe)."
            ),
            "ownership_structure": (
                "Sphere manages activation operations under annual "
                "sponsorship contracts.  Land remains with the Land Bank "
                "or CDCs.  Anchor institutions receive naming rights, "
                "branding placement, and quarterly impact reports but hold "
                "no ownership stake in parcels.  Community programming "
                "decisions are made collaboratively with neighborhood "
                "advisory councils."
            ),
            "pilot_parcels": (
                "Penn Medicine cluster: 12 lots along Baltimore Avenue, "
                "Woodland Avenue, and around Clark Park in West Philly.  "
                "Temple cluster: 8 lots along Broad Street, Diamond "
                "Street, and Cecil B. Moore Avenue in North Philly."
            ),
            "roi_analysis": (
                "For anchor institutions: $50K/year is a fraction of "
                "typical community-benefit budgets ($5M+ for major "
                "hospitals).  Demonstrated ROI includes employee wellness "
                "improvements (12% reduction in reported stress in pilot "
                "studies), enhanced community relations, and quantifiable "
                "community-benefit reporting for IRS Schedule H.  For "
                "Sphere: 10 anchors at $50K = $500K in predictable "
                "annual revenue with minimal customer-acquisition cost."
            ),
            "beneficiaries": [
                "Anchor institution employees gaining outdoor wellness spaces",
                "Surrounding neighborhood residents accessing new green space",
                "Hospitals meeting IRS community-benefit requirements",
                "Universities strengthening town-gown relationships",
                "Sphere platform gaining stable institutional revenue",
            ],
        },
        "tags": [
            "anchor-institution",
            "sponsorship",
            "employee-wellness",
            "community-benefit",
            "institutional-partnership",
        ],
    },
]


# ---------------------------------------------------------------------------
# GENERATOR TEMPLATES (8)
# ---------------------------------------------------------------------------

TEMPLATES: list[dict] = [
    # T1 — Sphere Exchange variant generator
    {
        "title": "Sphere Exchange Configuration",
        "summary": (
            "Generates marketplace variants for the Sphere Exchange with "
            "adjustable pricing algorithms, parcel-type filters, and "
            "revenue-sharing structures for different neighborhood contexts."
        ),
        "category": "marketplace",
        "time_horizon": "near",
        "impact_range": [4, 5],
        "feasibility_range": [3, 5],
        "novelty_range": [4, 5],
        "details": {
            "revenue_model": (
                "Dynamic pricing with configurable base rates, surge "
                "multipliers, seasonal adjustments, and platform fee "
                "percentages."
            ),
            "pricing_variants": [
                "Demand-driven dynamic (real-time adjustment)",
                "Seasonal fixed (quarterly rate cards)",
                "Auction-based (highest-bidder for premium slots)",
                "Equity-adjusted (subsidized rates for community orgs)",
            ],
            "key_parameters": [
                "Base rate per hour per parcel type",
                "Surge multiplier ceiling",
                "Platform fee percentage (8-15%)",
                "Lot-holder revenue share",
                "Seasonal adjustment coefficients",
            ],
            "pilot_neighborhoods": [
                "North Philly",
                "Kensington",
                "Germantown",
            ],
        },
        "tags": [
            "sphere-exchange",
            "generator",
            "dynamic-pricing",
            "marketplace",
        ],
    },

    # T2 — Subscription Spheres variant generator
    {
        "title": "Subscription Spheres Tier Builder",
        "summary": (
            "Produces subscription-model variants with configurable tier "
            "structures, pricing ladders, corporate plan options, and "
            "geographic access scopes."
        ),
        "category": "subscription",
        "time_horizon": "medium",
        "impact_range": [3, 5],
        "feasibility_range": [3, 5],
        "novelty_range": [3, 4],
        "details": {
            "revenue_model": (
                "Tiered recurring subscriptions with configurable pricing, "
                "booking limits, and add-on infrastructure bundles."
            ),
            "tier_options": [
                "Basic (limited monthly bookings, self-service)",
                "Premium (expanded bookings, priority reservations)",
                "Unlimited (unrestricted access, same-day booking)",
                "Corporate (group plans, team-building packages)",
            ],
            "key_parameters": [
                "Monthly price per tier",
                "Booking limit per tier",
                "Corporate group discount rate",
                "Add-on bundle pricing",
                "Geographic scope (neighborhood / citywide / regional)",
            ],
            "pilot_neighborhoods": [
                "Citywide launch",
                "North Philly",
                "West Philly",
                "Kensington",
            ],
        },
        "tags": [
            "subscription-spheres",
            "generator",
            "tiered-access",
            "recurring-revenue",
        ],
    },

    # T3 — Reverse Spheres variant generator
    {
        "title": "Reverse Spheres Subsidy Model",
        "summary": (
            "Generates city-subsidy models with adjustable per-parcel "
            "payment rates, compliance frameworks, and blight-cost "
            "comparison baselines for different municipal contexts."
        ),
        "category": "public-subsidy",
        "time_horizon": "near",
        "impact_range": [4, 5],
        "feasibility_range": [4, 5],
        "novelty_range": [3, 5],
        "details": {
            "revenue_model": (
                "Municipal subsidy payments to activators calibrated "
                "against avoided blight-management costs; configurable "
                "payment frequency, compliance triggers, and performance "
                "bonuses."
            ),
            "subsidy_variants": [
                "Flat monthly per-parcel payment",
                "Outcome-tiered (higher pay for higher activation levels)",
                "Declining subsidy (full rate year 1, tapering to zero by year 5)",
                "Matched-funding (city matches community fundraising 1:1)",
            ],
            "key_parameters": [
                "Monthly subsidy rate per parcel",
                "Blight-cost baseline for ROI calculation",
                "Compliance inspection frequency",
                "Performance bonus triggers",
                "Subsidy duration and taper schedule",
            ],
            "pilot_neighborhoods": [
                "North Philly",
                "Kensington",
                "Strawberry Mansion",
                "Nicetown-Tioga",
            ],
        },
        "tags": [
            "reverse-spheres",
            "generator",
            "city-subsidy",
            "blight-reduction",
        ],
    },

    # T4 — Community Cooperative variant generator
    {
        "title": "Community Cooperative Formation Kit",
        "summary": (
            "Produces cooperative-ownership models customized to different "
            "neighborhood scales, share-pricing structures, governance "
            "configurations, and community wealth-building goals."
        ),
        "category": "cooperative-ownership",
        "time_horizon": "medium",
        "impact_range": [4, 5],
        "feasibility_range": [2, 4],
        "novelty_range": [3, 5],
        "details": {
            "revenue_model": (
                "Community share raises plus ongoing earned revenue from "
                "space rentals, vendor leases, and programming fees; "
                "configurable dividend and reinvestment ratios."
            ),
            "governance_options": [
                "Resident-majority board (5 of 7 seats)",
                "Balanced stakeholder board (residents, businesses, CDC)",
                "Youth-led board (majority under-30 seats)",
                "Rotating leadership (annual board turnover by lottery)",
            ],
            "key_parameters": [
                "Share price range (minimum and maximum)",
                "Number of parcels per cooperative",
                "Board composition and term lengths",
                "Revenue allocation split (maintenance / dividend / acquisition)",
                "Community share raise target",
            ],
            "pilot_neighborhoods": [
                "Strawberry Mansion",
                "Kensington",
                "Point Breeze",
            ],
        },
        "tags": [
            "community-cooperatives",
            "generator",
            "community-shares",
            "governance",
        ],
    },

    # T5 — Sphere Futures Market variant generator
    {
        "title": "Sphere Futures Market Design",
        "summary": (
            "Generates tradeable-rights market configurations with "
            "adjustable time-slot granularity, transaction fee structures, "
            "anti-speculation safeguards, and regulatory compliance models."
        ),
        "category": "financial-innovation",
        "time_horizon": "far",
        "impact_range": [3, 5],
        "feasibility_range": [1, 3],
        "novelty_range": [4, 5],
        "details": {
            "revenue_model": (
                "Transaction fees on secondary trades plus annual trader "
                "memberships; configurable fee rates and membership tiers."
            ),
            "market_variants": [
                "Open exchange (unrestricted secondary trading)",
                "Community-first (preferential pricing for neighborhood orgs)",
                "Capped-gain (maximum resale price to prevent speculation)",
                "Seasonal futures (quarterly rights packages only)",
            ],
            "key_parameters": [
                "Time-slot granularity (2-hour, 4-hour, full-day)",
                "Transaction fee percentage (1-5%)",
                "Forward booking horizon (3, 6, or 12 months)",
                "Anti-speculation price cap",
                "Trader membership fee and tier structure",
            ],
            "pilot_neighborhoods": [
                "Center City fringe",
                "Northern Liberties",
                "Fishtown",
                "North Philly",
            ],
        },
        "tags": [
            "sphere-futures",
            "generator",
            "tradeable-rights",
            "market-design",
        ],
    },

    # T6 — Anchor Institution variant generator
    {
        "title": "Anchor Institution Sponsorship Package",
        "summary": (
            "Produces sponsorship-package variants for hospitals, "
            "universities, and employers with configurable lot counts, "
            "programming menus, branding options, and community-benefit "
            "reporting frameworks."
        ),
        "category": "institutional-sponsorship",
        "time_horizon": "near",
        "impact_range": [3, 5],
        "feasibility_range": [4, 5],
        "novelty_range": [2, 4],
        "details": {
            "revenue_model": (
                "Annual sponsorship contracts with configurable package "
                "size, programming scope, and community-benefit tie-ins."
            ),
            "sponsor_type_options": [
                "Hospital / health system (wellness + community benefit)",
                "University (student engagement + town-gown relations)",
                "Large employer (employee wellness + recruitment branding)",
                "Philanthropy / foundation (impact investment + visibility)",
            ],
            "key_parameters": [
                "Annual sponsorship fee",
                "Number of lots per sponsorship",
                "Radius from anchor campus",
                "Programming menu (wellness, arts, education, food)",
                "Branding and naming-rights scope",
                "Impact-reporting cadence and metrics",
            ],
            "pilot_neighborhoods": [
                "West Philly (Penn Medicine, CHOP)",
                "North Philly (Temple University)",
                "University City (Drexel University)",
            ],
        },
        "tags": [
            "anchor-institution",
            "generator",
            "sponsorship",
            "community-benefit",
        ],
    },

    # T7 — Blended Sphere revenue model generator
    {
        "title": "Blended Sphere Revenue Model",
        "summary": (
            "Generates hybrid business models that combine two or more "
            "Sphere revenue streams — exchange fees, subscriptions, city "
            "subsidies, co-op shares, and anchor sponsorships — into "
            "unified financial plans for specific neighborhoods."
        ),
        "category": "hybrid-finance",
        "time_horizon": "medium",
        "impact_range": [4, 5],
        "feasibility_range": [2, 4],
        "novelty_range": [4, 5],
        "details": {
            "revenue_model": (
                "Stacked revenue from multiple Sphere models weighted "
                "by neighborhood characteristics; configurable blend "
                "ratios and financial projection horizons."
            ),
            "blend_options": [
                "Exchange + Subscription (marketplace with membership layer)",
                "Reverse Spheres + Cooperative (subsidy bootstraps co-op)",
                "Anchor + Exchange (institutional floor + market upside)",
                "Full stack (all five models in a single neighborhood)",
            ],
            "key_parameters": [
                "Revenue-stream weight allocation",
                "Neighborhood demographic profile inputs",
                "Parcel inventory and typology mix",
                "3-year and 5-year financial projection horizon",
                "Risk-adjusted return targets",
            ],
            "pilot_neighborhoods": [
                "Strawberry Mansion",
                "Kensington",
                "North Broad corridor",
            ],
        },
        "tags": [
            "blended-model",
            "generator",
            "hybrid-finance",
            "revenue-stacking",
        ],
    },

    # T8 — Sphere Expansion Playbook generator
    {
        "title": "Sphere Expansion Playbook",
        "summary": (
            "Generates city-replication playbooks that adapt the Sphere "
            "business model portfolio to other cities with large vacant-lot "
            "inventories — Detroit, Baltimore, St. Louis, Cleveland — with "
            "localized financial projections and regulatory mapping."
        ),
        "category": "replication",
        "time_horizon": "far",
        "impact_range": [4, 5],
        "feasibility_range": [2, 4],
        "novelty_range": [3, 5],
        "details": {
            "revenue_model": (
                "Licensing fee for the Sphere platform and playbook; "
                "configurable per-city pricing based on lot inventory "
                "size and local economic conditions."
            ),
            "expansion_city_options": [
                "Detroit (150,000+ vacant lots — massive scale opportunity)",
                "Baltimore (17,000 vacant lots — strong CDC infrastructure)",
                "St. Louis (25,000 vacant lots — land-bank partnership ready)",
                "Cleveland (27,000 vacant lots — municipal innovation culture)",
            ],
            "key_parameters": [
                "Target city vacant-lot inventory size",
                "Local regulatory and zoning framework",
                "Existing community development infrastructure",
                "Municipal blight-management budget baseline",
                "Licensing fee and revenue-share structure",
                "Launch timeline and milestone targets",
            ],
            "pilot_neighborhoods": [
                "Detroit — Brightmoor and Grandmont-Rosedale",
                "Baltimore — Sandtown-Winchester and Harlem Park",
                "St. Louis — Old North and Dutchtown",
            ],
        },
        "tags": [
            "expansion-playbook",
            "generator",
            "city-replication",
            "licensing",
            "national-scale",
        ],
    },
]
