import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { fetchApi } from '../api/client';
import { DomainIcon } from '../components/IconMap';

interface Domain {
  id: string; name: string; color: string; icon: string; layer: string;
  description: string; flourishing_looks_like: string; threats: string[]; de_risked_by: string[];
}
interface Resource { type: string; name: string; description: string; coverage: number | string; }

const TYPE_ORDER = ['public', 'communal', 'private', 'personal', 'natural'];
const TYPE_LABELS: Record<string, string> = {
  public: 'Public', communal: 'Communal', private: 'Private', personal: 'Personal', natural: 'Natural'
};

export default function DomainDetailPage() {
  const { id } = useParams<{ id: string }>();
  const [domain, setDomain] = useState<Domain | null>(null);
  const [resources, setResources] = useState<Resource[]>([]);

  useEffect(() => {
    if (!id) return;
    fetchApi<Domain>(`/api/domains/${id}`).then(setDomain).catch(() => {});
    fetchApi<{ resources: Resource[] }>(`/api/domains/${id}/resources`).then(d => setResources(d.resources || [])).catch(() => {});
  }, [id]);

  if (!domain) return (
    <div className="min-h-[60vh] flex items-center justify-center">
      <p className="font-serif text-xl text-midnight/40 animate-pulse">Loading…</p>
    </div>
  );

  const byType: Record<string, Resource[]> = {};
  resources.forEach(r => { const k = r.type?.toLowerCase() || 'other'; (byType[k] ??= []).push(r); });

  return (
    <div>
      {/* Breadcrumb */}
      <nav className="max-w-4xl mx-auto px-6 pt-8 font-sans text-sm text-midnight/40">
        <Link to="/domains" className="hover:text-gold underline underline-offset-4">Domains</Link>
        <span className="mx-2">/</span>
        <span className="text-midnight/70">{domain.name}</span>
      </nav>

      {/* Hero */}
      <header className="max-w-4xl mx-auto px-6 pt-10 pb-12">
        <div className="flex items-center gap-4 mb-6">
          <div className="w-12 h-12 flex items-center justify-center border-2" style={{ borderColor: domain.color }}>
            <DomainIcon icon={domain.icon} className="w-6 h-6" color={domain.color} />
          </div>
          <div>
            <span className="font-mono text-[10px] tracking-widest uppercase text-midnight/40">{domain.layer}</span>
            <h1 className="font-serif text-4xl text-midnight">{domain.name}</h1>
          </div>
        </div>
        <div className="h-1 w-full mb-6" style={{ background: domain.color }} />
        <p className="font-sans text-base text-midnight/70 leading-relaxed">{domain.description}</p>
      </header>

      {/* Flourishing */}
      <section className="max-w-4xl mx-auto px-6 pb-12">
        <p className="font-mono text-[10px] tracking-widest uppercase text-midnight/40 mb-4">
          What Flourishing Looks Like
        </p>
        <div className="bg-parchment border-l-4 p-8" style={{ borderColor: domain.color }}>
          <p className="font-serif text-lg italic text-midnight/80 leading-relaxed">
            {domain.flourishing_looks_like}
          </p>
        </div>
      </section>

      {/* Threats & De-risking */}
      <section className="max-w-4xl mx-auto px-6 pb-12 grid grid-cols-1 md:grid-cols-2 gap-8">
        <div>
          <p className="font-mono text-[10px] tracking-widest uppercase text-midnight/40 mb-4">What Threatens It</p>
          <ul className="space-y-2">
            {domain.threats.map((t, i) => (
              <li key={i} className="flex items-start gap-3 bg-red-50/50 border border-red-200/50 p-3">
                <span className="text-red-600 font-mono text-xs mt-0.5">!</span>
                <span className="font-sans text-sm text-red-900/70">{t}</span>
              </li>
            ))}
          </ul>
        </div>
        <div>
          <p className="font-mono text-[10px] tracking-widest uppercase text-midnight/40 mb-4">What De-Risks It</p>
          <ul className="space-y-2">
            {domain.de_risked_by.map((t, i) => (
              <li key={i} className="flex items-start gap-3 bg-emerald-50/50 border border-emerald-200/50 p-3">
                <span className="text-emerald-600 font-mono text-xs mt-0.5">+</span>
                <span className="font-sans text-sm text-emerald-900/70">{t}</span>
              </li>
            ))}
          </ul>
        </div>
      </section>

      {/* Resources */}
      {resources.length > 0 && (
        <section className="bg-parchment border-t border-midnight/10">
          <div className="max-w-4xl mx-auto px-6 py-12">
            <h2 className="font-serif text-2xl text-midnight mb-8">Resources</h2>
            {TYPE_ORDER.map(type => {
              const group = byType[type];
              if (!group) return null;
              return (
                <div key={type} className="mb-8">
                  <div className="flex items-center gap-3 mb-4">
                    <h3 className="font-mono text-[10px] tracking-widest uppercase text-midnight/40">
                      {TYPE_LABELS[type] || type}
                    </h3>
                    <div className="flex-1 h-px bg-midnight/10" />
                  </div>
                  <div className="space-y-3">
                    {group.map((r, i) => (
                      <div key={i} className="bg-warm-white border border-midnight/8 p-4">
                        <div className="flex items-start justify-between gap-4">
                          <div>
                            <h4 className="font-serif text-base">{r.name}</h4>
                            <p className="font-sans text-sm text-midnight/50 mt-1">{r.description}</p>
                          </div>
                          <span className="font-mono text-[10px] px-2 py-0.5 border border-midnight/20 text-midnight/50 shrink-0">
                            {typeof r.coverage === 'number' ? `${r.coverage}%` : r.coverage}
                          </span>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              );
            })}
          </div>
        </section>
      )}

      <div className="max-w-4xl mx-auto px-6 py-8">
        <Link to="/domains" className="font-sans text-sm text-gold hover:text-gold-light underline underline-offset-4">
          ← Back to all domains
        </Link>
      </div>
    </div>
  );
}
