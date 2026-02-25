/**
 * FRAGMENT — Economic Data Sources (Layer 6: Economic)
 *
 * BLS: QCEW, LAUS county-level, OES, CES, CPI
 * Census: County Business Patterns, Annual Business Survey
 * SBA: Small business loans
 * FDIC: Bank branch data
 * USASpending: Federal spending by county
 * Treasury: Fiscal data
 *
 * The economic layer — employment, wages, business, financial access.
 */

import { blsSeries, restJSON, sodaAPI, usaSpend, treasuryAPI } from './factories.mjs'
import { stateAbbrev, stateFips, countyFips } from '../lib.mjs'

export default [

  // ══════════════════════════════════════════════════════════════════
  // BLS — Bureau of Labor Statistics
  // ══════════════════════════════════════════════════════════════════

  // State unemployment rate (LAUS)
  blsSeries({
    id: 'bls-unemployment',
    label: 'BLS State Unemployment Rate',
    layers: [6],
    seriesId: (fips) => `LASST${stateFips(fips)}0000000000003`,
    transform: (series, fips) => {
      const s = series[0]
      if (!s?.data?.length) return null
      const latest = s.data[0]
      const currentYear = new Date().getFullYear()
      const yearAgo = s.data.find(d => d.year === String(currentYear - 1) && d.period === latest.period)
      return {
        state_fips: stateFips(fips),
        series_id: s.seriesID,
        latest_rate: parseFloat(latest.value),
        latest_period: `${latest.year}-${latest.period}`,
        year_ago_rate: yearAgo ? parseFloat(yearAgo.value) : null,
        change: yearAgo ? parseFloat((latest.value - yearAgo.value).toFixed(1)) : null,
      }
    },
  }),

  // State employment level (LAUS)
  blsSeries({
    id: 'bls-employment-level',
    label: 'BLS State Employment Level',
    layers: [6],
    seriesId: (fips) => `LASST${stateFips(fips)}0000000000005`,
    transform: (series) => {
      const s = series[0]
      if (!s?.data?.length) return null
      const latest = s.data[0]
      return {
        series_id: s.seriesID,
        employed: parseInt(latest.value) * 1000, // BLS reports in thousands
        period: `${latest.year}-${latest.period}`,
      }
    },
  }),

  // State labor force (LAUS)
  blsSeries({
    id: 'bls-labor-force',
    label: 'BLS State Labor Force',
    layers: [6],
    seriesId: (fips) => `LASST${stateFips(fips)}0000000000006`,
    transform: (series) => {
      const s = series[0]
      if (!s?.data?.length) return null
      const latest = s.data[0]
      return {
        series_id: s.seriesID,
        labor_force: parseInt(latest.value) * 1000,
        period: `${latest.year}-${latest.period}`,
      }
    },
  }),

  // CPI — Consumer Price Index (national)
  blsSeries({
    id: 'bls-cpi-all-urban',
    label: 'BLS CPI All Urban Consumers',
    layers: [3, 6],
    seriesId: () => 'CUSR0000SA0',
    transform: (series) => {
      const s = series[0]
      if (!s?.data?.length) return null
      const latest = s.data[0]
      const yearAgo = s.data.find(d => d.year === String(parseInt(latest.year) - 1) && d.period === latest.period)
      return {
        cpi_index: parseFloat(latest.value),
        period: `${latest.year}-${latest.period}`,
        year_over_year_change: yearAgo
          ? Math.round((parseFloat(latest.value) - parseFloat(yearAgo.value)) / parseFloat(yearAgo.value) * 1000) / 10
          : null,
        note: 'National CPI-U, seasonally adjusted',
      }
    },
  }),

  // Average weekly wages (QCEW proxy — state-level)
  blsSeries({
    id: 'bls-average-weekly-wages',
    label: 'BLS Average Weekly Wages',
    layers: [3, 6],
    seriesId: (fips) => `ENU${stateFips(fips)}00010 10 0 0`,
    transform: (series) => {
      const s = series[0]
      if (!s?.data?.length) return { note: 'QCEW series — may need different format' }
      return {
        series_id: s.seriesID,
        latest_value: parseFloat(s.data[0]?.value),
        period: `${s.data[0]?.year}-${s.data[0]?.period}`,
      }
    },
  }),

  // ══════════════════════════════════════════════════════════════════
  // Census County Business Patterns
  // ══════════════════════════════════════════════════════════════════

  restJSON({
    id: 'census-county-business-patterns',
    label: 'Census County Business Patterns',
    layers: [6],
    url: (fips) => {
      const state = stateFips(fips)
      const county = countyFips(fips)
      return `https://api.census.gov/data/2021/cbp?get=ESTAB,EMP,PAYANN,PAYQTR1&for=county:${county}&in=state:${state}&NAICS2017=00`
    },
    transform: (data) => {
      if (!Array.isArray(data) || data.length < 2) return null
      const headers = data[0]
      const values = data[1]
      return {
        total_establishments: parseInt(values[headers.indexOf('ESTAB')]) || null,
        total_employees: parseInt(values[headers.indexOf('EMP')]) || null,
        annual_payroll_thousands: parseInt(values[headers.indexOf('PAYANN')]) || null,
        q1_payroll_thousands: parseInt(values[headers.indexOf('PAYQTR1')]) || null,
      }
    },
  }),

  // CBP by industry sector (2-digit NAICS)
  restJSON({
    id: 'census-cbp-by-sector',
    label: 'Census Business Patterns by Industry',
    layers: [6],
    url: (fips) => {
      const state = stateFips(fips)
      const county = countyFips(fips)
      return `https://api.census.gov/data/2021/cbp?get=ESTAB,EMP,NAICS2017_LABEL&for=county:${county}&in=state:${state}&NAICS2017=11,21,22,23,31-33,42,44-45,48-49,51,52,53,54,55,56,61,62,71,72,81,99`
    },
    transform: (data) => {
      if (!Array.isArray(data) || data.length < 2) return null
      const headers = data[0]
      return data.slice(1).map(row => ({
        sector: row[headers.indexOf('NAICS2017_LABEL')],
        establishments: parseInt(row[headers.indexOf('ESTAB')]) || null,
        employees: parseInt(row[headers.indexOf('EMP')]) || null,
      }))
    },
  }),

  // ══════════════════════════════════════════════════════════════════
  // FDIC BankFind — Bank branches per county
  // ══════════════════════════════════════════════════════════════════

  restJSON({
    id: 'fdic-bank-branches',
    label: 'FDIC Bank Branch Locations',
    layers: [3, 6],
    url: (fips) => {
      const state = stateAbbrev(fips)
      const county = countyFips(fips)
      return `https://banks.data.fdic.gov/api/locations?filters=STALP:${state} AND STCNTY:${fips}&limit=500&fields=UNINUMBR,NAMEFULL,ADDRESBR,CITYBR,STALPBR,ZIPBR,BRSERTYP&sort_by=UNINUMBR&sort_order=ASC`
    },
    transform: (data) => {
      const results = data?.data || []
      const institutions = new Set(results.map(r => r.data?.UNINUMBR))
      return {
        bank_branches: results.length,
        unique_institutions: institutions.size,
        branch_types: [...new Set(results.map(r => r.data?.BRSERTYP).filter(Boolean))],
        // Banking desert indicator: <5 branches per 10,000 people
        note: results.length < 5 ? 'POTENTIAL BANKING DESERT' : null,
      }
    },
  }),

  // FDIC Bank Summary
  restJSON({
    id: 'fdic-bank-summary',
    label: 'FDIC Bank Financial Summary',
    layers: [3, 6],
    url: (fips) => {
      const state = stateAbbrev(fips)
      return `https://banks.data.fdic.gov/api/financials?filters=STALP:${state}&limit=10&fields=REPDTE,ASSET,DEP,INTINC,LNLSNET&sort_by=ASSET&sort_order=DESC`
    },
    transform: (data) => {
      const results = data?.data || []
      return {
        banks_in_state: results.length,
        total_assets: results.reduce((s, r) => s + (parseFloat(r.data?.ASSET) || 0), 0),
        total_deposits: results.reduce((s, r) => s + (parseFloat(r.data?.DEP) || 0), 0),
        note: 'State-level bank financials (top 10 by assets)',
      }
    },
  }),

  // ══════════════════════════════════════════════════════════════════
  // USASpending — Federal Spending by County
  // ══════════════════════════════════════════════════════════════════

  usaSpend({
    id: 'usaspending-county-spending',
    label: 'USASpending Federal Spending by County',
    layers: [1, 3],
    endpoint: 'search/spending_by_geography/',
    body: (fips) => ({
      scope: 'place_of_performance',
      geo_layer: 'county',
      geo_layer_filters: [fips],
      filters: {
        time_period: [{ start_date: '2023-10-01', end_date: '2024-09-30' }],
      },
    }),
    transform: (data) => {
      const results = data?.results || []
      const total = results.reduce((s, r) => s + (r.aggregated_amount || 0), 0)
      return {
        total_federal_spending: total,
        categories: results.length,
        details: results.slice(0, 10).map(r => ({
          name: r.display_name,
          amount: r.aggregated_amount,
          per_capita: r.per_capita,
        })),
      }
    },
  }),

  usaSpend({
    id: 'usaspending-county-awards',
    label: 'USASpending Federal Awards by County',
    layers: [1, 3, 6],
    endpoint: 'search/spending_by_award/',
    body: (fips) => ({
      filters: {
        place_of_performance_locations: [{ country: 'USA', county: fips }],
        time_period: [{ start_date: '2023-10-01', end_date: '2024-09-30' }],
        award_type_codes: ['02', '03', '04', '05'], // Grants
      },
      fields: ['Award ID', 'Recipient Name', 'Award Amount', 'Awarding Agency'],
      limit: 50,
      page: 1,
    }),
    transform: (data) => {
      const results = data?.results || []
      const total = results.reduce((s, r) => s + (r['Award Amount'] || 0), 0)
      return {
        grant_awards: results.length,
        total_grant_amount: total,
        top_recipients: results.slice(0, 10).map(r => ({
          recipient: r['Recipient Name'],
          amount: r['Award Amount'],
          agency: r['Awarding Agency'],
        })),
      }
    },
  }),

  // ══════════════════════════════════════════════════════════════════
  // Treasury Fiscal Data
  // ══════════════════════════════════════════════════════════════════

  treasuryAPI({
    id: 'treasury-federal-spending',
    label: 'Treasury Federal Account Spending',
    layers: [1, 3],
    endpoint: 'v1/accounting/dts/dts_table_1',
    fields: 'record_date,account_type,close_today_bal',
    transform: (records) => {
      const latest = records[0]
      return {
        record_date: latest?.record_date,
        sample: records.slice(0, 5).map(r => ({
          date: r.record_date,
          account_type: r.account_type,
          balance: parseFloat(r.close_today_bal) || null,
        })),
        note: 'Daily Treasury Statement — federal cash position',
      }
    },
  }),

  treasuryAPI({
    id: 'treasury-debt',
    label: 'Treasury National Debt',
    layers: [3],
    endpoint: 'v2/accounting/od/debt_to_penny',
    fields: 'record_date,tot_pub_debt_out_amt,intragov_hold_amt',
    transform: (records) => {
      if (records.length === 0) return null
      const latest = records[0]
      return {
        record_date: latest.record_date,
        total_public_debt: parseFloat(latest.tot_pub_debt_out_amt) || null,
        intragovernmental: parseFloat(latest.intragov_hold_amt) || null,
        note: 'National context — total federal debt outstanding',
      }
    },
  }),

  // ══════════════════════════════════════════════════════════════════
  // SBA Loans (via Socrata)
  // ══════════════════════════════════════════════════════════════════

  sodaAPI({
    id: 'sba-loan-data',
    label: 'SBA Small Business Loan Data',
    layers: [6],
    host: 'data.sba.gov',
    dataset: 'uveh-gczb',
    where: (fips) => {
      const st = stateAbbrev(fips)
      return `borrowerstate='${st}'`
    },
    select: 'borrowerstate,borrowercity,currentapprovalamount,undisbursedamount,franchiscode,businesstype',
    transform: (rows) => {
      const totalApproved = rows.reduce((s, r) => s + (parseFloat(r.currentapprovalamount) || 0), 0)
      return {
        sba_loans_sample: rows.length,
        total_approved: totalApproved,
        avg_loan: rows.length > 0 ? Math.round(totalApproved / rows.length) : null,
        business_types: [...new Set(rows.map(r => r.businesstype).filter(Boolean))],
      }
    },
  }),

  // ══════════════════════════════════════════════════════════════════
  // IRS Statistics of Income (SOI) — County-level tax data
  // ══════════════════════════════════════════════════════════════════

  restJSON({
    id: 'irs-soi-county',
    label: 'IRS Statistics of Income by County',
    layers: [3, 6],
    url: (fips) => {
      const state = stateFips(fips)
      return `https://www.irs.gov/statistics/soi-tax-stats-county-data`
    },
    transform: () => {
      return {
        note: 'IRS SOI county data — available as bulk download, no REST API',
        available: false,
        needs_bulk_download: true,
      }
    },
  }),
]
