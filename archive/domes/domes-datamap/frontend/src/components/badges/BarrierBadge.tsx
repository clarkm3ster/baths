const BARRIER_STYLES: Record<string, { color: string; bg: string }> = {
  legal: { color: "#7C3AED", bg: "#7C3AED10" },
  technical: { color: "#2563EB", bg: "#2563EB10" },
  political: { color: "#EA580C", bg: "#EA580C10" },
  consent: { color: "#16A34A", bg: "#16A34A10" },
  funding: { color: "#CA8A04", bg: "#CA8A0410" },
};

interface BarrierBadgeProps {
  barrier: string;
}

export function BarrierBadge({ barrier }: BarrierBadgeProps) {
  const style =
    BARRIER_STYLES[barrier.toLowerCase()] || { color: "#6B7280", bg: "#6B728010" };

  return (
    <span
      className="badge px-2 py-0.5 text-[0.625rem]"
      style={{
        color: style.color,
        borderColor: style.color,
        backgroundColor: style.bg,
      }}
    >
      {barrier}
    </span>
  );
}
