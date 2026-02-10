import { useState, useEffect, useCallback } from "react";
import Map from "./components/Map";
import StatsBar from "./components/StatsBar";
import FilterPanel from "./components/FilterPanel";
import ParcelDetail from "./components/ParcelDetail";
import ListView from "./components/ListView";
import PortfolioView from "./components/PortfolioView";
import { fetchParcelsGeoJSON, fetchParcels, fetchParcel, fetchStats } from "./api/client";
import type { GeoJSONCollection, ParcelFull, ParcelSummary, Stats, Filters } from "./types";

type View = "map" | "list" | "portfolio";

export default function App() {
  const [view, setView] = useState<View>("map");
  const [geojson, setGeojson] = useState<GeoJSONCollection | null>(null);
  const [stats, setStats] = useState<Stats | null>(null);
  const [statsLoading, setStatsLoading] = useState(true);
  const [selectedId, setSelectedId] = useState<string | undefined>();
  const [selectedParcel, setSelectedParcel] = useState<ParcelFull | null>(null);
  const [detailLoading, setDetailLoading] = useState(false);
  const [filters, setFilters] = useState<Filters>({ score_min: 0, score_max: 100, size_min: 0 });
  const [wards, setWards] = useState<string[]>([]);

  // List view state
  const [listParcels, setListParcels] = useState<ParcelSummary[]>([]);
  const [listTotal, setListTotal] = useState(0);
  const [listLoading, setListLoading] = useState(false);
  const [listOffset, setListOffset] = useState(0);

  // Load stats & wards
  useEffect(() => {
    setStatsLoading(true);
    fetchStats()
      .then((s) => {
        setStats(s);
        setWards(s.by_ward.map((w) => w.ward).filter(Boolean).sort());
      })
      .finally(() => setStatsLoading(false));
  }, []);

  // Load GeoJSON when filters change
  useEffect(() => {
    const params: Record<string, string | number | boolean | undefined> = {};
    if (filters.owner) params.owner = filters.owner;
    if (filters.score_min > 0) params.score_min = filters.score_min;
    if (filters.category) params.category = filters.category;
    if (filters.vacancy !== undefined) params.vacancy = filters.vacancy;
    fetchParcelsGeoJSON(params).then(setGeojson);
  }, [filters.owner, filters.score_min, filters.category, filters.vacancy]);

  // Load list when in list view or filters change
  useEffect(() => {
    if (view !== "list") return;
    setListLoading(true);
    setListOffset(0);
    const params: Record<string, string | number | boolean | undefined> = {
      limit: 200,
      offset: 0,
    };
    if (filters.owner) params.owner = filters.owner;
    if (filters.score_min > 0) params.score_min = filters.score_min;
    if (filters.score_max < 100) params.score_max = filters.score_max;
    if (filters.category) params.category = filters.category;
    if (filters.vacancy !== undefined) params.vacancy = filters.vacancy;
    if (filters.ward) params.ward = filters.ward;
    if (filters.search) params.search = filters.search;
    fetchParcels(params)
      .then((res) => { setListParcels(res.parcels); setListTotal(res.total); })
      .finally(() => setListLoading(false));
  }, [view, filters]);

  const handleLoadMore = useCallback(() => {
    const newOffset = listOffset + 200;
    setListLoading(true);
    const params: Record<string, string | number | boolean | undefined> = {
      limit: 200,
      offset: newOffset,
    };
    if (filters.owner) params.owner = filters.owner;
    if (filters.score_min > 0) params.score_min = filters.score_min;
    fetchParcels(params)
      .then((res) => {
        setListParcels((prev) => [...prev, ...res.parcels]);
        setListOffset(newOffset);
      })
      .finally(() => setListLoading(false));
  }, [listOffset, filters]);

  const handleParcelClick = useCallback((id: string) => {
    setSelectedId(id);
    setDetailLoading(true);
    setSelectedParcel(null);
    fetchParcel(id)
      .then(setSelectedParcel)
      .finally(() => setDetailLoading(false));
  }, []);

  const handleClose = useCallback(() => {
    setSelectedId(undefined);
    setSelectedParcel(null);
  }, []);

  return (
    <>
      {/* Nav + Stats */}
      <div style={{ display: "flex", alignItems: "center", borderBottom: "1px solid #1F1F1F", flexShrink: 0 }}>
        {/* Nav */}
        <div style={{ display: "flex", gap: 0, padding: "0 8px" }}>
          {(["map", "list", "portfolio"] as View[]).map((v) => (
            <button
              key={v}
              onClick={() => setView(v)}
              style={{
                padding: "8px 14px",
                background: view === v ? "#141414" : "transparent",
                border: "none",
                color: view === v ? "#fff" : "#666",
                cursor: "pointer",
                fontSize: 11,
                textTransform: "uppercase",
                letterSpacing: "0.05em",
                fontFamily: "'Inter', sans-serif",
                fontWeight: view === v ? 600 : 400,
              }}
            >
              {v}
            </button>
          ))}
        </div>
        <div style={{ flex: 1 }}>
          <StatsBar stats={stats} loading={statsLoading} />
        </div>
      </div>

      {/* Content */}
      <div style={{ flex: 1, position: "relative", overflow: "hidden" }}>
        {view === "map" && (
          <>
            <Map
              geojson={geojson}
              onParcelClick={handleParcelClick}
              selectedParcelId={selectedId}
            />
            <FilterPanel filters={filters} onChange={setFilters} wards={wards} />
            <ParcelDetail
              parcel={selectedParcel}
              loading={detailLoading}
              onClose={handleClose}
            />
          </>
        )}
        {view === "list" && (
          <ListView
            parcels={listParcels}
            total={listTotal}
            loading={listLoading}
            onParcelClick={handleParcelClick}
            onLoadMore={handleLoadMore}
          />
        )}
        {view === "portfolio" && <PortfolioView />}
      </div>
    </>
  );
}
