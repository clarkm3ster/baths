import {
  createContext,
  useContext,
  useMemo,
  useCallback,
  useEffect,
  useRef,
  useState,
} from "react";
import type { ActId } from "./useScrollProgress";
import { useScrollProgress } from "./useScrollProgress";

/* ------------------------------------------------------------------ */
/*  Color mapping per act                                             */
/* ------------------------------------------------------------------ */

interface ActColor {
  bg: [number, number, number];
  text: [number, number, number];
}

const ACT_COLORS: Record<ActId, ActColor> = {
  opening: { bg: [13, 13, 13], text: [245, 245, 245] },       // #0D0D0D -> #F5F5F5
  promise: { bg: [26, 26, 26], text: [245, 245, 245] },       // #1A1A1A -> #F5F5F5
  reality: { bg: [13, 13, 13], text: [245, 245, 245] },       // #0D0D0D -> #F5F5F5
  vision:  { bg: [26, 26, 26], text: [245, 245, 245] },       // start: #1A1A1A, transitions to #F5F5F5
  math:    { bg: [255, 255, 255], text: [13, 13, 13] },       // #FFFFFF -> #0D0D0D
  call:    { bg: [255, 255, 255], text: [13, 13, 13] },       // #FFFFFF -> #0D0D0D
};

/**
 * "vision" is the transition act -- it interpolates from dark to light.
 * We define its end-state separately so we can lerp during that act.
 */
const VISION_END: ActColor = {
  bg: [245, 245, 245],
  text: [13, 13, 13],
};

/* ------------------------------------------------------------------ */
/*  Act ordering for inter-act interpolation                          */
/* ------------------------------------------------------------------ */

const ACT_ORDER: ActId[] = [
  "opening",
  "promise",
  "reality",
  "vision",
  "math",
  "call",
];

/* ------------------------------------------------------------------ */
/*  Context                                                           */
/* ------------------------------------------------------------------ */

interface BackgroundColors {
  /** Current background color as CSS rgb string */
  bg: string;
  /** Current text color as CSS rgb string */
  text: string;
  /** Current background as [r, g, b] tuple */
  bgRgb: [number, number, number];
  /** Current text as [r, g, b] tuple */
  textRgb: [number, number, number];
}

const BackgroundContext = createContext<BackgroundColors>({
  bg: "rgb(13, 13, 13)",
  text: "rgb(245, 245, 245)",
  bgRgb: [13, 13, 13],
  textRgb: [245, 245, 245],
});

/**
 * Read the current background/text colors from any child component.
 */
export function useBackgroundColors(): BackgroundColors {
  return useContext(BackgroundContext);
}

/* ------------------------------------------------------------------ */
/*  Helpers                                                           */
/* ------------------------------------------------------------------ */

function lerpChannel(a: number, b: number, t: number): number {
  return Math.round(a + (b - a) * t);
}

function lerpColor(
  a: [number, number, number],
  b: [number, number, number],
  t: number,
): [number, number, number] {
  return [
    lerpChannel(a[0], b[0], t),
    lerpChannel(a[1], b[1], t),
    lerpChannel(a[2], b[2], t),
  ];
}

function rgbString(c: [number, number, number]): string {
  return `rgb(${c[0]}, ${c[1]}, ${c[2]})`;
}

/* ------------------------------------------------------------------ */
/*  Component                                                         */
/* ------------------------------------------------------------------ */

interface BackgroundTransitionProps {
  children: React.ReactNode;
}

/**
 * Background color manager.
 *
 * Renders a fixed full-screen div behind all content (z-index: -1)
 * that smoothly transitions between act-specific background colors
 * based on scroll position.
 *
 * Provides a context so any child can read the current bg/text colors
 * (useful for adapting SVG strokes, border colors, etc.)
 */
export function BackgroundTransition({ children }: BackgroundTransitionProps) {
  const { currentAct, actProgress, progress } = useScrollProgress();

  const computeColors = useCallback((): {
    bg: [number, number, number];
    text: [number, number, number];
  } => {
    const actIndex = ACT_ORDER.indexOf(currentAct);
    const actColor = ACT_COLORS[currentAct];

    // Special handling for "vision" act: interpolate from dark start to light end
    if (currentAct === "vision") {
      return {
        bg: lerpColor(actColor.bg, VISION_END.bg, actProgress),
        text: lerpColor(actColor.text, VISION_END.text, actProgress),
      };
    }

    // For other acts, interpolate between current act and next act
    // in the last 20% of the act (smooth lead-in to next section)
    const nextIndex = actIndex + 1;
    if (nextIndex < ACT_ORDER.length && actProgress > 0.8) {
      const nextAct = ACT_ORDER[nextIndex];
      const nextColor = ACT_COLORS[nextAct];
      // Map 0.8-1.0 to 0-1 for the transition
      const transitionT = (actProgress - 0.8) / 0.2;
      return {
        bg: lerpColor(actColor.bg, nextColor.bg, transitionT),
        text: lerpColor(actColor.text, nextColor.text, transitionT),
      };
    }

    return { bg: actColor.bg, text: actColor.text };
  }, [currentAct, actProgress]);

  // Use a ref + rAF for the background div to avoid re-renders on every scroll tick
  const bgRef = useRef<HTMLDivElement | null>(null);
  const [colors, setColors] = useState<BackgroundColors>(() => {
    const c = computeColors();
    return {
      bg: rgbString(c.bg),
      text: rgbString(c.text),
      bgRgb: c.bg,
      textRgb: c.text,
    };
  });

  useEffect(() => {
    const c = computeColors();
    const bgStr = rgbString(c.bg);
    const textStr = rgbString(c.text);

    // Direct DOM update for the background div (no React re-render needed)
    if (bgRef.current) {
      bgRef.current.style.backgroundColor = bgStr;
    }

    // Update context state (batched by React)
    setColors({
      bg: bgStr,
      text: textStr,
      bgRgb: c.bg,
      textRgb: c.text,
    });
  }, [computeColors, progress]);

  const contextValue = useMemo(() => colors, [colors]);

  return (
    <BackgroundContext.Provider value={contextValue}>
      {/* Fixed full-screen background layer */}
      <div
        ref={bgRef}
        style={{
          position: "fixed",
          inset: 0,
          zIndex: -1,
          backgroundColor: colors.bg,
          transition: "background-color 150ms linear",
          pointerEvents: "none",
        }}
        aria-hidden="true"
        data-scroll-animated="background"
      />
      {/* Set text color on content wrapper */}
      <div style={{ color: colors.text, position: "relative" }}>
        {children}
      </div>
    </BackgroundContext.Provider>
  );
}
