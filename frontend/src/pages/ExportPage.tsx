import { useLocation, Link } from 'react-router-dom';
import type { MatchResult, MatchedProvision, Domain } from '../types';
import { DOMAIN_LABELS } from '../types';

export function ExportPage() {
  const location = useLocation();
  const matchResult = (location.state as { matchResult?: MatchResult } | null)
    ?.matchResult;

  if (!matchResult) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[calc(100vh-4rem)] px-4 text-center">
        <h1 className="font-serif text-3xl mb-4">No report available</h1>
        <p className="text-black/60 mb-8 max-w-md">
          Submit your circumstances first to generate a printable rights report.
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

  const grouped = matches.reduce<Record<string, MatchedProvision[]>>(
    (acc, p) => {
      if (!acc[p.domain]) acc[p.domain] = [];
      acc[p.domain].push(p);
      return acc;
    },
    {}
  );

  const domainOrder: Domain[] = [
    'health',
    'civil_rights',
    'housing',
    'income',
    'education',
    'justice',
  ];

  const today = new Date().toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  });

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 py-12 export-page">
      {/* Print button - hidden in print */}
      <div className="print-hide mb-8 flex items-center gap-4">
        <button
          onClick={() => window.print()}
          className="border-2 border-black bg-black text-white px-6 py-3 text-base font-medium cursor-pointer hover:bg-white hover:text-black transition-colors"
          aria-label="Print this report"
        >
          Print This Report
        </button>
        <Link
          to="/dome"
          state={{ matchResult }}
          className="text-sm text-black/60 no-underline hover:text-black hover:underline"
        >
          Back to Dome View
        </Link>
      </div>

      {/* Report header */}
      <header className="border-b-2 border-black pb-6 mb-8">
        <h1 className="font-serif text-3xl sm:text-4xl mb-2">
          DOMES Legal Rights Report
        </h1>
        <p className="text-sm text-black/60 mb-1">
          Generated {today}
        </p>
        <p className="text-sm text-black/60">
          {total_matched} provisions identified
        </p>
      </header>

      {/* Circumstances summary */}
      <section className="mb-10" aria-label="Circumstances summary">
        <h2 className="font-serif text-xl mb-3 border-b border-border pb-2">
          Circumstances
        </h2>
        <p className="text-sm leading-relaxed">{profileSummary}</p>
      </section>

      {/* Provisions by domain */}
      {domainOrder.map((domain) => {
        const domainProvisions = grouped[domain];
        if (!domainProvisions || domainProvisions.length === 0) return null;

        return (
          <section
            key={domain}
            className="mb-10 page-break-inside-avoid"
            aria-label={`${DOMAIN_LABELS[domain]} provisions`}
          >
            <h2 className="font-serif text-xl mb-4 border-b border-border pb-2">
              {DOMAIN_LABELS[domain]}
              <span className="text-sm font-sans text-black/40 ml-3">
                {domainProvisions.length} provision{domainProvisions.length !== 1 ? 's' : ''}
              </span>
            </h2>

            <div className="space-y-6">
              {domainProvisions.map((provision) => (
                <article
                  key={provision.provision_id}
                  className="border-l-2 border-black pl-4 page-break-inside-avoid"
                >
                  <p className="font-mono text-xs text-black/50 mb-0.5">
                    {provision.citation}
                  </p>
                  <h3 className="font-serif text-base font-medium mb-2">
                    {provision.title}
                  </h3>

                  {provision.match_reasons.length > 0 && (
                    <p className="text-sm leading-relaxed mb-3 text-black/70">
                      Applies because: {provision.match_reasons.join('; ')}
                    </p>
                  )}

                  <div className="flex gap-3 mb-3 text-xs">
                    <span className="font-medium uppercase tracking-wider text-black/50">
                      {provision.provision_type}
                    </span>
                  </div>

                  {provision.enforcement_steps.length > 0 && (
                    <div className="mb-2">
                      <p className="text-xs font-medium uppercase tracking-wider text-black/40 mb-1">
                        Enforcement Steps
                      </p>
                      <ul className="text-sm space-y-0.5">
                        {provision.enforcement_steps.map((step, i) => (
                          <li key={i} className="flex items-start gap-2">
                            <span className="text-black/30">&mdash;</span>
                            {step}
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}
                </article>
              ))}
            </div>
          </section>
        );
      })}

      {/* Gaps section */}
      {gaps.length > 0 && (
        <section className="mb-10 page-break-inside-avoid" aria-label="Coverage gaps">
          <h2 className="font-serif text-xl mb-4 border-b border-border pb-2">
            Potential Coverage Gaps
            <span className="text-sm font-sans text-black/40 ml-3">
              {gaps.length} identified
            </span>
          </h2>
          <div className="space-y-6">
            {gaps.map((gap) => (
              <article
                key={gap.provision_id}
                className="border-l-2 border-domain-education pl-4 page-break-inside-avoid"
              >
                <p className="font-mono text-xs text-black/50 mb-0.5">
                  {gap.citation}
                </p>
                <h3 className="font-serif text-base font-medium mb-2">
                  {gap.title}
                </h3>
                {gap.match_reasons.length > 0 && (
                  <p className="text-sm leading-relaxed mb-2 text-black/70">
                    {gap.match_reasons.join('; ')}
                  </p>
                )}
                {gap.enforcement_steps.length > 0 && (
                  <ul className="text-sm space-y-0.5">
                    {gap.enforcement_steps.map((step, i) => (
                      <li key={i} className="flex items-start gap-2">
                        <span className="text-black/30">&mdash;</span>
                        {step}
                      </li>
                    ))}
                  </ul>
                )}
              </article>
            ))}
          </div>
        </section>
      )}

      {/* Disclaimer footer */}
      <footer className="border-t-2 border-black pt-6 mt-12">
        <p className="text-xs text-black/40 leading-relaxed">
          This report provides legal information, not legal advice. The provisions listed
          are based on federal law and may not reflect the most recent amendments or
          state-specific variations. This report does not create an attorney-client
          relationship. For legal advice specific to your situation, consult a qualified
          attorney. Generated by DOMES on {today}.
        </p>
      </footer>
    </div>
  );
}
