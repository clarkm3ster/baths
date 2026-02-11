import { useState, useEffect } from "react";
import type { Agreement, Gap } from "../types";
import { AGREEMENT_TYPE_LABELS } from "../types";
import {
  getAgreements,
  getGaps,
  updateAgreementStatus,
  batchGenerate,
  getExportUrl,
} from "../api/client";

interface Props {
  onUpdated: () => void;
}

type Stage = "draft" | "in_review" | "executed";

const STAGES: { key: Stage; label: string; color: string }[] = [
  { key: "draft", label: "Draft", color: "var(--color-draft)" },
  { key: "in_review", label: "In Review", color: "var(--color-in-review)" },
  { key: "executed", label: "Executed", color: "var(--color-executed)" },
];

const VALID_TRANSITIONS: Record<string, string[]> = {
  draft: ["in_review"],
  in_review: ["executed", "draft"],
  executed: [],
};

const CIRCUMSTANCE_OPTIONS: { key: string; label: string }[] = [
  { key: "medicaid", label: "Medicaid" },
  { key: "mental_health", label: "Mental Health" },
  { key: "sud", label: "SUD" },
  { key: "incarcerated", label: "Incarcerated" },
  { key: "recently_released", label: "Recently Released" },
  { key: "homeless", label: "Homeless" },
  { key: "veteran", label: "Veteran" },
  { key: "foster_care", label: "Foster Care" },
  { key: "probation", label: "Probation" },
  { key: "under_18", label: "Under 18" },
  { key: "idd", label: "IDD" },
  { key: "section_8", label: "Section 8" },
  { key: "snap", label: "SNAP" },
  { key: "ssi", label: "SSI" },
  { key: "ssdi", label: "SSDI" },
];

export default function ExecutionTracker({ onUpdated }: Props) {
  const [agreements, setAgreements] = useState<Agreement[]>([]);
  const [gaps, setGaps] = useState<Gap[]>([]);
  const [loading, setLoading] = useState(true);

  const [updating, setUpdating] = useState<string | null>(null);
  const [confirmAction, setConfirmAction] = useState<{
    agreementId: string;
    newStatus: string;
    title: string;
  } | null>(null);
  const [error, setError] = useState("");

  // Batch generation state
  const [selectedCircumstances, setSelectedCircumstances] = useState<Set<string>>(new Set());
  const [batchLoading, setBatchLoading] = useState(false);
  const [batchResult, setBatchResult] = useState<{
    agreements_generated: number;
    gaps_matched: number;
    gaps_skipped_existing: number;
  } | null>(null);
  const [batchError, setBatchError] = useState("");

  useEffect(() => {
    Promise.all([getAgreements(), getGaps()])
      .then(([agResp, gapsResp]) => {
        setAgreements(agResp.agreements);
        setGaps(gapsResp);
      })
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  const refresh = () => {
    Promise.all([getAgreements(), getGaps()])
      .then(([agResp, gapsResp]) => {
        setAgreements(agResp.agreements);
        setGaps(gapsResp);
      })
      .catch(() => {});
    onUpdated();
  };

  async function handleStatusUpdate(id: string, status: string) {
    setUpdating(id);
    setError("");
    try {
      await updateAgreementStatus(id, status);
      setConfirmAction(null);
      refresh();
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : String(e));
    } finally {
      setUpdating(null);
    }
  }

  function toggleCircumstance(key: string) {
    setSelectedCircumstances((prev) => {
      const next = new Set(prev);
      if (next.has(key)) next.delete(key);
      else next.add(key);
      return next;
    });
  }

  async function handleBatchGenerate() {
    if (selectedCircumstances.size === 0) return;
    setBatchLoading(true);
    setBatchError("");
    setBatchResult(null);
    try {
      const result = await batchGenerate([...selectedCircumstances]);
      setBatchResult({
        agreements_generated: result.agreements_generated,
        gaps_matched: result.gaps_matched,
        gaps_skipped_existing: result.gaps_skipped_existing,
      });
      refresh();
    } catch (e: unknown) {
      setBatchError(e instanceof Error ? e.message : String(e));
    } finally {
      setBatchLoading(false);
    }
  }

  // Organize by stage
  const byStage: Record<Stage, Agreement[]> = {
    draft: agreements.filter((a) => a.status === "draft"),
    in_review: agreements.filter((a) => a.status === "in_review"),
    executed: agreements.filter((a) => a.status === "executed"),
  };

  // Coverage metrics
  const totalGaps = gaps.length;
  const gapsWithExecuted = new Set(
    agreements.filter((a) => a.status === "executed").map((a) => a.gap_id)
  ).size;
  const coveragePct = totalGaps > 0 ? Math.round((gapsWithExecuted / totalGaps) * 100) : 0;

  if (loading) return <div className="p-6 font-mono text-sm">Loading tracker...</div>;

  return (
    <div className="p-6 space-y-6">
      {/* ---- Summary metrics ---- */}
      <div className="flex items-end gap-8">
        <div>
          <h2 className="text-xl mb-1">Execution Tracker</h2>
          <p className="text-xs font-mono text-[var(--color-text-secondary)]">
            Pipeline view: move agreements from draft to execution
          </p>
        </div>

        <div className="flex gap-6 ml-auto">
          <div className="text-center">
            <div className="text-3xl font-serif font-bold">{coveragePct}%</div>
            <div className="text-[10px] font-mono uppercase tracking-wider text-[var(--color-text-secondary)]">
              Gap Coverage
            </div>
          </div>
          <div className="text-center">
            <div className="text-3xl font-serif font-bold">{gapsWithExecuted}</div>
            <div className="text-[10px] font-mono uppercase tracking-wider text-[var(--color-text-secondary)]">
              Gaps Covered
            </div>
          </div>
          <div className="text-center">
            <div className="text-3xl font-serif font-bold">{totalGaps}</div>
            <div className="text-[10px] font-mono uppercase tracking-wider text-[var(--color-text-secondary)]">
              Total Gaps
            </div>
          </div>
          <div className="text-center">
            <div className="text-3xl font-serif font-bold">{agreements.length}</div>
            <div className="text-[10px] font-mono uppercase tracking-wider text-[var(--color-text-secondary)]">
              Agreements
            </div>
          </div>
        </div>
      </div>

      {/* Coverage bar */}
      <div className="h-2 bg-[var(--color-surface)] border border-[var(--color-border)] w-full">
        <div
          className="h-full bg-[var(--color-executed)] transition-all"
          style={{ width: `${coveragePct}%` }}
        ></div>
      </div>

      {/* ---- Batch Generate section ---- */}
      <div className="border-2 border-black p-5 space-y-4">
        <div>
          <h3 className="text-sm font-mono uppercase tracking-wider font-bold mb-1">
            Batch Generate
          </h3>
          <p className="text-xs text-[var(--color-text-secondary)]">
            Select the circumstances that apply, then generate agreements for all matching gaps at once.
          </p>
        </div>

        <div className="flex flex-wrap gap-2">
          {CIRCUMSTANCE_OPTIONS.map((opt) => {
            const active = selectedCircumstances.has(opt.key);
            return (
              <button
                key={opt.key}
                onClick={() => toggleCircumstance(opt.key)}
                className={`text-[11px] font-mono px-2.5 py-1 border border-black transition-colors cursor-pointer ${
                  active
                    ? "bg-black text-white"
                    : "bg-white text-black hover:bg-[var(--color-surface)]"
                }`}
              >
                {opt.label}
              </button>
            );
          })}
        </div>

        <div className="flex items-center gap-4">
          <button
            onClick={handleBatchGenerate}
            disabled={batchLoading || selectedCircumstances.size === 0}
            className="btn-primary"
          >
            {batchLoading
              ? "Generating..."
              : `Generate All Agreements (${selectedCircumstances.size} circumstance${selectedCircumstances.size !== 1 ? "s" : ""})`}
          </button>

          {batchResult && (
            <span className="text-xs font-mono text-[var(--color-valid)]">
              Generated {batchResult.agreements_generated} agreements for{" "}
              {batchResult.gaps_matched} gaps ({batchResult.gaps_skipped_existing} gaps already had agreements)
            </span>
          )}

          {batchError && (
            <span className="text-xs font-mono text-[var(--color-issues)]">
              {batchError}
            </span>
          )}
        </div>
      </div>

      {/* Error */}
      {error && (
        <div className="card-surface text-xs font-mono text-[var(--color-issues)]">
          {error}
        </div>
      )}

      {/* Confirmation dialog */}
      {confirmAction && (
        <div className="card border-2 border-black p-4 bg-[var(--color-surface)]">
          <p className="text-sm font-medium mb-2">
            Move "{confirmAction.title}" to{" "}
            <span className="font-mono uppercase">{confirmAction.newStatus.replace("_", " ")}</span>?
          </p>
          <div className="flex gap-2">
            <button
              onClick={() => handleStatusUpdate(confirmAction.agreementId, confirmAction.newStatus)}
              disabled={updating === confirmAction.agreementId}
              className="btn-primary"
            >
              {updating === confirmAction.agreementId ? "Updating..." : "Confirm"}
            </button>
            <button
              onClick={() => setConfirmAction(null)}
              className="btn-secondary"
            >
              Cancel
            </button>
          </div>
        </div>
      )}

      {/* ---- Pipeline columns ---- */}
      <div className="grid grid-cols-3 gap-4 min-h-[400px]">
        {STAGES.map((stage) => (
          <div key={stage.key} className="flex flex-col">
            {/* Column header */}
            <div
              className="border-2 border-black p-3 mb-3 flex items-center justify-between"
              style={{ borderBottomColor: stage.color, borderBottomWidth: "4px" }}
            >
              <div>
                <h3 className="text-sm font-mono uppercase tracking-wider font-bold">
                  {stage.label}
                </h3>
                <span className="text-[10px] font-mono text-[var(--color-text-tertiary)]">
                  {byStage[stage.key].length} agreement{byStage[stage.key].length !== 1 ? "s" : ""}
                </span>
              </div>
              <span
                className="text-2xl font-serif font-bold"
                style={{ color: stage.color }}
              >
                {byStage[stage.key].length}
              </span>
            </div>

            {/* Cards */}
            <div className="flex-1 space-y-2">
              {byStage[stage.key].map((a) => (
                <div key={a.id} className="card-surface">
                  <div className="flex items-start justify-between gap-2 mb-1">
                    <p className="text-sm font-medium">{a.title}</p>
                    <a
                      href={getExportUrl(a.id)}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-[10px] font-mono uppercase tracking-wider px-2 py-0.5 border border-[var(--color-border)] hover:bg-black hover:text-white hover:border-black transition-colors cursor-pointer flex-shrink-0"
                      title="Download agreement"
                    >
                      Export
                    </a>
                  </div>
                  <p className="text-[10px] font-mono text-[var(--color-text-secondary)] mb-1">
                    {AGREEMENT_TYPE_LABELS[a.agreement_type] ?? a.agreement_type}
                  </p>
                  <p className="text-[10px] text-[var(--color-text-tertiary)] mb-2">
                    {a.party_a_name} &mdash; {a.party_b_name}
                  </p>

                  {/* Compliance indicator */}
                  <div className="flex items-center gap-1.5 mb-2">
                    <span
                      className="w-2 h-2"
                      style={{
                        background:
                          a.compliance_status === "valid"
                            ? "var(--color-valid)"
                            : a.compliance_status === "issues_found"
                            ? "var(--color-issues)"
                            : "var(--color-unchecked)",
                      }}
                    ></span>
                    <span className="text-[10px] font-mono text-[var(--color-text-tertiary)]">
                      {a.compliance_status.replace("_", " ")}
                    </span>
                  </div>

                  {/* Transition buttons */}
                  {VALID_TRANSITIONS[stage.key]?.length > 0 && (
                    <div className="flex gap-1">
                      {VALID_TRANSITIONS[stage.key].map((target) => (
                        <button
                          key={target}
                          onClick={() =>
                            setConfirmAction({
                              agreementId: a.id,
                              newStatus: target,
                              title: a.title,
                            })
                          }
                          className="text-[10px] font-mono uppercase tracking-wider px-2 py-1 border border-black hover:bg-black hover:text-white transition-colors cursor-pointer"
                        >
                          {target === "in_review"
                            ? "Send to Review"
                            : target === "executed"
                            ? "Execute"
                            : "Return to Draft"}
                        </button>
                      ))}
                    </div>
                  )}
                </div>
              ))}

              {byStage[stage.key].length === 0 && (
                <div className="border border-dashed border-[var(--color-border)] p-4 text-center">
                  <p className="text-xs text-[var(--color-text-tertiary)] font-mono">
                    No agreements in {stage.label.toLowerCase()}
                  </p>
                </div>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
