import { useState, useEffect, useRef } from "react";
import { Shield, MapPin, TrendingUp, AlertTriangle, DollarSign, Activity, Users } from "lucide-react";

interface ScoreResult {
  score: number;
  breakdown: Record<string, number>;
  priority_level: string;
  recommendations: string[];
}

interface OwnershipPathway {
  name: string;
  description: string;
  legal_mechanism: string;
}

interface EquityFramework {
  principles: { id: string; name: string; description: string }[];
  priority_scoring: { criteria: { name: string; weight: number; description: string }[] };
  anti_displacement_protections: string[];
  community_ownership_pathways: OwnershipPathway[];
}

// Philadelphia neighborhoods with approximate grid positions and data
const NEIGHBORHOODS = [
  { name: "Chestnut Hill", x: 2, y: 0, w: 2, h: 1, dormant_density: 0.08, median_income: 85000, activation_history: 0.8, org_density: 0.85, health_gaps: 0.1 },
  { name: "Germantown", x: 2, y: 1, w: 2, h: 1, dormant_density: 0.62, median_income: 28000, activation_history: 0.2, org_density: 0.55, health_gaps: 0.65 },
  { name: "Manayunk", x: 0, y: 0, w: 2, h: 1, dormant_density: 0.12, median_income: 62000, activation_history: 0.6, org_density: 0.7, health_gaps: 0.2 },
  { name: "Roxborough", x: 0, y: 1, w: 2, h: 1, dormant_density: 0.15, median_income: 58000, activation_history: 0.5, org_density: 0.6, health_gaps: 0.22 },
  { name: "Strawberry Mansion", x: 3, y: 2, w: 1, h: 1, dormant_density: 0.78, median_income: 19000, activation_history: 0.05, org_density: 0.35, health_gaps: 0.85 },
  { name: "North Philly", x: 2, y: 2, w: 1, h: 1, dormant_density: 0.72, median_income: 21000, activation_history: 0.15, org_density: 0.5, health_gaps: 0.8 },
  { name: "Kensington", x: 4, y: 2, w: 1, h: 1, dormant_density: 0.85, median_income: 22000, activation_history: 0.1, org_density: 0.4, health_gaps: 0.9 },
  { name: "Fishtown", x: 4, y: 3, w: 1, h: 1, dormant_density: 0.25, median_income: 55000, activation_history: 0.7, org_density: 0.8, health_gaps: 0.25 },
  { name: "Mantua", x: 1, y: 2, w: 1, h: 1, dormant_density: 0.68, median_income: 24000, activation_history: 0.12, org_density: 0.42, health_gaps: 0.78 },
  { name: "West Philly", x: 0, y: 3, w: 2, h: 1, dormant_density: 0.55, median_income: 32000, activation_history: 0.35, org_density: 0.65, health_gaps: 0.55 },
  { name: "Center City", x: 2, y: 3, w: 2, h: 1, dormant_density: 0.1, median_income: 72000, activation_history: 0.9, org_density: 0.9, health_gaps: 0.15 },
  { name: "Point Breeze", x: 2, y: 4, w: 1, h: 1, dormant_density: 0.5, median_income: 35000, activation_history: 0.4, org_density: 0.6, health_gaps: 0.5 },
  { name: "Cobbs Creek", x: 0, y: 4, w: 2, h: 1, dormant_density: 0.58, median_income: 30000, activation_history: 0.18, org_density: 0.48, health_gaps: 0.7 },
  { name: "South Philly", x: 3, y: 4, w: 2, h: 1, dormant_density: 0.3, median_income: 45000, activation_history: 0.55, org_density: 0.7, health_gaps: 0.35 },
  { name: "Southwest", x: 0, y: 5, w: 3, h: 1, dormant_density: 0.65, median_income: 26000, activation_history: 0.1, org_density: 0.38, health_gaps: 0.75 },
  { name: "Far Northeast", x: 4, y: 0, w: 1, h: 2, dormant_density: 0.18, median_income: 52000, activation_history: 0.3, org_density: 0.5, health_gaps: 0.3 },
];

type Metric = "score" | "dormant" | "income" | "health";

const METRICS: { key: Metric; label: string; icon: typeof MapPin }[] = [
  { key: "score", label: "Priority Score", icon: MapPin },
  { key: "dormant", label: "Dormant Space", icon: MapPin },
  { key: "income", label: "Income (Inv.)", icon: DollarSign },
  { key: "health", label: "Health Gaps", icon: Activity },
];

function scoreToColor(score: number): string {
  // Red (high priority) → green (low priority)
  if (score >= 75) return "#FF1744";
  if (score >= 60) return "#FF6D00";
  if (score >= 45) return "#FFB300";
  if (score >= 30) return "#00C853";
  return "#00E5FF";
}

function metricValue(n: typeof NEIGHBORHOODS[0], metric: Metric, scores: Map<string, ScoreResult>): number {
  if (metric === "score") return scores.get(n.name)?.score ?? 0;
  if (metric === "dormant") return n.dormant_density * 100;
  if (metric === "income") return Math.max(0, Math.min(100, (1 - n.median_income / 52649) * 100));
  if (metric === "health") return n.health_gaps * 100;
  return 0;
}

function fmt$(n: number) {
  return "$" + n.toLocaleString();
}

export default function EquityDashboardPage() {
  const [equity, setEquity] = useState<EquityFramework | null>(null);
  const [scores, setScores] = useState<Map<string, ScoreResult>>(new Map());
  const [loading, setLoading] = useState(true);
  const [metric, setMetric] = useState<Metric>("score");
  const [hovered, setHovered] = useState<string | null>(null);
  const [selected, setSelected] = useState<string | null>(null);

  useEffect(() => {
    fetch("/api/policy/equity")
      .then((r) => r.json())
      .then((d) => setEquity(d.framework || d));

    Promise.all(
      NEIGHBORHOODS.map(async (n) => {
        const r = await fetch("/api/policy/equity/score", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            dormant_space_density: n.dormant_density,
            median_income: n.median_income,
            activation_history: n.activation_history,
            community_organization_density: n.org_density,
            health_outcome_gaps: n.health_gaps,
          }),
        });
        return { name: n.name, result: await r.json() as ScoreResult };
      })
    ).then((results) => {
      const m = new Map<string, ScoreResult>();
      results.forEach((r) => m.set(r.name, r.result));
      setScores(m);
      setLoading(false);
    });
  }, []);

  const sorted = [...NEIGHBORHOODS]
    .map((n) => ({ ...n, score: scores.get(n.name)?.score ?? 0 }))
    .sort((a, b) => b.score - a.score);

  const selectedData = selected ? NEIGHBORHOODS.find((n) => n.name === selected) : null;
  const selectedScore = selected ? scores.get(selected) : null;

  const CELL = 90;
  const GAP = 3;

  return (
    <div className="min-h-screen bg-void pt-20 px-6 pb-20">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="mb-12">
          <p className="section-label mb-3">EQUITY DASHBOARD</p>
          <h1 className="text-3xl font-light tracking-tight mb-2">
            Where Activation Matters Most
          </h1>
          <p className="text-silver max-w-2xl">
            The places with the most dormant space and the least activation.
            This is the argument for why equity provisions matter.
          </p>
        </div>

        {/* Metric selector */}
        <div className="flex gap-2 mb-8">
          {METRICS.map((m) => (
            <button
              key={m.key}
              onClick={() => setMetric(m.key)}
              className={`tag cursor-pointer ${metric === m.key ? "tag-green" : ""}`}
            >
              {m.label}
            </button>
          ))}
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-5 gap-8 mb-16">
          {/* Map grid */}
          <div className="lg:col-span-3">
            <div className="card p-4">
              <p className="data-label mb-4">Philadelphia Neighborhoods</p>
              {loading ? (
                <div className="h-64 flex items-center justify-center text-steel font-mono text-sm">
                  Calculating scores...
                </div>
              ) : (
                <svg
                  viewBox={`0 0 ${5 * (CELL + GAP)} ${6 * (CELL + GAP)}`}
                  className="w-full"
                >
                  {NEIGHBORHOODS.map((n) => {
                    const val = metricValue(n, metric, scores);
                    const color = scoreToColor(val);
                    const isHovered = hovered === n.name;
                    const isSelected = selected === n.name;
                    return (
                      <g
                        key={n.name}
                        onMouseEnter={() => setHovered(n.name)}
                        onMouseLeave={() => setHovered(null)}
                        onClick={() => setSelected(selected === n.name ? null : n.name)}
                        style={{ cursor: "pointer" }}
                      >
                        <rect
                          x={n.x * (CELL + GAP)}
                          y={n.y * (CELL + GAP)}
                          width={n.w * (CELL + GAP) - GAP}
                          height={n.h * (CELL + GAP) - GAP}
                          fill={color}
                          opacity={isHovered || isSelected ? 1 : 0.7}
                          stroke={isSelected ? "#FFFFFF" : isHovered ? "#FFFFFF" : "none"}
                          strokeWidth={isSelected ? 2 : 1}
                        />
                        <text
                          x={n.x * (CELL + GAP) + (n.w * (CELL + GAP) - GAP) / 2}
                          y={n.y * (CELL + GAP) + (n.h * (CELL + GAP) - GAP) / 2 - 6}
                          textAnchor="middle"
                          fill="#FFFFFF"
                          fontSize="9"
                          fontFamily="Inter, sans-serif"
                          fontWeight="600"
                        >
                          {n.name}
                        </text>
                        <text
                          x={n.x * (CELL + GAP) + (n.w * (CELL + GAP) - GAP) / 2}
                          y={n.y * (CELL + GAP) + (n.h * (CELL + GAP) - GAP) / 2 + 10}
                          textAnchor="middle"
                          fill="#FFFFFF"
                          fontSize="14"
                          fontFamily="JetBrains Mono, monospace"
                          fontWeight="700"
                        >
                          {Math.round(val)}
                        </text>
                      </g>
                    );
                  })}
                </svg>
              )}
              {/* Legend */}
              <div className="flex items-center gap-4 mt-4 justify-center">
                <span className="text-xs text-silver font-mono">LOW PRIORITY</span>
                <div className="flex gap-0.5">
                  {["#00E5FF", "#00C853", "#FFB300", "#FF6D00", "#FF1744"].map((c) => (
                    <div key={c} className="w-8 h-3" style={{ background: c }} />
                  ))}
                </div>
                <span className="text-xs text-silver font-mono">HIGH PRIORITY</span>
              </div>
            </div>
          </div>

          {/* Detail panel */}
          <div className="lg:col-span-2">
            {selectedData && selectedScore ? (
              <div className="card">
                <div className="flex items-center justify-between mb-4">
                  <h3 className="font-medium text-lg">{selectedData.name}</h3>
                  <span
                    className="font-mono font-bold text-2xl"
                    style={{ color: scoreToColor(selectedScore.score) }}
                  >
                    {Math.round(selectedScore.score)}
                  </span>
                </div>
                <span className={`tag mb-4 inline-block ${
                  selectedScore.priority_level.includes("Critical") ? "tag-red" :
                  selectedScore.priority_level.includes("High") ? "tag-amber" :
                  selectedScore.priority_level.includes("Moderate") ? "tag-blue" : "tag-green"
                }`}>
                  {selectedScore.priority_level}
                </span>

                {/* Breakdown bars */}
                <div className="space-y-3 mt-4 mb-6">
                  {Object.entries(selectedScore.breakdown).map(([key, val]) => (
                    <div key={key}>
                      <div className="flex items-center justify-between mb-1">
                        <span className="text-xs text-silver">
                          {key.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase())}
                        </span>
                        <span className="font-mono text-xs">{Math.round(val)}</span>
                      </div>
                      <div className="h-1.5 bg-ash">
                        <div
                          className="h-full transition-all"
                          style={{
                            width: `${val}%`,
                            background: scoreToColor(val),
                          }}
                        />
                      </div>
                    </div>
                  ))}
                </div>

                {/* Raw data */}
                <div className="border-t border-ash pt-4 mb-4">
                  <p className="data-label mb-2">Neighborhood Data</p>
                  <div className="grid grid-cols-2 gap-2 text-xs">
                    <div className="p-2 bg-ash/30">
                      <span className="text-silver">Median Income</span>
                      <p className="font-mono font-bold mt-0.5">{fmt$(selectedData.median_income)}</p>
                    </div>
                    <div className="p-2 bg-ash/30">
                      <span className="text-silver">Dormant Space</span>
                      <p className="font-mono font-bold mt-0.5">{Math.round(selectedData.dormant_density * 100)}%</p>
                    </div>
                    <div className="p-2 bg-ash/30">
                      <span className="text-silver">Health Gaps</span>
                      <p className="font-mono font-bold mt-0.5">{Math.round(selectedData.health_gaps * 100)}%</p>
                    </div>
                    <div className="p-2 bg-ash/30">
                      <span className="text-silver">Activation Hx</span>
                      <p className="font-mono font-bold mt-0.5">{Math.round(selectedData.activation_history * 100)}%</p>
                    </div>
                  </div>
                </div>

                {/* Recommendations */}
                {selectedScore.recommendations.length > 0 && (
                  <div>
                    <p className="data-label mb-2">Recommendations</p>
                    <div className="space-y-1.5">
                      {selectedScore.recommendations.map((r, i) => (
                        <div key={i} className="flex items-start gap-2">
                          <AlertTriangle size={12} className="text-legal-amber mt-0.5 shrink-0" />
                          <p className="text-xs text-cloud">{r}</p>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            ) : (
              <div className="card flex items-center justify-center h-64 text-steel">
                <div className="text-center">
                  <MapPin size={24} className="mx-auto mb-2 opacity-40" />
                  <p className="text-sm">Click a neighborhood</p>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Ranking table */}
        <div className="mb-16">
          <h2 className="text-sm font-mono font-bold text-legal-green tracking-wider uppercase mb-6">
            Priority Ranking
          </h2>
          <div className="space-y-px">
            {sorted.map((n, i) => {
              const result = scores.get(n.name);
              if (!result) return null;
              return (
                <button
                  key={n.name}
                  onClick={() => setSelected(selected === n.name ? null : n.name)}
                  className={`w-full card bg-smoke text-left flex items-center gap-4 border-l-2 transition-colors ${
                    selected === n.name ? "border-legal-green bg-legal-green/5" :
                    result.priority_level.includes("Critical") ? "border-legal-red" :
                    result.priority_level.includes("High") ? "border-legal-amber" :
                    result.priority_level.includes("Moderate") ? "border-legal-cyan" :
                    "border-legal-green"
                  }`}
                >
                  <span className="font-mono text-xs text-steel w-6">
                    {String(i + 1).padStart(2, "0")}
                  </span>
                  <div className="flex-1">
                    <div className="flex items-center gap-3">
                      <MapPin size={14} className="text-silver" />
                      <h3 className="font-medium text-sm">{n.name}</h3>
                      <span className={`tag ${
                        result.priority_level.includes("Critical") ? "tag-red" :
                        result.priority_level.includes("High") ? "tag-amber" :
                        result.priority_level.includes("Moderate") ? "tag-blue" : "tag-green"
                      }`}>
                        {result.priority_level}
                      </span>
                    </div>
                    <div className="mt-2 flex items-center gap-3">
                      <div className="flex-1 h-1.5 bg-ash max-w-xs">
                        <div
                          className="h-full transition-all"
                          style={{ width: `${result.score}%`, background: scoreToColor(result.score) }}
                        />
                      </div>
                      <span className="font-mono font-bold text-sm w-8 text-right" style={{ color: scoreToColor(result.score) }}>
                        {Math.round(result.score)}
                      </span>
                    </div>
                  </div>
                  <div className="text-right text-xs font-mono text-silver hidden md:block">
                    <div>{fmt$(n.median_income)} income</div>
                    <div>{Math.round(n.dormant_density * 100)}% dormant</div>
                  </div>
                </button>
              );
            })}
          </div>
        </div>

        {/* Equity framework */}
        {equity && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div className="card">
              <div className="flex items-center gap-2 mb-4">
                <Shield size={16} className="text-legal-red" />
                <h3 className="text-sm font-mono font-bold text-legal-red tracking-wider uppercase">
                  Anti-Displacement Protections
                </h3>
              </div>
              <div className="space-y-2">
                {equity.anti_displacement_protections.map((p, i) => (
                  <div key={i} className="flex items-start gap-2">
                    <AlertTriangle size={12} className="text-legal-red mt-0.5 shrink-0" />
                    <p className="text-sm text-cloud">{p}</p>
                  </div>
                ))}
              </div>
            </div>
            <div className="card">
              <div className="flex items-center gap-2 mb-4">
                <TrendingUp size={16} className="text-legal-blue" />
                <h3 className="text-sm font-mono font-bold text-legal-blue tracking-wider uppercase">
                  Community Ownership Pathways
                </h3>
              </div>
              <div className="space-y-3">
                {equity.community_ownership_pathways.map((p) => (
                  <div key={p.name} className="p-3 border border-ash">
                    <p className="text-sm font-medium">{p.name}</p>
                    <p className="text-xs text-silver mt-1">{p.description}</p>
                    <p className="text-xs text-legal-blue font-mono mt-1">{p.legal_mechanism}</p>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
