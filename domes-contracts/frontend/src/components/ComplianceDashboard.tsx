import { useState, useEffect, useMemo } from "react";
import type { Agreement, ComplianceRule, ValidationResult } from "../types";
import { AGREEMENT_TYPE_LABELS } from "../types";
import {
  getAgreements,
  getComplianceRules,
  validateAgreement,
  validateAllUnchecked,
} from "../api/client";

interface Props {
  onValidated: () => void;
}

export default function ComplianceDashboard({ onValidated }: Props) {
  const [agreements, setAgreements] = useState<Agreement[]>([]);
  const [rules, setRules] = useState<ComplianceRule[]>([]);
  const [loading, setLoading] = useState(true);

  // View mode
  const [view, setView] = useState<"overview" | "rules">("overview");

  // Selected agreement for detail
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const [validationResult, setValidationResult] = useState<ValidationResult | null>(null);
  const [validating, setValidating] = useState(false);

  // Batch validation
  const [batchValidating, setBatchValidating] = useState(false);
  const [batchResult, setBatchResult] = useState("");

  // Rules filter
  const [lawFilter, setLawFilter] = useState("");

  // Expanded rule groups
  const [expandedLaws, setExpandedLaws] = useState<Set<string>>(new Set());

  // Track which failed checks have "Show Fix" expanded
  const [expandedFixes, setExpandedFixes] = useState<Set<string>>(new Set());

  useEffect(() => {
    Promise.all([
      getAgreements(),
      getComplianceRules(lawFilter ? { law: lawFilter } : undefined),
    ])
      .then(([agResp, rulesResp]) => {
        setAgreements(agResp.agreements);
        setRules(rulesResp.rules);
      })
      .catch(() => {})
      .finally(() => setLoading(false));
  }, [lawFilter]);

  // Build a Map for fast rule lookup by rule_id
  const rulesMap = useMemo(() => {
    const m = new Map<string, ComplianceRule>();
    for (const r of rules) {
      m.set(r.id, r);
    }
    return m;
  }, [rules]);

  const refresh = () => {
    getAgreements().then((r) => setAgreements(r.agreements)).catch(() => {});
    onValidated();
  };

  async function handleValidate(id: string) {
    setValidating(true);
    setExpandedFixes(new Set());
    try {
      const result = await validateAgreement(id);
      setValidationResult(result);
      refresh();
    } catch {
      /* ignore */
    } finally {
      setValidating(false);
    }
  }

  async function handleValidateAll() {
    setBatchValidating(true);
    setBatchResult("");
    try {
      const result = await validateAllUnchecked();
      setBatchResult(
        `Checked ${result.agreements_checked} agreements: ${result.valid} valid, ${result.issues_found} with issues`
      );
      refresh();
    } catch (e: unknown) {
      setBatchResult(`Error: ${e instanceof Error ? e.message : String(e)}`);
    } finally {
      setBatchValidating(false);
    }
  }

  function toggleFix(key: string) {
    setExpandedFixes((prev) => {
      const next = new Set(prev);
      if (next.has(key)) next.delete(key);
      else next.add(key);
      return next;
    });
  }

  // Stats
  const validCount = agreements.filter((a) => a.compliance_status === "valid").length;
  const issuesCount = agreements.filter((a) => a.compliance_status === "issues_found").length;
  const uncheckedCount = agreements.filter((a) => a.compliance_status === "unchecked").length;

  // Group rules by law
  const rulesByLaw = rules.reduce<Record<string, ComplianceRule[]>>((acc, r) => {
    if (!acc[r.law]) acc[r.law] = [];
    acc[r.law].push(r);
    return acc;
  }, {});

  const toggleLawExpand = (law: string) => {
    setExpandedLaws((prev) => {
      const next = new Set(prev);
      if (next.has(law)) next.delete(law);
      else next.add(law);
      return next;
    });
  };

  const complianceColor = (s: string) => {
    switch (s) {
      case "valid":
        return "var(--color-valid)";
      case "issues_found":
        return "var(--color-issues)";
      default:
        return "var(--color-unchecked)";
    }
  };

  /** Render the "Show Fix" section for a failed check */
  function renderFixSection(checkKey: string, ruleId: string, requirement: string) {
    const rule = rulesMap.get(ruleId);
    const isExpanded = expandedFixes.has(checkKey);
    const provisionText = rule?.provision_text;

    if (!provisionText) return null;

    return (
      <div className="mt-2">
        <button
          onClick={() => toggleFix(checkKey)}
          className="text-[10px] font-mono uppercase tracking-wider px-2 py-1 border border-black hover:bg-black hover:text-white transition-colors cursor-pointer"
        >
          {isExpanded ? "Hide Fix" : "Show Fix"}
        </button>
        {isExpanded && (
          <div className="mt-2 space-y-2">
            <p className="text-xs text-[var(--color-text-secondary)] italic">
              This provision should be added to satisfy {requirement}
            </p>
            <div className="bg-[var(--color-surface)] border border-[var(--color-border)] p-3">
              <pre className="text-xs font-mono whitespace-pre-wrap leading-relaxed">
                {provisionText}
              </pre>
            </div>
          </div>
        )}
      </div>
    );
  }

  if (loading) return <div className="p-6 font-mono text-sm">Loading compliance data...</div>;

  return (
    <div className="flex h-full">
      {/* ---- Left panel ---- */}
      <div className="w-[480px] border-r border-[var(--color-border)] overflow-auto flex flex-col">
        {/* View toggle + overview */}
        <div className="p-4 border-b border-[var(--color-border)]">
          <div className="flex gap-0 mb-4">
            <button
              onClick={() => setView("overview")}
              className={`px-4 py-2 text-xs font-mono uppercase tracking-wider border-2 border-black cursor-pointer ${
                view === "overview" ? "bg-black text-white" : "bg-white text-black"
              }`}
            >
              Agreements
            </button>
            <button
              onClick={() => setView("rules")}
              className={`px-4 py-2 text-xs font-mono uppercase tracking-wider border-2 border-black border-l-0 cursor-pointer ${
                view === "rules" ? "bg-black text-white" : "bg-white text-black"
              }`}
            >
              Rules
            </button>
          </div>

          {/* Stats row */}
          <div className="flex gap-4 text-xs font-mono">
            <div className="flex items-center gap-1.5">
              <span className="w-2.5 h-2.5 bg-[var(--color-valid)]"></span>
              <span>Valid: <strong>{validCount}</strong></span>
            </div>
            <div className="flex items-center gap-1.5">
              <span className="w-2.5 h-2.5 bg-[var(--color-issues)]"></span>
              <span>Issues: <strong>{issuesCount}</strong></span>
            </div>
            <div className="flex items-center gap-1.5">
              <span className="w-2.5 h-2.5 bg-[var(--color-unchecked)]"></span>
              <span>Unchecked: <strong>{uncheckedCount}</strong></span>
            </div>
          </div>

          {uncheckedCount > 0 && (
            <div className="mt-3 flex items-center gap-3">
              <button
                onClick={handleValidateAll}
                disabled={batchValidating}
                className="btn-primary"
              >
                {batchValidating ? "Validating..." : `Validate All Unchecked (${uncheckedCount})`}
              </button>
              {batchResult && (
                <span className="text-xs font-mono text-[var(--color-text-secondary)]">
                  {batchResult}
                </span>
              )}
            </div>
          )}
        </div>

        {/* List */}
        <div className="flex-1 overflow-auto">
          {view === "overview" && (
            <div className="divide-y divide-[var(--color-border)]">
              {agreements.map((a) => (
                <button
                  key={a.id}
                  onClick={() => {
                    setSelectedId(a.id);
                    setValidationResult(null);
                    setExpandedFixes(new Set());
                  }}
                  className={`w-full text-left p-3 hover:bg-[var(--color-surface)] transition-colors cursor-pointer ${
                    selectedId === a.id ? "bg-[var(--color-surface)]" : ""
                  }`}
                >
                  <div className="flex items-center gap-2 mb-1">
                    <span
                      className="w-2.5 h-2.5 flex-shrink-0"
                      style={{ background: complianceColor(a.compliance_status) }}
                    ></span>
                    <span className="text-[10px] font-mono uppercase" style={{ color: complianceColor(a.compliance_status) }}>
                      {a.compliance_status.replace("_", " ")}
                    </span>
                    <span className="text-[10px] font-mono text-[var(--color-text-tertiary)] ml-auto">
                      {AGREEMENT_TYPE_LABELS[a.agreement_type] ?? a.agreement_type}
                    </span>
                  </div>
                  <p className="text-sm font-medium truncate">{a.title}</p>
                  {a.compliance_flags.length > 0 && (
                    <p className="text-[10px] font-mono text-[var(--color-issues)] mt-0.5">
                      {a.compliance_flags.filter((f) => f.status === "fail").length} failures,{" "}
                      {a.compliance_flags.filter((f) => f.status === "warning").length} warnings
                    </p>
                  )}
                </button>
              ))}
            </div>
          )}

          {view === "rules" && (
            <div>
              <div className="p-3 border-b border-[var(--color-border)]">
                <select
                  value={lawFilter}
                  onChange={(e) => setLawFilter(e.target.value)}
                  className="text-xs font-mono border border-[var(--color-border)] px-2 py-1 bg-white w-full"
                >
                  <option value="">All Laws</option>
                  {[...new Set(rules.map((r) => r.law))].map((l) => (
                    <option key={l} value={l}>{l}</option>
                  ))}
                </select>
              </div>
              {Object.entries(rulesByLaw).map(([law, lawRules]) => (
                <div key={law} className="border-b border-[var(--color-border)]">
                  <button
                    onClick={() => toggleLawExpand(law)}
                    className="w-full text-left p-3 flex items-center justify-between hover:bg-[var(--color-surface)] cursor-pointer"
                  >
                    <div className="flex items-center gap-2">
                      <span className="text-xs font-mono font-bold">{law}</span>
                      <span className="text-[10px] font-mono text-[var(--color-text-tertiary)]">
                        {lawRules.length} rules
                      </span>
                    </div>
                    <span className="text-xs">{expandedLaws.has(law) ? "\u25B2" : "\u25BC"}</span>
                  </button>
                  {expandedLaws.has(law) && (
                    <div className="pb-2">
                      {lawRules.map((r) => (
                        <div key={r.id} className="px-3 py-2 mx-3 mb-1 card-surface">
                          <div className="flex items-center gap-2 mb-1">
                            <span
                              className={`text-[10px] font-mono uppercase px-1.5 py-0.5 ${
                                r.severity === "required"
                                  ? "bg-[var(--color-issues)] text-white"
                                  : "bg-[var(--color-surface)] text-[var(--color-text-secondary)] border border-[var(--color-border)]"
                              }`}
                            >
                              {r.severity}
                            </span>
                            <span className="text-[10px] font-mono text-[var(--color-text-tertiary)]">
                              {r.id}
                            </span>
                          </div>
                          <p className="text-xs font-medium">{r.requirement}</p>
                          <p className="text-xs text-[var(--color-text-secondary)] mt-0.5">{r.description}</p>
                          <div className="flex flex-wrap gap-1 mt-1">
                            {r.applies_to.map((t) => (
                              <span key={t} className="text-[10px] font-mono px-1 py-0.5 border border-[var(--color-border)]">
                                {t}
                              </span>
                            ))}
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* ---- Right: Detail ---- */}
      <div className="flex-1 overflow-auto">
        {!selectedId && (
          <div className="p-12 text-center text-[var(--color-text-tertiary)]">
            <p className="font-serif text-xl">Select an agreement to review compliance</p>
            <p className="text-sm mt-2 font-mono">
              Click on an agreement from the list to see or run compliance checks
            </p>
          </div>
        )}

        {selectedId && (() => {
          const ag = agreements.find((a) => a.id === selectedId);
          if (!ag) return null;
          return (
            <div className="p-6 space-y-5">
              <div className="flex items-center justify-between">
                <div>
                  <h2 className="text-xl">{ag.title}</h2>
                  <p className="text-xs text-[var(--color-text-secondary)] font-mono mt-1">
                    {AGREEMENT_TYPE_LABELS[ag.agreement_type] ?? ag.agreement_type} &middot; {ag.party_a_name} &mdash; {ag.party_b_name}
                  </p>
                </div>
                <button
                  onClick={() => handleValidate(ag.id)}
                  disabled={validating}
                  className="btn-primary"
                >
                  {validating ? "Validating..." : "Run Validation"}
                </button>
              </div>

              {/* Current compliance status */}
              <div
                className="card-surface flex items-center gap-3"
                style={{ borderLeft: `4px solid ${complianceColor(ag.compliance_status)}` }}
              >
                <span
                  className="w-4 h-4"
                  style={{ background: complianceColor(ag.compliance_status) }}
                ></span>
                <span className="text-sm font-mono uppercase font-bold" style={{ color: complianceColor(ag.compliance_status) }}>
                  {ag.compliance_status.replace("_", " ")}
                </span>
                {ag.compliance_flags.length > 0 && (
                  <span className="text-xs font-mono text-[var(--color-text-secondary)]">
                    ({ag.compliance_flags.length} flags)
                  </span>
                )}
              </div>

              {/* Validation result */}
              {validationResult && (
                <div className="space-y-3">
                  <h3 className="text-sm font-mono uppercase tracking-wider">
                    Validation Results
                  </h3>
                  <div className="flex gap-4 text-xs font-mono">
                    <span className="text-[var(--color-valid)]">
                      Passed: <strong>{validationResult.summary.passed}</strong>
                    </span>
                    <span className="text-[var(--color-issues)]">
                      Failed: <strong>{validationResult.summary.failed}</strong>
                    </span>
                    <span className="text-[var(--color-draft)]">
                      Warnings: <strong>{validationResult.summary.warnings}</strong>
                    </span>
                  </div>

                  <div className="space-y-1">
                    {validationResult.checks.map((c, i) => {
                      const checkKey = `validation-${i}-${c.rule_id}`;
                      return (
                        <div
                          key={i}
                          className={`card-surface text-xs font-mono border-l-4 ${
                            c.status === "pass"
                              ? "border-l-[var(--color-valid)]"
                              : c.status === "fail"
                              ? "border-l-[var(--color-issues)]"
                              : "border-l-[var(--color-draft)]"
                          }`}
                        >
                          <div className="flex items-center gap-2 mb-0.5">
                            <span
                              className={`uppercase font-bold ${
                                c.status === "pass"
                                  ? "text-[var(--color-valid)]"
                                  : c.status === "fail"
                                  ? "text-[var(--color-issues)]"
                                  : "text-[var(--color-draft)]"
                              }`}
                            >
                              {c.status}
                            </span>
                            <span className="text-[var(--color-text-tertiary)]">[{c.law}]</span>
                            <span className={`ml-auto px-1.5 py-0.5 ${
                              c.severity === "required"
                                ? "bg-[var(--color-issues)] text-white"
                                : "bg-[var(--color-surface)] border border-[var(--color-border)]"
                            }`}>
                              {c.severity}
                            </span>
                          </div>
                          <p className="font-medium">{c.requirement}</p>
                          {c.detail && (
                            <p className="text-[var(--color-text-secondary)] mt-0.5">{c.detail}</p>
                          )}
                          {c.status === "fail" && renderFixSection(checkKey, c.rule_id, c.requirement)}
                        </div>
                      );
                    })}
                  </div>
                </div>
              )}

              {/* Existing flags (if no fresh validation) */}
              {!validationResult && ag.compliance_flags.length > 0 && (
                <div className="space-y-2">
                  <h3 className="text-sm font-mono uppercase tracking-wider">
                    Existing Compliance Flags
                  </h3>
                  {ag.compliance_flags.map((f, i) => {
                    const flagKey = `flag-${i}-${f.rule_id}`;
                    return (
                      <div
                        key={i}
                        className={`card-surface text-xs font-mono border-l-4 ${
                          f.status === "fail"
                            ? "border-l-[var(--color-issues)]"
                            : "border-l-[var(--color-draft)]"
                        }`}
                      >
                        <div className="flex items-center gap-2 mb-0.5">
                          <span
                            className={`uppercase font-bold ${
                              f.status === "fail" ? "text-[var(--color-issues)]" : "text-[var(--color-draft)]"
                            }`}
                          >
                            {f.status}
                          </span>
                          <span className="text-[var(--color-text-tertiary)]">[{f.law}]</span>
                        </div>
                        <p className="font-medium">{f.requirement}</p>
                        <p className="text-[var(--color-text-secondary)] mt-0.5">{f.detail}</p>
                        {f.status === "fail" && renderFixSection(flagKey, f.rule_id, f.requirement)}
                      </div>
                    );
                  })}
                </div>
              )}
            </div>
          );
        })()}
      </div>
    </div>
  );
}
