#!/usr/bin/env node
/**
 * FRAGMENT — Data scraper agent
 *
 * Collects every publicly available data point about what it means to be alive,
 * by geography and time. It mirrors the fragmentation of human data.
 *
 * Sources are defined in src/fragment/sources/ — organized by dome layer.
 * Each source maps to specific layers (1=Legal through 9=Environment).
 * New sources can be added by editing the domain files or creating new ones.
 *
 * Architecture:
 *   sources/census.mjs       — 40+ Census ACS variable groups
 *   sources/health.mjs       — CDC PLACES, CMS, HRSA, SAMHSA
 *   sources/housing.mjs      — HUD, FEMA, HMDA, LIHTC
 *   sources/environment.mjs  — EPA, USGS, NWS, NOAA, FEMA
 *   sources/economic.mjs     — BLS, Census CBP, FDIC, USASpending
 *   sources/education.mjs    — NCES, College Scorecard, IPEDS
 *   sources/legal-fiscal.mjs — Federal Register, eCFR, Congress, Treasury
 *   sources/community.mjs    — Nonprofits, VA, FCC, elections
 *
 * Runs via GitHub Actions on schedule. No external dependencies — Node built-in fetch only.
 */

import { readFileSync, writeFileSync, mkdirSync, existsSync, readdirSync } from 'node:fs'
import { join, dirname } from 'node:path'
import { fileURLToPath } from 'node:url'
import { delay, readJSON, writeJSON, COUNTIES } from './lib.mjs'
import ALL_SOURCES, { printRegistry, getLayerCoverage } from './sources/index.mjs'

const __dirname = dirname(fileURLToPath(import.meta.url))
const ROOT = join(__dirname, '..', '..')
const DATA = join(ROOT, 'data')
const FRAGMENTS = join(DATA, 'fragments')
const META = join(DATA, 'meta')

// ── Config ───────────────────────────────────────────────────────────────────
const BATCH_LIMIT = parseInt(process.env.FRAGMENT_BATCH_LIMIT || '100')
const DELAY_MS = parseInt(process.env.FRAGMENT_DELAY_MS || '400')

// ── Fragment path helpers ────────────────────────────────────────────────────

function fragmentPath(sourceId, fips) {
  return join(FRAGMENTS, sourceId, `${fips}.json`)
}

function getFragmentAge(sourceId, fips) {
  const existing = readJSON(fragmentPath(sourceId, fips))
  if (!existing?.scraped_at) return Infinity
  return Date.now() - new Date(existing.scraped_at).getTime()
}

// ── Scheduling — breadth first, oldest first ─────────────────────────────────

function pickWork(sources, counties, limit) {
  const pairs = []

  for (const source of sources) {
    for (const county of counties) {
      const age = getFragmentAge(source.id, county.fips)
      pairs.push({
        source,
        county,
        age,
        priority: age,
      })
    }
  }

  // Sort: never-scraped first (Infinity), then oldest
  pairs.sort((a, b) => b.age - a.age)

  return pairs.slice(0, limit)
}

// ── Main scrape run ──────────────────────────────────────────────────────────

async function run() {
  console.log('\n╔══════════════════════════════════════════╗')
  console.log('║         FRAGMENT — Data Scraper          ║')
  console.log('╚══════════════════════════════════════════╝\n')

  const startTime = Date.now()

  // Print the registry
  printRegistry()

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
        const fragment = {
          source: source.id,
          source_label: source.label,
          api: source.api,
          layers: source.layers,
          fips: county.fips,
          county_name: county.name,
          scraped_at: new Date().toISOString(),
          data: result.data,
        }

        writeJSON(fragmentPath(source.id, county.fips), fragment)
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
            source: source.id,
            fips: county.fips,
            county: county.name,
            reason: result.error,
            needs_key: true,
            logged_at: new Date().toISOString(),
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

  // sources.json — what's been scraped and when
  const sourcesPath = join(META, 'sources.json')
  const existingSources = readJSON(sourcesPath) || {}
  for (const [sid, count] of Object.entries(sourcesUpdated)) {
    const src = sources.find(s => s.id === sid)
    existingSources[sid] = existingSources[sid] || {
      label: src?.label,
      api: src?.api,
      layers: src?.layers,
      first_scraped: new Date().toISOString(),
      total_scrapes: 0,
    }
    existingSources[sid].last_scraped = new Date().toISOString()
    existingSources[sid].total_scrapes = (existingSources[sid].total_scrapes || 0) + count
    existingSources[sid].counties_covered = countFragments(sid)
  }
  writeJSON(sourcesPath, existingSources)

  // coverage.json — overall stats
  const coverage = buildCoverage(sources)
  writeJSON(join(META, 'coverage.json'), coverage)

  // gaps.json — what's missing
  const gapsPath = join(META, 'gaps.json')
  const existingGaps = readJSON(gapsPath) || { gaps: [], last_updated: null }
  const gapKey = g => `${g.source}:${g.fips}`
  const gapMap = new Map(existingGaps.gaps.map(g => [gapKey(g), g]))
  for (const gap of gaps) {
    gapMap.set(gapKey(gap), gap)
  }
  writeJSON(gapsPath, {
    gaps: Array.from(gapMap.values()),
    last_updated: new Date().toISOString(),
    total: gapMap.size,
  })

  const elapsed = ((Date.now() - startTime) / 1000).toFixed(1)
  const layerNames = {
    1: 'Legal', 2: 'Systems', 3: 'Fiscal', 4: 'Health', 5: 'Housing',
    6: 'Economic', 7: 'Education', 8: 'Community', 9: 'Environment',
  }

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

function countFragments(sourceId) {
  const dir = join(FRAGMENTS, sourceId)
  if (!existsSync(dir)) return 0
  return readdirSync(dir).filter(f => f.endsWith('.json')).length
}

function countAllFragments() {
  if (!existsSync(FRAGMENTS)) return 0
  let count = 0
  for (const dir of readdirSync(FRAGMENTS)) {
    const full = join(FRAGMENTS, dir)
    try {
      count += readdirSync(full).filter(f => f.endsWith('.json')).length
    } catch { /* skip non-directories */ }
  }
  return count
}

function buildCoverage(sources) {
  const layerNames = {
    1: 'Legal', 2: 'Systems', 3: 'Fiscal', 4: 'Health', 5: 'Housing',
    6: 'Economic', 7: 'Education', 8: 'Community', 9: 'Environment',
  }

  const coverage = {
    generated_at: new Date().toISOString(),
    total_sources: sources.length,
    total_counties: COUNTIES.length,
    total_fragments: countAllFragments(),
    max_possible_fragments: sources.length * COUNTIES.length,
    by_layer: {},
    by_source: {},
    by_county: {},
  }

  // Layer coverage
  for (let i = 1; i <= 9; i++) {
    const layerSources = sources.filter(s => s.layers?.includes(i))
    coverage.by_layer[i] = {
      name: layerNames[i],
      sources: layerSources.length,
      source_ids: layerSources.map(s => s.id),
    }
  }

  // Source coverage
  for (const source of sources) {
    coverage.by_source[source.id] = {
      label: source.label,
      api: source.api,
      layers: source.layers,
      fragments: countFragments(source.id),
    }
  }

  // County coverage
  for (const county of COUNTIES) {
    let fragments = 0
    for (const source of sources) {
      if (existsSync(fragmentPath(source.id, county.fips))) fragments++
    }
    coverage.by_county[county.fips] = {
      name: county.name,
      fragments,
      coverage_pct: Math.round((fragments / sources.length) * 100),
    }
  }

  return coverage
}

// ── Run ──────────────────────────────────────────────────────────────────────
run().then(result => {
  // Exit 0 even if some fail — Cosm should still run on existing data
  process.exit(0)
}).catch(err => {
  console.error('FRAGMENT FATAL:', err)
  process.exit(1)
})
