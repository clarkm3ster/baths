// ─────────────────────────────────────────────────────────────
// ServiceGrid — Connected SPHERES apps overview
// ─────────────────────────────────────────────────────────────

import { useState } from 'react';
import { ExternalLink, Zap, Globe, Radio, Wifi } from 'lucide-react';
import type { ServiceInfo } from '../utils/api';

interface Props {
  services: ServiceInfo[];
  loading: boolean;
}

const APP_ICONS: Record<string, React.ReactNode> = {
  assets: <Globe size={16} />,
  legal: <Zap size={16} />,
  studio: <Radio size={16} />,
  viz: <Wifi size={16} />,
};

const STATUS_COLORS: Record<string, string> = {
  online: 'var(--green)',
  degraded: 'var(--yellow)',
  offline: 'var(--red)',
};

const FALLBACK_SERVICES: ServiceInfo[] = [
  {
    name: 'SPHERES Assets',
    slug: 'assets',
    description: 'Parcel intelligence & vacancy data for Philadelphia',
    status: 'online',
    url: 'http://localhost:8006',
    endpoints: 4,
    latency_ms: 34,
    accent_color: '#9333EA',
    key_stat: '12,437 parcels',
  },
  {
    name: 'SPHERES Legal',
    slug: 'legal',
    description: 'Permitting pathways, policy tracking & compliance',
    status: 'online',
    url: 'http://localhost:8006',
    endpoints: 4,
    latency_ms: 38,
    accent_color: '#00CC66',
    key_stat: '47 permit pathways',
  },
  {
    name: 'SPHERES Studio',
    slug: 'studio',
    description: 'Community design tool & activation planner',
    status: 'online',
    url: 'http://localhost:8007',
    endpoints: 4,
    latency_ms: 11,
    accent_color: '#0066FF',
    key_stat: '234 community designs',
  },
  {
    name: 'SPHERES Viz',
    slug: 'viz',
    description: 'Cinematic storytelling & data visualization',
    status: 'online',
    url: 'http://localhost:8008',
    endpoints: 3,
    latency_ms: 46,
    accent_color: '#FF8C00',
    key_stat: '10 episodes',
  },
];

export default function ServiceGrid({ services, loading }: Props) {
  const [hoveredIdx, setHoveredIdx] = useState<number | null>(null);
  const data = services.length > 0 ? services : FALLBACK_SERVICES;

  if (loading) {
    return (
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 12 }}>
        {[0, 1, 2, 3].map((i) => (
          <div
            key={i}
            style={{
              background: 'var(--bg-card)',
              border: '1px solid var(--border)',
              borderRadius: 8,
              padding: 16,
              height: 120,
              animation: 'pulse 1.5s ease-in-out infinite',
            }}
          />
        ))}
      </div>
    );
  }

  return (
    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 12 }}>
      {data.map((svc, idx) => (
        <a
          key={svc.slug}
          href={svc.url}
          target="_blank"
          rel="noopener noreferrer"
          onMouseEnter={() => setHoveredIdx(idx)}
          onMouseLeave={() => setHoveredIdx(null)}
          style={{
            display: 'block',
            textDecoration: 'none',
            color: 'inherit',
            background: hoveredIdx === idx ? 'var(--bg-hover)' : 'var(--bg-card)',
            border: '1px solid',
            borderColor: hoveredIdx === idx ? 'var(--border-hover)' : 'var(--border)',
            borderLeft: `3px solid ${svc.accent_color}`,
            borderRadius: 8,
            padding: 16,
            transition: 'all 0.2s ease',
            cursor: 'pointer',
            position: 'relative',
          }}
        >
          {/* Header row */}
          <div
            style={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between',
              marginBottom: 8,
            }}
          >
            <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
              <span style={{ color: svc.accent_color, display: 'flex' }}>
                {APP_ICONS[svc.slug] || <Globe size={16} />}
              </span>
              <span
                style={{
                  fontSize: 13,
                  fontWeight: 600,
                  letterSpacing: '0.03em',
                  textTransform: 'uppercase',
                }}
              >
                {svc.name}
              </span>
            </div>
            <ExternalLink size={12} style={{ opacity: 0.3 }} />
          </div>

          {/* Description */}
          <p
            style={{
              fontSize: 11,
              color: 'var(--text-secondary)',
              lineHeight: 1.4,
              marginBottom: 12,
            }}
          >
            {svc.description}
          </p>

          {/* Key stat */}
          {svc.key_stat && (
            <div
              style={{
                fontFamily: 'var(--mono)',
                fontSize: 16,
                fontWeight: 700,
                color: 'var(--text)',
                marginBottom: 8,
                letterSpacing: '-0.02em',
              }}
            >
              {svc.key_stat}
            </div>
          )}

          {/* Status row */}
          <div
            style={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between',
              fontSize: 11,
            }}
          >
            <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
              <span
                style={{
                  width: 6,
                  height: 6,
                  borderRadius: '50%',
                  background: STATUS_COLORS[svc.status] || 'var(--text-tertiary)',
                  boxShadow: `0 0 6px ${STATUS_COLORS[svc.status] || 'transparent'}`,
                  display: 'inline-block',
                  animation: svc.status === 'online' ? 'pulse-dot 2s ease-in-out infinite' : 'none',
                }}
              />
              <span style={{ color: 'var(--text-secondary)', textTransform: 'capitalize' }}>
                {svc.status}
              </span>
            </div>
            <div style={{ display: 'flex', gap: 12, color: 'var(--text-tertiary)' }}>
              <span style={{ fontFamily: 'var(--mono)', fontSize: 10 }}>
                {svc.latency_ms}ms
              </span>
              <span style={{ fontFamily: 'var(--mono)', fontSize: 10 }}>
                {svc.endpoints} endpoints
              </span>
            </div>
          </div>
        </a>
      ))}
      <style>{`
        @keyframes pulse-dot {
          0%, 100% { opacity: 1; transform: scale(1); }
          50% { opacity: 0.4; transform: scale(0.8); }
        }
      `}</style>
    </div>
  );
}
