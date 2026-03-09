/**
 * DUOMO COMPOSER — Person-focused product line
 * Composes "whole-person digital twins" across 12 life domains.
 * Guided wizard / exploration tool.
 *
 * Renders into container via window.renderDuomo(container)
 * All data from window.BATHS_DATA
 */

window.renderDuomo = function (container) {
  /* ───────── design tokens ───────── */
  var BG = '#0a0a0f';
  var GOLD = '#c9a84c';
  var IVORY = '#f5f0e8';
  var GOLD_DIM = 'rgba(201,168,76,0.3)';
  var GOLD_GLOW = 'rgba(201,168,76,0.08)';
  var IVORY_MUTED = 'rgba(245,240,232,0.5)';
  var IVORY_FAINT = 'rgba(245,240,232,0.25)';
  var CARD_BG = 'rgba(201,168,76,0.04)';
  var CARD_BORDER = 'rgba(201,168,76,0.12)';

  var D = window.BATHS_DATA;
  var rawProfiles = D.profiles || {};

  /* ───────── normalize profile property names ───────── */
  var profiles = {};
  Object.keys(rawProfiles).forEach(function (k) {
    var r = rawProfiles[k];
    profiles[k] = Object.assign({}, r, {
      location: (r.location && typeof r.location === 'object') ? (r.location.area || 'Philadelphia') : (r.location || 'Philadelphia'),
      systems: r.systems_involved || r.systems || [],
      costFragmented: r.annual_cost_fragmented || r.costFragmented || 0,
      costCoordinated: r.annual_cost_coordinated || r.costCoordinated || 0,
      delta: r.annual_savings || r.delta || 0,
      fiveYear: r.five_year_savings || r.fiveYear || 0,
      lifetime: r.lifetime_estimate || r.lifetime || 0
    });
  });

  /* ───────── EXTENDED DATA (from audit files) ───────── */

  // Full profile domain breakdowns (from domes-profiles/seed.py + cost_engine.py)
  var profileDomains = {
    marcus: {
      domains: [
        { domain: 'health', label: 'Health', fragmented: 45500, coordinated: 23350, savings: 22150, systems: [
          { id: 'medicaid', label: 'Medicaid', cost: 12000, savingsPct: 0.35 },
          { id: 'bha', label: 'Behavioral Health', cost: 18000, savingsPct: 0.45 },
          { id: 'mco', label: 'Managed Care Org', cost: 14000, savingsPct: 0.30 },
          { id: 'pdmp', label: 'Prescription Drug Monitoring', cost: 1500, savingsPct: 0.50 }
        ]},
        { domain: 'justice', label: 'Justice', fragmented: 20000, coordinated: 9500, savings: 10500, systems: [
          { id: 'doc', label: 'Dept of Corrections', cost: 15000, savingsPct: 0.50 },
          { id: 'probation', label: 'Probation/Parole', cost: 5000, savingsPct: 0.40 }
        ]},
        { domain: 'housing', label: 'Housing', fragmented: 20000, coordinated: 7400, savings: 12600, systems: [
          { id: 'hmis', label: 'Homeless Info System', cost: 8000, savingsPct: 0.55 },
          { id: 'shelter', label: 'Emergency Shelter', cost: 12000, savingsPct: 0.60 }
        ]},
        { domain: 'income', label: 'Income', fragmented: 9600, coordinated: 7500, savings: 2100, systems: [
          { id: 'snap', label: 'SNAP', cost: 3600, savingsPct: 0.20 },
          { id: 'unemployment', label: 'Unemployment Comp', cost: 6000, savingsPct: 0.30 }
        ]}
      ],
      fiveYear: 266000, lifetime: 1085280
    },
    sarah: {
      domains: [
        { domain: 'health', label: 'Health', fragmented: 28000, coordinated: 16800, savings: 11200, systems: [
          { id: 'medicaid', label: 'Medicaid', cost: 12000, savingsPct: 0.35 },
          { id: 'mco', label: 'Managed Care Org', cost: 14000, savingsPct: 0.30 },
          { id: 'bha', label: 'Behavioral Health', cost: 2000, savingsPct: 0.45 }
        ]},
        { domain: 'child_welfare', label: 'Child Welfare', fragmented: 18000, coordinated: 9900, savings: 8100, systems: [
          { id: 'sacwis', label: 'Child Welfare Info System', cost: 18000, savingsPct: 0.45 }
        ]},
        { domain: 'housing', label: 'Housing', fragmented: 9600, coordinated: 7200, savings: 2400, systems: [
          { id: 'pha', label: 'Public Housing Auth', cost: 9600, savingsPct: 0.25 }
        ]},
        { domain: 'justice', label: 'Justice', fragmented: 3000, coordinated: 1950, savings: 1050, systems: [
          { id: 'court_cms', label: 'Court Case Mgmt', cost: 3000, savingsPct: 0.35 }
        ]},
        { domain: 'income', label: 'Income', fragmented: 13600, coordinated: 10560, savings: 3040, systems: [
          { id: 'tanf', label: 'TANF', cost: 7200, savingsPct: 0.30 },
          { id: 'snap', label: 'SNAP', cost: 3600, savingsPct: 0.20 },
          { id: 'mco', label: 'Managed Care (benefits)', cost: 2800, savingsPct: 0.30 }
        ]}
      ],
      fiveYear: 215500, lifetime: 879240
    },
    james: {
      domains: [
        { domain: 'health', label: 'Health', fragmented: 58000, coordinated: 34800, savings: 23200, systems: [
          { id: 'va', label: 'VA Healthcare', cost: 22000, savingsPct: 0.40 },
          { id: 'medicaid', label: 'Medicaid', cost: 12000, savingsPct: 0.35 },
          { id: 'mco', label: 'Managed Care Org', cost: 14000, savingsPct: 0.30 },
          { id: 'pdmp', label: 'Prescription Drug Monitoring', cost: 1500, savingsPct: 0.50 },
          { id: 'hie', label: 'Health Info Exchange', cost: 2000, savingsPct: 0.60 }
        ]},
        { domain: 'income', label: 'Income', fragmented: 20200, coordinated: 15150, savings: 5050, systems: [
          { id: 'ssi', label: 'SSI', cost: 10200, savingsPct: 0.25 },
          { id: 'ssa', label: 'Social Security Admin', cost: 10000, savingsPct: 0.25 }
        ]}
      ],
      fiveYear: 209000, lifetime: 852360
    },
    maria: {
      domains: [
        { domain: 'child_welfare', label: 'Child Welfare', fragmented: 18000, coordinated: 9900, savings: 8100, systems: [
          { id: 'sacwis', label: 'Child Welfare Info System', cost: 18000, savingsPct: 0.45 }
        ]},
        { domain: 'health', label: 'Health', fragmented: 14000, coordinated: 9100, savings: 4900, systems: [
          { id: 'medicaid', label: 'Medicaid', cost: 12000, savingsPct: 0.35 },
          { id: 'mco', label: 'Managed Care Org', cost: 2000, savingsPct: 0.30 }
        ]},
        { domain: 'education', label: 'Education', fragmented: 12000, coordinated: 7800, savings: 4200, systems: [
          { id: 'slds', label: 'Student Data System', cost: 1500, savingsPct: 0.50 },
          { id: 'iep', label: 'IEP / Special Ed', cost: 10500, savingsPct: 0.35 }
        ]},
        { domain: 'justice', label: 'Justice', fragmented: 8000, coordinated: 4400, savings: 3600, systems: [
          { id: 'juvenile_court', label: 'Juvenile Court', cost: 8000, savingsPct: 0.45 }
        ]}
      ],
      fiveYear: 186500, lifetime: 760440
    },
    robert: {
      domains: [
        { domain: 'health', label: 'Health', fragmented: 54000, coordinated: 27000, savings: 27000, systems: [
          { id: 'medicaid', label: 'Medicaid', cost: 12000, savingsPct: 0.35 },
          { id: 'bha', label: 'Behavioral Health', cost: 18000, savingsPct: 0.45 },
          { id: 'mco', label: 'Managed Care Org', cost: 14000, savingsPct: 0.30 },
          { id: 'er_frequent', label: 'Frequent ER Use', cost: 28000, savingsPct: 0.65 }
        ]},
        { domain: 'housing', label: 'Housing', fragmented: 20000, coordinated: 7400, savings: 12600, systems: [
          { id: 'hmis', label: 'Homeless Info System', cost: 8000, savingsPct: 0.55 },
          { id: 'shelter', label: 'Emergency Shelter', cost: 12000, savingsPct: 0.60 }
        ]},
        { domain: 'income', label: 'Income', fragmented: 16200, coordinated: 12150, savings: 4050, systems: [
          { id: 'ssi', label: 'SSI', cost: 10200, savingsPct: 0.25 },
          { id: 'snap', label: 'SNAP', cost: 3600, savingsPct: 0.20 },
          { id: 'ssa', label: 'Social Security Admin', cost: 2400, savingsPct: 0.25 }
        ]}
      ],
      fiveYear: 283000, lifetime: 1153680
    }
  };

  // Provider registry (from studio/seed_scenarios.py)
  var providers = [
    { id: 'prov-kens-bh', name: 'Kensington Behavioral Health Center', services: ['mental_health', 'substance_use', 'crisis'], address: '3100 Kensington Ave', profiles: ['marcus', 'robert'] },
    { id: 'prov-temple-pc', name: 'Temple University Primary Care', services: ['primary_care', 'diabetes_management', 'chronic_pain'], address: '3401 N Broad St', profiles: ['james', 'robert'] },
    { id: 'prov-phr-housing', name: 'Project HOME Reentry Housing', services: ['housing_assistance', 'reentry_services'], address: '1515 Fairmount Ave', profiles: ['marcus', 'robert'] },
    { id: 'prov-wf-dev', name: 'Philadelphia Works Workforce Development', services: ['workforce_development', 'job_training', 'credential_programs'], address: '1617 JFK Blvd', profiles: ['marcus', 'sarah'] },
    { id: 'prov-wc-dv', name: "Women's Center of Montgomery County", services: ['domestic_violence', 'mental_health', 'legal_aid'], address: '100 S Broad St', profiles: ['sarah'] },
    { id: 'prov-va-med', name: 'Philadelphia VA Medical Center', services: ['primary_care', 'mental_health', 'chronic_pain', 'ptsd'], address: '3900 Woodland Ave', profiles: ['james'] },
    { id: 'prov-act-team', name: 'Community ACT Team — PATH Program', services: ['mental_health', 'housing_assistance', 'case_management'], address: '810 Arch St', profiles: ['robert'] },
    { id: 'prov-juv-mentor', name: 'Big Brothers Big Sisters — Philadelphia', services: ['mentorship', 'youth_development', 'education_support'], address: '230 S Broad St', profiles: ['maria'] }
  ];

  // N-of-1 trial configurations (from bio_experiment.py / seed_scenarios.py)
  var trialConfigs = {
    marcus: {
      hypothesis: 'Buprenorphine + counseling reduces cravings more than counseling alone',
      intervention: 'Buprenorphine 8mg sublingual + weekly counseling',
      control: 'Weekly counseling only',
      metric: 'daily_craving_score',
      controlData: [6.2, 5.8, 6.5, 7.0, 6.1, 5.9, 6.3, 6.8],
      interventionData: [4.1, 3.5, 3.8, 3.2, 4.0, 3.6, 3.3, 2.9]
    },
    sarah: {
      hypothesis: 'Trauma-focused CBT reduces PTSD symptoms more than standard therapy',
      intervention: 'Trauma-focused CBT (12-session protocol)',
      control: 'Standard supportive therapy',
      metric: 'PCL5_score',
      controlData: [52, 50, 53, 48, 51, 49, 50, 47],
      interventionData: [45, 38, 35, 32, 30, 28, 27, 25]
    },
    james: {
      hypothesis: 'Yoga + PT reduces chronic pain more than standard pain management',
      intervention: 'Adaptive yoga + physical therapy (3x/week)',
      control: 'Standard pain medication management',
      metric: 'pain_scale_0_10',
      controlData: [7.4, 7.1, 7.6, 7.2, 7.5, 7.0, 7.3, 7.8],
      interventionData: [6.2, 5.5, 5.1, 4.8, 5.0, 4.6, 4.3, 4.1]
    },
    maria: {
      hypothesis: 'Trauma-informed mentoring improves academic engagement',
      intervention: 'Structured mentoring + trauma-informed tutoring',
      control: 'Standard school support services',
      metric: 'weekly_attendance_pct',
      controlData: [62, 65, 58, 60, 63, 55, 61, 59],
      interventionData: [72, 78, 82, 85, 80, 88, 90, 87]
    },
    robert: {
      hypothesis: 'Housing First + ACT reduces ER visits more than standard outreach',
      intervention: 'Housing First placement + ACT team engagement',
      control: 'Standard homeless outreach + shelter access',
      metric: 'monthly_er_visits',
      controlData: [4.2, 3.8, 4.5, 5.0, 4.1, 3.9, 4.3, 4.8],
      interventionData: [2.1, 1.5, 1.8, 1.2, 1.0, 0.8, 0.6, 0.5]
    }
  };

  // Flourishing domains — 3 layers (from domes-flourishing/domains.py)
  var flourishingDomains = {
    foundation: [
      { id: 'safety', name: 'Safety & Security', desc: 'Physical safety, stable housing, legal protection, freedom from violence' },
      { id: 'economic', name: 'Economic Wellbeing', desc: 'Income, assets, financial stability, freedom from debt trap' },
      { id: 'physical_health', name: 'Physical Health', desc: 'Medical care, nutrition, environmental health, preventive care' },
      { id: 'mental_health', name: 'Mental & Emotional Health', desc: 'Psychological wellbeing, emotional regulation, trauma recovery' }
    ],
    aspiration: [
      { id: 'belonging', name: 'Belonging & Community', desc: 'Social connection, relationships, community participation' },
      { id: 'learning', name: 'Learning & Growth', desc: 'Education, skills development, intellectual curiosity' },
      { id: 'creative', name: 'Creative Expression', desc: 'Arts, culture, creativity, self-expression' },
      { id: 'civic', name: 'Civic & Political Voice', desc: 'Participation, rights, representation, advocacy' },
      { id: 'work', name: 'Meaningful Work', desc: 'Vocation, purpose, dignity in contribution' }
    ],
    transcendence: [
      { id: 'spiritual', name: 'Spiritual & Existential', desc: 'Meaning, purpose, faith, contemplative practice' },
      { id: 'ecological', name: 'Ecological Connection', desc: 'Relationship with nature, environmental stewardship' },
      { id: 'legacy', name: 'Legacy & Impact', desc: 'Contribution to future generations, lasting positive change' }
    ]
  };

  // Profile flourishing scores (simulated from domain data)
  var profileFlourishingScores = {
    marcus:  { safety: 25, economic: 30, physical_health: 35, mental_health: 20, belonging: 40, learning: 35, creative: 15, civic: 20, work: 45, spiritual: 30, ecological: 20, legacy: 15 },
    sarah:   { safety: 30, economic: 20, physical_health: 45, mental_health: 25, belonging: 35, learning: 50, creative: 40, civic: 30, work: 15, spiritual: 35, ecological: 25, legacy: 20 },
    james:   { safety: 55, economic: 25, physical_health: 30, mental_health: 40, belonging: 50, learning: 45, creative: 30, civic: 60, work: 10, spiritual: 55, ecological: 40, legacy: 50 },
    maria:   { safety: 20, economic: 15, physical_health: 50, mental_health: 30, belonging: 45, learning: 55, creative: 60, civic: 25, work: 10, spiritual: 20, ecological: 30, legacy: 15 },
    robert:  { safety: 10, economic: 10, physical_health: 15, mental_health: 10, belonging: 15, learning: 20, creative: 10, civic: 5, work: 5, spiritual: 15, ecological: 10, legacy: 5 }
  };

  // Philosophical traditions (from domes-flourishing/philosophy.py)
  var philosophicalTraditions = [
    { id: 'eudaimonia', name: 'Eudaimonia', thinker: 'Aristotle', core: 'Flourishing as the highest human good, achieved through virtue and practical wisdom',
      principles: ['Virtue ethics — character over rules', 'Practical wisdom (phronesis)', 'The good life requires community (polis)', 'Flourishing is an activity, not a state'],
      flourishingMap: 'All 12 domains as expressions of human excellence' },
    { id: 'capability_approach', name: 'Capability Approach', thinker: 'Amartya Sen & Martha Nussbaum', core: 'What people are actually able to do and be — real freedoms, not just formal rights',
      principles: ['Capabilities vs. functionings', 'Conversion factors matter', 'Agency and choice central', 'Irreducible plurality of goods'],
      flourishingMap: "Nussbaum's 10 capabilities map directly to DUOMO domains" },
    { id: 'ubuntu', name: 'Ubuntu', thinker: 'Desmond Tutu', core: '"I am because we are" — personhood through community',
      principles: ['Radical interdependence', 'Communal identity', 'Restorative over punitive justice', 'Shared humanity (umuntu)'],
      flourishingMap: 'Belonging, community, civic participation, legacy domains' },
    { id: 'interdependence', name: 'Interbeing', thinker: 'Thich Nhat Hanh', core: 'Non-separation — all things inter-are',
      principles: ['Mindfulness as foundation', 'Non-duality of self and other', 'Engaged Buddhism', 'Compassion as action'],
      flourishingMap: 'Ecological, spiritual, mental health, belonging domains' },
    { id: 'cura_personalis', name: 'Cura Personalis', thinker: 'Ignatius of Loyola (Jesuit)', core: 'Care of the whole person — body, mind, spirit',
      principles: ['Individual attention', 'Integration of all dimensions', 'Discernment', 'Service to others'],
      flourishingMap: 'Physical + mental health, spiritual, learning, work domains' },
    { id: 'relational_worldview', name: 'Relational Worldview', thinker: 'Robin Wall Kimmerer', core: 'Braided Sweetgrass — reciprocity with all living things',
      principles: ['Reciprocity over extraction', 'Gratitude as practice', 'Indigenous ecological knowledge', 'Gift economy'],
      flourishingMap: 'Ecological connection, legacy, belonging, creative expression' }
  ];

  // Nussbaum's 10 capabilities mapped to DUOMO domains
  var nussbaumCapabilities = [
    { num: 1, name: 'Life', desc: 'Being able to live to the end of a human life of normal length', domains: ['physical_health'] },
    { num: 2, name: 'Bodily Health', desc: 'Being able to have good health, including reproductive health; adequate nourishment; adequate shelter', domains: ['physical_health', 'safety', 'economic'] },
    { num: 3, name: 'Bodily Integrity', desc: 'Being able to move freely; secure against assault and violence', domains: ['safety'] },
    { num: 4, name: 'Senses, Imagination, Thought', desc: 'Being able to use senses, imagine, think, and reason in a truly human way — informed by education', domains: ['learning', 'creative'] },
    { num: 5, name: 'Emotions', desc: 'Being able to have attachments; to love, grieve, experience longing, gratitude', domains: ['mental_health', 'belonging'] },
    { num: 6, name: 'Practical Reason', desc: 'Being able to form a conception of the good and plan one\'s life', domains: ['spiritual', 'learning'] },
    { num: 7, name: 'Affiliation', desc: 'Being able to live with and toward others; having the social bases of self-respect', domains: ['belonging', 'civic', 'work'] },
    { num: 8, name: 'Other Species', desc: 'Being able to live with concern for animals, plants, nature', domains: ['ecological'] },
    { num: 9, name: 'Play', desc: 'Being able to laugh, play, enjoy recreational activities', domains: ['creative', 'belonging'] },
    { num: 10, name: 'Control Over Environment', desc: 'Being able to participate politically; hold property; seek employment on equal basis', domains: ['civic', 'economic', 'work'] }
  ];

  // AI Teammates (from domes-lab/teammates.py)
  var aiTeammates = [
    { slug: 'fiscal-alchemist', name: 'The Fiscal Alchemist', title: 'Creative Finance Director', domain: 'finance', color: '#FFD700', desc: 'Designs novel financial instruments that turn coordination savings into investable assets' },
    { slug: 'impact-investor', name: 'The Impact Investor', title: 'Social ROI Specialist', domain: 'investment', color: '#00E676', desc: 'Calculates social return on investment and structures prevention-backed securities' },
    { slug: 'data-inventor', name: 'The Data Inventor', title: 'Data Systems Architect', domain: 'data', color: '#448AFF', desc: 'Designs interoperable data architectures that bridge fragmented government systems' },
    { slug: 'tech-futurist', name: 'The Tech Futurist', title: 'Emerging Tech Strategist', domain: 'technology', color: '#7C4DFF', desc: 'Identifies and evaluates emerging technologies for civic infrastructure applications' },
    { slug: 'legislative-inventor', name: 'The Legislative Inventor', title: 'Policy Innovation Lead', domain: 'policy', color: '#FFAB00', desc: 'Drafts model legislation and regulatory frameworks for coordination innovation' },
    { slug: 'regulatory-hacker', name: 'The Regulatory Hacker', title: 'Compliance Innovation Specialist', domain: 'regulation', color: '#FF6D00', desc: 'Finds creative pathways through regulatory barriers without breaking rules' },
    { slug: 'service-designer', name: 'The Service Designer', title: 'Human-Centered Design Lead', domain: 'design', color: '#E040FB', desc: 'Redesigns service delivery from the perspective of people navigating systems' },
    { slug: 'space-architect', name: 'The Space Architect', title: 'Built Environment Strategist', domain: 'infrastructure', color: '#00BCD4', desc: 'Designs physical spaces that support human services integration' },
    { slug: 'measurement-scientist', name: 'The Measurement Scientist', title: 'Impact Metrics Lead', domain: 'evaluation', color: '#8BC34A', desc: 'Develops outcome measurement frameworks and validates intervention effectiveness' },
    { slug: 'narrative-researcher', name: 'The Narrative Researcher', title: 'Story & Data Translator', domain: 'communications', color: '#FF4081', desc: 'Translates complex system data into compelling human narratives' },
    { slug: 'market-maker', name: 'The Market Maker', title: 'Systems Market Strategist', domain: 'market', color: '#00E5FF', desc: 'Creates markets for coordination outcomes and trades fragmentation risk' },
    { slug: 'architect', name: 'The Architect', title: 'Systems Integration Lead', domain: 'systems', color: '#FF5722', desc: 'Orchestrates all teammates toward coherent whole-person coordination architectures' }
  ];

  // Provision matching algorithm constants (from backend/app/matching.py)
  var TYPE_WEIGHT = { right: 1.0, protection: 0.95, obligation: 0.90, enforcement: 0.85 };
  var DOMAIN_ORDER = { health: 0, civil_rights: 1, housing: 2, income: 3, education: 4, justice: 5 };

  // Gap detection rules (from backend/app/cross_reference.py — 15 rules)
  var gapRules = [
    { name: 'epsdt', desc: 'Medicaid EPSDT (Early & Periodic Screening)', condition: 'medicaid + age under 21', check: function(p) { return p.systems.indexOf('medicaid') >= 0 && p.age < 21; } },
    { name: 'mckinney_vento', desc: 'McKinney-Vento Homeless Education', condition: 'homeless housing', check: function(p) { return p.systems.indexOf('hmis') >= 0 || p.systems.indexOf('shelter') >= 0; } },
    { name: 'ada_accommodation', desc: 'ADA Reasonable Accommodation', condition: 'any disability', check: function(p) { return p.conditions && p.conditions.length > 0; } },
    { name: 'section_504', desc: 'Section 504 Rehabilitation Act', condition: 'any disability + federally funded', check: function(p) { return p.conditions && p.conditions.length > 0; } },
    { name: 'idea', desc: 'IDEA Special Education', condition: 'disability + age under 21', check: function(p) { return p.conditions && p.conditions.length > 0 && p.age < 21; } },
    { name: 'mh_parity', desc: 'Mental Health Parity (MHPAEA)', condition: 'mental health/SUD + insured', check: function(p) { return hasCondition(p, ['depression', 'anxiety', 'ptsd', 'schizophrenia', 'substance_use_disorder', 'trauma', 'adhd']); } },
    { name: 'snap', desc: 'SNAP Food Assistance', condition: 'below poverty or unemployed', check: function(p) { return p.income < 20000 || p.systems.indexOf('unemployment') >= 0; } },
    { name: 'ssi', desc: 'Supplemental Security Income', condition: 'disability + low income', check: function(p) { return p.conditions && p.conditions.length > 0 && p.income < 15000; } },
    { name: 'vawa_housing', desc: 'VAWA Housing Protections', condition: 'domestic violence survivor', check: function(p) { return p.id === 'sarah-chen'; } },
    { name: 'foster_care_aging_out', desc: 'Foster Care Aging Out Protections', condition: 'foster care + age under 21', check: function(p) { return p.systems.indexOf('sacwis') >= 0 && p.age < 21; } },
    { name: 'veteran_healthcare', desc: 'Veteran Healthcare Rights', condition: 'veteran', check: function(p) { return p.systems.indexOf('va') >= 0; } },
    { name: 'reentry', desc: 'Reentry / Second Chance', condition: 'recently released', check: function(p) { return p.systems.indexOf('doc') >= 0 || p.systems.indexOf('probation') >= 0; } },
    { name: 'medicaid_reentry', desc: 'Medicaid Reentry Coverage', condition: 'recently released + no medicaid', check: function(p) { return p.systems.indexOf('doc') >= 0 && p.systems.indexOf('medicaid') < 0; } },
    { name: 'fair_housing', desc: 'Fair Housing Act', condition: 'housing + disability', check: function(p) { return (p.systems.indexOf('hmis') >= 0 || p.systems.indexOf('pha') >= 0 || p.systems.indexOf('shelter') >= 0) && p.conditions && p.conditions.length > 0; } },
    { name: 'olmstead', desc: 'Olmstead Community Integration', condition: 'disability + institutional risk', check: function(p) { return p.conditions && p.conditions.length > 1 && p.severity === 'severe'; } }
  ];

  function hasCondition(p, list) {
    if (!p.conditions) return false;
    for (var i = 0; i < p.conditions.length; i++) {
      if (list.indexOf(p.conditions[i]) >= 0) return true;
    }
    return false;
  }

  // Narrative arc data (from narrative_synthesis.py)
  var DOMAIN_TENSION = { housing: 0.9, health: 0.8, financial: 0.7, legal: 0.6, employment: 0.5, digital: 0.4, social: 0.3 };

  var narrativeArcs = {
    marcus: { arcType: 'fall_and_recovery', title: 'From Kensington to Coordination', tension: 0.82, medium: 'doc',
      events: [
        { type: 'incarceration', domain: 'legal', day: 1 },
        { type: 'release_no_plan', domain: 'housing', day: 90 },
        { type: 'relapse', domain: 'health', day: 120 },
        { type: 'er_visit', domain: 'health', day: 125 },
        { type: 'shelter_entry', domain: 'housing', day: 130 },
        { type: 'mat_start', domain: 'health', day: 180 },
        { type: 'employment_gained', domain: 'employment', day: 220 },
        { type: 'housing_secured', domain: 'housing', day: 280 }
      ],
      turningPoints: ['mat_start', 'housing_secured'] },
    sarah: { arcType: 'rising_tension', title: 'Navigating the Maze with Children', tension: 0.71, medium: 'series',
      events: [
        { type: 'dv_incident', domain: 'legal', day: 1 },
        { type: 'shelter_entry', domain: 'housing', day: 3 },
        { type: 'benefits_enrollment', domain: 'financial', day: 15 },
        { type: 'custody_hearing', domain: 'legal', day: 45 },
        { type: 'cbt_start', domain: 'health', day: 60 },
        { type: 'housing_waitlist', domain: 'housing', day: 90 }
      ],
      turningPoints: ['cbt_start'] },
    james: { arcType: 'slow_burn', title: 'The Veteran\u2019s Quiet Struggle', tension: 0.55, medium: 'short',
      events: [
        { type: 'chronic_pain_onset', domain: 'health', day: 1 },
        { type: 'va_enrollment', domain: 'health', day: 30 },
        { type: 'medication_management', domain: 'health', day: 60 },
        { type: 'disability_application', domain: 'financial', day: 120 },
        { type: 'mobility_decline', domain: 'health', day: 200 },
        { type: 'home_modification', domain: 'housing', day: 250 },
        { type: 'community_connection', domain: 'social', day: 300 },
        { type: 'care_coordination', domain: 'health', day: 350 }
      ],
      turningPoints: ['care_coordination'] },
    maria: { arcType: 'breakthrough', title: 'A Teenager Finds Her Voice', tension: 0.64, medium: 'short',
      events: [
        { type: 'placement_change', domain: 'housing', day: 1 },
        { type: 'school_transfer', domain: 'employment', day: 5 },
        { type: 'truancy', domain: 'employment', day: 30 },
        { type: 'mentoring_start', domain: 'social', day: 60 },
        { type: 'academic_improvement', domain: 'employment', day: 120 },
        { type: 'art_program', domain: 'social', day: 150 }
      ],
      turningPoints: ['mentoring_start', 'academic_improvement'] },
    robert: { arcType: 'cascade', title: 'The $94,800 Question', tension: 0.95, medium: 'doc',
      events: [
        { type: 'psychotic_episode', domain: 'health', day: 1 },
        { type: 'er_visit', domain: 'health', day: 1 },
        { type: 'shelter_denied', domain: 'housing', day: 2 },
        { type: 'medication_lapse', domain: 'health', day: 5 },
        { type: 'er_visit', domain: 'health', day: 15 },
        { type: 'benefit_cutoff', domain: 'financial', day: 30 },
        { type: 'er_visit', domain: 'health', day: 45 },
        { type: 'hospitalization', domain: 'health', day: 50 },
        { type: 'act_engagement', domain: 'health', day: 90 },
        { type: 'housing_first', domain: 'housing', day: 120 }
      ],
      turningPoints: ['act_engagement', 'housing_first'] }
  };

  // Pipeline stages (from pipeline.py)
  var pipelineStages = [
    { key: 'development', label: 'DEVELOPMENT', num: '01', desc: 'Person intake, rights acquisition, legal landscape mapping', deliverables: ['Rights package', 'Market analysis', 'Cast list (systems)', 'Deal structure'], gate: 'greenlight' },
    { key: 'pre_production', label: 'PRE-PRODUCTION', num: '02', desc: 'Coordination architecture design, budget modeling, team assembly', deliverables: ['Coordination crew', 'Shooting script (dome blueprint)', 'Budget top sheet', 'Production framework'], gate: 'pre_production' },
    { key: 'production', label: 'PRODUCTION', num: '03', desc: 'Execute 12 DUOMO domains, query all services, build digital twin', deliverables: ['12 domain scores', 'Cosm dimensions', 'Provider matches', 'Gap resolution'], gate: 'production' },
    { key: 'post', label: 'POST-PRODUCTION', num: '04', desc: 'Verify dome completeness, generate innovations, create IP assets', deliverables: ['Dome completeness report', 'Innovation portfolio', 'IP asset register', 'Learning package'], gate: 'picture_lock' },
    { key: 'distribution', label: 'DISTRIBUTION', num: '05', desc: 'Calculate final COSM score, price Dome Bond, distribute replication kit', deliverables: ['Final COSM score', 'Dome Bond pricing', 'Industries changed', 'Replication kit'], gate: 'ship' }
  ];

  /* ───────── utilities ───────── */
  function $(sel, ctx) { return (ctx || document).querySelector(sel); }
  function $$(sel, ctx) { return (ctx || document).querySelectorAll(sel); }
  function el(tag, cls, html) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (html !== undefined) e.innerHTML = html;
    return e;
  }
  function fmt(n) { return n >= 1000000 ? '$' + (n / 1000000).toFixed(1) + 'M' : n >= 1000 ? '$' + (n / 1000).toFixed(0) + 'K' : '$' + n; }
  function fmtFull(n) { return '$' + n.toLocaleString(); }
  function pct(n) { return Math.round(n * 100) + '%'; }

  /* ───────── matching algorithm (ported from Python) ───────── */
  function matchProvisions(profileKey) {
    var p = profiles[profileKey];
    var provs = (D.provisions && D.provisions.records) || [];
    var results = [];
    for (var i = 0; i < provs.length; i++) {
      var prov = provs[i];
      var matchedKeys = 0;
      var totalKeys = 0;
      var reasons = [];
      // Simple matching based on domain overlap with profile systems
      var domainMap = { healthcare: 'health', housing: 'housing', income: 'income', food: 'income', education: 'education', legal: 'justice' };
      var provDomain = domainMap[prov.domain] || prov.domain;
      // Check if profile has systems in this domain
      var relevantSystems = (profileDomains[profileKey] && profileDomains[profileKey].domains) || [];
      for (var j = 0; j < relevantSystems.length; j++) {
        if (relevantSystems[j].domain === provDomain || relevantSystems[j].label.toLowerCase().indexOf(provDomain) >= 0) {
          matchedKeys++;
          reasons.push('Domain match: ' + relevantSystems[j].label);
        }
        totalKeys++;
      }
      if (totalKeys === 0) { totalKeys = 1; }
      var ratio = matchedKeys / totalKeys;
      var baseScore = ratio >= 1.0 ? 1.0 : ratio >= 0.75 ? 0.8 : ratio >= 0.5 ? 0.6 : ratio > 0 ? 0.5 : 0.4;
      var typeWeight = TYPE_WEIGHT['protection'] || 0.95;
      var relevance = Math.min(baseScore * typeWeight, 1.0);
      relevance = Math.round(relevance * 100) / 100;
      if (relevance > 0.3) {
        results.push({ citation: prov.citation, title: prov.title, domain: prov.domain, relevance: relevance, reasons: reasons, isGap: false });
      }
    }
    results.sort(function (a, b) {
      if (b.relevance !== a.relevance) return b.relevance - a.relevance;
      var da = DOMAIN_ORDER[a.domain] || 5;
      var db = DOMAIN_ORDER[b.domain] || 5;
      return da - db;
    });
    return results;
  }

  function detectGaps(profileKey) {
    var p = profiles[profileKey];
    var results = [];
    for (var i = 0; i < gapRules.length; i++) {
      var rule = gapRules[i];
      if (rule.check(p)) {
        results.push({ rule: rule.name, desc: rule.desc, condition: rule.condition, relevance: 0.9 });
      }
    }
    return results;
  }

  /* ───────── N-of-1 trial analysis (ported from Python) ───────── */
  function analyzeTrial(config) {
    var c = config.controlData;
    var t = config.interventionData;
    var cMean = c.reduce(function(a, b) { return a + b; }, 0) / c.length;
    var tMean = t.reduce(function(a, b) { return a + b; }, 0) / t.length;
    var cVar = c.reduce(function(a, b) { return a + (b - cMean) * (b - cMean); }, 0) / (c.length - 1);
    var tVar = t.reduce(function(a, b) { return a + (b - tMean) * (b - tMean); }, 0) / (t.length - 1);
    var pooledSD = Math.sqrt((cVar + tVar) / 2);
    var effectSize = pooledSD > 0 ? (cMean - tMean) / pooledSD : 0;
    // Welch's t-test approximation
    var se = Math.sqrt(cVar / c.length + tVar / t.length);
    var tStat = se > 0 ? (cMean - tMean) / se : 0;
    // Approximate p-value using normal distribution (good enough for display)
    var z = Math.abs(tStat);
    var pValue = z > 3.5 ? 0.001 : z > 2.58 ? 0.01 : z > 1.96 ? 0.05 : z > 1.645 ? 0.10 : 0.20;
    // Bayesian probability P(intervention better)
    var d = effectSize;
    var nFactor = Math.sqrt(1 / c.length + 1 / t.length);
    var bayesZ = nFactor > 0 ? d / nFactor : 0;
    var bayesProb = 0.5 * (1 + erf(bayesZ / Math.sqrt(2)));
    // Recommendation
    var rec;
    if (pValue < 0.05 && bayesProb > 0.95 && Math.abs(effectSize) >= 0.5) rec = 'Strong evidence — consider adopting intervention';
    else if (pValue < 0.05 && Math.abs(effectSize) >= 0.2) rec = 'Statistically significant — more cycles recommended';
    else if (bayesProb > 0.80 && Math.abs(effectSize) >= 0.2) rec = 'Suggestive — continue monitoring';
    else if (Math.abs(effectSize) < 0.2) rec = 'No meaningful difference detected';
    else rec = 'Inconclusive — continue data collection';

    return {
      controlMean: Math.round(cMean * 100) / 100,
      interventionMean: Math.round(tMean * 100) / 100,
      effectSize: Math.round(effectSize * 100) / 100,
      pValue: pValue,
      bayesianProb: Math.round(bayesProb * 1000) / 1000,
      recommendation: rec
    };
  }

  function erf(x) {
    var a1 = 0.254829592, a2 = -0.284496736, a3 = 1.421413741, a4 = -1.453152027, a5 = 1.061405429, p = 0.3275911;
    var sign = x < 0 ? -1 : 1;
    x = Math.abs(x);
    var t = 1.0 / (1.0 + p * x);
    var y = 1.0 - (((((a5 * t + a4) * t) + a3) * t + a2) * t + a1) * t * Math.exp(-x * x);
    return sign * y;
  }

  /* ───────── Narrative tension scoring (ported from Python) ───────── */
  function scoreTension(arc) {
    var events = arc.events || [];
    var eventDensity = Math.min(events.length / 10.0, 1.0);
    var escalationCount = 0;
    var escalationTypes = ['er_visit', 'hospitalization', 'benefit_cutoff', 'shelter_denied', 'medication_lapse', 'relapse', 'psychotic_episode'];
    for (var i = 0; i < events.length; i++) {
      if (escalationTypes.indexOf(events[i].type) >= 0) escalationCount++;
    }
    var turningPoints = arc.turningPoints || [];
    var baseTension = 0;
    for (var j = 0; j < events.length; j++) {
      var dw = DOMAIN_TENSION[events[j].domain] || 0.3;
      baseTension = Math.max(baseTension, dw);
    }
    var escalationFactor = Math.min(escalationCount * 0.15, 0.5);
    var turningFactor = Math.min(turningPoints.length * 0.1, 0.3);
    var tension = baseTension * 0.4 + eventDensity * 0.3 + escalationFactor + turningFactor * 0.5;
    return Math.max(0, Math.min(1, tension));
  }

  /* ───────── state ───────── */
  var currentProfile = 'marcus';
  var currentTab = 'slate';
  var currentFramework = 'eudaimonia';
  var chartInstances = {};

  function destroyCharts() {
    for (var k in chartInstances) {
      if (chartInstances[k] && chartInstances[k].destroy) chartInstances[k].destroy();
    }
    chartInstances = {};
  }

  /* ═══════════════════════════════════════════════════════════════════
     INJECT STYLES
     ═══════════════════════════════════════════════════════════════════ */
  var style = document.createElement('style');
  style.textContent = [
    '.duomo-root { font-family: system-ui,-apple-system,sans-serif; color:' + IVORY + '; background:' + BG + '; padding:0; min-height:100vh; }',
    '.duomo-header { text-align:center; padding:48px 24px 24px; border-bottom:1px solid ' + CARD_BORDER + '; }',
    '.duomo-header h1 { font-family:Georgia,serif; font-size:42px; color:' + GOLD + '; margin:0 0 8px; letter-spacing:4px; }',
    '.duomo-header p { color:' + IVORY_MUTED + '; font-size:15px; margin:0; }',
    '.duomo-tabs { display:flex; gap:2px; padding:16px 24px; background:rgba(0,0,0,0.3); border-bottom:1px solid ' + CARD_BORDER + '; flex-wrap:wrap; justify-content:center; }',
    '.duomo-tab { padding:10px 18px; border:1px solid transparent; border-radius:6px; cursor:pointer; font-size:13px; color:' + IVORY_MUTED + '; transition:all .2s; letter-spacing:1px; text-transform:uppercase; background:transparent; }',
    '.duomo-tab:hover { color:' + IVORY + '; border-color:' + GOLD_DIM + '; }',
    '.duomo-tab.active { color:' + GOLD + '; border-color:' + GOLD + '; background:' + GOLD_GLOW + '; }',
    '.duomo-content { padding:32px 24px; max-width:1400px; margin:0 auto; }',
    '.duomo-card { background:' + CARD_BG + '; border:1px solid ' + CARD_BORDER + '; border-radius:10px; padding:24px; margin-bottom:20px; transition:all .3s; }',
    '.duomo-card:hover { border-color:' + GOLD_DIM + '; }',
    '.duomo-card h3 { font-family:Georgia,serif; color:' + GOLD + '; margin:0 0 12px; font-size:18px; }',
    '.duomo-card h4 { color:' + IVORY + '; margin:0 0 8px; font-size:14px; }',
    '.duomo-card p, .duomo-card li { color:' + IVORY_MUTED + '; font-size:13px; line-height:1.6; }',
    '.duomo-grid { display:grid; gap:20px; }',
    '.duomo-grid-2 { grid-template-columns:repeat(auto-fill,minmax(320px,1fr)); }',
    '.duomo-grid-3 { grid-template-columns:repeat(auto-fill,minmax(260px,1fr)); }',
    '.duomo-grid-4 { grid-template-columns:repeat(auto-fill,minmax(200px,1fr)); }',
    '.duomo-profile-card { cursor:pointer; position:relative; }',
    '.duomo-profile-card.selected { border-color:' + GOLD + '; box-shadow:0 0 20px ' + GOLD_GLOW + '; }',
    '.duomo-profile-card .profile-badge { display:inline-block; background:' + GOLD + '; color:' + BG + '; padding:2px 10px; border-radius:20px; font-size:11px; font-weight:700; margin-bottom:8px; }',
    '.duomo-tag { display:inline-block; background:rgba(201,168,76,0.1); border:1px solid ' + CARD_BORDER + '; color:' + GOLD + '; padding:2px 8px; border-radius:4px; font-size:11px; margin:2px; }',
    '.duomo-stat { text-align:center; padding:16px; }',
    '.duomo-stat .val { font-size:28px; font-weight:700; color:' + GOLD + '; font-family:Georgia,serif; }',
    '.duomo-stat .lbl { font-size:11px; color:' + IVORY_MUTED + '; text-transform:uppercase; letter-spacing:1px; margin-top:4px; }',
    '.duomo-bar { height:6px; background:rgba(201,168,76,0.15); border-radius:3px; overflow:hidden; margin:4px 0; }',
    '.duomo-bar-fill { height:100%; background:linear-gradient(90deg,' + GOLD + ',' + GOLD_DIM + '); border-radius:3px; transition:width .6s ease; }',
    '.duomo-section-title { font-family:Georgia,serif; font-size:24px; color:' + GOLD + '; margin:0 0 24px; padding-bottom:12px; border-bottom:1px solid ' + CARD_BORDER + '; }',
    '.duomo-subsection { margin-top:24px; }',
    '.duomo-table { width:100%; border-collapse:collapse; font-size:13px; }',
    '.duomo-table th { text-align:left; padding:8px 12px; color:' + GOLD + '; border-bottom:1px solid ' + CARD_BORDER + '; font-weight:600; font-size:11px; text-transform:uppercase; letter-spacing:1px; }',
    '.duomo-table td { padding:8px 12px; border-bottom:1px solid rgba(201,168,76,0.06); color:' + IVORY_MUTED + '; }',
    '.duomo-chart-container { position:relative; height:300px; margin:16px 0; }',
    '.duomo-chart-container canvas { width:100%!important; }',
    '.duomo-layer-header { font-size:14px; text-transform:uppercase; letter-spacing:2px; color:' + GOLD + '; margin:20px 0 12px; padding:8px 0; border-bottom:1px solid ' + CARD_BORDER + '; }',
    '.duomo-domain-badge { display:inline-flex; align-items:center; gap:6px; padding:6px 12px; border-radius:20px; font-size:12px; margin:4px; }',
    '.duomo-gap-item { padding:12px 16px; border-left:3px solid ' + GOLD + '; margin:8px 0; background:rgba(201,168,76,0.03); border-radius:0 6px 6px 0; }',
    '.duomo-gap-item .gap-name { color:' + GOLD + '; font-weight:600; font-size:13px; }',
    '.duomo-gap-item .gap-cond { color:' + IVORY_MUTED + '; font-size:12px; margin-top:4px; }',
    '.duomo-teammate-card { text-align:center; padding:20px; }',
    '.duomo-teammate-card .tm-icon { width:48px; height:48px; border-radius:50%; display:flex; align-items:center; justify-content:center; margin:0 auto 12px; font-size:20px; }',
    '.duomo-teammate-card .tm-name { font-weight:700; color:' + IVORY + '; font-size:14px; }',
    '.duomo-teammate-card .tm-title { color:' + GOLD + '; font-size:12px; margin:4px 0; }',
    '.duomo-teammate-card .tm-domain { font-size:11px; color:' + IVORY_MUTED + '; text-transform:uppercase; letter-spacing:1px; }',
    '.duomo-pipeline-stage { display:flex; align-items:flex-start; gap:20px; padding:20px; }',
    '.duomo-pipeline-num { font-family:Georgia,serif; font-size:32px; color:' + GOLD_DIM + '; min-width:48px; }',
    '.duomo-pipeline-gate { display:inline-block; padding:2px 8px; border:1px solid ' + GOLD_DIM + '; border-radius:4px; font-size:10px; color:' + GOLD + '; text-transform:uppercase; letter-spacing:1px; margin-top:8px; }',
    '.duomo-trial-chart { display:flex; align-items:flex-end; gap:3px; height:120px; padding:8px 0; }',
    '.duomo-trial-bar { flex:1; border-radius:3px 3px 0 0; transition:height .4s ease; min-width:16px; }',
    '.duomo-arc-timeline { display:flex; gap:2px; align-items:flex-end; height:80px; margin:12px 0; }',
    '.duomo-arc-event { flex:1; border-radius:3px 3px 0 0; min-width:8px; cursor:pointer; position:relative; transition:transform .2s; }',
    '.duomo-arc-event:hover { transform:scaleY(1.1); }',
    '.duomo-expand-detail { margin-top:20px; padding-top:20px; border-top:1px solid ' + CARD_BORDER + '; }',
    '@keyframes duomo-fadein { from { opacity:0; transform:translateY(12px); } to { opacity:1; transform:translateY(0); } }',
    '.duomo-animate { animation: duomo-fadein .4s ease both; }',
    '.duomo-btn { padding:8px 16px; border:1px solid ' + GOLD_DIM + '; background:transparent; color:' + GOLD + '; border-radius:6px; cursor:pointer; font-size:12px; transition:all .2s; }',
    '.duomo-btn:hover { background:' + GOLD_GLOW + '; border-color:' + GOLD + '; }',
    '.duomo-btn.active { background:' + GOLD + '; color:' + BG + '; }',
    '.duomo-score-ring { width:80px; height:80px; border-radius:50%; border:3px solid ' + GOLD_DIM + '; display:flex; align-items:center; justify-content:center; font-family:Georgia,serif; font-size:24px; color:' + GOLD + '; margin:0 auto 8px; }',
    '.duomo-provision-row { padding:10px 0; border-bottom:1px solid rgba(201,168,76,0.06); }',
    '.duomo-provision-row:last-child { border-bottom:none; }',
    '.duomo-provision-score { display:inline-block; width:40px; text-align:center; padding:2px 0; border-radius:4px; font-size:11px; font-weight:700; }',
    '.duomo-framework-btn { padding:6px 14px; margin:4px; }',
    '.duomo-nussbaum-cap { display:flex; align-items:flex-start; gap:12px; padding:12px 0; border-bottom:1px solid rgba(201,168,76,0.06); }',
    '.duomo-nussbaum-num { font-family:Georgia,serif; font-size:20px; color:' + GOLD_DIM + '; min-width:28px; }',
    '.duomo-stats-row { display:flex; gap:12px; flex-wrap:wrap; margin-bottom:24px; }',
    '.duomo-stats-row .duomo-stat { flex:1; min-width:120px; background:' + CARD_BG + '; border:1px solid ' + CARD_BORDER + '; border-radius:8px; }'
  ].join('\n');
  container.innerHTML = '';
  container.appendChild(style);

  /* ═══════════════════════════════════════════════════════════════════
     BUILD SHELL
     ═══════════════════════════════════════════════════════════════════ */
  var root = el('div', 'duomo-root');
  root.innerHTML = [
    '<div class="duomo-header">',
    '  <h1>DUOMO</h1>',
    '  <p>Whole-Person Digital Twin Composer \u2014 12 Life Domains \u2014 5 Canonical Profiles</p>',
    '</div>',
    '<div class="duomo-tabs" id="duomo-tabs"></div>',
    '<div class="duomo-content" id="duomo-content"></div>'
  ].join('');
  container.appendChild(root);

  var tabs = [
    { id: 'slate', label: 'The Apollo Slate' },
    { id: 'profiles', label: 'Profile Explorer' },
    { id: 'domains', label: 'Domain Architecture' },
    { id: 'matcher', label: 'Provision Matcher' },
    { id: 'narrative', label: 'Narrative Studio' },
    { id: 'bio', label: 'Bio Experiments' },
    { id: 'philosophy', label: 'Philosophical Frameworks' },
    { id: 'teammates', label: 'AI Teammates' },
    { id: 'pipeline', label: 'Production Pipeline' }
  ];

  var tabBar = root.querySelector('#duomo-tabs');
  tabs.forEach(function (t) {
    var btn = el('button', 'duomo-tab' + (t.id === currentTab ? ' active' : ''), t.label);
    btn.dataset.tab = t.id;
    btn.addEventListener('click', function () {
      currentTab = t.id;
      $$('.duomo-tab', tabBar).forEach(function (b) { b.classList.remove('active'); });
      btn.classList.add('active');
      renderTab();
    });
    tabBar.appendChild(btn);
  });

  function renderTab() {
    destroyCharts();
    var ct = root.querySelector('#duomo-content');
    ct.innerHTML = '';
    switch (currentTab) {
      case 'slate': renderDuomoSlate(ct); break;
      case 'profiles': renderProfiles(ct); break;
      case 'domains': renderDomains(ct); break;
      case 'matcher': renderMatcher(ct); break;
      case 'narrative': renderNarrative(ct); break;
      case 'bio': renderBio(ct); break;
      case 'philosophy': renderPhilosophy(ct); break;
      case 'teammates': renderTeammates(ct); break;
      case 'pipeline': renderPipeline(ct); break;
    }
  }

  /* ═══════════════════════════════════════════════════════════════════
     A. PROFILE EXPLORER
     ═══════════════════════════════════════════════════════════════════ */
  function renderProfiles(ct) {
    ct.innerHTML = '<h2 class="duomo-section-title">Profile Explorer</h2>';
    // Profile cards
    var grid = el('div', 'duomo-grid duomo-grid-3');
    var keys = ['marcus', 'sarah', 'james', 'maria', 'robert'];
    keys.forEach(function (k) {
      var p = profiles[k];
      var card = el('div', 'duomo-card duomo-profile-card duomo-animate' + (k === currentProfile ? ' selected' : ''));
      card.innerHTML = [
        '<span class="profile-badge">' + p.name + '</span>',
        '<p style="margin:4px 0;"><strong>Age:</strong> ' + p.age + ' &middot; <strong>Location:</strong> ' + p.location + '</p>',
        '<p style="margin:4px 0;"><strong>Conditions:</strong> ' + (p.conditions || []).join(', ') + '</p>',
        '<p style="margin:4px 0;"><strong>Systems:</strong> ' + (p.systems || []).length + ' involved</p>',
        '<div style="display:flex;gap:8px;margin-top:12px;">',
        '  <div class="duomo-stat" style="padding:8px;flex:1;"><div class="val" style="font-size:18px;">' + fmtFull(p.costFragmented) + '</div><div class="lbl">Fragmented</div></div>',
        '  <div class="duomo-stat" style="padding:8px;flex:1;"><div class="val" style="font-size:18px;">' + fmtFull(p.costCoordinated) + '</div><div class="lbl">Coordinated</div></div>',
        '  <div class="duomo-stat" style="padding:8px;flex:1;"><div class="val" style="font-size:18px;color:#4CAF50;">' + fmtFull(p.delta) + '</div><div class="lbl">Savings</div></div>',
        '</div>'
      ].join('');
      card.addEventListener('click', function () {
        currentProfile = k;
        renderProfiles(ct);
      });
      grid.appendChild(card);
    });
    ct.appendChild(grid);

    // Selected profile detail
    var pk = currentProfile;
    var p = profiles[pk];
    var pd = profileDomains[pk];
    if (!pd) return;

    var detail = el('div', 'duomo-expand-detail duomo-animate');
    detail.style.animationDelay = '0.2s';

    // Stats row
    var statsHtml = '<div class="duomo-stats-row">';
    statsHtml += '<div class="duomo-stat"><div class="val">' + fmtFull(p.costFragmented) + '</div><div class="lbl">Annual Fragmented</div></div>';
    statsHtml += '<div class="duomo-stat"><div class="val">' + fmtFull(p.costCoordinated) + '</div><div class="lbl">Annual Coordinated</div></div>';
    statsHtml += '<div class="duomo-stat"><div class="val" style="color:#4CAF50;">' + fmtFull(p.delta) + '</div><div class="lbl">Annual Savings</div></div>';
    statsHtml += '<div class="duomo-stat"><div class="val">' + fmtFull(pd.fiveYear) + '</div><div class="lbl">5-Year Projection</div></div>';
    statsHtml += '<div class="duomo-stat"><div class="val">' + fmtFull(pd.lifetime) + '</div><div class="lbl">Lifetime Estimate</div></div>';
    statsHtml += '</div>';
    detail.innerHTML = statsHtml;

    // Domain breakdown
    var domainSection = el('div', 'duomo-subsection');
    domainSection.innerHTML = '<h3 style="color:' + GOLD + ';font-family:Georgia,serif;margin-bottom:16px;">Domain Breakdown — ' + p.name + '</h3>';

    // Chart
    var chartWrap = el('div', 'duomo-chart-container');
    chartWrap.style.height = '280px';
    var canvas = document.createElement('canvas');
    chartWrap.appendChild(canvas);
    domainSection.appendChild(chartWrap);

    // Domain table
    var table = el('table', 'duomo-table');
    table.innerHTML = '<thead><tr><th>Domain</th><th>Fragmented</th><th>Coordinated</th><th>Savings</th><th>Systems</th></tr></thead>';
    var tbody = el('tbody');
    pd.domains.forEach(function (d) {
      var tr = el('tr');
      tr.innerHTML = '<td style="color:' + IVORY + ';font-weight:600;">' + d.label + '</td>' +
        '<td>' + fmtFull(d.fragmented) + '</td>' +
        '<td>' + fmtFull(d.coordinated) + '</td>' +
        '<td style="color:#4CAF50;">' + fmtFull(d.savings) + '</td>' +
        '<td>' + d.systems.map(function (s) { return '<span class="duomo-tag">' + s.label + '</span>'; }).join('') + '</td>';
      tbody.appendChild(tr);
    });
    table.appendChild(tbody);
    domainSection.appendChild(table);
    detail.appendChild(domainSection);

    // Provider matches
    var matchedProviders = providers.filter(function (pr) { return pr.profiles.indexOf(pk) >= 0; });
    if (matchedProviders.length > 0) {
      var provSection = el('div', 'duomo-subsection');
      provSection.innerHTML = '<h3 style="color:' + GOLD + ';font-family:Georgia,serif;margin-bottom:16px;">Matched Providers</h3>';
      var provGrid = el('div', 'duomo-grid duomo-grid-2');
      matchedProviders.forEach(function (pr) {
        var card = el('div', 'duomo-card');
        card.innerHTML = '<h4>' + pr.name + '</h4>' +
          '<p style="margin:4px 0;">' + pr.address + '</p>' +
          '<div>' + pr.services.map(function (s) { return '<span class="duomo-tag">' + s.replace(/_/g, ' ') + '</span>'; }).join('') + '</div>';
        provGrid.appendChild(card);
      });
      provSection.appendChild(provGrid);
      detail.appendChild(provSection);
    }

    // Systems tags
    var sysSection = el('div', 'duomo-subsection');
    sysSection.innerHTML = '<h3 style="color:' + GOLD + ';font-family:Georgia,serif;margin-bottom:12px;">Systems Involved</h3>';
    sysSection.innerHTML += '<div>' + (p.systems || []).map(function (s) { return '<span class="duomo-tag">' + s + '</span>'; }).join('') + '</div>';
    detail.appendChild(sysSection);

    ct.appendChild(detail);

    // Render chart after DOM insertion
    setTimeout(function () {
      var labels = pd.domains.map(function (d) { return d.label; });
      var fragData = pd.domains.map(function (d) { return d.fragmented; });
      var coordData = pd.domains.map(function (d) { return d.coordinated; });
      if (typeof Chart !== 'undefined') {
        chartInstances.profileBar = new Chart(canvas, {
          type: 'bar',
          data: {
            labels: labels,
            datasets: [
              { label: 'Fragmented Cost', data: fragData, backgroundColor: 'rgba(201,168,76,0.6)', borderColor: GOLD, borderWidth: 1 },
              { label: 'Coordinated Cost', data: coordData, backgroundColor: 'rgba(76,175,80,0.5)', borderColor: '#4CAF50', borderWidth: 1 }
            ]
          },
          options: {
            responsive: true, maintainAspectRatio: false,
            plugins: { legend: { labels: { color: IVORY_MUTED, font: { size: 11 } } } },
            scales: {
              x: { ticks: { color: IVORY_MUTED, font: { size: 11 } }, grid: { color: 'rgba(201,168,76,0.06)' } },
              y: { ticks: { color: IVORY_MUTED, font: { size: 11 }, callback: function (v) { return fmt(v); } }, grid: { color: 'rgba(201,168,76,0.06)' } }
            }
          }
        });
      }
    }, 50);
  }

  /* ═══════════════════════════════════════════════════════════════════
     B. DOMAIN ARCHITECTURE
     ═══════════════════════════════════════════════════════════════════ */
  function renderDomains(ct) {
    ct.innerHTML = '<h2 class="duomo-section-title">Domain Architecture</h2>';
    ct.innerHTML += '<p style="color:' + IVORY_MUTED + ';margin-bottom:24px;">12 BATHS domains organized in 3 flourishing layers. Each domain represents a dimension of whole-person wellbeing.</p>';

    var layers = [
      { name: 'Foundation', color: '#4CAF50', domains: flourishingDomains.foundation },
      { name: 'Aspiration', color: '#2196F3', domains: flourishingDomains.aspiration },
      { name: 'Transcendence', color: '#9C27B0', domains: flourishingDomains.transcendence }
    ];

    layers.forEach(function (layer, li) {
      var section = el('div', 'duomo-animate');
      section.style.animationDelay = (li * 0.15) + 's';
      section.innerHTML = '<div class="duomo-layer-header" style="color:' + layer.color + ';">' + layer.name + ' Layer (' + layer.domains.length + ' domains)</div>';
      var grid = el('div', 'duomo-grid duomo-grid-3');
      layer.domains.forEach(function (d) {
        var card = el('div', 'duomo-card');
        card.style.borderLeft = '3px solid ' + layer.color;
        card.innerHTML = '<h3 style="color:' + layer.color + ';">' + d.name + '</h3><p>' + d.desc + '</p>';
        grid.appendChild(card);
      });
      section.appendChild(grid);
      ct.appendChild(section);
    });

    // Domain scores chart for selected profile
    var pk = currentProfile;
    var scores = profileFlourishingScores[pk];
    if (scores) {
      var chartSection = el('div', 'duomo-card duomo-animate');
      chartSection.style.animationDelay = '0.4s';
      chartSection.innerHTML = '<h3>Flourishing Scores — ' + profiles[pk].name + '</h3><p>Radar view of domain coverage. Scale: 0\u2013100.</p>';
      var chartWrap = el('div', 'duomo-chart-container');
      chartWrap.style.height = '350px';
      var canvas = document.createElement('canvas');
      chartWrap.appendChild(canvas);
      chartSection.appendChild(chartWrap);
      ct.appendChild(chartSection);

      setTimeout(function () {
        if (typeof Chart === 'undefined') return;
        var labels = Object.keys(scores).map(function (k) { return k.replace(/_/g, ' ').replace(/\b\w/g, function (l) { return l.toUpperCase(); }); });
        var data = Object.values(scores);
        chartInstances.domainRadar = new Chart(canvas, {
          type: 'radar',
          data: {
            labels: labels,
            datasets: [{
              label: profiles[pk].name,
              data: data,
              backgroundColor: 'rgba(201,168,76,0.15)',
              borderColor: GOLD,
              borderWidth: 2,
              pointBackgroundColor: GOLD,
              pointRadius: 4
            }]
          },
          options: {
            responsive: true, maintainAspectRatio: false,
            scales: { r: { min: 0, max: 100, ticks: { color: IVORY_MUTED, backdropColor: 'transparent', font: { size: 10 } }, grid: { color: 'rgba(201,168,76,0.1)' }, pointLabels: { color: IVORY_MUTED, font: { size: 10 } } } },
            plugins: { legend: { labels: { color: IVORY_MUTED } } }
          }
        });
      }, 50);
    }
  }

  /* ═══════════════════════════════════════════════════════════════════
     C. PROVISION MATCHER
     ═══════════════════════════════════════════════════════════════════ */
  function renderMatcher(ct) {
    ct.innerHTML = '<h2 class="duomo-section-title">Provision Matcher</h2>';
    ct.innerHTML += '<p style="color:' + IVORY_MUTED + ';margin-bottom:24px;">Real matching algorithm ported from Python. Scores provisions against the selected profile using TYPE_WEIGHT \u00d7 base_score. Gap detection uses 15 rules from the audit.</p>';

    // Profile selector row
    var selRow = el('div', '', '');
    selRow.style.cssText = 'display:flex;gap:8px;margin-bottom:24px;flex-wrap:wrap;';
    ['marcus', 'sarah', 'james', 'maria', 'robert'].forEach(function (k) {
      var btn = el('button', 'duomo-btn' + (k === currentProfile ? ' active' : ''), profiles[k].name);
      btn.addEventListener('click', function () { currentProfile = k; renderMatcher(ct); });
      selRow.appendChild(btn);
    });
    ct.appendChild(selRow);

    var pk = currentProfile;
    var matches = matchProvisions(pk);
    var gaps = detectGaps(pk);

    // Algorithm display
    var algoCard = el('div', 'duomo-card duomo-animate');
    algoCard.innerHTML = '<h3>Matching Algorithm</h3>' +
      '<table class="duomo-table"><thead><tr><th>Type</th><th>Weight</th></tr></thead><tbody>' +
      Object.keys(TYPE_WEIGHT).map(function (k) { return '<tr><td>' + k + '</td><td>' + TYPE_WEIGHT[k] + '</td></tr>'; }).join('') +
      '</tbody></table>' +
      '<p style="margin-top:12px;">Score = base_score \u00d7 type_weight. Base: ratio\u22651.0\u21921.0, \u22650.75\u21920.8, \u22650.5\u21920.6, else\u21920.5. Universal provisions: 0.4.</p>';
    ct.appendChild(algoCard);

    // Matched provisions
    var matchCard = el('div', 'duomo-card duomo-animate');
    matchCard.style.animationDelay = '0.1s';
    matchCard.innerHTML = '<h3>Matched Provisions for ' + profiles[pk].name + ' (' + matches.length + ' matches)</h3>';
    matches.forEach(function (m) {
      var row = el('div', 'duomo-provision-row');
      var scoreColor = m.relevance >= 0.8 ? '#4CAF50' : m.relevance >= 0.6 ? GOLD : '#FF9800';
      row.innerHTML = '<div style="display:flex;align-items:center;gap:12px;">' +
        '<span class="duomo-provision-score" style="background:' + scoreColor + '22;color:' + scoreColor + ';">' + m.relevance.toFixed(2) + '</span>' +
        '<div><div style="color:' + IVORY + ';font-weight:600;font-size:13px;">' + m.title + '</div>' +
        '<div style="color:' + IVORY_MUTED + ';font-size:11px;">' + m.citation + ' \u2014 ' + m.domain + '</div></div></div>';
      matchCard.appendChild(row);
    });
    ct.appendChild(matchCard);

    // Gap detection
    var gapCard = el('div', 'duomo-card duomo-animate');
    gapCard.style.animationDelay = '0.2s';
    gapCard.innerHTML = '<h3>Gap Detection (' + gaps.length + ' gaps found)</h3><p>Rules triggered for ' + profiles[pk].name + '. Each gap has relevance 0.9 and is_gap=true.</p>';
    if (gaps.length === 0) {
      gapCard.innerHTML += '<p style="color:' + IVORY_FAINT + ';">No gap rules triggered for this profile.</p>';
    }
    gaps.forEach(function (g) {
      var item = el('div', 'duomo-gap-item');
      item.innerHTML = '<div class="gap-name">' + g.desc + '</div><div class="gap-cond">Condition: ' + g.condition + ' \u2014 Relevance: ' + g.relevance + '</div>';
      gapCard.appendChild(item);
    });
    ct.appendChild(gapCard);
  }

  /* ═══════════════════════════════════════════════════════════════════
     D. NARRATIVE STUDIO
     ═══════════════════════════════════════════════════════════════════ */
  function renderNarrative(ct) {
    ct.innerHTML = '<h2 class="duomo-section-title">Narrative Studio</h2>';
    ct.innerHTML += '<p style="color:' + IVORY_MUTED + ';margin-bottom:24px;">Narrative synthesis engine. Arc types: rising_tension, turning_point, fall_and_recovery, slow_burn, cascade, breakthrough. Tension scoring formula: base_tension\u00d70.4 + event_density\u00d70.3 + escalation + turning\u00d70.5.</p>';

    var keys = ['marcus', 'sarah', 'james', 'maria', 'robert'];
    keys.forEach(function (k, ki) {
      var arc = narrativeArcs[k];
      var p = profiles[k];
      var tension = scoreTension(arc);
      var mediumLabel = { doc: 'Documentary', series: 'Series', short: 'Short Film', installation: 'Installation' };

      var card = el('div', 'duomo-card duomo-animate');
      card.style.animationDelay = (ki * 0.1) + 's';

      var arcColor = tension >= 0.8 ? '#f44336' : tension >= 0.6 ? '#FF9800' : tension >= 0.4 ? GOLD : '#4CAF50';

      var html = '<div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:16px;">';
      html += '<div><h3 style="margin-bottom:4px;">' + arc.title + '</h3>';
      html += '<p style="margin:0;">' + p.name + ' \u2014 <span style="color:' + arcColor + ';">' + arc.arcType.replace(/_/g, ' ') + '</span></p></div>';
      html += '<div style="text-align:center;">';
      html += '<div class="duomo-score-ring" style="border-color:' + arcColor + ';color:' + arcColor + ';">' + (Math.round(tension * 100)) + '</div>';
      html += '<div style="font-size:11px;color:' + IVORY_MUTED + ';">Tension Score</div></div></div>';

      // Arc timeline
      html += '<div class="duomo-arc-timeline">';
      var maxDay = 1;
      arc.events.forEach(function (e) { if (e.day > maxDay) maxDay = e.day; });
      arc.events.forEach(function (e) {
        var isTurning = arc.turningPoints.indexOf(e.type) >= 0;
        var domainW = DOMAIN_TENSION[e.domain] || 0.3;
        var h = 20 + domainW * 60;
        var color = isTurning ? '#4CAF50' : arcColor;
        html += '<div class="duomo-arc-event" style="height:' + h + 'px;background:' + color + ';opacity:0.8;" title="Day ' + e.day + ': ' + e.type.replace(/_/g, ' ') + ' (' + e.domain + ')"></div>';
      });
      html += '</div>';

      // Details
      html += '<div style="display:flex;gap:20px;flex-wrap:wrap;margin-top:12px;">';
      html += '<div><strong style="color:' + IVORY_FAINT + ';">Medium:</strong> <span style="color:' + GOLD + ';">' + (mediumLabel[arc.medium] || arc.medium) + '</span></div>';
      html += '<div><strong style="color:' + IVORY_FAINT + ';">Events:</strong> ' + arc.events.length + '</div>';
      html += '<div><strong style="color:' + IVORY_FAINT + ';">Turning Points:</strong> ' + arc.turningPoints.length + '</div>';
      html += '</div>';

      // Medium recommendation logic
      html += '<p style="font-size:11px;color:' + IVORY_FAINT + ';margin-top:8px;">Recommendation: tension \u2265 0.8 \u2192 documentary, \u2265 0.7 \u2192 series, \u2265 0.5 \u2192 short, else \u2192 installation</p>';

      card.innerHTML = html;
      ct.appendChild(card);
    });

    // Domain tension weights reference
    var refCard = el('div', 'duomo-card duomo-animate');
    refCard.innerHTML = '<h3>Domain Tension Weights</h3>';
    refCard.innerHTML += '<div style="display:flex;gap:8px;flex-wrap:wrap;">';
    Object.keys(DOMAIN_TENSION).forEach(function (k) {
      var w = DOMAIN_TENSION[k];
      refCard.innerHTML += '<div style="padding:6px 12px;border-radius:6px;background:rgba(201,168,76,' + (w * 0.3) + ');border:1px solid ' + CARD_BORDER + ';"><div style="font-weight:700;color:' + IVORY + ';font-size:12px;">' + k + '</div><div style="color:' + GOLD + ';font-size:16px;">' + w + '</div></div>';
    });
    refCard.innerHTML += '</div>';
    ct.appendChild(refCard);
  }

  /* ═══════════════════════════════════════════════════════════════════
     E. BIO EXPERIMENT DESIGNER
     ═══════════════════════════════════════════════════════════════════ */
  function renderBio(ct) {
    ct.innerHTML = '<h2 class="duomo-section-title">Bio Experiment Designer</h2>';
    ct.innerHTML += '<p style="color:' + IVORY_MUTED + ';margin-bottom:24px;">N-of-1 ABAB trial design. Analysis: Cohen\u2019s d effect size, Welch\u2019s t-test p-value, Bayesian P(intervention > control). Early stopping: decisive benefit (\u2265 0.95 prob), futility (\u2264 0.05), negligible effect (\u2265 20 measurements, |d| < 0.2).</p>';

    var keys = ['marcus', 'sarah', 'james', 'maria', 'robert'];
    keys.forEach(function (k, ki) {
      var config = trialConfigs[k];
      var p = profiles[k];
      var result = analyzeTrial(config);

      var card = el('div', 'duomo-card duomo-animate');
      card.style.animationDelay = (ki * 0.1) + 's';

      var html = '<h3>' + p.name + ' \u2014 N-of-1 Trial</h3>';
      html += '<p><strong>Hypothesis:</strong> ' + config.hypothesis + '</p>';
      html += '<div style="display:flex;gap:16px;flex-wrap:wrap;margin:12px 0;">';
      html += '<div class="duomo-card" style="flex:1;min-width:200px;padding:12px;"><h4 style="color:#f44336;">Control</h4><p>' + config.control + '</p></div>';
      html += '<div class="duomo-card" style="flex:1;min-width:200px;padding:12px;border-color:#4CAF50;"><h4 style="color:#4CAF50;">Intervention</h4><p>' + config.intervention + '</p></div>';
      html += '</div>';

      // Trial chart — bar visualization
      html += '<div style="margin:16px 0;"><div style="font-size:11px;color:' + IVORY_MUTED + ';margin-bottom:6px;">Metric: ' + config.metric + '</div>';
      html += '<div class="duomo-trial-chart">';
      var allVals = config.controlData.concat(config.interventionData);
      var maxVal = Math.max.apply(null, allVals);
      config.controlData.forEach(function (v) {
        html += '<div class="duomo-trial-bar" style="height:' + (v / maxVal * 100) + '%;background:rgba(244,67,54,0.6);"></div>';
      });
      // Washout gap
      html += '<div style="width:8px;"></div>';
      config.interventionData.forEach(function (v) {
        html += '<div class="duomo-trial-bar" style="height:' + (v / maxVal * 100) + '%;background:rgba(76,175,80,0.6);"></div>';
      });
      html += '</div>';
      html += '<div style="display:flex;justify-content:space-between;font-size:10px;color:' + IVORY_FAINT + ';"><span>Control Phase</span><span>Washout</span><span>Intervention Phase</span></div></div>';

      // Results
      html += '<div class="duomo-stats-row" style="margin-top:16px;">';
      html += '<div class="duomo-stat"><div class="val" style="font-size:18px;">' + result.controlMean + '</div><div class="lbl">Control Mean</div></div>';
      html += '<div class="duomo-stat"><div class="val" style="font-size:18px;color:#4CAF50;">' + result.interventionMean + '</div><div class="lbl">Intervention Mean</div></div>';
      html += '<div class="duomo-stat"><div class="val" style="font-size:18px;">' + result.effectSize + '</div><div class="lbl">Effect Size (d)</div></div>';
      html += '<div class="duomo-stat"><div class="val" style="font-size:18px;">' + result.pValue + '</div><div class="lbl">p-value</div></div>';
      html += '<div class="duomo-stat"><div class="val" style="font-size:18px;">' + result.bayesianProb + '</div><div class="lbl">P(Intervention Better)</div></div>';
      html += '</div>';

      // Recommendation
      var recColor = result.recommendation.indexOf('Strong') >= 0 ? '#4CAF50' : result.recommendation.indexOf('Statist') >= 0 ? '#2196F3' : GOLD;
      html += '<div style="padding:12px;border-radius:6px;background:' + recColor + '11;border:1px solid ' + recColor + '33;margin-top:8px;">';
      html += '<strong style="color:' + recColor + ';">' + result.recommendation + '</strong></div>';

      card.innerHTML = html;
      ct.appendChild(card);
    });
  }

  /* ═══════════════════════════════════════════════════════════════════
     F. PHILOSOPHICAL FRAMEWORKS
     ═══════════════════════════════════════════════════════════════════ */
  function renderPhilosophy(ct) {
    ct.innerHTML = '<h2 class="duomo-section-title">Philosophical Frameworks</h2>';
    ct.innerHTML += '<p style="color:' + IVORY_MUTED + ';margin-bottom:24px;">6 traditions informing DUOMO\'s whole-person architecture. Select a framework to see how it maps to the 12 flourishing domains.</p>';

    // Framework selector
    var selRow = el('div', '', '');
    selRow.style.cssText = 'display:flex;gap:4px;margin-bottom:24px;flex-wrap:wrap;';
    philosophicalTraditions.forEach(function (t) {
      var btn = el('button', 'duomo-btn duomo-framework-btn' + (t.id === currentFramework ? ' active' : ''), t.name);
      btn.addEventListener('click', function () { currentFramework = t.id; renderPhilosophy(ct); });
      selRow.appendChild(btn);
    });
    ct.appendChild(selRow);

    // Selected framework detail
    var fw = philosophicalTraditions.find(function (t) { return t.id === currentFramework; });
    if (fw) {
      var card = el('div', 'duomo-card duomo-animate');
      card.innerHTML = '<h3>' + fw.name + '</h3>' +
        '<p style="color:' + IVORY + ';font-size:14px;margin-bottom:8px;"><strong>Thinker:</strong> ' + fw.thinker + '</p>' +
        '<p style="font-style:italic;color:' + GOLD + ';margin-bottom:16px;">"' + fw.core + '"</p>' +
        '<h4>Key Principles</h4><ul>' + fw.principles.map(function (p) { return '<li>' + p + '</li>'; }).join('') + '</ul>' +
        '<h4 style="margin-top:16px;">Mapping to DUOMO Domains</h4><p>' + fw.flourishingMap + '</p>';
      ct.appendChild(card);
    }

    // All frameworks grid
    var grid = el('div', 'duomo-grid duomo-grid-2');
    philosophicalTraditions.forEach(function (t, i) {
      var card = el('div', 'duomo-card duomo-animate');
      card.style.animationDelay = (i * 0.08) + 's';
      card.style.cursor = 'pointer';
      if (t.id === currentFramework) card.style.borderColor = GOLD;
      card.innerHTML = '<h3>' + t.name + '</h3><p style="color:' + IVORY + ';font-size:12px;">' + t.thinker + '</p><p style="font-size:12px;">' + t.core.substring(0, 120) + '...</p>';
      card.addEventListener('click', function () { currentFramework = t.id; renderPhilosophy(ct); });
      grid.appendChild(card);
    });
    ct.appendChild(grid);

    // Nussbaum's 10 capabilities
    var nCard = el('div', 'duomo-card duomo-animate');
    nCard.style.animationDelay = '0.5s';
    nCard.innerHTML = '<h3>Nussbaum\u2019s 10 Central Capabilities \u2192 DUOMO Domains</h3>';
    nussbaumCapabilities.forEach(function (cap) {
      var row = el('div', 'duomo-nussbaum-cap');
      row.innerHTML = '<div class="duomo-nussbaum-num">' + cap.num + '</div>' +
        '<div><div style="color:' + IVORY + ';font-weight:600;font-size:14px;">' + cap.name + '</div>' +
        '<div style="color:' + IVORY_MUTED + ';font-size:12px;margin:4px 0;">' + cap.desc + '</div>' +
        '<div>' + cap.domains.map(function (d) { return '<span class="duomo-tag">' + d.replace(/_/g, ' ') + '</span>'; }).join('') + '</div></div>';
      nCard.appendChild(row);
    });
    ct.appendChild(nCard);
  }

  /* ═══════════════════════════════════════════════════════════════════
     G. AI TEAMMATES
     ═══════════════════════════════════════════════════════════════════ */
  function renderTeammates(ct) {
    ct.innerHTML = '<h2 class="duomo-section-title">AI Teammates</h2>';
    ct.innerHTML += '<p style="color:' + IVORY_MUTED + ';margin-bottom:24px;">12 AI teammates from the Innovation Lab. Each brings domain expertise to generate novel service-delivery innovations.</p>';

    var grid = el('div', 'duomo-grid duomo-grid-4');
    aiTeammates.forEach(function (tm, i) {
      var card = el('div', 'duomo-card duomo-teammate-card duomo-animate');
      card.style.animationDelay = (i * 0.05) + 's';
      card.innerHTML = '<div class="tm-icon" style="background:' + tm.color + '22;border:2px solid ' + tm.color + ';color:' + tm.color + ';">' + tm.name.charAt(4).toUpperCase() + '</div>' +
        '<div class="tm-name">' + tm.name + '</div>' +
        '<div class="tm-title">' + tm.title + '</div>' +
        '<div class="tm-domain">' + tm.domain + '</div>' +
        '<p style="margin-top:8px;font-size:11px;">' + tm.desc + '</p>';
      grid.appendChild(card);
    });
    ct.appendChild(grid);
  }

  /* ═══════════════════════════════════════════════════════════════════
     H. PRODUCTION PIPELINE
     ═══════════════════════════════════════════════════════════════════ */
  function renderPipeline(ct) {
    ct.innerHTML = '<h2 class="duomo-section-title">Production Pipeline</h2>';
    ct.innerHTML += '<p style="color:' + IVORY_MUTED + ';margin-bottom:24px;">5-stage DUOMO production pipeline. Each stage has gate requirements that must be met before advancing.</p>';

    pipelineStages.forEach(function (stage, i) {
      var card = el('div', 'duomo-card duomo-animate');
      card.style.animationDelay = (i * 0.1) + 's';
      card.innerHTML = '<div class="duomo-pipeline-stage">' +
        '<div class="duomo-pipeline-num">' + stage.num + '</div>' +
        '<div style="flex:1;"><h3 style="margin-bottom:4px;">' + stage.label + '</h3>' +
        '<p>' + stage.desc + '</p>' +
        '<div style="margin-top:12px;"><strong style="color:' + IVORY + ';font-size:12px;">Deliverables:</strong></div>' +
        '<div style="margin-top:4px;">' + stage.deliverables.map(function (d) { return '<span class="duomo-tag">' + d + '</span>'; }).join('') + '</div>' +
        '<div class="duomo-pipeline-gate" style="margin-top:12px;">Gate: ' + stage.gate + '</div>' +
        '</div></div>';
      ct.appendChild(card);
    });

    // Gate requirements reference
    var gateCard = el('div', 'duomo-card duomo-animate');
    gateCard.style.animationDelay = '0.5s';
    gateCard.innerHTML = '<h3>Gate Requirements</h3>' +
      '<table class="duomo-table"><thead><tr><th>Gate</th><th>Requirements</th></tr></thead><tbody>' +
      '<tr><td style="color:' + GOLD + ';">greenlight</td><td>Character ID present; consent tier appropriate; \u22651 Showrunner; budget > 0</td></tr>' +
      '<tr><td style="color:' + GOLD + ';">pre_production</td><td>Dome build sheet complete; team \u2265 2; all development deliverables done</td></tr>' +
      '<tr><td style="color:' + GOLD + ';">production</td><td>Skeleton key pack started; ethics review (real characters); budget allocated</td></tr>' +
      '<tr><td style="color:' + GOLD + ';">picture_lock</td><td>\u22651 IP asset; gap log has entries; all production deliverables done</td></tr>' +
      '<tr><td style="color:' + GOLD + ';">ship</td><td>Learning package generated; all gaps triaged; IP rights registered</td></tr>' +
      '</tbody></table>';
    ct.appendChild(gateCard);
  }

  /* ═══════════════════════════════════════════════════════════════════
     EXTENDED: CAPITAL MARKETS SECTION
     ═══════════════════════════════════════════════════════════════════ */
  // Prevention-Backed Securities data (from capital_markets.py)
  var PAYOUT_RATIO = 0.70;
  var TRANCHE_YIELD_MULT = { senior: 0.6, mezzanine: 1.0, equity: 1.5 };
  var TRANCHE_RISK_MULT = { senior: 0.4, mezzanine: 1.0, equity: 1.8 };
  var DEFAULT_SCENARIOS = { recession: 0.30, moderate: 0.15, baseline: 0.00 };

  // Settlement contracts per profile
  var settlementContracts = {
    marcus: {
      interventionType: 'MAT + coordinated reentry',
      expectedSavings: { medicaid: 12000, corrections: 15000, shelter: 8000, employer: 4000 },
      probabilityOfSuccess: 0.72,
      verificationMethod: 'Claims data + employment records',
      termYears: 3
    },
    sarah: {
      interventionType: 'Trauma-focused CBT + housing stability',
      expectedSavings: { medicaid: 8000, tanf: 4800, child_welfare: 12000, housing: 3600 },
      probabilityOfSuccess: 0.68,
      verificationMethod: 'Clinical outcomes + housing retention',
      termYears: 2
    },
    james: {
      interventionType: 'Integrated VA + community care coordination',
      expectedSavings: { va: 14000, medicaid: 6000, er_avoidance: 8000 },
      probabilityOfSuccess: 0.75,
      verificationMethod: 'VA records + community health metrics',
      termYears: 3
    },
    maria: {
      interventionType: 'Trauma-informed mentoring + educational support',
      expectedSavings: { juvenile_justice: 8000, education: 4000, child_welfare: 10000 },
      probabilityOfSuccess: 0.65,
      verificationMethod: 'School records + case disposition',
      termYears: 2
    },
    robert: {
      interventionType: 'Housing First + ACT team + benefits coordination',
      expectedSavings: { medicaid: 18000, er_avoidance: 45000, shelter: 12000, corrections: 5000 },
      probabilityOfSuccess: 0.58,
      verificationMethod: 'Housing retention + ER utilization data',
      termYears: 3
    }
  };

  function poolContracts(contractKeys, tranche) {
    var contracts = contractKeys.map(function(k) { return settlementContracts[k]; });
    var totalNotional = 0;
    var weightedYieldSum = 0;
    contracts.forEach(function(c) {
      var totalSavings = 0;
      for (var payer in c.expectedSavings) totalSavings += c.expectedSavings[payer];
      var weighted = totalSavings * c.probabilityOfSuccess;
      totalNotional += weighted;
      weightedYieldSum += c.probabilityOfSuccess * weighted;
    });
    var baseYield = totalNotional > 0 ? weightedYieldSum / totalNotional : 0;
    var trancheMult = TRANCHE_YIELD_MULT[tranche] || 1.0;
    var expectedYield = baseYield * trancheMult;
    var couponRate = expectedYield * PAYOUT_RATIO;
    return {
      totalNotional: Math.round(totalNotional),
      expectedYield: Math.round(expectedYield * 10000) / 10000,
      couponRate: Math.round(couponRate * 10000) / 10000,
      contractCount: contracts.length,
      tranche: tranche
    };
  }

  function priceBond(contractKeys, discountRate) {
    discountRate = discountRate || 0.05;
    var contracts = contractKeys.map(function(k) { return settlementContracts[k]; });
    var expectedCF = 0;
    var variance = 0;
    var defaultProbProduct = 1;
    contracts.forEach(function(c) {
      var totalSavings = 0;
      for (var payer in c.expectedSavings) totalSavings += c.expectedSavings[payer];
      for (var t = 1; t <= c.termYears; t++) {
        expectedCF += (c.probabilityOfSuccess * totalSavings) / Math.pow(1 + discountRate, t);
      }
      variance += c.probabilityOfSuccess * (1 - c.probabilityOfSuccess) * totalSavings * totalSavings;
      defaultProbProduct *= (1 - c.probabilityOfSuccess);
    });
    var pool = poolContracts(contractKeys, 'mezzanine');
    return {
      expectedReturn: Math.round(expectedCF - pool.totalNotional),
      var95: Math.round(1.645 * Math.sqrt(variance)),
      defaultProbability: Math.round(defaultProbProduct * 10000) / 10000,
      expectedCashFlow: Math.round(expectedCF)
    };
  }

  // Stress test scenarios
  function stressTest(contractKeys) {
    var results = {};
    for (var scenario in DEFAULT_SCENARIOS) {
      var drop = DEFAULT_SCENARIOS[scenario];
      var adjustedCF = 0;
      contractKeys.forEach(function(k) {
        var c = settlementContracts[k];
        var adjustedProb = Math.max(0, c.probabilityOfSuccess - drop);
        var totalSavings = 0;
        for (var payer in c.expectedSavings) totalSavings += c.expectedSavings[payer];
        adjustedCF += adjustedProb * totalSavings;
      });
      results[scenario] = Math.round(adjustedCF);
    }
    return results;
  }

  /* ═══════════════════════════════════════════════════════════════════
     EXTENDED: TREASURY / CLIFF GUARD
     ═══════════════════════════════════════════════════════════════════ */
  // Benefit phase-out schedules (from treasury.py)
  var PHASE_OUTS = {
    snap:     { floor: 18000, ceiling: 36000 },
    medicaid: { floor: 20000, ceiling: 40000 },
    tanf:     { floor: 10000, ceiling: 24000 },
    housing:  { floor: 15000, ceiling: 45000 },
    ccdf:     { floor: 20000, ceiling: 50000 },
    ssi:      { floor: 10000, ceiling: 28000 },
    liheap:   { floor: 15000, ceiling: 30000 },
    wic:      { floor: 22000, ceiling: 48000 },
    eitc:     { floor: 15000, ceiling: 55000 }
  };

  function benefitAtIncome(program, baseAmount, income) {
    var po = PHASE_OUTS[program];
    if (!po) return baseAmount;
    if (income <= po.floor) return baseAmount;
    if (income >= po.ceiling) return 0;
    var frac = (po.ceiling - income) / (po.ceiling - po.floor);
    return Math.round(baseAmount * frac);
  }

  function calculateCliffGuard(profileKey) {
    var p = profiles[profileKey];
    var benefits = p.benefits || {};
    var currentIncome = p.income || 0;
    var maxIncome = Math.max(currentIncome * 3, 150000);
    var step = 500;
    var results = [];
    var cliffZones = [];
    var maxSafeIncome = currentIncome;

    for (var inc = currentIncome; inc <= maxIncome; inc += step) {
      var totalBenefits = 0;
      for (var prog in benefits) {
        totalBenefits += benefitAtIncome(prog, benefits[prog], inc);
      }
      var totalResources = inc + totalBenefits;
      var prevTotal = results.length > 0 ? results[results.length - 1].totalResources : (currentIncome + Object.values(benefits).reduce(function(a,b){ return a+b; }, 0));
      var netGain = totalResources - prevTotal;
      var emtr = step > 0 ? 1.0 - (netGain / step) : 0;

      results.push({
        income: inc,
        benefits: totalBenefits,
        totalResources: totalResources,
        emtr: Math.round(emtr * 100) / 100
      });

      if (emtr > 0.5) {
        if (cliffZones.length === 0 || cliffZones[cliffZones.length - 1] !== inc - step) {
          cliffZones.push(inc);
        }
      } else {
        maxSafeIncome = inc;
      }
    }

    return {
      schedule: results.filter(function(r, i) { return i % 4 === 0; }), // Sample every $2000
      cliffZones: cliffZones,
      maxSafeIncome: maxSafeIncome
    };
  }

  /* ═══════════════════════════════════════════════════════════════════
     EXTENDED: SYSTEM BENCHMARKS DETAIL VIEW
     ═══════════════════════════════════════════════════════════════════ */
  var SYSTEM_BENCHMARKS = {
    medicaid:   { domain: 'health',   label: 'Medicaid',                 annualCost: 12000, coordSavings: 0.35, categories: { general_adult: 5040, disabled: 17424, behavioral_health: 13200, dual_eligible: 24360, pregnant: 10284, child: 3408, foster_child: 9516 } },
    bha:        { domain: 'health',   label: 'Behavioral Health',         annualCost: 18000, coordSavings: 0.45, categories: { outpatient_therapy: 4800, intensive_outpatient: 9600, residential_treatment: 28000, mat_opioid: 7200, crisis_services: 15000, act: 12000 } },
    hie:        { domain: 'health',   label: 'Health Info Exchange',      annualCost:  2000, coordSavings: 0.60 },
    pdmp:       { domain: 'health',   label: 'Prescription Drug Monitor', annualCost:  1500, coordSavings: 0.50 },
    mco:        { domain: 'health',   label: 'Managed Care Org',          annualCost: 14000, coordSavings: 0.30, categories: { general: 5400, behavioral_health: 11800, complex_care: 18500 } },
    va:         { domain: 'health',   label: 'VA Healthcare',             annualCost: 22000, coordSavings: 0.40, categories: { primary_care: 8400, mental_health: 12800, disability_comp: 18600 } },
    er_frequent:{ domain: 'health',   label: 'Frequent ER Use',           annualCost: 28000, coordSavings: 0.65 },
    doc:        { domain: 'justice',  label: 'Dept of Corrections',       annualCost: 15000, coordSavings: 0.50, categories: { state_prison: 45771, county_jail: 34600, juvenile_detention: 62044 } },
    probation:  { domain: 'justice',  label: 'Probation/Parole',          annualCost:  5000, coordSavings: 0.40, categories: { standard: 4200, intensive: 8400, electronic_monitoring: 6800 } },
    court_cms:  { domain: 'justice',  label: 'Court Case Mgmt',           annualCost:  3000, coordSavings: 0.35, categories: { criminal: 3200, family: 2400, juvenile: 4100, drug_court: 5800 } },
    juvenile_court: { domain: 'justice', label: 'Juvenile Court',         annualCost:  8000, coordSavings: 0.45 },
    hmis:       { domain: 'housing',  label: 'Homeless Info System',      annualCost:  8000, coordSavings: 0.55, categories: { emergency_shelter: 25550, transitional: 19200, permanent_supportive: 15642, rapid_rehousing: 9200 } },
    pha:        { domain: 'housing',  label: 'Public Housing Auth',       annualCost:  9600, coordSavings: 0.25, categories: { section_8_voucher: 10800, public_housing: 9200, project_based: 11400 } },
    shelter:    { domain: 'housing',  label: 'Emergency Shelter',         annualCost: 12000, coordSavings: 0.60 },
    tanf:       { domain: 'income',   label: 'TANF',                      annualCost:  7200, coordSavings: 0.30 },
    snap:       { domain: 'income',   label: 'SNAP',                      annualCost:  3600, coordSavings: 0.20 },
    ssi:        { domain: 'income',   label: 'SSI',                       annualCost: 10200, coordSavings: 0.25 },
    ssdi:       { domain: 'income',   label: 'SSDI',                      annualCost: 14400, coordSavings: 0.25 },
    ssa:        { domain: 'income',   label: 'Social Security Admin',     annualCost: 10200, coordSavings: 0.25 },
    unemployment:{ domain: 'income',  label: 'Unemployment Comp',         annualCost:  6000, coordSavings: 0.30 },
    iep:        { domain: 'education',label: 'IEP / Special Ed',          annualCost: 12000, coordSavings: 0.35 },
    slds:       { domain: 'education',label: 'Student Longitudinal Data', annualCost:  1500, coordSavings: 0.50 },
    sacwis:     { domain: 'child_welfare', label: 'Child Welfare Info',   annualCost: 18000, coordSavings: 0.45, categories: { investigation: 8500, foster_care: 32000, kinship_care: 18000, adoption_subsidy: 12000, family_preservation: 6500 } },
    foster_care:{ domain: 'child_welfare', label: 'Foster Care',          annualCost: 22000, coordSavings: 0.40 }
  };

  // Avoidable event costs (from cost_engine.py)
  var AVOIDABLE_EVENTS = [
    { event: 'Emergency room visit', cost: 2580, unit: 'per visit', source: 'HCUP Statistical Brief #268' },
    { event: 'Inpatient psychiatric stay', cost: 1950, unit: 'per day', source: 'HCUP Statistical Brief #249' },
    { event: 'Jail booking', cost: 150, unit: 'per day', source: 'Vera Institute' },
    { event: 'Shelter night', cost: 68, unit: 'per night', source: 'HUD AHAR 2023' }
  ];

  // Coordination savings by domain (from cost_calculator.py)
  var COORDINATION_SAVINGS = {
    health:       { factor: 0.62, source: 'SAMHSA, Evidence for Integrated Care Models' },
    housing:      { factor: 0.65, source: 'HUD, Housing First Evidence Base' },
    justice:      { factor: 0.68, source: 'RAND Corporation, Recidivism Reduction' },
    income:       { factor: 0.45, source: 'Mathematica, Benefits Coordination Pilot' },
    child_welfare:{ factor: 0.50, source: 'Casey Family Programs, Systems of Care' },
    education:    { factor: 0.35, source: 'MDRC, Integrated Student Support' }
  };

  // Cross-reference display data (from cross_reference.py)
  var STATUTE_TO_REG = [
    { statute: '42 U.S.C. § 1396', regs: ['42 CFR § 438', '42 CFR § 440', '42 CFR § 441'], rel: 'implements' },
    { statute: '42 U.S.C. § 1396a', regs: ['42 CFR § 438', '42 CFR § 440'], rel: 'implements' },
    { statute: '29 U.S.C. § 1185a', regs: ['45 CFR § 146', '29 CFR § 2590'], rel: 'implements' },
    { statute: '42 U.S.C. § 1395dd', regs: ['42 CFR § 489'], rel: 'implements' },
    { statute: '42 U.S.C. § 12132', regs: ['28 CFR § 35'], rel: 'implements' },
    { statute: '42 U.S.C. § 12182', regs: ['28 CFR § 36'], rel: 'implements' },
    { statute: '29 U.S.C. § 794', regs: ['34 CFR § 104'], rel: 'implements' },
    { statute: '42 U.S.C. § 3604', regs: ['24 CFR § 100'], rel: 'implements' },
    { statute: '20 U.S.C. § 1400', regs: ['34 CFR § 300'], rel: 'implements' },
    { statute: '7 U.S.C. § 2011', regs: ['7 CFR § 273'], rel: 'implements' }
  ];

  // Extended profile rendering functions
  function renderProfileCostBreakdown(profileKey) {
    var pd = profileDomains[profileKey];
    if (!pd) return '';
    var html = '<div class="duomo-subsection">';
    html += '<h4 style="color:' + IVORY + ';">Detailed System Benchmark Costs</h4>';
    html += '<table class="duomo-table"><thead><tr><th>System</th><th>Domain</th><th>Annual Cost</th><th>Coordination Savings %</th><th>Coordinated Cost</th></tr></thead><tbody>';
    pd.domains.forEach(function(d) {
      d.systems.forEach(function(s) {
        var bench = SYSTEM_BENCHMARKS[s.id];
        if (!bench) return;
        var coordCost = Math.round(bench.annualCost * (1 - bench.coordSavings));
        html += '<tr>';
        html += '<td style="color:' + IVORY + ';">' + bench.label + '</td>';
        html += '<td>' + bench.domain + '</td>';
        html += '<td>' + fmtFull(bench.annualCost) + '</td>';
        html += '<td>' + Math.round(bench.coordSavings * 100) + '%</td>';
        html += '<td style="color:#4CAF50;">' + fmtFull(coordCost) + '</td>';
        html += '</tr>';
        if (bench.categories) {
          for (var cat in bench.categories) {
            html += '<tr style="font-size:11px;">';
            html += '<td style="padding-left:24px;color:' + IVORY_FAINT + ';">' + cat.replace(/_/g, ' ') + '</td>';
            html += '<td></td>';
            html += '<td style="color:' + IVORY_FAINT + ';">' + fmtFull(bench.categories[cat]) + '</td>';
            html += '<td></td><td></td></tr>';
          }
        }
      });
    });
    html += '</tbody></table></div>';
    return html;
  }

  function renderCliffGuardChart(profileKey, container) {
    var guard = calculateCliffGuard(profileKey);
    if (!guard || !guard.schedule || guard.schedule.length === 0) return;

    var chartWrap = el('div', 'duomo-chart-container');
    chartWrap.style.height = '280px';
    var canvas = document.createElement('canvas');
    chartWrap.appendChild(canvas);
    container.appendChild(chartWrap);

    var infoDiv = el('div', '');
    infoDiv.innerHTML = '<p style="font-size:12px;color:' + IVORY_MUTED + ';margin-top:8px;">Cliff Zones (EMTR > 50%): ' +
      (guard.cliffZones.length > 0 ? guard.cliffZones.map(function(z) { return fmtFull(z); }).join(', ') : 'None detected') +
      ' | Max Safe Income: <strong style="color:' + GOLD + ';">' + fmtFull(guard.maxSafeIncome) + '</strong></p>';
    container.appendChild(infoDiv);

    setTimeout(function() {
      if (typeof Chart === 'undefined') return;
      var labels = guard.schedule.map(function(r) { return fmt(r.income); });
      var benefitData = guard.schedule.map(function(r) { return r.benefits; });
      var totalData = guard.schedule.map(function(r) { return r.totalResources; });
      var emtrData = guard.schedule.map(function(r) { return r.emtr * 100; });

      chartInstances['cliffGuard_' + profileKey] = new Chart(canvas, {
        type: 'line',
        data: {
          labels: labels,
          datasets: [
            { label: 'Total Resources', data: totalData, borderColor: GOLD, backgroundColor: 'rgba(201,168,76,0.1)', fill: true, tension: 0.3, pointRadius: 0 },
            { label: 'Benefits Only', data: benefitData, borderColor: '#4CAF50', backgroundColor: 'rgba(76,175,80,0.1)', fill: true, tension: 0.3, pointRadius: 0 },
            { label: 'EMTR %', data: emtrData, borderColor: '#f44336', borderDash: [4, 4], tension: 0.3, pointRadius: 0, yAxisID: 'y1' }
          ]
        },
        options: {
          responsive: true, maintainAspectRatio: false,
          plugins: { legend: { labels: { color: IVORY_MUTED, font: { size: 10 } } }, title: { display: true, text: 'Benefits Cliff Analysis — ' + profiles[profileKey].name, color: GOLD, font: { size: 13, family: 'Georgia,serif' } } },
          scales: {
            x: { ticks: { color: IVORY_MUTED, font: { size: 9 }, maxTicksLimit: 12 }, grid: { color: 'rgba(201,168,76,0.06)' } },
            y: { ticks: { color: IVORY_MUTED, font: { size: 9 }, callback: function(v) { return fmt(v); } }, grid: { color: 'rgba(201,168,76,0.06)' } },
            y1: { position: 'right', min: 0, max: 120, ticks: { color: '#f44336', font: { size: 9 }, callback: function(v) { return v + '%'; } }, grid: { display: false } }
          }
        }
      });
    }, 50);
  }

  function renderCapitalMarkets(ct) {
    var allKeys = ['marcus', 'sarah', 'james', 'maria', 'robert'];
    var pool = poolContracts(allKeys, 'mezzanine');
    var pricing = priceBond(allKeys, 0.05);
    var stress = stressTest(allKeys);

    var section = el('div', 'duomo-subsection');
    section.innerHTML = '<h3 style="color:' + GOLD + ';font-family:Georgia,serif;">Prevention-Backed Securities</h3>';
    section.innerHTML += '<p style="color:' + IVORY_MUTED + ';">Pooled settlement contracts from all 5 profiles. PAYOUT_RATIO = 0.70. Tranche: mezzanine.</p>';

    // Bond stats
    section.innerHTML += '<div class="duomo-stats-row">' +
      '<div class="duomo-stat"><div class="val">' + fmtFull(pool.totalNotional) + '</div><div class="lbl">Total Notional</div></div>' +
      '<div class="duomo-stat"><div class="val">' + (pool.couponRate * 100).toFixed(1) + '%</div><div class="lbl">Coupon Rate</div></div>' +
      '<div class="duomo-stat"><div class="val">' + (pool.expectedYield * 100).toFixed(1) + '%</div><div class="lbl">Expected Yield</div></div>' +
      '<div class="duomo-stat"><div class="val">' + fmtFull(pricing.expectedCashFlow) + '</div><div class="lbl">Expected Cash Flow</div></div>' +
      '<div class="duomo-stat"><div class="val">' + fmtFull(pricing.var95) + '</div><div class="lbl">VaR (95%)</div></div>' +
      '<div class="duomo-stat"><div class="val">' + (pricing.defaultProbability * 100).toFixed(2) + '%</div><div class="lbl">Default Prob</div></div>' +
      '</div>';

    // Settlement contracts table
    section.innerHTML += '<h4 style="color:' + IVORY + ';margin-top:20px;">Settlement Contracts</h4>';
    section.innerHTML += '<table class="duomo-table"><thead><tr><th>Profile</th><th>Intervention</th><th>Expected Savings</th><th>Prob of Success</th><th>Term</th></tr></thead><tbody>';
    allKeys.forEach(function(k) {
      var sc = settlementContracts[k];
      var totalSav = 0;
      for (var payer in sc.expectedSavings) totalSav += sc.expectedSavings[payer];
      section.innerHTML += '<tr><td style="color:' + IVORY + ';">' + profiles[k].name + '</td>' +
        '<td>' + sc.interventionType + '</td>' +
        '<td>' + fmtFull(totalSav) + '</td>' +
        '<td>' + (sc.probabilityOfSuccess * 100) + '%</td>' +
        '<td>' + sc.termYears + ' years</td></tr>';
    });
    section.innerHTML += '</tbody></table>';

    // Stress test
    section.innerHTML += '<h4 style="color:' + IVORY + ';margin-top:20px;">Stress Test Results</h4>';
    section.innerHTML += '<div style="display:flex;gap:16px;flex-wrap:wrap;">';
    for (var scenario in stress) {
      var drop = DEFAULT_SCENARIOS[scenario];
      var color = scenario === 'baseline' ? '#4CAF50' : scenario === 'moderate' ? GOLD : '#f44336';
      section.innerHTML += '<div class="duomo-card" style="flex:1;min-width:160px;text-align:center;padding:16px;">' +
        '<div style="font-size:11px;color:' + IVORY_MUTED + ';text-transform:uppercase;letter-spacing:1px;">' + scenario + '</div>' +
        '<div style="font-size:10px;color:' + IVORY_FAINT + ';margin:4px 0;">Success rates -' + (drop * 100) + '%</div>' +
        '<div style="font-size:22px;font-family:Georgia,serif;color:' + color + ';">' + fmtFull(stress[scenario]) + '</div>' +
        '<div style="font-size:10px;color:' + IVORY_FAINT + ';">Annual expected CF</div></div>';
    }
    section.innerHTML += '</div>';

    // Tranche comparison
    section.innerHTML += '<h4 style="color:' + IVORY + ';margin-top:20px;">Tranche Comparison</h4>';
    section.innerHTML += '<table class="duomo-table"><thead><tr><th>Tranche</th><th>Yield Mult</th><th>Risk Mult</th><th>Coupon Rate</th><th>Total Notional</th></tr></thead><tbody>';
    ['senior', 'mezzanine', 'equity'].forEach(function(tr) {
      var p = poolContracts(allKeys, tr);
      section.innerHTML += '<tr><td style="color:' + IVORY + ';text-transform:capitalize;">' + tr + '</td>' +
        '<td>' + TRANCHE_YIELD_MULT[tr] + 'x</td>' +
        '<td>' + TRANCHE_RISK_MULT[tr] + 'x</td>' +
        '<td>' + (p.couponRate * 100).toFixed(2) + '%</td>' +
        '<td>' + fmtFull(p.totalNotional) + '</td></tr>';
    });
    section.innerHTML += '</tbody></table>';

    return section;
  }

  /* ═══════════════════════════════════════════════════════════════════
     EXTENDED: COSM SCORING VISUALIZATION
     ═══════════════════════════════════════════════════════════════════ */
  var COSM_DIMENSIONS = [
    { key: 'rights', label: 'Rights', formula: 'provisions × 4.0 (max 100)', desc: 'Legal landscape — rights acquisition and mapping' },
    { key: 'research', label: 'Research', formula: '(active_links / total_links) × 120 (max 100)', desc: 'Data systems — market research completeness' },
    { key: 'budget', label: 'Budget', formula: 'cost_points × 2.5 (max 100)', desc: 'Cost landscape — fiscal model precision' },
    { key: 'package', label: 'Package', formula: 'crew_count × 15 + best_savings_pct (max 100)', desc: 'Coordination architecture — service package design' },
    { key: 'deliverables', label: 'Deliverables', formula: 'flourishing_score × 100', desc: 'Flourishing outcomes — domain completion' },
    { key: 'pitch', label: 'Pitch', formula: 'narrative_sections × 15 + ip_count × 5 (max 100)', desc: 'Narrative — stakeholder pitch strength' }
  ];

  // Simulated COSM scores per profile
  var profileCosmScores = {
    marcus: { rights: 72, research: 85, budget: 68, package: 78, deliverables: 45, pitch: 62 },
    sarah:  { rights: 65, research: 70, budget: 72, package: 65, deliverables: 50, pitch: 58 },
    james:  { rights: 78, research: 80, budget: 75, package: 72, deliverables: 55, pitch: 70 },
    maria:  { rights: 55, research: 60, budget: 58, package: 50, deliverables: 40, pitch: 45 },
    robert: { rights: 85, research: 90, budget: 82, package: 88, deliverables: 30, pitch: 75 }
  };

  function getCosmTotal(scores) {
    var vals = Object.values(scores);
    return Math.min.apply(null, vals);
  }

  /* ═══════════════════════════════════════════════════════════════════
     EXTENDED: DOCUMENTED CASES / RESEARCH CITATIONS
     ═══════════════════════════════════════════════════════════════════ */
  var documentedCases = [
    { id: 'propublica-er-2017', source: 'ProPublica', domain: 'health', finding: 'Frequent ED users average 6-12 visits/yr at $2,500+ each; 42 CFR Part 2 blocks ER from seeing SUD records', year: 2017 },
    { id: 'gao-medicaid-2019', source: 'GAO', domain: 'health', finding: '42 CFR Part 2 cited as primary barrier in 34 states; 23% duplicated services', year: 2019 },
    { id: 'marshall-jail-mh-2021', source: 'Marshall Project', domain: 'justice', finding: 'Average 3-week gap in psychiatric medication continuity at booking; Medicaid terminates at incarceration', year: 2021 },
    { id: 'hud-homelessness-2023', source: 'HUD', domain: 'housing', finding: 'Chronically homeless cost $35,578/yr in emergency services; Housing First reduces costs 49%', year: 2023 },
    { id: 'urban-inst-2020', source: 'Urban Institute', domain: 'housing', finding: '2-year housing waitlist while accumulating $50,000+ in avoidable emergency costs', year: 2020 },
    { id: 'casey-foster-2018', source: 'Casey Family Programs', domain: 'child_welfare', finding: 'Foster children change schools 1.6x/yr; 4-6 months academic progress lost per move; only 3% share data with CW', year: 2018 },
    { id: 'chapin-hall-2017', source: 'Chapin Hall', domain: 'child_welfare', finding: 'Crossover youth in avg 3.2 systems; retell trauma to avg 8 professionals; $85,000/yr cost', year: 2017 },
    { id: 'vera-reentry-2020', source: 'Vera Institute', domain: 'justice', finding: '$150/day jail; 3x recidivism without coordinated reentry; 45-day Medicaid re-enrollment gap', year: 2020 }
  ];

  // Job openings registry (from seed_scenarios.py)
  var jobOpenings = [
    { id: 'job-cdl-b', title: 'Delivery Driver', employer: 'UPS Supply Chain', wage: 26, annual: 54080, credential: 'CDL-B' },
    { id: 'job-warehouse', title: 'Warehouse Associate', employer: 'Amazon PHL1', wage: 18, annual: 37440, credential: 'Forklift cert' },
    { id: 'job-med-coder', title: 'Medical Coding Specialist', employer: 'Jefferson Health', wage: 22, annual: 45760, credential: 'CompTIA A+' },
    { id: 'job-peer-recovery', title: 'Peer Recovery Specialist', employer: 'DBHIDS Philadelphia', wage: 18, annual: 37440, credential: 'CNA' },
    { id: 'job-food-service', title: 'Food Service Worker', employer: 'Aramark', wage: 15, annual: 31200, credential: 'ServSafe' },
    { id: 'job-phlebotomist', title: 'Phlebotomist', employer: 'LabCorp Philadelphia', wage: 19, annual: 39520, credential: 'Phlebotomy cert' }
  ];

  /* ═══════════════════════════════════════════════════════════════════
     EXTENDED: COORDINATION MODEL SCORING ENGINE
     ═══════════════════════════════════════════════════════════════════ */
  var COORD_DOMAIN_WEIGHTS = {
    health: 1.0, behavioral_health: 0.9, housing: 0.8, income: 0.7,
    education: 0.7, child_welfare: 0.8, justice: 0.7, social_support: 0.6, immigration: 0.5
  };

  var POLITICAL_SCORES = { high: 1.0, moderate: 0.7, low: 0.4, contentious: 0.2 };

  var BUDGET_BREAKDOWN = {
    personnel: 0.45, technology: 0.15, operations: 0.12,
    provider_payments: 0.15, administration: 0.08, contingency: 0.05
  };

  var coordinationModelsExtended = [
    { id: 1, abbrev: 'ACO', name: 'Accountable Care Organization', category: 'managed_care', budget: '$5M-$500M/yr', timeline: '12-18 months', evidence: 'strong', political: 'moderate', domainsCovered: ['health', 'behavioral_health'] },
    { id: 2, abbrev: 'Health Home', name: 'Health Home', category: 'managed_care', budget: '$1M-$50M/yr', timeline: '9-15 months', evidence: 'moderate', political: 'high', domainsCovered: ['health', 'behavioral_health', 'housing'] },
    { id: 3, abbrev: 'PACE', name: 'Program of All-Inclusive Care for the Elderly', category: 'managed_care', budget: '$3M-$80M/yr', timeline: '18-36 months', evidence: 'strong', political: 'moderate', domainsCovered: ['health', 'housing', 'social_support'] },
    { id: 4, abbrev: 'WRAP', name: 'Wraparound/WRAP', category: 'community_based', budget: '$500K-$20M/yr', timeline: '6-12 months', evidence: 'strong', political: 'high', domainsCovered: ['child_welfare', 'education', 'behavioral_health', 'justice'] },
    { id: 5, abbrev: 'CCR', name: 'Coordinated Care Resource', category: 'community_based', budget: '$200K-$5M/yr', timeline: '3-6 months', evidence: 'moderate', political: 'high', domainsCovered: ['health', 'housing', 'income'] },
    { id: 6, abbrev: 'MCO', name: 'Managed Care Organization', category: 'managed_care', budget: '$50M-$5B/yr', timeline: '18-24 months', evidence: 'strong', political: 'moderate', domainsCovered: ['health', 'behavioral_health'] },
    { id: 7, abbrev: 'CHW Hub', name: 'Community Health Worker Hub', category: 'community_based', budget: '$300K-$8M/yr', timeline: '3-6 months', evidence: 'moderate', political: 'high', domainsCovered: ['health', 'housing', 'income', 'social_support'] },
    { id: 8, abbrev: 'SIB', name: 'Social Impact Bond', category: 'specialized', budget: '$2M-$50M/project', timeline: '12-24 months', evidence: 'emerging', political: 'low', domainsCovered: ['justice', 'housing', 'health'] },
    { id: 9, abbrev: 'DSNP+', name: 'Dual Special Needs Plan (enhanced)', category: 'managed_care', budget: '$20M-$2B/yr', timeline: '18-24 months', evidence: 'moderate', political: 'moderate', domainsCovered: ['health', 'housing', 'income'] },
    { id: 10, abbrev: 'CDIH', name: 'Cross-System Data Integration Hub', category: 'hybrid', budget: '$1M-$30M/yr', timeline: '12-24 months', evidence: 'emerging', political: 'low', domainsCovered: ['health', 'housing', 'income', 'education', 'justice', 'child_welfare'] }
  ];

  function scoreCoordinationModel(model, targetDomains) {
    var modelDims = model.domainsCovered;
    var overlap = 0;
    targetDomains.forEach(function(td) {
      if (modelDims.indexOf(td) >= 0) overlap++;
    });
    var overlapScore = targetDomains.length > 0 ? overlap / targetDomains.length : 0;
    var politicalScore = POLITICAL_SCORES[model.political] || 0.5;
    var evidenceScore = model.evidence === 'strong' ? 1.0 : model.evidence === 'moderate' ? 0.7 : 0.4;
    var composite = overlapScore * 0.4 + politicalScore * 0.2 + evidenceScore * 0.4;
    return Math.round(composite * 100) / 100;
  }

  /* ═══════════════════════════════════════════════════════════════════
     EXTENDED: OVERRIDE PROFILE EXPLORER WITH MORE DETAIL
     ═══════════════════════════════════════════════════════════════════ */

  // Override renderProfiles to include more sections
  var originalRenderProfiles = renderProfiles;
  renderProfiles = function(ct) {
    // Call original
    originalRenderProfiles(ct);

    var pk = currentProfile;
    var p = profiles[pk];

    // Capital Markets section
    var capSection = el('div', 'duomo-card duomo-animate');
    capSection.style.animationDelay = '0.4s';
    capSection.innerHTML = '<h3>Capital Markets — Settlement Contract</h3>';
    var sc = settlementContracts[pk];
    if (sc) {
      capSection.innerHTML += '<p><strong>Intervention:</strong> ' + sc.interventionType + '</p>';
      capSection.innerHTML += '<p><strong>Probability of Success:</strong> ' + (sc.probabilityOfSuccess * 100) + '%</p>';
      capSection.innerHTML += '<p><strong>Verification:</strong> ' + sc.verificationMethod + '</p>';
      capSection.innerHTML += '<p><strong>Term:</strong> ' + sc.termYears + ' years</p>';
      capSection.innerHTML += '<h4 style="margin-top:12px;">Expected Savings by Payer</h4>';
      capSection.innerHTML += '<div style="display:flex;gap:8px;flex-wrap:wrap;">';
      for (var payer in sc.expectedSavings) {
        capSection.innerHTML += '<div class="duomo-card" style="padding:12px;min-width:120px;text-align:center;">' +
          '<div style="font-size:10px;color:' + IVORY_MUTED + ';text-transform:uppercase;">' + payer.replace(/_/g, ' ') + '</div>' +
          '<div style="font-size:18px;color:' + GOLD + ';font-family:Georgia,serif;">' + fmtFull(sc.expectedSavings[payer]) + '</div></div>';
      }
      capSection.innerHTML += '</div>';
    }
    ct.appendChild(capSection);

    // Cliff Guard section
    var cliffSection = el('div', 'duomo-card duomo-animate');
    cliffSection.style.animationDelay = '0.5s';
    cliffSection.innerHTML = '<h3>Benefits Cliff Analysis</h3>';
    cliffSection.innerHTML += '<p style="color:' + IVORY_MUTED + ';">Simulates income from current up to 3× or $150K in $500 steps. EMTR > 50% = cliff zone.</p>';
    renderCliffGuardChart(pk, cliffSection);
    ct.appendChild(cliffSection);

    // COSM Score section
    var cosmSection = el('div', 'duomo-card duomo-animate');
    cosmSection.style.animationDelay = '0.6s';
    var cosm = profileCosmScores[pk];
    if (cosm) {
      var total = getCosmTotal(cosm);
      cosmSection.innerHTML = '<h3>COSM Dimensions</h3>';
      cosmSection.innerHTML += '<p style="color:' + IVORY_MUTED + ';">Weakest-link principle: total = min(all dimensions) = <strong style="color:' + GOLD + ';">' + total + '</strong></p>';
      var cosmChartWrap = el('div', 'duomo-chart-container');
      cosmChartWrap.style.height = '250px';
      var cosmCanvas = document.createElement('canvas');
      cosmChartWrap.appendChild(cosmCanvas);
      cosmSection.appendChild(cosmChartWrap);
      ct.appendChild(cosmSection);

      setTimeout(function() {
        if (typeof Chart === 'undefined') return;
        chartInstances['cosm_' + pk] = new Chart(cosmCanvas, {
          type: 'radar',
          data: {
            labels: COSM_DIMENSIONS.map(function(d) { return d.label; }),
            datasets: [{
              label: 'COSM Score',
              data: COSM_DIMENSIONS.map(function(d) { return cosm[d.key]; }),
              backgroundColor: 'rgba(201,168,76,0.15)',
              borderColor: GOLD,
              borderWidth: 2,
              pointBackgroundColor: GOLD,
              pointRadius: 4
            }]
          },
          options: {
            responsive: true, maintainAspectRatio: false,
            scales: { r: { min: 0, max: 100, ticks: { color: IVORY_MUTED, backdropColor: 'transparent' }, grid: { color: 'rgba(201,168,76,0.1)' }, pointLabels: { color: IVORY_MUTED, font: { size: 11 } } } },
            plugins: { legend: { display: false } }
          }
        });
      }, 100);
    }

    // Job matches section
    var jobSection = el('div', 'duomo-card duomo-animate');
    jobSection.style.animationDelay = '0.7s';
    jobSection.innerHTML = '<h3>Labor Market — Job Matches</h3>';
    jobSection.innerHTML += '<table class="duomo-table"><thead><tr><th>Title</th><th>Employer</th><th>Wage</th><th>Annual</th><th>Credential</th></tr></thead><tbody>';
    jobOpenings.forEach(function(j) {
      jobSection.innerHTML += '<tr><td style="color:' + IVORY + ';">' + j.title + '</td><td>' + j.employer + '</td><td>$' + j.wage + '/hr</td><td>' + fmtFull(j.annual) + '</td><td><span class="duomo-tag">' + j.credential + '</span></td></tr>';
    });
    jobSection.innerHTML += '</tbody></table>';
    ct.appendChild(jobSection);

    // Research citations
    var citeSection = el('div', 'duomo-card duomo-animate');
    citeSection.style.animationDelay = '0.8s';
    citeSection.innerHTML = '<h3>Research Citations</h3>';
    documentedCases.forEach(function(dc) {
      citeSection.innerHTML += '<div style="padding:8px 0;border-bottom:1px solid rgba(201,168,76,0.06);">' +
        '<div style="display:flex;gap:12px;align-items:baseline;"><span class="duomo-tag">' + dc.source + '</span><span style="color:' + IVORY_FAINT + ';font-size:11px;">' + dc.year + ' &middot; ' + dc.domain + '</span></div>' +
        '<p style="margin:4px 0;font-size:12px;">' + dc.finding + '</p></div>';
    });
    ct.appendChild(citeSection);
  };

  /* ═══════════════════════════════════════════════════════════════════
     EXTENDED: OVERRIDE MATCHER WITH CROSS-REFERENCE DISPLAY
     ═══════════════════════════════════════════════════════════════════ */
  var originalRenderMatcher = renderMatcher;
  renderMatcher = function(ct) {
    originalRenderMatcher(ct);

    // Cross-reference display
    var xrefCard = el('div', 'duomo-card duomo-animate');
    xrefCard.style.animationDelay = '0.3s';
    xrefCard.innerHTML = '<h3>Statute-to-Regulation Cross-References</h3>';
    xrefCard.innerHTML += '<p style="color:' + IVORY_MUTED + ';">From cross_reference.py — 10 statute-regulation mappings.</p>';
    xrefCard.innerHTML += '<table class="duomo-table"><thead><tr><th>Statute</th><th>Implementing Regulations</th><th>Relationship</th></tr></thead><tbody>';
    STATUTE_TO_REG.forEach(function(sr) {
      xrefCard.innerHTML += '<tr><td style="color:' + IVORY + ';">' + sr.statute + '</td>' +
        '<td>' + sr.regs.join(', ') + '</td>' +
        '<td><span class="duomo-tag">' + sr.rel + '</span></td></tr>';
    });
    xrefCard.innerHTML += '</tbody></table>';
    ct.appendChild(xrefCard);

    // Avoidable events
    var avoidCard = el('div', 'duomo-card duomo-animate');
    avoidCard.style.animationDelay = '0.4s';
    avoidCard.innerHTML = '<h3>Avoidable Event Costs</h3>';
    avoidCard.innerHTML += '<p style="color:' + IVORY_MUTED + ';">Preventable fraction: 50% of estimated frequency × cost.</p>';
    avoidCard.innerHTML += '<table class="duomo-table"><thead><tr><th>Event</th><th>Cost</th><th>Unit</th><th>Source</th></tr></thead><tbody>';
    AVOIDABLE_EVENTS.forEach(function(ae) {
      avoidCard.innerHTML += '<tr><td style="color:' + IVORY + ';">' + ae.event + '</td><td style="color:' + GOLD + ';">' + fmtFull(ae.cost) + '</td><td>' + ae.unit + '</td><td style="font-size:11px;">' + ae.source + '</td></tr>';
    });
    avoidCard.innerHTML += '</tbody></table>';
    ct.appendChild(avoidCard);

    // Coordination savings reference
    var coordCard = el('div', 'duomo-card duomo-animate');
    coordCard.style.animationDelay = '0.5s';
    coordCard.innerHTML = '<h3>Coordination Savings by Domain</h3>';
    coordCard.innerHTML += '<table class="duomo-table"><thead><tr><th>Domain</th><th>Savings Factor</th><th>Source</th></tr></thead><tbody>';
    for (var dom in COORDINATION_SAVINGS) {
      var cs = COORDINATION_SAVINGS[dom];
      coordCard.innerHTML += '<tr><td style="color:' + IVORY + ';text-transform:capitalize;">' + dom.replace(/_/g, ' ') + '</td><td style="color:#4CAF50;">' + Math.round(cs.factor * 100) + '%</td><td style="font-size:11px;">' + cs.source + '</td></tr>';
    }
    coordCard.innerHTML += '</tbody></table>';
    ct.appendChild(coordCard);
  };

  /* ═══════════════════════════════════════════════════════════════════
     EXTENDED: OVERRIDE PIPELINE WITH COORDINATION MODELS
     ═══════════════════════════════════════════════════════════════════ */
  var originalRenderPipeline = renderPipeline;
  renderPipeline = function(ct) {
    originalRenderPipeline(ct);

    // Coordination models comparison
    var modelsCard = el('div', 'duomo-card duomo-animate');
    modelsCard.style.animationDelay = '0.6s';
    modelsCard.innerHTML = '<h3>Coordination Models (10)</h3>';
    modelsCard.innerHTML += '<p style="color:' + IVORY_MUTED + ';">Scored against ' + profiles[currentProfile].name + "'s domains.</p>";

    var targetDomains = (profileDomains[currentProfile] && profileDomains[currentProfile].domains) ?
      profileDomains[currentProfile].domains.map(function(d) { return d.domain; }) : ['health'];

    modelsCard.innerHTML += '<table class="duomo-table"><thead><tr><th>Model</th><th>Category</th><th>Evidence</th><th>Budget</th><th>Timeline</th><th>Fit Score</th></tr></thead><tbody>';
    var scored = coordinationModelsExtended.map(function(m) {
      return { model: m, score: scoreCoordinationModel(m, targetDomains) };
    }).sort(function(a, b) { return b.score - a.score; });

    scored.forEach(function(item) {
      var m = item.model;
      var scoreColor = item.score >= 0.7 ? '#4CAF50' : item.score >= 0.5 ? GOLD : '#FF9800';
      modelsCard.innerHTML += '<tr><td style="color:' + IVORY + ';">' + m.abbrev + ' — ' + m.name + '</td>' +
        '<td>' + m.category.replace(/_/g, ' ') + '</td>' +
        '<td>' + m.evidence + '</td>' +
        '<td style="font-size:11px;">' + m.budget + '</td>' +
        '<td>' + m.timeline + '</td>' +
        '<td style="color:' + scoreColor + ';font-weight:700;">' + item.score + '</td></tr>';
    });
    modelsCard.innerHTML += '</tbody></table>';
    ct.appendChild(modelsCard);

    // Budget breakdown reference
    var budgetCard = el('div', 'duomo-card duomo-animate');
    budgetCard.style.animationDelay = '0.7s';
    budgetCard.innerHTML = '<h3>Standard Budget Breakdown</h3>';
    budgetCard.innerHTML += '<div style="display:flex;gap:12px;flex-wrap:wrap;">';
    for (var cat in BUDGET_BREAKDOWN) {
      budgetCard.innerHTML += '<div class="duomo-card" style="padding:12px;text-align:center;min-width:120px;">' +
        '<div style="font-size:24px;font-family:Georgia,serif;color:' + GOLD + ';">' + Math.round(BUDGET_BREAKDOWN[cat] * 100) + '%</div>' +
        '<div style="font-size:10px;color:' + IVORY_MUTED + ';text-transform:capitalize;">' + cat.replace(/_/g, ' ') + '</div></div>';
    }
    budgetCard.innerHTML += '</div>';
    ct.appendChild(budgetCard);

    // Full bond pricing section
    var bondSection = renderCapitalMarkets(ct);
    ct.appendChild(bondSection);
  };

  /* ═══════════════════════════════════════════════════════════════════
     THE APOLLO SLATE — DUOMO
     "The Uploaded Connectome"
     ═══════════════════════════════════════════════════════════════════ */
  function renderDuomoSlate(ct) {
    if (!window.renderStripboard) {
      ct.innerHTML = '<p style="color:#c9a84c;">Stripboard engine loading…</p>';
      return;
    }
    window.renderStripboard(ct, {
      title: 'DUOMO Slate: The First 10 Connectomes',
      themeColor: '#34d399',
      budgetColor: '#c9a84c',
      thesis: 'Constructing and financing the first 10 whole-person digital twins. We use prestige television production budgets to fund military-grade wearable deployments for the most vulnerable. The IP yielded is algorithmic stabilization protocols that scale infinitely.',
      quote: 'A fly has been uploaded. Science has simulated a complete biological neural connectome. \u2014 Marginal Revolution (Mar 2026)',
      manifesto: 'We are crossing the threshold from measuring biology to simulating it. DUOMO equips the marginalized with continuous wearables tethered to Personal Openclaws (local, sovereign AI agents). We are mapping the connectome of human resilience under systemic trauma.',
      columns: [
        {
          id: 'DUOMO #001', title: 'Marcus T.',
          budget: 'Prod Budget: $1.2M | Yield: Algorithmic Reentry',
          thesis: 'Algorithmic stabilization for dual-diagnosis reentry via continuous biometric tracking.',
          events: [
            { time: 'MO 01', title: 'The Biological Upload', desc: 'Oura, CGM, and Cortisol patch deployed. Linked to local Openclaw agent. Baseline connectome mapping begins.', tags: [{ label: 'FRONTIER BIO', color: '#34d399' }] },
            { time: 'MO 03', title: 'Openclaw Intervention', desc: 'Local agent detects 3am cortisol spikes predicting a systemic crisis. Preemptively routes resources.', tags: [{ label: 'AI ORCHESTRATION', color: '#c9a84c' }] },
            { time: 'MO 06', title: 'Wrong-Pocket Recoup', desc: '$53,200 in ER/Justice costs mathematically avoided. DomeBond priced.', tags: [{ label: 'CAPITAL MARKETS', color: '#60a5fa' }] },
            { time: 'MO 12', title: 'IP Extraction: The Protocol', desc: 'The specific open-weights algorithm that successfully down-regulated Marcus\u2019s nervous system is licensed to 300+ state facilities.', tags: [{ label: 'CIVILIZATION IP', color: '#a78bfa' }] }
          ]
        },
        {
          id: 'DUOMO #002', title: 'Sarah C.',
          budget: 'Prod Budget: $1.1M | Yield: Instability Predictor',
          thesis: 'Predictive modeling for housing instability via sleep architecture degradation.',
          events: [
            { time: 'MO 01', title: 'Baseline Upload', desc: 'Housing Openclaw deployed. Advanced sleep monitors track fragmentation and REM collapse linked to impending eviction threats.', tags: [{ label: 'FRONTIER BIO', color: '#34d399' }] },
            { time: 'MO 04', title: 'Predictive Deployment', desc: 'Algorithm flags a 94% probability of shelter entry within 14 days based on biological exhaustion markers. Rapid re-housing triggered.', tags: [{ label: 'AI ORCHESTRATION', color: '#c9a84c' }] },
            { time: 'MO 12', title: 'IP Extraction: Early Warning', desc: 'Shifts municipal child-welfare systems from reactive separation to predictive stabilization algorithms.', tags: [{ label: 'CIVILIZATION IP', color: '#a78bfa' }] }
          ]
        }
      ]
    });
  }

  /* ─── initial render ─── */
  renderTab();
};
