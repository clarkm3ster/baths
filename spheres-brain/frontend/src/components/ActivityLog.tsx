// -----------------------------------------------------------------
// ActivityLog -- Scrollable real-time activity feed
// -----------------------------------------------------------------

import { Activity, Globe, Zap, Radio, Wifi } from 'lucide-react';
import type { ActivityItem } from '../utils/api';

interface Props {
  activities: ActivityItem[];
  loading: boolean;
}

const SOURCE_META: Record<
  ActivityItem['source'],
  { icon: React.ReactNode; color: string; label: string }
> = {
  assets: { icon: <Globe size={10} />, color: '#9333EA', label: 'Assets' },
  legal: { icon: <Zap size={10} />, color: 'var(--green)', label: 'Legal' },
  studio: { icon: <Radio size={10} />, color: 'var(--accent)', label: 'Studio' },
  viz: { icon: <Wifi size={10} />, color: '#FF8C00', label: 'Viz' },
};

const PLACEHOLDER_ACTIVITIES: ActivityItem[] = [
  {
    id: 'a1',
    timestamp: '2026-02-14T10:22:14Z',
    source: 'assets',
    event: 'Parcel scan completed',
    detail: 'Scanned 1,247 parcels across North Philadelphia. 34 new vacancies flagged.',
  },
  {
    id: 'a2',
    timestamp: '2026-02-14T10:18:03Z',
    source: 'legal',
    event: 'Permit approved',
    detail: 'Temporary use permit approved for 1247 N Broad St — community garden.',
  },
  {
    id: 'a3',
    timestamp: '2026-02-14T10:12:45Z',
    source: 'studio',
    event: 'New design submitted',
    detail: 'User "PhillyGrows" submitted pocket park design for 3401 W Allegheny Ave.',
  },
  {
    id: 'a4',
    timestamp: '2026-02-14T09:58:30Z',
    source: 'viz',
    event: 'Episode published',
    detail: 'Episode 12: "The Corridor" — Germantown Ave vacant lot corridor analysis.',
  },
  {
    id: 'a5',
    timestamp: '2026-02-14T09:45:12Z',
    source: 'assets',
    event: 'Market update',
    detail: 'Assessed values updated for 892 parcels in West Philadelphia.',
  },
  {
    id: 'a6',
    timestamp: '2026-02-14T09:30:00Z',
    source: 'legal',
    event: 'Policy alert',
    detail: 'New zoning overlay proposed for Kensington corridor — public comment period open.',
  },
  {
    id: 'a7',
    timestamp: '2026-02-14T09:15:22Z',
    source: 'studio',
    event: 'Design rated',
    detail: 'Community rated "Sunflower Lot" design 4.8/5 for 601 S 52nd St.',
  },
  {
    id: 'a8',
    timestamp: '2026-02-14T08:55:10Z',
    source: 'assets',
    event: 'Ownership change detected',
    detail: 'Property at 2015 E Lehigh Ave transferred to Philadelphia Land Bank.',
  },
];

function formatTime(timestamp: string): string {
  const d = new Date(timestamp);
  return d.toLocaleTimeString('en-US', {
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    hour12: false,
  });
}

export default function ActivityLog({ activities, loading }: Props) {
  const data = activities.length > 0 ? activities : PLACEHOLDER_ACTIVITIES;

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
          <Activity size={12} style={{ color: 'var(--accent)' }} />
          <span
            style={{
              fontSize: 11,
              fontWeight: 600,
              textTransform: 'uppercase',
              letterSpacing: '0.06em',
              color: 'var(--text-secondary)',
            }}
          >
            Activity Log
          </span>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: 4 }}>
          <span
            style={{
              width: 6,
              height: 6,
              borderRadius: '50%',
              background: 'var(--green)',
              display: 'inline-block',
              animation: 'pulse-dot 2s ease-in-out infinite',
            }}
          />
          <span
            style={{
              fontFamily: 'var(--mono)',
              fontSize: 10,
              color: 'var(--text-tertiary)',
            }}
          >
            LIVE
          </span>
        </div>
      </div>

      {/* Scrollable list */}
      <div
        style={{
          flex: 1,
          overflowY: 'auto',
          opacity: loading ? 0.4 : 1,
          transition: 'opacity 0.3s ease',
        }}
      >
        {data.map((item, idx) => {
          const meta = SOURCE_META[item.source];
          return (
            <div
              key={item.id}
              style={{
                display: 'flex',
                gap: 10,
                padding: '9px 14px',
                borderBottom:
                  idx < data.length - 1
                    ? '1px solid var(--border)'
                    : 'none',
                alignItems: 'flex-start',
                transition: 'background 0.15s ease',
              }}
              onMouseEnter={(e) => {
                (e.currentTarget as HTMLElement).style.background =
                  'var(--bg-hover)';
              }}
              onMouseLeave={(e) => {
                (e.currentTarget as HTMLElement).style.background =
                  'transparent';
              }}
            >
              {/* Timeline column */}
              <div
                style={{
                  display: 'flex',
                  flexDirection: 'column',
                  alignItems: 'center',
                  gap: 4,
                  flexShrink: 0,
                  paddingTop: 1,
                }}
              >
                <div
                  style={{
                    width: 20,
                    height: 20,
                    borderRadius: 4,
                    background: `${meta.color}15`,
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    color: meta.color,
                  }}
                >
                  {meta.icon}
                </div>
              </div>

              {/* Content */}
              <div style={{ flex: 1, minWidth: 0 }}>
                <div
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: 6,
                    marginBottom: 2,
                  }}
                >
                  <span
                    style={{
                      fontSize: 11,
                      fontWeight: 600,
                      color: 'var(--text)',
                    }}
                  >
                    {item.event}
                  </span>
                  <span
                    style={{
                      fontSize: 9,
                      color: meta.color,
                      background: `${meta.color}15`,
                      padding: '1px 5px',
                      borderRadius: 3,
                      fontWeight: 500,
                      textTransform: 'uppercase',
                      letterSpacing: '0.04em',
                    }}
                  >
                    {meta.label}
                  </span>
                </div>
                <div
                  style={{
                    fontSize: 11,
                    color: 'var(--text-secondary)',
                    lineHeight: 1.4,
                  }}
                >
                  {item.detail}
                </div>
              </div>

              {/* Timestamp */}
              <span
                style={{
                  fontFamily: 'var(--mono)',
                  fontSize: 9,
                  color: 'var(--text-tertiary)',
                  whiteSpace: 'nowrap',
                  flexShrink: 0,
                  paddingTop: 2,
                }}
              >
                {formatTime(item.timestamp)}
              </span>
            </div>
          );
        })}
      </div>

      {/* Pulse animation */}
      <style>{`
        @keyframes pulse-dot {
          0%, 100% { opacity: 1; }
          50% { opacity: 0.3; }
        }
      `}</style>
    </div>
  );
}
