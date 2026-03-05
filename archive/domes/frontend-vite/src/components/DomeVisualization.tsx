import { useRef, useState, useMemo, useCallback, useEffect } from "react";
import type { MatchedProvision, Domain } from "../types/index.ts";
import { DOMAIN_COLORS, DOMAIN_LABELS } from "../types/index.ts";

interface DomeVisualizationProps {
  provisions: MatchedProvision[];
  gaps: MatchedProvision[];
  showGaps: boolean;
  onProvisionClick: (provision: MatchedProvision) => void;
  selectedProvision?: MatchedProvision;
}

const DOMAINS: Domain[] = [
  "health",
  "housing",
  "income",
  "justice",
  "education",
  "civil_rights",
];

interface TooltipState {
  visible: boolean;
  x: number;
  y: number;
  provision: MatchedProvision | null;
}

/**
 * Compute the SVG path for a single "coffer" panel in the dome.
 *
 * The dome is a semicircle. Domains divide it into angular sectors from left
 * to right. Within each sector, provisions are arranged in concentric rings
 * (rows) and sub-columns, like coffers in a real architectural dome.
 */
function cofferPath(
  cx: number,
  cy: number,
  innerR: number,
  outerR: number,
  startAngle: number,
  endAngle: number,
): string {
  const pad = 0.004; // small gap between coffers in radians
  const a1 = startAngle + pad;
  const a2 = endAngle - pad;

  const x1 = cx + outerR * Math.cos(a1);
  const y1 = cy - outerR * Math.sin(a1);
  const x2 = cx + outerR * Math.cos(a2);
  const y2 = cy - outerR * Math.sin(a2);
  const x3 = cx + innerR * Math.cos(a2);
  const y3 = cy - innerR * Math.sin(a2);
  const x4 = cx + innerR * Math.cos(a1);
  const y4 = cy - innerR * Math.sin(a1);

  const largeArc = a2 - a1 > Math.PI ? 1 : 0;

  return [
    `M ${x1} ${y1}`,
    `A ${outerR} ${outerR} 0 ${largeArc} 1 ${x2} ${y2}`,
    `L ${x3} ${y3}`,
    `A ${innerR} ${innerR} 0 ${largeArc} 0 ${x4} ${y4}`,
    "Z",
  ].join(" ");
}

/** Label position — center of the coffer arc. */
function cofferCenter(
  cx: number,
  cy: number,
  innerR: number,
  outerR: number,
  startAngle: number,
  endAngle: number,
): { x: number; y: number } {
  const midAngle = (startAngle + endAngle) / 2;
  const midR = (innerR + outerR) / 2;
  return {
    x: cx + midR * Math.cos(midAngle),
    y: cy - midR * Math.sin(midAngle),
  };
}

/** Truncate text to fit within a certain character count. */
function truncate(text: string, max: number): string {
  return text.length <= max ? text : text.slice(0, max - 1) + "\u2026";
}

export default function DomeVisualization({
  provisions,
  gaps,
  showGaps,
  onProvisionClick,
  selectedProvision,
}: DomeVisualizationProps) {
  const svgRef = useRef<SVGSVGElement>(null);
  const [tooltip, setTooltip] = useState<TooltipState>({
    visible: false,
    x: 0,
    y: 0,
    provision: null,
  });
  const [dimensions, setDimensions] = useState({ width: 960, height: 500 });

  // Responsive sizing
  useEffect(() => {
    function handleResize() {
      if (svgRef.current?.parentElement) {
        const rect = svgRef.current.parentElement.getBoundingClientRect();
        setDimensions({
          width: rect.width,
          height: Math.max(400, rect.width * 0.52),
        });
      }
    }
    handleResize();
    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, []);

  const { width, height } = dimensions;
  const cx = width / 2;
  const cy = height - 20;
  const maxR = Math.min(width / 2 - 20, height - 40);

  // Group provisions and gaps by domain
  const domainItems = useMemo(() => {
    const items = showGaps ? [...provisions, ...gaps] : [...provisions];

    const grouped: Record<Domain, MatchedProvision[]> = {
      health: [],
      housing: [],
      income: [],
      justice: [],
      education: [],
      civil_rights: [],
    };
    for (const p of items) {
      if (grouped[p.domain]) {
        grouped[p.domain].push(p);
      }
    }
    // Sort within each domain: highest relevance first
    for (const d of DOMAINS) {
      grouped[d].sort((a, b) => b.relevance_score - a.relevance_score);
    }
    return grouped;
  }, [provisions, gaps, showGaps]);

  // Layout: compute domain sector boundaries and per-provision coffers
  const coffers = useMemo(() => {
    const totalProvisions = DOMAINS.reduce(
      (sum, d) => sum + Math.max(domainItems[d].length, 1),
      0,
    );

    const result: {
      provision: MatchedProvision;
      path: string;
      center: { x: number; y: number };
      domain: Domain;
      innerR: number;
      outerR: number;
    }[] = [];

    let angleOffset = Math.PI; // start from left

    for (const domain of DOMAINS) {
      const items = domainItems[domain];
      const count = Math.max(items.length, 1);
      // Sector width proportional to number of provisions
      const sectorAngle = (count / totalProvisions) * Math.PI;

      // Arrange provisions in rows within the sector
      const cols = Math.min(count, Math.max(1, Math.ceil(Math.sqrt(count * 1.5))));
      const rows = Math.ceil(count / cols);

      const ringThickness = maxR / (rows + 0.5);

      let idx = 0;
      for (let row = 0; row < rows; row++) {
        const colsInRow = Math.min(cols, count - idx);
        const innerR = maxR - (row + 1) * ringThickness + 4;
        const outerR = maxR - row * ringThickness - 2;
        const colAngle = sectorAngle / colsInRow;

        for (let col = 0; col < colsInRow; col++) {
          if (idx >= items.length) break;
          const startA = angleOffset - sectorAngle + col * colAngle;
          const endA = startA + colAngle;

          result.push({
            provision: items[idx],
            path: cofferPath(cx, cy, innerR, outerR, startA, endA),
            center: cofferCenter(cx, cy, innerR, outerR, startA, endA),
            domain,
            innerR,
            outerR,
          });
          idx++;
        }
      }

      angleOffset -= sectorAngle;
    }

    return result;
  }, [domainItems, cx, cy, maxR]);

  // Domain labels along the dome edge
  const domainLabels = useMemo(() => {
    const totalProvisions = DOMAINS.reduce(
      (sum, d) => sum + Math.max(domainItems[d].length, 1),
      0,
    );
    const labels: { domain: Domain; x: number; y: number; angle: number }[] = [];
    let angleOffset = Math.PI;

    for (const domain of DOMAINS) {
      const count = Math.max(domainItems[domain].length, 1);
      const sectorAngle = (count / totalProvisions) * Math.PI;
      const midAngle = angleOffset - sectorAngle / 2;
      const labelR = maxR + 16;
      labels.push({
        domain,
        x: cx + labelR * Math.cos(midAngle),
        y: cy - labelR * Math.sin(midAngle),
        angle: midAngle,
      });
      angleOffset -= sectorAngle;
    }
    return labels;
  }, [domainItems, cx, cy, maxR]);

  const handleMouseEnter = useCallback(
    (e: React.MouseEvent, provision: MatchedProvision) => {
      const svgRect = svgRef.current?.getBoundingClientRect();
      if (!svgRect) return;
      setTooltip({
        visible: true,
        x: e.clientX - svgRect.left,
        y: e.clientY - svgRect.top - 10,
        provision,
      });
    },
    [],
  );

  const handleMouseLeave = useCallback(() => {
    setTooltip((prev) => ({ ...prev, visible: false }));
  }, []);

  return (
    <div style={{ position: "relative", width: "100%" }}>
      <svg
        ref={svgRef}
        viewBox={`0 0 ${width} ${height}`}
        style={{ width: "100%", height: "auto", display: "block" }}
        role="img"
        aria-label="Dome visualization of legal provisions grouped by domain"
      >
        {/* Dome outline */}
        <path
          d={`M ${cx - maxR} ${cy} A ${maxR} ${maxR} 0 0 1 ${cx + maxR} ${cy}`}
          fill="none"
          stroke="#E5E5E5"
          strokeWidth="1"
        />

        {/* Base line */}
        <line
          x1={cx - maxR - 10}
          y1={cy}
          x2={cx + maxR + 10}
          y2={cy}
          stroke="#E5E5E5"
          strokeWidth="1"
        />

        {/* Coffers */}
        {coffers.map((c) => {
          const isGap = c.provision.is_gap;
          const isSelected =
            selectedProvision?.provision_id === c.provision.provision_id;
          const baseColor = DOMAIN_COLORS[c.domain];
          const opacity = isGap ? 0.15 : Math.max(0.4, c.provision.relevance_score);

          return (
            <g
              key={c.provision.provision_id}
              style={{
                cursor: "pointer",
                transition: "opacity 0.3s ease, filter 0.2s ease",
              }}
              onClick={() => onProvisionClick(c.provision)}
              onMouseEnter={(e) => handleMouseEnter(e, c.provision)}
              onMouseMove={(e) => handleMouseEnter(e, c.provision)}
              onMouseLeave={handleMouseLeave}
              role="button"
              tabIndex={0}
              aria-label={`${c.provision.title} - ${c.provision.citation}`}
              onKeyDown={(e) => {
                if (e.key === "Enter" || e.key === " ") {
                  e.preventDefault();
                  onProvisionClick(c.provision);
                }
              }}
            >
              <path
                d={c.path}
                fill={isGap ? "none" : baseColor}
                fillOpacity={opacity}
                stroke={isGap ? baseColor : isSelected ? "#fff" : baseColor}
                strokeWidth={isSelected ? 2 : 0.5}
                strokeDasharray={isGap ? "6 3" : "none"}
                style={{ transition: "all 0.3s ease" }}
              />
              {/* Citation text inside coffer -- only show if large enough */}
              {c.outerR - c.innerR > 25 && (
                <text
                  x={c.center.x}
                  y={c.center.y - 4}
                  textAnchor="middle"
                  dominantBaseline="auto"
                  fill={isGap ? "#999" : "#fff"}
                  fontSize="7"
                  fontFamily="'JetBrains Mono', monospace"
                  style={{ pointerEvents: "none", userSelect: "none" }}
                >
                  {truncate(c.provision.citation, 22)}
                </text>
              )}
              {c.outerR - c.innerR > 40 && (
                <text
                  x={c.center.x}
                  y={c.center.y + 8}
                  textAnchor="middle"
                  dominantBaseline="auto"
                  fill={isGap ? "#aaa" : "rgba(255,255,255,0.85)"}
                  fontSize="6"
                  fontFamily="Georgia, 'Times New Roman', serif"
                  style={{ pointerEvents: "none", userSelect: "none" }}
                >
                  {truncate(c.provision.title, 28)}
                </text>
              )}
            </g>
          );
        })}

        {/* Domain labels */}
        {domainLabels.map((lbl) => {
          // Rotate text to follow the dome arc
          const deg = -(lbl.angle * 180) / Math.PI + 90;
          const rotate =
            lbl.angle > Math.PI / 2
              ? deg + 180
              : deg;
          return (
            <text
              key={lbl.domain}
              x={lbl.x}
              y={lbl.y}
              textAnchor="middle"
              dominantBaseline="middle"
              transform={`rotate(${rotate}, ${lbl.x}, ${lbl.y})`}
              fill={DOMAIN_COLORS[lbl.domain]}
              fontSize="9"
              fontFamily="'Inter', system-ui, sans-serif"
              fontWeight="600"
              letterSpacing="0.05em"
              style={{ textTransform: "uppercase" }}
            >
              {DOMAIN_LABELS[lbl.domain]}
            </text>
          );
        })}

        {/* Central label */}
        <text
          x={cx}
          y={cy - 8}
          textAnchor="middle"
          fill="#000"
          fontSize="10"
          fontFamily="Georgia, 'Times New Roman', serif"
          fontStyle="italic"
          opacity="0.4"
        >
          your rights
        </text>
      </svg>

      {/* Tooltip */}
      {tooltip.visible && tooltip.provision && (
        <div
          style={{
            position: "absolute",
            left: tooltip.x,
            top: tooltip.y,
            transform: "translate(-50%, -100%)",
            padding: "8px 12px",
            background: "#000",
            color: "#fff",
            fontSize: "12px",
            lineHeight: "1.4",
            maxWidth: "260px",
            pointerEvents: "none",
            zIndex: 10,
            border: "1px solid #333",
          }}
        >
          <div
            style={{
              fontFamily: "'JetBrains Mono', monospace",
              fontSize: "10px",
              opacity: 0.7,
              marginBottom: "2px",
            }}
          >
            {tooltip.provision.citation}
          </div>
          <div
            style={{
              fontFamily: "Georgia, 'Times New Roman', serif",
              fontWeight: 600,
              marginBottom: "4px",
            }}
          >
            {tooltip.provision.title}
          </div>
          <div style={{ fontSize: "10px", opacity: 0.7 }}>
            Relevance: {Math.round(tooltip.provision.relevance_score * 100)}%
            {tooltip.provision.is_gap && " \u2014 GAP IN PROTECTION"}
          </div>
        </div>
      )}
    </div>
  );
}
