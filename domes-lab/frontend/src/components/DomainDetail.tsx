import { useState, useEffect } from 'react';
import {
  getDomain,
  getTeammate,
  getAllInnovations,
  getReadiness,
  getStatusColor,
  READINESS_CONFIG,
  type DomainConfig,
  type Innovation,
  type Teammate,
} from '../api/client';

interface Props {
  slug: string;
  onBack: () => void;
}

export default function DomainDetail({ slug, onBack }: Props) {
  const [domain] = useState<DomainConfig | undefined>(() => getDomain(slug));
  const [teammate, setTeammate] = useState<(Teammate & { innovations: Innovation[] }) | null>(null);
  const [innovations, setInnovations] = useState<Innovation[]>([]);
  const [expanded, setExpanded] = useState<Set<number>>(new Set());
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    (async () => {
      const t = await getTeammate(slug);
      if (t) {
        setTeammate(t);
        setInnovations(t.innovations ?? []);
      } else {
        // Fallback: get all innovations and filter
        const all = await getAllInnovations();
        setInnovations(all.filter(i => i.domain === domain?.backendDomain));
      }
      setLoading(false);
    })();
  }, [slug, domain]);

  const toggle = (id: number) => {
    setExpanded(prev => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return next;
    });
  };

  if (!domain) {
    return <div className="font-mono text-text-muted">Domain not found.</div>;
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="font-mono text-sm text-text-muted animate-pulse">LOADING DOMAIN DATA...</div>
      </div>
    );
  }

  return (
    <div>
      {/* Back + Header */}
      <button
        onClick={onBack}
        className="btn-ghost mb-4 text-xs"
      >
        &larr; BACK TO LAB
      </button>

      <div className="flex items-center gap-4 mb-2">
        <div
          className="flex items-center justify-center w-12 h-12 border text-xl font-mono"
          style={{ borderColor: domain.color, color: domain.color }}
        >
          {domain.icon}
        </div>
        <div>
          <h2 className="font-serif text-2xl tracking-wide">{domain.label}</h2>
          <p className="font-mono text-xs text-text-muted tracking-wide">{domain.description}</p>
        </div>
      </div>

      {teammate && (
        <div className="card-alt mt-4 mb-6">
          <div className="flex items-center gap-2 mb-1">
            <span className="font-mono text-xs" style={{ color: domain.color }}>
              {teammate.icon_symbol}
            </span>
            <span className="font-serif text-sm">{teammate.name}</span>
            <span className="font-mono text-[10px] text-text-muted">// {teammate.title}</span>
          </div>
          <p className="text-xs text-text-muted">{teammate.description}</p>
        </div>
      )}

      <div className="font-mono text-xs text-text-muted mb-4 tracking-wider">
        {innovations.length} INNOVATION{innovations.length !== 1 ? 'S' : ''} IN THIS DOMAIN
      </div>

      {/* Innovation Cards */}
      <div className="space-y-3">
        {innovations.map(inn => {
          const isExpanded = expanded.has(inn.id);
          const readiness = getReadiness(inn);
          const rConfig = READINESS_CONFIG[readiness];

          return (
            <div
              key={inn.id}
              className="card transition-all duration-200"
              style={{ borderLeftWidth: '3px', borderLeftColor: domain.color }}
            >
              {/* Header — always visible */}
              <button
                onClick={() => toggle(inn.id)}
                className="w-full text-left"
              >
                <div className="flex items-start justify-between gap-4">
                  <div className="flex-1 min-w-0">
                    <h3 className="font-serif text-base mb-1">{inn.title}</h3>
                    <p className="text-xs text-text-muted">{inn.summary}</p>
                  </div>
                  <div className="flex flex-col items-end gap-1 shrink-0">
                    {/* Readiness badge */}
                    <span
                      className="badge"
                      style={{ borderColor: rConfig.color, color: rConfig.color }}
                    >
                      {rConfig.label}
                    </span>
                    {/* Status badge */}
                    <span
                      className="badge"
                      style={{ borderColor: getStatusColor(inn.status), color: getStatusColor(inn.status) }}
                    >
                      {inn.status.toUpperCase()}
                    </span>
                  </div>
                </div>

                {/* Scores bar */}
                <div className="flex items-center gap-4 mt-2">
                  <ScoreBar label="IMPACT" value={inn.impact_level} color="#3B7DD8" />
                  <ScoreBar label="FEASIBILITY" value={inn.feasibility} color="#059669" />
                  <ScoreBar label="NOVELTY" value={inn.novelty} color="#9333EA" />
                  <span className="font-mono text-[10px] text-text-muted ml-auto">
                    {isExpanded ? '[ COLLAPSE ]' : '[ EXPAND ]'}
                  </span>
                </div>
              </button>

              {/* Expanded content */}
              {isExpanded && (
                <div className="mt-4 pt-4 border-t border-border">
                  {/* Tags */}
                  {inn.tags.length > 0 && (
                    <div className="flex flex-wrap gap-1 mb-4">
                      {inn.tags.map(tag => (
                        <span key={tag} className="badge border-border text-text-muted">
                          {tag}
                        </span>
                      ))}
                    </div>
                  )}

                  {/* Details */}
                  {inn.details && typeof inn.details === 'object' && Object.keys(inn.details).length > 0 && (
                    <div className="space-y-3">
                      {Object.entries(inn.details).map(([key, value]) => (
                        <DetailBlock key={key} label={key} value={value} domainColor={domain.color} />
                      ))}
                    </div>
                  )}
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}

function ScoreBar({ label, value, color }: { label: string; value: number; color: string }) {
  return (
    <div className="flex items-center gap-1.5">
      <span className="font-mono text-[9px] text-text-muted w-16 text-right">{label}</span>
      <div className="w-16 h-1 bg-bg">
        <div className="h-full" style={{ width: `${(value / 5) * 100}%`, backgroundColor: color }} />
      </div>
      <span className="font-mono text-[10px] w-3" style={{ color }}>{value}</span>
    </div>
  );
}

function DetailBlock({ label, value, domainColor }: { label: string; value: unknown; domainColor: string }) {
  const displayLabel = label.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase());

  if (Array.isArray(value)) {
    return (
      <div>
        <div className="font-mono text-[10px] tracking-wider mb-1" style={{ color: domainColor }}>
          {displayLabel.toUpperCase()}
        </div>
        <ul className="space-y-0.5">
          {value.map((item, i) => (
            <li key={i} className="text-xs text-text-muted flex items-start gap-2">
              <span className="text-text-muted shrink-0 mt-0.5">-</span>
              <span>{typeof item === 'object' ? JSON.stringify(item) : String(item)}</span>
            </li>
          ))}
        </ul>
      </div>
    );
  }

  if (typeof value === 'object' && value !== null) {
    return (
      <div>
        <div className="font-mono text-[10px] tracking-wider mb-1" style={{ color: domainColor }}>
          {displayLabel.toUpperCase()}
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-x-6 gap-y-1">
          {Object.entries(value as Record<string, unknown>).map(([k, v]) => {
            const subLabel = k.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
            const display = typeof v === 'object' && v !== null
              ? (Array.isArray(v)
                ? v.map(String).join(', ')
                : Object.entries(v as Record<string, unknown>).map(([sk, sv]) => `${sk.replace(/_/g, ' ')}: ${sv}`).join('; '))
              : String(v);
            return (
              <div key={k} className="text-xs">
                <span className="text-text-muted">{subLabel}: </span>
                <span className="text-text">{display}</span>
              </div>
            );
          })}
        </div>
      </div>
    );
  }

  return (
    <div className="text-xs">
      <span className="font-mono text-[10px] tracking-wider" style={{ color: domainColor }}>
        {displayLabel.toUpperCase()}:
      </span>{' '}
      <span className="text-text">{String(value)}</span>
    </div>
  );
}
