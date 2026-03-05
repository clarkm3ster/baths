import { useState, useEffect } from "react";
import type { Agreement, Template, Gap } from "../types";
import { AGREEMENT_TYPE_LABELS } from "../types";
import {
  getAgreements,
  getTemplates,
  getGaps,
  generateAgreement,
  generateFromGap,
  validateAgreement,
} from "../api/client";

interface Props {
  onGenerated: () => void;
}

type Mode = "from_gap" | "from_template";

export default function AgreementGenerator({ onGenerated }: Props) {
  const [mode, setMode] = useState<Mode>("from_gap");
  const [agreements, setAgreements] = useState<Agreement[]>([]);
  const [templates, setTemplates] = useState<Template[]>([]);
  const [gaps, setGaps] = useState<Gap[]>([]);
  const [loading, setLoading] = useState(true);

  // From-gap mode
  const [selectedGapId, setSelectedGapId] = useState<number | null>(null);

  // From-template mode
  const [selectedTemplateId, setSelectedTemplateId] = useState("");
  const [partyA, setPartyA] = useState("");
  const [partyB, setPartyB] = useState("");
  const [state, setState] = useState("Pennsylvania");

  // Generation state
  const [generating, setGenerating] = useState(false);
  const [genError, setGenError] = useState("");
  const [previewAgreement, setPreviewAgreement] = useState<Agreement | null>(null);
  const [validating, setValidating] = useState(false);
  const [validationMsg, setValidationMsg] = useState("");

  // View detail
  const [selectedAgreement, setSelectedAgreement] = useState<Agreement | null>(null);

  // Status filter
  const [filterStatus, setFilterStatus] = useState("");

  useEffect(() => {
    Promise.all([
      getAgreements(filterStatus ? { status: filterStatus } : undefined),
      getTemplates(),
      getGaps(),
    ])
      .then(([agResp, tmplResp, gapsResp]) => {
        setAgreements(agResp.agreements);
        setTemplates(tmplResp.templates);
        setGaps(gapsResp);
      })
      .catch(() => {})
      .finally(() => setLoading(false));
  }, [filterStatus]);

  const refresh = () => {
    getAgreements(filterStatus ? { status: filterStatus } : undefined)
      .then((r) => setAgreements(r.agreements))
      .catch(() => {});
    onGenerated();
  };

  async function handleGenerateFromGap() {
    if (selectedGapId === null) return;
    setGenerating(true);
    setGenError("");
    try {
      const result = await generateFromGap(selectedGapId);
      if (result.agreements.length > 0) {
        setPreviewAgreement(result.agreements[0]);
      }
      refresh();
    } catch (e: unknown) {
      setGenError(e instanceof Error ? e.message : String(e));
    } finally {
      setGenerating(false);
    }
  }

  async function handleGenerateFromTemplate() {
    if (!selectedTemplateId || !partyA || !partyB) return;
    setGenerating(true);
    setGenError("");
    try {
      const result = await generateAgreement({
        template_id: selectedTemplateId,
        party_a_name: partyA,
        party_b_name: partyB,
        state,
      });
      setPreviewAgreement(result);
      refresh();
    } catch (e: unknown) {
      setGenError(e instanceof Error ? e.message : String(e));
    } finally {
      setGenerating(false);
    }
  }

  async function handleValidate(agreementId: string) {
    setValidating(true);
    setValidationMsg("");
    try {
      const result = await validateAgreement(agreementId);
      setValidationMsg(
        `${result.status.toUpperCase()}: ${result.summary.passed} passed, ${result.summary.failed} failed, ${result.summary.warnings} warnings`
      );
      refresh();
    } catch (e: unknown) {
      setValidationMsg(`Error: ${e instanceof Error ? e.message : String(e)}`);
    } finally {
      setValidating(false);
    }
  }

  const selectedTemplate = templates.find((t) => t.id === selectedTemplateId);

  const statusBadge = (s: string) => {
    switch (s) {
      case "draft":
        return "border border-[var(--color-draft)] text-[var(--color-draft)]";
      case "in_review":
        return "border border-[var(--color-in-review)] text-[var(--color-in-review)]";
      case "executed":
        return "border border-[var(--color-executed)] text-[var(--color-executed)]";
      default:
        return "border border-[var(--color-border)]";
    }
  };

  const complianceBadge = (s: string) => {
    switch (s) {
      case "valid":
        return "text-[var(--color-valid)]";
      case "issues_found":
        return "text-[var(--color-issues)]";
      default:
        return "text-[var(--color-unchecked)]";
    }
  };

  if (loading) return <div className="p-6 font-mono text-sm">Loading...</div>;

  return (
    <div className="flex h-full">
      {/* ---- Left: Generator + Agreement List ---- */}
      <div className="w-[500px] border-r border-[var(--color-border)] overflow-auto flex flex-col">
        {/* Mode toggle */}
        <div className="border-b border-[var(--color-border)] p-4">
          <h2 className="text-lg mb-3">Generate Agreement</h2>
          <div className="flex gap-0">
            <button
              onClick={() => setMode("from_gap")}
              className={`px-4 py-2 text-xs font-mono uppercase tracking-wider border-2 border-black cursor-pointer ${
                mode === "from_gap" ? "bg-black text-white" : "bg-white text-black"
              }`}
            >
              From Gap
            </button>
            <button
              onClick={() => setMode("from_template")}
              className={`px-4 py-2 text-xs font-mono uppercase tracking-wider border-2 border-black border-l-0 cursor-pointer ${
                mode === "from_template" ? "bg-black text-white" : "bg-white text-black"
              }`}
            >
              From Template
            </button>
          </div>
        </div>

        {/* Generator form */}
        <div className="p-4 border-b border-[var(--color-border)] space-y-3">
          {mode === "from_gap" && (
            <>
              <label className="block">
                <span className="text-xs font-mono uppercase tracking-wider text-[var(--color-text-secondary)]">
                  Select Gap
                </span>
                <select
                  value={selectedGapId ?? ""}
                  onChange={(e) =>
                    setSelectedGapId(e.target.value ? Number(e.target.value) : null)
                  }
                  className="mt-1 block w-full border-2 border-black p-2 text-sm font-mono bg-white"
                >
                  <option value="">-- Choose a gap --</option>
                  {gaps.map((g) => (
                    <option key={g.id} value={g.id}>
                      #{g.id} {g.system_a_id} &rarr; {g.system_b_id} ({g.barrier_type})
                    </option>
                  ))}
                </select>
              </label>
              <button
                onClick={handleGenerateFromGap}
                disabled={generating || selectedGapId === null}
                className="btn-primary w-full justify-center"
              >
                {generating ? "Generating..." : "Auto-Generate Agreements"}
              </button>
            </>
          )}

          {mode === "from_template" && (
            <>
              <label className="block">
                <span className="text-xs font-mono uppercase tracking-wider text-[var(--color-text-secondary)]">
                  Template
                </span>
                <select
                  value={selectedTemplateId}
                  onChange={(e) => setSelectedTemplateId(e.target.value)}
                  className="mt-1 block w-full border-2 border-black p-2 text-sm font-mono bg-white"
                >
                  <option value="">-- Choose a template --</option>
                  {templates.map((t) => (
                    <option key={t.id} value={t.id}>
                      {t.name} ({AGREEMENT_TYPE_LABELS[t.agreement_type] ?? t.agreement_type})
                    </option>
                  ))}
                </select>
              </label>

              {selectedTemplate && (
                <div className="card-surface text-xs space-y-1">
                  <p>{selectedTemplate.description}</p>
                  <div className="flex flex-wrap gap-1 mt-1">
                    {selectedTemplate.governing_laws.map((l) => (
                      <span key={l} className="px-1.5 py-0.5 font-mono bg-white border border-[var(--color-border)]">
                        {l}
                      </span>
                    ))}
                  </div>
                  {selectedTemplate.variable_fields.length > 0 && (
                    <p className="font-mono text-[var(--color-text-tertiary)]">
                      Fields: {selectedTemplate.variable_fields.join(", ")}
                    </p>
                  )}
                </div>
              )}

              <label className="block">
                <span className="text-xs font-mono uppercase tracking-wider text-[var(--color-text-secondary)]">
                  Party A
                </span>
                <input
                  type="text"
                  value={partyA}
                  onChange={(e) => setPartyA(e.target.value)}
                  placeholder="Disclosing entity..."
                  className="mt-1 block w-full border-2 border-black p-2 text-sm"
                />
              </label>
              <label className="block">
                <span className="text-xs font-mono uppercase tracking-wider text-[var(--color-text-secondary)]">
                  Party B
                </span>
                <input
                  type="text"
                  value={partyB}
                  onChange={(e) => setPartyB(e.target.value)}
                  placeholder="Receiving entity..."
                  className="mt-1 block w-full border-2 border-black p-2 text-sm"
                />
              </label>
              <label className="block">
                <span className="text-xs font-mono uppercase tracking-wider text-[var(--color-text-secondary)]">
                  State
                </span>
                <input
                  type="text"
                  value={state}
                  onChange={(e) => setState(e.target.value)}
                  className="mt-1 block w-full border-2 border-black p-2 text-sm"
                />
              </label>
              <button
                onClick={handleGenerateFromTemplate}
                disabled={generating || !selectedTemplateId || !partyA || !partyB}
                className="btn-primary w-full justify-center"
              >
                {generating ? "Generating..." : "Generate Agreement"}
              </button>
            </>
          )}

          {genError && (
            <p className="text-xs font-mono text-[var(--color-justice)]">{genError}</p>
          )}
        </div>

        {/* Agreements list */}
        <div className="flex-1 overflow-auto">
          <div className="p-4 border-b border-[var(--color-border)] flex items-center justify-between">
            <h3 className="text-sm font-mono uppercase tracking-wider">
              All Agreements ({agreements.length})
            </h3>
            <select
              value={filterStatus}
              onChange={(e) => setFilterStatus(e.target.value)}
              className="text-xs font-mono border border-[var(--color-border)] px-2 py-1 bg-white"
            >
              <option value="">All Statuses</option>
              <option value="draft">Draft</option>
              <option value="in_review">In Review</option>
              <option value="executed">Executed</option>
            </select>
          </div>
          <div className="divide-y divide-[var(--color-border)]">
            {agreements.map((a) => (
              <button
                key={a.id}
                onClick={() => {
                  setSelectedAgreement(a);
                  setPreviewAgreement(null);
                }}
                className={`w-full text-left p-3 hover:bg-[var(--color-surface)] transition-colors cursor-pointer ${
                  selectedAgreement?.id === a.id ? "bg-[var(--color-surface)]" : ""
                }`}
              >
                <div className="flex items-center gap-2 mb-1">
                  <span className={`px-2 py-0.5 text-[10px] font-mono uppercase ${statusBadge(a.status)}`}>
                    {a.status.replace("_", " ")}
                  </span>
                  <span className={`text-[10px] font-mono uppercase ${complianceBadge(a.compliance_status)}`}>
                    {a.compliance_status}
                  </span>
                </div>
                <p className="text-sm font-medium truncate">{a.title}</p>
                <p className="text-xs text-[var(--color-text-secondary)] truncate">
                  {a.party_a_name} &mdash; {a.party_b_name}
                </p>
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* ---- Right: Preview / Detail ---- */}
      <div className="flex-1 overflow-auto">
        {!previewAgreement && !selectedAgreement && (
          <div className="p-12 text-center text-[var(--color-text-tertiary)]">
            <p className="font-serif text-xl">Generate or select an agreement</p>
            <p className="text-sm mt-2 font-mono">
              Use the generator on the left or select an existing agreement from the list
            </p>
          </div>
        )}

        {(previewAgreement || selectedAgreement) && (() => {
          const ag = previewAgreement ?? selectedAgreement!;
          return (
            <div className="p-6 space-y-5">
              <div className="flex items-center justify-between">
                <div>
                  <div className="flex items-center gap-2 mb-1">
                    <span className={`px-2 py-0.5 text-xs font-mono uppercase ${statusBadge(ag.status)}`}>
                      {ag.status.replace("_", " ")}
                    </span>
                    <span className="text-xs font-mono text-[var(--color-text-tertiary)]">
                      {AGREEMENT_TYPE_LABELS[ag.agreement_type] ?? ag.agreement_type}
                    </span>
                    {ag.gap_id && (
                      <span className="text-xs font-mono text-[var(--color-text-tertiary)]">
                        Gap #{ag.gap_id}
                      </span>
                    )}
                  </div>
                  <h2 className="text-2xl">{ag.title}</h2>
                  <p className="text-sm text-[var(--color-text-secondary)] mt-1">
                    {ag.party_a_name} &mdash; {ag.party_b_name}
                  </p>
                </div>
                <div className="flex gap-2">
                  <button
                    onClick={() => handleValidate(ag.id)}
                    disabled={validating}
                    className="btn-secondary"
                  >
                    {validating ? "Validating..." : "Validate Compliance"}
                  </button>
                </div>
              </div>

              {validationMsg && (
                <div
                  className={`card-surface text-xs font-mono ${
                    validationMsg.startsWith("VALID") ? "text-[var(--color-valid)]" : validationMsg.startsWith("Error") ? "text-[var(--color-issues)]" : "text-[var(--color-in-review)]"
                  }`}
                >
                  {validationMsg}
                </div>
              )}

              {/* Metadata */}
              <div className="grid grid-cols-2 gap-4">
                {ag.governing_laws.length > 0 && (
                  <div>
                    <h4 className="text-xs font-mono uppercase tracking-wider text-[var(--color-text-secondary)] mb-1">
                      Governing Laws
                    </h4>
                    <div className="flex flex-wrap gap-1">
                      {ag.governing_laws.map((l) => (
                        <span key={l} className="text-xs font-mono px-2 py-0.5 border border-[var(--color-border)] bg-[var(--color-surface)]">
                          {l}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
                {ag.data_elements.length > 0 && (
                  <div>
                    <h4 className="text-xs font-mono uppercase tracking-wider text-[var(--color-text-secondary)] mb-1">
                      Data Elements
                    </h4>
                    <div className="flex flex-wrap gap-1">
                      {ag.data_elements.map((d) => (
                        <span key={d} className="text-xs font-mono px-2 py-0.5 border border-[var(--color-border)] bg-[var(--color-surface)]">
                          {d}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
                {ag.key_terms.length > 0 && (
                  <div>
                    <h4 className="text-xs font-mono uppercase tracking-wider text-[var(--color-text-secondary)] mb-1">
                      Key Terms
                    </h4>
                    <ul className="text-xs space-y-0.5">
                      {ag.key_terms.map((t, i) => (
                        <li key={i} className="font-mono text-[var(--color-text-secondary)]">
                          &bull; {t}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
                {ag.required_signatories.length > 0 && (
                  <div>
                    <h4 className="text-xs font-mono uppercase tracking-wider text-[var(--color-text-secondary)] mb-1">
                      Required Signatories
                    </h4>
                    <ul className="text-xs space-y-0.5">
                      {ag.required_signatories.map((s, i) => (
                        <li key={i} className="font-mono">{s}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>

              {/* Privacy provisions */}
              {ag.privacy_provisions.length > 0 && (
                <div>
                  <h4 className="text-xs font-mono uppercase tracking-wider text-[var(--color-text-secondary)] mb-2">
                    Privacy Provisions
                  </h4>
                  <div className="space-y-1">
                    {ag.privacy_provisions.map((p, i) => (
                      <p key={i} className="text-xs font-mono text-[var(--color-text-secondary)] pl-3 border-l-2 border-[var(--color-border)]">
                        {p}
                      </p>
                    ))}
                  </div>
                </div>
              )}

              {/* Compliance flags */}
              {ag.compliance_flags.length > 0 && (
                <div>
                  <h4 className="text-xs font-mono uppercase tracking-wider text-[var(--color-text-secondary)] mb-2">
                    Compliance Flags
                  </h4>
                  <div className="space-y-1">
                    {ag.compliance_flags.map((f, i) => (
                      <div
                        key={i}
                        className={`card-surface text-xs font-mono ${
                          f.status === "fail"
                            ? "border-l-4 border-l-[var(--color-issues)]"
                            : "border-l-4 border-l-[var(--color-draft)]"
                        }`}
                      >
                        <span className="uppercase font-bold">{f.status}</span>
                        <span className="text-[var(--color-text-secondary)] ml-2">[{f.law}]</span>
                        <p className="mt-0.5">{f.detail}</p>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Body text */}
              {ag.body_text && (
                <div>
                  <h4 className="text-xs font-mono uppercase tracking-wider text-[var(--color-text-secondary)] mb-2">
                    Agreement Text
                  </h4>
                  <div className="card bg-[var(--color-surface)] max-h-[600px] overflow-auto">
                    <pre className="text-xs font-mono whitespace-pre-wrap leading-relaxed">
                      {ag.body_text}
                    </pre>
                  </div>
                </div>
              )}
            </div>
          );
        })()}
      </div>
    </div>
  );
}
