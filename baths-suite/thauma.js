/**
 * THAUMA STUDIO — Place-focused product line
 * Activates public spaces using programmable material environments.
 * Interactive canvas + control panel.
 *
 * Renders into container via window.renderThauma(container)
 * All data from window.BATHS_DATA
 */

window.renderThauma = function (container) {
  /* ───────── design tokens ───────── */
  var BG = '#0a0a0f';
  var GOLD = '#c9a84c';
  var TEAL = '#1b4d4d';
  var TEAL_ACCENT = '#2a7a7a';
  var TEAL_GLOW = 'rgba(42,122,122,0.12)';
  var IVORY = '#f5f0e8';
  var IVORY_MUTED = 'rgba(245,240,232,0.5)';
  var IVORY_FAINT = 'rgba(245,240,232,0.25)';
  var CARD_BG = 'rgba(27,77,77,0.06)';
  var CARD_BORDER = 'rgba(42,122,122,0.18)';
  var GOLD_DIM = 'rgba(201,168,76,0.3)';
  var GOLD_GLOW = 'rgba(201,168,76,0.08)';

  var D = window.BATHS_DATA;

  /* ───────── EXTENDED DATA (from audit files) ───────── */

  // Full 14 parcels (from baths-engine/data/parcels.py)
  var parcels = [
    { id: '888000100', address: '1500 Market St, 19102', owner: 'Liberty Property Trust', zoning: 'CMX-5', sqft: 43560, vacant: false, value: 160000000 },
    { id: '888001200', address: '801 Market St, 19107', owner: 'City of Philadelphia', zoning: 'CMX-5', sqft: 65000, vacant: true, value: 18500000 },
    { id: '432100100', address: '2901 N Broad St, 19132', owner: 'Temple University', zoning: 'CMX-3', sqft: 22000, vacant: false, value: 17200000 },
    { id: '432200300', address: '3100 N 22nd St, 19132', owner: 'Philadelphia Land Bank', zoning: 'RSA-5', sqft: 1440, vacant: true, value: 14400 },
    { id: '371130500', address: '2500 Germantown Ave, 19133', owner: 'Private Individual', zoning: 'CMX-2', sqft: 2100, vacant: false, value: 66000 },
    { id: '271040600', address: '5200 Market St, 19139', owner: 'Private LLC', zoning: 'CMX-2.5', sqft: 8500, vacant: false, value: 520000 },
    { id: '271150200', address: '5601 Vine St, 19139', owner: 'Philadelphia Land Bank', zoning: 'RSA-5', sqft: 1200, vacant: true, value: 12000 },
    { id: '021086500', address: '1100 S Broad St, 19146', owner: 'Live Nation Entertainment', zoning: 'SP-STA', sqft: 180000, vacant: false, value: 57000000 },
    { id: '026107300', address: '1400 Passyunk Ave, 19147', owner: 'Private Individual', zoning: 'CMX-2', sqft: 1600, vacant: false, value: 308000 },
    { id: '314010600', address: '2800 Kensington Ave, 19134', owner: 'City of Philadelphia', zoning: 'IRMX', sqft: 45000, vacant: true, value: 450000 },
    { id: '501200100', address: '4700 Wissahickon Ave, 19144', owner: 'Philadelphia Land Bank', zoning: 'RSA-5', sqft: 2800, vacant: true, value: 28000 },
    { id: '883010200', address: '100 N Broad St, 19107', owner: 'City of Philadelphia', zoning: 'CMX-5', sqft: 32000, vacant: false, value: 45000000 },
    { id: '621030400', address: '6100 Cobbs Creek Pkwy, 19143', owner: 'City of Philadelphia', zoning: 'RM-1', sqft: 15000, vacant: true, value: 120000 },
    { id: '772050100', address: '8200 Lindbergh Blvd, 19153', owner: 'City of Philadelphia', zoning: 'I-2', sqft: 95000, vacant: true, value: 380000 }
  ];

  // THAUMA/OS Demo Spaces (from sphere-os frontend demo data)
  var demoSpaces = [
    { id: 'nbc-001', name: 'North Broad Concourse', address: 'N Broad & W Lehigh (below grade)', sqft: 48000, viability: 0.97, notes: 'Founding THAUMA — underground BSL concourse' },
    { id: 'phl-002', name: 'Germantown Rail Yard', address: '100 E Chelten Ave', sqft: 85000, viability: 0.88, notes: 'Brownfield remediated' },
    { id: 'phl-003', name: 'Point Breeze Triangle', address: '1600 S 21st St', sqft: 12000, viability: 0.72, notes: '' },
    { id: 'phl-004', name: 'Kensington Viaduct Lot', address: '2900 Kensington Ave', sqft: 22000, viability: 0.81, notes: '' },
    { id: 'phl-005', name: 'Strawberry Mansion Reservoir', address: '3200 N 33rd St', sqft: 35000, viability: 0.79, notes: '' },
    { id: 'phl-006', name: 'Cobbs Creek Gateway', address: '6300 Market St', sqft: 18000, viability: 0.74, notes: 'Flood zone adjacent' },
    { id: 'phl-007', name: 'Navy Yard East Pad', address: '5100 S Broad St', sqft: 120000, viability: 0.91, notes: 'PIDC; industrial remediated' },
    { id: 'phl-008', name: 'West Philly Innovation Lot', address: '4600 Market St', sqft: 9500, viability: 0.85, notes: 'UCSC owned; 50ft from transit' },
    { id: 'phl-009', name: 'Hunting Park Corner', address: '3700 N Broad St', sqft: 7500, viability: 0.68, notes: 'Philadelphia Land Bank' },
    { id: 'phl-010', name: 'Eastwick Meadow', address: '7400 Lindbergh Blvd', sqft: 280000, viability: 0.65, notes: 'City of Philadelphia' }
  ];

  // Zoning reference (from parcels.py)
  var zoningRef = {
    'CMX-1': { name: 'Neighborhood Commercial Mixed-Use', maxHeight: 38, maxFar: 2.0 },
    'CMX-2': { name: 'Community Commercial Mixed-Use', maxHeight: 38, maxFar: 3.0 },
    'CMX-2.5': { name: 'Community Commercial Mixed-Use (Transit)', maxHeight: 55, maxFar: 3.5 },
    'CMX-3': { name: 'Center City Commercial Mixed-Use', maxHeight: 65, maxFar: 5.0 },
    'CMX-4': { name: 'Center City Commercial Mixed-Use (High-Rise)', maxHeight: 'unlimited', maxFar: 12.0 },
    'CMX-5': { name: 'Center City Core Commercial Mixed-Use', maxHeight: 'unlimited', maxFar: 16.0 },
    'RSA-5': { name: 'Residential Single-Family Attached', maxHeight: 38, maxFar: 2.0 },
    'RM-1': { name: 'Residential Multi-Family (Low)', maxHeight: 38, maxFar: 2.5 },
    'I-1': { name: 'Light Industrial', maxHeight: 45, maxFar: 2.0 },
    'I-2': { name: 'Medium Industrial', maxHeight: 60, maxFar: 3.0 },
    'IRMX': { name: 'Industrial Residential Mixed-Use', maxHeight: 55, maxFar: 3.0 },
    'SP-STA': { name: 'Special Purpose — Stadium', maxHeight: 'varies', maxFar: 'varies' },
    'SP-ENT': { name: 'Special Purpose — Entertainment', maxHeight: 'varies', maxFar: 'varies' }
  };

  // 9 Material system types (from sphere-os/src/materials/drivers/)
  var materialSystems = [
    { id: 'acoustic_metamaterial', name: 'Acoustic Metamaterial', minTime: 0.025, maxTime: 60, color: '#7B68EE', desc: 'Surfaces that redirect, absorb, or amplify sound spatially' },
    { id: 'haptic_surface', name: 'Haptic Surface', minTime: 0.025, maxTime: 5, color: '#FF6B6B', desc: 'Floors and walls with controllable tactile feedback' },
    { id: 'olfactory_synthesis', name: 'Olfactory Synthesis', minTime: 600, maxTime: 1200, color: '#4CAF50', desc: 'Atmospheric chemistry composed by subtracting odor compounds' },
    { id: 'electrochromic_surface', name: 'Electrochromic Surface', minTime: 1, maxTime: 5, color: '#2196F3', desc: 'Transparency, color, and opacity respond to spatial state' },
    { id: 'projection_mapping', name: 'Projection Mapping', minTime: 0.1, maxTime: 10, color: '#FF9800', desc: 'Dynamic visual surfaces on any geometry' },
    { id: 'phase_change_panel', name: 'Phase Change Panel', minTime: 300, maxTime: 1800, color: '#9C27B0', desc: 'Thermal gradient surfaces with controllable warmth zones' },
    { id: 'shape_memory_element', name: 'Shape Memory Element', minTime: 300, maxTime: 3600, color: '#00BCD4', desc: 'Materials that change shape, rigidity, and texture on command' },
    { id: '4d_printed_deployable', name: '4D Printed Deployable', minTime: 1800, maxTime: 3600, color: '#FF5722', desc: 'Structures that self-assemble or change form over time' },
    { id: 'bioluminescent_coating', name: 'Bioluminescent Coating', minTime: 0, maxTime: 0, color: '#76FF03', desc: 'Living light that responds to environmental conditions (always on)' }
  ];

  // Season 1 Episodes — North Broad Concourse (from sphere-os demo data)
  var season1Episodes = [
    { num: 1, title: 'Descent', runtime: 48, desc: 'We enter the concourse for the first time. The space reveals itself through sound and light — 35 feet below Broad Street, a forgotten public infrastructure.', materials: ['acoustic_metamaterial', 'projection_mapping'],
      beats: ['Entrance through stairwell — acoustic metamaterial activates, absorbing city noise', 'First projection maps the history of the BSL onto concourse walls', 'Sound design reveals the 90-second train pulse rhythm', 'Closing: the space breathes for the first time'] },
    { num: 2, title: 'The Nine Senses', runtime: 52, desc: 'Each material system is introduced one by one. The audience experiences touch, temperature, scent, and visual transformation.', materials: ['electrochromic_surface', 'haptic_surface', 'phase_change_panel', 'olfactory_synthesis'],
      beats: ['Electrochromic panels shift from opaque to transparent — revealing hidden chambers', 'Haptic floor activates — visitors feel the vibration of passing trains as designed texture', 'Phase change panels create temperature gradients — warm zones near seating, cool corridors', 'Olfactory system: petrichor scent fades to reveal concrete and steel — THE BOTTLENECK (10-20 min transitions)'] },
    { num: 3, title: 'First Light', runtime: 45, desc: 'The first public performance. 200 people descend into a space that responds to their presence. Five material systems operate in concert.', materials: ['acoustic_metamaterial', 'electrochromic_surface', 'haptic_surface', 'projection_mapping', 'phase_change_panel'],
      beats: ['Audience descends — acoustic system reads crowd density and adjusts reverb', 'Projections respond to movement — generative art from crowd flow data', 'Temperature rises with crowd energy — phase change panels respond', 'Peak moment: all five systems synchronized to music', 'Departure: space slowly returns to baseline as last person exits'] },
    { num: 4, title: 'The Settlement', runtime: 50, desc: 'The space begins generating revenue. Production bookings at $180/hour. The economic model for permanent public infrastructure emerges.', materials: ['acoustic_metamaterial', 'electrochromic_surface', 'projection_mapping', 'haptic_surface', 'shape_memory_element', 'phase_change_panel'],
      beats: ['First paid production booking — a dance company', 'Shape memory elements debut: walls that physically reshape for different uses', 'Revenue model: $180/hr production, $50/hr community, free public hours', 'Conflict: should the space optimize for revenue or access?', 'Resolution: the Chron Score framework — measuring both'] },
    { num: 5, title: 'Permanence', runtime: 50, desc: 'The concourse becomes permanent public infrastructure. All 7 material systems are operational. The CHRON score is calculated and the Chron Bond is issued.', materials: ['acoustic_metamaterial', 'electrochromic_surface', 'haptic_surface', 'projection_mapping', 'phase_change_panel', 'shape_memory_element', 'olfactory_synthesis'],
      beats: ['All 7 systems operational — the space runs itself', 'Community vote: unanimous to make permanent', 'Chron Score calculation on screen', 'Chron Bond issued — investors back the permanence of public space', 'Final scene: the concourse at 3 AM, empty but alive — bioluminescent light growing on the walls'] }
  ];

  // BELOW environmental baseline (from sphere-os demo data)
  var belowBaseline = {
    location: 'N Broad St & W Lehigh Ave — BSL Concourse Level',
    depth: 35,
    area: 48000,
    temperature: { mean: 58, range: 2, unit: '°F' },
    humidity: { mean: 97, range: 6, unit: '%' },
    acoustics: { reverbTime: 7.2, ambientDb: 32, trainPulseDb: 78, trainFrequency: 90 },
    vibration: { baseline: 0.05, trainPeak: 4.2, trainInterval: 90, unit: 'mm/s' },
    airQuality: { pm25: 8.2, co2: 620, radon: 2.1, ventilation: 12000 },
    structural: { ceilingHeight: 14, columnSpacing: 25, floorMaterial: 'Poured concrete (1928)', wallMaterial: 'Glazed tile over reinforced concrete', loadBearing: 250 }
  };

  // Pipeline stages (from SpheresGame.jsx)
  var thaumaPipeline = [
    { key: 'development', label: 'DEVELOPMENT', num: '01', desc: 'Location scouting, rights & permits, development deal', deliverables: ['Active parcel selected', 'Nearby parcels surveyed', 'Zoning analysis', 'Legal barriers identified'] },
    { key: 'pre_production', label: 'PRE-PRODUCTION', num: '02', desc: 'Design board, budget model, timeline', deliverables: ['Activation design', 'Cost model', 'Activation timeline (9-15 months)', 'Material configuration'] },
    { key: 'production', label: 'PRODUCTION', num: '03', desc: 'Build, activate, capture', deliverables: ['Permits executed', 'Materials installed', 'Initial CHRON score', 'First activation captured'] },
    { key: 'post_production', label: 'POST-PRODUCTION', num: '04', desc: 'Measure impact, document episodes, extract IP', deliverables: ['Episode documentation', 'Innovation portfolio', 'Permanence assessment', 'Ripple effect analysis'] },
    { key: 'distribution', label: 'DISTRIBUTION', num: '05', desc: 'CHRON reveal, Chron Bond, replication kit', deliverables: ['Final CHRON score', 'Chron Bond pricing', 'Replication kit', 'Legacy mode designation'] }
  ];

  // Narrative functions for cue sheet
  var narrativeFunctions = ['builds_tension', 'reveals_character', 'marks_time_passage', 'establishes_mood', 'signals_resolution', 'creates_contrast'];

  // Production proposal formats
  var productionFormats = {
    genres: ['sci-fi', 'drama', 'thriller', 'experimental', 'documentary', 'musical', 'comedy'],
    formats: ['feature_film', 'series', 'short', 'installation', 'hybrid'],
    legacyModes: ['living_soundstage', 'public_installation', 'community_space', 'research_lab']
  };

  /* ───────── utilities ───────── */
  function el(tag, cls, html) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (html !== undefined) e.innerHTML = html;
    return e;
  }
  function fmt(n) { return n >= 1000000 ? '$' + (n / 1000000).toFixed(1) + 'M' : n >= 1000 ? '$' + Math.round(n / 1000) + 'K' : '$' + n; }
  function fmtFull(n) { return '$' + n.toLocaleString(); }
  function fmtTime(s) { return s >= 3600 ? (s / 3600).toFixed(1) + 'h' : s >= 60 ? (s / 60).toFixed(0) + 'min' : s.toFixed(2) + 's'; }
  function $$(sel, ctx) { return (ctx || document).querySelectorAll(sel); }

  /* ───────── CHRON Score calculation ───────── */
  function calculateChron(config) {
    var unlock = config.unlock || 0;
    var access = config.access || 0;
    var permanence = config.permanence || 0;
    var catalyst = config.catalyst || 0;
    var policy = config.policy || 0;
    var base = unlock * access;
    var significance = (permanence + catalyst + policy) / 3;
    return base * (1 + significance);
  }

  function chronBondRating(permanence, policy) {
    if (permanence >= 0.8 && policy >= 0.5) return 'AAA';
    if (permanence >= 0.6) return 'AA';
    if (permanence >= 0.4) return 'A';
    return 'BBB';
  }

  /* ───────── state ───────── */
  var currentTab = 'slate';
  var selectedParcel = null;
  var selectedSpace = 'nbc-001';
  var activeMaterials = {};
  var cueSheet = [];
  var chronSliders = { unlock: 48000, access: 8760, permanence: 0.85, catalyst: 0.7, policy: 0.6 };
  var chartInstances = {};
  var canvasInterval = null;

  function destroyCharts() {
    for (var k in chartInstances) {
      if (chartInstances[k] && chartInstances[k].destroy) chartInstances[k].destroy();
    }
    chartInstances = {};
    if (canvasInterval) { clearInterval(canvasInterval); canvasInterval = null; }
  }

  materialSystems.forEach(function (m) { activeMaterials[m.id] = false; });

  /* ═══════════════════════════════════════════════════════════════════
     INJECT STYLES
     ═══════════════════════════════════════════════════════════════════ */
  var style = document.createElement('style');
  style.textContent = [
    '.thauma-root { font-family: system-ui,-apple-system,sans-serif; color:' + IVORY + '; background:' + BG + '; padding:0; min-height:100vh; }',
    '.thauma-header { text-align:center; padding:48px 24px 24px; border-bottom:1px solid ' + CARD_BORDER + '; }',
    '.thauma-header h1 { font-family:Georgia,serif; font-size:42px; color:' + TEAL_ACCENT + '; margin:0 0 8px; letter-spacing:4px; }',
    '.thauma-header p { color:' + IVORY_MUTED + '; font-size:15px; margin:0; }',
    '.thauma-tabs { display:flex; gap:2px; padding:16px 24px; background:rgba(0,0,0,0.3); border-bottom:1px solid ' + CARD_BORDER + '; flex-wrap:wrap; justify-content:center; }',
    '.thauma-tab { padding:10px 18px; border:1px solid transparent; border-radius:6px; cursor:pointer; font-size:13px; color:' + IVORY_MUTED + '; transition:all .2s; letter-spacing:1px; text-transform:uppercase; background:transparent; }',
    '.thauma-tab:hover { color:' + IVORY + '; border-color:' + TEAL + '; }',
    '.thauma-tab.active { color:' + TEAL_ACCENT + '; border-color:' + TEAL_ACCENT + '; background:' + TEAL_GLOW + '; }',
    '.thauma-content { padding:32px 24px; max-width:1400px; margin:0 auto; }',
    '.thauma-card { background:' + CARD_BG + '; border:1px solid ' + CARD_BORDER + '; border-radius:10px; padding:24px; margin-bottom:20px; transition:all .3s; }',
    '.thauma-card:hover { border-color:' + TEAL_ACCENT + '44; }',
    '.thauma-card h3 { font-family:Georgia,serif; color:' + TEAL_ACCENT + '; margin:0 0 12px; font-size:18px; }',
    '.thauma-card h4 { color:' + IVORY + '; margin:0 0 8px; font-size:14px; }',
    '.thauma-card p, .thauma-card li { color:' + IVORY_MUTED + '; font-size:13px; line-height:1.6; }',
    '.thauma-grid { display:grid; gap:20px; }',
    '.thauma-grid-2 { grid-template-columns:repeat(auto-fill,minmax(320px,1fr)); }',
    '.thauma-grid-3 { grid-template-columns:repeat(auto-fill,minmax(260px,1fr)); }',
    '.thauma-grid-4 { grid-template-columns:repeat(auto-fill,minmax(200px,1fr)); }',
    '.thauma-section-title { font-family:Georgia,serif; font-size:24px; color:' + TEAL_ACCENT + '; margin:0 0 24px; padding-bottom:12px; border-bottom:1px solid ' + CARD_BORDER + '; }',
    '.thauma-tag { display:inline-block; background:rgba(42,122,122,0.1); border:1px solid ' + CARD_BORDER + '; color:' + TEAL_ACCENT + '; padding:2px 8px; border-radius:4px; font-size:11px; margin:2px; }',
    '.thauma-tag-gold { background:rgba(201,168,76,0.1); border-color:rgba(201,168,76,0.2); color:' + GOLD + '; }',
    '.thauma-stat { text-align:center; padding:16px; }',
    '.thauma-stat .val { font-size:28px; font-weight:700; color:' + TEAL_ACCENT + '; font-family:Georgia,serif; }',
    '.thauma-stat .lbl { font-size:11px; color:' + IVORY_MUTED + '; text-transform:uppercase; letter-spacing:1px; margin-top:4px; }',
    '.thauma-stats-row { display:flex; gap:12px; flex-wrap:wrap; margin-bottom:24px; }',
    '.thauma-stats-row .thauma-stat { flex:1; min-width:120px; background:' + CARD_BG + '; border:1px solid ' + CARD_BORDER + '; border-radius:8px; }',
    '.thauma-table { width:100%; border-collapse:collapse; font-size:13px; }',
    '.thauma-table th { text-align:left; padding:8px 12px; color:' + TEAL_ACCENT + '; border-bottom:1px solid ' + CARD_BORDER + '; font-weight:600; font-size:11px; text-transform:uppercase; letter-spacing:1px; }',
    '.thauma-table td { padding:8px 12px; border-bottom:1px solid rgba(42,122,122,0.06); color:' + IVORY_MUTED + '; }',
    '.thauma-btn { padding:8px 16px; border:1px solid rgba(42,122,122,0.3); background:transparent; color:' + TEAL_ACCENT + '; border-radius:6px; cursor:pointer; font-size:12px; transition:all .2s; }',
    '.thauma-btn:hover { background:' + TEAL_GLOW + '; border-color:' + TEAL_ACCENT + '; }',
    '.thauma-btn.active { background:' + TEAL_ACCENT + '; color:' + BG + '; }',
    '.thauma-btn-gold { border-color:' + GOLD_DIM + '; color:' + GOLD + '; }',
    '.thauma-btn-gold:hover { background:' + GOLD_GLOW + '; border-color:' + GOLD + '; }',
    '.thauma-btn-gold.active { background:' + GOLD + '; color:' + BG + '; }',
    '.thauma-material-card { cursor:pointer; position:relative; transition:all .3s; }',
    '.thauma-material-card.active { border-color:' + TEAL_ACCENT + '; box-shadow:0 0 20px ' + TEAL_GLOW + '; }',
    '.thauma-material-indicator { width:12px; height:12px; border-radius:50%; position:absolute; top:12px; right:12px; }',
    '.thauma-transition-bar { height:8px; background:rgba(42,122,122,0.1); border-radius:4px; overflow:hidden; margin:8px 0; position:relative; }',
    '.thauma-transition-fill { height:100%; border-radius:4px; position:absolute; }',
    '.thauma-canvas-wrap { border:1px solid ' + CARD_BORDER + '; border-radius:10px; overflow:hidden; background:#050510; position:relative; }',
    '.thauma-canvas-overlay { position:absolute; top:12px; right:12px; background:rgba(0,0,0,0.7); border:1px solid ' + CARD_BORDER + '; border-radius:8px; padding:12px; font-size:11px; min-width:180px; }',
    '.thauma-canvas-overlay .env-row { display:flex; justify-content:space-between; padding:3px 0; }',
    '.thauma-canvas-overlay .env-label { color:' + IVORY_MUTED + '; }',
    '.thauma-canvas-overlay .env-val { color:' + TEAL_ACCENT + '; font-weight:600; }',
    '.thauma-episode-card { position:relative; padding-left:60px; }',
    '.thauma-episode-num { position:absolute; left:0; top:24px; width:44px; height:44px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-family:Georgia,serif; font-size:18px; color:' + IVORY + '; border:2px solid ' + CARD_BORDER + '; }',
    '.thauma-cue-row { display:grid; grid-template-columns:160px 120px 120px 1fr 140px 50px; gap:8px; align-items:center; padding:8px 0; border-bottom:1px solid rgba(42,122,122,0.06); }',
    '.thauma-cue-row select, .thauma-cue-row input { background:rgba(0,0,0,0.3); border:1px solid ' + CARD_BORDER + '; color:' + IVORY + '; padding:6px 8px; border-radius:4px; font-size:12px; }',
    '.thauma-slider-group { margin:16px 0; }',
    '.thauma-slider-group label { display:flex; justify-content:space-between; font-size:12px; color:' + IVORY_MUTED + '; margin-bottom:4px; }',
    '.thauma-slider-group input[type=range] { width:100%; accent-color:' + TEAL_ACCENT + '; }',
    '.thauma-chron-val { font-size:36px; font-family:Georgia,serif; color:' + GOLD + '; text-align:center; margin:20px 0; }',
    '.thauma-pipeline-stage { display:flex; align-items:flex-start; gap:20px; padding:20px; }',
    '.thauma-pipeline-num { font-family:Georgia,serif; font-size:32px; color:' + TEAL + '; min-width:48px; }',
    '.thauma-env-card { padding:16px; }',
    '.thauma-env-reading { display:flex; justify-content:space-between; padding:6px 0; border-bottom:1px solid rgba(42,122,122,0.04); }',
    '.thauma-env-reading:last-child { border-bottom:none; }',
    '@keyframes thauma-fadein { from { opacity:0; transform:translateY(12px); } to { opacity:1; transform:translateY(0); } }',
    '.thauma-animate { animation: thauma-fadein .4s ease both; }',
    '.thauma-vacant-badge { display:inline-block; background:rgba(76,175,80,0.15); color:#4CAF50; padding:2px 8px; border-radius:4px; font-size:10px; font-weight:700; text-transform:uppercase; letter-spacing:1px; }',
    '.thauma-parcel-card { cursor:pointer; }',
    '.thauma-parcel-card.selected { border-color:' + TEAL_ACCENT + '; box-shadow:0 0 16px ' + TEAL_GLOW + '; }',
    '.thauma-chart-container { position:relative; height:300px; margin:16px 0; }',
    '.thauma-remove-btn { background:rgba(244,67,54,0.2); border:1px solid rgba(244,67,54,0.3); color:#f44336; padding:4px 8px; border-radius:4px; cursor:pointer; font-size:11px; }'
  ].join('\n');
  container.innerHTML = '';
  container.appendChild(style);

  /* ═══════════════════════════════════════════════════════════════════
     BUILD SHELL
     ═══════════════════════════════════════════════════════════════════ */
  var root = el('div', 'thauma-root');
  root.innerHTML = [
    '<div class="thauma-header">',
    '  <h1>THAUMA</h1>',
    '  <p>Programmable Material Environment Studio \u2014 Place-Focused Activation \u2014 9 Material Systems</p>',
    '</div>',
    '<div class="thauma-tabs" id="thauma-tabs"></div>',
    '<div class="thauma-content" id="thauma-content"></div>'
  ].join('');
  container.appendChild(root);

  var tabs = [
    { id: 'slate', label: 'The Apollo Slate' },
    { id: 'parcels', label: 'Parcel Explorer' },
    { id: 'materials', label: 'Material Palette' },
    { id: 'canvas', label: 'Canvas Visualization' },
    { id: 'timeline', label: 'Production Timeline' },
    { id: 'episodes', label: 'Episode Browser' },
    { id: 'cuesheet', label: 'Cue Sheet Builder' },
    { id: 'chron', label: 'Chron Score' },
    { id: 'environment', label: 'Environmental Monitor' }
  ];

  var tabBar = root.querySelector('#thauma-tabs');
  tabs.forEach(function (t) {
    var btn = el('button', 'thauma-tab' + (t.id === currentTab ? ' active' : ''), t.label);
    btn.dataset.tab = t.id;
    btn.addEventListener('click', function () {
      currentTab = t.id;
      $$('.thauma-tab', tabBar).forEach(function (b) { b.classList.remove('active'); });
      btn.classList.add('active');
      renderTab();
    });
    tabBar.appendChild(btn);
  });

  function renderTab() {
    destroyCharts();
    var ct = root.querySelector('#thauma-content');
    ct.innerHTML = '';
    switch (currentTab) {
      case 'slate': renderThaumaSlate(ct); break;
      case 'parcels': renderParcels(ct); break;
      case 'materials': renderMaterials(ct); break;
      case 'canvas': renderCanvas(ct); break;
      case 'timeline': renderTimeline(ct); break;
      case 'episodes': renderEpisodes(ct); break;
      case 'cuesheet': renderCueSheet(ct); break;
      case 'chron': renderChron(ct); break;
      case 'environment': renderEnvironment(ct); break;
    }
  }

  /* ═══════════════════════════════════════════════════════════════════
     A. PARCEL EXPLORER
     ═══════════════════════════════════════════════════════════════════ */
  function renderParcels(ct) {
    ct.innerHTML = '<h2 class="thauma-section-title">Parcel Explorer</h2>';
    ct.innerHTML += '<p style="color:' + IVORY_MUTED + ';margin-bottom:24px;">14 real Philadelphia parcels from OPA/Carto data + 10 THAUMA/OS demo spaces with viability scores.</p>';

    // Parcels
    var parcelSect = el('div');
    parcelSect.innerHTML = '<h3 style="font-family:Georgia,serif;color:' + TEAL_ACCENT + ';margin-bottom:16px;">Philadelphia Parcels (14)</h3>';
    var grid = el('div', 'thauma-grid thauma-grid-3');

    parcels.forEach(function (p, i) {
      var card = el('div', 'thauma-card thauma-parcel-card thauma-animate' + (selectedParcel === p.id ? ' selected' : ''));
      card.style.animationDelay = (i * 0.04) + 's';
      var zInfo = zoningRef[p.zoning] || {};
      card.innerHTML = '<div style="display:flex;justify-content:space-between;align-items:flex-start;">' +
        '<h4 style="font-size:13px;">' + p.address + '</h4>' +
        (p.vacant ? '<span class="thauma-vacant-badge">Vacant</span>' : '') +
        '</div>' +
        '<p style="margin:4px 0;"><strong>Owner:</strong> ' + p.owner + '</p>' +
        '<div style="display:flex;gap:8px;flex-wrap:wrap;margin:8px 0;">' +
        '<span class="thauma-tag">' + p.zoning + '</span>' +
        '<span class="thauma-tag">' + p.sqft.toLocaleString() + ' sqft</span>' +
        '<span class="thauma-tag thauma-tag-gold">' + fmt(p.value) + '</span>' +
        '</div>';

      if (selectedParcel === p.id && zInfo.name) {
        card.innerHTML += '<div style="margin-top:12px;padding-top:12px;border-top:1px solid ' + CARD_BORDER + ';">' +
          '<p><strong>Zone:</strong> ' + zInfo.name + '</p>' +
          '<p><strong>Max Height:</strong> ' + (zInfo.maxHeight === 'unlimited' ? 'Unlimited' : zInfo.maxHeight + ' ft') + '</p>' +
          '<p><strong>Max FAR:</strong> ' + (zInfo.maxFar === 'varies' ? 'Varies' : zInfo.maxFar) + '</p></div>';
      }

      card.addEventListener('click', function () { selectedParcel = selectedParcel === p.id ? null : p.id; renderParcels(ct); });
      grid.appendChild(card);
    });
    parcelSect.appendChild(grid);
    ct.appendChild(parcelSect);

    // THAUMA/OS Demo Spaces
    var spaceSect = el('div', '', '');
    spaceSect.style.marginTop = '32px';
    spaceSect.innerHTML = '<h3 style="font-family:Georgia,serif;color:' + TEAL_ACCENT + ';margin-bottom:16px;">THAUMA/OS Demo Spaces (10)</h3>';
    var spaceGrid = el('div', 'thauma-grid thauma-grid-2');

    demoSpaces.forEach(function (s, i) {
      var card = el('div', 'thauma-card thauma-animate');
      card.style.animationDelay = (0.5 + i * 0.04) + 's';
      var viabColor = s.viability >= 0.9 ? '#4CAF50' : s.viability >= 0.75 ? GOLD : '#FF9800';
      card.innerHTML = '<div style="display:flex;justify-content:space-between;align-items:flex-start;">' +
        '<div><h4>' + s.name + '</h4><p style="margin:2px 0;">' + s.address + '</p></div>' +
        '<div style="text-align:center;"><div style="font-family:Georgia,serif;font-size:22px;color:' + viabColor + ';">' + (s.viability * 100).toFixed(0) + '</div><div style="font-size:10px;color:' + IVORY_MUTED + ';">Viability</div></div></div>' +
        '<div style="margin-top:8px;display:flex;gap:8px;">' +
        '<span class="thauma-tag">' + s.sqft.toLocaleString() + ' sqft</span>' +
        '<span class="thauma-tag">' + s.id + '</span>' +
        '</div>' +
        (s.notes ? '<p style="margin-top:8px;font-size:11px;color:' + IVORY_FAINT + ';">' + s.notes + '</p>' : '');
      spaceGrid.appendChild(card);
    });
    spaceSect.appendChild(spaceGrid);
    ct.appendChild(spaceSect);
  }

  /* ═══════════════════════════════════════════════════════════════════
     B. MATERIAL PALETTE
     ═══════════════════════════════════════════════════════════════════ */
  function renderMaterials(ct) {
    ct.innerHTML = '<h2 class="thauma-section-title">Material Palette</h2>';
    ct.innerHTML += '<p style="color:' + IVORY_MUTED + ';margin-bottom:24px;">9 programmable material system types. Toggle materials to build a configuration. Transition times show responsiveness range.</p>';

    var activeCount = Object.keys(activeMaterials).filter(function (k) { return activeMaterials[k]; }).length;
    ct.innerHTML += '<div style="margin-bottom:16px;color:' + GOLD + ';font-size:13px;">' + activeCount + ' of 9 materials active</div>';

    var grid = el('div', 'thauma-grid thauma-grid-3');
    var maxTransition = 3600;

    materialSystems.forEach(function (m, i) {
      var isActive = activeMaterials[m.id];
      var card = el('div', 'thauma-card thauma-material-card thauma-animate' + (isActive ? ' active' : ''));
      card.style.animationDelay = (i * 0.05) + 's';
      card.style.borderLeft = '3px solid ' + m.color;

      var html = '<div class="thauma-material-indicator" style="background:' + (isActive ? '#4CAF50' : 'rgba(255,255,255,0.1)') + ';"></div>';
      html += '<h3 style="color:' + m.color + ';font-size:15px;">' + m.name + '</h3>';
      html += '<p>' + m.desc + '</p>';

      // Transition time bar
      if (m.maxTime > 0) {
        var minPct = Math.max(1, (Math.log(m.minTime + 1) / Math.log(maxTransition + 1)) * 100);
        var maxPct = Math.max(minPct + 2, (Math.log(m.maxTime + 1) / Math.log(maxTransition + 1)) * 100);
        html += '<div style="margin-top:12px;">';
        html += '<div style="display:flex;justify-content:space-between;font-size:10px;color:' + IVORY_FAINT + ';"><span>' + fmtTime(m.minTime) + '</span><span>Transition Time</span><span>' + fmtTime(m.maxTime) + '</span></div>';
        html += '<div class="thauma-transition-bar">';
        html += '<div class="thauma-transition-fill" style="left:' + minPct + '%;width:' + (maxPct - minPct) + '%;background:' + m.color + ';opacity:0.7;"></div>';
        html += '</div></div>';
      } else {
        html += '<div style="margin-top:12px;font-size:11px;color:' + m.color + ';">Always on \u2014 no transition time</div>';
      }

      card.innerHTML = html;
      card.addEventListener('click', function () { activeMaterials[m.id] = !activeMaterials[m.id]; renderMaterials(ct); });
      grid.appendChild(card);
    });
    ct.appendChild(grid);

    // Active configuration summary
    if (activeCount > 0) {
      var summary = el('div', 'thauma-card thauma-animate');
      summary.style.animationDelay = '0.5s';
      summary.innerHTML = '<h3 style="color:' + GOLD + ';">Active Configuration</h3>';
      var activeSys = materialSystems.filter(function (m) { return activeMaterials[m.id]; });
      summary.innerHTML += '<div style="display:flex;gap:8px;flex-wrap:wrap;">';
      activeSys.forEach(function (m) {
        summary.innerHTML += '<span class="thauma-tag" style="background:' + m.color + '22;border-color:' + m.color + '44;color:' + m.color + ';">' + m.name + '</span>';
      });
      summary.innerHTML += '</div>';
      var slowest = Math.max.apply(null, activeSys.map(function (m) { return m.maxTime; }));
      summary.innerHTML += '<p style="margin-top:12px;">Slowest transition: <strong style="color:' + TEAL_ACCENT + ';">' + fmtTime(slowest) + '</strong> (bottleneck: ' + activeSys.filter(function (m) { return m.maxTime === slowest; }).map(function (m) { return m.name; }).join(', ') + ')</p>';
      ct.appendChild(summary);
    }
  }

  /* ═══════════════════════════════════════════════════════════════════
     C. CANVAS VISUALIZATION
     ═══════════════════════════════════════════════════════════════════ */
  function renderCanvas(ct) {
    ct.innerHTML = '<h2 class="thauma-section-title">Canvas Visualization</h2>';

    var canvasWrap = el('div', 'thauma-canvas-wrap');
    canvasWrap.style.height = '500px';
    canvasWrap.style.position = 'relative';

    var cvs = document.createElement('canvas');
    cvs.id = 'thauma-canvas';
    cvs.style.width = '100%';
    cvs.style.height = '100%';
    canvasWrap.appendChild(cvs);

    // Environment overlay
    var overlay = el('div', 'thauma-canvas-overlay');
    overlay.innerHTML = '<div style="color:' + TEAL_ACCENT + ';font-weight:700;margin-bottom:8px;font-size:12px;">BELOW Readings</div>' +
      '<div class="env-row"><span class="env-label">Temperature</span><span class="env-val" id="env-temp">' + belowBaseline.temperature.mean + '°F</span></div>' +
      '<div class="env-row"><span class="env-label">Humidity</span><span class="env-val" id="env-humid">' + belowBaseline.humidity.mean + '%</span></div>' +
      '<div class="env-row"><span class="env-label">Reverb</span><span class="env-val" id="env-reverb">' + belowBaseline.acoustics.reverbTime + 's</span></div>' +
      '<div class="env-row"><span class="env-label">Ambient</span><span class="env-val">' + belowBaseline.acoustics.ambientDb + ' dB</span></div>' +
      '<div class="env-row"><span class="env-label">Vibration</span><span class="env-val" id="env-vib">' + belowBaseline.vibration.baseline + ' mm/s</span></div>' +
      '<div class="env-row"><span class="env-label">PM2.5</span><span class="env-val">' + belowBaseline.airQuality.pm25 + ' µg/m³</span></div>';
    canvasWrap.appendChild(overlay);
    ct.appendChild(canvasWrap);

    // Material toggles below canvas
    var toggleRow = el('div', '', '');
    toggleRow.style.cssText = 'display:flex;gap:6px;flex-wrap:wrap;margin-top:16px;';
    materialSystems.forEach(function (m) {
      var btn = el('button', 'thauma-btn' + (activeMaterials[m.id] ? ' active' : ''));
      btn.style.borderColor = m.color + '66';
      if (activeMaterials[m.id]) btn.style.background = m.color + '33';
      btn.textContent = m.name.replace(/_/g, ' ');
      btn.addEventListener('click', function () {
        activeMaterials[m.id] = !activeMaterials[m.id];
        renderCanvas(ct);
      });
      toggleRow.appendChild(btn);
    });
    ct.appendChild(toggleRow);

    // Draw canvas
    setTimeout(function () { drawThaumaCanvas(cvs); }, 50);
  }

  function drawThaumaCanvas(cvs) {
    var rect = cvs.parentElement.getBoundingClientRect();
    cvs.width = rect.width * (window.devicePixelRatio || 1);
    cvs.height = rect.height * (window.devicePixelRatio || 1);
    cvs.style.width = rect.width + 'px';
    cvs.style.height = rect.height + 'px';
    var ctx = cvs.getContext('2d');
    var dpr = window.devicePixelRatio || 1;
    ctx.scale(dpr, dpr);
    var W = rect.width;
    var H = rect.height;

    // Floor plan grid based on sqft (North Broad Concourse = 48000 sqft)
    var sqft = 48000;
    var cols = Math.ceil(Math.sqrt(sqft / 100));
    var rows = Math.ceil(sqft / 100 / cols);
    var cellW = (W - 80) / cols;
    var cellH = (H - 80) / rows;
    var offsetX = 40;
    var offsetY = 40;

    // Particles for active materials
    var particles = [];
    var activeSys = materialSystems.filter(function (m) { return activeMaterials[m.id]; });

    function initParticles() {
      particles = [];
      activeSys.forEach(function (m) {
        for (var i = 0; i < 30; i++) {
          particles.push({
            x: offsetX + Math.random() * (W - 80),
            y: offsetY + Math.random() * (H - 80),
            vx: (Math.random() - 0.5) * 1.5,
            vy: (Math.random() - 0.5) * 1.5,
            r: 2 + Math.random() * 4,
            color: m.color,
            alpha: 0.3 + Math.random() * 0.5,
            material: m.id
          });
        }
      });
    }

    initParticles();
    var trainPhase = 0;

    function draw() {
      ctx.clearRect(0, 0, W, H);

      // Background
      ctx.fillStyle = '#050510';
      ctx.fillRect(0, 0, W, H);

      // Grid
      ctx.strokeStyle = 'rgba(42,122,122,0.08)';
      ctx.lineWidth = 0.5;
      for (var r = 0; r <= rows; r++) {
        ctx.beginPath();
        ctx.moveTo(offsetX, offsetY + r * cellH);
        ctx.lineTo(offsetX + cols * cellW, offsetY + r * cellH);
        ctx.stroke();
      }
      for (var c = 0; c <= cols; c++) {
        ctx.beginPath();
        ctx.moveTo(offsetX + c * cellW, offsetY);
        ctx.lineTo(offsetX + c * cellW, offsetY + rows * cellH);
        ctx.stroke();
      }

      // Columns (column spacing = 25ft, approximate)
      ctx.fillStyle = 'rgba(42,122,122,0.12)';
      var colSpacing = cellW * 3;
      for (var cx = offsetX + colSpacing; cx < offsetX + cols * cellW; cx += colSpacing) {
        for (var cy = offsetY + colSpacing; cy < offsetY + rows * cellH; cy += colSpacing) {
          ctx.beginPath();
          ctx.arc(cx, cy, 4, 0, Math.PI * 2);
          ctx.fill();
        }
      }

      // Train pulse simulation
      trainPhase = (trainPhase + 0.02) % (Math.PI * 2);
      var trainPulse = Math.sin(trainPhase);
      if (trainPulse > 0.8) {
        ctx.fillStyle = 'rgba(255,100,100,' + (trainPulse - 0.8) * 2 + ')';
        ctx.fillRect(0, H - 4, W, 4);
        // Update vibration reading
        var vibEl = document.getElementById('env-vib');
        if (vibEl) vibEl.textContent = (belowBaseline.vibration.baseline + trainPulse * belowBaseline.vibration.trainPeak).toFixed(2) + ' mm/s';
      }

      // Active material overlays
      if (activeMaterials['projection_mapping']) {
        // Animated grid glow
        var t = Date.now() / 2000;
        for (var gr = 0; gr < rows; gr++) {
          for (var gc = 0; gc < cols; gc++) {
            var val = Math.sin(gr * 0.3 + t) * Math.cos(gc * 0.4 + t * 0.7) * 0.5 + 0.5;
            if (val > 0.7) {
              ctx.fillStyle = 'rgba(255,152,0,' + (val * 0.12) + ')';
              ctx.fillRect(offsetX + gc * cellW + 1, offsetY + gr * cellH + 1, cellW - 2, cellH - 2);
            }
          }
        }
      }

      if (activeMaterials['electrochromic_surface']) {
        var ePhase = Date.now() / 5000;
        for (var er = 0; er < rows; er += 3) {
          var alpha = Math.sin(er * 0.5 + ePhase) * 0.5 + 0.5;
          ctx.fillStyle = 'rgba(33,150,243,' + (alpha * 0.08) + ')';
          ctx.fillRect(offsetX, offsetY + er * cellH, cols * cellW, cellH * 3);
        }
      }

      if (activeMaterials['phase_change_panel']) {
        // Warm zones
        var gradient = ctx.createRadialGradient(W * 0.3, H * 0.5, 20, W * 0.3, H * 0.5, 150);
        gradient.addColorStop(0, 'rgba(156,39,176,0.1)');
        gradient.addColorStop(1, 'rgba(156,39,176,0)');
        ctx.fillStyle = gradient;
        ctx.fillRect(0, 0, W, H);
        var gradient2 = ctx.createRadialGradient(W * 0.7, H * 0.4, 20, W * 0.7, H * 0.4, 120);
        gradient2.addColorStop(0, 'rgba(156,39,176,0.08)');
        gradient2.addColorStop(1, 'rgba(156,39,176,0)');
        ctx.fillStyle = gradient2;
        ctx.fillRect(0, 0, W, H);
      }

      if (activeMaterials['acoustic_metamaterial']) {
        // Ripples
        var aPhase = Date.now() / 1000;
        ctx.strokeStyle = 'rgba(123,104,238,0.15)';
        ctx.lineWidth = 1;
        for (var ri = 0; ri < 3; ri++) {
          var radius = ((aPhase + ri * 2) % 6) * 40;
          ctx.beginPath();
          ctx.arc(W * 0.5, H * 0.5, radius, 0, Math.PI * 2);
          ctx.stroke();
        }
      }

      if (activeMaterials['bioluminescent_coating']) {
        // Gentle green glow at edges
        ctx.fillStyle = 'rgba(118,255,3,0.03)';
        ctx.fillRect(offsetX, offsetY, cols * cellW, 3);
        ctx.fillRect(offsetX, offsetY + rows * cellH - 3, cols * cellW, 3);
        ctx.fillRect(offsetX, offsetY, 3, rows * cellH);
        ctx.fillRect(offsetX + cols * cellW - 3, offsetY, 3, rows * cellH);
      }

      // Particles
      particles.forEach(function (p) {
        p.x += p.vx;
        p.y += p.vy;
        if (p.x < offsetX || p.x > offsetX + cols * cellW) p.vx *= -1;
        if (p.y < offsetY || p.y > offsetY + rows * cellH) p.vy *= -1;
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
        ctx.fillStyle = p.color + Math.round(p.alpha * 255).toString(16).padStart(2, '0');
        ctx.fill();
      });

      // Label
      ctx.font = '10px system-ui';
      ctx.fillStyle = 'rgba(42,122,122,0.3)';
      ctx.fillText('North Broad Concourse \u2014 48,000 sqft \u2014 35ft below grade', offsetX, H - 12);
    }

    draw();
    canvasInterval = setInterval(draw, 50);
  }

  /* ═══════════════════════════════════════════════════════════════════
     D. PRODUCTION TIMELINE
     ═══════════════════════════════════════════════════════════════════ */
  function renderTimeline(ct) {
    ct.innerHTML = '<h2 class="thauma-section-title">Production Timeline</h2>';
    ct.innerHTML += '<p style="color:' + IVORY_MUTED + ';margin-bottom:24px;">5-stage THAUMA production pipeline from location scouting to Chron Bond issuance.</p>';

    thaumaPipeline.forEach(function (stage, i) {
      var card = el('div', 'thauma-card thauma-animate');
      card.style.animationDelay = (i * 0.1) + 's';
      card.innerHTML = '<div class="thauma-pipeline-stage">' +
        '<div class="thauma-pipeline-num">' + stage.num + '</div>' +
        '<div style="flex:1;"><h3 style="margin-bottom:4px;">' + stage.label + '</h3>' +
        '<p>' + stage.desc + '</p>' +
        '<div style="margin-top:12px;"><strong style="color:' + IVORY + ';font-size:12px;">Deliverables:</strong></div>' +
        '<div style="margin-top:4px;">' + stage.deliverables.map(function (d) { return '<span class="thauma-tag">' + d + '</span>'; }).join('') + '</div>' +
        '</div></div>';
      ct.appendChild(card);
    });
  }

  /* ═══════════════════════════════════════════════════════════════════
     E. EPISODE BROWSER
     ═══════════════════════════════════════════════════════════════════ */
  function renderEpisodes(ct) {
    ct.innerHTML = '<h2 class="thauma-section-title">Episode Browser</h2>';
    ct.innerHTML += '<p style="color:' + IVORY_MUTED + ';margin-bottom:8px;">Season 1: "The North Broad Concourse" \u2014 5 episodes \u2014 245 minutes total</p>';
    ct.innerHTML += '<p style="color:' + IVORY_FAINT + ';margin-bottom:24px;font-style:italic;">"What happens when a city decides to remember what it buried?"</p>';

    season1Episodes.forEach(function (ep, i) {
      var card = el('div', 'thauma-card thauma-episode-card thauma-animate');
      card.style.animationDelay = (i * 0.1) + 's';
      var epColor = materialSystems.find(function (m) { return m.id === ep.materials[0]; });
      var color = epColor ? epColor.color : TEAL_ACCENT;

      card.innerHTML = '<div class="thauma-episode-num" style="border-color:' + color + ';color:' + color + ';">' + ep.num + '</div>';
      card.innerHTML += '<h3 style="color:' + color + ';">' + ep.title + '</h3>';
      card.innerHTML += '<p style="margin-bottom:8px;"><strong>' + ep.runtime + ' min</strong></p>';
      card.innerHTML += '<p>' + ep.desc + '</p>';

      // Materials used
      card.innerHTML += '<div style="margin-top:12px;"><strong style="color:' + IVORY + ';font-size:11px;">Material Systems:</strong> ';
      card.innerHTML += ep.materials.map(function (mid) {
        var ms = materialSystems.find(function (m) { return m.id === mid; });
        return '<span class="thauma-tag" style="background:' + (ms ? ms.color : TEAL) + '22;border-color:' + (ms ? ms.color : TEAL) + '44;color:' + (ms ? ms.color : TEAL_ACCENT) + ';">' + (ms ? ms.name : mid) + '</span>';
      }).join('');
      card.innerHTML += '</div>';

      // Narrative beats
      card.innerHTML += '<div style="margin-top:16px;padding-top:12px;border-top:1px solid ' + CARD_BORDER + ';">';
      card.innerHTML += '<strong style="color:' + IVORY + ';font-size:11px;text-transform:uppercase;letter-spacing:1px;">Narrative Beats</strong>';
      card.innerHTML += '<ol style="margin:8px 0 0;padding-left:20px;">';
      ep.beats.forEach(function (beat) {
        card.innerHTML += '<li style="margin:6px 0;">' + beat + '</li>';
      });
      card.innerHTML += '</ol></div>';

      ct.appendChild(card);
    });
  }

  /* ═══════════════════════════════════════════════════════════════════
     F. CUE SHEET BUILDER
     ═══════════════════════════════════════════════════════════════════ */
  function renderCueSheet(ct) {
    ct.innerHTML = '<h2 class="thauma-section-title">Cue Sheet Builder</h2>';
    ct.innerHTML += '<p style="color:' + IVORY_MUTED + ';margin-bottom:24px;">Build material cues for a THAUMA production. Each cue specifies a material system, timestamp, target property, and narrative function.</p>';

    // Cue table
    var cueTable = el('div', 'thauma-card');
    cueTable.innerHTML = '<h3>Material Cues</h3>';

    // Header
    cueTable.innerHTML += '<div class="thauma-cue-row" style="border-bottom:1px solid ' + CARD_BORDER + ';font-size:11px;color:' + TEAL_ACCENT + ';text-transform:uppercase;letter-spacing:1px;">' +
      '<div>Material System</div><div>Start (s)</div><div>End (s)</div><div>Target Property</div><div>Narrative Function</div><div></div></div>';

    // Existing cues
    cueSheet.forEach(function (cue, idx) {
      var row = el('div', 'thauma-cue-row');
      row.innerHTML = '<div style="color:' + IVORY + ';">' + (materialSystems.find(function (m) { return m.id === cue.material; }) || {}).name + '</div>' +
        '<div>' + cue.start + '</div>' +
        '<div>' + cue.end + '</div>' +
        '<div>' + cue.property + '</div>' +
        '<div><span class="thauma-tag">' + cue.narrative.replace(/_/g, ' ') + '</span></div>' +
        '<div><button class="thauma-remove-btn" data-idx="' + idx + '">\u00d7</button></div>';
      cueTable.appendChild(row);
    });

    // Add cue row
    var addRow = el('div', 'thauma-cue-row');
    addRow.style.paddingTop = '12px';
    addRow.style.borderTop = '1px solid ' + CARD_BORDER;

    var matSel = '<select id="cue-mat">' + materialSystems.map(function (m) { return '<option value="' + m.id + '">' + m.name + '</option>'; }).join('') + '</select>';
    var narSel = '<select id="cue-nar">' + narrativeFunctions.map(function (n) { return '<option value="' + n + '">' + n.replace(/_/g, ' ') + '</option>'; }).join('') + '</select>';

    addRow.innerHTML = matSel +
      '<input id="cue-start" type="number" value="0" min="0" placeholder="Start">' +
      '<input id="cue-end" type="number" value="60" min="0" placeholder="End">' +
      '<input id="cue-prop" type="text" placeholder="e.g. reverb_time_s" style="width:100%;">' +
      narSel +
      '<button class="thauma-btn" id="cue-add" style="padding:6px 12px;">+</button>';
    cueTable.appendChild(addRow);
    ct.appendChild(cueTable);

    // Event handlers
    setTimeout(function () {
      var addBtn = document.getElementById('cue-add');
      if (addBtn) {
        addBtn.addEventListener('click', function () {
          cueSheet.push({
            material: document.getElementById('cue-mat').value,
            start: parseFloat(document.getElementById('cue-start').value) || 0,
            end: parseFloat(document.getElementById('cue-end').value) || 60,
            property: document.getElementById('cue-prop').value || 'default',
            narrative: document.getElementById('cue-nar').value
          });
          renderCueSheet(ct);
        });
      }
      $$('.thauma-remove-btn', ct).forEach(function (btn) {
        btn.addEventListener('click', function () {
          cueSheet.splice(parseInt(btn.dataset.idx), 1);
          renderCueSheet(ct);
        });
      });
    }, 50);

    // Production proposal format options
    var formatCard = el('div', 'thauma-card thauma-animate');
    formatCard.style.animationDelay = '0.2s';
    formatCard.innerHTML = '<h3>Production Proposal Options</h3>';
    formatCard.innerHTML += '<div style="display:flex;gap:24px;flex-wrap:wrap;">';
    formatCard.innerHTML += '<div><strong style="color:' + IVORY + ';font-size:11px;">Genre</strong><br>' + productionFormats.genres.map(function (g) { return '<span class="thauma-tag">' + g + '</span>'; }).join('') + '</div>';
    formatCard.innerHTML += '<div><strong style="color:' + IVORY + ';font-size:11px;">Format</strong><br>' + productionFormats.formats.map(function (f) { return '<span class="thauma-tag">' + f.replace(/_/g, ' ') + '</span>'; }).join('') + '</div>';
    formatCard.innerHTML += '<div><strong style="color:' + IVORY + ';font-size:11px;">Legacy Modes</strong><br>' + productionFormats.legacyModes.map(function (l) { return '<span class="thauma-tag thauma-tag-gold">' + l.replace(/_/g, ' ') + '</span>'; }).join('') + '</div>';
    formatCard.innerHTML += '</div>';
    ct.appendChild(formatCard);
  }

  /* ═══════════════════════════════════════════════════════════════════
     G. CHRON SCORE DISPLAY
     ═══════════════════════════════════════════════════════════════════ */
  function renderChron(ct) {
    ct.innerHTML = '<h2 class="thauma-section-title">Chron Score Display</h2>';
    ct.innerHTML += '<p style="color:' + IVORY_MUTED + ';margin-bottom:24px;">Formula: (unlock \u00d7 access) \u00d7 (1 + (permanence + catalyst + policy) / 3). Interactive sliders to explore configurations.</p>';

    var chronScore = calculateChron(chronSliders);

    // Score display
    var scoreCard = el('div', 'thauma-card');
    scoreCard.innerHTML = '<div class="thauma-chron-val" id="chron-display">' + chronScore.toLocaleString(undefined, { maximumFractionDigits: 0 }) + '</div>';
    scoreCard.innerHTML += '<div style="text-align:center;color:' + IVORY_MUTED + ';font-size:12px;">CHRON Score = (m\u00b2 \u00d7 hours) \u00d7 (1 + significance)</div>';
    ct.appendChild(scoreCard);

    // Sliders
    var sliderCard = el('div', 'thauma-card');
    sliderCard.innerHTML = '<h3>CHRON Dimensions</h3>';

    var sliderDefs = [
      { key: 'unlock', label: 'Unlock (sqft)', min: 0, max: 280000, step: 1000 },
      { key: 'access', label: 'Access (hours/year)', min: 0, max: 8760, step: 100 },
      { key: 'permanence', label: 'Permanence', min: 0, max: 1, step: 0.05 },
      { key: 'catalyst', label: 'Catalyst (ripple effects)', min: 0, max: 1, step: 0.05 },
      { key: 'policy', label: 'Policy (changes unlocked)', min: 0, max: 1, step: 0.05 }
    ];

    sliderDefs.forEach(function (sd) {
      var group = el('div', 'thauma-slider-group');
      group.innerHTML = '<label><span>' + sd.label + '</span><span id="slider-val-' + sd.key + '" style="color:' + TEAL_ACCENT + ';font-weight:600;">' + chronSliders[sd.key] + '</span></label>' +
        '<input type="range" id="slider-' + sd.key + '" min="' + sd.min + '" max="' + sd.max + '" step="' + sd.step + '" value="' + chronSliders[sd.key] + '">';
      sliderCard.appendChild(group);
    });
    ct.appendChild(sliderCard);

    // Chron Bond pricing
    var rating = chronBondRating(chronSliders.permanence, chronSliders.policy);
    var bondCard = el('div', 'thauma-card thauma-animate');
    bondCard.style.animationDelay = '0.2s';
    var ratingColor = rating === 'AAA' ? '#4CAF50' : rating === 'AA' ? '#2196F3' : rating === 'A' ? GOLD : '#FF9800';
    bondCard.innerHTML = '<h3>Chron Bond Pricing</h3>' +
      '<div class="thauma-stats-row">' +
      '<div class="thauma-stat"><div class="val" style="color:' + ratingColor + ';">' + rating + '</div><div class="lbl">Bond Rating</div></div>' +
      '<div class="thauma-stat"><div class="val">' + chronScore.toLocaleString(undefined, { maximumFractionDigits: 0 }) + '</div><div class="lbl">Face Value (economic impact)</div></div>' +
      '<div class="thauma-stat"><div class="val">' + chronSliders.unlock.toLocaleString() + '</div><div class="lbl">SqFt Backing</div></div>' +
      '</div>' +
      '<table class="thauma-table"><thead><tr><th>Rating</th><th>Permanence</th><th>Policy</th></tr></thead><tbody>' +
      '<tr><td style="color:#4CAF50;">AAA</td><td>\u2265 0.8</td><td>\u2265 0.5</td></tr>' +
      '<tr><td style="color:#2196F3;">AA</td><td>\u2265 0.6</td><td>any</td></tr>' +
      '<tr><td style="color:' + GOLD + ';">A</td><td>\u2265 0.4</td><td>any</td></tr>' +
      '<tr><td style="color:#FF9800;">BBB</td><td>< 0.4</td><td>any</td></tr>' +
      '</tbody></table>';
    ct.appendChild(bondCard);

    // Slider event handlers
    setTimeout(function () {
      sliderDefs.forEach(function (sd) {
        var slider = document.getElementById('slider-' + sd.key);
        if (slider) {
          slider.addEventListener('input', function () {
            chronSliders[sd.key] = parseFloat(slider.value);
            var valEl = document.getElementById('slider-val-' + sd.key);
            if (valEl) valEl.textContent = slider.value;
            var score = calculateChron(chronSliders);
            var display = document.getElementById('chron-display');
            if (display) display.textContent = score.toLocaleString(undefined, { maximumFractionDigits: 0 });
          });
        }
      });
    }, 50);
  }

  /* ═══════════════════════════════════════════════════════════════════
     H. ENVIRONMENTAL MONITOR
     ═══════════════════════════════════════════════════════════════════ */
  function renderEnvironment(ct) {
    ct.innerHTML = '<h2 class="thauma-section-title">Environmental Monitor</h2>';
    ct.innerHTML += '<p style="color:' + IVORY_MUTED + ';margin-bottom:24px;">BELOW baseline environmental data for the North Broad Concourse — 35 ft below Broad Street.</p>';

    var b = belowBaseline;

    // Location header
    var locCard = el('div', 'thauma-card');
    locCard.innerHTML = '<h3>' + b.location + '</h3>' +
      '<div class="thauma-stats-row">' +
      '<div class="thauma-stat"><div class="val">' + b.depth + '</div><div class="lbl">Depth (ft)</div></div>' +
      '<div class="thauma-stat"><div class="val">' + b.area.toLocaleString() + '</div><div class="lbl">Area (sqft)</div></div>' +
      '<div class="thauma-stat"><div class="val">' + b.structural.ceilingHeight + '</div><div class="lbl">Ceiling (ft)</div></div>' +
      '<div class="thauma-stat"><div class="val">' + b.structural.columnSpacing + '</div><div class="lbl">Column Spacing (ft)</div></div>' +
      '</div>';
    ct.appendChild(locCard);

    // Environmental readings
    var envSections = [
      { title: 'Temperature', readings: [
        ['Mean Temperature', b.temperature.mean + ' ' + b.temperature.unit],
        ['Range', '\u00b1' + b.temperature.range + b.temperature.unit],
        ['Thermal Source', 'Underground thermal mass']
      ]},
      { title: 'Humidity', readings: [
        ['Mean Humidity', b.humidity.mean + b.humidity.unit],
        ['Range', '\u00b1' + b.humidity.range + b.humidity.unit],
        ['Source', 'Groundwater seepage']
      ]},
      { title: 'Acoustics', readings: [
        ['Reverb Time', b.acoustics.reverbTime + 's'],
        ['Ambient Level', b.acoustics.ambientDb + ' dB'],
        ['Train Pulse', b.acoustics.trainPulseDb + ' dB'],
        ['Train Frequency', 'Every ' + b.acoustics.trainFrequency + 's (BSL N/S — Lehigh Station)']
      ]},
      { title: 'Vibration', readings: [
        ['Baseline', b.vibration.baseline + ' ' + b.vibration.unit],
        ['Train Peak', b.vibration.trainPeak + ' ' + b.vibration.unit],
        ['Train Interval', b.vibration.trainInterval + 's']
      ]},
      { title: 'Air Quality', readings: [
        ['PM2.5', b.airQuality.pm25 + ' \u00b5g/m\u00b3'],
        ['CO\u2082', b.airQuality.co2 + ' ppm'],
        ['Radon', b.airQuality.radon + ' pCi/L'],
        ['Ventilation', b.airQuality.ventilation.toLocaleString() + ' CFM']
      ]},
      { title: 'Structural', readings: [
        ['Ceiling Height', b.structural.ceilingHeight + ' ft'],
        ['Column Spacing', b.structural.columnSpacing + ' ft'],
        ['Floor Material', b.structural.floorMaterial],
        ['Wall Material', b.structural.wallMaterial],
        ['Load Bearing', b.structural.loadBearing + ' PSF']
      ]}
    ];

    var grid = el('div', 'thauma-grid thauma-grid-2');
    envSections.forEach(function (sec, i) {
      var card = el('div', 'thauma-card thauma-env-card thauma-animate');
      card.style.animationDelay = (i * 0.08) + 's';
      card.innerHTML = '<h3>' + sec.title + '</h3>';
      sec.readings.forEach(function (r) {
        card.innerHTML += '<div class="thauma-env-reading">' +
          '<span style="color:' + IVORY_MUTED + ';">' + r[0] + '</span>' +
          '<span style="color:' + TEAL_ACCENT + ';font-weight:600;">' + r[1] + '</span></div>';
      });
      grid.appendChild(card);
    });
    ct.appendChild(grid);

    // Chart — environmental readings visualization
    var chartCard = el('div', 'thauma-card thauma-animate');
    chartCard.style.animationDelay = '0.5s';
    chartCard.innerHTML = '<h3>Environmental Profile</h3>';
    var chartWrap = el('div', 'thauma-chart-container');
    var canvas = document.createElement('canvas');
    chartWrap.appendChild(canvas);
    chartCard.appendChild(chartWrap);
    ct.appendChild(chartCard);

    setTimeout(function () {
      if (typeof Chart === 'undefined') return;
      chartInstances.envChart = new Chart(canvas, {
        type: 'bar',
        data: {
          labels: ['Temp (\u00b0F)', 'Humidity (%)', 'Reverb (s\u00d710)', 'Ambient (dB)', 'Train (dB)', 'PM2.5', 'CO\u2082/100', 'Load (PSF/10)'],
          datasets: [{
            label: 'BELOW Readings',
            data: [b.temperature.mean, b.humidity.mean, b.acoustics.reverbTime * 10, b.acoustics.ambientDb, b.acoustics.trainPulseDb, b.airQuality.pm25, b.airQuality.co2 / 100, b.structural.loadBearing / 10],
            backgroundColor: [
              'rgba(255,152,0,0.5)', 'rgba(33,150,243,0.5)', 'rgba(123,104,238,0.5)', 'rgba(156,39,176,0.5)',
              'rgba(244,67,54,0.5)', 'rgba(76,175,80,0.5)', 'rgba(255,235,59,0.5)', 'rgba(42,122,122,0.5)'
            ],
            borderColor: [
              '#FF9800', '#2196F3', '#7B68EE', '#9C27B0',
              '#f44336', '#4CAF50', '#FFEB3B', TEAL_ACCENT
            ],
            borderWidth: 1
          }]
        },
        options: {
          responsive: true, maintainAspectRatio: false,
          plugins: { legend: { labels: { color: IVORY_MUTED, font: { size: 11 } } } },
          scales: {
            x: { ticks: { color: IVORY_MUTED, font: { size: 10 } }, grid: { color: 'rgba(42,122,122,0.06)' } },
            y: { ticks: { color: IVORY_MUTED, font: { size: 10 } }, grid: { color: 'rgba(42,122,122,0.06)' } }
          }
        }
      });
    }, 50);
  }

  /* ═══════════════════════════════════════════════════════════════════
     THE APOLLO SLATE — THAUMA
     "The Spatial Frontier"
     ═══════════════════════════════════════════════════════════════════ */
  function renderThaumaSlate(ct) {
    if (!window.renderStripboard) {
      ct.innerHTML = '<p style="color:#60a5fa;">Stripboard engine loading…</p>';
      return;
    }
    window.renderStripboard(ct, {
      title: 'THAUMA Slate: The First 10 Frontiers',
      themeColor: '#60a5fa',
      budgetColor: '#c9a84c',
      thesis: 'Constructing and financing the first 10 programmable spaces. We aim the Hubble spotlight of tech at abandoned civic voids, funding the build via installation economics to yield the Spatial OS of the 2030s.',
      quote: 'Space: It\u2019s Still a Frontier\u2026 there is a staggering glut of empty, abandoned space in our cities. \u2014 NYT',
      manifesto: 'Physical civic space is the final un-rendered computing platform. THAUMA doesn\u2019t just renovate; it programs the void. By turning abandoned transit concourses into responsive environments using acoustic metamaterials, we author the OS for commercial real estate.',
      columns: [
        {
          id: 'THAUMA #001', title: 'N. Broad Concourse',
          budget: 'Build Budget: $4.5M | FV: $18M',
          thesis: 'Subterranean space as a responsive, therapeutic nervous system.',
          events: [
            { time: 'MO 01', title: 'Void Acquisition', desc: '48,000 sqft underground transit void secured. THAUMA/OS central computing node installed. Baseline telemetry begins.', tags: [{ label: 'INFRASTRUCTURE', color: '#60a5fa' }] },
            { time: 'MO 04', title: 'Programmable Matter', desc: 'Acoustic metamaterials and phase-change panels physically installed to capture the 90-second subway vibration and translate it into a calming ambient rhythm.', tags: [{ label: 'MATERIAL SCIENCE', color: '#f472b6' }] },
            { time: 'MO 08', title: 'The Premiere', desc: 'Citizens enter the space. The Concourse actively reads collective tension and dynamically shifts thermal/acoustic properties to down-regulate allostatic load.', tags: [{ label: 'SPATIAL COMPUTE', color: '#c9a84c' }] },
            { time: 'MO 12', title: 'IP Extraction: Spatial OS', desc: 'The spatial configuration that actively lowered visitor stress is exported as YAML and licensed to Delta Airlines for high-stress transit zones.', tags: [{ label: 'CIVILIZATION IP', color: '#a78bfa' }] }
          ]
        },
        {
          id: 'THAUMA #002', title: 'Strawberry Mansion Res.',
          budget: 'Build Budget: $3.2M | FV: $12M',
          thesis: 'Industrial brownfield rendered as a bioluminescent civic plaza.',
          events: [
            { time: 'MO 01', title: 'Environmental Telemetry', desc: 'Brownfield remediated. Passive crowd telemetry and soil-based sensors deployed to map the baseline emptiness.', tags: [{ label: 'INFRASTRUCTURE', color: '#60a5fa' }] },
            { time: 'MO 05', title: 'Living Architecture', desc: 'Deployment of subtractive odor synthesis and bioluminescent coatings that react to local air quality and human proximity.', tags: [{ label: 'MATERIAL SCIENCE', color: '#f472b6' }] },
            { time: 'MO 12', title: 'IP Extraction: Civic APIs', desc: 'The exact THAUMA/OS configuration for rendering safe, populated outdoor space without heavy policing is licensed to 5 major metro parks departments.', tags: [{ label: 'CIVILIZATION IP', color: '#a78bfa' }] }
          ]
        }
      ]
    });
  }

  /* ─── initial render ─── */
  renderTab();
};
