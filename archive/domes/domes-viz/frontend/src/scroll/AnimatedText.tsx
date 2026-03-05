import { useMemo } from "react";
import { useInViewAnimation } from "./useInViewAnimation";

interface AnimatedTextProps {
  children: React.ReactNode;
  /** Delay in milliseconds for staggered reveals */
  delay?: number;
  /** Direction the text slides in from */
  direction?: "up" | "down" | "left" | "right" | "none";
  className?: string;
}

/**
 * Text fade-in component.
 *
 * Fades text in with an optional directional slide when it enters the viewport.
 * Uses CSS transitions on opacity and transform only (GPU-accelerated).
 * Respects prefers-reduced-motion by disabling transforms.
 */
export function AnimatedText({
  children,
  delay = 0,
  direction = "up",
  className = "",
}: AnimatedTextProps) {
  const { ref, isInView } = useInViewAnimation({
    threshold: 0.2,
    once: true,
  });

  const initialTransform = useMemo(() => {
    switch (direction) {
      case "up":
        return "translateY(24px)";
      case "down":
        return "translateY(-24px)";
      case "left":
        return "translateX(24px)";
      case "right":
        return "translateX(-24px)";
      case "none":
        return "none";
    }
  }, [direction]);

  const style: React.CSSProperties = {
    opacity: isInView ? 1 : 0,
    transform: isInView ? "none" : initialTransform,
    transition: `opacity 800ms cubic-bezier(0.16, 1, 0.3, 1) ${delay}ms, transform 800ms cubic-bezier(0.16, 1, 0.3, 1) ${delay}ms`,
    willChange: "opacity, transform",
  };

  return (
    <div
      ref={ref}
      className={className}
      style={style}
      data-scroll-animated="text"
    >
      {children}
    </div>
  );
}
