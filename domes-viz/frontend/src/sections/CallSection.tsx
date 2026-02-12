import { NARRATIVE_SECTIONS } from "../data/narrative";
import { AnimatedText } from "../scroll";

export function CallSection() {
  const data = NARRATIVE_SECTIONS.find((s) => s.id === "call");
  if (!data) return null;

  const ctas = data.ctas ?? [];

  return (
    <section id="call" className="bg-light text-dark">
      <div className="flex min-h-screen flex-col items-center justify-center px-6">
        <AnimatedText>
          <h2 className="font-serif text-[48px] font-bold leading-[1.1] text-dark md:text-[96px] lg:text-[120px]">
            {data.headline}
          </h2>
        </AnimatedText>
        {data.subline && (
          <AnimatedText delay={300}>
            <p className="mt-8 max-w-2xl text-center font-sans text-[18px] leading-[1.6] text-dark/60 md:mt-12 md:text-[24px]">
              {data.subline}
            </p>
          </AnimatedText>
        )}
      </div>

      <div className="px-6 pb-32 pt-8 md:px-12 lg:px-20">
        <div className="mx-auto grid max-w-5xl grid-cols-1 gap-0 border border-dark md:grid-cols-2">
          {ctas.map((cta, i) => (
            <a
              key={i}
              href={cta.href}
              className={`cta-card group flex flex-col justify-between border-dark p-8 transition-colors duration-300 hover:bg-dark hover:text-light md:p-12 ${
                i % 2 === 0 ? "md:border-r" : ""
              } ${i < 2 ? "border-b md:border-b" : i === 2 ? "border-b md:border-b-0" : ""}`}
            >
              <div>
                <h3 className="font-serif text-[28px] font-bold leading-tight md:text-[36px]">
                  {cta.label}
                </h3>
                <p className="mt-4 font-sans text-[14px] leading-[1.6] text-dark/60 transition-colors duration-300 group-hover:text-light/60 md:text-[16px]">
                  {cta.description}
                </p>
              </div>
              <div className="mt-8 flex items-center gap-2">
                <span className="font-mono text-xs tracking-widest uppercase transition-colors duration-300 group-hover:text-accent">
                  Enter
                </span>
                <span className="inline-block transition-transform duration-300 group-hover:translate-x-2">
                  &rarr;
                </span>
              </div>
            </a>
          ))}
        </div>
      </div>
    </section>
  );
}
