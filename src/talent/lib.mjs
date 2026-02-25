/**
 * TALENT — Shared utilities
 *
 * File I/O, ID generation, layer constants for the unified talent pool.
 */

import { readFileSync, writeFileSync, mkdirSync, existsSync, readdirSync } from 'node:fs'
import { join, dirname } from 'node:path'
import { fileURLToPath } from 'node:url'
import { createHash } from 'node:crypto'

const __dirname = dirname(fileURLToPath(import.meta.url))
export const ROOT = join(__dirname, '..', '..')
export const POOL_DIR = join(ROOT, 'data', 'talent', 'pool')
export const DISCIPLINES_DIR = join(ROOT, 'data', 'talent', 'disciplines')
export const DISCOVERY_DIR = join(ROOT, 'data', 'talent', 'discovery-log')
export const INDEX_DIR = join(ROOT, 'data', 'talent', 'index')

// ── Dome layers (person-centered) ───────────────────────────────────────────
export const DOME_LAYERS = {
  1:  { name: 'Legal',       description: 'every right, every entitlement, every pathway' },
  2:  { name: 'Systems',     description: 'every government system, every portal, every form' },
  3:  { name: 'Fiscal',      description: 'every cost, every saving, every financial instrument' },
  4:  { name: 'Health',      description: 'every diagnosis, every treatment, every trajectory' },
  5:  { name: 'Housing',     description: 'every structure, every system, every environment' },
  6:  { name: 'Economic',    description: 'every job, every skill, every income path' },
  7:  { name: 'Education',   description: 'every credential, every learning path, every opportunity' },
  8:  { name: 'Community',   description: 'every connection, every asset, every risk' },
  9:  { name: 'Environment', description: 'every sensor, every reading, every exposure' },
  10: { name: 'Autonomy',    description: 'what autonomy means for THIS person' },
  11: { name: 'Creativity',  description: 'how THIS person makes meaning' },
  12: { name: 'Flourishing', description: 'what flourishing looks like HERE' },
}

// ── Sphere layers (place-centered) ──────────────────────────────────────────
export const SPHERE_LAYERS = {
  1:  { name: 'Parcel',          description: 'ownership, zoning, boundaries, regulatory landscape' },
  2:  { name: 'Infrastructure',  description: 'utilities, structures, connectivity, access' },
  3:  { name: 'Environmental',   description: 'soil, air, water, ecology, microclimate' },
  4:  { name: 'Economic',        description: 'value, revenue, tax, financial instruments' },
  5:  { name: 'Social',          description: 'demographics, foot traffic, community assets' },
  6:  { name: 'Temporal',        description: 'history, seasons, time-of-day dynamics' },
  7:  { name: 'Activation',      description: 'what happens in this space' },
  8:  { name: 'Permanence',      description: 'what lasting elements remain' },
  9:  { name: 'Policy',          description: 'what regulatory changes this inspires' },
  10: { name: 'Catalyst',        description: 'what adjacent activations this sparks' },
}

// ── File I/O ────────────────────────────────────────────────────────────────
export function readJSON(path) {
  try { return JSON.parse(readFileSync(path, 'utf8')) } catch { return null }
}

export function writeJSON(path, data) {
  mkdirSync(dirname(path), { recursive: true })
  writeFileSync(path, JSON.stringify(data, null, 2) + '\n')
}

export function listJSON(dir) {
  if (!existsSync(dir)) return []
  return readdirSync(dir).filter(f => f.endsWith('.json')).map(f => join(dir, f))
}

// ── ID generation ───────────────────────────────────────────────────────────
export function slugify(str) {
  return str.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, '')
}

export function practitionerID(name, source) {
  const input = `${name}::${source || 'unknown'}`
  return createHash('sha256').update(input).digest('hex').slice(0, 12)
}

export function disciplineID(name) {
  return slugify(name)
}
