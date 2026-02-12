"""
DOMES Innovation Laboratory — Innovation Generator.

When POST /api/generate/{slug} is called, this module creates a new innovation
for the specified teammate using predefined templates with randomized parameters.
Each domain has 8-10 innovation templates with title patterns, summary patterns,
and score ranges appropriate to that domain.
"""

import json
import random
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from models import Innovation, Teammate


# ── Template structure ──────────────────────────────────────────────────────
# Each template is a dict with:
#   title: str
#   summary: str
#   category: str
#   tags: str (comma-separated)
#   details: dict (will be JSON-serialized)
#   impact_range: (min, max)
#   feasibility_range: (min, max)
#   novelty_range: (min, max)
#   time_horizons: list of possible values

DOMAIN_TEMPLATES: dict[str, list[dict]] = {
    # ── 1. Fiscal Alchemist ─────────────────────────────────────────────────
    "fiscal-alchemist": [
        {
            "title": "Earned Income Amplification Fund",
            "summary": "A matched savings program that uses EITC refunds as the base deposit, with 3:1 employer and philanthropic matches channeled through CDFIs, creating a $4,000+ annual asset-building vehicle for working families below 200% FPL.",
            "category": "matched-savings",
            "tags": "EITC,matched-savings,asset-building,CDFI",
            "details": {"mechanism": "EITC-anchored matched savings", "match_ratio": "3:1", "target_population": "Working families below 200% FPL", "projected_asset_growth": "$4,000+ per family per year"},
            "impact_range": (4, 5), "feasibility_range": (3, 4), "novelty_range": (3, 4), "time_horizons": ["near", "medium"],
        },
        {
            "title": "Catastrophic Stability Insurance Pool",
            "summary": "A risk-pooling mechanism across 20+ counties that creates a shared insurance fund against sudden caseload surges from natural disasters, plant closures, or pandemics — smoothing fiscal shocks that destabilize county human services budgets.",
            "category": "risk-pooling",
            "tags": "risk-pool,insurance,fiscal-stability,county-budgets",
            "details": {"mechanism": "Inter-county risk pool with actuarial modeling", "pool_size": "20+ counties", "trigger_events": ["Natural disaster", "Major employer closure", "Pandemic surge"], "premium_structure": "Population-weighted annual contributions"},
            "impact_range": (4, 5), "feasibility_range": (3, 4), "novelty_range": (4, 5), "time_horizons": ["medium", "far"],
        },
        {
            "title": "Revenue Recycling Loop for Prevention Programs",
            "summary": "A fiscal mechanism that automatically redirects 15% of documented savings from reduced foster care placements, emergency room visits, and incarceration back into the upstream prevention programs that generated those savings.",
            "category": "reinvestment",
            "tags": "prevention,reinvestment,savings-recycling,upstream",
            "details": {"mechanism": "Automated savings capture and reinvestment", "reinvestment_rate": "15% of documented savings", "savings_sources": ["Reduced foster placements", "Lower ER utilization", "Decreased incarceration"], "verification": "Independent fiscal auditor"},
            "impact_range": (4, 5), "feasibility_range": (3, 4), "novelty_range": (4, 5), "time_horizons": ["medium"],
        },
        {
            "title": "Green Social Bond for Healthy Housing",
            "summary": "A green bond instrument that finances lead remediation, weatherization, and mold abatement in subsidized housing units, with debt service paid from Medicaid savings realized through reduced childhood lead poisoning and asthma hospitalizations.",
            "category": "green-bonds",
            "tags": "green-bond,healthy-housing,lead,Medicaid-savings",
            "details": {"mechanism": "Green bond with health-linked debt service", "target": "Lead remediation and weatherization", "savings_source": "Medicaid reduced hospitalization claims", "bond_size": "$25M-$50M per issuance"},
            "impact_range": (4, 5), "feasibility_range": (3, 4), "novelty_range": (4, 5), "time_horizons": ["medium"],
        },
        {
            "title": "Philanthropic First-Loss Guarantee Fund",
            "summary": "A philanthropic guarantee fund that absorbs the first 10% of losses on social innovation investments, de-risking participation for commercial and institutional investors who would otherwise not enter the social impact space.",
            "category": "credit-enhancement",
            "tags": "guarantee-fund,first-loss,philanthropy,de-risking",
            "details": {"mechanism": "First-loss credit enhancement", "loss_absorption": "First 10% of portfolio losses", "target_investors": "Commercial banks, pension funds, insurance companies", "fund_size": "$5M philanthropic to unlock $50M commercial"},
            "impact_range": (4, 5), "feasibility_range": (3, 5), "novelty_range": (3, 4), "time_horizons": ["near", "medium"],
        },
        {
            "title": "Benefit Cliff Smoothing Escrow",
            "summary": "An escrow mechanism that holds transitional funds for families approaching benefit cliffs, releasing graduated supplemental payments as earned income rises — preventing the abrupt loss of housing, childcare, and health benefits.",
            "category": "transition-finance",
            "tags": "benefit-cliff,escrow,transition,income-smoothing",
            "details": {"mechanism": "Graduated escrow release tied to income milestones", "funding": "Blended public/philanthropic capital", "duration": "24-month transition period", "coverage": "Housing, childcare, and health premium gaps"},
            "impact_range": (4, 5), "feasibility_range": (3, 4), "novelty_range": (4, 5), "time_horizons": ["medium"],
        },
        {
            "title": "Workforce Pipeline Tax Credit",
            "summary": "A refundable state tax credit for employers who hire and retain individuals from target populations (reentry, foster care alumni, long-term unemployed) for 12+ months, structured as a declining subsidy that phases out over 3 years.",
            "category": "tax-credits",
            "tags": "tax-credit,workforce,employer-incentive,retention",
            "details": {"mechanism": "Declining employer tax credit", "credit_structure": "Year 1: 50% of wages, Year 2: 30%, Year 3: 15%", "target_populations": ["Reentry", "Foster care alumni", "Long-term unemployed"], "retention_requirement": "12 months minimum"},
            "impact_range": (3, 5), "feasibility_range": (3, 4), "novelty_range": (3, 4), "time_horizons": ["near", "medium"],
        },
        {
            "title": "Municipal Social Infrastructure Bond",
            "summary": "A new class of municipal bond specifically designated for social infrastructure — community health centers, integrated service hubs, early childhood facilities — with tax-exempt status and priority underwriting from mission-aligned institutions.",
            "category": "municipal-bonds",
            "tags": "municipal-bond,social-infrastructure,tax-exempt,community-facilities",
            "details": {"mechanism": "Tax-exempt municipal bond for social infrastructure", "eligible_projects": ["Community health centers", "One-stop service hubs", "Early childhood centers", "Workforce training facilities"], "tax_treatment": "Federal and state tax-exempt interest"},
            "impact_range": (4, 5), "feasibility_range": (3, 4), "novelty_range": (3, 4), "time_horizons": ["medium", "far"],
        },
    ],

    # ── 2. Impact Investor ──────────────────────────────────────────────────
    "impact-investor": [
        {
            "title": "Early Childhood Development Impact Bond",
            "summary": "An impact bond financing high-quality home visiting programs for first-time parents in high-poverty zip codes, with investor returns tied to kindergarten readiness scores and reduced special education referrals measured at age 5.",
            "category": "social-impact-bonds",
            "tags": "early-childhood,home-visiting,impact-bond,kindergarten-readiness",
            "details": {"intervention": "Evidence-based home visiting (PAT/NFP models)", "outcome_metric": "Kindergarten readiness + special ed referral rates", "investment": "$6M over 5 years", "target": "First-time parents below 150% FPL"},
            "impact_range": (4, 5), "feasibility_range": (3, 4), "novelty_range": (3, 4), "time_horizons": ["medium", "far"],
        },
        {
            "title": "Chronic Homelessness Zero-Return Bond",
            "summary": "An outcomes-based financing instrument funding Housing First permanent supportive housing, with returns triggered by sustained housing retention at 12 and 24 months and documented reductions in emergency service utilization.",
            "category": "outcomes-based-financing",
            "tags": "homelessness,Housing-First,permanent-supportive,outcomes-based",
            "details": {"model": "Housing First permanent supportive housing", "success_metrics": ["12-month housing retention > 85%", "24-month retention > 75%", "ER visits reduced > 40%"], "investor_return": "5.5% IRR on outcome achievement"},
            "impact_range": (5, 5), "feasibility_range": (3, 4), "novelty_range": (3, 4), "time_horizons": ["medium"],
        },
        {
            "title": "Impact Measurement Standardization Protocol",
            "summary": "A standardized impact measurement protocol for social investments that creates comparability across diverse program types — enabling portfolio-level impact reporting and secondary market liquidity for social impact instruments.",
            "category": "impact-measurement",
            "tags": "standardization,measurement,portfolio,secondary-market",
            "details": {"framework": "IRIS+ aligned with GIIN standards", "metrics": ["Lives materially improved", "Cost per outcome achieved", "Government savings generated", "Beneficiary satisfaction index"], "comparability": "Cross-program normalization methodology"},
            "impact_range": (3, 4), "feasibility_range": (4, 5), "novelty_range": (3, 4), "time_horizons": ["near", "medium"],
        },
        {
            "title": "Community Ownership Investment Vehicle",
            "summary": "An investment vehicle allowing community residents to invest small amounts ($25-$500) in local social enterprises and affordable housing projects, earning modest returns while building community wealth and democratic ownership.",
            "category": "community-investment",
            "tags": "community-ownership,micro-investment,wealth-building,democratic",
            "details": {"minimum_investment": "$25", "maximum_investment": "$500 per offering", "target_return": "2-4% annually", "governance": "Investor-member voting rights on project selection"},
            "impact_range": (4, 5), "feasibility_range": (3, 4), "novelty_range": (4, 5), "time_horizons": ["medium"],
        },
        {
            "title": "Workforce Development Outcomes Fund",
            "summary": "A pooled outcomes fund that pays service providers upon achieving verified employment and earnings milestones for disconnected youth — creating competition among providers on outcomes rather than outputs.",
            "category": "outcomes-funds",
            "tags": "workforce,disconnected-youth,outcomes-fund,pay-for-performance",
            "details": {"target_population": "Disconnected youth ages 16-24", "outcome_payments": {"job_placement": "$1,500", "6_month_retention": "$2,500", "earnings_above_threshold": "$3,000"}, "fund_size": "$10M pooled from government and philanthropy"},
            "impact_range": (4, 5), "feasibility_range": (3, 4), "novelty_range": (3, 4), "time_horizons": ["near", "medium"],
        },
        {
            "title": "Disaster Recovery Social Bond",
            "summary": "A pre-positioned social bond that activates automatically upon federal disaster declaration, providing immediate capital for human services surge capacity while traditional FEMA reimbursement processes unfold over months.",
            "category": "disaster-finance",
            "tags": "disaster,pre-positioned,surge-capacity,rapid-response",
            "details": {"trigger": "Federal disaster declaration in covered jurisdiction", "activation_time": "48 hours from declaration", "capital_available": "$5M-$20M depending on disaster severity tier", "repayment": "FEMA PA reimbursement + state match"},
            "impact_range": (4, 5), "feasibility_range": (2, 3), "novelty_range": (5, 5), "time_horizons": ["medium", "far"],
        },
        {
            "title": "Racial Equity Investment Scoring Overlay",
            "summary": "An investment scoring overlay that explicitly weights racial equity outcomes — requiring that social investments demonstrate measurable reduction in racial disparities as a condition of positive impact classification.",
            "category": "equity-frameworks",
            "tags": "racial-equity,scoring,investment-criteria,disparities",
            "details": {"scoring_dimensions": ["Disparity reduction in target outcome", "Community ownership and governance", "Wealth building in BIPOC communities", "Cultural responsiveness of intervention"], "threshold": "Minimum 60/100 equity score for impact classification"},
            "impact_range": (4, 5), "feasibility_range": (3, 4), "novelty_range": (4, 5), "time_horizons": ["near", "medium"],
        },
        {
            "title": "Pay-for-Prevention Opioid Recovery Bond",
            "summary": "A pay-for-prevention bond funding medication-assisted treatment and peer recovery support, with returns linked to reduced overdose deaths, decreased Medicaid spending on acute care, and sustained recovery milestones.",
            "category": "pay-for-prevention",
            "tags": "opioid,MAT,recovery,pay-for-prevention",
            "details": {"intervention": "MAT + peer recovery support + housing", "outcome_metrics": ["Overdose death reduction", "Medicaid acute care savings", "12-month sustained recovery rate"], "investment": "$8M over 4 years"},
            "impact_range": (5, 5), "feasibility_range": (3, 4), "novelty_range": (4, 4), "time_horizons": ["medium"],
        },
    ],

    # ── 3. Data Inventor ────────────────────────────────────────────────────
    "data-inventor": [
        {
            "title": "Predictive Benefit Cliff Alert System",
            "summary": "A predictive analytics system that identifies families approaching benefit cliffs 90 days in advance by modeling income trajectories against program thresholds, enabling proactive caseworker outreach before benefits drop abruptly.",
            "category": "predictive-analytics",
            "tags": "predictive,benefit-cliff,early-warning,income-modeling",
            "details": {"model": "Time-series income trajectory with program threshold overlay", "lead_time": "90-day advance warning", "data_sources": ["Quarterly wage records", "Program eligibility files", "UI claims data"], "intervention": "Proactive caseworker outreach with transition planning"},
            "impact_range": (4, 5), "feasibility_range": (3, 4), "novelty_range": (4, 5), "time_horizons": ["medium"],
        },
        {
            "title": "Automated Eligibility Determination Engine",
            "summary": "A rules engine that ingests verified data from multiple administrative systems to auto-determine eligibility for 8 programs simultaneously — reducing application processing time from 30 days to 48 hours for straightforward cases.",
            "category": "automation",
            "tags": "eligibility,automation,rules-engine,processing-time",
            "details": {"programs_covered": ["SNAP", "Medicaid", "CHIP", "LIHEAP", "CCDF", "WIC", "Section 8", "School meals"], "data_sources": "IRS, SSA, state wage records, vital statistics", "processing_target": "48 hours for 70% of applications"},
            "impact_range": (5, 5), "feasibility_range": (3, 4), "novelty_range": (4, 4), "time_horizons": ["medium"],
        },
        {
            "title": "Sentiment Analysis of Client Feedback Streams",
            "summary": "A sentiment analysis pipeline that processes client satisfaction surveys, complaint records, ombudsman reports, and social media mentions to generate real-time service quality indices by office, program, and worker.",
            "category": "sentiment-analysis",
            "tags": "sentiment,client-feedback,service-quality,real-time",
            "details": {"data_streams": ["Client satisfaction surveys", "Formal complaints", "Ombudsman reports", "Social media mentions"], "output": "Real-time service quality index by office/program", "refresh_rate": "Daily aggregate, weekly trend analysis"},
            "impact_range": (3, 4), "feasibility_range": (4, 5), "novelty_range": (3, 4), "time_horizons": ["near"],
        },
        {
            "title": "Synthetic Data Generator for Policy Simulation",
            "summary": "A synthetic data generation system that creates statistically representative but fully anonymous population datasets, enabling policy analysts to model the impact of proposed rule changes without accessing real client data.",
            "category": "synthetic-data",
            "tags": "synthetic-data,privacy,policy-simulation,anonymization",
            "details": {"method": "Differentially private generative model trained on aggregate statistics", "fidelity_metrics": "Preserves marginal distributions and key correlations", "use_cases": ["Benefit cliff policy modeling", "Eligibility expansion impact estimates", "Budget forecasting under proposed rule changes"]},
            "impact_range": (4, 5), "feasibility_range": (3, 4), "novelty_range": (5, 5), "time_horizons": ["medium"],
        },
        {
            "title": "Multi-System Contact Timeline Visualization",
            "summary": "A timeline visualization tool that displays an individual's touchpoints across all government systems on a single chronological view — revealing patterns of escalating need, missed intervention windows, and system coordination failures.",
            "category": "visualization",
            "tags": "timeline,visualization,multi-system,touchpoints",
            "details": {"systems_displayed": ["Child welfare contacts", "Medicaid claims", "SNAP recertifications", "Housing inspections", "Court appearances", "School attendance"], "privacy": "Requires client consent and authenticated caseworker access", "insight_overlays": "Automated pattern detection for escalation sequences"},
            "impact_range": (4, 5), "feasibility_range": (3, 4), "novelty_range": (4, 4), "time_horizons": ["medium"],
        },
        {
            "title": "Address History Graph for Housing Stability Tracking",
            "summary": "A graph database linking address records across Medicaid, SNAP, school enrollment, and postal data to construct housing stability scores — identifying families with frequent moves that indicate housing instability before they enter shelter.",
            "category": "graph-analytics",
            "tags": "graph-database,housing-stability,address-linking,early-identification",
            "details": {"data_sources": ["Medicaid address records", "SNAP address changes", "School enrollment addresses", "USPS change-of-address data"], "stability_score": "Composite index based on move frequency, distance, and school disruption", "intervention_threshold": "3+ moves in 12 months triggers outreach"},
            "impact_range": (4, 5), "feasibility_range": (3, 4), "novelty_range": (4, 5), "time_horizons": ["medium"],
        },
        {
            "title": "Anomaly Detection for Fraud and Error in Benefits",
            "summary": "A machine learning anomaly detection system that identifies unusual patterns in benefit transactions — distinguishing intentional fraud from systemic errors and agency processing mistakes, reducing false positive rates from 30% to under 5%.",
            "category": "anomaly-detection",
            "tags": "anomaly-detection,fraud,error-detection,machine-learning",
            "details": {"approach": "Ensemble methods (isolation forest + autoencoder + rules)", "training_data": "Historical adjudicated cases with known outcomes", "false_positive_target": "< 5% (vs. 30% in current rules-based systems)", "equity_safeguard": "Disparate impact testing across demographic groups"},
            "impact_range": (4, 5), "feasibility_range": (3, 4), "novelty_range": (4, 4), "time_horizons": ["medium"],
        },
        {
            "title": "Open Data Portal for Human Services Research",
            "summary": "A public open data portal publishing de-identified, aggregated human services data at the county and census tract level — enabling academic researchers, journalists, and community organizations to analyze service patterns and outcomes.",
            "category": "open-data",
            "tags": "open-data,transparency,research,public-access",
            "details": {"data_granularity": "County and census tract level aggregates", "suppression_rules": "Cells with < 10 individuals suppressed", "datasets": ["Program enrollment counts by geography", "Average processing times", "Outcome metrics by program", "Demographic composition"], "api": "REST API with GeoJSON and CSV export"},
            "impact_range": (3, 4), "feasibility_range": (4, 5), "novelty_range": (3, 3), "time_horizons": ["near"],
        },
    ],

    # ── 4. Tech Futurist ────────────────────────────────────────────────────
    "tech-futurist": [
        {
            "title": "Voice-First Benefit Application Interface",
            "summary": "A multilingual voice interface that allows clients to apply for benefits through natural conversation via phone — eliminating literacy barriers and enabling application completion for populations who cannot navigate web forms.",
            "category": "voice-interface",
            "tags": "voice,multilingual,accessibility,benefit-application",
            "details": {"technology": "Conversational AI with speech-to-text and intent recognition", "languages": ["English", "Spanish", "Mandarin", "Vietnamese", "Arabic"], "channel": "Toll-free phone line + integration with smart speakers", "completion_rate_target": "75% of straightforward applications completed by voice"},
            "impact_range": (4, 5), "feasibility_range": (3, 4), "novelty_range": (4, 5), "time_horizons": ["medium"],
        },
        {
            "title": "Biometric Express Enrollment Kiosk",
            "summary": "Self-service kiosks at libraries, community centers, and laundromats that use fingerprint and facial verification to authenticate identity and pull pre-populated benefit applications from linked databases — enabling 15-minute enrollment.",
            "category": "biometric-enrollment",
            "tags": "biometric,kiosk,enrollment,self-service",
            "details": {"authentication": "Fingerprint + facial verification (liveness detection)", "integration": "Pre-populated applications from SSA, IRS, and state vital records", "locations": "Libraries, community centers, laundromats, grocery stores", "enrollment_time": "15 minutes for pre-verified individuals"},
            "impact_range": (4, 5), "feasibility_range": (2, 3), "novelty_range": (4, 5), "time_horizons": ["medium", "far"],
        },
        {
            "title": "Automated Document Verification Pipeline",
            "summary": "An AI-powered document verification system that validates uploaded identity documents, pay stubs, utility bills, and lease agreements in real-time — replacing manual document review that adds 2-3 weeks to application processing.",
            "category": "document-verification",
            "tags": "document-verification,AI,processing-time,automation",
            "details": {"document_types": ["Government-issued ID", "Pay stubs", "Utility bills", "Lease agreements", "Birth certificates"], "verification_methods": ["OCR extraction", "Tamper detection", "Cross-reference with issuing databases"], "processing_time": "Under 60 seconds per document"},
            "impact_range": (4, 5), "feasibility_range": (3, 4), "novelty_range": (3, 4), "time_horizons": ["near", "medium"],
        },
        {
            "title": "Chatbot Case Manager for Routine Interactions",
            "summary": "An AI chatbot that handles routine case management interactions — appointment reminders, document requests, status updates, and FAQ responses — freeing caseworkers to focus on complex human judgment tasks.",
            "category": "chatbot",
            "tags": "chatbot,case-management,routine-tasks,caseworker-relief",
            "details": {"handled_interactions": ["Appointment scheduling/reminders", "Document upload requests", "Application status inquiries", "FAQ responses", "Recertification reminders"], "escalation": "Automatic handoff to human caseworker for complex issues", "channel": "SMS, web chat, and Facebook Messenger"},
            "impact_range": (3, 4), "feasibility_range": (4, 5), "novelty_range": (3, 3), "time_horizons": ["near"],
        },
        {
            "title": "Augmented Reality Accessibility Assessment Tool",
            "summary": "An AR mobile application that allows housing inspectors to assess ADA compliance and accessibility features in real-time during unit inspections, overlaying requirement specifications on live camera views of physical spaces.",
            "category": "augmented-reality",
            "tags": "AR,accessibility,housing-inspection,ADA-compliance",
            "details": {"platform": "iOS and Android mobile application", "capabilities": ["Doorway width measurement", "Ramp grade calculation", "Turning radius assessment", "Counter height verification"], "output": "Automated compliance report with photo documentation"},
            "impact_range": (3, 4), "feasibility_range": (3, 4), "novelty_range": (5, 5), "time_horizons": ["medium", "far"],
        },
        {
            "title": "Federated Learning for Cross-Jurisdiction Risk Models",
            "summary": "A federated machine learning framework that trains predictive models across multiple jurisdictions without any jurisdiction sharing raw data — enabling small counties to benefit from large-dataset model quality.",
            "category": "federated-learning",
            "tags": "federated-learning,privacy,cross-jurisdiction,predictive-models",
            "details": {"approach": "Federated averaging with differential privacy guarantees", "participating_jurisdictions": "20+ counties contributing to shared model", "privacy_guarantee": "No raw data leaves originating jurisdiction", "model_types": ["Child maltreatment risk", "Homelessness prediction", "Benefit eligibility estimation"]},
            "impact_range": (4, 5), "feasibility_range": (2, 3), "novelty_range": (5, 5), "time_horizons": ["far"],
        },
        {
            "title": "Smart Contract Benefit Disbursement",
            "summary": "Blockchain smart contracts that automatically disburse benefit payments when eligibility conditions are verified through data feeds — eliminating processing delays and ensuring same-day payment for approved applicants.",
            "category": "smart-contracts",
            "tags": "smart-contract,blockchain,disbursement,automation",
            "details": {"technology": "Ethereum-compatible smart contract on permissioned chain", "triggers": "Automated eligibility verification from authoritative data sources", "payment_speed": "Same-day disbursement upon condition verification", "audit_trail": "Immutable transaction log for compliance"},
            "impact_range": (4, 5), "feasibility_range": (2, 3), "novelty_range": (5, 5), "time_horizons": ["far"],
        },
        {
            "title": "Wearable Health Monitor Integration for Medicaid",
            "summary": "Integration of consumer wearable health data (with patient consent) into Medicaid care management platforms, enabling remote monitoring of chronic conditions and early intervention for high-risk enrollees.",
            "category": "wearable-health",
            "tags": "wearable,remote-monitoring,Medicaid,chronic-conditions",
            "details": {"devices": ["Smartwatches", "Continuous glucose monitors", "Blood pressure cuffs", "Pulse oximeters"], "consent": "Explicit opt-in with granular data sharing controls", "alerts": "Automated alerts to care manager for out-of-range readings"},
            "impact_range": (4, 5), "feasibility_range": (2, 3), "novelty_range": (4, 5), "time_horizons": ["medium", "far"],
        },
    ],

    # ── 5. Legislative Inventor ─────────────────────────────────────────────
    "legislative-inventor": [
        {
            "title": "Child Poverty Reduction Accountability Act",
            "summary": "Model legislation requiring states to set binding 5-year child poverty reduction targets with annual benchmarks, mandatory corrective action plans when targets are missed, and legislative sunset review of underperforming programs.",
            "category": "accountability-legislation",
            "tags": "child-poverty,accountability,targets,corrective-action",
            "details": {"target_setting": "Binding 5-year reduction targets (e.g., 50% reduction)", "accountability": "Annual benchmarks with mandatory corrective action", "sunset": "Programs not meeting targets face automatic sunset review"},
            "impact_range": (5, 5), "feasibility_range": (2, 3), "novelty_range": (4, 5), "time_horizons": ["medium", "far"],
        },
        {
            "title": "Benefits Portability Enabling Act",
            "summary": "State legislation authorizing participation in the Interstate Benefits Portability Compact, enabling benefit eligibility to transfer seamlessly when families move across state lines without re-application.",
            "category": "enabling-statutes",
            "tags": "portability,interstate,enabling-statute,mobility",
            "details": {"compact_provisions": ["Reciprocal eligibility recognition", "60-day transition coverage", "Shared verification infrastructure", "Dispute resolution mechanism"], "fiscal_note": "Budget-neutral through reduced duplicate processing"},
            "impact_range": (4, 5), "feasibility_range": (2, 3), "novelty_range": (4, 5), "time_horizons": ["far"],
        },
        {
            "title": "Innovation Procurement Reform Act",
            "summary": "Legislation reforming government procurement to allow outcomes-based contracting, multi-year performance agreements, and rapid sole-source authority for validated innovations — removing procurement barriers to evidence-based practice adoption.",
            "category": "procurement-reform",
            "tags": "procurement,outcomes-based,contracting,innovation",
            "details": {"key_provisions": ["Outcomes-based contract authority", "5-year performance agreements", "Rapid sole-source for evidence-rated interventions", "Innovation fund set-aside (2% of human services budget)"]},
            "impact_range": (4, 5), "feasibility_range": (3, 4), "novelty_range": (3, 4), "time_horizons": ["near", "medium"],
        },
        {
            "title": "Right to Counsel in Benefits Proceedings Act",
            "summary": "Model legislation establishing a right to legal representation for individuals facing benefit termination, housing eviction, or child welfare proceedings — funded through a dedicated surcharge on corporate filing fees.",
            "category": "rights-legislation",
            "tags": "right-to-counsel,legal-representation,due-process,access-to-justice",
            "details": {"covered_proceedings": ["Benefit termination hearings", "Eviction proceedings", "Child welfare removal hearings"], "funding": "Corporate filing fee surcharge generating $15M annually", "implementation": "Phased rollout starting with highest-stakes proceedings"},
            "impact_range": (5, 5), "feasibility_range": (2, 3), "novelty_range": (4, 4), "time_horizons": ["medium"],
        },
        {
            "title": "Data Governance and Privacy Protection Act",
            "summary": "Comprehensive state legislation establishing data governance standards for human services, including data sharing authorization, privacy protections, algorithmic accountability requirements, and citizen data access rights.",
            "category": "data-governance",
            "tags": "data-governance,privacy,algorithmic-accountability,transparency",
            "details": {"key_provisions": ["Unified data sharing authorization framework", "Algorithmic impact assessments for automated decisions", "Individual right to access own government-held data", "Breach notification within 72 hours", "Annual transparency report on data use"]},
            "impact_range": (4, 5), "feasibility_range": (3, 4), "novelty_range": (4, 4), "time_horizons": ["medium"],
        },
        {
            "title": "Community Reinvestment in Human Services Act",
            "summary": "Legislation requiring financial institutions to invest in human services infrastructure as part of CRA obligations — expanding the Community Reinvestment Act concept to include social service facilities, workforce centers, and family resource centers.",
            "category": "reinvestment-legislation",
            "tags": "CRA,community-reinvestment,financial-institutions,social-infrastructure",
            "details": {"qualifying_investments": ["Family resource centers", "Workforce development facilities", "Integrated service hubs", "Supportive housing"], "compliance": "CRA examination credit for qualifying investments"},
            "impact_range": (4, 5), "feasibility_range": (2, 3), "novelty_range": (4, 5), "time_horizons": ["medium", "far"],
        },
        {
            "title": "Automatic Benefit Enrollment Authorization Act",
            "summary": "Model legislation authorizing automatic enrollment in benefits programs when eligibility is verified through existing government data — converting the current opt-in model to opt-out for SNAP, Medicaid, and EITC.",
            "category": "automatic-enrollment",
            "tags": "automatic-enrollment,opt-out,benefit-access,administrative-burden",
            "details": {"programs_covered": ["SNAP", "Medicaid", "CHIP", "EITC"], "mechanism": "Automatic enrollment based on tax return and wage data", "opt_out": "30-day opt-out window with simplified online/phone process", "projected_uptake_increase": "15-25% increase in eligible population enrolled"},
            "impact_range": (5, 5), "feasibility_range": (2, 3), "novelty_range": (5, 5), "time_horizons": ["medium", "far"],
        },
        {
            "title": "Human Services Workforce Investment Act",
            "summary": "Legislation establishing minimum qualifications, competitive compensation benchmarks, and professional development requirements for human services caseworkers — addressing the workforce crisis driving 40%+ annual turnover rates.",
            "category": "workforce-legislation",
            "tags": "workforce,caseworker,compensation,professional-development",
            "details": {"provisions": ["Minimum salary benchmarked to 80th percentile of comparable occupations", "Annual professional development stipend ($2,500)", "Caseload caps tied to case complexity scores", "Student loan forgiveness after 5 years of service"]},
            "impact_range": (4, 5), "feasibility_range": (3, 4), "novelty_range": (3, 4), "time_horizons": ["near", "medium"],
        },
    ],

    # ── 6. Regulatory Hacker ────────────────────────────────────────────────
    "regulatory-hacker": [
        {
            "title": "Categorical Eligibility Expansion via Existing Authority",
            "summary": "A strategy to expand categorical eligibility for SNAP by leveraging existing broad-based categorical eligibility provisions tied to TANF-funded services — increasing the gross income limit to 200% FPL without new legislation.",
            "category": "eligibility-expansion",
            "tags": "categorical-eligibility,SNAP,TANF,existing-authority",
            "details": {"mechanism": "Broad-based categorical eligibility through TANF-funded information brochure", "effect": "Raises SNAP gross income limit from 130% to 200% FPL", "legal_basis": "7 CFR 273.2(j)(2)(ii) and TANF MOE flexibility", "implementation": "Administrative policy change, no legislation required"},
            "impact_range": (5, 5), "feasibility_range": (4, 5), "novelty_range": (2, 3), "time_horizons": ["near"],
        },
        {
            "title": "Compliance Automation for Federal Reporting",
            "summary": "A system that auto-generates federal compliance reports (TANF Data Report, SNAP QC, Medicaid T-MSIS) directly from operational data systems — eliminating the manual reporting burden that consumes 15% of state agency staff time.",
            "category": "compliance-automation",
            "tags": "compliance,federal-reporting,automation,staff-time",
            "details": {"reports_automated": ["ACF-199 TANF Data Report", "SNAP QC Review", "T-MSIS Medicaid data", "CCDF ACF-801"], "data_source": "Direct extraction from operational eligibility systems", "time_savings": "15% of state agency analyst FTEs redirected to direct service"},
            "impact_range": (3, 4), "feasibility_range": (4, 5), "novelty_range": (2, 3), "time_horizons": ["near"],
        },
        {
            "title": "Multi-Agency Regulatory Alignment Assessment",
            "summary": "A comprehensive assessment tool that maps regulatory requirements across 6 federal agencies and identifies conflicting rules, duplicative requirements, and missed coordination opportunities — producing a prioritized deregulation agenda.",
            "category": "regulatory-assessment",
            "tags": "regulatory-alignment,deregulation,cross-agency,assessment",
            "details": {"agencies_mapped": ["HHS/ACF", "USDA/FNS", "HUD", "DOL/ETA", "ED", "SSA"], "analysis_dimensions": ["Conflicting definitions", "Duplicative reporting", "Incompatible timelines", "Contradictory incentives"], "output": "Prioritized list of 25 highest-impact regulatory fixes"},
            "impact_range": (4, 5), "feasibility_range": (3, 4), "novelty_range": (3, 4), "time_horizons": ["near", "medium"],
        },
        {
            "title": "Section 1915(c) Waiver for Community Integration",
            "summary": "A Medicaid 1915(c) home and community-based services waiver that funds non-traditional community integration supports — peer mentoring, community navigation, social connection facilitation — for individuals transitioning from institutional settings.",
            "category": "waiver-authorities",
            "tags": "1915c-waiver,HCBS,community-integration,Medicaid",
            "details": {"waiver_type": "Section 1915(c) HCBS", "novel_services": ["Peer mentoring", "Community navigation", "Social connection facilitation", "Independent living skills coaching"], "target_population": "Individuals transitioning from nursing facilities, IMDs, and group homes"},
            "impact_range": (4, 5), "feasibility_range": (3, 4), "novelty_range": (4, 4), "time_horizons": ["medium"],
        },
        {
            "title": "Joint Application Processing Agreement",
            "summary": "A regulatory framework enabling county welfare offices and Social Security field offices to process applications jointly at a single location, sharing intake staff and verification systems under a unified data sharing agreement.",
            "category": "joint-processing",
            "tags": "joint-processing,SSA,county-welfare,co-location",
            "details": {"agencies": "County welfare department + SSA field office", "shared_functions": ["Joint intake interview", "Shared document verification", "Cross-program eligibility screening"], "legal_framework": "Interagency agreement under SSA POMS SI 00601.010"},
            "impact_range": (3, 4), "feasibility_range": (3, 4), "novelty_range": (3, 3), "time_horizons": ["near", "medium"],
        },
        {
            "title": "Presumptive Eligibility Protocol for Emergency Periods",
            "summary": "A pre-authorized protocol that activates presumptive eligibility across all major benefit programs during declared emergencies — providing immediate access to food, health care, and housing assistance without full verification.",
            "category": "emergency-protocols",
            "tags": "presumptive-eligibility,emergency,rapid-access,disaster",
            "details": {"activation_trigger": "Governor's emergency declaration", "programs_covered": ["SNAP (D-SNAP)", "Medicaid", "Emergency housing assistance", "LIHEAP"], "eligibility": "Self-attestation with 90-day post-emergency verification", "duration": "Emergency period + 60 days"},
            "impact_range": (5, 5), "feasibility_range": (3, 4), "novelty_range": (3, 4), "time_horizons": ["near"],
        },
        {
            "title": "Regulatory Sandbox for Benefits Technology Startups",
            "summary": "A regulatory sandbox allowing govtech startups to pilot benefits-related technology solutions with real agency data and workflows for 12 months under supervised conditions — accelerating innovation without compromising client protections.",
            "category": "regulatory-sandboxes",
            "tags": "sandbox,govtech,startups,pilot",
            "details": {"duration": "12 months with option to extend to 18", "participant_cap": "5 startups per cohort", "data_access": "Synthetic data for development, supervised real data for pilot", "consumer_protections": "Enhanced complaint process + automatic rollback provisions"},
            "impact_range": (4, 5), "feasibility_range": (3, 4), "novelty_range": (4, 5), "time_horizons": ["near", "medium"],
        },
        {
            "title": "Cross-State Licensing Reciprocity for Social Workers",
            "summary": "An administrative agreement enabling licensed social workers to practice across state lines through a reciprocity framework, addressing the workforce shortage in border communities and rural areas without legislative action.",
            "category": "licensing-reciprocity",
            "tags": "licensing,reciprocity,social-workers,workforce",
            "details": {"mechanism": "Interstate administrative reciprocity agreement", "requirements": "Active license in home state + background check", "scope": "Telehealth and in-person practice in reciprocal states", "precedent": "Modeled on Nurse Licensure Compact administrative provisions"},
            "impact_range": (3, 4), "feasibility_range": (3, 4), "novelty_range": (3, 3), "time_horizons": ["near", "medium"],
        },
    ],

    # ── 7. Service Designer ─────────────────────────────────────────────────
    "service-designer": [
        {
            "title": "Warm Handoff Protocol with Guaranteed Callback",
            "summary": "A standardized warm handoff protocol where the referring worker personally introduces the client to the receiving worker by phone or video during the referral visit, with a guaranteed 48-hour callback if the connection is not made.",
            "category": "warm-handoffs",
            "tags": "warm-handoff,referral,guaranteed-callback,connection",
            "details": {"protocol": "Live introduction (phone/video) during referring visit", "fallback": "48-hour guaranteed callback from receiving agency", "tracking": "Referral completion tracked in shared dashboard", "success_metric": "90% connection rate within 72 hours"},
            "impact_range": (4, 5), "feasibility_range": (4, 5), "novelty_range": (3, 3), "time_horizons": ["near"],
        },
        {
            "title": "Life Event-Triggered Service Navigation",
            "summary": "A proactive service navigation system that detects life events — birth of a child, job loss, eviction filing, incarceration — and automatically dispatches a navigator with a pre-assembled package of relevant benefits and services.",
            "category": "proactive-outreach",
            "tags": "life-events,proactive,navigation,trigger-based",
            "details": {"trigger_events": ["Birth/adoption", "Job loss (UI filing)", "Eviction filing", "Release from incarceration", "Aging out of foster care", "Disability onset"], "response": "Navigator contact within 5 business days with pre-assembled benefit package", "data_source": "Cross-system event detection from administrative data"},
            "impact_range": (5, 5), "feasibility_range": (3, 4), "novelty_range": (5, 5), "time_horizons": ["medium"],
        },
        {
            "title": "Multilingual Service Access Audit Framework",
            "summary": "A comprehensive audit framework for assessing language access across all service touchpoints — phone trees, websites, forms, in-person interactions, and signage — with remediation scorecards for the top 10 languages in each jurisdiction.",
            "category": "language-access",
            "tags": "multilingual,language-access,audit,equity",
            "details": {"touchpoints_audited": ["Phone systems", "Websites", "Paper forms", "In-person interactions", "Signage", "Notices and correspondence"], "scoring": "0-100 language access score per touchpoint per language", "remediation": "Prioritized action plan with 90-day quick wins"},
            "impact_range": (4, 4), "feasibility_range": (4, 5), "novelty_range": (2, 3), "time_horizons": ["near"],
        },
        {
            "title": "Peer Navigator Program Design",
            "summary": "A structured peer navigator program that trains individuals with lived system experience to guide current clients through complex multi-system processes — providing emotional support, practical guidance, and institutional knowledge from the client perspective.",
            "category": "peer-support",
            "tags": "peer-navigator,lived-experience,client-support,training",
            "details": {"navigator_qualifications": "Personal experience navigating 2+ government systems", "training": "80-hour certification program covering systems knowledge, boundaries, and trauma-informed practice", "caseload": "15-20 active clients per navigator", "compensation": "$18-$22/hour with benefits"},
            "impact_range": (4, 5), "feasibility_range": (4, 5), "novelty_range": (3, 4), "time_horizons": ["near"],
        },
        {
            "title": "Service Experience Feedback Loop System",
            "summary": "A continuous feedback system that collects client experience data at every service touchpoint via SMS micro-surveys (2-3 questions), aggregates responses into real-time dashboards, and triggers automatic review when satisfaction drops below thresholds.",
            "category": "feedback-systems",
            "tags": "feedback,SMS-surveys,continuous-improvement,client-voice",
            "details": {"method": "SMS micro-surveys (2-3 questions) post-interaction", "response_rate_target": "25% participation", "dashboard": "Real-time satisfaction scores by office, program, and interaction type", "alert_threshold": "Score below 3.0/5.0 triggers supervisor review"},
            "impact_range": (3, 4), "feasibility_range": (4, 5), "novelty_range": (3, 3), "time_horizons": ["near"],
        },
        {
            "title": "Dignity-Centered Intake Redesign",
            "summary": "A complete redesign of the benefit intake process based on dignity principles — eliminating unnecessary verifications, providing private interview spaces, offering refreshments and childcare, and starting every interaction with 'How can we help?' instead of 'Prove you qualify.'",
            "category": "intake-redesign",
            "tags": "dignity,intake,redesign,client-experience",
            "details": {"principles": ["Presumption of eligibility", "Privacy for all conversations", "Physical comfort (refreshments, childcare, seating)", "Plain language (no jargon)", "Choice in communication channel"], "eliminations": ["Redundant identity verification across programs", "Waiting room intake questionnaires", "Visible case file numbers on paperwork"]},
            "impact_range": (4, 5), "feasibility_range": (4, 5), "novelty_range": (4, 4), "time_horizons": ["near"],
        },
        {
            "title": "Cross-System Care Coordination Protocol",
            "summary": "A structured care coordination protocol for families involved in 3+ government systems simultaneously, assigning a lead coordinator, establishing a shared family plan, and convening monthly cross-system team meetings.",
            "category": "care-coordination",
            "tags": "care-coordination,multi-system,shared-plan,lead-coordinator",
            "details": {"trigger": "Family involved in 3+ systems simultaneously", "lead_coordinator": "Assigned from the system with most intensive involvement", "shared_plan": "Single family plan with goals, actions, and accountability across all systems", "meetings": "Monthly cross-system team meetings with family participation"},
            "impact_range": (5, 5), "feasibility_range": (3, 4), "novelty_range": (3, 4), "time_horizons": ["near", "medium"],
        },
        {
            "title": "Service Design Pattern Library",
            "summary": "An open-source pattern library documenting 50+ proven service design patterns for human services — from appointment scheduling to notification design to grievance processes — enabling agencies to adopt proven solutions without reinventing them.",
            "category": "design-patterns",
            "tags": "pattern-library,open-source,design-patterns,reusable",
            "details": {"patterns_documented": 50, "categories": ["Intake and enrollment", "Communication and notifications", "Appointments and scheduling", "Referrals and handoffs", "Complaints and grievances", "Recertification and renewal"], "format": "Problem statement, solution, implementation guidance, examples"},
            "impact_range": (3, 4), "feasibility_range": (5, 5), "novelty_range": (3, 4), "time_horizons": ["near"],
        },
    ],

    # ── 8. Space Architect ──────────────────────────────────────────────────
    "space-architect": [
        {
            "title": "Pop-Up Service Hub Kit",
            "summary": "A modular pop-up service hub kit that can be deployed in vacant storefronts, community rooms, or outdoor spaces within 48 hours — providing temporary multi-agency service access during emergencies or in areas without permanent offices.",
            "category": "pop-up-services",
            "tags": "pop-up,modular,rapid-deployment,temporary",
            "details": {"deployment_time": "48 hours from decision to operational", "components": ["Portable interview partitions", "Satellite internet kit", "Folding workstations (6)", "Generator and lighting", "Signage and wayfinding package"], "cost": "$15,000 per kit (reusable)"},
            "impact_range": (4, 5), "feasibility_range": (4, 5), "novelty_range": (4, 4), "time_horizons": ["near"],
        },
        {
            "title": "Library-Based Service Access Points",
            "summary": "A partnership framework to establish dedicated human services access points within public libraries — leveraging existing trusted community spaces, internet access, and extended hours to reach populations who avoid government buildings.",
            "category": "partner-spaces",
            "tags": "library,partnership,trusted-spaces,access-points",
            "details": {"space_requirements": "Dedicated corner or room with privacy partitions", "staffing": "Rotating agency staff 3 days/week + trained library navigator", "services": ["Benefit screening and application assistance", "Document scanning and submission", "Video consultations with caseworkers"], "trust_factor": "Libraries rated as most trusted public institution by underserved populations"},
            "impact_range": (4, 5), "feasibility_range": (4, 5), "novelty_range": (3, 3), "time_horizons": ["near"],
        },
        {
            "title": "Sensory-Considerate Office Design Standards",
            "summary": "Design standards for government offices that accommodate sensory processing differences — adjustable lighting, sound-dampening materials, low-stimulation waiting areas, and quiet rooms — making services accessible to neurodiverse clients.",
            "category": "accessibility-standards",
            "tags": "sensory,neurodiversity,accessibility,office-design",
            "details": {"design_elements": ["Adjustable LED lighting (2700K-5000K range)", "Sound-absorbing wall panels and ceiling tiles", "Low-stimulation waiting area option", "Quiet room for overwhelm recovery", "Fidget tools and weighted blankets available"], "population_served": "Estimated 15-20% of clients with sensory processing differences"},
            "impact_range": (3, 4), "feasibility_range": (4, 5), "novelty_range": (4, 4), "time_horizons": ["near"],
        },
        {
            "title": "Family-Centered Integrated Service Campus",
            "summary": "Architectural blueprint for a family-centered integrated service campus co-locating child welfare, early childhood education, health clinic, legal aid, and economic assistance — designed around a central family commons with playground and community kitchen.",
            "category": "integrated-campus",
            "tags": "campus,co-location,family-centered,integrated",
            "details": {"co_located_services": ["Child welfare office", "Head Start/Early Head Start", "Federally qualified health center", "Legal aid office", "SNAP/TANF/Medicaid enrollment", "Workforce development center"], "shared_spaces": ["Family commons with playground", "Community kitchen and pantry", "Quiet study room", "Lactation room", "Children's library"]},
            "impact_range": (5, 5), "feasibility_range": (2, 3), "novelty_range": (4, 4), "time_horizons": ["far"],
        },
        {
            "title": "Digital Kiosk Network for Benefits Self-Service",
            "summary": "A network of self-service digital kiosks placed in high-traffic community locations (grocery stores, pharmacies, transit hubs) offering benefit eligibility screening, application initiation, and document upload with multilingual touch interfaces.",
            "category": "digital-kiosks",
            "tags": "kiosk,self-service,community-access,multilingual",
            "details": {"locations": ["Grocery stores", "Pharmacies", "Transit hubs", "Laundromats", "Community health centers"], "capabilities": ["Benefit eligibility screening", "Application initiation", "Document scanning and upload", "Appointment scheduling"], "languages": 12, "accessibility": "ADA-compliant height and screen reader compatible"},
            "impact_range": (4, 4), "feasibility_range": (3, 4), "novelty_range": (3, 4), "time_horizons": ["near", "medium"],
        },
        {
            "title": "Outdoor Service Pavilion Design",
            "summary": "Design specifications for outdoor covered service pavilions suitable for warm-weather months, reducing facility overcrowding and providing stigma-free service access in park-like settings with natural ventilation and open sight lines.",
            "category": "outdoor-services",
            "tags": "outdoor,pavilion,stigma-reduction,seasonal",
            "details": {"structure": "Covered pavilion with electrical, internet, and rain protection", "capacity": "4 service stations + waiting area for 12", "season": "May-October in temperate climates", "advantages": ["Reduced COVID/respiratory transmission", "Stigma reduction", "Pleasant environment", "No interior facility costs"]},
            "impact_range": (3, 4), "feasibility_range": (4, 5), "novelty_range": (4, 4), "time_horizons": ["near"],
        },
        {
            "title": "Trauma-Informed Architecture Checklist",
            "summary": "A 75-point architectural checklist for evaluating and improving government service spaces through a trauma-informed lens — covering sight lines, escape routes, sound privacy, natural elements, and power dynamics embedded in spatial design.",
            "category": "trauma-informed-space",
            "tags": "trauma-informed,architecture,checklist,spatial-design",
            "details": {"categories": ["Sight lines and orientation (15 items)", "Sound privacy and acoustic comfort (12 items)", "Lighting and color (10 items)", "Nature and biophilic elements (8 items)", "Power dynamics in spatial arrangement (10 items)", "Safety and escape routes (10 items)", "Wayfinding and signage (10 items)"], "scoring": "0-5 per item, minimum 280/375 for certification"},
            "impact_range": (3, 4), "feasibility_range": (4, 5), "novelty_range": (4, 5), "time_horizons": ["near"],
        },
        {
            "title": "Co-Working Space for Human Services Caseworkers",
            "summary": "A shared co-working model where caseworkers from multiple agencies work in the same physical space, enabling informal collaboration, spontaneous case consultations, and relationship building that improves cross-agency referral quality.",
            "category": "co-working",
            "tags": "co-working,collaboration,cross-agency,informal-coordination",
            "details": {"model": "Hot-desking co-working space for caseworkers from 4+ agencies", "features": ["Shared kitchen and break room", "Case consultation rooms", "Shared resource library", "Joint training space"], "outcomes": "30% increase in successful cross-agency referrals in pilot sites"},
            "impact_range": (3, 4), "feasibility_range": (4, 5), "novelty_range": (3, 4), "time_horizons": ["near"],
        },
    ],

    # ── 9. Measurement Scientist ────────────────────────────────────────────
    "measurement-scientist": [
        {
            "title": "Two-Generation Outcome Framework",
            "summary": "A measurement framework that simultaneously tracks parent and child outcomes across economic mobility, education, health, and social capital dimensions — capturing the intergenerational transmission of program effects that single-generation metrics miss.",
            "category": "outcome-frameworks",
            "tags": "two-generation,intergenerational,outcome-framework,family",
            "details": {"parent_outcomes": ["Employment and earnings", "Educational attainment", "Housing stability", "Health status"], "child_outcomes": ["School readiness", "Academic achievement", "Health and development", "Social-emotional wellbeing"], "linkage": "Family unit tracking across generations"},
            "impact_range": (4, 5), "feasibility_range": (3, 4), "novelty_range": (4, 5), "time_horizons": ["medium"],
        },
        {
            "title": "Administrative Data-Powered Regression Discontinuity Design",
            "summary": "A practical guide for implementing regression discontinuity designs using administrative data cutoffs that already exist in human services — income thresholds, age cutoffs, geographic boundaries — producing credible causal estimates at minimal cost.",
            "category": "quasi-experimental-designs",
            "tags": "regression-discontinuity,administrative-data,causal-inference,practical",
            "details": {"applicable_cutoffs": ["Income eligibility thresholds (130%, 185%, 200% FPL)", "Age cutoffs (aging out at 18/21)", "Geographic service area boundaries", "Wait list priority scores"], "advantages": "Uses existing data, no random assignment required", "cost": "$50K-$150K for a complete analysis"},
            "impact_range": (4, 5), "feasibility_range": (4, 5), "novelty_range": (3, 4), "time_horizons": ["near"],
        },
        {
            "title": "Client-Defined Outcome Measurement",
            "summary": "A participatory measurement approach where program clients define their own success outcomes at intake and progress is measured against client-set goals — complementing standard program outcomes with person-centered metrics.",
            "category": "participatory-measurement",
            "tags": "client-defined,participatory,person-centered,outcomes",
            "details": {"method": "Goal Attainment Scaling adapted for human services", "process": ["Client identifies 3-5 personal goals at intake", "Scaled outcomes defined collaboratively (worse/expected/better)", "Progress assessed at 3, 6, and 12 months"], "integration": "Reported alongside standard program outcomes"},
            "impact_range": (3, 4), "feasibility_range": (4, 5), "novelty_range": (4, 4), "time_horizons": ["near"],
        },
        {
            "title": "Equity-Stratified Impact Dashboard",
            "summary": "An impact dashboard that disaggregates all program outcomes by race, ethnicity, gender, disability status, and geography — making disparate impacts visible and trackable in real-time rather than discovered months later in annual reports.",
            "category": "equity-measurement",
            "tags": "equity,disaggregation,dashboard,disparities",
            "details": {"stratification_dimensions": ["Race/ethnicity", "Gender", "Disability status", "Geography (urban/suburban/rural)", "Language spoken at home"], "metrics_tracked": "All standard program outcomes disaggregated", "disparity_index": "Automated calculation of disparity ratios with statistical significance testing"},
            "impact_range": (4, 5), "feasibility_range": (4, 5), "novelty_range": (3, 4), "time_horizons": ["near"],
        },
        {
            "title": "Program Cost Accounting Standardization",
            "summary": "A standardized cost accounting methodology for social programs that enables apples-to-apples cost-effectiveness comparisons — allocating overhead, distinguishing fixed from variable costs, and accounting for start-up versus steady-state operations.",
            "category": "cost-accounting",
            "tags": "cost-accounting,standardization,cost-effectiveness,comparability",
            "details": {"methodology": "Activity-based costing adapted for social programs", "cost_categories": ["Direct service delivery", "Administrative overhead", "Training and supervision", "Facilities and technology", "Quality assurance"], "outputs": "Cost per participant, cost per outcome, marginal cost of expansion"},
            "impact_range": (3, 4), "feasibility_range": (4, 5), "novelty_range": (3, 3), "time_horizons": ["near"],
        },
        {
            "title": "Bayesian Adaptive Trial Design for Policy Pilots",
            "summary": "A Bayesian adaptive trial design that allows policy pilots to reallocate participants between intervention arms as evidence accumulates — ensuring more participants receive the more effective intervention while still generating rigorous evidence.",
            "category": "adaptive-trials",
            "tags": "bayesian,adaptive,policy-pilot,ethical-design",
            "details": {"design": "Multi-arm bandit with Thompson sampling", "ethical_advantage": "Minimizes participants assigned to inferior arms", "statistical_approach": "Bayesian posterior probability of superiority", "decision_rules": "Stop arm for futility at < 5% posterior probability of best"},
            "impact_range": (4, 5), "feasibility_range": (3, 4), "novelty_range": (5, 5), "time_horizons": ["medium"],
        },
        {
            "title": "Long-Term Follow-Up Infrastructure",
            "summary": "A shared infrastructure for 10-year follow-up of social program participants using administrative data linkage — enabling long-term outcome tracking that reveals delayed program effects on employment, health, housing, and justice involvement.",
            "category": "longitudinal-measurement",
            "tags": "longitudinal,long-term,follow-up,administrative-data",
            "details": {"follow_up_period": "10 years post-program exit", "data_sources": "Linked administrative data (wage records, Medicaid claims, corrections, vital statistics)", "consent": "Obtained at program enrollment for long-term follow-up", "cost_sharing": "Shared infrastructure costs across 10+ participating programs"},
            "impact_range": (4, 5), "feasibility_range": (3, 4), "novelty_range": (4, 4), "time_horizons": ["medium", "far"],
        },
        {
            "title": "Implementation Fidelity Monitoring System",
            "summary": "An automated implementation fidelity monitoring system that tracks whether evidence-based programs are being delivered as designed — flagging deviations in dosage, content, timing, and staffing before they compromise outcomes.",
            "category": "fidelity-monitoring",
            "tags": "fidelity,implementation,monitoring,evidence-based",
            "details": {"dimensions_monitored": ["Service dosage (hours/contacts delivered)", "Content adherence (curriculum completion)", "Staff qualifications and training", "Caseload ratios", "Timeliness of service initiation"], "data_collection": "Automated extraction from service delivery records", "alert_system": "Dashboard alerts when fidelity drops below 80% threshold"},
            "impact_range": (3, 4), "feasibility_range": (4, 5), "novelty_range": (3, 4), "time_horizons": ["near"],
        },
    ],

    # ── 10. Narrative Researcher ────────────────────────────────────────────
    "narrative-researcher": [
        {
            "title": "Participatory Action Research on Benefit Cliff Experiences",
            "summary": "A participatory action research project where 20 families experiencing benefit cliffs co-design the research questions, collect data through peer interviews, and present findings directly to legislative committees as expert witnesses.",
            "category": "participatory-action-research",
            "tags": "PAR,benefit-cliff,co-research,legislative-testimony",
            "details": {"co_researchers": "20 families currently experiencing benefit cliffs", "method": "Peer interviews + photovoice + financial diary", "training": "40-hour research methods training for co-researchers", "advocacy": "Direct legislative testimony as expert witnesses", "compensation": "$200/month for 6-month research period"},
            "impact_range": (4, 5), "feasibility_range": (3, 4), "novelty_range": (4, 5), "time_horizons": ["medium"],
        },
        {
            "title": "Oral History Archive: Child Welfare System Alumni",
            "summary": "A professionally recorded oral history archive preserving the long-term narratives of 50 adults who experienced foster care as children — documenting not just system experiences but entire life arcs to inform permanency and aftercare policy.",
            "category": "oral-history",
            "tags": "oral-history,foster-care,alumni,long-term-narratives",
            "details": {"participants": 50, "interview_format": "3-session life history (childhood, system experience, adult life)", "duration": "3-4 hours per participant across 3 sessions", "archive": "University library special collections with digital access", "ethical_framework": "Full narrative control, right to redact, perpetual consent review"},
            "impact_range": (3, 4), "feasibility_range": (4, 5), "novelty_range": (3, 4), "time_horizons": ["near", "medium"],
        },
        {
            "title": "Caseworker Narrative Inquiry: Moral Distress in Practice",
            "summary": "A narrative inquiry study exploring moral distress among child welfare caseworkers — the anguish of knowing the right thing to do but being constrained by system resources, policies, or caseloads from doing it.",
            "category": "narrative-inquiry",
            "tags": "narrative-inquiry,moral-distress,caseworker,workforce",
            "details": {"participants": "25 current and 10 former caseworkers", "method": "Semi-structured narrative interviews with follow-up member checking", "focus": ["Situations where policy conflicted with client need", "Resource constraints forcing suboptimal decisions", "Impact on professional identity and retention"], "output": "Thematic analysis published in peer-reviewed journal + agency brief"},
            "impact_range": (3, 4), "feasibility_range": (4, 5), "novelty_range": (4, 4), "time_horizons": ["near"],
        },
        {
            "title": "Community Mapping Through Storytelling",
            "summary": "A community asset mapping project where residents identify and document neighborhood resources, informal support networks, and cultural institutions through storytelling walks — revealing assets invisible to formal service directories.",
            "category": "community-mapping",
            "tags": "community-mapping,storytelling,assets,neighborhood",
            "details": {"method": "Storytelling walks with GPS tracking and audio recording", "participants": "60 residents from 6 neighborhoods", "outputs": ["Interactive digital map with story pins", "Neighborhood asset inventory", "Informal support network diagrams", "Policy recommendations for asset-based investment"], "duration": "4 months of fieldwork"},
            "impact_range": (3, 4), "feasibility_range": (4, 5), "novelty_range": (4, 4), "time_horizons": ["near"],
        },
        {
            "title": "Policy Impact Storytelling Toolkit",
            "summary": "A toolkit enabling human services agencies to systematically collect, curate, and present client stories as evidence in policy deliberations — with ethical guidelines, consent protocols, and narrative analysis frameworks.",
            "category": "storytelling-methods",
            "tags": "toolkit,policy-storytelling,ethical-guidelines,evidence",
            "details": {"components": ["Story collection protocol with trauma-informed guidelines", "Digital consent framework with right-to-withdraw", "Narrative analysis template (thematic + structural)", "Presentation formats for different audiences (legislative, media, public)"], "ethical_standards": "IRB-equivalent review for non-academic settings"},
            "impact_range": (3, 4), "feasibility_range": (5, 5), "novelty_range": (3, 3), "time_horizons": ["near"],
        },
        {
            "title": "Youth Participatory Evaluation Using Digital Media",
            "summary": "A participatory evaluation methodology where youth in government programs create short films, podcasts, and social media content documenting their program experiences — producing both evaluation data and authentic communication materials.",
            "category": "youth-participatory",
            "tags": "youth,digital-media,participatory-evaluation,creative",
            "details": {"participants": "15-20 youth ages 14-21", "media_formats": ["Short documentary films (3-5 minutes)", "Podcast episodes (15-20 minutes)", "Instagram/TikTok content series"], "training": "12-week media production + research ethics training", "dual_output": "Evaluation findings + shareable communication content"},
            "impact_range": (3, 4), "feasibility_range": (4, 5), "novelty_range": (4, 5), "time_horizons": ["near"],
        },
        {
            "title": "Cross-Cultural Narrative Methods Adaptation Guide",
            "summary": "A guide for adapting narrative research methods across cultural contexts — addressing translation, cultural protocols, relationship building, and meaning-making differences that affect the validity of story-based research with diverse populations.",
            "category": "cultural-adaptation",
            "tags": "cross-cultural,adaptation,methodology,validity",
            "details": {"cultures_addressed": ["Latinx immigrant communities", "African American communities", "Indigenous nations", "Southeast Asian refugee communities", "Arabic-speaking communities"], "adaptations": ["Language and translation protocols", "Community entry and relationship building", "Culturally specific narrative structures", "Community review and ownership of findings"]},
            "impact_range": (3, 4), "feasibility_range": (4, 5), "novelty_range": (3, 4), "time_horizons": ["near"],
        },
        {
            "title": "Lived Experience Research Fellowship",
            "summary": "A 12-month research fellowship for individuals with deep personal experience in government systems, providing research methods training, mentorship, and a stipend to conduct original narrative research on topics they define.",
            "category": "research-fellowship",
            "tags": "fellowship,lived-experience,research-training,empowerment",
            "details": {"fellows": "8 per annual cohort", "stipend": "$40,000 for 12 months", "training": "Graduate-level qualitative research methods", "mentorship": "Paired with university faculty advisor", "output": "Original research paper + community presentation"},
            "impact_range": (4, 5), "feasibility_range": (3, 4), "novelty_range": (4, 5), "time_horizons": ["medium"],
        },
    ],

    # ── 11. Market Maker ────────────────────────────────────────────────────
    "market-maker": [
        {
            "title": "Cooperative Home Care Worker Agency",
            "summary": "A worker-owned cooperative model for home care agencies where direct care workers own the business, set their own schedules, receive 90% of billing rates, and build equity through patronage dividends — addressing the caregiver shortage through worker empowerment.",
            "category": "cooperative-models",
            "tags": "cooperative,home-care,worker-ownership,caregiver-shortage",
            "details": {"structure": "Worker-owned cooperative (one member, one vote)", "revenue_share": "90% of billing rate to workers (vs. 55% industry average)", "benefits": ["Health insurance at 20 hours/week", "Paid training hours", "Annual patronage dividend", "Democratic governance"], "precedent": "Cooperative Home Care Associates (Bronx, NY)"},
            "impact_range": (4, 5), "feasibility_range": (3, 4), "novelty_range": (3, 4), "time_horizons": ["medium"],
        },
        {
            "title": "Social Enterprise Revenue Model for Workforce Training",
            "summary": "A social enterprise model where workforce training programs generate revenue through client-produced goods and services — screen printing, catering, landscaping, IT services — creating self-sustaining training programs less dependent on grant cycles.",
            "category": "social-enterprise",
            "tags": "social-enterprise,workforce-training,revenue,sustainability",
            "details": {"enterprise_types": ["Screen printing and apparel", "Catering and food production", "Landscaping and maintenance", "IT helpdesk and refurbishment"], "revenue_target": "60% of operating costs from enterprise revenue by year 3", "training_model": "Learn-and-earn: trainees receive wages while building skills"},
            "impact_range": (4, 5), "feasibility_range": (3, 4), "novelty_range": (3, 4), "time_horizons": ["medium"],
        },
        {
            "title": "Health-Focused Community Land Trust",
            "summary": "A community land trust specifically designed to co-locate permanently affordable housing with health-promoting infrastructure — community gardens, walking paths, health clinic space, and commercial kitchen for nutrition education.",
            "category": "community-land-trusts",
            "tags": "CLT,health,housing,community-garden",
            "details": {"housing_units": "30 permanently affordable units", "health_infrastructure": ["Community garden (0.5 acre)", "Walking and exercise path", "Ground-floor health clinic space", "Commercial teaching kitchen"], "health_outcomes_tracked": "BMI, blood pressure, diabetes management, food security"},
            "impact_range": (4, 5), "feasibility_range": (3, 4), "novelty_range": (4, 4), "time_horizons": ["medium"],
        },
        {
            "title": "Benefit Corporation Incubator for Human Services Spinoffs",
            "summary": "An incubator that helps government agencies spin off innovative programs as benefit corporations — maintaining public mission while gaining operational flexibility, diverse revenue streams, and freedom from procurement constraints.",
            "category": "benefit-corporations",
            "tags": "benefit-corp,incubator,government-spinoff,flexibility",
            "details": {"target": "High-performing government programs seeking operational independence", "support": ["Legal structure setup", "Business plan development", "Board recruitment", "Revenue diversification strategy"], "governance": "Government retains board seats and mission veto", "timeline": "18-month incubation from concept to independent operation"},
            "impact_range": (4, 5), "feasibility_range": (2, 3), "novelty_range": (5, 5), "time_horizons": ["medium", "far"],
        },
        {
            "title": "Mutual Aid Technology Platform",
            "summary": "An open-source technology platform for organizing neighborhood mutual aid networks — matching needs with offers, tracking exchanges, facilitating group purchases, and connecting to formal services when mutual aid is insufficient.",
            "category": "mutual-aid",
            "tags": "mutual-aid,platform,open-source,neighborhood",
            "details": {"features": ["Need/offer matching algorithm", "SMS and web interfaces", "Group purchasing coordination", "Formal service referral integration", "Privacy-preserving (no data sold)"], "governance": "Community-governed with elected moderators", "cost": "Free for community groups, hosted by municipal IT departments"},
            "impact_range": (3, 4), "feasibility_range": (4, 5), "novelty_range": (3, 4), "time_horizons": ["near"],
        },
        {
            "title": "Pay-What-You-Can Social Enterprise Cafe",
            "summary": "A pay-what-you-can community cafe that provides workforce training in food service, creates a dignified dining option for food-insecure individuals, and serves as an informal community gathering space — funded through a cross-subsidy model.",
            "category": "social-enterprise",
            "tags": "pay-what-you-can,cafe,food-security,workforce-training",
            "details": {"model": "Suggested prices with pay-what-you-can option", "revenue_mix": "40% full-price, 30% reduced-price, 20% pay-it-forward, 10% free", "training": "6-month food service certification program for 12 trainees/year", "community_functions": "Meeting space, job posting board, resource library"},
            "impact_range": (3, 4), "feasibility_range": (3, 4), "novelty_range": (3, 4), "time_horizons": ["near", "medium"],
        },
        {
            "title": "Community Currency for Local Economic Development",
            "summary": "A complementary community currency that circulates among local businesses and service providers in underserved neighborhoods, keeping economic value within the community and providing a medium of exchange when dollars are scarce.",
            "category": "community-currency",
            "tags": "community-currency,local-economy,circular,alternative-exchange",
            "details": {"mechanism": "Digital community currency backed by local business commitments", "circulation": "Accepted by 50+ local businesses within target neighborhood", "conversion": "Earned through community service, redeemable at participating businesses", "governance": "Community currency board with resident majority"},
            "impact_range": (3, 4), "feasibility_range": (3, 4), "novelty_range": (4, 5), "time_horizons": ["medium"],
        },
        {
            "title": "Employee Ownership Transition Fund",
            "summary": "A fund that finances the conversion of retiring small business owners' companies to employee-owned cooperatives, preserving local businesses and creating wealth-building pathways for low-wage workers in communities facing business succession crises.",
            "category": "employee-ownership",
            "tags": "employee-ownership,succession,cooperative-conversion,wealth-building",
            "details": {"target": "Small businesses (10-50 employees) with retiring owners", "financing": "Patient capital loans for employee buyouts (7-10 year terms)", "technical_assistance": "Cooperative governance training and business planning", "wealth_effect": "Average employee-owner accumulates $25K-$50K in equity over 5 years"},
            "impact_range": (4, 5), "feasibility_range": (3, 4), "novelty_range": (4, 4), "time_horizons": ["medium"],
        },
    ],

    # ── 12. Architect ───────────────────────────────────────────────────────
    "architect": [
        {
            "title": "Phased Implementation Roadmap for Integrated Human Services",
            "summary": "A 5-year phased implementation roadmap that sequences all 12 innovation domains into a coherent transformation strategy — starting with regulatory and data foundations, layering in service redesign and financing, and culminating in measurement and narrative documentation.",
            "category": "implementation-planning",
            "tags": "roadmap,phased-implementation,sequencing,transformation",
            "details": {"phases": [{"year": 1, "focus": "Foundation", "domains": ["regulatory-reform", "data-innovation"]}, {"year": 2, "focus": "Enablement", "domains": ["model-legislation", "service-design"]}, {"year": 3, "focus": "Innovation", "domains": ["creative-financing", "emerging-technology", "space-design"]}, {"year": 4, "focus": "Scaling", "domains": ["impact-investment", "social-markets"]}, {"year": 5, "focus": "Sustainability", "domains": ["impact-measurement", "narrative-research", "system-integration"]}]},
            "impact_range": (5, 5), "feasibility_range": (2, 3), "novelty_range": (4, 5), "time_horizons": ["far"],
        },
        {
            "title": "Innovation Portfolio Risk Assessment",
            "summary": "A portfolio-level risk assessment analyzing the collective risk profile of all active innovations — identifying concentration risks, dependency chains, political vulnerabilities, and technology risks, with mitigation strategies for each.",
            "category": "risk-management",
            "tags": "risk-assessment,portfolio,mitigation,strategy",
            "details": {"risk_categories": ["Political/leadership change risk", "Technology maturity risk", "Funding sustainability risk", "Regulatory reversal risk", "Implementation complexity risk"], "assessment_method": "Probability x Impact matrix with dependency overlay", "output": "Quarterly portfolio risk report with updated mitigations"},
            "impact_range": (4, 4), "feasibility_range": (4, 5), "novelty_range": (3, 4), "time_horizons": ["near"],
        },
        {
            "title": "Cross-Domain Innovation Synthesis: Benefits Access Reimagined",
            "summary": "A synthesis of innovations across 8 domains into a unified vision for reimagined benefits access — combining automatic enrollment (legislation), digital identity (technology), no-wrong-door (service), and virtual hubs (space) into one coherent system.",
            "category": "synthesis",
            "tags": "synthesis,benefits-access,cross-domain,unified-vision",
            "details": {"integrated_innovations": [{"domain": "model-legislation", "contribution": "Automatic enrollment authorization"}, {"domain": "emerging-technology", "contribution": "Digital identity wallet"}, {"domain": "service-design", "contribution": "No-wrong-door triage protocol"}, {"domain": "space-design", "contribution": "Virtual service hub"}, {"domain": "data-innovation", "contribution": "Cross-system data spine"}, {"domain": "regulatory-reform", "contribution": "Cross-agency MOU framework"}, {"domain": "impact-measurement", "contribution": "Equity-stratified outcome tracking"}, {"domain": "creative-financing", "contribution": "Braided funding pool"}], "user_experience": "Single identity, automatic eligibility, proactive enrollment, any-channel access"},
            "impact_range": (5, 5), "feasibility_range": (2, 3), "novelty_range": (5, 5), "time_horizons": ["far"],
        },
        {
            "title": "Stakeholder Alignment Mapping Tool",
            "summary": "A diagnostic tool that maps stakeholder positions (support, neutral, oppose) across all proposed innovations, identifies coalition-building opportunities, and generates engagement strategies for moving fence-sitters toward support.",
            "category": "stakeholder-analysis",
            "tags": "stakeholder,alignment,coalition,strategy",
            "details": {"stakeholder_categories": ["Elected officials", "Agency leadership", "Front-line workers and unions", "Client advocacy organizations", "Private sector partners", "Academic/research community"], "analysis_dimensions": ["Level of support (1-5)", "Influence over outcome (1-5)", "Key concerns and interests", "Engagement strategy"], "output": "Interactive stakeholder map with engagement playbook"},
            "impact_range": (3, 4), "feasibility_range": (5, 5), "novelty_range": (3, 3), "time_horizons": ["near"],
        },
        {
            "title": "Innovation Impact Multiplier Analysis",
            "summary": "An analysis quantifying the multiplier effects when innovations from different domains are combined — showing that integrated implementation produces 2.5x-4x the impact of isolated individual innovations.",
            "category": "impact-analysis",
            "tags": "multiplier,combined-impact,synergy,quantification",
            "details": {"methodology": "Comparative analysis of isolated vs. integrated implementation sites", "finding": "Integrated implementation produces 2.5x-4x impact of isolated deployment", "key_multiplier_pairs": [{"pair": "Data infrastructure + Measurement frameworks", "multiplier": "3.2x"}, {"pair": "Regulatory reform + Service redesign", "multiplier": "2.8x"}, {"pair": "Financing innovation + Technology deployment", "multiplier": "2.5x"}]},
            "impact_range": (4, 5), "feasibility_range": (3, 4), "novelty_range": (4, 5), "time_horizons": ["medium"],
        },
        {
            "title": "Lab Governance Framework and Decision Protocol",
            "summary": "The governance framework for the DOMES Innovation Lab itself — establishing how innovations are proposed, evaluated, prioritized, and advanced through the pipeline, with decision rights, resource allocation criteria, and accountability structures.",
            "category": "governance",
            "tags": "governance,decision-protocol,prioritization,accountability",
            "details": {"pipeline_stages": ["Ideation", "Feasibility assessment", "Prototype/pilot", "Evaluation", "Scale/mainstream"], "decision_criteria": ["Impact potential (30%)", "Feasibility (25%)", "Equity lens (20%)", "Innovation novelty (15%)", "Stakeholder readiness (10%)"], "governance_body": "Innovation Council with cross-domain representation + client advisory board"},
            "impact_range": (3, 4), "feasibility_range": (5, 5), "novelty_range": (3, 3), "time_horizons": ["near"],
        },
        {
            "title": "Technology Stack Integration Architecture",
            "summary": "The technical architecture for integrating data systems, service platforms, and measurement tools across all 12 innovation domains — specifying APIs, data standards, authentication, and interoperability requirements.",
            "category": "technical-architecture",
            "tags": "architecture,integration,APIs,interoperability",
            "details": {"layers": ["Data layer: Federated data spine with NIEM standards", "Service layer: RESTful APIs with OAuth 2.0", "Presentation layer: Universal design system", "Analytics layer: Shared measurement warehouse"], "standards": ["NIEM Human Services domain", "HL7 FHIR for health data", "XBRL for financial reporting", "W3C Verifiable Credentials for identity"]},
            "impact_range": (4, 5), "feasibility_range": (3, 4), "novelty_range": (3, 4), "time_horizons": ["medium"],
        },
        {
            "title": "Annual Innovation Lab State of Practice Report",
            "summary": "A comprehensive annual report documenting the Lab's innovations, outcomes, lessons learned, and strategic direction — serving as both accountability document and knowledge product for the broader human services innovation field.",
            "category": "knowledge-management",
            "tags": "annual-report,knowledge-management,field-building,accountability",
            "details": {"sections": ["Executive summary and key metrics", "Innovation portfolio review (all 12 domains)", "Outcomes achieved and evidence generated", "Lessons learned and failure analysis", "Strategic direction for coming year", "Financial report"], "distribution": "500+ government agencies, foundations, and academic institutions"},
            "impact_range": (3, 4), "feasibility_range": (5, 5), "novelty_range": (2, 3), "time_horizons": ["near"],
        },
    ],
}


def generate_innovation(db: Session, slug: str) -> Innovation | None:
    """
    Generate a new innovation for the teammate identified by *slug*.

    Picks a random template from the domain's template bank, applies randomized
    scores within the template's defined ranges, and persists the new Innovation
    to the database.

    Returns the created Innovation, or None if the slug is unknown.
    """
    teammate: Teammate | None = db.query(Teammate).filter(Teammate.slug == slug).first()
    if not teammate:
        return None

    templates = DOMAIN_TEMPLATES.get(slug)
    if not templates:
        return None

    template = random.choice(templates)

    impact = random.randint(*template["impact_range"])
    feasibility = random.randint(*template["feasibility_range"])
    novelty = random.randint(*template["novelty_range"])
    time_horizon = random.choice(template["time_horizons"])
    status = random.choice(["draft", "draft", "review"])  # bias toward draft

    innovation = Innovation(
        teammate_id=teammate.id,
        title=template["title"],
        summary=template["summary"],
        domain=teammate.domain,
        category=template.get("category", "general"),
        impact_level=impact,
        feasibility=feasibility,
        novelty=novelty,
        time_horizon=time_horizon,
        status=status,
        details=json.dumps(template.get("details", {})),
        tags=template.get("tags", ""),
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )

    db.add(innovation)
    db.commit()
    db.refresh(innovation)

    return innovation
