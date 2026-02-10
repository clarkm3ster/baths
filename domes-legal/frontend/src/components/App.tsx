import { useState, useEffect } from "react";
import type { Provision, Section, TaxonomyStats, GraphStats } from "../types";
import { getTaxonomyStats, getGraphStats } from "../api/client";
import SearchView from "./SearchView";
import BrowseView from "./BrowseView";
import GraphView from "./GraphView";
import MonitorView from "./MonitorView";
import ProvisionDetail from "./ProvisionDetail";
import { getProvision } from "../api/client";

export default function App() {
  const [section, setSection] = useState<Section>("search");
  const [selectedProvision, setSelectedProvision] = useState<Provision | null>(null);
  const [stats, setStats] = useState<TaxonomyStats | null>(null);
  const [graphStats, setGraphStats] = useState<GraphStats | null>(null);

  useEffect(() => {
    getTaxonomyStats().then(setStats);
    getGraphStats().then(setGraphStats);
  }, []);

  function handleSelect(p: Provision) {
    setSelectedProvision(p);
  }

  async function handleGraphSelect(id: number) {
    const p = await getProvision(id);
    setSelectedProvision(p);
  }

  const NAV_ITEMS: { id: Section; label: string }[] = [
    { id: "search", label: "Search" },
    { id: "browse", label: "Browse" },
    { id: "graph", label: "Graph" },
    { id: "monitor", label: "Monitor" },
  ];

  return (
    <div style={{ display: "flex", flexDirection: "column", height: "100vh" }}>
      {/* Header */}
      <header style={{ borderBottom: "1px solid var(--color-border)", padding: "12px 20px", display: "flex", justifyContent: "space-between", alignItems: "center", background: "var(--color-surface)" }}>
        <div style={{ fontFamily: "var(--font-mono)", fontSize: "13px", fontWeight: 600, letterSpacing: "0.08em", textTransform: "uppercase", color: "#FFF" }}>
          DOMES LEGAL ENGINE
        </div>
        <div style={{ fontFamily: "var(--font-mono)", fontSize: "10px", color: "var(--color-text-tertiary)" }}>
          STRUCTURED LAW
        </div>
      </header>

      <div style={{ display: "flex", flex: 1, overflow: "hidden" }}>
        {/* Sidebar */}
        <nav style={{ width: "160px", borderRight: "1px solid var(--color-border)", display: "flex", flexDirection: "column", paddingTop: "8px" }}>
          {NAV_ITEMS.map((item) => (
            <div
              key={item.id}
              className={`nav-item ${section === item.id ? "nav-item--active" : ""}`}
              onClick={() => setSection(item.id)}
            >
              {item.label}
            </div>
          ))}
        </nav>

        {/* Content */}
        <main style={{ flex: 1, overflow: "auto" }}>
          {section === "search" && <SearchView onSelect={handleSelect} />}
          {section === "browse" && <BrowseView onSelect={handleSelect} />}
          {section === "graph" && <GraphView onSelectProvision={handleGraphSelect} />}
          {section === "monitor" && <MonitorView />}
        </main>
      </div>

      {/* Footer status bar */}
      <footer style={{ borderTop: "1px solid var(--color-border)", padding: "6px 20px", display: "flex", gap: "20px", fontFamily: "var(--font-mono)", fontSize: "10px", color: "var(--color-text-tertiary)", background: "var(--color-surface)" }}>
        <span>
          <span className="status-indicator status-indicator--active" style={{ marginRight: "4px" }} />
          {stats?.total_provisions || 0} provisions
        </span>
        <span>{graphStats?.edges || 0} relationships</span>
        <span>{stats?.total_tags || 0} tags</span>
        <span style={{ flex: 1 }} />
        <span>Port 8003</span>
      </footer>

      {/* Detail panel */}
      {selectedProvision && (
        <ProvisionDetail
          provision={selectedProvision}
          onClose={() => setSelectedProvision(null)}
        />
      )}
    </div>
  );
}
