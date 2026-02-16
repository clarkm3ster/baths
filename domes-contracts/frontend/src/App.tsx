import { useState, useEffect } from "react";
import type { AgreementStats } from "./types";
import { getAgreementStats } from "./api/client";
import GapBrowser from "./components/GapBrowser";
import AgreementGenerator from "./components/AgreementGenerator";
import TemplateLibrary from "./components/TemplateLibrary";
import ComplianceDashboard from "./components/ComplianceDashboard";
import ConsentCenter from "./components/ConsentCenter";
import ExecutionTracker from "./components/ExecutionTracker";

type Tab = "gaps" | "agreements" | "templates" | "compliance" | "consent" | "tracker";

const TABS: { key: Tab; label: string }[] = [
  { key: "gaps", label: "Gaps" },
  { key: "agreements", label: "Agreements" },
  { key: "templates", label: "Templates" },
  { key: "compliance", label: "Compliance" },
  { key: "consent", label: "Consent" },
  { key: "tracker", label: "Tracker" },
];

export default function App() {
  const [activeTab, setActiveTab] = useState<Tab>("gaps");
  const [stats, setStats] = useState<AgreementStats | null>(null);
  const [refreshKey, setRefreshKey] = useState(0);

  const reload = () => setRefreshKey((k) => k + 1);

  useEffect(() => {
    getAgreementStats().then(setStats).catch(() => {});
  }, [refreshKey]);

  return (
    <div className="min-h-screen flex flex-col">
      {/* ---- Header ---- */}
      <header style={{ borderBottom: "2px solid black", padding: "16px 24px" }}>
        <div style={{ display: "flex", flexWrap: "wrap", alignItems: "baseline", gap: "8px" }}>
          <h1 style={{ fontSize: "28px", fontFamily: "var(--font-serif)", fontWeight: 700, letterSpacing: "-0.01em" }}>DOMES CONTRACTS</h1>
          <span style={{ fontSize: "14px", color: "var(--color-text-secondary)", fontFamily: "var(--font-mono, monospace)", textTransform: "uppercase", letterSpacing: "0.08em" }}>
            Agreement Generation Engine
          </span>
        </div>

        {/* Stats bar */}
        {stats && (
          <div style={{ marginTop: "12px", display: "flex", flexWrap: "wrap", gap: "16px", fontSize: "12px", fontFamily: "var(--font-mono, monospace)", textTransform: "uppercase", letterSpacing: "0.04em" }}>
            <span>
              Total:{" "}
              <strong style={{ fontSize: "14px" }}>{stats.total}</strong>
            </span>
            <span style={{ color: "var(--color-draft)" }}>
              Draft:{" "}
              <strong style={{ fontSize: "14px" }}>{stats.by_status.draft ?? 0}</strong>
            </span>
            <span style={{ color: "var(--color-in-review)" }}>
              In Review:{" "}
              <strong style={{ fontSize: "14px" }}>{stats.by_status.in_review ?? 0}</strong>
            </span>
            <span style={{ color: "var(--color-executed)" }}>
              Executed:{" "}
              <strong style={{ fontSize: "14px" }}>{stats.by_status.executed ?? 0}</strong>
            </span>
          </div>
        )}
      </header>

      {/* ---- Tabs ---- */}
      <nav style={{ borderBottom: "1px solid var(--color-border)", display: "flex", gap: 0, overflowX: "auto", WebkitOverflowScrolling: "touch", paddingLeft: "24px", paddingRight: "24px" }}>
        {TABS.map((t) => (
          <button
            key={t.key}
            onClick={() => setActiveTab(t.key)}
            style={{
              padding: "12px 20px",
              fontSize: "12px",
              fontFamily: "var(--font-mono, 'JetBrains Mono', monospace)",
              textTransform: "uppercase",
              letterSpacing: "0.08em",
              borderBottom: activeTab === t.key ? "2px solid black" : "2px solid transparent",
              color: activeTab === t.key ? "black" : "var(--color-text-secondary)",
              fontWeight: activeTab === t.key ? 700 : 400,
              background: "none",
              border: "none",
              borderBottomWidth: "2px",
              borderBottomStyle: "solid",
              borderBottomColor: activeTab === t.key ? "black" : "transparent",
              cursor: "pointer",
              whiteSpace: "nowrap",
              minHeight: "44px",
              transition: "color 0.15s",
            }}
          >
            {t.label}
          </button>
        ))}
      </nav>

      {/* ---- Content ---- */}
      <main className="flex-1 overflow-auto">
        {activeTab === "gaps" && <GapBrowser onGenerated={reload} />}
        {activeTab === "agreements" && <AgreementGenerator onGenerated={reload} />}
        {activeTab === "templates" && <TemplateLibrary />}
        {activeTab === "compliance" && <ComplianceDashboard onValidated={reload} />}
        {activeTab === "consent" && <ConsentCenter />}
        {activeTab === "tracker" && <ExecutionTracker onUpdated={reload} />}
      </main>
    </div>
  );
}
