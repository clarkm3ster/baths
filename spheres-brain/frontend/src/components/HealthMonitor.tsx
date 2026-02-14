// -----------------------------------------------------------------
// HealthMonitor -- Service health & uptime dashboard
// -----------------------------------------------------------------

import { Shield, ArrowUp, ArrowDown, Minus, Clock } from 'lucide-react';
import type { HealthStatus } from '../utils/api';

interface Props {
  health: HealthStatus | null;
  loading: boolean;
}

const STATUS_COLORS: Record<string, string> = {
  healthy: 'var(--green)',
  degraded: 'var(--yellow)',
  unhealthy: 'var(--red)',
};

const STATUS_ICONS: Record<string, React.ReactNode> = {
  healthy: <ArrowUp size={10} />,
  degraded: <Minus size={10} />,
  unhealthy: <ArrowDown size={10} />,
};

const PLACEHOLDER_HEALTH: HealthStatus = {
  status: 'healthy',
  uptime_seconds: 864000,
  services: [
    {
      name: 'SPHERES Assets',
      status: 'healthy',
      latency_ms: 42,
      uptime_pct: 99.97,
      last_check: '2026-02-14T10:22:00Z',
    },
    {
      name: 'SPHERES Legal',
      status: 'healthy',
      latency_ms: 38,
      uptime_pct: 99.94,
      last_check: '2026-02-14T10:22:00Z',
    },
    {
      name: 'SPHERES Studio',
      status: 'healthy',
      latency_ms: 55,
      uptime_pct: 99.89,
      last_check: '2026-02-14T10:22:00Z',
    },
    {
      name: 'SPHERES Viz',
      status: 'healthy',
      latency_ms: 31,
      uptime_pct: 99.99,
      last_check: '2026-02-14T10:22:00Z',
    },
  ],
};

function formatUptime(seconds: number): string {
  const days = Math.floor(seconds / 86400);
  const hours = Math.floor((seconds % 86400) / 3600);
  const mins = Math.floor((seconds % 3600) / 60);
  return `${days}d ${hours}h ${mins}m`;
}

function latencyColor(ms: number): string {
  if (ms < 50) return 'var(--green)';
  if (ms < 150) return 'var(--yellow)';
  return 'var(--red)';
}

// Tiny uptime sparkline (static bars representing last 7 "periods")
function UptimeBars({ uptime_pct }: { uptime_pct: number }) {
  // Simulate 7 bar segments based on the uptime pct
  const bars = Array.from({ length: 7 }, (_, i) => {
    // Last bar might reflect degraded uptime
    if (i === 6 && uptime_pct < 99.9) return 'var(--yellow)';
    if (i === 5 && uptime_pct < 99.5) return 'var(--red)';
    return 'var(--green)';
  });

  return (
    <div style={{ display: 'flex', gap: 2, alignItems: 'flex-end' }}>
      {bars.map((color, i) => (
        <div
          key={i}
          style={{
            width: 3,
            height: 10 + Math.random() * 4,
            background: color,
            borderRadius: 1,
            opacity: 0.6 + i * 0.06,
          }}
        />
      ))}
    </div>
  );
}

export default function HealthMonitor({ health, loading }: Props) {
  const data = health || PLACEHOLDER_HEALTH;
  const overallColor = STATUS_COLORS[data.status] || 'var(--text-tertiary)';

  return (
    <div
      style={{
        background: 'var(--bg-card)',
        border: '1px solid var(--border)',
        borderRadius: 8,
        overflow: 'hidden',
        display: 'flex',
        flexDirection: 'column',
        height: '100%',
      }}
    >
      {/* Header */}
      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          padding: '10px 14px',
          borderBottom: '1px solid var(--border)',
          flexShrink: 0,
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
          <Shield size={12} style={{ color: 'var(--accent)' }} />
          <span
            style={{
              fontSize: 11,
              fontWeight: 600,
              textTransform: 'uppercase',
              letterSpacing: '0.06em',
              color: 'var(--text-secondary)',
            }}
          >
            System Health
          </span>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
          <span
            style={{
              width: 6,
              height: 6,
              borderRadius: '50%',
              background: overallColor,
              display: 'inline-block',
              boxShadow: `0 0 6px ${overallColor}`,
            }}
          />
          <span
            style={{
              fontSize: 10,
              fontWeight: 600,
              color: overallColor,
              textTransform: 'uppercase',
              letterSpacing: '0.04em',
            }}
          >
            {data.status}
          </span>
        </div>
      </div>

      {/* Overall uptime strip */}
      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          padding: '8px 14px',
          borderBottom: '1px solid var(--border)',
          background: 'var(--bg)',
          opacity: loading ? 0.4 : 1,
          transition: 'opacity 0.3s ease',
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: 5 }}>
          <Clock size={10} style={{ color: 'var(--text-tertiary)' }} />
          <span
            style={{
              fontSize: 10,
              color: 'var(--text-tertiary)',
              textTransform: 'uppercase',
              letterSpacing: '0.04em',
            }}
          >
            Uptime
          </span>
        </div>
        <span
          style={{
            fontFamily: 'var(--mono)',
            fontSize: 12,
            fontWeight: 600,
            color: 'var(--text)',
          }}
        >
          {formatUptime(data.uptime_seconds)}
        </span>
      </div>

      {/* Service rows */}
      <div
        style={{
          flex: 1,
          overflowY: 'auto',
          opacity: loading ? 0.4 : 1,
          transition: 'opacity 0.3s ease',
        }}
      >
        {data.services.map((svc, idx) => {
          const svcColor = STATUS_COLORS[svc.status] || 'var(--text-tertiary)';
          return (
            <div
              key={svc.name}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: 10,
                padding: '10px 14px',
                borderBottom:
                  idx < data.services.length - 1
                    ? '1px solid var(--border)'
                    : 'none',
              }}
            >
              {/* Status icon */}
              <div
                style={{
                  width: 22,
                  height: 22,
                  borderRadius: 4,
                  background: `${svcColor}15`,
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  color: svcColor,
                  flexShrink: 0,
                }}
              >
                {STATUS_ICONS[svc.status]}
              </div>

              {/* Name */}
              <div style={{ flex: 1, minWidth: 0 }}>
                <div style={{ fontSize: 12, fontWeight: 600 }}>
                  {svc.name}
                </div>
                <div
                  style={{
                    fontSize: 10,
                    color: 'var(--text-tertiary)',
                    display: 'flex',
                    gap: 8,
                    marginTop: 2,
                  }}
                >
                  <span
                    style={{
                      fontFamily: 'var(--mono)',
                      color: latencyColor(svc.latency_ms),
                    }}
                  >
                    {svc.latency_ms}ms
                  </span>
                  <span style={{ fontFamily: 'var(--mono)' }}>
                    {svc.uptime_pct}%
                  </span>
                </div>
              </div>

              {/* Uptime bars */}
              <UptimeBars uptime_pct={svc.uptime_pct} />
            </div>
          );
        })}
      </div>
    </div>
  );
}
