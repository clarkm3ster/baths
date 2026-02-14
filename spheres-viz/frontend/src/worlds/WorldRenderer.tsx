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
    title: 'Episode 1',
    subtitle: 'Floating Theater on the Delaware',
    permanencePercent: 85,
    permanenceItems: [
      'Permanent barge stage and pier infrastructure',
      'Waterfront amphitheater seating',
      'Lighting grid and power connections',
      'ADA-accessible riverfront promenade',
    ],
  },
  'cinema-garden': {
    title: 'Episode 2',
    subtitle: 'Cinema Garden in Kensington',
    permanencePercent: 90,
    permanenceItems: [
      'Outdoor screening wall and AV infrastructure',
      'Raised community garden beds',
      'Permanent seating and gathering area',
      'Native pollinator landscaping',
    ],
  },
  'rooftop': {
    title: 'Episode 3',
    subtitle: 'Sky Park above Chinatown',
    permanencePercent: 95,
    permanenceItems: [
      'Rooftop skatepark with ramps and rails',
      'DJ booth and sound system housing',
      'Safety railings and ADA ramp access',
      'Graffiti art walls (rotating commissions)',
    ],
  },
  'alley': {
    title: 'Episode 4',
    subtitle: 'Art Corridor in Old City',
    permanencePercent: 80,
    permanenceItems: [
      'Permanent projection-mapping hardware',
      'Gallery-quality wall surfaces',
      'Embedded ground lighting',
      'Weather-protected art display frames',
    ],
  },
  'sound-garden': {
    title: 'Episode 5',
    subtitle: 'Sound Garden in FDR Park',
    permanencePercent: 92,
    permanenceItems: [
      'Bronze sound sculptures and wind harps',
      'Whisper dish installation',
      'Accessible winding pathway network',
      'Meditation benches and gathering areas',
    ],
  },
  'underpass': {
    title: 'Episode 6',
    subtitle: 'Climbing Gym beneath I-95',
    permanencePercent: 88,
    permanenceItems: [
      'Professional climbing walls with holds',
      'Safety matting and fall zones',
      'LED lighting rig on highway infrastructure',
      'Youth program equipment storage',
    ],
  },
  'night-market': {
    title: 'Episode 7',
    subtitle: 'Night Market on Broad Street',
    permanencePercent: 75,
    permanenceItems: [
      'Permanent vendor stall foundations',
      'String-light infrastructure and power drops',
      'Music stage with roof structure',
      'Commercial kitchen hookups',
    ],
  },
  'winter-village': {
    title: 'Episode 8',
    subtitle: 'Winter Village at City Hall',
    permanencePercent: 70,
    permanenceItems: [
      'Seasonal ice rink plumbing and refrigeration',
      'Market cabin foundations (seasonal deploy)',
      'Permanent power and lighting infrastructure',
      'Heated gathering pavilion',
    ],
  },
  'glow-corridor': {
    title: 'Episode 9',
    subtitle: 'Illuminated Corridor on Schuylkill Banks',
    permanencePercent: 93,
    permanenceItems: [
      'LED path lighting system (solar-powered)',
      'Fitness stations along the corridor',
      'Rest shelters and seating',
      'Accessible trail surface improvements',
    ],
  },
  'quiet-garden': {
    title: 'Episode 10',
    subtitle: 'Recovery Garden in West Philadelphia',
    permanencePercent: 96,
    permanenceItems: [
      'Labyrinth walking path in stone',
      'Central water feature with recirculation',
      'Walled garden perimeter and plantings',
      'Meditation circle and gathering benches',
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
