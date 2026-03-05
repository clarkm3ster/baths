import { useState, useEffect, useRef } from "react";
import type { GraphData, GraphNode, GraphEdge } from "../types";
import { DOMAIN_COLORS, DOMAIN_LABELS } from "../types";
import { getFullGraph } from "../api/client";

interface Props {
  onSelectProvision: (id: number) => void;
}

const REL_COLORS: Record<string, string> = {
  implements: "#1A3D8B",
  interprets: "#5A1A6B",
  cross_references: "#888888",
  supersedes: "#8B1A1A",
  triggers: "#6B5A1A",
  enforces: "#1A6B3C",
};

export default function GraphView({ onSelectProvision }: Props) {
  const [graph, setGraph] = useState<GraphData>({ nodes: [], edges: [] });
  const [domainFilter, setDomainFilter] = useState<string | undefined>();
  const [hoveredNode, setHoveredNode] = useState<GraphNode | null>(null);
  const containerRef = useRef<HTMLDivElement>(null);
  const [size, setSize] = useState({ w: 0, h: 0 });

  useEffect(() => {
    const el = containerRef.current;
    if (!el) return;
    const obs = new ResizeObserver((entries) => {
      const { width, height } = entries[0].contentRect;
      setSize({ w: width, h: height });
    });
    obs.observe(el);
    return () => obs.disconnect();
  }, []);

  useEffect(() => {
    getFullGraph(domainFilter).then(setGraph);
  }, [domainFilter]);

  const hasSize = size.w > 0 && size.h > 0;
  const nodeMap = new Map(graph.nodes.map((n) => [n.id, n]));
  const domains = Object.keys(DOMAIN_COLORS);

  return (
    <div style={{ display: "flex", flexDirection: "column", height: "100%" }}>
      {/* Controls */}
      <div style={{ padding: "12px 20px", borderBottom: "1px solid var(--color-border)", display: "flex", gap: "8px", alignItems: "center" }}>
        <div className="section-label" style={{ margin: 0 }}>Graph</div>
        <div style={{ flex: 1 }} />
        <button
          onClick={() => setDomainFilter(undefined)}
          style={{
            fontFamily: "var(--font-mono)", fontSize: "10px", textTransform: "uppercase",
            padding: "3px 8px", cursor: "pointer",
            border: !domainFilter ? "1px solid var(--color-accent)" : "1px solid var(--color-border)",
            background: !domainFilter ? "var(--color-accent)" + "30" : "var(--color-surface)",
            color: !domainFilter ? "#FFF" : "var(--color-text-secondary)",
          }}
        >
          All
        </button>
        {domains.map((d) => (
          <button
            key={d}
            onClick={() => setDomainFilter(d)}
            style={{
              fontFamily: "var(--font-mono)", fontSize: "10px", textTransform: "uppercase",
              padding: "3px 8px", cursor: "pointer",
              border: domainFilter === d ? "1px solid" : "1px solid var(--color-border)",
              borderColor: domainFilter === d ? DOMAIN_COLORS[d] : undefined,
              background: domainFilter === d ? DOMAIN_COLORS[d] + "25" : "var(--color-surface)",
              color: DOMAIN_COLORS[d],
            }}
          >
            {DOMAIN_LABELS[d]?.[0] || d[0]}
          </button>
        ))}
      </div>

      {/* SVG */}
      <div ref={containerRef} style={{ flex: 1, overflow: "hidden", position: "relative" }}>
        {hasSize && (
          <svg width={size.w} height={size.h} viewBox={`0 0 ${size.w} ${size.h}`}>
            {/* Scale nodes to fit */}
            {(() => {
              const xs = graph.nodes.map((n) => n.x);
              const ys = graph.nodes.map((n) => n.y);
              const minX = Math.min(...xs, 0);
              const maxX = Math.max(...xs, 800);
              const minY = Math.min(...ys, 0);
              const maxY = Math.max(...ys, 600);
              const scaleX = (size.w - 120) / Math.max(maxX - minX, 1);
              const scaleY = (size.h - 80) / Math.max(maxY - minY, 1);
              const scale = Math.min(scaleX, scaleY, 1.5);
              const tx = (x: number) => 60 + (x - minX) * scale;
              const ty = (y: number) => 40 + (y - minY) * scale;

              return (
                <>
                  {/* Edges */}
                  {graph.edges.map((e, i) => {
                    const src = nodeMap.get(e.source);
                    const tgt = nodeMap.get(e.target);
                    if (!src || !tgt) return null;
                    return (
                      <line
                        key={i}
                        x1={tx(src.x)} y1={ty(src.y)}
                        x2={tx(tgt.x)} y2={ty(tgt.y)}
                        stroke={REL_COLORS[e.type] || "#CCC"}
                        strokeWidth={1.5}
                        opacity={0.4}
                      />
                    );
                  })}
                  {/* Nodes */}
                  {graph.nodes.map((n) => (
                    <g
                      key={n.id}
                      className="graph-node"
                      onClick={() => onSelectProvision(n.id)}
                      onMouseEnter={() => setHoveredNode(n)}
                      onMouseLeave={() => setHoveredNode(null)}
                    >
                      <rect
                        x={tx(n.x) - 6} y={ty(n.y) - 6}
                        width={12} height={12}
                        fill={n.color}
                      />
                    </g>
                  ))}
                </>
              );
            })()}
          </svg>
        )}

        {/* Tooltip */}
        {hoveredNode && (
          <div style={{
            position: "absolute", top: "12px", left: "12px",
            background: "var(--color-surface)", border: "1px solid var(--color-border)",
            padding: "8px 12px", maxWidth: "300px", pointerEvents: "none",
          }}>
            <div style={{ fontFamily: "var(--font-mono)", fontSize: "11px", fontWeight: 500 }}>
              {hoveredNode.citation}
            </div>
            <div style={{ fontSize: "12px", marginTop: "2px" }}>
              {hoveredNode.title}
            </div>
          </div>
        )}
      </div>

      {/* Legend */}
      <div style={{ padding: "8px 20px", borderTop: "1px solid var(--color-border)", display: "flex", gap: "16px", flexWrap: "wrap" }}>
        {Object.entries(REL_COLORS).map(([type, color]) => (
          <div key={type} style={{ display: "flex", alignItems: "center", gap: "4px" }}>
            <div style={{ width: "16px", height: "2px", background: color }} />
            <span style={{ fontFamily: "var(--font-mono)", fontSize: "9px", textTransform: "uppercase", color: "var(--color-text-tertiary)" }}>
              {type}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}
