"use client";

import { useCallback, useMemo, useRef, useState } from "react";
import Map, { Layer, Popup, Source } from "react-map-gl";
import type { MapRef, MapLayerMouseEvent } from "react-map-gl";
import "mapbox-gl/dist/mapbox-gl.css";
import type { ParcelCollection, ParcelFeature } from "@/lib/types";

const MAPBOX_TOKEN = process.env.NEXT_PUBLIC_MAPBOX_TOKEN || "";

/** Viability score → color ramp (0=gray, 0.5=amber, 1.0=purple/accent). */
function viabilityColor(score: number | null): string {
  if (score === null || score === undefined) return "#444";
  if (score < 0.3) return "#666";
  if (score < 0.5) return "#b08030";
  if (score < 0.7) return "#c070e0";
  return "#7c5cfc";
}

interface Props {
  parcels: ParcelCollection | null;
  loading: boolean;
  onParcelClick?: (parcel: ParcelFeature) => void;
}

export default function MapExplorer({ parcels, loading, onParcelClick }: Props) {
  const mapRef = useRef<MapRef>(null);
  const [popup, setPopup] = useState<{
    lng: number;
    lat: number;
    feature: ParcelFeature;
  } | null>(null);

  // GeoJSON source with viability-based fill colors baked in
  const geojsonData = useMemo(() => {
    if (!parcels) return null;
    return {
      ...parcels,
      features: parcels.features.map((f) => ({
        ...f,
        properties: {
          ...f.properties,
          _fillColor: viabilityColor(f.properties.viability_score),
        },
      })),
    };
  }, [parcels]);

  const onMapClick = useCallback(
    (e: MapLayerMouseEvent) => {
      const feature = e.features?.[0];
      if (!feature) {
        setPopup(null);
        return;
      }
      const parcel = parcels?.features.find((f) => f.id === feature.id);
      if (parcel && (parcel.geometry as { type: string })?.type === "Point") {
        setPopup({
          lng: (parcel.geometry as GeoJSON.Point).coordinates[0],
          lat: (parcel.geometry as GeoJSON.Point).coordinates[1],
          feature: parcel,
        });
      } else if (parcel) {
        setPopup({ lng: e.lngLat.lng, lat: e.lngLat.lat, feature: parcel });
      }
    },
    [parcels],
  );

  return (
    <div className="relative w-full h-full">
      {loading && (
        <div className="absolute top-4 left-1/2 -translate-x-1/2 z-10 px-4 py-2 rounded-lg text-sm"
          style={{ background: "var(--surface)", border: "1px solid var(--border)" }}>
          Loading parcels...
        </div>
      )}

      <Map
        ref={mapRef}
        initialViewState={{
          longitude: -75.1652,
          latitude: 39.9526,
          zoom: 12,
        }}
        style={{ width: "100%", height: "100%" }}
        mapStyle="mapbox://styles/mapbox/dark-v11"
        mapboxAccessToken={MAPBOX_TOKEN}
        interactiveLayerIds={["parcel-circles"]}
        onClick={onMapClick}
        cursor="pointer"
      >
        {geojsonData && (
          <Source id="parcels" type="geojson" data={geojsonData}>
            <Layer
              id="parcel-circles"
              type="circle"
              paint={{
                "circle-radius": [
                  "interpolate", ["linear"], ["zoom"],
                  10, 2,
                  14, 6,
                  18, 12,
                ],
                "circle-color": ["get", "_fillColor"],
                "circle-opacity": 0.8,
                "circle-stroke-width": 1,
                "circle-stroke-color": "#fff",
                "circle-stroke-opacity": 0.2,
              }}
            />
          </Source>
        )}

        {popup && (
          <Popup
            longitude={popup.lng}
            latitude={popup.lat}
            closeOnClick={false}
            onClose={() => setPopup(null)}
            anchor="bottom"
          >
            <div className="text-sm">
              <p className="font-semibold">{popup.feature.properties.address || "Unknown"}</p>
              <p style={{ color: "var(--text-muted)" }}>
                {popup.feature.properties.area_sqft?.toLocaleString()} sqft
                {popup.feature.properties.zoning && ` · ${popup.feature.properties.zoning}`}
              </p>
              {popup.feature.properties.viability_score !== null && (
                <div className="mt-1 flex items-center gap-2">
                  <span className="text-xs" style={{ color: "var(--text-muted)" }}>Viability</span>
                  <div className="flex-1 h-1.5 rounded-full" style={{ background: "var(--border)" }}>
                    <div
                      className="h-full rounded-full"
                      style={{
                        width: `${(popup.feature.properties.viability_score ?? 0) * 100}%`,
                        background: viabilityColor(popup.feature.properties.viability_score),
                      }}
                    />
                  </div>
                  <span className="text-xs font-mono">
                    {((popup.feature.properties.viability_score ?? 0) * 100).toFixed(0)}
                  </span>
                </div>
              )}
              {onParcelClick && (
                <button
                  className="mt-2 text-xs px-3 py-1 rounded"
                  style={{ background: "var(--accent)", color: "#fff" }}
                  onClick={() => onParcelClick(popup.feature)}
                >
                  Activate Sphere
                </button>
              )}
            </div>
          </Popup>
        )}
      </Map>

      {/* Legend */}
      <div className="absolute bottom-4 right-4 px-3 py-2 rounded-lg text-xs"
        style={{ background: "var(--surface)", border: "1px solid var(--border)" }}>
        <div className="font-semibold mb-1">Viability</div>
        <div className="flex items-center gap-2">
          {[0.2, 0.4, 0.6, 0.8, 1.0].map((v) => (
            <div key={v} className="flex flex-col items-center gap-0.5">
              <div className="w-3 h-3 rounded-full" style={{ background: viabilityColor(v) }} />
              <span style={{ color: "var(--text-muted)" }}>{(v * 100).toFixed(0)}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
