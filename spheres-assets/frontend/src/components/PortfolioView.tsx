import { useState, useEffect } from "react";
import type { StaticValue, ActivationValue, LeveragedValue } from "../types";
import { AGENCY_LABELS, CATEGORY_LABELS } from "../types";
import { fetchStaticValue, fetchActivationValue, fetchLeveragedValue } from "../api/client";

function fmtM(n: number): string {
  if (n >= 1_000_000_000) return `$${(n / 1_000_000_000).toFixed(2)}B`;
  if (n >= 1_000_000) return `$${(n / 1_000_000).toFixed(2)}M`;
  if (n >= 1_000) return `$${(n / 1_000).toFixed(0)}K`;
  return `$${n.toFixed(0)}`;
}

export default function PortfolioView() {
  const [sv, setSv] = useState<StaticValue | null>(null);
  const [av, setAv] = useState<ActivationValue | null>(null);
  const [lv, setLv] = useState<LeveragedValue | null>(null);

  useEffect(() => {
    fetchStaticValue().then(setSv);
    fetchActivationValue().then(setAv);
    fetchLeveragedValue().then(setLv);
  }, []);

  return (
    <div style={{ flex: 1, overflow: "auto", background: "#0A0A0A", padding: 24 }}>
      <h1 style={{ fontSize: 20, fontWeight: 600, marginBottom: 4 }}>Portfolio Value</h1>
      <p style={{ fontSize: 12, color: "#666", marginBottom: 24 }}>
        Three-tier value analysis of Philadelphia's publicly-owned property
      </p>

      {/* Value Cards */}
      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(280px, 1fr))", gap: 16, marginBottom: 32 }}>
        <ValueCard
          title="Static Value"
          subtitle="Total assessed market value"
          value={sv ? fmtM(sv.total_value) : "—"}
          details={sv ? [
            `${sv.total_parcels.toLocaleString()} parcels`,
            `${sv.total_acres.toFixed(0)} acres`,
          ] : []}
        />
        <ValueCard
          title="Activation Value"
          subtitle="Projected annual revenue"
          value={av ? `${fmtM(av.annual_revenue)}/yr` : "—"}
          details={av ? Object.entries(av.by_category)
            .sort(([, a], [, b]) => b - a)
            .slice(0, 3)
            .map(([k, v]) => `${CATEGORY_LABELS[k] || k}: ${fmtM(v)}/yr`) : []}
        />
        <ValueCard
          title="Leveraged Value"
          subtitle="Total financial capacity"
          value={lv ? fmtM(lv.total_leveraged) : "—"}
          details={lv ? [
            `Bond capacity: ${fmtM(lv.bond_capacity)}`,
            `TIF potential: ${fmtM(lv.tif_potential)}`,
            `Grant match: ${fmtM(lv.grant_match)}`,
            `Private investment: ${fmtM(lv.private_investment)}`,
          ] : []}
        />
      </div>

      {/* By Agency */}
      {sv && (
        <div style={{ marginBottom: 32 }}>
          <h2 style={{ fontSize: 14, fontWeight: 600, marginBottom: 12 }}>By Agency</h2>
          <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(240px, 1fr))", gap: 8 }}>
            {Object.entries(sv.by_agency)
              .sort(([, a], [, b]) => b.total_value - a.total_value)
              .map(([agency, data]) => (
                <div key={agency} style={{
                  background: "#141414",
                  border: "1px solid #1F1F1F",
                  padding: 12,
                }}>
                  <div style={{ fontSize: 11, color: "#999", marginBottom: 4 }}>
                    {AGENCY_LABELS[agency] || agency}
                  </div>
                  <div style={{ fontFamily: "'JetBrains Mono', monospace", fontSize: 14, fontWeight: 600, marginBottom: 4 }}>
                    {fmtM(data.total_value)}
                  </div>
                  <div style={{ fontSize: 10, color: "#666" }}>
                    {data.count} parcels &middot; {(data.total_area_sqft / 43560).toFixed(0)} acres
                  </div>
                </div>
              ))}
          </div>
        </div>
      )}

      {/* Net Benefit */}
      {lv && (
        <div style={{
          background: "#141414",
          border: "1px solid #1F1F1F",
          padding: 16,
        }}>
          <div style={{ fontSize: 10, color: "#666", textTransform: "uppercase", letterSpacing: "0.05em", marginBottom: 8 }}>
            Net Activation Benefit
          </div>
          <div style={{ display: "flex", gap: 24, flexWrap: "wrap" }}>
            <div>
              <div style={{ fontSize: 11, color: "#666" }}>Annual Revenue</div>
              <div style={{ fontFamily: "'JetBrains Mono', monospace", fontSize: 16, fontWeight: 600 }}>
                {fmtM(lv.annual_activation_revenue)}
              </div>
            </div>
            <div>
              <div style={{ fontSize: 11, color: "#666" }}>Maintenance Cost</div>
              <div style={{ fontFamily: "'JetBrains Mono', monospace", fontSize: 16, fontWeight: 600 }}>
                {fmtM(lv.maintenance_cost_estimate)}
              </div>
            </div>
            <div>
              <div style={{ fontSize: 11, color: "#666" }}>Net Benefit</div>
              <div style={{
                fontFamily: "'JetBrains Mono', monospace",
                fontSize: 16,
                fontWeight: 600,
                color: lv.net_activation_benefit > 0 ? "#fff" : "#666",
              }}>
                {fmtM(lv.net_activation_benefit)}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

function ValueCard({ title, subtitle, value, details }: {
  title: string; subtitle: string; value: string; details: string[];
}) {
  return (
    <div style={{
      background: "#141414",
      border: "1px solid #1F1F1F",
      padding: 20,
    }}>
      <div style={{ fontSize: 10, color: "#666", textTransform: "uppercase", letterSpacing: "0.05em", marginBottom: 4 }}>
        {title}
      </div>
      <div style={{
        fontFamily: "'JetBrains Mono', monospace",
        fontSize: 28,
        fontWeight: 700,
        marginBottom: 4,
      }}>
        {value}
      </div>
      <div style={{ fontSize: 11, color: "#666", marginBottom: 8 }}>{subtitle}</div>
      {details.map((d, i) => (
        <div key={i} style={{ fontSize: 11, color: "#999", lineHeight: 1.5 }}>{d}</div>
      ))}
    </div>
  );
}
