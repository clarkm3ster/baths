/* ═══════════════════════════════════════════════════════════════════
   SLATE.JS — Apollo Slate Wrapper
   ───────────────────────────────────────────────────────────────────
   Wraps the shared stripboard.js engine with the DUOMO config
   (biometric green theme, featuring Marcus + Sarah columns).
   ═══════════════════════════════════════════════════════════════════ */
window.renderSlateView = (function () {
  "use strict";

  var container = document.getElementById("view-slate");
  var rendered = false;

  function render() {
    if (rendered) return;

    var mount = document.createElement("div");
    mount.id = "slate-container";
    container.innerHTML = "";
    container.appendChild(mount);

    var config = {
      themeColor: "#2ecc71",
      title: "The First 10 Connectomes \u2014 DUOMO Production Slate",
      thesis: "Each column represents one human being whose life is fragmented across disconnected government data systems. The DUOMO (Digital Unified Operational Model for Outcomes) maps every system, gap, and bridge \u2014 turning a person\u2019s bureaucratic maze into a coordinated production.",
      quote: "A person is not a case number. A person is a production \u2014 and every production deserves a script, a schedule, and a crew that can see the whole picture.",
      manifesto: "The BATHS framework treats each human connectome as a production slate. The first 10 profiles demonstrate what coordination looks like when government systems stop operating in silos. DUOMO is the operating system for that coordination.",
      budgetColor: "#c9a84c",
      columns: [
        {
          id: "DUOMO-001",
          title: "Marcus Thompson",
          budget: "$87,400 \u2192 $34,200 (\u221253K)",
          thesis: "Reentry case spanning 10 systems across 4 domains. Fragmentation is the primary barrier to recovery.",
          events: [
            { time: "DOC", title: "State Prison Release (6 months ago)", desc: "3-year sentence for non-violent drug offense. Release plan not shared with community providers.", tags: [{ label: "JUSTICE", color: "#8B1A1A" }] },
            { time: "BHA", title: "SUD Treatment Engagement", desc: "Active in substance use treatment through Medicaid BHA. Progress not visible to probation officer.", tags: [{ label: "HEALTH", color: "#1A6B3C" }] },
            { time: "HMIS", title: "Emergency Shelter Cycling", desc: "Rotating between shelters. Intake does not capture BH treatment status or Medicaid enrollment.", tags: [{ label: "HOUSING", color: "#1A3D8B" }] },
            { time: "SNAP", title: "Benefits Active", desc: "Receiving SNAP. Employment services not linked to probation compliance.", tags: [{ label: "INCOME", color: "#6B5A1A" }] },
            { time: "GAP", title: "42 CFR Part 2 Consent Needed", desc: "One consent form could bridge BH records to probation. Not yet signed.", tags: [{ label: "BRIDGE", color: "#2ecc71" }] }
          ]
        },
        {
          id: "DUOMO-002",
          title: "Sarah Chen",
          budget: "$72,200 \u2192 $29,100 (\u221243K)",
          thesis: "DV survivor racing the 15-month reunification clock across 7 systems.",
          events: [
            { time: "SACWIS", title: "Child in Kinship Care", desc: "Daughter placed with Sarah\u2019s sister. SACWIS cannot verify housing progress.", tags: [{ label: "CHILD WF", color: "#1A6B6B" }] },
            { time: "PHA", title: "Section 8 Voucher Active", desc: "Active voucher but no landlord will accept it. PHA has no link to reunification timeline.", tags: [{ label: "HOUSING", color: "#1A3D8B" }] },
            { time: "COURT", title: "Family Court Case", desc: "Reunification case active. Judge cannot see real-time service completion data.", tags: [{ label: "JUSTICE", color: "#8B1A1A" }] },
            { time: "TANF", title: "Benefits & DV Waiver", desc: "TANF work requirements not linked to DV safety planning.", tags: [{ label: "INCOME", color: "#6B5A1A" }] },
            { time: "MCO", title: "Trauma-Informed Care", desc: "Medicaid MCO unaware of DV history. Standard session limits inadequate for trauma recovery.", tags: [{ label: "HEALTH", color: "#1A6B3C" }] }
          ]
        }
      ]
    };

    if (typeof window.renderStripboard === "function") {
      window.renderStripboard(mount, config);
    } else {
      mount.innerHTML = '<p style="color:rgba(245,240,232,0.5); font-style:italic;">Stripboard engine not loaded. Ensure stripboard.js is included.</p>';
    }

    rendered = true;
  }

  return render;
})();
