import { NARRATIVE_SECTIONS } from "../data/narrative";
import { AnimatedText } from "../scroll";
import { WorldRenderer } from "../worlds";

const DOMAIN_COLORS: Record<number, string> = {
  0: "var(--color-health)",
  1: "var(--color-housing)",
  2: "var(--color-childwelfare)",
  3: "var(--color-income)",
  4: "var(--color-justice)",
  5: "var(--color-muted)",
};

export function RealitySection() {
  const data = NARRATIVE_SECTIONS.find((s) => s.id === "reality");
  if (!data) return null;

  const stops = data.marcusStops ?? [];
  const keyStats = data.keyStats ?? [];

  return (
    <section id="reality">
      <div className="flex min-h-[60vh] items-center justify-center px-6">
        <AnimatedText>
          <h2 className="font-serif text-[40px] font-bold md:text-[72px]">
            {data.headline}
          </h2>
        </AnimatedText>
      </div>

      {stops.map((stop, i) => (
        <div
          key={i}
          className="flex min-h-screen items-center justify-center px-6"
        >
          <AnimatedText delay={100}>
            <div className="max-w-3xl">
              <div className="mb-6 flex items-center gap-4">
                <span
                  className="inline-block h-3 w-3"
                  style={{ backgroundColor: DOMAIN_COLORS[i] }}
                />
                <span className="font-mono text-[36px] font-bold leading-none md:text-[64px]">
                  {stop.time}
                </span>
              </div>
              <p className="border-l-2 border-border pl-6 font-sans text-[20px] leading-[1.6] opacity-70 md:pl-8 md:text-[28px]">
                {stop.description}
              </p>
              <p className="mt-6 font-mono text-xs tracking-widest opacity-30 uppercase">
                Stop {i + 1} of {stops.length}
              </p>
            </div>
          </AnimatedText>
        </div>
      ))}

      <div className="flex min-h-[50vh] items-center justify-center px-6">
        <div className="grid grid-cols-2 gap-8 md:grid-cols-4 md:gap-16">
          {keyStats.map((stat, i) => (
            <AnimatedText key={i} delay={i * 150}>
              <div className="text-center">
                <span className="block font-mono text-[40px] font-bold leading-none md:text-[64px]">
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
