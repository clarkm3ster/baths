"use client";

import { useState } from "react";
import { useParams, useRouter } from "next/navigation";
import Link from "next/link";
import { createBookingCompat as createBooking } from "@/lib/api";

/** Material config presets for quick booking. */
const PRESETS: Record<string, Record<string, unknown>> = {
  "Warm Welcome": {
    wall_opacity: 0.7,
    wall_color_rgb: [255, 180, 100],
    thermal_target_celsius: 24,
    light_color_temp_kelvin: 3000,
    light_intensity_lux: 400,
  },
  "Cool Meditation": {
    wall_opacity: 0.3,
    wall_color_rgb: [80, 120, 200],
    thermal_target_celsius: 20,
    light_color_temp_kelvin: 5500,
    light_intensity_lux: 150,
  },
  "Full Sensory": {
    wall_opacity: 0.5,
    wall_color_rgb: [140, 80, 220],
    thermal_target_celsius: 22,
    light_color_temp_kelvin: 4000,
    light_intensity_lux: 600,
    floor_haptic_pattern: "pulse",
    floor_haptic_intensity: 0.3,
  },
  Neutral: {},
};

export default function BookingPage() {
  const { id } = useParams<{ id: string }>();
  const router = useRouter();
  const [date, setDate] = useState("");
  const [startTime, setStartTime] = useState("10:00");
  const [endTime, setEndTime] = useState("12:00");
  const [preset, setPreset] = useState("Neutral");
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!date || !id) return;

    setSubmitting(true);
    setError(null);

    try {
      await createBooking(id, {
        start_time: `${date}T${startTime}:00Z`,
        end_time: `${date}T${endTime}:00Z`,
      });
      router.push(`/spheres/${id}`);
    } catch (err) {
      setError(err instanceof Error ? err.message : String(err));
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="p-6 max-w-xl mx-auto">
      <Link href={`/spheres/${id}`} className="text-sm" style={{ color: "var(--text-muted)" }}>
        &larr; Back to sphere
      </Link>

      <h1 className="text-2xl font-bold mt-4 mb-6">Book Time Slice</h1>

      <form onSubmit={handleSubmit} className="space-y-5">
        {/* Date */}
        <div>
          <label className="block text-sm mb-1" style={{ color: "var(--text-muted)" }}>Date</label>
          <input
            type="date"
            value={date}
            onChange={(e) => setDate(e.target.value)}
            required
            className="w-full px-3 py-2 rounded-lg text-sm"
            style={{ background: "var(--surface)", border: "1px solid var(--border)", color: "var(--text)" }}
          />
        </div>

        {/* Time range */}
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm mb-1" style={{ color: "var(--text-muted)" }}>Start</label>
            <input
              type="time"
              value={startTime}
              onChange={(e) => setStartTime(e.target.value)}
              required
              className="w-full px-3 py-2 rounded-lg text-sm"
              style={{ background: "var(--surface)", border: "1px solid var(--border)", color: "var(--text)" }}
            />
          </div>
          <div>
            <label className="block text-sm mb-1" style={{ color: "var(--text-muted)" }}>End</label>
            <input
              type="time"
              value={endTime}
              onChange={(e) => setEndTime(e.target.value)}
              required
              className="w-full px-3 py-2 rounded-lg text-sm"
              style={{ background: "var(--surface)", border: "1px solid var(--border)", color: "var(--text)" }}
            />
          </div>
        </div>

        {/* Material preset */}
        <div>
          <label className="block text-sm mb-2" style={{ color: "var(--text-muted)" }}>
            Material preset
          </label>
          <div className="grid grid-cols-2 gap-2">
            {Object.keys(PRESETS).map((name) => (
              <button
                key={name}
                type="button"
                onClick={() => setPreset(name)}
                className="px-3 py-2 rounded-lg text-sm text-left transition-colors"
                style={{
                  background: preset === name ? "var(--accent)" : "var(--surface)",
                  color: preset === name ? "#fff" : "var(--text)",
                  border: `1px solid ${preset === name ? "var(--accent)" : "var(--border)"}`,
                }}
              >
                {name}
              </button>
            ))}
          </div>
        </div>

        {/* Preview selected config */}
        {preset !== "Neutral" && (
          <div className="p-3 rounded-lg text-xs font-mono"
            style={{ background: "var(--surface)", border: "1px solid var(--border)" }}>
            {Object.entries(PRESETS[preset]).map(([k, v]) => (
              <div key={k}>
                <span style={{ color: "var(--text-muted)" }}>{k}:</span>{" "}
                {JSON.stringify(v)}
              </div>
            ))}
          </div>
        )}

        {error && (
          <p className="text-sm" style={{ color: "var(--critical)" }}>{error}</p>
        )}

        <button
          type="submit"
          disabled={submitting || !date}
          className="w-full py-2.5 rounded-lg text-sm font-semibold disabled:opacity-50"
          style={{ background: "var(--accent)", color: "#fff" }}
        >
          {submitting ? "Booking..." : "Create Booking"}
        </button>
      </form>
    </div>
  );
}
