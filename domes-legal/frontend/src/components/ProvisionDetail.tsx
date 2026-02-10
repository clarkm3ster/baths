import type { Provision } from "../types";
import DomainBadge from "./DomainBadge";

interface Props {
  provision: Provision;
  onClose: () => void;
}

export default function ProvisionDetail({ provision, onClose }: Props) {
  const enforcement = provision.enforcement_mechanisms || [];
  const crossRefs = provision.cross_references || [];
  const tags = provision.tags || [];

  return (
    <>
      <div className="detail-overlay" onClick={onClose} />
      <div className="detail-panel">
        <div style={{ padding: "24px 28px" }}>
          {/* Close button */}
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: "20px" }}>
            <div>
              <div style={{ fontFamily: "var(--font-mono)", fontSize: "13px", fontWeight: 500, marginBottom: "6px", color: "var(--color-text-secondary)" }}>
                {provision.citation}
              </div>
              <DomainBadge domain={provision.domain} />
              <span style={{ fontFamily: "var(--font-mono)", fontSize: "10px", marginLeft: "8px", padding: "2px 6px", border: "1px solid var(--color-border)", textTransform: "uppercase" }}>
                {provision.provision_type}
              </span>
            </div>
            <button onClick={onClose} style={{ background: "none", border: "1px solid var(--color-border)", padding: "4px 12px", cursor: "pointer", fontFamily: "var(--font-mono)", fontSize: "11px", color: "var(--color-text-secondary)" }}>
              CLOSE
            </button>
          </div>

          {/* Title */}
          <h2 style={{ fontFamily: "var(--font-serif)", fontSize: "22px", fontWeight: 700, lineHeight: 1.3, marginBottom: "20px" }}>
            {provision.title}
          </h2>

          {/* Full text */}
          <div style={{ marginBottom: "24px" }}>
            <div className="section-label">Full Text</div>
            <p style={{ fontFamily: "var(--font-serif)", fontSize: "15px", lineHeight: 1.7, color: "var(--color-text-secondary)" }}>
              {provision.full_text}
            </p>
          </div>

          {/* Source metadata */}
          <div style={{ marginBottom: "24px", padding: "16px", background: "var(--color-surface)", border: "1px solid var(--color-border-light)" }}>
            <div className="section-label">Source</div>
            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "8px", fontFamily: "var(--font-mono)", fontSize: "11px" }}>
              <div><span style={{ color: "var(--color-text-tertiary)" }}>Type:</span> {provision.source_type}</div>
              <div><span style={{ color: "var(--color-text-tertiary)" }}>Title:</span> {provision.title_number || "—"}</div>
              <div><span style={{ color: "var(--color-text-tertiary)" }}>Part:</span> {provision.part || "—"}</div>
              <div><span style={{ color: "var(--color-text-tertiary)" }}>Section:</span> {provision.section || "—"}</div>
            </div>
            {provision.source_url && (
              <div style={{ marginTop: "8px" }}>
                <a href={provision.source_url} target="_blank" rel="noopener noreferrer" style={{ fontFamily: "var(--font-mono)", fontSize: "11px", color: "var(--color-accent)" }}>
                  View original source
                </a>
              </div>
            )}
          </div>

          {/* Tags */}
          {tags.length > 0 && (
            <div style={{ marginBottom: "24px" }}>
              <div className="section-label">Tags</div>
              <div style={{ display: "flex", flexWrap: "wrap", gap: "4px" }}>
                {tags.map((t) => (
                  <span key={t} className="citation-tag">{t}</span>
                ))}
              </div>
            </div>
          )}

          {/* Enforcement */}
          {enforcement.length > 0 && (
            <div style={{ marginBottom: "24px" }}>
              <div className="section-label">Enforcement Mechanisms</div>
              <div style={{ display: "flex", flexDirection: "column", gap: "6px" }}>
                {enforcement.map((e, i) => (
                  <div key={i} style={{ fontFamily: "var(--font-mono)", fontSize: "12px", padding: "8px 12px", background: "var(--color-surface)", borderLeft: "3px solid var(--color-justice)" }}>
                    {e}
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Cross references */}
          {crossRefs.length > 0 && (
            <div style={{ marginBottom: "24px" }}>
              <div className="section-label">Cross References</div>
              <div style={{ display: "flex", flexWrap: "wrap", gap: "6px" }}>
                {crossRefs.map((r) => (
                  <span key={r} className="citation-tag" style={{ cursor: "pointer", borderColor: "var(--color-accent)" }}>
                    {r}
                  </span>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </>
  );
}
