import { useState, useEffect } from 'react';
import { fetchApi } from '../api/client';
import { DomainIcon } from '../components/IconMap';
import FlourishingDome from '../components/FlourishingDome';

interface Domain { id: string; name: string; color: string; icon: string; layer: string; description: string; }

interface DomeDomain {
  id: string; name: string; color: string; icon: string; layer: string;
  is_personal_aspiration: boolean; resource_coverage: number;
}
interface DomeResponse {
  dome: {
    title: string; subtitle: string;
    person: { name: string; age: number };
    domain_architecture: {
      foundation_layer: { domains: DomeDomain[] };
      aspiration_layer: { domains: DomeDomain[] };
      transcendence_layer: { domains: DomeDomain[] };
    };
    financial_architecture: { total_annual_value: number };
    vitality_assessment: { composite_score: number; overall_status: string };
    weakest_domain: { name: string; coverage: number; message: string };
    strongest_domain: { name: string; coverage: number; message: string };
    closing_message: string;
  };
}

export default function DomeBuilderPage() {
  const [domains, setDomains] = useState<Domain[]>([]);
  const [name, setName] = useState('');
  const [age, setAge] = useState(30);
  const [location, setLocation] = useState('urban');
  const [aspirations, setAspirations] = useState<Record<string, number>>({});
  const [result, setResult] = useState<DomeResponse | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchApi<Domain[]>('/api/domains').then(d => {
      setDomains(d);
      const init: Record<string, number> = {};
      d.forEach(dom => init[dom.id] = 70);
      setAspirations(init);
    }).catch(() => {});
  }, []);

  async function buildDome() {
    setLoading(true);
    try {
      const aspirationIds = Object.entries(aspirations)
        .filter(([, v]) => v > 50)
        .map(([k]) => k);
      const r = await fetchApi<DomeResponse>('/api/flourishing-dome', {
        method: 'POST',
        body: JSON.stringify({
          name: name || 'You',
          age,
          location,
          environment: location,
          income_level: 'moderate',
          aspirations: aspirationIds,
          values: [],
          health_conditions: [],
        }),
      });
      setResult(r);
    } catch {}
    setLoading(false);
  }

  // Transform backend response to FlourishingDome component format
  const domeData = result ? (() => {
    const arch = result.dome.domain_architecture;
    const allDomains = [
      ...arch.foundation_layer.domains,
      ...arch.aspiration_layer.domains,
      ...arch.transcendence_layer.domains,
    ];
    return allDomains.map(d => ({
      id: d.id,
      name: d.name,
      color: d.color,
      icon: d.icon,
      current: d.resource_coverage,
      potential: d.is_personal_aspiration ? Math.min(100, d.resource_coverage + 30) : d.resource_coverage + 10,
      aspiration: aspirations[d.id] ?? 70,
      gap: 100 - d.resource_coverage,
      resources_available: d.resource_coverage,
    }));
  })() : null;

  const avgCoverage = domeData ? Math.round(domeData.reduce((s, d) => s + d.current, 0) / domeData.length) : 0;
  const avgPotential = domeData ? Math.round(domeData.reduce((s, d) => s + d.potential, 0) / domeData.length) : 0;

  return (
    <div className="max-w-6xl mx-auto px-6 py-16">
      <div className="text-center mb-16">
        <p className="section-label mb-3">Personal Dome Builder</p>
        <h1 className="font-serif text-4xl md:text-5xl text-midnight mb-4">
          What Does Your Flourishing Look Like?
        </h1>
        <p className="font-sans text-base text-midnight/60 max-w-xl mx-auto">
          Not checkboxes of problems. Not a needs assessment. Move each slider to
          express your aspiration — how important is this domain to your vision of a flourishing life?
        </p>
      </div>

      {/* Identity */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
        <div>
          <label className="font-mono text-[10px] tracking-widest uppercase text-midnight/40 mb-2 block">
            This dome belongs to
          </label>
          <input value={name} onChange={e => setName(e.target.value)}
            placeholder="Your name"
            className="w-full border border-midnight/20 px-4 py-3 font-serif text-lg focus:border-gold focus:outline-none bg-transparent" />
        </div>
        <div>
          <label className="font-mono text-[10px] tracking-widest uppercase text-midnight/40 mb-2 block">Age</label>
          <input type="number" value={age} onChange={e => setAge(Number(e.target.value))}
            className="w-full border border-midnight/20 px-4 py-3 font-mono focus:border-gold focus:outline-none bg-transparent" />
        </div>
        <div>
          <label className="font-mono text-[10px] tracking-widest uppercase text-midnight/40 mb-2 block">Location</label>
          <select value={location} onChange={e => setLocation(e.target.value)}
            className="w-full border border-midnight/20 px-4 py-3 font-mono focus:border-gold focus:outline-none bg-transparent appearance-none">
            <option value="urban">Urban</option>
            <option value="suburban">Suburban</option>
            <option value="rural">Rural</option>
          </select>
        </div>
      </div>

      {/* Aspiration Sliders */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-x-12 gap-y-6 mb-12">
        {domains.map(d => (
          <div key={d.id} className="flex items-center gap-4">
            <DomainIcon icon={d.icon} className="w-5 h-5 shrink-0" color={d.color} />
            <div className="flex-1">
              <div className="flex justify-between mb-1">
                <span className="font-serif text-sm">{d.name}</span>
                <span className="font-mono text-xs text-gold">{aspirations[d.id] ?? 70}</span>
              </div>
              <input type="range" min={0} max={100}
                value={aspirations[d.id] ?? 70}
                onChange={e => setAspirations(prev => ({ ...prev, [d.id]: Number(e.target.value) }))}
                className="w-full h-1.5 appearance-none bg-midnight/10 cursor-pointer"
                style={{ accentColor: d.color }} />
            </div>
          </div>
        ))}
      </div>

      {/* Build button */}
      <div className="text-center mb-16">
        <button onClick={buildDome} disabled={loading}
          className="btn-gold disabled:opacity-40 cursor-pointer">
          {loading ? 'Building…' : 'Build My Dome'}
        </button>
      </div>

      {/* Result */}
      {result && domeData && (
        <div>
          <FlourishingDome
            domains={domeData}
            score={avgCoverage}
            potentialScore={avgPotential}
            name={result.dome.person.name}
          />
          <div className="max-w-2xl mx-auto text-center mt-12">
            <div className="flex justify-center gap-12 mb-8">
              <div>
                <p className="font-mono text-[10px] tracking-widest text-midnight/40 mb-1">COVERAGE</p>
                <p className="font-serif text-4xl text-midnight">{avgCoverage}</p>
              </div>
              <div>
                <p className="font-mono text-[10px] tracking-widest text-gold mb-1">GAP</p>
                <p className="font-serif text-4xl text-gold">{100 - avgCoverage}</p>
              </div>
              <div>
                <p className="font-mono text-[10px] tracking-widest text-midnight/40 mb-1">POTENTIAL</p>
                <p className="font-serif text-4xl text-midnight">{avgPotential}</p>
              </div>
            </div>

            {/* Strongest & Weakest */}
            <div className="grid grid-cols-2 gap-6 mb-8">
              <div className="border border-emerald-200 p-4">
                <p className="font-mono text-[10px] tracking-widest text-emerald-600 mb-1">STRONGEST</p>
                <p className="font-serif text-lg">{result.dome.strongest_domain.name}</p>
                <p className="font-mono text-sm text-emerald-600">{result.dome.strongest_domain.coverage}%</p>
              </div>
              <div className="border border-red-200 p-4">
                <p className="font-mono text-[10px] tracking-widest text-red-600 mb-1">MOST VULNERABLE</p>
                <p className="font-serif text-lg">{result.dome.weakest_domain.name}</p>
                <p className="font-mono text-sm text-red-600">{result.dome.weakest_domain.coverage}%</p>
              </div>
            </div>

            <p className="font-serif text-xl italic text-midnight/70 leading-relaxed">
              {result.dome.closing_message}
            </p>
          </div>
        </div>
      )}
    </div>
  );
}
