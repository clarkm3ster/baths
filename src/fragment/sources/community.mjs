/**
 * FRAGMENT — Community Data Sources (Layer 8: Community)
 *
 * Census population estimates & poverty
 * Harvard Dataverse election data
 * AmeriCorps national service
 *
 * The community layer — connections, assets, social capital.
 */

import { restJSON, sodaAPI } from './factories.mjs'
import { stateAbbrev, stateFips, countyFips } from '../lib.mjs'

export default [

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
]
