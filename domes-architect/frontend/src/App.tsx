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
      <header className="border-b-2 border-black px-6 py-4">
        <div className="flex items-baseline gap-4">
          <h1 className="text-3xl font-bold tracking-tight">DOMES ARCHITECT</h1>
          <span className="text-sm text-[var(--color-text-secondary)] font-sans tracking-wide uppercase">
            Coordination Architecture Designer
          </span>
        </div>
        {/* Stats bar */}
        <div className="flex gap-6 mt-2 text-xs font-mono text-[var(--color-text-secondary)]">
          <span>
            MODELS:{" "}
            <span className="text-black font-semibold">{loading ? "..." : models.length}</span>
          </span>
          <span>
            ARCHITECTURES:{" "}
            <span className="text-black font-semibold">{loading ? "..." : architectures.length}</span>
          </span>
        </div>
      </header>

      {/* Tab Navigation */}
      <nav className="flex border-b-2 border-black">
        {TABS.map((tab) => (
          <button
            key={tab.key}
            onClick={() => setActiveTab(tab.key)}
            className={`px-5 py-2.5 text-xs font-semibold uppercase tracking-widest border-r border-black transition-colors cursor-pointer ${
              activeTab === tab.key
                ? "bg-black text-white"
                : "bg-white text-black hover:bg-[var(--color-surface)]"
            }`}
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
