"""
SPHERES Innovation Laboratory — City Replicator seed innovations and templates.

Domain: city-replication
City Readiness Scorecard approach: evaluating US cities across five dimensions
(Inventory, Permits, Culture, Funding, Policy) to prioritize and sequence
SPHERES deployment.  Scorecards generate month-by-month adoption playbooks
tailored to each city's archetype and readiness profile.
"""

# ---------------------------------------------------------------------------
# Seed Innovations — 6 validated ideas ready for the innovation pipeline
# ---------------------------------------------------------------------------

INNOVATIONS: list[dict] = [
    # ------------------------------------------------------------------
    # 1. Philadelphia Readiness Scorecard
    # ------------------------------------------------------------------
    {
        "title": "Philadelphia Readiness Scorecard",
        "summary": (
            "Comprehensive readiness assessment scoring Philadelphia at 82/100 "
            "for SPHERES activation.  The city's vast 40,000+ vacant lot inventory, "
            "deeply rooted Mural Arts culture, active Land Bank, and growing "
            "philanthropic base make it the flagship proof-of-concept city.  "
            "A month-by-month adoption playbook translates the scorecard into "
            "concrete actions across all five readiness dimensions."
        ),
        "category": "readiness-scorecard",
        "impact_level": 4,
        "feasibility": 5,
        "novelty": 3,
        "time_horizon": "near",
        "status": "approved",
        "details": {
            "overall_score": 82,
            "dimension_scores": {
                "inventory": 90,
                "permits": 68,
                "culture": 92,
                "funding": 78,
                "policy": 82,
            },
            "city_archetype": "Flagship — origin city with strongest institutional knowledge",
            "key_strengths": [
                "40,000+ publicly documented vacant lots providing massive activation inventory",
                "Mural Arts Philadelphia program creates deep cultural infrastructure for public art",
                "Strong neighborhood identity and civic association networks across the city",
                "Philadelphia Land Bank actively disposing lots to community organizations",
                "Rebuild initiative channeling beverage-tax revenue into parks and community spaces",
                "Robust philanthropic ecosystem including William Penn, Knight, and Lenfest foundations",
            ],
            "key_challenges": [
                "Permit complexity: multi-agency approval for lot activation (L&I, Water, Streets)",
                "Interdepartmental coordination delays average 4-6 weeks per project",
                "Gentrification pressure in rapidly appreciating neighborhoods may compete for lots",
                "Limited city IT capacity for deploying IoT sensor infrastructure at scale",
            ],
            "adoption_playbook": {
                "month_1": (
                    "Baseline — Finalize MOU with Land Bank; identify 10 pilot lots in "
                    "high-readiness neighborhoods (Strawberry Mansion, Kensington, Point Breeze); "
                    "convene cross-departmental steering committee."
                ),
                "month_2": (
                    "Community Onboarding — Launch community engagement sessions at each "
                    "pilot lot; recruit neighborhood ambassadors; map existing community "
                    "assets within 3-block radius of each site."
                ),
                "month_3": (
                    "Permit Fast-Track — Work with L&I to establish expedited review "
                    "pathway for SPHERES activations; draft standard conditions checklist "
                    "to reduce per-lot review time from 6 weeks to 2 weeks."
                ),
                "month_4": (
                    "Infrastructure Deployment — Install modular structures and IoT "
                    "sensors at first 5 lots; integrate data pipeline with city's "
                    "existing OpenDataPhilly platform; train on-site stewards."
                ),
                "month_5": (
                    "Programming Launch — Activate cultural programming at all 10 sites; "
                    "partner with Mural Arts for public art installations; launch "
                    "youth employment program for site maintenance."
                ),
                "month_6": (
                    "Measurement and Iteration — Publish first quarterly impact report; "
                    "conduct community satisfaction survey; adjust programming based on "
                    "foot-traffic and sentiment data; plan Phase 2 expansion to 25 lots."
                ),
            },
        },
        "tags": ["scorecard", "philadelphia", "flagship", "readiness", "adoption-playbook"],
    },
    # ------------------------------------------------------------------
    # 2. Detroit Readiness Scorecard
    # ------------------------------------------------------------------
    {
        "title": "Detroit Readiness Scorecard",
        "summary": (
            "Detroit scores 91/100 — the highest readiness of any US city evaluated.  "
            "With over 150,000 vacant lots (the largest inventory in the nation), an "
            "exceptionally active land bank, strong grassroots community energy, and "
            "a city government openly eager for innovative reuse strategies, Detroit "
            "represents the ideal second city for SPHERES deployment.  Limited but "
            "growing funding is the primary gap to address."
        ),
        "category": "readiness-scorecard",
        "impact_level": 5,
        "feasibility": 4,
        "novelty": 3,
        "time_horizon": "near",
        "status": "approved",
        "details": {
            "overall_score": 91,
            "dimension_scores": {
                "inventory": 98,
                "permits": 85,
                "culture": 88,
                "funding": 72,
                "policy": 95,
            },
            "city_archetype": "Rust Belt — inventory-rich with strong institutional support",
            "key_strengths": [
                "150,000+ vacant lots — largest inventory of any US city, providing unmatched scale",
                "Detroit Land Bank Authority is the most active in the country, disposing 10,000+ lots/year",
                "City government desperate for innovative lot reuse and openly supportive of pilots",
                "Strong grassroots community organizations (Brightmoor Alliance, Michigan Urban Farming Initiative)",
                "Arts and culture revival: Heidelberg Project, Detroit Design Festival, Mocad",
                "Existing side-lot disposition program provides legal template for community transfers",
            ],
            "key_challenges": [
                "Funding ecosystem still recovering; fewer large local foundations than Philadelphia",
                "Scale is both an asset and a challenge — 150K lots requires aggressive triage and prioritization",
                "Blight remediation costs on some lots may exceed activation budgets",
                "Population decline means some neighborhoods lack critical mass for sustained programming",
            ],
            "adoption_playbook": {
                "month_1": (
                    "Partnership Formation — Execute MOU with Detroit Land Bank Authority; "
                    "convene advisory council including Kresge Foundation, Community Development "
                    "Advocates of Detroit, and Mayor's Office of Neighborhoods."
                ),
                "month_2": (
                    "Lot Triage — Apply SPHERES scoring algorithm to DLBA inventory; "
                    "identify top 50 activation-ready lots clustered in 5 neighborhoods; "
                    "conduct environmental screening to flag brownfield issues."
                ),
                "month_3": (
                    "Community Co-Design — Host design charrettes in Brightmoor, "
                    "Fitzgerald, Grandmont-Rosedale, Banglatown, and Core City; "
                    "recruit 25 neighborhood stewards; establish local governance boards."
                ),
                "month_4": (
                    "Funding Blitz — Submit applications to Kresge, Ralph C. Wilson Jr. "
                    "Foundation, Michigan Economic Development Corporation; pursue USDA "
                    "Community Facilities grant; launch crowdfunding for first 10 sites."
                ),
                "month_5": (
                    "Activation Sprint — Deploy modular infrastructure at 10 pilot lots; "
                    "install IoT sensors; partner with Michigan Urban Farming Initiative "
                    "for productive green space programming; launch public art commissions."
                ),
                "month_6": (
                    "Scale Planning — Evaluate pilot data; publish impact report; present "
                    "results to City Council for budget allocation; develop 3-year plan "
                    "to scale from 10 to 200 activated lots across Detroit."
                ),
            },
        },
        "tags": ["scorecard", "detroit", "rust-belt", "highest-readiness", "land-bank"],
    },
    # ------------------------------------------------------------------
    # 3. Austin Readiness Scorecard
    # ------------------------------------------------------------------
    {
        "title": "Austin Readiness Scorecard",
        "summary": (
            "Austin scores 64/100, representing a fundamentally different city "
            "archetype: demand-driven rather than inventory-driven.  The city has "
            "limited public vacant land but a thriving creative culture, deep tech "
            "wealth, and strong foundation support.  The primary barriers are NIMBY "
            "resistance and complex permitting.  Austin tests whether SPHERES can "
            "succeed in high-growth Sun Belt cities where the challenge is access "
            "to space, not surplus of it."
        ),
        "category": "readiness-scorecard",
        "impact_level": 3,
        "feasibility": 4,
        "novelty": 3,
        "time_horizon": "near",
        "status": "approved",
        "details": {
            "overall_score": 64,
            "dimension_scores": {
                "inventory": 42,
                "permits": 58,
                "culture": 85,
                "funding": 88,
                "policy": 48,
            },
            "city_archetype": "Sun Belt — demand-driven with limited public land inventory",
            "key_strengths": [
                "Vibrant creative and music culture creates natural community around public space",
                "Strong tech economy generates wealth and corporate sponsorship potential",
                "Active foundation ecosystem including St. David's, Still Water, and Austin Community Foundation",
                "University of Texas provides research partnership and student volunteer pipeline",
                "Existing 'Creative Space' zoning overlay could be adapted for SPHERES activations",
                "High civic engagement rate and culture of volunteerism",
            ],
            "key_challenges": [
                "Limited publicly owned vacant land — most underutilized parcels are private",
                "NIMBY resistance in established neighborhoods, especially around density and use changes",
                "Complex permitting: multi-board review for land use changes (Planning, Zoning, Historic)",
                "Rapidly rising land values make even temporary activation economically contested",
                "Political polarization around growth and development limits policy innovation",
            ],
            "adoption_playbook": {
                "month_1": (
                    "Land Access Strategy — Map city-owned underutilized parcels, TxDOT "
                    "surplus land, and willing private landowners; negotiate interim-use "
                    "agreements rather than disposition; explore partnership with Austin "
                    "Housing Finance Corporation for co-located activation."
                ),
                "month_2": (
                    "NIMBY Mitigation — Launch proactive community engagement in target "
                    "neighborhoods; frame activations as amenity enhancements, not development; "
                    "recruit neighborhood association leaders as co-designers; prepare "
                    "visual impact studies for public meetings."
                ),
                "month_3": (
                    "Permit Pathway — Work with Development Services to create administrative "
                    "approval pathway for temporary activations (< 2 years); propose "
                    "amendment to Creative Space overlay to include SPHERES-type uses; "
                    "engage City Council allies on streamlining ordinance."
                ),
                "month_4": (
                    "Funding Mobilization — Approach tech companies (Dell, Indeed, Oracle) "
                    "for corporate sponsorship; submit proposals to St. David's Foundation "
                    "and Austin Community Foundation; explore Austin Smart City challenge funds."
                ),
                "month_5": (
                    "Pilot Launch — Activate 3-5 sites on secured parcels; partner with "
                    "local artists and SXSW community for programming; deploy lightweight "
                    "sensor infrastructure; coordinate with UT Austin for impact research."
                ),
                "month_6": (
                    "Model Validation — Assess whether demand-driven model generates "
                    "sufficient community traction without large-scale lot inventory; "
                    "document lessons for other Sun Belt cities (Phoenix, Charlotte, Nashville); "
                    "publish comparative analysis against Rust Belt deployment model."
                ),
            },
        },
        "tags": ["scorecard", "austin", "sun-belt", "demand-driven", "creative-culture"],
    },
    # ------------------------------------------------------------------
    # 4. Top 50 Cities Ranked Index
    # ------------------------------------------------------------------
    {
        "title": "Top 50 Cities Ranked Index",
        "summary": (
            "A comprehensive ranking of the top 50 US cities by SPHERES activation "
            "readiness, scored across five dimensions (Inventory, Permits, Culture, "
            "Funding, Policy) with radar charts enabling visual comparison.  Cities "
            "are classified into four archetypes: Rust Belt (inventory-rich), Sun Belt "
            "(demand-driven), Gateway (policy-complex), and College Town "
            "(institution-anchored).  The index serves as a strategic roadmap for "
            "national scaling, identifying which cities to approach first and what "
            "engagement strategy to use for each archetype."
        ),
        "category": "readiness-index",
        "impact_level": 5,
        "feasibility": 3,
        "novelty": 4,
        "time_horizon": "medium",
        "status": "review",
        "details": {
            "target_cities": [
                "Tier 1 (Score 85+): Detroit, Cleveland, Baltimore, St. Louis, Gary IN",
                "Tier 2 (Score 70-84): Philadelphia, Pittsburgh, Newark NJ, Camden NJ, Buffalo",
                "Tier 3 (Score 55-69): Austin, Memphis, Milwaukee, Cincinnati, Minneapolis",
                "Tier 4 (Score 40-54): Portland, Denver, Atlanta, Charlotte, Nashville",
                "Tier 5 (Score <40): San Francisco, New York, Los Angeles, Boston, Seattle",
            ],
            "deployment_timeline": {
                "phase_1_data_collection": (
                    "Months 1-3: Assemble parcel data, permit records, cultural asset "
                    "inventories, funding landscape maps, and policy audits for all 50 cities "
                    "using public data sources, FOIA requests, and partner networks."
                ),
                "phase_2_scoring_calibration": (
                    "Months 4-5: Apply scoring algorithm; calibrate weights using Philadelphia "
                    "and Detroit as validated baselines; peer-review methodology with urban "
                    "planning academics at Penn, MIT, and Michigan."
                ),
                "phase_3_visualization": (
                    "Month 6: Build interactive radar chart dashboard; generate city-specific "
                    "profile pages with archetype classification, dimension breakdowns, and "
                    "peer comparison views."
                ),
                "phase_4_publication": (
                    "Month 7: Publish index as open-access report and interactive web tool; "
                    "present at National League of Cities conference; distribute to municipal "
                    "partners and philanthropic funders."
                ),
            },
            "cost_to_replicate": {
                "data_collection_and_research": "$180,000 — research staff, data licensing, FOIA costs",
                "algorithm_development": "$60,000 — data science and calibration",
                "visualization_and_web_tool": "$75,000 — design, development, hosting",
                "publication_and_outreach": "$35,000 — report design, conference presentations, media",
                "total_estimated": "$350,000 for complete index development",
            },
            "success_metrics": [
                "Index methodology peer-reviewed and validated by 3+ academic institutions",
                "50 city profiles published within 8 months of project launch",
                "Interactive tool receives 10,000+ unique visitors in first 6 months",
                "At least 10 cities proactively reach out for SPHERES engagement after publication",
                "Index cited in at least 5 municipal planning documents within 18 months",
                "Archetype classification adopted by at least 2 national urban policy organizations",
            ],
        },
        "tags": ["ranking", "index", "radar-chart", "archetypes", "national-scaling", "top-50"],
    },
    # ------------------------------------------------------------------
    # 5. Sphere Academy: City Training Program
    # ------------------------------------------------------------------
    {
        "title": "Sphere Academy: City Training Program",
        "summary": (
            "A six-week intensive training program that graduates 30 municipal "
            "employees per cohort, equipping them to independently identify, design, "
            "activate, and sustain transformed public spaces using the SPHERES "
            "methodology.  Graduates receive certification and join an alumni network "
            "for ongoing peer support.  First cohorts are scheduled for Philadelphia, "
            "Detroit, and Baltimore — the three highest-readiness cities."
        ),
        "category": "training-program",
        "impact_level": 4,
        "feasibility": 4,
        "novelty": 4,
        "time_horizon": "near",
        "status": "approved",
        "details": {
            "target_cities": [
                "Philadelphia (first cohort — Q1)",
                "Detroit (second cohort — Q2)",
                "Baltimore (third cohort — Q3)",
                "Cleveland, St. Louis, Pittsburgh (Year 2 expansion)",
            ],
            "deployment_timeline": {
                "curriculum_design": (
                    "Months 1-2: Develop 6-week curriculum with modular units covering "
                    "site identification, community co-design, permit navigation, "
                    "activation programming, IoT deployment, and impact measurement."
                ),
                "pilot_cohort_philadelphia": (
                    "Month 3: Deliver pilot cohort in Philadelphia with 30 city staff "
                    "from Land Bank, Parks & Recreation, Commerce, and Planning; "
                    "incorporate hands-on field work at active SPHERES sites."
                ),
                "detroit_cohort": (
                    "Month 5: Deliver Detroit cohort with DLBA staff, Mayor's Office "
                    "of Neighborhoods, and community development corporation leaders; "
                    "customize case studies for Detroit's inventory-rich context."
                ),
                "baltimore_cohort": (
                    "Month 7: Deliver Baltimore cohort; partner with Baltimore Housing "
                    "Authority and Vacants to Value program; adapt curriculum for "
                    "Baltimore's unique rowhouse vacancy challenges."
                ),
                "certification_launch": (
                    "Month 8: Launch formal SPHERES Activator Certification; establish "
                    "alumni network; begin planning Year 2 expansion cohorts."
                ),
            },
            "cost_to_replicate": {
                "curriculum_development": "$95,000 — instructional design, materials, case studies",
                "instructor_team": "$120,000 — 2 lead instructors + 1 coordinator for Year 1",
                "venue_and_logistics": "$45,000 — per-cohort space, meals, printed materials",
                "certification_infrastructure": "$25,000 — assessment platform, credentials, alumni portal",
                "total_estimated": "$285,000 for three-cohort first year",
            },
            "success_metrics": [
                "90 city employees trained across 3 cities in Year 1 (30 per cohort)",
                "85% of graduates launch at least one space activation within 6 months of certification",
                "Post-training competency assessment pass rate >= 90%",
                "Net Promoter Score >= 65 among graduates",
                "At least 2 cities integrate SPHERES curriculum into ongoing municipal professional development",
                "Alumni network achieves 70%+ active participation rate in first year",
            ],
        },
        "tags": ["academy", "training", "certification", "municipal-staff", "capacity-building"],
    },
    # ------------------------------------------------------------------
    # 6. Sister City Sphere Exchange
    # ------------------------------------------------------------------
    {
        "title": "Sister City Sphere Exchange",
        "summary": (
            "An international exchange program pairing Philadelphia with cities "
            "worldwide that face analogous public space and vacancy challenges.  "
            "Partner cities — Medellín (Colombia), Liverpool (UK), Leipzig (Germany), "
            "and Kigali (Rwanda) — each bring unique innovations in community-led "
            "urban transformation.  The program enables cross-pollination of ideas, "
            "joint pilot projects, and an annual rotating summit that builds a global "
            "movement around public space activation."
        ),
        "category": "international-exchange",
        "impact_level": 5,
        "feasibility": 2,
        "novelty": 5,
        "time_horizon": "far",
        "status": "review",
        "details": {
            "target_cities": [
                "Medellín, Colombia — pioneered social urbanism and escalator-connected hillside comunas",
                "Liverpool, UK — transformed post-industrial decline through culture-led regeneration",
                "Leipzig, Germany — turned mass vacancy into artist-led neighborhood revival (Plagwitz model)",
                "Kigali, Rwanda — rapid urbanization with community-driven public space creation (umuganda tradition)",
            ],
            "deployment_timeline": {
                "year_1_foundations": (
                    "Establish bilateral MOUs with each partner city; identify 2 exchange "
                    "delegates per city; conduct virtual introductory workshops to map "
                    "each city's innovations, challenges, and assets."
                ),
                "year_2_exchanges": (
                    "Deploy 2-week immersive exchange visits: Philadelphia staff visit "
                    "each partner city and vice versa; document transferable innovations; "
                    "launch 1 joint pilot project per city pair."
                ),
                "year_3_summit": (
                    "Host inaugural annual Sister City Sphere Summit in Philadelphia; "
                    "present joint pilot results; sign multilateral cooperation framework; "
                    "publish open-access 'Global Playbook for Public Space Activation'."
                ),
                "year_4_plus_scaling": (
                    "Rotate summit to Medellín (Year 4), Liverpool (Year 5), Leipzig "
                    "(Year 6), Kigali (Year 7); expand network to 3 additional cities; "
                    "establish permanent secretariat and shared innovation fund."
                ),
            },
            "cost_to_replicate": {
                "partnership_development": "$80,000 — legal, translation, relationship building",
                "exchange_visits": "$200,000/year — travel, lodging, per diem for 10 delegates x 4 trips",
                "joint_pilot_projects": "$150,000/year — seed funding for 4 bilateral pilots",
                "annual_summit": "$120,000 — venue, logistics, simultaneous translation, media",
                "secretariat_operations": "$100,000/year — 1 FTE coordinator + administrative costs",
                "total_estimated": "$650,000 for Year 1; $570,000/year ongoing",
            },
            "success_metrics": [
                "MOUs signed with all 4 partner cities within 12 months",
                "At least 8 transferable innovations documented from exchange visits",
                "4 joint pilot projects launched (1 per city pair) by end of Year 2",
                "Annual summit attracts 150+ attendees from 10+ countries by Year 3",
                "At least 2 innovations from partner cities successfully adapted to Philadelphia context",
                "Global Playbook downloaded 5,000+ times within 12 months of publication",
                "Network expanded to 8+ cities by Year 5",
            ],
        },
        "tags": ["international", "sister-city", "exchange", "global", "cross-pollination", "summit"],
    },
]

# ---------------------------------------------------------------------------
# Generator Templates — 8 patterns the AI can use to create new innovations
# ---------------------------------------------------------------------------

TEMPLATES: list[dict] = [
    {
        "title": "City Partnership Agreement Generator",
        "summary": (
            "Template for generating formal partnership agreements between "
            "Philadelphia SPHERES and a target city, including governance "
            "structure, resource sharing, and mutual obligations."
        ),
        "category": "city-partnership",
        "time_horizon": "medium",
        "impact_range": [3, 5],
        "feasibility_range": [2, 4],
        "novelty_range": [2, 4],
        "details": {
            "target_cities": [
                "Detroit", "Baltimore", "St. Louis", "Cleveland",
                "Camden NJ", "Newark NJ", "Pittsburgh", "Gary IN",
            ],
            "partnership_components": [
                "Memorandum of understanding template",
                "Data sharing and privacy agreement",
                "Joint intellectual property framework",
                "Resource exchange protocol",
                "Dispute resolution mechanism",
            ],
            "adaptation_requirements": (
                "Each agreement must be reviewed by local municipal counsel, "
                "adapted to state-specific contract law, and approved by the "
                "relevant city council or authorizing body."
            ),
            "success_metrics": [
                "Agreement executed within 60 days of initial contact",
                "Both parties report positive ROI within 12 months",
                "At least 2 joint projects initiated per partnership per year",
            ],
        },
        "tags": ["partnership", "agreement", "governance", "legal", "template"],
    },
    {
        "title": "Vacant Lot Inventory Adaptation Module",
        "summary": (
            "Template for adapting Philadelphia's lot scoring and prioritization "
            "algorithms to a new city's parcel data, zoning codes, and "
            "community needs assessment framework."
        ),
        "category": "replication-playbook",
        "time_horizon": "near",
        "impact_range": [3, 5],
        "feasibility_range": [3, 5],
        "novelty_range": [2, 4],
        "details": {
            "data_requirements": [
                "Municipal parcel database with ownership and tax status",
                "GIS shapefiles or GeoJSON for lot boundaries",
                "Zoning and land use classification codes",
                "Environmental assessment records (brownfield status)",
                "Community survey data on neighborhood priorities",
            ],
            "scoring_algorithm_inputs": [
                "Lot size and geometry",
                "Proximity to existing community assets",
                "Environmental contamination risk level",
                "Ownership complexity (single owner vs. tax lien vs. city-owned)",
                "Neighborhood activation readiness score",
            ],
            "deployment_timeline": (
                "2-4 weeks per city: data ingestion, schema mapping, algorithm "
                "calibration, stakeholder review, and validation against known sites."
            ),
        },
        "tags": ["vacant-lots", "data", "scoring", "GIS", "prioritization"],
    },
    {
        "title": "Community Engagement Localization Kit",
        "summary": (
            "Template for adapting SPHERES community engagement strategies to "
            "local cultural contexts, languages, trust dynamics, and existing "
            "civic participation infrastructure."
        ),
        "category": "replication-playbook",
        "time_horizon": "near",
        "impact_range": [4, 5],
        "feasibility_range": [3, 5],
        "novelty_range": [3, 4],
        "details": {
            "localization_dimensions": [
                "Language and dialect adaptation",
                "Cultural event calendar integration",
                "Trust-building protocols for historically disinvested communities",
                "Local media and communication channel mapping",
                "Faith-based and civic organization partnership templates",
            ],
            "engagement_methods": [
                "Door-to-door canvassing with translated materials",
                "Community kitchen and block party activation events",
                "Youth ambassador programs with local schools",
                "Digital engagement through neighborhood social platforms",
                "Pop-up design charrettes at existing community gathering spots",
            ],
            "success_metrics": [
                "Community participation rate >= 15% of target neighborhood population",
                "Demographic representation within 10% of neighborhood census data",
                "Trust index improvement of 20%+ over baseline within 6 months",
            ],
        },
        "tags": ["community-engagement", "localization", "culture", "trust", "outreach"],
    },
    {
        "title": "Municipal Staff Training Curriculum Builder",
        "summary": (
            "Template for generating customized training curricula for city "
            "employees based on their department, role, existing competencies, "
            "and the specific activation strategies being deployed."
        ),
        "category": "training-program",
        "time_horizon": "near",
        "impact_range": [3, 5],
        "feasibility_range": [3, 5],
        "novelty_range": [3, 4],
        "details": {
            "curriculum_modules": [
                "Public Space Activation Fundamentals (8 hours)",
                "Community Engagement and Co-Design (12 hours)",
                "Technology Platform Operations (8 hours)",
                "Impact Measurement and Reporting (6 hours)",
                "Maintenance and Long-Term Stewardship (6 hours)",
                "Legal and Regulatory Navigation (4 hours)",
            ],
            "role_specific_tracks": [
                "City Planners: zoning flexibility, design review, permit streamlining",
                "Land Bank Staff: lot disposition, community transfer, liability management",
                "Parks and Recreation: programming, maintenance, volunteer coordination",
                "Community Development: grant writing, CDC partnerships, economic impact",
            ],
            "delivery_formats": [
                "In-person intensive (6 weeks, 2 days/week)",
                "Hybrid with self-paced online modules and weekly live sessions",
                "Train-the-trainer certification for local ongoing delivery",
            ],
        },
        "tags": ["training", "curriculum", "municipal", "capacity-building", "certification"],
    },
    {
        "title": "Cross-City Innovation Exchange Protocol",
        "summary": (
            "Template for structuring regular innovation exchanges between "
            "partner cities — sharing what works, what fails, and what adapts "
            "across different urban contexts."
        ),
        "category": "city-partnership",
        "time_horizon": "medium",
        "impact_range": [3, 5],
        "feasibility_range": [3, 4],
        "novelty_range": [3, 5],
        "details": {
            "exchange_formats": [
                "Quarterly virtual innovation showcases (2 hours each)",
                "Annual in-person summit rotating among member cities",
                "Monthly innovation digest newsletter with case studies",
                "Peer city visits: 3-day immersive exchanges between staff",
                "Shared Slack workspace for real-time troubleshooting",
            ],
            "knowledge_management": [
                "Innovation registry with standardized documentation",
                "Failure log: structured post-mortems on what did not work",
                "Adaptation tracker: how innovations change across contexts",
                "Cost-benefit database with normalized comparison metrics",
            ],
            "governance": (
                "Rotating chair among member cities; decisions by simple majority; "
                "each city contributes $10,000/year to shared operations fund; "
                "innovations shared under Creative Commons BY-SA license."
            ),
        },
        "tags": ["innovation-exchange", "knowledge-sharing", "peer-learning", "network", "summit"],
    },
    {
        "title": "Replication Cost Estimator and Funding Mapper",
        "summary": (
            "Template for generating city-specific cost estimates for SPHERES "
            "deployment and mapping available funding sources including federal "
            "grants, state programs, and local philanthropic capital."
        ),
        "category": "replication-playbook",
        "time_horizon": "near",
        "impact_range": [3, 4],
        "feasibility_range": [4, 5],
        "novelty_range": [2, 4],
        "details": {
            "cost_categories": [
                "Site preparation and environmental remediation",
                "Modular infrastructure and hardware procurement",
                "Technology platform deployment and configuration",
                "Staff hiring, training, and first-year salaries",
                "Community engagement programming and events",
                "Legal, insurance, and administrative overhead",
            ],
            "funding_sources": [
                "HUD Community Development Block Grants (CDBG)",
                "EPA Brownfields Program grants",
                "USDA Community Facilities Direct Loan and Grant Program",
                "State-level land bank and blight remediation funds",
                "Local community foundations and United Way chapters",
                "Corporate sponsorship and naming rights revenue",
            ],
            "estimation_methodology": (
                "Base cost model from Philadelphia pilot adjusted by local cost-of-living "
                "index, lot condition severity score, and existing infrastructure "
                "availability; Monte Carlo simulation for risk-adjusted projections."
            ),
        },
        "tags": ["cost-estimation", "funding", "grants", "financial-planning", "budgeting"],
    },
    {
        "title": "Climate and Ecology Adaptation Framework",
        "summary": (
            "Template for adjusting SPHERES spatial designs and programming to "
            "local climate zones, native plant ecosystems, stormwater management "
            "requirements, and seasonal activity patterns."
        ),
        "category": "replication-playbook",
        "time_horizon": "medium",
        "impact_range": [3, 5],
        "feasibility_range": [3, 4],
        "novelty_range": [3, 5],
        "details": {
            "climate_variables": [
                "USDA hardiness zone and frost-free season length",
                "Annual precipitation and stormwater management requirements",
                "Extreme heat days and urban heat island intensity",
                "Snow load and winter maintenance considerations",
                "Growing season length and viable crop/plant selections",
            ],
            "ecological_design_elements": [
                "Native plant palette builder by ecoregion",
                "Pollinator habitat corridor integration",
                "Stormwater bioretention and rain garden sizing calculators",
                "Urban tree canopy gap analysis and planting plans",
                "Soil remediation protocols for formerly industrial lots",
            ],
            "seasonal_programming": (
                "Year-round activation calendar adjusted for local climate: "
                "winter warming stations and indoor pop-ups for cold climates; "
                "shade structures and misting stations for summer heat; "
                "rain-resilient event planning for high-precipitation zones."
            ),
        },
        "tags": ["climate", "ecology", "native-plants", "stormwater", "seasonal"],
    },
    {
        "title": "Political Champion Cultivation Playbook",
        "summary": (
            "Template for identifying, engaging, and supporting political "
            "champions at city council, mayoral, and state legislative levels "
            "who will advocate for public space activation policy and funding."
        ),
        "category": "city-partnership",
        "time_horizon": "medium",
        "impact_range": [4, 5],
        "feasibility_range": [2, 4],
        "novelty_range": [3, 5],
        "details": {
            "champion_identification": [
                "Voting record analysis on land use, parks, and housing bills",
                "Committee membership mapping (housing, environment, budget)",
                "Campaign platform keyword analysis for alignment",
                "Constituent complaint data to identify sympathetic districts",
                "Social network analysis of council relationships and influence",
            ],
            "engagement_strategy": [
                "Private briefing with data visualization of local lot inventory",
                "Constituent tour of activated spaces in Philadelphia",
                "Co-branded press event at first local activation site",
                "Policy brief ghostwriting service for champion's office",
                "Regular impact report delivered to champion for public use",
            ],
            "sustainability": (
                "Build bipartisan support by framing public space activation as "
                "both economic development (conservative appeal) and environmental "
                "justice (progressive appeal); cultivate champions across party "
                "lines to survive electoral transitions; embed policy wins in "
                "ordinance rather than executive order for durability."
            ),
        },
        "tags": ["political-strategy", "advocacy", "champions", "policy", "coalition-building"],
    },
]
