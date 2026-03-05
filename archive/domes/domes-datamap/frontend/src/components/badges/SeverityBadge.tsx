const SEVERITY_STYLES: Record<string, { color: string; bg: string }> = {
  critical: { color: "#DC2626", bg: "#DC262610" },
  high: { color: "#EA580C", bg: "#EA580C10" },
  moderate: { color: "#CA8A04", bg: "#CA8A0410" },
  low: { color: "#6B7280", bg: "#6B728010" },
};

interface SeverityBadgeProps {
  severity: string;
}

export function SeverityBadge({ severity }: SeverityBadgeProps) {
  const style = SEVERITY_STYLES[severity.toLowerCase()] || SEVERITY_STYLES.low;

  return (
    <span
      className="badge px-2 py-0.5 text-[0.625rem]"
      style={{
        color: style.color,
        borderColor: style.color,
        backgroundColor: style.bg,
      }}
    >
      {severity}
    </span>
  );
}
