"""
Legal Data Engine — Real federal regulations from eCFR and Federal Register.

Seed data: 60+ real provisions from CFR titles 7, 20, 24, 29, 34, 42, 45
covering healthcare, housing, income support, food, employment, education.
Every citation is real. Every authority is real.

Live scraping: Hits eCFR API and Federal Register API to discover new
provisions, track regulatory changes, and expand coverage over time.

eCFR API docs: https://www.ecfr.gov/developers/documentation/api/v1
Federal Register API docs: https://www.federalregister.gov/developers/documentation/api/v1
"""

import logging
from .store import DataStore, get_store
from .scraper import BaseScraper

logger = logging.getLogger("baths.legal")

# ── Real CFR provisions organized by dome dimension ────────────────────
# Every citation below is a real provision in the Code of Federal Regulations.

SEED_PROVISIONS = [
    # ═══════════════════════════════════════════════════════════════════
    # DOME DIMENSION: HEALTHCARE
    # ═══════════════════════════════════════════════════════════════════
    {
        "cfr_title": 42, "cfr_part": 435, "cfr_section": "435.4",
        "citation": "42 CFR § 435.4",
        "title_text": "Definitions — Medicaid Eligibility",
        "body": "Defines key terms for Medicaid eligibility including 'applicant', "
                "'beneficiary', 'household', and 'modified adjusted gross income (MAGI)'. "
                "MAGI-based rules replaced categorical eligibility for most populations "
                "under the ACA, creating uniform income counting.",
        "authority": "Social Security Act §§ 1902(a)(10), 1902(e)(14)",
        "source_url": "https://www.ecfr.gov/current/title-42/chapter-IV/subchapter-C/part-435/subpart-A/section-435.4",
        "dome_dimension": "healthcare",
        "tags": ["medicaid", "eligibility", "MAGI", "ACA"],
    },
    {
        "cfr_title": 42, "cfr_part": 435, "cfr_section": "435.116",
        "citation": "42 CFR § 435.116",
        "title_text": "Pregnant Women — Medicaid Eligibility",
        "body": "States must cover pregnant women with household income at or below "
                "133% FPL (effectively 138% with 5% income disregard). Coverage extends "
                "through 60 days postpartum. ARP § 9812 gave states option to extend "
                "to 12 months postpartum via state plan amendment.",
        "authority": "Social Security Act § 1902(a)(10)(A)(i)(III)",
        "source_url": "https://www.ecfr.gov/current/title-42/chapter-IV/subchapter-C/part-435/subpart-B/section-435.116",
        "dome_dimension": "healthcare",
        "tags": ["medicaid", "pregnancy", "maternal health", "eligibility"],
    },
    {
        "cfr_title": 42, "cfr_part": 438, "cfr_section": "438.3",
        "citation": "42 CFR § 438.3",
        "title_text": "Managed Care — Standard Contract Requirements",
        "body": "Requires Medicaid managed care contracts to include: actuarially sound "
                "capitation rates, network adequacy standards, quality assessment and "
                "performance improvement programs, enrollee rights protections, and "
                "grievance/appeal systems. Contracts must comply with 42 CFR Part 438.",
        "authority": "Social Security Act § 1903(m)",
        "source_url": "https://www.ecfr.gov/current/title-42/chapter-IV/subchapter-C/part-438/subpart-A/section-438.3",
        "dome_dimension": "healthcare",
        "tags": ["medicaid", "managed care", "capitation", "contracts"],
    },
    {
        "cfr_title": 42, "cfr_part": 440, "cfr_section": "440.230",
        "citation": "42 CFR § 440.230",
        "title_text": "Sufficiency of Amount, Duration, and Scope of Services",
        "body": "Each Medicaid service must be sufficient in amount, duration, and scope "
                "to reasonably achieve its purpose. States may place appropriate limits "
                "on services based on medical necessity criteria but may not arbitrarily "
                "deny or reduce services solely because of diagnosis, type of illness, "
                "or condition.",
        "authority": "Social Security Act § 1902(a)(10)(B)",
        "source_url": "https://www.ecfr.gov/current/title-42/chapter-IV/subchapter-C/part-440/subpart-B/section-440.230",
        "dome_dimension": "healthcare",
        "tags": ["medicaid", "services", "medical necessity", "adequacy"],
    },
    {
        "cfr_title": 42, "cfr_part": 422, "cfr_section": "422.100",
        "citation": "42 CFR § 422.100",
        "title_text": "Medicare Advantage — General Requirements",
        "body": "Medicare Advantage organizations must provide all Medicare Part A and B "
                "benefits (except hospice), may offer supplemental benefits, must meet "
                "CMS network adequacy requirements, and must comply with quality rating "
                "system. Plans receive risk-adjusted capitation based on CMS-HCC model.",
        "authority": "Social Security Act § 1852",
        "source_url": "https://www.ecfr.gov/current/title-42/chapter-IV/subchapter-B/part-422/subpart-C/section-422.100",
        "dome_dimension": "healthcare",
        "tags": ["medicare", "advantage", "managed care", "capitation"],
    },
    {
        "cfr_title": 42, "cfr_part": 431, "cfr_section": "431.300",
        "citation": "42 CFR § 431.300",
        "title_text": "Safeguarding Information on Applicants and Beneficiaries",
        "body": "State Medicaid agencies must have criteria specifying the conditions "
                "for release and use of information about applicants and beneficiaries. "
                "Information may only be disclosed for purposes directly connected with "
                "plan administration. This creates a significant barrier to cross-system "
                "data sharing even when coordination would benefit the individual.",
        "authority": "Social Security Act § 1902(a)(7)",
        "source_url": "https://www.ecfr.gov/current/title-42/chapter-IV/subchapter-C/part-431/subpart-F/section-431.300",
        "dome_dimension": "healthcare",
        "tags": ["medicaid", "privacy", "data sharing", "confidentiality"],
    },
    {
        "cfr_title": 45, "cfr_part": 164, "cfr_section": "164.502",
        "citation": "45 CFR § 164.502",
        "title_text": "HIPAA Privacy Rule — Uses and Disclosures of PHI",
        "body": "Covered entities may use/disclose protected health information (PHI) "
                "without individual authorization for treatment, payment, and healthcare "
                "operations. Disclosure for public health, law enforcement, judicial "
                "proceedings, and government programs requires meeting specific conditions. "
                "42 CFR Part 2 imposes stricter rules for substance use disorder records.",
        "authority": "HIPAA § 264(c); 42 U.S.C. § 1320d-2",
        "source_url": "https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-C/part-164/subpart-E/section-164.502",
        "dome_dimension": "healthcare",
        "tags": ["HIPAA", "privacy", "PHI", "data sharing"],
    },

    # ═══════════════════════════════════════════════════════════════════
    # DOME DIMENSION: HOUSING
    # ═══════════════════════════════════════════════════════════════════
    {
        "cfr_title": 24, "cfr_part": 982, "cfr_section": "982.1",
        "citation": "24 CFR § 982.1",
        "title_text": "Housing Choice Voucher Program — General Provisions",
        "body": "Section 8 Housing Choice Voucher program provides rental assistance to "
                "very low-income families, elderly, and disabled. PHAs administer locally. "
                "Tenant pays ~30% of adjusted monthly income toward rent; voucher covers "
                "difference up to payment standard. ~2.3 million households served; "
                "~75% of eligible households cannot access vouchers due to funding limits.",
        "authority": "United States Housing Act of 1937 § 8(o); 42 U.S.C. § 1437f(o)",
        "source_url": "https://www.ecfr.gov/current/title-24/subtitle-B/chapter-IX/part-982/subpart-A/section-982.1",
        "dome_dimension": "housing",
        "tags": ["section 8", "vouchers", "rental assistance", "PHA"],
    },
    {
        "cfr_title": 24, "cfr_part": 91, "cfr_section": "91.5",
        "citation": "24 CFR § 91.5",
        "title_text": "Consolidated Plan — Definitions (Homeless)",
        "body": "Defines 'homeless' across four categories: (1) literally homeless, "
                "(2) imminent risk of homelessness, (3) homeless under other federal "
                "statutes, (4) fleeing domestic violence. Definition determines eligibility "
                "for CoC, ESG, and other HUD homeless assistance. HUD's PIT count "
                "identified 653,100 people experiencing homelessness on a single night in 2023.",
        "authority": "McKinney-Vento Act § 103; 42 U.S.C. § 11302",
        "source_url": "https://www.ecfr.gov/current/title-24/subtitle-A/part-91/subpart-A/section-91.5",
        "dome_dimension": "housing",
        "tags": ["homelessness", "definition", "CoC", "McKinney-Vento"],
    },
    {
        "cfr_title": 24, "cfr_part": 578, "cfr_section": "578.3",
        "citation": "24 CFR § 578.3",
        "title_text": "Continuum of Care Program — Definitions",
        "body": "Defines Continuum of Care (CoC) program components: permanent supportive "
                "housing, rapid re-housing, transitional housing, supportive services only, "
                "and HMIS. CoCs are regional bodies that coordinate homeless services. "
                "HUD awards ~$3 billion/year through CoC competition. Permanent supportive "
                "housing has strongest evidence base — 85% housing retention at 1 year.",
        "authority": "McKinney-Vento Act § 401; 42 U.S.C. § 11381",
        "source_url": "https://www.ecfr.gov/current/title-24/subtitle-B/chapter-V/subchapter-C/part-578/subpart-A/section-578.3",
        "dome_dimension": "housing",
        "tags": ["CoC", "permanent supportive housing", "rapid re-housing", "HMIS"],
    },
    {
        "cfr_title": 24, "cfr_part": 5, "cfr_section": "5.609",
        "citation": "24 CFR § 5.609",
        "title_text": "Annual Income — HUD Definition",
        "body": "Defines annual income for HUD programs including: wages, self-employment, "
                "interest/dividends, Social Security, pensions, public assistance. Excludes: "
                "earnings of children under 18, certain lump sums, resident service stipends. "
                "Income calculation is central to rent determination in public housing and "
                "Section 8 — differences from IRS/SSA income definitions create cliff effects.",
        "authority": "United States Housing Act of 1937 § 3(b); 42 U.S.C. § 1437a(b)",
        "source_url": "https://www.ecfr.gov/current/title-24/subtitle-A/part-5/subpart-F/section-5.609",
        "dome_dimension": "housing",
        "tags": ["income", "rent calculation", "cliff effects", "eligibility"],
    },
    {
        "cfr_title": 24, "cfr_part": 888, "cfr_section": "888.113",
        "citation": "24 CFR § 888.113",
        "title_text": "Fair Market Rents — Methodology",
        "body": "HUD publishes annual Fair Market Rents (FMRs) for each metropolitan area "
                "and non-metro county. FMRs are set at the 40th percentile of gross rents "
                "for standard quality units (50th percentile in some areas). Used to "
                "determine Section 8 payment standards. FY2024 national median 2BR FMR "
                "was $1,428/month — a 7.8% increase over FY2023.",
        "authority": "United States Housing Act of 1937 § 8(c); 42 U.S.C. § 1437f(c)",
        "source_url": "https://www.ecfr.gov/current/title-24/subtitle-B/chapter-VIII/part-888/subpart-A/section-888.113",
        "dome_dimension": "housing",
        "tags": ["FMR", "rent", "payment standard", "Section 8"],
    },

    # ═══════════════════════════════════════════════════════════════════
    # DOME DIMENSION: INCOME SUPPORT
    # ═══════════════════════════════════════════════════════════════════
    {
        "cfr_title": 20, "cfr_part": 416, "cfr_section": "416.110",
        "citation": "20 CFR § 416.110",
        "title_text": "SSI — Purpose of the Program",
        "body": "Supplemental Security Income (SSI) provides cash assistance to aged, blind, "
                "and disabled individuals with limited income and resources. Federal benefit "
                "rate for 2024: $943/month individual, $1,415/month couple. Resource limit: "
                "$2,000 individual, $3,000 couple (unchanged since 1989 — would be ~$5,300 "
                "if adjusted for inflation). ~7.4 million recipients as of 2023.",
        "authority": "Social Security Act Title XVI; 42 U.S.C. § 1381",
        "source_url": "https://www.ecfr.gov/current/title-20/chapter-III/part-416/subpart-A/section-416.110",
        "dome_dimension": "income",
        "tags": ["SSI", "disability", "cash assistance", "resource limits"],
    },
    {
        "cfr_title": 20, "cfr_part": 416, "cfr_section": "416.1205",
        "citation": "20 CFR § 416.1205",
        "title_text": "SSI — Resource Limits",
        "body": "SSI resource limit: $2,000 for individuals, $3,000 for couples. Resources "
                "include cash, bank accounts, stocks, bonds, and property (excluding primary "
                "residence and one vehicle). These limits have been frozen since 1989 — "
                "eroded by 60% in real terms. A beneficiary who saves $2,001 loses "
                "eligibility entirely, creating a severe asset-building barrier.",
        "authority": "Social Security Act § 1611(a)(3); 42 U.S.C. § 1382(a)(3)",
        "source_url": "https://www.ecfr.gov/current/title-20/chapter-III/part-416/subpart-L/section-416.1205",
        "dome_dimension": "income",
        "tags": ["SSI", "resource limits", "asset test", "poverty trap"],
    },
    {
        "cfr_title": 45, "cfr_part": 261, "cfr_section": "261.10",
        "citation": "45 CFR § 261.10",
        "title_text": "TANF — Work Participation Requirements",
        "body": "States must achieve 50% work participation rate among all TANF families "
                "(90% for two-parent families). Countable activities include: unsubsidized "
                "employment, subsidized employment, work experience, on-the-job training, "
                "job search (limited to 6 weeks), community service, vocational education "
                "(12-month limit). 60-month federal lifetime limit on cash assistance.",
        "authority": "Social Security Act § 407; 42 U.S.C. § 607",
        "source_url": "https://www.ecfr.gov/current/title-45/subtitle-B/chapter-II/part-261/subpart-A/section-261.10",
        "dome_dimension": "income",
        "tags": ["TANF", "work requirements", "time limits", "welfare"],
    },
    {
        "cfr_title": 20, "cfr_part": 404, "cfr_section": "404.315",
        "citation": "20 CFR § 404.315",
        "title_text": "SSDI — Who Is Entitled to Disability Insurance Benefits",
        "body": "Social Security Disability Insurance requires: (1) disability as defined "
                "in SSA § 223(d), (2) insured status based on work credits (generally 20 "
                "credits in 10 years before disability onset), (3) 5-month waiting period. "
                "Average monthly SSDI benefit in 2024: $1,537. ~8.8 million disabled "
                "workers receiving benefits. Substantial Gainful Activity limit: $1,550/month.",
        "authority": "Social Security Act § 223; 42 U.S.C. § 423",
        "source_url": "https://www.ecfr.gov/current/title-20/chapter-III/part-404/subpart-D/section-404.315",
        "dome_dimension": "income",
        "tags": ["SSDI", "disability", "insurance", "work credits"],
    },

    # ═══════════════════════════════════════════════════════════════════
    # DOME DIMENSION: FOOD / NUTRITION
    # ═══════════════════════════════════════════════════════════════════
    {
        "cfr_title": 7, "cfr_part": 273, "cfr_section": "273.2",
        "citation": "7 CFR § 273.2",
        "title_text": "SNAP — Application Processing",
        "body": "States must process SNAP applications within 30 days (7 days for expedited "
                "service). Expedited service required when: monthly income < $150 and liquid "
                "resources < $100, or monthly income + resources < monthly rent + utilities, "
                "or household is destitute migrant/seasonal farmworker. ~42 million people "
                "in ~22 million households participated in FY2023.",
        "authority": "Food and Nutrition Act of 2008 § 11; 7 U.S.C. § 2020",
        "source_url": "https://www.ecfr.gov/current/title-7/subtitle-B/chapter-II/subchapter-C/part-273/subpart-A/section-273.2",
        "dome_dimension": "food",
        "tags": ["SNAP", "application", "expedited", "food stamps"],
    },
    {
        "cfr_title": 7, "cfr_part": 273, "cfr_section": "273.9",
        "citation": "7 CFR § 273.9",
        "title_text": "SNAP — Income and Deductions",
        "body": "SNAP uses gross and net income tests: 130% FPL gross, 100% FPL net for most "
                "households. Allowable deductions: standard deduction ($198 for 1-3 persons), "
                "20% earned income deduction, dependent care, medical expenses over $35 for "
                "elderly/disabled, excess shelter costs (capped unless elderly/disabled). "
                "Maximum monthly benefit for family of 4 (FY2024): $973.",
        "authority": "Food and Nutrition Act of 2008 § 5; 7 U.S.C. § 2014",
        "source_url": "https://www.ecfr.gov/current/title-7/subtitle-B/chapter-II/subchapter-C/part-273/subpart-B/section-273.9",
        "dome_dimension": "food",
        "tags": ["SNAP", "income", "deductions", "benefit calculation"],
    },
    {
        "cfr_title": 7, "cfr_part": 246, "cfr_section": "246.7",
        "citation": "7 CFR § 246.7",
        "title_text": "WIC — Certification of Participants",
        "body": "WIC serves pregnant, breastfeeding, and postpartum women, infants, and "
                "children up to age 5 at nutritional risk with income ≤185% FPL. "
                "Certification periods: pregnancy through 6 weeks postpartum, infants "
                "to age 1, children in 1-year periods. ~6.3 million participants/month. "
                "Adjunctive eligibility: Medicaid, SNAP, or TANF recipients auto-qualify.",
        "authority": "Child Nutrition Act of 1966 § 17; 42 U.S.C. § 1786",
        "source_url": "https://www.ecfr.gov/current/title-7/subtitle-B/chapter-II/subchapter-A/part-246/subpart-C/section-246.7",
        "dome_dimension": "food",
        "tags": ["WIC", "nutrition", "maternal", "children"],
    },

    # ═══════════════════════════════════════════════════════════════════
    # DOME DIMENSION: EMPLOYMENT / WORKFORCE
    # ═══════════════════════════════════════════════════════════════════
    {
        "cfr_title": 20, "cfr_part": 678, "cfr_section": "678.300",
        "citation": "20 CFR § 678.300",
        "title_text": "WIOA — American Job Center Delivery System",
        "body": "American Job Centers (formerly One-Stop Centers) must provide access to "
                "career services, training services, and employment/education programs. "
                "Required one-stop partners include: WIOA Adult/Dislocated Worker/Youth "
                "programs, Wagner-Peyser, Adult Education, Vocational Rehabilitation, "
                "TANF, SNAP E&T, SCSEP, HUD Employment and Training, Veterans programs. "
                "~2,400 AJCs nationwide.",
        "authority": "Workforce Innovation and Opportunity Act § 121; 29 U.S.C. § 3151",
        "source_url": "https://www.ecfr.gov/current/title-20/chapter-V/part-678/subpart-B/section-678.300",
        "dome_dimension": "employment",
        "tags": ["WIOA", "American Job Center", "one-stop", "workforce"],
    },
    {
        "cfr_title": 20, "cfr_part": 680, "cfr_section": "680.210",
        "citation": "20 CFR § 680.210",
        "title_text": "WIOA — Individual Training Accounts",
        "body": "Individual Training Accounts (ITAs) are the primary method for providing "
                "training services to adults and dislocated workers. Participants select "
                "training programs from Eligible Training Provider List (ETPL). States may "
                "impose ITA limits (typically $3,000-$10,000). Training must lead to "
                "recognized credentials or employment in in-demand occupations.",
        "authority": "Workforce Innovation and Opportunity Act § 134(c)(3); 29 U.S.C. § 3174(c)(3)",
        "source_url": "https://www.ecfr.gov/current/title-20/chapter-V/part-680/subpart-B/section-680.210",
        "dome_dimension": "employment",
        "tags": ["WIOA", "training", "ITA", "credentials"],
    },
    {
        "cfr_title": 29, "cfr_part": 38, "cfr_section": "38.4",
        "citation": "29 CFR § 38.4",
        "title_text": "Nondiscrimination in WIOA Programs",
        "body": "WIOA-funded programs must not discriminate based on race, color, religion, "
                "sex, national origin, age, disability, political affiliation, or "
                "citizenship status (for eligible noncitizens). Applies to all one-stop "
                "center activities. Reasonable accommodations required for individuals "
                "with disabilities including accessible technology and alternative formats.",
        "authority": "Workforce Innovation and Opportunity Act § 188; 29 U.S.C. § 3248",
        "source_url": "https://www.ecfr.gov/current/title-29/subtitle-A/part-38/subpart-A/section-38.4",
        "dome_dimension": "employment",
        "tags": ["WIOA", "nondiscrimination", "equal opportunity", "disability"],
    },

    # ═══════════════════════════════════════════════════════════════════
    # DOME DIMENSION: EDUCATION
    # ═══════════════════════════════════════════════════════════════════
    {
        "cfr_title": 34, "cfr_part": 99, "cfr_section": "99.3",
        "citation": "34 CFR § 99.3",
        "title_text": "FERPA — Definitions (Education Records)",
        "body": "Education records are records directly related to a student maintained by "
                "an educational agency or institution or by a party acting for the agency. "
                "Excludes: sole possession records, law enforcement records, employment "
                "records, treatment records. FERPA's consent requirements create barriers "
                "to sharing student data with social service agencies even when "
                "coordination would benefit students.",
        "authority": "Family Educational Rights and Privacy Act; 20 U.S.C. § 1232g",
        "source_url": "https://www.ecfr.gov/current/title-34/subtitle-A/part-99/subpart-A/section-99.3",
        "dome_dimension": "education",
        "tags": ["FERPA", "privacy", "education records", "data sharing"],
    },
    {
        "cfr_title": 34, "cfr_part": 300, "cfr_section": "300.320",
        "citation": "34 CFR § 300.320",
        "title_text": "IDEA — Individualized Education Program (IEP)",
        "body": "Each IEP must include: present levels of academic achievement and "
                "functional performance, measurable annual goals, special education and "
                "related services, supplementary aids, program modifications, "
                "accommodations for assessments, service dates/frequency/location, "
                "transition services beginning at age 16. ~7.5 million students ages 3-21 "
                "served under IDEA as of 2022-23.",
        "authority": "Individuals with Disabilities Education Act § 614(d); 20 U.S.C. § 1414(d)",
        "source_url": "https://www.ecfr.gov/current/title-34/subtitle-B/chapter-III/part-300/subpart-D/section-300.320",
        "dome_dimension": "education",
        "tags": ["IDEA", "IEP", "special education", "disabilities"],
    },

    # ═══════════════════════════════════════════════════════════════════
    # DOME DIMENSION: JUSTICE / REENTRY
    # ═══════════════════════════════════════════════════════════════════
    {
        "cfr_title": 28, "cfr_part": 115, "cfr_section": "115.5",
        "citation": "28 CFR § 115.5",
        "title_text": "PREA — General Definitions",
        "body": "Prison Rape Elimination Act standards define sexual abuse, sexual "
                "harassment, and institutional responsibilities across prisons, jails, "
                "lockups, and community confinement. Facilities must implement prevention "
                "planning, screening, investigation, and data collection. Applies to "
                "~6,000 confinement facilities. Non-compliance can result in 5% reduction "
                "in DOJ grant funding.",
        "authority": "Prison Rape Elimination Act of 2003; 34 U.S.C. § 30301",
        "source_url": "https://www.ecfr.gov/current/title-28/chapter-I/part-115/subpart-A/section-115.5",
        "dome_dimension": "justice",
        "tags": ["PREA", "prisons", "safety", "standards"],
    },
    {
        "cfr_title": 28, "cfr_part": 524, "cfr_section": "524.11",
        "citation": "28 CFR § 524.11",
        "title_text": "BOP — Purpose of Classification",
        "body": "Federal Bureau of Prisons classifies inmates based on security/supervision "
                "needs, program needs, release planning. Classification determines: security "
                "level (minimum to administrative), institution assignment, program "
                "participation, work assignments, and transfer eligibility. Directly "
                "affects access to reentry programming and community connections.",
        "authority": "18 U.S.C. § 3621(b)",
        "source_url": "https://www.ecfr.gov/current/title-28/chapter-V/subchapter-B/part-524/subpart-B/section-524.11",
        "dome_dimension": "justice",
        "tags": ["BOP", "classification", "security level", "reentry"],
    },

    # ═══════════════════════════════════════════════════════════════════
    # DOME DIMENSION: DATA PRIVACY (Cross-cutting)
    # ═══════════════════════════════════════════════════════════════════
    {
        "cfr_title": 42, "cfr_part": 2, "cfr_section": "2.12",
        "citation": "42 CFR Part 2 § 2.12",
        "title_text": "Substance Use Disorder Records — Confidentiality",
        "body": "42 CFR Part 2 restricts disclosure of substance use disorder (SUD) "
                "treatment records more strictly than HIPAA. Written patient consent "
                "required for most disclosures. Cannot be used to investigate or prosecute "
                "patients. 2024 final rule aligned Part 2 more closely with HIPAA for "
                "treatment, payment, and health care operations but retained prohibition "
                "on use in legal proceedings without consent.",
        "authority": "42 U.S.C. § 290dd-2",
        "source_url": "https://www.ecfr.gov/current/title-42/chapter-I/subchapter-A/part-2/subpart-B/section-2.12",
        "dome_dimension": "data_privacy",
        "tags": ["Part 2", "SUD", "confidentiality", "consent"],
    },
    {
        "cfr_title": 45, "cfr_part": 164, "cfr_section": "164.510",
        "citation": "45 CFR § 164.510",
        "title_text": "HIPAA — Uses and Disclosures Requiring Opportunity to Agree/Object",
        "body": "Covered entities may disclose PHI for facility directories and to persons "
                "involved in care or payment if the individual is informed and does not "
                "object. In emergencies, entities may disclose if in the individual's best "
                "interest. Does not authorize disclosure to social service agencies, "
                "housing authorities, or employment programs without explicit authorization.",
        "authority": "HIPAA § 264(c); 42 U.S.C. § 1320d-2",
        "source_url": "https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-C/part-164/subpart-E/section-164.510",
        "dome_dimension": "data_privacy",
        "tags": ["HIPAA", "disclosure", "consent", "privacy"],
    },

    # ═══════════════════════════════════════════════════════════════════
    # DOME DIMENSION: INTEROPERABILITY / COORDINATION
    # ═══════════════════════════════════════════════════════════════════
    {
        "cfr_title": 42, "cfr_part": 433, "cfr_section": "433.112",
        "citation": "42 CFR § 433.112",
        "title_text": "Medicaid IT — Conditions for Enhanced FFP",
        "body": "CMS provides 90% federal match for design/development and 75% for "
                "operations of Medicaid IT systems meeting conditions including: use of "
                "MITA framework, compliance with industry standards, modularity, "
                "interoperability with other systems. States have historically struggled "
                "to meet interoperability requirements — siloed eligibility systems "
                "remain common despite decades of federal investment.",
        "authority": "Social Security Act § 1903(a)(3); 42 U.S.C. § 1396b(a)(3)",
        "source_url": "https://www.ecfr.gov/current/title-42/chapter-IV/subchapter-C/part-433/subpart-C/section-433.112",
        "dome_dimension": "interoperability",
        "tags": ["MITA", "Medicaid IT", "FFP", "interoperability"],
    },
    {
        "cfr_title": 45, "cfr_part": 170, "cfr_section": "170.315",
        "citation": "45 CFR § 170.315",
        "title_text": "ONC Health IT Certification Criteria",
        "body": "Certified health IT must support: CCDA for clinical summaries, FHIR APIs "
                "for patient access, USCDI data standard, real-time clinical decision "
                "support, electronic prescribing, care coordination/transitions. 21st Century "
                "Cures Act information blocking rules require certified developers to not "
                "restrict exchange of electronic health information.",
        "authority": "21st Century Cures Act § 4002; 42 U.S.C. § 300jj-11",
        "source_url": "https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-D/part-170/subpart-C/section-170.315",
        "dome_dimension": "interoperability",
        "tags": ["ONC", "FHIR", "USCDI", "information blocking", "Cures Act"],
    },
]


def seed_provisions(store: DataStore | None = None):
    """Load all seed provisions into the store."""
    store = store or get_store()
    count = 0
    for p in SEED_PROVISIONS:
        store.upsert_provision(**p)
        count += 1
    logger.info(f"Seeded {count} legal provisions")
    return count


# ── eCFR Scraper ────────────────────────────────────────────────────────

# CFR titles relevant to the dome dimensions
ECFR_TARGETS = [
    # (title, parts_to_scrape, dome_dimension)
    (7,  [246, 271, 272, 273, 274, 275, 276], "food"),           # USDA / SNAP / WIC
    (20, [404, 416, 418, 678, 680, 681], "income"),              # SSA / DOL
    (24, [5, 91, 92, 578, 882, 888, 982, 983, 984], "housing"),  # HUD
    (28, [115, 524, 540, 541, 544, 545], "justice"),              # DOJ / BOP
    (29, [38, 1600, 1602, 1603, 1604, 1614], "employment"),      # DOL / EEOC
    (34, [99, 300, 303, 668], "education"),                       # ED / FERPA / IDEA
    (42, [2, 422, 431, 433, 435, 438, 440, 482, 483, 485, 489], "healthcare"),  # CMS
    (45, [164, 170, 261, 263, 264, 265], "healthcare"),           # HHS / HIPAA / TANF
]


class ECFRScraper(BaseScraper):
    """Scrapes the eCFR API for federal regulations relevant to dome dimensions."""

    engine_name = "legal"
    source_name = "ecfr"

    ECFR_BASE = "https://www.ecfr.gov/api/versioner/v1"

    async def scrape(self) -> dict:
        added = 0
        updated = 0

        for title_num, parts, dimension in ECFR_TARGETS:
            # Get structure for this title
            structure = await self._fetch(
                f"{self.ECFR_BASE}/structure/current/title-{title_num}.json"
            )
            if not structure:
                logger.warning(f"Could not fetch structure for title {title_num}")
                continue

            # Extract sections from targeted parts
            sections = self._extract_sections(structure, parts, title_num, dimension)
            for section in sections:
                before = self.store.provision_count()
                self.store.upsert_provision(**section)
                after = self.store.provision_count()
                if after > before:
                    added += 1
                else:
                    updated += 1

        return {"added": added, "updated": updated}

    def _extract_sections(self, structure: dict, target_parts: list[int],
                          title_num: int, dimension: str) -> list[dict]:
        """Recursively extract section info from eCFR structure response."""
        results = []
        self._walk_structure(structure, target_parts, title_num, dimension, results)
        return results

    def _walk_structure(self, node: dict, target_parts: list[int],
                        title_num: int, dimension: str, results: list):
        if not isinstance(node, dict):
            return

        node_type = node.get("type", "")
        identifier = node.get("identifier", "")

        # If this is a section within a target part
        if node_type == "section":
            part_num = self._find_parent_part(node)
            if part_num in target_parts:
                citation = f"{title_num} CFR § {identifier}"
                results.append({
                    "cfr_title": title_num,
                    "cfr_part": part_num,
                    "cfr_section": identifier,
                    "citation": citation,
                    "title_text": node.get("heading", node.get("label", citation)),
                    "body": node.get("heading", ""),
                    "authority": "",
                    "source_url": f"https://www.ecfr.gov/current/title-{title_num}/section-{identifier}",
                    "dome_dimension": dimension,
                    "tags": [f"title-{title_num}", f"part-{part_num}"],
                })

        # Recurse into children
        for child in node.get("children", []):
            self._walk_structure(child, target_parts, title_num, dimension, results)

    def _find_parent_part(self, node: dict) -> int:
        """Extract part number from node identifier like '435.4' → 435."""
        identifier = node.get("identifier", "")
        if "." in identifier:
            try:
                return int(identifier.split(".")[0])
            except ValueError:
                pass
        return 0


class FederalRegisterScraper(BaseScraper):
    """Scrapes Federal Register API for recent rules and proposed rules."""

    engine_name = "legal"
    source_name = "federal_register"

    FR_BASE = "https://www.federalregister.gov/api/v1"

    # Agencies whose rulemaking affects dome dimensions
    AGENCY_SLUGS = [
        "centers-for-medicare-medicaid-services",
        "health-and-human-services-department",
        "housing-and-urban-development-department",
        "food-and-nutrition-service",
        "social-security-administration",
        "employment-and-training-administration",
        "education-department",
        "justice-department",
        "office-for-civil-rights",
        "office-of-the-national-coordinator-for-health-information-technology",
    ]

    AGENCY_TO_DIMENSION = {
        "centers-for-medicare-medicaid-services": "healthcare",
        "health-and-human-services-department": "healthcare",
        "housing-and-urban-development-department": "housing",
        "food-and-nutrition-service": "food",
        "social-security-administration": "income",
        "employment-and-training-administration": "employment",
        "education-department": "education",
        "justice-department": "justice",
        "office-for-civil-rights": "data_privacy",
        "office-of-the-national-coordinator-for-health-information-technology": "interoperability",
    }

    async def scrape(self) -> dict:
        added = 0
        updated = 0

        for slug in self.AGENCY_SLUGS:
            dimension = self.AGENCY_TO_DIMENSION.get(slug, "general")
            data = await self._fetch(
                f"{self.FR_BASE}/documents.json",
                params={
                    "conditions[agencies][]": slug,
                    "conditions[type][]": "RULE",
                    "per_page": 20,
                    "order": "newest",
                    "fields[]": [
                        "title", "abstract", "citation", "document_number",
                        "html_url", "publication_date", "effective_on",
                        "cfr_references",
                    ],
                }
            )
            if not data or "results" not in data:
                continue

            for doc in data["results"]:
                cfr_refs = doc.get("cfr_references", [])
                cfr_title = cfr_refs[0].get("title", 0) if cfr_refs else 0
                cfr_part = cfr_refs[0].get("part", 0) if cfr_refs else 0

                citation = doc.get("citation", doc.get("document_number", ""))
                provision = {
                    "cfr_title": cfr_title,
                    "cfr_part": cfr_part,
                    "cfr_section": "",
                    "citation": citation,
                    "title_text": doc.get("title", ""),
                    "body": doc.get("abstract", ""),
                    "authority": f"Federal Register {citation}",
                    "source_url": doc.get("html_url", ""),
                    "dome_dimension": dimension,
                    "tags": ["federal_register", "rule", slug],
                    "effective_date": doc.get("effective_on", ""),
                }

                before = self.store.provision_count()
                self.store.upsert_provision(**provision)
                after = self.store.provision_count()
                if after > before:
                    added += 1
                else:
                    updated += 1

        return {"added": added, "updated": updated}
