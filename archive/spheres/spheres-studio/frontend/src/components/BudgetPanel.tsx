/**
 * SPHERES Studio — BudgetPanel Component
 * ========================================
 * Full budget detail panel that slides out from the right edge.
 *
 * Features:
 * - Line-item table with categories, items, quantities, unit costs, totals
 * - Permit requirements list with estimated fees
 * - Revenue projections section
 * - Net analysis: total cost vs projected revenue
 * - Permanence value: what stays after the activation ends
 * - ROI calculation including permanence value
 * - Export buttons: CSV, PDF
 * - Budget comparison: shows how design compares to benchmarks
 */

import { useState, useEffect, useCallback, useRef } from "react";
import type {
  CostEstimate,
  CostBreakdownLine,
  RevenueProjections,
} from "../hooks/useCostEstimate";

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

interface PermitInfo {
  permit: string;
  permit_key: string;
  fee_min: number;
  fee_max: number;
  estimated_fee: number;
}

interface BenchmarkData {
  type: string;
  label: string;
  typical_size_sqft: number;
  typical_duration_days: number;
  cost_range: { min: number; max: number };
  description: string;
  estimated_total: number;
}

interface BudgetPanelProps {
  isOpen: boolean;
  onClose: () => void;
  costs: CostEstimate | null;
  isLoading: boolean;
  activationType?: string;
}

// ---------------------------------------------------------------------------
// Formatters
// ---------------------------------------------------------------------------

function fmt(value: number): string {
  return `$${value.toLocaleString("en-US", {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  })}`;
}

function fmtShort(value: number): string {
  if (Math.abs(value) >= 1_000_000) return `$${(value / 1_000_000).toFixed(1)}M`;
  if (Math.abs(value) >= 10_000) return `$${(value / 1_000).toFixed(1)}K`;
  return `$${value.toLocaleString("en-US", {
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  })}`;
}

function fmtPct(value: number): string {
  return `${value >= 0 ? "+" : ""}${value.toFixed(1)}%`;
}

// ---------------------------------------------------------------------------
// Category colors
// ---------------------------------------------------------------------------

const CATEGORY_COLORS: Record<string, string> = {
  Materials: "bg-emerald-500",
  Labor: "bg-blue-500",
  Permits: "bg-amber-500",
  Insurance: "bg-violet-500",
  Operations: "bg-red-400",
  Teardown: "bg-orange-500",
};

function categoryColor(cat: string): string {
  return CATEGORY_COLORS[cat] || "bg-zinc-500";
}

// ---------------------------------------------------------------------------
// CSV export
// ---------------------------------------------------------------------------

function exportCSV(lines: CostBreakdownLine[], costs: CostEstimate): void {
  const rows: string[] = [];
  rows.push("Category,Item,Quantity,Unit Cost,Total");

  for (const line of lines) {
    const item = `"${line.item.replace(/"/g, '""')}"`;
    rows.push(
      `${line.category},${item},${line.quantity},${line.unit_cost.toFixed(2)},${line.total.toFixed(2)}`
    );
  }

  rows.push("");
  rows.push(`,,,,`);
  rows.push(`Total Cost,,,,${costs.total_cost.toFixed(2)}`);

  const rev = costs.revenue_projections;
  rows.push("");
  rows.push("Revenue Projections,,,,");
  rows.push(`Ticket Sales,,,,${rev.ticket_sales.toFixed(2)}`);
  rows.push(`Vendor Fees,,,,${rev.vendor_fees.toFixed(2)}`);
  rows.push(`Sponsorship,,,,${rev.sponsorship_potential.toFixed(2)}`);
  rows.push(`Grant Eligibility,,,,${rev.grant_eligibility.toFixed(2)}`);
  rows.push("");
  rows.push(`Net Projection,,,,${costs.net_projection.toFixed(2)}`);
  rows.push(`Permanence Value,,,,${costs.permanence_value.toFixed(2)}`);
  rows.push(`ROI (with permanence),,,,${costs.roi_with_permanence.toFixed(1)}%`);

  const blob = new Blob([rows.join("\n")], { type: "text/csv;charset=utf-8;" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = `spheres-budget-${new Date().toISOString().slice(0, 10)}.csv`;
  link.click();
  URL.revokeObjectURL(url);
}

// ---------------------------------------------------------------------------
// PDF export (generates a printable HTML page)
// ---------------------------------------------------------------------------

function exportPDF(lines: CostBreakdownLine[], costs: CostEstimate): void {
  const rev = costs.revenue_projections;

  const tableRows = lines
    .map(
      (l) =>
        `<tr>
          <td style="padding:4px 8px;border-bottom:1px solid #e5e7eb;">${l.category}</td>
          <td style="padding:4px 8px;border-bottom:1px solid #e5e7eb;">${l.item}</td>
          <td style="padding:4px 8px;border-bottom:1px solid #e5e7eb;text-align:right;">${l.quantity}</td>
          <td style="padding:4px 8px;border-bottom:1px solid #e5e7eb;text-align:right;">$${l.unit_cost.toFixed(2)}</td>
          <td style="padding:4px 8px;border-bottom:1px solid #e5e7eb;text-align:right;font-weight:600;">$${l.total.toFixed(2)}</td>
        </tr>`
    )
    .join("");

  const html = `
    <!DOCTYPE html>
    <html>
    <head>
      <title>SPHERES Studio Budget</title>
      <style>
        body { font-family: system-ui, -apple-system, sans-serif; max-width: 900px; margin: 0 auto; padding: 40px 20px; color: #1f2937; }
        h1 { font-size: 24px; font-weight: 700; margin-bottom: 4px; }
        h2 { font-size: 18px; font-weight: 600; margin-top: 32px; margin-bottom: 12px; color: #374151; }
        .subtitle { color: #6b7280; font-size: 14px; margin-bottom: 24px; }
        table { width: 100%; border-collapse: collapse; font-size: 13px; }
        th { padding: 8px; text-align: left; border-bottom: 2px solid #1f2937; font-weight: 600; }
        th:nth-child(n+3) { text-align: right; }
        .summary { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-top: 24px; }
        .summary-box { background: #f9fafb; border: 1px solid #e5e7eb; border-radius: 8px; padding: 16px; }
        .summary-label { font-size: 11px; color: #6b7280; text-transform: uppercase; letter-spacing: 0.05em; }
        .summary-value { font-size: 20px; font-weight: 700; margin-top: 4px; }
        .positive { color: #059669; }
        .negative { color: #dc2626; }
        @media print { body { padding: 0; } }
      </style>
    </head>
    <body>
      <h1>SPHERES Studio Budget</h1>
      <p class="subtitle">Generated ${new Date().toLocaleDateString("en-US", { year: "numeric", month: "long", day: "numeric" })}</p>

      <h2>Line-Item Budget</h2>
      <table>
        <thead>
          <tr>
            <th>Category</th>
            <th>Item</th>
            <th style="text-align:right;">Qty</th>
            <th style="text-align:right;">Unit Cost</th>
            <th style="text-align:right;">Total</th>
          </tr>
        </thead>
        <tbody>
          ${tableRows}
          <tr style="font-weight:700;border-top:2px solid #1f2937;">
            <td colspan="4" style="padding:8px;">Total Cost</td>
            <td style="padding:8px;text-align:right;">$${costs.total_cost.toFixed(2)}</td>
          </tr>
        </tbody>
      </table>

      <h2>Revenue Projections</h2>
      <table>
        <tbody>
          <tr><td style="padding:4px 8px;">Ticket Sales</td><td style="padding:4px 8px;text-align:right;">$${rev.ticket_sales.toFixed(2)}</td></tr>
          <tr><td style="padding:4px 8px;">Vendor Fees</td><td style="padding:4px 8px;text-align:right;">$${rev.vendor_fees.toFixed(2)}</td></tr>
          <tr><td style="padding:4px 8px;">Sponsorship Potential</td><td style="padding:4px 8px;text-align:right;">$${rev.sponsorship_potential.toFixed(2)}</td></tr>
          <tr><td style="padding:4px 8px;">Grant Eligibility</td><td style="padding:4px 8px;text-align:right;">$${rev.grant_eligibility.toFixed(2)}</td></tr>
          <tr style="font-weight:700;border-top:2px solid #1f2937;">
            <td style="padding:8px;">Total Revenue</td>
            <td style="padding:8px;text-align:right;">$${(rev.ticket_sales + rev.vendor_fees + rev.sponsorship_potential + rev.grant_eligibility).toFixed(2)}</td>
          </tr>
        </tbody>
      </table>

      <div class="summary">
        <div class="summary-box">
          <div class="summary-label">Net Projection</div>
          <div class="summary-value ${costs.net_projection >= 0 ? "positive" : "negative"}">$${costs.net_projection.toFixed(2)}</div>
        </div>
        <div class="summary-box">
          <div class="summary-label">Permanence Value</div>
          <div class="summary-value positive">$${costs.permanence_value.toFixed(2)}</div>
        </div>
        <div class="summary-box">
          <div class="summary-label">ROI (with Permanence)</div>
          <div class="summary-value ${costs.roi_with_permanence >= 0 ? "positive" : "negative"}">${costs.roi_with_permanence.toFixed(1)}%</div>
        </div>
      </div>
    </body>
    </html>
  `;

  const printWindow = window.open("", "_blank");
  if (printWindow) {
    printWindow.document.write(html);
    printWindow.document.close();
    printWindow.focus();
    setTimeout(() => printWindow.print(), 250);
  }
}

// ---------------------------------------------------------------------------
// Sub-components
// ---------------------------------------------------------------------------

function SectionHeader({ children }: { children: React.ReactNode }) {
  return (
    <h3 className="text-xs uppercase tracking-widest text-zinc-500 font-semibold mt-6 mb-3 flex items-center gap-2">
      <div className="flex-1 h-px bg-zinc-800" />
      <span>{children}</span>
      <div className="flex-1 h-px bg-zinc-800" />
    </h3>
  );
}

function StatCard({
  label,
  value,
  positive,
  subtitle,
}: {
  label: string;
  value: string;
  positive?: boolean;
  subtitle?: string;
}) {
  return (
    <div className="bg-zinc-900/60 border border-zinc-800 rounded-xl p-4">
      <div className="text-[10px] uppercase tracking-widest text-zinc-500 font-medium">
        {label}
      </div>
      <div
        className={`text-xl font-bold font-mono mt-1 ${
          positive === undefined
            ? "text-zinc-200"
            : positive
            ? "text-emerald-400"
            : "text-red-400"
        }`}
      >
        {value}
      </div>
      {subtitle && (
        <div className="text-[10px] text-zinc-600 mt-1">{subtitle}</div>
      )}
    </div>
  );
}

// ---------------------------------------------------------------------------
// BudgetPanel Component
// ---------------------------------------------------------------------------

export function BudgetPanel({
  isOpen,
  onClose,
  costs,
  isLoading,
  activationType = "event",
}: BudgetPanelProps) {
  const [benchmarks, setBenchmarks] = useState<BenchmarkData[]>([]);
  const [benchmarksLoading, setBenchmarksLoading] = useState(false);
  const panelRef = useRef<HTMLDivElement>(null);

  // Fetch benchmarks when panel opens
  useEffect(() => {
    if (isOpen && benchmarks.length === 0) {
      setBenchmarksLoading(true);
      fetch("/api/cost/benchmarks")
        .then((res) => res.json())
        .then((data) => {
          setBenchmarks(data.benchmarks ?? []);
        })
        .catch(() => {
          // Silently fail — benchmarks are supplementary
        })
        .finally(() => {
          setBenchmarksLoading(false);
        });
    }
  }, [isOpen, benchmarks.length]);

  // Close on escape
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === "Escape" && isOpen) {
        onClose();
      }
    };
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  const breakdown = costs?.cost_breakdown ?? [];
  const revenue = costs?.revenue_projections;
  const totalRevenue = revenue
    ? revenue.ticket_sales +
      revenue.vendor_fees +
      revenue.sponsorship_potential +
      revenue.grant_eligibility
    : 0;

  // Group breakdown by category
  const grouped: Record<string, CostBreakdownLine[]> = {};
  for (const line of breakdown) {
    const cat = line.category || "Other";
    if (!grouped[cat]) grouped[cat] = [];
    grouped[cat].push(line);
  }
  const categoryOrder = [
    "Materials",
    "Labor",
    "Permits",
    "Insurance",
    "Operations",
    "Teardown",
  ];
  const sortedCategories = Object.keys(grouped).sort(
    (a, b) =>
      (categoryOrder.indexOf(a) === -1 ? 99 : categoryOrder.indexOf(a)) -
      (categoryOrder.indexOf(b) === -1 ? 99 : categoryOrder.indexOf(b))
  );

  // Find matching benchmark
  const matchingBenchmark = benchmarks.find(
    (b) =>
      b.type === activationType ||
      b.type.replace("event_small", "event").replace("event_large", "event") ===
        activationType
  );

  return (
    <>
      {/* Backdrop */}
      <div
        className="fixed inset-0 z-40 bg-black/50 backdrop-blur-sm transition-opacity duration-300"
        onClick={onClose}
      />

      {/* Panel */}
      <div
        ref={panelRef}
        className="fixed top-0 right-0 bottom-0 z-50 w-full max-w-lg bg-zinc-950 border-l border-zinc-800 shadow-2xl overflow-y-auto transition-transform duration-300 ease-out"
        style={{
          transform: isOpen ? "translateX(0)" : "translateX(100%)",
        }}
      >
        {/* Header */}
        <div className="sticky top-0 z-10 bg-zinc-950/95 backdrop-blur-sm border-b border-zinc-800 px-6 py-4 flex items-center justify-between">
          <div>
            <h2 className="text-lg font-bold text-zinc-100">Full Budget</h2>
            <p className="text-xs text-zinc-500 mt-0.5">
              SPHERES Studio Cost Estimation
            </p>
          </div>
          <div className="flex items-center gap-2">
            {/* Export buttons */}
            {costs && breakdown.length > 0 && (
              <>
                <button
                  onClick={() => exportCSV(breakdown, costs)}
                  className="px-3 py-1.5 rounded-lg bg-zinc-800 hover:bg-zinc-700 text-xs text-zinc-300 font-medium transition-colors border border-zinc-700"
                  title="Export as CSV"
                >
                  CSV
                </button>
                <button
                  onClick={() => exportPDF(breakdown, costs)}
                  className="px-3 py-1.5 rounded-lg bg-zinc-800 hover:bg-zinc-700 text-xs text-zinc-300 font-medium transition-colors border border-zinc-700"
                  title="Export as PDF"
                >
                  PDF
                </button>
              </>
            )}
            <button
              onClick={onClose}
              className="p-1.5 rounded-lg hover:bg-zinc-800 transition-colors"
            >
              <svg
                className="w-5 h-5 text-zinc-400"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M6 18L18 6M6 6l12 12"
                />
              </svg>
            </button>
          </div>
        </div>

        <div className="px-6 pb-8">
          {/* Loading state */}
          {isLoading && !costs && (
            <div className="flex items-center justify-center py-20">
              <div className="flex flex-col items-center gap-3">
                <div className="w-8 h-8 border-2 border-zinc-700 border-t-zinc-400 rounded-full animate-spin" />
                <span className="text-sm text-zinc-500">
                  Calculating costs...
                </span>
              </div>
            </div>
          )}

          {/* Empty state */}
          {!costs && !isLoading && (
            <div className="flex items-center justify-center py-20">
              <div className="text-center">
                <div className="w-12 h-12 mx-auto mb-3 rounded-full bg-zinc-900 flex items-center justify-center">
                  <svg
                    className="w-6 h-6 text-zinc-600"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                    />
                  </svg>
                </div>
                <p className="text-sm text-zinc-500">
                  Add elements to your design to see the budget.
                </p>
              </div>
            </div>
          )}

          {/* Budget content */}
          {costs && (
            <>
              {/* Summary cards */}
              <div className="grid grid-cols-2 gap-3 mt-4">
                <StatCard
                  label="Total Cost"
                  value={fmt(costs.total_cost)}
                />
                <StatCard
                  label="Net Projection"
                  value={fmt(costs.net_projection)}
                  positive={costs.net_projection >= 0}
                />
                <StatCard
                  label="Permanence Value"
                  value={fmt(costs.permanence_value)}
                  positive={costs.permanence_value > 0}
                  subtitle="Community wealth that stays"
                />
                <StatCard
                  label="ROI w/ Permanence"
                  value={fmtPct(costs.roi_with_permanence)}
                  positive={costs.roi_with_permanence >= 0}
                  subtitle="Return including permanent value"
                />
              </div>

              {/* Line-item table by category */}
              <SectionHeader>Line-Item Budget</SectionHeader>
              <div className="border border-zinc-800 rounded-xl overflow-hidden">
                <table className="w-full text-xs">
                  <thead>
                    <tr className="bg-zinc-900/80">
                      <th className="px-3 py-2 text-left font-semibold text-zinc-400">
                        Item
                      </th>
                      <th className="px-3 py-2 text-right font-semibold text-zinc-400 w-12">
                        Qty
                      </th>
                      <th className="px-3 py-2 text-right font-semibold text-zinc-400 w-20">
                        Unit
                      </th>
                      <th className="px-3 py-2 text-right font-semibold text-zinc-400 w-24">
                        Total
                      </th>
                    </tr>
                  </thead>
                  <tbody>
                    {sortedCategories.map((category) => {
                      const items = grouped[category];
                      const catTotal = items.reduce(
                        (sum, l) => sum + l.total,
                        0
                      );
                      return (
                        <CategoryGroup
                          key={category}
                          category={category}
                          items={items}
                          categoryTotal={catTotal}
                        />
                      );
                    })}
                    {/* Grand total row */}
                    <tr className="bg-zinc-900/60 border-t-2 border-zinc-700">
                      <td
                        colSpan={3}
                        className="px-3 py-2.5 text-left font-bold text-zinc-200"
                      >
                        Total Cost
                      </td>
                      <td className="px-3 py-2.5 text-right font-bold text-zinc-200 font-mono">
                        {fmt(costs.total_cost)}
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>

              {/* Permit requirements */}
              {costs.permits_cost.application_fees > 0 && (
                <>
                  <SectionHeader>Permit Requirements</SectionHeader>
                  <PermitsList costs={costs} />
                </>
              )}

              {/* Revenue projections */}
              <SectionHeader>Revenue Projections</SectionHeader>
              <RevenueSection revenue={costs.revenue_projections} />

              {/* Net analysis */}
              <SectionHeader>Net Analysis</SectionHeader>
              <NetAnalysis
                totalCost={costs.total_cost}
                totalRevenue={totalRevenue}
                netProjection={costs.net_projection}
                permanenceValue={costs.permanence_value}
                roiWithPermanence={costs.roi_with_permanence}
              />

              {/* Benchmark comparison */}
              {benchmarks.length > 0 && (
                <>
                  <SectionHeader>Benchmark Comparison</SectionHeader>
                  <BenchmarkComparison
                    benchmarks={benchmarks}
                    currentCost={costs.total_cost}
                    activationType={activationType}
                    isLoading={benchmarksLoading}
                  />
                </>
              )}
            </>
          )}
        </div>
      </div>
    </>
  );
}

// ---------------------------------------------------------------------------
// CategoryGroup — collapsible category rows in the line-item table
// ---------------------------------------------------------------------------

function CategoryGroup({
  category,
  items,
  categoryTotal,
}: {
  category: string;
  items: CostBreakdownLine[];
  categoryTotal: number;
}) {
  const [expanded, setExpanded] = useState(true);

  return (
    <>
      {/* Category header row */}
      <tr
        className="bg-zinc-900/40 cursor-pointer hover:bg-zinc-900/60 transition-colors"
        onClick={() => setExpanded(!expanded)}
      >
        <td colSpan={3} className="px-3 py-2">
          <div className="flex items-center gap-2">
            <div className={`w-2 h-2 rounded-full ${categoryColor(category)}`} />
            <span className="font-semibold text-zinc-300">{category}</span>
            <svg
              className={`w-3 h-3 text-zinc-500 transition-transform duration-200 ${
                expanded ? "rotate-180" : ""
              }`}
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M19 9l-7 7-7-7"
              />
            </svg>
            <span className="text-zinc-600 text-[10px]">
              ({items.length} item{items.length !== 1 ? "s" : ""})
            </span>
          </div>
        </td>
        <td className="px-3 py-2 text-right font-semibold text-zinc-300 font-mono">
          {fmt(categoryTotal)}
        </td>
      </tr>

      {/* Item rows */}
      {expanded &&
        items.map((line, i) => (
          <tr
            key={`${category}-${i}`}
            className="border-t border-zinc-900 hover:bg-zinc-900/20 transition-colors"
          >
            <td className="px-3 py-1.5 pl-7 text-zinc-400">{line.item}</td>
            <td className="px-3 py-1.5 text-right text-zinc-500 font-mono">
              {line.quantity}
            </td>
            <td className="px-3 py-1.5 text-right text-zinc-500 font-mono">
              {fmt(line.unit_cost)}
            </td>
            <td className="px-3 py-1.5 text-right text-zinc-300 font-mono">
              {fmt(line.total)}
            </td>
          </tr>
        ))}
    </>
  );
}

// ---------------------------------------------------------------------------
// PermitsList
// ---------------------------------------------------------------------------

function PermitsList({ costs }: { costs: CostEstimate }) {
  // Derive permits from the breakdown (permit category lines)
  const permitLines = costs.cost_breakdown.filter(
    (l) => l.category === "Permits"
  );

  if (permitLines.length === 0) {
    return (
      <p className="text-xs text-zinc-500 italic">
        No special permits required for current design elements.
      </p>
    );
  }

  return (
    <div className="space-y-2">
      {permitLines.map((p, i) => (
        <div
          key={i}
          className="flex items-center justify-between bg-zinc-900/40 border border-zinc-800 rounded-lg px-4 py-2.5"
        >
          <div className="flex items-center gap-2">
            <svg
              className="w-4 h-4 text-amber-500"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
              />
            </svg>
            <span className="text-xs text-zinc-300 font-medium">
              {p.item}
            </span>
          </div>
          <span className="text-xs font-mono text-amber-400">
            {fmt(p.total)}
          </span>
        </div>
      ))}
      <div className="flex justify-between items-center pt-2 border-t border-zinc-800">
        <span className="text-xs text-zinc-500 font-medium">
          Total permit fees
        </span>
        <span className="text-xs font-mono font-bold text-amber-400">
          {fmt(costs.permits_cost.application_fees)}
        </span>
      </div>
      <div className="flex justify-between items-center">
        <span className="text-xs text-zinc-500 font-medium">
          Insurance (GL + Event)
        </span>
        <span className="text-xs font-mono font-bold text-violet-400">
          {fmt(costs.permits_cost.insurance)}
        </span>
      </div>
    </div>
  );
}

// ---------------------------------------------------------------------------
// RevenueSection
// ---------------------------------------------------------------------------

function RevenueSection({ revenue }: { revenue: RevenueProjections }) {
  const total =
    revenue.ticket_sales +
    revenue.vendor_fees +
    revenue.sponsorship_potential +
    revenue.grant_eligibility;

  const items = [
    { label: "Ticket Sales", value: revenue.ticket_sales, color: "text-emerald-400" },
    { label: "Vendor Fees", value: revenue.vendor_fees, color: "text-blue-400" },
    { label: "Sponsorship", value: revenue.sponsorship_potential, color: "text-violet-400" },
    { label: "Grant Eligibility", value: revenue.grant_eligibility, color: "text-amber-400" },
  ].filter((item) => item.value > 0);

  if (items.length === 0) {
    return (
      <p className="text-xs text-zinc-500 italic">
        No revenue streams projected for current configuration.
      </p>
    );
  }

  return (
    <div className="space-y-2">
      {items.map((item) => (
        <div
          key={item.label}
          className="flex items-center justify-between"
        >
          <span className="text-xs text-zinc-400">{item.label}</span>
          <div className="flex items-center gap-3">
            {/* Mini progress bar relative to total */}
            <div className="w-20 h-1.5 bg-zinc-800 rounded-full overflow-hidden">
              <div
                className="h-full bg-emerald-500 rounded-full transition-all duration-500"
                style={{
                  width: `${total > 0 ? (item.value / total) * 100 : 0}%`,
                }}
              />
            </div>
            <span className={`text-xs font-mono font-bold ${item.color}`}>
              +{fmt(item.value)}
            </span>
          </div>
        </div>
      ))}
      <div className="flex justify-between items-center pt-2 border-t border-zinc-800">
        <span className="text-xs text-zinc-400 font-semibold">
          Total Projected Revenue
        </span>
        <span className="text-xs font-mono font-bold text-emerald-400">
          +{fmt(total)}
        </span>
      </div>
    </div>
  );
}

// ---------------------------------------------------------------------------
// NetAnalysis
// ---------------------------------------------------------------------------

function NetAnalysis({
  totalCost,
  totalRevenue,
  netProjection,
  permanenceValue,
  roiWithPermanence,
}: {
  totalCost: number;
  totalRevenue: number;
  netProjection: number;
  permanenceValue: number;
  roiWithPermanence: number;
}) {
  // Visual bar showing cost vs revenue proportions
  const maxVal = Math.max(totalCost, totalRevenue + permanenceValue, 1);
  const costPct = (totalCost / maxVal) * 100;
  const revPct = (totalRevenue / maxVal) * 100;
  const permPct = (permanenceValue / maxVal) * 100;

  return (
    <div className="space-y-4">
      {/* Visual comparison */}
      <div className="space-y-2">
        {/* Cost bar */}
        <div>
          <div className="flex justify-between text-[10px] text-zinc-500 mb-1">
            <span>Total Cost</span>
            <span className="font-mono">{fmt(totalCost)}</span>
          </div>
          <div className="h-3 bg-zinc-800 rounded-full overflow-hidden">
            <div
              className="h-full bg-red-500/70 rounded-full transition-all duration-500"
              style={{ width: `${costPct}%` }}
            />
          </div>
        </div>

        {/* Revenue + Permanence bar */}
        <div>
          <div className="flex justify-between text-[10px] text-zinc-500 mb-1">
            <span>Revenue + Permanence</span>
            <span className="font-mono">
              {fmt(totalRevenue + permanenceValue)}
            </span>
          </div>
          <div className="h-3 bg-zinc-800 rounded-full overflow-hidden flex">
            <div
              className="h-full bg-emerald-500/70 transition-all duration-500"
              style={{ width: `${revPct}%` }}
            />
            <div
              className="h-full bg-indigo-500/70 transition-all duration-500"
              style={{ width: `${permPct}%` }}
            />
          </div>
          <div className="flex gap-4 mt-1">
            <div className="flex items-center gap-1">
              <div className="w-2 h-2 rounded-full bg-emerald-500/70" />
              <span className="text-[9px] text-zinc-600">Revenue</span>
            </div>
            <div className="flex items-center gap-1">
              <div className="w-2 h-2 rounded-full bg-indigo-500/70" />
              <span className="text-[9px] text-zinc-600">Permanence</span>
            </div>
          </div>
        </div>
      </div>

      {/* Net result */}
      <div
        className={`rounded-xl p-4 border ${
          netProjection >= 0
            ? "bg-emerald-950/30 border-emerald-600/30"
            : "bg-red-950/30 border-red-600/30"
        }`}
      >
        <div className="flex items-center justify-between">
          <div>
            <div className="text-[10px] uppercase tracking-wider text-zinc-500">
              Net Financial Projection
            </div>
            <div
              className={`text-2xl font-bold font-mono mt-1 ${
                netProjection >= 0 ? "text-emerald-400" : "text-red-400"
              }`}
            >
              {netProjection >= 0 ? "+" : ""}
              {fmt(netProjection)}
            </div>
          </div>
          <div className="text-right">
            <div className="text-[10px] uppercase tracking-wider text-zinc-500">
              ROI w/ Permanence
            </div>
            <div
              className={`text-lg font-bold font-mono mt-1 ${
                roiWithPermanence >= 0 ? "text-emerald-400" : "text-red-400"
              }`}
            >
              {fmtPct(roiWithPermanence)}
            </div>
          </div>
        </div>
      </div>

      {/* Permanence value callout */}
      {permanenceValue > 0 && (
        <div className="bg-indigo-950/30 border border-indigo-600/20 rounded-xl p-4">
          <div className="flex items-start gap-3">
            <svg
              className="w-5 h-5 text-indigo-400 mt-0.5 shrink-0"
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
            <div>
              <div className="text-xs font-semibold text-indigo-300">
                Permanence Value: {fmt(permanenceValue)}
              </div>
              <p className="text-[11px] text-indigo-400/70 mt-1 leading-relaxed">
                This is the estimated value of permanent improvements that remain
                in the community after the activation ends. Benches, planters,
                trees, murals, paths, and infrastructure that become lasting
                public assets.
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

// ---------------------------------------------------------------------------
// BenchmarkComparison
// ---------------------------------------------------------------------------

function BenchmarkComparison({
  benchmarks,
  currentCost,
  activationType,
  isLoading,
}: {
  benchmarks: BenchmarkData[];
  currentCost: number;
  activationType: string;
  isLoading: boolean;
}) {
  if (isLoading) {
    return (
      <div className="flex items-center gap-2 py-4">
        <div className="w-4 h-4 border-2 border-zinc-700 border-t-zinc-400 rounded-full animate-spin" />
        <span className="text-xs text-zinc-500">Loading benchmarks...</span>
      </div>
    );
  }

  if (benchmarks.length === 0) return null;

  // Find the max cost for scaling
  const allValues = [
    ...benchmarks.map((b) => b.cost_range.max),
    currentCost,
  ];
  const maxCost = Math.max(...allValues, 1);

  return (
    <div className="space-y-3">
      {/* Current project indicator */}
      <div className="bg-zinc-900/60 border border-zinc-700 rounded-lg px-4 py-2.5">
        <div className="flex items-center justify-between mb-1.5">
          <span className="text-xs font-semibold text-zinc-200">
            Your Design
          </span>
          <span className="text-xs font-mono font-bold text-zinc-200">
            {fmtShort(currentCost)}
          </span>
        </div>
        <div className="h-2 bg-zinc-800 rounded-full overflow-hidden">
          <div
            className="h-full bg-white/60 rounded-full transition-all duration-500"
            style={{
              width: `${(currentCost / maxCost) * 100}%`,
            }}
          />
        </div>
      </div>

      {/* Benchmark bars */}
      {benchmarks.map((bench) => {
        const isMatch = bench.type === activationType;
        const minPct = (bench.cost_range.min / maxCost) * 100;
        const maxPct = (bench.cost_range.max / maxCost) * 100;

        return (
          <div
            key={bench.type}
            className={`rounded-lg px-4 py-2.5 ${
              isMatch
                ? "bg-emerald-950/30 border border-emerald-600/20"
                : "bg-zinc-900/30"
            }`}
          >
            <div className="flex items-center justify-between mb-1.5">
              <div className="flex items-center gap-2">
                <span
                  className={`text-xs font-medium ${
                    isMatch ? "text-emerald-300" : "text-zinc-400"
                  }`}
                >
                  {bench.label}
                </span>
                {isMatch && (
                  <span className="text-[9px] bg-emerald-800/50 text-emerald-400 px-1.5 py-0.5 rounded-full font-medium">
                    match
                  </span>
                )}
              </div>
              <span className="text-[10px] font-mono text-zinc-500">
                {fmtShort(bench.cost_range.min)} - {fmtShort(bench.cost_range.max)}
              </span>
            </div>
            <div className="h-2 bg-zinc-800 rounded-full overflow-hidden relative">
              {/* Range bar */}
              <div
                className={`absolute top-0 h-full rounded-full transition-all duration-500 ${
                  isMatch ? "bg-emerald-500/50" : "bg-zinc-600/50"
                }`}
                style={{
                  left: `${minPct}%`,
                  width: `${maxPct - minPct}%`,
                }}
              />
            </div>
          </div>
        );
      })}

      <p className="text-[10px] text-zinc-600 leading-relaxed mt-2">
        Benchmarks show typical cost ranges for similar activations in
        Philadelphia. Your design may vary based on specific materials,
        location, and duration.
      </p>
    </div>
  );
}

export default BudgetPanel;
