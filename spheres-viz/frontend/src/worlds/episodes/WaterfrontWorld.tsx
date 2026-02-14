import { useRef, useMemo } from 'react';
import { useFrame } from '@react-three/fiber';
import { MeshReflectorMaterial, Float, Stars } from '@react-three/drei';
import * as THREE from 'three';

// ---------- Skyline silhouette ----------

function Skyline() {
  const buildings = useMemo(() => {
    const data: { x: number; z: number; w: number; d: number; h: number }[] =
      [];
    for (let i = 0; i < 30; i++) {
      data.push({
        x: -40 + i * 2.8 + (Math.random() - 0.5) * 1.2,
        z: -45 + (Math.random() - 0.5) * 6,
        w: 1 + Math.random() * 1.8,
        d: 1 + Math.random() * 1.8,
        h: 2 + Math.random() * 12,
      });
    }
    return data;
  }, []);

  return (
    <group>
      {buildings.map((b, i) => (
        <mesh key={i} position={[b.x, b.h / 2, b.z]} castShadow>
          <boxGeometry args={[b.w, b.h, b.d]} />
          <meshStandardMaterial color="#1a1a2e" />
        </mesh>
      ))}
    </group>
  );
}

// ---------- Floating barge/stage ----------

function BargeStage() {
  const ref = useRef<THREE.Group>(null);

  useFrame(({ clock }) => {
    if (!ref.current) return;
    const t = clock.getElapsedTime();
    ref.current.position.y = 0.3 + Math.sin(t * 0.4) * 0.08;
    ref.current.rotation.z = Math.sin(t * 0.3) * 0.008;
  });

  return (
    <group ref={ref} position={[0, 0.3, -5]}>
      {/* Barge platform */}
      <mesh castShadow receiveShadow>
        <boxGeometry args={[10, 0.6, 6]} />
        <meshStandardMaterial color="#5c3a1e" roughness={0.8} />
      </mesh>
      {/* Stage backdrop */}
      <mesh position={[0, 3, -2.5]} castShadow>
        <boxGeometry args={[8, 5, 0.3]} />
        <meshStandardMaterial color="#2a1a0a" roughness={0.6} />
      </mesh>
      {/* Stage floor highlight */}
      <mesh position={[0, 0.32, 0]} receiveShadow>
        <boxGeometry args={[8, 0.02, 4]} />
        <meshStandardMaterial color="#3a2a1a" roughness={0.4} />
      </mesh>
      {/* Warm stage lights */}
      <pointLight
        position={[-3, 4, 0]}
        color="#ff9944"
        intensity={8}
        distance={20}
        castShadow
      />
      <pointLight
        position={[3, 4, 0]}
        color="#ffaa55"
        intensity={8}
        distance={20}
        castShadow
      />
      <spotLight
        position={[0, 6, 2]}
        angle={0.5}
        penumbra={0.8}
        color="#ffcc88"
        intensity={12}
        distance={25}
        target-position={[0, 0, -1]}
        castShadow
      />
    </group>
  );
}

// ---------- Pier ----------

function Pier() {
  return (
    <group position={[0, 0, 8]}>
      {/* Pier deck */}
      <mesh position={[0, 0.8, 0]} receiveShadow castShadow>
        <boxGeometry args={[6, 0.3, 16]} />
        <meshStandardMaterial color="#6b4226" roughness={0.85} />
      </mesh>
      {/* Pier supports */}
      {[-2, 0, 2].map((x) =>
        [2, 6, 10, 14].map((z) => (
          <mesh
            key={`${x}-${z}`}
            position={[x, 0, z - 8]}
            castShadow
          >
            <cylinderGeometry args={[0.12, 0.15, 1.8, 8]} />
            <meshStandardMaterial color="#4a3020" roughness={0.9} />
          </mesh>
        ))
      )}
      {/* Railing posts */}
      {Array.from({ length: 8 }).map((_, i) => (
        <mesh key={`rail-${i}`} position={[3, 1.6, -6 + i * 2]} castShadow>
          <cylinderGeometry args={[0.05, 0.05, 1.2, 6]} />
          <meshStandardMaterial color="#5a3a20" />
        </mesh>
      ))}
    </group>
  );
}

// ---------- Floating Lanterns ----------

function FloatingLanterns() {
  const lanterns = useMemo(() => {
    const arr: { x: number; z: number; phase: number; color: string }[] = [];
    for (let i = 0; i < 18; i++) {
      arr.push({
        x: (Math.random() - 0.5) * 40,
        z: -20 + Math.random() * 15,
        phase: Math.random() * Math.PI * 2,
        color: ['#ffaa44', '#ff8833', '#ffcc66', '#ffdd88'][
          Math.floor(Math.random() * 4)
        ],
      });
    }
    return arr;
  }, []);

  return (
    <group>
      {lanterns.map((l, i) => (
        <Float
          key={i}
          speed={0.8}
          rotationIntensity={0}
          floatIntensity={0.3}
          floatingRange={[-0.1, 0.1]}
        >
          <mesh position={[l.x, 0.4, l.z]}>
            <sphereGeometry args={[0.15, 8, 8]} />
            <meshStandardMaterial
              color={l.color}
              emissive={l.color}
              emissiveIntensity={2}
            />
          </mesh>
          <pointLight
            position={[l.x, 0.5, l.z]}
            color={l.color}
            intensity={1.5}
            distance={4}
          />
        </Float>
      ))}
    </group>
  );
}

// ---------- Twilight sky gradient ----------

function TwilightSky() {
  const meshRef = useRef<THREE.Mesh>(null);

  const gradientMap = useMemo(() => {
    const canvas = document.createElement('canvas');
    canvas.width = 1;
    canvas.height = 256;
    const ctx = canvas.getContext('2d')!;
    const gradient = ctx.createLinearGradient(0, 0, 0, 256);
    gradient.addColorStop(0, '#0a0a1a');
    gradient.addColorStop(0.3, '#1a1a3a');
    gradient.addColorStop(0.5, '#2a1a3a');
    gradient.addColorStop(0.7, '#4a2a3a');
    gradient.addColorStop(0.85, '#6a3a2a');
    gradient.addColorStop(1.0, '#8a4a1a');
    ctx.fillStyle = gradient;
    ctx.fillRect(0, 0, 1, 256);
    const tex = new THREE.CanvasTexture(canvas);
    return tex;
  }, []);

  return (
    <mesh ref={meshRef} position={[0, 0, 0]}>
      <sphereGeometry args={[200, 32, 32]} />
      <meshBasicMaterial map={gradientMap} side={THREE.BackSide} />
    </mesh>
  );
}

// ---------- Main world ----------

export default function WaterfrontWorld() {
  return (
    <>
      {/* Atmosphere */}
      <fog attach="fog" args={['#1a1a2e', 20, 120]} />
      <ambientLight intensity={0.15} color="#8888cc" />
      <directionalLight
        position={[20, 15, -10]}
        intensity={0.3}
        color="#ffccaa"
      />

      <TwilightSky />
      <Stars
        radius={150}
        depth={80}
        count={1500}
        factor={3}
        saturation={0.2}
        fade
        speed={0.5}
      />

      {/* Water surface */}
      <mesh
        rotation={[-Math.PI / 2, 0, 0]}
        position={[0, -0.05, 0]}
        receiveShadow
      >
        <planeGeometry args={[200, 200]} />
        <MeshReflectorMaterial
          mirror={0.6}
          blur={[300, 100]}
          resolution={512}
          mixBlur={1}
          mixStrength={40}
          roughness={1}
          depthScale={1.2}
          minDepthThreshold={0.4}
          maxDepthThreshold={1.4}
          color="#0a1a2a"
          metalness={0.5}
        />
      </mesh>

      <BargeStage />
      <Pier />
      <FloatingLanterns />
      <Skyline />
    </>
  );
}
