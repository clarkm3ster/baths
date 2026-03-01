/**
 * FRAGMENT — Nonprofit Services Sources
 *
 * ProPublica: IRS 990 filings (free, no key)
 * Census CBP: Nonprofit employment, social assistance (free, no key)
 * IMLS: Public libraries, museums (Socrata, no key)
 * Data.gov: Nonprofit dataset catalog (free, no key)
 * USASpending: Federal grants to nonprofits (free, no key)
 * NCES: Private schools via Urban Institute (free, no key)
 */

import { restJSON, sodaAPI, usaSpend } from './factories.mjs'
import { stateAbbrev, stateFips, countyFips } from '../lib.mjs'

export default [

  // ══════════════════════════════════════════════════════════════════
  // ProPublica Nonprofit Explorer — IRS 990 filings
  // ══════════════════════════════════════════════════════════════════

  restJSON({
    id: 'propublica-990-search',
    label: 'ProPublica Nonprofit 990 Search',
    layers: [3, 8],
    url: (fips) => {
      const st = stateAbbrev(fips).toLowerCase()
      return `https://projects.propublica.org/nonprofits/api/v2/search.json?state[id]=${st}&per_page=100`
    },
    transform: (data) => {
      const orgs = data?.organizations || []
      return {
        total_results: data?.total_results || 0,
        count: orgs.length,
        orgs: orgs.slice(0, 25).map(o => ({
          name: o.name,
          ein: o.ein,
          city: o.city,
          state: o.state,
          ntee_code: o.ntee_code,
          income: o.income_amount,
          assets: o.asset_amount,
          tax_period: o.tax_period,
        })),
      }
    },
  }),

  // ══════════════════════════════════════════════════════════════════
  // Census County Business Patterns — Nonprofit sector (NAICS 813)
  // ══════════════════════════════════════════════════════════════════

  restJSON({
    id: 'census-nonprofit-employment',
    label: 'Census CBP Nonprofit Employment (NAICS 813)',
    layers: [6, 8],
    url: (fips) => {
      const st = stateFips(fips)
      const co = countyFips(fips)
      return `https://api.census.gov/data/2021/cbp?get=ESTAB,EMP,PAYANN&for=county:${co}&in=state:${st}&NAICS2017=813`
    },
    transform: (data) => {
      if (!Array.isArray(data) || data.length < 2) return null
      const h = data[0], v = data[1]
      return {
        nonprofit_establishments: parseInt(v[h.indexOf('ESTAB')]) || null,
        nonprofit_employees: parseInt(v[h.indexOf('EMP')]) || null,
        annual_payroll_thousands: parseInt(v[h.indexOf('PAYANN')]) || null,
      }
    },
  }),

  // ══════════════════════════════════════════════════════════════════
  // Census CBP — Social Assistance (NAICS 624)
  // ══════════════════════════════════════════════════════════════════

  restJSON({
    id: 'census-social-assistance',
    label: 'Census CBP Social Assistance (NAICS 624)',
    layers: [4, 6, 8],
    url: (fips) => {
      const st = stateFips(fips)
      const co = countyFips(fips)
      return `https://api.census.gov/data/2021/cbp?get=ESTAB,EMP,PAYANN&for=county:${co}&in=state:${st}&NAICS2017=624`
    },
    transform: (data) => {
      if (!Array.isArray(data) || data.length < 2) return null
      const h = data[0], v = data[1]
      return {
        social_assistance_establishments: parseInt(v[h.indexOf('ESTAB')]) || null,
        social_assistance_employees: parseInt(v[h.indexOf('EMP')]) || null,
        annual_payroll_thousands: parseInt(v[h.indexOf('PAYANN')]) || null,
      }
    },
  }),

  // ══════════════════════════════════════════════════════════════════
  // Census CBP — Full Healthcare & Social Assistance (NAICS 62)
  // ══════════════════════════════════════════════════════════════════

  restJSON({
    id: 'census-healthcare-social',
    label: 'Census CBP Healthcare & Social (NAICS 62)',
    layers: [4, 6],
    url: (fips) => {
      const st = stateFips(fips)
      const co = countyFips(fips)
      return `https://api.census.gov/data/2021/cbp?get=ESTAB,EMP,PAYANN&for=county:${co}&in=state:${st}&NAICS2017=62`
    },
    transform: (data) => {
      if (!Array.isArray(data) || data.length < 2) return null
      const h = data[0], v = data[1]
      return {
        healthcare_social_establishments: parseInt(v[h.indexOf('ESTAB')]) || null,
        healthcare_social_employees: parseInt(v[h.indexOf('EMP')]) || null,
        annual_payroll_thousands: parseInt(v[h.indexOf('PAYANN')]) || null,
      }
    },
  }),

  // ══════════════════════════════════════════════════════════════════
  // IMLS Public Library Outlet Data
  // ══════════════════════════════════════════════════════════════════

  sodaAPI({
    id: 'imls-public-libraries',
    label: 'IMLS Public Library Outlet Data',
    layers: [7, 8],
    host: 'data.imls.gov',
    dataset: 'b4xf-6nc8',
    where: (fips) => `STABR='${stateAbbrev(fips)}'`,
    select: 'STABR,LIBNAME,CITY,CNTY,POPU_LSA,VISITS,TOTCIR,TOTPRO,TOTATTEN,TOTSTAFF,TOTEXPCO',
    transform: (rows) => {
      const totalVisits = rows.reduce((s, r) => s + (parseInt(r.VISITS) || 0), 0)
      const totalCirc = rows.reduce((s, r) => s + (parseInt(r.TOTCIR) || 0), 0)
      const totalPrograms = rows.reduce((s, r) => s + (parseInt(r.TOTPRO) || 0), 0)
      const totalAttend = rows.reduce((s, r) => s + (parseInt(r.TOTATTEN) || 0), 0)
      return {
        library_outlets: rows.length,
        total_visits: totalVisits,
        total_circulation: totalCirc,
        total_programs: totalPrograms,
        total_program_attendance: totalAttend,
        sample: rows.slice(0, 10).map(r => ({
          name: r.LIBNAME,
          city: r.CITY,
          county: r.CNTY,
          population_served: parseInt(r.POPU_LSA) || null,
          visits: parseInt(r.VISITS) || null,
        })),
      }
    },
  }),

  // ══════════════════════════════════════════════════════════════════
  // IMLS Museum Universe Data
  // ══════════════════════════════════════════════════════════════════

  sodaAPI({
    id: 'imls-museums',
    label: 'IMLS Museum Universe Data',
    layers: [7, 8],
    host: 'data.imls.gov',
    dataset: 'ku5e-7x6b',
    where: (fips) => `PHYSSTATE='${stateAbbrev(fips)}'`,
    select: 'COMMONNAME,DISCIPL,PHYSADDR,PHYSCITY,PHYSSTATE,PHYSZIP,INCOMECD,REVENUE',
    transform: (rows) => {
      const disciplines = {}
      for (const r of rows) {
        const d = r.DISCIPL || 'Unknown'
        disciplines[d] = (disciplines[d] || 0) + 1
      }
      return {
        museums: rows.length,
        by_discipline: disciplines,
        total_revenue: rows.reduce((s, r) => s + (parseInt(r.REVENUE) || 0), 0),
        sample: rows.slice(0, 10).map(r => ({
          name: r.COMMONNAME,
          discipline: r.DISCIPL,
          city: r.PHYSCITY,
          revenue: parseInt(r.REVENUE) || null,
        })),
      }
    },
  }),

  // ══════════════════════════════════════════════════════════════════
  // Data.gov Nonprofit Dataset Catalog
  // ══════════════════════════════════════════════════════════════════

  restJSON({
    id: 'datagov-catalog-nonprofit',
    label: 'Data.gov Nonprofit Dataset Catalog',
    layers: [8],
    url: () => 'https://catalog.data.gov/api/3/action/package_search?q=nonprofit+OR+charitable+OR+501c3&rows=50',
    transform: (data) => {
      const results = data?.result?.results || []
      return {
        datasets_found: data?.result?.count || 0,
        sample_count: results.length,
        datasets: results.slice(0, 25).map(d => ({
          name: d.name,
          title: d.title?.slice(0, 120),
          org: d.organization?.title,
          formats: (d.resources || []).map(r => r.format).filter(Boolean),
          notes: d.notes?.slice(0, 200),
        })),
      }
    },
  }),

  // ══════════════════════════════════════════════════════════════════
  // USASpending — Federal grants to nonprofits by county
  // ══════════════════════════════════════════════════════════════════

  usaSpend({
    id: 'usaspending-grants-nonprofit',
    label: 'USASpending Grants to Nonprofits by County',
    layers: [1, 3, 8],
    endpoint: 'search/spending_by_award/',
    body: (fips) => ({
      filters: {
        place_of_performance_locations: [{ country: 'USA', county: fips }],
        time_period: [{ start_date: '2023-10-01', end_date: '2024-09-30' }],
        award_type_codes: ['02', '03', '04', '05'],
        recipient_type_names: ['nonprofit'],
      },
      fields: ['Award ID', 'Recipient Name', 'Award Amount', 'Awarding Agency', 'CFDA Number'],
      limit: 100,
      page: 1,
    }),
    transform: (data) => {
      const results = data?.results || []
      const total = results.reduce((s, r) => s + (r['Award Amount'] || 0), 0)
      return {
        nonprofit_grants: results.length,
        total_amount: total,
        avg_grant: results.length > 0 ? Math.round(total / results.length) : 0,
        top_recipients: results.slice(0, 15).map(r => ({
          recipient: r['Recipient Name'],
          amount: r['Award Amount'],
          agency: r['Awarding Agency'],
          cfda: r['CFDA Number'],
        })),
      }
    },
  }),

  // ══════════════════════════════════════════════════════════════════
  // NCES Private School Universe (PSS)
  // ══════════════════════════════════════════════════════════════════

  restJSON({
    id: 'nces-private-schools',
    label: 'NCES Private School Universe (PSS)',
    layers: [7, 8],
    url: (fips) => {
      const st = stateFips(fips)
      return `https://educationdata.urban.org/api/v1/schools/pss/directory/2021/?fips=${st}&limit=100`
    },
    transform: (data) => {
      const results = data?.results || []
      const affiliations = {}
      for (const r of results) {
        const a = r.religious_affiliation_text || 'None'
        affiliations[a] = (affiliations[a] || 0) + 1
      }
      return {
        private_schools: results.length,
        total_enrollment: results.reduce((s, r) => s + (r.enrollment || 0), 0),
        by_affiliation: affiliations,
        sample: results.slice(0, 10).map(r => ({
          name: r.school_name,
          city: r.city_location,
          enrollment: r.enrollment,
          affiliation: r.religious_affiliation_text,
        })),
      }
    },
  }),
]
