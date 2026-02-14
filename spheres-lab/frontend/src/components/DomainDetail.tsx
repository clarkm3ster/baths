import { useState, useEffect } from 'react';
import { ArrowLeft, ChevronDown, ChevronUp } from 'lucide-react';
import {
  getTeammate,
  getInnovationsByDomain,
  getDomainConfig,
  getReadiness,
  getReadinessConfig,
  getStatusColor,
  DEMO_TEAMMATES,
  DEMO_INNOVATIONS,
  type Teammate,
  type Innovation,
} from '../api/client';

interface DomainDetailProps {
  slug: string;
  onBack: () => void;
  onNavigate: (view: string) => void;
}

export default function DomainDetail({
  slug,
  onBack,
}: DomainDetailProps) {
  const [teammate, setTeammate] = useState<Teammate | null>(null);
  const [innovations, setInnovations] = useState<Innovation[]>([]);
  const [loading, setLoading] = useState(true);
  const [expandedCard, setExpandedCard] = useState<number | null>(null);

  const domainConfig = getDomainConfig(slug);

  useEffect(() => {
    let cancelled = false;
    async function load() {
      setLoading(true);
      const [tm, inns] = await Promise.all([
        getTeammate(slug),
        getInnovationsByDomain(slug),
      ]);
      if (!cancelled) {
        if (tm) {
          setTeammate(tm);
          // Use innovations from teammate if available, else from innovations endpoint
          setInnovations(tm.innovations ?? inns);
        } else {
          // Fallback to demo
          const demo = DEMO_TEAMMATES.find((t) => t.slug === slug);
          setTeammate(demo ?? null);
          setInnovations(
            DEMO_INNOVATIONS.filter((i) => i.domain === slug)
          );
        }
        setLoading(false);
      }
    }
    load();
    return () => {
      cancelled = true;
    };
  }, [slug]);

  const color = domainConfig?.color ?? '#0066FF';

  if (loading) {
    return (
      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          height: '100%',
          color: 'rgba(255,255,255,0.4)',
          fontFamily: "'JetBrains Mono', monospace",
          fontSize: 13,
        }}
      >
        Loading domain data...
      </div>
    );
  }

  return (
    <div style={{ padding: 24, maxWidth: 960 }}>
      {/* Back Button */}
      <button
        onClick={onBack}
        style={{
          display: 'flex',
          alignItems: 'center',
          gap: 6,
          background: 'none',
          border: '1px solid #1A1A1A',
          borderRadius: 8,
          padding: '6px 14px',
          cursor: 'pointer',
          color: 'rgba(255,255,255,0.5)',
          fontSize: 12,
          marginBottom: 20,
          transition: 'border-color 0.15s, color 0.15s',
        }}
        onMouseEnter={(e) => {
          e.currentTarget.style.borderColor = '#2A2A2A';
          e.currentTarget.style.color = '#FFFFFF';
        }}
        onMouseLeave={(e) => {
          e.currentTarget.style.borderColor = '#1A1A1A';
          e.currentTarget.style.color = 'rgba(255,255,255,0.5)';
        }}
      >
        <ArrowLeft size={14} />
        Back to Lab
      </button>

      {/* Teammate Header */}
      <div
        style={{
          background: '#0A0A0A',
          border: '1px solid #1A1A1A',
          borderRadius: 12,
          padding: 24,
          marginBottom: 20,
          display: 'flex',
          alignItems: 'center',
          gap: 20,
        }}
      >
        <div
          style={{
            width: 56,
            height: 56,
            borderRadius: 14,
            background: color + '18',
            border: `1px solid ${color}30`,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            fontSize: 28,
            color,
            flexShrink: 0,
          }}
        >
          {domainConfig?.icon ?? '?'}
        </div>
        <div style={{ flex: 1 }}>
          <h1
            style={{
              fontSize: 20,
              fontWeight: 700,
              color: '#FFFFFF',
              margin: 0,
            }}
          >
            {teammate?.name ?? domainConfig?.label ?? slug}
          </h1>
          <div
            style={{
              fontSize: 13,
              color,
              fontWeight: 500,
              marginTop: 2,
            }}
          >
            {teammate?.title ?? 'Domain Specialist'}
          </div>
          <p
            style={{
              fontSize: 12,
              color: 'rgba(255,255,255,0.45)',
              marginTop: 6,
              margin: '6px 0 0',
              lineHeight: 1.5,
            }}
          >
            {teammate?.description ?? domainConfig?.description ?? ''}
          </p>
        </div>
        <div
          style={{
            textAlign: 'right',
            flexShrink: 0,
          }}
        >
          <div
            style={{
              fontSize: 28,
              fontWeight: 700,
              color,
              fontFamily: "'JetBrains Mono', monospace",
            }}
          >
            {innovations.length}
          </div>
          <div
            style={{
              fontSize: 10,
              color: 'rgba(255,255,255,0.4)',
              letterSpacing: '0.06em',
              textTransform: 'uppercase' as const,
            }}
          >
            INNOVATIONS
          </div>
        </div>
      </div>

      {/* Innovation List */}
      <div
        style={{
          fontSize: 12,
          fontWeight: 600,
          color: 'rgba(255,255,255,0.4)',
          letterSpacing: '0.06em',
          textTransform: 'uppercase' as const,
          marginBottom: 12,
        }}
      >
        ALL INNOVATIONS
      </div>

      {innovations.length === 0 ? (
        <div
          style={{
            background: '#0A0A0A',
            border: '1px solid #1A1A1A',
            borderRadius: 10,
            padding: '40px 20px',
            textAlign: 'center',
            color: 'rgba(255,255,255,0.3)',
            fontSize: 13,
          }}
        >
          No innovations generated yet for this domain.
        </div>
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
          {innovations.map((inn) => (
            <InnovationCard
              key={inn.id}
              innovation={inn}
              color={color}
              expanded={expandedCard === inn.id}
              onToggle={() =>
                setExpandedCard(expandedCard === inn.id ? null : inn.id)
              }
            />
          ))}
        </div>
      )}
    </div>
  );
}

// ── Innovation Card ──────────────────────────────────────────

function InnovationCard({
  innovation,
  color,
  expanded,
  onToggle,
}: {
  innovation: Innovation;
  color: string;
  expanded: boolean;
  onToggle: () => void;
}) {
  const readiness = getReadiness(innovation);
  const readinessConfig = getReadinessConfig(readiness);
  const statusColor = getStatusColor(innovation.status);

  return (
    <div
      style={{
        background: '#0A0A0A',
        border: `1px solid ${expanded ? '#2A2A2A' : '#1A1A1A'}`,
        borderRadius: 10,
        overflow: 'hidden',
        transition: 'border-color 0.15s',
      }}
    >
      {/* Card Header (always visible) */}
      <button
        onClick={onToggle}
        style={{
          width: '100%',
          background: 'none',
          border: 'none',
          padding: 16,
          cursor: 'pointer',
          display: 'flex',
          flexDirection: 'column',
          gap: 10,
          textAlign: 'left',
          color: '#FFFFFF',
        }}
      >
        {/* Top row */}
        <div
          style={{
            display: 'flex',
            alignItems: 'flex-start',
            justifyContent: 'space-between',
            width: '100%',
          }}
        >
          <div style={{ flex: 1, paddingRight: 12 }}>
            <div
              style={{
                fontSize: 14,
                fontWeight: 600,
                color: '#FFFFFF',
                marginBottom: 4,
              }}
            >
              {innovation.title}
            </div>
            <div
              style={{
                fontSize: 12,
                color: 'rgba(255,255,255,0.45)',
                lineHeight: 1.5,
              }}
            >
              {innovation.summary}
            </div>
          </div>
          <div
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: 6,
              flexShrink: 0,
            }}
          >
            {expanded ? (
              <ChevronUp size={16} style={{ color: 'rgba(255,255,255,0.3)' }} />
            ) : (
              <ChevronDown
                size={16}
                style={{ color: 'rgba(255,255,255,0.3)' }}
              />
            )}
          </div>
        </div>

        {/* Badges + Scores */}
        <div
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: 8,
            flexWrap: 'wrap',
          }}
        >
          {/* Readiness Badge */}
          <span
            style={{
              fontSize: 10,
              fontWeight: 600,
              fontFamily: "'JetBrains Mono', monospace",
              color: readinessConfig.color,
              background: readinessConfig.color + '18',
              border: `1px solid ${readinessConfig.color}30`,
              padding: '2px 8px',
              borderRadius: 4,
            }}
          >
            {readinessConfig.label}
          </span>

          {/* Status Badge */}
          <span
            style={{
              fontSize: 10,
              fontWeight: 600,
              fontFamily: "'JetBrains Mono', monospace",
              color: statusColor,
              background: statusColor + '18',
              border: `1px solid ${statusColor}30`,
              padding: '2px 8px',
              borderRadius: 4,
              textTransform: 'uppercase' as const,
            }}
          >
            {innovation.status}
          </span>

          {/* Spacer */}
          <div style={{ flex: 1 }} />

          {/* Score Bars */}
          <div style={{ display: 'flex', gap: 12, alignItems: 'center' }}>
            <ScoreBar label="IMP" value={innovation.impact_level} color={color} />
            <ScoreBar
              label="FEA"
              value={innovation.feasibility}
              color="#00CC66"
            />
            <ScoreBar label="NOV" value={innovation.novelty} color="#0066FF" />
          </div>
        </div>
      </button>

      {/* Expanded Content */}
      {expanded && (
        <div
          style={{
            borderTop: '1px solid #1A1A1A',
            padding: 16,
          }}
        >
          {/* Tags */}
          {innovation.tags.length > 0 && (
            <div style={{ marginBottom: 14 }}>
              <div
                style={{
                  fontSize: 10,
                  fontWeight: 600,
                  color: 'rgba(255,255,255,0.3)',
                  letterSpacing: '0.06em',
                  textTransform: 'uppercase' as const,
                  marginBottom: 6,
                }}
              >
                TAGS
              </div>
              <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap' }}>
                {innovation.tags.map((tag) => (
                  <span
                    key={tag}
                    style={{
                      fontSize: 11,
                      color: 'rgba(255,255,255,0.6)',
                      background: 'rgba(255,255,255,0.06)',
                      border: '1px solid rgba(255,255,255,0.08)',
                      padding: '2px 8px',
                      borderRadius: 4,
                      fontFamily: "'JetBrains Mono', monospace",
                    }}
                  >
                    {tag}
                  </span>
                ))}
              </div>
            </div>
          )}

          {/* Details */}
          {Object.keys(innovation.details).length > 0 && (
            <div>
              <div
                style={{
                  fontSize: 10,
                  fontWeight: 600,
                  color: 'rgba(255,255,255,0.3)',
                  letterSpacing: '0.06em',
                  textTransform: 'uppercase' as const,
                  marginBottom: 6,
                }}
              >
                DETAILS
              </div>
              <div
                style={{
                  background: 'rgba(255,255,255,0.02)',
                  border: '1px solid rgba(255,255,255,0.06)',
                  borderRadius: 8,
                  padding: 12,
                }}
              >
                <DetailRenderer data={innovation.details} depth={0} />
              </div>
            </div>
          )}

          {/* Metadata */}
          <div
            style={{
              marginTop: 14,
              display: 'flex',
              gap: 16,
              flexWrap: 'wrap',
            }}
          >
            <MetaItem label="Category" value={innovation.category} />
            <MetaItem label="Time Horizon" value={innovation.time_horizon} />
            <MetaItem
              label="Created"
              value={new Date(innovation.created_at).toLocaleDateString()}
            />
            <MetaItem
              label="Updated"
              value={new Date(innovation.updated_at).toLocaleDateString()}
            />
          </div>
        </div>
      )}
    </div>
  );
}

// ── Score Bar ────────────────────────────────────────────────

function ScoreBar({
  label,
  value,
  color,
}: {
  label: string;
  value: number;
  color: string;
}) {
  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: 4 }}>
      <span
        style={{
          fontSize: 9,
          fontFamily: "'JetBrains Mono', monospace",
          color: 'rgba(255,255,255,0.35)',
          fontWeight: 600,
          width: 24,
        }}
      >
        {label}
      </span>
      <div
        style={{
          width: 40,
          height: 4,
          borderRadius: 2,
          background: 'rgba(255,255,255,0.08)',
          overflow: 'hidden',
        }}
      >
        <div
          style={{
            width: `${(value / 10) * 100}%`,
            height: '100%',
            background: color,
            borderRadius: 2,
          }}
        />
      </div>
      <span
        style={{
          fontSize: 10,
          fontFamily: "'JetBrains Mono', monospace",
          color: 'rgba(255,255,255,0.5)',
          width: 14,
          textAlign: 'right' as const,
        }}
      >
        {value}
      </span>
    </div>
  );
}

// ── Detail Renderer (recursive) ──────────────────────────────

function DetailRenderer({
  data,
  depth,
}: {
  data: Record<string, unknown> | unknown[] | unknown;
  depth: number;
}) {
  if (data === null || data === undefined) {
    return (
      <span
        style={{
          color: 'rgba(255,255,255,0.3)',
          fontStyle: 'italic',
          fontSize: 12,
        }}
      >
        null
      </span>
    );
  }

  if (Array.isArray(data)) {
    return (
      <div style={{ paddingLeft: depth > 0 ? 12 : 0 }}>
        {data.map((item, idx) => (
          <div
            key={idx}
            style={{
              display: 'flex',
              alignItems: 'flex-start',
              gap: 6,
              marginBottom: 4,
            }}
          >
            <span
              style={{
                fontSize: 11,
                color: 'rgba(255,255,255,0.3)',
                fontFamily: "'JetBrains Mono', monospace",
                flexShrink: 0,
              }}
            >
              [{idx}]
            </span>
            {typeof item === 'object' && item !== null ? (
              <DetailRenderer data={item as Record<string, unknown>} depth={depth + 1} />
            ) : (
              <span
                style={{
                  fontSize: 12,
                  color: 'rgba(255,255,255,0.6)',
                  fontFamily: "'JetBrains Mono', monospace",
                }}
              >
                {String(item)}
              </span>
            )}
          </div>
        ))}
      </div>
    );
  }

  if (typeof data === 'object') {
    const obj = data as Record<string, unknown>;
    return (
      <div style={{ paddingLeft: depth > 0 ? 12 : 0 }}>
        {Object.entries(obj).map(([key, val]) => (
          <div
            key={key}
            style={{
              display: 'flex',
              alignItems: 'flex-start',
              gap: 8,
              marginBottom: 4,
            }}
          >
            <span
              style={{
                fontSize: 11,
                fontWeight: 600,
                color: 'rgba(255,255,255,0.5)',
                fontFamily: "'JetBrains Mono', monospace",
                minWidth: 80,
                flexShrink: 0,
              }}
            >
              {key}:
            </span>
            {typeof val === 'object' && val !== null ? (
              <DetailRenderer data={val as Record<string, unknown>} depth={depth + 1} />
            ) : (
              <span
                style={{
                  fontSize: 12,
                  color: 'rgba(255,255,255,0.6)',
                  fontFamily: "'JetBrains Mono', monospace",
                }}
              >
                {String(val)}
              </span>
            )}
          </div>
        ))}
      </div>
    );
  }

  return (
    <span
      style={{
        fontSize: 12,
        color: 'rgba(255,255,255,0.6)',
        fontFamily: "'JetBrains Mono', monospace",
      }}
    >
      {String(data)}
    </span>
  );
}

// ── Meta Item ────────────────────────────────────────────────

function MetaItem({ label, value }: { label: string; value: string }) {
  return (
    <div>
      <div
        style={{
          fontSize: 9,
          fontWeight: 600,
          color: 'rgba(255,255,255,0.3)',
          letterSpacing: '0.06em',
          textTransform: 'uppercase' as const,
          marginBottom: 2,
        }}
      >
        {label}
      </div>
      <div
        style={{
          fontSize: 11,
          color: 'rgba(255,255,255,0.6)',
          fontFamily: "'JetBrains Mono', monospace",
        }}
      >
        {value}
      </div>
    </div>
  );
}
