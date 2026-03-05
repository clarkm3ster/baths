import { useState, useRef, useEffect, useCallback } from 'react';
import { useLocation, Link } from 'react-router-dom';
import ProvisionDetail from '../components/ProvisionDetail';
import DomeVisualization from '../components/DomeVisualization';
import type { MatchResult, MatchedProvision, Domain, ExplanationResult } from '../types';
import { DOMAIN_COLORS, DOMAIN_LABELS } from '../types';
import { explainProvision } from '../api/client';

export function DomeViewPage() {
  const location = useLocation();
  const matchResult = (location.state as { matchResult?: MatchResult } | null)
    ?.matchResult;

  const [selectedProvision, setSelectedProvision] = useState<MatchedProvision | null>(
    null
  );
  const [explanation, setExplanation] = useState<ExplanationResult | undefined>();
  const [explanationLoading, setExplanationLoading] = useState(false);
  const [gapView, setGapView] = useState(false);
  const [domainFilter, setDomainFilter] = useState<Domain | 'all'>('all');
  const statusRef = useRef<HTMLDivElement>(null);

  const handleProvisionSelect = useCallback((provision: MatchedProvision) => {
    setSelectedProvision(provision);
    setExplanation(undefined);
    setExplanationLoading(true);
    const profileData = matchResult?.profile ?? {};
    explainProvision(provision.provision_id, profileData as Record<string, unknown>)
      .then(setExplanation)
      .catch(() => { /* explanation unavailable; show fallback */ })
      .finally(() => setExplanationLoading(false));
  }, [matchResult]);

  const displayItems = gapView
    ? matchResult?.gaps ?? []
    : matchResult?.matches ?? [];

  const filteredCount = domainFilter === 'all'
    ? displayItems.length
    : displayItems.filter((p) => p.domain === domainFilter).length;

  useEffect(() => {
    if (statusRef.current) {
      statusRef.current.textContent = filteredCount > 0
        ? `Showing ${filteredCount} provisions${domainFilter !== 'all' ? ` in ${DOMAIN_LABELS[domainFilter]}` : ''}`
        : '';
    }
  }, [filteredCount, domainFilter]);

  if (!matchResult) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[calc(100vh-4rem)] px-4 text-center">
        <h1 className="font-serif text-3xl mb-4">No provisions mapped</h1>
        <p className="text-black/60 mb-8 max-w-md">
          Submit your circumstances to see the legal provisions that apply to
          you.
        </p>
        <Link
          to="/circumstances"
          className="inline-block border-2 border-black bg-black text-white px-6 py-3 text-base font-medium no-underline hover:bg-white hover:text-black transition-colors"
        >
          Map Your Rights
        </Link>
      </div>
    );
  }

  const { matches, gaps, profile, total_matched } = matchResult;

  const provisions = gapView ? gaps : matches;

  const domains = Object.entries(
    provisions.reduce<Record<string, MatchedProvision[]>>((acc, p) => {
      if (!acc[p.domain]) acc[p.domain] = [];
      acc[p.domain].push(p);
      return acc;
    }, {})
  ).sort(([a], [b]) => a.localeCompare(b));

  const filteredProvisions =
    domainFilter === 'all'
      ? provisions
      : provisions.filter((p) => p.domain === domainFilter);

  const profileParts: string[] = [
    ...profile.insurance,
    ...profile.disabilities,
    ...(profile.age_group ? [profile.age_group] : []),
    ...(profile.pregnant ? ['pregnant'] : []),
    ...profile.housing,
    ...profile.income,
    ...profile.system_involvement,
    ...(profile.veteran ? ['veteran'] : []),
    ...(profile.dv_survivor ? ['dv survivor'] : []),
    ...(profile.immigrant ? ['immigrant'] : []),
    ...(profile.lgbtq ? ['lgbtq+'] : []),
    ...(profile.rural ? ['rural'] : []),
    ...(profile.state ? [profile.state] : []),
  ];
  const profileSummary = profileParts
    .map((s) => s.replace(/_/g, ' '))
    .join(', ');

  return (
    <div className="flex flex-col lg:flex-row min-h-[calc(100vh-4rem)]">
      {/* Main content */}
      <div className={`flex-1 ${selectedProvision ? 'lg:mr-[440px]' : ''}`}>
        {/* Header */}
        <header className="border-b border-border px-4 sm:px-6 py-6">
          <div className="max-w-6xl mx-auto">
            <h1 className="font-serif text-2xl sm:text-3xl mb-2">
              Your Legal Architecture
            </h1>
            <p className="text-sm text-black/60 mb-4 max-w-2xl">
              {total_matched} provisions identified across{' '}
              {domains.length} domains for: {profileSummary}
            </p>
            <div className="flex flex-wrap items-center gap-4">
              {/* Domain filter pills */}
              <div className="flex flex-wrap gap-2" role="group" aria-label="Filter by domain">
                <button
                  onClick={() => setDomainFilter('all')}
                  className={`text-xs font-medium px-3 py-1.5 border cursor-pointer transition-colors ${
                    domainFilter === 'all'
                      ? 'bg-black text-white border-black'
                      : 'border-border hover:border-black'
                  }`}
                >
                  All ({provisions.length})
                </button>
                {domains.map(([domain, domainProvisions]) => (
                  <button
                    key={domain}
                    onClick={() => setDomainFilter(domain as Domain)}
                    className={`text-xs font-medium px-3 py-1.5 border cursor-pointer transition-colors ${
                      domainFilter === domain
                        ? 'text-white border-transparent'
                        : 'border-border hover:border-black'
                    }`}
                    style={
                      domainFilter === domain
                        ? { backgroundColor: DOMAIN_COLORS[domain as Domain] }
                        : undefined
                    }
                  >
                    {DOMAIN_LABELS[domain as Domain]} ({domainProvisions.length})
                  </button>
                ))}
              </div>

              <div className="flex items-center gap-4 ml-auto">
                {/* Gap view toggle */}
                <label className="flex items-center gap-2 text-sm cursor-pointer">
                  <input
                    type="checkbox"
                    checked={gapView}
                    onChange={(e) => setGapView(e.target.checked)}
                    className="w-4 h-4 accent-black"
                  />
                  Gap View{gaps.length > 0 && ` (${gaps.length})`}
                </label>

                {/* Export link */}
                <Link
                  to="/export"
                  state={{ matchResult }}
                  className="text-xs border border-border px-3 py-1.5 hover:border-black no-underline text-black transition-colors"
                  aria-label="Export provisions as printable report"
                >
                  Export
                </Link>
              </div>
            </div>
          </div>
        </header>

        {gapView && (
          <div className="border-b border-border px-4 sm:px-6 py-4 bg-black/[0.02]">
            <div className="max-w-6xl mx-auto">
              <p className="text-sm text-black/60">
                <span className="font-medium text-black">Gap View</span> — Areas
                where provisions may be missing or where additional protections
                could apply are highlighted below. This analysis is preliminary.
              </p>
            </div>
          </div>
        )}

        {/* Screen reader status for dynamic content */}
        <div
          ref={statusRef}
          className="sr-only"
          aria-live="polite"
          aria-atomic="true"
        />

        {/* Dome visualization */}
        <div className="max-w-6xl mx-auto px-4 sm:px-6 pt-8">
          <DomeVisualization
            provisions={matches}
            gaps={gaps}
            showGaps={gapView}
            onProvisionClick={handleProvisionSelect}
            selectedProvision={selectedProvision ?? undefined}
          />
        </div>

        {/* Provisions grid */}
        <div className="max-w-6xl mx-auto px-4 sm:px-6 py-8">
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-0">
            {filteredProvisions.map((provision) => (
              <button
                key={provision.provision_id}
                onClick={() => handleProvisionSelect(provision)}
                className={`text-left p-5 border border-border cursor-pointer transition-colors hover:bg-black/[0.02] -mt-px -ml-px ${
                  selectedProvision?.provision_id === provision.provision_id
                    ? 'bg-black/[0.03] border-black z-10 relative'
                    : ''
                }`}
                aria-label={`View details for ${provision.title}`}
              >
                <div
                  className="w-full h-0.5 mb-3"
                  style={{ backgroundColor: DOMAIN_COLORS[provision.domain as Domain] }}
                />
                <p className="font-mono text-xs text-black/50 mb-1 truncate">
                  {provision.citation}
                </p>
                <h3 className="font-serif text-sm font-medium mb-2 line-clamp-2">
                  {provision.title}
                </h3>
                {provision.match_reasons.length > 0 && (
                  <p className="text-xs text-black/50 line-clamp-2">
                    {provision.match_reasons.join('; ')}
                  </p>
                )}
                <div className="flex items-center gap-2 mt-3">
                  <span
                    className="w-2 h-2 inline-block"
                    style={{ backgroundColor: DOMAIN_COLORS[provision.domain as Domain] }}
                  />
                  <span className="text-xs text-black/40 uppercase tracking-wider">
                    {DOMAIN_LABELS[provision.domain as Domain]}
                  </span>
                  <span className="text-xs text-black/30 ml-auto uppercase tracking-wider">
                    {provision.provision_type}
                  </span>
                </div>
              </button>
            ))}
          </div>

          {filteredProvisions.length === 0 && (
            <p className="text-center text-black/40 py-16">
              {gapView
                ? 'No coverage gaps identified for this filter.'
                : 'No provisions found for this filter.'}
            </p>
          )}
        </div>
      </div>

      {/* Detail sidebar */}
      {selectedProvision && (
        <aside
          className="fixed top-16 right-0 bottom-0 w-full lg:w-[440px] bg-white border-l border-border overflow-y-auto z-20"
          role="complementary"
          aria-label="Provision details"
        >
          <ProvisionDetail
            provision={selectedProvision}
            explanation={explanation}
            loading={explanationLoading}
            onClose={() => {
              setSelectedProvision(null);
              setExplanation(undefined);
            }}
          />
        </aside>
      )}
    </div>
  );
}
