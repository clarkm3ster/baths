import { useState, useEffect, useMemo } from 'react';
import {
  type Innovation,
  type Teammate,
  getInnovations,
  getTeammates,
  getStatusColor,
  getHorizonLabel,
  getTeammateColor,
  DEMO_INNOVATIONS,
  DEMO_TEAMMATES,
} from '../api/client';

type SortOption = 'newest' | 'impact' | 'feasibility' | 'novelty';

export default function InnovationBrowser() {
  const [innovations, setInnovations] = useState<Innovation[]>(DEMO_INNOVATIONS);
  const [teammates, setTeammates] = useState<Teammate[]>(DEMO_TEAMMATES);
  const [domainFilter, setDomainFilter] = useState<string>('all');
  const [statusFilter, setStatusFilter] = useState<string>('all');
  const [horizonFilter, setHorizonFilter] = useState<string>('all');
  const [minImpact, setMinImpact] = useState<number>(0);
  const [sortBy, setSortBy] = useState<SortOption>('newest');

  useEffect(() => {
    getInnovations().then(setInnovations);
    getTeammates().then(setTeammates);
  }, []);

  // Unique domains for filter dropdown
  const domains = useMemo(() => {
    const set = new Set(innovations.map((i) => i.domain));
    return Array.from(set).sort();
  }, [innovations]);

  // Filtered + sorted
  const filtered = useMemo(() => {
    let result = [...innovations];
    if (domainFilter !== 'all') result = result.filter((i) => i.domain === domainFilter);
    if (statusFilter !== 'all') result = result.filter((i) => i.status === statusFilter);
    if (horizonFilter !== 'all') result = result.filter((i) => i.time_horizon === horizonFilter);
    if (minImpact > 0) result = result.filter((i) => i.impact_score >= minImpact);

    const sortFns: Record<SortOption, (a: Innovation, b: Innovation) => number> = {
      newest: (a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime(),
      impact: (a, b) => b.impact_score - a.impact_score,
      feasibility: (a, b) => b.feasibility_score - a.feasibility_score,
      novelty: (a, b) => b.novelty_score - a.novelty_score,
    };
    result.sort(sortFns[sortBy]);
    return result;
  }, [innovations, domainFilter, statusFilter, horizonFilter, minImpact, sortBy]);

  const statusTabs = ['all', 'draft', 'review', 'approved', 'archived'] as const;

  return (
    <div className="space-y-6">
      {/* ── Header ── */}
      <div>
        <h2 className="font-serif text-2xl tracking-wide">Innovation Browser</h2>
        <p className="mt-1 font-mono text-xs text-text-muted tracking-wider">
          {innovations.length} INNOVATIONS TOTAL // {filtered.length} MATCHING FILTERS
        </p>
      </div>

      {/* ── Filters ── */}
      <div className="bg-surface border border-border p-4 space-y-4">
        {/* Status Tabs */}
        <div className="flex items-center gap-1">
          <span className="font-mono text-[10px] text-text-muted tracking-wider mr-3">STATUS:</span>
          {statusTabs.map((s) => (
            <button
              key={s}
              onClick={() => setStatusFilter(s)}
              className={`font-mono text-[10px] tracking-wider px-3 py-1.5 border transition-colors ${
                statusFilter === s
                  ? 'border-accent-glow bg-accent/30 text-text'
                  : 'border-border text-text-muted hover:text-text hover:border-text-muted'
              }`}
            >
              {s === 'all' ? 'ALL' : s.toUpperCase()}
            </button>
          ))}
        </div>

        {/* Filter Row */}
        <div className="flex items-end gap-4">
          {/* Domain */}
          <div className="flex-1">
            <label className="block font-mono text-[10px] text-text-muted tracking-wider mb-1">
              DOMAIN
            </label>
            <select
              value={domainFilter}
              onChange={(e) => setDomainFilter(e.target.value)}
              className="input-field w-full"
            >
              <option value="all">All Domains</option>
              {domains.map((d) => (
                <option key={d} value={d}>{d}</option>
              ))}
            </select>
          </div>

          {/* Horizon */}
          <div>
            <label className="block font-mono text-[10px] text-text-muted tracking-wider mb-1">
              TIME HORIZON
            </label>
            <select
              value={horizonFilter}
              onChange={(e) => setHorizonFilter(e.target.value)}
              className="input-field"
            >
              <option value="all">All</option>
              <option value="near">Near (0-2 yrs)</option>
              <option value="medium">Medium (2-5 yrs)</option>
              <option value="far">Far (5+ yrs)</option>
            </select>
          </div>

          {/* Min Impact */}
          <div>
            <label className="block font-mono text-[10px] text-text-muted tracking-wider mb-1">
              MIN IMPACT
            </label>
            <select
              value={minImpact}
              onChange={(e) => setMinImpact(Number(e.target.value))}
              className="input-field"
            >
              <option value={0}>Any</option>
              <option value={3}>3+</option>
              <option value={4}>4+</option>
              <option value={5}>5</option>
            </select>
          </div>

          {/* Sort */}
          <div>
            <label className="block font-mono text-[10px] text-text-muted tracking-wider mb-1">
              SORT BY
            </label>
            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value as SortOption)}
              className="input-field"
            >
              <option value="newest">Newest</option>
              <option value="impact">Highest Impact</option>
              <option value="feasibility">Highest Feasibility</option>
              <option value="novelty">Highest Novelty</option>
            </select>
          </div>
        </div>
      </div>

      {/* ── Results ── */}
      {filtered.length === 0 ? (
        <div className="bg-surface border border-border p-8 text-center">
          <div className="font-mono text-sm text-text-muted">
            NO INNOVATIONS MATCH CURRENT FILTERS
          </div>
        </div>
      ) : (
        <div className="space-y-3">
          {filtered.map((inn) => {
            const tmColor = getTeammateColor(inn.teammate_slug);
            const tm = teammates.find(t => t.slug === inn.teammate_slug);

            return (
              <div
                key={inn.id}
                className="bg-surface border border-border p-4"
                style={{ borderLeftWidth: '3px', borderLeftColor: tmColor }}
              >
                <div className="flex items-start gap-4">
                  {/* Main content */}
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-3 mb-1">
                      <h3 className="text-base font-medium">{inn.title}</h3>
                      <div
                        className="badge shrink-0"
                        style={{
                          color: getStatusColor(inn.status),
                          borderColor: getStatusColor(inn.status),
                        }}
                      >
                        {inn.status.toUpperCase()}
                      </div>
                      <div className="badge text-text-muted border-border shrink-0">
                        {getHorizonLabel(inn.time_horizon)}
                      </div>
                    </div>

                    <p className="text-sm text-text-muted leading-relaxed">
                      {inn.summary}
                    </p>

                    {/* Meta Row */}
                    <div className="flex items-center gap-4 mt-3">
                      {/* Domain Badge */}
                      <span
                        className="badge"
                        style={{ color: tmColor, borderColor: tmColor + '66' }}
                      >
                        {inn.domain}
                      </span>

                      {/* Teammate */}
                      <span className="font-mono text-[10px] text-text-muted">
                        by {tm?.name || inn.teammate_name}
                      </span>

                      {/* Date */}
                      <span className="font-mono text-[10px] text-text-muted">
                        {new Date(inn.created_at).toLocaleDateString('en-US', {
                          month: 'short', day: 'numeric', year: 'numeric',
                        })}
                      </span>

                      {/* Tags */}
                      {inn.tags.length > 0 && (
                        <div className="flex items-center gap-1">
                          {inn.tags.slice(0, 3).map((tag) => (
                            <span key={tag} className="font-mono text-[9px] text-text-muted bg-bg px-1.5 py-0.5 border border-border">
                              #{tag}
                            </span>
                          ))}
                        </div>
                      )}
                    </div>
                  </div>

                  {/* Score Bars */}
                  <div className="shrink-0 w-36 space-y-2">
                    {[
                      { label: 'Impact', value: inn.impact_score, color: '#DC2626' },
                      { label: 'Feasibility', value: inn.feasibility_score, color: '#C9A726' },
                      { label: 'Novelty', value: inn.novelty_score, color: '#4169E1' },
                    ].map((score) => (
                      <div key={score.label}>
                        <div className="flex items-center justify-between mb-0.5">
                          <span className="font-mono text-[9px] text-text-muted">
                            {score.label.substring(0, 3).toUpperCase()}
                          </span>
                          <span className="font-mono text-[10px]" style={{ color: score.color }}>
                            {score.value}/5
                          </span>
                        </div>
                        <div className="score-bar">
                          <div
                            className="score-bar-fill"
                            style={{
                              width: `${(score.value / 5) * 100}%`,
                              backgroundColor: score.color,
                            }}
                          />
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
