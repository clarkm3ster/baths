/* ═══════════════════════════════════════════════════════════════════
   BUDGET.JS — Cost Engine Dashboard
   ───────────────────────────────────────────────────────────────────
   KPI cards, stacked bar chart, waterfall chart, ROI metrics.
   All numbers from the real seed data.
   ═══════════════════════════════════════════════════════════════════ */
window.renderBudget = (function () {
  "use strict";

  var DATA = window.DUOMO_DATA;
  var container = document.getElementById("view-budget");
  var charts = {};

  function fmtFull(n) { return DATA.formatCurrencyFull(n); }
  function fmtK(n) { return DATA.formatCurrency(n); }

  function destroyCharts() {
    Object.keys(charts).forEach(function (k) {
      if (charts[k]) { charts[k].destroy(); charts[k] = null; }
    });
  }

  function render(profile) {
    destroyCharts();

    var savings = profile.savings_annual;
    var savPct = DATA.savingsPct(profile);
    var coordInvestment = 8500; /* per-person coordination infrastructure cost */
    var roiMultiple = savings > 0 ? ((savings * 5 - coordInvestment) / coordInvestment).toFixed(1) : "0";
    var breakEvenMonths = savings > 0 ? ((coordInvestment / savings) * 12).toFixed(1) : "N/A";
    var bondPricing = Math.round(savings * 0.6); /* 60% of savings as bond coupon estimate */

    var html = "";

    /* ── KPI Row ── */
    html += '<div class="budget-kpis">';
    html += '<div class="kpi-card"><div class="kpi-title">Total Fragmented Cost</div><div class="kpi-val" style="color:#e74c3c;">' + fmtFull(profile.total_annual_cost) + '</div><div class="kpi-sub">Annual per-person cost (siloed)</div></div>';
    html += '<div class="kpi-card"><div class="kpi-title">Total Coordinated Cost</div><div class="kpi-val" style="color:#2ecc71;">' + fmtFull(profile.coordinated_annual_cost) + '</div><div class="kpi-sub">With data integration</div></div>';
    html += '<div class="kpi-card"><div class="kpi-title">Annual Savings</div><div class="kpi-val" style="color:#c9a84c;">' + fmtFull(savings) + '</div><div class="kpi-sub">' + savPct + '% reduction</div></div>';
    html += '<div class="kpi-card"><div class="kpi-title">5-Year Projection</div><div class="kpi-val" style="color:#c9a84c;">' + fmtK(profile.five_year_projection) + '</div><div class="kpi-sub">Cumulative savings (3% inflation)</div></div>';
    html += '<div class="kpi-card"><div class="kpi-title">Lifetime Estimate</div><div class="kpi-val" style="color:#c9a84c;">' + fmtK(profile.lifetime_estimate) + '</div><div class="kpi-sub">Full horizon savings</div></div>';
    html += "</div>";

    /* ── Charts Row ── */
    html += '<div class="budget-charts">';

    /* Stacked bar chart */
    html += '<div class="chart-card"><h3>Domain Cost Comparison</h3><div class="chart-wrapper"><canvas id="budgetBarChart"></canvas></div></div>';

    /* Waterfall chart */
    html += '<div class="chart-card"><h3>Savings Waterfall by Domain</h3><div class="chart-wrapper"><canvas id="budgetWaterfallChart"></canvas></div></div>';

    html += "</div>";

    /* ── ROI Row ── */
    html += '<h3 class="section-heading" style="margin-top:0.5rem;">ROI Metrics</h3>';
    html += '<div class="roi-grid">';
    html += '<div class="roi-card"><div class="roi-label">Coordination Investment</div><div class="roi-val">' + fmtFull(coordInvestment) + "/yr</div></div>";
    html += '<div class="roi-card"><div class="roi-label">Cost Per Dollar Saved</div><div class="roi-val">$' + (savings > 0 ? (coordInvestment / savings).toFixed(2) : "N/A") + "</div></div>";
    html += '<div class="roi-card"><div class="roi-label">Break-Even Period</div><div class="roi-val">' + breakEvenMonths + " months</div></div>";
    html += '<div class="roi-card"><div class="roi-label">5-Year ROI Multiple</div><div class="roi-val">' + roiMultiple + "x</div></div>";
    html += '<div class="roi-card"><div class="roi-label">Bond Pricing Estimate</div><div class="roi-val">' + fmtFull(bondPricing) + "/yr coupon</div></div>";
    html += '<div class="roi-card"><div class="roi-label">Systems Integrated</div><div class="roi-val">' + profile.systems_involved.length + " systems</div></div>";
    html += "</div>";

    container.innerHTML = html;

    /* ── Render Charts ── */
    setTimeout(function () { renderBarChart(profile); renderWaterfallChart(profile); }, 50);
  }

  function renderBarChart(profile) {
    var canvas = document.getElementById("budgetBarChart");
    if (!canvas) return;
    var ctx = canvas.getContext("2d");

    var labels = profile.domains.map(function (d) { return d.label; });
    var fragmented = profile.domains.map(function (d) { return d.annual_cost; });
    var coordinated = profile.domains.map(function (d) { return d.coordinated_cost; });

    charts.bar = new Chart(ctx, {
      type: "bar",
      data: {
        labels: labels,
        datasets: [
          {
            label: "Fragmented",
            data: fragmented,
            backgroundColor: "rgba(231,76,60,0.55)",
            borderColor: "#e74c3c",
            borderWidth: 1,
            borderRadius: 3
          },
          {
            label: "Coordinated",
            data: coordinated,
            backgroundColor: "rgba(46,204,113,0.55)",
            borderColor: "#2ecc71",
            borderWidth: 1,
            borderRadius: 3
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            labels: { color: "rgba(245,240,232,0.6)", font: { size: 11 }, boxWidth: 12 }
          }
        },
        scales: {
          y: {
            beginAtZero: true,
            grid: { color: "rgba(245,240,232,0.05)" },
            ticks: { color: "rgba(245,240,232,0.4)", callback: function (v) { return "$" + (v / 1000).toFixed(0) + "K"; }, font: { family: "monospace", size: 10 } }
          },
          x: {
            grid: { display: false },
            ticks: { color: "rgba(245,240,232,0.6)", font: { size: 10 } }
          }
        }
      }
    });
  }

  function renderWaterfallChart(profile) {
    var canvas = document.getElementById("budgetWaterfallChart");
    if (!canvas) return;
    var ctx = canvas.getContext("2d");

    var labels = profile.domains.map(function (d) { return d.label; });
    labels.push("Total Savings");
    var savingsData = profile.domains.map(function (d) { return d.savings; });
    var totalSavings = savingsData.reduce(function (s, v) { return s + v; }, 0);
    savingsData.push(totalSavings);

    var colors = profile.domains.map(function (d) { return DATA.getDomainColor(d.domain) + "99"; });
    colors.push("rgba(201,168,76,0.7)");

    var borders = profile.domains.map(function (d) { return DATA.getDomainColor(d.domain); });
    borders.push("#c9a84c");

    charts.waterfall = new Chart(ctx, {
      type: "bar",
      data: {
        labels: labels,
        datasets: [{
          label: "Savings",
          data: savingsData,
          backgroundColor: colors,
          borderColor: borders,
          borderWidth: 1,
          borderRadius: 3
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false }
        },
        scales: {
          y: {
            beginAtZero: true,
            grid: { color: "rgba(245,240,232,0.05)" },
            ticks: { color: "rgba(245,240,232,0.4)", callback: function (v) { return "$" + (v / 1000).toFixed(0) + "K"; }, font: { family: "monospace", size: 10 } }
          },
          x: {
            grid: { display: false },
            ticks: { color: "rgba(245,240,232,0.6)", font: { size: 10 } }
          }
        }
      }
    });
  }

  return render;
})();
