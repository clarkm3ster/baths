"use client";

import { useEffect, useRef, useState } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import MaterialStateViz from "@/components/MaterialStateViz";
import MaterialPanel from "@/components/MaterialPanel";
import type { Sphere } from "@/lib/types";
import {
  getSphere,
  getMaterialState,
  getSchedule,
  emergencyReset,
  createMaterialStream,
} from "@/lib/api";

export default function SphereDetailPage() {
  const { id } = useParams<{ id: string }>();
  const [sphere, setSphere] = useState<Sphere | null>(null);
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const [materialState, setMaterialState] = useState<any>({});
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const [bookings, setBookings] = useState<any[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [wsStatus, setWsStatus] = useState<"connecting" | "open" | "closed">("connecting");
  const wsRef = useRef<WebSocket | null>(null);

  // Load sphere + initial state
  useEffect(() => {
    if (!id) return;
    Promise.all([
      getSphere(id).then(setSphere),
      getMaterialState(id).then(setMaterialState),
      getSchedule(id).then(setBookings),
    ]).catch((e) => setError(e.message));
  }, [id]);

  // WebSocket streaming for real-time state
  useEffect(() => {
    if (!id) return;
    setWsStatus("connecting");

    const ws = createMaterialStream(id);
    wsRef.current = ws;

    ws.onopen = () => setWsStatus("open");
    ws.onclose = () => setWsStatus("closed");
    ws.onerror = () => setWsStatus("closed");
    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        if (data.state) setMaterialState(data.state);
      } catch {
        // ignore non-JSON frames
      }
    };

    return () => {
      ws.close();
      wsRef.current = null;
    };
  }, [id]);

  const handleEmergencyReset = async () => {
    if (!id) return;
    if (!confirm("Emergency reset all material systems to safe defaults?")) return;
    try {
      await emergencyReset(id);
      const state = await getMaterialState(id);
      setMaterialState(state);
    } catch (e) {
      setError(String(e));
    }
  };

  if (error) {
    return (
      <div className="p-8">
        <p className="text-lg mb-2">Error loading sphere</p>
        <p className="text-sm" style={{ color: "var(--text-muted)" }}>{error}</p>
      </div>
    );
  }

  return (
    <div className="p-6 max-w-5xl mx-auto space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <div className="flex items-center gap-3">
            <Link href="/" className="text-sm" style={{ color: "var(--text-muted)" }}>
              &larr; Map
            </Link>
            <h1 className="text-2xl font-bold">{sphere?.name || "Sphere"}</h1>
            {sphere && (
              <span className="text-xs px-2 py-0.5 rounded font-mono"
                style={{ background: "var(--accent)", color: "#fff" }}>
                {sphere.status}
              </span>
            )}
          </div>
          <p className="text-sm mt-1" style={{ color: "var(--text-muted)" }}>
            {sphere?.material_inventory.length || 0} material systems installed
          </p>
        </div>
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-1.5 text-xs">
            <span className="w-2 h-2 rounded-full"
              style={{ background: wsStatus === "open" ? "var(--safe)" : wsStatus === "connecting" ? "var(--warning)" : "var(--critical)" }} />
            <span style={{ color: "var(--text-muted)" }}>
              {wsStatus === "open" ? "Live 10Hz" : wsStatus}
            </span>
          </div>
          <button
            onClick={handleEmergencyReset}
            className="px-3 py-1.5 rounded text-sm font-semibold"
            style={{ background: "var(--emergency)", color: "#fff" }}
          >
            Emergency Reset
          </button>
          <Link
            href={`/spheres/${id}/book`}
            className="px-3 py-1.5 rounded text-sm"
            style={{ background: "var(--accent)", color: "#fff" }}
          >
            Book Time
          </Link>
        </div>
      </div>

      {/* 3D Visualization */}
      <MaterialStateViz materialState={materialState} />

      {/* Material Systems Grid */}
      <div>
        <h2 className="text-lg font-semibold mb-3">Material Systems</h2>
        <MaterialPanel materialState={materialState} />
      </div>

      {/* Schedule */}
      <div>
        <h2 className="text-lg font-semibold mb-3">Schedule</h2>
        {bookings.length === 0 ? (
          <p className="text-sm" style={{ color: "var(--text-muted)" }}>No upcoming bookings.</p>
        ) : (
          <div className="space-y-2">
            {bookings.map((b) => (
              <div key={b.id} className="flex items-center justify-between p-3 rounded-lg"
                style={{ background: "var(--surface)", border: "1px solid var(--border)" }}>
                <div>
                  <span className="text-sm font-mono">
                    {new Date(b.start_time).toLocaleDateString()} {new Date(b.start_time).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}
                    {" – "}
                    {new Date(b.end_time).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}
                  </span>
                </div>
                <span className="text-xs px-2 py-0.5 rounded"
                  style={{ background: "var(--border)", color: "var(--text-muted)" }}>
                  {b.status}
                </span>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
