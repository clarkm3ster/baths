import { useRef, useMemo } from 'react';
import { useFrame } from '@react-three/fiber';
import { Stars } from '@react-three/drei';
import * as THREE from 'three';

// ---------- Winding path with LED edges ----------

function GlowPath() {
  const pathCurve = useMemo(() => {
    const points: THREE.Vector3[] = [];
    for (let i = 0; i <= 80; i++) {
      const t = i / 80;
      const x = Math.sin(t * Math.PI * 3) * 8 + t * 5;
      const z = -35 + t * 70;
      points.push(new THREE.Vector3(x, 0.05, z));
    }
    return new THREE.CatmullRomCurve3(points, false);
  }, []);

  const pathGeometry = useMemo(() => {
    return new THREE.TubeGeometry(pathCurve, 200, 1.5, 4, false);
  }, [pathCurve]);

  // Flatten to ground
  useMemo(() => {
    const positions = pathGeometry.attributes.position;
    for (let i = 0; i < positions.count; i++) {
      const y = positions.getY(i);
      positions.setY(i, Math.max(y, 0.01) * 0.1);
    }
    positions.needsUpdate = true;
  }, [pathGeometry]);

  // LED strips along edges
  const ledPositions = useMemo(() => {
    const leftLEDs: THREE.Vector3[] = [];
    const rightLEDs: THREE.Vector3[] = [];
    for (let i = 0; i <= 120; i++) {
      const t = i / 120;
      const point = pathCurve.getPoint(t);
      const tangent = pathCurve.getTangent(t);
      const normal = new THREE.Vector3(-tangent.z, 0, tangent.x).normalize();
      leftLEDs.push(
        new THREE.Vector3(
          point.x + normal.x * 1.6,
          0.1,
          point.z + normal.z * 1.6
        )
      );
      rightLEDs.push(
        new THREE.Vector3(
          point.x - normal.x * 1.6,
          0.1,
          point.z - normal.z * 1.6
        )
      );
    }
    return { left: leftLEDs, right: rightLEDs };
  }, [pathCurve]);

  const ledColors = ['#4488ff', '#8844ff', '#ff44aa'];

  return (
    <group>
      {/* Path surface */}
      <mesh geometry={pathGeometry} receiveShadow>
        <meshStandardMaterial color="#3a3a4a" roughness={0.7} />
      </mesh>

      {/* Left LED strip */}
      {ledPositions.left.map((pos, i) => {
        const colorIndex = Math.floor((i / ledPositions.left.length) * ledColors.length);
        const color = ledColors[Math.min(colorIndex, ledColors.length - 1)];
        return (
          <group key={`l-${i}`}>
            <mesh position={[pos.x, pos.y, pos.z]}>
              <sphereGeometry args={[0.08, 4, 4]} />
              <meshStandardMaterial
                color={color}
                emissive={color}
                emissiveIntensity={3}
              />
            </mesh>
            {i % 8 === 0 && (
              <pointLight
                position={[pos.x, 0.3, pos.z]}
                color={color}
                intensity={1}
                distance={4}
              />
            )}
          </group>
        );
      })}

      {/* Right LED strip */}
      {ledPositions.right.map((pos, i) => {
        const colorIndex = Math.floor((i / ledPositions.right.length) * ledColors.length);
        const color = ledColors[Math.min(colorIndex, ledColors.length - 1)];
        return (
          <mesh key={`r-${i}`} position={[pos.x, pos.y, pos.z]}>
            <sphereGeometry args={[0.08, 4, 4]} />
            <meshStandardMaterial
              color={color}
              emissive={color}
              emissiveIntensity={3}
            />
          </mesh>
        );
      })}
    </group>
  );
}

// ---------- River ----------

function River() {
  const ref = useRef<THREE.Mesh>(null);

  useFrame(({ clock }) => {
    if (!ref.current) return;
    const mat = ref.current.material as THREE.MeshStandardMaterial;
    mat.emissiveIntensity = 0.03 + Math.sin(clock.getElapsedTime() * 0.3) * 0.01;
  });

  return (
    <mesh
      ref={ref}
      rotation={[-Math.PI / 2, 0, 0]}
      position={[-15, -0.5, 0]}
      receiveShadow
    >
      <planeGeometry args={[20, 80]} />
      <meshStandardMaterial
        color="#0a1a3a"
        emissive="#0a1a3a"
        emissiveIntensity={0.03}
        roughness={0.1}
        metalness={0.7}
      />
    </mesh>
  );
}

// ---------- Fitness stations ----------

function FitnessStation({
  position,
}: {
  position: [number, number, number];
}) {
  return (
    <group position={position}>
      {/* Upright posts */}
      {[-0.8, 0.8].map((x) => (
        <mesh key={x} position={[x, 1, 0]} castShadow>
          <cylinderGeometry args={[0.06, 0.06, 2, 8]} />
          <meshStandardMaterial color="#888" metalness={0.7} roughness={0.3} />
        </mesh>
      ))}
      {/* Top bar */}
      <mesh position={[0, 2, 0]} rotation={[0, 0, Math.PI / 2]} castShadow>
        <cylinderGeometry args={[0.04, 0.04, 1.6, 8]} />
        <meshStandardMaterial color="#aaa" metalness={0.8} roughness={0.2} />
      </mesh>
      {/* Base plate */}
      <mesh position={[0, 0.02, 0]} receiveShadow>
        <boxGeometry args={[2, 0.04, 1.5]} />
        <meshStandardMaterial color="#555" roughness={0.8} />
      </mesh>
    </group>
  );
}

// ---------- Runner silhouettes ----------

function Runners() {
  const groupRef = useRef<THREE.Group>(null);

  const runners = useMemo(
    () => [
      { offset: 0, speed: 0.6 },
      { offset: 0.25, speed: 0.5 },
      { offset: 0.5, speed: 0.7 },
      { offset: 0.75, speed: 0.55 },
    ],
    []
  );

  const pathCurve = useMemo(() => {
    const points: THREE.Vector3[] = [];
    for (let i = 0; i <= 80; i++) {
      const t = i / 80;
      const x = Math.sin(t * Math.PI * 3) * 8 + t * 5;
      const z = -35 + t * 70;
      points.push(new THREE.Vector3(x, 0.05, z));
    }
    return new THREE.CatmullRomCurve3(points, false);
  }, []);

  useFrame(({ clock }) => {
    if (!groupRef.current) return;
    const t = clock.getElapsedTime();
    groupRef.current.children.forEach((child, i) => {
      if (i < runners.length) {
        const r = runners[i];
        const pos = (r.offset + t * r.speed * 0.02) % 1;
        const point = pathCurve.getPoint(pos);
        const tangent = pathCurve.getTangent(pos);
        child.position.set(point.x, 0, point.z);
        child.rotation.y = Math.atan2(tangent.x, tangent.z);
      }
    });
  });

  return (
    <group ref={groupRef}>
      {runners.map((_, i) => (
        <group key={i}>
          <mesh position={[0, 0.85, 0]} castShadow>
            <capsuleGeometry args={[0.15, 0.6, 4, 8]} />
            <meshStandardMaterial color="#1a1a2a" roughness={0.9} />
          </mesh>
          <mesh position={[0, 1.5, 0]} castShadow>
            <sphereGeometry args={[0.12, 6, 6]} />
            <meshStandardMaterial color="#1a1a2a" roughness={0.9} />
          </mesh>
        </group>
      ))}
    </group>
  );
}

// ---------- Rest stations ----------

function RestStation({
  position,
  rotation = 0,
}: {
  position: [number, number, number];
  rotation?: number;
}) {
  return (
    <group position={position} rotation={[0, rotation, 0]}>
      {/* Bench */}
      <mesh position={[0, 0.4, 0]} castShadow receiveShadow>
        <boxGeometry args={[2, 0.1, 0.5]} />
        <meshStandardMaterial color="#6b4a2a" roughness={0.85} />
      </mesh>
      {[-0.8, 0.8].map((x) => (
        <mesh key={x} position={[x, 0.2, 0]} castShadow>
          <boxGeometry args={[0.1, 0.4, 0.5]} />
          <meshStandardMaterial color="#555" roughness={0.7} />
        </mesh>
      ))}
      {/* Shelter posts */}
      {[-1, 1].map((x) => (
        <mesh key={`p-${x}`} position={[x, 1.2, -0.5]} castShadow>
          <cylinderGeometry args={[0.05, 0.05, 2.4, 6]} />
          <meshStandardMaterial color="#666" roughness={0.6} />
        </mesh>
      ))}
      {/* Shelter roof */}
      <mesh position={[0, 2.4, -0.3]} castShadow>
        <boxGeometry args={[2.5, 0.08, 1.2]} />
        <meshStandardMaterial color="#444" roughness={0.7} />
      </mesh>
    </group>
  );
}

// ---------- Main world ----------

export default function GlowCorridorWorld() {
  return (
    <>
      {/* Atmosphere */}
      <fog attach="fog" args={['#0a0a1a', 20, 80]} />
      <ambientLight intensity={0.06} color="#8888cc" />

      {/* Night sky */}
      <mesh>
        <sphereGeometry args={[180, 32, 32]} />
        <meshBasicMaterial color="#050510" side={THREE.BackSide} />
      </mesh>
      <Stars
        radius={150}
        depth={60}
        count={2000}
        factor={3}
        saturation={0.3}
        fade
        speed={0.3}
      />

      {/* Ground */}
      <mesh
        rotation={[-Math.PI / 2, 0, 0]}
        position={[0, -0.01, 0]}
        receiveShadow
      >
        <planeGeometry args={[80, 100]} />
        <meshStandardMaterial color="#1a2a1a" roughness={0.95} />
      </mesh>

      <River />
      <GlowPath />

      {/* Fitness stations along path */}
      <FitnessStation position={[5, 0, -15]} />
      <FitnessStation position={[10, 0, 5]} />
      <FitnessStation position={[3, 0, 20]} />

      <Runners />

      {/* Rest stations */}
      <RestStation position={[8, 0, -8]} rotation={0.3} />
      <RestStation position={[12, 0, 12]} rotation={-0.5} />
      <RestStation position={[2, 0, 28]} rotation={0.1} />
    </>
  );
}
