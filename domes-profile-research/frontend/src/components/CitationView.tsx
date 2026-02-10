import type { CompositeProfile, DocumentedCase } from "../types";
import { DOMAIN_COLORS, DOMAIN_LABELS } from "../types";

interface Props {
  profile: CompositeProfile;
  onCaseClick: (c: DocumentedCase) => void;
}

const SOURCE_TYPE_LABELS: Record<string, string> = {
  investigation: "Investigation",
  gov_report: "Government Report",
  academic: "Academic Research",
  news: "News",
};

export default function CitationView({ profile, onCaseClick }: Props) {
  const { matched_cases } = profile;

  // Group by source type
  const byType: Record<string, DocumentedCase[]> = {};
  for (const c of matched_cases) {
    const t = c.source_type;
    if (!byType[t]) byType[t] = [];
    byType[t].push(c);
  }

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
        Every detail is sourced
      </h3>
      <p
        style={{
          fontFamily: "var(--font-serif)",
          fontStyle: "italic",
          fontSize: "15px",
          color: "var(--color-text-secondary)",
          marginBottom: "12px",
          lineHeight: 1.5,
        }}
      >
        {profile.name} is a composite. But every system failure, every cost
        figure, every barrier is drawn from real published investigations,
        government audits, and academic research.
      </p>

      {/* Count bar */}
      <div
        style={{
          display: "flex",
          gap: "24px",
          padding: "16px 0",
          borderTop: "2px solid #000000",
          borderBottom: "1px solid var(--color-border)",
          marginBottom: "32px",
          flexWrap: "wrap",
        }}
      >
        {Object.entries(byType).map(([type, cases]) => (
          <div key={type}>
            <span
              style={{
                fontFamily: "var(--font-mono)",
                fontSize: "20px",
                fontWeight: 600,
                marginRight: "8px",
              }}
            >
              {cases.length}
            </span>
            <span
              style={{
                fontSize: "13px",
                color: "var(--color-text-secondary)",
              }}
            >
              {SOURCE_TYPE_LABELS[type] || type}
              {cases.length !== 1 ? "s" : ""}
            </span>
          </div>
        ))}
      </div>

      {/* Cases list */}
      {Object.entries(byType).map(([type, cases]) => (
        <div key={type} style={{ marginBottom: "36px" }}>
          <div className="section-label" style={{ marginBottom: "14px" }}>
            {SOURCE_TYPE_LABELS[type] || type}
          </div>

          <div style={{ display: "flex", flexDirection: "column", gap: "0" }}>
            {cases.map((c, i) => {
              const domainColor = DOMAIN_COLORS[c.domain] || "#333";
              return (
                <button
                  key={c.id}
                  onClick={() => onCaseClick(c)}
                  style={{
                    display: "block",
                    width: "100%",
                    textAlign: "left",
                    background: "#FFFFFF",
                    border: "none",
                    borderTop:
                      i === 0
                        ? "1px solid var(--color-border)"
                        : "1px solid var(--color-border-light)",
                    padding: "20px 0",
                    cursor: "pointer",
                    fontFamily: "var(--font-sans)",
                  }}
                >
                  {/* Source + domain */}
                  <div
                    style={{
                      display: "flex",
                      alignItems: "center",
                      gap: "8px",
                      marginBottom: "6px",
                    }}
                  >
                    <span
                      style={{
                        width: "8px",
                        height: "8px",
                        background: domainColor,
                        flexShrink: 0,
                      }}
                    />
                    <span
                      style={{
                        fontFamily: "var(--font-mono)",
                        fontSize: "12px",
                        fontWeight: 500,
                        color: "var(--color-text-tertiary)",
                      }}
                    >
                      {c.source}
                      {c.year ? ` (${c.year})` : ""}
                    </span>
                    <span
                      style={{
                        fontFamily: "var(--font-mono)",
                        fontSize: "10px",
                        padding: "1px 6px",
                        border: `1px solid ${domainColor}`,
                        color: domainColor,
                        textTransform: "uppercase",
                      }}
                    >
                      {DOMAIN_LABELS[c.domain] || c.domain}
                    </span>
                  </div>

                  {/* Title */}
                  <div
                    style={{
                      fontSize: "15px",
                      fontWeight: 600,
                      color: "#000000",
                      lineHeight: 1.35,
                      marginBottom: "6px",
                    }}
                  >
                    {c.source_title}
                  </div>

                  {/* Finding excerpt */}
                  <p
                    style={{
                      fontSize: "13px",
                      lineHeight: 1.5,
                      color: "var(--color-text-secondary)",
                      margin: 0,
                    }}
                  >
                    {c.finding.length > 200
                      ? c.finding.slice(0, 200) + "..."
                      : c.finding}
                  </p>
                </button>
              );
            })}
          </div>
        </div>
      ))}
    </div>
  );
}
