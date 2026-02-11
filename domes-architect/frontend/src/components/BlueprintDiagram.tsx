import { useState, useRef, useEffect, useCallback } from "react";
import type { Architecture, Stakeholder } from "../types";
import { DOMAIN_COLORS, DOMAIN_LABELS } from "../types";

interface Props {
  architecture: Architecture;
}

interface Size {
  w: number;
  h: number;
}

interface NodePosition {
  x: number;
  y: number;
}

const INFLUENCE_SIZE: Record<string, { w: number; h: number }> = {
  high: { w: 50, h: 30 },
  moderate: { w: 45, h: 28 },
  low: { w: 40, h: 26 },
};

const DOMAIN_BOX = { w: 60, h: 30 };
const INNER_RADIUS = 150;
const OUTER_RADIUS = 280;
const MIN_HEIGHT = 600;
const PERSON_RADIUS = 22;

function truncateText(text: string, maxLen: number): string {
  if (text.length <= maxLen) return text;
  return text.slice(0, maxLen - 1) + "\u2026";
}

function polarToCartesian(
  cx: number,
  cy: number,
  radius: number,
  angleRad: number
): NodePosition {
  return {
    x: cx + radius * Math.cos(angleRad),
    y: cy + radius * Math.sin(angleRad),
  };
}

function edgeEndpoint(
  fromX: number,
  fromY: number,
  toX: number,
  toY: number,
  boxW: number,
  boxH: number
): NodePosition {
  // Find the point on the edge of a rectangle centered at (toX, toY)
  // along the line from (fromX, fromY) to (toX, toY)
  const dx = toX - fromX;
  const dy = toY - fromY;
  const halfW = boxW / 2;
  const halfH = boxH / 2;

  if (dx === 0 && dy === 0) return { x: toX, y: toY };

  const absDx = Math.abs(dx);
  const absDy = Math.abs(dy);

  let t: number;
  if (absDx * halfH > absDy * halfW) {
    // Intersects left or right edge
    t = halfW / absDx;
  } else {
    // Intersects top or bottom edge
    t = halfH / absDy;
  }

  return {
    x: toX - dx * t,
    y: toY - dy * t,
  };
}

function getStakeholderPositions(
  stakeholders: Stakeholder[],
  cx: number,
  cy: number
): NodePosition[] {
  const count = stakeholders.length;
  if (count === 0) return [];
  const startAngle = -Math.PI / 2;
  const step = (2 * Math.PI) / count;
  return stakeholders.map((_, i) => {
    const angle = startAngle + i * step;
    return polarToCartesian(cx, cy, INNER_RADIUS, angle);
  });
}

function getDomainPositions(
  domains: string[],
  cx: number,
  cy: number
): NodePosition[] {
  const count = domains.length;
  if (count === 0) return [];
  const startAngle = -Math.PI / 2 + Math.PI / count;
  const step = (2 * Math.PI) / count;
  return domains.map((_, i) => {
    const angle = startAngle + i * step;
    return polarToCartesian(cx, cy, OUTER_RADIUS, angle);
  });
}

// Map stakeholders to relevant domains based on simple heuristics
function stakeholderDomainLinks(
  stakeholders: Stakeholder[],
  domains: string[]
): Array<[number, number]> {
  const links: Array<[number, number]> = [];
  const domainKeywords: Record<string, string[]> = {
    health: ["health", "medical", "clinical", "hospital", "physician", "nurse", "mental"],
    behavioral_health: ["behavioral", "mental", "substance", "addiction", "counselor", "therapist"],
    justice: ["justice", "court", "legal", "police", "law", "correctional", "probation", "judge"],
    housing: ["housing", "shelter", "homeless", "landlord", "hud", "rental"],
    income: ["income", "employment", "workforce", "financial", "economic", "benefits", "welfare"],
    education: ["education", "school", "academic", "teacher", "student", "university", "training"],
    child_welfare: ["child", "family", "foster", "dcfs", "youth", "juvenile", "cps"],
    social_support: ["social", "community", "support", "services", "nonprofit", "advocacy"],
    immigration: ["immigration", "immigrant", "refugee", "asylum", "visa", "citizenship"],
  };

  stakeholders.forEach((s, si) => {
    const text = `${s.name} ${s.role} ${s.description} ${s.interest}`.toLowerCase();
    domains.forEach((d, di) => {
      const keywords = domainKeywords[d] || [d.replace(/_/g, " ")];
      const matches = keywords.some((kw) => text.includes(kw));
      if (matches) {
        links.push([si, di]);
      }
    });
    // If no domain matched, link to the first domain as a default connection
    if (!links.some(([sIdx]) => sIdx === si) && domains.length > 0) {
      links.push([si, 0]);
    }
  });

  return links;
}

export default function BlueprintDiagram({ architecture }: Props) {
  const containerRef = useRef<HTMLDivElement>(null);
  const [size, setSize] = useState<Size>({ w: 0, h: 0 });

  const handleResize = useCallback(() => {
    if (containerRef.current) {
      const rect = containerRef.current.getBoundingClientRect();
      setSize({ w: rect.width, h: Math.max(rect.width * 0.75, MIN_HEIGHT) });
    }
  }, []);

  useEffect(() => {
    handleResize();
    const observer = new ResizeObserver(handleResize);
    if (containerRef.current) observer.observe(containerRef.current);
    return () => observer.disconnect();
  }, [handleResize]);

  const hasSize = size.w > 0 && size.h > 0;

  const { stakeholders, domains_targeted } = architecture;
  const domains = domains_targeted || [];
  const stakeList = stakeholders || [];

  // Compute center and scale
  const diagramNaturalWidth = OUTER_RADIUS * 2 + DOMAIN_BOX.w + 80;
  const diagramNaturalHeight = OUTER_RADIUS * 2 + DOMAIN_BOX.h + 120;
  const svgW = hasSize ? size.w : diagramNaturalWidth;
  const svgH = hasSize ? size.h : diagramNaturalHeight;
  const cx = svgW / 2;
  const cy = svgH / 2;

  // Scale if container is too small
  const scale = Math.min(
    1,
    (svgW - 40) / diagramNaturalWidth,
    (svgH - 80) / diagramNaturalHeight
  );

  const stakeholderPositions = getStakeholderPositions(stakeList, cx, cy);
  const domainPositions = getDomainPositions(domains, cx, cy);
  const domainLinks = stakeholderDomainLinks(stakeList, domains);

  return (
    <div ref={containerRef} style={{ width: "100%", minHeight: MIN_HEIGHT }}>
      {hasSize && (
        <svg
          width={svgW}
          height={svgH}
          viewBox={`0 0 ${svgW} ${svgH}`}
          style={{ display: "block", backgroundColor: "#ffffff" }}
        >
          <defs>
            <marker
              id="arrowSolid"
              markerWidth="8"
              markerHeight="6"
              refX="8"
              refY="3"
              orient="auto"
            >
              <polygon points="0,0 8,3 0,6" fill="#000000" />
            </marker>
            <marker
              id="arrowDashed"
              markerWidth="6"
              markerHeight="5"
              refX="6"
              refY="2.5"
              orient="auto"
            >
              <polygon points="0,0 6,2.5 0,5" fill="#000000" opacity="0.5" />
            </marker>
          </defs>

          <g transform={`scale(${scale}) translate(${((1 - scale) * svgW) / (2 * scale)}, ${((1 - scale) * svgH) / (2 * scale)})`}>
            {/* Title */}
            <text
              x={cx}
              y={30}
              textAnchor="middle"
              fontFamily="'Crimson Text', serif"
              fontSize="20"
              fontWeight="700"
              fill="#000000"
              letterSpacing="3"
            >
              ARCHITECTURE BLUEPRINT
            </text>
            <text
              x={cx}
              y={48}
              textAnchor="middle"
              fontFamily="'Inter', sans-serif"
              fontSize="11"
              fill="#555555"
            >
              {architecture.name}
            </text>

            {/* Connection lines: stakeholder to center */}
            {stakeholderPositions.map((pos, i) => {
              const influence = stakeList[i].influence?.toLowerCase() || "moderate";
              const boxSize = INFLUENCE_SIZE[influence] || INFLUENCE_SIZE.moderate;
              const edgePt = edgeEndpoint(cx, cy, pos.x, pos.y, boxSize.w, boxSize.h);
              // Also compute departure from person circle
              const angle = Math.atan2(pos.y - cy, pos.x - cx);
              const fromX = cx + PERSON_RADIUS * Math.cos(angle);
              const fromY = cy + PERSON_RADIUS * Math.sin(angle);
              return (
                <line
                  key={`s-line-${i}`}
                  x1={fromX}
                  y1={fromY}
                  x2={edgePt.x}
                  y2={edgePt.y}
                  stroke="#000000"
                  strokeWidth="1"
                  markerEnd="url(#arrowSolid)"
                />
              );
            })}

            {/* Connection lines: stakeholder to domain (dashed) */}
            {domainLinks.map(([si, di], idx) => {
              const sPos = stakeholderPositions[si];
              const dPos = domainPositions[di];
              if (!sPos || !dPos) return null;
              const influence = stakeList[si].influence?.toLowerCase() || "moderate";
              const sBox = INFLUENCE_SIZE[influence] || INFLUENCE_SIZE.moderate;
              const fromPt = edgeEndpoint(dPos.x, dPos.y, sPos.x, sPos.y, sBox.w, sBox.h);
              const toPt = edgeEndpoint(sPos.x, sPos.y, dPos.x, dPos.y, DOMAIN_BOX.w, DOMAIN_BOX.h);
              return (
                <line
                  key={`d-line-${idx}`}
                  x1={fromPt.x}
                  y1={fromPt.y}
                  x2={toPt.x}
                  y2={toPt.y}
                  stroke="#000000"
                  strokeWidth="1"
                  strokeDasharray="4,3"
                  opacity="0.4"
                  markerEnd="url(#arrowDashed)"
                />
              );
            })}

            {/* Center: Person icon */}
            <g>
              {/* Crosshair circle */}
              <circle
                cx={cx}
                cy={cy}
                r={PERSON_RADIUS}
                fill="#ffffff"
                stroke="#000000"
                strokeWidth="2"
              />
              {/* Crosshair lines */}
              <line
                x1={cx - PERSON_RADIUS - 6}
                y1={cy}
                x2={cx + PERSON_RADIUS + 6}
                y2={cy}
                stroke="#000000"
                strokeWidth="1"
              />
              <line
                x1={cx}
                y1={cy - PERSON_RADIUS - 6}
                x2={cx}
                y2={cy + PERSON_RADIUS + 6}
                stroke="#000000"
                strokeWidth="1"
              />
              {/* Inner circle for person head */}
              <circle
                cx={cx}
                cy={cy - 4}
                r={6}
                fill="#000000"
              />
              {/* Person body arc */}
              <path
                d={`M ${cx - 8} ${cy + 10} Q ${cx - 8} ${cy + 2} ${cx} ${cy + 2} Q ${cx + 8} ${cy + 2} ${cx + 8} ${cy + 10}`}
                fill="#000000"
              />
              {/* Label */}
              <text
                x={cx}
                y={cy + PERSON_RADIUS + 16}
                textAnchor="middle"
                fontFamily="'Inter', sans-serif"
                fontSize="9"
                fontWeight="600"
                fill="#000000"
                letterSpacing="2"
              >
                INDIVIDUAL
              </text>
            </g>

            {/* Stakeholder nodes (inner ring) */}
            {stakeList.map((s, i) => {
              const pos = stakeholderPositions[i];
              if (!pos) return null;
              const influence = s.influence?.toLowerCase() || "moderate";
              const boxSize = INFLUENCE_SIZE[influence] || INFLUENCE_SIZE.moderate;
              const halfW = boxSize.w / 2;
              const halfH = boxSize.h / 2;
              return (
                <g key={`s-node-${i}`}>
                  <rect
                    x={pos.x - halfW}
                    y={pos.y - halfH}
                    width={boxSize.w}
                    height={boxSize.h}
                    fill="#ffffff"
                    stroke="#000000"
                    strokeWidth="1.5"
                  />
                  <text
                    x={pos.x}
                    y={pos.y - 2}
                    textAnchor="middle"
                    fontFamily="'Inter', sans-serif"
                    fontSize="9"
                    fontWeight="600"
                    fill="#000000"
                  >
                    {truncateText(s.name, 12)}
                  </text>
                  <text
                    x={pos.x}
                    y={pos.y + 9}
                    textAnchor="middle"
                    fontFamily="'JetBrains Mono', monospace"
                    fontSize="7"
                    fill="#555555"
                  >
                    {truncateText(s.role, 14)}
                  </text>
                </g>
              );
            })}

            {/* Domain nodes (outer ring) */}
            {domains.map((d, i) => {
              const pos = domainPositions[i];
              if (!pos) return null;
              const color = DOMAIN_COLORS[d] || "#555555";
              const label = DOMAIN_LABELS[d] || d;
              const halfW = DOMAIN_BOX.w / 2;
              const halfH = DOMAIN_BOX.h / 2;
              return (
                <g key={`d-node-${i}`}>
                  <rect
                    x={pos.x - halfW}
                    y={pos.y - halfH}
                    width={DOMAIN_BOX.w}
                    height={DOMAIN_BOX.h}
                    fill={color}
                    stroke="#000000"
                    strokeWidth="1.5"
                  />
                  <text
                    x={pos.x}
                    y={pos.y + 1}
                    textAnchor="middle"
                    dominantBaseline="middle"
                    fontFamily="'Inter', sans-serif"
                    fontSize="9"
                    fontWeight="600"
                    fill="#ffffff"
                    letterSpacing="0.5"
                  >
                    {truncateText(label, 14)}
                  </text>
                </g>
              );
            })}

            {/* Metadata in top-right corner */}
            <g>
              <text
                x={svgW - 20}
                y={30}
                textAnchor="end"
                fontFamily="'JetBrains Mono', monospace"
                fontSize="9"
                fill="#555555"
              >
                COMPOSITE: {architecture.scores ? (architecture.scores.composite * 100).toFixed(0) : "N/A"}
              </text>
              <text
                x={svgW - 20}
                y={42}
                textAnchor="end"
                fontFamily="'JetBrains Mono', monospace"
                fontSize="9"
                fill="#555555"
              >
                FTE: {architecture.workforce_plan?.total_estimated_fte ?? "N/A"}
              </text>
              <text
                x={svgW - 20}
                y={54}
                textAnchor="end"
                fontFamily="'JetBrains Mono', monospace"
                fontSize="9"
                fill="#555555"
              >
                BUDGET: ${architecture.budget_breakdown?.total_annual
                  ? new Intl.NumberFormat("en-US", { maximumFractionDigits: 0 }).format(
                      architecture.budget_breakdown.total_annual
                    )
                  : "N/A"}
              </text>
            </g>

            {/* Ring guides (subtle) */}
            <circle
              cx={cx}
              cy={cy}
              r={INNER_RADIUS}
              fill="none"
              stroke="#000000"
              strokeWidth="0.5"
              strokeDasharray="2,6"
              opacity="0.15"
            />
            <circle
              cx={cx}
              cy={cy}
              r={OUTER_RADIUS}
              fill="none"
              stroke="#000000"
              strokeWidth="0.5"
              strokeDasharray="2,6"
              opacity="0.15"
            />

            {/* Legend at bottom */}
            <g>
              <text
                x={cx}
                y={svgH - 50}
                textAnchor="middle"
                fontFamily="'Inter', sans-serif"
                fontSize="9"
                fontWeight="600"
                fill="#000000"
                letterSpacing="2"
              >
                DOMAINS
              </text>
              {(() => {
                const legendDomains = domains.length > 0 ? domains : Object.keys(DOMAIN_COLORS);
                const itemWidth = 80;
                const totalWidth = legendDomains.length * itemWidth;
                const startX = cx - totalWidth / 2;
                const legendY = svgH - 30;
                return legendDomains.map((d, i) => {
                  const color = DOMAIN_COLORS[d] || "#555555";
                  const label = DOMAIN_LABELS[d] || d;
                  const x = startX + i * itemWidth + itemWidth / 2;
                  return (
                    <g key={`legend-${i}`}>
                      <rect
                        x={x - 5}
                        y={legendY - 7}
                        width={10}
                        height={10}
                        fill={color}
                        stroke="#000000"
                        strokeWidth="0.5"
                      />
                      <text
                        x={x + 10}
                        y={legendY}
                        textAnchor="start"
                        dominantBaseline="middle"
                        fontFamily="'JetBrains Mono', monospace"
                        fontSize="8"
                        fill="#000000"
                      >
                        {truncateText(label, 12)}
                      </text>
                    </g>
                  );
                });
              })()}
              {/* Line style legend */}
              <g>
                {(() => {
                  const lineY = svgH - 12;
                  return (
                    <>
                      <line
                        x1={cx - 100}
                        y1={lineY}
                        x2={cx - 70}
                        y2={lineY}
                        stroke="#000000"
                        strokeWidth="1"
                      />
                      <text
                        x={cx - 65}
                        y={lineY}
                        dominantBaseline="middle"
                        fontFamily="'JetBrains Mono', monospace"
                        fontSize="7"
                        fill="#555555"
                      >
                        Stakeholder link
                      </text>
                      <line
                        x1={cx + 20}
                        y1={lineY}
                        x2={cx + 50}
                        y2={lineY}
                        stroke="#000000"
                        strokeWidth="1"
                        strokeDasharray="4,3"
                      />
                      <text
                        x={cx + 55}
                        y={lineY}
                        dominantBaseline="middle"
                        fontFamily="'JetBrains Mono', monospace"
                        fontSize="7"
                        fill="#555555"
                      >
                        Domain link
                      </text>
                    </>
                  );
                })()}
              </g>
            </g>
          </g>
        </svg>
      )}
    </div>
  );
}
