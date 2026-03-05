import { useMemo, useState, useRef, useEffect, useCallback } from "react";
import type { System, Connection, Gap, Domain } from "../types";
import { DOMAIN_COLORS, DOMAIN_LABELS } from "../types";

interface Props {
  systems: System[];
  connections: Connection[];
  gaps: Gap[];
  onSystemClick: (system: System) => void;
  onGapClick: (gap: Gap) => void;
  onConnectionClick: (connection: Connection) => void;
  selectedId?: string | number;
}

interface NodePosition {
  x: number;
  y: number;
  system: System;
}

const DOMAIN_ORDER: Domain[] = [
  "health",
  "justice",
  "housing",
  "income",
  "education",
  "child_welfare",
];

export default function ConstellationView({
  systems,
  connections,
  gaps,
  onSystemClick,
  onGapClick,
  onConnectionClick,
  selectedId,
}: Props) {
  const [hoveredId, setHoveredId] = useState<string | null>(null);
  const containerRef = useRef<HTMLDivElement>(null);
  const [dims, setDims] = useState({ w: 0, h: 0 });

  // Measure container immediately + on resize
  const measure = useCallback(() => {
    const el = containerRef.current;
    if (!el) return;
    const rect = el.getBoundingClientRect();
    if (rect.width > 0 && rect.height > 0) {
      setDims({ w: rect.width, h: rect.height });
    }
  }, []);

  useEffect(() => {
    // Initial measurement after layout
    measure();
    // Also measure after a short delay for flex layout settling
    const timer = setTimeout(measure, 50);

    const el = containerRef.current;
    if (!el) return;
    const obs = new ResizeObserver((entries) => {
      const { width, height } = entries[0].contentRect;
      if (width > 0 && height > 0) {
        setDims({ w: width, h: height });
      }
    });
    obs.observe(el);
    return () => {
      obs.disconnect();
      clearTimeout(timer);
    };
  }, [measure]);

  // Don't render SVG until we have real dimensions
  const hasSize = dims.w > 0 && dims.h > 0;

  const CX = dims.w / 2;
  const CY = dims.h / 2;
  const RADIUS_SCALE = Math.min(dims.w, dims.h) / 2;

  const nodePositions = useMemo(() => {
    if (!hasSize) return new Map<string, NodePosition>();

    const positions = new Map<string, NodePosition>();
    const domainGroups = new Map<Domain, System[]>();

    for (const s of systems) {
      const d = s.domain as Domain;
      if (!domainGroups.has(d)) domainGroups.set(d, []);
      domainGroups.get(d)!.push(s);
    }

    const activeDomains = DOMAIN_ORDER.filter((d) => domainGroups.has(d));
    const domainCount = activeDomains.length;

    activeDomains.forEach((domain, di) => {
      const group = domainGroups.get(domain)!;
      const domainAngle = (di / domainCount) * Math.PI * 2 - Math.PI / 2;

      group.forEach((system, si) => {
        const count = group.length;
        const innerFrac = 0.38;
        const outerFrac = 0.75;
        const rFrac =
          count === 1
            ? 0.56
            : innerFrac + (si / (count - 1)) * (outerFrac - innerFrac);
        const r = rFrac * RADIUS_SCALE;
        const spread = (Math.PI * 0.32) / Math.max(count - 1, 1);
        const offset = count === 1 ? 0 : (si - (count - 1) / 2) * spread;
        const angle = domainAngle + offset;

        positions.set(system.id, {
          x: CX + Math.cos(angle) * r,
          y: CY + Math.sin(angle) * r,
          system,
        });
      });
    });

    return positions;
  }, [systems, CX, CY, RADIUS_SCALE, hasSize]);

  const systemIsInvolved = (sysId: string) =>
    hoveredId === sysId ||
    connections.some(
      (c) =>
        (c.source_id === hoveredId && c.target_id === sysId) ||
        (c.target_id === hoveredId && c.source_id === sysId)
    ) ||
    gaps.some(
      (g) =>
        (g.system_a_id === hoveredId && g.system_b_id === sysId) ||
        (g.system_b_id === hoveredId && g.system_a_id === sysId)
    );

  const nodeR = Math.max(20, Math.min(32, RADIUS_SCALE * 0.09));
  const personR = Math.max(22, Math.min(34, RADIUS_SCALE * 0.1));
  const labelR = RADIUS_SCALE * 0.88;

  return (
    <div className="constellation-wrapper" ref={containerRef}>
      {hasSize && (
        <svg
          viewBox={`0 0 ${dims.w} ${dims.h}`}
          xmlns="http://www.w3.org/2000/svg"
        >
          <defs>
            {/* Tick marks for orbit rings */}
            <pattern
              id="grid-dots"
              width="40"
              height="40"
              patternUnits="userSpaceOnUse"
            >
              <circle cx="20" cy="20" r="0.5" fill="#DDDDDD" />
            </pattern>
          </defs>

          {/* Subtle background grid for scientific feel */}
          <rect width={dims.w} height={dims.h} fill="url(#grid-dots)" />

          {/* Crosshair at center */}
          <line
            x1={CX - 12}
            y1={CY}
            x2={CX + 12}
            y2={CY}
            stroke="#CCCCCC"
            strokeWidth="0.5"
          />
          <line
            x1={CX}
            y1={CY - 12}
            x2={CX}
            y2={CY + 12}
            stroke="#CCCCCC"
            strokeWidth="0.5"
          />

          {/* Orbit rings -- faint concentric circles */}
          {[0.38, 0.56, 0.75].map((frac) => (
            <circle
              key={frac}
              cx={CX}
              cy={CY}
              r={frac * RADIUS_SCALE}
              fill="none"
              stroke="#E8E8E8"
              strokeWidth="0.5"
              strokeDasharray="2 6"
            />
          ))}

          {/* Domain sector labels */}
          {(() => {
            const domainGroups = new Map<Domain, System[]>();
            for (const s of systems) {
              const d = s.domain as Domain;
              if (!domainGroups.has(d)) domainGroups.set(d, []);
              domainGroups.get(d)!.push(s);
            }
            const activeDomains = DOMAIN_ORDER.filter((d) =>
              domainGroups.has(d)
            );
            return activeDomains.map((domain, di) => {
              const angle =
                (di / activeDomains.length) * Math.PI * 2 - Math.PI / 2;
              const lx = CX + Math.cos(angle) * labelR;
              const ly = CY + Math.sin(angle) * labelR;

              // Faint radial line from center toward sector label
              const lineR = RADIUS_SCALE * 0.82;
              const lineX = CX + Math.cos(angle) * lineR;
              const lineY = CY + Math.sin(angle) * lineR;

              return (
                <g key={domain}>
                  <line
                    x1={CX + Math.cos(angle) * (personR + 20)}
                    y1={CY + Math.sin(angle) * (personR + 20)}
                    x2={lineX}
                    y2={lineY}
                    stroke="#F0F0F0"
                    strokeWidth="0.5"
                  />
                  <text
                    x={lx}
                    y={ly}
                    textAnchor="middle"
                    dominantBaseline="central"
                    fill={DOMAIN_COLORS[domain]}
                    fontSize={Math.max(9, RADIUS_SCALE * 0.038)}
                    fontFamily="var(--font-sans)"
                    fontWeight="600"
                    letterSpacing="0.08em"
                    opacity="0.7"
                    style={{ textTransform: "uppercase" }}
                  >
                    {DOMAIN_LABELS[domain]}
                  </text>
                </g>
              );
            });
          })()}

          {/* Connection lines -- solid */}
          {connections.map((c) => {
            const a = nodePositions.get(c.source_id);
            const b = nodePositions.get(c.target_id);
            if (!a || !b) return null;
            const isHovered =
              hoveredId === c.source_id || hoveredId === c.target_id;
            return (
              <line
                key={`conn-${c.id}`}
                x1={a.x}
                y1={a.y}
                x2={b.x}
                y2={b.y}
                stroke="#333333"
                strokeWidth={isHovered ? 2.5 : 1.5}
                opacity={hoveredId ? (isHovered ? 0.8 : 0.08) : 0.3}
                style={{ cursor: "pointer", transition: "opacity 0.15s" }}
                onClick={() => onConnectionClick(c)}
              />
            );
          })}

          {/* Gap lines -- dashed red */}
          {gaps.map((g) => {
            const a = nodePositions.get(g.system_a_id);
            const b = nodePositions.get(g.system_b_id);
            if (!a || !b) return null;
            const isHovered =
              hoveredId === g.system_a_id || hoveredId === g.system_b_id;
            const color = g.consent_closable
              ? "#006600"
              : g.severity === "critical"
                ? "#CC0000"
                : g.severity === "high"
                  ? "#994400"
                  : "#888800";
            return (
              <g key={`gap-${g.id}`}>
                <line
                  x1={a.x}
                  y1={a.y}
                  x2={b.x}
                  y2={b.y}
                  stroke={color}
                  strokeWidth={isHovered ? 2.5 : 1.5}
                  strokeDasharray={g.consent_closable ? "8 5" : "4 4"}
                  opacity={hoveredId ? (isHovered ? 0.9 : 0.06) : 0.4}
                  style={{ cursor: "pointer", transition: "opacity 0.15s" }}
                  onClick={() => onGapClick(g)}
                />
                {/* Gap marker at midpoint */}
                {(!hoveredId || isHovered) && (
                  <g
                    style={{ cursor: "pointer", pointerEvents: "none" }}
                    opacity={hoveredId ? 1 : 0.5}
                  >
                    {g.consent_closable ? (
                      // Small triangle for consent-closable
                      <polygon
                        points={`${(a.x + b.x) / 2},${(a.y + b.y) / 2 - 5} ${(a.x + b.x) / 2 - 4.5},${(a.y + b.y) / 2 + 3} ${(a.x + b.x) / 2 + 4.5},${(a.y + b.y) / 2 + 3}`}
                        fill="none"
                        stroke={color}
                        strokeWidth="1.2"
                      />
                    ) : (
                      // Small X for blocked gap
                      <g>
                        <line
                          x1={(a.x + b.x) / 2 - 4}
                          y1={(a.y + b.y) / 2 - 4}
                          x2={(a.x + b.x) / 2 + 4}
                          y2={(a.y + b.y) / 2 + 4}
                          stroke={color}
                          strokeWidth="1.5"
                        />
                        <line
                          x1={(a.x + b.x) / 2 + 4}
                          y1={(a.y + b.y) / 2 - 4}
                          x2={(a.x + b.x) / 2 - 4}
                          y2={(a.y + b.y) / 2 + 4}
                          stroke={color}
                          strokeWidth="1.5"
                        />
                      </g>
                    )}
                  </g>
                )}
              </g>
            );
          })}

          {/* Person at center -- silhouette */}
          <circle cx={CX} cy={CY} r={personR} fill="#000" />
          {/* Simple person icon */}
          <circle
            cx={CX}
            cy={CY - personR * 0.22}
            r={personR * 0.25}
            fill="#FFFFFF"
          />
          <ellipse
            cx={CX}
            cy={CY + personR * 0.3}
            rx={personR * 0.35}
            ry={personR * 0.22}
            fill="#FFFFFF"
          />
          {/* "YOU" label below person */}
          <text
            x={CX}
            y={CY + personR + 14}
            textAnchor="middle"
            dominantBaseline="central"
            fontSize={Math.max(9, RADIUS_SCALE * 0.035)}
            fontFamily="var(--font-mono)"
            fontWeight="500"
            fill="#000000"
            letterSpacing="0.12em"
          >
            YOU
          </text>

          {/* System nodes -- planets */}
          {Array.from(nodePositions.entries()).map(([id, pos]) => {
            const isHov = hoveredId !== null && systemIsInvolved(id);
            const isSelected = selectedId === id;
            const dimmed = hoveredId !== null && !systemIsInvolved(id);
            const domain = pos.system.domain as Domain;
            const color = DOMAIN_COLORS[domain];

            return (
              <g
                key={id}
                style={{
                  cursor: "pointer",
                  transition: "opacity 0.15s",
                }}
                onClick={() => onSystemClick(pos.system)}
                onMouseEnter={() => setHoveredId(id)}
                onMouseLeave={() => setHoveredId(null)}
                opacity={dimmed ? 0.12 : 1}
              >
                {/* Selection/hover ring */}
                {(isHov || isSelected) && (
                  <circle
                    cx={pos.x}
                    cy={pos.y}
                    r={nodeR + 5}
                    fill="none"
                    stroke={color}
                    strokeWidth="1"
                    opacity="0.4"
                  />
                )}
                {/* Node circle */}
                <circle
                  cx={pos.x}
                  cy={pos.y}
                  r={nodeR}
                  fill="#FFFFFF"
                  stroke={isSelected ? "#000000" : color}
                  strokeWidth={isSelected ? 2.5 : isHov ? 2 : 1.2}
                />
                {/* Acronym label inside node */}
                <text
                  x={pos.x}
                  y={pos.y + 1}
                  textAnchor="middle"
                  dominantBaseline="central"
                  fontSize={Math.max(8, nodeR * 0.42)}
                  fontFamily="var(--font-mono)"
                  fontWeight="500"
                  fill={color}
                >
                  {pos.system.acronym || pos.system.id.toUpperCase()}
                </text>
                {/* Name label below node */}
                <text
                  x={pos.x}
                  y={pos.y + nodeR + 13}
                  textAnchor="middle"
                  dominantBaseline="central"
                  fontSize={Math.max(7, nodeR * 0.33)}
                  fontFamily="var(--font-sans)"
                  fill="var(--color-text-secondary)"
                  opacity={isHov || isSelected ? 1 : 0.45}
                >
                  {pos.system.name.length > 26
                    ? pos.system.name.slice(0, 24) + "\u2026"
                    : pos.system.name}
                </text>
              </g>
            );
          })}
        </svg>
      )}

      {/* Legend bar -- fixed at bottom of constellation */}
      <div
        style={{
          position: "absolute",
          bottom: 0,
          left: 0,
          right: 0,
          display: "flex",
          justifyContent: "center",
          gap: "24px",
          fontSize: "11px",
          fontFamily: "var(--font-sans)",
          color: "var(--color-text-tertiary)",
          background: "rgba(255, 255, 255, 0.92)",
          borderTop: "1px solid var(--color-border-light)",
          padding: "8px 16px",
          letterSpacing: "0.02em",
        }}
      >
        <span style={{ display: "flex", alignItems: "center", gap: "6px" }}>
          <svg width="24" height="3">
            <line
              x1="0"
              y1="1.5"
              x2="24"
              y2="1.5"
              stroke="#333333"
              strokeWidth="1.5"
            />
          </svg>
          Connected
        </span>
        <span style={{ display: "flex", alignItems: "center", gap: "6px" }}>
          <svg width="24" height="3">
            <line
              x1="0"
              y1="1.5"
              x2="24"
              y2="1.5"
              stroke="#CC0000"
              strokeWidth="1.5"
              strokeDasharray="4 4"
            />
          </svg>
          Gap
        </span>
        <span style={{ display: "flex", alignItems: "center", gap: "6px" }}>
          <svg width="24" height="3">
            <line
              x1="0"
              y1="1.5"
              x2="24"
              y2="1.5"
              stroke="#006600"
              strokeWidth="1.5"
              strokeDasharray="8 5"
            />
          </svg>
          Closable by consent
        </span>
      </div>
    </div>
  );
}
