/**
 * ElementMeshes.tsx — 3D mesh components for every SPHERES design element type.
 *
 * Each mesh is built from simple but recognisable geometry using Three.js
 * primitives via React Three Fiber. Every mesh:
 *   - Accepts position, rotation, scale, and color from the design
 *   - Casts and receives shadows
 *   - Highlights on hover (emissive boost)
 *   - Shows its name via drei <Html> on hover
 */

import { useRef, useState, useMemo, type FC } from 'react';
import * as THREE from 'three';
import { useFrame } from '@react-three/fiber';
import { Html } from '@react-three/drei';
import type { Element3DProps } from '../../utils/designTo3D';

// ---------------------------------------------------------------------------
// Shared wrapper — hover highlight + name label
// ---------------------------------------------------------------------------

interface ElementWrapperProps {
  element: Element3DProps;
  onClick?: (id: string) => void;
  opacity?: number;
  children: React.ReactNode;
}

const ElementWrapper: FC<ElementWrapperProps> = ({
  element,
  onClick,
  opacity = 1,
  children,
}) => {
  const groupRef = useRef<THREE.Group>(null);
  const [hovered, setHovered] = useState(false);

  return (
    <group
      ref={groupRef}
      position={element.position}
      rotation={element.rotation}
      scale={element.scale}
      onPointerOver={(e) => {
        e.stopPropagation();
        setHovered(true);
        document.body.style.cursor = 'pointer';
      }}
      onPointerOut={(e) => {
        e.stopPropagation();
        setHovered(false);
        document.body.style.cursor = 'default';
      }}
      onClick={(e) => {
        e.stopPropagation();
        onClick?.(element.id);
      }}
    >
      {/* Hover glow shell */}
      {hovered && (
        <mesh>
          <sphereGeometry args={[1.5, 8, 8]} />
          <meshBasicMaterial
            color="#ffffff"
            transparent
            opacity={0.08}
            depthWrite={false}
          />
        </mesh>
      )}

      {/* Actual mesh content — wrapped in a group so we can set global opacity */}
      <group userData={{ opacity }}>
        {children}
      </group>

      {/* Floating label */}
      {hovered && (
        <Html
          center
          distanceFactor={40}
          style={{
            pointerEvents: 'none',
            background: 'rgba(0,0,0,0.78)',
            color: '#fff',
            padding: '4px 10px',
            borderRadius: '6px',
            fontSize: '13px',
            fontFamily: 'system-ui, sans-serif',
            whiteSpace: 'nowrap',
            fontWeight: 500,
            letterSpacing: '0.01em',
          }}
          position={[0, 4, 0]}
        >
          {element.name}
        </Html>
      )}
    </group>
  );
};

// ---------------------------------------------------------------------------
// Reusable material hook — standard shadow-casting material with hover tint
// ---------------------------------------------------------------------------

function useShadowMaterial(
  color: string,
  opts?: { emissive?: string; roughness?: number; metalness?: number; transparent?: boolean; opacity?: number },
) {
  return useMemo(() => {
    return new THREE.MeshStandardMaterial({
      color,
      emissive: opts?.emissive ?? '#000000',
      roughness: opts?.roughness ?? 0.75,
      metalness: opts?.metalness ?? 0.05,
      transparent: opts?.transparent ?? false,
      opacity: opts?.opacity ?? 1,
      side: THREE.DoubleSide,
    });
  }, [color, opts?.emissive, opts?.roughness, opts?.metalness, opts?.transparent, opts?.opacity]);
}

// Small helper for shadow-enabled mesh
const ShadowMesh: FC<{
  geometry: THREE.BufferGeometry;
  material: THREE.Material;
  position?: [number, number, number];
  rotation?: [number, number, number];
  scale?: [number, number, number];
}> = ({ geometry, material, position, rotation, scale }) => (
  <mesh
    geometry={geometry}
    material={material}
    position={position}
    rotation={rotation}
    scale={scale}
    castShadow
    receiveShadow
  />
);

// ---------------------------------------------------------------------------
// PERFORMANCE — Stages
// ---------------------------------------------------------------------------

const StageSmall: FC<{ color: string }> = ({ color }) => {
  const mat = useShadowMaterial(color, { roughness: 0.85 });
  const poleMat = useShadowMaterial('#3a2a1a', { roughness: 0.9 });
  return (
    <group>
      {/* Platform */}
      <mesh position={[0, -0.75, 0]} castShadow receiveShadow>
        <boxGeometry args={[10, 1.5, 8]} />
        <primitive object={mat} attach="material" />
      </mesh>
      {/* Four poles */}
      {[[-4.5, 4, -3.5], [4.5, 4, -3.5], [-4.5, 4, 3.5], [4.5, 4, 3.5]].map((pos, i) => (
        <mesh key={i} position={pos as [number, number, number]} castShadow>
          <cylinderGeometry args={[0.15, 0.15, 8, 8]} />
          <primitive object={poleMat} attach="material" />
        </mesh>
      ))}
      {/* Overhead frame */}
      <mesh position={[0, 8, 0]} castShadow>
        <boxGeometry args={[10, 0.3, 8]} />
        <primitive object={poleMat} attach="material" />
      </mesh>
    </group>
  );
};

const StageMedium: FC<{ color: string }> = ({ color }) => {
  const mat = useShadowMaterial(color, { roughness: 0.85 });
  const poleMat = useShadowMaterial('#3a2a1a', { roughness: 0.9 });
  return (
    <group>
      <mesh position={[0, -0.5, 0]} castShadow receiveShadow>
        <boxGeometry args={[16, 2, 12]} />
        <primitive object={mat} attach="material" />
      </mesh>
      {[[-7.5, 5, -5.5], [7.5, 5, -5.5], [-7.5, 5, 5.5], [7.5, 5, 5.5]].map((pos, i) => (
        <mesh key={i} position={pos as [number, number, number]} castShadow>
          <cylinderGeometry args={[0.2, 0.2, 10, 8]} />
          <primitive object={poleMat} attach="material" />
        </mesh>
      ))}
      <mesh position={[0, 10, 0]} castShadow>
        <boxGeometry args={[16, 0.4, 12]} />
        <primitive object={poleMat} attach="material" />
      </mesh>
    </group>
  );
};

const StageLarge: FC<{ color: string }> = ({ color }) => {
  const mat = useShadowMaterial(color, { roughness: 0.85 });
  const poleMat = useShadowMaterial('#3a2a1a', { roughness: 0.9 });
  return (
    <group>
      <mesh position={[0, -0.25, 0]} castShadow receiveShadow>
        <boxGeometry args={[24, 2.5, 16]} />
        <primitive object={mat} attach="material" />
      </mesh>
      {[[-11.5, 6, -7.5], [11.5, 6, -7.5], [-11.5, 6, 7.5], [11.5, 6, 7.5], [0, 6, -7.5], [0, 6, 7.5]].map((pos, i) => (
        <mesh key={i} position={pos as [number, number, number]} castShadow>
          <cylinderGeometry args={[0.25, 0.25, 12, 8]} />
          <primitive object={poleMat} attach="material" />
        </mesh>
      ))}
      <mesh position={[0, 12, 0]} castShadow>
        <boxGeometry args={[24, 0.5, 16]} />
        <primitive object={poleMat} attach="material" />
      </mesh>
    </group>
  );
};

const SoundEquipment: FC<{ color: string }> = ({ color }) => {
  const mat = useShadowMaterial('#1a1a1a', { roughness: 0.6, metalness: 0.3 });
  const grillMat = useShadowMaterial(color, { metalness: 0.5 });
  return (
    <group>
      {/* Speaker stack */}
      <mesh position={[0, -1, 0]} castShadow receiveShadow>
        <boxGeometry args={[3, 2, 2.5]} />
        <primitive object={mat} attach="material" />
      </mesh>
      <mesh position={[0, 1, 0]} castShadow>
        <boxGeometry args={[3, 2, 2.5]} />
        <primitive object={mat} attach="material" />
      </mesh>
      <mesh position={[0, 3, 0]} castShadow>
        <boxGeometry args={[2.5, 1.5, 2]} />
        <primitive object={mat} attach="material" />
      </mesh>
      {/* Speaker grills */}
      <mesh position={[0, -1, 1.26]} castShadow>
        <circleGeometry args={[0.8, 16]} />
        <primitive object={grillMat} attach="material" />
      </mesh>
      <mesh position={[0, 1, 1.26]} castShadow>
        <circleGeometry args={[0.8, 16]} />
        <primitive object={grillMat} attach="material" />
      </mesh>
      {/* Stand */}
      <mesh position={[0, -2.5, 0]} castShadow>
        <cylinderGeometry args={[0.1, 0.8, 1, 8]} />
        <primitive object={mat} attach="material" />
      </mesh>
    </group>
  );
};

const ScreeningWall: FC<{ color: string }> = ({ color }) => {
  const mat = useShadowMaterial('#f0f0f0', { roughness: 0.4, transparent: true, opacity: 0.92 });
  const frameMat = useShadowMaterial(color, { metalness: 0.3 });
  return (
    <group>
      {/* Screen surface */}
      <mesh position={[0, 0, 0]} castShadow receiveShadow>
        <boxGeometry args={[16, 10, 0.3]} />
        <primitive object={mat} attach="material" />
      </mesh>
      {/* Frame */}
      <mesh position={[0, -5.2, 0]} castShadow>
        <boxGeometry args={[16.5, 0.4, 0.5]} />
        <primitive object={frameMat} attach="material" />
      </mesh>
      <mesh position={[0, 5.2, 0]} castShadow>
        <boxGeometry args={[16.5, 0.4, 0.5]} />
        <primitive object={frameMat} attach="material" />
      </mesh>
      {/* Support legs */}
      {[-7, 0, 7].map((x, i) => (
        <mesh key={i} position={[x, -7, 0]} castShadow>
          <boxGeometry args={[0.4, 4, 1.5]} />
          <primitive object={frameMat} attach="material" />
        </mesh>
      ))}
    </group>
  );
};

// ---------------------------------------------------------------------------
// SEATING
// ---------------------------------------------------------------------------

const Bench: FC<{ color: string }> = ({ color }) => {
  const woodMat = useShadowMaterial(color, { roughness: 0.85 });
  const legMat = useShadowMaterial('#555555', { metalness: 0.4 });
  return (
    <group>
      {/* Seat */}
      <mesh position={[0, 0, 0]} castShadow receiveShadow>
        <boxGeometry args={[5, 0.3, 1.5]} />
        <primitive object={woodMat} attach="material" />
      </mesh>
      {/* Backrest */}
      <mesh position={[0, 0.8, -0.65]} castShadow rotation={[0.15, 0, 0]}>
        <boxGeometry args={[5, 1.3, 0.2]} />
        <primitive object={woodMat} attach="material" />
      </mesh>
      {/* Legs */}
      {[[-2, -0.9, 0.5], [2, -0.9, 0.5], [-2, -0.9, -0.5], [2, -0.9, -0.5]].map((pos, i) => (
        <mesh key={i} position={pos as [number, number, number]} castShadow>
          <boxGeometry args={[0.15, 1.5, 0.15]} />
          <primitive object={legMat} attach="material" />
        </mesh>
      ))}
    </group>
  );
};

const PicnicTable: FC<{ color: string }> = ({ color }) => {
  const mat = useShadowMaterial(color, { roughness: 0.9 });
  return (
    <group>
      {/* Table top */}
      <mesh position={[0, 0.3, 0]} castShadow receiveShadow>
        <boxGeometry args={[6, 0.25, 2.5]} />
        <primitive object={mat} attach="material" />
      </mesh>
      {/* Bench seats */}
      <mesh position={[0, -0.3, -2]} castShadow receiveShadow>
        <boxGeometry args={[6, 0.2, 1]} />
        <primitive object={mat} attach="material" />
      </mesh>
      <mesh position={[0, -0.3, 2]} castShadow receiveShadow>
        <boxGeometry args={[6, 0.2, 1]} />
        <primitive object={mat} attach="material" />
      </mesh>
      {/* A-frame legs */}
      {[-2, 2].map((x, i) => (
        <group key={i} position={[x, -1, 0]}>
          <mesh rotation={[0, 0, 0.2]} castShadow>
            <boxGeometry args={[0.2, 2, 0.2]} />
            <primitive object={mat} attach="material" />
          </mesh>
          <mesh rotation={[0, 0, -0.2]} castShadow>
            <boxGeometry args={[0.2, 2, 0.2]} />
            <primitive object={mat} attach="material" />
          </mesh>
          {/* Cross brace */}
          <mesh position={[0, -0.5, 0]} castShadow>
            <boxGeometry args={[1.5, 0.15, 0.15]} />
            <primitive object={mat} attach="material" />
          </mesh>
        </group>
      ))}
    </group>
  );
};

const ChairCluster: FC<{ color: string }> = ({ color }) => {
  const mat = useShadowMaterial(color, { roughness: 0.7 });
  const positions: [number, number, number][] = [
    [0, 0, -1.5],
    [1.3, 0, -0.75],
    [1.3, 0, 0.75],
    [0, 0, 1.5],
    [-1.3, 0, 0.75],
    [-1.3, 0, -0.75],
  ];
  return (
    <group>
      {positions.map((pos, i) => (
        <group key={i} position={pos}>
          {/* Seat cube */}
          <mesh position={[0, -0.5, 0]} castShadow receiveShadow>
            <boxGeometry args={[1.2, 1.2, 1.2]} />
            <primitive object={mat} attach="material" />
          </mesh>
        </group>
      ))}
    </group>
  );
};

const Bleachers: FC<{ color: string }> = ({ color }) => {
  const mat = useShadowMaterial(color, { metalness: 0.2 });
  const rows = 4;
  return (
    <group>
      {Array.from({ length: rows }, (_, i) => (
        <mesh
          key={i}
          position={[0, i * 1.5 - 2, i * 1.2 - 2]}
          castShadow
          receiveShadow
        >
          <boxGeometry args={[12, 0.3, 2]} />
          <primitive object={mat} attach="material" />
        </mesh>
      ))}
      {/* Support structure */}
      {[-5.5, 0, 5.5].map((x, i) => (
        <mesh key={i} position={[x, 0, -0.5]} castShadow>
          <boxGeometry args={[0.3, 8, 6]} />
          <meshStandardMaterial color="#666666" metalness={0.3} roughness={0.6} transparent opacity={0.3} />
        </mesh>
      ))}
    </group>
  );
};

const AmphitheaterSeating: FC<{ color: string }> = ({ color }) => {
  const mat = useShadowMaterial(color, { roughness: 0.8 });
  const tiers = 5;
  return (
    <group>
      {Array.from({ length: tiers }, (_, i) => {
        const radius = 8 + i * 2;
        const tierY = i * 1.2 - 2;
        return (
          <mesh key={i} position={[0, tierY, i * 1.5]} castShadow receiveShadow>
            <cylinderGeometry args={[radius, radius, 0.4, 32, 1, false, 0, Math.PI]} />
            <primitive object={mat} attach="material" />
          </mesh>
        );
      })}
    </group>
  );
};

// ---------------------------------------------------------------------------
// FOOD & VENDOR
// ---------------------------------------------------------------------------

const FoodCart: FC<{ color: string }> = ({ color }) => {
  const bodyMat = useShadowMaterial(color, { roughness: 0.6 });
  const metalMat = useShadowMaterial('#cccccc', { metalness: 0.6 });
  const umbMat = useShadowMaterial('#dd3333', { roughness: 0.5 });
  return (
    <group>
      {/* Cart body */}
      <mesh position={[0, -0.3, 0]} castShadow receiveShadow>
        <boxGeometry args={[3, 2.5, 2]} />
        <primitive object={bodyMat} attach="material" />
      </mesh>
      {/* Wheels */}
      {[[-1.2, -1.7, 1.1], [1.2, -1.7, 1.1]].map((pos, i) => (
        <mesh key={i} position={pos as [number, number, number]} rotation={[Math.PI / 2, 0, 0]} castShadow>
          <cylinderGeometry args={[0.5, 0.5, 0.2, 16]} />
          <primitive object={metalMat} attach="material" />
        </mesh>
      ))}
      {/* Umbrella pole */}
      <mesh position={[0, 2.5, 0]} castShadow>
        <cylinderGeometry args={[0.06, 0.06, 4, 8]} />
        <primitive object={metalMat} attach="material" />
      </mesh>
      {/* Umbrella */}
      <mesh position={[0, 4.5, 0]} castShadow>
        <coneGeometry args={[2.5, 1, 8]} />
        <primitive object={umbMat} attach="material" />
      </mesh>
    </group>
  );
};

const FoodTruckSpace: FC<{ color: string }> = ({ color }) => {
  const bodyMat = useShadowMaterial(color, { roughness: 0.5, metalness: 0.2 });
  const wheelMat = useShadowMaterial('#222222', { roughness: 0.9 });
  const windowMat = useShadowMaterial('#88ccff', { roughness: 0.2, metalness: 0.5, transparent: true, opacity: 0.6 });
  return (
    <group>
      {/* Truck body */}
      <mesh position={[0, 0, 0]} castShadow receiveShadow>
        <boxGeometry args={[8, 5, 4]} />
        <primitive object={bodyMat} attach="material" />
      </mesh>
      {/* Cab */}
      <mesh position={[5, -0.5, 0]} castShadow>
        <boxGeometry args={[3, 4, 3.8]} />
        <primitive object={bodyMat} attach="material" />
      </mesh>
      {/* Serving window */}
      <mesh position={[0, 0.5, 2.01]} castShadow>
        <boxGeometry args={[4, 2.5, 0.1]} />
        <primitive object={windowMat} attach="material" />
      </mesh>
      {/* Wheels */}
      {[[-2, -3, 2.1], [-2, -3, -2.1], [4, -3, 2.1], [4, -3, -2.1]].map((pos, i) => (
        <mesh key={i} position={pos as [number, number, number]} rotation={[Math.PI / 2, 0, 0]} castShadow>
          <cylinderGeometry args={[0.7, 0.7, 0.4, 16]} />
          <primitive object={wheelMat} attach="material" />
        </mesh>
      ))}
      {/* Ground marking */}
      <mesh position={[0, -3.45, 0]} rotation={[-Math.PI / 2, 0, 0]} receiveShadow>
        <planeGeometry args={[12, 6]} />
        <meshStandardMaterial color="#ffcc00" transparent opacity={0.3} />
      </mesh>
    </group>
  );
};

const MarketStall: FC<{ color: string }> = ({ color }) => {
  const frameMat = useShadowMaterial('#8B4513', { roughness: 0.9 });
  const canopyMat = useShadowMaterial(color, { roughness: 0.6, transparent: true, opacity: 0.9 });
  const counterMat = useShadowMaterial('#D2B48C', { roughness: 0.85 });
  return (
    <group>
      {/* Counter */}
      <mesh position={[0, -1, 0]} castShadow receiveShadow>
        <boxGeometry args={[6, 2.5, 3]} />
        <primitive object={counterMat} attach="material" />
      </mesh>
      {/* Poles */}
      {[[-2.8, 2, -1.3], [2.8, 2, -1.3], [-2.8, 2, 1.3], [2.8, 2, 1.3]].map((pos, i) => (
        <mesh key={i} position={pos as [number, number, number]} castShadow>
          <cylinderGeometry args={[0.1, 0.1, 6.5, 8]} />
          <primitive object={frameMat} attach="material" />
        </mesh>
      ))}
      {/* Canopy */}
      <mesh position={[0, 5, 0]} castShadow>
        <boxGeometry args={[7, 0.15, 4]} />
        <primitive object={canopyMat} attach="material" />
      </mesh>
    </group>
  );
};

const VendorTent: FC<{ color: string }> = ({ color }) => {
  const tentMat = useShadowMaterial(color, { roughness: 0.5, transparent: true, opacity: 0.85 });
  const poleMat = useShadowMaterial('#888888', { metalness: 0.5 });
  return (
    <group>
      {/* Tent canopy — pyramid shape */}
      <mesh position={[0, 3.5, 0]} castShadow>
        <coneGeometry args={[5, 4, 4]} />
        <primitive object={tentMat} attach="material" />
      </mesh>
      {/* Poles */}
      {[[-3.2, 0, -3.2], [3.2, 0, -3.2], [-3.2, 0, 3.2], [3.2, 0, 3.2]].map((pos, i) => (
        <mesh key={i} position={pos as [number, number, number]} castShadow>
          <cylinderGeometry args={[0.08, 0.08, 7, 8]} />
          <primitive object={poleMat} attach="material" />
        </mesh>
      ))}
    </group>
  );
};

// ---------------------------------------------------------------------------
// GARDENS & NATURE
// ---------------------------------------------------------------------------

const RaisedBed: FC<{ color: string }> = ({ color }) => {
  const woodMat = useShadowMaterial(color, { roughness: 0.9 });
  const soilMat = useShadowMaterial('#5a3a1a');
  const greenMat = useShadowMaterial('#3a8a3a');
  return (
    <group>
      {/* Wooden frame */}
      <mesh position={[0, -0.5, 0]} castShadow receiveShadow>
        <boxGeometry args={[4, 1.5, 4]} />
        <primitive object={woodMat} attach="material" />
      </mesh>
      {/* Soil */}
      <mesh position={[0, 0.2, 0]} receiveShadow>
        <boxGeometry args={[3.6, 0.4, 3.6]} />
        <primitive object={soilMat} attach="material" />
      </mesh>
      {/* Plants — small spheres */}
      {[[-1, 0.7, -1], [1, 0.7, -1], [0, 0.8, 0], [-1, 0.7, 1], [1, 0.7, 1]].map((pos, i) => (
        <mesh key={i} position={pos as [number, number, number]} castShadow>
          <sphereGeometry args={[0.4 + Math.random() * 0.2, 8, 8]} />
          <primitive object={greenMat} attach="material" />
        </mesh>
      ))}
    </group>
  );
};

const TreePlanting: FC<{ color: string }> = ({ color }) => {
  const trunkMat = useShadowMaterial('#6B4226', { roughness: 0.95 });
  const leafMat = useShadowMaterial(color !== '#888888' ? color : '#2d7a2d', { roughness: 0.8 });
  // Generate a small grove of 3 trees at varying positions
  const trees: { x: number; z: number; h: number; r: number }[] = [
    { x: 0, z: 0, h: 12, r: 3.5 },
    { x: -3, z: 2, h: 9, r: 2.8 },
    { x: 2.5, z: -1.5, h: 10, r: 3 },
  ];
  return (
    <group>
      {trees.map((tree, i) => (
        <group key={i} position={[tree.x, 0, tree.z]}>
          {/* Trunk */}
          <mesh position={[0, tree.h / 2 - 3.5, 0]} castShadow>
            <cylinderGeometry args={[0.3, 0.5, tree.h * 0.6, 8]} />
            <primitive object={trunkMat} attach="material" />
          </mesh>
          {/* Canopy — layered spheres */}
          <mesh position={[0, tree.h - 3, 0]} castShadow>
            <sphereGeometry args={[tree.r, 12, 12]} />
            <primitive object={leafMat} attach="material" />
          </mesh>
          <mesh position={[0, tree.h - 1, 0]} castShadow>
            <sphereGeometry args={[tree.r * 0.7, 10, 10]} />
            <primitive object={leafMat} attach="material" />
          </mesh>
        </group>
      ))}
    </group>
  );
};

const FlowerGarden: FC<{ color: string }> = ({ color }) => {
  const groundMat = useShadowMaterial('#4a7a3a', { roughness: 0.95 });
  const flowerColors = ['#ff4466', '#ffaa22', '#ff66cc', '#aa44ff', '#44aaff', '#ffff44'];
  return (
    <group>
      {/* Ground cover */}
      <mesh position={[0, -0.75, 0]} receiveShadow>
        <boxGeometry args={[6, 0.5, 6]} />
        <primitive object={groundMat} attach="material" />
      </mesh>
      {/* Flowers — coloured dots */}
      {Array.from({ length: 20 }, (_, i) => {
        const x = (Math.random() - 0.5) * 5;
        const z = (Math.random() - 0.5) * 5;
        const fc = flowerColors[i % flowerColors.length];
        return (
          <mesh key={i} position={[x, -0.3, z]} castShadow>
            <sphereGeometry args={[0.15, 6, 6]} />
            <meshStandardMaterial color={fc} emissive={fc} emissiveIntensity={0.2} />
          </mesh>
        );
      })}
    </group>
  );
};

const NativeMeadow: FC<{ color: string }> = ({ color }) => {
  const grassMat = useShadowMaterial(color !== '#888888' ? color : '#5a9a3a', { roughness: 0.95 });
  return (
    <group>
      <mesh position={[0, -0.5, 0]} receiveShadow>
        <boxGeometry args={[10, 0.6, 10]} />
        <primitive object={grassMat} attach="material" />
      </mesh>
      {/* Grass tufts */}
      {Array.from({ length: 30 }, (_, i) => {
        const x = (Math.random() - 0.5) * 9;
        const z = (Math.random() - 0.5) * 9;
        const h = 0.5 + Math.random() * 1;
        return (
          <mesh key={i} position={[x, -0.2 + h / 2, z]} castShadow>
            <coneGeometry args={[0.12, h, 4]} />
            <meshStandardMaterial color="#6aaa4a" roughness={0.9} />
          </mesh>
        );
      })}
      {/* Wildflower dots */}
      {Array.from({ length: 12 }, (_, i) => {
        const x = (Math.random() - 0.5) * 8;
        const z = (Math.random() - 0.5) * 8;
        const fc = ['#ff6688', '#ffcc33', '#cc66ff'][i % 3];
        return (
          <mesh key={`f${i}`} position={[x, 0.2, z]}>
            <sphereGeometry args={[0.1, 6, 6]} />
            <meshStandardMaterial color={fc} emissive={fc} emissiveIntensity={0.3} />
          </mesh>
        );
      })}
    </group>
  );
};

const WaterFeature: FC<{ color: string }> = ({ color }) => {
  const ref = useRef<THREE.Mesh>(null);

  useFrame(({ clock }) => {
    if (ref.current) {
      const mat = ref.current.material as THREE.MeshStandardMaterial;
      mat.emissiveIntensity = 0.1 + Math.sin(clock.getElapsedTime() * 2) * 0.05;
      // Gentle undulation
      ref.current.position.y = -0.6 + Math.sin(clock.getElapsedTime() * 1.5) * 0.03;
    }
  });

  return (
    <group>
      {/* Basin */}
      <mesh position={[0, -1, 0]} castShadow receiveShadow>
        <cylinderGeometry args={[3, 3.3, 1, 24]} />
        <meshStandardMaterial color="#888888" roughness={0.8} />
      </mesh>
      {/* Water surface */}
      <mesh ref={ref} position={[0, -0.6, 0]} receiveShadow>
        <circleGeometry args={[2.8, 32]} />
        <meshStandardMaterial
          color={color !== '#888888' ? color : '#3388cc'}
          emissive="#2266aa"
          emissiveIntensity={0.1}
          roughness={0.1}
          metalness={0.8}
          transparent
          opacity={0.7}
        />
      </mesh>
    </group>
  );
};

// ---------------------------------------------------------------------------
// ART
// ---------------------------------------------------------------------------

const MuralWall: FC<{ color: string }> = ({ color }) => {
  const wallMat = useShadowMaterial('#f5f0e8', { roughness: 0.6 });
  // Simulate mural with colourful patches
  const patches = useMemo(() => {
    const cols = [color, '#ff6644', '#44aaff', '#ffcc22', '#66dd66', '#cc44ff'];
    return Array.from({ length: 12 }, (_, i) => ({
      x: (Math.random() - 0.5) * 10,
      y: (Math.random() - 0.5) * 8,
      w: 1 + Math.random() * 3,
      h: 1 + Math.random() * 3,
      c: cols[i % cols.length],
    }));
  }, [color]);

  return (
    <group>
      {/* Wall */}
      <mesh position={[0, 0, 0]} castShadow receiveShadow>
        <boxGeometry args={[12, 12, 0.6]} />
        <primitive object={wallMat} attach="material" />
      </mesh>
      {/* Mural patches */}
      {patches.map((p, i) => (
        <mesh key={i} position={[p.x, p.y, 0.32]}>
          <planeGeometry args={[p.w, p.h]} />
          <meshStandardMaterial color={p.c} roughness={0.5} />
        </mesh>
      ))}
    </group>
  );
};

const SculpturePad: FC<{ color: string }> = ({ color }) => {
  const baseMat = useShadowMaterial('#cccccc', { roughness: 0.5, metalness: 0.2 });
  const sculptMat = useShadowMaterial(color, { roughness: 0.3, metalness: 0.6 });
  return (
    <group>
      {/* Pedestal */}
      <mesh position={[0, -2.5, 0]} castShadow receiveShadow>
        <cylinderGeometry args={[1.5, 1.8, 3, 8]} />
        <primitive object={baseMat} attach="material" />
      </mesh>
      {/* Abstract sculpture — stacked geometric shapes */}
      <mesh position={[0, 0.5, 0]} castShadow rotation={[0.3, 0.5, 0.2]}>
        <dodecahedronGeometry args={[1.5, 0]} />
        <primitive object={sculptMat} attach="material" />
      </mesh>
      <mesh position={[0.5, 2.5, 0]} castShadow rotation={[0, 0.8, 0.4]}>
        <octahedronGeometry args={[1, 0]} />
        <primitive object={sculptMat} attach="material" />
      </mesh>
    </group>
  );
};

const InteractiveArt: FC<{ color: string }> = ({ color }) => {
  const groupRef = useRef<THREE.Group>(null);

  useFrame(({ clock }) => {
    if (groupRef.current) {
      groupRef.current.rotation.y = clock.getElapsedTime() * 0.3;
      groupRef.current.children.forEach((child, i) => {
        child.position.y = Math.sin(clock.getElapsedTime() * 1.5 + i * 1.2) * 0.5;
      });
    }
  });

  const glowMat = useMemo(
    () =>
      new THREE.MeshStandardMaterial({
        color,
        emissive: color,
        emissiveIntensity: 0.5,
        roughness: 0.2,
        metalness: 0.8,
        transparent: true,
        opacity: 0.85,
      }),
    [color],
  );

  return (
    <group ref={groupRef}>
      {/* Central pole */}
      <mesh position={[0, 0, 0]} castShadow>
        <cylinderGeometry args={[0.1, 0.1, 8, 8]} />
        <meshStandardMaterial color="#888888" metalness={0.5} roughness={0.4} />
      </mesh>
      {/* Floating geometric shapes */}
      {[
        { pos: [1.5, 1, 0] as [number, number, number], geo: 'ico' },
        { pos: [-1, 2.5, 1] as [number, number, number], geo: 'octa' },
        { pos: [0.5, -0.5, -1.5] as [number, number, number], geo: 'tetra' },
        { pos: [-0.8, -2, 0.8] as [number, number, number], geo: 'dodeca' },
      ].map((item, i) => (
        <mesh key={i} position={item.pos} castShadow>
          {item.geo === 'ico' && <icosahedronGeometry args={[0.6, 0]} />}
          {item.geo === 'octa' && <octahedronGeometry args={[0.5, 0]} />}
          {item.geo === 'tetra' && <tetrahedronGeometry args={[0.55, 0]} />}
          {item.geo === 'dodeca' && <dodecahedronGeometry args={[0.5, 0]} />}
          <primitive object={glowMat} attach="material" />
        </mesh>
      ))}
      {/* Point light for glow */}
      <pointLight color={color} intensity={2} distance={12} decay={2} />
    </group>
  );
};

const ArtInstallation: FC<{ color: string }> = ({ color }) => {
  const groupRef = useRef<THREE.Group>(null);

  useFrame(({ clock }) => {
    if (groupRef.current) {
      groupRef.current.rotation.y = Math.sin(clock.getElapsedTime() * 0.2) * 0.3;
    }
  });

  const mat = useMemo(
    () =>
      new THREE.MeshStandardMaterial({
        color,
        emissive: color,
        emissiveIntensity: 0.15,
        roughness: 0.4,
        metalness: 0.3,
        side: THREE.DoubleSide,
      }),
    [color],
  );

  return (
    <group ref={groupRef}>
      {/* Large abstract form — twisted torus + intersecting planes */}
      <mesh position={[0, 1, 0]} castShadow rotation={[0.5, 0, 0.3]}>
        <torusKnotGeometry args={[3, 0.8, 64, 12]} />
        <primitive object={mat} attach="material" />
      </mesh>
    </group>
  );
};

// ---------------------------------------------------------------------------
// RECREATION
// ---------------------------------------------------------------------------

const PlayStructure: FC<{ color: string }> = ({ color }) => {
  const frameMat = useShadowMaterial(color, { roughness: 0.5, metalness: 0.3 });
  const platformMat = useShadowMaterial('#D2B48C', { roughness: 0.85 });
  return (
    <group>
      {/* Main platform */}
      <mesh position={[0, 1, 0]} castShadow receiveShadow>
        <boxGeometry args={[5, 0.3, 5]} />
        <primitive object={platformMat} attach="material" />
      </mesh>
      {/* Four corner poles */}
      {[[-2.2, 3, -2.2], [2.2, 3, -2.2], [-2.2, 3, 2.2], [2.2, 3, 2.2]].map((pos, i) => (
        <mesh key={i} position={pos as [number, number, number]} castShadow>
          <cylinderGeometry args={[0.12, 0.12, 6, 8]} />
          <primitive object={frameMat} attach="material" />
        </mesh>
      ))}
      {/* Roof */}
      <mesh position={[0, 6, 0]} castShadow>
        <coneGeometry args={[3.5, 2, 4]} />
        <primitive object={frameMat} attach="material" />
      </mesh>
      {/* Slide */}
      <mesh position={[3.5, -0.5, 0]} rotation={[0, 0, -0.5]} castShadow>
        <boxGeometry args={[0.2, 4, 1.5]} />
        <meshStandardMaterial color="#ffcc00" roughness={0.3} metalness={0.4} />
      </mesh>
      {/* Climbing bars */}
      {Array.from({ length: 4 }, (_, i) => (
        <mesh key={`bar${i}`} position={[-2.6, i * 1 + 0.5, 0]} rotation={[0, 0, Math.PI / 2]} castShadow>
          <cylinderGeometry args={[0.08, 0.08, 2, 8]} />
          <primitive object={frameMat} attach="material" />
        </mesh>
      ))}
    </group>
  );
};

const BasketballHalf: FC<{ color: string }> = ({ color }) => {
  const courtMat = useShadowMaterial(color !== '#888888' ? color : '#cc6633', { roughness: 0.7 });
  const poleMat = useShadowMaterial('#888888', { metalness: 0.6 });
  return (
    <group>
      {/* Court surface */}
      <mesh position={[0, -1.45, 0]} rotation={[-Math.PI / 2, 0, 0]} receiveShadow>
        <planeGeometry args={[20, 15]} />
        <primitive object={courtMat} attach="material" />
      </mesh>
      {/* Court lines */}
      <mesh position={[0, -1.44, 0]} rotation={[-Math.PI / 2, 0, 0]}>
        <ringGeometry args={[5.8, 6, 32]} />
        <meshStandardMaterial color="#ffffff" />
      </mesh>
      {/* Hoop pole */}
      <mesh position={[0, 2, -7]} castShadow>
        <cylinderGeometry args={[0.2, 0.2, 10, 8]} />
        <primitive object={poleMat} attach="material" />
      </mesh>
      {/* Backboard */}
      <mesh position={[0, 6, -6.5]} castShadow>
        <boxGeometry args={[4, 3, 0.15]} />
        <meshStandardMaterial color="#ffffff" roughness={0.3} transparent opacity={0.85} />
      </mesh>
      {/* Rim */}
      <mesh position={[0, 5, -6]} rotation={[Math.PI / 2, 0, 0]} castShadow>
        <torusGeometry args={[0.6, 0.05, 8, 16]} />
        <meshStandardMaterial color="#ff4400" metalness={0.7} roughness={0.3} />
      </mesh>
    </group>
  );
};

const FitnessStation: FC<{ color: string }> = ({ color }) => {
  const mat = useShadowMaterial(color, { metalness: 0.5, roughness: 0.4 });
  return (
    <group>
      {/* Ground pad */}
      <mesh position={[0, -1.45, 0]} receiveShadow>
        <boxGeometry args={[8, 0.1, 6]} />
        <meshStandardMaterial color="#555555" roughness={0.9} />
      </mesh>
      {/* Pull-up bar frame */}
      {/* Vertical posts */}
      {[[-3, 1.5, 0], [3, 1.5, 0]].map((pos, i) => (
        <mesh key={i} position={pos as [number, number, number]} castShadow>
          <cylinderGeometry args={[0.12, 0.12, 7, 8]} />
          <primitive object={mat} attach="material" />
        </mesh>
      ))}
      {/* Top bar */}
      <mesh position={[0, 5, 0]} rotation={[0, 0, Math.PI / 2]} castShadow>
        <cylinderGeometry args={[0.1, 0.1, 6, 8]} />
        <primitive object={mat} attach="material" />
      </mesh>
      {/* Dip bars */}
      {[-1, 1].map((x, i) => (
        <group key={`dip${i}`} position={[x, 0, 2.5]}>
          <mesh position={[0, 0, 0]} castShadow>
            <cylinderGeometry args={[0.08, 0.08, 4, 8]} />
            <primitive object={mat} attach="material" />
          </mesh>
          <mesh position={[0, 2, 0.5]} rotation={[Math.PI / 2, 0, 0]} castShadow>
            <cylinderGeometry args={[0.06, 0.06, 2, 8]} />
            <primitive object={mat} attach="material" />
          </mesh>
        </group>
      ))}
    </group>
  );
};

const SportsField: FC<{ color: string }> = ({ color }) => {
  const fieldMat = useShadowMaterial(color !== '#888888' ? color : '#4a8a3a', { roughness: 0.95 });
  return (
    <group>
      {/* Field surface */}
      <mesh position={[0, -1.45, 0]} rotation={[-Math.PI / 2, 0, 0]} receiveShadow>
        <planeGeometry args={[30, 20]} />
        <primitive object={fieldMat} attach="material" />
      </mesh>
      {/* Field lines */}
      <mesh position={[0, -1.44, 0]} rotation={[-Math.PI / 2, 0, 0]}>
        <ringGeometry args={[4.8, 5, 32]} />
        <meshStandardMaterial color="#ffffff" />
      </mesh>
      {/* Center line */}
      <mesh position={[0, -1.44, 0]} rotation={[-Math.PI / 2, 0, 0]}>
        <planeGeometry args={[0.15, 20]} />
        <meshStandardMaterial color="#ffffff" />
      </mesh>
      {/* Goals */}
      {[-15, 15].map((x, i) => (
        <group key={i} position={[x, 0.5, 0]}>
          {/* Posts */}
          <mesh position={[-0.1, 0, -2.5]} castShadow>
            <cylinderGeometry args={[0.08, 0.08, 5, 8]} />
            <meshStandardMaterial color="#ffffff" />
          </mesh>
          <mesh position={[-0.1, 0, 2.5]} castShadow>
            <cylinderGeometry args={[0.08, 0.08, 5, 8]} />
            <meshStandardMaterial color="#ffffff" />
          </mesh>
          {/* Crossbar */}
          <mesh position={[-0.1, 2.5, 0]} rotation={[Math.PI / 2, 0, 0]} castShadow>
            <cylinderGeometry args={[0.06, 0.06, 5, 8]} />
            <meshStandardMaterial color="#ffffff" />
          </mesh>
        </group>
      ))}
    </group>
  );
};

// ---------------------------------------------------------------------------
// INFRASTRUCTURE
// ---------------------------------------------------------------------------

const Pathway: FC<{ color: string }> = ({ color }) => {
  const mat = useShadowMaterial(color !== '#888888' ? color : '#b8a88a', { roughness: 0.9 });
  return (
    <group>
      <mesh position={[0, -1.43, 0]} rotation={[-Math.PI / 2, 0, 0]} receiveShadow>
        <planeGeometry args={[4, 20]} />
        <primitive object={mat} attach="material" />
      </mesh>
      {/* Subtle edge stones */}
      {Array.from({ length: 10 }, (_, i) => (
        <mesh key={i} position={[2.1, -1.4, -9 + i * 2]} receiveShadow>
          <boxGeometry args={[0.3, 0.05, 1.8]} />
          <meshStandardMaterial color="#999999" roughness={0.95} />
        </mesh>
      ))}
    </group>
  );
};

const Fencing: FC<{ color: string }> = ({ color }) => {
  const postMat = useShadowMaterial(color !== '#888888' ? color : '#8B4513', { roughness: 0.85 });
  const railMat = useShadowMaterial(color !== '#888888' ? color : '#A0522D', { roughness: 0.85 });
  const postCount = 6;
  const spacing = 4;
  const totalLength = (postCount - 1) * spacing;
  return (
    <group>
      {Array.from({ length: postCount }, (_, i) => {
        const x = -totalLength / 2 + i * spacing;
        return (
          <group key={i}>
            {/* Post */}
            <mesh position={[x, 0, 0]} castShadow>
              <boxGeometry args={[0.3, 5, 0.3]} />
              <primitive object={postMat} attach="material" />
            </mesh>
            {/* Rails */}
            {i < postCount - 1 && (
              <>
                <mesh position={[x + spacing / 2, 1, 0]} castShadow>
                  <boxGeometry args={[spacing, 0.2, 0.15]} />
                  <primitive object={railMat} attach="material" />
                </mesh>
                <mesh position={[x + spacing / 2, -0.5, 0]} castShadow>
                  <boxGeometry args={[spacing, 0.2, 0.15]} />
                  <primitive object={railMat} attach="material" />
                </mesh>
              </>
            )}
          </group>
        );
      })}
    </group>
  );
};

const LightingPole: FC<{ color: string }> = ({ color }) => {
  const poleMat = useShadowMaterial('#555555', { metalness: 0.5, roughness: 0.4 });
  return (
    <group>
      {/* Pole */}
      <mesh position={[0, 0, 0]} castShadow>
        <cylinderGeometry args={[0.15, 0.25, 14, 8]} />
        <primitive object={poleMat} attach="material" />
      </mesh>
      {/* Light globe */}
      <mesh position={[0, 7.5, 0]}>
        <sphereGeometry args={[0.6, 16, 16]} />
        <meshStandardMaterial
          color={color !== '#888888' ? color : '#ffffdd'}
          emissive="#ffffaa"
          emissiveIntensity={1.5}
          transparent
          opacity={0.9}
        />
      </mesh>
      {/* Actual point light */}
      <pointLight
        position={[0, 7.5, 0]}
        color="#ffffcc"
        intensity={8}
        distance={25}
        decay={2}
        castShadow
      />
      {/* Base */}
      <mesh position={[0, -6.8, 0]} castShadow>
        <cylinderGeometry args={[0.6, 0.8, 0.6, 8]} />
        <primitive object={poleMat} attach="material" />
      </mesh>
    </group>
  );
};

const PowerHookup: FC<{ color: string }> = ({ color }) => {
  const mat = useShadowMaterial(color !== '#888888' ? color : '#666666', { metalness: 0.3, roughness: 0.6 });
  return (
    <group>
      <mesh position={[0, -0.5, 0]} castShadow receiveShadow>
        <boxGeometry args={[1.5, 1.5, 1.5]} />
        <primitive object={mat} attach="material" />
      </mesh>
      {/* Indicator light */}
      <mesh position={[0, 0.4, 0.76]}>
        <sphereGeometry args={[0.12, 8, 8]} />
        <meshStandardMaterial color="#44ff44" emissive="#44ff44" emissiveIntensity={2} />
      </mesh>
    </group>
  );
};

const WaterHookup: FC<{ color: string }> = ({ color }) => {
  const mat = useShadowMaterial(color !== '#888888' ? color : '#4488aa', { metalness: 0.4, roughness: 0.5 });
  return (
    <group>
      <mesh position={[0, -0.5, 0]} castShadow receiveShadow>
        <boxGeometry args={[1.5, 1.5, 1.5]} />
        <primitive object={mat} attach="material" />
      </mesh>
      {/* Pipe sticking up */}
      <mesh position={[0, 0.6, 0]} castShadow>
        <cylinderGeometry args={[0.12, 0.12, 1.2, 8]} />
        <primitive object={mat} attach="material" />
      </mesh>
      {/* Valve wheel */}
      <mesh position={[0, 1.2, 0]} rotation={[Math.PI / 2, 0, 0]} castShadow>
        <torusGeometry args={[0.25, 0.04, 8, 12]} />
        <meshStandardMaterial color="#cc2222" metalness={0.5} roughness={0.4} />
      </mesh>
    </group>
  );
};

const ShadeStructure: FC<{ color: string }> = ({ color }) => {
  const poleMat = useShadowMaterial('#888888', { metalness: 0.5 });
  const canopyRef = useRef<THREE.Mesh>(null);

  // Slight billowing animation
  useFrame(({ clock }) => {
    if (canopyRef.current) {
      const geo = canopyRef.current.geometry as THREE.BufferGeometry;
      const posAttr = geo.getAttribute('position');
      if (posAttr && !canopyRef.current.userData.origPositions) {
        canopyRef.current.userData.origPositions = Float32Array.from(posAttr.array);
      }
      if (canopyRef.current.userData.origPositions) {
        const orig = canopyRef.current.userData.origPositions as Float32Array;
        const t = clock.getElapsedTime();
        for (let i = 0; i < posAttr.count; i++) {
          const ox = orig[i * 3];
          const oz = orig[i * 3 + 2];
          const displacement = Math.sin(t * 2 + ox * 0.5 + oz * 0.5) * 0.15;
          posAttr.setY(i, orig[i * 3 + 1] + displacement);
        }
        posAttr.needsUpdate = true;
      }
    }
  });

  return (
    <group>
      {/* Four poles */}
      {[[-4, 2.5, -4], [4, 2.5, -4], [-4, 2.5, 4], [4, 2.5, 4]].map((pos, i) => (
        <mesh key={i} position={pos as [number, number, number]} castShadow>
          <cylinderGeometry args={[0.1, 0.1, 9, 8]} />
          <primitive object={poleMat} attach="material" />
        </mesh>
      ))}
      {/* Fabric canopy */}
      <mesh ref={canopyRef} position={[0, 7, 0]} castShadow>
        <planeGeometry args={[9, 9, 10, 10]} />
        <meshStandardMaterial
          color={color !== '#888888' ? color : '#f5e6d0'}
          side={THREE.DoubleSide}
          roughness={0.8}
          transparent
          opacity={0.88}
        />
      </mesh>
    </group>
  );
};

const Signage: FC<{ color: string }> = ({ color }) => {
  const poleMat = useShadowMaterial('#777777', { metalness: 0.4 });
  const signMat = useShadowMaterial(color, { roughness: 0.4 });
  return (
    <group>
      {/* Pole */}
      <mesh position={[0, -0.5, 0]} castShadow>
        <cylinderGeometry args={[0.1, 0.1, 7, 8]} />
        <primitive object={poleMat} attach="material" />
      </mesh>
      {/* Sign face */}
      <mesh position={[0, 3.5, 0.15]} castShadow>
        <boxGeometry args={[3, 2, 0.15]} />
        <primitive object={signMat} attach="material" />
      </mesh>
      {/* Text area (lighter rectangle) */}
      <mesh position={[0, 3.5, 0.24]}>
        <planeGeometry args={[2.6, 1.6]} />
        <meshStandardMaterial color="#ffffff" roughness={0.5} />
      </mesh>
    </group>
  );
};

// ---------------------------------------------------------------------------
// BEFORE-MODE: Blight objects
// ---------------------------------------------------------------------------

export const ChainLinkFenceSegment: FC<{
  start: [number, number, number];
  end: [number, number, number];
}> = ({ start, end }) => {
  const dx = end[0] - start[0];
  const dz = end[2] - start[2];
  const length = Math.sqrt(dx * dx + dz * dz);
  const angle = Math.atan2(dx, dz);
  const midX = (start[0] + end[0]) / 2;
  const midZ = (start[2] + end[2]) / 2;

  return (
    <group position={[midX, 2.5, midZ]} rotation={[0, angle, 0]}>
      {/* Mesh panel */}
      <mesh castShadow>
        <boxGeometry args={[0.05, 5, length]} />
        <meshStandardMaterial
          color="#999999"
          metalness={0.7}
          roughness={0.5}
          wireframe
        />
      </mesh>
      {/* Top rail */}
      <mesh position={[0, 2.5, 0]} castShadow>
        <cylinderGeometry args={[0.06, 0.06, length, 8]} />
        <meshStandardMaterial color="#888888" metalness={0.6} roughness={0.4} />
      </mesh>
    </group>
  );
};

export const LitterObject: FC<{ position: [number, number, number]; type: 'can' | 'bag' | 'bottle' }> = ({
  position,
  type,
}) => {
  return (
    <group position={position}>
      {type === 'can' && (
        <mesh rotation={[Math.PI / 2, 0, Math.random() * Math.PI]} castShadow>
          <cylinderGeometry args={[0.15, 0.15, 0.4, 8]} />
          <meshStandardMaterial color="#cc4444" roughness={0.6} metalness={0.5} />
        </mesh>
      )}
      {type === 'bag' && (
        <mesh castShadow>
          <sphereGeometry args={[0.25, 6, 6]} />
          <meshStandardMaterial color="#dddddd" roughness={0.9} transparent opacity={0.7} />
        </mesh>
      )}
      {type === 'bottle' && (
        <mesh rotation={[Math.PI / 2, 0, Math.random() * Math.PI]} castShadow>
          <cylinderGeometry args={[0.08, 0.1, 0.5, 8]} />
          <meshStandardMaterial color="#88cc88" roughness={0.2} transparent opacity={0.6} />
        </mesh>
      )}
    </group>
  );
};

export const DeadGrassPatch: FC<{ position: [number, number, number]; size: number }> = ({ position, size }) => {
  return (
    <mesh position={position} rotation={[-Math.PI / 2, 0, Math.random() * Math.PI]} receiveShadow>
      <circleGeometry args={[size, 12]} />
      <meshStandardMaterial color="#8a7a5a" roughness={0.95} />
    </mesh>
  );
};

// ---------------------------------------------------------------------------
// PEOPLE SILHOUETTES (for "after" mode atmosphere)
// ---------------------------------------------------------------------------

export const PersonSilhouette: FC<{ position: [number, number, number]; color?: string }> = ({
  position,
  color = '#444466',
}) => {
  return (
    <group position={position}>
      {/* Head */}
      <mesh position={[0, 5, 0]} castShadow>
        <sphereGeometry args={[0.35, 8, 8]} />
        <meshStandardMaterial color={color} roughness={0.8} />
      </mesh>
      {/* Body */}
      <mesh position={[0, 3.5, 0]} castShadow>
        <capsuleGeometry args={[0.35, 2.2, 4, 8]} />
        <meshStandardMaterial color={color} roughness={0.8} />
      </mesh>
      {/* Legs */}
      <mesh position={[-0.2, 1.2, 0]} castShadow>
        <capsuleGeometry args={[0.15, 1.8, 4, 8]} />
        <meshStandardMaterial color={color} roughness={0.8} />
      </mesh>
      <mesh position={[0.2, 1.2, 0]} castShadow>
        <capsuleGeometry args={[0.15, 1.8, 4, 8]} />
        <meshStandardMaterial color={color} roughness={0.8} />
      </mesh>
    </group>
  );
};

// ---------------------------------------------------------------------------
// MESH REGISTRY — maps meshType string to component
// ---------------------------------------------------------------------------

const MESH_REGISTRY: Record<string, FC<{ color: string }>> = {
  stage_small: StageSmall,
  stage_medium: StageMedium,
  stage_large: StageLarge,
  sound_equipment: SoundEquipment,
  screening_wall: ScreeningWall,
  bench: Bench,
  picnic_table: PicnicTable,
  chair_cluster: ChairCluster,
  bleachers: Bleachers,
  amphitheater_seating: AmphitheaterSeating,
  food_cart: FoodCart,
  food_truck_space: FoodTruckSpace,
  market_stall: MarketStall,
  vendor_tent: VendorTent,
  raised_bed: RaisedBed,
  tree_planting: TreePlanting,
  flower_garden: FlowerGarden,
  native_meadow: NativeMeadow,
  water_feature: WaterFeature,
  mural_wall: MuralWall,
  sculpture_pad: SculpturePad,
  interactive_art: InteractiveArt,
  art_installation: ArtInstallation,
  play_structure: PlayStructure,
  basketball_half: BasketballHalf,
  fitness_station: FitnessStation,
  sports_field: SportsField,
  pathway: Pathway,
  fencing: Fencing,
  lighting_pole: LightingPole,
  power_hookup: PowerHookup,
  water_hookup: WaterHookup,
  shade_structure: ShadeStructure,
  signage: Signage,
};

// ---------------------------------------------------------------------------
// PUBLIC: Render a single element
// ---------------------------------------------------------------------------

export interface ElementMeshProps {
  element: Element3DProps;
  onClick?: (id: string) => void;
  opacity?: number;
}

export const ElementMesh: FC<ElementMeshProps> = ({ element, onClick, opacity = 1 }) => {
  const MeshComponent = MESH_REGISTRY[element.meshType];

  if (!MeshComponent) {
    // Fallback: generic coloured box
    return (
      <ElementWrapper element={element} onClick={onClick} opacity={opacity}>
        <mesh castShadow receiveShadow>
          <boxGeometry args={[2, 2, 2]} />
          <meshStandardMaterial
            color={element.color}
            transparent={opacity < 1}
            opacity={opacity}
          />
        </mesh>
      </ElementWrapper>
    );
  }

  return (
    <ElementWrapper element={element} onClick={onClick} opacity={opacity}>
      <MeshComponent color={element.color} />
    </ElementWrapper>
  );
};

export default ElementMesh;
