"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const links = [
  { href: "/", label: "Map", icon: "M" },
  { href: "/spheres", label: "Spheres", icon: "S" },
  { href: "/safety", label: "Safety", icon: "!" },
];

export default function Nav() {
  const pathname = usePathname();

  return (
    <nav className="w-16 flex flex-col items-center py-4 gap-6 border-r"
      style={{ borderColor: "var(--border)", background: "var(--surface)" }}>
      <div className="text-xs font-bold tracking-widest" style={{ color: "var(--accent)" }}>
        S/OS
      </div>
      {links.map((link) => {
        const active = pathname === link.href || (link.href !== "/" && pathname.startsWith(link.href));
        return (
          <Link
            key={link.href}
            href={link.href}
            className="w-10 h-10 rounded-lg flex items-center justify-center text-sm font-mono transition-colors"
            style={{
              background: active ? "var(--accent)" : "transparent",
              color: active ? "#fff" : "var(--text-muted)",
            }}
            title={link.label}
          >
            {link.icon}
          </Link>
        );
      })}
    </nav>
  );
}
