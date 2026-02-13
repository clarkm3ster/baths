import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { fetchApi } from '../api/client';
import { DomainIcon } from '../components/IconMap';
import { ArrowRight } from 'lucide-react';

interface Domain {
  id: string; name: string; color: string; icon: string;
  layer: string; description: string;
}

interface PhilosophyData {
  traditions: Array<{ quote: string; thinker: string; name: string }>;
  synthesis: { title: string; thesis: string };
}

export default function LandingPage() {
  const [domains, setDomains] = useState<Domain[]>([]);
  const [philosophy, setPhilosophy] = useState<PhilosophyData | null>(null);
  const [quoteIdx, setQuoteIdx] = useState(0);
  const [entered, setEntered] = useState(false);
  const [fadeIn, setFadeIn] = useState(false);

  useEffect(() => {
    fetchApi<Domain[]>('/api/domains').then(setDomains).catch(() => {});
    fetchApi<PhilosophyData>('/api/philosophy').then(setPhilosophy).catch(() => {});
  }, []);

  useEffect(() => {
    if (!philosophy) return;
    const t = setInterval(() => setQuoteIdx(i => (i + 1) % philosophy.traditions.length), 6000);
    return () => clearInterval(t);
  }, [philosophy]);

  function handleEnter() {
    setEntered(true);
    // Small delay to let the gateway fade out, then fade in the content
    setTimeout(() => setFadeIn(true), 400);
  }

  const layers = ['foundation', 'aspiration', 'transcendence'];

  return (
    <div>
      {/* GATEWAY — pure minimal screen */}
      <div
        className="fixed inset-0 z-50 flex flex-col justify-center items-center text-center px-8 bg-warm-white"
        style={{
          opacity: entered ? 0 : 1,
          pointerEvents: entered ? 'none' : 'auto',
          transition: 'opacity 0.8s ease',
        }}
      >
        <h1 className="font-serif text-4xl sm:text-5xl md:text-7xl lg:text-8xl leading-[0.95] text-midnight max-w-5xl">
          You are not a case.<br />
          You are not a client.<br />
          <span className="text-gold">You are the reason<br />civilization exists.</span>
        </h1>
        <div className="mt-16">
          <button
            onClick={handleEnter}
            className="btn-gold px-12 py-5 text-sm cursor-pointer"
          >
            Enter
          </button>
        </div>
      </div>

      {/* FULL LANDING — revealed after Enter */}
      <div style={{
        opacity: fadeIn ? 1 : 0,
        transform: fadeIn ? 'translateY(0)' : 'translateY(20px)',
        transition: 'opacity 1s ease 0.2s, transform 1s ease 0.2s',
      }}>
        {/* HERO (revealed version) */}
        <section className="min-h-[70vh] flex flex-col justify-center items-center text-center px-8 pt-12">
          <p className="section-label mb-6">The Architecture of Human Flourishing</p>
          <h2 className="font-serif text-3xl md:text-5xl text-midnight max-w-4xl mb-8 leading-tight">
            Every institution, every resource, every policy — they exist for one purpose:
            <span className="text-gold"> to build the conditions for your flourishing.</span>
          </h2>
          <p className="font-serif text-lg text-midnight/50 max-w-2xl leading-relaxed mb-12">
            Government is just the foundation. Above it rise the twelve domains
            that make a life worth living. Not a safety net — a cathedral.
          </p>
          <Link to="/dome-builder" className="btn-gold flex items-center gap-2">
            Build Your Dome <ArrowRight className="w-4 h-4" />
          </Link>
          <div className="mt-16 w-24 h-[2px] bg-gold" />
        </section>

        {/* DOMAINS GRID */}
        <section className="max-w-6xl mx-auto px-6 py-20">
          <p className="section-label mb-3">The Twelve Domains</p>
          <h2 className="font-serif text-3xl md:text-4xl text-midnight mb-4">
            Government is the foundation — necessary but not sufficient.
          </h2>
          <p className="font-sans text-base text-midnight/60 max-w-2xl mb-16">
            Above it rise the domains that make a life worth living. Twelve dimensions
            of human flourishing, organized in three ascending layers.
          </p>

          {layers.map(layer => {
            const layerDomains = domains.filter(d => d.layer === layer);
            if (!layerDomains.length) return null;
            return (
              <div key={layer} className="mb-16">
                <div className="flex items-center gap-4 mb-6">
                  <span className="font-mono text-[10px] tracking-[0.3em] uppercase text-gold">
                    {layer}
                  </span>
                  <div className="flex-1 h-px bg-gold/20" />
                </div>
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-0">
                  {layerDomains.map(d => (
                    <Link
                      key={d.id}
                      to={`/domains/${d.id}`}
                      className="group border border-midnight/8 p-6 hover:border-gold transition-colors"
                    >
                      <div className="flex items-center gap-3 mb-3">
                        <DomainIcon icon={d.icon} className="w-5 h-5" color={d.color} />
                        <h3 className="font-serif text-lg group-hover:text-gold transition-colors">
                          {d.name}
                        </h3>
                      </div>
                      <p className="font-sans text-sm text-midnight/50 leading-relaxed line-clamp-3">
                        {d.description}
                      </p>
                    </Link>
                  ))}
                </div>
              </div>
            );
          })}
        </section>

        {/* PHILOSOPHY QUOTES */}
        {philosophy && (
          <section className="bg-midnight-deep text-white py-24 px-8">
            <div className="max-w-3xl mx-auto text-center">
              <p className="section-label text-gold-light mb-8">Philosophical Foundations</p>
              <blockquote className="font-serif text-2xl md:text-3xl italic leading-relaxed mb-6 min-h-[120px] transition-opacity">
                "{philosophy.traditions[quoteIdx]?.quote}"
              </blockquote>
              <p className="font-mono text-xs tracking-widest text-white/50">
                — {philosophy.traditions[quoteIdx]?.thinker}, {philosophy.traditions[quoteIdx]?.name}
              </p>
              <div className="flex justify-center gap-2 mt-8">
                {philosophy.traditions.map((_, i) => (
                  <button
                    key={i}
                    onClick={() => setQuoteIdx(i)}
                    className={`w-2 h-2 transition-colors cursor-pointer ${
                      i === quoteIdx ? 'bg-gold' : 'bg-white/20'
                    }`}
                  />
                ))}
              </div>
            </div>
          </section>
        )}

        {/* CTA */}
        <section className="py-24 text-center px-8">
          <h2 className="font-serif text-3xl md:text-4xl text-midnight mb-6">
            What does your flourishing look like?
          </h2>
          <p className="font-sans text-base text-midnight/60 max-w-lg mx-auto mb-10">
            Not checkboxes of problems. Not a needs assessment. An exploration of your aspirations
            across every domain of human existence.
          </p>
          <Link to="/dome-builder" className="btn-gold inline-flex items-center gap-2">
            Build Your Dome <ArrowRight className="w-4 h-4" />
          </Link>
        </section>
      </div>
    </div>
  );
}
