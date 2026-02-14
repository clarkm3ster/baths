import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import {
  FileText,
  Scale,
  Landmark,
  BarChart3,
  Shield,
  Calculator,
  ArrowRight,
  ChevronDown,
} from "lucide-react";

const SECTIONS = [
  {
    icon: FileText,
    to: "/permits",
    title: "Permit Navigator",
    desc: "Every permit pathway for activating public space in Philadelphia. Select a parcel type and activation — get the exact steps, timeline, and cost.",
  },
  {
    icon: Scale,
    to: "/contracts",
    title: "Contract Generator",
    desc: "Generate legally sound agreements for space activation. Temporary use licenses, revenue sharing, community benefit agreements — all with Philadelphia-specific terms.",
  },
  {
    icon: Landmark,
    to: "/policy",
    title: "Policy Library",
    desc: "Model legislation for transforming how cities handle public space. The SPHERES Act, Right to Activate, pooled liability — ready to introduce.",
  },
  {
    icon: BarChart3,
    to: "/comparative",
    title: "Comparative Analysis",
    desc: "How does Philadelphia stack up? Six global cities compared on space activation policy, with lessons and scores.",
  },
  {
    icon: Shield,
    to: "/equity",
    title: "Equity Dashboard",
    desc: "Which neighborhoods have the most dormant space and the least activation? Priority scoring that puts equity first.",
  },
  {
    icon: Calculator,
    to: "/cost",
    title: "Cost Calculator",
    desc: "Total legal and permit cost for an activation from start to finish. No surprises.",
  },
];

export default function LandingPage() {
  const [entered, setEntered] = useState(false);
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    const t = setTimeout(() => setVisible(true), 100);
    return () => clearTimeout(t);
  }, []);

  return (
    <div className="min-h-screen bg-void text-snow">
      {/* Gateway */}
      {!entered && (
        <div
          className="fixed inset-0 z-50 flex flex-col items-center justify-center bg-void transition-opacity duration-700"
          style={{ opacity: entered ? 0 : 1 }}
        >
          <div
            className="text-center transition-all duration-1000"
            style={{
              opacity: visible ? 1 : 0,
              transform: visible ? "translateY(0)" : "translateY(20px)",
            }}
          >
            <p className="section-label mb-8">SPHERES LEGAL</p>
            <h1 className="text-3xl md:text-5xl font-light leading-tight max-w-3xl mx-auto mb-4 tracking-tight">
              Public space is already yours.
              <br />
              <span className="text-legal-green font-medium">
                Now make it usable.
              </span>
            </h1>
            <p className="text-silver text-lg mt-6 max-w-xl mx-auto">
              Every permit. Every contract. Every legal pathway
              <br />
              to activating the land that belongs to you.
            </p>
            <button
              onClick={() => setEntered(true)}
              className="btn-primary mt-12"
            >
              Enter <ArrowRight size={16} />
            </button>
          </div>
        </div>
      )}

      {/* Main content */}
      <div
        className="transition-all duration-1000"
        style={{
          opacity: entered ? 1 : 0,
          transform: entered ? "translateY(0)" : "translateY(40px)",
        }}
      >
        {/* Hero */}
        <section className="pt-32 pb-20 px-6">
          <div className="max-w-5xl mx-auto">
            <p className="section-label mb-6">LEGAL INFRASTRUCTURE</p>
            <h1 className="text-4xl md:text-6xl font-light leading-tight tracking-tight mb-8">
              SPHERES makes dormant
              <br />
              public space{" "}
              <span className="text-legal-green font-medium">visible</span>.
              <br />
              This makes it{" "}
              <span className="text-legal-green font-medium">usable</span>.
            </h1>
            <p className="text-silver text-lg max-w-2xl leading-relaxed">
              Every permit type. Every agreement template. Every policy model.
              The complete legal infrastructure for activating publicly-owned
              land in Philadelphia — and a legislative blueprint for any city.
            </p>
          </div>
        </section>

        {/* Scroll indicator */}
        <div className="flex justify-center pb-12">
          <ChevronDown size={24} className="text-steel animate-bounce" />
        </div>

        {/* Section grid */}
        <section className="px-6 pb-32">
          <div className="max-w-5xl mx-auto grid grid-cols-1 md:grid-cols-2 gap-px bg-ash">
            {SECTIONS.map((s, i) => (
              <Link
                key={s.to}
                to={s.to}
                className="card group flex flex-col gap-4 bg-void hover:bg-smoke transition-colors"
                style={{
                  animationDelay: `${i * 100}ms`,
                }}
              >
                <div className="flex items-center gap-3">
                  <s.icon
                    size={20}
                    className="text-legal-green"
                    strokeWidth={1.5}
                  />
                  <h2 className="text-lg font-medium tracking-tight">
                    {s.title}
                  </h2>
                </div>
                <p className="text-silver text-sm leading-relaxed">{s.desc}</p>
                <div className="flex items-center gap-2 text-legal-green text-xs font-mono font-medium mt-auto pt-4 opacity-0 group-hover:opacity-100 transition-opacity">
                  EXPLORE <ArrowRight size={14} />
                </div>
              </Link>
            ))}
          </div>
        </section>

        {/* Stats bar */}
        <section className="border-t border-ash px-6 py-16">
          <div className="max-w-5xl mx-auto grid grid-cols-2 md:grid-cols-4 gap-8">
            {[
              { label: "Permit Types", value: "14+" },
              { label: "Agreement Templates", value: "10" },
              { label: "Model Legislation", value: "4" },
              { label: "Cities Compared", value: "6" },
            ].map((stat) => (
              <div key={stat.label}>
                <p className="data-value">{stat.value}</p>
                <p className="data-label mt-1">{stat.label}</p>
              </div>
            ))}
          </div>
        </section>
      </div>
    </div>
  );
}
