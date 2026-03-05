/**
 * SPHERES Studio — Design Canvas
 *
 * The main interactive HTML5 Canvas component for the activation design tool.
 *
 * Interactions:
 *   - Drag-and-drop elements from the ElementLibrary sidebar
 *   - Click to select / Shift+click for additive selection
 *   - Drag selected elements to move them
 *   - Drag on empty space to marquee-select
 *   - R  key        — rotate selected 15 degrees
 *   - G  key        — toggle snap-to-grid
 *   - Delete / Backspace — delete selected elements
 *   - Ctrl+Z / Cmd+Z    — undo
 *   - Ctrl+Shift+Z / Cmd+Shift+Z — redo
 *   - Scroll wheel       — zoom (centred on cursor)
 *   - Middle mouse drag / Space+drag — pan
 *   - Layer visibility toggles in the toolbar
 */

import React, {
  useCallback,
  useEffect,
  useLayoutEffect,
  useMemo,
  useRef,
  useState,
} from "react";
import {
  Grid3x3,
  Undo2,
  Redo2,
  Trash2,
  ZoomIn,
  ZoomOut,
  Eye,
  EyeOff,
  RotateCw,
  Lock,
  Unlock,
  Save,
} from "lucide-react";
import { useCanvas } from "../hooks/useCanvas";
import type { DesignElement, Point } from "../utils/canvasRenderer";
import {
  drawGrid,
  drawParcelBoundary,
  drawElement,
  drawSelectionBox,
  hitTest,
  hitTestRect,
  screenToCanvas,
  isInsideParcel,
  snapToGrid,
} from "../utils/canvasRenderer";
import ElementLibrary from "./ElementLibrary";

// ---------------------------------------------------------------------------
// Interaction state machine
// ---------------------------------------------------------------------------

type InteractionMode =
  | { kind: "idle" }
  | { kind: "panning"; startX: number; startY: number; startOffset: Point }
  | {
      kind: "moving";
      startX: number;
      startY: number;
      startPositions: Map<string, Point>;
    }
  | { kind: "marquee"; startX: number; startY: number };

// ---------------------------------------------------------------------------
// Component
// ---------------------------------------------------------------------------

const Canvas: React.FC = () => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);
  const [interaction, setInteraction] = useState<InteractionMode>({
    kind: "idle",
  });
  const [marqueeEnd, setMarqueeEnd] = useState<Point | null>(null);
  const [spaceHeld, setSpaceHeld] = useState(false);
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  const [boundaryWarnings, setBoundaryWarnings] = useState<Set<string>>(
    new Set(),
  );

  // Zustand state
  const {
    elements,
    elementDefs,
    setElementDefs,
    selectedIds,
    selectElement,
    multiSelect,
    deselectAll,
    parcelFootprint,
    gridEnabled,
    gridSize,
    zoom,
    panOffset,
    toggleGrid,
    zoomBy,
    panBy,
    layerVisibility,
    toggleLayerVisibility,
    addElement,
    removeElements,
    moveElement,
    moveElements,
    rotateElement,
    undo,
    redo,
    canUndo,
    canRedo,
    designName,
  } = useCanvas();

  // -----------------------------------------------------------------------
  // Load element definitions from API on mount
  // -----------------------------------------------------------------------
  useEffect(() => {
    fetch("/api/designs/elements")
      .then((r) => r.json())
      .then((data) => setElementDefs(data))
      .catch(() => {
        // Fallback: definitions may already be set or API unavailable
      });
  }, [setElementDefs]);

  // -----------------------------------------------------------------------
  // Canvas resize observer
  // -----------------------------------------------------------------------
  useLayoutEffect(() => {
    const container = containerRef.current;
    const canvas = canvasRef.current;
    if (!container || !canvas) return;

    const ro = new ResizeObserver(() => {
      const dpr = window.devicePixelRatio || 1;
      const { width, height } = container.getBoundingClientRect();
      canvas.width = width * dpr;
      canvas.height = height * dpr;
      canvas.style.width = `${width}px`;
      canvas.style.height = `${height}px`;
    });
    ro.observe(container);
    return () => ro.disconnect();
  }, []);

  // -----------------------------------------------------------------------
  // Drawing loop
  // -----------------------------------------------------------------------
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    let animId: number;

    const draw = () => {
      const ctx = canvas.getContext("2d");
      if (!ctx) return;

      const dpr = window.devicePixelRatio || 1;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);

      const w = canvas.width / dpr;
      const h = canvas.height / dpr;

      // Clear
      ctx.fillStyle = "#0F1117";
      ctx.fillRect(0, 0, w, h);

      // Grid
      if (gridEnabled) {
        drawGrid(ctx, gridSize, zoom, panOffset, w, h);
      }

      // Parcel
      drawParcelBoundary(ctx, parcelFootprint, zoom, panOffset);

      // Elements (layer-filtered)
      const visibleElements = elements.filter(
        (e) => layerVisibility[e.layer as keyof typeof layerVisibility],
      );

      for (const el of visibleElements) {
        const def = elementDefs.get(el.element_id);
        if (!def) continue;
        const isSelected = selectedIds.includes(el.instance_id);
        drawElement(ctx, el, def, isSelected, zoom, panOffset);

        // Boundary warning
        if (
          parcelFootprint.length >= 3 &&
          !isInsideParcel(el, def, parcelFootprint)
        ) {
          // Draw a small warning indicator
          const sp = {
            x: el.x * zoom + panOffset.x,
            y: el.y * zoom + panOffset.y,
          };
          ctx.save();
          ctx.fillStyle = "#EF4444";
          ctx.font = "bold 14px Inter, system-ui, sans-serif";
          ctx.fillText("\u26A0", sp.x - 2, sp.y - 4);
          ctx.restore();
        }
      }

      // Marquee
      if (interaction.kind === "marquee" && marqueeEnd) {
        drawSelectionBox(
          ctx,
          { x: interaction.startX, y: interaction.startY },
          marqueeEnd,
        );
      }

      animId = requestAnimationFrame(draw);
    };

    animId = requestAnimationFrame(draw);
    return () => cancelAnimationFrame(animId);
  }, [
    elements,
    elementDefs,
    selectedIds,
    parcelFootprint,
    gridEnabled,
    gridSize,
    zoom,
    panOffset,
    layerVisibility,
    interaction,
    marqueeEnd,
  ]);

  // -----------------------------------------------------------------------
  // Boundary warnings (computed on element changes)
  // -----------------------------------------------------------------------
  useEffect(() => {
    if (parcelFootprint.length < 3) {
      setBoundaryWarnings(new Set());
      return;
    }
    const warnings = new Set<string>();
    for (const el of elements) {
      const def = elementDefs.get(el.element_id);
      if (def && !isInsideParcel(el, def, parcelFootprint)) {
        warnings.add(el.instance_id);
      }
    }
    setBoundaryWarnings(warnings);
  }, [elements, elementDefs, parcelFootprint]);

  // -----------------------------------------------------------------------
  // Mouse handlers
  // -----------------------------------------------------------------------
  const handleMouseDown = useCallback(
    (e: React.MouseEvent<HTMLCanvasElement>) => {
      const canvas = canvasRef.current;
      if (!canvas) return;
      const rect = canvas.getBoundingClientRect();
      const sx = e.clientX - rect.left;
      const sy = e.clientY - rect.top;

      // Middle-button pan or space+click pan
      if (e.button === 1 || (e.button === 0 && spaceHeld)) {
        setInteraction({
          kind: "panning",
          startX: e.clientX,
          startY: e.clientY,
          startOffset: { ...panOffset },
        });
        return;
      }

      if (e.button !== 0) return;

      // Hit test
      const hit = hitTest(sx, sy, elements, elementDefs, zoom, panOffset);

      if (hit) {
        if (hit.locked) {
          // Just select locked elements, don't move
          selectElement(hit.instance_id, e.shiftKey);
          return;
        }

        // If clicking on an unselected element without shift, select it solo
        if (!e.shiftKey && !selectedIds.includes(hit.instance_id)) {
          selectElement(hit.instance_id);
        } else if (e.shiftKey) {
          selectElement(hit.instance_id, true);
        }

        // Prepare for move — capture current positions of all selected
        const ids = selectedIds.includes(hit.instance_id)
          ? selectedIds
          : [hit.instance_id];
        const startPositions = new Map<string, Point>();
        for (const id of ids) {
          const el = elements.find((el) => el.instance_id === id);
          if (el && !el.locked) startPositions.set(id, { x: el.x, y: el.y });
        }

        setInteraction({
          kind: "moving",
          startX: sx,
          startY: sy,
          startPositions,
        });
      } else {
        // Empty space — begin marquee
        if (!e.shiftKey) deselectAll();
        setInteraction({ kind: "marquee", startX: sx, startY: sy });
        setMarqueeEnd(null);
      }
    },
    [
      elements,
      elementDefs,
      selectedIds,
      zoom,
      panOffset,
      spaceHeld,
      selectElement,
      deselectAll,
    ],
  );

  const handleMouseMove = useCallback(
    (e: React.MouseEvent<HTMLCanvasElement>) => {
      const canvas = canvasRef.current;
      if (!canvas) return;

      if (interaction.kind === "panning") {
        const dx = e.clientX - interaction.startX;
        const dy = e.clientY - interaction.startY;
        useCanvas.setState({
          panOffset: {
            x: interaction.startOffset.x + dx,
            y: interaction.startOffset.y + dy,
          },
        });
        return;
      }

      const rect = canvas.getBoundingClientRect();
      const sx = e.clientX - rect.left;
      const sy = e.clientY - rect.top;

      if (interaction.kind === "moving") {
        const dxScreen = sx - interaction.startX;
        const dyScreen = sy - interaction.startY;
        const dxCanvas = dxScreen / zoom;
        const dyCanvas = dyScreen / zoom;

        // Directly update positions (history is pushed once on mouseup)
        const newElements = elements.map((el) => {
          const startPos = interaction.startPositions.get(el.instance_id);
          if (!startPos) return el;
          const nx = startPos.x + dxCanvas;
          const ny = startPos.y + dyCanvas;
          return {
            ...el,
            x: gridEnabled ? snapToGrid(nx, gridSize) : nx,
            y: gridEnabled ? snapToGrid(ny, gridSize) : ny,
          };
        });
        useCanvas.setState({ elements: newElements });
        return;
      }

      if (interaction.kind === "marquee") {
        setMarqueeEnd({ x: sx, y: sy });
      }
    },
    [interaction, elements, zoom, gridEnabled, gridSize],
  );

  const handleMouseUp = useCallback(
    (e: React.MouseEvent<HTMLCanvasElement>) => {
      const canvas = canvasRef.current;
      if (!canvas) return;

      if (interaction.kind === "moving") {
        // Push a single undo entry for the entire drag
        const rect = canvas.getBoundingClientRect();
        const sx = e.clientX - rect.left;
        const sy = e.clientY - rect.top;
        const dxScreen = sx - interaction.startX;
        const dyScreen = sy - interaction.startY;
        const dxCanvas = dxScreen / zoom;
        const dyCanvas = dyScreen / zoom;

        // Only push history if actually moved
        if (Math.abs(dxCanvas) > 0.5 || Math.abs(dyCanvas) > 0.5) {
          const ids = [...interaction.startPositions.keys()];
          moveElements(ids, 0, 0); // this pushes history with current positions
        }
      }

      if (interaction.kind === "marquee" && marqueeEnd) {
        const hits = hitTestRect(
          { x: interaction.startX, y: interaction.startY },
          marqueeEnd,
          elements,
          elementDefs,
          zoom,
          panOffset,
        );
        if (hits.length > 0) {
          multiSelect(hits.map((h) => h.instance_id));
        }
        setMarqueeEnd(null);
      }

      setInteraction({ kind: "idle" });
    },
    [
      interaction,
      marqueeEnd,
      elements,
      elementDefs,
      zoom,
      panOffset,
      moveElements,
      multiSelect,
    ],
  );

  // -----------------------------------------------------------------------
  // Scroll wheel → zoom
  // -----------------------------------------------------------------------
  const handleWheel = useCallback(
    (e: React.WheelEvent<HTMLCanvasElement>) => {
      e.preventDefault();
      const rect = canvasRef.current?.getBoundingClientRect();
      if (!rect) return;
      const pivot = { x: e.clientX - rect.left, y: e.clientY - rect.top };
      const delta = e.deltaY < 0 ? 0.08 : -0.08;
      zoomBy(delta, pivot);
    },
    [zoomBy],
  );

  // -----------------------------------------------------------------------
  // Keyboard shortcuts
  // -----------------------------------------------------------------------
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      // Space for panning
      if (e.code === "Space" && !e.repeat) {
        e.preventDefault();
        setSpaceHeld(true);
        return;
      }

      // G — toggle grid
      if (e.code === "KeyG" && !e.ctrlKey && !e.metaKey) {
        toggleGrid();
        return;
      }

      // R — rotate selected
      if (
        e.code === "KeyR" &&
        !e.ctrlKey &&
        !e.metaKey &&
        selectedIds.length > 0
      ) {
        for (const id of selectedIds) {
          rotateElement(id, 15);
        }
        return;
      }

      // Delete / Backspace — remove selected
      if (
        (e.code === "Delete" || e.code === "Backspace") &&
        selectedIds.length > 0
      ) {
        // Don't delete if focus is in an input
        if (
          document.activeElement instanceof HTMLInputElement ||
          document.activeElement instanceof HTMLTextAreaElement
        ) {
          return;
        }
        removeElements(selectedIds);
        return;
      }

      // Ctrl+Z / Cmd+Z — undo
      if ((e.ctrlKey || e.metaKey) && e.code === "KeyZ" && !e.shiftKey) {
        e.preventDefault();
        undo();
        return;
      }

      // Ctrl+Shift+Z / Cmd+Shift+Z — redo
      if ((e.ctrlKey || e.metaKey) && e.code === "KeyZ" && e.shiftKey) {
        e.preventDefault();
        redo();
        return;
      }

      // Escape — deselect
      if (e.code === "Escape") {
        deselectAll();
      }
    };

    const handleKeyUp = (e: KeyboardEvent) => {
      if (e.code === "Space") {
        setSpaceHeld(false);
      }
    };

    window.addEventListener("keydown", handleKeyDown);
    window.addEventListener("keyup", handleKeyUp);
    return () => {
      window.removeEventListener("keydown", handleKeyDown);
      window.removeEventListener("keyup", handleKeyUp);
    };
  }, [
    selectedIds,
    toggleGrid,
    rotateElement,
    removeElements,
    undo,
    redo,
    deselectAll,
  ]);

  // -----------------------------------------------------------------------
  // Drop handler — receive elements dragged from the library sidebar
  // -----------------------------------------------------------------------
  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.dataTransfer.dropEffect = "copy";
  }, []);

  const handleDrop = useCallback(
    (e: React.DragEvent) => {
      e.preventDefault();
      const elementId = e.dataTransfer.getData("application/spheres-element");
      if (!elementId) return;

      const canvas = canvasRef.current;
      if (!canvas) return;
      const rect = canvas.getBoundingClientRect();
      const sx = e.clientX - rect.left;
      const sy = e.clientY - rect.top;
      const canvasPoint = screenToCanvas(sx, sy, zoom, panOffset);

      const def = elementDefs.get(elementId);
      if (!def) return;

      // Centre the element on the drop point
      let x = canvasPoint.x - def.footprint_width / 2;
      let y = canvasPoint.y - def.footprint_height / 2;

      if (gridEnabled) {
        x = snapToGrid(x, gridSize);
        y = snapToGrid(y, gridSize);
      }

      const newElement: DesignElement = {
        instance_id: crypto.randomUUID().slice(0, 12),
        element_id: elementId,
        x,
        y,
        rotation: 0,
        scale: 1,
        layer: def.layer,
        locked: false,
        custom_notes: "",
      };

      addElement(newElement);
    },
    [elementDefs, zoom, panOffset, gridEnabled, gridSize, addElement],
  );

  // -----------------------------------------------------------------------
  // Save handler
  // -----------------------------------------------------------------------
  const handleSave = useCallback(async () => {
    try {
      const body = {
        name: designName,
        elements: elements,
        parcel_footprint: parcelFootprint,
        is_public: false,
        tags: [],
      };
      const res = await fetch("/api/designs/save", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      });
      if (res.ok) {
        const saved = await res.json();
        useCanvas.setState({ designId: saved.id });
      }
    } catch {
      // Silently fail in demo mode if API not available
    }
  }, [designName, elements, parcelFootprint]);

  // -----------------------------------------------------------------------
  // Selected element info
  // -----------------------------------------------------------------------
  const selectedElements = elements.filter((e) =>
    selectedIds.includes(e.instance_id),
  );
  const firstSelected =
    selectedElements.length === 1 ? selectedElements[0] : null;
  const firstSelectedDef = firstSelected
    ? elementDefs.get(firstSelected.element_id)
    : null;

  // -----------------------------------------------------------------------
  // Cursor
  // -----------------------------------------------------------------------
  let cursor = "default";
  if (spaceHeld || interaction.kind === "panning") cursor = "grab";
  if (interaction.kind === "moving") cursor = "grabbing";
  if (interaction.kind === "marquee") cursor = "crosshair";

  // -----------------------------------------------------------------------
  // Render
  // -----------------------------------------------------------------------
  const elementDefsArray = useMemo(
    () => [...elementDefs.values()],
    [elementDefs],
  );

  return (
    <div className="flex h-full w-full bg-[#0F1117]">
      {/* Sidebar */}
      <div
        className={`shrink-0 border-r border-white/[0.06] bg-[#13151C] transition-all duration-200 ${
          sidebarCollapsed ? "w-0 overflow-hidden" : "w-72"
        }`}
      >
        <ElementLibrary elements={elementDefsArray} />
      </div>

      {/* Main area */}
      <div className="flex-1 flex flex-col min-w-0">
        {/* Top toolbar */}
        <div className="h-11 shrink-0 border-b border-white/[0.06] bg-[#13151C] flex items-center gap-1 px-3">
          {/* Sidebar toggle */}
          <button
            onClick={() => setSidebarCollapsed((v) => !v)}
            className="p-1.5 rounded hover:bg-white/[0.08] text-white/50 hover:text-white/80 transition-colors"
            title={sidebarCollapsed ? "Show library" : "Hide library"}
          >
            <Grid3x3 className="w-4 h-4" />
          </button>

          <div className="w-px h-5 bg-white/[0.08] mx-1" />

          {/* Undo / Redo */}
          <button
            onClick={undo}
            disabled={!canUndo}
            className="p-1.5 rounded hover:bg-white/[0.08] text-white/50 hover:text-white/80 disabled:opacity-25 disabled:pointer-events-none transition-colors"
            title="Undo (Ctrl+Z)"
          >
            <Undo2 className="w-4 h-4" />
          </button>
          <button
            onClick={redo}
            disabled={!canRedo}
            className="p-1.5 rounded hover:bg-white/[0.08] text-white/50 hover:text-white/80 disabled:opacity-25 disabled:pointer-events-none transition-colors"
            title="Redo (Ctrl+Shift+Z)"
          >
            <Redo2 className="w-4 h-4" />
          </button>

          <div className="w-px h-5 bg-white/[0.08] mx-1" />

          {/* Zoom controls */}
          <button
            onClick={() => zoomBy(-0.15)}
            className="p-1.5 rounded hover:bg-white/[0.08] text-white/50 hover:text-white/80 transition-colors"
            title="Zoom out"
          >
            <ZoomOut className="w-4 h-4" />
          </button>
          <span className="text-[12px] text-white/40 w-12 text-center tabular-nums">
            {Math.round(zoom * 25)}%
          </span>
          <button
            onClick={() => zoomBy(0.15)}
            className="p-1.5 rounded hover:bg-white/[0.08] text-white/50 hover:text-white/80 transition-colors"
            title="Zoom in"
          >
            <ZoomIn className="w-4 h-4" />
          </button>

          <div className="w-px h-5 bg-white/[0.08] mx-1" />

          {/* Grid toggle */}
          <button
            onClick={toggleGrid}
            className={`p-1.5 rounded transition-colors ${
              gridEnabled
                ? "bg-blue-500/20 text-blue-400"
                : "hover:bg-white/[0.08] text-white/40"
            }`}
            title="Toggle grid (G)"
          >
            <Grid3x3 className="w-4 h-4" />
          </button>

          <div className="w-px h-5 bg-white/[0.08] mx-1" />

          {/* Layer visibility */}
          {(
            [
              ["temporary", "Temporary", "#FBBF24"],
              ["permanent", "Permanent", "#22C55E"],
              ["infrastructure", "Infrastructure", "#94A3B8"],
            ] as const
          ).map(([key, label, color]) => (
            <button
              key={key}
              onClick={() => toggleLayerVisibility(key)}
              className={`flex items-center gap-1 px-2 py-1 rounded text-[11px] transition-colors ${
                layerVisibility[key]
                  ? "bg-white/[0.06] text-white/70"
                  : "text-white/25 hover:bg-white/[0.04]"
              }`}
              title={`${layerVisibility[key] ? "Hide" : "Show"} ${label} layer`}
            >
              {layerVisibility[key] ? (
                <Eye className="w-3 h-3" />
              ) : (
                <EyeOff className="w-3 h-3" />
              )}
              <span
                className="w-2 h-2 rounded-full"
                style={{
                  backgroundColor: layerVisibility[key] ? color : "transparent",
                  border: `1px solid ${color}`,
                }}
              />
              {label}
            </button>
          ))}

          {/* Spacer */}
          <div className="flex-1" />

          {/* Selection actions */}
          {selectedIds.length > 0 && (
            <>
              <button
                onClick={() => {
                  for (const id of selectedIds) rotateElement(id, 15);
                }}
                className="p-1.5 rounded hover:bg-white/[0.08] text-white/50 hover:text-white/80 transition-colors"
                title="Rotate 15 degrees (R)"
              >
                <RotateCw className="w-4 h-4" />
              </button>
              <button
                onClick={() => {
                  const el = elements.find(
                    (e) => e.instance_id === selectedIds[0],
                  );
                  if (el) {
                    useCanvas.getState().updateElement(el.instance_id, {
                      locked: !el.locked,
                    });
                  }
                }}
                className="p-1.5 rounded hover:bg-white/[0.08] text-white/50 hover:text-white/80 transition-colors"
                title={firstSelected?.locked ? "Unlock" : "Lock"}
              >
                {firstSelected?.locked ? (
                  <Lock className="w-4 h-4" />
                ) : (
                  <Unlock className="w-4 h-4" />
                )}
              </button>
              <button
                onClick={() => removeElements(selectedIds)}
                className="p-1.5 rounded hover:bg-red-500/20 text-white/50 hover:text-red-400 transition-colors"
                title="Delete (Del)"
              >
                <Trash2 className="w-4 h-4" />
              </button>
              <div className="w-px h-5 bg-white/[0.08] mx-1" />
            </>
          )}

          {/* Save */}
          <button
            onClick={handleSave}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-md bg-blue-600 hover:bg-blue-500 text-white text-[12px] font-medium transition-colors"
          >
            <Save className="w-3.5 h-3.5" />
            Save
          </button>
        </div>

        {/* Canvas area */}
        <div ref={containerRef} className="flex-1 relative overflow-hidden">
          <canvas
            ref={canvasRef}
            className="absolute inset-0"
            style={{ cursor }}
            onMouseDown={handleMouseDown}
            onMouseMove={handleMouseMove}
            onMouseUp={handleMouseUp}
            onMouseLeave={handleMouseUp}
            onWheel={handleWheel}
            onDragOver={handleDragOver}
            onDrop={handleDrop}
          />

          {/* Status bar */}
          <div className="absolute bottom-0 left-0 right-0 h-7 bg-[#13151C]/90 backdrop-blur border-t border-white/[0.06] flex items-center px-3 gap-4 text-[11px] text-white/35">
            <span>
              Elements: {elements.length}
            </span>
            {selectedIds.length > 0 && (
              <span>
                Selected: {selectedIds.length}
              </span>
            )}
            {firstSelectedDef && firstSelected && (
              <span>
                {firstSelectedDef.name} &mdash;{" "}
                {firstSelectedDef.footprint_width}&times;
                {firstSelectedDef.footprint_height} ft &mdash; (
                {Math.round(firstSelected.x)}, {Math.round(firstSelected.y)})
              </span>
            )}
            {boundaryWarnings.size > 0 && (
              <span className="text-amber-400/70">
                {boundaryWarnings.size} element
                {boundaryWarnings.size > 1 ? "s" : ""} outside parcel boundary
              </span>
            )}
            <div className="flex-1" />
            <span>
              Grid: {gridEnabled ? `${gridSize} ft` : "off"}
            </span>
            <span>
              Zoom: {Math.round(zoom * 25)}%
            </span>
          </div>
        </div>

        {/* Properties panel (when single selection) */}
        {firstSelected && firstSelectedDef && (
          <div className="shrink-0 h-36 border-t border-white/[0.06] bg-[#13151C] px-4 py-3 overflow-y-auto">
            <div className="flex items-center gap-3 mb-2">
              <div
                className="w-8 h-8 rounded-md flex items-center justify-center"
                style={{
                  backgroundColor: firstSelectedDef.color + "30",
                }}
              >
                <div
                  className="w-4 h-4 rounded-sm"
                  style={{ backgroundColor: firstSelectedDef.color }}
                />
              </div>
              <div>
                <div className="text-[13px] font-semibold text-white/90">
                  {firstSelectedDef.name}
                </div>
                <div className="text-[11px] text-white/40">
                  {firstSelectedDef.description}
                </div>
              </div>
            </div>

            <div className="grid grid-cols-4 gap-x-4 gap-y-1.5 text-[12px]">
              <div>
                <span className="text-white/30">Position</span>
                <div className="text-white/70 font-mono">
                  ({Math.round(firstSelected.x)},{" "}
                  {Math.round(firstSelected.y)})
                </div>
              </div>
              <div>
                <span className="text-white/30">Size</span>
                <div className="text-white/70 font-mono">
                  {firstSelectedDef.footprint_width}&times;
                  {firstSelectedDef.footprint_height} ft
                </div>
              </div>
              <div>
                <span className="text-white/30">Rotation</span>
                <div className="text-white/70 font-mono">
                  {firstSelected.rotation}&deg;
                </div>
              </div>
              <div>
                <span className="text-white/30">Scale</span>
                <div className="text-white/70 font-mono">
                  {firstSelected.scale.toFixed(2)}x
                </div>
              </div>
              <div>
                <span className="text-white/30">Layer</span>
                <div className="text-white/70 capitalize">
                  {firstSelected.layer}
                </div>
              </div>
              <div>
                <span className="text-white/30">Cost</span>
                <div className="text-white/70">
                  ${firstSelectedDef.cost_estimate.low.toLocaleString()} &ndash;{" "}
                  ${firstSelectedDef.cost_estimate.high.toLocaleString()}
                </div>
              </div>
              <div>
                <span className="text-white/30">Permanence</span>
                <div className="text-white/70">
                  {firstSelectedDef.permanence_potential}%
                </div>
              </div>
              <div>
                <span className="text-white/30">Permits</span>
                <div className="text-white/70">
                  {firstSelectedDef.permit_requirements.length > 0
                    ? firstSelectedDef.permit_requirements
                        .map((p) => p.replace(/_/g, " "))
                        .join(", ")
                    : "None"}
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Canvas;
