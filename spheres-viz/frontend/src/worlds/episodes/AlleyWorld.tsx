import { useRef, useMemo } from 'react';
import { useFrame } from '@react-three/fiber';
import * as THREE from 'three';

// ---------- Corridor walls ----------

function CorridorWalls() {
  return (
    <group>
      {/* Left wall */}
      <mesh position={[-3, 5, 0]} receiveShadow castShadow>
        <boxGeometry args={[0.5, 10, 40]} />
        <meshStandardMaterial color="#2a2a2a" roughness={0.9} />
      </mesh>
      {/* Right wall */}
      <mesh position={[3, 5, 0]} receiveShadow castShadow>
        <boxGeometry args={[0.5, 10, 40]} />
        <meshStandardMaterial color="#2a2a2a" roughness={0.9} />
      </mesh>
    </group>
  );
}

// ---------- Projection mapping panels ----------

function ProjectionPanels() {
  const panels = useMemo(() => {
    const arr: {
      x: number;
      y: number;
      z: number;
      w: number;
      h: number;
      color: string;
      emissiveColor: string;
      side: 'left' | 'right';
    }[] = [];
    const colors = [
      { color: '#ff2266', emissive: '#ff2266' },
      { color: '#4422ff', emissive: '#4422ff' },
      { color: '#ff44ff', emissive: '#ff44ff' },
      { color: '#22ffcc', emissive: '#22ffcc' },
      { color: '#ff8800', emissive: '#ff8800' },
      { color: '#8844ff', emissive: '#8844ff' },
      { color: '#ff4488', emissive: '#ff4488' },
      { color: '#44aaff', emissive: '#44aaff' },
    ];
    for (let i = 0; i < 20; i++) {
      const side = i % 2 === 0 ? 'left' : 'right';
      const c = colors[i % colors.length];
      arr.push({
        x: side === 'left' ? -2.7 : 2.7,
        y: 1 + Math.random() * 6,
        z: -18 + i * 1.9,
        w: 1 + Math.random() * 1.5,
        h: 0.8 + Math.random() * 2,
        color: c.color,
        emissiveColor: c.emissive,
        side,
      });
    }
    return arr;
  }, []);

  const groupRef = useRef<THREE.Group>(null);

  useFrame(({ clock }) => {
    if (!groupRef.current) return;
    const t = clock.getElapsedTime();
    groupRef.current.children.forEach((child, i) => {
      if (child instanceof THREE.Mesh && child.material instanceof THREE.MeshStandardMaterial) {
        child.material.emissiveIntensity =
          0.3 + Math.sin(t * 0.8 + i * 0.5) * 0.2;
      }
    });
  });

  return (
    <group ref={groupRef}>
      {panels.map((p, i) => (
        <mesh
          key={i}
          position={[p.x, p.y, p.z]}
          rotation={[0, p.side === 'left' ? Math.PI / 2 : -Math.PI / 2, 0]}
        >
          <planeGeometry args={[p.w, p.h]} />
          <meshStandardMaterial
            color={p.color}
            emissive={p.emissiveColor}
            emissiveIntensity={0.4}
            roughness={0.2}
            transparent
            opacity={0.85}
          />
        </mesh>
      ))}
    </group>
  );
}

// ---------- Art frames ----------

function ArtFrames() {
  const frames = useMemo(() => {
    const arr: {
      x: number;
      y: number;
      z: number;
      w: number;
      h: number;
      side: 'left' | 'right';
      color: string;
    }[] = [];
    for (let i = 0; i < 8; i++) {
      const side = i % 2 === 0 ? 'left' : 'right';
      arr.push({
        x: side === 'left' ? -2.65 : 2.65,
        y: 2 + Math.random() * 2,
        z: -15 + i * 4.5,
        w: 0.8 + Math.random() * 0.6,
        h: 0.6 + Math.random() * 0.8,
        side,
        color: ['#1a1a2a', '#2a1a2a', '#1a2a2a', '#2a2a1a'][i % 4],
      });
    }
    return arr;
  }, []);

  return (
    <group>
      {frames.map((f, i) => (
        <group key={i} position={[f.x, f.y, f.z]}>
          {/* Frame border */}
          <mesh
            rotation={[
              0,
              f.side === 'left' ? Math.PI / 2 : -Math.PI / 2,
              0,
            ]}
          >
            <planeGeometry args={[f.w + 0.12, f.h + 0.12]} />
            <meshStandardMaterial color="#888" metalness={0.6} roughness={0.3} />
          </mesh>
          {/* Canvas inside */}
          <mesh
            position={[f.side === 'left' ? 0.01 : -0.01, 0, 0]}
            rotation={[
              0,
              f.side === 'left' ? Math.PI / 2 : -Math.PI / 2,
              0,
            ]}
          >
            <planeGeometry args={[f.w, f.h]} />
            <meshStandardMaterial color={f.color} roughness={0.8} />
          </mesh>
        </group>
      ))}
    </group>
  );
}

// ---------- Neon reflective ground ----------

function WetGround() {
  return (
    <mesh
      rotation={[-Math.PI / 2, 0, 0]}
      position={[0, 0, 0]}
      receiveShadow
    >
      <planeGeometry args={[6, 40]} />
      <meshStandardMaterial
        color="#111118"
        roughness={0.05}
        metalness={0.9}
      />
    </mesh>
  );
}

// ---------- Colored point lights ----------

function NeonLights() {
  const lights = useMemo(
    () => [
      { pos: [0, 3, -15] as [number, number, number], color: '#aa22ff' },
      { pos: [-1, 4, -10] as [number, number, number], color: '#4466ff' },
      { pos: [1, 2.5, -5] as [number, number, number], color: '#ff22aa' },
      { pos: [0, 5, 0] as [number, number, number], color: '#aa22ff' },
      { pos: [-1, 3, 5] as [number, number, number], color: '#2266ff' },
      { pos: [1, 4, 10] as [number, number, number], color: '#ff44cc' },
      { pos: [0, 2, 15] as [number, number, number], color: '#6622ff' },
    ],
    []
  );

  return (
    <group>
      {lights.map((l, i) => (
        <pointLight
          key={i}
          position={l.pos}
          color={l.color}
          intensity={4}
          distance={12}
          decay={2}
        />
      ))}
    </group>
  );
}

// ---------- Fog particles ----------

function FogParticles({ count = 40 }: { count?: number }) {
  const meshRef = useRef<THREE.InstancedMesh>(null);
  const dummy = useMemo(() => new THREE.Object3D(), []);

  const particles = useMemo(() => {
    const arr: { x: number; y: number; z: number; speed: number }[] = [];
    for (let i = 0; i < count; i++) {
      arr.push({
        x: (Math.random() - 0.5) * 5,
        y: 0.5 + Math.random() * 3,
        z: (Math.random() - 0.5) * 35,
        speed: 0.1 + Math.random() * 0.3,
      });
    }
    return arr;
  }, [count]);

  useFrame(({ clock }) => {
    if (!meshRef.current) return;
    const t = clock.getElapsedTime();
    particles.forEach((p, i) => {
      dummy.position.set(
        p.x + Math.sin(t * p.speed + i) * 0.5,
        p.y + Math.sin(t * p.speed * 0.5 + i * 2) * 0.3,
        p.z
      );
      const s = 0.3 + Math.sin(t * 0.2 + i) * 0.1;
      dummy.scale.set(s, s, s);
      dummy.updateMatrix();
      meshRef.current!.setMatrixAt(i, dummy.matrix);
    });
    meshRef.current.instanceMatrix.needsUpdate = true;
  });

  return (
    <instancedMesh ref={meshRef} args={[undefined, undefined, count]}>
      <sphereGeometry args={[1, 6, 6]} />
      <meshBasicMaterial color="#8866aa" transparent opacity={0.06} />
    </instancedMesh>
  );
}

// ---------- Night sky ----------

function NightSky() {
  return (
    <mesh>
      <sphereGeometry args={[180, 32, 32]} />
      <meshBasicMaterial color="#0a0a15" side={THREE.BackSide} />
    </mesh>
  );
}

// ---------- Main world ----------

export default function AlleyWorld() {
  return (
    <>
      {/* Atmosphere */}
      <fog attach="fog" args={['#0a0a15', 8, 50]} />
      <ambientLight intensity={0.05} color="#aaaaff" />

      <NightSky />

      <WetGround />
      <CorridorWalls />
      <ProjectionPanels />
      <ArtFrames />
      <NeonLights />
      <FogParticles count={40} />
    </>
  );
}
