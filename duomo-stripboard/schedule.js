/* ═══════════════════════════════════════════════════════════════════
   SCHEDULE.JS — Day Out of Days Calendar
   ───────────────────────────────────────────────────────────────────
   12-month grid. Rows = systems, Columns = months.
   Cell states: ● Active, ◐ Partial, ○ Pending, ✕ Gap/Blocked.
   ═══════════════════════════════════════════════════════════════════ */
window.renderSchedule = (function () {
  "use strict";

  var DATA = window.DUOMO_DATA;
  var container = document.getElementById("view-schedule");
  var MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
  var SYMBOLS = { active: "\u25CF", partial: "\u25D0", pending: "\u25CB", gap: "\u2715" };
  var LABELS = { active: "Active engagement", partial: "Partial / transitioning", pending: "Pending / scheduled", gap: "Gap / blocked" };

  /* Generate realistic engagement patterns based on system and domain */
  function generatePattern(sysId, domain) {
    var patterns = {
      /* Health systems — generally continuous */
      medicaid:    ["active","active","active","active","active","active","active","active","active","active","active","active"],
      bha:         ["active","active","active","partial","active","active","active","active","partial","active","active","active"],
      mco:         ["active","active","active","active","active","active","active","active","active","active","active","active"],
      hie:         ["pending","pending","partial","active","active","active","active","active","active","active","active","active"],
      pdmp:        ["active","active","active","active","active","active","active","active","active","active","active","active"],
      er_frequent: ["active","active","active","active","active","partial","active","active","active","active","active","active"],
      va:          ["active","active","active","active","partial","active","active","active","active","active","partial","active"],
      /* Justice systems — often front-loaded or periodic */
      doc:         ["active","active","partial","partial","pending","pending","pending","pending","pending","pending","pending","pending"],
      probation:   ["active","active","active","active","active","active","active","active","active","active","active","active"],
      court_cms:   ["active","partial","gap","pending","active","partial","pending","pending","active","partial","pending","pending"],
      juvenile_court: ["active","active","active","partial","pending","active","active","partial","pending","pending","active","partial"],
      /* Housing systems */
      hmis:        ["active","active","active","active","active","active","active","active","active","active","active","active"],
      shelter:     ["active","active","active","active","partial","partial","active","active","active","partial","active","active"],
      pha:         ["pending","pending","partial","partial","active","active","active","active","active","active","active","active"],
      /* Income systems — periodic reviews */
      tanf:        ["active","active","active","active","active","active","partial","active","active","active","active","active"],
      snap:        ["active","active","active","active","active","active","active","active","active","active","active","active"],
      ssi:         ["active","active","active","active","active","active","active","active","active","active","active","partial"],
      ssdi:        ["active","active","active","active","active","active","active","active","active","active","active","active"],
      ssa:         ["active","active","active","partial","partial","active","active","active","active","active","active","active"],
      unemployment:["active","active","active","active","partial","partial","gap","pending","pending","active","active","active"],
      /* Education systems */
      iep:         ["active","active","active","active","active","gap","gap","active","active","active","active","active"],
      slds:        ["active","active","active","active","active","active","active","active","active","active","active","active"],
      /* Child welfare */
      sacwis:      ["active","active","active","active","active","active","active","active","active","active","active","active"],
      foster_care: ["active","active","active","active","active","active","active","active","active","active","active","active"]
    };
    return patterns[sysId] || ["pending","pending","pending","pending","pending","pending","pending","pending","pending","pending","pending","pending"];
  }

  function getPopoverText(sysId, month, state) {
    var label = DATA.systems[sysId] ? DATA.systems[sysId].label : sysId;
    var descriptions = {
      active: label + " — Active engagement in " + MONTHS[month] + ". Regular service delivery and monitoring.",
      partial: label + " — Transitioning in " + MONTHS[month] + ". Service level changing or under review.",
      pending: label + " — Pending in " + MONTHS[month] + ". Scheduled to begin or awaiting authorization.",
      gap: label + " — Blocked in " + MONTHS[month] + ". Service gap due to data fragmentation."
    };
    return descriptions[state] || "";
  }

  function render(profile) {
    var html = '<h2 class="section-heading" style="margin-bottom:0.5rem;">Day Out of Days</h2>';
    html += '<p style="font-size:0.72rem; color:rgba(245,240,232,0.4); margin-bottom:1rem;">12-month engagement timeline for ' + profile.name + " (" + profile.id + ")</p>";

    /* Legend */
    html += '<div style="display:flex; gap:1.25rem; margin-bottom:1rem; font-size:0.7rem; color:rgba(245,240,232,0.5);">';
    html += '<span><span style="color:#2ecc71;">' + SYMBOLS.active + '</span> Active</span>';
    html += '<span><span style="color:#c9a84c;">' + SYMBOLS.partial + '</span> Partial</span>';
    html += '<span><span style="color:rgba(245,240,232,0.3);">' + SYMBOLS.pending + '</span> Pending</span>';
    html += '<span><span style="color:#e74c3c;">' + SYMBOLS.gap + '</span> Gap</span>';
    html += "</div>";

    html += '<div class="schedule-grid"><table class="schedule-table"><thead><tr>';
    html += "<th>System</th>";
    MONTHS.forEach(function (m) { html += "<th>" + m + "</th>"; });
    html += "<th>Summary</th></tr></thead><tbody>";

    /* One row per system in the profile */
    profile.domains.forEach(function (domain) {
      var color = DATA.getDomainColor(domain.domain);
      domain.systems.forEach(function (sys) {
        var pattern = generatePattern(sys.id, domain.domain);
        var activeCount = pattern.filter(function (s) { return s === "active"; }).length;
        var estCost = Math.round(sys.annual_cost * (activeCount / 12));

        html += "<tr>";
        html += "<td><div class=\"schedule-system-name\"><span class=\"domain-badge\" style=\"background:" + color + "22; color:" + color + ";\"><span class=\"dot\" style=\"background:" + color + ";\"></span>" + domain.label + "</span> <span style=\"font-weight:600;\">" + sys.label + "</span></div></td>";

        pattern.forEach(function (state, mi) {
          var symbolColor = "#2ecc71";
          if (state === "partial") symbolColor = "#c9a84c";
          else if (state === "pending") symbolColor = "rgba(245,240,232,0.25)";
          else if (state === "gap") symbolColor = "#e74c3c";

          var popText = getPopoverText(sys.id, mi, state);
          html += '<td class="schedule-cell"><span class="cell-symbol" style="color:' + symbolColor + ';">' + SYMBOLS[state] + '</span>';
          html += '<div class="schedule-popover"><strong>' + MONTHS[mi] + "</strong><br>" + popText + "</div></td>";
        });

        html += "<td>" + activeCount + " mo \u00B7 " + DATA.formatCurrency(estCost) + "</td>";
        html += "</tr>";
      });
    });

    html += "</tbody></table></div>";
    container.innerHTML = html;
  }

  return render;
})();
