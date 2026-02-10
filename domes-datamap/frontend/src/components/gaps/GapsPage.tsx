import { useState, useEffect, useMemo } from "react";
import type { Gap } from "../../types";
import { DOMAINS } from "../../types";
import { getGaps } from "../../api/client";
import { DomainBadge } from "../badges/DomainBadge";
import { SeverityBadge } from "../badges/SeverityBadge";
import { BarrierBadge } from "../badges/BarrierBadge";
import { GapDetail } from "./GapDetail";

const SEVERITY_OPTIONS = ["critical", "high", "moderate", "low"];
const BARRIER_OPTIONS = ["legal", "technical", "political", "consent", "funding"];

export function GapsPage() {
  const [gaps, setGaps] = useState<Gap[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedGap, setSelectedGap] = useState<number | null>(null);

  // Filters
  const [severityFilter, setSeverityFilter] = useState("");
  const [barrierFilter, setBarrierFilter] = useState("");
  const [consentFilter, setConsentFilter] = useState("");
  const [domainFilter, setDomainFilter] = useState("");
  const [sortBy, setSortBy] = useState<"severity" | "cost" | "barrier">(
    "severity"
  );

  useEffect(() => {
    setLoading(true);
    getGaps()
      .then(setGaps)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, []);

  const filtered = useMemo(() => {
    let result = gaps.filter((g) => {
      if (severityFilter && g.severity !== severityFilter) return false;
      if (barrierFilter && g.barrier_type !== barrierFilter) return false;
      if (consentFilter === "true" && !g.consent_closable) return false;
      if (consentFilter === "false" && g.consent_closable) return false;
      return true;
    });

    const severityOrder: Record<string, number> = {
      critical: 0,
      high: 1,
      moderate: 2,
      low: 3,
    };
    if (sortBy === "severity") {
      result.sort(
        (a, b) =>
          (severityOrder[a.severity] ?? 9) - (severityOrder[b.severity] ?? 9)
      );
    }

    return result;
  }, [gaps, severityFilter, barrierFilter, consentFilter, domainFilter, sortBy]);

  const consentCount = useMemo(
    () => gaps.filter((g) => g.consent_closable).length,
    [gaps]
  );

  return (
    <div className="flex flex-col h-[calc(100vh-3.5rem)]">
      {/* Header */}
      <div className="border-b border-black px-4 py-2 bg-gray-50">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="font-serif text-lg font-bold uppercase tracking-wide">
              Gap Dashboard
            </h2>
            <p className="font-mono text-[0.625rem] text-gray-500 uppercase tracking-wider">
              {filtered.length} gaps / {consentCount} consent-closable
            </p>
          </div>
          {/* Summary stats */}
          <div className="flex gap-2">
            {SEVERITY_OPTIONS.map((sev) => {
              const count = gaps.filter((g) => g.severity === sev).length;
              return (
                <div key={sev} className="stat-block px-3 py-1">
                  <div
                    className="stat-value text-sm"
                    style={{
                      color:
                        sev === "critical"
                          ? "#DC2626"
                          : sev === "high"
                          ? "#EA580C"
                          : sev === "moderate"
                          ? "#CA8A04"
                          : "#6B7280",
                    }}
                  >
                    {count}
                  </div>
                  <div className="stat-label">{sev}</div>
                </div>
              );
            })}
          </div>
        </div>
      </div>

      {/* Filter Bar */}
      <div className="filter-bar mx-0 border-x-0 border-t-0">
        <label className="font-mono text-[0.625rem] uppercase tracking-wider text-gray-500">
          Filter:
        </label>
        <select
          className="filter-select"
          value={severityFilter}
          onChange={(e) => setSeverityFilter(e.target.value)}
        >
          <option value="">All Severities</option>
          {SEVERITY_OPTIONS.map((s) => (
            <option key={s} value={s}>
              {s}
            </option>
          ))}
        </select>
        <select
          className="filter-select"
          value={barrierFilter}
          onChange={(e) => setBarrierFilter(e.target.value)}
        >
          <option value="">All Barriers</option>
          {BARRIER_OPTIONS.map((b) => (
            <option key={b} value={b}>
              {b}
            </option>
          ))}
        </select>
        <select
          className="filter-select"
          value={consentFilter}
          onChange={(e) => setConsentFilter(e.target.value)}
        >
          <option value="">All Consent</option>
          <option value="true">Consent-Closable</option>
          <option value="false">Not Consent-Closable</option>
        </select>
        <select
          className="filter-select"
          value={sortBy}
          onChange={(e) =>
            setSortBy(e.target.value as "severity" | "cost" | "barrier")
          }
        >
          <option value="severity">Sort: Severity</option>
          <option value="barrier">Sort: Barrier</option>
          <option value="cost">Sort: Cost</option>
        </select>
        {(severityFilter || barrierFilter || consentFilter) && (
          <button
            className="btn btn-sm"
            onClick={() => {
              setSeverityFilter("");
              setBarrierFilter("");
              setConsentFilter("");
            }}
          >
            CLEAR
          </button>
        )}
      </div>

      {/* Content */}
      <div className="flex flex-1 overflow-hidden">
        {/* Gap Cards Grid */}
        <div className="flex-1 overflow-auto p-4">
          {loading ? (
            <div className="text-center font-mono text-sm text-gray-500 py-8">
              Loading gaps...
            </div>
          ) : error ? (
            <div className="text-center font-mono text-sm text-red-600 py-8">
              Error: {error}
            </div>
          ) : (
            <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-3">
              {filtered.map((gap) => (
                <div
                  key={gap.id}
                  className={`card cursor-pointer transition-colors hover:bg-gray-50 ${
                    selectedGap === gap.id ? "border-2 border-black" : ""
                  } ${
                    gap.consent_closable
                      ? "border-l-4 border-l-green-600"
                      : ""
                  }`}
                  onClick={() =>
                    setSelectedGap(selectedGap === gap.id ? null : gap.id)
                  }
                >
                  {/* Header row */}
                  <div className="flex items-center gap-2 mb-2">
                    <SeverityBadge severity={gap.severity} />
                    <BarrierBadge barrier={gap.barrier_type} />
                    {gap.consent_closable && (
                      <span className="badge px-2 py-0.5 text-[0.625rem] border-green-600 text-green-700 bg-green-50">
                        CONSENT
                      </span>
                    )}
                    <span className="font-mono text-[0.5625rem] text-gray-400 ml-auto">
                      #{gap.id}
                    </span>
                  </div>

                  {/* Systems */}
                  <div className="flex items-center gap-2 mb-2">
                    <span className="font-mono text-xs font-bold">
                      {gap.system_a_name || gap.system_a_id}
                    </span>
                    <span className="font-mono text-[0.625rem] text-red-400">
                      --X--
                    </span>
                    <span className="font-mono text-xs font-bold">
                      {gap.system_b_name || gap.system_b_id}
                    </span>
                  </div>

                  {/* Impact */}
                  <p className="text-xs text-gray-700 mb-2 line-clamp-2">
                    {gap.impact}
                  </p>

                  {/* Footer */}
                  <div className="flex items-center gap-3 text-[0.625rem] font-mono text-gray-500">
                    <span>Cost: {gap.cost_to_bridge}</span>
                    <span>Timeline: {gap.timeline_to_bridge}</span>
                  </div>

                  {/* Applies when */}
                  {gap.applies_when && gap.applies_when.length > 0 && (
                    <div className="flex flex-wrap gap-1 mt-2">
                      {gap.applies_when.slice(0, 4).map((condition) => (
                        <span
                          key={condition}
                          className="font-mono text-[0.5625rem] px-1 py-0 border border-gray-300 text-gray-500"
                        >
                          {condition}
                        </span>
                      ))}
                      {gap.applies_when.length > 4 && (
                        <span className="font-mono text-[0.5625rem] text-gray-400">
                          +{gap.applies_when.length - 4}
                        </span>
                      )}
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Detail Panel */}
        {selectedGap !== null && (
          <div className="w-[480px] border-l-2 border-black overflow-auto flex-shrink-0">
            <GapDetail
              gapId={selectedGap}
              onClose={() => setSelectedGap(null)}
            />
          </div>
        )}
      </div>
    </div>
  );
}
