import { useRef, useMemo } from 'react';
import { useFrame } from '@react-three/fiber';
import * as THREE from 'three';

// ---------- City Hall facade ----------

function CityHallFacade() {
  return (
    <group position={[0, 0, -25]}>
      {/* Main building mass */}
      <mesh position={[0, 12, 0]} castShadow>
        <boxGeometry args={[30, 24, 10]} />
        <meshStandardMaterial color="#d4c9b8" roughness={0.7} />
      </mesh>
      {/* Tower */}
      <mesh position={[0, 30, 0]} castShadow>
        <boxGeometry args={[8, 16, 8]} />
        <meshStandardMaterial color="#c8bba8" roughness={0.65} />
      </mesh>
      {/* Tower top */}
      <mesh position={[0, 40, 0]} castShadow>
        <coneGeometry args={[4, 6, 8]} />
        <meshStandardMaterial color="#b8a898" roughness={0.6} />
      </mesh>
      {/* Columns */}
      {Array.from({ length: 8 }).map((_, i) => (
        <mesh
          key={i}
          position={[-10.5 + i * 3, 5, 5.2]}
          castShadow
        >
          <cylinderGeometry args={[0.4, 0.5, 10, 8]} />
          <meshStandardMaterial color="#d8ccbb" roughness={0.6} />
        </mesh>
      ))}
      {/* Warm lit windows */}
      {Array.from({ length: 6 }).map((_, row) =>
        Array.from({ length: 10 }).map((_, col) => (
          <mesh
            key={`${row}-${col}`}
            position={[-12 + col * 2.8, 4 + row * 3.2, 5.05]}
          >
            <planeGeometry args={[1, 1.6]} />
            <meshStandardMaterial
              color="#ffdd88"
              emissive="#ffdd88"
              emissiveIntensity={0.6}
            />
          </mesh>
        ))
      )}
    </group>
  );
}

// ---------- Ice skating rink ----------

function IceRink() {
  const ref = useRef<THREE.Mesh>(null);

  useFrame(({ clock }) => {
    if (!ref.current) return;
    const mat = ref.current.material as THREE.MeshStandardMaterial;
    mat.emissiveIntensity = 0.05 + Math.sin(clock.getElapsedTime() * 0.5) * 0.02;
  });

  return (
    <group position={[0, 0, 0]}>
      {/* Rink surface */}
      <mesh
        ref={ref}
        rotation={[-Math.PI / 2, 0, 0]}
        position={[0, 0.02, 0]}
        receiveShadow
      >
        <planeGeometry args={[18, 12]} />
        <meshStandardMaterial
          color="#b8d8f0"
          emissive="#88bbdd"
          emissiveIntensity={0.05}
          roughness={0.05}
          metalness={0.3}
        />
      </mesh>
      {/* Rink border */}
      {[
        [0, 0.3, -6, 18.4, 0.6, 0.3],
        [0, 0.3, 6, 18.4, 0.6, 0.3],
        [-9, 0.3, 0, 0.3, 0.6, 12],
        [9, 0.3, 0, 0.3, 0.6, 12],
      ].map(([x, y, z, w, h, d], i) => (
        <mesh key={i} position={[x, y, z]} castShadow>
          <boxGeometry args={[w, h, d]} />
          <meshStandardMaterial color="#ffffff" roughness={0.6} />
        </mesh>
      ))}
    </group>
  );
}

// ---------- Market cabins ----------

function MarketCabins() {
  const cabins = useMemo(() => {
    const arr: {
      x: number;
      z: number;
      rot: number;
      roofColor: string;
    }[] = [];
    // Along left side
    for (let i = 0; i < 5; i++) {
      arr.push({
        x: -14,
        z: -8 + i * 4,
        rot: Math.PI / 2,
        roofColor: ['#8b2222', '#228b22', '#22228b', '#8b8b22', '#8b2288'][i],
      });
    }
    // Along right side
    for (let i = 0; i < 5; i++) {
      arr.push({
        x: 14,
        z: -8 + i * 4,
        rot: -Math.PI / 2,
        roofColor: ['#228b22', '#8b2222', '#8b8b22', '#22228b', '#8b2288'][i],
      });
    }
    return arr;
  }, []);

  return (
    <group>
      {cabins.map((c, i) => (
        <group
          key={i}
          position={[c.x, 0, c.z]}
          rotation={[0, c.rot, 0]}
        >
          {/* Walls */}
          <mesh position={[0, 1.2, 0]} castShadow receiveShadow>
            <boxGeometry args={[3, 2.4, 2.5]} />
            <meshStandardMaterial color="#a0835a" roughness={0.8} />
          </mesh>
          {/* Peaked roof */}
          <mesh position={[0, 2.8, 0]} castShadow>
            <boxGeometry args={[3.4, 0.15, 2.8]} />
            <meshStandardMaterial color={c.roofColor} roughness={0.7} />
          </mesh>
          <mesh position={[0, 3.2, 0]} rotation={[0, 0, 0]} castShadow>
            <coneGeometry args={[1.8, 1, 4]} />
            <meshStandardMaterial color={c.roofColor} roughness={0.7} />
          </mesh>
          {/* Warm glowing window */}
          <mesh position={[0, 1.2, 1.26]}>
            <planeGeometry args={[1.5, 1.2]} />
            <meshStandardMaterial
              color="#ffdd88"
              emissive="#ffcc66"
              emissiveIntensity={1.2}
            />
          </mesh>
          {/* Interior glow */}
          <pointLight
            position={[0, 1.5, 0.5]}
            color="#ffcc66"
            intensity={3}
            distance={6}
          />
        </group>
      ))}
    </group>
  );
}

// ---------- Fairy lights / Christmas lights ----------

function FairyLights() {
  const lightStrings = useMemo(() => {
    const strings: { x1: number; x2: number; z: number; y: number }[] = [];
    for (let i = 0; i < 8; i++) {
      strings.push({
        x1: -14,
        x2: 14,
        z: -10 + i * 3,
        y: 4 + Math.random(),
      });
    }
    return strings;
  }, []);

  const colors = ['#ff4444', '#44ff44', '#ffff44', '#4444ff', '#ff44ff', '#ffffff'];

  return (
    <group>
      {lightStrings.map((s, si) => (
        <group key={si}>
          {Array.from({ length: 14 }).map((_, i) => {
            const t = i / 13;
            const x = s.x1 + t * (s.x2 - s.x1);
            const sag = 4 * t * (1 - t) * 1;
            const y = s.y - sag;
            const color = colors[(si + i) % colors.length];
            return (
              <mesh key={i} position={[x, y, s.z]}>
                <sphereGeometry args={[0.05, 4, 4]} />
                <meshStandardMaterial
                  color={color}
                  emissive={color}
                  emissiveIntensity={2}
                />
              </mesh>
            );
          })}
        </group>
      ))}
    </group>
  );
}

// ---------- Snowfall ----------

function Snowfall({ count = 500 }: { count?: number }) {
  const meshRef = useRef<THREE.InstancedMesh>(null);
  const dummy = useMemo(() => new THREE.Object3D(), []);

  const particles = useMemo(() => {
    const arr: {
      x: number;
      y: number;
      z: number;
      speed: number;
      wobble: number;
      phase: number;
    }[] = [];
    for (let i = 0; i < count; i++) {
      arr.push({
        x: (Math.random() - 0.5) * 50,
        y: Math.random() * 30,
        z: (Math.random() - 0.5) * 40,
        speed: 0.5 + Math.random() * 1.5,
        wobble: Math.random() * 2,
        phase: Math.random() * Math.PI * 2,
      });
    }
    return arr;
  }, [count]);

  useFrame(({ clock }) => {
    if (!meshRef.current) return;
    const t = clock.getElapsedTime();
    particles.forEach((p, i) => {
      let y = p.y - (t * p.speed) % 30;
      if (y < 0) y += 30;
      dummy.position.set(
        p.x + Math.sin(t * p.wobble + p.phase) * 0.5,
        y,
        p.z + Math.cos(t * p.wobble * 0.7 + p.phase) * 0.5
      );
      dummy.scale.setScalar(0.03 + Math.random() * 0.02);
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

// ---------- Hot chocolate bar ----------

function HotChocolateBar() {
  return (
    <group position={[0, 0, 10]}>
      {/* Stall */}
      <mesh position={[0, 1, 0]} castShadow receiveShadow>
        <boxGeometry args={[3, 2, 2]} />
        <meshStandardMaterial color="#8b5e3c" roughness={0.8} />
      </mesh>
      {/* Roof */}
      <mesh position={[0, 2.3, 0]} castShadow>
        <boxGeometry args={[3.5, 0.15, 2.5]} />
        <meshStandardMaterial color="#6b3e2c" roughness={0.7} />
      </mesh>
      {/* Steam */}
      <pointLight
        position={[0, 2.5, 0.5]}
        color="#ffcc88"
        intensity={4}
        distance={6}
      />
    </group>
  );
}

// ---------- Skating figures ----------

function SkatingFigures() {
  const groupRef = useRef<THREE.Group>(null);

  const figures = useMemo(
    () => [
      { angle: 0, radius: 4, speed: 0.3 },
      { angle: Math.PI / 3, radius: 5, speed: 0.25 },
      { angle: Math.PI, radius: 3, speed: 0.35 },
      { angle: (Math.PI * 4) / 3, radius: 6, speed: 0.2 },
      { angle: (Math.PI * 5) / 3, radius: 3.5, speed: 0.28 },
    ],
    []
  );

  useFrame(({ clock }) => {
    if (!groupRef.current) return;
    const t = clock.getElapsedTime();
    groupRef.current.children.forEach((child, i) => {
      if (i < figures.length) {
        const f = figures[i];
        const angle = f.angle + t * f.speed;
        child.position.x = Math.cos(angle) * f.radius;
        child.position.z = Math.sin(angle) * f.radius;
        child.rotation.y = angle + Math.PI / 2;
      }
    });
  });

  return (
    <group ref={groupRef} position={[0, 0.1, 0]}>
      {figures.map((_, i) => (
        <group key={i}>
          <mesh position={[0, 0.7, 0]} castShadow>
            <capsuleGeometry args={[0.15, 0.6, 4, 8]} />
            <meshStandardMaterial
              color={
                ['#cc3333', '#3333cc', '#33cc33', '#cc33cc', '#cccc33'][i]
              }
              roughness={0.7}
            />
          </mesh>
          <mesh position={[0, 1.3, 0]} castShadow>
            <sphereGeometry args={[0.12, 6, 6]} />
            <meshStandardMaterial color="#ffddcc" roughness={0.7} />
          </mesh>
        </group>
      ))}
    </group>
  );
}

// ---------- Winter sky ----------

function WinterSky() {
  const gradientMap = useMemo(() => {
    const canvas = document.createElement('canvas');
    canvas.width = 1;
    canvas.height = 256;
    const ctx = canvas.getContext('2d')!;
    const gradient = ctx.createLinearGradient(0, 0, 0, 256);
    gradient.addColorStop(0, '#0a0a2a');
    gradient.addColorStop(0.3, '#1a1a3a');
    gradient.addColorStop(0.6, '#2a2a4a');
    gradient.addColorStop(0.8, '#3a3a5a');
    gradient.addColorStop(1.0, '#4a4a6a');
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

export default function WinterVillageWorld() {
  return (
    <>
      {/* Atmosphere */}
      <fog attach="fog" args={['#2a2a4a', 25, 100]} />
      <ambientLight intensity={0.15} color="#aabbdd" />
      <directionalLight
        position={[10, 15, 10]}
        intensity={0.4}
        color="#bbccee"
        castShadow
        shadow-mapSize-width={1024}
        shadow-mapSize-height={1024}
      />

      <WinterSky />

      {/* Snow-covered ground */}
      <mesh
        rotation={[-Math.PI / 2, 0, 0]}
        position={[0, 0, 0]}
        receiveShadow
      >
        <planeGeometry args={[80, 80]} />
        <meshStandardMaterial color="#e8e8f0" roughness={0.9} />
      </mesh>

      <CityHallFacade />
      <IceRink />
      <MarketCabins />
      <FairyLights />
      <Snowfall count={500} />
      <HotChocolateBar />
      <SkatingFigures />
    </>
  );
}
