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
      <header className="border-b-2 border-black px-6 py-4">
        <div className="flex items-baseline gap-4">
          <h1 className="text-3xl tracking-tight">DOMES CONTRACTS</h1>
          <span className="text-sm text-[var(--color-text-secondary)] font-mono uppercase tracking-widest">
            Agreement Generation Engine
          </span>
        </div>

        {/* Stats bar */}
        {stats && (
          <div className="mt-3 flex gap-6 text-xs font-mono uppercase tracking-wider">
            <span>
              Total:{" "}
              <strong className="text-sm">{stats.total}</strong>
            </span>
            <span className="text-[var(--color-draft)]">
              Draft:{" "}
              <strong className="text-sm">{stats.by_status.draft ?? 0}</strong>
            </span>
            <span className="text-[var(--color-in-review)]">
              In Review:{" "}
              <strong className="text-sm">{stats.by_status.in_review ?? 0}</strong>
            </span>
            <span className="text-[var(--color-executed)]">
              Executed:{" "}
              <strong className="text-sm">{stats.by_status.executed ?? 0}</strong>
            </span>
          </div>
        )}
      </header>

      {/* ---- Tabs ---- */}
      <nav className="border-b border-[var(--color-border)] px-6 flex gap-0">
        {TABS.map((t) => (
          <button
            key={t.key}
            onClick={() => setActiveTab(t.key)}
            className={`px-5 py-3 text-xs font-mono uppercase tracking-widest border-b-2 transition-colors cursor-pointer ${
              activeTab === t.key
                ? "border-black text-black font-bold"
                : "border-transparent text-[var(--color-text-secondary)] hover:text-black"
            }`}
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
