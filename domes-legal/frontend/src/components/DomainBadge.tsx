import { DOMAIN_COLORS, DOMAIN_LABELS } from "../types";

export default function DomainBadge({ domain }: { domain: string }) {
  const color = DOMAIN_COLORS[domain] || "#333";
  const label = DOMAIN_LABELS[domain] || domain;
  return (
    <span className="domain-badge" style={{ background: color }}>
      {label}
    </span>
  );
}
