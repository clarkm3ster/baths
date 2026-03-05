/**
 * CostBreakdown — system-by-system cost table with domain-colored bars
 * and a totals row.
 */

import type { ProfileDomain } from '../../types';
import { formatCurrencyFull } from '../shared/CostDisplay';
import DomainBadge from '../shared/DomainBadge';

const DOMAIN_COLORS: Record<string, string> = {
  health: 'var(--color-health)',
  justice: 'var(--color-justice)',
  housing: 'var(--color-housing)',
  income: 'var(--color-income)',
  education: 'var(--color-education)',
  child_welfare: 'var(--color-child-welfare)',
};

interface SystemRow {
  name: string;
  domain: string;
  domainLabel: string;
  fragmented: number;
  coordinated: number;
  savings: number;
}

interface Props {
  domains: ProfileDomain[];
  totalFragmented: number;
  totalCoordinated: number;
  totalSavings: number;
}

export default function CostBreakdown({
  domains,
  totalFragmented,
  totalCoordinated,
  totalSavings,
}: Props) {
  // Flatten systems from all domains
  const systems: SystemRow[] = domains.flatMap((d) =>
    (d.systems || []).map((sys: any) => ({
      name: sys.name || sys.acronym || sys.id,
      domain: d.domain,
      domainLabel: d.domain_label,
      fragmented: sys.annual_cost ?? 0,
      coordinated: sys.coordinated_cost ?? 0,
      savings: (sys.annual_cost ?? 0) - (sys.coordinated_cost ?? 0),
    }))
  );

  const maxCost = Math.max(...systems.map((s) => s.fragmented), 1);

  return (
    <div>
      <div className="section-label mb-4">System-by-System Cost Breakdown</div>

      {/* Table header */}
      <div className="grid grid-cols-[1fr_120px_120px_120px_200px] gap-0 border-b-2 border-black pb-2 mb-0">
        <div className="font-mono text-[11px] uppercase tracking-wider text-[var(--color-text-tertiary)]">
          System
        </div>
        <div className="font-mono text-[11px] uppercase tracking-wider text-[var(--color-text-tertiary)] text-right">
          Fragmented
        </div>
        <div className="font-mono text-[11px] uppercase tracking-wider text-[var(--color-text-tertiary)] text-right">
          Coordinated
        </div>
        <div className="font-mono text-[11px] uppercase tracking-wider text-[var(--color-text-tertiary)] text-right">
          Savings
        </div>
        <div className="font-mono text-[11px] uppercase tracking-wider text-[var(--color-text-tertiary)] pl-4">
          Cost bar
        </div>
      </div>

      {/* System rows */}
      {systems.map((sys, i) => {
        const fragPct = (sys.fragmented / maxCost) * 100;
        const coordPct = (sys.coordinated / maxCost) * 100;
        const color = DOMAIN_COLORS[sys.domain] || '#666';

        return (
          <div
            key={i}
            className="grid grid-cols-[1fr_120px_120px_120px_200px] gap-0 items-center py-3 border-b border-[var(--color-border)]"
          >
            <div className="flex items-center gap-2">
              <span
                className="inline-block w-[8px] h-[8px] shrink-0"
                style={{ background: color }}
              />
              <span className="text-[13px]">{sys.name}</span>
            </div>
            <div className="font-mono text-[13px] text-right">
              {formatCurrencyFull(sys.fragmented)}
            </div>
            <div className="font-mono text-[13px] text-right">
              {formatCurrencyFull(sys.coordinated)}
            </div>
            <div className="font-mono text-[13px] text-right text-[var(--color-savings)]">
              {formatCurrencyFull(sys.savings)}
            </div>
            <div className="pl-4">
              <div className="cost-bar">
                <div
                  className="cost-bar__fill"
                  style={{
                    width: `${fragPct}%`,
                    background: `${color}33`,
                  }}
                />
                <div
                  className="cost-bar__fill"
                  style={{
                    width: `${coordPct}%`,
                    background: color,
                  }}
                />
              </div>
            </div>
          </div>
        );
      })}

      {/* Total row */}
      <div className="grid grid-cols-[1fr_120px_120px_120px_200px] gap-0 items-center py-3 border-t-2 border-black mt-0">
        <div className="font-mono text-[13px] font-bold uppercase">Total</div>
        <div className="font-mono text-[14px] font-bold text-right text-[var(--color-cost)]">
          {formatCurrencyFull(totalFragmented)}
        </div>
        <div className="font-mono text-[14px] font-bold text-right">
          {formatCurrencyFull(totalCoordinated)}
        </div>
        <div className="font-mono text-[14px] font-bold text-right text-[var(--color-savings)]">
          {formatCurrencyFull(totalSavings)}
        </div>
        <div />
      </div>

      {/* Domain summary bar chart */}
      <div className="mt-8">
        <div className="section-label mb-4">Costs by Domain</div>
        <div className="space-y-3">
          {domains.map((d) => {
            const fragPct = totalFragmented > 0 ? (d.annual_cost / totalFragmented) * 100 : 0;
            const coordPct = totalFragmented > 0 ? (d.coordinated_cost / totalFragmented) * 100 : 0;
            const color = DOMAIN_COLORS[d.domain] || '#666';

            return (
              <div key={d.domain}>
                <div className="flex items-center justify-between mb-1">
                  <DomainBadge domain={d.domain} label={d.domain_label} />
                  <span className="font-mono text-[12px] text-[var(--color-text-secondary)]">
                    {formatCurrencyFull(d.annual_cost)}
                    <span className="text-[var(--color-text-tertiary)]"> &rarr; </span>
                    {formatCurrencyFull(d.coordinated_cost)}
                  </span>
                </div>
                <div className="relative h-[32px] bg-[var(--color-surface-alt)]">
                  {/* Fragmented bar (faded) */}
                  <div
                    className="absolute left-0 top-0 bottom-0 opacity-30"
                    style={{
                      width: `${fragPct}%`,
                      background: color,
                    }}
                  />
                  {/* Coordinated bar (solid) */}
                  <div
                    className="absolute left-0 top-0 bottom-0"
                    style={{
                      width: `${coordPct}%`,
                      background: color,
                      transition: 'width 0.6s ease-out',
                    }}
                  />
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
