import { useState } from "react";
import type { Circumstances } from "../types";

interface Props {
  onSubmit: (c: Circumstances) => void;
  loading: boolean;
}

const DEFAULT: Circumstances = {
  age: "adult",
  gender: "male",
  has_mental_health: false,
  has_substance_use: false,
  has_disability: false,
  is_homeless: false,
  has_criminal_justice: false,
  has_children: false,
  is_on_medicaid: false,
  is_on_snap: false,
  is_on_tanf: false,
  is_on_ssi: false,
  has_housing_assistance: false,
  is_unemployed: false,
  has_foster_care: false,
  has_juvenile_justice: false,
  has_chronic_health: false,
  is_on_probation: false,
};

const PRESETS = [
  {
    label: "Maximum complexity",
    desc: "Touches every system. Mental health, substance use, homelessness, criminal justice, disability.",
    values: {
      has_mental_health: true,
      has_substance_use: true,
      is_homeless: true,
      has_criminal_justice: true,
      has_disability: true,
      is_on_medicaid: true,
      is_on_snap: true,
      has_housing_assistance: true,
      is_on_probation: true,
      is_unemployed: true,
    },
  },
  {
    label: "Youth crossover",
    desc: "Foster care, juvenile justice, school disruption, behavioral health.",
    values: {
      age: "youth",
      has_foster_care: true,
      has_juvenile_justice: true,
      has_mental_health: true,
      is_on_medicaid: true,
    },
  },
  {
    label: "Working parent",
    desc: "Low income, benefits cliff, children, housing assistance.",
    values: {
      gender: "female",
      has_children: true,
      is_on_medicaid: true,
      is_on_snap: true,
      is_on_tanf: true,
      has_housing_assistance: true,
    },
  },
  {
    label: "Reentry",
    desc: "Post-incarceration, homeless, no benefits, no job.",
    values: {
      has_criminal_justice: true,
      is_on_probation: true,
      is_homeless: true,
      is_unemployed: true,
      has_mental_health: true,
    },
  },
];

const SECTIONS = [
  {
    title: "Health",
    items: [
      { key: "has_mental_health", label: "Serious mental illness" },
      { key: "has_substance_use", label: "Substance use history" },
      { key: "has_chronic_health", label: "Chronic health condition" },
      { key: "has_disability", label: "Disability" },
    ],
  },
  {
    title: "Justice",
    items: [
      { key: "has_criminal_justice", label: "Criminal justice involvement" },
      { key: "is_on_probation", label: "On probation/parole" },
      { key: "has_juvenile_justice", label: "Juvenile justice history" },
    ],
  },
  {
    title: "Housing",
    items: [
      { key: "is_homeless", label: "Experiencing homelessness" },
      { key: "has_housing_assistance", label: "Housing assistance / Section 8" },
    ],
  },
  {
    title: "Income & Benefits",
    items: [
      { key: "is_on_medicaid", label: "Medicaid" },
      { key: "is_on_snap", label: "SNAP (food stamps)" },
      { key: "is_on_tanf", label: "TANF" },
      { key: "is_on_ssi", label: "SSI disability" },
      { key: "is_unemployed", label: "Unemployed" },
    ],
  },
  {
    title: "Family & Education",
    items: [
      { key: "has_children", label: "Has children" },
      { key: "has_foster_care", label: "Foster care history" },
    ],
  },
];

export default function CircumstanceSelector({ onSubmit, loading }: Props) {
  const [form, setForm] = useState<Circumstances>(DEFAULT);

  const toggle = (key: string) => {
    setForm((prev) => ({ ...prev, [key]: !(prev as unknown as Record<string, unknown>)[key] }));
  };

  const applyPreset = (preset: typeof PRESETS[number]) => {
    setForm({ ...DEFAULT, ...preset.values } as Circumstances);
  };

  const activeCount = Object.entries(form).filter(
    ([k, v]) => v === true && k !== "age" && k !== "gender"
  ).length;

  return (
    <div>
      {/* Presets */}
      <div className="section-label" style={{ marginBottom: "12px" }}>
        Quick profiles
      </div>
      <div style={{ display: "flex", flexDirection: "column", gap: "0", marginBottom: "36px" }}>
        {PRESETS.map((p) => (
          <button
            key={p.label}
            onClick={() => applyPreset(p)}
            style={{
              display: "block",
              width: "100%",
              textAlign: "left",
              background: "#FFFFFF",
              border: "none",
              borderTop: "1px solid var(--color-border)",
              padding: "16px 0",
              cursor: "pointer",
              fontFamily: "var(--font-sans)",
            }}
          >
            <span
              style={{
                fontFamily: "var(--font-mono)",
                fontSize: "14px",
                fontWeight: 600,
                display: "block",
                marginBottom: "4px",
              }}
            >
              {p.label}
            </span>
            <span
              style={{
                fontSize: "13px",
                color: "var(--color-text-secondary)",
                lineHeight: 1.4,
              }}
            >
              {p.desc}
            </span>
          </button>
        ))}
      </div>

      {/* Demographics */}
      <div style={{ display: "flex", gap: "24px", marginBottom: "32px" }}>
        <div>
          <div className="section-label">Age bracket</div>
          <div style={{ display: "flex", gap: "0" }}>
            {(["child", "youth", "young_adult", "adult", "elderly"] as const).map((a) => (
              <button
                key={a}
                onClick={() => setForm((prev) => ({ ...prev, age: a }))}
                style={{
                  padding: "6px 12px",
                  background: form.age === a ? "#000000" : "#FFFFFF",
                  color: form.age === a ? "#FFFFFF" : "var(--color-text-secondary)",
                  border: "1px solid #000000",
                  borderRight: "none",
                  cursor: "pointer",
                  fontSize: "12px",
                  fontFamily: "var(--font-mono)",
                  fontWeight: 500,
                }}
              >
                {a.replace("_", " ")}
              </button>
            ))}
            <div style={{ borderRight: "1px solid #000000" }} />
          </div>
        </div>
        <div>
          <div className="section-label">Gender</div>
          <div style={{ display: "flex", gap: "0" }}>
            {(["male", "female"] as const).map((g) => (
              <button
                key={g}
                onClick={() => setForm((prev) => ({ ...prev, gender: g }))}
                style={{
                  padding: "6px 14px",
                  background: form.gender === g ? "#000000" : "#FFFFFF",
                  color: form.gender === g ? "#FFFFFF" : "var(--color-text-secondary)",
                  border: "1px solid #000000",
                  borderRight: g === "male" ? "none" : "1px solid #000000",
                  cursor: "pointer",
                  fontSize: "12px",
                  fontFamily: "var(--font-mono)",
                  fontWeight: 500,
                }}
              >
                {g}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Circumstance checkboxes */}
      {SECTIONS.map((section) => (
        <div key={section.title} style={{ marginBottom: "28px" }}>
          <div className="section-label">{section.title}</div>
          <div style={{ display: "flex", flexDirection: "column", gap: "0" }}>
            {section.items.map((item) => {
              const checked = (form as unknown as Record<string, unknown>)[item.key] === true;
              return (
                <button
                  key={item.key}
                  onClick={() => toggle(item.key)}
                  style={{
                    display: "flex",
                    alignItems: "center",
                    gap: "12px",
                    padding: "10px 0",
                    background: "none",
                    border: "none",
                    borderBottom: "1px solid var(--color-border-light)",
                    cursor: "pointer",
                    width: "100%",
                    textAlign: "left",
                    fontFamily: "var(--font-sans)",
                    fontSize: "14px",
                    color: checked ? "#000000" : "var(--color-text-secondary)",
                    fontWeight: checked ? 600 : 400,
                  }}
                >
                  <span
                    style={{
                      width: "16px",
                      height: "16px",
                      border: checked ? "2px solid #000000" : "1px solid var(--color-border)",
                      background: checked ? "#000000" : "#FFFFFF",
                      flexShrink: 0,
                      display: "flex",
                      alignItems: "center",
                      justifyContent: "center",
                      color: "#FFFFFF",
                      fontSize: "11px",
                      fontWeight: 700,
                    }}
                  >
                    {checked ? "\u2713" : ""}
                  </span>
                  {item.label}
                </button>
              );
            })}
          </div>
        </div>
      ))}

      {/* Submit */}
      <button
        onClick={() => onSubmit(form)}
        disabled={loading || activeCount === 0}
        style={{
          width: "100%",
          padding: "16px",
          background: activeCount > 0 ? "#000000" : "var(--color-border)",
          color: "#FFFFFF",
          border: "none",
          cursor: activeCount > 0 ? "pointer" : "default",
          fontSize: "14px",
          fontFamily: "var(--font-mono)",
          fontWeight: 600,
          textTransform: "uppercase",
          letterSpacing: "0.06em",
          marginTop: "8px",
        }}
      >
        {loading
          ? "Building composite profile..."
          : `Build profile (${activeCount} circumstances)`}
      </button>
    </div>
  );
}
