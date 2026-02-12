import {
  useEffect,
  useRef,
  useState,
  useCallback,
  type ReactNode,
} from "react";
import * as THREE from "three";
import { OrbitControls } from "three/addons/controls/OrbitControls.js";
import { createRenaissanceDome } from "./RenaissanceDome.ts";
import { createBrokenCapitol } from "./BrokenCapitol.ts";
import { createPersonalDome } from "./PersonalDome.ts";

// ─── Types ────────────────────────────────────────────────

type WorldId = "renaissance" | "broken-capitol" | "personal-dome";

interface WorldRendererProps {
  worldId: WorldId;
  overlayText: string;
  onContinue?: () => void;
}

interface WorldCreatorResult {
  animate: (time: number) => void;
}

type WorldCreator = (scene: THREE.Scene) => WorldCreatorResult;

// ─── Camera presets per world ─────────────────────────────

interface CameraPreset {
  position: THREE.Vector3;
  lookAt: THREE.Vector3;
  fov: number;
}

const CAMERA_PRESETS: Record<WorldId, CameraPreset> = {
  renaissance: {
    position: new THREE.Vector3(0, 2, 0.1),
    lookAt: new THREE.Vector3(0, 14, 0),
    fov: 75,
  },
  "broken-capitol": {
    position: new THREE.Vector3(0, -4.2, -4),
    lookAt: new THREE.Vector3(0, 0, -9),
    fov: 65,
  },
  "personal-dome": {
    position: new THREE.Vector3(0, 1.8, 0.1),
    lookAt: new THREE.Vector3(0, 1.8, -5),
    fov: 70,
  },
};

// ─── World factory ────────────────────────────────────────

const WORLD_CREATORS: Record<WorldId, WorldCreator> = {
  renaissance: createRenaissanceDome,
  "broken-capitol": createBrokenCapitol,
  "personal-dome": createPersonalDome,
};

// ─── Auto-explore duration ────────────────────────────────

const AUTO_EXPLORE_DURATION = 30_000; // 30 seconds in ms

// ─── Component ────────────────────────────────────────────

export function WorldRenderer({
  worldId,
  overlayText,
  onContinue,
}: WorldRendererProps): ReactNode {
  const containerRef = useRef<HTMLDivElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const rendererRef = useRef<THREE.WebGLRenderer | null>(null);
  const sceneRef = useRef<THREE.Scene | null>(null);
  const cameraRef = useRef<THREE.PerspectiveCamera | null>(null);
  const controlsRef = useRef<OrbitControls | null>(null);
  const animateRef = useRef<WorldCreatorResult | null>(null);
  const rafRef = useRef<number>(0);
  const timerRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  const [isActive, setIsActive] = useState(false);
  const [isVisible, setIsVisible] = useState(false);
  const [showContinue, setShowContinue] = useState(false);
  const [size, setSize] = useState<{ w: number; h: number }>({ w: 0, h: 0 });

  const hasSize = size.w > 0 && size.h > 0;

  // ── Intersection Observer for fade-in ──────────────────

  useEffect(() => {
    const container = containerRef.current;
    if (!container) return;

    const observer = new IntersectionObserver(
      (entries) => {
        for (const entry of entries) {
          if (entry.isIntersecting) {
            setIsVisible(true);
          }
        }
      },
      { threshold: 0.15 }
    );

    observer.observe(container);
    return () => observer.disconnect();
  }, []);

  // ── ResizeObserver ─────────────────────────────────────

  useEffect(() => {
    const container = containerRef.current;
    if (!container) return;

    const observer = new ResizeObserver((entries) => {
      for (const entry of entries) {
        const { width, height } = entry.contentRect;
        setSize({ w: Math.floor(width), h: Math.floor(height) });
      }
    });

    observer.observe(container);
    return () => observer.disconnect();
  }, []);

  // ── Update renderer / camera when size changes ─────────

  useEffect(() => {
    if (!hasSize) return;

    const renderer = rendererRef.current;
    const camera = cameraRef.current;
    if (renderer) {
      renderer.setSize(size.w, size.h);
    }
    if (camera) {
      camera.aspect = size.w / size.h;
      camera.updateProjectionMatrix();
    }
  }, [size.w, size.h, hasSize]);

  // ── Initialize Three.js scene ──────────────────────────

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas || !hasSize) return;

    // Renderer
    const renderer = new THREE.WebGLRenderer({
      canvas,
      antialias: true,
      alpha: false,
    });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.setSize(size.w, size.h);
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1.0;
    rendererRef.current = renderer;

    // Scene
    const scene = new THREE.Scene();
    sceneRef.current = scene;

    // Camera
    const preset = CAMERA_PRESETS[worldId];
    const camera = new THREE.PerspectiveCamera(
      preset.fov,
      size.w / size.h,
      0.1,
      100
    );
    camera.position.copy(preset.position);
    camera.lookAt(preset.lookAt);
    cameraRef.current = camera;

    // Orbit controls (disabled until activation)
    const controls = new OrbitControls(camera, canvas);
    controls.enabled = false;
    controls.enableDamping = true;
    controls.dampingFactor = 0.05;
    controls.autoRotate = true;
    controls.autoRotateSpeed = 0.8;
    controls.enablePan = false;
    controls.minDistance = 1;
    controls.maxDistance = 15;
    controls.maxPolarAngle = Math.PI * 0.85;
    controlsRef.current = controls;

    // Build the world
    const worldResult = WORLD_CREATORS[worldId](scene);
    animateRef.current = worldResult;

    // Render loop
    const clock = new THREE.Clock();
    let running = true;

    const renderLoop = (): void => {
      if (!running) return;
      rafRef.current = requestAnimationFrame(renderLoop);

      const elapsed = clock.getElapsedTime();
      worldResult.animate(elapsed);

      if (controls.enabled) {
        controls.update();
      }

      renderer.render(scene, camera);
    };

    renderLoop();

    // Cleanup
    return () => {
      running = false;
      cancelAnimationFrame(rafRef.current);

      controls.dispose();
      controlsRef.current = null;

      // Dispose all scene objects
      scene.traverse((obj) => {
        if (obj instanceof THREE.Mesh) {
          obj.geometry.dispose();
          const mat = obj.material;
          if (Array.isArray(mat)) {
            mat.forEach(disposeMaterial);
          } else {
            disposeMaterial(mat);
          }
        }
        if (obj instanceof THREE.Points) {
          obj.geometry.dispose();
          const mat = obj.material;
          if (Array.isArray(mat)) {
            mat.forEach(disposeMaterial);
          } else {
            disposeMaterial(mat);
          }
        }
        if (obj instanceof THREE.Line) {
          obj.geometry.dispose();
          const mat = obj.material;
          if (Array.isArray(mat)) {
            mat.forEach(disposeMaterial);
          } else {
            disposeMaterial(mat);
          }
        }
        if (obj instanceof THREE.LineSegments) {
          obj.geometry.dispose();
          const mat = obj.material;
          if (Array.isArray(mat)) {
            mat.forEach(disposeMaterial);
          } else {
            disposeMaterial(mat);
          }
        }
      });

      scene.clear();
      renderer.dispose();

      rendererRef.current = null;
      sceneRef.current = null;
      cameraRef.current = null;
      animateRef.current = null;
    };
  }, [worldId, hasSize]); // eslint-disable-line react-hooks/exhaustive-deps

  // ── Activation handler ─────────────────────────────────

  const handleStepInside = useCallback(() => {
    setIsActive(true);
    setShowContinue(false);

    if (controlsRef.current) {
      controlsRef.current.enabled = true;
      controlsRef.current.autoRotate = true;
    }

    // Show "Continue" after auto-explore duration
    timerRef.current = setTimeout(() => {
      setShowContinue(true);
      if (controlsRef.current) {
        controlsRef.current.autoRotateSpeed = 0.3;
      }
    }, AUTO_EXPLORE_DURATION);
  }, []);

  const handleContinue = useCallback(() => {
    if (timerRef.current) {
      clearTimeout(timerRef.current);
      timerRef.current = null;
    }
    setIsActive(false);
    setShowContinue(false);

    if (controlsRef.current) {
      controlsRef.current.enabled = false;
      controlsRef.current.autoRotate = false;
    }

    // Reset camera to preset
    const preset = CAMERA_PRESETS[worldId];
    if (cameraRef.current) {
      cameraRef.current.position.copy(preset.position);
      cameraRef.current.lookAt(preset.lookAt);
    }

    onContinue?.();
  }, [worldId, onContinue]);

  // Cleanup timer on unmount
  useEffect(() => {
    return () => {
      if (timerRef.current) {
        clearTimeout(timerRef.current);
      }
    };
  }, []);

  // ── Render ─────────────────────────────────────────────

  return (
    <div
      ref={containerRef}
      className="relative w-full overflow-hidden"
      style={{
        height: "80vh",
        opacity: isVisible ? 1 : 0,
        transform: isVisible ? "translateY(0)" : "translateY(40px)",
        transition: "opacity 1.2s ease-out, transform 1.2s ease-out",
      }}
    >
      {/* Three.js Canvas */}
      <canvas
        ref={canvasRef}
        className="absolute inset-0 w-full h-full"
        style={{ display: hasSize ? "block" : "none" }}
      />

      {/* Overlay Text */}
      {!isActive && (
        <div
          className="absolute inset-0 flex flex-col items-center justify-end pb-16 pointer-events-none"
          style={{
            background:
              "linear-gradient(to top, rgba(0,0,0,0.7) 0%, rgba(0,0,0,0.2) 40%, transparent 70%)",
          }}
        >
          <p
            className="text-center max-w-2xl px-8 mb-8 leading-relaxed"
            style={{
              fontFamily: "var(--font-serif)",
              fontSize: "1.25rem",
              color: "#FFFFFF",
              opacity: 0.9,
            }}
          >
            {overlayText}
          </p>

          {/* Step Inside Button */}
          <button
            type="button"
            onClick={handleStepInside}
            className="pointer-events-auto px-8 py-3 cursor-pointer"
            style={{
              background: "transparent",
              border: "1px solid rgba(196, 162, 101, 0.6)",
              color: "#C4A265",
              fontFamily: "var(--font-mono)",
              fontSize: "0.85rem",
              letterSpacing: "0.15em",
              textTransform: "uppercase",
              transition: "all 0.3s ease",
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.background = "rgba(196, 162, 101, 0.15)";
              e.currentTarget.style.borderColor = "rgba(196, 162, 101, 1)";
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.background = "transparent";
              e.currentTarget.style.borderColor = "rgba(196, 162, 101, 0.6)";
            }}
          >
            Step Inside
          </button>
        </div>
      )}

      {/* Continue Button (after auto-explore) */}
      {isActive && showContinue && (
        <div className="absolute inset-x-0 bottom-0 flex justify-center pb-10">
          <button
            type="button"
            onClick={handleContinue}
            className="px-8 py-3 cursor-pointer"
            style={{
              background: "rgba(0, 0, 0, 0.6)",
              border: "1px solid rgba(196, 162, 101, 0.6)",
              color: "#C4A265",
              fontFamily: "var(--font-mono)",
              fontSize: "0.85rem",
              letterSpacing: "0.15em",
              textTransform: "uppercase",
              transition: "all 0.3s ease",
              animation: "fadeInUp 0.8s ease-out",
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.background = "rgba(196, 162, 101, 0.15)";
              e.currentTarget.style.borderColor = "rgba(196, 162, 101, 1)";
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.background = "rgba(0, 0, 0, 0.6)";
              e.currentTarget.style.borderColor = "rgba(196, 162, 101, 0.6)";
            }}
          >
            Continue
          </button>
        </div>
      )}

      {/* Active experience hint */}
      {isActive && !showContinue && (
        <div
          className="absolute top-6 left-0 right-0 text-center pointer-events-none"
          style={{
            fontFamily: "var(--font-mono)",
            fontSize: "0.7rem",
            color: "rgba(196, 162, 101, 0.5)",
            letterSpacing: "0.2em",
            textTransform: "uppercase",
          }}
        >
          drag to explore
        </div>
      )}
    </div>
  );
}

// ─── Material disposal helper ────────────────────────────

function disposeMaterial(mat: THREE.Material): void {
  // Dispose textures on standard-like materials
  const stdMat = mat as THREE.MeshStandardMaterial;
  if (stdMat.map) stdMat.map.dispose();
  if (stdMat.emissiveMap) stdMat.emissiveMap.dispose();
  if (stdMat.normalMap) stdMat.normalMap.dispose();
  if (stdMat.roughnessMap) stdMat.roughnessMap.dispose();
  if (stdMat.metalnessMap) stdMat.metalnessMap.dispose();
  if (stdMat.aoMap) stdMat.aoMap.dispose();
  mat.dispose();
}
