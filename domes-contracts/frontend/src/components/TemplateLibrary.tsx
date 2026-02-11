import { useState, useEffect } from "react";
import type { Template } from "../types";
import { AGREEMENT_TYPE_LABELS } from "../types";
import { getTemplates } from "../api/client";

export default function TemplateLibrary() {
  const [templates, setTemplates] = useState<Template[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedTemplate, setSelectedTemplate] = useState<Template | null>(null);

  useEffect(() => {
    getTemplates()
      .then((r) => setTemplates(r.templates))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  // Group by agreement type
  const grouped = templates.reduce<Record<string, Template[]>>((acc, t) => {
    const key = t.agreement_type;
    if (!acc[key]) acc[key] = [];
    acc[key].push(t);
    return acc;
  }, {});

  if (loading) return <div className="p-6 font-mono text-sm">Loading templates...</div>;

  return (
    <div className="flex h-full">
      {/* ---- Template Grid ---- */}
      <div className={`overflow-auto ${selectedTemplate ? "w-1/2 border-r border-[var(--color-border)]" : "w-full"}`}>
        <div className="p-6">
          <h2 className="text-xl mb-1">Template Library</h2>
          <p className="text-xs font-mono text-[var(--color-text-secondary)] mb-6">
            {templates.length} templates across {Object.keys(grouped).length} agreement types
          </p>

          {Object.entries(grouped).map(([type, tmpls]) => (
            <div key={type} className="mb-8">
              <h3 className="text-sm font-mono uppercase tracking-wider text-[var(--color-text-secondary)] mb-3 pb-1 border-b border-[var(--color-border)]">
                {AGREEMENT_TYPE_LABELS[type] ?? type}
              </h3>
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-3">
                {tmpls.map((t) => (
                  <button
                    key={t.id}
                    onClick={() => setSelectedTemplate(t)}
                    className={`card text-left cursor-pointer hover:bg-[var(--color-surface)] transition-colors ${
                      selectedTemplate?.id === t.id ? "bg-[var(--color-surface)]" : ""
                    }`}
                  >
                    <div className="flex items-center gap-2 mb-2">
                      <span className="text-xs font-mono px-2 py-0.5 bg-black text-white uppercase">
                        {type}
                      </span>
                    </div>
                    <h4 className="font-serif text-base font-semibold">{t.name}</h4>
                    <p className="text-xs text-[var(--color-text-secondary)] mt-1 line-clamp-2">
                      {t.description}
                    </p>
                    <div className="flex flex-wrap gap-1 mt-2">
                      {t.governing_laws.map((l) => (
                        <span
                          key={l}
                          className="text-[10px] font-mono px-1.5 py-0.5 border border-[var(--color-border)] text-[var(--color-text-tertiary)]"
                        >
                          {l}
                        </span>
                      ))}
                    </div>
                  </button>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* ---- Template Detail ---- */}
      {selectedTemplate && (
        <div className="w-1/2 overflow-auto p-6 space-y-5">
          <div className="flex items-center justify-between">
            <div>
              <span className="text-xs font-mono px-2 py-0.5 bg-black text-white uppercase">
                {selectedTemplate.agreement_type}
              </span>
              <h2 className="text-2xl mt-2">{selectedTemplate.name}</h2>
            </div>
            <button
              onClick={() => setSelectedTemplate(null)}
              className="btn-secondary text-xs"
            >
              Close
            </button>
          </div>

          <p className="text-sm leading-relaxed">{selectedTemplate.description}</p>

          {/* Governing laws */}
          <div>
            <h4 className="text-xs font-mono uppercase tracking-wider text-[var(--color-text-secondary)] mb-2">
              Governing Laws
            </h4>
            <div className="flex flex-wrap gap-1">
              {selectedTemplate.governing_laws.map((l) => (
                <span key={l} className="text-xs font-mono px-2 py-0.5 border border-black">
                  {l}
                </span>
              ))}
            </div>
          </div>

          {/* Required provisions */}
          {selectedTemplate.required_provisions.length > 0 && (
            <div>
              <h4 className="text-xs font-mono uppercase tracking-wider text-[var(--color-text-secondary)] mb-2">
                Required Provisions
              </h4>
              <ul className="space-y-1">
                {selectedTemplate.required_provisions.map((p, i) => (
                  <li key={i} className="text-xs font-mono pl-3 border-l-2 border-black">
                    {p}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Variable fields */}
          {selectedTemplate.variable_fields.length > 0 && (
            <div>
              <h4 className="text-xs font-mono uppercase tracking-wider text-[var(--color-text-secondary)] mb-2">
                Variable Fields
              </h4>
              <div className="flex flex-wrap gap-1">
                {selectedTemplate.variable_fields.map((f) => (
                  <span
                    key={f}
                    className="text-xs font-mono px-2 py-0.5 bg-[var(--color-surface)] border border-[var(--color-border)]"
                  >
                    {`{{${f}}}`}
                  </span>
                ))}
              </div>
            </div>
          )}

          {/* Template body */}
          {selectedTemplate.body_template && (
            <div>
              <h4 className="text-xs font-mono uppercase tracking-wider text-[var(--color-text-secondary)] mb-2">
                Template Text
              </h4>
              <div className="card bg-[var(--color-surface)] max-h-[500px] overflow-auto">
                <pre className="text-xs font-mono whitespace-pre-wrap leading-relaxed">
                  {selectedTemplate.body_template}
                </pre>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
