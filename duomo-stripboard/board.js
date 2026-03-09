/* ═══════════════════════════════════════════════════════════════════
   BOARD.JS — Stripboard Kanban View
   ───────────────────────────────────────────────────────────────────
   Horizontal-scrolling stripboard. Each column = one life domain.
   Each strip = one system intervention. Gaps and bridges shown inline.
   ═══════════════════════════════════════════════════════════════════ */
window.renderBoard = (function () {
  "use strict";

  var DATA = window.DUOMO_DATA;
  var container = document.getElementById("view-board");
  var splitMode = false;

  function fmt(n) { return DATA.formatCurrencyFull(n); }
  function fmtK(n) { return DATA.formatCurrency(n); }
  function pct(savings, domain) { return domain.annual_cost > 0 ? Math.round((savings / domain.annual_cost) * 100) : 0; }

  function buildColumn(domain, tinted) {
    var color = DATA.getDomainColor(domain.domain);
    var gapCount = domain.gaps ? domain.gaps.length : 0;
    var bridgeCount = domain.bridges ? domain.bridges.length : 0;
    var tintClass = tinted === "red" ? " style=\"border-top: 3px solid rgba(231,76,60,0.6);\"" : (tinted === "green" ? " style=\"border-top: 3px solid rgba(46,204,113,0.6);\"" : " style=\"border-top: 3px solid " + color + ";\"");

    var html = '<div class="board-column"' + tintClass + ">";
    html += '<div class="board-col-header">';
    html += '<h3 style="color:' + color + ';">' + domain.label + "</h3>";
    html += '<div class="board-col-stats">';
    if (tinted === "green") {
      html += '<span>Cost: <span class="stat-val" style="color:#2ecc71;">' + fmtK(domain.coordinated_cost) + "</span></span>";
    } else {
      html += '<span>Cost: <span class="stat-val">' + fmtK(domain.annual_cost) + "</span></span>";
    }
    html += "<span>Sys: " + domain.systems.length + "</span>";
    html += "<span>Gaps: " + gapCount + "</span>";
    html += "</div></div>";

    html += '<div class="board-col-body">';

    /* System strips */
    domain.systems.forEach(function (sys) {
      var savingsAmt = Math.round(sys.annual_cost * sys.coord_savings_pct);
      var dispCost = tinted === "green" ? (sys.annual_cost - savingsAmt) : sys.annual_cost;
      html += '<div class="strip-card">';
      html += '<div class="strip-name">' + sys.label + "</div>";
      html += '<div class="strip-meta">';
      html += '<span class="strip-cost">' + fmt(dispCost) + "</span>";
      if (tinted !== "green" && tinted !== "red") {
        html += '<span class="strip-savings">\u2193' + Math.round(sys.coord_savings_pct * 100) + "%</span>";
      }
      html += "</div></div>";
    });

    /* Gap strips */
    if (!tinted || tinted === "red") {
      (domain.gaps || []).forEach(function (gap) {
        html += '<div class="strip-card gap-strip">';
        html += '<div class="strip-name">\u26A0 ' + gap.label + "</div>";
        html += "</div>";
      });
    }

    /* Bridge strips (only in default or coordinated) */
    if (!tinted || tinted === "green") {
      (domain.bridges || []).forEach(function (br) {
        html += '<div class="strip-card bridge-strip">';
        html += '<div class="strip-name">\u2794 ' + br.label + "</div>";
        html += "</div>";
      });
    }

    html += "</div>"; /* close board-col-body */
    html += "</div>"; /* close board-column */
    return html;
  }

  function render(profile) {
    var html = "";

    /* Controls */
    html += '<div class="board-controls">';
    html += '<button class="toggle-btn' + (splitMode ? " active" : "") + '" id="splitToggle">Split View</button>';
    html += '<span style="font-size:0.7rem; color:rgba(245,240,232,0.4);">' + profile.domains.length + " domains \u00B7 " + profile.systems_involved.length + " systems \u00B7 " + fmtK(profile.savings_annual) + " potential savings</span>";
    html += "</div>";

    if (splitMode) {
      /* Split view: Fragmented vs Coordinated */
      html += '<div class="split-view">';
      html += '<div class="split-panel fragmented"><h3>Fragmented (' + fmtK(profile.total_annual_cost) + "/yr)</h3>";
      html += '<div class="board-grid">';
      profile.domains.forEach(function (d) { html += buildColumn(d, "red"); });
      html += "</div></div>";
      html += '<div class="split-panel coordinated"><h3>Coordinated (' + fmtK(profile.coordinated_annual_cost) + "/yr)</h3>";
      html += '<div class="board-grid">';
      profile.domains.forEach(function (d) { html += buildColumn(d, "green"); });
      html += "</div></div>";
      html += "</div>";
    } else {
      /* Default: single board */
      html += '<div class="board-grid">';
      profile.domains.forEach(function (d) { html += buildColumn(d); });
      html += "</div>";
    }

    container.innerHTML = html;

    /* Bind split toggle */
    var btn = document.getElementById("splitToggle");
    if (btn) {
      btn.addEventListener("click", function () {
        splitMode = !splitMode;
        render(profile);
      });
    }
  }

  return render;
})();
