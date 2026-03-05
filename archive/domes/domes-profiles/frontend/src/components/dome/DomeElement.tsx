/**
 * DomeElement.tsx
 *
 * Renders an individual system (rectangle) or provision (diamond) within
 * a dome panel sector. Positioned absolutely via x/y props that the parent
 * layout algorithm computes. Shows cost in JetBrains Mono, label in Inter,
 * and a tooltip on hover with full details.
 */

import { useState } from 'react';
import type { DomeSystem, DomeMode } from './types';

// ---------------------------------------------------------------------------
// Props
// ---------------------------------------------------------------------------

interface DomeElementProps {
  system: DomeSystem;
  x: number;
  y: number;
  color: string;
  mode: DomeMode;
  isProvision?: boolean;
  onClick?: (systemId: string) => void;
}

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

const RECT_W = 56;
const RECT_H = 28;
const DIAMOND_SIZE = 10;

function formatCost(n: number): string {
  if (n >= 1_000_000) return `$${(n / 1_000_000).toFixed(1)}M`;
  if (n >= 1_000) return `$${(n / 1_000).toFixed(0)}K`;
  return `$${n.toFixed(0)}`;
}

// ---------------------------------------------------------------------------
// Component
// ---------------------------------------------------------------------------

export default function DomeElement({
  system,
  x,
  y,
  color,
  mode,
  isProvision = false,
  onClick,
}: DomeElementProps) {
  const [hovered, setHovered] = useState(false);

  const cost = mode === 'fragmented' ? system.annual_cost : system.coordinated_cost;
  const label = system.acronym || system.name.slice(0, 6);

  const handleClick = () => onClick?.(system.id);

  // ------- Provision diamond -------
  if (isProvision) {
    const points = [
      `${x},${y - DIAMOND_SIZE}`,
      `${x + DIAMOND_SIZE},${y}`,
      `${x},${y + DIAMOND_SIZE}`,
      `${x - DIAMOND_SIZE},${y}`,
    ].join(' ');

    return (
      <g
        className="dome-element"
        onMouseEnter={() => setHovered(true)}
        onMouseLeave={() => setHovered(false)}
        onClick={handleClick}
        style={{ cursor: 'pointer' }}
      >
        <polygon
          points={points}
          fill={hovered ? color : `${color}22`}
          stroke={color}
          strokeWidth={hovered ? 2 : 1}
          style={{ transition: 'all 0.2s ease' }}
        />
        {hovered && (
          <g className="dome-element-tooltip">
            <rect
              x={x + 14}
              y={y - 32}
              width={Math.max(system.name.length * 7, 80)}
              height={40}
              fill="#000"
              fillOpacity={0.92}
              rx={0}
            />
            <text
              x={x + 18}
              y={y - 16}
              fill="#fff"
              fontSize={11}
              fontFamily="Inter, sans-serif"
            >
              {system.name}
            </text>
            <text
              x={x + 18}
              y={y - 2}
              fill="#0f0"
              fontSize={10}
              fontFamily="'JetBrains Mono', monospace"
            >
              {formatCost(cost)}
            </text>
          </g>
        )}
      </g>
    );
  }

  // ------- System rectangle -------
  const rx = x - RECT_W / 2;
  const ry = y - RECT_H / 2;

  return (
    <g
      className="dome-element"
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={() => setHovered(false)}
      onClick={handleClick}
      style={{ cursor: 'pointer' }}
    >
      <rect
        x={rx}
        y={ry}
        width={RECT_W}
        height={RECT_H}
        fill={hovered ? `${color}30` : `${color}14`}
        stroke={color}
        strokeWidth={hovered ? 2 : 1}
        style={{ transition: 'all 0.2s ease' }}
      />
      {/* Label */}
      <text
        x={x}
        y={y - 2}
        textAnchor="middle"
        dominantBaseline="middle"
        fill={color}
        fontSize={9}
        fontFamily="Inter, sans-serif"
        fontWeight={600}
      >
        {label}
      </text>
      {/* Cost */}
      <text
        x={x}
        y={y + 10}
        textAnchor="middle"
        dominantBaseline="middle"
        fill={color}
        fontSize={8}
        fontFamily="'JetBrains Mono', monospace"
        opacity={0.8}
      >
        {formatCost(cost)}
      </text>

      {/* Tooltip */}
      {hovered && (
        <g className="dome-element-tooltip">
          <rect
            x={x + RECT_W / 2 + 6}
            y={y - 36}
            width={Math.max(system.name.length * 6.5 + 16, 100)}
            height={52}
            fill="#000"
            fillOpacity={0.94}
            rx={0}
          />
          <text
            x={x + RECT_W / 2 + 14}
            y={y - 20}
            fill="#fff"
            fontSize={11}
            fontFamily="Inter, sans-serif"
            fontWeight={600}
          >
            {system.name}
          </text>
          <text
            x={x + RECT_W / 2 + 14}
            y={y - 6}
            fill="#ccc"
            fontSize={9}
            fontFamily="Inter, sans-serif"
          >
            {system.domain}
          </text>
          <text
            x={x + RECT_W / 2 + 14}
            y={y + 8}
            fill={mode === 'coordinated' ? '#4ade80' : '#f87171'}
            fontSize={10}
            fontFamily="'JetBrains Mono', monospace"
          >
            {formatCost(cost)}/yr
          </text>
        </g>
      )}
    </g>
  );
}
