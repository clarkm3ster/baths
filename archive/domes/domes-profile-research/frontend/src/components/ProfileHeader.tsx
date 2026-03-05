import type { CompositeProfile } from "../types";
import { DOMAIN_COLORS, DOMAIN_LABELS } from "../types";

interface Props {
  profile: CompositeProfile;
}

export default function ProfileHeader({ profile }: Props) {
  const savings = profile.total_annual_cost - profile.coordinated_cost;

  // Count systems per domain
  const domainCounts: Record<string, number> = {};
  for (const s of profile.matched_systems) {
    domainCounts[s.domain] = (domainCounts[s.domain] || 0) + 1;
  }
  const domains = Object.keys(domainCounts);

  return (
    <div
      style={{
        padding: "32px 40px",
        borderBottom: "2px solid #000000",
        background: "#FFFFFF",
      }}
    >
      {/* Name + age */}
      <div style={{ marginBottom: "6px" }}>
        <span
          className="section-label"
          style={{ marginBottom: "0", display: "inline" }}
        >
          Composite Profile
        </span>
      </div>
      <h1
        style={{
          fontFamily: "var(--font-serif)",
          fontSize: "42px",
          fontWeight: 700,
          lineHeight: 1.1,
          letterSpacing: "-0.02em",
          margin: "0 0 6px",
        }}
      >
        {profile.name}
      </h1>
      <div
        style={{
          fontFamily: "var(--font-serif)",
          fontSize: "18px",
          fontStyle: "italic",
          color: "var(--color-text-secondary)",
          marginBottom: "20px",
          lineHeight: 1.4,
        }}
      >
        {profile.age} years old. In {profile.systems_involved.length} government
        systems. None of them talk to each other.
      </div>

      {/* Stats row */}
      <div
        style={{
          display: "flex",
          flexWrap: "wrap",
          gap: "32px",
          alignItems: "baseline",
        }}
      >
        <div>
          <div className="stat-number">{profile.systems_involved.length}</div>
          <div
            style={{
              fontSize: "12px",
              fontFamily: "var(--font-mono)",
              color: "var(--color-text-tertiary)",
              marginTop: "4px",
            }}
          >
            systems
          </div>
        </div>
        <div>
          <div className="stat-number" style={{ color: "var(--color-cost)" }}>
            ${profile.total_annual_cost.toLocaleString()}
          </div>
          <div
            style={{
              fontSize: "12px",
              fontFamily: "var(--font-mono)",
              color: "var(--color-text-tertiary)",
              marginTop: "4px",
            }}
          >
            annual cost (fragmented)
          </div>
        </div>
        <div>
          <div className="stat-number" style={{ color: "var(--color-savings)" }}>
            ${savings.toLocaleString()}
          </div>
          <div
            style={{
              fontSize: "12px",
              fontFamily: "var(--font-mono)",
              color: "var(--color-text-tertiary)",
              marginTop: "4px",
            }}
          >
            wasted per year
          </div>
        </div>
        <div>
          <div className="stat-number">{profile.matched_cases.length}</div>
          <div
            style={{
              fontSize: "12px",
              fontFamily: "var(--font-mono)",
              color: "var(--color-text-tertiary)",
              marginTop: "4px",
            }}
          >
            citations
          </div>
        </div>
      </div>

      {/* Domain chips with counts */}
      <div
        style={{
          display: "flex",
          flexWrap: "wrap",
          gap: "6px",
          marginTop: "20px",
        }}
      >
        {domains.map((d) => (
          <span
            key={d}
            style={{
              fontFamily: "var(--font-mono)",
              fontSize: "11px",
              fontWeight: 500,
              padding: "3px 10px",
              border: `1px solid ${DOMAIN_COLORS[d] || "#333"}`,
              color: DOMAIN_COLORS[d] || "#333",
              letterSpacing: "0.02em",
            }}
          >
            {DOMAIN_LABELS[d] || d}: {domainCounts[d]}
          </span>
        ))}
      </div>
    </div>
  );
}
