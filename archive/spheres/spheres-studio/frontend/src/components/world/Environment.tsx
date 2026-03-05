/**
 * Environment.tsx — Scene environment for the SPHERES WorldView.
 *
 * Handles:
 *   - Ground plane (parcel footprint extruded from shape)
 *   - Sky (drei Sky component with dynamic sun position)
 *   - Directional light with shadow maps (sun)
 *   - Ambient light for fill
 *   - Time-of-day control (drives sun position, colour, intensity)
 *   - Before mode: cracked concrete, dead grass, litter, chain-link fence, overcast
 *   - After mode: clean ground, green grass, blue sky, warm sunlight
 *   - Permanence mode: same as After but slightly muted
 *   - Fog (mode-dependent)
 *   - Simple animated clouds
 */

import { useRef, useMemo, type FC } from 'react';
import * as THREE from 'three';
import { useFrame } from '@react-three/fiber';
import { Sky, Stars, Cloud } from '@react-three/drei';
import {
  sunFromTimeOfDay,
  fogForMode,
  defaultParcelShape,
  type Polygon2D,
  type Point2D,
  type TimeOfDay,
  parcelFootprintToShape,
} from '../../utils/designTo3D';
import {
  ChainLinkFenceSegment,
  LitterObject,
  DeadGrassPatch,
  PersonSilhouette,
} from './ElementMeshes';

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

export type ViewMode = 'before' | 'after' | 'permanence';

export interface EnvironmentProps {
  mode: ViewMode;
  timeOfDay: TimeOfDay;
  parcelPolygon?: Polygon2D;
  parcelCenter?: Point2D;
  parcelWidth?: number;
  parcelDepth?: number;
  showPeople?: boolean;
}

// ---------------------------------------------------------------------------
// Ground plane
// ---------------------------------------------------------------------------

const GroundPlane: FC<{
  shape: THREE.Shape;
  mode: ViewMode;
}> = ({ shape, mode }) => {
  const geometry = useMemo(() => {
    const extrudeSettings: THREE.ExtrudeGeometryOptions = {
      depth: 0.2,
      bevelEnabled: false,
    };
    const geo = new THREE.ExtrudeGeometry(shape, extrudeSettings);
    // Rotate so extrusion goes into +Y (up) rather than +Z
    geo.rotateX(-Math.PI / 2);
    geo.translate(0, -0.1, 0);
    return geo;
  }, [shape]);

  const color = mode === 'before' ? '#7a7a72' : mode === 'permanence' ? '#6a8a5a' : '#5a9a4a';

  return (
    <mesh geometry={geometry} receiveShadow>
      <meshStandardMaterial
        color={color}
        roughness={mode === 'before' ? 0.95 : 0.85}
        metalness={0}
      />
    </mesh>
  );
};

// ---------------------------------------------------------------------------
// Extended ground (infinite-ish plane beyond parcel)
// ---------------------------------------------------------------------------

const ExtendedGround: FC<{ mode: ViewMode }> = ({ mode }) => {
  const color = mode === 'before' ? '#5a5a52' : mode === 'permanence' ? '#4a6a3a' : '#3a7a2a';
  return (
    <mesh position={[0, -0.15, 0]} rotation={[-Math.PI / 2, 0, 0]} receiveShadow>
      <planeGeometry args={[500, 500]} />
      <meshStandardMaterial color={color} roughness={0.95} />
    </mesh>
  );
};

// ---------------------------------------------------------------------------
// Before-mode: blight dressing
// ---------------------------------------------------------------------------

const BlightDressing: FC<{
  parcelWidth: number;
  parcelDepth: number;
}> = ({ parcelWidth, parcelDepth }) => {
  const hw = parcelWidth / 2;
  const hd = parcelDepth / 2;

  // Fence corners
  const corners: [number, number, number][] = [
    [-hw, 0, -hd],
    [hw, 0, -hd],
    [hw, 0, hd],
    [-hw, 0, hd],
  ];

  // Litter positions — deterministic from dimensions
  const litter = useMemo(() => {
    const items: { pos: [number, number, number]; type: 'can' | 'bag' | 'bottle' }[] = [];
    const seed = parcelWidth * 17 + parcelDepth * 31;
    for (let i = 0; i < 15; i++) {
      const pseudoRand = Math.abs(Math.sin(seed + i * 127.1));
      const pseudoRand2 = Math.abs(Math.sin(seed + i * 269.5));
      items.push({
        pos: [
          (pseudoRand - 0.5) * parcelWidth * 0.8,
          0.05,
          (pseudoRand2 - 0.5) * parcelDepth * 0.8,
        ],
        type: (['can', 'bag', 'bottle'] as const)[i % 3],
      });
    }
    return items;
  }, [parcelWidth, parcelDepth]);

  // Dead grass patches
  const grassPatches = useMemo(() => {
    const patches: { pos: [number, number, number]; size: number }[] = [];
    const seed = parcelWidth * 11 + parcelDepth * 23;
    for (let i = 0; i < 8; i++) {
      const pr1 = Math.abs(Math.sin(seed + i * 97.3));
      const pr2 = Math.abs(Math.sin(seed + i * 183.7));
      patches.push({
        pos: [(pr1 - 0.5) * parcelWidth * 0.7, -0.08, (pr2 - 0.5) * parcelDepth * 0.7],
        size: 2 + pr1 * 4,
      });
    }
    return patches;
  }, [parcelWidth, parcelDepth]);

  return (
    <group>
      {/* Chain-link fence around perimeter */}
      {corners.map((corner, i) => {
        const next = corners[(i + 1) % corners.length];
        return (
          <ChainLinkFenceSegment key={i} start={corner} end={next} />
        );
      })}

      {/* Litter */}
      {litter.map((item, i) => (
        <LitterObject key={i} position={item.pos} type={item.type} />
      ))}

      {/* Dead grass */}
      {grassPatches.map((patch, i) => (
        <DeadGrassPatch key={i} position={patch.pos} size={patch.size} />
      ))}

      {/* Cracked concrete patches */}
      {Array.from({ length: 4 }, (_, i) => {
        const pr1 = Math.abs(Math.sin(i * 53.7 + parcelWidth));
        const pr2 = Math.abs(Math.sin(i * 91.3 + parcelDepth));
        return (
          <mesh
            key={`crack${i}`}
            position={[
              (pr1 - 0.5) * parcelWidth * 0.5,
              -0.05,
              (pr2 - 0.5) * parcelDepth * 0.5,
            ]}
            rotation={[-Math.PI / 2, 0, pr1 * Math.PI]}
            receiveShadow
          >
            <planeGeometry args={[3 + pr1 * 4, 3 + pr2 * 4]} />
            <meshStandardMaterial color="#8a8882" roughness={0.98} />
          </mesh>
        );
      })}
    </group>
  );
};

// ---------------------------------------------------------------------------
// After-mode: people silhouettes scattered through the space
// ---------------------------------------------------------------------------

const PeopleScatter: FC<{ parcelWidth: number; parcelDepth: number }> = ({
  parcelWidth,
  parcelDepth,
}) => {
  const people = useMemo(() => {
    const result: { pos: [number, number, number]; color: string }[] = [];
    const colors = ['#334455', '#445566', '#3a3a5a', '#5a4a3a', '#4a5a4a', '#5a3a4a'];
    const seed = parcelWidth * 7 + parcelDepth * 13;
    for (let i = 0; i < 12; i++) {
      const pr1 = Math.abs(Math.sin(seed + i * 67.1));
      const pr2 = Math.abs(Math.sin(seed + i * 139.3));
      result.push({
        pos: [
          (pr1 - 0.5) * parcelWidth * 0.6,
          0,
          (pr2 - 0.5) * parcelDepth * 0.6,
        ],
        color: colors[i % colors.length],
      });
    }
    return result;
  }, [parcelWidth, parcelDepth]);

  return (
    <group>
      {people.map((person, i) => (
        <PersonSilhouette key={i} position={person.pos} color={person.color} />
      ))}
    </group>
  );
};

// ---------------------------------------------------------------------------
// Animated clouds
// ---------------------------------------------------------------------------

const AnimatedClouds: FC<{ mode: ViewMode }> = ({ mode }) => {
  const groupRef = useRef<THREE.Group>(null);

  useFrame(({ clock }) => {
    if (groupRef.current) {
      groupRef.current.position.x = Math.sin(clock.getElapsedTime() * 0.02) * 20;
    }
  });

  const opacity = mode === 'before' ? 0.9 : 0.6;

  return (
    <group ref={groupRef} position={[0, 60, 0]}>
      <Cloud
        position={[-30, 0, -20]}
        opacity={opacity}
        speed={0.2}
        segments={20}
      />
      <Cloud
        position={[20, 5, 10]}
        opacity={opacity}
        speed={0.15}
        segments={16}
      />
      <Cloud
        position={[50, -5, -30]}
        opacity={opacity}
        speed={0.1}
        segments={14}
      />
    </group>
  );
};

// ---------------------------------------------------------------------------
// Sun light with shadow map
// ---------------------------------------------------------------------------

const SunLight: FC<{ timeOfDay: TimeOfDay; mode: ViewMode }> = ({ timeOfDay, mode }) => {
  const sun = sunFromTimeOfDay(timeOfDay);
  const lightRef = useRef<THREE.DirectionalLight>(null);

  // Reduce intensity for before mode
  const intensityMultiplier = mode === 'before' ? 0.5 : mode === 'permanence' ? 0.8 : 1;

  return (
    <>
      <directionalLight
        ref={lightRef}
        position={sun.direction}
        color={mode === 'before' ? '#aaaaaa' : sun.color}
        intensity={sun.intensity * intensityMultiplier}
        castShadow
        shadow-mapSize-width={2048}
        shadow-mapSize-height={2048}
        shadow-camera-near={0.5}
        shadow-camera-far={500}
        shadow-camera-left={-80}
        shadow-camera-right={80}
        shadow-camera-top={80}
        shadow-camera-bottom={-80}
        shadow-bias={-0.001}
      />
      <ambientLight
        color={mode === 'before' ? '#666666' : sun.color}
        intensity={sun.ambientIntensity * intensityMultiplier}
      />
      {/* Hemisphere light for natural sky-ground colour bleed */}
      <hemisphereLight
        color={mode === 'before' ? '#888888' : '#aaccff'}
        groundColor={mode === 'before' ? '#444444' : '#446622'}
        intensity={0.3 * intensityMultiplier}
      />
    </>
  );
};

// ---------------------------------------------------------------------------
// Fog controller (sets scene fog each frame)
// ---------------------------------------------------------------------------

const FogController: FC<{ mode: ViewMode }> = ({ mode }) => {
  const fog = fogForMode(mode);

  useFrame(({ scene }) => {
    if (!scene.fog || !(scene.fog instanceof THREE.Fog)) {
      scene.fog = new THREE.Fog(fog.color, fog.near, fog.far);
    } else {
      scene.fog.color.set(fog.color);
      scene.fog.near = fog.near;
      scene.fog.far = fog.far;
    }
  });

  return null;
};

// ---------------------------------------------------------------------------
// Sky wrapper — adjusts based on mode + time
// ---------------------------------------------------------------------------

const SkyWrapper: FC<{ timeOfDay: TimeOfDay; mode: ViewMode }> = ({ timeOfDay, mode }) => {
  const sun = sunFromTimeOfDay(timeOfDay);
  const isNight = timeOfDay < 0.2 || timeOfDay > 0.85;

  return (
    <>
      {mode === 'before' ? (
        // Overcast grey dome
        <mesh>
          <sphereGeometry args={[200, 32, 32]} />
          <meshBasicMaterial color="#8a8a8a" side={THREE.BackSide} />
        </mesh>
      ) : (
        <>
          <Sky
            distance={450000}
            sunPosition={sun.direction}
            turbidity={sun.skyTurbidity}
            rayleigh={sun.skyRayleigh}
            mieCoefficient={0.005}
            mieDirectionalG={0.8}
          />
          {isNight && (
            <Stars
              radius={200}
              depth={60}
              count={4000}
              factor={4}
              saturation={0}
              fade
            />
          )}
        </>
      )}
    </>
  );
};

// ---------------------------------------------------------------------------
// PUBLIC: Main Environment component
// ---------------------------------------------------------------------------

const Environment: FC<EnvironmentProps> = ({
  mode,
  timeOfDay,
  parcelPolygon,
  parcelCenter,
  parcelWidth = 100,
  parcelDepth = 80,
  showPeople = true,
}) => {
  const groundShape = useMemo(() => {
    if (parcelPolygon && parcelCenter) {
      return parcelFootprintToShape(parcelPolygon, parcelCenter);
    }
    return defaultParcelShape(parcelWidth, parcelDepth);
  }, [parcelPolygon, parcelCenter, parcelWidth, parcelDepth]);

  return (
    <>
      {/* Fog */}
      <FogController mode={mode} />

      {/* Sky */}
      <SkyWrapper timeOfDay={timeOfDay} mode={mode} />

      {/* Clouds */}
      <AnimatedClouds mode={mode} />

      {/* Lighting */}
      <SunLight timeOfDay={timeOfDay} mode={mode} />

      {/* Extended ground plane */}
      <ExtendedGround mode={mode} />

      {/* Parcel ground */}
      <GroundPlane shape={groundShape} mode={mode} />

      {/* Before-mode dressing */}
      {mode === 'before' && (
        <BlightDressing parcelWidth={parcelWidth} parcelDepth={parcelDepth} />
      )}

      {/* People in after mode */}
      {mode === 'after' && showPeople && (
        <PeopleScatter parcelWidth={parcelWidth} parcelDepth={parcelDepth} />
      )}
    </>
  );
};

export default Environment;
