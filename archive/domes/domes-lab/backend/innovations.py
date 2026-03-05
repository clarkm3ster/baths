"""
DOMES Innovation Laboratory — Seed Innovations.

Pre-generated innovations across all 12 domains, representing realistic
breakthrough concepts for person-centered government reform.
"""

import json
from datetime import datetime, timezone, timedelta

from models import Innovation, Teammate

# ── Seed data keyed by teammate slug ────────────────────────────────────────

SEED_INNOVATIONS: dict[str, list[dict]] = {
    # ── 1. Fiscal Alchemist ─────────────────────────────────────────────────
    "fiscal-alchemist": [
        {
            "title": "Braided Benefit Bridge Fund",
            "summary": (
                "A blended capital structure that braids TANF, SNAP E&T, and "
                "Workforce Innovation funds into a single flexible pool, reducing "
                "administrative overhead by 40% while expanding eligibility windows "
                "for transitional employment programs."
            ),
            "category": "blended-finance",
            "impact_level": 5,
            "feasibility": 3,
            "novelty": 4,
            "time_horizon": "medium",
            "status": "review",
            "details": json.dumps({
                "mechanism": "Braided funding pool with unified reporting",
                "funding_sources": ["TANF", "SNAP E&T", "WIOA Title I", "CDBG"],
                "projected_savings": "$2.3M annually per county",
                "legal_basis": "Section 1115 waiver + WIOA flexibility provisions",
                "implementation_steps": [
                    "Secure MOUs across 4 funding agencies",
                    "Design unified cost allocation methodology",
                    "Build integrated reporting dashboard",
                    "Pilot in 3 counties for 18 months",
                ],
            }),
            "tags": "blended-finance,TANF,workforce,cost-reduction",
        },
        {
            "title": "Pay-for-Success Recidivism Reduction Bond",
            "summary": (
                "A social impact bond targeting 30% recidivism reduction through "
                "intensive reentry services. Private investors fund upfront costs; "
                "government repays only upon verified outcome achievement, shifting "
                "financial risk from taxpayers to investors."
            ),
            "category": "social-impact-bonds",
            "impact_level": 5,
            "feasibility": 3,
            "novelty": 3,
            "time_horizon": "medium",
            "status": "approved",
            "details": json.dumps({
                "mechanism": "Pay-for-success contract with independent validation",
                "target_population": "Individuals released from state correctional facilities",
                "outcome_metric": "12-month recidivism rate reduction",
                "projected_roi": "287% social return on investment",
                "bond_structure": {
                    "total_raise": "$12M",
                    "investor_return_cap": "6.5% IRR",
                    "measurement_period": "36 months",
                },
            }),
            "tags": "pay-for-success,recidivism,criminal-justice,impact-bonds",
        },
        {
            "title": "Community Development Micro-TIF Districts",
            "summary": (
                "Micro-scale tax increment financing districts of 2-4 blocks in "
                "disinvested neighborhoods, capturing incremental property tax "
                "revenue to fund hyperlocal infrastructure improvements and small "
                "business grants without displacing existing residents."
            ),
            "category": "tax-increment-financing",
            "impact_level": 4,
            "feasibility": 4,
            "novelty": 4,
            "time_horizon": "near",
            "status": "draft",
            "details": json.dumps({
                "mechanism": "Micro-TIF with community oversight board",
                "district_size": "2-4 city blocks",
                "anti_displacement": [
                    "Community land trust partnership",
                    "Resident right-of-first-refusal",
                    "Affordability covenant on new units",
                ],
                "revenue_projection": "$150K-$400K per district over 10 years",
            }),
            "tags": "TIF,neighborhood-investment,anti-displacement,small-business",
        },
        {
            "title": "CDFI Bridge-to-Benefits Loan Product",
            "summary": (
                "A zero-interest micro-loan product administered through community "
                "development financial institutions that covers household expenses "
                "during the 30-90 day gap between benefit application and first "
                "payment, repaid automatically upon benefit receipt."
            ),
            "category": "community-finance",
            "impact_level": 4,
            "feasibility": 4,
            "novelty": 3,
            "time_horizon": "near",
            "status": "approved",
            "details": json.dumps({
                "mechanism": "Zero-interest bridge loan with automatic repayment",
                "loan_range": "$200-$2,000",
                "repayment": "Automatic deduction from first benefit payment",
                "default_projection": "< 8% based on benefit approval rates",
                "cdfi_partners": "National Federation of CDFIs member institutions",
            }),
            "tags": "CDFI,bridge-loans,benefit-gaps,financial-inclusion",
        },
        {
            "title": "Dome Bonds: Municipal Coordination Savings Bonds",
            "summary": (
                "New class of municipal bonds backed by documented coordination "
                "savings. When DOMES coordination reduces duplicative spending, "
                "verified savings back bond issuance — self-funding infrastructure "
                "for person-centered government."
            ),
            "category": "dome-financing",
            "impact_level": 5,
            "feasibility": 2,
            "novelty": 5,
            "time_horizon": "far",
            "status": "draft",
            "details": json.dumps({
                "financial_model": {
                    "bond_type": "Revenue bond backed by coordination savings",
                    "target_issuance": "$50M initial offering",
                    "coupon_rate": "3.5-4.2% tax-exempt",
                    "term": "20-year maturity",
                },
                "revenue_sources": [
                    "Reduced duplicative assessments ($2.1M/yr per county)",
                    "Eliminated redundant case management ($1.8M/yr)",
                    "Prevented crisis interventions ($3.4M/yr)",
                    "Reduced admin overhead from shared intake ($900K/yr)",
                ],
                "legal_requirements": [
                    "State enabling legislation",
                    "Independent savings verification",
                    "Bond counsel opinion on tax-exempt status",
                    "Credit rating agency engagement (target: A-)",
                ],
                "estimated_cost": "$2M for pilot verification infrastructure",
                "evidence_base": "Hennepin County coordination savings of $8.2M/yr documented 2019-2023",
            }),
            "tags": "dome-bonds,municipal-finance,coordination-savings,self-funding",
        },
        {
            "title": "Person-Centered Budgets: Unified Flexible Spending",
            "summary": (
                "Replace fragmented categorical spending with a single flexible "
                "budget per person. Instead of $4,200 SNAP + $8,400 Medicaid + "
                "$6,000 housing as separate allocations, combine into $18,600 the "
                "individual helps direct."
            ),
            "category": "dome-financing",
            "impact_level": 5,
            "feasibility": 2,
            "novelty": 5,
            "time_horizon": "far",
            "status": "draft",
            "details": json.dumps({
                "mechanism": "Pooled categorical funding with person-directed allocation",
                "current_fragmentation": {
                    "average_programs_per_person": 4.3,
                    "administrative_overhead_rate": "23% of total spending",
                    "duplication_rate": "17% of assessments redundant",
                },
                "implementation_path": [
                    "Phase 1: Shadow budgets (calculate unified amount)",
                    "Phase 2: Flex margins (10% movement between categories)",
                    "Phase 3: Full person-centered budgets for pilot cohort",
                ],
                "estimated_cost": "$1.5M for pilot infrastructure",
                "evidence_base": "UK Personal Budgets: 40% higher satisfaction, similar costs",
            }),
            "tags": "person-centered-budgets,flexible-spending,coordination,dome",
        },
    ],

    # ── 2. Impact Investor ──────────────────────────────────────────────────
    "impact-investor": [
        {
            "title": "Maternal Health Outcomes Bond",
            "summary": (
                "A development impact bond focused on reducing maternal mortality "
                "disparities in underserved communities. Investors fund community "
                "health worker programs and doula services; returns tied to measured "
                "reductions in adverse birth outcomes among Black and Indigenous mothers."
            ),
            "category": "development-impact-bonds",
            "impact_level": 5,
            "feasibility": 3,
            "novelty": 4,
            "time_horizon": "medium",
            "status": "review",
            "details": json.dumps({
                "target_outcome": "35% reduction in severe maternal morbidity",
                "investment_size": "$8.5M",
                "investor_class": "Impact-first institutional investors",
                "measurement": "Claims data analysis + patient-reported outcomes",
                "equity_focus": "Black and Indigenous birthing persons in rural areas",
            }),
            "tags": "maternal-health,equity,development-impact-bond,health-outcomes",
        },
        {
            "title": "ESG-Aligned Government Vendor Scoring",
            "summary": (
                "An ESG (Environmental, Social, Governance) scoring framework for "
                "government procurement that prioritizes vendors demonstrating "
                "measurable social impact, living wages, and environmental "
                "responsibility — creating market incentives for responsible "
                "contracting."
            ),
            "category": "esg-frameworks",
            "impact_level": 4,
            "feasibility": 4,
            "novelty": 3,
            "time_horizon": "near",
            "status": "approved",
            "details": json.dumps({
                "scoring_dimensions": [
                    "Living wage certification",
                    "Local hiring percentages",
                    "Carbon footprint per contract dollar",
                    "Subcontracting to MBE/WBE firms",
                    "Worker safety record",
                ],
                "weight_structure": "40% social, 30% environmental, 30% governance",
                "implementation": "Integrated into existing e-procurement platforms",
            }),
            "tags": "ESG,procurement,responsible-contracting,vendor-scoring",
        },
        {
            "title": "Outcomes-Based Foster Care Financing",
            "summary": (
                "An outcomes-based financing model for foster care that shifts "
                "payment from per-diem bed rates to permanency outcomes — "
                "reunification, adoption, or guardianship within 12 months. "
                "Agencies earn premium payments for faster, more stable placements."
            ),
            "category": "outcomes-based-financing",
            "impact_level": 5,
            "feasibility": 3,
            "novelty": 4,
            "time_horizon": "medium",
            "status": "draft",
            "details": json.dumps({
                "payment_model": "Base rate + outcome premium + stability bonus",
                "target_metrics": [
                    "Time to permanency (months)",
                    "Placement stability (moves per year)",
                    "Child wellbeing index score",
                ],
                "projected_savings": "$4,100 per child per year in system costs",
                "risk_mitigation": "Gradual phase-in with 24-month transition period",
            }),
            "tags": "foster-care,outcomes-based,child-welfare,permanency",
        },
        {
            "title": "Outcomes Marketplace: Coordination Credits Exchange",
            "summary": (
                "Like carbon credits but for coordination savings. Agencies earning "
                "verified savings trade Outcome Credits on a regulated exchange. "
                "Creates market incentives for system integration. 1 Credit = "
                "$1,000 in verified coordination savings."
            ),
            "category": "outcomes-markets",
            "impact_level": 5,
            "feasibility": 2,
            "novelty": 5,
            "time_horizon": "far",
            "status": "draft",
            "details": json.dumps({
                "market_design": {
                    "unit": "1 Outcome Credit = $1,000 verified savings",
                    "verification": "Independent actuarial audit",
                    "trading_platform": "Government-regulated exchange",
                },
                "market_sizing": {
                    "total_addressable": "$740B in means-tested programs",
                    "inefficiency_estimate": "15-23% duplication rate",
                    "initial_market_cap": "$500M in first 5 years",
                },
                "estimated_cost": "$5M for exchange infrastructure",
                "evidence_base": "Carbon credit markets: $851B in 2022",
            }),
            "tags": "outcomes-marketplace,coordination-credits,market-incentives,dome",
        },
    ],

    # ── 3. Data Inventor ────────────────────────────────────────────────────
    "data-inventor": [
        {
            "title": "Cross-System Administrative Data Spine",
            "summary": (
                "A privacy-preserving data linkage infrastructure that connects "
                "records across child welfare, Medicaid, SNAP, housing, and "
                "education systems using hashed identifiers — enabling whole-person "
                "analytics without sharing raw PII between agencies."
            ),
            "category": "data-linkage",
            "impact_level": 5,
            "feasibility": 3,
            "novelty": 4,
            "time_horizon": "medium",
            "status": "review",
            "details": json.dumps({
                "architecture": "Federated data spine with tokenized linkage keys",
                "systems_connected": ["CPS/CWS", "Medicaid/MMIS", "SNAP/TANF", "PHA/HCV", "SIS/education"],
                "privacy_model": "Differential privacy + k-anonymity thresholds",
                "governance": "Multi-agency data governance board with citizen representation",
                "use_cases": [
                    "Predictive risk modeling for child maltreatment",
                    "Benefit cliff analysis across programs",
                    "Longitudinal outcome tracking for reentry populations",
                ],
            }),
            "tags": "data-linkage,privacy,cross-system,administrative-data",
        },
        {
            "title": "NLP Case Note Intelligence Engine",
            "summary": (
                "A natural language processing system that extracts structured data "
                "from free-text caseworker notes — identifying risk factors, service "
                "needs, and outcome indicators that are invisible in checkbox-based "
                "data systems."
            ),
            "category": "natural-language-processing",
            "impact_level": 4,
            "feasibility": 3,
            "novelty": 5,
            "time_horizon": "medium",
            "status": "draft",
            "details": json.dumps({
                "model_type": "Fine-tuned domain-specific language model",
                "extraction_targets": [
                    "Substance use indicators",
                    "Domestic violence risk signals",
                    "Housing instability mentions",
                    "Employment barriers",
                    "Mental health concerns",
                ],
                "accuracy_target": "88% F1 score on validated test set",
                "ethical_safeguards": "Human-in-the-loop review for all flagged cases",
            }),
            "tags": "NLP,case-notes,risk-detection,text-analytics",
        },
        {
            "title": "Real-Time Benefit Uptake Dashboard",
            "summary": (
                "A live dashboard tracking benefit enrollment rates against "
                "estimated eligible populations at the census tract level, "
                "identifying enrollment deserts where eligible families are not "
                "accessing available programs."
            ),
            "category": "dashboards",
            "impact_level": 4,
            "feasibility": 4,
            "novelty": 3,
            "time_horizon": "near",
            "status": "approved",
            "details": json.dumps({
                "data_sources": ["ACS estimates", "Program enrollment files", "Outreach activity logs"],
                "refresh_rate": "Daily for enrollment, annual for eligibility estimates",
                "visualization": "Census-tract heat maps with drill-down to program level",
                "action_triggers": "Automated alerts when uptake drops below 40% of eligible",
            }),
            "tags": "dashboard,benefit-uptake,enrollment,geospatial",
        },
        {
            "title": "Geospatial Service Desert Mapper",
            "summary": (
                "A geospatial analysis tool that overlays service provider locations, "
                "public transit routes, and population density to identify service "
                "deserts — areas where residents must travel more than 30 minutes by "
                "public transit to reach essential services."
            ),
            "category": "geospatial-analysis",
            "impact_level": 4,
            "feasibility": 5,
            "novelty": 3,
            "time_horizon": "near",
            "status": "approved",
            "details": json.dumps({
                "analysis_layers": [
                    "Service provider geocoded locations",
                    "GTFS transit route and schedule data",
                    "Census block group population data",
                    "Walk/bike network from OpenStreetMap",
                ],
                "accessibility_metric": "Minutes to nearest provider by transit + walking",
                "threshold": "30-minute maximum for essential services",
                "output": "Priority zones for mobile service deployment",
            }),
            "tags": "geospatial,service-deserts,transit,accessibility",
        },
        {
            "title": "Person-Held Data Wallets",
            "summary": (
                "Sovereign data wallet putting individuals in control. Instead of "
                "7 agencies each maintaining separate records, the person holds a "
                "verified digital wallet with eligibility data, service history, "
                "and outcome records. They decide who sees what."
            ),
            "category": "data-sovereignty",
            "impact_level": 5,
            "feasibility": 2,
            "novelty": 5,
            "time_horizon": "far",
            "status": "draft",
            "details": json.dumps({
                "architecture": {
                    "storage": "Encrypted local-first with cloud backup",
                    "credentials": "W3C Verifiable Credentials standard",
                    "sharing": "Selective disclosure — share only what each agency needs",
                },
                "data_categories": [
                    "Identity verification",
                    "Income and employment attestations",
                    "Benefit enrollment status across all programs",
                    "Service history and case notes",
                    "Consent preferences and data sharing logs",
                ],
                "estimated_cost": "$3M for wallet infrastructure",
                "evidence_base": "Estonia's X-Road: 1.3M citizens with sovereign data access",
            }),
            "tags": "data-wallet,sovereignty,privacy,person-centered,dome",
        },
    ],

    # ── 4. Tech Futurist ────────────────────────────────────────────────────
    "tech-futurist": [
        {
            "title": "Blockchain Benefits Portability Ledger",
            "summary": (
                "A distributed ledger system that makes benefit eligibility "
                "determinations portable across state lines — when a SNAP recipient "
                "moves states, their verified eligibility travels with them, "
                "eliminating redundant applications and 60-day coverage gaps."
            ),
            "category": "blockchain",
            "impact_level": 5,
            "feasibility": 2,
            "novelty": 5,
            "time_horizon": "far",
            "status": "draft",
            "details": json.dumps({
                "technology": "Permissioned blockchain with state-node architecture",
                "data_stored": "Eligibility determinations (hashed), not personal data",
                "interoperability": "NIEM-compliant data exchange standards",
                "governance": "Interstate compact with federated node management",
                "privacy": "Zero-knowledge proofs for eligibility verification",
            }),
            "tags": "blockchain,portability,interstate,benefits-access",
        },
        {
            "title": "AI-Powered Caseworker Decision Support",
            "summary": (
                "An AI decision support tool that surfaces relevant precedents, "
                "policy options, and risk factors during caseworker-client "
                "interactions — not replacing judgment but augmenting it with "
                "pattern recognition across thousands of similar cases."
            ),
            "category": "artificial-intelligence",
            "impact_level": 4,
            "feasibility": 3,
            "novelty": 4,
            "time_horizon": "medium",
            "status": "review",
            "details": json.dumps({
                "model_approach": "Retrieval-augmented generation over case history corpus",
                "outputs": [
                    "Similar case outcomes and interventions",
                    "Relevant policy citations",
                    "Risk factor highlights",
                    "Service referral recommendations",
                ],
                "safeguards": [
                    "No autonomous decision-making",
                    "Confidence scoring on all suggestions",
                    "Bias auditing quarterly",
                    "Opt-out for caseworkers",
                ],
            }),
            "tags": "AI,decision-support,casework,augmented-intelligence",
        },
        {
            "title": "IoT Housing Quality Continuous Monitoring",
            "summary": (
                "Internet of Things sensor networks deployed in subsidized housing "
                "units that continuously monitor air quality, temperature, humidity, "
                "and structural vibration — enabling proactive maintenance and "
                "providing objective evidence for habitability complaints."
            ),
            "category": "internet-of-things",
            "impact_level": 4,
            "feasibility": 3,
            "novelty": 4,
            "time_horizon": "medium",
            "status": "draft",
            "details": json.dumps({
                "sensors": ["PM2.5 air quality", "Temperature/humidity", "CO/CO2", "Structural vibration", "Water leak detection"],
                "data_transmission": "LoRaWAN mesh network to cloud dashboard",
                "alert_thresholds": "EPA and HUD habitability standards",
                "tenant_access": "Mobile app with real-time readings and complaint filing",
            }),
            "tags": "IoT,housing-quality,sensors,proactive-maintenance",
        },
        {
            "title": "Digital Identity Wallet for Service Access",
            "summary": (
                "A self-sovereign digital identity wallet that lets individuals "
                "store and selectively share verified credentials — birth certificate, "
                "income verification, disability determination — without repeatedly "
                "producing paper documents at every agency."
            ),
            "category": "digital-identity",
            "impact_level": 5,
            "feasibility": 2,
            "novelty": 5,
            "time_horizon": "far",
            "status": "draft",
            "details": json.dumps({
                "technology": "W3C Verifiable Credentials + decentralized identifiers",
                "credentials_supported": [
                    "Identity verification",
                    "Income attestation",
                    "Disability determination",
                    "Housing status",
                    "Employment history",
                ],
                "privacy": "Selective disclosure — share only what each agency needs",
                "offline_capability": "QR code presentation without internet required",
            }),
            "tags": "digital-identity,self-sovereign,verifiable-credentials,access",
        },
        {
            "title": "AR Caseworker Overlay: Real-Time Dome Visualization",
            "summary": (
                "Augmented reality showing a person's complete Dome profile during "
                "home visits. Caseworker sees all active programs, deadlines, benefit "
                "cliffs, and coordination opportunities overlaid in real time — "
                "turning fragmented data into actionable visual intelligence."
            ),
            "category": "augmented-reality",
            "impact_level": 4,
            "feasibility": 2,
            "novelty": 5,
            "time_horizon": "far",
            "status": "draft",
            "details": json.dumps({
                "technology_stack": {
                    "display": "Tablet-first (iPad), smart glasses option for v2",
                    "data_source": "Real-time API to cross-system data spine",
                    "privacy": "Requires person consent via Dome Wallet",
                },
                "use_cases": [
                    "Home visit: see all agency touchpoints at a glance",
                    "Hospital discharge: housing + benefits status overlay",
                    "School meeting: family support ecosystem visualization",
                    "Court hearing: complete service engagement history",
                ],
                "dependencies": [
                    "Cross-system administrative data spine",
                    "Person-held data wallets for consent",
                ],
                "estimated_cost": "$2.5M development + $500K/yr maintenance",
            }),
            "tags": "augmented-reality,caseworker,real-time,dome,visualization",
        },
    ],

    # ── 5. Legislative Inventor ─────────────────────────────────────────────
    "legislative-inventor": [
        {
            "title": "Universal Benefit Application Act (Model)",
            "summary": (
                "Model state legislation requiring all means-tested programs to "
                "accept a single unified application, share eligibility data through "
                "a common intake system, and provide presumptive eligibility for "
                "programs with overlapping income thresholds."
            ),
            "category": "enabling-statutes",
            "impact_level": 5,
            "feasibility": 3,
            "novelty": 4,
            "time_horizon": "medium",
            "status": "review",
            "details": json.dumps({
                "key_provisions": [
                    "Single application for SNAP, Medicaid, CHIP, LIHEAP, CCDF",
                    "Presumptive eligibility at 150% FPL across programs",
                    "Mandatory data sharing between state agencies",
                    "12-month continuous eligibility floor",
                    "No asset test for households below 200% FPL",
                ],
                "fiscal_note": "Net savings of $3.2M per state from reduced duplicative processing",
                "political_strategy": "Bipartisan framing as government efficiency measure",
            }),
            "tags": "model-legislation,unified-application,eligibility,efficiency",
        },
        {
            "title": "Regulatory Sandbox Authorization Act",
            "summary": (
                "Legislation creating a formal regulatory sandbox framework that "
                "allows state agencies to test innovative service delivery models "
                "for up to 36 months with relaxed regulatory requirements, built-in "
                "evaluation, and automatic sunset provisions."
            ),
            "category": "regulatory-sandboxes",
            "impact_level": 4,
            "feasibility": 4,
            "novelty": 4,
            "time_horizon": "near",
            "status": "approved",
            "details": json.dumps({
                "sandbox_parameters": {
                    "duration": "Up to 36 months with one 12-month extension",
                    "scope": "Up to 5 counties or 50,000 participants",
                    "oversight": "Quarterly reporting to legislative committee",
                    "consumer_protection": "No reduction in benefit levels; enhanced grievance procedures",
                },
                "sunset_trigger": "Automatic expiration unless affirmatively renewed by legislature",
            }),
            "tags": "regulatory-sandbox,innovation,sunset-provisions,pilot-authority",
        },
        {
            "title": "Interstate Data Sharing Compact for Human Services",
            "summary": (
                "A model interstate compact enabling participating states to share "
                "benefit enrollment and eligibility data for mobile populations — "
                "seasonal workers, military families, and individuals experiencing "
                "homelessness who cross state lines."
            ),
            "category": "interstate-compacts",
            "impact_level": 4,
            "feasibility": 2,
            "novelty": 5,
            "time_horizon": "far",
            "status": "draft",
            "details": json.dumps({
                "compact_structure": "Commission-based governance with state delegates",
                "data_standards": "NIEM Human Services domain model",
                "populations_served": [
                    "Seasonal/migrant agricultural workers",
                    "Military families with PCS moves",
                    "Individuals experiencing homelessness",
                    "Disaster-displaced households",
                ],
                "privacy_framework": "HIPAA-equivalent protections with state breach notification",
            }),
            "tags": "interstate-compact,data-sharing,mobile-populations,portability",
        },
        {
            "title": "THE DOME ACT: Federal Coordination Cost Transparency",
            "summary": (
                "Federal legislation mandating every agency in means-tested programs "
                "publish annual coordination cost reports — documenting fragmentation "
                "cost, coordination savings, and the gap. Makes the invisible waste "
                "of siloed government visible to every taxpayer."
            ),
            "category": "federal-legislation",
            "impact_level": 5,
            "feasibility": 3,
            "novelty": 5,
            "time_horizon": "medium",
            "status": "review",
            "details": json.dumps({
                "full_title": "Documenting Outcomes and Measuring Efficiency Act (DOME Act)",
                "key_provisions": [
                    "SEC. 101: Annual Coordination Cost Report from HHS, USDA, HUD, DOL, ED",
                    "SEC. 102: Standardized methodology for measuring duplication",
                    "SEC. 103: Public dashboard showing coordination costs by state and county",
                    "SEC. 104: GAO audit of coordination savings potential every 3 years",
                    "SEC. 105: Innovation grants for states demonstrating 10%+ savings",
                    "SEC. 201: Person-centered coordination pilot authority for 10 states",
                    "SEC. 202: Data sharing safe harbor for coordination purposes",
                    "SEC. 301: Coordination Savings Reinvestment Fund",
                ],
                "strategy_memo": {
                    "bipartisan_framing": "Efficiency (R) + better outcomes for families (D)",
                    "coalition": "NGA, APHSA, NASCIO, CLASP, CBPP, Heritage Foundation",
                    "CBO_score": "Net savings $2.1B over 10 years",
                },
                "talking_points": [
                    "$740B in means-tested programs but no one can tell you the cost of NOT coordinating",
                    "Families in 4+ programs repeat their trauma story 7 times",
                    "Hennepin County: $8.2M in annual coordination savings documented",
                    "This bill makes existing spending transparent — not new programs",
                ],
                "estimated_cost": "$50M implementation over 5 years (offset by savings)",
            }),
            "tags": "dome-act,federal,transparency,coordination-costs,bipartisan",
        },
        {
            "title": "RIGHT TO YOUR DOME: Cross-System Data Access Rights",
            "summary": (
                "Model state legislation: every person receiving government services "
                "can see their complete cross-system profile — every enrollment, "
                "assessment, caseworker, and outcome recorded about them. Your data, "
                "your right."
            ),
            "category": "rights-legislation",
            "impact_level": 5,
            "feasibility": 3,
            "novelty": 5,
            "time_horizon": "medium",
            "status": "review",
            "details": json.dumps({
                "full_title": "Right to Integrated Government Records Act",
                "key_provisions": [
                    "SEC. 1: Right to complete cross-system profile within 30 days of request",
                    "SEC. 2: Must include all enrollments, assessments, assigned workers, outcomes",
                    "SEC. 3: Right to correct inaccurate information across all systems simultaneously",
                    "SEC. 4: Data portability — export in machine-readable format",
                    "SEC. 5: No adverse actions from cross-system data without notice and appeal",
                    "SEC. 6: Annual notification of data rights to all enrolled individuals",
                ],
                "talking_points": [
                    "You can see your credit score but not your government profile",
                    "A mother in 4 programs has 4 case files — she never sees a unified picture",
                    "Government data rights lag 20 years behind private sector (GDPR, CCPA)",
                ],
                "estimated_cost": "$800K per state for portal development and staff training",
            }),
            "tags": "data-rights,transparency,person-centered,dome,model-legislation",
        },
    ],

    # ── 6. Regulatory Hacker ────────────────────────────────────────────────
    "regulatory-hacker": [
        {
            "title": "Section 1115 Super-Waiver for Whole-Family Services",
            "summary": (
                "A comprehensive Section 1115 Medicaid waiver that extends "
                "coverage to address social determinants of health — including "
                "housing supports, nutritional counseling, and employment services "
                "— treating the whole family as the unit of care."
            ),
            "category": "waiver-authorities",
            "impact_level": 5,
            "feasibility": 3,
            "novelty": 4,
            "time_horizon": "medium",
            "status": "review",
            "details": json.dumps({
                "waiver_type": "Section 1115 Research & Demonstration",
                "expanded_services": [
                    "Housing transition and sustaining services",
                    "Medical respite for homeless individuals",
                    "Nutrition counseling and food prescription",
                    "Community health worker home visits",
                    "Employment readiness assessments",
                ],
                "budget_neutrality": "Achieved through reduced ER utilization and hospital readmissions",
                "evaluation_design": "Difference-in-differences with propensity score matching",
            }),
            "tags": "1115-waiver,Medicaid,social-determinants,whole-family",
        },
        {
            "title": "Cross-Agency MOU Template for Integrated Eligibility",
            "summary": (
                "A standardized memorandum of understanding template enabling "
                "any two state agencies to share eligibility data, conduct joint "
                "interviews, and make cross-program referrals — reducing the legal "
                "negotiation time from 18 months to 6 weeks."
            ),
            "category": "cross-agency-agreements",
            "impact_level": 3,
            "feasibility": 5,
            "novelty": 2,
            "time_horizon": "near",
            "status": "approved",
            "details": json.dumps({
                "template_sections": [
                    "Purpose and legal authority",
                    "Data elements to be shared",
                    "Security and privacy requirements",
                    "Roles and responsibilities",
                    "Dispute resolution procedures",
                    "Amendment and termination provisions",
                ],
                "pre_approved_clauses": "Vetted by legal counsel across 6 agency types",
                "implementation_time": "6 weeks from initiation to execution",
            }),
            "tags": "MOU,data-sharing,eligibility,interagency",
        },
        {
            "title": "Demonstration Project Fast-Track Protocol",
            "summary": (
                "A streamlined approval protocol for demonstration projects that "
                "reduces the federal approval timeline from 24 months to 90 days "
                "by pre-certifying common innovation categories and establishing "
                "expedited review lanes for low-risk demonstrations."
            ),
            "category": "demonstration-projects",
            "impact_level": 4,
            "feasibility": 3,
            "novelty": 4,
            "time_horizon": "medium",
            "status": "draft",
            "details": json.dumps({
                "fast_track_categories": [
                    "Technology-enabled service delivery",
                    "Simplified reporting requirements",
                    "Cross-program coordination pilots",
                    "Client-centered assessment tools",
                ],
                "approval_timeline": "90 days for pre-certified categories",
                "risk_classification": "Low/Medium/High with corresponding oversight levels",
            }),
            "tags": "demonstration-projects,fast-track,federal-approval,innovation",
        },
        {
            "title": "CMMI Dome Innovation Model",
            "summary": (
                "CMMI demonstration testing whole-person coordination across "
                "Medicaid, housing, nutrition, and employment. Uses existing "
                "Section 1115A authority — CMS already has the power to test this. "
                "No new legislation needed. Deploy immediately."
            ),
            "category": "federal-authority",
            "impact_level": 5,
            "feasibility": 4,
            "novelty": 4,
            "time_horizon": "near",
            "status": "approved",
            "details": json.dumps({
                "legal_authority": "Section 1115A of the Social Security Act (ACA Section 3021)",
                "model_design": {
                    "population": "Medicaid beneficiaries enrolled in 3+ programs",
                    "intervention": "Dome Navigator + shared care plan + braided funding",
                    "comparison": "Matched cohort using existing administrative data",
                    "duration": "5 years with 3-year extension option",
                },
                "existing_precedents": [
                    "Accountable Health Communities (AHC) model",
                    "Integrated Care for Kids (InCK) model",
                    "State Innovation Models (SIM) initiative",
                ],
                "estimated_cost": "$0 in new legislation; $50M from existing CMMI allocation",
                "evidence_base": "CMMI Accountable Health Communities: 9% utilization reduction",
            }),
            "tags": "CMMI,medicaid,existing-authority,immediate,dome,no-legislation",
        },
    ],

    # ── 7. Service Designer ─────────────────────────────────────────────────
    "service-designer": [
        {
            "title": "No-Wrong-Door Triage Protocol",
            "summary": (
                "A universal triage protocol that ensures any government office "
                "a client walks into can initiate service connections across all "
                "programs — using a 10-minute structured conversation to identify "
                "needs and generate warm referrals with scheduled appointments."
            ),
            "category": "no-wrong-door",
            "impact_level": 5,
            "feasibility": 4,
            "novelty": 3,
            "time_horizon": "near",
            "status": "approved",
            "details": json.dumps({
                "triage_tool": "10-minute structured needs assessment",
                "domains_screened": [
                    "Food security", "Housing stability", "Health coverage",
                    "Income/employment", "Child care", "Legal needs",
                ],
                "referral_method": "Warm handoff with scheduled appointment within 48 hours",
                "training_requirement": "8-hour cross-training for all front-line staff",
            }),
            "tags": "no-wrong-door,triage,warm-handoff,cross-training",
        },
        {
            "title": "Trauma-Informed Waiting Room Redesign Guide",
            "summary": (
                "A comprehensive design guide for transforming government office "
                "waiting areas from anxiety-inducing bureaucratic spaces into "
                "calming, dignity-preserving environments — addressing lighting, "
                "seating, signage, sound, and staff interaction protocols."
            ),
            "category": "trauma-informed-design",
            "impact_level": 3,
            "feasibility": 5,
            "novelty": 3,
            "time_horizon": "near",
            "status": "approved",
            "details": json.dumps({
                "design_elements": [
                    "Natural light maximization and warm color palette",
                    "Private conversation alcoves",
                    "Children's activity zones with sight lines for parents",
                    "Real-time wait time displays",
                    "Multilingual wayfinding signage with icons",
                ],
                "staff_protocols": [
                    "First-name greetings within 30 seconds of entry",
                    "Proactive check-ins during waits exceeding 20 minutes",
                    "De-escalation training for all reception staff",
                ],
            }),
            "tags": "trauma-informed,waiting-room,design,dignity",
        },
        {
            "title": "Client Co-Design Sprint Methodology",
            "summary": (
                "A structured 5-day co-design sprint methodology that brings "
                "current and former service recipients into the design process "
                "as equal partners, producing testable prototypes of improved "
                "service experiences with built-in client feedback loops."
            ),
            "category": "co-design",
            "impact_level": 4,
            "feasibility": 4,
            "novelty": 4,
            "time_horizon": "near",
            "status": "review",
            "details": json.dumps({
                "sprint_structure": {
                    "day_1": "Map current experience and pain points",
                    "day_2": "Generate solution concepts",
                    "day_3": "Prototype top 3 ideas",
                    "day_4": "Test prototypes with 5 additional clients",
                    "day_5": "Refine and create implementation plan",
                },
                "compensation": "$150/day stipend for client co-designers",
                "accessibility": "Childcare, transportation, and language interpretation provided",
            }),
            "tags": "co-design,participatory,sprint,client-voice",
        },
        {
            "title": "Journey Map Atlas for Multi-System Families",
            "summary": (
                "A comprehensive journey mapping project documenting the experiences "
                "of families simultaneously navigating child welfare, housing, "
                "behavioral health, and income support systems — revealing the "
                "invisible burden of multi-system involvement."
            ),
            "category": "journey-mapping",
            "impact_level": 4,
            "feasibility": 4,
            "novelty": 3,
            "time_horizon": "near",
            "status": "draft",
            "details": json.dumps({
                "research_method": "In-depth interviews with 40 multi-system families",
                "systems_mapped": ["Child welfare", "Section 8 housing", "Medicaid behavioral health", "TANF/SNAP"],
                "deliverables": [
                    "Visual journey maps for 5 family archetypes",
                    "Pain point inventory with severity ratings",
                    "Quick-win improvement recommendations",
                    "System redesign roadmap",
                ],
            }),
            "tags": "journey-mapping,multi-system,family-experience,service-integration",
        },
        {
            "title": "The Dome Navigator: A New Professional Role",
            "summary": (
                "New profession whose sole job is cross-system coordination for "
                "25-30 people. Not a caseworker in any single system — a coordinator "
                "across ALL systems. Licensed, trained in all benefit programs, with "
                "authority to convene agencies on behalf of the person."
            ),
            "category": "workforce-innovation",
            "impact_level": 5,
            "feasibility": 3,
            "novelty": 5,
            "time_horizon": "medium",
            "status": "review",
            "details": json.dumps({
                "role_definition": {
                    "caseload": "25-30 individuals/families",
                    "function": "Cross-system coordination, not direct service",
                    "authority": "Can convene case conferences across agencies",
                },
                "training_requirements": [
                    "120-hour curriculum covering all benefit programs",
                    "40-hour trauma-informed practice certification",
                    "20-hour data systems navigation training",
                    "Supervised practicum with experienced Navigator",
                ],
                "salary_model": {
                    "entry_level": "$48,000-$55,000",
                    "experienced": "$62,000-$75,000",
                    "senior": "$78,000-$95,000",
                },
                "workforce_sizing": {
                    "us_need": "~85,000 Dome Navigators nationally",
                    "per_county_average": "27 Navigators per county",
                },
                "estimated_cost": "$650K/yr for 10-Navigator pilot",
                "evidence_base": "Community health workers show 3:1 ROI; Navigator extends model to cross-system",
            }),
            "tags": "dome-navigator,workforce,profession,cross-system,dome",
        },
    ],

    # ── 8. Space Architect ──────────────────────────────────────────────────
    "space-architect": [
        {
            "title": "Mobile Service Unit Fleet Design",
            "summary": (
                "Design specifications for a fleet of mobile service units — "
                "converted vehicles equipped with private interview rooms, "
                "computer stations, and telepresence capability — that bring "
                "full-service government offices to underserved communities "
                "on rotating schedules."
            ),
            "category": "mobile-service-units",
            "impact_level": 4,
            "feasibility": 4,
            "novelty": 3,
            "time_horizon": "near",
            "status": "approved",
            "details": json.dumps({
                "vehicle_specs": {
                    "type": "30-foot converted transit vehicle",
                    "stations": 3,
                    "private_rooms": 1,
                    "accessibility": "ADA-compliant ramp and workstation",
                },
                "technology": ["Satellite internet", "Mobile hotspot", "Telepresence screen", "Document scanner/printer"],
                "deployment": "Rotating schedule covering 12 underserved zones per month",
            }),
            "tags": "mobile-units,access,underserved-communities,outreach",
        },
        {
            "title": "Virtual Service Hub Architecture",
            "summary": (
                "Architecture for a fully virtual one-stop service hub where "
                "clients access video consultations, document upload, and real-time "
                "eligibility screening from any device — designed for low-bandwidth "
                "environments with fallback to SMS-based interaction."
            ),
            "category": "virtual-service-hubs",
            "impact_level": 4,
            "feasibility": 3,
            "novelty": 4,
            "time_horizon": "medium",
            "status": "review",
            "details": json.dumps({
                "platform_features": [
                    "Video consultation scheduling and drop-in queue",
                    "Secure document upload with OCR verification",
                    "Multi-program eligibility pre-screening",
                    "Integrated interpreter services",
                    "SMS fallback for low-bandwidth users",
                ],
                "accessibility": "WCAG 2.1 AA compliant, screen reader optimized",
                "bandwidth_requirement": "Minimum 1.5 Mbps for full experience, 2G for SMS mode",
            }),
            "tags": "virtual-hub,digital-access,low-bandwidth,one-stop",
        },
        {
            "title": "One-Stop Center Wayfinding System",
            "summary": (
                "A universal wayfinding system for integrated service centers "
                "that guides clients through multi-agency buildings using color-coded "
                "pathways, digital kiosks, and optional smartphone navigation — "
                "reducing confusion and no-show rates for scheduled appointments."
            ),
            "category": "one-stop-centers",
            "impact_level": 3,
            "feasibility": 5,
            "novelty": 2,
            "time_horizon": "near",
            "status": "approved",
            "details": json.dumps({
                "system_components": [
                    "Color-coded floor pathways by service domain",
                    "Multilingual digital directory kiosks",
                    "Smartphone indoor navigation via Bluetooth beacons",
                    "Staff-guided escort option for complex visits",
                ],
                "expected_outcomes": "25% reduction in missed appointments, 15% faster visit completion",
            }),
            "tags": "wayfinding,one-stop,navigation,client-experience",
        },
        {
            "title": "Neighborhood Dome Center (2,000 sq ft Storefront)",
            "summary": (
                "Smallest viable coordination space — a welcoming community living "
                "room, not a government office. Two private rooms, open area, "
                "children's corner, tech station. Anti-pattern library: NO fluorescent "
                "lights, NO plastic chairs, NO bulletproof glass."
            ),
            "category": "dome-center-design",
            "impact_level": 4,
            "feasibility": 4,
            "novelty": 4,
            "time_horizon": "near",
            "status": "approved",
            "details": json.dumps({
                "floor_plan": {
                    "total_sqft": 2000,
                    "private_rooms": "2 consultation rooms (100 sqft each)",
                    "open_area": "800 sqft with flexible furniture",
                    "tech_station": "4 workstations + scanner",
                    "children_corner": "200 sqft supervised play",
                    "kitchenette": "Coffee, water, healthy snacks",
                },
                "material_palette": {
                    "flooring": "Warm wood-look LVT",
                    "walls": "Soft white + terracotta accent",
                    "furniture": "Residential-quality upholstered (not plastic)",
                    "lighting": "Warm LED 2700-3000K, NO fluorescent",
                },
                "anti_patterns": [
                    "NO fluorescent lighting",
                    "NO plastic chairs",
                    "NO bulletproof glass",
                    "NO numbered ticket queuing",
                    "NO mounted TVs playing news",
                    "NO visible security cameras in consultation areas",
                ],
                "cost_estimate": {
                    "buildout": "$180,000-$240,000",
                    "furniture": "$45,000-$65,000",
                    "technology": "$25,000-$35,000",
                    "annual_operating": "$180,000-$220,000 including 3 staff",
                },
            }),
            "tags": "dome-center,neighborhood,storefront,anti-pattern,dome",
        },
        {
            "title": "Regional Dome Hub (50,000 sq ft Campus)",
            "summary": (
                "Flagship campus: Navigator training academy, data operations center, "
                "community halls, health clinic, legal aid, demonstration spaces. "
                "Biophilic design, universal accessibility, trauma-informed architecture."
            ),
            "category": "dome-center-design",
            "impact_level": 5,
            "feasibility": 2,
            "novelty": 5,
            "time_horizon": "far",
            "status": "draft",
            "details": json.dumps({
                "floor_plan": {
                    "total_sqft": 50000,
                    "coordination_wing": "10,000 sqft — 20 rooms + Navigator floor",
                    "training_academy": "8,000 sqft — classrooms + simulation lab",
                    "community_wing": "12,000 sqft — 500-seat assembly + gallery",
                    "health_clinic": "5,000 sqft — FQHC partner",
                    "legal_aid": "3,000 sqft — civil legal + record expungement",
                    "data_center": "4,000 sqft — secure ops + visualization wall",
                },
                "cost_estimate": {
                    "new_construction": "$18M-$24M",
                    "adaptive_reuse": "$12M-$16M",
                    "annual_operating": "$4.5M-$6M including 50+ staff",
                },
                "dependencies": [
                    "Dome Navigator workforce pipeline",
                    "Dome Bonds financing mechanism",
                ],
                "evidence_base": "UK Integrated Care Hubs: 22% better outcomes from co-location at scale",
            }),
            "tags": "dome-hub,regional,campus,flagship,dome",
        },
    ],

    # ── 9. Measurement Scientist ────────────────────────────────────────────
    "measurement-scientist": [
        {
            "title": "Rapid-Cycle RCT Framework for Social Programs",
            "summary": (
                "A streamlined randomized controlled trial framework designed for "
                "social programs that produces actionable results in 6-12 months "
                "instead of the traditional 3-5 years — using administrative data "
                "outcomes, adaptive designs, and Bayesian stopping rules."
            ),
            "category": "randomized-controlled-trials",
            "impact_level": 5,
            "feasibility": 3,
            "novelty": 4,
            "time_horizon": "medium",
            "status": "review",
            "details": json.dumps({
                "design_features": [
                    "Administrative data outcomes (no primary data collection)",
                    "Sequential enrollment with adaptive randomization",
                    "Bayesian stopping rules for early efficacy/futility",
                    "Pre-registered analysis plans on OSF",
                ],
                "timeline": "6-12 months from enrollment to preliminary results",
                "cost_estimate": "$150K-$400K vs. $2M+ for traditional RCT",
            }),
            "tags": "RCT,rapid-cycle,evidence,bayesian",
        },
        {
            "title": "Social Return on Investment Calculator",
            "summary": (
                "An open-source calculator tool that enables any social program "
                "to estimate its Social Return on Investment (SROI) using "
                "standardized value maps, stakeholder-validated proxies, and "
                "conservative benefit estimates — democratizing impact measurement."
            ),
            "category": "social-return-on-investment",
            "impact_level": 4,
            "feasibility": 4,
            "novelty": 3,
            "time_horizon": "near",
            "status": "approved",
            "details": json.dumps({
                "methodology": "SROI Network International Standard (2012 update)",
                "value_maps": "Pre-built for 15 common program types",
                "outputs": [
                    "SROI ratio (dollars of value per dollar invested)",
                    "Sensitivity analysis across key assumptions",
                    "Stakeholder-specific value breakdown",
                    "Narrative impact report generator",
                ],
                "validation": "Benchmarked against 50 published SROI analyses",
            }),
            "tags": "SROI,calculator,impact-measurement,open-source",
        },
        {
            "title": "Cost-Benefit Analysis Template for Benefit Cliff Mitigation",
            "summary": (
                "A specialized cost-benefit analysis template for evaluating "
                "policies that address the benefit cliff — calculating the fiscal "
                "impact of graduated phase-outs versus abrupt cutoffs across "
                "SNAP, Medicaid, CCDF, and housing subsidy programs."
            ),
            "category": "cost-benefit-analysis",
            "impact_level": 4,
            "feasibility": 4,
            "novelty": 3,
            "time_horizon": "near",
            "status": "draft",
            "details": json.dumps({
                "programs_modeled": ["SNAP", "Medicaid", "CCDF", "Section 8 HCV"],
                "analysis_components": [
                    "Marginal tax rate calculation across programs",
                    "Labor supply response estimation",
                    "Government fiscal impact (gross vs. net)",
                    "Family income smoothing benefits",
                ],
                "scenarios": "Current law, 24-month phase-out, 36-month phase-out, earnings disregard",
            }),
            "tags": "cost-benefit,benefit-cliff,marginal-tax,policy-analysis",
        },
        {
            "title": "Quasi-Experimental Design Toolkit for County Agencies",
            "summary": (
                "A practical toolkit enabling county-level agencies to conduct "
                "rigorous quasi-experimental evaluations using regression "
                "discontinuity, interrupted time series, and difference-in-differences "
                "designs with existing administrative data."
            ),
            "category": "quasi-experimental-designs",
            "impact_level": 4,
            "feasibility": 4,
            "novelty": 3,
            "time_horizon": "near",
            "status": "approved",
            "details": json.dumps({
                "methods_included": [
                    "Regression discontinuity (sharp and fuzzy)",
                    "Interrupted time series with comparison group",
                    "Difference-in-differences with parallel trends testing",
                    "Propensity score matching with sensitivity analysis",
                ],
                "toolkit_components": [
                    "Decision tree for method selection",
                    "R and Stata code templates",
                    "Sample size and power calculators",
                    "Plain-language reporting templates",
                ],
            }),
            "tags": "quasi-experimental,toolkit,county-agencies,evaluation",
        },
        {
            "title": "Dome Index: 0-100 Coordination Quality Score",
            "summary": (
                "Single composite score measuring coordination quality for any "
                "jurisdiction. Six sub-indices: data sharing, service integration, "
                "financing alignment, workforce capacity, client experience, outcome "
                "equity. Like a credit score for government coordination."
            ),
            "category": "measurement-frameworks",
            "impact_level": 5,
            "feasibility": 3,
            "novelty": 5,
            "time_horizon": "medium",
            "status": "review",
            "details": json.dumps({
                "scoring_methodology": {
                    "total_range": "0-100",
                    "sub_indices": {
                        "data_sharing": "0-20 points",
                        "service_integration": "0-20 points",
                        "financing_alignment": "0-15 points",
                        "workforce_capacity": "0-15 points",
                        "client_experience": "0-15 points",
                        "outcome_equity": "0-15 points",
                    },
                },
                "benchmarks": {
                    "0-25": "Siloed — agencies operate independently",
                    "26-50": "Connecting — some data sharing in place",
                    "51-75": "Coordinating — shared intake, braided funding",
                    "76-100": "Integrated — person-centered budgets, full interop",
                },
                "estimated_cost": "$400K development; $150K/yr for 50 jurisdictions",
                "evidence_base": "Pilot-tested in 5 counties, Cronbach alpha = 0.87",
            }),
            "tags": "dome-index,coordination-score,benchmarking,dome",
        },
    ],

    # ── 10. Narrative Researcher ────────────────────────────────────────────
    "narrative-researcher": [
        {
            "title": "Photovoice Project: Navigating the Safety Net",
            "summary": (
                "A participatory photovoice research project where 30 families "
                "receiving multiple benefits document their daily experiences "
                "navigating government systems through photography and narrative "
                "— producing an exhibition and policy report centering client voice."
            ),
            "category": "photovoice",
            "impact_level": 4,
            "feasibility": 4,
            "novelty": 3,
            "time_horizon": "near",
            "status": "review",
            "details": json.dumps({
                "participants": 30,
                "duration": "12 weeks of photo documentation + 4 weeks analysis",
                "method": "SHOWeD analysis framework (What do you See? What is Happening? How does this relate to Our lives? Why does this exist? What can we Do?)",
                "outputs": [
                    "Public exhibition at county government center",
                    "Policy brief with 10 recommendations",
                    "Digital story collection for advocacy",
                    "Peer-reviewed publication",
                ],
            }),
            "tags": "photovoice,participatory,client-voice,visual-research",
        },
        {
            "title": "Digital Storytelling Archive: System Survivors",
            "summary": (
                "A curated digital storytelling archive collecting first-person "
                "narratives from individuals who have aged out of foster care, "
                "exited the criminal justice system, or transitioned off long-term "
                "benefits — preserving experiential knowledge for policy design."
            ),
            "category": "digital-storytelling",
            "impact_level": 3,
            "feasibility": 4,
            "novelty": 4,
            "time_horizon": "near",
            "status": "draft",
            "details": json.dumps({
                "story_format": "3-5 minute audio/video narratives with guided prompts",
                "target_collection": "100 stories across 3 system-exit populations",
                "ethical_framework": "Trauma-informed collection with full narrative control by storytellers",
                "access_model": "Open access archive with metadata for policy-relevant searching",
            }),
            "tags": "digital-storytelling,archive,lived-experience,qualitative",
        },
        {
            "title": "Ethnographic Study of Caseworker Decision-Making",
            "summary": (
                "A 12-month embedded ethnographic study observing caseworker "
                "decision-making in child welfare investigations — documenting "
                "the gap between policy-as-written and practice-as-lived, and "
                "identifying structural factors that drive discretionary variation."
            ),
            "category": "ethnography",
            "impact_level": 4,
            "feasibility": 3,
            "novelty": 4,
            "time_horizon": "medium",
            "status": "review",
            "details": json.dumps({
                "methodology": "Institutional ethnography with shadowing and interviews",
                "duration": "12 months embedded in 3 county CPS offices",
                "data_collection": [
                    "Field notes from 200+ hours of observation",
                    "Semi-structured interviews with 40 caseworkers",
                    "Document analysis of case files and policy manuals",
                ],
                "research_questions": [
                    "How do caseworkers interpret ambiguous risk indicators?",
                    "What organizational factors shape removal decisions?",
                    "Where does policy intent diverge from practice reality?",
                ],
            }),
            "tags": "ethnography,caseworker,child-welfare,discretion,qualitative",
        },
        {
            "title": "DOMES Documentary Series: The Invisible Architecture",
            "summary": (
                "3-part documentary series: 'The Maze' (families navigating "
                "fragmentation), 'The Workers' (caseworker moral injury), 'The "
                "Builders' (communities constructing DOMES). Target: Sundance → "
                "PBS → Congressional screening."
            ),
            "category": "documentary",
            "impact_level": 4,
            "feasibility": 3,
            "novelty": 4,
            "time_horizon": "medium",
            "status": "draft",
            "details": json.dumps({
                "series_structure": {
                    "part_1_the_maze": {
                        "duration": "55 minutes",
                        "subjects": "3 families navigating 4+ programs simultaneously",
                    },
                    "part_2_the_workers": {
                        "duration": "55 minutes",
                        "subjects": "12 caseworkers across child welfare, Medicaid, housing",
                    },
                    "part_3_the_builders": {
                        "duration": "55 minutes",
                        "subjects": "3 communities constructing DOMES coordination models",
                    },
                },
                "distribution_strategy": [
                    "Sundance Film Festival social impact track",
                    "PBS national broadcast",
                    "Congressional screening for DOME Act support",
                    "University curriculum integration",
                ],
                "estimated_cost": "$1.8M total production budget",
                "evidence_base": "'13th' influenced criminal justice reform; 'Waiting for Superman' drove education policy",
            }),
            "tags": "documentary,storytelling,advocacy,dome",
        },
    ],

    # ── 11. Market Maker ────────────────────────────────────────────────────
    "market-maker": [
        {
            "title": "Social Enterprise Incubator for Reentry Populations",
            "summary": (
                "A 12-month incubator program that helps formerly incarcerated "
                "individuals launch social enterprises, providing business "
                "training, seed capital, mentorship, and legal support for "
                "record-related barriers — creating pathways to economic "
                "self-sufficiency outside traditional employment."
            ),
            "category": "social-enterprise",
            "impact_level": 5,
            "feasibility": 3,
            "novelty": 4,
            "time_horizon": "medium",
            "status": "review",
            "details": json.dumps({
                "program_structure": {
                    "phase_1": "8-week business fundamentals bootcamp",
                    "phase_2": "16-week venture development with mentor pairing",
                    "phase_3": "6-month post-launch support and peer network",
                },
                "seed_capital": "$5,000-$15,000 per venture (grant, not loan)",
                "legal_support": "Record expungement clinic + business licensing assistance",
                "target_cohort": "15 entrepreneurs per annual cohort",
            }),
            "tags": "social-enterprise,reentry,incubator,entrepreneurship",
        },
        {
            "title": "Community Land Trust for Service-Enriched Housing",
            "summary": (
                "A community land trust model that permanently removes land from "
                "the speculative market and develops service-enriched affordable "
                "housing — combining permanently affordable units with on-site "
                "case management, health services, and workforce development."
            ),
            "category": "community-land-trusts",
            "impact_level": 5,
            "feasibility": 3,
            "novelty": 3,
            "time_horizon": "medium",
            "status": "draft",
            "details": json.dumps({
                "model": "Classic CLT with ground lease and resale formula",
                "housing_units": "40-60 units per development",
                "on_site_services": [
                    "Primary care clinic (partner FQHC)",
                    "Benefits enrollment office",
                    "Workforce readiness center",
                    "Children's after-school program",
                ],
                "affordability_guarantee": "Permanent — survives resale through ground lease restriction",
            }),
            "tags": "community-land-trust,affordable-housing,services,permanent-affordability",
        },
        {
            "title": "Time Banking Network for Mutual Aid",
            "summary": (
                "A digital time banking platform where community members exchange "
                "services hour-for-hour — childcare for tax preparation, "
                "transportation for home repairs — building social capital and "
                "addressing service gaps outside the cash economy."
            ),
            "category": "time-banking",
            "impact_level": 3,
            "feasibility": 4,
            "novelty": 3,
            "time_horizon": "near",
            "status": "approved",
            "details": json.dumps({
                "platform": "Mobile-first web application with SMS integration",
                "service_categories": [
                    "Transportation", "Childcare", "Home repair",
                    "Tax preparation", "Translation", "Technology help",
                    "Cooking/meal prep", "Companionship/check-ins",
                ],
                "governance": "Community steering committee with elected coordinators",
                "scale_target": "500 active members within 18 months",
            }),
            "tags": "time-banking,mutual-aid,community,social-capital",
        },
        {
            "title": "Benefit Corporation Certification for Human Service Providers",
            "summary": (
                "A specialized benefit corporation certification framework for "
                "organizations delivering government-contracted human services — "
                "ensuring they maintain mission fidelity, worker wellbeing, and "
                "client outcomes even as they scale through government contracting."
            ),
            "category": "benefit-corporations",
            "impact_level": 3,
            "feasibility": 4,
            "novelty": 4,
            "time_horizon": "near",
            "status": "draft",
            "details": json.dumps({
                "certification_criteria": [
                    "Client outcome measurement and reporting",
                    "Living wage for all direct service staff",
                    "Client representation on board of directors",
                    "Financial transparency beyond legal minimums",
                    "Annual impact audit by independent evaluator",
                ],
                "benefits_of_certification": [
                    "Preferred vendor status in government procurement",
                    "Access to impact investment capital",
                    "Public trust and accountability signal",
                ],
            }),
            "tags": "benefit-corporation,certification,mission-fidelity,accountability",
        },
        {
            "title": "Dome Certification: Agency Coordination Quality Standard",
            "summary": (
                "Like LEED for buildings but for government coordination. Bronze/"
                "Silver/Gold/Platinum certification based on coordination practices, "
                "data sharing, client experience, and outcomes. Market incentive for "
                "system integration."
            ),
            "category": "certification",
            "impact_level": 4,
            "feasibility": 4,
            "novelty": 4,
            "time_horizon": "near",
            "status": "review",
            "details": json.dumps({
                "certification_levels": {
                    "bronze": "Basic data sharing + referral protocols with 2+ agencies",
                    "silver": "Shared intake + braided funding + coordination staff",
                    "gold": "Integrated case management + shared outcomes + co-design",
                    "platinum": "Person-centered budgets + full interop + Dome Index 75+",
                },
                "market_incentives": [
                    "Preferred status in federal grants",
                    "Insurance premium reductions for certified agencies",
                    "Public Dome Certified branding and trust signal",
                    "Access to Dome Network knowledge exchanges",
                ],
                "estimated_cost": "$2M program development; $500K/yr operations",
                "evidence_base": "LEED drove $83B in green construction via market-verified quality standards",
            }),
            "tags": "dome-certification,quality-standard,coordination,market-incentives,dome",
        },
    ],

    # ── 12. Architect ───────────────────────────────────────────────────────
    "architect": [
        {
            "title": "Integrated Reform Package: Whole-Family Economic Mobility",
            "summary": (
                "A comprehensive cross-domain reform package that combines "
                "braided funding (fiscal), outcomes-based financing (impact), "
                "data spine infrastructure (data), no-wrong-door triage (service), "
                "and rapid-cycle RCT evaluation (measurement) into a cohesive "
                "whole-family economic mobility system."
            ),
            "category": "system-integration",
            "impact_level": 5,
            "feasibility": 2,
            "novelty": 5,
            "time_horizon": "far",
            "status": "review",
            "details": json.dumps({
                "components": [
                    {"domain": "creative-financing", "innovation": "Braided Benefit Bridge Fund"},
                    {"domain": "impact-investment", "innovation": "Outcomes-Based Foster Care Financing"},
                    {"domain": "data-innovation", "innovation": "Cross-System Administrative Data Spine"},
                    {"domain": "service-design", "innovation": "No-Wrong-Door Triage Protocol"},
                    {"domain": "impact-measurement", "innovation": "Rapid-Cycle RCT Framework"},
                ],
                "integration_architecture": "Shared data layer + unified outcome framework + blended funding",
                "implementation_timeline": "3-year phased rollout across 5 pilot counties",
            }),
            "tags": "integration,whole-family,economic-mobility,cross-domain",
        },
        {
            "title": "Dependency Map: Innovation Sequencing Strategy",
            "summary": (
                "A comprehensive dependency analysis identifying which innovations "
                "must be implemented first to enable others — revealing that data "
                "infrastructure and regulatory reform are critical-path prerequisites "
                "for most service delivery and financing innovations."
            ),
            "category": "dependency-mapping",
            "impact_level": 4,
            "feasibility": 4,
            "novelty": 4,
            "time_horizon": "near",
            "status": "approved",
            "details": json.dumps({
                "critical_path": [
                    "1. Cross-Agency MOU Template (regulatory-reform)",
                    "2. Cross-System Data Spine (data-innovation)",
                    "3. Unified Application Act (model-legislation)",
                    "4. No-Wrong-Door Triage (service-design)",
                    "5. Braided Funding Pool (creative-financing)",
                ],
                "parallel_tracks": [
                    "Narrative research can proceed independently",
                    "Measurement frameworks should co-develop with interventions",
                    "Market-making innovations need regulatory foundation first",
                ],
            }),
            "tags": "dependency-mapping,sequencing,critical-path,strategy",
        },
        {
            "title": "Cross-Domain Synergy Matrix",
            "summary": (
                "A quantified synergy matrix showing the interaction effects "
                "between all 12 innovation domains — identifying the highest-value "
                "collaboration pairs and the combinations that produce "
                "super-additive outcomes."
            ),
            "category": "systems-thinking",
            "impact_level": 4,
            "feasibility": 4,
            "novelty": 4,
            "time_horizon": "near",
            "status": "review",
            "details": json.dumps({
                "methodology": "Pairwise impact scoring by expert panel (n=24)",
                "top_synergy_pairs": [
                    {"pair": ["data-innovation", "impact-measurement"], "score": 9.2},
                    {"pair": ["creative-financing", "impact-investment"], "score": 8.8},
                    {"pair": ["regulatory-reform", "model-legislation"], "score": 8.5},
                    {"pair": ["service-design", "space-design"], "score": 8.3},
                    {"pair": ["narrative-research", "service-design"], "score": 7.9},
                ],
                "super_additive_combinations": [
                    "Data + Measurement + Financing = Evidence-based funding allocation",
                    "Regulation + Legislation + Service Design = Enabled innovation corridors",
                ],
            }),
            "tags": "synergy-matrix,cross-domain,systems-thinking,collaboration",
        },
    ],
}


def seed_innovations(db) -> list[Innovation]:
    """Seed the database with pre-generated innovations for each teammate."""
    from datetime import timedelta
    import random

    existing_count = db.query(Innovation).count()
    if existing_count > 0:
        return []

    # Build slug -> Teammate lookup
    teammates = {t.slug: t for t in db.query(Teammate).all()}
    created: list[Innovation] = []

    base_time = datetime.now(timezone.utc) - timedelta(days=60)

    for slug, innovations_data in SEED_INNOVATIONS.items():
        teammate = teammates.get(slug)
        if not teammate:
            continue

        for idx, inn in enumerate(innovations_data):
            # Stagger created_at times for realistic ordering
            offset_days = random.randint(0, 55)
            offset_hours = random.randint(0, 23)

            innovation = Innovation(
                teammate_id=teammate.id,
                title=inn["title"],
                summary=inn["summary"],
                domain=teammate.domain,
                category=inn.get("category", "general"),
                impact_level=inn.get("impact_level", 3),
                feasibility=inn.get("feasibility", 3),
                novelty=inn.get("novelty", 3),
                time_horizon=inn.get("time_horizon", "medium"),
                status=inn.get("status", "draft"),
                details=inn.get("details", "{}"),
                tags=inn.get("tags", ""),
                created_at=base_time + timedelta(days=offset_days, hours=offset_hours),
                updated_at=base_time + timedelta(days=offset_days, hours=offset_hours + 1),
            )
            db.add(innovation)
            created.append(innovation)

    if created:
        db.commit()
        for inn in created:
            db.refresh(inn)

    return created
