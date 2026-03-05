import { useRef, useEffect, useCallback } from "react";

interface ParallaxSectionProps {
  children: React.ReactNode;
  /**
   * Speed multiplier for parallax effect.
   * - 0.5 = moves at half scroll speed (receding background feel)
   * - 1.0 = normal scroll (no parallax)
   * - 1.5 = moves faster than scroll (foreground feel)
   * Default: 0.5
   */
  speed?: number;
  className?: string;
  id?: string;
}

/**
 * Parallax scroll wrapper.
 *
 * Applies a translateY transform based on scroll position and speed multiplier.
 * Uses requestAnimationFrame for smooth 60fps updates.
 * GPU-accelerated via transform only.
 * Respects prefers-reduced-motion by disabling the parallax effect.
 */
export function ParallaxSection({
  children,
  speed = 0.5,
  className = "",
  id,
}: ParallaxSectionProps) {
  const containerRef = useRef<HTMLDivElement | null>(null);
  const rafId = useRef(0);
  const prefersReducedMotion = useRef(false);

  useEffect(() => {
    prefersReducedMotion.current = window.matchMedia(
      "(prefers-reduced-motion: reduce)",
    ).matches;
  }, []);

  const updatePosition = useCallback(() => {
    const el = containerRef.current;
    if (!el || prefersReducedMotion.current) return;

    const rect = el.getBoundingClientRect();
    const centerY = rect.top + rect.height / 2;
    const viewportCenter = window.innerHeight / 2;
    const offset = (centerY - viewportCenter) * (speed - 1);

    el.style.transform = `translateY(${offset}px)`;
  }, [speed]);

  const handleScroll = useCallback(() => {
    cancelAnimationFrame(rafId.current);
    rafId.current = requestAnimationFrame(updatePosition);
  }, [updatePosition]);

  useEffect(() => {
    window.addEventListener("scroll", handleScroll, { passive: true });
    // Initial position
    handleScroll();

    return () => {
      window.removeEventListener("scroll", handleScroll);
      cancelAnimationFrame(rafId.current);
    };
  }, [handleScroll]);

  return (
    <div
      ref={containerRef}
      id={id}
      className={className}
      style={{ willChange: "transform" }}
      data-scroll-animated="parallax"
    >
      {children}
    </div>
  );
}
