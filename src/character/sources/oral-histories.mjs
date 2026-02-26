/**
 * CHARACTER FRAGMENT — Oral Histories, Memoirs, First-Person Accounts
 *
 * People who told their own stories in enough detail to build domes:
 * - StoryCorps archive
 * - Studs Terkel interviews
 * - WPA Federal Writers' Project narratives (1930s)
 * - Ellis Island oral histories
 * - Published memoirs focused on navigating systems
 * - Slave narratives (WPA collection)
 * - Holocaust testimonies (Shoah Foundation)
 * - Refugee oral histories
 */

export default [

  // ══════════════════════════════════════════════════════════════════════════════
  // WPA SLAVE NARRATIVES (1936-1938)
  // Over 2,300 first-person accounts of formerly enslaved people
  // ══════════════════════════════════════════════════════════════════════════════

  {
    name: 'Fountain Hughes',
    real_or_fictional: 'real',
    source_work: 'WPA Slave Narrative Collection / Library of Congress Audio',
    source_author_creator: 'WPA Federal Writers\' Project',
    source_year: 1949,
    circumstances: ['enslaved', 'poverty', 'elderly'],
    location: 'Charlottesville, VA; Baltimore, MD',
    time_period: '1848-1949',
    systems_touched: ['slavery', 'emancipation', 'sharecropping', 'Jim Crow', 'wage labor'],
    dome_layer_richness: { 1: 9, 2: 3, 3: 7, 4: 5, 5: 7, 6: 8, 7: 4, 8: 8, 9: 6, 10: 10, 11: 5, 12: 7 },
    key_relationships: ['Former enslaver\'s family', 'Community in Baltimore'],
    narrative_arc: 'One of the few WPA interviews recorded on audio. Born enslaved, he describes the transition from slavery to freedom in his own voice at age 101 — what it meant to own nothing, to be owned, and then to be "free" with nothing. His account spans the entire arc from bondage through Reconstruction through Jim Crow.',
    why_this_character_matters: 'Fountain is the only person in this catalog who experienced slavery firsthand and whose voice was recorded. His dome spans the most extreme Layer 10 (Autonomy) transition possible — from owned property to free person. Building his dome reveals what "freedom" meant without any other layer being filled.',
    source_urls: ['https://www.loc.gov/collections/slave-narratives-from-the-federal-writers-project-1936-to-1938/'],
    scraped_at: new Date().toISOString(),
  },

  {
    name: 'Harriet Jacobs',
    real_or_fictional: 'real',
    source_work: 'Incidents in the Life of a Slave Girl',
    source_author_creator: 'Harriet Jacobs (as Linda Brent)',
    source_year: 1861,
    circumstances: ['enslaved', 'domestic_violence', 'trafficking', 'housing_insecure', 'refugee'],
    location: 'Edenton, NC; Philadelphia, PA; New York City, NY',
    time_period: '1813-1897',
    systems_touched: ['slavery', 'Fugitive Slave Act', 'abolitionist networks', 'domestic service'],
    dome_layer_richness: { 1: 10, 2: 4, 3: 5, 4: 6, 5: 9, 6: 6, 7: 5, 8: 8, 9: 7, 10: 10, 11: 7, 12: 8 },
    key_relationships: ['Dr. Norcom (enslaver)', 'Children', 'Grandmother', 'Abolitionist allies'],
    narrative_arc: 'Hid in a crawl space above her grandmother\'s house for 7 years to escape her enslaver. The crawl space was 3 feet high, unheated, and without light. She endured it to stay near her children. Eventually escaped North. Her narrative is the most detailed first-person account of enslaved women\'s experience.',
    why_this_character_matters: 'Harriet\'s dome maps the architecture of escape from slavery. Layer 5 (Housing) includes 7 years in a 3-foot crawl space — the most extreme housing documentation in this catalog. Layer 10 (Autonomy) maps the precise mechanics of unfreedom.',
    source_urls: ['https://docsouth.unc.edu/fpn/jacobs/jacobs.html'],
    scraped_at: new Date().toISOString(),
  },

  // ══════════════════════════════════════════════════════════════════════════════
  // STUDS TERKEL — Working (1974)
  // Interviews with American workers across every occupation
  // ══════════════════════════════════════════════════════════════════════════════

  {
    name: 'Mike LeFevre (Steelworker)',
    real_or_fictional: 'real',
    source_work: 'Working: People Talk About What They Do All Day and How They Feel About What They Do',
    source_author_creator: 'Studs Terkel',
    source_year: 1974,
    circumstances: ['working_poor', 'chronic_illness', 'environmental_exposure'],
    location: 'Chicago, IL',
    time_period: '1970s',
    systems_touched: ['steel mills', 'unions', 'workers comp', 'bars (social infrastructure)'],
    dome_layer_richness: { 1: 3, 2: 3, 3: 7, 4: 6, 5: 5, 6: 10, 7: 4, 8: 6, 9: 7, 10: 7, 11: 5, 12: 7 },
    key_relationships: ['Wife', 'Co-workers', 'Union'],
    narrative_arc: 'Steelworker who describes the physical reality of manual labor — the heat, the danger, the monotony, the pride, and the despair. Terkel captures his rage at being invisible: "Who built the pyramids? It wasn\'t the pharaohs." He wants his work to matter but knows it won\'t survive him.',
    why_this_character_matters: 'Mike fills Layer 6 (Economic) and Layer 12 (Flourishing) simultaneously. His dome reveals the existential dimension of work — not just what it pays but what it means and what it costs the body.',
    source_urls: [],
    scraped_at: new Date().toISOString(),
  },

  {
    name: 'Dolores Dante (Waitress)',
    real_or_fictional: 'real',
    source_work: 'Working: People Talk About What They Do All Day and How They Feel About What They Do',
    source_author_creator: 'Studs Terkel',
    source_year: 1974,
    circumstances: ['working_poor', 'single_parent'],
    location: 'Chicago, IL',
    time_period: '1970s',
    systems_touched: ['restaurant industry', 'tips economy', 'schools'],
    dome_layer_richness: { 1: 2, 2: 3, 3: 7, 4: 5, 5: 5, 6: 9, 7: 4, 8: 6, 9: 4, 10: 7, 11: 6, 12: 7 },
    key_relationships: ['Customers', 'Other waitresses', 'Children'],
    narrative_arc: 'Waitress who describes her work as performance art — reading tables, managing emotions, providing invisible care. Terkel captures her insistence that waitressing is skilled labor: "I have to be an actress, a diplomat, a psychologist." She raises children on tips.',
    why_this_character_matters: 'Dolores fills Layer 11 (Creativity) from inside a job the economy classifies as unskilled. Her dome reveals the hidden expertise in service work — and the fiscal architecture of an economy that pays below minimum wage plus tips.',
    source_urls: [],
    scraped_at: new Date().toISOString(),
  },

  {
    name: 'Babe Secoli (Supermarket Checker)',
    real_or_fictional: 'real',
    source_work: 'Working: People Talk About What They Do All Day and How They Feel About What They Do',
    source_author_creator: 'Studs Terkel',
    source_year: 1974,
    circumstances: ['working_poor', 'chronic_illness'],
    location: 'Chicago, IL',
    time_period: '1970s',
    systems_touched: ['supermarket chain', 'union', 'Social Security'],
    dome_layer_richness: { 1: 2, 2: 3, 3: 6, 4: 5, 5: 4, 6: 9, 7: 3, 8: 6, 9: 4, 10: 5, 11: 4, 12: 6 },
    key_relationships: ['Co-workers', 'Regular customers', 'Union steward'],
    narrative_arc: 'Supermarket checker for 30 years who loves her job — knows every product by touch, reads customers\' moods from their groceries. Terkel captures work as knowledge and routine as meaning. Her body deteriorates (standing all day, repetitive motion) but she can\'t imagine stopping.',
    why_this_character_matters: 'Babe\'s dome fills Layer 6 (Economic) with the micro-economics of retail — what the body costs to stand 8 hours, what knowledge is embedded in routine, what happens when the union is the only buffer between the worker and the company.',
    source_urls: [],
    scraped_at: new Date().toISOString(),
  },

  // ══════════════════════════════════════════════════════════════════════════════
  // STUDS TERKEL — Hard Times (1970)
  // Oral histories of the Great Depression
  // ══════════════════════════════════════════════════════════════════════════════

  {
    name: 'Dynamite Garland (Hobo)',
    real_or_fictional: 'real',
    source_work: 'Hard Times: An Oral History of the Great Depression',
    source_author_creator: 'Studs Terkel',
    source_year: 1970,
    circumstances: ['homeless', 'unemployed', 'poverty', 'deep_poverty'],
    location: 'Nationwide (riding freight trains)',
    time_period: '1929-1940',
    systems_touched: ['railroad police', 'jails', 'soup kitchens', 'CCC camps', 'WPA', 'Hoovervilles'],
    dome_layer_richness: { 1: 5, 2: 4, 3: 7, 4: 5, 5: 8, 6: 8, 7: 3, 8: 8, 9: 7, 10: 7, 11: 5, 12: 5 },
    key_relationships: ['Fellow hobos', 'Railroad bulls (police)', 'Relief workers'],
    narrative_arc: 'Depression-era hobo who rode freight trains across America looking for work. Terkel captures the economics of homelessness in the 1930s — the hobo jungles, the kindness of farm wives, the brutality of railroad police, and the CCC camps that eventually gave structure.',
    why_this_character_matters: 'Dynamite\'s dome maps homelessness when it was nationwide and systemic — not individual failure but economic collapse. Comparing his dome to contemporary homeless domes reveals which systems existed in the 1930s that don\'t exist now (CCC, WPA) and vice versa.',
    source_urls: [],
    scraped_at: new Date().toISOString(),
  },

  // ══════════════════════════════════════════════════════════════════════════════
  // STORYCORPS ARCHIVE
  // ══════════════════════════════════════════════════════════════════════════════

  {
    name: 'StoryCorps Military Voices',
    real_or_fictional: 'real',
    source_work: 'StoryCorps Military Voices Initiative',
    source_author_creator: 'StoryCorps',
    source_year: 2010,
    circumstances: ['veteran', 'mental_illness', 'trauma', 'disability', 'homeless'],
    location: 'Nationwide',
    time_period: '2010-present',
    systems_touched: ['military', 'VA', 'disability', 'homeless veteran services', 'therapy', 'peer support'],
    dome_layer_richness: { 1: 5, 2: 7, 3: 5, 4: 8, 5: 6, 6: 5, 7: 4, 8: 7, 9: 4, 10: 7, 11: 5, 12: 7 },
    key_relationships: ['Spouses', 'Fellow veterans', 'Therapists', 'Children'],
    narrative_arc: 'Thousands of veterans telling their stories in StoryCorps booths — combat experience, PTSD, the transition home, the VA system, relationships damaged and repaired. The archive is the largest collection of veteran first-person testimony in the world.',
    why_this_character_matters: 'The Military Voices archive fills Layer 12 (Flourishing) for veterans — not diagnoses but meaning, not symptoms but stories. These domes capture what it means to have been at war and then be expected to be normal.',
    source_urls: ['https://storycorps.org/discover/military-voices/'],
    scraped_at: new Date().toISOString(),
  },

  {
    name: 'StoryCorps 9/11 Witnesses',
    real_or_fictional: 'real',
    source_work: 'StoryCorps September 11th Initiative',
    source_author_creator: 'StoryCorps',
    source_year: 2005,
    circumstances: ['grief', 'bereavement', 'trauma'],
    location: 'New York City, NY; Pentagon, VA; Shanksville, PA',
    time_period: '2001-present',
    systems_touched: ['September 11th Victim Compensation Fund', 'mental health services', 'first responder benefits', 'Social Security survivor benefits'],
    dome_layer_richness: { 1: 5, 2: 6, 3: 7, 4: 7, 5: 4, 6: 6, 7: 4, 8: 8, 9: 5, 10: 5, 11: 5, 12: 9 },
    key_relationships: ['Lost loved ones', 'Fellow survivors', 'First responders', 'Victim advocates'],
    narrative_arc: 'First-person accounts of September 11th — not the event but the aftermath. How families navigated the Victim Compensation Fund, how first responders fought for health coverage, how grief reshaped every layer of daily life for decades.',
    why_this_character_matters: 'These domes map catastrophic loss at national scale. The VCF is a real-world dome attempt — the government trying to wrap systems around victims of a single event. Building individual domes from these testimonies reveals whether the VCF succeeded.',
    source_urls: ['https://storycorps.org/discover/september-11th/'],
    scraped_at: new Date().toISOString(),
  },

  // ══════════════════════════════════════════════════════════════════════════════
  // ELLIS ISLAND ORAL HISTORIES
  // ══════════════════════════════════════════════════════════════════════════════

  {
    name: 'Ellis Island Immigrants',
    real_or_fictional: 'real',
    source_work: 'Ellis Island Oral History Collection',
    source_author_creator: 'National Park Service / Statue of Liberty-Ellis Island Foundation',
    source_year: 1973,
    circumstances: ['immigrant', 'refugee', 'poverty', 'housing_insecure'],
    location: 'Ellis Island, NY → nationwide',
    time_period: '1892-1954',
    systems_touched: ['immigration inspection', 'quarantine', 'settlement houses', 'tenement housing', 'public schools', 'factories', 'draft boards'],
    dome_layer_richness: { 1: 8, 2: 7, 3: 6, 4: 6, 5: 7, 6: 7, 7: 6, 8: 8, 9: 6, 10: 7, 11: 6, 12: 7 },
    key_relationships: ['Family members', 'Settlement house workers', 'Employers', 'Neighbors'],
    narrative_arc: 'Over 2,000 oral histories from immigrants who passed through Ellis Island. They describe the voyage, the inspection, the fear of rejection, and the decades of settlement — tenement conditions, factory work, learning English, navigating a new legal system, building communities.',
    why_this_character_matters: 'Ellis Island domes map the immigrant dome-from-zero — every layer starts empty and fills simultaneously. These domes reveal the order in which layers fill (housing first? work first? community first?) and how long it takes.',
    source_urls: ['https://www.nps.gov/elis/learn/historyculture/oral-histories.htm'],
    scraped_at: new Date().toISOString(),
  },

  // ══════════════════════════════════════════════════════════════════════════════
  // PUBLISHED MEMOIRS — Systems Navigation
  // ══════════════════════════════════════════════════════════════════════════════

  {
    name: 'Kiese Laymon',
    real_or_fictional: 'real',
    source_work: 'Heavy: An American Memoir',
    source_author_creator: 'Kiese Laymon',
    source_year: 2018,
    circumstances: ['poverty', 'addiction', 'domestic_violence', 'trauma'],
    location: 'Jackson, MS',
    time_period: '1974-2018',
    systems_touched: ['public schools', 'Millsaps College', 'Oberlin College', 'gambling industry', 'food systems'],
    dome_layer_richness: { 1: 4, 2: 3, 3: 6, 4: 8, 5: 5, 6: 6, 7: 8, 8: 8, 9: 5, 10: 7, 11: 9, 12: 9 },
    key_relationships: ['Mother', 'Grandmother', 'Mississippi community'],
    narrative_arc: 'Memoir about the body — Black, Southern, heavy. Laymon documents how food, gambling, exercise, and language became tools for managing pain his family couldn\'t name. His mother\'s physical abuse, his sexual abuse, his obesity — all documented with a precision that fills the body-layers (Health, Autonomy, Creativity) completely.',
    why_this_character_matters: 'Kiese fills Layers 10-12 with more depth than almost any other memoirist. His dome reveals how the body carries systems — how poverty enters through food, how trauma lives in weight, how language is both wound and healing.',
    source_urls: [],
    scraped_at: new Date().toISOString(),
  },

  {
    name: 'Carmen Maria Machado',
    real_or_fictional: 'real',
    source_work: 'In the Dream House',
    source_author_creator: 'Carmen Maria Machado',
    source_year: 2019,
    circumstances: ['domestic_violence', 'trauma', 'housing_insecure'],
    location: 'Bloomington, IN; Philadelphia, PA',
    time_period: '2010s',
    systems_touched: ['universities', 'domestic violence services (inadequate for same-sex couples)', 'housing', 'therapy'],
    dome_layer_richness: { 1: 5, 2: 4, 3: 4, 4: 7, 5: 7, 6: 4, 7: 5, 8: 5, 9: 4, 10: 9, 11: 10, 12: 8 },
    key_relationships: ['Abusive partner', 'Friends', 'Therapist'],
    narrative_arc: 'Memoir of domestic violence in a same-sex relationship, told through genre conventions (choose-your-own-adventure, horror, fairy tale). Machado documents how domestic violence services are designed for heterosexual relationships — shelters, hotlines, police protocols all assume a male abuser.',
    why_this_character_matters: 'Carmen\'s dome reveals the gaps in domestic violence systems for queer people. Layer 2 (Systems) shows a system designed for one kind of victim that excludes another. Layer 11 (Creativity) shows how genre becomes a tool for processing trauma.',
    source_urls: [],
    scraped_at: new Date().toISOString(),
  },

  {
    name: 'Roxane Gay',
    real_or_fictional: 'real',
    source_work: 'Hunger: A Memoir of (My) Body',
    source_author_creator: 'Roxane Gay',
    source_year: 2017,
    circumstances: ['trauma', 'chronic_illness', 'disability'],
    location: 'Nebraska; multiple states',
    time_period: '1990s-2017',
    systems_touched: ['healthcare (bariatric)', 'universities', 'airline industry (seat sizes)', 'public spaces (accessibility)'],
    dome_layer_richness: { 1: 3, 2: 4, 3: 5, 4: 8, 5: 4, 6: 5, 7: 7, 8: 6, 9: 5, 10: 9, 11: 8, 12: 8 },
    key_relationships: ['Family', 'Partners', 'Academic community'],
    narrative_arc: 'Memoir about living in a very large body after childhood sexual assault. Gay documents how every physical space — airplane seats, restaurant booths, medical equipment, office chairs — is designed for smaller bodies. Her body is her primary circumstance and every system she encounters responds to it.',
    why_this_character_matters: 'Roxane\'s dome maps the built environment as hostile. Layer 9 (Environment) isn\'t pollution or climate — it\'s chairs, doors, MRI machines, and every physical space designed to exclude her body. Her dome reveals how infrastructure assumes a body type.',
    source_urls: [],
    scraped_at: new Date().toISOString(),
  },

  {
    name: 'Trevor Noah',
    real_or_fictional: 'real',
    source_work: 'Born a Crime: Stories from a South African Childhood',
    source_author_creator: 'Trevor Noah',
    source_year: 2016,
    circumstances: ['poverty', 'domestic_violence', 'immigrant', 'housing_insecure'],
    location: 'Soweto / Johannesburg, South Africa',
    time_period: '1984-2000s',
    systems_touched: ['apartheid legal system', 'township schools', 'informal economy', 'churches', 'hospitals', 'police'],
    dome_layer_richness: { 1: 9, 2: 6, 3: 7, 4: 5, 5: 7, 6: 7, 7: 7, 8: 9, 9: 6, 10: 8, 11: 7, 12: 8 },
    key_relationships: ['Patricia Noah (mother)', 'Abel (stepfather)', 'Grandmother'],
    narrative_arc: 'Born a crime — his existence (mixed-race child under apartheid) was illegal. Noah documents how his mother navigated apartheid\'s bureaucracy to give him access to white schools, how she survived his stepfather\'s violence, and how language (he speaks 6+) was the primary survival tool.',
    why_this_character_matters: 'Trevor\'s dome maps apartheid as a system — Layer 1 (Legal) determines everything because his body is classified as a crime. Building a dome with US systems around his South African circumstances reveals universal patterns of racial classification.',
    source_urls: [],
    scraped_at: new Date().toISOString(),
  },

  {
    name: 'Paul Kalanithi',
    real_or_fictional: 'real',
    source_work: 'When Breath Becomes Air',
    source_author_creator: 'Paul Kalanithi',
    source_year: 2016,
    circumstances: ['terminal_illness', 'grief'],
    location: 'Stanford, CA',
    time_period: '2013-2015',
    systems_touched: ['Stanford Medical Center', 'oncology', 'insurance', 'neurosurgery', 'hospice', 'disability leave'],
    dome_layer_richness: { 1: 3, 2: 4, 3: 6, 4: 10, 5: 4, 6: 7, 7: 8, 8: 6, 9: 3, 10: 8, 11: 8, 12: 10 },
    key_relationships: ['Lucy (wife)', 'Cady (daughter)', 'Colleagues', 'Patients'],
    narrative_arc: 'Neurosurgeon diagnosed with terminal lung cancer at 36. Kalanithi documents the transition from doctor to patient — from the one who delivers the diagnosis to the one who receives it. He continued operating while undergoing treatment, had a daughter knowing he wouldn\'t see her grow up, and wrote this book as he was dying.',
    why_this_character_matters: 'Paul fills Layer 12 (Flourishing) with more depth than almost any character in this catalog. His dome maps what it means to build a life knowing it will be short — every decision filtered through mortality. Layer 4 (Health) from both sides of the doctor-patient relationship.',
    source_urls: [],
    scraped_at: new Date().toISOString(),
  },
]
