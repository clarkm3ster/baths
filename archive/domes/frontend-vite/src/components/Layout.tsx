import { Link, Outlet, useLocation } from 'react-router-dom';

export function Layout() {
  const location = useLocation();

  return (
    <div className="min-h-screen flex flex-col">
      <a href="#main-content" className="skip-link">
        Skip to main content
      </a>
      <nav
        className="border-b border-border print-hide"
        role="navigation"
        aria-label="Main navigation"
      >
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 flex items-center justify-between h-16">
          <Link
            to="/"
            className="font-serif text-xl tracking-[0.3em] font-bold no-underline text-black"
            aria-label="DOMES home"
          >
            DOMES
          </Link>
          <div className="flex gap-8 text-sm font-medium">
            <Link
              to="/"
              className={`no-underline hover:underline ${
                location.pathname === '/' ? 'text-black underline' : 'text-black/60'
              }`}
            >
              Home
            </Link>
            <Link
              to="/circumstances"
              className={`no-underline hover:underline ${
                location.pathname === '/circumstances' ? 'text-black underline' : 'text-black/60'
              }`}
            >
              Map Rights
            </Link>
            <Link
              to="/dome"
              className={`no-underline hover:underline ${
                location.pathname === '/dome' ? 'text-black underline' : 'text-black/60'
              }`}
            >
              Dome View
            </Link>
          </div>
        </div>
      </nav>

      <main id="main-content" className="flex-1" tabIndex={-1}>
        <Outlet />
      </main>
    </div>
  );
}
