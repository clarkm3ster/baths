import { useState, useEffect } from 'react';
import {
  type StatsResponse,
  getStats,
  getTeammateColor,
  DEMO_STATS,
  DEMO_TEAMMATES,
} from '../api/client';

export default function StatsPanel() {
  const [stats, setStats] = useState<StatsResponse>(DEMO_STATS);

  useEffect(() => {
    getStats().then(setStats);
  }, []);

  // Map domain names to teammate slugs for coloring
  const domainToSlug: Record<string, string> = {};
  DEMO_TEAMMATES.forEach((tm) => {
    domainToSlug[tm.domain] = tm.slug;
  });

  const domainEntries = Object.entries(stats.domain_counts).sort((a, b) => b[1] - a[1]);
  const maxDomainCount = Math.max(...Object.values(stats.domain_counts), 1);

  const statusEntries = Object.entries(stats.status_counts);
  const totalStatusCount = statusEntries.reduce((sum, [, c]) => sum + c, 0);

  const horizonEntries = Object.entries(stats.horizon_counts);
  const totalHorizonCount = horizonEntries.reduce((sum, [, c]) => sum + c, 0);

  const statusColors: Record<string, string> = {
    draft: '#6B7280', review: '#D97706', approved: '#059669', archived: '#4B5563',
  };

  const horizonColors: Record<string, string> = {
    near: '#059669', medium: '#D97706', far: '#DC2626',
  };

  const horizonLabels: Record<string, string> = {
    near: '0-2 YRS', medium: '2-5 YRS', far: '5+ YRS',
  };

  return (
    <div className="space-y-6">
      {/* ── Header ── */}
      <div>
        <h2 className="font-serif text-2xl tracking-wide">Analytics Dashboard</h2>
        <p className="mt-1 font-mono text-xs text-text-muted tracking-wider">
          DOMES INNOVATION LABORATORY // PERFORMANCE METRICS
        </p>
      </div>

      {/* ── Summary Stats ── */}
      <div className="grid grid-cols-4 gap-3">
        {[
          { label: 'Total Innovations', value: stats.total_innovations, color: '#4169E1' },
          { label: 'Avg Impact', value: stats.avg_impact.toFixed(1) + '/5', color: '#DC2626' },
          { label: 'Avg Feasibility', value: stats.avg_feasibility.toFixed(1) + '/5', color: '#C9A726' },
          { label: 'Avg Novelty', value: stats.avg_novelty.toFixed(1) + '/5', color: '#9333EA' },
        ].map((s) => (
          <div key={s.label} className="bg-surface border border-border p-4">
            <div className="font-mono text-[10px] text-text-muted tracking-wider uppercase mb-2">
              {s.label}
            </div>
            <div className="font-serif text-3xl" style={{ color: s.color }}>{s.value}</div>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-2 gap-6">
        {/* ── Domain Breakdown ── */}
        <div className="bg-surface border border-border p-5">
          <h3 className="font-mono text-xs tracking-widest text-text-muted uppercase mb-4">
            Innovation Count by Domain
          </h3>
          <div className="space-y-3">
            {domainEntries.map(([domain, count]) => {
              const slug = domainToSlug[domain] || 'architect';
              const color = getTeammateColor(slug);
              return (
                <div key={domain}>
                  <div className="flex items-center justify-between mb-1">
                    <span className="text-xs truncate max-w-[260px]" title={domain}>
                      {domain}
                    </span>
                    <span className="font-mono text-xs ml-2" style={{ color }}>
                      {count}
                    </span>
                  </div>
                  <div className="h-3 bg-bg">
                    <div
                      className="h-full transition-all duration-500"
                      style={{
                        width: `${(count / maxDomainCount) * 100}%`,
                        backgroundColor: color,
                      }}
                    />
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* ── Score Distributions by Domain ── */}
        <div className="bg-surface border border-border p-5">
          <h3 className="font-mono text-xs tracking-widest text-text-muted uppercase mb-4">
            Average Scores by Domain
          </h3>
          <div className="space-y-4">
            {domainEntries.map(([domain]) => {
              const slug = domainToSlug[domain] || 'architect';
              const color = getTeammateColor(slug);
              const impact = (stats.domain_avg_impact as Record<string, number>)[domain] || 0;
              const feasibility = (stats.domain_avg_feasibility as Record<string, number>)[domain] || 0;
              const novelty = (stats.domain_avg_novelty as Record<string, number>)[domain] || 0;

              return (
                <div key={domain}>
                  <div className="flex items-center gap-2 mb-1.5">
                    <div className="h-2.5 w-2.5 shrink-0" style={{ backgroundColor: color }} />
                    <span className="text-xs truncate" title={domain}>
                      {domain.length > 30 ? domain.substring(0, 30) + '...' : domain}
                    </span>
                  </div>
                  <div className="flex gap-2">
                    {/* Impact bar */}
                    <div className="flex-1">
                      <div className="flex items-center justify-between mb-0.5">
                        <span className="font-mono text-[8px] text-text-muted">IMP</span>
                        <span className="font-mono text-[8px]" style={{ color: '#DC2626' }}>
                          {impact.toFixed(1)}
                        </span>
                      </div>
                      <div className="h-1.5 bg-bg">
                        <div
                          className="h-full"
                          style={{ width: `${(impact / 5) * 100}%`, backgroundColor: '#DC2626' }}
                        />
                      </div>
                    </div>
                    {/* Feasibility bar */}
                    <div className="flex-1">
                      <div className="flex items-center justify-between mb-0.5">
                        <span className="font-mono text-[8px] text-text-muted">FEA</span>
                        <span className="font-mono text-[8px]" style={{ color: '#C9A726' }}>
                          {feasibility.toFixed(1)}
                        </span>
                      </div>
                      <div className="h-1.5 bg-bg">
                        <div
                          className="h-full"
                          style={{ width: `${(feasibility / 5) * 100}%`, backgroundColor: '#C9A726' }}
                        />
                      </div>
                    </div>
                    {/* Novelty bar */}
                    <div className="flex-1">
                      <div className="flex items-center justify-between mb-0.5">
                        <span className="font-mono text-[8px] text-text-muted">NOV</span>
                        <span className="font-mono text-[8px]" style={{ color: '#4169E1' }}>
                          {novelty.toFixed(1)}
                        </span>
                      </div>
                      <div className="h-1.5 bg-bg">
                        <div
                          className="h-full"
                          style={{ width: `${(novelty / 5) * 100}%`, backgroundColor: '#4169E1' }}
                        />
                      </div>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-6">
        {/* ── Status Pipeline ── */}
        <div className="bg-surface border border-border p-5">
          <h3 className="font-mono text-xs tracking-widest text-text-muted uppercase mb-4">
            Status Pipeline
          </h3>

          {/* Pipeline Visualization */}
          <div className="flex items-center gap-0 mb-6">
            {statusEntries.map(([status, count], i) => {
              const color = statusColors[status] || '#6B7280';
              const pct = totalStatusCount > 0 ? (count / totalStatusCount) * 100 : 0;
              return (
                <div
                  key={status}
                  className="flex flex-col items-center"
                  style={{ width: `${pct}%`, minWidth: '40px' }}
                >
                  <div
                    className="w-full h-8 flex items-center justify-center font-mono text-[10px] font-bold"
                    style={{ backgroundColor: color }}
                  >
                    {count}
                  </div>
                  {i < statusEntries.length - 1 && null}
                </div>
              );
            })}
          </div>

          {/* Status Legend */}
          <div className="space-y-2">
            {statusEntries.map(([status, count]) => {
              const color = statusColors[status] || '#6B7280';
              const pct = totalStatusCount > 0 ? ((count / totalStatusCount) * 100).toFixed(0) : '0';
              return (
                <div key={status} className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <div className="h-3 w-3 shrink-0" style={{ backgroundColor: color }} />
                    <span className="font-mono text-xs tracking-wider uppercase">{status}</span>
                  </div>
                  <div className="flex items-center gap-3">
                    <span className="font-mono text-xs" style={{ color }}>{count}</span>
                    <span className="font-mono text-[10px] text-text-muted">{pct}%</span>
                  </div>
                </div>
              );
            })}
          </div>

          {/* Pipeline Flow Arrow */}
          <div className="mt-4 flex items-center justify-center gap-2 text-text-muted">
            {['DRAFT', 'REVIEW', 'APPROVED', 'ARCHIVED'].map((label, i) => (
              <div key={label} className="flex items-center gap-2">
                <span className="font-mono text-[9px] tracking-wider">{label}</span>
                {i < 3 && <span className="font-mono text-[9px]">--&gt;</span>}
              </div>
            ))}
          </div>
        </div>

        {/* ── Time Horizon Distribution ── */}
        <div className="bg-surface border border-border p-5">
          <h3 className="font-mono text-xs tracking-widest text-text-muted uppercase mb-4">
            Time Horizon Distribution
          </h3>

          {/* Large Horizon Blocks */}
          <div className="grid grid-cols-3 gap-3 mb-4">
            {horizonEntries.map(([horizon, count]) => {
              const color = horizonColors[horizon] || '#6B7280';
              const label = horizonLabels[horizon] || horizon.toUpperCase();
              const pct = totalHorizonCount > 0 ? ((count / totalHorizonCount) * 100).toFixed(0) : '0';
              return (
                <div
                  key={horizon}
                  className="border p-4 text-center"
                  style={{ borderColor: color + '66' }}
                >
                  <div className="font-serif text-3xl mb-1" style={{ color }}>{count}</div>
                  <div className="font-mono text-[10px] tracking-wider" style={{ color }}>
                    {label}
                  </div>
                  <div className="font-mono text-[9px] text-text-muted mt-1">{pct}%</div>
                </div>
              );
            })}
          </div>

          {/* Horizon Bar */}
          <div className="h-4 flex">
            {horizonEntries.map(([horizon, count]) => {
              const color = horizonColors[horizon] || '#6B7280';
              const pct = totalHorizonCount > 0 ? (count / totalHorizonCount) * 100 : 0;
              return (
                <div
                  key={horizon}
                  className="h-full"
                  style={{ width: `${pct}%`, backgroundColor: color }}
                />
              );
            })}
          </div>
          <div className="flex items-center justify-between mt-2">
            <span className="font-mono text-[9px] text-text-muted">NEAR TERM</span>
            <span className="font-mono text-[9px] text-text-muted">FAR HORIZON</span>
          </div>

          {/* Meta Stats */}
          <div className="mt-6 grid grid-cols-2 gap-3">
            <div className="bg-bg border border-border p-3 text-center">
              <div className="font-mono text-[10px] text-text-muted tracking-wider mb-1">
                TOTAL TEAMMATES
              </div>
              <div className="font-serif text-2xl" style={{ color: '#059669' }}>
                {stats.total_teammates}
              </div>
            </div>
            <div className="bg-bg border border-border p-3 text-center">
              <div className="font-mono text-[10px] text-text-muted tracking-wider mb-1">
                COLLABORATIONS
              </div>
              <div className="font-serif text-2xl" style={{ color: '#9333EA' }}>
                {stats.total_collaborations}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
