import { useState } from "react";
import type { CoordinationModel } from "../types";
import { DOMAIN_COLORS, DOMAIN_LABELS, CATEGORY_COLORS, CATEGORY_LABELS } from "../types";

interface Props {
  models: CoordinationModel[];
  loading: boolean;
}

const CATEGORIES = ["all", "managed_care", "community_based", "hybrid", "specialized"];

function getEvidenceColor(rating: string): string {
  const r = rating.toLowerCase();
  if (r.includes("strong")) return "#1A6B3C";
  if (r.includes("moderate")) return "#6B5A1A";
  if (r.includes("emerging")) return "#8B5A1A";
  return "#888888";
}

export default function ModelBrowser({ models, loading }: Props) {
  const [category, setCategory] = useState("all");
  const [search, setSearch] = useState("");
  const [expanded, setExpanded] = useState<number | null>(null);

  const filtered = models.filter((m) => {
    const matchCat = category === "all" || m.category === category;
    const matchSearch =
      search === "" ||
      m.name.toLowerCase().includes(search.toLowerCase()) ||
      m.abbreviation.toLowerCase().includes(search.toLowerCase());
    return matchCat && matchSearch;
  });

  if (loading) {
    return (
      <div className="p-8 text-center font-mono text-sm text-[var(--color-text-secondary)]">
        Loading models...
      </div>
    );
  }

  return (
    <div className="p-6">
      {/* Filter Bar */}
      <div className="flex flex-wrap items-center gap-3 mb-6">
        <div className="flex border-2 border-black">
          {CATEGORIES.map((cat) => (
            <button
              key={cat}
              onClick={() => setCategory(cat)}
              className={`px-3 py-1.5 text-xs font-semibold uppercase tracking-wider border-r border-black last:border-r-0 cursor-pointer transition-colors ${
                category === cat
                  ? "bg-black text-white"
                  : "bg-white text-black hover:bg-[var(--color-surface)]"
              }`}
            >
              {cat === "all" ? "All" : CATEGORY_LABELS[cat] || cat}
            </button>
          ))}
        </div>
        <input
          type="text"
          placeholder="Search models..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="border-2 border-black px-3 py-1.5 text-sm font-sans w-64 focus:outline-none focus:ring-0"
        />
        <span className="text-xs font-mono text-[var(--color-text-secondary)] ml-auto">
          {filtered.length} model{filtered.length !== 1 ? "s" : ""}
        </span>
      </div>

      {/* Model Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        {filtered.map((model) => {
          const catColor = CATEGORY_COLORS[model.category] || "#000000";
          const isExpanded = expanded === model.id;
          return (
            <div
              key={model.id}
              className="border-2 border-black bg-white"
              style={{ borderLeftWidth: "6px", borderLeftColor: catColor }}
            >
              {/* Card Header */}
              <div className="p-4">
                <div className="flex items-start justify-between mb-2">
                  <div>
                    <span
                      className="font-mono text-2xl font-bold"
                      style={{ color: catColor }}
                    >
                      {model.abbreviation}
                    </span>
                    <h3 className="text-lg font-semibold mt-1">{model.name}</h3>
                  </div>
                  <span
                    className="text-[10px] font-semibold uppercase tracking-wider px-2 py-0.5 border"
                    style={{ color: catColor, borderColor: catColor }}
                  >
                    {CATEGORY_LABELS[model.category] || model.category}
                  </span>
                </div>

                {/* Domains */}
                <div className="flex flex-wrap gap-1 mb-3">
                  {model.domains_covered.map((d) => (
                    <span
                      key={d}
                      className="text-[10px] font-semibold uppercase tracking-wider px-1.5 py-0.5 text-white"
                      style={{ backgroundColor: DOMAIN_COLORS[d] || "#555555" }}
                    >
                      {DOMAIN_LABELS[d] || d}
                    </span>
                  ))}
                </div>

                {/* Meta */}
                <div className="flex flex-wrap gap-4 text-xs font-mono text-[var(--color-text-secondary)]">
                  <span>
                    Evidence:{" "}
                    <span style={{ color: getEvidenceColor(model.evidence_rating), fontWeight: 600 }}>
                      {model.evidence_rating}
                    </span>
                  </span>
                  <span>Political: {model.political_feasibility}</span>
                  <span>Launch: {model.timeline_to_launch}</span>
                </div>

                {/* Expand toggle */}
                <button
                  onClick={() => setExpanded(isExpanded ? null : model.id)}
                  className="mt-3 text-xs font-semibold uppercase tracking-wider text-[var(--color-text-secondary)] hover:text-black cursor-pointer"
                >
                  {isExpanded ? "- Collapse" : "+ Details"}
                </button>
              </div>

              {/* Expanded Details */}
              {isExpanded && (
                <div className="border-t-2 border-black p-4 bg-[var(--color-surface)]">
                  {/* Description */}
                  <div className="mb-4">
                    <h4 className="text-sm font-semibold mb-1">Description</h4>
                    <p className="text-sm text-[var(--color-text-secondary)] leading-relaxed">
                      {model.description}
                    </p>
                  </div>

                  {/* Target Population */}
                  <div className="mb-4">
                    <h4 className="text-sm font-semibold mb-1">Target Population</h4>
                    <div className="flex flex-wrap gap-1">
                      {model.target_population.map((p) => (
                        <span
                          key={p}
                          className="text-[10px] font-mono px-1.5 py-0.5 border border-black bg-white"
                        >
                          {p}
                        </span>
                      ))}
                    </div>
                  </div>

                  {/* Funding Sources */}
                  <div className="mb-4">
                    <h4 className="text-sm font-semibold mb-1">Funding Sources</h4>
                    <div className="flex flex-wrap gap-1">
                      {model.funding_sources.map((f) => (
                        <span
                          key={f}
                          className="text-[10px] font-mono px-1.5 py-0.5 border border-[var(--color-border)] bg-white"
                        >
                          {f}
                        </span>
                      ))}
                    </div>
                  </div>

                  {/* Key Features */}
                  <div className="mb-4">
                    <h4 className="text-sm font-semibold mb-1">Key Features</h4>
                    <ul className="list-none space-y-1">
                      {model.key_features.map((f, i) => (
                        <li key={i} className="text-sm text-[var(--color-text-secondary)] flex gap-2">
                          <span className="text-black font-mono text-xs mt-0.5">+</span>
                          {f}
                        </li>
                      ))}
                    </ul>
                  </div>

                  {/* Limitations */}
                  <div className="mb-4">
                    <h4 className="text-sm font-semibold mb-1">Limitations</h4>
                    <ul className="list-none space-y-1">
                      {model.limitations.map((l, i) => (
                        <li key={i} className="text-sm text-[var(--color-text-secondary)] flex gap-2">
                          <span className="text-[#8B1A1A] font-mono text-xs mt-0.5">-</span>
                          {l}
                        </li>
                      ))}
                    </ul>
                  </div>

                  {/* Staffing Model */}
                  <div className="mb-4">
                    <h4 className="text-sm font-semibold mb-1">Staffing Model</h4>
                    <div className="grid grid-cols-2 gap-2">
                      {Object.entries(model.staffing_model).map(([role, desc]) => (
                        <div key={role} className="text-xs">
                          <span className="font-mono font-semibold">{role}:</span>{" "}
                          <span className="text-[var(--color-text-secondary)]">{desc}</span>
                        </div>
                      ))}
                    </div>
                  </div>

                  {/* Governance */}
                  <div className="mb-4">
                    <h4 className="text-sm font-semibold mb-1">Governance Structure</h4>
                    <p className="text-sm text-[var(--color-text-secondary)]">{model.governance_structure}</p>
                  </div>

                  {/* Regulatory Requirements */}
                  <div className="mb-4">
                    <h4 className="text-sm font-semibold mb-1">Regulatory Requirements</h4>
                    <ul className="list-none space-y-1">
                      {model.regulatory_requirements.map((r, i) => (
                        <li key={i} className="text-xs font-mono text-[var(--color-text-secondary)]">
                          {r}
                        </li>
                      ))}
                    </ul>
                  </div>

                  {/* Example Sites */}
                  <div>
                    <h4 className="text-sm font-semibold mb-1">Example Sites</h4>
                    <div className="flex flex-wrap gap-1">
                      {model.example_sites.map((s) => (
                        <span
                          key={s}
                          className="text-[10px] font-mono px-1.5 py-0.5 border border-[var(--color-border)] bg-white"
                        >
                          {s}
                        </span>
                      ))}
                    </div>
                  </div>
                </div>
              )}
            </div>
          );
        })}
      </div>

      {filtered.length === 0 && (
        <div className="text-center py-12 text-sm text-[var(--color-text-secondary)] font-mono">
          No models match your filters.
        </div>
      )}
    </div>
  );
}
