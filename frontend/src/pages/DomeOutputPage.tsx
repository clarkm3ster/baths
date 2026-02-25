import { useLocation, Link } from 'react-router-dom';
import { useEffect, useRef, useMemo } from 'react';

interface CharacterData {
  name: string;
  source_type: string;
  source_citation: string;
  situation: string;
  full_landscape: string;
  production_challenge: string;
  age: string;
  gender: string;
  location_city: string;
  location_state: string;
  key_systems: string[];
  flourishing_dimensions: string[];
  disabilities: string[];
  housing: string[];
  income: string[];
  tier: string;
  focus_domains: string[];
  veteran: boolean;
  dv_survivor: boolean;
  immigrant: boolean;
  pregnant: boolean;
}

const LAYERS = [
  { n: 1, name: 'Legal', color: '#1a1a2e' },
  { n: 2, name: 'Systems', color: '#16213e' },
  { n: 3, name: 'Fiscal', color: '#0f3460' },
  { n: 4, name: 'Health', color: '#533483' },
  { n: 5, name: 'Housing', color: '#2d3436' },
  { n: 6, name: 'Economic', color: '#0a3d62' },
  { n: 7, name: 'Education', color: '#0c2461' },
  { n: 8, name: 'Community', color: '#6c5ce7' },
  { n: 9, name: 'Environment', color: '#00b894' },
  { n: 10, name: 'Autonomy', color: '#e17055' },
  { n: 11, name: 'Creativity', color: '#e94560' },
  { n: 12, name: 'Flourishing', color: '#fdcb6e' },
];

function generateIPPortfolio(character: CharacterData) {
  const assets = [
    {
      title: `${character.name}: Documentary Treatment`,
      domain: 'Entertainment',
      format: 'Documentary treatment',
      description: `Feature documentary following ${character.name}'s journey through the dome — every system made visible, every barrier mapped, every coordination moment captured.`,
      layer: 12,
    },
    {
      title: `${character.name}: Series Bible`,
      domain: 'Entertainment',
      format: 'Series bible',
      description: `Limited series adaptation. Each episode follows one dome layer. Episode 1: The person. Episodes 2-10: The AI layers. Episodes 11-13: The human-designed layers.`,
      layer: 11,
    },
    {
      title: 'Whole-Person Digital Twin Platform',
      domain: 'Technology',
      format: 'Software platform',
      description: 'The technical architecture of the dome itself — 12-layer person model, FHIR R4 health integration, SDOH screening, cross-layer query engine, Cosm scoring.',
      layer: 4,
    },
    {
      title: 'Cross-System Coordination Engine',
      domain: 'Technology',
      format: 'Software engine',
      description: `The Layer 2 systems fragmentation analyzer. Maps every government system ${character.name} interacts with, identifies gaps, and generates coordination plans.`,
      layer: 2,
    },
    {
      title: `Dome Bond: ${character.name}`,
      domain: 'Financial Product',
      format: 'Bond prospectus',
      description: 'Social impact bond structured from dome data. Converts measurable coordination savings into investor returns. GO Lab / Social Finance methodology.',
      layer: 3,
    },
    {
      title: `Policy Brief: Coordination Economics`,
      domain: 'Policy',
      format: 'Policy brief',
      description: 'Demonstrates the cost of system fragmentation vs. coordination. Model legislation, fiscal impact analysis, and implementation roadmap.',
      layer: 1,
    },
    {
      title: 'Dome Explorer: Interactive Visualization',
      domain: 'Product',
      format: 'Web application',
      description: 'Interactive experience exploring all 12 layers. Navigate from legal entitlements to health conditions to community connections.',
      layer: 12,
    },
    {
      title: `Whole-Person Coordination: Evidence from ${character.name}'s Dome`,
      domain: 'Research',
      format: 'Academic paper',
      description: 'Documents the dome methodology, cross-layer dynamics, coordination savings, and measurable outcomes.',
      layer: 0,
    },
  ];

  if (character.disabilities.some(d => ['mental_health', 'chronic_illness', 'sud'].includes(d))) {
    assets.push({
      title: 'Cross-System Health Coordination Protocol',
      domain: 'Healthcare',
      format: 'Clinical protocol',
      description: 'Coordinating health care across fragmented systems. FHIR R4 interoperable. Maps health conditions to housing, legal, economic impacts.',
      layer: 4,
    });
  }

  return assets;
}

function generateBudget(character: CharacterData) {
  const complexity = Math.min(character.key_systems.length / 10, 1);
  const tierMin: Record<string, number> = { blockbuster: 1000000, indie: 50000, micro: 5000 };
  const tierMax: Record<string, number> = { blockbuster: 50000000, indie: 250000, micro: 50000 };
  const min = tierMin[character.tier] || 50000;
  const max = tierMax[character.tier] || 250000;
  const total = min + (max - min) * complexity;

  const coordinationSavings = character.key_systems.length * 15000;
  const bondValue = coordinationSavings * 5 * 0.7;
  const ipRevenue = total * 3;
  const totalReturn = ipRevenue + coordinationSavings + bondValue;
  const roi = total > 0 ? Math.round((totalReturn / total) * 100) / 100 : 0;

  return {
    total,
    breakdown: [
      { category: 'Team', pct: 45, amount: total * 0.45 },
      { category: 'Technology', pct: 22, amount: total * 0.22 },
      { category: 'Creative', pct: 13, amount: total * 0.13 },
      { category: 'Data', pct: 12, amount: total * 0.12 },
      { category: 'Legal', pct: 4, amount: total * 0.04 },
      { category: 'Overhead', pct: 4, amount: total * 0.04 },
    ],
    coordinationSavings,
    bondValue,
    ipRevenue,
    totalReturn,
    roi,
  };
}

function generateSimulation(character: CharacterData) {
  const baselineCost = character.key_systems.length * 20000;
  return {
    baselineCosm: 15,
    coordinatedCosm: 72,
    cosmDelta: 57,
    baselineCost,
    coordinatedCost: Math.round(baselineCost * 0.45),
    annualSavings: Math.round(baselineCost * 0.55),
    timeToStability: 18,
  };
}

const TEAM_ROLES: Record<string, Array<{ role: string; desc: string }>> = {
  blockbuster: [
    { role: 'Director', desc: 'Visionary who sees the dome as a complete work' },
    { role: 'Data Architect', desc: '12-layer data architecture, AI agent wiring' },
    { role: 'Narrative Designer', desc: 'Documentary treatment, series bible' },
    { role: 'Systems Analyst', desc: 'Fragmentation mapping, coordination economics' },
    { role: 'Architect', desc: 'Spatial dimension of dome visualization' },
    { role: 'Composer', desc: 'Sonic environment for the world model' },
    { role: 'Health Informaticist', desc: 'FHIR R4, SDOH screening, cross-layer health' },
    { role: 'Material Designer', desc: 'Material palette, physical prototypes' },
    { role: 'Movement Designer', desc: 'Choreographic notation, accessibility pathways' },
    { role: 'Financial Engineer', desc: 'Dome Bond structuring, pay-for-success' },
  ],
  indie: [
    { role: 'Director', desc: 'Visionary who sees the dome as a complete work' },
    { role: 'Data Architect', desc: '12-layer data architecture, AI agent wiring' },
    { role: 'Narrative Designer', desc: 'Documentary treatment, series bible' },
    { role: 'Systems Analyst', desc: 'Fragmentation mapping, coordination economics' },
    { role: 'Architect', desc: 'Spatial dimension of dome visualization' },
    { role: 'Health Informaticist', desc: 'FHIR R4, SDOH screening, cross-layer health' },
  ],
  micro: [
    { role: 'Director', desc: 'Visionary who sees the dome as a complete work' },
    { role: 'Data Architect', desc: '12-layer data architecture, AI agent wiring' },
    { role: 'Narrative Designer', desc: 'Documentary treatment, series bible' },
  ],
};

const PIPELINE_STAGES = [
  { stage: 'Development', days: 44, pct: 22 },
  { stage: 'Pre-Production', days: 35, pct: 17 },
  { stage: 'Production', days: 81, pct: 40 },
  { stage: 'Post-Production', days: 35, pct: 17 },
  { stage: 'Distribution', days: 7, pct: 4 },
];

export function DomeOutputPage() {
  const location = useLocation();
  const character = (location.state as { character?: CharacterData } | null)?.character;
  const sectionsRef = useRef<HTMLElement[]>([]);

  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add('visible');
          }
        });
      },
      { threshold: 0.1 }
    );

    sectionsRef.current.forEach((el) => {
      if (el) observer.observe(el);
    });

    return () => observer.disconnect();
  }, []);

  const addRef = (el: HTMLElement | null, index: number) => {
    if (el) sectionsRef.current[index] = el;
  };

  const ipAssets = useMemo(() => character ? generateIPPortfolio(character) : [], [character]);
  const budget = useMemo(() => character ? generateBudget(character) : null, [character]);
  const simulation = useMemo(() => character ? generateSimulation(character) : null, [character]);
  const team = useMemo(() => TEAM_ROLES[character?.tier || 'indie'] || TEAM_ROLES.indie, [character]);

  if (!character) {
    return (
      <div className="pt-20 min-h-screen flex flex-col items-center justify-center px-6 text-center">
        <h1 className="font-serif text-4xl mb-4">No dome generated</h1>
        <p className="text-black/50 mb-8 max-w-md">
          Run Person-Runner to generate a dome production.
        </p>
        <Link
          to="/run"
          className="inline-block border-2 border-black bg-black text-white px-8 py-4 text-lg font-medium no-underline hover:bg-white hover:text-black transition-colors"
        >
          Run a Dome
        </Link>
      </div>
    );
  }

  return (
    <div>
      {/* ── HERO ────────────────────────────────────────────── */}
      <section className="min-h-screen flex flex-col items-center justify-center relative bg-black text-white overflow-hidden">
        {/* Animated dome SVG */}
        <div className="absolute inset-0 flex items-end justify-center">
          <svg viewBox="0 0 800 400" className="w-full max-w-4xl opacity-15">
            {LAYERS.map((layer, i) => {
              const r = 380 - i * 28;
              return (
                <path
                  key={i}
                  d={`M ${400 - r} 400 A ${r} ${r} 0 0 1 ${400 + r} 400`}
                  fill="none"
                  stroke={layer.color}
                  strokeWidth={layer.n >= 10 ? 4 : 2}
                  className={`layer-reveal layer-delay-${layer.n}`}
                />
              );
            })}
            <circle cx="400" cy="400" r="8" fill="white" className="count-up" />
          </svg>
        </div>

        <div className="relative z-10 text-center px-6 max-w-4xl">
          <p className="text-sm tracking-[0.5em] uppercase text-white/30 mb-4 font-mono">
            {character.tier.toUpperCase()} DOME PRODUCTION
          </p>
          <h1 className="font-serif text-6xl sm:text-8xl leading-[0.9] mb-8">
            DOME:<br />
            <em>{character.name}</em>
          </h1>
          <p className="text-lg text-white/50 max-w-2xl mx-auto mb-8 leading-relaxed">
            {character.situation}
          </p>
          <div className="flex flex-wrap justify-center gap-3 mb-12">
            <span className="text-xs bg-white/10 px-3 py-1 text-white/50 font-mono">
              {character.key_systems.length} systems
            </span>
            <span className="text-xs bg-white/10 px-3 py-1 text-white/50 font-mono">
              {ipAssets.length} IP assets
            </span>
            <span className="text-xs bg-white/10 px-3 py-1 text-white/50 font-mono">
              ${budget?.total.toLocaleString()} budget
            </span>
            <span className="text-xs bg-white/10 px-3 py-1 text-white/50 font-mono">
              {budget?.roi}x ROI
            </span>
          </div>
        </div>
      </section>

      {/* ── THE PERSON ──────────────────────────────────────── */}
      <section
        ref={(el) => addRef(el, 0)}
        className="section-fade py-24 px-6 bg-white"
      >
        <div className="max-w-4xl mx-auto">
          <p className="text-sm tracking-[0.4em] uppercase text-black/40 mb-4">The Person</p>
          <h2 className="font-serif text-4xl mb-8">{character.name}</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-12">
            <div>
              <h3 className="text-sm font-medium text-black/40 uppercase tracking-wider mb-3">Situation</h3>
              <p className="text-lg leading-relaxed text-black/70">{character.situation}</p>
              {character.full_landscape && (
                <>
                  <h3 className="text-sm font-medium text-black/40 uppercase tracking-wider mt-8 mb-3">Full Landscape</h3>
                  <p className="text-lg leading-relaxed text-black/70">{character.full_landscape}</p>
                </>
              )}
              {character.production_challenge && (
                <>
                  <h3 className="text-sm font-medium text-black/40 uppercase tracking-wider mt-8 mb-3">Production Challenge</h3>
                  <p className="text-lg leading-relaxed text-black/70">{character.production_challenge}</p>
                </>
              )}
            </div>
            <div className="space-y-6">
              <div className="bg-[#FAFAFA] p-6">
                <h3 className="text-sm font-medium text-black/40 uppercase tracking-wider mb-3">Profile</h3>
                <div className="space-y-2 text-sm">
                  {character.age && <p><span className="text-black/40">Age:</span> {character.age}</p>}
                  {character.gender && <p><span className="text-black/40">Gender:</span> {character.gender}</p>}
                  {character.location_city && (
                    <p><span className="text-black/40">Location:</span> {character.location_city}{character.location_state ? `, ${character.location_state}` : ''}</p>
                  )}
                  <p><span className="text-black/40">Source:</span> {character.source_type}{character.source_citation ? ` — ${character.source_citation}` : ''}</p>
                </div>
              </div>
              <div className="bg-[#FAFAFA] p-6">
                <h3 className="text-sm font-medium text-black/40 uppercase tracking-wider mb-3">Systems</h3>
                <div className="flex flex-wrap gap-2">
                  {character.key_systems.map((s) => (
                    <span key={s} className="text-xs bg-black text-white px-2 py-1">{s}</span>
                  ))}
                </div>
              </div>
              {character.flourishing_dimensions.length > 0 && (
                <div className="bg-[#FAFAFA] p-6">
                  <h3 className="text-sm font-medium text-black/40 uppercase tracking-wider mb-3">Flourishing</h3>
                  <div className="flex flex-wrap gap-2">
                    {character.flourishing_dimensions.map((d) => (
                      <span key={d} className="text-xs border border-black/20 px-2 py-1">{d}</span>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </section>

      {/* ── 12 LAYERS ────────────────────────────────────────── */}
      <section
        ref={(el) => addRef(el, 1)}
        className="section-fade py-24 px-6 bg-black text-white"
      >
        <div className="max-w-6xl mx-auto">
          <p className="text-sm tracking-[0.4em] uppercase text-white/40 mb-4">Architecture</p>
          <h2 className="font-serif text-4xl mb-16">12 Layers</h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-px bg-white/10">
            {LAYERS.map((layer) => (
              <div
                key={layer.n}
                className={`p-6 layer-reveal layer-delay-${layer.n}`}
                style={{ backgroundColor: layer.n >= 10 ? layer.color : 'black' }}
              >
                <div className="flex items-center gap-3 mb-2">
                  <span className="font-mono text-xs text-white/40">
                    {String(layer.n).padStart(2, '0')}
                  </span>
                  <span className="text-xs tracking-wider uppercase text-white/30">
                    {layer.n >= 10 ? 'HUMAN DESIGN' : 'AI AGENT'}
                  </span>
                </div>
                <h3 className="font-serif text-xl text-white">{layer.name}</h3>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── SIMULATION ──────────────────────────────────────── */}
      {simulation && (
        <section
          ref={(el) => addRef(el, 2)}
          className="section-fade py-24 px-6 bg-white"
        >
          <div className="max-w-4xl mx-auto">
            <p className="text-sm tracking-[0.4em] uppercase text-black/40 mb-4">Simulation</p>
            <h2 className="font-serif text-4xl mb-4">Fragmented vs. Coordinated</h2>
            <p className="text-lg text-black/50 mb-16">
              What happens when {character.key_systems.length} systems coordinate around {character.name}
              instead of operating independently.
            </p>

            <div className="grid grid-cols-1 sm:grid-cols-3 gap-px bg-border mb-12">
              <div className="p-8 bg-[#FAFAFA] text-center">
                <p className="font-mono text-xs text-black/30 mb-2">FRAGMENTED</p>
                <p className="font-serif text-4xl mb-1">${simulation.baselineCost.toLocaleString()}</p>
                <p className="text-sm text-black/40">per year</p>
                <div className="mt-4 h-2 bg-black/10">
                  <div className="h-full bg-black/30" style={{ width: '100%' }} />
                </div>
                <p className="mt-2 font-mono text-sm text-black/40">Cosm: {simulation.baselineCosm}</p>
              </div>
              <div className="p-8 bg-black text-white text-center">
                <p className="font-mono text-xs text-white/30 mb-2">COORDINATED</p>
                <p className="font-serif text-4xl mb-1">${simulation.coordinatedCost.toLocaleString()}</p>
                <p className="text-sm text-white/40">per year</p>
                <div className="mt-4 h-2 bg-white/10">
                  <div className="h-full bg-white/50" style={{ width: '45%' }} />
                </div>
                <p className="mt-2 font-mono text-sm text-white/40">Cosm: {simulation.coordinatedCosm}</p>
              </div>
              <div className="p-8 bg-[#FAFAFA] text-center">
                <p className="font-mono text-xs text-black/30 mb-2">DELTA</p>
                <p className="font-serif text-4xl mb-1">${simulation.annualSavings.toLocaleString()}</p>
                <p className="text-sm text-black/40">saved per year</p>
                <div className="mt-4 h-2 bg-black/10">
                  <div className="h-full bg-green-600" style={{ width: '55%' }} />
                </div>
                <p className="mt-2 font-mono text-sm text-black/40">+{simulation.cosmDelta} Cosm</p>
              </div>
            </div>

            <div className="p-6 bg-[#FAFAFA] text-sm text-black/50 text-center">
              Time to stability: <span className="font-medium text-black">{simulation.timeToStability} months</span>
              &nbsp;&middot;&nbsp;
              55% cost reduction through coordination
              &nbsp;&middot;&nbsp;
              Cosm improvement: {simulation.baselineCosm} → {simulation.coordinatedCosm}
            </div>
          </div>
        </section>
      )}

      {/* ── IP PORTFOLIO ────────────────────────────────────── */}
      <section
        ref={(el) => addRef(el, 3)}
        className="section-fade py-24 px-6 bg-[#FAFAFA]"
      >
        <div className="max-w-6xl mx-auto">
          <p className="text-sm tracking-[0.4em] uppercase text-black/40 mb-4">IP Portfolio</p>
          <h2 className="font-serif text-4xl mb-4">{ipAssets.length} IP Assets</h2>
          <p className="text-lg text-black/50 mb-16">
            Generated across {new Set(ipAssets.map(a => a.domain)).size} domains
            from {character.name}'s dome production.
          </p>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-px bg-border">
            {ipAssets.map((asset, i) => (
              <div key={i} className="p-6 bg-white">
                <div className="flex items-center gap-3 mb-2">
                  <span className="text-xs bg-black/5 px-2 py-0.5 text-black/40 font-mono">
                    {asset.domain}
                  </span>
                  <span className="text-xs text-black/30">Layer {asset.layer}</span>
                </div>
                <h3 className="font-serif text-lg mb-2">{asset.title}</h3>
                <p className="text-sm text-black/50 leading-relaxed mb-2">{asset.description}</p>
                <p className="text-xs text-black/30 font-mono">{asset.format}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── BUSINESS CASE ───────────────────────────────────── */}
      {budget && (
        <section
          ref={(el) => addRef(el, 4)}
          className="section-fade py-24 px-6 bg-black text-white"
        >
          <div className="max-w-5xl mx-auto">
            <p className="text-sm tracking-[0.4em] uppercase text-white/40 mb-4">Business Case</p>
            <h2 className="font-serif text-4xl mb-16">The Investment</h2>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-16">
              <div>
                <h3 className="font-serif text-2xl mb-8">Budget Breakdown</h3>
                <div className="space-y-4">
                  {budget.breakdown.map((line) => (
                    <div key={line.category}>
                      <div className="flex justify-between text-sm mb-1">
                        <span>{line.category}</span>
                        <span className="font-mono text-white/50">${Math.round(line.amount).toLocaleString()}</span>
                      </div>
                      <div className="h-1.5 bg-white/10">
                        <div className="h-full bg-white/40" style={{ width: `${line.pct}%` }} />
                      </div>
                    </div>
                  ))}
                </div>
                <div className="mt-8 pt-4 border-t border-white/10 flex justify-between">
                  <span className="font-medium">Total Budget</span>
                  <span className="font-serif text-2xl">${Math.round(budget.total).toLocaleString()}</span>
                </div>
              </div>

              <div>
                <h3 className="font-serif text-2xl mb-8">Projected Returns</h3>
                <div className="space-y-6">
                  <div className="p-6 bg-white/5">
                    <p className="text-sm text-white/40 mb-1">IP Revenue</p>
                    <p className="font-serif text-2xl">${Math.round(budget.ipRevenue).toLocaleString()}</p>
                  </div>
                  <div className="p-6 bg-white/5">
                    <p className="text-sm text-white/40 mb-1">Annual Coordination Savings</p>
                    <p className="font-serif text-2xl">${budget.coordinationSavings.toLocaleString()}/yr</p>
                  </div>
                  <div className="p-6 bg-white/5">
                    <p className="text-sm text-white/40 mb-1">Dome Bond Value</p>
                    <p className="font-serif text-2xl">${Math.round(budget.bondValue).toLocaleString()}</p>
                  </div>
                  <div className="p-6 bg-white/10">
                    <p className="text-sm text-white/40 mb-1">Total Projected Return</p>
                    <p className="font-serif text-3xl">${Math.round(budget.totalReturn).toLocaleString()}</p>
                    <p className="text-sm text-white/40 mt-1 font-mono">{budget.roi}x multiple</p>
                  </div>
                </div>
              </div>
            </div>

            <div className="mt-16 p-8 bg-white/5">
              <h3 className="font-serif text-xl mb-4">Investment Thesis</h3>
              <p className="text-lg text-white/60 leading-relaxed">
                Invest ${Math.round(budget.total).toLocaleString()} in a {character.tier} dome production
                for {character.name}. The dome generates {ipAssets.length} IP assets
                across {new Set(ipAssets.map(a => a.domain)).size} domains. Projected coordination savings
                of ${budget.coordinationSavings.toLocaleString()}/year across{' '}
                {character.key_systems.length} systems create a Dome Bond worth{' '}
                ${Math.round(budget.bondValue).toLocaleString()}. Total projected return:{' '}
                ${Math.round(budget.totalReturn).toLocaleString()} ({budget.roi}x multiple).
              </p>
            </div>
          </div>
        </section>
      )}

      {/* ── TEAM ────────────────────────────────────────────── */}
      <section
        ref={(el) => addRef(el, 5)}
        className="section-fade py-24 px-6 bg-white"
      >
        <div className="max-w-5xl mx-auto">
          <p className="text-sm tracking-[0.4em] uppercase text-black/40 mb-4">Team</p>
          <h2 className="font-serif text-4xl mb-4">The team the dome assembles</h2>
          <p className="text-lg text-black/50 mb-16">
            {team.length} roles across {new Set(team.map(t => t.role)).size} disciplines.
          </p>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-px bg-border">
            {team.map((member) => (
              <div key={member.role} className="p-6 bg-[#FAFAFA]">
                <h3 className="font-serif text-lg mb-2">{member.role}</h3>
                <p className="text-sm text-black/50 leading-relaxed">{member.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── PRODUCTION TIMELINE ─────────────────────────────── */}
      <section
        ref={(el) => addRef(el, 6)}
        className="section-fade py-24 px-6 bg-[#FAFAFA]"
      >
        <div className="max-w-4xl mx-auto">
          <p className="text-sm tracking-[0.4em] uppercase text-black/40 mb-4">Pipeline</p>
          <h2 className="font-serif text-4xl mb-4">Production Timeline</h2>
          <p className="text-lg text-black/50 mb-16">
            {PIPELINE_STAGES.reduce((a, s) => a + s.days, 0)} days from character to complete dome.
          </p>

          <div className="space-y-4">
            {PIPELINE_STAGES.map((stage) => (
              <div key={stage.stage} className="flex items-center gap-4">
                <div className="w-36 text-right">
                  <p className="font-serif text-sm">{stage.stage}</p>
                  <p className="font-mono text-xs text-black/30">{stage.days}d</p>
                </div>
                <div className="flex-1 h-10 bg-white border border-border relative">
                  <div
                    className="absolute inset-y-0 left-0 bg-black flex items-center px-3"
                    style={{ width: `${stage.pct}%` }}
                  >
                    <span className="text-xs text-white font-mono">{stage.pct}%</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── TECH INNOVATIONS ──────────────────────────────────── */}
      <section
        ref={(el) => addRef(el, 7)}
        className="section-fade py-24 px-6 bg-black text-white"
      >
        <div className="max-w-5xl mx-auto">
          <p className="text-sm tracking-[0.4em] uppercase text-white/40 mb-4">Technology</p>
          <h2 className="font-serif text-4xl mb-16">Tech Innovations</h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {[
              { title: 'Person-Runner Engine', desc: 'AI engine generating complete dome productions from character + circumstances.' },
              { title: 'Cross-Layer Query Engine', desc: 'Answers questions across all 12 dome layers simultaneously.' },
              { title: 'Cosm Scoring System', desc: 'Auditable scoring where every number has a source.' },
              { title: 'FHIR R4 Bridge', desc: 'Bidirectional bridge between health data and dome layers.' },
              { title: 'SDOH Mapping', desc: 'PRAPARE and AHC-HRSN screening instruments mapped to dome.' },
              { title: 'Dome Bond Engine', desc: 'Social impact bond prospectuses computed from dome data.' },
            ].map((t) => (
              <div key={t.title} className="border border-white/10 p-6">
                <h3 className="font-serif text-lg mb-2">{t.title}</h3>
                <p className="text-sm text-white/40 leading-relaxed">{t.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── DATA SOURCES ────────────────────────────────────── */}
      <section
        ref={(el) => addRef(el, 8)}
        className="section-fade py-24 px-6 bg-white"
      >
        <div className="max-w-4xl mx-auto text-center">
          <p className="text-sm tracking-[0.4em] uppercase text-black/40 mb-4">Data</p>
          <h2 className="font-serif text-4xl mb-8">Data Sources</h2>
          <div className="flex flex-wrap justify-center gap-3 text-sm text-black/40">
            {[
              'US Census ACS', 'BLS', 'HUD FMR', 'FEMA', 'EPA AirNow',
              'USDA Food Access', 'FHIR R4', 'PRAPARE', 'AHC-HRSN',
              'ICD-10-CM', 'LOINC', 'GO Lab', 'Social Finance',
            ].map((src) => (
              <span key={src} className="px-4 py-2 bg-[#FAFAFA] border border-border">{src}</span>
            ))}
          </div>
          <p className="mt-8 text-sm text-black/30">
            28 priority US counties &middot; 5x daily auto-scraping &middot; Fragment + Cosm data agents
          </p>
        </div>
      </section>

      {/* ── CTA ──────────────────────────────────────────────── */}
      <section className="py-24 px-6 bg-black text-white text-center">
        <div className="max-w-3xl mx-auto">
          <h2 className="font-serif text-4xl sm:text-5xl mb-8">
            This is {character.name}'s dome.
          </h2>
          <p className="text-lg text-white/40 mb-12">
            {ipAssets.length} IP assets &middot; ${Math.round(budget?.total || 0).toLocaleString()} budget
            &middot; {budget?.roi}x projected ROI &middot; {character.key_systems.length} systems coordinated
          </p>
          <Link
            to="/run"
            className="inline-block border-2 border-white bg-white text-black px-10 py-4 text-lg font-medium no-underline hover:bg-transparent hover:text-white transition-colors"
          >
            Run Another Dome
          </Link>
        </div>
      </section>
    </div>
  );
}
