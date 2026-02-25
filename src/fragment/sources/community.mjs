/**
 * FRAGMENT — Community Data Sources (Layer 8: Community)
 *
 * IRS 990: Nonprofit organizations
 * Census population estimates
 * Voting/elections
 * Parks & recreation
 * Community development
 *
 * The community layer — connections, assets, social capital.
 */

import { restJSON, sodaAPI } from './factories.mjs'
import { stateAbbrev, stateFips, countyFips } from '../lib.mjs'

export default [

  // ══════════════════════════════════════════════════════════════════
  // IRS 990 — Nonprofit Organizations (via ProPublica)
  // ══════════════════════════════════════════════════════════════════

  restJSON({
    id: 'propublica-nonprofits',
    label: 'ProPublica Nonprofit Explorer',
    layers: [8],
    url: (fips) => {
      const state = stateAbbrev(fips).toLowerCase()
      return `https://projects.propublica.org/nonprofits/api/v2/search.json?state[id]=${state}&c_code[id]=3&per_page=100`
    },
    transform: (data) => {
      const orgs = data?.organizations || []
      const totalRevenue = orgs.reduce((s, o) => s + (o.income_amount || 0), 0)
      const totalAssets = orgs.reduce((s, o) => s + (o.asset_amount || 0), 0)
      return {
        nonprofits: orgs.length,
        total_count: data?.total_results || orgs.length,
        total_revenue: totalRevenue,
        total_assets: totalAssets,
        ntee_codes: [...new Set(orgs.map(o => o.ntee_code).filter(Boolean))].slice(0, 20),
        sample: orgs.slice(0, 15).map(o => ({
          name: o.name,
          city: o.city,
          ntee_code: o.ntee_code,
          income: o.income_amount,
          assets: o.asset_amount,
        })),
      }
    },
  }),

  // ══════════════════════════════════════════════════════════════════
  // Census Population Estimates (Vintage 2023)
  // ══════════════════════════════════════════════════════════════════

  restJSON({
    id: 'census-population-estimates',
    label: 'Census Population Estimates',
    layers: [8],
    url: (fips) => {
      const state = stateFips(fips)
      const county = countyFips(fips)
      return `https://api.census.gov/data/2022/pep/charagegroups?get=POP,NAME&for=county:${county}&in=state:${state}`
    },
    transform: (data) => {
      if (!Array.isArray(data) || data.length < 2) return null
      const headers = data[0]
      const values = data[1]
      return {
        population_estimate: parseInt(values[headers.indexOf('POP')]) || null,
        name: values[headers.indexOf('NAME')],
        vintage: 2022,
      }
    },
  }),

  // ══════════════════════════════════════════════════════════════════
  // Census Annual Poverty Estimates (SAIPE)
  // Small Area Income and Poverty Estimates
  // ══════════════════════════════════════════════════════════════════

  restJSON({
    id: 'census-saipe',
    label: 'Census Small Area Poverty Estimates',
    layers: [3, 8],
    url: (fips) => {
      const state = stateFips(fips)
      const county = countyFips(fips)
      return `https://api.census.gov/data/timeseries/poverty/saipe?get=NAME,SAEMHI_PT,SAEPOVALL_PT,SAEPOVRTALL_PT,SAEPOV0_17_PT,SAEPOVRT0_17_PT&for=county:${county}&in=state:${state}&time=2022`
    },
    transform: (data) => {
      if (!Array.isArray(data) || data.length < 2) return null
      const headers = data[0]
      const values = data[1]
      return {
        name: values[headers.indexOf('NAME')],
        median_household_income: parseInt(values[headers.indexOf('SAEMHI_PT')]) || null,
        all_ages_in_poverty: parseInt(values[headers.indexOf('SAEPOVALL_PT')]) || null,
        poverty_rate_all: parseFloat(values[headers.indexOf('SAEPOVRTALL_PT')]) || null,
        children_in_poverty: parseInt(values[headers.indexOf('SAEPOV0_17_PT')]) || null,
        child_poverty_rate: parseFloat(values[headers.indexOf('SAEPOVRT0_17_PT')]) || null,
      }
    },
  }),

  // ══════════════════════════════════════════════════════════════════
  // Trust for Public Land — Park Access
  // ══════════════════════════════════════════════════════════════════

  restJSON({
    id: 'tpl-park-access',
    label: 'Trust for Public Land ParkServe',
    layers: [8, 9],
    url: () => 'https://parkserve.tpl.org/api/',
    transform: () => {
      return {
        note: 'TPL ParkServe — interactive map, limited REST API',
        available: false,
        needs_scraping: true,
      }
    },
  }),

  // ══════════════════════════════════════════════════════════════════
  // 211 — Community Services Referral Data
  // ══════════════════════════════════════════════════════════════════

  restJSON({
    id: '211-community-services',
    label: '211 Community Services Directory',
    layers: [2, 8],
    url: () => 'https://www.211.org/',
    transform: () => {
      return {
        note: '211 data — available through individual state/county 211 portals',
        available: false,
        needs_partnerships: true,
      }
    },
  }),

  // ══════════════════════════════════════════════════════════════════
  // FCC Broadband Data — Fixed broadband deployment
  // ══════════════════════════════════════════════════════════════════

  restJSON({
    id: 'fcc-broadband',
    label: 'FCC Broadband Deployment',
    layers: [2, 8],
    url: (fips) => {
      const state = stateFips(fips)
      const county = countyFips(fips)
      return `https://broadbandmap.fcc.gov/api/public/map/listCountyFiber?county_fips=${fips}&speed_download=25&speed_upload=3`
    },
    transform: (data) => {
      if (data?.error) return { note: 'FCC Broadband Map API — may need different endpoint' }
      return {
        ...data,
        note: 'FCC fixed broadband deployment data',
      }
    },
  }),

  // ══════════════════════════════════════════════════════════════════
  // Election Data — MIT Election Lab (via Harvard Dataverse)
  // ══════════════════════════════════════════════════════════════════

  restJSON({
    id: 'election-data',
    label: 'County-Level Election Data',
    layers: [8],
    url: () => 'https://dataverse.harvard.edu/api/search?q=county%20election%20returns&type=dataset&per_page=5',
    transform: (data) => {
      const items = data?.data?.items || []
      return {
        datasets_available: items.length,
        note: 'MIT Election Data + Science Lab — county-level returns available via Harvard Dataverse',
        datasets: items.slice(0, 5).map(d => ({
          name: d.name,
          description: d.description?.slice(0, 200),
          url: d.url,
        })),
      }
    },
  }),

  // ══════════════════════════════════════════════════════════════════
  // CNCS (AmeriCorps) — National Service Programs
  // ══════════════════════════════════════════════════════════════════

  restJSON({
    id: 'americorps-programs',
    label: 'AmeriCorps National Service Programs',
    layers: [8],
    url: (fips) => {
      const state = stateAbbrev(fips)
      return `https://data.americorps.gov/resource/yie5-yr6p.json?$where=state='${state}'&$limit=100`
    },
    transform: (data) => {
      if (!Array.isArray(data)) return { note: 'AmeriCorps SODA API' }
      return {
        programs_in_state: data.length,
        sample: data.slice(0, 10).map(p => ({
          name: p.sponsor_name || p.program_name,
          city: p.city,
          program_type: p.program_type,
        })),
      }
    },
  }),

  // ══════════════════════════════════════════════════════════════════
  // Crime — FBI UCR (needs free API key)
  // ══════════════════════════════════════════════════════════════════

  restJSON({
    id: 'fbi-crime-stats',
    label: 'FBI Uniform Crime Report',
    layers: [8],
    url: (fips) => {
      const state = stateAbbrev(fips).toLowerCase()
      return `https://api.usa.gov/crime/fbi/cde/arrest/state/${state}/all?from=2020&to=2022&API_KEY=DEMO_KEY`
    },
    transform: (data) => {
      if (data?.error || data?.message) return { note: 'FBI UCR API requires registered key from api.usa.gov', needs_key: true }
      const entries = data?.data || data || []
      if (!Array.isArray(entries)) return { note: 'FBI UCR API', data }
      return {
        years_covered: [...new Set(entries.map(e => e.data_year))],
        total_arrests: entries.reduce((s, e) => s + (e.value || 0), 0),
        note: 'State-level arrest data',
      }
    },
  }),

  // ══════════════════════════════════════════════════════════════════
  // VA — Veterans Affairs Facilities
  // ══════════════════════════════════════════════════════════════════

  restJSON({
    id: 'va-facilities',
    label: 'VA Health Care Facilities',
    layers: [1, 4, 8],
    url: (fips) => {
      const state = stateAbbrev(fips)
      return `https://api.va.gov/facilities/v1?state=${state}&type=health&page=1&per_page=100`
    },
    headers: { apikey: 'DEMO_KEY' },
    transform: (data) => {
      const facilities = data?.data || []
      if (!Array.isArray(facilities)) return { note: 'VA API requires key', needs_key: true }
      return {
        va_facilities: facilities.length,
        types: [...new Set(facilities.map(f => f.attributes?.facilityType).filter(Boolean))],
        sample: facilities.slice(0, 10).map(f => ({
          name: f.attributes?.name,
          city: f.attributes?.address?.physical?.city,
          type: f.attributes?.facilityType,
        })),
      }
    },
  }),
]
