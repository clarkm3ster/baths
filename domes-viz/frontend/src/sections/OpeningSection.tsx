/**
 * OpeningSection — The hook.
 *
 * Full viewport, pure black. One devastating headline fades in.
 * "The government spends $79,000 a year on Marcus."
 * "Nothing gets better."
 *
 * Typography: Crimson Text serif, 72px desktop / 40px mobile.
 * Uses CSS animation on mount (no scroll hook dependency).
 */
export function OpeningSection() {
  return (
    <section
      id="opening"
      className="relative flex min-h-screen flex-col items-center justify-center bg-dark px-6"
    >
      <div className="max-w-4xl text-center">
        <h1 className="font-serif text-[40px] leading-[1.15] font-bold text-light opacity-0 animate-fade-in md:text-[72px] md:leading-[1.1]">
          The government spends $79,000 a year on Marcus.
        </h1>
        <p className="mt-8 font-serif text-[24px] leading-[1.4] text-muted opacity-0 animate-fade-in-delayed md:mt-12 md:text-[40px]">
          Nothing gets better.
        </p>
      </div>

      {/* Scroll indicator */}
      <div className="absolute bottom-12 left-1/2 -translate-x-1/2 opacity-0 animate-fade-in-slow">
        <div className="flex flex-col items-center gap-3">
          <span className="font-mono text-xs tracking-widest text-muted uppercase">
            Scroll
          </span>
          <div className="h-12 w-px bg-muted/40 animate-pulse" />
        </div>
      </div>
    </section>
  );
}
