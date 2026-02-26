/**
 * CHARACTER FRAGMENT — Circumstance Catalog Engine
 *
 * Tracks every type of human circumstance discovered across all characters.
 * When Character Fragment encounters a new circumstance type, it logs it
 * and searches for more characters who share it.
 *
 * The catalog grows continuously. Every circumstance type maps to dome layers,
 * tracks how many characters experience it, and identifies gaps — circumstance
 * types with few documented characters.
 */

import { readJSON, writeJSON, CIRCUMSTANCES_DIR, CIRCUMSTANCE_TYPES } from './lib.mjs'
import { join } from 'node:path'
import { existsSync, readdirSync } from 'node:fs'

// ── Load or initialize the catalog ────────────────────────────────────────────

export function loadCatalog() {
  const catalogPath = join(CIRCUMSTANCES_DIR, 'catalog.json')
  const existing = readJSON(catalogPath)
  if (existing) return existing

  // Initialize from built-in taxonomy
  const catalog = {
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString(),
    version: 0,
    types: {},
    categories: {},
    discovery_queue: [],
  }

  for (const [type, def] of Object.entries(CIRCUMSTANCE_TYPES)) {
    catalog.types[type] = {
      ...def,
      character_count: 0,
      real_count: 0,
      fictional_count: 0,
      example_characters: [],
      discovered_at: new Date().toISOString(),
      discovered_from: 'built-in taxonomy',
    }

    if (!catalog.categories[def.category]) {
      catalog.categories[def.category] = { types: [], total_characters: 0 }
    }
    catalog.categories[def.category].types.push(type)
  }

  return catalog
}

// ── Register a character's circumstances in the catalog ───────────────────────

export function registerCharacterCircumstances(catalog, character) {
  let newTypes = 0

  for (const circ of character.circumstances || []) {
    // If this circumstance type doesn't exist, create it
    if (!catalog.types[circ]) {
      catalog.types[circ] = {
        category: 'discovered',
        layers: [],
        description: `Discovered from ${character.name} in ${character.source_work}`,
        character_count: 0,
        real_count: 0,
        fictional_count: 0,
        example_characters: [],
        discovered_at: new Date().toISOString(),
        discovered_from: `${character.name} (${character.source_work})`,
      }

      if (!catalog.categories.discovered) {
        catalog.categories.discovered = { types: [], total_characters: 0 }
      }
      catalog.categories.discovered.types.push(circ)

      // Queue for meta-discovery — find more characters with this circumstance
      catalog.discovery_queue.push({
        type: circ,
        discovered_from: character.name,
        source_work: character.source_work,
        queued_at: new Date().toISOString(),
        searched: false,
      })

      newTypes++
    }

    // Update counts
    catalog.types[circ].character_count++
    if (character.real_or_fictional === 'real') {
      catalog.types[circ].real_count++
    } else {
      catalog.types[circ].fictional_count++
    }

    // Track examples (keep top 10)
    const examples = catalog.types[circ].example_characters
    if (examples.length < 10) {
      examples.push({
        name: character.name,
        source_work: character.source_work,
        real_or_fictional: character.real_or_fictional,
      })
    }

    // Update category totals
    const catName = catalog.types[circ].category
    if (catalog.categories[catName]) {
      catalog.categories[catName].total_characters++
    }
  }

  catalog.version++
  catalog.updated_at = new Date().toISOString()
  return { newTypes, catalog }
}

// ── Save the catalog ──────────────────────────────────────────────────────────

export function saveCatalog(catalog) {
  writeJSON(join(CIRCUMSTANCES_DIR, 'catalog.json'), catalog)

  // Also write per-category files for browsing
  for (const [catName, catData] of Object.entries(catalog.categories)) {
    const types = catData.types.map(t => ({
      type: t,
      ...catalog.types[t],
    })).sort((a, b) => b.character_count - a.character_count)

    writeJSON(join(CIRCUMSTANCES_DIR, `category-${catName}.json`), {
      category: catName,
      types: types.length,
      total_characters: catData.total_characters,
      entries: types,
    })
  }

  // Write gaps — circumstance types with few characters
  const gaps = Object.entries(catalog.types)
    .filter(([, t]) => t.character_count < 3)
    .sort((a, b) => a[1].character_count - b[1].character_count)
    .map(([type, data]) => ({
      type,
      category: data.category,
      character_count: data.character_count,
      description: data.description,
      layers: data.layers,
    }))

  writeJSON(join(CIRCUMSTANCES_DIR, 'gaps.json'), {
    updated_at: new Date().toISOString(),
    total_gap_types: gaps.length,
    gaps,
  })

  // Write discovery queue
  const unprocessed = catalog.discovery_queue.filter(d => !d.searched)
  writeJSON(join(CIRCUMSTANCES_DIR, 'discovery-queue.json'), {
    updated_at: new Date().toISOString(),
    total_queued: catalog.discovery_queue.length,
    unprocessed: unprocessed.length,
    queue: unprocessed,
  })
}

// ── Summary statistics ────────────────────────────────────────────────────────

export function catalogStats(catalog) {
  const types = Object.entries(catalog.types)
  const totalCharacters = types.reduce((s, [, t]) => s + t.character_count, 0)
  const totalReal = types.reduce((s, [, t]) => s + t.real_count, 0)
  const totalFictional = types.reduce((s, [, t]) => s + t.fictional_count, 0)
  const discovered = types.filter(([, t]) => t.category === 'discovered').length
  const empty = types.filter(([, t]) => t.character_count === 0).length

  return {
    total_types: types.length,
    total_characters: totalCharacters,
    real_characters: totalReal,
    fictional_characters: totalFictional,
    categories: Object.keys(catalog.categories).length,
    discovered_types: discovered,
    empty_types: empty,
    most_common: types
      .sort((a, b) => b[1].character_count - a[1].character_count)
      .slice(0, 10)
      .map(([type, data]) => ({ type, count: data.character_count })),
    discovery_queue: catalog.discovery_queue.filter(d => !d.searched).length,
  }
}
