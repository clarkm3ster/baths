import { useState, useEffect, useRef } from 'react';
import {
  DOMAINS,
  CONNECTIONS,
  type Connection,
  getDomain,
} from '../api/client';

interface Props {
  onSelectDomain: (slug: string) => void;
}

// Position 11 domains in a circle
function getNodePositions(width: number, height: number): Map<string, { x: number; y: number }> {
  const cx = width / 2;
  const cy = height / 2;
  const rx = Math.min(width, height) * 0.35;
  const ry = rx * 0.85;
  const positions = new Map<string, { x: number; y: number }>();
  DOMAINS.forEach((d, i) => {
    const angle = (2 * Math.PI * i) / DOMAINS.length - Math.PI / 2;
    positions.set(d.slug, {
      x: cx + rx * Math.cos(angle),
      y: cy + ry * Math.sin(angle),
    });
  });
  return positions;
}

export default function ConnectionsMap({ onSelectDomain }: Props) {
  const containerRef = useRef<HTMLDivElement>(null);
  const [size, setSize] = useState({ w: 0, h: 0 });
  const [selected, setSelected] = useState<Connection | null>(null);
  const [hoveredNode, setHoveredNode] = useState<string | null>(null);

  useEffect(() => {
    if (!containerRef.current) return;
    const obs = new ResizeObserver(entries => {
      const { width, height } = entries[0].contentRect;
      setSize({ w: width, h: Math.max(height, 500) });
    });
    obs.observe(containerRef.current);
    return () => obs.disconnect();
  }, []);

  const hasSize = size.w > 0 && size.h > 0;
  const positions = hasSize ? getNodePositions(size.w, size.h) : new Map();

  return (
    <div>
      <div className="mb-6">
        <h2 className="font-serif text-2xl tracking-wide mb-1">Connections Map</h2>
        <p className="font-mono text-xs text-text-muted tracking-wide">
          {CONNECTIONS.length} CONNECTIONS BETWEEN 11 INNOVATION DOMAINS
        </p>
        <p className="text-xs text-text-muted mt-1">
          Hover a domain to highlight its connections. Click a line to see why they depend on each other.
        </p>
      </div>

      {/* Selected connection detail */}
      {selected && (
        <div className="card mb-4 border-accent-light">
          <div className="flex items-center justify-between mb-2">
            <div className="flex items-center gap-2">
              <span className="font-mono text-xs" style={{ color: getDomain(selected.from)?.color }}>
                {getDomain(selected.from)?.label}
              </span>
              <span className="font-mono text-xs text-text-muted">&harr;</span>
              <span className="font-mono text-xs" style={{ color: getDomain(selected.to)?.color }}>
                {getDomain(selected.to)?.label}
              </span>
              <span className="font-mono text-[10px] text-text-muted ml-2">
                STRENGTH: {selected.strength}/10
              </span>
            </div>
            <button onClick={() => setSelected(null)} className="font-mono text-xs text-text-muted hover:text-text">
              [X]
            </button>
          </div>
          <p className="text-sm">{selected.reason}</p>
        </div>
      )}

      {/* SVG Map */}
      <div ref={containerRef} className="card relative" style={{ minHeight: 500 }}>
        {hasSize && (
          <svg width={size.w} height={size.h} className="absolute inset-0">
            {/* Connection lines */}
            {CONNECTIONS.map((conn, i) => {
              const from = positions.get(conn.from);
              const to = positions.get(conn.to);
              if (!from || !to) return null;

              const isActive = !hoveredNode || conn.from === hoveredNode || conn.to === hoveredNode;
              const isSelected = selected === conn;
              const opacity = isActive ? (hoveredNode ? 0.8 : 0.3) : 0.06;
              const strokeWidth = isSelected ? 2.5 : (conn.strength / 10) * 2 + 0.5;

              return (
                <line
                  key={i}
                  x1={from.x}
                  y1={from.y}
                  x2={to.x}
                  y2={to.y}
                  stroke={isSelected ? '#3B7DD8' : '#3A3A42'}
                  strokeWidth={strokeWidth}
                  opacity={opacity}
                  className="cursor-pointer transition-opacity duration-200"
                  onClick={() => setSelected(conn)}
                />
              );
            })}

            {/* Domain nodes */}
            {DOMAINS.map(domain => {
              const pos = positions.get(domain.slug);
              if (!pos) return null;

              const isHovered = hoveredNode === domain.slug;
              const isConnected = hoveredNode
                ? CONNECTIONS.some(c =>
                    (c.from === hoveredNode && c.to === domain.slug) ||
                    (c.to === hoveredNode && c.from === domain.slug)
                  ) || domain.slug === hoveredNode
                : true;
              const nodeOpacity = isConnected ? 1 : 0.25;

              return (
                <g
                  key={domain.slug}
                  className="cursor-pointer"
                  onMouseEnter={() => setHoveredNode(domain.slug)}
                  onMouseLeave={() => setHoveredNode(null)}
                  onClick={() => onSelectDomain(domain.slug)}
                  opacity={nodeOpacity}
                >
                  {/* Glow */}
                  {isHovered && (
                    <circle
                      cx={pos.x}
                      cy={pos.y}
                      r={32}
                      fill={domain.color}
                      opacity={0.15}
                    />
                  )}
                  {/* Node circle */}
                  <circle
                    cx={pos.x}
                    cy={pos.y}
                    r={isHovered ? 22 : 18}
                    fill="#242428"
                    stroke={domain.color}
                    strokeWidth={isHovered ? 2.5 : 1.5}
                  />
                  {/* Icon */}
                  <text
                    x={pos.x}
                    y={pos.y + 1}
                    textAnchor="middle"
                    dominantBaseline="central"
                    fill={domain.color}
                    fontSize={isHovered ? 14 : 12}
                    fontFamily="'JetBrains Mono', monospace"
                  >
                    {domain.icon}
                  </text>
                  {/* Label */}
                  <text
                    x={pos.x}
                    y={pos.y + 32}
                    textAnchor="middle"
                    fill={isHovered ? domain.color : '#8A8A96'}
                    fontSize={10}
                    fontFamily="'JetBrains Mono', monospace"
                    letterSpacing="0.05em"
                  >
                    {domain.label.toUpperCase()}
                  </text>
                </g>
              );
            })}
          </svg>
        )}
      </div>

      {/* Connection list */}
      <div className="mt-6">
        <div className="font-mono text-xs text-text-muted tracking-wider mb-3">ALL CONNECTIONS</div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
          {CONNECTIONS.map((conn, i) => {
            const fromDomain = getDomain(conn.from);
            const toDomain = getDomain(conn.to);
            return (
              <button
                key={i}
                onClick={() => setSelected(conn)}
                className={`card-alt text-left text-xs transition-colors hover:border-accent-light ${
                  selected === conn ? 'border-accent-glow' : ''
                }`}
              >
                <div className="flex items-center gap-2 mb-1">
                  <span className="font-mono" style={{ color: fromDomain?.color }}>
                    {fromDomain?.label}
                  </span>
                  <span className="text-text-muted">&rarr;</span>
                  <span className="font-mono" style={{ color: toDomain?.color }}>
                    {toDomain?.label}
                  </span>
                  <span className="font-mono text-[9px] text-text-muted ml-auto">
                    {conn.strength}/10
                  </span>
                </div>
                <p className="text-[10px] text-text-muted line-clamp-1">{conn.reason}</p>
              </button>
            );
          })}
        </div>
      </div>
    </div>
  );
}
