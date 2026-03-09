/**
 * BATHS STUDIO SUITE — FINANCE STUDIO
 * ═══════════════════════════════════════════
 * Exports: window.renderFinance(container)
 *
 * Sections (tabs):
 *   A. Program Eligibility Engine (12 programs, 6 archetype presets)
 *   B. Benefits Cliff Guard (treasury phase-out, EMTR, Chart.js)
 *   C. Bond Pricing Studio (DomeBond + ChronBond)
 *   D. Capital Markets / Prevention-Backed Securities
 *   E. Coordination Model Scoring
 *   F. Wrong-Pocket Analysis
 *   G. Agreement Generator
 *
 * Data source: window.BATHS_DATA (data.js)
 * Never shows legacy names "Domes" or "Spheres" — uses DUOMO and THAUMA
 */

window.renderFinance = function (container) {
  'use strict';

  /* ───────────────────────── STYLE INJECTION ───────────────────────── */
  const styleId = 'finance-studio-styles';
  if (!document.getElementById(styleId)) {
    const style = document.createElement('style');
    style.id = styleId;
    style.textContent = `
      /* ═══ FINANCE STUDIO — SCOPED STYLES ═══ */
      .fin-wrap { font-family: system-ui, -apple-system, sans-serif; color: #f5f0e8; max-width: 1400px; margin: 0 auto; padding: 0 1rem; }
      .fin-title { font-family: Georgia, 'Times New Roman', serif; font-size: 2rem; font-weight: 700; color: #c9a84c; margin-bottom: 0.25rem; letter-spacing: -0.02em; }
      .fin-subtitle { color: rgba(245,240,232,0.5); font-size: 0.85rem; margin-bottom: 1.5rem; }

      /* TAB BAR */
      .fin-tabs { display: flex; gap: 0; border-bottom: 1px solid rgba(201,168,76,0.2); margin-bottom: 1.5rem; overflow-x: auto; -webkit-overflow-scrolling: touch; }
      .fin-tab { padding: 0.6rem 1rem; font-size: 0.78rem; color: rgba(245,240,232,0.45); cursor: pointer; border-bottom: 2px solid transparent; white-space: nowrap; transition: color 0.2s, border-color 0.2s; user-select: none; background: none; border-top: none; border-left: none; border-right: none; font-family: inherit; }
      .fin-tab:hover { color: rgba(245,240,232,0.7); }
      .fin-tab.active { color: #c9a84c; border-bottom-color: #c9a84c; }
      .fin-panel { display: none; }
      .fin-panel.active { display: block; }

      /* CARDS */
      .fin-card { background: rgba(201,168,76,0.04); border: 1px solid rgba(201,168,76,0.12); border-radius: 8px; padding: 1.25rem; margin-bottom: 1rem; }
      .fin-card-title { font-family: Georgia, serif; font-size: 1.1rem; color: #c9a84c; margin-bottom: 0.75rem; }
      .fin-card-subtitle { font-size: 0.8rem; color: rgba(245,240,232,0.5); margin-bottom: 1rem; }

      /* FORMS */
      .fin-form-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(180px, 1fr)); gap: 0.75rem; margin-bottom: 1rem; }
      .fin-field { display: flex; flex-direction: column; gap: 0.25rem; }
      .fin-field label { font-size: 0.72rem; color: rgba(245,240,232,0.5); text-transform: uppercase; letter-spacing: 0.06em; }
      .fin-field input, .fin-field select { background: rgba(10,10,15,0.8); border: 1px solid rgba(201,168,76,0.2); border-radius: 4px; padding: 0.5rem 0.65rem; color: #f5f0e8; font-size: 0.85rem; font-family: inherit; outline: none; transition: border-color 0.2s; }
      .fin-field input:focus, .fin-field select:focus { border-color: #c9a84c; }
      .fin-field input[type="checkbox"] { width: 18px; height: 18px; accent-color: #c9a84c; }
      .fin-chk-row { display: flex; align-items: center; gap: 0.5rem; }
      .fin-chk-row label { font-size: 0.8rem; color: rgba(245,240,232,0.6); text-transform: none; letter-spacing: 0; }

      /* BUTTONS */
      .fin-btn { background: rgba(201,168,76,0.15); border: 1px solid rgba(201,168,76,0.3); color: #c9a84c; padding: 0.5rem 1rem; border-radius: 4px; cursor: pointer; font-size: 0.8rem; font-family: inherit; transition: background 0.2s; }
      .fin-btn:hover { background: rgba(201,168,76,0.25); }
      .fin-btn.primary { background: rgba(201,168,76,0.25); border-color: #c9a84c; }
      .fin-btn-sm { padding: 0.3rem 0.6rem; font-size: 0.72rem; }
      .fin-btn-group { display: flex; flex-wrap: wrap; gap: 0.5rem; margin-bottom: 1rem; }

      /* TABLES */
      .fin-table-wrap { overflow-x: auto; margin-bottom: 1rem; }
      .fin-table { width: 100%; border-collapse: collapse; font-size: 0.8rem; }
      .fin-table th { text-align: left; padding: 0.5rem 0.75rem; color: rgba(245,240,232,0.5); font-weight: 600; font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.05em; border-bottom: 1px solid rgba(201,168,76,0.15); }
      .fin-table td { padding: 0.5rem 0.75rem; border-bottom: 1px solid rgba(201,168,76,0.06); vertical-align: top; }
      .fin-table tr:hover td { background: rgba(201,168,76,0.03); }
      .fin-eligible { color: #4caf50; font-weight: 600; }
      .fin-ineligible { color: rgba(245,240,232,0.25); }

      /* SUMMARY CARDS */
      .fin-summary { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin-bottom: 1.25rem; }
      .fin-stat { background: rgba(201,168,76,0.06); border: 1px solid rgba(201,168,76,0.1); border-radius: 6px; padding: 1rem; text-align: center; }
      .fin-stat-value { font-family: 'SF Mono', Consolas, monospace; font-size: 1.5rem; color: #c9a84c; font-weight: 700; }
      .fin-stat-label { font-size: 0.7rem; color: rgba(245,240,232,0.45); margin-top: 0.25rem; text-transform: uppercase; letter-spacing: 0.05em; }
      .fin-stat.green .fin-stat-value { color: #4caf50; }
      .fin-stat.red .fin-stat-value { color: #ef5350; }

      /* CHART CONTAINER */
      .fin-chart-box { background: rgba(10,10,15,0.6); border: 1px solid rgba(201,168,76,0.1); border-radius: 8px; padding: 1rem; margin-bottom: 1rem; position: relative; height: 340px; }
      .fin-chart-box canvas { width: 100% !important; height: 100% !important; }

      /* TRANCHE VIZ */
      .fin-tranche-stack { display: flex; flex-direction: column; gap: 0; border-radius: 8px; overflow: hidden; margin-bottom: 1rem; }
      .fin-tranche { padding: 1rem 1.25rem; }
      .fin-tranche.senior { background: rgba(76,175,80,0.15); border-left: 4px solid #4caf50; }
      .fin-tranche.mezzanine { background: rgba(255,193,7,0.12); border-left: 4px solid #ffc107; }
      .fin-tranche.equity { background: rgba(244,67,54,0.12); border-left: 4px solid #f44336; }
      .fin-tranche-label { font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.05em; color: rgba(245,240,232,0.5); margin-bottom: 0.25rem; }
      .fin-tranche-value { font-family: 'SF Mono', Consolas, monospace; font-size: 1.2rem; color: #f5f0e8; }
      .fin-tranche-detail { font-size: 0.75rem; color: rgba(245,240,232,0.4); margin-top: 0.25rem; }

      /* AGREEMENT CARDS */
      .fin-agree-card { background: rgba(201,168,76,0.04); border: 1px solid rgba(201,168,76,0.12); border-radius: 8px; padding: 1rem 1.25rem; margin-bottom: 0.75rem; cursor: pointer; transition: border-color 0.2s; }
      .fin-agree-card:hover { border-color: rgba(201,168,76,0.3); }
      .fin-agree-card.selected { border-color: #c9a84c; background: rgba(201,168,76,0.08); }
      .fin-agree-type { font-family: 'SF Mono', Consolas, monospace; font-size: 0.75rem; color: #c9a84c; margin-bottom: 0.15rem; }
      .fin-agree-name { font-size: 0.95rem; color: #f5f0e8; font-weight: 600; margin-bottom: 0.25rem; }
      .fin-agree-law { font-size: 0.72rem; color: rgba(245,240,232,0.4); }

      /* BADGE */
      .fin-badge { display: inline-block; padding: 0.15rem 0.5rem; border-radius: 3px; font-size: 0.68rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.04em; }
      .fin-badge-green { background: rgba(76,175,80,0.15); color: #4caf50; }
      .fin-badge-gold { background: rgba(201,168,76,0.15); color: #c9a84c; }
      .fin-badge-red { background: rgba(244,67,54,0.12); color: #ef5350; }
      .fin-badge-blue { background: rgba(33,150,243,0.12); color: #42a5f5; }

      /* SCORE BAR */
      .fin-score-bar { background: rgba(201,168,76,0.08); border-radius: 3px; height: 8px; overflow: hidden; }
      .fin-score-fill { height: 100%; border-radius: 3px; transition: width 0.4s ease; }

      /* RESPONSIVE */
      @media (max-width: 768px) {
        .fin-form-grid { grid-template-columns: 1fr 1fr; }
        .fin-summary { grid-template-columns: 1fr 1fr; }
        .fin-title { font-size: 1.5rem; }
        .fin-tabs { gap: 0; }
        .fin-tab { padding: 0.5rem 0.65rem; font-size: 0.7rem; }
      }
    `;
    document.head.appendChild(style);
  }

  /* ───────────────────────── DATA REFERENCES ───────────────────────── */
  const D = window.BATHS_DATA || {};
  const rawProfiles = D.profiles || {};
  const profiles = {};
  Object.keys(rawProfiles).forEach(k => {
    const r = rawProfiles[k];
    profiles[k] = Object.assign({}, r, {
      location: (r.location && typeof r.location === 'object') ? (r.location.area || 'Philadelphia') : (r.location || 'Philadelphia'),
      systems: r.systems_involved || r.systems || [],
      costFragmented: r.annual_cost_fragmented || r.costFragmented || 0,
      costCoordinated: r.annual_cost_coordinated || r.costCoordinated || 0,
      delta: r.annual_savings || r.delta || 0,
      fiveYear: r.five_year_savings || r.fiveYear || 0,
      lifetime: r.lifetime_estimate || r.lifetime || 0
    });
  });
  const costPoints = D.costData || [];
  const coordModels = D.coordinationModels || [];
  const episodes = D.episodes || [];

  /* ───────────────────────── UTILITY FUNCTIONS ───────────────────────── */
  const $ = (sel, ctx) => (ctx || document).querySelector(sel);
  const $$ = (sel, ctx) => Array.from((ctx || document).querySelectorAll(sel));
  const fmt = (n) => {
    if (n == null || isNaN(n)) return '—';
    if (Math.abs(n) >= 1e9) return '$' + (n / 1e9).toFixed(1) + 'B';
    if (Math.abs(n) >= 1e6) return '$' + (n / 1e6).toFixed(1) + 'M';
    return '$' + Math.round(n).toLocaleString();
  };
  const fmtPct = (n) => (n * 100).toFixed(1) + '%';
  const fmtNum = (n) => Math.round(n).toLocaleString();
  const clamp = (v, lo, hi) => Math.max(lo, Math.min(hi, v));

  /* ───────────────────────── A. PROGRAM ELIGIBILITY ENGINE ───────────────────────── */

  // FPL 2024
  function fpl(household) {
    return 15060 + 5380 * (household - 1);
  }

  // SNAP max monthly by household size
  const SNAP_MAX_MONTHLY = { 1: 291, 2: 535, 3: 766, 4: 973, 5: 1155 };
  // EITC income limits by # children
  const EITC_LIMITS = { 0: 17640, 1: 46560, 2: 52918, 3: 56838 };
  // EITC max credits by # children
  const EITC_MAX = { 0: 632, 1: 3995, 2: 6604, 3: 7430 };

  // 6 Cosm archetype presets (from audit-spheres-engine lines 792-801)
  const ARCHETYPES = {
    marcus:  { label: 'Marcus — Single Dad', income: 28000, household: 3, age: 34, children: 2, disabled: false },
    elena:   { label: 'Elena — Working Poor', income: 22000, household: 2, age: 29, children: 1, disabled: false },
    james:   { label: 'James — Elderly Disabled', income: 14000, household: 1, age: 72, children: 0, disabled: true },
    rivera:  { label: 'Rivera Family — Benefits Cliff', income: 52000, household: 5, age: 38, children: 3, disabled: false },
    aisha:   { label: 'Aisha — Aged Out Foster Care', income: 12000, household: 1, age: 19, children: 0, disabled: false },
    median:  { label: 'Median — Benchmark', income: 59540, household: 2, age: 38, children: 1, disabled: false }
  };

  // AMI for Section 8 (Philadelphia default)
  const AREA_MEDIAN_INCOME = 52649;
  const MEDIAN_RENT_MONTHLY = 1107;

  function calculateEligibility(income, household, age, children, disabled) {
    const fplVal = fpl(household);
    const hasChildren = children > 0;
    const programs = [];

    // 1. Medicaid — ≤138% FPL
    const medicaidEligible = income <= fplVal * 1.38;
    let medicaidBenefit = 0;
    if (medicaidEligible) {
      if (age >= 65) medicaidBenefit = 12000;
      else if (hasChildren) medicaidBenefit = 8500;
      else medicaidBenefit = 6500;
    }
    programs.push({ name: 'Medicaid', eligible: medicaidEligible, annual: medicaidBenefit, threshold: '≤138% FPL', detail: fmt(Math.round(fplVal * 1.38)) + ' for HH of ' + household });

    // 2. CHIP — ≤250% FPL, must have children
    const chipEligible = income <= fplVal * 2.50 && hasChildren;
    const chipBenefit = chipEligible ? 2800 * children : 0;
    programs.push({ name: 'CHIP', eligible: chipEligible, annual: chipBenefit, threshold: '≤250% FPL + children', detail: hasChildren ? fmt(Math.round(fplVal * 2.50)) : 'No children' });

    // 3. SNAP — ≤130% FPL
    const snapEligible = income <= fplVal * 1.30;
    const snapMax = SNAP_MAX_MONTHLY[Math.min(household, 5)] || SNAP_MAX_MONTHLY[5];
    const snapBenefit = snapEligible ? Math.round(snapMax * 0.70 * 12) : 0;
    programs.push({ name: 'SNAP', eligible: snapEligible, annual: snapBenefit, threshold: '≤130% FPL', detail: fmt(Math.round(fplVal * 1.30)) + ' | Max ' + fmt(snapMax) + '/mo' });

    // 4. Section 8 — ≤50% AMI
    const sec8Eligible = income <= AREA_MEDIAN_INCOME * 0.50;
    const sec8Voucher = sec8Eligible ? Math.max(0, Math.round((MEDIAN_RENT_MONTHLY - (income * 0.30 / 12)) * 12)) : 0;
    programs.push({ name: 'Section 8 HCV', eligible: sec8Eligible, annual: sec8Voucher, threshold: '≤50% AMI', detail: fmt(Math.round(AREA_MEDIAN_INCOME * 0.50)) + ' (AMI: ' + fmt(AREA_MEDIAN_INCOME) + ')' });

    // 5. EITC — income limits by children
    const eitcChildKey = Math.min(children, 3);
    const eitcLimit = EITC_LIMITS[eitcChildKey];
    const eitcMaxCredit = EITC_MAX[eitcChildKey];
    const eitcEligible = income <= eitcLimit;
    const eitcBenefit = eitcEligible ? Math.round(eitcMaxCredit * 0.60) : 0;
    programs.push({ name: 'EITC', eligible: eitcEligible, annual: eitcBenefit, threshold: '≤' + fmt(eitcLimit), detail: 'Max credit: ' + fmt(eitcMaxCredit) + ' (' + eitcChildKey + ' child' + (eitcChildKey !== 1 ? 'ren' : '') + ')' });

    // 6. WIC — ≤185% FPL, children
    const wicEligible = income <= fplVal * 1.85 && hasChildren;
    const wicBenefit = wicEligible ? 600 * Math.min(children, 3) : 0;
    programs.push({ name: 'WIC', eligible: wicEligible, annual: wicBenefit, threshold: '≤185% FPL + children', detail: hasChildren ? fmt(Math.round(fplVal * 1.85)) : 'No children' });

    // 7. LIHEAP — ≤150% FPL
    const liheapEligible = income <= fplVal * 1.50;
    const liheapBenefit = liheapEligible ? 500 : 0;
    programs.push({ name: 'LIHEAP', eligible: liheapEligible, annual: liheapBenefit, threshold: '≤150% FPL', detail: fmt(Math.round(fplVal * 1.50)) });

    // 8. Head Start — ≤100% FPL, children 3-5
    const headStartEligible = income <= fplVal && hasChildren;
    const headStartBenefit = headStartEligible ? 10000 * children : 0;
    programs.push({ name: 'Head Start', eligible: headStartEligible, annual: headStartBenefit, threshold: '≤100% FPL + children 3-5', detail: hasChildren ? fmt(fplVal) : 'No children' });

    // 9. Free School Lunch — ≤130% FPL, children
    const fslEligible = income <= fplVal * 1.30 && hasChildren;
    const fslBenefit = fslEligible ? 1200 * children : 0;
    programs.push({ name: 'Free School Lunch', eligible: fslEligible, annual: fslBenefit, threshold: '≤130% FPL + children', detail: hasChildren ? fmt(Math.round(fplVal * 1.30)) : 'No children' });

    // 10. Reduced School Lunch — 130-185% FPL, children (only if not free)
    const rslEligible = !fslEligible && income <= fplVal * 1.85 && income > fplVal * 1.30 && hasChildren;
    const rslBenefit = rslEligible ? 800 * children : 0;
    programs.push({ name: 'Reduced School Lunch', eligible: rslEligible, annual: rslBenefit, threshold: '130-185% FPL + children', detail: hasChildren ? fmt(Math.round(fplVal * 1.30)) + '–' + fmt(Math.round(fplVal * 1.85)) : 'No children' });

    // 11. SSI — Age 65+ or disabled, income < $11,316
    const ssiEligible = (age >= 65 || disabled) && income < 11316;
    let ssiBenefit = 0;
    if (ssiEligible) {
      const countableIncome = Math.max(0, (income / 12) - 20);
      ssiBenefit = Math.max(0, Math.round((943 - countableIncome) * 12));
    }
    programs.push({ name: 'SSI', eligible: ssiEligible, annual: ssiBenefit, threshold: '65+ or disabled, <$11,316', detail: (age >= 65 || disabled) ? 'Max $943/mo − countable' : 'Not 65+ or disabled' });

    // 12. TANF — ≤100% FPL, children
    const tanfEligible = income <= fplVal && hasChildren;
    const tanfBenefit = tanfEligible ? 400 * 12 : 0;
    programs.push({ name: 'TANF', eligible: tanfEligible, annual: tanfBenefit, threshold: '≤100% FPL + children', detail: hasChildren ? fmt(fplVal) : 'No children' });

    // 13. Pell Grant — age 17-30, income < $60k
    const pellEligible = age >= 17 && age <= 30 && income < 60000;
    let pellBenefit = 0;
    if (pellEligible) {
      pellBenefit = income < 30000 ? 7395 : 3698;
    }
    programs.push({ name: 'Pell Grant', eligible: pellEligible, annual: pellBenefit, threshold: 'Age 17-30, <$60k', detail: age >= 17 && age <= 30 ? (income < 30000 ? 'Full: $7,395' : '$30k-$60k: $3,698') : 'Age ' + age + ' outside 17-30' });

    return programs;
  }

  function calculateCosts(programs) {
    const totalBenefits = programs.reduce((s, p) => s + (p.eligible ? p.annual : 0), 0);
    const fragmented = Math.round(totalBenefits * 1.30);
    const coordinated = Math.round(fragmented * 0.60);
    const delta = fragmented - coordinated;
    return { totalBenefits, fragmented, coordinated, delta, eligible: programs.filter(p => p.eligible).length, total: programs.length };
  }

  /* ───────────────────────── B. BENEFITS CLIFF GUARD ───────────────────────── */

  const PHASE_OUTS = {
    snap:     { floor: 18000, ceiling: 36000, base: 2400, label: 'SNAP' },
    medicaid: { floor: 20000, ceiling: 40000, base: 8000, label: 'Medicaid' },
    tanf:     { floor: 10000, ceiling: 24000, base: 4800, label: 'TANF' },
    housing:  { floor: 15000, ceiling: 45000, base: 10000, label: 'Housing' },
    ccdf:     { floor: 20000, ceiling: 50000, base: 8400, label: 'CCDF' },
    ssi:      { floor: 10000, ceiling: 28000, base: 10800, label: 'SSI' },
    liheap:   { floor: 15000, ceiling: 30000, base: 500, label: 'LIHEAP' },
    wic:      { floor: 22000, ceiling: 48000, base: 600, label: 'WIC' },
    eitc:     { floor: 15000, ceiling: 55000, base: 3600, label: 'EITC' }
  };

  function benefitAtIncome(prog, income) {
    if (income <= prog.floor) return prog.base;
    if (income >= prog.ceiling) return 0;
    const fraction = (prog.ceiling - income) / (prog.ceiling - prog.floor);
    return prog.base * fraction;
  }

  function calculateCliffGuard(currentIncome, currentBenefits) {
    const step = 500;
    const maxIncome = Math.max(currentIncome * 3, 150000);
    const dataPoints = [];
    let maxSafeIncome = currentIncome;
    const cliffZones = [];
    let inCliff = false;

    for (let inc = currentIncome; inc <= maxIncome; inc += step) {
      let totalBen = 0;
      const benDetail = {};
      for (const [key, prog] of Object.entries(PHASE_OUTS)) {
        const baseAmt = (currentBenefits && currentBenefits[key]) || prog.base;
        const adjusted = { ...prog, base: baseAmt };
        const val = benefitAtIncome(adjusted, inc);
        totalBen += val;
        benDetail[key] = val;
      }

      const netIncome = inc + totalBen;
      let emtr = 0;
      if (inc > currentIncome) {
        const prevPt = dataPoints[dataPoints.length - 1];
        const incGain = inc - prevPt.income;
        const netGain = netIncome - prevPt.netIncome;
        emtr = incGain > 0 ? 1 - (netGain / incGain) : 0;
      }

      if (emtr <= 0.5) {
        maxSafeIncome = inc;
        if (inCliff) { inCliff = false; }
      } else {
        if (!inCliff) { cliffZones.push({ start: inc }); inCliff = true; }
        cliffZones[cliffZones.length - 1].end = inc;
      }

      dataPoints.push({ income: inc, totalBenefits: totalBen, netIncome, emtr, benefits: benDetail });
    }

    return { dataPoints, maxSafeIncome, cliffZones };
  }

  /* ───────────────────────── C. BOND PRICING ───────────────────────── */

  function getDomeBondRating(cosmScore) {
    if (cosmScore >= 80) return 'AAA';
    if (cosmScore >= 60) return 'AA';
    if (cosmScore >= 40) return 'A';
    if (cosmScore >= 20) return 'BBB';
    return 'B';
  }

  function getDomeBondCoupon(cosmScore) {
    if (cosmScore >= 80) return 0.035;
    if (cosmScore >= 70) return 0.040;
    if (cosmScore >= 60) return 0.045;
    if (cosmScore >= 50) return 0.055;
    if (cosmScore >= 40) return 0.065;
    return 0.080;
  }

  function priceDomeBond(delta, cosmScore, programCount, maturityYears) {
    maturityYears = maturityYears || 7;
    const faceValue = delta;
    const rating = getDomeBondRating(cosmScore);
    const couponRate = getDomeBondCoupon(cosmScore);
    const annualCoupon = faceValue * couponRate;
    // Simple YTM approximation
    const ytm = (annualCoupon + (faceValue - faceValue * 0.95) / maturityYears) / ((faceValue + faceValue * 0.95) / 2);
    return {
      faceValue, rating, couponRate, maturityYears,
      annualCoupon: Math.round(annualCoupon),
      ytm: ytm,
      programsBacking: programCount,
      cosmScore
    };
  }

  function getChronBondRating(permanence, policy) {
    if (permanence >= 0.8 && policy >= 0.5) return 'AAA';
    if (permanence >= 0.6) return 'AA';
    if (permanence >= 0.4) return 'A';
    return 'BBB';
  }

  function priceChronBond(sqft, accessHours, permanence, catalyst, policy, maturityYears) {
    maturityYears = maturityYears || 10;
    const significance = (permanence + catalyst + policy) / 3;
    const chronScore = (sqft * accessHours) * (1 + significance);
    const economicImpact = chronScore * 0.5; // simplified economic multiplier
    const faceValue = economicImpact;
    const rating = getChronBondRating(permanence, policy);
    const couponRate = rating === 'AAA' ? 0.04 : rating === 'AA' ? 0.05 : rating === 'A' ? 0.06 : 0.07;
    const annualCoupon = faceValue * couponRate;
    const ytm = (annualCoupon + (faceValue - faceValue * 0.95) / maturityYears) / ((faceValue + faceValue * 0.95) / 2);
    return {
      faceValue: Math.round(faceValue),
      rating, couponRate, maturityYears,
      annualCoupon: Math.round(annualCoupon),
      ytm, chronScore: Math.round(chronScore),
      sqftBacking: sqft, permanence, catalyst, policy
    };
  }

  /* ───────────────────────── D. CAPITAL MARKETS ───────────────────────── */

  const PAYOUT_RATIO = 0.70;
  const TRANCHE_YIELD_MULT = { senior: 0.6, mezzanine: 1.0, equity: 1.5 };
  const TRANCHE_RISK_MULT = { senior: 0.4, mezzanine: 1.0, equity: 1.8 };
  const STRESS_SCENARIOS = { recession: 0.30, moderate: 0.15, baseline: 0.00 };

  // Build settlement contracts from seed profiles
  function buildSettlementContracts() {
    const contracts = [];
    const profileKeys = Object.keys(profiles);
    profileKeys.forEach(key => {
      const p = profiles[key];
      if (!p) return;
      const delta = p.delta || (p.costFragmented - p.costCoordinated) || 0;
      if (delta <= 0) return;
      // Split savings across payers
      const medicaidPct = p.benefits && p.benefits.medicaid ? 0.4 : 0.25;
      const countyPct = 0.3;
      const fedPct = 1 - medicaidPct - countyPct;
      contracts.push({
        id: 'sc-' + key,
        person: p.name || key,
        intervention: (p.conditions || []).join(', ') || 'coordination',
        expectedSavings: {
          medicaid: Math.round(delta * medicaidPct),
          county: Math.round(delta * countyPct),
          federal: Math.round(delta * fedPct)
        },
        probability: clamp(0.55 + (delta / 200000), 0.40, 0.85),
        totalSavings: delta
      });
    });
    return contracts;
  }

  function poolContracts(contracts, tranche) {
    tranche = tranche || 'mezzanine';
    let totalNotional = 0;
    let weightedYieldSum = 0;
    contracts.forEach(c => {
      const totalSav = Object.values(c.expectedSavings).reduce((a, b) => a + b, 0);
      const weighted = totalSav * c.probability;
      totalNotional += weighted;
      weightedYieldSum += c.probability * weighted;
    });
    const baseYield = totalNotional > 0 ? weightedYieldSum / totalNotional : 0;
    const expectedYield = baseYield * (TRANCHE_YIELD_MULT[tranche] || 1);
    const coupon = expectedYield * PAYOUT_RATIO;
    return { totalNotional: Math.round(totalNotional), baseYield, expectedYield, coupon, tranche };
  }

  function priceBondCapMarkets(contracts, tranche, discountRate) {
    tranche = tranche || 'mezzanine';
    discountRate = discountRate || 0.05;
    const riskMult = TRANCHE_RISK_MULT[tranche] || 1;
    let expectedCF = 0;
    let variance = 0;
    let defaultProbProduct = 1;

    contracts.forEach(c => {
      const totalSav = Object.values(c.expectedSavings).reduce((a, b) => a + b, 0);
      const p = c.probability;
      expectedCF += (p * totalSav) / (1 + discountRate);
      variance += p * (1 - p) * totalSav * totalSav;
      defaultProbProduct *= (1 - p);
    });

    const pool = poolContracts(contracts, tranche);
    const expectedReturn = expectedCF - pool.totalNotional;
    const var95 = 1.645 * Math.sqrt(variance) * riskMult;
    const defaultProb = defaultProbProduct;

    return { expectedCF: Math.round(expectedCF), expectedReturn: Math.round(expectedReturn), var95: Math.round(var95), defaultProb, pool };
  }

  function stressTest(contracts, scenario) {
    const haircut = STRESS_SCENARIOS[scenario] || 0;
    const stressed = contracts.map(c => ({
      ...c,
      probability: clamp(c.probability * (1 - haircut), 0.05, 0.95)
    }));
    return stressed;
  }

  /* ───────────────────────── E. COORDINATION MODEL SCORING ───────────────────────── */

  const DOMAIN_WEIGHTS = {
    health: 1.0, behavioral_health: 0.9, housing: 0.8, income: 0.7,
    education: 0.7, child_welfare: 0.8, justice: 0.7, social_support: 0.6, immigration: 0.5
  };

  const POLITICAL_SCORES = { high: 1.0, moderate: 0.7, low: 0.4, contentious: 0.2 };

  const CONTEXT_ALIGNMENT = {
    supportive: { high: 1.0, moderate: 0.9, low: 0.7, contentious: 0.5 },
    neutral:    { high: 0.9, moderate: 0.8, low: 0.6, contentious: 0.3 },
    resistant:  { high: 0.7, moderate: 0.6, low: 0.4, contentious: 0.2 },
    hostile:    { high: 0.5, moderate: 0.4, low: 0.2, contentious: 0.1 }
  };

  const BUDGET_BREAKDOWN = {
    personnel: 0.45, technology: 0.15, operations: 0.12,
    provider_payments: 0.15, administration: 0.08, contingency: 0.05
  };

  // 10 architect models (from domes-architect seed)
  const ARCHITECT_MODELS = [
    { id: 1, abbr: 'ACO', name: 'Accountable Care Organization', category: 'managed_care', domains: ['health','behavioral_health','income'], budget: { min: 5e6, max: 5e8 }, timeline: '12-18 months', evidence: 'strong', political: 'high', population: ['complex_needs','elderly','chronic_conditions'] },
    { id: 2, abbr: 'Health Home', name: 'Health Home', category: 'managed_care', domains: ['health','behavioral_health','housing','social_support'], budget: { min: 1e6, max: 5e7 }, timeline: '9-15 months', evidence: 'moderate', political: 'high', population: ['chronic_conditions','smi','sud'] },
    { id: 3, abbr: 'PACE', name: 'Program of All-Inclusive Care for the Elderly', category: 'managed_care', domains: ['health','housing','social_support','income'], budget: { min: 3e6, max: 8e7 }, timeline: '18-36 months', evidence: 'strong', political: 'high', population: ['elderly','dual_eligible'] },
    { id: 4, abbr: 'WRAP', name: 'Wraparound / WRAP', category: 'community_based', domains: ['child_welfare','behavioral_health','education','justice'], budget: { min: 5e5, max: 2e7 }, timeline: '6-12 months', evidence: 'strong', political: 'moderate', population: ['youth','families','child_welfare'] },
    { id: 5, abbr: 'CCR', name: 'Coordinated Care Resource Ring', category: 'community_based', domains: ['health','housing','income','education'], budget: { min: 2e5, max: 5e6 }, timeline: '3-6 months', evidence: 'moderate', political: 'high', population: ['general','low_income'] },
    { id: 6, abbr: 'MCO', name: 'Managed Care Organization', category: 'managed_care', domains: ['health','behavioral_health'], budget: { min: 5e7, max: 5e9 }, timeline: '18-24 months', evidence: 'strong', political: 'moderate', population: ['medicaid','general'] },
    { id: 7, abbr: 'CHW Hub', name: 'Community Health Worker Hub', category: 'community_based', domains: ['health','social_support','housing','education'], budget: { min: 3e5, max: 8e6 }, timeline: '3-6 months', evidence: 'moderate', political: 'high', population: ['underserved','immigrant','rural'] },
    { id: 8, abbr: 'SIB', name: 'Social Impact Bond', category: 'specialized', domains: ['justice','housing','behavioral_health','income'], budget: { min: 2e6, max: 5e7 }, timeline: '12-24 months', evidence: 'emerging', political: 'moderate', population: ['reentry','homeless','recidivism'] },
    { id: 9, abbr: 'DSNP+', name: 'Dual Special Needs Plan (Enhanced)', category: 'managed_care', domains: ['health','behavioral_health','income','housing'], budget: { min: 2e7, max: 2e9 }, timeline: '18-24 months', evidence: 'moderate', political: 'moderate', population: ['dual_eligible','elderly','disabled'] },
    { id: 10, abbr: 'CDIH', name: 'Cross-System Data Integration Hub', category: 'hybrid', domains: ['health','housing','income','education','justice','child_welfare'], budget: { min: 1e6, max: 3e7 }, timeline: '12-24 months', evidence: 'emerging', political: 'low', population: ['cross_system','complex_needs'] }
  ];

  // Architect scoring (from coordination_engine.py)
  function scoreArchitectModel(model, targetDomains, politicalContext, annualBudget, timeHorizon) {
    politicalContext = politicalContext || 'neutral';
    annualBudget = annualBudget || 10000000;
    timeHorizon = timeHorizon || '3yr';

    // Coverage: weighted overlap
    const targetSet = new Set(targetDomains);
    let weightedOverlap = 0;
    let totalWeight = 0;
    targetDomains.forEach(d => {
      const w = DOMAIN_WEIGHTS[d] || 0.5;
      totalWeight += w;
      if (model.domains.includes(d)) weightedOverlap += w;
    });
    const coverage = totalWeight > 0 ? weightedOverlap / totalWeight : 0;

    // Budget fit
    const midBudget = (model.budget.min + model.budget.max) / 2;
    const budgetScore = annualBudget >= model.budget.min && annualBudget <= model.budget.max
      ? 1.0
      : annualBudget < model.budget.min
        ? annualBudget / model.budget.min
        : model.budget.max / annualBudget;

    // Political alignment
    const modelPol = model.political || 'moderate';
    const alignment = (CONTEXT_ALIGNMENT[politicalContext] || CONTEXT_ALIGNMENT.neutral)[modelPol] || 0.5;

    // Timeline
    const horizonMonths = timeHorizon === '1yr' ? 12 : timeHorizon === '3yr' ? 36 : 60;
    const timeStr = model.timeline || '12-18 months';
    const timeMatch = timeStr.match(/(\d+)/);
    const modelMonths = timeMatch ? parseInt(timeMatch[1]) : 12;
    const timelineScore = modelMonths <= horizonMonths ? 1.0 : horizonMonths / modelMonths;

    const composite = coverage * 0.35 + budgetScore * 0.25 + alignment * 0.20 + timelineScore * 0.20;

    return { coverage, budgetScore, politicalAlignment: alignment, timelineScore, composite: clamp(composite, 0, 1) };
  }

  // baths-engine scoring (from data/coordination.py)
  function scoreBathsCoordination(model, targetDimensions) {
    const modelDims = new Set(model.domains || []);
    const target = new Set(targetDimensions || []);
    const overlap = target.size > 0 ? [...target].filter(d => modelDims.has(d)).length / target.size : 0;
    const savingsPct = (model.savings || model.savingsPct || 15);
    const savingsScore = savingsPct / 25;
    const costStr = model.cost || 'medium';
    const costPenalty = { low: 0, medium: 0.1, high: 0.2, very_high: 0.3 };
    const fit = (overlap * 0.6) + (savingsScore * 0.4) - (costPenalty[costStr] || 0.1);
    return clamp(fit, 0, 1);
  }

  /* ───────────────────────── F. WRONG-POCKET ANALYSIS ───────────────────────── */

  function getWrongPocketData() {
    // Organize cost data by category
    const categories = {};
    costPoints.forEach(cp => {
      if (!categories[cp.category]) categories[cp.category] = [];
      categories[cp.category].push(cp);
    });
    return categories;
  }

  /* ───────────────────────── G. AGREEMENT GENERATOR ───────────────────────── */

  const AGREEMENT_TEMPLATES = [
    { id: 'tpl_baa', type: 'BAA', name: 'Business Associate Agreement', laws: 'HIPAA, HITECH Act, 45 CFR Parts 160 & 164', desc: 'Required when a covered entity shares PHI with a business associate for services.' },
    { id: 'tpl_dua', type: 'DUA', name: 'Data Use Agreement', laws: 'HIPAA, 45 CFR §164.514(e)', desc: 'Governs use of limited data sets for research, public health, or health care operations.' },
    { id: 'tpl_mou', type: 'MOU', name: 'Memorandum of Understanding', laws: 'Varies by jurisdiction', desc: 'Non-binding framework for interagency cooperation and data sharing intent.' },
    { id: 'tpl_idsa', type: 'IDSA', name: 'Interagency Data Sharing Agreement', laws: 'HIPAA, Privacy Act of 1974, State statutes', desc: 'Binding agreement between government agencies for systematic data exchange.' },
    { id: 'tpl_qsoa', type: 'QSOA', name: 'Qualified Service Organization Agreement', laws: '42 CFR Part 2, HIPAA', desc: 'Required when substance use disorder treatment programs share records with service organizations.' },
    { id: 'tpl_hipaa_consent', type: 'HIPAA_consent', name: 'HIPAA Authorization for Disclosure', laws: '45 CFR §164.508', desc: 'Individual authorization for release of protected health information.' },
    { id: 'tpl_ferpa_consent', type: 'FERPA_consent', name: 'FERPA Consent to Disclose', laws: '20 U.S.C. §1232g, 34 CFR Part 99', desc: 'Parental/student consent for release of education records.' }
  ];

  const GAP_TO_AGREEMENT = {
    'HIPAA': ['BAA', 'HIPAA_consent'],
    '42 CFR Part 2': ['QSOA', '42CFR_consent'],
    'FERPA': ['FERPA_consent'],
    'CJIS_Security_Policy': ['IDSA'],
    'Medicaid Inmate Exclusion Policy': ['IDSA', 'HIPAA_consent'],
    'Privacy Act / 42 CFR Part 2': ['42CFR_consent', 'DUA']
  };

  const BARRIER_TYPE_MAP = {
    legal: ['IDSA', 'MOU'],
    technical: ['IDSA', 'MOU', 'joint_funding'],
    political: ['MOU', 'compact'],
    funding: ['joint_funding', 'MOU'],
    consent: ['HIPAA_consent']
  };

  function determineAgreementTypes(barrierLaw, barrierType) {
    if (barrierLaw && GAP_TO_AGREEMENT[barrierLaw]) return GAP_TO_AGREEMENT[barrierLaw];
    if (barrierType && BARRIER_TYPE_MAP[barrierType]) return BARRIER_TYPE_MAP[barrierType];
    return ['MOU'];
  }

  /* ═══════════════════════════════════════════════════════════════════
     RENDER — Build the UI
     ═══════════════════════════════════════════════════════════════════ */

  const TAB_DEFS = [
    { id: 'eligibility', label: 'Eligibility Engine' },
    { id: 'cliff',       label: 'Cliff Guard' },
    { id: 'bonds',       label: 'Bond Pricing' },
    { id: 'capmarkets',  label: 'Capital Markets' },
    { id: 'coordination',label: 'Coordination Scoring' },
    { id: 'wrongpocket', label: 'Wrong-Pocket Analysis' },
    { id: 'agreements',  label: 'Agreement Generator' }
  ];

  container.innerHTML = `
    <div class="fin-wrap">
      <div class="fin-title">Finance Studio</div>
      <div class="fin-subtitle">Capital markets, eligibility modeling, coordination scoring, and fiscal engineering — powered by BATHS data</div>
      <div class="fin-tabs" id="finTabs">
        ${TAB_DEFS.map((t, i) => `<button class="fin-tab${i === 0 ? ' active' : ''}" data-tab="${t.id}">${t.label}</button>`).join('')}
      </div>
      <div id="finPanels">
        ${TAB_DEFS.map((t, i) => `<div class="fin-panel${i === 0 ? ' active' : ''}" id="panel-${t.id}"></div>`).join('')}
      </div>
    </div>
  `;

  // Tab switching
  const wrap = container.querySelector('.fin-wrap');
  const tabs = wrap.querySelectorAll('.fin-tab');
  const panels = wrap.querySelectorAll('.fin-panel');
  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      tabs.forEach(t => t.classList.remove('active'));
      panels.forEach(p => p.classList.remove('active'));
      tab.classList.add('active');
      const panel = wrap.querySelector('#panel-' + tab.dataset.tab);
      if (panel) panel.classList.add('active');
    });
  });

  /* ═══ PANEL A: ELIGIBILITY ENGINE ═══ */
  const panelEligibility = wrap.querySelector('#panel-eligibility');
  panelEligibility.innerHTML = `
    <div class="fin-card">
      <div class="fin-card-title">Program Eligibility Engine</div>
      <div class="fin-card-subtitle">12-program eligibility calculator · FPL(household) = $15,060 + $5,380 × (household − 1)</div>

      <div class="fin-btn-group" id="eligPresets">
        ${Object.entries(ARCHETYPES).map(([k, v]) => `<button class="fin-btn fin-btn-sm" data-preset="${k}">${v.label}</button>`).join('')}
      </div>

      <div class="fin-form-grid" id="eligForm">
        <div class="fin-field"><label>Annual Income ($)</label><input type="number" id="eligIncome" value="28000" min="0" step="500"></div>
        <div class="fin-field"><label>Household Size</label><input type="number" id="eligHousehold" value="3" min="1" max="10"></div>
        <div class="fin-field"><label>Age</label><input type="number" id="eligAge" value="34" min="0" max="120"></div>
        <div class="fin-field"><label>Number of Children</label><input type="number" id="eligChildren" value="2" min="0" max="10"></div>
        <div class="fin-field">
          <label>Disabled</label>
          <div class="fin-chk-row"><input type="checkbox" id="eligDisabled"><label for="eligDisabled">Yes</label></div>
        </div>
      </div>
      <button class="fin-btn primary" id="eligCalc">Calculate Eligibility</button>
    </div>

    <div id="eligResults" style="display:none">
      <div class="fin-summary" id="eligSummary"></div>
      <div class="fin-card">
        <div class="fin-card-title">Program Results</div>
        <div class="fin-table-wrap"><table class="fin-table" id="eligTable"><thead><tr><th>Program</th><th>Status</th><th>Threshold</th><th>Annual Benefit</th><th>Details</th></tr></thead><tbody></tbody></table></div>
      </div>
      <div class="fin-card">
        <div class="fin-card-title">Cost Analysis — Fragmented vs. Coordinated</div>
        <div class="fin-card-subtitle">30% administrative overhead applied to fragmented delivery · 40% reduction under coordination</div>
        <div class="fin-summary" id="eligCostSummary"></div>
      </div>
    </div>
  `;

  function runEligibility() {
    const income = parseInt(panelEligibility.querySelector('#eligIncome').value) || 0;
    const household = parseInt(panelEligibility.querySelector('#eligHousehold').value) || 1;
    const age = parseInt(panelEligibility.querySelector('#eligAge').value) || 30;
    const children = parseInt(panelEligibility.querySelector('#eligChildren').value) || 0;
    const disabled = panelEligibility.querySelector('#eligDisabled').checked;

    const programs = calculateEligibility(income, household, age, children, disabled);
    const costs = calculateCosts(programs);

    // Show results
    const resultsDiv = panelEligibility.querySelector('#eligResults');
    resultsDiv.style.display = 'block';

    // Summary
    panelEligibility.querySelector('#eligSummary').innerHTML = `
      <div class="fin-stat"><div class="fin-stat-value">${costs.eligible}</div><div class="fin-stat-label">Eligible Programs</div></div>
      <div class="fin-stat"><div class="fin-stat-value">${fmt(costs.totalBenefits)}</div><div class="fin-stat-label">Total Annual Benefits</div></div>
      <div class="fin-stat"><div class="fin-stat-value">${fmt(fpl(household))}</div><div class="fin-stat-label">FPL (HH of ${household})</div></div>
      <div class="fin-stat"><div class="fin-stat-value">${Math.round(income / fpl(household) * 100)}%</div><div class="fin-stat-label">Income as % FPL</div></div>
    `;

    // Table
    const tbody = panelEligibility.querySelector('#eligTable tbody');
    tbody.innerHTML = programs.map(p => `
      <tr>
        <td style="font-weight:600">${p.name}</td>
        <td><span class="${p.eligible ? 'fin-eligible' : 'fin-ineligible'}">${p.eligible ? '✓ Eligible' : '✗ Ineligible'}</span></td>
        <td style="font-size:0.75rem;color:rgba(245,240,232,0.5)">${p.threshold}</td>
        <td style="font-family:'SF Mono',Consolas,monospace;${p.eligible ? 'color:#c9a84c' : ''}">${p.eligible ? fmt(p.annual) + '/yr' : '—'}</td>
        <td style="font-size:0.72rem;color:rgba(245,240,232,0.4)">${p.detail}</td>
      </tr>
    `).join('');

    // Cost summary
    panelEligibility.querySelector('#eligCostSummary').innerHTML = `
      <div class="fin-stat red"><div class="fin-stat-value">${fmt(costs.fragmented)}</div><div class="fin-stat-label">Fragmented Cost (+ 30% overhead)</div></div>
      <div class="fin-stat green"><div class="fin-stat-value">${fmt(costs.coordinated)}</div><div class="fin-stat-label">Coordinated Cost (40% reduction)</div></div>
      <div class="fin-stat"><div class="fin-stat-value">${fmt(costs.delta)}</div><div class="fin-stat-label">Coordination Savings (Δ)</div></div>
      <div class="fin-stat"><div class="fin-stat-value">${costs.fragmented > 0 ? Math.round((costs.delta / costs.fragmented) * 100) : 0}%</div><div class="fin-stat-label">Savings Rate</div></div>
    `;
  }

  // Presets
  panelEligibility.querySelector('#eligPresets').addEventListener('click', e => {
    const btn = e.target.closest('[data-preset]');
    if (!btn) return;
    const p = ARCHETYPES[btn.dataset.preset];
    if (!p) return;
    panelEligibility.querySelector('#eligIncome').value = p.income;
    panelEligibility.querySelector('#eligHousehold').value = p.household;
    panelEligibility.querySelector('#eligAge').value = p.age;
    panelEligibility.querySelector('#eligChildren').value = p.children;
    panelEligibility.querySelector('#eligDisabled').checked = p.disabled;
    runEligibility();
  });

  panelEligibility.querySelector('#eligCalc').addEventListener('click', runEligibility);

  // Auto-run with Marcus
  runEligibility();

  /* ═══ PANEL B: CLIFF GUARD ═══ */
  const panelCliff = wrap.querySelector('#panel-cliff');
  panelCliff.innerHTML = `
    <div class="fin-card">
      <div class="fin-card-title">Benefits Cliff Guard</div>
      <div class="fin-card-subtitle">Phase-out simulation for 9 programs · Effective Marginal Tax Rate (EMTR) analysis · Cliff zones = EMTR > 50%</div>
      <div class="fin-form-grid">
        <div class="fin-field"><label>Current Income ($)</label><input type="number" id="cliffIncome" value="22880" min="0" step="500"></div>
        <div class="fin-field"><label>Preset</label>
          <select id="cliffPreset">
            <option value="">Custom</option>
            ${Object.entries(profiles).map(([k, p]) => `<option value="${k}">${p.name || k} (${fmt(p.income)})</option>`).join('')}
          </select>
        </div>
      </div>
      <div class="fin-card-subtitle" style="margin-top:0.5rem">Program base amounts (editable):</div>
      <div class="fin-form-grid" id="cliffBenInputs">
        ${Object.entries(PHASE_OUTS).map(([key, prog]) => `
          <div class="fin-field"><label>${prog.label} (floor: ${fmt(prog.floor)}, ceil: ${fmt(prog.ceiling)})</label><input type="number" id="cliff-${key}" value="${prog.base}" min="0" step="100"></div>
        `).join('')}
      </div>
      <button class="fin-btn primary" id="cliffCalc">Run Cliff Analysis</button>
    </div>
    <div id="cliffResults" style="display:none">
      <div class="fin-summary" id="cliffSummary"></div>
      <div class="fin-card">
        <div class="fin-card-title">Benefits & Income vs. Earned Income</div>
        <div class="fin-chart-box"><canvas id="cliffChart"></canvas></div>
      </div>
      <div class="fin-card">
        <div class="fin-card-title">Effective Marginal Tax Rate</div>
        <div class="fin-chart-box"><canvas id="emtrChart"></canvas></div>
      </div>
      <div class="fin-card" id="cliffZonesCard" style="display:none">
        <div class="fin-card-title">⚠ Cliff Zones Detected</div>
        <div id="cliffZonesList"></div>
      </div>
    </div>
  `;

  let cliffBenChart = null;
  let cliffEmtrChart = null;

  panelCliff.querySelector('#cliffPreset').addEventListener('change', e => {
    const key = e.target.value;
    if (!key || !profiles[key]) return;
    const p = profiles[key];
    panelCliff.querySelector('#cliffIncome').value = p.income || 0;
    // Set benefits if available
    if (p.benefits) {
      Object.entries(PHASE_OUTS).forEach(([k]) => {
        const inp = panelCliff.querySelector('#cliff-' + k);
        if (inp && p.benefits[k] != null) inp.value = p.benefits[k];
      });
    }
  });

  function runCliffGuard() {
    const currentIncome = parseInt(panelCliff.querySelector('#cliffIncome').value) || 0;
    const currentBenefits = {};
    Object.keys(PHASE_OUTS).forEach(k => {
      const inp = panelCliff.querySelector('#cliff-' + k);
      if (inp) currentBenefits[k] = parseInt(inp.value) || 0;
    });

    const result = calculateCliffGuard(currentIncome, currentBenefits);
    const resultsDiv = panelCliff.querySelector('#cliffResults');
    resultsDiv.style.display = 'block';

    const totalCurrentBen = Object.values(currentBenefits).reduce((a, b) => a + b, 0);

    // Summary
    panelCliff.querySelector('#cliffSummary').innerHTML = `
      <div class="fin-stat"><div class="fin-stat-value">${fmt(currentIncome)}</div><div class="fin-stat-label">Current Earned Income</div></div>
      <div class="fin-stat"><div class="fin-stat-value">${fmt(totalCurrentBen)}</div><div class="fin-stat-label">Current Total Benefits</div></div>
      <div class="fin-stat green"><div class="fin-stat-value">${fmt(result.maxSafeIncome)}</div><div class="fin-stat-label">Max Safe Income (EMTR ≤ 50%)</div></div>
      <div class="fin-stat ${result.cliffZones.length > 0 ? 'red' : ''}"><div class="fin-stat-value">${result.cliffZones.length}</div><div class="fin-stat-label">Cliff Zones</div></div>
    `;

    // Cliff zones card
    const zonesCard = panelCliff.querySelector('#cliffZonesCard');
    if (result.cliffZones.length > 0) {
      zonesCard.style.display = 'block';
      panelCliff.querySelector('#cliffZonesList').innerHTML = result.cliffZones.map(z =>
        `<div style="padding:0.4rem 0;font-size:0.85rem;color:rgba(245,240,232,0.7);border-bottom:1px solid rgba(201,168,76,0.06)">
          <span class="fin-badge fin-badge-red">CLIFF</span>
          Income range: <strong style="color:#ef5350">${fmt(z.start)}</strong> → <strong style="color:#ef5350">${fmt(z.end)}</strong>
        </div>`
      ).join('');
    } else {
      zonesCard.style.display = 'none';
    }

    // Chart data
    const labels = result.dataPoints.filter((_, i) => i % 2 === 0).map(d => fmt(d.income));
    const benefitsData = result.dataPoints.filter((_, i) => i % 2 === 0).map(d => d.totalBenefits);
    const netData = result.dataPoints.filter((_, i) => i % 2 === 0).map(d => d.netIncome);
    const emtrData = result.dataPoints.filter((_, i) => i % 2 === 0).map(d => d.emtr * 100);

    // Identify cliff zone indices for background coloring
    const cliffBgColor = result.dataPoints.filter((_, i) => i % 2 === 0).map(d => {
      return d.emtr > 0.5 ? 'rgba(244,67,54,0.12)' : 'rgba(0,0,0,0)';
    });

    const chartDefaults = {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { labels: { color: 'rgba(245,240,232,0.6)', font: { size: 11 } } }
      },
      scales: {
        x: { ticks: { color: 'rgba(245,240,232,0.35)', font: { size: 9 }, maxTicksLimit: 15 }, grid: { color: 'rgba(201,168,76,0.06)' } },
        y: { ticks: { color: 'rgba(245,240,232,0.35)', font: { size: 10 } }, grid: { color: 'rgba(201,168,76,0.06)' } }
      }
    };

    // Benefits chart
    if (cliffBenChart) cliffBenChart.destroy();
    const benCtx = panelCliff.querySelector('#cliffChart').getContext('2d');
    cliffBenChart = new Chart(benCtx, {
      type: 'line',
      data: {
        labels,
        datasets: [
          { label: 'Total Benefits', data: benefitsData, borderColor: '#c9a84c', backgroundColor: 'rgba(201,168,76,0.1)', fill: true, tension: 0.3, pointRadius: 0 },
          { label: 'Net Income (Earned + Benefits)', data: netData, borderColor: '#4caf50', backgroundColor: 'rgba(76,175,80,0.05)', fill: false, tension: 0.3, pointRadius: 0 }
        ]
      },
      options: chartDefaults
    });

    // EMTR chart
    if (cliffEmtrChart) cliffEmtrChart.destroy();
    const emtrCtx = panelCliff.querySelector('#emtrChart').getContext('2d');
    cliffEmtrChart = new Chart(emtrCtx, {
      type: 'line',
      data: {
        labels,
        datasets: [
          {
            label: 'EMTR (%)',
            data: emtrData,
            borderColor: result.cliffZones.length > 0 ? '#ef5350' : '#c9a84c',
            backgroundColor: 'rgba(244,67,54,0.08)',
            fill: true,
            tension: 0.2,
            pointRadius: 0,
            segment: {
              borderColor: ctx => {
                const val = ctx.p1.parsed.y;
                return val > 50 ? '#ef5350' : '#c9a84c';
              },
              backgroundColor: ctx => {
                const val = ctx.p1.parsed.y;
                return val > 50 ? 'rgba(244,67,54,0.15)' : 'rgba(201,168,76,0.05)';
              }
            }
          },
          {
            label: '50% Cliff Threshold',
            data: emtrData.map(() => 50),
            borderColor: 'rgba(244,67,54,0.4)',
            borderDash: [6, 4],
            pointRadius: 0,
            fill: false
          }
        ]
      },
      options: {
        ...chartDefaults,
        scales: {
          ...chartDefaults.scales,
          y: { ...chartDefaults.scales.y, min: -20, max: 120, ticks: { ...chartDefaults.scales.y.ticks, callback: v => v + '%' } }
        }
      }
    });
  }

  panelCliff.querySelector('#cliffCalc').addEventListener('click', runCliffGuard);

  /* ═══ PANEL C: BOND PRICING STUDIO ═══ */
  const panelBonds = wrap.querySelector('#panel-bonds');
  panelBonds.innerHTML = `
    <div class="fin-card">
      <div class="fin-card-title">DUOMO Bond (DomeBond)</div>
      <div class="fin-card-subtitle">Backed by coordination savings (Δ) from whole-person DUOMO analysis · Rating based on Cosm score</div>
      <div class="fin-form-grid">
        <div class="fin-field"><label>Profile</label>
          <select id="bondProfile">
            ${Object.entries(profiles).map(([k, p]) => `<option value="${k}">${p.name} — Δ=${fmt(p.delta)}</option>`).join('')}
          </select>
        </div>
        <div class="fin-field"><label>Cosm Score (0-100)</label><input type="number" id="bondCosm" value="42" min="0" max="100"></div>
        <div class="fin-field"><label>Maturity (years)</label><input type="number" id="bondMaturity" value="7" min="1" max="30"></div>
      </div>
      <button class="fin-btn primary" id="bondCalcDome">Price DUOMO Bond</button>
    </div>
    <div id="domeBondResult" style="display:none"></div>

    <div class="fin-card" style="margin-top:1.5rem">
      <div class="fin-card-title">THAUMA Bond (ChronBond)</div>
      <div class="fin-card-subtitle">Backed by space activation · Formula: (sqft × access_hours) × (1 + significance) · Rating: permanence + policy</div>
      <div class="fin-form-grid">
        <div class="fin-field"><label>Parcel / Episode</label>
          <select id="chronParcel">
            ${episodes.map((ep, i) => `<option value="${i}">${ep.title} — ${fmtNum(ep.served || 0)} served</option>`).join('')}
          </select>
        </div>
        <div class="fin-field"><label>Square Footage</label><input type="number" id="chronSqft" value="48000" min="100"></div>
        <div class="fin-field"><label>Access Hours / Year</label><input type="number" id="chronAccess" value="2000" min="1"></div>
        <div class="fin-field"><label>Permanence (0-1)</label><input type="number" id="chronPerm" value="0.72" min="0" max="1" step="0.01"></div>
        <div class="fin-field"><label>Catalyst (0-1)</label><input type="number" id="chronCatalyst" value="0.65" min="0" max="1" step="0.01"></div>
        <div class="fin-field"><label>Policy (0-1)</label><input type="number" id="chronPolicy" value="0.50" min="0" max="1" step="0.01"></div>
        <div class="fin-field"><label>Maturity (years)</label><input type="number" id="chronMaturity" value="10" min="1" max="30"></div>
      </div>
      <button class="fin-btn primary" id="bondCalcChron">Price THAUMA Bond</button>
    </div>
    <div id="chronBondResult" style="display:none"></div>
  `;

  // DomeBond
  panelBonds.querySelector('#bondProfile').addEventListener('change', e => {
    const p = profiles[e.target.value];
    if (!p) return;
    // Suggest cosm from sample dome or default
    const cosm = 42; // default Cosm score
    panelBonds.querySelector('#bondCosm').value = cosm;
  });

  panelBonds.querySelector('#bondCalcDome').addEventListener('click', () => {
    const profileKey = panelBonds.querySelector('#bondProfile').value;
    const p = profiles[profileKey] || {};
    const delta = p.delta || 0;
    const cosm = parseInt(panelBonds.querySelector('#bondCosm').value) || 42;
    const maturity = parseInt(panelBonds.querySelector('#bondMaturity').value) || 7;
    const programCount = p.systems ? p.systems.length : 6;
    const bond = priceDomeBond(delta, cosm, programCount, maturity);

    const ratingColor = bond.rating === 'AAA' ? '#4caf50' : bond.rating === 'AA' ? '#8bc34a' : bond.rating === 'A' ? '#ffc107' : bond.rating === 'BBB' ? '#ff9800' : '#ef5350';

    panelBonds.querySelector('#domeBondResult').style.display = 'block';
    panelBonds.querySelector('#domeBondResult').innerHTML = `
      <div class="fin-card">
        <div class="fin-card-title" style="display:flex;justify-content:space-between;align-items:center">
          DUOMO Bond — ${p.name || profileKey}
          <span class="fin-badge" style="background:${ratingColor}22;color:${ratingColor};font-size:1rem;padding:0.3rem 0.8rem">${bond.rating}</span>
        </div>
        <div class="fin-summary">
          <div class="fin-stat"><div class="fin-stat-value">${fmt(bond.faceValue)}</div><div class="fin-stat-label">Face Value (Δ Savings)</div></div>
          <div class="fin-stat"><div class="fin-stat-value">${(bond.couponRate * 100).toFixed(1)}%</div><div class="fin-stat-label">Coupon Rate</div></div>
          <div class="fin-stat"><div class="fin-stat-value">${fmt(bond.annualCoupon)}</div><div class="fin-stat-label">Annual Coupon</div></div>
          <div class="fin-stat"><div class="fin-stat-value">${(bond.ytm * 100).toFixed(2)}%</div><div class="fin-stat-label">Yield to Maturity</div></div>
          <div class="fin-stat"><div class="fin-stat-value">${bond.maturityYears}yr</div><div class="fin-stat-label">Maturity</div></div>
          <div class="fin-stat"><div class="fin-stat-value">${bond.programsBacking}</div><div class="fin-stat-label">Programs Backing</div></div>
        </div>
        <div style="font-size:0.75rem;color:rgba(245,240,232,0.4);margin-top:0.5rem">
          Cosm Score: ${bond.cosmScore} · Rating thresholds: AAA ≥ 80, AA ≥ 60, A ≥ 40, BBB ≥ 20
        </div>
      </div>
    `;
  });

  // ChronBond
  panelBonds.querySelector('#chronParcel').addEventListener('change', e => {
    const ep = episodes[parseInt(e.target.value)];
    if (!ep) return;
    // Rough sqft estimate from episode data
    panelBonds.querySelector('#chronPerm').value = ((ep.permanence || 70) / 100).toFixed(2);
  });

  panelBonds.querySelector('#bondCalcChron').addEventListener('click', () => {
    const sqft = parseInt(panelBonds.querySelector('#chronSqft').value) || 48000;
    const access = parseInt(panelBonds.querySelector('#chronAccess').value) || 2000;
    const perm = parseFloat(panelBonds.querySelector('#chronPerm').value) || 0.7;
    const cat = parseFloat(panelBonds.querySelector('#chronCatalyst').value) || 0.6;
    const pol = parseFloat(panelBonds.querySelector('#chronPolicy').value) || 0.5;
    const maturity = parseInt(panelBonds.querySelector('#chronMaturity').value) || 10;
    const epIdx = parseInt(panelBonds.querySelector('#chronParcel').value) || 0;
    const ep = episodes[epIdx] || {};

    const bond = priceChronBond(sqft, access, perm, cat, pol, maturity);
    const ratingColor = bond.rating === 'AAA' ? '#4caf50' : bond.rating === 'AA' ? '#8bc34a' : bond.rating === 'A' ? '#ffc107' : '#ff9800';

    panelBonds.querySelector('#chronBondResult').style.display = 'block';
    panelBonds.querySelector('#chronBondResult').innerHTML = `
      <div class="fin-card">
        <div class="fin-card-title" style="display:flex;justify-content:space-between;align-items:center">
          THAUMA Bond — ${ep.title || 'Custom Parcel'}
          <span class="fin-badge" style="background:${ratingColor}22;color:${ratingColor};font-size:1rem;padding:0.3rem 0.8rem">${bond.rating}</span>
        </div>
        <div class="fin-summary">
          <div class="fin-stat"><div class="fin-stat-value">${fmt(bond.faceValue)}</div><div class="fin-stat-label">Face Value (Economic Impact)</div></div>
          <div class="fin-stat"><div class="fin-stat-value">${(bond.couponRate * 100).toFixed(1)}%</div><div class="fin-stat-label">Coupon Rate</div></div>
          <div class="fin-stat"><div class="fin-stat-value">${fmt(bond.annualCoupon)}</div><div class="fin-stat-label">Annual Coupon</div></div>
          <div class="fin-stat"><div class="fin-stat-value">${(bond.ytm * 100).toFixed(2)}%</div><div class="fin-stat-label">Yield to Maturity</div></div>
          <div class="fin-stat"><div class="fin-stat-value">${fmtNum(bond.chronScore)}</div><div class="fin-stat-label">Chron Score</div></div>
          <div class="fin-stat"><div class="fin-stat-value">${fmtNum(bond.sqftBacking)} ft²</div><div class="fin-stat-label">Square Footage Backing</div></div>
        </div>
        <div style="font-size:0.75rem;color:rgba(245,240,232,0.4);margin-top:0.5rem">
          Formula: (${fmtNum(sqft)} sqft × ${fmtNum(access)} hrs) × (1 + ${((perm + cat + pol) / 3).toFixed(2)} significance) = ${fmtNum(bond.chronScore)} ·
          Permanence: ${perm} · Catalyst: ${cat} · Policy: ${pol}
        </div>
      </div>
    `;
  });

  /* ═══ PANEL D: CAPITAL MARKETS ═══ */
  const panelCapMarkets = wrap.querySelector('#panel-capmarkets');

  function renderCapMarkets() {
    const contracts = buildSettlementContracts();
    const senior = priceBondCapMarkets(contracts, 'senior');
    const mezz = priceBondCapMarkets(contracts, 'mezzanine');
    const equity = priceBondCapMarkets(contracts, 'equity');

    // Stress tests
    const stressResults = {};
    for (const [scenario, haircut] of Object.entries(STRESS_SCENARIOS)) {
      const stressed = stressTest(contracts, scenario);
      stressResults[scenario] = {
        senior: priceBondCapMarkets(stressed, 'senior'),
        mezzanine: priceBondCapMarkets(stressed, 'mezzanine'),
        equity: priceBondCapMarkets(stressed, 'equity')
      };
    }

    panelCapMarkets.innerHTML = `
      <div class="fin-card">
        <div class="fin-card-title">Prevention-Backed Securities</div>
        <div class="fin-card-subtitle">Settlement contracts pooled from ${contracts.length} DUOMO profiles · PAYOUT_RATIO = 70% · Structured into 3 tranches</div>
      </div>

      <div class="fin-card">
        <div class="fin-card-title">Settlement Contracts</div>
        <div class="fin-table-wrap">
          <table class="fin-table">
            <thead><tr><th>Person</th><th>Intervention</th><th>Expected Savings</th><th>P(Success)</th><th>Weighted Value</th></tr></thead>
            <tbody>
              ${contracts.map(c => {
                const total = Object.values(c.expectedSavings).reduce((a, b) => a + b, 0);
                return `<tr>
                  <td style="font-weight:600">${c.person}</td>
                  <td style="font-size:0.78rem;color:rgba(245,240,232,0.6)">${c.intervention}</td>
                  <td>
                    <div style="font-family:'SF Mono',Consolas,monospace">${fmt(total)}</div>
                    <div style="font-size:0.68rem;color:rgba(245,240,232,0.35)">
                      ${Object.entries(c.expectedSavings).map(([k, v]) => k + ': ' + fmt(v)).join(' · ')}
                    </div>
                  </td>
                  <td style="font-family:'SF Mono',Consolas,monospace">${(c.probability * 100).toFixed(0)}%</td>
                  <td style="font-family:'SF Mono',Consolas,monospace;color:#c9a84c">${fmt(total * c.probability)}</td>
                </tr>`;
              }).join('')}
            </tbody>
          </table>
        </div>
      </div>

      <div class="fin-card">
        <div class="fin-card-title">Structured Product — 3-Tranche Waterfall</div>
        <div class="fin-tranche-stack">
          <div class="fin-tranche senior">
            <div class="fin-tranche-label">Senior Tranche (60% allocation · 0.4× risk)</div>
            <div class="fin-tranche-value">${fmt(senior.pool.totalNotional * 0.6)}</div>
            <div class="fin-tranche-detail">Yield: ${(senior.pool.coupon * 100).toFixed(2)}% · VaR₉₅: ${fmt(senior.var95)} · Expected CF: ${fmt(senior.expectedCF)}</div>
          </div>
          <div class="fin-tranche mezzanine">
            <div class="fin-tranche-label">Mezzanine Tranche (30% allocation · 1.0× risk)</div>
            <div class="fin-tranche-value">${fmt(mezz.pool.totalNotional * 0.3)}</div>
            <div class="fin-tranche-detail">Yield: ${(mezz.pool.coupon * 100).toFixed(2)}% · VaR₉₅: ${fmt(mezz.var95)} · Expected CF: ${fmt(mezz.expectedCF)}</div>
          </div>
          <div class="fin-tranche equity">
            <div class="fin-tranche-label">Equity Tranche (10% allocation · 1.8× risk)</div>
            <div class="fin-tranche-value">${fmt(equity.pool.totalNotional * 0.1)}</div>
            <div class="fin-tranche-detail">Yield: ${(equity.pool.coupon * 100).toFixed(2)}% · VaR₉₅: ${fmt(equity.var95)} · Expected CF: ${fmt(equity.expectedCF)}</div>
          </div>
        </div>
        <div class="fin-summary">
          <div class="fin-stat"><div class="fin-stat-value">${fmt(mezz.pool.totalNotional)}</div><div class="fin-stat-label">Total Notional</div></div>
          <div class="fin-stat"><div class="fin-stat-value">${(mezz.pool.baseYield * 100).toFixed(2)}%</div><div class="fin-stat-label">Base Yield</div></div>
          <div class="fin-stat"><div class="fin-stat-value">${(mezz.defaultProb * 100).toFixed(4)}%</div><div class="fin-stat-label">Full Default Probability</div></div>
          <div class="fin-stat"><div class="fin-stat-value">${contracts.length}</div><div class="fin-stat-label">Contracts Pooled</div></div>
        </div>
      </div>

      <div class="fin-card">
        <div class="fin-card-title">Stress Scenarios</div>
        <div class="fin-card-subtitle">Success rates adjusted: Recession −30%, Moderate −15%, Baseline 0%</div>
        <div class="fin-table-wrap">
          <table class="fin-table">
            <thead><tr><th>Scenario</th><th>Tranche</th><th>Notional</th><th>Coupon</th><th>VaR₉₅</th><th>Expected Return</th></tr></thead>
            <tbody>
              ${Object.entries(stressResults).map(([scenario, tranches]) => {
                return ['senior', 'mezzanine', 'equity'].map((t, i) => {
                  const tr = tranches[t];
                  const alloc = t === 'senior' ? 0.6 : t === 'mezzanine' ? 0.3 : 0.1;
                  return `<tr>
                    ${i === 0 ? `<td rowspan="3" style="font-weight:600;text-transform:capitalize;vertical-align:middle">${scenario}<br><span style="font-size:0.68rem;color:rgba(245,240,232,0.35)">−${(STRESS_SCENARIOS[scenario] * 100).toFixed(0)}%</span></td>` : ''}
                    <td style="text-transform:capitalize">${t}</td>
                    <td style="font-family:'SF Mono',Consolas,monospace">${fmt(tr.pool.totalNotional * alloc)}</td>
                    <td style="font-family:'SF Mono',Consolas,monospace">${(tr.pool.coupon * 100).toFixed(2)}%</td>
                    <td style="font-family:'SF Mono',Consolas,monospace;color:${tr.var95 > 30000 ? '#ef5350' : '#c9a84c'}">${fmt(tr.var95)}</td>
                    <td style="font-family:'SF Mono',Consolas,monospace;color:${tr.expectedReturn >= 0 ? '#4caf50' : '#ef5350'}">${fmt(tr.expectedReturn)}</td>
                  </tr>`;
                }).join('');
              }).join('')}
            </tbody>
          </table>
        </div>
      </div>
    `;
  }
  renderCapMarkets();

  /* ═══ PANEL E: COORDINATION MODEL SCORING ═══ */
  const panelCoord = wrap.querySelector('#panel-coordination');
  panelCoord.innerHTML = `
    <div class="fin-card">
      <div class="fin-card-title">Coordination Model Scoring</div>
      <div class="fin-card-subtitle">
        Score 10 architect models by coverage, budget fit, political alignment, and timeline ·
        Also computes baths-engine fit: overlap × 0.6 + savings × 0.4 − cost_penalty
      </div>
      <div class="fin-card-subtitle" style="margin-top:0.25rem">Select target domains:</div>
      <div id="coordDomains" style="display:flex;flex-wrap:wrap;gap:0.5rem;margin-bottom:1rem">
        ${Object.keys(DOMAIN_WEIGHTS).map(d => `
          <label style="display:flex;align-items:center;gap:0.35rem;font-size:0.8rem;color:rgba(245,240,232,0.6);cursor:pointer">
            <input type="checkbox" value="${d}" ${['health', 'housing', 'income'].includes(d) ? 'checked' : ''} style="accent-color:#c9a84c">
            ${d.replace(/_/g, ' ')} <span style="font-size:0.65rem;color:rgba(245,240,232,0.3)">(${DOMAIN_WEIGHTS[d]})</span>
          </label>
        `).join('')}
      </div>
      <div class="fin-form-grid">
        <div class="fin-field"><label>Political Context</label>
          <select id="coordPolitical">
            <option value="supportive">Supportive</option>
            <option value="neutral" selected>Neutral</option>
            <option value="resistant">Resistant</option>
            <option value="hostile">Hostile</option>
          </select>
        </div>
        <div class="fin-field"><label>Annual Budget ($)</label><input type="number" id="coordBudget" value="10000000" min="0" step="1000000"></div>
        <div class="fin-field"><label>Time Horizon</label>
          <select id="coordHorizon">
            <option value="1yr">1 Year</option>
            <option value="3yr" selected>3 Years</option>
            <option value="5yr">5 Years</option>
          </select>
        </div>
      </div>
      <button class="fin-btn primary" id="coordCalc">Score All Models</button>
    </div>
    <div id="coordResults" style="display:none">
      <div class="fin-card" id="coordRanking"></div>
      <div class="fin-card">
        <div class="fin-card-title">Budget Breakdown Template</div>
        <div class="fin-card-subtitle">Standard allocation for annual coordination budget</div>
        <div id="coordBudgetBreakdown"></div>
      </div>
    </div>
  `;

  panelCoord.querySelector('#coordCalc').addEventListener('click', () => {
    const targetDomains = Array.from(panelCoord.querySelectorAll('#coordDomains input:checked')).map(cb => cb.value);
    const political = panelCoord.querySelector('#coordPolitical').value;
    const budget = parseInt(panelCoord.querySelector('#coordBudget').value) || 10000000;
    const horizon = panelCoord.querySelector('#coordHorizon').value;

    if (targetDomains.length === 0) {
      panelCoord.querySelector('#coordResults').style.display = 'block';
      panelCoord.querySelector('#coordRanking').innerHTML = '<div style="color:rgba(245,240,232,0.5);padding:1rem">Please select at least one target domain.</div>';
      return;
    }

    // Score all architect models
    const scored = ARCHITECT_MODELS.map(m => {
      const archScore = scoreArchitectModel(m, targetDomains, political, budget, horizon);
      // Also compute baths-engine fit
      const bathsFit = scoreBathsCoordination({
        domains: m.domains,
        savings: m.abbr === 'ACO' ? 20 : m.abbr === 'MCO' ? 18 : m.abbr === 'PACE' ? 22 : m.abbr === 'SIB' ? 25 : 15,
        cost: m.budget.max > 1e8 ? 'high' : m.budget.max > 1e7 ? 'medium' : 'low'
      }, targetDomains);
      return { ...m, score: archScore, bathsFit };
    });

    scored.sort((a, b) => b.score.composite - a.score.composite);

    panelCoord.querySelector('#coordResults').style.display = 'block';
    panelCoord.querySelector('#coordRanking').innerHTML = `
      <div class="fin-card-title">Ranked Models (${scored.length})</div>
      <div class="fin-card-subtitle">Target domains: ${targetDomains.join(', ')} · Context: ${political} · Budget: ${fmt(budget)} · Horizon: ${horizon}</div>
      <div class="fin-table-wrap">
        <table class="fin-table">
          <thead><tr><th>#</th><th>Model</th><th>Category</th><th>Coverage</th><th>Budget</th><th>Political</th><th>Timeline</th><th>Composite</th><th>BATHS Fit</th><th>Evidence</th></tr></thead>
          <tbody>
            ${scored.map((m, i) => {
              const s = m.score;
              const barColor = s.composite >= 0.7 ? '#4caf50' : s.composite >= 0.4 ? '#ffc107' : '#ef5350';
              return `<tr>
                <td style="font-weight:600;color:${i < 3 ? '#c9a84c' : 'rgba(245,240,232,0.4)'}">${i + 1}</td>
                <td>
                  <div style="font-weight:600">${m.abbr}</div>
                  <div style="font-size:0.7rem;color:rgba(245,240,232,0.4)">${m.name}</div>
                </td>
                <td style="font-size:0.75rem">${m.category.replace(/_/g, ' ')}</td>
                <td style="font-family:'SF Mono',Consolas,monospace">${(s.coverage * 100).toFixed(0)}%</td>
                <td style="font-family:'SF Mono',Consolas,monospace">${(s.budgetScore * 100).toFixed(0)}%</td>
                <td style="font-family:'SF Mono',Consolas,monospace">${(s.politicalAlignment * 100).toFixed(0)}%</td>
                <td style="font-family:'SF Mono',Consolas,monospace">${(s.timelineScore * 100).toFixed(0)}%</td>
                <td>
                  <div style="font-family:'SF Mono',Consolas,monospace;font-weight:700;color:${barColor}">${(s.composite * 100).toFixed(1)}%</div>
                  <div class="fin-score-bar" style="width:80px;margin-top:3px"><div class="fin-score-fill" style="width:${s.composite * 100}%;background:${barColor}"></div></div>
                </td>
                <td style="font-family:'SF Mono',Consolas,monospace">${(m.bathsFit * 100).toFixed(0)}%</td>
                <td><span class="fin-badge ${m.evidence === 'strong' ? 'fin-badge-green' : m.evidence === 'moderate' ? 'fin-badge-gold' : 'fin-badge-blue'}">${m.evidence}</span></td>
              </tr>`;
            }).join('')}
          </tbody>
        </table>
      </div>
    `;

    // Budget breakdown
    panelCoord.querySelector('#coordBudgetBreakdown').innerHTML = `
      <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(160px,1fr));gap:0.75rem">
        ${Object.entries(BUDGET_BREAKDOWN).map(([cat, pct]) => `
          <div class="fin-stat">
            <div class="fin-stat-value">${fmt(budget * pct)}</div>
            <div class="fin-stat-label">${cat.replace(/_/g, ' ')} (${(pct * 100).toFixed(0)}%)</div>
          </div>
        `).join('')}
      </div>
    `;
  });

  /* ═══ PANEL F: WRONG-POCKET ANALYSIS ═══ */
  const panelWP = wrap.querySelector('#panel-wrongpocket');
  let wpChart = null;

  function renderWrongPocket() {
    const categories = getWrongPocketData();
    const marcus = profiles.marcus || {};

    // Aggregate for chart
    const catSums = {};
    costPoints.forEach(cp => {
      if (!catSums[cp.category]) catSums[cp.category] = { total: 0, count: 0 };
      if (cp.unit === '$/year' || cp.unit === '$/month') {
        const annual = cp.unit === '$/month' ? cp.value * 12 : cp.value;
        catSums[cp.category].total += annual;
        catSums[cp.category].count += 1;
      }
    });

    const chartCats = Object.entries(catSums)
      .filter(([, v]) => v.count > 0)
      .sort((a, b) => (b[1].total / b[1].count) - (a[1].total / a[1].count));

    const fragCost = marcus.costFragmented || 87400;
    const coordCost = marcus.costCoordinated || 34200;
    const savings = marcus.delta || 53200;

    panelWP.innerHTML = `
      <div class="fin-card">
        <div class="fin-card-title">Wrong-Pocket Problem</div>
        <div class="fin-card-subtitle">
          When one agency pays for prevention but another reaps the savings · The fundamental coordination failure
        </div>
      </div>

      <div class="fin-card">
        <div class="fin-card-title">Case Study: Marcus Thompson</div>
        <div class="fin-card-subtitle">34, single father of 2, Kensington Philadelphia · ${(marcus.systems || []).length} government systems involved</div>
        <div class="fin-summary">
          <div class="fin-stat red"><div class="fin-stat-value">${fmt(fragCost)}</div><div class="fin-stat-label">Fragmented Annual Cost</div></div>
          <div class="fin-stat green"><div class="fin-stat-value">${fmt(coordCost)}</div><div class="fin-stat-label">Coordinated Annual Cost</div></div>
          <div class="fin-stat"><div class="fin-stat-value">${fmt(savings)}</div><div class="fin-stat-label">Coordination Savings (Δ)</div></div>
          <div class="fin-stat"><div class="fin-stat-value">${Math.round((savings / fragCost) * 100)}%</div><div class="fin-stat-label">Savings Rate</div></div>
        </div>
        <div style="font-size:0.8rem;color:rgba(245,240,232,0.5);margin-top:0.5rem;line-height:1.6">
          Marcus interacts with <strong style="color:#c9a84c">${(marcus.systems || []).length} systems</strong>:
          ${(marcus.systems || []).map(s => `<span class="fin-badge fin-badge-gold" style="margin:2px">${s}</span>`).join(' ')}
          <br>Each system budgets independently. No single payer captures the full savings from coordination.
          The county pays for shelter, Medicaid pays for ER visits, DOC pays for incarceration — all treating symptoms
          of the same root causes.
        </div>
      </div>

      <div class="fin-card">
        <div class="fin-card-title">Cost Landscape by Category</div>
        <div class="fin-card-subtitle">Average annual costs from ${costPoints.length} data points across U.S. systems</div>
        <div class="fin-chart-box"><canvas id="wpChart"></canvas></div>
      </div>

      <div class="fin-card">
        <div class="fin-card-title">All Cost Data Points (${costPoints.length})</div>
        <div class="fin-table-wrap">
          <table class="fin-table">
            <thead><tr><th>Category</th><th>Metric</th><th>Value</th><th>Unit</th><th>Source</th></tr></thead>
            <tbody>
              ${costPoints.map(cp => `
                <tr>
                  <td><span class="fin-badge fin-badge-gold">${cp.category}</span></td>
                  <td style="font-size:0.8rem">${cp.metric}</td>
                  <td style="font-family:'SF Mono',Consolas,monospace;color:#c9a84c">${typeof cp.value === 'number' ? (cp.value >= 1e6 ? fmt(cp.value) : '$' + cp.value.toLocaleString()) : cp.value}</td>
                  <td style="font-size:0.72rem;color:rgba(245,240,232,0.4)">${cp.unit}</td>
                  <td style="font-size:0.68rem;color:rgba(245,240,232,0.35);max-width:200px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">${cp.source || '—'}</td>
                </tr>
              `).join('')}
            </tbody>
          </table>
        </div>
      </div>

      <div class="fin-card">
        <div class="fin-card-title">Scale Projections</div>
        <div class="fin-card-subtitle">From individual to national — what coordination savings look like at scale</div>
        <div class="fin-summary">
          <div class="fin-stat"><div class="fin-stat-value">${fmt(savings)}</div><div class="fin-stat-label">Per Person (Marcus)</div></div>
          <div class="fin-stat"><div class="fin-stat-value">${fmt(savings * 10000)}</div><div class="fin-stat-label">City (10K complex cases)</div></div>
          <div class="fin-stat"><div class="fin-stat-value">${fmt(savings * 50000)}</div><div class="fin-stat-label">County (50K cases)</div></div>
          <div class="fin-stat"><div class="fin-stat-value">${fmt(savings * 500000)}</div><div class="fin-stat-label">State (500K cases)</div></div>
        </div>
        <div style="margin-top:1rem;padding:1rem;background:rgba(201,168,76,0.06);border-radius:6px;border-left:3px solid #c9a84c">
          <div style="font-size:0.9rem;font-weight:600;color:#c9a84c;margin-bottom:0.5rem">National Narrative</div>
          <div style="font-size:0.85rem;color:rgba(245,240,232,0.7);line-height:1.6">
            At <strong style="color:#c9a84c">$48,000 per person per year</strong> in fragmented costs across an estimated
            <strong>1.96 million</strong> high-need individuals, the annual cost of the wrong-pocket problem is approximately
            <strong style="color:#ef5350;font-size:1rem">$94 billion/year</strong>. Coordination could recover
            40% — <strong style="color:#4caf50">$37.6 billion</strong> in annual savings.
          </div>
        </div>
      </div>
    `;

    // Bar chart
    if (typeof Chart !== 'undefined') {
      const chartLabels = chartCats.map(([cat]) => cat.charAt(0).toUpperCase() + cat.slice(1));
      const chartValues = chartCats.map(([, v]) => Math.round(v.total / v.count));
      const colors = {
        healthcare: '#ef5350', incarceration: '#ff9800', shelter: '#ffc107',
        housing: '#42a5f5', justice: '#ab47bc', education: '#66bb6a',
        income: '#c9a84c', coordination: '#78909c', childcare: '#26c6da'
      };
      const chartColors = chartCats.map(([cat]) => colors[cat] || '#c9a84c');

      if (wpChart) wpChart.destroy();
      const ctx = panelWP.querySelector('#wpChart').getContext('2d');
      wpChart = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: chartLabels,
          datasets: [{
            label: 'Average Annual Cost',
            data: chartValues,
            backgroundColor: chartColors.map(c => c + '44'),
            borderColor: chartColors,
            borderWidth: 1
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: { legend: { display: false } },
          scales: {
            x: { ticks: { color: 'rgba(245,240,232,0.5)', font: { size: 10 } }, grid: { display: false } },
            y: { ticks: { color: 'rgba(245,240,232,0.35)', font: { size: 10 }, callback: v => fmt(v) }, grid: { color: 'rgba(201,168,76,0.06)' } }
          }
        }
      });
    }
  }
  renderWrongPocket();

  /* ═══ PANEL G: AGREEMENT GENERATOR ═══ */
  const panelAgree = wrap.querySelector('#panel-agreements');
  panelAgree.innerHTML = `
    <div class="fin-card">
      <div class="fin-card-title">Agreement Generator</div>
      <div class="fin-card-subtitle">
        7 core agreement templates · Auto-determination from barrier law or type ·
        Compliance validation framework
      </div>
    </div>

    <div class="fin-card">
      <div class="fin-card-title">Agreement Templates (${AGREEMENT_TEMPLATES.length})</div>
      <div id="agreeTemplates">
        ${AGREEMENT_TEMPLATES.map(t => `
          <div class="fin-agree-card" data-type="${t.type}">
            <div class="fin-agree-type">${t.type}</div>
            <div class="fin-agree-name">${t.name}</div>
            <div class="fin-agree-law">${t.laws}</div>
            <div style="font-size:0.75rem;color:rgba(245,240,232,0.5);margin-top:0.5rem">${t.desc}</div>
          </div>
        `).join('')}
      </div>
    </div>

    <div class="fin-card">
      <div class="fin-card-title">Gap-to-Agreement Resolver</div>
      <div class="fin-card-subtitle">Select a barrier law or type to auto-determine required agreement types</div>
      <div class="fin-form-grid">
        <div class="fin-field"><label>Barrier Law</label>
          <select id="agreeBarrierLaw">
            <option value="">— Select —</option>
            ${Object.keys(GAP_TO_AGREEMENT).map(k => `<option value="${k}">${k}</option>`).join('')}
          </select>
        </div>
        <div class="fin-field"><label>Barrier Type (fallback)</label>
          <select id="agreeBarrierType">
            <option value="">— Select —</option>
            ${Object.keys(BARRIER_TYPE_MAP).map(k => `<option value="${k}">${k}</option>`).join('')}
          </select>
        </div>
      </div>
      <button class="fin-btn primary" id="agreeResolve">Resolve Agreement Types</button>
      <div id="agreeResolveResult" style="margin-top:1rem;display:none"></div>
    </div>

    <div class="fin-card">
      <div class="fin-card-title">Mapping Reference</div>
      <div class="fin-card-subtitle">GAP_TO_AGREEMENT_MAP — barrier law → agreement types</div>
      <div class="fin-table-wrap">
        <table class="fin-table">
          <thead><tr><th>Barrier Law</th><th>Required Agreement Types</th></tr></thead>
          <tbody>
            ${Object.entries(GAP_TO_AGREEMENT).map(([law, types]) => `
              <tr>
                <td style="font-weight:600">${law}</td>
                <td>${types.map(t => `<span class="fin-badge fin-badge-gold" style="margin:2px">${t}</span>`).join(' ')}</td>
              </tr>
            `).join('')}
          </tbody>
        </table>
      </div>
      <div class="fin-card-subtitle" style="margin-top:1rem">BARRIER_TYPE_MAP — barrier type → agreement types (fallback)</div>
      <div class="fin-table-wrap">
        <table class="fin-table">
          <thead><tr><th>Barrier Type</th><th>Agreement Types</th></tr></thead>
          <tbody>
            ${Object.entries(BARRIER_TYPE_MAP).map(([type, types]) => `
              <tr>
                <td style="font-weight:600;text-transform:capitalize">${type}</td>
                <td>${types.map(t => `<span class="fin-badge fin-badge-blue" style="margin:2px">${t}</span>`).join(' ')}</td>
              </tr>
            `).join('')}
          </tbody>
        </table>
      </div>
    </div>

    <div class="fin-card">
      <div class="fin-card-title">Compliance Status Flow</div>
      <div style="display:flex;align-items:center;gap:1rem;flex-wrap:wrap;margin-top:0.5rem">
        <div style="display:flex;align-items:center;gap:0.5rem">
          <span class="fin-badge fin-badge-blue">DRAFT</span>
          <span style="color:rgba(245,240,232,0.3)">→</span>
          <span class="fin-badge fin-badge-gold">IN REVIEW</span>
          <span style="color:rgba(245,240,232,0.3)">→</span>
          <span class="fin-badge fin-badge-green">EXECUTED</span>
        </div>
      </div>
      <div style="font-size:0.75rem;color:rgba(245,240,232,0.4);margin-top:0.75rem;line-height:1.5">
        <strong>draft</strong> → in_review · <strong>in_review</strong> → executed or → draft ·
        <strong>executed</strong> → (terminal) ·
        Default state: <strong>Pennsylvania</strong> · Expiration: <strong>365 days</strong> from generation ·
        Compliance validated against all applicable ComplianceRule records
      </div>
    </div>
  `;

  // Resolve handler
  panelAgree.querySelector('#agreeResolve').addEventListener('click', () => {
    const law = panelAgree.querySelector('#agreeBarrierLaw').value;
    const type = panelAgree.querySelector('#agreeBarrierType').value;
    const types = determineAgreementTypes(law || null, type || null);
    const resultDiv = panelAgree.querySelector('#agreeResolveResult');
    resultDiv.style.display = 'block';

    const matchedTemplates = types.map(t => AGREEMENT_TEMPLATES.find(tmpl => tmpl.type === t)).filter(Boolean);

    resultDiv.innerHTML = `
      <div style="padding:1rem;background:rgba(201,168,76,0.06);border-radius:6px;border-left:3px solid #c9a84c">
        <div style="font-size:0.85rem;color:#c9a84c;font-weight:600;margin-bottom:0.5rem">
          Resolution: ${types.length} agreement type${types.length !== 1 ? 's' : ''} required
        </div>
        <div style="display:flex;flex-wrap:wrap;gap:0.5rem;margin-bottom:0.75rem">
          ${types.map(t => `<span class="fin-badge fin-badge-green">${t}</span>`).join('')}
        </div>
        ${law ? `<div style="font-size:0.75rem;color:rgba(245,240,232,0.5)">Matched via barrier law: <strong>${law}</strong></div>` : ''}
        ${!law && type ? `<div style="font-size:0.75rem;color:rgba(245,240,232,0.5)">Matched via barrier type fallback: <strong>${type}</strong></div>` : ''}
        ${!law && !type ? `<div style="font-size:0.75rem;color:rgba(245,240,232,0.5)">Ultimate fallback: MOU</div>` : ''}

        ${matchedTemplates.length > 0 ? `
          <div style="margin-top:1rem">
            ${matchedTemplates.map(t => `
              <div style="padding:0.5rem 0;border-top:1px solid rgba(201,168,76,0.08)">
                <div style="font-weight:600;font-size:0.85rem">${t.name} <span style="font-family:'SF Mono',Consolas,monospace;font-size:0.72rem;color:rgba(245,240,232,0.4)">${t.type}</span></div>
                <div style="font-size:0.72rem;color:rgba(245,240,232,0.4)">${t.laws}</div>
                <div style="font-size:0.75rem;color:rgba(245,240,232,0.5);margin-top:0.25rem">${t.desc}</div>
              </div>
            `).join('')}
          </div>
        ` : ''}
      </div>
    `;

    // Highlight matching template cards
    panelAgree.querySelectorAll('.fin-agree-card').forEach(card => {
      card.classList.remove('selected');
      if (types.includes(card.dataset.type)) card.classList.add('selected');
    });
  });

  // Template card click to select barrier law
  panelAgree.querySelectorAll('.fin-agree-card').forEach(card => {
    card.addEventListener('click', () => {
      panelAgree.querySelectorAll('.fin-agree-card').forEach(c => c.classList.remove('selected'));
      card.classList.add('selected');
    });
  });

  /* ═══ LAZY PANEL INIT — Cliff Guard auto-render on first tab click ═══ */
  // Listen for tab changes to render cliff guard chart on demand
  const cliffTab = wrap.querySelector('.fin-tab[data-tab="cliff"]');
  if (cliffTab) {
    cliffTab.addEventListener('click', () => {
      // Auto-run if not yet run
      if (!panelCliff.querySelector('#cliffResults')?.style.display || panelCliff.querySelector('#cliffResults').style.display === 'none') {
        // Set Marcus defaults
        const marcusP = profiles.marcus;
        if (marcusP) {
          panelCliff.querySelector('#cliffIncome').value = marcusP.income || 22880;
          if (marcusP.benefits) {
            Object.entries(PHASE_OUTS).forEach(([k]) => {
              const inp = panelCliff.querySelector('#cliff-' + k);
              if (inp && marcusP.benefits[k] != null) inp.value = marcusP.benefits[k];
            });
          }
        }
        runCliffGuard();
      }
    });
  }

  /* ═══ ADDITIONAL: Phase-Out Schedule Table (append to cliff panel) ═══ */
  function renderPhaseOutTable() {
    const existingTable = panelCliff.querySelector('#phaseOutTableCard');
    if (existingTable) return;

    const card = document.createElement('div');
    card.className = 'fin-card';
    card.id = 'phaseOutTableCard';
    card.innerHTML = `
      <div class="fin-card-title">Program Phase-Out Schedules</div>
      <div class="fin-card-subtitle">Linear interpolation: floor → full benefit, ceiling → $0</div>
      <div class="fin-table-wrap">
        <table class="fin-table">
          <thead>
            <tr>
              <th>Program</th>
              <th>Phase-Out Floor</th>
              <th>Phase-Out Ceiling</th>
              <th>Full Benefit</th>
              <th>Phase-Out Range</th>
              <th>Reduction Rate</th>
            </tr>
          </thead>
          <tbody>
            ${Object.entries(PHASE_OUTS).map(([key, prog]) => {
              const range = prog.ceiling - prog.floor;
              const ratePerK = (prog.base / range) * 1000;
              return `<tr>
                <td style="font-weight:600">${prog.label}</td>
                <td style="font-family:'SF Mono',Consolas,monospace">${fmt(prog.floor)}</td>
                <td style="font-family:'SF Mono',Consolas,monospace">${fmt(prog.ceiling)}</td>
                <td style="font-family:'SF Mono',Consolas,monospace;color:#c9a84c">${fmt(prog.base)}/yr</td>
                <td style="font-family:'SF Mono',Consolas,monospace">${fmt(range)}</td>
                <td style="font-size:0.75rem;color:rgba(245,240,232,0.5)">−$${Math.round(ratePerK)}/yr per $1K earned</td>
              </tr>`;
            }).join('')}
          </tbody>
        </table>
      </div>
      <div style="margin-top:0.75rem;font-size:0.75rem;color:rgba(245,240,232,0.4);line-height:1.5">
        <strong>Formula:</strong> If income ≤ floor → full benefit. If income ≥ ceiling → $0.
        Otherwise: benefit = base × (ceiling − income) / (ceiling − floor).
        <br><strong>EMTR:</strong> Simulated from current income to max(3× current, $150K) in $500 steps.
        Cliff zone = any income range where EMTR exceeds 50%.
      </div>
    `;
    panelCliff.querySelector('#cliffResults').appendChild(card);
  }

  // Hook phase-out table to cliff calc
  const origCliffCalc = panelCliff.querySelector('#cliffCalc');
  if (origCliffCalc) {
    origCliffCalc.addEventListener('click', () => {
      setTimeout(renderPhaseOutTable, 50);
    });
  }

  /* ═══ ADDITIONAL: Coordination Models Detail Cards ═══ */
  function renderCoordModelDetails() {
    const detailContainer = document.createElement('div');
    detailContainer.className = 'fin-card';
    detailContainer.innerHTML = `
      <div class="fin-card-title">All 10 Architect Models — Reference</div>
      <div class="fin-card-subtitle">From domes-architect · Each model has budget range, timeline, evidence base, and target populations</div>
      <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:0.75rem;margin-top:1rem">
        ${ARCHITECT_MODELS.map((m, i) => {
          const evidColor = m.evidence === 'strong' ? '#4caf50' : m.evidence === 'moderate' ? '#ffc107' : '#42a5f5';
          return `
            <div style="background:rgba(201,168,76,0.04);border:1px solid rgba(201,168,76,0.12);border-radius:6px;padding:1rem">
              <div style="display:flex;justify-content:space-between;align-items:flex-start">
                <div>
                  <div style="font-family:'SF Mono',Consolas,monospace;font-size:0.72rem;color:#c9a84c">#${m.id} — ${m.abbr}</div>
                  <div style="font-weight:600;font-size:0.9rem;margin-top:0.15rem">${m.name}</div>
                </div>
                <span class="fin-badge" style="background:${evidColor}22;color:${evidColor}">${m.evidence}</span>
              </div>
              <div style="margin-top:0.5rem;font-size:0.75rem;color:rgba(245,240,232,0.5)">
                <div><strong>Category:</strong> ${m.category.replace(/_/g, ' ')}</div>
                <div><strong>Budget:</strong> ${fmt(m.budget.min)} – ${fmt(m.budget.max)}/yr</div>
                <div><strong>Timeline:</strong> ${m.timeline}</div>
                <div><strong>Political:</strong> ${m.political}</div>
                <div style="margin-top:0.35rem"><strong>Domains:</strong>
                  ${m.domains.map(d => `<span class="fin-badge fin-badge-gold" style="margin:1px;font-size:0.62rem">${d.replace(/_/g, ' ')}</span>`).join('')}
                </div>
                <div style="margin-top:0.35rem"><strong>Populations:</strong>
                  ${(m.population || []).map(p => `<span class="fin-badge fin-badge-blue" style="margin:1px;font-size:0.62rem">${p.replace(/_/g, ' ')}</span>`).join('')}
                </div>
              </div>
            </div>
          `;
        }).join('')}
      </div>
    `;

    // Add to coordination panel if not already present
    const existing = panelCoord.querySelector('#coordModelDetails');
    if (existing) existing.remove();
    detailContainer.id = 'coordModelDetails';
    panelCoord.appendChild(detailContainer);
  }
  renderCoordModelDetails();

  /* ═══ ADDITIONAL: Domain Weight Reference ═══ */
  const domainWeightRef = document.createElement('div');
  domainWeightRef.className = 'fin-card';
  domainWeightRef.innerHTML = `
    <div class="fin-card-title">Domain Weight Reference</div>
    <div class="fin-card-subtitle">How important each domain is in coordination scoring</div>
    <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(140px,1fr));gap:0.5rem;margin-top:0.75rem">
      ${Object.entries(DOMAIN_WEIGHTS).map(([d, w]) => {
        const pct = w * 100;
        const barColor = w >= 0.8 ? '#4caf50' : w >= 0.6 ? '#ffc107' : '#ff9800';
        return `
          <div style="text-align:center">
            <div style="font-size:0.75rem;color:rgba(245,240,232,0.5);margin-bottom:0.3rem">${d.replace(/_/g, ' ')}</div>
            <div class="fin-score-bar" style="margin-bottom:0.2rem"><div class="fin-score-fill" style="width:${pct}%;background:${barColor}"></div></div>
            <div style="font-family:'SF Mono',Consolas,monospace;font-size:0.8rem;color:${barColor}">${w.toFixed(1)}</div>
          </div>
        `;
      }).join('')}
    </div>
    <div style="margin-top:1rem">
      <div class="fin-card-subtitle">Context Alignment Matrix</div>
      <div class="fin-table-wrap">
        <table class="fin-table">
          <thead><tr><th>Context \\ Feasibility</th><th>High</th><th>Moderate</th><th>Low</th><th>Contentious</th></tr></thead>
          <tbody>
            ${Object.entries(CONTEXT_ALIGNMENT).map(([ctx, scores]) => `
              <tr>
                <td style="font-weight:600;text-transform:capitalize">${ctx}</td>
                ${['high','moderate','low','contentious'].map(f => {
                  const v = scores[f];
                  const c = v >= 0.7 ? '#4caf50' : v >= 0.4 ? '#ffc107' : '#ef5350';
                  return `<td style="font-family:'SF Mono',Consolas,monospace;color:${c}">${v.toFixed(1)}</td>`;
                }).join('')}
              </tr>
            `).join('')}
          </tbody>
        </table>
      </div>
    </div>
  `;
  panelCoord.appendChild(domainWeightRef);

  /* ═══ ADDITIONAL: BATHS Coordination Models from data.js ═══ */
  if (coordModels.length > 0) {
    const bathsModelsCard = document.createElement('div');
    bathsModelsCard.className = 'fin-card';
    bathsModelsCard.innerHTML = `
      <div class="fin-card-title">BATHS Coordination Models (${coordModels.length})</div>
      <div class="fin-card-subtitle">From baths-engine/backend/data/coordination.py · score = overlap × 0.6 + savings_score × 0.4 − cost_penalty</div>
      <div class="fin-table-wrap">
        <table class="fin-table">
          <thead><tr><th>Model</th><th>Est. Savings</th><th>Cost</th><th>Timeline</th><th>Legal Authority</th><th>Key Barrier</th></tr></thead>
          <tbody>
            ${coordModels.map(m => `
              <tr>
                <td style="font-weight:600">${m.name}</td>
                <td style="font-family:'SF Mono',Consolas,monospace;color:#4caf50">${m.savings}%</td>
                <td><span class="fin-badge ${m.cost === 'low' ? 'fin-badge-green' : m.cost === 'medium' ? 'fin-badge-gold' : 'fin-badge-red'}">${m.cost}</span></td>
                <td style="font-size:0.78rem">${m.timeline}</td>
                <td style="font-size:0.68rem;color:rgba(245,240,232,0.4);max-width:180px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">${m.authority || '—'}</td>
                <td style="font-size:0.68rem;color:rgba(245,240,232,0.4);max-width:200px">${m.barrier || '—'}</td>
              </tr>
            `).join('')}
          </tbody>
        </table>
      </div>
    `;
    panelCoord.appendChild(bathsModelsCard);
  }

  /* ═══ ADDITIONAL: DomeBond Rating Scale Reference (Bond Panel) ═══ */
  const bondRatingRef = document.createElement('div');
  bondRatingRef.className = 'fin-card';
  bondRatingRef.innerHTML = `
    <div class="fin-card-title">Bond Rating Reference</div>
    <div class="fin-card-subtitle">Rating thresholds for DUOMO and THAUMA bonds</div>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:1rem;margin-top:0.75rem">
      <div>
        <div style="font-size:0.8rem;font-weight:600;color:#c9a84c;margin-bottom:0.5rem">DUOMO Bond (DomeBond)</div>
        <div class="fin-table-wrap">
          <table class="fin-table">
            <thead><tr><th>Rating</th><th>Min Cosm</th><th>Coupon</th></tr></thead>
            <tbody>
              <tr><td><span class="fin-badge fin-badge-green">AAA</span></td><td>≥ 80</td><td>3.5%</td></tr>
              <tr><td><span class="fin-badge fin-badge-green">AA</span></td><td>≥ 60</td><td>4.0–4.5%</td></tr>
              <tr><td><span class="fin-badge fin-badge-gold">A</span></td><td>≥ 40</td><td>4.5–5.5%</td></tr>
              <tr><td><span class="fin-badge fin-badge-gold">BBB</span></td><td>≥ 20</td><td>5.5–6.5%</td></tr>
              <tr><td><span class="fin-badge fin-badge-red">B</span></td><td>< 20</td><td>8.0%</td></tr>
            </tbody>
          </table>
        </div>
        <div style="font-size:0.72rem;color:rgba(245,240,232,0.4);margin-top:0.5rem">
          Face value = coordination savings (Δ) · Cosm = min(all 6 dimensions) · Weakest-link principle
        </div>
      </div>
      <div>
        <div style="font-size:0.8rem;font-weight:600;color:#c9a84c;margin-bottom:0.5rem">THAUMA Bond (ChronBond)</div>
        <div class="fin-table-wrap">
          <table class="fin-table">
            <thead><tr><th>Rating</th><th>Criteria</th><th>Coupon</th></tr></thead>
            <tbody>
              <tr><td><span class="fin-badge fin-badge-green">AAA</span></td><td>perm ≥ 0.8 AND policy ≥ 0.5</td><td>4.0%</td></tr>
              <tr><td><span class="fin-badge fin-badge-green">AA</span></td><td>perm ≥ 0.6</td><td>5.0%</td></tr>
              <tr><td><span class="fin-badge fin-badge-gold">A</span></td><td>perm ≥ 0.4</td><td>6.0%</td></tr>
              <tr><td><span class="fin-badge fin-badge-gold">BBB</span></td><td>else</td><td>7.0%</td></tr>
            </tbody>
          </table>
        </div>
        <div style="font-size:0.72rem;color:rgba(245,240,232,0.4);margin-top:0.5rem">
          Face value = economic impact = chronScore × 0.5 · ChronScore = (sqft × hrs) × (1 + significance)
        </div>
      </div>
    </div>
  `;
  panelBonds.appendChild(bondRatingRef);

  /* ═══ ADDITIONAL: Bond Comparison Across All Profiles ═══ */
  const bondCompCard = document.createElement('div');
  bondCompCard.className = 'fin-card';
  const allBonds = Object.entries(profiles).map(([key, p]) => {
    const delta = p.delta || 0;
    const cosm = key === 'robert' ? 18 : key === 'marcus' ? 42 : key === 'james' ? 55 : key === 'sarah' ? 62 : key === 'maria' ? 48 : 35;
    const bond = priceDomeBond(delta, cosm, (p.systems || []).length, 7);
    return { key, name: p.name || key, ...bond };
  });

  bondCompCard.innerHTML = `
    <div class="fin-card-title">DUOMO Bond Comparison — All Profiles</div>
    <div class="fin-table-wrap">
      <table class="fin-table">
        <thead><tr><th>Profile</th><th>Rating</th><th>Face Value</th><th>Coupon</th><th>Annual Coupon</th><th>YTM</th><th>Cosm</th><th>Programs</th></tr></thead>
        <tbody>
          ${allBonds.map(b => {
            const rColor = b.rating === 'AAA' ? '#4caf50' : b.rating === 'AA' ? '#8bc34a' : b.rating === 'A' ? '#ffc107' : b.rating === 'BBB' ? '#ff9800' : '#ef5350';
            return `<tr>
              <td style="font-weight:600">${b.name}</td>
              <td><span class="fin-badge" style="background:${rColor}22;color:${rColor}">${b.rating}</span></td>
              <td style="font-family:'SF Mono',Consolas,monospace">${fmt(b.faceValue)}</td>
              <td style="font-family:'SF Mono',Consolas,monospace">${(b.couponRate * 100).toFixed(1)}%</td>
              <td style="font-family:'SF Mono',Consolas,monospace;color:#c9a84c">${fmt(b.annualCoupon)}</td>
              <td style="font-family:'SF Mono',Consolas,monospace">${(b.ytm * 100).toFixed(2)}%</td>
              <td>${b.cosmScore}</td>
              <td>${b.programsBacking}</td>
            </tr>`;
          }).join('')}
        </tbody>
      </table>
    </div>
  `;
  panelBonds.appendChild(bondCompCard);

  /* ═══ ADDITIONAL: THAUMA Bond Comparison — All Episodes ═══ */
  if (episodes.length > 0) {
    const chronCompCard = document.createElement('div');
    chronCompCard.className = 'fin-card';
    const allChron = episodes.slice(0, 10).map(ep => {
      const sqft = ep.served ? Math.round(ep.served * 1.5) : 20000;
      const perm = (ep.permanence || 70) / 100;
      const cat = 0.6;
      const pol = perm > 0.7 ? 0.5 : 0.3;
      const bond = priceChronBond(sqft, 2000, perm, cat, pol, 10);
      return { title: ep.title, location: ep.location, ...bond };
    });

    chronCompCard.innerHTML = `
      <div class="fin-card-title">THAUMA Bond Comparison — Season 1 Episodes</div>
      <div class="fin-table-wrap">
        <table class="fin-table">
          <thead><tr><th>Episode</th><th>Rating</th><th>Face Value</th><th>Chron Score</th><th>Coupon</th><th>Annual</th><th>Permanence</th></tr></thead>
          <tbody>
            ${allChron.map(b => {
              const rColor = b.rating === 'AAA' ? '#4caf50' : b.rating === 'AA' ? '#8bc34a' : b.rating === 'A' ? '#ffc107' : '#ff9800';
              return `<tr>
                <td>
                  <div style="font-weight:600;font-size:0.85rem">${b.title}</div>
                  <div style="font-size:0.68rem;color:rgba(245,240,232,0.35)">${b.location}</div>
                </td>
                <td><span class="fin-badge" style="background:${rColor}22;color:${rColor}">${b.rating}</span></td>
                <td style="font-family:'SF Mono',Consolas,monospace">${fmt(b.faceValue)}</td>
                <td style="font-family:'SF Mono',Consolas,monospace">${fmtNum(b.chronScore)}</td>
                <td style="font-family:'SF Mono',Consolas,monospace">${(b.couponRate * 100).toFixed(1)}%</td>
                <td style="font-family:'SF Mono',Consolas,monospace;color:#c9a84c">${fmt(b.annualCoupon)}</td>
                <td style="font-family:'SF Mono',Consolas,monospace">${b.permanence.toFixed(2)}</td>
              </tr>`;
            }).join('')}
          </tbody>
        </table>
      </div>
    `;
    panelBonds.appendChild(chronCompCard);
  }

  /* ═══ ADDITIONAL: Eligibility Quick-Compare All Archetypes ═══ */
  const archCompCard = document.createElement('div');
  archCompCard.className = 'fin-card';
  const archResults = Object.entries(ARCHETYPES).map(([key, a]) => {
    const progs = calculateEligibility(a.income, a.household, a.age, a.children, a.disabled);
    const costs = calculateCosts(progs);
    return { key, ...a, ...costs };
  });

  archCompCard.innerHTML = `
    <div class="fin-card-title">Archetype Comparison — All 6 Profiles</div>
    <div class="fin-card-subtitle">Quick eligibility + cost comparison across all Cosm archetypes</div>
    <div class="fin-table-wrap">
      <table class="fin-table">
        <thead><tr><th>Archetype</th><th>Income</th><th>HH</th><th>Age</th><th>Children</th><th>FPL %</th><th>Eligible</th><th>Benefits</th><th>Fragmented</th><th>Coordinated</th><th>Δ Savings</th></tr></thead>
        <tbody>
          ${archResults.map(a => {
            const fplPct = Math.round(a.income / fpl(a.household) * 100);
            return `<tr>
              <td style="font-weight:600;font-size:0.8rem">${a.label.split(' — ')[0]}</td>
              <td style="font-family:'SF Mono',Consolas,monospace">${fmt(a.income)}</td>
              <td>${a.household}</td>
              <td>${a.age}</td>
              <td>${a.children}</td>
              <td style="font-family:'SF Mono',Consolas,monospace;color:${fplPct <= 130 ? '#ef5350' : fplPct <= 200 ? '#ffc107' : '#4caf50'}">${fplPct}%</td>
              <td style="font-family:'SF Mono',Consolas,monospace;color:#c9a84c">${a.eligible}/${a.total}</td>
              <td style="font-family:'SF Mono',Consolas,monospace">${fmt(a.totalBenefits)}</td>
              <td style="font-family:'SF Mono',Consolas,monospace;color:#ef5350">${fmt(a.fragmented)}</td>
              <td style="font-family:'SF Mono',Consolas,monospace;color:#4caf50">${fmt(a.coordinated)}</td>
              <td style="font-family:'SF Mono',Consolas,monospace;font-weight:700;color:#c9a84c">${fmt(a.delta)}</td>
            </tr>`;
          }).join('')}
        </tbody>
      </table>
    </div>
  `;
  panelEligibility.querySelector('#eligResults').appendChild(archCompCard);

  /* ═══ ADDITIONAL: FPL Reference Table ═══ */
  const fplRef = document.createElement('div');
  fplRef.className = 'fin-card';
  fplRef.innerHTML = `
    <div class="fin-card-title">Federal Poverty Level Reference (2024)</div>
    <div class="fin-card-subtitle">FPL(n) = $15,060 + $5,380 × (n − 1) · Key thresholds for all programs</div>
    <div class="fin-table-wrap">
      <table class="fin-table">
        <thead><tr><th>HH Size</th><th>100% FPL</th><th>130% FPL</th><th>138% FPL</th><th>150% FPL</th><th>185% FPL</th><th>250% FPL</th><th>50% AMI</th></tr></thead>
        <tbody>
          ${[1,2,3,4,5].map(n => {
            const f = fpl(n);
            return `<tr>
              <td style="font-weight:600">${n}</td>
              <td style="font-family:'SF Mono',Consolas,monospace">${fmt(f)}</td>
              <td style="font-family:'SF Mono',Consolas,monospace">${fmt(Math.round(f * 1.30))}</td>
              <td style="font-family:'SF Mono',Consolas,monospace">${fmt(Math.round(f * 1.38))}</td>
              <td style="font-family:'SF Mono',Consolas,monospace">${fmt(Math.round(f * 1.50))}</td>
              <td style="font-family:'SF Mono',Consolas,monospace">${fmt(Math.round(f * 1.85))}</td>
              <td style="font-family:'SF Mono',Consolas,monospace">${fmt(Math.round(f * 2.50))}</td>
              <td style="font-family:'SF Mono',Consolas,monospace;color:rgba(245,240,232,0.4)">${fmt(Math.round(AREA_MEDIAN_INCOME * 0.50))}</td>
            </tr>`;
          }).join('')}
        </tbody>
      </table>
    </div>
    <div style="font-size:0.72rem;color:rgba(245,240,232,0.35);margin-top:0.5rem">
      AMI (Area Median Income) = ${fmt(AREA_MEDIAN_INCOME)} (Philadelphia) · Programs using AMI: Section 8 HCV
    </div>
  `;
  panelEligibility.appendChild(fplRef);

  /* ═══ ADDITIONAL: EITC & SNAP Reference ═══ */
  const eitcSnapRef = document.createElement('div');
  eitcSnapRef.className = 'fin-card';
  eitcSnapRef.innerHTML = `
    <div class="fin-card-title">EITC & SNAP — Detailed Reference</div>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:1rem;margin-top:0.75rem">
      <div>
        <div style="font-size:0.85rem;font-weight:600;color:#c9a84c;margin-bottom:0.5rem">EITC Income Limits & Max Credits</div>
        <div class="fin-table-wrap">
          <table class="fin-table">
            <thead><tr><th># Children</th><th>Income Limit</th><th>Max Credit</th><th>Engine (60%)</th></tr></thead>
            <tbody>
              ${[0,1,2,3].map(n => `
                <tr>
                  <td>${n}</td>
                  <td style="font-family:'SF Mono',Consolas,monospace">${fmt(EITC_LIMITS[n])}</td>
                  <td style="font-family:'SF Mono',Consolas,monospace">${fmt(EITC_MAX[n])}</td>
                  <td style="font-family:'SF Mono',Consolas,monospace;color:#c9a84c">${fmt(Math.round(EITC_MAX[n] * 0.60))}</td>
                </tr>
              `).join('')}
            </tbody>
          </table>
        </div>
      </div>
      <div>
        <div style="font-size:0.85rem;font-weight:600;color:#c9a84c;margin-bottom:0.5rem">SNAP Max Monthly by Household</div>
        <div class="fin-table-wrap">
          <table class="fin-table">
            <thead><tr><th>HH Size</th><th>Max Monthly</th><th>Engine (70%)</th><th>Annual (70%)</th></tr></thead>
            <tbody>
              ${Object.entries(SNAP_MAX_MONTHLY).map(([n, v]) => `
                <tr>
                  <td>${n}</td>
                  <td style="font-family:'SF Mono',Consolas,monospace">${fmt(v)}/mo</td>
                  <td style="font-family:'SF Mono',Consolas,monospace">${fmt(Math.round(v * 0.70))}/mo</td>
                  <td style="font-family:'SF Mono',Consolas,monospace;color:#c9a84c">${fmt(Math.round(v * 0.70 * 12))}/yr</td>
                </tr>
              `).join('')}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  `;
  panelEligibility.appendChild(eitcSnapRef);

  /* ═══ ADDITIONAL: Wrong-Pocket Payer Matrix ═══ */
  const wpPayerMatrix = document.createElement('div');
  wpPayerMatrix.className = 'fin-card';
  wpPayerMatrix.innerHTML = `
    <div class="fin-card-title">Who Pays vs. Who Saves — The Wrong-Pocket Matrix</div>
    <div class="fin-card-subtitle">The fundamental coordination failure: the entity that invests in prevention is not the entity that captures the savings</div>
    <div class="fin-table-wrap">
      <table class="fin-table">
        <thead><tr><th>Intervention</th><th>Who Pays</th><th>Who Saves</th><th>Annual Savings</th><th>Wrong Pocket?</th></tr></thead>
        <tbody>
          <tr>
            <td>Permanent Supportive Housing</td>
            <td>HUD / Local Housing Auth</td>
            <td>Medicaid (ER), Criminal Justice (jail), Shelter System</td>
            <td style="font-family:'SF Mono',Consolas,monospace;color:#4caf50">$12,000–$35,000/person</td>
            <td><span class="fin-badge fin-badge-red">YES</span></td>
          </tr>
          <tr>
            <td>Substance Use Treatment</td>
            <td>Behavioral Health Dept</td>
            <td>Medicaid (ER), DOC (incarceration), Employers</td>
            <td style="font-family:'SF Mono',Consolas,monospace;color:#4caf50">$15,000–$45,000/person</td>
            <td><span class="fin-badge fin-badge-red">YES</span></td>
          </tr>
          <tr>
            <td>Early Childhood Education</td>
            <td>Dept of Education</td>
            <td>Criminal Justice (long-term), Employers, Tax Revenue</td>
            <td style="font-family:'SF Mono',Consolas,monospace;color:#4caf50">$7,000–$12,000/child/yr</td>
            <td><span class="fin-badge fin-badge-red">YES</span></td>
          </tr>
          <tr>
            <td>Care Coordination Hub</td>
            <td>Medicaid MCO / County</td>
            <td>All payers (reduced duplication, ER diversion)</td>
            <td style="font-family:'SF Mono',Consolas,monospace;color:#4caf50">$8,000–$20,000/person</td>
            <td><span class="fin-badge fin-badge-gold">PARTIAL</span></td>
          </tr>
          <tr>
            <td>Job Training / Workforce Dev</td>
            <td>DOL / WIOA</td>
            <td>SNAP (reduced), Tax Revenue (increased), Employers</td>
            <td style="font-family:'SF Mono',Consolas,monospace;color:#4caf50">$4,000–$15,000/person</td>
            <td><span class="fin-badge fin-badge-red">YES</span></td>
          </tr>
          <tr>
            <td>Preventive Healthcare</td>
            <td>Medicaid / Marketplace</td>
            <td>Same payer (Medicaid) + Employers (productivity)</td>
            <td style="font-family:'SF Mono',Consolas,monospace;color:#4caf50">$3,000–$8,000/person</td>
            <td><span class="fin-badge fin-badge-green">ALIGNED</span></td>
          </tr>
        </tbody>
      </table>
    </div>
    <div style="margin-top:0.75rem;padding:0.75rem;background:rgba(244,67,54,0.06);border-radius:6px;border-left:3px solid #ef5350;font-size:0.8rem;color:rgba(245,240,232,0.6);line-height:1.6">
      <strong style="color:#ef5350">The Core Problem:</strong> Government budgets are organized by agency (vertical silos), but human needs cut across agencies (horizontal reality).
      Prevention investments often flow to one pocket while savings accrue to another. This misalignment creates a rational bias toward crisis response over prevention.
      <br><strong style="color:#c9a84c">BATHS Solution:</strong> Prevention-backed securities (DomeBonds) pool cross-agency savings and distribute them back to investors proportionally,
      creating aligned incentives for prevention investment.
    </div>
  `;
  panelWP.appendChild(wpPayerMatrix);

  /* ═══ ADDITIONAL: Capital Markets — Payout Ratio & Constants Reference ═══ */
  const capConstRef = document.createElement('div');
  capConstRef.className = 'fin-card';
  capConstRef.innerHTML = `
    <div class="fin-card-title">Capital Markets — Constants & Formulas</div>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:1rem;margin-top:0.75rem">
      <div>
        <div style="font-size:0.85rem;font-weight:600;color:#c9a84c;margin-bottom:0.5rem">Tranche Parameters</div>
        <div class="fin-table-wrap">
          <table class="fin-table">
            <thead><tr><th>Tranche</th><th>Yield Mult</th><th>Risk Mult</th><th>Allocation</th></tr></thead>
            <tbody>
              <tr><td style="font-weight:600">Senior</td><td>0.6×</td><td>0.4×</td><td>60%</td></tr>
              <tr><td style="font-weight:600">Mezzanine</td><td>1.0×</td><td>1.0×</td><td>30%</td></tr>
              <tr><td style="font-weight:600">Equity</td><td>1.5×</td><td>1.8×</td><td>10%</td></tr>
            </tbody>
          </table>
        </div>
      </div>
      <div>
        <div style="font-size:0.85rem;font-weight:600;color:#c9a84c;margin-bottom:0.5rem">Key Constants</div>
        <div style="font-size:0.8rem;color:rgba(245,240,232,0.6);line-height:2">
          <div><strong>PAYOUT_RATIO:</strong> <span style="font-family:'SF Mono',Consolas,monospace;color:#c9a84c">0.70</span> (70% of verified savings → coupon)</div>
          <div><strong>VaR Confidence:</strong> <span style="font-family:'SF Mono',Consolas,monospace;color:#c9a84c">95%</span> (z = 1.645)</div>
          <div><strong>Discount Rate:</strong> <span style="font-family:'SF Mono',Consolas,monospace;color:#c9a84c">5%</span></div>
          <div><strong>Default Prob:</strong> <span style="font-family:'SF Mono',Consolas,monospace">∏(1 − p_i)</span> for all contracts</div>
        </div>
      </div>
    </div>
    <div style="margin-top:1rem;font-size:0.75rem;color:rgba(245,240,232,0.4);line-height:1.6">
      <strong>pool_contracts():</strong> total_notional = Σ(savings × probability) · base_yield = weighted_yield / total_notional · coupon = yield × 0.70<br>
      <strong>price_bond():</strong> expected_cf = Σ(p × savings / (1+r)^t) · VaR₉₅ = 1.645 × √(variance) × risk_mult · default_prob = ∏(1 − p_i)<br>
      <strong>Stress:</strong> Recession = −30% success rates · Moderate = −15% · Baseline = 0%
    </div>
  `;
  panelCapMarkets.appendChild(capConstRef);

}; // end window.renderFinance
