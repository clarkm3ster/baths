import type { ParcelFull } from "../types";
import { AGENCY_LABELS, CATEGORY_LABELS } from "../types";

interface ParcelDetailProps {
  parcel: ParcelFull | null;
  loading: boolean;
  onClose: () => void;
}

export default function ParcelDetail({ parcel, loading, onClose }: ParcelDetailProps) {
  if (!parcel && !loading) return null;

  return (
    <div style={{
      position: "absolute",
      top: 0,
      right: 0,
      width: 380,
      height: "100%",
      background: "#0A0A0A",
      borderLeft: "1px solid #1F1F1F",
      zIndex: 10,
      overflowY: "auto",
      display: "flex",
      flexDirection: "column",
    }}>
      {/* Header */}
      <div style={{
        display: "flex",
        justifyContent: "space-between",
        alignItems: "flex-start",
        padding: "16px 16px 0",
      }}>
        <div style={{ flex: 1 }}>
          {loading ? (
            <div style={{ height: 20, width: 200, background: "#1F1F1F", marginBottom: 8 }} />
          ) : parcel ? (
            <>
              <div style={{
                fontFamily: "'JetBrains Mono', monospace",
                fontSize: 11,
                color: "#666",
                marginBottom: 4,
              }}>
                {parcel.parcel_number}
              </div>
              <div style={{ fontSize: 16, fontWeight: 600 }}>{parcel.address}</div>
            </>
          ) : null}
        </div>
        <button
          onClick={onClose}
          style={{
            background: "transparent",
            border: "none",
            color: "#666",
            cursor: "pointer",
            fontSize: 20,
            lineHeight: 1,
            padding: 4,
          }}
        >
          &times;
        </button>
      </div>

      {parcel && (
        <div style={{ padding: 16, flex: 1 }}>
          {/* Score */}
          <div style={{
            background: "#141414",
            padding: 16,
            marginBottom: 16,
            border: "1px solid #1F1F1F",
          }}>
            <div style={{ fontSize: 10, color: "#666", textTransform: "uppercase", letterSpacing: "0.05em", marginBottom: 8 }}>
              Activation Score
            </div>
            <div style={{ display: "flex", alignItems: "baseline", gap: 8, marginBottom: 10 }}>
              <span style={{
                fontFamily: "'JetBrains Mono', monospace",
                fontSize: 36,
                fontWeight: 700,
                color: "#fff",
              }}>
                {parcel.activation_score}
              </span>
              <span style={{ fontSize: 14, color: "#666" }}>/ 100</span>
            </div>
            <div style={{ height: 4, background: "#1F1F1F", width: "100%" }}>
              <div style={{
                height: "100%",
                width: `${parcel.activation_score}%`,
                background: `linear-gradient(90deg, #333 0%, #fff ${Math.min(100, parcel.activation_score + 20)}%)`,
                transition: "width 0.3s",
              }} />
            </div>
          </div>

          {/* Categories */}
          <div style={{ display: "flex", flexWrap: "wrap", gap: 6, marginBottom: 16 }}>
            {parcel.activation_categories.map((cat) => (
              <span key={cat} style={{
                fontSize: 10,
                padding: "3px 8px",
                border: "1px solid #2A2A2A",
                color: "#999",
                textTransform: "uppercase",
                letterSpacing: "0.03em",
              }}>
                {CATEGORY_LABELS[cat] || cat}
              </span>
            ))}
            {parcel.vacancy_likely && (
              <span style={{
                fontSize: 10,
                padding: "3px 8px",
                border: "1px solid #444",
                color: "#fff",
                textTransform: "uppercase",
                letterSpacing: "0.03em",
              }}>
                Vacant
              </span>
            )}
          </div>

          {/* Owner */}
          <Row label="Owner" value={AGENCY_LABELS[parcel.owner_agency] || parcel.owner} />
          <Row label="Category" value={parcel.category_description || "—"} />
          <Row label="Zoning" value={parcel.zoning || "—"} />

          {/* Physical */}
          <Divider />
          <SectionTitle>Physical</SectionTitle>
          <Row label="Lot Size" value={`${parcel.total_area_sqft.toLocaleString()} sqft`} />
          <Row label="Frontage" value={parcel.frontage ? `${parcel.frontage} ft` : "—"} />
          <Row label="Depth" value={parcel.depth ? `${parcel.depth} ft` : "—"} />
          <Row label="Condition" value={parcel.exterior_condition || "—"} />
          <Row label="Year Built" value={parcel.year_built || "—"} />
          <Row label="Ward" value={parcel.geographic_ward || "—"} />
          <Row label="Zip" value={parcel.zip_code || "—"} />

          {/* Value */}
          <Divider />
          <SectionTitle>Value</SectionTitle>
          <Row label="Market Value" value={`$${parcel.market_value.toLocaleString()}`} />
          <Row label="Taxable Land" value={`$${parcel.taxable_land.toLocaleString()}`} />
          <Row label="Taxable Building" value={`$${parcel.taxable_building.toLocaleString()}`} />
          <Row label="Exempt Land" value={`$${parcel.exempt_land.toLocaleString()}`} />
          <Row label="Exempt Building" value={`$${parcel.exempt_building.toLocaleString()}`} />
        </div>
      )}
    </div>
  );
}

function Row({ label, value }: { label: string; value: string }) {
  return (
    <div style={{
      display: "flex",
      justifyContent: "space-between",
      padding: "5px 0",
      fontSize: 12,
      borderBottom: "1px solid #141414",
    }}>
      <span style={{ color: "#666" }}>{label}</span>
      <span style={{ fontFamily: "'JetBrains Mono', monospace", color: "#ccc" }}>{value}</span>
    </div>
  );
}

function Divider() {
  return <div style={{ height: 1, background: "#1F1F1F", margin: "12px 0" }} />;
}

function SectionTitle({ children }: { children: React.ReactNode }) {
  return (
    <div style={{
      fontSize: 10,
      color: "#666",
      textTransform: "uppercase",
      letterSpacing: "0.05em",
      marginBottom: 8,
    }}>
      {children}
    </div>
  );
}
