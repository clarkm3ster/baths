import { useState } from "react";
import type { ParcelSummary } from "../types";
import { AGENCY_LABELS } from "../types";

interface ListViewProps {
  parcels: ParcelSummary[];
  total: number;
  loading: boolean;
  onParcelClick: (id: string) => void;
  onLoadMore: () => void;
}

type SortKey = "activation_score" | "total_area_sqft" | "market_value" | "address";

export default function ListView({ parcels, total, loading, onParcelClick, onLoadMore }: ListViewProps) {
  const [sortKey, setSortKey] = useState<SortKey>("activation_score");
  const [sortAsc, setSortAsc] = useState(false);

  const sorted = [...parcels].sort((a, b) => {
    const av = a[sortKey] ?? 0;
    const bv = b[sortKey] ?? 0;
    if (typeof av === "string" && typeof bv === "string") {
      return sortAsc ? av.localeCompare(bv) : bv.localeCompare(av);
    }
    return sortAsc ? Number(av) - Number(bv) : Number(bv) - Number(av);
  });

  const toggleSort = (key: SortKey) => {
    if (sortKey === key) setSortAsc(!sortAsc);
    else { setSortKey(key); setSortAsc(false); }
  };

  const arrow = (key: SortKey) => sortKey === key ? (sortAsc ? " \u2191" : " \u2193") : "";

  return (
    <div style={{ flex: 1, overflow: "auto", background: "#0A0A0A" }}>
      <div style={{ padding: "12px 16px", fontSize: 12, color: "#666", borderBottom: "1px solid #1F1F1F" }}>
        {total.toLocaleString()} parcels
      </div>
      <table style={{ width: "100%", borderCollapse: "collapse", fontSize: 12 }}>
        <thead>
          <tr style={{ borderBottom: "1px solid #1F1F1F" }}>
            <Th onClick={() => toggleSort("address")}>Address{arrow("address")}</Th>
            <Th>Owner</Th>
            <Th onClick={() => toggleSort("activation_score")} align="right">Score{arrow("activation_score")}</Th>
            <Th onClick={() => toggleSort("total_area_sqft")} align="right">Area{arrow("total_area_sqft")}</Th>
            <Th onClick={() => toggleSort("market_value")} align="right">Value{arrow("market_value")}</Th>
            <Th>Zoning</Th>
          </tr>
        </thead>
        <tbody>
          {sorted.map((p) => (
            <tr
              key={p.parcel_number}
              onClick={() => onParcelClick(p.parcel_number)}
              style={{ cursor: "pointer", borderBottom: "1px solid #141414" }}
              onMouseOver={(e) => (e.currentTarget.style.background = "#141414")}
              onMouseOut={(e) => (e.currentTarget.style.background = "")}
            >
              <td style={cellStyle}>{p.address}</td>
              <td style={{ ...cellStyle, color: "#666" }}>
                {AGENCY_LABELS[p.owner_agency] || p.owner_agency}
              </td>
              <td style={{ ...cellStyle, textAlign: "right", fontFamily: "'JetBrains Mono', monospace" }}>
                {p.activation_score}
              </td>
              <td style={{ ...cellStyle, textAlign: "right", fontFamily: "'JetBrains Mono', monospace" }}>
                {p.total_area_sqft.toLocaleString()}
              </td>
              <td style={{ ...cellStyle, textAlign: "right", fontFamily: "'JetBrains Mono', monospace" }}>
                ${p.market_value.toLocaleString()}
              </td>
              <td style={{ ...cellStyle, fontFamily: "'JetBrains Mono', monospace", color: "#666" }}>
                {p.zoning}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      {parcels.length < total && (
        <div style={{ padding: 16, textAlign: "center" }}>
          <button
            onClick={onLoadMore}
            disabled={loading}
            style={{
              padding: "8px 24px",
              background: "#141414",
              border: "1px solid #2A2A2A",
              color: "#999",
              cursor: "pointer",
              fontSize: 12,
            }}
          >
            {loading ? "Loading..." : "Load More"}
          </button>
        </div>
      )}
    </div>
  );
}

function Th({ children, onClick, align }: { children: React.ReactNode; onClick?: () => void; align?: string }) {
  return (
    <th
      onClick={onClick}
      style={{
        padding: "8px 12px",
        textAlign: (align as CanvasTextAlign) || "left",
        color: "#666",
        fontWeight: 500,
        fontSize: 10,
        textTransform: "uppercase",
        letterSpacing: "0.05em",
        cursor: onClick ? "pointer" : undefined,
        userSelect: "none",
        position: "sticky",
        top: 0,
        background: "#0A0A0A",
      }}
    >
      {children}
    </th>
  );
}

const cellStyle: React.CSSProperties = {
  padding: "8px 12px",
  whiteSpace: "nowrap",
  overflow: "hidden",
  textOverflow: "ellipsis",
  maxWidth: 200,
};
