// ─────────────────────────────────────────────────────────────────────────────
// DOMES Brain — Discovery Feed: Discovery stream & priority queue
// ─────────────────────────────────────────────────────────────────────────────

import { useState, useEffect, useCallback } from 'react';
import {
  type Discovery,
  type DiscoveryFilters,
  type DiscoveryImpact,
  type DiscoverySourceType,
  type DiscoveryStatus,
  type DiscoveryStats,
  getDiscoveries,
  getDiscoveryQueue,
  getDiscoveryStats,
  triggerScan,
  formatTimestamp,
} from '../api/client.ts';

// ── Constants ────────────────────────────────────────────────────────────────

const SOURCE_COLORS: Record<DiscoverySourceType, string> = {
  legislation: '#8B1A1A',
  regulation: '#6B5A1A',
  policy: '#1A3D8B',
  data: '#5A1A6B',
  news: '#1A6B6B',
  research: '#1A6B3C',
};

const IMPACT_CONFIG: Record<DiscoveryImpact, { color: string; bg: string; label: string }> = {
  critical: { color: 'text-red', bg: 'bg-red-dim', label: 'CRITICAL' },
  high: { color: 'text-amber', bg: 'bg-amber-dim', label: 'HIGH' },
  medium: { color: 'text-blue', bg: 'bg-blue-dim', label: 'MEDIUM' },
  low: { color: 'text-text-muted', bg: 'bg-surface-alt', label: 'LOW' },
};

const SOURCE_TYPES: DiscoverySourceType[] = ['legislation', 'regulation', 'policy', 'data', 'news', 'research'];
const IMPACT_LEVELS: DiscoveryImpact[] = ['critical', 'high', 'medium', 'low'];
const STATUS_OPTIONS: DiscoveryStatus[] = ['new', 'reviewed', 'queued', 'dismissed'];

// ── Filter Select ────────────────────────────────────────────────────────────

function FilterSelect<T extends string>({
  label,
  value,
  options,
  onChange,
}: {
  label: string;
  value: T | undefined;
  options: T[];
  onChange: (v: T | undefined) => void;
}) {
  return (
    <select
      value={value ?? ''}
      onChange={(e) => onChange((e.target.value || undefined) as T | undefined)}
      className="bg-surface-alt border border-border px-2 py-1 text-xs font-mono text-text focus:outline-none focus:border-blue appearance-none cursor-pointer"
      title={label}
    >
      <option value="">{label}: All</option>
      {options.map((o) => (
        <option key={o} value={o}>
          {o}
        </option>
      ))}
    </select>
  );
}

// ── Discovery Card ───────────────────────────────────────────────────────────

function DiscoveryCard({
  item,
  onAction,
}: {
  item: Discovery;
  onAction: (id: string, action: 'review' | 'queue' | 'dismiss') => void;
}) {
  const sourceColor = SOURCE_COLORS[item.sourceType];
  const impact = IMPACT_CONFIG[item.impact];

  return (
    <div className="bg-surface border border-border p-3">
      {/* Header */}
      <div className="flex items-start justify-between gap-2 mb-1">
        <div className="flex items-center gap-2 min-w-0">
          <span
            className="text-xs font-mono px-1.5 py-0.5 border shrink-0"
            style={{ color: sourceColor, borderColor: sourceColor }}
          >
            {item.sourceType}
          </span>
          <span className={`text-xs font-mono px-1.5 py-0.5 ${impact.bg} ${impact.color} shrink-0`}>
            {impact.label}
          </span>
        </div>
        <span className="text-xs font-mono text-text-muted shrink-0">
          {formatTimestamp(item.timestamp)}
        </span>
      </div>

      {/* Title + Summary */}
      <h4 className="text-sm font-semibold text-text mb-1 leading-tight">{item.title}</h4>
      <p className="text-xs text-text-muted leading-relaxed mb-2 line-clamp-2">
        {item.summary}
      </p>

      {/* Relevance Bar + Source + Actions */}
      <div className="flex items-center justify-between gap-3">
        <div className="flex items-center gap-2 flex-1 min-w-0">
          <div className="flex-1 h-1 bg-surface-alt max-w-32">
            <div
              className="h-full"
              style={{
                width: `${item.relevanceScore * 100}%`,
                backgroundColor: sourceColor,
              }}
            />
          </div>
          <span className="text-xs font-mono text-text-muted">
            {(item.relevanceScore * 100).toFixed(0)}%
          </span>
          <span className="text-xs text-text-muted truncate">
            {item.source}
          </span>
        </div>

        <div className="flex gap-1 shrink-0">
          {item.status !== 'reviewed' && (
            <button
              onClick={() => onAction(item.id, 'review')}
              className="text-xs font-mono text-green hover:text-text border border-border px-1.5 py-0.5"
            >
              Review
            </button>
          )}
          {item.status !== 'queued' && (
            <button
              onClick={() => onAction(item.id, 'queue')}
              className="text-xs font-mono text-blue hover:text-text border border-border px-1.5 py-0.5"
            >
              Queue
            </button>
          )}
          {item.status !== 'dismissed' && (
            <button
              onClick={() => onAction(item.id, 'dismiss')}
              className="text-xs font-mono text-text-muted hover:text-red border border-border px-1.5 py-0.5"
            >
              Dismiss
            </button>
          )}
        </div>
      </div>
    </div>
  );
}

// ── Discovery Feed ───────────────────────────────────────────────────────────

type FeedTab = 'feed' | 'queue';

export default function DiscoveryFeed() {
  const [tab, setTab] = useState<FeedTab>('feed');
  const [items, setItems] = useState<Discovery[]>([]);
  const [queue, setQueue] = useState<Discovery[]>([]);
  const [stats, setStats] = useState<DiscoveryStats | null>(null);
  const [filters, setFilters] = useState<DiscoveryFilters>({});
  const [loading, setLoading] = useState(true);
  const [scanning, setScanning] = useState(false);
  const [scanMessage, setScanMessage] = useState('');

  const load = useCallback(async () => {
    const [d, q, s] = await Promise.all([
      getDiscoveries(filters),
      getDiscoveryQueue(),
      getDiscoveryStats(),
    ]);
    setItems(d);
    setQueue(q);
    setStats(s);
    setLoading(false);
  }, [filters]);

  useEffect(() => {
    load();
  }, [load]);

  const handleScan = async () => {
    setScanning(true);
    setScanMessage('');
    const res = await triggerScan();
    setScanMessage(res.message);
    setScanning(false);
    // Reload after brief delay
    setTimeout(load, 2000);
  };

  const handleAction = (id: string, action: 'review' | 'queue' | 'dismiss') => {
    const statusMap: Record<string, DiscoveryStatus> = {
      review: 'reviewed',
      queue: 'queued',
      dismiss: 'dismissed',
    };
    setItems((prev) =>
      prev.map((d) => (d.id === id ? { ...d, status: statusMap[action] } : d)),
    );
    setQueue((prev) =>
      prev.map((d) => (d.id === id ? { ...d, status: statusMap[action] } : d)),
    );
  };

  const currentItems = tab === 'feed' ? items : queue;

  return (
    <div className="p-6 space-y-4">
      {/* Stats Bar */}
      {stats && (
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
          <div className="bg-surface border border-border p-3">
            <div className="text-xs text-text-muted uppercase tracking-wider">Total</div>
            <div className="text-lg font-mono font-semibold text-text">{stats.totalDiscoveries}</div>
          </div>
          <div className="bg-surface border border-border p-3">
            <div className="text-xs text-text-muted uppercase tracking-wider">Pending</div>
            <div className="text-lg font-mono font-semibold text-amber">{stats.pendingReview}</div>
          </div>
          <div className="bg-surface border border-border p-3">
            <div className="text-xs text-text-muted uppercase tracking-wider">Critical</div>
            <div className="text-lg font-mono font-semibold text-red">{stats.criticalItems}</div>
          </div>
          <div className="bg-surface border border-border p-3">
            <div className="text-xs text-text-muted uppercase tracking-wider">Last Scan</div>
            <div className="text-sm font-mono text-text mt-0.5">{formatTimestamp(stats.lastScanTime)}</div>
          </div>
        </div>
      )}

      {/* Filter Bar + Scan Button */}
      <div className="bg-surface border border-border p-3 flex items-center justify-between flex-wrap gap-2">
        <div className="flex items-center gap-2 flex-wrap">
          {/* Tabs */}
          <button
            onClick={() => setTab('feed')}
            className={`text-xs font-mono px-2 py-1 border ${
              tab === 'feed' ? 'border-blue text-blue' : 'border-border text-text-muted hover:text-text'
            }`}
          >
            Feed ({items.length})
          </button>
          <button
            onClick={() => setTab('queue')}
            className={`text-xs font-mono px-2 py-1 border ${
              tab === 'queue' ? 'border-amber text-amber' : 'border-border text-text-muted hover:text-text'
            }`}
          >
            Priority Queue ({queue.length})
          </button>

          <span className="text-border mx-1">|</span>

          <FilterSelect<DiscoverySourceType>
            label="Source"
            value={filters.sourceType}
            options={SOURCE_TYPES}
            onChange={(v) => setFilters((f) => ({ ...f, sourceType: v }))}
          />
          <FilterSelect<DiscoveryImpact>
            label="Impact"
            value={filters.impact}
            options={IMPACT_LEVELS}
            onChange={(v) => setFilters((f) => ({ ...f, impact: v }))}
          />
          <FilterSelect<DiscoveryStatus>
            label="Status"
            value={filters.status}
            options={STATUS_OPTIONS}
            onChange={(v) => setFilters((f) => ({ ...f, status: v }))}
          />
        </div>

        <button
          onClick={handleScan}
          disabled={scanning}
          className="bg-green text-bg px-3 py-1 font-mono text-xs font-semibold hover:opacity-90 disabled:opacity-40"
        >
          {scanning ? 'Scanning...' : 'Scan Now'}
        </button>
      </div>

      {/* Scan Message */}
      {scanMessage && (
        <div className="bg-green-dim border border-green text-green text-xs font-mono p-2">
          {scanMessage}
        </div>
      )}

      {/* Items */}
      {loading ? (
        <div className="space-y-2">
          {Array.from({ length: 4 }).map((_, i) => (
            <div key={i} className="bg-surface border border-border p-3 h-24 animate-pulse" />
          ))}
        </div>
      ) : currentItems.length === 0 ? (
        <div className="bg-surface border border-border p-8 text-center">
          <p className="text-text-muted text-sm font-mono">No discoveries match the current filters</p>
        </div>
      ) : (
        <div className="space-y-2">
          {currentItems.map((item) => (
            <DiscoveryCard key={item.id} item={item} onAction={handleAction} />
          ))}
        </div>
      )}
    </div>
  );
}
