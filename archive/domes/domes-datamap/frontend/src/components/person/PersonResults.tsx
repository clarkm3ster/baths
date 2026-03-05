import { useState, useEffect, useRef, useMemo } from "react";
import type { PersonMapResult, System, Connection, Gap } from "../../types";
import { DOMAIN_COLORS } from "../../types";
import { DomainBadge } from "../badges/DomainBadge";
import { SeverityBadge } from "../badges/SeverityBadge";
import { BarrierBadge } from "../badges/BarrierBadge";
import { BridgeCard } from "../bridges/BridgeCard";

interface PersonResultsProps {
  result: PersonMapResult;
}

export function PersonResults({ result }: PersonResultsProps) {
  const [activeTab, setActiveTab] = useState<
    "systems" | "connections" | "gaps" | "consent" | "network"
  >("network");

  const consentGaps = useMemo(
    () => result.gaps.filter((g) => g.consent_closable),
    [result.gaps]
  );

  const tabs = [
    { id: "network" as const, label: "Network", count: null },
    { id: "systems" as const, label: "Systems", count: result.systems.length },
    {
      id: "connections" as const,
      label: "Connections",
      count: result.connections.length,
    },
    { id: "gaps" as const, label: "Gaps", count: result.gaps.length },
    {
      id: "consent" as const,
      label: "Consent Pathways",
      count: consentGaps.length,
    },
  ];

  return (
    <div className="space-y-4">
      {/* Summary Bar */}
      <div className="grid grid-cols-6 gap-0 border border-black">
        <div className="stat-block border-r border-black">
          <div className="stat-value">{result.summary.total_systems}</div>
          <div className="stat-label">Systems</div>
        </div>
        <div className="stat-block border-r border-black">
          <div className="stat-value text-green-700">
            {result.summary.connected_pairs}
          </div>
          <div className="stat-label">Connected</div>
        </div>
        <div className="stat-block border-r border-black">
          <div className="stat-value text-red-700">
            {result.summary.disconnected_pairs}
          </div>
          <div className="stat-label">Disconnected</div>
        </div>
        <div className="stat-block border-r border-black">
          <div className="stat-value text-orange-600">
            {result.summary.gaps_count}
          </div>
          <div className="stat-label">Gaps</div>
        </div>
        <div className="stat-block border-r border-black">
          <div className="stat-value text-green-600">
            {result.summary.consent_closable_count}
          </div>
          <div className="stat-label">Consent-Closable</div>
        </div>
        <div className="stat-block">
          <div className="stat-value text-xs pt-1">
            {result.summary.total_bridge_cost}
          </div>
          <div className="stat-label">Bridge Cost</div>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex border-b-2 border-black">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            className={`px-4 py-2 font-mono text-xs uppercase tracking-wider border border-b-0 border-black transition-colors ${
              activeTab === tab.id
                ? "bg-black text-white"
                : "bg-white text-black hover:bg-gray-100"
            }`}
            style={{ marginLeft: "-1px" }}
            onClick={() => setActiveTab(tab.id)}
          >
            {tab.label}
            {tab.count !== null && (
              <span className="ml-1 opacity-70">({tab.count})</span>
            )}
          </button>
        ))}
      </div>

      {/* Tab Content */}
      {activeTab === "network" && (
        <NetworkDiagram
          systems={result.systems}
          connections={result.connections}
          gaps={result.gaps}
        />
      )}

      {activeTab === "systems" && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-2">
          {result.systems.map((system) => (
            <div key={system.id} className="card-dense">
              <div className="flex items-center gap-2 mb-1">
                <DomainBadge domain={system.domain} />
                <span className="font-mono text-xs font-bold">
                  {system.acronym}
                </span>
              </div>
              <p className="text-xs font-medium">{system.name}</p>
              <p className="text-[0.6875rem] text-gray-500">{system.agency}</p>
              <div className="flex items-center gap-2 mt-2 text-[0.625rem] font-mono text-gray-500">
                <span>API: {system.api_availability}</span>
                <span>{system.update_frequency}</span>
              </div>
              {system.fields_held && system.fields_held.length > 0 && (
                <div className="flex flex-wrap gap-0.5 mt-1">
                  {system.fields_held.slice(0, 5).map((f) => (
                    <span
                      key={f}
                      className="font-mono text-[0.5rem] px-1 border border-gray-200 text-gray-500"
                    >
                      {f}
                    </span>
                  ))}
                  {system.fields_held.length > 5 && (
                    <span className="font-mono text-[0.5rem] text-gray-400">
                      +{system.fields_held.length - 5}
                    </span>
                  )}
                </div>
              )}
            </div>
          ))}
        </div>
      )}

      {activeTab === "connections" && (
        <div>
          {result.connections.length === 0 ? (
            <p className="font-mono text-sm text-gray-500 py-4">
              No connections between your systems.
            </p>
          ) : (
            <table className="data-table">
              <thead>
                <tr>
                  <th>Source</th>
                  <th>Target</th>
                  <th>Direction</th>
                  <th>Format</th>
                  <th>Frequency</th>
                  <th>Reliability</th>
                  <th>Data Shared</th>
                </tr>
              </thead>
              <tbody>
                {result.connections.map((conn) => (
                  <tr key={conn.id}>
                    <td className="font-mono text-xs font-bold">
                      {conn.source_name || conn.source_id}
                    </td>
                    <td className="font-mono text-xs font-bold">
                      {conn.target_name || conn.target_id}
                    </td>
                    <td className="font-mono text-[0.6875rem]">
                      {conn.direction}
                    </td>
                    <td className="font-mono text-[0.6875rem]">
                      {conn.format}
                    </td>
                    <td className="font-mono text-[0.6875rem]">
                      {conn.frequency}
                    </td>
                    <td>
                      <span
                        className="font-mono text-[0.625rem] px-1 border"
                        style={{
                          color:
                            conn.reliability === "high"
                              ? "#16A34A"
                              : conn.reliability === "moderate"
                              ? "#CA8A04"
                              : "#DC2626",
                          borderColor:
                            conn.reliability === "high"
                              ? "#16A34A"
                              : conn.reliability === "moderate"
                              ? "#CA8A04"
                              : "#DC2626",
                        }}
                      >
                        {conn.reliability}
                      </span>
                    </td>
                    <td>
                      <div className="flex flex-wrap gap-0.5">
                        {conn.data_shared?.slice(0, 3).map((d) => (
                          <span
                            key={d}
                            className="font-mono text-[0.5625rem] px-1 border border-gray-300"
                          >
                            {d}
                          </span>
                        ))}
                        {(conn.data_shared?.length || 0) > 3 && (
                          <span className="font-mono text-[0.5625rem] text-gray-400">
                            +{conn.data_shared!.length - 3}
                          </span>
                        )}
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      )}

      {activeTab === "gaps" && (
        <div className="space-y-2">
          {result.gaps.length === 0 ? (
            <p className="font-mono text-sm text-gray-500 py-4">
              No gaps found for your circumstances.
            </p>
          ) : (
            result.gaps.map((gap) => (
              <GapRow key={gap.id} gap={gap} bridges={result.bridges} />
            ))
          )}
        </div>
      )}

      {activeTab === "consent" && (
        <div className="space-y-3">
          {consentGaps.length === 0 ? (
            <p className="font-mono text-sm text-gray-500 py-4">
              No consent-closable gaps for your circumstances.
            </p>
          ) : (
            <>
              <div className="border-2 border-green-600 p-3 bg-green-50">
                <p className="font-mono text-xs font-bold text-green-800 uppercase">
                  You can close {consentGaps.length} gap
                  {consentGaps.length !== 1 ? "s" : ""} by signing consent
                  releases
                </p>
                <p className="text-xs text-green-700 mt-1">
                  These gaps exist because of consent requirements that you can
                  authorize to bridge.
                </p>
              </div>
              {consentGaps.map((gap) => (
                <div
                  key={gap.id}
                  className="card border-l-4 border-l-green-600"
                >
                  <div className="flex items-center gap-2 mb-2">
                    <SeverityBadge severity={gap.severity} />
                    <span className="font-mono text-xs font-bold">
                      {gap.system_a_name || gap.system_a_id}
                    </span>
                    <span className="font-mono text-[0.625rem] text-green-600">
                      --consent--
                    </span>
                    <span className="font-mono text-xs font-bold">
                      {gap.system_b_name || gap.system_b_id}
                    </span>
                  </div>
                  {gap.consent_mechanism && (
                    <p className="text-xs mb-2 text-green-800 bg-green-50 border border-green-200 p-2">
                      <span className="font-mono text-[0.625rem] font-bold uppercase">
                        Mechanism:{" "}
                      </span>
                      {gap.consent_mechanism}
                    </p>
                  )}
                  <p className="text-xs text-gray-700">{gap.impact}</p>
                </div>
              ))}
            </>
          )}
        </div>
      )}
    </div>
  );
}

function GapRow({
  gap,
  bridges,
}: {
  gap: Gap;
  bridges: PersonMapResult["bridges"];
}) {
  const [expanded, setExpanded] = useState(false);
  const gapBridges = bridges.filter((b) => b.gap_id === gap.id);

  return (
    <div
      className={`card ${
        gap.consent_closable ? "border-l-4 border-l-green-600" : ""
      }`}
    >
      <div
        className="flex items-center gap-2 cursor-pointer"
        onClick={() => setExpanded(!expanded)}
      >
        <SeverityBadge severity={gap.severity} />
        <BarrierBadge barrier={gap.barrier_type} />
        {gap.consent_closable && (
          <span className="badge px-1 py-0 text-[0.5625rem] border-green-600 text-green-700 bg-green-50">
            CONSENT
          </span>
        )}
        <span className="font-mono text-xs font-bold">
          {gap.system_a_name || gap.system_a_id}
        </span>
        <span className="font-mono text-[0.625rem] text-red-400">--X--</span>
        <span className="font-mono text-xs font-bold">
          {gap.system_b_name || gap.system_b_id}
        </span>
        <span className="ml-auto font-mono text-[0.625rem] text-gray-400">
          {gapBridges.length} bridge{gapBridges.length !== 1 ? "s" : ""}
        </span>
        <span className="font-mono text-xs">{expanded ? "[-]" : "[+]"}</span>
      </div>
      <p className="text-xs text-gray-600 mt-1">{gap.impact}</p>
      {expanded && gapBridges.length > 0 && (
        <div className="mt-3 space-y-2 border-t border-gray-200 pt-3">
          <h5 className="section-header">Bridge Solutions</h5>
          {gapBridges.map((bridge) => (
            <BridgeCard key={bridge.id} bridge={bridge} compact />
          ))}
        </div>
      )}
    </div>
  );
}

function NetworkDiagram({
  systems,
  connections,
  gaps,
}: {
  systems: System[];
  connections: Connection[];
  gaps: Gap[];
}) {
  const containerRef = useRef<HTMLDivElement>(null);
  const [size, setSize] = useState({ w: 0, h: 0 });

  useEffect(() => {
    if (!containerRef.current) return;
    const observer = new ResizeObserver((entries) => {
      for (const entry of entries) {
        setSize({
          w: entry.contentRect.width,
          h: entry.contentRect.height,
        });
      }
    });
    observer.observe(containerRef.current);
    return () => observer.disconnect();
  }, []);

  const hasSize = size.w > 0 && size.h > 0;

  // Layout: place systems in a circle
  const nodePositions = useMemo(() => {
    if (!hasSize) return [];
    const cx = size.w / 2;
    const cy = size.h / 2;
    const radius = Math.min(cx, cy) - 60;
    return systems.map((sys, i) => {
      const angle = (2 * Math.PI * i) / systems.length - Math.PI / 2;
      return {
        system: sys,
        x: cx + radius * Math.cos(angle),
        y: cy + radius * Math.sin(angle),
      };
    });
  }, [systems, hasSize, size]);

  const systemIndexMap = useMemo(() => {
    const map = new Map<string, number>();
    systems.forEach((s, i) => map.set(s.id, i));
    return map;
  }, [systems]);

  return (
    <div
      ref={containerRef}
      className="border border-black bg-white"
      style={{ height: 500 }}
    >
      {hasSize && (
        <svg width={size.w} height={size.h}>
          {/* Connections (solid lines) */}
          {connections.map((conn) => {
            const si = systemIndexMap.get(conn.source_id);
            const ti = systemIndexMap.get(conn.target_id);
            if (si === undefined || ti === undefined) return null;
            const source = nodePositions[si];
            const target = nodePositions[ti];
            if (!source || !target) return null;
            const color =
              conn.reliability === "high"
                ? "#16A34A"
                : conn.reliability === "moderate"
                ? "#CA8A04"
                : "#DC2626";
            return (
              <line
                key={`conn-${conn.id}`}
                x1={source.x}
                y1={source.y}
                x2={target.x}
                y2={target.y}
                stroke={color}
                strokeWidth={conn.direction === "bidirectional" ? 2 : 1.5}
                opacity={0.6}
              />
            );
          })}

          {/* Gaps (dashed red lines) */}
          {gaps.map((gap) => {
            const ai = systemIndexMap.get(gap.system_a_id);
            const bi = systemIndexMap.get(gap.system_b_id);
            if (ai === undefined || bi === undefined) return null;
            const a = nodePositions[ai];
            const b = nodePositions[bi];
            if (!a || !b) return null;
            return (
              <line
                key={`gap-${gap.id}`}
                x1={a.x}
                y1={a.y}
                x2={b.x}
                y2={b.y}
                stroke={gap.consent_closable ? "#16A34A" : "#DC2626"}
                strokeWidth={1.5}
                strokeDasharray={gap.consent_closable ? "6,3" : "4,4"}
                opacity={0.5}
              />
            );
          })}

          {/* Nodes */}
          {nodePositions.map((node) => {
            const color = DOMAIN_COLORS[node.system.domain] || "#6B7280";
            return (
              <g key={node.system.id}>
                <rect
                  x={node.x - 20}
                  y={node.y - 12}
                  width={40}
                  height={24}
                  fill="white"
                  stroke={color}
                  strokeWidth={2}
                />
                <text
                  x={node.x}
                  y={node.y + 1}
                  textAnchor="middle"
                  dominantBaseline="middle"
                  fill={color}
                  fontSize={8}
                  fontFamily="'JetBrains Mono', monospace"
                  fontWeight={700}
                >
                  {node.system.acronym}
                </text>
                <text
                  x={node.x}
                  y={node.y + 20}
                  textAnchor="middle"
                  fill="#6B7280"
                  fontSize={7}
                  fontFamily="'JetBrains Mono', monospace"
                >
                  {node.system.domain}
                </text>
              </g>
            );
          })}
        </svg>
      )}
    </div>
  );
}
