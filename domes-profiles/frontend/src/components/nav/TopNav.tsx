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
      <div style={{ maxWidth: "1400px", margin: "0 auto", padding: "16px 24px" }}>
        {/* Branding */}
        <Link to="/" style={{ display: "flex", flexDirection: "column", textDecoration: "none", color: "inherit", marginBottom: "8px" }}>
          <span className="font-serif" style={{ fontSize: "28px", fontWeight: 700, letterSpacing: "-0.01em", textTransform: "uppercase", lineHeight: 1 }}>
            DOMES
          </span>
          <span className="font-mono" style={{ fontSize: "10px", color: "var(--color-text-tertiary)", letterSpacing: "0.06em", textTransform: "uppercase", marginTop: "4px" }}>
            Digital Overview of Managed Entitlements &amp; Services
          </span>
        </Link>

        {/* Navigation links */}
        <div style={{ display: "flex", gap: "4px", overflowX: "auto", WebkitOverflowScrolling: "touch" }}>
          {NAV_LINKS.map((link) => {
            const isActive =
              link.to === '/'
                ? pathname === '/'
                : pathname.startsWith(link.to);

            return (
              <Link
                key={link.to}
                to={link.to}
                className="font-mono"
                style={{
                  padding: "10px 16px",
                  fontSize: "12px",
                  fontWeight: 500,
                  textTransform: "uppercase",
                  letterSpacing: "0.04em",
                  borderBottom: isActive ? "2px solid black" : "2px solid transparent",
                  color: isActive ? "black" : "var(--color-text-tertiary)",
                  textDecoration: "none",
                  whiteSpace: "nowrap",
                  minHeight: "44px",
                  display: "inline-flex",
                  alignItems: "center",
                  transition: "color 0.15s",
                }}
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
