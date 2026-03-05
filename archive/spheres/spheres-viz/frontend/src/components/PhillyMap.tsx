import { useMemo } from 'react';
import { EPISODES } from '../data/episodes';

interface PhillyMapProps {
  activatedEpisodes: number[]; // episode numbers (1-10) that should glow
  size?: 'mini' | 'large';
  className?: string;
}

/**
 * Simplified SVG outline of Philadelphia with 10 episode location dots.
 * Mini version for inter-episode transitions; large version for the finale.
 *
 * The SVG viewBox is 420x440.
 * The outline is a simplified polygon tracing Philadelphia's borders:
 * - North: roughly flat along Cheltenham Ave
 * - East: Delaware River (irregular)
 * - South: confluence area
 * - West: City Ave / Cobbs Creek curving line
 */

// Simplified Philadelphia outline path
const PHILLY_OUTLINE = `
  M 60,10
  L 180,5
  L 280,8
  L 340,15
  L 370,30
  L 390,60
  L 400,110
  L 405,160
  L 400,210
  L 395,260
  L 385,300
  L 375,330
  L 365,355
  L 355,375
  L 340,395
  L 315,410
  L 280,425
  L 240,432
  L 200,430
  L 160,420
  L 120,400
  L 90,375
  L 70,345
  L 55,310
  L 45,270
  L 40,230
  L 38,190
  L 40,150
  L 45,110
  L 50,70
  L 55,40
  Z
`;

export default function PhillyMap({
  activatedEpisodes,
  size = 'mini',
  className = '',
}: PhillyMapProps) {
  const isMini = size === 'mini';
  const containerSize = isMini
    ? { width: 200, height: 210 }
    : { width: 420, height: 440 };

  const activatedSet = useMemo(
    () => new Set(activatedEpisodes),
    [activatedEpisodes],
  );

  // Generate connecting lines between activated dots in order
  const activatedInOrder = useMemo(() => {
    return EPISODES.filter((e) => activatedSet.has(e.number)).sort(
      (a, b) => a.number - b.number,
    );
  }, [activatedSet]);

  return (
    <div className={className} style={{ display: 'inline-block' }}>
      <svg
        viewBox="0 0 420 440"
        width={containerSize.width}
        height={containerSize.height}
        xmlns="http://www.w3.org/2000/svg"
        style={{ overflow: 'visible' }}
      >
        {/* Glow filter definitions */}
        <defs>
          {EPISODES.map((episode) => (
            <filter
              key={`glow-${episode.number}`}
              id={`glow-${episode.number}`}
              x="-100%"
              y="-100%"
              width="300%"
              height="300%"
            >
              <feGaussianBlur
                stdDeviation={isMini ? 3 : 6}
                result="blur"
              />
              <feFlood
                floodColor={episode.genre_color}
                floodOpacity="0.8"
                result="color"
              />
              <feComposite in="color" in2="blur" operator="in" result="glow" />
              <feMerge>
                <feMergeNode in="glow" />
                <feMergeNode in="glow" />
                <feMergeNode in="SourceGraphic" />
              </feMerge>
            </filter>
          ))}
          {/* Subtle outline glow */}
          <filter id="outline-glow" x="-5%" y="-5%" width="110%" height="110%">
            <feGaussianBlur stdDeviation="2" result="blur" />
            <feFlood floodColor="#ffffff" floodOpacity="0.15" result="color" />
            <feComposite in="color" in2="blur" operator="in" result="glow" />
            <feMerge>
              <feMergeNode in="glow" />
              <feMergeNode in="SourceGraphic" />
            </feMerge>
          </filter>
        </defs>

        {/* City outline */}
        <path
          d={PHILLY_OUTLINE}
          fill="none"
          stroke="rgba(255,255,255,0.15)"
          strokeWidth={isMini ? 1 : 1.5}
          filter="url(#outline-glow)"
        />

        {/* Connecting lines between activated episodes */}
        {activatedInOrder.map((episode, i) => {
          if (i === 0) return null;
          const prev = activatedInOrder[i - 1];
          return (
            <line
              key={`line-${prev.number}-${episode.number}`}
              x1={prev.mapPosition.x}
              y1={prev.mapPosition.y}
              x2={episode.mapPosition.x}
              y2={episode.mapPosition.y}
              stroke="rgba(255,255,255,0.08)"
              strokeWidth={isMini ? 0.5 : 1}
              strokeDasharray={isMini ? '2,4' : '4,8'}
            />
          );
        })}

        {/* Episode dots */}
        {EPISODES.map((episode) => {
          const isActive = activatedSet.has(episode.number);
          const dotRadius = isMini ? 3 : 6;

          return (
            <g key={episode.number}>
              {/* Inactive dot (dim) */}
              {!isActive && (
                <circle
                  cx={episode.mapPosition.x}
                  cy={episode.mapPosition.y}
                  r={dotRadius * 0.5}
                  fill="rgba(255,255,255,0.12)"
                />
              )}

              {/* Active dot with glow and pulse */}
              {isActive && (
                <>
                  {/* Pulse ring */}
                  <circle
                    cx={episode.mapPosition.x}
                    cy={episode.mapPosition.y}
                    r={dotRadius}
                    fill="none"
                    stroke={episode.genre_color}
                    strokeWidth={isMini ? 0.5 : 1}
                    opacity={0.5}
                  >
                    <animate
                      attributeName="r"
                      values={`${dotRadius};${dotRadius * 3};${dotRadius}`}
                      dur="3s"
                      repeatCount="indefinite"
                    />
                    <animate
                      attributeName="opacity"
                      values="0.5;0;0.5"
                      dur="3s"
                      repeatCount="indefinite"
                    />
                  </circle>

                  {/* Core dot */}
                  <circle
                    cx={episode.mapPosition.x}
                    cy={episode.mapPosition.y}
                    r={dotRadius}
                    fill={episode.genre_color}
                    filter={`url(#glow-${episode.number})`}
                    style={{
                      animation: 'dot-appear 0.6s ease-out forwards',
                    }}
                  />

                  {/* Label (large map only) */}
                  {!isMini && (
                    <text
                      x={episode.mapPosition.x}
                      y={episode.mapPosition.y - dotRadius - 8}
                      textAnchor="middle"
                      fill={episode.genre_color}
                      fontSize="10"
                      fontFamily="Inter, sans-serif"
                      fontWeight="500"
                      opacity={0.8}
                    >
                      {episode.number}. {episode.title}
                    </text>
                  )}
                </>
              )}
            </g>
          );
        })}
      </svg>
    </div>
  );
}
