import { useState, useEffect } from "react";
import type { Provision, Section, TaxonomyStats, GraphStats } from "../types";
import { getTaxonomyStats, getGraphStats } from "../api/client";
import SearchView from "./SearchView";
import BrowseView from "./BrowseView";
import GraphView from "./GraphView";
import MonitorView from "./MonitorView";
import ProvisionDetail from "./ProvisionDetail";
import { getProvision } from "../api/client";

function useIsMobile() {
  const [isMobile, setIsMobile] = useState(window.innerWidth <= 640);
  useEffect(() => {
    const handler = () => setIsMobile(window.innerWidth <= 640);
    window.addEventListener("resize", handler);
    return () => window.removeEventListener("resize", handler);
  }, []);
  return isMobile;
}

export default function App() {
  const [section, setSection] = useState<Section>("search");
  const [selectedProvision, setSelectedProvision] = useState<Provision | null>(null);
  const [stats, setStats] = useState<TaxonomyStats | null>(null);
  const [graphStats, setGraphStats] = useState<GraphStats | null>(null);
  const isMobile = useIsMobile();
  const [mobileNavOpen, setMobileNavOpen] = useState(false);

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
        <div style={{ display: "flex", alignItems: "center", gap: "12px" }}>
          {isMobile && (
            <button
              onClick={() => setMobileNavOpen(!mobileNavOpen)}
              style={{ background: "none", border: "1px solid var(--color-border)", color: "#FFF", cursor: "pointer", padding: "6px 10px", fontFamily: "var(--font-mono)", fontSize: "12px", minHeight: "44px", minWidth: "44px", display: "flex", alignItems: "center", justifyContent: "center" }}
            >
              {mobileNavOpen ? "\u2715" : "\u2630"}
            </button>
          )}
          <div style={{ fontFamily: "var(--font-mono)", fontSize: "13px", fontWeight: 600, letterSpacing: "0.08em", textTransform: "uppercase", color: "#FFF" }}>
            DOMES LEGAL ENGINE
          </div>
        </div>
        {!isMobile && (
          <div style={{ fontFamily: "var(--font-mono)", fontSize: "10px", color: "var(--color-text-tertiary)" }}>
            STRUCTURED LAW
          </div>
        )}
      </header>

      <div style={{ display: "flex", flex: 1, overflow: "hidden" }}>
        {/* Sidebar - hidden on mobile unless toggled */}
        {(!isMobile || mobileNavOpen) && (
          <nav style={{
            width: isMobile ? "100%" : "160px",
            borderRight: isMobile ? "none" : "1px solid var(--color-border)",
            display: "flex",
            flexDirection: isMobile ? "row" : "column",
            paddingTop: isMobile ? "0" : "8px",
            flexWrap: isMobile ? "wrap" : undefined,
            borderBottom: isMobile ? "1px solid var(--color-border)" : undefined,
            position: isMobile ? "absolute" : undefined,
            zIndex: isMobile ? 50 : undefined,
            background: isMobile ? "var(--color-surface)" : undefined,
            ...(isMobile ? { left: 0, right: 0 } : {}),
          }}>
            {NAV_ITEMS.map((item) => (
              <div
                key={item.id}
                className={`nav-item ${section === item.id ? "nav-item--active" : ""}`}
                onClick={() => {
                  setSection(item.id);
                  if (isMobile) setMobileNavOpen(false);
                }}
                style={isMobile ? { flex: "1 1 auto", textAlign: "center", borderLeft: "none", borderBottom: section === item.id ? "3px solid var(--color-accent)" : "3px solid transparent", minHeight: "44px", display: "flex", alignItems: "center", justifyContent: "center" } : undefined}
              >
                {item.label}
              </div>
            ))}
          </nav>
        )}

        {/* Content */}
        <main style={{ flex: 1, overflow: "auto" }}>
          {section === "search" && <SearchView onSelect={handleSelect} />}
          {section === "browse" && <BrowseView onSelect={handleSelect} />}
          {section === "graph" && <GraphView onSelectProvision={handleGraphSelect} />}
          {section === "monitor" && <MonitorView />}
        </main>
      </div>

      {/* Footer status bar */}
      <footer style={{ borderTop: "1px solid var(--color-border)", padding: "6px 20px", display: "flex", gap: isMobile ? "10px" : "20px", fontFamily: "var(--font-mono)", fontSize: "10px", color: "var(--color-text-tertiary)", background: "var(--color-surface)", flexWrap: "wrap" }}>
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
