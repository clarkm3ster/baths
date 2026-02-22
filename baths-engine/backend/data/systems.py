"""
Government Systems Mapping Engine — Real federal/state/local data systems.

Maps every major government data system that touches a person navigating
social services: what data it holds, who runs it, how it connects (or doesn't)
to other systems, and where the gaps are.

This is the DATAMAP — the foundation for understanding why coordination fails
and what it would take to build a dome.
"""

import logging
from .store import DataStore, get_store
from .scraper import BaseScraper

logger = logging.getLogger("baths.systems")

# ── Real Government Data Systems ────────────────────────────────────────

SEED_SYSTEMS = [
    # ═══════════════════════════════════════════════════════════════════
    # FEDERAL SYSTEMS
    # ═══════════════════════════════════════════════════════════════════
    {
        "system_code": "SSA_NUMIDENT",
        "name": "Social Security Numident (Master File)",
        "agency": "Social Security Administration",
        "level": "federal",
        "domain": "income",
        "data_fields": ["SSN", "name", "DOB", "citizenship_status", "death_indicator",
                        "gender", "race", "birthplace_state", "birthplace_country",
                        "mothers_maiden_name"],
        "population_served": "All US persons with SSN (~450 million records)",
        "annual_records": 450000000,
        "api_endpoint": "",
        "consent_required": "statutory",
    },
    {
        "system_code": "SSA_MBR",
        "name": "Master Beneficiary Record",
        "agency": "Social Security Administration",
        "level": "federal",
        "domain": "income",
        "data_fields": ["SSN", "benefit_type", "monthly_benefit_amount", "date_of_entitlement",
                        "payment_status", "representative_payee", "work_history",
                        "earnings_record", "disability_onset_date", "primary_insurance_amount"],
        "population_served": "~70 million beneficiaries (OASDI + SSI)",
        "annual_records": 70000000,
        "api_endpoint": "",
        "consent_required": "statutory",
    },
    {
        "system_code": "SSA_SSR",
        "name": "Supplemental Security Record",
        "agency": "Social Security Administration",
        "level": "federal",
        "domain": "income",
        "data_fields": ["SSN", "SSI_payment_amount", "resource_amount", "income_sources",
                        "living_arrangement", "in-kind_support", "representative_payee",
                        "state_supplement", "eligibility_status", "redetermination_date"],
        "population_served": "~7.4 million SSI recipients",
        "annual_records": 7400000,
        "api_endpoint": "",
        "consent_required": "statutory",
    },
    {
        "system_code": "CMS_MMIS",
        "name": "Medicaid Management Information System",
        "agency": "Centers for Medicare & Medicaid Services (state-operated)",
        "level": "federal",
        "domain": "health",
        "data_fields": ["medicaid_id", "eligibility_category", "enrollment_dates",
                        "claims_data", "provider_data", "drug_utilization",
                        "managed_care_plan", "cost_sharing", "TPL_data",
                        "MAGI_income", "household_composition"],
        "population_served": "~94 million Medicaid/CHIP enrollees (each state runs own MMIS)",
        "annual_records": 94000000,
        "api_endpoint": "",
        "consent_required": "agency",
    },
    {
        "system_code": "CMS_MEDICARE_EDB",
        "name": "Medicare Enrollment Database",
        "agency": "Centers for Medicare & Medicaid Services",
        "level": "federal",
        "domain": "health",
        "data_fields": ["HIC_number", "beneficiary_id", "enrollment_type", "Part_A_dates",
                        "Part_B_dates", "Part_C_plan", "Part_D_plan", "LIS_status",
                        "MSP_status", "ESRD_indicator", "disability_indicator",
                        "date_of_death", "dual_eligible_status"],
        "population_served": "~66.7 million Medicare beneficiaries",
        "annual_records": 66700000,
        "api_endpoint": "",
        "consent_required": "statutory",
    },
    {
        "system_code": "CMS_CCW",
        "name": "Chronic Conditions Data Warehouse",
        "agency": "Centers for Medicare & Medicaid Services",
        "level": "federal",
        "domain": "health",
        "data_fields": ["beneficiary_demographics", "chronic_conditions_flags",
                        "Part_A_claims", "Part_B_claims", "Part_D_events",
                        "SNF_claims", "HHA_claims", "hospice_claims",
                        "DME_claims", "assessment_data_MDS_OASIS"],
        "population_served": "Medicare + Medicaid beneficiaries for research",
        "annual_records": 66700000,
        "api_endpoint": "https://www2.ccwdata.org/",
        "consent_required": "agency",
    },
    {
        "system_code": "HUD_IMS_PIC",
        "name": "Inventory Management System / PIH Information Center",
        "agency": "Department of Housing and Urban Development",
        "level": "federal",
        "domain": "housing",
        "data_fields": ["PHA_code", "program_type", "tenant_id", "household_income",
                        "annual_income", "TTP", "HAP", "unit_address", "bedroom_size",
                        "race_ethnicity", "disability_status", "elderly_status",
                        "admission_date", "lease_date"],
        "population_served": "~4.7 million HUD-assisted households",
        "annual_records": 4700000,
        "api_endpoint": "",
        "consent_required": "agency",
    },
    {
        "system_code": "HUD_HMIS",
        "name": "Homeless Management Information System",
        "agency": "Department of Housing and Urban Development (locally operated)",
        "level": "federal",
        "domain": "housing",
        "data_fields": ["personal_id", "name", "SSN_partial", "DOB", "gender",
                        "race_ethnicity", "veteran_status", "disabling_condition",
                        "project_entry_date", "project_exit_date", "destination",
                        "income_sources", "non_cash_benefits", "health_insurance",
                        "domestic_violence", "chronic_homeless_status"],
        "population_served": "~1.6 million people served by CoC programs annually",
        "annual_records": 1600000,
        "api_endpoint": "",
        "consent_required": "individual",
    },
    {
        "system_code": "IRS_IMF",
        "name": "Individual Master File",
        "agency": "Internal Revenue Service",
        "level": "federal",
        "domain": "income",
        "data_fields": ["SSN", "filing_status", "AGI", "taxable_income", "tax_liability",
                        "EITC_amount", "CTC_amount", "withholding", "estimated_payments",
                        "W2_data", "1099_data", "refund_amount", "audit_flags"],
        "population_served": "~160 million individual tax returns filed annually",
        "annual_records": 160000000,
        "api_endpoint": "",
        "consent_required": "statutory",
    },
    {
        "system_code": "USDA_SNAP",
        "name": "SNAP Quality Control Data System",
        "agency": "USDA Food and Nutrition Service (state-operated)",
        "level": "federal",
        "domain": "food",
        "data_fields": ["case_id", "household_size", "gross_income", "net_income",
                        "benefit_amount", "certification_period", "expedited_service",
                        "categorical_eligibility", "employment_status", "ABAWD_status",
                        "deductions", "shelter_costs", "dependent_care"],
        "population_served": "~42 million SNAP participants in ~22 million households",
        "annual_records": 22000000,
        "api_endpoint": "",
        "consent_required": "agency",
    },
    {
        "system_code": "DOL_UI",
        "name": "Unemployment Insurance System",
        "agency": "Department of Labor (state-operated)",
        "level": "federal",
        "domain": "employment",
        "data_fields": ["SSN", "employer_EIN", "quarterly_wages", "claim_status",
                        "weekly_benefit_amount", "weeks_claimed", "separation_reason",
                        "work_search_activities", "reemployment_services",
                        "base_period_wages", "benefit_year"],
        "population_served": "~6 million UI claimants; ~160 million wage records/year",
        "annual_records": 160000000,
        "api_endpoint": "",
        "consent_required": "statutory",
    },
    {
        "system_code": "VA_VISTA",
        "name": "Veterans Health Information Systems and Technology Architecture",
        "agency": "Department of Veterans Affairs",
        "level": "federal",
        "domain": "health",
        "data_fields": ["patient_id", "SSN", "service_history", "disability_rating",
                        "clinical_records", "pharmacy", "radiology", "laboratory",
                        "mental_health", "prosthetics", "community_care",
                        "social_work_notes", "housing_status"],
        "population_served": "~9.1 million enrolled veterans",
        "annual_records": 9100000,
        "api_endpoint": "",
        "consent_required": "statutory",
    },
    {
        "system_code": "ED_NSLDS",
        "name": "National Student Loan Data System",
        "agency": "Department of Education",
        "level": "federal",
        "domain": "education",
        "data_fields": ["SSN", "loan_type", "loan_amount", "outstanding_balance",
                        "repayment_plan", "loan_status", "school_code", "enrollment_status",
                        "Pell_grant_history", "TEACH_grant", "default_status",
                        "income_driven_repayment"],
        "population_served": "~43 million federal student loan borrowers",
        "annual_records": 43000000,
        "api_endpoint": "",
        "consent_required": "statutory",
    },
    {
        "system_code": "DOJ_NCIC",
        "name": "National Crime Information Center",
        "agency": "Federal Bureau of Investigation",
        "level": "federal",
        "domain": "justice",
        "data_fields": ["name", "DOB", "SSN", "FBI_number", "state_ID", "fingerprints",
                        "wanted_persons", "missing_persons", "protection_orders",
                        "supervised_release", "sex_offender_registry",
                        "gang_affiliation", "known_terrorists"],
        "population_served": "~83 million criminal history records",
        "annual_records": 83000000,
        "api_endpoint": "",
        "consent_required": "statutory",
    },
    {
        "system_code": "ACF_TANF",
        "name": "TANF Data Reporting System",
        "agency": "Administration for Children and Families (state-operated)",
        "level": "federal",
        "domain": "income",
        "data_fields": ["case_id", "family_composition", "monthly_benefit",
                        "work_participation_hours", "activity_type", "sanction_status",
                        "months_of_receipt", "child_care_usage", "child_support_collected",
                        "diversion_payment", "earnings", "education_level"],
        "population_served": "~1 million TANF families (monthly average)",
        "annual_records": 1000000,
        "api_endpoint": "",
        "consent_required": "agency",
    },
    {
        "system_code": "ACF_CCDF",
        "name": "Child Care and Development Fund Data System",
        "agency": "Administration for Children and Families (state-operated)",
        "level": "federal",
        "domain": "education",
        "data_fields": ["child_id", "family_income", "provider_type", "provider_id",
                        "subsidy_amount", "copay_amount", "care_type",
                        "provider_quality_rating", "hours_of_care", "age_group"],
        "population_served": "~1.4 million children receiving subsidies monthly",
        "annual_records": 1400000,
        "api_endpoint": "",
        "consent_required": "agency",
    },

    # ═══════════════════════════════════════════════════════════════════
    # PENNSYLVANIA / PHILADELPHIA LOCAL SYSTEMS
    # ═══════════════════════════════════════════════════════════════════
    {
        "system_code": "PA_COMPASS",
        "name": "Commonwealth of PA Access to Social Services (COMPASS)",
        "agency": "PA Department of Human Services",
        "level": "state",
        "domain": "income",
        "data_fields": ["case_id", "applications", "eligibility_determinations",
                        "SNAP_status", "Medicaid_status", "TANF_status", "LIHEAP_status",
                        "CHIP_status", "household_composition", "income_verification"],
        "population_served": "PA residents applying for public benefits",
        "annual_records": 3500000,
        "api_endpoint": "https://www.compass.state.pa.us/compass.web/Public/CMPHome",
        "consent_required": "individual",
    },
    {
        "system_code": "PHL_CARES",
        "name": "Philadelphia CARES (Coordinated Entry)",
        "agency": "City of Philadelphia Office of Homeless Services",
        "level": "local",
        "domain": "housing",
        "data_fields": ["client_id", "vulnerability_index", "housing_barriers",
                        "shelter_history", "chronic_status", "veteran_status",
                        "disability", "domestic_violence", "prioritization_score",
                        "referral_status", "housing_placement"],
        "population_served": "People experiencing homelessness in Philadelphia",
        "annual_records": 15000,
        "api_endpoint": "",
        "consent_required": "individual",
    },
    {
        "system_code": "PHL_BRT",
        "name": "Board of Revision of Taxes — Property Assessment",
        "agency": "City of Philadelphia",
        "level": "local",
        "domain": "housing",
        "data_fields": ["parcel_id", "address", "owner_name", "zoning_code",
                        "land_area", "improvement_area", "market_value",
                        "assessment_date", "tax_status", "exemptions",
                        "vacant_indicator", "land_use_code"],
        "population_served": "~580,000 Philadelphia parcels",
        "annual_records": 580000,
        "api_endpoint": "https://phl.carto.com/api/v2/sql",
        "consent_required": "none",
    },
]

# ── System Links (real connections and gaps) ──────────────────────────

SEED_LINKS = [
    # Active cross-system connections
    {
        "source_system": "SSA_NUMIDENT", "target_system": "IRS_IMF",
        "link_type": "active", "mechanism": "batch",
        "latency": "daily", "consent_barrier": "none",
        "legal_authority": "IRC § 6103(l)(1) — SSA access to tax data",
    },
    {
        "source_system": "SSA_MBR", "target_system": "CMS_MEDICARE_EDB",
        "link_type": "active", "mechanism": "batch",
        "latency": "daily", "consent_barrier": "none",
        "legal_authority": "SSA § 1818/1836 — Medicare enrollment via SSA",
    },
    {
        "source_system": "DOL_UI", "target_system": "SSA_NUMIDENT",
        "link_type": "active", "mechanism": "batch",
        "latency": "quarterly", "consent_barrier": "none",
        "legal_authority": "SSA § 1137 — wage/UI cross-match for benefit verification",
    },
    {
        "source_system": "USDA_SNAP", "target_system": "SSA_SSR",
        "link_type": "active", "mechanism": "batch",
        "latency": "monthly", "consent_barrier": "none",
        "legal_authority": "Food & Nutrition Act § 11(e)(19) — SSI categorical eligibility",
    },
    {
        "source_system": "IRS_IMF", "target_system": "CMS_MMIS",
        "link_type": "active", "mechanism": "batch",
        "latency": "daily", "consent_barrier": "none",
        "legal_authority": "ACA § 1413 — IRS income data for Medicaid MAGI determination",
    },
    {
        "source_system": "VA_VISTA", "target_system": "CMS_MEDICARE_EDB",
        "link_type": "active", "mechanism": "API",
        "latency": "realtime", "consent_barrier": "none",
        "legal_authority": "MISSION Act — VA community care coordination with Medicare",
    },
    {
        "source_system": "DOJ_NCIC", "target_system": "HUD_IMS_PIC",
        "link_type": "one-way", "mechanism": "manual",
        "latency": "monthly", "consent_barrier": "individual",
        "legal_authority": "PIH Notice 2015-19 — PHA access to criminal records for screening",
    },

    # Possible but not implemented connections
    {
        "source_system": "CMS_MMIS", "target_system": "HUD_HMIS",
        "link_type": "possible", "mechanism": "API",
        "latency": "none", "consent_barrier": "individual",
        "legal_authority": "42 CFR § 431.300 limits; no statutory authority for routine sharing",
    },
    {
        "source_system": "CMS_MMIS", "target_system": "USDA_SNAP",
        "link_type": "possible", "mechanism": "batch",
        "latency": "none", "consent_barrier": "agency",
        "legal_authority": "Express lane eligibility (42 U.S.C. § 1396a(e)(13)) — CHIP/Medicaid can use SNAP data",
    },
    {
        "source_system": "HUD_HMIS", "target_system": "VA_VISTA",
        "link_type": "possible", "mechanism": "API",
        "latency": "none", "consent_barrier": "individual",
        "legal_authority": "SSVF program allows data sharing with consent; no universal authority",
    },
    {
        "source_system": "ED_NSLDS", "target_system": "SSA_SSR",
        "link_type": "possible", "mechanism": "batch",
        "latency": "none", "consent_barrier": "statutory",
        "legal_authority": "FERPA restricts; would require statutory change or individual consent",
    },

    # Blocked connections (legal/structural barriers)
    {
        "source_system": "CMS_MMIS", "target_system": "DOJ_NCIC",
        "link_type": "blocked", "mechanism": "none",
        "latency": "none", "consent_barrier": "statutory",
        "legal_authority": "42 CFR Part 2 (SUD records); HIPAA minimum necessary; 28 CFR Part 20",
    },
    {
        "source_system": "IRS_IMF", "target_system": "HUD_IMS_PIC",
        "link_type": "blocked", "mechanism": "none",
        "latency": "none", "consent_barrier": "statutory",
        "legal_authority": "IRC § 6103 — strict limits on IRS data disclosure; HUD not listed",
    },
    {
        "source_system": "ED_NSLDS", "target_system": "CMS_MMIS",
        "link_type": "blocked", "mechanism": "none",
        "latency": "none", "consent_barrier": "statutory",
        "legal_authority": "FERPA § 99.31 — no exception for health/social services routine sharing",
    },
    {
        "source_system": "ACF_TANF", "target_system": "DOJ_NCIC",
        "link_type": "blocked", "mechanism": "none",
        "latency": "none", "consent_barrier": "statutory",
        "legal_authority": "TANF confidentiality rules (45 CFR § 265.6); no authorization for justice sharing",
    },

    # Philadelphia local links
    {
        "source_system": "PHL_CARES", "target_system": "HUD_HMIS",
        "link_type": "active", "mechanism": "API",
        "latency": "realtime", "consent_barrier": "individual",
        "legal_authority": "HUD CoC requirements; HMIS Data Standards",
    },
    {
        "source_system": "PHL_BRT", "target_system": "HUD_IMS_PIC",
        "link_type": "possible", "mechanism": "batch",
        "latency": "none", "consent_barrier": "none",
        "legal_authority": "Property data is public; no legal barrier, just no integration built",
    },
    {
        "source_system": "PA_COMPASS", "target_system": "CMS_MMIS",
        "link_type": "active", "mechanism": "batch",
        "latency": "daily", "consent_barrier": "none",
        "legal_authority": "PA DHS integrated eligibility — COMPASS feeds PA MMIS",
    },
    {
        "source_system": "PA_COMPASS", "target_system": "USDA_SNAP",
        "link_type": "active", "mechanism": "batch",
        "latency": "daily", "consent_barrier": "none",
        "legal_authority": "PA DHS administers SNAP through COMPASS; same agency",
    },
]


def seed_systems(store: DataStore | None = None):
    """Load all seed systems and links into the store."""
    store = store or get_store()
    sys_count = 0
    for s in SEED_SYSTEMS:
        store.upsert_system(**s)
        sys_count += 1

    link_count = 0
    for l in SEED_LINKS:
        store.upsert_system_link(**l)
        link_count += 1

    logger.info(f"Seeded {sys_count} systems and {link_count} links")
    return {"systems": sys_count, "links": link_count}


class SystemsScraper(BaseScraper):
    """Enriches system data with spending info from USASpending API."""

    engine_name = "systems"
    source_name = "usaspending"

    # Map agency names to USASpending toptier codes
    AGENCY_CODES = {
        "Social Security Administration": "028",
        "Centers for Medicare & Medicaid Services": "075",
        "Department of Housing and Urban Development": "086",
        "USDA Food and Nutrition Service": "012",
        "Department of Labor": "016",
        "Department of Education": "091",
        "Department of Veterans Affairs": "036",
        "Federal Bureau of Investigation": "015",
        "Administration for Children and Families": "075",
    }

    async def scrape(self) -> dict:
        added = 0
        updated = 0

        for agency_name, code in self.AGENCY_CODES.items():
            data = await self._fetch(
                f"https://api.usaspending.gov/api/v2/agency/{code}/sub_agency/",
                params={"fiscal_year": 2024, "limit": 10},
            )
            if data and "results" in data:
                for sub in data["results"]:
                    sub_name = sub.get("name", "")
                    obligations = sub.get("total_obligations", 0)
                    if sub_name and obligations:
                        # Create enrichment linking spending to system
                        self.store.add_enrichment(
                            enrichment_type="spending_data",
                            source_table="gov_systems",
                            source_id=0,
                            target_table=None,
                            target_id=None,
                            description=f"{sub_name}: ${obligations:,.0f} in obligations FY2024",
                            confidence=0.9,
                            data={
                                "agency": agency_name,
                                "sub_agency": sub_name,
                                "obligations": obligations,
                                "fiscal_year": 2024,
                            },
                        )
                        added += 1

        return {"added": added, "updated": updated}
