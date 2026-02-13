import { useState, useEffect } from 'react';
import { fetchApi } from '../api/client';
import { ChevronDown, ChevronUp } from 'lucide-react';

interface Nation {
  name: string; score: number; population: string;
  strengths: string[]; gaps: string[]; insight: string;
}
interface IndexData {
  title: string; description: string; methodology: string;
  nations: Nation[]; maximum_possible: number; current_global_average: number; message: string;
}

export default function FlourishingIndexPage() {
  const [data, setData] = useState<IndexData | null>(null);
  const [expanded, setExpanded] = useState<string | null>(null);

  useEffect(() => {
    fetchApi<IndexData>('/api/flourishing-index').then(setData).catch(() => {});
  }, []);

  if (!data) return (
    <div className="min-h-[60vh] flex items-center justify-center">
      <p className="font-serif text-xl text-midnight/40 animate-pulse">Loading…</p>
    </div>
  );

  return (
    <div className="max-w-5xl mx-auto px-6 py-20">
      <p className="section-label mb-3">{data.title}</p>
      <h1 className="font-serif text-4xl md:text-5xl text-midnight mb-4">
        Measuring What Matters
      </h1>
      <p className="font-sans text-base text-midnight/60 max-w-2xl mb-4">
        {data.description}
      </p>
      <p className="font-sans text-sm text-midnight/40 max-w-2xl mb-12">
        <span className="font-mono text-[10px] tracking-widest uppercase">Methodology: </span>
        {data.methodology}
      </p>

      {/* Global average indicator */}
      <div className="border border-midnight/10 p-6 mb-12">
        <div className="flex items-center justify-between mb-4">
          <div>
            <p className="font-mono text-[10px] tracking-widest text-midnight/40 uppercase">Global Average</p>
            <p className="font-serif text-4xl text-midnight">{data.current_global_average}<span className="text-lg text-midnight/30">/{data.maximum_possible}</span></p>
          </div>
          <div className="text-right">
            <p className="font-mono text-[10px] tracking-widest text-midnight/40 uppercase">Gap to What's Possible</p>
            <p className="font-serif text-4xl text-gold">{data.maximum_possible - data.current_global_average}</p>
          </div>
        </div>
        <div className="h-3 bg-midnight/5 relative">
          <div className="h-full bg-midnight/20 absolute left-0" style={{ width: `${data.current_global_average}%` }} />
          <div className="h-full bg-gold/30 absolute" style={{ left: `${data.current_global_average}%`, width: `${data.maximum_possible - data.current_global_average}%` }} />
        </div>
      </div>

      {/* Nations */}
      <div className="space-y-4">
        {data.nations.map((n, i) => {
          const isGolden = n.name === "What's Possible";
          const isExp = expanded === n.name;
          return (
            <div key={n.name}
              className={`border transition-colors ${
                isGolden ? 'border-gold border-2' : 'border-midnight/10 hover:border-gold'
              }`}>
              <div className="p-5 cursor-pointer flex items-center gap-6"
                onClick={() => setExpanded(isExp ? null : n.name)}>
                <span className="font-mono text-2xl font-bold text-gold w-10">{i + 1}</span>
                <div className="flex-1 min-w-0">
                  <div className="flex items-baseline gap-3 mb-2">
                    <h3 className={`font-serif text-xl ${isGolden ? 'text-gold' : ''}`}>{n.name}</h3>
                    <span className="font-mono text-[10px] text-midnight/40">{n.population}</span>
                  </div>
                  {/* Score bar */}
                  <div className="h-3 bg-midnight/5 relative">
                    <div className="h-full transition-all" style={{
                      width: `${n.score}%`,
                      background: isGolden ? '#B8860B' : `hsl(${40 + (n.score - 60) * 2}, 60%, 40%)`
                    }} />
                  </div>
                </div>
                <span className={`font-serif text-3xl font-bold ${isGolden ? 'text-gold' : 'text-midnight'}`}>{n.score}</span>
                {isExp ? <ChevronUp className="w-4 h-4 text-midnight/30" /> : <ChevronDown className="w-4 h-4 text-midnight/30" />}
              </div>

              {isExp && (
                <div className="border-t border-midnight/10 p-6 bg-parchment">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-6">
                    <div>
                      <p className="font-mono text-[10px] tracking-widest text-gold uppercase mb-3">Strengths</p>
                      <ul className="space-y-2">
                        {n.strengths.map((s, j) => (
                          <li key={j} className="flex items-start gap-2 text-sm">
                            <span className="w-1.5 h-1.5 bg-emerald-600 mt-1.5 shrink-0" />
                            <span className="text-midnight/70">{s}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                    <div>
                      <p className="font-mono text-[10px] tracking-widest text-gold uppercase mb-3">Gaps</p>
                      <ul className="space-y-2">
                        {n.gaps.map((g, j) => (
                          <li key={j} className="flex items-start gap-2 text-sm">
                            <span className="w-1.5 h-1.5 bg-red-600 mt-1.5 shrink-0" />
                            <span className="text-midnight/70">{g}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  </div>
                  <blockquote className="border-l-4 border-gold pl-4">
                    <p className="font-serif italic text-midnight/70 leading-relaxed">{n.insight}</p>
                  </blockquote>
                </div>
              )}
            </div>
          );
        })}
      </div>

      {/* Closing message */}
      <div className="mt-16 border-t border-midnight/10 pt-12 text-center max-w-3xl mx-auto">
        <p className="font-serif text-xl text-midnight/70 leading-relaxed italic">
          {data.message}
        </p>
      </div>
    </div>
  );
}
