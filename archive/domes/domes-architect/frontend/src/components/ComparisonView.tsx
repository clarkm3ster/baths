import { useState } from "react";
import type { Architecture } from "../types";
import { DOMAIN_COLORS, DOMAIN_LABELS } from "../types";

interface Props {
  architectures: Architecture[];
}

const SCORE_KEYS: { key: string; label: string }[] = [
  { key: "composite", label: "Composite" },
  { key: "coverage", label: "Coverage" },
  { key: "budget_feasibility", label: "Budget Feasibility" },
  { key: "political_feasibility", label: "Political Feasibility" },
  { key: "speed", label: "Speed" },
  { key: "sustainability", label: "Sustainability" },
  { key: "population_fit", label: "Population Fit" },
  { key: "cost_efficiency", label: "Cost Efficiency" },
];

function formatCurrency(n: number): string {
  return new Intl.NumberFormat("en-US", { style: "currency", currency: "USD", maximumFractionDigits: 0 }).format(n);
}

function formatNumber(n: number): string {
  return new Intl.NumberFormat("en-US").format(n);
}

export default function ComparisonView({ architectures }: Props) {
  const [selected, setSelected] = useState<Set<number>>(new Set());
  const [comparing, setComparing] = useState(false);

  const toggle = (id: number) => {
    setSelected((prev) => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return next;
    });
  };

  const compared = comparing
    ? architectures.filter((a) => selected.has(a.id))
    : [];

  const winnerId =
    compared.length > 1
      ? compared.reduce((best, a) =>
          (a.scores?.composite ?? 0) > (best.scores?.composite ?? 0) ? a : best
        ).id
      : null;

  if (architectures.length === 0) {
    return (
      <div className="p-8 text-center">
        <p className="text-sm text-[var(--color-text-secondary)] font-mono">
          No architectures available to compare. Generate some first.
        </p>
      </div>
    );
  }

  return (
    <div className="p-6">
      <h2 className="text-2xl font-bold mb-6">Compare Architectures</h2>

      {/* Selection */}
      {!comparing && (
        <div className="mb-6">
          <p className="text-xs font-semibold uppercase tracking-wider mb-3">
            Select architectures to compare (2 or more)
          </p>
          <div className="space-y-2 mb-4">
            {architectures.map((arch) => (
              <label
                key={arch.id}
                className="flex items-center gap-3 p-3 border border-black cursor-pointer hover:bg-[var(--color-surface)]"
              >
                <input
                  type="checkbox"
                  checked={selected.has(arch.id)}
                  onChange={() => toggle(arch.id)}
                  className="w-4 h-4 accent-black"
                />
                <span className="text-sm font-semibold">{arch.name}</span>
                <span className="text-xs font-mono text-[var(--color-text-secondary)]">
                  {arch.geography} | {formatNumber(arch.population_size)} pop | {formatCurrency(arch.annual_budget)}
                </span>
              </label>
            ))}
          </div>
          <button
            onClick={() => setComparing(true)}
            disabled={selected.size < 2}
            className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Compare Selected ({selected.size})
          </button>
        </div>
      )}

      {/* Comparison Table */}
      {comparing && compared.length > 0 && (
        <div>
          <button
            onClick={() => setComparing(false)}
            className="btn-secondary text-xs mb-4"
          >
            Back to Selection
          </button>

          <div className="overflow-x-auto">
            <table className="w-full border-collapse">
              <thead>
                <tr className="border-b-2 border-black">
                  <th className="text-left p-2 text-xs font-semibold uppercase tracking-wider w-48">
                    Dimension
                  </th>
                  {compared.map((arch) => (
                    <th
                      key={arch.id}
                      className="text-left p-2 text-xs font-semibold uppercase tracking-wider"
                      style={{
                        borderBottom: arch.id === winnerId ? "3px solid #1A6B3C" : undefined,
                      }}
                    >
                      <div className="flex items-center gap-2">
                        {arch.name}
                        {arch.id === winnerId && (
                          <span className="text-[10px] px-1 border border-[#1A6B3C] text-[#1A6B3C]">
                            BEST
                          </span>
                        )}
                      </div>
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {/* Status */}
                <tr className="border-b border-[var(--color-border)]">
                  <td className="p-2 text-xs font-mono text-[var(--color-text-secondary)]">Status</td>
                  {compared.map((a) => (
                    <td key={a.id} className="p-2 text-xs font-mono uppercase">{a.status}</td>
                  ))}
                </tr>

                {/* Population */}
                <tr className="border-b border-[var(--color-border)]">
                  <td className="p-2 text-xs font-mono text-[var(--color-text-secondary)]">Population</td>
                  {compared.map((a) => (
                    <td key={a.id} className="p-2 text-xs font-mono">{formatNumber(a.population_size)}</td>
                  ))}
                </tr>

                {/* Budget */}
                <tr className="border-b border-[var(--color-border)]">
                  <td className="p-2 text-xs font-mono text-[var(--color-text-secondary)]">Budget</td>
                  {compared.map((a) => (
                    <td key={a.id} className="p-2 text-xs font-mono">{formatCurrency(a.annual_budget)}</td>
                  ))}
                </tr>

                {/* Geography */}
                <tr className="border-b border-[var(--color-border)]">
                  <td className="p-2 text-xs font-mono text-[var(--color-text-secondary)]">Geography</td>
                  {compared.map((a) => (
                    <td key={a.id} className="p-2 text-xs font-mono">{a.geography}</td>
                  ))}
                </tr>

                {/* Primary Model */}
                <tr className="border-b border-[var(--color-border)]">
                  <td className="p-2 text-xs font-mono text-[var(--color-text-secondary)]">Primary Model</td>
                  {compared.map((a) => (
                    <td key={a.id} className="p-2 text-xs font-mono">{a.scores?.model_name || `ID ${a.primary_model_id}`}</td>
                  ))}
                </tr>

                {/* Domains */}
                <tr className="border-b border-[var(--color-border)]">
                  <td className="p-2 text-xs font-mono text-[var(--color-text-secondary)]">Domains</td>
                  {compared.map((a) => (
                    <td key={a.id} className="p-2">
                      <div className="flex flex-wrap gap-1">
                        {a.domains_targeted.map((d) => (
                          <span
                            key={d}
                            className="text-[9px] font-semibold uppercase px-1 py-0.5 text-white"
                            style={{ backgroundColor: DOMAIN_COLORS[d] || "#555" }}
                          >
                            {DOMAIN_LABELS[d] || d}
                          </span>
                        ))}
                      </div>
                    </td>
                  ))}
                </tr>

                {/* Scores */}
                {SCORE_KEYS.map(({ key, label }) => (
                  <tr key={key} className="border-b border-[var(--color-border)]">
                    <td className="p-2 text-xs font-mono text-[var(--color-text-secondary)]">{label}</td>
                    {compared.map((a) => {
                      const score = a.scores
                        ? (a.scores as unknown as Record<string, number>)[key] ?? 0
                        : 0;
                      const maxScore = Math.max(
                        ...compared.map((c) =>
                          c.scores ? ((c.scores as unknown as Record<string, number>)[key] ?? 0) : 0
                        )
                      );
                      const isBest = score === maxScore && compared.length > 1;
                      return (
                        <td key={a.id} className="p-2">
                          <div className="flex items-center gap-2">
                            <div className="flex-1 h-4 border border-black bg-white relative max-w-32">
                              <div
                                className="h-full"
                                style={{
                                  width: `${score * 100}%`,
                                  backgroundColor: isBest ? "#1A6B3C" : "#000",
                                }}
                              />
                            </div>
                            <span
                              className="text-xs font-mono"
                              style={{ fontWeight: isBest ? 700 : 400, color: isBest ? "#1A6B3C" : undefined }}
                            >
                              {(score * 100).toFixed(0)}
                            </span>
                          </div>
                        </td>
                      );
                    })}
                  </tr>
                ))}

                {/* Phase Count */}
                <tr className="border-b border-[var(--color-border)]">
                  <td className="p-2 text-xs font-mono text-[var(--color-text-secondary)]">Phases</td>
                  {compared.map((a) => (
                    <td key={a.id} className="p-2 text-xs font-mono">
                      {a.implementation_phases?.length ?? 0}
                    </td>
                  ))}
                </tr>

                {/* Stakeholder Count */}
                <tr className="border-b border-[var(--color-border)]">
                  <td className="p-2 text-xs font-mono text-[var(--color-text-secondary)]">Stakeholders</td>
                  {compared.map((a) => (
                    <td key={a.id} className="p-2 text-xs font-mono">
                      {a.stakeholders?.length ?? 0}
                    </td>
                  ))}
                </tr>

                {/* Risk Count */}
                <tr className="border-b border-[var(--color-border)]">
                  <td className="p-2 text-xs font-mono text-[var(--color-text-secondary)]">Risks</td>
                  {compared.map((a) => (
                    <td key={a.id} className="p-2 text-xs font-mono">
                      {a.risks?.length ?? 0}
                    </td>
                  ))}
                </tr>

                {/* Time Horizon */}
                <tr className="border-b border-[var(--color-border)]">
                  <td className="p-2 text-xs font-mono text-[var(--color-text-secondary)]">Time Horizon</td>
                  {compared.map((a) => (
                    <td key={a.id} className="p-2 text-xs font-mono">{a.time_horizon}</td>
                  ))}
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}
