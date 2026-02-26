/**
 * CHARACTER FRAGMENT — Case Studies, Testimony, Government Reports
 *
 * People documented in:
 * - Published social work case studies
 * - Medical case reports with social context
 * - Congressional testimony (first-person accounts)
 * - GAO case studies and Inspector General reports
 * - Legal proceedings with documented circumstances
 * - CMS demonstration project narratives
 */

export default [

  // ══════════════════════════════════════════════════════════════════════════════
  // CONGRESSIONAL TESTIMONY — First-Person Accounts
  // ══════════════════════════════════════════════════════════════════════════════

  {
    name: 'Theresa Flores',
    real_or_fictional: 'real',
    source_work: 'Senate Judiciary Committee Testimony on Human Trafficking',
    source_author_creator: 'Senate Judiciary Committee',
    source_year: 2010,
    circumstances: ['trafficking', 'domestic_violence', 'trauma', 'child_marriage'],
    location: 'Detroit, MI; Ohio',
    time_period: '1980s-2010s',
    systems_touched: ['schools (while being trafficked)', 'churches', 'law enforcement', 'victim services', 'congressional testimony'],
    dome_layer_richness: { 1: 8, 2: 5, 3: 4, 4: 7, 5: 5, 6: 4, 7: 5, 8: 6, 9: 4, 10: 10, 11: 3, 12: 6 },
    key_relationships: ['Traffickers', 'Family (unaware)', 'Advocacy organizations'],
    narrative_arc: 'Trafficked as a teenager while attending a suburban high school — her family never knew. She testified before Congress about how trafficking happens in plain sight, inside middle-class communities, and how the systems that should detect it (schools, healthcare, police) consistently fail to.',
    why_this_character_matters: 'Theresa\'s dome reveals trafficking as invisible. Layer 10 (Autonomy) is at zero while every other layer appears normal to outside systems. Her dome tests whether a well-built dome would have detected her situation.',
    source_urls: [],
    scraped_at: new Date().toISOString(),
  },

  {
    name: 'Matthew Charles',
    real_or_fictional: 'real',
    source_work: 'Senate Judiciary Committee Testimony on First Step Act',
    source_author_creator: 'Senate Judiciary Committee',
    source_year: 2018,
    circumstances: ['formerly_incarcerated', 'homeless', 'poverty', 'addiction'],
    location: 'Nashville, TN',
    time_period: '1996-2018',
    systems_touched: ['federal prison', 'courts', 'halfway house', 'reentry services', 'parole', 'employment (barriers)', 'housing (barriers)'],
    dome_layer_richness: { 1: 10, 2: 8, 3: 7, 4: 5, 5: 8, 6: 8, 7: 6, 8: 7, 9: 4, 10: 8, 11: 4, 12: 7 },
    key_relationships: ['Church community', 'Prison mentees', 'Attorneys', 'Employers (denied)'],
    narrative_arc: 'Served 21 years for federal drug charges, became a model prisoner and mentor, was released, started rebuilding his life, then was ordered back to prison because a court ruled his early release was a clerical error. Re-released under the First Step Act. Testified about what reentry actually requires — and how the system makes it nearly impossible.',
    why_this_character_matters: 'Matthew was the face of the First Step Act — the first federal sentencing reform in a generation. His dome maps the reentry obstacle course: Layer 1 (legal barriers), Layer 5 (housing denied to felons), Layer 6 (employers who won\'t hire), all documented in congressional testimony.',
    source_urls: [],
    scraped_at: new Date().toISOString(),
  },

  {
    name: 'Crystal Echo Hawk',
    real_or_fictional: 'real',
    source_work: 'Congressional Testimony on Native American Issues',
    source_author_creator: 'Multiple congressional committees',
    source_year: 2019,
    circumstances: ['indigenous', 'poverty', 'housing_insecure', 'environmental_exposure'],
    location: 'Pawnee Nation, OK',
    time_period: '2010s',
    systems_touched: ['BIA', 'IHS', 'tribal courts', 'federal trust responsibility', 'housing (HUD NAHASDA)', 'education'],
    dome_layer_richness: { 1: 8, 2: 8, 3: 6, 4: 7, 5: 7, 6: 5, 7: 6, 8: 9, 9: 7, 10: 7, 11: 7, 12: 7 },
    key_relationships: ['Pawnee community', 'Tribal leaders', 'Congressional allies'],
    narrative_arc: 'Testified about the invisibility of Native Americans in national data systems — how federal agencies literally don\'t count indigenous people in their surveys, creating a statistical genocide that makes it impossible to document need and therefore impossible to fund solutions.',
    why_this_character_matters: 'Crystal\'s dome reveals the meta-problem: you can\'t build domes for people the data systems don\'t count. Her Layer 2 (Systems) maps the absence of systems — the federal trust responsibility that exists on paper but not in databases.',
    source_urls: [],
    scraped_at: new Date().toISOString(),
  },

  // ══════════════════════════════════════════════════════════════════════════════
  // GAO / IG REPORTS — Documented Individuals
  // ══════════════════════════════════════════════════════════════════════════════

  {
    name: 'The "Phantom" Medicaid Patients',
    real_or_fictional: 'real',
    source_work: 'GAO Report on Medicaid Enrollment Barriers',
    source_author_creator: 'Government Accountability Office',
    source_year: 2019,
    circumstances: ['uninsured', 'poverty', 'chronic_illness', 'illiterate'],
    location: 'Rural South (Alabama, Mississippi, Georgia)',
    time_period: '2019',
    systems_touched: ['Medicaid (denied)', 'emergency rooms', 'community health centers', 'charity care', 'state eligibility systems'],
    dome_layer_richness: { 1: 5, 2: 10, 3: 7, 4: 8, 5: 4, 6: 6, 7: 4, 8: 5, 9: 4, 10: 5, 11: 2, 12: 3 },
    key_relationships: ['Community health workers', 'Emergency room staff', 'State bureaucrats'],
    narrative_arc: 'GAO documented people who qualified for Medicaid but couldn\'t enroll — they lacked internet access for online applications, couldn\'t navigate the phone system, couldn\'t provide required documentation, or didn\'t know Medicaid existed. They used emergency rooms as primary care at 10x the cost.',
    why_this_character_matters: 'This dome is defined by Layer 2 (Systems) failure. The benefit exists. The eligibility exists. But the interface between person and system is broken. These domes reveal the cost of bad UX at government scale.',
    source_urls: [],
    scraped_at: new Date().toISOString(),
  },

  {
    name: 'The Dual-Eligible Elders',
    real_or_fictional: 'real',
    source_work: 'CMS Dual-Eligible Demonstration Evaluation',
    source_author_creator: 'Centers for Medicare & Medicaid Services',
    source_year: 2020,
    circumstances: ['elderly', 'disability', 'chronic_illness', 'poverty', 'isolation'],
    location: 'Multiple states',
    time_period: '2015-2020',
    systems_touched: ['Medicare', 'Medicaid', 'nursing homes', 'home health aides', 'hospitals', 'pharmacies', 'disability services', 'food delivery'],
    dome_layer_richness: { 1: 5, 2: 10, 3: 9, 4: 9, 5: 7, 6: 4, 7: 3, 8: 7, 9: 5, 10: 6, 11: 3, 12: 5 },
    key_relationships: ['Home health aides', 'Case managers', 'Family members', 'Doctors'],
    narrative_arc: 'CMS documented elderly people simultaneously enrolled in Medicare and Medicaid — the most system-intensive population in America. Each person navigates two parallel bureaucracies with different rules, different providers, different formularies. The demonstration tried to coordinate them and documented the staggering complexity.',
    why_this_character_matters: 'Dual-eligible elders are the human proof of fragmentation cost. Their domes have the richest Layer 2 (Systems) of any population — two complete insurance bureaucracies, each with its own portal, its own forms, its own appeals process. The fragmented vs. coordinated cost delta is highest here.',
    source_urls: [],
    scraped_at: new Date().toISOString(),
  },

  // ══════════════════════════════════════════════════════════════════════════════
  // SOCIAL WORK JOURNALS — Published Case Studies
  // ══════════════════════════════════════════════════════════════════════════════

  {
    name: 'Maria (Composite Social Work Case)',
    real_or_fictional: 'real',
    source_work: 'Social Work Case Studies in Integrated Care (NASW)',
    source_author_creator: 'National Association of Social Workers',
    source_year: 2018,
    circumstances: ['immigrant', 'poverty', 'domestic_violence', 'chronic_illness', 'uninsured', 'illiterate'],
    location: 'Texas-Mexico border region',
    time_period: '2010s',
    systems_touched: ['community health center', 'domestic violence shelter', 'immigration services', 'food bank', 'ESL classes', 'legal aid', 'Medicaid (ineligible)'],
    dome_layer_richness: { 1: 8, 2: 7, 3: 6, 4: 7, 5: 7, 6: 6, 7: 7, 8: 6, 9: 5, 10: 8, 11: 3, 12: 4 },
    key_relationships: ['Children', 'Abusive spouse', 'Social worker', 'Legal aid attorney'],
    narrative_arc: 'Undocumented immigrant with diabetes who can\'t access Medicaid, fleeing domestic violence but afraid to call police because of immigration status. The social work case study documents every system she needs but can\'t safely access — the gap between what exists and what\'s available to people without status.',
    why_this_character_matters: 'Maria\'s dome maps the "anti-dome" — every system that should wrap around her instead pushes her away because of immigration status. Her Layer 1 (Legal) status nullifies Layers 2-9.',
    source_urls: [],
    scraped_at: new Date().toISOString(),
  },

  // ══════════════════════════════════════════════════════════════════════════════
  // MEDICAL CASE REPORTS — Social Determinants
  // ══════════════════════════════════════════════════════════════════════════════

  {
    name: 'The Frequent Flyer (Emergency Medicine Literature)',
    real_or_fictional: 'real',
    source_work: 'Super-Utilizers in Emergency Medicine (Annals of Emergency Medicine)',
    source_author_creator: 'Various medical researchers',
    source_year: 2017,
    circumstances: ['homeless', 'addiction', 'mental_illness', 'chronic_illness', 'uninsured'],
    location: 'Urban emergency departments nationwide',
    time_period: '2017',
    systems_touched: ['emergency rooms', 'ambulances', 'police', 'shelters', 'psychiatric holds', 'Medicaid', 'detox programs', 'sobering centers'],
    dome_layer_richness: { 1: 5, 2: 8, 3: 10, 4: 10, 5: 8, 6: 4, 7: 3, 8: 5, 9: 5, 10: 5, 11: 2, 12: 3 },
    key_relationships: ['ER nurses', 'Paramedics', 'Shelter staff'],
    narrative_arc: 'Medical literature documents "super-utilizers" — patients who visit the ER 50-100+ times per year. Each visit costs $2,000-$5,000. The same person costs the healthcare system $150,000-$500,000/year through fragmented emergency care. A coordinated dome (permanent housing + primary care + mental health) costs a fraction.',
    why_this_character_matters: 'The super-utilizer dome has the largest fragmented-vs-coordinated cost delta in the entire BATHS system. Their dome proves the financial thesis: wrapping systems around one person saves more money than treating crises as they come.',
    source_urls: [],
    scraped_at: new Date().toISOString(),
  },

  // ══════════════════════════════════════════════════════════════════════════════
  // COURT RECORDS — Public Legal Proceedings
  // ══════════════════════════════════════════════════════════════════════════════

  {
    name: 'The Central Park Five (Exonerated Five)',
    real_or_fictional: 'real',
    source_work: 'Court Records / When They See Us / Ken Burns Documentary',
    source_author_creator: 'Ava DuVernay (Netflix); Ken Burns (PBS); Court records',
    source_year: 2019,
    circumstances: ['wrongly_convicted', 'incarcerated', 'poverty', 'trauma'],
    location: 'New York City, NY',
    time_period: '1989-2002',
    systems_touched: ['NYPD', 'DA office', 'criminal courts', 'Rikers Island', 'prison', 'parole', 'exoneration process', 'civil lawsuit'],
    dome_layer_richness: { 1: 10, 2: 6, 3: 7, 4: 7, 5: 6, 6: 8, 7: 7, 8: 8, 9: 4, 10: 10, 11: 5, 12: 7 },
    key_relationships: ['Each other', 'Families', 'Matias Reyes (actual perpetrator)', 'Defense attorneys', 'Media'],
    narrative_arc: 'Five Black and Latino teenagers falsely convicted of assault in Central Park. Coerced confessions, rushed trial, 6-13 years in prison each. Exonerated by DNA evidence and the actual perpetrator\'s confession. Their civil suit revealed the NYPD\'s systematic failures — every procedure that was supposed to prevent false conviction failed.',
    why_this_character_matters: 'Five domes built from the same wrongful prosecution reveal how the same legal failure (Layer 1) creates five different life trajectories. Comparing their post-release domes — who recovered and who didn\'t — reveals which other layers buffer against injustice.',
    source_urls: [],
    scraped_at: new Date().toISOString(),
  },

  // ══════════════════════════════════════════════════════════════════════════════
  // PODCAST — First-Person Detailed Accounts
  // ══════════════════════════════════════════════════════════════════════════════

  {
    name: 'Ear Hustle Inmates',
    real_or_fictional: 'real',
    source_work: 'Ear Hustle (Podcast)',
    source_author_creator: 'Earlonne Woods, Nigel Poor, Rahsaan "New York" Thomas',
    source_year: 2017,
    circumstances: ['incarcerated', 'poverty', 'trauma', 'formerly_incarcerated'],
    location: 'San Quentin State Prison, CA',
    time_period: '2017-present',
    systems_touched: ['state prison', 'parole', 'prison education', 'prison health', 'disciplinary system', 'mail system', 'visitation'],
    dome_layer_richness: { 1: 9, 2: 8, 3: 5, 4: 7, 5: 8, 6: 6, 7: 6, 8: 9, 9: 7, 10: 9, 11: 8, 12: 7 },
    key_relationships: ['Fellow inmates', 'Families outside', 'Prison staff', 'Parole officers'],
    narrative_arc: 'The first podcast produced inside a prison. Over 100+ episodes, inmates describe their daily circumstances in extraordinary detail — cell conditions, food, health care, relationships, the experience of time, the bureaucracy of discipline, the architecture of hope inside confinement.',
    why_this_character_matters: 'Ear Hustle fills every dome layer from inside the prison. Layer 9 (Environment) has never been documented from the inhabitant\'s perspective with this much granularity. Layer 10 (Autonomy) and Layer 11 (Creativity) reveal how people create meaning inside total institutional control.',
    source_urls: ['https://www.earhustlesq.com/'],
    scraped_at: new Date().toISOString(),
  },

  {
    name: 'Death, Sex & Money Interviewees',
    real_or_fictional: 'real',
    source_work: 'Death, Sex & Money (Podcast)',
    source_author_creator: 'Anna Sale (WNYC)',
    source_year: 2014,
    circumstances: ['debt', 'grief', 'chronic_illness', 'poverty', 'addiction', 'housing_insecure'],
    location: 'Nationwide',
    time_period: '2014-present',
    systems_touched: ['hospitals', 'bankruptcy', 'student loans', 'hospice', 'welfare', 'rehab'],
    dome_layer_richness: { 1: 4, 2: 5, 3: 8, 4: 7, 5: 5, 6: 6, 7: 5, 8: 7, 9: 3, 10: 6, 11: 5, 12: 7 },
    key_relationships: ['Various — each episode features different person'],
    narrative_arc: 'Hundreds of episodes where ordinary people describe the financial, medical, and emotional circumstances that formal systems don\'t ask about. The "Student Loan Confessions" series alone documented hundreds of people describing how debt shapes every life decision.',
    why_this_character_matters: 'Death, Sex & Money fills Layer 3 (Fiscal) and Layer 12 (Flourishing) with first-person testimony about how money, health, and death actually feel. These are the layers that government data can\'t fill.',
    source_urls: ['https://www.wnycstudios.org/podcasts/deathsexmoney'],
    scraped_at: new Date().toISOString(),
  },

  // ══════════════════════════════════════════════════════════════════════════════
  // GOVERNMENT REPORTS — Individual Profiles
  // ══════════════════════════════════════════════════════════════════════════════

  {
    name: 'The "Falling Through the Cracks" Children',
    real_or_fictional: 'real',
    source_work: 'Child Welfare System Failures (HHS Inspector General)',
    source_author_creator: 'HHS Office of Inspector General',
    source_year: 2020,
    circumstances: ['foster_care', 'domestic_violence', 'trauma', 'housing_insecure'],
    location: 'Multiple states',
    time_period: '2015-2020',
    systems_touched: ['child welfare (CPS)', 'foster care', 'courts', 'schools', 'Medicaid', 'mental health', 'group homes'],
    dome_layer_richness: { 1: 8, 2: 9, 3: 6, 4: 7, 5: 8, 6: 4, 7: 7, 8: 7, 9: 5, 10: 8, 11: 3, 12: 4 },
    key_relationships: ['Biological parents', 'Foster parents', 'Case workers', 'Judges', 'Teachers'],
    narrative_arc: 'The HHS IG documented children who were reported to CPS multiple times before dying. Each case showed the same pattern: referral, investigation, case closed, repeat. The reports map every system failure — the overworked caseworker, the understaffed agency, the judge who believed the parents, the school that didn\'t follow up.',
    why_this_character_matters: 'These domes map fatal system failure. Every layer touched the child and none of them saved them. Building domes retroactively reveals which layer, if strengthened, could have changed the outcome.',
    source_urls: [],
    scraped_at: new Date().toISOString(),
  },

  {
    name: 'The VA Wait List Veterans',
    real_or_fictional: 'real',
    source_work: 'VA Wait Time Scandal (VA IG Report / Multiple outlets)',
    source_author_creator: 'VA Inspector General / CNN',
    source_year: 2014,
    circumstances: ['veteran', 'chronic_illness', 'mental_illness', 'bereavement'],
    location: 'Phoenix, AZ (initially); nationwide',
    time_period: '2014',
    systems_touched: ['VA hospitals', 'VA scheduling system', 'private healthcare (delayed referral)', 'disability benefits', 'congressional complaints'],
    dome_layer_richness: { 1: 6, 2: 10, 3: 6, 4: 10, 5: 5, 6: 5, 7: 4, 8: 6, 9: 4, 10: 7, 11: 3, 12: 5 },
    key_relationships: ['VA staff', 'Fellow veterans', 'Families', 'Congressional representatives'],
    narrative_arc: 'Veterans who died waiting for VA appointments that were hidden on secret wait lists. The Phoenix VA created a fake scheduling system showing short wait times while the actual wait times stretched to months. At least 40 veterans died waiting. The IG documented the systematic deception.',
    why_this_character_matters: 'These domes map Layer 2 (Systems) as a deliberate lie. The system didn\'t fail — it was designed to appear functional while letting people die. Building domes with actual wait times vs. reported wait times reveals the cost of bureaucratic fraud.',
    source_urls: [],
    scraped_at: new Date().toISOString(),
  },
]
