import { useState, useEffect, useRef, useCallback } from 'react';
import {
  DOMAINS,
  CONNECTIONS,
  type DomainConfig,
  type Connection,
} from '../api/client';

interface ConnectionsMapProps {
  onSelectDomain: (slug: string) => void;
}

interface NodePosition {
  x: number;
  y: number;
  domain: DomainConfig;
}

export default function ConnectionsMap({ onSelectDomain }: ConnectionsMapProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const [size, setSize] = useState({ width: 800, height: 600 });
  const [hoveredDomain, setHoveredDomain] = useState<string | null>(null);
  const [selectedEdge, setSelectedEdge] = useState<Connection | null>(null);

  // Responsive sizing
  useEffect(() => {
    const container = containerRef.current;
    if (!container) return;

    const observer = new ResizeObserver((entries) => {
      for (const entry of entries) {
        const { width, height } = entry.contentRect;
        setSize({ width: Math.max(width, 400), height: Math.max(height, 400) });
      }
    });

    observer.observe(container);
    // Initial size
    const rect = container.getBoundingClientRect();
    setSize({
      width: Math.max(rect.width, 400),
      height: Math.max(rect.height, 400),
    });

    return () => observer.disconnect();
  }, []);

  // Calculate node positions in an ellipse
  const cx = size.width / 2;
  const cy = size.height / 2;
  const rx = Math.min(size.width * 0.38, 340);
  const ry = Math.min(size.height * 0.38, 260);
  const nodeRadius = 28;

  const nodes: NodePosition[] = DOMAINS.map((domain, i) => {
    const angle = (2 * Math.PI * i) / DOMAINS.length - Math.PI / 2;
    return {
      x: cx + rx * Math.cos(angle),
      y: cy + ry * Math.sin(angle),
      domain,
    };
  });

  const getNode = useCallback(
    (slug: string) => nodes.find((n) => n.domain.slug === slug),
    [nodes]
  );

  // Check if a domain is connected to the hovered domain
  function isConnectedTo(slug: string): boolean {
    if (!hoveredDomain) return false;
    return CONNECTIONS.some(
      (c) =>
        (c.from === hoveredDomain && c.to === slug) ||
        (c.to === hoveredDomain && c.from === slug)
    );
  }

  // Get connection between two domains
  function getConnection(from: string, to: string): Connection | undefined {
    return CONNECTIONS.find(
      (c) =>
        (c.from === from && c.to === to) || (c.from === to && c.to === from)
    );
  }

  return (
    <div
      style={{
        padding: 24,
        height: '100%',
        display: 'flex',
        flexDirection: 'column',
      }}
    >
      {/* Header */}
      <div style={{ marginBottom: 16, flexShrink: 0 }}>
        <h1
          style={{
            fontSize: 20,
            fontWeight: 700,
            color: '#FFFFFF',
            margin: 0,
            marginBottom: 6,
          }}
        >
          Domain Connections
        </h1>
        <p
          style={{
            fontSize: 13,
            color: 'rgba(255,255,255,0.5)',
            margin: 0,
          }}
        >
          {CONNECTIONS.length} connections across {DOMAINS.length} domains.
          Hover a domain to highlight its connections. Click a line to see details.
        </p>
      </div>

      {/* Map Container */}
      <div
        ref={containerRef}
        style={{
          flex: 1,
          background: '#0A0A0A',
          border: '1px solid #1A1A1A',
          borderRadius: 12,
          position: 'relative',
          overflow: 'hidden',
          minHeight: 400,
        }}
      >
        <svg
          width={size.width}
          height={size.height}
          style={{ display: 'block' }}
        >
          {/* Grid pattern (subtle) */}
          <defs>
            <pattern
              id="grid"
              width="40"
              height="40"
              patternUnits="userSpaceOnUse"
            >
              <path
                d="M 40 0 L 0 0 0 40"
                fill="none"
                stroke="rgba(255,255,255,0.03)"
                strokeWidth="0.5"
              />
            </pattern>
          </defs>
          <rect width={size.width} height={size.height} fill="url(#grid)" />

          {/* Connection Lines */}
          {CONNECTIONS.map((conn, idx) => {
            const fromNode = getNode(conn.from);
            const toNode = getNode(conn.to);
            if (!fromNode || !toNode) return null;

            const isHighlighted =
              hoveredDomain === conn.from || hoveredDomain === conn.to;
            const isSelected =
              selectedEdge &&
              ((selectedEdge.from === conn.from &&
                selectedEdge.to === conn.to) ||
                (selectedEdge.from === conn.to &&
                  selectedEdge.to === conn.from));
            const isDimmed = hoveredDomain && !isHighlighted;

            const strokeWidth = Math.max(
              1,
              (conn.strength / 10) * (isHighlighted ? 4 : 2.5)
            );
            const opacity = isDimmed ? 0.08 : isHighlighted ? 0.7 : 0.2;

            // Color blend from source
            const fromColor =
              fromNode.domain.color;

            return (
              <line
                key={`${conn.from}-${conn.to}-${idx}`}
                x1={fromNode.x}
                y1={fromNode.y}
                x2={toNode.x}
                y2={toNode.y}
                stroke={isSelected ? '#FFFFFF' : fromColor}
                strokeWidth={isSelected ? strokeWidth + 1 : strokeWidth}
                opacity={isSelected ? 0.9 : opacity}
                strokeLinecap="round"
                style={{
                  cursor: 'pointer',
                  transition:
                    'opacity 0.2s, stroke-width 0.2s, stroke 0.2s',
                }}
                onClick={(e) => {
                  e.stopPropagation();
                  setSelectedEdge(
                    isSelected ? null : conn
                  );
                }}
              />
            );
          })}

          {/* Domain Nodes */}
          {nodes.map((node) => {
            const isHovered = hoveredDomain === node.domain.slug;
            const isConnected = isConnectedTo(node.domain.slug);
            const isDimmed =
              hoveredDomain !== null && !isHovered && !isConnected;

            const fillOpacity = isDimmed ? 0.15 : isHovered ? 1 : 0.8;
            const r = isHovered ? nodeRadius + 4 : nodeRadius;

            return (
              <g
                key={node.domain.slug}
                style={{
                  cursor: 'pointer',
                  transition: 'opacity 0.2s',
                  opacity: isDimmed ? 0.25 : 1,
                }}
                onMouseEnter={() => {
                  setHoveredDomain(node.domain.slug);
                  setSelectedEdge(null);
                }}
                onMouseLeave={() => setHoveredDomain(null)}
                onClick={() => onSelectDomain(node.domain.slug)}
              >
                {/* Glow effect */}
                {isHovered && (
                  <circle
                    cx={node.x}
                    cy={node.y}
                    r={r + 8}
                    fill={node.domain.color}
                    opacity={0.12}
                  />
                )}

                {/* Node background */}
                <circle
                  cx={node.x}
                  cy={node.y}
                  r={r}
                  fill="#0A0A0A"
                  stroke={node.domain.color}
                  strokeWidth={isHovered ? 2 : 1}
                  opacity={fillOpacity}
                />

                {/* Icon */}
                <text
                  x={node.x}
                  y={node.y}
                  textAnchor="middle"
                  dominantBaseline="central"
                  fill={node.domain.color}
                  fontSize={isHovered ? 18 : 16}
                  fontFamily="'Inter', sans-serif"
                  style={{ pointerEvents: 'none' }}
                >
                  {node.domain.icon}
                </text>

                {/* Label */}
                <text
                  x={node.x}
                  y={node.y + r + 14}
                  textAnchor="middle"
                  fill={
                    isDimmed
                      ? 'rgba(255,255,255,0.15)'
                      : isHovered
                      ? '#FFFFFF'
                      : 'rgba(255,255,255,0.5)'
                  }
                  fontSize={10}
                  fontFamily="'Inter', sans-serif"
                  fontWeight={isHovered ? 600 : 400}
                  style={{
                    pointerEvents: 'none',
                    transition: 'fill 0.2s',
                  }}
                >
                  {node.domain.label}
                </text>
              </g>
            );
          })}
        </svg>

        {/* Edge Detail Card (overlay) */}
        {selectedEdge && (
          <div
            style={{
              position: 'absolute',
              bottom: 16,
              left: 16,
              right: 16,
              maxWidth: 420,
              background: '#111111',
              border: '1px solid #2A2A2A',
              borderRadius: 10,
              padding: 16,
              zIndex: 10,
            }}
          >
            <div
              style={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
                marginBottom: 8,
              }}
            >
              <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                <ConnectionBadge slug={selectedEdge.from} />
                <span
                  style={{
                    fontSize: 11,
                    color: 'rgba(255,255,255,0.3)',
                    fontFamily: "'JetBrains Mono', monospace",
                  }}
                >
                  {'<-->'}
                </span>
                <ConnectionBadge slug={selectedEdge.to} />
              </div>
              <div
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: 4,
                }}
              >
                <span
                  style={{
                    fontSize: 10,
                    color: 'rgba(255,255,255,0.3)',
                    fontFamily: "'JetBrains Mono', monospace",
                  }}
                >
                  STR
                </span>
                <span
                  style={{
                    fontSize: 16,
                    fontWeight: 700,
                    color: '#FFFFFF',
                    fontFamily: "'JetBrains Mono', monospace",
                  }}
                >
                  {selectedEdge.strength}
                </span>
                <span
                  style={{
                    fontSize: 10,
                    color: 'rgba(255,255,255,0.3)',
                    fontFamily: "'JetBrains Mono', monospace",
                  }}
                >
                  /10
                </span>
              </div>
            </div>
            {/* Strength bar */}
            <div
              style={{
                height: 3,
                borderRadius: 2,
                background: 'rgba(255,255,255,0.08)',
                marginBottom: 10,
                overflow: 'hidden',
              }}
            >
              <div
                style={{
                  width: `${(selectedEdge.strength / 10) * 100}%`,
                  height: '100%',
                  background: '#0066FF',
                  borderRadius: 2,
                }}
              />
            </div>
            <p
              style={{
                fontSize: 12,
                color: 'rgba(255,255,255,0.6)',
                lineHeight: 1.5,
                margin: 0,
              }}
            >
              {selectedEdge.reason}
            </p>
            <button
              onClick={() => setSelectedEdge(null)}
              style={{
                marginTop: 10,
                background: 'none',
                border: '1px solid rgba(255,255,255,0.1)',
                borderRadius: 6,
                padding: '4px 12px',
                cursor: 'pointer',
                color: 'rgba(255,255,255,0.4)',
                fontSize: 11,
              }}
            >
              Close
            </button>
          </div>
        )}
      </div>

      {/* Legend */}
      <div
        style={{
          marginTop: 12,
          display: 'flex',
          gap: 16,
          flexWrap: 'wrap',
          alignItems: 'center',
          flexShrink: 0,
        }}
      >
        <span
          style={{
            fontSize: 10,
            color: 'rgba(255,255,255,0.3)',
            fontFamily: "'JetBrains Mono', monospace",
            fontWeight: 600,
            letterSpacing: '0.06em',
          }}
        >
          STRENGTH:
        </span>
        {[3, 6, 9].map((s) => (
          <div
            key={s}
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: 6,
            }}
          >
            <div
              style={{
                width: 24,
                height: Math.max(1, (s / 10) * 3),
                background: 'rgba(255,255,255,0.3)',
                borderRadius: 1,
              }}
            />
            <span
              style={{
                fontSize: 10,
                color: 'rgba(255,255,255,0.35)',
                fontFamily: "'JetBrains Mono', monospace",
              }}
            >
              {s}/10
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}

// ── Connection Badge ─────────────────────────────────────────

function ConnectionBadge({ slug }: { slug: string }) {
  const domain = DOMAINS.find((d) => d.slug === slug);
  if (!domain) return null;

  return (
    <span
      style={{
        display: 'inline-flex',
        alignItems: 'center',
        gap: 4,
        fontSize: 11,
        fontWeight: 600,
        color: domain.color,
        background: domain.color + '15',
        border: `1px solid ${domain.color}30`,
        padding: '2px 8px',
        borderRadius: 5,
      }}
    >
      <span style={{ fontSize: 12 }}>{domain.icon}</span>
      {domain.label}
    </span>
  );
}
