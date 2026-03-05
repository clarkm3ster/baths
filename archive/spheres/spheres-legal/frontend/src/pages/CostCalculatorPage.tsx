import { useState } from "react";
import {
  Calculator,
  DollarSign,
  Clock,
  FileText,
  ArrowRight,
  AlertTriangle,
} from "lucide-react";

interface PathwayStep {
  order: number;
  permit_name: string;
  action: string;
  timeline_days: number;
  cost: number;
}

interface CostBreakdown {
  permits: { name: string; cost: number }[];
  legal_review: number;
  insurance: number;
  total_permits: number;
  total_all: number;
  timeline_days: number;
  steps: PathwayStep[];
  warnings: string[];
}

const PARCEL_TYPES = [
  "park",
  "vacant_lot",
  "street",
  "sidewalk",
  "plaza",
  "parking_lot",
];

const ACTIVATION_TYPES = [
  "event",
  "food_vendor",
  "art_installation",
  "community_garden",
  "pop_up_market",
  "performance",
  "film_shoot",
  "temporary_structure",
  "block_party",
  "sidewalk_cafe",
];

const DURATION_OPTIONS = [
  { label: "1 Day", days: 1 },
  { label: "1 Week", days: 7 },
  { label: "1 Month", days: 30 },
  { label: "3 Months", days: 90 },
  { label: "6 Months", days: 180 },
  { label: "1 Year", days: 365 },
];

function fmt(n: number) {
  return n.toLocaleString("en-US", {
    style: "currency",
    currency: "USD",
    maximumFractionDigits: 0,
  });
}

function label(s: string) {
  return s.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());
}

export default function CostCalculatorPage() {
  const [parcelType, setParcelType] = useState("");
  const [activationType, setActivationType] = useState("");
  const [duration, setDuration] = useState(1);
  const [needsInsurance, setNeedsInsurance] = useState(true);
  const [needsLegalReview, setNeedsLegalReview] = useState(true);
  const [result, setResult] = useState<CostBreakdown | null>(null);
  const [loading, setLoading] = useState(false);

  const calculate = async () => {
    if (!parcelType || !activationType) return;
    setLoading(true);

    // Get permit pathway
    const r = await fetch("/api/permits/pathway", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        parcel_type: parcelType,
        zoning: "CMX-2",
        activation_type: activationType,
      }),
    });
    const pathway = await r.json();

    // Calculate costs
    const permits = pathway.permits_required.map(
      (p: { name: string; cost_range: { min: number; max: number } }) => ({
        name: p.name,
        cost: Math.round((p.cost_range.min + p.cost_range.max) / 2),
      })
    );
    const totalPermits = permits.reduce(
      (sum: number, p: { cost: number }) => sum + p.cost,
      0
    );

    // Legal review estimate: $250/hr, varies by complexity
    const legalHours = permits.length * 2;
    const legalReview = needsLegalReview ? legalHours * 250 : 0;

    // Insurance: $500 base + $100/month for general liability
    const months = Math.max(1, Math.ceil(duration / 30));
    const insurance = needsInsurance ? 500 + months * 100 : 0;

    setResult({
      permits,
      legal_review: legalReview,
      insurance,
      total_permits: totalPermits,
      total_all: totalPermits + legalReview + insurance,
      timeline_days: pathway.total_timeline_days,
      steps: pathway.steps,
      warnings: pathway.warnings,
    });
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-void pt-20 px-6 pb-20">
      <div className="max-w-5xl mx-auto">
        {/* Header */}
        <div className="mb-12">
          <p className="section-label mb-3">COST CALCULATOR</p>
          <h1 className="text-3xl font-light tracking-tight mb-2">
            Total Activation Cost
          </h1>
          <p className="text-silver">
            Permits, legal review, and insurance — the complete cost of
            activating public space. No surprises.
          </p>
        </div>

        {/* Calculator form */}
        <div className="card mb-8">
          <h2 className="text-sm font-mono font-bold text-legal-green tracking-wider uppercase mb-6">
            Configure Your Activation
          </h2>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
            <div>
              <label className="data-label block mb-2">Parcel Type</label>
              <select
                value={parcelType}
                onChange={(e) => setParcelType(e.target.value)}
                className="w-full bg-ash border border-steel text-snow p-3 font-sans text-sm appearance-none cursor-pointer"
              >
                <option value="">Select...</option>
                {PARCEL_TYPES.map((t) => (
                  <option key={t} value={t}>
                    {label(t)}
                  </option>
                ))}
              </select>
            </div>
            <div>
              <label className="data-label block mb-2">Activation Type</label>
              <select
                value={activationType}
                onChange={(e) => setActivationType(e.target.value)}
                className="w-full bg-ash border border-steel text-snow p-3 font-sans text-sm appearance-none cursor-pointer"
              >
                <option value="">Select...</option>
                {ACTIVATION_TYPES.map((t) => (
                  <option key={t} value={t}>
                    {label(t)}
                  </option>
                ))}
              </select>
            </div>
          </div>

          <div className="mb-6">
            <label className="data-label block mb-2">Duration</label>
            <div className="flex gap-2 flex-wrap">
              {DURATION_OPTIONS.map((d) => (
                <button
                  key={d.days}
                  onClick={() => setDuration(d.days)}
                  className={`tag cursor-pointer ${
                    duration === d.days ? "tag-green" : ""
                  }`}
                >
                  {d.label}
                </button>
              ))}
            </div>
          </div>

          <div className="flex gap-6 mb-6">
            <label className="flex items-center gap-2 cursor-pointer">
              <input
                type="checkbox"
                checked={needsInsurance}
                onChange={(e) => setNeedsInsurance(e.target.checked)}
                className="accent-legal-green"
              />
              <span className="text-sm text-silver">
                Include insurance estimate
              </span>
            </label>
            <label className="flex items-center gap-2 cursor-pointer">
              <input
                type="checkbox"
                checked={needsLegalReview}
                onChange={(e) => setNeedsLegalReview(e.target.checked)}
                className="accent-legal-green"
              />
              <span className="text-sm text-silver">
                Include legal review estimate
              </span>
            </label>
          </div>

          <button
            onClick={calculate}
            disabled={!parcelType || !activationType || loading}
            className="btn-primary disabled:opacity-40"
          >
            <Calculator size={16} />
            {loading ? "Calculating..." : "Calculate Total Cost"}
          </button>
        </div>

        {/* Results */}
        {result && (
          <div>
            {/* Plain-language summary */}
            <div className="border border-legal-green/30 bg-legal-green/5 p-5 mb-8">
              <p className="text-lg text-snow leading-relaxed">
                A{" "}
                <span className="text-legal-green font-medium">
                  {DURATION_OPTIONS.find((d) => d.days === duration)?.label.toLowerCase() || `${duration}-day`}
                </span>{" "}
                <span className="text-legal-green font-medium">
                  {label(activationType).toLowerCase()}
                </span>{" "}
                on a{" "}
                <span className="text-legal-green font-medium">
                  {label(parcelType).toLowerCase()}
                </span>{" "}
                costs{" "}
                <span className="font-mono font-bold text-legal-green">
                  {fmt(result.total_all)}
                </span>{" "}
                in legal/permit fees and takes{" "}
                <span className="font-mono font-bold text-legal-amber">
                  {result.timeline_days} days
                </span>
                .
              </p>
            </div>

            {/* Summary cards */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-px bg-ash mb-8">
              <div className="card bg-void">
                <div className="flex items-center gap-2 mb-2">
                  <DollarSign size={16} className="text-legal-green" />
                  <p className="data-label">Total Cost</p>
                </div>
                <p className="data-value text-legal-green">
                  {fmt(result.total_all)}
                </p>
              </div>
              <div className="card bg-void">
                <div className="flex items-center gap-2 mb-2">
                  <FileText size={16} className="text-silver" />
                  <p className="data-label">Permit Fees</p>
                </div>
                <p className="data-value">{fmt(result.total_permits)}</p>
              </div>
              <div className="card bg-void">
                <div className="flex items-center gap-2 mb-2">
                  <Clock size={16} className="text-legal-amber" />
                  <p className="data-label">Timeline</p>
                </div>
                <p className="data-value">{result.timeline_days} days</p>
              </div>
              <div className="card bg-void">
                <div className="flex items-center gap-2 mb-2">
                  <FileText size={16} className="text-silver" />
                  <p className="data-label">Permits Needed</p>
                </div>
                <p className="data-value">{result.permits.length}</p>
              </div>
            </div>

            {/* Warnings */}
            {result.warnings.length > 0 && (
              <div className="border border-legal-amber/30 bg-legal-amber/5 p-4 mb-8">
                {result.warnings.map((w, i) => (
                  <div
                    key={i}
                    className="flex items-start gap-2 mb-1 last:mb-0"
                  >
                    <AlertTriangle
                      size={14}
                      className="text-legal-amber mt-0.5 shrink-0"
                    />
                    <p className="text-sm text-legal-amber">{w}</p>
                  </div>
                ))}
              </div>
            )}

            {/* Cost breakdown */}
            <div className="card mb-8">
              <h3 className="text-sm font-mono font-bold text-legal-green tracking-wider uppercase mb-4">
                Cost Breakdown
              </h3>
              <div className="space-y-2">
                {result.permits.map((p) => (
                  <div
                    key={p.name}
                    className="flex items-center justify-between py-2 border-b border-ash last:border-0"
                  >
                    <div className="flex items-center gap-2">
                      <FileText size={14} className="text-steel" />
                      <span className="text-sm">{p.name}</span>
                    </div>
                    <span className="font-mono text-sm">{fmt(p.cost)}</span>
                  </div>
                ))}
                {needsLegalReview && (
                  <div className="flex items-center justify-between py-2 border-b border-ash">
                    <span className="text-sm text-silver">
                      Legal Review (est.)
                    </span>
                    <span className="font-mono text-sm text-silver">
                      {fmt(result.legal_review)}
                    </span>
                  </div>
                )}
                {needsInsurance && (
                  <div className="flex items-center justify-between py-2 border-b border-ash">
                    <span className="text-sm text-silver">
                      Insurance (est.)
                    </span>
                    <span className="font-mono text-sm text-silver">
                      {fmt(result.insurance)}
                    </span>
                  </div>
                )}
                <div className="flex items-center justify-between pt-3 mt-2 border-t border-legal-green/30">
                  <span className="font-medium">Total</span>
                  <span className="font-mono font-bold text-lg text-legal-green">
                    {fmt(result.total_all)}
                  </span>
                </div>
              </div>
            </div>

            {/* Timeline steps */}
            <div className="card">
              <h3 className="text-sm font-mono font-bold text-legal-green tracking-wider uppercase mb-4">
                Step-by-Step Timeline
              </h3>
              <div className="space-y-0">
                {result.steps.map((step, i) => (
                  <div
                    key={i}
                    className="flex items-start gap-4 p-3 border-l-2 border-legal-green/30 hover:border-legal-green transition-colors"
                  >
                    <div className="w-8 h-8 border border-legal-green flex items-center justify-center shrink-0">
                      <span className="font-mono text-xs font-bold text-legal-green">
                        {step.order}
                      </span>
                    </div>
                    <div className="flex-1">
                      <p className="font-medium text-sm">{step.permit_name}</p>
                      <p className="text-silver text-xs mt-0.5">
                        {step.action}
                      </p>
                    </div>
                    <div className="text-right shrink-0">
                      <p className="font-mono text-xs text-silver">
                        {step.timeline_days} days
                      </p>
                      <p className="font-mono text-xs text-legal-green">
                        {fmt(step.cost)}
                      </p>
                    </div>
                  </div>
                ))}
              </div>
              <div className="mt-4 pt-4 border-t border-ash flex items-center justify-between">
                <span className="text-sm text-silver">
                  Start to activation:
                </span>
                <span className="font-mono font-bold text-legal-amber">
                  {result.timeline_days} days
                </span>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
