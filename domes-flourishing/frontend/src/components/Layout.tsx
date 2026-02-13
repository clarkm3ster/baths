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
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <Link to="/" className="flex items-baseline gap-3 group">
            <span className="font-serif text-2xl font-bold text-gold tracking-wide">
              DOMES
            </span>
            <span className="font-mono text-[9px] tracking-[0.3em] uppercase text-midnight/40 hidden sm:inline">
              Flourishing
            </span>
          </Link>
          <nav className="flex items-center gap-1 overflow-x-auto">
            {NAV_LINKS.map(({ to, label }) => {
              const active = location.pathname === to || location.pathname.startsWith(to + '/');
              return (
                <Link
                  key={to}
                  to={to}
                  className={`px-3 py-1.5 font-mono text-[10px] tracking-widest uppercase transition-colors whitespace-nowrap ${
                    active
                      ? 'text-gold border-b-2 border-gold'
                      : 'text-midnight/50 hover:text-gold'
                  }`}
                >
                  {label}
                </Link>
              );
            })}
          </nav>
        </div>
      </header>

      <main className="flex-1">{children}</main>

      <footer className="border-t border-midnight/10 py-8 text-center">
        <p className="font-mono text-[10px] tracking-[0.4em] uppercase text-midnight/30">
          The Architecture of Human Flourishing
        </p>
      </footer>
    </div>
  );
}
