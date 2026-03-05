/**
 * MarbleViewer — Immersive 3D World Viewer
 *
 * Renders World Labs Marble-generated 3D worlds using SparkJS SplatMesh,
 * or falls back to a procedural geometric scene when no splat is available.
 *
 * Features:
 *   - Full-screen overlay with dark theme (#0A0A0A)
 *   - SplatMesh loading from world splat URL via SparkJS
 *   - Orbit controls for camera navigation
 *   - Fallback procedural scene with floating geometry
 *   - Close button to return to the design view
 */

import { useRef, useEffect, useCallback, useState } from 'react';
import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';
import { X, RotateCcw, Maximize2, Minimize2 } from 'lucide-react';

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

interface MarbleViewerProps {
  splatUrl: string;
  prompt: string;
  worldId: string;
  onClose: () => void;
  isMock?: boolean;
}

// ---------------------------------------------------------------------------
// Fallback scene builder
// ---------------------------------------------------------------------------

function buildFallbackScene(scene: THREE.Scene, prompt: string): void {
  // Ambient + directional lighting
  const ambient = new THREE.AmbientLight(0x404060, 0.6);
  scene.add(ambient);

  const directional = new THREE.DirectionalLight(0xffffff, 1.2);
  directional.position.set(5, 10, 7);
  scene.add(directional);

  const point = new THREE.PointLight(0x3b82f6, 2, 50);
  point.position.set(0, 5, 0);
  scene.add(point);

  // Ground plane
  const groundGeo = new THREE.PlaneGeometry(40, 40);
  const groundMat = new THREE.MeshStandardMaterial({
    color: 0x111111,
    roughness: 0.9,
    metalness: 0.1,
  });
  const ground = new THREE.Mesh(groundGeo, groundMat);
  ground.rotation.x = -Math.PI / 2;
  ground.position.y = -0.01;
  scene.add(ground);

  // Grid helper
  const gridHelper = new THREE.GridHelper(40, 40, 0x222222, 0x1a1a1a);
  scene.add(gridHelper);

  // Generate deterministic geometry from the prompt
  const seed = prompt.split('').reduce((acc, c) => acc + c.charCodeAt(0), 0);
  const rng = () => {
    const x = Math.sin(seed * 9301 + 49297) % 233280;
    return Math.abs(x / 233280);
  };

  const palette = [0x3b82f6, 0xa855f7, 0x22c55e, 0xf59e0b, 0xef4444, 0x06b6d4];

  // Central structure
  const centralGeo = new THREE.IcosahedronGeometry(1.8, 1);
  const centralMat = new THREE.MeshStandardMaterial({
    color: palette[seed % palette.length],
    roughness: 0.3,
    metalness: 0.7,
    wireframe: false,
  });
  const centralMesh = new THREE.Mesh(centralGeo, centralMat);
  centralMesh.position.y = 2.5;
  centralMesh.userData.animate = true;
  centralMesh.userData.floatSpeed = 0.8;
  centralMesh.userData.rotateSpeed = 0.3;
  scene.add(centralMesh);

  // Wireframe overlay
  const wireGeo = new THREE.IcosahedronGeometry(2.2, 1);
  const wireMat = new THREE.MeshBasicMaterial({
    color: palette[seed % palette.length],
    wireframe: true,
    transparent: true,
    opacity: 0.15,
  });
  const wireMesh = new THREE.Mesh(wireGeo, wireMat);
  wireMesh.position.y = 2.5;
  wireMesh.userData.animate = true;
  wireMesh.userData.floatSpeed = 0.8;
  wireMesh.userData.rotateSpeed = -0.15;
  scene.add(wireMesh);

  // Surrounding structures
  const geometries = [
    new THREE.BoxGeometry(1, 1, 1),
    new THREE.OctahedronGeometry(0.8, 0),
    new THREE.ConeGeometry(0.6, 1.4, 6),
    new THREE.TorusGeometry(0.6, 0.2, 8, 16),
    new THREE.TetrahedronGeometry(0.7, 0),
    new THREE.CylinderGeometry(0.3, 0.6, 1.2, 8),
  ];

  for (let i = 0; i < 12; i++) {
    const angle = (i / 12) * Math.PI * 2;
    const radius = 4 + (rng() * 4);
    const height = 0.5 + rng() * 3;
    const scale = 0.5 + rng() * 1.2;

    const geo = geometries[i % geometries.length];
    const mat = new THREE.MeshStandardMaterial({
      color: palette[(seed + i) % palette.length],
      roughness: 0.4,
      metalness: 0.5,
      transparent: true,
      opacity: 0.7 + rng() * 0.3,
    });
    const mesh = new THREE.Mesh(geo, mat);
    mesh.position.set(
      Math.cos(angle) * radius,
      height,
      Math.sin(angle) * radius
    );
    mesh.scale.setScalar(scale);
    mesh.userData.animate = true;
    mesh.userData.floatSpeed = 0.3 + rng() * 0.5;
    mesh.userData.rotateSpeed = (rng() - 0.5) * 0.4;
    mesh.userData.baseY = height;
    scene.add(mesh);
  }

  // Particle field (small spheres)
  const particleGeo = new THREE.SphereGeometry(0.04, 4, 4);
  for (let i = 0; i < 60; i++) {
    const mat = new THREE.MeshBasicMaterial({
      color: palette[(seed + i) % palette.length],
      transparent: true,
      opacity: 0.3 + rng() * 0.5,
    });
    const p = new THREE.Mesh(particleGeo, mat);
    p.position.set(
      (rng() - 0.5) * 30,
      rng() * 8,
      (rng() - 0.5) * 30
    );
    p.userData.animate = true;
    p.userData.floatSpeed = 0.2 + rng() * 0.8;
    p.userData.baseY = p.position.y;
    scene.add(p);
  }
}


// ---------------------------------------------------------------------------
// Component
// ---------------------------------------------------------------------------

export default function MarbleViewer({
  splatUrl,
  prompt,
  worldId,
  onClose,
  isMock = false,
}: MarbleViewerProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const rendererRef = useRef<THREE.WebGLRenderer | null>(null);
  const sceneRef = useRef<THREE.Scene | null>(null);
  const cameraRef = useRef<THREE.PerspectiveCamera | null>(null);
  const controlsRef = useRef<OrbitControls | null>(null);
  const frameIdRef = useRef<number>(0);
  const sparkRendererRef = useRef<any>(null);
  const splatMeshRef = useRef<any>(null);
  const clockRef = useRef(new THREE.Clock());

  const [loading, setLoading] = useState(!!splatUrl);
  const [error, setError] = useState<string | null>(null);

  // Initialise Three.js scene
  const initScene = useCallback(() => {
    const container = containerRef.current;
    if (!container) return;

    // Renderer
    const renderer = new THREE.WebGLRenderer({
      antialias: false,
      alpha: false,
    });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.setSize(container.clientWidth, container.clientHeight);
    renderer.setClearColor(0x0a0a0a, 1);
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1.0;
    container.appendChild(renderer.domElement);
    rendererRef.current = renderer;

    // Scene
    const scene = new THREE.Scene();
    scene.fog = new THREE.FogExp2(0x0a0a0a, 0.015);
    sceneRef.current = scene;

    // Camera
    const camera = new THREE.PerspectiveCamera(
      60,
      container.clientWidth / container.clientHeight,
      0.1,
      1000
    );
    camera.position.set(6, 5, 10);
    camera.lookAt(0, 1, 0);
    cameraRef.current = camera;

    // Orbit controls
    const controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.08;
    controls.target.set(0, 1, 0);
    controls.minDistance = 1;
    controls.maxDistance = 100;
    controls.maxPolarAngle = Math.PI * 0.85;
    controls.update();
    controlsRef.current = controls;

    return { renderer, scene, camera, controls };
  }, []);

  // Load the splat or build fallback
  useEffect(() => {
    const init = initScene();
    if (!init) return;
    const { renderer, scene, camera, controls } = init;

    let disposed = false;

    const loadSplat = async () => {
      if (!splatUrl || isMock) {
        // No real splat -- build the fallback scene
        buildFallbackScene(scene, prompt);
        setLoading(false);
        return;
      }

      try {
        // Dynamically import SparkJS to avoid SSR issues
        const { SparkRenderer, SplatMesh } = await import('@sparkjsdev/spark');

        if (disposed) return;

        const spark = new SparkRenderer({ renderer });
        scene.add(spark);
        sparkRendererRef.current = spark;

        const splat = new SplatMesh({ url: splatUrl });
        await splat.initialized;

        if (disposed) return;

        scene.add(splat);
        splatMeshRef.current = splat;

        // Auto-frame the splat
        const box = splat.getBoundingBox();
        const center = new THREE.Vector3();
        box.getCenter(center);
        const size = new THREE.Vector3();
        box.getSize(size);
        const maxDim = Math.max(size.x, size.y, size.z);

        controls.target.copy(center);
        camera.position.set(
          center.x + maxDim * 0.8,
          center.y + maxDim * 0.5,
          center.z + maxDim * 0.8
        );
        controls.update();

        setLoading(false);
      } catch (err: any) {
        console.error('Failed to load splat, falling back to geometric scene:', err);
        setError(err?.message || 'Failed to load 3D world');
        buildFallbackScene(scene, prompt);
        setLoading(false);
      }
    };

    loadSplat();

    // Animation loop
    const clock = clockRef.current;
    clock.start();

    const animate = () => {
      if (disposed) return;
      frameIdRef.current = requestAnimationFrame(animate);

      const elapsed = clock.getElapsedTime();
      controls.update();

      // Animate fallback objects
      scene.traverse((obj) => {
        if (obj.userData.animate) {
          const speed = obj.userData.floatSpeed || 0.5;
          const rotSpeed = obj.userData.rotateSpeed || 0;
          const baseY = obj.userData.baseY ?? obj.position.y;
          obj.position.y = baseY + Math.sin(elapsed * speed) * 0.3;
          obj.rotation.y += rotSpeed * 0.01;
        }
      });

      // SparkRenderer update
      if (sparkRendererRef.current) {
        sparkRendererRef.current.update({ scene });
      }

      renderer.render(scene, camera);
    };
    animate();

    // Resize handler
    const handleResize = () => {
      const container = containerRef.current;
      if (!container) return;
      const w = container.clientWidth;
      const h = container.clientHeight;
      camera.aspect = w / h;
      camera.updateProjectionMatrix();
      renderer.setSize(w, h);
    };
    window.addEventListener('resize', handleResize);

    // Cleanup
    return () => {
      disposed = true;
      window.removeEventListener('resize', handleResize);
      cancelAnimationFrame(frameIdRef.current);

      if (splatMeshRef.current) {
        splatMeshRef.current.dispose();
        splatMeshRef.current = null;
      }
      if (sparkRendererRef.current) {
        sparkRendererRef.current = null;
      }
      controls.dispose();
      renderer.dispose();
      if (containerRef.current && renderer.domElement.parentNode === containerRef.current) {
        containerRef.current.removeChild(renderer.domElement);
      }
    };
  }, [splatUrl, prompt, isMock, initScene]);

  // Reset camera
  const handleResetCamera = useCallback(() => {
    if (cameraRef.current && controlsRef.current) {
      cameraRef.current.position.set(6, 5, 10);
      controlsRef.current.target.set(0, 1, 0);
      controlsRef.current.update();
    }
  }, []);

  // ---------------------------------------------------------------------------
  // Render
  // ---------------------------------------------------------------------------

  return (
    <div
      style={{
        position: 'fixed',
        inset: 0,
        zIndex: 9999,
        background: '#0A0A0A',
        display: 'flex',
        flexDirection: 'column',
      }}
    >
      {/* Top bar */}
      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          height: '48px',
          padding: '0 16px',
          borderBottom: '1px solid #2A2A2A',
          background: '#141414',
          flexShrink: 0,
        }}
      >
        {/* Left: title */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <div
            style={{
              width: '28px',
              height: '28px',
              borderRadius: '8px',
              background: 'linear-gradient(135deg, #3B82F6, #A855F7)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontSize: '12px',
              fontWeight: 700,
              color: '#fff',
            }}
          >
            3D
          </div>
          <div>
            <div
              style={{
                fontSize: '12px',
                fontWeight: 600,
                color: '#FFFFFF',
                lineHeight: '1.2',
              }}
            >
              Marble 3D World
            </div>
            <div
              style={{
                fontSize: '10px',
                color: '#A0A0A0',
                maxWidth: '400px',
                overflow: 'hidden',
                textOverflow: 'ellipsis',
                whiteSpace: 'nowrap',
              }}
            >
              {prompt}
            </div>
          </div>
        </div>

        {/* Right: actions */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          {/* World ID badge */}
          <span
            style={{
              fontSize: '10px',
              fontFamily: "'JetBrains Mono', monospace",
              color: '#A0A0A0',
              background: '#1E1E1E',
              border: '1px solid #2A2A2A',
              borderRadius: '6px',
              padding: '4px 8px',
            }}
          >
            {worldId.slice(0, 12)}
          </span>

          {isMock && (
            <span
              style={{
                fontSize: '10px',
                color: '#F59E0B',
                background: 'rgba(245,158,11,0.1)',
                border: '1px solid rgba(245,158,11,0.2)',
                borderRadius: '6px',
                padding: '4px 8px',
              }}
            >
              Preview Mode
            </span>
          )}

          {/* Reset camera */}
          <button
            onClick={handleResetCamera}
            style={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              width: '32px',
              height: '32px',
              borderRadius: '8px',
              border: '1px solid #2A2A2A',
              background: '#1E1E1E',
              color: '#A0A0A0',
              cursor: 'pointer',
              transition: 'background 200ms',
            }}
            title="Reset Camera"
            onMouseEnter={(e) => (e.currentTarget.style.background = '#2A2A2A')}
            onMouseLeave={(e) => (e.currentTarget.style.background = '#1E1E1E')}
          >
            <RotateCcw size={14} />
          </button>

          {/* Close */}
          <button
            onClick={onClose}
            style={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              width: '32px',
              height: '32px',
              borderRadius: '8px',
              border: '1px solid #2A2A2A',
              background: '#1E1E1E',
              color: '#A0A0A0',
              cursor: 'pointer',
              transition: 'background 200ms',
            }}
            title="Close (Esc)"
            onMouseEnter={(e) => (e.currentTarget.style.background = '#2A2A2A')}
            onMouseLeave={(e) => (e.currentTarget.style.background = '#1E1E1E')}
          >
            <X size={14} />
          </button>
        </div>
      </div>

      {/* 3D Canvas */}
      <div
        ref={containerRef}
        style={{
          flex: 1,
          position: 'relative',
          overflow: 'hidden',
        }}
      >
        {/* Loading overlay */}
        {loading && (
          <div
            style={{
              position: 'absolute',
              inset: 0,
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              justifyContent: 'center',
              background: 'rgba(10,10,10,0.9)',
              zIndex: 10,
            }}
          >
            <div
              style={{
                width: '48px',
                height: '48px',
                border: '3px solid #2A2A2A',
                borderTopColor: '#3B82F6',
                borderRadius: '50%',
                animation: 'spin 1s linear infinite',
              }}
            />
            <div
              style={{
                marginTop: '16px',
                fontSize: '13px',
                fontWeight: 500,
                color: '#FFFFFF',
              }}
            >
              Loading 3D world...
            </div>
            <div
              style={{
                marginTop: '6px',
                fontSize: '11px',
                color: '#A0A0A0',
                maxWidth: '300px',
                textAlign: 'center',
              }}
            >
              Rendering splat data from Marble
            </div>
          </div>
        )}

        {/* Error banner */}
        {error && (
          <div
            style={{
              position: 'absolute',
              bottom: '16px',
              left: '50%',
              transform: 'translateX(-50%)',
              background: 'rgba(239,68,68,0.1)',
              border: '1px solid rgba(239,68,68,0.25)',
              borderRadius: '8px',
              padding: '8px 16px',
              fontSize: '11px',
              color: '#EF4444',
              zIndex: 10,
              maxWidth: '400px',
              textAlign: 'center',
            }}
          >
            {error} -- Showing fallback scene
          </div>
        )}
      </div>

      {/* Bottom hints bar */}
      <div
        style={{
          height: '28px',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          gap: '24px',
          fontSize: '10px',
          color: '#A0A0A0',
          background: '#141414',
          borderTop: '1px solid #2A2A2A',
          flexShrink: 0,
        }}
      >
        <span>Left-click + drag to orbit</span>
        <span>Right-click + drag to pan</span>
        <span>Scroll to zoom</span>
        <span>
          <kbd style={{ fontFamily: "'JetBrains Mono', monospace" }}>Esc</kbd> Close
        </span>
      </div>

      {/* Spin keyframe (injected once) */}
      <style>{`
        @keyframes spin {
          to { transform: rotate(360deg); }
        }
      `}</style>
    </div>
  );
}
