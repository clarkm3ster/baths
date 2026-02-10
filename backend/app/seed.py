import json
from sqlalchemy.orm import Session
from app.models import Provision


def _j(obj) -> str:
    return json.dumps(obj)


PROVISIONS: list[dict] = [
    # =========================================================================
    # HEALTH DOMAIN (30+ provisions)
    # =========================================================================
    {
        "citation": "42 U.S.C. § 1396d(r)",
        "title": "Medicaid EPSDT — Early and Periodic Screening, Diagnostic, and Treatment",
        "full_text": "Medicaid must cover all medically necessary services for individuals under 21, including screening services, vision services, dental services, hearing services, and any other medically necessary service listed in Section 1905(a) of the Social Security Act — even if the state does not cover that service for adults.",
        "domain": "health",
        "provision_type": "right",
        "applies_when": _j({"insurance": ["medicaid"], "age": ["under_21"]}),
        "enforcement_mechanisms": _j([
            "42 U.S.C. § 1983 — federal civil rights action",
            "State fair hearing under 42 CFR § 431.200",
            "CMS complaint to state Medicaid agency",
            "Federal court injunction"
        ]),
        "source_url": "https://www.law.cornell.edu/uscode/text/42/1396d",
        "cross_references": _j(["42 U.S.C. § 1396a(a)(10)(A)", "42 U.S.C. § 1396a(a)(43)"])
    },
    {
        "citation": "42 U.S.C. § 1396a(a)(10)(A)",
        "title": "Medicaid Mandatory Coverage Groups",
        "full_text": "States must provide Medicaid coverage to categorically needy individuals, including families meeting AFDC income standards, pregnant women and children under 6 at 133% FPL, children 6-18 at 100% FPL, SSI recipients, and certain Medicare beneficiaries. Coverage must include all mandatory services.",
        "domain": "health",
        "provision_type": "right",
        "applies_when": _j({"income_level": ["below_133_fpl", "below_100_fpl"], "insurance": ["medicaid", "none"], "age": ["under_21", "pregnant"]}),
        "enforcement_mechanisms": _j([
            "State fair hearing under 42 CFR § 431.200",
            "42 U.S.C. § 1983 action in federal court",
            "CMS enforcement against state plan violations"
        ]),
        "source_url": "https://www.law.cornell.edu/uscode/text/42/1396a",
        "cross_references": _j(["42 U.S.C. § 1396d(r)", "42 U.S.C. § 1396d(a)"])
    },
    {
        "citation": "42 U.S.C. § 1396a(a)(43)",
        "title": "Medicaid EPSDT Outreach and Informing Requirements",
        "full_text": "States must inform all Medicaid-eligible individuals under 21 of the availability of EPSDT services, provide or arrange for screening services, and arrange for corrective treatment the screening indicates is needed.",
        "domain": "health",
        "provision_type": "obligation",
        "applies_when": _j({"insurance": ["medicaid"], "age": ["under_21"]}),
        "enforcement_mechanisms": _j([
            "42 U.S.C. § 1983 action for failure to inform",
            "CMS oversight and compliance reviews",
            "State Medicaid fair hearing"
        ]),
        "source_url": "https://www.law.cornell.edu/uscode/text/42/1396a",
        "cross_references": _j(["42 U.S.C. § 1396d(r)"])
    },
    {
        "citation": "42 CFR Part 438",
        "title": "Medicaid Managed Care Protections",
        "full_text": "Managed care organizations serving Medicaid beneficiaries must meet requirements for access to services, network adequacy, quality assessment, grievance systems, and enrollee rights. MCOs must cover out-of-network services when network is inadequate and ensure timely access to care.",
        "domain": "health",
        "provision_type": "protection",
        "applies_when": _j({"insurance": ["medicaid_managed_care"]}),
        "enforcement_mechanisms": _j([
            "Internal MCO grievance process under 42 CFR § 438.402",
            "State fair hearing after exhausting MCO grievance",
            "External quality review under 42 CFR § 438.350",
            "CMS sanctions against non-compliant MCOs"
        ]),
        "source_url": "https://www.ecfr.gov/current/title-42/chapter-IV/subchapter-C/part-438",
        "cross_references": _j(["42 U.S.C. § 1396u-2", "42 CFR § 438.206"])
    },
    {
        "citation": "42 U.S.C. § 1396n(c)",
        "title": "HCBS Waiver — Home and Community-Based Services",
        "full_text": "States may request waivers to provide home and community-based services to individuals who would otherwise require institutional care. Services may include case management, homemaker services, home health aide services, personal care, adult day health, habilitation, and respite care.",
        "domain": "health",
        "provision_type": "right",
        "applies_when": _j({"insurance": ["medicaid"], "disability": ["physical", "intellectual", "developmental"], "setting": ["community", "home"]}),
        "enforcement_mechanisms": _j([
            "State fair hearing for denial of waiver services",
            "42 U.S.C. § 1983 for systemic failures",
            "ADA/Olmstead integration mandate",
            "CMS waiver compliance reviews"
        ]),
        "source_url": "https://www.law.cornell.edu/uscode/text/42/1396n",
        "cross_references": _j(["42 U.S.C. § 12132", "Olmstead v. L.C., 527 U.S. 581 (1999)"])
    },
    {
        "citation": "42 U.S.C. § 1396n(i)",
        "title": "Self-Directed Personal Assistance Services",
        "full_text": "States may offer self-directed personal assistance services under Medicaid, allowing individuals to hire, fire, and supervise their own personal care workers and manage an individual budget for services.",
        "domain": "health",
        "provision_type": "right",
        "applies_when": _j({"insurance": ["medicaid"], "disability": ["physical", "intellectual", "developmental"]}),
        "enforcement_mechanisms": _j([
            "State fair hearing",
            "CMS waiver compliance oversight"
        ]),
        "source_url": "https://www.law.cornell.edu/uscode/text/42/1396n",
        "cross_references": _j(["42 U.S.C. § 1396n(c)", "42 U.S.C. § 1396n(k)"])
    },
    {
        "citation": "29 U.S.C. § 1185a",
        "title": "Mental Health Parity and Addiction Equity Act (MHPAEA)",
        "full_text": "Group health plans that provide mental health or substance use disorder benefits may not impose less favorable benefit limitations on those benefits than on medical/surgical benefits. Financial requirements and treatment limitations must be no more restrictive than the predominant requirements applied to substantially all medical/surgical benefits.",
        "domain": "health",
        "provision_type": "protection",
        "applies_when": _j({"insurance": ["employer", "marketplace"], "condition": ["mental_health", "substance_use"]}),
        "enforcement_mechanisms": _j([
            "ERISA claim under 29 U.S.C. § 1132",
            "DOL complaint for ERISA plans",
            "State insurance department complaint for insured plans",
            "CMS enforcement for Medicaid/CHIP plans",
            "Federal lawsuit for denial of benefits"
        ]),
        "source_url": "https://www.law.cornell.edu/uscode/text/29/1185a",
        "cross_references": _j(["42 U.S.C. § 300gg-26", "42 U.S.C. § 18022"])
    },
    {
        "citation": "42 U.S.C. § 1395dd",
        "title": "EMTALA — Emergency Medical Treatment and Active Labor Act",
        "full_text": "Any hospital that participates in Medicare and has an emergency department must provide an appropriate medical screening examination to anyone who comes to the emergency department requesting treatment, regardless of ability to pay. If an emergency condition exists, the hospital must stabilize the patient before transfer or discharge.",
        "domain": "health",
        "provision_type": "right",
        "applies_when": _j({"setting": ["emergency_department"], "insurance": ["any", "none"]}),
        "enforcement_mechanisms": _j([
            "Private right of action against hospital under 42 U.S.C. § 1395dd(d)(2)",
            "CMS investigation and civil monetary penalties up to $50,000",
            "Hospital exclusion from Medicare program",
            "State medical board complaint against physician"
        ]),
        "source_url": "https://www.law.cornell.edu/uscode/text/42/1395dd",
        "cross_references": _j(["42 CFR § 489.24"])
    },
    {
        "citation": "42 U.S.C. § 18022",
        "title": "ACA Essential Health Benefits",
        "full_text": "Plans in the individual and small group market must cover ten essential health benefit categories: ambulatory care, emergency services, hospitalization, maternity and newborn care, mental health and substance use disorder services, prescription drugs, rehabilitative and habilitative services, laboratory services, preventive and wellness services, and pediatric services including dental and vision.",
        "domain": "health",
        "provision_type": "right",
        "applies_when": _j({"insurance": ["marketplace", "individual", "small_group"]}),
        "enforcement_mechanisms": _j([
            "Internal plan appeal under 29 CFR § 2560.503-1",
            "External review under 45 CFR Part 147",
            "State insurance department complaint",
            "HHS enforcement for federally-facilitated marketplace plans"
        ]),
        "source_url": "https://www.law.cornell.edu/uscode/text/42/18022",
        "cross_references": _j(["29 U.S.C. § 1185a", "42 U.S.C. § 300gg-13"])
    },
    {
        "citation": "42 U.S.C. § 300gg-13",
        "title": "ACA Preventive Services Without Cost-Sharing",
        "full_text": "Non-grandfathered health plans must cover recommended preventive services without imposing cost-sharing. This includes services rated A or B by the USPSTF, ACIP-recommended immunizations, HRSA-supported preventive care for infants, children, adolescents, and women.",
        "domain": "health",
        "provision_type": "right",
        "applies_when": _j({"insurance": ["marketplace", "employer", "individual"]}),
        "enforcement_mechanisms": _j([
            "Internal plan appeal",
            "External review",
            "DOL complaint for employer plans",
            "State insurance department complaint"
        ]),
        "source_url": "https://www.law.cornell.edu/uscode/text/42/300gg-13",
        "cross_references": _j(["42 U.S.C. § 18022"])
    },
    {
        "citation": "42 U.S.C. § 18116",
        "title": "Section 1557 ACA — Nondiscrimination in Health Programs",
        "full_text": "Individuals shall not be excluded from participation in, denied benefits of, or subjected to discrimination under any health program or activity receiving Federal financial assistance on the basis of race, color, national origin, sex, age, or disability. Applies to hospitals, clinics, insurers on marketplace, and any entity receiving HHS funding.",
        "domain": "health",
        "provision_type": "protection",
        "applies_when": _j({"insurance": ["any"], "setting": ["healthcare_facility", "insurance"]}),
        "enforcement_mechanisms": _j([
            "OCR complaint to HHS within 180 days",
            "Private right of action in federal court",
            "Administrative enforcement by HHS"
        ]),
        "source_url": "https://www.law.cornell.edu/uscode/text/42/18116",
        "cross_references": _j(["42 U.S.C. § 2000d", "29 U.S.C. § 794", "42 U.S.C. § 12132"])
    },
    {
        "citation": "42 CFR Part 2",
        "title": "Confidentiality of Substance Use Disorder Patient Records",
        "full_text": "Records of the identity, diagnosis, prognosis, or treatment of any patient maintained in connection with a federally assisted substance use disorder program are confidential. These records may not be disclosed without patient consent except in limited circumstances. Violations are subject to criminal penalties.",
        "domain": "health",
        "provision_type": "protection",
        "applies_when": _j({"condition": ["substance_use"], "setting": ["treatment_program"]}),
        "enforcement_mechanisms": _j([
            "Criminal penalties under 42 U.S.C. § 290dd-2",
            "Court order required for nonconsensual disclosure",
            "SAMHSA complaint",
            "Federal lawsuit for unauthorized disclosure"
        ]),
        "source_url": "https://www.ecfr.gov/current/title-42/chapter-I/subchapter-A/part-2",
        "cross_references": _j(["42 U.S.C. § 290dd-2", "45 CFR Parts 160 and 164"])
    },
    {
        "citation": "42 U.S.C. § 1395i-3",
        "title": "Nursing Home Residents' Rights (Medicare)",
        "full_text": "Skilled nursing facilities must protect and promote the rights of each resident, including the right to be free from physical or mental abuse, the right to participate in care planning, the right to privacy, the right to voice grievances, and the right to be free from unnecessary chemical and physical restraints.",
        "domain": "health",
        "provision_type": "right",
        "applies_when": _j({"setting": ["nursing_facility", "skilled_nursing"], "insurance": ["medicare", "medicaid"]}),
        "enforcement_mechanisms": _j([
            "State survey and certification under 42 CFR Part 483",
            "CMS civil monetary penalties",
            "State ombudsman complaint under Older Americans Act",
            "42 U.S.C. § 1983 action"
        ]),
        "source_url": "https://www.law.cornell.edu/uscode/text/42/1395i-3",
        "cross_references": _j(["42 CFR § 483.10", "42 U.S.C. § 1396r"])
    },
    {
        "citation": "42 U.S.C. § 1396r",
        "title": "Nursing Facility Requirements (Medicaid)",
        "full_text": "Medicaid nursing facilities must provide services to attain or maintain the highest practicable physical, mental, and psychosocial well-being of each resident. Facilities must conduct comprehensive assessments, develop care plans, and ensure adequate staffing.",
        "domain": "health",
        "provision_type": "right",
        "applies_when": _j({"setting": ["nursing_facility"], "insurance": ["medicaid"]}),
        "enforcement_mechanisms": _j([
            "State survey and enforcement",
            "CMS civil monetary penalties up to $10,000/day",
            "Long-term care ombudsman",
            "42 U.S.C. § 1983 for systemic violations"
        ]),
        "source_url": "https://www.law.cornell.edu/uscode/text/42/1396r",
        "cross_references": _j(["42 U.S.C. § 1395i-3", "42 CFR Part 483"])
    },
    {
        "citation": "42 U.S.C. § 1382(e)(1)(A)",
        "title": "Medicaid Eligibility for SSI Recipients",
        "full_text": "In most states, individuals who receive SSI are automatically eligible for Medicaid. Known as the '1634 states,' these jurisdictions provide Medicaid eligibility concurrent with SSI eligibility without a separate application process.",
        "domain": "health",
        "provision_type": "right",
        "applies_when": _j({"benefits": ["ssi"], "insurance": ["medicaid"]}),
        "enforcement_mechanisms": _j([
            "State Medicaid fair hearing",
            "42 U.S.C. § 1983 action",
            "CMS compliance review"
        ]),
        "source_url": "https://www.law.cornell.edu/uscode/text/42/1382",
        "cross_references": _j(["42 U.S.C. § 1396a(a)(10)(A)(i)(II)"])
    },
    {
        "citation": "42 U.S.C. § 300gg-14",
        "title": "ACA — Dependent Coverage Until Age 26",
        "full_text": "Group health plans and individual health insurance issuers offering dependent coverage must make coverage available for adult children until the child turns 26 years of age, regardless of marital status, student status, financial dependency, or eligibility for employer-sponsored coverage.",
        "domain": "health",
        "provision_type": "right",
        "applies_when": _j({"age": ["under_26"], "insurance": ["employer", "marketplace", "individual"]}),
        "enforcement_mechanisms": _j([
            "DOL complaint for employer plans",
            "State insurance department complaint",
            "Internal appeal and external review"
        ]),
        "source_url": "https://www.law.cornell.edu/uscode/text/42/300gg-14",
        "cross_references": _j(["42 U.S.C. § 18022"])
    },
    {
        "citation": "42 U.S.C. § 300gg-3",
        "title": "ACA — Prohibition on Preexisting Condition Exclusions",
        "full_text": "A group health plan or health insurance issuer may not impose any preexisting condition exclusion. No individual may be denied coverage or charged higher premiums based on health status, medical history, claims experience, disability, or genetic information.",
        "domain": "health",
        "provision_type": "protection",
        "applies_when": _j({"insurance": ["marketplace", "employer", "individual"], "condition": ["any_preexisting"]}),
        "enforcement_mechanisms": _j([
            "HHS/CMS enforcement",
            "State insurance department complaint",
            "DOL complaint for ERISA plans",
            "Federal lawsuit"
        ]),
        "source_url": "https://www.law.cornell.edu/uscode/text/42/300gg-3",
        "cross_references": _j(["42 U.S.C. § 300gg-4", "42 U.S.C. § 18022"])
    },
    {
        "citation": "42 U.S.C. § 1395(y)(b)",
        "title": "Medicare Entitlement for Disabled Individuals Under 65",
        "full_text": "Individuals under 65 who have received SSDI for 24 months are entitled to Medicare Part A (hospital insurance) and eligible for Part B (medical insurance). Individuals with end-stage renal disease or ALS are eligible without the 24-month waiting period.",
        "domain": "health",
        "provision_type": "right",
        "applies_when": _j({"benefits": ["ssdi"], "disability": ["any"], "age": ["under_65"]}),
        "enforcement_mechanisms": _j([
            "Medicare appeal process (redetermination, reconsideration, ALJ, Appeals Council, federal court)",
            "CMS complaint",
            "1-800-MEDICARE"
        ]),
        "source_url": "https://www.law.cornell.edu/uscode/text/42/1395",
        "cross_references": _j(["42 U.S.C. § 426", "42 U.S.C. § 426-1"])
    },
    {
        "citation": "42 U.S.C. § 1396d(a)(4)(B)",
        "title": "Medicaid Family Planning Services",
        "full_text": "Federal Medicaid law requires states to cover family planning services and supplies for individuals of childbearing age. Federal match is 90%, the highest rate for any Medicaid service. States may extend coverage to individuals up to a higher income level through state plan amendments.",
        "domain": "health",
        "provision_type": "right",
        "applies_when": _j({"insurance": ["medicaid"], "age": ["childbearing"]}),
        "enforcement_mechanisms": _j([
            "State Medicaid fair hearing",
            "42 U.S.C. § 1983 action",
            "CMS oversight"
        ]),
        "source_url": "https://www.law.cornell.edu/uscode/text/42/1396d",
        "cross_references": _j(["42 U.S.C. § 1396a(a)(10)"])
    },
    {
        "citation": "42 U.S.C. § 1396a(a)(25)",
        "title": "Medicaid as Payer of Last Resort — Third Party Liability",
        "full_text": "Medicaid must pay for covered services and then seek reimbursement from liable third parties. Providers may not refuse to furnish services to a Medicaid recipient because of a third-party liability issue. Medicaid beneficiaries cannot be held liable for the cost of services.",
        "domain": "health",
        "provision_type": "protection",
        "applies_when": _j({"insurance": ["medicaid"]}),
        "enforcement_mechanisms": _j([
            "State fair hearing",
            "42 U.S.C. § 1983 action",
            "Provider sanction for balance billing"
        ]),
        "source_url": "https://www.law.cornell.edu/uscode/text/42/1396a",
        "cross_references": _j(["42 CFR § 433.136"])
    },
    {
        "citation": "42 U.S.C. § 1396a(e)(14)",
        "title": "Medicaid for Former Foster Youth",
        "full_text": "States must provide Medicaid coverage to former foster care youth under age 26 who were in foster care and receiving Medicaid at age 18 (or older age at which the state's foster care assistance ends). Coverage is available regardless of income.",
        "domain": "health",
        "provision_type": "right",
        "applies_when": _j({"age": ["under_26"], "background": ["former_foster_care"]}),
        "enforcement_mechanisms": _j([
            "State Medicaid fair hearing",
            "42 U.S.C. § 1983",
            "CMS enforcement"
        ]),
        "source_url": "https://www.law.cornell.edu/uscode/text/42/1396a",
        "cross_references": _j(["42 U.S.C. § 18022"])
    },
    {
        "citation": "42 U.S.C. § 1396a(a)(10)(A)(i)(VIII)",
        "title": "Medicaid Expansion Under ACA",
        "full_text": "In states that have adopted Medicaid expansion, coverage is available to adults ages 19-64 with income up to 138% of the federal poverty level. The expansion population receives the alternative benefit plan which must include essential health benefits.",
        "domain": "health",
        "provision_type": "right",
        "applies_when": _j({"income_level": ["below_138_fpl"], "age": ["19_to_64"], "insurance": ["none", "medicaid"]}),
        "enforcement_mechanisms": _j([
            "State Medicaid fair hearing",
            "42 U.S.C. § 1983",
            "Healthcare.gov enrollment assistance"
        ]),
        "source_url": "https://www.law.cornell.edu/uscode/text/42/1396a",
        "cross_references": _j(["42 U.S.C. § 18022", "42 U.S.C. § 1396d(y)"])
    },
    {
        "citation": "42 U.S.C. § 1396a(bb)",
        "title": "FQHC Prospective Payment — Federally Qualified Health Centers",
        "full_text": "Federally Qualified Health Centers are entitled to prospective payment under Medicaid. FQHCs must serve all patients regardless of ability to pay and must offer sliding fee scale discounts. They provide primary care, dental, mental health, and substance use disorder services.",
        "domain": "health",
        "provision_type": "right",
        "applies_when": _j({"insurance": ["any", "none"], "income_level": ["any"]}),
        "enforcement_mechanisms": _j([
            "HRSA oversight of FQHC grant conditions",
            "Patient complaint to FQHC and HRSA",
            "State Medicaid fair hearing for coverage denials"
        ]),
        "source_url": "https://www.law.cornell.edu/uscode/text/42/1396a",
        "cross_references": _j(["42 U.S.C. § 254b"])
    },
    {
        "citation": "45 CFR Parts 160 and 164",
        "title": "HIPAA Privacy and Security Rules",
        "full_text": "The HIPAA Privacy Rule protects the privacy of individually identifiable health information. Individuals have the right to access their own medical records, request amendments, receive an accounting of disclosures, and file complaints about privacy violations. The minimum necessary standard limits use and disclosure to what is needed.",
        "domain": "health",
        "provision_type": "protection",
        "applies_when": _j({"setting": ["healthcare_facility", "insurance", "health_plan"]}),
        "enforcement_mechanisms": _j([
            "OCR complaint to HHS within 180 days",
            "State attorney general enforcement",
            "Civil monetary penalties up to $1.5M per violation category per year",
            "Criminal penalties for knowing violations"
        ]),
        "source_url": "https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-C/part-164",
        "cross_references": _j(["42 U.S.C. § 1320d", "42 CFR Part 2"])
    },
    {
        "citation": "42 U.S.C. § 1396d(a)(13)",
        "title": "Medicaid Rehabilitative Services",
        "full_text": "Medicaid may cover rehabilitative services, including medical or remedial services recommended by a physician for maximum reduction of physical or mental disability and restoration of a recipient to the best possible functional level. States that elect this option must provide services sufficient to achieve these goals.",
        "domain": "health",
        "provision_type": "right",
        "applies_when": _j({"insurance": ["medicaid"], "disability": ["physical", "mental"]}),
        "enforcement_mechanisms": _j([
            "State Medicaid fair hearing",
            "42 U.S.C. § 1983",
            "CMS compliance review"
        ]),
        "source_url": "https://www.law.cornell.edu/uscode/text/42/1396d",
        "cross_references": _j(["42 U.S.C. § 1396d(r)", "42 U.S.C. § 1396n(c)"])
    },
    {
        "citation": "42 U.S.C. § 1395x(dd)",
        "title": "Medicare/Medicaid Hospice Benefits",
        "full_text": "Individuals with a terminal illness and a life expectancy of 6 months or less may elect hospice care. Hospice benefits include nursing care, medical social services, counseling, short-term inpatient care, home health aide services, medical supplies, and bereavement counseling for families.",
        "domain": "health",
        "provision_type": "right",
        "applies_when": _j({"insurance": ["medicare", "medicaid"], "condition": ["terminal_illness"]}),
        "enforcement_mechanisms": _j([
            "Medicare appeals process",
            "State Medicaid fair hearing",
            "State hospice licensing board complaint"
        ]),
        "source_url": "https://www.law.cornell.edu/uscode/text/42/1395x",
        "cross_references": _j(["42 CFR Part 418"])
    },
    {
        "citation": "42 U.S.C. § 1320a-7b(d)(1)",
        "title": "Anti-Kickback Statute — Patient Protection",
        "full_text": "It is a criminal offense to knowingly and willfully offer, pay, solicit, or receive remuneration to induce or reward referrals of items or services reimbursable by federal healthcare programs. This protects patients from being treated as profit centers and ensures medical decisions are based on medical necessity.",
        "domain": "health",
        "provision_type": "protection",
        "applies_when": _j({"insurance": ["medicare", "medicaid", "tricare"]}),
        "enforcement_mechanisms": _j([
            "OIG investigation and exclusion from federal programs",
            "Criminal prosecution — felony up to 10 years",
            "Civil monetary penalties up to $100,000 per violation",
            "Qui tam (whistleblower) action under False Claims Act"
        ]),
        "source_url": "https://www.law.cornell.edu/uscode/text/42/1320a-7b",
        "cross_references": _j(["31 U.S.C. § 3729", "42 U.S.C. § 1320a-7a"])
    },
    {
        "citation": "42 U.S.C. § 256b",
        "title": "340B Drug Pricing Program",
        "full_text": "Covered entities (FQHCs, disproportionate share hospitals, Ryan White clinics, and others) are eligible to purchase outpatient drugs at significantly reduced prices. Pharmaceutical manufacturers must offer these discounts as a condition of having their drugs covered by Medicaid.",
        "domain": "health",
        "provision_type": "right",
        "applies_when": _j({"setting": ["fqhc", "dsh_hospital", "ryan_white_clinic"]}),
        "enforcement_mechanisms": _j([
            "HRSA 340B Program audit",
            "Administrative dispute resolution process",
            "Manufacturer compliance requirements"
        ]),
        "source_url": "https://www.law.cornell.edu/uscode/text/42/256b",
        "cross_references": _j(["42 U.S.C. § 1396r-8"])
    },
    {
        "citation": "42 U.S.C. § 290bb-36",
        "title": "Garrett Lee Smith Memorial Act — Youth Suicide Prevention",
        "full_text": "Authorizes grants for youth suicide early intervention and prevention strategies, campus mental health programs, and state and tribal youth suicide prevention plans. States must develop comprehensive strategies for preventing youth suicide and improving access to mental health services.",
        "domain": "health",
        "provision_type": "right",
        "applies_when": _j({"age": ["under_21", "under_26"], "condition": ["mental_health", "suicide_risk"]}),
        "enforcement_mechanisms": _j([
            "SAMHSA grant oversight",
            "State mental health authority accountability"
        ]),
        "source_url": "https://www.law.cornell.edu/uscode/text/42/290bb-36",
        "cross_references": _j(["42 U.S.C. § 290bb-32"])
    },

    # =========================================================================
    # CIVIL RIGHTS DOMAIN (20+ provisions)
    # =========================================================================
    {
        "citation": "42 U.S.C. § 12132",
        "title": "ADA Title II — Public Services and Programs",
        "full_text": "No qualified individual with a disability shall, by reason of such disability, be excluded from participation in or be denied the benefits of the services, programs, or activities of a public entity, or be subjected to discrimination by any such entity. Public entities must make reasonable modifications to policies, practices, and procedures.",
        "domain": "civil_rights",
        "provision_type": "protection",
        "applies_when": _j({"disability": ["any"], "setting": ["government", "public_program", "public_facility"]}),
        "enforcement_mechanisms": _j([
            "DOJ complaint within 180 days",
            "Private right of action in federal court — compensatory damages available",
            "State/local government grievance procedure under 28 CFR § 35.107",
            "DOJ pattern or practice investigation"
        ]),
        "source_url": "https://www.law.cornell.edu/uscode/text/42/12132",
        "cross_references": _j(["28 CFR Part 35", "29 U.S.C. § 794", "42 U.S.C. § 12182"])
    },
    {
        "citation": "42 U.S.C. § 12182",
        "title": "ADA Title III — Public Accommodations",
        "full_text": "No individual shall be discriminated against on the basis of disability in the full and equal enjoyment of the goods, services, facilities, privileges, advantages, or accommodations of any place of public accommodation. Public accommodations must remove architectural barriers where readily achievable and provide auxiliary aids and services.",
        "domain": "civil_rights",
        "provision_type": "protection",
        "applies_when": _j({"disability": ["any"], "setting": ["private_business", "public_accommodation", "restaurant", "hotel", "store"]}),
        "enforcement_mechanisms": _j([
            "Private right of action for injunctive relief",
            "DOJ enforcement — civil penalties up to $75,000 (first violation), $150,000 (subsequent)",
            "Attorney's fees under 42 U.S.C. § 12205",
            "State disability rights law claims (may allow damages)"
        ]),
        "source_url": "https://www.law.cornell.edu/uscode/text/42/12182",
        "cross_references": _j(["28 CFR Part 36", "42 U.S.C. § 12132"])
    },
    {
        "citation": "42 U.S.C. § 12112",
        "title": "ADA Title I — Employment Discrimination",
        "full_text": "No covered entity shall discriminate against a qualified individual on the basis of disability in regard to job application procedures, hiring, advancement, discharge, compensation, training, and other terms, conditions, and privileges of employment. Employers must provide reasonable accommodations unless doing so would cause undue hardship.",
        "domain": "civil_rights",
        "provision_type": "protection",
        "applies_when": _j({"disability": ["any"], "setting": ["employment"], "employer_size": ["15_or_more"]}),
        "enforcement_mechanisms": _j([
            "EEOC charge within 180/300 days",
            "Federal lawsuit after right-to-sue letter",
            "Back pay, reinstatement, compensatory and punitive damages (capped)",
            "State/local fair employment agency complaint"
        ]),
        "source_url": "https://www.law.cornell.edu/uscode/text/42/12112",
        "cross_references": _j(["29 CFR Part 1630", "29 U.S.C. § 794"])
    },
    {
        "citation": "29 U.S.C. § 794",
        "title": "Section 504 of the Rehabilitation Act",
        "full_text": "No otherwise qualified individual with a disability shall, solely by reason of her or his disability, be excluded from the participation in, be denied the benefits of, or be subjected to discrimination under any program or activity receiving Federal financial assistance. Section 504 applies to all recipients of federal funding.",
        "domain": "civil_rights",
        "provision_type": "protection",
        "applies_when": _j({"disability": ["any"], "setting": ["federally_funded"]}),
        "enforcement_mechanisms": _j([
            "Administrative complaint to funding agency within 180 days",
            "Private right of action in federal court — compensatory damages available",
            "Agency enforcement — fund termination",
            "Attorney's fees under 29 U.S.C. § 794a"
        ]),
        "source_url": "https://www.law.cornell.edu/uscode/text/29/794",
        "cross_references": _j(["42 U.S.C. § 12132", "34 CFR Part 104", "45 CFR Part 84"])
    },
    {
        "citation": "Olmstead v. L.C., 527 U.S. 581 (1999)",
        "title": "Olmstead Integration Mandate",
        "full_text": "Under the ADA, individuals with disabilities have a right to receive state-funded services in the most integrated setting appropriate to their needs. Unjustified institutionalization of persons with disabilities is a form of discrimination. States must make reasonable modifications to enable community placement when: treatment professionals determine community placement is appropriate, the individual does not oppose it, and placement can be reasonably accommodated.",
        "domain": "civil_rights",
        "provision_type": "right",
        "applies_when": _j({"disability": ["any"], "setting": ["institution", "nursing_facility", "psychiatric_facility"], "preference": ["community_living"]}),
        "enforcement_mechanisms": _j([
            "DOJ investigation and enforcement",
            "Private right of action under ADA Title II",
            "State Olmstead/transition plan compliance",
            "Federal court injunction and consent decree"
        ]),
        "source_url": "https://www.law.cornell.edu/supct/html/98-536.ZS.html",
        "cross_references": _j(["42 U.S.C. § 12132", "42 U.S.C. § 1396n(c)", "28 CFR § 35.130(d)"])
    },
    {
        "citation": "42 U.S.C. § 2000d",
        "title": "Title VI — Nondiscrimination in Federally Assisted Programs",
        "full_text": "No person in the United States shall, on the ground of race, color, or national origin, be excluded from participation in, be denied the benefits of, or be subjected to discrimination under any program or activity receiving Federal financial assistance. Includes requirement for meaningful access for limited English proficient individuals.",
        "domain": "civil_rights",
        "provision_type": "protection",
        "applies_when": _j({"setting": ["federally_funded"], "characteristic": ["race", "national_origin", "limited_english"]}),
        "enforcement_mechanisms": _j([
            "Administrative complaint to funding agency within 180 days",
            "Private right of action for intentional discrimination",
            "DOJ coordination and enforcement",
            "Fund termination proceedings"
        ]),
        "source_url": "https://www.law.cornell.edu/uscode/text/42/2000d",
        "cross_references": _j(["42 U.S.C. § 18116", "Executive Order 13166"])
    },
    {
        "citation": "42 U.S.C. § 2000e-2",
        "title": "Title VII — Employment Discrimination",
        "full_text": "It is unlawful for an employer to discriminate against any individual with respect to compensation, terms, conditions, or privileges of employment because of race, color, religion, sex, or national origin. Applies to employers with 15 or more employees.",
        "domain": "civil_rights",
        "provision_type": "protection",
        "applies_when": _j({"setting": ["employment"], "employer_size": ["15_or_more"], "characteristic": ["race", "sex", "religion", "national_origin"]}),
        "enforcement_mechanisms": _j([
            "EEOC charge within 180/300 days",
            "Right-to-sue letter and federal lawsuit",
            "Back pay, reinstatement, compensatory and punitive damages",
            "State/local fair employment agency"
        ]),
        "source_url": "https://www.law.cornell.edu/uscode/text/42/2000e-2",
        "cross_references": _j(["42 U.S.C. § 1981", "42 U.S.C. § 2000e-5"])
    },
    {
        "citation": "42 U.S.C. § 1983",
        "title": "Section 1983 — Civil Action for Deprivation of Rights",
        "full_text": "Every person who, under color of any statute, ordinance, regulation, custom, or usage of any State, subjects any citizen or person within the jurisdiction to the deprivation of any rights, privileges, or immunities secured by the Constitution and federal laws, shall be liable to the party injured in an action at law or equity.",
        "domain": "civil_rights",
        "provision_type": "enforcement",
        "applies_when": _j({"setting": ["government", "public_program"], "violation": ["constitutional_rights", "federal_statutory_rights"]}),
        "enforcement_mechanisms": _j([
            "Federal lawsuit — compensatory and punitive damages",
            "Injunctive and declaratory relief",
            "Attorney's fees under 42 U.S.C. § 1988",
            "Class action for systemic violations"
        ]),
        "source_url": "https://www.law.cornell.edu/uscode/text/42/1983",
        "cross_references": _j(["42 U.S.C. § 1988", "42 U.S.C. § 1985"])
    },
    {
        "citation": "42 U.S.C. § 12203",
        "title": "ADA Retaliation Prohibition",
        "full_text": "No person shall discriminate against any individual because such individual has opposed any act or practice made unlawful by the ADA, or because such individual has filed a charge, testified, assisted, or participated in any investigation, proceeding, or hearing under the ADA. Retaliation and coercion are prohibited.",
        "domain": "civil_rights",
        "provision_type": "protection",
        "applies_when": _j({"disability": ["any"], "setting": ["employment", "public_accommodation", "government"]}),
        "enforcement_mechanisms": _j([
            "EEOC charge for employment retaliation",
            "DOJ complaint for public accommodation retaliation",
            "Private right of action in federal court",
            "Compensatory and punitive damages"
        ]),
        "source_url": "https://www.law.cornell.edu/uscode/text/42/12203",
        "cross_references": _j(["42 U.S.C. § 12112", "42 U.S.C. § 12132", "42 U.S.C. § 12182"])
    },
    {
        "citation": "28 CFR § 35.130(d)",
        "title": "ADA Most Integrated Setting Requirement",
        "full_text": "A public entity shall administer services, programs, and activities in the most integrated setting appropriate to the needs of qualified individuals with disabilities. The 'most integrated setting' is one that enables individuals with disabilities to interact with nondisabled persons to the fullest extent possible.",
        "domain": "civil_rights",
        "provision_type": "right",
        "applies_when": _j({"disability": ["any"], "setting": ["government", "public_program"]}),
        "enforcement_mechanisms": _j([
            "DOJ enforcement",
            "Private right of action under ADA Title II",
            "Federal court injunction"
        ]),
        "source_url": "https://www.ecfr.gov/current/title-28/chapter-I/part-35",
        "cross_references": _j(["42 U.S.C. § 12132", "Olmstead v. L.C., 527 U.S. 581 (1999)"])
    },
    {
        "citation": "42 U.S.C. § 12181(7)",
        "title": "ADA Definition of Public Accommodation",
        "full_text": "Public accommodations include private entities operating places such as hotels, restaurants, theaters, stores, health care providers' offices, museums, parks, schools, day care centers, homeless shelters, and social service center establishments. The definition is broad and covers most private businesses open to the public.",
        "domain": "civil_rights",
        "provision_type": "right",
        "applies_when": _j({"disability": ["any"], "setting": ["public_accommodation"]}),
        "enforcement_mechanisms": _j([
            "ADA Title III enforcement mechanisms",
            "DOJ complaint",
            "Private lawsuit for injunctive relief"
        ]),
        "source_url": "https://www.law.cornell.edu/uscode/text/42/12181",
        "cross_references": _j(["42 U.S.C. § 12182", "28 CFR Part 36"])
    },
    {
        "citation": "29 U.S.C. § 794d",
        "title": "Section 508 — Electronic and Information Technology Accessibility",
        "full_text": "Federal agencies must ensure that electronic and information technology is accessible to people with disabilities, including employees and members of the public. Applies to federal websites, software, telecommunications, and information kiosks.",
        "domain": "civil_rights",
        "provision_type": "right",
        "applies_when": _j({"disability": ["any"], "setting": ["federal_agency", "federal_website"]}),
        "enforcement_mechanisms": _j([
            "Administrative complaint to federal agency",
            "Private right of action under Section 504 standards",
            "GSA oversight and compliance monitoring"
        ]),
        "source_url": "https://www.law.cornell.edu/uscode/text/29/794d",
        "cross_references": _j(["29 U.S.C. § 794", "42 U.S.C. § 12132"])
    },
    {
        "citation": "42 U.S.C. § 12102",
        "title": "ADA Amendments Act — Broad Definition of Disability",
        "full_text": "The term 'disability' is to be construed broadly. It includes a physical or mental impairment that substantially limits one or more major life activities, a record of such an impairment, or being regarded as having such an impairment. Major life activities include caring for oneself, performing manual tasks, seeing, hearing, eating, sleeping, walking, standing, lifting, bending, speaking, breathing, learning, reading, concentrating, thinking, communicating, and working.",
        "domain": "civil_rights",
        "provision_type": "right",
        "applies_when": _j({"disability": ["any"]}),
        "enforcement_mechanisms": _j([
            "Enforcement through ADA Titles I, II, and III",
            "Section 504 proceedings"
        ]),
        "source_url": "https://www.law.cornell.edu/uscode/text/42/12102",
        "cross_references": _j(["42 U.S.C. § 12112", "42 U.S.C. § 12132", "42 U.S.C. § 12182"])
    },
    {
        "citation": "42 U.S.C. § 1981",
        "title": "Equal Rights Under the Law — Racial Discrimination in Contracts",
        "full_text": "All persons within the jurisdiction of the United States shall have the same right to make and enforce contracts, to sue, be parties, give evidence, and to the full and equal benefit of all laws as is enjoyed by white citizens. Applies to private as well as government discrimination and has no cap on damages.",
        "domain": "civil_rights",
        "provision_type": "protection",
        "applies_when": _j({"characteristic": ["race", "ethnicity"]}),
        "enforcement_mechanisms": _j([
            "Federal lawsuit — compensatory and punitive damages (no cap)",
            "No exhaustion of administrative remedies required",
            "Attorney's fees under 42 U.S.C. § 1988"
        ]),
        "source_url": "https://www.law.cornell.edu/uscode/text/42/1981",
        "cross_references": _j(["42 U.S.C. § 2000e-2", "42 U.S.C. § 1983"])
    },
    {
        "citation": "42 U.S.C. § 3617",
        "title": "Fair Housing Act — Interference and Retaliation",
        "full_text": "It is unlawful to coerce, intimidate, threaten, or interfere with any person in the exercise or enjoyment of rights granted under the Fair Housing Act. Prohibits retaliation against anyone who files a fair housing complaint, testifies, or assists in a fair housing investigation.",
        "domain": "civil_rights",
        "provision_type": "protection",
        "applies_when": _j({"setting": ["housing"]}),
        "enforcement_mechanisms": _j([
            "HUD complaint within one year",
            "Federal lawsuit within two years",
            "DOJ enforcement for pattern or practice",
            "State/local fair housing agency complaint"
        ]),
        "source_url": "https://www.law.cornell.edu/uscode/text/42/3617",
        "cross_references": _j(["42 U.S.C. § 3604", "42 U.S.C. § 3613"])
    },
    {
        "citation": "42 U.S.C. § 2000a",
        "title": "Title II Civil Rights Act of 1964 — Public Accommodations",
        "full_text": "All persons shall be entitled to the full and equal enjoyment of the goods, services, facilities, privileges, advantages, and accommodations of any place of public accommodation without discrimination on the ground of race, color, religion, or national origin.",
        "domain": "civil_rights",
        "provision_type": "protection",
        "applies_when": _j({"characteristic": ["race", "religion", "national_origin"], "setting": ["public_accommodation"]}),
        "enforcement_mechanisms": _j([
            "DOJ enforcement",
            "Private right of action for injunctive relief",
            "State civil rights agency complaint"
        ]),
        "source_url": "https://www.law.cornell.edu/uscode/text/42/2000a",
        "cross_references": _j(["42 U.S.C. § 2000e-2"])
    },
    {
        "citation": "42 U.S.C. § 1397dd",
        "title": "CHIP — Children's Health Insurance Program",
        "full_text": "States receive federal funds to provide health insurance coverage to uninsured children in families with incomes too high to qualify for Medicaid but unable to afford private coverage. CHIP covers routine check-ups, immunizations, doctor visits, prescriptions, dental and vision care, hospital care, and mental health services.",
        "domain": "civil_rights",
        "provision_type": "right",
        "applies_when": _j({"age": ["under_19"], "insurance": ["none"], "income_level": ["above_medicaid_below_chip"]}),
        "enforcement_mechanisms": _j([
            "State CHIP fair hearing",
            "CMS oversight",
            "42 U.S.C. § 1983 for eligible children wrongly denied"
        ]),
        "source_url": "https://www.law.cornell.edu/uscode/text/42/1397dd",
        "cross_references": _j(["42 U.S.C. § 1396d(r)"])
    },

    # =========================================================================
    # HOUSING DOMAIN (15+ provisions)
    # =========================================================================
    {
        "citation": "42 U.S.C. § 3604",
        "title": "Fair Housing Act — Discrimination in Sale or Rental",
        "full_text": "It is unlawful to refuse to sell or rent, or otherwise make unavailable, a dwelling to any person because of race, color, religion, sex, familial status, national origin, or disability. Includes refusal to make reasonable accommodations in rules, policies, practices, or services when necessary for a person with a disability to use a dwelling.",
        "domain": "housing",
        "provision_type": "protection",
        "applies_when": _j({"setting": ["housing", "rental", "home_purchase"]}),
        "enforcement_mechanisms": _j([
            "HUD complaint within one year",
            "Private lawsuit within two years under 42 U.S.C. § 3613",
            "DOJ enforcement for pattern or practice",
            "State/local fair housing agency complaint",
            "Actual and punitive damages, injunctive relief, attorney's fees"
        ]),
        "source_url": "https://www.law.cornell.edu/uscode/text/42/3604",
        "cross_references": _j(["42 U.S.C. § 3617", "42 U.S.C. § 3631", "24 CFR Part 100"])
    },
    {
        "citation": "42 U.S.C. § 3604(f)(3)(A)",
        "title": "Fair Housing Act — Reasonable Accommodations",
        "full_text": "It is discriminatory to refuse to make reasonable accommodations in rules, policies, practices, or services when such accommodations may be necessary to afford a person with a disability equal opportunity to use and enjoy a dwelling. Examples include allowing service animals despite no-pet policies, providing reserved accessible parking, and modifying lease terms.",
        "domain": "housing",
        "provision_type": "right",
        "applies_when": _j({"disability": ["any"], "setting": ["housing", "rental"]}),
        "enforcement_mechanisms": _j([
            "HUD complaint within one year",
            "Federal lawsuit within two years",
            "Compensatory and punitive damages",
            "Attorney's fees"
        ]),
        "source_url": "https://www.law.cornell.edu/uscode/text/42/3604",
        "cross_references": _j(["42 U.S.C. § 3604(f)(3)(B)", "24 CFR § 100.204"])
    },
    {
        "citation": "42 U.S.C. § 3604(f)(3)(B)",
        "title": "Fair Housing Act — Reasonable Modifications",
        "full_text": "It is discriminatory to refuse to permit a person with a disability to make reasonable modifications to existing premises at the person's expense, when such modifications are necessary to afford full enjoyment of the premises. In rental housing, the landlord may require restoration at tenant's expense.",
        "domain": "housing",
        "provision_type": "right",
        "applies_when": _j({"disability": ["any"], "setting": ["housing", "rental"]}),
        "enforcement_mechanisms": _j([
            "HUD complaint",
            "Federal lawsuit",
            "State fair housing agency"
        ]),
        "source_url": "https://www.law.cornell.edu/uscode/text/42/3604",
        "cross_references": _j(["42 U.S.C. § 3604(f)(3)(A)", "24 CFR § 100.203"])
    },
    {
        "citation": "42 U.S.C. § 1437f",
        "title": "Section 8 Housing Choice Voucher Program",
        "full_text": "The Housing Choice Voucher program provides rental assistance to low-income families, the elderly, and persons with disabilities. Participants choose housing in the private market. The housing authority pays a subsidy directly to the landlord, and the tenant pays the difference between the actual rent and the subsidy (generally 30% of adjusted income).",
        "domain": "housing",
        "provision_type": "right",
        "applies_when": _j({"income_level": ["below_50_ami", "below_30_ami"], "housing": ["rental"]}),
        "enforcement_mechanisms": _j([
            "Housing authority informal hearing under 24 CFR § 982.555",
            "HUD complaint for PHA violations",
            "Federal lawsuit for due process violations",
            "Fair housing complaint if discriminatory denial"
        ]),
        "source_url": "https://www.law.cornell.edu/uscode/text/42/1437f",
        "cross_references": _j(["24 CFR Part 982", "42 U.S.C. § 1437a"])
    },
    {
        "citation": "34 U.S.C. § 12491",
        "title": "VAWA Housing Protections",
        "full_text": "Victims of domestic violence, dating violence, sexual assault, or stalking who are tenants or applicants for federally assisted housing cannot be denied admission, evicted, or have assistance terminated solely on the basis of being a victim. Applies to public housing, Section 8, LIHTC, and other HUD-assisted programs. Victims may request emergency transfers.",
        "domain": "housing",
        "provision_type": "protection",
        "applies_when": _j({"background": ["domestic_violence_survivor", "sexual_assault_survivor"], "housing": ["public_housing", "section_8", "federally_assisted"]}),
        "enforcement_mechanisms": _j([
            "Housing authority grievance/hearing process",
            "HUD complaint",
            "VAWA self-certification to housing provider",
            "Emergency transfer request",
            "Federal lawsuit for violations"
        ]),
        "source_url": "https://www.law.cornell.edu/uscode/text/34/12491",
        "cross_references": _j(["42 U.S.C. § 1437f", "42 U.S.C. § 1437d"])
    },
    {
        "citation": "42 U.S.C. § 11431",
        "title": "McKinney-Vento Homeless Assistance Act — Education Rights",
        "full_text": "Children and youth experiencing homelessness have the right to immediate enrollment in school, remain in the school of origin, receive transportation to the school of origin, and participate fully in school activities. The Act defines 'homeless' broadly to include doubled-up families, those in shelters, motels, cars, and unaccompanied youth.",
        "domain": "housing",
        "provision_type": "right",
        "applies_when": _j({"housing": ["homeless", "shelter", "doubled_up", "motel"], "age": ["school_age"]}),
        "enforcement_mechanisms": _j([
            "School district homeless liaison",
            "State coordinator for homeless education",
            "Dispute resolution process under 42 U.S.C. § 11432(g)(3)(E)",
            "Federal lawsuit"
        ]),
        "source_url": "https://www.law.cornell.edu/uscode/text/42/11431",
        "cross_references": _j(["20 U.S.C. § 1400", "42 U.S.C. § 11302"])
    },
    {
        "citation": "42 U.S.C. § 1437d(l)(6)",
        "title": "Public Housing One-Strike Eviction Protections",
        "full_text": "While PHAs may evict tenants for drug-related or violent criminal activity, courts have interpreted this provision to require consideration of the seriousness of the offense, the extent of participation by the tenant, and the effects the eviction would have on non-offending family members. Due process protections apply.",
        "domain": "housing",
        "provision_type": "protection",
        "applies_when": _j({"housing": ["public_housing"], "background": ["criminal_record"]}),
        "enforcement_mechanisms": _j([
            "PHA grievance hearing under 24 CFR Part 966",
            "State court eviction defense",
            "Legal aid representation",
            "Due process challenge in federal court"
        ]),
        "source_url": "https://www.law.cornell.edu/uscode/text/42/1437d",
        "cross_references": _j(["42 U.S.C. § 1437f", "24 CFR § 966.4"])
    },
    {
        "citation": "24 CFR § 5.2005(b)",
        "title": "HUD Prohibition on Denial Based on Domestic Violence Status",
        "full_text": "An applicant for federally assisted housing may not be denied admission on the basis of being or having been a victim of domestic violence, dating violence, sexual assault, or stalking. Incidents of domestic violence do not constitute serious or repeated lease violations by the victim.",
        "domain": "housing",
        "provision_type": "protection",
        "applies_when": _j({"background": ["domestic_violence_survivor"], "housing": ["public_housing", "section_8", "federally_assisted"]}),
        "enforcement_mechanisms": _j([
            "HUD complaint",
            "Housing authority hearing",
            "VAWA self-certification",
            "Federal lawsuit"
        ]),
        "source_url": "https://www.ecfr.gov/current/title-24/subtitle-A/part-5/subpart-L",
        "cross_references": _j(["34 U.S.C. § 12491", "42 U.S.C. § 1437d"])
    },
    {
        "citation": "42 U.S.C. § 3604(e)",
        "title": "Fair Housing Act — Familial Status Protection",
        "full_text": "It is unlawful to discriminate in the sale or rental of housing based on familial status — defined as having one or more children under 18 in the household, being pregnant, or being in the process of securing legal custody. Applies to all housing except qualifying senior housing (55+ or 62+).",
        "domain": "housing",
        "provision_type": "protection",
        "applies_when": _j({"household": ["children_under_18", "pregnant"], "setting": ["housing", "rental"]}),
        "enforcement_mechanisms": _j([
            "HUD complaint within one year",
            "Federal lawsuit within two years",
            "State/local fair housing agency",
            "Compensatory and punitive damages"
        ]),
        "source_url": "https://www.law.cornell.edu/uscode/text/42/3604",
        "cross_references": _j(["42 U.S.C. § 3607(b)", "24 CFR Part 100"])
    },
    {
        "citation": "42 U.S.C. § 11302",
        "title": "Definition of Homeless Individual",
        "full_text": "An individual or family is considered homeless if they lack a fixed, regular, and adequate nighttime residence, including those living in shelters, transitional housing, places not designed for human habitation, or fleeing domestic violence. Also includes individuals at imminent risk of losing housing within 14 days.",
        "domain": "housing",
        "provision_type": "right",
        "applies_when": _j({"housing": ["homeless", "shelter", "transitional", "fleeing_violence"]}),
        "enforcement_mechanisms": _j([
            "HUD Continuum of Care program requirements",
            "McKinney-Vento education rights",
            "Healthcare for the Homeless program access"
        ]),
        "source_url": "https://www.law.cornell.edu/uscode/text/42/11302",
        "cross_references": _j(["42 U.S.C. § 11431", "42 U.S.C. § 254b"])
    },
    {
        "citation": "42 U.S.C. § 1437a(a)",
        "title": "Public Housing Rent Calculation — 30% Income Cap",
        "full_text": "Families in public housing pay rent based on the highest of: 30% of monthly adjusted income, 10% of monthly income, the welfare rent, or a minimum rent (not exceeding $50). Income exclusions apply for earned income of certain individuals, including persons with disabilities returning to work.",
        "domain": "housing",
        "provision_type": "right",
        "applies_when": _j({"housing": ["public_housing"], "income_level": ["low_income"]}),
        "enforcement_mechanisms": _j([
            "PHA grievance procedure",
            "HUD complaint",
            "Federal lawsuit for incorrect rent calculation"
        ]),
        "source_url": "https://www.law.cornell.edu/uscode/text/42/1437a",
        "cross_references": _j(["24 CFR Part 5", "42 U.S.C. § 1437f"])
    },
    {
        "citation": "42 U.S.C. § 3608(d)",
        "title": "Affirmatively Furthering Fair Housing (AFFH)",
        "full_text": "All executive departments and agencies shall administer their programs and activities relating to housing and urban development in a manner that affirmatively furthers the purposes of the Fair Housing Act. HUD grantees must take meaningful actions to overcome patterns of segregation and promote inclusive communities.",
        "domain": "housing",
        "provision_type": "obligation",
        "applies_when": _j({"setting": ["housing", "community_development"]}),
        "enforcement_mechanisms": _j([
            "HUD review of grantee compliance",
            "Federal lawsuit for failure to AFFH",
            "Administrative complaint to HUD",
            "Community challenge to HUD funding decisions"
        ]),
        "source_url": "https://www.law.cornell.edu/uscode/text/42/3608",
        "cross_references": _j(["42 U.S.C. § 3604", "42 U.S.C. § 5301"])
    },
    {
        "citation": "42 U.S.C. § 3613(a)",
        "title": "Fair Housing Act — Private Enforcement",
        "full_text": "An aggrieved person may commence a civil action in federal or state court within two years after the occurrence or termination of the discriminatory housing practice. The court may award actual and punitive damages, injunctive relief, and reasonable attorney's fees.",
        "domain": "housing",
        "provision_type": "enforcement",
        "applies_when": _j({"setting": ["housing"]}),
        "enforcement_mechanisms": _j([
            "Federal or state court lawsuit within 2 years",
            "Actual and punitive damages",
            "Injunctive relief",
            "Attorney's fees and costs"
        ]),
        "source_url": "https://www.law.cornell.edu/uscode/text/42/3613",
        "cross_references": _j(["42 U.S.C. § 3604", "42 U.S.C. § 3610", "42 U.S.C. § 3612"])
    },
    {
        "citation": "24 CFR § 100.204",
        "title": "Reasonable Accommodation Requirements in Housing",
        "full_text": "A refusal to make reasonable accommodations in rules, policies, practices, or services, when such accommodations may be necessary to afford a person with a disability equal opportunity to use and enjoy a dwelling, constitutes unlawful discrimination. The accommodation must be related to the disability and not impose an undue financial or administrative burden.",
        "domain": "housing",
        "provision_type": "right",
        "applies_when": _j({"disability": ["any"], "setting": ["housing", "rental"]}),
        "enforcement_mechanisms": _j([
            "HUD complaint",
            "Federal lawsuit",
            "State/local fair housing enforcement"
        ]),
        "source_url": "https://www.ecfr.gov/current/title-24/subtitle-B/chapter-I/subchapter-A/part-100",
        "cross_references": _j(["42 U.S.C. § 3604(f)(3)(A)", "42 U.S.C. § 3604(f)(3)(B)"])
    },
    {
        "citation": "42 U.S.C. § 1437f(o)(20)",
        "title": "Section 8 Voucher Portability",
        "full_text": "Families with Section 8 vouchers may use their voucher in any jurisdiction where a PHA administers the voucher program. The initial PHA must allow the family to move with continued assistance. This enables mobility and access to areas of opportunity.",
        "domain": "housing",
        "provision_type": "right",
        "applies_when": _j({"housing": ["section_8"], "action": ["relocation"]}),
        "enforcement_mechanisms": _j([
            "PHA informal hearing",
            "HUD complaint for refusal of portability",
            "Federal lawsuit"
        ]),
        "source_url": "https://www.law.cornell.edu/uscode/text/42/1437f",
        "cross_references": _j(["24 CFR § 982.353", "42 U.S.C. § 1437f"])
    },

    # =========================================================================
    # INCOME DOMAIN (15+ provisions)
    # =========================================================================
    {
        "citation": "42 U.S.C. § 1382",
        "title": "SSI — Supplemental Security Income Eligibility",
        "full_text": "Aged, blind, or disabled individuals with limited income and resources are eligible for SSI cash assistance. The 2024 federal benefit rate is $943/month for individuals and $1,415/month for couples. Resources must be below $2,000 (individual) or $3,000 (couple). Many states supplement the federal payment.",
        "domain": "income",
        "provision_type": "right",
        "applies_when": _j({"disability": ["any"], "age": ["65_or_older", "any"], "income_level": ["below_ssi_limit"], "resources": ["below_2000_individual", "below_3000_couple"]}),
        "enforcement_mechanisms": _j([
            "SSA reconsideration",
            "ALJ hearing",
            "Appeals Council review",
            "Federal court review under 42 U.S.C. § 405(g)",
            "Legal aid assistance"
        ]),
        "source_url": "https://www.law.cornell.edu/uscode/text/42/1382",
        "cross_references": _j(["42 U.S.C. § 1382a", "42 U.S.C. § 1382b", "20 CFR Part 416"])
    },
    {
        "citation": "42 U.S.C. § 423",
        "title": "SSDI — Social Security Disability Insurance",
        "full_text": "Workers who have paid Social Security taxes and become disabled before retirement age are entitled to disability insurance benefits. Disability means inability to engage in any substantial gainful activity by reason of a medically determinable impairment expected to last at least 12 months or result in death. Benefits are based on the worker's earnings record.",
        "domain": "income",
        "provision_type": "right",
        "applies_when": _j({"disability": ["any"], "work_history": ["sufficient_work_credits"]}),
        "enforcement_mechanisms": _j([
            "SSA reconsideration",
            "ALJ hearing under 20 CFR Part 404",
            "Appeals Council review",
            "Federal court review under 42 U.S.C. § 405(g)"
        ]),
        "source_url": "https://www.law.cornell.edu/uscode/text/42/423",
        "cross_references": _j(["42 U.S.C. § 405(g)", "20 CFR Part 404"])
    },
    {
        "citation": "7 U.S.C. § 2011",
        "title": "SNAP — Supplemental Nutrition Assistance Program",
        "full_text": "SNAP provides food assistance to low-income individuals and families. Eligibility is generally based on gross income at or below 130% FPL and net income at or below 100% FPL. Benefits are delivered via EBT card and can be used to purchase food at authorized retailers. Most able-bodied adults without dependents face work requirements.",
        "domain": "income",
        "provision_type": "right",
        "applies_when": _j({"income_level": ["below_130_fpl"]}),
        "enforcement_mechanisms": _j([
            "State agency fair hearing within 90 days",
            "Federal court review",
            "USDA Food and Nutrition Service complaint",
            "Legal aid assistance"
        ]),
        "source_url": "https://www.law.cornell.edu/uscode/text/7/2011",
        "cross_references": _j(["7 U.S.C. § 2014", "7 CFR Part 273"])
    },
    {
        "citation": "42 U.S.C. § 601",
        "title": "TANF — Temporary Assistance for Needy Families",
        "full_text": "TANF provides cash assistance and work support to low-income families with children. States receive block grants and have wide flexibility in program design. Federal law imposes a 60-month lifetime limit on assistance and work participation requirements. States may exempt certain individuals from time limits and work requirements.",
        "domain": "income",
        "provision_type": "right",
        "applies_when": _j({"household": ["children_under_18"], "income_level": ["low_income"]}),
        "enforcement_mechanisms": _j([
            "State agency fair hearing",
            "State court review",
            "42 U.S.C. § 1983 for procedural due process violations"
        ]),
        "source_url": "https://www.law.cornell.edu/uscode/text/42/601",
        "cross_references": _j(["42 U.S.C. § 607", "42 U.S.C. § 608"])
    },
    {
        "citation": "26 U.S.C. § 32",
        "title": "Earned Income Tax Credit (EITC)",
        "full_text": "The EITC provides a refundable tax credit to low- and moderate-income workers. The credit amount varies based on filing status, number of qualifying children, and earned income. For 2024, the maximum credit ranges from $632 (no children) to $7,830 (three or more children). The credit phases in with earned income and phases out at higher income levels.",
        "domain": "income",
        "provision_type": "right",
        "applies_when": _j({"income_level": ["low_to_moderate"], "employment": ["employed", "self_employed"]}),
        "enforcement_mechanisms": _j([
            "IRS audit and reconsideration",
            "Tax Court petition",
            "Low Income Taxpayer Clinic assistance",
            "Taxpayer Advocate Service"
        ]),
        "source_url": "https://www.law.cornell.edu/uscode/text/26/32",
        "cross_references": _j(["26 U.S.C. § 24", "26 U.S.C. § 152"])
    },
    {
        "citation": "26 U.S.C. § 24",
        "title": "Child Tax Credit",
        "full_text": "Taxpayers may claim a tax credit of up to $2,000 per qualifying child under 17. Up to $1,700 of the credit is refundable as the Additional Child Tax Credit for taxpayers with earned income. The credit phases out at higher income levels ($200,000 single, $400,000 married filing jointly).",
        "domain": "income",
        "provision_type": "right",
        "applies_when": _j({"household": ["children_under_17"], "income_level": ["any"]}),
        "enforcement_mechanisms": _j([
            "IRS audit and reconsideration",
            "Tax Court petition",
            "Low Income Taxpayer Clinic"
        ]),
        "source_url": "https://www.law.cornell.edu/uscode/text/26/24",
        "cross_references": _j(["26 U.S.C. § 32", "26 U.S.C. § 152"])
    },
    {
        "citation": "42 U.S.C. § 1382a",
        "title": "SSI Income Exclusions and Work Incentives",
        "full_text": "SSI excludes certain income from the benefit calculation, including the first $20 of unearned income, the first $65 of earned income plus half the remainder, impairment-related work expenses, PASS (Plan to Achieve Self-Support) income, and student earned income. These exclusions encourage work while maintaining benefits.",
        "domain": "income",
        "provision_type": "right",
        "applies_when": _j({"benefits": ["ssi"], "employment": ["employed", "seeking_employment"]}),
        "enforcement_mechanisms": _j([
            "SSA reconsideration",
            "ALJ hearing",
            "Protection and advocacy organization assistance"
        ]),
        "source_url": "https://www.law.cornell.edu/uscode/text/42/1382a",
        "cross_references": _j(["42 U.S.C. § 1382", "20 CFR § 416.1112"])
    },
    {
        "citation": "42 U.S.C. § 1382h",
        "title": "Section 1619(b) — Medicaid While Working",
        "full_text": "SSI recipients who work and earn above the substantial gainful activity level may continue to receive Medicaid coverage if they still have the original disabling condition, are unable to afford equivalent private health insurance, and need Medicaid to continue working. This eliminates the 'benefits cliff' that discourages employment.",
        "domain": "income",
        "provision_type": "right",
        "applies_when": _j({"benefits": ["ssi"], "employment": ["employed"], "disability": ["any"]}),
        "enforcement_mechanisms": _j([
            "SSA reconsideration and appeal",
            "Ticket to Work program protections",
            "Benefits counseling through WIPA programs"
        ]),
        "source_url": "https://www.law.cornell.edu/uscode/text/42/1382h",
        "cross_references": _j(["42 U.S.C. § 1382", "42 U.S.C. § 1396a"])
    },
    {
        "citation": "29 U.S.C. § 206(a)",
        "title": "Federal Minimum Wage",
        "full_text": "Every employer shall pay to each of their employees a minimum wage of not less than $7.25 per hour. Many states and localities have higher minimum wages. Tipped employees may be paid $2.13/hour if tips bring total to minimum wage. Employers must make up any shortfall.",
        "domain": "income",
        "provision_type": "right",
        "applies_when": _j({"employment": ["employed"], "setting": ["employment"]}),
        "enforcement_mechanisms": _j([
            "DOL Wage and Hour Division complaint",
            "Private lawsuit under 29 U.S.C. § 216(b)",
            "Back wages plus equal amount in liquidated damages",
            "State labor department complaint"
        ]),
        "source_url": "https://www.law.cornell.edu/uscode/text/29/206",
        "cross_references": _j(["29 U.S.C. § 207", "29 U.S.C. § 213"])
    },
    {
        "citation": "29 U.S.C. § 207",
        "title": "FLSA Overtime Pay Requirements",
        "full_text": "Non-exempt employees must receive overtime pay at a rate of not less than one and one-half times their regular rate of pay for all hours worked over 40 in a workweek. Certain employees are exempt based on salary level and duties (executive, administrative, professional, outside sales, computer employees).",
        "domain": "income",
        "provision_type": "right",
        "applies_when": _j({"employment": ["employed", "non_exempt"]}),
        "enforcement_mechanisms": _j([
            "DOL Wage and Hour Division complaint",
            "Private lawsuit under 29 U.S.C. § 216(b)",
            "Back wages and liquidated damages",
            "State labor department complaint"
        ]),
        "source_url": "https://www.law.cornell.edu/uscode/text/29/207",
        "cross_references": _j(["29 U.S.C. § 206", "29 U.S.C. § 213"])
    },
    {
        "citation": "42 U.S.C. § 402(d)",
        "title": "Social Security Childhood Disability Benefits (DAC)",
        "full_text": "Disabled adult children may receive Social Security benefits based on a parent's earnings record if the disability began before age 22 and the parent is receiving Social Security retirement or disability benefits, or is deceased. Benefits continue as long as the individual remains disabled.",
        "domain": "income",
        "provision_type": "right",
        "applies_when": _j({"disability": ["any"], "age": ["onset_before_22"], "parent_status": ["parent_receiving_ss", "parent_deceased"]}),
        "enforcement_mechanisms": _j([
            "SSA reconsideration and ALJ hearing",
            "Appeals Council review",
            "Federal court review"
        ]),
        "source_url": "https://www.law.cornell.edu/uscode/text/42/402",
        "cross_references": _j(["42 U.S.C. § 423", "42 U.S.C. § 426"])
    },
    {
        "citation": "42 U.S.C. § 1396a(a)(17)",
        "title": "Medicaid Spend-Down — Medically Needy Program",
        "full_text": "States may offer Medicaid coverage to medically needy individuals whose income exceeds eligibility limits but who incur medical expenses that reduce their income below the medically needy income level. The 'spend-down' allows individuals to qualify by deducting medical expenses from countable income.",
        "domain": "income",
        "provision_type": "right",
        "applies_when": _j({"income_level": ["above_medicaid_limit"], "medical_expenses": ["high"]}),
        "enforcement_mechanisms": _j([
            "State Medicaid fair hearing",
            "42 U.S.C. § 1983"
        ]),
        "source_url": "https://www.law.cornell.edu/uscode/text/42/1396a",
        "cross_references": _j(["42 U.S.C. § 1396d(a)"])
    },
    {
        "citation": "42 U.S.C. § 1382b",
        "title": "SSI Resource Exclusions",
        "full_text": "Certain resources are excluded from SSI resource limits: the home and surrounding land, one automobile, life insurance with face value up to $1,500, burial funds up to $1,500, property needed for self-support, and retroactive SSI/SSDI payments for 9 months after receipt.",
        "domain": "income",
        "provision_type": "right",
        "applies_when": _j({"benefits": ["ssi"]}),
        "enforcement_mechanisms": _j([
            "SSA reconsideration",
            "ALJ hearing",
            "Federal court review"
        ]),
        "source_url": "https://www.law.cornell.edu/uscode/text/42/1382b",
        "cross_references": _j(["42 U.S.C. § 1382", "20 CFR § 416.1210"])
    },
    {
        "citation": "29 U.S.C. § 2612",
        "title": "FMLA — Family and Medical Leave",
        "full_text": "Eligible employees of covered employers are entitled to 12 weeks of unpaid, job-protected leave per year for the birth or adoption of a child, to care for a seriously ill family member, or for the employee's own serious health condition. Employer must maintain group health insurance during leave.",
        "domain": "income",
        "provision_type": "right",
        "applies_when": _j({"employment": ["employed"], "employer_size": ["50_or_more"], "tenure": ["12_months_plus"]}),
        "enforcement_mechanisms": _j([
            "DOL Wage and Hour Division complaint",
            "Private lawsuit in federal or state court",
            "Back pay, benefits, and liquidated damages",
            "Reinstatement to same or equivalent position"
        ]),
        "source_url": "https://www.law.cornell.edu/uscode/text/29/2612",
        "cross_references": _j(["29 CFR Part 825"])
    },
    {
        "citation": "42 U.S.C. § 1395w-114",
        "title": "Medicare Part D Low-Income Subsidy (Extra Help)",
        "full_text": "Medicare beneficiaries with limited income and resources may qualify for the Low-Income Subsidy (Extra Help), which pays part or all of Medicare prescription drug plan premiums, deductibles, and copayments. Full subsidy available for those with income below 135% FPL and limited resources.",
        "domain": "income",
        "provision_type": "right",
        "applies_when": _j({"insurance": ["medicare"], "income_level": ["below_150_fpl"]}),
        "enforcement_mechanisms": _j([
            "SSA redetermination",
            "Medicare appeal process",
            "State Health Insurance Assistance Program (SHIP) counseling"
        ]),
        "source_url": "https://www.law.cornell.edu/uscode/text/42/1395w-114",
        "cross_references": _j(["42 U.S.C. § 1395w-101"])
    },

    # =========================================================================
    # EDUCATION DOMAIN (10+ provisions)
    # =========================================================================
    {
        "citation": "20 U.S.C. § 1400",
        "title": "IDEA — Individuals with Disabilities Education Act",
        "full_text": "Children with disabilities ages 3-21 are entitled to a free appropriate public education (FAPE) in the least restrictive environment. Schools must develop an Individualized Education Program (IEP) for each eligible child. IDEA covers 13 disability categories and requires related services such as speech therapy, occupational therapy, counseling, and transportation.",
        "domain": "education",
        "provision_type": "right",
        "applies_when": _j({"disability": ["any"], "age": ["3_to_21"], "setting": ["school"]}),
        "enforcement_mechanisms": _j([
            "IEP dispute resolution — mediation under 20 U.S.C. § 1415(e)",
            "Due process hearing under 20 U.S.C. § 1415(f)",
            "State complaint to state education agency",
            "Federal court appeal of due process decision",
            "OCR complaint for disability discrimination"
        ]),
        "source_url": "https://www.law.cornell.edu/uscode/text/20/1400",
        "cross_references": _j(["20 U.S.C. § 1412", "20 U.S.C. § 1414", "20 U.S.C. § 1415", "34 CFR Part 300"])
    },
    {
        "citation": "20 U.S.C. § 1412(a)(5)",
        "title": "IDEA — Least Restrictive Environment (LRE)",
        "full_text": "To the maximum extent appropriate, children with disabilities must be educated with children who are not disabled. Removal from the regular educational environment may occur only when the nature or severity of the disability is such that education in regular classes with the use of supplementary aids and services cannot be achieved satisfactorily.",
        "domain": "education",
        "provision_type": "right",
        "applies_when": _j({"disability": ["any"], "age": ["3_to_21"], "setting": ["school"]}),
        "enforcement_mechanisms": _j([
            "IEP team dispute",
            "Due process hearing",
            "State complaint",
            "OCR complaint"
        ]),
        "source_url": "https://www.law.cornell.edu/uscode/text/20/1412",
        "cross_references": _j(["20 U.S.C. § 1400", "34 CFR § 300.114"])
    },
    {
        "citation": "20 U.S.C. § 1415(k)",
        "title": "IDEA Discipline Protections — Manifestation Determination",
        "full_text": "When a child with a disability is subject to a disciplinary change of placement (suspension over 10 days), the school must conduct a manifestation determination review within 10 school days. If the behavior was caused by or substantially related to the disability, or was a direct result of failure to implement the IEP, the child must be returned to placement. The school may not suspend or expel a child for disability-related behavior.",
        "domain": "education",
        "provision_type": "protection",
        "applies_when": _j({"disability": ["any"], "age": ["school_age"], "setting": ["school"], "situation": ["discipline", "suspension", "expulsion"]}),
        "enforcement_mechanisms": _j([
            "Expedited due process hearing under 20 U.S.C. § 1415(k)(3)",
            "State complaint",
            "OCR complaint",
            "Federal court injunction"
        ]),
        "source_url": "https://www.law.cornell.edu/uscode/text/20/1415",
        "cross_references": _j(["20 U.S.C. § 1400", "34 CFR § 300.530"])
    },
    {
        "citation": "34 CFR Part 104",
        "title": "Section 504 in Schools — Disability Accommodation",
        "full_text": "Public schools receiving federal financial assistance must provide a free appropriate public education to each qualified student with a disability. Section 504 plans provide accommodations such as extended test time, preferential seating, modified assignments, behavioral supports, and health-related accommodations. The definition of disability is broader than IDEA.",
        "domain": "education",
        "provision_type": "right",
        "applies_when": _j({"disability": ["any"], "setting": ["school"], "age": ["school_age"]}),
        "enforcement_mechanisms": _j([
            "OCR complaint within 180 days",
            "Section 504 hearing under 34 CFR § 104.36",
            "Private right of action in federal court",
            "Compensatory damages available"
        ]),
        "source_url": "https://www.ecfr.gov/current/title-34/subtitle-B/chapter-I/part-104",
        "cross_references": _j(["29 U.S.C. § 794", "20 U.S.C. § 1400"])
    },
    {
        "citation": "20 U.S.C. § 1681",
        "title": "Title IX — Sex Discrimination in Education",
        "full_text": "No person in the United States shall, on the basis of sex, be excluded from participation in, be denied the benefits of, or be subjected to discrimination under any education program or activity receiving Federal financial assistance. Covers admissions, athletics, sexual harassment, sexual assault, and pregnancy discrimination in schools.",
        "domain": "education",
        "provision_type": "protection",
        "applies_when": _j({"setting": ["school", "university"], "characteristic": ["sex", "gender"]}),
        "enforcement_mechanisms": _j([
            "OCR complaint within 180 days",
            "School's Title IX grievance procedures",
            "Private right of action in federal court — damages available",
            "Administrative enforcement — fund termination"
        ]),
        "source_url": "https://www.law.cornell.edu/uscode/text/20/1681",
        "cross_references": _j(["34 CFR Part 106"])
    },
    {
        "citation": "20 U.S.C. § 1232g",
        "title": "FERPA — Family Educational Rights and Privacy Act",
        "full_text": "Parents and eligible students (18+) have the right to inspect and review education records, request amendments, consent to disclosures of personally identifiable information, and file complaints with the Department of Education. Schools may not disclose education records without consent except in limited circumstances.",
        "domain": "education",
        "provision_type": "protection",
        "applies_when": _j({"setting": ["school", "university"], "age": ["school_age", "adult_student"]}),
        "enforcement_mechanisms": _j([
            "Complaint to Family Policy Compliance Office, U.S. Department of Education",
            "No private right of action (Gonzaga University v. Doe, 536 U.S. 273)",
            "Administrative enforcement — potential loss of federal funds"
        ]),
        "source_url": "https://www.law.cornell.edu/uscode/text/20/1232g",
        "cross_references": _j(["34 CFR Part 99"])
    },
    {
        "citation": "42 U.S.C. § 11432(g)(3)(C)",
        "title": "McKinney-Vento — Immediate Enrollment for Homeless Students",
        "full_text": "Homeless children and youth must be immediately enrolled in school, even if they lack normally required documents such as previous school records, immunization records, proof of residency, birth certificate, or other documentation. The enrolling school must immediately contact the prior school to obtain records.",
        "domain": "education",
        "provision_type": "right",
        "applies_when": _j({"housing": ["homeless", "shelter", "doubled_up"], "age": ["school_age"]}),
        "enforcement_mechanisms": _j([
            "School district homeless liaison",
            "State coordinator complaint",
            "McKinney-Vento dispute resolution"
        ]),
        "source_url": "https://www.law.cornell.edu/uscode/text/42/11432",
        "cross_references": _j(["42 U.S.C. § 11431", "42 U.S.C. § 11302"])
    },
    {
        "citation": "20 U.S.C. § 1414(d)",
        "title": "IDEA — Individualized Education Program (IEP) Requirements",
        "full_text": "Each child's IEP must include: a statement of present levels of performance, measurable annual goals, a description of services and supports, participation in state assessments, transition planning beginning at age 16, and a statement of how the child's progress will be measured and reported to parents.",
        "domain": "education",
        "provision_type": "right",
        "applies_when": _j({"disability": ["any"], "age": ["3_to_21"], "setting": ["school"]}),
        "enforcement_mechanisms": _j([
            "IEP team meeting",
            "Mediation",
            "Due process hearing",
            "State complaint"
        ]),
        "source_url": "https://www.law.cornell.edu/uscode/text/20/1414",
        "cross_references": _j(["20 U.S.C. § 1400", "20 U.S.C. § 1415", "34 CFR § 300.320"])
    },
    {
        "citation": "20 U.S.C. § 1415(b)(6)",
        "title": "IDEA — Due Process Hearing Rights",
        "full_text": "Parents or the school district may file a due process complaint on any matter relating to the identification, evaluation, educational placement, or provision of FAPE. An impartial hearing officer conducts the hearing and issues a decision. The losing party may appeal to state or federal court.",
        "domain": "education",
        "provision_type": "enforcement",
        "applies_when": _j({"disability": ["any"], "setting": ["school"], "situation": ["iep_dispute", "fape_denial"]}),
        "enforcement_mechanisms": _j([
            "Due process hearing before impartial hearing officer",
            "Appeal to state court or federal court",
            "Attorney's fees for prevailing parents under 20 U.S.C. § 1415(i)(3)",
            "Compensatory education remedy"
        ]),
        "source_url": "https://www.law.cornell.edu/uscode/text/20/1415",
        "cross_references": _j(["20 U.S.C. § 1400", "20 U.S.C. § 1414"])
    },
    {
        "citation": "20 U.S.C. § 1414(b)",
        "title": "IDEA — Child Find and Evaluation Requirements",
        "full_text": "States must have policies and procedures to ensure that all children with disabilities are identified, located, and evaluated. The initial evaluation must be completed within 60 days. The evaluation must use a variety of assessment tools and strategies, be administered by trained personnel, and assess all areas of suspected disability.",
        "domain": "education",
        "provision_type": "obligation",
        "applies_when": _j({"disability": ["suspected"], "age": ["birth_to_21"], "setting": ["school"]}),
        "enforcement_mechanisms": _j([
            "State complaint for Child Find failure",
            "Due process hearing",
            "OCR complaint",
            "Compensatory education for delay in identification"
        ]),
        "source_url": "https://www.law.cornell.edu/uscode/text/20/1414",
        "cross_references": _j(["20 U.S.C. § 1412(a)(3)", "34 CFR § 300.301"])
    },
    {
        "citation": "20 U.S.C. § 1431",
        "title": "IDEA Part C — Early Intervention for Infants and Toddlers",
        "full_text": "Infants and toddlers (birth through age 2) with developmental delays or established conditions are entitled to early intervention services. Services are provided through an Individualized Family Service Plan (IFSP) and may include speech therapy, physical therapy, occupational therapy, special instruction, and family training.",
        "domain": "education",
        "provision_type": "right",
        "applies_when": _j({"disability": ["developmental_delay"], "age": ["birth_to_2"]}),
        "enforcement_mechanisms": _j([
            "IFSP dispute resolution",
            "State complaint",
            "Due process hearing",
            "Mediation"
        ]),
        "source_url": "https://www.law.cornell.edu/uscode/text/20/1431",
        "cross_references": _j(["20 U.S.C. § 1400", "34 CFR Part 303"])
    },

    # =========================================================================
    # JUSTICE DOMAIN (10+ provisions)
    # =========================================================================
    {
        "citation": "U.S. Const. amend. VI",
        "title": "Sixth Amendment — Right to Counsel",
        "full_text": "In all criminal prosecutions, the accused shall enjoy the right to have the assistance of counsel for his defense. Under Gideon v. Wainwright, 372 U.S. 335 (1963), this right requires states to provide counsel to defendants who cannot afford an attorney in felony cases. Extended to misdemeanors resulting in imprisonment by Argersinger v. Hamlin, 407 U.S. 25 (1972).",
        "domain": "justice",
        "provision_type": "right",
        "applies_when": _j({"setting": ["criminal_court"], "situation": ["criminal_charges"], "income_level": ["cannot_afford_attorney"]}),
        "enforcement_mechanisms": _j([
            "Motion to appoint counsel in criminal proceedings",
            "Ineffective assistance of counsel claim (Strickland v. Washington)",
            "Habeas corpus petition under 28 U.S.C. § 2254",
            "Appeal of conviction"
        ]),
        "source_url": "https://www.law.cornell.edu/constitution/sixth_amendment",
        "cross_references": _j(["Gideon v. Wainwright, 372 U.S. 335 (1963)", "18 U.S.C. § 3006A"])
    },
    {
        "citation": "18 U.S.C. § 3142",
        "title": "Bail Reform Act — Pretrial Release and Detention",
        "full_text": "The judicial officer shall order pretrial release on personal recognizance or unsecured bond unless the officer determines that such release will not reasonably assure the appearance of the person or the safety of any person or the community. The least restrictive conditions must be imposed. Detention hearing required for rebuttable presumption offenses.",
        "domain": "justice",
        "provision_type": "right",
        "applies_when": _j({"setting": ["criminal_court", "federal_court"], "situation": ["pretrial", "arrest"]}),
        "enforcement_mechanisms": _j([
            "Motion for pretrial release under 18 U.S.C. § 3142",
            "Appeal of detention order to district court or circuit court",
            "Habeas corpus petition"
        ]),
        "source_url": "https://www.law.cornell.edu/uscode/text/18/3142",
        "cross_references": _j(["18 U.S.C. § 3141", "18 U.S.C. § 3145"])
    },
    {
        "citation": "42 U.S.C. § 12132 (correctional application)",
        "title": "ADA Title II in Correctional Settings",
        "full_text": "The ADA applies to state and local correctional facilities as public entities. Prisons and jails must provide reasonable accommodations for inmates with disabilities, including accessible facilities, sign language interpreters, assistive devices, and modifications to programs and services. The Supreme Court confirmed ADA applies to prisons in Pennsylvania Dept. of Corrections v. Yeskey, 524 U.S. 206 (1998).",
        "domain": "justice",
        "provision_type": "right",
        "applies_when": _j({"disability": ["any"], "setting": ["prison", "jail", "correctional_facility"]}),
        "enforcement_mechanisms": _j([
            "DOJ investigation and enforcement",
            "Private right of action under ADA Title II",
            "Prison grievance process (must exhaust under PLRA)",
            "42 U.S.C. § 1983 for Eighth Amendment violations"
        ]),
        "source_url": "https://www.law.cornell.edu/uscode/text/42/12132",
        "cross_references": _j(["Pa. Dept. of Corrections v. Yeskey, 524 U.S. 206 (1998)", "42 U.S.C. § 1997"])
    },
    {
        "citation": "18 U.S.C. § 3624(c)",
        "title": "Federal Prisoner Reentry — Prerelease Custody",
        "full_text": "The Bureau of Prisons shall, to the extent practicable, ensure that a prisoner serving a term of imprisonment spends a portion of the final months of the term in conditions that will afford the prisoner a reasonable opportunity to adjust to and prepare for reentry into the community, including placement in a community correctional facility or home confinement.",
        "domain": "justice",
        "provision_type": "right",
        "applies_when": _j({"setting": ["federal_prison"], "situation": ["approaching_release"]}),
        "enforcement_mechanisms": _j([
            "BOP administrative remedy process",
            "Federal habeas corpus under 28 U.S.C. § 2241",
            "Mandamus action"
        ]),
        "source_url": "https://www.law.cornell.edu/uscode/text/18/3624",
        "cross_references": _j(["18 U.S.C. § 3621", "34 U.S.C. § 60501"])
    },
    {
        "citation": "34 U.S.C. § 60501",
        "title": "Second Chance Act — Reentry Programs",
        "full_text": "Authorizes federal grants for reentry programs including employment assistance, substance abuse treatment, housing, family reunification, mentoring, and victim services. Programs serve individuals reentering the community after incarceration. Reentry courts and demonstration projects address recidivism reduction.",
        "domain": "justice",
        "provision_type": "right",
        "applies_when": _j({"background": ["incarcerated", "formerly_incarcerated"], "situation": ["reentry"]}),
        "enforcement_mechanisms": _j([
            "Grant program requirements and oversight",
            "DOJ Office of Justice Programs oversight",
            "State and local reentry program access"
        ]),
        "source_url": "https://www.law.cornell.edu/uscode/text/34/60501",
        "cross_references": _j(["18 U.S.C. § 3624(c)"])
    },
    {
        "citation": "42 U.S.C. § 1997",
        "title": "CRIPA — Civil Rights of Institutionalized Persons Act",
        "full_text": "The Attorney General may investigate conditions at state or local institutions (prisons, jails, juvenile facilities, nursing homes, mental health facilities) and bring civil actions to remedy a pattern or practice of egregious or flagrant conditions that deprive residents of constitutional rights.",
        "domain": "justice",
        "provision_type": "protection",
        "applies_when": _j({"setting": ["prison", "jail", "juvenile_facility", "psychiatric_facility", "nursing_facility"]}),
        "enforcement_mechanisms": _j([
            "DOJ investigation and findings letter",
            "Consent decree negotiations",
            "Federal court injunction",
            "Court-appointed monitor"
        ]),
        "source_url": "https://www.law.cornell.edu/uscode/text/42/1997",
        "cross_references": _j(["42 U.S.C. § 1983", "U.S. Const. amend. VIII"])
    },
    {
        "citation": "U.S. Const. amend. VIII",
        "title": "Eighth Amendment — Cruel and Unusual Punishment",
        "full_text": "Excessive bail shall not be required, nor excessive fines imposed, nor cruel and unusual punishments inflicted. In the prison context, this requires provision of adequate medical care (Estelle v. Gamble, 429 U.S. 97 (1976)), protection from violence, and humane conditions of confinement.",
        "domain": "justice",
        "provision_type": "right",
        "applies_when": _j({"setting": ["prison", "jail", "correctional_facility"]}),
        "enforcement_mechanisms": _j([
            "42 U.S.C. § 1983 — Bivens action for federal prisoners",
            "Habeas corpus petition",
            "DOJ investigation under CRIPA",
            "Prison grievance process (must exhaust under PLRA)"
        ]),
        "source_url": "https://www.law.cornell.edu/constitution/eighth_amendment",
        "cross_references": _j(["42 U.S.C. § 1983", "42 U.S.C. § 1997", "Estelle v. Gamble, 429 U.S. 97 (1976)"])
    },
    {
        "citation": "U.S. Const. amend. XIV, § 1",
        "title": "Fourteenth Amendment — Due Process and Equal Protection",
        "full_text": "No State shall deprive any person of life, liberty, or property, without due process of law; nor deny to any person within its jurisdiction the equal protection of the laws. Procedural due process requires notice and opportunity to be heard before deprivation of protected interests. Equal protection prohibits invidious discrimination by state actors.",
        "domain": "justice",
        "provision_type": "right",
        "applies_when": _j({"setting": ["government", "public_program", "criminal_court"]}),
        "enforcement_mechanisms": _j([
            "42 U.S.C. § 1983 action",
            "Federal court constitutional challenge",
            "Habeas corpus petition",
            "State court due process challenge"
        ]),
        "source_url": "https://www.law.cornell.edu/constitution/amendmentxiv",
        "cross_references": _j(["42 U.S.C. § 1983", "42 U.S.C. § 1988"])
    },
    {
        "citation": "18 U.S.C. § 3553(a)",
        "title": "Federal Sentencing — Parsimony Principle",
        "full_text": "The court shall impose a sentence sufficient, but not greater than necessary, to comply with the purposes of sentencing. The court must consider the nature and circumstances of the offense, the history and characteristics of the defendant, the need for the sentence to reflect the seriousness of the offense, promote respect for law, provide just punishment, deter criminal conduct, protect the public, and provide needed educational or vocational training, medical care, or other correctional treatment.",
        "domain": "justice",
        "provision_type": "protection",
        "applies_when": _j({"setting": ["federal_court"], "situation": ["sentencing"]}),
        "enforcement_mechanisms": _j([
            "Sentencing appeal under 18 U.S.C. § 3742",
            "Motion for sentence reduction",
            "28 U.S.C. § 2255 motion to vacate sentence"
        ]),
        "source_url": "https://www.law.cornell.edu/uscode/text/18/3553",
        "cross_references": _j(["18 U.S.C. § 3742", "U.S. Sentencing Guidelines Manual"])
    },
    {
        "citation": "18 U.S.C. § 3582(c)(1)(A)",
        "title": "Compassionate Release — Sentence Reduction",
        "full_text": "A federal prisoner may move the court for a reduction in sentence after exhausting administrative remedies or waiting 30 days from the warden's receipt of the request. The court may reduce the sentence if it finds extraordinary and compelling reasons warrant the reduction, consistent with the sentencing factors under 18 U.S.C. § 3553(a).",
        "domain": "justice",
        "provision_type": "right",
        "applies_when": _j({"setting": ["federal_prison"], "condition": ["terminal_illness", "serious_medical_condition", "elderly"]}),
        "enforcement_mechanisms": _j([
            "Motion to federal sentencing court",
            "Appeal to circuit court",
            "BOP administrative remedy for warden request"
        ]),
        "source_url": "https://www.law.cornell.edu/uscode/text/18/3582",
        "cross_references": _j(["18 U.S.C. § 3553(a)", "U.S.S.G. § 1B1.13"])
    },
    {
        "citation": "42 U.S.C. § 1983 (conditions of confinement)",
        "title": "Section 1983 — Prison Conditions Litigation",
        "full_text": "Prisoners may bring § 1983 actions against state and local officials for violations of constitutional rights including: inadequate medical care (Eighth Amendment), use of excessive force, unconstitutional conditions of confinement, denial of access to courts, and retaliation for exercising First Amendment rights. Must exhaust administrative remedies under PLRA.",
        "domain": "justice",
        "provision_type": "enforcement",
        "applies_when": _j({"setting": ["prison", "jail"], "situation": ["rights_violation"]}),
        "enforcement_mechanisms": _j([
            "Federal lawsuit under 42 U.S.C. § 1983",
            "Must exhaust prison grievance process first (42 U.S.C. § 1997e(a))",
            "Compensatory and punitive damages",
            "Injunctive relief",
            "Attorney's fees under 42 U.S.C. § 1988"
        ]),
        "source_url": "https://www.law.cornell.edu/uscode/text/42/1983",
        "cross_references": _j(["42 U.S.C. § 1997e", "28 U.S.C. § 1915"])
    },
    {
        "citation": "18 U.S.C. § 3006A",
        "title": "Criminal Justice Act — Appointment of Counsel",
        "full_text": "Any person financially unable to obtain adequate representation in federal criminal proceedings is entitled to have counsel appointed at government expense. Applies to felonies, misdemeanors (other than petty offenses), post-conviction proceedings, probation/supervised release revocation, and appeals.",
        "domain": "justice",
        "provision_type": "right",
        "applies_when": _j({"setting": ["federal_court"], "situation": ["criminal_charges"], "income_level": ["cannot_afford_attorney"]}),
        "enforcement_mechanisms": _j([
            "Motion for appointment of counsel",
            "Financial affidavit (CJA 23)",
            "Ineffective assistance of counsel claim"
        ]),
        "source_url": "https://www.law.cornell.edu/uscode/text/18/3006A",
        "cross_references": _j(["U.S. Const. amend. VI", "Gideon v. Wainwright, 372 U.S. 335 (1963)"])
    },
    {
        "citation": "42 U.S.C. § 1396k",
        "title": "Medicaid Assignment of Rights — Third Party Recovery",
        "full_text": "As a condition of eligibility, Medicaid applicants must assign to the state any rights to payment for medical care from third parties. States must take all reasonable measures to ascertain the legal liability of third parties. This provision ensures Medicaid recovers costs from liable parties while beneficiaries receive services without delay.",
        "domain": "health",
        "provision_type": "protection",
        "applies_when": _j({"insurance": ["medicaid"]}),
        "enforcement_mechanisms": _j([
            "State Medicaid agency recovery action",
            "State fair hearing if benefits denied during recovery",
            "42 U.S.C. § 1983 if benefits withheld"
        ]),
        "source_url": "https://www.law.cornell.edu/uscode/text/42/1396k",
        "cross_references": _j(["42 U.S.C. § 1396a(a)(25)"])
    },
    {
        "citation": "20 U.S.C. § 1092(f)",
        "title": "Clery Act — Campus Security Reporting",
        "full_text": "Institutions of higher education receiving federal financial assistance must disclose campus security policies and crime statistics. Schools must issue timely warnings about crimes that pose a threat to students and employees, maintain a daily crime log, and publish an annual security report.",
        "domain": "education",
        "provision_type": "protection",
        "applies_when": _j({"setting": ["university", "college"]}),
        "enforcement_mechanisms": _j([
            "Department of Education enforcement — fines up to $69,733 per violation",
            "Complaint to Department of Education",
            "State attorney general action"
        ]),
        "source_url": "https://www.law.cornell.edu/uscode/text/20/1092",
        "cross_references": _j(["20 U.S.C. § 1681", "34 CFR Part 668"])
    },
    {
        "citation": "42 U.S.C. § 1395cc(a)(1)(Q)",
        "title": "Medicare Patient Self-Determination Act — Advance Directives",
        "full_text": "Medicare-participating hospitals, nursing facilities, home health agencies, and hospice programs must inform patients of their right to make advance directives (living wills, healthcare powers of attorney) under state law. Providers must document whether a patient has an advance directive and may not condition treatment on execution of one.",
        "domain": "health",
        "provision_type": "right",
        "applies_when": _j({"insurance": ["medicare", "medicaid"], "setting": ["hospital", "nursing_facility"]}),
        "enforcement_mechanisms": _j([
            "CMS survey and certification",
            "State health department complaint",
            "Patient rights grievance to facility"
        ]),
        "source_url": "https://www.law.cornell.edu/uscode/text/42/1395cc",
        "cross_references": _j(["42 U.S.C. § 1396a(w)"])
    },
]


def seed_provisions(db: Session) -> int:
    """Seed provisions into the database. Returns count of provisions added."""
    existing = db.query(Provision).count()
    if existing > 0:
        return 0

    for p in PROVISIONS:
        db.add(Provision(**p))
    db.commit()
    return len(PROVISIONS)
