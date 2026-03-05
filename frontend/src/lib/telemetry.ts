"use client";

import { useState, useEffect, useRef, useCallback } from "react";

// ── Telemetry simulation ────────────────────────────────────────

export interface TelemetrySnapshot {
  timestamp: string;
  temperature_f: number;
  humidity_pct: number;
  reverb_s: number;
  vibration_mm_s: number;
}

/** Deterministic micro-drift around a center value. */
function drift(center: number, range: number, t: number, seed: number): number {
  const wave1 = Math.sin(t * 0.001 + seed) * range * 0.6;
  const wave2 = Math.sin(t * 0.0037 + seed * 2.7) * range * 0.3;
  const wave3 = Math.sin(t * 0.013 + seed * 0.3) * range * 0.1;
  return center + wave1 + wave2 + wave3;
}

/** Train vibration pulse: near-zero baseline, spikes every ~90s */
function trainPulse(t: number): number {
  const cycle = 90_000; // 90 seconds in ms
  const phase = t % cycle;
  // Spike window: 2 seconds centered at cycle midpoint
  const spikeCenter = cycle / 2;
  const dist = Math.abs(phase - spikeCenter);
  if (dist < 1000) {
    const intensity = 1 - dist / 1000;
    return 0.1 + intensity * intensity * (4.0 + Math.sin(t * 0.05) * 1.0);
  }
  return 0.05 + Math.random() * 0.1; // baseline micro-vibration
}

function generateSnapshot(t: number): TelemetrySnapshot {
  return {
    timestamp: new Date().toISOString(),
    temperature_f: Math.round(drift(58, 1, t, 1.0) * 10) / 10,
    humidity_pct: Math.round(drift(97, 3, t, 2.5) * 10) / 10,
    reverb_s: Math.round(drift(7.2, 2, t, 4.1) * 10) / 10,
    vibration_mm_s: Math.round(trainPulse(t) * 100) / 100,
  };
}

/**
 * Live-updating telemetry values simulating a BELOW environment.
 * Updates every 500ms. Returns the latest snapshot.
 */
export function useTelemetry(intervalMs = 500): TelemetrySnapshot {
  const [snapshot, setSnapshot] = useState<TelemetrySnapshot>(() =>
    generateSnapshot(Date.now())
  );

  useEffect(() => {
    const id = setInterval(() => {
      setSnapshot(generateSnapshot(Date.now()));
    }, intervalMs);
    return () => clearInterval(id);
  }, [intervalMs]);

  return snapshot;
}

// ── Event log ───────────────────────────────────────────────────

export interface TelemetryEvent {
  id: string;
  timestamp: string;
  message: string;
  type: "train" | "vibration" | "humidity" | "acoustic" | "info";
}

const EVENT_TEMPLATES: Array<{
  check: (s: TelemetrySnapshot, prev: TelemetrySnapshot | null) => boolean;
  message: (s: TelemetrySnapshot) => string;
  type: TelemetryEvent["type"];
}> = [
  {
    check: (s) => s.vibration_mm_s > 3.0,
    message: () => "Train detected \u2014 BSL northbound",
    type: "train",
  },
  {
    check: (s) => s.vibration_mm_s > 2.0 && s.vibration_mm_s <= 3.0,
    message: (s) =>
      `Vibration peak \u2014 ${s.vibration_mm_s.toFixed(1)}mm/s`,
    type: "vibration",
  },
  {
    check: (s, prev) =>
      prev !== null &&
      s.humidity_pct > 98 &&
      prev.humidity_pct <= 98,
    message: (s) => `Humidity spike \u2014 ${s.humidity_pct.toFixed(1)}%`,
    type: "humidity",
  },
  {
    check: (s) => s.reverb_s > 9.0,
    message: (s) =>
      `Acoustic event \u2014 ${s.reverb_s.toFixed(1)}s \u2014 source: unknown`,
    type: "acoustic",
  },
];

/**
 * Live event log generating timestamped entries from telemetry data.
 * Keeps the last `maxEvents` entries.
 */
export function useEventLog(maxEvents = 50): TelemetryEvent[] {
  const [events, setEvents] = useState<TelemetryEvent[]>([]);
  const prevRef = useRef<TelemetrySnapshot | null>(null);
  const counterRef = useRef(0);

  const snapshot = useTelemetry(1000);

  const addEvent = useCallback(
    (message: string, type: TelemetryEvent["type"]) => {
      counterRef.current += 1;
      const event: TelemetryEvent = {
        id: `evt-${counterRef.current}`,
        timestamp: new Date().toISOString(),
        message,
        type,
      };
      setEvents((prev) => [event, ...prev].slice(0, maxEvents));
    },
    [maxEvents]
  );

  useEffect(() => {
    for (const template of EVENT_TEMPLATES) {
      if (template.check(snapshot, prevRef.current)) {
        addEvent(template.message(snapshot), template.type);
        break; // one event per tick max
      }
    }
    prevRef.current = snapshot;
  }, [snapshot, addEvent]);

  return events;
}
