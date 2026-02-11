import { useState, useRef, useEffect, useCallback, useMemo } from "react";
import type { Architecture } from "../types";

interface Props {
  architectures: Architecture[];
}

const BUDGET_COLORS = ["#1A3D8B", "#1A6B3C", "#6B5A1A", "#5A1A6B", "#1A6B6B", "#8B1A1A", "#555555", "#333333"];

const YEAR_MULTIPLIERS = [1.2, 1.0, 0.95, 0.92, 0.90, 0.88];
const SAVINGS_RATES = [0, 0.20, 0.45, 0.70, 0.90, 1.10];
const BREAK_EVEN_RATIO = 0.85;

function formatCurrency(n: number): string {
  return new Intl.NumberFormat("en-US", { style: "currency", currency: "USD", maximumFractionDigits: 0 }).format(n);
}

function formatCurrencyCompact(n: number): string {
  if (n >= 1_000_000_000) return `$${(n / 1_000_000_000).toFixed(1)}B`;
  if (n >= 1_000_000) return `$${(n / 1_000_000).toFixed(1)}M`;
  if (n >= 1_000) return `$${(n / 1_000).toFixed(0)}K`;
  return formatCurrency(n);
}

function formatNumber(n: number): string {
  return new Intl.NumberFormat("en-US").format(n);
}

function getYearCount(timeHorizon: string): number {
  if (timeHorizon === "5yr") return 6;
  if (timeHorizon === "3yr") return 4;
  return 2; // "1yr"
}

function getYearLabels(count: number): string[] {
  const labels: string[] = [];
  for (let i = 0; i < count; i++) {
    labels.push(i === 0 ? "Year 0\n(Startup)" : `Year ${i}`);
  }
  return labels;
}

function useResizeObserver(): [React.RefCallback<HTMLDivElement>, { w: number; h: number }] {
  const [size, setSize] = useState({ w: 0, h: 0 });
  const observerRef = useRef<ResizeObserver | null>(null);
  const nodeRef = useRef<HTMLDivElement | null>(null);

  const ref = useCallback((node: HTMLDivElement | null) => {
    if (observerRef.current) {
      observerRef.current.disconnect();
      observerRef.current = null;
    }
    nodeRef.current = node;
    if (node) {
      const ro = new ResizeObserver((entries) => {
        for (const entry of entries) {
          const { width, height } = entry.contentRect;
          setSize({ w: width, h: height });
        }
      });
      ro.observe(node);
      observerRef.current = ro;
    }
  }, []);

  useEffect(() => {
    return () => {
      if (observerRef.current) {
        observerRef.current.disconnect();
      }
    };
  }, []);

  return [ref, size];
}

export default function BudgetView({ architectures }: Props) {
  const [selectedId, setSelectedId] = useState<number | "">(
    architectures.length > 0 ? architectures[0].id : ""
  );
  const barRef = useRef<HTMLDivElement>(null);
  const [barWidth, setBarWidth] = useState(0);

  const [waterfallRef, waterfallSize] = useResizeObserver();
  const [lineChartRef, lineChartSize] = useResizeObserver();

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

  const yearCount = arch ? getYearCount(arch.time_horizon) : 2;
  const yearLabels = getYearLabels(yearCount);

  const yearlyBudgets = useMemo(() => {
    if (!budget) return [];
    return Array.from({ length: yearCount }, (_, i) => {
      const multiplier = YEAR_MULTIPLIERS[i] ?? YEAR_MULTIPLIERS[YEAR_MULTIPLIERS.length - 1];
      return budget.total_annual * multiplier;
    });
  }, [budget, yearCount]);

  const yearCategoryAmounts = useMemo(() => {
    if (!budget) return [];
    return Array.from({ length: yearCount }, (_, yi) => {
      const multiplier = YEAR_MULTIPLIERS[yi] ?? YEAR_MULTIPLIERS[YEAR_MULTIPLIERS.length - 1];
      return budget.categories.map((cat) => cat.amount * multiplier);
    });
  }, [budget, yearCount]);

  const cumulativeInvestment = useMemo(() => {
    const result: number[] = [];
    let sum = 0;
    for (const yb of yearlyBudgets) {
      sum += yb;
      result.push(sum);
    }
    return result;
  }, [yearlyBudgets]);

  const projectedSavings = useMemo(() => {
    if (!budget) return [];
    return Array.from({ length: yearCount }, (_, i) => {
      let sum = 0;
      for (let j = 0; j <= i; j++) {
        const r = SAVINGS_RATES[j] ?? SAVINGS_RATES[SAVINGS_RATES.length - 1];
        sum += r * budget.total_annual;
      }
      return sum;
    });
  }, [budget, yearCount]);

  const breakEvenYear = useMemo(() => {
    for (let i = 0; i < cumulativeInvestment.length; i++) {
      if (projectedSavings[i] >= cumulativeInvestment[i]) return i;
    }
    // Interpolate between last two points if savings is approaching
    if (cumulativeInvestment.length >= 2) {
      const n = cumulativeInvestment.length;
      const invPrev = cumulativeInvestment[n - 2];
      const invLast = cumulativeInvestment[n - 1];
      const savPrev = projectedSavings[n - 2];
      const savLast = projectedSavings[n - 1];
      const gapPrev = invPrev - savPrev;
      const gapLast = invLast - savLast;
      if (gapPrev > 0 && gapLast <= 0) {
        const fraction = gapPrev / (gapPrev - gapLast);
        return n - 2 + fraction;
      }
    }
    return null;
  }, [cumulativeInvestment, projectedSavings]);

  const breakEvenThreshold = budget ? budget.total_annual * BREAK_EVEN_RATIO : 0;

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

          {/* Multi-Year Funding Waterfall */}
          <div className="mb-6">
            <span className="text-xs font-semibold uppercase tracking-wider block mb-2">
              Multi-Year Funding Waterfall
            </span>
            <div ref={waterfallRef} className="w-full border-2 border-black" style={{ height: 340 }}>
              {waterfallSize.w > 0 && (() => {
                const svgW = waterfallSize.w;
                const svgH = 336;
                const margin = { top: 24, right: 24, bottom: 56, left: 72 };
                const chartW = svgW - margin.left - margin.right;
                const chartH = svgH - margin.top - margin.bottom;
                const maxBudget = Math.max(...yearlyBudgets) * 1.1;
                const barGroupWidth = chartW / yearCount;
                const barPad = barGroupWidth * 0.2;
                const barW = barGroupWidth - barPad * 2;

                const yScale = (v: number) => chartH - (v / maxBudget) * chartH;

                const yTicks: number[] = [];
                const tickStep = maxBudget / 5;
                for (let t = 0; t <= maxBudget; t += tickStep) {
                  yTicks.push(t);
                }

                return (
                  <svg width={svgW} height={svgH} style={{ display: "block" }}>
                    <g transform={`translate(${margin.left},${margin.top})`}>
                      {/* Y-axis gridlines and labels */}
                      {yTicks.map((tick, ti) => (
                        <g key={ti}>
                          <line
                            x1={0}
                            y1={yScale(tick)}
                            x2={chartW}
                            y2={yScale(tick)}
                            stroke="#e0e0e0"
                            strokeWidth={1}
                          />
                          <text
                            x={-8}
                            y={yScale(tick)}
                            textAnchor="end"
                            dominantBaseline="middle"
                            fontSize={10}
                            fontFamily="JetBrains Mono, monospace"
                            fill="#333"
                          >
                            {formatCurrencyCompact(tick)}
                          </text>
                        </g>
                      ))}

                      {/* Stacked bars per year */}
                      {yearCategoryAmounts.map((catAmounts, yi) => {
                        const x = yi * barGroupWidth + barPad;
                        let cumY = 0;
                        return (
                          <g key={yi}>
                            {catAmounts.map((amt, ci) => {
                              const barH = (amt / maxBudget) * chartH;
                              const y = yScale(cumY + amt);
                              cumY += amt;
                              return (
                                <rect
                                  key={ci}
                                  x={x}
                                  y={y}
                                  width={barW}
                                  height={barH}
                                  fill={BUDGET_COLORS[ci % BUDGET_COLORS.length]}
                                />
                              );
                            })}
                            {/* Green shading below break-even */}
                            {yearlyBudgets[yi] < breakEvenThreshold && (
                              <rect
                                x={x}
                                y={yScale(breakEvenThreshold)}
                                width={barW}
                                height={yScale(yearlyBudgets[yi]) - yScale(breakEvenThreshold)}
                                fill="#1A6B3C"
                                fillOpacity={0.2}
                              />
                            )}
                          </g>
                        );
                      })}

                      {/* Break-even threshold line */}
                      <line
                        x1={0}
                        y1={yScale(breakEvenThreshold)}
                        x2={chartW}
                        y2={yScale(breakEvenThreshold)}
                        stroke="#1A6B3C"
                        strokeWidth={2}
                        strokeDasharray="8,4"
                      />
                      <text
                        x={chartW}
                        y={yScale(breakEvenThreshold) - 6}
                        textAnchor="end"
                        fontSize={10}
                        fontFamily="Inter, sans-serif"
                        fontWeight={700}
                        fill="#1A6B3C"
                      >
                        BREAK-EVEN THRESHOLD ({formatCurrencyCompact(breakEvenThreshold)})
                      </text>

                      {/* X-axis labels */}
                      {yearLabels.map((label, i) => {
                        const x = i * barGroupWidth + barGroupWidth / 2;
                        const lines = label.split("\n");
                        return (
                          <g key={i}>
                            {lines.map((line, li) => (
                              <text
                                key={li}
                                x={x}
                                y={chartH + 16 + li * 14}
                                textAnchor="middle"
                                fontSize={11}
                                fontFamily="Inter, sans-serif"
                                fontWeight={li === 0 ? 600 : 400}
                                fill="#333"
                              >
                                {line}
                              </text>
                            ))}
                          </g>
                        );
                      })}

                      {/* Y-axis line */}
                      <line x1={0} y1={0} x2={0} y2={chartH} stroke="black" strokeWidth={2} />
                      {/* X-axis line */}
                      <line x1={0} y1={chartH} x2={chartW} y2={chartH} stroke="black" strokeWidth={2} />

                      {/* Budget value labels on top of each bar */}
                      {yearlyBudgets.map((yb, yi) => {
                        const x = yi * barGroupWidth + barGroupWidth / 2;
                        return (
                          <text
                            key={yi}
                            x={x}
                            y={yScale(yb) - 6}
                            textAnchor="middle"
                            fontSize={10}
                            fontFamily="JetBrains Mono, monospace"
                            fontWeight={700}
                            fill="#000"
                          >
                            {formatCurrencyCompact(yb)}
                          </text>
                        );
                      })}
                    </g>
                  </svg>
                );
              })()}
            </div>
          </div>

          {/* Cumulative Cost vs Savings Line Chart */}
          <div className="mb-6">
            <span className="text-xs font-semibold uppercase tracking-wider block mb-2">
              Cumulative Investment vs Projected Savings
            </span>
            <div ref={lineChartRef} className="w-full border-2 border-black" style={{ height: 300 }}>
              {lineChartSize.w > 0 && (() => {
                const svgW = lineChartSize.w;
                const svgH = 296;
                const margin = { top: 24, right: 24, bottom: 56, left: 72 };
                const chartW = svgW - margin.left - margin.right;
                const chartH = svgH - margin.top - margin.bottom;
                const allValues = [...cumulativeInvestment, ...projectedSavings];
                const maxVal = Math.max(...allValues) * 1.15;

                const xScale = (i: number) => (i / Math.max(yearCount - 1, 1)) * chartW;
                const yScale = (v: number) => chartH - (v / maxVal) * chartH;

                const investmentPath = cumulativeInvestment
                  .map((v, i) => `${i === 0 ? "M" : "L"}${xScale(i)},${yScale(v)}`)
                  .join(" ");
                const savingsPath = projectedSavings
                  .map((v, i) => `${i === 0 ? "M" : "L"}${xScale(i)},${yScale(v)}`)
                  .join(" ");

                const yTicks: number[] = [];
                const tickStep = maxVal / 5;
                for (let t = 0; t <= maxVal; t += tickStep) {
                  yTicks.push(t);
                }

                // Calculate break-even X position for the vertical line
                let breakEvenX: number | null = null;
                if (breakEvenYear !== null) {
                  breakEvenX = xScale(breakEvenYear);
                }

                return (
                  <svg width={svgW} height={svgH} style={{ display: "block" }}>
                    <g transform={`translate(${margin.left},${margin.top})`}>
                      {/* Y-axis gridlines and labels */}
                      {yTicks.map((tick, ti) => (
                        <g key={ti}>
                          <line
                            x1={0}
                            y1={yScale(tick)}
                            x2={chartW}
                            y2={yScale(tick)}
                            stroke="#e0e0e0"
                            strokeWidth={1}
                          />
                          <text
                            x={-8}
                            y={yScale(tick)}
                            textAnchor="end"
                            dominantBaseline="middle"
                            fontSize={10}
                            fontFamily="JetBrains Mono, monospace"
                            fill="#333"
                          >
                            {formatCurrencyCompact(tick)}
                          </text>
                        </g>
                      ))}

                      {/* Investment line (solid black) */}
                      <path
                        d={investmentPath}
                        fill="none"
                        stroke="#000000"
                        strokeWidth={2.5}
                      />
                      {/* Investment dots */}
                      {cumulativeInvestment.map((v, i) => (
                        <circle
                          key={i}
                          cx={xScale(i)}
                          cy={yScale(v)}
                          r={4}
                          fill="#000000"
                          stroke="white"
                          strokeWidth={1.5}
                        />
                      ))}

                      {/* Savings line (dashed green) */}
                      <path
                        d={savingsPath}
                        fill="none"
                        stroke="#1A6B3C"
                        strokeWidth={2.5}
                        strokeDasharray="8,4"
                      />
                      {/* Savings dots */}
                      {projectedSavings.map((v, i) => (
                        <circle
                          key={i}
                          cx={xScale(i)}
                          cy={yScale(v)}
                          r={4}
                          fill="#1A6B3C"
                          stroke="white"
                          strokeWidth={1.5}
                        />
                      ))}

                      {/* Break-even vertical line */}
                      {breakEvenX !== null && (
                        <>
                          <line
                            x1={breakEvenX}
                            y1={0}
                            x2={breakEvenX}
                            y2={chartH}
                            stroke="#8B1A1A"
                            strokeWidth={2}
                            strokeDasharray="6,3"
                          />
                          <text
                            x={breakEvenX}
                            y={-6}
                            textAnchor="middle"
                            fontSize={10}
                            fontFamily="Inter, sans-serif"
                            fontWeight={700}
                            fill="#8B1A1A"
                          >
                            BREAK-EVEN YEAR
                          </text>
                        </>
                      )}

                      {/* Value labels on data points */}
                      {cumulativeInvestment.map((v, i) => (
                        <text
                          key={`inv-${i}`}
                          x={xScale(i)}
                          y={yScale(v) - 10}
                          textAnchor="middle"
                          fontSize={9}
                          fontFamily="JetBrains Mono, monospace"
                          fontWeight={600}
                          fill="#000"
                        >
                          {formatCurrencyCompact(v)}
                        </text>
                      ))}
                      {projectedSavings.map((v, i) => (
                        v > 0 ? (
                          <text
                            key={`sav-${i}`}
                            x={xScale(i)}
                            y={yScale(v) + 18}
                            textAnchor="middle"
                            fontSize={9}
                            fontFamily="JetBrains Mono, monospace"
                            fontWeight={600}
                            fill="#1A6B3C"
                          >
                            {formatCurrencyCompact(v)}
                          </text>
                        ) : null
                      ))}

                      {/* X-axis labels */}
                      {yearLabels.map((label, i) => {
                        const lines = label.split("\n");
                        return (
                          <g key={i}>
                            {lines.map((line, li) => (
                              <text
                                key={li}
                                x={xScale(i)}
                                y={chartH + 16 + li * 14}
                                textAnchor="middle"
                                fontSize={11}
                                fontFamily="Inter, sans-serif"
                                fontWeight={li === 0 ? 600 : 400}
                                fill="#333"
                              >
                                {line}
                              </text>
                            ))}
                          </g>
                        );
                      })}

                      {/* Y-axis line */}
                      <line x1={0} y1={0} x2={0} y2={chartH} stroke="black" strokeWidth={2} />
                      {/* X-axis line */}
                      <line x1={0} y1={chartH} x2={chartW} y2={chartH} stroke="black" strokeWidth={2} />
                    </g>

                    {/* Legend */}
                    <g transform={`translate(${margin.left + 12},${svgH - 14})`}>
                      <line x1={0} y1={0} x2={20} y2={0} stroke="#000" strokeWidth={2.5} />
                      <text x={26} y={0} dominantBaseline="middle" fontSize={10} fontFamily="Inter, sans-serif" fill="#000">
                        Cumulative Investment
                      </text>
                      <line x1={180} y1={0} x2={200} y2={0} stroke="#1A6B3C" strokeWidth={2.5} strokeDasharray="8,4" />
                      <text x={206} y={0} dominantBaseline="middle" fontSize={10} fontFamily="Inter, sans-serif" fill="#1A6B3C">
                        Projected Savings
                      </text>
                    </g>
                  </svg>
                );
              })()}
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
