import { useMemo } from "react";
import type { Bridge } from "../../types";

interface BridgePlannerProps {
  selectedBridges: Bridge[];
  onRemove: (bridge: Bridge) => void;
  onClear: () => void;
}

export function BridgePlanner({
  selectedBridges,
  onRemove,
  onClear,
}: BridgePlannerProps) {
  const summary = useMemo(() => {
    const costs = selectedBridges.map((b) => {
      const match = b.estimated_cost.match(/[\d,.]+/);
      if (!match) return 0;
      return parseFloat(match[0].replace(/,/g, ""));
    });
    const totalCost = costs.reduce((a, b) => a + b, 0);

    const timelines = selectedBridges.map((b) => {
      const match = b.timeline.match(/(\d+)/);
      return match ? parseInt(match[1]) : 0;
    });

    const avgPriority =
      selectedBridges.length > 0
        ? selectedBridges.reduce((a, b) => a + b.priority_score, 0) /
          selectedBridges.length
        : 0;

    const avgImpact =
      selectedBridges.length > 0
        ? selectedBridges.reduce((a, b) => a + b.impact_score, 0) /
          selectedBridges.length
        : 0;

    const gapsCovered = new Set(selectedBridges.map((b) => b.gap_id)).size;

    // Sort by priority for implementation sequence
    const sequence = [...selectedBridges].sort(
      (a, b) => b.priority_score - a.priority_score
    );

    return {
      totalCost,
      maxTimeline: Math.max(...timelines, 0),
      avgPriority,
      avgImpact,
      gapsCovered,
      sequence,
    };
  }, [selectedBridges]);

  if (selectedBridges.length === 0) {
    return (
      <div className="panel">
        <div className="panel-header">
          <h3 className="text-sm">Build a Plan</h3>
        </div>
        <div className="panel-body">
          <p className="font-mono text-xs text-gray-500">
            Select bridges from the list to build an implementation plan.
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="panel">
      <div className="panel-header flex items-center justify-between">
        <h3 className="text-sm">
          Implementation Plan ({selectedBridges.length} bridges)
        </h3>
        <button className="btn btn-sm" onClick={onClear}>
          CLEAR PLAN
        </button>
      </div>
      <div className="panel-body space-y-4">
        {/* Summary Stats */}
        <div className="grid grid-cols-5 gap-0 border border-black">
          <div className="stat-block border-r border-black">
            <div className="stat-value text-sm">
              ${summary.totalCost.toLocaleString()}
            </div>
            <div className="stat-label">Total Cost</div>
          </div>
          <div className="stat-block border-r border-black">
            <div className="stat-value text-sm">
              {summary.maxTimeline}mo
            </div>
            <div className="stat-label">Max Timeline</div>
          </div>
          <div className="stat-block border-r border-black">
            <div className="stat-value text-sm">{summary.gapsCovered}</div>
            <div className="stat-label">Gaps Covered</div>
          </div>
          <div className="stat-block border-r border-black">
            <div className="stat-value text-sm">
              {summary.avgPriority.toFixed(1)}
            </div>
            <div className="stat-label">Avg Priority</div>
          </div>
          <div className="stat-block">
            <div className="stat-value text-sm">
              {summary.avgImpact.toFixed(1)}
            </div>
            <div className="stat-label">Avg Impact</div>
          </div>
        </div>

        {/* Implementation Sequence */}
        <div>
          <h4 className="section-header">Implementation Sequence</h4>
          <div className="space-y-1">
            {summary.sequence.map((bridge, idx) => (
              <div
                key={bridge.id}
                className="flex items-center gap-2 border border-gray-200 p-2"
              >
                <span className="font-mono text-xs font-bold w-6 text-center text-gray-400">
                  {idx + 1}.
                </span>
                <div className="flex-1">
                  <p className="text-xs font-medium">{bridge.title}</p>
                  <div className="flex gap-2 mt-0.5 text-[0.5625rem] font-mono text-gray-500">
                    <span>P:{bridge.priority_score}</span>
                    <span>I:{bridge.impact_score}</span>
                    <span>E:{bridge.effort_score}</span>
                    <span>{bridge.estimated_cost}</span>
                    <span>{bridge.timeline}</span>
                  </div>
                </div>
                <button
                  className="btn btn-sm text-[0.5625rem]"
                  onClick={() => onRemove(bridge)}
                >
                  REMOVE
                </button>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
