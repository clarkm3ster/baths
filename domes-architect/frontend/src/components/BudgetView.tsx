import { useState, useRef, useEffect, useCallback } from "react";
import type { Architecture } from "../types";

interface Props {
  architectures: Architecture[];
}

const BUDGET_COLORS = ["#1A3D8B", "#1A6B3C", "#6B5A1A", "#5A1A6B", "#1A6B6B", "#8B1A1A", "#555555", "#333333"];

function formatCurrency(n: number): string {
  return new Intl.NumberFormat("en-US", { style: "currency", currency: "USD", maximumFractionDigits: 0 }).format(n);
}

function formatNumber(n: number): string {
  return new Intl.NumberFormat("en-US").format(n);
}

export default function BudgetView({ architectures }: Props) {
  const [selectedId, setSelectedId] = useState<number | "">(
    architectures.length > 0 ? architectures[0].id : ""
  );
  const barRef = useRef<HTMLDivElement>(null);
  const [barWidth, setBarWidth] = useState(0);

  const handleResize = useCallback(() => {
    if (barRef.current) {
      setBarWidth(barRef.current.getBoundingClientRect().width);
    }
  }, []);

  useEffect(() => {
    handleResize();
    const observer = new ResizeObserver(handleResize);
    if (barRef.current) observer.observe(barRef.current);
    return () => observer.disconnect();
  }, [handleResize]);

  const arch = architectures.find((a) => a.id === selectedId);
  const budget = arch?.budget_breakdown;
  const perPerson = arch && arch.population_size > 0
    ? arch.annual_budget / arch.population_size
    : 0;

  return (
    <div className="p-6">
      <h2 className="text-2xl font-bold mb-6">Budget Breakdown</h2>

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
          Select an architecture to view its budget.
        </div>
      )}

      {arch && !budget && (
        <div className="text-sm text-[var(--color-text-secondary)] font-mono">
          No budget breakdown available for this architecture.
        </div>
      )}

      {arch && budget && (
        <>
          {/* Total Budget */}
          <div className="border-2 border-black p-4 mb-6">
            <div className="flex items-baseline gap-6">
              <div>
                <span className="text-xs font-semibold uppercase tracking-wider block mb-1">
                  Total Annual Budget
                </span>
                <span className="font-mono text-4xl font-bold">
                  {formatCurrency(budget.total_annual)}
                </span>
              </div>
              <div>
                <span className="text-xs font-semibold uppercase tracking-wider block mb-1">
                  Per Person Cost
                </span>
                <span className="font-mono text-2xl font-bold">
                  {formatCurrency(perPerson)}
                </span>
                <span className="text-xs font-mono text-[var(--color-text-secondary)] ml-1">
                  / {formatNumber(arch.population_size)} people
                </span>
              </div>
            </div>
          </div>

          {/* Stacked Bar */}
          <div className="mb-6">
            <span className="text-xs font-semibold uppercase tracking-wider block mb-2">
              Budget Allocation
            </span>
            <div
              ref={barRef}
              className="w-full h-12 border-2 border-black flex overflow-hidden"
            >
              {barWidth > 0 &&
                budget.categories.map((cat, i) => {
                  const color = BUDGET_COLORS[i % BUDGET_COLORS.length];
                  const widthPct = cat.percentage;
                  return (
                    <div
                      key={i}
                      className="h-full relative group flex items-center justify-center"
                      style={{
                        width: `${widthPct}%`,
                        backgroundColor: color,
                        minWidth: widthPct > 3 ? undefined : "2px",
                      }}
                    >
                      {widthPct > 8 && (
                        <span className="text-[10px] font-mono text-white font-semibold truncate px-1">
                          {cat.name} ({cat.percentage}%)
                        </span>
                      )}
                      {/* Tooltip */}
                      <div className="absolute bottom-full left-1/2 -translate-x-1/2 mb-1 bg-black text-white text-[10px] font-mono px-2 py-1 whitespace-nowrap opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none z-10">
                        {cat.name}: {formatCurrency(cat.amount)} ({cat.percentage}%)
                      </div>
                    </div>
                  );
                })}
            </div>
            {/* Legend */}
            <div className="flex flex-wrap gap-3 mt-2">
              {budget.categories.map((cat, i) => (
                <div key={i} className="flex items-center gap-1">
                  <div
                    className="w-3 h-3"
                    style={{ backgroundColor: BUDGET_COLORS[i % BUDGET_COLORS.length] }}
                  />
                  <span className="text-[10px] font-mono text-[var(--color-text-secondary)]">
                    {cat.name}
                  </span>
                </div>
              ))}
            </div>
          </div>

          {/* Category Table */}
          <div className="border-2 border-black mb-6">
            <table className="w-full border-collapse">
              <thead>
                <tr className="border-b-2 border-black bg-[var(--color-surface)]">
                  <th className="text-left p-3 text-xs font-semibold uppercase tracking-wider">Category</th>
                  <th className="text-right p-3 text-xs font-semibold uppercase tracking-wider w-24">%</th>
                  <th className="text-right p-3 text-xs font-semibold uppercase tracking-wider w-36">Amount</th>
                  <th className="text-left p-3 text-xs font-semibold uppercase tracking-wider">Description</th>
                </tr>
              </thead>
              <tbody>
                {budget.categories.map((cat, i) => (
                  <tr key={i} className="border-b border-[var(--color-border)]">
                    <td className="p-3">
                      <div className="flex items-center gap-2">
                        <div
                          className="w-3 h-3 flex-shrink-0"
                          style={{ backgroundColor: BUDGET_COLORS[i % BUDGET_COLORS.length] }}
                        />
                        <span className="text-sm font-semibold">{cat.name}</span>
                      </div>
                    </td>
                    <td className="p-3 text-right text-sm font-mono">{cat.percentage}%</td>
                    <td className="p-3 text-right text-sm font-mono font-semibold">
                      {formatCurrency(cat.amount)}
                    </td>
                    <td className="p-3 text-sm text-[var(--color-text-secondary)]">{cat.description}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* Funding Sources */}
          <div className="border-2 border-black p-4">
            <h3 className="text-sm font-semibold uppercase tracking-wider mb-3">Funding Sources</h3>
            <div className="flex flex-wrap gap-2">
              {budget.funding_sources.map((source) => (
                <span
                  key={source}
                  className="text-xs font-mono px-2 py-1 border-2 border-black"
                >
                  {source}
                </span>
              ))}
            </div>
          </div>
        </>
      )}
    </div>
  );
}
