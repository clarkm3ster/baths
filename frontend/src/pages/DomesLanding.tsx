import { Link } from 'react-router-dom';
import { useEffect, useRef } from 'react';

const LAYERS = [
  { n: 1, name: 'Legal', desc: 'Every right, every entitlement, every pathway', agent: 'AI' },
  { n: 2, name: 'Systems', desc: 'Every government system, every portal, every form', agent: 'AI' },
  { n: 3, name: 'Fiscal', desc: 'Every cost, every saving, every financial instrument', agent: 'AI' },
  { n: 4, name: 'Health', desc: 'Every diagnosis, every treatment, every trajectory', agent: 'AI' },
  { n: 5, name: 'Housing', desc: 'Every structure, every system, every environment', agent: 'AI' },
  { n: 6, name: 'Economic', desc: 'Every job, every skill, every income path', agent: 'AI' },
  { n: 7, name: 'Education', desc: 'Every credential, every learning path, every opportunity', agent: 'AI' },
  { n: 8, name: 'Community', desc: 'Every connection, every asset, every risk', agent: 'AI' },
  { n: 9, name: 'Environment', desc: 'Every sensor, every reading, every exposure', agent: 'AI' },
  { n: 10, name: 'Autonomy', desc: 'What autonomy means for THIS person', agent: 'HUMAN' },
  { n: 11, name: 'Creativity', desc: 'How THIS person makes meaning', agent: 'HUMAN' },
  { n: 12, name: 'Flourishing', desc: 'What flourishing looks like HERE', agent: 'HUMAN' },
];

const TIERS = [
  {
    name: 'BLOCKBUSTER',
    budget: '$1M+',
    team: '15-80 people',
    layers: '12-layer deep',
    timeline: '12-36 months',
    desc: 'Full-scale dome production. Visionary director. Multi-disciplinary creative team. Every layer filled to maximum depth. The dome itself becomes a franchise.',
  },
  {
    name: 'INDIE',
    budget: '$50K-$250K',
    team: '5-15 people',
    layers: '9 layers',
    timeline: '6-18 months',
    desc: 'Focused dome production. Strong director with specific vision. AI fills layers 1-9, creative team designs 2-3 human layers. The dome tells one story exceptionally well.',
  },
  {
    name: 'MICRO',
    budget: '$5K-$50K',
    team: '2-5 people',
    layers: '6 layers',
    timeline: '2-6 months',
    desc: 'AI-heavy proof-of-concept. Produces a focused business case and single-domain IP. Often used to prove the concept before scaling.',
  },
];

const IP_DOMAINS = [
  'Film & Television',
  'Technology Platforms',
  'Financial Products',
  'Healthcare Protocols',
  'Policy & Research',
  'Product Design',
  'Architecture',
  'Performance Art',
];

export function DomesLanding() {
  const sectionsRef = useRef<HTMLElement[]>([]);

  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add('visible');
          }
        });
      },
      { threshold: 0.1 }
    );

    sectionsRef.current.forEach((el) => {
      if (el) observer.observe(el);
    });

    return () => observer.disconnect();
  }, []);

  const addRef = (el: HTMLElement | null, index: number) => {
    if (el) sectionsRef.current[index] = el;
  };

  return (
    <div>
      {/* ── HERO ─────────────────────────────────────────────── */}
      <section className="min-h-screen flex flex-col items-center justify-center relative overflow-hidden bg-black text-white">
        {/* Animated dome silhouette */}
        <div className="absolute inset-0 flex items-end justify-center opacity-10">
          <svg viewBox="0 0 800 400" className="w-full max-w-4xl dome-pulse">
            {[...Array(12)].map((_, i) => {
              const r = 380 - i * 28;
              return (
                <path
                  key={i}
                  d={`M ${400 - r} 400 A ${r} ${r} 0 0 1 ${400 + r} 400`}
                  fill="none"
                  stroke="white"
                  strokeWidth={i >= 9 ? 3 : 1}
                  opacity={0.2 + i * 0.06}
                />
              );
            })}
            {/* Person at center */}
            <circle cx="400" cy="400" r="6" fill="white" opacity="0.8" />
          </svg>
        </div>

        <div className="relative z-10 text-center px-6 max-w-4xl">
          <p className="text-sm tracking-[0.5em] uppercase text-white/40 mb-8">
            Person-Runner Production Engine
          </p>
          <h1 className="font-serif text-5xl sm:text-7xl lg:text-8xl leading-[0.95] mb-8">
            Character In,<br />
            <em className="font-serif">Dome Out.</em>
          </h1>
          <p className="text-lg sm:text-xl text-white/60 max-w-2xl mx-auto mb-12 leading-relaxed">
            Input a character and their circumstances. Person-Runner generates a massive
            IP pitch across film, TV, product, technology, and biological domains.
            Everything organized around the person at the gravitational center.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              to="/run"
              className="inline-block border-2 border-white bg-white text-black px-10 py-4 text-lg font-medium no-underline hover:bg-transparent hover:text-white transition-colors"
            >
              Run a Dome
            </Link>
            <Link
              to="/product"
              className="inline-block border-2 border-white/30 text-white px-10 py-4 text-lg font-medium no-underline hover:border-white transition-colors"
            >
              How It Works
            </Link>
          </div>
        </div>

        {/* Scroll indicator */}
        <div className="absolute bottom-8 left-1/2 -translate-x-1/2 flex flex-col items-center gap-2">
          <span className="text-white/30 text-xs tracking-widest uppercase">Scroll</span>
          <div className="w-px h-8 bg-gradient-to-b from-white/30 to-transparent" />
        </div>
      </section>

      {/* ── THE ARCHITECTURE ─────────────────────────────────── */}
      <section
        ref={(el) => addRef(el, 0)}
        className="section-fade py-24 sm:py-32 px-6 bg-white"
      >
        <div className="max-w-6xl mx-auto">
          <div className="max-w-3xl mb-16">
            <p className="text-sm tracking-[0.4em] uppercase text-black/40 mb-4">
              Architecture
            </p>
            <h2 className="font-serif text-4xl sm:text-5xl leading-tight mb-6">
              The person is the gravitational center.
            </h2>
            <p className="text-lg text-black/60 leading-relaxed">
              12 layers surround them — each one a dimension of their life.
              Layers 1-9 are filled by AI agents. Layers 10-12 are designed by
              human creative teams. The dome is only as strong as its weakest layer.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-px bg-border">
            {LAYERS.map((layer) => (
              <div
                key={layer.n}
                className={`p-6 bg-white layer-reveal layer-delay-${layer.n} ${
                  layer.agent === 'HUMAN' ? 'bg-black text-white' : ''
                }`}
              >
                <div className="flex items-center gap-3 mb-3">
                  <span className={`font-mono text-xs px-2 py-0.5 ${
                    layer.agent === 'HUMAN'
                      ? 'bg-white/10 text-white/60'
                      : 'bg-black/5 text-black/40'
                  }`}>
                    {String(layer.n).padStart(2, '0')}
                  </span>
                  <span className={`text-xs tracking-wider uppercase ${
                    layer.agent === 'HUMAN' ? 'text-white/40' : 'text-black/30'
                  }`}>
                    {layer.agent}
                  </span>
                </div>
                <h3 className={`font-serif text-xl mb-2 ${
                  layer.agent === 'HUMAN' ? 'text-white' : 'text-black'
                }`}>
                  {layer.name}
                </h3>
                <p className={`text-sm leading-relaxed ${
                  layer.agent === 'HUMAN' ? 'text-white/60' : 'text-black/50'
                }`}>
                  {layer.desc}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── WHAT PERSON-RUNNER GENERATES ──────────────────────── */}
      <section
        ref={(el) => addRef(el, 1)}
        className="section-fade py-24 sm:py-32 px-6 bg-black text-white"
      >
        <div className="max-w-6xl mx-auto">
          <div className="max-w-3xl mb-16">
            <p className="text-sm tracking-[0.4em] uppercase text-white/40 mb-4">
              The Product
            </p>
            <h2 className="font-serif text-4xl sm:text-5xl leading-tight mb-6">
              One character. One engine.<br />
              <em>Everything.</em>
            </h2>
            <p className="text-lg text-white/50 leading-relaxed">
              Person-Runner takes a character and their circumstances and generates
              the entire gamut of the business case to fund the dome. Production budget,
              IP portfolio, team assembly, simulation, and a complete website of the
              dome and everything that went into building it.
            </p>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8">
            {[
              {
                title: 'IP Portfolio',
                items: IP_DOMAINS.slice(0, 4),
                stat: '8+ domains',
              },
              {
                title: 'Business Case',
                items: ['Production budget', 'ROI justification', 'Dome Bond prospectus', 'Investment thesis'],
                stat: 'Full pitch',
              },
              {
                title: 'Production',
                items: ['Team assembly', 'Pipeline milestones', 'Creative disciplines', 'Tech innovations'],
                stat: '5 stages',
              },
              {
                title: 'Simulation',
                items: ['Fragmented baseline', 'Coordinated scenario', 'Intervention targets', 'Cosm scoring'],
                stat: '3 scenarios',
              },
            ].map((block) => (
              <div key={block.title} className="border border-white/10 p-6">
                <h3 className="font-serif text-xl mb-1">{block.title}</h3>
                <p className="text-white/30 text-sm mb-4 font-mono">{block.stat}</p>
                <ul className="space-y-2">
                  {block.items.map((item) => (
                    <li key={item} className="text-sm text-white/50 flex items-start gap-2">
                      <span className="text-white/20 mt-1">&#9656;</span>
                      {item}
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── DOME TIERS ────────────────────────────────────────── */}
      <section
        ref={(el) => addRef(el, 2)}
        className="section-fade py-24 sm:py-32 px-6 bg-white"
      >
        <div className="max-w-6xl mx-auto">
          <div className="max-w-3xl mb-16">
            <p className="text-sm tracking-[0.4em] uppercase text-black/40 mb-4">
              Production Tiers
            </p>
            <h2 className="font-serif text-4xl sm:text-5xl leading-tight mb-6">
              Blockbuster. Indie. Micro.
            </h2>
            <p className="text-lg text-black/60 leading-relaxed">
              Every dome has a tier. The tier determines the production budget,
              team size, creative depth, and IP surface area. The person at the
              center is always the same. The dome just gets deeper.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-px bg-border">
            {TIERS.map((tier) => (
              <div key={tier.name} className="p-8 bg-white">
                <h3 className="font-mono text-sm tracking-[0.3em] text-black/40 mb-4">
                  {tier.name}
                </h3>
                <p className="font-serif text-3xl mb-4">{tier.budget}</p>
                <div className="space-y-2 mb-6 text-sm text-black/50">
                  <p>{tier.team}</p>
                  <p>{tier.layers}</p>
                  <p>{tier.timeline}</p>
                </div>
                <p className="text-sm text-black/60 leading-relaxed">
                  {tier.desc}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── IP DOMAINS ────────────────────────────────────────── */}
      <section
        ref={(el) => addRef(el, 3)}
        className="section-fade py-24 sm:py-32 px-6 bg-[#FAFAFA]"
      >
        <div className="max-w-6xl mx-auto">
          <div className="max-w-3xl mb-16">
            <p className="text-sm tracking-[0.4em] uppercase text-black/40 mb-4">
              IP Generation
            </p>
            <h2 className="font-serif text-4xl sm:text-5xl leading-tight mb-6">
              Every dome is an IP engine.
            </h2>
            <p className="text-lg text-black/60 leading-relaxed">
              Each production generates intellectual property across every domain
              it touches. Documentary treatments. Series bibles. Technology platforms.
              Financial instruments. Policy briefs. Academic papers. Product designs.
              The IP portfolio is how the dome pays for itself.
            </p>
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-4 gap-px bg-border">
            {IP_DOMAINS.map((domain) => (
              <div key={domain} className="p-6 bg-white text-center">
                <p className="font-serif text-lg">{domain}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── DATA ENGINE ─────────────────────────────────────────── */}
      <section
        ref={(el) => addRef(el, 4)}
        className="section-fade py-24 sm:py-32 px-6 bg-black text-white"
      >
        <div className="max-w-6xl mx-auto">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-16 items-center">
            <div>
              <p className="text-sm tracking-[0.4em] uppercase text-white/40 mb-4">
                Data Infrastructure
              </p>
              <h2 className="font-serif text-4xl sm:text-5xl leading-tight mb-6">
                Fragment &amp; Cosm
              </h2>
              <p className="text-lg text-white/50 leading-relaxed mb-8">
                Two automated agents scrape, accumulate, and assemble public data
                about the conditions of human existence. Fragment mirrors the
                fragmentation of human data. Cosm assembles it around a single life.
                Running 5 times daily across 28 US counties.
              </p>
              <div className="space-y-4 text-sm text-white/40">
                <p>US Census ACS 5-year &middot; BLS &middot; HUD FMR &middot; FEMA &middot; EPA AirNow &middot; USDA Food Access</p>
                <p>FHIR R4 &middot; PRAPARE &middot; AHC-HRSN &middot; ICD-10-CM &middot; LOINC</p>
              </div>
            </div>
            <div className="font-mono text-sm text-white/30 space-y-1 bg-white/5 p-6">
              <p className="text-white/50 mb-3"># Data structure</p>
              <p>data/</p>
              <p>&nbsp;&nbsp;fragments/&lbrace;source&rbrace;/&lbrace;fips&rbrace;.json</p>
              <p>&nbsp;&nbsp;domes/&lbrace;fips&rbrace;/&lbrace;archetype&rbrace;.json</p>
              <p>&nbsp;&nbsp;patterns/patterns-&lbrace;ts&rbrace;.json</p>
              <p>&nbsp;&nbsp;meta/</p>
              <p>&nbsp;&nbsp;&nbsp;&nbsp;sources.json</p>
              <p>&nbsp;&nbsp;&nbsp;&nbsp;coverage.json</p>
              <p>&nbsp;&nbsp;&nbsp;&nbsp;gaps.json</p>
              <p>&nbsp;&nbsp;cosm.json</p>
              <p className="text-white/50 mt-4 mb-3"># Schema architecture</p>
              <p>schema/</p>
              <p>&nbsp;&nbsp;dome.py &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# 12-layer person model</p>
              <p>&nbsp;&nbsp;sphere.py &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# 10-layer place model</p>
              <p>&nbsp;&nbsp;person_runner.py # The product</p>
              <p>&nbsp;&nbsp;fhir.py &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# FHIR R4 bridge</p>
              <p>&nbsp;&nbsp;sdoh.py &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# SDOH instruments</p>
              <p>&nbsp;&nbsp;dome_bond.py &nbsp;&nbsp;&nbsp;# Financial engine</p>
              <p>&nbsp;&nbsp;cosm_scoring.py &nbsp;# Auditable scoring</p>
            </div>
          </div>
        </div>
      </section>

      {/* ── CTA ──────────────────────────────────────────────── */}
      <section className="py-32 sm:py-40 px-6 bg-white text-center">
        <div className="max-w-3xl mx-auto">
          <h2 className="font-serif text-4xl sm:text-6xl leading-tight mb-6">
            The person at the center.<br />
            <em>Everything else is a layer.</em>
          </h2>
          <p className="text-lg text-black/50 mb-12 max-w-xl mx-auto leading-relaxed">
            Input a character. Get a production-ready dome with IP portfolio,
            business case, team plan, and a complete interactive website.
          </p>
          <Link
            to="/run"
            className="inline-block border-2 border-black bg-black text-white px-12 py-5 text-xl font-medium no-underline hover:bg-white hover:text-black transition-colors"
          >
            Run a Dome
          </Link>
        </div>
      </section>
    </div>
  );
}
