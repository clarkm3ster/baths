#!/usr/bin/env node
/**
 * BATHS — Perpetual Discovery Loop
 *
 * Runs Fragment (data scrapers) and Talent (practitioner discovery) on a
 * continuous loop. Each subsystem discovers new sources, generates new
 * scrapers, and expands its frontier.
 *
 * Fragment discovers data sources and scrapes them.
 * Talent discovers disciplines and practitioners.
 * Both run cron-style forever.
 *
 * Usage:
 *   node src/loop.mjs                  # run both
 *   node src/loop.mjs --fragment       # fragment only
 *   node src/loop.mjs --talent         # talent only
 *   node src/loop.mjs --sphere         # sphere spaces only
 *   node src/loop.mjs --interval 120   # seconds between cycles (default 300)
 *
 * Environment:
 *   LOOP_INTERVAL=300      seconds between cycles
 *   FRAGMENT_BATCH_LIMIT=100  max scraper runs per cycle
 *
 * Eventually connect to a database. Until then, file-based.
 */

import { spawn } from 'node:child_process'
import { join, dirname } from 'node:path'
import { fileURLToPath } from 'node:url'

const __dirname = dirname(fileURLToPath(import.meta.url))

// ── Config ──────────────────────────────────────────────────────────────────
const args = process.argv.slice(2)
const runFragment = args.includes('--fragment') || (!args.includes('--talent') && !args.includes('--sphere'))
const runTalent = args.includes('--talent') || (!args.includes('--fragment') && !args.includes('--sphere'))
const runSphere = args.includes('--sphere') || (!args.includes('--fragment') && !args.includes('--talent'))

const intervalIdx = args.indexOf('--interval')
const INTERVAL = (intervalIdx >= 0 ? parseInt(args[intervalIdx + 1]) : parseInt(process.env.LOOP_INTERVAL || '300')) * 1000

let cycle = 0

// ── Run a subprocess and stream its output ──────────────────────────────────
function runScript(label, script, scriptArgs = []) {
  return new Promise((resolve) => {
    const proc = spawn('node', [script, ...scriptArgs], {
      cwd: join(__dirname, '..'),
      stdio: ['ignore', 'pipe', 'pipe'],
      env: { ...process.env },
    })

    proc.stdout.on('data', d => {
      for (const line of d.toString().split('\n').filter(Boolean)) {
        console.log(`[${label}] ${line}`)
      }
    })

    proc.stderr.on('data', d => {
      for (const line of d.toString().split('\n').filter(Boolean)) {
        console.error(`[${label}] ${line}`)
      }
    })

    proc.on('close', code => {
      resolve({ label, code })
    })

    // Safety timeout — 10 minutes max per subsystem per cycle
    setTimeout(() => {
      try { proc.kill('SIGTERM') } catch {}
      resolve({ label, code: 'timeout' })
    }, 10 * 60 * 1000)
  })
}

// ── Main loop ───────────────────────────────────────────────────────────────
async function loop() {
  console.log('\n╔══════════════════════════════════════════════════════════════╗')
  console.log('║             BATHS — Perpetual Discovery Loop                ║')
  console.log('╚══════════════════════════════════════════════════════════════╝')
  console.log(`  Fragment: ${runFragment ? 'ON' : 'off'}`)
  console.log(`  Talent:   ${runTalent ? 'ON' : 'off'}`)
  console.log(`  Sphere:   ${runSphere ? 'ON' : 'off'}`)
  console.log(`  Interval: ${INTERVAL / 1000}s`)
  console.log('')

  while (true) {
    cycle++
    const start = Date.now()
    console.log(`\n── Cycle ${cycle} ── ${new Date().toISOString()} ${'─'.repeat(30)}`)

    const tasks = []

    if (runFragment) {
      tasks.push(runScript('FRAGMENT', join(__dirname, 'fragment', 'scrape.mjs')))
    }

    if (runTalent) {
      tasks.push(runScript('TALENT', join(__dirname, 'talent', 'discover.mjs')))
    }

    if (runSphere) {
      tasks.push(runScript('SPHERE', join(__dirname, 'sphere', 'discover.mjs')))
    }

    const results = await Promise.all(tasks)

    const elapsed = ((Date.now() - start) / 1000).toFixed(1)
    console.log(`\n── Cycle ${cycle} complete (${elapsed}s) ──`)
    for (const r of results) {
      console.log(`  ${r.label}: ${r.code === 0 ? 'OK' : r.code === 'timeout' ? 'TIMEOUT' : `exit ${r.code}`}`)
    }

    console.log(`  Next cycle in ${INTERVAL / 1000}s...`)
    await new Promise(r => setTimeout(r, INTERVAL))
  }
}

loop().catch(err => {
  console.error('LOOP FATAL:', err)
  process.exit(1)
})
