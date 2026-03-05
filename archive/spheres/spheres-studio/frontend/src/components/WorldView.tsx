/**
 * WorldView.tsx — The main 3D world component for SPHERES Studio.
 *
 * This is the killer feature: a full-screen, immersive 3D preview of a
 * community space design. Users can walk through their design, toggle
 * between Before/After/Permanence views, adjust time of day, capture
 * screenshots, and toggle ambient audio.
 *
 * Usage:
 *   <WorldView
 *     elements={designElements}
 *     elementDefs={catalogMap}
 *     parcelPolygon={polygon}
 *     parcelWidth={120}
 *     parcelDepth={80}
 *   />
 */

import {
  useState,
  useRef,
  useCallback,
  useMemo,
  useEffect,
  type FC,
} from 'react';
import { Canvas } from '@react-three/fiber';
import * as THREE from 'three';
import Environment, { type ViewMode } from './world/Environment';
import { ElementMesh } from './world/ElementMeshes';
import Controls, { type CameraMode, type ControlsHandle } from './world/Controls';
import {
  designTo3DScene,
  computeBounds,
  calculateCameraStartPosition,
  calculateFirstPersonStart,
  type DesignElement,
  type ElementDef,
  type Polygon2D,
  type Point2D,
  type TimeOfDay,
  type Element3DProps,
} from '../utils/designTo3D';

// ---------------------------------------------------------------------------
// Icons (inline SVG to avoid dependency on lucide for simple shapes)
// ---------------------------------------------------------------------------

const IconCamera = () => (
  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z" />
    <circle cx="12" cy="13" r="4" />
  </svg>
);

const IconSun = () => (
  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <circle cx="12" cy="12" r="5" />
    <line x1="12" y1="1" x2="12" y2="3" /><line x1="12" y1="21" x2="12" y2="23" />
    <line x1="4.22" y1="4.22" x2="5.64" y2="5.64" /><line x1="18.36" y1="18.36" x2="19.78" y2="19.78" />
    <line x1="1" y1="12" x2="3" y2="12" /><line x1="21" y1="12" x2="23" y2="12" />
    <line x1="4.22" y1="19.78" x2="5.64" y2="18.36" /><line x1="18.36" y1="5.64" x2="19.78" y2="4.22" />
  </svg>
);

const IconVolume = () => (
  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5" />
    <path d="M19.07 4.93a10 10 0 0 1 0 14.14M15.54 8.46a5 5 0 0 1 0 7.07" />
  </svg>
);

const IconVolumeOff = () => (
  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5" />
    <line x1="23" y1="9" x2="17" y2="15" /><line x1="17" y1="9" x2="23" y2="15" />
  </svg>
);

const IconEye = () => (
  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" />
    <circle cx="12" cy="12" r="3" />
  </svg>
);

const IconWalk = () => (
  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <circle cx="13" cy="4" r="2" />
    <path d="M7 21l3-7 2.5 2V21" /><path d="M16 21l-2-4-3.5-1L14 9l-4-1-3 4" />
  </svg>
);

const IconRotate = () => (
  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <polyline points="1 4 1 10 7 10" /><path d="M3.51 15a9 9 0 1 0 2.13-9.36L1 10" />
  </svg>
);

// ---------------------------------------------------------------------------
// Audio manager — simple Web Audio API ambient soundscapes
// ---------------------------------------------------------------------------

class AmbientAudioManager {
  private ctx: AudioContext | null = null;
  private gainNode: GainNode | null = null;
  private oscillators: OscillatorNode[] = [];
  private active = false;

  start(mode: ViewMode) {
    if (this.active) this.stop();
    this.ctx = new AudioContext();
    this.gainNode = this.ctx.createGain();
    this.gainNode.gain.value = 0.04;
    this.gainNode.connect(this.ctx.destination);

    if (mode === 'before') {
      // Wind-like noise via detuned oscillators
      this.addOscillator(80, 'sawtooth', 0.015);
      this.addOscillator(120, 'sawtooth', 0.01);
    } else {
      // Birds + gentle crowd murmur via layered sine tones
      this.addOscillator(2400, 'sine', 0.008);
      this.addOscillator(3200, 'sine', 0.005);
      this.addOscillator(1800, 'sine', 0.006);
      // Crowd murmur — low rumble
      this.addOscillator(200, 'sawtooth', 0.008);
      this.addOscillator(280, 'sawtooth', 0.005);
    }
    this.active = true;
  }

  stop() {
    this.oscillators.forEach((osc) => {
      try { osc.stop(); } catch { /* already stopped */ }
    });
    this.oscillators = [];
    if (this.ctx) {
      this.ctx.close();
      this.ctx = null;
    }
    this.gainNode = null;
    this.active = false;
  }

  private addOscillator(freq: number, type: OscillatorType, gain: number) {
    if (!this.ctx || !this.gainNode) return;
    const osc = this.ctx.createOscillator();
    const g = this.ctx.createGain();
    osc.type = type;
    osc.frequency.value = freq;
    // Add slight random modulation for natural feel
    osc.frequency.setValueAtTime(freq, this.ctx.currentTime);
    osc.frequency.linearRampToValueAtTime(freq * 1.02, this.ctx.currentTime + 2);
    g.gain.value = gain;
    osc.connect(g);
    g.connect(this.gainNode);
    osc.start();
    this.oscillators.push(osc);
  }

  get isActive() {
    return this.active;
  }
}

// ---------------------------------------------------------------------------
// Element info panel (shown on click)
// ---------------------------------------------------------------------------

interface ElementInfoPanelProps {
  element: Element3DProps | null;
  onClose: () => void;
}

const ElementInfoPanel: FC<ElementInfoPanelProps> = ({ element, onClose }) => {
  if (!element) return null;

  return (
    <div
      style={{
        position: 'absolute',
        top: '16px',
        right: '16px',
        width: '280px',
        background: 'rgba(15, 15, 25, 0.9)',
        backdropFilter: 'blur(12px)',
        borderRadius: '12px',
        border: '1px solid rgba(255,255,255,0.12)',
        color: '#fff',
        fontFamily: 'system-ui, sans-serif',
        padding: '20px',
        zIndex: 50,
      }}
    >
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '12px' }}>
        <h3 style={{ margin: 0, fontSize: '16px', fontWeight: 600 }}>{element.name}</h3>
        <button
          onClick={onClose}
          style={{
            background: 'rgba(255,255,255,0.1)',
            border: 'none',
            color: '#fff',
            width: '28px',
            height: '28px',
            borderRadius: '6px',
            cursor: 'pointer',
            fontSize: '16px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
          }}
        >
          x
        </button>
      </div>
      <div style={{ fontSize: '13px', opacity: 0.7, lineHeight: 1.6 }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '6px' }}>
          <span
            style={{
              width: '14px',
              height: '14px',
              borderRadius: '3px',
              background: element.color,
              display: 'inline-block',
              flexShrink: 0,
            }}
          />
          <span>{element.category}</span>
        </div>
        <div>Type: {element.meshType.replace(/_/g, ' ')}</div>
        <div>
          Position: ({element.position[0].toFixed(1)}, {element.position[2].toFixed(1)}) ft
        </div>
        <div>
          {element.isPermanent ? (
            <span style={{ color: '#66cc88' }}>Permanent element</span>
          ) : (
            <span style={{ color: '#ffaa44' }}>Temporary element</span>
          )}
        </div>
      </div>
    </div>
  );
};

// ---------------------------------------------------------------------------
// Screenshot utility
// ---------------------------------------------------------------------------

function captureScreenshot(canvas: HTMLCanvasElement): string {
  return canvas.toDataURL('image/png');
}

function downloadScreenshot(dataUrl: string, filename: string) {
  const link = document.createElement('a');
  link.download = filename;
  link.href = dataUrl;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}

// ---------------------------------------------------------------------------
// View mode labels
// ---------------------------------------------------------------------------

const MODE_LABELS: Record<ViewMode, { label: string; description: string; color: string }> = {
  before: {
    label: 'Before',
    description: 'Empty lot as it exists today',
    color: '#888888',
  },
  after: {
    label: 'After',
    description: 'Activated space with all elements',
    color: '#44cc88',
  },
  permanence: {
    label: 'Permanence',
    description: 'After activation ends - permanent elements only',
    color: '#cc8844',
  },
};

// ---------------------------------------------------------------------------
// Time-of-day labels
// ---------------------------------------------------------------------------

function timeLabel(t: TimeOfDay): string {
  const hour = Math.floor(t * 24);
  const minute = Math.floor((t * 24 - hour) * 60);
  const ampm = hour >= 12 ? 'PM' : 'AM';
  const h12 = hour % 12 || 12;
  return `${h12}:${minute.toString().padStart(2, '0')} ${ampm}`;
}

// ---------------------------------------------------------------------------
// Main WorldView props
// ---------------------------------------------------------------------------

export interface WorldViewProps {
  elements?: DesignElement[];
  elementDefs?: Map<string, ElementDef>;
  parcelPolygon?: Polygon2D;
  parcelWidth?: number;
  parcelDepth?: number;
  /** Start in a specific mode */
  initialMode?: ViewMode;
  /** Callback when the scene is ready */
  onReady?: () => void;
  /** Callback with screenshot data URL */
  onScreenshot?: (dataUrl: string) => void;
}

// ---------------------------------------------------------------------------
// PUBLIC: WorldView component
// ---------------------------------------------------------------------------

const WorldView: FC<WorldViewProps> = ({
  elements = [],
  elementDefs = new Map(),
  parcelPolygon,
  parcelWidth = 100,
  parcelDepth = 80,
  initialMode = 'after',
  onReady,
  onScreenshot,
}) => {
  // State
  const [viewMode, setViewMode] = useState<ViewMode>(initialMode);
  const [timeOfDay, setTimeOfDay] = useState<TimeOfDay>(0.45); // Late morning
  const [cameraMode, setCameraMode] = useState<CameraMode>('orbit');
  const [audioEnabled, setAudioEnabled] = useState(false);
  const [selectedElement, setSelectedElement] = useState<Element3DProps | null>(null);
  const [showHelp, setShowHelp] = useState(true);
  const [fadeOpacity, setFadeOpacity] = useState<Record<string, number>>({});

  // Refs
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const controlsRef = useRef<ControlsHandle>(null);
  const audioManagerRef = useRef(new AmbientAudioManager());

  // Computed
  const parcelCenter: Point2D = useMemo(() => {
    if (parcelPolygon) {
      const bounds = computeBounds(parcelPolygon.points);
      return { x: bounds.centerX, y: bounds.centerY };
    }
    return { x: parcelWidth / 2, y: parcelDepth / 2 };
  }, [parcelPolygon, parcelWidth, parcelDepth]);

  const parcelBounds = useMemo(() => {
    if (parcelPolygon) return computeBounds(parcelPolygon.points);
    return {
      minX: 0,
      maxX: parcelWidth,
      minY: 0,
      maxY: parcelDepth,
      width: parcelWidth,
      height: parcelDepth,
      centerX: parcelWidth / 2,
      centerY: parcelDepth / 2,
    };
  }, [parcelPolygon, parcelWidth, parcelDepth]);

  const cameraStart = useMemo(
    () =>
      cameraMode === 'orbit'
        ? calculateCameraStartPosition(parcelBounds)
        : calculateFirstPersonStart(parcelBounds),
    [parcelBounds, cameraMode],
  );

  // Convert design elements to 3D props
  const elements3D = useMemo(
    () => designTo3DScene(elements, elementDefs, parcelCenter, viewMode),
    [elements, elementDefs, parcelCenter, viewMode],
  );

  // Permanence fade: when switching to permanence mode, fade out non-permanent elements
  useEffect(() => {
    if (viewMode === 'permanence') {
      // All permanent elements stay at full opacity
      const opacities: Record<string, number> = {};
      elements3D.forEach((el) => {
        opacities[el.id] = el.isPermanent ? 1 : 0.15;
      });
      setFadeOpacity(opacities);
    } else {
      setFadeOpacity({});
    }
  }, [viewMode, elements3D]);

  // Audio
  useEffect(() => {
    if (audioEnabled) {
      audioManagerRef.current.start(viewMode);
    } else {
      audioManagerRef.current.stop();
    }
    return () => audioManagerRef.current.stop();
  }, [audioEnabled, viewMode]);

  // Screenshot handler
  const handleScreenshot = useCallback(() => {
    if (!canvasRef.current) return;
    // Wait one frame for the canvas to be up to date
    requestAnimationFrame(() => {
      if (!canvasRef.current) return;
      const dataUrl = captureScreenshot(canvasRef.current);
      const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
      downloadScreenshot(dataUrl, `spheres-${viewMode}-${timestamp}.png`);
      onScreenshot?.(dataUrl);
    });
  }, [viewMode, onScreenshot]);

  // Dismiss help after a few seconds
  useEffect(() => {
    const timer = setTimeout(() => setShowHelp(false), 6000);
    return () => clearTimeout(timer);
  }, []);

  // Fire onReady
  useEffect(() => {
    onReady?.();
  }, [onReady]);

  // Cycle view mode
  const cycleViewMode = useCallback(() => {
    setViewMode((prev) => {
      if (prev === 'before') return 'after';
      if (prev === 'after') return 'permanence';
      return 'before';
    });
  }, []);

  const currentModeInfo = MODE_LABELS[viewMode];

  return (
    <div
      style={{
        position: 'relative',
        width: '100%',
        height: '100%',
        background: '#000',
        overflow: 'hidden',
      }}
    >
      {/* ---- 3D Canvas ---- */}
      <Canvas
        ref={canvasRef}
        shadows
        gl={{
          antialias: true,
          toneMapping: THREE.ACESFilmicToneMapping,
          toneMappingExposure: viewMode === 'before' ? 0.6 : 1.0,
          preserveDrawingBuffer: true, // Required for screenshots
        }}
        camera={{
          fov: 60,
          near: 0.5,
          far: 1000,
          position: cameraStart.position,
        }}
        style={{ width: '100%', height: '100%' }}
      >
        {/* Environment (sky, ground, lighting, fog) */}
        <Environment
          mode={viewMode}
          timeOfDay={timeOfDay}
          parcelPolygon={parcelPolygon}
          parcelCenter={parcelCenter}
          parcelWidth={parcelWidth}
          parcelDepth={parcelDepth}
          showPeople={viewMode === 'after'}
        />

        {/* Design elements */}
        {elements3D.map((el) => (
          <ElementMesh
            key={el.id}
            element={el}
            onClick={(id) => {
              const clicked = elements3D.find((e) => e.id === id);
              setSelectedElement(clicked ?? null);
            }}
            opacity={fadeOpacity[el.id] ?? 1}
          />
        ))}

        {/* Camera controls */}
        <Controls
          ref={controlsRef}
          mode={cameraMode}
          onModeChange={setCameraMode}
          initialPosition={cameraStart.position}
          initialTarget={cameraStart.target}
          parcelWidth={parcelWidth}
          parcelDepth={parcelDepth}
        />
      </Canvas>

      {/* ---- HUD Overlay ---- */}

      {/* Top-left: View mode toggle */}
      <div
        style={{
          position: 'absolute',
          top: '16px',
          left: '16px',
          display: 'flex',
          flexDirection: 'column',
          gap: '8px',
          zIndex: 40,
        }}
      >
        {/* Mode badge */}
        <button
          onClick={cycleViewMode}
          style={{
            background: 'rgba(15, 15, 25, 0.85)',
            backdropFilter: 'blur(12px)',
            border: `1px solid ${currentModeInfo.color}55`,
            borderRadius: '10px',
            color: '#fff',
            padding: '10px 18px',
            cursor: 'pointer',
            fontFamily: 'system-ui, sans-serif',
            fontSize: '14px',
            display: 'flex',
            alignItems: 'center',
            gap: '10px',
            transition: 'all 0.2s',
          }}
        >
          <span
            style={{
              width: '10px',
              height: '10px',
              borderRadius: '50%',
              background: currentModeInfo.color,
              boxShadow: `0 0 8px ${currentModeInfo.color}`,
            }}
          />
          <span style={{ fontWeight: 600 }}>{currentModeInfo.label}</span>
          <span style={{ opacity: 0.5, fontSize: '12px' }}>{currentModeInfo.description}</span>
        </button>

        {/* Individual mode buttons */}
        <div style={{ display: 'flex', gap: '4px' }}>
          {(['before', 'after', 'permanence'] as ViewMode[]).map((m) => (
            <button
              key={m}
              onClick={() => setViewMode(m)}
              style={{
                background: viewMode === m ? MODE_LABELS[m].color + '33' : 'rgba(15,15,25,0.7)',
                border: viewMode === m
                  ? `1px solid ${MODE_LABELS[m].color}`
                  : '1px solid rgba(255,255,255,0.1)',
                borderRadius: '8px',
                color: viewMode === m ? MODE_LABELS[m].color : '#aaa',
                padding: '6px 14px',
                cursor: 'pointer',
                fontFamily: 'system-ui, sans-serif',
                fontSize: '12px',
                fontWeight: viewMode === m ? 600 : 400,
                transition: 'all 0.2s',
              }}
            >
              {MODE_LABELS[m].label}
            </button>
          ))}
        </div>
      </div>

      {/* Bottom: Time of day slider + controls bar */}
      <div
        style={{
          position: 'absolute',
          bottom: '16px',
          left: '16px',
          right: '170px', // Leave space for minimap
          display: 'flex',
          alignItems: 'center',
          gap: '12px',
          zIndex: 40,
        }}
      >
        {/* Camera mode toggle */}
        <button
          onClick={() => setCameraMode(cameraMode === 'orbit' ? 'firstperson' : 'orbit')}
          title={cameraMode === 'orbit' ? 'Switch to first person (V)' : 'Switch to orbit view (V)'}
          style={{
            background: 'rgba(15, 15, 25, 0.85)',
            backdropFilter: 'blur(12px)',
            border: '1px solid rgba(255,255,255,0.12)',
            borderRadius: '8px',
            color: '#fff',
            padding: '8px 12px',
            cursor: 'pointer',
            display: 'flex',
            alignItems: 'center',
            gap: '6px',
            fontSize: '12px',
            fontFamily: 'system-ui, sans-serif',
          }}
        >
          {cameraMode === 'orbit' ? <IconEye /> : <IconWalk />}
          {cameraMode === 'orbit' ? 'Orbit' : 'Walk'}
        </button>

        {/* Reset camera */}
        <button
          onClick={() => controlsRef.current?.resetCamera()}
          title="Reset camera"
          style={{
            background: 'rgba(15, 15, 25, 0.85)',
            backdropFilter: 'blur(12px)',
            border: '1px solid rgba(255,255,255,0.12)',
            borderRadius: '8px',
            color: '#fff',
            padding: '8px',
            cursor: 'pointer',
            display: 'flex',
            alignItems: 'center',
          }}
        >
          <IconRotate />
        </button>

        {/* Time of day */}
        <div
          style={{
            flex: 1,
            background: 'rgba(15, 15, 25, 0.85)',
            backdropFilter: 'blur(12px)',
            border: '1px solid rgba(255,255,255,0.12)',
            borderRadius: '8px',
            padding: '8px 16px',
            display: 'flex',
            alignItems: 'center',
            gap: '10px',
          }}
        >
          <IconSun />
          <input
            type="range"
            min="0"
            max="1"
            step="0.01"
            value={timeOfDay}
            onChange={(e) => setTimeOfDay(parseFloat(e.target.value))}
            style={{
              flex: 1,
              accentColor: '#ffaa44',
              height: '4px',
              cursor: 'pointer',
            }}
          />
          <span
            style={{
              color: '#fff',
              fontSize: '12px',
              fontFamily: 'system-ui, monospace',
              minWidth: '65px',
              textAlign: 'right',
              opacity: 0.7,
            }}
          >
            {timeLabel(timeOfDay)}
          </span>
        </div>

        {/* Audio toggle */}
        <button
          onClick={() => setAudioEnabled(!audioEnabled)}
          title={audioEnabled ? 'Mute ambient audio' : 'Enable ambient audio'}
          style={{
            background: audioEnabled ? 'rgba(68, 204, 136, 0.2)' : 'rgba(15, 15, 25, 0.85)',
            backdropFilter: 'blur(12px)',
            border: audioEnabled
              ? '1px solid rgba(68, 204, 136, 0.4)'
              : '1px solid rgba(255,255,255,0.12)',
            borderRadius: '8px',
            color: '#fff',
            padding: '8px',
            cursor: 'pointer',
            display: 'flex',
            alignItems: 'center',
          }}
        >
          {audioEnabled ? <IconVolume /> : <IconVolumeOff />}
        </button>

        {/* Screenshot */}
        <button
          onClick={handleScreenshot}
          title="Capture screenshot"
          style={{
            background: 'rgba(15, 15, 25, 0.85)',
            backdropFilter: 'blur(12px)',
            border: '1px solid rgba(255,255,255,0.12)',
            borderRadius: '8px',
            color: '#fff',
            padding: '8px 14px',
            cursor: 'pointer',
            display: 'flex',
            alignItems: 'center',
            gap: '6px',
            fontSize: '12px',
            fontFamily: 'system-ui, sans-serif',
          }}
        >
          <IconCamera />
          Capture
        </button>
      </div>

      {/* Element info panel */}
      <ElementInfoPanel
        element={selectedElement}
        onClose={() => setSelectedElement(null)}
      />

      {/* Keyboard help overlay */}
      {showHelp && (
        <div
          style={{
            position: 'absolute',
            top: '50%',
            left: '50%',
            transform: 'translate(-50%, -50%)',
            background: 'rgba(0, 0, 0, 0.75)',
            backdropFilter: 'blur(16px)',
            borderRadius: '16px',
            border: '1px solid rgba(255,255,255,0.1)',
            color: '#fff',
            fontFamily: 'system-ui, sans-serif',
            padding: '32px 40px',
            textAlign: 'center',
            zIndex: 50,
            pointerEvents: 'none',
            animation: 'fadeOut 1s ease-in-out 4s forwards',
          }}
        >
          <h2 style={{ margin: '0 0 16px', fontSize: '22px', fontWeight: 700 }}>
            SPHERES World Preview
          </h2>
          <p style={{ margin: '0 0 8px', opacity: 0.7, fontSize: '14px' }}>
            Explore your community space design in 3D
          </p>
          <div
            style={{
              display: 'grid',
              gridTemplateColumns: 'auto auto',
              gap: '8px 20px',
              fontSize: '13px',
              opacity: 0.6,
              marginTop: '16px',
            }}
          >
            <span>Orbit / Walk</span><kbd style={kbdStyle}>V</kbd>
            <span>Move</span><kbd style={kbdStyle}>WASD</kbd>
            <span>Look</span><kbd style={kbdStyle}>Mouse</kbd>
            <span>Jump</span><kbd style={kbdStyle}>Space</kbd>
            <span>Sprint</span><kbd style={kbdStyle}>Shift</kbd>
          </div>
        </div>
      )}

      {/* CSS animation for fade */}
      <style>{`
        @keyframes fadeOut {
          from { opacity: 1; }
          to { opacity: 0; }
        }
      `}</style>
    </div>
  );
};

const kbdStyle: React.CSSProperties = {
  background: 'rgba(255,255,255,0.1)',
  borderRadius: '4px',
  padding: '2px 8px',
  fontFamily: 'monospace',
  fontSize: '12px',
};

export default WorldView;
