import { useRef, useMemo } from 'react';
import { useFrame } from '@react-three/fiber';
import * as THREE from 'three';

// ---------- Highway ceiling ----------

function HighwayCeiling() {
  return (
    <group>
      {/* Main ceiling slab */}
      <mesh position={[0, 12, 0]} receiveShadow>
        <boxGeometry args={[50, 1.5, 40]} />
        <meshStandardMaterial color="#3a3a3a" roughness={0.95} />
      </mesh>
      {/* Ceiling underside detail beams */}
      {Array.from({ length: 6 }).map((_, i) => (
        <mesh key={i} position={[0, 11.2, -15 + i * 6]}>
          <boxGeometry args={[50, 0.4, 0.6]} />
          <meshStandardMaterial color="#333" roughness={0.9} />
        </mesh>
      ))}
    </group>
  );
}

// ---------- Support columns ----------

function SupportColumns() {
  const columns = useMemo(
    () => [
      [-15, -12],
      [-15, 0],
      [-15, 12],
      [15, -12],
      [15, 0],
      [15, 12],
    ],
    []
  );

  return (
    <group>
      {columns.map(([x, z], i) => (
        <mesh key={i} position={[x, 6, z]} castShadow receiveShadow>
          <cylinderGeometry args={[0.6, 0.7, 12, 12]} />
          <meshStandardMaterial color="#4a4a4a" roughness={0.85} />
        </mesh>
      ))}
    </group>
  );
}

// ---------- Climbing walls ----------

function ClimbingWall({
  position,
  rotation = 0,
  width = 8,
  height = 10,
}: {
  position: [number, number, number];
  rotation?: number;
  width?: number;
  height?: number;
}) {
  const holds = useMemo(() => {
    const arr: { x: number; y: number; z: number; s: number; color: string }[] =
      [];
    const colors = ['#ff4444', '#44ff44', '#4444ff', '#ffff44', '#ff44ff', '#44ffff'];
    for (let i = 0; i < 40; i++) {
      arr.push({
        x: (Math.random() - 0.5) * (width - 1),
        y: Math.random() * (height - 1) + 0.5,
        z: 0.15,
        s: 0.08 + Math.random() * 0.1,
        color: colors[Math.floor(Math.random() * colors.length)],
      });
    }
    return arr;
  }, [width, height]);

  return (
    <group position={position} rotation={[0, rotation, 0]}>
      {/* Wall panel */}
      <mesh position={[0, height / 2, 0]} castShadow receiveShadow>
        <boxGeometry args={[width, height, 0.3]} />
        <meshStandardMaterial color="#5a5a5a" roughness={0.75} />
      </mesh>
      {/* Climbing holds */}
      {holds.map((h, i) => (
        <mesh key={i} position={[h.x, h.y, h.z]} castShadow>
          <sphereGeometry args={[h.s, 6, 6]} />
          <meshStandardMaterial
            color={h.color}
            roughness={0.6}
          />
        </mesh>
      ))}
    </group>
  );
}

// ---------- Rubber mat ground ----------

function RubberMatGround() {
  return (
    <mesh
      rotation={[-Math.PI / 2, 0, 0]}
      position={[0, 0, 0]}
      receiveShadow
    >
      <planeGeometry args={[50, 40]} />
      <meshStandardMaterial color="#8b3a1a" roughness={0.95} />
    </mesh>
  );
}

// ---------- LED spotlights ----------

function LEDSpotlights() {
  const lights = useMemo(
    () => [
      { pos: [-8, 11, -6] as [number, number, number], color: '#ff2244', target: [-8, 0, -6] as [number, number, number] },
      { pos: [0, 11, -8] as [number, number, number], color: '#2244ff', target: [0, 0, -8] as [number, number, number] },
      { pos: [8, 11, -4] as [number, number, number], color: '#22ff44', target: [8, 0, -4] as [number, number, number] },
      { pos: [-5, 11, 5] as [number, number, number], color: '#ff44ff', target: [-5, 0, 5] as [number, number, number] },
      { pos: [5, 11, 8] as [number, number, number], color: '#ffaa22', target: [5, 0, 8] as [number, number, number] },
      { pos: [0, 11, 0] as [number, number, number], color: '#44ddff', target: [0, 0, 0] as [number, number, number] },
    ],
    []
  );

  return (
    <group>
      {lights.map((l, i) => (
        <group key={i}>
          <spotLight
            position={l.pos}
            color={l.color}
            intensity={15}
            distance={15}
            angle={0.5}
            penumbra={0.6}
            castShadow
          />
          {/* Light fixture */}
          <mesh position={l.pos}>
            <cylinderGeometry args={[0.15, 0.2, 0.3, 8]} />
            <meshStandardMaterial
              color={l.color}
              emissive={l.color}
              emissiveIntensity={2}
            />
          </mesh>
        </group>
      ))}
    </group>
  );
}

// ---------- Youth silhouettes ----------

function YouthFigures() {
  const figures = useMemo(
    () => [
      { x: -3, z: -3, scale: 0.9, rot: 0.3 },
      { x: 2, z: 2, scale: 1.0, rot: -0.5 },
      { x: 6, z: -5, scale: 0.85, rot: 1.2 },
      { x: -7, z: 4, scale: 0.95, rot: -0.8 },
    ],
    []
  );

  return (
    <group>
      {figures.map((f, i) => (
        <group
          key={i}
          position={[f.x, 0, f.z]}
          rotation={[0, f.rot, 0]}
          scale={f.scale}
        >
          {/* Body */}
          <mesh position={[0, 1, 0]} castShadow>
            <capsuleGeometry args={[0.2, 0.8, 4, 8]} />
            <meshStandardMaterial color="#1a1a1a" roughness={0.9} />
          </mesh>
          {/* Head */}
          <mesh position={[0, 1.8, 0]} castShadow>
            <sphereGeometry args={[0.18, 8, 8]} />
            <meshStandardMaterial color="#1a1a1a" roughness={0.9} />
          </mesh>
          {/* Legs */}
          {[-0.1, 0.1].map((x) => (
            <mesh key={x} position={[x, 0.35, 0]} castShadow>
              <capsuleGeometry args={[0.08, 0.5, 4, 6]} />
              <meshStandardMaterial color="#1a1a1a" roughness={0.9} />
            </mesh>
          ))}
        </group>
      ))}
    </group>
  );
}

// ---------- Energy particles ----------

function EnergyParticles({ count = 60 }: { count?: number }) {
  const meshRef = useRef<THREE.InstancedMesh>(null);
  const dummy = useMemo(() => new THREE.Object3D(), []);

  const particles = useMemo(() => {
    const arr: { x: number; y: number; z: number; speed: number; phase: number }[] = [];
    for (let i = 0; i < count; i++) {
      arr.push({
        x: (Math.random() - 0.5) * 30,
        y: Math.random() * 10 + 1,
        z: (Math.random() - 0.5) * 25,
        speed: 1 + Math.random() * 3,
        phase: Math.random() * Math.PI * 2,
      });
    }
    return arr;
  }, [count]);

  useFrame(({ clock }) => {
    if (!meshRef.current) return;
    const t = clock.getElapsedTime();
    particles.forEach((p, i) => {
      dummy.position.set(
        p.x + Math.sin(t * p.speed * 0.3 + p.phase) * 2,
        p.y + Math.sin(t * p.speed * 0.5 + p.phase) * 1,
        p.z + Math.cos(t * p.speed * 0.3 + p.phase) * 2
      );
      dummy.scale.setScalar(0.03 + Math.sin(t * 2 + i) * 0.01);
      dummy.updateMatrix();
      meshRef.current!.setMatrixAt(i, dummy.matrix);
    });
    meshRef.current.instanceMatrix.needsUpdate = true;
  });

  return (
    <instancedMesh ref={meshRef} args={[undefined, undefined, count]}>
      <sphereGeometry args={[1, 4, 4]} />
      <meshBasicMaterial color="#ffffff" transparent opacity={0.6} />
    </instancedMesh>
  );
}

// ---------- Main world ----------

export default function UnderpassWorld() {
  return (
    <>
      {/* Atmosphere — dark, industrial */}
      <fog attach="fog" args={['#1a1a1a', 15, 60]} />
      <ambientLight intensity={0.08} color="#aaaacc" />

      {/* Background — dark void (no sky, just darkness under the highway) */}
      <mesh>
        <sphereGeometry args={[180, 16, 16]} />
        <meshBasicMaterial color="#0a0a0a" side={THREE.BackSide} />
      </mesh>

      <RubberMatGround />
      <HighwayCeiling />
      <SupportColumns />

      <ClimbingWall position={[-5, 0, -10]} width={8} height={10} />
      <ClimbingWall position={[5, 0, -10]} width={8} height={10} />

      <LEDSpotlights />
      <YouthFigures />
      <EnergyParticles count={60} />
    </>
  );
}
