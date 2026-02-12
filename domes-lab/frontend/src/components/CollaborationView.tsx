import { useState, useEffect } from 'react';
import {
  type Collaboration,
  type Innovation,
  getCollaborations,
  getInnovations,
  getStatusColor,
  DEMO_COLLABORATIONS,
  DEMO_INNOVATIONS,
} from '../api/client';

export default function CollaborationView() {
  const [collaborations, setCollaborations] = useState<Collaboration[]>(DEMO_COLLABORATIONS);
  const [innovations, setInnovations] = useState<Innovation[]>(DEMO_INNOVATIONS);
  const [expandedId, setExpandedId] = useState<number | null>(null);
  const [statusFilter, setStatusFilter] = useState<string>('all');

  useEffect(() => {
    getCollaborations().then(setCollaborations);
    getInnovations().then(setInnovations);
  }, []);

  const filtered = statusFilter === 'all'
    ? collaborations
    : collaborations.filter((c) => c.status === statusFilter);

  const getInnovationById = (id: number) => innovations.find((i) => i.id === id);

  const statusTabs = ['all', 'proposed', 'active', 'completed'] as const;

  return (
    <div className="space-y-6">
      {/* ── Header ── */}
      <div>
        <h2 className="font-serif text-2xl tracking-wide">Cross-Domain Collaborations</h2>
        <p className="mt-1 font-mono text-xs text-text-muted tracking-wider">
          {collaborations.length} COLLABORATIONS // {collaborations.filter(c => c.status === 'active').length} ACTIVE
        </p>
      </div>

      {/* ── Status Filter ── */}
      <div className="flex items-center gap-1">
        <span className="font-mono text-[10px] text-text-muted tracking-wider mr-3">STATUS:</span>
        {statusTabs.map((s) => (
          <button
            key={s}
            onClick={() => setStatusFilter(s)}
            className={`font-mono text-[10px] tracking-wider px-3 py-1.5 border transition-colors ${
              statusFilter === s
                ? 'border-accent-glow bg-accent/30 text-text'
                : 'border-border text-text-muted hover:text-text hover:border-text-muted'
            }`}
          >
            {s === 'all' ? 'ALL' : s.toUpperCase()}
          </button>
        ))}
      </div>

      {/* ── Collaboration Cards ── */}
      {filtered.length === 0 ? (
        <div className="bg-surface border border-border p-8 text-center">
          <div className="font-mono text-sm text-text-muted">
            NO COLLABORATIONS MATCH CURRENT FILTER
          </div>
        </div>
      ) : (
        <div className="space-y-4">
          {filtered.map((collab) => {
            const isExpanded = expandedId === collab.id;

            return (
              <div key={collab.id} className="bg-surface border border-border">
                {/* Card Header */}
                <button
                  onClick={() => setExpandedId(isExpanded ? null : collab.id)}
                  className="w-full text-left p-4 hover:bg-surface-alt transition-colors"
                >
                  <div className="flex items-start justify-between">
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-3 mb-1">
                        <h3 className="text-base font-medium">{collab.title}</h3>
                        <div
                          className="badge shrink-0"
                          style={{
                            color: getStatusColor(collab.status),
                            borderColor: getStatusColor(collab.status),
                          }}
                        >
                          {collab.status.toUpperCase()}
                        </div>
                      </div>
                      <p className="text-sm text-text-muted">{collab.description}</p>
                    </div>

                    <span className="font-mono text-xs text-text-muted ml-4 shrink-0">
                      {isExpanded ? '[-]' : '[+]'}
                    </span>
                  </div>

                  {/* Participants Row */}
                  <div className="flex items-center gap-3 mt-3">
                    <span className="font-mono text-[10px] text-text-muted tracking-wider">
                      PARTICIPANTS:
                    </span>
                    <div className="flex items-center gap-2">
                      {collab.participants.map((p) => (
                        <div
                          key={p.slug}
                          className="flex items-center gap-1.5"
                        >
                          <div
                            className="h-3 w-3 shrink-0"
                            style={{ backgroundColor: p.color }}
                          />
                          <span className="font-mono text-[10px] text-text-muted">
                            {p.name}
                          </span>
                        </div>
                      ))}
                    </div>
                    <span className="font-mono text-[10px] text-text-muted ml-auto">
                      {new Date(collab.created_at).toLocaleDateString('en-US', {
                        month: 'short', day: 'numeric', year: 'numeric',
                      })}
                    </span>
                  </div>
                </button>

                {/* Expanded: Connected Innovations */}
                {isExpanded && (
                  <div className="border-t border-border p-4 bg-surface-alt">
                    <div className="font-mono text-[10px] text-text-muted tracking-wider mb-3 uppercase">
                      Connected Innovations ({collab.innovation_ids.length})
                    </div>
                    {collab.innovation_ids.length === 0 ? (
                      <div className="text-sm text-text-muted italic">
                        No innovations connected yet.
                      </div>
                    ) : (
                      <div className="space-y-2">
                        {collab.innovation_ids.map((innId) => {
                          const inn = getInnovationById(innId);
                          if (!inn) return null;
                          return (
                            <div
                              key={innId}
                              className="bg-bg border border-border p-3 flex items-center gap-4"
                            >
                              <div className="flex-1 min-w-0">
                                <div className="text-sm font-medium">{inn.title}</div>
                                <div className="text-xs text-text-muted mt-0.5 line-clamp-1">
                                  {inn.summary}
                                </div>
                              </div>
                              <div className="flex items-center gap-3 shrink-0 font-mono text-[10px]">
                                <span style={{ color: '#DC2626' }}>I:{inn.impact_score}</span>
                                <span style={{ color: '#C9A726' }}>F:{inn.feasibility_score}</span>
                                <span style={{ color: '#4169E1' }}>N:{inn.novelty_score}</span>
                              </div>
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
                    )}

                    {/* Collaboration Network Visualization (simple) */}
                    <div className="mt-4 p-4 bg-bg border border-border">
                      <div className="font-mono text-[10px] text-text-muted tracking-wider mb-3">
                        COLLABORATION NETWORK
                      </div>
                      <div className="flex items-center justify-center gap-2 py-4">
                        {collab.participants.map((p, i) => (
                          <div key={p.slug} className="flex items-center gap-2">
                            <div className="flex flex-col items-center">
                              <div
                                className="h-8 w-8 flex items-center justify-center font-mono text-[10px] font-bold"
                                style={{
                                  backgroundColor: p.color + '22',
                                  color: p.color,
                                  border: `1px solid ${p.color}`,
                                }}
                              >
                                {p.name.split(' ').pop()?.charAt(0)}
                              </div>
                              <span className="font-mono text-[8px] text-text-muted mt-1 max-w-16 truncate text-center">
                                {p.name.split(' ').pop()}
                              </span>
                            </div>
                            {i < collab.participants.length - 1 && (
                              <div className="flex items-center gap-1 text-text-muted">
                                <div className="w-8 h-px bg-border" />
                                <span className="font-mono text-[8px]">&lt;&gt;</span>
                                <div className="w-8 h-px bg-border" />
                              </div>
                            )}
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                )}
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
