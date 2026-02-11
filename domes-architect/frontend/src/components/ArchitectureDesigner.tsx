import { useState } from "react";
import { generateArchitecture } from "../api/client";
import type { Architecture } from "../types";
import { DOMAIN_LABELS, DOMAIN_COLORS } from "../types";

type Tab = "models" | "designer" | "blueprints" | "compare" | "timeline" | "budget" | "risks";

interface Props {
  onGenerated: (arch: Architecture) => void;
  onNavigate: (tab: Tab) => void;
}

const AVAILABLE_DOMAINS = [
  "health",
  "behavioral_health",
  "housing",
  "income",
  "education",
  "child_welfare",
  "justice",
];

const POLITICAL_OPTIONS = ["supportive", "neutral", "resistant", "hostile"];
const TIME_OPTIONS = ["1yr", "3yr", "5yr"];

const SCORE_DIMENSIONS: { key: string; label: string }[] = [
  { key: "coverage", label: "Coverage" },
  { key: "budget_feasibility", label: "Budget Feasibility" },
  { key: "political_feasibility", label: "Political Feasibility" },
  { key: "speed", label: "Speed" },
  { key: "sustainability", label: "Sustainability" },
  { key: "population_fit", label: "Population Fit" },
  { key: "cost_efficiency", label: "Cost Efficiency" },
];

function formatCurrency(n: number): string {
  return new Intl.NumberFormat("en-US", { style: "currency", currency: "USD", maximumFractionDigits: 0 }).format(n);
}

export default function ArchitectureDesigner({ onGenerated, onNavigate }: Props) {
  const [geography, setGeography] = useState("");
  const [populationDesc, setPopulationDesc] = useState("");
  const [populationSize, setPopulationSize] = useState<number | "">("");
  const [annualBudget, setAnnualBudget] = useState<number | "">("");
  const [politicalContext, setPoliticalContext] = useState("neutral");
  const [timeHorizon, setTimeHorizon] = useState("3yr");
  const [domains, setDomains] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<Architecture | null>(null);

  const toggleDomain = (d: string) => {
    setDomains((prev) => (prev.includes(d) ? prev.filter((x) => x !== d) : [...prev, d]));
  };

  const handleGenerate = async () => {
    if (!geography || !populationDesc || !populationSize || !annualBudget || domains.length === 0) {
      setError("Please fill in all fields and select at least one domain.");
      return;
    }
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const arch = await generateArchitecture({
        geography,
        population_description: populationDesc,
        population_size: populationSize,
        annual_budget: annualBudget,
        political_context: politicalContext,
        time_horizon: timeHorizon,
        domains,
      });
      setResult(arch);
      onGenerated(arch);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Generation failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-6 max-w-5xl">
      <h2 className="text-2xl font-bold mb-6">Architecture Designer</h2>

      {/* Form */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
        {/* Geography */}
        <div>
          <label className="block text-xs font-semibold uppercase tracking-wider mb-1">
            Geography
          </label>
          <input
            type="text"
            value={geography}
            onChange={(e) => setGeography(e.target.value)}
            placeholder="e.g. Philadelphia, PA"
            className="w-full border-2 border-black px-3 py-2 text-sm focus:outline-none"
          />
        </div>

        {/* Population Description */}
        <div>
          <label className="block text-xs font-semibold uppercase tracking-wider mb-1">
            Population Description
          </label>
          <input
            type="text"
            value={populationDesc}
            onChange={(e) => setPopulationDesc(e.target.value)}
            placeholder="e.g. Adults with complex needs"
            className="w-full border-2 border-black px-3 py-2 text-sm focus:outline-none"
          />
        </div>

        {/* Population Size */}
        <div>
          <label className="block text-xs font-semibold uppercase tracking-wider mb-1">
            Population Size
          </label>
          <input
            type="number"
            value={populationSize}
            onChange={(e) => setPopulationSize(e.target.value ? Number(e.target.value) : "")}
            placeholder="e.g. 50000"
            className="w-full border-2 border-black px-3 py-2 text-sm focus:outline-none font-mono"
          />
        </div>

        {/* Annual Budget */}
        <div>
          <label className="block text-xs font-semibold uppercase tracking-wider mb-1">
            Annual Budget
          </label>
          <input
            type="number"
            value={annualBudget}
            onChange={(e) => setAnnualBudget(e.target.value ? Number(e.target.value) : "")}
            placeholder="e.g. 25000000"
            className="w-full border-2 border-black px-3 py-2 text-sm focus:outline-none font-mono"
          />
          {annualBudget !== "" && (
            <span className="text-xs font-mono text-[var(--color-text-secondary)] mt-0.5 block">
              {formatCurrency(annualBudget)}
            </span>
          )}
        </div>

        {/* Political Context */}
        <div>
          <label className="block text-xs font-semibold uppercase tracking-wider mb-1">
            Political Context
          </label>
          <select
            value={politicalContext}
            onChange={(e) => setPoliticalContext(e.target.value)}
            className="w-full border-2 border-black px-3 py-2 text-sm focus:outline-none bg-white"
          >
            {POLITICAL_OPTIONS.map((opt) => (
              <option key={opt} value={opt}>
                {opt.charAt(0).toUpperCase() + opt.slice(1)}
              </option>
            ))}
          </select>
        </div>

        {/* Time Horizon */}
        <div>
          <label className="block text-xs font-semibold uppercase tracking-wider mb-1">
            Time Horizon
          </label>
          <select
            value={timeHorizon}
            onChange={(e) => setTimeHorizon(e.target.value)}
            className="w-full border-2 border-black px-3 py-2 text-sm focus:outline-none bg-white"
          >
            {TIME_OPTIONS.map((opt) => (
              <option key={opt} value={opt}>
                {opt}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Domains */}
      <div className="mb-6">
        <label className="block text-xs font-semibold uppercase tracking-wider mb-2">
          Domains (select at least one)
        </label>
        <div className="flex flex-wrap gap-2">
          {AVAILABLE_DOMAINS.map((d) => {
            const selected = domains.includes(d);
            const color = DOMAIN_COLORS[d] || "#555555";
            return (
              <button
                key={d}
                onClick={() => toggleDomain(d)}
                className="px-3 py-1.5 text-xs font-semibold uppercase tracking-wider border-2 cursor-pointer transition-colors"
                style={{
                  borderColor: color,
                  backgroundColor: selected ? color : "white",
                  color: selected ? "white" : color,
                }}
              >
                {DOMAIN_LABELS[d] || d}
              </button>
            );
          })}
        </div>
      </div>

      {/* Error */}
      {error && (
        <div className="mb-4 border-2 border-[#8B1A1A] bg-[#8B1A1A]/5 p-3 text-sm text-[#8B1A1A] font-mono">
          {error}
        </div>
      )}

      {/* Generate Button */}
      <button
        onClick={handleGenerate}
        disabled={loading}
        className="btn-primary mb-8 disabled:opacity-50 disabled:cursor-not-allowed"
      >
        {loading ? "Analyzing Constraints..." : "Generate Architecture"}
      </button>

      {/* Loading */}
      {loading && (
        <div className="mb-8 p-6 border-2 border-black bg-[var(--color-surface)]">
          <div className="flex items-center gap-3">
            <div className="w-3 h-3 bg-black animate-pulse" />
            <span className="text-sm font-mono">
              Analyzing constraints and generating optimal architecture...
            </span>
          </div>
        </div>
      )}

      {/* Result */}
      {result && !loading && (
        <div className="border-2 border-black">
          {/* Header */}
          <div className="p-4 border-b-2 border-black bg-[var(--color-surface)]">
            <h3 className="text-xl font-bold">{result.name}</h3>
            <p className="text-sm text-[var(--color-text-secondary)] mt-1">{result.description}</p>
          </div>

          {/* Model Rationale */}
          <div className="p-4 border-b border-[var(--color-border)]">
            <h4 className="text-sm font-semibold uppercase tracking-wider mb-2">Model Rationale</h4>
            <p className="text-sm text-[var(--color-text-secondary)] leading-relaxed">
              {result.model_rationale}
            </p>
          </div>

          {/* Composite Score */}
          <div className="p-4 border-b border-[var(--color-border)]">
            <div className="flex items-center gap-4 mb-4">
              <span className="text-xs font-semibold uppercase tracking-wider">Composite Score</span>
              <span className="font-mono text-3xl font-bold">
                {result.scores ? (result.scores.composite * 100).toFixed(0) : "N/A"}
              </span>
              <span className="text-xs font-mono text-[var(--color-text-secondary)]">/ 100</span>
            </div>

            {/* Score Bars */}
            {result.scores && (
              <div className="space-y-2">
                {SCORE_DIMENSIONS.map(({ key, label }) => {
                  const score = (result.scores as unknown as Record<string, number>)[key] ?? 0;
                  return (
                    <div key={key} className="flex items-center gap-3">
                      <span className="text-xs font-mono w-44 text-[var(--color-text-secondary)]">
                        {label}
                      </span>
                      <div className="flex-1 h-5 border border-black bg-white relative">
                        <div
                          className="h-full bg-black"
                          style={{ width: `${score * 100}%` }}
                        />
                        <span className="absolute right-1 top-0 text-[10px] font-mono leading-5 text-[var(--color-text-secondary)]">
                          {(score * 100).toFixed(0)}
                        </span>
                      </div>
                    </div>
                  );
                })}
              </div>
            )}
          </div>

          {/* Quick Navigation */}
          <div className="p-4 flex gap-3">
            <button onClick={() => onNavigate("timeline")} className="btn-secondary text-xs">
              View Timeline
            </button>
            <button onClick={() => onNavigate("budget")} className="btn-secondary text-xs">
              View Budget
            </button>
            <button onClick={() => onNavigate("risks")} className="btn-secondary text-xs">
              View Risks
            </button>
            <button onClick={() => onNavigate("blueprints")} className="btn-secondary text-xs">
              View Blueprints
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
