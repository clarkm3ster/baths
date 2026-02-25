#!/usr/bin/env node
/**
 * SPHERE FRAGMENT — Autonomous Public Space Discovery Engine
 *
 * Discovers every physical space owned or controlled by every
 * municipality in the United States.
 *
 * Claude IS the intelligence layer. This script is the execution pipeline.
 * Claude writes municipality discovery definitions to:
 *   data/sphere-queue/{state}/{municipality-slug}.json
 *
 * Each definition contains:
 *   - municipality info (name, state, population, fips)
 *   - data sources to probe (URLs, types)
 *   - scraper definitions for each source
 *   - spaces discovered from Claude's analysis
 *
 * The engine processes the queue:
 *   1. LOAD — read queue, check what's already done
 *   2. PROBE — test data source URLs
 *   3. SCRAPE — run scrapers, collect space records
 *   4. REGISTER — save spaces, update type catalog
 *   5. REPORT — log results and gaps
 *
 * Usage:
 *   node src/sphere/discover.mjs                     # process queue
 *   node src/sphere/discover.mjs --loop              # perpetual mode
 *   node src/sphere/discover.mjs --state PA          # single state
 *   node src/sphere/discover.mjs --city "Philadelphia" --state PA  # single city
 *
 * Known open data portals (Socrata SODA pattern):
 *   - data.phila.gov (Philadelphia)
 *   - data.cityofnewyork.us (NYC)
 *   - data.cityofchicago.org (Chicago)
 *   - data.lacity.org (Los Angeles)
 *   - data.sfgov.org (San Francisco)
 *   - data.seattle.gov (Seattle)
 *   - data.austintexas.gov (Austin)
 *   - data.boston.gov (Boston)
 *   - data.detroitmi.gov (Detroit)
 *   - data.pittsburghpa.gov (Pittsburgh)
 *   ... and hundreds more on data.gov
 */

import { readdirSync, existsSync, mkdirSync, renameSync } from 'node:fs'
import { join, dirname } from 'node:path'
import { fileURLToPath } from 'node:url'
import {
  ROOT, DATA, SPACES_DIR, TYPES_DIR, GAPS_DIR, QUEUE_DIR, REPORTS_DIR, META_DIR,
  readJSON, writeJSON, listJSON, listDirs, safeFetch, delay, slugify, spaceID
} from './lib.mjs'
import { addSpace, countSpaces, rebuildSummary } from './spaces.mjs'
import { loadTypes, addType, seedTypes } from './types.mjs'
import { logGap } from './gaps.mjs'

const __dirname = dirname(fileURLToPath(import.meta.url))
const PROCESSED_DIR = join(QUEUE_DIR, 'processed')
const LOOP_INTERVAL = 60 * 1000

// ── Logging ─────────────────────────────────────────────────────────────────
const P = {
  phase: (n, name) => console.log(`\n${'═'.repeat(60)}\n  PHASE ${n}: ${name}\n${'═'.repeat(60)}`),
  step:  (msg) => console.log(`  > ${msg}`),
  ok:    (msg) => console.log(`  + ${msg}`),
  fail:  (msg) => console.log(`  - ${msg}`),
  info:  (msg) => console.log(`    ${msg}`),
  blank: ()    => console.log(''),
}

let cycleCount = 0

// ═══════════════════════════════════════════════════════════════════════════
//  PHASE 1: LOAD
// ═══════════════════════════════════════════════════════════════════════════

function loadQueue(filterState, filterCity) {
  P.phase(1, 'LOAD')

  mkdirSync(QUEUE_DIR, { recursive: true })
  mkdirSync(PROCESSED_DIR, { recursive: true })

  // Ensure type catalog exists
  loadTypes()

  const queue = []

  // Queue structure: data/sphere-queue/{state}/{city-slug}.json
  const states = filterState
    ? [filterState.toUpperCase()]
    : listDirs(QUEUE_DIR).filter(d => d !== 'processed' && d.length === 2)

  for (const state of states) {
    const stateDir = join(QUEUE_DIR, state)
    if (!existsSync(stateDir)) continue

    const files = readdirSync(stateDir).filter(f => f.endsWith('.json'))
    for (const f of files) {
      const def = readJSON(join(stateDir, f))
      if (!def) continue
      if (filterCity && slugify(def.municipality) !== slugify(filterCity)) continue
      queue.push({ ...def, _file: join(stateDir, f), _state: state })
    }
  }

  P.ok(`Queue: ${queue.length} municipalities`)
  P.ok(`Existing spaces: ${countSpaces()}`)
  return queue
}

// ═══════════════════════════════════════════════════════════════════════════
//  PHASE 2: PROBE — test data source URLs
// ═══════════════════════════════════════════════════════════════════════════

async function probeSources(municipalityDef) {
  const sources = municipalityDef.data_sources || []
  if (sources.length === 0) return []

  P.step(`Probing ${sources.length} sources for ${municipalityDef.municipality}, ${municipalityDef.state}`)

  const results = []
  for (const source of sources) {
    if (!source.probe_url) {
      results.push({ ...source, probe_ok: false, probe_error: 'No URL' })
      continue
    }

    process.stdout.write(`    ${source.name}... `)
    const res = await safeFetch(source.probe_url, source.name, { timeout: 15000 })

    if (res.ok) {
      const dataSize = typeof res.data === 'string' ? res.data.length : JSON.stringify(res.data).length
      console.log(`OK (${dataSize} bytes)`)
      results.push({ ...source, probe_ok: true, probe_data: res.data })
    } else {
      console.log(`FAIL (${res.error})`)
      results.push({ ...source, probe_ok: false, probe_error: res.error })
    }

    await delay(300)
  }

  return results
}

// ═══════════════════════════════════════════════════════════════════════════
//  PHASE 3: REGISTER SPACES — save spaces from definitions
// ═══════════════════════════════════════════════════════════════════════════

function registerSpaces(municipalityDef) {
  const spaces = municipalityDef.spaces || []
  if (spaces.length === 0) return { registered: 0, types_discovered: 0 }

  P.step(`Registering ${spaces.length} spaces`)

  let registered = 0
  let typesDiscovered = 0

  for (const space of spaces) {
    const record = addSpace({
      ...space,
      municipality: municipalityDef.municipality,
      state: municipalityDef.state,
      county: municipalityDef.county || null,
      discovery_cycle: cycleCount,
    })

    // Check if this is a new type
    const existingTypes = loadTypes()
    if (!existingTypes.find(t => t.id === space.type)) {
      addType({
        id: space.type,
        name: space.type_name || space.type,
        description: space.type_description || `Discovered in ${municipalityDef.municipality}`,
        discovered_in: `${municipalityDef.municipality}, ${municipalityDef.state}`,
        sphere_layers: space.activation_potential || [],
      })
      typesDiscovered++
      P.ok(`  NEW TYPE: ${space.type}`)
    }

    registered++
  }

  P.ok(`Registered: ${registered} spaces, ${typesDiscovered} new types`)
  return { registered, types_discovered: typesDiscovered }
}

// ═══════════════════════════════════════════════════════════════════════════
//  PHASE 4: ARCHIVE + GAP LOG
// ═══════════════════════════════════════════════════════════════════════════

function archiveAndLog(municipalityDef, probeResults, registerResult) {
  // Move to processed
  if (municipalityDef._file) {
    const processedState = join(PROCESSED_DIR, municipalityDef._state || 'XX')
    mkdirSync(processedState, { recursive: true })
    const destFile = join(processedState, `${slugify(municipalityDef.municipality)}.json`)
    try { renameSync(municipalityDef._file, destFile) } catch {}
  }

  // Log gap if no spaces found
  if (registerResult.registered === 0) {
    logGap({
      name: municipalityDef.municipality,
      state: municipalityDef.state,
      population: municipalityDef.population || null,
      fips: municipalityDef.fips || null,
      sources_checked: probeResults.map(s => s.name),
      not_found: probeResults.filter(s => !s.probe_ok).map(s => `${s.name}: ${s.probe_error}`),
      gap_type: probeResults.every(s => !s.probe_ok) ? 'all-sources-failed' : 'no-spaces-extracted',
      discovery_cycle: cycleCount,
    })
    P.info(`Gap logged for ${municipalityDef.municipality}, ${municipalityDef.state}`)
  }
}

// ═══════════════════════════════════════════════════════════════════════════
//  MAIN CYCLE
// ═══════════════════════════════════════════════════════════════════════════

async function runCycle(filterState, filterCity) {
  cycleCount++
  console.log('\n╔══════════════════════════════════════════════════════════════╗')
  console.log('║         SPHERE FRAGMENT — Public Space Discovery            ║')
  console.log('║                       Cycle ' + String(cycleCount).padStart(4) + '                              ║')
  console.log('╚══════════════════════════════════════════════════════════════╝')

  const queue = loadQueue(filterState, filterCity)
  if (queue.length === 0) {
    P.info('Queue empty — waiting for Claude to add municipality definitions.')
    return { empty: true }
  }

  let totalSpaces = 0
  let totalTypes = 0
  let totalGaps = 0

  for (const def of queue) {
    P.blank()
    P.phase(2, `${def.municipality}, ${def.state}`)

    const probeResults = await probeSources(def)
    const registerResult = registerSpaces(def)

    totalSpaces += registerResult.registered
    totalTypes += registerResult.types_discovered
    if (registerResult.registered === 0) totalGaps++

    archiveAndLog(def, probeResults, registerResult)
  }

  // Rebuild summary
  P.phase(5, 'REPORT')
  const summary = rebuildSummary()

  const report = {
    cycle: cycleCount,
    timestamp: new Date().toISOString(),
    municipalities_processed: queue.length,
    spaces_registered: totalSpaces,
    new_types_discovered: totalTypes,
    gaps_logged: totalGaps,
    total_spaces: summary.total_spaces,
    states_covered: summary.states_covered,
    type_count: summary.type_count,
  }

  mkdirSync(REPORTS_DIR, { recursive: true })
  writeJSON(join(REPORTS_DIR, `cycle-${cycleCount}-${Date.now()}.json`), report)

  console.log(`
  Municipalities: ${queue.length}
  Spaces added:   ${totalSpaces}
  New types:      ${totalTypes}
  Gaps logged:    ${totalGaps}
  Total spaces:   ${summary.total_spaces}
  States:         ${summary.states_covered}
  Types:          ${summary.type_count}
`)

  return report
}

// ── CLI ─────────────────────────────────────────────────────────────────────

const args = process.argv.slice(2)
const loopMode = args.includes('--loop')
const stateIdx = args.indexOf('--state')
const cityIdx = args.indexOf('--city')
const filterState = stateIdx >= 0 ? args[stateIdx + 1] : null
const filterCity = cityIdx >= 0 ? args[cityIdx + 1] : null

async function loop() {
  console.log('SPHERE FRAGMENT — Perpetual discovery mode')
  console.log(`Checking queue every ${LOOP_INTERVAL / 1000}s\n`)

  while (true) {
    await runCycle(filterState, filterCity)
    await new Promise(r => setTimeout(r, LOOP_INTERVAL))
  }
}

if (loopMode) {
  loop().catch(err => { console.error('FATAL:', err); process.exit(1) })
} else {
  runCycle(filterState, filterCity).then(r => {
    process.exit(r.empty ? 0 : (r.spaces_registered > 0 ? 0 : 1))
  }).catch(err => { console.error('FATAL:', err); process.exit(1) })
}
