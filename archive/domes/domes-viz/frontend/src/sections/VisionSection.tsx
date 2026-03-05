import { NARRATIVE_SECTIONS } from "../data/narrative";
import { AnimatedText } from "../scroll";
import { WorldRenderer } from "../worlds";

interface ComparisonRow {
  label: string;
  before: string;
  after: string;
}

const COMPARISONS: ComparisonRow[] = [
  { label: "Annual cost", before: "$79,000", after: "$31,000" },
  { label: "Agencies visited", before: "6", after: "1" },
  { label: "Coordinators", before: "0", after: "1" },
  { label: "Shared records", before: "0", after: "1" },
  { label: "Outcome trajectory", before: "Declining", after: "Improving" },
];

export function VisionSection() {
  const data = NARRATIVE_SECTIONS.find((s) => s.id === "vision");
  if (!data) return null;

  const sections = data.sections ?? [];
  const keyStats = data.keyStats ?? [];

  return (
    <section id="vision" className="vision-gradient">
      <div className="flex min-h-[60vh] items-center justify-center px-6">
        <AnimatedText>
          <h2 className="font-serif text-[40px] font-bold md:text-[72px]">
            {data.headline}
          </h2>
        </AnimatedText>
      </div>

      {sections.map((text, i) => (
        <div
          key={i}
          className="flex min-h-screen items-center justify-center px-6"
        >
          <AnimatedText delay={i * 80}>
            <p className="max-w-3xl text-center font-serif text-[28px] leading-[1.35] md:text-[48px] md:leading-[1.25]">
              {text}
            </p>
          </AnimatedText>
        </div>
      ))}

      <div className="flex min-h-[40vh] items-center justify-center px-6">
        <div className="grid grid-cols-2 gap-8 md:grid-cols-4 md:gap-16">
          {keyStats.map((stat, i) => (
            <AnimatedText key={i} delay={i * 150}>
              <div className="text-center">
                <span className="block font-mono text-[40px] font-bold leading-none text-accent md:text-[64px]">
                  {stat.value}
                </span>
                <span className="mt-2 block font-sans text-xs tracking-widest opacity-50 uppercase md:text-sm">
                  {stat.label}
                </span>
              </div>
            </AnimatedText>
          ))}
        </div>
      </div>

      <div className="flex min-h-[60vh] items-center justify-center px-6 py-20">
        <AnimatedText>
          <div className="w-full max-w-3xl">
            <h3 className="mb-12 text-center font-serif text-[28px] font-bold md:text-[40px]">
              Before vs. After
            </h3>
            <div className="border border-border">
              <div className="grid grid-cols-3 border-b border-border">
                <div className="p-4 font-mono text-xs tracking-widest opacity-50 uppercase md:p-6 md:text-sm">
                  Metric
                </div>
                <div className="border-l border-border p-4 text-center font-mono text-xs tracking-widest text-justice uppercase md:p-6 md:text-sm">
                  Before
                </div>
                <div className="border-l border-border p-4 text-center font-mono text-xs tracking-widest text-health uppercase md:p-6 md:text-sm">
                  After
                </div>
              </div>
              {COMPARISONS.map((row, i) => (
                <div
                  key={i}
                  className={`grid grid-cols-3 ${i < COMPARISONS.length - 1 ? "border-b border-border" : ""}`}
                >
                  <div className="p-4 font-sans text-sm opacity-50 md:p-6 md:text-base">
                    {row.label}
                  </div>
                  <div className="border-l border-border p-4 text-center font-mono text-sm opacity-60 md:p-6 md:text-base">
                    {row.before}
                  </div>
                  <div className="border-l border-border p-4 text-center font-mono text-sm font-bold md:p-6 md:text-base">
                    {row.after}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </AnimatedText>
      </div>

      {data.world && (
        <div className="border-y border-border">
          <WorldRenderer
            worldId={data.world.worldId as "renaissance" | "broken-capitol" | "personal-dome"}
            overlayText={data.world.overlayText}
          />
        </div>
      )}
    </section>
  );
}
