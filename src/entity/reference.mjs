/**
 * ENTITY — Reference data for entity resolution
 *
 * Tax brackets, benefit thresholds, per-capita spending.
 * These are the parameters that turn aggregate fragment data
 * into person-level estimates.
 *
 * Year: 2024 (most recent complete data).
 * Sources: IRS, SSA, USDA-FNS, CMS, CBO, Census of Governments.
 */

// ── Federal Poverty Level (2024) ─────────────────────────────────
// https://aspe.hhs.gov/poverty-guidelines
export const FPL = {
  base: 15060,      // 1 person
  increment: 5380,  // each additional person
  forSize(n) { return this.base + this.increment * Math.max(0, n - 1) },
}

// ── Federal income tax brackets (2024, single) ──────────────────
export const FED_TAX_BRACKETS_SINGLE = [
  { min: 0,       max: 11600,  rate: 0.10 },
  { min: 11600,   max: 47150,  rate: 0.12 },
  { min: 47150,   max: 100525, rate: 0.22 },
  { min: 100525,  max: 191950, rate: 0.24 },
  { min: 191950,  max: 243725, rate: 0.32 },
  { min: 243725,  max: 609350, rate: 0.35 },
  { min: 609350,  max: Infinity, rate: 0.37 },
]

export const FED_TAX_BRACKETS_HOH = [
  { min: 0,       max: 16550,  rate: 0.10 },
  { min: 16550,   max: 63100,  rate: 0.12 },
  { min: 63100,   max: 100500, rate: 0.22 },
  { min: 100500,  max: 191950, rate: 0.24 },
  { min: 191950,  max: 243700, rate: 0.32 },
  { min: 243700,  max: 609350, rate: 0.35 },
  { min: 609350,  max: Infinity, rate: 0.37 },
]

export const FED_TAX_BRACKETS_MFJ = [
  { min: 0,       max: 23200,  rate: 0.10 },
  { min: 23200,   max: 94300,  rate: 0.12 },
  { min: 94300,   max: 201050, rate: 0.22 },
  { min: 201050,  max: 383900, rate: 0.24 },
  { min: 383900,  max: 487450, rate: 0.32 },
  { min: 487450,  max: 731200, rate: 0.35 },
  { min: 731200,  max: Infinity, rate: 0.37 },
]

export const STANDARD_DEDUCTION = {
  single: 14600,
  hoh: 21900,
  mfj: 29200,
}

// ── FICA ─────────────────────────────────────────────────────────
export const FICA = {
  ss_rate: 0.062,
  ss_wage_base: 168600,
  medicare_rate: 0.0145,
}

// ── State tax rates (simplified — flat or effective rate) ────────
// Key = state abbreviation
export const STATE_INCOME_TAX = {
  AL: 0.04, AK: 0, AZ: 0.025, AR: 0.039, CA: 0.06,
  CO: 0.044, CT: 0.05, DE: 0.055, DC: 0.06, FL: 0,
  GA: 0.0549, HI: 0.06, ID: 0.058, IL: 0.0495, IN: 0.0305,
  IA: 0.044, KS: 0.046, KY: 0.04, LA: 0.03, ME: 0.055,
  MD: 0.0475, MA: 0.05, MI: 0.0425, MN: 0.0535, MS: 0.047,
  MO: 0.048, MT: 0.059, NE: 0.0501, NV: 0, NH: 0,
  NJ: 0.0525, NM: 0.039, NY: 0.055, NC: 0.045, ND: 0.0195,
  OH: 0.035, OK: 0.0425, OR: 0.08, PA: 0.0307, RI: 0.0475,
  SC: 0.05, SD: 0, TN: 0, TX: 0, UT: 0.0465,
  VT: 0.055, VA: 0.0475, WA: 0, WV: 0.047, WI: 0.0465,
  WY: 0,
}

// ── State sales tax rates ────────────────────────────────────────
export const STATE_SALES_TAX = {
  AL: 0.04, AK: 0, AZ: 0.056, AR: 0.065, CA: 0.0725,
  CO: 0.029, CT: 0.0635, DE: 0, DC: 0.06, FL: 0.06,
  GA: 0.04, HI: 0.04, ID: 0.06, IL: 0.0625, IN: 0.07,
  IA: 0.06, KS: 0.065, KY: 0.06, LA: 0.0445, ME: 0.055,
  MD: 0.06, MA: 0.0625, MI: 0.06, MN: 0.06875, MS: 0.07,
  MO: 0.04225, MT: 0, NE: 0.055, NV: 0.0685, NH: 0,
  NJ: 0.06625, NM: 0.05125, NY: 0.04, NC: 0.0475, ND: 0.05,
  OH: 0.0575, OK: 0.045, OR: 0, PA: 0.06, RI: 0.07,
  SC: 0.06, SD: 0.042, TN: 0.07, TX: 0.0625, UT: 0.061,
  VT: 0.06, VA: 0.053, WA: 0.065, WV: 0.06, WI: 0.05,
  WY: 0.04,
}

// ── Local wage/income tax (cities with significant local taxes) ──
// Key = FIPS code
export const LOCAL_WAGE_TAX = {
  '42101': 0.0375,   // Philadelphia
  '36061': 0.03078,  // Manhattan / NYC
  '36047': 0.03078,  // Brooklyn / NYC
  '36081': 0.03078,  // Queens / NYC
  '36005': 0.03078,  // Bronx / NYC
  '24510': 0.032,    // Baltimore City
  '39035': 0.02,     // Cuyahoga / Cleveland
  '26163': 0.024,    // Wayne / Detroit
  '11001': 0,        // DC (uses state income tax)
}

// ── Sales tax consumption rate ───────────────────────────────────
// Fraction of after-tax income spent on taxable goods
// Lower income → higher share spent on consumption
export function consumptionRate(income) {
  if (income < 15000) return 0.85
  if (income < 30000) return 0.75
  if (income < 50000) return 0.65
  if (income < 80000) return 0.55
  return 0.45
}

// ── SNAP max allotment (FY2024, 48 contiguous states) ────────────
export const SNAP_MAX = {
  1: 291, 2: 535, 3: 766, 4: 973, 5: 1155, 6: 1386,
  forSize(n) { return this[Math.min(n, 6)] || 291 },
}

// ── EITC (2024) ──────────────────────────────────────────────────
export const EITC = [
  { children: 0, max_credit: 632,  phase_out_start: 9800,   income_limit: 18591 },
  { children: 1, max_credit: 3995, phase_out_start: 21370,  income_limit: 49084 },
  { children: 2, max_credit: 6604, phase_out_start: 21370,  income_limit: 55768 },
  { children: 3, max_credit: 7430, phase_out_start: 21370,  income_limit: 59899 },
]

// ── Child Tax Credit (2024) ──────────────────────────────────────
export const CTC = {
  per_child: 2000,
  refundable_max: 1700,
  phase_out_single: 200000,
  phase_out_mfj: 400000,
  child_max_age: 16,
}

// ── SSI (2024) ───────────────────────────────────────────────────
export const SSI = {
  individual: 943,   // monthly
  couple: 1415,      // monthly
  annual_individual: 943 * 12,
  annual_couple: 1415 * 12,
}

// ── Medicaid per-capita cost (2024 estimates by category) ────────
export const MEDICAID_PER_CAPITA = {
  child: 3500,
  adult: 6200,
  elderly: 18000,
  disabled: 22000,
}

// ── Medicare per-capita (2024) ───────────────────────────────────
export const MEDICARE_PER_CAPITA = 15000

// ── K-12 per-pupil expenditure (national average, use fragment for local) ─
export const K12_PER_PUPIL = 16000

// ── Public university per-student state subsidy ──────────────────
export const UNIVERSITY_STATE_SUBSIDY = 8500

// ── Pell Grant (2024-25) ─────────────────────────────────────────
export const PELL_MAX = 7395

// ── Per-capita collective goods allocation (2024, national) ──────
// Federal: from CBO budget function analysis
export const FEDERAL_COLLECTIVE = {
  defense_per_capita_share: 2685,
  veterans_affairs_per_capita: 896,
  federal_law_enforcement_intel_share: 179,
  diplomacy_foreign_affairs_share: 194,
  fed_infrastructure_share: 299,
  fed_public_health_share: 164,
  fed_environment_share: 36,
  fed_courts_share: 27,
  fed_general_govt_share: 45,
  fed_interest_on_debt_share: 2687,
}

// State: from Census of Governments, national averages
export const STATE_COLLECTIVE = {
  state_police_corrections_share: 350,
  state_infrastructure_share: 420,
  state_courts_share: 140,
  state_public_health_share: 280,
  state_parks_environment_share: 90,
  state_general_govt_share: 250,
}

// Local: from Census of Governments, national averages
export const LOCAL_COLLECTIVE = {
  local_police_share: 480,
  local_fire_ems_share: 280,
  local_roads_share: 310,
  local_water_sewer_share: 260,
  local_parks_rec_share: 155,
  local_library_share: 48,
  local_general_govt_share: 250,
}

// ── Housing ──────────────────────────────────────────────────────
export const SECTION_8_PAYMENT_STANDARD_PCT = 0.40  // 40% of AMI → tenant pays 30% of income

// ── Transit subsidy per rider (national average) ─────────────────
export const TRANSIT_SUBSIDY_PER_RIDER = 1200

// ── Healthcare service costs ─────────────────────────────────────
export const COMMUNITY_HEALTH_CENTER_COST = 950  // per patient per year
export const UNCOMPENSATED_CARE_PER_UNINSURED = 1800

// ── Criminal justice costs ───────────────────────────────────────
export const INCARCERATION_COST_PER_YEAR = 45000
export const PROBATION_COST_PER_YEAR = 3500
export const PUBLIC_DEFENDER_COST = 1200

// ── Foster care ──────────────────────────────────────────────────
export const FOSTER_CARE_COST_PER_YEAR = 35000

// ── WIC ──────────────────────────────────────────────────────────
export const WIC_MONTHLY = 75   // average monthly benefit

// ── TANF (varies wildly, national average) ───────────────────────
export const TANF_MONTHLY = {
  1: 200, 2: 350, 3: 450, 4: 550, 5: 650,
  forSize(n) { return this[Math.min(n, 5)] || 200 },
}

// ── Utility: compute progressive tax ─────────────────────────────
export function progressiveTax(taxableIncome, brackets) {
  let tax = 0
  for (const bracket of brackets) {
    if (taxableIncome <= bracket.min) break
    const taxable = Math.min(taxableIncome, bracket.max) - bracket.min
    tax += taxable * bracket.rate
  }
  return Math.round(tax)
}
