#!/usr/bin/env node
/**
 * ENTITY — Resolution Runner
 *
 * Resolves all archetypes × counties into lifecycle CSV records.
 *
 * Usage:
 *   node src/entity/run.mjs              # resolve all
 *   node src/entity/run.mjs marcus       # single archetype
 *   node src/entity/run.mjs --fips 42101 # single county
 *
 * Output: data/entities/
 *   all-entities.csv    — every archetype × county
 *   marcus.csv          — one archetype, all counties
 *   summary.json        — aggregate statistics
 */

import { join, dirname } from 'node:path'
import { fileURLToPath } from 'node:url'
import { resolveEntity, resolveAll, ARCHETYPES, COUNTIES } from './resolve.mjs'
import { writeCSV, writeSummary } from './emit.mjs'

const __dirname = dirname(fileURLToPath(import.meta.url))
const OUT_DIR = join(__dirname, '..', '..', 'data', 'entities')

async function run() {
  const args = process.argv.slice(2)
  const year = new Date().getFullYear()

  console.log('\n╔══════════════════════════════════════════╗')
  console.log('║       ENTITY — Resolution Engine         ║')
  console.log('╚══════════════════════════════════════════╝\n')

  console.log(`  Year:       ${year}`)
  console.log(`  Archetypes: ${ARCHETYPES.length}`)
  console.log(`  Counties:   ${COUNTIES.length}`)
  console.log(`  Output:     data/entities/\n`)

  let results

  // Filter by archetype or FIPS if args provided
  const fipsArg = args.includes('--fips') ? args[args.indexOf('--fips') + 1] : null
  const archetypeArg = args.find(a => !a.startsWith('--') && a !== fipsArg)

  const archetypes = archetypeArg
    ? ARCHETYPES.filter(a => a.id === archetypeArg)
    : ARCHETYPES

  const counties = fipsArg
    ? COUNTIES.filter(c => c.fips === fipsArg)
    : COUNTIES

  if (archetypeArg && archetypes.length === 0) {
    console.error(`Unknown archetype: ${archetypeArg}`)
    console.error(`Available: ${ARCHETYPES.map(a => a.id).join(', ')}`)
    process.exit(1)
  }

  if (fipsArg && counties.length === 0) {
    console.error(`Unknown FIPS: ${fipsArg}`)
    process.exit(1)
  }

  console.log(`  Resolving ${archetypes.length} archetypes × ${counties.length} counties...\n`)

  results = []
  let count = 0

  for (const county of counties) {
    for (const archetype of archetypes) {
      const state = extractState(county)
      const { record, fragments_used } = resolveEntity(
        { ...archetype, state },
        { ...county, state },
        year
      )
      results.push({
        archetype_id: archetype.id,
        fips: county.fips,
        record,
        fragments_used,
      })
      count++

      // Print one-line summary
      const net = record.net_fiscal_impact
      const sign = net >= 0 ? '+' : ''
      const taxes = record.total_taxes_fees_paid
      const benefits = record.total_direct_benefits
      process.stdout.write(
        `  [${archetype.id.padEnd(7)}][${county.fips}] ` +
        `taxes=$${taxes.toLocaleString().padStart(7)} ` +
        `benefits=$${benefits.toLocaleString().padStart(7)} ` +
        `net=${sign}$${net.toLocaleString().padStart(8)} ` +
        `(${fragments_used} fragments)\n`
      )
    }
  }

  // Write output
  console.log('\n── Writing CSV ─────────────────────────────')
  const csvResult = writeCSV(results, OUT_DIR)
  console.log(`  Combined:   ${csvResult.combined}`)
  console.log(`  Archetypes: ${csvResult.archetypes.join(', ')}`)
  console.log(`  Records:    ${csvResult.total_records}`)

  const summary = writeSummary(results, OUT_DIR)
  console.log('\n── Summary ─────────────────────────────────')
  console.log(`  Avg taxes paid:         $${summary.avg_total_taxes.toLocaleString()}`)
  console.log(`  Avg benefits received:  $${summary.avg_total_benefits.toLocaleString()}`)
  console.log(`  Avg services consumed:  $${summary.avg_total_services.toLocaleString()}`)
  console.log(`  Avg collective share:   $${summary.avg_total_collective.toLocaleString()}`)
  console.log(`  Avg net fiscal impact:  $${summary.avg_net_fiscal_impact.toLocaleString()}`)
  console.log(`  Avg fragments resolved: ${summary.avg_fragments_used}`)

  console.log('\n  By archetype:')
  for (const [id, stats] of Object.entries(summary.by_archetype)) {
    const net = stats.avg_net
    const sign = net >= 0 ? '+' : ''
    console.log(`    ${id.padEnd(10)} taxes=$${stats.avg_taxes.toLocaleString().padStart(7)}  benefits=$${stats.avg_benefits.toLocaleString().padStart(7)}  net=${sign}$${net.toLocaleString().padStart(8)}`)
  }

  console.log('\n────────────────────────────────────────────\n')
}

function extractState(county) {
  const match = county.name.match(/,\s*([A-Z]{2})$/)
  if (match) return match[1]
  if (county.fips === '11001') return 'DC'
  return ''
}

run().catch(err => { console.error('ENTITY FATAL:', err); process.exit(1) })
