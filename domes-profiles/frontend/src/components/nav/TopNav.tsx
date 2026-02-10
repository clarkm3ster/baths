import { Link, useLocation } from 'react-router-dom';

const NAV_LINKS = [
  { to: '/', label: 'Home' },
  { to: '/intake', label: 'Build Profile' },
  { to: '/profiles', label: 'Profiles' },
  { to: '/compare', label: 'Compare' },
];

export default function TopNav() {
  const { pathname } = useLocation();

  return (
    <nav className="border-b-2 border-black bg-white">
      <div className="max-w-[1400px] mx-auto px-6 py-4 flex items-end justify-between">
        {/* Branding */}
        <Link to="/" className="flex flex-col">
          <span className="font-serif text-3xl font-bold tracking-tight uppercase leading-none">
            DOMES
          </span>
          <span className="font-mono text-[10px] text-[var(--color-text-tertiary)] tracking-[0.06em] uppercase mt-1">
            Digital Overview of Managed Entitlements &amp; Services
          </span>
        </Link>

        {/* Navigation links */}
        <div className="flex items-center gap-1">
          {NAV_LINKS.map((link) => {
            const isActive =
              link.to === '/'
                ? pathname === '/'
                : pathname.startsWith(link.to);

            return (
              <Link
                key={link.to}
                to={link.to}
                className={`
                  px-4 py-2 font-mono text-[12px] font-medium uppercase tracking-[0.04em]
                  border-b-2 transition-colors
                  ${
                    isActive
                      ? 'border-black text-black'
                      : 'border-transparent text-[var(--color-text-tertiary)] hover:text-black hover:border-[var(--color-border)]'
                  }
                `}
              >
                {link.label}
              </Link>
            );
          })}
        </div>
      </div>
    </nav>
  );
}
