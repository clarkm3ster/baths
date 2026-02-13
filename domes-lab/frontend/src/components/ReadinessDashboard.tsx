import { useState, useEffect } from 'react';
import {
  READINESS_ORDER,
  READINESS_CONFIG,
  type Innovation,
  type Readiness,
  getAllInnovations,
  getReadiness,
  getDomainByBackend,
  getStatusColor,
} from '../api/client';

interface Props {
  onSelectDomain: (slug: string) => void;
}

export default function ReadinessDashboard({ onSelectDomain }: Props) {
  const [innovations, setInnovations] = useState<Innovation[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getAllInnovations().then(all => {
      setInnovations(all);
      setLoading(false);
    });
  }, []);

  // Group by readiness
  const columns: Record<Readiness, Innovation[]> = {
    immediate: [], '1-year': [], '5-year': [], moonshot: [],
  };
  for (const inn of innovations) {
    columns[getReadiness(inn)].push(inn);
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="font-mono text-sm text-text-muted animate-pulse">LOADING READINESS DATA...</div>
      </div>
    );
  }

  return (
    <div>
      <div className="mb-6">
        <h2 className="font-serif text-2xl tracking-wide mb-1">Readiness Dashboard</h2>
        <p className="font-mono text-xs text-text-muted tracking-wide">
          {innovations.length} INNOVATIONS SORTED BY IMPLEMENTATION TIMELINE
        </p>
      </div>

      {/* 4-column layout */}
      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-4">
        {READINESS_ORDER.map(readiness => {
          const rConfig = READINESS_CONFIG[readiness];
          const items = columns[readiness];

          return (
            <div key={readiness} className="flex flex-col">
              {/* Column header */}
              <div
                className="px-3 py-2 border-b-2 mb-3"
                style={{ borderColor: rConfig.color }}
              >
                <div className="flex items-center justify-between">
                  <span className="font-mono text-xs tracking-wider" style={{ color: rConfig.color }}>
                    {rConfig.label}
                  </span>
                  <span className="font-mono text-[10px] text-text-muted">
                    {items.length}
                  </span>
                </div>
                <div className="font-mono text-[9px] text-text-muted mt-0.5">
                  {rConfig.description}
                </div>
              </div>

              {/* Cards */}
              <div className="space-y-2 flex-1">
                {items.map(inn => {
                  const domain = getDomainByBackend(inn.domain);
                  return (
                    <button
                      key={inn.id}
                      onClick={() => domain && onSelectDomain(domain.slug)}
                      className="card w-full text-left transition-colors hover:border-accent-light"
                      style={{ borderLeftWidth: '3px', borderLeftColor: domain?.color ?? '#475569' }}
                    >
                      <div className="flex items-start justify-between gap-2 mb-1">
                        <h4 className="font-serif text-xs leading-tight flex-1">{inn.title}</h4>
                        <span
                          className="badge shrink-0"
                          style={{ borderColor: getStatusColor(inn.status), color: getStatusColor(inn.status) }}
                        >
                          {inn.status.toUpperCase()}
                        </span>
                      </div>
                      <p className="text-[10px] text-text-muted line-clamp-2 mb-2">{inn.summary}</p>
                      <div className="flex items-center gap-2">
                        {domain && (
                          <span
                            className="font-mono text-[9px]"
                            style={{ color: domain.color }}
                          >
                            {domain.label}
                          </span>
                        )}
                        <span className="font-mono text-[9px] text-text-muted ml-auto">
                          IMP {inn.impact_level} / FEA {inn.feasibility}
                        </span>
                      </div>
                    </button>
                  );
                })}

                {items.length === 0 && (
                  <div className="text-center py-8">
                    <div className="font-mono text-[10px] text-text-muted">NO INNOVATIONS</div>
                  </div>
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
