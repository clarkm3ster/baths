/**
 * Controls.tsx — Camera and interaction controls for the SPHERES WorldView.
 *
 * Two modes:
 *   1. ORBIT  — OrbitControls for overview panning/rotating (default)
 *   2. FIRST-PERSON — PointerLockControls + WASD movement + mouse look
 *
 * Also provides:
 *   - Minimap in corner (top-down orthographic render-to-texture)
 *   - Click-on-element info popup plumbing
 *   - Speed control
 */

import {
  useRef,
  useState,
  useEffect,
  useCallback,
  forwardRef,
  useImperativeHandle,
  type FC,
} from 'react';
import * as THREE from 'three';
import { useThree, useFrame } from '@react-three/fiber';
import { OrbitControls, PointerLockControls, Html } from '@react-three/drei';

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

export type CameraMode = 'orbit' | 'firstperson';

export interface ControlsProps {
  mode: CameraMode;
  onModeChange?: (mode: CameraMode) => void;
  moveSpeed?: number;
  initialPosition?: [number, number, number];
  initialTarget?: [number, number, number];
  parcelWidth?: number;
  parcelDepth?: number;
  /** Called when user clicks an element (id) */
  onElementClick?: (elementId: string) => void;
}

export interface ControlsHandle {
  resetCamera: () => void;
  setMode: (mode: CameraMode) => void;
}

// ---------------------------------------------------------------------------
// Keyboard state tracking
// ---------------------------------------------------------------------------

const pressedKeys = new Set<string>();

function onKeyDown(e: KeyboardEvent) {
  pressedKeys.add(e.code);
}
function onKeyUp(e: KeyboardEvent) {
  pressedKeys.delete(e.code);
}

// ---------------------------------------------------------------------------
// First-person movement system
// ---------------------------------------------------------------------------

const FirstPersonMovement: FC<{
  speed: number;
}> = ({ speed }) => {
  const { camera } = useThree();
  const velocity = useRef(new THREE.Vector3());
  const direction = useRef(new THREE.Vector3());
  const verticalVelocity = useRef(0);
  const isOnGround = useRef(true);
  const EYE_HEIGHT = 5.5;
  const GRAVITY = -30;
  const JUMP_FORCE = 12;

  useFrame((_, delta) => {
    const clampedDelta = Math.min(delta, 0.1);

    // Movement direction from WASD
    direction.current.set(0, 0, 0);
    if (pressedKeys.has('KeyW') || pressedKeys.has('ArrowUp')) direction.current.z -= 1;
    if (pressedKeys.has('KeyS') || pressedKeys.has('ArrowDown')) direction.current.z += 1;
    if (pressedKeys.has('KeyA') || pressedKeys.has('ArrowLeft')) direction.current.x -= 1;
    if (pressedKeys.has('KeyD') || pressedKeys.has('ArrowRight')) direction.current.x += 1;

    direction.current.normalize();

    // Apply camera rotation to movement direction
    const euler = new THREE.Euler(0, camera.rotation.y, 0, 'YXZ');
    direction.current.applyEuler(euler);

    // Horizontal velocity with damping
    velocity.current.x = direction.current.x * speed;
    velocity.current.z = direction.current.z * speed;

    // Jump
    if (pressedKeys.has('Space') && isOnGround.current) {
      verticalVelocity.current = JUMP_FORCE;
      isOnGround.current = false;
    }

    // Gravity
    verticalVelocity.current += GRAVITY * clampedDelta;

    // Apply movement
    camera.position.x += velocity.current.x * clampedDelta;
    camera.position.z += velocity.current.z * clampedDelta;
    camera.position.y += verticalVelocity.current * clampedDelta;

    // Ground collision
    if (camera.position.y <= EYE_HEIGHT) {
      camera.position.y = EYE_HEIGHT;
      verticalVelocity.current = 0;
      isOnGround.current = true;
    }

    // Sprint with shift
    if (pressedKeys.has('ShiftLeft') || pressedKeys.has('ShiftRight')) {
      velocity.current.multiplyScalar(2);
    }
  });

  return null;
};

// ---------------------------------------------------------------------------
// Minimap component — renders a top-down view
// ---------------------------------------------------------------------------

const Minimap: FC<{
  parcelWidth: number;
  parcelDepth: number;
}> = ({ parcelWidth, parcelDepth }) => {
  const { camera } = useThree();
  const indicatorRef = useRef<THREE.Mesh>(null);
  const dirRef = useRef<THREE.Mesh>(null);

  useFrame(() => {
    if (indicatorRef.current) {
      // Map camera world position to minimap coordinates
      const mapSize = 120;
      const scaleX = mapSize / Math.max(parcelWidth, 100);
      const scaleZ = mapSize / Math.max(parcelDepth, 100);
      indicatorRef.current.position.set(
        camera.position.x * scaleX,
        camera.position.z * scaleZ,
        0,
      );
    }
    if (dirRef.current) {
      // Direction indicator
      const forward = new THREE.Vector3(0, 0, -1);
      forward.applyQuaternion(camera.quaternion);
      const angle = Math.atan2(forward.x, forward.z);
      dirRef.current.rotation.z = -angle;
    }
  });

  return (
    <Html
      center={false}
      fullscreen={false}
      style={{
        position: 'fixed',
        bottom: '16px',
        right: '16px',
        width: '140px',
        height: '140px',
        background: 'rgba(0,0,0,0.65)',
        borderRadius: '8px',
        border: '2px solid rgba(255,255,255,0.2)',
        overflow: 'hidden',
        pointerEvents: 'none',
      }}
      portal={{ current: document.body } as React.RefObject<HTMLElement>}
    >
      <div style={{ position: 'relative', width: '100%', height: '100%' }}>
        {/* Parcel outline */}
        <div
          style={{
            position: 'absolute',
            top: '50%',
            left: '50%',
            transform: 'translate(-50%, -50%)',
            width: '80%',
            height: '80%',
            border: '1px solid rgba(255,255,255,0.4)',
            borderRadius: '2px',
          }}
        />
        {/* Camera indicator — we update this via a separate mechanism */}
        <MinimapDot parcelWidth={parcelWidth} parcelDepth={parcelDepth} />
      </div>
    </Html>
  );
};

const MinimapDot: FC<{ parcelWidth: number; parcelDepth: number }> = ({
  parcelWidth,
  parcelDepth,
}) => {
  const { camera } = useThree();
  const dotRef = useRef<HTMLDivElement>(null);

  useFrame(() => {
    if (dotRef.current) {
      const hw = Math.max(parcelWidth, 100) / 2;
      const hd = Math.max(parcelDepth, 100) / 2;
      const normX = ((camera.position.x / hw) * 0.4 + 0.5) * 100;
      const normZ = ((camera.position.z / hd) * 0.4 + 0.5) * 100;
      dotRef.current.style.left = `${Math.max(5, Math.min(95, normX))}%`;
      dotRef.current.style.top = `${Math.max(5, Math.min(95, normZ))}%`;

      // Direction arrow
      const forward = new THREE.Vector3(0, 0, -1);
      forward.applyQuaternion(camera.quaternion);
      const angle = Math.atan2(forward.x, forward.z);
      dotRef.current.style.transform = `translate(-50%, -50%) rotate(${-angle}rad)`;
    }
  });

  return (
    <div
      ref={dotRef}
      style={{
        position: 'absolute',
        width: '0',
        height: '0',
        borderLeft: '5px solid transparent',
        borderRight: '5px solid transparent',
        borderBottom: '12px solid #44bbff',
        filter: 'drop-shadow(0 0 3px #44bbff)',
      }}
    />
  );
};

// ---------------------------------------------------------------------------
// PUBLIC: Controls component
// ---------------------------------------------------------------------------

const Controls = forwardRef<ControlsHandle, ControlsProps>(
  (
    {
      mode,
      onModeChange,
      moveSpeed = 18,
      initialPosition = [-30, 25, -30],
      initialTarget = [0, 0, 0],
      parcelWidth = 100,
      parcelDepth = 80,
    },
    ref,
  ) => {
    const { camera } = useThree();
    const orbitRef = useRef<any>(null);
    const pointerLockRef = useRef<any>(null);
    const [isLocked, setIsLocked] = useState(false);

    // Set initial camera position
    useEffect(() => {
      camera.position.set(...initialPosition);
      camera.lookAt(...initialTarget);
    }, []); // Only on mount

    // Keyboard listeners
    useEffect(() => {
      window.addEventListener('keydown', onKeyDown);
      window.addEventListener('keyup', onKeyUp);
      return () => {
        window.removeEventListener('keydown', onKeyDown);
        window.removeEventListener('keyup', onKeyUp);
        pressedKeys.clear();
      };
    }, []);

    // Toggle mode with 'V' key
    useEffect(() => {
      const handleToggle = (e: KeyboardEvent) => {
        if (e.code === 'KeyV' && !e.ctrlKey && !e.metaKey) {
          const newMode: CameraMode = mode === 'orbit' ? 'firstperson' : 'orbit';
          onModeChange?.(newMode);
        }
      };
      window.addEventListener('keydown', handleToggle);
      return () => window.removeEventListener('keydown', handleToggle);
    }, [mode, onModeChange]);

    // Reset camera handler
    const resetCamera = useCallback(() => {
      camera.position.set(...initialPosition);
      camera.lookAt(...initialTarget);
      if (orbitRef.current) {
        orbitRef.current.target.set(...initialTarget);
        orbitRef.current.update();
      }
    }, [camera, initialPosition, initialTarget]);

    useImperativeHandle(ref, () => ({
      resetCamera,
      setMode: (m: CameraMode) => onModeChange?.(m),
    }));

    return (
      <>
        {mode === 'orbit' ? (
          <OrbitControls
            ref={orbitRef}
            target={initialTarget}
            maxPolarAngle={Math.PI / 2 - 0.05}
            minDistance={5}
            maxDistance={200}
            enableDamping
            dampingFactor={0.08}
            rotateSpeed={0.5}
          />
        ) : (
          <>
            <PointerLockControls
              ref={pointerLockRef}
              onLock={() => setIsLocked(true)}
              onUnlock={() => setIsLocked(false)}
            />
            <FirstPersonMovement speed={moveSpeed} />
            {!isLocked && (
              <Html
                center
                style={{
                  pointerEvents: 'none',
                  textAlign: 'center',
                  color: '#ffffff',
                  fontFamily: 'system-ui, sans-serif',
                  fontSize: '16px',
                  textShadow: '0 2px 8px rgba(0,0,0,0.7)',
                  whiteSpace: 'nowrap',
                }}
              >
                <div
                  style={{
                    background: 'rgba(0,0,0,0.7)',
                    padding: '16px 28px',
                    borderRadius: '12px',
                    pointerEvents: 'auto',
                    cursor: 'pointer',
                  }}
                  onClick={() => {
                    (pointerLockRef.current as any)?.lock?.();
                  }}
                >
                  <div style={{ fontSize: '20px', fontWeight: 600, marginBottom: '6px' }}>
                    Click to explore
                  </div>
                  <div style={{ fontSize: '13px', opacity: 0.7 }}>
                    WASD to move | Mouse to look | Space to jump | ESC to exit
                  </div>
                </div>
              </Html>
            )}
          </>
        )}

        {/* Minimap */}
        <Minimap parcelWidth={parcelWidth} parcelDepth={parcelDepth} />
      </>
    );
  },
);

Controls.displayName = 'Controls';

export default Controls;
