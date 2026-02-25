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
 * Each fragment is tagged with every layer it feeds. A single fragment can
 * live in multiple layer directories (via hardlink or copy). The file system
 * is the data lake. The schema is the database.
 *
 * Scheduling: breadth-first, oldest-first across all (source, county) pairs.
 * New sources added by Fragment Agent are automatically picked up.
 */

import { readFileSync, writeFileSync, mkdirSync, existsSync, readdirSync, linkSync, copyFileSync } from 'node:fs'
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

// ── Fragment path helpers ────────────────────────────────────────────────────

function layerDir(layerNum) {
  return join(DATA, LAYER_DIRS[layerNum] || 'raw')
}

function fragmentPath(sourceId, fips, layerNum) {
  return join(layerDir(layerNum), sourceId, `${fips}.json`)
}

// Primary path = first layer in the source's layers array
function primaryPath(source, fips) {
  const primary = source.layers?.[0]
  return fragmentPath(source.id, fips, primary)
}

// All paths this fragment should exist at (one per layer)
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

// ── Scheduling — breadth first, oldest first ─────────────────────────────────

function pickWork(sources, counties, limit) {
  const pairs = []

  for (const source of sources) {
    for (const county of counties) {
      const age = getFragmentAge(source, county.fips)
      pairs.push({ source, county, age })
    }
  }

  // Never-scraped first (Infinity), then oldest
  pairs.sort((a, b) => b.age - a.age)
  return pairs.slice(0, limit)
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
      // If copy fails, write directly
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

  const sources = ALL_SOURCES
  const work = pickWork(sources, COUNTIES, BATCH_LIMIT)

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
        console.log('OK')
      } else {
        console.log(`SKIP — ${result.error}`)
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
      failed++
    }

    await delay(DELAY_MS)
  }

  // ── Update metadata ──────────────────────────────────────────────────────

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
