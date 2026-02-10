import { useState, useCallback } from "react";
import type { CompositeProfile, Circumstances, DocumentedCase, Section } from "./types";
import { generateProfile } from "./api/client";
import CircumstanceSelector from "./components/CircumstanceSelector";
import ProfileHeader from "./components/ProfileHeader";
import TimelineView from "./components/TimelineView";
import CostView from "./components/CostView";
import CitationView from "./components/CitationView";
import CompareView from "./components/CompareView";
import CaseDetail from "./components/CaseDetail";

export default function App() {
  const [profile, setProfile] = useState<CompositeProfile | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [showForm, setShowForm] = useState(true);
  const [section, setSection] = useState<Section>("timeline");
  const [selectedCase, setSelectedCase] = useState<DocumentedCase | null>(null);

  const handleSubmit = useCallback(async (circumstances: Circumstances) => {
    setLoading(true);
    setError(null);
    try {
      const data = await generateProfile(circumstances);
      setProfile(data);
      setShowForm(false);
      setSection("timeline");
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to generate profile");
    } finally {
      setLoading(false);
    }
  }, []);

  /* ─── Landing / Circumstances page ─── */
  if (showForm) {
    return (
      <div
        style={{
          minHeight: "100%",
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "flex-start",
          padding: "64px 24px",
          background: "#FFFFFF",
        }}
      >
        <div style={{ maxWidth: "640px", width: "100%" }}>
          {/* Title */}
          <div style={{ marginBottom: "12px" }}>
            <div
              style={{
                fontFamily: "var(--font-mono)",
                fontSize: "11px",
                fontWeight: 500,
                textTransform: "uppercase",
                letterSpacing: "0.1em",
                color: "var(--color-text-tertiary)",
                marginBottom: "12px",
              }}
            >
              DOMES // Profile Research
            </div>
            <h1
              style={{
                fontFamily: "var(--font-serif)",
                fontSize: "42px",
                fontWeight: 700,
                marginBottom: "8px",
                letterSpacing: "-0.02em",
                lineHeight: 1.1,
              }}
            >
              Composite Profile
            </h1>
            <p
              style={{
                fontFamily: "var(--font-serif)",
                fontSize: "18px",
                fontStyle: "italic",
                color: "var(--color-text-secondary)",
                lineHeight: 1.5,
                marginBottom: "8px",
              }}
            >
              Build a documented composite person from real investigations, real
              audits, real published data. See what happens when government
              systems don't talk to each other -- and what it costs.
            </p>
            <p
              style={{
                fontSize: "13px",
                color: "var(--color-text-tertiary)",
                lineHeight: 1.5,
                marginBottom: "32px",
              }}
            >
              Select circumstances below. The system will construct a composite
              profile -- every cost figure, every system failure, every data gap
              is sourced from published research.
            </p>
          </div>

          {/* Back button if we already have a profile */}
          {profile && (
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
              Back to profile
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
              }}
            >
              {error}
            </div>
          )}

          <CircumstanceSelector onSubmit={handleSubmit} loading={loading} />
        </div>
      </div>
    );
  }

  /* ─── Profile view ─── */
  if (!profile) return null;

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
      {/* Profile header */}
      <ProfileHeader profile={profile} />

      {/* Tab navigation */}
      <nav
        style={{
          display: "flex",
          gap: "0",
          borderBottom: "1px solid var(--color-border)",
          padding: "0 40px",
          background: "#FFFFFF",
          flexShrink: 0,
        }}
      >
        {(
          [
            ["timeline", "Timeline"],
            ["cost", "Cost"],
            ["citations", "Citations"],
            ["compare", "Compare"],
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
            {key === "citations" && (
              <span
                style={{
                  marginLeft: "6px",
                  fontFamily: "var(--font-mono)",
                  fontSize: "11px",
                  color: "var(--color-text-tertiary)",
                  fontWeight: 500,
                }}
              >
                {profile.matched_cases.length}
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
          New profile
        </button>
      </nav>

      {/* Content area */}
      <div
        style={{
          flex: "1 1 0%",
          minHeight: 0,
          overflowY: "auto",
        }}
      >
        {section === "timeline" && (
          <TimelineView
            profile={profile}
            onCaseClick={(c) => setSelectedCase(c)}
          />
        )}
        {section === "cost" && <CostView profile={profile} />}
        {section === "citations" && (
          <CitationView
            profile={profile}
            onCaseClick={(c) => setSelectedCase(c)}
          />
        )}
        {section === "compare" && <CompareView profile={profile} />}
      </div>

      {/* Case detail panel */}
      {selectedCase && (
        <CaseDetail
          caseData={selectedCase}
          onClose={() => setSelectedCase(null)}
        />
      )}
    </div>
  );
}
