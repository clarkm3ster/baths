#!/usr/bin/env node
/**
 * FRAGMENT — Migrate existing fragments to layer-based storage
 *
 * Moves data/fragments/{source-id}/{fips}.json
 *    to data/layer-{NN}-{name}/{source-id}/{fips}.json
 *
 * Fragments that feed multiple layers get copied to each.
 * Fragments with no layer mapping go to data/raw/.
 *
 * Run once: node src/fragment/migrate-to-layers.mjs
 */

import { readFileSync, writeFileSync, mkdirSync, existsSync, readdirSync, copyFileSync, rmSync } from 'node:fs'
import { join, dirname } from 'node:path'
import { fileURLToPath } from 'node:url'
import { readJSON, writeJSON } from './lib.mjs'
import ALL_SOURCES from './sources/index.mjs'

const __dirname = dirname(fileURLToPath(import.meta.url))
const ROOT = join(__dirname, '..', '..')
const DATA = join(ROOT, 'data')
const OLD_FRAGMENTS = join(DATA, 'fragments')

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

// Build source → layers map from registry
const sourceLayerMap = new Map()
for (const s of ALL_SOURCES) {
  sourceLayerMap.set(s.id, s.layers || [])
}

// Also map old source IDs that might not be in the new registry
// (from the original 13 scrapers)
const LEGACY_LAYER_MAP = {
  'census-demographics':      [8],
  'census-income':            [3, 6],
  'census-housing':           [5],
  'census-rent-burden':       [3, 5],
  'census-health-insurance':  [4],
  'census-disability':        [1, 4],
  'census-education':         [7],
  'census-employment':        [6],
  'census-commute':           [5, 9],
  'census-internet':          [2, 7],
  'bls-unemployment':         [6],
  'hud-fmr':                  [3, 5],
  'fema-disasters':           [5, 9],
}

function getLayersForSource(sourceId) {
  return sourceLayerMap.get(sourceId) || LEGACY_LAYER_MAP[sourceId] || []
}

console.log('\n  FRAGMENT — Migrating to layer-based storage\n')

// Create layer directories
for (const dir of Object.values(LAYER_DIRS)) {
  mkdirSync(join(DATA, dir), { recursive: true })
}
mkdirSync(join(DATA, 'raw'), { recursive: true })

if (!existsSync(OLD_FRAGMENTS)) {
  console.log('  No data/fragments/ directory — nothing to migrate.')
  process.exit(0)
}

let moved = 0
let copied = 0
let unmapped = 0

const sourceDirs = readdirSync(OLD_FRAGMENTS)
for (const sourceId of sourceDirs) {
  const sourceDir = join(OLD_FRAGMENTS, sourceId)
  let files
  try {
    files = readdirSync(sourceDir).filter(f => f.endsWith('.json'))
  } catch { continue }

  const layers = getLayersForSource(sourceId)

  for (const file of files) {
    const srcPath = join(sourceDir, file)
    const fragment = readJSON(srcPath)

    // Update fragment with layer tags if missing
    if (fragment && !fragment.layers) {
      fragment.layers = layers.length > 0 ? layers : undefined
    }

    if (layers.length === 0) {
      // No layer mapping — goes to raw/
      const dest = join(DATA, 'raw', sourceId, file)
      mkdirSync(dirname(dest), { recursive: true })
      if (fragment) {
        writeJSON(dest, fragment)
      } else {
        copyFileSync(srcPath, dest)
      }
      unmapped++
      continue
    }

    // Write to primary layer
    const primaryDest = join(DATA, LAYER_DIRS[layers[0]], sourceId, file)
    mkdirSync(dirname(primaryDest), { recursive: true })
    if (fragment) {
      writeJSON(primaryDest, fragment)
    } else {
      copyFileSync(srcPath, primaryDest)
    }
    moved++

    // Copy to additional layers
    for (let i = 1; i < layers.length; i++) {
      const dest = join(DATA, LAYER_DIRS[layers[i]], sourceId, file)
      mkdirSync(dirname(dest), { recursive: true })
      copyFileSync(primaryDest, dest)
      copied++
    }
  }
}

console.log(`  Moved:    ${moved} fragments to primary layer`)
console.log(`  Copied:   ${copied} fragments to additional layers`)
console.log(`  Unmapped: ${unmapped} fragments to raw/`)
console.log(`  Total:    ${moved + copied + unmapped} file operations`)
console.log('')

// Verify
let total = 0
for (const dir of [...Object.values(LAYER_DIRS), 'raw']) {
  const full = join(DATA, dir)
  if (!existsSync(full)) continue
  let count = 0
  for (const sub of readdirSync(full)) {
    try { count += readdirSync(join(full, sub)).filter(f => f.endsWith('.json')).length } catch {}
  }
  if (count > 0) console.log(`  ${dir}: ${count} fragments`)
  total += count
}
console.log(`\n  Total fragments in layer storage: ${total}`)

// Don't delete old fragments/ yet — user can do that manually
console.log('\n  Old data/fragments/ preserved. Remove manually when ready:')
console.log('    rm -rf data/fragments/')
console.log('')
