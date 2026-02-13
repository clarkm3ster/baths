import { useState, useEffect } from 'react';
import { fetchApi } from '../api/client';
import { AlertTriangle, Lightbulb } from 'lucide-react';

interface CultureDomain {
  id: string; name: string; description: string;
  public_infrastructure: string; community_infrastructure: string; what_flourishing_requires: string;
}
interface CultureAsset { count: number; description: string; distribution_equity: number; }
interface CultureDesert {
  id: string; name: string; description: string; affected_population: string;
  indicators: string[]; interventions: string[];
}

function eqColor(s: number) { return s >= 70 ? '#1A6B3C' : s >= 40 ? '#B8860B' : '#8B1A1A'; }

export default function CulturePage() {
  const [domains, setDomains] = useState<CultureDomain[]>([]);
  const [assets, setAssets] = useState<Record<string, CultureAsset>>({});
  const [deserts, setDeserts] = useState<CultureDesert[]>([]);

  useEffect(() => {
    fetchApi<CultureDomain[]>('/api/culture/domains').then(setDomains).catch(() => {});
    fetchApi<{ assets: Record<string, CultureAsset> }>('/api/culture/assets').then(d => setAssets(d.assets || {})).catch(() => {});
    fetchApi<CultureDesert[]>('/api/culture/deserts').then(setDeserts).catch(() => {});
  }, []);

  return (
    <div>
      {/* Hero */}
      <section className="max-w-5xl mx-auto px-6 py-20">
        <p className="section-label mb-3">Creative Infrastructure</p>
        <h1 className="font-serif text-4xl md:text-6xl text-midnight mb-6">The Creative Dome</h1>
        <p className="font-serif text-xl text-midnight/60 max-w-3xl leading-relaxed">
          Art, design, music, literature, and creative practice are not luxuries appended to life
          after the "real" needs are met. They are essential infrastructure for human flourishing.
        </p>
      </section>

      {/* Domains */}
      <section className="max-w-5xl mx-auto px-6 pb-16">
        <p className="section-label mb-6">Creative Domains</p>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-0">
          {domains.map((d, i) => (
            <div key={d.id} className={`p-6 border border-midnight/10 ${i % 2 === 0 ? 'md:border-r-0' : ''}`}>
              <h3 className="font-serif text-xl mb-3">{d.name}</h3>
              <p className="font-sans text-sm text-midnight/60 mb-4 leading-relaxed">{d.description}</p>
              <div className="space-y-3 text-sm">
                <div>
                  <p className="font-mono text-[10px] tracking-widest text-gold uppercase mb-1">Public Infrastructure</p>
                  <p className="text-midnight/70">{d.public_infrastructure}</p>
                </div>
                <div>
                  <p className="font-mono text-[10px] tracking-widest text-gold uppercase mb-1">Community Infrastructure</p>
                  <p className="text-midnight/70">{d.community_infrastructure}</p>
                </div>
                <div className="border-t border-midnight/10 pt-3">
                  <p className="font-serif italic text-midnight/80">{d.what_flourishing_requires}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Assets */}
      <section className="max-w-5xl mx-auto px-6 pb-16">
        <p className="section-label mb-6">What Exists Today</p>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {Object.entries(assets).map(([key, a]) => (
            <div key={key} className="border border-midnight/10 p-5">
              <div className="flex justify-between items-baseline mb-2">
                <h3 className="font-serif text-base capitalize">{key.replace(/_/g, ' ')}</h3>
                <span className="font-mono text-xl font-bold text-midnight">{a.count.toLocaleString()}</span>
              </div>
              <p className="font-sans text-sm text-midnight/50 mb-4">{a.description}</p>
              <div>
                <div className="flex justify-between text-[10px] font-mono mb-1">
                  <span className="tracking-widest text-midnight/40 uppercase">Equity</span>
                  <span style={{ color: eqColor(a.distribution_equity) }}>{a.distribution_equity}%</span>
                </div>
                <div className="h-2 bg-midnight/5">
                  <div className="h-full" style={{ width: `${a.distribution_equity}%`, background: eqColor(a.distribution_equity) }} />
                </div>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Deserts */}
      <section className="max-w-5xl mx-auto px-6 pb-20">
        <p className="section-label mb-6">What Is Missing</p>
        {deserts.map(d => (
          <div key={d.id} className="border border-midnight/10 p-6 mb-4 md:grid md:grid-cols-3 md:gap-8">
            <div>
              <div className="flex items-center gap-2 mb-2">
                <AlertTriangle className="w-4 h-4 text-gold" />
                <h3 className="font-serif text-xl">{d.name}</h3>
              </div>
              <p className="font-sans text-sm text-midnight/60 mb-3">{d.description}</p>
              <p className="font-mono text-[10px] tracking-widest text-midnight/40 uppercase">{d.affected_population}</p>
            </div>
            <div>
              <p className="font-mono text-[10px] tracking-widest text-midnight/40 uppercase mb-2 mt-4 md:mt-0">Indicators</p>
              <ul className="space-y-1">{d.indicators.map((ind, i) => (
                <li key={i} className="flex items-start gap-2 text-sm"><span className="w-1.5 h-1.5 bg-gold mt-1.5 shrink-0" />{ind}</li>
              ))}</ul>
            </div>
            <div>
              <p className="font-mono text-[10px] tracking-widest text-midnight/40 uppercase mb-2 mt-4 md:mt-0">Interventions</p>
              <ul className="space-y-1">{d.interventions.map((int_, i) => (
                <li key={i} className="flex items-start gap-2 text-sm"><Lightbulb className="w-3 h-3 text-gold mt-1 shrink-0" />{int_}</li>
              ))}</ul>
            </div>
          </div>
        ))}
      </section>
    </div>
  );
}
