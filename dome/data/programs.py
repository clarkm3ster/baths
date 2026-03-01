"""
Government Program Reference Data
====================================

Comprehensive definitions for 63 federal, state, and local government
programs tracked by THE DOME fiscal-cascade engine.

Each program entry captures:

- **name** / **code**: Human-readable name and short machine identifier.
- **agency**: Administering federal agency (or "Various" for state/local).
- **level**: ``federal``, ``state``, ``local``, or ``federal_state`` (jointly
  funded programs such as Medicaid).
- **annual_spend_total**: Approximate annual spending in billions of current
  (2024) USD.
- **eligibility_rules**: Income thresholds (as % FPL), age ranges, and
  categorical requirements.
- **benefit_type**: One of ``cash``, ``in_kind``, ``service``,
  ``tax_expenditure``, or ``institutional``.
- **domain**: Policy domain (healthcare, income_support, housing, food,
  education, justice, child_family, workforce, energy, other).
- **cascade_types**: List of cascade IDs (from :mod:`dome.data.cascades`)
  whose progression drives utilization of this program.

Usage::

    from dome.data.programs import PROGRAMS
    medicaid = next(p for p in PROGRAMS if p["code"] == "medicaid")
    print(medicaid["annual_spend_total"])  # 805.0

Sources:
    - CBO Budget and Economic Outlook (FY 2024)
    - CMS National Health Expenditure Accounts
    - OMB Budget of the United States Government, Appendix
    - USDA Food and Nutrition Service annual reports
    - HUD budget justifications
    - SSA Annual Statistical Supplement
    - DOJ Bureau of Justice Statistics
    - DOEd Budget Service tables
"""

from __future__ import annotations

from typing import Any, Dict, List


# ---------------------------------------------------------------------------
# Helper constants for common eligibility thresholds
# ---------------------------------------------------------------------------
_FPL_100 = {"income_pct_fpl_max": 100}
_FPL_125 = {"income_pct_fpl_max": 125}
_FPL_138 = {"income_pct_fpl_max": 138}
_FPL_150 = {"income_pct_fpl_max": 150}
_FPL_185 = {"income_pct_fpl_max": 185}
_FPL_200 = {"income_pct_fpl_max": 200}
_FPL_250 = {"income_pct_fpl_max": 250}
_FPL_300 = {"income_pct_fpl_max": 300}
_FPL_400 = {"income_pct_fpl_max": 400}
_NO_INCOME_TEST = {"income_pct_fpl_max": None}
_AGE_65_PLUS = {"age_min": 65}
_AGE_UNDER_5 = {"age_max": 5}
_AGE_UNDER_18 = {"age_max": 18}
_AGE_UNDER_19 = {"age_max": 19}
_AGE_UNDER_6 = {"age_max": 6}

PROGRAMS: List[Dict[str, Any]] = [
    # =====================================================================
    #  HEALTHCARE  (1-10)
    # =====================================================================
    {  # 1
        "name": "Medicare",
        "code": "medicare",
        "agency": "CMS",
        "level": "federal",
        "annual_spend_total": 944.0,
        "eligibility_rules": {
            **_NO_INCOME_TEST,
            **_AGE_65_PLUS,
            "categorical": ["age_65_plus", "ssdi_after_24mo", "esrd", "als"],
        },
        "benefit_type": "in_kind",
        "domain": "healthcare",
        "cascade_types": [
            "econ_psych_bio_fiscal",
            "env_bio_econ_fiscal",
            "social_psych_bio_fiscal",
        ],
        "enrollees_millions": 67.0,
        "notes": "Parts A/B/C/D combined; includes MA plan payments.",
    },
    {  # 2
        "name": "Medicaid",
        "code": "medicaid",
        "agency": "CMS",
        "level": "federal_state",
        "annual_spend_total": 805.0,
        "eligibility_rules": {
            **_FPL_138,
            "categorical": [
                "low_income_adults",
                "children",
                "pregnant_women",
                "aged",
                "disabled",
            ],
            "notes": "Expansion states cover adults to 138% FPL; non-expansion states vary.",
        },
        "benefit_type": "in_kind",
        "domain": "healthcare",
        "cascade_types": [
            "econ_psych_bio_fiscal",
            "social_psych_bio_fiscal",
            "legal_econ_social_geo_bio_fiscal",
            "env_bio_econ_fiscal",
        ],
        "enrollees_millions": 93.0,
        "notes": "Federal share (FMAP) averages ~63%; total includes state share.",
    },
    {  # 3
        "name": "Children's Health Insurance Program (CHIP)",
        "code": "chip",
        "agency": "CMS",
        "level": "federal_state",
        "annual_spend_total": 19.5,
        "eligibility_rules": {
            **_FPL_250,
            **_AGE_UNDER_19,
            "categorical": ["children_above_medicaid_but_below_chip_threshold"],
        },
        "benefit_type": "in_kind",
        "domain": "healthcare",
        "cascade_types": ["env_cog_edu_econ_fiscal"],
        "enrollees_millions": 7.0,
        "notes": "Upper income limit varies by state (200-300% FPL typical).",
    },
    {  # 4
        "name": "ACA Health Insurance Marketplace",
        "code": "aca_marketplace",
        "agency": "CMS",
        "level": "federal",
        "annual_spend_total": 80.0,
        "eligibility_rules": {
            **_FPL_400,
            "categorical": ["not_eligible_for_employer_coverage", "not_medicaid_eligible"],
            "notes": "Premium tax credits currently uncapped (IRA extension).",
        },
        "benefit_type": "tax_expenditure",
        "domain": "healthcare",
        "cascade_types": ["econ_psych_bio_fiscal"],
        "enrollees_millions": 21.3,
        "notes": "Includes premium tax credits and cost-sharing reductions.",
    },
    {  # 5
        "name": "Veterans Health Administration (VA Health)",
        "code": "va_health",
        "agency": "VA",
        "level": "federal",
        "annual_spend_total": 113.0,
        "eligibility_rules": {
            **_NO_INCOME_TEST,
            "categorical": ["veterans", "service_connected_disability"],
            "notes": "Priority groups 1-8; income test for some groups.",
        },
        "benefit_type": "in_kind",
        "domain": "healthcare",
        "cascade_types": [
            "econ_psych_bio_fiscal",
            "social_psych_bio_fiscal",
        ],
        "enrollees_millions": 9.1,
        "notes": "VHA is the largest integrated healthcare system in the US.",
    },
    {  # 6
        "name": "TRICARE",
        "code": "tricare",
        "agency": "DoD",
        "level": "federal",
        "annual_spend_total": 55.0,
        "eligibility_rules": {
            **_NO_INCOME_TEST,
            "categorical": [
                "active_duty",
                "active_duty_family",
                "retiree",
                "retiree_family",
                "guard_reserve",
            ],
        },
        "benefit_type": "in_kind",
        "domain": "healthcare",
        "cascade_types": ["econ_psych_bio_fiscal"],
        "enrollees_millions": 9.6,
        "notes": "Defense Health Program; includes TRICARE Prime, Select, For Life.",
    },
    {  # 7
        "name": "Ryan White HIV/AIDS Program",
        "code": "ryan_white",
        "agency": "HRSA",
        "level": "federal",
        "annual_spend_total": 2.6,
        "eligibility_rules": {
            **_FPL_300,
            "categorical": ["hiv_positive", "low_income"],
        },
        "benefit_type": "service",
        "domain": "healthcare",
        "cascade_types": [
            "social_psych_bio_fiscal",
            "econ_psych_bio_fiscal",
        ],
        "enrollees_millions": 0.56,
        "notes": "Parts A-D plus ADAP (AIDS Drug Assistance Program).",
    },
    {  # 8
        "name": "Federally Qualified Health Centers (FQHC)",
        "code": "fqhc",
        "agency": "HRSA",
        "level": "federal",
        "annual_spend_total": 6.4,
        "eligibility_rules": {
            "income_pct_fpl_max": None,
            "categorical": ["open_to_all", "sliding_fee_scale"],
            "notes": "Serve anyone regardless of ability to pay.",
        },
        "benefit_type": "service",
        "domain": "healthcare",
        "cascade_types": [
            "econ_psych_bio_fiscal",
            "env_bio_econ_fiscal",
        ],
        "enrollees_millions": 30.0,
        "notes": "1,400+ grantees operating 15,000+ sites; Section 330 grants.",
    },
    {  # 9
        "name": "Indian Health Service (IHS)",
        "code": "ihs",
        "agency": "IHS",
        "level": "federal",
        "annual_spend_total": 7.0,
        "eligibility_rules": {
            **_NO_INCOME_TEST,
            "categorical": ["american_indian", "alaska_native", "tribal_member"],
        },
        "benefit_type": "service",
        "domain": "healthcare",
        "cascade_types": [
            "econ_psych_bio_fiscal",
            "env_bio_econ_fiscal",
            "social_psych_bio_fiscal",
        ],
        "enrollees_millions": 2.6,
        "notes": "Direct care and tribal/urban programs for AI/AN populations.",
    },
    {  # 10
        "name": "CHIP Dental Coverage",
        "code": "chip_dental",
        "agency": "CMS",
        "level": "federal_state",
        "annual_spend_total": 2.0,
        "eligibility_rules": {
            **_FPL_250,
            **_AGE_UNDER_19,
            "categorical": ["chip_enrolled_children"],
        },
        "benefit_type": "in_kind",
        "domain": "healthcare",
        "cascade_types": ["env_cog_edu_econ_fiscal"],
        "enrollees_millions": 5.0,
        "notes": "Dental is a required CHIP benefit; subset of CHIP spending.",
    },

    # =====================================================================
    #  INCOME SUPPORT  (11-17)
    # =====================================================================
    {  # 11
        "name": "Social Security Retirement (OASI)",
        "code": "ss_retirement",
        "agency": "SSA",
        "level": "federal",
        "annual_spend_total": 1_200.0,
        "eligibility_rules": {
            **_NO_INCOME_TEST,
            "age_min": 62,
            "categorical": ["40_quarters_covered_employment"],
        },
        "benefit_type": "cash",
        "domain": "income_support",
        "cascade_types": ["econ_psych_bio_fiscal"],
        "enrollees_millions": 52.0,
        "notes": "Old-Age and Survivors Insurance; includes spousal/survivor benefits.",
    },
    {  # 12
        "name": "Social Security Disability Insurance (SSDI)",
        "code": "ssdi",
        "agency": "SSA",
        "level": "federal",
        "annual_spend_total": 150.0,
        "eligibility_rules": {
            **_NO_INCOME_TEST,
            "categorical": ["disabled", "sufficient_work_credits"],
            "notes": "SGA limit ~$1,550/mo (non-blind) 2024.",
        },
        "benefit_type": "cash",
        "domain": "income_support",
        "cascade_types": [
            "econ_psych_bio_fiscal",
            "env_bio_econ_fiscal",
        ],
        "enrollees_millions": 7.6,
        "notes": "Average benefit ~$1,537/mo; 24-month waiting period for Medicare.",
    },
    {  # 13
        "name": "Supplemental Security Income (SSI)",
        "code": "ssi",
        "agency": "SSA",
        "level": "federal",
        "annual_spend_total": 61.0,
        "eligibility_rules": {
            "income_pct_fpl_max": 74,
            "categorical": ["aged", "blind", "disabled", "limited_resources"],
            "resource_limit": 2_000,
            "notes": "Federal benefit rate $943/mo (2024); states may supplement.",
        },
        "benefit_type": "cash",
        "domain": "income_support",
        "cascade_types": [
            "econ_psych_bio_fiscal",
            "social_psych_bio_fiscal",
        ],
        "enrollees_millions": 7.5,
        "notes": "Means-tested; automatic Medicaid eligibility in most states.",
    },
    {  # 14
        "name": "Temporary Assistance for Needy Families (TANF)",
        "code": "tanf",
        "agency": "ACF",
        "level": "federal_state",
        "annual_spend_total": 16.5,
        "eligibility_rules": {
            **_FPL_100,
            "categorical": ["families_with_children", "work_requirements"],
            "notes": "60-month federal lifetime limit; states may set shorter.",
        },
        "benefit_type": "cash",
        "domain": "income_support",
        "cascade_types": [
            "econ_psych_bio_fiscal",
            "econ_social_legal_fiscal",
        ],
        "enrollees_millions": 1.8,
        "notes": "Block grant; significant state flexibility; declining caseloads.",
    },
    {  # 15
        "name": "Unemployment Insurance (UI)",
        "code": "unemployment_insurance",
        "agency": "DOL",
        "level": "federal_state",
        "annual_spend_total": 29.0,
        "eligibility_rules": {
            **_NO_INCOME_TEST,
            "categorical": ["recently_employed", "involuntary_separation", "able_to_work"],
            "notes": "Typically 26 weeks; extended during recessions.",
        },
        "benefit_type": "cash",
        "domain": "income_support",
        "cascade_types": ["econ_psych_bio_fiscal"],
        "enrollees_millions": 5.8,
        "notes": "Federal-state system; benefit amount and duration vary by state.",
    },
    {  # 16
        "name": "Social Services Block Grant (SSBG)",
        "code": "ssbg",
        "agency": "ACF",
        "level": "federal_state",
        "annual_spend_total": 1.7,
        "eligibility_rules": {
            **_NO_INCOME_TEST,
            "categorical": ["state_defined_populations"],
            "notes": "States have broad discretion in targeting.",
        },
        "benefit_type": "service",
        "domain": "income_support",
        "cascade_types": [
            "econ_psych_bio_fiscal",
            "social_psych_bio_fiscal",
        ],
        "enrollees_millions": 23.0,
        "notes": "Title XX; funds social services including child care, elder services.",
    },
    {  # 17
        "name": "Community Services Block Grant (CSBG)",
        "code": "csbg",
        "agency": "ACF",
        "level": "federal_state",
        "annual_spend_total": 0.8,
        "eligibility_rules": {
            **_FPL_200,
            "categorical": ["low_income_individuals_and_families"],
        },
        "benefit_type": "service",
        "domain": "income_support",
        "cascade_types": [
            "econ_psych_bio_fiscal",
            "econ_social_legal_fiscal",
        ],
        "enrollees_millions": 15.0,
        "notes": "Funds 1,000+ Community Action Agencies nationwide.",
    },

    # =====================================================================
    #  TAX EXPENDITURES  (18-22)
    # =====================================================================
    {  # 18
        "name": "Earned Income Tax Credit (EITC)",
        "code": "eitc",
        "agency": "IRS",
        "level": "federal",
        "annual_spend_total": 64.0,
        "eligibility_rules": {
            "income_max": 63_398,
            "categorical": ["earned_income", "working_families_or_individuals"],
            "notes": "Max credit ~$7,430 with 3+ children (2024).",
        },
        "benefit_type": "tax_expenditure",
        "domain": "income_support",
        "cascade_types": [
            "econ_psych_bio_fiscal",
            "econ_social_legal_fiscal",
        ],
        "enrollees_millions": 31.0,
        "notes": "Refundable credit; largest anti-poverty program for working families.",
    },
    {  # 19
        "name": "Child Tax Credit (CTC)",
        "code": "child_tax_credit",
        "agency": "IRS",
        "level": "federal",
        "annual_spend_total": 122.0,
        "eligibility_rules": {
            "income_max": 200_000,
            "categorical": ["dependent_children_under_17"],
            "notes": "$2,000 per child; refundable portion up to $1,700 (2024).",
        },
        "benefit_type": "tax_expenditure",
        "domain": "child_family",
        "cascade_types": [
            "econ_psych_bio_fiscal",
            "env_cog_edu_econ_fiscal",
        ],
        "enrollees_millions": 48.0,
        "notes": "Phases out above $200K single / $400K married.",
    },
    {  # 20
        "name": "Child and Dependent Care Tax Credit (CDCTC)",
        "code": "cdctc",
        "agency": "IRS",
        "level": "federal",
        "annual_spend_total": 5.0,
        "eligibility_rules": {
            **_NO_INCOME_TEST,
            "categorical": ["working_parent_with_care_expenses"],
            "notes": "Max $3,000 expenses for 1 dependent, $6,000 for 2+.",
        },
        "benefit_type": "tax_expenditure",
        "domain": "child_family",
        "cascade_types": ["econ_psych_bio_fiscal"],
        "enrollees_millions": 6.0,
        "notes": "Non-refundable; credit rate phases down from 35% to 20%.",
    },
    {  # 21
        "name": "Mortgage Interest Deduction",
        "code": "mortgage_interest_deduction",
        "agency": "IRS",
        "level": "federal",
        "annual_spend_total": 25.0,
        "eligibility_rules": {
            **_NO_INCOME_TEST,
            "categorical": ["homeowner_with_mortgage", "itemizing_taxpayer"],
            "notes": "Limited to interest on first $750K of mortgage debt (TCJA).",
        },
        "benefit_type": "tax_expenditure",
        "domain": "housing",
        "cascade_types": [],
        "enrollees_millions": 15.0,
        "notes": "Primarily benefits higher-income homeowners who itemize.",
    },
    {  # 22
        "name": "Premium Tax Credits (ACA)",
        "code": "premium_tax_credits",
        "agency": "IRS",
        "level": "federal",
        "annual_spend_total": 72.0,
        "eligibility_rules": {
            **_FPL_400,
            "categorical": ["marketplace_enrollee", "not_employer_eligible"],
            "notes": "Enhanced credits through 2025 under IRA; cap at 8.5% income.",
        },
        "benefit_type": "tax_expenditure",
        "domain": "healthcare",
        "cascade_types": ["econ_psych_bio_fiscal"],
        "enrollees_millions": 19.0,
        "notes": "Advance payments made directly to insurers.",
    },

    # =====================================================================
    #  FOOD / NUTRITION  (23-25)
    # =====================================================================
    {  # 23
        "name": "Supplemental Nutrition Assistance Program (SNAP)",
        "code": "snap",
        "agency": "USDA-FNS",
        "level": "federal",
        "annual_spend_total": 113.0,
        "eligibility_rules": {
            "income_pct_fpl_max": 130,
            "categorical": ["low_income_households"],
            "notes": "Gross income <=130% FPL; net income <=100% FPL; asset test waived in most states.",
        },
        "benefit_type": "in_kind",
        "domain": "food",
        "cascade_types": [
            "econ_psych_bio_fiscal",
            "econ_social_legal_fiscal",
        ],
        "enrollees_millions": 42.0,
        "notes": "Formerly Food Stamps; EBT card for food purchases.",
    },
    {  # 24
        "name": "Special Supplemental Nutrition Program for Women, Infants, and Children (WIC)",
        "code": "wic",
        "agency": "USDA-FNS",
        "level": "federal",
        "annual_spend_total": 5.5,
        "eligibility_rules": {
            **_FPL_185,
            "categorical": [
                "pregnant_women",
                "postpartum_women",
                "infants",
                "children_under_5",
            ],
            "notes": "Nutritional risk assessment required.",
        },
        "benefit_type": "in_kind",
        "domain": "food",
        "cascade_types": [
            "env_cog_edu_econ_fiscal",
            "env_bio_econ_fiscal",
        ],
        "enrollees_millions": 6.3,
        "notes": "Supplemental foods, nutrition education, healthcare referrals.",
    },
    {  # 25
        "name": "National School Lunch & Breakfast Programs",
        "code": "school_meals",
        "agency": "USDA-FNS",
        "level": "federal",
        "annual_spend_total": 22.0,
        "eligibility_rules": {
            **_FPL_185,
            **_AGE_UNDER_18,
            "categorical": ["enrolled_students"],
            "notes": "Free meals <=130% FPL; reduced price 130-185% FPL.",
        },
        "benefit_type": "in_kind",
        "domain": "food",
        "cascade_types": ["env_cog_edu_econ_fiscal"],
        "enrollees_millions": 30.0,
        "notes": "Combined NSLP and SBP; Community Eligibility Provision expands access.",
    },

    # =====================================================================
    #  HOUSING  (26-33)
    # =====================================================================
    {  # 26
        "name": "Section 8 Housing Choice Vouchers (HCV)",
        "code": "section_8_hcv",
        "agency": "HUD",
        "level": "federal",
        "annual_spend_total": 30.0,
        "eligibility_rules": {
            "income_pct_ami_max": 50,
            "categorical": ["very_low_income_families", "elderly", "disabled"],
            "notes": "75% of new vouchers must go to <=30% AMI households.",
        },
        "benefit_type": "in_kind",
        "domain": "housing",
        "cascade_types": [
            "legal_econ_social_geo_bio_fiscal",
            "social_psych_bio_fiscal",
        ],
        "enrollees_millions": 2.3,
        "notes": "Tenant-based rental assistance; long waitlists in most PHAs.",
    },
    {  # 27
        "name": "Public Housing",
        "code": "public_housing",
        "agency": "HUD",
        "level": "federal",
        "annual_spend_total": 8.5,
        "eligibility_rules": {
            "income_pct_ami_max": 80,
            "categorical": ["low_income_families", "elderly", "disabled"],
            "notes": "Rent set at 30% of adjusted income.",
        },
        "benefit_type": "in_kind",
        "domain": "housing",
        "cascade_types": [
            "legal_econ_social_geo_bio_fiscal",
            "env_bio_econ_fiscal",
        ],
        "enrollees_millions": 0.9,
        "notes": "~950,000 units managed by ~3,100 Public Housing Authorities.",
    },
    {  # 28
        "name": "HOME Investment Partnerships Program",
        "code": "home",
        "agency": "HUD",
        "level": "federal_state",
        "annual_spend_total": 1.5,
        "eligibility_rules": {
            "income_pct_ami_max": 80,
            "categorical": ["low_income_households"],
            "notes": "At least 15% for CHDOs; income targeting varies by activity.",
        },
        "benefit_type": "in_kind",
        "domain": "housing",
        "cascade_types": ["legal_econ_social_geo_bio_fiscal"],
        "enrollees_millions": 0.3,
        "notes": "Formula grant to states/localities for affordable housing activities.",
    },
    {  # 29
        "name": "Low-Income Housing Tax Credit (LIHTC)",
        "code": "lihtc",
        "agency": "IRS",
        "level": "federal",
        "annual_spend_total": 13.0,
        "eligibility_rules": {
            "income_pct_ami_max": 60,
            "categorical": ["low_income_renters"],
            "notes": "Projects must maintain income restrictions for 15-30 years.",
        },
        "benefit_type": "tax_expenditure",
        "domain": "housing",
        "cascade_types": ["legal_econ_social_geo_bio_fiscal"],
        "enrollees_millions": 3.5,
        "notes": "Largest source of affordable housing production; ~110,000 units/year.",
    },
    {  # 30
        "name": "Section 811 Supportive Housing for Persons with Disabilities",
        "code": "section_811",
        "agency": "HUD",
        "level": "federal",
        "annual_spend_total": 0.3,
        "eligibility_rules": {
            "income_pct_ami_max": 50,
            "categorical": ["disabled_adults_18_61"],
            "notes": "Extremely low-income priority.",
        },
        "benefit_type": "in_kind",
        "domain": "housing",
        "cascade_types": [
            "social_psych_bio_fiscal",
            "legal_econ_social_geo_bio_fiscal",
        ],
        "enrollees_millions": 0.035,
        "notes": "Capital advances and project rental assistance for disabled tenants.",
    },
    {  # 31
        "name": "Section 202 Supportive Housing for the Elderly",
        "code": "section_202",
        "agency": "HUD",
        "level": "federal",
        "annual_spend_total": 0.8,
        "eligibility_rules": {
            "income_pct_ami_max": 50,
            **_AGE_65_PLUS,
            "categorical": ["very_low_income_elderly"],
        },
        "benefit_type": "in_kind",
        "domain": "housing",
        "cascade_types": ["social_psych_bio_fiscal"],
        "enrollees_millions": 0.13,
        "notes": "Capital advances and PRAC; ~6,800 properties nationwide.",
    },
    {  # 32
        "name": "McKinney-Vento Homeless Assistance",
        "code": "mckinney_vento",
        "agency": "HUD",
        "level": "federal",
        "annual_spend_total": 3.6,
        "eligibility_rules": {
            **_NO_INCOME_TEST,
            "categorical": ["homeless_individuals_and_families"],
            "notes": "McKinney-Vento Act; includes CoC, ESG, and other programs.",
        },
        "benefit_type": "service",
        "domain": "housing",
        "cascade_types": [
            "legal_econ_social_geo_bio_fiscal",
            "social_psych_bio_fiscal",
        ],
        "enrollees_millions": 0.58,
        "notes": "Umbrella for federal homeless assistance programs.",
    },
    {  # 33
        "name": "Continuum of Care (CoC) Program",
        "code": "continuum_of_care",
        "agency": "HUD",
        "level": "federal",
        "annual_spend_total": 3.1,
        "eligibility_rules": {
            **_NO_INCOME_TEST,
            "categorical": [
                "homeless",
                "chronically_homeless",
                "at_risk_of_homelessness",
            ],
        },
        "benefit_type": "service",
        "domain": "housing",
        "cascade_types": [
            "legal_econ_social_geo_bio_fiscal",
            "social_psych_bio_fiscal",
        ],
        "enrollees_millions": 0.35,
        "notes": "Competitive grants; transitional, permanent supportive, rapid rehousing.",
    },

    # =====================================================================
    #  EDUCATION  (34-38)
    # =====================================================================
    {  # 34
        "name": "Pell Grants",
        "code": "pell_grants",
        "agency": "ED",
        "level": "federal",
        "annual_spend_total": 26.0,
        "eligibility_rules": {
            "efc_max": "varies",
            "categorical": ["undergraduate_students", "financial_need"],
            "notes": "Max award $7,395 (2024-25); based on expected family contribution.",
        },
        "benefit_type": "cash",
        "domain": "education",
        "cascade_types": ["env_cog_edu_econ_fiscal"],
        "enrollees_millions": 6.4,
        "notes": "Entitlement-like grant; largest federal student aid program.",
    },
    {  # 35
        "name": "Federal Student Loans",
        "code": "federal_student_loans",
        "agency": "ED",
        "level": "federal",
        "annual_spend_total": 95.0,
        "eligibility_rules": {
            **_NO_INCOME_TEST,
            "categorical": ["enrolled_postsecondary_students"],
            "notes": "Direct loans; subsidized limited to financial need.",
        },
        "benefit_type": "cash",
        "domain": "education",
        "cascade_types": ["env_cog_edu_econ_fiscal"],
        "enrollees_millions": 10.0,
        "notes": "Net cost reflects subsidy and default costs; outstanding balance ~$1.6T.",
    },
    {  # 36
        "name": "Head Start / Early Head Start",
        "code": "head_start",
        "agency": "ACF",
        "level": "federal",
        "annual_spend_total": 12.0,
        "eligibility_rules": {
            **_FPL_100,
            **_AGE_UNDER_6,
            "categorical": ["low_income_families", "homeless_children", "foster_children"],
        },
        "benefit_type": "service",
        "domain": "education",
        "cascade_types": ["env_cog_edu_econ_fiscal"],
        "enrollees_millions": 0.83,
        "notes": "Comprehensive early childhood education, health, and family services.",
    },
    {  # 37
        "name": "IDEA Special Education (Part B & C)",
        "code": "idea_special_ed",
        "agency": "ED",
        "level": "federal_state",
        "annual_spend_total": 15.0,
        "eligibility_rules": {
            **_NO_INCOME_TEST,
            **_AGE_UNDER_18,
            "categorical": ["children_with_disabilities"],
            "notes": "Ages 3-21 (Part B); birth-2 (Part C early intervention).",
        },
        "benefit_type": "service",
        "domain": "education",
        "cascade_types": [
            "env_cog_edu_econ_fiscal",
            "env_bio_econ_fiscal",
        ],
        "enrollees_millions": 7.5,
        "notes": "Federal contribution ~14% of excess cost; state/local funds majority.",
    },
    {  # 38
        "name": "Title I (ESEA / ESSA)",
        "code": "title_i",
        "agency": "ED",
        "level": "federal",
        "annual_spend_total": 18.4,
        "eligibility_rules": {
            **_NO_INCOME_TEST,
            "categorical": ["high_poverty_schools"],
            "notes": "School-wide programs at >=40% poverty; targeted assistance otherwise.",
        },
        "benefit_type": "service",
        "domain": "education",
        "cascade_types": ["env_cog_edu_econ_fiscal"],
        "enrollees_millions": 25.0,
        "notes": "Largest federal K-12 program; formula grants to LEAs.",
    },

    # =====================================================================
    #  WORKFORCE  (39-44)
    # =====================================================================
    {  # 39
        "name": "Workforce Innovation and Opportunity Act (WIOA)",
        "code": "wioa",
        "agency": "DOL",
        "level": "federal_state",
        "annual_spend_total": 3.4,
        "eligibility_rules": {
            **_NO_INCOME_TEST,
            "categorical": ["adults", "dislocated_workers", "youth"],
            "notes": "Priority for low-income and basic skills deficient.",
        },
        "benefit_type": "service",
        "domain": "workforce",
        "cascade_types": [
            "econ_psych_bio_fiscal",
            "legal_econ_social_geo_bio_fiscal",
        ],
        "enrollees_millions": 3.5,
        "notes": "Titles I-IV; American Job Centers (One-Stop system).",
    },
    {  # 40
        "name": "Vocational Rehabilitation (VR)",
        "code": "vocational_rehab",
        "agency": "ED-RSA",
        "level": "federal_state",
        "annual_spend_total": 3.8,
        "eligibility_rules": {
            **_NO_INCOME_TEST,
            "categorical": ["individuals_with_disabilities"],
            "notes": "Must have disability that is impediment to employment.",
        },
        "benefit_type": "service",
        "domain": "workforce",
        "cascade_types": [
            "econ_psych_bio_fiscal",
            "env_bio_econ_fiscal",
        ],
        "enrollees_millions": 1.0,
        "notes": "Title I of Rehabilitation Act; state VR agencies.",
    },
    {  # 41
        "name": "Senior Community Service Employment Program (SCSEP)",
        "code": "scsep",
        "agency": "DOL",
        "level": "federal",
        "annual_spend_total": 0.4,
        "eligibility_rules": {
            **_FPL_125,
            "age_min": 55,
            "categorical": ["low_income_seniors"],
        },
        "benefit_type": "service",
        "domain": "workforce",
        "cascade_types": ["econ_psych_bio_fiscal"],
        "enrollees_millions": 0.04,
        "notes": "Part-time community service jobs and job training for seniors.",
    },
    {  # 42
        "name": "Job Corps",
        "code": "job_corps",
        "agency": "DOL",
        "level": "federal",
        "annual_spend_total": 1.7,
        "eligibility_rules": {
            **_FPL_100,
            "age_min": 16,
            "age_max": 24,
            "categorical": ["low_income_youth", "high_school_dropout"],
        },
        "benefit_type": "service",
        "domain": "workforce",
        "cascade_types": [
            "env_cog_edu_econ_fiscal",
            "econ_social_legal_fiscal",
        ],
        "enrollees_millions": 0.05,
        "notes": "Residential education and training; ~120 centers nationwide.",
    },
    {  # 43
        "name": "AmeriCorps",
        "code": "americorps",
        "agency": "AmeriCorps",
        "level": "federal",
        "annual_spend_total": 1.1,
        "eligibility_rules": {
            **_NO_INCOME_TEST,
            "age_min": 17,
            "categorical": ["us_citizens_or_permanent_residents"],
        },
        "benefit_type": "service",
        "domain": "workforce",
        "cascade_types": ["econ_psych_bio_fiscal"],
        "enrollees_millions": 0.2,
        "notes": "National service; includes VISTA, NCCC, State/National programs.",
    },
    {  # 44
        "name": "Community Health Workers Programs",
        "code": "community_health_workers",
        "agency": "HRSA",
        "level": "federal_state",
        "annual_spend_total": 0.5,
        "eligibility_rules": {
            **_NO_INCOME_TEST,
            "categorical": ["underserved_communities"],
        },
        "benefit_type": "service",
        "domain": "workforce",
        "cascade_types": [
            "econ_psych_bio_fiscal",
            "social_psych_bio_fiscal",
        ],
        "enrollees_millions": 0.06,
        "notes": "CHW workforce development; Medicaid reimbursement growing in states.",
    },

    # =====================================================================
    #  JUSTICE  (45-50)
    # =====================================================================
    {  # 45
        "name": "Federal Bureau of Prisons",
        "code": "federal_prisons",
        "agency": "DOJ-BOP",
        "level": "federal",
        "annual_spend_total": 9.6,
        "eligibility_rules": {
            **_NO_INCOME_TEST,
            "categorical": ["federal_inmates"],
        },
        "benefit_type": "institutional",
        "domain": "justice",
        "cascade_types": [
            "legal_econ_social_geo_bio_fiscal",
            "econ_social_legal_fiscal",
        ],
        "enrollees_millions": 0.16,
        "notes": "~158,000 federal inmates; cost ~$42K/year per inmate.",
    },
    {  # 46
        "name": "State Prisons",
        "code": "state_prisons",
        "agency": "Various",
        "level": "state",
        "annual_spend_total": 57.0,
        "eligibility_rules": {
            **_NO_INCOME_TEST,
            "categorical": ["state_inmates"],
        },
        "benefit_type": "institutional",
        "domain": "justice",
        "cascade_types": [
            "legal_econ_social_geo_bio_fiscal",
            "econ_social_legal_fiscal",
        ],
        "enrollees_millions": 1.04,
        "notes": "~1.04 million state prisoners; average cost ~$47.5K/year.",
    },
    {  # 47
        "name": "County Jails",
        "code": "county_jails",
        "agency": "Various",
        "level": "local",
        "annual_spend_total": 30.0,
        "eligibility_rules": {
            **_NO_INCOME_TEST,
            "categorical": ["pretrial_detainees", "short_sentence_inmates"],
        },
        "benefit_type": "institutional",
        "domain": "justice",
        "cascade_types": [
            "legal_econ_social_geo_bio_fiscal",
            "econ_social_legal_fiscal",
        ],
        "enrollees_millions": 0.66,
        "notes": "~3,100 jails; ~10.3M annual admissions; high turnover.",
    },
    {  # 48
        "name": "Probation and Parole",
        "code": "probation_parole",
        "agency": "Various",
        "level": "state",
        "annual_spend_total": 10.5,
        "eligibility_rules": {
            **_NO_INCOME_TEST,
            "categorical": ["convicted_offenders_community_supervision"],
        },
        "benefit_type": "service",
        "domain": "justice",
        "cascade_types": [
            "legal_econ_social_geo_bio_fiscal",
            "econ_social_legal_fiscal",
        ],
        "enrollees_millions": 3.7,
        "notes": "~3 million on probation; ~800K on parole.",
    },
    {  # 49
        "name": "Drug Courts",
        "code": "drug_courts",
        "agency": "DOJ-SAMHSA",
        "level": "state",
        "annual_spend_total": 1.5,
        "eligibility_rules": {
            **_NO_INCOME_TEST,
            "categorical": ["nonviolent_drug_offenders"],
            "notes": "Judicial discretion; typically substance use disorder diagnosis.",
        },
        "benefit_type": "service",
        "domain": "justice",
        "cascade_types": [
            "econ_social_legal_fiscal",
            "social_psych_bio_fiscal",
        ],
        "enrollees_millions": 0.15,
        "notes": "~3,800 drug courts; evidence-based alternative to incarceration.",
    },
    {  # 50
        "name": "Juvenile Justice System",
        "code": "juvenile_justice",
        "agency": "OJJDP",
        "level": "state",
        "annual_spend_total": 8.0,
        "eligibility_rules": {
            **_NO_INCOME_TEST,
            **_AGE_UNDER_18,
            "categorical": ["juvenile_offenders"],
        },
        "benefit_type": "institutional",
        "domain": "justice",
        "cascade_types": [
            "econ_social_legal_fiscal",
            "legal_econ_social_geo_bio_fiscal",
            "env_cog_edu_econ_fiscal",
        ],
        "enrollees_millions": 0.36,
        "notes": "Detention, residential placement, and community supervision.",
    },

    # =====================================================================
    #  BEHAVIORAL HEALTH  (51-53)
    # =====================================================================
    {  # 51
        "name": "SAMHSA Block Grants (MHBG + SABG)",
        "code": "samhsa_block_grants",
        "agency": "SAMHSA",
        "level": "federal_state",
        "annual_spend_total": 5.8,
        "eligibility_rules": {
            **_NO_INCOME_TEST,
            "categorical": [
                "serious_mental_illness",
                "substance_use_disorder",
                "uninsured_underinsured",
            ],
        },
        "benefit_type": "service",
        "domain": "healthcare",
        "cascade_types": [
            "social_psych_bio_fiscal",
            "econ_social_legal_fiscal",
        ],
        "enrollees_millions": 8.0,
        "notes": "Mental Health Block Grant + Substance Abuse Prevention & Treatment BG.",
    },
    {  # 52
        "name": "Community Mental Health Services",
        "code": "community_mental_health",
        "agency": "SAMHSA",
        "level": "federal_state",
        "annual_spend_total": 2.2,
        "eligibility_rules": {
            **_NO_INCOME_TEST,
            "categorical": [
                "serious_mental_illness",
                "serious_emotional_disturbance_youth",
            ],
        },
        "benefit_type": "service",
        "domain": "healthcare",
        "cascade_types": [
            "social_psych_bio_fiscal",
            "econ_psych_bio_fiscal",
        ],
        "enrollees_millions": 6.0,
        "notes": "CCBHCs, CMHCs, and state mental health authority services.",
    },
    {  # 53
        "name": "340B Drug Pricing Program",
        "code": "340b_drug_pricing",
        "agency": "HRSA",
        "level": "federal",
        "annual_spend_total": 53.0,
        "eligibility_rules": {
            **_NO_INCOME_TEST,
            "categorical": ["patients_at_covered_entities"],
            "notes": "Covered entities include FQHCs, DSH hospitals, Ryan White grantees.",
        },
        "benefit_type": "in_kind",
        "domain": "healthcare",
        "cascade_types": [
            "econ_psych_bio_fiscal",
            "social_psych_bio_fiscal",
        ],
        "enrollees_millions": 12.0,
        "notes": "Drug discounts ~25-50%; $53B in estimated savings/program value.",
    },

    # =====================================================================
    #  CHILD & FAMILY  (54-57)
    # =====================================================================
    {  # 54
        "name": "Title IV-E Foster Care",
        "code": "title_iv_e_foster",
        "agency": "ACF",
        "level": "federal_state",
        "annual_spend_total": 9.0,
        "eligibility_rules": {
            **_NO_INCOME_TEST,
            **_AGE_UNDER_18,
            "categorical": [
                "children_removed_from_home",
                "judicial_determination",
            ],
        },
        "benefit_type": "service",
        "domain": "child_family",
        "cascade_types": [
            "econ_social_legal_fiscal",
            "social_psych_bio_fiscal",
        ],
        "enrollees_millions": 0.37,
        "notes": "Maintenance payments, admin, training; Family First Act reforms.",
    },
    {  # 55
        "name": "Title IV-B Child Welfare Services",
        "code": "title_iv_b_welfare",
        "agency": "ACF",
        "level": "federal_state",
        "annual_spend_total": 0.7,
        "eligibility_rules": {
            **_NO_INCOME_TEST,
            "categorical": ["families_at_risk", "children_in_care"],
        },
        "benefit_type": "service",
        "domain": "child_family",
        "cascade_types": [
            "econ_social_legal_fiscal",
            "social_psych_bio_fiscal",
        ],
        "enrollees_millions": 3.5,
        "notes": "Subparts 1 (Stephanie Tubbs Jones) and 2 (PSSF); prevention focus.",
    },
    {  # 56
        "name": "Adoption Assistance (Title IV-E)",
        "code": "adoption_assistance",
        "agency": "ACF",
        "level": "federal_state",
        "annual_spend_total": 3.5,
        "eligibility_rules": {
            **_NO_INCOME_TEST,
            "categorical": [
                "children_with_special_needs",
                "adopted_from_foster_care",
            ],
        },
        "benefit_type": "cash",
        "domain": "child_family",
        "cascade_types": ["social_psych_bio_fiscal"],
        "enrollees_millions": 0.55,
        "notes": "Monthly subsidies and Medicaid; de-linked from AFDC income test.",
    },
    {  # 57
        "name": "Child Care and Development Fund (CCDF)",
        "code": "ccdf_child_care",
        "agency": "ACF",
        "level": "federal_state",
        "annual_spend_total": 12.0,
        "eligibility_rules": {
            "income_pct_smi_max": 85,
            "categorical": [
                "working_families",
                "families_in_education_training",
                "children_under_13",
            ],
            "notes": "State median income (SMI) test; most states set lower.",
        },
        "benefit_type": "in_kind",
        "domain": "child_family",
        "cascade_types": [
            "econ_psych_bio_fiscal",
            "env_cog_edu_econ_fiscal",
        ],
        "enrollees_millions": 1.5,
        "notes": "Child care subsidies; only serves ~15% of eligible children.",
    },

    # =====================================================================
    #  ENERGY / UTILITIES  (58-59)
    # =====================================================================
    {  # 58
        "name": "Low Income Home Energy Assistance Program (LIHEAP)",
        "code": "liheap",
        "agency": "ACF",
        "level": "federal_state",
        "annual_spend_total": 4.1,
        "eligibility_rules": {
            **_FPL_150,
            "categorical": ["low_income_households"],
            "notes": "States may set up to 150% FPL or 60% state median income.",
        },
        "benefit_type": "cash",
        "domain": "energy",
        "cascade_types": [
            "econ_psych_bio_fiscal",
            "env_bio_econ_fiscal",
        ],
        "enrollees_millions": 5.3,
        "notes": "Heating and cooling assistance, crisis intervention, weatherization.",
    },
    {  # 59
        "name": "Weatherization Assistance Program (WAP)",
        "code": "weatherization",
        "agency": "DOE",
        "level": "federal_state",
        "annual_spend_total": 0.4,
        "eligibility_rules": {
            **_FPL_200,
            "categorical": [
                "low_income_households",
                "priority_elderly_disabled_children",
            ],
        },
        "benefit_type": "service",
        "domain": "energy",
        "cascade_types": [
            "env_bio_econ_fiscal",
            "econ_psych_bio_fiscal",
        ],
        "enrollees_millions": 0.035,
        "notes": "~35,000 homes/year weatherized; average savings ~$283/year.",
    },

    # =====================================================================
    #  HOMELESS / EMERGENCY  (60)
    # =====================================================================
    {  # 60
        "name": "Emergency Solutions Grants (ESG)",
        "code": "emergency_solutions_grants",
        "agency": "HUD",
        "level": "federal",
        "annual_spend_total": 0.3,
        "eligibility_rules": {
            **_NO_INCOME_TEST,
            "categorical": [
                "homeless",
                "at_risk_of_homelessness",
            ],
            "notes": "Homelessness prevention component has 30% AMI income test.",
        },
        "benefit_type": "service",
        "domain": "housing",
        "cascade_types": [
            "legal_econ_social_geo_bio_fiscal",
            "social_psych_bio_fiscal",
        ],
        "enrollees_millions": 0.30,
        "notes": "Street outreach, emergency shelter, rapid rehousing, prevention.",
    },

    # =====================================================================
    #  HEALTHCARE — ADDITIONAL  (61-63)
    # =====================================================================
    {  # 61
        "name": "Disproportionate Share Hospital (DSH) Payments",
        "code": "dsh_payments",
        "agency": "CMS",
        "level": "federal_state",
        "annual_spend_total": 21.0,
        "eligibility_rules": {
            **_NO_INCOME_TEST,
            "categorical": ["hospitals_serving_high_uninsured_medicaid_share"],
            "notes": "Hospital-level eligibility; DSH adjustment percentage threshold.",
        },
        "benefit_type": "in_kind",
        "domain": "healthcare",
        "cascade_types": [
            "econ_psych_bio_fiscal",
            "legal_econ_social_geo_bio_fiscal",
        ],
        "enrollees_millions": None,
        "notes": "~$21B combined federal/state; payments to safety-net hospitals.",
    },
    {  # 62
        "name": "Program of All-Inclusive Care for the Elderly (PACE)",
        "code": "pace",
        "agency": "CMS",
        "level": "federal_state",
        "annual_spend_total": 9.6,
        "eligibility_rules": {
            **_NO_INCOME_TEST,
            "age_min": 55,
            "categorical": [
                "nursing_home_eligible",
                "able_to_live_in_community",
            ],
        },
        "benefit_type": "service",
        "domain": "healthcare",
        "cascade_types": [
            "social_psych_bio_fiscal",
            "econ_psych_bio_fiscal",
        ],
        "enrollees_millions": 0.07,
        "notes": "Capitated model integrating all Medicare/Medicaid services; ~150 orgs.",
    },
    {  # 63
        "name": "Emergency Medicaid (EMTALA Uncompensated Care)",
        "code": "emergency_medicaid",
        "agency": "CMS",
        "level": "federal_state",
        "annual_spend_total": 6.5,
        "eligibility_rules": {
            **_NO_INCOME_TEST,
            "categorical": [
                "emergency_medical_condition",
                "otherwise_ineligible_for_medicaid",
            ],
        },
        "benefit_type": "in_kind",
        "domain": "healthcare",
        "cascade_types": [
            "econ_psych_bio_fiscal",
            "legal_econ_social_geo_bio_fiscal",
            "social_psych_bio_fiscal",
        ],
        "enrollees_millions": 2.0,
        "notes": "Emergency services for undocumented and other non-qualified aliens.",
    },
]
"""list[dict]: All 63 government programs tracked by THE DOME engine.

Programs are grouped by domain:
    - Healthcare (1-10): Medicare, Medicaid, CHIP, ACA, VA, TRICARE, etc.
    - Income Support (11-17): OASI, SSDI, SSI, TANF, UI, SSBG, CSBG
    - Tax Expenditures (18-22): EITC, CTC, CDCTC, MID, Premium Tax Credits
    - Food/Nutrition (23-25): SNAP, WIC, School Meals
    - Housing (26-33): Section 8, Public Housing, HOME, LIHTC, 811, 202, etc.
    - Education (34-38): Pell, Student Loans, Head Start, IDEA, Title I
    - Workforce (39-44): WIOA, VR, SCSEP, Job Corps, AmeriCorps, CHWs
    - Justice (45-50): Federal/State Prisons, Jails, Probation, Drug Courts, Juvenile
    - Behavioral Health (51-53): SAMHSA BGs, Community MH, 340B
    - Child & Family (54-57): Foster Care, Child Welfare, Adoption, CCDF
    - Energy (58-59): LIHEAP, Weatherization
    - Homeless/Emergency (60): ESG
    - Healthcare Additional (61-63): DSH, PACE, Emergency Medicaid

Each entry's ``cascade_types`` field references cascade IDs defined in
:mod:`dome.data.cascades`.
"""


def get_program(code: str) -> Dict[str, Any]:
    """Look up a single program by its short code.

    Parameters
    ----------
    code:
        Machine-readable program identifier (e.g. ``"medicaid"``).

    Returns
    -------
    dict
        The matching program dictionary.

    Raises
    ------
    KeyError
        If no program with the given code exists.
    """
    for program in PROGRAMS:
        if program["code"] == code:
            return program
    raise KeyError(f"No program with code '{code}'")


def programs_by_domain(domain: str) -> List[Dict[str, Any]]:
    """Return all programs in a given policy domain.

    Parameters
    ----------
    domain:
        One of ``healthcare``, ``income_support``, ``housing``, ``food``,
        ``education``, ``workforce``, ``justice``, ``child_family``,
        ``energy``, ``other``.

    Returns
    -------
    list[dict]
        Programs whose ``domain`` matches.
    """
    return [p for p in PROGRAMS if p["domain"] == domain]


def programs_by_cascade(cascade_id: str) -> List[Dict[str, Any]]:
    """Return all programs linked to a given cascade type.

    Parameters
    ----------
    cascade_id:
        A cascade identifier from :mod:`dome.data.cascades`
        (e.g. ``"econ_psych_bio_fiscal"``).

    Returns
    -------
    list[dict]
        Programs whose ``cascade_types`` list includes the given ID.
    """
    return [p for p in PROGRAMS if cascade_id in p["cascade_types"]]
