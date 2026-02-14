import { useState, useEffect } from "react";
import { Globe, ArrowRight, Star, AlertTriangle, Lightbulb } from "lucide-react";

interface NotableProject {
  name: string;
  description: string;
  outcome: string;
}

interface CityAnalysis {
  name: string;
  country: string;
  population: number;
  approach_name: string;
  description: string;
  key_policies: string[];
  strengths: string[];
  weaknesses: string[];
  lessons_for_philadelphia: string[];
  activation_score: number;
  notable_projects: NotableProject[];
}

function fmtPop(n: number) {
  if (n >= 1_000_000) return `${(n / 1_000_000).toFixed(1)}M`;
  if (n >= 1_000) return `${(n / 1_000).toFixed(0)}K`;
  return n.toString();
}

function scoreColor(score: number) {
  if (score >= 75) return "text-legal-green";
  if (score >= 50) return "text-legal-amber";
  return "text-legal-red";
}

export default function ComparativePage() {
  const [cities, setCities] = useState<CityAnalysis[]>([]);
  const [selected, setSelected] = useState<CityAnalysis | null>(null);
  const [compareWith, setCompareWith] = useState<CityAnalysis | null>(null);

  useEffect(() => {
    fetch("/api/policy/comparative")
      .then((r) => r.json())
      .then((d) => {
        const list = d.cities || d;
        setCities(list);
        if (list.length > 0) setSelected(list[0]);
      });
  }, []);

  const sorted = [...cities].sort((a, b) => b.activation_score - a.activation_score);

  return (
    <div className="min-h-screen bg-void pt-20 px-6 pb-20">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="mb-12">
          <p className="section-label mb-3">COMPARATIVE ANALYSIS</p>
          <h1 className="text-3xl font-light tracking-tight mb-2">
            Global Space Activation
          </h1>
          <p className="text-silver">
            How Philadelphia compares to leading cities in public space
            activation policy.
          </p>
        </div>

        {/* Score ranking */}
        <div className="card mb-12">
          <h2 className="text-sm font-mono font-bold text-legal-green tracking-wider uppercase mb-6">
            Activation Score Ranking
          </h2>
          <div className="space-y-3">
            {sorted.map((city, i) => (
              <button
                key={city.name}
                onClick={() => {
                  setSelected(city);
                  setCompareWith(null);
                }}
                className={`w-full flex items-center gap-4 p-3 border transition-colors text-left ${
                  selected?.name === city.name
                    ? "border-legal-green bg-legal-green/5"
                    : "border-ash hover:border-steel"
                }`}
              >
                <span className="font-mono text-xs text-steel w-6">
                  {String(i + 1).padStart(2, "0")}
                </span>
                <div className="flex-1">
                  <div className="flex items-center gap-2">
                    <span className="font-medium text-sm">{city.name}</span>
                    <span className="text-xs text-silver">
                      {city.country}
                    </span>
                  </div>
                  <p className="text-xs text-silver mt-0.5">
                    {city.approach_name} · {fmtPop(city.population)}
                  </p>
                </div>
                <div className="w-32 h-2 bg-ash">
                  <div
                    className="h-full bg-legal-green transition-all"
                    style={{ width: `${city.activation_score}%` }}
                  />
                </div>
                <span
                  className={`font-mono font-bold text-lg w-12 text-right ${scoreColor(
                    city.activation_score
                  )}`}
                >
                  {city.activation_score}
                </span>
              </button>
            ))}
          </div>
        </div>

        {/* Compare selector */}
        {selected && (
          <div className="mb-4 flex items-center gap-4">
            <span className="text-xs text-silver font-mono uppercase tracking-wider">
              Compare:
            </span>
            {cities
              .filter((c) => c.name !== selected.name)
              .map((c) => (
                <button
                  key={c.name}
                  onClick={() =>
                    setCompareWith(compareWith?.name === c.name ? null : c)
                  }
                  className={`tag cursor-pointer ${
                    compareWith?.name === c.name ? "tag-green" : ""
                  }`}
                >
                  {c.name}
                </button>
              ))}
          </div>
        )}

        {/* City detail / comparison */}
        {selected && (
          <div
            className={`grid gap-8 ${
              compareWith ? "grid-cols-1 md:grid-cols-2" : "grid-cols-1"
            }`}
          >
            {[selected, compareWith].filter(Boolean).map((city) => (
              <div key={city!.name} className="card">
                <div className="flex items-center justify-between mb-4">
                  <div>
                    <h2 className="text-xl font-medium">{city!.name}</h2>
                    <p className="text-silver text-sm">
                      {city!.country} · {fmtPop(city!.population)}
                    </p>
                  </div>
                  <div
                    className={`text-3xl font-mono font-bold ${scoreColor(
                      city!.activation_score
                    )}`}
                  >
                    {city!.activation_score}
                  </div>
                </div>

                <p className="text-sm font-mono text-legal-green mb-2">
                  {city!.approach_name}
                </p>
                <p className="text-silver text-sm mb-6">{city!.description}</p>

                {/* Key policies */}
                <div className="mb-6">
                  <p className="data-label mb-2">Key Policies</p>
                  <div className="flex gap-2 flex-wrap">
                    {city!.key_policies.map((p, i) => (
                      <span key={i} className="tag">
                        {p}
                      </span>
                    ))}
                  </div>
                </div>

                {/* Strengths */}
                <div className="mb-6">
                  <p className="data-label mb-2">Strengths</p>
                  <div className="space-y-1.5">
                    {city!.strengths.map((s, i) => (
                      <div key={i} className="flex items-start gap-2">
                        <Star
                          size={12}
                          className="text-legal-green mt-0.5 shrink-0"
                        />
                        <p className="text-sm text-cloud">{s}</p>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Weaknesses */}
                <div className="mb-6">
                  <p className="data-label mb-2">Weaknesses</p>
                  <div className="space-y-1.5">
                    {city!.weaknesses.map((w, i) => (
                      <div key={i} className="flex items-start gap-2">
                        <AlertTriangle
                          size={12}
                          className="text-legal-amber mt-0.5 shrink-0"
                        />
                        <p className="text-sm text-cloud">{w}</p>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Lessons */}
                <div className="mb-6">
                  <p className="data-label mb-2">Lessons for Philadelphia</p>
                  <div className="space-y-1.5">
                    {city!.lessons_for_philadelphia.map((l, i) => (
                      <div key={i} className="flex items-start gap-2">
                        <Lightbulb
                          size={12}
                          className="text-legal-cyan mt-0.5 shrink-0"
                        />
                        <p className="text-sm text-cloud">{l}</p>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Notable projects */}
                {city!.notable_projects.length > 0 && (
                  <div>
                    <p className="data-label mb-2">Notable Projects</p>
                    <div className="space-y-2">
                      {city!.notable_projects.map((proj) => (
                        <div
                          key={proj.name}
                          className="p-3 border border-ash"
                        >
                          <p className="text-sm font-medium">{proj.name}</p>
                          <p className="text-xs text-silver mt-1">
                            {proj.description}
                          </p>
                          <p className="text-xs text-legal-green mt-1 font-mono">
                            {proj.outcome}
                          </p>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
