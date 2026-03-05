import { Link, useLocation } from 'react-router-dom';

const NAV_LINKS = [
  { to: '/philosophy', label: 'Philosophy' },
  { to: '/domains', label: 'Domains' },
  { to: '/dome-builder', label: 'Dome Builder' },
  { to: '/finance', label: 'Finance' },
  { to: '/global', label: 'Global' },
  { to: '/flourishing-index', label: 'Index' },
  { to: '/culture', label: 'Culture' },
  { to: '/vitality', label: 'Vitality' },
  { to: '/vision', label: 'Vision' },
];

export default function Layout({ children }: { children: React.ReactNode }) {
  const location = useLocation();

  return (
    <div className="min-h-screen flex flex-col">
      <header className="border-b border-gold/30 bg-warm-white sticky top-0 z-50">
        <div style={{ maxWidth: "1280px", margin: "0 auto", padding: "12px 24px" }}>
          <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: "8px" }}>
            <Link to="/" style={{ display: "flex", alignItems: "baseline", gap: "12px", textDecoration: "none", color: "inherit" }}>
              <span className="font-serif" style={{ fontSize: "24px", fontWeight: 700, color: "var(--color-gold)", letterSpacing: "0.04em" }}>
                DOMES
              </span>
              <span className="font-mono" style={{ fontSize: "9px", letterSpacing: "0.3em", textTransform: "uppercase", color: "rgba(25,25,112,0.4)" }}>
                Flourishing
              </span>
            </Link>
          </div>
          <nav style={{ display: "flex", gap: "4px", overflowX: "auto", WebkitOverflowScrolling: "touch", paddingBottom: "4px" }}>
            {NAV_LINKS.map(({ to, label }) => {
              const active = location.pathname === to || location.pathname.startsWith(to + '/');
              return (
                <Link
                  key={to}
                  to={to}
                  className="font-mono"
                  style={{
                    padding: "8px 12px",
                    fontSize: "10px",
                    letterSpacing: "0.1em",
                    textTransform: "uppercase",
                    whiteSpace: "nowrap",
                    textDecoration: "none",
                    color: active ? "var(--color-gold)" : "rgba(25,25,112,0.5)",
                    borderBottom: active ? "2px solid var(--color-gold)" : "2px solid transparent",
                    minHeight: "44px",
                    display: "inline-flex",
                    alignItems: "center",
                    transition: "color 0.15s",
                  }}
                >
                  {label}
                </Link>
              );
            })}
          </nav>
        </div>
      </header>

      <main className="flex-1">{children}</main>

      <footer style={{ borderTop: "1px solid rgba(25,25,112,0.1)", padding: "32px 24px", textAlign: "center" }}>
        <p className="font-mono" style={{ fontSize: "10px", letterSpacing: "0.4em", textTransform: "uppercase", color: "rgba(25,25,112,0.3)" }}>
          The Architecture of Human Flourishing
        </p>
      </footer>
    </div>
  );
}
