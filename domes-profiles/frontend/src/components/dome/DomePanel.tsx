/**
 * DomePanel.tsx
 *
 * Renders one sector (pie-slice) of the dome for a single domain.
 * Contains the arc path, domain label, system elements positioned along
 * inner arcs, cost labels, provision count badge, and gap count badge.
 */

import { useMemo } from 'react';
import type { DomeDomain, DomeMode, SectorGeometry, SystemPosition } from './types';
import DomeElement from './DomeElement';

// ---------------------------------------------------------------------------
// Props
// ---------------------------------------------------------------------------

interface DomePanelProps {
  domain: DomeDomain;
  sector: SectorGeometry;
  cx: number;
  cy: number;
  outerRadius: number;
  innerRadius: number;
  mode: DomeMode;
  selected: boolean;
  onDomainClick: (domain: string) => void;
  onSystemClick: (systemId: string) => void;
}

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

function polarToCartesian(cx: number, cy: number, r: number, angleDeg: number) {
  const rad = ((angleDeg - 90) * Math.PI) / 180;
  return { x: cx + r * Math.cos(rad), y: cy + r * Math.sin(rad) };
}

function describeArc(
  cx: number,
  cy: number,
  r: number,
  startAngle: number,
  endAngle: number,
): string {
  const start = polarToCartesian(cx, cy, r, endAngle);
  const end = polarToCartesian(cx, cy, r, startAngle);
  const largeArc = endAngle - startAngle > 180 ? 1 : 0;
  return `M ${start.x} ${start.y} A ${r} ${r} 0 ${largeArc} 0 ${end.x} ${end.y}`;
}

function describeSector(
  cx: number,
  cy: number,
  innerR: number,
  outerR: number,
  startAngle: number,
  endAngle: number,
): string {
  const outerStart = polarToCartesian(cx, cy, outerR, endAngle);
  const outerEnd = polarToCartesian(cx, cy, outerR, startAngle);
  const innerStart = polarToCartesian(cx, cy, innerR, startAngle);
  const innerEnd = polarToCartesian(cx, cy, innerR, endAngle);
  const largeArc = endAngle - startAngle > 180 ? 1 : 0;

  return [
    `M ${outerStart.x} ${outerStart.y}`,
    `A ${outerR} ${outerR} 0 ${largeArc} 0 ${outerEnd.x} ${outerEnd.y}`,
    `L ${innerStart.x} ${innerStart.y}`,
    `A ${innerR} ${innerR} 0 ${largeArc} 1 ${innerEnd.x} ${innerEnd.y}`,
    'Z',
  ].join(' ');
}

function formatCost(n: number): string {
  if (n >= 1_000_000) return `$${(n / 1_000_000).toFixed(1)}M`;
  if (n >= 1_000) return `$${(n / 1_000).toFixed(0)}K`;
  return `$${n.toFixed(0)}`;
}

// ---------------------------------------------------------------------------
// Component
// ---------------------------------------------------------------------------

export default function DomePanel({
  domain,
  sector,
  cx,
  cy,
  outerRadius,
  innerRadius,
  mode,
  selected,
  onDomainClick,
  onSystemClick,
}: DomePanelProps) {
  const { startAngle, endAngle, color, midAngle } = sector;

  // Sector path
  const sectorPath = useMemo(
    () => describeSector(cx, cy, innerRadius, outerRadius, startAngle, endAngle),
    [cx, cy, innerRadius, outerRadius, startAngle, endAngle],
  );

  // Outer arc path (for text)
  const labelArcId = `label-arc-${domain.domain}`;
  const labelArc = useMemo(
    () => describeArc(cx, cy, outerRadius + 14, startAngle, endAngle),
    [cx, cy, outerRadius, startAngle, endAngle],
  );

  // Position systems along inner arcs
  const systemPositions: SystemPosition[] = useMemo(() => {
    const systems = domain.systems;
    if (systems.length === 0) return [];
    const arcSpan = endAngle - startAngle;
    const padding = arcSpan * 0.1;
    const usable = arcSpan - padding * 2;
    const step = systems.length > 1 ? usable / (systems.length - 1) : 0;
    const systemRadius = innerRadius + (outerRadius - innerRadius) * 0.55;

    return systems.map((sys, i) => {
      const angle = startAngle + padding + (systems.length > 1 ? step * i : usable / 2);
      const pos = polarToCartesian(cx, cy, systemRadius, angle);
      return { system: sys, x: pos.x, y: pos.y, angle, domain: domain.domain };
    });
  }, [domain.systems, startAngle, endAngle, innerRadius, outerRadius, cx, cy, domain.domain]);

  // Cost label position
  const costPos = useMemo(
    () => polarToCartesian(cx, cy, innerRadius + (outerRadius - innerRadius) * 0.25, midAngle),
    [cx, cy, innerRadius, outerRadius, midAngle],
  );

  // Badge positions
  const provBadgePos = useMemo(
    () => polarToCartesian(cx, cy, outerRadius - 18, startAngle + (endAngle - startAngle) * 0.85),
    [cx, cy, outerRadius, startAngle, endAngle],
  );
  const gapBadgePos = useMemo(
    () => polarToCartesian(cx, cy, outerRadius - 18, startAngle + (endAngle - startAngle) * 0.15),
    [cx, cy, outerRadius, startAngle, endAngle],
  );

  const cost = mode === 'fragmented' ? domain.annual_cost : domain.coordinated_cost;
  const fillOpacity = selected ? 0.16 : 0.08;
  const strokeWidth = selected ? 2.5 : 1;

  return (
    <g
      className="dome-panel"
      onClick={() => onDomainClick(domain.domain)}
      style={{ cursor: 'pointer' }}
    >
      {/* Sector fill */}
      <path
        d={sectorPath}
        fill={color}
        fillOpacity={fillOpacity}
        stroke={color}
        strokeWidth={strokeWidth}
        strokeOpacity={mode === 'fragmented' ? 0.5 : 0.9}
        style={{
          transition: 'fill-opacity 800ms ease, stroke-width 300ms ease, stroke-opacity 800ms ease',
        }}
      />

      {/* Domain label along outer arc */}
      <defs>
        <path id={labelArcId} d={labelArc} />
      </defs>
      <text
        fill={color}
        fontSize={12}
        fontFamily="'Crimson Text', serif"
        fontWeight={700}
        letterSpacing="0.5px"
      >
        <textPath
          href={`#${labelArcId}`}
          startOffset="50%"
          textAnchor="middle"
        >
          {domain.label.toUpperCase()}
        </textPath>
      </text>

      {/* Cost in center of panel */}
      <text
        x={costPos.x}
        y={costPos.y}
        textAnchor="middle"
        dominantBaseline="middle"
        fill={color}
        fontSize={13}
        fontFamily="'JetBrains Mono', monospace"
        fontWeight={700}
        style={{ transition: 'all 800ms ease' }}
      >
        {formatCost(cost)}
      </text>
      <text
        x={costPos.x}
        y={costPos.y + 14}
        textAnchor="middle"
        dominantBaseline="middle"
        fill={color}
        fontSize={8}
        fontFamily="Inter, sans-serif"
        opacity={0.6}
      >
        /year
      </text>

      {/* Systems */}
      {systemPositions.map((sp) => (
        <DomeElement
          key={sp.system.id}
          system={sp.system}
          x={sp.x}
          y={sp.y}
          color={color}
          mode={mode}
          onClick={onSystemClick}
        />
      ))}

      {/* Provisions count badge */}
      {domain.provisions_count > 0 && (
        <g>
          <rect
            x={provBadgePos.x - 14}
            y={provBadgePos.y - 8}
            width={28}
            height={16}
            fill={color}
            fillOpacity={0.15}
            stroke={color}
            strokeWidth={0.5}
          />
          <text
            x={provBadgePos.x}
            y={provBadgePos.y + 1}
            textAnchor="middle"
            dominantBaseline="middle"
            fill={color}
            fontSize={8}
            fontFamily="'JetBrains Mono', monospace"
          >
            {domain.provisions_count}p
          </text>
        </g>
      )}

      {/* Gap count badge (red warning) */}
      {domain.gaps_count > 0 && mode === 'fragmented' && (
        <g>
          <rect
            x={gapBadgePos.x - 14}
            y={gapBadgePos.y - 8}
            width={28}
            height={16}
            fill="#8B1A1A"
            fillOpacity={0.2}
            stroke="#8B1A1A"
            strokeWidth={1}
          />
          <text
            x={gapBadgePos.x}
            y={gapBadgePos.y + 1}
            textAnchor="middle"
            dominantBaseline="middle"
            fill="#8B1A1A"
            fontSize={8}
            fontFamily="'JetBrains Mono', monospace"
            fontWeight={700}
          >
            {domain.gaps_count}!
          </text>
        </g>
      )}
    </g>
  );
}
