import { useRef, useMemo } from 'react';
import { useFrame } from '@react-three/fiber';
import * as THREE from 'three';

// ---------- Perimeter walls ----------

function GardenWalls() {
  const wallHeight = 2;
  const halfSize = 18;

  return (
    <group>
      {/* North wall */}
      <mesh position={[0, wallHeight / 2, -halfSize]} castShadow receiveShadow>
        <boxGeometry args={[halfSize * 2 + 0.6, wallHeight, 0.6]} />
        <meshStandardMaterial color="#a09080" roughness={0.9} />
      </mesh>
      {/* South wall */}
      <mesh position={[0, wallHeight / 2, halfSize]} castShadow receiveShadow>
        <boxGeometry args={[halfSize * 2 + 0.6, wallHeight, 0.6]} />
        <meshStandardMaterial color="#a09080" roughness={0.9} />
      </mesh>
      {/* East wall */}
      <mesh position={[halfSize, wallHeight / 2, 0]} castShadow receiveShadow>
        <boxGeometry args={[0.6, wallHeight, halfSize * 2]} />
        <meshStandardMaterial color="#a09080" roughness={0.9} />
      </mesh>
      {/* West wall (with entrance gap) */}
      <mesh
        position={[-halfSize, wallHeight / 2, -halfSize / 2 - 1]}
        castShadow
        receiveShadow
      >
        <boxGeometry args={[0.6, wallHeight, halfSize - 2]} />
        <meshStandardMaterial color="#a09080" roughness={0.9} />
      </mesh>
      <mesh
        position={[-halfSize, wallHeight / 2, halfSize / 2 + 1]}
        castShadow
        receiveShadow
      >
        <boxGeometry args={[0.6, wallHeight, halfSize - 2]} />
        <meshStandardMaterial color="#a09080" roughness={0.9} />
      </mesh>
    </group>
  );
}

// ---------- Labyrinth path ----------

function LabyrinthPath() {
  const pathGeometry = useMemo(() => {
    const points: THREE.Vector3[] = [];
    // Create a spiral labyrinth pattern
    const rings = 5;
    for (let ring = rings; ring >= 1; ring--) {
      const radius = ring * 2.2;
      const startAngle = ring % 2 === 0 ? 0 : Math.PI;
      const endAngle = startAngle + Math.PI * 1.8;
      const segments = 30;
      for (let i = 0; i <= segments; i++) {
        const t = i / segments;
        const angle = startAngle + t * (endAngle - startAngle);
        points.push(
          new THREE.Vector3(Math.cos(angle) * radius, 0.03, Math.sin(angle) * radius)
        );
      }
      // Connect to next ring
      if (ring > 1) {
        const nextRadius = (ring - 1) * 2.2;
        const connectAngle = endAngle;
        for (let i = 0; i <= 5; i++) {
          const t = i / 5;
          const r = radius + t * (nextRadius - radius);
          points.push(
            new THREE.Vector3(
              Math.cos(connectAngle) * r,
              0.03,
              Math.sin(connectAngle) * r
            )
          );
        }
      }
    }

    const curve = new THREE.CatmullRomCurve3(points, false);
    const tubeGeo = new THREE.TubeGeometry(curve, 300, 0.4, 4, false);
    // Flatten to ground
    const positions = tubeGeo.attributes.position;
    for (let i = 0; i < positions.count; i++) {
      positions.setY(i, Math.max(positions.getY(i), 0.01) * 0.15 + 0.01);
    }
    positions.needsUpdate = true;
    return tubeGeo;
  }, []);

  return (
    <mesh geometry={pathGeometry} receiveShadow>
      <meshStandardMaterial color="#c4a882" roughness={0.92} />
    </mesh>
  );
}

// ---------- Central water feature ----------

function WaterFeature() {
  const ref = useRef<THREE.Mesh>(null);

  useFrame(({ clock }) => {
    if (!ref.current) return;
    const t = clock.getElapsedTime();
    // Gentle ripple effect via scale oscillation
    const scale = 1 + Math.sin(t * 1.5) * 0.002;
    ref.current.scale.set(scale, 1, scale);
    const mat = ref.current.material as THREE.MeshStandardMaterial;
    mat.emissiveIntensity = 0.08 + Math.sin(t * 0.8) * 0.03;
  });

  return (
    <group position={[0, 0, 0]}>
      {/* Pool basin */}
      <mesh position={[0, 0.15, 0]} castShadow receiveShadow>
        <cylinderGeometry args={[2.2, 2.4, 0.3, 24]} />
        <meshStandardMaterial color="#8a8878" roughness={0.8} />
      </mesh>
      {/* Water surface */}
      <mesh
        ref={ref}
        rotation={[-Math.PI / 2, 0, 0]}
        position={[0, 0.32, 0]}
      >
        <circleGeometry args={[2, 32]} />
        <meshStandardMaterial
          color="#4a7a8a"
          emissive="#4a7a8a"
          emissiveIntensity={0.08}
          roughness={0.05}
          metalness={0.4}
          transparent
          opacity={0.85}
        />
      </mesh>
      {/* Central fountain stone */}
      <mesh position={[0, 0.5, 0]} castShadow>
        <sphereGeometry args={[0.3, 12, 12]} />
        <meshStandardMaterial color="#7a7a6a" roughness={0.85} />
      </mesh>
    </group>
  );
}

// ---------- Meditation seating areas (stone circles) ----------

function MeditationCircle({
  position,
  radius = 2,
}: {
  position: [number, number, number];
  radius?: number;
}) {
  const stones = useMemo(() => {
    const arr: { angle: number; size: number }[] = [];
    const count = 6;
    for (let i = 0; i < count; i++) {
      arr.push({
        angle: (i / count) * Math.PI * 2,
        size: 0.25 + Math.random() * 0.15,
      });
    }
    return arr;
  }, []);

  return (
    <group position={position}>
      {stones.map((s, i) => (
        <mesh
          key={i}
          position={[
            Math.cos(s.angle) * radius,
            s.size * 0.8,
            Math.sin(s.angle) * radius,
          ]}
          castShadow
          receiveShadow
        >
          <sphereGeometry args={[s.size, 8, 6]} />
          <meshStandardMaterial color="#8a8a7a" roughness={0.9} />
        </mesh>
      ))}
    </group>
  );
}

// ---------- Gathering circle (ring of benches) ----------

function GatheringCircle() {
  const benchCount = 8;

  return (
    <group position={[8, 0, -8]}>
      {Array.from({ length: benchCount }).map((_, i) => {
        const angle = (i / benchCount) * Math.PI * 2;
        const x = Math.cos(angle) * 3.5;
        const z = Math.sin(angle) * 3.5;
        return (
          <group
            key={i}
            position={[x, 0, z]}
            rotation={[0, -angle + Math.PI / 2, 0]}
          >
            <mesh position={[0, 0.3, 0]} castShadow receiveShadow>
              <boxGeometry args={[1.2, 0.1, 0.4]} />
              <meshStandardMaterial color="#6b4a2a" roughness={0.85} />
            </mesh>
            {[-0.5, 0.5].map((lx) => (
              <mesh key={lx} position={[lx, 0.15, 0]} castShadow>
                <boxGeometry args={[0.08, 0.3, 0.4]} />
                <meshStandardMaterial color="#555" roughness={0.7} />
              </mesh>
            ))}
          </group>
        );
      })}
    </group>
  );
}

// ---------- Lush vegetation ----------

function GardenTree({
  position,
  height = 4,
  crownColor = '#2a6a2a',
  crownScale = 1,
}: {
  position: [number, number, number];
  height?: number;
  crownColor?: string;
  crownScale?: number;
}) {
  return (
    <group position={position}>
      <mesh position={[0, height * 0.3, 0]} castShadow>
        <cylinderGeometry args={[0.08, 0.12, height * 0.6, 6]} />
        <meshStandardMaterial color="#4a3020" roughness={0.9} />
      </mesh>
      <mesh position={[0, height * 0.7, 0]} castShadow>
        <sphereGeometry args={[height * 0.32 * crownScale, 10, 8]} />
        <meshStandardMaterial color={crownColor} roughness={0.82} />
      </mesh>
    </group>
  );
}

function Bush({
  position,
  size = 0.5,
  color = '#2a6a2a',
}: {
  position: [number, number, number];
  size?: number;
  color?: string;
}) {
  return (
    <mesh position={position} castShadow>
      <sphereGeometry args={[size, 8, 6]} />
      <meshStandardMaterial color={color} roughness={0.85} />
    </mesh>
  );
}

// ---------- Morning mist ----------

function MorningMist({ count = 30 }: { count?: number }) {
  const meshRef = useRef<THREE.InstancedMesh>(null);
  const dummy = useMemo(() => new THREE.Object3D(), []);

  const particles = useMemo(() => {
    const arr: { x: number; z: number; phase: number; size: number }[] = [];
    for (let i = 0; i < count; i++) {
      arr.push({
        x: (Math.random() - 0.5) * 30,
        z: (Math.random() - 0.5) * 30,
        phase: Math.random() * Math.PI * 2,
        size: 2 + Math.random() * 3,
      });
    }
    return arr;
  }, [count]);

  useFrame(({ clock }) => {
    if (!meshRef.current) return;
    const t = clock.getElapsedTime();
    particles.forEach((p, i) => {
      dummy.position.set(
        p.x + Math.sin(t * 0.1 + p.phase) * 2,
        0.5 + Math.sin(t * 0.15 + i) * 0.3,
        p.z + Math.cos(t * 0.08 + p.phase) * 2
      );
      dummy.scale.setScalar(p.size);
      dummy.updateMatrix();
      meshRef.current!.setMatrixAt(i, dummy.matrix);
    });
    meshRef.current.instanceMatrix.needsUpdate = true;
  });

  return (
    <instancedMesh ref={meshRef} args={[undefined, undefined, count]}>
      <sphereGeometry args={[1, 8, 6]} />
      <meshBasicMaterial color="#d8e0d0" transparent opacity={0.06} />
    </instancedMesh>
  );
}

// ---------- Musical note particles (birdsong) ----------

function BirdsongNotes({ count = 20 }: { count?: number }) {
  const meshRef = useRef<THREE.InstancedMesh>(null);
  const dummy = useMemo(() => new THREE.Object3D(), []);

  const particles = useMemo(() => {
    const arr: {
      x: number;
      y: number;
      z: number;
      speed: number;
      phase: number;
    }[] = [];
    for (let i = 0; i < count; i++) {
      arr.push({
        x: (Math.random() - 0.5) * 25,
        y: 2 + Math.random() * 5,
        z: (Math.random() - 0.5) * 25,
        speed: 0.2 + Math.random() * 0.4,
        phase: Math.random() * Math.PI * 2,
      });
    }
    return arr;
  }, [count]);

  useFrame(({ clock }) => {
    if (!meshRef.current) return;
    const t = clock.getElapsedTime();
    particles.forEach((p, i) => {
      const life = (Math.sin(t * p.speed + p.phase) + 1) / 2;
      const scale = life > 0.6 ? 0.06 : 0.02;
      dummy.position.set(
        p.x + Math.sin(t * 0.3 + p.phase) * 1.5,
        p.y + Math.sin(t * 0.5 + i) * 0.8,
        p.z + Math.cos(t * 0.3 + p.phase) * 1.5
      );
      dummy.scale.setScalar(scale);
      dummy.updateMatrix();
      meshRef.current!.setMatrixAt(i, dummy.matrix);
    });
    meshRef.current.instanceMatrix.needsUpdate = true;
  });

  return (
    <instancedMesh ref={meshRef} args={[undefined, undefined, count]}>
      <sphereGeometry args={[1, 4, 4]} />
      <meshBasicMaterial color="#ffeecc" transparent opacity={0.5} />
    </instancedMesh>
  );
}

// ---------- Peaceful morning sky ----------

function PeacefulSky() {
  const gradientMap = useMemo(() => {
    const canvas = document.createElement('canvas');
    canvas.width = 1;
    canvas.height = 256;
    const ctx = canvas.getContext('2d')!;
    const gradient = ctx.createLinearGradient(0, 0, 0, 256);
    gradient.addColorStop(0, '#7a9abb');
    gradient.addColorStop(0.3, '#9ab5cc');
    gradient.addColorStop(0.5, '#b8ccdd');
    gradient.addColorStop(0.7, '#d0ddee');
    gradient.addColorStop(0.85, '#e0e8ee');
    gradient.addColorStop(1.0, '#e8eef0');
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

export default function QuietGardenWorld() {
  return (
    <>
      {/* Atmosphere -- the most peaceful scene */}
      <fog attach="fog" args={['#d0ddd0', 10, 50]} />
      <ambientLight intensity={0.45} color="#eeeedd" />
      <directionalLight
        position={[15, 20, 10]}
        intensity={0.6}
        color="#ffeecc"
        castShadow
        shadow-mapSize-width={1024}
        shadow-mapSize-height={1024}
        shadow-camera-left={-25}
        shadow-camera-right={25}
        shadow-camera-top={25}
        shadow-camera-bottom={-25}
      />
      {/* Soft fill */}
      <directionalLight
        position={[-10, 8, -5]}
        intensity={0.2}
        color="#ccddee"
      />

      <PeacefulSky />

      {/* Lush grass ground */}
      <mesh
        rotation={[-Math.PI / 2, 0, 0]}
        position={[0, 0, 0]}
        receiveShadow
      >
        <planeGeometry args={[60, 60]} />
        <meshStandardMaterial color="#4a7a3a" roughness={0.95} />
      </mesh>

      <GardenWalls />
      <LabyrinthPath />
      <WaterFeature />

      {/* Meditation circles */}
      <MeditationCircle position={[-8, 0, -8]} radius={2} />
      <MeditationCircle position={[10, 0, 5]} radius={1.8} />

      <GatheringCircle />

      {/* Trees -- varied, lush */}
      <GardenTree position={[-12, 0, -12]} height={5} crownColor="#2a6a2a" crownScale={1.3} />
      <GardenTree position={[12, 0, -14]} height={6} crownColor="#1e5a1e" crownScale={1.2} />
      <GardenTree position={[-14, 0, 5]} height={4.5} crownColor="#3a7a3a" crownScale={1.1} />
      <GardenTree position={[14, 0, 10]} height={5.5} crownColor="#2a6a2a" crownScale={1.4} />
      <GardenTree position={[-10, 0, 14]} height={4} crownColor="#1e5a1e" crownScale={1.2} />
      <GardenTree position={[6, 0, 14]} height={5} crownColor="#3a7a3a" crownScale={1.3} />
      <GardenTree position={[-5, 0, -14]} height={4.5} crownColor="#2a6a2a" crownScale={1.0} />
      <GardenTree position={[15, 0, -5]} height={3.5} crownColor="#4a8a4a" crownScale={1.1} />
      <GardenTree position={[-15, 0, -2]} height={6} crownColor="#1e5a1e" crownScale={1.5} />
      <GardenTree position={[0, 0, -15]} height={5} crownColor="#2a6a2a" crownScale={1.2} />

      {/* Bushes -- dense perimeter planting */}
      <Bush position={[-16, 0.4, -10]} size={0.7} color="#2a6a2a" />
      <Bush position={[-16, 0.35, -6]} size={0.6} color="#3a7a3a" />
      <Bush position={[-16, 0.45, 2]} size={0.8} color="#1e5a1e" />
      <Bush position={[-16, 0.4, 8]} size={0.65} color="#2a6a2a" />
      <Bush position={[16, 0.5, -8]} size={0.7} color="#3a7a3a" />
      <Bush position={[16, 0.4, -3]} size={0.6} color="#2a6a2a" />
      <Bush position={[16, 0.55, 4]} size={0.8} color="#1e5a1e" />
      <Bush position={[16, 0.4, 12]} size={0.65} color="#3a7a3a" />
      <Bush position={[-5, 0.35, 16]} size={0.6} color="#2a6a2a" />
      <Bush position={[5, 0.4, 16]} size={0.7} color="#1e5a1e" />
      <Bush position={[-10, 0.4, -16]} size={0.6} color="#3a7a3a" />
      <Bush position={[8, 0.45, -16]} size={0.7} color="#2a6a2a" />

      {/* Inner garden bushes */}
      <Bush position={[-4, 0.3, 5]} size={0.45} color="#4a8a4a" />
      <Bush position={[5, 0.35, -4]} size={0.5} color="#3a7a3a" />
      <Bush position={[-6, 0.3, -3]} size={0.4} color="#2a6a2a" />
      <Bush position={[3, 0.35, 8]} size={0.5} color="#4a8a4a" />

      <MorningMist count={30} />
      <BirdsongNotes count={20} />
    </>
  );
}
