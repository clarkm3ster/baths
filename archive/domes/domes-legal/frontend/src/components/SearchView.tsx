import { useState, useEffect } from "react";
import type { Provision, DomainCount } from "../types";
import { DOMAIN_COLORS, DOMAIN_LABELS } from "../types";
import { searchProvisions, getDomains } from "../api/client";
import DomainBadge from "./DomainBadge";

interface Props {
  onSelect: (p: Provision) => void;
}

export default function SearchView({ onSelect }: Props) {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<Provision[]>([]);
  const [total, setTotal] = useState(0);
  const [domains, setDomains] = useState<DomainCount[]>([]);
  const [selectedDomains, setSelectedDomains] = useState<string[]>([]);
  const [selectedTypes, setSelectedTypes] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    getDomains().then(setDomains);
    doSearch();
  }, []);

  async function doSearch() {
    setLoading(true);
    const res = await searchProvisions({
      query: query || undefined,
      domains: selectedDomains.length > 0 ? selectedDomains : undefined,
      provision_types: selectedTypes.length > 0 ? selectedTypes : undefined,
    });
    setResults(res.items);
    setTotal(res.total);
    setLoading(false);
  }

  function toggleDomain(d: string) {
    setSelectedDomains((prev) => prev.includes(d) ? prev.filter((x) => x !== d) : [...prev, d]);
  }

  function toggleType(t: string) {
    setSelectedTypes((prev) => prev.includes(t) ? prev.filter((x) => x !== t) : [...prev, t]);
  }

  useEffect(() => {
    const timer = setTimeout(doSearch, 300);
    return () => clearTimeout(timer);
  }, [query, selectedDomains, selectedTypes]);

  const types = ["right", "protection", "obligation", "enforcement"];

  return (
    <div style={{ padding: "28px 32px" }}>
      <div className="section-label">Search Provisions</div>

      {/* Search input */}
      <input
        className="search-input"
        placeholder="Search by citation, title, or text..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        style={{ marginBottom: "16px" }}
      />

      {/* Domain filters */}
      <div style={{ display: "flex", flexWrap: "wrap", gap: "6px", marginBottom: "8px" }}>
        {domains.map((d) => (
          <button
            key={d.domain}
            onClick={() => toggleDomain(d.domain)}
            style={{
              fontFamily: "var(--font-mono)", fontSize: "10px", textTransform: "uppercase",
              letterSpacing: "0.04em", padding: "4px 10px", cursor: "pointer",
              border: selectedDomains.includes(d.domain) ? "2px solid" : "1px solid var(--color-border)",
              borderColor: selectedDomains.includes(d.domain) ? DOMAIN_COLORS[d.domain] || "#333" : undefined,
              background: selectedDomains.includes(d.domain) ? DOMAIN_COLORS[d.domain] + "25" : "var(--color-surface)",
              color: DOMAIN_COLORS[d.domain] || "#999",
            }}
          >
            {DOMAIN_LABELS[d.domain] || d.domain} ({d.count})
          </button>
        ))}
      </div>

      {/* Type filters */}
      <div style={{ display: "flex", gap: "6px", marginBottom: "20px" }}>
        {types.map((t) => (
          <button
            key={t}
            onClick={() => toggleType(t)}
            style={{
              fontFamily: "var(--font-mono)", fontSize: "10px", textTransform: "uppercase",
              padding: "4px 10px", cursor: "pointer",
              border: selectedTypes.includes(t) ? "1px solid var(--color-accent)" : "1px solid var(--color-border)",
              background: selectedTypes.includes(t) ? "var(--color-accent)" + "30" : "var(--color-surface)",
              color: selectedTypes.includes(t) ? "#FFF" : "var(--color-text-secondary)",
            }}
          >
            {t}
          </button>
        ))}
      </div>

      {/* Results header */}
      <div style={{ fontFamily: "var(--font-mono)", fontSize: "11px", color: "var(--color-text-tertiary)", marginBottom: "12px" }}>
        {loading ? "SEARCHING..." : `${total} PROVISIONS`}
      </div>

      {/* Results */}
      <div>
        {results.map((p) => (
          <div key={p.id} className="provision-card" onClick={() => onSelect(p)}>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: "4px" }}>
              <span style={{ fontFamily: "var(--font-mono)", fontSize: "12px", fontWeight: 500 }}>
                {p.citation}
              </span>
              <DomainBadge domain={p.domain} />
            </div>
            <div style={{ fontFamily: "var(--font-serif)", fontSize: "15px", fontWeight: 600, marginBottom: "4px" }}>
              {p.title}
            </div>
            <div style={{ fontSize: "13px", color: "var(--color-text-secondary)", lineHeight: 1.5, overflow: "hidden", textOverflow: "ellipsis", display: "-webkit-box", WebkitLineClamp: 2, WebkitBoxOrient: "vertical" as const }}>
              {p.full_text}
            </div>
            <div style={{ marginTop: "6px", display: "flex", gap: "4px", alignItems: "center" }}>
              <span style={{ fontFamily: "var(--font-mono)", fontSize: "10px", textTransform: "uppercase", color: "var(--color-text-tertiary)", padding: "1px 4px", border: "1px solid var(--color-border-light)" }}>
                {p.provision_type}
              </span>
              <span style={{ fontFamily: "var(--font-mono)", fontSize: "10px", color: "var(--color-text-tertiary)" }}>
                {p.source_type}
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
