import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { matchProvisions } from '../api/client';
import type { PersonProfile } from '../types';

const CHECKBOX_GROUPS = [
  {
    key: 'insurance',
    label: 'Health Insurance',
    options: [
      { value: 'medicaid', label: 'Medicaid' },
      { value: 'medicare', label: 'Medicare' },
      { value: 'private', label: 'Private Insurance' },
      { value: 'uninsured', label: 'Uninsured' },
      { value: 'chip', label: 'CHIP' },
    ],
  },
  {
    key: 'disabilities',
    label: 'Disability / Condition',
    options: [
      { value: 'mental_health', label: 'Mental health condition' },
      { value: 'sud', label: 'Substance use disorder' },
      { value: 'idd', label: 'Intellectual/developmental disability' },
      { value: 'physical', label: 'Physical disability' },
      { value: 'chronic_illness', label: 'Chronic illness' },
    ],
  },
  {
    key: 'housing',
    label: 'Housing',
    options: [
      { value: 'section_8', label: 'Section 8 voucher' },
      { value: 'public_housing', label: 'Public housing' },
      { value: 'homeless', label: 'Homeless/unstable housing' },
      { value: 'private_rental', label: 'Private rental' },
      { value: 'homeowner', label: 'Homeowner' },
    ],
  },
  {
    key: 'income',
    label: 'Income',
    options: [
      { value: 'ssi', label: 'SSI recipient' },
      { value: 'ssdi', label: 'SSDI recipient' },
      { value: 'snap', label: 'SNAP recipient' },
      { value: 'tanf', label: 'TANF recipient' },
      { value: 'below_poverty', label: 'Employed below poverty line' },
      { value: 'unemployed', label: 'Unemployed' },
    ],
  },
  {
    key: 'system_involvement',
    label: 'System Involvement',
    options: [
      { value: 'incarcerated', label: 'Currently incarcerated' },
      { value: 'recently_released', label: 'Recently released' },
      { value: 'probation', label: 'On probation/parole' },
      { value: 'juvenile_justice', label: 'Juvenile justice involvement' },
      { value: 'foster_care', label: 'Child welfare/foster care' },
    ],
  },
] as const;

const AGE_OPTIONS = [
  { value: 'under_18', label: 'Under 18' },
  { value: '18_to_21', label: '18\u201321' },
  { value: '22_to_64', label: '22\u201364' },
  { value: '65_plus', label: '65+' },
] as const;

const BOOLEAN_OPTIONS = [
  { key: 'pregnant' as const, label: 'Pregnant' },
  { key: 'veteran' as const, label: 'Veteran' },
  { key: 'dv_survivor' as const, label: 'Domestic violence survivor' },
  { key: 'immigrant' as const, label: 'Immigrant' },
  { key: 'lgbtq' as const, label: 'LGBTQ+' },
  { key: 'rural' as const, label: 'Rural area resident' },
];

const US_STATES = [
  'Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado',
  'Connecticut', 'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Idaho',
  'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana',
  'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota',
  'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada',
  'New Hampshire', 'New Jersey', 'New Mexico', 'New York',
  'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon',
  'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota',
  'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington',
  'West Virginia', 'Wisconsin', 'Wyoming', 'District of Columbia',
];

type ArrayField = 'insurance' | 'disabilities' | 'housing' | 'income' | 'system_involvement';

function createEmptyProfile(): PersonProfile {
  return {
    insurance: [],
    disabilities: [],
    age_group: '',
    pregnant: false,
    housing: [],
    income: [],
    system_involvement: [],
    veteran: false,
    dv_survivor: false,
    immigrant: false,
    lgbtq: false,
    rural: false,
    state: '',
  };
}

export function CircumstancesPage() {
  const navigate = useNavigate();
  const [profile, setProfile] = useState<PersonProfile>(createEmptyProfile);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  function handleArrayCheckbox(field: ArrayField, value: string, checked: boolean) {
    setProfile((prev) => ({
      ...prev,
      [field]: checked
        ? [...prev[field], value]
        : prev[field].filter((v) => v !== value),
    }));
  }

  function handleBoolean(key: keyof PersonProfile, checked: boolean) {
    setProfile((prev) => ({ ...prev, [key]: checked }));
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const result = await matchProvisions(profile);
      navigate('/dome', { state: { matchResult: result } });
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : 'Failed to connect to the matching engine. Ensure the backend is running.'
      );
    } finally {
      setLoading(false);
    }
  }

  const hasSelections =
    profile.insurance.length > 0 ||
    profile.disabilities.length > 0 ||
    profile.age_group !== '' ||
    profile.pregnant ||
    profile.housing.length > 0 ||
    profile.income.length > 0 ||
    profile.system_involvement.length > 0 ||
    profile.veteran ||
    profile.dv_survivor ||
    profile.immigrant ||
    profile.lgbtq ||
    profile.rural ||
    profile.state !== '';

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 py-12">
      <header className="mb-12">
        <h1 className="font-serif text-3xl sm:text-4xl mb-4">
          Describe your circumstances
        </h1>
        <p className="text-black/60 text-base sm:text-lg max-w-2xl leading-relaxed">
          Select the legal statuses that apply to you. These are used to identify
          the federal provisions, rights, and protections relevant to your situation.
          All information stays in your browser.
        </p>
      </header>

      <form onSubmit={handleSubmit}>
        <div className="space-y-10">
          {/* Array-based checkbox groups */}
          {CHECKBOX_GROUPS.map((group) => (
            <fieldset key={group.key} className="border-t border-border pt-6">
              <legend className="font-serif text-lg font-medium mb-4">
                {group.label}
              </legend>
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
                {group.options.map((option) => {
                  const checked = profile[group.key as ArrayField].includes(option.value);
                  return (
                    <label
                      key={option.value}
                      className={`flex items-center gap-3 p-3 border cursor-pointer transition-colors ${
                        checked
                          ? 'border-black bg-black/[0.03]'
                          : 'border-border hover:border-black/30'
                      }`}
                    >
                      <input
                        type="checkbox"
                        checked={checked}
                        onChange={(e) =>
                          handleArrayCheckbox(group.key as ArrayField, option.value, e.target.checked)
                        }
                        className="w-4 h-4 accent-black"
                        aria-label={option.label}
                      />
                      <span className="text-sm">{option.label}</span>
                    </label>
                  );
                })}
              </div>
            </fieldset>
          ))}

          {/* Age group (radio - single selection) */}
          <fieldset className="border-t border-border pt-6">
            <legend className="font-serif text-lg font-medium mb-4">
              Age
            </legend>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
              {AGE_OPTIONS.map((option) => {
                const checked = profile.age_group === option.value;
                return (
                  <label
                    key={option.value}
                    className={`flex items-center gap-3 p-3 border cursor-pointer transition-colors ${
                      checked
                        ? 'border-black bg-black/[0.03]'
                        : 'border-border hover:border-black/30'
                    }`}
                  >
                    <input
                      type="radio"
                      name="age_group"
                      value={option.value}
                      checked={checked}
                      onChange={() =>
                        setProfile((prev) => ({ ...prev, age_group: option.value }))
                      }
                      className="w-4 h-4 accent-black"
                      aria-label={option.label}
                    />
                    <span className="text-sm">{option.label}</span>
                  </label>
                );
              })}
            </div>
          </fieldset>

          {/* Boolean options (pregnant, veteran, etc.) */}
          <fieldset className="border-t border-border pt-6">
            <legend className="font-serif text-lg font-medium mb-4">
              Other
            </legend>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
              {BOOLEAN_OPTIONS.map((option) => {
                const checked = profile[option.key] as boolean;
                return (
                  <label
                    key={option.key}
                    className={`flex items-center gap-3 p-3 border cursor-pointer transition-colors ${
                      checked
                        ? 'border-black bg-black/[0.03]'
                        : 'border-border hover:border-black/30'
                    }`}
                  >
                    <input
                      type="checkbox"
                      checked={checked}
                      onChange={(e) => handleBoolean(option.key, e.target.checked)}
                      className="w-4 h-4 accent-black"
                      aria-label={option.label}
                    />
                    <span className="text-sm">{option.label}</span>
                  </label>
                );
              })}
            </div>
          </fieldset>

          {/* State dropdown */}
          <fieldset className="border-t border-border pt-6">
            <legend className="font-serif text-lg font-medium mb-4">
              State
            </legend>
            <select
              value={profile.state}
              onChange={(e) =>
                setProfile((prev) => ({ ...prev, state: e.target.value }))
              }
              className="w-full sm:w-80 p-3 border border-border bg-white text-sm focus:border-black"
              aria-label="Select your state"
            >
              <option value="">Select a state</option>
              {US_STATES.map((state) => (
                <option key={state} value={state}>
                  {state}
                </option>
              ))}
            </select>
          </fieldset>
        </div>

        {error && (
          <div
            className="mt-8 p-4 border border-domain-education text-domain-education text-sm"
            role="alert"
          >
            {error}
          </div>
        )}

        <div className="mt-12 border-t border-border pt-8">
          <button
            type="submit"
            disabled={loading || !hasSelections}
            className={`border-2 border-black px-8 py-4 text-lg font-medium transition-colors ${
              loading || !hasSelections
                ? 'bg-border text-black/40 border-border cursor-not-allowed'
                : 'bg-black text-white hover:bg-white hover:text-black cursor-pointer'
            }`}
            aria-label="Submit circumstances and map your rights"
          >
            {loading ? 'Mapping provisions\u2026' : 'Map My Rights'}
          </button>
          <p className="mt-4 text-xs text-black/40">
            Your selections are sent to the matching engine and are not stored.
          </p>
        </div>
      </form>
    </div>
  );
}
