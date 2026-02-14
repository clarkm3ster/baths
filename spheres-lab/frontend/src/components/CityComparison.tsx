import { useState } from 'react';
import { ArrowLeftRight, BarChart3, MapPin, TrendingUp, TrendingDown, Minus } from 'lucide-react';

interface CityDimensions {
  inventory: number;
  permits: number;
  culture: number;
  funding: number;
  policy: number;
}

interface CityData {
  name: string;
  state: string;
  readiness_score: number;
  dimensions: CityDimensions;
  archetype: string;
  vacant_lots: string;
  key_strength: string;
  key_challenge: string;
}

const CITIES: CityData[] = [
  {
    name: 'Philadelphia',
    state: 'PA',
    readiness_score: 82,
    dimensions: { inventory: 90, permits: 68, culture: 92, funding: 78, policy: 82 },
    archetype: 'Rust Belt',
    vacant_lots: '40,000+',
    key_strength: 'Cultural infrastructure',
    key_challenge: 'Permit complexity',
  },
  {
    name: 'Detroit',
    state: 'MI',
    readiness_score: 91,
    dimensions: { inventory: 98, permits: 85, culture: 88, funding: 72, policy: 95 },
    archetype: 'Rust Belt',
    vacant_lots: '150,000+',
    key_strength: 'Massive inventory + political will',
    key_challenge: 'Funding gaps',
  },
  {
    name: 'Baltimore',
    state: 'MD',
    readiness_score: 74,
    dimensions: { inventory: 82, permits: 65, culture: 76, funding: 70, policy: 75 },
    archetype: 'Rust Belt',
    vacant_lots: '16,000+',
    key_strength: 'Strong CDCs',
    key_challenge: 'Safety concerns',
  },
  {
    name: 'St. Louis',
    state: 'MO',
    readiness_score: 78,
    dimensions: { inventory: 88, permits: 72, culture: 74, funding: 68, policy: 82 },
    archetype: 'Rust Belt',
    vacant_lots: '25,000+',
    key_strength: 'Land bank efficiency',
    key_challenge: 'Population loss',
  },
  {
    name: 'Cleveland',
    state: 'OH',
    readiness_score: 76,
    dimensions: { inventory: 86, permits: 70, culture: 72, funding: 66, policy: 80 },
    archetype: 'Rust Belt',
    vacant_lots: '27,000+',
    key_strength: 'Land bank model',
    key_challenge: 'Economic base',
  },
  {
    name: 'Austin',
    state: 'TX',
    readiness_score: 64,
    dimensions: { inventory: 42, permits: 58, culture: 85, funding: 88, policy: 48 },
    archetype: 'Sun Belt',
    vacant_lots: '3,000+',
    key_strength: 'Tech wealth + creative scene',
    key_challenge: 'NIMBY resistance',
  },
  {
    name: 'Pittsburgh',
    state: 'PA',
    readiness_score: 72,
    dimensions: { inventory: 76, permits: 68, culture: 80, funding: 74, policy: 72 },
    archetype: 'Rust Belt',
    vacant_lots: '12,000+',
    key_strength: 'University anchors',
    key_challenge: 'Terrain challenges',
  },
  {
    name: 'Camden',
    state: 'NJ',
    readiness_score: 68,
    dimensions: { inventory: 78, permits: 62, culture: 64, funding: 58, policy: 76 },
    archetype: 'Rust Belt',
    vacant_lots: '3,000+',
    key_strength: 'State support',
    key_challenge: 'Resource constraints',
  },
  {
    name: 'Newark',
    state: 'NJ',
    readiness_score: 70,
    dimensions: { inventory: 74, permits: 64, culture: 72, funding: 68, policy: 72 },
    archetype: 'Gateway',
    vacant_lots: '5,000+',
    key_strength: 'Transit access',
    key_challenge: 'Political complexity',
  },
  {
    name: 'Gary',
    state: 'IN',
    readiness_score: 80,
    dimensions: { inventory: 92, permits: 78, culture: 62, funding: 52, policy: 88 },
    archetype: 'Rust Belt',
    vacant_lots: '10,000+',
    key_strength: 'Policy openness',
    key_challenge: 'Population decline',
  },
];

const DIMENSION_LABELS: { key: keyof CityDimensions; label: string }[] = [
  { key: 'inventory', label: 'Inventory' },
  { key: 'permits', label: 'Permits' },
  { key: 'culture', label: 'Culture' },
  { key: 'funding', label: 'Funding' },
  { key: 'policy', label: 'Policy' },
];

function getScoreColor(score: number): string {
  if (score >= 80) return '#22C55E';
  if (score >= 60) return '#EAB308';
  return '#EF4444';
}

function getArchetypeColor(archetype: string): string {
  switch (archetype) {
    case 'Rust Belt':
      return '#F97316';
    case 'Sun Belt':
      return '#EAB308';
    case 'Gateway':
      return '#8B5CF6';
    default:
      return '#6B7280';
  }
}

export default function CityComparison() {
  const [cityAIndex, setCityAIndex] = useState(0); // Philadelphia
  const [cityBIndex, setCityBIndex] = useState(1); // Detroit
  const [hoveredDimension, setHoveredDimension] = useState<string | null>(null);

  const cityA = CITIES[cityAIndex];
  const cityB = CITIES[cityBIndex];

  function swapCities() {
    setCityAIndex(cityBIndex);
    setCityBIndex(cityAIndex);
  }

  const selectStyle: React.CSSProperties = {
    background: '#0A0A0A',
    border: '1px solid #1A1A1A',
    borderRadius: 8,
    color: '#FFFFFF',
    fontFamily: "'Inter', sans-serif",
    fontSize: 14,
    fontWeight: 500,
    padding: '10px 14px',
    paddingRight: 36,
    flex: 1,
    cursor: 'pointer',
    outline: 'none',
    appearance: 'none',
    WebkitAppearance: 'none',
    MozAppearance: 'none' as React.CSSProperties['MozAppearance'],
    backgroundImage:
      'url("data:image/svg+xml,%3Csvg xmlns=\'http://www.w3.org/2000/svg\' width=\'12\' height=\'12\' viewBox=\'0 0 24 24\' fill=\'none\' stroke=\'rgba(255,255,255,0.5)\' stroke-width=\'2\'%3E%3Cpolyline points=\'6 9 12 15 18 9\'/%3E%3C/svg%3E")',
    backgroundRepeat: 'no-repeat',
    backgroundPosition: 'right 12px center',
  };

  return (
    <div
      style={{
        padding: 24,
        height: '100%',
        display: 'flex',
        flexDirection: 'column',
        background: '#050505',
        overflowY: 'auto',
      }}
    >
      {/* Header */}
      <div style={{ marginBottom: 24, flexShrink: 0 }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 6 }}>
          <BarChart3 size={20} color="#0066FF" />
          <h1
            style={{
              fontSize: 20,
              fontWeight: 700,
              color: '#FFFFFF',
              margin: 0,
              fontFamily: "'Inter', sans-serif",
            }}
          >
            City Comparison Tool
          </h1>
        </div>
        <p
          style={{
            fontSize: 13,
            color: 'rgba(255,255,255,0.5)',
            margin: 0,
            fontFamily: "'Inter', sans-serif",
          }}
        >
          Compare SPHERES readiness scores and dimensions across cities
        </p>
      </div>

      {/* City Selector Row */}
      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          gap: 12,
          marginBottom: 28,
          flexShrink: 0,
        }}
      >
        <div style={{ position: 'relative', flex: 1 }}>
          <select
            value={cityAIndex}
            onChange={(e) => setCityAIndex(Number(e.target.value))}
            style={selectStyle}
          >
            {CITIES.map((city, i) => (
              <option key={city.name} value={i} style={{ background: '#0A0A0A' }}>
                {city.name}, {city.state}
              </option>
            ))}
          </select>
        </div>

        <button
          onClick={swapCities}
          style={{
            background: '#0A0A0A',
            border: '1px solid #1A1A1A',
            borderRadius: 8,
            padding: 10,
            cursor: 'pointer',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            flexShrink: 0,
            transition: 'border-color 0.15s',
          }}
          onMouseEnter={(e) => {
            (e.currentTarget as HTMLButtonElement).style.borderColor = '#2A2A2A';
          }}
          onMouseLeave={(e) => {
            (e.currentTarget as HTMLButtonElement).style.borderColor = '#1A1A1A';
          }}
        >
          <ArrowLeftRight size={16} color="rgba(255,255,255,0.5)" />
        </button>

        <div style={{ position: 'relative', flex: 1 }}>
          <select
            value={cityBIndex}
            onChange={(e) => setCityBIndex(Number(e.target.value))}
            style={selectStyle}
          >
            {CITIES.map((city, i) => (
              <option key={city.name} value={i} style={{ background: '#0A0A0A' }}>
                {city.name}, {city.state}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Score Comparison */}
      <div
        style={{
          display: 'grid',
          gridTemplateColumns: '1fr auto 1fr',
          gap: 16,
          marginBottom: 28,
          flexShrink: 0,
        }}
      >
        {/* City A Score */}
        <div
          style={{
            background: '#0A0A0A',
            border: '1px solid #1A1A1A',
            borderRadius: 12,
            padding: 24,
            textAlign: 'center',
          }}
        >
          <div
            style={{
              fontSize: 13,
              color: 'rgba(255,255,255,0.5)',
              marginBottom: 8,
              fontFamily: "'Inter', sans-serif",
            }}
          >
            {cityA.name}, {cityA.state}
          </div>
          <div
            style={{
              fontSize: 48,
              fontWeight: 700,
              color: getScoreColor(cityA.readiness_score),
              fontFamily: "'JetBrains Mono', monospace",
              lineHeight: 1,
              marginBottom: 8,
            }}
          >
            {cityA.readiness_score}
          </div>
          <div
            style={{
              fontSize: 11,
              color: 'rgba(255,255,255,0.4)',
              fontFamily: "'JetBrains Mono', monospace",
              textTransform: 'uppercase',
              letterSpacing: 1,
            }}
          >
            Readiness Score
          </div>
        </div>

        {/* VS Divider */}
        <div
          style={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
          }}
        >
          <div
            style={{
              fontSize: 14,
              fontWeight: 600,
              color: 'rgba(255,255,255,0.3)',
              fontFamily: "'Inter', sans-serif",
              textTransform: 'uppercase',
              letterSpacing: 2,
            }}
          >
            vs
          </div>
        </div>

        {/* City B Score */}
        <div
          style={{
            background: '#0A0A0A',
            border: '1px solid #1A1A1A',
            borderRadius: 12,
            padding: 24,
            textAlign: 'center',
          }}
        >
          <div
            style={{
              fontSize: 13,
              color: 'rgba(255,255,255,0.5)',
              marginBottom: 8,
              fontFamily: "'Inter', sans-serif",
            }}
          >
            {cityB.name}, {cityB.state}
          </div>
          <div
            style={{
              fontSize: 48,
              fontWeight: 700,
              color: getScoreColor(cityB.readiness_score),
              fontFamily: "'JetBrains Mono', monospace",
              lineHeight: 1,
              marginBottom: 8,
            }}
          >
            {cityB.readiness_score}
          </div>
          <div
            style={{
              fontSize: 11,
              color: 'rgba(255,255,255,0.4)',
              fontFamily: "'JetBrains Mono', monospace",
              textTransform: 'uppercase',
              letterSpacing: 1,
            }}
          >
            Readiness Score
          </div>
        </div>
      </div>

      {/* Dimension Bars Comparison */}
      <div
        style={{
          background: '#0A0A0A',
          border: '1px solid #1A1A1A',
          borderRadius: 12,
          padding: 24,
          marginBottom: 28,
          flexShrink: 0,
        }}
      >
        <div
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: 8,
            marginBottom: 20,
          }}
        >
          <BarChart3 size={16} color="rgba(255,255,255,0.4)" />
          <span
            style={{
              fontSize: 14,
              fontWeight: 600,
              color: '#FFFFFF',
              fontFamily: "'Inter', sans-serif",
            }}
          >
            Dimension Comparison
          </span>
        </div>

        <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
          {DIMENSION_LABELS.map(({ key, label }) => {
            const valA = cityA.dimensions[key];
            const valB = cityB.dimensions[key];
            const isHovered = hoveredDimension === key;

            return (
              <div
                key={key}
                onMouseEnter={() => setHoveredDimension(key)}
                onMouseLeave={() => setHoveredDimension(null)}
                style={{
                  padding: '8px 12px',
                  borderRadius: 8,
                  background: isHovered ? '#111111' : 'transparent',
                  transition: 'background 0.15s',
                }}
              >
                {/* Dimension label */}
                <div
                  style={{
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center',
                    marginBottom: 8,
                  }}
                >
                  <span
                    style={{
                      fontSize: 12,
                      fontWeight: 500,
                      color: 'rgba(255,255,255,0.5)',
                      fontFamily: "'Inter', sans-serif",
                      textTransform: 'uppercase',
                      letterSpacing: 0.5,
                    }}
                  >
                    {label}
                  </span>
                  <div style={{ display: 'flex', gap: 16 }}>
                    <span
                      style={{
                        fontSize: 13,
                        fontWeight: 600,
                        color: '#0066FF',
                        fontFamily: "'JetBrains Mono', monospace",
                      }}
                    >
                      {valA}
                    </span>
                    <span
                      style={{
                        fontSize: 13,
                        fontWeight: 600,
                        color: '#8B5CF6',
                        fontFamily: "'JetBrains Mono', monospace",
                      }}
                    >
                      {valB}
                    </span>
                  </div>
                </div>

                {/* Bars */}
                <div style={{ display: 'flex', flexDirection: 'column', gap: 4 }}>
                  {/* City A bar */}
                  <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                    <span
                      style={{
                        fontSize: 10,
                        color: 'rgba(255,255,255,0.3)',
                        fontFamily: "'JetBrains Mono', monospace",
                        width: 28,
                        textAlign: 'right',
                        flexShrink: 0,
                      }}
                    >
                      {cityA.state}
                    </span>
                    <div
                      style={{
                        flex: 1,
                        height: 8,
                        background: '#1A1A1A',
                        borderRadius: 4,
                        overflow: 'hidden',
                      }}
                    >
                      <div
                        style={{
                          width: `${valA}%`,
                          height: '100%',
                          background: '#0066FF',
                          borderRadius: 4,
                          transition: 'width 0.4s ease',
                        }}
                      />
                    </div>
                  </div>

                  {/* City B bar */}
                  <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                    <span
                      style={{
                        fontSize: 10,
                        color: 'rgba(255,255,255,0.3)',
                        fontFamily: "'JetBrains Mono', monospace",
                        width: 28,
                        textAlign: 'right',
                        flexShrink: 0,
                      }}
                    >
                      {cityB.state}
                    </span>
                    <div
                      style={{
                        flex: 1,
                        height: 8,
                        background: '#1A1A1A',
                        borderRadius: 4,
                        overflow: 'hidden',
                      }}
                    >
                      <div
                        style={{
                          width: `${valB}%`,
                          height: '100%',
                          background: '#8B5CF6',
                          borderRadius: 4,
                          transition: 'width 0.4s ease',
                        }}
                      />
                    </div>
                  </div>
                </div>
              </div>
            );
          })}
        </div>

        {/* Legend */}
        <div
          style={{
            display: 'flex',
            gap: 20,
            marginTop: 16,
            paddingTop: 16,
            borderTop: '1px solid #1A1A1A',
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
            <div
              style={{
                width: 10,
                height: 10,
                borderRadius: 2,
                background: '#0066FF',
              }}
            />
            <span
              style={{
                fontSize: 11,
                color: 'rgba(255,255,255,0.4)',
                fontFamily: "'Inter', sans-serif",
              }}
            >
              {cityA.name}
            </span>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
            <div
              style={{
                width: 10,
                height: 10,
                borderRadius: 2,
                background: '#8B5CF6',
              }}
            />
            <span
              style={{
                fontSize: 11,
                color: 'rgba(255,255,255,0.4)',
                fontFamily: "'Inter', sans-serif",
              }}
            >
              {cityB.name}
            </span>
          </div>
        </div>
      </div>

      {/* Gap Analysis */}
      <div
        style={{
          background: '#0A0A0A',
          border: '1px solid #1A1A1A',
          borderRadius: 12,
          padding: 24,
          marginBottom: 28,
          flexShrink: 0,
        }}
      >
        <div
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: 8,
            marginBottom: 20,
          }}
        >
          <ArrowLeftRight size={16} color="rgba(255,255,255,0.4)" />
          <span
            style={{
              fontSize: 14,
              fontWeight: 600,
              color: '#FFFFFF',
              fontFamily: "'Inter', sans-serif",
            }}
          >
            Gap Analysis
          </span>
        </div>

        <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
          {DIMENSION_LABELS.map(({ key, label }) => {
            const valA = cityA.dimensions[key];
            const valB = cityB.dimensions[key];
            const diff = valA - valB;
            const absDiff = Math.abs(diff);

            let leader: string;
            let GapIcon: typeof TrendingUp;
            let gapColor: string;

            if (diff > 0) {
              leader = cityA.name;
              GapIcon = TrendingUp;
              gapColor = '#0066FF';
            } else if (diff < 0) {
              leader = cityB.name;
              GapIcon = TrendingDown;
              gapColor = '#8B5CF6';
            } else {
              leader = 'Tied';
              GapIcon = Minus;
              gapColor = 'rgba(255,255,255,0.3)';
            }

            return (
              <div
                key={key}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                  padding: '10px 14px',
                  background: '#050505',
                  border: '1px solid #1A1A1A',
                  borderRadius: 8,
                }}
              >
                <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
                  <span
                    style={{
                      fontSize: 12,
                      fontWeight: 500,
                      color: 'rgba(255,255,255,0.6)',
                      fontFamily: "'Inter', sans-serif",
                      width: 70,
                    }}
                  >
                    {label}
                  </span>
                  <GapIcon size={14} color={gapColor} />
                  <span
                    style={{
                      fontSize: 12,
                      color: gapColor,
                      fontFamily: "'Inter', sans-serif",
                      fontWeight: 500,
                    }}
                  >
                    {leader}
                    {diff !== 0 && (
                      <span
                        style={{
                          color: 'rgba(255,255,255,0.3)',
                          fontWeight: 400,
                          marginLeft: 4,
                        }}
                      >
                        leads
                      </span>
                    )}
                  </span>
                </div>
                <span
                  style={{
                    fontSize: 14,
                    fontWeight: 700,
                    color: diff === 0 ? 'rgba(255,255,255,0.3)' : gapColor,
                    fontFamily: "'JetBrains Mono', monospace",
                  }}
                >
                  {diff === 0 ? '0' : `+${absDiff}`}
                </span>
              </div>
            );
          })}
        </div>

        {/* Transfer Insights */}
        <div
          style={{
            display: 'grid',
            gridTemplateColumns: '1fr 1fr',
            gap: 12,
            marginTop: 20,
            paddingTop: 20,
            borderTop: '1px solid #1A1A1A',
          }}
        >
          {/* What City B needs from City A */}
          <div>
            <div
              style={{
                fontSize: 11,
                color: 'rgba(255,255,255,0.4)',
                fontFamily: "'Inter', sans-serif",
                marginBottom: 10,
                textTransform: 'uppercase',
                letterSpacing: 0.5,
              }}
            >
              What {cityB.name} needs from {cityA.name}
            </div>
            <div style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
              {DIMENSION_LABELS.filter(
                ({ key }) => cityA.dimensions[key] > cityB.dimensions[key]
              ).map(({ key, label }) => {
                const gap = cityA.dimensions[key] - cityB.dimensions[key];
                return (
                  <div
                    key={key}
                    style={{
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'space-between',
                      padding: '6px 10px',
                      background: 'rgba(0,102,255,0.06)',
                      border: '1px solid rgba(0,102,255,0.15)',
                      borderRadius: 6,
                    }}
                  >
                    <span
                      style={{
                        fontSize: 12,
                        color: 'rgba(255,255,255,0.6)',
                        fontFamily: "'Inter', sans-serif",
                      }}
                    >
                      {label}
                    </span>
                    <span
                      style={{
                        fontSize: 12,
                        fontWeight: 600,
                        color: '#0066FF',
                        fontFamily: "'JetBrains Mono', monospace",
                      }}
                    >
                      +{gap}
                    </span>
                  </div>
                );
              })}
              {DIMENSION_LABELS.filter(
                ({ key }) => cityA.dimensions[key] > cityB.dimensions[key]
              ).length === 0 && (
                <span
                  style={{
                    fontSize: 12,
                    color: 'rgba(255,255,255,0.3)',
                    fontFamily: "'Inter', sans-serif",
                    fontStyle: 'italic',
                  }}
                >
                  {cityB.name} leads or ties on all dimensions
                </span>
              )}
            </div>
          </div>

          {/* What City A needs from City B */}
          <div>
            <div
              style={{
                fontSize: 11,
                color: 'rgba(255,255,255,0.4)',
                fontFamily: "'Inter', sans-serif",
                marginBottom: 10,
                textTransform: 'uppercase',
                letterSpacing: 0.5,
              }}
            >
              What {cityA.name} needs from {cityB.name}
            </div>
            <div style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
              {DIMENSION_LABELS.filter(
                ({ key }) => cityB.dimensions[key] > cityA.dimensions[key]
              ).map(({ key, label }) => {
                const gap = cityB.dimensions[key] - cityA.dimensions[key];
                return (
                  <div
                    key={key}
                    style={{
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'space-between',
                      padding: '6px 10px',
                      background: 'rgba(139,92,246,0.06)',
                      border: '1px solid rgba(139,92,246,0.15)',
                      borderRadius: 6,
                    }}
                  >
                    <span
                      style={{
                        fontSize: 12,
                        color: 'rgba(255,255,255,0.6)',
                        fontFamily: "'Inter', sans-serif",
                      }}
                    >
                      {label}
                    </span>
                    <span
                      style={{
                        fontSize: 12,
                        fontWeight: 600,
                        color: '#8B5CF6',
                        fontFamily: "'JetBrains Mono', monospace",
                      }}
                    >
                      +{gap}
                    </span>
                  </div>
                );
              })}
              {DIMENSION_LABELS.filter(
                ({ key }) => cityB.dimensions[key] > cityA.dimensions[key]
              ).length === 0 && (
                <span
                  style={{
                    fontSize: 12,
                    color: 'rgba(255,255,255,0.3)',
                    fontFamily: "'Inter', sans-serif",
                    fontStyle: 'italic',
                  }}
                >
                  {cityA.name} leads or ties on all dimensions
                </span>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* City Profiles */}
      <div
        style={{
          display: 'grid',
          gridTemplateColumns: '1fr 1fr',
          gap: 16,
          flexShrink: 0,
        }}
      >
        {[cityA, cityB].map((city, idx) => {
          const accentColor = idx === 0 ? '#0066FF' : '#8B5CF6';

          return (
            <div
              key={city.name + city.state}
              style={{
                background: '#0A0A0A',
                border: '1px solid #1A1A1A',
                borderRadius: 12,
                padding: 20,
              }}
            >
              {/* City Name + Archetype */}
              <div
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                  marginBottom: 16,
                }}
              >
                <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                  <MapPin size={14} color={accentColor} />
                  <span
                    style={{
                      fontSize: 15,
                      fontWeight: 600,
                      color: '#FFFFFF',
                      fontFamily: "'Inter', sans-serif",
                    }}
                  >
                    {city.name}, {city.state}
                  </span>
                </div>
                <span
                  style={{
                    fontSize: 10,
                    fontWeight: 600,
                    color: getArchetypeColor(city.archetype),
                    background: `${getArchetypeColor(city.archetype)}15`,
                    border: `1px solid ${getArchetypeColor(city.archetype)}30`,
                    borderRadius: 20,
                    padding: '3px 10px',
                    fontFamily: "'Inter', sans-serif",
                    textTransform: 'uppercase',
                    letterSpacing: 0.5,
                  }}
                >
                  {city.archetype}
                </span>
              </div>

              {/* Facts Grid */}
              <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
                {/* Vacant Lots */}
                <div
                  style={{
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center',
                    padding: '8px 12px',
                    background: '#050505',
                    borderRadius: 6,
                    border: '1px solid #1A1A1A',
                  }}
                >
                  <span
                    style={{
                      fontSize: 11,
                      color: 'rgba(255,255,255,0.4)',
                      fontFamily: "'Inter', sans-serif",
                      textTransform: 'uppercase',
                      letterSpacing: 0.5,
                    }}
                  >
                    Vacant Lots
                  </span>
                  <span
                    style={{
                      fontSize: 14,
                      fontWeight: 700,
                      color: '#FFFFFF',
                      fontFamily: "'JetBrains Mono', monospace",
                    }}
                  >
                    {city.vacant_lots}
                  </span>
                </div>

                {/* Key Strength */}
                <div
                  style={{
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center',
                    padding: '8px 12px',
                    background: '#050505',
                    borderRadius: 6,
                    border: '1px solid #1A1A1A',
                  }}
                >
                  <span
                    style={{
                      fontSize: 11,
                      color: 'rgba(255,255,255,0.4)',
                      fontFamily: "'Inter', sans-serif",
                      textTransform: 'uppercase',
                      letterSpacing: 0.5,
                    }}
                  >
                    Key Strength
                  </span>
                  <span
                    style={{
                      fontSize: 12,
                      fontWeight: 500,
                      color: '#22C55E',
                      fontFamily: "'Inter', sans-serif",
                    }}
                  >
                    {city.key_strength}
                  </span>
                </div>

                {/* Key Challenge */}
                <div
                  style={{
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center',
                    padding: '8px 12px',
                    background: '#050505',
                    borderRadius: 6,
                    border: '1px solid #1A1A1A',
                  }}
                >
                  <span
                    style={{
                      fontSize: 11,
                      color: 'rgba(255,255,255,0.4)',
                      fontFamily: "'Inter', sans-serif",
                      textTransform: 'uppercase',
                      letterSpacing: 0.5,
                    }}
                  >
                    Key Challenge
                  </span>
                  <span
                    style={{
                      fontSize: 12,
                      fontWeight: 500,
                      color: '#EF4444',
                      fontFamily: "'Inter', sans-serif",
                    }}
                  >
                    {city.key_challenge}
                  </span>
                </div>

                {/* Readiness Score mini */}
                <div
                  style={{
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center',
                    padding: '8px 12px',
                    background: '#050505',
                    borderRadius: 6,
                    border: '1px solid #1A1A1A',
                  }}
                >
                  <span
                    style={{
                      fontSize: 11,
                      color: 'rgba(255,255,255,0.4)',
                      fontFamily: "'Inter', sans-serif",
                      textTransform: 'uppercase',
                      letterSpacing: 0.5,
                    }}
                  >
                    Readiness
                  </span>
                  <span
                    style={{
                      fontSize: 14,
                      fontWeight: 700,
                      color: getScoreColor(city.readiness_score),
                      fontFamily: "'JetBrains Mono', monospace",
                    }}
                  >
                    {city.readiness_score}/100
                  </span>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
