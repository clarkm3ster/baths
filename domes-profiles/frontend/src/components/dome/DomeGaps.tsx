/**
 * DomeGaps.tsx
 *
 * Visualises gaps (cracks) in the dome:
 * - Fragmented mode: red dashed lines between panels where gaps exist,
 *   crack/break visual at the dome boundary, severity indicators
 * - Coordinated mode: green "healed" lines with bridge labels
 * - Click a gap to see bridge solution
 */

import { useMemo } from 'react';
import type { DomeGap, DomeMode, SystemPosition, SectorGeometry } from './types';

// ---------------------------------------------------------------------------
// Props
// ---------------------------------------------------------------------------

interface DomeGapsProps {
  gaps: DomeGap[];
  systemPositions: Map<string, SystemPosition>;
  sectors: SectorGeometry[];
  cx: number;
  cy: number;
  outerRadius: number;
  mode: DomeMode;
  onGapClick: (gapId: number) => void;
}

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

function polarToCartesian(cx: number, cy: number, r: number, angleDeg: number) {
  const rad = ((angleDeg - 90) * Math.PI) / 180;
  return { x: cx + r * Math.cos(rad), y: cy + r * Math.sin(rad) };
}

function severityStroke(severity: string): number {
  switch (severity.toLowerCase()) {
    case 'critical': return 3;
    case 'high': return 2.5;
    case 'medium': return 1.8;
    case 'low': return 1.2;
    default: return 1.5;
  }
}

function severityDashArray(severity: string): string {
  switch (severity.toLowerCase()) {
    case 'critical': return '6 3';
    case 'high': return '8 4';
    case 'medium': return '5 5';
    case 'low': return '3 6';
    default: return '5 5';
  }
}

// ---------------------------------------------------------------------------
// Crack effect: jagged line segments at dome boundary between sectors
// ---------------------------------------------------------------------------

function crackPath(
  cx: number,
  cy: number,
  outerR: number,
  angle: number,
  severity: string,
): string {
  const depth = severity === 'critical' ? 22 : severity === 'high' ? 16 : 10;
  const jags = severity === 'critical' ? 5 : severity === 'high' ? 4 : 3;
  const pts: string[] = [];
  const start = polarToCartesian(cx, cy, outerR + 4, angle);
  pts.push(`M ${start.x} ${start.y}`);

  for (let i = 1; i <= jags; i++) {
    const ratio = i / jags;
    const inward = outerR - ratio * depth;
    const jitter = (i % 2 === 0 ? 1 : -1) * (3 + Math.random() * 3);
    const pt = polarToCartesian(cx, cy, inward, angle + jitter);
    pts.push(`L ${pt.x} ${pt.y}`);
  }

  return pts.join(' ');
}

// ---------------------------------------------------------------------------
// Component
// ---------------------------------------------------------------------------

export default function DomeGaps({
  gaps,
  systemPositions,
  sectors,
  cx,
  cy,
  outerRadius,
  mode,
  onGapClick,
}: DomeGapsProps) {
  // Build a set of sector boundary angles for crack placement
  const boundaryAngles = useMemo(() => {
    return sectors.map((s) => s.endAngle);
  }, [sectors]);

  // Determine which gaps have both endpoints positioned
  const renderableGaps = useMemo(() => {
    return gaps.filter(
      (g) => systemPositions.has(g.system_a_id) && systemPositions.has(g.system_b_id),
    );
  }, [gaps, systemPositions]);

  const isFragmented = mode === 'fragmented';

  return (
    <g className="dome-gaps">
      {/* Boundary cracks (fragmented mode only) */}
      {isFragmented &&
        boundaryAngles.map((angle, i) => (
          <path
            key={`crack-${i}`}
            d={crackPath(cx, cy, outerRadius, angle, 'high')}
            fill="none"
            stroke="#8B1A1A"
            strokeWidth={2}
            strokeOpacity={0.7}
            strokeLinecap="round"
            style={{
              transition: 'stroke-opacity 800ms ease',
            }}
          />
        ))}

      {/* Gap lines between systems */}
      {renderableGaps.map((gap) => {
        const a = systemPositions.get(gap.system_a_id)!;
        const b = systemPositions.get(gap.system_b_id)!;
        const midX = (a.x + b.x) / 2;
        const midY = (a.y + b.y) / 2;
        const sw = severityStroke(gap.severity);

        if (isFragmented) {
          // --- FRAGMENTED: red dashed crack line ---
          return (
            <g
              key={`gap-${gap.id}`}
              onClick={() => onGapClick(gap.id)}
              style={{ cursor: 'pointer' }}
            >
              <line
                x1={a.x}
                y1={a.y}
                x2={b.x}
                y2={b.y}
                stroke="#8B1A1A"
                strokeWidth={sw}
                strokeDasharray={severityDashArray(gap.severity)}
                strokeOpacity={0.8}
                strokeLinecap="round"
                style={{ transition: 'all 800ms ease' }}
              />
              {/* Severity X mark at midpoint */}
              <g transform={`translate(${midX}, ${midY})`}>
                <line
                  x1={-4}
                  y1={-4}
                  x2={4}
                  y2={4}
                  stroke="#8B1A1A"
                  strokeWidth={2}
                  strokeLinecap="round"
                />
                <line
                  x1={4}
                  y1={-4}
                  x2={-4}
                  y2={4}
                  stroke="#8B1A1A"
                  strokeWidth={2}
                  strokeLinecap="round"
                />
              </g>
              {/* Barrier type label */}
              <text
                x={midX}
                y={midY + 14}
                textAnchor="middle"
                fill="#8B1A1A"
                fontSize={7}
                fontFamily="'JetBrains Mono', monospace"
                fontWeight={600}
              >
                {gap.barrier_type}
              </text>
              {/* Cost to bridge */}
              {gap.cost_to_bridge && (
                <text
                  x={midX}
                  y={midY + 24}
                  textAnchor="middle"
                  fill="#8B1A1A"
                  fontSize={7}
                  fontFamily="'JetBrains Mono', monospace"
                  opacity={0.7}
                >
                  {gap.cost_to_bridge}
                </text>
              )}
              {/* Consent closable badge */}
              {gap.consent_closable && (
                <g>
                  <rect
                    x={midX + 10}
                    y={midY - 14}
                    width={12}
                    height={12}
                    fill="#22c55e"
                    fillOpacity={0.2}
                    stroke="#22c55e"
                    strokeWidth={0.5}
                  />
                  <text
                    x={midX + 16}
                    y={midY - 5}
                    textAnchor="middle"
                    fill="#22c55e"
                    fontSize={8}
                    fontFamily="Inter, sans-serif"
                    fontWeight={700}
                  >
                    C
                  </text>
                </g>
              )}
            </g>
          );
        }

        // --- COORDINATED: green healed bridge line ---
        return (
          <g
            key={`gap-${gap.id}`}
            onClick={() => onGapClick(gap.id)}
            style={{ cursor: 'pointer' }}
          >
            <line
              x1={a.x}
              y1={a.y}
              x2={b.x}
              y2={b.y}
              stroke="#22c55e"
              strokeWidth={sw * 0.8}
              strokeOpacity={0.6}
              strokeLinecap="round"
              style={{ transition: 'all 800ms ease' }}
            />
            {/* Bridge / healed icon: checkmark */}
            <g transform={`translate(${midX}, ${midY})`}>
              <circle r={6} fill="#22c55e" fillOpacity={0.15} stroke="#22c55e" strokeWidth={1} />
              <path
                d="M -3 0 L -1 2 L 3 -2"
                fill="none"
                stroke="#22c55e"
                strokeWidth={1.5}
                strokeLinecap="round"
                strokeLinejoin="round"
              />
            </g>
            {/* Bridge label */}
            <text
              x={midX}
              y={midY + 14}
              textAnchor="middle"
              fill="#22c55e"
              fontSize={7}
              fontFamily="'JetBrains Mono', monospace"
            >
              BRIDGED
            </text>
          </g>
        );
      })}

      {/* Healed boundary glow (coordinated mode) */}
      {!isFragmented &&
        boundaryAngles.map((angle, i) => {
          const inner = polarToCartesian(cx, cy, outerRadius - 8, angle);
          const outer = polarToCartesian(cx, cy, outerRadius + 4, angle);
          return (
            <line
              key={`heal-${i}`}
              x1={inner.x}
              y1={inner.y}
              x2={outer.x}
              y2={outer.y}
              stroke="#22c55e"
              strokeWidth={2}
              strokeOpacity={0.4}
              strokeLinecap="round"
              style={{ transition: 'stroke-opacity 800ms ease' }}
            />
          );
        })}
    </g>
  );
}
