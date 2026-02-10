import { useState } from "react";
import type { Filters } from "../types";
import { AGENCY_LABELS, CATEGORY_LABELS } from "../types";

interface FilterPanelProps {
  filters: Filters;
  onChange: (f: Filters) => void;
  wards: string[];
}

export default function FilterPanel({ filters, onChange, wards }: FilterPanelProps) {
  const [open, setOpen] = useState(true);

  const update = (patch: Partial<Filters>) => onChange({ ...filters, ...patch });

  return (
    <div style={{
      position: "absolute",
      top: 0,
      left: 0,
      width: open ? 260 : 40,
      height: "100%",
      background: open ? "#0A0A0A" : "transparent",
      borderRight: open ? "1px solid #1F1F1F" : "none",
      zIndex: 10,
      transition: "width 0.2s",
      display: "flex",
      flexDirection: "column",
    }}>
      <button
        onClick={() => setOpen(!open)}
        style={{
          width: 32,
          height: 32,
          margin: 4,
          background: "#141414",
          border: "1px solid #2A2A2A",
          color: "#999",
          cursor: "pointer",
          fontSize: 14,
          flexShrink: 0,
        }}
      >
        {open ? "\u2039" : "\u203A"}
      </button>

      {open && (
        <div style={{ flex: 1, overflowY: "auto", padding: "0 12px 12px" }}>
          {/* Search */}
          <Section title="Search">
            <input
              type="text"
              placeholder="Address..."
              value={filters.search || ""}
              onChange={(e) => update({ search: e.target.value || undefined })}
              style={inputStyle}
            />
          </Section>

          {/* Owner Agency */}
          <Section title="Owner">
            <select
              value={filters.owner || ""}
              onChange={(e) => update({ owner: e.target.value || undefined })}
              style={inputStyle}
            >
              <option value="">All agencies</option>
              {Object.entries(AGENCY_LABELS).map(([k, v]) => (
                <option key={k} value={k}>{v}</option>
              ))}
            </select>
          </Section>

          {/* Activation Score */}
          <Section title={`Score: ${filters.score_min}–${filters.score_max}`}>
            <div style={{ display: "flex", gap: 8, alignItems: "center" }}>
              <input
                type="range" min={0} max={100}
                value={filters.score_min}
                onChange={(e) => update({ score_min: Number(e.target.value) })}
                style={{ flex: 1, accentColor: "#fff" }}
              />
              <input
                type="range" min={0} max={100}
                value={filters.score_max}
                onChange={(e) => update({ score_max: Number(e.target.value) })}
                style={{ flex: 1, accentColor: "#fff" }}
              />
            </div>
          </Section>

          {/* Category */}
          <Section title="Activation Type">
            <select
              value={filters.category || ""}
              onChange={(e) => update({ category: e.target.value || undefined })}
              style={inputStyle}
            >
              <option value="">All types</option>
              {Object.entries(CATEGORY_LABELS).map(([k, v]) => (
                <option key={k} value={k}>{v}</option>
              ))}
            </select>
          </Section>

          {/* Vacancy */}
          <Section title="Vacancy">
            <select
              value={filters.vacancy === undefined ? "" : String(filters.vacancy)}
              onChange={(e) => {
                const v = e.target.value;
                update({ vacancy: v === "" ? undefined : v === "true" });
              }}
              style={inputStyle}
            >
              <option value="">All</option>
              <option value="true">Vacant only</option>
              <option value="false">Non-vacant only</option>
            </select>
          </Section>

          {/* Ward */}
          {wards.length > 0 && (
            <Section title="Ward">
              <select
                value={filters.ward || ""}
                onChange={(e) => update({ ward: e.target.value || undefined })}
                style={inputStyle}
              >
                <option value="">All wards</option>
                {wards.map((w) => (
                  <option key={w} value={w}>Ward {w}</option>
                ))}
              </select>
            </Section>
          )}

          {/* Reset */}
          <button
            onClick={() => onChange({ score_min: 0, score_max: 100, size_min: 0 })}
            style={{
              marginTop: 12,
              width: "100%",
              padding: "6px 0",
              background: "transparent",
              border: "1px solid #2A2A2A",
              color: "#666",
              cursor: "pointer",
              fontSize: 11,
              textTransform: "uppercase",
              letterSpacing: "0.05em",
            }}
          >
            Reset Filters
          </button>
        </div>
      )}
    </div>
  );
}

function Section({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <div style={{ marginTop: 14 }}>
      <div style={{
        fontSize: 10,
        color: "#666",
        textTransform: "uppercase",
        letterSpacing: "0.05em",
        marginBottom: 6,
      }}>
        {title}
      </div>
      {children}
    </div>
  );
}

const inputStyle: React.CSSProperties = {
  width: "100%",
  padding: "6px 8px",
  background: "#141414",
  border: "1px solid #1F1F1F",
  color: "#fff",
  fontSize: 12,
  fontFamily: "'Inter', sans-serif",
  outline: "none",
};
