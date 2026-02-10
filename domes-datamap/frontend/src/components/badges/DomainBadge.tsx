import { DOMAIN_COLORS } from "../../types";

interface DomainBadgeProps {
  domain: string;
  size?: "sm" | "md";
}

export function DomainBadge({ domain, size = "sm" }: DomainBadgeProps) {
  const color = DOMAIN_COLORS[domain] || "#6B7280";
  const sizeClasses =
    size === "sm"
      ? "px-2 py-0.5 text-[0.625rem]"
      : "px-3 py-1 text-xs";

  return (
    <span
      className={`badge ${sizeClasses}`}
      style={{
        color,
        borderColor: color,
        backgroundColor: `${color}10`,
      }}
    >
      {domain}
    </span>
  );
}
