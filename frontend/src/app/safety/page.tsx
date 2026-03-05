"use client";

import { useEffect, useState } from "react";
import type { SafetyEvent } from "@/lib/types";
import { getSafetyEvents, acknowledgeSafetyEvent } from "@/lib/api";

function severityStyle(severity: string) {
  switch (severity) {
    case "emergency":
      return { bg: "var(--emergency)", text: "#fff" };
    case "critical":
      return { bg: "var(--critical)", text: "#fff" };
    case "warning":
      return { bg: "var(--warning)", text: "#000" };
    default:
      return { bg: "var(--border)", text: "var(--text)" };
  }
}

export default function SafetyDashboard() {
  const [events, setEvents] = useState<SafetyEvent[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const loadEvents = () => {
    setLoading(true);
    getSafetyEvents()
      .then(setEvents)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    loadEvents();
    const interval = setInterval(loadEvents, 10000);
    return () => clearInterval(interval);
  }, []);

  const handleAcknowledge = async (eventId: string) => {
    try {
      await acknowledgeSafetyEvent(eventId);
      setEvents((prev) =>
        prev.map((e) => (e.id === eventId ? { ...e, acknowledged: true } : e)),
      );
    } catch (e) {
      console.error("Failed to acknowledge:", e);
    }
  };

  const unacknowledged = events.filter((e) => !e.acknowledged);
  const acknowledged = events.filter((e) => e.acknowledged);

  return (
    <div className="p-6 max-w-4xl mx-auto">
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold">Safety Monitor</h1>
        <div className="flex items-center gap-2">
          {unacknowledged.length > 0 ? (
            <span className="px-2 py-1 rounded text-xs font-semibold"
              style={{ background: "var(--critical)", color: "#fff" }}>
              {unacknowledged.length} active alert{unacknowledged.length !== 1 ? "s" : ""}
            </span>
          ) : (
            <span className="px-2 py-1 rounded text-xs"
              style={{ background: "var(--safe)", color: "#000" }}>
              All clear
            </span>
          )}
        </div>
      </div>

      {loading && events.length === 0 && (
        <p style={{ color: "var(--text-muted)" }}>Loading events...</p>
      )}
      {error && (
        <p className="text-sm mb-4" style={{ color: "var(--critical)" }}>{error}</p>
      )}

      {/* Active alerts */}
      {unacknowledged.length > 0 && (
        <div className="mb-6">
          <h2 className="text-sm font-semibold mb-3" style={{ color: "var(--text-muted)" }}>
            ACTIVE ALERTS
          </h2>
          <div className="space-y-2">
            {unacknowledged.map((event) => {
              const style = severityStyle(event.severity);
              return (
                <div key={event.id} className="flex items-center gap-3 p-3 rounded-lg"
                  style={{ background: "var(--surface)", border: `1px solid ${style.bg}` }}>
                  <span className="px-2 py-0.5 rounded text-xs font-bold uppercase"
                    style={{ background: style.bg, color: style.text }}>
                    {event.severity}
                  </span>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-semibold">{event.system_type}: {event.parameter}</p>
                    <p className="text-xs" style={{ color: "var(--text-muted)" }}>
                      {event.message} · Value: {event.value.toFixed(2)} (threshold: {event.threshold.toFixed(2)})
                    </p>
                  </div>
                  <span className="text-xs font-mono" style={{ color: "var(--text-muted)" }}>
                    {new Date(event.created_at || event.timestamp).toLocaleTimeString()}
                  </span>
                  <button
                    onClick={() => handleAcknowledge(event.id)}
                    className="px-2 py-1 rounded text-xs"
                    style={{ background: "var(--border)", color: "var(--text)" }}
                  >
                    ACK
                  </button>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* History */}
      {acknowledged.length > 0 && (
        <div>
          <h2 className="text-sm font-semibold mb-3" style={{ color: "var(--text-muted)" }}>
            HISTORY
          </h2>
          <div className="space-y-1">
            {acknowledged.slice(0, 50).map((event) => (
              <div key={event.id} className="flex items-center gap-3 p-2 rounded text-xs"
                style={{ color: "var(--text-muted)" }}>
                <span className="w-16 uppercase">{event.severity}</span>
                <span className="flex-1">{event.system_type}: {event.parameter} = {event.value.toFixed(2)}</span>
                <span className="font-mono">{new Date(event.created_at || event.timestamp).toLocaleString()}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {events.length === 0 && !loading && (
        <div className="text-center py-12" style={{ color: "var(--text-muted)" }}>
          <p className="text-lg mb-1">No safety events</p>
          <p className="text-sm">All material systems operating within thresholds.</p>
        </div>
      )}
    </div>
  );
}
