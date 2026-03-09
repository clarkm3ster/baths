// ============================================================================
// BATHS Studio Suite — Complete Data Layer
// Generated from clarkm3ster/baths repo audit (2026-03-08)
// Sets window.BATHS_DATA with all extracted business data.
// ============================================================================

window.BATHS_DATA = {

// ============================================================================
// 1. NAMING — DUOMO / THAUMA / BATHS Identity
// ============================================================================
naming: {
  company: "BATHS",
  equation: "Cosm × Chron = Flourishing",
  duomo: { display: "DUOMO", legacy: "Domes", description: "Points at a person. Builds whole-person digital twins across 12 life domains." },
  thauma: { display: "THAUMA", legacy: "Spheres", description: "Points at a place. Activates public spaces in cities." },
  thaumaOS: { display: "THAUMA/OS", legacy: "SPHERE/OS", description: "Programmable material environment OS for activating Philadelphia vacant parcels." },
  rule: "Never show legacy names (Domes, Spheres, SPHERE/OS) in UI. Internal code comments are fine.",
},

// ============================================================================
// 2. CODEBASE STATS — Real counts from repo
// ============================================================================
codebaseStats: {
  provisions: 5126,
  costPoints: 35,
  govSystems: 31,
  parcels: 14,
  enrichments: 4898,
  services: 18,
  totalScrapeRuns: 7,
  successfulScrapes: 7,
  dbSizeMb: 3.73,
  systemLinks: 19,
  coordinationModels: 18,    // 10 domes-architect + 8 baths-engine
  aiTeammates: 12,
  innovations: 66,
  philosophicalFrameworks: 6,
  flourishingDomains: 12,
  agreementTemplates: 7,
  eligibilityPrograms: 12,
  canonicalProfiles: 5,
  providers: 8,
  jobs: 6,
  materialSystems: 9,
  pipelineStages: 5,
  censusAcsGroups: 10,
  priorityCounties: 28,
  cosmArchetypes: 6,
  ormClasses: 22,
  apiEndpoints: 35,
  coreAlgorithms: 12,
},

// ============================================================================
// 3. DOMAINS — All 12 BATHS Life Domains
// ============================================================================
domains: [
  { id: "health",       label: "Health",        color: "#1A6B3C", provisionTypes: ["right","protection","obligation","enforcement"] },
  { id: "civil_rights", label: "Civil Rights",   color: "#6B1A4B", provisionTypes: ["protection","right","enforcement"] },
  { id: "housing",      label: "Housing",        color: "#1A3D8B", provisionTypes: ["right","protection"] },
  { id: "income",       label: "Income",         color: "#6B5A1A", provisionTypes: ["right","protection"] },
  { id: "education",    label: "Education",      color: "#5A1A6B", provisionTypes: ["right","protection","obligation"] },
  { id: "justice",      label: "Justice",        color: "#8B1A1A", provisionTypes: ["right","protection","enforcement"] },
  { id: "child_welfare",label: "Child Welfare",  color: "#1A6B6B", provisionTypes: ["right","protection","obligation"] },
],

// ============================================================================
// 4. STUDIO SCHEMA — Full Studio ORM (7 classes)
// ============================================================================
studioSchema: {
  StudioCharacter: {
    fields: {
      character_id: "Text, unique, indexed",
      character_type: "Text",   // real | fictional | composite | scenario
      name_or_alias: "Text",
      consent_tier: "Text",     // tier1_public | tier2_personal | tier3_sensitive | tier4_highest
      fictionalization_rules: "JSON",
      circumstances_summary: "Text",
      initial_conditions: "JSON",
    },
    enums: {
      character_type: ["real","fictional","composite","scenario"],
      consent_tier: ["tier1_public","tier2_personal","tier3_sensitive","tier4_highest"],
    },
  },
  StudioProduction: {
    fields: {
      production_id: "Text, unique, indexed",
      title: "Text",
      medium: "Text",  // film|short|doc|series|installation|live_event|product|game|interactive
      character_id: "FK → StudioCharacter",
      stage: "Text, default greenlit", // greenlit|in_progress|paused|shipped
      budget_total: "Float, default 0.0",
      financing_sources: "JSON",
    },
    enums: {
      medium: ["film","short","doc","series","installation","live_event","product","game","interactive"],
      stage: ["greenlit","in_progress","paused","shipped"],
    },
  },
  StudioProductionStage: {
    fields: {
      production_id: "FK → StudioProduction",
      stage: "Text",  // development|pre_production|production|post|distribution
      start_date: "Text",
      end_date: "Text",
      cost_cap: "Float, default 0.0",
      deliverables: "JSON",
      risk_register: "JSON",
    },
    enums: { stage: ["development","pre_production","production","post","distribution"] },
  },
  StudioTalentRole: {
    fields: {
      production_id: "FK → StudioProduction",
      person_or_entity: "Text",
      role: "Text",
      rate_type: "Text",  // day|week|flat|salary|vendor
      rate: "Float, default 0.0",
    },
    enums: { rate_type: ["day","week","flat","salary","vendor"] },
  },
  StudioGap: {
    fields: {
      gap_id: "Text, unique, indexed",
      production_id: "FK → StudioProduction",
      character_id: "FK → StudioCharacter",
      area: "Text, indexed",  // metrics|connectors|ledger|forecast|scenario|settlement|validation|consent|ux
      severity: "Text, indexed",  // low|medium|high|blocking
      description: "Text",
      reproduction_steps: "JSON",
      proposed_fix: "Text",
      owner_module: "Text, indexed",
      status: "Text, default new",  // new|triaged|planned|in_progress|shipped|wont_fix
    },
    enums: {
      area: ["metrics","connectors","ledger","forecast","scenario","settlement","validation","consent","ux"],
      severity: ["low","medium","high","blocking"],
      status: ["new","triaged","planned","in_progress","shipped","wont_fix"],
    },
  },
  StudioIPAsset: {
    fields: {
      asset_id: "Text, unique, indexed",
      production_id: "FK → StudioProduction",
      asset_type: "Text",  // script|footage|cut|poster|soundtrack|prototype|dataset_synthetic|curriculum|installation_plan
      title: "Text",
      storage_uri: "Text",
      contributors: "JSON",
      rights: "JSON",
    },
    enums: { asset_type: ["script","footage","cut","poster","soundtrack","prototype","dataset_synthetic","curriculum","installation_plan"] },
  },
  StudioLearningPackage: {
    fields: {
      learning_id: "Text, unique, indexed",
      production_id: "FK → StudioProduction",
      summary: "Text",
      gap_ids: "JSON",
      proposed_os_changes: "JSON",
      validation_needed: "JSON",
    },
  },
},

// ============================================================================
// 5. PROFILES — All 5 Canonical Profiles (complete data)
// ============================================================================
profiles: {
  marcus: {
    person_id: "marcus-thompson",
    name: "Marcus Thompson",
    age: 34, sex: "male", race_ethnicity: "black",
    conditions: ["substance_use_disorder","depression"],
    setting: "outpatient", severity: "moderate",
    earned_income: 22880.0,
    benefits: { snap: 2400, medicaid: 8000 },
    location: { lat: 39.9918, lng: -75.1286, area: "Kensington, Philadelphia" },
    has_vehicle: false, transit_pass: true, travel_budget: 80.0,
    insurance: "medicaid", language: "en",
    systems_involved: ["doc","medicaid","bha","hmis","probation","snap","unemployment","mco","pdmp","shelter"],
    annual_cost_fragmented: 87400.0,
    annual_cost_coordinated: 34200.0,
    annual_savings: 53200.0,
    five_year_savings: 266000.0,
    lifetime_estimate: 1085280.0,
    domainBreakdown: {
      health:  { total: 45500, coordinated: 23350, savings: 22150, systems: { medicaid: 12000, bha: 18000, mco: 14000, pdmp: 1500 } },
      justice: { total: 20000, coordinated: 9500,  savings: 10500, systems: { doc: 15000, probation: 5000 } },
      housing: { total: 20000, coordinated: 7400,  savings: 12600, systems: { hmis: 8000, shelter: 12000 } },
      income:  { total: 9600,  coordinated: 7500,  savings: 2100,  systems: { snap: 3600, unemployment: 6000 } },
    },
    circumstances: ["is_recently_released","has_substance_use","has_mental_illness","is_homeless","is_on_medicaid","is_on_snap","is_unemployed"],
  },
  sarah: {
    person_id: "sarah-chen",
    name: "Sarah Chen",
    age: 28, sex: "female", race_ethnicity: "asian",
    conditions: ["ptsd","anxiety"],
    setting: "outpatient", severity: "moderate",
    earned_income: 0.0,
    benefits: { tanf: 4800, snap: 3600, medicaid: 8000, ccdf: 6000 },
    location: { lat: 39.9526, lng: -75.1652, area: "Center City, Philadelphia" },
    has_vehicle: false, transit_pass: false, travel_budget: 40.0,
    mobility_constraints: ["child_care_hours"],
    insurance: "medicaid", language: "zh",
    systems_involved: ["sacwis","tanf","pha","medicaid","court_cms","snap","mco"],
    annual_cost_fragmented: 72200.0,
    annual_cost_coordinated: 29100.0,
    annual_savings: 43100.0,
    five_year_savings: 215500.0,
    lifetime_estimate: 879240.0,
    circumstances: ["has_dv_history","is_on_tanf","is_section_8","is_on_medicaid","has_child_in_foster","is_on_snap"],
  },
  james: {
    person_id: "james-williams",
    name: "James Williams",
    age: 52, sex: "male", race_ethnicity: "black",
    conditions: ["ptsd","chronic_pain","diabetes"],
    setting: "outpatient", severity: "moderate",
    earned_income: 0.0,
    benefits: { ssi: 10800, medicaid: 8000 },
    location: { lat: 39.9637, lng: -75.2406, area: "West Philadelphia" },
    has_vehicle: true, transit_pass: false, travel_budget: 150.0,
    mobility_constraints: ["wheelchair"],
    insurance: "medicaid", language: "en",
    systems_involved: ["va","medicaid","ssa","pdmp","hie","mco","ssi"],
    annual_cost_fragmented: 94100.0,
    annual_cost_coordinated: 52300.0,
    annual_savings: 41800.0,
    circumstances: ["is_va_healthcare","has_disability","has_chronic_health","is_on_medicaid","is_on_ssi"],
  },
  maria: {
    person_id: "maria-rodriguez",
    name: "Maria Rodriguez",
    age: 16, sex: "female", race_ethnicity: "hispanic",
    conditions: ["trauma","adhd"],
    setting: "outpatient", severity: "moderate",
    earned_income: 0.0,
    benefits: { medicaid: 8000 },
    location: { lat: 40.0379, lng: -75.1396, area: "North Philadelphia" },
    has_vehicle: false, transit_pass: false, travel_budget: 20.0,
    insurance: "medicaid", language: "es",
    systems_involved: ["sacwis","education","juvenile_justice","medicaid","mco"],
    annual_cost_fragmented: 68500.0,
    annual_cost_coordinated: 31200.0,
    annual_savings: 37300.0,
    circumstances: ["is_juvenile_justice","has_child_in_foster","is_on_medicaid","is_school_age","has_mental_illness"],
  },
  robert: {
    person_id: "robert-jackson",
    name: "Robert Jackson",
    age: 45, sex: "male", race_ethnicity: "black",
    conditions: ["schizophrenia","diabetes","hypertension"],
    setting: "emergency", severity: "severe",
    earned_income: 0.0,
    benefits: { ssi: 10800, medicaid: 8000, snap: 2400 },
    location: { lat: 39.9550, lng: -75.1550, area: "Downtown Philadelphia (no fixed address)" },
    has_vehicle: false, transit_pass: false, travel_budget: 0.0,
    mobility_constraints: ["limited_walking"],
    insurance: "medicaid", language: "en",
    systems_involved: ["medicaid","bha","hmis","shelter","snap","ssi","mco","er"],
    annual_cost_fragmented: 94800.0,
    annual_cost_coordinated: 38200.0,
    annual_savings: 56600.0,
    circumstances: ["is_homeless","has_mental_illness","has_chronic_health","is_frequent_er","is_on_medicaid","is_on_snap","is_on_ssi"],
  },
},

// ============================================================================
// 6. PROVIDERS — All 8 Philadelphia Providers
// ============================================================================
providers: [
  { id: "prov-kens-bh",     name: "Kensington Behavioral Health Center",             services: ["mental_health","substance_use","crisis"],                     address: "3100 Kensington Ave" },
  { id: "prov-temple-pc",   name: "Temple University Primary Care",                  services: ["primary_care","diabetes_management","chronic_pain"],           address: "3401 N Broad St" },
  { id: "prov-phr-housing", name: "Project HOME Reentry Housing",                    services: ["housing_assistance","reentry_services"],                      address: "1515 Fairmount Ave" },
  { id: "prov-wf-dev",      name: "Philadelphia Works Workforce Development",        services: ["workforce_development","job_training","credential_programs"], address: "1617 JFK Blvd" },
  { id: "prov-wc-dv",       name: "Women's Center of Montgomery County",             services: ["domestic_violence","mental_health","legal_aid"],              address: "100 S Broad St" },
  { id: "prov-va-med",      name: "Philadelphia VA Medical Center",                  services: ["primary_care","mental_health","chronic_pain","ptsd"],         address: "3900 Woodland Ave" },
  { id: "prov-act-team",    name: "Community ACT Team - PATH Program",               services: ["mental_health","housing_assistance","case_management"],       address: "810 Arch St" },
  { id: "prov-juv-mentor",  name: "Big Brothers Big Sisters - Philadelphia",          services: ["mentorship","youth_development","education_support"],         address: "230 S Broad St" },
],

// ============================================================================
// 7. JOBS — All 6 Job Openings
// ============================================================================
jobs: [
  { id: "job-cdl-b",          title: "Delivery Driver",              employer: "UPS Supply Chain",          wage_hr: 26, wage_yr: 54080, credentials: ["CDL-B"] },
  { id: "job-warehouse",      title: "Warehouse Associate",          employer: "Amazon PHL1",               wage_hr: 18, wage_yr: 37440, credentials: ["forklift"] },
  { id: "job-med-coder",      title: "Medical Coding Specialist",    employer: "Jefferson Health",          wage_hr: 22, wage_yr: 45760, credentials: ["comptia-a+"] },
  { id: "job-peer-recovery",  title: "Peer Recovery Specialist",     employer: "DBHIDS Philadelphia",      wage_hr: 18, wage_yr: 37440, credentials: ["cna"] },
  { id: "job-food-service",   title: "Food Service Worker",          employer: "Aramark - School District", wage_hr: 15, wage_yr: 31200, credentials: ["servsafe"] },
  { id: "job-phlebotomist",   title: "Phlebotomist",                 employer: "LabCorp Philadelphia",      wage_hr: 19, wage_yr: 39520, credentials: ["phlebotomy"] },
],

// ============================================================================
// 8. PROVISIONS — 70+ representative provisions from backend/seed.py
//    (Total in full DB: 5,126)
// ============================================================================
provisions: {
  totalInDB: 5126,
  domainOrder: { health: 0, civil_rights: 1, housing: 2, income: 3, education: 4, justice: 5 },
  typeWeights: { right: 1.0, protection: 0.95, obligation: 0.90, enforcement: 0.85 },
  records: [
    // --- HEALTH (30) ---
    { citation: "42 U.S.C. § 1396d(r)",                   title: "Medicaid EPSDT",                                domain: "health", provision_type: "right",       applies_when: { insurance: ["medicaid"], age: ["under_21"] } },
    { citation: "42 U.S.C. § 1396a(a)(10)(A)",            title: "Medicaid Mandatory Coverage Groups",            domain: "health", provision_type: "right",       applies_when: { income_level: ["below_133_fpl","below_100_fpl"], insurance: ["medicaid","none"], age: ["under_21","pregnant"] } },
    { citation: "42 U.S.C. § 1396a(a)(43)",               title: "Medicaid EPSDT Outreach",                       domain: "health", provision_type: "obligation",  applies_when: { insurance: ["medicaid"], age: ["under_21"] } },
    { citation: "42 CFR Part 438",                         title: "Medicaid Managed Care Protections",             domain: "health", provision_type: "protection",  applies_when: { insurance: ["medicaid_managed_care"] } },
    { citation: "42 U.S.C. § 1396n(c)",                   title: "HCBS Waiver",                                   domain: "health", provision_type: "right",       applies_when: { insurance: ["medicaid"], disability: ["physical","intellectual","developmental"], setting: ["community","home"] } },
    { citation: "42 U.S.C. § 1396n(i)",                   title: "Self-Directed Personal Assistance",             domain: "health", provision_type: "right",       applies_when: { insurance: ["medicaid"], disability: ["physical","intellectual","developmental"] } },
    { citation: "29 U.S.C. § 1185a",                      title: "MHPAEA Mental Health Parity",                   domain: "health", provision_type: "protection",  applies_when: { insurance: ["employer","marketplace"], condition: ["mental_health","substance_use"] } },
    { citation: "42 U.S.C. § 1395dd",                     title: "EMTALA",                                        domain: "health", provision_type: "right",       applies_when: { setting: ["emergency_department"], insurance: ["any","none"] } },
    { citation: "42 U.S.C. § 18022",                      title: "ACA Essential Health Benefits",                  domain: "health", provision_type: "right",       applies_when: { insurance: ["marketplace","individual","small_group"] } },
    { citation: "42 U.S.C. § 300gg-13",                   title: "ACA Preventive Services Without Cost-Sharing",  domain: "health", provision_type: "right",       applies_when: { insurance: ["marketplace","employer","individual"] } },
    { citation: "42 U.S.C. § 18116",                      title: "Section 1557 ACA Nondiscrimination",            domain: "health", provision_type: "protection",  applies_when: { insurance: ["any"], setting: ["healthcare_facility","insurance"] } },
    { citation: "42 CFR Part 2",                           title: "SUD Record Confidentiality",                    domain: "health", provision_type: "protection",  applies_when: { condition: ["substance_use"], setting: ["treatment_program"] } },
    { citation: "42 U.S.C. § 1395i-3",                    title: "Nursing Home Residents' Rights (Medicare)",      domain: "health", provision_type: "right",       applies_when: { setting: ["nursing_facility","skilled_nursing"], insurance: ["medicare","medicaid"] } },
    { citation: "42 U.S.C. § 1396r",                      title: "Nursing Facility Requirements (Medicaid)",       domain: "health", provision_type: "right",       applies_when: { setting: ["nursing_facility"], insurance: ["medicaid"] } },
    { citation: "42 U.S.C. § 1382(e)(1)(A)",              title: "Medicaid Eligibility for SSI Recipients",        domain: "health", provision_type: "right",       applies_when: { benefits: ["ssi"], insurance: ["medicaid"] } },
    { citation: "42 U.S.C. § 300gg-14",                   title: "ACA Dependent Coverage Until Age 26",            domain: "health", provision_type: "right",       applies_when: { age: ["under_26"], insurance: ["employer","marketplace","individual"] } },
    { citation: "42 U.S.C. § 300gg-3",                    title: "ACA No Preexisting Condition Exclusions",        domain: "health", provision_type: "protection",  applies_when: { insurance: ["marketplace","employer","individual"], condition: ["any_preexisting"] } },
    { citation: "42 U.S.C. § 1395(y)(b)",                 title: "Medicare for Disabled Under 65",                 domain: "health", provision_type: "right",       applies_when: { benefits: ["ssdi"], disability: ["any"], age: ["under_65"] } },
    { citation: "42 U.S.C. § 1396d(a)(4)(B)",             title: "Medicaid Family Planning Services",              domain: "health", provision_type: "right",       applies_when: { insurance: ["medicaid"], age: ["childbearing"] } },
    { citation: "42 U.S.C. § 1396a(a)(25)",               title: "Medicaid Payer of Last Resort",                  domain: "health", provision_type: "protection",  applies_when: { insurance: ["medicaid"] } },
    { citation: "42 U.S.C. § 1396a(e)(14)",               title: "Medicaid for Former Foster Youth",               domain: "health", provision_type: "right",       applies_when: { age: ["under_26"], background: ["former_foster_care"] } },
    { citation: "42 U.S.C. § 1396a(a)(10)(A)(i)(VIII)",   title: "Medicaid Expansion Under ACA",                  domain: "health", provision_type: "right",       applies_when: { income_level: ["below_138_fpl"], age: ["19_to_64"], insurance: ["none","medicaid"] } },
    { citation: "42 U.S.C. § 1396a(bb)",                  title: "FQHC Prospective Payment",                      domain: "health", provision_type: "right",       applies_when: { insurance: ["any","none"], income_level: ["any"] } },
    { citation: "45 CFR Parts 160 and 164",                title: "HIPAA Privacy and Security Rules",               domain: "health", provision_type: "protection",  applies_when: { setting: ["healthcare_facility","insurance","health_plan"] } },
    { citation: "42 U.S.C. § 1396d(a)(13)",               title: "Medicaid Rehabilitative Services",               domain: "health", provision_type: "right",       applies_when: { insurance: ["medicaid"], disability: ["physical","mental"] } },
    { citation: "42 U.S.C. § 1395x(dd)",                  title: "Medicare/Medicaid Hospice Benefits",             domain: "health", provision_type: "right",       applies_when: { insurance: ["medicare","medicaid"], condition: ["terminal_illness"] } },
    { citation: "42 U.S.C. § 1320a-7b(d)(1)",             title: "Anti-Kickback Statute",                          domain: "health", provision_type: "protection",  applies_when: { insurance: ["medicare","medicaid","tricare"] } },
    { citation: "42 U.S.C. § 256b",                       title: "340B Drug Pricing Program",                      domain: "health", provision_type: "right",       applies_when: { setting: ["fqhc","dsh_hospital","ryan_white_clinic"] } },
    { citation: "42 U.S.C. § 290bb-36",                   title: "Garrett Lee Smith Act Youth Suicide Prevention", domain: "health", provision_type: "right",       applies_when: { age: ["under_21","under_26"], condition: ["mental_health","suicide_risk"] } },
    { citation: "42 CFR § 435.4",                          title: "Medicaid Eligibility Definitions",               domain: "health", provision_type: "right",       applies_when: {} },
    // --- CIVIL RIGHTS (20+) ---
    { citation: "42 U.S.C. § 12132",                       title: "ADA Title II — Public Services",                domain: "civil_rights", provision_type: "protection",  applies_when: { disability: ["any"] } },
    { citation: "42 U.S.C. § 12182",                       title: "ADA Title III — Public Accommodations",         domain: "civil_rights", provision_type: "protection",  applies_when: { disability: ["any"] } },
    { citation: "29 U.S.C. § 794",                         title: "Section 504 Rehabilitation Act",                domain: "civil_rights", provision_type: "protection",  applies_when: { disability: ["any"], setting: ["federally_funded"] } },
    { citation: "42 U.S.C. § 2000d",                       title: "Title VI Civil Rights Act",                     domain: "civil_rights", provision_type: "protection",  applies_when: { race: ["any"] } },
    { citation: "42 U.S.C. § 3604",                        title: "Fair Housing Act — Discrimination",             domain: "civil_rights", provision_type: "protection",  applies_when: { housing: ["any"] } },
    // --- HOUSING ---
    { citation: "24 CFR § 982.1",                          title: "Section 8 HCV General Provisions",              domain: "housing", provision_type: "right",       applies_when: { income_level: ["below_50_ami"] } },
    { citation: "24 CFR § 91.5",                           title: "Consolidated Plan Definitions",                 domain: "housing", provision_type: "right",       applies_when: {} },
    { citation: "24 CFR § 578.3",                          title: "Continuum of Care Definitions",                 domain: "housing", provision_type: "right",       applies_when: { housing: ["homeless"] } },
    { citation: "24 CFR § 5.609",                          title: "Annual Income Determination",                   domain: "housing", provision_type: "right",       applies_when: {} },
    { citation: "24 CFR § 888.113",                        title: "Fair Market Rents",                             domain: "housing", provision_type: "right",       applies_when: {} },
    // --- INCOME ---
    { citation: "20 CFR § 416.110",                        title: "SSI Purpose",                                    domain: "income", provision_type: "right",       applies_when: { income_level: ["below_ssi_limit"], disability: ["any"] } },
    { citation: "20 CFR § 416.1205",                       title: "SSI Resource Limits",                            domain: "income", provision_type: "right",       applies_when: { income_level: ["below_ssi_limit"] } },
    { citation: "20 CFR § 404.315",                        title: "SSDI Child's Benefits",                          domain: "income", provision_type: "right",       applies_when: { benefits: ["ssdi"], age: ["under_18"] } },
    { citation: "45 CFR § 261.10",                         title: "TANF Purpose",                                   domain: "income", provision_type: "right",       applies_when: {} },
    { citation: "7 CFR § 273.2",                           title: "SNAP Application Processing",                    domain: "income", provision_type: "right",       applies_when: {} },
    { citation: "7 CFR § 273.9",                           title: "SNAP Income and Deductions",                     domain: "income", provision_type: "right",       applies_when: {} },
    { citation: "7 CFR § 246.7",                           title: "WIC Certification",                              domain: "income", provision_type: "right",       applies_when: { income_level: ["below_185_fpl"] } },
    // --- EDUCATION ---
    { citation: "34 CFR § 99.3",                           title: "FERPA Definitions",                              domain: "education", provision_type: "protection", applies_when: {} },
    { citation: "34 CFR § 300.320",                        title: "IDEA IEP Definition",                            domain: "education", provision_type: "right",      applies_when: { disability: ["any"], age: ["under_21"] } },
    { citation: "20 U.S.C. § 1400",                        title: "IDEA General Provisions",                        domain: "education", provision_type: "right",      applies_when: { disability: ["any"], age: ["under_21"] } },
    // --- JUSTICE ---
    { citation: "28 CFR § 115.5",                          title: "PREA Definitions",                               domain: "justice", provision_type: "protection",   applies_when: { setting: ["correctional_facility"] } },
    { citation: "28 CFR § 524.11",                         title: "BOP Classification Procedures",                  domain: "justice", provision_type: "right",        applies_when: { setting: ["federal_prison"] } },
    { citation: "42 CFR Part 2 § 2.12",                    title: "42 CFR Part 2 Penalties",                        domain: "justice", provision_type: "enforcement",   applies_when: { condition: ["substance_use"] } },
    { citation: "45 CFR § 164.510",                        title: "HIPAA Uses and Disclosures",                     domain: "justice", provision_type: "protection",   applies_when: { setting: ["healthcare_facility"] } },
  ],
},

// ============================================================================
// 9. COST DATA — All 35+ cost points from baths-engine/data/costs.py
// ============================================================================
costData: [
  // Healthcare
  { category: "healthcare", metric: "Medicare per enrollee spending",              value: 15091,          unit: "$/year",  source_year: "2022" },
  { category: "healthcare", metric: "Medicaid per enrollee spending",              value: 8436,           unit: "$/year",  source_year: "2022" },
  { category: "healthcare", metric: "Medicaid PMPM — aged/disabled",               value: 1677,           unit: "$/month", source_year: "2022" },
  { category: "healthcare", metric: "Medicaid PMPM — children",                    value: 304,            unit: "$/month", source_year: "2022" },
  { category: "healthcare", metric: "Medicaid PMPM — expansion adults",            value: 619,            unit: "$/month", source_year: "2022" },
  { category: "healthcare", metric: "Uninsured ER visit average charge",           value: 2246,           unit: "$/visit", source_year: "2020" },
  { category: "healthcare", metric: "Homeless individuals annual healthcare",      value: 18500,          unit: "$/year",  source_year: "2023" },
  { category: "healthcare", metric: "High-utilizer ER annual cost",                value: 41274,          unit: "$/year",  source_year: "2022" },
  { category: "healthcare", metric: "Behavioral health — SMI Medicaid annual",     value: 22872,          unit: "$/year",  source_year: "2022" },
  // Incarceration
  { category: "incarceration", metric: "Average annual federal prisoner",           value: 39158,          unit: "$/year",  source_year: "2022" },
  { category: "incarceration", metric: "Average annual state prisoner (national)",  value: 45771,          unit: "$/year",  source_year: "2023" },
  { category: "incarceration", metric: "Annual cost per prisoner — Pennsylvania",   value: 51115,          unit: "$/year",  source_year: "2023" },
  { category: "incarceration", metric: "Annual cost per prisoner — New York",       value: 69355,          unit: "$/year",  source_year: "2023" },
  { category: "incarceration", metric: "Annual cost per prisoner — California",     value: 132860,         unit: "$/year",  source_year: "2023" },
  { category: "incarceration", metric: "Daily cost per local jail bed",             value: 166,            unit: "$/day",   source_year: "2023" },
  { category: "incarceration", metric: "Total US incarceration spending",           value: 182000000000,   unit: "$/year",  source_year: "2023" },
  // Shelter
  { category: "shelter", metric: "Emergency shelter cost/night — national",         value: 56,             unit: "$/night", source_year: "2023" },
  { category: "shelter", metric: "Emergency shelter cost/night — NYC",              value: 132,            unit: "$/night", source_year: "2023" },
  { category: "shelter", metric: "Annual cost per chronically homeless",            value: 35578,          unit: "$/year",  source_year: "2023" },
  { category: "shelter", metric: "Permanent supportive housing annual",             value: 21268,          unit: "$/year",  source_year: "2023" },
  // Housing
  { category: "housing", metric: "Fair Market Rent — 2BR national median",          value: 1428,           unit: "$/month", source_year: "2024" },
  { category: "housing", metric: "Fair Market Rent — 2BR Philadelphia MSA",         value: 1431,           unit: "$/month", source_year: "2024" },
  { category: "housing", metric: "Housing Choice Voucher — avg monthly HAP",        value: 898,            unit: "$/month", source_year: "2023" },
  { category: "housing", metric: "Households paying >50% income on rent",           value: 12100000,       unit: "households", source_year: null },
  // Fragmentation
  { category: "fragmentation", metric: "Emergency room visit (avoidable)",          value: 2580,           unit: "$/visit", source_year: "HCUP" },
  { category: "fragmentation", metric: "Inpatient psychiatric stay",                value: 1950,           unit: "$/day",   source_year: "HCUP" },
  { category: "fragmentation", metric: "Jail booking (avoidable)",                  value: 150,            unit: "$/day",   source_year: "Vera" },
  { category: "fragmentation", metric: "Shelter night (avoidable)",                 value: 68,             unit: "$/night", source_year: "HUD" },
  // Education
  { category: "education", metric: "Per-pupil expenditure — Philadelphia",          value: 16400,          unit: "$/year",  source_year: "FY2024" },
  { category: "education", metric: "Special education per pupil",                   value: 29000,          unit: "$/year",  source_year: "2023" },
  // Food
  { category: "food", metric: "Max monthly SNAP FY2024 family of 4",               value: 973,            unit: "$/month", source_year: "2024" },
  // SSI
  { category: "income", metric: "SSI monthly rate — individual (2024)",             value: 943,            unit: "$/month", source_year: "2024" },
  { category: "income", metric: "SSI monthly rate — couple (2024)",                 value: 1415,           unit: "$/month", source_year: "2024" },
  { category: "income", metric: "SSI resource limit — individual",                  value: 2000,           unit: "$",       source_year: "frozen since 1989" },
  { category: "income", metric: "SSI recipients total",                             value: 7400000,        unit: "persons", source_year: "2023" },
],

// ============================================================================
// 10. GOV SYSTEMS — All 31 systems from domes-datamap
// ============================================================================
govSystems: [
  // Health (8)
  { id: "mmis",          name: "Medicaid Management Information System",      acronym: "MMIS",  agency: "CMS",                domain: "health",        data_standard: "HL7/FHIR",   api_availability: "limited", privacy_law: "HIPAA",              is_federal: false },
  { id: "mco",           name: "Managed Care Organization Claims",            acronym: "MCO",   agency: "State Medicaid",     domain: "health",        data_standard: "HL7/FHIR",   api_availability: "limited", privacy_law: "HIPAA",              is_federal: false },
  { id: "bha",           name: "Behavioral Health Authority",                  acronym: "BHA",   agency: "State BHA",          domain: "health",        data_standard: "HL7 CCD",    api_availability: "none",    privacy_law: "42 CFR Part 2",      is_federal: false },
  { id: "cmhc_ehr",      name: "Community Mental Health Center EHR",           acronym: "CMHC",  agency: "State CMHC",         domain: "health",        data_standard: "HL7/FHIR",   api_availability: "limited", privacy_law: "42 CFR Part 2",      is_federal: false },
  { id: "hie",           name: "Health Information Exchange",                  acronym: "HIE",   agency: "State HIE",          domain: "health",        data_standard: "HL7/FHIR",   api_availability: "full",    privacy_law: "HIPAA",              is_federal: false },
  { id: "pdmp",          name: "Prescription Drug Monitoring Program",         acronym: "PDMP",  agency: "State DEA-affiliated",domain: "health",        data_standard: "PMIX/NIEM",  api_availability: "limited", privacy_law: "HIPAA",              is_federal: false },
  { id: "va_system",     name: "Veterans Affairs Health System",               acronym: "VA",    agency: "VA",                 domain: "health",        data_standard: "HL7/FHIR",   api_availability: "full",    privacy_law: "HIPAA",              is_federal: true },
  { id: "vital_records", name: "Vital Records",                               acronym: "VR",    agency: "State Health Dept",  domain: "health",        data_standard: "HL7 CDA",    api_availability: "none",    privacy_law: "HIPAA",              is_federal: false },
  // Justice (5)
  { id: "doc",               name: "Department of Corrections",                 acronym: "DOC",  agency: "State DOC",          domain: "justice",       data_standard: "varies",     api_availability: "none",    privacy_law: "HIPAA (limited)",    is_federal: false },
  { id: "cjis",              name: "Criminal Justice Information Services",      acronym: "CJIS", agency: "FBI/State",          domain: "justice",       data_standard: "CJIS",       api_availability: "none",    privacy_law: "CJIS Security Policy", is_federal: true },
  { id: "probation_parole",  name: "Probation & Parole System",                 acronym: "P&P",  agency: "State Courts",       domain: "justice",       data_standard: "varies",     api_availability: "none",    privacy_law: "varies",             is_federal: false },
  { id: "court_cms",         name: "Court Case Management System",              acronym: "CMS",  agency: "State Courts",       domain: "justice",       data_standard: "varies",     api_availability: "none",    privacy_law: "varies",             is_federal: false },
  { id: "sacwis",            name: "Statewide Automated Child Welfare Info System", acronym: "SACWIS", agency: "State DCFS",   domain: "child_welfare", data_standard: "varies",     api_availability: "none",    privacy_law: "CAPTA / FERPA",      is_federal: false },
  // Housing (2)
  { id: "hmis",      name: "Homeless Management Information System",            acronym: "HMIS",  agency: "HUD",               domain: "housing",       data_standard: "HMIS CSV",   api_availability: "limited", privacy_law: "HUD HMIS Privacy",   is_federal: false },
  { id: "pha",       name: "Public Housing Authority",                          acronym: "PHA",   agency: "Local PHA",         domain: "housing",       data_standard: "varies",     api_availability: "none",    privacy_law: "Privacy Act",        is_federal: false },
  // Income (4)
  { id: "ssa",             name: "Social Security Administration",               acronym: "SSA",  agency: "SSA",               domain: "income",        data_standard: "proprietary",api_availability: "limited", privacy_law: "Privacy Act",        is_federal: true },
  { id: "snap_ebt",       name: "SNAP/EBT Benefits",                            acronym: "SNAP", agency: "State SNAP",        domain: "income",        data_standard: "varies",     api_availability: "none",    privacy_law: "Privacy Act",        is_federal: false },
  { id: "tanf",           name: "Temporary Assistance for Needy Families",       acronym: "TANF", agency: "State TANF",        domain: "income",        data_standard: "varies",     api_availability: "none",    privacy_law: "Privacy Act",        is_federal: false },
  { id: "unemployment",   name: "Unemployment Insurance",                       acronym: "UI",   agency: "State Labor",       domain: "income",        data_standard: "varies",     api_availability: "none",    privacy_law: "Privacy Act",        is_federal: false },
  // Education (2)
  { id: "slds",           name: "Statewide Longitudinal Data System",            acronym: "SLDS", agency: "State Ed Dept",     domain: "education",     data_standard: "CEDS/EdFi",  api_availability: "limited", privacy_law: "FERPA",              is_federal: false },
  { id: "iep_system",     name: "Special Education / IEP System",               acronym: "IEP",  agency: "State Ed Dept",     domain: "education",     data_standard: "varies",     api_availability: "none",    privacy_law: "IDEA / FERPA",       is_federal: false },
  // baths-engine extended systems (from data/systems.py)
  { id: "SSA_NUMIDENT",   name: "Social Security Numident",                     acronym: "NUM",  agency: "SSA",               domain: "income",        data_standard: "proprietary",api_availability: "none",    privacy_law: "Privacy Act",        is_federal: true },
  { id: "SSA_MBR",        name: "Master Beneficiary Record",                    acronym: "MBR",  agency: "SSA",               domain: "income",        data_standard: "proprietary",api_availability: "none",    privacy_law: "Privacy Act",        is_federal: true },
  { id: "SSA_SSR",        name: "Supplemental Security Record",                 acronym: "SSR",  agency: "SSA",               domain: "income",        data_standard: "proprietary",api_availability: "none",    privacy_law: "Privacy Act",        is_federal: true },
  { id: "CMS_MMIS",       name: "Medicaid Management Information System",       acronym: "MMIS", agency: "CMS (state-operated)",domain: "health",      data_standard: "HL7/FHIR",   api_availability: "limited", privacy_law: "HIPAA",              is_federal: false },
  { id: "CMS_MEDICARE_EDB",name: "Medicare Enrollment Database",                acronym: "EDB",  agency: "CMS",               domain: "health",        data_standard: "proprietary",api_availability: "limited", privacy_law: "Privacy Act",        is_federal: true },
  { id: "CMS_CCW",        name: "Chronic Conditions Data Warehouse",            acronym: "CCW",  agency: "CMS",               domain: "health",        data_standard: "proprietary",api_availability: "limited", privacy_law: "HIPAA",              is_federal: true },
  { id: "HUD_IMS_PIC",    name: "Inventory Management System / PIC",            acronym: "PIC",  agency: "HUD",               domain: "housing",       data_standard: "proprietary",api_availability: "limited", privacy_law: "Privacy Act",        is_federal: true },
  { id: "HUD_HMIS",       name: "Homeless Management Information System",       acronym: "HMIS", agency: "HUD (locally operated)",domain: "housing",   data_standard: "HMIS CSV",   api_availability: "limited", privacy_law: "HUD HMIS Privacy",   is_federal: false },
  { id: "IRS_IMF",        name: "Individual Master File",                       acronym: "IMF",  agency: "IRS",               domain: "income",        data_standard: "proprietary",api_availability: "none",    privacy_law: "IRC § 6103",         is_federal: true },
],

// ============================================================================
// 11. SYSTEM CONNECTIONS (representative)
// ============================================================================
systemConnections: [
  { source: "mmis",  target: "mco",          direction: "bidirectional", format: "HL7/FHIR",  governing_agreement: "BAA", reliability: "high" },
  { source: "mmis",  target: "hie",          direction: "bidirectional", format: "HL7/FHIR",  governing_agreement: "BAA", reliability: "medium" },
  { source: "mmis",  target: "bha",          direction: "unidirectional",format: "HL7 CCD",   governing_agreement: "QSOA", reliability: "low" },
  { source: "ssa",   target: "mmis",         direction: "unidirectional",format: "batch",      governing_agreement: "IDSA", reliability: "high" },
  { source: "hie",   target: "pdmp",         direction: "bidirectional", format: "PMIX",       governing_agreement: "BAA", reliability: "medium" },
  { source: "doc",   target: "medicaid",     direction: "blocked",       format: "none",       governing_agreement: "none", reliability: "none" },
  { source: "sacwis",target: "slds",         direction: "blocked",       format: "none",       governing_agreement: "none", reliability: "none" },
  { source: "hmis",  target: "pha",          direction: "unidirectional",format: "CSV",        governing_agreement: "MOU",  reliability: "low" },
],

// ============================================================================
// 12. GAPS — Data sharing gaps (representative)
// ============================================================================
gaps: [
  { system_a: "bha",   system_b: "mmis",  barrier_type: "legal",     severity: "critical", consent_closable: false, cost_to_bridge: "$500K-1M",   barrier_law: "42 CFR Part 2",  impact: "SUD records invisible to Medicaid — duplicated services, treatment gaps" },
  { system_a: "doc",   system_b: "mmis",  barrier_type: "legal",     severity: "critical", consent_closable: false, cost_to_bridge: "$1M-2M",     barrier_law: "Medicaid Inmate Exclusion Policy", impact: "Medicaid terminates at incarceration — 45-day re-enrollment gap" },
  { system_a: "sacwis",system_b: "slds",  barrier_type: "legal",     severity: "high",     consent_closable: true,  cost_to_bridge: "$200K-500K", barrier_law: "FERPA",          impact: "Foster children change schools 1.6x/yr; schools cannot see CW data" },
  { system_a: "bha",   system_b: "doc",   barrier_type: "legal",     severity: "critical", consent_closable: true,  cost_to_bridge: "$200K-500K", barrier_law: "42 CFR Part 2",  impact: "3-week psychiatric medication gap at booking" },
  { system_a: "hmis",  system_b: "pha",   barrier_type: "technical", severity: "high",     consent_closable: false, cost_to_bridge: "$500K-1M",   barrier_law: "HUD HMIS Privacy", impact: "2-year housing waitlist while accumulating $50K+ in ER costs" },
  { system_a: "hie",   system_b: "bha",   barrier_type: "consent",   severity: "high",     consent_closable: true,  cost_to_bridge: "$100K-200K", barrier_law: "42 CFR Part 2",  impact: "ER cannot see SUD treatment records — repeated assessments" },
],

// ============================================================================
// 13. BRIDGES — Bridge solutions (representative)
// ============================================================================
bridges: [
  { gap_systems: ["bha","mmis"],  bridge_type: "consent",   title: "42 CFR Part 2 Consent Form",        priority_score: 9.2, impact_score: 9.0, effort_score: 2.0, estimated_cost: "$50K-100K", status: "proposed" },
  { gap_systems: ["hie","bha"],   bridge_type: "consent",   title: "HIPAA/42 CFR Cross-Consent",        priority_score: 8.5, impact_score: 8.5, effort_score: 2.0, estimated_cost: "$50K-100K", status: "proposed" },
  { gap_systems: ["sacwis","slds"],bridge_type: "legal",    title: "FERPA Data Sharing Agreement",      priority_score: 7.0, impact_score: 7.5, effort_score: 3.0, estimated_cost: "$200K-500K", status: "proposed" },
  { gap_systems: ["doc","mmis"],  bridge_type: "legal",     title: "Medicaid Suspension (not Termination) Policy", priority_score: 8.0, impact_score: 9.5, effort_score: 5.0, estimated_cost: "$1M-2M", status: "proposed" },
  { gap_systems: ["hmis","pha"],  bridge_type: "technical", title: "HMIS-PHA Real-Time Data Exchange",  priority_score: 6.5, impact_score: 8.0, effort_score: 5.0, estimated_cost: "$500K-1M", status: "proposed" },
],

// ============================================================================
// 14. PARCELS — 14 Real Philadelphia Parcels + 10 THAUMA/OS Demo Spaces
// ============================================================================
parcels: {
  real: [
    { parcel_id: "888000100", address: "1500 Market St, 19102",         owner: "Liberty Property Trust",     zoning: "CMX-5",   sqft: 43560,  vacant: false, value: 160000000 },
    { parcel_id: "888001200", address: "801 Market St, 19107",          owner: "City of Philadelphia",       zoning: "CMX-5",   sqft: 65000,  vacant: true,  value: 18500000 },
    { parcel_id: "432100100", address: "2901 N Broad St, 19132",        owner: "Temple University",          zoning: "CMX-3",   sqft: 22000,  vacant: false, value: 17200000 },
    { parcel_id: "432200300", address: "3100 N 22nd St, 19132",         owner: "Philadelphia Land Bank",     zoning: "RSA-5",   sqft: 1440,   vacant: true,  value: 14400 },
    { parcel_id: "371130500", address: "2500 Germantown Ave, 19133",    owner: "Private Individual",         zoning: "CMX-2",   sqft: 2100,   vacant: false, value: 66000 },
    { parcel_id: "271040600", address: "5200 Market St, 19139",         owner: "Private LLC",                zoning: "CMX-2.5", sqft: 8500,   vacant: false, value: 520000 },
    { parcel_id: "271150200", address: "5601 Vine St, 19139",           owner: "Philadelphia Land Bank",     zoning: "RSA-5",   sqft: 1200,   vacant: true,  value: 12000 },
    { parcel_id: "021086500", address: "1100 S Broad St, 19146",        owner: "Live Nation Entertainment",  zoning: "SP-STA",  sqft: 180000, vacant: false, value: 57000000 },
    { parcel_id: "026107300", address: "1400 Passyunk Ave, 19147",      owner: "Private Individual",         zoning: "CMX-2",   sqft: 1600,   vacant: false, value: 308000 },
    { parcel_id: "314010600", address: "2800 Kensington Ave, 19134",    owner: "City of Philadelphia",       zoning: "IRMX",    sqft: 45000,  vacant: true,  value: 450000 },
    { parcel_id: "432200400", address: "3200 N 22nd St, 19132",         owner: "Philadelphia Land Bank",     zoning: "RSA-5",   sqft: 1380,   vacant: true,  value: 13800 },
    { parcel_id: "271150300", address: "5605 Vine St, 19139",           owner: "Philadelphia Land Bank",     zoning: "RSA-5",   sqft: 1150,   vacant: true,  value: 11500 },
    { parcel_id: "341040200", address: "3500 N Broad St, 19140",        owner: "City of Philadelphia",       zoning: "CMX-3",   sqft: 18000,  vacant: true,  value: 850000 },
    { parcel_id: "881000100", address: "1901 JFK Blvd, 19103",          owner: "Brandywine Realty",          zoning: "CMX-5",   sqft: 52000,  vacant: false, value: 95000000 },
  ],
  thaumaOS: [
    { id: "nbc-001", name: "North Broad Concourse",         address: "N Broad & W Lehigh (below grade)", sqft: 48000,  viability: 0.97, notes: "Founding SPHERE; underground BSL concourse" },
    { id: "phl-002", name: "Germantown Rail Yard",          address: "100 E Chelten Ave",                sqft: 85000,  viability: 0.88, notes: "Brownfield remediated" },
    { id: "phl-003", name: "Point Breeze Triangle",         address: "1600 S 21st St",                   sqft: 12000,  viability: 0.72, notes: "" },
    { id: "phl-004", name: "Kensington Viaduct Lot",        address: "2900 Kensington Ave",              sqft: 22000,  viability: 0.81, notes: "" },
    { id: "phl-005", name: "Strawberry Mansion Reservoir",   address: "3200 N 33rd St",                   sqft: 35000,  viability: 0.79, notes: "" },
    { id: "phl-006", name: "Cobbs Creek Gateway",           address: "6300 Market St",                   sqft: 18000,  viability: 0.74, notes: "Flood zone adjacent" },
    { id: "phl-007", name: "Navy Yard East Pad",            address: "5100 S Broad St",                  sqft: 120000, viability: 0.91, notes: "PIDC; industrial remediated" },
    { id: "phl-008", name: "West Philly Innovation Lot",    address: "4600 Market St",                   sqft: 9500,   viability: 0.85, notes: "UCSC owned; 50ft from transit" },
    { id: "phl-009", name: "Hunting Park Corner",           address: "3700 N Broad St",                  sqft: 7500,   viability: 0.68, notes: "Philadelphia Land Bank" },
    { id: "phl-010", name: "Eastwick Meadow",               address: "7400 Lindbergh Blvd",              sqft: 280000, viability: null,  notes: "City of Philadelphia" },
  ],
},

// ============================================================================
// 15. ZONING REFERENCE
// ============================================================================
zoningReference: [
  { code: "CMX-1",  name: "Neighborhood Commercial Mixed-Use",      max_height_ft: 38,  max_far: 2.0 },
  { code: "CMX-2",  name: "Community Commercial Mixed-Use",          max_height_ft: 38,  max_far: 3.0 },
  { code: "CMX-2.5",name: "Community Commercial Mixed-Use (Enhanced)",max_height_ft: 55,  max_far: 3.5 },
  { code: "CMX-3",  name: "Center City Commercial Mixed-Use",        max_height_ft: 65,  max_far: 5.0 },
  { code: "CMX-4",  name: "Center City Core Commercial Mixed-Use",   max_height_ft: null, max_far: 12.0 },
  { code: "CMX-5",  name: "Center City Core — No Height Limit",      max_height_ft: null, max_far: 16.0 },
  { code: "RSA-5",  name: "Residential Single-Family Attached",      max_height_ft: 38,  max_far: 2.5 },
  { code: "RM-1",   name: "Residential Multi-Family",                max_height_ft: 55,  max_far: 3.0 },
  { code: "I-1",    name: "Light Industrial",                        max_height_ft: 45,  max_far: 2.0 },
  { code: "I-2",    name: "Medium Industrial",                       max_height_ft: 65,  max_far: 3.0 },
  { code: "IRMX",   name: "Industrial Residential Mixed-Use",        max_height_ft: 65,  max_far: 3.5 },
  { code: "SP-STA", name: "Special Purpose — Stadium",               max_height_ft: null, max_far: null },
  { code: "SP-ENT", name: "Special Purpose — Entertainment",         max_height_ft: null, max_far: null },
],

// ============================================================================
// 16. MATERIAL SYSTEMS — All 9 types with transition times
// ============================================================================
materialSystems: [
  { type: "acoustic_metamaterial",  transition_time_min_s: 0.025,  transition_time_max_s: 60 },
  { type: "haptic_surface",         transition_time_min_s: 0.025,  transition_time_max_s: 5 },
  { type: "olfactory_synthesis",    transition_time_min_s: 600,    transition_time_max_s: 1200 },
  { type: "electrochromic_surface", transition_time_min_s: 1,      transition_time_max_s: 5 },
  { type: "projection_mapping",     transition_time_min_s: 0.1,    transition_time_max_s: 10 },
  { type: "phase_change_panel",     transition_time_min_s: 300,    transition_time_max_s: 1800 },
  { type: "shape_memory_element",   transition_time_min_s: 300,    transition_time_max_s: 3600 },
  { type: "4d_printed_deployable",  transition_time_min_s: 1800,   transition_time_max_s: 3600 },
  { type: "bioluminescent_coating", transition_time_min_s: 0,      transition_time_max_s: 0 },
],

// ============================================================================
// 17. COORDINATION MODELS — 10 from domes-architect + 8 from baths-engine
// ============================================================================
coordinationModels: {
  domesArchitect: [
    { id: 1,  name: "Accountable Care Organization",                    abbreviation: "ACO",     category: "managed_care",     budget_range: { min: 5000000,  max: 500000000, unit: "annual" }, timeline: "12-18 months", evidence_rating: "strong",   political_feasibility: "moderate" },
    { id: 2,  name: "Health Home",                                      abbreviation: "HH",      category: "managed_care",     budget_range: { min: 1000000,  max: 50000000,  unit: "annual" }, timeline: "9-15 months",  evidence_rating: "moderate", political_feasibility: "high" },
    { id: 3,  name: "Program of All-Inclusive Care for the Elderly",     abbreviation: "PACE",    category: "managed_care",     budget_range: { min: 3000000,  max: 80000000,  unit: "annual" }, timeline: "18-36 months", evidence_rating: "strong",   political_feasibility: "moderate" },
    { id: 4,  name: "Wraparound / WRAP",                                abbreviation: "WRAP",    category: "community_based",  budget_range: { min: 500000,   max: 20000000,  unit: "annual" }, timeline: "6-12 months",  evidence_rating: "strong",   political_feasibility: "high" },
    { id: 5,  name: "Coordinated Care Resource / Care Coordination Ring",abbreviation: "CCR",     category: "community_based",  budget_range: { min: 200000,   max: 5000000,   unit: "annual" }, timeline: "3-6 months",   evidence_rating: "moderate", political_feasibility: "high" },
    { id: 6,  name: "Managed Care Organization",                        abbreviation: "MCO",     category: "managed_care",     budget_range: { min: 50000000, max: 5000000000,unit: "annual" }, timeline: "18-24 months", evidence_rating: "strong",   political_feasibility: "moderate" },
    { id: 7,  name: "Community Health Worker Hub",                       abbreviation: "CHW Hub", category: "community_based",  budget_range: { min: 300000,   max: 8000000,   unit: "annual" }, timeline: "3-6 months",   evidence_rating: "moderate", political_feasibility: "high" },
    { id: 8,  name: "Social Impact Bond",                               abbreviation: "SIB",     category: "specialized",      budget_range: { min: 2000000,  max: 50000000,  unit: "project" },timeline: "12-24 months", evidence_rating: "emerging", political_feasibility: "moderate" },
    { id: 9,  name: "Dual Special Needs Plan (Enhanced)",               abbreviation: "DSNP+",   category: "managed_care",     budget_range: { min: 20000000, max: 2000000000,unit: "annual" }, timeline: "18-24 months", evidence_rating: "moderate", political_feasibility: "moderate" },
    { id: 10, name: "Cross-System Data Integration Hub",                abbreviation: "CDIH",    category: "hybrid",           budget_range: { min: 1000000,  max: 30000000,  unit: "annual" }, timeline: "12-24 months", evidence_rating: "emerging", political_feasibility: "moderate" },
  ],
  bathsEngine: [
    { id: "hub_spoke",              name: "Hub-and-Spoke (Centralized Intake)",  savings_pct: 15, implementation_cost: "medium", timeline: "12-18 months", real_examples: ["Camden Coalition","Hennepin Health","Central City Concern"], dome_dimensions: ["healthcare","housing","income"] },
    { id: "shared_care_plan",       name: "Shared Care Plan (Person-Centered)",   savings_pct: 22, implementation_cost: "high",   timeline: "18-24 months", real_examples: ["Vermont Blueprint","Oregon CCO","Massachusetts MBHP"], dome_dimensions: ["healthcare","housing","income","justice","education"] },
    { id: "data_trust",             name: "Data Trust (Governed Sharing)",         savings_pct: 12, implementation_cost: "high",   timeline: "24-36 months", real_examples: ["Allegheny County DHS","NYC MODA","Chicago DFSS"], dome_dimensions: ["data_privacy","interoperability","healthcare"] },
    { id: "categorical_auto_enroll",name: "Categorical Auto-Enrollment",          savings_pct: 18, implementation_cost: "low",    timeline: "6-12 months",  real_examples: ["Louisiana Express Lane","Massachusetts MassHealth","Michigan Healthy Kids"], dome_dimensions: ["income","healthcare","food"] },
    { id: "community_health_worker",name: "Community Health Worker Navigation",   savings_pct: 10, implementation_cost: "low",    timeline: "3-6 months",   real_examples: ["Penn Center for CHW","IMPaCT","Partners in Health"], dome_dimensions: ["healthcare","housing"] },
    { id: "health_home",            name: "Medicaid Health Home (§ 2703)",         savings_pct: 20, implementation_cost: "medium", timeline: "12-18 months", real_examples: ["Missouri Health Home","New York Health Home","Rhode Island"], dome_dimensions: ["healthcare","income","housing","justice"] },
    { id: "social_impact_bond",     name: "Social Impact Bond / Pay for Success", savings_pct: 25, implementation_cost: "high",   timeline: "18-30 months", real_examples: ["Rikers Island SIB","Massachusetts Juvenile Justice","Denver SIB"], dome_dimensions: ["justice","healthcare","housing","employment"] },
    { id: "braided_funding",        name: "Braided/Blended Funding",              savings_pct: 15, implementation_cost: "medium", timeline: "12-24 months", real_examples: ["California Whole Person Care","Colorado RCCO","Washington HCA"], dome_dimensions: ["healthcare","housing","income","employment","education"] },
  ],
  budgetBreakdown: { personnel: 0.45, technology: 0.15, operations: 0.12, provider_payments: 0.15, administration: 0.08, contingency: 0.05 },
},

// ============================================================================
// 18. FLOURISHING DOMAINS — 12 domains in 3 layers
// ============================================================================
flourishingDomains: {
  foundation: [
    { id: "safety_security",        name: "Safety & Security",          theme: "Physical safety, stable housing, legal protection" },
    { id: "economic_wellbeing",     name: "Economic Wellbeing",         theme: "Income, assets, financial stability" },
    { id: "physical_health",        name: "Physical Health",            theme: "Medical care, nutrition, environment" },
    { id: "mental_emotional_health",name: "Mental & Emotional Health",  theme: "Psychological wellbeing, emotional regulation" },
  ],
  aspiration: [
    { id: "belonging_community",    name: "Belonging & Community",      theme: "Social connection, relationships, community" },
    { id: "learning_growth",        name: "Learning & Growth",          theme: "Education, skills, intellectual development" },
    { id: "creative_expression",    name: "Creative Expression",        theme: "Arts, culture, creativity" },
    { id: "civic_political_voice",  name: "Civic & Political Voice",    theme: "Participation, rights, representation" },
    { id: "meaningful_work",        name: "Meaningful Work",            theme: "Vocation, purpose, contribution" },
  ],
  transcendence: [
    { id: "spiritual_existential",  name: "Spiritual & Existential",    theme: "Meaning, purpose, faith" },
    { id: "ecological_connection",  name: "Ecological Connection",      theme: "Relationship with nature, environment" },
    { id: "legacy_impact",          name: "Legacy & Impact",            theme: "Contribution to future generations" },
  ],
  scoringFormula: "composite = min(scores) × 0.6 + average(scores) × 0.4",
},

// ============================================================================
// 19. PHILOSOPHICAL FRAMEWORKS — All 6
// ============================================================================
philosophicalFrameworks: [
  { id: "eudaimonia",          name: "Aristotelian Flourishing",       thinker: "Aristotle",              core_concept: "The good life as activity of the soul in accordance with virtue", key_principles: ["Practical wisdom (phronesis)","Moral virtue through habit","The mean between extremes","Community as essential to flourishing"] },
  { id: "capability_approach", name: "Human Capabilities Framework",   thinker: "Amartya Sen & Martha Nussbaum", core_concept: "Freedom to achieve well-being is a matter of what people are able to do and become", key_principles: ["10 Central Capabilities","Threshold for human dignity","Functioning vs. capability distinction","Political obligation to secure capabilities"] },
  { id: "ubuntu",              name: "I Am Because We Are",            thinker: "Desmond Tutu",           core_concept: "A person is a person through other persons — interconnected humanity", key_principles: ["Communal personhood","Shared humanity","Reconciliation over retribution","Collective flourishing"] },
  { id: "interdependence",     name: "Interbeing / Non-Separation",    thinker: "Thich Nhat Hanh",        core_concept: "Nothing exists by itself — everything inter-is", key_principles: ["Interbeing","Mindful awareness","Engaged Buddhism","Non-dualism"] },
  { id: "cura_personalis",     name: "Care of the Whole Person",       thinker: "Ignatius of Loyola",     core_concept: "Holistic care attending to body, mind, and spirit of each individual", key_principles: ["Individual attention","Discernment","Magis (the greater good)","Finding God in all things"] },
  { id: "relational_worldview",name: "Braided Sweetgrass / Reciprocity",thinker: "Robin Wall Kimmerer",   core_concept: "Reciprocal relationship with the living world — gratitude as foundation", key_principles: ["Gratitude as worldview","Reciprocity with nature","Indigenous ecological knowledge","Gift economy"] },
],

// ============================================================================
// 20. FINANCE MODELS — All 6 flourishing finance models
// ============================================================================
financeModels: [
  { id: "sovereign_wealth",       name: "Sovereign Wealth / Public Trust",     per_person_investment: 14200 },
  { id: "public_finance",         name: "Public Finance & Taxation",            per_person_investment: 22800 },
  { id: "impact_investing",       name: "Impact Investing",                     per_person_investment: 5400 },
  { id: "cooperative_economics",  name: "Cooperative Economics",                per_person_investment: 8600 },
  { id: "ubi_ubs",                name: "Universal Basic Income + Services",    per_person_investment: 18000 },
  { id: "philanthropic",          name: "Philanthropic",                        per_person_investment: 3200 },
],

// ============================================================================
// 21. NEW INSTRUMENTS — 3 Novel Financial Instruments
// ============================================================================
newInstruments: [
  { id: "flourishing_bonds",       name: "Flourishing Bonds",          description: "Outcome-based bonds tied to flourishing index" },
  { id: "flourishing_index_fund",  name: "Flourishing Index Fund",     description: "Investment fund tracking flourishing outcomes" },
  { id: "community_wealth_engines",name: "Community Wealth Engines",   description: "Local cooperative wealth-building vehicles" },
],

// ============================================================================
// 22. AI TEAMMATES — All 12 from domes-lab
// ============================================================================
aiTeammates: [
  { slug: "fiscal-alchemist",       name: "The Fiscal Alchemist",         title: "Creative Finance Director",            domain: "finance" },
  { slug: "impact-investor",        name: "The Impact Investor",          title: "Social ROI Specialist",                domain: "investment" },
  { slug: "data-inventor",          name: "The Data Inventor",            title: "Data Systems Architect",               domain: "data" },
  { slug: "tech-futurist",          name: "The Tech Futurist",            title: "Emerging Tech Strategist",             domain: "technology" },
  { slug: "legislative-inventor",   name: "The Legislative Inventor",     title: "Policy Innovation Lead",               domain: "policy" },
  { slug: "regulatory-hacker",      name: "The Regulatory Hacker",        title: "Compliance Innovation Specialist",     domain: "regulation" },
  { slug: "service-designer",       name: "The Service Designer",         title: "Human-Centered Design Lead",           domain: "design" },
  { slug: "space-architect",        name: "The Space Architect",          title: "Built Environment Strategist",         domain: "infrastructure" },
  { slug: "measurement-scientist",  name: "The Measurement Scientist",    title: "Impact Metrics Lead",                  domain: "evaluation" },
  { slug: "narrative-researcher",   name: "The Narrative Researcher",     title: "Story & Data Translator",              domain: "communications" },
  { slug: "market-maker",           name: "The Market Maker",             title: "Systems Market Strategist",            domain: "market" },
  { slug: "architect",              name: "The Architect",                title: "Systems Integration Lead",             domain: "systems" },
],

// ============================================================================
// 23. AGREEMENT TEMPLATES — All 7
// ============================================================================
agreementTemplates: [
  { id: "tpl_baa",           type: "BAA",           name: "Business Associate Agreement",             governing_laws: ["HIPAA","HITECH Act","45 CFR Parts 160 & 164"] },
  { id: "tpl_dua",           type: "DUA",           name: "Data Use Agreement",                       governing_laws: ["HIPAA","45 CFR §164.514(e)"] },
  { id: "tpl_mou",           type: "MOU",           name: "Memorandum of Understanding",              governing_laws: ["Varies by jurisdiction"] },
  { id: "tpl_idsa",          type: "IDSA",          name: "Interagency Data Sharing Agreement",       governing_laws: ["HIPAA","Privacy Act of 1974","State data sharing statutes"] },
  { id: "tpl_qsoa",          type: "QSOA",          name: "Qualified Service Organization Agreement",  governing_laws: ["42 CFR Part 2","HIPAA"] },
  { id: "tpl_hipaa_consent", type: "HIPAA_consent", name: "HIPAA Authorization for Disclosure",       governing_laws: ["45 CFR §164.508"] },
  { id: "tpl_ferpa_consent", type: "FERPA_consent", name: "FERPA Consent to Disclose",                governing_laws: ["20 U.S.C. §1232g","34 CFR Part 99"] },
],

// ============================================================================
// 24. COMPLIANCE RULES — GAP_TO_AGREEMENT_MAP and BARRIER_TYPE_MAP
// ============================================================================
complianceRules: {
  gapToAgreementMap: {
    "HIPAA":                          ["BAA","HIPAA_consent"],
    "42 CFR Part 2":                  ["QSOA","42CFR_consent"],
    "FERPA":                          ["FERPA_consent"],
    "CJIS_Security_Policy":           ["IDSA"],
    "Medicaid Inmate Exclusion Policy":["IDSA","HIPAA_consent"],
    "Privacy Act / 42 CFR Part 2":    ["42CFR_consent","DUA"],
  },
  barrierTypeMap: {
    legal:    ["IDSA","MOU"],
    technical:["IDSA","MOU","joint_funding"],
    political:["MOU","compact"],
    funding:  ["joint_funding","MOU"],
    consent:  ["HIPAA_consent"],
  },
  statusTransitions: {
    draft:     ["in_review"],
    in_review: ["executed","draft"],
    executed:  [],
  },
  defaultState: "Pennsylvania",
  defaultExpiration: 365,
},

// ============================================================================
// 25. ELIGIBILITY ENGINE — 12 programs + FPL formula
// ============================================================================
eligibilityEngine: {
  fplFormula: { base: 15060, perPerson: 5380, note: "FPL(household) = 15060 + 5380 × (household - 1)" },
  fplExamples: { hh1: 15060, hh2: 20440, hh3: 25820, hh4: 31200, hh5: 36580 },
  programs: [
    { id: "medicaid",           name: "Medicaid",            fpl_threshold: 138, threshold_type: "lte_pct_fpl", benefit_formula: "age >= 65 ? $12,000 : (children ? $8,500 : $6,500) per year" },
    { id: "chip",               name: "CHIP",                fpl_threshold: 250, threshold_type: "lte_pct_fpl", benefit_formula: "$2,800 × children / year" },
    { id: "snap",               name: "SNAP",                fpl_threshold: 130, threshold_type: "lte_pct_fpl_gross", benefit_formula: "70% of max: hh1=$203/mo, hh2=$374/mo, hh3=$536/mo, hh4=$681/mo, hh5=$809/mo" },
    { id: "section_8",          name: "Section 8 HCV",       fpl_threshold: null, threshold_type: "lte_50_pct_ami", benefit_formula: "voucher = medianRent - (income × 0.30 / 12)" },
    { id: "eitc",               name: "EITC",                fpl_threshold: null, threshold_type: "income_limit", benefit_formula: "60% of max: 0 kids=$379, 1=$2,397, 2=$3,962, 3=$4,458" },
    { id: "wic",                name: "WIC",                 fpl_threshold: 185, threshold_type: "lte_pct_fpl", benefit_formula: "$600 × min(children, 3) / year" },
    { id: "liheap",             name: "LIHEAP",              fpl_threshold: 150, threshold_type: "lte_pct_fpl", benefit_formula: "$500 / year" },
    { id: "head_start",         name: "Head Start",          fpl_threshold: 100, threshold_type: "lte_pct_fpl", benefit_formula: "$10,000 per child / year (ages 3-5)" },
    { id: "free_lunch",         name: "Free School Lunch",   fpl_threshold: 130, threshold_type: "lte_pct_fpl", benefit_formula: "$1,200 × children / year" },
    { id: "reduced_lunch",      name: "Reduced School Lunch",fpl_threshold: 185, threshold_type: "130_to_185_fpl", benefit_formula: "$800 × children / year" },
    { id: "ssi",                name: "SSI",                 fpl_threshold: null, threshold_type: "income_lt_11316_or_disabled", benefit_formula: "max $943/month - countable income (with $20 exclusion)" },
    { id: "tanf",               name: "TANF",                fpl_threshold: 100, threshold_type: "lte_pct_fpl", benefit_formula: "$400/month (conservative median)" },
    { id: "pell_grant",         name: "Pell Grant",          fpl_threshold: null, threshold_type: "age_17_30_income_lt_60k", benefit_formula: "$7,395 if income < $30k; $3,698 if $30k-$60k" },
  ],
  snapMaxMonthly: { hh1: 291, hh2: 535, hh3: 766, hh4: 973, hh5: 1155 },
  eitcIncomeLimits: { children_0: 17640, children_1: 46560, children_2: 52918, children_3: 56838 },
  eitcMaxCredits:   { children_0: 632, children_1: 3995, children_2: 6604, children_3: 7430 },
},

// ============================================================================
// 26. BOND MODELS — DomeBond and ChronBond structures
// ============================================================================
bondModels: {
  domeBond: {
    fields: ["bond_id","subject","face_value","coupon_rate","maturity_years","rating","cosm_score","programs_backing","yield_to_maturity"],
    ratingFormula: "Based on dome coverage (cosm_score): higher cosm → better rating (AAA–B)",
    faceValue: "Total coordination savings (delta = fragmented - coordinated)",
  },
  chronBond: {
    fields: ["bond_id","parcel","face_value","coupon_rate","maturity_years","rating","chron_score","sqft_backing","yield_to_maturity"],
    ratingFormula: "permanence >= 0.8 AND policy >= 0.5 → AAA; permanence >= 0.6 → AA; permanence >= 0.4 → A; else → BBB",
    faceValue: "Economic impact value of activated space",
  },
  trancheYieldMultipliers: { senior: 0.6, mezzanine: 1.0, equity: 1.5 },
  trancheRiskMultipliers:  { senior: 0.4, mezzanine: 1.0, equity: 1.8 },
  stressScenarios: { recession: 0.30, moderate: 0.15, baseline: 0.00 },
},

// ============================================================================
// 27. TREASURY PHASE-OUTS — All 9 benefit phase-out schedules
// ============================================================================
treasuryPhaseOuts: {
  schedules: {
    snap:     { floor: 18000, ceiling: 36000 },
    medicaid: { floor: 20000, ceiling: 40000 },
    tanf:     { floor: 10000, ceiling: 24000 },
    housing:  { floor: 15000, ceiling: 45000 },
    ccdf:     { floor: 20000, ceiling: 50000 },
    ssi:      { floor: 10000, ceiling: 28000 },
    liheap:   { floor: 15000, ceiling: 30000 },
    wic:      { floor: 22000, ceiling: 48000 },
    eitc:     { floor: 15000, ceiling: 55000 },
  },
  phaseOutFormula: "if income <= floor: base_amount; if income >= ceiling: 0; else: base_amount × (ceiling - income) / (ceiling - floor)",
  cliffGuard: {
    emtrThreshold: 0.50,
    incomeSimulationStep: 500,
    incomeSimulationCeiling: "max(current × 3, $150,000)",
    bridgeStep: 2500,
  },
},

// ============================================================================
// 28. NARRATIVE CONFIG — Arc types, tension weights, signals
// ============================================================================
narrativeConfig: {
  arcTypes: ["rising_tension","turning_point","fall_and_recovery","slow_burn","cascade","breakthrough"],
  domainTensionWeights: {
    financial: 0.7, health: 0.8, legal: 0.6, housing: 0.9, employment: 0.5, digital: 0.4, social: 0.3,
  },
  turningPointSignals: ["appeal_overturned","trial_decisive_benefit","cliff_bridge_activated","credential_completed","referral_completed","gap_resolved","production_shipped","benefit_restored","housing_secured"],
  escalationSignals: ["cliff_zone_entered","cascade_risk_critical","appeal_denied","trial_stopped_futility","eviction_notice","benefit_cutoff","exposure_critical","readmission"],
  tensionFormula: "tension = base_tension × 0.4 + event_density × 0.3 + escalation_factor + turning_factor × 0.5; clamped [0, 1]",
  arcClassification: {
    "escalation AND turning": "fall_and_recovery",
    "escalation AND no turning": "rising_tension",
    "turning AND no escalation": "breakthrough",
    ">=8 events": "slow_burn",
    "else": "rising_tension",
  },
  cascadeDetection: {
    minDomains: 2,
    minEventsPerDomain: 2,
    tensionFormula: "min(0.5 + n_high_domains × 0.15 + escalation_count × 0.1, 1.0)",
  },
  mediumRecommendationThresholds: {
    doc: { minPotential: 0.8, requiresCascade: true },
    series: { minPotential: 0.7 },
    short: { minPotential: 0.5 },
    installation: { minPotential: 0.0 },
  },
},

// ============================================================================
// 29. PIPELINE STAGES — 5 stages with gate requirements (DUOMO + THAUMA)
// ============================================================================
pipelineStages: {
  stageOrder: ["development","pre_production","production","post","distribution"],
  gateForStage: {
    development:    "greenlight",
    pre_production: "pre_production",
    production:     "production",
    post:           "picture_lock",
    distribution:   "ship",
  },
  gateRequirements: {
    greenlight:      ["character_id present","consent_tier appropriate (real → tier2+)","≥1 Showrunner on team","budget_total > 0"],
    pre_production:  ["dome_build_sheet_complete (initial_conditions present)","team ≥ 2","all development deliverables done"],
    production:      ["skeleton_key_pack_started","ethics_review if real character","budget allocated across stages"],
    picture_lock:    ["≥1 IP asset","gap log has entries","all production deliverables done"],
    ship:            ["learning_package_generated","all gaps triaged","IP rights registered for all assets"],
  },
  duomoPipeline: {
    development:    { progress: 20, actions: "Fetch legal provisions, build rights_package, cost data, cast_list, deal_structure" },
    pre_production: { progress: 40, actions: "Recommend coordination models (top 4), build shooting_script, budget_top_sheet" },
    production:     { progress: 65, actions: "Execute 12 dome domains, query all DUOMO APIs, domain scores" },
    post:           { progress: 85, actions: "Verify dome completeness, generate innovations, IP outputs across 8 domains" },
    distribution:   { progress: 100, actions: "Calculate final COSM score, price DomeBond, generate industries_changed" },
  },
  thaumaPipeline: {
    development:    { progress: 20, actions: "Query parcels, return active_parcel (vacant preference), nearby_parcels" },
    pre_production: { progress: 40, actions: "Generate activation_design, activation_timeline (9-15 months), cost_model" },
    production:     { progress: 65, actions: "Execute permits, activation, capture; calculate initial Chron score" },
    post:           { progress: 85, actions: "Document episodes, generate innovations, assess permanence and ripple" },
    distribution:   { progress: 100, actions: "Final CHRON score: (sqft × hours) × (1 + significance); price ChronBond" },
  },
},

// ============================================================================
// 30. SERVICE REGISTRY — All 18 services (12 DUOMO + 6 THAUMA)
// ============================================================================
serviceRegistry: {
  duomo: [
    { name: "domes-legal-research",  backendPort: 8000, frontendPort: 5173, endpoints: ["/api/match","/api/provisions","/api/domains","/api/explain"] },
    { name: "domes-data-research",   backendPort: 8001, frontendPort: 5174, endpoints: ["/api/systems","/api/connections","/api/gaps","/api/consent-pathways"] },
    { name: "domes-profile-research",backendPort: 8002, frontendPort: 5175, endpoints: ["/api/cases","/api/profiles","/api/cost","/api/systems"] },
    { name: "domes-legal",           backendPort: 8003, frontendPort: 5177, endpoints: ["/api/provisions","/api/search","/api/match","/api/graph"] },
    { name: "domes-datamap",         backendPort: 8013, frontendPort: 5176, endpoints: ["/api/systems","/api/connections","/api/gaps","/api/person-map","/api/bridges","/api/stats"] },
    { name: "domes-profiles",        backendPort: 8004, frontendPort: 5178, endpoints: ["/api/profiles","/api/cost"] },
    { name: "domes-contracts",       backendPort: 8014, frontendPort: 5182, endpoints: ["/api/agreements","/api/compliance","/api/consent"] },
    { name: "domes-architect",       backendPort: 8015, frontendPort: 5183, endpoints: ["/api/models","/api/architectures"] },
    { name: "domes-viz",             backendPort: 8005, frontendPort: 5179, endpoints: ["/api/narrative/sections","/api/marble/worlds","/api/marble/generate"] },
    { name: "domes-brain",           backendPort: 8006, frontendPort: 5180, endpoints: ["/api/query","/api/services","/api/activity","/api/stats","/api/discoveries"] },
    { name: "domes-lab",             backendPort: 8007, frontendPort: 5181, endpoints: ["/api/teammates","/api/innovations","/api/collaborations","/api/sessions","/api/stats","/api/generate"] },
    { name: "domes-flourishing",     backendPort: 8016, frontendPort: 5184, endpoints: ["/api/domains","/api/philosophy","/api/finance","/api/culture","/api/vitality","/api/flourishing-index"] },
  ],
  thauma: [
    { name: "spheres-assets", backendPort: 8017, frontendPort: 5185, endpoints: ["/api/parcels","/api/stats","/api/value"] },
    { name: "spheres-legal",  backendPort: 8018, frontendPort: 5186, endpoints: ["/api/permits","/api/contracts","/api/policy"] },
    { name: "spheres-studio", backendPort: 8019, frontendPort: 5190, endpoints: ["/api/designs","/api/cost","/api/timeline","/api/world","/api/gallery"] },
    { name: "spheres-viz",    backendPort: 8008, frontendPort: 5200, endpoints: ["/api/episodes"] },
    { name: "spheres-brain",  backendPort: 8009, frontendPort: 5210, endpoints: ["/api/query","/api/services","/api/activity","/api/metrics","/api/discoveries"] },
    { name: "spheres-lab",    backendPort: 8010, frontendPort: 5220, endpoints: ["/api/teammates","/api/innovations","/api/collaborations","/api/sessions","/api/stats","/api/generate"] },
  ],
  engine: { name: "baths-engine", backendPort: 9000, frontendPort: 5300, version: "0.2.0" },
  thaumaOS: { backendPort: 8100, frontendPort: 3000 },
},

// ============================================================================
// 31. FRAGMENT CONFIG — 28 priority counties, 10 Census ACS groups, 6 external
// ============================================================================
fragmentConfig: {
  priorityCounties: [
    // Philadelphia metro
    { fips: "42101", name: "Philadelphia, PA" },
    { fips: "42045", name: "Delaware County, PA" },
    { fips: "42091", name: "Montgomery County, PA" },
    { fips: "42017", name: "Bucks County, PA" },
    { fips: "42029", name: "Chester County, PA" },
    // NYC
    { fips: "36061", name: "Manhattan, NY" },
    { fips: "36047", name: "Brooklyn, NY" },
    { fips: "36081", name: "Queens, NY" },
    { fips: "36005", name: "Bronx, NY" },
    // Major metros
    { fips: "06037", name: "Los Angeles, CA" },
    { fips: "17031", name: "Cook County (Chicago), IL" },
    { fips: "48201", name: "Harris County (Houston), TX" },
    { fips: "04013", name: "Maricopa County (Phoenix), AZ" },
    { fips: "48113", name: "Dallas County, TX" },
    { fips: "12086", name: "Miami-Dade County, FL" },
    { fips: "13121", name: "Fulton County (Atlanta), GA" },
    { fips: "53033", name: "King County (Seattle), WA" },
    { fips: "24510", name: "Baltimore City, MD" },
    { fips: "11001", name: "Washington, DC" },
    // Rural/Appalachia
    { fips: "21013", name: "Bell County, KY" },
    { fips: "54055", name: "Mercer County, WV" },
    // Deep South
    { fips: "28049", name: "Hinds County (Jackson), MS" },
    { fips: "01073", name: "Jefferson County (Birmingham), AL" },
    // Midwest
    { fips: "26163", name: "Wayne County (Detroit), MI" },
    { fips: "39035", name: "Cuyahoga County (Cleveland), OH" },
    // New Jersey
    { fips: "34013", name: "Essex County, NJ" },
    { fips: "34017", name: "Hudson County, NJ" },
    { fips: "34023", name: "Middlesex County, NJ" },
  ],
  censusAcsGroups: [
    { id: "census-demographics",      variables: ["total_pop","median_age","male_pop","female_pop","white_alone","black_alone","asian_alone","hispanic_latino","foreign_born"] },
    { id: "census-income",            variables: ["median_household_income","per_capita_income","poverty_total","poverty_below","gini_index","snap_households","public_assistance_income","ssi_income"] },
    { id: "census-housing",           variables: ["total_units","occupied_units","vacant_units","owner_occupied","renter_occupied","median_home_value","median_gross_rent","median_monthly_housing_cost"] },
    { id: "census-rent-burden",       variables: ["rent_total","rent_30_35_pct","rent_35_40_pct","rent_40_50_pct","rent_50_plus_pct","rent_not_computed"] },
    { id: "census-health-insurance",  variables: ["total_pop_insurance","with_insurance","male_under6_uninsured","medicaid_means_tested","employer_insurance"] },
    { id: "census-disability",        variables: ["total_disability_pop","male_with_disability","female_with_disability","disability_under5","disability_5_17","disability_18_34","disability_65_74","disability_75_plus"] },
    { id: "census-education",         variables: ["edu_pop_25plus","less_than_9th","high_school_diploma","some_college","bachelors","masters","doctorate","school_enrollment_total","school_enrollment_public"] },
    { id: "census-commute",           variables: ["workers_total","drove_alone","public_transit","walked","worked_from_home","mean_travel_time","no_vehicle","one_vehicle"] },
    { id: "census-internet",          variables: ["total_households_internet","with_internet","broadband","no_internet","has_computer","has_smartphone_only","no_computer"] },
    { id: "census-employment",        variables: ["pop_16_plus","in_labor_force","civilian_employed","civilian_unemployed","not_in_labor_force","occupation_mgmt","occupation_service","occupation_production"] },
  ],
  externalSources: [
    { id: "bls-unemployment", name: "BLS LAUS Unemployment", status: "active" },
    { id: "hud-fmr",         name: "HUD Fair Market Rents", status: "active" },
    { id: "epa-air-quality", name: "EPA AQS Ozone Data", status: "active" },
    { id: "usda-food-access",name: "USDA Food Access Atlas", status: "active" },
    { id: "fema-disasters",  name: "OpenFEMA Disaster Declarations", status: "active" },
    { id: "cdc-mortality",   name: "CDC Mortality Data", status: "gap" },
    { id: "fbi-crime",       name: "FBI Crime Statistics", status: "gap" },
  ],
  schedule: "5x daily (7am, 12pm, 5pm, 10pm, 3am UTC), ~30 source-geography pairs per run",
},

// ============================================================================
// 32. COSM ARCHETYPES — All 6 archetype profiles
// ============================================================================
cosmArchetypes: [
  { id: "marcus", name: "Marcus", age: 34, income: 28000, household: 3, children: 2, description: "Single dad, systems-heavy" },
  { id: "elena",  name: "Elena",  age: 29, income: 22000, household: 2, children: 1, description: "Working poor" },
  { id: "james",  name: "James",  age: 72, income: 14000, household: 1, children: 0, description: "Elderly disabled" },
  { id: "rivera", name: "Rivera Family", age: 38, income: 52000, household: 5, children: 3, description: "Benefits cliff" },
  { id: "aisha",  name: "Aisha",  age: 19, income: 12000, household: 1, children: 0, description: "Aged out of foster care" },
  { id: "median", name: "Median", age: 38, income: 59540, household: 2, children: 1, description: "Benchmark" },
],

// ============================================================================
// 33. SEED CENSUS DATA — Philadelphia real data (Census ACS 2022 5-year)
// ============================================================================
seedCensusData: {
  philadelphia: {
    fips: "42101",
    total_pop: 1603797,
    median_age: 34.8,
    median_household_income: 52649,
    per_capita_income: 30422,
    poverty_rate: 22.6,
    poverty_below: 347948,
    poverty_total: 1541987,
    gini_index: 0.5058,
    snap_households: 171847,
    total_housing_units: 700392,
    vacant_units: 82523,
    owner_occupied: 310946,
    renter_occupied: 306923,
    median_gross_rent: 1107,
    median_home_value: 200300,
    rent_50_plus_pct: 72910,
    medicaid_means_tested: 462596,
    unemployment_rate: 5.1,
    fmr: { br0: 1088, br1: 1166, br2: 1431, br3: 1797, br4: 1963 },
    fema_events: [
      { id: "DR-4618", name: "Hurricane Ida", year: 2021 },
      { id: "EM-3506", name: "COVID-19", year: 2020 },
    ],
  },
  manhattan: {
    fips: "36061",
    total_pop: 1694251,
    median_age: 37.2,
    median_household_income: 93651,
    per_capita_income: 79781,
    gini_index: 0.5976,
    median_gross_rent: 1899,
    median_home_value: 999999,
    medicaid_means_tested: 391434,
  },
},

// ============================================================================
// 34. SYSTEM BENCHMARKS — from profile_engine.py (annual_cost + coord_savings)
// ============================================================================
systemBenchmarks: {
  // Health
  medicaid:      { domain: "health",        label: "Medicaid",                      annual_cost: 12000, coord_savings: 0.35 },
  bha:           { domain: "health",        label: "Behavioral Health",             annual_cost: 18000, coord_savings: 0.45 },
  hie:           { domain: "health",        label: "Health Info Exchange",           annual_cost: 2000,  coord_savings: 0.60 },
  pdmp:          { domain: "health",        label: "Prescription Drug Monitoring",   annual_cost: 1500,  coord_savings: 0.50 },
  mco:           { domain: "health",        label: "Managed Care Org",              annual_cost: 14000, coord_savings: 0.30 },
  va:            { domain: "health",        label: "VA Healthcare",                 annual_cost: 22000, coord_savings: 0.40 },
  er_frequent:   { domain: "health",        label: "Frequent ER Use",               annual_cost: 28000, coord_savings: 0.65 },
  // Justice
  doc:           { domain: "justice",       label: "Dept of Corrections",           annual_cost: 15000, coord_savings: 0.50 },
  probation:     { domain: "justice",       label: "Probation/Parole",              annual_cost: 5000,  coord_savings: 0.40 },
  court_cms:     { domain: "justice",       label: "Court Case Mgmt",              annual_cost: 3000,  coord_savings: 0.35 },
  juvenile_court:{ domain: "justice",       label: "Juvenile Court",               annual_cost: 8000,  coord_savings: 0.45 },
  // Housing
  hmis:          { domain: "housing",       label: "Homeless Info System",           annual_cost: 8000,  coord_savings: 0.55 },
  pha:           { domain: "housing",       label: "Public Housing Auth",           annual_cost: 9600,  coord_savings: 0.25 },
  shelter:       { domain: "housing",       label: "Emergency Shelter",             annual_cost: 12000, coord_savings: 0.60 },
  // Income
  tanf:          { domain: "income",        label: "TANF",                          annual_cost: 7200,  coord_savings: 0.30 },
  snap:          { domain: "income",        label: "SNAP",                          annual_cost: 3600,  coord_savings: 0.20 },
  ssi:           { domain: "income",        label: "SSI",                           annual_cost: 10200, coord_savings: 0.25 },
  ssdi:          { domain: "income",        label: "SSDI",                          annual_cost: 14400, coord_savings: 0.25 },
  ssa:           { domain: "income",        label: "Social Security Admin",         annual_cost: 10200, coord_savings: 0.25 },
  unemployment:  { domain: "income",        label: "Unemployment Comp",             annual_cost: 6000,  coord_savings: 0.30 },
  // Education
  iep:           { domain: "education",     label: "IEP / Special Ed",              annual_cost: 12000, coord_savings: 0.35 },
  slds:          { domain: "education",     label: "Student Longitudinal Data",     annual_cost: 1500,  coord_savings: 0.50 },
  // Child Welfare
  sacwis:        { domain: "child_welfare", label: "Child Welfare Info System",      annual_cost: 18000, coord_savings: 0.45 },
  foster_care:   { domain: "child_welfare", label: "Foster Care",                   annual_cost: 22000, coord_savings: 0.40 },
},

// ============================================================================
// 35. CIRCUMSTANCE SYSTEMS — Full mapping
// ============================================================================
circumstanceSystems: {
  is_homeless:            ["hmis","shelter"],
  has_housing_instability:["hmis"],
  is_section_8:           ["pha"],
  is_in_shelter:          ["shelter"],
  has_substance_use:      ["bha","pdmp"],
  has_mental_illness:     ["bha"],
  has_chronic_health:     ["hie","mco"],
  is_frequent_er:         ["er_frequent","hie"],
  is_on_medicaid:         ["medicaid","mco"],
  is_va_healthcare:       ["va"],
  is_dual_eligible:       ["va","medicaid"],
  has_disability:         ["ssa"],
  is_incarcerated:        ["doc"],
  is_recently_released:   ["doc","probation"],
  is_on_probation:        ["probation"],
  is_on_parole:           ["probation"],
  is_juvenile_justice:    ["juvenile_court","court_cms"],
  has_dv_history:         ["court_cms"],
  is_on_tanf:             ["tanf"],
  is_on_snap:             ["snap"],
  is_on_ssi:              ["ssi"],
  is_on_ssdi:             ["ssdi"],
  is_unemployed:          ["unemployment"],
  is_in_foster_care:      ["sacwis","foster_care"],
  has_child_in_foster:    ["sacwis"],
  is_aging_out_foster:    ["sacwis","foster_care"],
  has_iep:                ["iep","slds"],
  is_in_special_ed:       ["iep"],
  has_truancy:            ["slds"],
  is_school_age:          ["slds"],
},

// ============================================================================
// 36. ENRICHMENT CONFIG — dimension-to-cost mapping, 6 enrichment pass types
// ============================================================================
enrichmentConfig: {
  dimensionToCost: {
    healthcare:       ["healthcare","fragmentation"],
    housing:          ["housing","shelter"],
    income:           ["fragmentation"],
    food:             ["food"],
    employment:       ["education","fragmentation"],
    education:        ["education"],
    justice:          ["incarceration"],
    data_privacy:     ["fragmentation"],
    interoperability: ["fragmentation"],
  },
  enrichmentPasses: [
    { type: "link_provisions_to_costs",      description: "Cross-references legal provisions with cost data by dome_dimension → cost_category mapping" },
    { type: "link_provisions_to_systems",    description: "Maps provisions to government systems they affect" },
    { type: "detect_regulatory_conflicts",   description: "Identifies conflicts between systems (e.g., HIPAA vs 42 CFR Part 2)" },
    { type: "score_coordination_opportunities",description: "Calculates coordination savings potential per provision/system pair" },
    { type: "detect_fragmentation_hotspots", description: "Identifies where multiple provisions create barriers at the same point" },
    { type: "score_parcel_opportunities",    description: "For THAUMA: overlays zoning, cost, regulatory data on parcels" },
  ],
  totalEnrichments: 4898,
},

// ============================================================================
// 37. BIO EXPERIMENT CONFIG — Trial configs for all 5 profiles
// ============================================================================
bioExperimentConfig: {
  design: "ABAB crossover",
  washoutDays: "max(phase_days / 4, 1)",
  defaultPhaseDays: 14,
  statistics: {
    effectSize: "Cohen's d (pooled SD)",
    pValue: "Welch's t-test with Satterthwaite df",
    bayesianProbability: "P(B > A) = Φ(d / √(1/nA + 1/nB))",
  },
  stoppingRules: {
    decisiveBenefit: { bayesian_prob: 0.95, min_effect: 0.2, action: "stop, adopt" },
    decisiveFutility: { bayesian_prob_lte: 0.05, action: "stop, control is better" },
    negligibleEffect: { min_measurements: 20, max_effect: 0.2, action: "stop, no meaningful difference" },
  },
  recommendations: {
    strong:       { p: 0.05, bayesian: 0.95, effect: 0.5, text: "Strong evidence, consider adopting" },
    significant:  { p: 0.05, effect: 0.2, text: "Statistically significant, more cycles recommended" },
    suggestive:   { bayesian: 0.80, effect: 0.2, text: "Suggestive, continue" },
    noEffect:     { effect_lt: 0.2, text: "No meaningful difference" },
    inconclusive: { text: "Inconclusive, continue" },
  },
  trials: {
    "marcus-thompson": {
      hypothesis: "Buprenorphine + counseling reduces cravings more than counseling alone",
      intervention: "Buprenorphine 8mg sublingual + weekly counseling",
      control: "Weekly counseling only",
      metric_name: "daily_craving_score",
      control_data: [6.2, 5.8, 6.5, 7.0, 6.1, 5.9, 6.3, 6.8],
      intervention_data: [4.1, 3.5, 3.8, 3.2, 4.0, 3.6, 3.3, 2.9],
    },
    "sarah-chen": {
      hypothesis: "Trauma-focused CBT reduces PTSD symptoms more than standard therapy",
      intervention: "Trauma-focused CBT (12-session protocol)",
      control: "Standard supportive therapy",
      metric_name: "PCL5_score",
      control_data: [52, 50, 53, 48, 51, 49, 50, 47],
      intervention_data: [45, 38, 35, 32, 30, 28, 27, 25],
    },
    "james-williams": {
      hypothesis: "Yoga + PT reduces chronic pain more than standard care",
      intervention: "Yoga + physical therapy (3x/week)",
      control: "Standard pain management",
      metric_name: "pain_score_0_10",
      control_data: [7.1, 6.8, 7.3, 6.9, 7.0, 7.2, 6.7, 7.1],
      intervention_data: [5.5, 4.8, 4.2, 3.9, 4.1, 3.7, 3.5, 3.3],
    },
    "maria-rodriguez": {
      hypothesis: "Structured mentoring reduces behavioral incidents more than standard school support",
      intervention: "1:1 mentoring + after-school program",
      control: "Standard school counseling",
      metric_name: "weekly_behavioral_incidents",
      control_data: [3, 4, 3, 5, 4, 3, 4, 3],
      intervention_data: [2, 1, 2, 1, 1, 0, 1, 0],
    },
    "robert-jackson": {
      hypothesis: "ACT team + housing first reduces ER visits vs standard outreach",
      intervention: "ACT team engagement + housing first placement",
      control: "Standard street outreach",
      metric_name: "monthly_er_visits",
      control_data: [4, 5, 3, 6, 4, 5, 4, 3],
      intervention_data: [2, 1, 1, 0, 1, 0, 0, 1],
    },
  },
},

// ============================================================================
// 38. CAPITAL MARKETS CONFIG — Payout, tranches, default scenarios
// ============================================================================
capitalMarketsConfig: {
  payoutRatio: 0.70,
  discountRate: 0.05,
  var95ZScore: 1.645,
  trancheYieldMultipliers: { senior: 0.6, mezzanine: 1.0, equity: 1.5 },
  trancheRiskMultipliers:  { senior: 0.4, mezzanine: 1.0, equity: 1.8 },
  defaultScenarios: { recession: 0.30, moderate: 0.15, baseline: 0.00 },
  poolFormula: "total_notional = Σ(expected_savings × probability_of_success); coupon = expected_yield × PAYOUT_RATIO",
  pricingFormula: "expected_cf = Σ(p × s / (1+r)^t); var_95 = 1.645 × √(Σ(p(1-p)s²)) × risk_mult",
},

// ============================================================================
// 39. OECD SCORES — US vs OECD Average for all 11 dimensions
// ============================================================================
oecdScores: [
  { dimension: "Housing",            us: 7.9, oecd_avg: 6.6 },
  { dimension: "Income",             us: 10.0, oecd_avg: 5.5 },
  { dimension: "Jobs",               us: 7.5, oecd_avg: 6.5 },
  { dimension: "Community",          us: 7.3, oecd_avg: 6.3 },
  { dimension: "Education",          us: 7.1, oecd_avg: 6.2 },
  { dimension: "Environment",        us: 6.9, oecd_avg: 6.2 },
  { dimension: "Civic Engagement",   us: 7.1, oecd_avg: 5.5 },
  { dimension: "Health",             us: 5.5, oecd_avg: 6.9 },
  { dimension: "Life Satisfaction",  us: 6.9, oecd_avg: 6.5 },
  { dimension: "Safety",             us: 4.8, oecd_avg: 7.8 },
  { dimension: "Work-Life Balance",  us: 5.2, oecd_avg: 6.4 },
],

// ============================================================================
// 40. FLOURISHING INDICATORS — Healthcare targets vs current US values
// ============================================================================
flourishingIndicators: {
  healthcare: [
    { metric: "Insurance coverage",         target: 100,   current: 91.7, unit: "%",       source: "Census CPS 2023" },
    { metric: "PCPs per 100K",              target: 80,    current: 55.4, unit: "per 100K", source: "HRSA 2023" },
    { metric: "Preventable ER visits",      target: 0,     current: 48.3, unit: "per 1000", source: "AHRQ 2022" },
    { metric: "Care coordination score",    target: 100,   current: 52,   unit: "score",    source: "Commonwealth Fund 2023" },
  ],
  vitalityDomains: {
    clinical_care:     0.20,
    nutrition_food:    0.15,
    mental_wellness:   0.15,
    movement_fitness:  0.10,
    sleep_rest:        0.10,
    nature_environment:0.10,
    social_connection: 0.20,
  },
},

// ============================================================================
// 41. DOMAIN COLORS — from domes-legal graph routes
// ============================================================================
domainColors: {
  health:        "#1A6B3C",
  justice:       "#8B1A1A",
  housing:       "#1A3D8B",
  income:        "#6B5A1A",
  education:     "#5A1A6B",
  child_welfare: "#1A6B6B",
  civil_rights:  "#6B1A4B",
},

// ============================================================================
// 42. EPISODES — Season 1 "The North Broad Concourse"
// ============================================================================
episodes: {
  season1: {
    title: "The North Broad Concourse",
    tagline: "What happens when a city decides to remember what it buried?",
    location: "N Broad St & W Lehigh Ave — BSL Concourse (below grade)",
    budget: 2400000,
    crew: 18,
    totalRuntime: 245,
    materialSystemsDeployed: 7,
    episodes: [
      { number: 1, title: "Descent",          runtime: 48, arc: "establishing",   materials: ["acoustic_metamaterial","projection_mapping"] },
      { number: 2, title: "The Nine Senses",  runtime: 52, arc: "rising_action",  materials: ["electrochromic_surface","haptic_surface","phase_change_panel","olfactory_synthesis"] },
      { number: 3, title: "First Light",      runtime: 45, arc: "turning_point",  materials: ["acoustic_metamaterial","electrochromic_surface","haptic_surface","projection_mapping","phase_change_panel"], notes: "First public performance — 200 people" },
      { number: 4, title: "The Settlement",   runtime: 50, arc: "complication",   materials: ["projection_mapping","electrochromic_surface","haptic_surface"], notes: "Revenue model: $180/hr production bookings" },
      { number: 5, title: "Permanence",        runtime: 50, arc: "resolution",     materials: ["acoustic_metamaterial","haptic_surface","olfactory_synthesis","electrochromic_surface","projection_mapping","phase_change_panel","shape_memory_element"], notes: "All 7 systems; becomes permanent public infrastructure" },
    ],
  },
},

// ============================================================================
// 43. ENVIRONMENTAL BASELINE — North Broad Concourse BELOW data
// ============================================================================
environmentalBaseline: {
  location: "N Broad St & W Lehigh Ave — BSL Concourse Level",
  depth_ft: 35,
  area_sqft: 48000,
  temperature: { mean_f: 58, range_f: 2, note: "Underground thermal mass" },
  humidity: { mean_pct: 97, range_pct: 6, note: "Groundwater seepage" },
  acoustics: {
    reverb_time_s: 7.2,
    ambient_db: 32,
    train_pulse_db: 78,
    train_frequency_s: 90,
    note: "BSL northbound/southbound — Lehigh Station",
  },
  vibration: {
    baseline_mm_s: 0.05,
    train_peak_mm_s: 4.2,
    train_interval_s: 90,
  },
  air_quality: {
    pm25: 8.2,
    co2_ppm: 620,
    radon_pci_l: 2.1,
    ventilation_cfm: 12000,
  },
  structural: {
    ceiling_height_ft: 14,
    column_spacing_ft: 25,
    floor_material: "Poured concrete (1928)",
    wall_material: "Glazed tile over reinforced concrete",
    load_bearing_psf: 250,
  },
},

}; // end window.BATHS_DATA
