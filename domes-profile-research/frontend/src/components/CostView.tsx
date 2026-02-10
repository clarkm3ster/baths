import { useState } from "react";
import type { CompositeProfile, CostItem } from "../types";
import { DOMAIN_COLORS, DOMAIN_LABELS } from "../types";

interface Props {
  profile: CompositeProfile;
}

type CostMode = "fragmented" | "coordinated";

export default function CostView({ profile }: Props) {
  const [mode, setMode] = useState<CostMode>("fragmented");
  const { cost_breakdown, total_annual_cost, coordinated_cost, name } = profile;
  const savings = total_annual_cost - coordinated_cost;
  const savingsPct = total_annual_cost > 0 ? (savings / total_annual_cost) * 100 : 0;

  // Group by domain
  const byDomain: Record<string, CostItem[]> = {};
  for (const item of cost_breakdown) {
    if (!byDomain[item.domain]) byDomain[item.domain] = [];
    byDomain[item.domain].push(item);
  }

  // Domain-level coordinated costs (apply savings proportionally)
  const domainCoordinated: Record<string, { fragmented: number; coordinated: number; savings: number; savingsPct: number }> = {};
  const totalFragmented = total_annual_cost || 1;
  for (const [domain, items] of Object.entries(byDomain)) {
    const domainTotal = items.reduce((s, i) => s + i.annual_cost, 0);
    const proportion = domainTotal / totalFragmented;
    const domainCoord = coordinated_cost * proportion;
    const domainSavings = domainTotal - domainCoord;
    const domainSavingsPct = domainTotal > 0 ? (domainSavings / domainTotal) * 100 : 0;
    domainCoordinated[domain] = {
      fragmented: domainTotal,
      coordinated: domainCoord,
      savings: domainSavings,
      savingsPct: domainSavingsPct,
    };
  }

  const maxCost = Math.max(...cost_breakdown.map((c) => c.annual_cost), 1);
  const maxDomainCost = Math.max(
    ...Object.values(domainCoordinated).map((d) => d.fragmented),
    1
  );

  const isCoordinated = mode === "coordinated";
  const displayTotal = isCoordinated ? coordinated_cost : total_annual_cost;

  return (
    <div style={{ padding: "32px 40px", maxWidth: "860px" }}>
      {/* Header */}
      <h3
        style={{
          fontFamily: "var(--font-serif)",
          fontSize: "26px",
          fontWeight: 700,
          marginBottom: "6px",
          letterSpacing: "-0.02em",
        }}
      >
        What {name} costs the government
      </h3>
      <p
        style={{
          fontFamily: "var(--font-serif)",
          fontStyle: "italic",
          fontSize: "15px",
          color: "var(--color-text-secondary)",
          marginBottom: "28px",
          lineHeight: 1.5,
        }}
      >
        Every dollar sourced from published federal data.
        {isCoordinated
          ? " What if systems actually shared data?"
          : " None of it is coordinated."}
      </p>

      {/* Toggle */}
      <div
        style={{
          display: "flex",
          gap: "0",
          marginBottom: "32px",
        }}
      >
        <button
          onClick={() => setMode("fragmented")}
          style={{
            padding: "10px 24px",
            background: !isCoordinated ? "#000000" : "#FFFFFF",
            color: !isCoordinated ? "#FFFFFF" : "var(--color-text-secondary)",
            border: "2px solid #000000",
            borderRight: "none",
            cursor: "pointer",
            fontSize: "12px",
            fontFamily: "var(--font-mono)",
            fontWeight: 600,
            textTransform: "uppercase",
            letterSpacing: "0.06em",
          }}
        >
          Fragmented
        </button>
        <button
          onClick={() => setMode("coordinated")}
          style={{
            padding: "10px 24px",
            background: isCoordinated ? "#000000" : "#FFFFFF",
            color: isCoordinated ? "#FFFFFF" : "var(--color-text-secondary)",
            border: "2px solid #000000",
            cursor: "pointer",
            fontSize: "12px",
            fontFamily: "var(--font-mono)",
            fontWeight: 600,
            textTransform: "uppercase",
            letterSpacing: "0.06em",
          }}
        >
          Coordinated
        </button>
      </div>

      {/* Big number */}
      <div
        style={{
          borderTop: "2px solid #000000",
          padding: "24px 0",
          marginBottom: "12px",
        }}
      >
        <div className="section-label">
          {isCoordinated ? "Coordinated (possible)" : "Fragmented (current)"}
        </div>
        <div
          className="stat-number"
          style={{
            color: isCoordinated ? "var(--color-savings)" : "var(--color-cost)",
            transition: "color 0.3s ease",
          }}
        >
          <span style={{ transition: "opacity 0.3s ease" }}>
            ${Math.round(displayTotal).toLocaleString()}
          </span>
        </div>
        <div
          style={{
            fontSize: "12px",
            fontFamily: "var(--font-mono)",
            color: "var(--color-text-tertiary)",
            marginTop: "4px",
          }}
        >
          per year
          {isCoordinated && ` (${savingsPct.toFixed(0)}% less)`}
        </div>
      </div>

      {/* Savings callout -- only in coordinated mode */}
      {isCoordinated && (
        <div
          style={{
            padding: "24px",
            border: "2px solid var(--color-savings)",
            marginBottom: "40px",
            background: "#FFFFFF",
          }}
        >
          <div
            style={{
              fontFamily: "var(--font-serif)",
              fontSize: "22px",
              fontWeight: 700,
              color: "var(--color-savings)",
              marginBottom: "8px",
            }}
          >
            ${savings.toLocaleString()} saved per year
          </div>
          <p
            style={{
              fontSize: "14px",
              lineHeight: 1.6,
              color: "var(--color-text-secondary)",
              margin: 0,
            }}
          >
            Coordination across {profile.systems_involved.length} systems
            reduces spending by {savingsPct.toFixed(0)}%.
            Published research shows integrated case management, shared data
            layers, and cross-system referrals eliminate duplication
            and prevent costly crises.
          </p>
        </div>
      )}

      {/* Fragmented callout -- only in fragmented mode */}
      {!isCoordinated && (
        <div
          style={{
            padding: "24px",
            border: "2px solid var(--color-cost)",
            marginBottom: "40px",
            background: "#FFFFFF",
          }}
        >
          <div
            style={{
              fontFamily: "var(--font-serif)",
              fontSize: "22px",
              fontWeight: 700,
              color: "var(--color-cost)",
              marginBottom: "8px",
            }}
          >
            ${savings.toLocaleString()} wasted every year
          </div>
          <p
            style={{
              fontSize: "14px",
              lineHeight: 1.6,
              color: "var(--color-text-secondary)",
              margin: 0,
            }}
          >
            This is the cost of fragmentation for one person. The government
            spends ${total_annual_cost.toLocaleString()} per year on {name} --
            across {profile.systems_involved.length} systems that don't share
            data. If they coordinated, published research shows costs drop by{" "}
            {savingsPct.toFixed(0)}%.
          </p>
        </div>
      )}

      {/* FRAGMENTED mode: cost breakdown by system */}
      {!isCoordinated &&
        Object.entries(byDomain).map(([domain, items]) => {
          const domainTotal = items.reduce((s, i) => s + i.annual_cost, 0);
          const color = DOMAIN_COLORS[domain] || "#333";

          return (
            <div key={domain} style={{ marginBottom: "32px" }}>
              <div
                style={{
                  display: "flex",
                  justifyContent: "space-between",
                  alignItems: "baseline",
                  marginBottom: "12px",
                }}
              >
                <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
                  <span
                    style={{
                      width: "10px",
                      height: "10px",
                      background: color,
                      display: "inline-block",
                    }}
                  />
                  <span
                    style={{
                      fontFamily: "var(--font-mono)",
                      fontSize: "13px",
                      fontWeight: 600,
                      textTransform: "uppercase",
                      letterSpacing: "0.04em",
                    }}
                  >
                    {DOMAIN_LABELS[domain] || domain}
                  </span>
                </div>
                <span
                  style={{
                    fontFamily: "var(--font-mono)",
                    fontSize: "16px",
                    fontWeight: 600,
                  }}
                >
                  ${domainTotal.toLocaleString()}
                </span>
              </div>

              {items.map((item) => {
                const pct = (item.annual_cost / maxCost) * 100;
                return (
                  <div
                    key={item.system_id}
                    style={{
                      marginBottom: "8px",
                      borderBottom: "1px solid var(--color-border-light)",
                      paddingBottom: "8px",
                    }}
                  >
                    <div
                      style={{
                        display: "flex",
                        justifyContent: "space-between",
                        alignItems: "baseline",
                        marginBottom: "4px",
                      }}
                    >
                      <span style={{ fontSize: "13px" }}>
                        <span
                          style={{
                            fontFamily: "var(--font-mono)",
                            fontSize: "12px",
                            color,
                            marginRight: "8px",
                          }}
                        >
                          {item.acronym}
                        </span>
                        {item.system_name}
                      </span>
                      <span
                        style={{
                          fontFamily: "var(--font-mono)",
                          fontSize: "14px",
                          fontWeight: 500,
                        }}
                      >
                        ${item.annual_cost.toLocaleString()}
                      </span>
                    </div>

                    {/* Cost bar */}
                    <div className="cost-bar">
                      <div
                        className="cost-bar__fill"
                        style={{ width: `${pct}%`, background: color, opacity: 0.2 }}
                      />
                    </div>

                    {/* Source */}
                    <div
                      style={{
                        fontSize: "11px",
                        fontFamily: "var(--font-mono)",
                        color: "var(--color-text-tertiary)",
                        marginTop: "4px",
                      }}
                    >
                      Source: {item.source}
                    </div>
                  </div>
                );
              })}
            </div>
          );
        })}

      {/* COORDINATED mode: domain-level with savings */}
      {isCoordinated &&
        Object.entries(domainCoordinated)
          .sort(([, a], [, b]) => b.savings - a.savings)
          .map(([domain, data]) => {
            const color = DOMAIN_COLORS[domain] || "#333";
            const coordPct = (data.coordinated / maxDomainCost) * 100;
            const fragPct = (data.fragmented / maxDomainCost) * 100;

            return (
              <div key={domain} style={{ marginBottom: "28px" }}>
                <div
                  style={{
                    display: "flex",
                    justifyContent: "space-between",
                    alignItems: "baseline",
                    marginBottom: "8px",
                  }}
                >
                  <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
                    <span
                      style={{
                        width: "10px",
                        height: "10px",
                        background: color,
                        display: "inline-block",
                      }}
                    />
                    <span
                      style={{
                        fontFamily: "var(--font-mono)",
                        fontSize: "13px",
                        fontWeight: 600,
                        textTransform: "uppercase",
                        letterSpacing: "0.04em",
                      }}
                    >
                      {DOMAIN_LABELS[domain] || domain}
                    </span>
                  </div>
                  <div style={{ textAlign: "right" }}>
                    <span
                      style={{
                        fontFamily: "var(--font-mono)",
                        fontSize: "16px",
                        fontWeight: 600,
                        color: "var(--color-savings)",
                      }}
                    >
                      ${Math.round(data.coordinated).toLocaleString()}
                    </span>
                    <span
                      style={{
                        fontFamily: "var(--font-mono)",
                        fontSize: "12px",
                        color: "var(--color-text-tertiary)",
                        marginLeft: "8px",
                        textDecoration: "line-through",
                      }}
                    >
                      ${data.fragmented.toLocaleString()}
                    </span>
                  </div>
                </div>

                {/* Stacked bars: coordinated over fragmented */}
                <div
                  style={{
                    position: "relative",
                    height: "28px",
                    background: "var(--color-surface-alt)",
                    marginBottom: "6px",
                  }}
                >
                  {/* Fragmented (ghost bar) */}
                  <div
                    style={{
                      position: "absolute",
                      left: 0,
                      top: 0,
                      bottom: 0,
                      width: `${fragPct}%`,
                      background: color,
                      opacity: 0.08,
                      transition: "width 0.6s ease-out",
                    }}
                  />
                  {/* Coordinated (solid bar) */}
                  <div
                    style={{
                      position: "absolute",
                      left: 0,
                      top: 0,
                      bottom: 0,
                      width: `${coordPct}%`,
                      background: color,
                      opacity: 0.3,
                      transition: "width 0.6s ease-out",
                    }}
                  />
                </div>

                {/* Savings line */}
                <div
                  style={{
                    fontFamily: "var(--font-mono)",
                    fontSize: "12px",
                    color: "var(--color-savings)",
                    fontWeight: 500,
                  }}
                >
                  -{data.savingsPct.toFixed(0)}% = ${Math.round(data.savings).toLocaleString()} saved
                </div>
              </div>
            );
          })}
    </div>
  );
}
