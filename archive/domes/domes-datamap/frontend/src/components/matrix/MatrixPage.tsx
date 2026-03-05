import { useState, useEffect, useMemo, useRef } from "react";
import type { Connection, System } from "../../types";
import { DOMAINS, DOMAIN_COLORS } from "../../types";
import { getConnectionMatrix } from "../../api/client";
import { DomainBadge } from "../badges/DomainBadge";

interface CellDetail {
  connection: Connection;
  sourceSystem: System;
  targetSystem: System;
  row: number;
  col: number;
}

export function MatrixPage() {
  const [systems, setSystems] = useState<System[]>([]);
  const [matrix, setMatrix] = useState<(Connection | null)[][]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [domainFilter, setDomainFilter] = useState("");
  const [cellDetail, setCellDetail] = useState<CellDetail | null>(null);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    setLoading(true);
    getConnectionMatrix()
      .then((data) => {
        setSystems(data.systems);
        setMatrix(data.matrix);
      })
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, []);

  const filteredIndices = useMemo(() => {
    if (!domainFilter) return systems.map((_, i) => i);
    return systems
      .map((s, i) => ({ s, i }))
      .filter(({ s }) => s.domain === domainFilter)
      .map(({ i }) => i);
  }, [systems, domainFilter]);

  // Group systems by domain for display
  const groupedIndices = useMemo(() => {
    const groups: { domain: string; indices: number[] }[] = [];
    const domainOrder = DOMAINS;
    for (const domain of domainOrder) {
      const indices = filteredIndices.filter(
        (i) => systems[i]?.domain === domain
      );
      if (indices.length > 0) {
        groups.push({ domain, indices });
      }
    }
    // Add any domains not in the standard list
    const coveredDomains = new Set(groups.map((g) => g.domain));
    const remaining = filteredIndices.filter(
      (i) => !coveredDomains.has(systems[i]?.domain)
    );
    if (remaining.length > 0) {
      groups.push({ domain: "Other", indices: remaining });
    }
    return groups;
  }, [filteredIndices, systems]);

  const flatIndices = useMemo(
    () => groupedIndices.flatMap((g) => g.indices),
    [groupedIndices]
  );

  function getCellColor(conn: Connection | null | undefined): string {
    if (!conn) return "transparent";
    if (conn.direction === "bidirectional" && conn.reliability === "high")
      return "#16A34A";
    if (conn.reliability === "high") return "#22C55E";
    if (conn.reliability === "moderate") return "#EAB308";
    return "#EF4444";
  }

  function getCellOpacity(conn: Connection | null | undefined): number {
    if (!conn) return 0;
    if (conn.direction === "bidirectional") return 0.9;
    return 0.7;
  }

  function handleCellClick(rowIdx: number, colIdx: number) {
    const conn = matrix[rowIdx]?.[colIdx];
    if (!conn) {
      setCellDetail(null);
      return;
    }
    setCellDetail({
      connection: conn,
      sourceSystem: systems[rowIdx],
      targetSystem: systems[colIdx],
      row: rowIdx,
      col: colIdx,
    });
  }

  if (loading) {
    return (
      <div className="p-8 text-center font-mono text-sm text-gray-500">
        Loading matrix data...
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-8 text-center font-mono text-sm text-red-600">
        Error: {error}
      </div>
    );
  }

  return (
    <div className="flex flex-col h-[calc(100vh-3.5rem)]">
      {/* Header */}
      <div className="border-b border-black px-4 py-2 bg-gray-50">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="font-serif text-lg font-bold uppercase tracking-wide">
              Connection Matrix
            </h2>
            <p className="font-mono text-[0.625rem] text-gray-500 uppercase tracking-wider">
              {systems.length} systems / {flatIndices.length} displayed
            </p>
          </div>
          <div className="flex items-center gap-4">
            {/* Legend */}
            <div className="flex items-center gap-3 text-[0.625rem] font-mono">
              <div className="flex items-center gap-1">
                <span
                  className="w-3 h-3 border border-gray-400"
                  style={{ background: "#16A34A", opacity: 0.9 }}
                />
                <span>Bi / High</span>
              </div>
              <div className="flex items-center gap-1">
                <span
                  className="w-3 h-3 border border-gray-400"
                  style={{ background: "#22C55E", opacity: 0.7 }}
                />
                <span>Uni / High</span>
              </div>
              <div className="flex items-center gap-1">
                <span
                  className="w-3 h-3 border border-gray-400"
                  style={{ background: "#EAB308", opacity: 0.7 }}
                />
                <span>Moderate</span>
              </div>
              <div className="flex items-center gap-1">
                <span
                  className="w-3 h-3 border border-gray-400"
                  style={{ background: "#EF4444", opacity: 0.7 }}
                />
                <span>Low</span>
              </div>
              <div className="flex items-center gap-1">
                <span className="w-3 h-3 border border-gray-300 bg-white" />
                <span>None</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Filter */}
      <div className="filter-bar mx-0 border-x-0 border-t-0">
        <label className="font-mono text-[0.625rem] uppercase tracking-wider text-gray-500">
          Domain:
        </label>
        <select
          className="filter-select"
          value={domainFilter}
          onChange={(e) => setDomainFilter(e.target.value)}
        >
          <option value="">All Domains</option>
          {DOMAINS.map((d) => (
            <option key={d} value={d}>
              {d}
            </option>
          ))}
        </select>
        {domainFilter && (
          <button className="btn btn-sm" onClick={() => setDomainFilter("")}>
            CLEAR
          </button>
        )}
      </div>

      {/* Matrix + Detail */}
      <div className="flex flex-1 overflow-hidden">
        <div className="flex-1 overflow-auto" ref={scrollRef}>
          <div className="p-2" style={{ minWidth: flatIndices.length * 28 + 140 }}>
            <table className="border-collapse" style={{ tableLayout: "fixed" }}>
              <thead>
                <tr>
                  <th
                    className="sticky left-0 z-10 bg-white border border-gray-300"
                    style={{ width: 140, minWidth: 140 }}
                  />
                  {groupedIndices.map((group) => (
                    <th
                      key={group.domain}
                      colSpan={group.indices.length}
                      className="text-center font-mono text-[0.5625rem] uppercase tracking-wider py-1 border border-gray-300"
                      style={{
                        backgroundColor: `${DOMAIN_COLORS[group.domain] || "#6B7280"}15`,
                        color: DOMAIN_COLORS[group.domain] || "#6B7280",
                      }}
                    >
                      {group.domain}
                    </th>
                  ))}
                </tr>
                <tr>
                  <th
                    className="sticky left-0 z-10 bg-white border border-gray-300"
                    style={{ width: 140, minWidth: 140 }}
                  />
                  {flatIndices.map((idx) => (
                    <th
                      key={idx}
                      className="border border-gray-300 p-0"
                      style={{ width: 26, minWidth: 26 }}
                    >
                      <div
                        className="font-mono text-[0.5rem] font-bold whitespace-nowrap overflow-hidden"
                        style={{
                          writingMode: "vertical-lr",
                          transform: "rotate(180deg)",
                          height: 80,
                          lineHeight: "26px",
                          textAlign: "left",
                          paddingTop: 4,
                          color: DOMAIN_COLORS[systems[idx]?.domain] || "#000",
                        }}
                        title={systems[idx]?.name}
                      >
                        {systems[idx]?.acronym}
                      </div>
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {flatIndices.map((rowIdx) => (
                  <tr key={rowIdx}>
                    <td
                      className="sticky left-0 z-10 bg-white border border-gray-300 px-2 py-0"
                      style={{ width: 140, minWidth: 140 }}
                    >
                      <div className="flex items-center gap-1">
                        <span
                          className="w-1.5 h-3 flex-shrink-0"
                          style={{
                            backgroundColor:
                              DOMAIN_COLORS[systems[rowIdx]?.domain] || "#6B7280",
                          }}
                        />
                        <span
                          className="font-mono text-[0.5625rem] font-bold truncate"
                          title={systems[rowIdx]?.name}
                        >
                          {systems[rowIdx]?.acronym}
                        </span>
                      </div>
                    </td>
                    {flatIndices.map((colIdx) => {
                      const conn = matrix[rowIdx]?.[colIdx];
                      const isSelf = rowIdx === colIdx;
                      return (
                        <td
                          key={colIdx}
                          className={`border border-gray-200 p-0 ${
                            isSelf ? "" : "cursor-pointer hover:outline hover:outline-2 hover:outline-black hover:z-10"
                          }`}
                          style={{
                            width: 26,
                            height: 26,
                            minWidth: 26,
                            background: isSelf
                              ? "#E5E7EB"
                              : getCellColor(conn),
                            opacity: isSelf ? 1 : getCellOpacity(conn),
                          }}
                          onClick={() =>
                            !isSelf && handleCellClick(rowIdx, colIdx)
                          }
                          title={
                            isSelf
                              ? systems[rowIdx]?.name
                              : conn
                              ? `${systems[rowIdx]?.acronym} -> ${systems[colIdx]?.acronym}: ${conn.reliability} (${conn.direction})`
                              : `No connection: ${systems[rowIdx]?.acronym} -> ${systems[colIdx]?.acronym}`
                          }
                        />
                      );
                    })}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Detail Panel */}
        {cellDetail && (
          <div className="w-[360px] border-l-2 border-black overflow-auto flex-shrink-0">
            <div className="panel border-0">
              <div className="panel-header flex items-center justify-between">
                <span className="text-sm">Connection Detail</span>
                <button
                  className="btn btn-sm"
                  onClick={() => setCellDetail(null)}
                >
                  CLOSE
                </button>
              </div>
              <div className="panel-body space-y-3">
                <div className="flex items-center gap-2">
                  <div className="text-center">
                    <DomainBadge domain={cellDetail.sourceSystem.domain} />
                    <p className="font-mono text-xs font-bold mt-1">
                      {cellDetail.sourceSystem.acronym}
                    </p>
                    <p className="text-[0.625rem] text-gray-600">
                      {cellDetail.sourceSystem.name}
                    </p>
                  </div>
                  <div className="flex-1 text-center font-mono text-xs text-gray-500">
                    {cellDetail.connection.direction === "bidirectional"
                      ? "<--->"
                      : "--->"}
                  </div>
                  <div className="text-center">
                    <DomainBadge domain={cellDetail.targetSystem.domain} />
                    <p className="font-mono text-xs font-bold mt-1">
                      {cellDetail.targetSystem.acronym}
                    </p>
                    <p className="text-[0.625rem] text-gray-600">
                      {cellDetail.targetSystem.name}
                    </p>
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-2 text-xs">
                  <div>
                    <span className="font-mono text-[0.5625rem] uppercase text-gray-500">
                      Direction
                    </span>
                    <p className="font-mono font-medium">
                      {cellDetail.connection.direction}
                    </p>
                  </div>
                  <div>
                    <span className="font-mono text-[0.5625rem] uppercase text-gray-500">
                      Reliability
                    </span>
                    <p
                      className="font-mono font-medium"
                      style={{
                        color:
                          cellDetail.connection.reliability === "high"
                            ? "#16A34A"
                            : cellDetail.connection.reliability === "moderate"
                            ? "#CA8A04"
                            : "#DC2626",
                      }}
                    >
                      {cellDetail.connection.reliability}
                    </p>
                  </div>
                  <div>
                    <span className="font-mono text-[0.5625rem] uppercase text-gray-500">
                      Format
                    </span>
                    <p className="font-mono">{cellDetail.connection.format}</p>
                  </div>
                  <div>
                    <span className="font-mono text-[0.5625rem] uppercase text-gray-500">
                      Frequency
                    </span>
                    <p className="font-mono">{cellDetail.connection.frequency}</p>
                  </div>
                </div>

                <div>
                  <span className="font-mono text-[0.5625rem] uppercase text-gray-500">
                    Governing Agreement
                  </span>
                  <p className="text-xs">{cellDetail.connection.governing_agreement}</p>
                </div>

                <div>
                  <span className="font-mono text-[0.5625rem] uppercase text-gray-500">
                    Privacy Law
                  </span>
                  <p className="text-xs font-mono">
                    {cellDetail.connection.privacy_law}
                  </p>
                </div>

                <div>
                  <span className="font-mono text-[0.5625rem] uppercase text-gray-500">
                    Description
                  </span>
                  <p className="text-xs">{cellDetail.connection.description}</p>
                </div>

                <div>
                  <span className="font-mono text-[0.5625rem] uppercase text-gray-500">
                    Data Shared ({cellDetail.connection.data_shared?.length || 0})
                  </span>
                  <div className="flex flex-wrap gap-1 mt-1">
                    {cellDetail.connection.data_shared?.map((field) => (
                      <span
                        key={field}
                        className="font-mono text-[0.5625rem] px-1.5 py-0.5 border border-gray-300 bg-gray-50"
                      >
                        {field}
                      </span>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
