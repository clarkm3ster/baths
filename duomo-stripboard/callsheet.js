/* ═══════════════════════════════════════════════════════════════════
   CALLSHEET.JS — Today's Coordination Priorities
   ───────────────────────────────────────────────────────────────────
   Priority-sorted list of actions derived from profile gaps/bridges.
   Printable layout. Inspired by StudioBinder call sheets.
   ═══════════════════════════════════════════════════════════════════ */
window.renderCallSheet = (function () {
  "use strict";

  var DATA = window.DUOMO_DATA;
  var container = document.getElementById("view-callsheet");

  /* Generate realistic actions from gaps and bridges */
  function generateActions(profile) {
    var actions = [];
    var dayNum = Math.floor((Date.now() - new Date("2026-01-01").getTime()) / 86400000) + 1;

    /* Critical: from high-severity gaps */
    profile.domains.forEach(function (domain) {
      (domain.gaps || []).forEach(function (gap) {
        if (gap.severity === "high") {
          actions.push({
            priority: "critical",
            system: DATA.getDomainLabel(domain.domain) + " / " + domain.systems[0].label,
            desc: "Resolve: " + gap.label,
            party: "Care coordinator / Data integration team",
            deadline: "Immediate",
            status: "in-progress"
          });
        }
      });
    });

    /* High: from bridges with high impact */
    profile.domains.forEach(function (domain) {
      (domain.bridges || []).forEach(function (bridge) {
        if (bridge.impact === "high") {
          actions.push({
            priority: "high",
            system: DATA.getDomainLabel(domain.domain) + " / " + bridge.type,
            desc: "Implement: " + bridge.label,
            party: bridge.type === "consent" ? "Case worker / Client" : (bridge.type === "policy" ? "Policy coordinator" : "IT / Systems team"),
            deadline: bridge.type === "consent" ? "This week" : "30 days",
            status: bridge.type === "consent" ? "pending" : "pending"
          });
        }
      });
    });

    /* Standard: from medium gaps and lower bridges */
    profile.domains.forEach(function (domain) {
      (domain.gaps || []).forEach(function (gap) {
        if (gap.severity === "medium") {
          actions.push({
            priority: "standard",
            system: DATA.getDomainLabel(domain.domain),
            desc: "Monitor: " + gap.label,
            party: "Case manager",
            deadline: "Ongoing",
            status: "pending"
          });
        }
      });
      (domain.bridges || []).forEach(function (bridge) {
        if (bridge.impact === "medium") {
          actions.push({
            priority: "standard",
            system: DATA.getDomainLabel(domain.domain),
            desc: "Plan: " + bridge.label,
            party: bridge.type === "technical" ? "IT team" : "Policy team",
            deadline: "60 days",
            status: "pending"
          });
        }
      });
    });

    return actions;
  }

  function renderActionCard(action) {
    var html = '<div class="action-card">';
    html += "<div class=\"action-main\">";
    html += '<div class="action-system">' + action.system + "</div>";
    html += '<div class="action-desc">' + action.desc + "</div>";
    html += '<div class="action-party">\u2192 ' + action.party + "</div>";
    html += "</div>";
    html += '<div class="action-deadline">' + action.deadline + "</div>";
    html += '<div class="action-status ' + action.status + '">' + action.status.replace("-", " ") + "</div>";
    html += "</div>";
    return html;
  }

  function render(profile) {
    var today = new Date();
    var dayOfYear = Math.floor((today - new Date(today.getFullYear(), 0, 0)) / 86400000);
    var dateStr = today.toLocaleDateString("en-US", { weekday: "long", year: "numeric", month: "long", day: "numeric" });

    var actions = generateActions(profile);
    var critical = actions.filter(function (a) { return a.priority === "critical"; });
    var high = actions.filter(function (a) { return a.priority === "high"; });
    var standard = actions.filter(function (a) { return a.priority === "standard"; });

    var html = '<div class="callsheet-header">';
    html += "<h2>" + profile.name + "</h2>";
    html += '<span class="cs-date">' + dateStr + "</span>";
    html += '<span class="cs-day">Production Day ' + dayOfYear + " of 365</span>";
    html += "</div>";

    /* Critical */
    if (critical.length) {
      html += '<div class="priority-section">';
      html += '<div class="priority-label critical">Critical (' + critical.length + ")</div>";
      critical.forEach(function (a) { html += renderActionCard(a); });
      html += "</div>";
    }

    /* High */
    if (high.length) {
      html += '<div class="priority-section">';
      html += '<div class="priority-label high">High Priority (' + high.length + ")</div>";
      high.forEach(function (a) { html += renderActionCard(a); });
      html += "</div>";
    }

    /* Standard */
    if (standard.length) {
      html += '<div class="priority-section">';
      html += '<div class="priority-label standard">Standard (' + standard.length + ")</div>";
      standard.forEach(function (a) { html += renderActionCard(a); });
      html += "</div>";
    }

    /* Print button */
    html += '<div style="margin-top:1.5rem;"><button onclick="window.print()" style="background:var(--bg-surface); border:1px solid var(--border-gold); color:var(--gold); padding:0.5rem 1.25rem; border-radius:6px; cursor:pointer; font-size:0.75rem;">Print Call Sheet</button></div>';

    container.innerHTML = html;
  }

  return render;
})();
