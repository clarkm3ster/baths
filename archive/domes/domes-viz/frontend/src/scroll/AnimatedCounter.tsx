import { useState, useEffect, useRef, useCallback } from "react";
import { useInViewAnimation } from "./useInViewAnimation";

interface AnimatedCounterProps {
  /** Target number to count up to */
  value: number;
  /** Text before the number, e.g. "$" */
  prefix?: string;
  /** Text after the number, e.g. "M" */
  suffix?: string;
  /** Descriptive label below the number */
  label: string;
  /** Animation duration in milliseconds, default 2000 */
  duration?: number;
  className?: string;
}

/** EaseOutQuart: decelerating to zero velocity */
function easeOutQuart(t: number): number {
  return 1 - Math.pow(1 - t, 4);
}

/**
 * Animated number count-up component.
 *
 * Counts from 0 to `value` over `duration` ms using easeOutQuart easing.
 * Only starts when the element enters the viewport.
 * Formats integers with locale-aware comma separators.
 * Respects prefers-reduced-motion by showing the final value immediately.
 */
export function AnimatedCounter({
  value,
  prefix = "",
  suffix = "",
  label,
  duration = 2000,
  className = "",
}: AnimatedCounterProps) {
  const { ref, isInView } = useInViewAnimation({
    threshold: 0.2,
    once: true,
  });

  const [displayValue, setDisplayValue] = useState(0);
  const hasStarted = useRef(false);
  const rafId = useRef(0);

  const prefersReducedMotion = useCallback(() => {
    return window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  }, []);

  useEffect(() => {
    if (!isInView || hasStarted.current) return;
    hasStarted.current = true;

    // Reduced motion: show final value immediately
    if (prefersReducedMotion()) {
      setDisplayValue(value);
      return;
    }

    const startTime = performance.now();

    function animate(now: number) {
      const elapsed = now - startTime;
      const rawProgress = Math.min(1, elapsed / duration);
      const easedProgress = easeOutQuart(rawProgress);

      setDisplayValue(Math.round(easedProgress * value));

      if (rawProgress < 1) {
        rafId.current = requestAnimationFrame(animate);
      } else {
        setDisplayValue(value);
      }
    }

    rafId.current = requestAnimationFrame(animate);

    return () => {
      cancelAnimationFrame(rafId.current);
    };
  }, [isInView, value, duration, prefersReducedMotion]);

  const formattedValue = displayValue.toLocaleString();

  return (
    <div
      ref={ref}
      className={className}
      style={{
        opacity: isInView ? 1 : 0,
        transform: isInView ? "none" : "translateY(16px)",
        transition: "opacity 600ms cubic-bezier(0.16, 1, 0.3, 1), transform 600ms cubic-bezier(0.16, 1, 0.3, 1)",
        willChange: "opacity, transform",
      }}
      data-scroll-animated="counter"
    >
      <span
        className="block font-mono text-[64px] font-bold leading-none md:text-[120px] lg:text-[160px]"
        style={{ fontVariantNumeric: "tabular-nums" }}
      >
        {prefix}
        {formattedValue}
        {suffix}
      </span>
      <span className="mt-6 block font-sans text-[18px] tracking-wide opacity-60 md:mt-8 md:text-[24px]">{label}</span>
    </div>
  );
}
