import type { Stats } from "../types";

interface StatsBarProps {
  stats: Stats | null;
  loading: boolean;
}

function fmt(n: number): string {
  if (n >= 1_000_000_000) return `$${(n / 1_000_000_000).toFixed(1)}B`;
  if (n >= 1_000_000) return `$${(n / 1_000_000).toFixed(1)}M`;
  if (n >= 1_000) return `$${(n / 1_000).toFixed(0)}K`;
  return `$${n.toFixed(0)}`;
}

export default function StatsBar({ stats, loading }: StatsBarProps) {
  if (loading || !stats) {
    return (
      <div style={barStyle}>
        <span style={{ color: "#666", fontFamily: "'JetBrains Mono', monospace", fontSize: 12 }}>
          Loading parcel data...
        </span>
      </div>
    );
  }

  return (
    <div style={barStyle}>
      <Stat label="Parcels" value={stats.total_parcels.toLocaleString()} />
      <Sep />
      <Stat label="Acres" value={stats.total_acres.toFixed(0)} />
      <Sep />
      <Stat label="Dormant Value" value={fmt(stats.total_value)} />
      <Sep />
      <Stat label="Avg Score" value={String(stats.avg_activation_score)} />
      <Sep />
      <Stat label="Vacant" value={stats.vacant_count.toLocaleString()} />
    </div>
  );
}

function Stat({ label, value }: { label: string; value: string }) {
  return (
    <div style={{ display: "flex", alignItems: "baseline", gap: 6 }}>
      <span style={{
        fontFamily: "'JetBrains Mono', monospace",
        fontSize: 13,
        fontWeight: 600,
        color: "#fff",
      }}>
        {value}
      </span>
      <span style={{ fontSize: 10, color: "#666", textTransform: "uppercase", letterSpacing: "0.05em" }}>
        {label}
      </span>
    </div>
  );
}

function Sep() {
  return <div style={{ width: 1, height: 16, background: "#1F1F1F" }} />;
}

const barStyle: React.CSSProperties = {
  display: "flex",
  alignItems: "center",
  gap: 16,
  padding: "8px 16px",
  background: "#0A0A0A",
  borderBottom: "1px solid #1F1F1F",
  flexShrink: 0,
  overflowX: "auto",
};
