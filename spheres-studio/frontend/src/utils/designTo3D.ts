/**
 * designTo3D.ts — Conversion utilities for mapping 2D design elements
 * to 3D world coordinates in the SPHERES Studio WorldView.
 *
 * Coordinate system:
 *   2D canvas: X right, Y down (in feet)
 *   3D world:  X right, Y up, Z forward (1 unit = 1 foot)
 *
 * The ground plane lives at Y = 0.
 */

import * as THREE from 'three';

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

/** A point in the 2D design canvas (feet). */
export interface Point2D {
  x: number;
  y: number;
}

/** A polygon described as an ordered ring of 2D points. */
export interface Polygon2D {
  points: Point2D[];
}

/** Bounding box in 2D canvas space. */
export interface Bounds2D {
  minX: number;
  maxX: number;
  minY: number;
  maxY: number;
  width: number;
  height: number;
  centerX: number;
  centerY: number;
}

/** Minimal representation of a design element coming from the editor. */
export interface DesignElement {
  id: string;
  type: string;
  x: number;         // canvas feet
  y: number;         // canvas feet
  width: number;     // feet
  height: number;    // feet (depth in 3D)
  rotation?: number; // degrees, clockwise in canvas
  color?: string;
  name?: string;
  isPermanent?: boolean;
  category?: string;
}

/** Catalog definition for a given element type. */
export interface ElementDef {
  type: string;
  defaultWidth: number;
  defaultHeight: number;
  category: string;
}

/** Props consumed by the 3D mesh components. */
export interface Element3DProps {
  id: string;
  meshType: string;
  position: [number, number, number];
  rotation: [number, number, number];
  scale: [number, number, number];
  color: string;
  name: string;
  isPermanent: boolean;
  category: string;
}

/** Time of day expressed as a normalised float 0..1 (0 = midnight, 0.5 = noon). */
export type TimeOfDay = number;

// ---------------------------------------------------------------------------
// Height table — base Y-extents for each mesh type (in feet)
// ---------------------------------------------------------------------------

const BASE_HEIGHTS: Record<string, number> = {
  stage_small: 3,
  stage_medium: 4,
  stage_large: 5,
  sound_equipment: 5,
  screening_wall: 12,
  bench: 3,
  picnic_table: 3,
  chair_cluster: 3,
  bleachers: 8,
  amphitheater_seating: 6,
  food_cart: 7,
  food_truck_space: 9,
  market_stall: 8,
  vendor_tent: 9,
  raised_bed: 2,
  tree_planting: 15,
  flower_garden: 1,
  native_meadow: 2,
  water_feature: 0.5,
  mural_wall: 14,
  sculpture_pad: 8,
  interactive_art: 6,
  art_installation: 10,
  play_structure: 10,
  basketball_half: 10,
  fitness_station: 8,
  sports_field: 0.1,
  pathway: 0.05,
  fencing: 6,
  lighting_pole: 16,
  power_hookup: 2,
  water_hookup: 2,
  shade_structure: 10,
  signage: 8,
};

// ---------------------------------------------------------------------------
// Coordinate conversions
// ---------------------------------------------------------------------------

/**
 * Convert a 2D canvas position (feet, Y-down) to a 3D world position.
 * The parcel centre is used as the origin so the scene is centred at (0, 0, 0).
 */
export function canvasTo3D(
  canvasX: number,
  canvasY: number,
  parcelCenter: Point2D,
): [number, number, number] {
  const x = canvasX - parcelCenter.x;
  const y = 0; // ground plane
  const z = canvasY - parcelCenter.y;
  return [x, y, z];
}

/**
 * Compute the bounding box of a set of 2D points.
 */
export function computeBounds(points: Point2D[]): Bounds2D {
  let minX = Infinity;
  let maxX = -Infinity;
  let minY = Infinity;
  let maxY = -Infinity;

  for (const p of points) {
    if (p.x < minX) minX = p.x;
    if (p.x > maxX) maxX = p.x;
    if (p.y < minY) minY = p.y;
    if (p.y > maxY) maxY = p.y;
  }

  const width = maxX - minX;
  const height = maxY - minY;
  return {
    minX,
    maxX,
    minY,
    maxY,
    width,
    height,
    centerX: minX + width / 2,
    centerY: minY + height / 2,
  };
}

// ---------------------------------------------------------------------------
// Design element -> 3D props
// ---------------------------------------------------------------------------

/**
 * Convert a single design element into the props needed by the 3D mesh system.
 */
export function designElementTo3DProps(
  element: DesignElement,
  elementDef: ElementDef | undefined,
  parcelCenter: Point2D,
): Element3DProps {
  const meshType = element.type;
  const baseHeight = BASE_HEIGHTS[meshType] ?? 4;

  // The element's centre in canvas feet
  const cx = element.x + element.width / 2;
  const cy = element.y + element.height / 2;

  const [px, , pz] = canvasTo3D(cx, cy, parcelCenter);

  // Y position: half the mesh height so it sits on the ground
  const py = baseHeight / 2;

  // Rotation — canvas uses clockwise degrees, Three.js uses radians about Y (counter-clockwise)
  const rotY = -((element.rotation ?? 0) * Math.PI) / 180;

  // Scale: the design element width/height define the XZ footprint relative
  // to the catalog default size. We normalise so that scale 1 = defaultWidth feet.
  const defWidth = elementDef?.defaultWidth ?? element.width;
  const defHeight = elementDef?.defaultHeight ?? element.height;
  const sx = element.width / defWidth;
  const sz = element.height / defHeight;

  return {
    id: element.id,
    meshType,
    position: [px, py, pz],
    rotation: [0, rotY, 0],
    scale: [sx, 1, sz],
    color: element.color ?? '#888888',
    name: element.name ?? meshType.replace(/_/g, ' '),
    isPermanent: element.isPermanent ?? false,
    category: element.category ?? elementDef?.category ?? 'other',
  };
}

// ---------------------------------------------------------------------------
// Parcel footprint -> THREE.Shape
// ---------------------------------------------------------------------------

/**
 * Convert a 2D polygon (in canvas feet) to a THREE.Shape suitable for
 * extrusion as the ground plane. The shape is centred at the parcel origin.
 */
export function parcelFootprintToShape(
  polygon: Polygon2D,
  parcelCenter: Point2D,
): THREE.Shape {
  const shape = new THREE.Shape();
  const pts = polygon.points;

  if (pts.length === 0) return shape;

  const first = pts[0];
  shape.moveTo(first.x - parcelCenter.x, -(first.y - parcelCenter.y));

  for (let i = 1; i < pts.length; i++) {
    const p = pts[i];
    shape.lineTo(p.x - parcelCenter.x, -(p.y - parcelCenter.y));
  }

  shape.closePath();
  return shape;
}

/**
 * Create a default rectangular parcel shape when no polygon data is available.
 */
export function defaultParcelShape(width: number, depth: number): THREE.Shape {
  const hw = width / 2;
  const hd = depth / 2;
  const shape = new THREE.Shape();
  shape.moveTo(-hw, -hd);
  shape.lineTo(hw, -hd);
  shape.lineTo(hw, hd);
  shape.lineTo(-hw, hd);
  shape.closePath();
  return shape;
}

// ---------------------------------------------------------------------------
// Camera helpers
// ---------------------------------------------------------------------------

/**
 * Calculate a good starting camera position that shows the whole parcel.
 * Returns both position and look-at target.
 */
export function calculateCameraStartPosition(
  parcelBounds: Bounds2D,
): { position: [number, number, number]; target: [number, number, number] } {
  const maxDim = Math.max(parcelBounds.width, parcelBounds.height);
  const altitude = Math.max(maxDim * 0.8, 30);
  const pullback = Math.max(maxDim * 0.5, 20);

  return {
    position: [-pullback, altitude, -pullback],
    target: [0, 0, 0],
  };
}

/**
 * Calculate a first-person starting position — standing at one corner looking in.
 */
export function calculateFirstPersonStart(
  parcelBounds: Bounds2D,
): { position: [number, number, number]; target: [number, number, number] } {
  const hw = parcelBounds.width / 2;
  const hd = parcelBounds.height / 2;

  return {
    position: [-hw + 5, 5.5, -hd + 5], // 5.5 ft eye height
    target: [0, 5.5, 0],
  };
}

// ---------------------------------------------------------------------------
// Sun position from time of day
// ---------------------------------------------------------------------------

/**
 * Compute a sun direction vector and color temperature from the normalised
 * time of day (0 = midnight, 0.25 = 6 AM, 0.5 = noon, 0.75 = 6 PM).
 */
export function sunFromTimeOfDay(time: TimeOfDay): {
  direction: [number, number, number];
  color: string;
  intensity: number;
  ambientIntensity: number;
  skyTurbidity: number;
  skyRayleigh: number;
} {
  // Solar angle: ranges from -PI (midnight) through 0 (6 AM rise) to PI/2 (noon) and back
  const solarAngle = (time - 0.25) * Math.PI * 2;
  const elevation = Math.sin(solarAngle);
  const azimuth = Math.cos(solarAngle);

  // Sun direction (normalised)
  const sunY = Math.max(elevation, -0.1);
  const sunX = azimuth;
  const sunZ = 0.3;

  // Color temperature shifts
  let color: string;
  let intensity: number;
  let ambientIntensity: number;
  let skyTurbidity: number;
  let skyRayleigh: number;

  if (time < 0.2 || time > 0.85) {
    // Night
    color = '#3344aa';
    intensity = 0.15;
    ambientIntensity = 0.08;
    skyTurbidity = 20;
    skyRayleigh = 0.5;
  } else if (time < 0.3) {
    // Dawn
    color = '#ffaa66';
    intensity = 0.6;
    ambientIntensity = 0.3;
    skyTurbidity = 8;
    skyRayleigh = 2;
  } else if (time < 0.4) {
    // Morning
    color = '#ffe0b0';
    intensity = 1.0;
    ambientIntensity = 0.5;
    skyTurbidity = 6;
    skyRayleigh = 1.5;
  } else if (time < 0.6) {
    // Midday
    color = '#fffff0';
    intensity = 1.4;
    ambientIntensity = 0.6;
    skyTurbidity = 4;
    skyRayleigh = 1;
  } else if (time < 0.75) {
    // Afternoon
    color = '#ffdd88';
    intensity = 1.1;
    ambientIntensity = 0.5;
    skyTurbidity = 5;
    skyRayleigh = 1.5;
  } else {
    // Evening / golden hour
    color = '#ff8844';
    intensity = 0.7;
    ambientIntensity = 0.3;
    skyTurbidity = 10;
    skyRayleigh = 3;
  }

  return {
    direction: [sunX * 100, sunY * 100, sunZ * 100],
    color,
    intensity,
    ambientIntensity,
    skyTurbidity,
    skyRayleigh,
  };
}

// ---------------------------------------------------------------------------
// Fog settings for modes
// ---------------------------------------------------------------------------

export function fogForMode(mode: 'before' | 'after' | 'permanence'): {
  color: string;
  near: number;
  far: number;
} {
  switch (mode) {
    case 'before':
      return { color: '#8a8a8a', near: 20, far: 120 };
    case 'after':
      return { color: '#d4e8f0', near: 60, far: 300 };
    case 'permanence':
      return { color: '#c0c8cc', near: 40, far: 200 };
  }
}

// ---------------------------------------------------------------------------
// Batch conversion
// ---------------------------------------------------------------------------

/**
 * Convert an entire design (array of elements) into 3D props, applying
 * filtering for the current view mode.
 */
export function designTo3DScene(
  elements: DesignElement[],
  elementDefs: Map<string, ElementDef>,
  parcelCenter: Point2D,
  mode: 'before' | 'after' | 'permanence',
): Element3DProps[] {
  if (mode === 'before') return []; // no elements in "before" view

  return elements
    .filter((el) => {
      if (mode === 'permanence') return el.isPermanent;
      return true; // 'after' shows everything
    })
    .map((el) => designElementTo3DProps(el, elementDefs.get(el.type), parcelCenter));
}
