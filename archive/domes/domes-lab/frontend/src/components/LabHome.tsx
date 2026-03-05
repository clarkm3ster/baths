import { useState, useEffect } from 'react';
import {
  DOMAINS,
  READINESS_CONFIG,
  READINESS_ORDER,
  type DomainConfig,
  type Innovation,
  getTeammates,
  getAllInnovations,
  getReadinessBreakdown,
  type Teammate,
} from '../api/client';

interface Props {
  onSelectDomain: (slug: string) => void;
}

export default function LabHome({ onSelectDomain }: Props) {
  const [teammates, setTeammates] = useState<Teammate[]>([]);
  const [innovations, setInnovations] = useState<Innovation[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([getTeammates(), getAllInnovations()]).then(([t, i]) => {
      setTeammates(t);
      setInnovations(i);
      setLoading(false);
    });
  }, []);

  // Group innovations by domain
  const domainInnovations = (domain: DomainConfig): Innovation[] =>
    innovations.filter(i => i.domain === domain.backendDomain);

  const totalInnovations = innovations.length;
  const totalBreakdown = getReadinessBreakdown(innovations);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="font-mono text-sm text-text-muted animate-pulse">LOADING LAB DATA...</div>
      </div>
    );
  }

  return (
    <div>
      {/* Header */}
      <div className="mb-8">
        <h2 className="font-serif text-3xl tracking-wide mb-2">Innovation Laboratory</h2>
        <p className="font-mono text-xs text-text-muted tracking-wide">
          {totalInnovations} INNOVATIONS ACROSS 11 RESEARCH DOMAINS
        </p>

        {/* Global readiness summary */}
        <div className="flex gap-4 mt-4">
          {READINESS_ORDER.map(r => (
            <div key={r} className="flex items-center gap-2">
              <div className="w-2 h-2" style={{ backgroundColor: READINESS_CONFIG[r].color }} />
              <span className="font-mono text-[10px] text-text-muted">
                {READINESS_CONFIG[r].label}: {totalBreakdown[r]}
              </span>
            </div>
          ))}
        </div>
      </div>

      {/* Domain Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {DOMAINS.map(domain => {
          const innos = domainInnovations(domain);
          const breakdown = getReadinessBreakdown(innos);
          const teammate = teammates.find(t => t.slug === domain.slug);
          const count = teammate?.innovation_count ?? innos.length;

          return (
            <button
              key={domain.slug}
              onClick={() => onSelectDomain(domain.slug)}
              className="card text-left transition-all duration-200 hover:border-accent-light group relative overflow-hidden"
              style={{ borderLeftWidth: '3px', borderLeftColor: domain.color }}
            >
              {/* Glow effect */}
              <div
                className="absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-300"
                style={{
                  background: `radial-gradient(ellipse at center, ${domain.color}15 0%, transparent 70%)`,
                }}
              />

              <div className="relative z-10">
                {/* Domain icon + name */}
                <div className="flex items-center gap-3 mb-3">
                  <div
                    className="flex items-center justify-center w-10 h-10 border text-lg font-mono"
                    style={{ borderColor: domain.color, color: domain.color }}
                  >
                    {domain.icon}
                  </div>
                  <div>
                    <div className="font-serif text-base tracking-wide">{domain.label}</div>
                    <div className="font-mono text-[10px] text-text-muted tracking-wider">
                      {count} INNOVATION{count !== 1 ? 'S' : ''}
                    </div>
                  </div>
                </div>

                {/* Description */}
                <p className="text-xs text-text-muted mb-3 line-clamp-2">{domain.description}</p>

                {/* Readiness breakdown bar */}
                <div className="flex h-1.5 w-full overflow-hidden bg-bg">
                  {READINESS_ORDER.map(r => {
                    const pct = count > 0 ? (breakdown[r] / count) * 100 : 0;
                    if (pct === 0) return null;
                    return (
                      <div
                        key={r}
                        style={{
                          width: `${pct}%`,
                          backgroundColor: READINESS_CONFIG[r].color,
                        }}
                      />
                    );
                  })}
                </div>

                {/* Readiness counts */}
                <div className="flex gap-3 mt-2">
                  {READINESS_ORDER.map(r => (
                    breakdown[r] > 0 && (
                      <span
                        key={r}
                        className="font-mono text-[9px]"
                        style={{ color: READINESS_CONFIG[r].color }}
                      >
                        {READINESS_CONFIG[r].short} {breakdown[r]}
                      </span>
                    )
                  ))}
                </div>
              </div>
            </button>
          );
        })}
      </div>
    </div>
  );
}
