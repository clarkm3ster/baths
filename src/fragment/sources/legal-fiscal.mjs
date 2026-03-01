/**
 * FRAGMENT — Legal & Fiscal Data Sources (Layer 1: Legal, Layer 2: Systems, Layer 3: Fiscal)
 *
 * Federal Register: Proposed and final rules (free, no key)
 * eCFR: Code of Federal Regulations (free, no key)
 * USASpending: Federal obligations (free, no key)
 *
 * The legal layer is the foundation. Every right, entitlement, pathway.
 */

import { restJSON, usaSpend } from './factories.mjs'
import { stateAbbrev } from '../lib.mjs'

export default [

  // ══════════════════════════════════════════════════════════════════
  // Federal Register — Rules, Proposed Rules, Notices
  // ══════════════════════════════════════════════════════════════════

  restJSON({
    id: 'federal-register-rules',
    label: 'Federal Register Final Rules',
    layers: [1],
    url: () => {
      const year = new Date().getFullYear()
      return `https://www.federalregister.gov/api/v1/documents.json?conditions[type][]=RULE&conditions[publication_date][gte]=${year}-01-01&per_page=50&order=newest&fields[]=title,abstract,agencies,citation,document_number,publication_date,effective_on`
    },
    transform: (data) => {
      const results = data?.results || []
      return {
        recent_final_rules: results.length,
        total_count: data?.count || results.length,
        rules: results.slice(0, 20).map(r => ({
          title: r.title?.slice(0, 200),
          agencies: r.agencies?.map(a => a.name),
          publication_date: r.publication_date,
          effective_on: r.effective_on,
          citation: r.citation,
        })),
      }
    },
  }),

  restJSON({
    id: 'federal-register-proposed',
    label: 'Federal Register Proposed Rules',
    layers: [1],
    url: () => {
      const year = new Date().getFullYear()
      return `https://www.federalregister.gov/api/v1/documents.json?conditions[type][]=PRORULE&conditions[publication_date][gte]=${year}-01-01&per_page=50&order=newest&fields[]=title,abstract,agencies,citation,document_number,publication_date,comment_end_date`
    },
    transform: (data) => {
      const results = data?.results || []
      return {
        recent_proposed_rules: results.length,
        total_count: data?.count || results.length,
        open_for_comment: results.filter(r => {
          if (!r.comment_end_date) return false
          return new Date(r.comment_end_date) > new Date()
        }).length,
        rules: results.slice(0, 20).map(r => ({
          title: r.title?.slice(0, 200),
          agencies: r.agencies?.map(a => a.name),
          publication_date: r.publication_date,
          comment_end: r.comment_end_date,
        })),
      }
    },
  }),

  // Federal Register — Agency-specific (HHS, HUD, DOL, ED, USDA)
  ..._agencyRules('hhs', 'Health and Human Services', [1, 4]),
  ..._agencyRules('hud', 'Housing and Urban Development', [1, 5]),
  ..._agencyRules('dol', 'Labor', [1, 6]),
  ..._agencyRules('ed', 'Education', [1, 7]),
  ..._agencyRules('usda', 'Agriculture', [1, 9]),

  // ══════════════════════════════════════════════════════════════════
  // eCFR — Electronic Code of Federal Regulations
  // ══════════════════════════════════════════════════════════════════

  restJSON({
    id: 'ecfr-titles',
    label: 'eCFR Regulation Titles',
    layers: [1],
    url: () => 'https://www.ecfr.gov/api/versioner/v1/titles',
    transform: (data) => {
      const titles = data?.titles || []
      return {
        total_cfr_titles: titles.length,
        titles: titles.map(t => ({
          number: t.number,
          name: t.name,
          latest_issue_date: t.latest_issue_date,
        })),
      }
    },
  }),

  restJSON({
    id: 'ecfr-title-42',
    label: 'eCFR Title 42 (Public Health & Welfare)',
    layers: [1, 4],
    url: () => 'https://www.ecfr.gov/api/versioner/v1/structure/2024-01-01/title-42.json',
    transform: (data) => {
      const children = data?.children || []
      return {
        title: 'Public Health and Welfare',
        chapters: children.length,
        structure: children.slice(0, 20).map(c => ({
          identifier: c.identifier,
          label: c.label,
          type: c.type,
        })),
      }
    },
  }),

  restJSON({
    id: 'ecfr-title-24',
    label: 'eCFR Title 24 (Housing & Urban Development)',
    layers: [1, 5],
    url: () => 'https://www.ecfr.gov/api/versioner/v1/structure/2024-01-01/title-24.json',
    transform: (data) => {
      const children = data?.children || []
      return {
        title: 'Housing and Urban Development',
        chapters: children.length,
        structure: children.slice(0, 20).map(c => ({
          identifier: c.identifier,
          label: c.label,
          type: c.type,
        })),
      }
    },
  }),

  // ══════════════════════════════════════════════════════════════════
  // Federal Spending on Social Programs by State
  // ══════════════════════════════════════════════════════════════════

  usaSpend({
    id: 'usaspending-social-programs',
    label: 'USASpending Social Program Spending',
    layers: [1, 3],
    endpoint: 'search/spending_by_category/agency/',
    body: (fips) => ({
      filters: {
        place_of_performance_locations: [{ country: 'USA', state: stateAbbrev(fips) }],
        time_period: [{ start_date: '2023-10-01', end_date: '2024-09-30' }],
        agencies: [
          { type: 'funding', tier: 'toptier', name: 'Department of Health and Human Services' },
          { type: 'funding', tier: 'toptier', name: 'Department of Housing and Urban Development' },
          { type: 'funding', tier: 'toptier', name: 'Social Security Administration' },
          { type: 'funding', tier: 'toptier', name: 'Department of Education' },
          { type: 'funding', tier: 'toptier', name: 'Department of Agriculture' },
        ],
      },
      limit: 20,
      page: 1,
    }),
    transform: (data) => {
      const results = data?.results || data?.category || []
      if (!Array.isArray(results)) return { note: 'USASpending category format', data }
      return {
        agencies: results.length,
        total: results.reduce((s, r) => s + (r.aggregated_amount || 0), 0),
        by_agency: results.slice(0, 10).map(r => ({
          name: r.name,
          amount: r.aggregated_amount,
        })),
      }
    },
  }),
]

// ── Agency-specific Federal Register sources ────────────────────

function _agencyRules(slug, agencyName, layers) {
  return [
    restJSON({
      id: `federal-register-${slug}`,
      label: `Federal Register: ${agencyName}`,
      layers,
      url: () => {
        const year = new Date().getFullYear()
        return `https://www.federalregister.gov/api/v1/documents.json?conditions[agencies][]=${slug}&conditions[type][]=RULE&conditions[publication_date][gte]=${year - 1}-01-01&per_page=25&order=newest&fields[]=title,citation,publication_date,effective_on,abstract`
      },
      transform: (data) => {
        const results = data?.results || []
        return {
          agency: agencyName,
          recent_rules: results.length,
          rules: results.slice(0, 10).map(r => ({
            title: r.title?.slice(0, 200),
            citation: r.citation,
            publication_date: r.publication_date,
            effective_on: r.effective_on,
          })),
        }
      },
    }),
  ]
}
