// -----------------------------------------------------------------
// DiscoveryFeed -- Automated discoveries grouped by type
// -----------------------------------------------------------------

import { useState } from 'react';
import {
  Compass,
  MapPin,
  ScrollText,
  BarChart3,
  Film,
  ChevronRight,
} from 'lucide-react';
import type { Discovery } from '../utils/api';

interface Props {
  discoveries: Discovery[];
  loading: boolean;
}

type DiscoveryType = Discovery['type'];

const TYPE_META: Record<
  DiscoveryType,
  { label: string; icon: React.ReactNode; color: string }
> = {
  parcel: {
    label: 'Parcels',
    icon: <MapPin size={12} />,
    color: '#9333EA',
  },
  policy: {
    label: 'Policy',
    icon: <ScrollText size={12} />,
    color: 'var(--green)',
  },
  comparable: {
    label: 'Comparable',
    icon: <BarChart3 size={12} />,
    color: 'var(--accent)',
  },
  media: {
    label: 'Media',
    icon: <Film size={12} />,
    color: '#FF8C00',
  },
};

const PLACEHOLDER_DISCOVERIES: Discovery[] = [
  {
    id: 'd1',
    type: 'parcel',
    title: 'New vacancy cluster detected on N 15th St',
    description: '3 adjacent parcels flagged as newly vacant within 200ft radius. High activation potential.',
    source: 'SPHERES Assets',
    timestamp: '2026-02-14T09:32:00Z',
    relevance_score: 92,
  },
  {
    id: 'd2',
    type: 'policy',
    title: 'Philly Land Bank expedited transfer program updated',
    description: 'New fast-track process for community-owned vacant lot transfers. 60-day timeline.',
    source: 'City of Philadelphia',
    timestamp: '2026-02-14T08:15:00Z',
    relevance_score: 88,
  },
  {
    id: 'd3',
    type: 'comparable',
    title: 'Detroit Land Bank Authority model shows 40% cost reduction',
    description: 'Detroit program reduced activation costs by standardizing community garden kits.',
    source: 'Comparative Analysis',
    timestamp: '2026-02-13T22:40:00Z',
    relevance_score: 78,
  },
  {
    id: 'd4',
    type: 'media',
    title: 'WHYY feature on vacant lot transformations in Kensington',
    description: 'Local media coverage of community-led vacant lot activation aligned with SPHERES.',
    source: 'WHYY News',
    timestamp: '2026-02-13T16:20:00Z',
    relevance_score: 72,
  },
  {
    id: 'd5',
    type: 'parcel',
    title: 'Zoning variance approved for 2301 W Girard Ave',
    description: 'Variance allows mixed-use activation on previously restricted lot.',
    source: 'SPHERES Legal',
    timestamp: '2026-02-13T14:05:00Z',
    relevance_score: 85,
  },
  {
    id: 'd6',
    type: 'policy',
    title: 'City Council Bill 240315 - Community Garden Tax Incentive',
    description: 'Proposed tax credit for property owners who allow community garden use on vacant lots.',
    source: 'Philadelphia City Council',
    timestamp: '2026-02-12T10:00:00Z',
    relevance_score: 95,
  },
];

function timeAgo(timestamp: string): string {
  const diff = Date.now() - new Date(timestamp).getTime();
  const mins = Math.floor(diff / 60000);
  if (mins < 60) return `${mins}m ago`;
  const hrs = Math.floor(mins / 60);
  if (hrs < 24) return `${hrs}h ago`;
  const days = Math.floor(hrs / 24);
  return `${days}d ago`;
}

export default function DiscoveryFeed({ discoveries, loading }: Props) {
  const [activeFilter, setActiveFilter] = useState<DiscoveryType | 'all'>('all');
  const data = discoveries.length > 0 ? discoveries : PLACEHOLDER_DISCOVERIES;

  const filtered =
    activeFilter === 'all'
      ? data
      : data.filter((d) => d.type === activeFilter);

  // Group by type for the filter counts
  const counts: Record<string, number> = { all: data.length };
  for (const d of data) {
    counts[d.type] = (counts[d.type] || 0) + 1;
  }

  return (
    <div
      style={{
        background: 'var(--bg-card)',
        border: '1px solid var(--border)',
        borderRadius: 8,
        overflow: 'hidden',
        display: 'flex',
        flexDirection: 'column',
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
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
          <Compass size={12} style={{ color: 'var(--accent)' }} />
          <span
            style={{
              fontSize: 11,
              fontWeight: 600,
              textTransform: 'uppercase',
              letterSpacing: '0.06em',
              color: 'var(--text-secondary)',
            }}
          >
            Discovery Feed
          </span>
        </div>
        <span
          style={{
            fontFamily: 'var(--mono)',
            fontSize: 10,
            color: 'var(--text-tertiary)',
          }}
        >
          {data.length} items
        </span>
      </div>

      {/* Filters */}
      <div
        style={{
          display: 'flex',
          gap: 4,
          padding: '8px 14px',
          borderBottom: '1px solid var(--border)',
          overflowX: 'auto',
        }}
      >
        <FilterPill
          label="All"
          count={counts.all}
          active={activeFilter === 'all'}
          onClick={() => setActiveFilter('all')}
        />
        {(Object.keys(TYPE_META) as DiscoveryType[]).map((type) => (
          <FilterPill
            key={type}
            label={TYPE_META[type].label}
            count={counts[type] || 0}
            active={activeFilter === type}
            color={TYPE_META[type].color}
            onClick={() => setActiveFilter(type)}
          />
        ))}
      </div>

      {/* Items */}
      <div
        style={{
          flex: 1,
          overflowY: 'auto',
          opacity: loading ? 0.4 : 1,
          transition: 'opacity 0.3s ease',
        }}
      >
        {filtered.length === 0 && (
          <div
            style={{
              padding: '28px 14px',
              textAlign: 'center',
              color: 'var(--text-tertiary)',
              fontSize: 12,
            }}
          >
            No discoveries for this category.
          </div>
        )}
        {filtered.map((item, idx) => {
          const meta = TYPE_META[item.type];
          return (
            <div
              key={item.id}
              style={{
                padding: '10px 14px',
                borderBottom:
                  idx < filtered.length - 1
                    ? '1px solid var(--border)'
                    : 'none',
                display: 'flex',
                gap: 10,
                alignItems: 'flex-start',
                cursor: 'pointer',
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
              {/* Type badge */}
              <div
                style={{
                  marginTop: 2,
                  width: 24,
                  height: 24,
                  borderRadius: 6,
                  background: `${meta.color}15`,
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  color: meta.color,
                  flexShrink: 0,
                }}
              >
                {meta.icon}
              </div>

              {/* Content */}
              <div style={{ flex: 1, minWidth: 0 }}>
                <div
                  style={{
                    fontSize: 12,
                    fontWeight: 600,
                    lineHeight: 1.3,
                    marginBottom: 3,
                  }}
                >
                  {item.title}
                </div>
                <div
                  style={{
                    fontSize: 11,
                    color: 'var(--text-secondary)',
                    lineHeight: 1.4,
                    marginBottom: 4,
                  }}
                >
                  {item.description}
                </div>
                <div
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: 8,
                    fontSize: 10,
                    color: 'var(--text-tertiary)',
                  }}
                >
                  <span>{item.source}</span>
                  <span style={{ opacity: 0.3 }}>|</span>
                  <span style={{ fontFamily: 'var(--mono)' }}>
                    {timeAgo(item.timestamp)}
                  </span>
                </div>
              </div>

              {/* Relevance score */}
              <div
                style={{
                  display: 'flex',
                  flexDirection: 'column',
                  alignItems: 'center',
                  gap: 2,
                  flexShrink: 0,
                }}
              >
                <span
                  style={{
                    fontFamily: 'var(--mono)',
                    fontSize: 14,
                    fontWeight: 700,
                    color:
                      item.relevance_score >= 85
                        ? 'var(--green)'
                        : item.relevance_score >= 70
                          ? 'var(--accent)'
                          : 'var(--text-secondary)',
                  }}
                >
                  {item.relevance_score}
                </span>
                <span
                  style={{
                    fontSize: 8,
                    color: 'var(--text-tertiary)',
                    textTransform: 'uppercase',
                    letterSpacing: '0.06em',
                  }}
                >
                  REL
                </span>
              </div>

              <ChevronRight
                size={12}
                style={{
                  color: 'var(--text-tertiary)',
                  flexShrink: 0,
                  marginTop: 4,
                  opacity: 0.5,
                }}
              />
            </div>
          );
        })}
      </div>
    </div>
  );
}

// -- Filter pill sub-component -----------------------------------------------

function FilterPill({
  label,
  count,
  active,
  color,
  onClick,
}: {
  label: string;
  count: number;
  active: boolean;
  color?: string;
  onClick: () => void;
}) {
  return (
    <button
      onClick={onClick}
      style={{
        background: active
          ? color
            ? `${color}20`
            : 'var(--accent-dim)'
          : 'transparent',
        border: '1px solid',
        borderColor: active
          ? color || 'var(--accent)'
          : 'var(--border)',
        borderRadius: 4,
        padding: '3px 8px',
        fontSize: 10,
        fontWeight: 500,
        color: active
          ? color || 'var(--accent)'
          : 'var(--text-tertiary)',
        cursor: 'pointer',
        display: 'flex',
        alignItems: 'center',
        gap: 4,
        whiteSpace: 'nowrap',
        transition: 'all 0.15s ease',
      }}
    >
      {label}
      <span
        style={{
          fontFamily: 'var(--mono)',
          fontSize: 9,
          opacity: 0.7,
        }}
      >
        {count}
      </span>
    </button>
  );
}
