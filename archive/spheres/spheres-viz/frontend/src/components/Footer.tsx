// ---------------------------------------------------------------------------
// Footer — SPHERES Viz
// ---------------------------------------------------------------------------
// Minimal, cinematic footer. Blends into the black background. Thin white
// top-border separates it from content above.
// ---------------------------------------------------------------------------

const LINKS = [
  { label: 'Explore', href: '/spheres-assets' },
  { label: 'Design', href: '/spheres-studio' },
  { label: 'Legal', href: '/spheres-legal' },
] as const;

export default function Footer() {
  return (
    <footer
      className="relative w-full"
      style={{ borderTop: '1px solid rgba(255, 255, 255, 0.08)' }}
    >
      <div className="mx-auto max-w-6xl px-6 py-20 md:py-28">
        {/* Wordmark */}
        <p
          className="text-4xl md:text-5xl font-light"
          style={{ letterSpacing: '0.35em', color: 'var(--text)' }}
        >
          SPHERES
        </p>

        {/* Tagline */}
        <p
          className="mt-4 text-sm md:text-base"
          style={{ color: 'var(--text-secondary)', maxWidth: '28rem' }}
        >
          Activating Philadelphia's forgotten spaces
        </p>

        {/* Links */}
        <nav className="mt-10 flex flex-wrap gap-8" aria-label="Footer navigation">
          {LINKS.map(({ label, href }) => (
            <a
              key={label}
              href={href}
              className="text-xs uppercase transition-colors duration-300"
              style={{
                letterSpacing: '0.15em',
                color: 'var(--text-muted)',
              }}
              onMouseEnter={(e) =>
                ((e.currentTarget as HTMLAnchorElement).style.color = 'var(--text)')
              }
              onMouseLeave={(e) =>
                ((e.currentTarget as HTMLAnchorElement).style.color = 'var(--text-muted)')
              }
            >
              {label}
            </a>
          ))}
        </nav>

        {/* Attribution */}
        <div
          className="mt-16 flex flex-col gap-2 text-xs"
          style={{ color: 'var(--text-muted)' }}
        >
          <p>
            A{' '}
            <a
              href="https://baths.studio"
              target="_blank"
              rel="noopener noreferrer"
              className="transition-colors duration-300"
              style={{ color: 'var(--text-secondary)' }}
              onMouseEnter={(e) =>
                ((e.currentTarget as HTMLAnchorElement).style.color = 'var(--text)')
              }
              onMouseLeave={(e) =>
                ((e.currentTarget as HTMLAnchorElement).style.color =
                  'var(--text-secondary)')
              }
            >
              BATHS
            </a>{' '}
            project
          </p>
          <p>&copy; 2025</p>
        </div>
      </div>
    </footer>
  );
}
