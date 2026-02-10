import { useState, useCallback } from "react";
import type {
  Profile,
  System,
  Connection,
  Gap,
  ConstellationResponse,
} from "./types";
import { getConstellation } from "./api/client";
import CircumstancesForm from "./components/CircumstancesForm";
import ConstellationView from "./components/ConstellationView";
import Summary from "./components/Summary";
import ImpactView from "./components/ImpactView";
import ConsentPathways from "./components/ConsentPathways";
import DetailPanel from "./components/DetailPanel";

type DetailView =
  | { type: "system"; system: System }
  | { type: "gap"; gap: Gap; systemA?: System; systemB?: System }
  | {
      type: "connection";
      connection: Connection;
      source?: System;
      target?: System;
    };

type Section = "constellation" | "impact" | "consent";

export default function App() {
  const [constellation, setConstellation] =
    useState<ConstellationResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [detail, setDetail] = useState<DetailView | null>(null);
  const [showForm, setShowForm] = useState(true);
  const [section, setSection] = useState<Section>("constellation");

  const handleSubmit = useCallback(async (profile: Profile) => {
    setLoading(true);
    setError(null);
    setDetail(null);
    try {
      const data = await getConstellation(profile);
      setConstellation(data);
      setShowForm(false);
      setSection("constellation");
    } catch (e) {
      setError(
        e instanceof Error ? e.message : "Failed to load constellation"
      );
    } finally {
      setLoading(false);
    }
  }, []);

  const systemMap = new Map<string, System>();
  if (constellation) {
    for (const s of constellation.systems) {
      systemMap.set(s.id, s);
    }
  }

  const openGap = (g: Gap) =>
    setDetail({
      type: "gap",
      gap: g,
      systemA: systemMap.get(g.system_a_id),
      systemB: systemMap.get(g.system_b_id),
    });

  /* ─── Circumstances page ─── */
  if (showForm) {
    return (
      <div
        style={{
          minHeight: "100%",
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "center",
          padding: "48px 24px",
          background: "#FFFFFF",
        }}
      >
        <div style={{ maxWidth: "640px", width: "100%" }}>
          {/* Title block */}
          <div style={{ marginBottom: "36px" }}>
            <h1
              style={{
                fontFamily: "var(--font-serif)",
                fontSize: "36px",
                fontWeight: 700,
                marginBottom: "8px",
                letterSpacing: "-0.02em",
                lineHeight: 1.15,
              }}
            >
              Data Constellation
            </h1>
            <p
              style={{
                fontFamily: "var(--font-serif)",
                fontSize: "17px",
                fontStyle: "italic",
                color: "var(--color-text-secondary)",
                lineHeight: 1.55,
              }}
            >
              Every government database that has information about you -- and the
              disconnections between them. Check what applies to your life.
            </p>
          </div>

          {/* Back button if we already have a constellation */}
          {constellation && (
            <button
              onClick={() => setShowForm(false)}
              style={{
                background: "none",
                border: "1px solid var(--color-border)",
                cursor: "pointer",
                fontSize: "12px",
                fontFamily: "var(--font-mono)",
                color: "var(--color-text-secondary)",
                padding: "6px 14px",
                marginBottom: "20px",
                textTransform: "uppercase",
                letterSpacing: "0.04em",
                fontWeight: 500,
              }}
            >
              Back to constellation
            </button>
          )}

          {/* Error */}
          {error && (
            <div
              style={{
                color: "#CC0000",
                fontSize: "14px",
                fontFamily: "var(--font-mono)",
                marginBottom: "20px",
                padding: "12px",
                border: "1px solid #CC0000",
                background: "#FFFFFF",
              }}
            >
              {error}
            </div>
          )}

          <CircumstancesForm onSubmit={handleSubmit} loading={loading} />
        </div>
      </div>
    );
  }

  /* ─── Main constellation view ─── */
  if (!constellation) return null;

  const { summary } = constellation;

  return (
    <div
      style={{
        height: "100%",
        display: "flex",
        flexDirection: "column",
        overflow: "hidden",
        background: "#FFFFFF",
      }}
    >
      {/* Summary bar */}
      <Summary
        totalSystems={summary.total_systems}
        connected={summary.connected}
        siloed={summary.siloed}
        gapCount={summary.gaps}
        consentClosable={summary.consent_closable}
      />

      {/* Tab navigation */}
      <nav
        style={{
          display: "flex",
          gap: "0",
          borderBottom: "1px solid var(--color-border)",
          padding: "0 32px",
          background: "#FFFFFF",
          flexShrink: 0,
        }}
      >
        {(
          [
            ["constellation", "Constellation"],
            ["impact", "Impact"],
            ["consent", "Consent Pathways"],
          ] as [Section, string][]
        ).map(([key, label]) => (
          <button
            key={key}
            onClick={() => setSection(key)}
            style={{
              background: "none",
              border: "none",
              borderBottom:
                section === key
                  ? "2px solid #000000"
                  : "2px solid transparent",
              padding: "12px 20px",
              cursor: "pointer",
              fontSize: "13px",
              fontFamily: "var(--font-sans)",
              fontWeight: section === key ? 600 : 400,
              color:
                section === key
                  ? "#000000"
                  : "var(--color-text-tertiary)",
              letterSpacing: "0.02em",
              transition: "color 0.1s",
            }}
          >
            {label}
            {key === "consent" && summary.consent_closable > 0 && (
              <span
                style={{
                  marginLeft: "8px",
                  fontFamily: "var(--font-mono)",
                  fontSize: "11px",
                  color: "#006600",
                  fontWeight: 500,
                }}
              >
                {summary.consent_closable}
              </span>
            )}
          </button>
        ))}

        <div style={{ flex: 1 }} />

        <button
          onClick={() => setShowForm(true)}
          style={{
            background: "none",
            border: "1px solid var(--color-border)",
            cursor: "pointer",
            fontSize: "11px",
            fontFamily: "var(--font-mono)",
            color: "var(--color-text-tertiary)",
            padding: "4px 12px",
            alignSelf: "center",
            textTransform: "uppercase",
            letterSpacing: "0.04em",
            fontWeight: 500,
          }}
        >
          Change circumstances
        </button>
      </nav>

      {/* Content area -- fills remaining space */}
      <div
        style={{
          flex: "1 1 0%",
          minHeight: 0,
          overflow: section === "constellation" ? "hidden" : "auto",
          display: "flex",
          flexDirection: "column",
        }}
      >
        {section === "constellation" && (
          <>
            {/* Constellation gets full remaining flex space */}
            <ConstellationView
              systems={constellation.systems}
              connections={constellation.connections}
              gaps={constellation.gaps}
              onSystemClick={(s) => setDetail({ type: "system", system: s })}
              onGapClick={openGap}
              onConnectionClick={(c) =>
                setDetail({
                  type: "connection",
                  connection: c,
                  source: systemMap.get(c.source_id),
                  target: systemMap.get(c.target_id),
                })
              }
              selectedId={
                detail?.type === "system" ? detail.system.id : undefined
              }
            />

            {/* Gap list below constellation */}
            {constellation.gaps.length > 0 && (
              <div
                style={{
                  padding: "14px 32px",
                  borderTop: "1px solid var(--color-border)",
                  background: "#FFFFFF",
                  overflowY: "auto",
                  maxHeight: "200px",
                  flexShrink: 0,
                }}
              >
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
                  {constellation.gaps.length} gaps in your constellation
                </div>
                <div
                  style={{
                    display: "flex",
                    flexDirection: "column",
                    gap: "0",
                  }}
                >
                  {constellation.gaps.map((g) => {
                    const sA = systemMap.get(g.system_a_id);
                    const sB = systemMap.get(g.system_b_id);
                    const sevColor =
                      g.severity === "critical"
                        ? "#CC0000"
                        : g.severity === "high"
                          ? "#994400"
                          : "#666600";
                    return (
                      <button
                        key={g.id}
                        onClick={() => openGap(g)}
                        style={{
                          display: "flex",
                          alignItems: "center",
                          gap: "10px",
                          padding: "7px 0",
                          background: "none",
                          border: "none",
                          borderBottom: "1px solid var(--color-border-light)",
                          cursor: "pointer",
                          textAlign: "left",
                          width: "100%",
                          fontFamily: "var(--font-sans)",
                          fontSize: "13px",
                        }}
                      >
                        <span
                          style={{
                            width: "6px",
                            height: "6px",
                            background: sevColor,
                            flexShrink: 0,
                          }}
                        />
                        <span
                          style={{
                            fontFamily: "var(--font-mono)",
                            fontSize: "12px",
                            minWidth: "120px",
                          }}
                        >
                          {sA?.acronym || g.system_a_id}
                          {" \u2194 "}
                          {sB?.acronym || g.system_b_id}
                        </span>
                        <span
                          style={{
                            color: "var(--color-text-secondary)",
                            flex: 1,
                          }}
                        >
                          {g.barrier_type}
                          {g.barrier_law ? ` -- ${g.barrier_law}` : ""}
                        </span>
                        {g.consent_closable && (
                          <span
                            style={{
                              fontSize: "10px",
                              fontFamily: "var(--font-mono)",
                              color: "#006600",
                              border: "1px solid #006600",
                              padding: "1px 6px",
                              whiteSpace: "nowrap",
                              fontWeight: 500,
                            }}
                          >
                            CLOSABLE
                          </span>
                        )}
                      </button>
                    );
                  })}
                </div>
              </div>
            )}
          </>
        )}

        {section === "impact" && (
          <ImpactView
            gaps={constellation.gaps}
            systemMap={systemMap}
            onGapClick={openGap}
          />
        )}

        {section === "consent" && (
          <ConsentPathways
            gaps={constellation.gaps}
            systemMap={systemMap}
            onGapClick={openGap}
          />
        )}
      </div>

      {/* Slide-in detail panel */}
      {detail && (
        <DetailPanel detail={detail} onClose={() => setDetail(null)} />
      )}
    </div>
  );
}
