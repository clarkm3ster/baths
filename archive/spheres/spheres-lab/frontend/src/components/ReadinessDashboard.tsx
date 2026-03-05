import { useState, useEffect } from 'react';
import { ChevronDown, ChevronUp } from 'lucide-react';
import {
  getAllInnovations,
  getReadiness,
  getReadinessConfig,
  getStatusColor,
  getDomainConfig,
  READINESS_LEVELS,
  type Innovation,
  type ReadinessLevel,
} from '../api/client';

export default function ReadinessDashboard() {
  const [innovations, setInnovations] = useState<Innovation[]>([]);
  const [loading, setLoading] = useState(true);
  const [expandedCard, setExpandedCard] = useState<number | null>(null);

  useEffect(() => {
    let cancelled = false;
    async function load() {
      setLoading(true);
      const data = await getAllInnovations();
      if (!cancelled) {
        setInnovations(data);
        setLoading(false);
      }
    }
    load();
    return () => {
      cancelled = true;
    };
  }, []);

  // Group innovations by readiness
  const grouped: Record<ReadinessLevel, Innovation[]> = {
    immediate: [],
    '1-year': [],
    '5-year': [],
    moonshot: [],
  };

  innovations.forEach((inn) => {
    const r = getReadiness(inn);
    grouped[r].push(inn);
  });

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
        Loading readiness data...
      </div>
    );
  }

  return (
    <div style={{ padding: 24, height: '100%', display: 'flex', flexDirection: 'column' }}>
      {/* Header */}
      <div style={{ marginBottom: 20, flexShrink: 0 }}>
        <h1
          style={{
            fontSize: 20,
            fontWeight: 700,
            color: '#FFFFFF',
            margin: 0,
            marginBottom: 6,
          }}
        >
          Readiness Dashboard
        </h1>
        <p
          style={{
            fontSize: 13,
            color: 'rgba(255,255,255,0.5)',
            margin: 0,
          }}
        >
          {innovations.length} innovations organized by deployment readiness
        </p>
      </div>

      {/* Kanban Columns */}
      <div
        style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(4, 1fr)',
          gap: 12,
          flex: 1,
          overflow: 'hidden',
        }}
      >
        {READINESS_LEVELS.map((level) => {
          const items = grouped[level.key];
          return (
            <div
              key={level.key}
              style={{
                background: '#0A0A0A',
                border: '1px solid #1A1A1A',
                borderRadius: 12,
                display: 'flex',
                flexDirection: 'column',
                overflow: 'hidden',
              }}
            >
              {/* Column Header */}
              <div
                style={{
                  padding: '14px 16px',
                  borderBottom: '1px solid #1A1A1A',
                  flexShrink: 0,
                }}
              >
                <div
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-between',
                    marginBottom: 4,
                  }}
                >
                  <div
                    style={{
                      display: 'flex',
                      alignItems: 'center',
                      gap: 8,
                    }}
                  >
                    <div
                      style={{
                        width: 10,
                        height: 10,
                        borderRadius: 3,
                        background: level.color,
                      }}
                    />
                    <span
                      style={{
                        fontSize: 13,
                        fontWeight: 700,
                        color: '#FFFFFF',
                      }}
                    >
                      {level.label}
                    </span>
                  </div>
                  <span
                    style={{
                      fontSize: 12,
                      fontFamily: "'JetBrains Mono', monospace",
                      fontWeight: 600,
                      color: level.color,
                      background: level.color + '15',
                      padding: '2px 8px',
                      borderRadius: 6,
                    }}
                  >
                    {items.length}
                  </span>
                </div>
                <div
                  style={{
                    fontSize: 11,
                    color: 'rgba(255,255,255,0.35)',
                    lineHeight: 1.4,
                  }}
                >
                  {level.description}
                </div>
              </div>

              {/* Column Cards */}
              <div
                style={{
                  flex: 1,
                  overflowY: 'auto',
                  padding: 8,
                  display: 'flex',
                  flexDirection: 'column',
                  gap: 6,
                }}
              >
                {items.length === 0 ? (
                  <div
                    style={{
                      textAlign: 'center',
                      padding: '24px 12px',
                      color: 'rgba(255,255,255,0.2)',
                      fontSize: 11,
                      fontFamily: "'JetBrains Mono', monospace",
                    }}
                  >
                    No items
                  </div>
                ) : (
                  items.map((inn) => (
                    <KanbanCard
                      key={inn.id}
                      innovation={inn}
                      expanded={expandedCard === inn.id}
                      onToggle={() =>
                        setExpandedCard(
                          expandedCard === inn.id ? null : inn.id
                        )
                      }
                    />
                  ))
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

// ── Kanban Card ──────────────────────────────────────────────

function KanbanCard({
  innovation,
  expanded,
  onToggle,
}: {
  innovation: Innovation;
  expanded: boolean;
  onToggle: () => void;
}) {
  const statusColor = getStatusColor(innovation.status);
  const domainConfig = getDomainConfig(innovation.domain);
  const domainColor = domainConfig?.color ?? '#0066FF';

  return (
    <div
      style={{
        background: expanded ? '#111111' : 'rgba(255,255,255,0.02)',
        border: `1px solid ${expanded ? '#2A2A2A' : 'rgba(255,255,255,0.06)'}`,
        borderRadius: 8,
        overflow: 'hidden',
        transition: 'background 0.15s, border-color 0.15s',
      }}
    >
      <button
        onClick={onToggle}
        style={{
          width: '100%',
          background: 'none',
          border: 'none',
          padding: 12,
          cursor: 'pointer',
          textAlign: 'left',
          color: '#FFFFFF',
        }}
      >
        {/* Title */}
        <div
          style={{
            display: 'flex',
            alignItems: 'flex-start',
            justifyContent: 'space-between',
            gap: 6,
          }}
        >
          <div
            style={{
              fontSize: 12,
              fontWeight: 600,
              color: '#FFFFFF',
              lineHeight: 1.4,
              flex: 1,
            }}
          >
            {innovation.title}
          </div>
          {expanded ? (
            <ChevronUp
              size={12}
              style={{ color: 'rgba(255,255,255,0.3)', flexShrink: 0, marginTop: 2 }}
            />
          ) : (
            <ChevronDown
              size={12}
              style={{ color: 'rgba(255,255,255,0.3)', flexShrink: 0, marginTop: 2 }}
            />
          )}
        </div>

        {/* Badges */}
        <div
          style={{
            display: 'flex',
            gap: 4,
            marginTop: 8,
            flexWrap: 'wrap',
          }}
        >
          {/* Status */}
          <span
            style={{
              fontSize: 9,
              fontWeight: 600,
              fontFamily: "'JetBrains Mono', monospace",
              color: statusColor,
              background: statusColor + '18',
              padding: '1px 6px',
              borderRadius: 3,
              textTransform: 'uppercase' as const,
            }}
          >
            {innovation.status}
          </span>
          {/* Domain */}
          <span
            style={{
              fontSize: 9,
              fontWeight: 600,
              fontFamily: "'JetBrains Mono', monospace",
              color: domainColor,
              background: domainColor + '18',
              padding: '1px 6px',
              borderRadius: 3,
            }}
          >
            {domainConfig?.icon ?? ''} {domainConfig?.label ?? innovation.domain}
          </span>
        </div>

        {/* Mini Score Row */}
        <div
          style={{
            display: 'flex',
            gap: 8,
            marginTop: 8,
          }}
        >
          <MiniScore label="IMP" value={innovation.impact_level} />
          <MiniScore label="FEA" value={innovation.feasibility} />
          <MiniScore label="NOV" value={innovation.novelty} />
        </div>
      </button>

      {/* Expanded */}
      {expanded && (
        <div
          style={{
            borderTop: '1px solid rgba(255,255,255,0.06)',
            padding: 12,
          }}
        >
          <p
            style={{
              fontSize: 11,
              color: 'rgba(255,255,255,0.5)',
              lineHeight: 1.5,
              margin: 0,
              marginBottom: 8,
            }}
          >
            {innovation.summary}
          </p>
          {innovation.tags.length > 0 && (
            <div style={{ display: 'flex', gap: 4, flexWrap: 'wrap' }}>
              {innovation.tags.map((tag) => (
                <span
                  key={tag}
                  style={{
                    fontSize: 9,
                    fontFamily: "'JetBrains Mono', monospace",
                    color: 'rgba(255,255,255,0.4)',
                    background: 'rgba(255,255,255,0.04)',
                    padding: '1px 6px',
                    borderRadius: 3,
                  }}
                >
                  {tag}
                </span>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}

// ── Mini Score Display ───────────────────────────────────────

function MiniScore({ label, value }: { label: string; value: number }) {
  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: 3 }}>
      <span
        style={{
          fontSize: 8,
          fontFamily: "'JetBrains Mono', monospace",
          color: 'rgba(255,255,255,0.3)',
          fontWeight: 600,
        }}
      >
        {label}
      </span>
      <span
        style={{
          fontSize: 10,
          fontFamily: "'JetBrains Mono', monospace",
          color: 'rgba(255,255,255,0.5)',
          fontWeight: 600,
        }}
      >
        {value}
      </span>
    </div>
  );
}
