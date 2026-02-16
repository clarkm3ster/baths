import { useState, useEffect, useCallback, useRef } from 'react'

// ── Types ──────────────────────────────────────────────────────────────

interface AppConfig {
  name: string
  backendPort: number
  frontendPort: number
  group: 'DOMES' | 'SPHERES'
}

interface AppStatus extends AppConfig {
  healthy: boolean
  lastChecked: Date | null
  checking: boolean
}

// ── App Registry ───────────────────────────────────────────────────────

const APPS: AppConfig[] = [
  // DOMES (12 apps)
  { name: 'domes-legal-research', backendPort: 8000, frontendPort: 5173, group: 'DOMES' },
  { name: 'domes-data-research', backendPort: 8001, frontendPort: 5174, group: 'DOMES' },
  { name: 'domes-profile-research', backendPort: 8002, frontendPort: 5175, group: 'DOMES' },
  { name: 'domes-legal', backendPort: 8003, frontendPort: 5177, group: 'DOMES' },
  { name: 'domes-datamap', backendPort: 8013, frontendPort: 5176, group: 'DOMES' },
  { name: 'domes-profiles', backendPort: 8004, frontendPort: 5178, group: 'DOMES' },
  { name: 'domes-contracts', backendPort: 8014, frontendPort: 5182, group: 'DOMES' },
  { name: 'domes-architect', backendPort: 8015, frontendPort: 5183, group: 'DOMES' },
  { name: 'domes-viz', backendPort: 8005, frontendPort: 5179, group: 'DOMES' },
  { name: 'domes-brain', backendPort: 8006, frontendPort: 5180, group: 'DOMES' },
  { name: 'domes-lab', backendPort: 8007, frontendPort: 5181, group: 'DOMES' },
  { name: 'domes-flourishing', backendPort: 8016, frontendPort: 5184, group: 'DOMES' },
  // SPHERES (6 apps)
  { name: 'spheres-assets', backendPort: 8017, frontendPort: 5185, group: 'SPHERES' },
  { name: 'spheres-legal', backendPort: 8018, frontendPort: 5186, group: 'SPHERES' },
  { name: 'spheres-studio', backendPort: 8019, frontendPort: 5190, group: 'SPHERES' },
  { name: 'spheres-viz', backendPort: 8008, frontendPort: 5200, group: 'SPHERES' },
  { name: 'spheres-brain', backendPort: 8009, frontendPort: 5210, group: 'SPHERES' },
  { name: 'spheres-lab', backendPort: 8010, frontendPort: 5220, group: 'SPHERES' },
]

const TOTAL_APPS = APPS.length // 18

// ── Health Check ───────────────────────────────────────────────────────

async function checkHealth(backendPort: number): Promise<boolean> {
  const controller = new AbortController()
  const timeout = setTimeout(() => controller.abort(), 3000)
  try {
    const res = await fetch(`http://localhost:${backendPort}/api/health`, {
      signal: controller.signal,
    })
    clearTimeout(timeout)
    return res.ok
  } catch {
    clearTimeout(timeout)
    return false
  }
}

// ── Helpers ────────────────────────────────────────────────────────────

function formatTime(date: Date | null): string {
  if (!date) return '--:--:--'
  return date.toLocaleTimeString('en-US', {
    hour12: false,
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
  })
}

function formatAppName(name: string): string {
  // "domes-legal-research" -> "Legal Research"
  const parts = name.split('-')
  // Remove the first part (domes/spheres)
  const rest = parts.slice(1)
  return rest.map(p => p.charAt(0).toUpperCase() + p.slice(1)).join(' ')
}

// ── Styles ─────────────────────────────────────────────────────────────

const mono: React.CSSProperties = {
  fontFamily: "'JetBrains Mono', monospace",
}

// ── Components ─────────────────────────────────────────────────────────

function StatusDot({ healthy, checking }: { healthy: boolean; checking: boolean }) {
  return (
    <span
      style={{
        display: 'inline-block',
        width: 12,
        height: 12,
        borderRadius: '50%',
        backgroundColor: checking ? '#888888' : healthy ? '#00FF00' : '#FF0000',
        boxShadow: checking
          ? '0 0 6px rgba(136,136,136,0.5)'
          : healthy
            ? '0 0 8px rgba(0,255,0,0.6)'
            : '0 0 8px rgba(255,0,0,0.6)',
        transition: 'all 0.3s ease',
        flexShrink: 0,
      }}
    />
  )
}

function ProgressBar({ running, total }: { running: number; total: number }) {
  const pct = total > 0 ? (running / total) * 100 : 0
  return (
    <div
      style={{
        width: '100%',
        height: 8,
        backgroundColor: '#1A1A1A',
        borderRadius: 4,
        overflow: 'hidden',
        marginTop: 8,
      }}
    >
      <div
        style={{
          width: `${pct}%`,
          height: '100%',
          backgroundColor: running === total ? '#00FF00' : running > 0 ? '#FFAA00' : '#FF0000',
          borderRadius: 4,
          transition: 'width 0.5s ease, background-color 0.5s ease',
        }}
      />
    </div>
  )
}

function AppCard({ app }: { app: AppStatus }) {
  const [hovered, setHovered] = useState(false)

  return (
    <a
      href={`http://localhost:${app.frontendPort}`}
      target="_blank"
      rel="noopener noreferrer"
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={() => setHovered(false)}
      style={{
        display: 'flex',
        alignItems: 'center',
        gap: 14,
        padding: '16px 18px',
        minHeight: 72,
        backgroundColor: hovered ? '#1A1A1A' : '#111111',
        borderRadius: 12,
        border: `1px solid ${hovered ? '#333' : '#1A1A1A'}`,
        cursor: 'pointer',
        textDecoration: 'none',
        color: '#FFFFFF',
        transition: 'all 0.2s ease',
        WebkitTapHighlightColor: 'transparent',
      }}
    >
      {/* Status dot */}
      <StatusDot healthy={app.healthy} checking={app.checking} />

      {/* App info */}
      <div style={{ flex: 1, minWidth: 0 }}>
        <div
          style={{
            fontSize: 15,
            fontWeight: 600,
            lineHeight: '20px',
            whiteSpace: 'nowrap',
            overflow: 'hidden',
            textOverflow: 'ellipsis',
          }}
        >
          {formatAppName(app.name)}
        </div>
        <div
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: 12,
            marginTop: 4,
            fontSize: 12,
            color: '#888',
            ...mono,
          }}
        >
          <span>BE:{app.backendPort}</span>
          <span>FE:{app.frontendPort}</span>
        </div>
      </div>

      {/* Timestamp + arrow */}
      <div
        style={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'flex-end',
          gap: 2,
          flexShrink: 0,
        }}
      >
        <span
          style={{
            fontSize: 11,
            color: '#666',
            ...mono,
          }}
        >
          {formatTime(app.lastChecked)}
        </span>
        <span
          style={{
            fontSize: 14,
            color: '#555',
            transition: 'color 0.2s ease',
            ...(hovered ? { color: '#AAA' } : {}),
          }}
        >
          &#8599;
        </span>
      </div>
    </a>
  )
}

function SectionHeader({ title, count, running }: { title: string; count: number; running: number }) {
  return (
    <div
      style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        padding: '0 4px',
        marginTop: 28,
        marginBottom: 12,
      }}
    >
      <h2
        style={{
          fontSize: 13,
          fontWeight: 700,
          letterSpacing: '0.12em',
          textTransform: 'uppercase',
          color: '#666',
        }}
      >
        {title}
      </h2>
      <span
        style={{
          fontSize: 12,
          color: '#555',
          ...mono,
        }}
      >
        {running}/{count}
      </span>
    </div>
  )
}

// ── Main App ───────────────────────────────────────────────────────────

function App() {
  const [statuses, setStatuses] = useState<AppStatus[]>(() =>
    APPS.map(app => ({
      ...app,
      healthy: false,
      lastChecked: null,
      checking: true,
    }))
  )
  const [countdown, setCountdown] = useState(30)
  const intervalRef = useRef<ReturnType<typeof setInterval> | null>(null)
  const countdownRef = useRef<ReturnType<typeof setInterval> | null>(null)

  const runHealthChecks = useCallback(async () => {
    // Set all to checking
    setStatuses(prev =>
      prev.map(s => ({ ...s, checking: true }))
    )

    const results = await Promise.allSettled(
      APPS.map(app => checkHealth(app.backendPort))
    )

    const now = new Date()
    setStatuses(prev =>
      prev.map((s, i) => ({
        ...s,
        healthy: results[i].status === 'fulfilled' && (results[i] as PromiseFulfilledResult<boolean>).value,
        lastChecked: now,
        checking: false,
      }))
    )

    // Reset countdown
    setCountdown(30)
  }, [])

  useEffect(() => {
    // Initial health check
    runHealthChecks()

    // Auto-refresh every 30 seconds
    intervalRef.current = setInterval(runHealthChecks, 30000)

    // Countdown timer
    countdownRef.current = setInterval(() => {
      setCountdown(prev => (prev > 0 ? prev - 1 : 30))
    }, 1000)

    return () => {
      if (intervalRef.current) clearInterval(intervalRef.current)
      if (countdownRef.current) clearInterval(countdownRef.current)
    }
  }, [runHealthChecks])

  const runningCount = statuses.filter(s => s.healthy).length
  const domesApps = statuses.filter(s => s.group === 'DOMES')
  const spheresApps = statuses.filter(s => s.group === 'SPHERES')
  const domesRunning = domesApps.filter(s => s.healthy).length
  const spheresRunning = spheresApps.filter(s => s.healthy).length

  const anyChecking = statuses.some(s => s.checking)

  return (
    <div
      style={{
        maxWidth: 520,
        margin: '0 auto',
        padding: '24px 16px 48px',
        minHeight: '100vh',
      }}
    >
      {/* Header */}
      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          marginBottom: 8,
        }}
      >
        <h1
          style={{
            fontSize: 22,
            fontWeight: 800,
            letterSpacing: '-0.02em',
          }}
        >
          BATHS
        </h1>
        <button
          onClick={runHealthChecks}
          disabled={anyChecking}
          style={{
            background: 'none',
            border: '1px solid #333',
            borderRadius: 8,
            color: anyChecking ? '#555' : '#AAA',
            fontSize: 12,
            padding: '6px 14px',
            cursor: anyChecking ? 'not-allowed' : 'pointer',
            minHeight: 44,
            minWidth: 44,
            display: 'flex',
            alignItems: 'center',
            gap: 6,
            ...mono,
            transition: 'all 0.2s ease',
          }}
        >
          <span
            style={{
              display: 'inline-block',
              transition: 'transform 0.3s ease',
              ...(anyChecking ? { animation: 'spin 1s linear infinite' } : {}),
            }}
          >
            &#8635;
          </span>
          {countdown}s
        </button>
      </div>

      {/* Summary */}
      <div
        style={{
          padding: '18px 20px',
          backgroundColor: '#111111',
          borderRadius: 14,
          border: '1px solid #1A1A1A',
        }}
      >
        <div
          style={{
            display: 'flex',
            alignItems: 'baseline',
            gap: 8,
          }}
        >
          <span
            style={{
              fontSize: 36,
              fontWeight: 800,
              lineHeight: 1,
              color: runningCount === TOTAL_APPS ? '#00FF00' : runningCount > 0 ? '#FFAA00' : '#FF0000',
              ...mono,
            }}
          >
            {runningCount}
          </span>
          <span
            style={{
              fontSize: 14,
              color: '#666',
            }}
          >
            / {TOTAL_APPS} apps running
          </span>
        </div>
        <ProgressBar running={runningCount} total={TOTAL_APPS} />
      </div>

      {/* DOMES Section */}
      <SectionHeader title="DOMES" count={domesApps.length} running={domesRunning} />
      <div
        style={{
          display: 'flex',
          flexDirection: 'column',
          gap: 8,
        }}
      >
        {domesApps.map(app => (
          <AppCard key={app.name} app={app} />
        ))}
      </div>

      {/* SPHERES Section */}
      <SectionHeader title="SPHERES" count={spheresApps.length} running={spheresRunning} />
      <div
        style={{
          display: 'flex',
          flexDirection: 'column',
          gap: 8,
        }}
      >
        {spheresApps.map(app => (
          <AppCard key={app.name} app={app} />
        ))}
      </div>

      {/* Footer */}
      <div
        style={{
          textAlign: 'center',
          marginTop: 32,
          fontSize: 11,
          color: '#444',
          ...mono,
        }}
      >
        Auto-refreshes every 30s
      </div>

      {/* Keyframe animation for spinner */}
      <style>{`
        @keyframes spin {
          from { transform: rotate(0deg); }
          to { transform: rotate(360deg); }
        }
      `}</style>
    </div>
  )
}

export default App
