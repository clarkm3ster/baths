/**
 * SPHERES Studio — Pricing Page
 *
 * Four-tier pricing: FREE, CREATOR ($49/mo), PRODUCTION ($199/mo),
 * STUDIO ($499/mo).  Full feature comparison table, FAQ, and CTA.
 */

import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import {
  ArrowLeft,
  Check,
  X,
  Sparkles,
  Zap,
  Building2,
  Crown,
  ChevronDown,
  ChevronUp,
  ArrowRight,
} from 'lucide-react';
import type { LucideProps } from 'lucide-react';

type LucideIcon = React.FC<LucideProps>;

// ---------------------------------------------------------------------------
// Data
// ---------------------------------------------------------------------------

interface PricingTier {
  id: string;
  name: string;
  price: string;
  period: string;
  subtitle: string;
  icon: LucideIcon;
  accentColor: string;
  highlighted: boolean;
  cta: string;
  features: string[];
}

const TIERS: PricingTier[] = [
  {
    id: 'free',
    name: 'FREE',
    price: '$0',
    period: '',
    subtitle: 'For dreamers and explorers',
    icon: Sparkles,
    accentColor: '#A0A0A0',
    highlighted: false,
    cta: 'Get Started',
    features: [
      'Basic canvas (up to 10 elements)',
      'Watermarked export',
      'Public designs only',
      'Community gallery access',
      'Standard element library',
      'Basic cost estimates',
    ],
  },
  {
    id: 'creator',
    name: 'CREATOR',
    price: '$49',
    period: '/mo',
    subtitle: 'For community organizers and designers',
    icon: Zap,
    accentColor: '#3B82F6',
    highlighted: true,
    cta: 'Start Free Trial',
    features: [
      'Unlimited elements',
      'Full export (PDF, budget)',
      'Private designs',
      '3D preview',
      '10 saved designs',
      'No watermark',
      'Priority element library updates',
      'Revenue projections',
    ],
  },
  {
    id: 'production',
    name: 'PRODUCTION',
    price: '$199',
    period: '/mo',
    subtitle: 'For teams building real activations',
    icon: Building2,
    accentColor: '#A855F7',
    highlighted: false,
    cta: 'Contact Sales',
    features: [
      'Everything in Creator',
      'Team collaboration (up to 5 members)',
      'Timeline & scheduling engine',
      'Priority support',
      'Unlimited designs',
      'Custom branding on exports',
      'Permit checklist generator',
      'Client sharing portal',
    ],
  },
  {
    id: 'studio',
    name: 'STUDIO',
    price: '$499',
    period: '/mo',
    subtitle: 'For agencies and production studios',
    icon: Crown,
    accentColor: '#F59E0B',
    highlighted: false,
    cta: 'Contact Sales',
    features: [
      'Everything in Production',
      'API access',
      'Unlimited team members',
      'Multi-project management',
      'Client sharing portal',
      'White-label option',
      'Dedicated account manager',
      'Custom integrations',
      'SLA guarantee',
    ],
  },
];

// Feature comparison rows
interface ComparisonRow {
  feature: string;
  free: string | boolean;
  creator: string | boolean;
  production: string | boolean;
  studio: string | boolean;
}

const COMPARISON: ComparisonRow[] = [
  { feature: 'Canvas elements', free: 'Up to 10', creator: 'Unlimited', production: 'Unlimited', studio: 'Unlimited' },
  { feature: 'Saved designs', free: '1', creator: '10', production: 'Unlimited', studio: 'Unlimited' },
  { feature: 'Export formats', free: 'PNG (watermarked)', creator: 'PDF, CSV, PNG', production: 'PDF, CSV, PNG', studio: 'PDF, CSV, PNG, API' },
  { feature: 'Private designs', free: false, creator: true, production: true, studio: true },
  { feature: '3D preview', free: false, creator: true, production: true, studio: true },
  { feature: 'Revenue projections', free: false, creator: true, production: true, studio: true },
  { feature: 'Team collaboration', free: false, creator: false, production: 'Up to 5', studio: 'Unlimited' },
  { feature: 'Timeline & scheduling', free: false, creator: false, production: true, studio: true },
  { feature: 'Custom branding', free: false, creator: false, production: true, studio: true },
  { feature: 'Permit checklist', free: false, creator: false, production: true, studio: true },
  { feature: 'API access', free: false, creator: false, production: false, studio: true },
  { feature: 'White-label', free: false, creator: false, production: false, studio: true },
  { feature: 'Dedicated support', free: false, creator: false, production: false, studio: true },
  { feature: 'Multi-project management', free: false, creator: false, production: false, studio: true },
];

// FAQ
interface FAQ {
  question: string;
  answer: string;
}

const FAQS: FAQ[] = [
  {
    question: 'Can I try SPHERES Studio for free?',
    answer:
      'Yes. The free tier gives you full access to the canvas with up to 10 elements, community gallery, and watermarked exports. No credit card required.',
  },
  {
    question: 'What happens when I exceed 10 elements on the free plan?',
    answer:
      'You will see a prompt to upgrade. Your existing design is preserved — you just cannot add more elements until you upgrade or remove some.',
  },
  {
    question: 'Is there a free trial for paid plans?',
    answer:
      'Yes. The Creator plan includes a 14-day free trial with full access to all Creator features. Cancel anytime during the trial and you will not be charged.',
  },
  {
    question: 'Can I switch plans at any time?',
    answer:
      'Absolutely. Upgrades take effect immediately, and downgrades take effect at the end of your current billing period. No lock-in contracts.',
  },
  {
    question: 'Do you offer annual billing?',
    answer:
      'Yes. Annual plans receive a 20% discount. Contact our sales team for enterprise pricing on the Studio plan.',
  },
  {
    question: 'What payment methods do you accept?',
    answer:
      'We accept all major credit and debit cards, as well as ACH bank transfers for annual plans.',
  },
];

// ---------------------------------------------------------------------------
// Sub-components
// ---------------------------------------------------------------------------

function TierCard({ tier }: { tier: PricingTier }) {
  const navigate = useNavigate();
  const Icon = tier.icon;

  return (
    <div
      className="relative flex flex-col rounded-2xl p-6 transition-all duration-300 hover:-translate-y-1"
      style={{
        background: tier.highlighted ? 'var(--bg-elevated)' : 'var(--bg-surface)',
        border: tier.highlighted
          ? `1px solid ${tier.accentColor}`
          : '1px solid var(--border)',
      }}
    >
      {tier.highlighted && (
        <div
          className="absolute -top-3 left-1/2 -translate-x-1/2 rounded-full px-4 py-0.5 text-[10px] font-semibold uppercase tracking-wider text-white"
          style={{ background: tier.accentColor }}
        >
          Most Popular
        </div>
      )}

      <div className="mb-6">
        <div
          className="mb-4 flex h-10 w-10 items-center justify-center rounded-xl"
          style={{ background: `${tier.accentColor}15`, color: tier.accentColor }}
        >
          <Icon size={20} />
        </div>
        <h3 className="mb-0.5 text-xs font-semibold uppercase tracking-wider" style={{ color: 'var(--text-secondary)' }}>
          {tier.name}
        </h3>
        <div className="flex items-baseline gap-1">
          <span className="text-4xl font-bold" style={{ color: 'var(--text-primary)' }}>
            {tier.price}
          </span>
          {tier.period && (
            <span className="text-sm" style={{ color: 'var(--text-secondary)' }}>
              {tier.period}
            </span>
          )}
        </div>
        <p className="mt-2 text-xs" style={{ color: 'var(--text-secondary)' }}>
          {tier.subtitle}
        </p>
      </div>

      <ul className="mb-8 flex flex-1 flex-col gap-3">
        {tier.features.map((f) => (
          <li key={f} className="flex items-start gap-2.5 text-sm" style={{ color: 'var(--text-secondary)' }}>
            <Check
              size={14}
              className="mt-0.5 shrink-0"
              style={{ color: tier.accentColor }}
            />
            {f}
          </li>
        ))}
      </ul>

      <button
        onClick={() => navigate(tier.id === 'free' ? '/studio' : '#')}
        className="group w-full cursor-pointer rounded-xl py-3 text-sm font-semibold transition-all duration-200 hover:brightness-110"
        style={{
          background: tier.highlighted ? tier.accentColor : 'var(--bg-elevated)',
          color: tier.highlighted ? '#fff' : 'var(--text-primary)',
          border: tier.highlighted ? 'none' : '1px solid var(--border)',
        }}
      >
        <span className="flex items-center justify-center gap-2">
          {tier.cta}
          <ArrowRight
            size={14}
            className="transition-transform duration-200 group-hover:translate-x-0.5"
          />
        </span>
      </button>
    </div>
  );
}

function ComparisonCell({ value }: { value: string | boolean }) {
  if (typeof value === 'boolean') {
    return value ? (
      <Check size={14} style={{ color: 'var(--accent-green)' }} />
    ) : (
      <X size={14} style={{ color: 'var(--text-secondary)', opacity: 0.3 }} />
    );
  }
  return (
    <span className="text-xs" style={{ color: 'var(--text-primary)' }}>
      {value}
    </span>
  );
}

function FAQItem({ faq }: { faq: FAQ }) {
  const [open, setOpen] = useState(false);

  return (
    <div
      className="rounded-xl transition-all duration-200"
      style={{
        background: open ? 'var(--bg-surface)' : 'transparent',
        border: '1px solid var(--border)',
      }}
    >
      <button
        onClick={() => setOpen(!open)}
        className="flex w-full cursor-pointer items-center justify-between px-5 py-4 text-left"
      >
        <span className="text-sm font-medium" style={{ color: 'var(--text-primary)' }}>
          {faq.question}
        </span>
        {open ? (
          <ChevronUp size={16} style={{ color: 'var(--text-secondary)' }} />
        ) : (
          <ChevronDown size={16} style={{ color: 'var(--text-secondary)' }} />
        )}
      </button>
      {open && (
        <div className="px-5 pb-4">
          <p className="text-sm leading-relaxed" style={{ color: 'var(--text-secondary)' }}>
            {faq.answer}
          </p>
        </div>
      )}
    </div>
  );
}

// ---------------------------------------------------------------------------
// Pricing Page
// ---------------------------------------------------------------------------

export default function PricingPage() {
  const [billingCycle, setBillingCycle] = useState<'monthly' | 'annual'>('monthly');

  return (
    <div className="h-screen overflow-y-auto" style={{ background: 'var(--bg-primary)' }}>
      {/* Nav */}
      <nav
        className="glass sticky top-0 z-50 flex h-14 items-center justify-between px-6"
        style={{ borderBottom: '1px solid var(--border)' }}
      >
        <div className="flex items-center gap-4">
          <Link to="/" className="flex items-center gap-2">
            <div
              className="flex h-7 w-7 items-center justify-center rounded-lg text-xs font-bold"
              style={{ background: 'var(--accent)', color: '#fff' }}
            >
              S
            </div>
            <span className="text-sm font-semibold tracking-tight">SPHERES Studio</span>
          </Link>
        </div>
        <Link
          to="/studio"
          className="flex items-center gap-1.5 text-xs font-medium transition-colors duration-200 hover:text-white"
          style={{ color: 'var(--text-secondary)' }}
        >
          <ArrowLeft size={14} />
          Back to Studio
        </Link>
      </nav>

      {/* Hero */}
      <section className="relative px-6 pt-20 pb-16 text-center">
        <div
          className="pointer-events-none absolute inset-0"
          style={{
            background:
              'radial-gradient(ellipse 60% 40% at 50% 20%, rgba(59,130,246,0.06) 0%, transparent 70%)',
          }}
        />
        <div className="relative z-10">
          <h1
            className="mb-4 text-4xl font-bold tracking-tight md:text-5xl"
            style={{ color: 'var(--text-primary)' }}
          >
            Plans for every scale
          </h1>
          <p
            className="mx-auto max-w-lg text-base"
            style={{ color: 'var(--text-secondary)' }}
          >
            From solo community organizers to full production studios.
            Start free, scale when your activations do.
          </p>

          {/* Billing toggle */}
          <div className="mt-8 flex items-center justify-center gap-3">
            <span
              className="text-xs font-medium"
              style={{
                color: billingCycle === 'monthly' ? 'var(--text-primary)' : 'var(--text-secondary)',
              }}
            >
              Monthly
            </span>
            <button
              onClick={() =>
                setBillingCycle(billingCycle === 'monthly' ? 'annual' : 'monthly')
              }
              className="relative flex h-6 w-11 cursor-pointer items-center rounded-full transition-colors duration-200"
              style={{
                background: billingCycle === 'annual' ? 'var(--accent)' : 'var(--bg-elevated)',
                border: '1px solid var(--border)',
              }}
            >
              <div
                className="h-4 w-4 rounded-full bg-white transition-transform duration-200"
                style={{
                  transform: billingCycle === 'annual' ? 'translateX(22px)' : 'translateX(4px)',
                }}
              />
            </button>
            <span
              className="text-xs font-medium"
              style={{
                color: billingCycle === 'annual' ? 'var(--text-primary)' : 'var(--text-secondary)',
              }}
            >
              Annual
            </span>
            {billingCycle === 'annual' && (
              <span
                className="rounded-full px-2 py-0.5 text-[10px] font-semibold"
                style={{
                  background: 'rgba(34,197,94,0.1)',
                  color: 'var(--accent-green)',
                  border: '1px solid rgba(34,197,94,0.2)',
                }}
              >
                Save 20%
              </span>
            )}
          </div>
        </div>
      </section>

      {/* Tier Cards */}
      <section className="px-6 pb-24">
        <div className="stagger-children mx-auto grid max-w-6xl gap-6 md:grid-cols-2 lg:grid-cols-4">
          {TIERS.map((tier) => (
            <TierCard key={tier.id} tier={tier} />
          ))}
        </div>
      </section>

      {/* Feature Comparison Table */}
      <section className="px-6 pb-24">
        <div className="mx-auto max-w-5xl">
          <h2
            className="mb-10 text-center text-2xl font-bold tracking-tight"
            style={{ color: 'var(--text-primary)' }}
          >
            Feature comparison
          </h2>

          <div
            className="overflow-hidden rounded-xl"
            style={{ border: '1px solid var(--border)' }}
          >
            {/* Header */}
            <div
              className="grid grid-cols-5 gap-4 px-5 py-3"
              style={{ background: 'var(--bg-surface)', borderBottom: '1px solid var(--border)' }}
            >
              <div className="text-xs font-semibold" style={{ color: 'var(--text-secondary)' }}>
                Feature
              </div>
              {TIERS.map((t) => (
                <div
                  key={t.id}
                  className="text-center text-xs font-semibold"
                  style={{ color: t.accentColor }}
                >
                  {t.name}
                </div>
              ))}
            </div>

            {/* Rows */}
            {COMPARISON.map((row, i) => (
              <div
                key={row.feature}
                className="grid grid-cols-5 items-center gap-4 px-5 py-3"
                style={{
                  background: i % 2 === 0 ? 'var(--bg-primary)' : 'var(--bg-surface)',
                  borderBottom:
                    i < COMPARISON.length - 1 ? '1px solid var(--border)' : 'none',
                }}
              >
                <div className="text-xs" style={{ color: 'var(--text-secondary)' }}>
                  {row.feature}
                </div>
                <div className="flex justify-center">
                  <ComparisonCell value={row.free} />
                </div>
                <div className="flex justify-center">
                  <ComparisonCell value={row.creator} />
                </div>
                <div className="flex justify-center">
                  <ComparisonCell value={row.production} />
                </div>
                <div className="flex justify-center">
                  <ComparisonCell value={row.studio} />
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* FAQ */}
      <section className="px-6 pb-24" style={{ background: 'var(--bg-surface)' }}>
        <div className="mx-auto max-w-3xl pt-20">
          <h2
            className="mb-10 text-center text-2xl font-bold tracking-tight"
            style={{ color: 'var(--text-primary)' }}
          >
            Frequently asked questions
          </h2>
          <div className="space-y-3">
            {FAQS.map((faq) => (
              <FAQItem key={faq.question} faq={faq} />
            ))}
          </div>
        </div>
      </section>

      {/* Bottom CTA */}
      <section className="px-6 py-20 text-center">
        <h2
          className="mb-3 text-3xl font-bold tracking-tight"
          style={{ color: 'var(--text-primary)' }}
        >
          Ready to design your activation?
        </h2>
        <p className="mb-8 text-sm" style={{ color: 'var(--text-secondary)' }}>
          Start with the free plan. No credit card required.
        </p>
        <Link
          to="/studio"
          className="inline-flex items-center gap-2 rounded-xl px-8 py-3.5 text-sm font-semibold text-white transition-all duration-200 hover:brightness-110"
          style={{ background: 'var(--accent)' }}
        >
          Open Studio
          <ArrowRight size={16} />
        </Link>
      </section>

      {/* Footer */}
      <footer className="px-6 py-10" style={{ borderTop: '1px solid var(--border)' }}>
        <div className="mx-auto flex max-w-5xl items-center justify-between">
          <div className="flex items-center gap-2">
            <div
              className="flex h-6 w-6 items-center justify-center rounded-md text-[10px] font-bold"
              style={{ background: 'var(--accent)', color: '#fff' }}
            >
              S
            </div>
            <span className="text-xs font-semibold">SPHERES Studio</span>
          </div>
          <p className="text-[11px]" style={{ color: 'var(--text-secondary)' }}>
            &copy; {new Date().getFullYear()} SPHERES. All rights reserved.
          </p>
        </div>
      </footer>
    </div>
  );
}
