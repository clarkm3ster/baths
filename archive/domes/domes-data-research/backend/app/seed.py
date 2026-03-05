"""Seed data: government data systems, connections, and gaps.

This is the data archaeologist's inventory — every system that touches
complex populations, how they're connected, and where the gaps are.
"""

import json
from sqlalchemy.orm import Session
from app.models import System, Connection, Gap


def seed_all(db: Session) -> dict[str, int]:
    if db.query(System).count() > 0:
        return {"systems": 0, "connections": 0, "gaps": 0}

    systems = _seed_systems(db)
    connections = _seed_connections(db)
    gaps = _seed_gaps(db)
    db.commit()
    return {"systems": systems, "connections": connections, "gaps": gaps}


def _j(lst: list) -> str:
    return json.dumps(lst)


# ---------------------------------------------------------------------------
# SYSTEMS
# ---------------------------------------------------------------------------

def _seed_systems(db: Session) -> int:
    systems = [
        # ===== HEALTH =====
        System(
            id="mmis",
            name="Medicaid Management Information System",
            acronym="MMIS",
            agency="State Medicaid Agency",
            domain="health",
            description="Core claims processing and eligibility system for Medicaid. Contains every encounter, diagnosis, prescription, and provider interaction for Medicaid beneficiaries.",
            data_standard="X12",
            data_held=_j(["demographics", "eligibility", "claims", "encounters", "diagnoses", "prescriptions", "providers", "prior_authorizations"]),
            who_can_access=_j(["state_medicaid_agency", "cms", "mcos_contracted", "providers_treating"]),
            privacy_law="HIPAA",
            privacy_laws=_j(["HIPAA", "42 CFR Part 431"]),
            applies_when=_j(["medicaid", "chip"]),
            is_federal=False,
            state_operated=True,
        ),
        System(
            id="mco",
            name="Managed Care Organization Systems",
            acronym="MCO",
            agency="Contracted MCOs",
            domain="health",
            description="Each MCO (e.g., Aetna Better Health, UnitedHealthcare Community Plan) maintains its own member management, care coordination, and claims systems. Data is fragmented across 3-6 MCOs per state.",
            data_standard="mixed",
            data_held=_j(["demographics", "eligibility", "claims", "care_plans", "care_management_notes", "utilization_reviews", "provider_networks"]),
            who_can_access=_j(["mco_staff", "care_managers", "state_medicaid_agency_limited"]),
            privacy_law="HIPAA",
            privacy_laws=_j(["HIPAA", "state_contract"]),
            applies_when=_j(["medicaid"]),
            is_federal=False,
            state_operated=False,
        ),
        System(
            id="bh_authority",
            name="Behavioral Health Authority System",
            acronym="BHA",
            agency="State/County Behavioral Health Authority",
            domain="health",
            description="Tracks individuals receiving publicly-funded mental health and substance use treatment. In many states, this is a separate system from Medicaid with its own intake, assessment, and outcome tracking.",
            data_standard="custom",
            data_held=_j(["demographics", "diagnoses", "treatment_episodes", "substance_use_history", "mental_health_assessments", "crisis_events", "involuntary_commitments", "medications"]),
            who_can_access=_j(["bh_authority_staff", "contracted_providers", "state_medicaid_limited"]),
            privacy_law="42 CFR Part 2",
            privacy_laws=_j(["HIPAA", "42 CFR Part 2", "state_mental_health_act"]),
            applies_when=_j(["mental_health", "sud"]),
            is_federal=False,
            state_operated=True,
        ),
        System(
            id="ehr_cmhc",
            name="Community Mental Health Center EHR",
            acronym="CMHC EHR",
            agency="Community Mental Health Centers",
            domain="health",
            description="Electronic health records at community mental health centers. Often a different EHR vendor than hospitals. Contains detailed clinical notes, treatment plans, and crisis intervention records.",
            data_standard="HL7",
            data_held=_j(["demographics", "clinical_notes", "treatment_plans", "medications", "crisis_plans", "therapy_notes", "psychosocial_assessments"]),
            who_can_access=_j(["treating_clinicians", "clinical_supervisors"]),
            privacy_law="42 CFR Part 2",
            privacy_laws=_j(["HIPAA", "42 CFR Part 2"]),
            applies_when=_j(["mental_health", "sud"]),
            is_federal=False,
            state_operated=False,
        ),
        System(
            id="hie",
            name="Health Information Exchange",
            acronym="HIE",
            agency="State/Regional HIE Organization",
            domain="health",
            description="Aggregates clinical data from hospitals, labs, and some providers. The primary bridge between health systems, but participation is often incomplete — behavioral health and corrections rarely connected.",
            data_standard="FHIR",
            data_held=_j(["demographics", "lab_results", "hospital_admissions", "discharge_summaries", "medications", "allergies", "immunizations"]),
            who_can_access=_j(["participating_providers", "hospitals", "state_agencies_with_agreement"]),
            privacy_law="HIPAA",
            privacy_laws=_j(["HIPAA", "state_HIE_statute"]),
            applies_when=_j(["medicaid", "medicare", "private", "uninsured"]),
            is_federal=False,
            state_operated=True,
        ),
        System(
            id="pdmp",
            name="Prescription Drug Monitoring Program",
            acronym="PDMP",
            agency="State Board of Pharmacy / DOH",
            domain="health",
            description="Tracks all controlled substance prescriptions dispensed in the state. Used to identify potential misuse patterns. Prescribers and pharmacists required to check before prescribing.",
            data_standard="custom",
            data_held=_j(["patient_demographics", "controlled_substance_prescriptions", "prescriber_info", "pharmacy_info", "fill_dates"]),
            who_can_access=_j(["prescribers", "pharmacists", "state_board", "law_enforcement_with_warrant"]),
            privacy_law="state_PDMP_statute",
            privacy_laws=_j(["state_PDMP_statute", "HIPAA"]),
            applies_when=_j(["sud", "chronic_illness"]),
            is_federal=False,
            state_operated=True,
        ),
        System(
            id="vital_records",
            name="Vital Records System",
            acronym="VR",
            agency="State Department of Health",
            domain="health",
            description="Birth certificates, death certificates, marriage/divorce records. Critical for establishing identity and eligibility for benefits, but often completely disconnected from service systems.",
            data_standard="flat_file",
            data_held=_j(["birth_records", "death_records", "marriage_records", "fetal_death_records", "demographics"]),
            who_can_access=_j(["state_registrar", "authorized_requestors", "funeral_directors"]),
            privacy_law="state_vital_records_act",
            privacy_laws=_j(["state_vital_records_act", "HIPAA_limited"]),
            applies_when=_j(["medicaid", "medicare", "private", "uninsured", "chip"]),
            is_federal=False,
            state_operated=True,
        ),

        # ===== JUSTICE =====
        System(
            id="doc",
            name="Department of Corrections System",
            acronym="DOC",
            agency="State Department of Corrections",
            domain="justice",
            description="Manages incarcerated individuals: sentence, facility assignment, health records (separate from community systems), release dates, disciplinary records. Health data in corrections is almost completely siloed from community health systems.",
            data_standard="custom",
            data_held=_j(["demographics", "sentence_info", "facility_assignment", "health_records", "mental_health_records", "medications", "disciplinary_records", "release_dates", "reentry_plans"]),
            who_can_access=_j(["corrections_staff", "corrections_healthcare", "parole_board"]),
            privacy_law="state_corrections_statute",
            privacy_laws=_j(["HIPAA_limited", "state_corrections_statute", "CJIS_policy"]),
            applies_when=_j(["incarcerated", "recently_released"]),
            is_federal=False,
            state_operated=True,
        ),
        System(
            id="cjis",
            name="Criminal Justice Information System",
            acronym="CJIS",
            agency="State Police / FBI",
            domain="justice",
            description="Criminal history records, warrants, sex offender registry. Contains arrest records, charges, dispositions, and fingerprint data. Governed by strict FBI CJIS Security Policy.",
            data_standard="custom",
            data_held=_j(["criminal_history", "arrest_records", "warrants", "sex_offender_status", "fingerprints", "mugshots", "dispositions"]),
            who_can_access=_j(["law_enforcement", "prosecutors", "courts", "some_employers_with_consent"]),
            privacy_law="CJIS_Security_Policy",
            privacy_laws=_j(["CJIS_Security_Policy", "state_criminal_records_act", "28_CFR_Part_20"]),
            applies_when=_j(["incarcerated", "recently_released", "probation", "juvenile_justice"]),
            is_federal=True,
            state_operated=False,
        ),
        System(
            id="probation",
            name="Probation/Parole Management System",
            acronym="P&P",
            agency="State/County Probation Department",
            domain="justice",
            description="Tracks individuals on community supervision: conditions, check-ins, drug tests, employment status, treatment compliance. Officers often have no access to health or housing data about their supervisees.",
            data_standard="custom",
            data_held=_j(["demographics", "supervision_conditions", "check_in_records", "drug_test_results", "employment_status", "residence_address", "violation_reports", "risk_assessments"]),
            who_can_access=_j(["probation_officers", "judges", "prosecutors"]),
            privacy_law="state_probation_statute",
            privacy_laws=_j(["state_probation_statute", "CJIS_policy_limited"]),
            applies_when=_j(["probation", "recently_released"]),
            is_federal=False,
            state_operated=True,
        ),
        System(
            id="courts",
            name="Court Case Management System",
            acronym="CMS",
            agency="State/County Courts",
            domain="justice",
            description="Docket management, case records, orders, plea agreements, sentencing records. Each county may run a different system. Public records but rarely integrated with service systems.",
            data_standard="custom",
            data_held=_j(["case_filings", "docket_entries", "orders", "sentencing_records", "plea_agreements", "protective_orders", "custody_orders"]),
            who_can_access=_j(["judges", "court_staff", "attorneys_of_record", "public_limited"]),
            privacy_law="state_court_rules",
            privacy_laws=_j(["state_court_rules", "state_public_records_act"]),
            applies_when=_j(["incarcerated", "recently_released", "probation", "juvenile_justice"]),
            is_federal=False,
            state_operated=True,
        ),

        # ===== HOUSING =====
        System(
            id="hmis",
            name="Homeless Management Information System",
            acronym="HMIS",
            agency="HUD / Continuum of Care",
            domain="housing",
            description="Tracks individuals experiencing homelessness across shelters, outreach, transitional housing, and permanent supportive housing. Federally mandated by HUD. Uses a standardized data dictionary but implementations vary by community.",
            data_standard="custom",
            data_held=_j(["demographics", "shelter_stays", "housing_history", "disability_status", "income", "benefits", "domestic_violence_flag", "chronic_homelessness_status", "vulnerability_index"]),
            who_can_access=_j(["hmis_lead_agency", "participating_providers", "hud_aggregated"]),
            privacy_law="HUD_HMIS_standards",
            privacy_laws=_j(["HUD_HMIS_data_standards", "VAWA_protections", "state_homeless_services_statute"]),
            applies_when=_j(["homeless"]),
            is_federal=True,
            state_operated=False,
        ),
        System(
            id="pha",
            name="Public Housing Authority System",
            acronym="PHA",
            agency="Local Housing Authority",
            domain="housing",
            description="Manages Section 8 vouchers, public housing units, waitlists, and tenant records. Tracks income, family composition, lease compliance, and inspections. Each PHA runs its own system.",
            data_standard="flat_file",
            data_held=_j(["demographics", "income_verification", "family_composition", "voucher_status", "unit_assignment", "lease_compliance", "inspection_records", "waitlist_position"]),
            who_can_access=_j(["pha_staff", "hud_aggregated"]),
            privacy_law="HUD_privacy_requirements",
            privacy_laws=_j(["HUD_privacy_requirements", "Privacy_Act"]),
            applies_when=_j(["section_8", "public_housing"]),
            is_federal=False,
            state_operated=False,
        ),

        # ===== INCOME / BENEFITS =====
        System(
            id="ssa",
            name="Social Security Administration Systems",
            acronym="SSA",
            agency="Social Security Administration",
            domain="income",
            description="Manages SSI, SSDI, retirement, and survivors benefits. Contains detailed disability determination records, work history, earnings, and benefit payment data. Federal system with state disability determination services.",
            data_standard="custom",
            data_held=_j(["demographics", "work_history", "earnings_records", "disability_determinations", "benefit_amounts", "representative_payee", "overpayment_records"]),
            who_can_access=_j(["ssa_staff", "disability_determination_services", "authorized_representatives"]),
            privacy_law="Privacy_Act",
            privacy_laws=_j(["Privacy_Act", "Social_Security_Act"]),
            applies_when=_j(["ssi", "ssdi"]),
            is_federal=True,
            state_operated=False,
        ),
        System(
            id="snap_system",
            name="SNAP Eligibility System",
            acronym="SNAP/EBT",
            agency="State Department of Human Services",
            domain="income",
            description="Determines SNAP eligibility, issues EBT cards, tracks benefits. In many states, this is part of an integrated eligibility system that also handles TANF and Medicaid.",
            data_standard="flat_file",
            data_held=_j(["demographics", "income_verification", "household_composition", "benefit_amounts", "transaction_history", "recertification_dates"]),
            who_can_access=_j(["dhs_eligibility_workers", "usda_aggregated"]),
            privacy_law="Privacy_Act",
            privacy_laws=_j(["Privacy_Act", "7_CFR_Part_272"]),
            applies_when=_j(["snap", "below_poverty"]),
            is_federal=False,
            state_operated=True,
        ),
        System(
            id="tanf_system",
            name="TANF Case Management System",
            acronym="TANF",
            agency="State Department of Human Services",
            domain="income",
            description="Manages Temporary Assistance for Needy Families cases: eligibility, work requirements, sanctions, time limits. Often same agency as SNAP but may be a different system.",
            data_standard="flat_file",
            data_held=_j(["demographics", "income", "employment_status", "work_participation", "sanctions", "time_limit_clock", "child_care_needs"]),
            who_can_access=_j(["dhs_caseworkers", "hhs_aggregated"]),
            privacy_law="Privacy_Act",
            privacy_laws=_j(["Privacy_Act", "45_CFR_Part_205"]),
            applies_when=_j(["tanf", "below_poverty"]),
            is_federal=False,
            state_operated=True,
        ),
        System(
            id="unemployment",
            name="Unemployment Insurance System",
            acronym="UI",
            agency="State Department of Labor",
            domain="income",
            description="Processes unemployment claims, determines eligibility, tracks employer contributions. Contains wage records that are valuable for verifying income across systems.",
            data_standard="flat_file",
            data_held=_j(["demographics", "employment_history", "wage_records", "claim_status", "benefit_amounts", "employer_info"]),
            who_can_access=_j(["dol_staff", "authorized_state_agencies"]),
            privacy_law="state_UI_statute",
            privacy_laws=_j(["state_UI_statute", "20_CFR_Part_603"]),
            applies_when=_j(["unemployed"]),
            is_federal=False,
            state_operated=True,
        ),

        # ===== EDUCATION =====
        System(
            id="state_doe",
            name="State Education Data System",
            acronym="SLDS",
            agency="State Department of Education",
            domain="education",
            description="Statewide longitudinal data system tracking students from pre-K through postsecondary. Contains enrollment, attendance, test scores, graduation status, and special education eligibility.",
            data_standard="custom",
            data_held=_j(["demographics", "enrollment", "attendance", "test_scores", "graduation_status", "disciplinary_records", "special_education_status"]),
            who_can_access=_j(["state_doe_staff", "school_districts", "researchers_with_agreement"]),
            privacy_law="FERPA",
            privacy_laws=_j(["FERPA", "state_student_privacy_act"]),
            applies_when=_j(["under_18", "18_to_21"]),
            is_federal=False,
            state_operated=True,
        ),
        System(
            id="iep_system",
            name="IEP/Special Education System",
            acronym="IEP",
            agency="School Districts",
            domain="education",
            description="Manages Individualized Education Programs for students with disabilities. Contains evaluations, goals, accommodations, related services, and transition plans. Highly sensitive, governed by both FERPA and IDEA.",
            data_standard="custom",
            data_held=_j(["demographics", "disability_category", "evaluations", "iep_goals", "accommodations", "related_services", "transition_plans", "progress_monitoring"]),
            who_can_access=_j(["iep_team_members", "parents", "school_administrators"]),
            privacy_law="FERPA",
            privacy_laws=_j(["FERPA", "IDEA", "state_special_education_code"]),
            applies_when=_j(["under_18", "18_to_21", "idd", "mental_health", "physical"]),
            is_federal=False,
            state_operated=False,
        ),

        # ===== CHILD WELFARE =====
        System(
            id="sacwis",
            name="Child Welfare Information System",
            acronym="SACWIS/CCWIS",
            agency="State Child Welfare Agency",
            domain="child_welfare",
            description="Statewide Automated Child Welfare Information System (or newer CCWIS). Tracks child abuse/neglect reports, investigations, foster care placements, adoption, and case management. One of the most data-rich systems about vulnerable families.",
            data_standard="custom",
            data_held=_j(["demographics", "abuse_neglect_reports", "investigation_findings", "foster_placements", "case_plans", "court_orders", "adoption_records", "family_assessments", "safety_plans"]),
            who_can_access=_j(["child_welfare_workers", "foster_parents_limited", "courts", "gal_casa"]),
            privacy_law="state_child_welfare_statute",
            privacy_laws=_j(["CAPTA", "state_child_welfare_statute", "Fostering_Connections_Act"]),
            applies_when=_j(["foster_care", "under_18"]),
            is_federal=False,
            state_operated=True,
        ),

        # ===== VETERANS =====
        System(
            id="va_system",
            name="Veterans Health Information Systems",
            acronym="VistA/EHRM",
            agency="Department of Veterans Affairs",
            domain="health",
            description="VA's electronic health record (transitioning from VistA to Oracle Health EHRM). Contains comprehensive health data for enrolled veterans. Historically one of the most complete EHR systems but poorly connected to non-VA community systems.",
            data_standard="HL7",
            data_held=_j(["demographics", "military_service", "service_connected_disabilities", "health_records", "mental_health_records", "medications", "appointments", "benefits_enrollment"]),
            who_can_access=_j(["va_clinicians", "va_benefits_staff", "community_care_providers_limited"]),
            privacy_law="38_USC_5701",
            privacy_laws=_j(["38_USC_5701", "Privacy_Act", "HIPAA"]),
            applies_when=_j(["veteran"]),
            is_federal=True,
            state_operated=False,
        ),
    ]

    for s in systems:
        db.add(s)
    db.flush()
    return len(systems)


# ---------------------------------------------------------------------------
# CONNECTIONS (where data actually flows today)
# ---------------------------------------------------------------------------

def _seed_connections(db: Session) -> int:
    connections = [
        # Health <-> Health
        Connection(source_id="mmis", target_id="mco", direction="bidirectional",
                   frequency="daily", format="X12",
                   data_shared=_j(["eligibility", "claims", "encounters"]),
                   description="MMIS sends eligibility files to MCOs daily; MCOs submit encounter data back. This is the primary health data exchange but misses care coordination details.",
                   reliability="high"),
        Connection(source_id="hie", target_id="mmis", direction="unidirectional",
                   frequency="batch", format="HL7",
                   data_shared=_j(["hospital_admissions", "discharge_summaries"]),
                   description="HIE sends admission/discharge/transfer notifications to Medicaid. Helps identify ER utilization but incomplete for behavioral health.",
                   reliability="moderate"),
        Connection(source_id="hie", target_id="mco", direction="bidirectional",
                   frequency="realtime", format="FHIR",
                   data_shared=_j(["lab_results", "hospital_admissions", "medications"]),
                   description="MCOs increasingly connected to HIE for real-time notifications. Quality varies significantly by MCO.",
                   reliability="moderate"),
        Connection(source_id="pdmp", target_id="hie", direction="unidirectional",
                   frequency="daily", format="custom",
                   data_shared=_j(["controlled_substance_prescriptions"]),
                   description="Some states integrate PDMP data into the HIE so prescribers can check in-workflow.",
                   reliability="moderate"),

        # Income systems
        Connection(source_id="mmis", target_id="snap_system", direction="bidirectional",
                   frequency="batch", format="flat_file",
                   data_shared=_j(["eligibility_status", "demographics"]),
                   description="Many states have integrated eligibility systems where Medicaid and SNAP share a common application. Data flows are batch-based and often incomplete.",
                   reliability="moderate"),
        Connection(source_id="snap_system", target_id="tanf_system", direction="bidirectional",
                   frequency="realtime", format="flat_file",
                   data_shared=_j(["demographics", "income", "household_composition"]),
                   description="Often the same state DHS system, so data sharing is built-in.",
                   reliability="high"),
        Connection(source_id="ssa", target_id="mmis", direction="unidirectional",
                   frequency="batch", format="flat_file",
                   data_shared=_j(["ssi_eligibility", "disability_status"]),
                   description="SSA sends eligibility data to state Medicaid for automatic enrollment of SSI recipients. Monthly batch file.",
                   reliability="high"),

        # Justice internal
        Connection(source_id="cjis", target_id="courts", direction="bidirectional",
                   frequency="batch", format="custom",
                   data_shared=_j(["criminal_history", "dispositions", "warrants"]),
                   description="Courts report dispositions to CJIS. CJIS provides criminal history for sentencing.",
                   reliability="high"),
        Connection(source_id="doc", target_id="probation", direction="unidirectional",
                   frequency="batch", format="custom",
                   data_shared=_j(["release_dates", "conditions", "risk_assessments"]),
                   description="DOC notifies probation/parole of upcoming releases and supervision conditions.",
                   reliability="moderate"),

        # Child welfare
        Connection(source_id="sacwis", target_id="courts", direction="bidirectional",
                   frequency="manual", format="custom",
                   data_shared=_j(["case_status", "court_orders", "placement_changes"]),
                   description="Child welfare and courts exchange information about dependency cases, but often through manual filing rather than electronic exchange.",
                   reliability="low"),

        # Education
        Connection(source_id="state_doe", target_id="iep_system", direction="bidirectional",
                   frequency="batch", format="custom",
                   data_shared=_j(["enrollment", "special_education_status", "disability_category"]),
                   description="State DOE collects aggregate special education data from districts. Individual IEP details stay at the district level.",
                   reliability="moderate"),
    ]

    for c in connections:
        db.add(c)
    db.flush()
    return len(connections)


# ---------------------------------------------------------------------------
# GAPS (connections that should exist but don't)
# ---------------------------------------------------------------------------

def _seed_gaps(db: Session) -> int:
    gaps = [
        # === HEALTH <-> JUSTICE ===
        Gap(
            system_a_id="doc", system_b_id="mmis",
            barrier_type="legal",
            barrier_law="Medicaid Inmate Exclusion Policy",
            barrier_description="Federal law prohibits Medicaid payment for incarcerated individuals (except inpatient hospital stays in some states). This means Medicaid coverage is suspended/terminated upon incarceration, and corrections health records are completely disconnected from Medicaid claims history.",
            impact="When someone is released from prison, their treating providers have NO access to years of correctional health records. Medications are often discontinued. Chronic conditions go unmanaged. People die in the first two weeks after release at 12x the normal rate.",
            what_it_would_take="CMS 1115 waivers (several states now pursuing), requiring Medicaid enrollment pre-release. Technical: HL7/FHIR interface between DOC health system and state HIE. Funding: estimated $2-5M per state for technical integration.",
            consent_closable=True,
            consent_mechanism="Person can sign a HIPAA release authorizing DOC to share health records with community providers. However, this rarely happens systematically — it requires the person to know to ask, and DOC to have a process.",
            severity="critical",
            applies_when=_j(["incarcerated", "recently_released", "medicaid"]),
        ),
        Gap(
            system_a_id="doc", system_b_id="bh_authority",
            barrier_type="legal",
            barrier_law="42 CFR Part 2",
            barrier_description="Substance use treatment records in corrections are protected by 42 CFR Part 2, which requires patient consent for any disclosure. Even within the same corrections facility, SUD treatment staff may not share records with general medical staff without consent.",
            impact="A person receiving MAT (medication-assisted treatment) in prison may not have this information shared with their community behavioral health provider upon release. Treatment continuity is broken at the most dangerous moment.",
            what_it_would_take="Updated 42 CFR Part 2 regulations (SAMHSA has proposed changes). In the interim: standardized consent forms signed pre-release, electronic transmission protocols between DOC and BH authorities.",
            consent_closable=True,
            consent_mechanism="Person can sign a 42 CFR Part 2 compliant consent form specifically authorizing DOC SUD treatment providers to share records with named community providers. The consent must be specific about what information, to whom, and for what purpose.",
            severity="critical",
            applies_when=_j(["incarcerated", "recently_released", "sud", "mental_health"]),
        ),
        Gap(
            system_a_id="probation", system_b_id="bh_authority",
            barrier_type="legal",
            barrier_law="42 CFR Part 2",
            barrier_description="Probation officers cannot access substance use treatment records without specific patient consent under 42 CFR Part 2. This creates a paradox: courts order treatment as a condition of supervision, but the supervising officer cannot verify compliance without consent.",
            impact="Your probation officer doesn't know you're in treatment. They can't verify compliance with court-ordered treatment. If you miss a check-in because you were at a treatment appointment, they may file a violation. If treatment saves you, probation doesn't know — and can't advocate for you.",
            what_it_would_take="Standardized 'compliance-only' consent that allows treatment providers to confirm attendance without clinical details. Some drug courts have implemented this successfully. Requires consent form, policy, and simple electronic verification system.",
            consent_closable=True,
            consent_mechanism="Sign a limited-disclosure consent form authorizing treatment provider to share ONLY attendance/compliance data (not clinical details) with probation officer. Must specify the probation officer by name.",
            severity="high",
            applies_when=_j(["probation", "sud", "mental_health"]),
        ),
        Gap(
            system_a_id="probation", system_b_id="mmis",
            barrier_type="technical",
            barrier_law="",
            barrier_description="No technical interface exists between probation case management systems and Medicaid. Probation officers cannot verify whether supervisees have active Medicaid coverage, and Medicaid has no awareness of justice involvement that might affect care needs.",
            impact="Probation officers spend hours on the phone trying to help supervisees get Medicaid coverage reinstated after release. They can't verify if someone has coverage before referring them to treatment. Gaps in coverage mean gaps in treatment.",
            what_it_would_take="API integration between probation systems and state Medicaid eligibility lookup. Technically straightforward but requires interagency data-sharing agreement and funding. Estimated cost: $500K-$1M.",
            consent_closable=False,
            consent_mechanism="",
            severity="high",
            applies_when=_j(["probation", "recently_released", "medicaid"]),
        ),

        # === HEALTH <-> HOUSING ===
        Gap(
            system_a_id="hmis", system_b_id="mmis",
            barrier_type="technical",
            barrier_law="",
            barrier_description="HMIS (homeless services) and Medicaid operate on completely different technical platforms with no data exchange. A person's homelessness — a critical social determinant of health — is invisible to their Medicaid health plan.",
            impact="Your MCO care manager doesn't know you're homeless. They send appointment reminders to an address you don't live at. They prescribe medications that need refrigeration you don't have. They create care plans assuming stable housing that doesn't exist.",
            what_it_would_take="HMIS-to-HIE data bridge, using community information exchange (CIE) standards. Pilots exist (San Diego 211, Unite Us). Requires consent framework, technical bridge (~$1-3M), and cross-sector governance agreement.",
            consent_closable=True,
            consent_mechanism="Person can authorize HMIS provider to share housing status with Medicaid health plan. Requires awareness that this is possible and a mechanism at the provider level to transmit the data.",
            severity="critical",
            applies_when=_j(["homeless", "medicaid"]),
        ),
        Gap(
            system_a_id="hmis", system_b_id="bh_authority",
            barrier_type="political",
            barrier_law="",
            barrier_description="Despite serving the same individuals, homeless services and behavioral health authorities rarely share data systematically. Different agencies, different funding streams, different IT systems. Both document the same person's name, DOB, and needs — independently.",
            impact="You tell your story to the shelter intake worker. Then to the outreach worker. Then to the behavioral health assessor. Then to the housing navigator. Each one enters your data from scratch. No one has the full picture. Everyone has a fragment.",
            what_it_would_take="Interagency data governance agreement, common client identifier or matching algorithm, and consent framework. Community information exchange (CIE) platforms can bridge this. Estimated: $500K-$2M plus ongoing governance.",
            consent_closable=True,
            consent_mechanism="Person can sign a release authorizing homeless services provider and behavioral health provider to share information for care coordination purposes.",
            severity="high",
            applies_when=_j(["homeless", "mental_health", "sud"]),
        ),
        Gap(
            system_a_id="pha", system_b_id="mmis",
            barrier_type="technical",
            barrier_law="",
            barrier_description="Public housing authorities and Medicaid have no data exchange. Housing stability is a critical health determinant, and health conditions affect housing needs (accessibility, proximity to providers), but neither system sees the other.",
            impact="Your housing authority doesn't know you need a wheelchair-accessible unit because your disability data is in Medicaid, not housing. Your health plan doesn't know you're at risk of eviction because your housing data is at PHA.",
            what_it_would_take="HUD-HHS data matching initiative (has been piloted). Requires interagency agreement, common identifier, and consent framework. Technical: moderate complexity.",
            consent_closable=True,
            consent_mechanism="Person can authorize PHA and Medicaid MCO to share relevant information. Requires separate releases for each direction of data flow.",
            severity="moderate",
            applies_when=_j(["section_8", "public_housing", "medicaid"]),
        ),

        # === HEALTH <-> EDUCATION ===
        Gap(
            system_a_id="iep_system", system_b_id="bh_authority",
            barrier_type="legal",
            barrier_law="FERPA",
            barrier_description="FERPA prohibits schools from sharing student education records (including IEPs) with outside agencies without parental consent. Behavioral health providers treating a child often cannot access the child's IEP or school-based assessments.",
            impact="Your child's therapist doesn't know what accommodations are in the IEP. The school doesn't know what the therapist is working on. Goals conflict. Progress is duplicated or contradicted. The child is caught between two systems that don't talk.",
            what_it_would_take="Parental consent (FERPA allows disclosure with written consent). Schools and BH providers need a standardized consent form and a secure way to exchange IEP-relevant information. Technical: shared care plan platform.",
            consent_closable=True,
            consent_mechanism="Parent/guardian signs a FERPA release authorizing school to share IEP and relevant records with named behavioral health provider. Must be specific about which records and which provider.",
            severity="high",
            applies_when=_j(["under_18", "mental_health", "idd"]),
        ),
        Gap(
            system_a_id="iep_system", system_b_id="mmis",
            barrier_type="legal",
            barrier_law="FERPA",
            barrier_description="Medicaid can pay for health-related services in schools (speech therapy, counseling, OT/PT), but billing requires coordination between education and Medicaid systems that rarely exists. FERPA restricts what schools can share with Medicaid without consent.",
            impact="Schools provide Medicaid-billable services but can't bill because the data interface doesn't exist. Districts leave millions in federal Medicaid dollars on the table. Students who need services don't get them because schools can't prove medical necessity to Medicaid.",
            what_it_would_take="School-based Medicaid billing integration (some states have this). Requires parental consent for Medicaid billing, technical interface between school systems and MMIS, and trained billing staff. Investment: $1-5M per state.",
            consent_closable=True,
            consent_mechanism="Parent signs consent for school to bill Medicaid for covered services. This is separate from the IEP consent and often not explained to parents.",
            severity="moderate",
            applies_when=_j(["under_18", "medicaid", "idd", "mental_health"]),
        ),

        # === CHILD WELFARE <-> HEALTH ===
        Gap(
            system_a_id="sacwis", system_b_id="mmis",
            barrier_type="technical",
            barrier_law="",
            barrier_description="Child welfare and Medicaid serve many of the same children but rarely share data in real time. Foster children are categorically eligible for Medicaid, but placement changes create coverage gaps. Health histories don't transfer with the child.",
            impact="A foster child moves to a new placement. Their Medicaid coverage lapses for weeks during the transfer. Their health history — medications, allergies, diagnoses — stays in the old MCO's system. The new foster parent starts from zero. The child's prescriptions can't be filled.",
            what_it_would_take="Real-time interface between SACWIS/CCWIS and MMIS for placement changes. Health passport or portable health record for foster children. Federal CCWIS requirements are starting to address this but implementation is years away.",
            consent_closable=False,
            consent_mechanism="",
            severity="critical",
            applies_when=_j(["foster_care", "medicaid", "under_18"]),
        ),
        Gap(
            system_a_id="sacwis", system_b_id="bh_authority",
            barrier_type="political",
            barrier_law="",
            barrier_description="Child welfare agencies and behavioral health authorities serve overlapping populations (children with trauma, parents with SUD) but operate in different departments with different data systems. Case workers often don't know what behavioral health services a family is receiving.",
            impact="A child welfare caseworker doesn't know the parent is in treatment. They can't support recovery. They can't include treatment progress in court reports. The parent's effort is invisible to the system deciding whether to return their children.",
            what_it_would_take="Cross-system case management platform or data sharing agreement. Some states have implemented 'wraparound' coordination platforms. Requires interagency agreement, consent framework, and shared case planning tools.",
            consent_closable=True,
            consent_mechanism="Parent can sign releases allowing BH provider to share treatment status with child welfare. Courts can also order information sharing in dependency proceedings.",
            severity="critical",
            applies_when=_j(["foster_care", "mental_health", "sud"]),
        ),

        # === VETERANS ===
        Gap(
            system_a_id="va_system", system_b_id="hie",
            barrier_type="technical",
            barrier_law="",
            barrier_description="VA health records are in a federal system (VistA/Oracle Health) that is poorly connected to state and community health information exchanges. Veterans who receive care from both VA and community providers have fragmented records.",
            impact="Your VA psychiatrist doesn't see the ER visit at the community hospital. Your community PCP doesn't see the medications the VA prescribed. Drug interactions go undetected. Duplicate tests are ordered. Care is fragmented at every level.",
            what_it_would_take="VA Community Care network has improved this somewhat, but HIE integration remains incomplete. Requires FHIR-based interoperability (VA has committed to this), state HIE participation agreements, and identity matching across federal/state systems.",
            consent_closable=True,
            consent_mechanism="Veteran can authorize VA to share records with community providers through VA's release of information process (VA Form 10-5345). Can also authorize HIE participation.",
            severity="high",
            applies_when=_j(["veteran"]),
        ),
        Gap(
            system_a_id="va_system", system_b_id="mmis",
            barrier_type="technical",
            barrier_law="",
            barrier_description="Veterans eligible for both VA and Medicaid (dual-eligible) have records in two completely separate systems. Neither knows what the other is doing. This affects ~1.5M veterans nationally.",
            impact="Medicaid pays for services the VA already provides. The VA doesn't know about Medicaid-covered home health services. Dual-eligible veterans fall through both systems' care coordination because each assumes the other is handling it.",
            what_it_would_take="Federal-state data sharing agreement, common patient identifier matching, and care coordination platform for dual-eligibles. CMS and VA have MOU frameworks but implementation is state-by-state.",
            consent_closable=True,
            consent_mechanism="Veteran can sign releases for both VA and Medicaid MCO to share information. Requires two separate consent processes in two separate systems.",
            severity="moderate",
            applies_when=_j(["veteran", "medicaid"]),
        ),

        # === INCOME <-> HEALTH ===
        Gap(
            system_a_id="ssa", system_b_id="bh_authority",
            barrier_type="legal",
            barrier_law="Privacy Act / 42 CFR Part 2",
            barrier_description="SSA disability determination often requires behavioral health records, but 42 CFR Part 2 restricts sharing SUD treatment records, and the Privacy Act limits what SSA can share back. The result: people with SUD who need SSI/SSDI face extra barriers to proving disability.",
            impact="You're applying for SSI because your substance use disorder prevents you from working. SSA needs treatment records to evaluate your claim. Your SUD treatment provider can't share without your specific, written consent. You don't know this. Your claim is denied for insufficient evidence.",
            what_it_would_take="Streamlined consent process embedded in SSI/SSDI application. Training for benefits counselors on 42 CFR Part 2 consent requirements. Electronic submission pathway from BH providers to SSA.",
            consent_closable=True,
            consent_mechanism="Person must sign a specific 42 CFR Part 2 consent form naming SSA as the recipient, describing what records can be shared, and for what purpose (disability determination). This is separate from the general SSA authorization.",
            severity="high",
            applies_when=_j(["ssi", "ssdi", "sud", "mental_health"]),
        ),
    ]

    for g in gaps:
        db.add(g)
    db.flush()
    return len(gaps)
