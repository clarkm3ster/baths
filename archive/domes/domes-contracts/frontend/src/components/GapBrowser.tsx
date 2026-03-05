import { useState, useEffect } from "react";
import type { Gap, Agreement } from "../types";
import { DOMAIN_COLORS, AGREEMENT_TYPE_LABELS } from "../types";
import { getGaps, getGap, getAgreementsForGap, generateFromGap, getGapCoverage, getExportUrl } from "../api/client";

interface Props {
  onGenerated: () => void;
}

const COVERAGE_STYLES: Record<string, { bg: string; border: string; label: string }> = {
  none: { bg: "var(--color-issues)", border: "var(--color-issues)", label: "NO AGREEMENT" },
  draft: { bg: "var(--color-executed)", border: "var(--color-executed)", label: "DRAFTED" },
  in_review: { bg: "var(--color-in-review)", border: "var(--color-in-review)", label: "IN REVIEW" },
  executed: { bg: "var(--color-in-review)", border: "var(--color-in-review)", label: "EXECUTED" },
};

export default function GapBrowser({ onGenerated }: Props) {
  const [gaps, setGaps] = useState<Gap[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [coverage, setCoverage] = useState<Record<number, string>>({});

  const [selectedGap, setSelectedGap] = useState<Gap | null>(null);
  const [gapAgreements, setGapAgreements] = useState<Agreement[]>([]);
  const [loadingDetail, setLoadingDetail] = useState(false);

  const [generating, setGenerating] = useState(false);
  const [genResult, setGenResult] = useState<string>("");

  useEffect(() => {
    setLoading(true);
    Promise.all([getGaps(), getGapCoverage()])
      .then(([g, c]) => { setGaps(g); setCoverage(c); })
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, []);

  async function selectGap(gap: Gap) {
    setLoadingDetail(true);
    setGenResult("");
    try {
      const detail = await getGap(gap.id);
      setSelectedGap(detail);
      const resp = await getAgreementsForGap(gap.id);
      setGapAgreements(resp.agreements);
    } catch {
      setSelectedGap(gap);
      setGapAgreements([]);
    } finally {
      setLoadingDetail(false);
    }
  }

  async function handleGenerate(gapId: number) {
    setGenerating(true);
    setGenResult("");
    try {
      const result = await generateFromGap(gapId);
      setGenResult(
        `Generated ${result.agreements_generated} agreement(s): ${result.agreement_types_needed.join(", ")}`
      );
      const resp = await getAgreementsForGap(gapId);
      setGapAgreements(resp.agreements);
      // Refresh coverage
      getGapCoverage().then(setCoverage).catch(() => {});
      onGenerated();
    } catch (e: unknown) {
      setGenResult(`Error: ${e instanceof Error ? e.message : String(e)}`);
    } finally {
      setGenerating(false);
    }
  }

  const severityColor = (s: string) => {
    switch (s) {
      case "critical": return "bg-[var(--color-justice)] text-white";
      case "high": return "bg-[var(--color-draft)] text-white";
      case "moderate": return "bg-[var(--color-in-review)] text-white";
      default: return "bg-[var(--color-surface)] text-[var(--color-text-secondary)]";
    }
  };

  const statusBadge = (s: string) => {
    switch (s) {
      case "draft": return "border border-[var(--color-draft)] text-[var(--color-draft)]";
      case "in_review": return "border border-[var(--color-in-review)] text-[var(--color-in-review)]";
      case "executed": return "border border-[var(--color-executed)] text-[var(--color-executed)]";
      default: return "border border-[var(--color-border)]";
    }
  };

  // Summary counts
  const noCoverage = gaps.filter((g) => !coverage[g.id]).length;
  const drafted = gaps.filter((g) => coverage[g.id] === "draft").length;
  const reviewed = gaps.filter((g) => coverage[g.id] === "in_review").length;
  const executed = gaps.filter((g) => coverage[g.id] === "executed").length;

  if (loading) return <div className="p-6 font-mono text-sm">Loading gaps...</div>;
  if (error) return <div className="p-6 font-mono text-sm text-[var(--color-justice)]">Error: {error}</div>;

  return (
    <div className="flex h-full">
      {/* ---- Gap List ---- */}
      <div className="w-[420px] border-r border-[var(--color-border)] overflow-auto">
        <div className="p-4 border-b border-[var(--color-border)]">
          <h2 className="text-lg">Data-Sharing Gaps</h2>
          <p className="text-xs text-[var(--color-text-secondary)] mt-1 font-mono">
            {gaps.length} gaps from domes-datamap
          </p>
          {/* Coverage summary */}
          <div className="flex gap-3 mt-2 text-[10px] font-mono uppercase tracking-wider">
            <span className="flex items-center gap-1">
              <span className="w-2.5 h-2.5" style={{ background: "var(--color-issues)" }}></span>
              No agreement: <strong>{noCoverage}</strong>
            </span>
            <span className="flex items-center gap-1">
              <span className="w-2.5 h-2.5" style={{ background: "var(--color-executed)" }}></span>
              Drafted: <strong>{drafted + reviewed}</strong>
            </span>
            <span className="flex items-center gap-1">
              <span className="w-2.5 h-2.5" style={{ background: "var(--color-in-review)" }}></span>
              Executed: <strong>{executed}</strong>
            </span>
          </div>
        </div>

        <div className="divide-y divide-[var(--color-border)]">
          {gaps.map((gap) => {
            const cov = coverage[gap.id] || "none";
            const covStyle = COVERAGE_STYLES[cov] || COVERAGE_STYLES.none;
            return (
              <button
                key={gap.id}
                onClick={() => selectGap(gap)}
                className={`w-full text-left p-4 hover:bg-[var(--color-surface)] transition-colors cursor-pointer ${
                  selectedGap?.id === gap.id ? "bg-[var(--color-surface)]" : ""
                }`}
                style={{ borderLeft: `4px solid ${covStyle.border}` }}
              >
                <div className="flex items-center gap-2 mb-1">
                  <span
                    className={`px-2 py-0.5 text-[10px] font-mono uppercase tracking-wider ${severityColor(gap.severity)}`}
                  >
                    {gap.severity}
                  </span>
                  <span className="text-[10px] font-mono" style={{ color: covStyle.bg }}>
                    {covStyle.label}
                  </span>
                  {gap.consent_closable && (
                    <span className="text-[10px] font-mono text-[var(--color-executed)] ml-auto">
                      CONSENT-CLOSABLE
                    </span>
                  )}
                </div>

                <div className="flex items-center gap-1.5 text-sm mt-1">
                  <span
                    className="font-mono text-xs px-1.5 py-0.5 border"
                    style={{
                      borderColor: DOMAIN_COLORS[gap.system_a?.domain ?? ""] ?? "var(--color-border)",
                      color: DOMAIN_COLORS[gap.system_a?.domain ?? ""] ?? "var(--color-text)",
                    }}
                  >
                    {gap.system_a?.acronym ?? gap.system_a_id}
                  </span>
                  <span className="text-[var(--color-text-tertiary)]">&harr;</span>
                  <span
                    className="font-mono text-xs px-1.5 py-0.5 border"
                    style={{
                      borderColor: DOMAIN_COLORS[gap.system_b?.domain ?? ""] ?? "var(--color-border)",
                      color: DOMAIN_COLORS[gap.system_b?.domain ?? ""] ?? "var(--color-text)",
                    }}
                  >
                    {gap.system_b?.acronym ?? gap.system_b_id}
                  </span>
                </div>

                <p className="text-xs text-[var(--color-text-secondary)] mt-1.5 line-clamp-2">
                  {gap.barrier_description}
                </p>

                <div className="flex gap-2 mt-1.5">
                  <span className="text-[10px] font-mono text-[var(--color-text-tertiary)] uppercase">
                    {gap.barrier_type}
                  </span>
                  {gap.barrier_law && (
                    <span className="text-[10px] font-mono text-[var(--color-text-tertiary)]">
                      {gap.barrier_law}
                    </span>
                  )}
                </div>
              </button>
            );
          })}
        </div>
      </div>

      {/* ---- Detail Panel ---- */}
      <div className="flex-1 overflow-auto">
        {!selectedGap && (
          <div className="p-12 text-center text-[var(--color-text-tertiary)]">
            <p className="font-serif text-xl">Select a gap to view details</p>
            <p className="text-sm mt-2 font-mono">
              Choose a data-sharing gap from the list to see its details and generate agreements
            </p>
          </div>
        )}

        {selectedGap && loadingDetail && (
          <div className="p-6 font-mono text-sm">Loading details...</div>
        )}

        {selectedGap && !loadingDetail && (
          <div className="p-6 space-y-6">
            {/* Header */}
            <div>
              <div className="flex items-center gap-3 mb-2">
                <span className={`px-2 py-0.5 text-xs font-mono uppercase ${severityColor(selectedGap.severity)}`}>
                  {selectedGap.severity}
                </span>
                <span className="font-mono text-xs text-[var(--color-text-tertiary)]">
                  Gap #{selectedGap.id}
                </span>
                {selectedGap.consent_closable && (
                  <span className="px-2 py-0.5 text-xs font-mono border border-[var(--color-executed)] text-[var(--color-executed)]">
                    CONSENT-CLOSABLE
                  </span>
                )}
              </div>

              <h2 className="text-2xl mb-2">
                {selectedGap.system_a?.name ?? selectedGap.system_a_id}{" "}
                <span className="text-[var(--color-text-tertiary)]">&harr;</span>{" "}
                {selectedGap.system_b?.name ?? selectedGap.system_b_id}
              </h2>

              <div className="flex gap-2 text-xs font-mono">
                {selectedGap.system_a?.domain && (
                  <span
                    className="px-2 py-0.5 border"
                    style={{
                      borderColor: DOMAIN_COLORS[selectedGap.system_a.domain] ?? "var(--color-border)",
                      color: DOMAIN_COLORS[selectedGap.system_a.domain] ?? "var(--color-text)",
                    }}
                  >
                    {selectedGap.system_a.domain}
                  </span>
                )}
                {selectedGap.system_b?.domain && selectedGap.system_b.domain !== selectedGap.system_a?.domain && (
                  <span
                    className="px-2 py-0.5 border"
                    style={{
                      borderColor: DOMAIN_COLORS[selectedGap.system_b.domain] ?? "var(--color-border)",
                      color: DOMAIN_COLORS[selectedGap.system_b.domain] ?? "var(--color-text)",
                    }}
                  >
                    {selectedGap.system_b.domain}
                  </span>
                )}
              </div>
            </div>

            {/* Barrier info */}
            <div className="card space-y-3">
              <div>
                <h3 className="text-sm font-mono uppercase tracking-wider text-[var(--color-text-secondary)] mb-1">
                  Barrier
                </h3>
                <div className="flex gap-2 mb-2">
                  <span className="text-xs font-mono px-2 py-0.5 bg-[var(--color-surface)] border border-[var(--color-border)]">
                    {selectedGap.barrier_type}
                  </span>
                  {selectedGap.barrier_law && (
                    <span className="text-xs font-mono px-2 py-0.5 bg-[var(--color-surface)] border border-[var(--color-border)]">
                      {selectedGap.barrier_law}
                    </span>
                  )}
                </div>
                <p className="text-sm leading-relaxed">{selectedGap.barrier_description}</p>
              </div>

              <div>
                <h3 className="text-sm font-mono uppercase tracking-wider text-[var(--color-text-secondary)] mb-1">
                  Impact
                </h3>
                <p className="text-sm leading-relaxed">{selectedGap.impact}</p>
              </div>

              <div>
                <h3 className="text-sm font-mono uppercase tracking-wider text-[var(--color-text-secondary)] mb-1">
                  What It Would Take
                </h3>
                <p className="text-sm leading-relaxed">{selectedGap.what_it_would_take}</p>
              </div>

              {selectedGap.consent_closable && selectedGap.consent_mechanism && (
                <div>
                  <h3 className="text-sm font-mono uppercase tracking-wider text-[var(--color-executed)] mb-1">
                    Consent Mechanism
                  </h3>
                  <p className="text-sm leading-relaxed">{selectedGap.consent_mechanism}</p>
                </div>
              )}
            </div>

            {/* Generate button */}
            <div className="flex items-center gap-3">
              <button
                onClick={() => handleGenerate(selectedGap.id)}
                disabled={generating}
                className="btn-primary"
              >
                {generating ? "Generating..." : "Generate Agreements"}
              </button>
              {genResult && (
                <span
                  className={`text-xs font-mono ${
                    genResult.startsWith("Error") ? "text-[var(--color-justice)]" : "text-[var(--color-executed)]"
                  }`}
                >
                  {genResult}
                </span>
              )}
            </div>

            {/* Linked agreements */}
            <div>
              <h3 className="text-lg mb-3">Linked Agreements</h3>
              {gapAgreements.length === 0 ? (
                <div className="card-surface text-center py-8">
                  <p className="font-serif text-lg text-[var(--color-text-secondary)]">
                    No agreements yet
                  </p>
                  <p className="text-xs text-[var(--color-text-tertiary)] mt-1 font-mono">
                    Generate agreements to close this gap
                  </p>
                  <button
                    onClick={() => handleGenerate(selectedGap.id)}
                    disabled={generating}
                    className="btn-secondary mt-4"
                  >
                    Generate Agreements
                  </button>
                </div>
              ) : (
                <div className="space-y-2">
                  {gapAgreements.map((a) => (
                    <div key={a.id} className="card-surface flex items-center justify-between">
                      <div>
                        <div className="flex items-center gap-2">
                          <span className={`px-2 py-0.5 text-[10px] font-mono uppercase ${statusBadge(a.status)}`}>
                            {a.status.replace("_", " ")}
                          </span>
                          <span className="text-xs font-mono text-[var(--color-text-tertiary)]">
                            {AGREEMENT_TYPE_LABELS[a.agreement_type] ?? a.agreement_type}
                          </span>
                        </div>
                        <p className="text-sm mt-1 font-medium">{a.title}</p>
                        <p className="text-xs text-[var(--color-text-secondary)] mt-0.5">
                          {a.party_a_name} &mdash; {a.party_b_name}
                        </p>
                      </div>
                      <div className="text-right flex flex-col items-end gap-1">
                        <span
                          className={`text-[10px] font-mono uppercase ${
                            a.compliance_status === "valid"
                              ? "text-[var(--color-valid)]"
                              : a.compliance_status === "issues_found"
                              ? "text-[var(--color-issues)]"
                              : "text-[var(--color-unchecked)]"
                          }`}
                        >
                          {a.compliance_status}
                        </span>
                        <a
                          href={getExportUrl(a.id)}
                          className="text-[10px] font-mono text-[var(--color-text-tertiary)] underline hover:text-black"
                          download
                        >
                          Download
                        </a>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
