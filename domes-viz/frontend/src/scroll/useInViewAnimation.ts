import { useState, useEffect, useRef, useCallback } from "react";

interface InViewOptions {
  /** Intersection threshold 0-1, default 0.2 */
  threshold?: number;
  /** IntersectionObserver rootMargin, default "0px" */
  rootMargin?: string;
  /** Trigger animation only once, default true */
  once?: boolean;
}

interface InViewResult {
  /** Ref to attach to the target element */
  ref: React.RefObject<HTMLDivElement | null>;
  /** Whether the element is currently in the viewport */
  isInView: boolean;
  /** 0-1 scroll progress through the element */
  progress: number;
}

/**
 * Element visibility hook.
 *
 * Attaches to a ref, returns whether element is in viewport
 * and its individual scroll progress (0 at bottom of viewport, 1 at top).
 *
 * Uses IntersectionObserver for visibility detection and a passive
 * scroll listener for progress tracking (only active while in view).
 */
export function useInViewAnimation(options?: InViewOptions): InViewResult {
  const {
    threshold = 0.2,
    rootMargin = "0px",
    once = true,
  } = options ?? {};

  const ref = useRef<HTMLDivElement | null>(null);
  const [isInView, setIsInView] = useState(false);
  const [progress, setProgress] = useState(0);
  const hasTriggered = useRef(false);
  const rafId = useRef(0);

  // Progress calculation via scroll
  const updateProgress = useCallback(() => {
    const el = ref.current;
    if (!el) return;

    const rect = el.getBoundingClientRect();
    const elHeight = el.offsetHeight;

    if (elHeight <= 0) {
      setProgress(0);
      return;
    }

    // 0 when element top enters viewport bottom, 1 when element bottom exits viewport top
    const raw =
      (window.innerHeight - rect.top) / (window.innerHeight + elHeight);
    setProgress(Math.min(1, Math.max(0, raw)));
  }, []);

  const handleScroll = useCallback(() => {
    cancelAnimationFrame(rafId.current);
    rafId.current = requestAnimationFrame(updateProgress);
  }, [updateProgress]);

  // IntersectionObserver for visibility
  useEffect(() => {
    const el = ref.current;
    if (!el) return;

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            if (once && hasTriggered.current) return;
            hasTriggered.current = true;
            setIsInView(true);
          } else if (!once) {
            setIsInView(false);
          }
        });
      },
      { threshold, rootMargin },
    );

    observer.observe(el);

    return () => {
      observer.disconnect();
    };
  }, [threshold, rootMargin, once]);

  // Scroll listener for progress (only while in view, or always if once triggered)
  useEffect(() => {
    if (!isInView && !hasTriggered.current) return;

    window.addEventListener("scroll", handleScroll, { passive: true });
    // Compute initial progress
    handleScroll();

    return () => {
      window.removeEventListener("scroll", handleScroll);
      cancelAnimationFrame(rafId.current);
    };
  }, [isInView, handleScroll]);

  return { ref, isInView, progress };
}
