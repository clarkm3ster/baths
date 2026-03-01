/**
 * ENTITY — Resolution Engine
 *
 * Takes an archetype profile + county + fragments → resolved entity record.
 *
 * One record = one person × one county × one year.
 * The record has every column from the lifecycle CSV schema.
 *
 * This is the core of entity resolution:
 *   fragments (raw aggregate data) + profile (person characteristics)
 *   → resolved individual-level fiscal record
 */

import { emptyRecord, lifeStage, ALL_COLUMNS } from './schema.mjs'
import { loadFragments } from './fragments.mjs'
import taxes from './resolvers/taxes.mjs'
import benefits from './resolvers/benefits.mjs'
import services from './resolvers/services.mjs'
import collective from './resolvers/collective.mjs'

const RESOLVERS = [taxes, benefits, services, collective]

// ── Archetype profiles ───────────────────────────────────────────
// Each archetype is a person with known characteristics.
// Entity resolution maps aggregate data to their specific situation.

export const ARCHETYPES = [
  {
    id: 'marcus', name: 'Marcus', age: 34, income: 28000,
    household: 3, children: 2, filing: 'hoh',
    employed: true, disabled: false, veteran: false,
    homeowner: false, student: false,
    incarcerated: false, onProbation: false, fosterYouth: false,
    description: 'Single dad, two kids, systems-heavy',
  },
  {
    id: 'elena', name: 'Elena', age: 29, income: 22000,
    household: 2, children: 1, filing: 'hoh',
    employed: true, disabled: false, veteran: false,
    homeowner: false, student: false,
    incarcerated: false, onProbation: false, fosterYouth: false,
    description: 'Working poor, one child',
  },
  {
    id: 'james', name: 'James', age: 72, income: 14000,
    household: 1, children: 0, filing: 'single',
    employed: false, disabled: true, veteran: false,
    homeowner: false, student: false,
    incarcerated: false, onProbation: false, fosterYouth: false,
    description: 'Elderly, disabled, fixed income',
  },
  {
    id: 'rivera', name: 'Rivera Family', age: 38, income: 52000,
    household: 5, children: 3, filing: 'mfj',
    employed: true, disabled: false, veteran: false,
    homeowner: false, student: false,
    incarcerated: false, onProbation: false, fosterYouth: false,
    description: 'Working family, benefits cliff',
  },
  {
    id: 'aisha', name: 'Aisha', age: 19, income: 12000,
    household: 1, children: 0, filing: 'single',
    employed: true, disabled: false, veteran: false,
    homeowner: false, student: true,
    incarcerated: false, onProbation: false, fosterYouth: true,
    description: 'Aged out of foster care, part-time student',
  },
  {
    id: 'median', name: 'Median', age: 38, income: 59500,
    household: 2, children: 1, filing: 'mfj',
    employed: true, disabled: false, veteran: false,
    homeowner: true, student: false,
    incarcerated: false, onProbation: false, fosterYouth: false,
    description: 'National benchmark — median household',
  },
]

// ── Counties (same as fragment layer) ────────────────────────────
import { COUNTIES } from '../fragment/lib.mjs'
export { COUNTIES }

// ── Resolve one entity ───────────────────────────────────────────

export function resolveEntity(profile, county, year) {
  const fragments = loadFragments(county.fips)
  const record = emptyRecord()

  // Identity
  record.year = year || new Date().getFullYear()
  record.age = profile.age
  record.life_stage = lifeStage(profile.age)
  record.zip_code = ''  // zip not available from county-level data
  record.city = county.name.split(',')[0].replace(/\s*County.*/, '').replace(/\s*\(.*\)/, '').trim()
  record.county = county.name.split(',')[0].trim()
  record.state = county.name.includes(',')
    ? county.name.split(',').pop().trim()
    : county.state || ''

  // Run each resolver
  for (const resolver of RESOLVERS) {
    const partial = resolver.resolve(profile, county, fragments)
    for (const [key, val] of Object.entries(partial)) {
      if (key in record) {
        record[key] = typeof val === 'number' ? Math.round(val) : val
      }
    }
  }

  // Summary
  record.total_govt_cost = record.total_direct_benefits
    + record.total_direct_services
    + record.total_collective_allocated

  record.net_fiscal_impact = record.total_taxes_fees_paid - record.total_govt_cost
  record.data_source_quality = Object.keys(fragments).length > 10 ? 'estimated' : 'modeled'
  record.notes = `${profile.description}; ${Object.keys(fragments).length} fragments resolved`

  return { record, fragments_used: Object.keys(fragments).length }
}

// ── Resolve all archetypes × counties ────────────────────────────

export function resolveAll(year) {
  const results = []

  for (const county of COUNTIES) {
    for (const archetype of ARCHETYPES) {
      const { record, fragments_used } = resolveEntity(
        { ...archetype, state: extractState(county) },
        { ...county, state: extractState(county) },
        year
      )
      results.push({
        archetype_id: archetype.id,
        fips: county.fips,
        record,
        fragments_used,
      })
    }
  }

  return results
}

function extractState(county) {
  // Get 2-letter state from county name ("Philadelphia, PA" → "PA")
  const match = county.name.match(/,\s*([A-Z]{2})$/)
  if (match) return match[1]
  // DC special case
  if (county.fips === '11001') return 'DC'
  return ''
}
