// ─────────────────────────────────────────────────────────────
// MetricsBar — Key ecosystem metrics strip
// ─────────────────────────────────────────────────────────────

import { Palette, FileCheck, Rocket, TrendingUp, DollarSign, MapPin, Users } from 'lucide-react';
import type { MetricsData } from '../utils/api';

interface Props {
  metrics: MetricsData | null;
  loading: boolean;
}

function fmt(n: number): string {
  if (n >= 1_000_000) return `$${(n / 1_000_000).toFixed(1)}M`;
  if (n >= 1_000) return n >= 10_000 ? `${(n / 1_000).toFixed(0)}K` : n.toLocaleString();
  return n.toString();
}

function fmtDollar(n: number): string {
  if (n >= 1_000_000) return `$${(n / 1_000_000).toFixed(1)}M`;
  if (n >= 1_000) return `$${(n / 1_000).toFixed(0)}K`;
  return `$${n}`;
}

const METRIC_DEFS = [
  { key: 'total_designs' as const, label: 'Designs Created', icon: Palette, format: fmt },
  { key: 'permits_pulled' as const, label: 'Permits Pulled', icon: FileCheck, format: fmt },
  { key: 'activations_completed' as const, label: 'Activations', icon: Rocket, format: fmt },
  { key: 'permanent_value' as const, label: 'Permanent Value', icon: TrendingUp, format: fmtDollar },
  { key: 'revenue_generated' as const, label: 'Revenue', icon: DollarSign, format: fmtDollar },
  { key: 'active_parcels' as const, label: 'Active Parcels', icon: MapPin, format: fmt },
  { key: 'community_participants' as const, label: 'Participants', icon: Users, format: fmt },
];

const PLACEHOLDER: MetricsData = {
  total_designs: 234,
  permits_pulled: 47,
  activations_completed: 13,
  permanent_value: 340000,
  revenue_generated: 890000,
  active_parcels: 28,
  community_participants: 1847,
};

export default function MetricsBar({ metrics, loading }: Props) {
  const data = metrics || PLACEHOLDER;

  return (
    <div
      style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(7, 1fr)',
        gap: 1,
        background: 'var(--border)',
        borderRadius: 8,
        overflow: 'hidden',
      }}
    >
      {METRIC_DEFS.map((def) => {
        const Icon = def.icon;
        return (
          <div
            key={def.key}
            style={{
              background: 'var(--bg-card)',
              padding: '14px 16px',
              display: 'flex',
              flexDirection: 'column',
              gap: 4,
              opacity: loading ? 0.4 : 1,
              transition: 'opacity 0.3s ease',
            }}
          >
            <div style={{ display: 'flex', alignItems: 'center', gap: 6, marginBottom: 2 }}>
              <Icon size={12} style={{ color: 'var(--accent)', opacity: 0.7 }} />
              <span
                style={{
                  fontSize: 10,
                  color: 'var(--text-tertiary)',
                  textTransform: 'uppercase',
                  letterSpacing: '0.06em',
                  fontWeight: 500,
                }}
              >
                {def.label}
              </span>
            </div>
            <span
              style={{
                fontFamily: 'var(--mono)',
                fontSize: 22,
                fontWeight: 700,
                color: 'var(--text)',
                letterSpacing: '-0.02em',
                lineHeight: 1,
              }}
            >
              {loading ? '--' : def.format(data[def.key])}
            </span>
          </div>
        );
      })}
    </div>
  );
}
