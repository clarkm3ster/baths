import type { MatchedProvision } from "../types/index.ts";

export const mockProvisions: MatchedProvision[] = [
  // ── Health ──────────────────────────────────────────────────────
  {
    provision_id: 1,
    citation: "42 U.S.C. § 1396d(r)",
    title: "Medicaid EPSDT — Comprehensive Care for Under-21",
    full_text:
      "Early and Periodic Screening, Diagnostic, and Treatment (EPSDT) requires state Medicaid programs to provide comprehensive health services to children and young adults under age 21, including any medically necessary service listed in Section 1905(a) of the Social Security Act, even if the state does not otherwise cover the service in its Medicaid plan.",
    domain: "health",
    provision_type: "right",
    relevance_score: 1.0,
    match_reasons: ["Under 21 with Medicaid coverage"],
    enforcement_steps: [
      "Request the specific service from your provider in writing",
      "If denied, file a fair hearing request with your state Medicaid agency within 90 days",
      "Contact your state's Protection & Advocacy organization",
    ],
    is_gap: false,
    source_url: "https://www.law.cornell.edu/uscode/text/42/1396d",
    cross_references: ["42 U.S.C. § 1396a(a)(10)", "42 U.S.C. § 1396a(a)(43)"],
  },
  {
    provision_id: 2,
    citation: "29 U.S.C. § 1185a",
    title: "Mental Health Parity and Addiction Equity Act",
    full_text:
      "Group health plans offering mental health or substance use disorder benefits must ensure that financial requirements and treatment limitations are no more restrictive than the predominant requirements and limitations applied to substantially all medical and surgical benefits.",
    domain: "health",
    provision_type: "protection",
    relevance_score: 0.8,
    match_reasons: ["Has mental health condition", "Insurance coverage applies"],
    enforcement_steps: [
      "Request a written explanation of any denial in terms of parity requirements",
      "File a complaint with your state insurance commissioner",
      "File a complaint with the U.S. Department of Labor at (866) 444-3272",
    ],
    is_gap: false,
    source_url: "https://www.law.cornell.edu/uscode/text/29/1185a",
    cross_references: ["42 U.S.C. § 300gg-26"],
  },
  {
    provision_id: 3,
    citation: "42 U.S.C. § 1395dd",
    title: "EMTALA — Emergency Medical Treatment",
    full_text:
      "A hospital with an emergency department must provide an appropriate medical screening examination to any individual who comes to the emergency department requesting examination or treatment. If the individual has an emergency medical condition, the hospital must stabilize the condition before discharge or transfer.",
    domain: "health",
    provision_type: "right",
    relevance_score: 0.6,
    match_reasons: ["Universal right applicable to all persons"],
    enforcement_steps: [
      "If turned away from an ER, document the date, time, and staff involved",
      "File a complaint with CMS at 1-800-MEDICARE",
      "File a complaint with your state health department",
    ],
    is_gap: false,
    source_url: "https://www.law.cornell.edu/uscode/text/42/1395dd",
    cross_references: [],
  },
  {
    provision_id: 4,
    citation: "42 CFR Part 438",
    title: "Medicaid Managed Care Protections",
    full_text:
      "Managed care organizations serving Medicaid beneficiaries must meet requirements for access to services, network adequacy, grievance and appeal procedures, and quality assessment. Enrollees have the right to timely access to covered services and to file grievances and appeals.",
    domain: "health",
    provision_type: "protection",
    relevance_score: 0.9,
    match_reasons: ["Medicaid beneficiary in managed care"],
    enforcement_steps: [
      "File an internal grievance with your MCO within 60 days",
      "Request a state fair hearing if MCO denies your appeal",
      "Contact your state Medicaid managed care ombudsman",
    ],
    is_gap: false,
    source_url: "https://www.law.cornell.edu/cfr/text/42/part-438",
    cross_references: ["42 U.S.C. § 1396u-2"],
  },
  {
    provision_id: 5,
    citation: "42 U.S.C. § 1396n(c)",
    title: "HCBS Waiver — Home and Community-Based Services",
    full_text:
      "States may request waivers to provide home and community-based services to individuals who would otherwise require institutional care. Services may include case management, homemaker services, home health aide, personal care, adult day health, habilitation, and respite care.",
    domain: "health",
    provision_type: "right",
    relevance_score: 0.8,
    match_reasons: ["Has disability", "May qualify for community-based services"],
    enforcement_steps: [
      "Apply through your state Medicaid agency for an HCBS waiver slot",
      "If placed on a waitlist, request expedited review if your needs are urgent",
      "Appeal any denial through the state fair hearing process",
    ],
    is_gap: false,
    source_url: "https://www.law.cornell.edu/uscode/text/42/1396n",
    cross_references: ["42 U.S.C. § 1396a"],
  },

  // ── Civil Rights ────────────────────────────────────────────────
  {
    provision_id: 6,
    citation: "42 U.S.C. § 12132",
    title: "ADA Title II — Public Services",
    full_text:
      "No qualified individual with a disability shall, by reason of such disability, be excluded from participation in or be denied the benefits of the services, programs, or activities of a public entity, or be subjected to discrimination by any such entity.",
    domain: "civil_rights",
    provision_type: "right",
    relevance_score: 1.0,
    match_reasons: ["Person with a disability interacting with public entities"],
    enforcement_steps: [
      "File a complaint with the relevant federal agency (DOJ for state/local gov)",
      "File an ADA complaint online at ada.gov within 180 days",
      "Request reasonable modifications in writing to the public entity",
    ],
    is_gap: false,
    source_url: "https://www.law.cornell.edu/uscode/text/42/12132",
    cross_references: ["28 CFR Part 35", "29 U.S.C. § 794"],
  },
  {
    provision_id: 7,
    citation: "42 U.S.C. § 12182",
    title: "ADA Title III — Public Accommodations",
    full_text:
      "No individual shall be discriminated against on the basis of disability in the full and equal enjoyment of the goods, services, facilities, privileges, advantages, or accommodations of any place of public accommodation.",
    domain: "civil_rights",
    provision_type: "right",
    relevance_score: 0.9,
    match_reasons: ["Person with a disability accessing private businesses"],
    enforcement_steps: [
      "Notify the business in writing of the access barrier",
      "File a complaint with the DOJ Civil Rights Division",
      "File a private lawsuit — no exhaustion of administrative remedies required",
    ],
    is_gap: false,
    source_url: "https://www.law.cornell.edu/uscode/text/42/12182",
    cross_references: ["28 CFR Part 36"],
  },
  {
    provision_id: 8,
    citation: "29 U.S.C. § 794",
    title: "Section 504 — Rehabilitation Act",
    full_text:
      "No otherwise qualified individual with a disability shall, solely by reason of her or his disability, be excluded from the participation in, be denied the benefits of, or be subjected to discrimination under any program or activity receiving Federal financial assistance.",
    domain: "civil_rights",
    provision_type: "protection",
    relevance_score: 0.9,
    match_reasons: ["Has disability", "Interacts with federally funded programs"],
    enforcement_steps: [
      "File a complaint with the federal agency funding the program within 180 days",
      "For education: file with the Office for Civil Rights (OCR) at ed.gov",
      "For health: file with HHS Office for Civil Rights",
    ],
    is_gap: false,
    source_url: "https://www.law.cornell.edu/uscode/text/29/794",
    cross_references: ["42 U.S.C. § 12132"],
  },
  {
    provision_id: 9,
    citation: "Olmstead v. L.C., 527 U.S. 581 (1999)",
    title: "Olmstead — Community Integration Mandate",
    full_text:
      "Under the ADA, states are required to provide community-based services to persons with disabilities when (1) such services are appropriate, (2) the affected persons do not oppose community-based treatment, and (3) community-based services can be reasonably accommodated, taking into account the resources available to the state.",
    domain: "civil_rights",
    provision_type: "right",
    relevance_score: 0.8,
    match_reasons: [
      "Has disability",
      "May be at risk of unnecessary institutionalization",
    ],
    enforcement_steps: [
      "Request a community-based placement from your state disability services agency",
      "File a complaint with the DOJ under the Olmstead mandate",
      "Contact your state Protection & Advocacy organization for assistance",
    ],
    is_gap: false,
    source_url:
      "https://supreme.justia.com/cases/federal/us/527/581/",
    cross_references: ["42 U.S.C. § 12132"],
  },

  // ── Housing ─────────────────────────────────────────────────────
  {
    provision_id: 10,
    citation: "42 U.S.C. § 3604",
    title: "Fair Housing Act — Disability Protections",
    full_text:
      "It is unlawful to discriminate in the sale, rental, or financing of housing based on disability. This includes a refusal to make reasonable accommodations in rules, policies, practices, or services when such accommodations may be necessary to afford a person with a disability equal opportunity to use and enjoy a dwelling.",
    domain: "housing",
    provision_type: "protection",
    relevance_score: 0.9,
    match_reasons: ["Person with disability in housing situation"],
    enforcement_steps: [
      "Request reasonable accommodation in writing to your landlord",
      "File a complaint with HUD within 1 year at (800) 669-9777",
      "File with your state or local fair housing agency",
    ],
    is_gap: false,
    source_url: "https://www.law.cornell.edu/uscode/text/42/3604",
    cross_references: ["24 CFR Part 100"],
  },
  {
    provision_id: 11,
    citation: "42 U.S.C. § 1437f",
    title: "Section 8 Housing Choice Voucher Program",
    full_text:
      "The Housing Choice Voucher program provides rental assistance to eligible low-income families, the elderly, and persons with disabilities. Participants find their own housing and the public housing agency pays a subsidy directly to the landlord.",
    domain: "housing",
    provision_type: "right",
    relevance_score: 0.7,
    match_reasons: ["Low income", "May qualify for housing assistance"],
    enforcement_steps: [
      "Apply at your local Public Housing Agency (PHA)",
      "If denied, request an informal hearing within the PHA's stated timeframe",
      "Contact HUD if you believe the PHA violated program rules",
    ],
    is_gap: false,
    source_url: "https://www.law.cornell.edu/uscode/text/42/1437f",
    cross_references: ["24 CFR Part 982"],
  },
  {
    provision_id: 12,
    citation: "34 U.S.C. § 12491",
    title: "VAWA Housing Protections",
    full_text:
      "Tenants in federally subsidized housing who are victims of domestic violence, dating violence, sexual assault, or stalking cannot be denied housing, evicted, or have assistance terminated solely because they are victims.",
    domain: "housing",
    provision_type: "protection",
    relevance_score: 0.9,
    match_reasons: ["DV survivor", "In subsidized housing"],
    enforcement_steps: [
      "Notify your housing provider of your VAWA protections in writing",
      "Request an emergency transfer if you are in danger",
      "File a complaint with HUD if your housing provider violates VAWA",
    ],
    is_gap: false,
    source_url: "https://www.law.cornell.edu/uscode/text/34/12491",
    cross_references: ["42 U.S.C. § 1437f"],
  },
  {
    provision_id: 13,
    citation: "42 U.S.C. § 11431",
    title: "McKinney-Vento — Homeless Education Rights",
    full_text:
      "Homeless children and youth have the right to immediate enrollment in school, transportation to their school of origin, and access to the same programs and services available to other students. Each school district must designate a homeless liaison.",
    domain: "housing",
    provision_type: "right",
    relevance_score: 0.8,
    match_reasons: ["Experiencing homelessness or housing instability"],
    enforcement_steps: [
      "Contact your school district's McKinney-Vento liaison",
      "If denied enrollment, request immediate provisional enrollment",
      "File a complaint with your state Department of Education",
    ],
    is_gap: false,
    source_url: "https://www.law.cornell.edu/uscode/text/42/11431",
    cross_references: [],
  },

  // ── Income ──────────────────────────────────────────────────────
  {
    provision_id: 14,
    citation: "42 U.S.C. § 1382",
    title: "Supplemental Security Income (SSI)",
    full_text:
      "SSI provides monthly cash payments to eligible individuals who are aged 65 or older, blind, or disabled and who have limited income and resources. The federal benefit rate is adjusted annually for cost of living.",
    domain: "income",
    provision_type: "right",
    relevance_score: 0.9,
    match_reasons: ["Has disability", "Limited income"],
    enforcement_steps: [
      "Apply at your local Social Security office or online at ssa.gov",
      "If denied, request reconsideration within 60 days",
      "Request an ALJ hearing within 60 days of reconsideration denial",
      "Contact your state's legal aid organization for representation",
    ],
    is_gap: false,
    source_url: "https://www.law.cornell.edu/uscode/text/42/1382",
    cross_references: ["42 U.S.C. § 1382c"],
  },
  {
    provision_id: 15,
    citation: "42 U.S.C. § 423",
    title: "Social Security Disability Insurance (SSDI)",
    full_text:
      "SSDI provides monthly disability benefits to individuals who have worked and paid Social Security taxes but can no longer work due to a significant medical condition expected to last at least 12 months or result in death.",
    domain: "income",
    provision_type: "right",
    relevance_score: 0.7,
    match_reasons: ["Has disability with work history"],
    enforcement_steps: [
      "Apply online at ssa.gov or at your local Social Security office",
      "If denied, request reconsideration within 60 days",
      "Request an ALJ hearing if reconsideration is denied",
    ],
    is_gap: false,
    source_url: "https://www.law.cornell.edu/uscode/text/42/423",
    cross_references: ["42 U.S.C. § 1382"],
  },
  {
    provision_id: 16,
    citation: "7 U.S.C. § 2011",
    title: "SNAP — Supplemental Nutrition Assistance",
    full_text:
      "The Supplemental Nutrition Assistance Program provides food-purchasing assistance for low-income individuals and families. Eligibility is based on household income, resources, and certain expenses. Most able-bodied adults must meet work requirements.",
    domain: "income",
    provision_type: "right",
    relevance_score: 0.8,
    match_reasons: ["Low income", "May qualify for nutrition assistance"],
    enforcement_steps: [
      "Apply through your state SNAP agency or local DSS office",
      "If denied, request a fair hearing within 90 days",
      "Benefits must begin within 30 days of application (7 days if expedited)",
    ],
    is_gap: false,
    source_url: "https://www.law.cornell.edu/uscode/text/7/2011",
    cross_references: [],
  },

  // ── Education ───────────────────────────────────────────────────
  {
    provision_id: 17,
    citation: "20 U.S.C. § 1400",
    title: "IDEA — Individuals with Disabilities Education Act",
    full_text:
      "Children with disabilities are entitled to a free appropriate public education (FAPE) in the least restrictive environment. Schools must develop an Individualized Education Program (IEP) for each eligible child, with parent participation in all decisions.",
    domain: "education",
    provision_type: "right",
    relevance_score: 1.0,
    match_reasons: ["Under 21 with disability", "In educational setting"],
    enforcement_steps: [
      "Request an IEP evaluation in writing to your school district",
      "School must respond within 60 days (or state timeline)",
      "If you disagree with the IEP, request mediation or a due process hearing",
      "File a state complaint with your state Department of Education",
    ],
    is_gap: false,
    source_url: "https://www.law.cornell.edu/uscode/text/20/1400",
    cross_references: ["29 U.S.C. § 794"],
  },
  {
    provision_id: 18,
    citation: "29 U.S.C. § 794 (Education)",
    title: "Section 504 Plan in Schools",
    full_text:
      "Students with disabilities who do not qualify for an IEP under IDEA may still be entitled to a Section 504 plan providing accommodations and modifications to ensure equal access to education.",
    domain: "education",
    provision_type: "right",
    relevance_score: 0.8,
    match_reasons: ["Has disability", "In educational setting"],
    enforcement_steps: [
      "Request a Section 504 evaluation from your school in writing",
      "Participate in the 504 team meeting to develop accommodations",
      "File a complaint with OCR if the school fails to provide accommodations",
    ],
    is_gap: false,
    source_url: "https://www.law.cornell.edu/uscode/text/29/794",
    cross_references: ["20 U.S.C. § 1400"],
  },
  {
    provision_id: 19,
    citation: "20 U.S.C. § 1681",
    title: "Title IX — Sex Discrimination in Education",
    full_text:
      "No person in the United States shall, on the basis of sex, be excluded from participation in, be denied the benefits of, or be subjected to discrimination under any education program or activity receiving Federal financial assistance.",
    domain: "education",
    provision_type: "protection",
    relevance_score: 0.6,
    match_reasons: ["Enrolled in educational program receiving federal funds"],
    enforcement_steps: [
      "Report to your school's Title IX coordinator",
      "File a complaint with the OCR within 180 days",
    ],
    is_gap: false,
    source_url: "https://www.law.cornell.edu/uscode/text/20/1681",
    cross_references: [],
  },

  // ── Justice ─────────────────────────────────────────────────────
  {
    provision_id: 20,
    citation: "U.S. Const. amend. VI",
    title: "Right to Counsel",
    full_text:
      "In all criminal prosecutions, the accused shall enjoy the right to have the Assistance of Counsel for his defence. If the accused cannot afford counsel, the court must appoint a public defender.",
    domain: "justice",
    provision_type: "right",
    relevance_score: 0.6,
    match_reasons: ["Fundamental constitutional right"],
    enforcement_steps: [
      "If arrested, clearly state 'I want a lawyer' and do not answer questions",
      "If you cannot afford one, the court must appoint counsel at no cost",
      "Contact your local public defender's office",
    ],
    is_gap: false,
    source_url:
      "https://constitution.congress.gov/browse/amendment-6/",
    cross_references: [],
  },
  {
    provision_id: 21,
    citation: "42 U.S.C. § 12132 (Corrections)",
    title: "ADA in Correctional Settings",
    full_text:
      "The ADA applies to state and local correctional facilities. Inmates with disabilities must be provided reasonable accommodations, accessible facilities, and cannot be discriminated against in programs, services, or activities.",
    domain: "justice",
    provision_type: "protection",
    relevance_score: 0.8,
    match_reasons: ["Has disability", "System involvement"],
    enforcement_steps: [
      "File a grievance with the facility's ADA coordinator",
      "File a complaint with the DOJ Civil Rights Division",
      "Contact your state's Protection & Advocacy organization",
    ],
    is_gap: false,
    source_url: "https://www.law.cornell.edu/uscode/text/42/12132",
    cross_references: ["42 U.S.C. § 12132"],
  },
  {
    provision_id: 22,
    citation: "18 U.S.C. § 3142",
    title: "Bail Reform Act — Pretrial Release",
    full_text:
      "Federal courts must consider release on personal recognizance or unsecured bond unless the judicial officer determines that such release will not reasonably assure the appearance of the person or the safety of the community.",
    domain: "justice",
    provision_type: "right",
    relevance_score: 0.5,
    match_reasons: ["General justice system right"],
    enforcement_steps: [
      "Request a bail hearing and present information on ties to community",
      "Challenge detention conditions through defense counsel",
    ],
    is_gap: false,
    source_url: "https://www.law.cornell.edu/uscode/text/18/3142",
    cross_references: [],
  },
  {
    provision_id: 23,
    citation: "42 U.S.C. § 1396a(a)(10)(A)",
    title: "Medicaid Mandatory Coverage Groups",
    full_text:
      "States must provide Medicaid coverage to certain mandatory eligibility groups, including low-income families, qualified pregnant women, children under age 19 in families with income at or below 138% FPL, SSI recipients, and certain other groups.",
    domain: "health",
    provision_type: "right",
    relevance_score: 0.9,
    match_reasons: ["Medicaid beneficiary"],
    enforcement_steps: [
      "Apply through your state Medicaid agency or healthcare.gov",
      "If denied, appeal within 90 days through the state fair hearing process",
      "Contact your state health insurance assistance program (SHIP)",
    ],
    is_gap: false,
    source_url: "https://www.law.cornell.edu/uscode/text/42/1396a",
    cross_references: ["42 U.S.C. § 1396d(r)"],
  },
  {
    provision_id: 24,
    citation: "42 U.S.C. § 300gg-14",
    title: "ACA — Dependent Coverage to Age 26",
    full_text:
      "Health insurance issuers offering dependent coverage must make coverage available for adult children until they turn 26 years of age, regardless of whether the child is married, a student, or financially dependent.",
    domain: "health",
    provision_type: "right",
    relevance_score: 0.7,
    match_reasons: ["Under 26", "Health insurance access"],
    enforcement_steps: [
      "Contact your parent's insurance plan to enroll",
      "If denied, file a complaint with your state insurance commissioner",
      "File with CMS if it is a self-funded employer plan",
    ],
    is_gap: false,
    source_url: "https://www.law.cornell.edu/uscode/text/42/300gg-14",
    cross_references: [],
  },
];

export const mockGaps: MatchedProvision[] = [
  {
    provision_id: 101,
    citation: "42 U.S.C. § 1396d(r)",
    title: "EPSDT Services — Not Currently Receiving",
    full_text:
      "You appear to qualify for comprehensive EPSDT screening and treatment services under Medicaid but may not be receiving all services you are entitled to.",
    domain: "health",
    provision_type: "right",
    relevance_score: 0.9,
    match_reasons: [
      "Under 21 on Medicaid",
      "No record of EPSDT screening in past year",
    ],
    enforcement_steps: [
      "Contact your Medicaid MCO and request an EPSDT screening",
      "Ask your pediatrician to conduct a comprehensive screening",
    ],
    is_gap: true,
  },
  {
    provision_id: 102,
    citation: "42 U.S.C. § 3604",
    title: "Reasonable Accommodation — Not Requested",
    full_text:
      "You may be entitled to a reasonable accommodation in your housing based on your disability but have not yet made a formal request.",
    domain: "housing",
    provision_type: "protection",
    relevance_score: 0.7,
    match_reasons: [
      "Has disability",
      "In rental housing",
      "No accommodation on record",
    ],
    enforcement_steps: [
      "Submit a written reasonable accommodation request to your landlord",
      "Include documentation from your healthcare provider",
    ],
    is_gap: true,
  },
  {
    provision_id: 103,
    citation: "42 U.S.C. § 1382",
    title: "SSI Benefits — Potentially Eligible",
    full_text:
      "Based on your disability status and income level, you may be eligible for Supplemental Security Income but do not appear to be receiving it.",
    domain: "income",
    provision_type: "right",
    relevance_score: 0.8,
    match_reasons: ["Has disability", "Low income", "Not currently receiving SSI"],
    enforcement_steps: [
      "Apply at ssa.gov or visit your local Social Security office",
      "Gather medical records documenting your disability",
    ],
    is_gap: true,
  },
  {
    provision_id: 104,
    citation: "20 U.S.C. § 1400",
    title: "IEP Services — May Be Underserved",
    full_text:
      "You may be entitled to additional special education services under an IEP that are not currently being provided.",
    domain: "education",
    provision_type: "right",
    relevance_score: 0.7,
    match_reasons: ["Under 21 with disability", "Enrolled in school"],
    enforcement_steps: [
      "Request an IEP review meeting with your school district",
      "Bring documentation of unmet needs to the meeting",
    ],
    is_gap: true,
  },
  {
    provision_id: 105,
    citation: "42 U.S.C. § 12132",
    title: "ADA Reasonable Modification — State Services",
    full_text:
      "You may be entitled to reasonable modifications from state agencies that you have not yet requested.",
    domain: "civil_rights",
    provision_type: "right",
    relevance_score: 0.6,
    match_reasons: ["Has disability", "Uses state services"],
    enforcement_steps: [
      "Identify the specific service or program where you need modification",
      "Submit a written request to the agency's ADA coordinator",
    ],
    is_gap: true,
  },
  {
    provision_id: 106,
    citation: "18 U.S.C. § 3624(c)",
    title: "Reentry Planning — Not Yet Initiated",
    full_text:
      "Individuals nearing release from federal custody are entitled to pre-release planning and transitional services, including placement in community corrections.",
    domain: "justice",
    provision_type: "right",
    relevance_score: 0.6,
    match_reasons: ["Currently incarcerated", "Approaching release"],
    enforcement_steps: [
      "Request a meeting with your case manager about reentry planning",
      "Contact the Bureau of Prisons reentry affairs coordinator",
    ],
    is_gap: true,
  },
];

export const mockExplanation = {
  plain_english:
    "This law says that if you are under 21 and on Medicaid, your state MUST provide you with any medically necessary health service — even services that adults on Medicaid in your state cannot get. This includes physical exams, dental care, vision, hearing, mental health services, and any treatment a doctor says you need.",
  what_it_means_for_you:
    "Because you are under 21 and have Medicaid, you have the right to comprehensive health screenings and ANY treatment that is medically necessary. If a doctor says you need a service, Medicaid must cover it — period. This is broader than what adults get.",
  your_rights: [
    "Right to periodic health screenings (physical, dental, vision, hearing)",
    "Right to any medically necessary treatment, even if not in the state plan",
    "Right to transportation to medical appointments",
    "Right to have your parent or guardian involved in care decisions",
  ],
  enforcement_steps: [
    "Step 1: Ask your doctor to document that the service is medically necessary",
    "Step 2: Submit the request to your Medicaid managed care plan in writing",
    "Step 3: If denied, file an internal appeal with the MCO within 60 days",
    "Step 4: If the MCO upholds the denial, request a state fair hearing within 120 days",
    "Step 5: Contact your state Protection & Advocacy organization for free legal help",
  ],
  key_deadlines: [
    "60 days to file internal appeal after denial",
    "120 days to request state fair hearing after internal appeal",
    "Screenings should occur at regular intervals set by the state's periodicity schedule",
  ],
  who_to_contact: [
    "Your state Medicaid agency — find at medicaid.gov",
    "State Protection & Advocacy organization — find at ndrn.org",
    "Legal aid: lawhelp.org for free legal assistance",
    "Medicaid ombudsman in your state",
  ],
};
