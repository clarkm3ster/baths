import { NARRATIVE_SECTIONS } from "../data/narrative";
import { AnimatedText, AnimatedCounter } from "../scroll";

export function MathSection() {
  const data = NARRATIVE_SECTIONS.find((s) => s.id === "math");
  if (!data) return null;

  const stats = data.stats ?? [];
  const sections = data.sections ?? [];

  return (
    <section id="math" className="bg-light text-dark">
      <div className="flex min-h-[60vh] items-center justify-center px-6">
        <AnimatedText>
          <h2 className="font-serif text-[40px] font-bold text-dark md:text-[72px]">
            {data.headline}
          </h2>
        </AnimatedText>
      </div>

      {stats.map((stat, i) => (
        <div
          key={i}
          className="flex min-h-screen flex-col items-center justify-center px-6"
        >
          <AnimatedCounter
            value={stat.value}
            prefix={stat.prefix}
            suffix={stat.suffix}
            label={stat.label}
            duration={2500}
            className="text-center text-dark"
          />

          {sections[i] && (
            <AnimatedText delay={400}>
              <p className="mt-16 max-w-2xl text-center font-serif text-[20px] leading-[1.5] text-dark/70 md:mt-24 md:text-[28px]">
                {sections[i]}
              </p>
            </AnimatedText>
          )}
        </div>
      ))}
    </section>
  );
}
