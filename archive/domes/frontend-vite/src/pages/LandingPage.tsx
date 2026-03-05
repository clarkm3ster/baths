import { Link } from 'react-router-dom';

export function LandingPage() {
  return (
    <div className="flex flex-col min-h-[calc(100vh-4rem)]">
      <section className="flex-1 flex flex-col items-center justify-center max-w-3xl mx-auto px-4 sm:px-6 py-16 sm:py-24 text-center">
        <h1 className="font-serif text-4xl sm:text-5xl lg:text-6xl leading-tight mb-6">
          The Capitol dome houses America&rsquo;s legal architecture.
        </h1>
        <p className="font-serif text-xl sm:text-2xl text-black/70 mb-8">
          DOMES rebuilds it around you.
        </p>
        <p className="text-base sm:text-lg text-black/60 max-w-2xl mb-12 leading-relaxed">
          Every person in the United States exists at an intersection of federal statutes,
          regulations, and constitutional protections. DOMES maps the specific legal provisions
          that apply to your circumstances — your rights, your protections, your entitlements,
          and the mechanisms to enforce them.
        </p>
        <Link
          to="/circumstances"
          className="inline-block border-2 border-black bg-black text-white px-8 py-4 text-lg font-medium no-underline hover:bg-white hover:text-black transition-colors"
          aria-label="Begin mapping your legal rights"
        >
          Map Your Rights
        </Link>
      </section>

      <footer className="border-t border-border py-8 px-4 sm:px-6">
        <div className="max-w-3xl mx-auto text-center">
          <p className="text-xs text-black/40 leading-relaxed">
            DOMES provides legal information, not legal advice. The provisions displayed are
            based on federal law and may not reflect the most recent amendments or state-specific
            variations. This tool does not create an attorney-client relationship. For legal
            advice specific to your situation, consult a qualified attorney.
          </p>
        </div>
      </footer>
    </div>
  );
}
