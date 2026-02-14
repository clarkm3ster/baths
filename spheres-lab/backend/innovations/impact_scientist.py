"""
SPHERES Innovation Laboratory — Impact Scientist domain.

Rigorous impact measurement: SROI calculators, health outcome trackers,
property value analyses, community wellbeing indices, environmental metrics.

All innovations are grounded in Philadelphia-specific research, including
peer-reviewed studies from Penn Medicine, the Philadelphia LandCare program,
and the CDC's PLACES dataset for community health.
"""

# ---------------------------------------------------------------------------
# Seed innovations — 6 validated impact-science tools
# ---------------------------------------------------------------------------

INNOVATIONS: list[dict] = [
    # ------------------------------------------------------------------
    # 1. Space Activation SROI Calculator
    # ------------------------------------------------------------------
    {
        "title": "Space Activation SROI Calculator",
        "summary": (
            "A social return on investment model that quantifies the full "
            "economic and social value generated per dollar invested in "
            "vacant lot transformations across Philadelphia."
        ),
        "category": "sroi-model",
        "impact_level": 5,
        "feasibility": 4,
        "novelty": 4,
        "time_horizon": "near",
        "status": "approved",
        "details": {
            "methodology": (
                "Cost-benefit analysis using the New Economics Foundation "
                "SROI framework adapted for urban land activation. Inputs "
                "include direct program costs, volunteer labor valuation "
                "(Independent Sector rate), avoided municipal costs "
                "(illegal dumping cleanup, emergency medical services), "
                "and monetized health and safety outcomes. Discount rate "
                "of 3.5% applied over a 10-year projection window."
            ),
            "data_sources": [
                "Philadelphia LandCare program cost records",
                "City of Philadelphia 311 illegal-dumping complaints",
                "Penn Medicine emergency department visit data",
                "Bureau of Labor Statistics wage data for volunteer valuation",
                "Philadelphia Office of Property Assessment (OPA) records",
            ],
            "measurement_frequency": "quarterly",
            "statistical_model": (
                "Propensity-score-matched difference-in-differences "
                "comparing treated lots to control lots within the same "
                "census tract. Bootstrap confidence intervals (n=1000) "
                "for SROI ratio estimates."
            ),
            "baseline_metrics": {
                "avg_activation_cost_per_lot": 1600,
                "estimated_sroi_ratio": 6.2,
                "municipal_cost_avoidance_per_lot_year": 980,
                "volunteer_hours_monetized_per_lot_year": 2400,
            },
            "peer_reviewed_basis": (
                "Branas et al. (2018) 'Citywide cluster randomized trial "
                "to restore blighted vacant land and its effects on "
                "violence, crime, and safety,' PNAS 115(12)."
            ),
        },
        "tags": ["sroi", "cost-benefit", "landcare", "economic-valuation", "vacant-lots"],
    },
    # ------------------------------------------------------------------
    # 2. Green Space Health Index
    # ------------------------------------------------------------------
    {
        "title": "Green Space Health Index",
        "summary": (
            "A composite health outcome tracker that monitors asthma "
            "hospitalization rates, depression screening scores, and "
            "physical activity levels within a 1/4-mile radius of "
            "activated green spaces."
        ),
        "category": "health-outcomes",
        "impact_level": 5,
        "feasibility": 3,
        "novelty": 4,
        "time_horizon": "medium",
        "status": "approved",
        "details": {
            "methodology": (
                "Interrupted time-series analysis with seasonal adjustment "
                "tracking three health domains: respiratory (pediatric "
                "asthma ED visits), mental health (PHQ-9 screening via "
                "partner clinics), and physical activity (accelerometer "
                "sub-sample plus self-report IPAQ). Health index is a "
                "weighted z-score composite normalized to a 0-100 scale."
            ),
            "data_sources": [
                "Pennsylvania Health Care Cost Containment Council (PHC4) "
                "hospitalization data",
                "CDC PLACES dataset — census-tract-level health estimates",
                "Philadelphia Department of Public Health asthma surveillance",
                "Partner clinic PHQ-9 depression screens (Jefferson Health, "
                "Penn Medicine community health centers)",
                "Fitbit/accelerometer sub-cohort (n=200 per activation site)",
            ],
            "measurement_frequency": "monthly",
            "sample_size": (
                "Target 500 residents per activation site; 12 treatment "
                "sites and 12 matched control sites in Year 1."
            ),
            "statistical_model": (
                "Bayesian structural time-series (CausalImpact framework) "
                "with pre-intervention window of 24 months and "
                "post-intervention tracking of 36 months. Hierarchical "
                "random effects for census tract."
            ),
            "baseline_metrics": {
                "pediatric_asthma_ed_rate_per_10k": 142,
                "avg_phq9_score_target_tracts": 8.7,
                "pct_meeting_physical_activity_guidelines": 38,
                "expected_asthma_reduction_pct": 15,
            },
            "peer_reviewed_basis": (
                "Kondo et al. (2018) 'Effects of greening vacant lots on "
                "health: A randomised controlled trial,' Lancet Planetary "
                "Health 2(1); South et al. (2015) 'Neighborhood blight, "
                "stress, and health,' AJPH 105(7)."
            ),
        },
        "tags": ["health", "asthma", "mental-health", "physical-activity", "epidemiology"],
    },
    # ------------------------------------------------------------------
    # 3. Property Value Uplift Tracker
    # ------------------------------------------------------------------
    {
        "title": "Property Value Uplift Tracker",
        "summary": (
            "Real-time monitoring system that measures residential property "
            "value changes within 500 feet of SPHERES lot activations, "
            "isolating the causal uplift from confounding market trends."
        ),
        "category": "property-analysis",
        "impact_level": 4,
        "feasibility": 4,
        "novelty": 3,
        "time_horizon": "near",
        "status": "approved",
        "details": {
            "methodology": (
                "Hedonic pricing model with spatial lag using Philadelphia "
                "OPA assessed values and arms-length sales. Treatment "
                "boundary set at 500 ft from lot centroid with concentric "
                "ring controls at 500-1000 ft and 1000-1500 ft. Spatial "
                "fixed effects at the block-group level to absorb "
                "neighborhood-wide trends."
            ),
            "data_sources": [
                "Philadelphia OPA certified property assessments (annual)",
                "Zillow Transaction and Assessment Dataset (ZTRAX)",
                "Philadelphia Licenses & Inspections permits",
                "SPHERES activation dates and investment amounts",
                "U.S. Census ACS 5-year block-group demographics",
            ],
            "measurement_frequency": "quarterly",
            "sample_size": (
                "Full universe of residential parcels within 1500 ft "
                "of each activation (~800-1200 parcels per site)."
            ),
            "statistical_model": (
                "Spatial difference-in-differences with inverse-distance "
                "weighting kernel. Conley standard errors to account "
                "for spatial autocorrelation. Robustness checks via "
                "repeat-sales index for properties transacting pre- "
                "and post-activation."
            ),
            "baseline_metrics": {
                "avg_assessed_value_target_tracts": 78500,
                "expected_uplift_pct_500ft": 5.4,
                "expected_uplift_pct_1000ft": 2.1,
                "landcare_documented_uplift": 5.0,
            },
            "peer_reviewed_basis": (
                "Wachter et al. (2010) 'Determinants of outcomes in the "
                "Philadelphia LandCare program,' Penn IUR; Branas et al. "
                "(2011) 'A difference-in-differences analysis of health, "
                "safety, and greening vacant urban space,' AJE 174(11)."
            ),
        },
        "tags": ["property-values", "hedonic-model", "real-estate", "spatial-analysis", "OPA"],
    },
    # ------------------------------------------------------------------
    # 4. Community Wellbeing Dashboard
    # ------------------------------------------------------------------
    {
        "title": "Community Wellbeing Dashboard",
        "summary": (
            "A composite neighborhood wellbeing index combining safety, "
            "social cohesion, health, and economic vitality indicators "
            "at the census-tract level for every SPHERES activation zone."
        ),
        "category": "wellbeing-index",
        "impact_level": 4,
        "feasibility": 3,
        "novelty": 5,
        "time_horizon": "medium",
        "status": "approved",
        "details": {
            "methodology": (
                "Four-domain composite index using principal component "
                "analysis to derive domain weights. Domains: (1) Safety — "
                "violent crime rate, 911 call density, perceived safety "
                "survey; (2) Social Cohesion — neighboring behavior scale, "
                "event attendance, voter turnout; (3) Health — GSHI score, "
                "life expectancy, insurance coverage; (4) Economic — "
                "median household income, business starts, employment "
                "rate. Each domain normalized to 0-100, overall index "
                "is the PCA-weighted mean."
            ),
            "data_sources": [
                "Philadelphia Police Department incident data (OpenDataPhilly)",
                "SPHERES community survey instrument (administered bi-annually)",
                "CDC PLACES and RWJF County Health Rankings",
                "U.S. Census ACS 1-year and 5-year estimates",
                "Philadelphia Commerce Department business license data",
                "Philadelphia City Commissioners voter file",
            ],
            "measurement_frequency": "semi-annual",
            "sample_size": (
                "Community survey: 300 respondents per activation zone "
                "(stratified random sample by age, race, tenure). "
                "Administrative data covers full census tract populations."
            ),
            "statistical_model": (
                "Confirmatory factor analysis to validate four-domain "
                "structure. Change scores analyzed via multilevel growth "
                "models (residents nested in tracts nested in activation "
                "cohorts). Pre-registered analysis plan on OSF."
            ),
            "baseline_metrics": {
                "avg_composite_index_target_tracts": 42,
                "safety_domain_avg": 35,
                "social_cohesion_domain_avg": 48,
                "health_domain_avg": 40,
                "economic_domain_avg": 45,
            },
            "peer_reviewed_basis": (
                "Alaimo et al. (2010) 'Community gardening, neighborhood "
                "meetings, and social capital,' J Community Practice "
                "18(1); Kuo & Sullivan (2001) 'Environment and crime "
                "in the inner city,' Environment and Behavior 33(3)."
            ),
        },
        "tags": [
            "wellbeing", "composite-index", "safety", "social-cohesion",
            "dashboard", "pca",
        ],
    },
    # ------------------------------------------------------------------
    # 5. Environmental Benefit Quantifier
    # ------------------------------------------------------------------
    {
        "title": "Environmental Benefit Quantifier",
        "summary": (
            "Measures the ecological services produced by activated lots "
            "including carbon sequestration, stormwater absorption, and "
            "urban heat island reduction using remote sensing and "
            "ground-truth sampling."
        ),
        "category": "environmental-metrics",
        "impact_level": 4,
        "feasibility": 3,
        "novelty": 4,
        "time_horizon": "medium",
        "status": "approved",
        "details": {
            "methodology": (
                "Ecosystem services valuation following the i-Tree Eco "
                "model (USDA Forest Service) for tree canopy and the "
                "EPA Green Infrastructure modeling toolkit for stormwater. "
                "Carbon sequestration estimated via allometric biomass "
                "equations for planted species. Heat island effect "
                "measured by Landsat 8/9 thermal band surface temperature "
                "differentials between activated and control lots. "
                "Monetary values assigned using EPA social cost of carbon "
                "($51/ton) and Philadelphia Water Department green "
                "stormwater credit rates."
            ),
            "data_sources": [
                "USDA i-Tree Eco field survey protocol",
                "Landsat 8/9 thermal infrared imagery (30m resolution)",
                "Philadelphia Water Department stormwater billing data",
                "EPA SWMM stormwater runoff model outputs",
                "NOAA weather station data (Philadelphia International Airport)",
            ],
            "measurement_frequency": "seasonal (quarterly)",
            "sample_size": (
                "Ground-truth measurements at all activation sites; "
                "remote sensing covers full city extent for comparison. "
                "Minimum 20 soil cores per site for infiltration testing."
            ),
            "statistical_model": (
                "Mixed-effects regression of surface temperature on "
                "NDVI change with spatial random effects. Stormwater "
                "volume modeled via curve-number method calibrated "
                "to Philadelphia soils (hydrologic group C/D). "
                "Monte Carlo uncertainty propagation for carbon "
                "estimates (10,000 iterations)."
            ),
            "baseline_metrics": {
                "avg_surface_temp_reduction_celsius": 1.8,
                "stormwater_gallons_absorbed_per_lot_year": 45000,
                "carbon_sequestered_tons_per_lot_year": 0.35,
                "ecosystem_services_dollar_value_per_lot_year": 2800,
            },
            "peer_reviewed_basis": (
                "Nowak et al. (2014) 'Tree and forest effects on air "
                "quality and human health in the United States,' "
                "Environmental Pollution 193; Livesley et al. (2016) "
                "'The Urban Forest and Ecosystem Services,' Springer."
            ),
        },
        "tags": [
            "environment", "carbon", "stormwater", "heat-island",
            "ecosystem-services", "remote-sensing",
        ],
    },
    # ------------------------------------------------------------------
    # 6. Violence Reduction Mapper
    # ------------------------------------------------------------------
    {
        "title": "Violence Reduction Mapper",
        "summary": (
            "Geospatial analysis tool that correlates SPHERES lot greening "
            "interventions with reductions in gun violence incidents by "
            "census tract, building on Penn's proven research methodology."
        ),
        "category": "safety-analysis",
        "impact_level": 5,
        "feasibility": 4,
        "novelty": 3,
        "time_horizon": "near",
        "status": "approved",
        "details": {
            "methodology": (
                "Replication and extension of the Branas et al. (2018) "
                "cluster-randomized trial design. Shootings and aggravated "
                "assaults geocoded to 100-ft accuracy and aggregated to "
                "census-tract-month panels. Intent-to-treat analysis with "
                "Poisson regression controlling for tract-level poverty, "
                "vacancy rates, and seasonal fixed effects. Dose-response "
                "curve estimated by number of lots treated per tract."
            ),
            "data_sources": [
                "Philadelphia Police Department shooting victims database "
                "(OpenDataPhilly)",
                "Penn Injury Science Center geocoded violence data",
                "SPHERES lot activation registry with GPS coordinates",
                "U.S. Census ACS tract-level poverty and vacancy rates",
                "Philadelphia Managing Director's Office 311 data",
            ],
            "measurement_frequency": "monthly",
            "sample_size": (
                "All census tracts containing SPHERES activations "
                "(estimated 40+ tracts by Year 2) with 1:2 matched "
                "control tracts using Mahalanobis distance on baseline "
                "crime rate, poverty, and racial composition."
            ),
            "statistical_model": (
                "Conditional Poisson fixed-effects model with tract and "
                "month-year fixed effects. Spatial Durbin specification "
                "to capture spillover effects into adjacent tracts. "
                "Synthetic control method as robustness check for "
                "high-activation tracts."
            ),
            "baseline_metrics": {
                "avg_shootings_per_tract_year_target": 8.4,
                "expected_reduction_pct_per_lot_treated": 4.5,
                "branas_trial_documented_reduction_pct": 29,
                "spillover_radius_meters": 500,
            },
            "peer_reviewed_basis": (
                "Branas et al. (2018) PNAS 115(12); Moyer et al. (2019) "
                "'Effect of remediating blighted vacant land on shootings,' "
                "American Journal of Public Health 109(1); South et al. "
                "(2018) 'Effect of greening vacant land on mental health,' "
                "JAMA Network Open 1(3)."
            ),
        },
        "tags": [
            "violence-reduction", "gun-violence", "spatial-analysis",
            "public-safety", "lot-greening", "quasi-experimental",
        ],
    },
]


# ---------------------------------------------------------------------------
# Generator templates — 8 parameterized patterns for AI-generated innovations
# ---------------------------------------------------------------------------

TEMPLATES: list[dict] = [
    # ------------------------------------------------------------------
    # T1. Longitudinal Cohort Health Study
    # ------------------------------------------------------------------
    {
        "title": "Longitudinal Cohort Health Study: {health_domain}",
        "summary": (
            "Multi-year prospective cohort study tracking {health_domain} "
            "outcomes among residents living near SPHERES-activated lots "
            "versus matched controls in non-activated neighborhoods."
        ),
        "category": "health-outcomes",
        "time_horizon": "far",
        "impact_range": [4, 5],
        "feasibility_range": [2, 3],
        "novelty_range": [4, 5],
        "details": {
            "methodology": (
                "Prospective cohort design with baseline enrollment at "
                "activation onset. Annual biomarker collection (cortisol, "
                "HbA1c, BMI), validated survey instruments, and EHR "
                "linkage via partner health systems."
            ),
            "data_sources": [
                "Electronic health records (Penn Medicine, Jefferson Health)",
                "Biomarker collection at community health fairs",
                "CDC Behavioral Risk Factor Surveillance System (BRFSS)",
                "SPHERES activation registry",
            ],
            "measurement_frequency": "annual with quarterly survey touchpoints",
            "statistical_model": (
                "Cox proportional hazards for time-to-event outcomes; "
                "generalized estimating equations for repeated measures. "
                "Inverse probability of treatment weighting to adjust "
                "for selection into activated neighborhoods."
            ),
            "peer_reviewed_basis": (
                "Study protocol modeled on the Jackson Heart Study "
                "and the Philadelphia Collaborative Violence Reduction "
                "initiative longitudinal design."
            ),
        },
        "tags": ["cohort-study", "longitudinal", "health", "biomarkers", "ehr-linkage"],
    },
    # ------------------------------------------------------------------
    # T2. Micro-Economic Multiplier Model
    # ------------------------------------------------------------------
    {
        "title": "Micro-Economic Multiplier Model: {economic_sector}",
        "summary": (
            "Input-output economic model estimating the local multiplier "
            "effect of SPHERES activation spending on {economic_sector} "
            "in surrounding commercial corridors."
        ),
        "category": "sroi-model",
        "time_horizon": "medium",
        "impact_range": [3, 5],
        "feasibility_range": [3, 4],
        "novelty_range": [3, 4],
        "details": {
            "methodology": (
                "Regional input-output model using IMPLAN data for the "
                "Philadelphia MSA. Direct, indirect, and induced effects "
                "estimated for each activation dollar. Consumer spending "
                "surveys in 1/4-mile commercial corridors pre/post "
                "activation."
            ),
            "data_sources": [
                "IMPLAN regional economic model (Philadelphia MSA)",
                "SPHERES procurement and contractor payment records",
                "Philadelphia Commerce Department sales tax receipts",
                "Pedestrian count data from activation-adjacent corridors",
            ],
            "measurement_frequency": "semi-annual",
            "statistical_model": (
                "Leontief inverse matrix for multiplier estimation. "
                "Sensitivity analysis across three scenarios (low, "
                "medium, high local capture rates)."
            ),
            "peer_reviewed_basis": (
                "Weisbrod & Weisbrod (1997) 'Measuring economic impacts "
                "of projects and programs,' Economic Development Research "
                "Group; Philadelphia Federal Reserve community development "
                "working papers."
            ),
        },
        "tags": ["economic-multiplier", "implan", "commercial-corridor", "local-spending"],
    },
    # ------------------------------------------------------------------
    # T3. Equity-Weighted Impact Score
    # ------------------------------------------------------------------
    {
        "title": "Equity-Weighted Impact Score: {equity_dimension}",
        "summary": (
            "An impact scoring framework that applies equity multipliers "
            "based on {equity_dimension} to ensure SPHERES resources flow "
            "disproportionately to Philadelphia's most under-resourced "
            "communities."
        ),
        "category": "wellbeing-index",
        "time_horizon": "near",
        "impact_range": [4, 5],
        "feasibility_range": [3, 5],
        "novelty_range": [4, 5],
        "details": {
            "methodology": (
                "Composite equity index combining CDC Social Vulnerability "
                "Index, Philadelphia percent-below-poverty, tree canopy "
                "coverage deficit, and historical redlining grade (HOLC). "
                "Equity multiplier ranges from 1.0 (low need) to 3.0 "
                "(highest need), applied to all SROI and wellbeing scores."
            ),
            "data_sources": [
                "CDC/ATSDR Social Vulnerability Index (SVI)",
                "University of Richmond Mapping Inequality (HOLC grades)",
                "Philadelphia Parks & Recreation tree canopy assessment",
                "U.S. Census ACS poverty and race/ethnicity data",
            ],
            "measurement_frequency": "annual recalibration",
            "statistical_model": (
                "Rank-based equity weighting using the Atkinson inequality "
                "index with epsilon parameter set via community advisory "
                "board input. Lorenz curve visualization of resource "
                "distribution across deciles."
            ),
            "peer_reviewed_basis": (
                "Atkinson (1970) 'On the measurement of inequality,' "
                "Journal of Economic Theory; Krieger et al. (2020) "
                "'Structural racism, historical redlining, and health,' "
                "AJPH 110(7)."
            ),
        },
        "tags": ["equity", "social-vulnerability", "redlining", "resource-allocation"],
    },
    # ------------------------------------------------------------------
    # T4. Real-Time Sensor Network Impact Feed
    # ------------------------------------------------------------------
    {
        "title": "Real-Time Sensor Network: {sensor_type} Monitoring",
        "summary": (
            "IoT sensor deployment at activation sites providing "
            "continuous {sensor_type} data streams for real-time "
            "impact measurement and public-facing dashboards."
        ),
        "category": "environmental-metrics",
        "time_horizon": "medium",
        "impact_range": [3, 4],
        "feasibility_range": [2, 4],
        "novelty_range": [4, 5],
        "details": {
            "methodology": (
                "Low-cost sensor arrays (PM2.5, temperature/humidity, "
                "soil moisture, noise level, foot traffic) deployed at "
                "activation sites with LoRaWAN connectivity. Data "
                "ingested to time-series database with anomaly detection "
                "and automated reporting."
            ),
            "data_sources": [
                "PurpleAir PM2.5 sensors (community-calibrated)",
                "Custom soil moisture probes (capacitive, 30cm depth)",
                "Infrared pedestrian counters",
                "NOAA reference weather stations for calibration",
            ],
            "measurement_frequency": "continuous (5-minute intervals)",
            "statistical_model": (
                "Change-point detection using PELT algorithm on sensor "
                "time series. Spatial interpolation via ordinary kriging "
                "for neighborhood-level estimates. Sensor drift correction "
                "via co-location with reference instruments."
            ),
            "peer_reviewed_basis": (
                "Morawska et al. (2018) 'Applications of low-cost sensing "
                "technologies for air quality monitoring,' Environment "
                "International 116."
            ),
        },
        "tags": ["iot", "sensors", "real-time", "air-quality", "environmental-monitoring"],
    },
    # ------------------------------------------------------------------
    # T5. Randomized Controlled Trial Protocol
    # ------------------------------------------------------------------
    {
        "title": "Randomized Controlled Trial: {intervention_type} Activation",
        "summary": (
            "Gold-standard RCT protocol for evaluating causal impact of "
            "{intervention_type} space activation on resident outcomes, "
            "designed for peer-reviewed publication and policy influence."
        ),
        "category": "health-outcomes",
        "time_horizon": "far",
        "impact_range": [5, 5],
        "feasibility_range": [2, 3],
        "novelty_range": [3, 5],
        "details": {
            "methodology": (
                "Cluster-randomized trial with census tracts as unit of "
                "randomization. Waitlist control design to ensure all "
                "communities receive intervention. Primary outcomes "
                "assessed by blinded data collectors. Pre-registered "
                "on ClinicalTrials.gov with IRB approval from Penn."
            ),
            "data_sources": [
                "Baseline and follow-up household surveys",
                "Administrative health and crime data (blinded linkage)",
                "Philadelphia OPA property records",
                "Activation fidelity checklists (process evaluation)",
            ],
            "measurement_frequency": "baseline, 6-month, 12-month, 24-month",
            "statistical_model": (
                "Intent-to-treat analysis with generalized linear mixed "
                "models. Intraclass correlation coefficient estimated "
                "from pilot data for power calculation. Minimum detectable "
                "effect size of 0.25 SD with 80% power."
            ),
            "peer_reviewed_basis": (
                "Branas et al. (2018) PNAS cluster-RCT of vacant land "
                "remediation; CONSORT extension for cluster trials."
            ),
        },
        "tags": ["rct", "causal-inference", "clinical-trial", "peer-review", "gold-standard"],
    },
    # ------------------------------------------------------------------
    # T6. Cost-Effectiveness Comparative Analysis
    # ------------------------------------------------------------------
    {
        "title": "Cost-Effectiveness Analysis: {intervention_a} vs {intervention_b}",
        "summary": (
            "Head-to-head cost-effectiveness comparison of "
            "{intervention_a} versus {intervention_b} as space activation "
            "strategies, expressed as cost per QALY gained and cost per "
            "violent crime averted."
        ),
        "category": "sroi-model",
        "time_horizon": "medium",
        "impact_range": [4, 5],
        "feasibility_range": [3, 4],
        "novelty_range": [3, 4],
        "details": {
            "methodology": (
                "Decision-analytic Markov model simulating health and "
                "safety state transitions over a 20-year horizon. "
                "Incremental cost-effectiveness ratio (ICER) computed "
                "against willingness-to-pay threshold of $50,000/QALY. "
                "Probabilistic sensitivity analysis with 10,000 Monte "
                "Carlo iterations."
            ),
            "data_sources": [
                "SPHERES activation cost accounting system",
                "Published effectiveness estimates from Philadelphia trials",
                "EQ-5D utility weights from community survey",
                "Bureau of Justice Statistics cost-of-crime estimates",
            ],
            "measurement_frequency": "annual model update",
            "statistical_model": (
                "Microsimulation with heterogeneous agents varying by "
                "age, gender, baseline health, and neighborhood risk. "
                "Value-of-information analysis to prioritize future "
                "data collection."
            ),
            "peer_reviewed_basis": (
                "Drummond et al. (2015) 'Methods for the Economic "
                "Evaluation of Health Care Programmes,' Oxford; "
                "Sanders et al. (2016) Second Panel on Cost-Effectiveness "
                "in Health and Medicine, JAMA 316(10)."
            ),
        },
        "tags": ["cost-effectiveness", "qaly", "markov-model", "decision-analysis"],
    },
    # ------------------------------------------------------------------
    # T7. Community-Participatory Impact Audit
    # ------------------------------------------------------------------
    {
        "title": "Community-Participatory Impact Audit: {neighborhood}",
        "summary": (
            "Resident-led impact assessment in {neighborhood} using "
            "participatory research methods that center community voice "
            "alongside quantitative metrics to validate and contextualize "
            "SPHERES outcomes."
        ),
        "category": "wellbeing-index",
        "time_horizon": "near",
        "impact_range": [3, 5],
        "feasibility_range": [3, 5],
        "novelty_range": [4, 5],
        "details": {
            "methodology": (
                "Community-based participatory research (CBPR) framework "
                "with resident co-investigators trained in photovoice, "
                "asset mapping, and survey administration. Mixed-methods "
                "design combining resident-collected qualitative data "
                "with administrative quantitative indicators. Findings "
                "validated through community town halls."
            ),
            "data_sources": [
                "Photovoice narratives and thematic coding",
                "Community asset maps (GIS-enabled walking audits)",
                "Resident-administered neighborhood satisfaction surveys",
                "SPHERES quantitative dashboard data for triangulation",
            ],
            "measurement_frequency": "bi-annual audit cycles",
            "statistical_model": (
                "Convergent mixed-methods design with joint display "
                "matrices. Qualitative themes analyzed via grounded "
                "theory; quantitative trends via paired t-tests and "
                "effect sizes. Discordance analysis where qualitative "
                "and quantitative findings diverge."
            ),
            "peer_reviewed_basis": (
                "Israel et al. (2010) 'Community-Based Participatory "
                "Research for Health,' Jossey-Bass; Wang & Burris (1997) "
                "'Photovoice: concept, methodology, and use,' Health "
                "Education & Behavior 24(3)."
            ),
        },
        "tags": [
            "cbpr", "participatory", "photovoice", "community-voice",
            "mixed-methods", "resident-led",
        ],
    },
    # ------------------------------------------------------------------
    # T8. Cross-City Benchmarking Framework
    # ------------------------------------------------------------------
    {
        "title": "Cross-City Benchmarking: Philadelphia vs {comparison_city}",
        "summary": (
            "Standardized benchmarking framework comparing SPHERES impact "
            "metrics in Philadelphia against {comparison_city} to "
            "establish transferable evidence and identify context-dependent "
            "moderators of activation success."
        ),
        "category": "sroi-model",
        "time_horizon": "far",
        "impact_range": [3, 5],
        "feasibility_range": [2, 4],
        "novelty_range": [3, 5],
        "details": {
            "methodology": (
                "Common metrics protocol defining standardized outcome "
                "measures across cities. Meta-analytic framework "
                "combining effect sizes from multiple sites. Moderator "
                "analysis examining how city-level factors (climate, "
                "vacancy rate, demographics, policy environment) "
                "modify intervention effects."
            ),
            "data_sources": [
                "SPHERES standardized outcome reporting system",
                "Partner city administrative data (via data use agreements)",
                "U.S. Census ACS for demographic harmonization",
                "National Land Bank Network vacant lot inventories",
            ],
            "measurement_frequency": "annual cross-city report",
            "statistical_model": (
                "Random-effects meta-analysis with city as the unit. "
                "Meta-regression of effect sizes on city-level moderators. "
                "I-squared heterogeneity statistic to quantify "
                "between-city variation."
            ),
            "peer_reviewed_basis": (
                "Higgins & Green (2011) Cochrane Handbook for Systematic "
                "Reviews; Borenstein et al. (2009) 'Introduction to "
                "Meta-Analysis,' Wiley."
            ),
        },
        "tags": ["benchmarking", "cross-city", "meta-analysis", "replication", "scalability"],
    },
]
