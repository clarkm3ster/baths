/**
 * DomePage — the centerpiece page.
 *
 * Fetches dome data for a profile, renders the full-screen dome view
 * with a top control bar, center DomeVisualization (from dome-renderer),
 * bottom cost summary, and a slide-in side panel for details.
 */

import { useEffect, useState, useCallback } from 'react';
import { useParams, Link } from 'react-router-dom';
import { getDomeData } from '../../api/client';
import type { DomeData, DomeMode } from '../../types';
import type { DomeDomain } from './types';
import DomeVisualization from './DomeVisualization';
import { formatCurrencyFull } from '../shared/CostDisplay';
import DomainBadge from '../shared/DomainBadge';

export default function DomePage() {
  const { id } = useParams<{ id: string }>();
  const [data, setData] = useState<DomeData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [mode, setMode] = useState<DomeMode>('fragmented');
  const [selectedDomain, setSelectedDomain] = useState<DomeDomain | null>(null);

  useEffect(() => {
    if (!id) return;
    setLoading(true);
    getDomeData(id)
      .then((d) => {
        setData(d);
        setError('');
      })
      .catch((err) => setError(err instanceof Error ? err.message : 'Failed to load'))
      .finally(() => setLoading(false));
  }, [id]);

  const handleDomainClick = useCallback((domain: DomeDomain) => {
    setSelectedDomain((prev) => (prev?.domain === domain.domain ? null : domain));
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-[calc(100vh-80px)]">
        <div className="loading-pulse" />
      </div>
    );
  }

  if (error || !data) {
    return (
      <div className="flex items-center justify-center h-[calc(100vh-80px)]">
        <div className="text-center">
          <p className="font-mono text-[var(--color-cost)] text-[14px] mb-4">
            {error || 'Profile not found'}
          </p>
          <Link to="/profiles" className="btn btn--small">
            Back to Profiles
          </Link>
        </div>
      </div>
    );
  }

  const { profile, domains, totals, connections } = data;
  const fragmented = totals.annual_cost;
  const coordinated = totals.coordinated_cost;
  const savings = totals.savings;

  return (
    <div className="flex flex-col h-[calc(100vh-80px)]">
      {/* ── Top control bar ── */}
      <div className="border-b-2 border-black px-6 py-3 flex items-center justify-between bg-white shrink-0">
        <div className="flex items-center gap-4">
          <h1 className="font-serif text-[22px] font-bold">
            {profile.name || 'Profile'}
          </h1>
          <span className="font-mono text-[11px] text-[var(--color-text-tertiary)] uppercase">
            v{profile.version}
          </span>
        </div>

        <div className="flex items-center gap-4">
          {/* Mode toggle */}
          <div className="mode-toggle">
            <button
              className={`mode-toggle__option ${mode === 'fragmented' ? 'mode-toggle__option--active' : ''}`}
              onClick={() => setMode('fragmented')}
            >
              Fragmented
            </button>
            <button
              className={`mode-toggle__option ${mode === 'coordinated' ? 'mode-toggle__option--active' : ''}`}
              onClick={() => setMode('coordinated')}
            >
              Coordinated
            </button>
          </div>

          {/* Action links */}
          <Link to={`/cost/${id}`} className="btn btn--small">
            Cost Detail
          </Link>
          <Link to={`/timeline/${id}`} className="btn btn--small">
            Timeline
          </Link>
          <button onClick={() => window.print()} className="btn btn--small">
            Export PDF
          </button>
        </div>
      </div>

      {/* ── Center: Dome visualization ── */}
      <div className="flex-1 relative overflow-hidden bg-white">
        <DomeVisualization
          domains={domains}
          connections={connections}
          totals={totals}
          mode={mode}
          onDomainClick={handleDomainClick}
        />
      </div>

      {/* ── Bottom cost summary bar ── */}
      <div className="border-t-2 border-black px-6 py-4 bg-[var(--color-surface)] shrink-0">
        <div className="max-w-[1200px] mx-auto flex items-center justify-between">
          <div className="flex items-center gap-8">
            <div>
              <span className="section-label">Fragmented</span>
              <span className="font-mono text-[24px] font-medium text-[var(--color-cost)] ml-3">
                {formatCurrencyFull(fragmented)}
              </span>
            </div>

            <span className="font-mono text-[20px] text-[var(--color-text-tertiary)]">
              &rarr;
            </span>

            <div>
              <span className="section-label">Coordinated</span>
              <span className="font-mono text-[24px] font-medium ml-3">
                {formatCurrencyFull(coordinated)}
              </span>
            </div>
          </div>

          <div className="border-l-2 border-black pl-8">
            <span className="section-label">Savings</span>
            <span className="font-mono text-[28px] font-medium text-[var(--color-savings)] ml-3">
              {formatCurrencyFull(savings)}
              <span className="text-[14px] text-[var(--color-text-tertiary)]">/yr</span>
            </span>
          </div>
        </div>
      </div>

      {/* ── Side panel (domain detail) ── */}
      {selectedDomain && (
        <>
          <div
            className="detail-overlay"
            onClick={() => setSelectedDomain(null)}
          />
          <div className="detail-panel">
            <DomainDetailPanel
              domain={selectedDomain}
              mode={mode}
              onClose={() => setSelectedDomain(null)}
            />
          </div>
        </>
      )}
    </div>
  );
}

// ---------------------------------------------------------------------------
// Domain detail side panel
// ---------------------------------------------------------------------------

function DomainDetailPanel({
  domain,
  mode,
  onClose,
}: {
  domain: DomeDomain;
  mode: DomeMode;
  onClose: () => void;
}) {
  const cost = mode === 'fragmented' ? domain.annual_cost : domain.coordinated_cost;

  return (
    <div className="p-6">
      {/* Header */}
      <div className="flex items-start justify-between mb-6">
        <div>
          <DomainBadge domain={domain.domain} label={domain.label} />
          <h2 className="font-serif text-[24px] font-bold mt-2">{domain.label}</h2>
        </div>
        <button onClick={onClose} className="btn btn--small">
          Close
        </button>
      </div>

      {/* Cost summary */}
      <div className="grid grid-cols-3 gap-4 mb-6 pb-6 border-b border-[var(--color-border)]">
        <div>
          <div className="section-label">Current cost</div>
          <div className="font-mono text-[20px] font-medium">
            {formatCurrencyFull(cost)}
          </div>
        </div>
        <div>
          <div className="section-label">Savings</div>
          <div className="font-mono text-[20px] font-medium text-[var(--color-savings)]">
            {formatCurrencyFull(domain.savings)}
          </div>
        </div>
        <div>
          <div className="section-label">Systems</div>
          <div className="font-mono text-[20px] font-medium">
            {domain.systems.length}
          </div>
        </div>
      </div>

      {/* Systems list */}
      <div className="mb-6">
        <div className="section-label mb-3">Systems involved</div>
        <div className="space-y-2">
          {domain.systems.map((sys) => (
            <div
              key={sys.id}
              className="flex items-center justify-between py-2 px-3 border border-[var(--color-border)]"
            >
              <div>
                <span className="font-mono text-[12px] font-medium">{sys.acronym}</span>
                <span className="text-[13px] ml-2">{sys.name}</span>
              </div>
              <span className="font-mono text-[13px] text-[var(--color-text-secondary)]">
                {formatCurrencyFull(mode === 'fragmented' ? sys.annual_cost : sys.coordinated_cost)}
              </span>
            </div>
          ))}
        </div>
      </div>

      {/* Gaps */}
      {domain.gaps.length > 0 && (
        <div className="mb-6">
          <div className="section-label mb-3">
            Gaps ({domain.gaps.length})
          </div>
          <div className="space-y-2">
            {domain.gaps.map((gap) => (
              <div
                key={gap.id}
                className="py-2 px-3 border border-[var(--color-border)]"
              >
                <div className="flex items-center justify-between">
                  <span className="text-[13px] font-medium">
                    {gap.system_a} &harr; {gap.system_b}
                  </span>
                  <span className={`font-mono text-[11px] uppercase ${
                    gap.severity === 'critical'
                      ? 'text-[var(--color-cost)]'
                      : 'text-[var(--color-text-tertiary)]'
                  }`}>
                    {gap.severity}
                  </span>
                </div>
                <div className="text-[12px] text-[var(--color-text-secondary)] mt-1">
                  {gap.barrier_type}
                  {gap.consent_closable && (
                    <span className="ml-2 text-[var(--color-savings)]">
                      consent-closable
                    </span>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Bridges */}
      {domain.bridges.length > 0 && (
        <div className="mb-6">
          <div className="section-label mb-3">
            Bridges ({domain.bridges.length})
          </div>
          <div className="space-y-2">
            {domain.bridges.map((bridge) => (
              <div
                key={bridge.id}
                className="py-2 px-3 border border-[var(--color-border)]"
              >
                <div className="text-[13px] font-medium">{bridge.title}</div>
                <div className="flex items-center gap-3 mt-1 text-[12px] text-[var(--color-text-secondary)]">
                  <span>{bridge.bridge_type}</span>
                  <span className="font-mono">Priority: {bridge.priority_score}</span>
                  <span className="font-mono">{bridge.estimated_cost}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Provisions */}
      {domain.top_provisions.length > 0 && (
        <div>
          <div className="section-label mb-3">
            Legal provisions ({domain.provisions_count})
          </div>
          <div className="space-y-1">
            {domain.top_provisions.map((prov, i) => (
              <div
                key={i}
                className="py-2 px-3 border border-[var(--color-border)] text-[12px]"
              >
                <span className="citation-tag mr-2">{prov.citation}</span>
                <span className="text-[var(--color-text-secondary)]">
                  {prov.title}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
