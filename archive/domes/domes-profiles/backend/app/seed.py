"""
Seed data for DOMES Profiles.

Five sample profiles with pre-computed realistic data that work without
upstream services. Each profile tells a compelling story about the human
cost of fragmented government data systems.
"""

import logging
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from .models import Profile, ProfileDomain

logger = logging.getLogger(__name__)


def seed_profiles(db: Session) -> None:
    """Insert sample profiles if the database is empty."""
    existing = db.query(Profile).filter(Profile.is_sample == True).count()  # noqa: E712
    if existing > 0:
        logger.info("Seed data already exists (%d sample profiles), skipping.", existing)
        return

    logger.info("Seeding 5 sample profiles...")

    profiles = [
        _marcus_thompson(),
        _sarah_chen(),
        _james_williams(),
        _maria_rodriguez(),
        _robert_jackson(),
    ]

    for profile_data in profiles:
        profile = profile_data["profile"]
        db.add(profile)
        db.flush()  # Get the profile ID
        for domain in profile_data["domains"]:
            domain.profile_id = profile.id
            db.add(domain)

    db.commit()
    logger.info("Seeded %d sample profiles.", len(profiles))


# ===========================================================================
# Profile 1: Marcus Thompson
# ===========================================================================

def _marcus_thompson() -> dict:
    """
    Age 34, male, recently released from prison, substance use disorder,
    on Medicaid, homeless. Classic reentry case showing the revolving door.
    """
    profile = Profile(
        id="sample-marcus-thompson",
        name="Marcus Thompson",
        version=1,
        created_at=datetime(2025, 1, 15, tzinfo=timezone.utc),
        updated_at=datetime(2025, 1, 15, tzinfo=timezone.utc),
        circumstances={
            "is_recently_released": True,
            "has_substance_use": True,
            "is_on_medicaid": True,
            "is_homeless": True,
            "is_on_probation": True,
            "is_on_snap": True,
            "is_unemployed": True,
        },
        systems_involved=[
            "doc", "medicaid", "bha", "hmis", "probation",
            "snap", "unemployment", "mco", "pdmp", "shelter",
        ],
        total_annual_cost=87400.0,
        coordinated_annual_cost=34200.0,
        savings_annual=53200.0,
        five_year_projection=266000.0,
        lifetime_estimate=1085280.0,
        narrative=(
            "Marcus Thompson is 34 years old and was released from state prison "
            "six months ago after serving three years for a non-violent drug offense. "
            "He has a substance use disorder and is currently homeless, cycling between "
            "emergency shelters and the street. He is on Medicaid, receiving SNAP benefits, "
            "and reports to a probation officer monthly. He has no stable employment. "
            "Marcus interacts with at least 10 separate government data systems across "
            "4 domains. None of these systems share data with each other by default. "
            "His probation officer cannot see his treatment progress. His shelter intake "
            "worker has no visibility into his Medicaid coverage or behavioral health plan. "
            "His substance use counselor does not know about his housing status. "
            "The annual cost of serving Marcus in this fragmented system is approximately "
            "$87,400. With coordinated data sharing — achievable through existing legal "
            "mechanisms like 42 CFR Part 2 consent and reentry MOUs — that cost could "
            "drop to $34,200, a savings of $53,200 per year. Over five years, coordination "
            "would save taxpayers $266,000 for this single individual. The fragmentation "
            "is not just expensive — it is the primary barrier to Marcus's recovery."
        ),
        is_sample=True,
    )

    domains = [
        ProfileDomain(
            domain="health",
            domain_label="Health",
            systems=[
                {"id": "medicaid", "label": "Medicaid", "annual_cost": 12000, "coord_savings_pct": 0.35},
                {"id": "bha", "label": "Behavioral Health", "annual_cost": 18000, "coord_savings_pct": 0.45},
                {"id": "mco", "label": "Managed Care Org", "annual_cost": 14000, "coord_savings_pct": 0.30},
                {"id": "pdmp", "label": "Prescription Drug Monitoring", "annual_cost": 1500, "coord_savings_pct": 0.50},
            ],
            provisions_count=6,
            annual_cost=45500.0,
            coordinated_cost=23350.0,
            savings=22150.0,
            top_provisions=[
                {"id": "prov_h1", "title": "42 CFR Part 2 - SUD Record Confidentiality", "type": "federal",
                 "relevance": "Governs sharing of Marcus's substance use treatment records. Consent-based sharing could enable coordinated care."},
                {"id": "prov_h2", "title": "HIPAA Privacy Rule - Treatment/Payment/Operations", "type": "federal",
                 "relevance": "Allows sharing for treatment coordination without additional consent in many cases."},
                {"id": "prov_h3", "title": "ACA Section 2703 - Health Home Services", "type": "federal",
                 "relevance": "Could fund a Health Home model integrating BH and primary care for Marcus."},
                {"id": "prov_h4", "title": "Medicaid 1115 Waiver - SUD Treatment Coverage", "type": "state",
                 "relevance": "Expands Medicaid SUD treatment options available to Marcus."},
                {"id": "prov_h5", "title": "Medicaid Inmate Exclusion Policy - Suspension vs Termination", "type": "federal",
                 "relevance": "Marcus's Medicaid was suspended, not terminated, during incarceration — enabling faster reactivation."},
                {"id": "prov_h6", "title": "SAMHSA Reentry Grant Requirements", "type": "federal",
                 "relevance": "Requires grantees to coordinate SUD treatment with reentry services."},
            ],
            gaps=[
                {"id": "gap_mt_h1", "label": "BH treatment progress not visible to probation officer", "severity": "high",
                 "impact": "Probation may revoke for non-compliance that is actually treatment engagement."},
                {"id": "gap_mt_h2", "label": "Medicaid MCO authorization not shared with BH provider", "severity": "high",
                 "impact": "Treatment delays while BH provider navigates MCO prior authorization blindly."},
                {"id": "gap_mt_h3", "label": "PDMP data not linked to outpatient treatment plan", "severity": "medium",
                 "impact": "Prescriber lacks full picture of medication history during recovery."},
            ],
            bridges=[
                {"id": "bridge_mt_h1", "label": "42 CFR Part 2 consent for SUD records sharing with probation", "type": "consent", "impact": "high",
                 "description": "A single consent form could allow Marcus's treatment provider to share progress updates with his probation officer."},
                {"id": "bridge_mt_h2", "label": "HIE opt-in for cross-provider visibility", "type": "consent", "impact": "high",
                 "description": "Enrolling Marcus in the Health Information Exchange would give all his providers a shared view."},
                {"id": "bridge_mt_h3", "label": "MCO care coordination flag for justice-involved members", "type": "technical", "impact": "medium",
                 "description": "Technical flag in MCO system to prioritize care coordination for recently released members."},
            ],
        ),
        ProfileDomain(
            domain="justice",
            domain_label="Justice",
            systems=[
                {"id": "doc", "label": "Dept of Corrections", "annual_cost": 15000, "coord_savings_pct": 0.50},
                {"id": "probation", "label": "Probation/Parole", "annual_cost": 5000, "coord_savings_pct": 0.40},
            ],
            provisions_count=4,
            annual_cost=20000.0,
            coordinated_cost=9500.0,
            savings=10500.0,
            top_provisions=[
                {"id": "prov_j1", "title": "Second Chance Act - Reentry Programs", "type": "federal",
                 "relevance": "Funds comprehensive reentry services that require data coordination."},
                {"id": "prov_j2", "title": "Medicaid Inmate Exclusion - Suspension Policy", "type": "federal",
                 "relevance": "Allows Medicaid to resume immediately upon release rather than re-application."},
                {"id": "prov_j3", "title": "First Step Act - Federal Reentry Provisions", "type": "federal",
                 "relevance": "Mandates needs assessment and individualized reentry planning."},
                {"id": "prov_j4", "title": "PA Act 122 - County Reentry Coalitions", "type": "state",
                 "relevance": "State mandate for cross-system reentry coordination at county level."},
            ],
            gaps=[
                {"id": "gap_mt_j1", "label": "DOC release plan not shared with community providers", "severity": "high",
                 "impact": "Community providers start from scratch rather than building on institutional treatment progress."},
                {"id": "gap_mt_j2", "label": "Probation compliance data siloed from housing and employment services", "severity": "medium",
                 "impact": "Marcus must separately prove compliance to each agency he works with."},
            ],
            bridges=[
                {"id": "bridge_mt_j1", "label": "Reentry data-sharing MOU between DOC and community BH providers", "type": "policy", "impact": "high",
                 "description": "Memorandum of Understanding allowing DOC to share reentry plan with designated community providers."},
                {"id": "bridge_mt_j2", "label": "Unified case management platform for justice-involved individuals", "type": "technical", "impact": "high",
                 "description": "Shared case management system linking probation, BH, and housing services."},
            ],
        ),
        ProfileDomain(
            domain="housing",
            domain_label="Housing",
            systems=[
                {"id": "hmis", "label": "Homeless Info System", "annual_cost": 8000, "coord_savings_pct": 0.55},
                {"id": "shelter", "label": "Emergency Shelter", "annual_cost": 12000, "coord_savings_pct": 0.60},
            ],
            provisions_count=3,
            annual_cost=20000.0,
            coordinated_cost=7400.0,
            savings=12600.0,
            top_provisions=[
                {"id": "prov_ho1", "title": "McKinney-Vento Act - Homeless Assistance", "type": "federal",
                 "relevance": "Authorizes coordinated entry and continuum of care for people like Marcus."},
                {"id": "prov_ho2", "title": "HEARTH Act - Continuum of Care", "type": "federal",
                 "relevance": "Requires coordinated assessment and data collection via HMIS."},
                {"id": "prov_ho3", "title": "HUD-VASH Voucher (if eligible)", "type": "federal",
                 "relevance": "Combines housing voucher with VA case management — model for non-veteran coordination."},
            ],
            gaps=[
                {"id": "gap_mt_ho1", "label": "HMIS not linked to Medicaid enrollment status", "severity": "high",
                 "impact": "Shelter staff cannot confirm whether Marcus has active health coverage or help him access it."},
                {"id": "gap_mt_ho2", "label": "Shelter intake does not capture BH treatment engagement", "severity": "medium",
                 "impact": "Housing workers unaware of treatment schedule, may schedule conflicting appointments."},
            ],
            bridges=[
                {"id": "bridge_mt_ho1", "label": "Coordinated entry with Medicaid enrollment linkage", "type": "technical", "impact": "high",
                 "description": "Automated check of Medicaid status during HMIS coordinated entry assessment."},
                {"id": "bridge_mt_ho2", "label": "Housing First placement with integrated BH support", "type": "policy", "impact": "high",
                 "description": "Place Marcus in permanent supportive housing with on-site BH services."},
            ],
        ),
        ProfileDomain(
            domain="income",
            domain_label="Income",
            systems=[
                {"id": "snap", "label": "SNAP", "annual_cost": 3600, "coord_savings_pct": 0.20},
                {"id": "unemployment", "label": "Unemployment Comp", "annual_cost": 6000, "coord_savings_pct": 0.30},
            ],
            provisions_count=3,
            annual_cost=9600.0,
            coordinated_cost=7500.0,
            savings=2100.0,
            top_provisions=[
                {"id": "prov_i1", "title": "SNAP - Expedited Benefits for Homeless", "type": "federal",
                 "relevance": "Marcus qualifies for expedited SNAP processing due to homelessness."},
                {"id": "prov_i2", "title": "WIOA - Workforce Innovation & Opportunity Act", "type": "federal",
                 "relevance": "Funds employment training and placement services for ex-offenders."},
                {"id": "prov_i3", "title": "Federal Bonding Program", "type": "federal",
                 "relevance": "Provides fidelity bonds to employers hiring people with criminal records."},
            ],
            gaps=[
                {"id": "gap_mt_i1", "label": "Employment services not linked to probation compliance tracking", "severity": "medium",
                 "impact": "Marcus must separately document employment search for probation and workforce agency."},
            ],
            bridges=[
                {"id": "bridge_mt_i1", "label": "Automated SNAP cross-enrollment at shelter intake", "type": "technical", "impact": "medium",
                 "description": "Auto-check SNAP eligibility and status during HMIS assessment."},
            ],
        ),
    ]

    return {"profile": profile, "domains": domains}


# ===========================================================================
# Profile 2: Sarah Chen
# ===========================================================================

def _sarah_chen() -> dict:
    """
    Age 28, female, single mother, domestic violence survivor,
    on TANF, Section 8, child in foster care.
    """
    profile = Profile(
        id="sample-sarah-chen",
        name="Sarah Chen",
        version=1,
        created_at=datetime(2025, 2, 1, tzinfo=timezone.utc),
        updated_at=datetime(2025, 2, 1, tzinfo=timezone.utc),
        circumstances={
            "has_dv_history": True,
            "is_on_tanf": True,
            "is_section_8": True,
            "is_on_medicaid": True,
            "has_child_in_foster": True,
            "is_on_snap": True,
        },
        systems_involved=[
            "sacwis", "tanf", "pha", "medicaid", "court_cms",
            "snap", "mco",
        ],
        total_annual_cost=72200.0,
        coordinated_annual_cost=29100.0,
        savings_annual=43100.0,
        five_year_projection=215500.0,
        lifetime_estimate=879240.0,
        narrative=(
            "Sarah Chen is a 28-year-old single mother who fled a domestic violence "
            "situation eight months ago. Her 4-year-old daughter was briefly placed in "
            "foster care during the crisis and is now in kinship care with Sarah's sister "
            "while Sarah stabilizes her housing. Sarah has a Section 8 voucher but has been "
            "unable to find a landlord who will accept it. She receives TANF and SNAP benefits "
            "and is on Medicaid. She has an active family court case for custody reunification. "
            "Sarah interacts with 7 separate systems across 4 domains. The child welfare system "
            "(SACWIS) does not share data with the housing authority (PHA). Her family court "
            "case manager cannot see her TANF or Section 8 status. Her daughter's foster care "
            "worker does not have visibility into Sarah's domestic violence services or her "
            "progress on her reunification plan. The annual cost of serving Sarah's family "
            "in this fragmented system is approximately $72,200. Coordination could reduce "
            "this to $29,100 — a savings of $43,100 per year. More importantly, coordination "
            "could accelerate reunification with her daughter by months."
        ),
        is_sample=True,
    )

    domains = [
        ProfileDomain(
            domain="child_welfare",
            domain_label="Child Welfare",
            systems=[
                {"id": "sacwis", "label": "Child Welfare Info System", "annual_cost": 18000, "coord_savings_pct": 0.45},
            ],
            provisions_count=5,
            annual_cost=18000.0,
            coordinated_cost=9900.0,
            savings=8100.0,
            top_provisions=[
                {"id": "prov_cw1", "title": "Title IV-E - Foster Care Assistance", "type": "federal",
                 "relevance": "Funds the foster care placement for Sarah's daughter and reunification services."},
                {"id": "prov_cw2", "title": "Title IV-B - Child & Family Services", "type": "federal",
                 "relevance": "Funds family preservation and reunification services Sarah needs."},
                {"id": "prov_cw3", "title": "CAPTA - Child Abuse Prevention & Treatment Act", "type": "federal",
                 "relevance": "Governs investigation and service response; DV context matters for disposition."},
                {"id": "prov_cw4", "title": "Family First Prevention Services Act", "type": "federal",
                 "relevance": "Allows Title IV-E funds for prevention services that could have kept Sarah's family together."},
                {"id": "prov_cw5", "title": "Adoption and Safe Families Act - Reunification Timelines", "type": "federal",
                 "relevance": "Sets the 15-month reunification clock that Sarah is racing against."},
            ],
            gaps=[
                {"id": "gap_sc_cw1", "label": "SACWIS cannot see Sarah's housing status or Section 8 progress", "severity": "high",
                 "impact": "Child welfare worker cannot verify housing stability — a key reunification requirement."},
                {"id": "gap_sc_cw2", "label": "Foster care provider has no visibility into Sarah's DV service engagement", "severity": "high",
                 "impact": "Foster care plan does not account for Sarah's safety planning progress."},
                {"id": "gap_sc_cw3", "label": "Court CMS reunification timeline not linked to service completion data", "severity": "medium",
                 "impact": "Judge lacks real-time view of Sarah's progress toward reunification benchmarks."},
            ],
            bridges=[
                {"id": "bridge_sc_cw1", "label": "SACWIS-PHA data sharing for housing verification", "type": "technical", "impact": "high",
                 "description": "Automated housing status check from PHA visible in SACWIS case record."},
                {"id": "bridge_sc_cw2", "label": "Unified family services plan across CW, court, and DV services", "type": "policy", "impact": "high",
                 "description": "Single service plan visible to all providers working with Sarah's family."},
            ],
        ),
        ProfileDomain(
            domain="justice",
            domain_label="Justice",
            systems=[
                {"id": "court_cms", "label": "Court Case Mgmt", "annual_cost": 3000, "coord_savings_pct": 0.35},
            ],
            provisions_count=3,
            annual_cost=3000.0,
            coordinated_cost=1950.0,
            savings=1050.0,
            top_provisions=[
                {"id": "prov_sc_j1", "title": "VAWA - Violence Against Women Act", "type": "federal",
                 "relevance": "Provides protections and service funding for Sarah as a DV survivor."},
                {"id": "prov_sc_j2", "title": "Address Confidentiality Program", "type": "state",
                 "relevance": "Protects Sarah's location from her abuser through address substitution."},
                {"id": "prov_sc_j3", "title": "Protection From Abuse Act", "type": "state",
                 "relevance": "Governs Sarah's PFA order and court proceedings."},
            ],
            gaps=[
                {"id": "gap_sc_j1", "label": "DV protection order status not visible to housing providers", "severity": "high",
                 "impact": "Landlords screening Sarah cannot verify she has legal protections in place."},
            ],
            bridges=[
                {"id": "bridge_sc_j1", "label": "Court-DV services information sharing protocol", "type": "policy", "impact": "medium",
                 "description": "Structured data exchange between family court and DV service providers."},
            ],
        ),
        ProfileDomain(
            domain="housing",
            domain_label="Housing",
            systems=[
                {"id": "pha", "label": "Public Housing Auth", "annual_cost": 9600, "coord_savings_pct": 0.25},
            ],
            provisions_count=3,
            annual_cost=9600.0,
            coordinated_cost=7200.0,
            savings=2400.0,
            top_provisions=[
                {"id": "prov_sc_ho1", "title": "Section 8 Housing Choice Voucher Program", "type": "federal",
                 "relevance": "Sarah has an active voucher — the barrier is finding a landlord."},
                {"id": "prov_sc_ho2", "title": "VAWA Housing Protections", "type": "federal",
                 "relevance": "Protects Sarah from eviction due to DV and allows emergency transfers."},
                {"id": "prov_sc_ho3", "title": "FUP Voucher - Family Unification Program", "type": "federal",
                 "relevance": "Prioritizes vouchers for families in the child welfare system to prevent foster care."},
            ],
            gaps=[
                {"id": "gap_sc_ho1", "label": "PHA has no link to SACWIS reunification timeline", "severity": "high",
                 "impact": "Housing search not prioritized based on foster care reunification deadline."},
                {"id": "gap_sc_ho2", "label": "Landlord incentive programs not connected to voucher system", "severity": "medium",
                 "impact": "Sarah cannot easily find landlords willing to accept Section 8 with DV protections."},
            ],
            bridges=[
                {"id": "bridge_sc_ho1", "label": "FUP voucher expedited processing linked to SACWIS timeline", "type": "policy", "impact": "high",
                 "description": "Priority housing placement when child welfare reunification clock is running."},
            ],
        ),
        ProfileDomain(
            domain="income",
            domain_label="Income",
            systems=[
                {"id": "tanf", "label": "TANF", "annual_cost": 7200, "coord_savings_pct": 0.30},
                {"id": "snap", "label": "SNAP", "annual_cost": 3600, "coord_savings_pct": 0.20},
            ],
            provisions_count=3,
            annual_cost=10800.0,
            coordinated_cost=7920.0,
            savings=2880.0,
            top_provisions=[
                {"id": "prov_sc_i1", "title": "TANF - DV Waiver of Work Requirements", "type": "federal",
                 "relevance": "Sarah may qualify for work requirement waiver due to DV circumstances."},
                {"id": "prov_sc_i2", "title": "SNAP - Expedited Benefits", "type": "federal",
                 "relevance": "Sarah qualifies for expedited SNAP due to DV displacement."},
                {"id": "prov_sc_i3", "title": "TANF Family Violence Option", "type": "federal",
                 "relevance": "Allows states to waive TANF requirements that would make DV survivors unsafe."},
            ],
            gaps=[
                {"id": "gap_sc_i1", "label": "TANF work requirements not linked to DV safety planning", "severity": "medium",
                 "impact": "Sarah may be required to seek employment in ways that compromise her safety."},
            ],
            bridges=[
                {"id": "bridge_sc_i1", "label": "Automated DV waiver flag across TANF and SNAP", "type": "technical", "impact": "medium",
                 "description": "DV verification shared once, applied across all benefits programs."},
            ],
        ),
        ProfileDomain(
            domain="health",
            domain_label="Health",
            systems=[
                {"id": "medicaid", "label": "Medicaid", "annual_cost": 12000, "coord_savings_pct": 0.35},
                {"id": "mco", "label": "Managed Care Org", "annual_cost": 14000, "coord_savings_pct": 0.30},
            ],
            provisions_count=3,
            annual_cost=26000.0,
            coordinated_cost=17030.0,
            savings=8970.0,
            top_provisions=[
                {"id": "prov_sc_h1", "title": "HIPAA Privacy Rule - DV Safety Exception", "type": "federal",
                 "relevance": "Allows withholding health records from abuser even if named on insurance."},
                {"id": "prov_sc_h2", "title": "Medicaid - Trauma-Informed Care Coverage", "type": "state",
                 "relevance": "Covers trauma therapy and DV-related mental health services for Sarah."},
                {"id": "prov_sc_h3", "title": "ACA Preventive Services - DV Screening", "type": "federal",
                 "relevance": "Requires DV screening at preventive visits with no cost-sharing."},
            ],
            gaps=[
                {"id": "gap_sc_h1", "label": "Medicaid provider unaware of DV history and safety needs", "severity": "high",
                 "impact": "Provider may inadvertently share information or schedule in unsafe ways."},
                {"id": "gap_sc_h2", "label": "MCO authorization does not account for trauma-informed care needs", "severity": "medium",
                 "impact": "Standard session limits may be inadequate for Sarah's trauma recovery."},
            ],
            bridges=[
                {"id": "bridge_sc_h1", "label": "DV safety flag in Medicaid/MCO system (consent-based)", "type": "consent", "impact": "high",
                 "description": "Opt-in flag alerting providers to DV safety considerations without full disclosure."},
            ],
        ),
    ]

    return {"profile": profile, "domains": domains}


# ===========================================================================
# Profile 3: James Williams
# ===========================================================================

def _james_williams() -> dict:
    """
    Age 52, male, veteran, disabled, chronic health conditions,
    on SSI, VA healthcare + Medicaid dual-eligible.
    """
    profile = Profile(
        id="sample-james-williams",
        name="James Williams",
        version=1,
        created_at=datetime(2025, 2, 10, tzinfo=timezone.utc),
        updated_at=datetime(2025, 2, 10, tzinfo=timezone.utc),
        circumstances={
            "is_va_healthcare": True,
            "is_dual_eligible": True,
            "is_on_medicaid": True,
            "has_chronic_health": True,
            "has_disability": True,
            "is_on_ssi": True,
        },
        systems_involved=[
            "va", "medicaid", "ssa", "pdmp", "hie",
            "mco", "ssi",
        ],
        total_annual_cost=94100.0,
        coordinated_annual_cost=52300.0,
        savings_annual=41800.0,
        five_year_projection=209000.0,
        lifetime_estimate=852720.0,
        narrative=(
            "James Williams is a 52-year-old disabled veteran living in Philadelphia. "
            "He served two tours in Iraq and suffers from PTSD, chronic pain, and Type 2 "
            "diabetes. He is dual-eligible for both VA healthcare and Medicaid, receives SSI "
            "disability benefits, and has multiple chronic conditions requiring ongoing "
            "management. James sees providers in both the VA system and the Medicaid managed "
            "care system — but these systems do not share records. His VA psychiatrist does "
            "not know what medications his Medicaid primary care doctor has prescribed, and "
            "vice versa. His SSI eligibility review requires documentation from both health "
            "systems, which he must gather himself. James interacts with 7 systems across "
            "2 primary domains. The annual cost of his fragmented care is approximately "
            "$94,100. With VA-Medicaid data sharing (technically possible through existing "
            "federal infrastructure) and SSA integration, coordinated cost would be $52,300 "
            "— a savings of $41,800. For James, coordination is not just about money. "
            "It could prevent the dangerous drug interactions that sent him to the ER twice "
            "last year."
        ),
        is_sample=True,
    )

    domains = [
        ProfileDomain(
            domain="health",
            domain_label="Health",
            systems=[
                {"id": "va", "label": "VA Healthcare", "annual_cost": 22000, "coord_savings_pct": 0.40},
                {"id": "medicaid", "label": "Medicaid", "annual_cost": 12000, "coord_savings_pct": 0.35},
                {"id": "mco", "label": "Managed Care Org", "annual_cost": 14000, "coord_savings_pct": 0.30},
                {"id": "hie", "label": "Health Info Exchange", "annual_cost": 2000, "coord_savings_pct": 0.60},
                {"id": "pdmp", "label": "Prescription Drug Monitoring", "annual_cost": 1500, "coord_savings_pct": 0.50},
            ],
            provisions_count=7,
            annual_cost=51500.0,
            coordinated_cost=28350.0,
            savings=23150.0,
            top_provisions=[
                {"id": "prov_jw_h1", "title": "VA-Medicaid Dual Eligible Special Needs Plan", "type": "federal",
                 "relevance": "James qualifies for D-SNP coordinating VA and Medicaid benefits."},
                {"id": "prov_jw_h2", "title": "VA Community Care (MISSION Act)", "type": "federal",
                 "relevance": "Allows James to see community providers when VA wait times are long."},
                {"id": "prov_jw_h3", "title": "HIPAA - Treatment/Payment/Operations Exception", "type": "federal",
                 "relevance": "Permits data sharing between VA and Medicaid providers for treatment."},
                {"id": "prov_jw_h4", "title": "VA-HIE Data Sharing (VHIE Program)", "type": "federal",
                 "relevance": "VA's own program to share data with community HIEs — James can opt in."},
                {"id": "prov_jw_h5", "title": "Prescription Drug Monitoring Program - Interstate Compact", "type": "state",
                 "relevance": "Allows checking James's prescriptions across VA and civilian pharmacies."},
                {"id": "prov_jw_h6", "title": "Medicare-Medicaid Coordination Office Programs", "type": "federal",
                 "relevance": "Federal programs specifically designed for dual-eligible beneficiaries like James."},
                {"id": "prov_jw_h7", "title": "ACA Section 2703 - Health Home for Chronic Conditions", "type": "federal",
                 "relevance": "Could fund an integrated Health Home model for James's multiple chronic conditions."},
            ],
            gaps=[
                {"id": "gap_jw_h1", "label": "VA and Medicaid medication lists not reconciled", "severity": "high",
                 "impact": "James had two ER visits last year from drug interactions between VA and civilian prescriptions."},
                {"id": "gap_jw_h2", "label": "VA mental health records not visible to Medicaid PCP", "severity": "high",
                 "impact": "Primary care doctor prescribes without knowledge of James's PTSD medications."},
                {"id": "gap_jw_h3", "label": "Chronic disease management split across two care teams", "severity": "high",
                 "impact": "Diabetes managed by Medicaid PCP, pain by VA — no unified care plan."},
                {"id": "gap_jw_h4", "label": "HIE enrollment not completed for VA records", "severity": "medium",
                 "impact": "James's VA data not flowing to the state HIE despite technical capability."},
            ],
            bridges=[
                {"id": "bridge_jw_h1", "label": "VA HIE opt-in enrollment (VHIE consent)", "type": "consent", "impact": "high",
                 "description": "James signs one form and his VA records flow to the community HIE, visible to all his providers."},
                {"id": "bridge_jw_h2", "label": "Dual-eligible care coordination through D-SNP enrollment", "type": "technical", "impact": "high",
                 "description": "Enrolling James in a Dual Special Needs Plan that coordinates VA and Medicaid benefits."},
                {"id": "bridge_jw_h3", "label": "Unified medication reconciliation via PDMP integration", "type": "technical", "impact": "high",
                 "description": "Linking PDMP data to both VA and civilian EHRs for a single medication view."},
            ],
        ),
        ProfileDomain(
            domain="income",
            domain_label="Income",
            systems=[
                {"id": "ssi", "label": "SSI", "annual_cost": 10200, "coord_savings_pct": 0.25},
                {"id": "ssa", "label": "Social Security Admin", "annual_cost": 10200, "coord_savings_pct": 0.25},
            ],
            provisions_count=3,
            annual_cost=20400.0,
            coordinated_cost=15300.0,
            savings=5100.0,
            top_provisions=[
                {"id": "prov_jw_i1", "title": "SSI - Disability Benefits for Veterans", "type": "federal",
                 "relevance": "James receives SSI in addition to VA disability compensation."},
                {"id": "prov_jw_i2", "title": "VA Disability Compensation - Service Connected", "type": "federal",
                 "relevance": "James's service-connected disability rating affects both VA and SSI benefits."},
                {"id": "prov_jw_i3", "title": "SSA-VA Data Exchange Agreement", "type": "federal",
                 "relevance": "Existing federal agreement that could automate disability verification between SSA and VA."},
            ],
            gaps=[
                {"id": "gap_jw_i1", "label": "SSI disability review requires manual documentation from both VA and Medicaid", "severity": "high",
                 "impact": "James must gather and submit medical records from two separate systems for annual SSI review."},
                {"id": "gap_jw_i2", "label": "VA disability rating changes not automatically reflected in SSI", "severity": "medium",
                 "impact": "Benefits adjustments delayed by months after VA rating changes."},
            ],
            bridges=[
                {"id": "bridge_jw_i1", "label": "Automated SSA-VA disability verification data exchange", "type": "technical", "impact": "high",
                 "description": "Use existing federal data exchange agreement to automate disability documentation."},
                {"id": "bridge_jw_i2", "label": "Single medical records request for SSI review (VA + Medicaid)", "type": "policy", "impact": "medium",
                 "description": "One records request satisfying both VA and SSA documentation requirements."},
            ],
        ),
    ]

    return {"profile": profile, "domains": domains}


# ===========================================================================
# Profile 4: Maria Rodriguez
# ===========================================================================

def _maria_rodriguez() -> dict:
    """
    Age 16, female, in foster care, special education IEP,
    behavioral health treatment, juvenile justice involved.
    """
    profile = Profile(
        id="sample-maria-rodriguez",
        name="Maria Rodriguez",
        version=1,
        created_at=datetime(2025, 2, 20, tzinfo=timezone.utc),
        updated_at=datetime(2025, 2, 20, tzinfo=timezone.utc),
        circumstances={
            "is_in_foster_care": True,
            "has_iep": True,
            "has_mental_illness": True,
            "is_on_medicaid": True,
            "is_juvenile_justice": True,
            "is_school_age": True,
        },
        systems_involved=[
            "sacwis", "iep", "bha", "medicaid", "court_cms",
            "slds", "juvenile_court", "mco",
        ],
        total_annual_cost=68200.0,
        coordinated_annual_cost=31400.0,
        savings_annual=36800.0,
        five_year_projection=184000.0,
        lifetime_estimate=750720.0,
        narrative=(
            "Maria Rodriguez is 16 years old. She has been in foster care since age 12 "
            "after her mother's parental rights were terminated. She has been in four "
            "different placements in four years. Maria has an IEP for emotional disturbance "
            "and receives behavioral health services through Medicaid. She was recently "
            "adjudicated delinquent for a shoplifting charge and is on juvenile probation. "
            "Maria navigates 8 separate systems across 4 domains. Every time she changes "
            "foster placements, she changes schools — and her IEP must be re-established. "
            "Her behavioral health provider changes with each placement. Her juvenile "
            "probation officer does not have access to her school attendance or her BH "
            "treatment records. Her foster care caseworker does not know her IEP goals. "
            "The annual cost of serving Maria in these fragmented systems is approximately "
            "$68,200. Coordination could reduce this to $31,400 — saving $36,800 per year. "
            "But for Maria, the cost of fragmentation is measured not in dollars but in "
            "lost years: each school change sets her back academically, each provider "
            "change restarts her therapeutic relationship, and each system treats her as "
            "a new case rather than a whole person."
        ),
        is_sample=True,
    )

    domains = [
        ProfileDomain(
            domain="child_welfare",
            domain_label="Child Welfare",
            systems=[
                {"id": "sacwis", "label": "Child Welfare Info System", "annual_cost": 18000, "coord_savings_pct": 0.45},
            ],
            provisions_count=5,
            annual_cost=18000.0,
            coordinated_cost=9900.0,
            savings=8100.0,
            top_provisions=[
                {"id": "prov_mr_cw1", "title": "Title IV-E - Foster Care Assistance", "type": "federal",
                 "relevance": "Funds Maria's foster care placement and independent living preparation."},
                {"id": "prov_mr_cw2", "title": "Chafee Foster Care Independence Program", "type": "federal",
                 "relevance": "Maria will age out in 2 years — Chafee funds transition planning."},
                {"id": "prov_mr_cw3", "title": "ESSA - Foster Care Education Stability Provisions", "type": "federal",
                 "relevance": "Requires school stability when placement changes — Maria has changed schools 4 times."},
                {"id": "prov_mr_cw4", "title": "Fostering Connections Act - Educational Stability", "type": "federal",
                 "relevance": "Mandates transportation to school of origin when placement changes."},
                {"id": "prov_mr_cw5", "title": "Family First Prevention Services Act", "type": "federal",
                 "relevance": "Limits congregate care and funds therapeutic foster care for Maria."},
            ],
            gaps=[
                {"id": "gap_mr_cw1", "label": "Foster placement changes not linked to school enrollment system", "severity": "high",
                 "impact": "Maria loses weeks of school each time she moves — SACWIS and SLDS are disconnected."},
                {"id": "gap_mr_cw2", "label": "Caseworker cannot see IEP status or school performance", "severity": "high",
                 "impact": "Foster care plan does not account for Maria's educational needs."},
                {"id": "gap_mr_cw3", "label": "Aging-out planning not coordinated with education or employment data", "severity": "medium",
                 "impact": "Maria will age out of foster care in 2 years with no coordinated transition plan."},
            ],
            bridges=[
                {"id": "bridge_mr_cw1", "label": "SACWIS-SLDS data match under ESSA foster care provisions", "type": "policy", "impact": "high",
                 "description": "Automated notification to school when placement changes, triggering ESSA stability protections."},
                {"id": "bridge_mr_cw2", "label": "Unified transition plan linking CW, education, and BH services", "type": "technical", "impact": "high",
                 "description": "Single transition plan for aging out that incorporates IEP goals, BH treatment, and independent living skills."},
            ],
        ),
        ProfileDomain(
            domain="education",
            domain_label="Education",
            systems=[
                {"id": "iep", "label": "IEP / Special Ed", "annual_cost": 12000, "coord_savings_pct": 0.35},
                {"id": "slds", "label": "Student Longitudinal Data", "annual_cost": 1500, "coord_savings_pct": 0.50},
            ],
            provisions_count=4,
            annual_cost=13500.0,
            coordinated_cost=8550.0,
            savings=4950.0,
            top_provisions=[
                {"id": "prov_mr_e1", "title": "IDEA - IEP Portability Requirements", "type": "federal",
                 "relevance": "Requires new school to implement comparable IEP services immediately upon transfer."},
                {"id": "prov_mr_e2", "title": "FERPA - Education Records Transfer", "type": "federal",
                 "relevance": "Governs how Maria's school records transfer between districts."},
                {"id": "prov_mr_e3", "title": "ESSA Title I - Foster Care Educational Liaison", "type": "federal",
                 "relevance": "Requires each LEA to designate a foster care point of contact for students like Maria."},
                {"id": "prov_mr_e4", "title": "IDEA-FERPA Exception for Child Welfare Agencies", "type": "federal",
                 "relevance": "Allows education records sharing with child welfare agencies for foster youth."},
            ],
            gaps=[
                {"id": "gap_mr_e1", "label": "IEP does not transfer automatically when Maria changes schools", "severity": "high",
                 "impact": "Maria goes weeks without special education services after each move."},
                {"id": "gap_mr_e2", "label": "BH treatment progress not available to IEP team", "severity": "high",
                 "impact": "IEP goals for emotional disturbance set without knowledge of Maria's BH treatment plan."},
                {"id": "gap_mr_e3", "label": "School attendance data not visible to juvenile probation", "severity": "medium",
                 "impact": "Probation officer cannot verify school compliance without manual documentation."},
            ],
            bridges=[
                {"id": "bridge_mr_e1", "label": "Automated IEP transfer through SLDS when placement changes", "type": "technical", "impact": "high",
                 "description": "IEP follows Maria through the student data system when foster placement triggers school change."},
                {"id": "bridge_mr_e2", "label": "FERPA-HIPAA consent for IEP-BH data sharing", "type": "consent", "impact": "high",
                 "description": "Aligned consent under both FERPA and HIPAA allowing BH and IEP teams to coordinate."},
            ],
        ),
        ProfileDomain(
            domain="health",
            domain_label="Health",
            systems=[
                {"id": "bha", "label": "Behavioral Health", "annual_cost": 18000, "coord_savings_pct": 0.45},
                {"id": "medicaid", "label": "Medicaid", "annual_cost": 12000, "coord_savings_pct": 0.35},
                {"id": "mco", "label": "Managed Care Org", "annual_cost": 14000, "coord_savings_pct": 0.30},
            ],
            provisions_count=4,
            annual_cost=44000.0,
            coordinated_cost=25800.0,
            savings=18200.0,
            top_provisions=[
                {"id": "prov_mr_h1", "title": "EPSDT - Early & Periodic Screening", "type": "federal",
                 "relevance": "Maria is entitled to comprehensive Medicaid screening including BH assessment."},
                {"id": "prov_mr_h2", "title": "Medicaid - Therapeutic Foster Care Coverage", "type": "state",
                 "relevance": "Funds enhanced foster care with integrated BH support for Maria."},
                {"id": "prov_mr_h3", "title": "HIPAA - Minor's Rights to BH Record Privacy", "type": "federal",
                 "relevance": "Governs Maria's privacy rights over her own BH records as a minor."},
                {"id": "prov_mr_h4", "title": "42 CFR Part 2 - Consent for Minor SUD Records", "type": "federal",
                 "relevance": "Applicable if Maria has any substance use treatment records."},
            ],
            gaps=[
                {"id": "gap_mr_h1", "label": "BH provider changes with each foster placement", "severity": "high",
                 "impact": "Maria has had 4 different therapists in 4 years — each starting from scratch."},
                {"id": "gap_mr_h2", "label": "BH records not transferred between Medicaid MCOs when placement changes", "severity": "high",
                 "impact": "New MCO has no treatment history; Maria must repeat intake assessments."},
            ],
            bridges=[
                {"id": "bridge_mr_h1", "label": "BH treatment record portability through HIE for foster youth", "type": "technical", "impact": "high",
                 "description": "Maria's BH records follow her through the HIE regardless of placement or MCO changes."},
                {"id": "bridge_mr_h2", "label": "Therapeutic continuity requirement in foster care contracts", "type": "policy", "impact": "high",
                 "description": "Require MCOs to maintain BH provider continuity across placement changes."},
            ],
        ),
        ProfileDomain(
            domain="justice",
            domain_label="Justice",
            systems=[
                {"id": "juvenile_court", "label": "Juvenile Court", "annual_cost": 8000, "coord_savings_pct": 0.45},
                {"id": "court_cms", "label": "Court Case Mgmt", "annual_cost": 3000, "coord_savings_pct": 0.35},
            ],
            provisions_count=3,
            annual_cost=11000.0,
            coordinated_cost=5850.0,
            savings=5150.0,
            top_provisions=[
                {"id": "prov_mr_j1", "title": "Juvenile Justice & Delinquency Prevention Act", "type": "federal",
                 "relevance": "Governs Maria's treatment in the juvenile justice system; emphasizes diversion."},
                {"id": "prov_mr_j2", "title": "Crossover Youth Practice Model", "type": "policy",
                 "relevance": "Framework for coordinating CW and JJ responses for dual-system youth like Maria."},
                {"id": "prov_mr_j3", "title": "Juvenile Court Confidentiality Provisions", "type": "state",
                 "relevance": "Governs what juvenile justice information can be shared and with whom."},
            ],
            gaps=[
                {"id": "gap_mr_j1", "label": "Juvenile probation has no access to school attendance or BH progress", "severity": "high",
                 "impact": "Probation requirements set without understanding Maria's school or treatment schedule."},
                {"id": "gap_mr_j2", "label": "Dual-system (CW+JJ) youth not identified for coordinated response", "severity": "high",
                 "impact": "Maria's CW and JJ cases proceed independently despite being deeply interrelated."},
            ],
            bridges=[
                {"id": "bridge_mr_j1", "label": "Dual-system youth screening at juvenile court intake", "type": "policy", "impact": "high",
                 "description": "Automated SACWIS check at juvenile court intake to identify crossover youth like Maria."},
                {"id": "bridge_mr_j2", "label": "Shared case plan between JJ and CW caseworkers", "type": "technical", "impact": "high",
                 "description": "Joint case plan visible to both juvenile probation and foster care caseworker."},
            ],
        ),
    ]

    return {"profile": profile, "domains": domains}


# ===========================================================================
# Profile 5: Robert Jackson
# ===========================================================================

def _robert_jackson() -> dict:
    """
    Age 45, male, chronic homelessness, severe mental illness,
    frequent ER user, on Medicaid, SNAP.
    """
    profile = Profile(
        id="sample-robert-jackson",
        name="Robert Jackson",
        version=1,
        created_at=datetime(2025, 3, 1, tzinfo=timezone.utc),
        updated_at=datetime(2025, 3, 1, tzinfo=timezone.utc),
        circumstances={
            "is_homeless": True,
            "has_mental_illness": True,
            "is_frequent_er": True,
            "is_on_medicaid": True,
            "is_on_snap": True,
            "has_chronic_health": True,
        },
        systems_involved=[
            "hmis", "medicaid", "bha", "snap", "hie",
            "mco", "er_frequent", "shelter", "pdmp",
        ],
        total_annual_cost=112100.0,
        coordinated_annual_cost=41200.0,
        savings_annual=70900.0,
        five_year_projection=354500.0,
        lifetime_estimate=1446360.0,
        narrative=(
            "Robert Jackson is 45 years old and has been chronically homeless for over "
            "seven years. He has a diagnosis of schizoaffective disorder and co-occurring "
            "chronic health conditions including COPD and hypertension. Robert is one of "
            "the city's highest-cost individuals: he visited the emergency room 47 times "
            "last year, each visit costing an average of $2,800. He is on Medicaid and "
            "receives SNAP benefits. He cycles between emergency shelters, the street, "
            "the ER, and occasional psychiatric inpatient stays. Robert interacts with "
            "9 systems across 3 domains, but no single system has a complete picture of "
            "him. The ER treats his acute symptoms but cannot see his BH treatment history "
            "or housing status. The shelter records his bed nights but not his health "
            "conditions. His Medicaid MCO authorizes services but cannot coordinate across "
            "the fragmented provider network. The annual cost of Robert's fragmented care "
            "is approximately $112,100 — making him one of the most expensive individuals "
            "in the system. With coordination through permanent supportive housing, "
            "integrated BH care, and connected data systems, that cost could drop to "
            "$41,200 — a 63% reduction. Robert represents the strongest possible case "
            "for data integration: the most expensive, the most fragmented, and the most "
            "likely to benefit from coordination."
        ),
        is_sample=True,
    )

    domains = [
        ProfileDomain(
            domain="health",
            domain_label="Health",
            systems=[
                {"id": "medicaid", "label": "Medicaid", "annual_cost": 12000, "coord_savings_pct": 0.35},
                {"id": "bha", "label": "Behavioral Health", "annual_cost": 18000, "coord_savings_pct": 0.45},
                {"id": "mco", "label": "Managed Care Org", "annual_cost": 14000, "coord_savings_pct": 0.30},
                {"id": "hie", "label": "Health Info Exchange", "annual_cost": 2000, "coord_savings_pct": 0.60},
                {"id": "er_frequent", "label": "Frequent ER Use", "annual_cost": 28000, "coord_savings_pct": 0.65},
                {"id": "pdmp", "label": "Prescription Drug Monitoring", "annual_cost": 1500, "coord_savings_pct": 0.50},
            ],
            provisions_count=7,
            annual_cost=75500.0,
            coordinated_cost=30600.0,
            savings=44900.0,
            top_provisions=[
                {"id": "prov_rj_h1", "title": "ACA Section 2703 - Health Home for High Utilizers", "type": "federal",
                 "relevance": "Robert qualifies as a super-utilizer for a Medicaid Health Home with care coordination."},
                {"id": "prov_rj_h2", "title": "Medicaid 1115 Waiver - Housing-Related Services", "type": "state",
                 "relevance": "Allows Medicaid to fund housing-related services for high-cost enrollees like Robert."},
                {"id": "prov_rj_h3", "title": "42 CFR Part 2 - SUD Record Sharing (if applicable)", "type": "federal",
                 "relevance": "Governs sharing of any substance use records across Robert's providers."},
                {"id": "prov_rj_h4", "title": "HIPAA - Emergency Treatment Exception", "type": "federal",
                 "relevance": "Allows ER to access Robert's records during emergencies — but only if they exist in a shared system."},
                {"id": "prov_rj_h5", "title": "Medicaid Super-Utilizer Programs", "type": "state",
                 "relevance": "State program targeting the highest-cost Medicaid enrollees for intensive coordination."},
                {"id": "prov_rj_h6", "title": "SAMHSA PATH Program - Homeless Mental Health", "type": "federal",
                 "relevance": "Funds outreach and treatment for people with SMI who are homeless."},
                {"id": "prov_rj_h7", "title": "Community Paramedicine / Mobile Crisis Programs", "type": "state",
                 "relevance": "Alternative to ER for Robert's non-emergency crises — if providers can access his records."},
            ],
            gaps=[
                {"id": "gap_rj_h1", "label": "ER has no access to Robert's BH treatment plan or medications", "severity": "high",
                 "impact": "47 ER visits per year, each starting from scratch without treatment history."},
                {"id": "gap_rj_h2", "label": "BH provider does not know when Robert visits the ER", "severity": "high",
                 "impact": "No follow-up or care plan adjustment after ER crises."},
                {"id": "gap_rj_h3", "label": "MCO cannot identify Robert as high-utilizer for targeted intervention", "severity": "high",
                 "impact": "MCO data does not integrate ER, BH, and shelter utilization for a whole-person view."},
                {"id": "gap_rj_h4", "label": "Shelter health screening data not shared with Medicaid providers", "severity": "medium",
                 "impact": "Health issues identified at shelter intake not communicated to Robert's care team."},
            ],
            bridges=[
                {"id": "bridge_rj_h1", "label": "HIE enrollment with ER notification to BH provider", "type": "consent", "impact": "high",
                 "description": "Robert opts into HIE so his BH provider is notified within 24 hours of any ER visit."},
                {"id": "bridge_rj_h2", "label": "Super-utilizer care coordination through Health Home model", "type": "technical", "impact": "high",
                 "description": "Single care coordinator with access to all of Robert's health data across systems."},
                {"id": "bridge_rj_h3", "label": "Mobile crisis team with real-time access to Robert's care plan", "type": "technical", "impact": "high",
                 "description": "Crisis responders can see Robert's medications, diagnoses, and preferred interventions on-scene."},
            ],
        ),
        ProfileDomain(
            domain="housing",
            domain_label="Housing",
            systems=[
                {"id": "hmis", "label": "Homeless Info System", "annual_cost": 8000, "coord_savings_pct": 0.55},
                {"id": "shelter", "label": "Emergency Shelter", "annual_cost": 12000, "coord_savings_pct": 0.60},
            ],
            provisions_count=4,
            annual_cost=20000.0,
            coordinated_cost=6400.0,
            savings=13600.0,
            top_provisions=[
                {"id": "prov_rj_ho1", "title": "McKinney-Vento Act - Continuum of Care for Chronic Homelessness", "type": "federal",
                 "relevance": "Robert meets the HUD definition of chronically homeless — eligible for permanent supportive housing."},
                {"id": "prov_rj_ho2", "title": "HEARTH Act - Chronic Homelessness Priority", "type": "federal",
                 "relevance": "Requires CoC to prioritize chronically homeless individuals like Robert for PSH."},
                {"id": "prov_rj_ho3", "title": "Medicaid 1115 Waiver - Housing Transition Services", "type": "state",
                 "relevance": "Allows Medicaid to pay for housing transition services when Robert is placed."},
                {"id": "prov_rj_ho4", "title": "Section 811 - Supportive Housing for Disabled", "type": "federal",
                 "relevance": "Robert's disability qualifies him for Section 811 supportive housing."},
            ],
            gaps=[
                {"id": "gap_rj_ho1", "label": "HMIS not linked to Medicaid claims for cost analysis", "severity": "high",
                 "impact": "Cannot demonstrate to funders that housing Robert would reduce Medicaid costs."},
                {"id": "gap_rj_ho2", "label": "Shelter system has no visibility into Robert's health crises", "severity": "high",
                 "impact": "Shelter staff cannot provide appropriate support during mental health episodes."},
                {"id": "gap_rj_ho3", "label": "Coordinated entry VI-SPDAT score does not include health utilization data", "severity": "medium",
                 "impact": "Robert's vulnerability score may not reflect his true acuity based on health system use."},
            ],
            bridges=[
                {"id": "bridge_rj_ho1", "label": "HMIS-Medicaid data match for super-utilizer identification", "type": "technical", "impact": "high",
                 "description": "Link HMIS and Medicaid data to identify the highest-cost homeless individuals for PSH."},
                {"id": "bridge_rj_ho2", "label": "Housing First placement with on-site BH and primary care", "type": "policy", "impact": "high",
                 "description": "Place Robert in PSH with integrated health services — the evidence-based solution."},
            ],
        ),
        ProfileDomain(
            domain="income",
            domain_label="Income",
            systems=[
                {"id": "snap", "label": "SNAP", "annual_cost": 3600, "coord_savings_pct": 0.20},
            ],
            provisions_count=2,
            annual_cost=3600.0,
            coordinated_cost=2880.0,
            savings=720.0,
            top_provisions=[
                {"id": "prov_rj_i1", "title": "SNAP - Homeless Shelter Deduction", "type": "federal",
                 "relevance": "Robert qualifies for simplified SNAP application as a homeless individual."},
                {"id": "prov_rj_i2", "title": "SSI - Presumptive Disability for Homeless with SMI", "type": "federal",
                 "relevance": "Robert likely qualifies for SSI based on his schizoaffective disorder — but has never applied."},
            ],
            gaps=[
                {"id": "gap_rj_i1", "label": "Robert likely SSI-eligible but has never been connected to application", "severity": "high",
                 "impact": "Missing $10,000+/year in disability benefits that could fund housing."},
                {"id": "gap_rj_i2", "label": "SNAP recertification difficult without stable address", "severity": "medium",
                 "impact": "Robert's SNAP benefits lapse periodically due to missed recertification mailings."},
            ],
            bridges=[
                {"id": "bridge_rj_i1", "label": "SOAR application for SSI through homeless services", "type": "technical", "impact": "high",
                 "description": "Use SOAR (SSI/SSDI Outreach, Access, and Recovery) to file SSI application for Robert."},
                {"id": "bridge_rj_i2", "label": "SNAP recertification linked to HMIS contact", "type": "technical", "impact": "medium",
                 "description": "Trigger SNAP recertification through shelter check-in rather than mailed notice."},
            ],
        ),
    ]

    return {"profile": profile, "domains": domains}
