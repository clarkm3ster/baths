import type { CompositeProfile, DocumentedCase, SystemProfile } from "../types";
import { DOMAIN_COLORS, DOMAIN_LABELS } from "../types";

interface Props {
  profile: CompositeProfile;
  onCaseClick?: (c: DocumentedCase) => void;
}

const TYPE_LABELS: Record<string, string> = {
  entry: "System entry",
  placement: "Placement",
  disruption: "Disruption",
  gap: "Data gap",
  waiting: "Waiting",
  release: "Release",
  crisis: "Crisis",
  current: "Current state",
};

export default function TimelineView({ profile, onCaseClick }: Props) {
  const { timeline, name, matched_cases, matched_systems } = profile;

  // Build a map of case ID -> DocumentedCase for citation lookups
  const caseMap = new Map<string, DocumentedCase>();
  for (const c of matched_cases) {
    caseMap.set(c.id, c);
  }

  // Group systems by domain for right panel
  const systemsByDomain: Record<string, SystemProfile[]> = {};
  for (const sys of matched_systems) {
    if (!systemsByDomain[sys.domain]) systemsByDomain[sys.domain] = [];
    systemsByDomain[sys.domain].push(sys);
  }

  return (
    <div
      style={{
        display: "grid",
        gridTemplateColumns: "60% 40%",
        height: "100%",
        minHeight: 0,
      }}
    >
      {/* LEFT: Timeline */}
      <div
        style={{
          padding: "32px 40px",
          overflowY: "auto",
          borderRight: "1px solid var(--color-border)",
        }}
      >
        {/* Narrative */}
        <div
          style={{
            padding: "28px",
            borderLeft: "3px solid #000000",
            background: "var(--color-surface)",
            marginBottom: "40px",
          }}
        >
          <p
            style={{
              fontFamily: "var(--font-serif)",
              fontSize: "18px",
              lineHeight: 1.55,
              margin: 0,
              color: "#000000",
            }}
          >
            {profile.narrative}
          </p>
        </div>

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
          Life timeline
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
          How {name} moved through the system -- every entry, every gap, every
          crisis. Each event sourced from documented cases.
        </p>

        {/* Timeline */}
        <div style={{ position: "relative", paddingLeft: "56px" }}>
          <div className="timeline-line" />

          {timeline.map((evt, i) => {
            const domainColor = evt.domain
              ? DOMAIN_COLORS[evt.domain] || "#333"
              : "#000000";
            const dotClass =
              evt.type === "crisis"
                ? "timeline-dot timeline-dot--crisis"
                : evt.type === "gap"
                  ? "timeline-dot timeline-dot--gap"
                  : evt.type === "current"
                    ? "timeline-dot timeline-dot--current"
                    : evt.type === "entry"
                      ? "timeline-dot timeline-dot--entry"
                      : "timeline-dot";

            // Look up citation if present
            const citedCase = evt.citation_id
              ? caseMap.get(evt.citation_id)
              : null;

            return (
              <div
                key={i}
                style={{
                  position: "relative",
                  paddingBottom: i < timeline.length - 1 ? "28px" : "0",
                  paddingTop: "2px",
                }}
              >
                <div className={dotClass} style={{ top: "4px" }} />

                {/* Age label */}
                <div
                  style={{
                    fontFamily: "var(--font-mono)",
                    fontSize: "12px",
                    fontWeight: 600,
                    color: "var(--color-text-tertiary)",
                    marginBottom: "4px",
                    display: "flex",
                    alignItems: "center",
                    gap: "8px",
                  }}
                >
                  Age {evt.age}
                  {evt.domain && (
                    <span
                      style={{
                        width: "8px",
                        height: "8px",
                        background: domainColor,
                        display: "inline-block",
                      }}
                    />
                  )}
                  <span
                    style={{
                      fontSize: "10px",
                      textTransform: "uppercase",
                      letterSpacing: "0.06em",
                      color:
                        evt.type === "crisis"
                          ? "#CC0000"
                          : evt.type === "gap"
                            ? "#994400"
                            : "var(--color-text-tertiary)",
                      fontWeight: 500,
                    }}
                  >
                    {TYPE_LABELS[evt.type] || evt.type}
                  </span>
                </div>

                {/* Event text + citation tag */}
                <div
                  style={{
                    display: "flex",
                    alignItems: "baseline",
                    gap: "8px",
                    flexWrap: "wrap",
                  }}
                >
                  <p
                    style={{
                      fontSize: evt.type === "current" ? "17px" : "15px",
                      fontFamily:
                        evt.type === "current"
                          ? "var(--font-serif)"
                          : "var(--font-sans)",
                      fontWeight: evt.type === "current" ? 700 : 400,
                      lineHeight: 1.5,
                      color:
                        evt.type === "crisis"
                          ? "#CC0000"
                          : evt.type === "current"
                            ? "#000000"
                            : "var(--color-text-secondary)",
                      margin: 0,
                    }}
                  >
                    {evt.event}
                  </p>

                  {/* Citation indicator */}
                  {citedCase && onCaseClick && (
                    <span
                      className="citation-tag"
                      onClick={() => onCaseClick(citedCase)}
                      role="button"
                      tabIndex={0}
                      onKeyDown={(e) => {
                        if (e.key === "Enter") onCaseClick(citedCase);
                      }}
                    >
                      [{citedCase.source}
                      {citedCase.year ? ` ${citedCase.year}` : ""}]
                    </span>
                  )}
                </div>

                {/* System tag */}
                {evt.system && (
                  <div style={{ marginTop: "6px" }}>
                    <span
                      style={{
                        fontFamily: "var(--font-mono)",
                        fontSize: "10px",
                        fontWeight: 500,
                        padding: "2px 8px",
                        border: `1px solid ${domainColor}`,
                        color: domainColor,
                        textTransform: "uppercase",
                        letterSpacing: "0.04em",
                      }}
                    >
                      {evt.system}
                    </span>
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </div>

      {/* RIGHT: Systems panel */}
      <div
        style={{
          padding: "32px 28px",
          overflowY: "auto",
          position: "sticky",
          top: 0,
          height: "100%",
          background: "var(--color-surface)",
        }}
      >
        <div className="section-label" style={{ marginBottom: "4px" }}>
          Systems involved
        </div>
        <div
          style={{
            fontFamily: "var(--font-mono)",
            fontSize: "28px",
            fontWeight: 500,
            lineHeight: 1,
            marginBottom: "24px",
          }}
        >
          {matched_systems.length}
        </div>

        {Object.entries(systemsByDomain).map(([domain, systems]) => {
          const color = DOMAIN_COLORS[domain] || "#333";
          return (
            <div key={domain} style={{ marginBottom: "28px" }}>
              {/* Domain header */}
              <div
                style={{
                  display: "flex",
                  alignItems: "center",
                  gap: "8px",
                  marginBottom: "12px",
                  paddingBottom: "8px",
                  borderBottom: `2px solid ${color}`,
                }}
              >
                <span
                  style={{
                    width: "10px",
                    height: "10px",
                    background: color,
                    display: "inline-block",
                    flexShrink: 0,
                  }}
                />
                <span
                  style={{
                    fontFamily: "var(--font-mono)",
                    fontSize: "12px",
                    fontWeight: 600,
                    textTransform: "uppercase",
                    letterSpacing: "0.06em",
                    color,
                  }}
                >
                  {DOMAIN_LABELS[domain] || domain}
                </span>
                <span
                  style={{
                    fontFamily: "var(--font-mono)",
                    fontSize: "11px",
                    color: "var(--color-text-tertiary)",
                    marginLeft: "auto",
                  }}
                >
                  {systems.length} system{systems.length !== 1 ? "s" : ""}
                </span>
              </div>

              {/* Systems list */}
              {systems.map((sys) => (
                <div
                  key={sys.id}
                  style={{
                    marginBottom: "16px",
                    paddingBottom: "16px",
                    borderBottom: "1px solid var(--color-border-light)",
                  }}
                >
                  {/* Name + acronym */}
                  <div
                    style={{
                      display: "flex",
                      alignItems: "baseline",
                      gap: "8px",
                      marginBottom: "6px",
                    }}
                  >
                    <span
                      style={{
                        fontFamily: "var(--font-mono)",
                        fontSize: "11px",
                        fontWeight: 600,
                        color,
                        padding: "1px 6px",
                        border: `1px solid ${color}`,
                      }}
                    >
                      {sys.acronym}
                    </span>
                    <span
                      style={{
                        fontSize: "13px",
                        fontWeight: 600,
                        color: "#000000",
                      }}
                    >
                      {sys.name}
                    </span>
                  </div>

                  {/* Data held tags */}
                  {sys.data_held.length > 0 && (
                    <div
                      style={{
                        display: "flex",
                        flexWrap: "wrap",
                        gap: "4px",
                        marginBottom: "6px",
                      }}
                    >
                      {sys.data_held.map((d) => (
                        <span
                          key={d}
                          style={{
                            fontFamily: "var(--font-mono)",
                            fontSize: "9px",
                            fontWeight: 500,
                            padding: "2px 6px",
                            background: "var(--color-bg)",
                            border: "1px solid var(--color-border)",
                            color: "var(--color-text-tertiary)",
                            textTransform: "uppercase",
                            letterSpacing: "0.04em",
                          }}
                        >
                          {d}
                        </span>
                      ))}
                    </div>
                  )}

                  {/* Cost per year */}
                  {sys.annual_cost_per_person != null && (
                    <div
                      style={{
                        fontFamily: "var(--font-mono)",
                        fontSize: "13px",
                        fontWeight: 500,
                        color: "var(--color-text-secondary)",
                      }}
                    >
                      ${sys.annual_cost_per_person.toLocaleString()}
                      <span
                        style={{
                          fontSize: "10px",
                          color: "var(--color-text-tertiary)",
                          marginLeft: "4px",
                        }}
                      >
                        /year
                      </span>
                    </div>
                  )}
                </div>
              ))}
            </div>
          );
        })}
      </div>
    </div>
  );
}
