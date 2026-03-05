import { CIRCUMSTANCES, type Circumstance } from "../../types";

const CIRCUMSTANCE_LABELS: Record<Circumstance, string> = {
  medicaid: "Medicaid",
  incarcerated: "Incarcerated",
  recently_released: "Recently Released",
  substance_use: "Substance Use",
  mental_health: "Mental Health",
  homeless: "Homeless",
  foster_care: "Foster Care",
  veteran: "Veteran",
  disabled: "Disabled",
  low_income: "Low Income",
  school_age: "School Age",
  special_education: "Special Education",
  pregnant: "Pregnant",
  unemployed: "Unemployed",
  snap_recipient: "SNAP Recipient",
  tanf_recipient: "TANF Recipient",
  child_support: "Child Support",
  probation: "Probation",
  parole: "Parole",
  immigration: "Immigration",
};

const CIRCUMSTANCE_GROUPS: { label: string; items: Circumstance[] }[] = [
  {
    label: "Justice",
    items: ["incarcerated", "recently_released", "probation", "parole"],
  },
  {
    label: "Health",
    items: ["medicaid", "substance_use", "mental_health", "pregnant", "disabled"],
  },
  {
    label: "Economic",
    items: [
      "low_income",
      "unemployed",
      "snap_recipient",
      "tanf_recipient",
      "child_support",
    ],
  },
  {
    label: "Housing / Care",
    items: ["homeless", "foster_care", "veteran"],
  },
  {
    label: "Education",
    items: ["school_age", "special_education"],
  },
  {
    label: "Other",
    items: ["immigration"],
  },
];

interface CircumstancesFormProps {
  selected: string[];
  onChange: (selected: string[]) => void;
  onSubmit: () => void;
  loading: boolean;
}

export function CircumstancesForm({
  selected,
  onChange,
  onSubmit,
  loading,
}: CircumstancesFormProps) {
  function toggle(circumstance: string) {
    if (selected.includes(circumstance)) {
      onChange(selected.filter((c) => c !== circumstance));
    } else {
      onChange([...selected, circumstance]);
    }
  }

  return (
    <div className="panel">
      <div className="panel-header">
        <h3 className="text-sm">Select Circumstances</h3>
        <p className="font-mono text-[0.625rem] text-gray-500 mt-0.5">
          Choose all that apply to map relevant government data systems
        </p>
      </div>
      <div className="panel-body space-y-4">
        {CIRCUMSTANCE_GROUPS.map((group) => (
          <div key={group.label}>
            <h4 className="font-mono text-[0.625rem] font-bold uppercase tracking-wider text-gray-500 mb-2">
              {group.label}
            </h4>
            <div className="flex flex-wrap gap-1">
              {group.items.map((item) => {
                const isSelected = selected.includes(item);
                return (
                  <button
                    key={item}
                    type="button"
                    className={`font-mono text-xs px-3 py-1.5 border transition-colors ${
                      isSelected
                        ? "bg-black text-white border-black"
                        : "bg-white text-black border-gray-300 hover:border-black"
                    }`}
                    onClick={() => toggle(item)}
                  >
                    {CIRCUMSTANCE_LABELS[item] || item}
                  </button>
                );
              })}
            </div>
          </div>
        ))}

        <div className="flex items-center gap-3 pt-2 border-t border-black">
          <button
            className="btn btn-primary"
            onClick={onSubmit}
            disabled={selected.length === 0 || loading}
          >
            {loading ? "MAPPING..." : "MAP MY DATA"}
          </button>
          <span className="font-mono text-[0.625rem] text-gray-500">
            {selected.length} selected
          </span>
          {selected.length > 0 && (
            <button
              className="btn btn-sm"
              onClick={() => onChange([])}
              disabled={loading}
            >
              CLEAR
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
