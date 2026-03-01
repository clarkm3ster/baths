/**
 * ENTITY RESOLVER — Taxes & Fees
 *
 * Resolves: What does this person pay to government?
 *
 * Federal income tax, FICA, excise, state income, sales, local wage, property.
 * Uses archetype income + county/state context from fragments.
 */

import { getNum } from '../fragments.mjs'
import {
  progressiveTax,
  FED_TAX_BRACKETS_SINGLE, FED_TAX_BRACKETS_HOH, FED_TAX_BRACKETS_MFJ,
  STANDARD_DEDUCTION, FICA,
  STATE_INCOME_TAX, STATE_SALES_TAX, LOCAL_WAGE_TAX,
  CTC, consumptionRate,
} from '../reference.mjs'

export default {
  id: 'taxes',
  fields: [
    'fed_income_tax_paid', 'fica_social_security_paid', 'fica_medicare_paid',
    'fed_excise_tax_est', 'fed_other_fees',
    'state_income_tax_paid', 'state_sales_tax_est', 'state_excise_tax_est', 'state_fees',
    'local_income_wage_tax_paid', 'property_tax_paid', 'local_fees_fines',
    'total_taxes_fees_paid',
  ],

  resolve(profile, county, fragments) {
    const income = profile.income
    const state = county.state
    const fips = county.fips

    // ── Federal income tax ───────────────────────────────────
    const brackets = profile.filing === 'mfj' ? FED_TAX_BRACKETS_MFJ
      : profile.filing === 'hoh' ? FED_TAX_BRACKETS_HOH
      : FED_TAX_BRACKETS_SINGLE

    const deduction = profile.filing === 'mfj' ? STANDARD_DEDUCTION.mfj
      : profile.filing === 'hoh' ? STANDARD_DEDUCTION.hoh
      : STANDARD_DEDUCTION.single

    const taxableIncome = Math.max(0, income - deduction)
    let fedTax = progressiveTax(taxableIncome, brackets)

    // Non-refundable CTC reduces tax liability to 0 (refundable part is in benefits)
    const ctcNonrefundable = Math.min(
      profile.children * CTC.per_child,
      fedTax
    )
    fedTax = Math.max(0, fedTax - ctcNonrefundable)

    // ── FICA ─────────────────────────────────────────────────
    const ficaSS = Math.round(Math.min(income, FICA.ss_wage_base) * FICA.ss_rate)
    const ficaMedicare = Math.round(income * FICA.medicare_rate)

    // ── Federal excise (fuel, alcohol, tobacco — income proxy) ─
    const fedExcise = Math.round(income * 0.008)

    // ── State income tax ─────────────────────────────────────
    const stateRate = STATE_INCOME_TAX[state] || 0
    const stateIncomeTax = Math.round(income * stateRate)

    // ── State sales tax ──────────────────────────────────────
    const salesRate = STATE_SALES_TAX[state] || 0
    const afterTaxIncome = income - fedTax - ficaSS - ficaMedicare - stateIncomeTax
    const taxableConsumption = Math.max(0, afterTaxIncome) * consumptionRate(income)
    const stateSalesTax = Math.round(taxableConsumption * salesRate)

    // ── State excise & fees ──────────────────────────────────
    const stateExcise = Math.round(income * 0.004)
    const stateFees = Math.round(50 + income * 0.001)  // DMV, licenses, etc.

    // ── Local wage/income tax ────────────────────────────────
    const localRate = LOCAL_WAGE_TAX[fips] || 0
    const localWageTax = Math.round(income * localRate)

    // ── Property tax ─────────────────────────────────────────
    // If homeowner, use fragment data or estimate from income
    let propertyTax = 0
    if (profile.homeowner) {
      const medianValue = getNum(fragments, 'census-housing', 'median_home_value')
      const homeValue = medianValue > 0
        ? medianValue * (income / (getNum(fragments, 'census-income', 'median_household_income') || 60000))
        : income * 3  // rough estimate
      propertyTax = Math.round(homeValue * 0.012)  // ~1.2% national average
    }

    // ── Local fees & fines ───────────────────────────────────
    const localFees = Math.round(30 + income * 0.0005)

    // ── Total ────────────────────────────────────────────────
    const total = fedTax + ficaSS + ficaMedicare + fedExcise + 0
      + stateIncomeTax + stateSalesTax + stateExcise + stateFees
      + localWageTax + propertyTax + localFees

    return {
      fed_income_tax_paid: fedTax,
      fica_social_security_paid: ficaSS,
      fica_medicare_paid: ficaMedicare,
      fed_excise_tax_est: fedExcise,
      fed_other_fees: 0,
      state_income_tax_paid: stateIncomeTax,
      state_sales_tax_est: stateSalesTax,
      state_excise_tax_est: stateExcise,
      state_fees: stateFees,
      local_income_wage_tax_paid: localWageTax,
      property_tax_paid: propertyTax,
      local_fees_fines: localFees,
      total_taxes_fees_paid: total,
    }
  },
}
