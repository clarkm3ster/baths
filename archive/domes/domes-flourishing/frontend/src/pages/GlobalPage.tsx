import { useState, useEffect } from 'react';
import { fetchApi } from '../api/client';

interface GlobalModel {
  id: string; name: string; country: string; description: string;
  tax_rate: string; flourishing_score: number; key_insight: string;
}

export default function GlobalPage() {
  const [models, setModels] = useState<GlobalModel[]>([]);

  useEffect(() => {
    fetchApi<{ models: GlobalModel[] }>('/api/finance/global')
      .then(d => setModels((d.models || []).sort((a, b) => b.flourishing_score - a.flourishing_score)))
      .catch(() => {});
  }, []);

  return (
    <div className="max-w-5xl mx-auto px-6 py-20">
      <p className="section-label mb-3">Global Models</p>
      <h1 className="font-serif text-4xl md:text-5xl text-midnight mb-4">
        How Different Societies Build Flourishing
      </h1>
      <p className="font-sans text-base text-midnight/60 max-w-2xl mb-16">
        No nation has built a complete dome. But each has constructed panels that prove it is possible.
      </p>

      <div className="space-y-6">
        {models.map((m, i) => (
          <div key={m.id} className="border border-midnight/10 hover:border-gold transition-colors">
            <div className="p-6 md:flex md:gap-8">
              <div className="md:w-16 shrink-0 mb-4 md:mb-0">
                <span className="font-mono text-3xl font-bold text-gold">#{i + 1}</span>
              </div>
              <div className="flex-1">
                <div className="flex items-baseline gap-3 mb-2">
                  <h3 className="font-serif text-2xl">{m.name}</h3>
                  <span className="font-mono text-xs text-midnight/40">{m.country}</span>
                </div>
                <p className="font-sans text-sm text-midnight/60 mb-4 leading-relaxed">{m.description}</p>

                <div className="flex items-center gap-6 mb-4">
                  <div>
                    <p className="font-mono text-[10px] tracking-widest text-midnight/40 uppercase">Score</p>
                    <div className="flex items-center gap-2">
                      <div className="w-32 h-3 bg-midnight/5">
                        <div className="h-full bg-gold" style={{ width: `${m.flourishing_score}%` }} />
                      </div>
                      <span className="font-mono text-sm font-bold text-gold">{m.flourishing_score}</span>
                    </div>
                  </div>
                  <div>
                    <p className="font-mono text-[10px] tracking-widest text-midnight/40 uppercase">Tax Rate</p>
                    <p className="font-mono text-sm">{m.tax_rate}</p>
                  </div>
                </div>

                <blockquote className="border-l-4 border-gold pl-4">
                  <p className="font-serif italic text-midnight/70">{m.key_insight}</p>
                </blockquote>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
