import { useState, useEffect, useCallback, useRef } from "react";

/**
 * Act definitions mapping section IDs to their narrative position.
 * Sections must appear in DOM order for correct act detection.
 */
const ACT_IDS = [
  "opening",
  "promise",
  "reality",
  "vision",
  "math",
  "call",
] as const;

export type ActId = (typeof ACT_IDS)[number];

interface ScrollProgressState {
  /** 0-1 overall page scroll progress */
  progress: number;
  /** Which act section is currently in view */
  currentAct: ActId;
  /** 0-1 progress within the current act */
  actProgress: number;
}

/**
 * Core scroll tracking hook.
 *
 * Returns a 0-1 progress value for overall page scroll,
 * the current act section in view, and 0-1 progress within that act.
 *
 * Uses passive scroll listeners and IntersectionObserver for efficiency.
 * Respects reduced-motion preference by still tracking position without animation cost.
 */
export function useScrollProgress(): ScrollProgressState {
  const [state, setState] = useState<ScrollProgressState>({
    progress: 0,
    currentAct: "opening",
    actProgress: 0,
  });

  const rafId = useRef(0);
  const currentActRef = useRef<ActId>("opening");

  // IntersectionObserver to detect which act section is visible
  useEffect(() => {
    const observers: IntersectionObserver[] = [];

    ACT_IDS.forEach((id) => {
      const el = document.getElementById(id);
      if (!el) return;

      const observer = new IntersectionObserver(
        (entries) => {
          entries.forEach((entry) => {
            if (entry.isIntersecting) {
              currentActRef.current = id;
            }
          });
        },
        {
          threshold: 0.3,
          rootMargin: "-10% 0px -10% 0px",
        },
      );

      observer.observe(el);
      observers.push(observer);
    });

    return () => {
      observers.forEach((o) => o.disconnect());
    };
  }, []);

  // Scroll listener for progress calculation
  const handleScroll = useCallback(() => {
    cancelAnimationFrame(rafId.current);

    rafId.current = requestAnimationFrame(() => {
      const scrollTop = window.scrollY;
      const docHeight =
        document.documentElement.scrollHeight - window.innerHeight;
      const overallProgress = docHeight > 0 ? Math.min(1, Math.max(0, scrollTop / docHeight)) : 0;

      // Calculate progress within current act
      let actProgress = 0;
      const actId = currentActRef.current;
      const actEl = document.getElementById(actId);

      if (actEl) {
        const rect = actEl.getBoundingClientRect();
        const actHeight = actEl.offsetHeight;
        if (actHeight > 0) {
          // rect.top goes from positive (below viewport top) to negative (scrolled past)
          // Progress: 0 when top of section at viewport bottom, 1 when bottom of section at viewport top
          const raw = (window.innerHeight - rect.top) / (window.innerHeight + actHeight);
          actProgress = Math.min(1, Math.max(0, raw));
        }
      }

      setState({
        progress: overallProgress,
        currentAct: actId,
        actProgress,
      });
    });
  }, []);

  useEffect(() => {
    window.addEventListener("scroll", handleScroll, { passive: true });
    // Initial calculation
    handleScroll();

    return () => {
      window.removeEventListener("scroll", handleScroll);
      cancelAnimationFrame(rafId.current);
    };
  }, [handleScroll]);

  return state;
}
