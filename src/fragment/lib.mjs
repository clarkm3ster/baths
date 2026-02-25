/**
 * FRAGMENT — Shared utilities
 *
 * Common helpers for all scraper sources.
 * safeFetch, delay, state lookups, file I/O.
 */

import { readFileSync, writeFileSync, mkdirSync, existsSync, readdirSync } from 'node:fs'
import { join, dirname } from 'node:path'

// ── Delay helper ─────────────────────────────────────────────────────────────
export const delay = ms => new Promise(r => setTimeout(r, ms))

// ── Safe fetch with timeout + error handling ─────────────────────────────────
export async function safeFetch(url, label, options = {}) {
  try {
    const controller = new AbortController()
    const timeout = setTimeout(() => controller.abort(), options.timeout || 30000)
    const fetchOpts = { signal: controller.signal, ...options }
    delete fetchOpts.timeout
    const res = await fetch(url, fetchOpts)
    clearTimeout(timeout)
    if (!res.ok) {
      return { ok: false, error: `HTTP ${res.status}`, status: res.status }
    }
    const text = await res.text()
    try {
      return { ok: true, data: JSON.parse(text) }
    } catch {
      return { ok: false, error: 'Invalid JSON', raw: text.slice(0, 500) }
    }
  } catch (err) {
    return { ok: false, error: err.message }
  }
}

// ── File I/O helpers ─────────────────────────────────────────────────────────
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

// ── State FIPS to abbreviation ───────────────────────────────────────────────
const STATE_FIPS = {
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

export function stateAbbrev(fips) {
  return STATE_FIPS[fips.slice(0, 2)] || fips.slice(0, 2)
}

export function stateFips(fips) {
  return fips.slice(0, 2)
}

export function countyFips(fips) {
  return fips.slice(2)
}

// ── Counties ─────────────────────────────────────────────────────────────────
export const COUNTIES = [
  // Philadelphia metro
  { fips: '42101', name: 'Philadelphia, PA' },
  { fips: '42045', name: 'Delaware County, PA' },
  { fips: '42091', name: 'Montgomery County, PA' },
  { fips: '42017', name: 'Bucks County, PA' },
  { fips: '42029', name: 'Chester County, PA' },
  // NYC
  { fips: '36061', name: 'New York County (Manhattan), NY' },
  { fips: '36047', name: 'Kings County (Brooklyn), NY' },
  { fips: '36081', name: 'Queens County, NY' },
  { fips: '36005', name: 'Bronx County, NY' },
  // Major metros
  { fips: '06037', name: 'Los Angeles County, CA' },
  { fips: '17031', name: 'Cook County (Chicago), IL' },
  { fips: '48201', name: 'Harris County (Houston), TX' },
  { fips: '04013', name: 'Maricopa County (Phoenix), AZ' },
  { fips: '48113', name: 'Dallas County, TX' },
  { fips: '12086', name: 'Miami-Dade County, FL' },
  { fips: '13121', name: 'Fulton County (Atlanta), GA' },
  { fips: '53033', name: 'King County (Seattle), WA' },
  { fips: '24510', name: 'Baltimore City, MD' },
  { fips: '11001', name: 'District of Columbia' },
  // Rural / Appalachia
  { fips: '21013', name: 'Bell County, KY' },
  { fips: '54055', name: 'Mercer County, WV' },
  // Deep South
  { fips: '28049', name: 'Hinds County (Jackson), MS' },
  { fips: '01073', name: 'Jefferson County (Birmingham), AL' },
  // Midwest
  { fips: '26163', name: 'Wayne County (Detroit), MI' },
  { fips: '39035', name: 'Cuyahoga County (Cleveland), OH' },
  // New Jersey
  { fips: '34013', name: 'Essex County, NJ' },
  { fips: '34017', name: 'Hudson County, NJ' },
  { fips: '34023', name: 'Middlesex County, NJ' },
]
