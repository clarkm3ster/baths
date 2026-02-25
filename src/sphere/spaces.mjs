/**
 * SPHERE FRAGMENT — Space Registry
 *
 * Records for discovered public spaces.
 * Storage: data/sphere-spaces/{state}/{municipality-slug}/{space-id}.json
 *
 * Each space record is raw material for a sphere production.
 * When someone selects a space, the sphere schema (10 layers)
 * reorganizes everything known about it as the gravitational center.
 */

import { join } from 'node:path'
import {
  SPACES_DIR, META_DIR, readJSON, writeJSON, listJSON, listDirs,
  slugify, spaceID
} from './lib.mjs'

// ── Space record schema ─────────────────────────────────────────────────────
//
// {
//   id: string,
//   name: string,
//   type: string (space type slug),
//   type_category: string (discovered category),
//   address: string,
//   lat: number | null,
//   lng: number | null,
//   parcel_id: string | null,
//   municipality: string,
//   municipality_slug: string,
//   county: string | null,
//   state: string (2-letter),
//   owning_entity: string (city|county|school_district|housing_authority|transit_authority|port_authority|state|federal),
//   current_use: string,
//   current_use_hours: string | null,
//   physical: {
//     indoor_outdoor: string (indoor|outdoor|both),
//     approximate_size_sqft: number | null,
//     covered_open: string (covered|open|partial),
//     accessible: boolean | null,
//     level: string (ground|elevated|below_grade|multi),
//     has_water: boolean | null,
//     has_power: boolean | null,
//     has_restrooms: boolean | null,
//     surface_type: string | null,
//   },
//   zoning: string | null,
//   assessed_value: number | null,
//   restrictions: string[],
//   adjacent_context: string | null,
//   condition: string | null (maintained|neglected|abandoned|under_construction),
//   activation_potential: number[] (sphere layers 1-10),
//   data_source_url: string,
//   data_source_name: string,
//   scraped_at: string (ISO),
//   discovery_cycle: number,
// }

export function addSpace(record) {
  const id = record.id || spaceID(record.name || '', record.address || '', record.municipality || '')
  const state = record.state?.toUpperCase() || 'XX'
  const munSlug = slugify(record.municipality || 'unknown')

  const full = {
    id,
    name: record.name || 'Unnamed Space',
    type: record.type || 'unknown',
    type_category: record.type_category || record.type || 'unknown',
    address: record.address || '',
    lat: record.lat || null,
    lng: record.lng || null,
    parcel_id: record.parcel_id || null,

    municipality: record.municipality || '',
    municipality_slug: munSlug,
    county: record.county || null,
    state,

    owning_entity: record.owning_entity || 'city',
    current_use: record.current_use || '',
    current_use_hours: record.current_use_hours || null,

    physical: {
      indoor_outdoor: record.physical?.indoor_outdoor || 'outdoor',
      approximate_size_sqft: record.physical?.approximate_size_sqft || null,
      covered_open: record.physical?.covered_open || 'open',
      accessible: record.physical?.accessible ?? null,
      level: record.physical?.level || 'ground',
      has_water: record.physical?.has_water ?? null,
      has_power: record.physical?.has_power ?? null,
      has_restrooms: record.physical?.has_restrooms ?? null,
      surface_type: record.physical?.surface_type || null,
    },

    zoning: record.zoning || null,
    assessed_value: record.assessed_value || null,
    restrictions: record.restrictions || [],
    adjacent_context: record.adjacent_context || null,
    condition: record.condition || null,

    activation_potential: record.activation_potential || [],
    data_source_url: record.data_source_url || '',
    data_source_name: record.data_source_name || '',
    scraped_at: record.scraped_at || new Date().toISOString(),
    discovery_cycle: record.discovery_cycle || 0,
  }

  const dir = join(SPACES_DIR, state, munSlug)
  writeJSON(join(dir, `${id}.json`), full)
  return full
}

export function getSpace(state, municipalitySlug, id) {
  return readJSON(join(SPACES_DIR, state, municipalitySlug, `${id}.json`))
}

export function countSpaces() {
  let total = 0
  for (const state of listDirs(SPACES_DIR)) {
    for (const mun of listDirs(join(SPACES_DIR, state))) {
      total += listJSON(join(SPACES_DIR, state, mun)).length
    }
  }
  return total
}

export function countByState() {
  const counts = {}
  for (const state of listDirs(SPACES_DIR)) {
    let stateTotal = 0
    for (const mun of listDirs(join(SPACES_DIR, state))) {
      stateTotal += listJSON(join(SPACES_DIR, state, mun)).length
    }
    if (stateTotal > 0) counts[state] = stateTotal
  }
  return counts
}

export function countByType() {
  const counts = {}
  for (const state of listDirs(SPACES_DIR)) {
    for (const mun of listDirs(join(SPACES_DIR, state))) {
      for (const file of listJSON(join(SPACES_DIR, state, mun))) {
        const space = readJSON(file)
        if (space?.type) {
          counts[space.type] = (counts[space.type] || 0) + 1
        }
      }
    }
  }
  return counts
}

// ── Summary / indexes ───────────────────────────────────────────────────────

export function rebuildSummary() {
  const byState = countByState()
  const byType = countByType()
  const total = Object.values(byState).reduce((a, b) => a + b, 0)

  const summary = {
    updated_at: new Date().toISOString(),
    total_spaces: total,
    states_covered: Object.keys(byState).length,
    by_state: byState,
    by_type: byType,
    type_count: Object.keys(byType).length,
  }

  writeJSON(join(META_DIR, 'sphere-summary.json'), summary)
  return summary
}
