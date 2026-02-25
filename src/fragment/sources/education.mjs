/**
 * FRAGMENT — Education Data Sources (Layer 7: Education)
 *
 * NCES: Common Core of Data (school districts), IPEDS (colleges)
 * College Scorecard: College outcomes data
 * Head Start: Early childhood program data
 * Title I: Federal education funding
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
      const county = countyFips(fips)
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
  // College Scorecard — College Outcomes
  // Uses data.gov API key (DEMO_KEY works for limited queries)
  // ══════════════════════════════════════════════════════════════════

  restJSON({
    id: 'college-scorecard',
    label: 'College Scorecard Institutions',
    layers: [6, 7],
    url: (fips) => {
      const state = stateAbbrev(fips)
      return `https://api.data.gov/ed/collegescorecard/v1/schools.json?api_key=DEMO_KEY&school.state=${state}&fields=school.name,school.city,school.state,latest.admissions.admission_rate.overall,latest.cost.avg_net_price.overall,latest.earnings.10_yrs_after_entry.median,latest.student.size,latest.completion.rate_suppressed.overall&per_page=50`
    },
    transform: (data) => {
      const results = data?.results || []
      if (results.length === 0) return { note: 'No College Scorecard results' }
      const withEarnings = results.filter(r => r['latest.earnings.10_yrs_after_entry.median'])
      return {
        institutions: results.length,
        avg_admission_rate: _avg(results.map(r => r['latest.admissions.admission_rate.overall'])),
        avg_net_price: _avg(results.map(r => r['latest.cost.avg_net_price.overall'])),
        median_earnings_10yr: _avg(withEarnings.map(r => r['latest.earnings.10_yrs_after_entry.median'])),
        avg_completion_rate: _avg(results.map(r => r['latest.completion.rate_suppressed.overall'])),
        total_enrollment: results.reduce((s, r) => s + (r['latest.student.size'] || 0), 0),
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

  // Libraries: see nonprofit-services.mjs (imls-public-libraries — real SODA scraper)

  // ══════════════════════════════════════════════════════════════════
  // Workforce Development — DOL CareerOneStop
  // ══════════════════════════════════════════════════════════════════

  restJSON({
    id: 'dol-career-onestop',
    label: 'DOL CareerOneStop Centers',
    layers: [6, 7],
    url: (fips) => {
      const state = stateAbbrev(fips)
      return `https://api.careeronestop.org/v1/ajcfinder/${state}?radius=50&pageSize=50`
    },
    transform: (data) => {
      // CareerOneStop needs API key — log as available with key
      return {
        note: 'CareerOneStop API — requires free API key from careeronestop.org',
        available: false,
        needs_key: true,
      }
    },
  }),
]

// ── Helpers ──────────────────────────────────────────────────────

function _avg(arr) {
  const nums = arr.filter(n => n != null && !isNaN(n))
  if (nums.length === 0) return null
  return Math.round(nums.reduce((a, b) => a + b, 0) / nums.length * 100) / 100
}

function _groupCount(arr, field) {
  const counts = {}
  for (const item of arr) {
    const val = item[field] || 'unknown'
    counts[val] = (counts[val] || 0) + 1
  }
  return counts
}
