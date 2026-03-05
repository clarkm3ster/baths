/**
 * SPHERES Studio — Canvas State Management Hook
 *
 * Zustand store that manages the entire design canvas state:
 * placed elements, selection, grid/zoom/pan, undo/redo history,
 * parcel boundary, and layer visibility.
 */

import { create } from "zustand";
import type {
  DesignElement,
  ElementDefinition,
  Point,
} from "../utils/canvasRenderer";
import { snapToGrid } from "../utils/canvasRenderer";

// ---------------------------------------------------------------------------
// History entry — captures a snapshot of the mutable canvas state
// ---------------------------------------------------------------------------

interface HistoryEntry {
  elements: DesignElement[];
  selectedIds: string[];
}

// ---------------------------------------------------------------------------
// Layer visibility
// ---------------------------------------------------------------------------

export interface LayerVisibility {
  temporary: boolean;
  permanent: boolean;
  infrastructure: boolean;
}

// ---------------------------------------------------------------------------
// Store shape
// ---------------------------------------------------------------------------

export interface CanvasState {
  // ---- Elements -----------------------------------------------------------
  elements: DesignElement[];
  elementDefs: Map<string, ElementDefinition>;
  setElementDefs: (defs: ElementDefinition[]) => void;

  // ---- Selection ----------------------------------------------------------
  selectedIds: string[];
  selectElement: (id: string, additive?: boolean) => void;
  multiSelect: (ids: string[]) => void;
  deselectAll: () => void;

  // ---- Parcel boundary ----------------------------------------------------
  parcelFootprint: Point[];
  setParcelFootprint: (polygon: Point[]) => void;

  // ---- Grid / Zoom / Pan --------------------------------------------------
  gridEnabled: boolean;
  gridSize: number;
  zoom: number;
  panOffset: Point;
  toggleGrid: () => void;
  setGridSize: (size: number) => void;
  setZoom: (zoom: number) => void;
  zoomBy: (delta: number, pivotScreen?: Point) => void;
  setPanOffset: (offset: Point) => void;
  panBy: (dx: number, dy: number) => void;

  // ---- Layer visibility ---------------------------------------------------
  layerVisibility: LayerVisibility;
  toggleLayerVisibility: (layer: keyof LayerVisibility) => void;

  // ---- Element mutations (all push history) --------------------------------
  addElement: (element: DesignElement) => void;
  removeElements: (ids: string[]) => void;
  moveElement: (id: string, x: number, y: number) => void;
  moveElements: (ids: string[], dx: number, dy: number) => void;
  rotateElement: (id: string, angle: number) => void;
  scaleElement: (id: string, scale: number) => void;
  updateElement: (id: string, patch: Partial<DesignElement>) => void;
  setElements: (elements: DesignElement[]) => void;

  // ---- Undo / Redo --------------------------------------------------------
  undo: () => void;
  redo: () => void;
  canUndo: boolean;
  canRedo: boolean;

  // ---- Design metadata (for save/load) ------------------------------------
  designId: string | null;
  designName: string;
  setDesignId: (id: string | null) => void;
  setDesignName: (name: string) => void;
}

// ---------------------------------------------------------------------------
// History helpers
// ---------------------------------------------------------------------------

const MAX_HISTORY = 100;

function snapshot(elements: DesignElement[], selectedIds: string[]): HistoryEntry {
  return {
    elements: elements.map((e) => ({ ...e })),
    selectedIds: [...selectedIds],
  };
}

// ---------------------------------------------------------------------------
// Store
// ---------------------------------------------------------------------------

export const useCanvas = create<CanvasState>()((set, get) => {
  let _undoStack: HistoryEntry[] = [];
  let _redoStack: HistoryEntry[] = [];

  /** Push current state to undo stack (call before mutation). */
  function pushUndo() {
    const { elements, selectedIds } = get();
    _undoStack.push(snapshot(elements, selectedIds));
    if (_undoStack.length > MAX_HISTORY) _undoStack.shift();
    _redoStack = [];
    set({ canUndo: true, canRedo: false });
  }

  return {
    // ---- Elements ---------------------------------------------------------
    elements: [],
    elementDefs: new Map(),
    setElementDefs: (defs) =>
      set({
        elementDefs: new Map(defs.map((d) => [d.id, d])),
      }),

    // ---- Selection --------------------------------------------------------
    selectedIds: [],
    selectElement: (id, additive = false) =>
      set((s) => {
        if (additive) {
          const already = s.selectedIds.includes(id);
          return {
            selectedIds: already
              ? s.selectedIds.filter((sid) => sid !== id)
              : [...s.selectedIds, id],
          };
        }
        return { selectedIds: [id] };
      }),
    multiSelect: (ids) => set({ selectedIds: ids }),
    deselectAll: () => set({ selectedIds: [] }),

    // ---- Parcel boundary --------------------------------------------------
    parcelFootprint: [],
    setParcelFootprint: (polygon) => set({ parcelFootprint: polygon }),

    // ---- Grid / Zoom / Pan ------------------------------------------------
    gridEnabled: true,
    gridSize: 5, // 5-foot grid
    zoom: 4, // 4 px per foot
    panOffset: { x: 60, y: 60 },
    toggleGrid: () => set((s) => ({ gridEnabled: !s.gridEnabled })),
    setGridSize: (size) => set({ gridSize: size }),
    setZoom: (zoom) => set({ zoom: Math.max(0.5, Math.min(40, zoom)) }),
    zoomBy: (delta, pivotScreen) => {
      const state = get();
      const oldZoom = state.zoom;
      const newZoom = Math.max(0.5, Math.min(40, oldZoom * (1 + delta)));
      if (pivotScreen) {
        // Keep the canvas point under the cursor stationary
        const canvasX = (pivotScreen.x - state.panOffset.x) / oldZoom;
        const canvasY = (pivotScreen.y - state.panOffset.y) / oldZoom;
        set({
          zoom: newZoom,
          panOffset: {
            x: pivotScreen.x - canvasX * newZoom,
            y: pivotScreen.y - canvasY * newZoom,
          },
        });
      } else {
        set({ zoom: newZoom });
      }
    },
    setPanOffset: (offset) => set({ panOffset: offset }),
    panBy: (dx, dy) =>
      set((s) => ({
        panOffset: { x: s.panOffset.x + dx, y: s.panOffset.y + dy },
      })),

    // ---- Layer visibility -------------------------------------------------
    layerVisibility: { temporary: true, permanent: true, infrastructure: true },
    toggleLayerVisibility: (layer) =>
      set((s) => ({
        layerVisibility: {
          ...s.layerVisibility,
          [layer]: !s.layerVisibility[layer],
        },
      })),

    // ---- Element mutations ------------------------------------------------
    addElement: (element) => {
      pushUndo();
      set((s) => ({
        elements: [...s.elements, element],
        selectedIds: [element.instance_id],
      }));
    },
    removeElements: (ids) => {
      pushUndo();
      set((s) => ({
        elements: s.elements.filter((e) => !ids.includes(e.instance_id)),
        selectedIds: s.selectedIds.filter((sid) => !ids.includes(sid)),
      }));
    },
    moveElement: (id, x, y) => {
      const state = get();
      const el = state.elements.find((e) => e.instance_id === id);
      if (!el || el.locked) return;
      pushUndo();
      const finalX = state.gridEnabled ? snapToGrid(x, state.gridSize) : x;
      const finalY = state.gridEnabled ? snapToGrid(y, state.gridSize) : y;
      set((s) => ({
        elements: s.elements.map((e) =>
          e.instance_id === id ? { ...e, x: finalX, y: finalY } : e,
        ),
      }));
    },
    moveElements: (ids, dx, dy) => {
      pushUndo();
      const state = get();
      set({
        elements: state.elements.map((e) => {
          if (!ids.includes(e.instance_id) || e.locked) return e;
          const nx = e.x + dx;
          const ny = e.y + dy;
          return {
            ...e,
            x: state.gridEnabled ? snapToGrid(nx, state.gridSize) : nx,
            y: state.gridEnabled ? snapToGrid(ny, state.gridSize) : ny,
          };
        }),
      });
    },
    rotateElement: (id, angle) => {
      const el = get().elements.find((e) => e.instance_id === id);
      if (!el || el.locked) return;
      pushUndo();
      set((s) => ({
        elements: s.elements.map((e) =>
          e.instance_id === id
            ? { ...e, rotation: (e.rotation + angle + 360) % 360 }
            : e,
        ),
      }));
    },
    scaleElement: (id, scale) => {
      const el = get().elements.find((e) => e.instance_id === id);
      if (!el || el.locked) return;
      pushUndo();
      set((s) => ({
        elements: s.elements.map((e) =>
          e.instance_id === id
            ? { ...e, scale: Math.max(0.25, Math.min(4, scale)) }
            : e,
        ),
      }));
    },
    updateElement: (id, patch) => {
      pushUndo();
      set((s) => ({
        elements: s.elements.map((e) =>
          e.instance_id === id ? { ...e, ...patch } : e,
        ),
      }));
    },
    setElements: (elements) => {
      pushUndo();
      set({ elements: elements.map((e) => ({ ...e })) });
    },

    // ---- Undo / Redo ------------------------------------------------------
    canUndo: false,
    canRedo: false,
    undo: () => {
      if (_undoStack.length === 0) return;
      const current = snapshot(get().elements, get().selectedIds);
      _redoStack.push(current);
      const prev = _undoStack.pop()!;
      set({
        elements: prev.elements,
        selectedIds: prev.selectedIds,
        canUndo: _undoStack.length > 0,
        canRedo: true,
      });
    },
    redo: () => {
      if (_redoStack.length === 0) return;
      const current = snapshot(get().elements, get().selectedIds);
      _undoStack.push(current);
      const next = _redoStack.pop()!;
      set({
        elements: next.elements,
        selectedIds: next.selectedIds,
        canUndo: true,
        canRedo: _redoStack.length > 0,
      });
    },

    // ---- Design metadata --------------------------------------------------
    designId: null,
    designName: "Untitled Design",
    setDesignId: (id) => set({ designId: id }),
    setDesignName: (name) => set({ designName: name }),
  };
});
