import { useScrollProgress } from "./useScrollProgress";

/**
 * Thin progress bar fixed to the top of the viewport.
 *
 * Shows overall scroll progress as a horizontal bar.
 * Color transitions from light on dark background to dark on light background
 * as the user scrolls through the narrative.
 *
 * Height: 2px, z-index: 50.
 */
export function ScrollProgress() {
  const { progress } = useScrollProgress();

  // Transition from a warm light color (on dark bg) to a dark color (on light bg)
  // At progress 0: light gold-ish for visibility on dark bg
  // At progress 1: dark charcoal for visibility on white bg
  const r = Math.round(196 - progress * 176); // 196 -> 20
  const g = Math.round(162 - progress * 142); // 162 -> 20
  const b = Math.round(101 - progress * 81);  // 101 -> 20
  const barColor = `rgb(${r}, ${g}, ${b})`;

  return (
    <div
      style={{
        position: "fixed",
        top: 0,
        left: 0,
        width: "100%",
        height: "2px",
        zIndex: 50,
        pointerEvents: "none",
      }}
      aria-hidden="true"
      data-scroll-animated="progress-track"
    >
      <div
        style={{
          height: "100%",
          width: `${progress * 100}%`,
          backgroundColor: barColor,
          transition: "background-color 300ms linear",
          willChange: "width",
        }}
        data-scroll-animated="progress-bar"
      />
    </div>
  );
}
