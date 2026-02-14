"""
SPHERES Innovation Laboratory — Ecosystem Architect seed innovations and
generator templates.

Domain: ecosystem-architecture — Cross-sector partnerships, institutional
alignment, governance structures, resource flow networks, collaborative
frameworks for Philadelphia's public space activation platform.
"""

# ---------------------------------------------------------------------------
# Seed Innovations — 6 curated concepts ready for lab exploration
# ---------------------------------------------------------------------------

INNOVATIONS: list[dict] = [
    # 1 ── Space Activation Governance Council
    {
        "title": "Space Activation Governance Council",
        "summary": (
            "A cross-sector decision-making body uniting City agencies, CDCs, "
            "universities, and neighborhood leaders to co-govern activated public "
            "spaces across Philadelphia."
        ),
        "category": "governance-model",
        "impact_level": 5,
        "feasibility": 3,
        "novelty": 4,
        "time_horizon": "medium",
        "status": "approved",
        "details": {
            "governance_structure": (
                "Tri-chamber model with an Agency Chamber (L&I, Parks & Rec, "
                "Commerce, Planning Commission), a Community Chamber (CDC reps "
                "and neighborhood advisory committees), and a Knowledge Chamber "
                "(UPenn, Temple, Drexel faculty and health system liaisons). "
                "Each chamber holds equal voting weight. A rotating Chair "
                "cycles across chambers every six months."
            ),
            "participating_organizations": [
                "Philadelphia Department of Licenses & Inspections",
                "Philadelphia Parks & Recreation",
                "Philadelphia Commerce Department",
                "Philadelphia City Planning Commission",
                "Philadelphia Land Bank",
                "Asociacion Puertorriquenos en Marcha (APM)",
                "New Kensington CDC",
                "People's Emergency Center CDC",
                "University of Pennsylvania Weitzman School of Design",
                "Temple University Community Collaborative",
                "Drexel University Lindy Institute for Urban Innovation",
                "Jefferson Health",
                "Philadelphia Foundation",
                "William Penn Foundation",
            ],
            "decision_making_process": (
                "Modified consensus: proposals require support from at least "
                "two of three chambers. Any single chamber may invoke a 30-day "
                "deliberation pause for community input. Emergency operational "
                "decisions (safety, weather) follow a streamlined pathway with "
                "ratification at the next regular session."
            ),
            "meeting_cadence": (
                "Full Council meets monthly; standing committees (Finance, "
                "Equity, Operations) meet biweekly; ad-hoc task forces convene "
                "as needed with a 72-hour formation protocol."
            ),
            "accountability_framework": (
                "Quarterly public scorecards published on the SPHERES dashboard "
                "tracking activation outcomes, equity metrics, and budget "
                "utilization. Annual independent audit by a rotating evaluator "
                "selected from the Knowledge Chamber."
            ),
        },
        "tags": [
            "governance",
            "cross-sector",
            "decision-making",
            "equity",
            "public-accountability",
        ],
    },

    # 2 ── Resource Flow Network
    {
        "title": "Resource Flow Network",
        "summary": (
            "A real-time mapping and optimization engine that visualizes how "
            "funding, materials, staff time, and expertise flow across 50+ "
            "organizations involved in Philadelphia space activation."
        ),
        "category": "partnership-framework",
        "impact_level": 4,
        "feasibility": 3,
        "novelty": 5,
        "time_horizon": "medium",
        "status": "approved",
        "details": {
            "governance_structure": (
                "Managed by a Network Coordinator embedded within the SPHERES "
                "platform team, reporting jointly to the Governance Council "
                "and the Philanthropic Alignment Table. An open-data steering "
                "committee ensures transparency norms."
            ),
            "resource_allocation_model": (
                "Four resource classes tracked: financial (grants, city "
                "allocations), material (tools, signage, furnishings), human "
                "(staff hours, volunteer hours), and intellectual (research, "
                "design consultation). Each node in the network self-reports "
                "quarterly; AI-assisted anomaly detection flags under-utilized "
                "or bottlenecked flows for Council review."
            ),
            "participating_organizations": [
                "All Governance Council members",
                "12 neighborhood CDCs",
                "Philadelphia Land Bank",
                "Philadelphia Housing Authority",
                "LISC Philadelphia",
                "Enterprise Community Partners",
                "Local Initiatives Support Corporation",
                "Reinvestment Fund",
                "Philadelphia Energy Authority",
            ],
            "conflict_resolution": (
                "Resource disputes escalate through a three-tier process: "
                "1) direct negotiation between nodes facilitated by the "
                "Network Coordinator, 2) mediation panel drawn from uninvolved "
                "Council members, 3) binding recommendation from an external "
                "mediator approved by all chambers."
            ),
            "accountability_framework": (
                "Live network dashboard accessible to all member organizations. "
                "Monthly flow reports auto-generated. Annual equity audit "
                "ensures no neighborhood receives less than its proportional "
                "share of total resource throughput."
            ),
        },
        "tags": [
            "resource-mapping",
            "network-analysis",
            "optimization",
            "transparency",
            "cross-organization",
        ],
    },

    # 3 ── University-Community Research Alliance
    {
        "title": "University-Community Research Alliance",
        "summary": (
            "Embeds PhD researchers and graduate fellows from UPenn, Temple, "
            "and Drexel directly into neighborhood activation projects, "
            "co-designing research agendas with community stakeholders."
        ),
        "category": "partnership-framework",
        "impact_level": 4,
        "feasibility": 4,
        "novelty": 3,
        "time_horizon": "near",
        "status": "approved",
        "details": {
            "governance_structure": (
                "Joint Oversight Board with equal representation from each "
                "university partner and participating CDCs. A Community "
                "Research Ethics Panel reviews all project proposals to ensure "
                "alignment with neighborhood priorities and data sovereignty "
                "principles."
            ),
            "participating_organizations": [
                "University of Pennsylvania Weitzman School of Design",
                "UPenn School of Social Policy & Practice",
                "Temple University Department of Geography and Urban Studies",
                "Temple University Community Collaborative",
                "Drexel University Lindy Institute for Urban Innovation",
                "Drexel University Dornsife School of Public Health",
                "New Kensington CDC",
                "People's Emergency Center CDC",
                "Asociacion Puertorriquenos en Marcha",
                "Philadelphia Parks & Recreation",
            ],
            "decision_making_process": (
                "Research agendas co-developed through seasonal community "
                "design charrettes. Each project requires a signed Community "
                "Benefit Agreement specifying deliverables, timelines, data "
                "ownership, and public reporting commitments before IRB "
                "submission."
            ),
            "resource_allocation_model": (
                "Universities contribute researcher time and overhead waivers; "
                "CDCs provide site access and community liaison hours; SPHERES "
                "platform provides data infrastructure. External grants "
                "administered through a pooled fund with 60% flowing to "
                "community-side costs."
            ),
            "conflict_resolution": (
                "Disputes between researchers and community partners heard by "
                "the Community Research Ethics Panel within 14 days. Panel "
                "decisions are binding; persistent conflicts trigger project "
                "pause and reassignment of the research fellow."
            ),
        },
        "tags": [
            "university-partnership",
            "community-research",
            "co-design",
            "data-sovereignty",
            "graduate-fellows",
        ],
    },

    # 4 ── Inter-Agency Data Sharing Protocol
    {
        "title": "Inter-Agency Data Sharing Protocol",
        "summary": (
            "A unified API layer and governance protocol enabling real-time "
            "data exchange among L&I, Parks & Rec, Commerce, Planning, and "
            "the Land Bank to streamline space activation decisions."
        ),
        "category": "data-governance",
        "impact_level": 5,
        "feasibility": 2,
        "novelty": 4,
        "time_horizon": "medium",
        "status": "review",
        "details": {
            "governance_structure": (
                "Data Governance Board chaired by the City Chief Data Officer "
                "with representatives from each participating agency and a "
                "community data advocate appointed by the Governance Council. "
                "Technical operations managed by the Office of Innovation & "
                "Technology (OIT)."
            ),
            "participating_organizations": [
                "Philadelphia Office of Innovation & Technology",
                "Department of Licenses & Inspections",
                "Philadelphia Parks & Recreation",
                "Philadelphia Commerce Department",
                "Philadelphia City Planning Commission",
                "Philadelphia Land Bank",
                "Philadelphia Water Department",
                "Streets Department",
                "Office of the Chief Data Officer",
            ],
            "decision_making_process": (
                "New data-sharing agreements require approval from each "
                "agency's data steward and legal counsel. The Data Governance "
                "Board ratifies cross-agency schemas quarterly. Community "
                "data advocate holds veto power over any expansion that could "
                "enable surveillance or punitive enforcement."
            ),
            "resource_allocation_model": (
                "Initial buildout funded by a joint OIT-Commerce allocation. "
                "Ongoing maintenance shared proportionally by API call volume. "
                "Partner universities contribute integration engineering via "
                "the Research Alliance."
            ),
            "accountability_framework": (
                "Monthly uptime and latency reports published publicly. "
                "Privacy impact assessments conducted annually. Community "
                "data advocate publishes an independent transparency report "
                "every six months."
            ),
        },
        "tags": [
            "data-sharing",
            "API",
            "inter-agency",
            "privacy",
            "open-data",
        ],
    },

    # 5 ── Community Stewardship Network
    {
        "title": "Community Stewardship Network",
        "summary": (
            "Neighborhood-level governance circles empowering residents to "
            "manage, program, and maintain activated public spaces through "
            "elected stewardship committees with real budget authority."
        ),
        "category": "governance-model",
        "impact_level": 5,
        "feasibility": 3,
        "novelty": 4,
        "time_horizon": "near",
        "status": "approved",
        "details": {
            "governance_structure": (
                "Each activated space has a Stewardship Circle of 7-12 elected "
                "residents serving staggered two-year terms. Circles are "
                "organized into District Clusters aligned with City Council "
                "districts. A citywide Steward Assembly meets quarterly to "
                "share best practices and escalate systemic issues to the "
                "Governance Council."
            ),
            "participating_organizations": [
                "Neighborhood advisory committees (10 pilot neighborhoods)",
                "Registered community organizations (RCOs)",
                "Philadelphia Parks & Recreation",
                "Philadelphia Land Bank",
                "Local CDCs as fiscal sponsors",
                "Philadelphia Volunteer Center",
            ],
            "decision_making_process": (
                "Stewardship Circles use consent-based decision-making for "
                "programming and maintenance. Budget decisions above $5,000 "
                "require a public meeting with 48-hour advance notice. "
                "Annual participatory budgeting process allocates discretionary "
                "funds across each District Cluster."
            ),
            "resource_allocation_model": (
                "Each Stewardship Circle receives an annual operational "
                "micro-grant ($15,000-$40,000 based on space size and foot "
                "traffic) administered through CDC fiscal sponsors. In-kind "
                "support from Parks & Rec for maintenance equipment and "
                "training. Volunteer hour-banking system enables labor exchange "
                "across neighborhoods."
            ),
            "meeting_cadence": (
                "Stewardship Circles meet biweekly; District Clusters meet "
                "monthly; citywide Steward Assembly meets quarterly. All "
                "meetings are open to the public with childcare and "
                "interpretation services provided."
            ),
        },
        "tags": [
            "community-governance",
            "stewardship",
            "participatory-budgeting",
            "neighborhood-power",
            "resident-leadership",
        ],
    },

    # 6 ── Philanthropic Alignment Table
    {
        "title": "Philanthropic Alignment Table",
        "summary": (
            "A coordinating body for 12+ regional and national foundations to "
            "align grantmaking around shared public space activation metrics, "
            "reducing duplication and amplifying collective impact."
        ),
        "category": "partnership-framework",
        "impact_level": 4,
        "feasibility": 4,
        "novelty": 3,
        "time_horizon": "near",
        "status": "approved",
        "details": {
            "governance_structure": (
                "Facilitated roundtable with a rotating Chair drawn from "
                "member foundations. A small Secretariat (2 FTEs) housed at "
                "the Philadelphia Foundation manages logistics, data, and "
                "reporting. Community accountability ensured by two seats "
                "reserved for Stewardship Network representatives."
            ),
            "participating_organizations": [
                "William Penn Foundation",
                "Philadelphia Foundation",
                "Knight Foundation — Philadelphia",
                "Pew Charitable Trusts",
                "Lenfest Foundation",
                "Wells Fargo Regional Foundation",
                "JPMorgan Chase Foundation",
                "Wyncote Foundation",
                "Samuel S. Fels Fund",
                "Patricia Kind Family Foundation",
                "Barra Foundation",
                "Surdna Foundation",
                "Kresge Foundation",
            ],
            "decision_making_process": (
                "Non-binding alignment: each foundation retains independent "
                "grantmaking authority but commits to sharing pipeline data "
                "and coordinating timelines. Shared metrics adopted by "
                "consensus; any foundation may opt out of specific metrics "
                "with written rationale."
            ),
            "resource_allocation_model": (
                "Pooled Impact Fund ($2M annually) for gap-filling grants "
                "that no single foundation would cover. Contributions "
                "proportional to each foundation's Philadelphia-area giving. "
                "Secretariat costs shared equally among members."
            ),
            "accountability_framework": (
                "Shared outcomes dashboard updated quarterly. Annual "
                "alignment report benchmarks collective progress against "
                "shared metrics. Community accountability hearings held twice "
                "per year in partnership with the Stewardship Network."
            ),
        },
        "tags": [
            "philanthropy",
            "foundation-alignment",
            "collective-impact",
            "grantmaking",
            "shared-metrics",
        ],
    },
]


# ---------------------------------------------------------------------------
# Generator Templates — 8 patterns the innovation generator can remix
# ---------------------------------------------------------------------------

TEMPLATES: list[dict] = [
    # T1 ── Multi-Stakeholder Governance Body
    {
        "title": "Multi-Stakeholder Governance Body",
        "summary": (
            "Template for creating cross-sector governance structures that "
            "balance agency authority, community voice, and institutional "
            "expertise in public space decisions."
        ),
        "category": "governance-model",
        "time_horizon": "medium",
        "impact_range": [4, 5],
        "feasibility_range": [2, 4],
        "novelty_range": [3, 5],
        "details": {
            "governance_structure": (
                "Configurable chamber model (2-4 chambers) with adjustable "
                "voting weights, quorum rules, and escalation pathways. "
                "Supports consensus, supermajority, and consent-based "
                "decision protocols."
            ),
            "participating_organizations": (
                "Variable: city agencies, CDCs, anchor institutions, "
                "neighborhood advisory bodies. Minimum three sectors required."
            ),
            "decision_making_process": (
                "Modular ruleset: select from consensus, modified consensus, "
                "supermajority, or consent-based protocols. All variants "
                "include community input windows and emergency bypass clauses."
            ),
        },
        "tags": [
            "governance",
            "multi-stakeholder",
            "template",
            "decision-making",
        ],
    },

    # T2 ── Cross-Sector Data Exchange
    {
        "title": "Cross-Sector Data Exchange",
        "summary": (
            "Template for designing inter-organizational data sharing "
            "agreements with built-in privacy protections, community "
            "oversight, and technical interoperability standards."
        ),
        "category": "data-governance",
        "time_horizon": "medium",
        "impact_range": [3, 5],
        "feasibility_range": [2, 3],
        "novelty_range": [3, 4],
        "details": {
            "governance_structure": (
                "Data governance board with agency stewards, legal counsel, "
                "community data advocates, and technical leads. Privacy "
                "impact assessment required for each new data flow."
            ),
            "resource_allocation_model": (
                "Cost-sharing formula based on API call volume, data storage, "
                "and integration complexity. Open-source components preferred "
                "to reduce vendor lock-in."
            ),
            "accountability_framework": (
                "Public uptime dashboards, annual privacy audits, and "
                "community transparency reports. Breach notification protocol "
                "with 24-hour disclosure window."
            ),
        },
        "tags": [
            "data-sharing",
            "interoperability",
            "privacy",
            "template",
        ],
    },

    # T3 ── Community Governance Circle
    {
        "title": "Community Governance Circle",
        "summary": (
            "Template for establishing neighborhood-level governance bodies "
            "with elected residents, fiscal authority, and formal linkage "
            "to city decision-making structures."
        ),
        "category": "governance-model",
        "time_horizon": "near",
        "impact_range": [4, 5],
        "feasibility_range": [3, 4],
        "novelty_range": [3, 4],
        "details": {
            "governance_structure": (
                "Elected circle of 5-15 residents with staggered terms. "
                "Nested into district clusters and citywide assemblies. "
                "Fiscal sponsor relationship with established CDC."
            ),
            "decision_making_process": (
                "Consent-based for operations; participatory budgeting for "
                "annual allocations. Public meeting requirements with "
                "accessibility provisions (childcare, translation, ADA)."
            ),
            "meeting_cadence": (
                "Configurable: biweekly circles, monthly clusters, quarterly "
                "assemblies. All meetings open to public with advance notice "
                "requirements."
            ),
        },
        "tags": [
            "community-power",
            "neighborhood-governance",
            "participatory",
            "template",
        ],
    },

    # T4 ── Philanthropic Coordination Mechanism
    {
        "title": "Philanthropic Coordination Mechanism",
        "summary": (
            "Template for aligning multiple funders around shared outcome "
            "metrics while preserving individual grantmaking autonomy and "
            "ensuring community accountability."
        ),
        "category": "partnership-framework",
        "time_horizon": "near",
        "impact_range": [3, 5],
        "feasibility_range": [3, 5],
        "novelty_range": [3, 4],
        "details": {
            "governance_structure": (
                "Rotating chair model with independent secretariat. Community "
                "seats ensure grassroots accountability. Non-binding alignment "
                "with opt-out provisions for specific metrics."
            ),
            "resource_allocation_model": (
                "Pooled impact fund for gap-filling; contributions proportional "
                "to regional giving. Shared pipeline data to avoid duplication. "
                "Secretariat costs split equally."
            ),
            "accountability_framework": (
                "Shared outcomes dashboard, annual alignment reports, and "
                "community accountability hearings. Independent evaluation "
                "every three years."
            ),
        },
        "tags": [
            "philanthropy",
            "alignment",
            "collective-impact",
            "template",
        ],
    },

    # T5 ── University-Community Partnership
    {
        "title": "University-Community Partnership",
        "summary": (
            "Template for structuring equitable research collaborations "
            "between anchor institutions and neighborhood organizations, "
            "centering community benefit and data sovereignty."
        ),
        "category": "partnership-framework",
        "time_horizon": "near",
        "impact_range": [3, 5],
        "feasibility_range": [3, 4],
        "novelty_range": [3, 5],
        "details": {
            "governance_structure": (
                "Joint oversight board with parity representation. Community "
                "Research Ethics Panel with authority to pause projects. "
                "Data sovereignty clause in all agreements."
            ),
            "decision_making_process": (
                "Co-designed research agendas via community charrettes. "
                "Community Benefit Agreements signed before project launch. "
                "All publications require community review period."
            ),
            "conflict_resolution": (
                "Ethics Panel mediation within 14 days. Escalation to joint "
                "oversight board. Project pause and fellow reassignment as "
                "final remedy."
            ),
        },
        "tags": [
            "university",
            "community-research",
            "equity",
            "co-design",
            "template",
        ],
    },

    # T6 ── Resource Flow Optimization Network
    {
        "title": "Resource Flow Optimization Network",
        "summary": (
            "Template for building multi-organization resource tracking "
            "systems that visualize, analyze, and rebalance the flow of "
            "funding, materials, and expertise across a coalition."
        ),
        "category": "resource-network",
        "time_horizon": "medium",
        "impact_range": [3, 5],
        "feasibility_range": [2, 4],
        "novelty_range": [4, 5],
        "details": {
            "resource_allocation_model": (
                "Four resource classes: financial, material, human, and "
                "intellectual. Self-reporting by nodes with AI anomaly "
                "detection. Equity-weighted rebalancing recommendations."
            ),
            "accountability_framework": (
                "Live network dashboard, monthly flow reports, annual equity "
                "audit. Proportional share guarantees prevent systematic "
                "under-investment in any neighborhood."
            ),
            "conflict_resolution": (
                "Three-tier process: direct negotiation, mediation panel, "
                "external binding arbitration. Resource disputes resolved "
                "within 30 days."
            ),
        },
        "tags": [
            "resource-flow",
            "network-analysis",
            "optimization",
            "equity",
            "template",
        ],
    },

    # T7 ── Inter-Institutional Memorandum of Understanding
    {
        "title": "Inter-Institutional Memorandum of Understanding",
        "summary": (
            "Template for drafting MOUs between city agencies, nonprofits, "
            "and anchor institutions that codify shared commitments, "
            "resource contributions, and dispute resolution pathways."
        ),
        "category": "legal-framework",
        "time_horizon": "near",
        "impact_range": [3, 4],
        "feasibility_range": [4, 5],
        "novelty_range": [2, 3],
        "details": {
            "governance_structure": (
                "Bilateral or multilateral MOU with named signatories, "
                "designated liaisons, and annual renewal clauses. Amendment "
                "process requires written consent of all parties."
            ),
            "resource_allocation_model": (
                "Each signatory's contributions enumerated: staff time, "
                "funding commitments, in-kind support, data access. "
                "Quarterly reconciliation against commitments."
            ),
            "conflict_resolution": (
                "Step 1: liaison-level resolution within 10 business days. "
                "Step 2: executive-level mediation within 30 days. "
                "Step 3: external mediation with shared cost."
            ),
        },
        "tags": [
            "MOU",
            "legal",
            "institutional-agreement",
            "template",
        ],
    },

    # T8 ── Equity-Centered Accountability System
    {
        "title": "Equity-Centered Accountability System",
        "summary": (
            "Template for building accountability frameworks that center "
            "racial equity, geographic fairness, and community voice in "
            "how partnerships measure success and course-correct."
        ),
        "category": "accountability-framework",
        "time_horizon": "medium",
        "impact_range": [4, 5],
        "feasibility_range": [2, 4],
        "novelty_range": [4, 5],
        "details": {
            "accountability_framework": (
                "Equity scorecard with disaggregated metrics by race, "
                "income, geography, and language. Community-defined success "
                "indicators weighted equally with institutional KPIs."
            ),
            "decision_making_process": (
                "Annual equity audit with public hearings. Course-correction "
                "triggers when disparity ratios exceed thresholds. Community "
                "veto power over metrics that enable harm."
            ),
            "governance_structure": (
                "Independent equity monitor appointed jointly by community "
                "and institutional partners. Monitor publishes biannual "
                "reports and recommends binding corrective actions."
            ),
        },
        "tags": [
            "equity",
            "accountability",
            "racial-justice",
            "metrics",
            "template",
        ],
    },
]
