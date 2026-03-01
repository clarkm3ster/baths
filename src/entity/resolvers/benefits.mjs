/**
 * ENTITY RESOLVER — Direct Benefits
 *
 * Resolves: What does this person receive from government?
 *
 * Social Security, Medicare, Medicaid, CHIP, SNAP, WIC, TANF,
 * UI, SSI/SSDI, ACA subsidies, EITC, CTC, Pell, student loans,
 * housing assistance, VA benefits.
 *
 * Uses archetype profile + fragment context for local conditions.
 */

import { getNum } from '../fragments.mjs'
import {
  FPL, SNAP_MAX, EITC, CTC, SSI, PELL_MAX,
  MEDICAID_PER_CAPITA, MEDICARE_PER_CAPITA,
  WIC_MONTHLY, TANF_MONTHLY, SECTION_8_PAYMENT_STANDARD_PCT,
} from '../reference.mjs'

export default {
  id: 'benefits',
  fields: [
    'social_security_received', 'medicare_benefits_received',
    'medicaid_benefits_received', 'chip_benefits_received',
    'snap_received', 'wic_received', 'tanf_received',
    'unemployment_insurance_received', 'ssi_ssdi_received',
    'aca_premium_subsidy_received', 'eitc_refundable_received',
    'child_tax_credit_refundable', 'pell_grant_received',
    'fed_student_loan_subsidy_est', 'housing_assistance_received',
    'va_benefits_received', 'other_direct_benefits',
    'total_direct_benefits',
  ],

  resolve(profile, county, fragments) {
    const { age, income, household, children, employed, disabled, veteran, student } = profile
    const fpl = FPL.forSize(household)
    const fplPct = income / fpl

    let benefits = {}

    // ── Social Security ──────────────────────────────────────
    // Only for retired (65+) or disabled
    benefits.social_security_received = 0
    if (age >= 65) {
      // Average SS benefit ~$22,000/year; scale by prior income proxy
      benefits.social_security_received = Math.round(22000 * Math.min(1, income / 40000))
      if (benefits.social_security_received < 10000) benefits.social_security_received = 10000
    }

    // ── Medicare ─────────────────────────────────────────────
    benefits.medicare_benefits_received = age >= 65 ? MEDICARE_PER_CAPITA : 0

    // ── Medicaid ─────────────────────────────────────────────
    // Expansion states: adults under 138% FPL
    // Children: generally up to 200%+ FPL via Medicaid/CHIP
    benefits.medicaid_benefits_received = 0
    benefits.chip_benefits_received = 0

    if (fplPct <= 1.38 && age < 65) {
      benefits.medicaid_benefits_received = disabled
        ? MEDICAID_PER_CAPITA.disabled
        : age < 18
          ? MEDICAID_PER_CAPITA.child
          : MEDICAID_PER_CAPITA.adult
    }
    // Children in household
    if (children > 0 && fplPct <= 2.5) {
      const childCost = MEDICAID_PER_CAPITA.child * children
      if (fplPct <= 1.38) {
        benefits.medicaid_benefits_received += childCost
      } else {
        benefits.chip_benefits_received = childCost
      }
    }

    // ── SNAP ─────────────────────────────────────────────────
    // Gross income test: 130% FPL
    benefits.snap_received = 0
    if (fplPct <= 1.30) {
      const maxBenefit = SNAP_MAX.forSize(household)
      // Net income test: benefit = max - 30% of net income
      const netIncome = Math.max(0, income - income * 0.20) // rough deductions
      const monthlyBenefit = Math.max(0, maxBenefit - Math.round(netIncome / 12 * 0.30))
      benefits.snap_received = monthlyBenefit * 12
    }

    // ── WIC ──────────────────────────────────────────────────
    // Women, infants, children under 5; 185% FPL
    benefits.wic_received = 0
    if (fplPct <= 1.85 && children > 0) {
      // Count children under 5 (approximate: if youngest archetype has kids, assume at least 1 under 5)
      const youngChildren = age < 30 ? children : Math.max(0, children - 1)
      if (youngChildren > 0) {
        benefits.wic_received = WIC_MONTHLY * 12 * youngChildren
      }
    }

    // ── TANF ─────────────────────────────────────────────────
    // Very low income with children
    benefits.tanf_received = 0
    if (fplPct <= 0.50 && children > 0) {
      benefits.tanf_received = TANF_MONTHLY.forSize(household) * 12
    }

    // ── Unemployment Insurance ───────────────────────────────
    benefits.unemployment_insurance_received = 0
    if (!employed && age >= 18 && age < 65 && !disabled) {
      // Average UI benefit ~$380/week for ~20 weeks
      benefits.unemployment_insurance_received = 380 * 20
    }

    // ── SSI / SSDI ───────────────────────────────────────────
    benefits.ssi_ssdi_received = 0
    if (disabled && income < SSI.annual_individual) {
      benefits.ssi_ssdi_received = SSI.annual_individual
    }

    // ── ACA Premium Subsidy ──────────────────────────────────
    // 100-400% FPL, not on Medicaid/Medicare/employer coverage
    benefits.aca_premium_subsidy_received = 0
    if (fplPct > 1.38 && fplPct <= 4.0 && age >= 18 && age < 65) {
      // Benchmark silver plan ~$7,500/year; subsidy covers difference above expected contribution
      const expectedContribution = income * (fplPct <= 1.50 ? 0.02 : fplPct <= 2.0 ? 0.04 : fplPct <= 2.5 ? 0.06 : 0.085)
      benefits.aca_premium_subsidy_received = Math.max(0, Math.round(7500 - expectedContribution))
    }

    // ── EITC (refundable portion) ────────────────────────────
    benefits.eitc_refundable_received = 0
    if (age >= 19 && employed !== false) {
      const tier = EITC[Math.min(children, 3)]
      if (income <= tier.income_limit) {
        // Simplified: phase-in → max → phase-out
        if (income <= tier.phase_out_start) {
          benefits.eitc_refundable_received = Math.min(tier.max_credit, Math.round(income * 0.34))
        } else {
          const phaseOut = Math.round((income - tier.phase_out_start) * 0.21)
          benefits.eitc_refundable_received = Math.max(0, tier.max_credit - phaseOut)
        }
      }
    }

    // ── Child Tax Credit (refundable portion) ────────────────
    benefits.child_tax_credit_refundable = 0
    if (children > 0 && income < CTC.phase_out_single) {
      benefits.child_tax_credit_refundable = Math.min(
        children * CTC.refundable_max,
        Math.round(Math.max(0, income - 2500) * 0.15)
      )
    }

    // ── Pell Grant ───────────────────────────────────────────
    benefits.pell_grant_received = 0
    if (student && fplPct <= 4.0) {
      benefits.pell_grant_received = fplPct <= 1.5 ? PELL_MAX
        : fplPct <= 2.5 ? Math.round(PELL_MAX * 0.6)
        : Math.round(PELL_MAX * 0.3)
    }

    // ── Federal Student Loan Subsidy ─────────────────────────
    benefits.fed_student_loan_subsidy_est = student ? Math.round(PELL_MAX * 0.3) : 0

    // ── Housing Assistance ───────────────────────────────────
    benefits.housing_assistance_received = 0
    if (fplPct <= 0.50 && !profile.homeowner) {
      // Section 8: government pays difference between FMR and 30% of income
      const fmr = getNum(fragments, 'hud-fmr', 'two_bedroom') || 1200
      const tenantPortion = Math.round(income * 0.30 / 12)
      const monthlySubsidy = Math.max(0, fmr - tenantPortion)
      benefits.housing_assistance_received = monthlySubsidy * 12
    }

    // ── VA Benefits ──────────────────────────────────────────
    benefits.va_benefits_received = veteran ? 15000 : 0  // healthcare + disability avg

    // ── Other direct benefits ────────────────────────────────
    benefits.other_direct_benefits = 0

    // ── Total ────────────────────────────────────────────────
    benefits.total_direct_benefits = Object.values(benefits).reduce((s, v) => s + v, 0)

    return benefits
  },
}
