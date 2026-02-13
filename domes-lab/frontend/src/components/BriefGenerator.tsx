import { useState, useEffect } from 'react';
import {
  DOMAINS,
  READINESS_ORDER,
  READINESS_CONFIG,
  AUDIENCES,
  type Innovation,
  type Readiness,
  getAllInnovations,
  generateBrief,
} from '../api/client';

export default function BriefGenerator() {
  const [innovations, setInnovations] = useState<Innovation[]>([]);
  const [loading, setLoading] = useState(true);

  const [selectedDomain, setSelectedDomain] = useState(DOMAINS[0].slug);
  const [selectedReadiness, setSelectedReadiness] = useState<Readiness | 'all'>('all');
  const [selectedAudience, setSelectedAudience] = useState<'governor' | 'cms' | 'investor' | 'legislature'>('governor');
  const [brief, setBrief] = useState('');
  const [copied, setCopied] = useState(false);

  useEffect(() => {
    getAllInnovations().then(all => {
      setInnovations(all);
      setLoading(false);
    });
  }, []);

  const handleGenerate = () => {
    const result = generateBrief(selectedDomain, selectedReadiness, selectedAudience, innovations);
    setBrief(result);
    setCopied(false);
  };

  const handleCopy = () => {
    navigator.clipboard.writeText(brief).then(() => {
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    });
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="font-mono text-sm text-text-muted animate-pulse">LOADING INNOVATION DATA...</div>
      </div>
    );
  }

  return (
    <div>
      <div className="mb-6">
        <h2 className="font-serif text-2xl tracking-wide mb-1">Brief Generator</h2>
        <p className="font-mono text-xs text-text-muted tracking-wide">
          SELECT DOMAIN + READINESS + AUDIENCE &rarr; GENERATE POLISHED BRIEF
        </p>
      </div>

      {/* Controls */}
      <div className="card mb-6">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
          {/* Domain selector */}
          <div>
            <label className="font-mono text-[10px] text-text-muted tracking-wider block mb-1">
              DOMAIN
            </label>
            <select
              value={selectedDomain}
              onChange={e => setSelectedDomain(e.target.value)}
              className="input-field w-full"
            >
              {DOMAINS.map(d => (
                <option key={d.slug} value={d.slug}>{d.label}</option>
              ))}
            </select>
          </div>

          {/* Readiness selector */}
          <div>
            <label className="font-mono text-[10px] text-text-muted tracking-wider block mb-1">
              READINESS LEVEL
            </label>
            <select
              value={selectedReadiness}
              onChange={e => setSelectedReadiness(e.target.value as Readiness | 'all')}
              className="input-field w-full"
            >
              <option value="all">All Readiness Levels</option>
              {READINESS_ORDER.map(r => (
                <option key={r} value={r}>{READINESS_CONFIG[r].label} — {READINESS_CONFIG[r].description}</option>
              ))}
            </select>
          </div>

          {/* Audience selector */}
          <div>
            <label className="font-mono text-[10px] text-text-muted tracking-wider block mb-1">
              TARGET AUDIENCE
            </label>
            <select
              value={selectedAudience}
              onChange={e => setSelectedAudience(e.target.value as typeof selectedAudience)}
              className="input-field w-full"
            >
              {AUDIENCES.map(a => (
                <option key={a.key} value={a.key}>{a.label}</option>
              ))}
            </select>
          </div>
        </div>

        {/* Audience descriptions */}
        <div className="grid grid-cols-4 gap-2 mb-4">
          {AUDIENCES.map(a => (
            <button
              key={a.key}
              onClick={() => setSelectedAudience(a.key as typeof selectedAudience)}
              className={`p-2 border text-left transition-colors ${
                selectedAudience === a.key
                  ? 'border-accent-glow bg-accent/20'
                  : 'border-border hover:border-accent-light'
              }`}
            >
              <div className="font-mono text-[10px] tracking-wider mb-0.5">{a.label.toUpperCase()}</div>
              <div className="text-[10px] text-text-muted">{a.description}</div>
            </button>
          ))}
        </div>

        <button onClick={handleGenerate} className="btn-primary w-full">
          GENERATE BRIEF
        </button>
      </div>

      {/* Output */}
      {brief && (
        <div className="card">
          <div className="flex items-center justify-between mb-3">
            <span className="font-mono text-xs text-text-muted tracking-wider">GENERATED BRIEF</span>
            <button onClick={handleCopy} className="btn-ghost text-xs">
              {copied ? 'COPIED!' : 'COPY TO CLIPBOARD'}
            </button>
          </div>
          <pre className="font-mono text-xs text-text whitespace-pre-wrap leading-relaxed bg-bg p-4 border border-border overflow-auto max-h-[600px]">
            {brief}
          </pre>
        </div>
      )}
    </div>
  );
}
