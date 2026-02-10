interface Props {
  totalSystems: number;
  connected: number;
  siloed: number;
  gapCount: number;
  consentClosable: number;
}

export default function Summary({
  totalSystems,
  connected,
  siloed,
  gapCount,
  consentClosable,
}: Props) {
  return (
    <div
      style={{
        padding: "24px 32px",
        borderBottom: "2px solid #000000",
        background: "#FFFFFF",
      }}
    >
      {/* Main headline */}
      <h2
        style={{
          fontFamily: "var(--font-serif)",
          fontSize: "28px",
          fontWeight: 700,
          lineHeight: 1.25,
          margin: 0,
          letterSpacing: "-0.02em",
        }}
      >
        You are in{" "}
        <span
          style={{
            fontFamily: "var(--font-mono)",
            fontSize: "32px",
            fontWeight: 500,
          }}
        >
          {totalSystems}
        </span>{" "}
        systems.{" "}
        {connected > 0 ? (
          <>
            Only{" "}
            <span
              style={{
                fontFamily: "var(--font-mono)",
                fontSize: "32px",
                fontWeight: 500,
              }}
            >
              {connected}
            </span>{" "}
            are connected.
          </>
        ) : (
          <>None of them talk to each other.</>
        )}
      </h2>

      {/* Stats row */}
      <div
        style={{
          display: "flex",
          flexWrap: "wrap",
          gap: "24px",
          marginTop: "14px",
          fontSize: "14px",
          fontFamily: "var(--font-sans)",
          color: "var(--color-text-secondary)",
        }}
      >
        {siloed > 0 && (
          <span>
            <strong
              style={{
                fontFamily: "var(--font-mono)",
                color: "#000000",
                fontWeight: 500,
                fontSize: "16px",
              }}
            >
              {siloed}
            </strong>{" "}
            completely siloed
          </span>
        )}
        <span>
          <strong
            style={{
              fontFamily: "var(--font-mono)",
              color: "#CC0000",
              fontWeight: 500,
              fontSize: "16px",
            }}
          >
            {gapCount}
          </strong>{" "}
          gaps between systems that should talk
        </span>
        {consentClosable > 0 && (
          <span>
            <strong
              style={{
                fontFamily: "var(--font-mono)",
                color: "#006600",
                fontWeight: 500,
                fontSize: "16px",
              }}
            >
              {consentClosable}
            </strong>{" "}
            gaps you could close yourself
          </span>
        )}
      </div>
    </div>
  );
}
