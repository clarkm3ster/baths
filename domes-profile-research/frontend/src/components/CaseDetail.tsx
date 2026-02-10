import type { DocumentedCase } from "../types";
import { DOMAIN_COLORS, DOMAIN_LABELS } from "../types";

interface Props {
  caseData: DocumentedCase;
  onClose: () => void;
}

export default function CaseDetail({ caseData, onClose }: Props) {
  const domainColor = DOMAIN_COLORS[caseData.domain] || "#333";

  return (
    <>
      <div className="detail-overlay" onClick={onClose} />
      <div className="detail-panel">
        <div style={{ padding: "28px 32px" }}>
          {/* Close button */}
          <button
            onClick={onClose}
            style={{
              float: "right",
              background: "none",
              border: "1px solid #000000",
              padding: "5px 14px",
              cursor: "pointer",
              fontSize: "12px",
              fontFamily: "var(--font-mono)",
              fontWeight: 500,
              letterSpacing: "0.04em",
              textTransform: "uppercase",
            }}
          >
            Close
          </button>

          {/* Domain color bar */}
          <div
            style={{
              width: "100%",
              height: "3px",
              background: domainColor,
              marginBottom: "24px",
            }}
          />

          {/* Source info */}
          <div
            style={{
              fontFamily: "var(--font-mono)",
              fontSize: "12px",
              color: domainColor,
              marginBottom: "6px",
              display: "flex",
              alignItems: "center",
              gap: "8px",
            }}
          >
            <span>{caseData.source}</span>
            <span style={{ opacity: 0.5 }}>{caseData.year}</span>
            <span
              style={{
                fontSize: "10px",
                padding: "1px 6px",
                border: `1px solid ${domainColor}`,
                textTransform: "uppercase",
              }}
            >
              {DOMAIN_LABELS[caseData.domain] || caseData.domain}
            </span>
          </div>

          {/* Title */}
          <h2
            style={{
              fontFamily: "var(--font-serif)",
              fontSize: "22px",
              fontWeight: 700,
              lineHeight: 1.25,
              margin: "0 0 6px",
            }}
          >
            {caseData.source_title}
          </h2>

          <div
            style={{
              fontFamily: "var(--font-mono)",
              fontSize: "11px",
              color: "var(--color-text-tertiary)",
              marginBottom: "24px",
            }}
          >
            {caseData.source_type.toUpperCase()}
            {caseData.source_date ? ` \u00B7 ${caseData.source_date}` : ""}
            {caseData.location ? ` \u00B7 ${caseData.location}` : ""}
          </div>

          {/* Summary */}
          <SectionBlock title="Summary">
            <p
              style={{
                fontSize: "14px",
                lineHeight: 1.65,
                color: "var(--color-text-secondary)",
                margin: 0,
              }}
            >
              {caseData.summary}
            </p>
          </SectionBlock>

          {/* Key finding */}
          <div
            style={{
              padding: "20px",
              borderLeft: `3px solid ${domainColor}`,
              background: "var(--color-surface)",
              marginBottom: "24px",
            }}
          >
            <div className="section-label">Key finding</div>
            <p
              style={{
                fontFamily: "var(--font-serif)",
                fontSize: "16px",
                lineHeight: 1.55,
                margin: "6px 0 0",
              }}
            >
              {caseData.finding}
            </p>
          </div>

          {/* Cost data */}
          {caseData.cost_data && Object.keys(caseData.cost_data).length > 0 && (
            <SectionBlock title="Extracted cost data">
              <div style={{ display: "flex", flexDirection: "column", gap: "8px" }}>
                {Object.entries(caseData.cost_data).map(([key, val]) => (
                  <div
                    key={key}
                    style={{
                      display: "flex",
                      justifyContent: "space-between",
                      fontSize: "13px",
                      fontFamily: "var(--font-mono)",
                      padding: "6px 0",
                      borderBottom: "1px solid var(--color-border-light)",
                    }}
                  >
                    <span style={{ color: "var(--color-text-secondary)" }}>
                      {key.replace(/_/g, " ")}
                    </span>
                    <span style={{ fontWeight: 600 }}>
                      {typeof val === "number" && val > 100
                        ? `$${val.toLocaleString()}`
                        : typeof val === "number" && val < 1
                          ? `${(val * 100).toFixed(0)}%`
                          : String(val)}
                    </span>
                  </div>
                ))}
              </div>
            </SectionBlock>
          )}

          {/* Systems involved */}
          {caseData.system_ids.length > 0 && (
            <SectionBlock title="Systems involved">
              <div style={{ display: "flex", flexWrap: "wrap", gap: "4px" }}>
                {caseData.system_ids.map((sid) => (
                  <span
                    key={sid}
                    style={{
                      fontFamily: "var(--font-mono)",
                      fontSize: "11px",
                      padding: "3px 8px",
                      border: "1px solid var(--color-border)",
                      background: "var(--color-surface)",
                    }}
                  >
                    {sid}
                  </span>
                ))}
              </div>
            </SectionBlock>
          )}

          {/* Link */}
          {caseData.source_url && (
            <div style={{ marginTop: "24px" }}>
              <a
                href={caseData.source_url}
                target="_blank"
                rel="noopener noreferrer"
                style={{
                  fontFamily: "var(--font-mono)",
                  fontSize: "12px",
                  color: "#000000",
                  textDecoration: "underline",
                  textUnderlineOffset: "3px",
                }}
              >
                View original source \u2197
              </a>
            </div>
          )}
        </div>
      </div>
    </>
  );
}

function SectionBlock({
  title,
  children,
}: {
  title: string;
  children: React.ReactNode;
}) {
  return (
    <div style={{ marginBottom: "24px" }}>
      <div className="section-label">{title}</div>
      {children}
    </div>
  );
}
