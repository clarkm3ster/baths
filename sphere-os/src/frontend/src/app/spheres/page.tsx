"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import type { Sphere } from "@/lib/types";
import { getSpheres } from "@/lib/api";

function statusColor(status: string): string {
  switch (status) {
    case "active": return "var(--safe)";
    case "transitioning": return "var(--warning)";
    case "maintenance": return "var(--critical)";
    default: return "var(--text-muted)";
  }
}

export default function SpheresListPage() {
  const [spheres, setSpheres] = useState<Sphere[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    getSpheres()
      .then(setSpheres)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="p-6 max-w-4xl mx-auto">
      <h1 className="text-2xl font-bold mb-6">Active Spheres</h1>

      {loading && <p style={{ color: "var(--text-muted)" }}>Loading...</p>}
      {error && (
        <div className="p-4 rounded-lg" style={{ background: "var(--surface)", border: "1px solid var(--border)" }}>
          <p className="mb-1">Could not load spheres</p>
          <p className="text-sm" style={{ color: "var(--text-muted)" }}>{error}</p>
        </div>
      )}

      {!loading && spheres.length === 0 && !error && (
        <div className="text-center py-12" style={{ color: "var(--text-muted)" }}>
          <p className="text-lg mb-2">No active spheres</p>
          <p className="text-sm">Activate a parcel from the map to create a sphere.</p>
          <Link href="/" className="inline-block mt-4 px-4 py-2 rounded-lg text-sm"
            style={{ background: "var(--accent)", color: "#fff" }}>
            Go to Map
          </Link>
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {spheres.map((s) => (
          <Link
            key={s.id}
            href={`/spheres/${s.id}`}
            className="block p-4 rounded-lg transition-colors"
            style={{ background: "var(--surface)", border: "1px solid var(--border)" }}
          >
            <div className="flex items-center justify-between mb-2">
              <span className="font-semibold">{s.name}</span>
              <div className="flex items-center gap-1.5">
                <span className="w-2 h-2 rounded-full" style={{ background: statusColor(s.status) }} />
                <span className="text-xs" style={{ color: "var(--text-muted)" }}>{s.status}</span>
              </div>
            </div>
            <div className="text-xs" style={{ color: "var(--text-muted)" }}>
              {s.material_inventory.length} systems · Mode: {s.mode}
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
}
