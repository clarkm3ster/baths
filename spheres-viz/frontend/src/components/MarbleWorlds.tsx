/**
 * MarbleWorlds — World Labs Marble 3D World Viewer
 * =================================================
 * Full-screen viewer for browsing all 10 Marble-generated Gaussian splat
 * worlds. When a splat URL is available, renders via SparkJS SplatMesh.
 * Falls back to a geometric Three.js scene per episode otherwise.
 *
 * Dark design: bg #050505, text #FFFFFF, inline styles throughout.
 */

import { useState, useEffect, useCallback, useRef, useMemo } from 'react';
import { Canvas, useThree, useFrame } from '@react-three/fiber';
import { OrbitControls, Stars, Float } from '@react-three/drei';
import * as THREE from 'three';
import { fetchMarbleWorlds, type MarbleWorld } from '../utils/api';

// ---------------------------------------------------------------------------
// Episode fallback metadata — colors and mood per episode
// ---------------------------------------------------------------------------

const EPISODE_FALLBACKS: Record<
  number,
  {
    label: string;
    primary: string;
    secondary: string;
    accent: string;
    fogColor: string;
    description: string;
  }
> = {
  1: {
    label: 'Waterfront Theater',
    primary: '#7B68EE',
    secondary: '#4B0082',
    accent: '#FFD700',
    fogColor: '#0D0B1A',
    description: 'An amphitheater on the Delaware River at sunset.',
  },
  2: {
    label: 'Cinema Garden',
    primary: '#00C853',
    secondary: '#1B5E20',
    accent: '#FFEB3B',
    fogColor: '#0A1A0D',
    description: 'An outdoor cinema surrounded by wildflowers at twilight.',
  },
  3: {
    label: 'Rooftop Skate Park',
    primary: '#FF6D00',
    secondary: '#BF360C',
    accent: '#FFC107',
    fogColor: '#1A0F0A',
    description: 'A rooftop skatepark bathed in golden hour light.',
  },
  4: {
    label: 'Art Alley',
    primary: '#E040FB',
    secondary: '#7B1FA2',
    accent: '#00E5FF',
    fogColor: '#120A1A',
    description: 'A narrow alley transformed into an immersive neon gallery.',
  },
  5: {
    label: 'Sound Garden',
    primary: '#26C6DA',
    secondary: '#00695C',
    accent: '#B2FF59',
    fogColor: '#0A1A1A',
    description: 'A garden of musical instruments in morning mist.',
  },
  6: {
    label: 'Climbing Gym Underpass',
    primary: '#FF7043',
    secondary: '#D84315',
    accent: '#FFAB40',
    fogColor: '#1A0D0A',
    description: 'A climbing gym under a highway overpass.',
  },
  7: {
    label: 'Night Market',
    primary: '#FFD54F',
    secondary: '#F57F17',
    accent: '#FF4081',
    fogColor: '#1A150A',
    description: 'A vibrant night market with lanterns and steam.',
  },
  8: {
    label: 'Winter Village',
    primary: '#90CAF9',
    secondary: '#1565C0',
    accent: '#FFE082',
    fogColor: '#0A0F1A',
    description: 'A winter village with skating rink and holiday lights.',
  },
  9: {
    label: 'Skating Corridor',
    primary: '#80DEEA',
    secondary: '#00838F',
    accent: '#F8BBD0',
    fogColor: '#0A1518',
    description: 'A narrow ice skating path with fairy lights overhead.',
  },
  10: {
    label: 'Recovery Garden',
    primary: '#A5D6A7',
    secondary: '#2E7D32',
    accent: '#BCAAA4',
    fogColor: '#0D1A0D',
    description: 'A peaceful therapeutic garden in soft morning light.',
  },
};

// ---------------------------------------------------------------------------
// SplatWorld — renders a Gaussian splat via SparkJS inside R3F
// ---------------------------------------------------------------------------

function SplatWorld({ url }: { url: string }) {
  const { gl, scene, camera } = useThree();
  const sparkRef = useRef<any>(null);
  const splatRef = useRef<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let disposed = false;

    async function init() {
      try {
        // Dynamic import to avoid SSR/bundling issues
        const { SparkRenderer, SplatMesh } = await import(
          '@sparkjsdev/spark'
        );

        if (disposed) return;

        // Create SparkRenderer (extends THREE.Mesh, must be in the scene)
        const spark = new SparkRenderer({
          renderer: gl,
        });
        sparkRef.current = spark;
        scene.add(spark);

        // Create SplatMesh from URL
        const splat = new SplatMesh({
          url,
          onLoad: () => {
            if (!disposed) setLoading(false);
          },
        });
        splatRef.current = splat;
        scene.add(splat);

        // Wait for initialization
        await splat.initialized;
        if (!disposed) setLoading(false);
      } catch (err) {
        console.error('Failed to load splat world:', err);
        if (!disposed) setLoading(false);
      }
    }

    init();

    return () => {
      disposed = true;
      if (splatRef.current) {
        scene.remove(splatRef.current);
        splatRef.current.dispose?.();
      }
      if (sparkRef.current) {
        scene.remove(sparkRef.current);
        sparkRef.current.dispose?.();
      }
    };
  }, [url, gl, scene]);

  // Drive SparkRenderer update each frame
  useFrame(() => {
    if (sparkRef.current) {
      sparkRef.current.update({ scene });
    }
  });

  if (loading) {
    return (
      <mesh>
        <sphereGeometry args={[0.3, 16, 16]} />
        <meshBasicMaterial color="#ffffff" wireframe />
      </mesh>
    );
  }

  return null;
}

// ---------------------------------------------------------------------------
// FallbackWorld — procedural geometric scene per episode
// ---------------------------------------------------------------------------

function FallbackWorld({ episodeNum }: { episodeNum: number }) {
  const fb = EPISODE_FALLBACKS[episodeNum];
  const groupRef = useRef<THREE.Group>(null);
  const primary = new THREE.Color(fb.primary);
  const secondary = new THREE.Color(fb.secondary);
  const accent = new THREE.Color(fb.accent);

  // Generate random shapes per episode deterministically
  const shapes = useMemo(() => {
    const items: {
      pos: [number, number, number];
      scale: [number, number, number];
      color: THREE.Color;
      type: 'box' | 'sphere' | 'torus' | 'cylinder' | 'cone';
      rotSpeed: number;
    }[] = [];

    // Seed-like behavior from episode number
    const seed = episodeNum * 137.5;
    for (let i = 0; i < 24; i++) {
      const angle = (i / 24) * Math.PI * 2 + seed;
      const radius = 3 + Math.sin(seed + i * 0.7) * 4;
      const height = Math.sin(seed + i * 1.3) * 3 + 1;
      const s = 0.3 + Math.abs(Math.sin(seed + i * 2.1)) * 0.8;
      const colors = [primary, secondary, accent];
      const color = colors[i % 3];
      const types: ('box' | 'sphere' | 'torus' | 'cylinder' | 'cone')[] = [
        'box',
        'sphere',
        'torus',
        'cylinder',
        'cone',
      ];
      items.push({
        pos: [
          Math.cos(angle) * radius,
          height,
          Math.sin(angle) * radius,
        ],
        scale: [s, s, s],
        color,
        type: types[i % 5],
        rotSpeed: 0.2 + Math.sin(seed + i) * 0.3,
      });
    }
    return items;
  }, [episodeNum, primary, secondary, accent]);

  useFrame((_, delta) => {
    if (groupRef.current) {
      groupRef.current.rotation.y += delta * 0.05;
    }
  });

  return (
    <>
      <fog attach="fog" args={[fb.fogColor, 15, 50]} />
      <ambientLight intensity={0.3} />
      <directionalLight position={[10, 15, 10]} intensity={0.8} color="#ffffff" />
      <pointLight
        position={[0, 5, 0]}
        intensity={1.5}
        color={fb.primary}
        distance={20}
      />
      <Stars
        radius={40}
        depth={50}
        count={1000}
        factor={3}
        fade
        speed={0.5}
      />

      {/* Ground plane */}
      <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, -0.5, 0]} receiveShadow>
        <planeGeometry args={[60, 60]} />
        <meshStandardMaterial
          color={fb.fogColor}
          roughness={0.9}
          metalness={0.1}
        />
      </mesh>

      {/* Central glowing orb */}
      <Float speed={2} rotationIntensity={0.5} floatIntensity={1}>
        <mesh position={[0, 3, 0]}>
          <icosahedronGeometry args={[1.2, 2]} />
          <meshStandardMaterial
            color={fb.primary}
            emissive={fb.primary}
            emissiveIntensity={0.6}
            roughness={0.2}
            metalness={0.8}
          />
        </mesh>
      </Float>

      {/* Scattered shapes */}
      <group ref={groupRef}>
        {shapes.map((shape, i) => (
          <Float
            key={i}
            speed={1 + shape.rotSpeed}
            rotationIntensity={0.3}
            floatIntensity={0.5}
          >
            <mesh position={shape.pos} scale={shape.scale} castShadow>
              {shape.type === 'box' && <boxGeometry args={[1, 1, 1]} />}
              {shape.type === 'sphere' && (
                <sphereGeometry args={[0.6, 16, 16]} />
              )}
              {shape.type === 'torus' && (
                <torusGeometry args={[0.5, 0.2, 12, 24]} />
              )}
              {shape.type === 'cylinder' && (
                <cylinderGeometry args={[0.3, 0.3, 1.2, 12]} />
              )}
              {shape.type === 'cone' && (
                <coneGeometry args={[0.4, 1, 12]} />
              )}
              <meshStandardMaterial
                color={shape.color}
                emissive={shape.color}
                emissiveIntensity={0.15}
                roughness={0.4}
                metalness={0.6}
              />
            </mesh>
          </Float>
        ))}
      </group>
    </>
  );
}

// ---------------------------------------------------------------------------
// Episode selector sidebar
// ---------------------------------------------------------------------------

function EpisodeSelector({
  worlds,
  activeEpisode,
  onSelect,
}: {
  worlds: MarbleWorld[];
  activeEpisode: number;
  onSelect: (ep: number) => void;
}) {
  return (
    <div
      style={{
        position: 'absolute',
        top: 0,
        right: 0,
        bottom: 0,
        width: 280,
        zIndex: 30,
        background: 'linear-gradient(to left, rgba(5,5,5,0.95), rgba(5,5,5,0.6))',
        backdropFilter: 'blur(16px)',
        WebkitBackdropFilter: 'blur(16px)',
        overflowY: 'auto',
        padding: '24px 16px',
        display: 'flex',
        flexDirection: 'column',
        gap: 4,
        fontFamily: "'Inter', system-ui, sans-serif",
      }}
    >
      <p
        style={{
          fontSize: 10,
          letterSpacing: '0.18em',
          textTransform: 'uppercase',
          color: 'rgba(255,255,255,0.35)',
          marginBottom: 12,
          paddingLeft: 8,
        }}
      >
        Episodes
      </p>
      {worlds.map((w) => {
        const fb = EPISODE_FALLBACKS[w.episode_num];
        const isActive = w.episode_num === activeEpisode;
        const isReady = w.status === 'ready' && w.splat_url;
        return (
          <button
            key={w.episode_num}
            onClick={() => onSelect(w.episode_num)}
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: 10,
              padding: '10px 12px',
              border: isActive
                ? `1px solid ${fb?.primary || '#fff'}44`
                : '1px solid transparent',
              borderRadius: 8,
              background: isActive
                ? `${fb?.primary || '#fff'}12`
                : 'transparent',
              color: isActive ? '#FFFFFF' : 'rgba(255,255,255,0.55)',
              fontSize: 13,
              fontFamily: "'Inter', system-ui, sans-serif",
              fontWeight: isActive ? 500 : 400,
              cursor: 'pointer',
              textAlign: 'left',
              transition: 'all 0.2s ease',
              width: '100%',
              letterSpacing: '0.01em',
            }}
            onMouseEnter={(e) => {
              if (!isActive) {
                (e.currentTarget as HTMLElement).style.background =
                  'rgba(255,255,255,0.04)';
                (e.currentTarget as HTMLElement).style.color =
                  'rgba(255,255,255,0.8)';
              }
            }}
            onMouseLeave={(e) => {
              if (!isActive) {
                (e.currentTarget as HTMLElement).style.background =
                  'transparent';
                (e.currentTarget as HTMLElement).style.color =
                  'rgba(255,255,255,0.55)';
              }
            }}
          >
            {/* Episode number pill */}
            <span
              style={{
                display: 'inline-flex',
                alignItems: 'center',
                justifyContent: 'center',
                width: 24,
                height: 24,
                borderRadius: 6,
                fontSize: 11,
                fontWeight: 600,
                background: isActive
                  ? fb?.primary || '#fff'
                  : 'rgba(255,255,255,0.08)',
                color: isActive ? '#050505' : 'rgba(255,255,255,0.4)',
                flexShrink: 0,
                transition: 'all 0.2s ease',
              }}
            >
              {w.episode_num}
            </span>
            <span style={{ flex: 1, lineHeight: 1.3 }}>
              {fb?.label || w.title}
            </span>
            {/* Status dot */}
            <span
              style={{
                width: 6,
                height: 6,
                borderRadius: '50%',
                background: isReady
                  ? '#00C853'
                  : w.status === 'error'
                    ? '#FF5252'
                    : 'rgba(255,255,255,0.15)',
                flexShrink: 0,
              }}
              title={
                isReady
                  ? 'Marble world ready'
                  : w.status === 'error'
                    ? 'Generation failed'
                    : 'Geometric fallback'
              }
            />
          </button>
        );
      })}

      {/* Legend */}
      <div
        style={{
          marginTop: 16,
          padding: '12px 8px',
          borderTop: '1px solid rgba(255,255,255,0.06)',
          display: 'flex',
          flexDirection: 'column',
          gap: 6,
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
          <span
            style={{
              width: 6,
              height: 6,
              borderRadius: '50%',
              background: '#00C853',
            }}
          />
          <span style={{ fontSize: 10, color: 'rgba(255,255,255,0.3)' }}>
            Marble splat world
          </span>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
          <span
            style={{
              width: 6,
              height: 6,
              borderRadius: '50%',
              background: 'rgba(255,255,255,0.15)',
            }}
          />
          <span style={{ fontSize: 10, color: 'rgba(255,255,255,0.3)' }}>
            Geometric fallback
          </span>
        </div>
      </div>
    </div>
  );
}

// ---------------------------------------------------------------------------
// MarbleWorlds — main component
// ---------------------------------------------------------------------------

interface MarbleWorldsProps {
  onClose: () => void;
  initialEpisode?: number;
}

export default function MarbleWorlds({
  onClose,
  initialEpisode = 1,
}: MarbleWorldsProps) {
  const [worlds, setWorlds] = useState<MarbleWorld[]>([]);
  const [activeEpisode, setActiveEpisode] = useState(initialEpisode);
  const [loading, setLoading] = useState(true);
  const [canvasReady, setCanvasReady] = useState(false);

  // Fetch marble worlds from backend
  useEffect(() => {
    let cancelled = false;
    async function load() {
      try {
        const data = await fetchMarbleWorlds();
        if (!cancelled) {
          setWorlds(data);
          setLoading(false);
        }
      } catch {
        // If backend is down, create placeholder worlds
        if (!cancelled) {
          const placeholders: MarbleWorld[] = Array.from(
            { length: 10 },
            (_, i) => ({
              episode_num: i + 1,
              slug: EPISODE_FALLBACKS[i + 1]?.label || `episode-${i + 1}`,
              title: EPISODE_FALLBACKS[i + 1]?.label || `Episode ${i + 1}`,
              world_id: null,
              splat_url: null,
              status: 'pending' as const,
            }),
          );
          setWorlds(placeholders);
          setLoading(false);
        }
      }
    }
    load();
    return () => {
      cancelled = true;
    };
  }, []);

  const handleSelect = useCallback((ep: number) => {
    setCanvasReady(false);
    setActiveEpisode(ep);
  }, []);

  const handleCanvasCreated = useCallback(() => {
    setCanvasReady(true);
  }, []);

  const currentWorld = worlds.find((w) => w.episode_num === activeEpisode);
  const hasSplat =
    currentWorld?.status === 'ready' && currentWorld?.splat_url;
  const fb = EPISODE_FALLBACKS[activeEpisode];

  return (
    <div
      style={{
        position: 'fixed',
        inset: 0,
        zIndex: 100,
        background: '#050505',
        fontFamily: "'Inter', system-ui, sans-serif",
      }}
    >
      {/* Loading state */}
      {loading && (
        <div
          style={{
            position: 'absolute',
            inset: 0,
            zIndex: 60,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            gap: 16,
            color: '#FFFFFF',
          }}
        >
          <div
            style={{
              width: 40,
              height: 40,
              border: '2px solid rgba(255,255,255,0.15)',
              borderTopColor: '#fff',
              borderRadius: '50%',
              animation: 'marbleSpin 1s linear infinite',
            }}
          />
          <p
            style={{
              fontSize: 13,
              opacity: 0.5,
              letterSpacing: '0.08em',
            }}
          >
            Loading worlds...
          </p>
          <style>{`@keyframes marbleSpin { to { transform: rotate(360deg) } }`}</style>
        </div>
      )}

      {/* Canvas loading overlay (shows while Three.js initializes) */}
      {!loading && !canvasReady && (
        <div
          style={{
            position: 'absolute',
            inset: 0,
            zIndex: 40,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            gap: 16,
            color: '#FFFFFF',
          }}
        >
          <div
            style={{
              width: 40,
              height: 40,
              border: '2px solid rgba(255,255,255,0.15)',
              borderTopColor: fb?.primary || '#fff',
              borderRadius: '50%',
              animation: 'marbleSpin 1s linear infinite',
            }}
          />
          <p
            style={{
              fontSize: 13,
              opacity: 0.5,
              letterSpacing: '0.08em',
            }}
          >
            Building world...
          </p>
        </div>
      )}

      {/* Three.js Canvas */}
      {!loading && (
        <Canvas
          shadows
          dpr={[1, 1.5]}
          gl={{
            antialias: true,
            toneMapping: THREE.ACESFilmicToneMapping,
            toneMappingExposure: 1.0,
          }}
          camera={{ position: [12, 8, 12], fov: 50, near: 0.1, far: 500 }}
          onCreated={handleCanvasCreated}
          style={{
            width: '100%',
            height: '100%',
            opacity: canvasReady ? 1 : 0,
            transition: 'opacity 0.8s ease',
          }}
        >
          {hasSplat ? (
            <SplatWorld url={currentWorld!.splat_url!} />
          ) : (
            <FallbackWorld episodeNum={activeEpisode} />
          )}
          <OrbitControls
            enablePan={false}
            enableZoom
            minDistance={3}
            maxDistance={60}
            maxPolarAngle={Math.PI / 2.1}
            autoRotate
            autoRotateSpeed={0.4}
            enableDamping
            dampingFactor={0.05}
          />
        </Canvas>
      )}

      {/* Close button */}
      <button
        onClick={onClose}
        style={{
          position: 'absolute',
          top: 20,
          left: 20,
          zIndex: 50,
          display: 'flex',
          alignItems: 'center',
          gap: 8,
          padding: '10px 18px',
          border: '1px solid rgba(255,255,255,0.15)',
          borderRadius: 12,
          backgroundColor: 'rgba(5,5,5,0.6)',
          backdropFilter: 'blur(12px)',
          WebkitBackdropFilter: 'blur(12px)',
          color: '#FFFFFF',
          fontSize: 13,
          fontFamily: "'Inter', system-ui, sans-serif",
          fontWeight: 400,
          letterSpacing: '0.04em',
          cursor: 'pointer',
          transition: 'background-color 0.2s, border-color 0.2s',
        }}
        onMouseEnter={(e) => {
          (e.currentTarget as HTMLElement).style.backgroundColor =
            'rgba(255,255,255,0.1)';
          (e.currentTarget as HTMLElement).style.borderColor =
            'rgba(255,255,255,0.3)';
        }}
        onMouseLeave={(e) => {
          (e.currentTarget as HTMLElement).style.backgroundColor =
            'rgba(5,5,5,0.6)';
          (e.currentTarget as HTMLElement).style.borderColor =
            'rgba(255,255,255,0.15)';
        }}
      >
        <svg
          width="14"
          height="14"
          viewBox="0 0 14 14"
          fill="none"
          stroke="currentColor"
          strokeWidth="1.5"
          strokeLinecap="round"
        >
          <line x1="2" y1="2" x2="12" y2="12" />
          <line x1="12" y1="2" x2="2" y2="12" />
        </svg>
        Close
      </button>

      {/* Episode info overlay (bottom-left) */}
      <div
        style={{
          position: 'absolute',
          bottom: 24,
          left: 24,
          zIndex: 30,
          color: '#FFFFFF',
          pointerEvents: 'none',
          maxWidth: 360,
        }}
      >
        <p
          style={{
            fontSize: 10,
            letterSpacing: '0.14em',
            textTransform: 'uppercase',
            opacity: 0.35,
            margin: '0 0 4px 0',
          }}
        >
          Episode {activeEpisode} / 10
          {hasSplat ? ' \u2022 Marble World' : ' \u2022 Geometric'}
        </p>
        <p
          style={{
            fontSize: 20,
            fontWeight: 300,
            letterSpacing: '0.02em',
            margin: '0 0 6px 0',
            opacity: 0.85,
            textShadow: '0 2px 8px rgba(0,0,0,0.5)',
          }}
        >
          {fb?.label || currentWorld?.title}
        </p>
        <p
          style={{
            fontSize: 12,
            opacity: 0.4,
            lineHeight: 1.5,
            margin: 0,
          }}
        >
          {fb?.description}
        </p>
      </div>

      {/* Keyboard nav hint */}
      <div
        style={{
          position: 'absolute',
          bottom: 24,
          right: 296,
          zIndex: 30,
          color: 'rgba(255,255,255,0.2)',
          fontSize: 10,
          letterSpacing: '0.06em',
          pointerEvents: 'none',
          display: 'flex',
          gap: 12,
          alignItems: 'center',
        }}
      >
        <span
          style={{
            padding: '3px 8px',
            border: '1px solid rgba(255,255,255,0.1)',
            borderRadius: 4,
          }}
        >
          &larr;
        </span>
        <span
          style={{
            padding: '3px 8px',
            border: '1px solid rgba(255,255,255,0.1)',
            borderRadius: 4,
          }}
        >
          &rarr;
        </span>
        <span>Navigate</span>
      </div>

      {/* Episode selector sidebar */}
      {!loading && (
        <EpisodeSelector
          worlds={worlds}
          activeEpisode={activeEpisode}
          onSelect={handleSelect}
        />
      )}

      {/* Keyboard navigation */}
      <KeyboardNav
        activeEpisode={activeEpisode}
        onSelect={handleSelect}
        onClose={onClose}
      />
    </div>
  );
}

// ---------------------------------------------------------------------------
// Keyboard navigation hook component
// ---------------------------------------------------------------------------

function KeyboardNav({
  activeEpisode,
  onSelect,
  onClose,
}: {
  activeEpisode: number;
  onSelect: (ep: number) => void;
  onClose: () => void;
}) {
  useEffect(() => {
    function handleKeyDown(e: KeyboardEvent) {
      if (e.key === 'ArrowRight' || e.key === 'ArrowDown') {
        e.preventDefault();
        onSelect(activeEpisode < 10 ? activeEpisode + 1 : 1);
      } else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') {
        e.preventDefault();
        onSelect(activeEpisode > 1 ? activeEpisode - 1 : 10);
      } else if (e.key === 'Escape') {
        onClose();
      } else if (e.key >= '1' && e.key <= '9') {
        onSelect(parseInt(e.key));
      } else if (e.key === '0') {
        onSelect(10);
      }
    }
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [activeEpisode, onSelect, onClose]);

  return null;
}
