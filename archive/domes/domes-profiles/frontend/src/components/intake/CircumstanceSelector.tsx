/**
 * CircumstanceSelector — grouped checkboxes for selecting life circumstances.
 *
 * Circumstances are organized by life domain with domain-colored headers.
 */

interface CircumstanceItem {
  key: string;
  label: string;
}

interface CircumstanceGroupDef {
  category: string;
  color: string;
  items: CircumstanceItem[];
}

const CIRCUMSTANCE_GROUPS: CircumstanceGroupDef[] = [
  {
    category: 'Health',
    color: 'var(--color-health)',
    items: [
      { key: 'is_on_medicaid', label: 'Enrolled in Medicaid' },
      { key: 'is_on_medicare', label: 'Enrolled in Medicare' },
      { key: 'is_uninsured', label: 'Uninsured' },
      { key: 'has_mental_health', label: 'Mental health condition' },
      { key: 'has_substance_use', label: 'Substance use disorder' },
      { key: 'has_chronic_health', label: 'Chronic health condition' },
    ],
  },
  {
    category: 'Disability',
    color: 'var(--color-education)',
    items: [
      { key: 'has_idd', label: 'Intellectual/developmental disability (IDD)' },
      { key: 'has_disability', label: 'Physical disability' },
      { key: 'has_mental_health_disability', label: 'Serious mental illness' },
    ],
  },
  {
    category: 'Justice',
    color: 'var(--color-justice)',
    items: [
      { key: 'has_criminal_justice', label: 'Currently or formerly incarcerated' },
      { key: 'is_on_probation', label: 'On probation or parole' },
      { key: 'has_juvenile_justice', label: 'Juvenile justice involvement' },
      { key: 'is_veteran', label: 'Veteran' },
    ],
  },
  {
    category: 'Housing',
    color: 'var(--color-housing)',
    items: [
      { key: 'is_homeless', label: 'Experiencing homelessness' },
      { key: 'is_in_shelter', label: 'Currently in shelter' },
      { key: 'has_section_8', label: 'Section 8 voucher' },
      { key: 'has_housing_assistance', label: 'Other housing assistance' },
    ],
  },
  {
    category: 'Income',
    color: 'var(--color-income)',
    items: [
      { key: 'is_on_ssi', label: 'Receiving SSI' },
      { key: 'is_on_ssdi', label: 'Receiving SSDI' },
      { key: 'is_on_snap', label: 'Receiving SNAP benefits' },
      { key: 'is_on_tanf', label: 'Receiving TANF' },
      { key: 'is_unemployed', label: 'Unemployed' },
    ],
  },
  {
    category: 'Family',
    color: 'var(--color-child-welfare)',
    items: [
      { key: 'has_children', label: 'Has dependent children' },
      { key: 'has_foster_care', label: 'Foster care involvement' },
    ],
  },
];

const AGE_OPTIONS = [
  { value: 'child', label: 'Child (0-12)' },
  { value: 'youth', label: 'Youth (13-24)' },
  { value: 'adult', label: 'Adult (25-64)' },
  { value: 'elderly', label: 'Elderly (65+)' },
];

const GENDER_OPTIONS = [
  { value: 'male', label: 'Male' },
  { value: 'female', label: 'Female' },
  { value: 'nonbinary', label: 'Non-binary' },
];

interface Props {
  circumstances: Record<string, boolean | string>;
  onChange: (updated: Record<string, boolean | string>) => void;
}

export default function CircumstanceSelector({ circumstances, onChange }: Props) {
  function toggleBool(key: string) {
    onChange({ ...circumstances, [key]: !circumstances[key] });
  }

  function setField(key: string, value: string) {
    onChange({ ...circumstances, [key]: value });
  }

  return (
    <div className="space-y-8">
      {/* Boolean circumstance groups */}
      {CIRCUMSTANCE_GROUPS.map((group) => (
        <div key={group.category}>
          <div
            className="font-mono text-[12px] font-semibold uppercase tracking-[0.06em] mb-3 flex items-center gap-2"
            style={{ color: group.color }}
          >
            <span
              className="inline-block w-[10px] h-[10px]"
              style={{ background: group.color }}
            />
            {group.category}
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-0">
            {group.items.map((item) => {
              const active = !!circumstances[item.key];
              return (
                <label
                  key={item.key}
                  className={`circumstance-check -mt-[1px] -ml-[1px] first:mt-0 first:ml-0 ${
                    active ? 'circumstance-check--active' : ''
                  }`}
                >
                  <input
                    type="checkbox"
                    checked={active}
                    onChange={() => toggleBool(item.key)}
                  />
                  <span className="text-[13px]">{item.label}</span>
                </label>
              );
            })}
          </div>
        </div>
      ))}

      {/* Demographics: age and gender */}
      <div>
        <div
          className="font-mono text-[12px] font-semibold uppercase tracking-[0.06em] mb-3 flex items-center gap-2"
          style={{ color: 'var(--color-education)' }}
        >
          <span
            className="inline-block w-[10px] h-[10px]"
            style={{ background: 'var(--color-education)' }}
          />
          Demographics
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
          {/* Age */}
          <div>
            <label className="text-[12px] font-mono text-[var(--color-text-tertiary)] uppercase tracking-wider block mb-2">
              Age group
            </label>
            <div className="flex flex-col gap-0">
              {AGE_OPTIONS.map((opt) => (
                <label
                  key={opt.value}
                  className={`circumstance-check -mt-[1px] first:mt-0 ${
                    circumstances.age === opt.value ? 'circumstance-check--active' : ''
                  }`}
                >
                  <input
                    type="radio"
                    name="age"
                    value={opt.value}
                    checked={circumstances.age === opt.value}
                    onChange={() => setField('age', opt.value)}
                    className="w-[16px] h-[16px] accent-black cursor-pointer"
                  />
                  <span className="text-[13px]">{opt.label}</span>
                </label>
              ))}
            </div>
          </div>

          {/* Gender */}
          <div>
            <label className="text-[12px] font-mono text-[var(--color-text-tertiary)] uppercase tracking-wider block mb-2">
              Gender
            </label>
            <div className="flex flex-col gap-0">
              {GENDER_OPTIONS.map((opt) => (
                <label
                  key={opt.value}
                  className={`circumstance-check -mt-[1px] first:mt-0 ${
                    circumstances.gender === opt.value ? 'circumstance-check--active' : ''
                  }`}
                >
                  <input
                    type="radio"
                    name="gender"
                    value={opt.value}
                    checked={circumstances.gender === opt.value}
                    onChange={() => setField('gender', opt.value)}
                    className="w-[16px] h-[16px] accent-black cursor-pointer"
                  />
                  <span className="text-[13px]">{opt.label}</span>
                </label>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
