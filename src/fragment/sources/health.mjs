/**
 * FRAGMENT — Health Data Sources (Layer 4: Health)
 *
 * CDC PLACES: County-level health outcomes & prevention data via Socrata
 * CMS: Medicare enrollment, spending, hospital data
 * HRSA: Health professional shortage areas, community health centers
 * SAMHSA: Substance abuse treatment facilities
 * Hospital price transparency, NPPES provider data
 *
 * All no-key or free-key APIs.
 */

import { sodaAPI, restJSON } from './factories.mjs'
import { safeFetch, stateAbbrev, stateFips, countyFips } from '../lib.mjs'

export default [

  // ══════════════════════════════════════════════════════════════════
  // CDC PLACES — County-level health data (Socrata)
  // Dataset: swc5-untb (county data, 2023 release)
  // 36 health measures at county level
  // ══════════════════════════════════════════════════════════════════

  sodaAPI({
    id: 'cdc-places-prevention',
    label: 'CDC PLACES Prevention Measures',
    layers: [4],
    host: 'data.cdc.gov',
    dataset: 'swc5-untb',
    where: (fips) => `locationid='${fips}' AND category='Prevention'`,
    select: 'measure,data_value,data_value_unit,low_confidence_limit,high_confidence_limit,totalpopulation',
    transform: (rows) => {
      const measures = {}
      for (const r of rows) {
        measures[r.measure?.toLowerCase().replace(/[^a-z0-9]+/g, '_')] = {
          value: parseFloat(r.data_value) || null,
          unit: r.data_value_unit,
          ci_low: parseFloat(r.low_confidence_limit) || null,
          ci_high: parseFloat(r.high_confidence_limit) || null,
        }
      }
      return { category: 'prevention', measure_count: rows.length, measures }
    },
  }),

  sodaAPI({
    id: 'cdc-places-outcomes',
    label: 'CDC PLACES Health Outcomes',
    layers: [4],
    host: 'data.cdc.gov',
    dataset: 'swc5-untb',
    where: (fips) => `locationid='${fips}' AND category='Health Outcomes'`,
    select: 'measure,data_value,data_value_unit,low_confidence_limit,high_confidence_limit',
    transform: (rows) => {
      const measures = {}
      for (const r of rows) {
        measures[r.measure?.toLowerCase().replace(/[^a-z0-9]+/g, '_')] = {
          value: parseFloat(r.data_value) || null,
          unit: r.data_value_unit,
          ci_low: parseFloat(r.low_confidence_limit) || null,
          ci_high: parseFloat(r.high_confidence_limit) || null,
        }
      }
      return { category: 'health_outcomes', measure_count: rows.length, measures }
    },
  }),

  sodaAPI({
    id: 'cdc-places-status',
    label: 'CDC PLACES Health Status',
    layers: [4],
    host: 'data.cdc.gov',
    dataset: 'swc5-untb',
    where: (fips) => `locationid='${fips}' AND category='Health Status'`,
    select: 'measure,data_value,data_value_unit',
    transform: (rows) => {
      const measures = {}
      for (const r of rows) {
        measures[r.measure?.toLowerCase().replace(/[^a-z0-9]+/g, '_')] = {
          value: parseFloat(r.data_value) || null,
          unit: r.data_value_unit,
        }
      }
      return { category: 'health_status', measure_count: rows.length, measures }
    },
  }),

  sodaAPI({
    id: 'cdc-places-disability',
    label: 'CDC PLACES Disability Measures',
    layers: [1, 4],
    host: 'data.cdc.gov',
    dataset: 'swc5-untb',
    where: (fips) => `locationid='${fips}' AND category='Disability'`,
    select: 'measure,data_value,data_value_unit',
    transform: (rows) => {
      const measures = {}
      for (const r of rows) {
        measures[r.measure?.toLowerCase().replace(/[^a-z0-9]+/g, '_')] = {
          value: parseFloat(r.data_value) || null,
          unit: r.data_value_unit,
        }
      }
      return { category: 'disability', measure_count: rows.length, measures }
    },
  }),

  sodaAPI({
    id: 'cdc-places-risk',
    label: 'CDC PLACES Risk Behaviors',
    layers: [4],
    host: 'data.cdc.gov',
    dataset: 'swc5-untb',
    where: (fips) => `locationid='${fips}' AND category='Health Risk Behaviors'`,
    select: 'measure,data_value,data_value_unit',
    transform: (rows) => {
      const measures = {}
      for (const r of rows) {
        measures[r.measure?.toLowerCase().replace(/[^a-z0-9]+/g, '_')] = {
          value: parseFloat(r.data_value) || null,
          unit: r.data_value_unit,
        }
      }
      return { category: 'risk_behaviors', measure_count: rows.length, measures }
    },
  }),

  // ══════════════════════════════════════════════════════════════════
  // CMS Medicare Data (Socrata — data.cms.gov)
  // ══════════════════════════════════════════════════════════════════

  sodaAPI({
    id: 'cms-medicare-enrollment',
    label: 'CMS Medicare Enrollment by County',
    layers: [3, 4],
    host: 'data.cms.gov',
    dataset: 'jqee-erxe', // Medicare Monthly Enrollment
    where: (fips) => {
      const st = stateAbbrev(fips)
      return `bene_state_abrvtn='${st}'`
    },
    select: 'bene_state_abrvtn,bene_county_cd,tot_benes,aged_tot,dsbld_tot,a_b_tot,hmo_tot,ma_and_oth_tot',
    transform: (rows, fips) => {
      const county = countyFips(fips)
      const match = rows.find(r => r.bene_county_cd === county) || rows[0]
      if (!match) return { note: 'No county match found', state_records: rows.length }
      return {
        total_beneficiaries: parseInt(match.tot_benes) || null,
        aged_beneficiaries: parseInt(match.aged_tot) || null,
        disabled_beneficiaries: parseInt(match.dsbld_tot) || null,
        parts_ab_total: parseInt(match.a_b_tot) || null,
        hmo_total: parseInt(match.hmo_tot) || null,
        medicare_advantage: parseInt(match.ma_and_oth_tot) || null,
      }
    },
  }),

  // ══════════════════════════════════════════════════════════════════
  // HRSA — Health Resources and Services Administration
  // ══════════════════════════════════════════════════════════════════

  // Health Professional Shortage Areas (HPSA)
  restJSON({
    id: 'hrsa-hpsa',
    label: 'HRSA Health Professional Shortage Areas',
    layers: [4],
    url: (fips) => {
      const state = stateAbbrev(fips)
      return `https://data.hrsa.gov/api/shortage-areas?$filter=stateFIPSCode eq '${stateFips(fips)}'&$top=200`
    },
    transform: (data, fips) => {
      const county = countyFips(fips)
      // HRSA data structure varies — extract what we can
      const records = Array.isArray(data) ? data : data?.value || []
      return {
        total_shortage_areas_in_state: records.length,
        note: 'Health Professional Shortage Area designations',
      }
    },
  }),

  // Community Health Centers
  sodaAPI({
    id: 'hrsa-health-centers',
    label: 'HRSA Community Health Centers',
    layers: [4, 8],
    host: 'data.hrsa.gov',
    dataset: 'bqz4-jjsb', // Health Center Service Delivery Sites
    where: (fips) => {
      const st = stateAbbrev(fips)
      return `site_state_abbreviation='${st}'`
    },
    select: 'site_name,site_address,site_city,site_state_abbreviation,site_status_description,health_center_type',
    transform: (rows, fips) => {
      return {
        health_centers_in_state: rows.length,
        types: [...new Set(rows.map(r => r.health_center_type).filter(Boolean))],
        active: rows.filter(r => r.site_status_description?.includes('Active')).length,
      }
    },
  }),

  // ══════════════════════════════════════════════════════════════════
  // SAMHSA — Substance Abuse & Mental Health
  // ══════════════════════════════════════════════════════════════════

  restJSON({
    id: 'samhsa-treatment-locator',
    label: 'SAMHSA Treatment Facility Locator',
    layers: [4],
    url: (fips) => {
      const state = stateAbbrev(fips)
      return `https://findtreatment.gov/locator/listing?sState=${state}&sType=SA&pageSize=100&page=1&dataset=none`
    },
    transform: (data) => {
      const rows = data?.rows || data || []
      if (!Array.isArray(rows)) return { error: 'Unexpected format', note: 'SAMHSA locator API' }
      return {
        treatment_facilities: rows.length,
        note: 'Substance abuse treatment facilities in state',
      }
    },
  }),

  // ══════════════════════════════════════════════════════════════════
  // Hospital Data — CMS Hospital Compare
  // ══════════════════════════════════════════════════════════════════

  sodaAPI({
    id: 'cms-hospital-general',
    label: 'CMS Hospital General Information',
    layers: [4],
    host: 'data.cms.gov',
    dataset: 'xubh-q36u', // Hospital General Information
    where: (fips) => {
      const st = stateAbbrev(fips)
      return `state='${st}'`
    },
    select: 'facility_name,city,state,county_name,hospital_type,hospital_ownership,emergency_services,hospital_overall_rating',
    transform: (rows, fips) => {
      const ratings = rows.map(r => parseInt(r.hospital_overall_rating)).filter(n => !isNaN(n))
      return {
        hospitals_in_state: rows.length,
        hospital_types: [...new Set(rows.map(r => r.hospital_type).filter(Boolean))],
        with_emergency: rows.filter(r => r.emergency_services === 'Yes').length,
        avg_rating: ratings.length > 0 ? Math.round(ratings.reduce((a, b) => a + b, 0) / ratings.length * 10) / 10 : null,
        ownership_types: [...new Set(rows.map(r => r.hospital_ownership).filter(Boolean))],
      }
    },
  }),

  // ══════════════════════════════════════════════════════════════════
  // CDC Social Vulnerability Index (SVI)
  // ══════════════════════════════════════════════════════════════════

  sodaAPI({
    id: 'cdc-svi',
    label: 'CDC Social Vulnerability Index',
    layers: [4, 8, 9],
    host: 'data.cdc.gov',
    dataset: 'nzfg-th89', // CDC SVI
    where: (fips) => `fips='${fips}'`,
    transform: (rows) => {
      if (rows.length === 0) return null
      const r = rows[0]
      return {
        overall_svi: parseFloat(r.rpl_themes) || null,
        socioeconomic: parseFloat(r.rpl_theme1) || null,
        household_disability: parseFloat(r.rpl_theme2) || null,
        minority_language: parseFloat(r.rpl_theme3) || null,
        housing_transportation: parseFloat(r.rpl_theme4) || null,
        population: parseInt(r.e_totpop) || null,
      }
    },
  }),

  // ══════════════════════════════════════════════════════════════════
  // CDC WONDER — Natality (birth data, public access)
  // ══════════════════════════════════════════════════════════════════

  sodaAPI({
    id: 'cdc-natality',
    label: 'CDC Natality (Birth Statistics)',
    layers: [4],
    host: 'data.cdc.gov',
    dataset: '89q2-wh5f', // NCHS Natality
    where: (fips) => {
      const st = stateAbbrev(fips)
      return `state='${st}'`
    },
    select: 'state,births,ave_age_of_mother,ave_birth_weight_gms,ave_pre_pregnancy_bmi',
    transform: (rows) => {
      if (rows.length === 0) return null
      const r = rows[0]
      return {
        total_births: parseInt(r.births) || null,
        avg_mother_age: parseFloat(r.ave_age_of_mother) || null,
        avg_birth_weight_grams: parseFloat(r.ave_birth_weight_gms) || null,
        avg_pre_pregnancy_bmi: parseFloat(r.ave_pre_pregnancy_bmi) || null,
      }
    },
  }),

  // ══════════════════════════════════════════════════════════════════
  // Drug Overdose Deaths (CDC WONDER via Socrata)
  // ══════════════════════════════════════════════════════════════════

  sodaAPI({
    id: 'cdc-drug-overdose',
    label: 'CDC Drug Overdose Death Rates',
    layers: [4],
    host: 'data.cdc.gov',
    dataset: 'jx6g-fdh6', // NCHS Drug Poisoning Mortality
    where: (fips) => {
      const st = stateAbbrev(fips)
      return `state='${st}'`
    },
    select: 'state,year,deaths,population,crude_rate,age_adjusted_rate',
    transform: (rows) => {
      if (rows.length === 0) return null
      // Get most recent year
      const sorted = rows.sort((a, b) => (b.year || '').localeCompare(a.year || ''))
      const latest = sorted[0]
      return {
        year: latest.year,
        deaths: parseInt(latest.deaths) || null,
        population: parseInt(latest.population) || null,
        crude_rate: parseFloat(latest.crude_rate) || null,
        age_adjusted_rate: parseFloat(latest.age_adjusted_rate) || null,
        trend: sorted.slice(0, 5).map(r => ({
          year: r.year,
          rate: parseFloat(r.age_adjusted_rate) || null,
        })),
      }
    },
  }),

  // ══════════════════════════════════════════════════════════════════
  // Medically Underserved Areas (HRSA)
  // ══════════════════════════════════════════════════════════════════

  sodaAPI({
    id: 'hrsa-mua',
    label: 'HRSA Medically Underserved Areas',
    layers: [4],
    host: 'data.hrsa.gov',
    dataset: 'b2b3-htr2', // MUA/P
    where: (fips) => {
      const st = stateAbbrev(fips)
      return `common_state_fips_code='${stateFips(fips)}'`
    },
    transform: (rows, fips) => {
      return {
        underserved_areas_in_state: rows.length,
        designation_types: [...new Set(rows.map(r => r.mua_p_designation_type_description).filter(Boolean))],
      }
    },
  }),
]
