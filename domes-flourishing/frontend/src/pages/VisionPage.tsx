import { Link } from 'react-router-dom';
import { ArrowRight } from 'lucide-react';

export default function VisionPage() {
  return (
    <div>
      {/* Hero */}
      <section className="min-h-[80vh] flex items-center justify-center px-8">
        <h1 className="font-serif text-5xl md:text-7xl lg:text-8xl text-midnight text-center leading-[0.95]">
          What Would<br />It Take?
        </h1>
      </section>

      {/* Current State */}
      <section className="max-w-3xl mx-auto px-8 py-20 border-t border-midnight/10">
        <p className="section-label mb-4">The Current State</p>
        <h2 className="font-serif text-3xl md:text-4xl text-midnight mb-8">
          Most people have gaps in most domains.
        </h2>
        <div className="space-y-6 font-serif text-lg text-midnight/70 leading-relaxed">
          <p>
            Even in the wealthiest nations, the dome is incomplete. We build floors when we
            could build cathedrals. We fund emergency rooms when we could fund vitality.
            We manage crises when we could architect flourishing.
          </p>
          <p>
            The United States spends more per person than almost any nation on earth — and
            ranks below dozens of countries on nearly every measure of human flourishing.
            The money is there. The architecture is not.
          </p>
        </div>
      </section>

      {/* The Architecture */}
      <section className="max-w-3xl mx-auto px-8 py-20 border-t border-midnight/10">
        <p className="section-label mb-4">The Architecture</p>
        <h2 className="font-serif text-3xl md:text-4xl text-midnight mb-8">
          The twelve domains are not a wish list. They are a blueprint.
        </h2>
        <div className="space-y-6 font-serif text-lg text-midnight/70 leading-relaxed">
          <p>
            Each domain has existing resources, proven models, and clear paths to expansion.
            Health. Economic security. Creative expression. Intellectual growth. Spiritual depth.
            Community belonging. Environmental harmony. Physical beauty. Love. Purpose. Play. Legacy.
          </p>
          <p>
            For every domain, we can point to a place on earth where it has been built well.
            No single place has built them all. But together, the precedents prove that every
            panel of the dome is possible.
          </p>
        </div>
      </section>

      {/* The Investment */}
      <section className="max-w-3xl mx-auto px-8 py-20 border-t border-midnight/10">
        <p className="section-label mb-4">The Investment</p>
        <h2 className="font-serif text-3xl md:text-4xl text-midnight mb-8">
          What would a complete dome cost?
        </h2>
        <div className="space-y-6 font-serif text-lg text-midnight/70 leading-relaxed">
          <p>
            The US already spends approximately <span className="text-gold font-bold">$22,000 per person per year</span> in
            public funds. Reoriented toward flourishing architecture rather than fragmented
            services, this is enough for a strong foundation.
          </p>
          <p>
            Add cooperative economics, impact investment, community wealth engines, and personal
            asset building, and the complete dome — not a safety net but a cathedral — is within reach.
            Not in some distant future. Now.
          </p>
        </div>
      </section>

      {/* The Precedent */}
      <section className="bg-midnight-deep text-white py-20 px-8">
        <div className="max-w-3xl mx-auto">
          <p className="section-label text-gold-light mb-4">The Precedent</p>
          <h2 className="font-serif text-3xl md:text-4xl mb-8">
            Nations that have built partial domes.
          </h2>
          <div className="space-y-6 font-serif text-lg text-white/70 leading-relaxed">
            <p>
              <span className="text-gold-light">The Nordic countries</span> built the social dome — universal
              healthcare, education, childcare, elder care, unemployment protection. Result:
              highest social mobility, lowest inequality, highest reported happiness.
            </p>
            <p>
              <span className="text-gold-light">Bhutan</span> built the spiritual dome — measuring Gross
              National Happiness instead of GDP. Nine domains of wellbeing as national policy.
            </p>
            <p>
              <span className="text-gold-light">Singapore</span> built the economic dome — mandatory savings,
              90% home ownership, world-class infrastructure. Proof that intentional architecture works.
            </p>
            <p>
              <span className="text-gold-light">Kerala</span> built the education dome — universal literacy,
              universal healthcare, high life expectancy, on a fraction of US spending.
              Proof that you don't need to be rich to build a dome.
            </p>
            <p className="text-white/40 italic">
              None are complete. But they prove it's possible.
            </p>
          </div>
        </div>
      </section>

      {/* The Invitation */}
      <section className="min-h-[80vh] flex items-center justify-center px-8">
        <div className="max-w-3xl text-center">
          <h2 className="font-serif text-3xl md:text-5xl text-midnight mb-8 leading-tight">
            You are not a case number.<br />
            You are not a line item in a budget.<br />
            <span className="text-gold">You are the reason all of this exists.</span>
          </h2>
          <p className="font-serif text-xl text-midnight/60 leading-relaxed mb-4">
            Your flourishing is not a program to be funded — it is a cathedral to be built.
          </p>
          <p className="font-serif text-xl text-midnight/60 leading-relaxed mb-12">
            And it begins with a single question:
          </p>
          <p className="font-serif text-3xl text-midnight italic mb-12">
            What does your flourishing look like?
          </p>
          <Link to="/dome-builder" className="btn-gold inline-flex items-center gap-2 text-base px-8 py-4">
            Build Your Dome <ArrowRight className="w-5 h-5" />
          </Link>
        </div>
      </section>
    </div>
  );
}
