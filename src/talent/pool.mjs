/**
 * TALENT POOL — Unified practitioner roster
 *
 * One pool serves both DOMES and SPHERES productions.
 * Real practitioners (living and dead) profiled from actual body of work.
 * Fictional practitioners (characters from narratives) profiled from their embodied practice.
 *
 * Storage: data/talent/pool/{practitioner-id}.json
 * Index:   data/talent/index/by-discipline.json
 *          data/talent/index/by-dome-layer.json
 *          data/talent/index/by-sphere-layer.json
 *          data/talent/index/by-type.json
 *
 * The pool doesn't distinguish "dome talent" from "sphere talent."
 * A landscape architect is relevant to both.
 * A poet is relevant to both.
 * A forensic accountant is relevant to both.
 * The pool is unified. The matching is production-specific.
 */

import { join } from 'node:path'
import {
  POOL_DIR, INDEX_DIR, readJSON, writeJSON, listJSON,
  practitionerID, slugify, DOME_LAYERS, SPHERE_LAYERS
} from './lib.mjs'

// ── Practitioner schema ─────────────────────────────────────────────────────
//
// {
//   id:            string  — sha256(name::source)[:12]
//   name:          string  — full name
//   type:          'real' | 'fictional'
//   alive:         boolean | null  — for real practitioners
//
//   // Identity
//   born:          string | null  — year or date
//   died:          string | null  — year or date, null if alive
//   nationality:   string | null
//   era:           string  — "contemporary", "20th century", "ancient", etc.
//
//   // For fictional practitioners
//   source_work:   string | null  — which novel, film, show, myth
//   source_medium: string | null  — novel, film, television, game, mythology, folklore
//   creator:       string | null  — author/director/etc.
//
//   // Practice
//   discipline:    string  — primary discipline slug
//   disciplines:   string[]  — all discipline slugs
//   practice:      string  — what they do / did
//   approach:      string  — their philosophy / methodology as demonstrated
//   body_of_work:  string  — summary of actual work (real) or narrative arc (fictional)
//   why_instructive: string  — why their perspective matters for productions
//
//   // Layer mapping — unified, not segregated
//   dome_layers:   number[]  — which dome layers (1-12) their practice maps to
//   sphere_layers: number[]  — which sphere layers (1-10) their practice maps to
//   dome_relevance:   { [layer]: string }  — why relevant to each dome layer
//   sphere_relevance: { [layer]: string }  — why relevant to each sphere layer
//
//   // Metadata
//   discovered_at:   string  — ISO timestamp
//   discovery_cycle: number  — which discovery loop found them
//   tags:            string[]  — freeform tags
// }

// ── Add practitioner to pool ────────────────────────────────────────────────

export function addPractitioner(record) {
  const id = record.id || practitionerID(record.name, record.source_work || record.discipline)
  const full = {
    id,
    name: record.name,
    type: record.type || 'real',
    alive: record.alive ?? null,

    born: record.born || null,
    died: record.died || null,
    nationality: record.nationality || null,
    era: record.era || 'contemporary',

    source_work: record.source_work || null,
    source_medium: record.source_medium || null,
    creator: record.creator || null,

    discipline: record.discipline,
    disciplines: record.disciplines || [record.discipline],
    practice: record.practice,
    approach: record.approach || '',
    body_of_work: record.body_of_work || '',
    why_instructive: record.why_instructive || '',

    dome_layers: record.dome_layers || [],
    sphere_layers: record.sphere_layers || [],
    dome_relevance: record.dome_relevance || {},
    sphere_relevance: record.sphere_relevance || {},

    discovered_at: record.discovered_at || new Date().toISOString(),
    discovery_cycle: record.discovery_cycle || 0,
    tags: record.tags || [],
  }

  writeJSON(join(POOL_DIR, `${id}.json`), full)
  return full
}

// ── Read pool ───────────────────────────────────────────────────────────────

export function loadPool() {
  return listJSON(POOL_DIR).map(f => readJSON(f)).filter(Boolean)
}

export function poolSize() {
  return listJSON(POOL_DIR).length
}

export function getPractitioner(id) {
  return readJSON(join(POOL_DIR, `${id}.json`))
}

// ── Rebuild indexes ─────────────────────────────────────────────────────────

export function rebuildIndexes() {
  const pool = loadPool()

  const byDiscipline = {}
  const byDomeLayer = {}
  const bySphereLayer = {}
  const byType = { real: [], fictional: [] }

  for (const p of pool) {
    // By discipline
    for (const d of p.disciplines) {
      if (!byDiscipline[d]) byDiscipline[d] = []
      byDiscipline[d].push({ id: p.id, name: p.name, type: p.type })
    }

    // By dome layer
    for (const l of p.dome_layers) {
      if (!byDomeLayer[l]) byDomeLayer[l] = []
      byDomeLayer[l].push({ id: p.id, name: p.name, type: p.type, discipline: p.discipline })
    }

    // By sphere layer
    for (const l of p.sphere_layers) {
      if (!bySphereLayer[l]) bySphereLayer[l] = []
      bySphereLayer[l].push({ id: p.id, name: p.name, type: p.type, discipline: p.discipline })
    }

    // By type
    byType[p.type]?.push({ id: p.id, name: p.name, discipline: p.discipline })
  }

  writeJSON(join(INDEX_DIR, 'by-discipline.json'), byDiscipline)
  writeJSON(join(INDEX_DIR, 'by-dome-layer.json'), byDomeLayer)
  writeJSON(join(INDEX_DIR, 'by-sphere-layer.json'), bySphereLayer)
  writeJSON(join(INDEX_DIR, 'by-type.json'), byType)
  writeJSON(join(INDEX_DIR, 'summary.json'), {
    updated_at: new Date().toISOString(),
    total: pool.length,
    real: byType.real.length,
    fictional: byType.fictional.length,
    disciplines: Object.keys(byDiscipline).length,
    dome_layer_coverage: Object.fromEntries(
      Object.entries(byDomeLayer).map(([k, v]) => [k, v.length])
    ),
    sphere_layer_coverage: Object.fromEntries(
      Object.entries(bySphereLayer).map(([k, v]) => [k, v.length])
    ),
  })

  return { total: pool.length, disciplines: Object.keys(byDiscipline).length }
}
