import { useState, useEffect, useRef, useCallback } from 'react';

interface DomainScore {
  id: string; name: string; color: string; icon: string;
  current: number; potential: number; aspiration: number;
  gap: number; resources_available: number;
}

interface Props {
  domains: DomainScore[];
  score: number;
  potentialScore: number;
  name: string;
}

const GOLD = '#B8860B';
const GOLD_LIGHT = '#DAA520';
const MIDNIGHT = '#191970';

function polar(cx: number, by: number, r: number, deg: number) {
  const rad = (deg * Math.PI) / 180;
  return { x: cx + r * Math.cos(Math.PI - rad), y: by - r * Math.sin(Math.PI - rad) };
}

function arc(cx: number, by: number, r: number, s: number, e: number, sweep: number) {
  const end = polar(cx, by, r, e);
  const large = Math.abs(e - s) > 180 ? 1 : 0;
  return `A ${r} ${r} 0 ${large} ${sweep} ${end.x} ${end.y}`;
}

/**
 * Staged animation: each domain animates with a per-layer delay.
 * Foundation (0-3): starts immediately
 * Aspiration (4-7): starts after 800ms
 * Transcendence (8-11): starts after 1600ms
 */
function useStagedAnim(targets: number[], dur = 1500) {
  const [vals, setVals] = useState(targets.map(() => 0));
  const ref = useRef<number>(0);
  const key = targets.join(',');

  useEffect(() => {
    const startTime = performance.now();
    const go = (t: number) => {
      const elapsed = t - startTime;
      setVals(targets.map((v, i) => {
        // Determine layer delay based on index
        const layerIndex = Math.floor(i / 4);
        const delay = layerIndex * 800;
        const localElapsed = Math.max(0, elapsed - delay);
        const p = Math.min(localElapsed / dur, 1);
        // Cubic ease-out
        const e = 1 - Math.pow(1 - p, 3);
        return v * e;
      }));
      // Keep animating until all layers complete
      const totalDur = 1600 + dur;
      if (elapsed < totalDur) ref.current = requestAnimationFrame(go);
    };
    ref.current = requestAnimationFrame(go);
    return () => cancelAnimationFrame(ref.current);
  }, [key, dur]);
  return vals;
}

/** Score counter that starts after a delay */
function useDelayedAnim(target: number, delay = 1200, dur = 1800) {
  const [val, setVal] = useState(0);
  const ref = useRef<number>(0);

  useEffect(() => {
    const startTime = performance.now();
    const go = (t: number) => {
      const elapsed = t - startTime;
      const localElapsed = Math.max(0, elapsed - delay);
      const p = Math.min(localElapsed / dur, 1);
      const e = 1 - Math.pow(1 - p, 3);
      setVal(target * e);
      if (elapsed < delay + dur) ref.current = requestAnimationFrame(go);
    };
    ref.current = requestAnimationFrame(go);
    return () => cancelAnimationFrame(ref.current);
  }, [target, delay, dur]);
  return val;
}

/** Layer label that fades in with its layer */
function useLayerLabels() {
  const [opacities, setOpacities] = useState([0, 0, 0]);
  const ref = useRef<number>(0);

  useEffect(() => {
    const startTime = performance.now();
    const go = (t: number) => {
      const elapsed = t - startTime;
      setOpacities([0, 1, 2].map(layer => {
        const delay = layer * 800;
        const p = Math.min(Math.max(0, elapsed - delay) / 600, 1);
        return p;
      }));
      if (elapsed < 3000) ref.current = requestAnimationFrame(go);
    };
    ref.current = requestAnimationFrame(go);
    return () => cancelAnimationFrame(ref.current);
  }, []);
  return opacities;
}

const LAYER_NAMES = ['FOUNDATION', 'ASPIRATION', 'TRANSCENDENCE'];
const LAYER_COLORS = ['rgba(25,25,112,0.3)', 'rgba(184,134,11,0.5)', 'rgba(218,165,32,0.7)'];

export default function FlourishingDome({ domains, score, potentialScore, name }: Props) {
  const containerRef = useRef<HTMLDivElement>(null);
  const [size, setSize] = useState({ w: 0, h: 0 });
  const [hovered, setHovered] = useState<DomainScore | null>(null);

  const measure = useCallback(() => {
    if (!containerRef.current) return;
    const r = containerRef.current.getBoundingClientRect();
    setSize({ w: r.width, h: Math.max(r.width * 0.65, 400) });
  }, []);

  useEffect(() => {
    measure();
    const obs = new ResizeObserver(measure);
    if (containerRef.current) obs.observe(containerRef.current);
    return () => obs.disconnect();
  }, [measure]);

  // Staged animations — foundation first, then aspiration, then transcendence
  const animCurrent = useStagedAnim(domains.map(d => d.current), 1500);
  const animPotential = useStagedAnim(domains.map(d => d.potential), 1800);
  const animScore = useDelayedAnim(score, 1200, 1800);
  const layerOpacities = useLayerLabels();

  if (!size.w) return <div ref={containerRef} style={{ width: '100%', minHeight: 400 }} />;

  const W = size.w, H = size.h;
  const cx = W / 2, by = H * 0.82;
  const outerR = Math.min(W * 0.44, H * 0.65);
  const innerR = outerR * 0.28;
  const n = domains.length || 12;
  const step = 180 / n;

  return (
    <div ref={containerRef} style={{ width: '100%', minHeight: 400, position: 'relative' }}>
      <svg width={W} height={H} viewBox={`0 0 ${W} ${H}`}>
        <defs>
          <linearGradient id="gGrad" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor={GOLD_LIGHT} />
            <stop offset="100%" stopColor={GOLD} />
          </linearGradient>
          <radialGradient id="cGlow" cx="50%" cy="50%" r="50%">
            <stop offset="0%" stopColor={GOLD_LIGHT} stopOpacity="0.2" />
            <stop offset="100%" stopColor={GOLD_LIGHT} stopOpacity="0" />
          </radialGradient>
        </defs>

        <rect width={W} height={H} fill="#FEFDFB" />

        {/* Base line */}
        <line x1={cx - outerR - 30} y1={by} x2={cx + outerR + 30} y2={by}
          stroke={GOLD} strokeWidth="2.5" />

        {/* Layer arc labels — fade in with each layer */}
        {LAYER_NAMES.map((label, li) => {
          const layerStart = li * 4;
          const layerEnd = (li + 1) * 4;
          const midAngle = ((layerStart + layerEnd) / 2) * step;
          const labelR = outerR + 18;
          const lp = polar(cx, by, labelR, midAngle);
          return (
            <text key={label} x={lp.x} y={lp.y} textAnchor="middle"
              fontFamily="'JetBrains Mono',monospace" fontSize="7"
              fill={LAYER_COLORS[li]} letterSpacing="3"
              opacity={layerOpacities[li]}
              style={{ transition: 'opacity 0.3s' }}>
              {label}
            </text>
          );
        })}

        {/* Panels — staged by layer */}
        {domains.map((d, i) => {
          const s = i * step, e = (i + 1) * step;
          const curPct = (animCurrent[i] ?? 0) / 100;
          const potPct = (animPotential[i] ?? 0) / 100;
          const fillR = innerR + (outerR - innerR) * curPct;
          const potR = innerR + (outerR - innerR) * potPct;

          const is_ = polar(cx, by, innerR, s);
          const ie_ = polar(cx, by, innerR, e);

          // Potential ghost
          const ps = polar(cx, by, potR, s);
          const potPath = `M ${is_.x} ${is_.y} L ${ps.x} ${ps.y} ${arc(cx, by, potR, s, e, 0)} L ${ie_.x} ${ie_.y} ${arc(cx, by, innerR, e, s, 1)} Z`;

          // Current fill
          const fs = polar(cx, by, fillR, s);
          const fillPath = `M ${is_.x} ${is_.y} L ${fs.x} ${fs.y} ${arc(cx, by, fillR, s, e, 0)} L ${ie_.x} ${ie_.y} ${arc(cx, by, innerR, e, s, 1)} Z`;

          // Outline
          const os = polar(cx, by, outerR, s);
          const outPath = `M ${is_.x} ${is_.y} L ${os.x} ${os.y} ${arc(cx, by, outerR, s, e, 0)} L ${ie_.x} ${ie_.y} ${arc(cx, by, innerR, e, s, 1)} Z`;

          // Label position
          const mid = (s + e) / 2;
          const lr = innerR + (outerR - innerR) * 0.55;
          const lp = polar(cx, by, lr, mid);
          let rot = -(mid - 90);
          if (mid < 90) rot += 180;

          const isHov = hovered?.id === d.id;
          const opacity = 0.15 + curPct * 0.55;
          // Outline fades in with its layer
          const layerIdx = Math.floor(i / 4);
          const outlineOpacity = layerOpacities[layerIdx] * (isHov ? 1 : 0.6);

          return (
            <g key={d.id}
              onMouseEnter={() => setHovered(d)}
              onMouseLeave={() => setHovered(null)}
              style={{ cursor: 'pointer' }}
            >
              <path d={potPath} fill={d.color} opacity={0.08 * layerOpacities[layerIdx]} />
              <path d={fillPath} fill={d.color} opacity={opacity} />
              <path d={outPath} fill="none" stroke={isHov ? GOLD_LIGHT : GOLD}
                strokeWidth={isHov ? 2.5 : 1} opacity={outlineOpacity} />
              <text x={lp.x} y={lp.y} textAnchor="middle" dominantBaseline="middle"
                transform={`rotate(${rot},${lp.x},${lp.y})`}
                fontFamily="'Crimson Text',serif" fontSize={Math.max(9, Math.min(12, W / 85))}
                fontWeight="600" fill={MIDNIGHT} opacity={0.8 * layerOpacities[layerIdx]}
                style={{ pointerEvents: 'none' }}
              >
                {d.name.length > 16 ? d.name.slice(0, 15) + '…' : d.name}
              </text>
            </g>
          );
        })}

        {/* Radial ribs — fade in with their layer */}
        {Array.from({ length: n + 1 }).map((_, i) => {
          const a = i * step;
          const p1 = polar(cx, by, innerR, a);
          const p2 = polar(cx, by, outerR, a);
          const layerIdx = Math.min(Math.floor(i / 4), 2);
          return <line key={i} x1={p1.x} y1={p1.y} x2={p2.x} y2={p2.y}
            stroke={GOLD} strokeWidth="1" opacity={0.4 * layerOpacities[layerIdx]} />;
        })}

        {/* Center glow */}
        <ellipse cx={cx} cy={by} rx={innerR} ry={innerR} fill="url(#cGlow)" />

        {/* Person silhouette */}
        <circle cx={cx} cy={by - 35} r={7} fill={MIDNIGHT} opacity="0.4" />
        <line x1={cx} y1={by - 28} x2={cx} y2={by - 8} stroke={MIDNIGHT} strokeWidth="2" opacity="0.4" />
        {/* Arms */}
        <line x1={cx - 12} y1={by - 20} x2={cx + 12} y2={by - 20} stroke={MIDNIGHT} strokeWidth="1.5" opacity="0.3" />
        {/* Legs */}
        <line x1={cx} y1={by - 8} x2={cx - 8} y2={by + 5} stroke={MIDNIGHT} strokeWidth="1.5" opacity="0.3" />
        <line x1={cx} y1={by - 8} x2={cx + 8} y2={by + 5} stroke={MIDNIGHT} strokeWidth="1.5" opacity="0.3" />

        {/* Score — fades in after foundation builds */}
        <text x={cx} y={by - 60} textAnchor="middle"
          fontFamily="'Crimson Text',serif" fontSize={Math.max(32, Math.min(48, W / 18))}
          fontWeight="700" fill={MIDNIGHT}
          opacity={Math.min(1, animScore / (score * 0.3 || 1))}>
          {Math.round(animScore)}
        </text>
        <text x={cx} y={by - 48} textAnchor="middle"
          fontFamily="'JetBrains Mono',monospace" fontSize="8"
          fill={GOLD} letterSpacing="3"
          opacity={Math.min(1, animScore / (score * 0.3 || 1))}>
          FLOURISHING SCORE
        </text>

        {/* Title */}
        <text x={cx} y={28} textAnchor="middle"
          fontFamily="'Crimson Text',serif" fontSize={Math.max(16, Math.min(24, W / 40))}
          fontWeight="700" fill={MIDNIGHT}>
          {name ? `${name}'s Flourishing Dome` : 'Flourishing Dome'}
        </text>
        <text x={cx} y={46} textAnchor="middle"
          fontFamily="'JetBrains Mono',monospace" fontSize="9"
          fill={GOLD} letterSpacing="3">
          POTENTIAL: {Math.round(potentialScore)} / 100
        </text>
      </svg>

      {/* Tooltip */}
      {hovered && (
        <div className="absolute top-4 right-4 bg-warm-white border-2 border-gold p-4 min-w-[200px] shadow-lg z-10">
          <h4 className="font-serif text-lg font-bold mb-2" style={{ color: hovered.color }}>
            {hovered.name}
          </h4>
          <div className="space-y-1 text-sm">
            <div className="flex justify-between">
              <span className="font-mono text-[10px] tracking-widest">CURRENT</span>
              <span className="font-bold">{hovered.current}</span>
            </div>
            <div className="flex justify-between">
              <span className="font-mono text-[10px] tracking-widest">POTENTIAL</span>
              <span className="font-bold">{hovered.potential}</span>
            </div>
            <div className="flex justify-between">
              <span className="font-mono text-[10px] tracking-widest text-gold">GAP</span>
              <span className="font-bold text-gold">{hovered.gap}</span>
            </div>
          </div>
          <div className="mt-2 h-1.5 bg-midnight/10">
            <div className="h-full" style={{ width: `${hovered.current}%`, background: hovered.color }} />
          </div>
        </div>
      )}
    </div>
  );
}
