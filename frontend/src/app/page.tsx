"use client";

import { useEffect, useState } from "react";
import MapExplorer from "@/components/MapExplorer";
import type { ParcelCollection, ParcelFeature } from "@/lib/types";
import { getParcels } from "@/lib/api";

export default function HomePage() {
  const [parcels, setParcels] = useState<ParcelCollection | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [filter, setFilter] = useState(0);

  useEffect(() => {
    setLoading(true);
    getParcels({ min_viability: filter || undefined, limit: 5000 })
      .then(setParcels)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, [filter]);

  const handleParcelClick = (parcel: ParcelFeature) => {
    // In production this would POST to activate the sphere
    console.log("Activate sphere on parcel:", parcel.id);
  };

  return (
    <div className="flex flex-col h-full">
      {/* Toolbar */}
      <div className="flex items-center gap-4 px-4 py-3 border-b"
        style={{ borderColor: "var(--border)", background: "var(--surface)" }}>
        <h1 className="text-lg font-semibold tracking-tight">
          <span style={{ color: "var(--accent)" }}>SPHERE</span>/OS
        </h1>
        <span style={{ color: "var(--text-muted)" }}>·</span>
        <span className="text-sm" style={{ color: "var(--text-muted)" }}>
          Philadelphia Vacant Land Explorer
        </span>
        <div className="ml-auto flex items-center gap-2">
          <label className="text-xs" style={{ color: "var(--text-muted)" }}>
            Min viability
          </label>
          <input
            type="range"
            min={0}
            max={100}
            value={filter * 100}
            onChange={(e) => setFilter(Number(e.target.value) / 100)}
            className="w-24 accent-purple-500"
          />
          <span className="text-xs font-mono w-8">{(filter * 100).toFixed(0)}%</span>
        </div>
        {parcels && (
          <span className="text-xs" style={{ color: "var(--text-muted)" }}>
            {parcels.features.length.toLocaleString()} parcels
          </span>
        )}
      </div>

      {/* Map */}
      <div className="flex-1 relative">
        {error ? (
          <div className="flex items-center justify-center h-full">
            <div className="text-center">
              <p className="text-lg mb-2">Could not load parcels</p>
              <p className="text-sm" style={{ color: "var(--text-muted)" }}>{error}</p>
              <p className="text-xs mt-4" style={{ color: "var(--text-muted)" }}>
                Ensure the API is running on localhost:8100
              </p>
            </div>
          </div>
        ) : (
          <MapExplorer parcels={parcels} loading={loading} onParcelClick={handleParcelClick} />
        )}
      </div>
    </div>
  );
}
