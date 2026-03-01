/**
 * ENTITY — Resolved entity schema
 *
 * Defines every field in a resolved entity record.
 * One record = one person × one county × one year.
 *
 * The lifecycle CSV is the canonical output format.
 * This schema is the source of truth for column order and types.
 */

// ── Identity ─────────────────────────────────────────────────────
export const IDENTITY = [
  'year',
  'age',
  'life_stage',
  'zip_code',
  'city',
  'county',
  'state',
]

// ── Taxes & fees paid (outflows from person to government) ───────
export const TAXES = [
  'fed_income_tax_paid',
  'fica_social_security_paid',
  'fica_medicare_paid',
  'fed_excise_tax_est',
  'fed_other_fees',
  'state_income_tax_paid',
  'state_sales_tax_est',
  'state_excise_tax_est',
  'state_fees',
  'local_income_wage_tax_paid',
  'property_tax_paid',
  'local_fees_fines',
  'total_taxes_fees_paid',
]

// ── Direct benefits received (government → person) ───────────────
export const BENEFITS = [
  'social_security_received',
  'medicare_benefits_received',
  'medicaid_benefits_received',
  'chip_benefits_received',
  'snap_received',
  'wic_received',
  'tanf_received',
  'unemployment_insurance_received',
  'ssi_ssdi_received',
  'aca_premium_subsidy_received',
  'eitc_refundable_received',
  'child_tax_credit_refundable',
  'pell_grant_received',
  'fed_student_loan_subsidy_est',
  'housing_assistance_received',
  'va_benefits_received',
  'other_direct_benefits',
  'total_direct_benefits',
]

// ── Direct services consumed (government services used) ──────────
export const SERVICES = [
  'k12_public_education_cost',
  'public_university_state_subsidy',
  'public_hospital_uncompensated',
  'community_health_center',
  'public_defender_cost',
  'incarceration_cost',
  'probation_parole_cost',
  'foster_care_cost',
  'public_transit_subsidy_est',
  'other_direct_services',
  'total_direct_services',
]

// ── Collective goods allocated (per-capita share) ────────────────
export const COLLECTIVE = [
  // Federal
  'defense_per_capita_share',
  'veterans_affairs_per_capita',
  'federal_law_enforcement_intel_share',
  'diplomacy_foreign_affairs_share',
  'fed_infrastructure_share',
  'fed_public_health_share',
  'fed_environment_share',
  'fed_courts_share',
  'fed_general_govt_share',
  'fed_interest_on_debt_share',
  // State
  'state_police_corrections_share',
  'state_infrastructure_share',
  'state_courts_share',
  'state_public_health_share',
  'state_parks_environment_share',
  'state_general_govt_share',
  // Local
  'local_police_share',
  'local_fire_ems_share',
  'local_roads_share',
  'local_water_sewer_share',
  'local_parks_rec_share',
  'local_library_share',
  'local_general_govt_share',
  'total_collective_allocated',
]

// ── Summary ──────────────────────────────────────────────────────
export const SUMMARY = [
  'total_govt_cost',
  'net_fiscal_impact',
  'cumulative_net_fiscal_impact',
  'data_source_quality',
  'notes',
]

// ── All columns in order (matches lifecycle CSV) ─────────────────
export const ALL_COLUMNS = [
  ...IDENTITY,
  ...TAXES,
  ...BENEFITS,
  ...SERVICES,
  ...COLLECTIVE,
  ...SUMMARY,
]

// ── Life stage from age ──────────────────────────────────────────
export function lifeStage(age) {
  if (age < 1) return 'infant'
  if (age < 5) return 'toddler'
  if (age < 18) return 'K-12'
  if (age < 23) return 'college'
  if (age < 65) return 'working'
  return 'retired'
}

// ── Empty record with all fields zeroed ──────────────────────────
export function emptyRecord() {
  const r = {}
  for (const col of ALL_COLUMNS) {
    r[col] = col === 'data_source_quality' ? 'modeled'
      : col === 'notes' ? ''
      : col === 'life_stage' || col === 'zip_code' || col === 'city' || col === 'county' || col === 'state' ? ''
      : 0
  }
  return r
}
