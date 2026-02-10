import type { Gap, System } from "../types";

interface Props {
  gaps: Gap[];
  systemMap: Map<string, System>;
  onGapClick: (gap: Gap) => void;
}

export default function ImpactView({ gaps, systemMap, onGapClick }: Props) {
  const impactGaps = gaps.filter((g) => g.impact);

  if (impactGaps.length === 0) {
    return (
      <div style={{ padding: "48px 32px", textAlign: "center" }}>
        <p
          style={{
            fontFamily: "var(--font-serif)",
            fontSize: "18px",
            color: "var(--color-text-tertiary)",
            fontStyle: "italic",
          }}
        >
          No impact data available for your constellation.
        </p>
      </div>
    );
  }

  return (
    <div style={{ padding: "32px", maxWidth: "800px" }}>
      {/* Section header */}
      <h3
        style={{
          fontFamily: "var(--font-serif)",
          fontSize: "26px",
          fontWeight: 700,
          marginBottom: "6px",
          letterSpacing: "-0.02em",
        }}
      >
        What this means for you
      </h3>
      <p
        style={{
          fontSize: "15px",
          color: "var(--color-text-secondary)",
          marginBottom: "32px",
          lineHeight: 1.5,
          fontFamily: "var(--font-serif)",
          fontStyle: "italic",
        }}
      >
        In plain English -- what happens because these systems don't talk to each
        other.
      </p>

      {/* Impact statements */}
      <div style={{ display: "flex", flexDirection: "column", gap: "0" }}>
        {impactGaps.map((g, i) => {
          const sA = systemMap.get(g.system_a_id);
          const sB = systemMap.get(g.system_b_id);
          const sevColor =
            g.severity === "critical"
              ? "#CC0000"
              : g.severity === "high"
                ? "#994400"
                : g.severity === "moderate"
                  ? "#666600"
                  : "#446644";

          return (
            <button
              key={g.id}
              onClick={() => onGapClick(g)}
              style={{
                display: "block",
                width: "100%",
                textAlign: "left",
                background: "#FFFFFF",
                border: "none",
                borderTop: i === 0 ? "2px solid #000000" : "1px solid var(--color-border)",
                padding: "24px 0",
                cursor: "pointer",
                fontFamily: "var(--font-sans)",
              }}
            >
              {/* System pair label */}
              <div
                style={{
                  fontSize: "11px",
                  fontFamily: "var(--font-mono)",
                  color: "var(--color-text-tertiary)",
                  marginBottom: "10px",
                  textTransform: "uppercase",
                  letterSpacing: "0.06em",
                  display: "flex",
                  alignItems: "center",
                  gap: "8px",
                }}
              >
                <span
                  style={{
                    width: "8px",
                    height: "8px",
                    background: sevColor,
                    display: "inline-block",
                    flexShrink: 0,
                  }}
                />
                {sA?.acronym || g.system_a_id} / {sB?.acronym || g.system_b_id}
                <span style={{ marginLeft: "4px", opacity: 0.6 }}>
                  {g.severity}
                </span>
              </div>

              {/* Impact statement -- big, personal, hard-hitting */}
              <p
                style={{
                  fontFamily: "var(--font-serif)",
                  fontSize: "20px",
                  lineHeight: 1.45,
                  color: "#000000",
                  margin: 0,
                  fontWeight: 400,
                }}
              >
                {g.impact}
              </p>

              {/* Consent pathway hint */}
              {g.consent_closable && (
                <div
                  style={{
                    marginTop: "12px",
                    fontSize: "13px",
                    fontFamily: "var(--font-sans)",
                    color: "#006600",
                    fontWeight: 600,
                    letterSpacing: "0.02em",
                  }}
                >
                  You can authorize this data to be shared.
                </div>
              )}
            </button>
          );
        })}
      </div>
    </div>
  );
}
