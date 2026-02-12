import { useState, useEffect } from 'react';
import {
  type Teammate,
  type Innovation,
  getTeammates,
  getInnovations,
  getStatusColor,
  getHorizonLabel,
  DEMO_TEAMMATES,
  DEMO_INNOVATIONS,
} from '../api/client';

export default function TeammateGrid() {
  const [teammates, setTeammates] = useState<Teammate[]>(DEMO_TEAMMATES);
  const [innovations, setInnovations] = useState<Innovation[]>(DEMO_INNOVATIONS);
  const [expandedSlug, setExpandedSlug] = useState<string | null>(null);

  useEffect(() => {
    getTeammates().then(setTeammates);
    getInnovations().then(setInnovations);
  }, []);

  const getTeammateInnovations = (slug: string) =>
    innovations.filter((i) => i.teammate_slug === slug);

  return (
    <div className="space-y-6">
      {/* ── Header ── */}
      <div>
        <h2 className="font-serif text-2xl tracking-wide">Domain Agents</h2>
        <p className="mt-1 font-mono text-xs text-text-muted tracking-wider">
          12 SPECIALIZED AI TEAMMATES // CLICK TO EXPAND
        </p>
      </div>

      {/* ── Grid ── */}
      <div className="grid grid-cols-3 gap-4">
        {teammates.map((tm) => {
          const isExpanded = expandedSlug === tm.slug;
          const tmInnovations = getTeammateInnovations(tm.slug);

          return (
            <div
              key={tm.slug}
              className={`bg-surface border border-border transition-all duration-200 ${
                isExpanded ? 'col-span-3' : ''
              }`}
              style={{ borderLeftWidth: '4px', borderLeftColor: tm.color }}
            >
              {/* Card Header (always visible) */}
              <button
                onClick={() => setExpandedSlug(isExpanded ? null : tm.slug)}
                className="w-full text-left p-4 flex items-start gap-4 hover:bg-surface-alt transition-colors"
              >
                {/* Color Avatar */}
                <div
                  className="h-10 w-10 shrink-0 flex items-center justify-center font-mono text-sm font-bold"
                  style={{ backgroundColor: tm.color + '22', color: tm.color, border: `1px solid ${tm.color}44` }}
                >
                  {tm.name.split(' ').pop()?.charAt(0) || '?'}
                </div>

                {/* Info */}
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2">
                    <h3 className="text-base font-medium">{tm.name}</h3>
                    <div
                      className="h-2 w-2 shrink-0"
                      style={{ backgroundColor: getStatusColor(tm.status) }}
                    />
                  </div>
                  <div className="font-mono text-[10px] text-text-muted tracking-wider mt-0.5">
                    {tm.title}
                  </div>
                  {!isExpanded && (
                    <div className="text-xs text-text-muted mt-1 line-clamp-2">
                      {tm.description}
                    </div>
                  )}
                </div>

                {/* Stats */}
                <div className="flex items-center gap-4 shrink-0">
                  <div className="text-center">
                    <div className="font-mono text-[9px] text-text-muted">INNOV</div>
                    <div className="font-mono text-sm" style={{ color: tm.color }}>
                      {tm.innovation_count}
                    </div>
                  </div>
                  <div className="text-center">
                    <div className="font-mono text-[9px] text-text-muted">IMP</div>
                    <div className="font-mono text-sm">{tm.avg_impact.toFixed(1)}</div>
                  </div>
                  <div className="text-center">
                    <div className="font-mono text-[9px] text-text-muted">FEA</div>
                    <div className="font-mono text-sm">{tm.avg_feasibility.toFixed(1)}</div>
                  </div>
                  <div className="text-center">
                    <div className="font-mono text-[9px] text-text-muted">NOV</div>
                    <div className="font-mono text-sm">{tm.avg_novelty.toFixed(1)}</div>
                  </div>

                  {/* Expand Indicator */}
                  <span className="font-mono text-xs text-text-muted">
                    {isExpanded ? '[-]' : '[+]'}
                  </span>
                </div>
              </button>

              {/* Expanded: Domain Description + Innovations */}
              {isExpanded && (
                <div className="border-t border-border">
                  {/* Domain Description */}
                  <div className="p-4 bg-surface-alt">
                    <div className="font-mono text-[10px] text-text-muted tracking-wider mb-1 uppercase">
                      Domain: {tm.domain}
                    </div>
                    <p className="text-sm text-text-muted leading-relaxed">
                      {tm.description}
                    </p>

                    {/* Score Bars */}
                    <div className="grid grid-cols-3 gap-4 mt-4">
                      {[
                        { label: 'Impact', value: tm.avg_impact, color: '#DC2626' },
                        { label: 'Feasibility', value: tm.avg_feasibility, color: '#C9A726' },
                        { label: 'Novelty', value: tm.avg_novelty, color: '#4169E1' },
                      ].map((score) => (
                        <div key={score.label}>
                          <div className="flex items-center justify-between mb-1">
                            <span className="font-mono text-[10px] text-text-muted">
                              {score.label.toUpperCase()}
                            </span>
                            <span className="font-mono text-xs" style={{ color: score.color }}>
                              {score.value.toFixed(1)}
                            </span>
                          </div>
                          <div className="score-bar">
                            <div
                              className="score-bar-fill"
                              style={{
                                width: `${(score.value / 5) * 100}%`,
                                backgroundColor: score.color,
                              }}
                            />
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>

                  {/* Innovations List */}
                  <div className="p-4">
                    <div className="font-mono text-[10px] text-text-muted tracking-wider mb-3 uppercase">
                      Innovations ({tmInnovations.length})
                    </div>
                    {tmInnovations.length === 0 ? (
                      <div className="text-sm text-text-muted italic">
                        No innovations recorded yet.
                      </div>
                    ) : (
                      <div className="space-y-2">
                        {tmInnovations.map((inn) => (
                          <div
                            key={inn.id}
                            className="bg-bg border border-border p-3 flex items-center gap-4"
                          >
                            <div className="flex-1 min-w-0">
                              <div className="text-sm font-medium">{inn.title}</div>
                              <div className="text-xs text-text-muted mt-0.5 line-clamp-1">
                                {inn.summary}
                              </div>
                            </div>

                            {/* Scores */}
                            <div className="flex items-center gap-3 shrink-0 font-mono text-[10px]">
                              <span style={{ color: '#DC2626' }}>I:{inn.impact_score}</span>
                              <span style={{ color: '#C9A726' }}>F:{inn.feasibility_score}</span>
                              <span style={{ color: '#4169E1' }}>N:{inn.novelty_score}</span>
                            </div>

                            {/* Tags */}
                            <div
                              className="badge shrink-0"
                              style={{
                                color: getStatusColor(inn.status),
                                borderColor: getStatusColor(inn.status),
                              }}
                            >
                              {inn.status.toUpperCase()}
                            </div>
                            <div className="badge text-text-muted border-border shrink-0">
                              {getHorizonLabel(inn.time_horizon)}
                            </div>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
