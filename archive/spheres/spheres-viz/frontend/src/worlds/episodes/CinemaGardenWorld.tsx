import { useRef, useMemo } from 'react';
import { useFrame } from '@react-three/fiber';
import * as THREE from 'three';

// ---------- Garden beds ----------

function GardenBeds() {
  const beds = useMemo(
    () => [
      { x: -8, z: -4, w: 4, d: 2 },
      { x: -8, z: 2, w: 3, d: 2.5 },
      { x: 8, z: -3, w: 3.5, d: 2 },
      { x: 8, z: 3, w: 4, d: 1.8 },
      { x: -3, z: 8, w: 5, d: 2 },
      { x: 5, z: 8, w: 3, d: 2.5 },
    ],
    []
  );

  return (
    <group>
      {beds.map((b, i) => (
        <group key={i} position={[b.x, 0, b.z]}>
          {/* Raised bed frame */}
          <mesh position={[0, 0.25, 0]} castShadow receiveShadow>
            <boxGeometry args={[b.w, 0.5, b.d]} />
            <meshStandardMaterial color="#5a3a1e" roughness={0.9} />
          </mesh>
          {/* Soil/greenery top */}
          <mesh position={[0, 0.52, 0]} receiveShadow>
            <boxGeometry args={[b.w - 0.2, 0.06, b.d - 0.2]} />
            <meshStandardMaterial color="#2a5a2a" roughness={0.95} />
          </mesh>
          {/* Small plants */}
          {Array.from({ length: 3 }).map((_, j) => (
            <mesh
              key={j}
              position={[
                (j - 1) * (b.w / 3),
                0.8,
                (Math.random() - 0.5) * (b.d - 0.8),
              ]}
              castShadow
            >
              <sphereGeometry args={[0.25 + Math.random() * 0.15, 8, 6]} />
              <meshStandardMaterial
                color={['#2d6b2d', '#3a7a3a', '#1e5a1e'][j]}
                roughness={0.85}
              />
            </mesh>
          ))}
        </group>
      ))}
    </group>
  );
}

// ---------- Screening wall ----------

function ScreeningWall() {
  return (
    <group position={[0, 0, -10]}>
      {/* Wall structure */}
      <mesh position={[0, 3.5, 0]} castShadow receiveShadow>
        <boxGeometry args={[12, 7, 0.4]} />
        <meshStandardMaterial color="#e8e0d8" roughness={0.3} />
      </mesh>
      {/* Screen surface (emissive — as if projecting) */}
      <mesh position={[0, 3.5, 0.22]}>
        <planeGeometry args={[10, 5.5]} />
        <meshStandardMaterial
          color="#d0c8c0"
          emissive="#eee8dd"
          emissiveIntensity={0.4}
          roughness={0.2}
        />
      </mesh>
      {/* Support posts */}
      {[-6.5, 6.5].map((x) => (
        <mesh key={x} position={[x, 2, 0]} castShadow>
          <cylinderGeometry args={[0.15, 0.15, 7, 8]} />
          <meshStandardMaterial color="#555" roughness={0.7} />
        </mesh>
      ))}
    </group>
  );
}

// ---------- Seating ----------

function Seating() {
  const rows = useMemo(() => {
    const arr: { x: number; z: number; type: 'bench' | 'blanket' }[] = [];
    for (let row = 0; row < 4; row++) {
      for (let col = -2; col <= 2; col++) {
        arr.push({
          x: col * 2.5,
          z: -4 + row * 2.5,
          type: row < 2 ? 'blanket' : 'bench',
        });
      }
    }
    return arr;
  }, []);

  return (
    <group>
      {rows.map((s, i) =>
        s.type === 'blanket' ? (
          <mesh
            key={i}
            position={[s.x, 0.02, s.z]}
            rotation={[-Math.PI / 2, 0, Math.random() * 0.2 - 0.1]}
            receiveShadow
          >
            <planeGeometry args={[1.8, 1.4]} />
            <meshStandardMaterial
              color={['#884422', '#996633', '#aa7744'][i % 3]}
              roughness={0.95}
            />
          </mesh>
        ) : (
          <mesh key={i} position={[s.x, 0.25, s.z]} castShadow receiveShadow>
            <boxGeometry args={[1.8, 0.15, 0.5]} />
            <meshStandardMaterial color="#6b4a2a" roughness={0.85} />
          </mesh>
        )
      )}
    </group>
  );
}

// ---------- Projector beam ----------

function ProjectorBeam() {
  return (
    <group position={[0, 5, 8]} rotation={[-0.45, 0, 0]}>
      <mesh>
        <coneGeometry args={[3.5, 18, 16, 1, true]} />
        <meshBasicMaterial
          color="#fffde8"
          transparent
          opacity={0.04}
          side={THREE.DoubleSide}
        />
      </mesh>
    </group>
  );
}

// ---------- Fireflies ----------

function Fireflies({ count = 60 }: { count?: number }) {
  const meshRef = useRef<THREE.InstancedMesh>(null);
  const dummy = useMemo(() => new THREE.Object3D(), []);

  const particles = useMemo(() => {
    const arr: {
      x: number;
      y: number;
      z: number;
      speed: number;
      phase: number;
      radius: number;
    }[] = [];
    for (let i = 0; i < count; i++) {
      arr.push({
        x: (Math.random() - 0.5) * 30,
        y: 0.5 + Math.random() * 4,
        z: (Math.random() - 0.5) * 30,
        speed: 0.3 + Math.random() * 0.6,
        phase: Math.random() * Math.PI * 2,
        radius: 0.5 + Math.random() * 2,
      });
    }
    return arr;
  }, [count]);

  useFrame(({ clock }) => {
    if (!meshRef.current) return;
    const t = clock.getElapsedTime();
    particles.forEach((p, i) => {
      const blink = Math.sin(t * p.speed * 3 + p.phase) * 0.5 + 0.5;
      const scale = blink > 0.7 ? 0.06 : 0.02;
      dummy.position.set(
        p.x + Math.sin(t * p.speed + p.phase) * p.radius,
        p.y + Math.sin(t * p.speed * 0.7 + p.phase) * 0.5,
        p.z + Math.cos(t * p.speed + p.phase) * p.radius
      );
      dummy.scale.setScalar(scale);
      dummy.updateMatrix();
      meshRef.current!.setMatrixAt(i, dummy.matrix);
    });
    meshRef.current.instanceMatrix.needsUpdate = true;
  });

  return (
    <instancedMesh ref={meshRef} args={[undefined, undefined, count]}>
      <sphereGeometry args={[1, 6, 6]} />
      <meshBasicMaterial color="#ffee44" />
    </instancedMesh>
  );
}

// ---------- Simple trees ----------

function SimpleTree({
  position,
  height = 3,
  color = '#2d6b2d',
}: {
  position: [number, number, number];
  height?: number;
  color?: string;
}) {
  return (
    <group position={position}>
      <mesh position={[0, height * 0.3, 0]} castShadow>
        <cylinderGeometry args={[0.08, 0.12, height * 0.6, 6]} />
        <meshStandardMaterial color="#5a3a20" roughness={0.9} />
      </mesh>
      <mesh position={[0, height * 0.7, 0]} castShadow>
        <coneGeometry args={[height * 0.35, height * 0.6, 8]} />
        <meshStandardMaterial color={color} roughness={0.8} />
      </mesh>
    </group>
  );
}

// ---------- Dusk sky ----------

function DuskSky() {
  const gradientMap = useMemo(() => {
    const canvas = document.createElement('canvas');
    canvas.width = 1;
    canvas.height = 256;
    const ctx = canvas.getContext('2d')!;
    const gradient = ctx.createLinearGradient(0, 0, 0, 256);
    gradient.addColorStop(0, '#1a1a2e');
    gradient.addColorStop(0.3, '#2a2040');
    gradient.addColorStop(0.55, '#5a3050');
    gradient.addColorStop(0.75, '#8a4a40');
    gradient.addColorStop(0.9, '#cc7744');
    gradient.addColorStop(1.0, '#ee9944');
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

export default function CinemaGardenWorld() {
  return (
    <>
      {/* Atmosphere */}
      <fog attach="fog" args={['#2a2040', 30, 100]} />
      <ambientLight intensity={0.2} color="#ccaadd" />
      <directionalLight
        position={[-15, 12, 10]}
        intensity={0.6}
        color="#ffcc88"
        castShadow
        shadow-mapSize-width={1024}
        shadow-mapSize-height={1024}
      />

      <DuskSky />

      {/* Ground */}
      <mesh
        rotation={[-Math.PI / 2, 0, 0]}
        position={[0, 0, 0]}
        receiveShadow
      >
        <planeGeometry args={[80, 80]} />
        <meshStandardMaterial color="#2a4a2a" roughness={0.95} />
      </mesh>

      <ScreeningWall />
      <Seating />
      <GardenBeds />
      <ProjectorBeam />
      <Fireflies count={60} />

      {/* Scattered trees */}
      <SimpleTree position={[-12, 0, -6]} height={4} color="#2d6b2d" />
      <SimpleTree position={[12, 0, -8]} height={3.5} color="#1e5a1e" />
      <SimpleTree position={[-14, 0, 5]} height={5} color="#3a7a3a" />
      <SimpleTree position={[14, 0, 6]} height={4.5} color="#2d6b2d" />
      <SimpleTree position={[-10, 0, 10]} height={3} color="#1e5a1e" />
      <SimpleTree position={[10, 0, 10]} height={3.8} color="#3a7a3a" />

      {/* Sphere bushes near beds */}
      {[
        [-6, 0.4, -2],
        [6, 0.35, 1],
        [-5, 0.3, 6],
        [7, 0.45, 7],
      ].map((pos, i) => (
        <mesh
          key={i}
          position={pos as [number, number, number]}
          castShadow
        >
          <sphereGeometry args={[0.5 + Math.random() * 0.3, 8, 6]} />
          <meshStandardMaterial
            color={['#2d6b2d', '#3a7a3a', '#1e5a1e', '#2d6b2d'][i]}
            roughness={0.85}
          />
        </mesh>
      ))}
    </>
  );
}
