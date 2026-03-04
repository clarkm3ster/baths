"use client";

import { useRef, useMemo } from "react";
import { Canvas, useFrame } from "@react-three/fiber";
import { OrbitControls, Environment } from "@react-three/drei";
import * as THREE from "three";
import type { MaterialState } from "@/lib/types";

/** Map material state to visual properties of the sphere mesh. */
function useMaterialProps(state: MaterialState) {
  return useMemo(() => {
    const ec = state?.electrochromic_surface;
    const thermal = state?.phase_change_panel;
    const haptic = state?.haptic_surface;

    // Opacity from electrochromic
    const opacity = typeof ec?.wall_opacity === "number" ? ec.wall_opacity as number : 0.8;

    // Color from electrochromic or thermal
    let color = new THREE.Color(0.3, 0.25, 0.5); // default purple
    if (ec?.wall_color_rgb && Array.isArray(ec.wall_color_rgb)) {
      const [r, g, b] = ec.wall_color_rgb as number[];
      color = new THREE.Color(r / 255, g / 255, b / 255);
    }

    // Temperature → emissive warmth
    const temp = typeof thermal?.thermal_target_celsius === "number"
      ? thermal.thermal_target_celsius as number : 22;
    const warmth = Math.max(0, (temp - 18) / 12); // 0-1 over 18-30°C

    // Haptic → displacement scale
    const hapticIntensity = typeof haptic?.floor_haptic_intensity === "number"
      ? haptic.floor_haptic_intensity as number : 0;

    return { opacity, color, warmth, hapticIntensity };
  }, [state]);
}

function SphereMesh({ state }: { state: MaterialState }) {
  const meshRef = useRef<THREE.Mesh>(null);
  const { opacity, color, warmth, hapticIntensity } = useMaterialProps(state);

  useFrame((_, delta) => {
    if (!meshRef.current) return;
    // Slow rotation
    meshRef.current.rotation.y += delta * 0.15;
    // Haptic pulse — sinusoidal scale oscillation
    const pulse = 1 + Math.sin(Date.now() * 0.005) * hapticIntensity * 0.05;
    meshRef.current.scale.setScalar(pulse);
  });

  return (
    <mesh ref={meshRef}>
      <icosahedronGeometry args={[1.8, 4]} />
      <meshPhysicalMaterial
        color={color}
        transparent
        opacity={opacity}
        roughness={0.2}
        metalness={0.1}
        emissive={new THREE.Color(warmth * 0.3, warmth * 0.15, 0)}
        emissiveIntensity={warmth}
        wireframe={opacity < 0.3}
      />
    </mesh>
  );
}

interface Props {
  materialState: MaterialState;
}

export default function MaterialStateViz({ materialState }: Props) {
  return (
    <div className="w-full h-64 rounded-lg overflow-hidden" style={{ background: "#080812" }}>
      <Canvas camera={{ position: [0, 0, 5], fov: 50 }}>
        <ambientLight intensity={0.3} />
        <pointLight position={[5, 5, 5]} intensity={0.8} />
        <pointLight position={[-3, -2, 4]} intensity={0.4} color="#7c5cfc" />
        <SphereMesh state={materialState} />
        <OrbitControls enablePan={false} enableZoom={false} autoRotate autoRotateSpeed={0.5} />
        <Environment preset="night" />
      </Canvas>
    </div>
  );
}
