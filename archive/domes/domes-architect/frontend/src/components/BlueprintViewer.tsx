import { useState } from "react";
import type { Architecture } from "../types";
import { DOMAIN_COLORS, DOMAIN_LABELS } from "../types";
import { updateArchitectureStatus, deleteArchitecture, exportArchitecture } from "../api/client";

interface Props {
  architectures: Architecture[];
  onRefresh: () => void;
}

const STATUS_COLORS: Record<string, string> = {
  draft: "#888888",
  analysis: "#6B5A1A",
  approved: "#1A3D8B",
  implementing: "#1A6B3C",
};

const STATUS_OPTIONS = ["draft", "analysis", "approved", "implementing"];

function formatCurrency(n: number): string {
  return new Intl.NumberFormat("en-US", { style: "currency", currency: "USD", maximumFractionDigits: 0 }).format(n);
}

function formatNumber(n: number): string {
  return new Intl.NumberFormat("en-US").format(n);
}

export default function BlueprintViewer({ architectures, onRefresh }: Props) {
  const [expanded, setExpanded] = useState<number | null>(null);
  const [actionLoading, setActionLoading] = useState<number | null>(null);

  const handleStatusUpdate = async (id: number, status: string) => {
    setActionLoading(id);
    try {
      await updateArchitectureStatus(id, status);
      onRefresh();
    } catch {
      // silent fail
    } finally {
      setActionLoading(null);
    }
  };

  const handleDelete = async (id: number) => {
    if (!confirm("Delete this architecture?")) return;
    setActionLoading(id);
    try {
      await deleteArchitecture(id);
      onRefresh();
    } catch {
      // silent fail
    } finally {
      setActionLoading(null);
    }
  };

  const handleExport = async (id: number) => {
    try {
      const data = await exportArchitecture(id);
      const blob = new Blob([JSON.stringify(data, null, 2)], { type: "application/json" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `architecture-${id}.json`;
      a.click();
      URL.revokeObjectURL(url);
    } catch {
      // silent fail
    }
  };

  if (architectures.length === 0) {
    return (
      <div className="p-8 text-center">
        <p className="text-sm text-[var(--color-text-secondary)] font-mono">
          No architectures generated yet. Use the Designer tab to create one.
        </p>
      </div>
    );
  }

  return (
    <div className="p-6">
      <h2 className="text-2xl font-bold mb-6">Blueprints</h2>
      <div className="space-y-4">
        {architectures.map((arch) => {
          const isExpanded = expanded === arch.id;
          const statusColor = STATUS_COLORS[arch.status] || "#888888";
          return (
            <div key={arch.id} className="border-2 border-black">
              {/* Card Header */}
              <div className="p-4">
                <div className="flex items-start justify-between mb-2">
                  <div>
                    <h3 className="text-lg font-bold">{arch.name}</h3>
                    <p className="text-sm text-[var(--color-text-secondary)] mt-0.5">
                      {arch.description}
                    </p>
                  </div>
                  <span
                    className="text-[10px] font-semibold uppercase tracking-wider px-2 py-0.5 border text-white"
                    style={{ backgroundColor: statusColor, borderColor: statusColor }}
                  >
                    {arch.status}
                  </span>
                </div>

                {/* Meta */}
                <div className="flex flex-wrap gap-4 text-xs font-mono text-[var(--color-text-secondary)] mb-3">
                  <span>Geography: {arch.geography}</span>
                  <span>Population: {formatNumber(arch.population_size)}</span>
                  <span>Budget: {formatCurrency(arch.annual_budget)}</span>
                  <span>Model: {arch.scores?.model_name || `ID ${arch.primary_model_id}`}</span>
                </div>

                {/* Domains */}
                <div className="flex flex-wrap gap-1 mb-3">
                  {arch.domains_targeted.map((d) => (
                    <span
                      key={d}
                      className="text-[10px] font-semibold uppercase tracking-wider px-1.5 py-0.5 text-white"
                      style={{ backgroundColor: DOMAIN_COLORS[d] || "#555555" }}
                    >
                      {DOMAIN_LABELS[d] || d}
                    </span>
                  ))}
                </div>

                {/* Composite */}
                {arch.scores && (
                  <div className="flex items-center gap-2 mb-3">
                    <span className="text-xs font-semibold uppercase tracking-wider">Composite:</span>
                    <span className="font-mono text-xl font-bold">
                      {(arch.scores.composite * 100).toFixed(0)}
                    </span>
                    <span className="text-xs font-mono text-[var(--color-text-secondary)]">/ 100</span>
                  </div>
                )}

                {/* Actions Row */}
                <div className="flex items-center gap-3 mt-3">
                  <button
                    onClick={() => setExpanded(isExpanded ? null : arch.id)}
                    className="text-xs font-semibold uppercase tracking-wider text-[var(--color-text-secondary)] hover:text-black cursor-pointer"
                  >
                    {isExpanded ? "- Collapse" : "+ Expand"}
                  </button>

                  {/* Status Update */}
                  <select
                    value={arch.status}
                    onChange={(e) => handleStatusUpdate(arch.id, e.target.value)}
                    disabled={actionLoading === arch.id}
                    className="border border-black px-2 py-1 text-xs font-mono bg-white cursor-pointer"
                  >
                    {STATUS_OPTIONS.map((s) => (
                      <option key={s} value={s}>
                        {s}
                      </option>
                    ))}
                  </select>

                  <button
                    onClick={() => handleExport(arch.id)}
                    className="btn-secondary text-xs py-1"
                  >
                    Export
                  </button>
                  <button
                    onClick={() => handleDelete(arch.id)}
                    disabled={actionLoading === arch.id}
                    className="text-xs font-semibold uppercase tracking-wider text-[#8B1A1A] hover:underline cursor-pointer disabled:opacity-50"
                  >
                    Delete
                  </button>
                </div>
              </div>

              {/* Expanded Detail */}
              {isExpanded && (
                <div className="border-t-2 border-black p-4 bg-[var(--color-surface)]">
                  {/* Phases Summary */}
                  {arch.implementation_phases && arch.implementation_phases.length > 0 && (
                    <div className="mb-4">
                      <h4 className="text-sm font-semibold mb-2">
                        Implementation Phases ({arch.implementation_phases.length})
                      </h4>
                      <div className="space-y-1">
                        {arch.implementation_phases.map((phase, i) => (
                          <div key={i} className="flex items-center gap-3 text-xs font-mono">
                            <span className="w-4 h-4 border border-black flex items-center justify-center text-[10px]">
                              {i + 1}
                            </span>
                            <span className="font-semibold">{phase.name}</span>
                            <span className="text-[var(--color-text-secondary)]">{phase.duration}</span>
                            <span
                              className="text-[10px] uppercase px-1 border"
                              style={{
                                color: phase.status === "completed" ? "#1A6B3C" : "#888888",
                                borderColor: phase.status === "completed" ? "#1A6B3C" : "#888888",
                              }}
                            >
                              {phase.status}
                            </span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Stakeholders count */}
                  {arch.stakeholders && (
                    <div className="mb-2 text-xs font-mono text-[var(--color-text-secondary)]">
                      Stakeholders: {arch.stakeholders.length}
                    </div>
                  )}

                  {/* Risk count */}
                  {arch.risks && (
                    <div className="mb-2 text-xs font-mono text-[var(--color-text-secondary)]">
                      Risks: {arch.risks.length}
                    </div>
                  )}

                  {/* Budget breakdown summary */}
                  {arch.budget_breakdown && (
                    <div className="mb-2 text-xs font-mono text-[var(--color-text-secondary)]">
                      Budget Categories: {arch.budget_breakdown.categories.length} |
                      Total: {formatCurrency(arch.budget_breakdown.total_annual)}
                    </div>
                  )}

                  {/* Workforce summary */}
                  {arch.workforce_plan && (
                    <div className="text-xs font-mono text-[var(--color-text-secondary)]">
                      Workforce: {arch.workforce_plan.total_estimated_fte} FTE across{" "}
                      {arch.workforce_plan.roles.length} roles
                    </div>
                  )}
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
