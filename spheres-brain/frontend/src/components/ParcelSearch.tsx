// ─────────────────────────────────────────────────────────────
// ParcelSearch — Unified parcel query with tabbed results
// ─────────────────────────────────────────────────────────────

import { useState, useCallback } from 'react';
import {
  Search,
  MapPin,
  FileText,
  Paintbrush,
  Tv,
  Clock,
  Star,
  CheckCircle,
  AlertTriangle,
  Loader2,
} from 'lucide-react';
import { queryParcel } from '../utils/api';
import type { QueryResult } from '../utils/api';

type Tab = 'parcel' | 'legal' | 'designs' | 'episode' | 'history';

const TABS: { key: Tab; label: string; icon: React.ReactNode }[] = [
  { key: 'parcel', label: 'Parcel Data', icon: <MapPin size={12} /> },
  { key: 'legal', label: 'Legal Pathway', icon: <FileText size={12} /> },
  { key: 'designs', label: 'Community Designs', icon: <Paintbrush size={12} /> },
  { key: 'episode', label: 'Episode', icon: <Tv size={12} /> },
  { key: 'history', label: 'History', icon: <Clock size={12} /> },
];

const VACANCY_COLORS: Record<string, string> = {
  vacant: 'var(--red)',
  occupied: 'var(--green)',
  unknown: 'var(--yellow)',
};

function StarRating({ rating }: { rating: number }) {
  return (
    <span style={{ display: 'inline-flex', gap: 2 }}>
      {[1, 2, 3, 4, 5].map((i) => (
        <Star
          key={i}
          size={10}
          fill={i <= Math.round(rating) ? 'var(--yellow)' : 'transparent'}
          stroke={i <= Math.round(rating) ? 'var(--yellow)' : 'var(--text-tertiary)'}
          strokeWidth={1.5}
        />
      ))}
    </span>
  );
}

export default function ParcelSearch() {
  const [query, setQuery] = useState('');
  const [result, setResult] = useState<QueryResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<Tab>('parcel');

  const handleSubmit = useCallback(
    async (e: React.FormEvent) => {
      e.preventDefault();
      if (!query.trim()) return;
      setLoading(true);
      setError(null);
      try {
        const res = await queryParcel(query.trim());
        setResult(res);
        setActiveTab('parcel');
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Search failed');
        setResult(null);
      } finally {
        setLoading(false);
      }
    },
    [query],
  );

  return (
    <div
      style={{
        background: 'var(--bg-card)',
        border: '1px solid var(--border)',
        borderRadius: 8,
        overflow: 'hidden',
      }}
    >
      {/* Search input */}
      <form onSubmit={handleSubmit} style={{ position: 'relative' }}>
        <div
          style={{
            display: 'flex',
            alignItems: 'center',
            borderBottom: '1px solid var(--border)',
          }}
        >
          <Search
            size={14}
            style={{
              position: 'absolute',
              left: 14,
              color: 'var(--text-tertiary)',
              pointerEvents: 'none',
            }}
          />
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search any Philadelphia address or parcel ID..."
            style={{
              flex: 1,
              background: 'transparent',
              border: 'none',
              outline: 'none',
              padding: '12px 12px 12px 38px',
              color: 'var(--text)',
              fontSize: 13,
              fontFamily: 'inherit',
            }}
          />
          <button
            type="submit"
            disabled={loading || !query.trim()}
            style={{
              background: loading ? 'var(--border)' : 'var(--accent)',
              color: '#fff',
              border: 'none',
              padding: '8px 16px',
              margin: 6,
              borderRadius: 4,
              fontSize: 11,
              fontWeight: 600,
              cursor: loading ? 'wait' : 'pointer',
              opacity: !query.trim() ? 0.4 : 1,
              display: 'flex',
              alignItems: 'center',
              gap: 6,
              letterSpacing: '0.03em',
            }}
          >
            {loading && <Loader2 size={12} style={{ animation: 'spin 1s linear infinite' }} />}
            QUERY
          </button>
        </div>
      </form>

      {/* Error */}
      {error && (
        <div
          style={{
            padding: '10px 14px',
            fontSize: 12,
            color: 'var(--red)',
            display: 'flex',
            alignItems: 'center',
            gap: 6,
          }}
        >
          <AlertTriangle size={12} />
          {error}
        </div>
      )}

      {/* Loading */}
      {loading && (
        <div
          style={{
            padding: '32px 14px',
            textAlign: 'center',
            color: 'var(--text-tertiary)',
            fontSize: 12,
          }}
        >
          <Loader2 size={18} style={{ animation: 'spin 1s linear infinite', margin: '0 auto 8px' }} />
          <div>Querying across all SPHERES services...</div>
        </div>
      )}

      {/* Results */}
      {result && !loading && (
        <>
          {/* Tab bar */}
          <div
            style={{
              display: 'flex',
              borderBottom: '1px solid var(--border)',
              overflowX: 'auto',
            }}
          >
            {TABS.map((tab) => (
              <button
                key={tab.key}
                onClick={() => setActiveTab(tab.key)}
                style={{
                  background: 'transparent',
                  border: 'none',
                  borderBottom: activeTab === tab.key ? '2px solid var(--accent)' : '2px solid transparent',
                  padding: '8px 14px',
                  color: activeTab === tab.key ? 'var(--text)' : 'var(--text-tertiary)',
                  fontSize: 11,
                  fontWeight: 500,
                  cursor: 'pointer',
                  display: 'flex',
                  alignItems: 'center',
                  gap: 5,
                  whiteSpace: 'nowrap',
                  transition: 'color 0.15s ease',
                  letterSpacing: '0.02em',
                }}
              >
                {tab.icon}
                {tab.label}
              </button>
            ))}
          </div>

          {/* Tab content */}
          <div style={{ padding: 14 }}>
            {activeTab === 'parcel' && <ParcelTab data={result} />}
            {activeTab === 'legal' && <LegalTab data={result} />}
            {activeTab === 'designs' && <DesignsTab data={result} />}
            {activeTab === 'episode' && <EpisodeTab data={result} />}
            {activeTab === 'history' && <HistoryTab data={result} />}
          </div>
        </>
      )}

      {/* Empty state */}
      {!result && !loading && !error && (
        <div
          style={{
            padding: '28px 14px',
            textAlign: 'center',
            color: 'var(--text-tertiary)',
            fontSize: 12,
          }}
        >
          <MapPin size={20} style={{ margin: '0 auto 8px', opacity: 0.4 }} />
          <div>Enter an address or parcel ID to query the entire SPHERES ecosystem</div>
        </div>
      )}

      {/* Spin animation style */}
      <style>{`@keyframes spin { to { transform: rotate(360deg) } }`}</style>
    </div>
  );
}

// ── Sub-panels ────────────────────────────────────────────────

function DataRow({ label, value, mono }: { label: string; value: React.ReactNode; mono?: boolean }) {
  return (
    <div
      style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        padding: '6px 0',
        borderBottom: '1px solid var(--border)',
        fontSize: 12,
      }}
    >
      <span style={{ color: 'var(--text-secondary)' }}>{label}</span>
      <span style={{ fontFamily: mono ? 'var(--mono)' : 'inherit', fontWeight: 500 }}>{value}</span>
    </div>
  );
}

function ParcelTab({ data }: { data: QueryResult }) {
  const p = data.parcel;
  return (
    <div>
      <div
        style={{
          fontSize: 14,
          fontWeight: 600,
          marginBottom: 10,
          display: 'flex',
          alignItems: 'center',
          gap: 6,
        }}
      >
        <MapPin size={14} style={{ color: 'var(--accent)' }} />
        {p.address}
      </div>
      <DataRow label="Parcel ID" value={p.parcel_id} mono />
      <DataRow label="Owner" value={p.owner} />
      <DataRow label="Zoning" value={p.zoning} mono />
      <DataRow label="Square Footage" value={p.sqft.toLocaleString() + ' sqft'} mono />
      <DataRow
        label="Assessed Value"
        value={'$' + p.assessed_value.toLocaleString()}
        mono
      />
      <DataRow
        label="Market Value"
        value={'$' + p.market_value.toLocaleString()}
        mono
      />
      <DataRow
        label="Vacancy Status"
        value={
          <span
            style={{
              display: 'inline-flex',
              alignItems: 'center',
              gap: 5,
              textTransform: 'capitalize',
            }}
          >
            <span
              style={{
                width: 6,
                height: 6,
                borderRadius: '50%',
                background: VACANCY_COLORS[p.vacancy_status] || 'var(--text-tertiary)',
              }}
            />
            {p.vacancy_status}
          </span>
        }
      />
    </div>
  );
}

function LegalTab({ data }: { data: QueryResult }) {
  const l = data.legal;
  return (
    <div>
      <div style={{ marginBottom: 10 }}>
        <DataRow
          label="Zoning Compliant"
          value={
            <span
              style={{
                display: 'inline-flex',
                alignItems: 'center',
                gap: 4,
                color: l.zoning_compliant ? 'var(--green)' : 'var(--red)',
              }}
            >
              {l.zoning_compliant ? <CheckCircle size={12} /> : <AlertTriangle size={12} />}
              {l.zoning_compliant ? 'Yes' : 'No'}
            </span>
          }
        />
        <DataRow label="Timeline" value={`${l.timeline_weeks} weeks`} mono />
        <DataRow label="Estimated Fees" value={`$${l.estimated_fees.toLocaleString()}`} mono />
      </div>

      {l.permits_needed.length > 0 && (
        <div style={{ marginBottom: 12 }}>
          <div
            style={{
              fontSize: 11,
              color: 'var(--text-tertiary)',
              textTransform: 'uppercase',
              letterSpacing: '0.06em',
              marginBottom: 6,
            }}
          >
            Permits Needed
          </div>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: 6 }}>
            {l.permits_needed.map((p) => (
              <span
                key={p}
                style={{
                  background: 'var(--accent-dim)',
                  color: 'var(--accent)',
                  padding: '3px 8px',
                  borderRadius: 4,
                  fontSize: 11,
                  fontWeight: 500,
                }}
              >
                {p}
              </span>
            ))}
          </div>
        </div>
      )}

      {l.next_steps.length > 0 && (
        <div>
          <div
            style={{
              fontSize: 11,
              color: 'var(--text-tertiary)',
              textTransform: 'uppercase',
              letterSpacing: '0.06em',
              marginBottom: 6,
            }}
          >
            Next Steps
          </div>
          {l.next_steps.map((step, i) => (
            <div
              key={i}
              style={{
                display: 'flex',
                gap: 8,
                alignItems: 'flex-start',
                padding: '5px 0',
                fontSize: 12,
                color: 'var(--text-secondary)',
              }}
            >
              <span
                style={{
                  fontFamily: 'var(--mono)',
                  fontSize: 10,
                  color: 'var(--text-tertiary)',
                  marginTop: 1,
                }}
              >
                {String(i + 1).padStart(2, '0')}
              </span>
              {step}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

function DesignsTab({ data }: { data: QueryResult }) {
  if (data.designs.length === 0) {
    return (
      <div style={{ padding: 20, textAlign: 'center', color: 'var(--text-tertiary)', fontSize: 12 }}>
        No community designs found for this parcel.
      </div>
    );
  }

  return (
    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: 10 }}>
      {data.designs.map((d) => (
        <div
          key={d.id}
          style={{
            background: 'var(--bg)',
            border: '1px solid var(--border)',
            borderRadius: 6,
            padding: 12,
          }}
        >
          <div style={{ fontSize: 13, fontWeight: 600, marginBottom: 4 }}>{d.name}</div>
          <div style={{ fontSize: 11, color: 'var(--text-secondary)', marginBottom: 6 }}>
            by {d.creator}
          </div>
          <div
            style={{
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center',
              fontSize: 11,
            }}
          >
            <span
              style={{
                fontFamily: 'var(--mono)',
                color: 'var(--accent)',
                fontSize: 12,
                fontWeight: 600,
              }}
            >
              ${d.cost_estimate.toLocaleString()}
            </span>
            <StarRating rating={d.rating} />
          </div>
          <div
            style={{
              marginTop: 6,
              fontSize: 10,
              color: 'var(--text-tertiary)',
              textTransform: 'uppercase',
              letterSpacing: '0.04em',
            }}
          >
            {d.type}
          </div>
        </div>
      ))}
    </div>
  );
}

function EpisodeTab({ data }: { data: QueryResult }) {
  if (!data.episode) {
    return (
      <div style={{ padding: 20, textAlign: 'center', color: 'var(--text-tertiary)', fontSize: 12 }}>
        No related SPHERES Viz episode found.
      </div>
    );
  }

  const ep = data.episode;
  return (
    <div
      style={{
        background: 'var(--bg)',
        border: '1px solid var(--border)',
        borderRadius: 6,
        padding: 16,
      }}
    >
      <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 8 }}>
        <span
          style={{
            fontFamily: 'var(--mono)',
            fontSize: 20,
            fontWeight: 700,
            color: 'var(--accent)',
          }}
        >
          {String(ep.episode_number).padStart(2, '0')}
        </span>
        <div>
          <div style={{ fontSize: 14, fontWeight: 600 }}>{ep.episode_title}</div>
          <div style={{ fontSize: 11, color: 'var(--text-tertiary)' }}>SPHERES Viz Episode</div>
        </div>
      </div>
      <div style={{ fontSize: 12, color: 'var(--text-secondary)', lineHeight: 1.5 }}>
        {ep.relevance}
      </div>
    </div>
  );
}

function HistoryTab({ data }: { data: QueryResult }) {
  if (data.history.length === 0) {
    return (
      <div style={{ padding: 20, textAlign: 'center', color: 'var(--text-tertiary)', fontSize: 12 }}>
        No history records found.
      </div>
    );
  }

  return (
    <div>
      {data.history.map((h, i) => (
        <div
          key={i}
          style={{
            display: 'flex',
            gap: 10,
            padding: '8px 0',
            borderBottom: i < data.history.length - 1 ? '1px solid var(--border)' : 'none',
            fontSize: 12,
          }}
        >
          <span
            style={{
              fontFamily: 'var(--mono)',
              fontSize: 10,
              color: 'var(--text-tertiary)',
              whiteSpace: 'nowrap',
              minWidth: 72,
            }}
          >
            {h.date}
          </span>
          <span style={{ color: 'var(--text-secondary)', flex: 1 }}>{h.event}</span>
          <span
            style={{
              fontSize: 10,
              color: 'var(--text-tertiary)',
              whiteSpace: 'nowrap',
            }}
          >
            {h.source}
          </span>
        </div>
      ))}
    </div>
  );
}
