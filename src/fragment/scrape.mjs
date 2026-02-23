#!/usr/bin/env node
/**
 * FRAGMENT — Data scraper agent
 *
 * Collects every publicly available data point about what it means to be alive,
 * by geography and time. It mirrors the fragmentation of human data.
 *
 * Runs 5x daily via GitHub Actions. No external dependencies — Node built-in fetch only.
 */

import { readFileSync, writeFileSync, mkdirSync, existsSync, readdirSync } from 'node:fs'
import { join, dirname } from 'node:path'
import { fileURLToPath } from 'node:url'

const __dirname = dirname(fileURLToPath(import.meta.url))
const ROOT = join(__dirname, '..', '..')
const DATA = join(ROOT, 'data')
const FRAGMENTS = join(DATA, 'fragments')
const META = join(DATA, 'meta')

// ── Priority Counties ────────────────────────────────────────────────────────
const COUNTIES = [
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

// ── Delay helper ─────────────────────────────────────────────────────────────
const delay = ms => new Promise(r => setTimeout(r, ms))

// ── Safe fetch with timeout + error handling ─────────────────────────────────
async function safeFetch(url, label) {
  try {
    const controller = new AbortController()
    const timeout = setTimeout(() => controller.abort(), 30000)
    const res = await fetch(url, { signal: controller.signal })
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
function readJSON(path) {
  try {
    return JSON.parse(readFileSync(path, 'utf8'))
  } catch {
    return null
  }
}

function writeJSON(path, data) {
  mkdirSync(dirname(path), { recursive: true })
  writeFileSync(path, JSON.stringify(data, null, 2) + '\n')
}

function fragmentPath(sourceId, fips) {
  return join(FRAGMENTS, sourceId, `${fips}.json`)
}

function getFragmentAge(sourceId, fips) {
  const existing = readJSON(fragmentPath(sourceId, fips))
  if (!existing?.scraped_at) return Infinity
  return Date.now() - new Date(existing.scraped_at).getTime()
}

// ── Source Definitions ───────────────────────────────────────────────────────
// Each source defines how to scrape a specific dataset

const CENSUS_ACS_YEAR = '2022' // Latest stable ACS 5-year

// Census ACS variable groups — each becomes a source
const CENSUS_GROUPS = [
  {
    id: 'census-demographics',
    label: 'Census Demographics',
    variables: {
      total_pop: 'B01003_001E',
      median_age: 'B01002_001E',
      male_pop: 'B01001_002E',
      female_pop: 'B01001_026E',
      white_alone: 'B02001_002E',
      black_alone: 'B02001_003E',
      asian_alone: 'B02001_005E',
      hispanic_latino: 'B03003_003E',
      foreign_born: 'B05002_013E',
    }
  },
  {
    id: 'census-income',
    label: 'Census Income & Poverty',
    variables: {
      median_household_income: 'B19013_001E',
      per_capita_income: 'B19301_001E',
      poverty_total: 'B17001_001E',
      poverty_below: 'B17001_002E',
      gini_index: 'B19083_001E',
      snap_households: 'B22003_002E',
      public_assistance_income: 'B19057_002E',
      ssi_income: 'B19056_002E',
    }
  },
  {
    id: 'census-housing',
    label: 'Census Housing',
    variables: {
      total_units: 'B25001_001E',
      occupied_units: 'B25002_002E',
      vacant_units: 'B25002_003E',
      owner_occupied: 'B25003_002E',
      renter_occupied: 'B25003_003E',
      median_home_value: 'B25077_001E',
      median_gross_rent: 'B25064_001E',
      median_monthly_housing_cost: 'B25105_001E',
    }
  },
  {
    id: 'census-rent-burden',
    label: 'Census Rent Burden',
    variables: {
      rent_total: 'B25070_001E',
      rent_30_35_pct: 'B25070_007E',
      rent_35_40_pct: 'B25070_008E',
      rent_40_50_pct: 'B25070_009E',
      rent_50_plus_pct: 'B25070_010E',
      rent_not_computed: 'B25070_011E',
    }
  },
  {
    id: 'census-health-insurance',
    label: 'Census Health Insurance',
    variables: {
      total_pop_insurance: 'B27001_001E',
      with_insurance: 'B27001_004E',
      male_under6_uninsured: 'B27001_005E',
      male_6_18_uninsured: 'B27001_008E',
      female_under6_uninsured: 'B27001_033E',
      female_6_18_uninsured: 'B27001_036E',
      medicaid_means_tested: 'B27007_004E',
      employer_insurance: 'B27010_003E',
    }
  },
  {
    id: 'census-disability',
    label: 'Census Disability',
    variables: {
      total_disability_pop: 'B18101_001E',
      male_with_disability: 'B18101_004E',
      female_with_disability: 'B18101_023E',
      disability_under5: 'B18101_003E',
      disability_5_17: 'B18101_006E',
      disability_18_34: 'B18101_009E',
      disability_65_74: 'B18101_015E',
      disability_75_plus: 'B18101_018E',
    }
  },
  {
    id: 'census-education',
    label: 'Census Education',
    variables: {
      edu_pop_25plus: 'B15003_001E',
      less_than_9th: 'B15003_002E',
      high_school_diploma: 'B15003_017E',
      some_college: 'B15003_019E',
      bachelors: 'B15003_022E',
      masters: 'B15003_023E',
      doctorate: 'B15003_025E',
      school_enrollment_total: 'B14001_001E',
      school_enrollment_public: 'B14002_003E',
    }
  },
  {
    id: 'census-commute',
    label: 'Census Commute & Transportation',
    variables: {
      workers_total: 'B08301_001E',
      drove_alone: 'B08301_003E',
      public_transit: 'B08301_010E',
      walked: 'B08301_019E',
      worked_from_home: 'B08301_021E',
      mean_travel_time: 'B08135_001E',
      no_vehicle: 'B08014_002E',
      one_vehicle: 'B08014_003E',
    }
  },
  {
    id: 'census-internet',
    label: 'Census Internet & Technology',
    variables: {
      total_households_internet: 'B28002_001E',
      with_internet: 'B28002_002E',
      broadband: 'B28002_004E',
      no_internet: 'B28002_013E',
      has_computer: 'B28001_002E',
      has_smartphone_only: 'B28001_005E',
      no_computer: 'B28001_011E',
    }
  },
  {
    id: 'census-employment',
    label: 'Census Employment',
    variables: {
      pop_16_plus: 'B23025_001E',
      in_labor_force: 'B23025_002E',
      civilian_employed: 'B23025_004E',
      civilian_unemployed: 'B23025_005E',
      not_in_labor_force: 'B23025_007E',
      occupation_mgmt: 'C24010_003E',
      occupation_service: 'C24010_019E',
      occupation_production: 'C24010_030E',
    }
  },
]

// BLS series IDs for state unemployment (LAUS)
// Format: LASST{state_fips}0000000000003 for unemployment rate
function blsSeriesForState(stateFips) {
  return `LASST${stateFips}0000000000003`
}

// Map county FIPS to state FIPS
function stateFromCounty(fips) {
  return fips.slice(0, 2)
}

// ── Source scrapers ──────────────────────────────────────────────────────────

async function scrapeCensusGroup(group, fips) {
  const state = fips.slice(0, 2)
  const county = fips.slice(2)
  const vars = Object.values(group.variables).join(',')
  const url = `https://api.census.gov/data/${CENSUS_ACS_YEAR}/acs/acs5?get=${vars}&for=county:${county}&in=state:${state}`

  const result = await safeFetch(url, group.label)
  if (!result.ok) {
    return { ok: false, source: group.id, error: result.error }
  }

  if (!Array.isArray(result.data) || result.data.length < 2) {
    return { ok: false, source: group.id, error: 'Unexpected response format' }
  }

  const headers = result.data[0]
  const values = result.data[1]
  const parsed = {}
  const varKeys = Object.keys(group.variables)
  const varVals = Object.values(group.variables)

  for (let i = 0; i < varVals.length; i++) {
    const idx = headers.indexOf(varVals[i])
    if (idx !== -1) {
      const raw = values[idx]
      parsed[varKeys[i]] = raw === null || raw === '-666666666' ? null : Number(raw)
    }
  }

  return {
    ok: true,
    source: group.id,
    data: parsed,
  }
}

async function scrapeBLS(fips) {
  const stateFips = stateFromCounty(fips)
  const seriesId = blsSeriesForState(stateFips)
  const currentYear = new Date().getFullYear()

  const url = 'https://api.bls.gov/publicAPI/v2/timeseries/data/'
  const body = JSON.stringify({
    seriesid: [seriesId],
    startyear: String(currentYear - 1),
    endyear: String(currentYear),
  })

  const result = await safeFetch(url, 'BLS')

  // BLS public API needs POST
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

    if (!res.ok) {
      return { ok: false, source: 'bls-unemployment', error: `HTTP ${res.status}` }
    }

    const json = await res.json()
    if (json.status !== 'REQUEST_SUCCEEDED' || !json.Results?.series?.[0]?.data?.length) {
      return { ok: false, source: 'bls-unemployment', error: json.message?.[0] || 'No data' }
    }

    const series = json.Results.series[0].data
    const latest = series[0] // Most recent period first
    const yearAgo = series.find(d => d.year === String(currentYear - 1) && d.period === latest.period)

    return {
      ok: true,
      source: 'bls-unemployment',
      data: {
        state_fips: stateFips,
        series_id: seriesId,
        latest_rate: parseFloat(latest.value),
        latest_period: `${latest.year}-${latest.period}`,
        year_ago_rate: yearAgo ? parseFloat(yearAgo.value) : null,
        year_ago_period: yearAgo ? `${yearAgo.year}-${yearAgo.period}` : null,
        change: yearAgo ? parseFloat((latest.value - yearAgo.value).toFixed(1)) : null,
        note: 'State-level rate (county not available in public BLS tier)',
      }
    }
  } catch (err) {
    return { ok: false, source: 'bls-unemployment', error: err.message }
  }
}

async function scrapeHUD(fips) {
  const stateFips = fips.slice(0, 2)
  const countyFips = fips

  // HUD FMR API — Small Area FMRs
  const url = `https://www.huduser.gov/hudapi/public/fmr/data/${countyFips}99999`

  // HUD API needs a token for most endpoints — try the public summary
  const altUrl = `https://www.huduser.gov/hudapi/public/fmr/statedata/${stateFips}`

  const result = await safeFetch(url, 'HUD FMR')

  if (result.ok && result.data?.data) {
    const d = result.data.data
    return {
      ok: true,
      source: 'hud-fmr',
      data: {
        county_name: d.county_name || null,
        metro_name: d.metro_name || null,
        efficiency: d.Efficiency || d.efficiency || null,
        one_bedroom: d.one_bedroom || d['One-Bedroom'] || null,
        two_bedroom: d.two_bedroom || d['Two-Bedroom'] || null,
        three_bedroom: d.three_bedroom || d['Three-Bedroom'] || null,
        four_bedroom: d.four_bedroom || d['Four-Bedroom'] || null,
        year: d.year || null,
      }
    }
  }

  // Log as gap — HUD public API often requires token
  return {
    ok: false,
    source: 'hud-fmr',
    error: result.error || 'HUD API may require token',
    needs_key: true,
  }
}

async function scrapeEPAAirQuality(fips) {
  const stateFips = fips.slice(0, 2)
  const countyFips = fips.slice(2)
  const currentYear = new Date().getFullYear()

  // EPA AQS API — annual summary, no key needed for basic queries
  const url = `https://aqs.epa.gov/data/api/annualData/byCounty?email=baths@fragment.dev&key=test&param=44201&bdate=${currentYear - 1}0101&edate=${currentYear - 1}1231&state=${stateFips}&county=${countyFips}`

  // Try the EPA outdoor air quality flag
  const summaryUrl = `https://aqs.epa.gov/data/api/quarterlyData/byCounty?email=baths@fragment.dev&key=test&param=44201&bdate=${currentYear - 1}0101&edate=${currentYear - 1}0331&state=${stateFips}&county=${countyFips}`

  const result = await safeFetch(summaryUrl, 'EPA AQI')

  if (result.ok && result.data?.Header?.[0]?.status === 'Success' && result.data?.Data?.length > 0) {
    const readings = result.data.Data
    return {
      ok: true,
      source: 'epa-air-quality',
      data: {
        parameter: 'Ozone',
        readings_count: readings.length,
        sample: readings.slice(0, 3).map(r => ({
          site: r.site_number,
          mean: r.arithmetic_mean,
          max: r.first_max_value,
          observation_count: r.observation_count,
        })),
        note: 'Quarterly ozone data',
      }
    }
  }

  // EPA often needs registration — log as gap
  return {
    ok: false,
    source: 'epa-air-quality',
    error: result.error || 'EPA AQS API requires registered key',
    needs_key: true,
  }
}

async function scrapeUSDAFoodAccess(fips) {
  // USDA Food Access Research Atlas — check ERS API
  const url = `https://api.ers.usda.gov/data/food-access?api_key=DEMO_KEY&fips=${fips}`

  // The USDA ERS API is limited — try the food desert data
  const altUrl = `https://gis.ers.usda.gov/arcgis/rest/services/foodDesert/MapServer/0/query?where=CensusTract+LIKE+'${fips}%25'&outFields=*&f=json`

  const result = await safeFetch(altUrl, 'USDA Food Access')

  if (result.ok && result.data?.features?.length > 0) {
    const tracts = result.data.features.map(f => f.attributes)
    const lowAccess = tracts.filter(t => t.LILATracts_1And10 === 1 || t.LILATracts_halfAnd10 === 1).length

    return {
      ok: true,
      source: 'usda-food-access',
      data: {
        total_tracts: tracts.length,
        low_access_tracts: lowAccess,
        low_access_pct: tracts.length > 0 ? Math.round((lowAccess / tracts.length) * 100) : 0,
        note: 'USDA Food Access Research Atlas - low income, low access tracts',
      }
    }
  }

  return {
    ok: false,
    source: 'usda-food-access',
    error: result.error || 'USDA Food Access endpoint unavailable',
    needs_key: false,
  }
}

async function scrapeFEMADisasters(fips) {
  const state = fips.slice(0, 2)
  const county = fips.slice(2)
  // FEMA OpenFEMA API — no key needed
  const url = `https://www.fema.gov/api/open/v2/DisasterDeclarationsSummaries?$filter=state eq '${stateAbbrevFromFips(state)}' and designatedArea eq '(County)'&$top=50&$orderby=declarationDate desc&$select=disasterNumber,declarationDate,disasterType,incidentType,title,designatedArea`

  const result = await safeFetch(url, 'FEMA')

  if (result.ok && result.data?.DisasterDeclarationsSummaries) {
    const disasters = result.data.DisasterDeclarationsSummaries
    return {
      ok: true,
      source: 'fema-disasters',
      data: {
        state: stateAbbrevFromFips(state),
        recent_count: disasters.length,
        disasters: disasters.slice(0, 10).map(d => ({
          number: d.disasterNumber,
          date: d.declarationDate,
          type: d.incidentType,
          title: d.title,
        })),
      }
    }
  }

  return {
    ok: false,
    source: 'fema-disasters',
    error: result.error || 'FEMA API error',
  }
}

async function scrapeCDCWonder(fips) {
  // CDC WONDER doesn't have a clean REST API — log as gap
  return {
    ok: false,
    source: 'cdc-mortality',
    error: 'CDC WONDER requires interactive agreement, no public REST API',
    needs_key: true,
  }
}

async function scrapeFBIcrime(fips) {
  // FBI UCR API needs key
  return {
    ok: false,
    source: 'fbi-crime',
    error: 'FBI UCR API requires API key (api.usa.gov)',
    needs_key: true,
  }
}

// State FIPS to abbreviation lookup
function stateAbbrevFromFips(fips) {
  const map = {
    '01': 'AL', '04': 'AZ', '06': 'CA', '11': 'DC', '12': 'FL',
    '13': 'GA', '17': 'IL', '21': 'KY', '24': 'MD', '26': 'MI',
    '28': 'MS', '34': 'NJ', '36': 'NY', '39': 'OH', '42': 'PA',
    '48': 'TX', '53': 'WA', '54': 'WV',
  }
  return map[fips] || fips
}

// ── All sources registry ─────────────────────────────────────────────────────

function getAllSources() {
  const sources = []

  // Census groups
  for (const group of CENSUS_GROUPS) {
    sources.push({
      id: group.id,
      label: group.label,
      api: 'Census ACS 5-year',
      scrape: (fips) => scrapeCensusGroup(group, fips),
    })
  }

  // BLS
  sources.push({
    id: 'bls-unemployment',
    label: 'BLS State Unemployment',
    api: 'BLS Public Data API',
    scrape: scrapeBLS,
  })

  // HUD
  sources.push({
    id: 'hud-fmr',
    label: 'HUD Fair Market Rents',
    api: 'HUD User API',
    scrape: scrapeHUD,
  })

  // EPA
  sources.push({
    id: 'epa-air-quality',
    label: 'EPA Air Quality',
    api: 'EPA AQS API',
    scrape: scrapeEPAAirQuality,
  })

  // USDA
  sources.push({
    id: 'usda-food-access',
    label: 'USDA Food Access',
    api: 'USDA Food Access Atlas',
    scrape: scrapeUSDAFoodAccess,
  })

  // FEMA
  sources.push({
    id: 'fema-disasters',
    label: 'FEMA Disaster Declarations',
    api: 'OpenFEMA API',
    scrape: scrapeFEMADisasters,
  })

  // Gaps — known data that needs keys
  sources.push({
    id: 'cdc-mortality',
    label: 'CDC Mortality',
    api: 'CDC WONDER',
    scrape: scrapeCDCWonder,
    gap: true,
  })

  sources.push({
    id: 'fbi-crime',
    label: 'FBI Crime Statistics',
    api: 'FBI UCR API',
    scrape: scrapeFBIcrime,
    gap: true,
  })

  return sources
}

// ── Scheduling — breadth first, oldest first ─────────────────────────────────

function pickWork(sources, counties, limit = 100) {
  const pairs = []

  for (const source of sources) {
    for (const county of counties) {
      const age = getFragmentAge(source.id, county.fips)
      pairs.push({
        source,
        county,
        age,
        priority: source.gap ? -1 : age, // gaps go last
      })
    }
  }

  // Sort: never-scraped first (Infinity), then oldest, gaps last
  pairs.sort((a, b) => {
    if (a.priority === -1 && b.priority !== -1) return 1
    if (b.priority === -1 && a.priority !== -1) return -1
    return b.age - a.age
  })

  return pairs.slice(0, limit)
}

// ── Main scrape run ──────────────────────────────────────────────────────────

async function run() {
  console.log('\n╔══════════════════════════════════════════╗')
  console.log('║         FRAGMENT — Data Scraper          ║')
  console.log('╚══════════════════════════════════════════╝\n')

  const startTime = Date.now()
  const sources = getAllSources()
  const work = pickWork(sources, COUNTIES, 30)

  console.log(`Sources: ${sources.length}`)
  console.log(`Counties: ${COUNTIES.length}`)
  console.log(`Work items this run: ${work.length}\n`)

  let scraped = 0
  let failed = 0
  let gapsLogged = 0
  const gaps = []
  const sourcesUpdated = {}

  for (const item of work) {
    const { source, county } = item
    const tag = `[${source.id}][${county.fips}]`

    try {
      process.stdout.write(`  ${tag} ${county.name}... `)
      const result = await source.scrape(county.fips)

      if (result.ok) {
        const fragment = {
          source: source.id,
          source_label: source.label,
          api: source.api,
          fips: county.fips,
          county_name: county.name,
          scraped_at: new Date().toISOString(),
          data: result.data,
        }

        writeJSON(fragmentPath(source.id, county.fips), fragment)
        scraped++
        sourcesUpdated[source.id] = (sourcesUpdated[source.id] || 0) + 1
        console.log('OK')
      } else {
        console.log(`SKIP — ${result.error}`)
        if (result.needs_key) {
          gaps.push({
            source: source.id,
            fips: county.fips,
            county: county.name,
            reason: result.error,
            needs_key: true,
            logged_at: new Date().toISOString(),
          })
          gapsLogged++
        } else {
          failed++
        }
      }
    } catch (err) {
      console.log(`ERROR — ${err.message}`)
      failed++
    }

    // 500ms delay between API calls
    await delay(500)
  }

  // ── Update metadata ──────────────────────────────────────────────────────

  // sources.json — what's been scraped and when
  const sourcesPath = join(META, 'sources.json')
  const existingSources = readJSON(sourcesPath) || {}
  for (const [sid, count] of Object.entries(sourcesUpdated)) {
    existingSources[sid] = existingSources[sid] || { first_scraped: new Date().toISOString(), total_scrapes: 0 }
    existingSources[sid].last_scraped = new Date().toISOString()
    existingSources[sid].total_scrapes += count
    existingSources[sid].counties_covered = countFragments(sid)
  }
  writeJSON(sourcesPath, existingSources)

  // coverage.json — overall stats
  const coverage = buildCoverage(sources)
  writeJSON(join(META, 'coverage.json'), coverage)

  // gaps.json — what's missing
  const gapsPath = join(META, 'gaps.json')
  const existingGaps = readJSON(gapsPath) || { gaps: [], last_updated: null }
  // Merge new gaps, deduplicate by source+fips
  const gapKey = g => `${g.source}:${g.fips}`
  const gapMap = new Map(existingGaps.gaps.map(g => [gapKey(g), g]))
  for (const gap of gaps) {
    gapMap.set(gapKey(gap), gap)
  }
  writeJSON(gapsPath, {
    gaps: Array.from(gapMap.values()),
    last_updated: new Date().toISOString(),
    total: gapMap.size,
  })

  const elapsed = ((Date.now() - startTime) / 1000).toFixed(1)

  console.log('\n── Results ─────────────────────────────────')
  console.log(`  Scraped:    ${scraped}`)
  console.log(`  Failed:     ${failed}`)
  console.log(`  Gaps:       ${gapsLogged}`)
  console.log(`  Time:       ${elapsed}s`)
  console.log(`  Fragments:  ${countAllFragments()}`)
  console.log('────────────────────────────────────────────\n')

  return { scraped, failed, gaps: gapsLogged, total_fragments: countAllFragments() }
}

// ── Coverage helpers ─────────────────────────────────────────────────────────

function countFragments(sourceId) {
  const dir = join(FRAGMENTS, sourceId)
  if (!existsSync(dir)) return 0
  return readdirSync(dir).filter(f => f.endsWith('.json')).length
}

function countAllFragments() {
  if (!existsSync(FRAGMENTS)) return 0
  let count = 0
  for (const dir of readdirSync(FRAGMENTS)) {
    const full = join(FRAGMENTS, dir)
    try {
      count += readdirSync(full).filter(f => f.endsWith('.json')).length
    } catch { /* skip non-directories */ }
  }
  return count
}

function buildCoverage(sources) {
  const coverage = {
    generated_at: new Date().toISOString(),
    total_sources: sources.length,
    active_sources: sources.filter(s => !s.gap).length,
    gap_sources: sources.filter(s => s.gap).length,
    total_counties: COUNTIES.length,
    total_fragments: countAllFragments(),
    by_source: {},
    by_county: {},
  }

  for (const source of sources) {
    coverage.by_source[source.id] = {
      label: source.label,
      api: source.api,
      fragments: countFragments(source.id),
      gap: !!source.gap,
    }
  }

  for (const county of COUNTIES) {
    let fragments = 0
    for (const source of sources) {
      if (existsSync(fragmentPath(source.id, county.fips))) fragments++
    }
    coverage.by_county[county.fips] = {
      name: county.name,
      fragments,
      coverage_pct: Math.round((fragments / sources.length) * 100),
    }
  }

  return coverage
}

// ── Run ──────────────────────────────────────────────────────────────────────
run().then(result => {
  // Exit 0 even if all fail — Cosm should still run on existing data
  process.exit(0)
}).catch(err => {
  console.error('FRAGMENT FATAL:', err)
  process.exit(1)
})
