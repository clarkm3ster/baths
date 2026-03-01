/**
 * ENTITY — Fragment loader
 *
 * Loads all scraped fragment data for a given county (FIPS)
 * into a single flat object keyed by source ID.
 *
 * This is the bridge between the scraper layer (raw data collection)
 * and the entity resolution layer (person-level estimation).
 *
 * Returns: { 'census-income': { data: {...} }, 'hud-fmr': { data: {...} }, ... }
 */

import { readFileSync, readdirSync, existsSync } from 'node:fs'
import { join, dirname } from 'node:path'
import { fileURLToPath } from 'node:url'

const __dirname = dirname(fileURLToPath(import.meta.url))
const DATA = join(__dirname, '..', '..', 'data')

const LAYER_DIRS = [
  'layer-01-legal',
  'layer-02-systems',
  'layer-03-fiscal',
  'layer-04-health',
  'layer-05-housing',
  'layer-06-economic',
  'layer-07-education',
  'layer-08-community',
  'layer-09-environment',
]

/**
 * Load all fragments for a county.
 * Deduplicates — if a source appears in multiple layers, only loads once.
 *
 * @param {string} fips — 5-digit county FIPS code
 * @returns {object} — { sourceId: { data, source, scraped_at, ... }, ... }
 */
export function loadFragments(fips) {
  const fragments = {}

  for (const layerDir of LAYER_DIRS) {
    const dir = join(DATA, layerDir)
    if (!existsSync(dir)) continue

    let sources
    try { sources = readdirSync(dir) } catch { continue }

    for (const sourceId of sources) {
      if (fragments[sourceId]) continue // already loaded from a higher-priority layer

      const filePath = join(dir, sourceId, `${fips}.json`)
      if (!existsSync(filePath)) continue

      try {
        const raw = JSON.parse(readFileSync(filePath, 'utf8'))
        fragments[sourceId] = raw
      } catch {
        // skip corrupt files
      }
    }
  }

  return fragments
}

/**
 * Extract a specific field from fragment data.
 * Handles the nested { data: { field } } structure.
 */
export function getField(fragments, sourceId, field) {
  const frag = fragments[sourceId]
  if (!frag) return null
  const data = frag.data || frag
  return data[field] ?? null
}

/**
 * Get a numeric field, returning 0 if missing.
 */
export function getNum(fragments, sourceId, field) {
  const val = getField(fragments, sourceId, field)
  if (val === null || val === undefined) return 0
  const num = Number(val)
  return isNaN(num) ? 0 : num
}

/**
 * List all available source IDs for a county.
 */
export function availableSources(fips) {
  const sources = new Set()
  for (const layerDir of LAYER_DIRS) {
    const dir = join(DATA, layerDir)
    if (!existsSync(dir)) continue
    try {
      for (const sourceId of readdirSync(dir)) {
        if (existsSync(join(dir, sourceId, `${fips}.json`))) {
          sources.add(sourceId)
        }
      }
    } catch { /* skip */ }
  }
  return [...sources]
}
