import { useState, useEffect } from 'react';
import LabFloor from './components/LabFloor';
import TeammateGrid from './components/TeammateGrid';
import InnovationBrowser from './components/InnovationBrowser';
import CollaborationView from './components/CollaborationView';
import SessionManager from './components/SessionManager';
import StatsPanel from './components/StatsPanel';

type View = 'lab-floor' | 'teammates' | 'innovations' | 'collaborations' | 'sessions' | 'stats';

interface NavItem {
  id: View;
  label: string;
  symbol: string;
  description: string;
}

const NAV_ITEMS: NavItem[] = [
  { id: 'lab-floor', label: 'Lab Floor', symbol: '[*]', description: 'Main Dashboard' },
  { id: 'teammates', label: 'Teammates', symbol: '[=]', description: '12 Domain Experts' },
  { id: 'innovations', label: 'Innovations', symbol: '[!]', description: 'Browse All' },
  { id: 'collaborations', label: 'Collaborations', symbol: '[&]', description: 'Cross-Domain' },
  { id: 'sessions', label: 'Sessions', symbol: '[~]', description: 'Lab Sessions' },
  { id: 'stats', label: 'Stats', symbol: '[%]', description: 'Analytics' },
];

function App() {
  const [currentView, setCurrentView] = useState<View>('lab-floor');
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  const [systemTime, setSystemTime] = useState(new Date());

  useEffect(() => {
    const timer = setInterval(() => setSystemTime(new Date()), 1000);
    return () => clearInterval(timer);
  }, []);

  const renderView = () => {
    switch (currentView) {
      case 'lab-floor': return <LabFloor onNavigate={setCurrentView} />;
      case 'teammates': return <TeammateGrid />;
      case 'innovations': return <InnovationBrowser />;
      case 'collaborations': return <CollaborationView />;
      case 'sessions': return <SessionManager />;
      case 'stats': return <StatsPanel />;
    }
  };

  return (
    <div className="flex h-screen overflow-hidden bg-bg text-text">
      {/* ── Sidebar ── */}
      <aside
        className={`flex flex-col border-r border-border bg-surface transition-all duration-200 ${
          sidebarCollapsed ? 'w-14' : 'w-56'
        }`}
      >
        {/* Sidebar Header */}
        <div className="flex items-center justify-between border-b border-border px-3 py-3">
          {!sidebarCollapsed && (
            <div className="font-mono text-xs tracking-widest text-text-muted">
              NAVIGATION
            </div>
          )}
          <button
            onClick={() => setSidebarCollapsed(!sidebarCollapsed)}
            className="flex h-7 w-7 items-center justify-center border border-border font-mono text-xs text-text-muted hover:border-text-muted hover:text-text transition-colors"
            title={sidebarCollapsed ? 'Expand sidebar' : 'Collapse sidebar'}
          >
            {sidebarCollapsed ? '>' : '<'}
          </button>
        </div>

        {/* Nav Items */}
        <nav className="flex-1 overflow-y-auto py-2">
          {NAV_ITEMS.map((item) => {
            const isActive = currentView === item.id;
            return (
              <button
                key={item.id}
                onClick={() => setCurrentView(item.id)}
                className={`flex w-full items-center gap-3 px-3 py-2.5 text-left transition-colors ${
                  isActive
                    ? 'bg-accent/30 border-l-2 border-accent-glow text-text'
                    : 'border-l-2 border-transparent text-text-muted hover:bg-surface-alt hover:text-text'
                }`}
                title={item.label}
              >
                <span className="font-mono text-xs shrink-0">{item.symbol}</span>
                {!sidebarCollapsed && (
                  <div className="min-w-0">
                    <div className="text-sm font-medium truncate">{item.label}</div>
                    <div className="text-[10px] font-mono text-text-muted tracking-wide truncate">
                      {item.description}
                    </div>
                  </div>
                )}
              </button>
            );
          })}
        </nav>

        {/* Sidebar Footer */}
        {!sidebarCollapsed && (
          <div className="border-t border-border px-3 py-3">
            <div className="font-mono text-[10px] text-text-muted tracking-wider">
              <div>DOMES INNOVATION LAB</div>
              <div className="mt-1">v1.0.0 // CLASSIFIED</div>
            </div>
          </div>
        )}
      </aside>

      {/* ── Main Content ── */}
      <div className="flex flex-1 flex-col overflow-hidden">
        {/* Header */}
        <header className="flex items-center justify-between border-b border-border bg-surface px-6 py-3">
          <div className="flex items-center gap-4">
            <h1 className="font-serif text-xl tracking-wide">DOMES LAB</h1>
            <div className="h-4 w-px bg-border" />
            <span className="font-mono text-xs text-text-muted tracking-widest uppercase">
              Innovation Laboratory
            </span>
          </div>

          <div className="flex items-center gap-5">
            {/* System Status */}
            <div className="flex items-center gap-2">
              <div className="h-2 w-2 bg-status-approved animate-pulse" />
              <span className="font-mono text-[10px] text-text-muted tracking-wider">
                SYSTEM ONLINE
              </span>
            </div>

            <div className="h-4 w-px bg-border" />

            {/* Active View */}
            <span className="font-mono text-[10px] text-accent-glow tracking-wider uppercase">
              {NAV_ITEMS.find(n => n.id === currentView)?.label || 'UNKNOWN'}
            </span>

            <div className="h-4 w-px bg-border" />

            {/* Clock */}
            <span className="font-mono text-[10px] text-text-muted tabular-nums">
              {systemTime.toLocaleTimeString('en-US', { hour12: false })}
            </span>
          </div>
        </header>

        {/* View Content */}
        <main className="flex-1 overflow-y-auto bg-bg p-6">
          {renderView()}
        </main>
      </div>
    </div>
  );
}

export default App;
