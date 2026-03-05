import { useEffect, useRef, useState, type ReactNode } from "react";
import * as THREE from "three";
import { OrbitControls } from "three/addons/controls/OrbitControls.js";
import { createRenaissanceDome } from "../worlds/RenaissanceDome";
import { createBrokenCapitol } from "../worlds/BrokenCapitol";
import { createPersonalDome } from "../worlds/PersonalDome";

// ─── Types ────────────────────────────────────────────────

type WorldKey = "renaissance" | "broken-capitol" | "personal-dome";

interface SplatWorldViewerProps {
  worldKey: WorldKey;
  splatUrl: string;
  title: string;
}

// ─── Fallback geometric scene factories ───────────────────

const FALLBACK_CREATORS: Record<
  WorldKey,
  (scene: THREE.Scene) => { animate: (time: number) => void }
> = {
  renaissance: createRenaissanceDome,
  "broken-capitol": createBrokenCapitol,
  "personal-dome": createPersonalDome,
};

// ─── Component ────────────────────────────────────────────

export function SplatWorldViewer({
  worldKey,
  splatUrl,
  title,
}: SplatWorldViewerProps): ReactNode {
  const containerRef = useRef<HTMLDivElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [size, setSize] = useState<{ w: number; h: number }>({ w: 0, h: 0 });
  const [loadingState, setLoadingState] = useState<
    "loading" | "splat" | "fallback"
  >("loading");
  const hasSize = size.w > 0 && size.h > 0;

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

  // ── Main Three.js scene setup ──────────────────────────

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

    // Scene
    const scene = new THREE.Scene();

    // Camera
    const camera = new THREE.PerspectiveCamera(70, size.w / size.h, 0.1, 100);
    camera.position.set(0, 2, 5);
    camera.lookAt(0, 1, 0);

    // Controls
    const controls = new OrbitControls(camera, canvas);
    controls.enableDamping = true;
    controls.dampingFactor = 0.05;
    controls.autoRotate = true;
    controls.autoRotateSpeed = 0.6;
    controls.enablePan = false;
    controls.minDistance = 1;
    controls.maxDistance = 20;
    controls.maxPolarAngle = Math.PI * 0.85;

    let animateFn: ((time: number) => void) | null = null;
    let sparkRendererObj: THREE.Object3D | null = null;
    let splatMeshObj: THREE.Object3D | null = null;
    let running = true;
    const clock = new THREE.Clock();

    // Try to load splat world, or fall back to geometric
    async function initSplatOrFallback() {
      if (splatUrl) {
        try {
          // Dynamically import SparkJS to avoid blocking initial load
          const { SparkRenderer, SplatMesh } = await import(
            "@sparkjsdev/spark"
          );

          if (!running) return;

          // Create SparkRenderer
          const spark = new SparkRenderer({ renderer });
          scene.add(spark);
          sparkRendererObj = spark;

          // Create SplatMesh from URL
          const splat = new SplatMesh({ url: splatUrl });
          await splat.initialized;

          if (!running) {
            splat.dispose();
            return;
          }

          scene.add(splat);
          splatMeshObj = splat;

          // Add some ambient light for the splat scene
          scene.add(new THREE.AmbientLight(0xffffff, 0.5));
          scene.add(new THREE.DirectionalLight(0xffffff, 0.8));

          setLoadingState("splat");
        } catch (err) {
          console.warn(
            `SplatMesh load failed for "${worldKey}", using fallback:`,
            err
          );
          initFallback();
        }
      } else {
        initFallback();
      }
    }

    function initFallback() {
      const creator = FALLBACK_CREATORS[worldKey];
      if (creator) {
        const result = creator(scene);
        animateFn = result.animate;
      }
      setLoadingState("fallback");
    }

    initSplatOrFallback();

    // Render loop
    const renderLoop = (): void => {
      if (!running) return;
      requestAnimationFrame(renderLoop);

      const elapsed = clock.getElapsedTime();
      if (animateFn) {
        animateFn(elapsed);
      }
      controls.update();
      renderer.render(scene, camera);
    };
    renderLoop();

    // Handle resize
    const handleResize = () => {
      if (!containerRef.current) return;
      const { clientWidth, clientHeight } = containerRef.current;
      renderer.setSize(clientWidth, clientHeight);
      camera.aspect = clientWidth / clientHeight;
      camera.updateProjectionMatrix();
    };
    window.addEventListener("resize", handleResize);

    // Cleanup
    return () => {
      running = false;
      window.removeEventListener("resize", handleResize);
      controls.dispose();

      if (splatMeshObj && "dispose" in splatMeshObj) {
        (splatMeshObj as { dispose: () => void }).dispose();
      }

      scene.traverse((obj) => {
        if (obj instanceof THREE.Mesh) {
          obj.geometry.dispose();
          const mat = obj.material;
          if (Array.isArray(mat)) {
            mat.forEach((m) => m.dispose());
          } else {
            mat.dispose();
          }
        }
      });
      scene.clear();
      renderer.dispose();
    };
  }, [worldKey, splatUrl, hasSize, size.w, size.h]);

  return (
    <div
      ref={containerRef}
      style={{
        position: "relative",
        width: "100%",
        height: "100%",
        background: "#0D0D0D",
        overflow: "hidden",
      }}
    >
      <canvas
        ref={canvasRef}
        style={{
          display: hasSize ? "block" : "none",
          width: "100%",
          height: "100%",
        }}
      />

      {/* Title overlay */}
      <div
        style={{
          position: "absolute",
          bottom: 0,
          left: 0,
          right: 0,
          padding: "48px 24px 32px",
          background:
            "linear-gradient(to top, rgba(0,0,0,0.8) 0%, rgba(0,0,0,0.3) 50%, transparent 100%)",
          pointerEvents: "none",
        }}
      >
        <h3
          style={{
            margin: 0,
            fontFamily: "Georgia, serif",
            fontSize: "1.75rem",
            color: "#FFFFFF",
            letterSpacing: "0.02em",
            textAlign: "center",
          }}
        >
          {title}
        </h3>

        {loadingState === "loading" && (
          <p
            style={{
              margin: "8px 0 0",
              fontFamily: '"JetBrains Mono", monospace',
              fontSize: "0.7rem",
              color: "#C4A265",
              letterSpacing: "0.15em",
              textTransform: "uppercase",
              textAlign: "center",
              opacity: 0.7,
            }}
          >
            Loading world...
          </p>
        )}

        {loadingState === "fallback" && (
          <p
            style={{
              margin: "8px 0 0",
              fontFamily: '"JetBrains Mono", monospace',
              fontSize: "0.65rem",
              color: "rgba(196, 162, 101, 0.5)",
              letterSpacing: "0.12em",
              textTransform: "uppercase",
              textAlign: "center",
            }}
          >
            geometric preview
          </p>
        )}
      </div>

      {/* Drag hint */}
      <div
        style={{
          position: "absolute",
          top: 16,
          left: 0,
          right: 0,
          textAlign: "center",
          pointerEvents: "none",
          fontFamily: '"JetBrains Mono", monospace',
          fontSize: "0.65rem",
          color: "rgba(196, 162, 101, 0.4)",
          letterSpacing: "0.2em",
          textTransform: "uppercase",
        }}
      >
        drag to explore
      </div>
    </div>
  );
}
