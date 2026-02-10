import type { CompositeProfile } from "../types";
import { DOMAIN_COLORS, DOMAIN_LABELS } from "../types";

interface Props {
  profile: CompositeProfile;
}

const ESTIMATED_POPULATION = 5000;

export default function CompareView({ profile }: Props) {
  const { name, total_annual_cost, coordinated_cost, cost_breakdown, matched_systems, timeline } = profile;
  const savings = total_annual_cost - coordinated_cost;
  const savingsPct = total_annual_cost > 0 ? (savings / total_annual_cost) * 100 : 0;

  // Count crisis/gap events in timeline
  const crisisEvents = timeline.filter((e) => e.type === "crisis").length;
  const gapEvents = timeline.filter((e) => e.type === "gap").length;

  // Domain totals
  const domainCosts: Record<string, number> = {};
  for (const item of cost_breakdown) {
    domainCosts[item.domain] = (domainCosts[item.domain] || 0) + item.annual_cost;
  }
  const sortedDomains = Object.entries(domainCosts).sort(([, a], [, b]) => b - a);
  const maxDomainCost = Math.max(...Object.values(domainCosts), 1);

  // Aggregate multiplier
  const aggregateWaste = savings * ESTIMATED_POPULATION;
  const aggregateWasteMillions = aggregateWaste / 1_000_000;

  return (
    <div style={{ padding: "32px 40px", maxWidth: "960px" }}>
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
        Two realities
      </h3>
      <p
        style={{
          fontFamily: "var(--font-serif)",
          fontStyle: "italic",
          fontSize: "15px",
          color: "var(--color-text-secondary)",
          marginBottom: "36px",
          lineHeight: 1.5,
        }}
      >
        Same person. Same circumstances. Same systems. The only difference is
        whether those systems share data.
      </p>

      {/* Side-by-side comparison */}
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "1fr 1fr",
          gap: "0",
          borderTop: "2px solid #000000",
        }}
      >
        {/* LEFT: Fragmented */}
        <div
          style={{
            padding: "28px 28px 28px 0",
            borderRight: "1px solid var(--color-border)",
          }}
        >
          <div className="section-label" style={{ color: "var(--color-cost)" }}>
            Fragmented (today)
          </div>
          <div
            className="stat-number"
            style={{ color: "var(--color-cost)", marginBottom: "20px" }}
          >
            ${total_annual_cost.toLocaleString()}
            <span
              style={{
                fontSize: "14px",
                fontWeight: 400,
                color: "var(--color-text-tertiary)",
                marginLeft: "6px",
              }}
            >
              /year
            </span>
          </div>

          <div style={{ display: "flex", flexDirection: "column", gap: "16px" }}>
            <CompareRow label="Systems" value={`${matched_systems.length} separate databases`} />
            <CompareRow label="Case plans" value={`${matched_systems.length} uncoordinated plans`} />
            <CompareRow label="Data sharing" value="None" accent />
            <CompareRow label="Applications" value={`${matched_systems.length} separate applications`} />
            <CompareRow label="Times retelling story" value={`${matched_systems.length}+`} />
            <CompareRow label="Crisis events" value={`${crisisEvents} per year`} accent />
            <CompareRow label="Data gaps" value={`${gapEvents} critical gaps`} accent />
          </div>

          {/* What happens */}
          <div
            style={{
              marginTop: "28px",
              padding: "20px",
              borderLeft: "3px solid var(--color-cost)",
              background: "var(--color-surface)",
            }}
          >
            <div className="section-label">What happens</div>
            <p
              style={{
                fontFamily: "var(--font-serif)",
                fontSize: "16px",
                lineHeight: 1.5,
                margin: 0,
              }}
            >
              {name} cycles between ER, jail, and shelter. Every system starts
              from scratch. Medications get restarted. Housing applications
              expire. The government spends ${total_annual_cost.toLocaleString()}{" "}
              and nothing improves.
            </p>
          </div>
        </div>

        {/* RIGHT: Coordinated */}
        <div style={{ padding: "28px 0 28px 28px" }}>
          <div className="section-label" style={{ color: "var(--color-savings)" }}>
            Coordinated (possible)
          </div>
          <div
            className="stat-number"
            style={{ color: "var(--color-savings)", marginBottom: "20px" }}
          >
            ${coordinated_cost.toLocaleString()}
            <span
              style={{
                fontSize: "14px",
                fontWeight: 400,
                color: "var(--color-text-tertiary)",
                marginLeft: "6px",
              }}
            >
              /year
            </span>
          </div>

          <div style={{ display: "flex", flexDirection: "column", gap: "16px" }}>
            <CompareRow label="Systems" value={`${matched_systems.length} with shared data layer`} />
            <CompareRow label="Case plans" value="1 unified plan" good />
            <CompareRow label="Data sharing" value="Real-time, consent-based" good />
            <CompareRow label="Applications" value="1 universal application" good />
            <CompareRow label="Times retelling story" value="Once" good />
            <CompareRow label="Crisis events" value="Prevented by coordination" good />
            <CompareRow label="Data gaps" value="Closed" good />
          </div>

          {/* What happens */}
          <div
            style={{
              marginTop: "28px",
              padding: "20px",
              borderLeft: "3px solid var(--color-savings)",
              background: "var(--color-surface)",
            }}
          >
            <div className="section-label">What happens</div>
            <p
              style={{
                fontFamily: "var(--font-serif)",
                fontSize: "16px",
                lineHeight: 1.5,
                margin: 0,
              }}
            >
              {name}'s treatment history follows him. His probation officer
              sees treatment compliance. The housing authority knows he's
              high-cost. He gets a voucher in weeks, not years. His
              medications continue through transitions. The cycle breaks.
            </p>
          </div>
        </div>
      </div>

      {/* Cost waterfall: stacked bars side by side */}
      <div
        style={{
          marginTop: "48px",
          borderTop: "2px solid #000000",
          paddingTop: "28px",
        }}
      >
        <h4
          style={{
            fontFamily: "var(--font-serif)",
            fontSize: "22px",
            fontWeight: 700,
            marginBottom: "6px",
            letterSpacing: "-0.01em",
          }}
        >
          Where the money goes
        </h4>
        <p
          style={{
            fontFamily: "var(--font-serif)",
            fontStyle: "italic",
            fontSize: "14px",
            color: "var(--color-text-secondary)",
            marginBottom: "28px",
            lineHeight: 1.5,
          }}
        >
          Cost waterfall by domain. Left bar: fragmented. Right bar: coordinated.
        </p>

        <div style={{ display: "flex", flexDirection: "column", gap: "16px" }}>
          {sortedDomains.map(([domain, cost]) => {
            const color = DOMAIN_COLORS[domain] || "#333";
            const fragPct = (cost / maxDomainCost) * 100;
            // Proportional coordinated cost for this domain
            const proportion = cost / (total_annual_cost || 1);
            const coordCost = coordinated_cost * proportion;
            const coordPct = (coordCost / maxDomainCost) * 100;
            const domainSavings = cost - coordCost;

            return (
              <div key={domain}>
                {/* Domain label + numbers */}
                <div
                  style={{
                    display: "flex",
                    justifyContent: "space-between",
                    alignItems: "baseline",
                    marginBottom: "6px",
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
                        fontSize: "11px",
                        fontWeight: 600,
                        textTransform: "uppercase",
                        letterSpacing: "0.04em",
                        color,
                      }}
                    >
                      {DOMAIN_LABELS[domain] || domain}
                    </span>
                  </div>
                  <span
                    style={{
                      fontFamily: "var(--font-mono)",
                      fontSize: "11px",
                      color: "var(--color-savings)",
                      fontWeight: 500,
                    }}
                  >
                    -${Math.round(domainSavings).toLocaleString()}
                  </span>
                </div>

                {/* Fragmented bar */}
                <div
                  style={{
                    position: "relative",
                    height: "20px",
                    background: "var(--color-surface-alt)",
                    marginBottom: "3px",
                  }}
                >
                  <div
                    style={{
                      position: "absolute",
                      left: 0,
                      top: 0,
                      bottom: 0,
                      width: `${fragPct}%`,
                      background: color,
                      opacity: 0.25,
                      transition: "width 0.6s ease-out",
                    }}
                  />
                  <div
                    style={{
                      position: "absolute",
                      right: "4px",
                      top: "2px",
                      fontFamily: "var(--font-mono)",
                      fontSize: "10px",
                      color: "var(--color-text-tertiary)",
                    }}
                  >
                    ${cost.toLocaleString()}
                  </div>
                </div>

                {/* Coordinated bar */}
                <div
                  style={{
                    position: "relative",
                    height: "20px",
                    background: "var(--color-surface-alt)",
                  }}
                >
                  <div
                    style={{
                      position: "absolute",
                      left: 0,
                      top: 0,
                      bottom: 0,
                      width: `${coordPct}%`,
                      background: "var(--color-savings)",
                      opacity: 0.3,
                      transition: "width 0.6s ease-out",
                    }}
                  />
                  <div
                    style={{
                      position: "absolute",
                      right: "4px",
                      top: "2px",
                      fontFamily: "var(--font-mono)",
                      fontSize: "10px",
                      color: "var(--color-text-tertiary)",
                    }}
                  >
                    ${Math.round(coordCost).toLocaleString()}
                  </div>
                </div>
              </div>
            );
          })}
        </div>

        {/* Legend */}
        <div
          style={{
            display: "flex",
            gap: "24px",
            marginTop: "16px",
            paddingTop: "12px",
            borderTop: "1px solid var(--color-border-light)",
          }}
        >
          <div style={{ display: "flex", alignItems: "center", gap: "6px" }}>
            <span
              style={{
                width: "20px",
                height: "10px",
                background: "var(--color-text-tertiary)",
                opacity: 0.25,
                display: "inline-block",
              }}
            />
            <span
              style={{
                fontFamily: "var(--font-mono)",
                fontSize: "10px",
                color: "var(--color-text-tertiary)",
                textTransform: "uppercase",
              }}
            >
              Fragmented
            </span>
          </div>
          <div style={{ display: "flex", alignItems: "center", gap: "6px" }}>
            <span
              style={{
                width: "20px",
                height: "10px",
                background: "var(--color-savings)",
                opacity: 0.3,
                display: "inline-block",
              }}
            />
            <span
              style={{
                fontFamily: "var(--font-mono)",
                fontSize: "10px",
                color: "var(--color-text-tertiary)",
                textTransform: "uppercase",
              }}
            >
              Coordinated
            </span>
          </div>
        </div>
      </div>

      {/* Savings summary */}
      <div
        style={{
          marginTop: "36px",
          padding: "28px",
          border: "2px solid #000000",
          background: "#FFFFFF",
        }}
      >
        <div
          style={{
            fontFamily: "var(--font-serif)",
            fontSize: "24px",
            fontWeight: 700,
            marginBottom: "12px",
            lineHeight: 1.25,
          }}
        >
          The cost of not sharing data: ${savings.toLocaleString()} per year,
          per person
        </div>
        <p
          style={{
            fontSize: "14px",
            lineHeight: 1.6,
            color: "var(--color-text-secondary)",
            margin: "0 0 20px",
          }}
        >
          This is one composite person drawn from real data. Philadelphia has
          thousands of people in similar circumstances. The aggregate waste from
          system fragmentation runs into hundreds of millions per year -- with
          worse outcomes for everyone.
        </p>

        {/* Domain savings bars */}
        <div style={{ display: "flex", flexDirection: "column", gap: "8px" }}>
          {sortedDomains.map(([domain, cost]) => {
            const color = DOMAIN_COLORS[domain] || "#333";
            const pct = (cost / maxDomainCost) * 100;
            return (
              <div key={domain}>
                <div
                  style={{
                    display: "flex",
                    justifyContent: "space-between",
                    alignItems: "baseline",
                    marginBottom: "2px",
                  }}
                >
                  <span
                    style={{
                      fontFamily: "var(--font-mono)",
                      fontSize: "11px",
                      fontWeight: 500,
                      textTransform: "uppercase",
                      color,
                    }}
                  >
                    {DOMAIN_LABELS[domain] || domain}
                  </span>
                  <span
                    style={{
                      fontFamily: "var(--font-mono)",
                      fontSize: "13px",
                      fontWeight: 500,
                    }}
                  >
                    ${cost.toLocaleString()}
                  </span>
                </div>
                <div className="cost-bar" style={{ height: "16px" }}>
                  <div
                    className="cost-bar__fill"
                    style={{
                      width: `${pct}%`,
                      background: color,
                      opacity: 0.25,
                    }}
                  />
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Multiplier section */}
      <div
        style={{
          marginTop: "36px",
          padding: "32px",
          background: "#000000",
          color: "#FFFFFF",
        }}
      >
        <div className="section-label" style={{ color: "rgba(255,255,255,0.5)", marginBottom: "12px" }}>
          Scale
        </div>
        <div
          style={{
            fontFamily: "var(--font-serif)",
            fontSize: "28px",
            fontWeight: 700,
            lineHeight: 1.2,
            marginBottom: "16px",
          }}
        >
          If Philadelphia has ~{ESTIMATED_POPULATION.toLocaleString()} people in
          similar circumstances
        </div>
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "1fr 1fr 1fr",
            gap: "24px",
            paddingTop: "20px",
            borderTop: "1px solid rgba(255,255,255,0.15)",
          }}
        >
          <div>
            <div
              style={{
                fontFamily: "var(--font-mono)",
                fontSize: "32px",
                fontWeight: 500,
                lineHeight: 1,
                color: "var(--color-cost)",
                marginBottom: "6px",
              }}
            >
              ${Math.round(total_annual_cost * ESTIMATED_POPULATION / 1_000_000).toLocaleString()}M
            </div>
            <div
              style={{
                fontFamily: "var(--font-mono)",
                fontSize: "10px",
                textTransform: "uppercase",
                letterSpacing: "0.06em",
                color: "rgba(255,255,255,0.5)",
              }}
            >
              Total fragmented spend
            </div>
          </div>
          <div>
            <div
              style={{
                fontFamily: "var(--font-mono)",
                fontSize: "32px",
                fontWeight: 500,
                lineHeight: 1,
                color: "#FFFFFF",
                marginBottom: "6px",
              }}
            >
              ${aggregateWasteMillions < 1
                ? `${Math.round(aggregateWaste / 1000).toLocaleString()}K`
                : `${aggregateWasteMillions.toFixed(1)}M`}
            </div>
            <div
              style={{
                fontFamily: "var(--font-mono)",
                fontSize: "10px",
                textTransform: "uppercase",
                letterSpacing: "0.06em",
                color: "rgba(255,255,255,0.5)",
              }}
            >
              Annual waste from fragmentation
            </div>
          </div>
          <div>
            <div
              style={{
                fontFamily: "var(--font-mono)",
                fontSize: "32px",
                fontWeight: 500,
                lineHeight: 1,
                color: "var(--color-savings)",
                marginBottom: "6px",
              }}
            >
              {savingsPct.toFixed(0)}%
            </div>
            <div
              style={{
                fontFamily: "var(--font-mono)",
                fontSize: "10px",
                textTransform: "uppercase",
                letterSpacing: "0.06em",
                color: "rgba(255,255,255,0.5)",
              }}
            >
              Reducible through coordination
            </div>
          </div>
        </div>
        <p
          style={{
            fontSize: "13px",
            lineHeight: 1.6,
            color: "rgba(255,255,255,0.6)",
            marginTop: "20px",
            marginBottom: 0,
          }}
        >
          This multiplier is conservative. The actual number of people cycling
          through multiple systems simultaneously in a major city is likely higher.
          Every dollar of waste represents a failure of coordination, not a
          failure of individuals.
        </p>
      </div>
    </div>
  );
}

function CompareRow({
  label,
  value,
  accent,
  good,
}: {
  label: string;
  value: string;
  accent?: boolean;
  good?: boolean;
}) {
  return (
    <div>
      <div
        style={{
          fontSize: "11px",
          fontFamily: "var(--font-mono)",
          color: "var(--color-text-tertiary)",
          textTransform: "uppercase",
          letterSpacing: "0.06em",
          marginBottom: "2px",
        }}
      >
        {label}
      </div>
      <div
        style={{
          fontSize: "14px",
          fontWeight: 600,
          color: accent
            ? "var(--color-cost)"
            : good
              ? "var(--color-savings)"
              : "#000000",
        }}
      >
        {value}
      </div>
    </div>
  );
}
