/* ═══════════════════════════════════════════════════════════════════
   BREAKDOWN.JS — Domain Drill-Down View
   ───────────────────────────────────────────────────────────────────
   Left panel: domain selector cards. Right panel: detail with
   systems table, provisions, gaps, bridges, and cost chart.
   ═══════════════════════════════════════════════════════════════════ */
window.renderBreakdown = (function () {
  "use strict";

  var DATA = window.DUOMO_DATA;
  var container = document.getElementById("view-breakdown");
  var activeDomainIdx = 0;
  var chartInstance = null;

  function fmt(n) { return DATA.formatCurrencyFull(n); }

  function renderDomainSelector(profile) {
    var html = "";
    profile.domains.forEach(function (d, i) {
      var color = DATA.getDomainColor(d.domain);
      var activeClass = i === activeDomainIdx ? " active" : "";
      html += '<div class="domain-card' + activeClass + '" data-idx="' + i + '" style="border-left: 3px solid ' + color + ';">';
      html += '<div class="dc-name" style="color:' + color + ';">' + d.label + "</div>";
      html += '<div class="dc-stats">' + fmt(d.annual_cost) + " \u00B7 " + d.systems.length + " sys \u00B7 " + (d.gaps ? d.gaps.length : 0) + " gaps</div>";
      html += "</div>";
    });
    return html;
  }

  function renderDomainDetail(domain) {
    var color = DATA.getDomainColor(domain.domain);
    var html = "";

    /* Systems table */
    html += '<h3 class="section-heading" style="color:' + color + ';">Systems</h3>';
    html += '<table class="data-table"><thead><tr>';
    html += "<th>ID</th><th>Label</th><th>Annual Cost</th><th>Coord Savings</th><th>Status</th>";
    html += "</tr></thead><tbody>";
    domain.systems.forEach(function (sys) {
      var savAmt = Math.round(sys.annual_cost * sys.coord_savings_pct);
      html += "<tr>";
      html += '<td><code class="mono" style="font-size:0.7rem; color:' + color + ';">' + sys.id + "</code></td>";
      html += "<td>" + sys.label + "</td>";
      html += '<td class="cost-cell">' + fmt(sys.annual_cost) + "</td>";
      html += '<td class="cost-cell" style="color:#2ecc71;">' + Math.round(sys.coord_savings_pct * 100) + "% (" + fmt(savAmt) + ")</td>";
      html += "<td><span class=\"severity-badge low\">Active</span></td>";
      html += "</tr>";
    });
    html += "</tbody></table>";

    /* Provisions */
    if (domain.provisions && domain.provisions.length) {
      html += '<h3 class="section-heading" style="margin-top:1.5rem; color:' + color + ';">Provisions</h3>';
      domain.provisions.forEach(function (prov) {
        html += '<div class="provision-card">';
        html += '<div class="prov-title"><span class="type-badge ' + prov.type + '">' + prov.type + "</span> " + prov.title + "</div>";
        html += '<div class="prov-relevance">' + prov.relevance + "</div>";
        html += "</div>";
      });
    }

    /* Gaps */
    if (domain.gaps && domain.gaps.length) {
      html += '<h3 class="section-heading" style="margin-top:1.5rem;">Gaps</h3>';
      domain.gaps.forEach(function (gap) {
        html += '<div class="gap-card">';
        html += '<div class="gap-label"><span class="severity-badge ' + gap.severity + '">' + gap.severity + "</span> " + gap.label + "</div>";
        html += '<div class="gap-impact">' + gap.impact + "</div>";
        html += "</div>";
      });
    }

    /* Bridges */
    if (domain.bridges && domain.bridges.length) {
      html += '<h3 class="section-heading" style="margin-top:1.5rem;">Bridges</h3>';
      domain.bridges.forEach(function (br) {
        html += '<div class="bridge-card">';
        html += '<div class="bridge-label"><span class="type-badge ' + br.type + '">' + br.type + '</span> <span class="severity-badge ' + (br.impact === "high" ? "high" : "medium") + '">' + br.impact + "</span> " + br.label + "</div>";
        html += '<div class="bridge-desc">' + br.description + "</div>";
        html += "</div>";
      });
    }

    /* Cost chart container */
    html += '<div class="domain-chart-container">';
    html += '<h3 class="section-heading" style="margin-top:1.5rem; color:' + color + ';">Cost Comparison</h3>';
    html += '<canvas id="domainCostChart" height="200"></canvas>';
    html += "</div>";

    return html;
  }

  function renderChart(domain) {
    if (chartInstance) { chartInstance.destroy(); }
    var canvas = document.getElementById("domainCostChart");
    if (!canvas) return;
    var ctx = canvas.getContext("2d");
    var color = DATA.getDomainColor(domain.domain);
    chartInstance = new Chart(ctx, {
      type: "bar",
      data: {
        labels: ["Fragmented", "Coordinated"],
        datasets: [{
          data: [domain.annual_cost, domain.coordinated_cost],
          backgroundColor: ["rgba(231,76,60,0.5)", "rgba(46,204,113,0.5)"],
          borderColor: ["#e74c3c", "#2ecc71"],
          borderWidth: 1,
          borderRadius: 4
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { display: false } },
        scales: {
          y: {
            beginAtZero: true,
            grid: { color: "rgba(245,240,232,0.05)" },
            ticks: { color: "rgba(245,240,232,0.4)", callback: function (v) { return "$" + (v / 1000).toFixed(0) + "K"; }, font: { family: "monospace", size: 10 } }
          },
          x: {
            grid: { display: false },
            ticks: { color: "rgba(245,240,232,0.6)", font: { size: 11 } }
          }
        }
      }
    });
  }

  function render(profile) {
    if (activeDomainIdx >= profile.domains.length) { activeDomainIdx = 0; }
    var domain = profile.domains[activeDomainIdx];

    var html = '<div class="breakdown-layout">';
    html += '<div class="domain-selector" id="domainSelector">' + renderDomainSelector(profile) + "</div>";
    html += '<div class="domain-detail">' + renderDomainDetail(domain) + "</div>";
    html += "</div>";
    container.innerHTML = html;

    /* Bind domain card clicks */
    var cards = document.querySelectorAll("#domainSelector .domain-card");
    cards.forEach(function (card) {
      card.addEventListener("click", function () {
        activeDomainIdx = parseInt(card.dataset.idx, 10);
        render(profile);
      });
    });

    /* Render chart after DOM update */
    setTimeout(function () { renderChart(domain); }, 50);
  }

  return render;
})();
