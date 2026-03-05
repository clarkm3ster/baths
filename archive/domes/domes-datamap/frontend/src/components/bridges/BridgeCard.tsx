import type { Bridge } from "../../types";

const TYPE_COLORS: Record<string, { color: string; bg: string }> = {
  technical: { color: "#2563EB", bg: "#2563EB10" },
  legal: { color: "#7C3AED", bg: "#7C3AED10" },
  policy: { color: "#EA580C", bg: "#EA580C10" },
  consent: { color: "#16A34A", bg: "#16A34A10" },
  funding: { color: "#CA8A04", bg: "#CA8A0410" },
  administrative: { color: "#6B7280", bg: "#6B728010" },
};

const STATUS_COLORS: Record<string, string> = {
  proposed: "#6B7280",
  planned: "#2563EB",
  in_progress: "#CA8A04",
  completed: "#16A34A",
  blocked: "#DC2626",
};

interface BridgeCardProps {
  bridge: Bridge;
  compact?: boolean;
  selectable?: boolean;
  selected?: boolean;
  onSelect?: (bridge: Bridge) => void;
}

export function BridgeCard({
  bridge,
  compact = false,
  selectable = false,
  selected = false,
  onSelect,
}: BridgeCardProps) {
  const typeStyle = TYPE_COLORS[bridge.bridge_type] || TYPE_COLORS.administrative;
  const statusColor = STATUS_COLORS[bridge.status] || "#6B7280";

  if (compact) {
    return (
      <div className="card-dense">
        <div className="flex items-center gap-2 mb-1">
          <span
            className="badge px-2 py-0 text-[0.5625rem]"
            style={{
              color: typeStyle.color,
              borderColor: typeStyle.color,
              backgroundColor: typeStyle.bg,
            }}
          >
            {bridge.bridge_type}
          </span>
          <span className="text-xs font-medium flex-1 truncate">
            {bridge.title}
          </span>
          <span
            className="font-mono text-[0.5625rem] px-1 border"
            style={{ color: statusColor, borderColor: statusColor }}
          >
            {bridge.status}
          </span>
        </div>
        <div className="flex items-center gap-3 text-[0.5625rem] font-mono text-gray-500">
          <span>Cost: {bridge.estimated_cost}</span>
          <span>Timeline: {bridge.timeline}</span>
          <span>Priority: {bridge.priority_score}/10</span>
        </div>
      </div>
    );
  }

  return (
    <div
      className={`card ${selectable ? "cursor-pointer" : ""} ${
        selected ? "border-2 border-black bg-gray-50" : ""
      }`}
      onClick={selectable ? () => onSelect?.(bridge) : undefined}
    >
      {/* Header */}
      <div className="flex items-center gap-2 mb-2">
        {selectable && (
          <span
            className={`w-4 h-4 border-2 border-black flex items-center justify-center flex-shrink-0 ${
              selected ? "bg-black" : "bg-white"
            }`}
          >
            {selected && (
              <svg
                viewBox="0 0 12 12"
                className="w-2.5 h-2.5"
                fill="none"
                stroke="white"
                strokeWidth={2}
              >
                <path d="M2 6l3 3 5-5" />
              </svg>
            )}
          </span>
        )}
        <span
          className="badge px-2 py-0.5 text-[0.625rem]"
          style={{
            color: typeStyle.color,
            borderColor: typeStyle.color,
            backgroundColor: typeStyle.bg,
          }}
        >
          {bridge.bridge_type}
        </span>
        <span
          className="font-mono text-[0.625rem] px-1.5 py-0.5 border"
          style={{ color: statusColor, borderColor: statusColor }}
        >
          {bridge.status}
        </span>
        <span className="font-mono text-[0.5625rem] text-gray-400 ml-auto">
          Gap #{bridge.gap_id}
        </span>
      </div>

      {/* Title & description */}
      <h4 className="text-sm font-semibold mb-1">{bridge.title}</h4>
      <p className="text-xs text-gray-600 mb-3">{bridge.description}</p>

      {/* Scores */}
      <div className="grid grid-cols-3 gap-2 mb-3">
        <div>
          <div className="flex items-center justify-between">
            <span className="font-mono text-[0.5625rem] uppercase text-gray-500">
              Priority
            </span>
            <span className="font-mono text-xs font-bold">
              {bridge.priority_score}
            </span>
          </div>
          <div className="score-bar">
            <div
              className="score-bar-fill"
              style={{
                width: `${bridge.priority_score * 10}%`,
                backgroundColor: "#000",
              }}
            />
          </div>
        </div>
        <div>
          <div className="flex items-center justify-between">
            <span className="font-mono text-[0.5625rem] uppercase text-gray-500">
              Impact
            </span>
            <span className="font-mono text-xs font-bold">
              {bridge.impact_score}
            </span>
          </div>
          <div className="score-bar">
            <div
              className="score-bar-fill"
              style={{
                width: `${bridge.impact_score * 10}%`,
                backgroundColor: "#16A34A",
              }}
            />
          </div>
        </div>
        <div>
          <div className="flex items-center justify-between">
            <span className="font-mono text-[0.5625rem] uppercase text-gray-500">
              Effort
            </span>
            <span className="font-mono text-xs font-bold">
              {bridge.effort_score}
            </span>
          </div>
          <div className="score-bar">
            <div
              className="score-bar-fill"
              style={{
                width: `${bridge.effort_score * 10}%`,
                backgroundColor:
                  bridge.effort_score <= 3
                    ? "#16A34A"
                    : bridge.effort_score <= 6
                    ? "#CA8A04"
                    : "#DC2626",
              }}
            />
          </div>
        </div>
      </div>

      {/* Details grid */}
      <div className="grid grid-cols-3 gap-2 text-[0.6875rem]">
        <div>
          <span className="font-mono text-[0.5625rem] uppercase text-gray-500 block">
            Cost
          </span>
          <span className="font-mono font-medium">{bridge.estimated_cost}</span>
        </div>
        <div>
          <span className="font-mono text-[0.5625rem] uppercase text-gray-500 block">
            Timeline
          </span>
          <span className="font-mono font-medium">{bridge.timeline}</span>
        </div>
        <div>
          <span className="font-mono text-[0.5625rem] uppercase text-gray-500 block">
            Who Pays
          </span>
          <span className="font-mono font-medium">{bridge.who_pays}</span>
        </div>
      </div>

      {/* Requirements */}
      {(bridge.technical_requirements || bridge.legal_requirements) && (
        <div className="mt-3 pt-2 border-t border-gray-200 space-y-1">
          {bridge.technical_requirements && (
            <div>
              <span className="font-mono text-[0.5625rem] uppercase text-gray-500">
                Technical:{" "}
              </span>
              <span className="text-[0.6875rem]">
                {bridge.technical_requirements}
              </span>
            </div>
          )}
          {bridge.legal_requirements && (
            <div>
              <span className="font-mono text-[0.5625rem] uppercase text-gray-500">
                Legal:{" "}
              </span>
              <span className="text-[0.6875rem]">
                {bridge.legal_requirements}
              </span>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
