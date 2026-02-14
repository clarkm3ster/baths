import { Suspense, useState, useEffect, useCallback, lazy } from 'react';
import { Canvas } from '@react-three/fiber';
import { OrbitControls } from '@react-three/drei';
import PermanenceOverlay from './PermanenceOverlay';

// ---------- Episode metadata ----------

interface EpisodeMeta {
  title: string;
  subtitle: string;
  permanencePercent: number;
  permanenceItems: string[];
}

const EPISODE_META: Record<string, EpisodeMeta> = {
  'waterfront': {
    title: 'Episode 1 \u2014 Magical Realism',
    subtitle: 'The Floating Theater',
    permanencePercent: 72,
    permanenceItems: [
      'When the show leaves, the dock stays.',
      'The lighting stays.',
      'The waterfront access stays.',
    ],
  },
  'cinema-garden': {
    title: 'Episode 2 \u2014 Documentary',
    subtitle: 'The Cinema Garden',
    permanencePercent: 85,
    permanenceItems: [
      'The raised beds stay.',
      'The screening wall stays.',
      'The irrigation stays.',
    ],
  },
  'rooftop': {
    title: 'Episode 3 \u2014 Action',
    subtitle: 'The Sky Park',
    permanencePercent: 90,
    permanenceItems: [
      'The skatepark structures stay.',
      'The sound system stays.',
      'The safety railings and ADA ramp stay.',
    ],
  },
  'alley': {
    title: 'Episode 4 \u2014 Mystery',
    subtitle: 'The Light Alley',
    permanencePercent: 80,
    permanenceItems: [
      'The projection hardware stays.',
      'The gallery walls stay.',
      'The embedded ground lighting stays.',
    ],
  },
  'sound-garden': {
    title: 'Episode 5 \u2014 Fantasy',
    subtitle: 'The Sound Garden',
    permanencePercent: 92,
    permanenceItems: [
      'The bronze sculptures stay.',
      'The pathways stay.',
      'The meditation circle stays.',
    ],
  },
  'underpass': {
    title: 'Episode 6 \u2014 Adventure',
    subtitle: 'The Vertical Playground',
    permanencePercent: 88,
    permanenceItems: [
      'The climbing walls stay forever.',
      'The ground surfacing stays forever.',
      'The lighting stays forever.',
    ],
  },
  'night-market': {
    title: 'Episode 7 \u2014 Ensemble Comedy',
    subtitle: 'The Night Market',
    permanencePercent: 75,
    permanenceItems: [
      'The vendor electrical hookups stay.',
      'The market pavilion structure stays.',
      'The string-light infrastructure stays.',
    ],
  },
  'winter-village': {
    title: 'Episode 8 \u2014 Romance',
    subtitle: 'The Winter Village',
    permanencePercent: 70,
    permanenceItems: [
      'The ice rink plumbing stays.',
      'The power and lighting infrastructure stays.',
      'The heated gathering pavilion stays.',
    ],
  },
  'glow-corridor': {
    title: 'Episode 9 \u2014 Thriller',
    subtitle: 'The Glow Corridor',
    permanencePercent: 93,
    permanenceItems: [
      'The solar LED path lighting stays.',
      'The fitness stations stay.',
      'The rest shelters stay.',
    ],
  },
  'quiet-garden': {
    title: 'Episode 10 \u2014 Quiet Drama',
    subtitle: 'The Recovery Garden',
    permanencePercent: 100,
    permanenceItems: [
      'The entire garden stays.',
      'The water feature stays.',
      'The winding paths stay.',
      'The counseling pavilion stays.',
      'Every bench, every tree, every stone.',
      'Forever.',
    ],
  },
};

// ---------- Lazy world components ----------

const WaterfrontWorld = lazy(() => import('./episodes/WaterfrontWorld'));
const CinemaGardenWorld = lazy(() => import('./episodes/CinemaGardenWorld'));
const RooftopWorld = lazy(() => import('./episodes/RooftopWorld'));
const AlleyWorld = lazy(() => import('./episodes/AlleyWorld'));
const SoundGardenWorld = lazy(() => import('./episodes/SoundGardenWorld'));
const UnderpassWorld = lazy(() => import('./episodes/UnderpassWorld'));
const NightMarketWorld = lazy(() => import('./episodes/NightMarketWorld'));
const WinterVillageWorld = lazy(() => import('./episodes/WinterVillageWorld'));
const GlowCorridorWorld = lazy(() => import('./episodes/GlowCorridorWorld'));
const QuietGardenWorld = lazy(() => import('./episodes/QuietGardenWorld'));

function getWorldComponent(slug: string) {
  switch (slug) {
    case 'waterfront':
      return <WaterfrontWorld />;
    case 'cinema-garden':
      return <CinemaGardenWorld />;
    case 'rooftop':
      return <RooftopWorld />;
    case 'alley':
      return <AlleyWorld />;
    case 'sound-garden':
      return <SoundGardenWorld />;
    case 'underpass':
      return <UnderpassWorld />;
    case 'night-market':
      return <NightMarketWorld />;
    case 'winter-village':
      return <WinterVillageWorld />;
    case 'glow-corridor':
      return <GlowCorridorWorld />;
    case 'quiet-garden':
      return <QuietGardenWorld />;
    default:
      return null;
  }
}

// ---------- Loading fallback (in-canvas) ----------

function LoadingIndicator() {
  return (
    <mesh>
      <sphereGeometry args={[0.3, 16, 16]} />
      <meshBasicMaterial color="#ffffff" wireframe />
    </mesh>
  );
}

// ---------- Main component ----------

interface WorldRendererProps {
  episodeSlug: string;
  onClose: () => void;
}

export default function WorldRenderer({
  episodeSlug,
  onClose,
}: WorldRendererProps) {
  const [showPermanence, setShowPermanence] = useState(false);
  const [isLoaded, setIsLoaded] = useState(false);

  const meta = EPISODE_META[episodeSlug];

  // 30-second permanence timer
  useEffect(() => {
    if (!isLoaded) return;
    const timer = setTimeout(() => setShowPermanence(true), 30000);
    return () => clearTimeout(timer);
  }, [isLoaded]);

  const handleCreated = useCallback(() => {
    setIsLoaded(true);
  }, []);

  if (!meta) {
    return (
      <div
        style={{
          position: 'fixed',
          inset: 0,
          zIndex: 50,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          backgroundColor: '#000',
          color: '#fff',
          fontFamily: "'Inter', sans-serif",
          fontSize: 18,
        }}
      >
        Unknown episode: {episodeSlug}
      </div>
    );
  }

  return (
    <div
      style={{
        position: 'fixed',
        inset: 0,
        zIndex: 50,
        backgroundColor: '#000',
      }}
    >
      {/* Loading overlay before Canvas is ready */}
      {!isLoaded && (
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
            color: '#fff',
            fontFamily: "'Inter', sans-serif",
          }}
        >
          <div
            style={{
              width: 40,
              height: 40,
              border: '2px solid rgba(255,255,255,0.15)',
              borderTopColor: '#fff',
              borderRadius: '50%',
              animation: 'spin 1s linear infinite',
            }}
          />
          <p style={{ fontSize: 13, opacity: 0.5, letterSpacing: '0.08em' }}>
            Building world...
          </p>
          <style>{`@keyframes spin { to { transform: rotate(360deg) } }`}</style>
        </div>
      )}

      {/* Three.js Canvas */}
      <Canvas
        shadows
        dpr={[1, 1.5]}
        gl={{
          antialias: true,
          toneMapping: 3, // ACESFilmicToneMapping
          toneMappingExposure: 1.0,
        }}
        camera={{ position: [12, 8, 12], fov: 50, near: 0.1, far: 500 }}
        onCreated={handleCreated}
        style={{
          width: '100%',
          height: '100%',
          opacity: isLoaded ? 1 : 0,
          transition: 'opacity 0.8s ease',
        }}
      >
        <Suspense fallback={<LoadingIndicator />}>
          {getWorldComponent(episodeSlug)}
        </Suspense>
        <OrbitControls
          enablePan={false}
          enableZoom={true}
          minDistance={5}
          maxDistance={60}
          maxPolarAngle={Math.PI / 2.1}
          autoRotate
          autoRotateSpeed={0.4}
          enableDamping
          dampingFactor={0.05}
        />
      </Canvas>

      {/* Close button */}
      <button
        onClick={onClose}
        style={{
          position: 'absolute',
          top: 20,
          left: 20,
          zIndex: 20,
          display: 'flex',
          alignItems: 'center',
          gap: 8,
          padding: '10px 18px',
          border: '1px solid rgba(255,255,255,0.15)',
          borderRadius: 12,
          backgroundColor: 'rgba(0,0,0,0.4)',
          backdropFilter: 'blur(12px)',
          WebkitBackdropFilter: 'blur(12px)',
          color: '#fff',
          fontSize: 13,
          fontFamily: "'Inter', sans-serif",
          fontWeight: 400,
          letterSpacing: '0.04em',
          cursor: 'pointer',
          transition: 'background-color 0.2s, border-color 0.2s',
        }}
        onMouseEnter={(e) => {
          (e.target as HTMLElement).style.backgroundColor =
            'rgba(255,255,255,0.1)';
          (e.target as HTMLElement).style.borderColor =
            'rgba(255,255,255,0.3)';
        }}
        onMouseLeave={(e) => {
          (e.target as HTMLElement).style.backgroundColor =
            'rgba(0,0,0,0.4)';
          (e.target as HTMLElement).style.borderColor =
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

      {/* Episode title overlay */}
      <div
        style={{
          position: 'absolute',
          bottom: 24,
          left: 24,
          zIndex: 20,
          color: '#fff',
          fontFamily: "'Inter', sans-serif",
          pointerEvents: 'none',
        }}
      >
        <p
          style={{
            fontSize: 11,
            letterSpacing: '0.12em',
            textTransform: 'uppercase',
            opacity: 0.4,
            margin: '0 0 4px 0',
          }}
        >
          {meta.title}
        </p>
        <p
          style={{
            fontSize: 18,
            fontWeight: 300,
            letterSpacing: '0.02em',
            margin: 0,
            opacity: 0.75,
            textShadow: '0 2px 8px rgba(0,0,0,0.5)',
          }}
        >
          {meta.subtitle}
        </p>
      </div>

      {/* Permanence overlay */}
      {showPermanence && (
        <PermanenceOverlay
          permanenceItems={meta.permanenceItems}
          permanencePercent={meta.permanencePercent}
          episodeTitle={`${meta.title}: ${meta.subtitle}`}
        />
      )}
    </div>
  );
}
