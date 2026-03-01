/**
 * FRAGMENT — Education Data Sources (Layer 7: Education)
 *
 * NCES: Common Core of Data (school districts), IPEDS (colleges)
 * Head Start: Early childhood program data
 *
 * The education layer — from pre-K through workforce development.
 */

import { restJSON, sodaAPI } from './factories.mjs'
import { stateAbbrev, stateFips, countyFips } from '../lib.mjs'

export default [

  // ══════════════════════════════════════════════════════════════════
  // NCES Common Core of Data (CCD) — School Districts
  // ══════════════════════════════════════════════════════════════════

  restJSON({
    id: 'nces-school-districts',
    label: 'NCES School Districts (CCD)',
    layers: [7],
    url: (fips) => {
      const state = stateFips(fips)
      return `https://educationdata.urban.org/api/v1/schools/ccd/directory/2022/?fips=${state}&county_code=${fips}&limit=100`
    },
    transform: (data) => {
      const results = data?.results || []
      return {
        schools: results.length,
        school_types: [...new Set(results.map(r => r.school_type_text).filter(Boolean))],
        charter_schools: results.filter(r => r.charter_text === 'Yes').length,
        magnet_schools: results.filter(r => r.magnet_text === 'Yes').length,
        title_i_schools: results.filter(r => r.title_i_status_text?.includes('Yes')).length,
        total_enrollment: results.reduce((s, r) => s + (r.enrollment || 0), 0),
      }
    },
  }),

  // NCES School District Finance
  restJSON({
    id: 'nces-district-finance',
    label: 'NCES School District Finance',
    layers: [3, 7],
    url: (fips) => {
      const state = stateFips(fips)
      return `https://educationdata.urban.org/api/v1/school-districts/ccd/finance/2021/?fips=${state}&limit=50`
    },
    transform: (data) => {
      const results = data?.results || []
      if (results.length === 0) return { note: 'No finance data returned' }
      const totalRevenue = results.reduce((s, r) => s + (r.rev_total || 0), 0)
      const totalExpend = results.reduce((s, r) => s + (r.exp_total || 0), 0)
      return {
        districts: results.length,
        total_revenue: totalRevenue,
        total_expenditures: totalExpend,
        avg_per_pupil: results.length > 0
          ? Math.round(totalExpend / results.reduce((s, r) => s + (r.enrollment || 1), 0))
          : null,
        federal_revenue_pct: totalRevenue > 0
          ? Math.round(results.reduce((s, r) => s + (r.rev_fed_total || 0), 0) / totalRevenue * 1000) / 10
          : null,
      }
    },
  }),

  // ══════════════════════════════════════════════════════════════════
  // IPEDS — Integrated Postsecondary Education Data
  // ══════════════════════════════════════════════════════════════════

  restJSON({
    id: 'ipeds-institutions',
    label: 'IPEDS Postsecondary Institutions',
    layers: [7],
    url: (fips) => {
      const state = stateFips(fips)
      return `https://educationdata.urban.org/api/v1/college-university/ipeds/directory/2022/?fips=${state}&limit=100`
    },
    transform: (data) => {
      const results = data?.results || []
      return {
        institutions: results.length,
        by_sector: _groupCount(results, 'inst_sector_text'),
        by_level: _groupCount(results, 'inst_level_text'),
        hbcus: results.filter(r => r.hbcu === 1).length,
        tribal: results.filter(r => r.tribal_college === 1).length,
      }
    },
  }),

  // ══════════════════════════════════════════════════════════════════
  // Head Start Program Data (via ACF/HHS)
  // ══════════════════════════════════════════════════════════════════

  sodaAPI({
    id: 'headstart-programs',
    label: 'Head Start Program Data',
    layers: [7],
    host: 'data.acf.hhs.gov',
    dataset: 'xv6x-mn5y',
    where: (fips) => {
      const st = stateAbbrev(fips)
      return `state='${st}'`
    },
    select: 'program_name,state,total_cumulative_enrollment,funded_enrollment_slots',
    transform: (rows) => {
      const totalEnrollment = rows.reduce((s, r) => s + (parseInt(r.total_cumulative_enrollment) || 0), 0)
      const totalSlots = rows.reduce((s, r) => s + (parseInt(r.funded_enrollment_slots) || 0), 0)
      return {
        programs: rows.length,
        total_enrollment: totalEnrollment,
        funded_slots: totalSlots,
        utilization: totalSlots > 0 ? Math.round((totalEnrollment / totalSlots) * 1000) / 10 : null,
      }
    },
  }),
]

// ── Helpers ──────────────────────────────────────────────────────

function _groupCount(arr, field) {
  const counts = {}
  for (const item of arr) {
    const val = item[field] || 'unknown'
    counts[val] = (counts[val] || 0) + 1
  }
  return counts
}
