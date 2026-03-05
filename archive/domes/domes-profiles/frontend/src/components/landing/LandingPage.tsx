import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { listProfiles } from '../../api/client';
import type { Profile } from '../../types';
import CostDisplay, { formatCurrency } from '../shared/CostDisplay';
import DomainBadge from '../shared/DomainBadge';

/** Pre-computed averages for the hero stats (updated from API if available) */
const HERO_STATS = {
  fragmented: 79_000,
  coordinated: 31_000,
  savings: 48_000,
};

export default function LandingPage() {
  const [samples, setSamples] = useState<Profile[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    listProfiles({ is_sample: true, limit: 3 })
      .then(setSamples)
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="min-h-[calc(100vh-80px)]">
      {/* ── Hero ── */}
      <section className="border-b-2 border-black">
        <div className="max-w-[1100px] mx-auto px-6 py-20">
          <h1 className="font-serif text-[56px] leading-[1.05] font-bold max-w-[900px]">
            Every system. Every dollar. Every gap. One&nbsp;person.
          </h1>
          <p className="font-sans text-[18px] text-[var(--color-text-secondary)] mt-6 max-w-[700px]">
            DOMES maps the total architecture of government around a single person&nbsp;&mdash;
            every system involved, every dollar spent, every gap between them, and every
            dollar that coordination could&nbsp;save.
          </p>
        </div>
      </section>

      {/* ── Big stat row ── */}
      <section className="border-b-2 border-black bg-[var(--color-surface)]">
        <div className="max-w-[1100px] mx-auto px-6 py-12">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-12">
            <div>
              <div className="section-label">Average cost fragmented</div>
              <div className="font-mono text-[48px] font-medium leading-none text-[var(--color-cost)]">
                {formatCurrency(HERO_STATS.fragmented)}
              </div>
              <div className="text-[12px] text-[var(--color-text-tertiary)] mt-1">
                per person per year
              </div>
            </div>
            <div>
              <div className="section-label">Coordinated cost</div>
              <div className="font-mono text-[48px] font-medium leading-none">
                {formatCurrency(HERO_STATS.coordinated)}
              </div>
              <div className="text-[12px] text-[var(--color-text-tertiary)] mt-1">
                per person per year
              </div>
            </div>
            <div>
              <div className="section-label">Savings per person</div>
              <div className="font-mono text-[48px] font-medium leading-none text-[var(--color-savings)]">
                {formatCurrency(HERO_STATS.savings)}
              </div>
              <div className="text-[12px] text-[var(--color-text-tertiary)] mt-1">
                per person per year
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* ── Call to action ── */}
      <section className="border-b-2 border-black">
        <div className="max-w-[1100px] mx-auto px-6 py-12 flex flex-col sm:flex-row items-start gap-4">
          <Link to="/intake" className="btn btn--primary">
            Build a Profile
          </Link>
          <Link to="/profiles" className="btn">
            Browse Profiles
          </Link>
        </div>
      </section>

      {/* ── Sample profiles ── */}
      <section>
        <div className="max-w-[1100px] mx-auto px-6 py-12">
          <div className="section-label mb-6">Sample Profiles</div>

          {loading ? (
            <div className="flex items-center justify-center py-20">
              <div className="loading-pulse" />
            </div>
          ) : samples.length === 0 ? (
            <p className="text-[var(--color-text-tertiary)] text-[13px]">
              No sample profiles available. Build one to get started.
            </p>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-3 gap-0">
              {samples.map((profile) => (
                <SampleCard key={profile.id} profile={profile} />
              ))}
            </div>
          )}
        </div>
      </section>
    </div>
  );
}

// ---------------------------------------------------------------------------
// Sample card
// ---------------------------------------------------------------------------

function SampleCard({ profile }: { profile: Profile }) {
  const circumstances = Object.entries(profile.circumstances)
    .filter(([, v]) => v === true)
    .map(([k]) => k);

  // Determine domains from circumstances
  const domainKeys = Array.from(
    new Set(
      profile.domains?.map((d) => d.domain) ?? []
    )
  ).slice(0, 3);

  return (
    <Link
      to={`/dome/${profile.id}`}
      className="border-2 border-black p-6 -ml-[2px] first:ml-0 hover:bg-[var(--color-surface)] transition-colors block"
    >
      <h3 className="font-serif text-[20px] font-bold mb-3">
        {profile.name || 'Unnamed Profile'}
      </h3>

      {/* Domain badges */}
      <div className="flex flex-wrap gap-2 mb-4">
        {domainKeys.map((d) => (
          <DomainBadge key={d} domain={d} />
        ))}
      </div>

      {/* Key circumstances */}
      <div className="mb-4">
        <div className="text-[11px] text-[var(--color-text-tertiary)] font-mono uppercase tracking-wider mb-1">
          Circumstances
        </div>
        <div className="flex flex-wrap gap-1">
          {circumstances.slice(0, 5).map((c) => (
            <span
              key={c}
              className="text-[11px] font-mono px-2 py-[2px] border border-[var(--color-border)] text-[var(--color-text-secondary)]"
            >
              {c.replace(/^(has_|is_)/, '').replace(/_/g, ' ')}
            </span>
          ))}
          {circumstances.length > 5 && (
            <span className="text-[11px] font-mono text-[var(--color-text-tertiary)]">
              +{circumstances.length - 5}
            </span>
          )}
        </div>
      </div>

      {/* Cost summary */}
      <div className="grid grid-cols-2 gap-4 pt-4 border-t border-[var(--color-border)]">
        <CostDisplay
          value={profile.total_annual_cost}
          label="Annual cost"
          size="small"
          mode="cost"
        />
        <CostDisplay
          value={profile.savings_annual}
          label="Savings"
          size="small"
          mode="savings"
          suffix="/yr"
        />
      </div>
    </Link>
  );
}
