import type { System, Connection, Gap, Domain } from "../types";
import { DOMAIN_COLORS, DOMAIN_LABELS } from "../types";

type Detail =
  | { type: "system"; system: System }
  | { type: "gap"; gap: Gap; systemA?: System; systemB?: System }
  | {
      type: "connection";
      connection: Connection;
      source?: System;
      target?: System;
    };

interface Props {
  detail: Detail;
  onClose: () => void;
}

export default function DetailPanel({ detail, onClose }: Props) {
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

          {detail.type === "system" && <SystemPanel system={detail.system} />}
          {detail.type === "gap" && (
            <GapPanel
              gap={detail.gap}
              systemA={detail.systemA}
              systemB={detail.systemB}
            />
          )}
          {detail.type === "connection" && (
            <ConnectionPanel
              connection={detail.connection}
              source={detail.source}
              target={detail.target}
            />
          )}
        </div>
      </div>
    </>
  );
}

/* ─────────────────────────────────
   System Panel
   ───────────────────────────────── */

function SystemPanel({ system }: { system: System }) {
  const domain = system.domain as Domain;
  const color = DOMAIN_COLORS[domain] || "#333333";

  return (
    <div>
      {/* Domain color bar */}
      <div
        style={{
          width: "100%",
          height: "3px",
          background: color,
          marginBottom: "24px",
        }}
      />

      <h2
        style={{
          fontFamily: "var(--font-serif)",
          fontSize: "24px",
          fontWeight: 700,
          margin: "0 0 4px",
          lineHeight: 1.2,
        }}
      >
        {system.name}
      </h2>
      <div
        style={{
          fontFamily: "var(--font-mono)",
          fontSize: "13px",
          color,
          marginBottom: "20px",
        }}
      >
        {system.acronym}
        {" \u00B7 "}
        {DOMAIN_LABELS[domain]}
      </div>

      <p
        style={{
          fontSize: "14px",
          lineHeight: 1.65,
          color: "var(--color-text-secondary)",
          marginBottom: "28px",
        }}
      >
        {system.description}
      </p>

      <Section title="What they know about you">
        <Tags items={system.data_held} />
      </Section>

      <Section title="Who can see it">
        <Tags items={system.who_can_access} />
      </Section>

      <Section title="Governed by">
        <span
          style={{
            fontFamily: "var(--font-mono)",
            fontSize: "14px",
            fontWeight: 500,
          }}
        >
          {system.privacy_law}
        </span>
        {system.privacy_laws.length > 1 && (
          <div
            style={{
              fontSize: "12px",
              color: "var(--color-text-tertiary)",
              marginTop: "4px",
              fontFamily: "var(--font-mono)",
            }}
          >
            Also:{" "}
            {system.privacy_laws
              .filter((l) => l !== system.privacy_law)
              .join(", ")}
          </div>
        )}
      </Section>

      <Section title="Technical details">
        <div
          style={{
            display: "flex",
            flexWrap: "wrap",
            gap: "8px",
          }}
        >
          <Tag>{system.data_standard}</Tag>
          <Tag>{system.is_federal ? "Federal" : "State/Local"}</Tag>
          <Tag>{system.state_operated ? "Gov operated" : "Contracted"}</Tag>
        </div>
      </Section>

      <Section title="Run by">
        <p style={{ fontSize: "14px", margin: 0 }}>{system.agency}</p>
      </Section>
    </div>
  );
}

/* ─────────────────────────────────
   Gap Panel
   ───────────────────────────────── */

const SEVERITY_STYLE: Record<string, { color: string; label: string }> = {
  critical: { color: "#CC0000", label: "CRITICAL" },
  high: { color: "#994400", label: "HIGH" },
  moderate: { color: "#666600", label: "MODERATE" },
  low: { color: "#446644", label: "LOW" },
};

const BARRIER_LABELS: Record<string, string> = {
  legal: "Legal barrier",
  technical: "Technical barrier",
  political: "Political / governance barrier",
  funding: "Funding barrier",
  consent: "Consent barrier",
};

function GapPanel({
  gap,
  systemA,
  systemB,
}: {
  gap: Gap;
  systemA?: System;
  systemB?: System;
}) {
  const sev = SEVERITY_STYLE[gap.severity] || SEVERITY_STYLE.moderate;

  return (
    <div>
      {/* Severity color bar */}
      <div
        style={{
          width: "100%",
          height: "3px",
          background: sev.color,
          marginBottom: "24px",
        }}
      />

      <h2
        style={{
          fontFamily: "var(--font-serif)",
          fontSize: "22px",
          fontWeight: 700,
          margin: "0 0 4px",
          lineHeight: 1.25,
        }}
      >
        {systemA?.name || gap.system_a_id}
      </h2>
      <div
        style={{
          fontSize: "14px",
          color: "var(--color-text-tertiary)",
          marginBottom: "4px",
          fontFamily: "var(--font-serif)",
          fontStyle: "italic",
        }}
      >
        does not talk to
      </div>
      <h2
        style={{
          fontFamily: "var(--font-serif)",
          fontSize: "22px",
          fontWeight: 700,
          margin: "0 0 16px",
          lineHeight: 1.25,
        }}
      >
        {systemB?.name || gap.system_b_id}
      </h2>

      <div style={{ display: "flex", gap: "8px", marginBottom: "28px" }}>
        <Tag color={sev.color}>{sev.label}</Tag>
        <Tag>{BARRIER_LABELS[gap.barrier_type] || gap.barrier_type}</Tag>
      </div>

      {gap.barrier_law && (
        <Section title="Governing law">
          <span
            style={{
              fontFamily: "var(--font-mono)",
              fontSize: "14px",
              fontWeight: 500,
            }}
          >
            {gap.barrier_law}
          </span>
        </Section>
      )}

      <Section title="Why they don't talk">
        <p
          style={{
            fontSize: "14px",
            lineHeight: 1.65,
            color: "var(--color-text-secondary)",
            margin: 0,
          }}
        >
          {gap.barrier_description}
        </p>
      </Section>

      {/* Impact callout */}
      <div
        style={{
          padding: "20px",
          borderLeft: `3px solid ${sev.color}`,
          background: "var(--color-surface)",
          marginBottom: "24px",
        }}
      >
        <SectionLabel>What this means for you</SectionLabel>
        <p
          style={{
            fontFamily: "var(--font-serif)",
            fontSize: "17px",
            lineHeight: 1.5,
            margin: "6px 0 0",
            color: "#000000",
          }}
        >
          {gap.impact}
        </p>
      </div>

      <Section title="What it would take to fix">
        <p
          style={{
            fontSize: "14px",
            lineHeight: 1.65,
            color: "var(--color-text-secondary)",
            margin: 0,
          }}
        >
          {gap.what_it_would_take}
        </p>
      </Section>

      {/* Consent closable callout */}
      {gap.consent_closable && (
        <div
          style={{
            padding: "20px",
            border: "2px solid #006600",
            background: "#FFFFFF",
          }}
        >
          <div
            style={{
              fontFamily: "var(--font-serif)",
              fontSize: "19px",
              fontWeight: 700,
              color: "#006600",
              marginBottom: "10px",
            }}
          >
            You can close this gap
          </div>
          <p
            style={{
              fontSize: "14px",
              lineHeight: 1.65,
              margin: 0,
              color: "var(--color-text-secondary)",
            }}
          >
            {gap.consent_mechanism}
          </p>
        </div>
      )}
    </div>
  );
}

/* ─────────────────────────────────
   Connection Panel
   ───────────────────────────────── */

function ConnectionPanel({
  connection,
  source,
  target,
}: {
  connection: Connection;
  source?: System;
  target?: System;
}) {
  const relColor =
    connection.reliability === "high"
      ? "#1A6B3C"
      : connection.reliability === "low"
        ? "#8B1A1A"
        : "#6B5A1A";

  return (
    <div>
      {/* Connection color bar */}
      <div
        style={{
          width: "100%",
          height: "3px",
          background: "#333333",
          marginBottom: "24px",
        }}
      />

      <h2
        style={{
          fontFamily: "var(--font-serif)",
          fontSize: "22px",
          fontWeight: 700,
          margin: "0 0 4px",
          lineHeight: 1.25,
        }}
      >
        {source?.name || connection.source_id}
      </h2>
      <div
        style={{
          fontSize: "14px",
          color: "var(--color-text-tertiary)",
          marginBottom: "4px",
          fontFamily: "var(--font-serif)",
          fontStyle: "italic",
        }}
      >
        {connection.direction === "bidirectional"
          ? "shares data with"
          : "sends data to"}
      </div>
      <h2
        style={{
          fontFamily: "var(--font-serif)",
          fontSize: "22px",
          fontWeight: 700,
          margin: "0 0 16px",
          lineHeight: 1.25,
        }}
      >
        {target?.name || connection.target_id}
      </h2>

      <div style={{ display: "flex", gap: "8px", marginBottom: "28px" }}>
        <Tag color={relColor}>{connection.reliability} reliability</Tag>
        <Tag>{connection.frequency}</Tag>
        <Tag>{connection.format}</Tag>
      </div>

      <Section title="How it works">
        <p
          style={{
            fontSize: "14px",
            lineHeight: 1.65,
            color: "var(--color-text-secondary)",
            margin: 0,
          }}
        >
          {connection.description}
        </p>
      </Section>

      <Section title="Data that flows">
        <Tags items={connection.data_shared} />
      </Section>
    </div>
  );
}

/* ─────────────────────────────────
   Shared helpers
   ───────────────────────────────── */

function Section({
  title,
  children,
}: {
  title: string;
  children: React.ReactNode;
}) {
  return (
    <div style={{ marginBottom: "24px" }}>
      <SectionLabel>{title}</SectionLabel>
      {children}
    </div>
  );
}

function SectionLabel({ children }: { children: React.ReactNode }) {
  return (
    <div
      style={{
        fontSize: "11px",
        fontFamily: "var(--font-mono)",
        fontWeight: 500,
        textTransform: "uppercase",
        letterSpacing: "0.08em",
        color: "var(--color-text-tertiary)",
        marginBottom: "8px",
      }}
    >
      {children}
    </div>
  );
}

function Tags({ items }: { items: string[] }) {
  return (
    <div style={{ display: "flex", flexWrap: "wrap", gap: "4px" }}>
      {items.map((item) => (
        <span
          key={item}
          style={{
            fontFamily: "var(--font-mono)",
            fontSize: "12px",
            padding: "4px 10px",
            border: "1px solid var(--color-border)",
            background: "var(--color-surface)",
          }}
        >
          {item.replace(/_/g, " ")}
        </span>
      ))}
    </div>
  );
}

function Tag({
  children,
  color,
}: {
  children: React.ReactNode;
  color?: string;
}) {
  return (
    <span
      style={{
        fontSize: "11px",
        fontFamily: "var(--font-mono)",
        fontWeight: 500,
        padding: "3px 10px",
        border: `1px solid ${color || "var(--color-border)"}`,
        color: color || "var(--color-text-secondary)",
        letterSpacing: "0.02em",
      }}
    >
      {children}
    </span>
  );
}
