/**
 * SPHERES Studio — Landing Page
 *
 * Dark, cinematic hero-driven landing that introduces the activation design
 * studio.  Sections: hero, feature cards, how-it-works, permanence, pricing
 * teaser, and footer.
 */

import { useNavigate, Link } from 'react-router-dom';
import {
  Layers,
  DollarSign,
  Box,
  MapPin,
  Paintbrush,
  Eye,
  Share2,
  ArrowRight,
  ChevronRight,
  Sparkles,
  Check,
} from 'lucide-react';
import type { LucideProps } from 'lucide-react';

type LucideIcon = React.FC<LucideProps>;

// ---------------------------------------------------------------------------
// Sub-components
// ---------------------------------------------------------------------------

function FeatureCard({
  icon: Icon,
  title,
  description,
  accent,
}: {
  icon: LucideIcon;
  title: string;
  description: string;
  accent: string;
}) {
  return (
    <div
      className="group relative rounded-2xl p-6 transition-all duration-300 hover:-translate-y-1"
      style={{
        background: 'var(--bg-surface)',
        border: '1px solid var(--border)',
      }}
    >
      <div
        className="absolute inset-0 rounded-2xl opacity-0 transition-opacity duration-300 group-hover:opacity-100"
        style={{
          background: `radial-gradient(ellipse at top left, ${accent}08 0%, transparent 70%)`,
        }}
      />
      <div className="relative z-10">
        <div
          className="mb-4 flex h-12 w-12 items-center justify-center rounded-xl"
          style={{ background: `${accent}15`, color: accent }}
        >
          <Icon size={24} />
        </div>
        <h3 className="mb-2 text-lg font-semibold" style={{ color: 'var(--text-primary)' }}>
          {title}
        </h3>
        <p className="text-sm leading-relaxed" style={{ color: 'var(--text-secondary)' }}>
          {description}
        </p>
      </div>
    </div>
  );
}

function StepCard({
  number,
  title,
  description,
}: {
  number: number;
  title: string;
  description: string;
}) {
  return (
    <div className="relative flex flex-col items-center text-center">
      <div
        className="mb-4 flex h-10 w-10 items-center justify-center rounded-full text-sm font-bold"
        style={{ background: 'var(--accent)', color: '#fff' }}
      >
        {number}
      </div>
      <h4 className="mb-1 text-sm font-semibold" style={{ color: 'var(--text-primary)' }}>
        {title}
      </h4>
      <p className="text-xs leading-relaxed" style={{ color: 'var(--text-secondary)' }}>
        {description}
      </p>
    </div>
  );
}

interface PricingTierProps {
  name: string;
  price: string;
  period?: string;
  features: string[];
  accent?: string;
  highlighted?: boolean;
  cta: string;
}

function PricingTier({ name, price, period, features, accent, highlighted, cta }: PricingTierProps) {
  const navigate = useNavigate();

  return (
    <div
      className="relative flex flex-col rounded-2xl p-6 transition-all duration-300 hover:-translate-y-1"
      style={{
        background: highlighted ? 'var(--bg-elevated)' : 'var(--bg-surface)',
        border: highlighted
          ? `1px solid ${accent || 'var(--accent)'}`
          : '1px solid var(--border)',
      }}
    >
      {highlighted && (
        <div
          className="absolute -top-3 left-1/2 -translate-x-1/2 rounded-full px-3 py-0.5 text-[10px] font-semibold uppercase tracking-wider text-white"
          style={{ background: accent || 'var(--accent)' }}
        >
          Most Popular
        </div>
      )}
      <div className="mb-6">
        <h4 className="mb-1 text-sm font-medium uppercase tracking-wider" style={{ color: 'var(--text-secondary)' }}>
          {name}
        </h4>
        <div className="flex items-baseline gap-1">
          <span className="text-3xl font-bold" style={{ color: 'var(--text-primary)' }}>
            {price}
          </span>
          {period && (
            <span className="text-sm" style={{ color: 'var(--text-secondary)' }}>
              {period}
            </span>
          )}
        </div>
      </div>

      <ul className="mb-6 flex flex-1 flex-col gap-2.5">
        {features.map((f) => (
          <li key={f} className="flex items-start gap-2 text-sm" style={{ color: 'var(--text-secondary)' }}>
            <Check size={14} className="mt-0.5 shrink-0" style={{ color: 'var(--accent-green)' }} />
            {f}
          </li>
        ))}
      </ul>

      <button
        onClick={() => navigate(name === 'FREE' ? '/studio' : '/pricing')}
        className="w-full cursor-pointer rounded-lg py-2.5 text-sm font-medium transition-all duration-200 hover:brightness-110"
        style={{
          background: highlighted ? (accent || 'var(--accent)') : 'var(--bg-elevated)',
          color: highlighted ? '#fff' : 'var(--text-primary)',
          border: highlighted ? 'none' : '1px solid var(--border)',
        }}
      >
        {cta}
      </button>
    </div>
  );
}

// ---------------------------------------------------------------------------
// Landing Page
// ---------------------------------------------------------------------------

export default function LandingPage() {
  const navigate = useNavigate();

  return (
    <div
      className="h-screen overflow-y-auto"
      style={{ background: 'var(--bg-primary)' }}
    >
      {/* ── Nav ─────────────────────────────────────────────────────────── */}
      <nav
        className="glass fixed top-0 right-0 left-0 z-50 flex h-14 items-center justify-between px-6"
        style={{ borderBottom: '1px solid var(--border)' }}
      >
        <Link to="/" className="flex items-center gap-2">
          <div
            className="flex h-7 w-7 items-center justify-center rounded-lg text-xs font-bold"
            style={{ background: 'var(--accent)', color: '#fff' }}
          >
            S
          </div>
          <span className="text-sm font-semibold tracking-tight">SPHERES Studio</span>
        </Link>

        <div className="flex items-center gap-6">
          <Link
            to="/gallery"
            className="text-xs font-medium transition-colors duration-200 hover:text-white"
            style={{ color: 'var(--text-secondary)' }}
          >
            Gallery
          </Link>
          <Link
            to="/pricing"
            className="text-xs font-medium transition-colors duration-200 hover:text-white"
            style={{ color: 'var(--text-secondary)' }}
          >
            Pricing
          </Link>
          <button
            onClick={() => navigate('/studio')}
            className="cursor-pointer rounded-lg px-4 py-1.5 text-xs font-medium text-white transition-all duration-200 hover:brightness-110"
            style={{ background: 'var(--accent)' }}
          >
            Open Studio
          </button>
        </div>
      </nav>

      {/* ── Hero ────────────────────────────────────────────────────────── */}
      <section className="relative flex min-h-screen flex-col items-center justify-center px-6 pt-14 text-center">
        {/* Subtle radial gradient background */}
        <div
          className="pointer-events-none absolute inset-0"
          style={{
            background:
              'radial-gradient(ellipse 80% 50% at 50% 30%, rgba(59,130,246,0.06) 0%, transparent 70%)',
          }}
        />

        <div className="animate-fade-in-up relative z-10 max-w-3xl">
          <div
            className="mb-6 inline-flex items-center gap-2 rounded-full px-4 py-1.5 text-xs font-medium"
            style={{
              background: 'rgba(59,130,246,0.1)',
              color: 'var(--accent)',
              border: '1px solid rgba(59,130,246,0.2)',
            }}
          >
            <Sparkles size={12} />
            The activation design studio
          </div>

          <h1
            className="mb-6 text-5xl leading-tight font-extrabold tracking-tight md:text-6xl lg:text-7xl"
            style={{ color: 'var(--text-primary)' }}
          >
            Design What Your City{' '}
            <span className="gradient-text-accent">Could Become</span>
          </h1>

          <p
            className="mx-auto mb-10 max-w-xl text-base leading-relaxed md:text-lg"
            style={{ color: 'var(--text-secondary)' }}
          >
            Drag. Drop. Explore in 3D. Build the future of public space with the
            first design studio purpose-built for urban activations.
          </p>

          <div className="flex flex-wrap items-center justify-center gap-4">
            <button
              onClick={() => navigate('/studio')}
              className="animate-pulse-glow group flex cursor-pointer items-center gap-2 rounded-xl px-8 py-3.5 text-sm font-semibold text-white transition-all duration-200 hover:brightness-110"
              style={{ background: 'var(--accent)' }}
            >
              Start Designing
              <ArrowRight
                size={16}
                className="transition-transform duration-200 group-hover:translate-x-0.5"
              />
            </button>
            <button
              onClick={() => navigate('/gallery')}
              className="flex cursor-pointer items-center gap-2 rounded-xl px-8 py-3.5 text-sm font-semibold transition-all duration-200 hover:brightness-125"
              style={{
                background: 'var(--bg-surface)',
                color: 'var(--text-primary)',
                border: '1px solid var(--border)',
              }}
            >
              Browse Gallery
              <ChevronRight size={16} />
            </button>
          </div>
        </div>

        {/* Scroll indicator */}
        <div className="animate-float absolute bottom-10 flex flex-col items-center gap-2">
          <span className="text-[10px] uppercase tracking-widest" style={{ color: 'var(--text-secondary)' }}>
            Scroll
          </span>
          <div className="h-6 w-px" style={{ background: 'var(--border)' }} />
        </div>
      </section>

      {/* ── Feature Cards ──────────────────────────────────────────────── */}
      <section className="relative px-6 py-24">
        <div className="mx-auto max-w-5xl">
          <div className="stagger-children mb-14 text-center">
            <h2
              className="mb-3 text-3xl font-bold tracking-tight md:text-4xl"
              style={{ color: 'var(--text-primary)' }}
            >
              Everything you need to activate a space
            </h2>
            <p className="text-sm" style={{ color: 'var(--text-secondary)' }}>
              From blank lot to fully-costed, permit-ready activation — in minutes.
            </p>
          </div>

          <div className="stagger-children grid gap-6 md:grid-cols-3">
            <FeatureCard
              icon={Layers}
              title="Design"
              description="Drag-and-drop canvas with 50+ activation elements — stages, gardens, food vendors, art installations, and more. Snap to grid, layer by permanence, and see it all come together."
              accent="#3B82F6"
            />
            <FeatureCard
              icon={DollarSign}
              title="Cost It"
              description="Every element carries real cost data. Watch the budget ticker update in real time, see revenue projections, and export a complete budget breakdown ready for stakeholders."
              accent="#22C55E"
            />
            <FeatureCard
              icon={Box}
              title="Explore It"
              description="Step into your design with a first-person 3D walkthrough. Toggle time of day, see before-and-after, and share immersive previews with the community."
              accent="#A855F7"
            />
          </div>
        </div>
      </section>

      {/* ── How It Works ───────────────────────────────────────────────── */}
      <section className="px-6 py-24" style={{ background: 'var(--bg-surface)' }}>
        <div className="mx-auto max-w-4xl">
          <h2
            className="mb-14 text-center text-3xl font-bold tracking-tight md:text-4xl"
            style={{ color: 'var(--text-primary)' }}
          >
            How it works
          </h2>

          <div className="relative grid grid-cols-2 gap-10 md:grid-cols-4">
            {/* Connecting line */}
            <div
              className="pointer-events-none absolute top-5 right-[12%] left-[12%] hidden h-px md:block"
              style={{ background: 'var(--border)' }}
            />
            <StepCard
              number={1}
              title="Pick a space"
              description="Search for a parcel or draw your own site boundary on the map."
            />
            <StepCard
              number={2}
              title="Design your activation"
              description="Drag elements onto the canvas. Costs and permits update automatically."
            />
            <StepCard
              number={3}
              title="Explore in 3D"
              description="Walk through your design at street level with realistic lighting."
            />
            <StepCard
              number={4}
              title="Share & build support"
              description="Export budgets, share 3D previews, and rally community backing."
            />
          </div>
        </div>
      </section>

      {/* ── Permanence ─────────────────────────────────────────────────── */}
      <section className="relative px-6 py-24">
        <div
          className="pointer-events-none absolute inset-0"
          style={{
            background:
              'radial-gradient(ellipse 60% 50% at 50% 50%, rgba(34,197,94,0.04) 0%, transparent 70%)',
          }}
        />
        <div className="relative z-10 mx-auto max-w-3xl text-center">
          <div
            className="mb-4 inline-flex items-center gap-2 rounded-full px-3 py-1 text-[10px] font-semibold uppercase tracking-wider"
            style={{
              background: 'rgba(34,197,94,0.1)',
              color: 'var(--accent-green)',
              border: '1px solid rgba(34,197,94,0.2)',
            }}
          >
            <MapPin size={12} />
            Permanence Engine
          </div>
          <h2
            className="mb-4 text-3xl font-bold tracking-tight md:text-4xl"
            style={{ color: 'var(--text-primary)' }}
          >
            What stays behind matters
          </h2>
          <p
            className="mx-auto max-w-xl text-base leading-relaxed"
            style={{ color: 'var(--text-secondary)' }}
          >
            Every SPHERES design calculates the permanent value left for the
            community. Garden beds that remain. Murals that endure. Infrastructure
            that keeps giving. We track it all so activations aren't just events
            — they're investments.
          </p>

          <div className="stagger-children mt-12 grid gap-4 md:grid-cols-3">
            {[
              { label: 'Physical', desc: 'Benches, paths, lighting that stay', color: '#3B82F6' },
              { label: 'Environmental', desc: 'Trees, gardens, native meadows', color: '#22C55E' },
              { label: 'Community', desc: 'Murals, play areas, gathering spaces', color: '#A855F7' },
            ].map((item) => (
              <div
                key={item.label}
                className="rounded-xl p-5 text-left"
                style={{ background: 'var(--bg-surface)', border: '1px solid var(--border)' }}
              >
                <div className="mb-2 h-1 w-10 rounded-full" style={{ background: item.color }} />
                <h4 className="mb-1 text-sm font-semibold" style={{ color: 'var(--text-primary)' }}>
                  {item.label}
                </h4>
                <p className="text-xs" style={{ color: 'var(--text-secondary)' }}>
                  {item.desc}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── Pricing Teaser ─────────────────────────────────────────────── */}
      <section className="px-6 py-24" style={{ background: 'var(--bg-surface)' }}>
        <div className="mx-auto max-w-5xl">
          <div className="mb-14 text-center">
            <h2
              className="mb-3 text-3xl font-bold tracking-tight md:text-4xl"
              style={{ color: 'var(--text-primary)' }}
            >
              Start free. Scale when ready.
            </h2>
            <p className="text-sm" style={{ color: 'var(--text-secondary)' }}>
              From solo dreamers to production studios.
            </p>
          </div>

          <div className="stagger-children grid gap-5 md:grid-cols-4">
            <PricingTier
              name="FREE"
              price="$0"
              features={[
                'Basic canvas (up to 10 elements)',
                'Watermarked export',
                'Public designs only',
                'Community gallery access',
              ]}
              cta="Get Started"
            />
            <PricingTier
              name="CREATOR"
              price="$49"
              period="/mo"
              features={[
                'Unlimited elements',
                'Full export (PDF, budget)',
                'Private designs',
                '3D preview',
                '10 saved designs',
              ]}
              accent="#3B82F6"
              highlighted
              cta="Start Free Trial"
            />
            <PricingTier
              name="PRODUCTION"
              price="$199"
              period="/mo"
              features={[
                'Everything in Creator',
                'Team collaboration (up to 5)',
                'Timeline & scheduling',
                'Priority support',
                'Unlimited designs',
              ]}
              cta="Contact Sales"
            />
            <PricingTier
              name="STUDIO"
              price="$499"
              period="/mo"
              features={[
                'Everything in Production',
                'API access',
                'Unlimited team members',
                'White-label option',
                'Dedicated support',
              ]}
              cta="Contact Sales"
            />
          </div>

          <div className="mt-8 text-center">
            <Link
              to="/pricing"
              className="inline-flex items-center gap-1 text-xs font-medium transition-colors duration-200 hover:text-white"
              style={{ color: 'var(--accent)' }}
            >
              See full plan comparison
              <ChevronRight size={14} />
            </Link>
          </div>
        </div>
      </section>

      {/* ── Footer ─────────────────────────────────────────────────────── */}
      <footer className="px-6 py-16" style={{ borderTop: '1px solid var(--border)' }}>
        <div className="mx-auto flex max-w-5xl flex-col items-center gap-8 md:flex-row md:justify-between">
          <div className="flex items-center gap-2">
            <div
              className="flex h-7 w-7 items-center justify-center rounded-lg text-xs font-bold"
              style={{ background: 'var(--accent)', color: '#fff' }}
            >
              S
            </div>
            <span className="text-sm font-semibold tracking-tight">SPHERES Studio</span>
          </div>

          <div className="flex gap-8">
            {[
              { label: 'Studio', to: '/studio' },
              { label: 'Gallery', to: '/gallery' },
              { label: 'Pricing', to: '/pricing' },
            ].map((link) => (
              <Link
                key={link.to}
                to={link.to}
                className="text-xs font-medium transition-colors duration-200 hover:text-white"
                style={{ color: 'var(--text-secondary)' }}
              >
                {link.label}
              </Link>
            ))}
          </div>

          <p className="text-[11px]" style={{ color: 'var(--text-secondary)' }}>
            &copy; {new Date().getFullYear()} SPHERES. All rights reserved.
          </p>
        </div>
      </footer>
    </div>
  );
}
