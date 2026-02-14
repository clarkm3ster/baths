import { useState, useEffect, useCallback, useRef, RefObject } from 'react';

interface ScrollState {
  scrollY: number;
  scrollProgress: number;
  viewportHeight: number;
  activeEpisodeIndex: number;
}

/**
 * Primary scroll tracking hook.
 * Returns scrollY, overall page progress (0-1), viewport height,
 * and the index of the currently active episode.
 *
 * Layout assumptions (in vh):
 *   Opening:   100vh
 *   Per episode: 200vh content + 50vh map transition = 250vh each
 *   Finale:    150vh
 *   Total:     100 + (10 * 250) + 150 = 2750vh
 */
export function useScrollProgress(): ScrollState {
  const [state, setState] = useState<ScrollState>({
    scrollY: 0,
    scrollProgress: 0,
    viewportHeight: typeof window !== 'undefined' ? window.innerHeight : 900,
    activeEpisodeIndex: -1,
  });

  const rafId = useRef<number>(0);
  const ticking = useRef(false);

  const update = useCallback(() => {
    const scrollY = window.scrollY;
    const vh = window.innerHeight;
    const docHeight = document.documentElement.scrollHeight - vh;
    const scrollProgress = docHeight > 0 ? Math.min(scrollY / docHeight, 1) : 0;

    // Determine which episode is active
    const openingEnd = vh; // 100vh
    const episodeBlockSize = 2.5 * vh; // 200vh + 50vh transition

    let activeEpisodeIndex = -1;
    if (scrollY >= openingEnd) {
      const scrollIntoEpisodes = scrollY - openingEnd;
      const rawIndex = Math.floor(scrollIntoEpisodes / episodeBlockSize);
      activeEpisodeIndex = Math.min(rawIndex, 9);
    }

    setState({
      scrollY,
      scrollProgress,
      viewportHeight: vh,
      activeEpisodeIndex,
    });

    ticking.current = false;
  }, []);

  const onScroll = useCallback(() => {
    if (!ticking.current) {
      ticking.current = true;
      rafId.current = requestAnimationFrame(update);
    }
  }, [update]);

  useEffect(() => {
    window.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('resize', update, { passive: true });
    // Initial measurement
    update();

    return () => {
      window.removeEventListener('scroll', onScroll);
      window.removeEventListener('resize', update);
      if (rafId.current) cancelAnimationFrame(rafId.current);
    };
  }, [onScroll, update]);

  return state;
}

/**
 * Returns 0-1 progress of an element through the viewport.
 * 0 = element top is at viewport bottom
 * 1 = element bottom is at viewport top
 * Clamps to [0, 1].
 */
export function useElementProgress(ref: RefObject<HTMLElement | null>): number {
  const [progress, setProgress] = useState(0);
  const rafId = useRef<number>(0);
  const ticking = useRef(false);

  const update = useCallback(() => {
    if (!ref.current) return;
    const rect = ref.current.getBoundingClientRect();
    const vh = window.innerHeight;
    const elementHeight = rect.height;

    // When element top is at viewport bottom -> 0
    // When element bottom is at viewport top -> 1
    const totalTravel = vh + elementHeight;
    const traveled = vh - rect.top;
    const raw = traveled / totalTravel;
    setProgress(Math.max(0, Math.min(1, raw)));
    ticking.current = false;
  }, [ref]);

  const onScroll = useCallback(() => {
    if (!ticking.current) {
      ticking.current = true;
      rafId.current = requestAnimationFrame(update);
    }
  }, [update]);

  useEffect(() => {
    window.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('resize', update, { passive: true });
    update();
    return () => {
      window.removeEventListener('scroll', onScroll);
      window.removeEventListener('resize', update);
      if (rafId.current) cancelAnimationFrame(rafId.current);
    };
  }, [onScroll, update]);

  return progress;
}

/**
 * Returns 0-1 progress within a specific section of the page.
 * sectionStart / sectionEnd in pixels.
 */
export function useSectionProgress(
  sectionStartVh: number,
  sectionEndVh: number,
): number {
  const [progress, setProgress] = useState(0);
  const rafId = useRef<number>(0);
  const ticking = useRef(false);

  const update = useCallback(() => {
    const vh = window.innerHeight;
    const scrollY = window.scrollY;
    const startPx = sectionStartVh * vh;
    const endPx = sectionEndVh * vh;
    const range = endPx - startPx;
    if (range <= 0) {
      setProgress(0);
      ticking.current = false;
      return;
    }
    const raw = (scrollY - startPx) / range;
    setProgress(Math.max(0, Math.min(1, raw)));
    ticking.current = false;
  }, [sectionStartVh, sectionEndVh]);

  const onScroll = useCallback(() => {
    if (!ticking.current) {
      ticking.current = true;
      rafId.current = requestAnimationFrame(update);
    }
  }, [update]);

  useEffect(() => {
    window.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('resize', update, { passive: true });
    update();
    return () => {
      window.removeEventListener('scroll', onScroll);
      window.removeEventListener('resize', update);
      if (rafId.current) cancelAnimationFrame(rafId.current);
    };
  }, [onScroll, update]);

  return progress;
}

/**
 * Hook to detect when an element is in the viewport.
 * Uses IntersectionObserver for performance.
 */
export function useInView(
  ref: RefObject<HTMLElement | null>,
  options?: IntersectionObserverInit,
): boolean {
  const [inView, setInView] = useState(false);

  useEffect(() => {
    if (!ref.current) return;
    const observer = new IntersectionObserver(([entry]) => {
      setInView(entry.isIntersecting);
    }, options);

    observer.observe(ref.current);
    return () => observer.disconnect();
  }, [ref, options?.threshold, options?.rootMargin]);

  return inView;
}
