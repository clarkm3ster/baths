// -----------------------------------------------------------------
// SPHERES BRAIN -- Main Dashboard Shell
// Command center for the SPHERES ecosystem
// -----------------------------------------------------------------

import { useState, useEffect, useCallback } from 'react';
import {
  Brain,
  RefreshCw,
  Wifi,
  WifiOff,
  Clock,
} from 'lucide-react';

import {
  fetchServices,
  fetchHealth,
  fetchActivity,
  fetchMetrics,
  fetchDiscoveries,
  fetchOpportunities,
} from './utils/api';
import type {
  ServiceInfo,
  HealthStatus,
  ActivityItem,
  MetricsData,
  Discovery,
  Opportunity,
} from './utils/api';

import ServiceGrid from './components/ServiceGrid';
import MetricsBar from './components/MetricsBar';
import ParcelSearch from './components/ParcelSearch';
import OpportunityFeed from './components/OpportunityFeed';
import DiscoveryFeed from './components/DiscoveryFeed';
import ActivityLog from './components/ActivityLog';
import HealthMonitor from './components/HealthMonitor';
import PhillyActivityMap from './components/PhillyActivityMap';

// -- Clock helper -----------------------------------------------------------

function useCurrentTime() {
  const [time, setTime] = useState(new Date());
  useEffect(() => {
    const id = setInterval(() => setTime(new Date()), 1000);
    return () => clearInterval(id);
  }, []);
  return time;
}

function formatTime(date: Date): string {
  return date.toLocaleTimeString('en-US', {
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    hour12: false,
  });
}

function formatDate(date: Date): string {
  return date.toLocaleDateString('en-US', {
    weekday: 'short',
    month: 'short',
    day: 'numeric',
    year: 'numeric',
  });
}

// -- Main App ---------------------------------------------------------------

export default function App() {
  const time = useCurrentTime();

  // Data state
  const [services, setServices] = useState<ServiceInfo[]>([]);
  const [health, setHealth] = useState<HealthStatus | null>(null);
  const [activities, setActivities] = useState<ActivityItem[]>([]);
  const [metrics, setMetrics] = useState<MetricsData | null>(null);
  const [discoveries, setDiscoveries] = useState<Discovery[]>([]);
  const [opportunities, setOpportunities] = useState<Opportunity[]>([]);

  // Loading / connection state
  const [loading, setLoading] = useState(true);
  const [connected, setConnected] = useState(true);
  const [lastRefresh, setLastRefresh] = useState<Date | null>(null);

  const loadData = useCallback(async () => {
    setLoading(true);
    try {
      const [svc, hp, act, met, disc, opp] = await Promise.allSettled([
        fetchServices(),
        fetchHealth(),
        fetchActivity(),
        fetchMetrics(),
        fetchDiscoveries(),
        fetchOpportunities(),
      ]);

      if (svc.status === 'fulfilled') setServices(svc.value);
      if (hp.status === 'fulfilled') setHealth(hp.value);
      if (act.status === 'fulfilled') setActivities(act.value);
      if (met.status === 'fulfilled') setMetrics(met.value);
      if (disc.status === 'fulfilled') setDiscoveries(disc.value);
      if (opp.status === 'fulfilled') setOpportunities(opp.value);

      setConnected(true);
      setLastRefresh(new Date());
    } catch {
      setConnected(false);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadData();
    const id = setInterval(loadData, 60000); // refresh every 60s
    return () => clearInterval(id);
  }, [loadData]);

  return (
    <div
      style={{
        minHeight: '100vh',
        background: '#050505',
        display: 'flex',
        flexDirection: 'column',
      }}
    >
      {/* ── Top Bar ─────────────────────────────────────────────── */}
      <header
        style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          padding: '0 20px',
          height: 48,
          borderBottom: '1px solid var(--border)',
          background: 'var(--bg-card)',
          flexShrink: 0,
          position: 'sticky',
          top: 0,
          zIndex: 100,
        }}
      >
        {/* Left: Logo */}
        <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
          <Brain size={18} style={{ color: '#0066FF' }} />
          <span
            style={{
              fontSize: 14,
              fontWeight: 700,
              letterSpacing: '0.12em',
              textTransform: 'uppercase',
              color: '#FFFFFF',
            }}
          >
            SPHERES BRAIN
          </span>
          <span
            style={{
              fontSize: 9,
              color: 'var(--text-tertiary)',
              background: 'var(--accent-dim)',
              padding: '2px 6px',
              borderRadius: 3,
              fontWeight: 500,
              letterSpacing: '0.06em',
              marginLeft: 4,
            }}
          >
            COMMAND CENTER
          </span>
        </div>

        {/* Center: System status */}
        <div style={{ display: 'flex', alignItems: 'center', gap: 16 }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
            {connected ? (
              <Wifi size={12} style={{ color: 'var(--green)' }} />
            ) : (
              <WifiOff size={12} style={{ color: 'var(--red)' }} />
            )}
            <span
              style={{
                fontSize: 10,
                color: connected ? 'var(--green)' : 'var(--red)',
                fontWeight: 500,
                textTransform: 'uppercase',
                letterSpacing: '0.04em',
              }}
            >
              {connected ? 'Connected' : 'Offline'}
            </span>
          </div>

          {lastRefresh && (
            <span
              style={{
                fontSize: 9,
                color: 'var(--text-tertiary)',
                fontFamily: 'var(--mono)',
              }}
            >
              Last sync {formatTime(lastRefresh)}
            </span>
          )}

          <button
            onClick={loadData}
            disabled={loading}
            style={{
              background: 'transparent',
              border: '1px solid var(--border)',
              borderRadius: 4,
              padding: '4px 8px',
              color: 'var(--text-tertiary)',
              cursor: loading ? 'wait' : 'pointer',
              display: 'flex',
              alignItems: 'center',
              gap: 4,
              fontSize: 10,
              transition: 'all 0.15s ease',
            }}
            onMouseEnter={(e) => {
              (e.currentTarget as HTMLElement).style.borderColor = 'var(--border-hover)';
              (e.currentTarget as HTMLElement).style.color = 'var(--text-secondary)';
            }}
            onMouseLeave={(e) => {
              (e.currentTarget as HTMLElement).style.borderColor = 'var(--border)';
              (e.currentTarget as HTMLElement).style.color = 'var(--text-tertiary)';
            }}
          >
            <RefreshCw
              size={10}
              style={{
                animation: loading ? 'spin 1s linear infinite' : 'none',
              }}
            />
            REFRESH
          </button>
        </div>

        {/* Right: Time */}
        <div
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: 10,
          }}
        >
          <Clock size={12} style={{ color: 'var(--text-tertiary)' }} />
          <div style={{ textAlign: 'right' }}>
            <div
              style={{
                fontFamily: 'var(--mono)',
                fontSize: 14,
                fontWeight: 600,
                color: '#FFFFFF',
                letterSpacing: '0.04em',
                lineHeight: 1,
              }}
            >
              {formatTime(time)}
            </div>
            <div
              style={{
                fontSize: 9,
                color: 'var(--text-tertiary)',
                letterSpacing: '0.02em',
                lineHeight: 1,
                marginTop: 2,
              }}
            >
              {formatDate(time)}
            </div>
          </div>
        </div>
      </header>

      {/* ── Dashboard Body ──────────────────────────────────────── */}
      <main
        style={{
          flex: 1,
          padding: 20,
          display: 'flex',
          flexDirection: 'column',
          gap: 16,
          maxWidth: 1600,
          width: '100%',
          margin: '0 auto',
        }}
      >
        {/* Row 1: Metrics bar */}
        <MetricsBar metrics={metrics} loading={loading} />

        {/* Row 2: Service grid */}
        <ServiceGrid services={services} loading={loading} />

        {/* Row 3: Search (full width) */}
        <ParcelSearch />

        {/* Row 4: Main content grid */}
        <div
          style={{
            display: 'grid',
            gridTemplateColumns: '1fr 1fr',
            gap: 16,
          }}
        >
          {/* Left: Opportunity Feed */}
          <OpportunityFeed opportunities={opportunities} loading={loading} />

          {/* Right: Discovery Feed */}
          <DiscoveryFeed discoveries={discoveries} loading={loading} />
        </div>

        {/* Row 5: Bottom panels */}
        <div
          style={{
            display: 'grid',
            gridTemplateColumns: '2fr 1fr 1fr',
            gap: 16,
            minHeight: 360,
          }}
        >
          {/* Activity Log */}
          <ActivityLog activities={activities} loading={loading} />

          {/* Health Monitor */}
          <HealthMonitor health={health} loading={loading} />

          {/* Philly Map */}
          <PhillyActivityMap opportunities={opportunities} loading={loading} />
        </div>
      </main>

      {/* ── Footer ──────────────────────────────────────────────── */}
      <footer
        style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          padding: '12px 20px',
          borderTop: '1px solid var(--border)',
          flexShrink: 0,
        }}
      >
        <span
          style={{
            fontSize: 9,
            color: 'var(--text-tertiary)',
            letterSpacing: '0.06em',
            textTransform: 'uppercase',
          }}
        >
          SPHERES Ecosystem -- Philadelphia Vacant Lot Activation Platform
        </span>
      </footer>

      {/* Global animation styles */}
      <style>{`
        @keyframes spin { to { transform: rotate(360deg); } }
        @keyframes pulse { 0%, 100% { opacity: 0.3; } 50% { opacity: 0.1; } }
      `}</style>
    </div>
  );
}
