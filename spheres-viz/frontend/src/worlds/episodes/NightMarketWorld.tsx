import { useRef, useMemo } from 'react';
import { useFrame } from '@react-three/fiber';
import * as THREE from 'three';

// ---------- Street buildings ----------

function StreetBuildings() {
  const buildings = useMemo(() => {
    const arr: {
      x: number;
      z: number;
      w: number;
      h: number;
      d: number;
      side: 'left' | 'right';
    }[] = [];
    for (let i = 0; i < 12; i++) {
      const z = -25 + i * 4.5;
      arr.push({
        x: -10,
        z,
        w: 5 + Math.random() * 3,
        h: 8 + Math.random() * 8,
        d: 3 + Math.random() * 2,
        side: 'left',
      });
      arr.push({
        x: 10,
        z,
        w: 5 + Math.random() * 3,
        h: 8 + Math.random() * 8,
        d: 3 + Math.random() * 2,
        side: 'right',
      });
    }
    return arr;
  }, []);

  return (
    <group>
      {buildings.map((b, i) => (
        <group key={i}>
          <mesh position={[b.x, b.h / 2, b.z]} castShadow>
            <boxGeometry args={[b.w, b.h, b.d]} />
            <meshStandardMaterial color="#2a2a30" roughness={0.85} />
          </mesh>
          {/* Lit windows */}
          {Array.from({ length: Math.floor(b.h / 2) }).map((_, j) =>
            Array.from({ length: 2 }).map((_, k) => (
              <mesh
                key={`${j}-${k}`}
                position={[
                  b.x + (b.side === 'left' ? b.w / 2 + 0.01 : -b.w / 2 - 0.01),
                  1.5 + j * 2,
                  b.z - 0.5 + k * 1,
                ]}
                rotation={[0, b.side === 'left' ? 0 : Math.PI, 0]}
              >
                <planeGeometry args={[0.5, 0.7]} />
                <meshStandardMaterial
                  color="#ffdd88"
                  emissive="#ffdd88"
                  emissiveIntensity={Math.random() > 0.4 ? 0.8 : 0.1}
                />
              </mesh>
            ))
          )}
        </group>
      ))}
    </group>
  );
}

// ---------- Vendor stalls ----------

function VendorStalls() {
  const stalls = useMemo(() => {
    const arr: {
      x: number;
      z: number;
      color: string;
      canopyColor: string;
      side: 'left' | 'right';
    }[] = [];
    const colors = [
      '#cc3333',
      '#cc6633',
      '#cccc33',
      '#33cc33',
      '#3333cc',
      '#cc33cc',
      '#33cccc',
      '#cc6666',
    ];
    for (let i = 0; i < 30; i++) {
      const side = i % 2 === 0 ? 'left' : 'right';
      arr.push({
        x: side === 'left' ? -5.5 : 5.5,
        z: -28 + i * 1.9,
        color: colors[i % colors.length],
        canopyColor: colors[(i + 3) % colors.length],
        side,
      });
    }
    return arr;
  }, []);

  return (
    <group>
      {stalls.map((s, i) => (
        <group key={i} position={[s.x, 0, s.z]}>
          {/* Booth base */}
          <mesh position={[0, 0.5, 0]} castShadow receiveShadow>
            <boxGeometry args={[1.5, 1, 1.2]} />
            <meshStandardMaterial color="#5a4a3a" roughness={0.85} />
          </mesh>
          {/* Counter top */}
          <mesh position={[0, 1.02, 0]} castShadow>
            <boxGeometry args={[1.6, 0.06, 1.3]} />
            <meshStandardMaterial color="#7a6a5a" roughness={0.8} />
          </mesh>
          {/* Canopy support poles */}
          {[-0.7, 0.7].map((x) => (
            <mesh key={x} position={[x, 1.5, 0]} castShadow>
              <cylinderGeometry args={[0.03, 0.03, 2, 6]} />
              <meshStandardMaterial color="#888" roughness={0.5} />
            </mesh>
          ))}
          {/* Canopy */}
          <mesh position={[0, 2.5, 0]} castShadow>
            <boxGeometry args={[1.8, 0.05, 1.5]} />
            <meshStandardMaterial
              color={s.canopyColor}
              roughness={0.7}
            />
          </mesh>
          {/* Warm light underneath */}
          <pointLight
            position={[0, 2, 0]}
            color="#ffcc88"
            intensity={1.5}
            distance={4}
          />
        </group>
      ))}
    </group>
  );
}

// ---------- String lights ----------

function StringLights() {
  const lightSets = useMemo(() => {
    const sets: { z: number; count: number }[] = [];
    for (let i = 0; i < 12; i++) {
      sets.push({ z: -25 + i * 4.5, count: 8 });
    }
    return sets;
  }, []);

  return (
    <group>
      {lightSets.map((set, si) => (
        <group key={si}>
          {/* Wire (catenary approximation) */}
          {Array.from({ length: set.count }).map((_, i) => {
            const t = i / (set.count - 1);
            const x = -6 + t * 12;
            // catenary sag
            const sag = 4 * t * (1 - t) * 1.2;
            const y = 6 - sag;
            return (
              <group key={i}>
                <mesh position={[x, y, set.z]}>
                  <sphereGeometry args={[0.06, 6, 6]} />
                  <meshStandardMaterial
                    color="#ffeeaa"
                    emissive="#ffeeaa"
                    emissiveIntensity={3}
                  />
                </mesh>
                <pointLight
                  position={[x, y, set.z]}
                  color="#ffeeaa"
                  intensity={0.5}
                  distance={3}
                />
              </group>
            );
          })}
        </group>
      ))}
    </group>
  );
}

// ---------- Steam particles ----------

function SteamParticles({ count = 50 }: { count?: number }) {
  const meshRef = useRef<THREE.InstancedMesh>(null);
  const dummy = useMemo(() => new THREE.Object3D(), []);

  const particles = useMemo(() => {
    const arr: {
      x: number;
      z: number;
      speed: number;
      phase: number;
    }[] = [];
    for (let i = 0; i < count; i++) {
      const side = Math.random() > 0.5 ? -5.5 : 5.5;
      arr.push({
        x: side + (Math.random() - 0.5) * 1.5,
        z: -28 + Math.random() * 56,
        speed: 0.3 + Math.random() * 0.5,
        phase: Math.random() * Math.PI * 2,
      });
    }
    return arr;
  }, [count]);

  useFrame(({ clock }) => {
    if (!meshRef.current) return;
    const t = clock.getElapsedTime();
    particles.forEach((p, i) => {
      const life = ((t * p.speed + p.phase) % 3) / 3;
      const y = 1.5 + life * 3;
      const opacity = life < 0.3 ? life / 0.3 : life > 0.7 ? (1 - life) / 0.3 : 1;
      const s = 0.1 + life * 0.3;
      dummy.position.set(
        p.x + Math.sin(t + i) * 0.2,
        y,
        p.z
      );
      dummy.scale.setScalar(s * opacity);
      dummy.updateMatrix();
      meshRef.current!.setMatrixAt(i, dummy.matrix);
    });
    meshRef.current.instanceMatrix.needsUpdate = true;
  });

  return (
    <instancedMesh ref={meshRef} args={[undefined, undefined, count]}>
      <sphereGeometry args={[1, 6, 6]} />
      <meshBasicMaterial color="#cccccc" transparent opacity={0.15} />
    </instancedMesh>
  );
}

// ---------- Music stage ----------

function MusicStage() {
  return (
    <group position={[0, 0, 28]}>
      {/* Platform */}
      <mesh position={[0, 0.4, 0]} castShadow receiveShadow>
        <boxGeometry args={[8, 0.8, 5]} />
        <meshStandardMaterial color="#2a2a2a" roughness={0.6} />
      </mesh>
      {/* Backdrop */}
      <mesh position={[0, 3.5, -2.2]} castShadow>
        <boxGeometry args={[7, 6, 0.2]} />
        <meshStandardMaterial color="#1a1a1a" roughness={0.7} />
      </mesh>
      {/* Stage lights */}
      <spotLight
        position={[-3, 6, 2]}
        color="#ff4488"
        intensity={15}
        distance={15}
        angle={0.6}
        penumbra={0.7}
        castShadow
      />
      <spotLight
        position={[3, 6, 2]}
        color="#4488ff"
        intensity={15}
        distance={15}
        angle={0.6}
        penumbra={0.7}
        castShadow
      />
      <spotLight
        position={[0, 7, 0]}
        color="#ffcc44"
        intensity={10}
        distance={12}
        angle={0.4}
        penumbra={0.5}
      />
    </group>
  );
}

// ---------- People silhouettes ----------

function PeopleSilhouettes() {
  const people = useMemo(() => {
    const arr: { x: number; z: number; scale: number; rot: number }[] = [];
    for (let i = 0; i < 20; i++) {
      arr.push({
        x: (Math.random() - 0.5) * 8,
        z: -20 + Math.random() * 45,
        scale: 0.7 + Math.random() * 0.4,
        rot: Math.random() * Math.PI * 2,
      });
    }
    return arr;
  }, []);

  return (
    <group>
      {people.map((p, i) => (
        <group
          key={i}
          position={[p.x, 0, p.z]}
          rotation={[0, p.rot, 0]}
          scale={p.scale}
        >
          <mesh position={[0, 0.9, 0]} castShadow>
            <capsuleGeometry args={[0.18, 0.7, 4, 8]} />
            <meshStandardMaterial color="#1a1a1a" roughness={0.9} />
          </mesh>
          <mesh position={[0, 1.6, 0]} castShadow>
            <sphereGeometry args={[0.15, 6, 6]} />
            <meshStandardMaterial color="#1a1a1a" roughness={0.9} />
          </mesh>
        </group>
      ))}
    </group>
  );
}

// ---------- Night sky ----------

function NightSky() {
  const gradientMap = useMemo(() => {
    const canvas = document.createElement('canvas');
    canvas.width = 1;
    canvas.height = 256;
    const ctx = canvas.getContext('2d')!;
    const gradient = ctx.createLinearGradient(0, 0, 0, 256);
    gradient.addColorStop(0, '#0a0a1a');
    gradient.addColorStop(0.5, '#1a1a2a');
    gradient.addColorStop(0.8, '#2a2030');
    gradient.addColorStop(1.0, '#3a2a30');
    ctx.fillStyle = gradient;
    ctx.fillRect(0, 0, 1, 256);
    return new THREE.CanvasTexture(canvas);
  }, []);

  return (
    <mesh>
      <sphereGeometry args={[180, 32, 32]} />
      <meshBasicMaterial map={gradientMap} side={THREE.BackSide} />
    </mesh>
  );
}

// ---------- Main world ----------

export default function NightMarketWorld() {
  return (
    <>
      {/* Atmosphere */}
      <fog attach="fog" args={['#1a1a2a', 20, 80]} />
      <ambientLight intensity={0.1} color="#ffddcc" />

      <NightSky />

      {/* Street ground */}
      <mesh
        rotation={[-Math.PI / 2, 0, 0]}
        position={[0, 0, 0]}
        receiveShadow
      >
        <planeGeometry args={[20, 70]} />
        <meshStandardMaterial color="#2a2a2a" roughness={0.8} />
      </mesh>
      {/* Sidewalks */}
      <mesh
        rotation={[-Math.PI / 2, 0, 0]}
        position={[-8, 0.1, 0]}
        receiveShadow
      >
        <planeGeometry args={[4, 70]} />
        <meshStandardMaterial color="#444" roughness={0.85} />
      </mesh>
      <mesh
        rotation={[-Math.PI / 2, 0, 0]}
        position={[8, 0.1, 0]}
        receiveShadow
      >
        <planeGeometry args={[4, 70]} />
        <meshStandardMaterial color="#444" roughness={0.85} />
      </mesh>

      <StreetBuildings />
      <VendorStalls />
      <StringLights />
      <SteamParticles count={50} />
      <MusicStage />
      <PeopleSilhouettes />
    </>
  );
}
