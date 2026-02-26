#!/usr/bin/env node
/**
 * CHARACTER FRAGMENT — Discovery Engine
 *
 * Autonomous agent that discovers and catalogs every documented person,
 * fictional and real, whose life circumstances have been recorded in
 * enough detail to build a dome around them.
 *
 * Phase 1: Process all seed characters (curated knowledge)
 * Phase 2: Score dome layer richness and prioritize
 * Phase 3: Run API discovery for new source works
 * Phase 4: Follow references between works
 * Phase 5: Expand circumstance catalog
 * Phase 6: Never stop
 *
 * Output:
 *   data/characters/real/{slug}.json
 *   data/characters/fictional/{slug}.json
 *   data/characters/circumstances-catalog/
 *   data/characters/source-works/
 *   data/characters/meta/
 */

import { mkdirSync, existsSync, readdirSync } from 'node:fs'
import { join } from 'node:path'
import {
  readJSON, writeJSON, delay, characterId, slugify, validateCharacter,
  REAL_DIR, FICTIONAL_DIR, CIRCUMSTANCES_DIR, SOURCE_WORKS_DIR, META_DIR, CHARACTERS,
} from './lib.mjs'
import { getAllSeedCharacters, getSourceStats, printRegistry } from './sources/index.mjs'
import { scoreDomeLayerRichness, rankByRichness } from './richness.mjs'
import { loadCatalog, registerCharacterCircumstances, saveCatalog, catalogStats } from './circumstances.mjs'
import { loadTracker, registerWork, registerCharacterForWork, discoverGenres, saveTracker, trackerStats } from './source-works.mjs'
import { runDiscoverySweep, scoreWorkForDomePotential } from './sources/api-discovery.mjs'

// ── Config ────────────────────────────────────────────────────────────────────

const BATCH_LIMIT = parseInt(process.env.CHARACTER_BATCH_LIMIT || '500')
const DISCOVERY_ENABLED = process.env.CHARACTER_DISCOVERY !== 'false'
const DISCOVERY_QUERIES = parseInt(process.env.CHARACTER_DISCOVERY_QUERIES || '3')
const DELAY_MS = parseInt(process.env.CHARACTER_DELAY_MS || '300')

// ── Ensure directories ────────────────────────────────────────────────────────

function ensureDirs() {
  for (const dir of [REAL_DIR, FICTIONAL_DIR, CIRCUMSTANCES_DIR, SOURCE_WORKS_DIR, META_DIR]) {
    mkdirSync(dir, { recursive: true })
  }
}

// ── Write a character file ────────────────────────────────────────────────────

function writeCharacter(character) {
  const id = characterId(character.name, character.source_work)
  const dir = character.real_or_fictional === 'real' ? REAL_DIR : FICTIONAL_DIR
  const path = join(dir, `${id}.json`)

  // Score richness
  const richness = scoreDomeLayerRichness(character)

  const entry = {
    id,
    ...character,
    richness,
    indexed_at: new Date().toISOString(),
  }

  writeJSON(path, entry)
  return { id, path, richness }
}

// ── Check if character already exists ─────────────────────────────────────────

function characterExists(character) {
  const id = characterId(character.name, character.source_work)
  const dir = character.real_or_fictional === 'real' ? REAL_DIR : FICTIONAL_DIR
  return existsSync(join(dir, `${id}.json`))
}

// ── Count existing characters ─────────────────────────────────────────────────

function countExisting() {
  let real = 0
  let fictional = 0
  try { real = readdirSync(REAL_DIR).filter(f => f.endsWith('.json')).length } catch { /* empty */ }
  try { fictional = readdirSync(FICTIONAL_DIR).filter(f => f.endsWith('.json')).length } catch { /* empty */ }
  return { real, fictional, total: real + fictional }
}

// ── Phase 1: Process seed characters ──────────────────────────────────────────

function processSeedCharacters(catalog, tracker) {
  const seeds = getAllSeedCharacters()
  let processed = 0
  let skipped = 0
  let newCircumstanceTypes = 0

  for (const character of seeds) {
    // Validate
    const validation = validateCharacter(character)
    if (!validation.valid) {
      console.log(`    SKIP ${character.name}: ${validation.error || validation.missing.join(', ')}`)
      skipped++
      continue
    }

    // Skip if already indexed
    if (characterExists(character)) {
      skipped++
      continue
    }

    // Write character
    const result = writeCharacter(character)
    processed++

    // Register in circumstance catalog
    const { newTypes } = registerCharacterCircumstances(catalog, character)
    newCircumstanceTypes += newTypes

    // Register source work
    registerWork(tracker, {
      title: character.source_work,
      source_author_creator: character.source_author_creator,
      source_year: character.source_year,
    })
    registerCharacterForWork(tracker, character.source_work, character.name)

    const buildability = result.richness.dome_buildability
    const filled = result.richness.filled_layers
    console.log(`    ✓ ${character.name} [${character.real_or_fictional}] — ${filled} layers, ${buildability} buildability`)

    if (processed >= BATCH_LIMIT) break
  }

  return { processed, skipped, newCircumstanceTypes }
}

// ── Phase 2: Build rankings ───────────────────────────────────────────────────

function buildRankings() {
  const allCharacters = []

  // Read all character files
  for (const dir of [REAL_DIR, FICTIONAL_DIR]) {
    try {
      for (const file of readdirSync(dir).filter(f => f.endsWith('.json'))) {
        const character = readJSON(join(dir, file))
        if (character) allCharacters.push(character)
      }
    } catch { /* empty dir */ }
  }

  // Rank by richness
  const ranked = rankByRichness(allCharacters)

  // Write rankings
  writeJSON(join(META_DIR, 'rankings.json'), {
    generated_at: new Date().toISOString(),
    total_characters: ranked.length,
    rankings: ranked.slice(0, 100), // Top 100
  })

  // Write rankings by buildability tier
  const tiers = { high: [], medium: [], low: [] }
  for (const r of ranked) {
    tiers[r.richness.dome_buildability].push(r)
  }

  writeJSON(join(META_DIR, 'tiers.json'), {
    generated_at: new Date().toISOString(),
    high: { count: tiers.high.length, characters: tiers.high.slice(0, 50) },
    medium: { count: tiers.medium.length, characters: tiers.medium.slice(0, 50) },
    low: { count: tiers.low.length, characters: tiers.low.slice(0, 50) },
  })

  // Write rankings by circumstance
  const byCircumstance = {}
  for (const character of allCharacters) {
    for (const circ of character.circumstances || []) {
      if (!byCircumstance[circ]) byCircumstance[circ] = []
      byCircumstance[circ].push({
        name: character.name,
        source_work: character.source_work,
        real_or_fictional: character.real_or_fictional,
        filled_layers: character.richness?.filled_layers || 0,
      })
    }
  }

  writeJSON(join(META_DIR, 'by-circumstance.json'), {
    generated_at: new Date().toISOString(),
    circumstances: Object.entries(byCircumstance)
      .sort((a, b) => b[1].length - a[1].length)
      .map(([circ, chars]) => ({ circumstance: circ, count: chars.length, characters: chars })),
  })

  // Write rankings by source work
  const byWork = {}
  for (const character of allCharacters) {
    const work = character.source_work
    if (!byWork[work]) byWork[work] = { work, characters: [] }
    byWork[work].characters.push({
      name: character.name,
      real_or_fictional: character.real_or_fictional,
      filled_layers: character.richness?.filled_layers || 0,
      dome_buildability: character.richness?.dome_buildability,
    })
  }

  writeJSON(join(META_DIR, 'by-source-work.json'), {
    generated_at: new Date().toISOString(),
    works: Object.values(byWork)
      .sort((a, b) => b.characters.length - a.characters.length),
  })

  return {
    total: ranked.length,
    high: tiers.high.length,
    medium: tiers.medium.length,
    low: tiers.low.length,
    top_5: ranked.slice(0, 5).map(r => `${r.name} (${r.richness.filled_layers} layers)`),
  }
}

// ── Phase 3: API Discovery ────────────────────────────────────────────────────

async function runApiDiscovery(tracker) {
  if (!DISCOVERY_ENABLED) return { skipped: true, reason: 'CHARACTER_DISCOVERY=false' }

  console.log('\n  Phase 3: API Discovery')
  console.log(`    Running ${DISCOVERY_QUERIES} queries across Open Library, Gutenberg, Internet Archive...`)

  const stateFile = join(META_DIR, 'discovery-state.json')
  const results = await runDiscoverySweep({
    queriesPerSweep: DISCOVERY_QUERIES,
    delayMs: DELAY_MS,
    stateFile,
  })

  if (!results.ok) {
    console.log(`    Discovery failed: ${results.error}`)
    return { ok: false, error: results.error }
  }

  // Score and register discovered works
  let highPotential = 0
  let registered = 0

  for (const work of results.works) {
    const potential = scoreWorkForDomePotential(work)
    work.dome_potential = potential

    if (potential.potential !== 'low') {
      registerWork(tracker, work)
      registered++
      if (potential.potential === 'high') highPotential++
    }
  }

  // Save discovery state for next run
  writeJSON(stateFile, {
    lastRun: new Date().toISOString(),
    nextQueryIndex: results.nextQueryIndex,
    queriesRun: results.queries_run,
  })

  console.log(`    Discovered: ${results.works.length} works`)
  console.log(`    Registered: ${registered} (${highPotential} high potential)`)
  console.log(`    Queries run: ${results.queries_run}`)

  return {
    ok: true,
    discovered: results.works.length,
    registered,
    highPotential,
    queriesRun: results.queries_run,
    errors: results.errors?.length || 0,
  }
}

// ── Phase 4: Follow References ────────────────────────────────────────────────

function followReferences(tracker) {
  const newGenres = discoverGenres(tracker)

  console.log('\n  Phase 4: Reference Following')
  console.log(`    Reference queue: ${tracker.reference_queue.filter(r => !r.searched).length} unresolved`)
  console.log(`    Genre queue: ${tracker.genre_queue.filter(g => !g.searched).length} unresolved`)
  console.log(`    New genres discovered: ${newGenres.length}`)

  for (const genre of newGenres) {
    console.log(`      → ${genre.genre}: ${genre.works_queued} works queued`)
  }

  return {
    referenceQueue: tracker.reference_queue.filter(r => !r.searched).length,
    genreQueue: tracker.genre_queue.filter(g => !g.searched).length,
    newGenres: newGenres.length,
  }
}

// ── Main ──────────────────────────────────────────────────────────────────────

async function run() {
  console.log('\n╔══════════════════════════════════════════╗')
  console.log('║    CHARACTER FRAGMENT — Discovery Engine ║')
  console.log('╚══════════════════════════════════════════╝\n')

  const startTime = Date.now()
  ensureDirs()

  // Print source registry
  printRegistry()

  const existingCount = countExisting()
  console.log(`  Existing characters: ${existingCount.total} (${existingCount.real} real, ${existingCount.fictional} fictional)\n`)

  // Load state
  const catalog = loadCatalog()
  const tracker = loadTracker()

  // ── Phase 1: Process seed characters ──────────────────────────────────
  console.log('  Phase 1: Processing seed characters')
  const seedResults = processSeedCharacters(catalog, tracker)
  console.log(`    Processed: ${seedResults.processed}`)
  console.log(`    Skipped: ${seedResults.skipped}`)
  console.log(`    New circumstance types: ${seedResults.newCircumstanceTypes}`)

  // ── Phase 2: Build rankings ───────────────────────────────────────────
  console.log('\n  Phase 2: Building rankings')
  const rankings = buildRankings()
  console.log(`    Total ranked: ${rankings.total}`)
  console.log(`    High buildability: ${rankings.high}`)
  console.log(`    Medium buildability: ${rankings.medium}`)
  console.log(`    Low buildability: ${rankings.low}`)
  console.log(`    Top 5:`)
  for (const name of rankings.top_5) {
    console.log(`      → ${name}`)
  }

  // ── Phase 3: API Discovery ────────────────────────────────────────────
  const discoveryResults = await runApiDiscovery(tracker)

  // ── Phase 4: Follow References ────────────────────────────────────────
  const refResults = followReferences(tracker)

  // ── Save all state ────────────────────────────────────────────────────
  saveCatalog(catalog)
  saveTracker(tracker)

  // ── Write master catalog ──────────────────────────────────────────────
  const finalCount = countExisting()
  const cStats = catalogStats(catalog)
  const tStats = trackerStats(tracker)

  writeJSON(join(CHARACTERS, 'catalog.json'), {
    generated_at: new Date().toISOString(),
    characters: {
      total: finalCount.total,
      real: finalCount.real,
      fictional: finalCount.fictional,
    },
    circumstances: cStats,
    source_works: tStats,
    rankings: {
      high_buildability: rankings.high,
      medium_buildability: rankings.medium,
      low_buildability: rankings.low,
    },
  })

  const elapsed = ((Date.now() - startTime) / 1000).toFixed(1)

  console.log('\n── Results ─────────────────────────────────')
  console.log(`  Characters:        ${finalCount.total} (${finalCount.real} real, ${finalCount.fictional} fictional)`)
  console.log(`  New this run:      ${seedResults.processed}`)
  console.log(`  Circumstance types: ${cStats.total_types} (${cStats.discovered_types} discovered)`)
  console.log(`  Source works:      ${tStats.total_works}`)
  console.log(`  Reference queue:   ${tStats.reference_queue} unresolved`)
  console.log(`  Genre queue:       ${tStats.genre_queue} unresolved`)
  console.log(`  Discovery queue:   ${cStats.discovery_queue} circumstance searches`)
  console.log(`  Time:              ${elapsed}s`)
  console.log('────────────────────────────────────────────\n')

  return {
    characters: finalCount,
    seed: seedResults,
    rankings,
    discovery: discoveryResults,
    references: refResults,
    circumstances: cStats,
    source_works: tStats,
  }
}

// ── Run ───────────────────────────────────────────────────────────────────────
run().then(() => process.exit(0)).catch(err => { console.error('CHARACTER FRAGMENT FATAL:', err); process.exit(1) })
