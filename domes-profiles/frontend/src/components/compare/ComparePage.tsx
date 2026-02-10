import { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import { listProfiles, compareProfiles } from '../../api/client';
import CostDisplay from '../shared/CostDisplay';
import type { Profile, CompareResult } from '../../types';

export function ComparePage() {
  const [searchParams] = useSearchParams();
  const [profiles, setProfiles] = useState<Profile[]>([]);
  const [selectedA, setSelectedA] = useState<string>(searchParams.get('a') || '');
  const [selectedB, setSelectedB] = useState<string>(searchParams.get('b') || '');
  const [comparison, setComparison] = useState<CompareResult | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    listProfiles().then(setProfiles).catch(() => {});
  }, []);

  async function handleCompare() {
    if (!selectedA || !selectedB) return;
    setLoading(true);
    try {
      const data = await compareProfiles([selectedA, selectedB]);
      setComparison(data);
    } catch {
      setComparison(null);
    }
    setLoading(false);
  }

  const profileA = comparison?.profiles?.[0];
  const profileB = comparison?.profiles?.[1];

  return (
    <div className="max-w-7xl mx-auto px-6 py-8">
      <h1 className="font-serif text-3xl font-bold tracking-tight mb-2">COMPARE PROFILES</h1>
      <p className="text-gray-600 mb-8">Side-by-side comparison of two profiles showing cost, system, and gap differences.</p>

      <div className="flex gap-4 items-end mb-8">
        <div className="flex-1">
          <label className="block text-xs font-mono uppercase tracking-wider text-gray-500 mb-1">Profile A</label>
          <select
            value={selectedA}
            onChange={e => setSelectedA(e.target.value)}
            className="w-full border border-black p-2 font-sans text-sm bg-white"
          >
            <option value="">Select profile...</option>
            {profiles.map(p => (
              <option key={p.id} value={p.id}>{p.name}</option>
            ))}
          </select>
        </div>
        <div className="text-2xl font-serif font-bold px-4">vs</div>
        <div className="flex-1">
          <label className="block text-xs font-mono uppercase tracking-wider text-gray-500 mb-1">Profile B</label>
          <select
            value={selectedB}
            onChange={e => setSelectedB(e.target.value)}
            className="w-full border border-black p-2 font-sans text-sm bg-white"
          >
            <option value="">Select profile...</option>
            {profiles.map(p => (
              <option key={p.id} value={p.id}>{p.name}</option>
            ))}
          </select>
        </div>
        <button
          onClick={handleCompare}
          disabled={!selectedA || !selectedB || loading}
          className="bg-black text-white px-6 py-2 font-mono text-sm uppercase tracking-wider disabled:opacity-40"
        >
          {loading ? 'Comparing...' : 'Compare'}
        </button>
      </div>

      {comparison && profileA && profileB && (
        <>
          <div className="grid grid-cols-3 gap-0 border border-black mb-8">
            <div className="p-4 border-r border-black bg-gray-50">
              <div className="font-mono text-xs uppercase tracking-wider text-gray-500 mb-1">Metric</div>
            </div>
            <div className="p-4 border-r border-black">
              <div className="font-serif text-lg font-bold">{profileA.name}</div>
            </div>
            <div className="p-4">
              <div className="font-serif text-lg font-bold">{profileB.name}</div>
            </div>

            {[
              { label: 'Annual Cost (Fragmented)', a: profileA.total_annual_cost, b: profileB.total_annual_cost },
              { label: 'Annual Cost (Coordinated)', a: profileA.coordinated_annual_cost, b: profileB.coordinated_annual_cost },
              { label: 'Annual Savings', a: profileA.savings_annual, b: profileB.savings_annual, mode: 'savings' as const },
              { label: 'Systems Involved', a: profileA.systems_involved?.length || 0, b: profileB.systems_involved?.length || 0, isCost: false },
            ].map((row, i) => (
              <div key={i} className="contents">
                <div className="p-4 border-r border-t border-black bg-gray-50">
                  <span className="font-mono text-xs uppercase tracking-wider">{row.label}</span>
                </div>
                <div className="p-4 border-r border-t border-black">
                  {row.isCost !== false ? (
                    <CostDisplay value={row.a as number} mode={row.mode} />
                  ) : (
                    <span className="font-mono text-lg font-bold">{row.a}</span>
                  )}
                </div>
                <div className="p-4 border-t border-black">
                  {row.isCost !== false ? (
                    <CostDisplay value={row.b as number} mode={row.mode} />
                  ) : (
                    <span className="font-mono text-lg font-bold">{row.b}</span>
                  )}
                </div>
              </div>
            ))}
          </div>

          {comparison.deltas && (
            <div className="grid grid-cols-2 gap-6">
              <div className="border border-black p-6">
                <h3 className="font-mono text-xs uppercase tracking-wider text-gray-500 mb-4">Deltas</h3>
                <div className="space-y-3">
                  <div className="flex justify-between items-center">
                    <span className="font-mono text-xs uppercase">Cost Difference</span>
                    <CostDisplay value={comparison.deltas.cost_delta} mode="delta" size="small" />
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="font-mono text-xs uppercase">Savings Difference</span>
                    <CostDisplay value={comparison.deltas.savings_delta} mode="delta" size="small" />
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="font-mono text-xs uppercase">Systems Difference</span>
                    <span className="font-mono text-lg font-bold">{comparison.deltas.systems_delta > 0 ? '+' : ''}{comparison.deltas.systems_delta}</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="font-mono text-xs uppercase">Gaps Difference</span>
                    <span className="font-mono text-lg font-bold">{comparison.deltas.gaps_delta > 0 ? '+' : ''}{comparison.deltas.gaps_delta}</span>
                  </div>
                </div>
              </div>
              {comparison.deltas.circumstances_diff.length > 0 && (
                <div className="border border-black p-6">
                  <h3 className="font-mono text-xs uppercase tracking-wider text-gray-500 mb-4">Differing Circumstances</h3>
                  <div className="flex flex-wrap gap-1">
                    {comparison.deltas.circumstances_diff.map(c => (
                      <span key={c} className="bg-gray-100 border border-gray-300 px-2 py-0.5 font-mono text-xs">{c}</span>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}
        </>
      )}

      {!comparison && !loading && (
        <div className="text-center py-20 text-gray-400">
          <p className="font-serif text-xl">Select two profiles to compare</p>
        </div>
      )}
    </div>
  );
}
