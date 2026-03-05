/**
 * Footer — Site footer with links to all DOMES apps.
 *
 * Dark background, clean grid of links, minimal.
 */

interface FooterLink {
  label: string;
  href: string;
  description: string;
}

const FOOTER_LINKS: FooterLink[] = [
  {
    label: "Legal Research",
    href: "https://legal.domes.cc",
    description: "Rights mapping",
  },
  {
    label: "Public Assets",
    href: "https://assets.domes.cc",
    description: "Property intelligence",
  },
  {
    label: "Data Research",
    href: "https://data.domes.cc",
    description: "Government data constellation",
  },
  {
    label: "Profile Builder",
    href: "https://profile.domes.cc",
    description: "Composite profile construction",
  },
  {
    label: "Contracts",
    href: "https://contracts.domes.cc",
    description: "Agreement generation",
  },
  {
    label: "Architecture Designer",
    href: "https://architect.domes.cc",
    description: "Coordination architecture",
  },
];

export function Footer() {
  return (
    <footer className="border-t border-border bg-dark px-6 py-20 md:px-12 lg:px-20">
      <div className="mx-auto max-w-5xl">
        {/* DOMES wordmark */}
        <div className="mb-16">
          <span className="font-mono text-[24px] font-bold tracking-widest text-light">
            DOMES
          </span>
          <p className="mt-2 font-sans text-sm text-muted">
            Designing the infrastructure of individual government
          </p>
        </div>

        {/* Links grid */}
        <div className="grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-3">
          {FOOTER_LINKS.map((link) => (
            <a
              key={link.label}
              href={link.href}
              className="group border border-border p-6 transition-colors duration-200 hover:border-light/30"
            >
              <span className="block font-sans text-[16px] font-medium text-light transition-colors duration-200 group-hover:text-accent">
                {link.label}
              </span>
              <span className="mt-1 block font-sans text-xs text-muted">
                {link.description}
              </span>
            </a>
          ))}
        </div>

        {/* Copyright */}
        <div className="mt-20 border-t border-border pt-8">
          <p className="font-mono text-xs text-muted">
            &copy; {new Date().getFullYear()} DOMES Project. Building the
            infrastructure of individual government.
          </p>
        </div>
      </div>
    </footer>
  );
}
