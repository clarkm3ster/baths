import { useRef, useMemo } from 'react';
import { useFrame } from '@react-three/fiber';
import * as THREE from 'three';

// ---------- Sound sculptures ----------

function BellSculpture({
  position,
}: {
  position: [number, number, number];
}) {
  const ref = useRef<THREE.Mesh>(null);

  useFrame(({ clock }) => {
    if (!ref.current) return;
    const t = clock.getElapsedTime();
    ref.current.rotation.y = Math.sin(t * 0.3 + position[0]) * 0.05;
  });

  return (
    <group position={position}>
      {/* Support pole */}
      <mesh position={[0, 1.5, 0]} castShadow>
        <cylinderGeometry args={[0.06, 0.08, 3, 8]} />
        <meshStandardMaterial color="#8B7355" metalness={0.6} roughness={0.4} />
      </mesh>
      {/* Cross bar */}
      <mesh position={[0, 3, 0]} castShadow>
        <cylinderGeometry args={[0.04, 0.04, 1.2, 8]} />
        <meshStandardMaterial color="#8B7355" metalness={0.6} roughness={0.4} />
      </mesh>
      {/* Bell (inverted cone) */}
      <mesh ref={ref} position={[0, 2.4, 0]} rotation={[Math.PI, 0, 0]} castShadow>
        <coneGeometry args={[0.5, 0.8, 12]} />
        <meshStandardMaterial
          color="#b8860b"
          metalness={0.8}
          roughness={0.2}
        />
      </mesh>
    </group>
  );
}

function WindHarp({
  position,
}: {
  position: [number, number, number];
}) {
  return (
    <group position={position}>
      {/* Tall cylinder frame */}
      <mesh position={[0, 2, 0]} castShadow>
        <cylinderGeometry args={[0.08, 0.1, 4, 8]} />
        <meshStandardMaterial color="#b8860b" metalness={0.7} roughness={0.3} />
      </mesh>
      {/* Strings */}
      {[-0.15, -0.05, 0.05, 0.15].map((offset, i) => (
        <mesh key={i} position={[offset, 2, 0]} castShadow>
          <cylinderGeometry args={[0.005, 0.005, 3.5, 4]} />
          <meshStandardMaterial
            color="#ddd"
            metalness={0.9}
            roughness={0.1}
          />
        </mesh>
      ))}
      {/* Top cap */}
      <mesh position={[0, 4, 0]} castShadow>
        <sphereGeometry args={[0.15, 8, 8]} />
        <meshStandardMaterial color="#b8860b" metalness={0.7} roughness={0.3} />
      </mesh>
    </group>
  );
}

function PercussionStone({
  position,
  scale = 1,
}: {
  position: [number, number, number];
  scale?: number;
}) {
  return (
    <mesh position={position} castShadow receiveShadow>
      <sphereGeometry args={[0.5 * scale, 12, 8]} />
      <meshStandardMaterial
        color="#8a8a7a"
        roughness={0.85}
        metalness={0.1}
      />
    </mesh>
  );
}

// ---------- Whisper dish ----------

function WhisperDish({
  position,
}: {
  position: [number, number, number];
}) {
  const geometry = useMemo(() => {
    const geo = new THREE.SphereGeometry(1.5, 24, 16, 0, Math.PI * 2, 0, Math.PI / 3);
    return geo;
  }, []);

  return (
    <group position={position}>
      {/* Support pole */}
      <mesh position={[0, 1, 0]} castShadow>
        <cylinderGeometry args={[0.1, 0.15, 2, 8]} />
        <meshStandardMaterial color="#8B7355" metalness={0.5} roughness={0.5} />
      </mesh>
      {/* Parabolic dish */}
      <mesh
        geometry={geometry}
        position={[0, 2.2, 0]}
        rotation={[Math.PI, 0, 0]}
        castShadow
      >
        <meshStandardMaterial
          color="#b8860b"
          metalness={0.7}
          roughness={0.3}
          side={THREE.DoubleSide}
        />
      </mesh>
    </group>
  );
}

// ---------- Winding pathway ----------

function WindingPath() {
  const pathPoints = useMemo(() => {
    const points: THREE.Vector3[] = [];
    for (let i = 0; i <= 60; i++) {
      const t = (i / 60) * Math.PI * 2;
      const r = 6 + Math.sin(t * 3) * 2;
      points.push(new THREE.Vector3(Math.cos(t) * r, 0.02, Math.sin(t) * r));
    }
    return points;
  }, []);

  const geometry = useMemo(() => {
    const curve = new THREE.CatmullRomCurve3(pathPoints, true);
    const tubeGeo = new THREE.TubeGeometry(curve, 120, 0.6, 4, true);
    // Flatten to ground
    const positions = tubeGeo.attributes.position;
    for (let i = 0; i < positions.count; i++) {
      positions.setY(i, Math.max(positions.getY(i), 0.01));
    }
    positions.needsUpdate = true;
    return tubeGeo;
  }, [pathPoints]);

  return (
    <mesh geometry={geometry} receiveShadow>
      <meshStandardMaterial color="#c4a882" roughness={0.9} />
    </mesh>
  );
}

// ---------- Trees ----------

function ParkTree({
  position,
  height = 4,
  crownColor = '#3a7a3a',
}: {
  position: [number, number, number];
  height?: number;
  crownColor?: string;
}) {
  return (
    <group position={position}>
      {/* Trunk */}
      <mesh position={[0, height * 0.3, 0]} castShadow>
        <cylinderGeometry args={[0.1, 0.15, height * 0.6, 6]} />
        <meshStandardMaterial color="#5a3a20" roughness={0.9} />
      </mesh>
      {/* Crown - sphere */}
      <mesh position={[0, height * 0.7, 0]} castShadow>
        <sphereGeometry args={[height * 0.35, 10, 8]} />
        <meshStandardMaterial color={crownColor} roughness={0.8} />
      </mesh>
    </group>
  );
}

// ---------- Benches ----------

function ParkBench({
  position,
  rotation = 0,
}: {
  position: [number, number, number];
  rotation?: number;
}) {
  return (
    <group position={position} rotation={[0, rotation, 0]}>
      {/* Seat */}
      <mesh position={[0, 0.45, 0]} castShadow receiveShadow>
        <boxGeometry args={[1.5, 0.08, 0.45]} />
        <meshStandardMaterial color="#6b4a2a" roughness={0.85} />
      </mesh>
      {/* Legs */}
      {[-0.6, 0.6].map((x) => (
        <mesh key={x} position={[x, 0.22, 0]} castShadow>
          <boxGeometry args={[0.08, 0.44, 0.4]} />
          <meshStandardMaterial color="#555" roughness={0.7} />
        </mesh>
      ))}
      {/* Backrest */}
      <mesh position={[0, 0.75, -0.2]} castShadow>
        <boxGeometry args={[1.5, 0.5, 0.06]} />
        <meshStandardMaterial color="#6b4a2a" roughness={0.85} />
      </mesh>
    </group>
  );
}

// ---------- Morning dew sparkles ----------

function MorningDew({ count = 200 }: { count?: number }) {
  const meshRef = useRef<THREE.InstancedMesh>(null);
  const dummy = useMemo(() => new THREE.Object3D(), []);

  const particles = useMemo(() => {
    const arr: { x: number; z: number; phase: number }[] = [];
    for (let i = 0; i < count; i++) {
      arr.push({
        x: (Math.random() - 0.5) * 30,
        z: (Math.random() - 0.5) * 30,
        phase: Math.random() * Math.PI * 2,
      });
    }
    return arr;
  }, [count]);

  useFrame(({ clock }) => {
    if (!meshRef.current) return;
    const t = clock.getElapsedTime();
    particles.forEach((p, i) => {
      const sparkle = Math.sin(t * 2 + p.phase) * 0.5 + 0.5;
      const s = sparkle > 0.8 ? 0.04 : 0.015;
      dummy.position.set(p.x, 0.05, p.z);
      dummy.scale.setScalar(s);
      dummy.updateMatrix();
      meshRef.current!.setMatrixAt(i, dummy.matrix);
    });
    meshRef.current.instanceMatrix.needsUpdate = true;
  });

  return (
    <instancedMesh ref={meshRef} args={[undefined, undefined, count]}>
      <sphereGeometry args={[1, 4, 4]} />
      <meshBasicMaterial color="#ffffff" />
    </instancedMesh>
  );
}

// ---------- Morning sky ----------

function MorningSky() {
  const gradientMap = useMemo(() => {
    const canvas = document.createElement('canvas');
    canvas.width = 1;
    canvas.height = 256;
    const ctx = canvas.getContext('2d')!;
    const gradient = ctx.createLinearGradient(0, 0, 0, 256);
    gradient.addColorStop(0, '#4a6a8a');
    gradient.addColorStop(0.3, '#6a8aaa');
    gradient.addColorStop(0.5, '#8aaacc');
    gradient.addColorStop(0.7, '#ccccaa');
    gradient.addColorStop(0.85, '#eeddaa');
    gradient.addColorStop(1.0, '#ffeecc');
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

export default function SoundGardenWorld() {
  return (
    <>
      {/* Atmosphere */}
      <fog attach="fog" args={['#aabb99', 30, 100]} />
      <ambientLight intensity={0.35} color="#ffffdd" />
      <directionalLight
        position={[20, 25, 15]}
        intensity={1.0}
        color="#ffeecc"
        castShadow
        shadow-mapSize-width={1024}
        shadow-mapSize-height={1024}
        shadow-camera-left={-20}
        shadow-camera-right={20}
        shadow-camera-top={20}
        shadow-camera-bottom={-20}
      />
      {/* Warm fill from behind */}
      <directionalLight
        position={[-10, 8, -15]}
        intensity={0.3}
        color="#ffddaa"
      />

      <MorningSky />

      {/* Grass ground */}
      <mesh
        rotation={[-Math.PI / 2, 0, 0]}
        position={[0, 0, 0]}
        receiveShadow
      >
        <planeGeometry args={[80, 80]} />
        <meshStandardMaterial color="#4a6a3a" roughness={0.95} />
      </mesh>

      {/* Sound sculptures */}
      <BellSculpture position={[-4, 0, -3]} />
      <BellSculpture position={[5, 0, -5]} />
      <WindHarp position={[-6, 0, 4]} />
      <WindHarp position={[7, 0, 2]} />
      <WindHarp position={[0, 0, -8]} />
      <PercussionStone position={[-2, 0.3, 2]} scale={1.2} />
      <PercussionStone position={[3, 0.25, 5]} scale={0.9} />
      <PercussionStone position={[-1, 0.35, 6]} scale={1.0} />
      <PercussionStone position={[1, 0.2, 3]} scale={0.7} />

      {/* Whisper dishes */}
      <WhisperDish position={[-8, 0, -6]} />
      <WhisperDish position={[9, 0, 7]} />

      <WindingPath />

      {/* Trees */}
      <ParkTree position={[-10, 0, -8]} height={5} crownColor="#3a7a3a" />
      <ParkTree position={[10, 0, -10]} height={6} crownColor="#2d6b2d" />
      <ParkTree position={[-12, 0, 5]} height={4.5} crownColor="#4a8a4a" />
      <ParkTree position={[12, 0, 8]} height={5.5} crownColor="#3a7a3a" />
      <ParkTree position={[-7, 0, 10]} height={4} crownColor="#2d6b2d" />
      <ParkTree position={[5, 0, 12]} height={3.5} crownColor="#4a8a4a" />
      <ParkTree position={[0, 0, 14]} height={5} crownColor="#3a7a3a" />

      {/* Benches along paths */}
      <ParkBench position={[6, 0, 0]} rotation={Math.PI / 4} />
      <ParkBench position={[-6, 0, -1]} rotation={-Math.PI / 3} />
      <ParkBench position={[0, 0, 8]} rotation={0} />
      <ParkBench position={[-3, 0, -7]} rotation={Math.PI / 6} />

      <MorningDew count={200} />
    </>
  );
}
