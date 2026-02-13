import { useState, useEffect } from 'react';
import { fetchApi } from '../api/client';

interface Tradition {
  id: string; name: string; tradition: string; thinker: string; era: string;
  core_idea: string; key_concepts: string[]; implications_for_dome: string; quote: string;
}
interface Synthesis {
  title: string; thesis: string;
  principles: Array<{ name: string; description: string }>;
}

// Each tradition gets a unique color palette — subtle shifts when expanded
const TRADITION_PALETTES: Record<string, { bg: string; border: string; accent: string; glow: string }> = {
  eudaimonia:           { bg: '#FDFBF3', border: '#8B7D3C', accent: '#6B5D1A', glow: 'rgba(139,125,60,0.08)' },
  capability_approach:  { bg: '#F3FBFA', border: '#1A6B6B', accent: '#1A5A5A', glow: 'rgba(26,107,107,0.08)' },
  ubuntu:               { bg: '#FBF5F0', border: '#8B4513', accent: '#6B3410', glow: 'rgba(139,69,19,0.08)' },
  interdependence:      { bg: '#F3FBF5', border: '#2D6B3A', accent: '#1A5A28', glow: 'rgba(45,107,58,0.08)' },
  cura_personalis:      { bg: '#FBF3F5', border: '#6B1A2E', accent: '#5A1025', glow: 'rgba(107,26,46,0.08)' },
  relational_worldview: { bg: '#FBF8F0', border: '#8B6B1A', accent: '#6B5010', glow: 'rgba(139,107,26,0.08)' },
  authentic_existence:  { bg: '#F3F5FB', border: '#1A3D8B', accent: '#102D6B', glow: 'rgba(26,61,139,0.08)' },
  self_actualization:   { bg: '#F8F3FB', border: '#5A1A6B', accent: '#4A105A', glow: 'rgba(90,26,107,0.08)' },
};

const DEFAULT_PALETTE = { bg: '#FEFDFB', border: '#B8860B', accent: '#B8860B', glow: 'transparent' };

export default function PhilosophyPage() {
  const [traditions, setTraditions] = useState<Tradition[]>([]);
  const [synthesis, setSynthesis] = useState<Synthesis | null>(null);
  const [expanded, setExpanded] = useState<string | null>(null);

  useEffect(() => {
    fetchApi<{ traditions: Tradition[]; synthesis: Synthesis }>('/api/philosophy').then(d => {
      setTraditions(d.traditions);
      setSynthesis(d.synthesis);
    }).catch(() => {});
  }, []);

  const activePalette = expanded ? (TRADITION_PALETTES[expanded] || DEFAULT_PALETTE) : DEFAULT_PALETTE;

  return (
    <div style={{
      background: activePalette.bg,
      transition: 'background 0.8s ease',
    }}>
      {/* Hero */}
      {synthesis && (
        <section className="max-w-4xl mx-auto px-6 pt-20 pb-16 text-center">
          <p className="section-label mb-4">Philosophical Foundations</p>
          <h1 className="font-serif text-4xl md:text-5xl text-midnight mb-8">{synthesis.title}</h1>
          <p className="font-serif text-lg text-midnight/70 leading-relaxed">{synthesis.thesis}</p>
          <div className="mt-10 w-24 h-[2px] mx-auto" style={{
            background: activePalette.accent,
            transition: 'background 0.8s ease',
          }} />
        </section>
      )}

      {/* Traditions */}
      <section className="max-w-5xl mx-auto px-6 py-16">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {traditions.map(t => {
            const isOpen = expanded === t.id;
            const palette = TRADITION_PALETTES[t.id] || DEFAULT_PALETTE;
            return (
              <div key={t.id}
                className="border p-6 cursor-pointer"
                style={{
                  borderColor: isOpen ? palette.border : 'rgba(25,25,112,0.1)',
                  background: isOpen ? palette.glow : 'transparent',
                  boxShadow: isOpen ? `0 0 40px ${palette.glow}` : 'none',
                  transition: 'all 0.5s ease',
                }}
                onClick={() => setExpanded(isOpen ? null : t.id)}>
                <div className="flex items-start justify-between mb-3">
                  <div>
                    <h3 className="font-serif text-xl" style={{
                      color: isOpen ? palette.accent : undefined,
                      transition: 'color 0.5s ease',
                    }}>{t.name}</h3>
                    <p className="font-mono text-[10px] tracking-widest text-midnight/40 mt-1">
                      {t.tradition} · {t.thinker} · {t.era}
                    </p>
                  </div>
                  <span className="font-mono text-lg" style={{
                    color: isOpen ? palette.border : '#B8860B',
                    transition: 'color 0.5s ease',
                  }}>{isOpen ? '−' : '+'}</span>
                </div>
                <p className="font-sans text-sm text-midnight/60 leading-relaxed line-clamp-3">
                  {t.core_idea}
                </p>

                {isOpen && (
                  <div className="mt-6 space-y-6 border-t pt-6" style={{ borderColor: `${palette.border}40` }}>
                    <div>
                      <p className="font-mono text-[10px] tracking-widest mb-3" style={{ color: palette.border }}>
                        KEY CONCEPTS
                      </p>
                      <ul className="space-y-2">
                        {t.key_concepts.map((c, i) => (
                          <li key={i} className="flex items-start gap-2 text-sm">
                            <span className="w-1.5 h-1.5 mt-2 shrink-0" style={{ background: palette.border }} />
                            <span className="text-midnight/70">{c}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                    <div>
                      <p className="font-mono text-[10px] tracking-widest mb-3" style={{ color: palette.border }}>
                        IMPLICATIONS FOR THE DOME
                      </p>
                      <p className="font-sans text-sm text-midnight/70 leading-relaxed">{t.implications_for_dome}</p>
                    </div>
                    <blockquote className="border-l-4 pl-6 py-2" style={{ borderColor: palette.border }}>
                      <p className="font-serif text-xl italic text-midnight/80">"{t.quote}"</p>
                      <p className="font-mono text-[10px] tracking-widest text-midnight/40 mt-2">— {t.thinker}</p>
                    </blockquote>
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </section>

      {/* Principles */}
      {synthesis && (
        <section className="bg-midnight-deep text-white py-20 px-6">
          <div className="max-w-5xl mx-auto">
            <p className="section-label text-gold-light mb-4">Six Principles</p>
            <h2 className="font-serif text-3xl mb-12">The Architecture of the Dome</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
              {synthesis.principles.map(p => (
                <div key={p.name} className="border border-white/10 p-6">
                  <h3 className="font-serif text-xl text-gold-light mb-3">{p.name}</h3>
                  <p className="font-sans text-sm text-white/70 leading-relaxed">{p.description}</p>
                </div>
              ))}
            </div>
          </div>
        </section>
      )}
    </div>
  );
}
