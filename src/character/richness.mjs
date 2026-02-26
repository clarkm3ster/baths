/**
 * CHARACTER FRAGMENT — Dome Layer Richness Scorer
 *
 * Scores how much source material exists for each of the 12 dome layers.
 * A character whose housing, health, legal, and economic circumstances
 * are all deeply documented scores higher than one with only housing.
 *
 * This determines prioritization: richest characters get domes first.
 */

import { DOME_LAYERS, CIRCUMSTANCE_TYPES } from './lib.mjs'

// ── Layer evidence keywords ───────────────────────────────────────────────────
// When these words appear in circumstances, narrative_arc, or systems_touched,
// they indicate evidence for specific dome layers.

const LAYER_SIGNALS = {
  1: { // Legal
    circumstances: ['incarcerated', 'formerly_incarcerated', 'on_probation', 'undocumented', 'asylum_seeker', 'detained', 'wrongly_convicted', 'enslaved', 'trafficking', 'child_marriage', 'surveillance'],
    systems: ['courts', 'criminal justice', 'immigration', 'legal aid', 'police', 'prison', 'probation', 'parole', 'public defender', 'family court', 'juvenile justice', 'civil rights', 'custody'],
    keywords: ['arrest', 'trial', 'sentenc', 'law', 'rights', 'legal', 'attorney', 'judge', 'hearing', 'appeal', 'warrant', 'bail', 'plea', 'conviction'],
  },
  2: { // Systems
    circumstances: ['foster_care', 'benefits_cliff'],
    systems: ['social services', 'child welfare', 'case management', 'bureaucracy', 'welfare', 'SSA', 'SNAP', 'WIC', 'Medicaid', 'Section 8', 'disability services', 'unemployment office', 'food stamps'],
    keywords: ['casework', 'application', 'eligib', 'benefit', 'portal', 'form', 'intake', 'waitlist', 'deny', 'approve', 'recertif'],
  },
  3: { // Fiscal
    circumstances: ['poverty', 'deep_poverty', 'working_poor', 'debt', 'benefits_cliff', 'wealth'],
    systems: ['tax', 'IRS', 'EITC', 'payday loans', 'bankruptcy', 'collections', 'credit'],
    keywords: ['income', 'money', 'cost', 'debt', 'pay', 'wage', 'rent', 'bill', 'afford', 'price', 'savings', 'loan', 'credit', 'budget'],
  },
  4: { // Health
    circumstances: ['chronic_illness', 'mental_illness', 'disability', 'addiction', 'terminal_illness', 'uninsured', 'trauma', 'environmental_exposure'],
    systems: ['hospitals', 'clinics', 'mental health', 'rehab', 'pharmacy', 'insurance', 'Medicaid', 'Medicare', 'VA health', 'emergency room', 'therapy'],
    keywords: ['health', 'sick', 'disease', 'doctor', 'medicin', 'hospital', 'diagnos', 'treatment', 'pain', 'mental', 'depress', 'anxiet', 'addict', 'overdose', 'disabl'],
  },
  5: { // Housing
    circumstances: ['homeless', 'evicted', 'displaced', 'housing_insecure', 'institutionalized', 'shelter', 'climate_displaced'],
    systems: ['shelters', 'public housing', 'Section 8', 'HUD', 'landlord-tenant', 'housing authority', 'halfway house', 'group home'],
    keywords: ['hous', 'home', 'rent', 'evict', 'shelter', 'apartment', 'room', 'sleep', 'street', 'tent', 'motel', 'squat', 'displac', 'homeless'],
  },
  6: { // Economic
    circumstances: ['poverty', 'deep_poverty', 'working_poor', 'unemployed', 'debt', 'benefits_cliff', 'child_labor', 'forced_labor'],
    systems: ['employers', 'temp agencies', 'unemployment insurance', 'workforce development', 'TANF', 'job training'],
    keywords: ['work', 'job', 'employ', 'labor', 'career', 'hiring', 'fired', 'wage', 'shift', 'hustle', 'gig', 'factory', 'union'],
  },
  7: { // Education
    circumstances: ['illiterate', 'dropout', 'special_education', 'foster_care'],
    systems: ['schools', 'colleges', 'GED', 'special education', 'tutoring', 'libraries', 'Pell Grant', 'Head Start', 'school lunch'],
    keywords: ['school', 'learn', 'read', 'teach', 'class', 'educat', 'degree', 'college', 'graduat', 'liter', 'student'],
  },
  8: { // Community
    circumstances: ['foster_care', 'domestic_violence', 'single_parent', 'orphan', 'caregiver', 'isolation', 'elderly', 'immigrant', 'refugee', 'indigenous'],
    systems: ['church', 'mosque', 'temple', 'community center', 'neighborhood', 'family', 'social network', 'gang', 'mutual aid'],
    keywords: ['communit', 'neighbor', 'friend', 'family', 'church', 'belong', 'isolat', 'network', 'social', 'connect', 'trust', 'gang', 'crew'],
  },
  9: { // Environment
    circumstances: ['environmental_exposure', 'climate_displaced', 'food_desert'],
    systems: ['EPA', 'water treatment', 'air quality', 'sanitation', 'infrastructure'],
    keywords: ['pollut', 'water', 'air', 'lead', 'toxic', 'contaminat', 'flood', 'climate', 'environment', 'waste', 'smell', 'noise', 'heat'],
  },
  10: { // Autonomy
    circumstances: ['incarcerated', 'detained', 'surveillance', 'forced_labor', 'enslaved', 'trafficking', 'child_marriage', 'institutionalized', 'domestic_violence'],
    systems: [],
    keywords: ['freedom', 'autonomy', 'choice', 'dignity', 'agency', 'control', 'power', 'resist', 'escape', 'surviv', 'self-determin', 'movement'],
  },
  11: { // Creativity
    circumstances: [],
    systems: [],
    keywords: ['art', 'music', 'creat', 'express', 'write', 'sing', 'danc', 'paint', 'cultur', 'identit', 'story', 'tradition', 'ritual', 'craft'],
  },
  12: { // Flourishing
    circumstances: ['terminal_illness', 'grief', 'wrongly_convicted'],
    systems: [],
    keywords: ['flourish', 'purpose', 'meaning', 'hope', 'dream', 'vision', 'future', 'thrive', 'potential', 'transform', 'transcend', 'spirit', 'joy'],
  },
}

// ── Score a single character ──────────────────────────────────────────────────

export function scoreDomeLayerRichness(character) {
  const scores = {}
  const evidence = {}

  for (let layer = 1; layer <= 12; layer++) {
    const signals = LAYER_SIGNALS[layer]
    let score = 0
    const layerEvidence = []

    // Check circumstances (strongest signal — 3 points each)
    if (character.circumstances && signals.circumstances) {
      for (const circ of character.circumstances) {
        if (signals.circumstances.includes(circ)) {
          score += 3
          layerEvidence.push(`circumstance:${circ}`)
        }
      }
    }

    // Check circumstance type definitions that map to this layer
    if (character.circumstances) {
      for (const circ of character.circumstances) {
        const def = CIRCUMSTANCE_TYPES[circ]
        if (def?.layers?.includes(layer) && !signals.circumstances?.includes(circ)) {
          score += 2
          layerEvidence.push(`circumstance-layer:${circ}`)
        }
      }
    }

    // Check systems_touched (2 points each)
    if (character.systems_touched && signals.systems) {
      for (const sys of character.systems_touched) {
        const sysLower = sys.toLowerCase()
        for (const signal of signals.systems) {
          if (sysLower.includes(signal.toLowerCase())) {
            score += 2
            layerEvidence.push(`system:${sys}`)
            break
          }
        }
      }
    }

    // Check narrative_arc and why_this_character_matters for keywords (1 point each, max 5)
    const textFields = [
      character.narrative_arc || '',
      character.why_this_character_matters || '',
    ].join(' ').toLowerCase()

    let keywordHits = 0
    if (signals.keywords) {
      for (const kw of signals.keywords) {
        if (textFields.includes(kw) && keywordHits < 5) {
          score += 1
          keywordHits++
          layerEvidence.push(`keyword:${kw}`)
        }
      }
    }

    // Explicit dome_layer_richness from source data (override)
    if (character.dome_layer_richness?.[layer] !== undefined) {
      const explicit = character.dome_layer_richness[layer]
      score = Math.max(score, explicit)
      if (explicit > 0) layerEvidence.push(`explicit:${explicit}`)
    }

    // Normalize to 0-10
    scores[layer] = Math.min(10, score)
    evidence[layer] = layerEvidence
  }

  // Overall richness = number of layers with score > 0
  const filledLayers = Object.values(scores).filter(s => s > 0).length
  const totalScore = Object.values(scores).reduce((a, b) => a + b, 0)
  const avgScore = filledLayers > 0 ? Math.round((totalScore / filledLayers) * 10) / 10 : 0

  // Dome buildability — minimum of top 9 layers (AI-fillable layers 1-9)
  const aiLayerScores = []
  for (let i = 1; i <= 9; i++) aiLayerScores.push(scores[i])
  const domeMinimum = Math.min(...aiLayerScores)

  return {
    layer_scores: scores,
    layer_evidence: evidence,
    filled_layers: filledLayers,
    total_score: totalScore,
    average_score: avgScore,
    dome_minimum: domeMinimum,
    dome_buildability: filledLayers >= 6 ? 'high' : filledLayers >= 3 ? 'medium' : 'low',
    richest_layers: Object.entries(scores)
      .filter(([, s]) => s > 0)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 5)
      .map(([l, s]) => ({ layer: parseInt(l), name: DOME_LAYERS[l].name, score: s })),
    thinnest_layers: Object.entries(scores)
      .filter(([, s]) => s === 0)
      .map(([l]) => ({ layer: parseInt(l), name: DOME_LAYERS[l].name })),
  }
}

// ── Rank characters by richness ───────────────────────────────────────────────

export function rankByRichness(characters) {
  return characters
    .map(c => ({
      id: c.id || `${c.name}--${c.source_work}`,
      name: c.name,
      source_work: c.source_work,
      real_or_fictional: c.real_or_fictional,
      richness: scoreDomeLayerRichness(c),
    }))
    .sort((a, b) => {
      // Primary: filled layers (more layers = higher priority)
      if (b.richness.filled_layers !== a.richness.filled_layers) {
        return b.richness.filled_layers - a.richness.filled_layers
      }
      // Secondary: total score
      return b.richness.total_score - a.richness.total_score
    })
}
