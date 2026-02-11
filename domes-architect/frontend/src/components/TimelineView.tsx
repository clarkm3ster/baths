import { useState, useRef, useEffect, useCallback } from "react";
import type { Architecture, Phase } from "../types";

interface Props {
  architectures: Architecture[];
}

const PHASE_COLORS = ["#1A3D8B", "#1A6B3C", "#6B5A1A", "#5A1A6B", "#1A6B6B", "#8B1A1A"];

function parseDuration(duration: string): number {
  const lower = duration.toLowerCase();
  const match = lower.match(/(\d+)/);
  if (!match) return 3;
  const num = parseInt(match[1], 10);
  if (lower.includes("year")) return num * 12;
  if (lower.includes("week")) return Math.max(1, Math.round(num / 4));
  return num; // assume months
}

export default function TimelineView({ architectures }: Props) {
  const [selectedId, setSelectedId] = useState<number | "">(
    architectures.length > 0 ? architectures[0].id : ""
  );
  const containerRef = useRef<HTMLDivElement>(null);
  const [size, setSize] = useState({ w: 0, h: 0 });

  const handleResize = useCallback(() => {
    if (containerRef.current) {
      const rect = containerRef.current.getBoundingClientRect();
      setSize({ w: rect.width, h: rect.height });
    }
  }, []);

  useEffect(() => {
    handleResize();
    const observer = new ResizeObserver(handleResize);
    if (containerRef.current) observer.observe(containerRef.current);
    return () => observer.disconnect();
  }, [handleResize]);

  const arch = architectures.find((a) => a.id === selectedId);
  const phases: Phase[] = arch?.implementation_phases ?? [];

  // Calculate timeline
  const durations = phases.map((p) => parseDuration(p.duration));
  const totalMonths = durations.reduce((s, d) => s + d, 0) || 1;

  // SVG layout
  const margin = { top: 40, right: 20, bottom: 40, left: 200 };
  const barHeight = 40;
  const barGap = 16;
  const svgHeight = margin.top + phases.length * (barHeight + barGap) + margin.bottom;
  const chartWidth = size.w - margin.left - margin.right;

  return (
    <div className="p-6">
      <h2 className="text-2xl font-bold mb-6">Implementation Timeline</h2>

      {/* Architecture Selector */}
      <div className="mb-6">
        <label className="block text-xs font-semibold uppercase tracking-wider mb-1">
          Select Architecture
        </label>
        <select
          value={selectedId}
          onChange={(e) => setSelectedId(e.target.value ? Number(e.target.value) : "")}
          className="border-2 border-black px-3 py-2 text-sm font-mono bg-white focus:outline-none min-w-64"
        >
          {architectures.length === 0 && <option value="">No architectures available</option>}
          {architectures.map((a) => (
            <option key={a.id} value={a.id}>
              {a.name}
            </option>
          ))}
        </select>
      </div>

      {!arch && (
        <div className="text-sm text-[var(--color-text-secondary)] font-mono">
          Select an architecture to view its timeline.
        </div>
      )}

      {arch && phases.length === 0 && (
        <div className="text-sm text-[var(--color-text-secondary)] font-mono">
          No implementation phases defined for this architecture.
        </div>
      )}

      {arch && phases.length > 0 && (
        <>
          {/* Gantt Chart */}
          <div ref={containerRef} className="w-full border-2 border-black bg-white mb-6" style={{ minHeight: svgHeight }}>
            {size.w > 0 && (
              <svg width={size.w} height={svgHeight}>
                {/* Month markers */}
                {Array.from({ length: totalMonths + 1 }, (_, i) => {
                  const x = margin.left + (i / totalMonths) * chartWidth;
                  return (
                    <g key={i}>
                      <line
                        x1={x}
                        y1={margin.top - 10}
                        x2={x}
                        y2={svgHeight - margin.bottom}
                        stroke="#E0E0E0"
                        strokeWidth={1}
                      />
                      <text
                        x={x}
                        y={margin.top - 16}
                        textAnchor="middle"
                        fontSize={10}
                        fontFamily="'JetBrains Mono', monospace"
                        fill="#888888"
                      >
                        M{i}
                      </text>
                    </g>
                  );
                })}

                {/* Phase bars */}
                {phases.map((phase, i) => {
                  const startMonth = durations.slice(0, i).reduce((s, d) => s + d, 0);
                  const duration = durations[i];
                  const x = margin.left + (startMonth / totalMonths) * chartWidth;
                  const w = (duration / totalMonths) * chartWidth;
                  const y = margin.top + i * (barHeight + barGap);
                  const color = PHASE_COLORS[i % PHASE_COLORS.length];

                  return (
                    <g key={i}>
                      {/* Phase label */}
                      <text
                        x={margin.left - 8}
                        y={y + barHeight / 2 + 4}
                        textAnchor="end"
                        fontSize={11}
                        fontFamily="'Inter', sans-serif"
                        fontWeight={600}
                        fill="#000000"
                      >
                        {phase.name.length > 24 ? phase.name.slice(0, 24) + "..." : phase.name}
                      </text>

                      {/* Bar */}
                      <rect
                        x={x}
                        y={y}
                        width={Math.max(w, 2)}
                        height={barHeight}
                        fill={color}
                        stroke="#000000"
                        strokeWidth={1}
                      />

                      {/* Duration label */}
                      <text
                        x={x + w / 2}
                        y={y + barHeight / 2 + 4}
                        textAnchor="middle"
                        fontSize={10}
                        fontFamily="'JetBrains Mono', monospace"
                        fill="#FFFFFF"
                        fontWeight={600}
                      >
                        {phase.duration}
                      </text>

                      {/* Milestone dots */}
                      {phase.milestones.map((_, mi) => {
                        const mx = x + ((mi + 1) / (phase.milestones.length + 1)) * w;
                        return (
                          <circle
                            key={mi}
                            cx={mx}
                            cy={y + barHeight + 6}
                            r={3}
                            fill={color}
                            stroke="#000000"
                            strokeWidth={1}
                          />
                        );
                      })}
                    </g>
                  );
                })}
              </svg>
            )}
          </div>

          {/* Milestone Checklist */}
          <div className="border-2 border-black p-4">
            <h3 className="text-lg font-bold mb-4">Milestones</h3>
            <div className="space-y-4">
              {phases.map((phase, pi) => {
                const color = PHASE_COLORS[pi % PHASE_COLORS.length];
                return (
                  <div key={pi}>
                    <div className="flex items-center gap-2 mb-2">
                      <div className="w-3 h-3" style={{ backgroundColor: color }} />
                      <h4 className="text-sm font-semibold">{phase.name}</h4>
                      <span className="text-xs font-mono text-[var(--color-text-secondary)]">
                        ({phase.duration})
                      </span>
                      <span
                        className="text-[10px] font-semibold uppercase tracking-wider px-1.5 py-0.5 border ml-auto"
                        style={{
                          color: phase.status === "completed" ? "#1A6B3C" : "#888888",
                          borderColor: phase.status === "completed" ? "#1A6B3C" : "#888888",
                        }}
                      >
                        {phase.status}
                      </span>
                    </div>
                    <p className="text-xs text-[var(--color-text-secondary)] mb-2 ml-5">
                      {phase.description}
                    </p>
                    <ul className="ml-5 space-y-1">
                      {phase.milestones.map((m, mi) => (
                        <li key={mi} className="flex items-center gap-2 text-xs">
                          <span
                            className="w-3 h-3 border flex-shrink-0"
                            style={{ borderColor: color }}
                          />
                          <span className="font-mono text-[var(--color-text-secondary)]">{m}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                );
              })}
            </div>
          </div>
        </>
      )}
    </div>
  );
}
