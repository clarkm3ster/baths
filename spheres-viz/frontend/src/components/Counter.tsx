import { useState, useEffect, useRef, useCallback } from 'react';
import { useInView } from '../hooks/useScrollProgress';

interface CounterProps {
  target: number;
  duration?: number;
  prefix?: string;
  suffix?: string;
  className?: string;
}

function easeOutExpo(t: number): number {
  return t === 1 ? 1 : 1 - Math.pow(2, -10 * t);
}

function formatNumber(n: number): string {
  return n.toLocaleString('en-US');
}

/**
 * Animated counter that counts from 0 to target.
 * Triggers when scrolled into view via IntersectionObserver.
 * Uses easeOutExpo easing for a cinematic deceleration.
 */
export default function Counter({
  target,
  duration = 2000,
  prefix = '',
  suffix = '',
  className = '',
}: CounterProps) {
  const [displayValue, setDisplayValue] = useState(0);
  const ref = useRef<HTMLSpanElement>(null);
  const hasAnimated = useRef(false);
  const inView = useInView(ref, { threshold: 0.3 });

  const animate = useCallback(() => {
    if (hasAnimated.current) return;
    hasAnimated.current = true;

    const startTime = performance.now();

    const tick = (now: number) => {
      const elapsed = now - startTime;
      const progress = Math.min(elapsed / duration, 1);
      const easedProgress = easeOutExpo(progress);
      const currentValue = Math.round(easedProgress * target);

      setDisplayValue(currentValue);

      if (progress < 1) {
        requestAnimationFrame(tick);
      }
    };

    requestAnimationFrame(tick);
  }, [target, duration]);

  useEffect(() => {
    if (inView && !hasAnimated.current) {
      animate();
    }
  }, [inView, animate]);

  return (
    <span ref={ref} className={className}>
      {prefix}
      {formatNumber(displayValue)}
      {suffix}
    </span>
  );
}
