/**
 * SPHERES Studio — Explore Page
 *
 * Full-screen 3D exploration of an activation design.
 * Renders the WorldView component which has its own complete HUD
 * (before/after, time-of-day, camera controls, screenshot, audio).
 * This page adds a back button and pulls design data from the store.
 */

import { useCallback, useMemo } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { ArrowLeft } from 'lucide-react';
import WorldView from '../components/WorldView';
import { useStudioStore } from '../context/StudioStore';
import type { DesignElement as StoreElement } from '../context/StudioStore';
import type { DesignElement, ElementDef, Polygon2D } from '../utils/designTo3D';

// Element catalog mapping element IDs to their visual properties
const ELEMENT_CATALOG: Record<string, { name: string; category: string; w: number; h: number; color: string; perm: boolean }> = {
  stage_small: { name: 'Small Stage', category: 'Performance', w: 10, h: 10, color: '#8B5CF6', perm: false },
  stage_medium: { name: 'Medium Stage', category: 'Performance', w: 20, h: 15, color: '#7C3AED', perm: false },
  stage_large: { name: 'Large Stage', category: 'Performance', w: 30, h: 20, color: '#6D28D9', perm: false },
  sound_equipment: { name: 'Sound Equipment', category: 'Performance', w: 5, h: 5, color: '#A78BFA', perm: false },
  screening_wall: { name: 'Screening Wall', category: 'Performance', w: 15, h: 8, color: '#C4B5FD', perm: false },
  bench: { name: 'Bench', category: 'Seating', w: 6, h: 2, color: '#F59E0B', perm: true },
  picnic_table: { name: 'Picnic Table', category: 'Seating', w: 6, h: 4, color: '#FBBF24', perm: true },
  chair_cluster: { name: 'Chair Cluster', category: 'Seating', w: 8, h: 8, color: '#FCD34D', perm: false },
  bleachers: { name: 'Bleachers', category: 'Seating', w: 20, h: 8, color: '#F59E0B', perm: false },
  amphitheater_seating: { name: 'Amphitheater', category: 'Seating', w: 30, h: 20, color: '#D97706', perm: true },
  food_cart: { name: 'Food Cart', category: 'Food & Vendor', w: 6, h: 4, color: '#EF4444', perm: false },
  food_truck_space: { name: 'Food Truck', category: 'Food & Vendor', w: 25, h: 10, color: '#DC2626', perm: false },
  market_stall: { name: 'Market Stall', category: 'Food & Vendor', w: 10, h: 10, color: '#F87171', perm: false },
  vendor_tent: { name: 'Vendor Tent', category: 'Food & Vendor', w: 10, h: 10, color: '#FCA5A5', perm: false },
  raised_bed: { name: 'Raised Bed', category: 'Gardens & Nature', w: 8, h: 4, color: '#22C55E', perm: true },
  tree_planting: { name: 'Tree Planting', category: 'Gardens & Nature', w: 8, h: 8, color: '#16A34A', perm: true },
  flower_garden: { name: 'Flower Garden', category: 'Gardens & Nature', w: 10, h: 10, color: '#4ADE80', perm: true },
  native_meadow: { name: 'Native Meadow', category: 'Gardens & Nature', w: 20, h: 20, color: '#15803D', perm: true },
  water_feature: { name: 'Water Feature', category: 'Gardens & Nature', w: 10, h: 10, color: '#06B6D4', perm: true },
  mural_wall: { name: 'Mural Wall', category: 'Art', w: 20, h: 10, color: '#EC4899', perm: true },
  sculpture_pad: { name: 'Sculpture Pad', category: 'Art', w: 8, h: 8, color: '#F472B6', perm: false },
  interactive_art: { name: 'Interactive Art', category: 'Art', w: 12, h: 12, color: '#DB2777', perm: false },
  art_installation: { name: 'Art Installation', category: 'Art', w: 15, h: 15, color: '#BE185D', perm: false },
  play_structure: { name: 'Play Structure', category: 'Recreation', w: 20, h: 20, color: '#3B82F6', perm: true },
  basketball_half: { name: 'Half Court', category: 'Recreation', w: 30, h: 25, color: '#2563EB', perm: true },
  fitness_station: { name: 'Fitness Station', category: 'Recreation', w: 10, h: 10, color: '#1D4ED8', perm: true },
  sports_field: { name: 'Sports Field', category: 'Recreation', w: 60, h: 30, color: '#1E40AF', perm: true },
  pathway: { name: 'Pathway', category: 'Infrastructure', w: 20, h: 4, color: '#6B7280', perm: true },
  fencing: { name: 'Fencing', category: 'Infrastructure', w: 20, h: 1, color: '#9CA3AF', perm: true },
  lighting_pole: { name: 'Lighting Pole', category: 'Infrastructure', w: 3, h: 3, color: '#D1D5DB', perm: true },
  power_hookup: { name: 'Power Hookup', category: 'Infrastructure', w: 3, h: 3, color: '#E5E7EB', perm: true },
  water_hookup: { name: 'Water Hookup', category: 'Infrastructure', w: 3, h: 3, color: '#93C5FD', perm: true },
  shade_structure: { name: 'Shade Structure', category: 'Infrastructure', w: 15, h: 15, color: '#A3A3A3', perm: false },
  signage: { name: 'Signage', category: 'Infrastructure', w: 4, h: 2, color: '#78716C', perm: true },
};

// Build element definitions map matching the ElementDef interface
function buildElementDefs(): Map<string, ElementDef> {
  const defs = new Map<string, ElementDef>();
  for (const [id, el] of Object.entries(ELEMENT_CATALOG)) {
    defs.set(id, {
      type: id,
      defaultWidth: el.w,
      defaultHeight: el.h,
      category: el.category,
    });
  }
  return defs;
}

const ELEMENT_DEFS = buildElementDefs();

// Convert store elements to the DesignElement format WorldView expects
function toWorldElements(storeElements: StoreElement[]): DesignElement[] {
  return storeElements.map((el) => {
    const catalog = ELEMENT_CATALOG[el.elementId];
    return {
      id: el.instanceId,
      type: el.elementId,
      x: el.x,
      y: el.y,
      width: catalog ? catalog.w * el.scale : 10,
      height: catalog ? catalog.h * el.scale : 10,
      rotation: el.rotation,
      color: catalog?.color ?? '#888',
      name: catalog?.name ?? el.elementId,
      isPermanent: catalog?.perm ?? false,
      category: catalog?.category ?? 'Other',
    };
  });
}

export default function ExplorePage() {
  const navigate = useNavigate();
  const { designId } = useParams();
  const design = useStudioStore((s) => s.design);

  // Convert store parcel footprint to Polygon2D
  const parcelPolygon: Polygon2D | undefined = useMemo(() => {
    if (design.parcelFootprint.length === 0) return undefined;
    return {
      points: design.parcelFootprint.map((p) => ({ x: p.x, y: p.y })),
    };
  }, [design.parcelFootprint]);

  // Compute parcel dimensions
  const parcelWidth = useMemo(() => {
    if (design.parcelFootprint.length === 0) return 100;
    return (
      Math.max(...design.parcelFootprint.map((p) => p.x)) -
      Math.min(...design.parcelFootprint.map((p) => p.x))
    );
  }, [design.parcelFootprint]);

  const parcelDepth = useMemo(() => {
    if (design.parcelFootprint.length === 0) return 80;
    return (
      Math.max(...design.parcelFootprint.map((p) => p.y)) -
      Math.min(...design.parcelFootprint.map((p) => p.y))
    );
  }, [design.parcelFootprint]);

  const worldElements = useMemo(
    () => toWorldElements(design.elements),
    [design.elements]
  );

  const handleScreenshot = useCallback(
    (dataUrl: string) => {
      const link = document.createElement('a');
      link.download = `spheres-${designId || 'design'}-${Date.now()}.png`;
      link.href = dataUrl;
      link.click();
    },
    [designId]
  );

  return (
    <div className="relative h-screen w-screen" style={{ background: '#000' }}>
      {/* WorldView fills the entire screen with its own HUD */}
      <WorldView
        elements={worldElements}
        elementDefs={ELEMENT_DEFS}
        parcelPolygon={parcelPolygon}
        parcelWidth={parcelWidth}
        parcelDepth={parcelDepth}
        initialMode="after"
        onScreenshot={handleScreenshot}
      />

      {/* Back to studio button (overlays on top of WorldView's HUD) */}
      <div className="absolute top-4 left-4 z-50">
        <button
          onClick={() => navigate(-1)}
          style={{
            background: 'rgba(15, 15, 25, 0.85)',
            backdropFilter: 'blur(12px)',
            border: '1px solid rgba(255,255,255,0.12)',
            borderRadius: '10px',
            color: '#fff',
            padding: '8px 16px',
            cursor: 'pointer',
            display: 'flex',
            alignItems: 'center',
            gap: '8px',
            fontSize: '13px',
            fontFamily: 'Inter, system-ui, sans-serif',
            fontWeight: 500,
          }}
        >
          <ArrowLeft size={14} />
          Back to Studio
        </button>
      </div>
    </div>
  );
}
