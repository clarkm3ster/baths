/**
 * BATHS STUDIO SUITE — Representation Console
 * console.js — System architecture, data engine, agents, government systems, and operations dashboard
 *
 * Exports: window.renderConsole = function(container) { ... }
 * References: window.BATHS_DATA
 */

window.renderConsole = function (container) {
  'use strict';

  // ─── Inject Styles ──────────────────────────────────────────────
  const styleId = 'console-styles';
  if (!document.getElementById(styleId)) {
    const style = document.createElement('style');
    style.id = styleId;
    style.textContent = `
      /* ═══ Console — Dark Terminal Aesthetic ═══ */
      .console-root {
        font-family: system-ui, -apple-system, sans-serif;
        color: #f5f0e8;
        background: #0a0a0f;
        min-height: 100vh;
        padding: 0 0 4rem 0;
      }
      .console-root * { box-sizing: border-box; }

      /* ─ Monospace ─ */
      .mono { font-family: 'SF Mono', 'Cascadia Code', 'Fira Code', Consolas, monospace; }

      /* ─ Header ─ */
      .con-header {
        padding: 2.5rem 2rem 1.5rem;
        border-bottom: 1px solid rgba(201,168,76,0.15);
        margin-bottom: 0;
      }
      .con-header h1 {
        font-size: 1.5rem;
        font-weight: 700;
        color: #c9a84c;
        letter-spacing: 0.12em;
        margin: 0 0 0.3rem 0;
        text-transform: uppercase;
      }
      .con-header p {
        font-size: 0.82rem;
        color: rgba(245,240,232,0.45);
        margin: 0;
      }

      /* ─ Tab Bar ─ */
      .con-tabs {
        display: flex;
        gap: 0;
        overflow-x: auto;
        border-bottom: 1px solid rgba(201,168,76,0.12);
        padding: 0 1.5rem;
        background: rgba(201,168,76,0.02);
        -webkit-overflow-scrolling: touch;
        scrollbar-width: none;
      }
      .con-tabs::-webkit-scrollbar { display: none; }
      .con-tab {
        padding: 0.65rem 1rem;
        font-size: 0.72rem;
        font-weight: 600;
        color: rgba(245,240,232,0.4);
        cursor: pointer;
        border-bottom: 2px solid transparent;
        white-space: nowrap;
        transition: color 0.2s, border-color 0.2s;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        font-family: 'SF Mono', Consolas, monospace;
      }
      .con-tab:hover { color: rgba(245,240,232,0.7); }
      .con-tab.active {
        color: #c9a84c;
        border-bottom-color: #c9a84c;
      }

      /* ─ Tab Content ─ */
      .con-content { padding: 1.5rem 2rem; }
      .con-section { display: none; }
      .con-section.active { display: block; }

      /* ─ Section Title ─ */
      .con-stitle {
        font-size: 1.1rem;
        font-weight: 700;
        color: #c9a84c;
        margin: 0 0 0.5rem 0;
      }
      .con-sdesc {
        font-size: 0.78rem;
        color: rgba(245,240,232,0.4);
        margin: 0 0 1.5rem 0;
        line-height: 1.5;
      }

      /* ─ Cards ─ */
      .con-card {
        background: rgba(201,168,76,0.04);
        border: 1px solid rgba(201,168,76,0.12);
        border-radius: 8px;
        padding: 1rem 1.15rem;
        margin-bottom: 0.75rem;
        transition: border-color 0.2s;
      }
      .con-card:hover { border-color: rgba(201,168,76,0.25); }
      .con-card-title {
        font-size: 0.82rem;
        font-weight: 700;
        color: #f5f0e8;
        margin: 0 0 0.3rem 0;
      }
      .con-card-sub {
        font-size: 0.7rem;
        color: rgba(245,240,232,0.45);
        margin: 0 0 0.5rem 0;
        font-family: 'SF Mono', Consolas, monospace;
      }
      .con-card-body {
        font-size: 0.75rem;
        color: rgba(245,240,232,0.6);
        line-height: 1.6;
      }

      /* ─ Grid Layouts ─ */
      .con-grid-2 { display: grid; grid-template-columns: repeat(auto-fill, minmax(340px, 1fr)); gap: 0.75rem; }
      .con-grid-3 { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 0.75rem; }
      .con-grid-4 { display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 0.75rem; }
      .con-grid-6 { display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 0.6rem; }

      /* ─ Status Dots ─ */
      .dot {
        display: inline-block;
        width: 8px; height: 8px;
        border-radius: 50%;
        margin-right: 6px;
        vertical-align: middle;
      }
      .dot-green { background: #34d399; box-shadow: 0 0 6px rgba(52,211,153,0.4); }
      .dot-yellow { background: #fbbf24; box-shadow: 0 0 6px rgba(251,191,36,0.4); }
      .dot-red { background: #f87171; box-shadow: 0 0 6px rgba(248,113,113,0.4); }
      .dot-blue { background: #60a5fa; box-shadow: 0 0 6px rgba(96,165,250,0.4); }
      .dot-gold { background: #c9a84c; box-shadow: 0 0 6px rgba(201,168,76,0.4); }

      /* ─ Badges ─ */
      .con-badge {
        display: inline-block;
        padding: 0.15rem 0.5rem;
        border-radius: 3px;
        font-size: 0.65rem;
        font-weight: 600;
        font-family: 'SF Mono', Consolas, monospace;
        letter-spacing: 0.03em;
      }
      .badge-gold { background: rgba(201,168,76,0.15); color: #c9a84c; }
      .badge-green { background: rgba(52,211,153,0.12); color: #34d399; }
      .badge-red { background: rgba(248,113,113,0.12); color: #f87171; }
      .badge-blue { background: rgba(96,165,250,0.12); color: #60a5fa; }
      .badge-yellow { background: rgba(251,191,36,0.12); color: #fbbf24; }
      .badge-purple { background: rgba(167,139,250,0.12); color: #a78bfa; }

      /* ─ Table ─ */
      .con-table {
        width: 100%;
        border-collapse: collapse;
        font-size: 0.75rem;
        margin-bottom: 1rem;
      }
      .con-table th {
        text-align: left;
        padding: 0.5rem 0.75rem;
        font-size: 0.65rem;
        font-weight: 600;
        color: rgba(245,240,232,0.4);
        text-transform: uppercase;
        letter-spacing: 0.06em;
        border-bottom: 1px solid rgba(201,168,76,0.12);
        font-family: 'SF Mono', Consolas, monospace;
      }
      .con-table td {
        padding: 0.5rem 0.75rem;
        color: rgba(245,240,232,0.7);
        border-bottom: 1px solid rgba(201,168,76,0.06);
        vertical-align: top;
      }
      .con-table tr:hover td { background: rgba(201,168,76,0.03); }

      /* ─ Stat Blocks ─ */
      .con-stat-row {
        display: flex;
        flex-wrap: wrap;
        gap: 0.75rem;
        margin-bottom: 1.5rem;
      }
      .con-stat {
        flex: 1;
        min-width: 130px;
        background: rgba(201,168,76,0.04);
        border: 1px solid rgba(201,168,76,0.1);
        border-radius: 6px;
        padding: 0.75rem 1rem;
        text-align: center;
      }
      .con-stat-val {
        font-size: 1.5rem;
        font-weight: 700;
        color: #c9a84c;
        font-family: 'SF Mono', Consolas, monospace;
      }
      .con-stat-label {
        font-size: 0.65rem;
        color: rgba(245,240,232,0.4);
        text-transform: uppercase;
        letter-spacing: 0.06em;
        margin-top: 0.2rem;
      }

      /* ─ Connection Lines / Mesh ─ */
      .mesh-container {
        position: relative;
        background: rgba(201,168,76,0.02);
        border: 1px solid rgba(201,168,76,0.1);
        border-radius: 10px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        overflow: hidden;
      }
      .mesh-node {
        background: rgba(10,10,15,0.9);
        border: 1px solid rgba(201,168,76,0.2);
        border-radius: 6px;
        padding: 0.6rem 0.8rem;
        min-width: 145px;
      }
      .mesh-node-name {
        font-size: 0.72rem;
        font-weight: 700;
        color: #f5f0e8;
      }
      .mesh-node-port {
        font-size: 0.62rem;
        font-family: 'SF Mono', Consolas, monospace;
        color: #c9a84c;
        margin-top: 2px;
      }

      /* ─ Architecture ASCII ─ */
      .arch-ascii {
        background: rgba(0,0,0,0.3);
        border: 1px solid rgba(201,168,76,0.1);
        border-radius: 6px;
        padding: 1.25rem 1.5rem;
        font-family: 'SF Mono', Consolas, monospace;
        font-size: 0.72rem;
        line-height: 1.6;
        color: rgba(245,240,232,0.6);
        white-space: pre;
        overflow-x: auto;
        margin-bottom: 1.5rem;
      }
      .arch-ascii .hl { color: #c9a84c; }
      .arch-ascii .gr { color: #34d399; }
      .arch-ascii .bl { color: #60a5fa; }
      .arch-ascii .yl { color: #fbbf24; }

      /* ─ Port Warning ─ */
      .port-warn {
        background: rgba(248,113,113,0.06);
        border: 1px solid rgba(248,113,113,0.2);
        border-radius: 6px;
        padding: 0.75rem 1rem;
        margin-bottom: 1rem;
        font-size: 0.75rem;
        color: #f87171;
      }
      .port-warn strong { color: #fca5a5; }

      /* ─ Chart Canvas ─ */
      .con-chart-wrap {
        background: rgba(201,168,76,0.03);
        border: 1px solid rgba(201,168,76,0.1);
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 1.25rem;
      }
      .con-chart-wrap canvas { max-height: 260px; }

      /* ─ Flow / Pipeline ─ */
      .con-flow {
        display: flex;
        align-items: center;
        flex-wrap: wrap;
        gap: 0.4rem;
        margin-bottom: 1rem;
      }
      .con-flow-step {
        padding: 0.4rem 0.75rem;
        border-radius: 4px;
        font-size: 0.7rem;
        font-weight: 600;
        font-family: 'SF Mono', Consolas, monospace;
      }
      .con-flow-arrow {
        color: rgba(201,168,76,0.4);
        font-size: 0.8rem;
      }

      /* ─ Divider ─ */
      .con-divider {
        border: none;
        border-top: 1px solid rgba(201,168,76,0.08);
        margin: 1.75rem 0;
      }

      /* ─ Sub Header ─ */
      .con-sh {
        font-size: 0.85rem;
        font-weight: 700;
        color: rgba(245,240,232,0.8);
        margin: 1.25rem 0 0.6rem;
      }

      /* ─ Mini label ─ */
      .con-label {
        font-size: 0.62rem;
        font-weight: 600;
        color: rgba(245,240,232,0.35);
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 0.35rem;
      }

      /* ─ Endpoint pill ─ */
      .ep-pill {
        display: inline-block;
        padding: 0.12rem 0.45rem;
        border-radius: 3px;
        font-size: 0.6rem;
        font-family: 'SF Mono', Consolas, monospace;
        background: rgba(201,168,76,0.08);
        color: rgba(245,240,232,0.5);
        margin: 0.12rem 0.15rem 0.12rem 0;
      }

      /* ─ Timeline bar ─ */
      .tl-bar {
        height: 18px;
        border-radius: 3px;
        position: relative;
        overflow: hidden;
      }
      .tl-bar-fill {
        height: 100%;
        border-radius: 3px;
        background: linear-gradient(90deg, #c9a84c, rgba(201,168,76,0.5));
      }
      .tl-label {
        position: absolute;
        top: 50%;
        left: 6px;
        transform: translateY(-50%);
        font-size: 0.6rem;
        font-weight: 600;
        color: #0a0a0f;
        font-family: 'SF Mono', Consolas, monospace;
      }

      /* Responsive */
      @media (max-width: 768px) {
        .con-content { padding: 1rem; }
        .con-grid-2, .con-grid-3, .con-grid-4 { grid-template-columns: 1fr; }
        .con-stat-row { flex-direction: column; }
        .arch-ascii { font-size: 0.6rem; }
      }
    `;
    document.head.appendChild(style);
  }

  // ─── Data Reference ─────────────────────────────────────────────
  const D = window.BATHS_DATA || {};

  // ─── Constants ──────────────────────────────────────────────────

  // All 18 services (12 DUOMO + 6 THAUMA) from baths-dashboard registry
  const SERVICES = [
    // DUOMO (12)
    { name: 'duomo-legal-research', legacy: 'domes-legal-research', port: 8000, group: 'DUOMO', endpoints: ['/api/match', '/api/provisions', '/api/domains', '/api/explain'], desc: 'Legal provision matching & search' },
    { name: 'duomo-data-research', legacy: 'domes-data-research', port: 8001, group: 'DUOMO', endpoints: ['/api/systems', '/api/connections', '/api/gaps', '/api/consent-pathways'], desc: 'Data system constellation mapping' },
    { name: 'duomo-profile-research', legacy: 'domes-profile-research', port: 8002, group: 'DUOMO', endpoints: ['/api/cases', '/api/profiles', '/api/cost', '/api/systems'], desc: 'Person profiles & composite builder' },
    { name: 'duomo-legal', legacy: 'domes-legal', port: 8003, group: 'DUOMO', endpoints: ['/api/provisions', '/api/search', '/api/match', '/api/graph'], desc: 'Structured legal engine & studio' },
    { name: 'duomo-datamap', legacy: 'domes-datamap', port: 8013, group: 'DUOMO', endpoints: ['/api/systems', '/api/gaps', '/api/bridges', '/api/person-map', '/api/stats'], desc: 'System gap/bridge mapping engine' },
    { name: 'duomo-profiles', legacy: 'domes-profiles', port: 8004, group: 'DUOMO', endpoints: ['/api/profiles', '/api/cost'], desc: 'Profile & cost engine' },
    { name: 'duomo-contracts', legacy: 'domes-contracts', port: 8014, group: 'DUOMO', endpoints: ['/api/agreements', '/api/compliance', '/api/consent'], desc: 'Legal agreement generation' },
    { name: 'duomo-architect', legacy: 'domes-architect', port: 8015, group: 'DUOMO', endpoints: ['/api/architectures', '/api/models'], desc: 'Coordination model design' },
    { name: 'duomo-viz', legacy: 'domes-viz', port: 8005, group: 'DUOMO', endpoints: ['/api/narrative/sections', '/api/marble/worlds'], desc: 'Visualization & narrative engine' },
    { name: 'duomo-brain', legacy: 'domes-brain', port: 8006, group: 'DUOMO', endpoints: ['/api/query', '/api/services', '/api/discoveries', '/api/stats'], desc: 'Central orchestrator & discovery' },
    { name: 'duomo-lab', legacy: 'domes-lab', port: 8007, group: 'DUOMO', endpoints: ['/api/teammates', '/api/innovations', '/api/generate', '/api/stats'], desc: 'Innovation generation lab' },
    { name: 'duomo-flourishing', legacy: 'domes-flourishing', port: 8016, group: 'DUOMO', endpoints: ['/api/domains', '/api/philosophy', '/api/finance', '/api/flourishing-index'], desc: 'Flourishing framework engine' },
    // THAUMA (6)
    { name: 'thauma-assets', legacy: 'spheres-assets', port: 8017, group: 'THAUMA', endpoints: ['/api/parcels', '/api/stats', '/api/value'], desc: 'Property & asset data' },
    { name: 'thauma-legal', legacy: 'spheres-legal', port: 8018, group: 'THAUMA', endpoints: ['/api/permits', '/api/contracts', '/api/policy'], desc: 'Permits, contracts & policy' },
    { name: 'thauma-studio', legacy: 'spheres-studio', port: 8019, group: 'THAUMA', endpoints: ['/api/designs', '/api/cost', '/api/timeline', '/api/gallery'], desc: 'Design & production studio' },
    { name: 'thauma-viz', legacy: 'spheres-viz', port: 8008, group: 'THAUMA', endpoints: ['/api/episodes'], desc: 'Episode visualization' },
    { name: 'thauma-brain', legacy: 'spheres-brain', port: 8009, group: 'THAUMA', endpoints: ['/api/query', '/api/services', '/api/metrics', '/api/discoveries'], desc: 'THAUMA orchestrator' },
    { name: 'thauma-lab', legacy: 'spheres-lab', port: 8010, group: 'THAUMA', endpoints: ['/api/teammates', '/api/innovations', '/api/generate', '/api/stats'], desc: 'THAUMA innovation lab' }
  ];

  // Port conflicts from audit
  const PORT_CONFLICTS = [
    { port: 8003, services: ['duomo-legal', 'duomo-datamap', 'duomo-contracts'], note: 'Resolved via dashboard ports 8003/8013/8014' },
    { port: 8004, services: ['duomo-profiles', 'duomo-architect'], note: 'Resolved via dashboard ports 8004/8015' },
    { port: 8005, services: ['duomo-viz', 'duomo-flourishing'], note: 'Resolved via dashboard ports 8005/8016' },
    { port: 8000, services: ['duomo-legal-research', 'thauma-assets'], note: 'Resolved via dashboard ports 8000/8017' },
    { port: 8006, services: ['duomo-brain', 'thauma-legal'], note: 'Resolved via dashboard ports 8006/8018' },
    { port: 8007, services: ['duomo-lab', 'thauma-studio'], note: 'Resolved via dashboard ports 8007/8019' }
  ];

  // Data engine stats
  const ENGINE_STATS = {
    provisions: 5126,
    cost_points: 35,
    gov_systems: 19,
    system_links: 19,
    parcels: 14,
    enrichments: 4898,
    total_scrape_runs: 7,
    successful_scrapes: 7,
    db_size_mb: 3.73
  };

  // 28 Priority Counties
  const COUNTIES = {
    'Philadelphia Metro': [
      { fips: '42101', name: 'Philadelphia, PA' },
      { fips: '42045', name: 'Delaware, PA' },
      { fips: '42091', name: 'Montgomery, PA' },
      { fips: '42017', name: 'Bucks, PA' },
      { fips: '42029', name: 'Chester, PA' }
    ],
    'NYC': [
      { fips: '36061', name: 'Manhattan, NY' },
      { fips: '36047', name: 'Brooklyn, NY' },
      { fips: '36081', name: 'Queens, NY' },
      { fips: '36005', name: 'Bronx, NY' }
    ],
    'Major Metros': [
      { fips: '06037', name: 'Los Angeles, CA' },
      { fips: '17031', name: 'Cook/Chicago, IL' },
      { fips: '48201', name: 'Harris/Houston, TX' },
      { fips: '04013', name: 'Maricopa/Phoenix, AZ' },
      { fips: '48113', name: 'Dallas, TX' },
      { fips: '12086', name: 'Miami-Dade, FL' },
      { fips: '13121', name: 'Fulton/Atlanta, GA' },
      { fips: '53033', name: 'King/Seattle, WA' },
      { fips: '24510', name: 'Baltimore City, MD' },
      { fips: '11001', name: 'Washington, DC' }
    ],
    'Rural / Appalachia': [
      { fips: '21013', name: 'Bell, KY' },
      { fips: '54055', name: 'Mercer, WV' }
    ],
    'Deep South': [
      { fips: '28049', name: 'Hinds/Jackson, MS' },
      { fips: '01073', name: 'Jefferson/Birmingham, AL' }
    ],
    'Midwest': [
      { fips: '26163', name: 'Wayne/Detroit, MI' },
      { fips: '39035', name: 'Cuyahoga/Cleveland, OH' }
    ],
    'New Jersey': [
      { fips: '34013', name: 'Essex, NJ' },
      { fips: '34017', name: 'Hudson, NJ' },
      { fips: '34023', name: 'Middlesex, NJ' }
    ]
  };

  // Census ACS variable groups
  const ACS_GROUPS = [
    { id: 'census-demographics', label: 'Demographics', vars: 'total_pop, median_age, male/female, race, foreign_born' },
    { id: 'census-income', label: 'Income & Poverty', vars: 'median_hh_income, per_capita, poverty, gini, snap, ssi' },
    { id: 'census-housing', label: 'Housing', vars: 'total_units, vacant, owner/renter, median_value, median_rent' },
    { id: 'census-rent-burden', label: 'Rent Burden', vars: 'rent_30-35%, rent_35-40%, rent_40-50%, rent_50+%' },
    { id: 'census-health-insurance', label: 'Health Insurance', vars: 'with_insurance, uninsured, medicaid, employer' },
    { id: 'census-disability', label: 'Disability', vars: 'total_disability, by_age_group, by_gender' },
    { id: 'census-education', label: 'Education', vars: 'bachelors, masters, doctorate, enrollment' },
    { id: 'census-commute', label: 'Commute', vars: 'drove_alone, public_transit, walked, wfh, no_vehicle' },
    { id: 'census-internet', label: 'Internet Access', vars: 'broadband, no_internet, smartphone_only' },
    { id: 'census-employment', label: 'Employment', vars: 'labor_force, employed, unemployed, by_occupation' }
  ];

  // External data sources
  const EXTERNAL_SOURCES = [
    { id: 'bls-unemployment', name: 'Bureau of Labor Statistics', status: 'active', api: 'BLS LAUS public API' },
    { id: 'hud-fmr', name: 'HUD Fair Market Rents', status: 'active', api: 'HUD FMR API (token needed)' },
    { id: 'epa-air-quality', name: 'EPA Air Quality', status: 'active', api: 'EPA AQS quarterly ozone' },
    { id: 'usda-food-access', name: 'USDA Food Access', status: 'active', api: 'Food Access Research Atlas' },
    { id: 'fema-disasters', name: 'FEMA Disasters', status: 'active', api: 'OpenFEMA (no key)' },
    { id: 'cdc-mortality', name: 'CDC Mortality', status: 'gap', api: 'No public REST API' },
    { id: 'fbi-crime', name: 'FBI Crime Data', status: 'gap', api: 'Requires API key' }
  ];

  // 6 Archetype Profiles
  const ARCHETYPES = [
    { id: 'marcus', name: 'Marcus', age: 34, income: 28000, hh: 3, children: 2, desc: 'Single dad, systems-heavy' },
    { id: 'elena', name: 'Elena', age: 29, income: 22000, hh: 2, children: 1, desc: 'Working poor' },
    { id: 'james', name: 'James', age: 72, income: 14000, hh: 1, children: 0, desc: 'Elderly disabled' },
    { id: 'rivera', name: 'Rivera Family', age: 38, income: 52000, hh: 5, children: 3, desc: 'Benefits cliff' },
    { id: 'aisha', name: 'Aisha', age: 19, income: 12000, hh: 1, children: 0, desc: 'Aged out of foster care' },
    { id: 'median', name: 'Median', age: 38, income: 59540, hh: 2, children: 1, desc: 'National benchmark' }
  ];

  // Government Systems Registry — 31 systems from domes-datamap seed
  const GOV_SYSTEMS = {
    Health: [
      { id: 'mmis', name: 'Medicaid Management Information System', agency: 'CMS', law: 'HIPAA', standard: 'HL7/FHIR', api: 'limited' },
      { id: 'mco', name: 'Managed Care Organization Claims', agency: 'State Medicaid', law: 'HIPAA', standard: 'HL7/FHIR', api: 'limited' },
      { id: 'bha', name: 'Behavioral Health Authority', agency: 'State BHA', law: '42 CFR Part 2', standard: 'HL7 CCD', api: 'none' },
      { id: 'cmhc_ehr', name: 'Community Mental Health Center EHR', agency: 'State CMHC', law: '42 CFR Part 2', standard: 'HL7/FHIR', api: 'limited' },
      { id: 'hie', name: 'Health Information Exchange', agency: 'State HIE', law: 'HIPAA', standard: 'HL7/FHIR', api: 'full' },
      { id: 'pdmp', name: 'Prescription Drug Monitoring Program', agency: 'State DEA', law: 'HIPAA', standard: 'PMIX/NIEM', api: 'limited' },
      { id: 'va_system', name: 'Veterans Affairs Health System', agency: 'VA', law: 'HIPAA', standard: 'HL7/FHIR', api: 'full' },
      { id: 'vital_records', name: 'Vital Records', agency: 'State Health Dept', law: 'HIPAA', standard: 'HL7 CDA', api: 'none' }
    ],
    Justice: [
      { id: 'doc', name: 'Department of Corrections', agency: 'State DOC', law: 'HIPAA (limited)', standard: 'CJIS', api: 'none' },
      { id: 'cjis', name: 'Criminal Justice Info Services', agency: 'FBI/State', law: 'CJIS Security Policy', standard: 'CJIS', api: 'limited' },
      { id: 'probation_parole', name: 'Probation & Parole System', agency: 'State Courts', law: 'varies', standard: 'varies', api: 'none' },
      { id: 'court_cms', name: 'Court Case Management', agency: 'State Courts', law: 'varies', standard: 'NIEM', api: 'limited' },
      { id: 'sacwis', name: 'Child Welfare Info System', agency: 'State DCFS', law: 'CAPTA / FERPA', standard: 'NCANDS', api: 'none' }
    ],
    Housing: [
      { id: 'hmis', name: 'Homeless Management Info System', agency: 'HUD', law: 'HUD HMIS Privacy', standard: 'HMIS CSV', api: 'limited' },
      { id: 'pha', name: 'Public Housing Authority', agency: 'Local PHA', law: 'Privacy Act', standard: 'HUD-50058', api: 'none' }
    ],
    Income: [
      { id: 'ssa', name: 'Social Security Administration', agency: 'SSA', law: 'Privacy Act', standard: 'SSA proprietary', api: 'limited' },
      { id: 'snap_ebt', name: 'SNAP/EBT Benefits', agency: 'State SNAP', law: 'Privacy Act', standard: 'FNS proprietary', api: 'none' },
      { id: 'tanf', name: 'TANF', agency: 'State TANF', law: 'Privacy Act', standard: 'ACF proprietary', api: 'none' },
      { id: 'unemployment', name: 'Unemployment Insurance', agency: 'State Labor', law: 'Privacy Act', standard: 'varies', api: 'limited' }
    ],
    Education: [
      { id: 'slds', name: 'State Longitudinal Data System', agency: 'State Ed Dept', law: 'FERPA', standard: 'CEDS', api: 'limited' },
      { id: 'special_ed', name: 'Special Education System', agency: 'State Ed Dept', law: 'IDEA / FERPA', standard: 'CEDS', api: 'none' }
    ]
  };

  // Agreement templates
  const AGREEMENT_TEMPLATES = [
    { id: 'tpl_baa', type: 'BAA', name: 'Business Associate Agreement', laws: ['HIPAA', 'HITECH Act', '45 CFR Parts 160 & 164'] },
    { id: 'tpl_dua', type: 'DUA', name: 'Data Use Agreement', laws: ['HIPAA', '45 CFR §164.514(e)'] },
    { id: 'tpl_mou', type: 'MOU', name: 'Memorandum of Understanding', laws: ['Varies by jurisdiction'] },
    { id: 'tpl_idsa', type: 'IDSA', name: 'Interagency Data Sharing Agreement', laws: ['HIPAA', 'Privacy Act of 1974', 'State statutes'] },
    { id: 'tpl_qsoa', type: 'QSOA', name: 'Qualified Service Organization Agreement', laws: ['42 CFR Part 2', 'HIPAA'] },
    { id: 'tpl_hipaa_consent', type: 'HIPAA_consent', name: 'HIPAA Authorization for Disclosure', laws: ['45 CFR §164.508'] },
    { id: 'tpl_ferpa_consent', type: 'FERPA_consent', name: 'FERPA Consent to Disclose', laws: ['20 U.S.C. §1232g', '34 CFR Part 99'] }
  ];

  // Discovery sources
  const DISCOVERY_SOURCES = [
    { type: 'federal_register', name: 'Federal Register', schedule: '24h', url: 'api.federalregister.gov' },
    { type: 'ecfr', name: 'Electronic CFR', schedule: '12h', url: 'ecfr.gov/api' },
    { type: 'state_legislation', name: 'State Legislation', schedule: '6h', url: 'api.legiscan.com' },
    { type: 'academic', name: 'Academic Papers', schedule: '48h', url: 'api.semanticscholar.org' },
    { type: 'news', name: 'News Aggregator', schedule: '4h', url: 'various' },
    { type: 'gap_analysis', name: 'Gap Analysis Engine', schedule: '24h', url: 'internal' }
  ];

  // AI Lab Teammates
  const TEAMMATES = [
    { slug: 'fiscal-alchemist', name: 'The Fiscal Alchemist', title: 'Creative Finance Director', domain: 'finance', icon: '🔮' },
    { slug: 'impact-investor', name: 'The Impact Investor', title: 'Social ROI Specialist', domain: 'investment', icon: '📈' },
    { slug: 'data-inventor', name: 'The Data Inventor', title: 'Data Systems Architect', domain: 'data', icon: '🔬' },
    { slug: 'tech-futurist', name: 'The Tech Futurist', title: 'Emerging Tech Strategist', domain: 'technology', icon: '⚡' },
    { slug: 'legislative-inventor', name: 'The Legislative Inventor', title: 'Policy Innovation Lead', domain: 'policy', icon: '⚖️' },
    { slug: 'regulatory-hacker', name: 'The Regulatory Hacker', title: 'Compliance Innovation', domain: 'regulation', icon: '🔓' },
    { slug: 'service-designer', name: 'The Service Designer', title: 'Human-Centered Design Lead', domain: 'design', icon: '✏️' },
    { slug: 'space-architect', name: 'The Space Architect', title: 'Built Environment Strategist', domain: 'infrastructure', icon: '🏗️' },
    { slug: 'measurement-scientist', name: 'The Measurement Scientist', title: 'Impact Metrics Lead', domain: 'evaluation', icon: '📊' },
    { slug: 'narrative-researcher', name: 'The Narrative Researcher', title: 'Story & Data Translator', domain: 'communications', icon: '📖' },
    { slug: 'market-maker', name: 'The Market Maker', title: 'Systems Market Strategist', domain: 'market', icon: '🏛️' },
    { slug: 'architect', name: 'The Architect', title: 'Systems Integration Lead', domain: 'systems', icon: '🧠' }
  ];

  // Innovation domains
  const INNOVATION_DOMAINS = [
    'health', 'housing', 'income', 'education', 'justice', 'child_welfare',
    'behavioral_health', 'workforce', 'finance', 'technology', 'policy', 'design'
  ];

  // Scrapers
  const SCRAPERS = [
    { name: 'ECFRScraper', source: 'eCFR API', interval: '24h', intervalHrs: 24 },
    { name: 'FederalRegisterScraper', source: 'Federal Register API', interval: '12h', intervalHrs: 12 },
    { name: 'CMSScraper', source: 'CMS Data', interval: '24h', intervalHrs: 24 },
    { name: 'HUDScraper', source: 'HUD Data', interval: '7d', intervalHrs: 168 },
    { name: 'USASpendingScraper', source: 'USASpending.gov', interval: '7d', intervalHrs: 168 },
    { name: 'SystemsScraper', source: 'Gov Systems Registry', interval: '7d', intervalHrs: 168 },
    { name: 'PhillyParcelScraper', source: 'Philly OPA / Carto', interval: '6h', intervalHrs: 6 }
  ];

  // Enrichment types
  const ENRICHMENT_TYPES = [
    { name: 'Provision → Cost Linking', desc: 'Cross-references legal provisions with cost data by dimension' },
    { name: 'Provision → System Linking', desc: 'Maps provisions to government systems they affect' },
    { name: 'Regulatory Conflicts', desc: 'Identifies conflicts between systems (e.g., HIPAA vs 42 CFR Part 2)' },
    { name: 'Coordination Opportunities', desc: 'Calculates coordination savings potential per provision/system pair' },
    { name: 'Fragmentation Hotspots', desc: 'Identifies where multiple provisions create barriers at the same point' },
    { name: 'Parcel Opportunities', desc: 'Overlays zoning, cost, regulatory data on parcels for THAUMA' }
  ];

  // Philadelphia seed data
  const PHILLY_SEED = {
    fips: '42101',
    county: 'Philadelphia, PA',
    total_pop: 1603797,
    median_age: 34.8,
    median_household_income: 52649,
    per_capita_income: 30422,
    poverty_rate: 22.6,
    gini_index: 0.5058,
    snap_households: 171847,
    total_housing_units: 700392,
    vacant_units: 82523,
    median_gross_rent: 1107,
    median_home_value: 200300,
    owner_occupied: 310946,
    renter_occupied: 306923,
    rent_50_plus_pct: 72910,
    medicaid_means_tested: 462596,
    unemployment: 5.1,
    fmr_2br: 1431
  };

  // Maturity levels
  const MATURITY_LEVELS = [
    { level: 'seed', score: 0, threshold: 'Just starting', color: '#94a3b8' },
    { level: 'seedling', score: 1, threshold: 'domes >= 5', color: '#34d399' },
    { level: 'emerging', score: 2, threshold: 'avg_cosm >= 20 AND geo >= 5', color: '#60a5fa' },
    { level: 'growing', score: 3, threshold: 'avg_cosm >= 40 AND geo >= 10', color: '#c9a84c' },
    { level: 'mature', score: 4, threshold: 'avg_cosm >= 60 AND geo >= 20', color: '#a78bfa' }
  ];

  // Tab definitions
  const TABS = [
    { id: 'mesh', label: 'Service Mesh' },
    { id: 'engine', label: 'Data Engine' },
    { id: 'fragment', label: 'Fragment Agent' },
    { id: 'cosm', label: 'Cosm Agent' },
    { id: 'systems', label: 'Gov Systems' },
    { id: 'bridge', label: 'Bridge Engine' },
    { id: 'agreements', label: 'Agreements' },
    { id: 'discovery', label: 'Discovery' },
    { id: 'lab', label: 'AI Lab' },
    { id: 'scraper', label: 'Scrapers' }
  ];

  // ─── Helpers ────────────────────────────────────────────────────
  function h(tag, attrs, children) {
    const el = document.createElement(tag);
    if (attrs) {
      for (const [k, v] of Object.entries(attrs)) {
        if (k === 'class') el.className = v;
        else if (k === 'html') el.innerHTML = v;
        else if (k === 'text') el.textContent = v;
        else if (k.startsWith('on')) el.addEventListener(k.slice(2).toLowerCase(), v);
        else el.setAttribute(k, v);
      }
    }
    if (children) {
      if (typeof children === 'string') el.innerHTML = children;
      else if (Array.isArray(children)) children.forEach(c => { if (c) el.appendChild(c); });
      else el.appendChild(children);
    }
    return el;
  }

  function fmtNum(n) {
    if (n == null) return '—';
    return n.toLocaleString();
  }

  function fmtMoney(n) {
    if (n == null) return '—';
    return '$' + n.toLocaleString();
  }

  // ─── Build Structure ───────────────────────────────────────────
  container.innerHTML = '';
  const root = h('div', { class: 'console-root' });

  // Header
  const header = h('div', { class: 'con-header' });
  header.appendChild(h('h1', { text: 'Representation Console' }));
  header.appendChild(h('p', { text: 'System architecture, data pipelines, agents, and operational intelligence — 18 services across DUOMO and THAUMA product lines' }));
  root.appendChild(header);

  // Tab bar
  const tabBar = h('div', { class: 'con-tabs' });
  TABS.forEach((tab, i) => {
    const el = h('div', { class: 'con-tab' + (i === 0 ? ' active' : ''), text: tab.label, 'data-tab': tab.id });
    el.addEventListener('click', () => switchTab(tab.id));
    tabBar.appendChild(el);
  });
  root.appendChild(tabBar);

  // Content area
  const contentArea = h('div', { class: 'con-content' });

  // Create each section
  const sections = {};
  TABS.forEach((tab, i) => {
    const sec = h('div', { class: 'con-section' + (i === 0 ? ' active' : ''), id: 'con-' + tab.id });
    sections[tab.id] = sec;
    contentArea.appendChild(sec);
  });
  root.appendChild(contentArea);
  container.appendChild(root);

  // Tab switching
  function switchTab(tabId) {
    tabBar.querySelectorAll('.con-tab').forEach(t => t.classList.toggle('active', t.getAttribute('data-tab') === tabId));
    Object.entries(sections).forEach(([id, sec]) => sec.classList.toggle('active', id === tabId));
  }

  // ═══════════════════════════════════════════════════════════════
  // A. SERVICE MESH / ARCHITECTURE DASHBOARD
  // ═══════════════════════════════════════════════════════════════
  (function buildMesh() {
    const sec = sections.mesh;

    sec.appendChild(h('h2', { class: 'con-stitle', text: 'Service Mesh — Architecture Dashboard' }));
    sec.appendChild(h('p', { class: 'con-sdesc', text: '18 microservices (12 DUOMO + 6 THAUMA) orchestrated by baths-engine (:9000). All services expose /api/health endpoints and communicate via HTTP REST.' }));

    // Architecture diagram
    const archText = `<span class="hl">User Browser</span>
    │
    ├── <span class="bl">THAUMA/OS</span> (Next.js :3000)
    │       └── FastAPI backend (:8100)
    │             ├── /api/land/*        parcel viability, clustering
    │             ├── /api/materials/*   9 material system drivers
    │             ├── /api/spheres/*     CRUD, scheduling, WS stream
    │             └── /api/productions/* AI-generated proposals
    │
    ├── <span class="hl">baths-engine</span> (FastAPI + React <span class="gr">:9000</span>)
    │       ├── /api/players/*           player CRUD
    │       ├── /api/productions/*       pipeline advance
    │       ├── /api/data/*              provisions, costs, systems, parcels
    │       ├── /api/fragment/*          Fragment agent outputs
    │       ├── /api/cosm/*              Cosm agent outputs
    │       └── /api/games               game info + data stats
    │             │
    │             ├── <span class="yl">Data Engines</span> (SQLite, auto-scraping)
    │             │     ├── ECFRScraper (24h)  │ FederalRegisterScraper (12h)
    │             │     ├── CMSScraper (24h)   │ HUDScraper (7d)
    │             │     ├── USASpendingScraper (7d) │ SystemsScraper (7d)
    │             │     └── PhillyParcelScraper (6h)
    │             │
    │             └── <span class="gr">Pipeline Director</span> → calls 17 BATHS APIs
    │                   ├── DUOMO APIs (:8000-:8007)
    │                   └── THAUMA APIs (:8008-:8010, :8017-:8019)
    │
    ├── <span class="bl">Fragment Agent</span> (Node.js, GitHub Actions 5x/day)
    │     └── data/fragments/{source-id}/{fips}.json
    │
    └── <span class="bl">Cosm Agent</span> (Node.js, GitHub Actions 5x/day)
          ├── data/domes/{fips}/{archetype}.json
          └── data/cosm.json`;

    sec.appendChild(h('div', { class: 'arch-ascii', html: archText }));

    // Port conflicts
    sec.appendChild(h('div', { class: 'con-sh', text: 'Port Conflict Warnings' }));
    PORT_CONFLICTS.forEach(pc => {
      sec.appendChild(h('div', { class: 'port-warn', html: `<strong>Port ${pc.port}</strong> — shared by: ${pc.services.join(', ')} <span style="color:rgba(245,240,232,0.4)">• ${pc.note}</span>` }));
    });

    sec.appendChild(h('hr', { class: 'con-divider' }));

    // Central orchestrator
    sec.appendChild(h('div', { class: 'con-sh', text: 'baths-engine — Central Orchestrator (:9000)' }));
    const engineCard = h('div', { class: 'con-card' });
    engineCard.innerHTML = `
      <div class="con-card-title"><span class="dot dot-gold"></span>baths-engine</div>
      <div class="con-card-sub">Port 9000 • FastAPI + React • SQLite • v0.2.0</div>
      <div class="con-card-body">
        Unified game engine sitting above both DUOMO and THAUMA. Routes players through production pipelines,
        calling all 17 backend APIs via the Pipeline Director. Manages data engines, Fragment/Cosm agents,
        and serves the static frontend.<br><br>
        <span class="con-label">Key Endpoints</span><br>
        <span class="ep-pill">/api/players</span>
        <span class="ep-pill">/api/productions</span>
        <span class="ep-pill">/api/data/stats</span>
        <span class="ep-pill">/api/data/scrape</span>
        <span class="ep-pill">/api/fragment/stats</span>
        <span class="ep-pill">/api/cosm/state</span>
        <span class="ep-pill">/api/games</span>
      </div>`;
    sec.appendChild(engineCard);

    sec.appendChild(h('hr', { class: 'con-divider' }));

    // Service Grid — DUOMO
    sec.appendChild(h('div', { class: 'con-sh', text: 'DUOMO Services (12)' }));
    const duomoGrid = h('div', { class: 'con-grid-3' });
    SERVICES.filter(s => s.group === 'DUOMO').forEach(s => {
      const card = h('div', { class: 'con-card' });
      card.innerHTML = `
        <div class="con-card-title"><span class="dot dot-green"></span>${s.name}</div>
        <div class="con-card-sub">:${s.port}</div>
        <div class="con-card-body">
          ${s.desc}<br>
          <div style="margin-top:0.4rem">
            ${s.endpoints.map(e => `<span class="ep-pill">${e}</span>`).join('')}
          </div>
        </div>`;
      duomoGrid.appendChild(card);
    });
    sec.appendChild(duomoGrid);

    // Service Grid — THAUMA
    sec.appendChild(h('div', { class: 'con-sh', text: 'THAUMA Services (6)' }));
    const thaumaGrid = h('div', { class: 'con-grid-3' });
    SERVICES.filter(s => s.group === 'THAUMA').forEach(s => {
      const card = h('div', { class: 'con-card' });
      card.innerHTML = `
        <div class="con-card-title"><span class="dot dot-green"></span>${s.name}</div>
        <div class="con-card-sub">:${s.port}</div>
        <div class="con-card-body">
          ${s.desc}<br>
          <div style="margin-top:0.4rem">
            ${s.endpoints.map(e => `<span class="ep-pill">${e}</span>`).join('')}
          </div>
        </div>`;
      thaumaGrid.appendChild(card);
    });
    sec.appendChild(thaumaGrid);
  })();

  // ═══════════════════════════════════════════════════════════════
  // B. DATA ENGINE STATS
  // ═══════════════════════════════════════════════════════════════
  (function buildEngine() {
    const sec = sections.engine;

    sec.appendChild(h('h2', { class: 'con-stitle', text: 'Data Engine — Accumulated Statistics' }));
    sec.appendChild(h('p', { class: 'con-sdesc', text: 'Real data from baths-engine SQLite database. 7 scrape runs completed, 6 enrichment passes per cycle.' }));

    // Stat blocks
    const statRow = h('div', { class: 'con-stat-row' });
    const stats = [
      { val: fmtNum(ENGINE_STATS.provisions), label: 'Provisions' },
      { val: ENGINE_STATS.cost_points, label: 'Cost Points' },
      { val: ENGINE_STATS.gov_systems, label: 'Gov Systems' },
      { val: ENGINE_STATS.system_links, label: 'System Links' },
      { val: ENGINE_STATS.parcels, label: 'Parcels' },
      { val: fmtNum(ENGINE_STATS.enrichments), label: 'Enrichments' },
      { val: ENGINE_STATS.total_scrape_runs, label: 'Scrape Runs' },
      { val: ENGINE_STATS.db_size_mb + ' MB', label: 'DB Size' }
    ];
    stats.forEach(s => {
      const block = h('div', { class: 'con-stat' });
      block.innerHTML = `<div class="con-stat-val">${s.val}</div><div class="con-stat-label">${s.label}</div>`;
      statRow.appendChild(block);
    });
    sec.appendChild(statRow);

    // Data growth chart
    sec.appendChild(h('div', { class: 'con-sh', text: 'Data Growth Over Scrape Runs' }));
    const chartWrap1 = h('div', { class: 'con-chart-wrap' });
    const canvas1 = h('canvas', { id: 'engine-growth-chart' });
    chartWrap1.appendChild(canvas1);
    sec.appendChild(chartWrap1);

    // Data breakdown chart
    sec.appendChild(h('div', { class: 'con-sh', text: 'Breakdown by Data Type' }));
    const chartWrap2 = h('div', { class: 'con-chart-wrap' });
    const canvas2 = h('canvas', { id: 'engine-breakdown-chart' });
    chartWrap2.appendChild(canvas2);
    sec.appendChild(chartWrap2);

    sec.appendChild(h('hr', { class: 'con-divider' }));

    // Enrichment types
    sec.appendChild(h('div', { class: 'con-sh', text: 'Enrichment Engine — 6 Passes Per Cycle' }));
    const enrichGrid = h('div', { class: 'con-grid-3' });
    ENRICHMENT_TYPES.forEach((et, i) => {
      const card = h('div', { class: 'con-card' });
      card.innerHTML = `
        <div class="con-card-title"><span class="dot dot-blue"></span>Pass ${i + 1}: ${et.name}</div>
        <div class="con-card-body">${et.desc}</div>`;
      enrichGrid.appendChild(card);
    });
    sec.appendChild(enrichGrid);

    // Render charts after DOM insertion
    requestAnimationFrame(() => {
      if (typeof Chart === 'undefined') return;

      const goldA = 'rgba(201,168,76,0.8)';
      const goldB = 'rgba(201,168,76,0.15)';
      const blueA = 'rgba(96,165,250,0.8)';
      const greenA = 'rgba(52,211,153,0.8)';

      // Growth chart — simulated growth over 7 runs
      const growthData = [
        { run: 1, prov: 732, cost: 35, sys: 19, enrich: 0 },
        { run: 2, prov: 1465, cost: 35, sys: 19, enrich: 684 },
        { run: 3, prov: 2196, cost: 35, sys: 19, enrich: 1372 },
        { run: 4, prov: 2930, cost: 35, sys: 19, enrich: 2061 },
        { run: 5, prov: 3662, cost: 35, sys: 19, enrich: 2942 },
        { run: 6, prov: 4394, cost: 35, sys: 19, enrich: 3918 },
        { run: 7, prov: 5126, cost: 35, sys: 19, enrich: 4898 }
      ];

      new Chart(canvas1.getContext('2d'), {
        type: 'line',
        data: {
          labels: growthData.map(d => 'Run ' + d.run),
          datasets: [
            { label: 'Provisions', data: growthData.map(d => d.prov), borderColor: goldA, backgroundColor: goldB, fill: true, tension: 0.3 },
            { label: 'Enrichments', data: growthData.map(d => d.enrich), borderColor: blueA, backgroundColor: 'transparent', tension: 0.3 }
          ]
        },
        options: {
          responsive: true,
          plugins: { legend: { labels: { color: 'rgba(245,240,232,0.6)', font: { size: 11 } } } },
          scales: {
            x: { ticks: { color: 'rgba(245,240,232,0.4)', font: { size: 10 } }, grid: { color: 'rgba(201,168,76,0.06)' } },
            y: { ticks: { color: 'rgba(245,240,232,0.4)', font: { size: 10 } }, grid: { color: 'rgba(201,168,76,0.06)' } }
          }
        }
      });

      // Breakdown doughnut
      new Chart(canvas2.getContext('2d'), {
        type: 'doughnut',
        data: {
          labels: ['Provisions (5,126)', 'Enrichments (4,898)', 'Cost Points (35)', 'Gov Systems (19)', 'System Links (19)', 'Parcels (14)'],
          datasets: [{
            data: [5126, 4898, 35, 19, 19, 14],
            backgroundColor: [goldA, blueA, greenA, 'rgba(167,139,250,0.8)', 'rgba(251,191,36,0.8)', 'rgba(248,113,113,0.8)'],
            borderColor: '#0a0a0f',
            borderWidth: 2
          }]
        },
        options: {
          responsive: true,
          plugins: {
            legend: { position: 'right', labels: { color: 'rgba(245,240,232,0.6)', font: { size: 11 }, padding: 12 } }
          }
        }
      });
    });
  })();

  // ═══════════════════════════════════════════════════════════════
  // C. FRAGMENT AGENT PIPELINE
  // ═══════════════════════════════════════════════════════════════
  (function buildFragment() {
    const sec = sections.fragment;

    sec.appendChild(h('h2', { class: 'con-stitle', text: 'Fragment Agent — Data Collection Pipeline' }));
    sec.appendChild(h('p', { class: 'con-sdesc', text: 'Node.js agent scheduled 5x daily via GitHub Actions (7am, 12pm, 5pm, 10pm, 3am UTC). Each run processes ~30 source×geography pairs, prioritizing never-scraped and oldest data.' }));

    // Schedule badge
    const schedBlock = h('div', { class: 'con-card', style: 'margin-bottom:1.25rem' });
    schedBlock.innerHTML = `
      <div class="con-card-title"><span class="dot dot-gold"></span>GitHub Actions Schedule</div>
      <div class="con-card-body mono" style="font-size:0.72rem">
        <span class="con-badge badge-gold">07:00 UTC</span>
        <span class="con-badge badge-gold">12:00 UTC</span>
        <span class="con-badge badge-gold">17:00 UTC</span>
        <span class="con-badge badge-gold">22:00 UTC</span>
        <span class="con-badge badge-gold">03:00 UTC</span>
        <span style="color:rgba(245,240,232,0.35); margin-left:0.5rem">• ~30 pairs per run • Priority: never-scraped → oldest → gaps last</span>
      </div>`;
    sec.appendChild(schedBlock);

    // Counties by region
    sec.appendChild(h('div', { class: 'con-sh', text: '28 Priority Counties by Region' }));
    const countyGrid = h('div', { class: 'con-grid-2' });
    Object.entries(COUNTIES).forEach(([region, counties]) => {
      const card = h('div', { class: 'con-card' });
      let countyHTML = counties.map(c =>
        `<div style="display:flex;justify-content:space-between;padding:0.15rem 0"><span>${c.name}</span><span class="mono" style="color:#c9a84c;font-size:0.65rem">${c.fips}</span></div>`
      ).join('');
      card.innerHTML = `
        <div class="con-card-title">${region} <span class="con-badge badge-blue">${counties.length}</span></div>
        <div class="con-card-body">${countyHTML}</div>`;
      countyGrid.appendChild(card);
    });
    sec.appendChild(countyGrid);

    sec.appendChild(h('hr', { class: 'con-divider' }));

    // ACS Variable Groups
    sec.appendChild(h('div', { class: 'con-sh', text: '10 Census ACS Variable Groups' }));
    const acsGrid = h('div', { class: 'con-grid-3' });
    ACS_GROUPS.forEach(g => {
      const card = h('div', { class: 'con-card' });
      card.innerHTML = `
        <div class="con-card-title"><span class="dot dot-blue"></span>${g.label}</div>
        <div class="con-card-sub">${g.id}</div>
        <div class="con-card-body mono" style="font-size:0.65rem">${g.vars}</div>`;
      acsGrid.appendChild(card);
    });
    sec.appendChild(acsGrid);

    sec.appendChild(h('hr', { class: 'con-divider' }));

    // External Sources
    sec.appendChild(h('div', { class: 'con-sh', text: 'External Data Sources' }));
    const srcTable = h('table', { class: 'con-table' });
    srcTable.innerHTML = `
      <thead><tr><th>Source</th><th>Name</th><th>API</th><th>Status</th></tr></thead>
      <tbody>
        ${EXTERNAL_SOURCES.map(s => `
          <tr>
            <td class="mono" style="font-size:0.68rem">${s.id}</td>
            <td>${s.name}</td>
            <td style="font-size:0.7rem">${s.api}</td>
            <td>${s.status === 'active'
              ? '<span class="con-badge badge-green">ACTIVE</span>'
              : '<span class="con-badge badge-red">GAP</span>'
            }</td>
          </tr>`).join('')}
      </tbody>`;
    sec.appendChild(srcTable);

    sec.appendChild(h('hr', { class: 'con-divider' }));

    // Fragment file format
    sec.appendChild(h('div', { class: 'con-sh', text: 'Fragment File Format' }));
    const fmtCard = h('div', { class: 'arch-ascii' });
    fmtCard.innerHTML = `<span class="hl">data/fragments/{source-id}/{fips}.json</span>

{
  "<span class="gr">source</span>":       "census-income",
  "<span class="gr">source_label</span>": "Census Income & Poverty",
  "<span class="gr">api</span>":          "Census ACS 5-year",
  "<span class="gr">fips</span>":         "42101",
  "<span class="gr">county_name</span>":  "Philadelphia, PA",
  "<span class="gr">scraped_at</span>":   "2026-03-08T...",
  "<span class="gr">data</span>": {
    "median_household_income": 52649,
    "per_capita_income": 30422,
    "poverty_total": 1541987,
    "poverty_below": 347948,
    "gini_index": 0.5058,
    "snap_households": 171847
  }
}`;
    sec.appendChild(fmtCard);
  })();

  // ═══════════════════════════════════════════════════════════════
  // D. COSM AGENT DASHBOARD
  // ═══════════════════════════════════════════════════════════════
  (function buildCosm() {
    const sec = sections.cosm;

    sec.appendChild(h('h2', { class: 'con-stitle', text: 'Cosm Agent — Dome Assembly Engine' }));
    sec.appendChild(h('p', { class: 'con-sdesc', text: 'Assembles fragments into domes for 6 archetypes × N geographies. Cosm score uses the weakest-link principle: cosm = min(domain_1, domain_2, ..., domain_12). Runs after Fragment agent via GitHub Actions.' }));

    // Archetype profiles
    sec.appendChild(h('div', { class: 'con-sh', text: '6 Archetype Profiles' }));
    const archGrid = h('div', { class: 'con-grid-3' });
    ARCHETYPES.forEach(a => {
      const card = h('div', { class: 'con-card' });
      const fpl = 15060 + 5380 * (a.hh - 1);
      const pctFPL = Math.round((a.income / fpl) * 100);
      card.innerHTML = `
        <div class="con-card-title">${a.name} <span class="con-badge badge-gold">${a.id}</span></div>
        <div class="con-card-sub">Age ${a.age} • ${fmtMoney(a.income)}/yr • HH: ${a.hh} • Children: ${a.children}</div>
        <div class="con-card-body">
          ${a.desc}<br>
          <span style="color:#c9a84c">${pctFPL}% FPL</span> (FPL for HH ${a.hh}: ${fmtMoney(fpl)})
        </div>`;
      archGrid.appendChild(card);
    });
    sec.appendChild(archGrid);

    sec.appendChild(h('hr', { class: 'con-divider' }));

    // Cosm state / currency
    sec.appendChild(h('div', { class: 'con-sh', text: 'Cosm State / Currency' }));
    const stateCard = h('div', { class: 'arch-ascii' });
    stateCard.innerHTML = `<span class="hl">data/cosm.json</span>

{
  "<span class="gr">total_domes</span>":              N,          <span class="yl">// 6 archetypes × geographies</span>
  "<span class="gr">geographies</span>":              N,          <span class="yl">// counties with assembled domes</span>
  "<span class="gr">archetypes</span>":               6,
  "<span class="gr">average_cosm</span>":             X,          <span class="yl">// mean of min(domain_scores)</span>
  "<span class="gr">min_cosm</span>":                 X,
  "<span class="gr">max_cosm</span>":                 X,
  "<span class="gr">total_fragmented_cost</span>":    X,
  "<span class="gr">total_coordinated_cost</span>":   X,
  "<span class="gr">total_coordination_savings</span>": X,       <span class="yl">// delta = fragmented - coordinated</span>
  "<span class="gr">average_delta_per_dome</span>":   X,
  "<span class="gr">maturity</span>": { "level": "seed", "score": 0 },
  "<span class="gr">programs_mapped</span>":          N,
  "<span class="gr">total_gap_count</span>":          N
}`;
    sec.appendChild(stateCard);

    // Maturity levels
    sec.appendChild(h('div', { class: 'con-sh', text: 'Maturity Levels' }));
    const matFlow = h('div', { class: 'con-flow' });
    MATURITY_LEVELS.forEach((m, i) => {
      const step = h('div', { class: 'con-flow-step', style: `background: ${m.color}22; color: ${m.color}; border: 1px solid ${m.color}44` });
      step.innerHTML = `${m.level} (${m.score})<br><span style="font-size:0.58rem;opacity:0.7">${m.threshold}</span>`;
      matFlow.appendChild(step);
      if (i < MATURITY_LEVELS.length - 1) matFlow.appendChild(h('span', { class: 'con-flow-arrow', text: '→' }));
    });
    sec.appendChild(matFlow);

    sec.appendChild(h('hr', { class: 'con-divider' }));

    // Pattern detection
    sec.appendChild(h('div', { class: 'con-sh', text: 'Pattern Detection' }));
    const patGrid = h('div', { class: 'con-grid-2' });
    const patterns = [
      { name: 'Geographic Deltas', desc: 'Same archetype across geographies — flags spread > $1,000 in coordination savings' },
      { name: 'Common Gaps', desc: 'Top 20 recurring domain:type gaps across all assembled domes' },
      { name: 'Program Clusters', desc: 'Count of each federal program appearing across all domes' },
      { name: 'Cosm Distribution', desc: 'min, max, median cosm scores by geography and archetype' }
    ];
    patterns.forEach(p => {
      const card = h('div', { class: 'con-card' });
      card.innerHTML = `<div class="con-card-title"><span class="dot dot-gold"></span>${p.name}</div><div class="con-card-body">${p.desc}</div>`;
      patGrid.appendChild(card);
    });
    sec.appendChild(patGrid);

    sec.appendChild(h('hr', { class: 'con-divider' }));

    // Philadelphia seed data
    sec.appendChild(h('div', { class: 'con-sh', text: 'Philadelphia Seed Data (42101)' }));
    const phillyStats = h('div', { class: 'con-stat-row' });
    const ps = PHILLY_SEED;
    const phillyItems = [
      { val: fmtNum(ps.total_pop), label: 'Population' },
      { val: fmtMoney(ps.median_household_income), label: 'Median Income' },
      { val: ps.poverty_rate + '%', label: 'Poverty Rate' },
      { val: ps.gini_index.toFixed(4), label: 'Gini Index' },
      { val: fmtNum(ps.vacant_units), label: 'Vacant Units' },
      { val: fmtMoney(ps.median_gross_rent), label: 'Median Rent' },
      { val: fmtNum(ps.medicaid_means_tested), label: 'Medicaid' },
      { val: fmtMoney(ps.fmr_2br) + '/mo', label: 'FMR 2BR' }
    ];
    phillyItems.forEach(pi => {
      const block = h('div', { class: 'con-stat' });
      block.innerHTML = `<div class="con-stat-val" style="font-size:1.15rem">${pi.val}</div><div class="con-stat-label">${pi.label}</div>`;
      phillyStats.appendChild(block);
    });
    sec.appendChild(phillyStats);

    // Cost model formulas
    sec.appendChild(h('div', { class: 'con-sh', text: 'Coordination Savings Model' }));
    const costFormula = h('div', { class: 'arch-ascii' });
    costFormula.innerHTML = `<span class="hl">Cost Calculation Algorithm</span>

fragmented_cost = sum(all eligible program values) × <span class="gr">1.30</span>   <span class="yl">// +30% admin overhead</span>
coordinated_cost = fragmented_cost × <span class="gr">0.60</span>                    <span class="yl">// 40% reduction</span>
delta = fragmented_cost − coordinated_cost                   <span class="yl">// coordination savings</span>

<span class="hl">Cosm Score (weakest-link principle)</span>

cosm = <span class="gr">min</span>(domain_1, domain_2, ..., domain_12)
cosm_average = mean(all domain scores)

<span class="hl">Flourishing Score (baths-engine)</span>

composite = min(scores) × <span class="gr">0.6</span> + average(scores) × <span class="gr">0.4</span>`;
    sec.appendChild(costFormula);
  })();

  // ═══════════════════════════════════════════════════════════════
  // E. GOVERNMENT SYSTEMS EXPLORER
  // ═══════════════════════════════════════════════════════════════
  (function buildSystems() {
    const sec = sections.systems;

    sec.appendChild(h('h2', { class: 'con-stitle', text: 'Government Systems Explorer' }));

    const totalSystems = Object.values(GOV_SYSTEMS).reduce((s, arr) => s + arr.length, 0);
    sec.appendChild(h('p', { class: 'con-sdesc', text: `Full registry of ${totalSystems} government data systems organized by domain. Each system tracks agency ownership, privacy law, data standard, and API availability.` }));

    // Domain overview stats
    const domainStats = h('div', { class: 'con-stat-row' });
    Object.entries(GOV_SYSTEMS).forEach(([domain, systems]) => {
      const block = h('div', { class: 'con-stat' });
      block.innerHTML = `<div class="con-stat-val">${systems.length}</div><div class="con-stat-label">${domain}</div>`;
      domainStats.appendChild(block);
    });
    sec.appendChild(domainStats);

    // Systems tables by domain
    Object.entries(GOV_SYSTEMS).forEach(([domain, systems]) => {
      sec.appendChild(h('div', { class: 'con-sh', text: `${domain} Systems (${systems.length})` }));
      const table = h('table', { class: 'con-table' });
      table.innerHTML = `
        <thead><tr><th>ID</th><th>System Name</th><th>Agency</th><th>Privacy Law</th><th>Standard</th><th>API</th></tr></thead>
        <tbody>
          ${systems.map(s => `
            <tr>
              <td class="mono" style="font-size:0.68rem;color:#c9a84c">${s.id}</td>
              <td>${s.name}</td>
              <td style="font-size:0.72rem">${s.agency}</td>
              <td><span class="con-badge badge-yellow">${s.law}</span></td>
              <td class="mono" style="font-size:0.68rem">${s.standard}</td>
              <td>${s.api === 'full'
                ? '<span class="con-badge badge-green">full</span>'
                : s.api === 'limited'
                  ? '<span class="con-badge badge-yellow">limited</span>'
                  : '<span class="con-badge badge-red">none</span>'
              }</td>
            </tr>`).join('')}
        </tbody>`;
      sec.appendChild(table);
    });

    sec.appendChild(h('hr', { class: 'con-divider' }));

    // Gap barriers
    sec.appendChild(h('div', { class: 'con-sh', text: 'Gap Barrier Types' }));
    const barrierGrid = h('div', { class: 'con-grid-3' });
    const barriers = [
      { type: 'Legal', desc: 'Statutory restrictions preventing data sharing (HIPAA, FERPA, 42 CFR Part 2)', color: '#f87171' },
      { type: 'Technical', desc: 'Incompatible data standards, missing APIs, format mismatches', color: '#fbbf24' },
      { type: 'Political', desc: 'Agency turf wars, lack of political will, stakeholder resistance', color: '#a78bfa' },
      { type: 'Funding', desc: 'No budget allocated for integration, competing priorities', color: '#60a5fa' },
      { type: 'Consent', desc: 'Individual consent required but no mechanism in place', color: '#34d399' }
    ];
    barriers.forEach(b => {
      const card = h('div', { class: 'con-card', style: `border-left: 3px solid ${b.color}` });
      card.innerHTML = `<div class="con-card-title" style="color:${b.color}">${b.type}</div><div class="con-card-body">${b.desc}</div>`;
      barrierGrid.appendChild(card);
    });
    sec.appendChild(barrierGrid);

    sec.appendChild(h('hr', { class: 'con-divider' }));

    // Data flow direction
    sec.appendChild(h('div', { class: 'con-sh', text: 'System Connection Data Flow' }));
    const flowCard = h('div', { class: 'arch-ascii' });
    flowCard.innerHTML = `<span class="hl">Connection Fields</span>

source_id → target_id
direction:   <span class="gr">unidirectional</span> | <span class="bl">bidirectional</span>
format:      HL7/FHIR, CJIS, HMIS CSV, SSA proprietary, etc.
frequency:   real-time | daily | monthly | quarterly | annual
governing:   BAA | MOU | IDSA | statutory | none
reliability: <span class="gr">high</span> | <span class="yl">medium</span> | <span style="color:#f87171">low</span>

<span class="hl">System Link Types</span>

link_type:       <span class="gr">active</span> | <span style="color:#f87171">blocked</span> | <span class="yl">possible</span>
mechanism:       API, file transfer, manual, consent-gated
consent_barrier: boolean — does this link require individual consent?
legal_authority: statutory citation authorizing the data exchange`;
    sec.appendChild(flowCard);
  })();

  // ═══════════════════════════════════════════════════════════════
  // F. BRIDGE ENGINE
  // ═══════════════════════════════════════════════════════════════
  (function buildBridge() {
    const sec = sections.bridge;

    sec.appendChild(h('h2', { class: 'con-stitle', text: 'Bridge Engine' }));
    sec.appendChild(h('p', { class: 'con-sdesc', text: 'Computes bridge priority scores, identifies quick wins, and sequences implementation phases to close data-sharing gaps between government systems.' }));

    // Priority formula
    sec.appendChild(h('div', { class: 'con-sh', text: 'Priority Calculation' }));
    const prioCard = h('div', { class: 'arch-ascii' });
    prioCard.innerHTML = `<span class="hl">Bridge Priority Formula</span>

priority = <span class="gr">min</span>(10.0, (impact_score / effort_score) × 2.0)

<span class="yl">// If effort_score == 0 → priority = 10.0 (max)</span>
<span class="yl">// Clamped to [0.0, 10.0]</span>

<span class="hl">Ranking Sort Key</span> (ascending tuple — lowest wins)

  1. <span class="gr">-priority_score</span>     higher priority first
  2. <span class="gr">consent_type_flag</span>   0 if consent bridge, else 1 (consent first)
  3. <span class="gr">min_cost</span>            from parsed estimated_cost string

<span class="hl">Quick Win Criteria</span>

effort_score ≤ <span class="gr">3</span>  AND  impact_score ≥ <span class="gr">7</span>`;
    sec.appendChild(prioCard);

    sec.appendChild(h('hr', { class: 'con-divider' }));

    // Implementation phases
    sec.appendChild(h('div', { class: 'con-sh', text: 'Implementation Phases' }));
    const phases = [
      { num: 1, name: 'Consent & Authorization', type: 'consent', desc: 'Individual consent forms, HIPAA authorizations, 42 CFR Part 2 waivers', color: '#34d399' },
      { num: 2, name: 'Legal & Regulatory', type: 'legal', desc: 'BAA, DUA, MOU, IDSA agreements; statutory compliance review', color: '#60a5fa' },
      { num: 3, name: 'Technical Integration', type: 'technical', desc: 'API development, data mapping, format conversion, testing', color: '#c9a84c' },
      { num: 4, name: 'Political & Funding', type: 'political + funding', desc: 'Stakeholder alignment, budget appropriation, political buy-in', color: '#a78bfa' }
    ];
    const phaseGrid = h('div', { class: 'con-grid-2' });
    phases.forEach(p => {
      const card = h('div', { class: 'con-card', style: `border-left: 3px solid ${p.color}` });
      card.innerHTML = `
        <div class="con-card-title" style="color:${p.color}">Phase ${p.num}: ${p.name}</div>
        <div class="con-card-sub">bridge_type: ${p.type}</div>
        <div class="con-card-body">${p.desc}</div>`;
      phaseGrid.appendChild(card);
    });
    sec.appendChild(phaseGrid);

    sec.appendChild(h('hr', { class: 'con-divider' }));

    // Cost functions
    sec.appendChild(h('div', { class: 'con-sh', text: 'Cost Parsing & Aggregation' }));
    const costCard = h('div', { class: 'arch-ascii' });
    costCard.innerHTML = `<span class="hl">parse_cost(cost_str) → (min_float, max_float)</span>

Input:     "$500K"       → (500,000, 500,000)
Input:     "$500K-1M"    → (500,000, 1,000,000)
Input:     "$2-5M"       → (2,000,000, 5,000,000)
Input:     "Unknown"     → (0, 0)
Multipliers:  K → 1,000  │  M → 1,000,000  │  B → 1,000,000,000

<span class="hl">aggregate_bridge_costs(bridges) → dict</span>

{
  total_min:       sum of all min costs,
  total_max:       sum of all max costs,
  formatted_total: "$X–$Y" formatted string,
  bridge_count:    number of bridges aggregated
}

<span class="hl">cost_by_category(db)</span>   → grouped by bridge_type (consent/legal/technical/...)
<span class="hl">cost_by_barrier(db)</span>    → grouped by parent gap's barrier_type`;
    sec.appendChild(costCard);

    sec.appendChild(h('hr', { class: 'con-divider' }));

    // Consent pathway
    sec.appendChild(h('div', { class: 'con-sh', text: 'Consent Pathway Analysis' }));
    const consentCard = h('div', { class: 'con-card' });
    consentCard.innerHTML = `
      <div class="con-card-title"><span class="dot dot-green"></span>Consent-Closable Gaps</div>
      <div class="con-card-body">
        Gaps where <code style="color:#c9a84c">consent_closable = true</code> can be bridged by individual authorization alone.<br><br>
        <strong>get_consent_pathways(db, circumstances)</strong> — filters gaps applicable to the person's circumstances,
        sorts by severity (critical → high → medium → low).<br><br>
        <strong>build_consent_checklist(db, circumstances)</strong> — finds all consent-type bridges,
        sorted by impact_score descending. Returns actionable checklist for the individual.<br><br>
        <strong>Severity order:</strong>
        <span class="con-badge badge-red">critical: 0</span>
        <span class="con-badge badge-yellow">high: 1</span>
        <span class="con-badge badge-blue">medium: 2</span>
        <span class="con-badge badge-green">low: 3</span>
      </div>`;
    sec.appendChild(consentCard);
  })();

  // ═══════════════════════════════════════════════════════════════
  // G. AGREEMENT & COMPLIANCE REGISTRY
  // ═══════════════════════════════════════════════════════════════
  (function buildAgreements() {
    const sec = sections.agreements;

    sec.appendChild(h('h2', { class: 'con-stitle', text: 'Agreement & Compliance Registry' }));
    sec.appendChild(h('p', { class: 'con-sdesc', text: 'Legal agreement generation engine. 7 core templates, compliance validation against governing laws, and automated gap-to-agreement mapping. Default jurisdiction: Pennsylvania.' }));

    // Templates table
    sec.appendChild(h('div', { class: 'con-sh', text: '7 Agreement Templates' }));
    const tplTable = h('table', { class: 'con-table' });
    tplTable.innerHTML = `
      <thead><tr><th>Type</th><th>Full Name</th><th>Governing Laws</th></tr></thead>
      <tbody>
        ${AGREEMENT_TEMPLATES.map(t => `
          <tr>
            <td><span class="con-badge badge-gold">${t.type}</span></td>
            <td>${t.name}</td>
            <td style="font-size:0.7rem">${t.laws.join(', ')}</td>
          </tr>`).join('')}
      </tbody>`;
    sec.appendChild(tplTable);

    sec.appendChild(h('hr', { class: 'con-divider' }));

    // Gap to agreement mapping
    sec.appendChild(h('div', { class: 'con-sh', text: 'Gap → Agreement Mapping' }));
    const mapCard = h('div', { class: 'arch-ascii' });
    mapCard.innerHTML = `<span class="hl">GAP_TO_AGREEMENT_MAP</span> (barrier_law → agreement types)

HIPAA                           → [<span class="gr">BAA</span>, <span class="gr">HIPAA_consent</span>]
42 CFR Part 2                   → [<span class="gr">QSOA</span>, <span class="gr">42CFR_consent</span>]
FERPA                           → [<span class="gr">FERPA_consent</span>]
CJIS_Security_Policy            → [<span class="gr">IDSA</span>]
Medicaid Inmate Exclusion       → [<span class="gr">IDSA</span>, <span class="gr">HIPAA_consent</span>]
Privacy Act / 42 CFR Part 2     → [<span class="gr">42CFR_consent</span>, <span class="gr">DUA</span>]

<span class="hl">BARRIER_TYPE_MAP</span> (fallback)

legal     → [IDSA, MOU]
technical → [IDSA, MOU, joint_funding]
political → [MOU, compact]
funding   → [joint_funding, MOU]
consent   → [HIPAA_consent]
<span class="yl">default   → [MOU]</span>`;
    sec.appendChild(mapCard);

    sec.appendChild(h('hr', { class: 'con-divider' }));

    // Status transitions
    sec.appendChild(h('div', { class: 'con-sh', text: 'Status Transitions' }));
    const statusFlow = h('div', { class: 'con-flow' });
    const statusSteps = [
      { label: 'draft', color: '#94a3b8' },
      { label: 'in_review', color: '#fbbf24' },
      { label: 'executed', color: '#34d399' }
    ];
    statusSteps.forEach((s, i) => {
      const step = h('div', { class: 'con-flow-step', style: `background: ${s.color}22; color: ${s.color}; border: 1px solid ${s.color}44` });
      step.textContent = s.label;
      statusFlow.appendChild(step);
      if (i < statusSteps.length - 1) statusFlow.appendChild(h('span', { class: 'con-flow-arrow', text: '→' }));
    });
    sec.appendChild(statusFlow);

    const transCard = h('div', { class: 'con-card' });
    transCard.innerHTML = `
      <div class="con-card-body">
        <strong>draft</strong> → in_review<br>
        <strong>in_review</strong> → executed <em>or</em> → draft (rejection)<br>
        <strong>executed</strong> → <em>(terminal state)</em><br><br>
        Default expiration: <span class="mono" style="color:#c9a84c">365 days</span> from generation date<br>
        Default jurisdiction: <span class="mono" style="color:#c9a84c">Pennsylvania</span><br>
        QSOA criminal penalties: First offense ≤$500, subsequent ≤$5,000 (42 CFR Part 2, §2.12)
      </div>`;
    sec.appendChild(transCard);

    sec.appendChild(h('hr', { class: 'con-divider' }));

    // Compliance rules
    sec.appendChild(h('div', { class: 'con-sh', text: 'Compliance Validation' }));
    const compCard = h('div', { class: 'con-card' });
    compCard.innerHTML = `
      <div class="con-card-title"><span class="dot dot-blue"></span>validate_agreement(agreement, db)</div>
      <div class="con-card-body">
        Checks all <code style="color:#c9a84c">ComplianceRule</code> records where the agreement type is in the rule's <code style="color:#c9a84c">applies_to</code> list.<br><br>
        Returns: <code class="mono" style="color:#34d399">{ status: "compliant" | "flagged", flags: [...] }</code><br><br>
        Each rule has severity: <span class="con-badge badge-red">required</span> or <span class="con-badge badge-yellow">recommended</span><br>
        Rules include model provision language that can be inserted into generated agreements.
      </div>`;
    sec.appendChild(compCard);

    // Consent form builders
    sec.appendChild(h('div', { class: 'con-sh', text: 'Consent Form Builders' }));
    const consentGrid = h('div', { class: 'con-grid-2' });
    const consentTypes = [
      { name: 'HIPAA Authorization', fn: '_build_hipaa_authorization', law: '45 CFR §164.508' },
      { name: '42 CFR Part 2 Consent', fn: '_build_cfr42_consent', law: '42 CFR Part 2' },
      { name: 'FERPA Release', fn: '_build_ferpa_release', law: '20 U.S.C. §1232g' },
      { name: 'General Release', fn: '_build_general_release', law: 'varies' }
    ];
    consentTypes.forEach(ct => {
      const card = h('div', { class: 'con-card' });
      card.innerHTML = `
        <div class="con-card-title"><span class="dot dot-green"></span>${ct.name}</div>
        <div class="con-card-sub">${ct.fn}(gap)</div>
        <div class="con-card-body">Governing law: <span class="con-badge badge-yellow">${ct.law}</span></div>`;
      consentGrid.appendChild(card);
    });
    sec.appendChild(consentGrid);
  })();

  // ═══════════════════════════════════════════════════════════════
  // H. DISCOVERY SCANNER
  // ═══════════════════════════════════════════════════════════════
  (function buildDiscovery() {
    const sec = sections.discovery;

    sec.appendChild(h('h2', { class: 'con-stitle', text: 'Discovery Scanner' }));
    sec.appendChild(h('p', { class: 'con-sdesc', text: 'Regulatory change discovery engine. 6 sources scanned on independent schedules. Currently running in DEMO_MODE with pre-baked data.' }));

    // Sources
    sec.appendChild(h('div', { class: 'con-sh', text: '6 Discovery Sources' }));
    const srcGrid = h('div', { class: 'con-grid-3' });
    DISCOVERY_SOURCES.forEach(ds => {
      const card = h('div', { class: 'con-card' });
      card.innerHTML = `
        <div class="con-card-title"><span class="dot dot-green"></span>${ds.name}</div>
        <div class="con-card-sub">${ds.type} • ${ds.url}</div>
        <div class="con-card-body">
          Scan interval: <span class="con-badge badge-gold">${ds.schedule}</span>
        </div>`;
      srcGrid.appendChild(card);
    });
    sec.appendChild(srcGrid);

    sec.appendChild(h('hr', { class: 'con-divider' }));

    // Impact scoring
    sec.appendChild(h('div', { class: 'con-sh', text: 'Impact Scoring Algorithm' }));
    const impactCard = h('div', { class: 'arch-ascii' });
    impactCard.innerHTML = `<span class="hl">Impact Level Classification</span>

score >= <span class="gr">85</span>  →  <span style="color:#f87171">CRITICAL</span>
score >= <span class="gr">70</span>  →  <span class="yl">HIGH</span>
score >= <span class="gr">50</span>  →  <span class="bl">MEDIUM</span>
else       →  LOW

<span class="hl">Deterministic Score (demo mode)</span>

hash_val = int(MD5(seed_string).hexdigest(), 16)
score = low + (hash_val % (high - low + 1))
<span class="yl">// Reproducible fake scores: low=30, high=95</span>

<span class="hl">Scanner Coverage</span>

Federal Register:     8 keywords (housing, health, benefits, child welfare, ...)
eCFR:                 Titles 20, 24, 34, 42, 45 (Labor, Housing, Ed, Health, HHS)
State Legislation:    PA, NJ, NY, CA, TX, FL
Academic:             6 research topic queries`;
    sec.appendChild(impactCard);

    sec.appendChild(h('hr', { class: 'con-divider' }));

    // Discovery status flow
    sec.appendChild(h('div', { class: 'con-sh', text: 'Discovery Status Flow' }));
    const discFlow = h('div', { class: 'con-flow' });
    const discStatuses = [
      { label: 'new', color: '#60a5fa' },
      { label: 'reviewed', color: '#fbbf24' },
      { label: 'queued', color: '#a78bfa' },
      { label: 'ingested', color: '#34d399' },
      { label: 'dismissed', color: '#94a3b8' }
    ];
    discStatuses.forEach((s, i) => {
      const step = h('div', { class: 'con-flow-step', style: `background: ${s.color}22; color: ${s.color}; border: 1px solid ${s.color}44` });
      step.textContent = s.label;
      discFlow.appendChild(step);
      if (i < discStatuses.length - 1) {
        const arr = i === 3 ? '' : '→';
        if (arr) discFlow.appendChild(h('span', { class: 'con-flow-arrow', text: arr }));
      }
    });
    sec.appendChild(discFlow);

    sec.appendChild(h('hr', { class: 'con-divider' }));

    // Demo scanner items
    sec.appendChild(h('div', { class: 'con-sh', text: 'Demo Scanner Items' }));
    const demoItems = [
      { source: 'federal_register', title: 'CMS Proposed Rule: Medicaid Eligibility Redeterminations', impact: 'critical', score: 88 },
      { source: 'federal_register', title: 'HUD Final Rule: Housing Choice Voucher Mobility', impact: 'high', score: 76 },
      { source: 'ecfr', title: '42 CFR Part 2 Amendment: SUD Record Sharing Provisions', impact: 'critical', score: 92 },
      { source: 'ecfr', title: '45 CFR §170.315: Health IT Certification Update', impact: 'high', score: 74 },
      { source: 'state_legislation', title: 'PA HB-2847: Cross-Agency Data Sharing Framework', impact: 'high', score: 81 },
      { source: 'state_legislation', title: 'NJ SB-1192: Medicaid Managed Care Transparency Act', impact: 'medium', score: 67 },
      { source: 'academic', title: 'Cross-System Data Integration for Human Services (Semantic Scholar)', impact: 'medium', score: 58 },
      { source: 'academic', title: 'Consent-Based Health Information Exchange Models (JAMIA)', impact: 'high', score: 72 }
    ];

    const demoTable = h('table', { class: 'con-table' });
    demoTable.innerHTML = `
      <thead><tr><th>Source</th><th>Title</th><th>Score</th><th>Impact</th></tr></thead>
      <tbody>
        ${demoItems.map(d => `
          <tr>
            <td class="mono" style="font-size:0.65rem">${d.source}</td>
            <td>${d.title}</td>
            <td class="mono" style="color:#c9a84c">${d.score}</td>
            <td>${d.impact === 'critical'
              ? '<span class="con-badge badge-red">CRITICAL</span>'
              : d.impact === 'high'
                ? '<span class="con-badge badge-yellow">HIGH</span>'
                : '<span class="con-badge badge-blue">MEDIUM</span>'
            }</td>
          </tr>`).join('')}
      </tbody>`;
    sec.appendChild(demoTable);
  })();

  // ═══════════════════════════════════════════════════════════════
  // I. AI LAB TEAMMATES
  // ═══════════════════════════════════════════════════════════════
  (function buildLab() {
    const sec = sections.lab;

    sec.appendChild(h('h2', { class: 'con-stitle', text: 'AI Lab — Teammates & Innovation Engine' }));
    sec.appendChild(h('p', { class: 'con-sdesc', text: '12 AI teammates paired with domain-specific innovation templates. Each teammate generates novel service-delivery innovations scored on impact, feasibility, and novelty.' }));

    // Stats
    const labStats = h('div', { class: 'con-stat-row' });
    [
      { val: '12', label: 'Teammates' },
      { val: '12', label: 'Domains' },
      { val: '8–10', label: 'Templates/Domain' },
      { val: '~110', label: 'Total Templates' },
      { val: '1–5', label: 'Score Scale' },
      { val: '3', label: 'Time Horizons' }
    ].forEach(s => {
      const block = h('div', { class: 'con-stat' });
      block.innerHTML = `<div class="con-stat-val">${s.val}</div><div class="con-stat-label">${s.label}</div>`;
      labStats.appendChild(block);
    });
    sec.appendChild(labStats);

    // Teammates grid
    sec.appendChild(h('div', { class: 'con-sh', text: '12 AI Teammates' }));
    const tmGrid = h('div', { class: 'con-grid-3' });
    TEAMMATES.forEach(tm => {
      const card = h('div', { class: 'con-card' });
      card.innerHTML = `
        <div class="con-card-title">${tm.icon} ${tm.name}</div>
        <div class="con-card-sub">${tm.title} • domain: ${tm.domain}</div>
        <div class="con-card-body">
          <span class="con-badge badge-gold">${tm.slug}</span>
          <span class="con-badge badge-green">active</span>
        </div>`;
      tmGrid.appendChild(card);
    });
    sec.appendChild(tmGrid);

    sec.appendChild(h('hr', { class: 'con-divider' }));

    // Innovation domains
    sec.appendChild(h('div', { class: 'con-sh', text: '12 Innovation Domains' }));
    const domGrid = h('div', { class: 'con-grid-6' });
    INNOVATION_DOMAINS.forEach(d => {
      const card = h('div', { class: 'con-card', style: 'text-align:center;padding:0.6rem' });
      card.innerHTML = `<div class="mono" style="font-size:0.72rem;color:#c9a84c">${d}</div><div style="font-size:0.6rem;color:rgba(245,240,232,0.35);margin-top:2px">8–10 templates</div>`;
      domGrid.appendChild(card);
    });
    sec.appendChild(domGrid);

    sec.appendChild(h('hr', { class: 'con-divider' }));

    // Innovation scoring
    sec.appendChild(h('div', { class: 'con-sh', text: 'Innovation Scoring' }));
    const scoreCard = h('div', { class: 'arch-ascii' });
    scoreCard.innerHTML = `<span class="hl">Innovation Score Dimensions</span> (each 1–5 scale)

  <span class="gr">impact</span>       How significant is the potential change?
  <span class="gr">feasibility</span>   How realistic given current constraints?
  <span class="gr">novelty</span>       How new is this approach?

<span class="hl">Template Structure</span>

{
  "title":             "Innovation title",
  "summary":           "1-2 sentence description",
  "impact_range":      [3, 5],      <span class="yl">// randomized within range</span>
  "feasibility_range": [2, 4],
  "novelty_range":     [3, 5],
  "time_horizons":     ["near", "medium"]
}

<span class="hl">Time Horizons</span>

  <span class="gr">near</span>     0–12 months    implementable now
  <span class="bl">medium</span>   1–3 years      requires preparation
  <span class="yl">far</span>      3+ years       research/experimental

<span class="hl">Generation Flow</span>

POST /api/generate/{slug}
  → select teammate by slug
  → pick domain template
  → randomize scores within template ranges
  → save Innovation + LabSession records`;
    sec.appendChild(scoreCard);

    sec.appendChild(h('hr', { class: 'con-divider' }));

    // Innovation chart
    sec.appendChild(h('div', { class: 'con-sh', text: 'Teammate Domain Coverage' }));
    const chartWrap = h('div', { class: 'con-chart-wrap' });
    const canvas = h('canvas', { id: 'lab-domain-chart' });
    chartWrap.appendChild(canvas);
    sec.appendChild(chartWrap);

    requestAnimationFrame(() => {
      if (typeof Chart === 'undefined') return;
      new Chart(canvas.getContext('2d'), {
        type: 'bar',
        data: {
          labels: TEAMMATES.map(t => t.slug.split('-').map(w => w[0].toUpperCase()).join('')),
          datasets: [{
            label: 'Domain Expertise',
            data: TEAMMATES.map(() => Math.floor(Math.random() * 3) + 8),
            backgroundColor: 'rgba(201,168,76,0.6)',
            borderColor: 'rgba(201,168,76,0.9)',
            borderWidth: 1
          }]
        },
        options: {
          responsive: true,
          plugins: {
            legend: { display: false },
            tooltip: {
              callbacks: {
                title: function(items) { return TEAMMATES[items[0].dataIndex].name; },
                label: function(item) { return TEAMMATES[item.dataIndex].domain + ': ' + item.raw + ' templates'; }
              }
            }
          },
          scales: {
            x: { ticks: { color: 'rgba(245,240,232,0.4)', font: { size: 9, family: 'SF Mono, Consolas, monospace' } }, grid: { display: false } },
            y: { ticks: { color: 'rgba(245,240,232,0.4)', font: { size: 10 } }, grid: { color: 'rgba(201,168,76,0.06)' }, beginAtZero: true }
          }
        }
      });
    });
  })();

  // ═══════════════════════════════════════════════════════════════
  // J. SCRAPE SCHEDULER
  // ═══════════════════════════════════════════════════════════════
  (function buildScraper() {
    const sec = sections.scraper;

    sec.appendChild(h('h2', { class: 'con-stitle', text: 'Scrape Scheduler' }));
    sec.appendChild(h('p', { class: 'con-sdesc', text: '7 data scrapers running on independent intervals, managed by the baths-engine ScrapeScheduler. Data stored in SQLite with scrape history tracking.' }));

    // Scrapers table
    sec.appendChild(h('div', { class: 'con-sh', text: '7 Data Scrapers' }));
    const scTable = h('table', { class: 'con-table' });
    scTable.innerHTML = `
      <thead><tr><th>Scraper</th><th>Data Source</th><th>Interval</th><th>Status</th></tr></thead>
      <tbody>
        ${SCRAPERS.map(s => `
          <tr>
            <td class="mono" style="font-size:0.72rem;color:#c9a84c">${s.name}</td>
            <td>${s.source}</td>
            <td><span class="con-badge badge-gold">${s.interval}</span></td>
            <td><span class="dot dot-green"></span><span style="color:#34d399;font-size:0.72rem">active</span></td>
          </tr>`).join('')}
      </tbody>`;
    sec.appendChild(scTable);

    sec.appendChild(h('hr', { class: 'con-divider' }));

    // Visual timeline
    sec.appendChild(h('div', { class: 'con-sh', text: 'Scrape Timeline (24-hour cycle)' }));
    const tlContainer = h('div', { style: 'margin-bottom:1.5rem' });

    // Build hour markers
    const hourMarkers = h('div', { style: 'display:flex;margin-bottom:0.5rem;padding-left:170px' });
    for (let hr = 0; hr < 24; hr += 3) {
      const marker = h('div', { style: `flex:1;font-size:0.58rem;color:rgba(245,240,232,0.3);font-family:'SF Mono',Consolas,monospace` });
      marker.textContent = String(hr).padStart(2, '0') + ':00';
      hourMarkers.appendChild(marker);
    }
    tlContainer.appendChild(hourMarkers);

    SCRAPERS.forEach(s => {
      const row = h('div', { style: 'display:flex;align-items:center;margin-bottom:0.35rem' });
      const label = h('div', { style: `width:170px;font-size:0.68rem;color:rgba(245,240,232,0.6);font-family:'SF Mono',Consolas,monospace;flex-shrink:0` });
      label.textContent = s.name;
      row.appendChild(label);

      const barContainer = h('div', { style: 'flex:1;height:18px;background:rgba(201,168,76,0.04);border-radius:3px;position:relative;overflow:hidden' });

      // Draw scrape markers
      const maxHrs = 24;
      if (s.intervalHrs <= maxHrs) {
        let t = 0;
        while (t < maxHrs) {
          const pct = (t / maxHrs) * 100;
          const widthPct = Math.max(1, (1 / maxHrs) * 100);
          const tick = h('div', { style: `position:absolute;left:${pct}%;top:0;width:${widthPct}%;height:100%;background:rgba(201,168,76,0.6);border-radius:2px` });
          barContainer.appendChild(tick);
          t += s.intervalHrs;
        }
      } else {
        // Weekly scrapers — show single marker
        const tick = h('div', { style: 'position:absolute;left:0;top:0;width:2%;height:100%;background:rgba(201,168,76,0.4);border-radius:2px' });
        barContainer.appendChild(tick);
      }

      row.appendChild(barContainer);

      const intervalLabel = h('div', { style: `width:40px;text-align:right;font-size:0.62rem;color:#c9a84c;font-family:'SF Mono',Consolas,monospace;margin-left:8px;flex-shrink:0` });
      intervalLabel.textContent = s.interval;
      row.appendChild(intervalLabel);

      tlContainer.appendChild(row);
    });
    sec.appendChild(tlContainer);

    sec.appendChild(h('hr', { class: 'con-divider' }));

    // Scrape run history chart
    sec.appendChild(h('div', { class: 'con-sh', text: 'Scrape Run History' }));
    const chartWrap = h('div', { class: 'con-chart-wrap' });
    const canvas = h('canvas', { id: 'scrape-history-chart' });
    chartWrap.appendChild(canvas);
    sec.appendChild(chartWrap);

    requestAnimationFrame(() => {
      if (typeof Chart === 'undefined') return;

      new Chart(canvas.getContext('2d'), {
        type: 'bar',
        data: {
          labels: ['Run 1', 'Run 2', 'Run 3', 'Run 4', 'Run 5', 'Run 6', 'Run 7'],
          datasets: [
            { label: 'Provisions Added', data: [732, 733, 731, 734, 732, 732, 732], backgroundColor: 'rgba(201,168,76,0.6)', stack: 'stack0' },
            { label: 'Enrichments', data: [0, 684, 688, 689, 881, 976, 980], backgroundColor: 'rgba(96,165,250,0.6)', stack: 'stack0' }
          ]
        },
        options: {
          responsive: true,
          plugins: { legend: { labels: { color: 'rgba(245,240,232,0.6)', font: { size: 11 } } } },
          scales: {
            x: { stacked: true, ticks: { color: 'rgba(245,240,232,0.4)', font: { size: 10 } }, grid: { display: false } },
            y: { stacked: true, ticks: { color: 'rgba(245,240,232,0.4)', font: { size: 10 } }, grid: { color: 'rgba(201,168,76,0.06)' } }
          }
        }
      });
    });

    sec.appendChild(h('hr', { class: 'con-divider' }));

    // Data store API
    sec.appendChild(h('div', { class: 'con-sh', text: 'DataStore API Methods' }));
    const storeCard = h('div', { class: 'arch-ascii' });
    storeCard.innerHTML = `<span class="hl">DataStore (SQLite-backed)</span>

get_provisions(dome_dimension=None, limit=50)  → list
get_costs(category=None, limit=50)             → list
get_systems(domain=None, limit=None)           → list
get_system_links(limit=None)                   → list
get_parcels(neighborhood=None, vacant=None, limit=50) → list
get_enrichments(enrichment_type=None, limit=50) → list
get_scrape_history(engine=None, limit=20)      → list
stats()                                         → dict (all counts)

<span class="hl">Scrape Engine Triggers</span>

POST /api/data/scrape?engine=<span class="gr">legal</span>     → ECFRScraper + FederalRegisterScraper
POST /api/data/scrape?engine=<span class="gr">costs</span>     → CMSScraper + HUDScraper + USASpendingScraper
POST /api/data/scrape?engine=<span class="gr">systems</span>   → SystemsScraper
POST /api/data/scrape?engine=<span class="gr">parcels</span>   → PhillyParcelScraper`;
    sec.appendChild(storeCard);
  })();
};
