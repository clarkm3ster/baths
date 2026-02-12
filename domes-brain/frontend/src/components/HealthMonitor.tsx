// ─────────────────────────────────────────────────────────────────────────────
// DOMES Brain — Health Monitor: Real-time service health
// ─────────────────────────────────────────────────────────────────────────────

import { useState, useEffect, useCallback } from 'react';
import {
  type ServiceInfo,
  type ServiceStatus,
  getServices,
  formatTimestamp,
  formatTime,
} from '../api/client.ts';

// ── Status Badge ─────────────────────────────────────────────────────────────

function StatusBadge({ status }: { status: ServiceStatus }) {
  const config: Record<ServiceStatus, { dot: string; text: string; label: string }> = {
    online: { dot: 'bg-green', text: 'text-green', label: 'ONLINE' },
    degraded: { dot: 'bg-amber', text: 'text-amber', label: 'DEGRADED' },
    offline: { dot: 'bg-red', text: 'text-red', label: 'OFFLINE' },
  };
  const c = config[status];
  return (
    <span className={`inline-flex items-center gap-1.5 text-xs font-mono ${c.text}`}>
      <span className={`inline-block w-2 h-2 ${c.dot}`} />
      {c.label}
    </span>
  );
}

// ── Uptime Bar ───────────────────────────────────────────────────────────────

function UptimeBar({ history }: { history: boolean[] }) {
  return (
    <div className="flex gap-px" title="Last 24 checks">
      {history.map((up, i) => (
        <div
          key={i}
          className={`w-1.5 h-3 ${up ? 'bg-green' : 'bg-red'}`}
          style={{ opacity: up ? 0.7 : 1 }}
          title={`Check ${i + 1}: ${up ? 'OK' : 'DOWN'}`}
        />
      ))}
    </div>
  );
}

// ── Expanded Detail ──────────────────────────────────────────────────────────

function ServiceDetail({ svc }: { svc: ServiceInfo }) {
  return (
    <tr>
      <td colSpan={6} className="bg-surface-alt border-x border-b border-border p-4">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {/* Endpoints */}
          <div>
            <h4 className="text-xs text-text-muted uppercase tracking-wider mb-2">Endpoints</h4>
            <div className="space-y-1">
              {svc.endpoints.map((ep) => (
                <div key={ep} className="text-xs font-mono text-text">{ep}</div>
              ))}
            </div>
          </div>

          {/* Recent Errors */}
          <div>
            <h4 className="text-xs text-text-muted uppercase tracking-wider mb-2">Recent Errors</h4>
            {svc.recentErrors.length === 0 ? (
              <div className="text-xs font-mono text-green">No recent errors</div>
            ) : (
              <div className="space-y-2">
                {svc.recentErrors.map((err, i) => (
                  <div key={i} className="border-l-2 border-red pl-2">
                    <div className="text-xs font-mono text-red">{err.message}</div>
                    <div className="text-xs font-mono text-text-muted">
                      {err.endpoint} — {formatTimestamp(err.timestamp)}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Data Freshness */}
          <div>
            <h4 className="text-xs text-text-muted uppercase tracking-wider mb-2">Data Freshness</h4>
            <div className="text-xs font-mono text-text">{svc.dataFreshness}</div>
            <h4 className="text-xs text-text-muted uppercase tracking-wider mb-2 mt-4">Service URL</h4>
            <div className="text-xs font-mono text-blue">{svc.url}</div>
          </div>
        </div>
      </td>
    </tr>
  );
}

// ── Health Monitor ───────────────────────────────────────────────────────────

export default function HealthMonitor() {
  const [services, setServices] = useState<ServiceInfo[]>([]);
  const [loading, setLoading] = useState(true);
  const [expandedSlug, setExpandedSlug] = useState<string | null>(null);
  const [lastRefresh, setLastRefresh] = useState<Date>(new Date());
  const [refreshing, setRefreshing] = useState(false);

  const load = useCallback(async () => {
    setRefreshing(true);
    const s = await getServices();
    setServices(s);
    setLastRefresh(new Date());
    setLoading(false);
    setRefreshing(false);
  }, []);

  useEffect(() => {
    load();
    const iv = setInterval(load, 15_000);
    return () => clearInterval(iv);
  }, [load]);

  const toggle = (slug: string) => {
    setExpandedSlug((prev) => (prev === slug ? null : slug));
  };

  if (loading) {
    return (
      <div className="p-6">
        <div className="bg-surface border border-border p-4 h-64 animate-pulse" />
      </div>
    );
  }

  return (
    <div className="p-6 space-y-4">
      {/* Header */}
      <div className="flex items-center justify-between">
        <h2 className="font-serif text-lg text-text">Service Health</h2>
        <div className="flex items-center gap-3">
          <span className={`inline-block w-2 h-2 ${refreshing ? 'bg-blue animate-pulse' : 'bg-green'}`} />
          <span className="text-xs font-mono text-text-muted">
            Auto-refresh 15s — last: {formatTime(lastRefresh.toISOString())}
          </span>
          <button
            onClick={load}
            className="text-xs font-mono text-blue hover:text-text border border-border px-2 py-0.5"
          >
            Refresh
          </button>
        </div>
      </div>

      {/* Table */}
      <div className="overflow-x-auto">
        <table className="w-full border-collapse">
          <thead>
            <tr className="border-b border-border">
              <th className="text-left text-xs text-text-muted uppercase tracking-wider font-mono py-2 px-3">Service</th>
              <th className="text-left text-xs text-text-muted uppercase tracking-wider font-mono py-2 px-3">Status</th>
              <th className="text-left text-xs text-text-muted uppercase tracking-wider font-mono py-2 px-3">Last Check</th>
              <th className="text-right text-xs text-text-muted uppercase tracking-wider font-mono py-2 px-3">Response</th>
              <th className="text-right text-xs text-text-muted uppercase tracking-wider font-mono py-2 px-3">Uptime</th>
              <th className="text-left text-xs text-text-muted uppercase tracking-wider font-mono py-2 px-3">24h History</th>
            </tr>
          </thead>
          {services.map((svc) => {
            const isExpanded = expandedSlug === svc.slug;
            return (
              <tbody key={svc.slug}>
                <tr
                  className={`border-b border-border cursor-pointer hover:bg-surface-alt transition-colors ${
                    isExpanded ? 'bg-surface-alt' : ''
                  }`}
                  onClick={() => toggle(svc.slug)}
                >
                  <td className="py-2 px-3">
                    <div className="flex items-center gap-2">
                      <div
                        className="w-1 h-6 shrink-0"
                        style={{ backgroundColor: svc.domainColor }}
                      />
                      <div>
                        <div className="text-sm font-semibold text-text">{svc.name}</div>
                        <div className="text-xs font-mono text-text-muted">:{svc.port}</div>
                      </div>
                    </div>
                  </td>
                  <td className="py-2 px-3">
                    <StatusBadge status={svc.status} />
                  </td>
                  <td className="py-2 px-3">
                    <span className="text-xs font-mono text-text-muted">
                      {formatTimestamp(svc.lastChecked)}
                    </span>
                  </td>
                  <td className="py-2 px-3 text-right">
                    <span
                      className={`text-xs font-mono font-semibold ${
                        svc.responseTime > 200
                          ? 'text-red'
                          : svc.responseTime > 100
                            ? 'text-amber'
                            : 'text-green'
                      }`}
                    >
                      {svc.responseTime}ms
                    </span>
                  </td>
                  <td className="py-2 px-3 text-right">
                    <span
                      className={`text-xs font-mono font-semibold ${
                        svc.uptime >= 99.5
                          ? 'text-green'
                          : svc.uptime >= 98
                            ? 'text-amber'
                            : 'text-red'
                      }`}
                    >
                      {svc.uptime}%
                    </span>
                  </td>
                  <td className="py-2 px-3">
                    <UptimeBar history={svc.uptimeHistory} />
                  </td>
                </tr>
                {isExpanded && <ServiceDetail svc={svc} />}
              </tbody>
            );
          })}
        </table>
      </div>
    </div>
  );
}
