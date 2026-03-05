/**
 * MarbleWorlds — Interactive 3D world viewer for the BATHS dashboard.
 *
 * Fetches real Marble API worlds from both DOMES and SPHERES backends
 * and renders them as 360 panoramic images or Gaussian splats.
 *
 * No hardcoded Three.js scenes. All content from the Marble API.
 */

import { useState, useEffect, useRef, useCallback } from 'react'
import { Canvas, useThree, useFrame } from '@react-three/fiber'
import { OrbitControls } from '@react-three/drei'
import * as THREE from 'three'

// ─── Types ──────────────────────────────────────────────────

interface MarbleWorldEntry {
  key: string
  title: string
  group: 'DOMES' | 'SPHERES'
  splatUrl: string
  panoUrl: string
}

// ─── API helpers ────────────────────────────────────────────

function getBackendBase(port: number): string {
  if (typeof window !== 'undefined') {
    const host = window.location.hostname
    const match = host.match(/^(.+)-(\d+)(\.app\.github\.dev)$/)
    if (match) {
      return `https://${match[1]}-${port}${match[3]}`
    }
  }
  return `http://localhost:${port}`
}

async function fetchAllWorlds(): Promise<MarbleWorldEntry[]> {
  const worlds: MarbleWorldEntry[] = []

  // Fetch DOMES worlds (3 worlds from port 8003)
  try {
    const resp = await fetch(`${getBackendBase(8003)}/api/marble/worlds`)
    if (resp.ok) {
      const data = await resp.json()
      for (const w of data.worlds || []) {
        if (w.splatUrl || w.panoUrl) {
          worlds.push({
            key: w.key,
            title: w.title || w.key,
            group: 'DOMES',
            splatUrl: w.splatUrl || '',
            panoUrl: w.panoUrl || '',
          })
        }
      }
    }
  } catch (err) {
    console.warn('Failed to fetch DOMES worlds:', err)
  }

  // Fetch SPHERES worlds (10 worlds from port 8004)
  try {
    const resp = await fetch(`${getBackendBase(8004)}/api/marble/worlds`)
    if (resp.ok) {
      const data = await resp.json()
      for (const w of (Array.isArray(data) ? data : data.worlds || [])) {
        if (w.splat_url || w.pano_url) {
          worlds.push({
            key: `spheres-${w.episode_num || w.slug}`,
            title: w.title || w.slug || `Episode ${w.episode_num}`,
            group: 'SPHERES',
            splatUrl: w.splat_url || '',
            panoUrl: w.pano_url || '',
          })
        }
      }
    }
  } catch (err) {
    console.warn('Failed to fetch SPHERES worlds:', err)
  }

  return worlds
}

// ─── PanoWorld — 360 panoramic image ────────────────────────

function PanoWorld({ url }: { url: string }) {
  const { camera } = useThree()
  const [texture, setTexture] = useState<THREE.Texture | null>(null)

  useEffect(() => {
    camera.position.set(0, 0, 0.01)
    camera.lookAt(0, 0, -1)

    const loader = new THREE.TextureLoader()
    loader.load(
      url,
      (tex) => {
        tex.colorSpace = THREE.SRGBColorSpace
        setTexture(tex)
      },
      undefined,
      (err) => console.warn('Pano load failed:', err)
    )

    return () => {
      if (texture) texture.dispose()
    }
  }, [url])

  if (!texture) {
    return (
      <mesh>
        <sphereGeometry args={[0.3, 16, 16]} />
        <meshBasicMaterial color="#ffffff" wireframe />
      </mesh>
    )
  }

  return (
    <mesh>
      <sphereGeometry args={[50, 64, 32]} />
      <meshBasicMaterial map={texture} side={THREE.BackSide} />
    </mesh>
  )
}

// ─── SplatWorld — Gaussian splat via SparkJS ────────────────

function SplatWorld({ url }: { url: string }) {
  const { gl, scene } = useThree()
  const sparkRef = useRef<any>(null)
  const splatRef = useRef<any>(null)

  useEffect(() => {
    let disposed = false

    async function init() {
      try {
        const { SparkRenderer, SplatMesh } = await import('@sparkjsdev/spark')
        if (disposed) return

        const spark = new SparkRenderer({ renderer: gl })
        sparkRef.current = spark
        scene.add(spark)

        const splat = new SplatMesh({ url })
        splatRef.current = splat
        scene.add(splat)
        await splat.initialized
      } catch (err) {
        console.warn('Splat load failed:', err)
      }
    }

    init()

    return () => {
      disposed = true
      if (splatRef.current) {
        scene.remove(splatRef.current)
        splatRef.current.dispose?.()
      }
      if (sparkRef.current) {
        scene.remove(sparkRef.current)
        sparkRef.current.dispose?.()
      }
    }
  }, [url, gl, scene])

  useFrame(() => {
    if (sparkRef.current) {
      sparkRef.current.update({ scene })
    }
  })

  return null
}

// ─── Styles ─────────────────────────────────────────────────

const mono = { fontFamily: '"JetBrains Mono", "SF Mono", monospace' }

// ─── Main component ─────────────────────────────────────────

export default function MarbleWorlds() {
  const [worlds, setWorlds] = useState<MarbleWorldEntry[]>([])
  const [activeIndex, setActiveIndex] = useState(0)
  const [loading, setLoading] = useState(true)
  const [canvasReady, setCanvasReady] = useState(false)

  useEffect(() => {
    let cancelled = false
    async function load() {
      const data = await fetchAllWorlds()
      if (!cancelled) {
        setWorlds(data)
        setLoading(false)
      }
    }
    load()
    return () => { cancelled = true }
  }, [])

  const handleCanvasCreated = useCallback(() => {
    setCanvasReady(true)
  }, [])

  const activeWorld = worlds[activeIndex]
  const hasSplat = !!activeWorld?.splatUrl
  const hasPano = !!activeWorld?.panoUrl

  return (
    <div style={{ marginTop: 28, padding: '0 4px' }}>
      {/* Header */}
      <h2
        style={{
          fontSize: 13,
          fontWeight: 700,
          letterSpacing: '0.12em',
          textTransform: 'uppercase',
          color: '#666',
          margin: '0 0 12px 0',
        }}
      >
        MARBLE WORLDS
      </h2>

      {loading ? (
        <div
          style={{
            aspectRatio: '4 / 3',
            backgroundColor: '#111111',
            borderRadius: 12,
            border: '1px solid #1A1A1A',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: '#444',
            fontSize: 12,
            ...mono,
          }}
        >
          Loading Marble worlds...
        </div>
      ) : worlds.length === 0 ? (
        <div
          style={{
            aspectRatio: '4 / 3',
            backgroundColor: '#111111',
            borderRadius: 12,
            border: '1px solid #1A1A1A',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: '#666',
            fontSize: 12,
            ...mono,
          }}
        >
          No Marble worlds available. Start the viz backends.
        </div>
      ) : (
        <>
          {/* World tabs */}
          <div
            style={{
              display: 'flex',
              gap: 0,
              overflowX: 'auto',
              borderBottom: '1px solid #222',
              marginBottom: 0,
            }}
          >
            {worlds.map((w, i) => {
              const isActive = i === activeIndex
              return (
                <button
                  key={w.key}
                  onClick={() => {
                    setCanvasReady(false)
                    setActiveIndex(i)
                  }}
                  style={{
                    padding: '8px 14px',
                    background: 'transparent',
                    border: 'none',
                    borderBottom: isActive
                      ? '2px solid #C4A265'
                      : '2px solid transparent',
                    color: isActive ? '#C4A265' : '#555',
                    fontSize: 10,
                    letterSpacing: '0.08em',
                    textTransform: 'uppercase',
                    cursor: 'pointer',
                    whiteSpace: 'nowrap',
                    flexShrink: 0,
                    ...mono,
                  }}
                >
                  {w.title}
                </button>
              )
            })}
          </div>

          {/* 3D viewer */}
          <div
            style={{
              aspectRatio: '4 / 3',
              backgroundColor: '#0D0D0D',
              borderRadius: '0 0 12px 12px',
              border: '1px solid #1A1A1A',
              borderTop: 'none',
              overflow: 'hidden',
              position: 'relative',
            }}
          >
            {/* Loading spinner */}
            {!canvasReady && (
              <div
                style={{
                  position: 'absolute',
                  inset: 0,
                  zIndex: 10,
                  display: 'flex',
                  flexDirection: 'column',
                  alignItems: 'center',
                  justifyContent: 'center',
                  gap: 12,
                  color: '#555',
                }}
              >
                <div
                  style={{
                    width: 28,
                    height: 28,
                    border: '2px solid rgba(255,255,255,0.1)',
                    borderTopColor: '#C4A265',
                    borderRadius: '50%',
                    animation: 'marbleSpin 1s linear infinite',
                  }}
                />
                <span style={{ fontSize: 10, letterSpacing: '0.1em', ...mono }}>
                  Loading...
                </span>
                <style>{`@keyframes marbleSpin { to { transform: rotate(360deg) } }`}</style>
              </div>
            )}

            <Canvas
              dpr={[1, 1.5]}
              gl={{ antialias: true, toneMapping: THREE.ACESFilmicToneMapping }}
              camera={{
                position: hasPano ? [0, 0, 0.01] : [0, 2, 5],
                fov: 70,
                near: 0.1,
                far: 100,
              }}
              onCreated={handleCanvasCreated}
              style={{
                width: '100%',
                height: '100%',
                opacity: canvasReady ? 1 : 0,
                transition: 'opacity 0.6s ease',
              }}
            >
              {activeWorld && (
                hasSplat ? (
                  <SplatWorld key={activeWorld.key} url={activeWorld.splatUrl} />
                ) : hasPano ? (
                  <PanoWorld key={activeWorld.key} url={activeWorld.panoUrl} />
                ) : null
              )}
              <OrbitControls
                enablePan={false}
                enableZoom
                minDistance={hasPano ? 0.01 : 1}
                maxDistance={hasPano ? 0.02 : 20}
                maxPolarAngle={hasPano ? Math.PI : Math.PI * 0.85}
                autoRotate
                autoRotateSpeed={0.5}
                enableDamping
                dampingFactor={0.05}
              />
            </Canvas>

            {/* Source badge */}
            {canvasReady && activeWorld && (
              <div
                style={{
                  position: 'absolute',
                  bottom: 8,
                  right: 8,
                  padding: '4px 8px',
                  borderRadius: 6,
                  backgroundColor: 'rgba(0,0,0,0.6)',
                  color: '#C4A265',
                  fontSize: 9,
                  letterSpacing: '0.1em',
                  textTransform: 'uppercase',
                  pointerEvents: 'none',
                  ...mono,
                }}
              >
                {activeWorld.group} / Marble API
              </div>
            )}

            {/* Drag hint */}
            {canvasReady && (
              <div
                style={{
                  position: 'absolute',
                  top: 8,
                  left: 0,
                  right: 0,
                  textAlign: 'center',
                  pointerEvents: 'none',
                  color: 'rgba(196, 162, 101, 0.3)',
                  fontSize: 9,
                  letterSpacing: '0.15em',
                  textTransform: 'uppercase',
                  ...mono,
                }}
              >
                drag to explore
              </div>
            )}
          </div>
        </>
      )}
    </div>
  )
}
