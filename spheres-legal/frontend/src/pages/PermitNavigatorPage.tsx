import { useState, useEffect } from "react";
import {
  FileText,
  Clock,
  DollarSign,
  AlertTriangle,
  ChevronRight,
  Search,
  CheckCircle2,
} from "lucide-react";

interface Permit {
  id: string;
  name: string;
  issuing_agency: string;
  description: string;
  application_process: string[];
  timeline_days: number;
  cost_range: { min: number; max: number };
  requirements: string[];
  restrictions: string[];
  seasonal_limitations: string[] | null;
  applicable_zoning: string[];
  applicable_property_types: string[];
}

interface PathwayStep {
  order: number;
  permit_name: string;
  action: string;
  timeline_days: number;
  cost: number;
}

interface Pathway {
  permits_required: Permit[];
  total_timeline_days: number;
  total_cost_range: { min: number; max: number };
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

function fmt(n: number) {
  return n.toLocaleString("en-US", { style: "currency", currency: "USD", maximumFractionDigits: 0 });
}

function label(s: string) {
  return s.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());
}

export default function PermitNavigatorPage() {
  const [permits, setPermits] = useState<Permit[]>([]);
  const [parcelType, setParcelType] = useState("");
  const [activationType, setActivationType] = useState("");
  const [pathway, setPathway] = useState<Pathway | null>(null);
  const [loading, setLoading] = useState(false);
  const [expandedPermit, setExpandedPermit] = useState<string | null>(null);
  const [filter, setFilter] = useState("");

  useEffect(() => {
    fetch("/api/permits")
      .then((r) => r.json())
      .then((d) => setPermits(d.permits || d));
  }, []);

  const findPathway = async () => {
    if (!parcelType || !activationType) return;
    setLoading(true);
    const r = await fetch("/api/permits/pathway", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        parcel_type: parcelType,
        zoning: "CMX-2",
        activation_type: activationType,
      }),
    });
    const d = await r.json();
    setPathway(d);
    setLoading(false);
  };

  const filtered = permits.filter(
    (p) =>
      !filter ||
      p.name.toLowerCase().includes(filter.toLowerCase()) ||
      p.issuing_agency.toLowerCase().includes(filter.toLowerCase())
  );

  return (
    <div className="min-h-screen bg-void pt-20 px-6 pb-20">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="mb-12">
          <p className="section-label mb-3">PERMIT NAVIGATOR</p>
          <h1 className="text-3xl font-light tracking-tight mb-2">
            Find Your Pathway
          </h1>
          <p className="text-silver">
            Select a parcel type and activation to get the exact permits,
            timeline, and cost.
          </p>
        </div>

        {/* Pathway Builder */}
        <div className="card mb-12">
          <h2 className="text-sm font-mono font-bold text-legal-green tracking-wider uppercase mb-6">
            Pathway Builder
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
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
            <div className="flex items-end">
              <button
                onClick={findPathway}
                disabled={!parcelType || !activationType || loading}
                className="btn-primary w-full justify-center disabled:opacity-40"
              >
                {loading ? "Searching..." : "Find Pathway"}
              </button>
            </div>
          </div>
        </div>

        {/* Pathway Results */}
        {pathway && (
          <div className="mb-16">
            <h2 className="text-sm font-mono font-bold text-legal-green tracking-wider uppercase mb-6">
              Your Pathway
            </h2>

            {/* Summary */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-px bg-ash mb-8">
              <div className="card bg-void">
                <div className="flex items-center gap-2 mb-2">
                  <FileText size={16} className="text-legal-green" />
                  <p className="data-label">Permits Required</p>
                </div>
                <p className="data-value">
                  {pathway.permits_required.length}
                </p>
              </div>
              <div className="card bg-void">
                <div className="flex items-center gap-2 mb-2">
                  <Clock size={16} className="text-legal-amber" />
                  <p className="data-label">Total Timeline</p>
                </div>
                <p className="data-value">
                  {pathway.total_timeline_days} days
                </p>
              </div>
              <div className="card bg-void">
                <div className="flex items-center gap-2 mb-2">
                  <DollarSign size={16} className="text-legal-green" />
                  <p className="data-label">Cost Range</p>
                </div>
                <p className="data-value">
                  {fmt(pathway.total_cost_range.min)} —{" "}
                  {fmt(pathway.total_cost_range.max)}
                </p>
              </div>
            </div>

            {/* Warnings */}
            {pathway.warnings.length > 0 && (
              <div className="border border-legal-amber/30 bg-legal-amber/5 p-4 mb-8">
                {pathway.warnings.map((w, i) => (
                  <div key={i} className="flex items-start gap-2 mb-1 last:mb-0">
                    <AlertTriangle
                      size={14}
                      className="text-legal-amber mt-0.5 shrink-0"
                    />
                    <p className="text-sm text-legal-amber">{w}</p>
                  </div>
                ))}
              </div>
            )}

            {/* Steps */}
            <div className="space-y-0">
              {pathway.steps.map((step, i) => (
                <div
                  key={i}
                  className="flex items-start gap-4 p-4 border-l-2 border-legal-green/30 hover:border-legal-green transition-colors"
                >
                  <div className="w-8 h-8 border border-legal-green flex items-center justify-center shrink-0">
                    <span className="font-mono text-sm font-bold text-legal-green">
                      {step.order}
                    </span>
                  </div>
                  <div className="flex-1">
                    <p className="font-medium text-sm">{step.permit_name}</p>
                    <p className="text-silver text-sm mt-1">{step.action}</p>
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
          </div>
        )}

        {/* All Permits */}
        <div>
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-sm font-mono font-bold text-legal-green tracking-wider uppercase">
              All Permits ({filtered.length})
            </h2>
            <div className="relative">
              <Search
                size={14}
                className="absolute left-3 top-1/2 -translate-y-1/2 text-slate"
              />
              <input
                type="text"
                placeholder="Filter..."
                value={filter}
                onChange={(e) => setFilter(e.target.value)}
                className="bg-ash border border-steel text-snow pl-9 pr-4 py-2 text-sm font-mono w-64"
              />
            </div>
          </div>

          <div className="space-y-px">
            {filtered.map((p) => (
              <div key={p.id} className="card bg-smoke">
                <button
                  onClick={() =>
                    setExpandedPermit(expandedPermit === p.id ? null : p.id)
                  }
                  className="w-full flex items-center justify-between text-left"
                >
                  <div>
                    <h3 className="font-medium text-sm">{p.name}</h3>
                    <p className="text-silver text-xs mt-0.5">
                      {p.issuing_agency}
                    </p>
                  </div>
                  <div className="flex items-center gap-4">
                    <span className="tag">
                      {p.timeline_days} days
                    </span>
                    <span className="tag tag-green">
                      {fmt(p.cost_range.min)}–{fmt(p.cost_range.max)}
                    </span>
                    <ChevronRight
                      size={16}
                      className={`text-steel transition-transform ${
                        expandedPermit === p.id ? "rotate-90" : ""
                      }`}
                    />
                  </div>
                </button>

                {expandedPermit === p.id && (
                  <div className="mt-4 pt-4 border-t border-ash">
                    <p className="text-silver text-sm mb-4">{p.description}</p>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                      <div>
                        <p className="data-label mb-2">Application Process</p>
                        <ol className="space-y-1.5">
                          {p.application_process.map((step, i) => (
                            <li
                              key={i}
                              className="flex items-start gap-2 text-sm text-cloud"
                            >
                              <CheckCircle2
                                size={14}
                                className="text-legal-green mt-0.5 shrink-0"
                              />
                              {step}
                            </li>
                          ))}
                        </ol>
                      </div>
                      <div>
                        <p className="data-label mb-2">Requirements</p>
                        <ul className="space-y-1">
                          {p.requirements.map((r, i) => (
                            <li
                              key={i}
                              className="text-sm text-cloud flex items-start gap-2"
                            >
                              <span className="text-steel mt-1">—</span>
                              {r}
                            </li>
                          ))}
                        </ul>
                        {p.restrictions.length > 0 && (
                          <>
                            <p className="data-label mb-2 mt-4">Restrictions</p>
                            <ul className="space-y-1">
                              {p.restrictions.map((r, i) => (
                                <li
                                  key={i}
                                  className="text-sm text-legal-amber flex items-start gap-2"
                                >
                                  <span className="mt-1">—</span>
                                  {r}
                                </li>
                              ))}
                            </ul>
                          </>
                        )}
                      </div>
                    </div>

                    {p.seasonal_limitations && p.seasonal_limitations.length > 0 && (
                      <div className="mt-4">
                        <p className="data-label mb-2">Seasonal Limitations</p>
                        <div className="flex gap-2 flex-wrap">
                          {p.seasonal_limitations.map((s, i) => (
                            <span key={i} className="tag tag-amber">
                              {s}
                            </span>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
