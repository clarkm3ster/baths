/**
 * FRAGMENT — Source Registry
 *
 * Aggregates all source definitions from domain modules.
 * Every source maps to specific dome layers.
 *
 * Source structure:
 *   { id, label, api, layers, scrape(fips) }
 *
 * layers: Array of dome layer numbers this source feeds
 *   1=Legal, 2=Systems, 3=Fiscal, 4=Health, 5=Housing,
 *   6=Economic, 7=Education, 8=Community, 9=Environment
 */

import censusSources from './census.mjs'
import healthSources from './health.mjs'
import housingSources from './housing.mjs'
import environmentSources from './environment.mjs'
import economicSources from './economic.mjs'
import educationSources from './education.mjs'
import legalFiscalSources from './legal-fiscal.mjs'
import communitySources from './community.mjs'

// Flatten all sources into a single registry
const ALL_SOURCES = [
  ...censusSources,
  ...healthSources,
  ...housingSources,
  ...environmentSources,
  ...economicSources,
  ...educationSources,
  ...legalFiscalSources,
  ...communitySources,
]

// Validate: no duplicate IDs
const ids = new Set()
for (const s of ALL_SOURCES) {
  if (ids.has(s.id)) {
    console.warn(`DUPLICATE SOURCE ID: ${s.id}`)
  }
  ids.add(s.id)
}

export default ALL_SOURCES

// ── Registry queries ────────────────────────────────────────────

export function getSourcesByLayer(layer) {
  return ALL_SOURCES.filter(s => s.layers?.includes(layer))
}

export function getSourcesByDomain(domain) {
  const layerMap = {
    legal: 1, systems: 2, fiscal: 3, health: 4, housing: 5,
    economic: 6, education: 7, community: 8, environment: 9,
  }
  const layer = layerMap[domain]
  return layer ? getSourcesByLayer(layer) : []
}

export function getSourceCount() {
  return ALL_SOURCES.length
}

export function getLayerCoverage() {
  const coverage = {}
  for (let i = 1; i <= 9; i++) {
    coverage[i] = getSourcesByLayer(i).length
  }
  return coverage
}

export function printRegistry() {
  const layerNames = {
    1: 'Legal', 2: 'Systems', 3: 'Fiscal', 4: 'Health', 5: 'Housing',
    6: 'Economic', 7: 'Education', 8: 'Community', 9: 'Environment',
  }

  console.log(`\n── Source Registry: ${ALL_SOURCES.length} sources ──────────────`)
  const coverage = getLayerCoverage()
  for (const [layer, count] of Object.entries(coverage)) {
    console.log(`  Layer ${layer} (${layerNames[layer]}): ${count} sources`)
  }
  console.log('')
}
