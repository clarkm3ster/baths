import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { fetchApi } from '../api/client';
import { ArrowRight, ChevronDown, ChevronUp } from 'lucide-react';

interface Model { id: string; name: string; layer: string; description: string; examples: string[]; per_person_impact: number; }
interface Instrument { id: string; name: string; description: string; mechanism: string; projected_return: string; }
interface PersonalArch {
  layers: Array<{ name: string; purpose: string; instruments: Array<{ name: string; annual_value: number; type: string; description: string }>; annual_value: number }>;
  total_annual_architecture: number; philosophy: string;
}

function fmt(n: number) { return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', maximumFractionDigits: 0 }).format(n); }

export default function FinancePage() {
  const [models, setModels] = useState<Model[]>([]);
  const [instruments, setInstruments] = useState<Instrument[]>([]);
  const [age, setAge] = useState(35);
  const [income, setIncome] = useState('median');
  const [loc, setLoc] = useState('urban');
  const [result, setResult] = useState<PersonalArch | null>(null);
  const [openInst, setOpenInst] = useState<string | null>(null);

  useEffect(() => {
    fetchApi<{ existing_models: Model[]; new_instruments: Instrument[] }>('/api/finance/models')
      .then(d => { setModels(d.existing_models || []); setInstruments(d.new_instruments || []); })
      .catch(() => {});
  }, []);

  async function build() {
    const r = await fetchApi<PersonalArch>('/api/finance/personal-architecture', {
      method: 'POST', body: JSON.stringify({ age, income_level: income, location: loc, aspirations: [] }),
    });
    setResult(r);
  }

  return (
    <div>
      <section className="max-w-5xl mx-auto px-6 py-20">
        <p className="section-label mb-3">Financial Architecture</p>
        <h1 className="font-serif text-4xl md:text-5xl text-midnight mb-4">
          The Financial Architecture of Human Flourishing
        </h1>
        <p className="font-sans text-base text-midnight/60 max-w-2xl mb-8">
          Not benefits. Not welfare. A comprehensive investment architecture designed to unlock
          human potential at every scale.
        </p>
        <div className="flex gap-4">
          <Link to="/global" className="btn-gold flex items-center gap-2">Global Models <ArrowRight className="w-3 h-3" /></Link>
          <Link to="/flourishing-index" className="btn-gold flex items-center gap-2">Index <ArrowRight className="w-3 h-3" /></Link>
        </div>
      </section>

      {/* Models */}
      <section className="max-w-5xl mx-auto px-6 pb-16">
        <p className="section-label mb-6">Finance Models</p>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {models.map(m => (
            <div key={m.id} className="border border-midnight/10 p-5 hover:border-gold transition-colors">
              <p className="font-mono text-[10px] tracking-widest text-midnight/30 mb-1 uppercase">{m.layer}</p>
              <h3 className="font-serif text-lg mb-2">{m.name}</h3>
              <p className="font-sans text-sm text-midnight/60 mb-3 leading-relaxed">{m.description}</p>
              <div className="flex flex-wrap gap-1 mb-3">
                {m.examples.map(e => (
                  <span key={e} className="border border-midnight/10 px-2 py-0.5 text-[10px] font-mono text-midnight/50">{e}</span>
                ))}
              </div>
              <p className="font-mono text-sm text-gold">{fmt(m.per_person_impact)}/person</p>
            </div>
          ))}
        </div>
      </section>

      {/* Instruments */}
      {instruments.length > 0 && (
        <section className="max-w-5xl mx-auto px-6 pb-16">
          <p className="section-label mb-6">New Financial Instruments</p>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {instruments.map(inst => (
              <div key={inst.id} className="border border-midnight/10">
                <div className="p-5">
                  <h3 className="font-serif text-lg mb-2">{inst.name}</h3>
                  <p className="font-sans text-sm text-midnight/60 mb-3">{inst.description}</p>
                  <p className="font-mono text-sm text-gold mb-3">Return: {inst.projected_return}</p>
                  <button onClick={() => setOpenInst(openInst === inst.id ? null : inst.id)}
                    className="flex items-center gap-1 font-mono text-[10px] tracking-widest text-midnight/40 hover:text-gold cursor-pointer uppercase">
                    Mechanism {openInst === inst.id ? <ChevronUp className="w-3 h-3" /> : <ChevronDown className="w-3 h-3" />}
                  </button>
                </div>
                {openInst === inst.id && (
                  <div className="border-t border-midnight/10 bg-parchment p-5">
                    <p className="font-sans text-sm text-midnight/60 leading-relaxed">{inst.mechanism}</p>
                  </div>
                )}
              </div>
            ))}
          </div>
        </section>
      )}

      {/* Personal Builder */}
      <section className="max-w-5xl mx-auto px-6 pb-20">
        <p className="section-label mb-6">Personal Architecture Builder</p>
        <div className="border border-midnight/10 p-6 max-w-xl">
          <div className="grid grid-cols-3 gap-4 mb-6">
            <div>
              <label className="font-mono text-[10px] tracking-widest text-midnight/40 mb-1 block uppercase">Age</label>
              <input type="number" value={age} onChange={e => setAge(+e.target.value)}
                className="w-full border border-midnight/20 px-3 py-2 font-mono text-sm focus:border-gold focus:outline-none bg-transparent" />
            </div>
            <div>
              <label className="font-mono text-[10px] tracking-widest text-midnight/40 mb-1 block uppercase">Income</label>
              <select value={income} onChange={e => setIncome(e.target.value)}
                className="w-full border border-midnight/20 px-3 py-2 font-mono text-sm focus:border-gold focus:outline-none bg-transparent appearance-none">
                <option value="low">Low</option><option value="median">Median</option>
                <option value="high">High</option><option value="wealthy">Wealthy</option>
              </select>
            </div>
            <div>
              <label className="font-mono text-[10px] tracking-widest text-midnight/40 mb-1 block uppercase">Location</label>
              <select value={loc} onChange={e => setLoc(e.target.value)}
                className="w-full border border-midnight/20 px-3 py-2 font-mono text-sm focus:border-gold focus:outline-none bg-transparent appearance-none">
                <option value="urban">Urban</option><option value="suburban">Suburban</option><option value="rural">Rural</option>
              </select>
            </div>
          </div>
          <button onClick={build} className="btn-gold cursor-pointer">Build My Architecture</button>
        </div>

        {result && (
          <div className="mt-8 border border-gold p-6">
            <div className="flex justify-between items-start mb-6">
              <p className="font-mono text-[10px] tracking-widest text-midnight/40 uppercase">Personal Financial Dome</p>
              <p className="font-serif text-3xl text-gold">{fmt(result.total_annual_architecture)}<span className="text-sm text-midnight/40">/year</span></p>
            </div>
            {result.layers.map((l, i) => (
              <div key={i} className="mb-4">
                <div className="flex justify-between mb-1">
                  <span className="font-serif text-sm">{l.name}</span>
                  <span className="font-mono text-sm text-gold">{fmt(l.annual_value)}</span>
                </div>
                <div className="h-4 bg-midnight/5 relative">
                  <div className="h-full bg-gold/70" style={{ width: `${(l.annual_value / result.total_annual_architecture) * 100}%` }} />
                </div>
              </div>
            ))}
            <p className="font-serif text-base italic text-midnight/60 mt-6">{result.philosophy}</p>
          </div>
        )}
      </section>
    </div>
  );
}
