import { useState, useRef, useEffect, useCallback } from "react";
import type { Architecture, Risk, Stakeholder, WorkforcePlan, AuthorityMap } from "../types";

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

function RiskSection({
  risks,
  highSeverity,
  withMitigation,
  groupedRisks,
}: {
  risks: Risk[];
  highSeverity: number;
  withMitigation: number;
  groupedRisks: Record<string, Risk[]>;
}) {
  const matrixRef = useRef<HTMLDivElement>(null);
  const [matrixSize, setMatrixSize] = useState({ w: 0, h: 0 });

  const handleResize = useCallback(() => {
    if (matrixRef.current) {
      const rect = matrixRef.current.getBoundingClientRect();
      setMatrixSize({ w: rect.width, h: rect.height });
    }
  }, []);

  useEffect(() => {
    handleResize();
    const observer = new ResizeObserver(handleResize);
    if (matrixRef.current) observer.observe(matrixRef.current);
    return () => observer.disconnect();
  }, [handleResize]);

  if (risks.length === 0) {
    return (
      <div className="text-sm text-[var(--color-text-secondary)] font-mono">
        No risks defined for this architecture.
      </div>
    );
  }

  // Build risk matrix data
  const likelihoodLabels = ["Low", "Moderate", "High"];
  const impactLabels = ["Low", "Moderate", "High"];
  const matrixCellSize = Math.min(120, (matrixSize.w - 80) / 3);
  const svgW = matrixCellSize * 3 + 80;
  const svgH = matrixCellSize * 3 + 60;

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

      {/* Risk Matrix */}
      <div className="border-2 border-black p-4 mb-6">
        <h3 className="text-sm font-semibold uppercase tracking-wider mb-3">Risk Matrix</h3>
        <div ref={matrixRef} className="w-full" style={{ minHeight: svgH }}>
          {matrixSize.w > 0 && (
            <svg width={svgW} height={svgH}>
              {/* Axis labels */}
              <text
                x={svgW / 2}
                y={svgH - 4}
                textAnchor="middle"
                fontSize={10}
                fontFamily="'Inter', sans-serif"
                fontWeight={600}
                fill="#555555"
              >
                IMPACT
              </text>
              <text
                x={10}
                y={svgH / 2 - 20}
                textAnchor="middle"
                fontSize={10}
                fontFamily="'Inter', sans-serif"
                fontWeight={600}
                fill="#555555"
                transform={`rotate(-90, 10, ${svgH / 2 - 20})`}
              >
                LIKELIHOOD
              </text>

              {/* Grid cells */}
              {likelihoodLabels.map((lbl, li) => {
                const y = (2 - li) * matrixCellSize + 10;
                return impactLabels.map((ilbl, ii) => {
                  const x = ii * matrixCellSize + 60;
                  // Background color intensity
                  const severity = li + ii; // 0=low-low, 4=high-high
                  const alpha = severity <= 1 ? 0.05 : severity <= 2 ? 0.1 : severity <= 3 ? 0.2 : 0.3;
                  const bgColor =
                    severity <= 1 ? "#1A6B3C" : severity <= 3 ? "#6B5A1A" : "#8B1A1A";

                  // Find risks in this cell
                  const cellRisks = risks.filter(
                    (r) =>
                      (LIKELIHOOD_ORDER[r.likelihood.toLowerCase()] ?? 1) === li &&
                      (IMPACT_ORDER[r.impact.toLowerCase()] ?? 1) === ii
                  );

                  return (
                    <g key={`${li}-${ii}`}>
                      <rect
                        x={x}
                        y={y}
                        width={matrixCellSize}
                        height={matrixCellSize}
                        fill={bgColor}
                        fillOpacity={alpha}
                        stroke="#E0E0E0"
                        strokeWidth={1}
                      />
                      {/* Column label (bottom row) */}
                      {li === 0 && (
                        <text
                          x={x + matrixCellSize / 2}
                          y={y + matrixCellSize + 14}
                          textAnchor="middle"
                          fontSize={9}
                          fontFamily="'JetBrains Mono', monospace"
                          fill="#888888"
                        >
                          {ilbl}
                        </text>
                      )}
                      {/* Row label (left) */}
                      {ii === 0 && (
                        <text
                          x={56}
                          y={y + matrixCellSize / 2 + 3}
                          textAnchor="end"
                          fontSize={9}
                          fontFamily="'JetBrains Mono', monospace"
                          fill="#888888"
                        >
                          {lbl}
                        </text>
                      )}
                      {/* Risk dots */}
                      {cellRisks.map((r, ri) => {
                        const dotX = x + 16 + (ri % 4) * 22;
                        const dotY = y + 20 + Math.floor(ri / 4) * 22;
                        const sev = riskSeverity(r);
                        return (
                          <circle
                            key={ri}
                            cx={dotX}
                            cy={dotY}
                            r={7}
                            fill={RISK_COLORS[sev] || "#888888"}
                            stroke="#000000"
                            strokeWidth={1}
                          >
                            <title>
                              {r.category}: {r.description}
                            </title>
                          </circle>
                        );
                      })}
                    </g>
                  );
                });
              })}
            </svg>
          )}
        </div>
      </div>

      {/* Risk Cards by Category */}
      <div className="space-y-4">
        {RISK_CATEGORIES.filter((cat) => groupedRisks[cat]?.length).map((cat) => (
          <div key={cat} className="border-2 border-black">
            <div className="p-3 bg-[var(--color-surface)] border-b border-black">
              <h4 className="text-sm font-semibold uppercase tracking-wider">
                {cat} ({groupedRisks[cat].length})
              </h4>
            </div>
            <div className="divide-y divide-[var(--color-border)]">
              {groupedRisks[cat].map((r, i) => (
                <div key={i} className="p-3">
                  <p className="text-sm mb-2">{r.description}</p>
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
          </div>
        ))}

        {/* Also show any categories not in our predefined list */}
        {Object.keys(groupedRisks)
          .filter((cat) => !RISK_CATEGORIES.includes(cat))
          .map((cat) => (
            <div key={cat} className="border-2 border-black">
              <div className="p-3 bg-[var(--color-surface)] border-b border-black">
                <h4 className="text-sm font-semibold uppercase tracking-wider">
                  {cat} ({groupedRisks[cat].length})
                </h4>
              </div>
              <div className="divide-y divide-[var(--color-border)]">
                {groupedRisks[cat].map((r, i) => (
                  <div key={i} className="p-3">
                    <p className="text-sm mb-2">{r.description}</p>
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
            </div>
          ))}
      </div>
    </>
  );
}

/* ============ STAKEHOLDER SECTION ============ */

function StakeholderSection({ stakeholders }: { stakeholders: Stakeholder[] }) {
  if (stakeholders.length === 0) {
    return (
      <div className="text-sm text-[var(--color-text-secondary)] font-mono">
        No stakeholders defined for this architecture.
      </div>
    );
  }

  return (
    <div>
      <h3 className="text-lg font-bold mb-4">Stakeholder Map</h3>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {stakeholders.map((s, i) => (
          <div key={i} className="border-2 border-black p-3">
            <h4 className="text-sm font-bold mb-1">{s.name}</h4>
            <span className="text-[10px] font-semibold uppercase tracking-wider px-1.5 py-0.5 border border-black inline-block mb-2">
              {s.role}
            </span>
            {s.description && (
              <p className="text-xs text-[var(--color-text-secondary)] mb-2">{s.description}</p>
            )}

            {/* Influence bar */}
            <div className="mb-1">
              <span className="text-[10px] font-mono text-[var(--color-text-secondary)]">
                Influence: {s.influence}
              </span>
              <div className="w-full h-2 border border-black bg-white mt-0.5">
                <div
                  className="h-full"
                  style={{
                    width:
                      s.influence.toLowerCase() === "high"
                        ? "100%"
                        : s.influence.toLowerCase() === "moderate"
                        ? "60%"
                        : "30%",
                    backgroundColor: INFLUENCE_COLORS[s.influence.toLowerCase()] || "#888",
                  }}
                />
              </div>
            </div>

            {/* Interest bar */}
            <div className="mb-2">
              <span className="text-[10px] font-mono text-[var(--color-text-secondary)]">
                Interest: {s.interest}
              </span>
              <div className="w-full h-2 border border-black bg-white mt-0.5">
                <div
                  className="h-full"
                  style={{
                    width:
                      s.interest.toLowerCase() === "high"
                        ? "100%"
                        : s.interest.toLowerCase() === "moderate"
                        ? "60%"
                        : "30%",
                    backgroundColor: INFLUENCE_COLORS[s.interest.toLowerCase()] || "#888",
                  }}
                />
              </div>
            </div>

            {/* Engagement strategy */}
            {s.engagement_strategy && (
              <div className="text-xs text-[var(--color-text-secondary)] bg-[var(--color-surface)] p-2 border border-[var(--color-border)]">
                <span className="font-semibold text-black">Strategy:</span> {s.engagement_strategy}
              </div>
            )}
          </div>
        ))}
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
