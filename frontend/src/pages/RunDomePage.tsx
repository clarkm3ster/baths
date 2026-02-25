import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const SOURCE_TYPES = [
  { value: 'fictional', label: 'Fictional', desc: 'From a book, film, screenplay, or imagined scenario' },
  { value: 'real', label: 'Real', desc: 'A real case study, journalism, or lived experience' },
  { value: 'composite', label: 'Composite', desc: 'Blended from multiple real or fictional sources' },
  { value: 'archetypal', label: 'Archetypal', desc: 'A representative pattern — the median, the edge case' },
] as const;

const TIER_OPTIONS = [
  { value: 'blockbuster', label: 'Blockbuster', budget: '$1M+', team: '15-80', layers: 12 },
  { value: 'indie', label: 'Indie', budget: '$50K-$250K', team: '5-15', layers: 9 },
  { value: 'micro', label: 'Micro', budget: '$5K-$50K', team: '2-5', layers: 6 },
] as const;

const SYSTEM_OPTIONS = [
  'Medicaid', 'Medicare', 'SNAP', 'Section 8', 'SSI/SSDI', 'TANF',
  'WIC', 'CHIP', 'LIHEAP', 'Head Start', 'Free School Lunch',
  'Pell Grant', 'Foster Care', 'Probation/Parole', 'Veterans Affairs',
  'Workers Compensation', 'Unemployment Insurance', 'Child Support',
];

const FLOURISHING_DIMENSIONS = [
  'Autonomy', 'Purpose', 'Connection', 'Safety', 'Health',
  'Creativity', 'Stability', 'Growth', 'Joy', 'Belonging',
  'Dignity', 'Agency',
];

const DISABILITY_OPTIONS = [
  { value: 'mental_health', label: 'Mental health condition' },
  { value: 'sud', label: 'Substance use disorder' },
  { value: 'idd', label: 'Intellectual/developmental disability' },
  { value: 'physical', label: 'Physical disability' },
  { value: 'chronic_illness', label: 'Chronic illness' },
];

const HOUSING_OPTIONS = [
  { value: 'section_8', label: 'Section 8 voucher' },
  { value: 'public_housing', label: 'Public housing' },
  { value: 'homeless', label: 'Homeless/unstable' },
  { value: 'private_rental', label: 'Private rental' },
  { value: 'homeowner', label: 'Homeowner' },
];

const INCOME_OPTIONS = [
  { value: 'ssi', label: 'SSI' },
  { value: 'ssdi', label: 'SSDI' },
  { value: 'snap', label: 'SNAP' },
  { value: 'tanf', label: 'TANF' },
  { value: 'below_poverty', label: 'Below poverty line' },
  { value: 'unemployed', label: 'Unemployed' },
];

const IP_DOMAINS = [
  { value: 'entertainment', label: 'Entertainment' },
  { value: 'technology', label: 'Technology' },
  { value: 'financial_product', label: 'Financial Product' },
  { value: 'policy', label: 'Policy' },
  { value: 'product', label: 'Product Design' },
  { value: 'research', label: 'Research' },
  { value: 'healthcare', label: 'Healthcare' },
  { value: 'housing', label: 'Housing' },
  { value: 'education', label: 'Education' },
  { value: 'architectural', label: 'Architecture' },
  { value: 'performance', label: 'Performance' },
  { value: 'fashion', label: 'Fashion' },
];

interface CharacterForm {
  name: string;
  source_type: string;
  source_citation: string;
  fictional_source: string;
  age: string;
  gender: string;
  location_city: string;
  location_state: string;
  situation: string;
  full_landscape: string;
  production_challenge: string;
  insurance: string[];
  disabilities: string[];
  housing: string[];
  income: string[];
  system_involvement: string[];
  key_systems: string[];
  flourishing_dimensions: string[];
  veteran: boolean;
  dv_survivor: boolean;
  immigrant: boolean;
  pregnant: boolean;
  tier: string;
  focus_domains: string[];
}

function createEmptyForm(): CharacterForm {
  return {
    name: '',
    source_type: 'fictional',
    source_citation: '',
    fictional_source: '',
    age: '',
    gender: '',
    location_city: '',
    location_state: '',
    situation: '',
    full_landscape: '',
    production_challenge: '',
    insurance: [],
    disabilities: [],
    housing: [],
    income: [],
    system_involvement: [],
    key_systems: [],
    flourishing_dimensions: [],
    veteran: false,
    dv_survivor: false,
    immigrant: false,
    pregnant: false,
    tier: 'indie',
    focus_domains: [],
  };
}

const EXAMPLE_CHARACTERS = [
  {
    name: 'Marcus',
    source_type: 'archetypal',
    situation: 'Single dad, 34, two kids. Systems-heavy: Medicaid, SNAP, Section 8 waitlist, child support. $28K/year. Works overnight shifts. One kid needs speech therapy the insurance won\'t cover. Car just failed inspection.',
    tier: 'blockbuster',
    key_systems: ['Medicaid', 'SNAP', 'Section 8', 'Child Support', 'Workers Compensation'],
    full_landscape: 'Not just the systems — Marcus coaches his son\'s basketball team on Saturdays. He\'s teaching himself to code from YouTube. His mother watches the kids during overnight shifts but she\'s 68 and it\'s wearing on her.',
  },
  {
    name: 'Aisha',
    source_type: 'archetypal',
    situation: 'Aged out of foster care at 19. $12K/year. No family safety net. Couch surfing. Community college enrollment pending. History of mental health services in the system. Brilliant writer.',
    tier: 'indie',
    key_systems: ['Foster Care', 'Medicaid', 'Pell Grant', 'SNAP'],
    full_landscape: 'Aisha keeps a journal. She wants to write about what the system did and didn\'t do. She has a support worker she trusts but the program ends in 6 months.',
  },
  {
    name: 'Dasani',
    source_type: 'fictional',
    source_citation: 'Invisible Child by Andrea Elliott',
    fictional_source: 'Invisible Child',
    situation: 'Girl growing up in a NYC homeless shelter. Family of 10 in one room. Navigating school, poverty, the shelter system, and child welfare simultaneously. Exceptional student despite everything.',
    tier: 'blockbuster',
    key_systems: ['Homeless Shelter', 'SNAP', 'Medicaid', 'Free School Lunch', 'Child Support', 'Foster Care'],
    full_landscape: 'Dasani is the oldest. She mothers her siblings. She excels at school when she can get there. The shelter has rules that contradict the school\'s rules. Every system sees a different piece of her.',
  },
];

export function RunDomePage() {
  const navigate = useNavigate();
  const [form, setForm] = useState<CharacterForm>(createEmptyForm);
  const [step, setStep] = useState(0);
  const [generating, setGenerating] = useState(false);

  function loadExample(example: typeof EXAMPLE_CHARACTERS[0]) {
    setForm({
      ...createEmptyForm(),
      name: example.name,
      source_type: example.source_type,
      source_citation: (example as Record<string, unknown>).source_citation as string || '',
      fictional_source: (example as Record<string, unknown>).fictional_source as string || '',
      situation: example.situation,
      full_landscape: example.full_landscape,
      tier: example.tier,
      key_systems: example.key_systems,
    });
    setStep(1);
  }

  function toggleArray(field: keyof CharacterForm, value: string) {
    setForm((prev) => {
      const arr = prev[field] as string[];
      return {
        ...prev,
        [field]: arr.includes(value)
          ? arr.filter((v) => v !== value)
          : [...arr, value],
      };
    });
  }

  function handleGenerate() {
    setGenerating(true);
    // Simulate generation (in production, this calls the PersonRunner API)
    setTimeout(() => {
      navigate('/dome-output', { state: { character: form } });
    }, 2000);
  }

  const steps = [
    { title: 'Character', desc: 'Who is this person?' },
    { title: 'Circumstances', desc: 'What is their situation?' },
    { title: 'Systems', desc: 'What systems do they touch?' },
    { title: 'Production', desc: 'What kind of dome?' },
  ];

  const canProceed = step === 0
    ? form.name.length > 0
    : step === 1
    ? form.situation.length > 0
    : step === 2
    ? form.key_systems.length > 0
    : true;

  return (
    <div className="pt-20 min-h-screen bg-white">
      {/* Header */}
      <section className="py-12 px-6 border-b border-border">
        <div className="max-w-4xl mx-auto">
          <p className="text-sm tracking-[0.4em] uppercase text-black/40 mb-4">
            Person-Runner
          </p>
          <h1 className="font-serif text-4xl sm:text-5xl leading-tight mb-4">
            Run a Dome
          </h1>
          <p className="text-lg text-black/50 max-w-2xl">
            Input a character and their circumstances. Person-Runner generates
            the complete dome — IP portfolio, business case, team, simulation, and website.
          </p>
        </div>
      </section>

      {/* Example characters */}
      {step === 0 && (
        <section className="py-8 px-6 bg-[#FAFAFA] border-b border-border">
          <div className="max-w-4xl mx-auto">
            <p className="text-sm font-medium text-black/40 mb-4">
              Or start with an example character:
            </p>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
              {EXAMPLE_CHARACTERS.map((ex) => (
                <button
                  key={ex.name}
                  onClick={() => loadExample(ex)}
                  className="text-left p-4 bg-white border border-border hover:border-black transition-colors cursor-pointer"
                >
                  <p className="font-serif text-lg mb-1">{ex.name}</p>
                  <p className="text-xs text-black/40 uppercase tracking-wider mb-2">{ex.source_type} &middot; {ex.tier}</p>
                  <p className="text-sm text-black/50 line-clamp-3">{ex.situation}</p>
                </button>
              ))}
            </div>
          </div>
        </section>
      )}

      {/* Step indicator */}
      <div className="px-6 py-6 border-b border-border">
        <div className="max-w-4xl mx-auto flex gap-2">
          {steps.map((s, i) => (
            <button
              key={s.title}
              onClick={() => i <= step && setStep(i)}
              className={`flex-1 p-3 text-left border transition-colors ${
                i === step
                  ? 'border-black bg-black text-white'
                  : i < step
                  ? 'border-black/20 bg-black/5 cursor-pointer'
                  : 'border-border text-black/30 cursor-default'
              }`}
            >
              <span className="font-mono text-xs block">{String(i + 1).padStart(2, '0')}</span>
              <span className="text-sm font-medium">{s.title}</span>
            </button>
          ))}
        </div>
      </div>

      {/* Form content */}
      <div className="max-w-4xl mx-auto px-6 py-12">
        {/* Step 0: Character Identity */}
        {step === 0 && (
          <div className="space-y-8">
            <div>
              <label className="block text-sm font-medium mb-2">Character Name</label>
              <input
                type="text"
                value={form.name}
                onChange={(e) => setForm((f) => ({ ...f, name: e.target.value }))}
                placeholder="e.g., Marcus, Dasani, Elena..."
                className="w-full p-4 border border-border text-lg focus:border-black focus:outline-none"
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-3">Source Type</label>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                {SOURCE_TYPES.map((st) => (
                  <label
                    key={st.value}
                    className={`flex flex-col p-4 border cursor-pointer transition-colors ${
                      form.source_type === st.value
                        ? 'border-black bg-black/[0.03]'
                        : 'border-border hover:border-black/30'
                    }`}
                  >
                    <div className="flex items-center gap-3">
                      <input
                        type="radio"
                        name="source_type"
                        value={st.value}
                        checked={form.source_type === st.value}
                        onChange={() => setForm((f) => ({ ...f, source_type: st.value }))}
                        className="accent-black"
                      />
                      <span className="font-medium">{st.label}</span>
                    </div>
                    <span className="text-xs text-black/40 mt-1 ml-7">{st.desc}</span>
                  </label>
                ))}
              </div>
            </div>

            {(form.source_type === 'fictional' || form.source_type === 'real') && (
              <div>
                <label className="block text-sm font-medium mb-2">
                  {form.source_type === 'fictional' ? 'Source Work' : 'Source Citation'}
                </label>
                <input
                  type="text"
                  value={form.source_citation}
                  onChange={(e) => setForm((f) => ({ ...f, source_citation: e.target.value }))}
                  placeholder={form.source_type === 'fictional'
                    ? 'e.g., The Wire, Invisible Child, Evicted...'
                    : 'e.g., Case study, article, report...'}
                  className="w-full p-3 border border-border focus:border-black focus:outline-none"
                />
              </div>
            )}

            <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
              <div>
                <label className="block text-sm font-medium mb-2">Age</label>
                <input
                  type="number"
                  value={form.age}
                  onChange={(e) => setForm((f) => ({ ...f, age: e.target.value }))}
                  placeholder="34"
                  className="w-full p-3 border border-border focus:border-black focus:outline-none"
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-2">Gender</label>
                <input
                  type="text"
                  value={form.gender}
                  onChange={(e) => setForm((f) => ({ ...f, gender: e.target.value }))}
                  placeholder="Male"
                  className="w-full p-3 border border-border focus:border-black focus:outline-none"
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-2">City</label>
                <input
                  type="text"
                  value={form.location_city}
                  onChange={(e) => setForm((f) => ({ ...f, location_city: e.target.value }))}
                  placeholder="Philadelphia"
                  className="w-full p-3 border border-border focus:border-black focus:outline-none"
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-2">State</label>
                <input
                  type="text"
                  value={form.location_state}
                  onChange={(e) => setForm((f) => ({ ...f, location_state: e.target.value }))}
                  placeholder="PA"
                  className="w-full p-3 border border-border focus:border-black focus:outline-none"
                />
              </div>
            </div>
          </div>
        )}

        {/* Step 1: Circumstances */}
        {step === 1 && (
          <div className="space-y-8">
            <div>
              <label className="block text-sm font-medium mb-2">
                Their Situation
              </label>
              <p className="text-xs text-black/40 mb-3">
                What's happening in their life? The systems, the pressures, the circumstances.
              </p>
              <textarea
                value={form.situation}
                onChange={(e) => setForm((f) => ({ ...f, situation: e.target.value }))}
                rows={5}
                placeholder="Single dad, 34, two kids. Systems-heavy: Medicaid, SNAP, Section 8 waitlist..."
                className="w-full p-4 border border-border focus:border-black focus:outline-none text-base leading-relaxed resize-none"
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">
                Full Landscape
              </label>
              <p className="text-xs text-black/40 mb-3">
                Not just the problems — their whole life. What do they care about? What are they good at?
              </p>
              <textarea
                value={form.full_landscape}
                onChange={(e) => setForm((f) => ({ ...f, full_landscape: e.target.value }))}
                rows={4}
                placeholder="Marcus coaches his son's basketball team on Saturdays. He's teaching himself to code..."
                className="w-full p-4 border border-border focus:border-black focus:outline-none text-base leading-relaxed resize-none"
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">
                Production Challenge
              </label>
              <p className="text-xs text-black/40 mb-3">
                Why is this dome hard to build? What makes it interesting?
              </p>
              <textarea
                value={form.production_challenge}
                onChange={(e) => setForm((f) => ({ ...f, production_challenge: e.target.value }))}
                rows={3}
                placeholder="The systems that are supposed to help Marcus actively work against each other..."
                className="w-full p-4 border border-border focus:border-black focus:outline-none text-base leading-relaxed resize-none"
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-3">Disabilities / Conditions</label>
              <div className="flex flex-wrap gap-2">
                {DISABILITY_OPTIONS.map((opt) => (
                  <button
                    key={opt.value}
                    onClick={() => toggleArray('disabilities', opt.value)}
                    className={`px-4 py-2 text-sm border transition-colors cursor-pointer ${
                      form.disabilities.includes(opt.value)
                        ? 'border-black bg-black text-white'
                        : 'border-border hover:border-black/30'
                    }`}
                  >
                    {opt.label}
                  </button>
                ))}
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium mb-3">Housing</label>
              <div className="flex flex-wrap gap-2">
                {HOUSING_OPTIONS.map((opt) => (
                  <button
                    key={opt.value}
                    onClick={() => toggleArray('housing', opt.value)}
                    className={`px-4 py-2 text-sm border transition-colors cursor-pointer ${
                      form.housing.includes(opt.value)
                        ? 'border-black bg-black text-white'
                        : 'border-border hover:border-black/30'
                    }`}
                  >
                    {opt.label}
                  </button>
                ))}
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium mb-3">Income</label>
              <div className="flex flex-wrap gap-2">
                {INCOME_OPTIONS.map((opt) => (
                  <button
                    key={opt.value}
                    onClick={() => toggleArray('income', opt.value)}
                    className={`px-4 py-2 text-sm border transition-colors cursor-pointer ${
                      form.income.includes(opt.value)
                        ? 'border-black bg-black text-white'
                        : 'border-border hover:border-black/30'
                    }`}
                  >
                    {opt.label}
                  </button>
                ))}
              </div>
            </div>

            <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
              {[
                { key: 'veteran', label: 'Veteran' },
                { key: 'dv_survivor', label: 'DV Survivor' },
                { key: 'immigrant', label: 'Immigrant' },
                { key: 'pregnant', label: 'Pregnant' },
              ].map((opt) => (
                <label
                  key={opt.key}
                  className={`flex items-center gap-3 p-3 border cursor-pointer transition-colors ${
                    form[opt.key as keyof CharacterForm]
                      ? 'border-black bg-black/[0.03]'
                      : 'border-border hover:border-black/30'
                  }`}
                >
                  <input
                    type="checkbox"
                    checked={form[opt.key as keyof CharacterForm] as boolean}
                    onChange={(e) => setForm((f) => ({ ...f, [opt.key]: e.target.checked }))}
                    className="accent-black"
                  />
                  <span className="text-sm">{opt.label}</span>
                </label>
              ))}
            </div>
          </div>
        )}

        {/* Step 2: Systems */}
        {step === 2 && (
          <div className="space-y-8">
            <div>
              <label className="block text-sm font-medium mb-2">
                Key Systems
              </label>
              <p className="text-xs text-black/40 mb-4">
                Which government systems does this person interact with?
                Each system is a thread in the dome. More systems = deeper dome.
              </p>
              <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
                {SYSTEM_OPTIONS.map((sys) => (
                  <button
                    key={sys}
                    onClick={() => toggleArray('key_systems', sys)}
                    className={`p-3 text-sm text-left border transition-colors cursor-pointer ${
                      form.key_systems.includes(sys)
                        ? 'border-black bg-black text-white'
                        : 'border-border hover:border-black/30'
                    }`}
                  >
                    {sys}
                  </button>
                ))}
              </div>
              <p className="mt-4 text-sm text-black/30 font-mono">
                {form.key_systems.length} systems selected &middot;
                ~${(form.key_systems.length * 20000).toLocaleString()}/year fragmented cost
              </p>
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">
                What Flourishing Looks Like
              </label>
              <p className="text-xs text-black/40 mb-4">
                For THIS person — what dimensions of flourishing matter most?
              </p>
              <div className="flex flex-wrap gap-2">
                {FLOURISHING_DIMENSIONS.map((dim) => (
                  <button
                    key={dim}
                    onClick={() => toggleArray('flourishing_dimensions', dim)}
                    className={`px-4 py-2 text-sm border transition-colors cursor-pointer ${
                      form.flourishing_dimensions.includes(dim)
                        ? 'border-black bg-black text-white'
                        : 'border-border hover:border-black/30'
                    }`}
                  >
                    {dim}
                  </button>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* Step 3: Production */}
        {step === 3 && (
          <div className="space-y-8">
            <div>
              <label className="block text-sm font-medium mb-3">Dome Tier</label>
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                {TIER_OPTIONS.map((t) => (
                  <label
                    key={t.value}
                    className={`p-6 border cursor-pointer transition-colors ${
                      form.tier === t.value
                        ? 'border-black bg-black text-white'
                        : 'border-border hover:border-black/30'
                    }`}
                  >
                    <input
                      type="radio"
                      name="tier"
                      value={t.value}
                      checked={form.tier === t.value}
                      onChange={() => setForm((f) => ({ ...f, tier: t.value }))}
                      className="sr-only"
                    />
                    <span className="font-mono text-xs tracking-wider block mb-2">{t.label.toUpperCase()}</span>
                    <span className="font-serif text-2xl block mb-3">{t.budget}</span>
                    <span className={`text-sm block ${form.tier === t.value ? 'text-white/50' : 'text-black/40'}`}>
                      {t.team} people &middot; {t.layers} layers
                    </span>
                  </label>
                ))}
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium mb-3">Focus IP Domains</label>
              <p className="text-xs text-black/40 mb-4">
                Which IP domains should the dome prioritize? Leave empty for automatic selection.
              </p>
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-2">
                {IP_DOMAINS.map((d) => (
                  <button
                    key={d.value}
                    onClick={() => toggleArray('focus_domains', d.value)}
                    className={`px-3 py-2 text-sm border transition-colors cursor-pointer ${
                      form.focus_domains.includes(d.value)
                        ? 'border-black bg-black text-white'
                        : 'border-border hover:border-black/30'
                    }`}
                  >
                    {d.label}
                  </button>
                ))}
              </div>
            </div>

            {/* Summary */}
            <div className="bg-[#FAFAFA] p-8 border border-border">
              <h3 className="font-serif text-xl mb-6">Dome Summary</h3>
              <div className="grid grid-cols-2 gap-4 text-sm">
                <div>
                  <p className="text-black/40 mb-1">Character</p>
                  <p className="font-medium">{form.name || '—'}</p>
                </div>
                <div>
                  <p className="text-black/40 mb-1">Source</p>
                  <p className="font-medium">{form.source_type}</p>
                </div>
                <div>
                  <p className="text-black/40 mb-1">Systems</p>
                  <p className="font-medium">{form.key_systems.length} systems</p>
                </div>
                <div>
                  <p className="text-black/40 mb-1">Tier</p>
                  <p className="font-medium capitalize">{form.tier}</p>
                </div>
                <div className="col-span-2">
                  <p className="text-black/40 mb-1">Situation</p>
                  <p className="font-medium">{form.situation?.substring(0, 120) || '—'}...</p>
                </div>
                <div>
                  <p className="text-black/40 mb-1">Est. Fragmented Cost</p>
                  <p className="font-mono">${(form.key_systems.length * 20000).toLocaleString()}/yr</p>
                </div>
                <div>
                  <p className="text-black/40 mb-1">Est. Coordination Savings</p>
                  <p className="font-mono">${(form.key_systems.length * 11000).toLocaleString()}/yr</p>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Navigation */}
        <div className="flex justify-between items-center mt-12 pt-8 border-t border-border">
          <button
            onClick={() => setStep((s) => Math.max(0, s - 1))}
            className={`px-6 py-3 border border-border text-sm font-medium transition-colors ${
              step === 0 ? 'opacity-0 cursor-default' : 'hover:border-black cursor-pointer'
            }`}
            disabled={step === 0}
          >
            Back
          </button>

          {step < 3 ? (
            <button
              onClick={() => setStep((s) => s + 1)}
              disabled={!canProceed}
              className={`px-8 py-3 border-2 text-sm font-medium transition-colors ${
                canProceed
                  ? 'border-black bg-black text-white hover:bg-white hover:text-black cursor-pointer'
                  : 'border-border text-black/30 cursor-not-allowed'
              }`}
            >
              Continue
            </button>
          ) : (
            <button
              onClick={handleGenerate}
              disabled={generating}
              className={`px-10 py-4 border-2 text-lg font-medium transition-colors ${
                generating
                  ? 'border-border text-black/30 cursor-wait'
                  : 'border-black bg-black text-white hover:bg-white hover:text-black cursor-pointer'
              }`}
            >
              {generating ? 'Generating Dome...' : 'Generate Dome'}
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
