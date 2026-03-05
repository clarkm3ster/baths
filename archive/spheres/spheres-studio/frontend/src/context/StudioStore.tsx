/**
 * SPHERES Studio — Zustand Store
 *
 * Central state management for the activation design canvas.
 * Handles design document, selection, viewport, undo/redo, and UI panels.
 */

import { create } from 'zustand';

// ---------------------------------------------------------------------------
// Type definitions
// ---------------------------------------------------------------------------

export interface Point {
  x: number;
  y: number;
}

export interface DesignElement {
  instanceId: string;
  elementId: string;
  x: number;
  y: number;
  rotation: number;
  scale: number;
  layer: 'temporary' | 'permanent' | 'infrastructure';
  locked: boolean;
  customNotes: string;
}

export interface Design {
  id: string;
  name: string;
  description: string;
  parcelId: string | null;
  parcelFootprint: Point[];
  elements: DesignElement[];
  createdAt: string;
  updatedAt: string;
  authorId: string | null;
  isPublic: boolean;
  tags: string[];
  thumbnailUrl: string | null;
}

export type ActiveTool = 'select' | 'pan' | 'place';
export type ViewMode = 'canvas' | 'timeline' | 'budget';

interface HistoryEntry {
  elements: DesignElement[];
  name: string;
}

// ---------------------------------------------------------------------------
// Store interface
// ---------------------------------------------------------------------------

export interface StudioState {
  // Design document
  design: Design;
  isDirty: boolean;

  // Selection
  selectedElementIds: string[];

  // Active tool
  activeTool: ActiveTool;
  placingElement: string | null;

  // Viewport
  gridEnabled: boolean;
  snapToGrid: boolean;
  gridSize: number;
  zoom: number;
  panOffset: Point;

  // UI panels
  sidebarOpen: boolean;
  detailPanelOpen: boolean;
  viewMode: ViewMode;

  // Undo / redo
  history: HistoryEntry[];
  historyIndex: number;

  // ── Design actions ──────────────────────────────────────────────────
  setDesign: (design: Design) => void;
  setDesignName: (name: string) => void;
  setDesignDescription: (description: string) => void;
  setParcel: (parcelId: string, footprint: Point[]) => void;
  clearParcel: () => void;
  markClean: () => void;

  // ── Element CRUD ────────────────────────────────────────────────────
  addElement: (element: DesignElement) => void;
  removeElements: (ids: string[]) => void;
  updateElement: (id: string, patch: Partial<DesignElement>) => void;
  duplicateElements: (ids: string[]) => void;
  moveElements: (ids: string[], dx: number, dy: number) => void;
  rotateElements: (ids: string[], degrees: number) => void;
  lockElements: (ids: string[], locked: boolean) => void;

  // ── Selection ───────────────────────────────────────────────────────
  selectElements: (ids: string[], append?: boolean) => void;
  selectAll: () => void;
  deselectAll: () => void;

  // ── Tools ───────────────────────────────────────────────────────────
  setActiveTool: (tool: ActiveTool) => void;
  startPlacing: (elementId: string) => void;
  cancelPlacing: () => void;

  // ── Viewport ────────────────────────────────────────────────────────
  setZoom: (zoom: number) => void;
  setPan: (offset: Point) => void;
  toggleGrid: () => void;
  toggleSnap: () => void;
  resetView: () => void;

  // ── Panels ──────────────────────────────────────────────────────────
  toggleSidebar: () => void;
  toggleDetailPanel: () => void;
  setViewMode: (mode: ViewMode) => void;

  // ── History ─────────────────────────────────────────────────────────
  pushHistory: (label?: string) => void;
  undo: () => void;
  redo: () => void;
  canUndo: () => boolean;
  canRedo: () => boolean;
}

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

function generateId(): string {
  return Math.random().toString(36).substring(2, 14);
}

function createEmptyDesign(): Design {
  return {
    id: generateId(),
    name: 'Untitled Design',
    description: '',
    parcelId: null,
    parcelFootprint: [],
    elements: [],
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString(),
    authorId: null,
    isPublic: false,
    tags: [],
    thumbnailUrl: null,
  };
}

function cloneElements(elements: DesignElement[]): DesignElement[] {
  return elements.map((el) => ({ ...el }));
}

const MAX_HISTORY = 100;

// ---------------------------------------------------------------------------
// Store
// ---------------------------------------------------------------------------

export const useStudioStore = create<StudioState>((set, get) => ({
  // ── Initial state ─────────────────────────────────────────────────────
  design: createEmptyDesign(),
  isDirty: false,

  selectedElementIds: [],
  activeTool: 'select',
  placingElement: null,

  gridEnabled: true,
  snapToGrid: true,
  gridSize: 1,
  zoom: 1,
  panOffset: { x: 0, y: 0 },

  sidebarOpen: window.innerWidth > 768,
  detailPanelOpen: window.innerWidth > 768,
  viewMode: 'canvas',

  history: [],
  historyIndex: -1,

  // ── Design actions ────────────────────────────────────────────────────
  setDesign: (design) =>
    set({
      design,
      isDirty: false,
      selectedElementIds: [],
      history: [{ elements: cloneElements(design.elements), name: 'Load design' }],
      historyIndex: 0,
    }),

  setDesignName: (name) =>
    set((s) => ({
      design: { ...s.design, name, updatedAt: new Date().toISOString() },
      isDirty: true,
    })),

  setDesignDescription: (description) =>
    set((s) => ({
      design: { ...s.design, description, updatedAt: new Date().toISOString() },
      isDirty: true,
    })),

  setParcel: (parcelId, footprint) =>
    set((s) => ({
      design: {
        ...s.design,
        parcelId,
        parcelFootprint: footprint,
        updatedAt: new Date().toISOString(),
      },
      isDirty: true,
    })),

  clearParcel: () =>
    set((s) => ({
      design: {
        ...s.design,
        parcelId: null,
        parcelFootprint: [],
        updatedAt: new Date().toISOString(),
      },
      isDirty: true,
    })),

  markClean: () => set({ isDirty: false }),

  // ── Element CRUD ──────────────────────────────────────────────────────
  addElement: (element) => {
    const state = get();
    state.pushHistory('Add element');
    set((s) => ({
      design: {
        ...s.design,
        elements: [...s.design.elements, element],
        updatedAt: new Date().toISOString(),
      },
      isDirty: true,
      selectedElementIds: [element.instanceId],
    }));
  },

  removeElements: (ids) => {
    const state = get();
    state.pushHistory('Remove elements');
    set((s) => ({
      design: {
        ...s.design,
        elements: s.design.elements.filter((el) => !ids.includes(el.instanceId)),
        updatedAt: new Date().toISOString(),
      },
      isDirty: true,
      selectedElementIds: s.selectedElementIds.filter((id) => !ids.includes(id)),
    }));
  },

  updateElement: (id, patch) => {
    set((s) => ({
      design: {
        ...s.design,
        elements: s.design.elements.map((el) =>
          el.instanceId === id ? { ...el, ...patch } : el
        ),
        updatedAt: new Date().toISOString(),
      },
      isDirty: true,
    }));
  },

  duplicateElements: (ids) => {
    const state = get();
    state.pushHistory('Duplicate elements');
    const newElements: DesignElement[] = [];
    const newIds: string[] = [];

    for (const id of ids) {
      const original = state.design.elements.find((el) => el.instanceId === id);
      if (original) {
        const newId = generateId();
        newElements.push({
          ...original,
          instanceId: newId,
          x: original.x + 2,
          y: original.y + 2,
          locked: false,
        });
        newIds.push(newId);
      }
    }

    set((s) => ({
      design: {
        ...s.design,
        elements: [...s.design.elements, ...newElements],
        updatedAt: new Date().toISOString(),
      },
      isDirty: true,
      selectedElementIds: newIds,
    }));
  },

  moveElements: (ids, dx, dy) => {
    set((s) => ({
      design: {
        ...s.design,
        elements: s.design.elements.map((el) =>
          ids.includes(el.instanceId) && !el.locked
            ? { ...el, x: el.x + dx, y: el.y + dy }
            : el
        ),
        updatedAt: new Date().toISOString(),
      },
      isDirty: true,
    }));
  },

  rotateElements: (ids, degrees) => {
    set((s) => ({
      design: {
        ...s.design,
        elements: s.design.elements.map((el) =>
          ids.includes(el.instanceId) && !el.locked
            ? { ...el, rotation: (el.rotation + degrees) % 360 }
            : el
        ),
        updatedAt: new Date().toISOString(),
      },
      isDirty: true,
    }));
  },

  lockElements: (ids, locked) => {
    set((s) => ({
      design: {
        ...s.design,
        elements: s.design.elements.map((el) =>
          ids.includes(el.instanceId) ? { ...el, locked } : el
        ),
        updatedAt: new Date().toISOString(),
      },
      isDirty: true,
    }));
  },

  // ── Selection ─────────────────────────────────────────────────────────
  selectElements: (ids, append = false) =>
    set((s) => ({
      selectedElementIds: append
        ? [...new Set([...s.selectedElementIds, ...ids])]
        : ids,
      detailPanelOpen: ids.length > 0 ? true : s.detailPanelOpen,
    })),

  selectAll: () =>
    set((s) => ({
      selectedElementIds: s.design.elements.map((el) => el.instanceId),
    })),

  deselectAll: () => set({ selectedElementIds: [] }),

  // ── Tools ─────────────────────────────────────────────────────────────
  setActiveTool: (tool) =>
    set({ activeTool: tool, placingElement: tool === 'place' ? get().placingElement : null }),

  startPlacing: (elementId) =>
    set({ activeTool: 'place', placingElement: elementId }),

  cancelPlacing: () =>
    set({ activeTool: 'select', placingElement: null }),

  // ── Viewport ──────────────────────────────────────────────────────────
  setZoom: (zoom) => set({ zoom: Math.max(0.1, Math.min(5, zoom)) }),

  setPan: (offset) => set({ panOffset: offset }),

  toggleGrid: () => set((s) => ({ gridEnabled: !s.gridEnabled })),

  toggleSnap: () => set((s) => ({ snapToGrid: !s.snapToGrid })),

  resetView: () => set({ zoom: 1, panOffset: { x: 0, y: 0 } }),

  // ── Panels ────────────────────────────────────────────────────────────
  toggleSidebar: () => set((s) => ({ sidebarOpen: !s.sidebarOpen })),

  toggleDetailPanel: () => set((s) => ({ detailPanelOpen: !s.detailPanelOpen })),

  setViewMode: (mode) => set({ viewMode: mode }),

  // ── History (undo / redo) ─────────────────────────────────────────────
  pushHistory: (label = 'Edit') => {
    const state = get();
    const snapshot: HistoryEntry = {
      elements: cloneElements(state.design.elements),
      name: label,
    };

    // Trim future entries if we diverged
    const trimmed = state.history.slice(0, state.historyIndex + 1);
    const updated = [...trimmed, snapshot];

    // Cap history length
    if (updated.length > MAX_HISTORY) {
      updated.shift();
    }

    set({
      history: updated,
      historyIndex: updated.length - 1,
    });
  },

  undo: () => {
    const state = get();
    if (state.historyIndex <= 0) return;

    const newIndex = state.historyIndex - 1;
    const entry = state.history[newIndex];

    set((s) => ({
      design: {
        ...s.design,
        elements: cloneElements(entry.elements),
        updatedAt: new Date().toISOString(),
      },
      historyIndex: newIndex,
      isDirty: true,
      selectedElementIds: [],
    }));
  },

  redo: () => {
    const state = get();
    if (state.historyIndex >= state.history.length - 1) return;

    const newIndex = state.historyIndex + 1;
    const entry = state.history[newIndex];

    set((s) => ({
      design: {
        ...s.design,
        elements: cloneElements(entry.elements),
        updatedAt: new Date().toISOString(),
      },
      historyIndex: newIndex,
      isDirty: true,
      selectedElementIds: [],
    }));
  },

  canUndo: () => {
    const s = get();
    return s.historyIndex > 0;
  },

  canRedo: () => {
    const s = get();
    return s.historyIndex < s.history.length - 1;
  },
}));
