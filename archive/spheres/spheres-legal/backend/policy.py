"""
policy.py — Legislative models, comparative analysis, and equity framework
for public space activation.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional


# ---------------------------------------------------------------------------
# Model Legislation
# ---------------------------------------------------------------------------

MODEL_LEGISLATION = [
    {
        "id": "spheres_act",
        "title": "THE SPHERES ACT — Space, Heritage, and Public Resource Equity for Streets",
        "type": "municipal_ordinance",
        "summary": (
            "A comprehensive municipal ordinance establishing a streamlined "
            "permitting pathway for activating publicly-owned dormant space in "
            "Philadelphia. Creates a single-application portal, equity-weighted "
            "priority scoring, permanence requirements, and community input "
            "safeguards. Designed to reduce the average activation timeline "
            "from 120+ days to under 45."
        ),
        "full_text": (
            "AN ORDINANCE\n"
            "Amending Title 10 (Regulation of Individual Conduct and Activity) "
            "of The Philadelphia Code by adding a new Chapter 10-900, entitled "
            "'Space Activation and Public Resource Equity,' to establish a "
            "streamlined framework for the temporary and permanent activation "
            "of publicly-owned dormant space.\n\n"
            "THE COUNCIL OF THE CITY OF PHILADELPHIA HEREBY ORDAINS:\n\n"
            "SECTION 1. Title 10 of The Philadelphia Code is hereby amended by "
            "adding a new Chapter 10-900, to read as follows:\n\n"
            "CHAPTER 10-900. SPACE ACTIVATION AND PUBLIC RESOURCE EQUITY\n\n"
            "§ 10-901. Definitions.\n"
            "(a) 'Dormant Public Space' shall mean any parcel of land owned by "
            "the City of Philadelphia, the Philadelphia Land Bank, the "
            "Redevelopment Authority, or any City-affiliated entity that has "
            "been vacant, underutilized, or without a designated active use "
            "for a period of twelve (12) consecutive months or more.\n"
            "(b) 'Activation' shall mean any lawful temporary or permanent use "
            "of Dormant Public Space that creates public benefit, including "
            "but not limited to: community gathering, cultural programming, "
            "urban agriculture, public art, markets, recreation, or "
            "commercial activity with community benefit requirements.\n"
            "(c) 'Activator' shall mean any natural person, nonprofit "
            "organization, community development corporation, business "
            "improvement district, or registered business entity proposing "
            "an Activation.\n"
            "(d) 'Permanence Value' shall mean any lasting physical, social, "
            "economic, or environmental improvement resulting from an "
            "Activation that endures beyond the Activation period.\n\n"
            "§ 10-902. Space Activation Office.\n"
            "There is hereby established within the Managing Director's Office "
            "a Space Activation Office ('SAO') responsible for:\n"
            "(a) Maintaining an inventory of all Dormant Public Space;\n"
            "(b) Operating a single-application portal for Activation permits;\n"
            "(c) Coordinating inter-agency review within 30 calendar days;\n"
            "(d) Administering equity-weighted priority scoring;\n"
            "(e) Monitoring Permanence Value compliance.\n\n"
            "§ 10-903. Unified Application Process.\n"
            "(a) Any Activator may submit a single application to the SAO "
            "for Activation of any Dormant Public Space.\n"
            "(b) The SAO shall, within five (5) business days, identify all "
            "required permits and route the application to relevant agencies.\n"
            "(c) All agencies shall complete review within thirty (30) "
            "calendar days of receipt.\n"
            "(d) If an agency fails to respond within thirty (30) days, "
            "the application shall be deemed approved by that agency.\n\n"
            "§ 10-904. Equity-Weighted Priority Scoring.\n"
            "(a) Applications shall be scored using the following criteria:\n"
            "  (1) Neighborhood dormant space density (25%)\n"
            "  (2) Inverse median household income (20%)\n"
            "  (3) Inverse activation history (20%)\n"
            "  (4) Community organization support (15%)\n"
            "  (5) Health outcome gaps (20%)\n"
            "(b) Applications from neighborhoods scoring in the top quartile "
            "shall receive expedited review (15 calendar days).\n\n"
            "§ 10-905. Permanence Requirements.\n"
            "(a) Every Activation of sixty (60) days or longer shall include "
            "a Permanence Plan demonstrating that at least twenty-five percent "
            "(25%) of the Activation's value will remain as permanent "
            "community benefit.\n"
            "(b) Permanence Value categories include: physical improvements, "
            "community assets, knowledge transfer, economic legacy, and "
            "environmental improvement.\n\n"
            "§ 10-906. Community Input.\n"
            "(a) The SAO shall notify the relevant Registered Community "
            "Organization (RCO) within three (3) business days of receiving "
            "an application.\n"
            "(b) The RCO shall have fifteen (15) calendar days to provide "
            "comment.\n"
            "(c) Community comment shall be advisory, not binding, but the "
            "SAO shall respond in writing to all substantive concerns.\n\n"
            "§ 10-907. Insurance and Liability.\n"
            "(a) The SAO shall establish a Pooled Liability Fund for "
            "Activations in high-priority neighborhoods.\n"
            "(b) Small-scale Activations (under $5,000 in estimated cost "
            "and under 100 attendees) may utilize the Pooled Liability Fund "
            "in lieu of individual insurance policies.\n\n"
            "§ 10-908. Effective Date.\n"
            "This Ordinance shall take effect one hundred twenty (120) days "
            "after enactment."
        ),
        "key_provisions": [
            "Single-application portal for all space activation permits",
            "30-day inter-agency review deadline with deemed-approved provision",
            "Equity-weighted priority scoring based on 5 neighborhood criteria",
            "Expedited 15-day review for highest-need neighborhoods",
            "25% permanence value requirement for activations over 60 days",
            "Pooled liability fund for small-scale activations in high-priority areas",
            "Space Activation Office within the Managing Director's Office",
        ],
        "equity_requirements": [
            "Neighborhood dormant space density weighted at 25%",
            "Inverse median household income weighted at 20%",
            "Communities with least activation history receive highest scores",
            "Health outcome gaps factored at 20% of priority score",
            "Top-quartile neighborhoods receive expedited review",
        ],
        "permanence_requirements": (
            "Every activation of 60+ days must include a Permanence Plan "
            "demonstrating that at least 25% of value remains as permanent "
            "community benefit across five categories: physical improvements, "
            "community assets, knowledge transfer, economic legacy, and "
            "environmental improvement."
        ),
        "community_input_process": (
            "RCO notified within 3 business days. 15-day comment window. "
            "Community comment is advisory but SAO must respond in writing "
            "to all substantive concerns."
        ),
        "implementation_timeline": (
            "120 days after enactment. SAO established within 60 days. "
            "Portal operational within 90 days. Full implementation by day 120."
        ),
        "strategy_memo": (
            "INTRODUCTION STRATEGY: Introduce through the Committee on "
            "Streets and Services (Chair: Council Member), with co-sponsorship "
            "from at least 5 Council members representing high-vacancy districts. "
            "Build coalition of: Philadelphia Land Bank, PHS, community garden "
            "networks, food justice orgs, arts organizations, and BIDs. "
            "Key timing: introduce in Q1 when Council agenda is lighter. "
            "Pre-file a resolution supporting the concept 60 days before "
            "introducing the bill to gauge support. Engage the Managing "
            "Director's Office early — they will house the SAO."
        ),
        "talking_points": [
            "Philadelphia has 40,000+ publicly-owned vacant parcels — more than any city this size. The current permitting process takes 90-120 days and requires navigating 5+ agencies. This ordinance cuts that to 30 days through one portal.",
            "The SPHERES Act doesn't create new bureaucracy — it coordinates existing agencies through a single office. The SAO is 3-5 staff within the Managing Director's Office.",
            "Equity isn't optional. The neighborhoods with the most dormant space are the same neighborhoods with the least investment. This ordinance ensures they get first priority.",
            "The 25% permanence requirement means every activation leaves something behind. Not just a weekend event, but a permanent bench, a mural, a community garden bed, a trained workforce.",
            "The pooled liability fund eliminates the #1 barrier for small activators: the $500-$2,000 cost of individual insurance policies. For $75-$150, community groups get $1M in coverage.",
            "Every comparable city that has streamlined space activation has seen economic returns of 5-10x the program cost. NYC's Plaza Program generated $1.4B in adjacent property value.",
        ],
        "fiscal_impact": (
            "ESTIMATED ANNUAL COST: $450,000-$650,000 (SAO staffing: $350K, "
            "technology/portal: $50K, pooled liability fund capitalization: "
            "$500K one-time). ESTIMATED ANNUAL REVENUE: $200K-$400K in permit "
            "fees, plus indirect tax revenue from activated spaces. NET: "
            "Self-sustaining within 3 years. ROI: Conservative estimate of "
            "$5M-$15M in economic activity from 200-500 new activations per year."
        ),
        "comparable_cities": [
            "NYC Plaza Program — $4M annual budget, 80+ plazas, $1.4B in adjacent property value increase",
            "Barcelona Pla Buits — activated 30+ vacant lots in first 2 years at minimal cost",
            "London Meanwhile Use — standardized lease templates reduced legal costs 80%",
            "Detroit Land Bank — 30,000+ lots transferred, $500M in neighborhood investment",
        ],
    },
    {
        "id": "state_enabling",
        "title": "Space Activation Districts Enabling Act",
        "type": "state_legislation",
        "summary": (
            "Model state legislation authorizing Pennsylvania municipalities "
            "to create Space Activation Districts (SADs) — designated areas "
            "where streamlined permitting, tax incentives, and liability "
            "protections encourage the activation of dormant public space."
        ),
        "full_text": (
            "AN ACT\n"
            "Amending Title 53 (Municipalities Generally) of the Pennsylvania "
            "Consolidated Statutes, by adding Chapter 59, entitled 'Space "
            "Activation Districts.'\n\n"
            "THE GENERAL ASSEMBLY OF THE COMMONWEALTH OF PENNSYLVANIA "
            "HEREBY ENACTS AS FOLLOWS:\n\n"
            "Section 1. Title 53 of the Pennsylvania Consolidated Statutes "
            "is amended by adding a chapter to read:\n\n"
            "CHAPTER 59. SPACE ACTIVATION DISTRICTS\n\n"
            "§ 5901. Authorization.\n"
            "Any municipality of the first class, second class, second class A, "
            "or third class may, by ordinance, establish one or more Space "
            "Activation Districts within its boundaries.\n\n"
            "§ 5902. District Designation.\n"
            "(a) A Space Activation District may be established in any area "
            "where:\n"
            "  (1) At least 20% of publicly-owned parcels have been dormant "
            "for 12 or more months; or\n"
            "  (2) The median household income is below 80% of the area "
            "median income; or\n"
            "  (3) The municipality determines there is a demonstrated "
            "need for increased public space activation.\n\n"
            "§ 5903. District Benefits.\n"
            "Within a Space Activation District, the following shall apply:\n"
            "(a) Permit processing times shall not exceed 21 calendar days;\n"
            "(b) Permit fees shall be reduced by 50% for nonprofit and "
            "community-based Activators;\n"
            "(c) Property tax exemptions shall be available for permanently "
            "activated parcels for up to 10 years;\n"
            "(d) The municipality may establish a pooled liability fund;\n"
            "(e) Activators may access municipal technical assistance.\n\n"
            "§ 5904. Anti-Displacement Protections.\n"
            "No Space Activation District may be established or maintained "
            "without:\n"
            "(a) A community engagement process including at least two public "
            "hearings;\n"
            "(b) An anti-displacement impact assessment;\n"
            "(c) Community benefit agreement requirements for commercial "
            "activations exceeding $50,000 in annual revenue.\n\n"
            "§ 5905. Reporting.\n"
            "Each municipality with an active Space Activation District shall "
            "submit an annual report to the Department of Community and "
            "Economic Development including activation counts, economic "
            "impact, equity metrics, and community feedback.\n\n"
            "Section 2. This act shall take effect in 60 days."
        ),
        "key_provisions": [
            "Authorizes municipalities to create Space Activation Districts",
            "21-day maximum permit processing within SADs",
            "50% fee reduction for nonprofit and community Activators",
            "10-year property tax exemption for permanently activated parcels",
            "Municipal pooled liability fund authorization",
            "Technical assistance for Activators",
            "Annual reporting to DCED on equity metrics",
        ],
        "equity_requirements": [
            "Districts targeted at areas with 20%+ dormant parcels or below-80% AMI",
            "Two public hearings required before district establishment",
            "Anti-displacement impact assessment mandatory",
            "Community benefit agreements for commercial activations over $50K",
        ],
        "permanence_requirements": (
            "10-year property tax exemption incentivizes permanent activation. "
            "Municipalities may require permanence plans as condition of "
            "district benefits."
        ),
        "community_input_process": (
            "Minimum two public hearings before district establishment. "
            "Annual community feedback incorporated into DCED reporting."
        ),
        "implementation_timeline": (
            "60 days after enactment. Municipalities may begin designating "
            "districts immediately upon effective date."
        ),
        "strategy_memo": (
            "INTRODUCTION STRATEGY: Requires state-level advocacy through "
            "the Philadelphia delegation in Harrisburg. Build a coalition of "
            "Pennsylvania municipalities (Pittsburgh, Allentown, Reading, Erie) "
            "that share vacancy challenges. Frame as local control legislation — "
            "municipalities are *requesting* the authority, not being mandated. "
            "Introduce through the Urban Affairs Committee. Engage DCED as a "
            "partner — they benefit from better data and outcomes. "
            "Key champion: a Philadelphia state senator with urban policy credentials."
        ),
        "talking_points": [
            "Pennsylvania municipalities currently lack explicit authority to create streamlined space activation zones. This bill gives them the tool — it doesn't mandate anything.",
            "Space Activation Districts are the economic development zones of the 21st century. Instead of attracting corporations with tax breaks, they activate community assets with reduced barriers.",
            "Every municipality that wants to use this will have to hold public hearings and conduct anti-displacement assessments. This is enabling legislation with built-in safeguards.",
            "The 50% fee reduction for nonprofits costs municipalities almost nothing — these are fees that aren't being collected anyway because the spaces aren't being activated.",
            "Annual DCED reporting creates the first statewide dataset on public space activation — valuable for policy research and federal grant applications.",
        ],
        "fiscal_impact": (
            "ESTIMATED STATE COST: Minimal — DCED reporting infrastructure ~$75K "
            "one-time. MUNICIPAL COST: Varies by municipality. For Philadelphia: "
            "estimated $200K-$400K annually for SAD administration, offset by "
            "increased permit revenue and property tax gains in activated areas. "
            "10-year property tax exemption cost offset by 3-5x increase in "
            "surrounding property values."
        ),
        "comparable_cities": [
            "New York State — Empire State Development zones provide model for district-based activation incentives",
            "Michigan — Land Bank Fast Track Authority enables streamlined property disposition",
            "Oregon — Portland's inclusionary zoning enabling legislation demonstrates state-local partnership",
            "Colorado — Creative Districts Act authorizes municipal arts and culture zones with tax benefits",
        ],
    },
    {
        "id": "right_to_activate",
        "title": "RIGHT TO ACTIVATE — Community Activation Petition Act",
        "type": "municipal_ordinance",
        "summary": (
            "Model ordinance establishing the right of Philadelphia residents "
            "to petition for the activation of dormant public parcels. If a "
            "qualifying parcel has been dormant for 18+ months, residents may "
            "submit an Activation Petition. The city must respond with an "
            "approval, alternative plan, or written denial within 90 days."
        ),
        "full_text": (
            "AN ORDINANCE\n"
            "Amending Title 10 of The Philadelphia Code by adding Chapter "
            "10-950, entitled 'Right to Activate.'\n\n"
            "THE COUNCIL OF THE CITY OF PHILADELPHIA HEREBY ORDAINS:\n\n"
            "CHAPTER 10-950. RIGHT TO ACTIVATE\n\n"
            "§ 10-951. Right to Petition.\n"
            "(a) Any group of ten (10) or more residents of a Philadelphia "
            "ZIP code may submit an Activation Petition to the Space "
            "Activation Office for any Dormant Public Space within their "
            "ZIP code that has been dormant for eighteen (18) or more "
            "consecutive months.\n"
            "(b) The Petition shall include: a description of the proposed "
            "Activation, evidence of dormancy, a community support statement "
            "with at least 25 signatures, and a preliminary site plan.\n\n"
            "§ 10-952. City Response.\n"
            "(a) Within ninety (90) days of receiving a valid Petition, "
            "the City shall:\n"
            "  (1) Approve the proposed Activation and issue permits; or\n"
            "  (2) Propose an alternative Activation plan for the parcel; or\n"
            "  (3) Issue a written denial with specific findings of fact.\n"
            "(b) Denial may only be based on:\n"
            "  (1) Documented public safety hazard that cannot be mitigated;\n"
            "  (2) Binding legal obligation preventing the proposed use;\n"
            "  (3) Active development plan with committed funding and a "
            "construction start date within 24 months.\n\n"
            "§ 10-953. Default Approval.\n"
            "If the City fails to respond within ninety (90) days, the "
            "Petition shall be deemed approved, and the SAO shall issue "
            "necessary permits within fifteen (15) additional days.\n\n"
            "§ 10-954. Community Stewardship.\n"
            "(a) Approved Petitioners shall form a Community Stewardship "
            "Committee responsible for ongoing management.\n"
            "(b) The Committee shall submit semi-annual reports on "
            "activation status, community benefit, and maintenance.\n\n"
            "§ 10-955. Permanence Pathway.\n"
            "After three (3) years of continuous activation, the Community "
            "Stewardship Committee may petition for permanent transfer of "
            "the parcel to a community land trust or nonprofit entity at "
            "nominal cost."
        ),
        "key_provisions": [
            "10 residents can petition for activation of any 18-month dormant parcel",
            "90-day city response deadline with deemed-approved default",
            "Denial limited to 3 specific grounds (safety, legal obligation, active development)",
            "Community Stewardship Committee required for approved activations",
            "Permanence pathway: after 3 years, parcel can transfer to community land trust",
            "25-signature community support requirement",
        ],
        "equity_requirements": [
            "ZIP-code-based petitioning ensures neighborhood-level access",
            "No fee for filing an Activation Petition",
            "SAO must provide technical assistance to Petitioners upon request",
            "Permanence pathway prioritizes community ownership over disposition",
        ],
        "permanence_requirements": (
            "After 3 years of continuous activation, Community Stewardship "
            "Committee may petition for permanent transfer to a community "
            "land trust or nonprofit at nominal cost."
        ),
        "community_input_process": (
            "Petition requires 25 community signatures. Community Stewardship "
            "Committee formed for ongoing management. Semi-annual reporting "
            "on community benefit."
        ),
        "implementation_timeline": (
            "Effective 90 days after enactment. SAO begins accepting "
            "Petitions on day 91."
        ),
        "strategy_memo": (
            "INTRODUCTION STRATEGY: Frame as a community empowerment measure, "
            "not an anti-government measure. The city retains authority to deny — "
            "but must give a reason. Key allies: community land trusts (especially "
            "the Philadelphia CLT), neighborhood advisory committees, RCOs, "
            "urban farmers, and community garden networks. Introduce alongside "
            "the SPHERES Act as a companion ordinance. The SPHERES Act streamlines "
            "city-initiated activation; Right to Activate enables resident-initiated "
            "activation. Together they create a complete framework."
        ),
        "talking_points": [
            "If a publicly-owned lot has been empty for 18 months, residents should be able to ask: 'Can we use this?' Right now, there's no formal way to do that. This creates one.",
            "The city can still say no — but only for three specific reasons: safety hazard, legal obligation, or active development plan. 'We haven't gotten around to it' is not a valid denial.",
            "The 90-day response deadline with deemed-approved default ensures the city actually responds. Right now, community requests disappear into bureaucratic limbo.",
            "The permanence pathway after 3 years means community gardens, gathering spaces, and neighborhood assets can become permanent through community land trusts.",
            "This costs the city nothing. No new staff, no new budget. It's a process reform that uses existing SAO infrastructure from the SPHERES Act.",
        ],
        "fiscal_impact": (
            "ESTIMATED COST: $0 incremental if SPHERES Act SAO is already "
            "established. Petition processing handled by existing SAO staff. "
            "POTENTIAL SAVINGS: Reduces Land Bank maintenance costs on activated "
            "parcels ($2,000-$5,000/year per parcel in mowing, boarding, "
            "trash removal). If 100 parcels activated: $200K-$500K annual "
            "maintenance savings."
        ),
        "comparable_cities": [
            "Detroit Side Lot Program — residents can acquire adjacent vacant lots for $100, 30,000+ transferred",
            "Baltimore Adopt-a-Lot — residents maintain vacant lots in exchange for use rights",
            "Cleveland Land Bank — community groups can lease vacant lots for $1/year for garden use",
            "Pittsburgh PULSE — vacant lot activation program with 5-year community stewardship agreements",
        ],
    },
    {
        "id": "pooled_liability",
        "title": "POOLED LIABILITY ACT — Shared Insurance for Space Activation",
        "type": "municipal_ordinance",
        "summary": (
            "Creates a city-administered pooled liability insurance program "
            "for public space activations, reducing the #1 barrier for small "
            "activators: the cost and complexity of obtaining individual "
            "liability coverage. The pool is funded by a modest per-activation "
            "fee and supplemented by city appropriation."
        ),
        "full_text": (
            "AN ORDINANCE\n"
            "Amending Title 10 of The Philadelphia Code by adding Chapter "
            "10-960, entitled 'Pooled Liability for Space Activation.'\n\n"
            "THE COUNCIL OF THE CITY OF PHILADELPHIA HEREBY ORDAINS:\n\n"
            "CHAPTER 10-960. POOLED LIABILITY FOR SPACE ACTIVATION\n\n"
            "§ 10-961. Establishment.\n"
            "There is hereby established the Philadelphia Space Activation "
            "Liability Pool ('the Pool'), administered by the SAO in "
            "coordination with the City's Risk Management Division.\n\n"
            "§ 10-962. Eligibility.\n"
            "(a) The Pool shall be available to Activators meeting all of "
            "the following criteria:\n"
            "  (1) Activation budget under $10,000;\n"
            "  (2) Expected attendance under 500 persons;\n"
            "  (3) Duration of 30 days or fewer per activation;\n"
            "  (4) No alcohol service (separate license required);\n"
            "  (5) Activator has completed SAO safety orientation.\n\n"
            "§ 10-963. Coverage.\n"
            "(a) The Pool provides:\n"
            "  (1) General liability: $1,000,000 per occurrence / "
            "$2,000,000 aggregate;\n"
            "  (2) City of Philadelphia named as additional insured;\n"
            "  (3) Property damage: $500,000 per occurrence.\n"
            "(b) The Pool does not cover:\n"
            "  (1) Liquor liability;\n"
            "  (2) Professional liability;\n"
            "  (3) Workers' compensation;\n"
            "  (4) Vehicular liability.\n\n"
            "§ 10-964. Funding.\n"
            "(a) Per-activation fee: $75 for activations under $2,500 budget; "
            "$150 for activations $2,500-$10,000.\n"
            "(b) Annual City appropriation of $500,000 to capitalize the Pool.\n"
            "(c) The Pool shall maintain reserves of at least $2,000,000.\n\n"
            "§ 10-965. Claims.\n"
            "Claims against the Pool shall be administered by the City's "
            "Risk Management Division following standard municipal claims "
            "procedures.\n\n"
            "§ 10-966. Reporting.\n"
            "The SAO shall publish quarterly reports on Pool utilization, "
            "claims history, reserve levels, and demographic data on "
            "Pool participants."
        ),
        "key_provisions": [
            "City-administered pooled liability insurance for small activations",
            "$1M/$2M general liability coverage through the Pool",
            "Activation fee of $75-$150 replaces $500-$2,000 individual policies",
            "$500,000 annual city appropriation to capitalize the Pool",
            "Eligibility: under $10K budget, under 500 attendees, under 30 days",
            "SAO safety orientation required for Pool access",
            "Quarterly transparency reporting on Pool finances",
        ],
        "equity_requirements": [
            "Fee structure progressive: lower fee for smaller activations",
            "Pool specifically targets cost barrier that disproportionately affects low-income activators",
            "Safety orientation offered free and in multiple languages",
            "Demographic data collected and published quarterly",
        ],
        "permanence_requirements": (
            "Pool participants must agree to permanence requirements of "
            "the SPHERES Act if their activation exceeds 60 days."
        ),
        "community_input_process": (
            "Quarterly public reporting. Annual public hearing on Pool "
            "performance and proposed fee adjustments."
        ),
        "implementation_timeline": (
            "Pool capitalized within 90 days. First policies available "
            "within 120 days of enactment. Safety orientation program "
            "developed within 60 days."
        ),
        "strategy_memo": (
            "INTRODUCTION STRATEGY: This is the easiest of the four to pass "
            "because it solves a concrete problem everyone agrees on: insurance "
            "is too expensive for small community activations. Introduce as a "
            "standalone ordinance or as part of the SPHERES Act package. "
            "Key allies: Risk Management Division (they understand pooled risk), "
            "insurance industry (they don't want to underwrite $500 policies), "
            "and community organizations (they've been asking for this). "
            "Frame as innovation, not spending: the $500K capitalization is an "
            "investment that generates returns through activation."
        ),
        "talking_points": [
            "A neighborhood group that wants to host a weekend movie night in a vacant lot needs $1,000,000 in liability insurance. That policy costs $500-$2,000. For a movie night. The pooled fund makes it $75.",
            "The Pool doesn't increase the city's risk — it manages risk that's already happening. Community events are occurring without insurance because the cost is prohibitive. The Pool brings them into a managed framework.",
            "At $75-$150 per activation, the Pool is self-sustaining after year 2. The $500K capitalization is a one-time investment that generates perpetual coverage.",
            "Quarterly reporting means full transparency. Every dollar in, every claim out, every demographic data point — all public.",
            "The safety orientation requirement isn't bureaucratic burden — it's risk management. 30 minutes online, available in 6 languages, and it reduces claims by an estimated 40%.",
        ],
        "fiscal_impact": (
            "CAPITALIZATION: $500,000 one-time appropriation. ANNUAL OPERATING "
            "COST: $50K (administration, claims processing within Risk Management). "
            "ANNUAL REVENUE: $15K-$50K in per-activation fees (200-500 activations "
            "at $75-$150). BREAK-EVEN: Year 2-3, assuming average claims of "
            "$100K/year (based on comparable municipal risk pools). NET SAVINGS: "
            "Reduced uninsured incident liability exposure for the city."
        ),
        "comparable_cities": [
            "San Francisco Shared Spaces Program — city-provided insurance for sidewalk and street activations during COVID, continued permanently",
            "Minneapolis Park Board — pooled liability for community events in parks, $50/event fee",
            "Austin Special Events — graduated insurance requirements based on event size, city-facilitated pool for small events",
            "Toronto Community Activations — city self-insures small community events under its municipal policy",
        ],
    },
]


# ---------------------------------------------------------------------------
# Comparative Analysis
# ---------------------------------------------------------------------------

COMPARATIVE_ANALYSIS = [
    {
        "name": "Philadelphia",
        "country": "United States",
        "population": 1_603_797,
        "approach_name": "Fragmented Multi-Agency System",
        "description": (
            "Philadelphia's public space activation requires navigating "
            "multiple city agencies with no centralized portal. Permits are "
            "handled separately by Parks & Recreation, Streets Department, "
            "L&I, Commerce, and the Managing Director's Office. The process "
            "is slow, opaque, and particularly burdensome for small and "
            "community-based activators."
        ),
        "key_policies": [
            "Special Event Permit (Managing Director's Office)",
            "Park Use Permit (Parks & Recreation)",
            "Temporary Use License (Land Bank)",
            "Philadelphia Land Bank Strategic Plan",
            "Rebuild initiative (park improvements)",
        ],
        "strengths": [
            "Large inventory of publicly-owned vacant land (over 40,000 parcels)",
            "Strong community garden movement through PHS",
            "Philadelphia Land Bank consolidates city-owned property",
            "Rebuild program investing $500M in parks and recreation",
            "Active RCO network provides community input infrastructure",
        ],
        "weaknesses": [
            "No centralized permitting portal for space activation",
            "Average timeline of 90-120 days for complex activations",
            "High insurance requirements ($1M GL) with no pooled alternative",
            "No equity framework for prioritizing underserved neighborhoods",
            "Dormant parcels lack systematic tracking or reporting",
        ],
        "lessons_for_philadelphia": [
            "Create a single-application portal (the SPHERES Act proposes this)",
            "Establish a pooled liability fund to reduce insurance barriers",
            "Implement equity-weighted priority scoring for permit review",
            "Set binding response deadlines with deemed-approved defaults",
        ],
        "activation_score": 38,
        "notable_projects": [
            {
                "name": "The Rail Park",
                "description": "Elevated rail viaduct converted into public green space in Callowhill.",
                "outcome": "Phase 1 opened 2018. Catalyst for neighborhood revitalization.",
            },
            {
                "name": "PHS Pop-Up Gardens",
                "description": "Pennsylvania Horticultural Society converts vacant lots into seasonal beer gardens and community spaces.",
                "outcome": "40+ lots activated. Model for temporary-to-permanent transformation.",
            },
        ],
    },
    {
        "name": "New York City",
        "country": "United States",
        "population": 8_336_817,
        "approach_name": "Plaza Program & Open Streets",
        "description": (
            "NYC has pioneered public space activation through DOT's Plaza "
            "Program and the pandemic-era Open Streets initiative. The city "
            "permanently transforms underused roadways into pedestrian plazas "
            "managed by local nonprofit partners, and seasonal Open Streets "
            "close roadways to vehicles for community programming."
        ),
        "key_policies": [
            "NYC DOT Plaza Program",
            "Open Streets Program (permanent since 2023)",
            "POPS (Privately Owned Public Spaces) regulation",
            "NYC Parks Concession Program",
            "Street Activity Permit Office (SAPO)",
        ],
        "strengths": [
            "Plaza Program converts road space to permanent public plazas",
            "Open Streets reached 100+ streets with community programming",
            "Strong nonprofit partnership model for plaza management",
            "POPS regulations create publicly accessible space in private development",
            "Centralized Street Activity Permit Office for events",
        ],
        "weaknesses": [
            "High barriers for small organizations to manage plazas",
            "Open Streets program still contested in some neighborhoods",
            "POPS enforcement historically weak (many spaces not truly public)",
            "Insurance requirements remain high ($1M-$5M depending on size)",
            "Limited equity framework — plazas concentrated in wealthier areas",
        ],
        "lessons_for_philadelphia": [
            "Adopt a Plaza Program model for converting road space to public plazas",
            "Permanent Open Streets legislation shows pandemic innovation can persist",
            "Nonprofit management partnerships reduce city operational burden",
            "POPS concept could apply to large development projects in Philadelphia",
        ],
        "activation_score": 72,
        "notable_projects": [
            {
                "name": "Times Square Pedestrianization",
                "description": "Broadway closed to traffic between 42nd-47th Streets, creating massive pedestrian plaza.",
                "outcome": "Injuries down 40%, retail rents up, now permanent.",
            },
            {
                "name": "DUMBO Archway",
                "description": "Manhattan Bridge archway activated as public market, performance venue, and community space.",
                "outcome": "Year-round programming serving 500K+ visitors annually.",
            },
        ],
    },
    {
        "name": "Detroit",
        "country": "United States",
        "population": 639_111,
        "approach_name": "Land Bank Innovation",
        "description": (
            "Detroit's massive vacant land inventory (over 100,000 parcels) "
            "has forced innovation in space activation. The Detroit Land Bank "
            "Authority, Side Lot Program, and community-driven vacant lot "
            "activation have created a laboratory for public space reuse "
            "that directly informs Philadelphia's approach."
        ),
        "key_policies": [
            "Detroit Land Bank Authority",
            "Side Lot Program (adjacent vacant lots to neighbors)",
            "Motor City Match (small business placement)",
            "Detroit Future City framework",
            "Neighborhood Enterprise Zones",
        ],
        "strengths": [
            "Land Bank streamlines acquisition and activation of vacant parcels",
            "Side Lot Program has transferred 30,000+ lots to residents",
            "Strong community-driven activation culture (urban farming, art)",
            "Detroit Future City provides strategic framework for land reuse",
            "Low cost of acquisition enables experimentation",
        ],
        "weaknesses": [
            "Scale of vacancy overwhelms administrative capacity",
            "Limited public safety infrastructure for activated spaces",
            "Tax foreclosure pipeline continues feeding vacancy",
            "Racial equity concerns in who benefits from land activation",
            "Infrastructure (water, power) often missing on vacant parcels",
        ],
        "lessons_for_philadelphia": [
            "Side Lot Program model could accelerate adjacent-neighbor activation",
            "Community land trust integration protects against displacement",
            "Strategic land use framework prevents piecemeal activation",
            "Low-barrier acquisition paths encourage grassroots activation",
        ],
        "activation_score": 58,
        "notable_projects": [
            {
                "name": "Michigan Urban Farming Initiative",
                "description": "3-acre urban agrihood in North End providing free produce to 2,000 households.",
                "outcome": "Largest urban farm in the US. Model for food sovereignty.",
            },
            {
                "name": "Heidelberg Project",
                "description": "Tyree Guyton's outdoor art installation transforming two blocks of abandoned houses.",
                "outcome": "30+ years of operation. International recognition. Tourism driver.",
            },
        ],
    },
    {
        "name": "London",
        "country": "United Kingdom",
        "population": 8_982_000,
        "approach_name": "Meanwhile Use & Community Infrastructure Levy",
        "description": (
            "London leads in 'meanwhile use' — temporary activation of vacant "
            "buildings and land between permanent uses. The Meanwhile Foundation, "
            "Community Infrastructure Levy, and planning reforms have created "
            "a mature ecosystem for space activation."
        ),
        "key_policies": [
            "Meanwhile Use Leases (standard template)",
            "Community Infrastructure Levy",
            "Permitted Development Rights (temporary use)",
            "London Plan public space requirements",
            "Mayor's Good Growth Fund",
        ],
        "strengths": [
            "Standardized Meanwhile Use Lease templates reduce legal costs",
            "Community Infrastructure Levy funds public space in new development",
            "Permitted Development Rights allow temporary use without full planning permission",
            "Good Growth Fund specifically supports community-led space activation",
            "Strong creative/cultural sector drives innovative space use",
        ],
        "weaknesses": [
            "Meanwhile use can delay permanent affordable housing",
            "Community Infrastructure Levy complicated and inconsistently applied",
            "Land values make permanent activation financially challenging",
            "Gentrification concerns around 'creative' space activation",
            "Bureaucratic borough-level variation in implementation",
        ],
        "lessons_for_philadelphia": [
            "Standardized meanwhile-use lease templates reduce legal barriers dramatically",
            "Community Infrastructure Levy model could fund space activation in Philadelphia",
            "Permitted Development Rights concept could streamline temporary activations",
            "Good Growth Fund model — dedicated public funding for community-led activation",
        ],
        "activation_score": 76,
        "notable_projects": [
            {
                "name": "Pop Brixton",
                "description": "Shipping container village on council-owned land with 50+ independent businesses.",
                "outcome": "500 jobs created. Model replicated across UK.",
            },
            {
                "name": "Meanwhile Space CIC",
                "description": "Social enterprise matching vacant spaces with community organizations.",
                "outcome": "500+ spaces activated. £50M+ social value generated.",
            },
        ],
    },
    {
        "name": "Barcelona",
        "country": "Spain",
        "population": 1_636_762,
        "approach_name": "Superblocks & Citizen Platform",
        "description": (
            "Barcelona's Superblocks program transforms urban streets into "
            "community-controlled public spaces by restricting car traffic. "
            "Combined with the Decidim citizen participation platform and "
            "strong municipal commitment to public space, Barcelona represents "
            "the most ambitious systematic approach to space activation."
        ),
        "key_policies": [
            "Superilles (Superblocks) program",
            "Decidim citizen participation platform",
            "Pla Buits (Empty Lots Plan)",
            "Barcelona Right to the City",
            "Municipal Institute of Urban Landscape",
        ],
        "strengths": [
            "Superblocks systematically reclaim street space for public use",
            "Decidim platform enables direct citizen proposals for space use",
            "Pla Buits specifically activates vacant lots with community projects",
            "Strong political commitment to public space as a right",
            "Integrated climate, mobility, and public space planning",
        ],
        "weaknesses": [
            "Superblocks faced significant initial resident opposition",
            "Tourism pressure on public spaces in central districts",
            "Real estate speculation around activated/improved areas",
            "Complex multi-level governance (city, province, region)",
            "Scalability challenges — each Superblock requires intensive design",
        ],
        "lessons_for_philadelphia": [
            "Superblock concept could be adapted for Philadelphia's grid — 'Super Squares'",
            "Digital citizen platform (like Decidim) for proposing space activations",
            "Pla Buits vacant lot program directly applicable to Philly's vacant land",
            "Political framing of public space as a right builds public support",
        ],
        "activation_score": 85,
        "notable_projects": [
            {
                "name": "Superilla Sant Antoni",
                "description": "Nine-block Superblock transforming streets into plazas, play areas, and green space.",
                "outcome": "27% increase in pedestrian activity. 25% reduction in NO2 pollution.",
            },
            {
                "name": "Pla Buits Can Batlló",
                "description": "Former factory complex occupied and converted by community into cultural center.",
                "outcome": "20,000 sq meters of community space. 100+ activities weekly.",
            },
        ],
    },
    {
        "name": "Melbourne",
        "country": "Australia",
        "population": 5_078_193,
        "approach_name": "Laneways & Creative Spaces",
        "description": (
            "Melbourne transformed from a car-dominated city to a global model "
            "for public space through its Laneway Activation program, creative "
            "spaces policy, and integrated urban design. The city's approach "
            "emphasizes cultural programming and creative economy as drivers "
            "of space activation."
        ),
        "key_policies": [
            "Laneway Activation Program",
            "Creative Spaces Framework",
            "Places for People initiative",
            "Urban Forest Strategy",
            "Public Art Framework",
        ],
        "strengths": [
            "Laneway program turned neglected alleys into vibrant public spaces",
            "Creative Spaces Framework provides affordable space for artists/makers",
            "Strong integration of public art into all space activation",
            "Places for People research program grounds decisions in data",
            "Urban Forest Strategy connects green space to public space goals",
        ],
        "weaknesses": [
            "Activation concentrated in central city — suburbs less served",
            "Affordability crisis displacing creative tenants from activated areas",
            "COVID highlighted fragility of activation dependent on foot traffic",
            "Aboriginal and Torres Strait Islander space claims underaddressed",
            "Climate vulnerability (heat, flooding) in activated spaces",
        ],
        "lessons_for_philadelphia": [
            "Laneway activation model applicable to Philadelphia's alleys and passages",
            "Creative Spaces Framework could be adapted for Philly's artist community",
            "Data-driven approach (Places for People) builds evidence for investment",
            "Integration of public art into space activation elevates community value",
        ],
        "activation_score": 79,
        "notable_projects": [
            {
                "name": "Hosier Lane",
                "description": "Narrow laneway transformed into world-famous street art gallery and cultural destination.",
                "outcome": "Top tourist attraction. Template for laneway activation worldwide.",
            },
            {
                "name": "Testing Grounds",
                "description": "City-owned lot on Southbank converted to experimental arts and design space.",
                "outcome": "5 years of meanwhile use. 1,000+ events. Community design hub.",
            },
        ],
    },
]


# ---------------------------------------------------------------------------
# Equity Framework
# ---------------------------------------------------------------------------

EQUITY_FRAMEWORK = {
    "principles": [
        {
            "id": "access",
            "name": "Universal Access",
            "description": (
                "Every resident has the right to activate public space "
                "regardless of income, organization type, or political "
                "connection. Legal and financial barriers must be "
                "systematically reduced."
            ),
        },
        {
            "id": "priority",
            "name": "Need-Based Priority",
            "description": (
                "Neighborhoods with the most dormant space and least "
                "activation history receive first priority for resources, "
                "expedited review, and technical assistance."
            ),
        },
        {
            "id": "anti_displacement",
            "name": "Anti-Displacement",
            "description": (
                "Space activation must not accelerate displacement of "
                "existing residents. Community benefit agreements, "
                "affordability requirements, and community ownership "
                "pathways are mandatory safeguards."
            ),
        },
        {
            "id": "community_control",
            "name": "Community Control",
            "description": (
                "Residents of affected neighborhoods have decision-making "
                "power over how public space in their community is activated. "
                "Top-down activation without community consent is prohibited."
            ),
        },
        {
            "id": "permanence",
            "name": "Permanence Over Extraction",
            "description": (
                "Every activation must leave lasting value. The 25% permanence "
                "requirement ensures that temporary use creates permanent "
                "community benefit, not just temporary profit."
            ),
        },
        {
            "id": "transparency",
            "name": "Radical Transparency",
            "description": (
                "All permit decisions, scoring criteria, denial reasons, "
                "and activation outcomes are public. The activation process "
                "is fully legible to every resident."
            ),
        },
    ],
    "priority_scoring": {
        "criteria": [
            {
                "name": "Dormant Space Density",
                "weight": 0.25,
                "description": (
                    "Percentage of publicly-owned parcels in the ZIP code "
                    "that have been dormant for 12+ months. Higher density "
                    "= higher score."
                ),
            },
            {
                "name": "Median Income (Inverse)",
                "weight": 0.20,
                "description": (
                    "Inverse of ZIP code median household income relative "
                    "to city median. Lower income = higher score."
                ),
            },
            {
                "name": "Activation History (Inverse)",
                "weight": 0.20,
                "description": (
                    "Inverse of the number of space activations in the "
                    "ZIP code over the past 3 years. Fewer activations "
                    "= higher score."
                ),
            },
            {
                "name": "Community Organization Density",
                "weight": 0.15,
                "description": (
                    "Number of registered community organizations, CDCs, "
                    "and civic associations per capita in the ZIP code. "
                    "Higher density = higher capacity for activation."
                ),
            },
            {
                "name": "Health Outcome Gaps",
                "weight": 0.20,
                "description": (
                    "Composite health disadvantage score based on life "
                    "expectancy, chronic disease rates, mental health "
                    "indicators, and access to green space. Larger gaps "
                    "= higher priority."
                ),
            },
        ],
    },
    "anti_displacement_protections": [
        (
            "Community Benefit Agreements required for any commercial "
            "activation generating over $50,000 in annual revenue within "
            "a high-priority neighborhood."
        ),
        (
            "Affordability lock: activated spaces in high-priority "
            "neighborhoods must maintain at least 30% of programming "
            "at no cost or reduced cost to residents below 80% AMI."
        ),
        (
            "Right of first refusal: existing community organizations "
            "have 90-day right of first refusal for new activation "
            "opportunities in their service area."
        ),
        (
            "Anti-speculation clause: parcels activated through community "
            "petition may not be sold for market-rate development for "
            "5 years after activation begins."
        ),
        (
            "Local hiring requirement: activations with paid staff must "
            "hire at least 50% of workers from the surrounding ZIP code."
        ),
        (
            "Rent stabilization trigger: if median rents within 0.25 miles "
            "of an activated space increase by more than 10% in 12 months, "
            "the SAO must conduct a displacement impact assessment."
        ),
        (
            "Community land trust pathway: after 3 years of continuous "
            "community-led activation, the parcel may be transferred to "
            "a community land trust at nominal cost, permanently removing "
            "it from speculative markets."
        ),
    ],
    "community_ownership_pathways": [
        {
            "name": "Community Land Trust Transfer",
            "description": (
                "After 3 years of continuous community-led activation, "
                "parcels transfer to a qualified CLT at nominal cost ($1), "
                "with permanent affordability deed restrictions."
            ),
            "legal_mechanism": (
                "Philadelphia Land Bank disposition authority under "
                "Act 153 of 2012, with deed restriction recorded at "
                "time of transfer."
            ),
        },
        {
            "name": "Cooperative Ownership",
            "description": (
                "Activator groups may form cooperatives to collectively "
                "own and manage activated spaces, with technical assistance "
                "from the SAO and the Philadelphia Area Cooperative Alliance."
            ),
            "legal_mechanism": (
                "Pennsylvania Cooperative Corporation Act (15 Pa.C.S. "
                "Chapter 73), with land lease from the city or outright "
                "transfer to cooperative entity."
            ),
        },
        {
            "name": "Nonprofit Long-Term Lease",
            "description": (
                "Qualified 501(c)(3) organizations may enter 30-year "
                "renewable leases for activated public parcels at below-"
                "market rates, with performance milestones."
            ),
            "legal_mechanism": (
                "City Council authorization for below-market disposition "
                "under Philadelphia Home Rule Charter Section 11-1604, "
                "with performance-based lease terms."
            ),
        },
        {
            "name": "Public Benefit Corporation",
            "description": (
                "Community groups may form Pennsylvania Benefit Corporations "
                "that combine social mission with sustainable business "
                "operations to manage activated spaces permanently."
            ),
            "legal_mechanism": (
                "Pennsylvania Benefit Corporation Act (15 Pa.C.S. Chapter "
                "33), with community benefit reporting requirements and "
                "SAO oversight."
            ),
        },
    ],
}


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def get_city_comparison(city1: str, city2: str) -> dict:
    """Return side-by-side data for two cities."""
    data = {c["name"].lower(): c for c in COMPARATIVE_ANALYSIS}
    c1 = data.get(city1.lower())
    c2 = data.get(city2.lower())
    if not c1 or not c2:
        available = [c["name"] for c in COMPARATIVE_ANALYSIS]
        return {"error": f"City not found. Available: {available}"}
    return {"city_1": c1, "city_2": c2}


def calculate_equity_score(neighborhood_data: dict) -> dict:
    """
    Calculate equity priority score for a neighborhood.

    Parameters
    ----------
    neighborhood_data : dict
        Keys: dormant_space_density (0-1), median_income (int),
        activation_history (0-1, where 0 = no history),
        community_organization_density (0-1),
        health_outcome_gaps (0-1, where 1 = worst gaps)

    Returns
    -------
    dict with score, breakdown, priority_level, recommendations
    """
    criteria = EQUITY_FRAMEWORK["priority_scoring"]["criteria"]
    city_median_income = 52_649  # Philadelphia 2023 ACS

    # Normalize inputs
    dormant = neighborhood_data.get("dormant_space_density", 0)
    income = neighborhood_data.get("median_income", city_median_income)
    activation = neighborhood_data.get("activation_history", 0.5)
    org_density = neighborhood_data.get("community_organization_density", 0.5)
    health_gaps = neighborhood_data.get("health_outcome_gaps", 0.5)

    # Calculate component scores (0-100)
    dormant_score = dormant * 100
    income_score = max(0, min(100, (1 - income / city_median_income) * 100))
    activation_score = (1 - activation) * 100
    org_score = org_density * 100  # Higher org density = higher capacity
    health_score = health_gaps * 100

    # Weighted total
    breakdown = {
        "dormant_space_density": round(dormant_score, 1),
        "median_income_inverse": round(income_score, 1),
        "activation_history_inverse": round(activation_score, 1),
        "community_organization_density": round(org_score, 1),
        "health_outcome_gaps": round(health_score, 1),
    }

    weights = [c["weight"] for c in criteria]
    scores = [dormant_score, income_score, activation_score, org_score, health_score]
    total = sum(w * s for w, s in zip(weights, scores))
    total = round(total, 1)

    # Priority level
    if total >= 75:
        priority = "Critical Priority"
    elif total >= 55:
        priority = "High Priority"
    elif total >= 35:
        priority = "Moderate Priority"
    else:
        priority = "Standard"

    # Recommendations
    recommendations = []
    if dormant_score > 60:
        recommendations.append("High dormant space density — prioritize land bank activation partnerships")
    if income_score > 60:
        recommendations.append("Below-median income — waive permit fees and provide technical assistance")
    if activation_score > 70:
        recommendations.append("Low activation history — target for SAO outreach and community engagement")
    if org_score < 40:
        recommendations.append("Low organizational capacity — invest in community organizing support")
    if health_score > 60:
        recommendations.append("Significant health gaps — prioritize green space and food access activations")

    return {
        "score": total,
        "breakdown": breakdown,
        "priority_level": priority,
        "recommendations": recommendations,
    }
