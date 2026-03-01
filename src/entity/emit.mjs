/**
 * ENTITY — CSV Emitter
 *
 * Writes resolved entity records to lifecycle CSV format.
 * One CSV per archetype, rows = counties.
 * Also emits a combined CSV with all archetypes × counties.
 */

import { writeFileSync, mkdirSync } from 'node:fs'
import { join, dirname } from 'node:path'
import { ALL_COLUMNS } from './schema.mjs'

/**
 * Convert a resolved record to a CSV row.
 * Handles quoting for fields containing commas.
 */
function recordToRow(record) {
  return ALL_COLUMNS.map(col => {
    const val = record[col]
    if (val === null || val === undefined) return ''
    const str = String(val)
    // Quote if contains comma, newline, or double quote
    if (str.includes(',') || str.includes('\n') || str.includes('"')) {
      return `"${str.replace(/"/g, '""')}"`
    }
    return str
  }).join(',')
}

/**
 * Write resolved records to CSV.
 *
 * @param {Array} results — from resolveAll()
 * @param {string} outDir — output directory
 */
export function writeCSV(results, outDir) {
  mkdirSync(outDir, { recursive: true })

  const header = ALL_COLUMNS.join(',')

  // ── Combined CSV: all archetypes × counties ────────────────
  const allRows = [header]
  for (const { record } of results) {
    allRows.push(recordToRow(record))
  }
  const combinedPath = join(outDir, 'all-entities.csv')
  writeFileSync(combinedPath, allRows.join('\n') + '\n')

  // ── Per-archetype CSVs ─────────────────────────────────────
  const byArchetype = {}
  for (const result of results) {
    const id = result.archetype_id
    if (!byArchetype[id]) byArchetype[id] = [header]
    byArchetype[id].push(recordToRow(result.record))
  }

  for (const [id, rows] of Object.entries(byArchetype)) {
    const path = join(outDir, `${id}.csv`)
    writeFileSync(path, rows.join('\n') + '\n')
  }

  return {
    combined: combinedPath,
    archetypes: Object.keys(byArchetype),
    total_records: results.length,
  }
}

/**
 * Write a summary JSON alongside the CSVs.
 */
export function writeSummary(results, outDir) {
  const summary = {
    generated_at: new Date().toISOString(),
    total_records: results.length,
    archetypes: [...new Set(results.map(r => r.archetype_id))],
    counties: [...new Set(results.map(r => r.fips))],
    columns: ALL_COLUMNS.length,

    // Aggregate stats
    avg_net_fiscal_impact: Math.round(
      results.reduce((s, r) => s + r.record.net_fiscal_impact, 0) / results.length
    ),
    avg_total_taxes: Math.round(
      results.reduce((s, r) => s + r.record.total_taxes_fees_paid, 0) / results.length
    ),
    avg_total_benefits: Math.round(
      results.reduce((s, r) => s + r.record.total_direct_benefits, 0) / results.length
    ),
    avg_total_services: Math.round(
      results.reduce((s, r) => s + r.record.total_direct_services, 0) / results.length
    ),
    avg_total_collective: Math.round(
      results.reduce((s, r) => s + r.record.total_collective_allocated, 0) / results.length
    ),
    avg_fragments_used: Math.round(
      results.reduce((s, r) => s + r.fragments_used, 0) / results.length
    ),

    // Per archetype
    by_archetype: {},
  }

  for (const id of summary.archetypes) {
    const rows = results.filter(r => r.archetype_id === id)
    summary.by_archetype[id] = {
      records: rows.length,
      avg_taxes: Math.round(rows.reduce((s, r) => s + r.record.total_taxes_fees_paid, 0) / rows.length),
      avg_benefits: Math.round(rows.reduce((s, r) => s + r.record.total_direct_benefits, 0) / rows.length),
      avg_net: Math.round(rows.reduce((s, r) => s + r.record.net_fiscal_impact, 0) / rows.length),
    }
  }

  const path = join(outDir, 'summary.json')
  writeFileSync(path, JSON.stringify(summary, null, 2) + '\n')
  return summary
}
