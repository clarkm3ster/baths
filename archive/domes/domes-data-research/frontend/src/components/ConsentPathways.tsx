import type { Gap, System } from "../types";

interface Props {
  gaps: Gap[];
  systemMap: Map<string, System>;
  onGapClick: (gap: Gap) => void;
}

export default function ConsentPathways({
  gaps,
  systemMap,
  onGapClick,
}: Props) {
  const closable = gaps.filter((g) => g.consent_closable);
  const notClosable = gaps.filter((g) => !g.consent_closable);

  return (
    <div style={{ padding: "32px", maxWidth: "800px" }}>
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
        Consent Pathways
      </h3>
      <p
        style={{
          fontSize: "15px",
          color: "var(--color-text-secondary)",
          marginBottom: "12px",
          lineHeight: 1.5,
          fontFamily: "var(--font-serif)",
          fontStyle: "italic",
        }}
      >
        Some gaps exist only because nobody asked you. You have the power to
        close them.
      </p>

      {/* Closable gaps */}
      {closable.length > 0 && (
        <>
          <div
            style={{
              fontFamily: "var(--font-mono)",
              fontSize: "11px",
              fontWeight: 500,
              textTransform: "uppercase",
              letterSpacing: "0.08em",
              color: "#006600",
              marginBottom: "12px",
              marginTop: "28px",
            }}
          >
            {closable.length} gap{closable.length !== 1 ? "s" : ""} you can
            close
          </div>

          <div
            style={{
              display: "flex",
              flexDirection: "column",
              gap: "0",
            }}
          >
            {closable.map((g, i) => {
              const sA = systemMap.get(g.system_a_id);
              const sB = systemMap.get(g.system_b_id);

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
                    borderTop:
                      i === 0
                        ? "2px solid #006600"
                        : "1px solid var(--color-border)",
                    padding: "20px 0",
                    cursor: "pointer",
                    fontFamily: "var(--font-sans)",
                  }}
                >
                  <div
                    style={{
                      display: "flex",
                      justifyContent: "space-between",
                      alignItems: "flex-start",
                      marginBottom: "8px",
                    }}
                  >
                    <span
                      style={{
                        fontFamily: "var(--font-mono)",
                        fontSize: "14px",
                        fontWeight: 500,
                        color: "#000000",
                      }}
                    >
                      {sA?.name || g.system_a_id}
                      {" \u2194 "}
                      {sB?.name || g.system_b_id}
                    </span>
                    <span
                      style={{
                        fontSize: "11px",
                        fontFamily: "var(--font-mono)",
                        color: "#006600",
                        border: "1px solid #006600",
                        padding: "2px 8px",
                        flexShrink: 0,
                        marginLeft: "12px",
                      }}
                    >
                      CLOSABLE
                    </span>
                  </div>

                  <p
                    style={{
                      fontSize: "15px",
                      lineHeight: 1.55,
                      color: "var(--color-text-secondary)",
                      margin: "0 0 8px",
                    }}
                  >
                    {g.consent_mechanism}
                  </p>

                  {g.barrier_law && (
                    <div
                      style={{
                        fontSize: "12px",
                        fontFamily: "var(--font-mono)",
                        color: "var(--color-text-tertiary)",
                      }}
                    >
                      Barrier: {g.barrier_law}
                    </div>
                  )}
                </button>
              );
            })}
          </div>
        </>
      )}

      {closable.length === 0 && (
        <div
          style={{
            padding: "24px 0",
            borderTop: "2px solid var(--color-border)",
            marginTop: "20px",
          }}
        >
          <p
            style={{
              fontFamily: "var(--font-serif)",
              fontSize: "17px",
              color: "var(--color-text-secondary)",
              fontStyle: "italic",
              lineHeight: 1.5,
            }}
          >
            None of the gaps in your constellation can be closed by consent
            alone. They require legislative, technical, or funding changes.
          </p>
        </div>
      )}

      {/* Non-closable gaps summary */}
      {notClosable.length > 0 && (
        <>
          <div
            style={{
              fontFamily: "var(--font-mono)",
              fontSize: "11px",
              fontWeight: 500,
              textTransform: "uppercase",
              letterSpacing: "0.08em",
              color: "var(--color-text-tertiary)",
              marginBottom: "12px",
              marginTop: "36px",
            }}
          >
            {notClosable.length} gap{notClosable.length !== 1 ? "s" : ""} that
            require systemic change
          </div>

          <div
            style={{
              display: "flex",
              flexDirection: "column",
              gap: "0",
            }}
          >
            {notClosable.map((g, i) => {
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
                  onClick={() => onGapClick(g)}
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
                    padding: "14px 0",
                    cursor: "pointer",
                    fontFamily: "var(--font-sans)",
                    fontSize: "13px",
                    color: "var(--color-text-secondary)",
                  }}
                >
                  <span
                    style={{
                      display: "inline-block",
                      width: "6px",
                      height: "6px",
                      background: sevColor,
                      marginRight: "10px",
                      verticalAlign: "middle",
                    }}
                  />
                  <span
                    style={{
                      fontFamily: "var(--font-mono)",
                      fontSize: "12px",
                      marginRight: "12px",
                    }}
                  >
                    {sA?.acronym || g.system_a_id} / {sB?.acronym || g.system_b_id}
                  </span>
                  {g.barrier_type}
                  {g.barrier_law ? ` -- ${g.barrier_law}` : ""}
                </button>
              );
            })}
          </div>
        </>
      )}
    </div>
  );
}
