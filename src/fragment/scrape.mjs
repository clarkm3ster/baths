#!/usr/bin/env node
/**
 * FRAGMENT — Data scraper runtime
 *
 * Executes all registered scrapers. Writes output organized by dome layer:
 *
 *   data/layer-01-legal/{source-id}/{fips}.json
 *   data/layer-02-systems/{source-id}/{fips}.json
 *   ...
 *   data/layer-09-environment/{source-id}/{fips}.json
 *   data/raw/{source-id}/{fips}.json          ← unmapped sources
 *
 * Scheduling: split-batch strategy
 *   - 70% of batch goes to REFRESH (re-scrape existing data, oldest first)
 *   - 30% of batch goes to DISCOVERY (try never-scraped pairs)
 *   - Sources with >5 consecutive failures are deprioritized (1 pair per run)
 *   - Sources with >15 consecutive failures are disabled until manual reset
 *   - Failure counts are tracked in data/meta/failures.json
 */

import { readFileSync, writeFileSync, mkdirSync, existsSync, readdirSync, copyFileSync } from 'node:fs'
import { join, dirname } from 'node:path'
import { fileURLToPath } from 'node:url'
import { delay, readJSON, writeJSON, COUNTIES } from './lib.mjs'
import ALL_SOURCES, { printRegistry, getLayerCoverage } from './sources/index.mjs'

const __dirname = dirname(fileURLToPath(import.meta.url))
const ROOT = join(__dirname, '..', '..')
const DATA = join(ROOT, 'data')
const META = join(DATA, 'meta')

const LAYER_DIRS = {
  1: 'layer-01-legal',
  2: 'layer-02-systems',
  3: 'layer-03-fiscal',
  4: 'layer-04-health',
  5: 'layer-05-housing',
  6: 'layer-06-economic',
  7: 'layer-07-education',
  8: 'layer-08-community',
  9: 'layer-09-environment',
}

// ── Config ───────────────────────────────────────────────────────────────────
const BATCH_LIMIT = parseInt(process.env.FRAGMENT_BATCH_LIMIT || '100')
const DELAY_MS = parseInt(process.env.FRAGMENT_DELAY_MS || '400')
const REFRESH_PCT = 0.7     // 70% of batch for refreshing known-working sources
const DISCOVERY_PCT = 0.3   // 30% for trying never-scraped sources
const BACKOFF_THRESHOLD = 5  // After 5 consecutive failures, deprioritize
const DISABLE_THRESHOLD = 15 // After 15 consecutive failures, disable source

// ── Fragment path helpers ────────────────────────────────────────────────────

function layerDir(layerNum) {
  return join(DATA, LAYER_DIRS[layerNum] || 'raw')
}

function fragmentPath(sourceId, fips, layerNum) {
  return join(layerDir(layerNum), sourceId, `${fips}.json`)
}

function primaryPath(source, fips) {
  const primary = source.layers?.[0]
  return fragmentPath(source.id, fips, primary)
}

function allPaths(source, fips) {
  const layers = source.layers || []
  if (layers.length === 0) return [join(DATA, 'raw', source.id, `${fips}.json`)]
  return layers.map(l => fragmentPath(source.id, fips, l))
}

function getFragmentAge(source, fips) {
  const existing = readJSON(primaryPath(source, fips))
  if (!existing?.scraped_at) return Infinity
  return Date.now() - new Date(existing.scraped_at).getTime()
}

// ── Failure tracking ─────────────────────────────────────────────────────────

function loadFailures() {
  return readJSON(join(META, 'failures.json')) || {}
}

function saveFailures(failures) {
  writeJSON(join(META, 'failures.json'), failures)
}

function recordFailure(failures, sourceId, error) {
  if (!failures[sourceId]) {
    failures[sourceId] = { consecutive: 0, total: 0, last_error: '', last_tried: '' }
  }
  failures[sourceId].consecutive++
  failures[sourceId].total++
  failures[sourceId].last_error = error
  failures[sourceId].last_tried = new Date().toISOString()
}

function recordSuccess(failures, sourceId) {
  if (failures[sourceId]) {
    failures[sourceId].consecutive = 0
    failures[sourceId].last_success = new Date().toISOString()
  }
}

function isDisabled(failures, sourceId) {
  return (failures[sourceId]?.consecutive || 0) >= DISABLE_THRESHOLD
}

function isBackedOff(failures, sourceId) {
  return (failures[sourceId]?.consecutive || 0) >= BACKOFF_THRESHOLD
}

// ── Scheduling — split batch: refresh + discovery ────────────────────────────

function pickWork(sources, counties, limit, failures) {
  const refreshPairs = []
  const discoveryPairs = []
  const disabledSources = new Set()

  for (const source of sources) {
    if (isDisabled(failures, source.id)) {
      disabledSources.add(source.id)
      continue
    }

    for (const county of counties) {
      const age = getFragmentAge(source, county.fips)

      if (age === Infinity) {
        // Never scraped — discovery pool
        discoveryPairs.push({ source, county, age })
      } else {
        // Previously scraped — refresh pool
        refreshPairs.push({ source, county, age })
      }
    }
  }

  // Sort both pools: oldest first
  refreshPairs.sort((a, b) => b.age - a.age)
  discoveryPairs.sort((a, b) => {
    // Deprioritize backed-off sources within discovery
    const aBackoff = isBackedOff(failures, a.source.id) ? 1 : 0
    const bBackoff = isBackedOff(failures, b.source.id) ? 1 : 0
    if (aBackoff !== bBackoff) return aBackoff - bBackoff
    return b.age - a.age
  })

  // For backed-off sources in discovery, limit to 1 pair per source
  const backedOffSeen = new Set()
  const filteredDiscovery = discoveryPairs.filter(item => {
    if (isBackedOff(failures, item.source.id)) {
      if (backedOffSeen.has(item.source.id)) return false
      backedOffSeen.add(item.source.id)
    }
    return true
  })

  // Allocate batch slots
  const refreshSlots = Math.min(
    Math.ceil(limit * REFRESH_PCT),
    refreshPairs.length
  )
  const discoverySlots = Math.min(
    limit - refreshSlots,
    filteredDiscovery.length
  )

  // If refresh pool is empty (first run), give all to discovery
  const actualRefresh = refreshPairs.slice(0, refreshSlots || 0)
  const actualDiscovery = filteredDiscovery.slice(0, discoverySlots || limit)

  const work = [...actualRefresh, ...actualDiscovery]

  // Log scheduling decisions
  console.log(`\n── Scheduling ──────────────────────────────`)
  console.log(`  Refresh pool:   ${refreshPairs.length} pairs → ${actualRefresh.length} selected`)
  console.log(`  Discovery pool: ${discoveryPairs.length} pairs → ${actualDiscovery.length} selected`)
  console.log(`  Backed-off:     ${backedOffSeen.size} sources (limited to 1 pair each)`)
  console.log(`  Disabled:       ${disabledSources.size} sources (>${DISABLE_THRESHOLD} consecutive failures)`)
  if (disabledSources.size > 0) {
    console.log(`    ${[...disabledSources].slice(0, 10).join(', ')}${disabledSources.size > 10 ? '...' : ''}`)
  }
  console.log(`  Total work:     ${work.length} items\n`)

  return work
}

// ── Write fragment to all layer directories ──────────────────────────────────

function writeFragment(source, fips, countyName, data) {
  const fragment = {
    source: source.id,
    source_label: source.label,
    api: source.api,
    layers: source.layers,
    fips,
    county_name: countyName,
    scraped_at: new Date().toISOString(),
    data,
  }

  const paths = allPaths(source, fips)

  // Write primary copy
  writeJSON(paths[0], fragment)

  // Copy to additional layer directories
  for (let i = 1; i < paths.length; i++) {
    try {
      mkdirSync(dirname(paths[i]), { recursive: true })
      copyFileSync(paths[0], paths[i])
    } catch {
      writeJSON(paths[i], fragment)
    }
  }
}

// ── Main scrape run ──────────────────────────────────────────────────────────

async function run() {
  console.log('\n╔══════════════════════════════════════════╗')
  console.log('║         FRAGMENT — Data Scraper          ║')
  console.log('╚══════════════════════════════════════════╝\n')

  const startTime = Date.now()
  printRegistry()

  // Ensure layer directories exist
  for (const dir of Object.values(LAYER_DIRS)) {
    mkdirSync(join(DATA, dir), { recursive: true })
  }
  mkdirSync(join(DATA, 'raw'), { recursive: true })
  mkdirSync(META, { recursive: true })

  const sources = ALL_SOURCES
  const failures = loadFailures()
  const work = pickWork(sources, COUNTIES, BATCH_LIMIT, failures)

  console.log(`Sources: ${sources.length}`)
  console.log(`Counties: ${COUNTIES.length}`)
  console.log(`Max possible pairs: ${sources.length * COUNTIES.length}`)
  console.log(`Work items this run: ${work.length}`)
  console.log(`Batch limit: ${BATCH_LIMIT}\n`)

  let scraped = 0
  let failed = 0
  let gapsLogged = 0
  const gaps = []
  const sourcesUpdated = {}
  const layerHits = {}

  for (const item of work) {
    const { source, county } = item
    const tag = `[${source.id}][${county.fips}]`

    try {
      process.stdout.write(`  ${tag} ${county.name}... `)
      const result = await source.scrape(county.fips)

      if (result.ok) {
        writeFragment(source, county.fips, county.name, result.data)
        scraped++
        sourcesUpdated[source.id] = (sourcesUpdated[source.id] || 0) + 1
        for (const layer of (source.layers || [])) {
          layerHits[layer] = (layerHits[layer] || 0) + 1
        }
        recordSuccess(failures, source.id)
        console.log('OK')
      } else {
        console.log(`SKIP — ${result.error}`)
        recordFailure(failures, source.id, result.error)
        if (result.needs_key) {
          gaps.push({
            source: source.id, fips: county.fips, county: county.name,
            reason: result.error, needs_key: true, logged_at: new Date().toISOString(),
          })
          gapsLogged++
        } else {
          failed++
        }
      }
    } catch (err) {
      console.log(`ERROR — ${err.message}`)
      recordFailure(failures, source.id, err.message)
      failed++
    }

    await delay(DELAY_MS)
  }

  // ── Update metadata ──────────────────────────────────────────────────────

  // Save failure tracking
  saveFailures(failures)

  const sourcesPath = join(META, 'sources.json')
  const existingSources = readJSON(sourcesPath) || {}
  for (const [sid, count] of Object.entries(sourcesUpdated)) {
    const src = sources.find(s => s.id === sid)
    existingSources[sid] = existingSources[sid] || {
      label: src?.label, api: src?.api, layers: src?.layers,
      first_scraped: new Date().toISOString(), total_scrapes: 0,
    }
    existingSources[sid].last_scraped = new Date().toISOString()
    existingSources[sid].total_scrapes = (existingSources[sid].total_scrapes || 0) + count
    existingSources[sid].counties_covered = countFragments(sid, sources)
  }
  writeJSON(sourcesPath, existingSources)

  const coverage = buildCoverage(sources)
  writeJSON(join(META, 'coverage.json'), coverage)

  const gapsPath = join(META, 'gaps.json')
  const existingGaps = readJSON(gapsPath) || { gaps: [], last_updated: null }
  const gapMap = new Map(existingGaps.gaps.map(g => [`${g.source}:${g.fips}`, g]))
  for (const gap of gaps) gapMap.set(`${gap.source}:${gap.fips}`, gap)
  writeJSON(gapsPath, { gaps: Array.from(gapMap.values()), last_updated: new Date().toISOString(), total: gapMap.size })

  const elapsed = ((Date.now() - startTime) / 1000).toFixed(1)
  const layerNames = { 1:'Legal', 2:'Systems', 3:'Fiscal', 4:'Health', 5:'Housing', 6:'Economic', 7:'Education', 8:'Community', 9:'Environment' }

  console.log('\n── Results ─────────────────────────────────')
  console.log(`  Scraped:    ${scraped}`)
  console.log(`  Failed:     ${failed}`)
  console.log(`  Gaps:       ${gapsLogged}`)
  console.log(`  Time:       ${elapsed}s`)
  console.log(`  Fragments:  ${countAllFragments()}`)
  console.log('')
  console.log('  Layer hits this run:')
  for (const [layer, count] of Object.entries(layerHits).sort((a, b) => a[0] - b[0])) {
    console.log(`    ${layer}. ${layerNames[layer]}: ${count} new fragments`)
  }

  // Report failure summary
  const failedSources = Object.entries(failures)
    .filter(([, f]) => f.consecutive > 0)
    .sort((a, b) => b[1].consecutive - a[1].consecutive)
  if (failedSources.length > 0) {
    console.log('\n  Source failure summary:')
    for (const [sid, f] of failedSources.slice(0, 15)) {
      const status = f.consecutive >= DISABLE_THRESHOLD ? 'DISABLED'
        : f.consecutive >= BACKOFF_THRESHOLD ? 'BACKED OFF'
        : 'failing'
      console.log(`    ${sid}: ${f.consecutive} consecutive (${status}) — ${f.last_error}`)
    }
  }

  console.log('────────────────────────────────────────────\n')

  return { scraped, failed, gaps: gapsLogged, total_fragments: countAllFragments() }
}

// ── Coverage helpers ─────────────────────────────────────────────────────────

function countFragments(sourceId, sources) {
  const src = sources.find(s => s.id === sourceId)
  const layer = src?.layers?.[0]
  const dir = join(layerDir(layer), sourceId)
  if (!existsSync(dir)) return 0
  return readdirSync(dir).filter(f => f.endsWith('.json')).length
}

function countAllFragments() {
  let count = 0
  for (const dir of [...Object.values(LAYER_DIRS), 'raw']) {
    const full = join(DATA, dir)
    if (!existsSync(full)) continue
    for (const sub of readdirSync(full)) {
      const subFull = join(full, sub)
      try {
        count += readdirSync(subFull).filter(f => f.endsWith('.json')).length
      } catch { /* skip non-dirs */ }
    }
  }
  return count
}

function buildCoverage(sources) {
  const layerNames = { 1:'Legal', 2:'Systems', 3:'Fiscal', 4:'Health', 5:'Housing', 6:'Economic', 7:'Education', 8:'Community', 9:'Environment' }

  const coverage = {
    generated_at: new Date().toISOString(),
    total_sources: sources.length,
    total_counties: COUNTIES.length,
    total_fragments: countAllFragments(),
    max_possible_fragments: sources.length * COUNTIES.length,
    storage: 'layer-based',
    by_layer: {},
    by_source: {},
    by_county: {},
  }

  for (let i = 1; i <= 9; i++) {
    const layerSources = sources.filter(s => s.layers?.includes(i))
    const dir = join(DATA, LAYER_DIRS[i])
    let fragments = 0
    if (existsSync(dir)) {
      for (const sub of readdirSync(dir)) {
        try { fragments += readdirSync(join(dir, sub)).filter(f => f.endsWith('.json')).length } catch {}
      }
    }
    coverage.by_layer[i] = {
      name: layerNames[i],
      directory: LAYER_DIRS[i],
      sources: layerSources.length,
      fragments,
    }
  }

  for (const source of sources) {
    coverage.by_source[source.id] = {
      label: source.label, api: source.api, layers: source.layers,
      fragments: countFragments(source.id, sources),
    }
  }

  for (const county of COUNTIES) {
    let fragments = 0
    for (const source of sources) {
      if (existsSync(primaryPath(source, county.fips))) fragments++
    }
    coverage.by_county[county.fips] = {
      name: county.name, fragments,
      coverage_pct: Math.round((fragments / sources.length) * 100),
    }
  }

  return coverage
}

// ── Run ──────────────────────────────────────────────────────────────────────
run().then(() => process.exit(0)).catch(err => { console.error('FRAGMENT FATAL:', err); process.exit(1) })
