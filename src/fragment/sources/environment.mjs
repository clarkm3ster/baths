/**
 * FRAGMENT — Environment Data Sources (Layer 9: Environment)
 *
 * EPA: Air quality, ECHO enforcement, EJSCREEN, Superfund, TRI
 * USGS: Water quality
 * NWS: Weather/climate
 * NOAA: Climate normals
 * FEMA: Flood zones, National Risk Index
 *
 * The environmental layer of the dome — what's in the air, water, soil.
 */

import { restJSON, sodaAPI, femaAPI } from './factories.mjs'
import { safeFetch, stateAbbrev, stateFips, countyFips } from '../lib.mjs'

export default [

  // ══════════════════════════════════════════════════════════════════
  // EPA ECHO — Enforcement & Compliance (no key)
  // ══════════════════════════════════════════════════════════════════

  restJSON({
    id: 'epa-echo-facilities',
    label: 'EPA ECHO Regulated Facilities',
    layers: [9],
    url: (fips) => {
      const state = stateAbbrev(fips)
      return `https://echodata.epa.gov/echo/echo_rest_services.get_facilities?output=JSON&p_st=${state}&p_co=${countyFips(fips)}&responseset=100`
    },
    transform: (data) => {
      const results = data?.Results || data
      const facilities = results?.Facilities || []
      return {
        total_facilities: parseInt(results?.QueryRows) || facilities.length,
        sample: facilities.slice(0, 10).map(f => ({
          name: f.FacName,
          city: f.FacCity,
          lat: f.FacLat,
          lng: f.FacLong,
          compliance_status: f.CurrSvFlag,
          violations: f.CurrVioFlag,
        })),
        with_violations: facilities.filter(f => f.CurrVioFlag === 'Y').length,
      }
    },
  }),

  restJSON({
    id: 'epa-echo-violations',
    label: 'EPA ECHO Compliance Violations',
    layers: [1, 9],
    url: (fips) => {
      const state = stateAbbrev(fips)
      return `https://echodata.epa.gov/echo/echo_rest_services.get_qid?output=JSON&p_st=${state}&p_co=${countyFips(fips)}&p_sv=Y&responseset=50`
    },
    transform: (data) => {
      const results = data?.Results || data
      return {
        facilities_with_violations: parseInt(results?.QueryRows) || 0,
        query_id: results?.QueryID || null,
      }
    },
  }),

  // ══════════════════════════════════════════════════════════════════
  // EPA EJSCREEN — Environmental Justice Screening
  // ══════════════════════════════════════════════════════════════════

  restJSON({
    id: 'epa-ejscreen',
    label: 'EPA EJSCREEN Environmental Justice',
    layers: [8, 9],
    url: (fips) => {
      // EJSCREEN ArcGIS REST service — query by FIPS
      return `https://ejscreen.epa.gov/mapper/ejscreenRESTbroker.aspx?namestr=${fips}&geometry=&distance=&unit=9035&aession=&f=json`
    },
    transform: (data) => {
      if (data?.error || !data) return { note: 'EJSCREEN API — may need alternate endpoint' }
      return data
    },
  }),

  // ══════════════════════════════════════════════════════════════════
  // EPA Toxic Release Inventory (TRI)
  // ══════════════════════════════════════════════════════════════════

  restJSON({
    id: 'epa-tri',
    label: 'EPA Toxic Release Inventory',
    layers: [4, 9],
    url: (fips) => {
      const state = stateAbbrev(fips)
      const county = countyFips(fips)
      return `https://enviro.epa.gov/enviro/efservice/TRI_FACILITY/STATE_ABBR/${state}/COUNTY_FIPS/${fips}/JSON/rows/0:50`
    },
    transform: (data) => {
      if (!Array.isArray(data)) return { note: 'TRI Envirofacts API', available: false }
      return {
        tri_facilities: data.length,
        sample: data.slice(0, 10).map(f => ({
          name: f.FACILITY_NAME,
          city: f.CITY_NAME,
          industry: f.INDUSTRY_SECTOR,
        })),
      }
    },
  }),

  // ══════════════════════════════════════════════════════════════════
  // EPA Superfund Sites (CERCLIS)
  // ══════════════════════════════════════════════════════════════════

  restJSON({
    id: 'epa-superfund',
    label: 'EPA Superfund Sites',
    layers: [5, 9],
    url: (fips) => {
      const state = stateAbbrev(fips)
      return `https://enviro.epa.gov/enviro/efservice/SEMS_ACTIVE_SITES/STATE_CODE/${state}/JSON/rows/0:100`
    },
    transform: (data) => {
      if (!Array.isArray(data)) return { note: 'Superfund Envirofacts API' }
      const county = countyFips(fips)
      return {
        superfund_sites_in_state: data.length,
        npl_sites: data.filter(s => s.NPL_STATUS?.includes('Final')).length,
        sample: data.slice(0, 10).map(s => ({
          name: s.SITE_NAME,
          city: s.CITY_NAME,
          npl_status: s.NPL_STATUS,
        })),
      }
    },
  }),

  // ══════════════════════════════════════════════════════════════════
  // EPA Air Quality (AirNow — current conditions)
  // ══════════════════════════════════════════════════════════════════

  restJSON({
    id: 'epa-airnow',
    label: 'EPA AirNow Current Air Quality',
    layers: [4, 9],
    url: (fips) => {
      const state = stateAbbrev(fips)
      return `https://www.airnowapi.org/aq/observation/zipCode/current/?format=application/json&zipCode=00000&distance=50&API_KEY=DEMO_KEY`
    },
    transform: (data) => {
      // AirNow needs zip code, not FIPS — log as gap
      return {
        note: 'AirNow API requires zip code mapping from FIPS',
        needs_geocoding: true,
        available: false,
      }
    },
  }),

  // ══════════════════════════════════════════════════════════════════
  // EPA Safe Drinking Water (SDWIS)
  // ══════════════════════════════════════════════════════════════════

  restJSON({
    id: 'epa-drinking-water',
    label: 'EPA Safe Drinking Water Violations',
    layers: [4, 9],
    url: (fips) => {
      const state = stateAbbrev(fips)
      return `https://enviro.epa.gov/enviro/efservice/SDWIS_WATER_SYSTEM/PRIMACY_AGENCY_CODE/${state}/JSON/rows/0:100`
    },
    transform: (data) => {
      if (!Array.isArray(data)) return { note: 'SDWIS Envirofacts API' }
      return {
        water_systems_in_state: data.length,
        community_systems: data.filter(s => s.PWS_TYPE_CODE === 'CWS').length,
        sample: data.slice(0, 10).map(s => ({
          name: s.PWS_NAME,
          type: s.PWS_TYPE_CODE,
          population_served: s.POPULATION_SERVED_COUNT,
        })),
      }
    },
  }),

  // ══════════════════════════════════════════════════════════════════
  // USGS Water Quality
  // ══════════════════════════════════════════════════════════════════

  restJSON({
    id: 'usgs-water-quality',
    label: 'USGS Water Quality Monitoring Sites',
    layers: [9],
    url: (fips) => {
      const state = stateAbbrev(fips).toLowerCase()
      const county = countyFips(fips)
      return `https://waterservices.usgs.gov/nwis/site/?format=rdb&stateCd=${stateAbbrev(fips)}&countyCd=${county}&siteType=ST&siteStatus=active&hasDataTypeCd=qw`
    },
    transform: (data) => {
      // USGS returns tab-delimited RDB format, not JSON
      return {
        note: 'USGS Water Services — RDB format, needs parser',
        format: 'rdb',
        available: true,
      }
    },
  }),

  // ══════════════════════════════════════════════════════════════════
  // NWS — National Weather Service (no key, just User-Agent)
  // ══════════════════════════════════════════════════════════════════

  restJSON({
    id: 'nws-alerts',
    label: 'NWS Active Weather Alerts',
    layers: [9],
    url: (fips) => {
      const state = stateAbbrev(fips)
      return `https://api.weather.gov/alerts/active?area=${state}`
    },
    headers: { 'User-Agent': 'BATHS Fragment Agent (fragment@baths.dev)' },
    transform: (data) => {
      const features = data?.features || []
      return {
        active_alerts: features.length,
        alerts: features.slice(0, 10).map(f => ({
          event: f.properties?.event,
          severity: f.properties?.severity,
          headline: f.properties?.headline,
          effective: f.properties?.effective,
          expires: f.properties?.expires,
        })),
      }
    },
  }),

  // ══════════════════════════════════════════════════════════════════
  // FEMA National Risk Index
  // ══════════════════════════════════════════════════════════════════

  femaAPI({
    id: 'fema-national-risk-index',
    label: 'FEMA National Risk Index',
    layers: [5, 9],
    endpoint: 'NationalRiskIndexCountyData',
    filter: (fips) => `countyFips eq '${fips}'`,
    top: 5,
    transform: (records) => {
      if (records.length === 0) return null
      const r = records[0]
      return {
        risk_score: r.riskScore || null,
        risk_rating: r.riskRating || null,
        expected_annual_loss: r.expectedAnnualLoss || null,
        social_vulnerability: r.socialVulnerability || null,
        community_resilience: r.communityResilience || null,
        hazard_type_risk_count: r.hazardTypeRiskCount || null,
      }
    },
  }),

  // ══════════════════════════════════════════════════════════════════
  // FEMA Flood Map Data
  // ══════════════════════════════════════════════════════════════════

  femaAPI({
    id: 'fema-flood-zones',
    label: 'FEMA Flood Insurance Data',
    layers: [5, 9],
    endpoint: 'FimaNfipPolicies',
    filter: (fips) => {
      const st = stateAbbrev(fips)
      return `propertyState eq '${st}'`
    },
    top: 100,
    transform: (records) => {
      const totalPremium = records.reduce((s, r) => s + (parseFloat(r.totalInsurancePremiumOfThePolicy) || 0), 0)
      return {
        flood_policies_sample: records.length,
        avg_premium: records.length > 0 ? Math.round(totalPremium / records.length) : null,
        flood_zones: [...new Set(records.map(r => r.floodZone).filter(Boolean))],
      }
    },
  }),

  // ══════════════════════════════════════════════════════════════════
  // NOAA Climate Normals (via NCEI)
  // ══════════════════════════════════════════════════════════════════

  restJSON({
    id: 'noaa-climate-normals',
    label: 'NOAA 30-Year Climate Normals',
    layers: [9],
    url: (fips) => {
      const state = stateAbbrev(fips)
      return `https://www.ncei.noaa.gov/access/services/data/v1?dataset=normals-annualseasonal-2006-2020&stations=&dataTypes=ANN-TAVG-NORMAL,ANN-PRCP-NORMAL,ANN-HTDD-NORMAL,ANN-CLDD-NORMAL&startDate=2020-01-01&endDate=2020-12-31&boundingBox=90,-180,-90,180&units=standard&format=json&limit=10`
    },
    transform: (data) => {
      if (!Array.isArray(data) || data.length === 0) return { note: 'NOAA NCEI — query by station needed' }
      return {
        stations: data.length,
        sample: data.slice(0, 5),
      }
    },
  }),

  // ══════════════════════════════════════════════════════════════════
  // USDA Food Access Research Atlas
  // ══════════════════════════════════════════════════════════════════

  restJSON({
    id: 'usda-food-access',
    label: 'USDA Food Access Research Atlas',
    layers: [4, 9],
    url: (fips) => {
      return `https://gis.ers.usda.gov/arcgis/rest/services/foodDesert/MapServer/0/query?where=CensusTract+LIKE+'${fips}%25'&outFields=*&f=json`
    },
    transform: (data) => {
      const features = data?.features || []
      if (features.length === 0) return { note: 'No tracts found for FIPS prefix' }
      const tracts = features.map(f => f.attributes)
      const lowAccess = tracts.filter(t => t.LILATracts_1And10 === 1 || t.LILATracts_halfAnd10 === 1).length
      return {
        total_tracts: tracts.length,
        low_access_tracts: lowAccess,
        low_access_pct: tracts.length > 0 ? Math.round((lowAccess / tracts.length) * 100) : 0,
        note: 'USDA Food Access Research Atlas — low income, low access tracts',
      }
    },
  }),
]
