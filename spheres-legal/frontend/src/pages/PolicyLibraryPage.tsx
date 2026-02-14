import { useState, useEffect } from "react";
import {
  Landmark,
  ChevronDown,
  BookOpen,
  Shield,
  CheckCircle2,
  Clock,
  MessageSquare,
  DollarSign,
  Globe,
  Target,
} from "lucide-react";

interface Legislation {
  id: string;
  title: string;
  type: string;
  summary: string;
  full_text: string;
  key_provisions: string[];
  equity_requirements: string[];
  permanence_requirements: string;
  community_input_process: string;
  implementation_timeline: string;
  strategy_memo?: string;
  talking_points?: string[];
  fiscal_impact?: string;
  comparable_cities?: string[];
}

interface EquityPrinciple {
  id: string;
  name: string;
  description: string;
}

interface OwnershipPathway {
  name: string;
  description: string;
  legal_mechanism: string;
}

interface EquityFramework {
  principles: EquityPrinciple[];
  priority_scoring: {
    criteria: { name: string; weight: number; description: string }[];
  };
  anti_displacement_protections: string[];
  community_ownership_pathways: OwnershipPathway[];
}

function label(s: string) {
  return s.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());
}

export default function PolicyLibraryPage() {
  const [models, setModels] = useState<Legislation[]>([]);
  const [equity, setEquity] = useState<EquityFramework | null>(null);
  const [expanded, setExpanded] = useState<string | null>(null);
  const [tab, setTab] = useState<"legislation" | "equity">("legislation");

  useEffect(() => {
    fetch("/api/policy/models")
      .then((r) => r.json())
      .then((d) => setModels(d.models || d));
    fetch("/api/policy/equity")
      .then((r) => r.json())
      .then((d) => setEquity(d.framework || d));
  }, []);

  return (
    <div className="min-h-screen bg-void pt-20 px-6 pb-20">
      <div className="max-w-5xl mx-auto">
        {/* Header */}
        <div className="mb-12">
          <p className="section-label mb-3">POLICY LIBRARY</p>
          <h1 className="text-3xl font-light tracking-tight mb-2">
            Model Legislation & Equity Framework
          </h1>
          <p className="text-silver">
            Ready-to-introduce legislation and the equity framework that ensures
            space activation serves everyone.
          </p>
        </div>

        {/* Tabs */}
        <div className="flex gap-4 mb-8 border-b border-ash">
          {(["legislation", "equity"] as const).map((t) => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`pb-3 text-sm font-mono uppercase tracking-wider border-b-2 transition-colors ${
                tab === t
                  ? "border-legal-green text-legal-green"
                  : "border-transparent text-silver hover:text-snow"
              }`}
            >
              {t === "legislation" ? "Model Legislation" : "Equity Framework"}
            </button>
          ))}
        </div>

        {/* Legislation tab */}
        {tab === "legislation" && (
          <div className="space-y-px">
            {models.map((m) => (
              <div key={m.id} className="card bg-smoke">
                <button
                  onClick={() =>
                    setExpanded(expanded === m.id ? null : m.id)
                  }
                  className="w-full text-left flex items-start justify-between"
                >
                  <div className="flex-1">
                    <div className="flex items-center gap-3 mb-2">
                      <Landmark
                        size={18}
                        className="text-legal-green shrink-0"
                      />
                      <h3 className="font-medium">{m.title}</h3>
                    </div>
                    <div className="flex items-center gap-2 ml-8">
                      <span className="tag tag-blue">{label(m.type)}</span>
                    </div>
                  </div>
                  <ChevronDown
                    size={18}
                    className={`text-steel transition-transform mt-1 ${
                      expanded === m.id ? "rotate-180" : ""
                    }`}
                  />
                </button>

                {expanded === m.id && (
                  <div className="mt-6 pt-6 border-t border-ash">
                    <p className="text-silver text-sm mb-6">{m.summary}</p>

                    {/* Key provisions */}
                    <div className="mb-6">
                      <p className="data-label mb-3">Key Provisions</p>
                      <div className="space-y-2">
                        {m.key_provisions.map((p, i) => (
                          <div
                            key={i}
                            className="flex items-start gap-2"
                          >
                            <CheckCircle2
                              size={14}
                              className="text-legal-green mt-0.5 shrink-0"
                            />
                            <p className="text-sm text-cloud">{p}</p>
                          </div>
                        ))}
                      </div>
                    </div>

                    {/* Equity requirements */}
                    <div className="mb-6">
                      <p className="data-label mb-3">Equity Requirements</p>
                      <div className="space-y-2">
                        {m.equity_requirements.map((r, i) => (
                          <div
                            key={i}
                            className="flex items-start gap-2"
                          >
                            <Shield
                              size={14}
                              className="text-legal-blue mt-0.5 shrink-0"
                            />
                            <p className="text-sm text-cloud">{r}</p>
                          </div>
                        ))}
                      </div>
                    </div>

                    {/* Implementation */}
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
                      <div className="p-3 border border-ash">
                        <div className="flex items-center gap-2 mb-2">
                          <Clock size={14} className="text-legal-amber" />
                          <p className="data-label">Implementation Timeline</p>
                        </div>
                        <p className="text-sm text-cloud">
                          {m.implementation_timeline}
                        </p>
                      </div>
                      <div className="p-3 border border-ash">
                        <div className="flex items-center gap-2 mb-2">
                          <BookOpen size={14} className="text-legal-cyan" />
                          <p className="data-label">Community Input</p>
                        </div>
                        <p className="text-sm text-cloud">
                          {m.community_input_process}
                        </p>
                      </div>
                    </div>

                    {/* Talking points */}
                    {m.talking_points && m.talking_points.length > 0 && (
                      <div className="mb-6">
                        <div className="flex items-center gap-2 mb-3">
                          <MessageSquare size={14} className="text-legal-green" />
                          <p className="data-label">Talking Points</p>
                        </div>
                        <div className="space-y-3">
                          {m.talking_points.map((tp, i) => (
                            <div key={i} className="p-3 border-l-2 border-legal-green/30 bg-legal-green/5">
                              <p className="text-sm text-cloud leading-relaxed">{tp}</p>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* Strategy memo + Fiscal impact */}
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
                      {m.strategy_memo && (
                        <div className="p-4 border border-ash">
                          <div className="flex items-center gap-2 mb-3">
                            <Target size={14} className="text-legal-cyan" />
                            <p className="data-label">Strategy Memo</p>
                          </div>
                          <p className="text-sm text-cloud leading-relaxed">
                            {m.strategy_memo}
                          </p>
                        </div>
                      )}
                      {m.fiscal_impact && (
                        <div className="p-4 border border-ash">
                          <div className="flex items-center gap-2 mb-3">
                            <DollarSign size={14} className="text-legal-amber" />
                            <p className="data-label">Fiscal Impact</p>
                          </div>
                          <p className="text-sm text-cloud leading-relaxed">
                            {m.fiscal_impact}
                          </p>
                        </div>
                      )}
                    </div>

                    {/* Comparable cities */}
                    {m.comparable_cities && m.comparable_cities.length > 0 && (
                      <div className="mb-6">
                        <div className="flex items-center gap-2 mb-3">
                          <Globe size={14} className="text-legal-blue" />
                          <p className="data-label">Comparable Cities</p>
                        </div>
                        <div className="space-y-1.5">
                          {m.comparable_cities.map((c, i) => (
                            <div key={i} className="flex items-start gap-2 p-2 bg-ash/30">
                              <span className="text-legal-blue mt-0.5 text-xs">&#9679;</span>
                              <p className="text-sm text-cloud">{c}</p>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* Full text */}
                    <details className="group">
                      <summary className="cursor-pointer text-xs font-mono text-legal-green uppercase tracking-wider hover:underline">
                        Read Full Text
                      </summary>
                      <div className="mt-4 p-4 bg-void border border-ash text-sm text-cloud leading-relaxed whitespace-pre-line font-mono">
                        {m.full_text}
                      </div>
                    </details>
                  </div>
                )}
              </div>
            ))}
          </div>
        )}

        {/* Equity tab */}
        {tab === "equity" && equity && (
          <div>
            {/* Principles */}
            <div className="mb-12">
              <h2 className="text-sm font-mono font-bold text-legal-green tracking-wider uppercase mb-6">
                Equity Principles
              </h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-px bg-ash">
                {equity.principles.map((p) => (
                  <div key={p.id} className="card bg-void">
                    <h3 className="font-medium text-sm mb-2">{p.name}</h3>
                    <p className="text-silver text-sm">{p.description}</p>
                  </div>
                ))}
              </div>
            </div>

            {/* Priority scoring */}
            <div className="mb-12">
              <h2 className="text-sm font-mono font-bold text-legal-green tracking-wider uppercase mb-6">
                Priority Scoring Criteria
              </h2>
              <div className="space-y-3">
                {equity.priority_scoring.criteria.map((c) => (
                  <div
                    key={c.name}
                    className="card bg-smoke flex items-center gap-4"
                  >
                    <div className="w-16 shrink-0 text-center">
                      <p className="data-value text-lg">
                        {Math.round(c.weight * 100)}%
                      </p>
                    </div>
                    <div className="flex-1">
                      <p className="font-medium text-sm">{c.name}</p>
                      <p className="text-silver text-xs mt-0.5">
                        {c.description}
                      </p>
                    </div>
                    <div
                      className="h-2 bg-legal-green/20"
                      style={{ width: `${c.weight * 200}px` }}
                    >
                      <div
                        className="h-full bg-legal-green"
                        style={{ width: `${c.weight * 100}%` }}
                      />
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Anti-displacement */}
            <div className="mb-12">
              <h2 className="text-sm font-mono font-bold text-legal-red tracking-wider uppercase mb-6">
                Anti-Displacement Protections
              </h2>
              <div className="space-y-2">
                {equity.anti_displacement_protections.map((p, i) => (
                  <div
                    key={i}
                    className="flex items-start gap-2 p-3 border border-ash"
                  >
                    <Shield
                      size={14}
                      className="text-legal-red mt-0.5 shrink-0"
                    />
                    <p className="text-sm text-cloud">{p}</p>
                  </div>
                ))}
              </div>
            </div>

            {/* Community ownership */}
            <div>
              <h2 className="text-sm font-mono font-bold text-legal-blue tracking-wider uppercase mb-6">
                Community Ownership Pathways
              </h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-px bg-ash">
                {equity.community_ownership_pathways.map((p) => (
                  <div key={p.name} className="card bg-void">
                    <h3 className="font-medium text-sm mb-2">{p.name}</h3>
                    <p className="text-silver text-sm mb-3">{p.description}</p>
                    <p className="font-mono text-xs text-legal-blue">
                      {p.legal_mechanism}
                    </p>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
