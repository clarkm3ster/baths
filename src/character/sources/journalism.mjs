/**
 * CHARACTER FRAGMENT — Investigative Journalism Sources
 *
 * Real people documented in investigative journalism — ProPublica,
 * NYT, Washington Post, local outlets. Not profiles or features.
 * People whose CIRCUMSTANCES were documented through investigation.
 */

export default [

  // ══════════════════════════════════════════════════════════════════════════════
  // PROPUBLICA — Machine Bias (2016)
  // Criminal justice risk assessment algorithms
  // ══════════════════════════════════════════════════════════════════════════════

  {
    name: 'Brisha Borden',
    real_or_fictional: 'real',
    source_work: 'Machine Bias (ProPublica)',
    source_author_creator: 'Julia Angwin, Jeff Larson, Surya Mattu, Lauren Kirchner',
    source_year: 2016,
    circumstances: ['formerly_incarcerated', 'poverty', 'surveillance'],
    location: 'Broward County, FL',
    time_period: '2013-2014',
    systems_touched: ['criminal justice', 'COMPAS risk assessment', 'courts', 'probation'],
    dome_layer_richness: { 1: 10, 2: 7, 3: 5, 4: 3, 5: 4, 6: 5, 7: 4, 8: 5, 9: 3, 10: 8, 11: 2, 12: 4 },
    key_relationships: ['Other defendants scored by COMPAS'],
    narrative_arc: 'Black woman scored "high risk" by the COMPAS algorithm for a minor offense. A white man with a long criminal history scored "low risk" for a similar charge. ProPublica documented how the algorithm systematically overestimated Black defendants\' risk and underestimated white defendants\' risk.',
    why_this_character_matters: 'Brisha\'s dome reveals how algorithmic systems (Layer 2) encode racial bias into legal outcomes (Layer 1). Her dome vs. comparable white defendants\' domes would show the exact architecture of algorithmic discrimination.',
    source_urls: ['https://www.propublica.org/article/machine-bias-risk-assessments-in-criminal-sentencing'],
    scraped_at: new Date().toISOString(),
  },

  // ══════════════════════════════════════════════════════════════════════════════
  // PROPUBLICA — Maternal Mortality
  // Lost Mothers investigation
  // ══════════════════════════════════════════════════════════════════════════════

  {
    name: 'Kira Johnson',
    real_or_fictional: 'real',
    source_work: 'Lost Mothers: Maternal Mortality in the U.S. (ProPublica/NPR)',
    source_author_creator: 'ProPublica & NPR',
    source_year: 2017,
    circumstances: ['terminal_illness', 'bereavement'],
    location: 'Los Angeles, CA',
    time_period: '2016',
    systems_touched: ['Cedars-Sinai Hospital', 'insurance', 'obstetric care', 'emergency surgery'],
    dome_layer_richness: { 1: 7, 2: 5, 3: 6, 4: 10, 5: 3, 6: 4, 7: 3, 8: 5, 9: 3, 10: 8, 11: 3, 12: 6 },
    key_relationships: ['Charles Johnson IV (husband)', 'Langston (son)', 'Medical staff'],
    narrative_arc: 'Died of internal bleeding after a routine cesarean section at Cedars-Sinai. Her husband begged staff for 10 hours to check on her while her condition deteriorated. ProPublica documented how the hospital ignored a Black woman\'s pain until it was too late — in one of the best-resourced hospitals in America.',
    why_this_character_matters: 'Kira\'s dome reveals maternal mortality architecture. Layer 4 (Health) shows exactly where the medical system failed — not from lack of resources but from failure to listen. Her case launched a national investigation into why the US has the highest maternal mortality rate in the developed world.',
    source_urls: ['https://www.propublica.org/article/lost-mothers-maternal-health-died-childbirth-pregnancy'],
    scraped_at: new Date().toISOString(),
  },

  // ══════════════════════════════════════════════════════════════════════════════
  // NYT — The 1619 Project Case Studies
  // ══════════════════════════════════════════════════════════════════════════════

  {
    name: 'Clyde Ross',
    real_or_fictional: 'real',
    source_work: 'The Case for Reparations (The Atlantic) / The 1619 Project',
    source_author_creator: 'Ta-Nehisi Coates',
    source_year: 2014,
    circumstances: ['poverty', 'displaced', 'housing_insecure', 'debt'],
    location: 'Clarksdale, MS → Chicago, IL (North Lawndale)',
    time_period: '1940s-2010s',
    systems_touched: ['sharecropping', 'contract buying (predatory housing)', 'FHA (denied)', 'banks', 'courts', 'Contract Buyers League'],
    dome_layer_richness: { 1: 8, 2: 6, 3: 10, 4: 3, 5: 10, 6: 7, 7: 4, 8: 8, 9: 5, 10: 7, 11: 3, 12: 5 },
    key_relationships: ['Wife', 'Children', 'Contract Buyers League members'],
    narrative_arc: 'Fled Mississippi sharecropping for Chicago, where he was sold a house on contract — a predatory financing scheme that charged inflated prices with no equity until the final payment. One missed payment and you lost everything. Coates documents the exact financial architecture of racial housing exploitation.',
    why_this_character_matters: 'Clyde\'s dome is the definitive map of racialized housing economics. Layer 3 (Fiscal) and Layer 5 (Housing) are documented with forensic precision — the exact numbers showing how contract buying extracted wealth from Black neighborhoods.',
    source_urls: ['https://www.theatlantic.com/magazine/archive/2014/06/the-case-for-reparations/361631/'],
    scraped_at: new Date().toISOString(),
  },

  // ══════════════════════════════════════════════════════════════════════════════
  // WASHINGTON POST — Flint Water Crisis
  // ══════════════════════════════════════════════════════════════════════════════

  {
    name: 'LeeAnne Walters',
    real_or_fictional: 'real',
    source_work: 'Flint Water Crisis Coverage (Washington Post/multiple)',
    source_author_creator: 'Multiple journalists',
    source_year: 2015,
    circumstances: ['environmental_exposure', 'chronic_illness', 'housing_insecure'],
    location: 'Flint, MI',
    time_period: '2014-2016',
    systems_touched: ['city water system', 'EPA', 'MDEQ', 'hospitals', 'schools', 'Medicaid', 'emergency management'],
    dome_layer_richness: { 1: 8, 2: 7, 3: 6, 4: 8, 5: 7, 6: 5, 7: 6, 8: 8, 9: 10, 10: 8, 11: 3, 12: 5 },
    key_relationships: ['Children (lead-exposed)', 'Marc Edwards (Virginia Tech researcher)', 'Community activists'],
    narrative_arc: 'Mother who first sounded the alarm about Flint\'s water. Her children\'s blood lead levels were off the charts. She fought city, state, and federal agencies who all insisted the water was safe. Her persistence, and her decision to send water samples to Virginia Tech, eventually broke the cover-up open.',
    why_this_character_matters: 'LeeAnne\'s dome maps environmental racism with precision. Layer 9 (Environment) dominates — lead in the water that the government knew about and covered up. Her dome reveals the full cost of infrastructure neglect to a single family.',
    source_urls: [],
    scraped_at: new Date().toISOString(),
  },

  // ══════════════════════════════════════════════════════════════════════════════
  // PROPUBLICA / MARSHALL PROJECT — Kalief Browder
  // ══════════════════════════════════════════════════════════════════════════════

  {
    name: 'Kalief Browder',
    real_or_fictional: 'real',
    source_work: 'Kalief Browder Investigation (New Yorker / ProPublica / Marshall Project)',
    source_author_creator: 'Jennifer Gonnerman (New Yorker)',
    source_year: 2014,
    circumstances: ['detained', 'incarcerated', 'mental_illness', 'trauma', 'poverty'],
    location: 'Bronx, NY; Rikers Island, NY',
    time_period: '2010-2015',
    systems_touched: ['NYPD', 'Rikers Island', 'Bronx criminal court', 'bail system', 'solitary confinement', 'mental health', 'Medicaid'],
    dome_layer_richness: { 1: 10, 2: 6, 3: 7, 4: 9, 5: 7, 6: 5, 7: 6, 8: 7, 9: 5, 10: 10, 11: 3, 12: 7 },
    key_relationships: ['Venida Browder (mother)', 'Siblings', 'Defense attorney'],
    narrative_arc: 'Sixteen-year-old held at Rikers for 3 years without trial for allegedly stealing a backpack. Could not make $3,000 bail. Spent 2 of 3 years in solitary confinement. Repeatedly beaten. Case eventually dismissed. Died by suicide at 22. His story changed bail reform nationally.',
    why_this_character_matters: 'Kalief\'s dome is the definitive indictment of pretrial detention. Layer 1 (Legal) shows a system that held a child for 3 years for a crime that was never proven. Layer 10 (Autonomy) shows what solitary confinement does to a developing mind. The $3,000 bail is the dome\'s financial hinge.',
    source_urls: ['https://www.newyorker.com/magazine/2014/10/06/before-the-law'],
    scraped_at: new Date().toISOString(),
  },

  // ══════════════════════════════════════════════════════════════════════════════
  // TAMPA BAY TIMES — Failure Factories (2015)
  // Pinellas County, FL — school resegregation
  // ══════════════════════════════════════════════════════════════════════════════

  {
    name: 'Students of the Five Failure Factories',
    real_or_fictional: 'real',
    source_work: 'Failure Factories (Tampa Bay Times)',
    source_author_creator: 'Cara Fitzpatrick, Lisa Gartner, Michael LaForgia',
    source_year: 2015,
    circumstances: ['poverty', 'dropout', 'housing_insecure'],
    location: 'Pinellas County, FL (south St. Petersburg)',
    time_period: '2007-2015',
    systems_touched: ['public schools', 'school board', 'housing', 'juvenile justice', 'NAACP'],
    dome_layer_richness: { 1: 5, 2: 6, 3: 5, 4: 4, 5: 6, 6: 5, 7: 10, 8: 8, 9: 6, 10: 6, 11: 3, 12: 4 },
    key_relationships: ['Teachers', 'Parents', 'School administrators'],
    narrative_arc: 'The Tampa Bay Times documented how Pinellas County systematically resegregated five elementary schools by ending school choice programs, concentrating poverty and Black students into schools that then received fewer resources. Test scores collapsed. Violence increased. The schools became failure factories.',
    why_this_character_matters: 'This dome fills Layer 7 (Education) with the mechanics of school failure — not student failure but institutional failure. The dome reveals how housing policy (Layer 5) creates school composition (Layer 7) which determines educational outcomes.',
    source_urls: ['https://projects.tampabay.com/projects/2015/investigations/pinellas-failure-factories/'],
    scraped_at: new Date().toISOString(),
  },

  // ══════════════════════════════════════════════════════════════════════════════
  // REUTERS — Breathing Toxic Air
  // Lead contamination in American neighborhoods
  // ══════════════════════════════════════════════════════════════════════════════

  {
    name: 'Children of East Chicago',
    real_or_fictional: 'real',
    source_work: 'Unsafe at Any Level (Reuters)',
    source_author_creator: 'M.B. Pell, Joshua Schneyer',
    source_year: 2016,
    circumstances: ['environmental_exposure', 'poverty', 'housing_insecure', 'chronic_illness'],
    location: 'East Chicago, IN (West Calumet Housing Complex)',
    time_period: '2016',
    systems_touched: ['EPA Superfund', 'public housing', 'schools', 'Medicaid', 'lead testing', 'state health department'],
    dome_layer_richness: { 1: 7, 2: 6, 3: 5, 4: 9, 5: 8, 6: 5, 7: 6, 8: 7, 9: 10, 10: 6, 11: 3, 12: 4 },
    key_relationships: ['Parents', 'EPA officials', 'Housing authority'],
    narrative_arc: 'Children living in public housing built on a former lead smelter site. Blood lead levels were catastrophically high. The EPA knew for years. The housing authority knew. Nobody moved the families. Reuters mapped 3,810 neighborhoods nationwide with lead exposure rates double Flint\'s.',
    why_this_character_matters: 'This dome maps environmental poisoning as housing policy. Layer 9 (Environment) and Layer 5 (Housing) are inseparable — the government built homes on poison and then didn\'t tell the residents. The children\'s Layer 4 (Health) damage is permanent.',
    source_urls: ['https://www.reuters.com/investigates/special-report/usa-lead-testing/'],
    scraped_at: new Date().toISOString(),
  },

  // ══════════════════════════════════════════════════════════════════════════════
  // MARSHALL PROJECT — Life After Death Row
  // Exonerees rebuilding
  // ══════════════════════════════════════════════════════════════════════════════

  {
    name: 'Ricky Jackson',
    real_or_fictional: 'real',
    source_work: 'Life After Death Row (Marshall Project)',
    source_author_creator: 'Maurice Chammah',
    source_year: 2015,
    circumstances: ['wrongly_convicted', 'incarcerated', 'formerly_incarcerated', 'poverty', 'housing_insecure', 'isolation'],
    location: 'Cleveland, OH',
    time_period: '1975-2014',
    systems_touched: ['criminal justice', 'prison', 'Ohio Innocence Project', 'reentry services', 'SSI', 'housing assistance'],
    dome_layer_richness: { 1: 10, 2: 7, 3: 7, 4: 6, 5: 7, 6: 8, 7: 4, 8: 7, 9: 4, 10: 9, 11: 4, 12: 7 },
    key_relationships: ['Brothers (also convicted)', 'Eddie Vernon (false witness)', 'Attorneys'],
    narrative_arc: 'Spent 39 years in prison — the longest wrongful imprisonment in US history — based on the testimony of a 12-year-old who recanted. Released at 57 into a world he didn\'t recognize, with no smartphone skills, no work history, no housing, and $75 from the state. The Marshall Project documented his reentry.',
    why_this_character_matters: 'Ricky\'s dome maps the total cost of wrongful conviction — 39 years × 12 layers = the most expensive dome failure in American history. His reentry dome shows what happens when every layer must be rebuilt simultaneously from zero.',
    source_urls: ['https://www.themarshallproject.org/'],
    scraped_at: new Date().toISOString(),
  },

  // ══════════════════════════════════════════════════════════════════════════════
  // NYT — Disability Benefits Investigation
  // ══════════════════════════════════════════════════════════════════════════════

  {
    name: 'The Hale County Disabled',
    real_or_fictional: 'real',
    source_work: 'Unfit for Work (NPR Planet Money / This American Life)',
    source_author_creator: 'Chana Joffe-Walt',
    source_year: 2013,
    circumstances: ['disability', 'poverty', 'unemployed', 'chronic_illness'],
    location: 'Hale County, AL',
    time_period: '2013',
    systems_touched: ['SSI', 'SSDI', 'disability determination', 'disability attorneys', 'Medicaid', 'schools', 'factories (closed)'],
    dome_layer_richness: { 1: 6, 2: 9, 3: 8, 4: 8, 5: 5, 6: 9, 7: 5, 8: 7, 9: 5, 10: 6, 11: 3, 12: 4 },
    key_relationships: ['Disability attorneys', 'Case workers', 'Former employers'],
    narrative_arc: 'In Hale County, Alabama, 1 in 4 working-age adults is on disability. Not because they\'re faking — because the factories closed and disability became the only remaining safety net. Joffe-Walt documents the system that converts unemployed people into disabled people because there is no other category for them.',
    why_this_character_matters: 'This dome reveals how Layer 6 (Economic) collapse forces people into Layer 4 (Health) systems. When work disappears, disability becomes the only remaining door. The dome maps the economics of deindustrialization as a health condition.',
    source_urls: ['https://apps.npr.org/unfit-for-work/'],
    scraped_at: new Date().toISOString(),
  },

  // ══════════════════════════════════════════════════════════════════════════════
  // PROPUBLICA — Segregation in Medical Algorithms
  // ══════════════════════════════════════════════════════════════════════════════

  {
    name: 'The Undercounted Kidney Patients',
    real_or_fictional: 'real',
    source_work: 'Dissecting Racial Bias in an Algorithm (ProPublica / Science)',
    source_author_creator: 'Ziad Obermeyer et al.',
    source_year: 2019,
    circumstances: ['chronic_illness', 'poverty', 'uninsured'],
    location: 'Nationwide',
    time_period: '2019',
    systems_touched: ['hospitals', 'insurance', 'care management algorithms', 'Medicaid', 'dialysis centers'],
    dome_layer_richness: { 1: 5, 2: 8, 3: 7, 4: 10, 5: 3, 6: 4, 7: 3, 8: 4, 9: 3, 10: 7, 11: 2, 12: 4 },
    key_relationships: ['Healthcare providers', 'Insurance companies'],
    narrative_arc: 'A widely used algorithm determined that Black patients needed less care than equally sick white patients because it used healthcare spending as a proxy for health need. Since Black patients had historically received less care (due to access barriers), the algorithm concluded they were healthier. Obermeyer documented how the algorithm reduced care referrals for Black patients by more than half.',
    why_this_character_matters: 'This dome reveals how Layer 2 (Systems) automates inequality. The algorithm\'s logic: past discrimination → less spending → "lower need" → continued discrimination. Building domes around these patients with real health data (not spending data) reveals the gap.',
    source_urls: ['https://www.science.org/doi/10.1126/science.aax2342'],
    scraped_at: new Date().toISOString(),
  },

  // ══════════════════════════════════════════════════════════════════════════════
  // WASHINGTON POST — Afghanistan Papers
  // Veterans returning from documented failure
  // ══════════════════════════════════════════════════════════════════════════════

  {
    name: 'The Afghanistan Veterans',
    real_or_fictional: 'real',
    source_work: 'The Afghanistan Papers (Washington Post)',
    source_author_creator: 'Craig Whitlock',
    source_year: 2019,
    circumstances: ['veteran', 'mental_illness', 'trauma', 'addiction', 'homeless'],
    location: 'Nationwide',
    time_period: '2001-2021',
    systems_touched: ['military', 'VA hospitals', 'VA benefits', 'GI Bill', 'homeless veteran programs', 'mental health', 'disability determination'],
    dome_layer_richness: { 1: 6, 2: 8, 3: 7, 4: 9, 5: 6, 6: 6, 7: 5, 8: 7, 9: 5, 10: 7, 11: 3, 12: 6 },
    key_relationships: ['Fellow veterans', 'VA staff', 'Families'],
    narrative_arc: 'Veterans returning from a war their own leaders knew was failing. The Afghanistan Papers revealed that senior officials consistently lied about progress. Veterans came home with PTSD, traumatic brain injuries, and moral injury from a war documented as fraudulent.',
    why_this_character_matters: 'This dome maps the veteran reentry pipeline. Layer 4 (Health) carries combat trauma. Layer 2 (Systems) maps VA navigation. Layer 1 (Legal) covers benefits claims. The dome reveals the gap between what veterans were promised and what they received.',
    source_urls: ['https://www.washingtonpost.com/graphics/2019/investigations/afghanistan-papers/afghanistan-war-confidential-documents/'],
    scraped_at: new Date().toISOString(),
  },

  // ══════════════════════════════════════════════════════════════════════════════
  // LOCAL — Philadelphia Inquirer Toxic City (2017)
  // Lead paint in Philadelphia
  // ══════════════════════════════════════════════════════════════════════════════

  {
    name: 'Philadelphia Lead-Poisoned Children',
    real_or_fictional: 'real',
    source_work: 'Toxic City: Sick Kids and Dirty Homes (Philadelphia Inquirer)',
    source_author_creator: 'Barbara Laker, Wendy Ruderman',
    source_year: 2017,
    circumstances: ['environmental_exposure', 'poverty', 'housing_insecure', 'chronic_illness'],
    location: 'Philadelphia, PA (North Philadelphia, Kensington)',
    time_period: '2017',
    systems_touched: ['health department', 'landlords', 'code enforcement', 'schools', 'Medicaid', 'early intervention', 'lead abatement'],
    dome_layer_richness: { 1: 7, 2: 7, 3: 6, 4: 9, 5: 9, 6: 4, 7: 6, 8: 7, 9: 10, 10: 6, 11: 3, 12: 4 },
    key_relationships: ['Parents', 'Landlords', 'Health department inspectors'],
    narrative_arc: 'The Inquirer documented how thousands of Philadelphia children are lead-poisoned every year in rental housing with known lead paint hazards. The city health department knew which properties were dangerous but couldn\'t force remediation. Landlords kept renting. Children kept getting poisoned.',
    why_this_character_matters: 'This dome connects BATHS\' home geography (Philadelphia, FIPS 42101) to environmental health catastrophe. Layer 9 and Layer 4 are inseparable — the paint in the walls enters the blood of the children who live behind them.',
    source_urls: ['https://www.inquirer.com/news/inq/lead-paint-poison-children-asbestos-mold-housing-philadelphia-toxic-city-20170618.html'],
    scraped_at: new Date().toISOString(),
  },

  // ══════════════════════════════════════════════════════════════════════════════
  // PROPUBLICA — The TurboTax Trap (2019)
  // IRS Free File and the poor
  // ══════════════════════════════════════════════════════════════════════════════

  {
    name: 'The Free File Denied Taxpayers',
    real_or_fictional: 'real',
    source_work: 'The TurboTax Trap (ProPublica)',
    source_author_creator: 'Justin Elliott, Lucas Waldron',
    source_year: 2019,
    circumstances: ['poverty', 'working_poor', 'debt'],
    location: 'Nationwide',
    time_period: '2019',
    systems_touched: ['IRS', 'TurboTax', 'H&R Block', 'EITC', 'tax preparation industry'],
    dome_layer_richness: { 1: 5, 2: 9, 3: 10, 4: 2, 5: 3, 6: 6, 7: 3, 8: 4, 9: 2, 10: 5, 11: 2, 12: 3 },
    key_relationships: ['IRS', 'Tax preparation companies'],
    narrative_arc: 'ProPublica documented how Intuit (TurboTax) deliberately hid the free version of its tax software that it was legally required to offer low-income taxpayers. Millions of people who qualified for free filing were steered to paid products, losing hundreds of dollars from their EITC refunds — the very money designed to lift them out of poverty.',
    why_this_character_matters: 'This dome reveals Layer 2 (Systems) and Layer 3 (Fiscal) in collision. The system designed to return money to the poor (EITC) is intercepted by the system designed to process it (TurboTax). The fragmentation tax is literal.',
    source_urls: ['https://www.propublica.org/article/inside-turbotax-20-year-fight-to-stop-americans-from-filing-their-taxes-for-free'],
    scraped_at: new Date().toISOString(),
  },

  // ══════════════════════════════════════════════════════════════════════════════
  // REVEAL / CENTER FOR INVESTIGATIVE REPORTING — Modern Slavery
  // ══════════════════════════════════════════════════════════════════════════════

  {
    name: 'The Trafficked Farm Workers',
    real_or_fictional: 'real',
    source_work: 'Trafficked into Forced Labor (Reveal / CIR)',
    source_author_creator: 'Bernice Yeung, Grace Rubenstein',
    source_year: 2016,
    circumstances: ['trafficking', 'forced_labor', 'immigrant', 'undocumented', 'housing_insecure', 'poverty'],
    location: 'California Central Valley; Georgia; multiple states',
    time_period: '2010s',
    systems_touched: ['H-2A visa program', 'Department of Labor', 'immigration enforcement', 'farm labor contractors', 'courts'],
    dome_layer_richness: { 1: 8, 2: 6, 3: 7, 4: 5, 5: 7, 6: 9, 7: 3, 8: 6, 9: 7, 10: 10, 11: 2, 12: 4 },
    key_relationships: ['Labor contractors', 'Other workers', 'Legal aid attorneys'],
    narrative_arc: 'Workers brought to the US on temporary agricultural visas and then trapped — passports confiscated, housed in labor camps, paid below minimum wage, threatened with deportation if they complained. Reveal documented the supply chain from recruitment in home countries to exploitation in American fields.',
    why_this_character_matters: 'This dome maps modern slavery in America. Layer 10 (Autonomy) is at zero — these workers had no freedom of movement, no ability to leave. Layer 1 (Legal) shows how immigration law creates the conditions for trafficking by tying visas to specific employers.',
    source_urls: ['https://revealnews.org/topic/forced-labor/'],
    scraped_at: new Date().toISOString(),
  },

  // ══════════════════════════════════════════════════════════════════════════════
  // NYT — Invisible Child (original series before the book)
  // ══════════════════════════════════════════════════════════════════════════════

  {
    name: 'The Auburn Shelter Families',
    real_or_fictional: 'real',
    source_work: 'Invisible Child (NYT Series)',
    source_author_creator: 'Andrea Elliott',
    source_year: 2013,
    circumstances: ['homeless', 'shelter', 'poverty', 'single_parent'],
    location: 'Brooklyn, NY (Auburn Family Residence)',
    time_period: '2012-2013',
    systems_touched: ['NYC Department of Homeless Services', 'shelters', 'schools', 'Medicaid', 'SNAP', 'child welfare'],
    dome_layer_richness: { 1: 5, 2: 9, 3: 7, 4: 6, 5: 10, 6: 5, 7: 7, 8: 8, 9: 8, 10: 6, 11: 4, 12: 5 },
    key_relationships: ['Other shelter families', 'Shelter staff', 'Teachers'],
    narrative_arc: 'Beyond Dasani, Elliott documented the Auburn shelter system itself — 433 children in a former jail, sharing one communal bathroom per floor, passing through metal detectors to enter their home. The 5-part NYT series is a systems map of how NYC warehouses its homeless children.',
    why_this_character_matters: 'The Auburn families collectively map the shelter system as environment. Their dome reveals Layer 9 (Environment) inside a shelter — the physical conditions that are supposed to be temporary but become years.',
    source_urls: ['https://www.nytimes.com/projects/2013/invisible-child/'],
    scraped_at: new Date().toISOString(),
  },

  // ══════════════════════════════════════════════════════════════════════════════
  // PROPUBLICA — Dollars for Docs
  // Pharmaceutical industry payments to doctors
  // ══════════════════════════════════════════════════════════════════════════════

  {
    name: 'The Opioid-Prescribed Patients of WV',
    real_or_fictional: 'real',
    source_work: 'The Pain Hustlers / Opioid Files (multiple outlets)',
    source_author_creator: 'Evan Hughes, Scott Higham (WaPo), Eric Eyre (Charleston Gazette-Mail)',
    source_year: 2018,
    circumstances: ['addiction', 'chronic_illness', 'poverty', 'disability', 'bereavement'],
    location: 'West Virginia (Mingo, Logan, Kermit)',
    time_period: '2006-2016',
    systems_touched: ['pharmacies', 'pain clinics', 'DEA', 'Medicaid', 'hospitals', 'funeral homes', 'disability system'],
    dome_layer_richness: { 1: 7, 2: 7, 3: 7, 4: 10, 5: 5, 6: 7, 7: 4, 8: 8, 9: 5, 10: 6, 11: 3, 12: 5 },
    key_relationships: ['Doctors', 'Pharmacists', 'Drug distributors', 'Families of deceased'],
    narrative_arc: 'Eric Eyre documented that drug companies shipped 780 million opioid pills to West Virginia in 6 years — enough for 433 pills per person. The Charleston Gazette-Mail revealed that in Kermit (population 392), a single pharmacy received 9 million hydrocodone pills in 2 years. The patients who received these prescriptions were overwhelmingly on Medicaid and disability.',
    why_this_character_matters: 'This dome maps the pharmaceutical supply chain as it enters the body. Layer 4 (Health) shows the medical system as drug delivery mechanism. Layer 3 (Fiscal) shows Medicaid paying for the pills that killed its own enrollees.',
    source_urls: [],
    scraped_at: new Date().toISOString(),
  },
]
