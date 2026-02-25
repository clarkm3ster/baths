/**
 * SPHERE FRAGMENT — Gap Logger
 *
 * For every municipality where no accessible public property data exists,
 * log what was searched for and what was not found.
 * The gap itself is data — which cities are invisible.
 */

import { readdirSync } from 'node:fs'
import { join } from 'node:path'
import { GAPS_DIR, readJSON, writeJSON, slugify } from './lib.mjs'

export function logGap(municipality) {
  const state = municipality.state?.toUpperCase() || 'XX'
  const slug = slugify(municipality.name || 'unknown')

  const gap = {
    municipality: municipality.name,
    state,
    population: municipality.population || null,
    fips: municipality.fips || null,
    searched_for: municipality.searched_for || [
      'open data portal',
      'county assessor records',
      'GIS parcel data',
      'municipal CAFR',
      'parks department inventory',
      'school district property records',
    ],
    not_found: municipality.not_found || [],
    sources_checked: municipality.sources_checked || [],
    gap_type: municipality.gap_type || 'no-data-portal',
    logged_at: new Date().toISOString(),
    discovery_cycle: municipality.discovery_cycle || 0,
  }

  writeJSON(join(GAPS_DIR, state, `${slug}.json`), gap)
  return gap
}

export function loadGaps(state) {
  const dir = join(GAPS_DIR, state)
  const gaps = []
  try {
    for (const f of readdirSync(dir).filter(f => f.endsWith('.json'))) {
      const gap = readJSON(join(dir, f))
      if (gap) gaps.push(gap)
    }
  } catch {}
  return gaps
}
