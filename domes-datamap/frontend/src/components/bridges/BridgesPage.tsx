import { useState, useEffect, useMemo } from "react";
import type { Bridge } from "../../types";
import { getBridgesPriority } from "../../api/client";
import { BridgeCard } from "./BridgeCard";
import { BridgePlanner } from "./BridgePlanner";

const TYPE_OPTIONS = [
  "technical",
  "legal",
  "policy",
  "consent",
  "funding",
  "administrative",
];
const STATUS_OPTIONS = [
  "proposed",
  "planned",
  "in_progress",
  "completed",
  "blocked",
];

export function BridgesPage() {
  const [bridges, setBridges] = useState<Bridge[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedBridges, setSelectedBridges] = useState<Bridge[]>([]);

  // Filters
  const [typeFilter, setTypeFilter] = useState("");
  const [statusFilter, setStatusFilter] = useState("");
  const [showPlanner, setShowPlanner] = useState(false);

  useEffect(() => {
    setLoading(true);
    getBridgesPriority({ limit: 100 })
      .then(setBridges)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, []);

  const filtered = useMemo(() => {
    return bridges.filter((b) => {
      if (typeFilter && b.bridge_type !== typeFilter) return false;
      if (statusFilter && b.status !== statusFilter) return false;
      return true;
    });
  }, [bridges, typeFilter, statusFilter]);

  function toggleBridge(bridge: Bridge) {
    setSelectedBridges((prev) => {
      const exists = prev.find((b) => b.id === bridge.id);
      if (exists) return prev.filter((b) => b.id !== bridge.id);
      return [...prev, bridge];
    });
    if (!showPlanner) setShowPlanner(true);
  }

  function removeBridge(bridge: Bridge) {
    setSelectedBridges((prev) => prev.filter((b) => b.id !== bridge.id));
  }

  return (
    <div className="flex flex-col h-[calc(100vh-3.5rem)]">
      {/* Header */}
      <div className="border-b border-black px-4 py-2 bg-gray-50">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="font-serif text-lg font-bold uppercase tracking-wide">
              Bridge Planner
            </h2>
            <p className="font-mono text-[0.625rem] text-gray-500 uppercase tracking-wider">
              {filtered.length} bridges / {selectedBridges.length} selected
            </p>
          </div>
          <button
            className={`btn ${showPlanner ? "btn-primary" : ""}`}
            onClick={() => setShowPlanner(!showPlanner)}
          >
            {showPlanner ? "HIDE PLANNER" : "SHOW PLANNER"}{" "}
            {selectedBridges.length > 0 && `(${selectedBridges.length})`}
          </button>
        </div>
      </div>

      {/* Filter Bar */}
      <div className="filter-bar mx-0 border-x-0 border-t-0">
        <label className="font-mono text-[0.625rem] uppercase tracking-wider text-gray-500">
          Filter:
        </label>
        <select
          className="filter-select"
          value={typeFilter}
          onChange={(e) => setTypeFilter(e.target.value)}
        >
          <option value="">All Types</option>
          {TYPE_OPTIONS.map((t) => (
            <option key={t} value={t}>
              {t}
            </option>
          ))}
        </select>
        <select
          className="filter-select"
          value={statusFilter}
          onChange={(e) => setStatusFilter(e.target.value)}
        >
          <option value="">All Statuses</option>
          {STATUS_OPTIONS.map((s) => (
            <option key={s} value={s}>
              {s}
            </option>
          ))}
        </select>
        {(typeFilter || statusFilter) && (
          <button
            className="btn btn-sm"
            onClick={() => {
              setTypeFilter("");
              setStatusFilter("");
            }}
          >
            CLEAR
          </button>
        )}
      </div>

      {/* Content */}
      <div className="flex flex-1 overflow-hidden">
        {/* Bridge List */}
        <div className="flex-1 overflow-auto p-4">
          {loading ? (
            <div className="text-center font-mono text-sm text-gray-500 py-8">
              Loading bridges...
            </div>
          ) : error ? (
            <div className="text-center font-mono text-sm text-red-600 py-8">
              Error: {error}
            </div>
          ) : (
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-3">
              {filtered.map((bridge) => (
                <BridgeCard
                  key={bridge.id}
                  bridge={bridge}
                  selectable
                  selected={selectedBridges.some((b) => b.id === bridge.id)}
                  onSelect={toggleBridge}
                />
              ))}
            </div>
          )}
        </div>

        {/* Planner Panel */}
        {showPlanner && (
          <div className="w-[400px] border-l-2 border-black overflow-auto flex-shrink-0">
            <BridgePlanner
              selectedBridges={selectedBridges}
              onRemove={removeBridge}
              onClear={() => setSelectedBridges([])}
            />
          </div>
        )}
      </div>
    </div>
  );
}
