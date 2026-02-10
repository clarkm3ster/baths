/**
 * DomeConnections.tsx
 *
 * Renders data-flow connection lines between systems across the dome.
 * - Solid green lines for existing connections
 * - Line thickness based on reliability (high=thick, low=thin)
 * - Animated dots flowing along connections
 * - Format labels (FHIR, HL7, etc.)
 */

import { useMemo } from 'react';
import type { DomeConnection, DomeMode, SystemPosition } from './types';

// ---------------------------------------------------------------------------
// Props
// ---------------------------------------------------------------------------

interface DomeConnectionsProps {
  connections: DomeConnection[];
  systemPositions: Map<string, SystemPosition>;
  mode: DomeMode;
}

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

const RELIABILITY_WIDTH: Record<string, number> = {
  high: 2.5,
  medium: 1.5,
  low: 0.8,
};

function reliabilityWidth(r: string): number {
  return RELIABILITY_WIDTH[r.toLowerCase()] ?? 1.2;
}

function reliabilityColor(r: string, mode: DomeMode): string {
  if (mode === 'fragmented') {
    switch (r.toLowerCase()) {
      case 'high': return '#22c55e';
      case 'medium': return '#a3e635';
      case 'low': return '#fbbf24';
      default: return '#6b7280';
    }
  }
  // Coordinated: all connections are strong green
  return '#22c55e';
}

// ---------------------------------------------------------------------------
// Component
// ---------------------------------------------------------------------------

export default function DomeConnections({
  connections,
  systemPositions,
  mode,
}: DomeConnectionsProps) {
  // Filter to connections where both endpoints have positions
  const renderable = useMemo(() => {
    return connections.filter(
      (c) => systemPositions.has(c.source_id) && systemPositions.has(c.target_id),
    );
  }, [connections, systemPositions]);

  if (renderable.length === 0) return null;

  return (
    <g className="dome-connections">
      {/* Animated dot definition */}
      <defs>
        <circle id="flow-dot" r="2.5" fill="#22c55e" />
        {renderable.map((conn, i) => {
          const src = systemPositions.get(conn.source_id)!;
          const tgt = systemPositions.get(conn.target_id)!;
          return (
            <path
              key={`path-${i}`}
              id={`conn-path-${i}`}
              d={`M ${src.x} ${src.y} Q ${(src.x + tgt.x) / 2 + (src.y - tgt.y) * 0.15} ${(src.y + tgt.y) / 2 + (tgt.x - src.x) * 0.15}, ${tgt.x} ${tgt.y}`}
              fill="none"
            />
          );
        })}
      </defs>

      {renderable.map((conn, i) => {
        const src = systemPositions.get(conn.source_id)!;
        const tgt = systemPositions.get(conn.target_id)!;
        const width = reliabilityWidth(conn.reliability);
        const color = reliabilityColor(conn.reliability, mode);
        const midX = (src.x + tgt.x) / 2 + (src.y - tgt.y) * 0.15;
        const midY = (src.y + tgt.y) / 2 + (tgt.x - src.x) * 0.15;
        const opacity = mode === 'coordinated' ? 0.8 : 0.5;

        return (
          <g key={`conn-${i}`}>
            {/* Connection line (quadratic bezier for visual curve) */}
            <path
              d={`M ${src.x} ${src.y} Q ${midX} ${midY}, ${tgt.x} ${tgt.y}`}
              fill="none"
              stroke={color}
              strokeWidth={mode === 'coordinated' ? width * 1.3 : width}
              strokeOpacity={opacity}
              strokeLinecap="round"
              style={{
                transition: 'stroke-width 800ms ease, stroke-opacity 800ms ease, stroke 800ms ease',
              }}
            />

            {/* Animated flow dot */}
            {mode === 'coordinated' && (
              <circle r="2" fill={color} opacity={0.9}>
                <animateMotion
                  dur={`${2.5 + i * 0.3}s`}
                  repeatCount="indefinite"
                  path={`M ${src.x} ${src.y} Q ${midX} ${midY}, ${tgt.x} ${tgt.y}`}
                />
              </circle>
            )}

            {/* Format label at midpoint */}
            {conn.format && (
              <g>
                <rect
                  x={midX - conn.format.length * 3 - 4}
                  y={midY - 7}
                  width={conn.format.length * 6 + 8}
                  height={14}
                  fill="#000"
                  fillOpacity={0.7}
                  rx={0}
                />
                <text
                  x={midX}
                  y={midY + 3}
                  textAnchor="middle"
                  fill="#fff"
                  fontSize={8}
                  fontFamily="'JetBrains Mono', monospace"
                  opacity={0.9}
                >
                  {conn.format}
                </text>
              </g>
            )}
          </g>
        );
      })}
    </g>
  );
}
