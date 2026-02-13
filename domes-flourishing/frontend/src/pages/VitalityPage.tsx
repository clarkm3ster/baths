import { useState, useEffect } from 'react';
import { fetchApi } from '../api/client';

interface VitalityDomain {
  id: string; name: string; percentage_of_health_outcomes: number;
  description: string; infrastructure_needed: string[]; current_gaps: string[];
}
interface VitalityResult {
  domain_assessments: Array<{ domain_id: string; domain_name: string; score: number; status: string; recommendation: string }>;
  composite_score: number; overall_message: string; overall_status: string;
  top_priority: string; greatest_strength: string;
}

export default function VitalityPage() {
  const [domains, setDomains] = useState<VitalityDomain[]>([]);
  const [age, setAge] = useState(35);
  const [env, setEnv] = useState('urban');
  const [result, setResult] = useState<VitalityResult | null>(null);

  useEffect(() => {
    fetchApi<{ domains: VitalityDomain[] }>('/api/vitality/domains').then(d => setDomains(d.domains || [])).catch(() => {});
  }, []);

  async function build() {
    const r = await fetchApi<VitalityResult>('/api/vitality/personal-dome', {
      method: 'POST', body: JSON.stringify({ age, priorities: [], conditions: [], environment: env }),
    });
    setResult(r);
  }

  return (
    <div>
      {/* Hero */}
      <section className="max-w-5xl mx-auto px-6 py-20">
        <p className="section-label mb-3">Health Beyond Clinical Care</p>
        <h1 className="font-serif text-4xl md:text-6xl text-midnight mb-6">The Vitality Dome</h1>
        <p className="font-serif text-xl text-midnight/60 max-w-3xl leading-relaxed">
          Clinical care accounts for only 20% of health outcomes. The other 80%
          is social determinants, environment, behavior, relationships, and purpose.
        </p>
      </section>

      {/* Outcome breakdown */}
      <section className="max-w-5xl mx-auto px-6 pb-12">
        <p className="section-label mb-4">Health Outcome Contributions</p>
        <div className="flex gap-0.5 h-8 mb-4">
          {domains.map(d => (
            <div key={d.id} className="relative group" style={{ flex: d.percentage_of_health_outcomes }}
              title={`${d.name}: ${d.percentage_of_health_outcomes}%`}>
              <div className="h-full" style={{ background: `hsl(${120 + domains.indexOf(d) * 30}, 40%, 40%)` }} />
              <div className="absolute -top-8 left-1/2 -translate-x-1/2 hidden group-hover:block bg-midnight text-white px-2 py-1 text-[10px] font-mono whitespace-nowrap z-10">
                {d.name}: {d.percentage_of_health_outcomes}%
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Domain cards */}
      <section className="max-w-5xl mx-auto px-6 pb-16">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {domains.map(d => (
            <div key={d.id} className="border border-midnight/10 p-5">
              <div className="flex justify-between items-baseline mb-2">
                <h3 className="font-serif text-lg">{d.name}</h3>
                <span className="font-mono text-lg font-bold text-gold">{d.percentage_of_health_outcomes}%</span>
              </div>
              <p className="font-sans text-sm text-midnight/60 mb-4 leading-relaxed">{d.description}</p>
              <div className="mb-3">
                <p className="font-mono text-[10px] tracking-widest text-midnight/40 mb-1 uppercase">Infrastructure Needed</p>
                <ul className="space-y-1">{d.infrastructure_needed.map((item, i) => (
                  <li key={i} className="text-sm flex items-start gap-2">
                    <span className="w-1 h-1 bg-gold mt-2 shrink-0" /><span className="text-midnight/60">{item}</span>
                  </li>
                ))}</ul>
              </div>
              <div>
                <p className="font-mono text-[10px] tracking-widest text-midnight/40 mb-1 uppercase">Current Gaps</p>
                <ul className="space-y-1">{d.current_gaps.map((item, i) => (
                  <li key={i} className="text-sm flex items-start gap-2">
                    <span className="w-1 h-1 bg-red-600 mt-2 shrink-0" /><span className="text-midnight/50">{item}</span>
                  </li>
                ))}</ul>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Personal builder */}
      <section className="max-w-5xl mx-auto px-6 pb-20">
        <p className="section-label mb-6">Personal Vitality Assessment</p>
        <div className="border border-midnight/10 p-6 max-w-md mb-6">
          <div className="grid grid-cols-2 gap-4 mb-4">
            <div>
              <label className="font-mono text-[10px] tracking-widest text-midnight/40 mb-1 block uppercase">Age</label>
              <input type="number" value={age} onChange={e => setAge(+e.target.value)}
                className="w-full border border-midnight/20 px-3 py-2 font-mono text-sm focus:border-gold focus:outline-none bg-transparent" />
            </div>
            <div>
              <label className="font-mono text-[10px] tracking-widest text-midnight/40 mb-1 block uppercase">Environment</label>
              <select value={env} onChange={e => setEnv(e.target.value)}
                className="w-full border border-midnight/20 px-3 py-2 font-mono text-sm focus:border-gold focus:outline-none bg-transparent appearance-none">
                <option value="urban">Urban</option><option value="suburban">Suburban</option><option value="rural">Rural</option>
              </select>
            </div>
          </div>
          <button onClick={build} className="btn-gold cursor-pointer">Assess My Vitality</button>
        </div>

        {result && (
          <div className="border border-gold p-6">
            <div className="flex justify-between items-start mb-6">
              <p className="section-label">Vitality Assessment</p>
              <p className="font-serif text-3xl text-gold">{result.composite_score}<span className="text-sm text-midnight/40">/100</span></p>
            </div>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3 mb-6">
              {result.domain_assessments.map(d => (
                <div key={d.domain_id} className="border border-midnight/10 p-3">
                  <div className="flex justify-between mb-1">
                    <span className="font-serif text-sm">{d.domain_name}</span>
                    <span className="font-mono text-sm text-gold">{d.score}</span>
                  </div>
                  <div className="h-1.5 bg-midnight/5"><div className="h-full bg-gold" style={{ width: `${d.score}%` }} /></div>
                  <p className="font-sans text-[11px] text-midnight/50 mt-2">{d.recommendation}</p>
                </div>
              ))}
            </div>
            <p className="font-serif italic text-midnight/60">{result.overall_message}</p>
          </div>
        )}
      </section>
    </div>
  );
}
