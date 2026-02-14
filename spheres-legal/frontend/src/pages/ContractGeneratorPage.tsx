import { useState, useEffect } from "react";
import {
  FileText,
  Download,
  ChevronRight,
  CheckCircle2,
  AlertCircle,
  Layers,
} from "lucide-react";

interface VariableField {
  field_name: string;
  field_type: string;
  description: string;
  required: boolean;
}

interface Template {
  id: string;
  name: string;
  description: string;
  category: string;
  parties_required: string[];
  variable_fields: VariableField[];
  standard_terms: string[];
  negotiation_points: string[];
  philadelphia_specific_requirements: string[];
  estimated_legal_review_hours: number;
  template_text: string;
}

interface GeneratedContract {
  title: string;
  parties: Record<string, string>;
  effective_date: string;
  body: string;
  permanence_clause: string;
  signatures_required: string[];
}

const CATEGORY_COLORS: Record<string, string> = {
  use: "tag-green",
  financial: "tag-amber",
  community: "tag-blue",
  insurance: "tag-red",
  permanence: "tag-green",
};

function label(s: string) {
  return s.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());
}

export default function ContractGeneratorPage() {
  const [templates, setTemplates] = useState<Template[]>([]);
  const [selected, setSelected] = useState<Template | null>(null);
  const [variables, setVariables] = useState<Record<string, string>>({});
  const [generated, setGenerated] = useState<GeneratedContract | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetch("/api/contracts/templates")
      .then((r) => r.json())
      .then((d) => setTemplates(d.templates || d));
  }, []);

  const selectTemplate = (t: Template) => {
    setSelected(t);
    setGenerated(null);
    const vars: Record<string, string> = {};
    t.variable_fields.forEach((f) => {
      vars[f.field_name] = "";
    });
    setVariables(vars);
  };

  const generate = async () => {
    if (!selected) return;
    setLoading(true);
    const r = await fetch("/api/contracts/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        template_id: selected.id,
        variables,
      }),
    });
    const d = await r.json();
    setGenerated(d);
    setLoading(false);
  };

  const downloadText = () => {
    if (!generated) return;
    const text = `${generated.title}\n\nEffective Date: ${generated.effective_date}\n\nParties:\n${Object.entries(generated.parties).map(([k, v]) => `  ${label(k)}: ${v}`).join("\n")}\n\n${generated.body}\n\nPERMANENCE CLAUSE:\n${generated.permanence_clause}\n\nSIGNATURES REQUIRED:\n${generated.signatures_required.map((s) => `  ${s}: _______________`).join("\n")}`;
    const blob = new Blob([text], { type: "text/plain" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `${generated.title.replace(/\s+/g, "_").toLowerCase()}.txt`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="min-h-screen bg-void pt-20 px-6 pb-20">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="mb-12">
          <p className="section-label mb-3">CONTRACT GENERATOR</p>
          <h1 className="text-3xl font-light tracking-tight mb-2">
            Generate Agreements
          </h1>
          <p className="text-silver">
            Select a template, fill in the variables, and generate a
            Philadelphia-specific legal agreement.
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Template list */}
          <div className="lg:col-span-1">
            <h2 className="text-sm font-mono font-bold text-legal-green tracking-wider uppercase mb-4">
              Templates ({templates.length})
            </h2>
            <div className="space-y-px">
              {templates.map((t) => (
                <button
                  key={t.id}
                  onClick={() => selectTemplate(t)}
                  className={`w-full text-left p-4 border transition-colors ${
                    selected?.id === t.id
                      ? "bg-smoke border-legal-green"
                      : "bg-smoke border-ash hover:border-steel"
                  }`}
                >
                  <div className="flex items-center justify-between mb-1">
                    <h3 className="text-sm font-medium">{t.name}</h3>
                    <ChevronRight size={14} className="text-steel" />
                  </div>
                  <div className="flex items-center gap-2 mt-2">
                    <span
                      className={`tag ${
                        CATEGORY_COLORS[t.category] || ""
                      }`}
                    >
                      {t.category}
                    </span>
                    <span className="tag">
                      {t.estimated_legal_review_hours}h review
                    </span>
                  </div>
                </button>
              ))}
            </div>
          </div>

          {/* Form + Output */}
          <div className="lg:col-span-2">
            {!selected && (
              <div className="card flex items-center justify-center h-64 text-steel">
                <div className="text-center">
                  <FileText size={32} className="mx-auto mb-3 opacity-40" />
                  <p className="text-sm">Select a template to begin</p>
                </div>
              </div>
            )}

            {selected && !generated && (
              <div>
                <div className="card mb-6">
                  <h2 className="font-medium text-lg mb-2">{selected.name}</h2>
                  <p className="text-silver text-sm mb-4">
                    {selected.description}
                  </p>

                  <div className="flex gap-2 flex-wrap mb-6">
                    {selected.parties_required.map((p) => (
                      <span key={p} className="tag tag-blue">
                        {label(p)}
                      </span>
                    ))}
                  </div>

                  {/* Philadelphia requirements */}
                  {selected.philadelphia_specific_requirements.length > 0 && (
                    <div className="border border-legal-blue/20 bg-legal-blue/5 p-3 mb-6">
                      <p className="text-xs font-mono font-bold text-legal-blue tracking-wider uppercase mb-2">
                        Philadelphia Requirements
                      </p>
                      {selected.philadelphia_specific_requirements.map(
                        (r, i) => (
                          <div
                            key={i}
                            className="flex items-start gap-2 mb-1 last:mb-0"
                          >
                            <AlertCircle
                              size={12}
                              className="text-legal-blue mt-0.5 shrink-0"
                            />
                            <p className="text-xs text-cloud">{r}</p>
                          </div>
                        )
                      )}
                    </div>
                  )}
                </div>

                {/* Variable fields */}
                <div className="card mb-6">
                  <h3 className="text-sm font-mono font-bold text-legal-green tracking-wider uppercase mb-4">
                    Fill Variables
                  </h3>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {selected.variable_fields.map((f) => (
                      <div key={f.field_name}>
                        <label className="data-label block mb-1">
                          {label(f.field_name)}
                          {f.required && (
                            <span className="text-legal-red ml-1">*</span>
                          )}
                        </label>
                        <input
                          type={f.field_type === "number" ? "number" : "text"}
                          placeholder={f.description}
                          value={variables[f.field_name] || ""}
                          onChange={(e) =>
                            setVariables({
                              ...variables,
                              [f.field_name]: e.target.value,
                            })
                          }
                          className="w-full bg-ash border border-steel text-snow p-2.5 text-sm"
                        />
                      </div>
                    ))}
                  </div>

                  <button
                    onClick={generate}
                    disabled={loading}
                    className="btn-primary mt-6"
                  >
                    {loading ? "Generating..." : "Generate Agreement"}
                  </button>
                </div>

                {/* Negotiation points */}
                <div className="card">
                  <h3 className="text-sm font-mono font-bold text-legal-amber tracking-wider uppercase mb-3">
                    Negotiation Points
                  </h3>
                  <ul className="space-y-1.5">
                    {selected.negotiation_points.map((p, i) => (
                      <li
                        key={i}
                        className="text-sm text-silver flex items-start gap-2"
                      >
                        <span className="text-legal-amber mt-1">—</span>
                        {p}
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            )}

            {generated && (
              <div>
                <div className="flex items-center justify-between mb-4">
                  <h2 className="text-sm font-mono font-bold text-legal-green tracking-wider uppercase">
                    Generated Agreement
                  </h2>
                  <div className="flex gap-3">
                    <button onClick={downloadText} className="btn-secondary text-xs">
                      <Download size={14} /> Download
                    </button>
                    <button
                      onClick={() => setGenerated(null)}
                      className="btn-secondary text-xs"
                    >
                      Edit Variables
                    </button>
                  </div>
                </div>

                <div className="card">
                  <h2 className="text-xl font-medium mb-4 pb-4 border-b border-ash">
                    {generated.title}
                  </h2>

                  <div className="grid grid-cols-2 gap-4 mb-6">
                    <div>
                      <p className="data-label mb-1">Effective Date</p>
                      <p className="text-sm">{generated.effective_date}</p>
                    </div>
                    {Object.entries(generated.parties).map(([role, name]) => (
                      <div key={role}>
                        <p className="data-label mb-1">{label(role)}</p>
                        <p className="text-sm">{name || "—"}</p>
                      </div>
                    ))}
                  </div>

                  <div className="border-t border-ash pt-6">
                    <div className="prose prose-invert max-w-none text-sm text-cloud leading-relaxed whitespace-pre-line">
                      {generated.body}
                    </div>
                  </div>

                  {generated.permanence_clause && (
                    <div className="border-t border-ash mt-6 pt-6">
                      <div className="flex items-center gap-2 mb-3">
                        <Layers size={16} className="text-legal-green" />
                        <p className="text-sm font-mono font-bold text-legal-green tracking-wider uppercase">
                          Permanence Clause
                        </p>
                      </div>
                      <p className="text-sm text-cloud leading-relaxed whitespace-pre-line">
                        {generated.permanence_clause}
                      </p>
                    </div>
                  )}

                  <div className="border-t border-ash mt-6 pt-6">
                    <p className="data-label mb-3">Signatures Required</p>
                    <div className="grid grid-cols-2 gap-4">
                      {generated.signatures_required.map((s) => (
                        <div key={s} className="flex items-center gap-2">
                          <CheckCircle2
                            size={14}
                            className="text-steel"
                          />
                          <p className="text-sm text-silver">{s}</p>
                          <div className="flex-1 border-b border-steel ml-2" />
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
