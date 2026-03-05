import { useRef, useMemo } from 'react';
import { useFrame } from '@react-three/fiber';
import * as THREE from 'three';

// ---------- Half pipe ----------

function HalfPipe() {
  const geometry = useMemo(() => {
    const shape = new THREE.Shape();
    const segments = 32;
    // Draw a U-shape cross section
    for (let i = 0; i <= segments; i++) {
      const angle = Math.PI + (Math.PI * i) / segments;
      const x = Math.cos(angle) * 3;
      const y = Math.sin(angle) * 3;
      if (i === 0) shape.moveTo(x, y);
      else shape.lineTo(x, y);
    }
    // Close with outer shell
    for (let i = segments; i >= 0; i--) {
      const angle = Math.PI + (Math.PI * i) / segments;
      const x = Math.cos(angle) * 3.3;
      const y = Math.sin(angle) * 3.3;
      shape.lineTo(x, y);
    }
    shape.closePath();

    const extrudeSettings = {
      steps: 1,
      depth: 8,
      bevelEnabled: false,
    };
    return new THREE.ExtrudeGeometry(shape, extrudeSettings);
  }, []);

  return (
    <mesh
      geometry={geometry}
      position={[-6, 3, -4]}
      rotation={[0, Math.PI / 2, 0]}
      castShadow
      receiveShadow
    >
      <meshStandardMaterial color="#888899" roughness={0.3} metalness={0.1} />
    </mesh>
  );
}

// ---------- Quarter pipes ----------

function QuarterPipe({
  position,
  rotation = 0,
}: {
  position: [number, number, number];
  rotation?: number;
}) {
  const geometry = useMemo(() => {
    const shape = new THREE.Shape();
    const segments = 16;
    shape.moveTo(0, 0);
    for (let i = 0; i <= segments; i++) {
      const angle = (Math.PI / 2) * (i / segments);
      const x = Math.sin(angle) * 2.5;
      const y = (1 - Math.cos(angle)) * 2.5;
      shape.lineTo(x, y);
    }
    shape.lineTo(2.5, 0);
    shape.closePath();

    return new THREE.ExtrudeGeometry(shape, {
      steps: 1,
      depth: 4,
      bevelEnabled: false,
    });
  }, []);

  return (
    <mesh
      geometry={geometry}
      position={position}
      rotation={[0, rotation, 0]}
      castShadow
      receiveShadow
    >
      <meshStandardMaterial color="#888899" roughness={0.3} metalness={0.1} />
    </mesh>
  );
}

// ---------- Grind rails ----------

function GrindRail({
  start,
  end,
  height,
}: {
  start: [number, number, number];
  end: [number, number, number];
  height: number;
}) {
  const midX = (start[0] + end[0]) / 2;
  const midZ = (start[2] + end[2]) / 2;
  const dx = end[0] - start[0];
  const dz = end[2] - start[2];
  const length = Math.sqrt(dx * dx + dz * dz);
  const angle = Math.atan2(dx, dz);

  return (
    <group>
      {/* Rail */}
      <mesh
        position={[midX, height, midZ]}
        rotation={[0, angle, 0]}
        castShadow
      >
        <cylinderGeometry args={[0.04, 0.04, length, 8]} />
        <meshStandardMaterial color="#ccccdd" metalness={0.8} roughness={0.2} />
      </mesh>
      {/* Supports */}
      {[start, end].map((pos, i) => (
        <mesh key={i} position={[pos[0], height / 2, pos[2]]} castShadow>
          <cylinderGeometry args={[0.05, 0.06, height, 6]} />
          <meshStandardMaterial color="#999" roughness={0.5} />
        </mesh>
      ))}
    </group>
  );
}

// ---------- Graffiti walls ----------

function GraffitiWalls() {
  const walls = useMemo(
    () => [
      {
        pos: [10, 2, -6] as [number, number, number],
        size: [0.3, 4, 8] as [number, number, number],
        colors: ['#ff4466', '#ff6644'],
      },
      {
        pos: [-10, 1.5, 2] as [number, number, number],
        size: [0.3, 3, 6] as [number, number, number],
        colors: ['#4488ff', '#44ddff'],
      },
      {
        pos: [3, 2, 10] as [number, number, number],
        size: [7, 4, 0.3] as [number, number, number],
        colors: ['#ffcc00', '#ff8800'],
      },
    ],
    []
  );

  return (
    <group>
      {walls.map((w, i) => (
        <mesh key={i} position={w.pos} castShadow receiveShadow>
          <boxGeometry args={w.size} />
          <meshStandardMaterial
            color={w.colors[0]}
            emissive={w.colors[1]}
            emissiveIntensity={0.15}
            roughness={0.7}
          />
        </mesh>
      ))}
    </group>
  );
}

// ---------- DJ booth ----------

function DJBooth() {
  return (
    <group position={[6, 0, -8]}>
      {/* Elevated platform */}
      <mesh position={[0, 0.5, 0]} castShadow receiveShadow>
        <boxGeometry args={[3, 1, 2]} />
        <meshStandardMaterial color="#222" roughness={0.6} />
      </mesh>
      {/* Table */}
      <mesh position={[0, 1.2, 0]} castShadow>
        <boxGeometry args={[2, 0.1, 1]} />
        <meshStandardMaterial color="#111" roughness={0.4} />
      </mesh>
      {/* Speakers */}
      {[-1.8, 1.8].map((x) => (
        <mesh key={x} position={[x, 1, 0]} castShadow>
          <boxGeometry args={[0.8, 1.2, 0.6]} />
          <meshStandardMaterial color="#1a1a1a" roughness={0.5} />
        </mesh>
      ))}
      {/* Colored lights */}
      <pointLight
        position={[0, 3, 0]}
        color="#ff44ff"
        intensity={5}
        distance={12}
      />
      <pointLight
        position={[-2, 2, 1]}
        color="#44ff44"
        intensity={3}
        distance={8}
      />
    </group>
  );
}

// ---------- City panorama below ----------

function CityBelow() {
  const buildings = useMemo(() => {
    const arr: {
      x: number;
      z: number;
      w: number;
      d: number;
      h: number;
    }[] = [];
    for (let i = 0; i < 60; i++) {
      arr.push({
        x: (Math.random() - 0.5) * 100,
        z: (Math.random() - 0.5) * 100,
        w: 1 + Math.random() * 3,
        d: 1 + Math.random() * 3,
        h: 2 + Math.random() * 15,
      });
    }
    return arr;
  }, []);

  return (
    <group position={[0, -20, 0]}>
      {buildings.map((b, i) => (
        <mesh key={i} position={[b.x, b.h / 2, b.z]}>
          <boxGeometry args={[b.w, b.h, b.d]} />
          <meshStandardMaterial
            color="#2a2a3a"
            emissive="#1a1a2a"
            emissiveIntensity={0.1}
          />
        </mesh>
      ))}
    </group>
  );
}

// ---------- Wind particles ----------

function WindParticles({ count = 80 }: { count?: number }) {
  const meshRef = useRef<THREE.InstancedMesh>(null);
  const dummy = useMemo(() => new THREE.Object3D(), []);

  const particles = useMemo(() => {
    const arr: { x: number; y: number; z: number; speed: number }[] = [];
    for (let i = 0; i < count; i++) {
      arr.push({
        x: (Math.random() - 0.5) * 40,
        y: 1 + Math.random() * 8,
        z: (Math.random() - 0.5) * 40,
        speed: 2 + Math.random() * 4,
      });
    }
    return arr;
  }, [count]);

  useFrame(({ clock }) => {
    if (!meshRef.current) return;
    const t = clock.getElapsedTime();
    particles.forEach((p, i) => {
      const x = ((p.x + t * p.speed) % 40) - 20;
      dummy.position.set(x, p.y, p.z);
      dummy.scale.set(0.3, 0.02, 0.02);
      dummy.rotation.set(0, 0, 0);
      dummy.updateMatrix();
      meshRef.current!.setMatrixAt(i, dummy.matrix);
    });
    meshRef.current.instanceMatrix.needsUpdate = true;
  });

  return (
    <instancedMesh ref={meshRef} args={[undefined, undefined, count]}>
      <boxGeometry args={[1, 1, 1]} />
      <meshBasicMaterial color="#ffffff" transparent opacity={0.3} />
    </instancedMesh>
  );
}

// ---------- Golden hour sky ----------

function GoldenSky() {
  const gradientMap = useMemo(() => {
    const canvas = document.createElement('canvas');
    canvas.width = 1;
    canvas.height = 256;
    const ctx = canvas.getContext('2d')!;
    const gradient = ctx.createLinearGradient(0, 0, 0, 256);
    gradient.addColorStop(0, '#1a2a4a');
    gradient.addColorStop(0.3, '#3a4a6a');
    gradient.addColorStop(0.5, '#6a5a4a');
    gradient.addColorStop(0.7, '#cc8844');
    gradient.addColorStop(0.85, '#ee9944');
    gradient.addColorStop(1.0, '#ffbb66');
    ctx.fillStyle = gradient;
    ctx.fillRect(0, 0, 1, 256);
    return new THREE.CanvasTexture(canvas);
  }, []);

  return (
    <mesh>
      <sphereGeometry args={[200, 32, 32]} />
      <meshBasicMaterial map={gradientMap} side={THREE.BackSide} />
    </mesh>
  );
}

// ---------- Main world ----------

export default function RooftopWorld() {
  return (
    <>
      {/* Atmosphere */}
      <fog attach="fog" args={['#cc8844', 40, 150]} />
      <ambientLight intensity={0.25} color="#ffddaa" />
      <directionalLight
        position={[30, 20, 15]}
        intensity={1.2}
        color="#ffaa55"
        castShadow
        shadow-mapSize-width={1024}
        shadow-mapSize-height={1024}
        shadow-camera-left={-20}
        shadow-camera-right={20}
        shadow-camera-top={20}
        shadow-camera-bottom={-20}
      />

      <GoldenSky />

      {/* Rooftop platform */}
      <mesh position={[0, -0.25, 0]} receiveShadow castShadow>
        <boxGeometry args={[30, 0.5, 24]} />
        <meshStandardMaterial color="#888888" roughness={0.8} />
      </mesh>
      {/* Platform edge lip */}
      <mesh position={[0, 0.15, -12]} castShadow>
        <boxGeometry args={[30, 0.8, 0.3]} />
        <meshStandardMaterial color="#666" roughness={0.7} />
      </mesh>
      <mesh position={[0, 0.15, 12]} castShadow>
        <boxGeometry args={[30, 0.8, 0.3]} />
        <meshStandardMaterial color="#666" roughness={0.7} />
      </mesh>

      <HalfPipe />
      <QuarterPipe position={[8, 0, -8]} rotation={Math.PI} />
      <QuarterPipe position={[-4, 0, 6]} rotation={Math.PI / 2} />

      <GrindRail
        start={[-2, 0, -2]}
        end={[4, 0, -2]}
        height={0.6}
      />
      <GrindRail
        start={[0, 0, 2]}
        end={[6, 0, 4]}
        height={0.45}
      />

      <GraffitiWalls />
      <DJBooth />
      <WindParticles count={80} />
      <CityBelow />
    </>
  );
}
