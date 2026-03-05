import { useState, useEffect } from "react";
import { getModels, getArchitectures } from "./api/client";
import type { CoordinationModel, Architecture } from "./types";
import ModelBrowser from "./components/ModelBrowser";
import ArchitectureDesigner from "./components/ArchitectureDesigner";
import BlueprintViewer from "./components/BlueprintViewer";
import ComparisonView from "./components/ComparisonView";
import TimelineView from "./components/TimelineView";
import BudgetView from "./components/BudgetView";
import RiskDashboard from "./components/RiskDashboard";

type Tab = "models" | "designer" | "blueprints" | "compare" | "timeline" | "budget" | "risks";

const TABS: { key: Tab; label: string }[] = [
  { key: "models", label: "Models" },
  { key: "designer", label: "Designer" },
  { key: "blueprints", label: "Blueprints" },
  { key: "compare", label: "Compare" },
  { key: "timeline", label: "Timeline" },
  { key: "budget", label: "Budget" },
  { key: "risks", label: "Risks" },
];

export default function App() {
  const [activeTab, setActiveTab] = useState<Tab>("models");
  const [models, setModels] = useState<CoordinationModel[]>([]);
  const [architectures, setArchitectures] = useState<Architecture[]>([]);
  const [loading, setLoading] = useState(true);

  const refreshArchitectures = () => {
    getArchitectures()
      .then(setArchitectures)
      .catch(() => setArchitectures([]));
  };

  useEffect(() => {
    Promise.allSettled([getModels(), getArchitectures()]).then(([m, a]) => {
      if (m.status === "fulfilled") setModels(m.value);
      if (a.status === "fulfilled") setArchitectures(a.value);
      setLoading(false);
    });
  }, []);

  const handleArchitectureGenerated = (arch: Architecture) => {
    setArchitectures((prev) => [...prev, arch]);
  };

  const navigateTo = (tab: Tab) => setActiveTab(tab);

  return (
    <div className="min-h-full flex flex-col">
      {/* Header */}
      <header style={{ borderBottom: "2px solid black", padding: "16px 24px" }}>
        <div style={{ display: "flex", flexWrap: "wrap", alignItems: "baseline", gap: "8px" }}>
          <h1 style={{ fontSize: "28px", fontFamily: "var(--font-serif)", fontWeight: 700, letterSpacing: "-0.01em" }}>DOMES ARCHITECT</h1>
          <span style={{ fontSize: "14px", color: "var(--color-text-secondary)", textTransform: "uppercase", letterSpacing: "0.04em" }}>
            Coordination Architecture Designer
          </span>
        </div>
        {/* Stats bar */}
        <div style={{ display: "flex", flexWrap: "wrap", gap: "16px", marginTop: "8px", fontSize: "12px", fontFamily: "var(--font-mono, monospace)", color: "var(--color-text-secondary)" }}>
          <span>
            MODELS:{" "}
            <span style={{ color: "black", fontWeight: 600 }}>{loading ? "..." : models.length}</span>
          </span>
          <span>
            ARCHITECTURES:{" "}
            <span style={{ color: "black", fontWeight: 600 }}>{loading ? "..." : architectures.length}</span>
          </span>
        </div>
      </header>

      {/* Tab Navigation */}
      <nav style={{ display: "flex", borderBottom: "2px solid black", overflowX: "auto", WebkitOverflowScrolling: "touch" }}>
        {TABS.map((tab) => (
          <button
            key={tab.key}
            onClick={() => setActiveTab(tab.key)}
            style={{
              padding: "10px 20px",
              fontSize: "12px",
              fontWeight: 600,
              textTransform: "uppercase",
              letterSpacing: "0.08em",
              background: activeTab === tab.key ? "black" : "white",
              color: activeTab === tab.key ? "white" : "black",
              border: "none",
              borderRight: "1px solid black",
              cursor: "pointer",
              whiteSpace: "nowrap",
              minHeight: "44px",
              transition: "background 0.15s, color 0.15s",
            }}
          >
            {tab.label}
          </button>
        ))}
      </nav>

      {/* Content */}
      <main className="flex-1 overflow-auto">
        {activeTab === "models" && <ModelBrowser models={models} loading={loading} />}
        {activeTab === "designer" && (
          <ArchitectureDesigner
            onGenerated={handleArchitectureGenerated}
            onNavigate={navigateTo}
          />
        )}
        {activeTab === "blueprints" && (
          <BlueprintViewer
            architectures={architectures}
            onRefresh={refreshArchitectures}
          />
        )}
        {activeTab === "compare" && <ComparisonView architectures={architectures} />}
        {activeTab === "timeline" && <TimelineView architectures={architectures} />}
        {activeTab === "budget" && <BudgetView architectures={architectures} />}
        {activeTab === "risks" && <RiskDashboard architectures={architectures} />}
      </main>
    </div>
  );
}
