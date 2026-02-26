/**
 * CHARACTER FRAGMENT — Shared Utilities
 *
 * Dome layer definitions, circumstance taxonomy, character schema,
 * and helpers for the character discovery engine.
 */

import { readFileSync, writeFileSync, mkdirSync, existsSync, readdirSync } from 'node:fs'
import { join, dirname } from 'node:path'
import { fileURLToPath } from 'node:url'

const __dirname = dirname(fileURLToPath(import.meta.url))
export const ROOT = join(__dirname, '..', '..')
export const DATA = join(ROOT, 'data')
export const CHARACTERS = join(DATA, 'characters')
export const REAL_DIR = join(CHARACTERS, 'real')
export const FICTIONAL_DIR = join(CHARACTERS, 'fictional')
export const CIRCUMSTANCES_DIR = join(CHARACTERS, 'circumstances-catalog')
export const SOURCE_WORKS_DIR = join(CHARACTERS, 'source-works')
export const META_DIR = join(CHARACTERS, 'meta')

// ── File I/O ──────────────────────────────────────────────────────────────────

export function readJSON(path) {
  try {
    return JSON.parse(readFileSync(path, 'utf8'))
  } catch {
    return null
  }
}

export function writeJSON(path, data) {
  mkdirSync(dirname(path), { recursive: true })
  writeFileSync(path, JSON.stringify(data, null, 2) + '\n')
}

export const delay = ms => new Promise(r => setTimeout(r, ms))

// ── Safe fetch ────────────────────────────────────────────────────────────────

export async function safeFetch(url, label, options = {}) {
  try {
    const controller = new AbortController()
    const timeout = setTimeout(() => controller.abort(), options.timeout || 30000)
    const fetchOpts = { signal: controller.signal, ...options }
    delete fetchOpts.timeout
    if (!fetchOpts.headers) fetchOpts.headers = {}
    if (!fetchOpts.headers['User-Agent']) fetchOpts.headers['User-Agent'] = 'BATHS-CharacterFragment/1.0'
    const res = await fetch(url, fetchOpts)
    clearTimeout(timeout)
    if (!res.ok) return { ok: false, error: `HTTP ${res.status}`, status: res.status }
    const text = await res.text()
    try {
      return { ok: true, data: JSON.parse(text) }
    } catch {
      return { ok: true, data: text, format: 'text' }
    }
  } catch (err) {
    return { ok: false, error: err.message }
  }
}

// ── The 12 Dome Layers ────────────────────────────────────────────────────────

export const DOME_LAYERS = {
  1:  { name: 'Legal',       type: 'ai',    description: 'Rights, entitlements, legal entanglements, criminal justice involvement' },
  2:  { name: 'Systems',     type: 'ai',    description: 'Government portals, forms, bureaucratic navigation, case management' },
  3:  { name: 'Fiscal',      type: 'ai',    description: 'Income, costs, debt, benefits, financial instruments' },
  4:  { name: 'Health',      type: 'ai',    description: 'Physical health, mental health, disability, addiction, healthcare access' },
  5:  { name: 'Housing',     type: 'ai',    description: 'Shelter, homelessness, housing instability, eviction, displacement' },
  6:  { name: 'Economic',    type: 'ai',    description: 'Employment, unemployment, wages, economic mobility, poverty' },
  7:  { name: 'Education',   type: 'ai',    description: 'Schooling, literacy, credentials, learning barriers, opportunities' },
  8:  { name: 'Community',   type: 'ai',    description: 'Social networks, isolation, belonging, neighborhood, social capital' },
  9:  { name: 'Environment', type: 'ai',    description: 'Physical environment, pollution, climate exposure, infrastructure' },
  10: { name: 'Autonomy',    type: 'human', description: 'Self-determination, agency, dignity, freedom of movement' },
  11: { name: 'Creativity',  type: 'human', description: 'Expression, meaning-making, art, culture, identity' },
  12: { name: 'Flourishing', type: 'human', description: 'What thriving looks like for this person — philosophy, vitality, purpose' },
}

// ── Circumstance Taxonomy ─────────────────────────────────────────────────────
// Starting taxonomy. Character Fragment expands this as it discovers new types.

export const CIRCUMSTANCE_TYPES = {
  // Housing
  homeless: { category: 'housing', layers: [5, 3, 8], description: 'Without stable housing' },
  evicted: { category: 'housing', layers: [5, 1, 3], description: 'Forcibly removed from housing' },
  displaced: { category: 'housing', layers: [5, 8, 9], description: 'Displaced from home by force, disaster, or policy' },
  housing_insecure: { category: 'housing', layers: [5, 3], description: 'Unstable housing, at risk of loss' },
  institutionalized: { category: 'housing', layers: [5, 1, 10], description: 'Living in an institution (nursing home, group home, etc.)' },
  shelter: { category: 'housing', layers: [5, 2], description: 'Living in emergency shelter' },

  // Legal/Criminal Justice
  incarcerated: { category: 'legal', layers: [1, 5, 10], description: 'Currently in prison or jail' },
  formerly_incarcerated: { category: 'legal', layers: [1, 6, 5], description: 'Previously incarcerated, navigating reentry' },
  on_probation: { category: 'legal', layers: [1, 10], description: 'Under supervised probation' },
  undocumented: { category: 'legal', layers: [1, 6, 4], description: 'Without legal immigration status' },
  asylum_seeker: { category: 'legal', layers: [1, 5, 4], description: 'Seeking asylum or refugee status' },
  detained: { category: 'legal', layers: [1, 5, 10], description: 'In immigration or other detention' },
  wrongly_convicted: { category: 'legal', layers: [1, 10, 12], description: 'Convicted of crime they did not commit' },

  // Health
  chronic_illness: { category: 'health', layers: [4, 3, 6], description: 'Living with chronic disease' },
  mental_illness: { category: 'health', layers: [4, 10, 8], description: 'Living with mental health condition' },
  disability: { category: 'health', layers: [4, 10, 6], description: 'Physical or cognitive disability' },
  addiction: { category: 'health', layers: [4, 1, 8], description: 'Substance use disorder' },
  terminal_illness: { category: 'health', layers: [4, 12, 3], description: 'Facing terminal diagnosis' },
  uninsured: { category: 'health', layers: [4, 3, 2], description: 'Without health insurance' },
  trauma: { category: 'health', layers: [4, 10, 11], description: 'Surviving significant trauma' },

  // Economic
  poverty: { category: 'economic', layers: [6, 3, 5], description: 'Living in poverty' },
  deep_poverty: { category: 'economic', layers: [6, 3, 5], description: 'Living below 50% of poverty line' },
  working_poor: { category: 'economic', layers: [6, 3, 5], description: 'Working but still in poverty' },
  unemployed: { category: 'economic', layers: [6, 3, 8], description: 'Without employment' },
  debt: { category: 'economic', layers: [3, 6, 1], description: 'Significant debt burden' },
  benefits_cliff: { category: 'economic', layers: [6, 3, 2], description: 'Earning just enough to lose benefits' },
  wealth: { category: 'economic', layers: [3, 6, 5], description: 'Significant wealth — useful for contrast' },

  // Family/Community
  foster_care: { category: 'community', layers: [8, 1, 7], description: 'In or aged out of foster care system' },
  domestic_violence: { category: 'community', layers: [8, 1, 4], description: 'Experiencing intimate partner violence' },
  single_parent: { category: 'community', layers: [8, 6, 3], description: 'Raising children alone' },
  orphan: { category: 'community', layers: [8, 1, 5], description: 'Without parents or guardians' },
  caregiver: { category: 'community', layers: [8, 4, 6], description: 'Primary caregiver for dependent' },
  isolation: { category: 'community', layers: [8, 4, 10], description: 'Socially isolated, disconnected from community' },
  elderly: { category: 'community', layers: [8, 4, 3], description: 'Elderly, navigating aging-related systems' },

  // Identity/Status
  immigrant: { category: 'identity', layers: [1, 8, 6], description: 'Navigating immigration experience' },
  refugee: { category: 'identity', layers: [1, 5, 8], description: 'Displaced by conflict or persecution' },
  veteran: { category: 'identity', layers: [1, 4, 6], description: 'Military veteran, navigating VA systems' },
  indigenous: { category: 'identity', layers: [1, 8, 9], description: 'Indigenous person navigating colonial systems' },
  enslaved: { category: 'identity', layers: [1, 10, 12], description: 'Person held in slavery (historical or contemporary)' },
  trafficking: { category: 'identity', layers: [1, 10, 4], description: 'Victim of human trafficking' },

  // Education
  illiterate: { category: 'education', layers: [7, 6, 10], description: 'Cannot read or write' },
  dropout: { category: 'education', layers: [7, 6], description: 'Left school before completion' },
  special_education: { category: 'education', layers: [7, 4, 1], description: 'In special education systems' },

  // Environment
  environmental_exposure: { category: 'environment', layers: [9, 4, 1], description: 'Exposed to environmental hazards' },
  climate_displaced: { category: 'environment', layers: [9, 5, 8], description: 'Displaced by climate events' },
  food_desert: { category: 'environment', layers: [9, 4, 6], description: 'Living in area without food access' },

  // Grief/Loss
  grief: { category: 'loss', layers: [4, 8, 12], description: 'Processing significant loss' },
  bereavement: { category: 'loss', layers: [4, 8, 3], description: 'Death of close person, navigating aftermath' },

  // Agency/Autonomy
  surveillance: { category: 'autonomy', layers: [10, 1, 8], description: 'Under surveillance or monitoring' },
  forced_labor: { category: 'autonomy', layers: [10, 1, 6], description: 'Compelled to work against will' },
  child_labor: { category: 'autonomy', layers: [10, 7, 4], description: 'Working as a child' },
  child_marriage: { category: 'autonomy', layers: [10, 1, 7], description: 'Married as a minor' },
}

// ── Slug generator ────────────────────────────────────────────────────────────

export function slugify(name) {
  return name.toLowerCase()
    .replace(/['']/g, '')
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/-+$/, '')
    .replace(/^-+/, '')
}

// ── Character ID generator ────────────────────────────────────────────────────

export function characterId(name, sourceWork) {
  return slugify(name) + '--' + slugify(sourceWork)
}

// ── Validate a character entry ────────────────────────────────────────────────

export function validateCharacter(c) {
  const required = ['name', 'real_or_fictional', 'source_work', 'circumstances']
  const missing = required.filter(f => !c[f])
  if (missing.length > 0) return { valid: false, missing }
  if (!['real', 'fictional'].includes(c.real_or_fictional)) return { valid: false, error: 'real_or_fictional must be "real" or "fictional"' }
  if (!Array.isArray(c.circumstances) || c.circumstances.length === 0) return { valid: false, error: 'circumstances must be non-empty array' }
  return { valid: true }
}
