/**
 * SPHERE FRAGMENT — Shared utilities
 *
 * File I/O, state/municipality lookups, data source patterns
 * for the public space discovery engine.
 */

import { readFileSync, writeFileSync, mkdirSync, existsSync, readdirSync, statSync } from 'node:fs'
import { join, dirname } from 'node:path'
import { fileURLToPath } from 'node:url'
import { createHash } from 'node:crypto'

const __dirname = dirname(fileURLToPath(import.meta.url))
export const ROOT = join(__dirname, '..', '..')
export const DATA = join(ROOT, 'data')

// ── Directories ─────────────────────────────────────────────────────────────
export const SPACES_DIR = join(DATA, 'sphere-spaces')
export const TYPES_DIR = join(DATA, 'sphere-types')
export const GAPS_DIR = join(DATA, 'sphere-gaps')
export const SCRAPERS_DIR = join(__dirname, 'scrapers')
export const QUEUE_DIR = join(DATA, 'sphere-queue')
export const REPORTS_DIR = join(DATA, 'sphere-reports')
export const META_DIR = join(DATA, 'sphere-meta')

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

export function listDirs(dir) {
  if (!existsSync(dir)) return []
  return readdirSync(dir).filter(f => {
    try { return statSync(join(dir, f)).isDirectory() } catch { return false }
  })
}

// ── Safe fetch ──────────────────────────────────────────────────────────────
export async function safeFetch(url, label, options = {}) {
  try {
    const controller = new AbortController()
    const timeout = setTimeout(() => controller.abort(), options.timeout || 30000)
    const fetchOpts = {
      signal: controller.signal,
      headers: { 'User-Agent': 'BATHS-SphereFragment/1.0', ...options.headers },
    }
    const res = await fetch(url, fetchOpts)
    clearTimeout(timeout)
    if (!res.ok) return { ok: false, error: `HTTP ${res.status}`, status: res.status }
    const text = await res.text()
    try { return { ok: true, data: JSON.parse(text) } }
    catch { return { ok: true, data: text, format: 'text' } }
  } catch (err) {
    return { ok: false, error: err.message }
  }
}

export const delay = ms => new Promise(r => setTimeout(r, ms))

// ── Slugify ─────────────────────────────────────────────────────────────────
export function slugify(str) {
  return str.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, '')
}

export function spaceID(name, address, municipality) {
  const input = `${name}::${address}::${municipality}`
  return createHash('sha256').update(input).digest('hex').slice(0, 16)
}

// ── State abbreviations ─────────────────────────────────────────────────────
export const STATE_ABBREV = {
  'AL': 'Alabama', 'AK': 'Alaska', 'AZ': 'Arizona', 'AR': 'Arkansas',
  'CA': 'California', 'CO': 'Colorado', 'CT': 'Connecticut', 'DE': 'Delaware',
  'DC': 'District of Columbia', 'FL': 'Florida', 'GA': 'Georgia', 'HI': 'Hawaii',
  'ID': 'Idaho', 'IL': 'Illinois', 'IN': 'Indiana', 'IA': 'Iowa',
  'KS': 'Kansas', 'KY': 'Kentucky', 'LA': 'Louisiana', 'ME': 'Maine',
  'MD': 'Maryland', 'MA': 'Massachusetts', 'MI': 'Michigan', 'MN': 'Minnesota',
  'MS': 'Mississippi', 'MO': 'Missouri', 'MT': 'Montana', 'NE': 'Nebraska',
  'NV': 'Nevada', 'NH': 'New Hampshire', 'NJ': 'New Jersey', 'NM': 'New Mexico',
  'NY': 'New York', 'NC': 'North Carolina', 'ND': 'North Dakota', 'OH': 'Ohio',
  'OK': 'Oklahoma', 'OR': 'Oregon', 'PA': 'Pennsylvania', 'RI': 'Rhode Island',
  'SC': 'South Carolina', 'SD': 'South Dakota', 'TN': 'Tennessee', 'TX': 'Texas',
  'UT': 'Utah', 'VT': 'Vermont', 'VA': 'Virginia', 'WA': 'Washington',
  'WV': 'West Virginia', 'WI': 'Wisconsin', 'WY': 'Wyoming',
}

export const STATE_FIPS = {
  '01': 'AL', '02': 'AK', '04': 'AZ', '05': 'AR', '06': 'CA',
  '08': 'CO', '09': 'CT', '10': 'DE', '11': 'DC', '12': 'FL',
  '13': 'GA', '15': 'HI', '16': 'ID', '17': 'IL', '18': 'IN',
  '19': 'IA', '20': 'KS', '21': 'KY', '22': 'LA', '23': 'ME',
  '24': 'MD', '25': 'MA', '26': 'MI', '27': 'MN', '28': 'MS',
  '29': 'MO', '30': 'MT', '31': 'NE', '32': 'NV', '33': 'NH',
  '34': 'NJ', '35': 'NM', '36': 'NY', '37': 'NC', '38': 'ND',
  '39': 'OH', '40': 'OK', '41': 'OR', '42': 'PA', '44': 'RI',
  '45': 'SC', '46': 'SD', '47': 'TN', '48': 'TX', '49': 'UT',
  '50': 'VT', '51': 'VA', '53': 'WA', '54': 'WV', '55': 'WI',
  '56': 'WY',
}

// ── Prioritization tiers ────────────────────────────────────────────────────
export const PRIORITY = {
  TIER_1: 'open-data-portal',        // Cities with open data portals
  TIER_2: 'large-city-no-portal',    // 100k+ pop, no portal
  TIER_3: 'medium-city',             // 25k-100k pop
  TIER_4: 'small-city',              // <25k pop
}

// ── Sphere schema layer numbers ─────────────────────────────────────────────
export const SPHERE_LAYERS = {
  1: 'Parcel',
  2: 'Infrastructure',
  3: 'Environmental',
  4: 'Economic',
  5: 'Social',
  6: 'Temporal',
  7: 'Activation',
  8: 'Permanence',
  9: 'Policy',
  10: 'Catalyst',
}
