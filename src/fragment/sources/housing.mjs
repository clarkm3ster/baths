/**
 * FRAGMENT — Housing Data Sources (Layer 5: Housing)
 *
 * HUD: Fair Market Rents, Point-in-Time homeless counts, LIHTC, Public Housing
 * FEMA: Disaster declarations, Individual housing assistance
 * Census: Building permits
 *
 * Housing is where the dome meets the ground.
 */

import { restJSON, sodaAPI, femaAPI } from './factories.mjs'
import { safeFetch, stateAbbrev, stateFips, countyFips } from '../lib.mjs'

export default [

  // ══════════════════════════════════════════════════════════════════
  // HUD Fair Market Rents
  // ══════════════════════════════════════════════════════════════════

  restJSON({
    id: 'hud-fmr',
    label: 'HUD Fair Market Rents',
    layers: [3, 5],
    url: (fips) => `https://www.huduser.gov/hudapi/public/fmr/data/${fips}99999`,
    transform: (data) => {
      const d = data?.data || data
      if (!d) return null
      return {
        county_name: d.county_name || null,
        metro_name: d.metro_name || null,
        efficiency: d.Efficiency || d.efficiency || null,
        one_bedroom: d.one_bedroom || d['One-Bedroom'] || null,
        two_bedroom: d.two_bedroom || d['Two-Bedroom'] || null,
        three_bedroom: d.three_bedroom || d['Three-Bedroom'] || null,
        four_bedroom: d.four_bedroom || d['Four-Bedroom'] || null,
        year: d.year || null,
      }
    },
  }),

  // ══════════════════════════════════════════════════════════════════
  // HUD Point-in-Time Homeless Count (via Socrata on HUD Exchange)
  // ══════════════════════════════════════════════════════════════════

  sodaAPI({
    id: 'hud-pit-homeless',
    label: 'HUD Point-in-Time Homeless Count',
    layers: [5],
    host: 'data.hudexchange.info',
    dataset: 'xbcz-b7nh',
    where: (fips) => {
      const st = stateAbbrev(fips)
      return `state='${st}'`
    },
    select: 'coc_number,coc_name,overall_homeless,sheltered_total_homeless,unsheltered_homeless,chronically_homeless',
    transform: (rows) => {
      const total = rows.reduce((s, r) => s + (parseInt(r.overall_homeless) || 0), 0)
      const sheltered = rows.reduce((s, r) => s + (parseInt(r.sheltered_total_homeless) || 0), 0)
      const unsheltered = rows.reduce((s, r) => s + (parseInt(r.unsheltered_homeless) || 0), 0)
      const chronic = rows.reduce((s, r) => s + (parseInt(r.chronically_homeless) || 0), 0)
      return {
        coc_count: rows.length,
        total_homeless: total,
        sheltered: sheltered,
        unsheltered: unsheltered,
        chronically_homeless: chronic,
        unsheltered_pct: total > 0 ? Math.round((unsheltered / total) * 1000) / 10 : null,
      }
    },
  }),

  // ══════════════════════════════════════════════════════════════════
  // Census Building Permits Survey
  // ══════════════════════════════════════════════════════════════════

  restJSON({
    id: 'census-building-permits',
    label: 'Census Building Permits Survey',
    layers: [5, 6],
    url: (fips) => {
      const state = stateFips(fips)
      const county = countyFips(fips)
      return `https://api.census.gov/data/2022/cbp?get=PERMITS,BLDGS,UNITS,VALUATION&for=county:${county}&in=state:${state}`
    },
    transform: (data) => {
      if (!Array.isArray(data) || data.length < 2) return null
      const headers = data[0]
      const values = data[1]
      const result = {}
      for (let i = 0; i < headers.length; i++) {
        result[headers[i].toLowerCase()] = values[i]
      }
      return result
    },
  }),

  // ══════════════════════════════════════════════════════════════════
  // HUD/USPS Vacancy Data
  // ══════════════════════════════════════════════════════════════════

  restJSON({
    id: 'hud-usps-vacancy',
    label: 'HUD/USPS Vacancy Data',
    layers: [5],
    url: (fips) => {
      const state = stateFips(fips)
      return `https://www.huduser.gov/hudapi/public/usps?type=2&query=${state}`
    },
    transform: (data) => {
      if (!data?.data) return { note: 'HUD USPS API may require token', available: false }
      return data.data
    },
  }),

  // ══════════════════════════════════════════════════════════════════
  // FEMA Disaster Declarations (impacts housing)
  // ══════════════════════════════════════════════════════════════════

  femaAPI({
    id: 'fema-disasters',
    label: 'FEMA Disaster Declarations',
    layers: [5, 9],
    endpoint: 'DisasterDeclarationsSummaries',
    filter: (fips) => {
      const st = stateAbbrev(fips)
      return `state eq '${st}'`
    },
    select: 'disasterNumber,declarationDate,disasterType,incidentType,title,designatedArea',
    top: 50,
    transform: (records, fips) => {
      return {
        state: stateAbbrev(fips),
        recent_count: records.length,
        disasters: records.slice(0, 15).map(d => ({
          number: d.disasterNumber,
          date: d.declarationDate,
          type: d.incidentType,
          title: d.title,
        })),
      }
    },
  }),

  // ══════════════════════════════════════════════════════════════════
  // FEMA Individual Assistance (housing assistance applications)
  // ══════════════════════════════════════════════════════════════════

  femaAPI({
    id: 'fema-individual-assistance',
    label: 'FEMA Individual Housing Assistance',
    layers: [1, 5],
    endpoint: 'HousingAssistanceOwners',
    filter: (fips) => {
      const st = stateAbbrev(fips)
      return `state eq '${st}'`
    },
    top: 50,
    transform: (records) => {
      const totalApproved = records.reduce((s, r) => s + (parseFloat(r.approvedAmount) || 0), 0)
      return {
        disaster_housing_records: records.length,
        total_approved_amount: totalApproved,
        avg_approved: records.length > 0 ? Math.round(totalApproved / records.length) : 0,
      }
    },
  }),

  // ══════════════════════════════════════════════════════════════════
  // HUD Public Housing Buildings
  // ══════════════════════════════════════════════════════════════════

  restJSON({
    id: 'hud-public-housing',
    label: 'HUD Public Housing Buildings',
    layers: [5],
    url: (fips) => {
      const state = stateAbbrev(fips).toLowerCase()
      return `https://data.hud.gov/Housing_Counselor/searchByLocation?Location=${state}&MaxResults=100`
    },
    transform: (data) => {
      if (!Array.isArray(data)) return { note: 'HUD counselor API format', available: false }
      return {
        housing_counselors: data.length,
        agencies: [...new Set(data.map(d => d.agcnm).filter(Boolean))].slice(0, 20),
      }
    },
  }),

  // ══════════════════════════════════════════════════════════════════
  // Low Income Housing Tax Credit (LIHTC) Properties
  // ══════════════════════════════════════════════════════════════════

  restJSON({
    id: 'hud-lihtc',
    label: 'HUD LIHTC Properties',
    layers: [5],
    url: (fips) => {
      const state = stateFips(fips)
      return `https://www.huduser.gov/hudapi/public/lihtc?statefp=${state}`
    },
    transform: (data) => {
      if (!data?.data && !Array.isArray(data)) return { note: 'LIHTC API may require token', available: false }
      const records = data?.data || data
      if (!Array.isArray(records)) return { note: 'Unexpected format' }
      return {
        lihtc_properties: records.length,
        total_units: records.reduce((s, r) => s + (parseInt(r.li_units) || 0), 0),
        total_low_income_units: records.reduce((s, r) => s + (parseInt(r.lihtc_li_units) || 0), 0),
      }
    },
  }),
]
