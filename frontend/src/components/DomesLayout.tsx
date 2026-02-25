import { Link, Outlet, useLocation } from 'react-router-dom';
import { useState } from 'react';

const NAV_ITEMS = [
  { path: '/', label: 'Home' },
  { path: '/product', label: 'The Product' },
  { path: '/run', label: 'Run a Dome' },
];

export function DomesLayout() {
  const location = useLocation();
  const [mobileOpen, setMobileOpen] = useState(false);

  const isHome = location.pathname === '/';

  return (
    <div className="min-h-screen flex flex-col">
      <a href="#main-content" className="skip-link">
        Skip to main content
      </a>
      <nav
        className={`fixed top-0 left-0 right-0 z-50 transition-colors duration-300 ${
          isHome ? 'bg-transparent' : 'bg-white/95 backdrop-blur-sm border-b border-border'
        }`}
        role="navigation"
        aria-label="Main navigation"
      >
        <div className="max-w-7xl mx-auto px-6 lg:px-8 flex items-center justify-between h-20">
          <Link
            to="/"
            className="font-serif text-2xl tracking-[0.4em] font-bold no-underline text-black"
            aria-label="DOMES home"
          >
            DOMES
          </Link>

          {/* Desktop nav */}
          <div className="hidden md:flex items-center gap-10 text-sm font-medium tracking-wide">
            {NAV_ITEMS.map(({ path, label }) => (
              <Link
                key={path}
                to={path}
                className={`no-underline hover:text-black transition-colors ${
                  location.pathname === path
                    ? 'text-black border-b-2 border-black pb-0.5'
                    : 'text-black/50'
                }`}
              >
                {label}
              </Link>
            ))}
          </div>

          {/* Mobile hamburger */}
          <button
            className="md:hidden p-2"
            onClick={() => setMobileOpen(!mobileOpen)}
            aria-label="Toggle navigation"
          >
            <div className="w-6 flex flex-col gap-1.5">
              <span className={`block h-0.5 bg-black transition-transform ${mobileOpen ? 'rotate-45 translate-y-2' : ''}`} />
              <span className={`block h-0.5 bg-black transition-opacity ${mobileOpen ? 'opacity-0' : ''}`} />
              <span className={`block h-0.5 bg-black transition-transform ${mobileOpen ? '-rotate-45 -translate-y-2' : ''}`} />
            </div>
          </button>
        </div>

        {/* Mobile menu */}
        {mobileOpen && (
          <div className="md:hidden bg-white border-t border-border">
            <div className="px-6 py-4 flex flex-col gap-4">
              {NAV_ITEMS.map(({ path, label }) => (
                <Link
                  key={path}
                  to={path}
                  className={`no-underline text-lg ${
                    location.pathname === path ? 'text-black font-medium' : 'text-black/50'
                  }`}
                  onClick={() => setMobileOpen(false)}
                >
                  {label}
                </Link>
              ))}
            </div>
          </div>
        )}
      </nav>

      <main id="main-content" className="flex-1" tabIndex={-1}>
        <Outlet />
      </main>

      <footer className="bg-black text-white">
        <div className="max-w-7xl mx-auto px-6 lg:px-8 py-16">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-12">
            <div>
              <h3 className="font-serif text-xl tracking-[0.3em] mb-4">DOMES</h3>
              <p className="text-white/50 text-sm leading-relaxed">
                Character in, dome out. The person is the gravitational center.
                12 layers surround them. Everything is one architecture.
              </p>
            </div>
            <div>
              <h4 className="text-sm font-medium tracking-wider uppercase mb-4 text-white/70">Architecture</h4>
              <ul className="space-y-2 text-sm text-white/50">
                <li>Layers 1-9: AI Agents</li>
                <li>Layers 10-12: Human Design</li>
                <li>FHIR R4 Health Integration</li>
                <li>SDOH Screening Instruments</li>
                <li>Dome Bond Financial Engine</li>
              </ul>
            </div>
            <div>
              <h4 className="text-sm font-medium tracking-wider uppercase mb-4 text-white/70">Data Sources</h4>
              <ul className="space-y-2 text-sm text-white/50">
                <li>US Census ACS 5-Year</li>
                <li>BLS, HUD, FEMA, EPA</li>
                <li>USDA Food Access</li>
                <li>28 Priority US Counties</li>
                <li>5x Daily Auto-Scraping</li>
              </ul>
            </div>
          </div>
          <div className="mt-12 pt-8 border-t border-white/10 text-center text-xs text-white/30">
            BATHS: Cosm x Chron = Flourishing
          </div>
        </div>
      </footer>
    </div>
  );
}
