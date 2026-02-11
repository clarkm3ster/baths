import { useState, useRef, useEffect, useCallback } from "react";
import type { Architecture, Risk, Stakeholder, WorkforcePlan, AuthorityMap, Phase } from "../types";

interface Props {
  architectures: Architecture[];
}

const RISK_COLORS: Record<string, string> = {
  high: "#8B1A1A",
  moderate: "#6B5A1A",
  low: "#1A6B3C",
};

const LIKELIHOOD_ORDER: Record<string, number> = { low: 0, moderate: 1, high: 2 };
const IMPACT_ORDER: Record<string, number> = { low: 0, moderate: 1, high: 2 };

const RISK_CATEGORIES = [
  "political",
  "financial",
  "operational",
  "technical",
  "regulatory",
  "stakeholder",
  "community",
];

const INFLUENCE_COLORS: Record<string, string> = {
  high: "#8B1A1A",
  moderate: "#6B5A1A",
  low: "#1A6B3C",
};

const AUTHORITY_STATUS_COLORS: Record<string, string> = {
  required: "#8B1A1A",
  pending: "#6B5A1A",
  obtained: "#1A6B3C",
  in_progress: "#1A3D8B",
};

function riskSeverity(r: Risk): string {
  if (r.likelihood === "high" && r.impact === "high") return "high";
  if (r.likelihood === "low" && r.impact === "low") return "low";
  return "moderate";
}

export default function RiskDashboard({ architectures }: Props) {
  const [selectedId, setSelectedId] = useState<number | "">(
    architectures.length > 0 ? architectures[0].id : ""
  );
  const [expandedSection, setExpandedSection] = useState<string>("risks");

  const arch = architectures.find((a) => a.id === selectedId);
  const risks: Risk[] = arch?.risks ?? [];
  const stakeholders: Stakeholder[] = arch?.stakeholders ?? [];
  const workforce: WorkforcePlan | undefined = arch?.workforce_plan;
  const authority: AuthorityMap | undefined = arch?.authority_map;

  // Risk stats
  const highSeverity = risks.filter((r) => riskSeverity(r) === "high").length;
  const withMitigation = risks.filter((r) => r.mitigation && r.mitigation.length > 0).length;

  // Group risks by category
  const groupedRisks: Record<string, Risk[]> = {};
  for (const r of risks) {
    const cat = r.category.toLowerCase();
    if (!groupedRisks[cat]) groupedRisks[cat] = [];
    groupedRisks[cat].push(r);
  }

  const toggleSection = (section: string) => {
    setExpandedSection((prev) => (prev === section ? "" : section));
  };

  return (
    <div className="p-6">
      <h2 className="text-2xl font-bold mb-6">Risk & Operations Dashboard</h2>

      {/* Architecture Selector */}
      <div className="mb-6">
        <label className="block text-xs font-semibold uppercase tracking-wider mb-1">
          Select Architecture
        </label>
        <select
          value={selectedId}
          onChange={(e) => setSelectedId(e.target.value ? Number(e.target.value) : "")}
          className="border-2 border-black px-3 py-2 text-sm font-mono bg-white focus:outline-none min-w-64"
        >
          {architectures.length === 0 && <option value="">No architectures available</option>}
          {architectures.map((a) => (
            <option key={a.id} value={a.id}>
              {a.name}
            </option>
          ))}
        </select>
      </div>

      {!arch && (
        <div className="text-sm text-[var(--color-text-secondary)] font-mono">
          Select an architecture to view its risk dashboard.
        </div>
      )}

      {arch && (
        <>
          {/* Section Navigation */}
          <div className="flex border-2 border-black mb-6">
            {[
              { key: "risks", label: "Risks" },
              { key: "stakeholders", label: "Stakeholders" },
              { key: "workforce", label: "Workforce" },
              { key: "authority", label: "Authority" },
            ].map((s) => (
              <button
                key={s.key}
                onClick={() => toggleSection(s.key)}
                className={`flex-1 px-4 py-2 text-xs font-semibold uppercase tracking-wider border-r border-black last:border-r-0 cursor-pointer transition-colors ${
                  expandedSection === s.key
                    ? "bg-black text-white"
                    : "bg-white text-black hover:bg-[var(--color-surface)]"
                }`}
              >
                {s.label}
              </button>
            ))}
          </div>

          {/* === RISKS SECTION === */}
          {expandedSection === "risks" && (
            <RiskSection
              risks={risks}
              highSeverity={highSeverity}
              withMitigation={withMitigation}
              groupedRisks={groupedRisks}
              phases={arch?.implementation_phases ?? []}
            />
          )}

          {/* === STAKEHOLDERS SECTION === */}
          {expandedSection === "stakeholders" && (
            <StakeholderSection stakeholders={stakeholders} />
          )}

          {/* === WORKFORCE SECTION === */}
          {expandedSection === "workforce" && (
            <WorkforceSection workforce={workforce} />
          )}

          {/* === AUTHORITY SECTION === */}
          {expandedSection === "authority" && (
            <AuthoritySection authority={authority} />
          )}
        </>
      )}
    </div>
  );
}

/* ============ RISK SECTION ============ */

const SEVERITY_COLORS: Record<string, string> = {
  high: "#8B1A1A",
  moderate: "#6B5A1A",
  low: "#1A6B3C",
  none: "#E0E0E0",
};

const SEVERITY_LABELS: Record<string, string> = {
  high: "H",
  moderate: "M",
  low: "L",
  none: "",
};

function computeCellSeverity(
  baseSeverity: string,
  phaseIndex: number,
  totalPhases: number
): string {
  if (baseSeverity === "none") return "none";

  // Severity score: high=3, moderate=2, low=1
  const scoreMap: Record<string, number> = { high: 3, moderate: 2, low: 1 };
  const base = scoreMap[baseSeverity] ?? 2;

  // Phase adjustment: early phases (0,1) get +0.5 boost, later phases get reduction
  // The further into implementation, the more risk diminishes
  const phaseRatio = totalPhases > 1 ? phaseIndex / (totalPhases - 1) : 0;
  const adjustment = 0.5 - phaseRatio * 1.0; // +0.5 at start, -0.5 at end
  const adjusted = base + adjustment;

  if (adjusted >= 2.5) return "high";
  if (adjusted >= 1.5) return "moderate";
  return "low";
}

function RiskSection({
  risks,
  highSeverity,
  withMitigation,
  groupedRisks,
  phases,
}: {
  risks: Risk[];
  highSeverity: number;
  withMitigation: number;
  groupedRisks: Record<string, Risk[]>;
  phases: Phase[];
}) {
  const [tooltipCell, setTooltipCell] = useState<{
    category: string;
    phaseIndex: number;
    x: number;
    y: number;
  } | null>(null);

  if (risks.length === 0) {
    return (
      <div className="text-sm text-[var(--color-text-secondary)] font-mono">
        No risks defined for this architecture.
      </div>
    );
  }

  // Collect all categories present in risks (use predefined order, then extras)
  const presentCategories = RISK_CATEGORIES.filter(
    (cat) => groupedRisks[cat]?.length
  );
  const extraCategories = Object.keys(groupedRisks).filter(
    (cat) => !RISK_CATEGORIES.includes(cat)
  );
  const allCategories = [...presentCategories, ...extraCategories];

  // If no phases available, create a single default phase
  const displayPhases: Phase[] =
    phases.length > 0
      ? phases
      : [{ name: "Implementation", duration: "", description: "", milestones: [], status: "" }];

  // Build heat map data: for each (category, phase) compute severity
  const heatMapData: Record<string, { severity: string; risks: Risk[] }[]> = {};
  for (const cat of allCategories) {
    const catRisks = groupedRisks[cat] || [];
    // Base severity for this category: worst severity among its risks
    const worstSeverity = catRisks.reduce((worst, r) => {
      const sev = riskSeverity(r);
      const order: Record<string, number> = { high: 3, moderate: 2, low: 1 };
      return (order[sev] ?? 0) > (order[worst] ?? 0) ? sev : worst;
    }, "low");

    heatMapData[cat] = displayPhases.map((_, pi) => ({
      severity: computeCellSeverity(worstSeverity, pi, displayPhases.length),
      risks: catRisks,
    }));
  }

  // Truncate phase name for header display
  const truncateName = (name: string, maxLen: number) =>
    name.length > maxLen ? name.slice(0, maxLen - 1) + "\u2026" : name;

  return (
    <>
      {/* Summary Stats */}
      <div className="flex gap-4 mb-6">
        <div className="border-2 border-black p-3 flex-1">
          <span className="text-xs font-semibold uppercase tracking-wider block">Total Risks</span>
          <span className="font-mono text-2xl font-bold">{risks.length}</span>
        </div>
        <div className="border-2 border-[#8B1A1A] p-3 flex-1">
          <span className="text-xs font-semibold uppercase tracking-wider block text-[#8B1A1A]">
            High Severity
          </span>
          <span className="font-mono text-2xl font-bold text-[#8B1A1A]">{highSeverity}</span>
        </div>
        <div className="border-2 border-[#1A6B3C] p-3 flex-1">
          <span className="text-xs font-semibold uppercase tracking-wider block text-[#1A6B3C]">
            Mitigation Coverage
          </span>
          <span className="font-mono text-2xl font-bold text-[#1A6B3C]">
            {risks.length > 0 ? Math.round((withMitigation / risks.length) * 100) : 0}%
          </span>
        </div>
      </div>

      {/* Phase-Based Risk Heat Map */}
      <div className="border-2 border-black mb-6 relative">
        <div className="p-4 border-b border-black bg-[var(--color-surface)]">
          <h3 className="text-sm font-semibold uppercase tracking-wider">
            Risk Heat Map by Implementation Phase
          </h3>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full border-collapse">
            <thead>
              <tr className="border-b-2 border-black">
                <th className="text-left p-3 text-xs font-semibold uppercase tracking-wider border-r border-black min-w-[140px] bg-white">
                  Category
                </th>
                {displayPhases.map((phase, pi) => (
                  <th
                    key={pi}
                    className="p-2 text-[10px] font-semibold uppercase tracking-wider text-center border-r border-black last:border-r-0 bg-white min-w-[80px]"
                    title={phase.name}
                  >
                    <span className="font-sans">{truncateName(phase.name, 18)}</span>
                    {phase.duration && (
                      <span className="block font-mono text-[9px] font-normal text-[var(--color-text-secondary)] mt-0.5">
                        {phase.duration}
                      </span>
                    )}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {allCategories.map((cat) => (
                <tr key={cat} className="border-b border-black last:border-b-0">
                  <td className="p-3 text-xs font-semibold uppercase tracking-wider border-r border-black bg-white">
                    <span className="font-sans">{cat}</span>
                    <span className="font-mono text-[var(--color-text-secondary)] ml-1.5">
                      ({groupedRisks[cat]?.length ?? 0})
                    </span>
                  </td>
                  {heatMapData[cat]?.map((cell, pi) => {
                    const bgColor = SEVERITY_COLORS[cell.severity] || "#E0E0E0";
                    const label = SEVERITY_LABELS[cell.severity] || "";
                    const textColor =
                      cell.severity === "none" || cell.severity === "low"
                        ? "#000000"
                        : "#FFFFFF";

                    return (
                      <td
                        key={pi}
                        className="p-0 border-r border-black last:border-r-0 relative"
                        onMouseEnter={(e) => {
                          const rect = (e.target as HTMLElement).getBoundingClientRect();
                          setTooltipCell({
                            category: cat,
                            phaseIndex: pi,
                            x: rect.left + rect.width / 2,
                            y: rect.bottom + 4,
                          });
                        }}
                        onMouseLeave={() => setTooltipCell(null)}
                      >
                        <div
                          className="w-full h-full min-h-[40px] flex items-center justify-center cursor-default"
                          style={{ backgroundColor: bgColor }}
                        >
                          <span
                            className="font-mono text-sm font-bold"
                            style={{ color: textColor }}
                          >
                            {label}
                          </span>
                        </div>
                      </td>
                    );
                  })}
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Tooltip */}
        {tooltipCell && (() => {
          const cell = heatMapData[tooltipCell.category]?.[tooltipCell.phaseIndex];
          if (!cell) return null;
          const phase = displayPhases[tooltipCell.phaseIndex];
          const severityLabel =
            cell.severity === "high"
              ? "HIGH"
              : cell.severity === "moderate"
              ? "MODERATE"
              : cell.severity === "low"
              ? "LOW"
              : "N/A";

          return (
            <div
              className="fixed z-50 border-2 border-black bg-white p-3 max-w-sm"
              style={{
                left: tooltipCell.x,
                top: tooltipCell.y,
                transform: "translateX(-50%)",
              }}
            >
              <div className="text-xs font-semibold uppercase tracking-wider mb-1">
                {tooltipCell.category} &mdash; {phase.name}
              </div>
              <div className="flex items-center gap-2 mb-2">
                <span
                  className="text-[10px] font-bold uppercase tracking-wider px-1.5 py-0.5 border"
                  style={{
                    color: SEVERITY_COLORS[cell.severity],
                    borderColor: SEVERITY_COLORS[cell.severity],
                  }}
                >
                  {severityLabel}
                </span>
              </div>
              {cell.risks.map((r, ri) => (
                <div key={ri} className="mb-1.5 last:mb-0">
                  <p className="text-xs text-black">{r.description}</p>
                  {r.mitigation && (
                    <p className="text-[10px] text-[var(--color-text-secondary)] mt-0.5">
                      <span className="font-semibold text-black">Mitigation:</span> {r.mitigation}
                    </p>
                  )}
                </div>
              ))}
            </div>
          );
        })()}
      </div>

      {/* Color Legend */}
      <div className="border-2 border-black p-3 mb-6">
        <h4 className="text-xs font-semibold uppercase tracking-wider mb-2">Severity Legend</h4>
        <div className="flex gap-6 flex-wrap">
          {[
            { key: "high", label: "HIGH" },
            { key: "moderate", label: "MODERATE" },
            { key: "low", label: "LOW" },
            { key: "none", label: "N/A" },
          ].map((item) => (
            <div key={item.key} className="flex items-center gap-2">
              <div
                className="w-5 h-5 border border-black"
                style={{ backgroundColor: SEVERITY_COLORS[item.key] }}
              />
              <span className="text-xs font-mono uppercase">{item.label}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Risk Detail Cards */}
      <div className="space-y-3">
        <h3 className="text-sm font-semibold uppercase tracking-wider">Risk Details</h3>
        {risks.map((r, i) => (
          <div key={i} className="border-2 border-black p-3">
            <div className="flex items-start gap-3 mb-2">
              <span
                className="text-[10px] font-semibold uppercase tracking-wider px-1.5 py-0.5 border shrink-0"
                style={{
                  color: RISK_COLORS[riskSeverity(r)] || "#888",
                  borderColor: RISK_COLORS[riskSeverity(r)] || "#888",
                }}
              >
                {r.category}
              </span>
              <p className="text-sm">{r.description}</p>
            </div>
            <div className="flex gap-3 mb-2">
              <span
                className="text-[10px] font-semibold uppercase tracking-wider px-1.5 py-0.5 border"
                style={{
                  color: RISK_COLORS[r.likelihood.toLowerCase()] || "#888",
                  borderColor: RISK_COLORS[r.likelihood.toLowerCase()] || "#888",
                }}
              >
                Likelihood: {r.likelihood}
              </span>
              <span
                className="text-[10px] font-semibold uppercase tracking-wider px-1.5 py-0.5 border"
                style={{
                  color: RISK_COLORS[r.impact.toLowerCase()] || "#888",
                  borderColor: RISK_COLORS[r.impact.toLowerCase()] || "#888",
                }}
              >
                Impact: {r.impact}
              </span>
            </div>
            {r.mitigation && (
              <div className="text-xs text-[var(--color-text-secondary)] bg-[var(--color-surface)] p-2 border border-[var(--color-border)]">
                <span className="font-semibold text-black">Mitigation:</span> {r.mitigation}
              </div>
            )}
          </div>
        ))}
      </div>
    </>
  );
}

/* ============ STAKEHOLDER SECTION ============ */

function StakeholderSection({ stakeholders }: { stakeholders: Stakeholder[] }) {
  const graphRef = useRef<HTMLDivElement>(null);
  const [graphSize, setGraphSize] = useState({ w: 0, h: 0 });

  const handleGraphResize = useCallback(() => {
    if (graphRef.current) {
      const rect = graphRef.current.getBoundingClientRect();
      setGraphSize({ w: rect.width, h: rect.height });
    }
  }, []);

  useEffect(() => {
    handleGraphResize();
    const observer = new ResizeObserver(handleGraphResize);
    if (graphRef.current) observer.observe(graphRef.current);
    return () => observer.disconnect();
  }, [handleGraphResize]);

  if (stakeholders.length === 0) {
    return (
      <div className="text-sm text-[var(--color-text-secondary)] font-mono">
        No stakeholders defined for this architecture.
      </div>
    );
  }

  const hasSize = graphSize.w > 0 && graphSize.h > 0;
  const cx = graphSize.w / 2;
  const cy = graphSize.h / 2;

  // Influence-based radii (proportional to container)
  const scale = Math.min(graphSize.w, graphSize.h) / 600;
  const radiusMap: Record<string, number> = {
    high: 120 * scale,
    moderate: 200 * scale,
    low: 270 * scale,
  };

  // Node sizing by influence
  const nodeSizeMap: Record<string, { w: number; h: number }> = {
    high: { w: 140 * scale, h: 48 * scale },
    moderate: { w: 120 * scale, h: 42 * scale },
    low: { w: 100 * scale, h: 38 * scale },
  };

  // Group stakeholders by influence for ring placement
  const byInfluence: Record<string, Stakeholder[]> = { high: [], moderate: [], low: [] };
  for (const s of stakeholders) {
    const key = s.influence.toLowerCase();
    if (byInfluence[key]) byInfluence[key].push(s);
    else byInfluence["moderate"].push(s);
  }

  // Compute node positions
  interface NodePos {
    x: number;
    y: number;
    w: number;
    h: number;
    stakeholder: Stakeholder;
  }

  const nodes: NodePos[] = [];
  for (const level of ["high", "moderate", "low"] as const) {
    const group = byInfluence[level];
    const radius = radiusMap[level];
    const size = nodeSizeMap[level];
    const count = group.length;
    // Offset start angle per ring to avoid overlap
    const angleOffset = level === "high" ? 0 : level === "moderate" ? Math.PI / 8 : Math.PI / 6;
    for (let i = 0; i < count; i++) {
      const angle = angleOffset + (2 * Math.PI * i) / count - Math.PI / 2;
      nodes.push({
        x: cx + radius * Math.cos(angle),
        y: cy + radius * Math.sin(angle),
        w: size.w,
        h: size.h,
        stakeholder: group[i],
      });
    }
  }

  // Hub node dimensions
  const hubW = 130 * scale;
  const hubH = 36 * scale;

  // Find same-interest connections
  const interestGroups: Record<string, number[]> = {};
  nodes.forEach((n, idx) => {
    const key = n.stakeholder.interest.toLowerCase();
    if (!interestGroups[key]) interestGroups[key] = [];
    interestGroups[key].push(idx);
  });

  const lineThickness: Record<string, number> = {
    high: 2,
    moderate: 1.5,
    low: 1,
  };

  const fontSize = Math.max(9, 11 * scale);
  const roleFontSize = Math.max(7, 9 * scale);

  return (
    <div>
      <h3 className="text-lg font-bold mb-4">Stakeholder Network</h3>

      {/* Network Graph */}
      <div className="border-2 border-black mb-6">
        <div ref={graphRef} className="w-full" style={{ minHeight: 560 }}>
          {hasSize && (
            <svg width={graphSize.w} height={graphSize.h}>
              {/* Relationship lines (same interest level) - drawn first so they appear behind */}
              {Object.values(interestGroups).map((indices) =>
                indices.length > 1
                  ? indices.map((a, ai) =>
                      indices.slice(ai + 1).map((b) => (
                        <line
                          key={`rel-${a}-${b}`}
                          x1={nodes[a].x}
                          y1={nodes[a].y}
                          x2={nodes[b].x}
                          y2={nodes[b].y}
                          stroke="#CCCCCC"
                          strokeWidth={1}
                          strokeDasharray="4,3"
                        />
                      ))
                    )
                  : null
              )}

              {/* Connection lines from each node to hub */}
              {nodes.map((n, i) => {
                const inf = n.stakeholder.influence.toLowerCase();
                return (
                  <line
                    key={`conn-${i}`}
                    x1={n.x}
                    y1={n.y}
                    x2={cx}
                    y2={cy}
                    stroke={INFLUENCE_COLORS[inf] || "#888888"}
                    strokeWidth={lineThickness[inf] || 1}
                  />
                );
              })}

              {/* Central hub node */}
              <rect
                x={cx - hubW / 2}
                y={cy - hubH / 2}
                width={hubW}
                height={hubH}
                fill="black"
                stroke="black"
                strokeWidth={2}
              />
              <text
                x={cx}
                y={cy + 1}
                textAnchor="middle"
                dominantBaseline="middle"
                fontSize={Math.max(8, 10 * scale)}
                fontFamily="'Inter', sans-serif"
                fontWeight={700}
                fill="white"
                letterSpacing="0.05em"
              >
                COORDINATION HUB
              </text>

              {/* Stakeholder nodes */}
              {nodes.map((n, i) => {
                const inf = n.stakeholder.influence.toLowerCase();
                const borderColor = INFLUENCE_COLORS[inf] || "#888888";
                return (
                  <g key={`node-${i}`}>
                    <rect
                      x={n.x - n.w / 2}
                      y={n.y - n.h / 2}
                      width={n.w}
                      height={n.h}
                      fill="white"
                      stroke={borderColor}
                      strokeWidth={2}
                    />
                    {/* Name */}
                    <text
                      x={n.x}
                      y={n.y - n.h * 0.1}
                      textAnchor="middle"
                      dominantBaseline="middle"
                      fontSize={fontSize}
                      fontFamily="'Inter', sans-serif"
                      fontWeight={600}
                      fill="black"
                    >
                      {n.stakeholder.name.length > 16
                        ? n.stakeholder.name.slice(0, 15) + "\u2026"
                        : n.stakeholder.name}
                    </text>
                    {/* Role */}
                    <text
                      x={n.x}
                      y={n.y + n.h * 0.25}
                      textAnchor="middle"
                      dominantBaseline="middle"
                      fontSize={roleFontSize}
                      fontFamily="'JetBrains Mono', monospace"
                      fill="#666666"
                    >
                      {n.stakeholder.role.length > 20
                        ? n.stakeholder.role.slice(0, 19) + "\u2026"
                        : n.stakeholder.role}
                    </text>
                    <title>
                      {n.stakeholder.name} ({n.stakeholder.role}) — Influence: {n.stakeholder.influence}, Interest: {n.stakeholder.interest}
                    </title>
                  </g>
                );
              })}
            </svg>
          )}
        </div>
      </div>

      {/* Legend */}
      <div className="border-2 border-black p-3 mb-6">
        <h4 className="text-xs font-semibold uppercase tracking-wider mb-2">Influence Level</h4>
        <div className="flex gap-6 flex-wrap">
          {(["high", "moderate", "low"] as const).map((level) => (
            <div key={level} className="flex items-center gap-2">
              <div
                className="border-2"
                style={{
                  width: level === "high" ? 28 : level === "moderate" ? 22 : 16,
                  height: 12,
                  borderColor: INFLUENCE_COLORS[level],
                  backgroundColor: "white",
                }}
              />
              <span className="text-xs font-mono uppercase">{level}</span>
            </div>
          ))}
          <div className="flex items-center gap-2">
            <svg width={28} height={12}>
              <line x1={0} y1={6} x2={28} y2={6} stroke="#CCCCCC" strokeWidth={1} strokeDasharray="4,3" />
            </svg>
            <span className="text-xs font-mono uppercase">Same Interest</span>
          </div>
        </div>
      </div>

      {/* Stakeholder Detail Table */}
      <div className="border-2 border-black">
        <table className="w-full border-collapse">
          <thead>
            <tr className="border-b-2 border-black bg-[var(--color-surface)]">
              <th className="text-left p-3 text-xs font-semibold uppercase tracking-wider">Name</th>
              <th className="text-left p-3 text-xs font-semibold uppercase tracking-wider">Role</th>
              <th className="text-left p-3 text-xs font-semibold uppercase tracking-wider w-24">Influence</th>
              <th className="text-left p-3 text-xs font-semibold uppercase tracking-wider w-24">Interest</th>
              <th className="text-left p-3 text-xs font-semibold uppercase tracking-wider">Engagement Strategy</th>
            </tr>
          </thead>
          <tbody>
            {stakeholders.map((s, i) => {
              const infColor = INFLUENCE_COLORS[s.influence.toLowerCase()] || "#888";
              const intColor = INFLUENCE_COLORS[s.interest.toLowerCase()] || "#888";
              return (
                <tr key={i} className="border-b border-[var(--color-border)]">
                  <td className="p-3 text-sm font-semibold">{s.name}</td>
                  <td className="p-3 text-sm font-mono text-[var(--color-text-secondary)]">{s.role}</td>
                  <td className="p-3">
                    <span
                      className="text-[10px] font-semibold uppercase tracking-wider px-1.5 py-0.5 border"
                      style={{ color: infColor, borderColor: infColor }}
                    >
                      {s.influence}
                    </span>
                  </td>
                  <td className="p-3">
                    <span
                      className="text-[10px] font-semibold uppercase tracking-wider px-1.5 py-0.5 border"
                      style={{ color: intColor, borderColor: intColor }}
                    >
                      {s.interest}
                    </span>
                  </td>
                  <td className="p-3 text-xs text-[var(--color-text-secondary)]">{s.engagement_strategy}</td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}

/* ============ WORKFORCE SECTION ============ */

function WorkforceSection({ workforce }: { workforce: WorkforcePlan | undefined }) {
  if (!workforce) {
    return (
      <div className="text-sm text-[var(--color-text-secondary)] font-mono">
        No workforce plan defined for this architecture.
      </div>
    );
  }

  return (
    <div>
      <h3 className="text-lg font-bold mb-4">Workforce Plan</h3>

      {/* Total FTE */}
      <div className="border-2 border-black p-4 mb-6">
        <span className="text-xs font-semibold uppercase tracking-wider block mb-1">
          Total Estimated FTE
        </span>
        <span className="font-mono text-4xl font-bold">{workforce.total_estimated_fte}</span>
      </div>

      {/* Roles Table */}
      {workforce.roles.length > 0 && (
        <div className="border-2 border-black mb-6">
          <table className="w-full border-collapse">
            <thead>
              <tr className="border-b-2 border-black bg-[var(--color-surface)]">
                <th className="text-left p-3 text-xs font-semibold uppercase tracking-wider">Title</th>
                <th className="text-left p-3 text-xs font-semibold uppercase tracking-wider">Ratio</th>
                <th className="text-right p-3 text-xs font-semibold uppercase tracking-wider w-24">FTE</th>
                <th className="text-left p-3 text-xs font-semibold uppercase tracking-wider">Recruitment</th>
                <th className="text-left p-3 text-xs font-semibold uppercase tracking-wider">Training</th>
              </tr>
            </thead>
            <tbody>
              {workforce.roles.map((role, i) => (
                <tr key={i} className="border-b border-[var(--color-border)]">
                  <td className="p-3 text-sm font-semibold">{role.title}</td>
                  <td className="p-3 text-sm font-mono text-[var(--color-text-secondary)]">{role.ratio}</td>
                  <td className="p-3 text-sm font-mono text-right font-semibold">{role.estimated_fte}</td>
                  <td className="p-3 text-sm text-[var(--color-text-secondary)]">{role.recruitment_timeline}</td>
                  <td className="p-3 text-sm text-[var(--color-text-secondary)]">{role.training_required}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* Training & Retention */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="border-2 border-black p-3">
          <h4 className="text-xs font-semibold uppercase tracking-wider mb-2">Training Approach</h4>
          <p className="text-sm text-[var(--color-text-secondary)]">{workforce.training_approach}</p>
        </div>
        <div className="border-2 border-black p-3">
          <h4 className="text-xs font-semibold uppercase tracking-wider mb-2">Retention Strategy</h4>
          <p className="text-sm text-[var(--color-text-secondary)]">{workforce.retention_strategy}</p>
        </div>
      </div>
    </div>
  );
}

/* ============ AUTHORITY SECTION ============ */

function AuthoritySection({ authority }: { authority: AuthorityMap | undefined }) {
  if (!authority) {
    return (
      <div className="text-sm text-[var(--color-text-secondary)] font-mono">
        No authority map defined for this architecture.
      </div>
    );
  }

  return (
    <div>
      <h3 className="text-lg font-bold mb-2">Authority Map</h3>
      <p className="text-sm text-[var(--color-text-secondary)] mb-4 font-mono">
        Primary Authority Type: <span className="font-semibold text-black">{authority.primary_authority_type}</span>
      </p>

      {authority.entries.length === 0 && (
        <div className="text-sm text-[var(--color-text-secondary)] font-mono">
          No authority entries defined.
        </div>
      )}

      {/* Vertical Timeline */}
      <div className="relative pl-8">
        {/* Vertical line */}
        <div className="absolute left-3 top-0 bottom-0 w-0.5 bg-black" />

        {authority.entries.map((entry, i) => {
          const statusColor = AUTHORITY_STATUS_COLORS[entry.status?.toLowerCase()] || "#888888";
          return (
            <div key={i} className="relative mb-6 last:mb-0">
              {/* Dot on timeline */}
              <div
                className="absolute -left-5 top-2 w-4 h-4 border-2 border-black"
                style={{ backgroundColor: statusColor }}
              />

              <div className="border-2 border-black p-3 ml-4">
                <div className="flex items-start justify-between mb-1">
                  <h4 className="text-sm font-bold">{entry.authority}</h4>
                  <span
                    className="text-[10px] font-semibold uppercase tracking-wider px-1.5 py-0.5 border text-white"
                    style={{ backgroundColor: statusColor, borderColor: statusColor }}
                  >
                    {entry.status}
                  </span>
                </div>

                <div className="flex flex-wrap gap-3 text-xs font-mono text-[var(--color-text-secondary)] mb-2">
                  <span>Grantor: {entry.grantor}</span>
                  <span>Type: {entry.type}</span>
                  <span>Timeline: {entry.timeline}</span>
                </div>

                {entry.requirements.length > 0 && (
                  <div>
                    <span className="text-[10px] font-semibold uppercase tracking-wider">
                      Requirements:
                    </span>
                    <ul className="mt-1 space-y-0.5">
                      {entry.requirements.map((req, ri) => (
                        <li key={ri} className="text-xs font-mono text-[var(--color-text-secondary)] flex gap-1">
                          <span className="text-black">-</span> {req}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
