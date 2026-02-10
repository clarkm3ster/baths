/**
 * DomeVisualization.tsx
 *
 * THE CROWN JEWEL of the DOMES project.
 *
 * An architectural visualization of a dome/rotunda viewed from above.
 * The person is at the center. The dome is divided into panels (sectors)
 * by domain. Each panel contains systems, legal provisions, costs, and
 * data flows for that domain.
 *
 * FRAGMENTED view: Dome is CRACKED. Panels have gaps between them (red
 * dashed borders). Systems are disconnected. Costs are high. The dome
 * looks broken.
 *
 * COORDINATED view: Dome is WHOLE. Panels connect with solid lines.
 * Systems communicate. Costs are lower. The dome is intact and functional.
 *
 * Pure SVG, no D3. Uses ResizeObserver + hasSize guard pattern.
 */

import { useRef, useState, useEffect, useMemo } from 'react';
import type {
  DomeDomain,
  DomeConnection,
  DomeGap,
  DomeTotals,
  DomeMode,
  SectorGeometry,
  SystemPosition,
} from './types';
import DomePanel from './DomePanel';
import DomeConnections from './DomeConnections';
import DomeGaps from './DomeGaps';
import DomeTransition from './DomeTransition';
import DomeLegend from './DomeLegend';
import DomeExport from './DomeExport';

// ---------------------------------------------------------------------------
// Props
// ---------------------------------------------------------------------------

interface DomeProps {
  domains: DomeDomain[];
  connections: DomeConnection[];
  gaps?: DomeGap[];
  totals: DomeTotals;
  mode: DomeMode;
  onModeChange?: (mode: DomeMode) => void;
  /** Accepts either a domain key string or the full DomeDomain object */
  onDomainClick?: ((domain: string) => void) | ((domain: DomeDomain) => void);
  onSystemClick?: (systemId: string) => void;
  onGapClick?: (gapId: number) => void;
  selectedDomain?: string;
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

function formatCost(n: number): string {
  if (n >= 1_000_000) return `$${(n / 1_000_000).toFixed(1)}M`;
  if (n >= 1_000) return `$${Math.round(n / 1_000)}K`;
  return `$${Math.round(n)}`;
}

// ---------------------------------------------------------------------------
// Dome boundary path (full or fragmented)
// ---------------------------------------------------------------------------

function domeBoundaryPath(
  cx: number,
  cy: number,
  r: number,
  sectors: SectorGeometry[],
  mode: DomeMode,
): string {
  if (mode === 'coordinated' || sectors.length === 0) {
    // Full circle
    return [
      `M ${cx + r} ${cy}`,
      `A ${r} ${r} 0 1 1 ${cx - r} ${cy}`,
      `A ${r} ${r} 0 1 1 ${cx + r} ${cy}`,
    ].join(' ');
  }

  // Fragmented: arcs with gaps at sector boundaries
  const parts: string[] = [];
  const gapDeg = 3; // degrees of gap

  sectors.forEach((s) => {
    const arcStart = s.startAngle + gapDeg / 2;
    const arcEnd = s.endAngle - gapDeg / 2;
    if (arcEnd <= arcStart) return;
    const arc = describeArc(cx, cy, r, arcStart, arcEnd);
    parts.push(arc);
  });

  return parts.join(' ');
}

// ---------------------------------------------------------------------------
// Person icon (center of dome)
// ---------------------------------------------------------------------------

function PersonIcon({ cx, cy, scale = 1 }: { cx: number; cy: number; scale?: number }) {
  const s = scale;
  return (
    <g transform={`translate(${cx}, ${cy}) scale(${s})`}>
      {/* Head */}
      <circle cx={0} cy={-10} r={6} fill="none" stroke="#000" strokeWidth={1.5} />
      {/* Body */}
      <line x1={0} y1={-4} x2={0} y2={8} stroke="#000" strokeWidth={1.5} />
      {/* Arms */}
      <line x1={-8} y1={1} x2={8} y2={1} stroke="#000" strokeWidth={1.5} />
      {/* Legs */}
      <line x1={0} y1={8} x2={-6} y2={16} stroke="#000" strokeWidth={1.5} />
      <line x1={0} y1={8} x2={6} y2={16} stroke="#000" strokeWidth={1.5} />
    </g>
  );
}

// ---------------------------------------------------------------------------
// Concentric ring guides
// ---------------------------------------------------------------------------

function ConcentricRings({
  cx,
  cy,
  outerR,
  innerR,
  rings,
}: {
  cx: number;
  cy: number;
  outerR: number;
  innerR: number;
  rings: number;
}) {
  const step = (outerR - innerR) / rings;
  return (
    <g className="dome-rings" opacity={0.06}>
      {Array.from({ length: rings }, (_, i) => (
        <circle
          key={i}
          cx={cx}
          cy={cy}
          r={innerR + step * (i + 1)}
          fill="none"
          stroke="#000"
          strokeWidth={0.5}
        />
      ))}
    </g>
  );
}

// ---------------------------------------------------------------------------
// Radial guide lines (sector dividers)
// ---------------------------------------------------------------------------

function RadialGuides({
  cx,
  cy,
  innerR,
  outerR,
  sectors,
  mode,
}: {
  cx: number;
  cy: number;
  innerR: number;
  outerR: number;
  sectors: SectorGeometry[];
  mode: DomeMode;
}) {
  return (
    <g className="dome-radials">
      {sectors.map((s, i) => {
        const inner = polarToCartesian(cx, cy, innerR, s.startAngle);
        const outer = polarToCartesian(cx, cy, outerR + 4, s.startAngle);
        return (
          <line
            key={i}
            x1={inner.x}
            y1={inner.y}
            x2={outer.x}
            y2={outer.y}
            stroke={mode === 'fragmented' ? '#8B1A1A' : '#000'}
            strokeWidth={mode === 'fragmented' ? 1 : 0.5}
            strokeOpacity={mode === 'fragmented' ? 0.4 : 0.15}
            strokeDasharray={mode === 'fragmented' ? '4 3' : 'none'}
            style={{ transition: 'all 800ms ease' }}
          />
        );
      })}
    </g>
  );
}

// ---------------------------------------------------------------------------
// Main Component
// ---------------------------------------------------------------------------

export default function DomeVisualization({
  domains,
  connections,
  gaps: gapsProp,
  totals,
  mode,
  onModeChange,
  onDomainClick,
  onSystemClick,
  onGapClick,
  selectedDomain,
}: DomeProps) {
  // ---- Internal state for mode when onModeChange not provided ----
  const [internalMode, setInternalMode] = useState<DomeMode>(mode);
  const effectiveMode = onModeChange ? mode : internalMode;
  const handleModeChange = onModeChange ?? setInternalMode;

  // ---- Build gaps from domain gap data if not provided directly ----
  const gaps: DomeGap[] = useMemo(() => {
    if (gapsProp) return gapsProp;
    // Derive from domain.gaps
    const result: DomeGap[] = [];
    domains.forEach((d) => {
      d.gaps?.forEach((g) => {
        result.push({
          id: g.id,
          system_a_id: g.system_a,
          system_b_id: g.system_b,
          system_a_name: g.system_a,
          system_b_name: g.system_b,
          barrier_type: g.barrier_type,
          severity: g.severity,
          consent_closable: g.consent_closable,
          cost_to_bridge: '',
        });
      });
    });
    return result;
  }, [gapsProp, domains]);

  // ---- Wrap onDomainClick to support both signatures ----
  const handleDomainClick = useMemo(() => {
    if (!onDomainClick) return (_key: string) => {};
    return (domainKey: string) => {
      const domainObj = domains.find((d) => d.domain === domainKey);
      // Try calling with string first; if the caller expects an object it will
      // receive the object. We unify by always passing the object when available.
      if (domainObj) {
        (onDomainClick as (arg: DomeDomain | string) => void)(domainObj);
      } else {
        (onDomainClick as (arg: string) => void)(domainKey);
      }
    };
  }, [onDomainClick, domains]);

  const handleSystemClick = onSystemClick ?? (() => {});
  const handleGapClick = onGapClick ?? (() => {});

  // ---- ResizeObserver pattern ----
  const containerRef = useRef<HTMLDivElement>(null);
  const svgRef = useRef<SVGSVGElement>(null);
  const [size, setSize] = useState({ w: 0, h: 0 });

  useEffect(() => {
    if (!containerRef.current) return;
    const obs = new ResizeObserver((entries) => {
      const { width, height } = entries[0].contentRect;
      setSize({ w: width, h: height });
    });
    obs.observe(containerRef.current);
    return () => obs.disconnect();
  }, []);

  const hasSize = size.w > 0 && size.h > 0;

  // ---- Geometry calculations ----
  const svgWidth = Math.max(size.w, 600);
  const svgHeight = Math.max(Math.min(svgWidth * 0.85, size.h || 700), 500);
  const cx = svgWidth / 2;
  const cy = svgHeight / 2;
  const outerRadius = Math.min(svgWidth, svgHeight) / 2 - 40;
  const innerRadius = outerRadius * 0.22;

  // ---- Sector geometry ----
  const sectors: SectorGeometry[] = useMemo(() => {
    if (domains.length === 0) return [];
    const sliceAngle = 360 / domains.length;
    return domains.map((d, i) => ({
      domain: d.domain,
      startAngle: i * sliceAngle,
      endAngle: (i + 1) * sliceAngle,
      midAngle: i * sliceAngle + sliceAngle / 2,
      color: d.color,
      label: d.label,
    }));
  }, [domains]);

  // ---- System positions (for connections/gaps to reference) ----
  const systemPositions: Map<string, SystemPosition> = useMemo(() => {
    const map = new Map<string, SystemPosition>();
    sectors.forEach((sector) => {
      const domain = domains.find((d) => d.domain === sector.domain);
      if (!domain) return;
      const systems = domain.systems;
      if (systems.length === 0) return;
      const arcSpan = sector.endAngle - sector.startAngle;
      const padding = arcSpan * 0.1;
      const usable = arcSpan - padding * 2;
      const step = systems.length > 1 ? usable / (systems.length - 1) : 0;
      const systemRadius = innerRadius + (outerRadius - innerRadius) * 0.55;

      systems.forEach((sys, idx) => {
        const angle =
          sector.startAngle +
          padding +
          (systems.length > 1 ? step * idx : usable / 2);
        const pos = polarToCartesian(cx, cy, systemRadius, angle);
        map.set(sys.id, {
          system: sys,
          x: pos.x,
          y: pos.y,
          angle,
          domain: domain.domain,
        });
      });
    });
    return map;
  }, [sectors, domains, innerRadius, outerRadius, cx, cy]);

  // ---- Dome boundary ----
  const boundaryPath = useMemo(
    () => domeBoundaryPath(cx, cy, outerRadius, sectors, effectiveMode),
    [cx, cy, outerRadius, sectors, effectiveMode],
  );

  // ---- Cost display ----
  const centerCost = effectiveMode === 'fragmented' ? totals.annual_cost : totals.coordinated_cost;

  return (
    <div className="flex flex-col items-center gap-4 w-full">
      {/* Header controls: transition toggle + export */}
      <div className="w-full flex flex-col items-center gap-3">
        <DomeTransition mode={effectiveMode} onModeChange={handleModeChange} totals={totals} />
      </div>

      {/* Main dome area */}
      <div className="w-full flex gap-4">
        {/* SVG container */}
        <div
          ref={containerRef}
          className="flex-1 border border-black bg-white"
          style={{ minHeight: 500, minWidth: 600, position: 'relative' }}
        >
          {hasSize && (
            <svg
              ref={svgRef}
              width={svgWidth}
              height={svgHeight}
              viewBox={`0 0 ${svgWidth} ${svgHeight}`}
              xmlns="http://www.w3.org/2000/svg"
              style={{ display: 'block' }}
            >
              {/* Background pattern: subtle grid */}
              <defs>
                <pattern
                  id="dome-grid"
                  width="20"
                  height="20"
                  patternUnits="userSpaceOnUse"
                >
                  <path
                    d="M 20 0 L 0 0 0 20"
                    fill="none"
                    stroke="#000"
                    strokeWidth="0.15"
                    strokeOpacity="0.08"
                  />
                </pattern>
                {/* Glow filter for coordinated mode */}
                <filter id="dome-glow" x="-20%" y="-20%" width="140%" height="140%">
                  <feGaussianBlur in="SourceGraphic" stdDeviation="3" result="blur" />
                  <feMerge>
                    <feMergeNode in="blur" />
                    <feMergeNode in="SourceGraphic" />
                  </feMerge>
                </filter>
                {/* Drop shadow for selected state */}
                <filter id="dome-shadow" x="-10%" y="-10%" width="120%" height="120%">
                  <feDropShadow dx="0" dy="2" stdDeviation="3" floodColor="#000" floodOpacity="0.15" />
                </filter>
              </defs>

              {/* Grid background */}
              <rect width={svgWidth} height={svgHeight} fill="url(#dome-grid)" />

              {/* Concentric ring guides */}
              <ConcentricRings
                cx={cx}
                cy={cy}
                outerR={outerRadius}
                innerR={innerRadius}
                rings={4}
              />

              {/* Radial sector dividers */}
              <RadialGuides
                cx={cx}
                cy={cy}
                innerR={innerRadius}
                outerR={outerRadius}
                sectors={sectors}
                mode={effectiveMode}
              />

              {/* Dome boundary */}
              <path
                d={boundaryPath}
                fill="none"
                stroke={effectiveMode === 'fragmented' ? '#8B1A1A' : '#000'}
                strokeWidth={effectiveMode === 'fragmented' ? 2 : 2.5}
                strokeOpacity={effectiveMode === 'fragmented' ? 0.6 : 0.9}
                strokeDasharray={effectiveMode === 'fragmented' ? '8 4' : 'none'}
                style={{
                  transition: 'stroke 800ms ease, stroke-width 800ms ease, stroke-dasharray 800ms ease, stroke-opacity 800ms ease',
                }}
              />

              {/* Inner circle (person boundary) */}
              <circle
                cx={cx}
                cy={cy}
                r={innerRadius}
                fill="#fff"
                stroke={effectiveMode === 'fragmented' ? '#8B1A1A' : '#000'}
                strokeWidth={1.5}
                strokeOpacity={0.4}
                strokeDasharray={effectiveMode === 'fragmented' ? '3 3' : 'none'}
                style={{ transition: 'all 800ms ease' }}
              />

              {/* Domain panels (sectors) */}
              {sectors.map((sector) => {
                const domain = domains.find((d) => d.domain === sector.domain);
                if (!domain) return null;
                return (
                  <DomePanel
                    key={sector.domain}
                    domain={domain}
                    sector={sector}
                    cx={cx}
                    cy={cy}
                    outerRadius={outerRadius}
                    innerRadius={innerRadius}
                    mode={effectiveMode}
                    selected={selectedDomain === sector.domain}
                    onDomainClick={handleDomainClick}
                    onSystemClick={handleSystemClick}
                  />
                );
              })}

              {/* Connections layer */}
              <DomeConnections
                connections={connections}
                systemPositions={systemPositions}
                mode={effectiveMode}
              />

              {/* Gaps layer */}
              <DomeGaps
                gaps={gaps}
                systemPositions={systemPositions}
                sectors={sectors}
                cx={cx}
                cy={cy}
                outerRadius={outerRadius}
                mode={effectiveMode}
                onGapClick={handleGapClick}
              />

              {/* Outer glow ring (coordinated mode) */}
              {effectiveMode === 'coordinated' && (
                <circle
                  cx={cx}
                  cy={cy}
                  r={outerRadius + 6}
                  fill="none"
                  stroke="#22c55e"
                  strokeWidth={1.5}
                  strokeOpacity={0.25}
                  filter="url(#dome-glow)"
                  style={{ transition: 'stroke-opacity 800ms ease' }}
                />
              )}

              {/* Fragmented outer distress ring */}
              {effectiveMode === 'fragmented' && (
                <circle
                  cx={cx}
                  cy={cy}
                  r={outerRadius + 6}
                  fill="none"
                  stroke="#8B1A1A"
                  strokeWidth={1}
                  strokeOpacity={0.2}
                  strokeDasharray="2 6"
                  style={{ transition: 'stroke-opacity 800ms ease' }}
                />
              )}

              {/* ========== CENTER: Person + Cost ========== */}
              <g className="dome-center">
                {/* Person icon */}
                <PersonIcon cx={cx} cy={cy - 14} scale={1.2} />

                {/* Total cost */}
                <text
                  x={cx}
                  y={cy + 20}
                  textAnchor="middle"
                  dominantBaseline="middle"
                  fill={effectiveMode === 'fragmented' ? '#8B1A1A' : '#1A6B3C'}
                  fontSize={18}
                  fontFamily="'JetBrains Mono', monospace"
                  fontWeight={700}
                  style={{ transition: 'fill 800ms ease' }}
                >
                  {formatCost(centerCost)}
                </text>
                <text
                  x={cx}
                  y={cy + 35}
                  textAnchor="middle"
                  dominantBaseline="middle"
                  fill="#666"
                  fontSize={9}
                  fontFamily="Inter, sans-serif"
                >
                  per year
                </text>

                {/* Savings callout (always visible) */}
                <text
                  x={cx}
                  y={cy + 50}
                  textAnchor="middle"
                  dominantBaseline="middle"
                  fill="#22c55e"
                  fontSize={11}
                  fontFamily="'JetBrains Mono', monospace"
                  fontWeight={600}
                  opacity={effectiveMode === 'coordinated' ? 1 : 0.5}
                  style={{ transition: 'opacity 800ms ease' }}
                >
                  {effectiveMode === 'coordinated'
                    ? `SAVING ${formatCost(totals.savings)}`
                    : `${formatCost(totals.savings)} possible`}
                </text>
              </g>

              {/* Mode label at top */}
              <text
                x={cx}
                y={20}
                textAnchor="middle"
                fill={effectiveMode === 'fragmented' ? '#8B1A1A' : '#1A6B3C'}
                fontSize={11}
                fontFamily="'JetBrains Mono', monospace"
                fontWeight={700}
                letterSpacing="3px"
                style={{ transition: 'fill 800ms ease' }}
              >
                {effectiveMode === 'fragmented' ? 'FRAGMENTED' : 'COORDINATED'}
              </text>

              {/* Systems count at bottom */}
              <text
                x={cx}
                y={svgHeight - 10}
                textAnchor="middle"
                fill="#999"
                fontSize={9}
                fontFamily="'JetBrains Mono', monospace"
              >
                {totals.systems_count} systems | {totals.gaps_count} gaps | {totals.consent_closable} consent-closable
              </text>
            </svg>
          )}

          {/* Loading placeholder */}
          {!hasSize && (
            <div
              className="flex items-center justify-center"
              style={{ minHeight: 500, fontFamily: "'JetBrains Mono', monospace", color: '#999' }}
            >
              Initializing dome...
            </div>
          )}
        </div>

        {/* Side panel: Legend */}
        <div className="shrink-0 hidden lg:block">
          <DomeLegend />
        </div>
      </div>

      {/* Footer: Export */}
      <div className="w-full flex justify-between items-center">
        <DomeExport svgRef={svgRef} />

        {/* Mobile legend toggle */}
        <div className="lg:hidden">
          <MobileLegendToggle />
        </div>
      </div>
    </div>
  );
}

// ---------------------------------------------------------------------------
// Mobile legend toggle (shown on small screens)
// ---------------------------------------------------------------------------

function MobileLegendToggle() {
  const [open, setOpen] = useState(false);

  return (
    <div className="relative">
      <button
        onClick={() => setOpen(!open)}
        className="px-3 py-1.5 text-xs border border-black bg-white text-black hover:bg-black hover:text-white transition-colors duration-200"
        style={{ fontFamily: "'JetBrains Mono', monospace" }}
      >
        {open ? 'HIDE LEGEND' : 'SHOW LEGEND'}
      </button>
      {open && (
        <div className="absolute right-0 bottom-10 z-50 bg-white shadow-lg">
          <DomeLegend />
        </div>
      )}
    </div>
  );
}
