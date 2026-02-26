/**
 * CHARACTER FRAGMENT — Nonfiction Book Sources
 *
 * Real people whose circumstances have been documented in nonfiction books
 * with enough detail to build domes. These are not celebrities — they are
 * people whose housing, health, legal, economic, community, and environmental
 * circumstances were recorded by journalists and scholars.
 */

export default [

  // ══════════════════════════════════════════════════════════════════════════════
  // EVICTED by Matthew Desmond (2016)
  // Milwaukee, WI — housing crisis documented in extraordinary detail
  // ══════════════════════════════════════════════════════════════════════════════

  {
    name: 'Arleen Belle',
    real_or_fictional: 'real',
    source_work: 'Evicted: Poverty and Profit in the American City',
    source_author_creator: 'Matthew Desmond',
    source_year: 2016,
    circumstances: ['evicted', 'poverty', 'single_parent', 'housing_insecure', 'mental_illness', 'domestic_violence'],
    location: 'Milwaukee, WI',
    time_period: '2008-2009',
    systems_touched: ['landlord-tenant court', 'welfare', 'public housing', 'shelters', 'child welfare', 'schools', 'SNAP', 'W-2 (Wisconsin Works)'],
    dome_layer_richness: { 1: 7, 2: 8, 3: 9, 4: 6, 5: 10, 6: 7, 7: 4, 8: 8, 9: 5, 10: 7, 11: 3, 12: 4 },
    key_relationships: ['Jori (son)', 'Jafaris (son)', 'Crystal Mayberry', 'Sherrena Tarver (landlord)'],
    narrative_arc: 'Cycles through 5 addresses in 2 years. Each eviction destabilizes every other system — kids change schools, benefits get disrupted, depression deepens. The eviction record itself becomes a barrier to future housing, creating a downward spiral that Desmond documents with financial precision.',
    why_this_character_matters: 'Arleen is the most comprehensively documented eviction case in American nonfiction. Building a dome around her reveals exactly how housing instability cascades across every other system — legal, fiscal, health, education, community. The coordinated cost vs. fragmented cost delta would be enormous.',
    source_urls: ['https://www.evictedbook.com/'],
    scraped_at: new Date().toISOString(),
  },

  {
    name: 'Crystal Mayberry',
    real_or_fictional: 'real',
    source_work: 'Evicted: Poverty and Profit in the American City',
    source_author_creator: 'Matthew Desmond',
    source_year: 2016,
    circumstances: ['evicted', 'foster_care', 'homeless', 'deep_poverty', 'trauma', 'isolation'],
    location: 'Milwaukee, WI',
    time_period: '2008-2009',
    systems_touched: ['foster care', 'shelters', 'landlord-tenant court', 'welfare', 'job training programs'],
    dome_layer_richness: { 1: 5, 2: 7, 3: 6, 4: 5, 5: 9, 6: 6, 7: 3, 8: 8, 9: 4, 10: 7, 11: 2, 12: 5 },
    key_relationships: ['Arleen Belle', 'Various landlords'],
    narrative_arc: 'Aged out of foster care at 18 into homelessness. No safety net caught her. Cycles through shelters, doubled-up situations, and evictions. The system that was supposed to protect her as a child released her into a housing market she could not navigate alone.',
    why_this_character_matters: 'Crystal represents the foster-care-to-homelessness pipeline. Her dome would reveal the catastrophic gap between child welfare and adult housing systems — the moment the state stops being responsible for you.',
    source_urls: ['https://www.evictedbook.com/'],
    scraped_at: new Date().toISOString(),
  },

  {
    name: 'Scott Bunker',
    real_or_fictional: 'real',
    source_work: 'Evicted: Poverty and Profit in the American City',
    source_author_creator: 'Matthew Desmond',
    source_year: 2016,
    circumstances: ['evicted', 'addiction', 'formerly_incarcerated', 'poverty', 'housing_insecure'],
    location: 'Milwaukee, WI',
    time_period: '2008-2009',
    systems_touched: ['criminal justice', 'rehab', 'landlord-tenant court', 'rooming houses', 'nursing homes'],
    dome_layer_richness: { 1: 7, 2: 5, 3: 7, 4: 8, 5: 9, 6: 6, 7: 3, 8: 6, 9: 4, 10: 6, 11: 3, 12: 4 },
    key_relationships: ['Other rooming house residents', 'Sherrena Tarver (landlord)'],
    narrative_arc: 'Former nurse whose addiction cost him his career, freedom, and housing. Desmond documents his attempts at sobriety, the economics of rooming houses, and how the housing market creates a separate tier for people with criminal records and addiction histories.',
    why_this_character_matters: 'Scott shows how addiction, incarceration, and housing markets interact. His dome reveals the fiscal architecture of bottom-tier housing — rooming houses that charge per week, extracting maximum rent from people with minimum options.',
    source_urls: ['https://www.evictedbook.com/'],
    scraped_at: new Date().toISOString(),
  },

  {
    name: 'Lamar',
    real_or_fictional: 'real',
    source_work: 'Evicted: Poverty and Profit in the American City',
    source_author_creator: 'Matthew Desmond',
    source_year: 2016,
    circumstances: ['disability', 'poverty', 'housing_insecure', 'single_parent', 'evicted'],
    location: 'Milwaukee, WI',
    time_period: '2008-2009',
    systems_touched: ['SSI', 'disability services', 'landlord-tenant court', 'schools', 'child welfare'],
    dome_layer_richness: { 1: 5, 2: 6, 3: 8, 4: 7, 5: 9, 6: 5, 7: 4, 8: 7, 9: 5, 10: 6, 11: 4, 12: 5 },
    key_relationships: ['Two sons', 'Neighbors in trailer park'],
    narrative_arc: 'Lost both legs, raising two sons on SSI in a dilapidated trailer park. His disability income is consumed almost entirely by rent. Desmond documents with precision how the disability benefits system interacts with the housing market to keep him trapped.',
    why_this_character_matters: 'Lamar reveals how disability benefits get captured by landlords. His dome would show that SSI was designed to support independence but the housing market converts it into landlord revenue.',
    source_urls: ['https://www.evictedbook.com/'],
    scraped_at: new Date().toISOString(),
  },

  {
    name: 'Sherrena Tarver',
    real_or_fictional: 'real',
    source_work: 'Evicted: Poverty and Profit in the American City',
    source_author_creator: 'Matthew Desmond',
    source_year: 2016,
    circumstances: ['wealth'],
    location: 'Milwaukee, WI',
    time_period: '2008-2009',
    systems_touched: ['landlord-tenant court', 'property management', 'code enforcement', 'tax system'],
    dome_layer_richness: { 1: 7, 2: 4, 3: 10, 4: 2, 5: 8, 6: 9, 7: 3, 8: 6, 9: 5, 10: 8, 11: 3, 12: 4 },
    key_relationships: ['Arleen Belle (tenant)', 'Quentin (husband/partner)', 'Multiple tenants'],
    narrative_arc: 'Landlord who profits from the eviction economy. Desmond documents her business model in detail — how she extracts rent from the poorest tenants, uses eviction court as a management tool, and accumulates property. She is the system viewed from the other side.',
    why_this_character_matters: 'Building a dome around a landlord reveals the profit structure of poverty housing. Her dome is the inverse of her tenants — where their layers are thin, hers are thick. The delta between her dome and Arleen\'s is the architecture of extraction.',
    source_urls: ['https://www.evictedbook.com/'],
    scraped_at: new Date().toISOString(),
  },

  // ══════════════════════════════════════════════════════════════════════════════
  // RANDOM FAMILY by Adrian Nicole LeBlanc (2003)
  // Bronx, NY — 11 years of immersive reporting on poverty, drugs, incarceration
  // ══════════════════════════════════════════════════════════════════════════════

  {
    name: 'Jessica',
    real_or_fictional: 'real',
    source_work: 'Random Family: Love, Drugs, Trouble, and Coming of Age in the Bronx',
    source_author_creator: 'Adrian Nicole LeBlanc',
    source_year: 2003,
    circumstances: ['poverty', 'incarcerated', 'domestic_violence', 'addiction', 'single_parent', 'housing_insecure'],
    location: 'Bronx, NY',
    time_period: '1988-2000',
    systems_touched: ['criminal justice', 'prison', 'welfare', 'child welfare', 'public housing', 'courts', 'schools', 'hospitals'],
    dome_layer_richness: { 1: 9, 2: 7, 3: 7, 4: 6, 5: 8, 6: 6, 7: 4, 8: 9, 9: 5, 10: 8, 11: 5, 12: 6 },
    key_relationships: ['Boy George (partner)', 'Coco (friend)', 'Serena (daughter)', 'Multiple children', 'Lourdes (mother)'],
    narrative_arc: 'Beautiful teenager drawn into the drug economy through her boyfriend Boy George. LeBlanc follows her through federal prison, multiple children by different fathers, release, and the struggle to rebuild. 11 years of documentation captures every system she touches.',
    why_this_character_matters: 'Jessica is documented across a longer time span than almost any other character in American nonfiction. Her dome would track system interactions over 11 years — the temporal dimension reveals how systems compound disadvantage over time.',
    source_urls: [],
    scraped_at: new Date().toISOString(),
  },

  {
    name: 'Coco',
    real_or_fictional: 'real',
    source_work: 'Random Family: Love, Drugs, Trouble, and Coming of Age in the Bronx',
    source_author_creator: 'Adrian Nicole LeBlanc',
    source_year: 2003,
    circumstances: ['poverty', 'single_parent', 'domestic_violence', 'housing_insecure', 'dropout', 'trauma'],
    location: 'Bronx, NY; Troy, NY',
    time_period: '1988-2000',
    systems_touched: ['welfare', 'public housing', 'WIC', 'SNAP', 'Medicaid', 'schools', 'child welfare', 'domestic violence services'],
    dome_layer_richness: { 1: 5, 2: 8, 3: 8, 4: 6, 5: 8, 6: 7, 7: 5, 8: 9, 9: 5, 10: 6, 11: 4, 12: 5 },
    key_relationships: ['Jessica', 'Cesar (partner)', 'Mercedes, Nikki, Nautica, Pearl (daughters)', 'Foxy (mother)'],
    narrative_arc: 'Navigates welfare, public housing, and raising four daughters largely alone while partners cycle through incarceration. LeBlanc documents every welfare appointment, every housing application, every school enrollment — the bureaucratic texture of poverty.',
    why_this_character_matters: 'Coco\'s dome would be the most detailed map of Layer 2 (Systems) ever built. LeBlanc documented her bureaucratic navigation with extraordinary precision — every form, every office, every denial and approval.',
    source_urls: [],
    scraped_at: new Date().toISOString(),
  },

  // ══════════════════════════════════════════════════════════════════════════════
  // INVISIBLE CHILD by Andrea Elliott (2021)
  // Brooklyn, NY — 12 years following one homeless child
  // ══════════════════════════════════════════════════════════════════════════════

  {
    name: 'Dasani Coates',
    real_or_fictional: 'real',
    source_work: 'Invisible Child: Poverty, Survival & Hope in an American City',
    source_author_creator: 'Andrea Elliott',
    source_year: 2021,
    circumstances: ['homeless', 'poverty', 'shelter', 'foster_care', 'trauma', 'child_labor'],
    location: 'Brooklyn, NY; Hershey, PA',
    time_period: '2003-2020',
    systems_touched: ['shelters', 'child welfare', 'schools', 'homeless services', 'foster care', 'courts', 'Medicaid', 'SNAP', 'Milton Hershey School'],
    dome_layer_richness: { 1: 6, 2: 9, 3: 7, 4: 7, 5: 10, 6: 5, 7: 9, 8: 9, 9: 7, 10: 8, 11: 7, 12: 8 },
    key_relationships: ['Chanel (mother)', 'Supreme (father)', '7 siblings', 'Teachers', 'Social workers'],
    narrative_arc: 'Born into homelessness in Brooklyn, growing up in the Auburn shelter. Elliott follows her for 12 years — through shelter life, school struggles, a scholarship to a boarding school in Pennsylvania, the pull between family and opportunity, and eventual return. The most granular documentation of child homelessness ever published.',
    why_this_character_matters: 'Dasani has the richest dome of any documented child in American nonfiction. 12 years of reporting means every layer has material. Her dome reveals how childhood homelessness interacts with education, health, community, and autonomy across a full developmental arc.',
    source_urls: ['https://www.nytimes.com/projects/2013/invisible-child/'],
    scraped_at: new Date().toISOString(),
  },

  {
    name: 'Chanel Sykes',
    real_or_fictional: 'real',
    source_work: 'Invisible Child: Poverty, Survival & Hope in an American City',
    source_author_creator: 'Andrea Elliott',
    source_year: 2021,
    circumstances: ['homeless', 'addiction', 'poverty', 'domestic_violence', 'shelter', 'mental_illness', 'single_parent'],
    location: 'Brooklyn, NY',
    time_period: '2003-2020',
    systems_touched: ['shelters', 'child welfare', 'courts', 'rehab', 'welfare', 'Medicaid', 'SNAP', 'public housing waitlist'],
    dome_layer_richness: { 1: 7, 2: 9, 3: 8, 4: 8, 5: 10, 6: 6, 7: 4, 8: 7, 9: 6, 10: 6, 11: 4, 12: 4 },
    key_relationships: ['Dasani (daughter)', 'Supreme (partner)', '7 children', 'Shelter staff', 'Case workers'],
    narrative_arc: 'Mother of 8 navigating the shelter system while battling addiction, domestic violence, and child welfare investigations. Elliott documents the impossible calculus: comply with every agency requirement while housed in a building with no kitchen, no privacy, and constant surveillance.',
    why_this_character_matters: 'Chanel is the adult counterpart to Dasani — her dome shows the parent side of family homelessness, where every system demands compliance while providing contradictory instructions and insufficient resources.',
    source_urls: [],
    scraped_at: new Date().toISOString(),
  },

  // ══════════════════════════════════════════════════════════════════════════════
  // NICKEL AND DIMED by Barbara Ehrenreich (2001)
  // Multiple US locations — undercover documentation of low-wage work
  // ══════════════════════════════════════════════════════════════════════════════

  {
    name: 'Barbara Ehrenreich (as worker)',
    real_or_fictional: 'real',
    source_work: 'Nickel and Dimed: On (Not) Getting By in America',
    source_author_creator: 'Barbara Ehrenreich',
    source_year: 2001,
    circumstances: ['working_poor', 'housing_insecure'],
    location: 'Key West, FL; Portland, ME; Minneapolis, MN',
    time_period: '1998-2000',
    systems_touched: ['temp agencies', 'fast food', 'retail', 'housekeeping', 'nursing homes', 'Walmart'],
    dome_layer_richness: { 1: 3, 2: 4, 3: 9, 4: 6, 5: 8, 6: 10, 7: 3, 8: 5, 9: 5, 10: 7, 11: 3, 12: 5 },
    key_relationships: ['Co-workers at each job', 'Managers', 'Holly (Walmart co-worker)'],
    narrative_arc: 'Journalist goes undercover as a low-wage worker in three American cities. Documents with financial precision how minimum-wage math doesn\'t work — the gap between wages and rent is unbridgeable without assistance. The body breaks down, the math never adds up.',
    why_this_character_matters: 'The first systematic documentation of the working-poor fiscal architecture. Her dome would show Layer 3 (Fiscal) and Layer 6 (Economic) in extraordinary detail — the exact math of why you cannot survive on minimum wage in any American city.',
    source_urls: [],
    scraped_at: new Date().toISOString(),
  },

  // ══════════════════════════════════════════════════════════════════════════════
  // BEHIND THE BEAUTIFUL FOREVERS by Katherine Boo (2012)
  // Mumbai, India — life in a slum next to the airport
  // ══════════════════════════════════════════════════════════════════════════════

  {
    name: 'Abdul Husain',
    real_or_fictional: 'real',
    source_work: 'Behind the Beautiful Forevers: Life, Death, and Hope in a Mumbai Undercity',
    source_author_creator: 'Katherine Boo',
    source_year: 2012,
    circumstances: ['poverty', 'housing_insecure', 'wrongly_convicted', 'child_labor', 'immigrant'],
    location: 'Annawadi slum, Mumbai, India',
    time_period: '2007-2011',
    systems_touched: ['police', 'courts', 'recycling economy', 'hospitals', 'municipal government', 'schools'],
    dome_layer_richness: { 1: 9, 2: 6, 3: 8, 4: 5, 5: 8, 6: 9, 7: 4, 8: 8, 9: 8, 10: 7, 11: 3, 12: 5 },
    key_relationships: ['Karam (father)', 'Zehrunisa (mother)', 'Kehkashan (sister)', 'Fatima (neighbor)'],
    narrative_arc: 'Teenage garbage sorter who is the primary earner for his family. When a neighbor self-immolates, his family is falsely accused. Boo documents his journey through Mumbai\'s criminal justice system — the corruption, the delays, the economics of innocence in a system where everything has a price.',
    why_this_character_matters: 'Abdul\'s dome bridges international systems. Building a dome with US systems applied to his Mumbai circumstances reveals universal patterns in how poverty, housing, and justice interact — and where systems diverge.',
    source_urls: [],
    scraped_at: new Date().toISOString(),
  },

  {
    name: 'Asha Waghekar',
    real_or_fictional: 'real',
    source_work: 'Behind the Beautiful Forevers: Life, Death, and Hope in a Mumbai Undercity',
    source_author_creator: 'Katherine Boo',
    source_year: 2012,
    circumstances: ['poverty', 'housing_insecure'],
    location: 'Annawadi slum, Mumbai, India',
    time_period: '2007-2011',
    systems_touched: ['municipal politics', 'schools', 'police', 'slum redevelopment', 'NGOs'],
    dome_layer_richness: { 1: 6, 2: 7, 3: 7, 4: 3, 5: 7, 6: 8, 7: 6, 8: 9, 9: 6, 10: 8, 11: 4, 12: 6 },
    key_relationships: ['Manju (daughter)', 'Political party bosses', 'Slum residents'],
    narrative_arc: 'Aspiring slumlord who navigates corruption as a ladder out of poverty. Boo documents her political economy — how she brokers deals between slum residents, NGOs, and politicians, extracting a percentage at every step.',
    why_this_character_matters: 'Asha shows how informal power structures work inside communities that formal systems have abandoned. Her dome reveals Layer 8 (Community) as a shadow government.',
    source_urls: [],
    scraped_at: new Date().toISOString(),
  },

  // ══════════════════════════════════════════════════════════════════════════════
  // JUST MERCY by Bryan Stevenson (2014)
  // Alabama — wrongful conviction and death row
  // ══════════════════════════════════════════════════════════════════════════════

  {
    name: 'Walter McMillian',
    real_or_fictional: 'real',
    source_work: 'Just Mercy: A Story of Justice and Redemption',
    source_author_creator: 'Bryan Stevenson',
    source_year: 2014,
    circumstances: ['wrongly_convicted', 'incarcerated', 'poverty'],
    location: 'Monroeville, AL',
    time_period: '1986-1993',
    systems_touched: ['criminal justice', 'death row', 'courts', 'police', 'prison', 'public defender', 'Supreme Court'],
    dome_layer_richness: { 1: 10, 2: 5, 3: 6, 4: 6, 5: 7, 6: 7, 7: 3, 8: 8, 9: 4, 10: 9, 11: 3, 12: 7 },
    key_relationships: ['Bryan Stevenson (attorney)', 'Minnie McMillian (wife)', 'Ralph Myers (coerced witness)', 'Community supporters'],
    narrative_arc: 'Black man wrongly convicted of murder and sentenced to death in Alabama. Stevenson documents every stage of the legal system\'s failure — coerced witnesses, prosecutorial misconduct, racial bias, and the 6-year fight for exoneration.',
    why_this_character_matters: 'Walter\'s dome is a map of criminal justice failure. Every layer of the legal system that should have protected him instead convicted him. Building his dome reveals the cost — financial, human, communal — of wrongful conviction.',
    source_urls: [],
    scraped_at: new Date().toISOString(),
  },

  {
    name: 'Herbert Richardson',
    real_or_fictional: 'real',
    source_work: 'Just Mercy: A Story of Justice and Redemption',
    source_author_creator: 'Bryan Stevenson',
    source_year: 2014,
    circumstances: ['incarcerated', 'veteran', 'mental_illness', 'trauma'],
    location: 'Alabama',
    time_period: '1970s-1989',
    systems_touched: ['military', 'VA', 'criminal justice', 'death row', 'mental health', 'prison'],
    dome_layer_richness: { 1: 9, 2: 5, 3: 4, 4: 8, 5: 5, 6: 4, 7: 3, 8: 5, 9: 3, 10: 8, 11: 2, 12: 6 },
    key_relationships: ['Bryan Stevenson (attorney)', 'Fellow veterans'],
    narrative_arc: 'Vietnam veteran with severe PTSD who committed a crime while in a dissociative state. The military broke him, the VA failed him, and the criminal justice system executed him. Stevenson documents how combat trauma traveled through every system that touched him.',
    why_this_character_matters: 'Herbert\'s dome is a map of the veteran pipeline — from military trauma to inadequate VA care to criminal behavior to execution. Each system failure feeds the next.',
    source_urls: [],
    scraped_at: new Date().toISOString(),
  },

  {
    name: 'Anthony Ray Hinton',
    real_or_fictional: 'real',
    source_work: 'Just Mercy: A Story of Justice and Redemption',
    source_author_creator: 'Bryan Stevenson',
    source_year: 2014,
    circumstances: ['wrongly_convicted', 'incarcerated', 'poverty'],
    location: 'Alabama',
    time_period: '1985-2015',
    systems_touched: ['criminal justice', 'death row', 'courts', 'prison', 'Supreme Court'],
    dome_layer_richness: { 1: 10, 2: 4, 3: 5, 4: 5, 5: 5, 6: 5, 7: 3, 8: 7, 9: 3, 10: 9, 11: 4, 12: 8 },
    key_relationships: ['Bryan Stevenson (attorney)', 'Mother', 'Fellow death row inmates'],
    narrative_arc: 'Spent 30 years on death row for crimes he did not commit because his appointed lawyer couldn\'t afford a proper ballistics expert. Stevenson documents how poverty — the inability to pay for adequate defense — is itself a death sentence.',
    why_this_character_matters: 'Anthony Ray Hinton spent 30 years in a system that knew he was likely innocent. His dome reveals the fiscal architecture of injustice — the cost of a ballistics expert ($500-$1000) vs. the cost of 30 years on death row.',
    source_urls: [],
    scraped_at: new Date().toISOString(),
  },

  // ══════════════════════════════════════════════════════════════════════════════
  // THE OTHER AMERICA by Michael Harrington (1962)
  // America — the book that launched the War on Poverty
  // ══════════════════════════════════════════════════════════════════════════════

  {
    name: 'The Appalachian Miner',
    real_or_fictional: 'real',
    source_work: 'The Other America: Poverty in the United States',
    source_author_creator: 'Michael Harrington',
    source_year: 1962,
    circumstances: ['poverty', 'chronic_illness', 'unemployed', 'environmental_exposure', 'isolation'],
    location: 'Appalachia, WV/KY',
    time_period: '1950s-1960s',
    systems_touched: ['mining companies', 'black lung benefits', 'welfare', 'hospitals', 'schools'],
    dome_layer_richness: { 1: 4, 2: 5, 3: 7, 4: 8, 5: 6, 6: 8, 7: 5, 8: 7, 9: 9, 10: 5, 11: 3, 12: 4 },
    key_relationships: ['Mining community', 'Family'],
    narrative_arc: 'Composite of miners Harrington documented in Appalachia — men whose bodies were destroyed by coal dust, whose communities were owned by mining companies, whose economic options disappeared when mines closed. The environment literally killed them while the legal system protected the companies.',
    why_this_character_matters: 'The Appalachian miner dome reveals environmental-health-economic triangulation — how an industry can destroy bodies, communities, and landscapes simultaneously while extracting all the wealth.',
    source_urls: [],
    scraped_at: new Date().toISOString(),
  },

  // ══════════════════════════════════════════════════════════════════════════════
  // AMERICAN HUNGER / BLACK BOY by Richard Wright (1945)
  // Mississippi and Chicago — autobiography of growing up Black in the Jim Crow South
  // ══════════════════════════════════════════════════════════════════════════════

  {
    name: 'Richard Wright',
    real_or_fictional: 'real',
    source_work: 'Black Boy / American Hunger',
    source_author_creator: 'Richard Wright',
    source_year: 1945,
    circumstances: ['poverty', 'deep_poverty', 'orphan', 'child_labor', 'dropout', 'immigrant', 'food_desert'],
    location: 'Natchez, MS; Memphis, TN; Chicago, IL',
    time_period: '1908-1937',
    systems_touched: ['schools', 'Jim Crow legal system', 'welfare', 'WPA', 'factories', 'post office'],
    dome_layer_richness: { 1: 7, 2: 5, 3: 7, 4: 6, 5: 7, 6: 8, 7: 8, 8: 8, 9: 5, 10: 9, 11: 10, 12: 8 },
    key_relationships: ['Ella (mother)', 'Grandmother', 'Uncle', 'Communist Party members'],
    narrative_arc: 'From literal starvation in Mississippi to self-education to literary career. Wright documents hunger (real, physical hunger) as a constant. Every system he encounters — schools, jobs, libraries, legal restrictions — is shaped by Jim Crow. His escape is through literacy, which the South tried to deny him.',
    why_this_character_matters: 'Wright documented the sensory experience of poverty — what hunger feels like, what cold feels like, what fear of white violence feels like. His dome fills layers 10, 11, 12 (Autonomy, Creativity, Flourishing) with extraordinary depth.',
    source_urls: [],
    scraped_at: new Date().toISOString(),
  },

  // ══════════════════════════════════════════════════════════════════════════════
  // THE WARMTH OF OTHER SUNS by Isabel Wilkerson (2010)
  // Great Migration — three people who left the South
  // ══════════════════════════════════════════════════════════════════════════════

  {
    name: 'Ida Mae Brandon Gladney',
    real_or_fictional: 'real',
    source_work: 'The Warmth of Other Suns: The Epic Story of America\'s Great Migration',
    source_author_creator: 'Isabel Wilkerson',
    source_year: 2010,
    circumstances: ['poverty', 'displaced', 'immigrant'],
    location: 'Chickasaw County, MS → Chicago, IL',
    time_period: '1937-2000s',
    systems_touched: ['sharecropping system', 'Jim Crow', 'Chicago public housing', 'schools', 'factories', 'churches'],
    dome_layer_richness: { 1: 6, 2: 5, 3: 7, 4: 4, 5: 8, 6: 8, 7: 5, 8: 9, 9: 6, 10: 7, 11: 5, 12: 7 },
    key_relationships: ['George Gladney (husband)', 'Children', 'Church community in Chicago'],
    narrative_arc: 'Left Mississippi sharecropping after a relative was beaten. Wilkerson follows her entire life — the journey north, settling in Chicago, raising a family, watching the South Side transform. Her story spans 70 years of American racial and economic history.',
    why_this_character_matters: 'Ida Mae\'s dome spans the longest timeframe of any documented character — from 1930s sharecropping to 2000s Chicago. It reveals how migration transforms every dome layer simultaneously.',
    source_urls: [],
    scraped_at: new Date().toISOString(),
  },

  {
    name: 'George Swanson Starling',
    real_or_fictional: 'real',
    source_work: 'The Warmth of Other Suns: The Epic Story of America\'s Great Migration',
    source_author_creator: 'Isabel Wilkerson',
    source_year: 2010,
    circumstances: ['poverty', 'displaced', 'immigrant'],
    location: 'Eustis, FL → Harlem, NY',
    time_period: '1945-2000s',
    systems_touched: ['citrus industry', 'Jim Crow', 'railroads', 'New York transit', 'churches', 'unions'],
    dome_layer_richness: { 1: 7, 2: 4, 3: 6, 4: 4, 5: 6, 6: 8, 7: 5, 8: 8, 9: 5, 10: 7, 11: 4, 12: 6 },
    key_relationships: ['Inez (wife)', 'Children', 'Fellow migrants'],
    narrative_arc: 'Fled Florida after organizing citrus workers — his labor activism made him a target. Wilkerson documents his new life in Harlem, working as a railroad attendant, watching his children navigate a different but still constrained world.',
    why_this_character_matters: 'George\'s dome shows how labor organizing in one system (agriculture) creates legal danger that forces migration into another system (urban employment). The displacement is economic and political simultaneously.',
    source_urls: [],
    scraped_at: new Date().toISOString(),
  },

  {
    name: 'Robert Joseph Pershing Foster',
    real_or_fictional: 'real',
    source_work: 'The Warmth of Other Suns: The Epic Story of America\'s Great Migration',
    source_author_creator: 'Isabel Wilkerson',
    source_year: 2010,
    circumstances: ['displaced', 'immigrant'],
    location: 'Monroe, LA → Los Angeles, CA',
    time_period: '1953-2000s',
    systems_touched: ['Jim Crow medical system', 'hospitals', 'medical licensing', 'VA', 'military'],
    dome_layer_richness: { 1: 6, 2: 5, 3: 7, 4: 7, 5: 6, 6: 8, 7: 8, 8: 7, 9: 4, 10: 7, 11: 4, 12: 6 },
    key_relationships: ['Alice (wife)', 'Patients', 'Medical community'],
    narrative_arc: 'Black doctor who couldn\'t practice freely in Louisiana. Drove to Los Angeles alone, rebuilt his career, became a doctor to the stars while carrying the psychological weight of what the South denied him. Wilkerson documents how even professional success doesn\'t heal displacement.',
    why_this_character_matters: 'Robert shows that migration doesn\'t only happen to the poor. His dome reveals how racial systems constrain even the economically privileged — and how displacement affects Layer 12 (Flourishing) regardless of income.',
    source_urls: [],
    scraped_at: new Date().toISOString(),
  },

  // ══════════════════════════════════════════════════════════════════════════════
  // $2.00 A DAY by Kathryn Edin and H. Luke Shaefer (2015)
  // Multiple US locations — extreme poverty in America
  // ══════════════════════════════════════════════════════════════════════════════

  {
    name: 'Jennifer Hernandez',
    real_or_fictional: 'real',
    source_work: '$2.00 a Day: Living on Almost Nothing in America',
    source_author_creator: 'Kathryn Edin & H. Luke Shaefer',
    source_year: 2015,
    circumstances: ['deep_poverty', 'single_parent', 'housing_insecure', 'domestic_violence', 'trauma'],
    location: 'Chicago, IL',
    time_period: '2012-2013',
    systems_touched: ['TANF', 'SNAP', 'shelters', 'domestic violence services', 'welfare', 'child welfare'],
    dome_layer_richness: { 1: 5, 2: 8, 3: 10, 4: 5, 5: 8, 6: 7, 7: 4, 8: 6, 9: 5, 10: 6, 11: 3, 12: 4 },
    key_relationships: ['Children', 'Abusive partner', 'Shelter staff'],
    narrative_arc: 'Living on literally $2 a day with children after fleeing domestic violence. Edin and Shaefer document the precise economics of extreme poverty — how you eat, where you sleep, what you sell, what you trade when money runs out completely.',
    why_this_character_matters: 'Jennifer\'s dome fills Layer 3 (Fiscal) with more precision than any other character. The documentation of how someone survives on $2/day reveals the shadow economy that formal systems don\'t see.',
    source_urls: [],
    scraped_at: new Date().toISOString(),
  },

  {
    name: 'Rae McCormick',
    real_or_fictional: 'real',
    source_work: '$2.00 a Day: Living on Almost Nothing in America',
    source_author_creator: 'Kathryn Edin & H. Luke Shaefer',
    source_year: 2015,
    circumstances: ['deep_poverty', 'single_parent', 'housing_insecure', 'disability', 'environmental_exposure'],
    location: 'Johnson City, TN',
    time_period: '2012-2013',
    systems_touched: ['SNAP', 'SSI', 'welfare', 'schools', 'charity organizations', 'plasma donation centers'],
    dome_layer_richness: { 1: 4, 2: 7, 3: 10, 4: 6, 5: 7, 6: 7, 7: 5, 8: 6, 9: 5, 10: 5, 11: 3, 12: 4 },
    key_relationships: ['Children', 'Extended family'],
    narrative_arc: 'Sells plasma to feed her children. Edin and Shaefer document the literal marketplace of the body — how the poorest Americans convert their blood into food money, twice a week, at $30 per donation.',
    why_this_character_matters: 'Rae\'s dome reveals the plasma economy — a multi-billion dollar industry built on the blood of people in extreme poverty. Layer 4 (Health) and Layer 3 (Fiscal) intersect in her body.',
    source_urls: [],
    scraped_at: new Date().toISOString(),
  },

  // ══════════════════════════════════════════════════════════════════════════════
  // HILLBILLY ELEGY by J.D. Vance (2016)
  // Middletown, OH / Jackson, KY — Appalachian poverty and mobility
  // ══════════════════════════════════════════════════════════════════════════════

  {
    name: 'J.D. Vance',
    real_or_fictional: 'real',
    source_work: 'Hillbilly Elegy: A Memoir of a Family and Culture in Crisis',
    source_author_creator: 'J.D. Vance',
    source_year: 2016,
    circumstances: ['poverty', 'addiction', 'domestic_violence', 'foster_care', 'trauma'],
    location: 'Middletown, OH; Jackson, KY',
    time_period: '1984-2010s',
    systems_touched: ['schools', 'child welfare', 'military (Marines)', 'universities', 'legal system'],
    dome_layer_richness: { 1: 5, 2: 5, 3: 7, 4: 6, 5: 7, 6: 8, 7: 8, 8: 8, 9: 6, 10: 7, 11: 4, 12: 7 },
    key_relationships: ['Mamaw (grandmother)', 'Bev (mother)', 'Lindsay (sister)', 'Usha (wife)'],
    narrative_arc: 'Child of addiction and instability who made it to Yale Law School. The memoir documents the Appalachian family structure, the decline of Middletown, the role of grandparents as stabilizers, and how the military provided the structure his family couldn\'t.',
    why_this_character_matters: 'Vance\'s dome is a rare upward-mobility case. Comparing it to static-poverty domes reveals which systems enabled escape and which trapped others. The grandmother (Mamaw) is the key variable — community as rescue.',
    source_urls: [],
    scraped_at: new Date().toISOString(),
  },

  // ══════════════════════════════════════════════════════════════════════════════
  // THE GLASS CASTLE by Jeannette Walls (2005)
  // Welch, WV; Phoenix, AZ; NYC — childhood poverty with mentally ill parents
  // ══════════════════════════════════════════════════════════════════════════════

  {
    name: 'Jeannette Walls',
    real_or_fictional: 'real',
    source_work: 'The Glass Castle',
    source_author_creator: 'Jeannette Walls',
    source_year: 2005,
    circumstances: ['poverty', 'deep_poverty', 'homeless', 'housing_insecure', 'mental_illness', 'child_labor', 'food_desert'],
    location: 'Welch, WV; Phoenix, AZ; New York City, NY',
    time_period: '1960s-1990s',
    systems_touched: ['schools', 'child welfare (avoided)', 'hospitals', 'squatting'],
    dome_layer_richness: { 1: 4, 2: 3, 3: 7, 4: 6, 5: 9, 6: 7, 7: 7, 8: 7, 9: 7, 10: 8, 11: 7, 12: 8 },
    key_relationships: ['Rex (father)', 'Rose Mary (mother)', 'Lori, Brian, Maureen (siblings)'],
    narrative_arc: 'Growing up with brilliant but mentally ill parents who chose homelessness and refused assistance. Walls documents a childhood of starvation, no heat, collapsing houses, and parents who viewed poverty as freedom. She escaped through self-rescue.',
    why_this_character_matters: 'Jeannette\'s dome is unique because her family actively avoided systems. It reveals what happens when Layer 2 (Systems) is empty not because systems failed but because they were refused. Her dome measures the cost of anti-system ideology.',
    source_urls: [],
    scraped_at: new Date().toISOString(),
  },

  // ══════════════════════════════════════════════════════════════════════════════
  // THE IMMORTAL LIFE OF HENRIETTA LACKS by Rebecca Skloot (2010)
  // Baltimore, MD — medical exploitation, race, poverty
  // ══════════════════════════════════════════════════════════════════════════════

  {
    name: 'Henrietta Lacks',
    real_or_fictional: 'real',
    source_work: 'The Immortal Life of Henrietta Lacks',
    source_author_creator: 'Rebecca Skloot',
    source_year: 2010,
    circumstances: ['poverty', 'terminal_illness', 'uninsured'],
    location: 'Clover, VA; Baltimore, MD',
    time_period: '1920-1951',
    systems_touched: ['Johns Hopkins Hospital', 'medical research', 'tobacco farming', 'Jim Crow medical system'],
    dome_layer_richness: { 1: 8, 2: 4, 3: 6, 4: 10, 5: 6, 6: 6, 7: 4, 8: 7, 9: 5, 10: 9, 11: 4, 12: 7 },
    key_relationships: ['David (Day) Lacks (husband)', 'Deborah Lacks (daughter)', 'Children', 'George Gey (researcher)'],
    narrative_arc: 'Black woman whose cancer cells were taken without consent and became the most important cell line in medical history (HeLa cells). She died poor in a segregated hospital ward while her cells generated billions in medical advancement. Her family never knew, never consented, never profited.',
    why_this_character_matters: 'Henrietta\'s dome reveals the ultimate extraction — her body literally became an industry while her family remained in poverty. Layer 4 (Health) collides with Layer 1 (Legal) and Layer 10 (Autonomy) in unprecedented ways.',
    source_urls: [],
    scraped_at: new Date().toISOString(),
  },

  // ══════════════════════════════════════════════════════════════════════════════
  // EDUCATED by Tara Westover (2018)
  // Buck's Peak, ID — survivalist family, education as escape
  // ══════════════════════════════════════════════════════════════════════════════

  {
    name: 'Tara Westover',
    real_or_fictional: 'real',
    source_work: 'Educated',
    source_author_creator: 'Tara Westover',
    source_year: 2018,
    circumstances: ['isolation', 'domestic_violence', 'poverty', 'illiterate', 'uninsured', 'child_labor'],
    location: 'Buck\'s Peak, ID; Provo, UT; Cambridge, UK',
    time_period: '1986-2014',
    systems_touched: ['homeschooling (non)system', 'BYU', 'Cambridge University', 'hospitals (avoided)', 'birth certificates (lacked)'],
    dome_layer_richness: { 1: 5, 2: 3, 3: 5, 4: 7, 5: 6, 6: 6, 7: 10, 8: 8, 9: 6, 10: 9, 11: 6, 12: 9 },
    key_relationships: ['Gene (father)', 'Faye (mother)', 'Shawn (brother)', 'Tyler (brother)', 'Professors'],
    narrative_arc: 'Never attended school, no birth certificate until age 9, no medical care, working in her father\'s junkyard. Self-educated her way to a PhD from Cambridge. Westover documents the total absence of systems — what a dome looks like when almost every layer is empty by design.',
    why_this_character_matters: 'Tara\'s dome is defined by absence. Most layers are deliberately empty — no schooling, no healthcare, no government contact. Her dome reveals what happens when Layer 7 (Education) is the single pathway out and every other layer is hostile.',
    source_urls: [],
    scraped_at: new Date().toISOString(),
  },

  // ══════════════════════════════════════════════════════════════════════════════
  // THE NEW JIM CROW by Michelle Alexander (2010)
  // America — mass incarceration case studies
  // ══════════════════════════════════════════════════════════════════════════════

  {
    name: 'Jarvious Cotton',
    real_or_fictional: 'real',
    source_work: 'The New Jim Crow: Mass Incarceration in the Age of Colorblindness',
    source_author_creator: 'Michelle Alexander',
    source_year: 2010,
    circumstances: ['formerly_incarcerated', 'on_probation', 'poverty'],
    location: 'Mississippi',
    time_period: '2000s',
    systems_touched: ['criminal justice', 'probation', 'voting rights', 'employment (barriers)'],
    dome_layer_richness: { 1: 10, 2: 6, 3: 5, 4: 3, 5: 4, 6: 7, 7: 4, 8: 6, 9: 3, 10: 8, 11: 3, 12: 5 },
    key_relationships: ['Ancestors (each generation denied voting rights by different mechanism)'],
    narrative_arc: 'Alexander opens the book with Jarvious Cotton, who cannot vote because of a felony conviction. His father couldn\'t vote because of poll taxes. His grandfather couldn\'t vote because of literacy tests. His great-grandfather couldn\'t vote because of the KKK. His great-great-grandfather couldn\'t vote because he was a slave. Five generations, five different mechanisms, same result.',
    why_this_character_matters: 'Jarvious is a genealogical dome — his Layer 1 (Legal) extends across 5 generations, each facing a different legal mechanism achieving the same exclusion. His dome reveals how systems evolve to maintain the same outcome.',
    source_urls: [],
    scraped_at: new Date().toISOString(),
  },

  // ══════════════════════════════════════════════════════════════════════════════
  // THERE ARE NO CHILDREN HERE by Alex Kotlowitz (1991)
  // Chicago, IL — growing up in public housing projects
  // ══════════════════════════════════════════════════════════════════════════════

  {
    name: 'Pharoah Rivers',
    real_or_fictional: 'real',
    source_work: 'There Are No Children Here: The Story of Two Boys Growing Up in the Other America',
    source_author_creator: 'Alex Kotlowitz',
    source_year: 1991,
    circumstances: ['poverty', 'housing_insecure', 'trauma', 'environmental_exposure'],
    location: 'Henry Horner Homes, Chicago, IL',
    time_period: '1987-1990',
    systems_touched: ['public housing (CHA)', 'schools', 'police', 'child welfare', 'community organizations'],
    dome_layer_richness: { 1: 5, 2: 6, 3: 6, 4: 6, 5: 9, 6: 4, 7: 7, 8: 9, 9: 8, 10: 7, 11: 5, 12: 6 },
    key_relationships: ['Lafayette (brother)', 'LaJoe (mother)', 'Friends in the projects'],
    narrative_arc: 'Ten-year-old growing up in one of Chicago\'s most dangerous housing projects. Kotlowitz documents his school life, his friendships, the violence around him, and his attempts to maintain childhood in a place designed to deny it. The environmental detail is extraordinary — the physical decay of public housing.',
    why_this_character_matters: 'Pharoah\'s dome fills Layer 9 (Environment) with granular physical description of public housing failure — broken elevators, leaking pipes, rat infestations, open-air drug markets. His dome is a building inspection report of American public housing.',
    source_urls: [],
    scraped_at: new Date().toISOString(),
  },

  {
    name: 'Lafayette Rivers',
    real_or_fictional: 'real',
    source_work: 'There Are No Children Here: The Story of Two Boys Growing Up in the Other America',
    source_author_creator: 'Alex Kotlowitz',
    source_year: 1991,
    circumstances: ['poverty', 'housing_insecure', 'trauma', 'environmental_exposure'],
    location: 'Henry Horner Homes, Chicago, IL',
    time_period: '1987-1990',
    systems_touched: ['public housing (CHA)', 'schools', 'police', 'juvenile justice', 'community organizations'],
    dome_layer_richness: { 1: 6, 2: 6, 3: 6, 4: 5, 5: 9, 6: 4, 7: 6, 8: 9, 9: 8, 10: 6, 11: 4, 12: 5 },
    key_relationships: ['Pharoah (brother)', 'LaJoe (mother)', 'Gang-involved friends'],
    narrative_arc: 'Pharoah\'s older brother, pulled toward the street economy that Pharoah tries to avoid. Kotlowitz documents the impossible choice facing boys in public housing — stay inside and be safe but trapped, or go outside and face violence that also offers belonging and income.',
    why_this_character_matters: 'Lafayette and Pharoah are the same dome in two versions — same address, same systems, different trajectories. Comparing their domes reveals which layer differences cause divergent outcomes from identical starting conditions.',
    source_urls: [],
    scraped_at: new Date().toISOString(),
  },

  // ══════════════════════════════════════════════════════════════════════════════
  // DREAMLAND by Sam Quinones (2015)
  // Portsmouth, OH and nationwide — opioid crisis
  // ══════════════════════════════════════════════════════════════════════════════

  {
    name: 'The Portsmouth Addicts',
    real_or_fictional: 'real',
    source_work: 'Dreamland: The True Tale of America\'s Opiate Epidemic',
    source_author_creator: 'Sam Quinones',
    source_year: 2015,
    circumstances: ['addiction', 'poverty', 'unemployed', 'housing_insecure', 'chronic_illness'],
    location: 'Portsmouth, OH',
    time_period: '1990s-2010s',
    systems_touched: ['pill mills', 'pain clinics', 'Medicaid', 'emergency rooms', 'rehab', 'criminal justice', 'pharmacy'],
    dome_layer_richness: { 1: 6, 2: 6, 3: 7, 4: 10, 5: 6, 6: 8, 7: 4, 8: 8, 9: 6, 10: 7, 11: 3, 12: 5 },
    key_relationships: ['Dealers', 'Doctors', 'Fellow addicts', 'Families'],
    narrative_arc: 'Quinones documents how OxyContin destroyed a town — from the pill mills that prescribed it, to the Medicaid system that paid for it, to the Mexican heroin networks that replaced it when pills got expensive. Portsmouth went from manufacturing town to addiction capital in one generation.',
    why_this_character_matters: 'This dome maps the pharmaceutical-to-street pipeline. Layer 4 (Health) contains the entire arc — legitimate medicine becoming addiction becoming black market. The system that was supposed to heal became the system that destroyed.',
    source_urls: [],
    scraped_at: new Date().toISOString(),
  },

  // ══════════════════════════════════════════════════════════════════════════════
  // GANG LEADER FOR A DAY by Sudhir Venkatesh (2008)
  // Robert Taylor Homes, Chicago, IL — economics of a crack gang
  // ══════════════════════════════════════════════════════════════════════════════

  {
    name: 'J.T.',
    real_or_fictional: 'real',
    source_work: 'Gang Leader for a Day',
    source_author_creator: 'Sudhir Venkatesh',
    source_year: 2008,
    circumstances: ['poverty', 'housing_insecure'],
    location: 'Robert Taylor Homes, Chicago, IL',
    time_period: '1989-1996',
    systems_touched: ['public housing (CHA)', 'drug economy', 'police', 'gang hierarchy', 'community governance'],
    dome_layer_richness: { 1: 7, 2: 5, 3: 9, 4: 4, 5: 8, 6: 9, 7: 5, 8: 10, 9: 7, 10: 7, 11: 3, 12: 5 },
    key_relationships: ['Ms. Bailey (building president)', 'Gang members', 'Sudhir Venkatesh (researcher)', 'Tenants'],
    narrative_arc: 'College-educated gang leader running a crack franchise in Robert Taylor Homes. Venkatesh embeds with him for years, documenting the economics — who earns what, where the money goes, how the gang provides governance (settling disputes, maintaining infrastructure) when the city won\'t.',
    why_this_character_matters: 'J.T.\'s dome reveals the shadow government of public housing. Where Layer 2 (Systems) fails, Layer 8 (Community) creates its own institutions. His fiscal data (Layer 3) shows the exact economics of the drug trade at street level.',
    source_urls: [],
    scraped_at: new Date().toISOString(),
  },

  // ══════════════════════════════════════════════════════════════════════════════
  // THEY CALLED US ENEMY by George Takei (2019)
  // Japanese internment camps — childhood imprisonment
  // ══════════════════════════════════════════════════════════════════════════════

  {
    name: 'George Takei (as child)',
    real_or_fictional: 'real',
    source_work: 'They Called Us Enemy',
    source_author_creator: 'George Takei, Justin Eisinger, Steven Scott',
    source_year: 2019,
    circumstances: ['detained', 'displaced', 'housing_insecure', 'surveillance'],
    location: 'Los Angeles, CA; Rohwer, AR; Tule Lake, CA',
    time_period: '1942-1946',
    systems_touched: ['War Relocation Authority', 'internment camps', 'military', 'schools (in camp)', 'loyalty questionnaires'],
    dome_layer_richness: { 1: 9, 2: 7, 3: 6, 4: 5, 5: 8, 6: 7, 7: 6, 8: 8, 9: 7, 10: 9, 11: 5, 12: 7 },
    key_relationships: ['Parents', 'Siblings', 'Camp community'],
    narrative_arc: 'Five years old when his family was forced into internment. Takei documents the logistics of mass detention — the property seizures, the identification numbers, the barracks, the barbed wire, the loyalty tests. A child\'s experience of state power exercised against an entire ethnic group.',
    why_this_character_matters: 'George\'s dome is state-sponsored displacement documented from a child\'s perspective. Every layer was simultaneously disrupted by a single government order. His dome reveals the total cost of mass detention — and the systems required to execute it.',
    source_urls: [],
    scraped_at: new Date().toISOString(),
  },

  // ══════════════════════════════════════════════════════════════════════════════
  // MEN WE REAPED by Jesmyn Ward (2013)
  // DeLisle, MS — five deaths in four years
  // ══════════════════════════════════════════════════════════════════════════════

  {
    name: 'Jesmyn Ward',
    real_or_fictional: 'real',
    source_work: 'Men We Reaped',
    source_author_creator: 'Jesmyn Ward',
    source_year: 2013,
    circumstances: ['poverty', 'grief', 'bereavement', 'trauma'],
    location: 'DeLisle, MS',
    time_period: '2000-2004',
    systems_touched: ['schools', 'Stanford University', 'hospitals', 'police', 'drug economy', 'community'],
    dome_layer_richness: { 1: 4, 2: 4, 3: 6, 4: 7, 5: 6, 6: 7, 7: 8, 8: 9, 9: 7, 10: 6, 11: 8, 12: 8 },
    key_relationships: ['Roger Eric Daniels', 'Demond Cook', 'C.J.', 'Ronald Wayne Lizana', 'Joshua Adam Celious'],
    narrative_arc: 'Five young Black men she loved died in four years — overdose, suicide, accident, murder. Ward documents each death and weaves it with her own story of growing up in DeLisle. The memoir is a systematic autopsy of a place where young Black men die routinely and nobody counts.',
    why_this_character_matters: 'Jesmyn\'s dome maps grief as a structural condition. Five deaths in four years is not bad luck — it\'s environmental. Her dome would reveal the mortality architecture of rural Black Mississippi.',
    source_urls: [],
    scraped_at: new Date().toISOString(),
  },

  // ══════════════════════════════════════════════════════════════════════════════
  // BRAIN ON FIRE by Susannah Cahalan (2012)
  // New York City — medical mystery, insurance, diagnosis
  // ══════════════════════════════════════════════════════════════════════════════

  {
    name: 'Susannah Cahalan',
    real_or_fictional: 'real',
    source_work: 'Brain on Fire: My Month of Madness',
    source_author_creator: 'Susannah Cahalan',
    source_year: 2012,
    circumstances: ['chronic_illness', 'mental_illness', 'trauma'],
    location: 'New York City, NY',
    time_period: '2009',
    systems_touched: ['hospitals', 'neurologists', 'psychiatrists', 'insurance', 'emergency rooms', 'NYU Epilepsy Center'],
    dome_layer_richness: { 1: 3, 2: 4, 3: 7, 4: 10, 5: 4, 6: 6, 7: 4, 8: 6, 9: 3, 10: 8, 11: 4, 12: 6 },
    key_relationships: ['Parents', 'Dr. Souhel Najjar', 'Stephen (boyfriend)', 'Colleagues at NY Post'],
    narrative_arc: 'Journalist who developed anti-NMDA receptor encephalitis — a rare autoimmune brain disease that mimics psychosis. Cahalan documents every misdiagnosis, every emergency room visit, the insurance battles, and how close she came to being institutionalized forever because no one could identify her disease.',
    why_this_character_matters: 'Susannah\'s dome is a diagnostic odyssey. Layer 4 (Health) is filled with extraordinary detail — the exact cost and sequence of misdiagnosis. Her dome reveals how the medical system handles mystery, and how close she came to falling through into the psychiatric system permanently.',
    source_urls: [],
    scraped_at: new Date().toISOString(),
  },

  // ══════════════════════════════════════════════════════════════════════════════
  // BECOMING by Michelle Obama (2018)
  // South Side Chicago to White House — systems navigation at every scale
  // ══════════════════════════════════════════════════════════════════════════════

  {
    name: 'Michelle Robinson Obama',
    real_or_fictional: 'real',
    source_work: 'Becoming',
    source_author_creator: 'Michelle Obama',
    source_year: 2018,
    circumstances: ['poverty', 'immigrant'],
    location: 'South Side Chicago, IL; Princeton, NJ; Cambridge, MA; Washington, DC',
    time_period: '1964-2017',
    systems_touched: ['public schools', 'Princeton University', 'Harvard Law', 'hospitals', 'law firms', 'nonprofits', 'White House'],
    dome_layer_richness: { 1: 4, 2: 5, 3: 7, 4: 5, 5: 7, 6: 9, 7: 10, 8: 9, 9: 5, 10: 8, 11: 7, 12: 9 },
    key_relationships: ['Fraser Robinson (father, disabled)', 'Marian Robinson (mother)', 'Craig Robinson (brother)', 'Barack Obama'],
    narrative_arc: 'From a South Side apartment above her great-aunt\'s house to Princeton to the White House. Obama documents the specific mechanisms of upward mobility — the busing program, the guidance counselor who doubted her, the law firm pipeline, the neighborhood that raised her. Also documents her father\'s MS and disability with precision.',
    why_this_character_matters: 'Michelle\'s dome is an upward mobility map with maximum documentation. Comparing it to static-poverty domes reveals which Layer 8 (Community) and Layer 7 (Education) features enable trajectory change. Her father\'s disability story fills Layer 4.',
    source_urls: [],
    scraped_at: new Date().toISOString(),
  },

  // ══════════════════════════════════════════════════════════════════════════════
  // THE HOUSE ON MANGO STREET by Sandra Cisneros (1984)
  // — Often taught as fiction but rooted in autobiographical experience
  // ══════════════════════════════════════════════════════════════════════════════

  {
    name: 'Sandra Cisneros (as Esperanza)',
    real_or_fictional: 'real',
    source_work: 'A House of My Own: Stories from My Life',
    source_author_creator: 'Sandra Cisneros',
    source_year: 2015,
    circumstances: ['poverty', 'immigrant', 'housing_insecure'],
    location: 'Chicago, IL (Humboldt Park, Pilsen)',
    time_period: '1960s-1970s',
    systems_touched: ['public schools', 'public housing', 'universities', 'NEA/arts grants', 'libraries'],
    dome_layer_richness: { 1: 4, 2: 4, 3: 6, 4: 3, 5: 8, 6: 5, 7: 7, 8: 9, 9: 6, 10: 7, 11: 10, 12: 8 },
    key_relationships: ['Parents', 'Six siblings', 'Neighborhood'],
    narrative_arc: 'Mexican-American girl growing up in a series of cramped Chicago apartments, dreaming of a house of her own. Cisneros documents the neighborhood with poetic precision — who lives where, how spaces shape identity, how housing shame drives ambition.',
    why_this_character_matters: 'Sandra fills Layer 11 (Creativity) and Layer 5 (Housing) with equal depth. Her dome reveals how housing conditions create creative expression — the house you don\'t have becomes the house you write.',
    source_urls: [],
    scraped_at: new Date().toISOString(),
  },

  // ══════════════════════════════════════════════════════════════════════════════
  // IN THE SHADOW OF THE AMERICAN DREAM by David Wojnarowicz (1999)
  // NYC — queer homelessness, AIDS, art
  // ══════════════════════════════════════════════════════════════════════════════

  {
    name: 'David Wojnarowicz',
    real_or_fictional: 'real',
    source_work: 'In the Shadow of the American Dream: The Diaries of David Wojnarowicz',
    source_author_creator: 'David Wojnarowicz',
    source_year: 1999,
    circumstances: ['homeless', 'terminal_illness', 'poverty', 'child_labor', 'domestic_violence', 'trauma', 'addiction'],
    location: 'New York City, NY',
    time_period: '1970s-1992',
    systems_touched: ['shelters', 'hospitals', 'hustling economy', 'art world', 'ACT UP', 'Medicaid'],
    dome_layer_richness: { 1: 6, 2: 4, 3: 6, 4: 9, 5: 8, 6: 6, 7: 4, 8: 7, 9: 6, 10: 9, 11: 10, 12: 9 },
    key_relationships: ['Peter Hujar (mentor/partner)', 'ACT UP community', 'East Village art community'],
    narrative_arc: 'From child abuse and teenage hustling on the piers to becoming one of the most important artists of the AIDS crisis. His diaries document every form of precarity — homelessness, sex work, addiction, and then AIDS, while making art that became the visual language of an epidemic.',
    why_this_character_matters: 'David fills Layers 10-12 (Autonomy, Creativity, Flourishing) with intensity that most documented lives lack. His dome reveals how crisis produces art, and how the systems that failed him (Layer 2) were replaced by the community he built (Layer 8).',
    source_urls: [],
    scraped_at: new Date().toISOString(),
  },
]
