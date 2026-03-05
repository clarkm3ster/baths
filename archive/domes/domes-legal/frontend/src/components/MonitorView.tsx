import { useState, useEffect } from "react";
import type { TaxonomyStats, GraphStats } from "../types";
import { DOMAIN_COLORS, DOMAIN_LABELS } from "../types";
import { getTaxonomyStats, getGraphStats } from "../api/client";
import type { RecentChangesResponse } from "../api/client";
import { getRecentChanges } from "../api/client";

const SOURCE_LABELS: Record<string, string> = {
  usc: "US Code",
  cfr: "CFR",
  fr: "Fed Register",
  pa_statute: "PA Statute",
  pa_reg: "PA Reg",
  case_law: "Case Law",
};

const CHANGE_TYPE_COLORS: Record<string, string> = {
  amended: "#EAB308",
  new: "#22C55E",
  guidance: "#3388FF",
  repealed: "#EF4444",
};

export default function MonitorView() {
  const [stats, setStats] = useState<TaxonomyStats | null>(null);
  const [graphStats, setGraphStats] = useState<GraphStats | null>(null);
  const [changes, setChanges] = useState<RecentChangesResponse | null>(null);

  useEffect(() => {
    getTaxonomyStats().then(setStats);
    getGraphStats().then(setGraphStats);
    getRecentChanges().then(setChanges).catch(() => {});
  }, []);

  if (!stats) return <div style={{ padding: "32px", fontFamily: "var(--font-mono)", fontSize: "12px", color: "var(--color-text-tertiary)" }}>LOADING...</div>;

  const maxDomainCount = Math.max(...Object.values(stats.domains), 1);

  return (
    <div style={{ padding: "28px 32px" }}>
      {/* Header stats */}
      <div style={{ display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: "16px", marginBottom: "32px" }}>
        <StatCard label="Provisions" value={stats.total_provisions} />
        <StatCard label="Relationships" value={graphStats?.edges || 0} />
        <StatCard label="Tags" value={stats.total_tags} />
        <StatCard label="Sources" value={Object.keys(stats.source_types).length} />
      </div>

      {/* Recent Changes Feed */}
      {changes && (
        <div style={{ marginBottom: "32px" }}>
          <div className="section-label">Recent Changes</div>
          <div style={{
            padding: "12px 16px", marginBottom: "12px",
            background: "var(--color-surface)", border: "1px solid var(--color-border)",
            fontFamily: "var(--font-mono)", fontSize: "12px", color: "var(--color-text)",
          }}>
            <span className="status-indicator status-indicator--pending" style={{ marginRight: "8px" }} />
            {changes.week_summary}
          </div>

          <div style={{ display: "flex", flexDirection: "column", gap: "6px" }}>
            {changes.changes.map((c, i) => (
              <div key={i} style={{
                padding: "14px 16px",
                border: "1px solid var(--color-border)",
                background: "var(--color-surface-alt)",
              }}>
                <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: "6px" }}>
                  <div style={{ display: "flex", gap: "8px", alignItems: "center" }}>
                    <span style={{
                      fontFamily: "var(--font-mono)", fontSize: "9px", textTransform: "uppercase",
                      padding: "2px 6px", border: "1px solid",
                      borderColor: CHANGE_TYPE_COLORS[c.change_type] || "#666",
                      color: CHANGE_TYPE_COLORS[c.change_type] || "#666",
                    }}>
                      {c.change_type}
                    </span>
                    <span style={{
                      fontFamily: "var(--font-mono)", fontSize: "9px", textTransform: "uppercase",
                      padding: "2px 6px", border: "1px solid var(--color-border)", color: "var(--color-text-tertiary)",
                    }}>
                      {SOURCE_LABELS[c.source] || c.source}
                    </span>
                  </div>
                  <span style={{ fontFamily: "var(--font-mono)", fontSize: "10px", color: "var(--color-text-tertiary)" }}>
                    {c.date}
                  </span>
                </div>
                <div style={{ fontFamily: "var(--font-mono)", fontSize: "12px", fontWeight: 500, color: "var(--color-text)", marginBottom: "4px" }}>
                  {c.citation}
                </div>
                <div style={{ fontFamily: "var(--font-serif)", fontSize: "13px", fontWeight: 600, marginBottom: "4px" }}>
                  {c.title}
                </div>
                <div style={{ fontSize: "12px", color: "var(--color-text-secondary)", lineHeight: 1.5, marginBottom: "6px" }}>
                  {c.summary}
                </div>
                <div style={{ display: "flex", gap: "6px", alignItems: "center" }}>
                  {c.affected_domains.map((d) => (
                    <span key={d} style={{
                      fontFamily: "var(--font-mono)", fontSize: "9px", textTransform: "uppercase",
                      padding: "1px 6px", background: (DOMAIN_COLORS[d] || "#333") + "25",
                      color: DOMAIN_COLORS[d] || "#999",
                    }}>
                      {DOMAIN_LABELS[d] || d}
                    </span>
                  ))}
                  <span style={{ fontFamily: "var(--font-mono)", fontSize: "10px", color: "var(--color-text-tertiary)" }}>
                    {c.affected_provisions} provisions affected
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Source Status */}
      {changes && (
        <div style={{ marginBottom: "32px" }}>
          <div className="section-label">Source Status</div>
          <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: "8px" }}>
            {Object.entries(changes.source_status).map(([source, status]) => (
              <div key={source} style={{
                padding: "12px", border: "1px solid var(--color-border)", background: "var(--color-surface-alt)",
              }}>
                <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "4px" }}>
                  <span style={{ fontFamily: "var(--font-mono)", fontSize: "11px", textTransform: "uppercase", fontWeight: 500 }}>
                    {SOURCE_LABELS[source] || source}
                  </span>
                  <span className={`status-indicator ${status.status === "current" ? "status-indicator--active" : "status-indicator--pending"}`} />
                </div>
                <div style={{ fontFamily: "var(--font-mono)", fontSize: "9px", color: "var(--color-text-tertiary)" }}>
                  {status.status === "current" ? "UP TO DATE" : "CHANGES DETECTED"}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Domain breakdown */}
      <div style={{ marginBottom: "32px" }}>
        <div className="section-label">Provisions by Domain</div>
        <div style={{ display: "flex", flexDirection: "column", gap: "10px" }}>
          {Object.entries(stats.domains)
            .sort(([, a], [, b]) => b - a)
            .map(([domain, count]) => {
              const color = DOMAIN_COLORS[domain] || "#333";
              const pct = (count / maxDomainCount) * 100;
              return (
                <div key={domain}>
                  <div style={{ display: "flex", justifyContent: "space-between", marginBottom: "3px" }}>
                    <span style={{ fontFamily: "var(--font-mono)", fontSize: "11px", textTransform: "uppercase", color, fontWeight: 600 }}>
                      {DOMAIN_LABELS[domain] || domain}
                    </span>
                    <span style={{ fontFamily: "var(--font-mono)", fontSize: "13px", fontWeight: 500, color: "#FFF" }}>
                      {count}
                    </span>
                  </div>
                  <div style={{ height: "20px", background: "var(--color-surface-alt)", position: "relative" }}>
                    <div style={{ position: "absolute", left: 0, top: 0, bottom: 0, width: `${pct}%`, background: color, opacity: 0.4, transition: "width 0.6s" }} />
                  </div>
                </div>
              );
            })}
        </div>
      </div>

      {/* Provision types */}
      <div style={{ marginBottom: "32px" }}>
        <div className="section-label">By Type</div>
        <div style={{ display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: "12px" }}>
          {Object.entries(stats.provision_types).map(([type, count]) => (
            <div key={type} style={{ padding: "16px", border: "1px solid var(--color-border)", textAlign: "center", background: "var(--color-surface-alt)" }}>
              <div className="stat-readout" style={{ fontSize: "24px" }}>{count}</div>
              <div style={{ fontFamily: "var(--font-mono)", fontSize: "10px", textTransform: "uppercase", color: "var(--color-text-tertiary)", marginTop: "4px" }}>
                {type}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Source types */}
      <div style={{ marginBottom: "32px" }}>
        <div className="section-label">By Source</div>
        <div style={{ display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: "12px" }}>
          {Object.entries(stats.source_types).map(([type, count]) => (
            <div key={type} style={{ padding: "16px", border: "1px solid var(--color-border)", textAlign: "center", background: "var(--color-surface-alt)" }}>
              <div className="stat-readout" style={{ fontSize: "24px" }}>{count}</div>
              <div style={{ fontFamily: "var(--font-mono)", fontSize: "10px", textTransform: "uppercase", color: "var(--color-text-tertiary)", marginTop: "4px" }}>
                {type}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Graph stats */}
      {graphStats && (
        <div>
          <div className="section-label">Relationship Graph</div>
          <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(120px, 1fr))", gap: "12px" }}>
            {Object.entries(graphStats.relationship_types).map(([type, count]) => (
              <div key={type} style={{ padding: "12px", border: "1px solid var(--color-border)", background: "var(--color-surface-alt)" }}>
                <div style={{ fontFamily: "var(--font-mono)", fontSize: "20px", fontWeight: 500, color: "#FFF" }}>{count}</div>
                <div style={{ fontFamily: "var(--font-mono)", fontSize: "10px", textTransform: "uppercase", color: "var(--color-text-tertiary)" }}>
                  {type}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

function StatCard({ label, value }: { label: string; value: number }) {
  return (
    <div style={{ padding: "20px", border: "1px solid var(--color-border)", background: "var(--color-surface)" }}>
      <div className="stat-readout">{value}</div>
      <div style={{ fontFamily: "var(--font-mono)", fontSize: "10px", textTransform: "uppercase", letterSpacing: "0.06em", color: "var(--color-text-tertiary)", marginTop: "6px" }}>
        {label}
      </div>
    </div>
  );
}
