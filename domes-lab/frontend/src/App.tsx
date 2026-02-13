import { useState, useEffect } from 'react';
import LabHome from './components/LabHome';
import DomainDetail from './components/DomainDetail';
import ReadinessDashboard from './components/ReadinessDashboard';
import ConnectionsMap from './components/ConnectionsMap';
import BriefGenerator from './components/BriefGenerator';

type View =
  | { page: 'home' }
  | { page: 'domain'; slug: string }
  | { page: 'readiness' }
  | { page: 'connections' }
  | { page: 'brief' };

interface NavItem {
  id: string;
  label: string;
  symbol: string;
  description: string;
  view: View;
}

const NAV_ITEMS: NavItem[] = [
  { id: 'home', label: 'Lab Home', symbol: '[*]', description: '11 Domain Grid', view: { page: 'home' } },
  { id: 'readiness', label: 'Readiness', symbol: '[!]', description: '4-Column Board', view: { page: 'readiness' } },
  { id: 'connections', label: 'Connections', symbol: '[&]', description: 'Network Map', view: { page: 'connections' } },
  { id: 'brief', label: 'Brief Gen', symbol: '[>]', description: 'Generate Briefs', view: { page: 'brief' } },
];

function App() {
  const [currentView, setCurrentView] = useState<View>({ page: 'home' });
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  const [systemTime, setSystemTime] = useState(new Date());

  useEffect(() => {
    const timer = setInterval(() => setSystemTime(new Date()), 1000);
    return () => clearInterval(timer);
  }, []);

  const navigateTo = (view: View) => setCurrentView(view);
  const navigateToDomain = (slug: string) => setCurrentView({ page: 'domain', slug });

  const renderView = () => {
    switch (currentView.page) {
      case 'home':
        return <LabHome onSelectDomain={navigateToDomain} />;
      case 'domain':
        return <DomainDetail slug={currentView.slug} onBack={() => navigateTo({ page: 'home' })} />;
      case 'readiness':
        return <ReadinessDashboard onSelectDomain={navigateToDomain} />;
      case 'connections':
        return <ConnectionsMap onSelectDomain={navigateToDomain} />;
      case 'brief':
        return <BriefGenerator />;
    }
  };

  const activeId = currentView.page === 'domain' ? 'home' : currentView.page;

  return (
    <div className="flex h-screen overflow-hidden bg-bg text-text">
      {/* Sidebar */}
      <aside
        className={`flex flex-col border-r border-border bg-surface transition-all duration-200 ${
          sidebarCollapsed ? 'w-14' : 'w-56'
        }`}
      >
        <div className="flex items-center justify-between border-b border-border px-3 py-3">
          {!sidebarCollapsed && (
            <div className="font-mono text-xs tracking-widest text-text-muted">
              DOMES LAB
            </div>
          )}
          <button
            onClick={() => setSidebarCollapsed(!sidebarCollapsed)}
            className="flex h-7 w-7 items-center justify-center border border-border font-mono text-xs text-text-muted hover:border-text-muted hover:text-text transition-colors"
          >
            {sidebarCollapsed ? '>' : '<'}
          </button>
        </div>

        <nav className="flex-1 overflow-y-auto py-2">
          {NAV_ITEMS.map((item) => {
            const isActive = activeId === item.id;
            return (
              <button
                key={item.id}
                onClick={() => navigateTo(item.view)}
                className={`flex w-full items-center gap-3 px-3 py-2.5 text-left transition-colors ${
                  isActive
                    ? 'bg-accent/30 border-l-2 border-accent-glow text-text'
                    : 'border-l-2 border-transparent text-text-muted hover:bg-surface-alt hover:text-text'
                }`}
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

        {!sidebarCollapsed && (
          <div className="border-t border-border px-3 py-3">
            <div className="font-mono text-[10px] text-text-muted tracking-wider">
              <div>INNOVATION LABORATORY</div>
              <div className="mt-1">v2.0.0 // R&amp;D DIVISION</div>
            </div>
          </div>
        )}
      </aside>

      {/* Main */}
      <div className="flex flex-1 flex-col overflow-hidden">
        <header className="flex items-center justify-between border-b border-border bg-surface px-6 py-3">
          <div className="flex items-center gap-4">
            <h1 className="font-serif text-xl tracking-wide">DOMES LAB</h1>
            <div className="h-4 w-px bg-border" />
            <span className="font-mono text-xs text-text-muted tracking-widest uppercase">
              Innovation Laboratory
            </span>
          </div>
          <div className="flex items-center gap-5">
            <div className="flex items-center gap-2">
              <div className="h-2 w-2 bg-status-approved animate-pulse" />
              <span className="font-mono text-[10px] text-text-muted tracking-wider">SYSTEM ONLINE</span>
            </div>
            <div className="h-4 w-px bg-border" />
            <span className="font-mono text-[10px] text-accent-glow tracking-wider uppercase">
              {currentView.page === 'domain' ? 'DOMAIN DETAIL' : currentView.page.toUpperCase()}
            </span>
            <div className="h-4 w-px bg-border" />
            <span className="font-mono text-[10px] text-text-muted tabular-nums">
              {systemTime.toLocaleTimeString('en-US', { hour12: false })}
            </span>
          </div>
        </header>

        <main className="flex-1 overflow-y-auto bg-bg p-6">
          {renderView()}
        </main>
      </div>
    </div>
  );
}

export default App;
