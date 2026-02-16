// ─────────────────────────────────────────────────────────────────────────────
// DOMES Brain — Main App Layout
// ─────────────────────────────────────────────────────────────────────────────

import { useState, useEffect, useCallback } from 'react';
import Dashboard from './components/Dashboard.tsx';
import UnifiedSearch from './components/UnifiedSearch.tsx';
import DiscoveryFeed from './components/DiscoveryFeed.tsx';
import HealthMonitor from './components/HealthMonitor.tsx';
import ActivityLog from './components/ActivityLog.tsx';
import QueryExplorer from './components/QueryExplorer.tsx';
import { getHealth, type HealthResponse } from './api/client.ts';

// ── Navigation ───────────────────────────────────────────────────────────────

type View = 'dashboard' | 'search' | 'discoveries' | 'health' | 'activity' | 'query';

interface NavItem {
  id: View;
  label: string;
  symbol: string;
}

const NAV_ITEMS: NavItem[] = [
  { id: 'dashboard', label: 'Dashboard', symbol: '[#]' },
  { id: 'search', label: 'Search', symbol: '[?]' },
  { id: 'discoveries', label: 'Discoveries', symbol: '[!]' },
  { id: 'health', label: 'Health', symbol: '[+]' },
  { id: 'activity', label: 'Activity', symbol: '[~]' },
  { id: 'query', label: 'Query', symbol: '[>]' },
];

// ── View Renderer ────────────────────────────────────────────────────────────

function ViewContent({ view }: { view: View }) {
  switch (view) {
    case 'dashboard':
      return <Dashboard />;
    case 'search':
      return <UnifiedSearch />;
    case 'discoveries':
      return <DiscoveryFeed />;
    case 'health':
      return <HealthMonitor />;
    case 'activity':
      return <ActivityLog />;
    case 'query':
      return <QueryExplorer />;
  }
}

// ── System Status Indicator ──────────────────────────────────────────────────

function SystemStatus({ health }: { health: HealthResponse | null }) {
  if (!health) {
    return (
      <div className="flex items-center gap-2">
        <span className="inline-block w-2 h-2 bg-text-muted animate-pulse" />
        <span className="text-xs font-mono text-text-muted">Connecting...</span>
      </div>
    );
  }

  const allOnline = health.servicesOnline === health.servicesTotal;
  const dotColor = allOnline ? 'bg-green' : 'bg-amber';
  const textColor = allOnline ? 'text-green' : 'text-amber';

  return (
    <div className="flex items-center gap-2">
      <span className={`inline-block w-2 h-2 ${dotColor}`} />
      <span className={`text-xs font-mono ${textColor}`}>
        {health.servicesOnline}/{health.servicesTotal}
      </span>
    </div>
  );
}

// ── App ──────────────────────────────────────────────────────────────────────

function useIsMobile() {
  const [isMobile, setIsMobile] = useState(window.innerWidth <= 768);
  useEffect(() => {
    const handler = () => setIsMobile(window.innerWidth <= 768);
    window.addEventListener("resize", handler);
    return () => window.removeEventListener("resize", handler);
  }, []);
  return isMobile;
}

export default function App() {
  const [view, setView] = useState<View>('dashboard');
  const [health, setHealth] = useState<HealthResponse | null>(null);
  const isMobile = useIsMobile();
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  const effectiveSidebarCollapsed = isMobile ? true : sidebarCollapsed;

  const loadHealth = useCallback(async () => {
    const h = await getHealth();
    setHealth(h);
  }, []);

  useEffect(() => {
    loadHealth();
    const iv = setInterval(loadHealth, 30_000);
    return () => clearInterval(iv);
  }, [loadHealth]);

  return (
    <div className="flex h-screen overflow-hidden bg-bg">
      {/* Sidebar */}
      <aside
        className={`bg-surface border-r border-border flex flex-col shrink-0 transition-all ${
          effectiveSidebarCollapsed ? 'w-14' : 'w-48'
        }`}
        style={isMobile ? { position: 'absolute', left: 0, top: 0, bottom: 0, zIndex: 40 } : undefined}
      >
        {/* Brand */}
        <div className="px-3 py-4 border-b border-border">
          <button
            onClick={() => setSidebarCollapsed(!sidebarCollapsed)}
            className="w-full text-left"
          >
            {effectiveSidebarCollapsed ? (
              <span className="font-mono text-xs text-blue font-bold block text-center">DB</span>
            ) : (
              <div>
                <span className="font-mono text-sm text-blue font-bold tracking-wider">
                  DOMES BRAIN
                </span>
                <span className="block text-xs font-mono text-text-muted mt-0.5">
                  System Command Center
                </span>
              </div>
            )}
          </button>
        </div>

        {/* Nav Items */}
        <nav className="flex-1 py-2">
          {NAV_ITEMS.map((item) => {
            const isActive = view === item.id;
            return (
              <button
                key={item.id}
                onClick={() => setView(item.id)}
                className={`w-full flex items-center gap-2 px-3 py-2 text-left transition-colors ${
                  isActive
                    ? 'bg-surface-alt text-text border-l-2 border-blue'
                    : 'text-text-muted hover:text-text hover:bg-surface-alt border-l-2 border-transparent'
                }`}
              >
                <span className="font-mono text-xs shrink-0">{item.symbol}</span>
                {!effectiveSidebarCollapsed && (
                  <span className="text-sm">{item.label}</span>
                )}
              </button>
            );
          })}
        </nav>

        {/* Footer */}
        <div className="px-3 py-3 border-t border-border">
          <SystemStatus health={health} />
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 overflow-y-auto min-w-0">
        {/* Header */}
        <header className="bg-surface border-b border-border px-6 py-3 flex items-center justify-between sticky top-0 z-10">
          <div className="flex items-center gap-3">
            <h1 className="font-mono text-sm font-bold text-text uppercase tracking-wider">
              {NAV_ITEMS.find((n) => n.id === view)?.label ?? 'Dashboard'}
            </h1>
          </div>
          <div className="flex items-center gap-4">
            <SystemStatus health={health} />
          </div>
        </header>

        {/* View */}
        <ViewContent view={view} />
      </main>
    </div>
  );
}
