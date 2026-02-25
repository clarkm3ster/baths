import { Link } from 'react-router-dom';

const PRODUCTION_STAGES = [
  {
    stage: 'Development',
    duration: '44 days',
    milestones: [
      {
        title: 'Character Analysis & Swarm Query',
        desc: 'Analyze character circumstances. Query swarm intelligence for relevant patterns from prior domes. Generate initial dome schema.',
        deliverables: ['Character profile', 'Swarm briefing', 'Initial dome schema'],
        days: 14,
      },
      {
        title: 'AI Layer Population (1-9)',
        desc: 'AI agents fill layers 1-9. Legal navigator maps entitlements. Systems analyst maps fragmentation. Fiscal engine computes coordination economics. Health layer populated with FHIR R4. SDOH screening instruments applied.',
        deliverables: ['Legal landscape', 'Systems map', 'Fiscal model', 'Health layer', 'Housing data', 'Economic profile', 'Education data', 'Community map', 'Environmental data'],
        days: 30,
      },
    ],
  },
  {
    stage: 'Pre-Production',
    duration: '35 days',
    milestones: [
      {
        title: 'Team Assembly & IP Mapping',
        desc: 'Assemble the creative team. Map the IP surface area. Identify unlikely collisions between disciplines.',
        deliverables: ['Team roster', 'IP map', 'Collision predictions'],
        days: 21,
      },
      {
        title: 'Dome Bond Prospectus',
        desc: 'Generate the Dome Bond prospectus from Layer 3 data. Compute coordination savings, structure the bond, generate risk assessment.',
        deliverables: ['Dome Bond prospectus', 'Cost analysis', 'Risk assessment'],
        days: 14,
      },
    ],
  },
  {
    stage: 'Production',
    duration: '81 days',
    milestones: [
      {
        title: 'Human Layer Design (10-12)',
        desc: 'Creative team designs layers 10 (Autonomy), 11 (Creativity), 12 (Flourishing). Each layer gets discipline-specific creative inputs.',
        deliverables: ['Autonomy design', 'Creativity design', 'Flourishing design', 'Awe framework'],
        days: 60,
      },
      {
        title: 'Cross-Layer Integration & Simulation',
        desc: 'Run cross-layer queries. Generate whole-person simulation. Compare baseline vs. coordinated scenarios. Compute final Cosm score.',
        deliverables: ['Cross-layer analysis', 'Simulation results', 'Cosm score report'],
        days: 21,
      },
    ],
  },
  {
    stage: 'Post-Production',
    duration: '35 days',
    milestones: [
      {
        title: 'IP Portfolio Assembly',
        desc: 'Catalogue all IP generated. File protections. Build the IP portfolio with valuations.',
        deliverables: ['IP portfolio', 'IP filings'],
        days: 14,
      },
      {
        title: 'Dome Website & World Model',
        desc: 'Build the dome website. Render the world model. Create the interactive 12-layer explorer.',
        deliverables: ['Dome website', 'World model render', 'Layer explorer'],
        days: 21,
      },
    ],
  },
  {
    stage: 'Distribution',
    duration: '7 days',
    milestones: [
      {
        title: 'Pitch Assembly & Distribution',
        desc: 'Assemble the complete pitch: dome, IP portfolio, business case, simulation results, team, budget, website. Ready for management company or agent presentation.',
        deliverables: ['Pitch deck', 'Complete dome package'],
        days: 7,
      },
    ],
  },
];

const CREATIVE_DISCIPLINES = [
  { role: 'Director', desc: 'Visionary who sees the dome as a complete work — not just data, not just film, but a 12-layer whole-person architecture rendered as art.' },
  { role: 'Data Architect', desc: 'Designs the 12-layer data architecture. Wires AI agents to dome layers.' },
  { role: 'Narrative Designer', desc: 'Shapes the dome\'s story. Documentary treatment. Series bible.' },
  { role: 'Systems Analyst', desc: 'Maps government system fragmentation. Builds the coordination economics.' },
  { role: 'Architect', desc: 'Designs the physical/spatial dimension of the dome visualization.' },
  { role: 'Composer', desc: 'Scores the dome. Sonic environment for the world model.' },
  { role: 'Health Informaticist', desc: 'FHIR R4 integration. SDOH screening. Cross-layer health impacts.' },
  { role: 'Material Designer', desc: 'Material palette for the dome. Physical prototypes.' },
  { role: 'Movement Designer', desc: 'Choreographic notation for the dome experience. Accessibility pathways.' },
  { role: 'Financial Engineer', desc: 'Dome Bond structuring. Pay-for-success modeling.' },
];

const TECH_INNOVATIONS = [
  { title: 'Person-Runner Engine', desc: 'AI engine that generates complete dome productions from character + circumstances input.' },
  { title: 'Cross-Layer Query Engine', desc: 'Answers questions across dome layers. "Given this person\'s legal entitlements and health conditions, what is the optimal fiscal coordination?"' },
  { title: 'Cosm Scoring System', desc: 'Auditable scoring where every number has a source. Dome is only as strong as its weakest layer.' },
  { title: 'FHIR R4 ↔ Dome Bridge', desc: 'Bidirectional bridge between FHIR R4 health resources and dome layer 4.' },
  { title: 'SDOH Screening ↔ Dome', desc: 'Maps PRAPARE and AHC-HRSN screening instruments to dome layers.' },
  { title: 'Dome Bond Engine', desc: 'Computes social impact bond prospectuses from dome data. GO Lab / Social Finance methodologies.' },
];

export function ProductPage() {
  return (
    <div className="pt-20">
      {/* ── HERO ───────────────────────────────────────── */}
      <section className="py-24 sm:py-32 px-6 bg-white">
        <div className="max-w-4xl mx-auto">
          <p className="text-sm tracking-[0.4em] uppercase text-black/40 mb-4">
            The Product
          </p>
          <h1 className="font-serif text-5xl sm:text-6xl leading-tight mb-8">
            Person-Runner is the dome production engine.
          </h1>
          <p className="text-xl text-black/50 leading-relaxed max-w-3xl">
            You input a character and their circumstances — fictional or real.
            Person-Runner uses the complete dome architecture to generate a massive
            IP pitch, production plan, business case, and a complete website of the
            dome and everything that went into building it.
          </p>
        </div>
      </section>

      {/* ── WHAT YOU GET ───────────────────────────────────── */}
      <section className="py-24 px-6 bg-black text-white">
        <div className="max-w-6xl mx-auto">
          <h2 className="font-serif text-3xl sm:text-4xl mb-16">
            What Person-Runner generates
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-px bg-white/10">
            {[
              {
                title: 'Complete 12-Layer Dome',
                desc: 'Full dome schema with all layers populated. AI fills layers 1-9 from real data. Creative team specs for layers 10-12.',
              },
              {
                title: 'IP Portfolio (8+ domains)',
                desc: 'Documentary treatment, series bible, technology platforms, Dome Bond prospectus, policy brief, academic paper, product designs.',
              },
              {
                title: 'Production Budget & ROI',
                desc: 'Every dollar justified by the IP and outcomes it generates. Team costs, technology, data, creative, legal. Full ROI projection.',
              },
              {
                title: 'Team Assembly Plan',
                desc: 'Director and multi-disciplinary creative team. Each role mapped to the dome layers and IP domains they enable.',
              },
              {
                title: 'Whole-Person Simulation',
                desc: 'Fragmented vs. coordinated comparison. Baseline costs, coordination savings, intervention priorities. Cosm scoring across all 12 layers.',
              },
              {
                title: 'Dome Website',
                desc: 'A complete interactive website showing the dome and everything that went into building it. Layer explorer, IP showcase, business case, timeline.',
              },
              {
                title: 'Tech Innovations Catalogue',
                desc: 'Every technology innovation discovered or created during production. Patent potential, open-source candidates, reusability.',
              },
              {
                title: 'Pitch Deck',
                desc: 'Management-company-ready: The Person, The Problem, The Dome, The Coordination, The IP, The Business Case, The Bond, The Team, The Ask.',
              },
            ].map((item) => (
              <div key={item.title} className="p-8 bg-black">
                <h3 className="font-serif text-xl mb-3">{item.title}</h3>
                <p className="text-sm text-white/50 leading-relaxed">{item.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── PRODUCTION TIMELINE ────────────────────────────── */}
      <section className="py-24 sm:py-32 px-6 bg-white">
        <div className="max-w-5xl mx-auto">
          <p className="text-sm tracking-[0.4em] uppercase text-black/40 mb-4">
            Production Pipeline
          </p>
          <h2 className="font-serif text-3xl sm:text-4xl mb-4">
            202 days from character to complete dome
          </h2>
          <p className="text-lg text-black/50 mb-16 max-w-2xl">
            Blockbuster timeline. Indie and Micro productions compress stages.
            Every milestone produces deliverables. Every deliverable generates IP.
          </p>

          <div className="space-y-12">
            {PRODUCTION_STAGES.map((stage) => (
              <div key={stage.stage} className="border-l-2 border-black pl-8 relative">
                <div className="absolute -left-2.5 top-0 w-5 h-5 bg-black" />
                <div className="flex items-baseline gap-4 mb-6">
                  <h3 className="font-serif text-2xl">{stage.stage}</h3>
                  <span className="font-mono text-sm text-black/30">{stage.duration}</span>
                </div>
                <div className="space-y-6">
                  {stage.milestones.map((milestone) => (
                    <div key={milestone.title} className="bg-[#FAFAFA] p-6">
                      <div className="flex items-baseline justify-between mb-2">
                        <h4 className="font-medium">{milestone.title}</h4>
                        <span className="font-mono text-xs text-black/30">{milestone.days}d</span>
                      </div>
                      <p className="text-sm text-black/50 mb-4 leading-relaxed">{milestone.desc}</p>
                      <div className="flex flex-wrap gap-2">
                        {milestone.deliverables.map((d) => (
                          <span key={d} className="text-xs bg-black/5 px-2 py-1 text-black/40 font-mono">
                            {d}
                          </span>
                        ))}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── CREATIVE TEAM ──────────────────────────────────── */}
      <section className="py-24 px-6 bg-[#FAFAFA]">
        <div className="max-w-6xl mx-auto">
          <p className="text-sm tracking-[0.4em] uppercase text-black/40 mb-4">
            Multi-Disciplinary Team
          </p>
          <h2 className="font-serif text-3xl sm:text-4xl mb-16">
            The team the dome assembles
          </h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-px bg-border">
            {CREATIVE_DISCIPLINES.map((d) => (
              <div key={d.role} className="p-6 bg-white">
                <h3 className="font-serif text-lg mb-2">{d.role}</h3>
                <p className="text-sm text-black/50 leading-relaxed">{d.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── TECH INNOVATIONS ───────────────────────────────── */}
      <section className="py-24 px-6 bg-black text-white">
        <div className="max-w-6xl mx-auto">
          <p className="text-sm tracking-[0.4em] uppercase text-white/40 mb-4">
            Technology
          </p>
          <h2 className="font-serif text-3xl sm:text-4xl mb-16">
            Every dome creates tech.
          </h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8">
            {TECH_INNOVATIONS.map((t) => (
              <div key={t.title} className="border border-white/10 p-6">
                <h3 className="font-serif text-lg mb-3">{t.title}</h3>
                <p className="text-sm text-white/40 leading-relaxed">{t.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── THE DOME BOND ──────────────────────────────────── */}
      <section className="py-24 sm:py-32 px-6 bg-white">
        <div className="max-w-4xl mx-auto">
          <p className="text-sm tracking-[0.4em] uppercase text-black/40 mb-4">
            Financial Innovation
          </p>
          <h2 className="font-serif text-4xl sm:text-5xl leading-tight mb-8">
            The Dome Bond
          </h2>
          <p className="text-xl text-black/50 leading-relaxed mb-12">
            Social impact bond structured from dome data. Every dome production
            measures the cost of system fragmentation and the savings from coordination.
            The delta becomes a financial instrument. Real cost references, GO Lab /
            Social Finance methodologies, real precedents.
          </p>
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-px bg-border">
            <div className="p-8 bg-[#FAFAFA] text-center">
              <p className="font-serif text-3xl mb-2">~$20K</p>
              <p className="text-sm text-black/40">per system per year<br />fragmented cost</p>
            </div>
            <div className="p-8 bg-[#FAFAFA] text-center">
              <p className="font-serif text-3xl mb-2">55%</p>
              <p className="text-sm text-black/40">cost reduction<br />through coordination</p>
            </div>
            <div className="p-8 bg-[#FAFAFA] text-center">
              <p className="font-serif text-3xl mb-2">5-year</p>
              <p className="text-sm text-black/40">bond horizon<br />70% capture rate</p>
            </div>
          </div>
          <div className="mt-8 p-6 bg-[#FAFAFA] text-sm text-black/40 leading-relaxed">
            <p className="font-medium text-black/60 mb-2">Precedents:</p>
            <p>Massachusetts Juvenile Justice PFS ($18M) &middot; Denver SIB Supportive Housing ($8.6M) &middot; Cuyahoga County Partnering for Family Success ($4M)</p>
          </div>
        </div>
      </section>

      {/* ── CTA ──────────────────────────────────────────── */}
      <section className="py-24 sm:py-32 px-6 bg-black text-white text-center">
        <div className="max-w-3xl mx-auto">
          <h2 className="font-serif text-4xl sm:text-5xl leading-tight mb-8">
            Ready to run a dome?
          </h2>
          <p className="text-lg text-white/40 mb-12">
            Input a character and their circumstances. Get everything you need
            to pitch, fund, and execute the dome.
          </p>
          <Link
            to="/run"
            className="inline-block border-2 border-white bg-white text-black px-12 py-5 text-xl font-medium no-underline hover:bg-transparent hover:text-white transition-colors"
          >
            Run a Dome
          </Link>
        </div>
      </section>
    </div>
  );
}
