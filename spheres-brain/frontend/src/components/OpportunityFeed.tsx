// -----------------------------------------------------------------
// OpportunityFeed -- Scored opportunities ranked by potential
// -----------------------------------------------------------------

import { useState } from 'react';
import { MapPin, TrendingUp, ChevronDown, ChevronUp, Zap } from 'lucide-react';
import type { Opportunity } from '../utils/api';

interface Props {
  opportunities: Opportunity[];
  loading: boolean;
}

const SCORE_LABELS: { key: keyof Opportunity['scores']; label: string }[] = [
  { key: 'location', label: 'Location' },
  { key: 'permit_readiness', label: 'Permits' },
  { key: 'community', label: 'Community' },
  { key: 'seasonal_fit', label: 'Seasonal' },
  { key: 'cost_efficiency', label: 'Cost Eff.' },
];

const PLACEHOLDER_OPPORTUNITIES: Opportunity[] = [];

function scoreColor(score: number): string {
  if (score >= 90) return 'var(--green)';
  if (score >= 75) return 'var(--accent)';
  if (score >= 60) return 'var(--yellow)';
  return 'var(--red)';
}

function ScoreBar({ score }: { score: number }) {
  return (
    <div
      style={{
        width: '100%',
        height: 3,
        background: 'var(--border)',
        borderRadius: 2,
        overflow: 'hidden',
      }}
    >
      <div
        style={{
          width: `${score}%`,
          height: '100%',
          background: scoreColor(score),
          borderRadius: 2,
          transition: 'width 0.4s ease',
        }}
      />
    </div>
  );
}

export default function OpportunityFeed({ opportunities, loading }: Props) {
  const [expandedId, setExpandedId] = useState<string | null>(null);
  const data = opportunities.length > 0 ? opportunities : PLACEHOLDER_OPPORTUNITIES;

  return (
    <div
      style={{
        background: 'var(--bg-card)',
        border: '1px solid var(--border)',
        borderRadius: 8,
        overflow: 'hidden',
        display: 'flex',
        flexDirection: 'column',
      }}
    >
      {/* Header */}
      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          padding: '10px 14px',
          borderBottom: '1px solid var(--border)',
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
          <Zap size={12} style={{ color: 'var(--accent)' }} />
          <span
            style={{
              fontSize: 11,
              fontWeight: 600,
              textTransform: 'uppercase',
              letterSpacing: '0.06em',
              color: 'var(--text-secondary)',
            }}
          >
            Top Opportunities
          </span>
        </div>
        <span
          style={{
            fontFamily: 'var(--mono)',
            fontSize: 10,
            color: 'var(--text-tertiary)',
          }}
        >
          {data.length} scored
        </span>
      </div>

      {/* List */}
      <div
        style={{
          flex: 1,
          overflowY: 'auto',
          opacity: loading ? 0.4 : 1,
          transition: 'opacity 0.3s ease',
        }}
      >
        {data.map((opp, idx) => {
          const expanded = expandedId === opp.id;
          return (
            <div
              key={opp.id}
              style={{
                borderBottom: idx < data.length - 1 ? '1px solid var(--border)' : 'none',
              }}
            >
              {/* Row */}
              <button
                onClick={() => setExpandedId(expanded ? null : opp.id)}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: 10,
                  width: '100%',
                  padding: '10px 14px',
                  background: 'transparent',
                  border: 'none',
                  color: 'var(--text)',
                  cursor: 'pointer',
                  textAlign: 'left',
                  transition: 'background 0.15s ease',
                }}
                onMouseEnter={(e) => {
                  (e.currentTarget as HTMLElement).style.background = 'var(--bg-hover)';
                }}
                onMouseLeave={(e) => {
                  (e.currentTarget as HTMLElement).style.background = 'transparent';
                }}
              >
                {/* Rank */}
                <span
                  style={{
                    fontFamily: 'var(--mono)',
                    fontSize: 10,
                    color: 'var(--text-tertiary)',
                    minWidth: 18,
                  }}
                >
                  {String(idx + 1).padStart(2, '0')}
                </span>

                {/* Score circle */}
                <div
                  style={{
                    width: 32,
                    height: 32,
                    borderRadius: '50%',
                    border: `2px solid ${scoreColor(opp.overall_score)}`,
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    fontFamily: 'var(--mono)',
                    fontSize: 11,
                    fontWeight: 700,
                    color: scoreColor(opp.overall_score),
                    flexShrink: 0,
                  }}
                >
                  {opp.overall_score}
                </div>

                {/* Info */}
                <div style={{ flex: 1, minWidth: 0 }}>
                  <div
                    style={{
                      fontSize: 12,
                      fontWeight: 600,
                      whiteSpace: 'nowrap',
                      overflow: 'hidden',
                      textOverflow: 'ellipsis',
                    }}
                  >
                    {opp.address}
                  </div>
                  <div
                    style={{
                      fontSize: 10,
                      color: 'var(--text-tertiary)',
                      display: 'flex',
                      gap: 8,
                      marginTop: 2,
                      alignItems: 'center',
                    }}
                  >
                    <span>{opp.recommended_type}</span>
                    <span style={{ fontFamily: 'var(--mono)' }}>
                      ${opp.estimated_cost.toLocaleString()}
                    </span>
                    {opp.neighborhood && (
                      <span style={{ opacity: 0.7 }}>{opp.neighborhood}</span>
                    )}
                    {opp.permit_window_open && (
                      <span style={{
                        background: 'rgba(0,204,102,0.15)',
                        color: 'var(--green)',
                        padding: '1px 4px',
                        borderRadius: 2,
                        fontSize: 8,
                        fontWeight: 600,
                        letterSpacing: '0.04em',
                      }}>
                        PERMITS OPEN
                      </span>
                    )}
                  </div>
                </div>

                {/* Expand arrow */}
                {expanded ? (
                  <ChevronUp size={12} style={{ color: 'var(--text-tertiary)', flexShrink: 0 }} />
                ) : (
                  <ChevronDown size={12} style={{ color: 'var(--text-tertiary)', flexShrink: 0 }} />
                )}
              </button>

              {/* Expanded detail */}
              {expanded && (
                <div
                  style={{
                    padding: '0 14px 12px 56px',
                  }}
                >
                  <div
                    style={{
                      display: 'grid',
                      gridTemplateColumns: 'repeat(5, 1fr)',
                      gap: 8,
                    }}
                  >
                    {SCORE_LABELS.map((s) => (
                      <div key={s.key}>
                        <div
                          style={{
                            fontSize: 9,
                            color: 'var(--text-tertiary)',
                            textTransform: 'uppercase',
                            letterSpacing: '0.06em',
                            marginBottom: 4,
                          }}
                        >
                          {s.label}
                        </div>
                        <div
                          style={{
                            fontFamily: 'var(--mono)',
                            fontSize: 13,
                            fontWeight: 600,
                            color: scoreColor(opp.scores[s.key]),
                            marginBottom: 4,
                          }}
                        >
                          {opp.scores[s.key]}
                        </div>
                        <ScoreBar score={opp.scores[s.key]} />
                      </div>
                    ))}
                  </div>
                  {/* Factor descriptions */}
                  {opp.factors && opp.factors.length > 0 && (
                    <div style={{ marginTop: 8 }}>
                      {opp.factors.slice(0, 2).map((f, fi) => (
                        <div key={fi} style={{ fontSize: 10, color: 'var(--text-secondary)', lineHeight: 1.4, marginBottom: 2 }}>
                          {f.description}
                        </div>
                      ))}
                    </div>
                  )}
                  <div
                    style={{
                      marginTop: 8,
                      display: 'flex',
                      alignItems: 'center',
                      gap: 4,
                      fontSize: 10,
                      color: 'var(--text-tertiary)',
                    }}
                  >
                    <MapPin size={10} />
                    <span style={{ fontFamily: 'var(--mono)' }}>
                      {opp.lat.toFixed(4)}, {opp.lng.toFixed(4)}
                    </span>
                    <TrendingUp size={10} style={{ marginLeft: 8 }} />
                    <span>{opp.recommended_type}</span>
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
