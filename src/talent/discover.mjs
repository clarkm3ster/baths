#!/usr/bin/env node
/**
 * TALENT DISCOVERY ENGINE — Perpetual meta-scraper
 *
 * This is the talent equivalent of Fragment's agent.mjs.
 * Claude IS the intelligence layer. This script is the execution pipeline.
 *
 * It runs on a loop forever:
 *   1. LOAD — read discipline queue + existing pool
 *   2. DISCOVER — for each discipline, discover real + fictional practitioners
 *   3. REGISTER — add practitioners to pool, rebuild indexes
 *   4. EXPAND — discover adjacent disciplines from what was found
 *   5. LOG — write discovery report
 *   6. WAIT — sleep, then loop
 *
 * Claude writes discipline definitions to data/talent/discovery-queue/
 * Each file: { discipline, description, dome_relevance, sphere_relevance, seed_practitioners }
 *
 * The engine reads them, processes them, and expands the frontier.
 *
 * Run:  node src/talent/discover.mjs
 * Loop: node src/talent/discover.mjs --loop
 * Single discipline: node src/talent/discover.mjs --discipline "forensic-accounting"
 */

import { readFileSync, writeFileSync, mkdirSync, existsSync, readdirSync, renameSync } from 'node:fs'
import { join, dirname, basename } from 'node:path'
import { fileURLToPath } from 'node:url'
import {
  ROOT, POOL_DIR, DISCIPLINES_DIR, DISCOVERY_DIR, INDEX_DIR,
  readJSON, writeJSON, listJSON, slugify, disciplineID
} from './lib.mjs'
import { addPractitioner, loadPool, poolSize, rebuildIndexes } from './pool.mjs'

const __dirname = dirname(fileURLToPath(import.meta.url))
const QUEUE_DIR = join(ROOT, 'data', 'talent', 'discovery-queue')
const PROCESSED_DIR = join(ROOT, 'data', 'talent', 'discovery-queue', 'processed')
const LOOP_INTERVAL = 60 * 1000 // 60 seconds between cycles

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
//  PHASE 1: LOAD — read discipline queue + existing pool state
// ═══════════════════════════════════════════════════════════════════════════

function loadQueue(singleDiscipline) {
  P.phase(1, 'LOAD')

  mkdirSync(QUEUE_DIR, { recursive: true })
  mkdirSync(PROCESSED_DIR, { recursive: true })

  if (singleDiscipline) {
    const path = join(QUEUE_DIR, `${slugify(singleDiscipline)}.json`)
    if (!existsSync(path)) {
      P.fail(`No queue file for "${singleDiscipline}" at ${path}`)
      return []
    }
    P.ok(`Single discipline mode: ${singleDiscipline}`)
    return [readJSON(path)].filter(Boolean)
  }

  const files = readdirSync(QUEUE_DIR)
    .filter(f => f.endsWith('.json') && !f.startsWith('.'))

  if (files.length === 0) {
    P.info('Queue empty — nothing to discover')
    return []
  }

  const queue = files.map(f => readJSON(join(QUEUE_DIR, f))).filter(Boolean)
  P.ok(`Queue: ${queue.length} disciplines`)
  P.ok(`Pool: ${poolSize()} practitioners`)
  return queue
}

// ═══════════════════════════════════════════════════════════════════════════
//  PHASE 2: DISCOVER — process each discipline's practitioners
// ═══════════════════════════════════════════════════════════════════════════

function discoverFromDiscipline(disciplineDef) {
  P.phase(2, `DISCOVER: ${disciplineDef.discipline}`)

  const slug = disciplineID(disciplineDef.discipline)
  const practitioners = disciplineDef.practitioners || []

  if (practitioners.length === 0) {
    P.info('No practitioners defined — Claude needs to populate this discipline')
    return { registered: 0, skipped: 0, discipline: slug }
  }

  P.step(`Processing ${practitioners.length} practitioners in "${disciplineDef.discipline}"`)

  let registered = 0
  let skipped = 0

  // Load existing IDs to avoid duplicates
  const existingPool = loadPool()
  const existingNames = new Set(existingPool.map(p => p.name.toLowerCase()))

  for (const p of practitioners) {
    if (existingNames.has(p.name.toLowerCase())) {
      P.info(`  skip: ${p.name} (already in pool)`)
      skipped++
      continue
    }

    const record = addPractitioner({
      ...p,
      discipline: slug,
      disciplines: [slug, ...(p.disciplines || []).map(disciplineID)],
      discovery_cycle: cycleCount,
    })

    P.ok(`  ${record.type === 'fictional' ? '📖' : '👤'} ${record.name} → dome[${record.dome_layers.join(',')}] sphere[${record.sphere_layers.join(',')}]`)
    registered++
    existingNames.add(record.name.toLowerCase())
  }

  // Save discipline definition
  writeJSON(join(DISCIPLINES_DIR, `${slug}.json`), {
    id: slug,
    discipline: disciplineDef.discipline,
    description: disciplineDef.description || '',
    dome_relevance: disciplineDef.dome_relevance || {},
    sphere_relevance: disciplineDef.sphere_relevance || {},
    practitioner_count: registered,
    discovered_at: new Date().toISOString(),
    cycle: cycleCount,
  })

  P.blank()
  P.ok(`Registered: ${registered} | Skipped: ${skipped}`)
  return { registered, skipped, discipline: slug }
}

// ═══════════════════════════════════════════════════════════════════════════
//  PHASE 3: REGISTER — rebuild indexes after all discoveries
// ═══════════════════════════════════════════════════════════════════════════

function registerAndIndex() {
  P.phase(3, 'INDEX')
  const result = rebuildIndexes()
  P.ok(`Pool: ${result.total} practitioners across ${result.disciplines} disciplines`)
  return result
}

// ═══════════════════════════════════════════════════════════════════════════
//  PHASE 4: EXPAND — move processed, log what's left to discover
// ═══════════════════════════════════════════════════════════════════════════

function expandAndArchive(queue) {
  P.phase(4, 'EXPAND')

  for (const def of queue) {
    const slug = slugify(def.discipline)
    const srcPath = join(QUEUE_DIR, `${slug}.json`)
    const destPath = join(PROCESSED_DIR, `${slug}.json`)

    if (existsSync(srcPath)) {
      renameSync(srcPath, destPath)
      P.ok(`Archived: ${slug}`)
    }

    // If the discipline definition includes adjacent_disciplines, queue them
    if (def.adjacent_disciplines?.length > 0) {
      for (const adj of def.adjacent_disciplines) {
        const adjSlug = slugify(adj.discipline || adj)
        const adjPath = join(QUEUE_DIR, `${adjSlug}.json`)
        const processedPath = join(PROCESSED_DIR, `${adjSlug}.json`)

        if (!existsSync(adjPath) && !existsSync(processedPath)) {
          // Write a skeleton for Claude to fill on next cycle
          writeJSON(adjPath, {
            discipline: adj.discipline || adj,
            description: adj.description || `Adjacent to ${def.discipline}. Needs practitioners.`,
            dome_relevance: adj.dome_relevance || {},
            sphere_relevance: adj.sphere_relevance || {},
            adjacent_disciplines: [],
            practitioners: [],
            queued_by: def.discipline,
            queued_at: new Date().toISOString(),
          })
          P.ok(`Queued adjacent: ${adjSlug}`)
        }
      }
    }
  }
}

// ═══════════════════════════════════════════════════════════════════════════
//  PHASE 5: REPORT
// ═══════════════════════════════════════════════════════════════════════════

function writeReport(queue, results, indexResult) {
  P.phase(5, 'REPORT')

  const report = {
    cycle: cycleCount,
    timestamp: new Date().toISOString(),
    disciplines_processed: queue.length,
    results: results.map(r => ({
      discipline: r.discipline,
      registered: r.registered,
      skipped: r.skipped,
    })),
    total_registered: results.reduce((s, r) => s + r.registered, 0),
    total_skipped: results.reduce((s, r) => s + r.skipped, 0),
    pool_size: indexResult.total,
    discipline_count: indexResult.disciplines,
    remaining_queue: readdirSync(QUEUE_DIR)
      .filter(f => f.endsWith('.json') && !f.startsWith('.')).length,
  }

  mkdirSync(DISCOVERY_DIR, { recursive: true })
  writeJSON(join(DISCOVERY_DIR, `cycle-${cycleCount}-${Date.now()}.json`), report)

  console.log(`
  Cycle:               ${cycleCount}
  Disciplines:         ${queue.length}
  Practitioners added: ${report.total_registered}
  Duplicates skipped:  ${report.total_skipped}
  Pool size:           ${report.pool_size}
  Total disciplines:   ${report.discipline_count}
  Queue remaining:     ${report.remaining_queue}
`)

  return report
}

// ═══════════════════════════════════════════════════════════════════════════
//  MAIN LOOP
// ═══════════════════════════════════════════════════════════════════════════

async function runCycle(singleDiscipline) {
  cycleCount++
  console.log('\n╔══════════════════════════════════════════════════════════════╗')
  console.log('║            TALENT DISCOVERY ENGINE — Cycle ' + String(cycleCount).padStart(4) + '             ║')
  console.log('╚══════════════════════════════════════════════════════════════╝')

  const queue = loadQueue(singleDiscipline)
  if (queue.length === 0) return { empty: true }

  const results = []
  for (const def of queue) {
    results.push(discoverFromDiscipline(def))
  }

  const indexResult = registerAndIndex()
  expandAndArchive(queue)
  return writeReport(queue, results, indexResult)
}

async function loop() {
  console.log('TALENT DISCOVERY — Perpetual loop mode')
  console.log(`Checking queue every ${LOOP_INTERVAL / 1000}s\n`)

  while (true) {
    const result = await runCycle()
    if (result.empty) {
      console.log(`  [${new Date().toISOString()}] Queue empty. Waiting for Claude to add disciplines...`)
    }
    await new Promise(r => setTimeout(r, LOOP_INTERVAL))
  }
}

// ── CLI ─────────────────────────────────────────────────────────────────────

const args = process.argv.slice(2)
const loopMode = args.includes('--loop')
const disciplineIdx = args.indexOf('--discipline')
const singleDiscipline = disciplineIdx >= 0 ? args[disciplineIdx + 1] : null

if (loopMode) {
  loop().catch(err => { console.error('FATAL:', err); process.exit(1) })
} else {
  runCycle(singleDiscipline).then(r => {
    process.exit(r.empty ? 0 : (r.total_registered > 0 ? 0 : 1))
  }).catch(err => { console.error('FATAL:', err); process.exit(1) })
}
