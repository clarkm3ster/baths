/**
 * SPHERES Studio — CostTicker Component
 * =======================================
 * Floating cost display positioned in the bottom-right corner.
 *
 * Features:
 * - Running total cost with smooth animation on changes
 * - Click to expand into detailed breakdown panel
 * - Color-coded: green (under budget), yellow (near budget), red (over budget)
 * - Mini bar chart showing cost categories
 * - Net projection (cost - revenue)
 * - Permanence value badge
 */

import { useState, useEffect, useRef, useCallback } from "react";
import type { CostEstimate, CostBreakdownLine } from "../hooks/useCostEstimate";

// ---------------------------------------------------------------------------
// Props
// ---------------------------------------------------------------------------

interface CostTickerProps {
  costs: CostEstimate | null;
  isLoading: boolean;
  budget?: number;
  onExpandClick?: () => void;
}

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

function formatCurrency(value: number): string {
  if (Math.abs(value) >= 1_000_000) {
    return `$${(value / 1_000_000).toFixed(1)}M`;
  }
  if (Math.abs(value) >= 10_000) {
    return `$${(value / 1_000).toFixed(1)}K`;
  }
  return `$${value.toLocaleString("en-US", {
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  })}`;
}

function formatCurrencyFull(value: number): string {
  return `$${value.toLocaleString("en-US", {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  })}`;
}

type BudgetStatus = "under" | "near" | "over";

function getBudgetStatus(totalCost: number, budget: number): BudgetStatus {
  if (budget <= 0) return "under";
  const ratio = totalCost / budget;
  if (ratio > 1.0) return "over";
  if (ratio > 0.85) return "near";
  return "under";
}

const STATUS_COLORS: Record<BudgetStatus, { bg: string; text: string; border: string; glow: string }> = {
  under: {
    bg: "bg-emerald-950/80",
    text: "text-emerald-400",
    border: "border-emerald-600/40",
    glow: "shadow-emerald-500/20",
  },
  near: {
    bg: "bg-amber-950/80",
    text: "text-amber-400",
    border: "border-amber-600/40",
    glow: "shadow-amber-500/20",
  },
  over: {
    bg: "bg-red-950/80",
    text: "text-red-400",
    border: "border-red-600/40",
    glow: "shadow-red-500/20",
  },
};

// ---------------------------------------------------------------------------
// Animated number display
// ---------------------------------------------------------------------------

function useAnimatedValue(target: number, duration: number = 400): number {
  const [display, setDisplay] = useState(target);
  const animFrameRef = useRef<number>(0);
  const startRef = useRef(target);
  const startTimeRef = useRef<number | null>(null);

  useEffect(() => {
    startRef.current = display;
    startTimeRef.current = null;

    const animate = (timestamp: number) => {
      if (startTimeRef.current === null) {
        startTimeRef.current = timestamp;
      }
      const elapsed = timestamp - startTimeRef.current;
      const progress = Math.min(elapsed / duration, 1);

      // Ease-out cubic
      const eased = 1 - Math.pow(1 - progress, 3);
      const current = startRef.current + (target - startRef.current) * eased;

      setDisplay(Math.round(current * 100) / 100);

      if (progress < 1) {
        animFrameRef.current = requestAnimationFrame(animate);
      }
    };

    animFrameRef.current = requestAnimationFrame(animate);

    return () => {
      cancelAnimationFrame(animFrameRef.current);
    };
    // We intentionally only react to target changes, not display
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [target, duration]);

  return display;
}

// ---------------------------------------------------------------------------
// Mini bar chart
// ---------------------------------------------------------------------------

interface CategoryBar {
  label: string;
  value: number;
  color: string;
}

function aggregateCategories(breakdown: CostBreakdownLine[]): CategoryBar[] {
  const categoryMap: Record<string, number> = {};
  for (const line of breakdown) {
    const cat = line.category || "Other";
    categoryMap[cat] = (categoryMap[cat] || 0) + line.total;
  }

  const colorMap: Record<string, string> = {
    Materials: "#34d399",
    Labor: "#60a5fa",
    Permits: "#fbbf24",
    Insurance: "#a78bfa",
    Operations: "#f87171",
    Teardown: "#fb923c",
    Other: "#94a3b8",
  };

  return Object.entries(categoryMap)
    .map(([label, value]) => ({
      label,
      value,
      color: colorMap[label] || colorMap.Other,
    }))
    .sort((a, b) => b.value - a.value);
}

function MiniBarChart({ categories, maxValue }: { categories: CategoryBar[]; maxValue: number }) {
  if (categories.length === 0 || maxValue <= 0) return null;

  return (
    <div className="flex flex-col gap-1 w-full mt-2">
      {categories.map((cat) => {
        const widthPct = Math.max(2, (cat.value / maxValue) * 100);
        return (
          <div key={cat.label} className="flex items-center gap-2">
            <span className="text-[10px] text-zinc-400 w-16 text-right truncate font-mono">
              {cat.label}
            </span>
            <div className="flex-1 h-2 bg-zinc-800 rounded-full overflow-hidden">
              <div
                className="h-full rounded-full transition-all duration-500 ease-out"
                style={{
                  width: `${widthPct}%`,
                  backgroundColor: cat.color,
                }}
              />
            </div>
            <span className="text-[10px] text-zinc-500 w-14 font-mono">
              {formatCurrency(cat.value)}
            </span>
          </div>
        );
      })}
    </div>
  );
}

// ---------------------------------------------------------------------------
// CostTicker Component
// ---------------------------------------------------------------------------

export function CostTicker({
  costs,
  isLoading,
  budget = 0,
  onExpandClick,
}: CostTickerProps) {
  const [isExpanded, setIsExpanded] = useState(false);

  const totalCost = costs?.total_cost ?? 0;
  const netProjection = costs?.net_projection ?? 0;
  const permanenceValue = costs?.permanence_value ?? 0;
  const breakdown = costs?.cost_breakdown ?? [];
  const revenue = costs?.revenue_projections;

  const animatedTotal = useAnimatedValue(totalCost);
  const animatedNet = useAnimatedValue(netProjection);

  const status = getBudgetStatus(totalCost, budget);
  const colors = STATUS_COLORS[status];

  const categories = aggregateCategories(breakdown);
  const maxCatValue = categories.length > 0 ? categories[0].value : 0;

  const totalRevenue = revenue
    ? revenue.ticket_sales +
      revenue.vendor_fees +
      revenue.sponsorship_potential +
      revenue.grant_eligibility
    : 0;

  const handleClick = useCallback(() => {
    if (onExpandClick) {
      onExpandClick();
    } else {
      setIsExpanded((prev) => !prev);
    }
  }, [onExpandClick]);

  // If no cost data at all, show minimal placeholder
  if (!costs && !isLoading) {
    return (
      <div className="fixed bottom-6 right-6 z-50">
        <div
          className="backdrop-blur-xl bg-zinc-900/70 border border-zinc-700/50 rounded-2xl px-5 py-3 shadow-2xl cursor-pointer hover:bg-zinc-800/70 transition-all duration-300"
          onClick={handleClick}
        >
          <div className="flex items-center gap-2">
            <div className="w-2 h-2 rounded-full bg-zinc-600" />
            <span className="text-sm text-zinc-400 font-mono">
              Add elements to see costs
            </span>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="fixed bottom-6 right-6 z-50">
      <div
        className={`
          backdrop-blur-xl ${colors.bg} border ${colors.border}
          rounded-2xl shadow-2xl ${colors.glow} shadow-lg
          transition-all duration-500 ease-out overflow-hidden
          ${isExpanded ? "w-80" : "w-auto"}
          cursor-pointer hover:scale-[1.02]
        `}
        onClick={handleClick}
      >
        {/* -- Collapsed header -- */}
        <div className="px-5 py-3 flex items-center gap-3">
          {/* Status dot */}
          <div className="relative">
            <div
              className={`w-2.5 h-2.5 rounded-full ${
                status === "under"
                  ? "bg-emerald-400"
                  : status === "near"
                  ? "bg-amber-400"
                  : "bg-red-400"
              }`}
            />
            {isLoading && (
              <div className="absolute inset-0 w-2.5 h-2.5 rounded-full bg-white/30 animate-ping" />
            )}
          </div>

          {/* Total cost */}
          <div className="flex flex-col">
            <span className="text-[10px] uppercase tracking-widest text-zinc-500 font-medium">
              Total Cost
            </span>
            <span className={`text-xl font-bold font-mono ${colors.text} tabular-nums`}>
              {formatCurrency(animatedTotal)}
            </span>
          </div>

          {/* Net indicator */}
          <div className="ml-auto flex flex-col items-end">
            <span className="text-[10px] uppercase tracking-widest text-zinc-500 font-medium">
              Net
            </span>
            <span
              className={`text-sm font-bold font-mono tabular-nums ${
                animatedNet >= 0 ? "text-emerald-400" : "text-red-400"
              }`}
            >
              {animatedNet >= 0 ? "+" : ""}
              {formatCurrency(animatedNet)}
            </span>
          </div>

          {/* Expand chevron */}
          <svg
            className={`w-4 h-4 text-zinc-500 transition-transform duration-300 ml-1 ${
              isExpanded ? "rotate-180" : ""
            }`}
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M5 15l7-7 7 7"
            />
          </svg>
        </div>

        {/* -- Expanded panel -- */}
        {isExpanded && (
          <div
            className="px-5 pb-4 border-t border-white/5"
            onClick={(e) => e.stopPropagation()}
          >
            {/* Permanence value badge */}
            {permanenceValue > 0 && (
              <div className="mt-3 flex items-center gap-2 bg-indigo-950/60 border border-indigo-600/30 rounded-lg px-3 py-1.5">
                <svg
                  className="w-4 h-4 text-indigo-400"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"
                  />
                </svg>
                <div className="flex-1">
                  <span className="text-[10px] uppercase tracking-wider text-indigo-400 font-medium">
                    Permanence Value
                  </span>
                  <p className="text-sm font-bold font-mono text-indigo-300">
                    {formatCurrencyFull(permanenceValue)}
                  </p>
                </div>
                <span className="text-[10px] text-indigo-500">stays behind</span>
              </div>
            )}

            {/* Revenue breakdown */}
            {totalRevenue > 0 && (
              <div className="mt-3 space-y-1">
                <span className="text-[10px] uppercase tracking-widest text-zinc-500 font-medium">
                  Revenue Projections
                </span>
                <div className="grid grid-cols-2 gap-x-4 gap-y-0.5">
                  {revenue && revenue.ticket_sales > 0 && (
                    <RevenueRow label="Tickets" value={revenue.ticket_sales} />
                  )}
                  {revenue && revenue.vendor_fees > 0 && (
                    <RevenueRow label="Vendor Fees" value={revenue.vendor_fees} />
                  )}
                  {revenue && revenue.sponsorship_potential > 0 && (
                    <RevenueRow label="Sponsorship" value={revenue.sponsorship_potential} />
                  )}
                  {revenue && revenue.grant_eligibility > 0 && (
                    <RevenueRow label="Grants" value={revenue.grant_eligibility} />
                  )}
                </div>
              </div>
            )}

            {/* Budget status bar */}
            {budget > 0 && (
              <div className="mt-3">
                <div className="flex justify-between text-[10px] text-zinc-500 mb-1">
                  <span>Budget</span>
                  <span>
                    {formatCurrency(totalCost)} / {formatCurrency(budget)}
                  </span>
                </div>
                <div className="h-2 bg-zinc-800 rounded-full overflow-hidden">
                  <div
                    className={`h-full rounded-full transition-all duration-500 ${
                      status === "under"
                        ? "bg-emerald-500"
                        : status === "near"
                        ? "bg-amber-500"
                        : "bg-red-500"
                    }`}
                    style={{
                      width: `${Math.min(100, (totalCost / budget) * 100)}%`,
                    }}
                  />
                </div>
              </div>
            )}

            {/* Mini bar chart */}
            <MiniBarChart categories={categories} maxValue={maxCatValue} />

            {/* ROI with permanence */}
            {costs && costs.roi_with_permanence !== 0 && (
              <div className="mt-3 flex items-center justify-between text-[10px]">
                <span className="text-zinc-500 uppercase tracking-wider">
                  ROI (incl. permanence)
                </span>
                <span
                  className={`font-bold font-mono ${
                    costs.roi_with_permanence >= 0
                      ? "text-emerald-400"
                      : "text-red-400"
                  }`}
                >
                  {costs.roi_with_permanence >= 0 ? "+" : ""}
                  {costs.roi_with_permanence.toFixed(1)}%
                </span>
              </div>
            )}

            {/* View full budget button */}
            {onExpandClick && (
              <button
                className="mt-3 w-full py-2 rounded-lg bg-white/5 hover:bg-white/10 border border-white/10 text-xs text-zinc-300 font-medium transition-colors duration-200"
                onClick={(e) => {
                  e.stopPropagation();
                  onExpandClick();
                }}
              >
                View Full Budget
              </button>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

// ---------------------------------------------------------------------------
// Sub-components
// ---------------------------------------------------------------------------

function RevenueRow({ label, value }: { label: string; value: number }) {
  return (
    <>
      <span className="text-[10px] text-zinc-500 font-mono">{label}</span>
      <span className="text-[10px] text-emerald-400 font-mono text-right">
        +{formatCurrency(value)}
      </span>
    </>
  );
}

export default CostTicker;
