#!/usr/bin/env node
/**
 * COSM — Dome Assembler
 *
 * Takes all fragments for a geography and assembles them around a single human life.
 * This is the act of financialization — fragmented data organized around a person
 * becomes a financial instrument.
 *
 * The delta between fragmented and coordinated cost IS the financial value of the dome.
 */

import { readFileSync, writeFileSync, mkdirSync, existsSync, readdirSync } from 'node:fs'
import { join, dirname } from 'node:path'
import { fileURLToPath } from 'node:url'

const __dirname = dirname(fileURLToPath(import.meta.url))
const ROOT = join(__dirname, '..', '..')
const DATA = join(ROOT, 'data')
const DOMES = join(DATA, 'domes')
const PATTERNS = join(DATA, 'patterns')
const META = join(DATA, 'meta')

const LAYER_DIRS = {
  1: 'layer-01-legal',
  2: 'layer-02-systems',
  3: 'layer-03-fiscal',
  4: 'layer-04-health',
  5: 'layer-05-housing',
  6: 'layer-06-economic',
  7: 'layer-07-education',
  8: 'layer-08-community',
  9: 'layer-09-environment',
}

// ── File I/O ─────────────────────────────────────────────────────────────────

function readJSON(path) {
  try {
    return JSON.parse(readFileSync(path, 'utf8'))
  } catch {
    return null
  }
}

// ── Meta files — loaded once at startup ──────────────────────────────────────

const TRADITIONS = readJSON(join(META, 'traditions.json'))
const SYNERGY = readJSON(join(META, 'synergy.json'))
const DOMAIN_COSTS = readJSON(join(META, 'costs.json'))

function writeJSON(path, data) {
  mkdirSync(dirname(path), { recursive: true })
  writeFileSync(path, JSON.stringify(data, null, 2) + '\n')
}

// ── Archetype Profiles ───────────────────────────────────────────────────────

const ARCHETYPES = [
  { id: 'marcus', name: 'Marcus', age: 34, income: 28000, household: 3, children: 2, description: 'Single dad, systems-heavy' },
  { id: 'elena', name: 'Elena', age: 29, income: 22000, household: 2, children: 1, description: 'Working poor' },
  { id: 'james', name: 'James', age: 72, income: 14000, household: 1, children: 0, description: 'Elderly disabled' },
  { id: 'rivera', name: 'Rivera Family', age: 38, income: 52000, household: 5, children: 3, description: 'Benefits cliff' },
  { id: 'aisha', name: 'Aisha', age: 19, income: 12000, household: 1, children: 0, description: 'Aged out of foster care' },
  { id: 'median', name: 'Median', age: 38, income: 59540, household: 2, children: 1, description: 'Benchmark' },
]

// ── Counties ─────────────────────────────────────────────────────────────────

const COUNTIES = [
  { fips: '42101', name: 'Philadelphia, PA' },
  { fips: '42045', name: 'Delaware County, PA' },
  { fips: '42091', name: 'Montgomery County, PA' },
  { fips: '42017', name: 'Bucks County, PA' },
  { fips: '42029', name: 'Chester County, PA' },
  { fips: '36061', name: 'New York County (Manhattan), NY' },
  { fips: '36047', name: 'Kings County (Brooklyn), NY' },
  { fips: '36081', name: 'Queens County, NY' },
  { fips: '36005', name: 'Bronx County, NY' },
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
  { fips: '21013', name: 'Bell County, KY' },
  { fips: '54055', name: 'Mercer County, WV' },
  { fips: '28049', name: 'Hinds County (Jackson), MS' },
  { fips: '01073', name: 'Jefferson County (Birmingham), AL' },
  { fips: '26163', name: 'Wayne County (Detroit), MI' },
  { fips: '39035', name: 'Cuyahoga County (Cleveland), OH' },
  { fips: '34013', name: 'Essex County, NJ' },
  { fips: '34017', name: 'Hudson County, NJ' },
  { fips: '34023', name: 'Middlesex County, NJ' },
]

// ── Federal Poverty Level (2024) ─────────────────────────────────────────────

function federalPovertyLevel(household) {
  // 2024 FPL for 48 contiguous states
  const base = 15060
  const perPerson = 5380
  return base + perPerson * (household - 1)
}

function pctFPL(income, household) {
  return income / federalPovertyLevel(household)
}

// ── Program Eligibility Engine ───────────────────────────────────────────────
// Real eligibility thresholds and conservative benefit estimates

function determineEligibility(profile, fragments) {
  const fpl = pctFPL(profile.income, profile.household)
  const programs = []

  // Get local data if available
  const housing = fragments['census-housing']?.data || {}
  const income = fragments['census-income']?.data || {}
  const medianRent = housing.median_gross_rent || 1200

  // ── Medicaid (138% FPL under ACA expansion, varies by state)
  if (fpl <= 1.38) {
    const annualValue = profile.age >= 65 ? 12000 : profile.children > 0 ? 8500 : 6500
    programs.push({
      program: 'Medicaid',
      eligible: true,
      threshold: '138% FPL',
      fpl_pct: Math.round(fpl * 100),
      annual_value: annualValue,
      category: 'health',
      note: 'ACA expansion states; non-expansion states use lower thresholds',
    })
  }

  // ── CHIP (Children's Health Insurance Program, up to 200-300% FPL)
  if (profile.children > 0 && fpl <= 2.50) {
    programs.push({
      program: 'CHIP',
      eligible: true,
      threshold: '250% FPL (varies by state)',
      fpl_pct: Math.round(fpl * 100),
      annual_value: 2800 * profile.children,
      category: 'health',
    })
  }

  // ── SNAP (Supplemental Nutrition Assistance Program, 130% FPL gross)
  if (fpl <= 1.30) {
    // Max monthly SNAP benefit by household size (FY2024)
    const maxSnap = { 1: 291, 2: 535, 3: 766, 4: 973, 5: 1155 }
    const monthly = maxSnap[Math.min(profile.household, 5)] || 291
    // Actual benefit is max minus 30% of net income — estimate conservatively at 70%
    const estimatedMonthly = Math.round(monthly * 0.70)
    programs.push({
      program: 'SNAP',
      eligible: true,
      threshold: '130% FPL gross income',
      fpl_pct: Math.round(fpl * 100),
      annual_value: estimatedMonthly * 12,
      monthly_value: estimatedMonthly,
      category: 'nutrition',
    })
  }

  // ── Section 8 Housing Choice Voucher (50% AMI)
  // Use local median income if available
  const localMedian = income.median_household_income || 75000
  const amiThreshold = localMedian * 0.50
  if (profile.income <= amiThreshold) {
    // Fair Market Rent standard — voucher covers gap between 30% of income and FMR
    const tenantPortion = Math.round(profile.income * 0.30 / 12)
    const voucherValue = Math.max(0, medianRent - tenantPortion)
    programs.push({
      program: 'Section 8 HCV',
      eligible: true,
      threshold: '50% Area Median Income',
      income_limit: Math.round(amiThreshold),
      annual_value: voucherValue * 12,
      monthly_value: voucherValue,
      category: 'housing',
      note: 'Extreme waitlist — average 2-5 year wait nationwide',
    })
  }

  // ── EITC (Earned Income Tax Credit)
  if (profile.income > 0) {
    const eitcLimits = {
      0: { max_income: 17640, max_credit: 632 },
      1: { max_income: 46560, max_credit: 3995 },
      2: { max_income: 52918, max_credit: 6604 },
      3: { max_income: 56838, max_credit: 7430 },
    }
    const kids = Math.min(profile.children, 3)
    const eitc = eitcLimits[kids]
    if (profile.income <= eitc.max_income) {
      // Phase-in/phase-out — estimate conservatively at 60% of max
      const estimatedCredit = Math.round(eitc.max_credit * 0.60)
      programs.push({
        program: 'EITC',
        eligible: true,
        threshold: `Income <= $${eitc.max_income.toLocaleString()} (${kids} children)`,
        annual_value: estimatedCredit,
        category: 'economics',
      })
    }
  }

  // ── WIC (Women, Infants, Children — 185% FPL)
  if (profile.children > 0 && fpl <= 1.85) {
    const wicChildren = Math.min(profile.children, 3)
    programs.push({
      program: 'WIC',
      eligible: true,
      threshold: '185% FPL',
      fpl_pct: Math.round(fpl * 100),
      annual_value: 600 * wicChildren, // ~$50/month per participant
      category: 'nutrition',
      note: 'For pregnant/postpartum women and children under 5',
    })
  }

  // ── LIHEAP (Low Income Home Energy Assistance — 150% FPL or 60% state median)
  if (fpl <= 1.50) {
    programs.push({
      program: 'LIHEAP',
      eligible: true,
      threshold: '150% FPL',
      fpl_pct: Math.round(fpl * 100),
      annual_value: 500, // Conservative — average grant ~$500
      category: 'housing',
      note: 'One-time annual benefit, varies widely by state',
    })
  }

  // ── Head Start (100% FPL, children 3-5)
  if (profile.children > 0 && fpl <= 1.00) {
    programs.push({
      program: 'Head Start',
      eligible: true,
      threshold: '100% FPL',
      fpl_pct: Math.round(fpl * 100),
      annual_value: 10000, // Per-child cost to government
      category: 'education',
      note: 'For children ages 3-5; Early Head Start for under 3',
    })
  }

  // ── Free School Lunch (NSLP — 130% FPL)
  if (profile.children > 0 && fpl <= 1.30) {
    programs.push({
      program: 'Free School Lunch',
      eligible: true,
      threshold: '130% FPL',
      fpl_pct: Math.round(fpl * 100),
      annual_value: 1200 * profile.children, // ~$6/day * 200 school days
      category: 'nutrition',
    })
  }

  // ── Reduced School Lunch (185% FPL)
  if (profile.children > 0 && fpl > 1.30 && fpl <= 1.85) {
    programs.push({
      program: 'Reduced School Lunch',
      eligible: true,
      threshold: '185% FPL',
      fpl_pct: Math.round(fpl * 100),
      annual_value: 800 * profile.children,
      category: 'nutrition',
    })
  }

  // ── SSI (Supplemental Security Income — disabled/elderly, income < ~$943/month)
  if ((profile.age >= 65 || profile.description?.includes('disabled')) && profile.income < 11316) {
    const maxSSI = 943 // 2024 monthly max
    const countableIncome = Math.max(0, (profile.income / 12) - 20) // $20 general exclusion
    const monthlyBenefit = Math.max(0, Math.round(maxSSI - countableIncome))
    programs.push({
      program: 'SSI',
      eligible: true,
      threshold: 'Limited income and resources, age 65+ or disabled',
      annual_value: monthlyBenefit * 12,
      monthly_value: monthlyBenefit,
      category: 'economics',
    })
  }

  // ── TANF (Temporary Assistance for Needy Families — varies wildly by state)
  if (profile.children > 0 && fpl <= 1.00) {
    // TANF benefits range from $170/month (MS) to $1,000/month (NH). Use conservative median.
    const monthlyTANF = 400
    programs.push({
      program: 'TANF',
      eligible: true,
      threshold: '~100% FPL (varies by state)',
      fpl_pct: Math.round(fpl * 100),
      annual_value: monthlyTANF * 12,
      monthly_value: monthlyTANF,
      category: 'economics',
      note: 'Highly variable by state; 60-month lifetime limit',
    })
  }

  // ── Pell Grant (for students — EFC-based, effectively < ~$60k family income)
  if (profile.age >= 17 && profile.age <= 30 && profile.income < 60000) {
    const maxPell = 7395 // 2024-25
    // Rough estimate based on income
    const estimatedPell = profile.income < 30000 ? maxPell : Math.round(maxPell * 0.50)
    programs.push({
      program: 'Pell Grant',
      eligible: true,
      threshold: 'EFC-based (effectively < ~$60k family income)',
      annual_value: estimatedPell,
      category: 'education',
      note: 'For enrolled students only; assumes enrollment',
    })
  }

  return programs
}

// ── Extract Conditions of Existence ──────────────────────────────────────────

function extractConditions(fragments) {
  const conditions = {}

  const housing = fragments['census-housing']?.data
  if (housing) {
    conditions.median_rent = housing.median_gross_rent
    conditions.median_home_value = housing.median_home_value
    conditions.vacancy_rate = housing.total_units > 0
      ? Math.round((housing.vacant_units / housing.total_units) * 1000) / 10
      : null
    conditions.ownership_rate = housing.occupied_units > 0
      ? Math.round((housing.owner_occupied / housing.occupied_units) * 1000) / 10
      : null
  }

  const rentBurden = fragments['census-rent-burden']?.data
  if (rentBurden && rentBurden.rent_total > 0) {
    const burdened = (rentBurden.rent_30_35_pct || 0) + (rentBurden.rent_35_40_pct || 0) +
      (rentBurden.rent_40_50_pct || 0) + (rentBurden.rent_50_plus_pct || 0)
    conditions.rent_burdened_pct = Math.round((burdened / rentBurden.rent_total) * 1000) / 10
    conditions.severely_burdened_pct = rentBurden.rent_total > 0
      ? Math.round(((rentBurden.rent_50_plus_pct || 0) / rentBurden.rent_total) * 1000) / 10
      : null
  }

  const incomeData = fragments['census-income']?.data
  if (incomeData) {
    conditions.median_household_income = incomeData.median_household_income
    conditions.per_capita_income = incomeData.per_capita_income
    conditions.poverty_rate = incomeData.poverty_total > 0
      ? Math.round((incomeData.poverty_below / incomeData.poverty_total) * 1000) / 10
      : null
    conditions.gini_index = incomeData.gini_index
    conditions.snap_households = incomeData.snap_households
  }

  const demographics = fragments['census-demographics']?.data
  if (demographics) {
    conditions.total_population = demographics.total_pop
    conditions.median_age = demographics.median_age
  }

  const health = fragments['census-health-insurance']?.data
  if (health) {
    conditions.uninsured_estimate = health.total_pop_insurance > 0
      ? Math.round(((health.total_pop_insurance - (health.with_insurance || 0)) / health.total_pop_insurance) * 1000) / 10
      : null
    conditions.medicaid_enrolled = health.medicaid_means_tested
  }

  const disability = fragments['census-disability']?.data
  if (disability && disability.total_disability_pop > 0) {
    const withDisability = (disability.male_with_disability || 0) + (disability.female_with_disability || 0)
    conditions.disability_rate = Math.round((withDisability / disability.total_disability_pop) * 1000) / 10
  }

  const education = fragments['census-education']?.data
  if (education && education.edu_pop_25plus > 0) {
    conditions.bachelors_plus_pct = Math.round(
      (((education.bachelors || 0) + (education.masters || 0) + (education.doctorate || 0)) / education.edu_pop_25plus) * 1000
    ) / 10
  }

  const commute = fragments['census-commute']?.data
  if (commute) {
    conditions.public_transit_pct = commute.workers_total > 0
      ? Math.round((commute.public_transit / commute.workers_total) * 1000) / 10
      : null
    conditions.work_from_home_pct = commute.workers_total > 0
      ? Math.round((commute.worked_from_home / commute.workers_total) * 1000) / 10
      : null
    conditions.no_vehicle_pct = commute.workers_total > 0
      ? Math.round((commute.no_vehicle / commute.workers_total) * 1000) / 10
      : null
  }

  const internet = fragments['census-internet']?.data
  if (internet && internet.total_households_internet > 0) {
    conditions.broadband_pct = Math.round((internet.broadband / internet.total_households_internet) * 1000) / 10
    conditions.no_internet_pct = Math.round((internet.no_internet / internet.total_households_internet) * 1000) / 10
  }

  const employment = fragments['census-employment']?.data
  if (employment && employment.in_labor_force > 0) {
    conditions.unemployment_rate = Math.round((employment.civilian_unemployed / employment.in_labor_force) * 1000) / 10
  }

  const bls = fragments['bls-unemployment']?.data
  if (bls) {
    conditions.state_unemployment_rate = bls.latest_rate
    conditions.state_unemployment_period = bls.latest_period
  }

  return conditions
}

// ── Calculate Fragmented & Coordinated Costs ─────────────────────────────────

function calculateCosts(programs) {
  if (programs.length === 0) {
    return { fragmented: 0, coordinated: 0, delta: 0, admin_overhead: 0 }
  }

  // Total direct benefit value across all programs
  const directValue = programs.reduce((sum, p) => sum + (p.annual_value || 0), 0)

  // Administrative overhead in fragmented system:
  // Each program has its own application, eligibility determination, case management,
  // compliance, reporting. Research shows 20-40% admin overhead. Use 30% conservatively.
  const adminOverheadRate = 0.30
  const adminOverhead = Math.round(directValue * adminOverheadRate)

  // Fragmented cost = direct benefits + admin overhead
  const fragmented = directValue + adminOverhead

  // Coordinated cost reduction:
  // Single intake, shared eligibility, unified case management.
  // Research estimates 25-50% admin reduction, plus 10-15% better outcomes.
  // We use conservative 40% total reduction (underestimate, never overestimate).
  const coordinationSavingsRate = 0.40
  const coordinated = Math.round(fragmented * (1 - coordinationSavingsRate))

  const delta = fragmented - coordinated

  return {
    fragmented,
    coordinated,
    delta,
    direct_benefit_value: directValue,
    admin_overhead: adminOverhead,
    admin_overhead_rate: adminOverheadRate,
    coordination_savings_rate: coordinationSavingsRate,
    program_count: programs.length,
  }
}

// ── Domain Coverage — the 12 domains of existence ────────────────────────────

function calculateDomainCoverage(fragments, conditions, programs) {
  // Cosm = minimum coverage across all domains
  // A dome with perfect health data but no housing data has low Cosm
  const domains = {
    health: {
      fragments: ['census-health-insurance', 'census-disability'],
      programs: ['Medicaid', 'CHIP'],
      conditions: ['uninsured_estimate', 'disability_rate', 'medicaid_enrolled'],
    },
    housing: {
      fragments: ['census-housing', 'census-rent-burden', 'hud-fmr'],
      programs: ['Section 8 HCV', 'LIHEAP'],
      conditions: ['median_rent', 'vacancy_rate', 'ownership_rate', 'rent_burdened_pct'],
    },
    economics: {
      fragments: ['census-income', 'census-employment', 'bls-unemployment'],
      programs: ['EITC', 'SSI', 'TANF'],
      conditions: ['median_household_income', 'poverty_rate', 'unemployment_rate', 'gini_index'],
    },
    education: {
      fragments: ['census-education'],
      programs: ['Head Start', 'Pell Grant'],
      conditions: ['bachelors_plus_pct'],
    },
    nutrition: {
      fragments: ['census-income', 'usda-food-access'],
      programs: ['SNAP', 'WIC', 'Free School Lunch', 'Reduced School Lunch'],
      conditions: ['snap_households'],
    },
    safety: {
      fragments: ['fbi-crime', 'fema-disasters'],
      programs: [],
      conditions: [],
    },
    transportation: {
      fragments: ['census-commute'],
      programs: [],
      conditions: ['public_transit_pct', 'no_vehicle_pct', 'work_from_home_pct'],
    },
    infrastructure: {
      fragments: ['census-internet'],
      programs: [],
      conditions: ['broadband_pct', 'no_internet_pct'],
    },
    environment: {
      fragments: ['epa-air-quality'],
      programs: [],
      conditions: [],
    },
    legal: {
      fragments: [],
      programs: [],
      conditions: [],
      note: 'Legal framework data not yet scraped — future fragment source',
    },
    community: {
      fragments: ['census-demographics'],
      programs: [],
      conditions: ['total_population', 'median_age'],
    },
    purpose: {
      fragments: ['census-education', 'census-employment'],
      programs: [],
      conditions: ['bachelors_plus_pct', 'unemployment_rate'],
    },
  }

  const coverage = {}
  const gaps = []

  for (const [domain, spec] of Object.entries(domains)) {
    // Calculate coverage score (0-100) based on data availability
    let score = 0
    let maxScore = 0

    // Fragment availability (40% of score)
    if (spec.fragments.length > 0) {
      maxScore += 40
      const available = spec.fragments.filter(f => fragments[f]).length
      score += Math.round((available / spec.fragments.length) * 40)
      if (available < spec.fragments.length) {
        const missing = spec.fragments.filter(f => !fragments[f])
        gaps.push({ domain, type: 'fragment', missing })
      }
    } else {
      maxScore += 40
      gaps.push({ domain, type: 'fragment', missing: ['no sources defined'] })
    }

    // Condition extraction (40% of score)
    if (spec.conditions.length > 0) {
      maxScore += 40
      const extracted = spec.conditions.filter(c => conditions[c] !== undefined && conditions[c] !== null).length
      score += Math.round((extracted / spec.conditions.length) * 40)
      if (extracted < spec.conditions.length) {
        const missing = spec.conditions.filter(c => conditions[c] === undefined || conditions[c] === null)
        gaps.push({ domain, type: 'condition', missing })
      }
    } else {
      maxScore += 40
      gaps.push({ domain, type: 'condition', missing: ['no conditions defined'] })
    }

    // Program coverage (20% of score)
    if (spec.programs.length > 0) {
      maxScore += 20
      const eligible = spec.programs.filter(p => programs.some(ep => ep.program === p)).length
      score += Math.round((eligible / spec.programs.length) * 20)
    } else {
      maxScore += 20
      score += 10 // Half credit for domains without program eligibility
    }

    coverage[domain] = {
      score: maxScore > 0 ? Math.round((score / maxScore) * 100) : 0,
      raw_score: score,
      max_score: maxScore,
      note: spec.note || null,
    }
  }

  return { coverage, gaps }
}

// ── Load all fragments for a FIPS ────────────────────────────────────────────
// Reads from data/layer-*/{source-id}/{fips}.json — deduplicates by source ID
// since the same fragment can live in multiple layer directories.

function loadFragments(fips) {
  const result = {}

  for (const layerDir of Object.values(LAYER_DIRS)) {
    const dir = join(DATA, layerDir)
    if (!existsSync(dir)) continue
    for (const sourceDir of readdirSync(dir)) {
      if (result[sourceDir]) continue // already loaded from an earlier layer
      const filePath = join(dir, sourceDir, `${fips}.json`)
      const fragment = readJSON(filePath)
      if (fragment) {
        result[sourceDir] = fragment
      }
    }
  }

  return { fragments: result, count: Object.keys(result).length }
}

// ── Tradition Scoring ────────────────────────────────────────────────────────
// Score each dome through each philosophical tradition's weight matrix.

function scoreByTraditions(domainCoverage) {
  if (!TRADITIONS?.traditions) return null

  const scores = {}
  for (const [tid, tradition] of Object.entries(TRADITIONS.traditions)) {
    const weights = tradition.weights
    let weightedSum = 0
    let totalWeight = 0
    for (const [domain, weight] of Object.entries(weights)) {
      const domScore = domainCoverage[domain]?.score ?? 0
      weightedSum += domScore * weight
      totalWeight += weight
    }
    scores[tid] = {
      name: tradition.name,
      tradition: tradition.tradition,
      score: totalWeight > 0 ? Math.round(weightedSum / totalWeight) : 0,
    }
  }
  return scores
}

// ── Synergy Propagation ──────────────────────────────────────────────────────
// Given domain scores, propagate improvements through the synergy graph.
// One pass: for each edge, add (source_score * weight * 0.15) to the target.
// The 0.15 damping prevents runaway feedback while showing real connections.

function applySynergy(domainCoverage) {
  if (!SYNERGY?.edges) return domainCoverage

  // Start with raw scores
  const raw = {}
  const propagated = {}
  for (const [domain, cov] of Object.entries(domainCoverage)) {
    raw[domain] = cov.score
    propagated[domain] = 0
  }

  const DAMPING = 0.15

  for (const edge of SYNERGY.edges) {
    if (raw[edge.from] !== undefined && raw[edge.to] !== undefined) {
      propagated[edge.to] += raw[edge.from] * edge.weight * DAMPING
    }
  }

  // Merge: synergy-adjusted score = raw + propagated, capped at 100
  const adjusted = {}
  for (const [domain, cov] of Object.entries(domainCoverage)) {
    const boost = Math.round(propagated[domain] || 0)
    adjusted[domain] = {
      ...cov,
      score: Math.min(100, cov.score + boost),
      raw_score_before_synergy: cov.score,
      synergy_boost: boost,
    }
  }
  return adjusted
}

// ── Domain Cost Estimates ────────────────────────────────────────────────────
// For each domain, estimate: current cost burden, improvement cost, and savings.

function estimateDomainCosts(domainCoverage) {
  if (!DOMAIN_COSTS?.domains) return null

  const estimates = {}
  for (const [domain, cov] of Object.entries(domainCoverage)) {
    const costData = DOMAIN_COSTS.domains[domain]
    if (!costData) continue

    const score = cov.score
    const gap = 100 - score
    const gapFraction = gap / 100

    // Current cost burden: proportional to how far domain is from 100
    const currentBurden = Math.round(costData.cost_at_zero * gapFraction)
    // Cost to reach sufficiency (score=70): invest cost_per_tenth for each 10 points needed
    const tenthsToSufficiency = Math.max(0, Math.ceil((70 - score) / 10))
    const investmentToSufficiency = tenthsToSufficiency * costData.cost_per_tenth
    // Savings = burden reduction from reaching sufficiency
    const sufficiencyBurden = Math.round(costData.cost_at_zero * 0.30) // 30% burden remains at score=70
    const savingsAtSufficiency = Math.max(0, currentBurden - sufficiencyBurden)

    estimates[domain] = {
      score,
      current_annual_burden: currentBurden,
      investment_to_sufficiency: investmentToSufficiency,
      annual_savings_at_sufficiency: savingsAtSufficiency,
      tenths_needed: tenthsToSufficiency,
    }
  }

  const totalBurden = Object.values(estimates).reduce((s, e) => s + e.current_annual_burden, 0)
  const totalInvestment = Object.values(estimates).reduce((s, e) => s + e.investment_to_sufficiency, 0)
  const totalSavings = Object.values(estimates).reduce((s, e) => s + e.annual_savings_at_sufficiency, 0)

  return { by_domain: estimates, total_annual_burden: totalBurden, total_investment_to_sufficiency: totalInvestment, total_annual_savings: totalSavings }
}

// ── Assemble a single dome ───────────────────────────────────────────────────

function assembleDome(profile, fips, countyName) {
  const { fragments, count: fragmentsUsed } = loadFragments(fips)

  if (fragmentsUsed === 0) {
    return null // No fragments available for this geography
  }

  // 1. Determine program eligibility
  const eligiblePrograms = determineEligibility(profile, fragments)

  // 2. Extract conditions of existence
  const conditions = extractConditions(fragments)

  // 3. Calculate costs
  const costs = calculateCosts(eligiblePrograms)

  // 4. Calculate domain coverage
  const { coverage: rawCoverage, gaps } = calculateDomainCoverage(fragments, conditions, eligiblePrograms)

  // 5. Apply synergy propagation — connected domains boost each other
  const domainCoverage = applySynergy(rawCoverage)

  // 6. Cosm score = MINIMUM coverage across all 12 domains
  const domainScores = Object.values(domainCoverage).map(d => d.score)
  const cosmScore = Math.min(...domainScores)
  const cosmAverage = Math.round(domainScores.reduce((a, b) => a + b, 0) / domainScores.length)

  // 7. Score through philosophical traditions
  const traditionScores = scoreByTraditions(domainCoverage)

  // 8. Estimate per-domain costs and investment needs
  const domainCostEstimates = estimateDomainCosts(domainCoverage)

  // 9. Build panels — the narrative explanation for each domain
  const panels = {}
  for (const [domain, cov] of Object.entries(domainCoverage)) {
    const relevantPrograms = eligiblePrograms.filter(p => p.category === domain)
    panels[domain] = {
      score: cov.score,
      synergy_boost: cov.synergy_boost || 0,
      programs: relevantPrograms.map(p => p.program),
      program_value: relevantPrograms.reduce((s, p) => s + (p.annual_value || 0), 0),
    }
  }

  return {
    // Identity
    fips,
    county_name: countyName,
    profile: {
      id: profile.id,
      name: profile.name,
      age: profile.age,
      income: profile.income,
      household: profile.household,
      children: profile.children,
      description: profile.description,
    },
    assembled_at: new Date().toISOString(),

    // Data
    fragments_used: fragmentsUsed,
    fragment_sources: Object.keys(fragments),

    // Programs
    eligible_programs: eligiblePrograms,
    program_count: eligiblePrograms.length,

    // Costs — the financial instrument
    fragmented_cost: costs.fragmented,
    coordinated_cost: costs.coordinated,
    delta: costs.delta,
    cost_detail: costs,

    // Cosm score
    cosm: cosmScore,
    cosm_average: cosmAverage,
    domain_coverage: domainCoverage,

    // Tradition scores — same dome through 8 lenses
    tradition_scores: traditionScores,

    // Domain cost estimates — per-domain investment analysis
    domain_costs: domainCostEstimates,

    // Gaps
    gaps,
    gap_count: gaps.length,

    // Conditions of existence
    conditions,

    // Panels
    panels,
  }
}

// ── Detect Cross-Dome Patterns ───────────────────────────────────────────────

function detectPatterns(allDomes) {
  const patterns = {
    generated_at: new Date().toISOString(),
    dome_count: allDomes.length,
    geographic_deltas: [],
    common_gaps: {},
    program_clusters: {},
    archetype_patterns: {},
    cosm_distribution: { min: 100, max: 0, median: 0, by_geography: {} },
    savings_total: 0,
  }

  if (allDomes.length === 0) return patterns

  // Geographic deltas — compare same archetype across geographies
  const byArchetype = {}
  for (const dome of allDomes) {
    const id = dome.profile.id
    if (!byArchetype[id]) byArchetype[id] = []
    byArchetype[id].push(dome)
  }

  for (const [archId, domes] of Object.entries(byArchetype)) {
    if (domes.length < 2) continue

    const sorted = [...domes].sort((a, b) => b.delta - a.delta)
    const highest = sorted[0]
    const lowest = sorted[sorted.length - 1]

    if (highest.delta - lowest.delta > 1000) {
      patterns.geographic_deltas.push({
        archetype: archId,
        highest_delta: { fips: highest.fips, county: highest.county_name, delta: highest.delta },
        lowest_delta: { fips: lowest.fips, county: lowest.county_name, delta: lowest.delta },
        spread: highest.delta - lowest.delta,
      })
    }

    patterns.archetype_patterns[archId] = {
      domes: domes.length,
      avg_cosm: Math.round(domes.reduce((s, d) => s + d.cosm, 0) / domes.length),
      avg_delta: Math.round(domes.reduce((s, d) => s + d.delta, 0) / domes.length),
      avg_programs: Math.round(domes.reduce((s, d) => s + d.program_count, 0) / domes.length * 10) / 10,
    }
  }

  // Common gaps
  const gapCounts = {}
  for (const dome of allDomes) {
    for (const gap of dome.gaps) {
      const key = `${gap.domain}:${gap.type}`
      gapCounts[key] = (gapCounts[key] || 0) + 1
    }
  }
  patterns.common_gaps = Object.fromEntries(
    Object.entries(gapCounts).sort((a, b) => b[1] - a[1]).slice(0, 20)
  )

  // Program clusters
  const programCounts = {}
  for (const dome of allDomes) {
    for (const p of dome.eligible_programs) {
      programCounts[p.program] = (programCounts[p.program] || 0) + 1
    }
  }
  patterns.program_clusters = programCounts

  // Cosm distribution
  const cosmScores = allDomes.map(d => d.cosm).sort((a, b) => a - b)
  patterns.cosm_distribution.min = cosmScores[0]
  patterns.cosm_distribution.max = cosmScores[cosmScores.length - 1]
  patterns.cosm_distribution.median = cosmScores[Math.floor(cosmScores.length / 2)]

  // By geography
  const byGeo = {}
  for (const dome of allDomes) {
    if (!byGeo[dome.fips]) byGeo[dome.fips] = { name: dome.county_name, domes: 0, avg_cosm: 0, total_delta: 0 }
    byGeo[dome.fips].domes++
    byGeo[dome.fips].avg_cosm += dome.cosm
    byGeo[dome.fips].total_delta += dome.delta
  }
  for (const geo of Object.values(byGeo)) {
    geo.avg_cosm = Math.round(geo.avg_cosm / geo.domes)
  }
  patterns.cosm_distribution.by_geography = byGeo

  // Total savings identified
  patterns.savings_total = allDomes.reduce((s, d) => s + d.delta, 0)

  return patterns
}

// ── Update cosm.json — the evolving currency state ───────────────────────────

function updateCosmState(allDomes, patterns) {
  const existingState = readJSON(join(DATA, 'cosm.json')) || {
    created_at: new Date().toISOString(),
    version: 0,
  }

  const cosmScores = allDomes.map(d => d.cosm)

  const state = {
    ...existingState,
    updated_at: new Date().toISOString(),
    version: (existingState.version || 0) + 1,

    // Dome inventory
    total_domes: allDomes.length,
    geographies: [...new Set(allDomes.map(d => d.fips))].length,
    archetypes: [...new Set(allDomes.map(d => d.profile.id))].length,

    // Cosm metrics
    average_cosm: cosmScores.length > 0 ? Math.round(cosmScores.reduce((a, b) => a + b, 0) / cosmScores.length) : 0,
    min_cosm: cosmScores.length > 0 ? Math.min(...cosmScores) : 0,
    max_cosm: cosmScores.length > 0 ? Math.max(...cosmScores) : 0,
    median_cosm: cosmScores.length > 0 ? cosmScores.sort((a, b) => a - b)[Math.floor(cosmScores.length / 2)] : 0,

    // Financial
    total_fragmented_cost: allDomes.reduce((s, d) => s + d.fragmented_cost, 0),
    total_coordinated_cost: allDomes.reduce((s, d) => s + d.coordinated_cost, 0),
    total_coordination_savings: patterns.savings_total,
    average_delta_per_dome: allDomes.length > 0 ? Math.round(patterns.savings_total / allDomes.length) : 0,

    // Maturity — how complete is the data?
    maturity: calculateMaturity(allDomes),

    // Coverage
    programs_mapped: [...new Set(allDomes.flatMap(d => d.eligible_programs.map(p => p.program)))].length,
    total_gap_count: allDomes.reduce((s, d) => s + d.gap_count, 0),
  }

  return state
}

function calculateMaturity(domes) {
  if (domes.length === 0) return { level: 'seed', score: 0, label: 'No domes assembled' }

  const avgCosm = domes.reduce((s, d) => s + d.cosm, 0) / domes.length
  const geos = new Set(domes.map(d => d.fips)).size

  if (avgCosm >= 60 && geos >= 20) return { level: 'mature', score: 4, label: 'High coverage, broad geography' }
  if (avgCosm >= 40 && geos >= 10) return { level: 'growing', score: 3, label: 'Good coverage, expanding geography' }
  if (avgCosm >= 20 && geos >= 5) return { level: 'emerging', score: 2, label: 'Building coverage' }
  if (domes.length >= 5) return { level: 'seedling', score: 1, label: 'Initial domes assembled' }
  return { level: 'seed', score: 0, label: 'Just starting' }
}

// ── Main ─────────────────────────────────────────────────────────────────────

async function run() {
  console.log('\n╔══════════════════════════════════════════╗')
  console.log('║          COSM — Dome Assembler           ║')
  console.log('╚══════════════════════════════════════════╝\n')

  const startTime = Date.now()
  const allDomes = []
  let assembled = 0
  let skipped = 0

  for (const county of COUNTIES) {
    // Check if we have ANY fragments for this county
    const { count } = loadFragments(county.fips)
    if (count === 0) {
      console.log(`  [${county.fips}] ${county.name} — no fragments, skipping`)
      skipped++
      continue
    }

    console.log(`  [${county.fips}] ${county.name} — ${count} fragments`)

    for (const archetype of ARCHETYPES) {
      const dome = assembleDome(archetype, county.fips, county.name)
      if (dome) {
        const outPath = join(DOMES, county.fips, `${archetype.id}.json`)
        writeJSON(outPath, dome)
        allDomes.push(dome)
        assembled++
        console.log(`    → ${archetype.name}: cosm=${dome.cosm}, delta=$${dome.delta.toLocaleString()}, programs=${dome.program_count}`)
      }
    }
  }

  // Detect patterns
  console.log('\n── Detecting patterns ──────────────────────')
  const patterns = detectPatterns(allDomes)
  writeJSON(join(PATTERNS, 'latest.json'), patterns)
  console.log(`  Geographic deltas: ${patterns.geographic_deltas.length}`)
  console.log(`  Common gaps: ${Object.keys(patterns.common_gaps).length}`)
  console.log(`  Program clusters: ${Object.keys(patterns.program_clusters).length}`)

  // Update cosm.json
  const cosmState = updateCosmState(allDomes, patterns)
  writeJSON(join(DATA, 'cosm.json'), cosmState)

  const elapsed = ((Date.now() - startTime) / 1000).toFixed(1)

  console.log('\n── Results ─────────────────────────────────')
  console.log(`  Domes assembled:   ${assembled}`)
  console.log(`  Geographies:       ${cosmState.geographies}`)
  console.log(`  Skipped (no data): ${skipped}`)
  console.log(`  Average Cosm:      ${cosmState.average_cosm}`)
  console.log(`  Total savings:     $${patterns.savings_total.toLocaleString()}`)
  console.log(`  Maturity:          ${cosmState.maturity.level} — ${cosmState.maturity.label}`)
  console.log(`  Time:              ${elapsed}s`)
  console.log('────────────────────────────────────────────\n')

  return { assembled, skipped, total_savings: patterns.savings_total }
}

run().then(result => {
  process.exit(0)
}).catch(err => {
  console.error('COSM FATAL:', err)
  process.exit(1)
})
