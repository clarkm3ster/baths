import { useState, useEffect, useRef } from "react";
import type { ConsentForm, ConsentStats } from "../types";
import { getConsentForms, getConsentStats } from "../api/client";

const CONSENT_TYPE_LABELS: Record<string, string> = {
  HIPAA_authorization: "HIPAA Authorization",
  CFR42_consent: "42 CFR Part 2 Consent",
  FERPA_release: "FERPA Release",
  general_release: "General Information Release",
};

// ---------------------------------------------------------------------------
// Plain English explanation generator
// ---------------------------------------------------------------------------

interface PlainEnglish {
  authorizing: string;
  why: string;
  notAuthorizing: string;
}

function getPlainEnglish(form: ConsentForm): PlainEnglish {
  const type = form.consent_type;

  // "What you're authorizing" - based on consent_type
  const authorizingDefaults: Record<string, string> = {
    HIPAA_authorization:
      "You are authorizing one health care provider to share specific health information with another provider or organization.",
    CFR42_consent:
      "You are authorizing a substance use disorder treatment program to share specific treatment information. This is protected by extra-strong federal privacy rules.",
    FERPA_release:
      "You (or your parent/guardian) are authorizing a school to share specific education records with an outside provider.",
    general_release:
      "You are authorizing two service providers to share information about you for care coordination.",
  };

  // "What this does NOT authorize" - based on consent_type
  const notAuthorizingDefaults: Record<string, string> = {
    HIPAA_authorization:
      "This does NOT give the recipient blanket access to your full medical record. Only the specific information described in this form may be shared, and only for the stated purpose.",
    CFR42_consent:
      "This does NOT authorize re-disclosure -- the recipient cannot share your substance use disorder treatment information with anyone else without a separate consent. This is a federal protection under 42 CFR Part 2.",
    FERPA_release:
      "This does NOT give the recipient access to all school records. Only the specific records listed may be shared, and the recipient may not re-disclose them without additional consent.",
    general_release:
      "This does NOT authorize unlimited sharing. Only the information described in this form may be shared, only between the named parties, and only for the stated purpose.",
  };

  const authorizing = authorizingDefaults[type] ?? authorizingDefaults.general_release;

  // "Why this matters" - pull from the form's description
  const why = form.description
    ? form.description
    : "This consent is needed so that the named parties can coordinate services on your behalf.";

  const notAuthorizing = notAuthorizingDefaults[type] ?? notAuthorizingDefaults.general_release;

  return { authorizing, why, notAuthorizing };
}

// ---------------------------------------------------------------------------
// Component
// ---------------------------------------------------------------------------

export default function ConsentCenter() {
  const [forms, setForms] = useState<ConsentForm[]>([]);
  const [stats, setStats] = useState<ConsentStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [selectedForm, setSelectedForm] = useState<ConsentForm | null>(null);
  const [filterType, setFilterType] = useState("");
  const [printMode, setPrintMode] = useState(false);
  const printRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    Promise.all([
      getConsentForms(filterType ? { consent_type: filterType } : undefined),
      getConsentStats(),
    ])
      .then(([formsResp, statsResp]) => {
        setForms(formsResp.forms);
        setStats(statsResp);
      })
      .catch(() => {})
      .finally(() => setLoading(false));
  }, [filterType]);

  // Group by consent type
  const grouped = forms.reduce<Record<string, ConsentForm[]>>((acc, f) => {
    const key = f.consent_type;
    if (!acc[key]) acc[key] = [];
    acc[key].push(f);
    return acc;
  }, {});

  function handlePrint() {
    setPrintMode(true);
    setTimeout(() => {
      window.print();
      setPrintMode(false);
    }, 200);
  }

  if (loading) return <div className="p-6 font-mono text-sm">Loading consent forms...</div>;

  // Print-ready view
  if (printMode && selectedForm) {
    return (
      <div ref={printRef} className="p-8 max-w-3xl mx-auto">
        <h1 className="text-xl font-serif font-bold text-center mb-1">{selectedForm.title}</h1>
        <p className="text-xs text-center font-mono text-[var(--color-text-secondary)] mb-6">
          {CONSENT_TYPE_LABELS[selectedForm.consent_type] ?? selectedForm.consent_type}
          {selectedForm.governing_law && ` | ${selectedForm.governing_law}`}
        </p>
        <pre className="text-sm font-mono whitespace-pre-wrap leading-relaxed">
          {selectedForm.body_text}
        </pre>
      </div>
    );
  }

  return (
    <div className="flex h-full">
      {/* ---- Left: Form List ---- */}
      <div className={`overflow-auto flex flex-col ${selectedForm ? "w-[420px] border-r border-[var(--color-border)]" : "w-full max-w-4xl mx-auto"}`}>
        <div className="p-4 border-b border-[var(--color-border)]">
          <h2 className="text-lg mb-2">Consent Center</h2>

          {/* Stats */}
          {stats && (
            <div className="flex gap-4 text-xs font-mono mb-3">
              <span>Total: <strong>{stats.total}</strong></span>
              {Object.entries(stats.by_status).map(([status, count]) => (
                <span key={status} className={status === "ready" ? "text-[var(--color-valid)]" : "text-[var(--color-draft)]"}>
                  {status}: <strong>{count}</strong>
                </span>
              ))}
            </div>
          )}

          <select
            value={filterType}
            onChange={(e) => setFilterType(e.target.value)}
            className="text-xs font-mono border border-[var(--color-border)] px-2 py-1 bg-white w-full"
          >
            <option value="">All Consent Types</option>
            {Object.entries(CONSENT_TYPE_LABELS).map(([k, v]) => (
              <option key={k} value={k}>{v}</option>
            ))}
          </select>
        </div>

        <div className="flex-1 overflow-auto">
          {filterType ? (
            /* Flat list for filtered view */
            <div className="divide-y divide-[var(--color-border)]">
              {forms.map((f) => (
                <ConsentFormRow
                  key={f.id}
                  form={f}
                  selected={selectedForm?.id === f.id}
                  onClick={() => setSelectedForm(f)}
                />
              ))}
            </div>
          ) : (
            /* Grouped view */
            Object.entries(grouped).map(([type, typeForms]) => (
              <div key={type}>
                <div className="px-4 py-2 bg-[var(--color-surface)] border-b border-[var(--color-border)]">
                  <h3 className="text-xs font-mono uppercase tracking-wider font-bold">
                    {CONSENT_TYPE_LABELS[type] ?? type}
                  </h3>
                  <span className="text-[10px] font-mono text-[var(--color-text-tertiary)]">
                    {typeForms.length} form{typeForms.length !== 1 ? "s" : ""}
                  </span>
                </div>
                <div className="divide-y divide-[var(--color-border)]">
                  {typeForms.map((f) => (
                    <ConsentFormRow
                      key={f.id}
                      form={f}
                      selected={selectedForm?.id === f.id}
                      onClick={() => setSelectedForm(f)}
                    />
                  ))}
                </div>
              </div>
            ))
          )}

          {forms.length === 0 && (
            <div className="p-8 text-center text-[var(--color-text-tertiary)]">
              <p className="font-serif text-lg">No consent forms found</p>
              <p className="text-xs font-mono mt-1">Generate agreements from gaps to create consent forms</p>
            </div>
          )}
        </div>
      </div>

      {/* ---- Right: Form Detail ---- */}
      {selectedForm && (
        <div className="flex-1 overflow-auto p-6 space-y-5">
          <div className="flex items-center justify-between">
            <div>
              <div className="flex items-center gap-2 mb-1">
                <span
                  className={`px-2 py-0.5 text-xs font-mono uppercase border ${
                    selectedForm.status === "ready"
                      ? "border-[var(--color-valid)] text-[var(--color-valid)]"
                      : "border-[var(--color-draft)] text-[var(--color-draft)]"
                  }`}
                >
                  {selectedForm.status}
                </span>
                <span className="text-xs font-mono text-[var(--color-text-tertiary)]">
                  {CONSENT_TYPE_LABELS[selectedForm.consent_type] ?? selectedForm.consent_type}
                </span>
                {selectedForm.gap_id && (
                  <span className="text-xs font-mono text-[var(--color-text-tertiary)]">
                    Gap #{selectedForm.gap_id}
                  </span>
                )}
              </div>
              <h2 className="text-2xl">{selectedForm.title}</h2>
            </div>
            <div className="flex gap-2">
              <button onClick={handlePrint} className="btn-secondary no-print">
                Print View
              </button>
              <button onClick={() => setSelectedForm(null)} className="btn-secondary no-print">
                Close
              </button>
            </div>
          </div>

          {selectedForm.governing_law && (
            <div className="flex items-center gap-2">
              <span className="text-xs font-mono uppercase tracking-wider text-[var(--color-text-secondary)]">
                Governing Law:
              </span>
              <span className="text-xs font-mono px-2 py-0.5 border border-black">
                {selectedForm.governing_law}
              </span>
            </div>
          )}

          {/* ---- Plain English "What this means" section ---- */}
          <PlainEnglishSection form={selectedForm} />

          {/* Required fields */}
          {selectedForm.required_fields.length > 0 && (
            <div>
              <h4 className="text-xs font-mono uppercase tracking-wider text-[var(--color-text-secondary)] mb-2">
                Required Fields
              </h4>
              <div className="flex flex-wrap gap-2">
                {selectedForm.required_fields.map((f) => (
                  <span key={f} className="text-xs font-mono px-2 py-0.5 bg-[var(--color-surface)] border border-[var(--color-border)]">
                    {f}
                  </span>
                ))}
              </div>
            </div>
          )}

          {/* Form body */}
          {selectedForm.body_text && (
            <div>
              <h4 className="text-xs font-mono uppercase tracking-wider text-[var(--color-text-secondary)] mb-2">
                Consent Form Text
              </h4>
              <div className="card bg-[var(--color-surface)] max-h-[600px] overflow-auto">
                <pre className="text-xs font-mono whitespace-pre-wrap leading-relaxed">
                  {selectedForm.body_text}
                </pre>
              </div>
            </div>
          )}

          <div className="text-[10px] font-mono text-[var(--color-text-tertiary)]">
            Created: {selectedForm.created_at} &middot; ID: {selectedForm.id}
          </div>
        </div>
      )}

      {!selectedForm && (
        <div className="flex-1 flex items-center justify-center text-[var(--color-text-tertiary)]">
          <div className="text-center">
            <p className="font-serif text-xl">Select a consent form</p>
            <p className="text-sm mt-2 font-mono">Choose a form from the list to view its details</p>
          </div>
        </div>
      )}
    </div>
  );
}

// ---------------------------------------------------------------------------
// Plain English explanation card
// ---------------------------------------------------------------------------

function PlainEnglishSection({ form }: { form: ConsentForm }) {
  const plain = getPlainEnglish(form);

  return (
    <div
      className="border border-[var(--color-border)] p-5 space-y-4"
      style={{ borderLeft: "4px solid var(--color-valid)" }}
    >
      <h4 className="text-sm font-mono uppercase tracking-wider font-bold">
        What This Means
      </h4>

      <div>
        <p className="text-xs font-mono uppercase tracking-wider text-[var(--color-text-secondary)] mb-1">
          What you are authorizing
        </p>
        <p className="text-sm font-serif leading-relaxed">
          {plain.authorizing}
        </p>
      </div>

      <div>
        <p className="text-xs font-mono uppercase tracking-wider text-[var(--color-text-secondary)] mb-1">
          Why this matters
        </p>
        <p className="text-sm font-serif leading-relaxed">
          {plain.why}
        </p>
      </div>

      <div>
        <p className="text-xs font-mono uppercase tracking-wider text-[var(--color-text-secondary)] mb-1">
          What this does NOT authorize
        </p>
        <p className="text-sm font-serif leading-relaxed">
          {plain.notAuthorizing}
        </p>
      </div>
    </div>
  );
}

// ---------------------------------------------------------------------------
// Form list row
// ---------------------------------------------------------------------------

function ConsentFormRow({
  form,
  selected,
  onClick,
}: {
  form: ConsentForm;
  selected: boolean;
  onClick: () => void;
}) {
  return (
    <button
      onClick={onClick}
      className={`w-full text-left p-3 hover:bg-[var(--color-surface)] transition-colors cursor-pointer ${
        selected ? "bg-[var(--color-surface)]" : ""
      }`}
    >
      <div className="flex items-center gap-2 mb-1">
        <span
          className={`px-2 py-0.5 text-[10px] font-mono uppercase border ${
            form.status === "ready"
              ? "border-[var(--color-valid)] text-[var(--color-valid)]"
              : "border-[var(--color-draft)] text-[var(--color-draft)]"
          }`}
        >
          {form.status}
        </span>
        {form.governing_law && (
          <span className="text-[10px] font-mono text-[var(--color-text-tertiary)]">
            {form.governing_law}
          </span>
        )}
        {form.gap_id && (
          <span className="text-[10px] font-mono text-[var(--color-text-tertiary)] ml-auto">
            Gap #{form.gap_id}
          </span>
        )}
      </div>
      <p className="text-sm font-medium truncate">{form.title}</p>
      <p className="text-xs text-[var(--color-text-secondary)] mt-0.5 line-clamp-1">
        {form.description}
      </p>
    </button>
  );
}
