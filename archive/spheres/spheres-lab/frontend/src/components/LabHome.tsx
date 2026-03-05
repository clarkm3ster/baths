import { useState, useEffect } from 'react';
import {
  DOMAINS,
  DEMO_TEAMMATES,
  DEMO_INNOVATIONS,
  getReadiness,
  READINESS_LEVELS,
  getTeammates,
  getAllInnovations,
  type Teammate,
  type Innovation,
  type DomainConfig,
  type ReadinessLevel,
} from '../api/client';

interface LabHomeProps {
  onSelectDomain: (slug: string) => void;
}

export default function LabHome({ onSelectDomain }: LabHomeProps) {
  const [teammates, setTeammates] = useState<Teammate[]>([]);
  const [innovations, setInnovations] = useState<Innovation[]>([]);
  const [loading, setLoading] = useState(true);
  const [hoveredCard, setHoveredCard] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    async function load() {
      setLoading(true);
      const [t, i] = await Promise.all([getTeammates(), getAllInnovations()]);
      if (!cancelled) {
        setTeammates(t);
        setInnovations(i);
        setLoading(false);
      }
    }
    load();
    return () => {
      cancelled = true;
    };
  }, []);

  // Build readiness breakdown per domain
  function getReadinessBreakdown(domain: string): Record<ReadinessLevel, number> {
    const domainInns = innovations.filter((i) => i.domain === domain);
    const counts: Record<ReadinessLevel, number> = {
      immediate: 0,
      '1-year': 0,
      '5-year': 0,
      moonshot: 0,
    };
    domainInns.forEach((inn) => {
      counts[getReadiness(inn)]++;
    });
    return counts;
  }

  function getInnovationCount(domain: DomainConfig): number {
    // Prefer live teammate data, fallback to counting innovations
    const tm = teammates.find(
      (t) => t.slug === domain.slug || t.domain === domain.backendDomain
    );
    if (tm) return tm.innovation_count;
    return innovations.filter((i) => i.domain === domain.backendDomain).length;
  }

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
        Loading innovation data...
      </div>
    );
  }

  return (
    <div style={{ padding: 24 }}>
      {/* Page Header */}
      <div style={{ marginBottom: 24 }}>
        <h1
          style={{
            fontSize: 20,
            fontWeight: 700,
            color: '#FFFFFF',
            marginBottom: 6,
          }}
        >
          Innovation Domains
        </h1>
        <p
          style={{
            fontSize: 13,
            color: 'rgba(255,255,255,0.5)',
            maxWidth: 600,
          }}
        >
          {DOMAINS.length} active domains generating innovations across the
          SPHERES ecosystem. Select a domain to explore its innovations.
        </p>
      </div>

      {/* Summary Bar */}
      <div
        style={{
          display: 'flex',
          gap: 16,
          marginBottom: 24,
          flexWrap: 'wrap',
        }}
      >
        <SummaryCard
          label="Total Domains"
          value={DOMAINS.length.toString()}
          color="#0066FF"
        />
        <SummaryCard
          label="Total Innovations"
          value={innovations.length.toString()}
          color="#00CC66"
        />
        <SummaryCard
          label="Active Teammates"
          value={
            (teammates.length || DEMO_TEAMMATES.length).toString()
          }
          color="#9333EA"
        />
        <SummaryCard
          label="Avg Impact"
          value={
            innovations.length > 0
              ? (
                  innovations.reduce((s, i) => s + i.impact_level, 0) /
                  innovations.length
                ).toFixed(1)
              : '--'
          }
          color="#FFCC00"
        />
      </div>

      {/* Domain Grid */}
      <div
        style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fill, minmax(320, 1fr))',
          gap: 12,
        }}
      >
        {/* Use CSS grid with responsive columns */}
        <div
          style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fill, minmax(320px, 1fr))',
            gap: 12,
          }}
        >
          {DOMAINS.map((domain) => {
            const count = getInnovationCount(domain);
            const breakdown = getReadinessBreakdown(domain.backendDomain);
            const total =
              breakdown.immediate +
              breakdown['1-year'] +
              breakdown['5-year'] +
              breakdown.moonshot;
            const isHovered = hoveredCard === domain.slug;

            return (
              <button
                key={domain.slug}
                onClick={() => onSelectDomain(domain.slug)}
                onMouseEnter={() => setHoveredCard(domain.slug)}
                onMouseLeave={() => setHoveredCard(null)}
                style={{
                  background: isHovered ? '#111111' : '#0A0A0A',
                  border: `1px solid ${
                    isHovered ? domain.color + '40' : '#1A1A1A'
                  }`,
                  borderRadius: 10,
                  padding: 20,
                  cursor: 'pointer',
                  textAlign: 'left',
                  transition: 'background 0.15s, border-color 0.25s',
                  display: 'flex',
                  flexDirection: 'column',
                  gap: 12,
                }}
              >
                {/* Card Header */}
                <div
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-between',
                  }}
                >
                  <div
                    style={{ display: 'flex', alignItems: 'center', gap: 12 }}
                  >
                    <div
                      style={{
                        width: 40,
                        height: 40,
                        borderRadius: 10,
                        background: domain.color + '18',
                        border: `1px solid ${domain.color}30`,
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        fontSize: 20,
                        color: domain.color,
                        flexShrink: 0,
                      }}
                    >
                      {domain.icon}
                    </div>
                    <div>
                      <div
                        style={{
                          fontSize: 14,
                          fontWeight: 600,
                          color: '#FFFFFF',
                        }}
                      >
                        {domain.label}
                      </div>
                    </div>
                  </div>
                  <div
                    style={{
                      fontSize: 12,
                      fontFamily: "'JetBrains Mono', monospace",
                      color: domain.color,
                      fontWeight: 600,
                      background: domain.color + '15',
                      padding: '3px 8px',
                      borderRadius: 6,
                    }}
                  >
                    {count}
                  </div>
                </div>

                {/* Description */}
                <p
                  style={{
                    fontSize: 12,
                    color: 'rgba(255,255,255,0.45)',
                    lineHeight: 1.5,
                    margin: 0,
                  }}
                >
                  {domain.description}
                </p>

                {/* Readiness Breakdown Bar */}
                {total > 0 ? (
                  <div>
                    <div
                      style={{
                        display: 'flex',
                        height: 4,
                        borderRadius: 2,
                        overflow: 'hidden',
                        background: 'rgba(255,255,255,0.05)',
                      }}
                    >
                      {READINESS_LEVELS.map((level) => {
                        const pct = (breakdown[level.key] / total) * 100;
                        if (pct === 0) return null;
                        return (
                          <div
                            key={level.key}
                            style={{
                              width: `${pct}%`,
                              background: level.color,
                              minWidth: pct > 0 ? 4 : 0,
                            }}
                          />
                        );
                      })}
                    </div>
                    <div
                      style={{
                        display: 'flex',
                        gap: 10,
                        marginTop: 6,
                        flexWrap: 'wrap',
                      }}
                    >
                      {READINESS_LEVELS.map((level) =>
                        breakdown[level.key] > 0 ? (
                          <span
                            key={level.key}
                            style={{
                              fontSize: 10,
                              fontFamily: "'JetBrains Mono', monospace",
                              color: level.color,
                            }}
                          >
                            {level.label}: {breakdown[level.key]}
                          </span>
                        ) : null
                      )}
                    </div>
                  </div>
                ) : (
                  <div
                    style={{
                      height: 4,
                      borderRadius: 2,
                      background: 'rgba(255,255,255,0.05)',
                    }}
                  />
                )}
              </button>
            );
          })}
        </div>
      </div>
    </div>
  );
}

// ── Summary Card ──────────────────────────────────────────────

function SummaryCard({
  label,
  value,
  color,
}: {
  label: string;
  value: string;
  color: string;
}) {
  return (
    <div
      style={{
        background: '#0A0A0A',
        border: '1px solid #1A1A1A',
        borderRadius: 10,
        padding: '14px 20px',
        minWidth: 140,
        flex: '1 1 140px',
      }}
    >
      <div
        style={{
          fontSize: 10,
          fontWeight: 600,
          color: 'rgba(255,255,255,0.4)',
          letterSpacing: '0.06em',
          textTransform: 'uppercase' as const,
          marginBottom: 4,
        }}
      >
        {label}
      </div>
      <div
        style={{
          fontSize: 22,
          fontWeight: 700,
          color,
          fontFamily: "'JetBrains Mono', monospace",
        }}
      >
        {value}
      </div>
    </div>
  );
}
