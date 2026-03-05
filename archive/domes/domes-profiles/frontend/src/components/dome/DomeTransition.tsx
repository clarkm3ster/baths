/**
 * DomeTransition.tsx
 *
 * Toggle component + animation controller for switching between
 * FRAGMENTED and COORDINATED views of the dome.
 *
 * Features:
 * - Toggle switch: "FRAGMENTED" <-> "COORDINATED"
 * - Animated cost countdown when switching modes
 * - Cost difference shown prominently: "$79K -> $31K" with savings highlighted
 * - 800ms CSS transition duration
 */

import { useState, useEffect, useRef } from 'react';
import type { DomeMode, DomeTotals } from './types';

// ---------------------------------------------------------------------------
// Props
// ---------------------------------------------------------------------------

interface DomeTransitionProps {
  mode: DomeMode;
  onModeChange: (mode: DomeMode) => void;
  totals: DomeTotals;
}

// ---------------------------------------------------------------------------
// Animated number hook
// ---------------------------------------------------------------------------

function useAnimatedNumber(target: number, duration = 800): number {
  const [current, setCurrent] = useState(target);
  const rafRef = useRef<number>(0);
  const startRef = useRef(current);
  const startTimeRef = useRef(0);

  useEffect(() => {
    startRef.current = current;
    startTimeRef.current = performance.now();

    const animate = (now: number) => {
      const elapsed = now - startTimeRef.current;
      const progress = Math.min(elapsed / duration, 1);
      // Ease-out cubic
      const eased = 1 - Math.pow(1 - progress, 3);
      const value = startRef.current + (target - startRef.current) * eased;
      setCurrent(value);
      if (progress < 1) {
        rafRef.current = requestAnimationFrame(animate);
      }
    };

    rafRef.current = requestAnimationFrame(animate);
    return () => cancelAnimationFrame(rafRef.current);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [target, duration]);

  return current;
}

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

function formatCost(n: number): string {
  if (n >= 1_000_000) return `$${(n / 1_000_000).toFixed(1)}M`;
  if (n >= 1_000) return `$${Math.round(n / 1_000)}K`;
  return `$${Math.round(n)}`;
}

// ---------------------------------------------------------------------------
// Component
// ---------------------------------------------------------------------------

export default function DomeTransition({
  mode,
  onModeChange,
  totals,
}: DomeTransitionProps) {
  const isFragmented = mode === 'fragmented';
  const displayCost = useAnimatedNumber(
    isFragmented ? totals.annual_cost : totals.coordinated_cost,
    800,
  );

  return (
    <div className="flex flex-col items-center gap-3">
      {/* Toggle switch */}
      <div className="flex items-center gap-0 border border-black">
        <button
          onClick={() => onModeChange('fragmented')}
          className={[
            'px-4 py-2 text-xs font-mono tracking-widest uppercase transition-all duration-300',
            isFragmented
              ? 'bg-black text-white'
              : 'bg-white text-black hover:bg-gray-100',
          ].join(' ')}
          style={{ fontFamily: "'JetBrains Mono', monospace" }}
        >
          FRAGMENTED
        </button>
        <div className="w-px h-full bg-black" />
        <button
          onClick={() => onModeChange('coordinated')}
          className={[
            'px-4 py-2 text-xs font-mono tracking-widest uppercase transition-all duration-300',
            !isFragmented
              ? 'bg-black text-white'
              : 'bg-white text-black hover:bg-gray-100',
          ].join(' ')}
          style={{ fontFamily: "'JetBrains Mono', monospace" }}
        >
          COORDINATED
        </button>
      </div>

      {/* Cost display */}
      <div className="flex items-center gap-4">
        {/* Current cost */}
        <div className="text-center">
          <div
            className="text-2xl font-bold"
            style={{
              fontFamily: "'JetBrains Mono', monospace",
              color: isFragmented ? '#8B1A1A' : '#1A6B3C',
              transition: 'color 800ms ease',
            }}
          >
            {formatCost(displayCost)}
          </div>
          <div
            className="text-xs mt-0.5"
            style={{
              fontFamily: 'Inter, sans-serif',
              color: '#666',
            }}
          >
            annual cost
          </div>
        </div>

        {/* Arrow + savings */}
        <div className="flex flex-col items-center">
          <div
            className="text-xs font-mono"
            style={{
              fontFamily: "'JetBrains Mono', monospace",
              color: '#666',
            }}
          >
            {formatCost(totals.annual_cost)}
            <span className="mx-1" style={{ color: '#22c55e' }}>
              {' -> '}
            </span>
            {formatCost(totals.coordinated_cost)}
          </div>
          <div
            className="text-sm font-bold mt-0.5"
            style={{
              fontFamily: "'JetBrains Mono', monospace",
              color: '#22c55e',
            }}
          >
            SAVE {formatCost(totals.savings)}/yr
          </div>
        </div>
      </div>

      {/* Stats bar */}
      <div
        className="flex items-center gap-4 text-xs"
        style={{ fontFamily: 'Inter, sans-serif', color: '#888' }}
      >
        <span>
          <strong style={{ color: '#000' }}>{totals.systems_count}</strong> systems
        </span>
        <span
          style={{
            color: isFragmented ? '#8B1A1A' : '#22c55e',
            transition: 'color 800ms ease',
          }}
        >
          <strong>{totals.gaps_count}</strong> gaps
        </span>
        <span style={{ color: '#22c55e' }}>
          <strong>{totals.consent_closable}</strong> consent-closable
        </span>
        <span>
          5yr: <strong style={{ color: '#000', fontFamily: "'JetBrains Mono', monospace" }}>
            {formatCost(totals.five_year)}
          </strong>
        </span>
        <span>
          lifetime: <strong style={{ color: '#000', fontFamily: "'JetBrains Mono', monospace" }}>
            {formatCost(totals.lifetime)}
          </strong>
        </span>
      </div>
    </div>
  );
}
