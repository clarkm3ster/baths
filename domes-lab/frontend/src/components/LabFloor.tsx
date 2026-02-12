import { useState, useEffect } from 'react';
import {
  type Teammate,
  type Innovation,
  type StatsResponse,
  getTeammates,
  getInnovations,
  getStats,
  generateInnovation,
  getStatusColor,
  getHorizonLabel,
  DEMO_TEAMMATES,
  DEMO_INNOVATIONS,
  DEMO_STATS,
} from '../api/client';

type View = 'lab-floor' | 'teammates' | 'innovations' | 'collaborations' | 'sessions' | 'stats';

interface LabFloorProps {
  onNavigate: (view: View) => void;
}

export default function LabFloor({ onNavigate }: LabFloorProps) {
  const [teammates, setTeammates] = useState<Teammate[]>(DEMO_TEAMMATES);
  const [innovations, setInnovations] = useState<Innovation[]>(DEMO_INNOVATIONS);
  const [stats, setStats] = useState<StatsResponse>(DEMO_STATS);
  const [generating, setGenerating] = useState<string | null>(null);
  const [generatedInnovation, setGeneratedInnovation] = useState<Innovation | null>(null);

  useEffect(() => {
    getTeammates().then(setTeammates);
    getInnovations({ sort: 'newest' }).then(setInnovations);
    getStats().then(setStats);
  }, []);

  const handleGenerate = async (slug: string) => {
    setGenerating(slug);
    setGeneratedInnovation(null);
    try {
      const innovation = await generateInnovation(slug);
      setGeneratedInnovation(innovation);
      // Refresh innovations list
      const updated = await getInnovations({ sort: 'newest' });
      setInnovations(updated);
    } catch {
      // Demo fallback already handled in client
    } finally {
      setGenerating(null);
    }
  };

  const recentInnovations = innovations.slice(0, 10);

  return (
    <div className="space-y-6">
      {/* ── Section Header ── */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="font-serif text-2xl tracking-wide">Lab Floor</h2>
          <p className="mt-1 font-mono text-xs text-text-muted tracking-wider">
            DOMES INNOVATION LABORATORY // OPERATIONAL DASHBOARD
          </p>
        </div>
        <div className="font-mono text-[10px] text-text-muted tracking-wider">
          {teammates.length} AGENTS ACTIVE // {innovations.length} INNOVATIONS LOGGED
        </div>
      </div>

      {/* ── Stats Row ── */}
      <div className="grid grid-cols-6 gap-3">
        {[
          { label: 'Innovations', value: stats.total_innovations, color: '#4169E1' },
          { label: 'Active Agents', value: stats.total_teammates, color: '#059669' },
          { label: 'Avg Impact', value: stats.avg_impact.toFixed(1), color: '#DC2626' },
          { label: 'Avg Feasibility', value: stats.avg_feasibility.toFixed(1), color: '#C9A726' },
          { label: 'Collaborations', value: stats.total_collaborations, color: '#9333EA' },
          { label: 'Sessions', value: stats.total_sessions, color: '#0891B2' },
        ].map((stat) => (
          <div key={stat.label} className="bg-surface border border-border p-4">
            <div className="font-mono text-[10px] text-text-muted tracking-wider uppercase mb-2">
              {stat.label}
            </div>
            <div className="flex items-end gap-2">
              <span className="font-serif text-3xl leading-none" style={{ color: stat.color }}>
                {stat.value}
              </span>
            </div>
            <div className="mt-2 h-0.5 w-full bg-bg">
              <div className="h-full" style={{ width: '100%', backgroundColor: stat.color, opacity: 0.3 }} />
            </div>
          </div>
        ))}
      </div>

      {/* ── Generated Innovation Alert ── */}
      {generatedInnovation && (
        <div className="bg-accent/20 border border-accent-glow p-4">
          <div className="flex items-start justify-between">
            <div>
              <div className="font-mono text-[10px] text-accent-glow tracking-wider mb-1">
                NEW INNOVATION GENERATED
              </div>
              <h3 className="font-serif text-lg">{generatedInnovation.title}</h3>
              <p className="mt-1 text-sm text-text-muted">{generatedInnovation.summary}</p>
              <div className="mt-2 flex items-center gap-3 font-mono text-[10px]">
                <span style={{ color: getStatusColor(generatedInnovation.status) }}>
                  {generatedInnovation.status.toUpperCase()}
                </span>
                <span className="text-text-muted">|</span>
                <span className="text-text-muted">IMPACT: {generatedInnovation.impact_score}</span>
                <span className="text-text-muted">|</span>
                <span className="text-text-muted">FEASIBILITY: {generatedInnovation.feasibility_score}</span>
                <span className="text-text-muted">|</span>
                <span className="text-text-muted">NOVELTY: {generatedInnovation.novelty_score}</span>
              </div>
            </div>
            <button
              onClick={() => setGeneratedInnovation(null)}
              className="font-mono text-xs text-text-muted hover:text-text"
            >
              [X]
            </button>
          </div>
        </div>
      )}

      {/* ── Teammate Grid (3x4) ── */}
      <div>
        <div className="flex items-center justify-between mb-3">
          <h3 className="font-mono text-xs tracking-widest text-text-muted uppercase">
            Domain Agents
          </h3>
          <button
            onClick={() => onNavigate('teammates')}
            className="btn-ghost text-[10px]"
          >
            VIEW ALL
          </button>
        </div>

        <div className="grid grid-cols-4 gap-3">
          {teammates.map((tm) => (
            <div
              key={tm.slug}
              className="bg-surface border border-border p-3 flex flex-col"
              style={{ borderLeftWidth: '3px', borderLeftColor: tm.color }}
            >
              {/* Header */}
              <div className="flex items-start justify-between mb-2">
                <div className="min-w-0 flex-1">
                  <div className="text-sm font-medium truncate">{tm.name}</div>
                  <div className="font-mono text-[10px] text-text-muted truncate mt-0.5">
                    {tm.title}
                  </div>
                </div>
                <div className="flex items-center gap-1 shrink-0 ml-2">
                  <div
                    className="h-2 w-2"
                    style={{ backgroundColor: getStatusColor(tm.status) }}
                  />
                </div>
              </div>

              {/* Innovation Count */}
              <div className="mt-auto pt-2 flex items-center justify-between">
                <div className="font-mono text-[10px] text-text-muted">
                  <span style={{ color: tm.color }}>{tm.innovation_count}</span> innovations
                </div>
                <button
                  onClick={() => handleGenerate(tm.slug)}
                  disabled={generating === tm.slug}
                  className="btn-primary text-[9px] py-1 px-2 disabled:opacity-50"
                >
                  {generating === tm.slug ? 'GEN...' : 'GENERATE'}
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* ── Recent Innovations ── */}
      <div>
        <div className="flex items-center justify-between mb-3">
          <h3 className="font-mono text-xs tracking-widest text-text-muted uppercase">
            Recent Innovations
          </h3>
          <button
            onClick={() => onNavigate('innovations')}
            className="btn-ghost text-[10px]"
          >
            BROWSE ALL
          </button>
        </div>

        <div className="space-y-2">
          {recentInnovations.map((inn) => {
            const teammate = teammates.find(t => t.slug === inn.teammate_slug);
            return (
              <div
                key={inn.id}
                className="bg-surface border border-border p-3 flex items-center gap-4"
              >
                {/* Domain Color Indicator */}
                <div
                  className="h-8 w-1 shrink-0"
                  style={{ backgroundColor: teammate?.color || '#475569' }}
                />

                {/* Title & Summary */}
                <div className="flex-1 min-w-0">
                  <div className="text-sm font-medium truncate">{inn.title}</div>
                  <div className="text-xs text-text-muted truncate mt-0.5">{inn.summary}</div>
                </div>

                {/* Scores */}
                <div className="flex items-center gap-4 shrink-0">
                  <div className="text-center">
                    <div className="font-mono text-[9px] text-text-muted">IMP</div>
                    <div className="font-mono text-xs" style={{ color: '#DC2626' }}>
                      {inn.impact_score}
                    </div>
                  </div>
                  <div className="text-center">
                    <div className="font-mono text-[9px] text-text-muted">FEA</div>
                    <div className="font-mono text-xs" style={{ color: '#C9A726' }}>
                      {inn.feasibility_score}
                    </div>
                  </div>
                  <div className="text-center">
                    <div className="font-mono text-[9px] text-text-muted">NOV</div>
                    <div className="font-mono text-xs" style={{ color: '#4169E1' }}>
                      {inn.novelty_score}
                    </div>
                  </div>
                </div>

                {/* Horizon */}
                <div
                  className="badge text-text-muted border-border shrink-0"
                >
                  {getHorizonLabel(inn.time_horizon)}
                </div>

                {/* Status */}
                <div
                  className="badge shrink-0"
                  style={{
                    color: getStatusColor(inn.status),
                    borderColor: getStatusColor(inn.status),
                  }}
                >
                  {inn.status.toUpperCase()}
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
