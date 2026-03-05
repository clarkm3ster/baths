import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { fetchApi } from '../api/client';
import { DomainIcon } from '../components/IconMap';

interface Domain {
  id: string; name: string; color: string; icon: string;
  layer: string; description: string;
}

const LAYERS = [
  { key: 'foundation', label: 'Foundation', sub: 'The bedrock upon which all flourishing rests' },
  { key: 'aspiration', label: 'Aspiration', sub: 'The pursuits that elevate life beyond adequacy' },
  { key: 'transcendence', label: 'Transcendence', sub: 'The dimensions that touch something beyond the self' },
];

export default function DomainsPage() {
  const [domains, setDomains] = useState<Domain[]>([]);
  useEffect(() => { fetchApi<Domain[]>('/api/domains').then(setDomains).catch(() => {}); }, []);

  return (
    <div className="max-w-5xl mx-auto px-6 py-20">
      <div className="text-center mb-16">
        <h1 className="font-serif text-4xl md:text-5xl text-midnight mb-4">
          The Twelve Domains of Human Flourishing
        </h1>
        <p className="font-sans text-base text-midnight/60 max-w-2xl mx-auto">
          A comprehensive map of what it means to live well — organized in three ascending layers.
        </p>
        <div className="mt-8 w-24 h-px bg-gold mx-auto" />
      </div>

      {LAYERS.map((layer, li) => {
        const ld = domains.filter(d => d.layer === layer.key);
        if (!ld.length) return null;
        return (
          <section key={layer.key} className={li > 0 ? 'mt-16' : ''}>
            <div className="flex items-center gap-4 mb-2">
              <span className="font-mono text-[10px] tracking-[0.3em] uppercase text-gold">
                Layer {li + 1}
              </span>
              <div className="flex-1 h-px bg-gold/20" />
            </div>
            <h2 className="font-serif text-2xl text-midnight mb-1">{layer.label}</h2>
            <p className="font-sans text-sm text-midnight/40 mb-8">{layer.sub}</p>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {ld.map(d => (
                <Link key={d.id} to={`/domains/${d.id}`}
                  className="group flex border border-midnight/8 hover:border-gold transition-colors">
                  <div className="w-1.5 shrink-0" style={{ background: d.color }} />
                  <div className="flex-1 p-5">
                    <div className="flex items-center gap-3 mb-2">
                      <DomainIcon icon={d.icon} className="w-5 h-5" color={d.color} />
                      <h3 className="font-serif text-lg group-hover:text-gold transition-colors">{d.name}</h3>
                    </div>
                    <p className="font-sans text-sm text-midnight/50 leading-relaxed line-clamp-3">{d.description}</p>
                  </div>
                </Link>
              ))}
            </div>
          </section>
        );
      })}
    </div>
  );
}
