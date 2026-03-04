"use client";

import type { MaterialState } from "@/lib/types";

/** System status badge colors. */
function statusColor(status: string): string {
  switch (status) {
    case "active": return "var(--safe)";
    case "transitioning": return "var(--warning)";
    case "emergency_reset": return "var(--emergency)";
    case "error": return "var(--critical)";
    default: return "var(--text-muted)";
  }
}

/** TRL badge. */
function TrlBadge({ trl }: { trl: number }) {
  const bg = trl >= 7 ? "var(--safe)" : trl >= 5 ? "var(--warning)" : "var(--critical)";
  return (
    <span className="text-[10px] font-mono px-1 rounded" style={{ background: bg, color: "#000" }}>
      TRL {trl}
    </span>
  );
}

/** Render a single material system's state. */
function SystemCard({
  name,
  data,
}: {
  name: string;
  data: Record<string, unknown>;
}) {
  const status = (data.status as string) || "unknown";
  const trl = (data.trl as number) || 0;

  // Filter out metadata keys for display
  const displayKeys = Object.entries(data).filter(
    ([k]) => !["system_type", "status", "trl"].includes(k),
  );

  return (
    <div className="p-3 rounded-lg" style={{ background: "var(--surface)", border: "1px solid var(--border)" }}>
      <div className="flex items-center justify-between mb-2">
        <span className="text-sm font-semibold">{name.replace(/_/g, " ")}</span>
        <div className="flex items-center gap-2">
          <TrlBadge trl={trl} />
          <span className="w-2 h-2 rounded-full" style={{ background: statusColor(status) }} />
        </div>
      </div>
      <div className="space-y-1">
        {displayKeys.slice(0, 6).map(([key, val]) => (
          <div key={key} className="flex justify-between text-xs">
            <span style={{ color: "var(--text-muted)" }}>{key}</span>
            <span className="font-mono">
              {typeof val === "number"
                ? val.toFixed(3)
                : typeof val === "object"
                  ? JSON.stringify(val).slice(0, 30)
                  : String(val)}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}

interface Props {
  materialState: MaterialState;
}

export default function MaterialPanel({ materialState }: Props) {
  const systems = Object.entries(materialState);

  if (systems.length === 0) {
    return (
      <div className="text-sm" style={{ color: "var(--text-muted)" }}>
        No material systems loaded.
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
      {systems.map(([name, data]) => (
        <SystemCard key={name} name={name} data={data as Record<string, unknown>} />
      ))}
    </div>
  );
}
