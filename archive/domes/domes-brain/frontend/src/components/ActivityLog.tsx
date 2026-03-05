// ─────────────────────────────────────────────────────────────────────────────
// DOMES Brain — Activity Log: System activity feed
// ─────────────────────────────────────────────────────────────────────────────

import { useState, useEffect, useCallback, useMemo } from 'react';
import {
  type ActivityEntry,
  type ActivityEventType,
  getActivity,
  getServiceColor,
  formatTime,
  getDateGroup,
} from '../api/client.ts';

// ── Constants ────────────────────────────────────────────────────────────────

const EVENT_CONFIG: Record<ActivityEventType, { color: string; bg: string; label: string }> = {
  scan: { color: 'text-blue', bg: 'bg-blue-dim', label: 'SCAN' },
  error: { color: 'text-red', bg: 'bg-red-dim', label: 'ERROR' },
  update: { color: 'text-green', bg: 'bg-green-dim', label: 'UPDATE' },
  query: { color: 'text-text-muted', bg: 'bg-surface-alt', label: 'QUERY' },
};

const EVENT_TYPES: ActivityEventType[] = ['scan', 'error', 'update', 'query'];

const SERVICE_SLUGS = [
  'domes-brain',
  'spheres-assets',
  'domes-data',
  'domes-profile',
  'domes-contracts',
  'domes-architect',
  'domes-viz',
];

// ── Filter Pill ──────────────────────────────────────────────────────────────

function FilterPill({
  label,
  active,
  color,
  onClick,
}: {
  label: string;
  active: boolean;
  color?: string;
  onClick: () => void;
}) {
  return (
    <button
      onClick={onClick}
      className={`text-xs font-mono px-2 py-0.5 border transition-colors ${
        active
          ? 'border-blue text-text'
          : 'border-border text-text-muted hover:text-text'
      }`}
      style={active && color ? { borderColor: color, color } : undefined}
    >
      {label}
    </button>
  );
}

// ── Activity Row ─────────────────────────────────────────────────────────────

function ActivityRow({ entry }: { entry: ActivityEntry }) {
  const evt = EVENT_CONFIG[entry.eventType];
  const serviceColor = getServiceColor(entry.serviceSlug);

  return (
    <div className="flex items-start gap-3 py-2 px-3 border-b border-border hover:bg-surface-alt transition-colors">
      {/* Timestamp */}
      <span className="text-xs font-mono text-text-muted w-16 shrink-0 pt-0.5">
        {formatTime(entry.timestamp)}
      </span>

      {/* Service Badge */}
      <span
        className="text-xs font-mono px-1.5 py-0.5 border shrink-0"
        style={{ color: serviceColor, borderColor: serviceColor }}
      >
        {entry.service}
      </span>

      {/* Event Type */}
      <span className={`text-xs font-mono px-1.5 py-0.5 ${evt.bg} ${evt.color} shrink-0`}>
        {evt.label}
      </span>

      {/* Description */}
      <span className="text-xs text-text leading-relaxed min-w-0">
        {entry.description}
      </span>
    </div>
  );
}

// ── Activity Log ─────────────────────────────────────────────────────────────

export default function ActivityLog() {
  const [entries, setEntries] = useState<ActivityEntry[]>([]);
  const [loading, setLoading] = useState(true);
  const [filterService, setFilterService] = useState<string | null>(null);
  const [filterEvent, setFilterEvent] = useState<ActivityEventType | null>(null);

  const load = useCallback(async () => {
    const a = await getActivity();
    setEntries(a);
    setLoading(false);
  }, []);

  useEffect(() => {
    load();
    const iv = setInterval(load, 30_000);
    return () => clearInterval(iv);
  }, [load]);

  // Apply filters
  const filtered = useMemo(() => {
    let items = entries;
    if (filterService) items = items.filter((e) => e.serviceSlug === filterService);
    if (filterEvent) items = items.filter((e) => e.eventType === filterEvent);
    return items;
  }, [entries, filterService, filterEvent]);

  // Group by date
  const grouped = useMemo(() => {
    const groups: { label: string; items: ActivityEntry[] }[] = [];
    let currentLabel = '';
    for (const entry of filtered) {
      const label = getDateGroup(entry.timestamp);
      if (label !== currentLabel) {
        groups.push({ label, items: [] });
        currentLabel = label;
      }
      groups[groups.length - 1].items.push(entry);
    }
    return groups;
  }, [filtered]);

  // Unique services in data
  const serviceNames = useMemo(() => {
    const map = new Map<string, string>();
    for (const e of entries) {
      map.set(e.serviceSlug, e.service);
    }
    return map;
  }, [entries]);

  if (loading) {
    return (
      <div className="p-6">
        <div className="bg-surface border border-border p-4 h-64 animate-pulse" />
      </div>
    );
  }

  return (
    <div className="p-6 space-y-4">
      {/* Filter Bar */}
      <div className="bg-surface border border-border p-3">
        <div className="flex flex-wrap items-center gap-2 mb-2">
          <span className="text-xs text-text-muted uppercase tracking-wider mr-1">Service:</span>
          <FilterPill
            label="All"
            active={filterService === null}
            onClick={() => setFilterService(null)}
          />
          {SERVICE_SLUGS.filter((s) => serviceNames.has(s)).map((slug) => (
            <FilterPill
              key={slug}
              label={serviceNames.get(slug) ?? slug}
              active={filterService === slug}
              color={getServiceColor(slug)}
              onClick={() => setFilterService(filterService === slug ? null : slug)}
            />
          ))}
        </div>
        <div className="flex flex-wrap items-center gap-2">
          <span className="text-xs text-text-muted uppercase tracking-wider mr-1">Event:</span>
          <FilterPill
            label="All"
            active={filterEvent === null}
            onClick={() => setFilterEvent(null)}
          />
          {EVENT_TYPES.map((type) => {
            const cfg = EVENT_CONFIG[type];
            return (
              <FilterPill
                key={type}
                label={cfg.label}
                active={filterEvent === type}
                color={filterEvent === type ? undefined : undefined}
                onClick={() => setFilterEvent(filterEvent === type ? null : type)}
              />
            );
          })}
        </div>
      </div>

      {/* Entries grouped by date */}
      {grouped.length === 0 ? (
        <div className="bg-surface border border-border p-8 text-center">
          <p className="text-text-muted text-sm font-mono">No activity matches the current filters</p>
        </div>
      ) : (
        grouped.map((group) => (
          <div key={group.label}>
            <div className="text-xs font-mono text-text-muted uppercase tracking-wider py-1 px-3 bg-surface-alt border border-border">
              {group.label}
            </div>
            <div className="bg-surface border-x border-b border-border">
              {group.items.map((entry) => (
                <ActivityRow key={entry.id} entry={entry} />
              ))}
            </div>
          </div>
        ))
      )}
    </div>
  );
}
