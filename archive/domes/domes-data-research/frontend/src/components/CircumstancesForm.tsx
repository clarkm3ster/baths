import { useState } from "react";
import type { Profile } from "../types";

interface Props {
  onSubmit: (profile: Profile) => void;
  loading?: boolean;
}

const AGE_GROUPS = [
  { value: "under_18", label: "Under 18" },
  { value: "18_to_21", label: "18 -- 21" },
  { value: "22_to_64", label: "22 -- 64" },
  { value: "65_plus", label: "65+" },
];

const INSURANCE_OPTIONS = [
  { value: "medicaid", label: "Medicaid" },
  { value: "medicare", label: "Medicare" },
  { value: "chip", label: "CHIP" },
  { value: "private", label: "Private insurance" },
  { value: "uninsured", label: "Uninsured" },
];

const DISABILITY_OPTIONS = [
  { value: "mental_health", label: "Mental health condition" },
  { value: "sud", label: "Substance use disorder" },
  { value: "idd", label: "Intellectual / developmental disability" },
  { value: "physical", label: "Physical disability" },
  { value: "chronic_illness", label: "Chronic illness" },
];

const HOUSING_OPTIONS = [
  { value: "homeless", label: "Experiencing homelessness" },
  { value: "section_8", label: "Section 8 voucher" },
  { value: "public_housing", label: "Public housing" },
  { value: "unstable", label: "Unstable housing" },
];

const INCOME_OPTIONS = [
  { value: "ssi", label: "SSI" },
  { value: "ssdi", label: "SSDI" },
  { value: "snap", label: "SNAP / Food stamps" },
  { value: "tanf", label: "TANF / Cash assistance" },
  { value: "below_poverty", label: "Below poverty line" },
  { value: "unemployed", label: "Unemployed" },
];

const SYSTEM_OPTIONS = [
  { value: "incarcerated", label: "Currently incarcerated" },
  { value: "recently_released", label: "Recently released" },
  { value: "probation", label: "On probation / parole" },
  { value: "juvenile_justice", label: "Juvenile justice involved" },
  { value: "foster_care", label: "In foster care / aging out" },
];

const BOOLEAN_FLAGS = [
  { key: "pregnant", label: "Pregnant" },
  { key: "veteran", label: "Veteran" },
  { key: "dv_survivor", label: "Domestic violence survivor" },
  { key: "immigrant", label: "Immigrant" },
  { key: "lgbtq", label: "LGBTQ+" },
  { key: "rural", label: "Rural area" },
] as const;

/* ─── Reusable checkbox group ─── */

function CheckboxGroup({
  label,
  options,
  selected,
  onChange,
}: {
  label: string;
  options: { value: string; label: string }[];
  selected: string[];
  onChange: (values: string[]) => void;
}) {
  const toggle = (value: string) => {
    onChange(
      selected.includes(value)
        ? selected.filter((v) => v !== value)
        : [...selected, value]
    );
  };

  return (
    <fieldset
      style={{
        border: "none",
        padding: 0,
        borderBottom: "1px solid var(--color-border-light)",
        paddingBottom: "20px",
      }}
    >
      <legend
        style={{
          fontFamily: "var(--font-serif)",
          fontSize: "17px",
          fontWeight: 600,
          marginBottom: "10px",
          display: "block",
        }}
      >
        {label}
      </legend>
      <div style={{ display: "flex", flexWrap: "wrap", gap: "2px 16px" }}>
        {options.map((opt) => {
          const isChecked = selected.includes(opt.value);
          return (
            <label
              key={opt.value}
              style={{
                display: "flex",
                alignItems: "center",
                gap: "8px",
                fontSize: "14px",
                padding: "5px 0",
                cursor: "pointer",
                color: isChecked ? "#000000" : "var(--color-text-secondary)",
                fontWeight: isChecked ? 500 : 400,
                transition: "color 0.1s",
              }}
            >
              <input
                type="checkbox"
                checked={isChecked}
                onChange={() => toggle(opt.value)}
                style={{
                  accentColor: "#000",
                  width: "15px",
                  height: "15px",
                }}
              />
              {opt.label}
            </label>
          );
        })}
      </div>
    </fieldset>
  );
}

/* ─── Main form ─── */

export default function CircumstancesForm({ onSubmit, loading }: Props) {
  const [ageGroup, setAgeGroup] = useState("");
  const [insurance, setInsurance] = useState<string[]>([]);
  const [disabilities, setDisabilities] = useState<string[]>([]);
  const [housing, setHousing] = useState<string[]>([]);
  const [income, setIncome] = useState<string[]>([]);
  const [systemInvolvement, setSystemInvolvement] = useState<string[]>([]);
  const [booleans, setBooleans] = useState<Record<string, boolean>>({});

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const profile: Profile = {
      age_group: ageGroup || undefined,
      insurance,
      disabilities,
      housing,
      income,
      system_involvement: systemInvolvement,
    };
    for (const flag of BOOLEAN_FLAGS) {
      if (booleans[flag.key]) {
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        (profile as any)[flag.key] = true;
      }
    }
    onSubmit(profile);
  };

  const hasAny =
    ageGroup ||
    insurance.length ||
    disabilities.length ||
    housing.length ||
    income.length ||
    systemInvolvement.length ||
    Object.values(booleans).some(Boolean);

  const selectedCount =
    (ageGroup ? 1 : 0) +
    insurance.length +
    disabilities.length +
    housing.length +
    income.length +
    systemInvolvement.length +
    Object.values(booleans).filter(Boolean).length;

  return (
    <form onSubmit={handleSubmit}>
      <div style={{ display: "flex", flexDirection: "column", gap: "20px" }}>
        {/* Age group */}
        <fieldset
          style={{
            border: "none",
            padding: 0,
            borderBottom: "1px solid var(--color-border-light)",
            paddingBottom: "20px",
          }}
        >
          <legend
            style={{
              fontFamily: "var(--font-serif)",
              fontSize: "17px",
              fontWeight: 600,
              marginBottom: "10px",
              display: "block",
            }}
          >
            Age group
          </legend>
          <div style={{ display: "flex", flexWrap: "wrap", gap: "2px 16px" }}>
            {AGE_GROUPS.map((ag) => {
              const isChecked = ageGroup === ag.value;
              return (
                <label
                  key={ag.value}
                  style={{
                    display: "flex",
                    alignItems: "center",
                    gap: "8px",
                    fontSize: "14px",
                    padding: "5px 0",
                    cursor: "pointer",
                    color: isChecked ? "#000000" : "var(--color-text-secondary)",
                    fontWeight: isChecked ? 500 : 400,
                    transition: "color 0.1s",
                  }}
                >
                  <input
                    type="radio"
                    name="age_group"
                    value={ag.value}
                    checked={isChecked}
                    onChange={() => setAgeGroup(ag.value)}
                    style={{
                      accentColor: "#000",
                      width: "15px",
                      height: "15px",
                    }}
                  />
                  {ag.label}
                </label>
              );
            })}
          </div>
        </fieldset>

        <CheckboxGroup
          label="Insurance"
          options={INSURANCE_OPTIONS}
          selected={insurance}
          onChange={setInsurance}
        />
        <CheckboxGroup
          label="Disabilities & conditions"
          options={DISABILITY_OPTIONS}
          selected={disabilities}
          onChange={setDisabilities}
        />
        <CheckboxGroup
          label="Housing"
          options={HOUSING_OPTIONS}
          selected={housing}
          onChange={setHousing}
        />
        <CheckboxGroup
          label="Income & benefits"
          options={INCOME_OPTIONS}
          selected={income}
          onChange={setIncome}
        />
        <CheckboxGroup
          label="System involvement"
          options={SYSTEM_OPTIONS}
          selected={systemInvolvement}
          onChange={setSystemInvolvement}
        />

        {/* Boolean flags */}
        <fieldset
          style={{
            border: "none",
            padding: 0,
            borderBottom: "1px solid var(--color-border-light)",
            paddingBottom: "20px",
          }}
        >
          <legend
            style={{
              fontFamily: "var(--font-serif)",
              fontSize: "17px",
              fontWeight: 600,
              marginBottom: "10px",
              display: "block",
            }}
          >
            Additional circumstances
          </legend>
          <div style={{ display: "flex", flexWrap: "wrap", gap: "2px 16px" }}>
            {BOOLEAN_FLAGS.map((flag) => {
              const isChecked = !!booleans[flag.key];
              return (
                <label
                  key={flag.key}
                  style={{
                    display: "flex",
                    alignItems: "center",
                    gap: "8px",
                    fontSize: "14px",
                    padding: "5px 0",
                    cursor: "pointer",
                    color: isChecked ? "#000000" : "var(--color-text-secondary)",
                    fontWeight: isChecked ? 500 : 400,
                    transition: "color 0.1s",
                  }}
                >
                  <input
                    type="checkbox"
                    checked={isChecked}
                    onChange={() =>
                      setBooleans((prev) => ({
                        ...prev,
                        [flag.key]: !prev[flag.key],
                      }))
                    }
                    style={{
                      accentColor: "#000",
                      width: "15px",
                      height: "15px",
                    }}
                  />
                  {flag.label}
                </label>
              );
            })}
          </div>
        </fieldset>

        {/* Submit button */}
        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: "16px",
            paddingTop: "4px",
          }}
        >
          <button
            type="submit"
            disabled={!hasAny || loading}
            style={{
              fontFamily: "var(--font-sans)",
              fontSize: "14px",
              fontWeight: 600,
              padding: "12px 32px",
              background: hasAny ? "#000000" : "#CCCCCC",
              color: "#FFFFFF",
              border: "none",
              cursor: hasAny ? "pointer" : "default",
              letterSpacing: "0.04em",
              textTransform: "uppercase",
              transition: "background 0.15s",
            }}
          >
            {loading ? "Mapping your data..." : "Show my constellation"}
          </button>
          {selectedCount > 0 && (
            <span
              style={{
                fontFamily: "var(--font-mono)",
                fontSize: "12px",
                color: "var(--color-text-tertiary)",
              }}
            >
              {selectedCount} selected
            </span>
          )}
        </div>
      </div>
    </form>
  );
}
