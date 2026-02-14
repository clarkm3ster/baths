/**
 * SPHERES Studio — Canvas Rendering Utilities
 *
 * Pure functions for drawing the design canvas: grid, parcel boundary,
 * elements, selection overlays, and coordinate transforms.  All drawing
 * operates on a CanvasRenderingContext2D and is zoom/pan aware.
 */

// ---------------------------------------------------------------------------
// Types shared with the rest of the frontend
// ---------------------------------------------------------------------------

export interface Point {
  x: number;
  y: number;
}

export interface CostRange {
  low: number;
  high: number;
}

export interface ElementDefinition {
  id: string;
  name: string;
  category: string;
  icon: string;
  footprint_width: number;
  footprint_height: number;
  cost_estimate: CostRange;
  permit_requirements: string[];
  permanence_potential: number;
  permanence_category: string;
  layer: "temporary" | "permanent" | "infrastructure";
  color: string;
  description: string;
}

export interface DesignElement {
  instance_id: string;
  element_id: string;
  x: number;
  y: number;
  rotation: number;
  scale: number;
  layer: "temporary" | "permanent" | "infrastructure";
  locked: boolean;
  custom_notes: string;
}

export interface ViewTransform {
  zoom: number;
  offsetX: number;
  offsetY: number;
}

// ---------------------------------------------------------------------------
// Coordinate transforms
// ---------------------------------------------------------------------------

/** Convert a screen-space pixel position to canvas (design) coordinates. */
export function screenToCanvas(
  screenX: number,
  screenY: number,
  zoom: number,
  offset: Point,
): Point {
  return {
    x: (screenX - offset.x) / zoom,
    y: (screenY - offset.y) / zoom,
  };
}

/** Convert canvas (design) coordinates to screen-space pixels. */
export function canvasToScreen(
  canvasX: number,
  canvasY: number,
  zoom: number,
  offset: Point,
): Point {
  return {
    x: canvasX * zoom + offset.x,
    y: canvasY * zoom + offset.y,
  };
}

// ---------------------------------------------------------------------------
// Grid drawing
// ---------------------------------------------------------------------------

/**
 * Draw an infinite-feeling dot grid that adjusts density with zoom level.
 */
export function drawGrid(
  ctx: CanvasRenderingContext2D,
  gridSize: number,
  zoom: number,
  offset: Point,
  canvasWidth: number,
  canvasHeight: number,
): void {
  // Determine effective grid spacing in screen pixels
  let step = gridSize;
  while (step * zoom < 12) step *= 2; // avoid cramming when zoomed out
  while (step * zoom > 120) step /= 2;

  const screenStep = step * zoom;

  // Start positions (snapped to grid)
  const startX = offset.x % screenStep;
  const startY = offset.y % screenStep;

  ctx.save();
  ctx.fillStyle = "rgba(148, 163, 184, 0.35)"; // slate-400 @ 35%

  for (let sx = startX; sx < canvasWidth; sx += screenStep) {
    for (let sy = startY; sy < canvasHeight; sy += screenStep) {
      ctx.beginPath();
      ctx.arc(sx, sy, 1.2, 0, Math.PI * 2);
      ctx.fill();
    }
  }

  ctx.restore();
}

// ---------------------------------------------------------------------------
// Parcel boundary
// ---------------------------------------------------------------------------

/**
 * Draw the parcel polygon outline.  Fills with a very faint tint so the
 * user can see the buildable area.
 */
export function drawParcelBoundary(
  ctx: CanvasRenderingContext2D,
  polygon: Point[],
  zoom: number,
  offset: Point,
): void {
  if (polygon.length < 3) return;

  ctx.save();

  ctx.beginPath();
  const first = canvasToScreen(polygon[0].x, polygon[0].y, zoom, offset);
  ctx.moveTo(first.x, first.y);
  for (let i = 1; i < polygon.length; i++) {
    const p = canvasToScreen(polygon[i].x, polygon[i].y, zoom, offset);
    ctx.lineTo(p.x, p.y);
  }
  ctx.closePath();

  // Fill
  ctx.fillStyle = "rgba(59, 130, 246, 0.04)"; // blue-500 @ 4%
  ctx.fill();

  // Stroke
  ctx.strokeStyle = "rgba(59, 130, 246, 0.5)";
  ctx.lineWidth = 2;
  ctx.setLineDash([8, 4]);
  ctx.stroke();

  ctx.restore();
}

// ---------------------------------------------------------------------------
// Element drawing
// ---------------------------------------------------------------------------

/**
 * Draw a single design element as a coloured rectangle with its name label.
 * When selected, draws resize handles and a highlight border.
 */
export function drawElement(
  ctx: CanvasRenderingContext2D,
  element: DesignElement,
  elementDef: ElementDefinition,
  isSelected: boolean,
  zoom: number,
  offset: Point,
): void {
  const screenPos = canvasToScreen(element.x, element.y, zoom, offset);
  const w = elementDef.footprint_width * element.scale * zoom;
  const h = elementDef.footprint_height * element.scale * zoom;

  ctx.save();

  // Translate to element centre, then rotate
  const cx = screenPos.x + w / 2;
  const cy = screenPos.y + h / 2;
  ctx.translate(cx, cy);
  ctx.rotate((element.rotation * Math.PI) / 180);
  ctx.translate(-w / 2, -h / 2);

  // Body fill
  ctx.fillStyle = elementDef.color + "CC"; // ~80% opacity
  ctx.strokeStyle = elementDef.color;
  ctx.lineWidth = 1.5;

  const radius = Math.min(4, w * 0.08, h * 0.08);
  roundRect(ctx, 0, 0, w, h, radius);
  ctx.fill();
  ctx.stroke();

  // Layer indicator stripe along the top
  const stripeColor = layerStripeColor(element.layer);
  ctx.fillStyle = stripeColor;
  const stripeH = Math.max(3, h * 0.06);
  roundRectTop(ctx, 0, 0, w, stripeH, radius);
  ctx.fill();

  // Locked indicator
  if (element.locked) {
    ctx.fillStyle = "rgba(0,0,0,0.35)";
    ctx.fillRect(0, 0, w, h);
  }

  // Label
  const fontSize = Math.max(9, Math.min(14, w * 0.12));
  ctx.font = `600 ${fontSize}px Inter, system-ui, sans-serif`;
  ctx.fillStyle = "#FFFFFF";
  ctx.textAlign = "center";
  ctx.textBaseline = "middle";
  const label = truncateLabel(elementDef.name, ctx, w * 0.85);
  ctx.fillText(label, w / 2, h / 2);

  // Dimensions text (small)
  if (w > 50 && h > 36) {
    const dimFontSize = Math.max(7, fontSize * 0.65);
    ctx.font = `400 ${dimFontSize}px Inter, system-ui, sans-serif`;
    ctx.fillStyle = "rgba(255,255,255,0.7)";
    const dimText = `${elementDef.footprint_width}\u00d7${elementDef.footprint_height} ft`;
    ctx.fillText(dimText, w / 2, h / 2 + fontSize * 0.8);
  }

  ctx.restore();

  // Selection overlay
  if (isSelected) {
    drawSelectionHighlight(ctx, screenPos, w, h, element.rotation, zoom);
  }
}

function layerStripeColor(layer: string): string {
  switch (layer) {
    case "permanent":
      return "rgba(34,197,94,0.7)"; // green
    case "infrastructure":
      return "rgba(148,163,184,0.7)"; // slate
    default:
      return "rgba(251,191,36,0.7)"; // amber
  }
}

function truncateLabel(
  text: string,
  ctx: CanvasRenderingContext2D,
  maxWidth: number,
): string {
  if (ctx.measureText(text).width <= maxWidth) return text;
  let truncated = text;
  while (truncated.length > 1 && ctx.measureText(truncated + "\u2026").width > maxWidth) {
    truncated = truncated.slice(0, -1);
  }
  return truncated + "\u2026";
}

function drawSelectionHighlight(
  ctx: CanvasRenderingContext2D,
  screenPos: Point,
  w: number,
  h: number,
  rotation: number,
  _zoom: number,
): void {
  ctx.save();

  const cx = screenPos.x + w / 2;
  const cy = screenPos.y + h / 2;
  ctx.translate(cx, cy);
  ctx.rotate((rotation * Math.PI) / 180);
  ctx.translate(-w / 2, -h / 2);

  // Highlight border
  ctx.strokeStyle = "#3B82F6";
  ctx.lineWidth = 2;
  ctx.setLineDash([]);
  const pad = 3;
  ctx.strokeRect(-pad, -pad, w + pad * 2, h + pad * 2);

  // Corner handles
  const handleSize = 7;
  ctx.fillStyle = "#FFFFFF";
  ctx.strokeStyle = "#3B82F6";
  ctx.lineWidth = 1.5;
  const corners = [
    [-pad, -pad],
    [w + pad, -pad],
    [-pad, h + pad],
    [w + pad, h + pad],
  ];
  for (const [hx, hy] of corners) {
    ctx.fillRect(hx - handleSize / 2, hy - handleSize / 2, handleSize, handleSize);
    ctx.strokeRect(hx - handleSize / 2, hy - handleSize / 2, handleSize, handleSize);
  }

  // Edge-midpoint handles
  const midpoints = [
    [w / 2, -pad],
    [w / 2, h + pad],
    [-pad, h / 2],
    [w + pad, h / 2],
  ];
  for (const [mx, my] of midpoints) {
    ctx.fillRect(mx - handleSize / 2, my - handleSize / 2, handleSize, handleSize);
    ctx.strokeRect(mx - handleSize / 2, my - handleSize / 2, handleSize, handleSize);
  }

  ctx.restore();
}

// ---------------------------------------------------------------------------
// Selection box (marquee)
// ---------------------------------------------------------------------------

/**
 * Draw a translucent blue rectangle for multi-select dragging.
 */
export function drawSelectionBox(
  ctx: CanvasRenderingContext2D,
  start: Point,
  end: Point,
): void {
  const x = Math.min(start.x, end.x);
  const y = Math.min(start.y, end.y);
  const w = Math.abs(end.x - start.x);
  const h = Math.abs(end.y - start.y);

  ctx.save();
  ctx.fillStyle = "rgba(59, 130, 246, 0.1)";
  ctx.strokeStyle = "rgba(59, 130, 246, 0.6)";
  ctx.lineWidth = 1;
  ctx.setLineDash([4, 3]);
  ctx.fillRect(x, y, w, h);
  ctx.strokeRect(x, y, w, h);
  ctx.restore();
}

// ---------------------------------------------------------------------------
// Hit testing
// ---------------------------------------------------------------------------

/**
 * Determine which element (if any) lies under the given screen coordinates.
 * Returns the topmost (last in array) match, or null.
 *
 * Uses axis-aligned bounding-box testing with rotation taken into account
 * by transforming the test point into the element's local coordinate frame.
 */
export function hitTest(
  screenX: number,
  screenY: number,
  elements: DesignElement[],
  elementDefs: Map<string, ElementDefinition>,
  zoom: number,
  offset: Point,
): DesignElement | null {
  // Iterate in reverse so topmost (last-drawn) wins
  for (let i = elements.length - 1; i >= 0; i--) {
    const el = elements[i];
    const def = elementDefs.get(el.element_id);
    if (!def) continue;

    const sp = canvasToScreen(el.x, el.y, zoom, offset);
    const w = def.footprint_width * el.scale * zoom;
    const h = def.footprint_height * el.scale * zoom;

    // Centre of the element in screen space
    const cx = sp.x + w / 2;
    const cy = sp.y + h / 2;

    // Rotate the test point into local space
    const angle = (-el.rotation * Math.PI) / 180;
    const dx = screenX - cx;
    const dy = screenY - cy;
    const localX = dx * Math.cos(angle) - dy * Math.sin(angle);
    const localY = dx * Math.sin(angle) + dy * Math.cos(angle);

    if (
      localX >= -w / 2 &&
      localX <= w / 2 &&
      localY >= -h / 2 &&
      localY <= h / 2
    ) {
      return el;
    }
  }

  return null;
}

/**
 * Find all elements whose bounding boxes intersect a screen-space rectangle.
 * Used for marquee / drag-select.
 */
export function hitTestRect(
  rectStart: Point,
  rectEnd: Point,
  elements: DesignElement[],
  elementDefs: Map<string, ElementDefinition>,
  zoom: number,
  offset: Point,
): DesignElement[] {
  const rx1 = Math.min(rectStart.x, rectEnd.x);
  const ry1 = Math.min(rectStart.y, rectEnd.y);
  const rx2 = Math.max(rectStart.x, rectEnd.x);
  const ry2 = Math.max(rectStart.y, rectEnd.y);

  const hits: DesignElement[] = [];
  for (const el of elements) {
    const def = elementDefs.get(el.element_id);
    if (!def) continue;

    const sp = canvasToScreen(el.x, el.y, zoom, offset);
    const w = def.footprint_width * el.scale * zoom;
    const h = def.footprint_height * el.scale * zoom;

    // AABB overlap (ignoring rotation for marquee)
    if (sp.x + w >= rx1 && sp.x <= rx2 && sp.y + h >= ry1 && sp.y <= ry2) {
      hits.push(el);
    }
  }
  return hits;
}

// ---------------------------------------------------------------------------
// Boundary check
// ---------------------------------------------------------------------------

/**
 * Test whether an element's bounding box is fully inside the parcel polygon.
 * Uses a simple point-in-polygon ray-cast for each corner.
 */
export function isInsideParcel(
  element: DesignElement,
  elementDef: ElementDefinition,
  parcel: Point[],
): boolean {
  if (parcel.length < 3) return true; // no boundary defined

  const w = elementDef.footprint_width * element.scale;
  const h = elementDef.footprint_height * element.scale;
  const corners: Point[] = [
    { x: element.x, y: element.y },
    { x: element.x + w, y: element.y },
    { x: element.x + w, y: element.y + h },
    { x: element.x, y: element.y + h },
  ];

  return corners.every((c) => pointInPolygon(c, parcel));
}

function pointInPolygon(point: Point, polygon: Point[]): boolean {
  let inside = false;
  for (let i = 0, j = polygon.length - 1; i < polygon.length; j = i++) {
    const xi = polygon[i].x,
      yi = polygon[i].y;
    const xj = polygon[j].x,
      yj = polygon[j].y;
    const intersect =
      yi > point.y !== yj > point.y &&
      point.x < ((xj - xi) * (point.y - yi)) / (yj - yi) + xi;
    if (intersect) inside = !inside;
  }
  return inside;
}

// ---------------------------------------------------------------------------
// Snap to grid helper
// ---------------------------------------------------------------------------

export function snapToGrid(value: number, gridSize: number): number {
  return Math.round(value / gridSize) * gridSize;
}

// ---------------------------------------------------------------------------
// Rounded-rect helpers (not using ctx.roundRect for Safari < 16 compat)
// ---------------------------------------------------------------------------

function roundRect(
  ctx: CanvasRenderingContext2D,
  x: number,
  y: number,
  w: number,
  h: number,
  r: number,
): void {
  ctx.beginPath();
  ctx.moveTo(x + r, y);
  ctx.lineTo(x + w - r, y);
  ctx.quadraticCurveTo(x + w, y, x + w, y + r);
  ctx.lineTo(x + w, y + h - r);
  ctx.quadraticCurveTo(x + w, y + h, x + w - r, y + h);
  ctx.lineTo(x + r, y + h);
  ctx.quadraticCurveTo(x, y + h, x, y + h - r);
  ctx.lineTo(x, y + r);
  ctx.quadraticCurveTo(x, y, x + r, y);
  ctx.closePath();
}

function roundRectTop(
  ctx: CanvasRenderingContext2D,
  x: number,
  y: number,
  w: number,
  h: number,
  r: number,
): void {
  ctx.beginPath();
  ctx.moveTo(x + r, y);
  ctx.lineTo(x + w - r, y);
  ctx.quadraticCurveTo(x + w, y, x + w, y + r);
  ctx.lineTo(x + w, y + h);
  ctx.lineTo(x, y + h);
  ctx.lineTo(x, y + r);
  ctx.quadraticCurveTo(x, y, x + r, y);
  ctx.closePath();
}
