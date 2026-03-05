// -----------------------------------------------------------------
// PhillyActivityMap -- SVG map of Philadelphia with activity dots
// -----------------------------------------------------------------

import { useState } from 'react';
import { Map } from 'lucide-react';
import type { Opportunity } from '../utils/api';

interface Props {
  opportunities: Opportunity[];
  loading: boolean;
}

// Philadelphia bounding box (approximate)
const BOUNDS = {
  minLat: 39.867,
  maxLat: 40.138,
  minLng: -75.28,
  maxLng: -74.955,
};

const MAP_WIDTH = 300;
const MAP_HEIGHT = 360;

// Convert lat/lng to SVG x/y
function project(lat: number, lng: number): { x: number; y: number } {
  const x =
    ((lng - BOUNDS.minLng) / (BOUNDS.maxLng - BOUNDS.minLng)) * MAP_WIDTH;
  const y =
    ((BOUNDS.maxLat - lat) / (BOUNDS.maxLat - BOUNDS.minLat)) * MAP_HEIGHT;
  return { x, y };
}

function scoreColor(score: number): string {
  if (score >= 90) return 'var(--green)';
  if (score >= 75) return 'var(--accent)';
  if (score >= 60) return 'var(--yellow)';
  return 'var(--red)';
}

const PLACEHOLDER_POINTS: Opportunity[] = [];

// Simplified Philadelphia boundary outline (rough polygon)
const PHILLY_OUTLINE = `
  M 140,15
  C 160,10 185,8 210,12
  C 230,18 245,30 255,48
  L 268,80
  C 275,100 278,120 280,140
  L 285,175
  C 282,195 276,220 270,240
  L 260,270
  C 250,290 240,305 225,320
  C 210,338 195,348 175,355
  C 160,358 145,355 130,348
  C 112,340 100,328 88,310
  L 75,280
  C 65,260 58,240 52,218
  L 45,185
  C 42,160 40,140 42,120
  L 48,90
  C 55,65 65,48 80,35
  C 100,22 120,18 140,15
  Z
`;

// Major road lines for visual reference
const ROADS = [
  // Broad St (north-south)
  { x1: 155, y1: 20, x2: 155, y2: 350 },
  // Market St (east-west)
  { x1: 45, y1: 175, x2: 280, y2: 175 },
  // Spring Garden / Vine
  { x1: 55, y1: 140, x2: 270, y2: 140 },
  // Girard Ave
  { x1: 60, y1: 115, x2: 265, y2: 115 },
];

export default function PhillyActivityMap({ opportunities, loading }: Props) {
  const [hoveredId, setHoveredId] = useState<string | null>(null);
  const data = opportunities.length > 0 ? opportunities : PLACEHOLDER_POINTS;

  return (
    <div
      style={{
        background: 'var(--bg-card)',
        border: '1px solid var(--border)',
        borderRadius: 8,
        overflow: 'hidden',
        display: 'flex',
        flexDirection: 'column',
        height: '100%',
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
          flexShrink: 0,
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
          <Map size={12} style={{ color: 'var(--accent)' }} />
          <span
            style={{
              fontSize: 11,
              fontWeight: 600,
              textTransform: 'uppercase',
              letterSpacing: '0.06em',
              color: 'var(--text-secondary)',
            }}
          >
            Philadelphia Activity
          </span>
        </div>
        <span
          style={{
            fontFamily: 'var(--mono)',
            fontSize: 10,
            color: 'var(--text-tertiary)',
          }}
        >
          {data.length} sites
        </span>
      </div>

      {/* Map */}
      <div
        style={{
          flex: 1,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          padding: 12,
          position: 'relative',
          opacity: loading ? 0.4 : 1,
          transition: 'opacity 0.3s ease',
        }}
      >
        <svg
          viewBox={`0 0 ${MAP_WIDTH} ${MAP_HEIGHT}`}
          style={{
            width: '100%',
            maxHeight: '100%',
          }}
        >
          {/* City outline */}
          <path
            d={PHILLY_OUTLINE}
            fill="var(--bg)"
            stroke="var(--border-hover)"
            strokeWidth={1.5}
          />

          {/* Roads */}
          {ROADS.map((road, i) => (
            <line
              key={i}
              x1={road.x1}
              y1={road.y1}
              x2={road.x2}
              y2={road.y2}
              stroke="var(--border)"
              strokeWidth={0.5}
              strokeDasharray="3,3"
              opacity={0.5}
            />
          ))}

          {/* Activity dots */}
          {data.map((opp) => {
            const { x, y } = project(opp.lat, opp.lng);
            const isHovered = hoveredId === opp.id;
            const color = scoreColor(opp.overall_score);
            return (
              <g
                key={opp.id}
                onMouseEnter={() => setHoveredId(opp.id)}
                onMouseLeave={() => setHoveredId(null)}
                style={{ cursor: 'pointer' }}
              >
                {/* Pulse ring */}
                <circle
                  cx={x}
                  cy={y}
                  r={isHovered ? 14 : 8}
                  fill={color}
                  opacity={0.1}
                  style={{ transition: 'r 0.2s ease' }}
                />
                {/* Outer glow */}
                <circle
                  cx={x}
                  cy={y}
                  r={isHovered ? 8 : 5}
                  fill={color}
                  opacity={0.25}
                  style={{ transition: 'r 0.2s ease' }}
                />
                {/* Core dot */}
                <circle
                  cx={x}
                  cy={y}
                  r={isHovered ? 5 : 3}
                  fill={color}
                  style={{ transition: 'r 0.2s ease' }}
                />

                {/* Tooltip on hover */}
                {isHovered && (
                  <g>
                    <rect
                      x={x + 8}
                      y={y - 22}
                      width={120}
                      height={32}
                      rx={4}
                      fill="var(--bg-card)"
                      stroke="var(--border-hover)"
                      strokeWidth={1}
                    />
                    <text
                      x={x + 14}
                      y={y - 8}
                      fill="var(--text)"
                      fontSize={8}
                      fontWeight={600}
                      fontFamily="Inter, sans-serif"
                    >
                      {opp.address.length > 20
                        ? opp.address.slice(0, 20) + '...'
                        : opp.address}
                    </text>
                    <text
                      x={x + 14}
                      y={y + 3}
                      fill="var(--text-tertiary)"
                      fontSize={7}
                      fontFamily="'JetBrains Mono', monospace"
                    >
                      Score: {opp.overall_score} | {opp.recommended_type}
                    </text>
                  </g>
                )}
              </g>
            );
          })}
        </svg>
      </div>

      {/* Legend */}
      <div
        style={{
          display: 'flex',
          justifyContent: 'center',
          gap: 14,
          padding: '8px 14px',
          borderTop: '1px solid var(--border)',
          flexShrink: 0,
        }}
      >
        {[
          { label: '90+', color: 'var(--green)' },
          { label: '75-89', color: 'var(--accent)' },
          { label: '60-74', color: 'var(--yellow)' },
          { label: '<60', color: 'var(--red)' },
        ].map((item) => (
          <div
            key={item.label}
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: 4,
              fontSize: 9,
              color: 'var(--text-tertiary)',
            }}
          >
            <span
              style={{
                width: 6,
                height: 6,
                borderRadius: '50%',
                background: item.color,
                display: 'inline-block',
              }}
            />
            <span style={{ fontFamily: 'var(--mono)' }}>{item.label}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
