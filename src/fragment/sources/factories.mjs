/**
 * FRAGMENT — Scraper Factories
 *
 * Factory functions for common API patterns.
 * Each factory takes a config and returns a source definition:
 *   { id, label, api, layers, scrape(fips) }
 *
 * Patterns:
 *   censusACS  — Census American Community Survey (hundreds of tables)
 *   sodaAPI    — Socrata Open Data (CDC, CMS, HHS, city portals)
 *   blsSeries  — Bureau of Labor Statistics time series
 *   restJSON   — Generic REST JSON endpoint
 *   femaAPI    — FEMA OpenFEMA datasets
 *   usaSpend   — USASpending.gov
 *   treasuryAPI — Treasury Fiscal Data
 */

import { safeFetch, stateFips, countyFips, stateAbbrev } from '../lib.mjs'

const CENSUS_ACS_YEAR = '2022' // Latest stable ACS 5-year

// ── Census ACS Factory ──────────────────────────────────────────────────────
// All Census ACS tables use the same URL pattern. Just pass variable groups.

export function censusACS({ id, label, layers, variables, transform }) {
  return {
    id,
    label,
    api: 'Census ACS 5-year',
    layers,
    scrape: async (fips) => {
      const state = stateFips(fips)
      const county = countyFips(fips)
      const vars = Object.values(variables).join(',')
      const url = `https://api.census.gov/data/${CENSUS_ACS_YEAR}/acs/acs5?get=${vars}&for=county:${county}&in=state:${state}`

      const result = await safeFetch(url, label)
      if (!result.ok) return { ok: false, source: id, error: result.error }

      if (!Array.isArray(result.data) || result.data.length < 2) {
        return { ok: false, source: id, error: 'Unexpected response format' }
      }

      const headers = result.data[0]
      const values = result.data[1]
      const parsed = {}
      const varKeys = Object.keys(variables)
      const varVals = Object.values(variables)

      for (let i = 0; i < varVals.length; i++) {
        const idx = headers.indexOf(varVals[i])
        if (idx !== -1) {
          const raw = values[idx]
          parsed[varKeys[i]] = raw === null || raw === '-666666666' ? null : Number(raw)
        }
      }

      // Optional transform for derived metrics
      const data = transform ? transform(parsed) : parsed
      return { ok: true, source: id, data }
    },
  }
}

// ── Census ACS Subject Table Factory ────────────────────────────────────────
// Subject tables (S-tables) use a slightly different URL path.

export function censusSubject({ id, label, layers, table, variables, transform }) {
  return {
    id,
    label,
    api: 'Census ACS 5-year Subject',
    layers,
    scrape: async (fips) => {
      const state = stateFips(fips)
      const county = countyFips(fips)
      const vars = Object.values(variables).join(',')
      const url = `https://api.census.gov/data/${CENSUS_ACS_YEAR}/acs/acs5/subject?get=${vars}&for=county:${county}&in=state:${state}`

      const result = await safeFetch(url, label)
      if (!result.ok) return { ok: false, source: id, error: result.error }

      if (!Array.isArray(result.data) || result.data.length < 2) {
        return { ok: false, source: id, error: 'Unexpected response format' }
      }

      const headers = result.data[0]
      const values = result.data[1]
      const parsed = {}
      const varKeys = Object.keys(variables)
      const varVals = Object.values(variables)

      for (let i = 0; i < varVals.length; i++) {
        const idx = headers.indexOf(varVals[i])
        if (idx !== -1) {
          const raw = values[idx]
          parsed[varKeys[i]] = raw === null || raw === '-666666666' ? null : Number(raw)
        }
      }

      const data = transform ? transform(parsed) : parsed
      return { ok: true, source: id, data }
    },
  }
}

// ── Socrata Open Data (SODA) Factory ────────────────────────────────────────
// CDC PLACES, CMS, HHS, many city/state portals use Socrata.
// Query format: https://{host}/resource/{dataset}.json?$where=...

export function sodaAPI({ id, label, layers, host, dataset, where, select, transform }) {
  return {
    id,
    label,
    api: `Socrata SODA (${host})`,
    layers,
    scrape: async (fips) => {
      const params = new URLSearchParams({ $limit: '500' })
      const whereClause = typeof where === 'function' ? where(fips) : where
      if (whereClause) params.set('$where', whereClause)
      if (select) params.set('$select', select)

      const url = `https://${host}/resource/${dataset}.json?${params}`
      const result = await safeFetch(url, label)

      if (!result.ok) return { ok: false, source: id, error: result.error }
      if (!Array.isArray(result.data) || result.data.length === 0) {
        return { ok: false, source: id, error: 'No records returned' }
      }

      const data = transform ? transform(result.data, fips) : result.data
      return { ok: true, source: id, data }
    },
  }
}

// ── BLS Time Series Factory ─────────────────────────────────────────────────
// BLS public API v2 — POST with series IDs. No key needed for basic queries.

export function blsSeries({ id, label, layers, seriesId, transform }) {
  return {
    id,
    label,
    api: 'BLS Public Data API v2',
    layers,
    scrape: async (fips) => {
      const sid = typeof seriesId === 'function' ? seriesId(fips) : seriesId
      const currentYear = new Date().getFullYear()

      const url = 'https://api.bls.gov/publicAPI/v2/timeseries/data/'
      const body = JSON.stringify({
        seriesid: Array.isArray(sid) ? sid : [sid],
        startyear: String(currentYear - 2),
        endyear: String(currentYear),
      })

      try {
        const controller = new AbortController()
        const timeout = setTimeout(() => controller.abort(), 30000)
        const res = await fetch(url, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body,
          signal: controller.signal,
        })
        clearTimeout(timeout)

        if (!res.ok) return { ok: false, source: id, error: `HTTP ${res.status}` }
        const json = await res.json()

        if (json.status !== 'REQUEST_SUCCEEDED' || !json.Results?.series?.length) {
          return { ok: false, source: id, error: json.message?.[0] || 'No data' }
        }

        const data = transform
          ? transform(json.Results.series, fips)
          : _defaultBLSTransform(json.Results.series)

        return { ok: true, source: id, data }
      } catch (err) {
        return { ok: false, source: id, error: err.message }
      }
    },
  }
}

function _defaultBLSTransform(series) {
  const s = series[0]
  if (!s?.data?.length) return null
  const latest = s.data[0]
  return {
    series_id: s.seriesID,
    latest_value: parseFloat(latest.value),
    latest_period: `${latest.year}-${latest.period}`,
    data_points: s.data.length,
  }
}

// ── Generic REST JSON Factory ───────────────────────────────────────────────
// For APIs with unique URL patterns.

export function restJSON({ id, label, layers, url, headers: hdrs, transform }) {
  return {
    id,
    label,
    api: 'REST JSON',
    layers,
    scrape: async (fips) => {
      const resolvedUrl = typeof url === 'function' ? url(fips) : url
      const opts = hdrs ? { headers: typeof hdrs === 'function' ? hdrs(fips) : hdrs } : {}
      const result = await safeFetch(resolvedUrl, label, opts)

      if (!result.ok) return { ok: false, source: id, error: result.error }

      const data = transform ? transform(result.data, fips) : result.data
      return { ok: true, source: id, data }
    },
  }
}

// ── FEMA OpenFEMA Factory ───────────────────────────────────────────────────
// All OpenFEMA datasets use the same pattern.

export function femaAPI({ id, label, layers, endpoint, filter, select, top, transform }) {
  return {
    id,
    label,
    api: 'OpenFEMA API',
    layers,
    scrape: async (fips) => {
      const params = []
      const filterStr = typeof filter === 'function' ? filter(fips) : filter
      if (filterStr) params.push(`$filter=${encodeURIComponent(filterStr)}`)
      if (select) params.push(`$select=${select}`)
      params.push(`$top=${top || 100}`)
      params.push('$orderby=id desc')

      const url = `https://www.fema.gov/api/open/v2/${endpoint}?${params.join('&')}`
      const result = await safeFetch(url, label)

      if (!result.ok) return { ok: false, source: id, error: result.error }

      const key = Object.keys(result.data).find(k => Array.isArray(result.data[k]))
      const records = key ? result.data[key] : []

      if (records.length === 0) {
        return { ok: false, source: id, error: 'No records returned' }
      }

      const data = transform ? transform(records, fips) : { count: records.length, records: records.slice(0, 20) }
      return { ok: true, source: id, data }
    },
  }
}

// ── USASpending Factory ─────────────────────────────────────────────────────

export function usaSpend({ id, label, layers, endpoint, body: bodyFn, transform }) {
  return {
    id,
    label,
    api: 'USASpending.gov',
    layers,
    scrape: async (fips) => {
      const url = `https://api.usaspending.gov/api/v2/${endpoint}`
      const body = typeof bodyFn === 'function' ? bodyFn(fips) : bodyFn

      try {
        const controller = new AbortController()
        const timeout = setTimeout(() => controller.abort(), 30000)
        const res = await fetch(url, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(body),
          signal: controller.signal,
        })
        clearTimeout(timeout)

        if (!res.ok) return { ok: false, source: id, error: `HTTP ${res.status}` }
        const json = await res.json()
        const data = transform ? transform(json, fips) : json
        return { ok: true, source: id, data }
      } catch (err) {
        return { ok: false, source: id, error: err.message }
      }
    },
  }
}

// ── Treasury Fiscal Data Factory ────────────────────────────────────────────

export function treasuryAPI({ id, label, layers, endpoint, fields, filter, transform }) {
  return {
    id,
    label,
    api: 'Treasury Fiscal Data',
    layers,
    scrape: async (fips) => {
      const params = []
      if (fields) params.push(`fields=${fields}`)
      const filterStr = typeof filter === 'function' ? filter(fips) : filter
      if (filterStr) params.push(`filter=${filterStr}`)
      params.push('page[size]=100')
      params.push('sort=-record_date')

      const url = `https://api.fiscaldata.treasury.gov/services/api/fiscal_service/${endpoint}?${params.join('&')}`
      const result = await safeFetch(url, label)

      if (!result.ok) return { ok: false, source: id, error: result.error }

      const records = result.data?.data || []
      if (records.length === 0) return { ok: false, source: id, error: 'No records' }

      const data = transform ? transform(records, fips) : { count: records.length, records: records.slice(0, 10) }
      return { ok: true, source: id, data }
    },
  }
}
