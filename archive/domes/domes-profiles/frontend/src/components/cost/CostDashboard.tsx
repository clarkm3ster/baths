/**
 * CostDashboard — the full cost analysis page for a profile.
 *
 * System-by-system breakdown, domain bar charts, avoidable events,
 * scale calculator, and ROI calculator.
 */

import { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { getProfile, getAvoidableEvents } from '../../api/client';
import type { Profile, AvoidableEvent } from '../../types';
import CostDisplay, { formatCurrencyFull, formatCurrency } from '../shared/CostDisplay';
import StatBlock from '../shared/StatBlock';
import CostBreakdown from './CostBreakdown';
import SavingsCalculator from './SavingsCalculator';

export default function CostDashboard() {
  const { id } = useParams<{ id: string }>();
  const [profile, setProfile] = useState<Profile | null>(null);
  const [events, setEvents] = useState<AvoidableEvent[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    if (!id) return;
    setLoading(true);
    Promise.all([
      getProfile(id),
      getAvoidableEvents().catch(() => []),
    ])
      .then(([p, e]) => {
        setProfile(p);
        setEvents(e);
      })
      .catch((err) => setError(err instanceof Error ? err.message : 'Failed to load'))
      .finally(() => setLoading(false));
  }, [id]);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-[calc(100vh-80px)]">
        <div className="loading-pulse" />
      </div>
    );
  }

  if (error || !profile) {
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

  const fragmented = profile.total_annual_cost;
  const coordinated = profile.coordinated_annual_cost;
  const savings = profile.savings_annual;

  return (
    <div className="max-w-[1200px] mx-auto px-6 py-10">
      {/* Header */}
      <div className="flex items-start justify-between mb-8">
        <div>
          <div className="section-label mb-1">Cost analysis</div>
          <h1 className="font-serif text-[32px] font-bold">
            {profile.name || 'Profile'}
          </h1>
        </div>
        <div className="flex gap-2">
          <Link to={`/dome/${id}`} className="btn btn--small">
            View Dome
          </Link>
          <Link to={`/timeline/${id}`} className="btn btn--small">
            Timeline
          </Link>
          <button onClick={() => window.print()} className="btn btn--small">
            Export PDF
          </button>
        </div>
      </div>

      {/* ── Hero stats row ── */}
      <div className="grid grid-cols-2 sm:grid-cols-5 gap-0 border-2 border-black mb-10">
        <div className="p-5 border-r border-[var(--color-border)]">
          <CostDisplay
            value={fragmented}
            label="Fragmented annual"
            size="medium"
            mode="cost"
          />
        </div>
        <div className="p-5 border-r border-[var(--color-border)]">
          <CostDisplay
            value={coordinated}
            label="Coordinated annual"
            size="medium"
          />
        </div>
        <div className="p-5 border-r border-[var(--color-border)]">
          <CostDisplay
            value={savings}
            label="Annual savings"
            size="medium"
            mode="savings"
          />
        </div>
        <div className="p-5 border-r border-[var(--color-border)]">
          <CostDisplay
            value={profile.five_year_projection}
            label="5-year projection"
            size="medium"
            mode="savings"
          />
        </div>
        <div className="p-5">
          <StatBlock
            value={String(profile.systems_involved?.length ?? 0)}
            label="Systems involved"
          />
        </div>
      </div>

      {/* ── System-by-system breakdown ── */}
      <div className="mb-12">
        <CostBreakdown
          domains={profile.domains || []}
          totalFragmented={fragmented}
          totalCoordinated={coordinated}
          totalSavings={savings}
        />
      </div>

      {/* ── Avoidable events ── */}
      {events.length > 0 && (
        <div className="mb-12">
          <div className="section-label mb-4">Avoidable Cost Events</div>
          <p className="text-[13px] text-[var(--color-text-secondary)] mb-4">
            Specific high-cost events that coordination would reduce or eliminate.
          </p>

          <div className="border-2 border-black">
            {/* Header */}
            <div className="grid grid-cols-[1fr_100px_100px_100px_100px] gap-0 px-4 py-2 border-b-2 border-black bg-[var(--color-surface)]">
              <div className="font-mono text-[11px] uppercase tracking-wider text-[var(--color-text-tertiary)]">
                Event
              </div>
              <div className="font-mono text-[11px] uppercase tracking-wider text-[var(--color-text-tertiary)] text-right">
                Cost/event
              </div>
              <div className="font-mono text-[11px] uppercase tracking-wider text-[var(--color-text-tertiary)] text-right">
                Freq/yr
              </div>
              <div className="font-mono text-[11px] uppercase tracking-wider text-[var(--color-text-tertiary)] text-right">
                Avoidable %
              </div>
              <div className="font-mono text-[11px] uppercase tracking-wider text-[var(--color-text-tertiary)] text-right">
                Savings
              </div>
            </div>

            {events.map((evt) => (
              <div
                key={evt.id}
                className="grid grid-cols-[1fr_100px_100px_100px_100px] gap-0 px-4 py-3 border-b border-[var(--color-border)]"
              >
                <div>
                  <span className="text-[13px]">{evt.label}</span>
                  <span className="citation-tag ml-2">{evt.source}</span>
                </div>
                <div className="font-mono text-[13px] text-right">
                  {formatCurrencyFull(evt.cost_per_event)}
                </div>
                <div className="font-mono text-[13px] text-right">
                  {evt.annual_frequency}
                </div>
                <div className="font-mono text-[13px] text-right">
                  {Math.round(evt.avoidable_pct * 100)}%
                </div>
                <div className="font-mono text-[13px] text-right text-[var(--color-savings)]">
                  {formatCurrencyFull(evt.avoidable_savings)}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* ── Scale & ROI calculators ── */}
      <SavingsCalculator perPersonSavings={savings} />

      {/* ── Narrative ── */}
      {profile.narrative && (
        <div className="mt-12 pt-8 border-t-2 border-black">
          <div className="section-label mb-3">Profile Narrative</div>
          <p className="text-[14px] text-[var(--color-text-secondary)] leading-relaxed max-w-[800px]">
            {profile.narrative}
          </p>
        </div>
      )}
    </div>
  );
}
