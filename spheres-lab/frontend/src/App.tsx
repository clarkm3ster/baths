import { useState, useEffect, useCallback } from 'react';
import { Activity, ChevronLeft, ChevronRight } from 'lucide-react';
import LabHome from './components/LabHome';
import DomainDetail from './components/DomainDetail';
import ReadinessDashboard from './components/ReadinessDashboard';
import ConnectionsMap from './components/ConnectionsMap';
import BriefGenerator from './components/BriefGenerator';
import CityComparison from './components/CityComparison';

// ── View Types ───────────────────────────────────────────────

type View =
  | { type: 'home' }
  | { type: 'domain'; slug: string }
  | { type: 'readiness' }
  | { type: 'connections' }
  | { type: 'cities' }
  | { type: 'brief' };

interface NavItem {
  icon: string;
  label: string;
  viewType: string;
}

const NAV_ITEMS: NavItem[] = [
  { icon: '*', label: 'Lab Home', viewType: 'home' },
  { icon: '!', label: 'Readiness', viewType: 'readiness' },
  { icon: '&', label: 'Connections', viewType: 'connections' },
  { icon: '⇆', label: 'City Compare', viewType: 'cities' },
  { icon: '>', label: 'Brief Gen', viewType: 'brief' },
];

// ── App Component ────────────────────────────────────────────

export default function App() {
  const [view, setView] = useState<View>({ type: 'home' });
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [clock, setClock] = useState(new Date());
  const [backendUp, setBackendUp] = useState<boolean | null>(null);

  // Live clock
  useEffect(() => {
    const timer = setInterval(() => setClock(new Date()), 1000);
    return () => clearInterval(timer);
  }, []);

  // Backend health check
  useEffect(() => {
    let cancelled = false;
    async function check() {
      try {
        const res = await fetch('/api/stats');
        if (!cancelled) setBackendUp(res.ok);
      } catch {
        if (!cancelled) setBackendUp(false);
      }
    }
    check();
    const interval = setInterval(check, 30000);
    return () => {
      cancelled = true;
      clearInterval(interval);
    };
  }, []);

  const navigate = useCallback((viewType: string, slug?: string) => {
    switch (viewType) {
      case 'home':
        setView({ type: 'home' });
        break;
      case 'domain':
        setView({ type: 'domain', slug: slug ?? '' });
        break;
      case 'readiness':
        setView({ type: 'readiness' });
        break;
      case 'connections':
        setView({ type: 'connections' });
        break;
      case 'cities':
        setView({ type: 'cities' });
        break;
      case 'brief':
        setView({ type: 'brief' });
        break;
      default:
        setView({ type: 'home' });
    }
  }, []);

  const formatTime = (d: Date) => {
    return d.toLocaleTimeString('en-US', {
      hour12: false,
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit',
    });
  };

  const formatDate = (d: Date) => {
    return d.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
    });
  };

  // ── Render ───────────────────────────────────────────────

  return (
    <div
      style={{
        display: 'flex',
        height: '100vh',
        width: '100vw',
        overflow: 'hidden',
        background: '#050505',
        color: '#FFFFFF',
        fontFamily: "'Inter', -apple-system, BlinkMacSystemFont, sans-serif",
      }}
    >
      {/* ── Sidebar ─────────────────────────────────────── */}
      <aside
        style={{
          width: sidebarOpen ? 240 : 56,
          minWidth: sidebarOpen ? 240 : 56,
          height: '100vh',
          background: '#0A0A0A',
          borderRight: '1px solid #1A1A1A',
          display: 'flex',
          flexDirection: 'column',
          transition: 'width 0.2s ease, min-width 0.2s ease',
          overflow: 'hidden',
          position: 'relative',
          zIndex: 10,
        }}
      >
        {/* Sidebar Header */}
        <div
          style={{
            padding: sidebarOpen ? '20px 16px 16px' : '20px 8px 16px',
            borderBottom: '1px solid #1A1A1A',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            minHeight: 64,
          }}
        >
          {sidebarOpen && (
            <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
              <div
                style={{
                  width: 28,
                  height: 28,
                  borderRadius: 6,
                  background: 'rgba(0,102,255,0.15)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  fontSize: 14,
                  fontWeight: 700,
                  color: '#0066FF',
                  fontFamily: "'JetBrains Mono', monospace",
                }}
              >
                S
              </div>
              <span
                style={{
                  fontSize: 13,
                  fontWeight: 700,
                  letterSpacing: '0.08em',
                  color: 'rgba(255,255,255,0.7)',
                }}
              >
                NAVIGATION
              </span>
            </div>
          )}
          <button
            onClick={() => setSidebarOpen(!sidebarOpen)}
            style={{
              background: 'none',
              border: '1px solid #1A1A1A',
              borderRadius: 6,
              width: 28,
              height: 28,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              cursor: 'pointer',
              color: 'rgba(255,255,255,0.5)',
              flexShrink: 0,
            }}
          >
            {sidebarOpen ? (
              <ChevronLeft size={14} />
            ) : (
              <ChevronRight size={14} />
            )}
          </button>
        </div>

        {/* Nav Items */}
        <nav style={{ flex: 1, padding: '12px 8px', overflowY: 'auto' }}>
          {NAV_ITEMS.map((item) => {
            const isActive = view.type === item.viewType;
            return (
              <button
                key={item.viewType}
                onClick={() => navigate(item.viewType)}
                style={{
                  width: '100%',
                  display: 'flex',
                  alignItems: 'center',
                  gap: 10,
                  padding: sidebarOpen ? '10px 12px' : '10px 0',
                  justifyContent: sidebarOpen ? 'flex-start' : 'center',
                  background: isActive
                    ? 'rgba(0,102,255,0.1)'
                    : 'transparent',
                  border: isActive
                    ? '1px solid rgba(0,102,255,0.2)'
                    : '1px solid transparent',
                  borderRadius: 8,
                  cursor: 'pointer',
                  marginBottom: 4,
                  transition: 'background 0.15s, border 0.15s',
                  color: isActive ? '#FFFFFF' : 'rgba(255,255,255,0.5)',
                }}
                onMouseEnter={(e) => {
                  if (!isActive) {
                    e.currentTarget.style.background = '#111111';
                    e.currentTarget.style.borderColor = '#2A2A2A';
                  }
                }}
                onMouseLeave={(e) => {
                  if (!isActive) {
                    e.currentTarget.style.background = 'transparent';
                    e.currentTarget.style.borderColor = 'transparent';
                  }
                }}
              >
                <span
                  style={{
                    width: 28,
                    height: 28,
                    borderRadius: 6,
                    background: isActive
                      ? 'rgba(0,102,255,0.2)'
                      : 'rgba(255,255,255,0.05)',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    fontSize: 14,
                    fontFamily: "'JetBrains Mono', monospace",
                    fontWeight: 600,
                    color: isActive ? '#0066FF' : 'rgba(255,255,255,0.4)',
                    flexShrink: 0,
                  }}
                >
                  {item.icon}
                </span>
                {sidebarOpen && (
                  <span
                    style={{
                      fontSize: 13,
                      fontWeight: isActive ? 600 : 400,
                      whiteSpace: 'nowrap',
                    }}
                  >
                    {item.label}
                  </span>
                )}
              </button>
            );
          })}
        </nav>

        {/* System Status */}
        <div
          style={{
            padding: sidebarOpen ? '12px 16px' : '12px 8px',
            borderTop: '1px solid #1A1A1A',
          }}
        >
          <div
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: 8,
              justifyContent: sidebarOpen ? 'flex-start' : 'center',
            }}
          >
            <div
              style={{
                width: 8,
                height: 8,
                borderRadius: '50%',
                background:
                  backendUp === null
                    ? '#FFCC00'
                    : backendUp
                    ? '#00CC66'
                    : '#FF3333',
                boxShadow: `0 0 6px ${
                  backendUp === null
                    ? '#FFCC00'
                    : backendUp
                    ? '#00CC66'
                    : '#FF3333'
                }`,
                flexShrink: 0,
              }}
            />
            {sidebarOpen && (
              <span
                style={{
                  fontSize: 11,
                  color: 'rgba(255,255,255,0.4)',
                  fontFamily: "'JetBrains Mono', monospace",
                }}
              >
                {backendUp === null
                  ? 'CHECKING...'
                  : backendUp
                  ? 'API ONLINE'
                  : 'DEMO MODE'}
              </span>
            )}
          </div>
        </div>
      </aside>

      {/* ── Main Content ────────────────────────────────── */}
      <div
        style={{
          flex: 1,
          display: 'flex',
          flexDirection: 'column',
          overflow: 'hidden',
        }}
      >
        {/* ── Top Header ─────────────────────────────────── */}
        <header
          style={{
            height: 56,
            minHeight: 56,
            background: '#0A0A0A',
            borderBottom: '1px solid #1A1A1A',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            padding: '0 24px',
          }}
        >
          {/* Left: Title */}
          <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
            <Activity size={18} style={{ color: '#0066FF' }} />
            <span
              style={{
                fontSize: 15,
                fontWeight: 800,
                letterSpacing: '0.12em',
                color: '#FFFFFF',
              }}
            >
              SPHERES LAB
            </span>
            <span
              style={{
                fontSize: 11,
                color: 'rgba(255,255,255,0.3)',
                fontFamily: "'JetBrains Mono', monospace",
                marginLeft: 4,
              }}
            >
              Innovation Laboratory
            </span>
          </div>

          {/* Right: Clock + Status */}
          <div style={{ display: 'flex', alignItems: 'center', gap: 16 }}>
            <span
              style={{
                fontSize: 11,
                color: 'rgba(255,255,255,0.4)',
                fontFamily: "'JetBrains Mono', monospace",
              }}
            >
              {formatDate(clock)}
            </span>
            <span
              style={{
                fontSize: 13,
                fontWeight: 600,
                color: 'rgba(255,255,255,0.7)',
                fontFamily: "'JetBrains Mono', monospace",
                letterSpacing: '0.05em',
              }}
            >
              {formatTime(clock)}
            </span>
            <div
              style={{
                width: 8,
                height: 8,
                borderRadius: '50%',
                background: '#00CC66',
                boxShadow: '0 0 6px #00CC66',
              }}
            />
          </div>
        </header>

        {/* ── View Content ───────────────────────────────── */}
        <main
          style={{
            flex: 1,
            overflow: 'auto',
            padding: 0,
          }}
        >
          {view.type === 'home' && (
            <LabHome
              onSelectDomain={(slug: string) => navigate('domain', slug)}
            />
          )}
          {view.type === 'domain' && (
            <DomainDetail
              slug={view.slug}
              onBack={() => navigate('home')}
              onNavigate={(v: string) => navigate(v)}
            />
          )}
          {view.type === 'readiness' && <ReadinessDashboard />}
          {view.type === 'connections' && (
            <ConnectionsMap
              onSelectDomain={(slug: string) => navigate('domain', slug)}
            />
          )}
          {view.type === 'cities' && <CityComparison />}
          {view.type === 'brief' && <BriefGenerator />}
        </main>
      </div>
    </div>
  );
}
