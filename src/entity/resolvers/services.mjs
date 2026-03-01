/**
 * ENTITY RESOLVER — Direct Services
 *
 * Resolves: What government services does this person consume?
 *
 * K-12 education, university, hospital, health center,
 * public defender, incarceration, probation, foster care, transit.
 *
 * These are services consumed, not cash transfers.
 * The cost is what government spends to provide them.
 */

import { getNum } from '../fragments.mjs'
import {
  K12_PER_PUPIL, UNIVERSITY_STATE_SUBSIDY,
  COMMUNITY_HEALTH_CENTER_COST, UNCOMPENSATED_CARE_PER_UNINSURED,
  PUBLIC_DEFENDER_COST, INCARCERATION_COST_PER_YEAR,
  PROBATION_COST_PER_YEAR, FOSTER_CARE_COST_PER_YEAR,
  TRANSIT_SUBSIDY_PER_RIDER, FPL,
} from '../reference.mjs'

export default {
  id: 'services',
  fields: [
    'k12_public_education_cost', 'public_university_state_subsidy',
    'public_hospital_uncompensated', 'community_health_center',
    'public_defender_cost', 'incarceration_cost',
    'probation_parole_cost', 'foster_care_cost',
    'public_transit_subsidy_est', 'other_direct_services',
    'total_direct_services',
  ],

  resolve(profile, county, fragments) {
    const { age, income, household, children, student, incarcerated, onProbation, fosterYouth } = profile
    const fpl = FPL.forSize(household)
    const fplPct = income / fpl

    let svc = {}

    // ── K-12 Public Education ────────────────────────────────
    // For the person themselves (if school age) or their children
    svc.k12_public_education_cost = 0
    if (age >= 5 && age <= 17) {
      // The person IS a K-12 student
      svc.k12_public_education_cost = K12_PER_PUPIL
    } else if (children > 0 && age >= 25) {
      // Allocate children's education cost
      // Estimate school-age children (rough: kids aged 5-17)
      const schoolAge = Math.min(children, Math.max(0, Math.ceil(children * 0.8)))
      svc.k12_public_education_cost = K12_PER_PUPIL * schoolAge
    }

    // ── Public University Subsidy ────────────────────────────
    svc.public_university_state_subsidy = 0
    if (student && age >= 18 && age <= 26) {
      svc.public_university_state_subsidy = UNIVERSITY_STATE_SUBSIDY
    }

    // ── Hospital Uncompensated Care ──────────────────────────
    // Uninsured people who use ERs — cost absorbed by hospitals
    svc.public_hospital_uncompensated = 0
    const uninsuredRate = getNum(fragments, 'census-health-insurance', 'uninsured_pct') / 100
    if (fplPct <= 2.0 && uninsuredRate > 0.05) {
      // Higher likelihood of uncompensated care in areas with high uninsured rates
      svc.public_hospital_uncompensated = Math.round(UNCOMPENSATED_CARE_PER_UNINSURED * uninsuredRate * 3)
    }

    // ── Community Health Center ──────────────────────────────
    svc.community_health_center = 0
    if (fplPct <= 2.0) {
      svc.community_health_center = COMMUNITY_HEALTH_CENTER_COST
    }

    // ── Criminal Justice ─────────────────────────────────────
    svc.public_defender_cost = 0
    svc.incarceration_cost = 0
    svc.probation_parole_cost = 0

    if (incarcerated) {
      svc.incarceration_cost = INCARCERATION_COST_PER_YEAR
      svc.public_defender_cost = PUBLIC_DEFENDER_COST
    }
    if (onProbation) {
      svc.probation_parole_cost = PROBATION_COST_PER_YEAR
    }

    // ── Foster Care ──────────────────────────────────────────
    svc.foster_care_cost = 0
    if (fosterYouth) {
      svc.foster_care_cost = FOSTER_CARE_COST_PER_YEAR
    }

    // ── Public Transit ───────────────────────────────────────
    svc.public_transit_subsidy_est = 0
    const commutePublicPct = getNum(fragments, 'census-commute', 'public_transit_pct')
    if (commutePublicPct > 5 && !profile.homeowner) {
      // More likely transit rider if renter in transit-served area
      svc.public_transit_subsidy_est = TRANSIT_SUBSIDY_PER_RIDER
    } else if (commutePublicPct > 2) {
      svc.public_transit_subsidy_est = Math.round(TRANSIT_SUBSIDY_PER_RIDER * 0.3)
    }

    // ── Other ────────────────────────────────────────────────
    svc.other_direct_services = 0

    // ── Total ────────────────────────────────────────────────
    svc.total_direct_services = Object.values(svc).reduce((s, v) => s + v, 0)

    return svc
  },
}
