import { useRef, useEffect, useCallback } from "react";
import maplibregl from "maplibre-gl";
import "maplibre-gl/dist/maplibre-gl.css";
import type { GeoJSONCollection } from "../types";

interface MapProps {
  geojson: GeoJSONCollection | null;
  onParcelClick: (parcelId: string) => void;
  selectedParcelId?: string;
}

const PHILLY_CENTER: [number, number] = [-75.1652, 39.9526];
const DARK_STYLE = "https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json";

export default function Map({ geojson, onParcelClick, selectedParcelId }: MapProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const mapRef = useRef<maplibregl.Map | null>(null);
  const popupRef = useRef<maplibregl.Popup | null>(null);

  // Initialize map
  useEffect(() => {
    if (!containerRef.current || mapRef.current) return;

    const map = new maplibregl.Map({
      container: containerRef.current,
      style: DARK_STYLE,
      center: PHILLY_CENTER,
      zoom: 12,
      minZoom: 10,
      maxZoom: 19,
    });

    map.addControl(new maplibregl.NavigationControl({ showCompass: false }), "bottom-right");

    map.on("load", () => {
      map.addSource("parcels", {
        type: "geojson",
        data: { type: "FeatureCollection", features: [] },
      });

      // Circle layer for parcels
      map.addLayer({
        id: "parcels-circle",
        type: "circle",
        source: "parcels",
        paint: {
          "circle-radius": [
            "interpolate", ["linear"], ["zoom"],
            10, 2,
            14, 4,
            18, 8,
          ],
          "circle-color": [
            "interpolate", ["linear"], ["get", "score"],
            0, "#1A1A1A",
            25, "#333333",
            50, "#666666",
            75, "#AAAAAA",
            100, "#FFFFFF",
          ],
          "circle-opacity": 0.85,
          "circle-stroke-width": [
            "case",
            ["boolean", ["feature-state", "selected"], false], 2,
            ["boolean", ["feature-state", "hover"], false], 1.5,
            0,
          ],
          "circle-stroke-color": "#FFFFFF",
        },
      });

      // Hover interactivity
      let hoveredId: string | null = null;

      map.on("mouseenter", "parcels-circle", () => {
        map.getCanvas().style.cursor = "pointer";
      });

      map.on("mouseleave", "parcels-circle", () => {
        map.getCanvas().style.cursor = "";
        if (hoveredId) {
          map.setFeatureState({ source: "parcels", id: hoveredId }, { hover: false });
          hoveredId = null;
        }
        popupRef.current?.remove();
      });

      map.on("mousemove", "parcels-circle", (e) => {
        if (!e.features?.length) return;
        const f = e.features[0];
        const id = f.properties?.id;

        if (hoveredId && hoveredId !== id) {
          map.setFeatureState({ source: "parcels", id: hoveredId }, { hover: false });
        }
        if (id) {
          hoveredId = id;
          map.setFeatureState({ source: "parcels", id }, { hover: true });
        }

        // Tooltip
        const props = f.properties!;
        const html = `
          <div style="font-family:'JetBrains Mono',monospace;font-size:10px;opacity:0.6;margin-bottom:3px">${props.id}</div>
          <div style="font-weight:600;margin-bottom:4px">${props.address}</div>
          <div style="font-size:10px;opacity:0.7">
            Score: ${props.score} &middot; ${Number(props.area).toLocaleString()} sqft &middot; $${Number(props.value).toLocaleString()}
          </div>
        `;
        if (!popupRef.current) {
          popupRef.current = new maplibregl.Popup({
            closeButton: false,
            closeOnClick: false,
            offset: 12,
          });
        }
        popupRef.current
          .setLngLat(e.lngLat)
          .setHTML(html)
          .addTo(map);
      });

      map.on("click", "parcels-circle", (e) => {
        if (!e.features?.length) return;
        const id = e.features[0].properties?.id;
        if (id) onParcelClick(id);
      });
    });

    mapRef.current = map;
    return () => { map.remove(); mapRef.current = null; };
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  // Update data
  useEffect(() => {
    const map = mapRef.current;
    if (!map || !geojson) return;

    const src = map.getSource("parcels") as maplibregl.GeoJSONSource | undefined;
    if (src) {
      // Add unique id to each feature for feature-state
      const withIds = {
        ...geojson,
        features: geojson.features.map((f) => ({
          ...f,
          id: f.properties.id,
        })),
      };
      src.setData(withIds as GeoJSON.FeatureCollection);
    }
  }, [geojson]);

  // Highlight selected
  const prevSelectedRef = useRef<string | undefined>();
  useEffect(() => {
    const map = mapRef.current;
    if (!map) return;
    if (prevSelectedRef.current) {
      map.setFeatureState({ source: "parcels", id: prevSelectedRef.current }, { selected: false });
    }
    if (selectedParcelId) {
      map.setFeatureState({ source: "parcels", id: selectedParcelId }, { selected: true });
    }
    prevSelectedRef.current = selectedParcelId;
  }, [selectedParcelId]);

  const handleRecenter = useCallback(() => {
    mapRef.current?.flyTo({ center: PHILLY_CENTER, zoom: 12 });
  }, []);

  return (
    <div style={{ position: "absolute", inset: 0 }}>
      <div ref={containerRef} style={{ width: "100%", height: "100%" }} />
      <button
        onClick={handleRecenter}
        title="Recenter map"
        style={{
          position: "absolute",
          bottom: 100,
          right: 10,
          width: 30,
          height: 30,
          background: "#141414",
          border: "1px solid #2A2A2A",
          color: "#999",
          cursor: "pointer",
          fontSize: 14,
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
        }}
      >
        &bull;
      </button>
    </div>
  );
}
