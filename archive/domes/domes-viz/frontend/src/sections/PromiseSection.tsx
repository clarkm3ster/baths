import { NARRATIVE_SECTIONS } from "../data/narrative";
import { AnimatedText } from "../scroll";
import { WorldRenderer } from "../worlds";

export function PromiseSection() {
  const data = NARRATIVE_SECTIONS.find((s) => s.id === "promise");
  if (!data) return null;

  const sections = data.sections ?? [];
  const keyStats = data.keyStats ?? [];

  return (
    <section id="promise">
      {sections.map((text, i) => (
        <div
          key={i}
          className="flex min-h-screen items-center justify-center px-6"
        >
          <AnimatedText delay={i * 100}>
            <p className="max-w-3xl text-center font-serif text-[28px] leading-[1.35] md:text-[48px] md:leading-[1.25]">
              {text}
            </p>
          </AnimatedText>
        </div>
      ))}

      <div className="flex min-h-[50vh] items-center justify-center px-6">
        <div className="flex flex-col items-center gap-8 md:flex-row md:gap-20">
          {keyStats.map((stat, i) => (
            <AnimatedText key={i} delay={i * 200}>
              <div className="text-center">
                <span className="block font-mono text-[64px] font-bold leading-none text-accent md:text-[96px]">
                  {stat.value}
                </span>
                <span className="mt-3 block font-sans text-sm tracking-widest text-muted uppercase md:text-base">
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
