// ─────────────────────────────────────────────────────────────────────────────
// DOMES Brain — Dashboard: System Overview
// ─────────────────────────────────────────────────────────────────────────────

import { useState, useEffect, useCallback } from 'react';
import {
  type ServiceInfo,
  type HealthResponse,
  type StatsResponse,
  getServices,
  getHealth,
  getStats,
  formatTimestamp,
} from '../api/client.ts';

// ── Status dot ───────────────────────────────────────────────────────────────

function StatusDot({ status }: { status: ServiceInfo['status'] }) {
  const color =
    status === 'online'
      ? 'bg-green'
      : status === 'degraded'
        ? 'bg-amber'
        : 'bg-red';
  return (
    <span
      className={`inline-block w-2 h-2 ${color}`}
      title={status}
    />
  );
}

// ── Service Card ─────────────────────────────────────────────────────────────

function ServiceCard({ svc }: { svc: ServiceInfo }) {
  return (
    <div
      className="bg-surface border border-border p-4 relative"
      style={{ borderLeftWidth: '3px', borderLeftColor: svc.domainColor }}
    >
      <div className="flex items-center justify-between mb-2">
        <h3 className="font-sans font-semibold text-sm text-text">{svc.name}</h3>
        <StatusDot status={svc.status} />
      </div>
      <p className="text-text-muted text-xs mb-3 leading-tight">{svc.description}</p>
      <div className="flex items-center justify-between text-xs font-mono">
        <span className="text-text-muted">
          :{svc.port}
        </span>
        <span
          className={
            svc.responseTime > 200
              ? 'text-amber'
              : svc.responseTime > 100
                ? 'text-blue'
                : 'text-green'
          }
        >
          {svc.responseTime}ms
        </span>
      </div>
      <div className="flex items-center justify-between text-xs font-mono mt-1">
        <span className="text-text-muted">checked {formatTimestamp(svc.lastChecked)}</span>
        <span className="text-text-muted">{svc.uptime}% up</span>
      </div>
    </div>
  );
}

// ── Stats Row ────────────────────────────────────────────────────────────────

function StatBlock({ label, value, mono }: { label: string; value: string | number; mono?: boolean }) {
  return (
    <div className="bg-surface border border-border p-3">
      <div className="text-text-muted text-xs uppercase tracking-wider mb-1">{label}</div>
      <div className={`text-lg font-semibold ${mono ? 'font-mono' : 'font-sans'} text-text`}>
        {value}
      </div>
    </div>
  );
}

// ── Dashboard ────────────────────────────────────────────────────────────────

export default function Dashboard() {
  const [services, setServices] = useState<ServiceInfo[]>([]);
  const [health, setHealth] = useState<HealthResponse | null>(null);
  const [stats, setStats] = useState<StatsResponse | null>(null);
  const [loading, setLoading] = useState(true);

  const load = useCallback(async () => {
    const [s, h, st] = await Promise.all([getServices(), getHealth(), getStats()]);
    setServices(s);
    setHealth(h);
    setStats(st);
    setLoading(false);
  }, []);

  useEffect(() => {
    load();
    const iv = setInterval(load, 30_000);
    return () => clearInterval(iv);
  }, [load]);

  const onlineCount = services.filter((s) => s.status === 'online').length;
  const degradedCount = services.filter((s) => s.status === 'degraded').length;
  const offlineCount = services.filter((s) => s.status === 'offline').length;

  const summaryColor =
    offlineCount > 0
      ? 'text-red'
      : degradedCount > 0
        ? 'text-amber'
        : 'text-green';

  const summaryText = (() => {
    const parts: string[] = [];
    if (offlineCount > 0) parts.push(`${offlineCount} offline`);
    if (degradedCount > 0) parts.push(`${degradedCount} degraded`);
    if (parts.length === 0) return 'All systems operational';
    return `${onlineCount}/${services.length} online — ${parts.join(', ')}`;
  })();

  if (loading) {
    return (
      <div className="p-6">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
          {Array.from({ length: 6 }).map((_, i) => (
            <div key={i} className="bg-surface border border-border p-4 h-28 animate-pulse" />
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="p-6 space-y-4">
      {/* System Health Summary */}
      <div className="bg-surface border border-border p-4 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <span className={`font-mono text-sm font-semibold ${summaryColor}`}>
            {summaryText}
          </span>
        </div>
        <div className="text-xs font-mono text-text-muted">
          Last scan: {health ? formatTimestamp(health.lastScan) : '—'}
        </div>
      </div>

      {/* Stats Row */}
      {stats && (
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
          <StatBlock label="Total Queries" value={stats.totalQueries.toLocaleString()} mono />
          <StatBlock label="Discoveries" value={stats.totalDiscoveries.toLocaleString()} mono />
          <StatBlock label="Avg Response" value={`${stats.avgResponseTime}ms`} mono />
          <StatBlock label="Uptime" value={`${stats.uptimePercent}%`} mono />
          <StatBlock label="Queries / hr" value={stats.queriesThisHour} mono />
          <StatBlock label="Disc. Today" value={stats.discoveriesToday} mono />
        </div>
      )}

      {/* Service Cards Grid */}
      <div>
        <h2 className="font-serif text-lg mb-3 text-text">Services</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
          {services.map((svc) => (
            <ServiceCard key={svc.slug} svc={svc} />
          ))}
        </div>
      </div>
    </div>
  );
}
