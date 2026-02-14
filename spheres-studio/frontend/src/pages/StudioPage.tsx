/**
 * SPHERES Studio — Studio Page
 *
 * The core design experience: top bar, collapsible left sidebar (element
 * library), center canvas, collapsible right detail panel, and floating
 * cost ticker.  Keyboard shortcuts are registered at mount time.
 */

import { useCallback, useEffect, useRef, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import {
  // Top bar icons
  Save,
  Share2,
  Box,
  Clock,
  Download,
  ChevronDown,
  User,
  Undo2,
  Redo2,
  // Sidebar icons
  Mic,
  Armchair,
  ShoppingCart,
  Sprout,
  Paintbrush,
  Baby,
  Route,
  ChevronRight,
  ChevronLeft,
  Search,
  GripVertical,
  // Canvas tools
  MousePointer2,
  Hand,
  Grid3x3,
  // Detail panel
  X,
  Lock,
  Unlock,
  RotateCw,
  Trash2,
  Copy,
  FileText,
  // Cost ticker
  DollarSign,
  TrendingUp,
  AlertTriangle,
  MapPin,
  // Canvas empty state
  Layers,
} from 'lucide-react';
import type { LucideProps } from 'lucide-react';
import { useStudioStore, type DesignElement } from '../context/StudioStore';

// ---------------------------------------------------------------------------
// Element library data (mirrors the backend catalog for the sidebar)
// ---------------------------------------------------------------------------

type LucideIcon = React.FC<LucideProps>;

interface ElementDef {
  id: string;
  name: string;
  category: string;
  icon: LucideIcon;
  footprintWidth: number;
  footprintHeight: number;
  costLow: number;
  costHigh: number;
  permits: string[];
  permanence: number;
  layer: 'temporary' | 'permanent' | 'infrastructure';
  color: string;
  description: string;
}

const CATEGORIES: { id: string; label: string; icon: LucideIcon }[] = [
  { id: 'performance', label: 'Performance', icon: Mic },
  { id: 'seating', label: 'Seating', icon: Armchair },
  { id: 'food_vendor', label: 'Food & Vendor', icon: ShoppingCart },
  { id: 'gardens_nature', label: 'Gardens & Nature', icon: Sprout },
  { id: 'art', label: 'Art', icon: Paintbrush },
  { id: 'recreation', label: 'Recreation', icon: Baby },
  { id: 'infrastructure', label: 'Infrastructure', icon: Route },
];

const ELEMENTS: ElementDef[] = [
  { id: 'stage_small', name: 'Small Stage', category: 'performance', icon: Mic, footprintWidth: 10, footprintHeight: 10, costLow: 500, costHigh: 2000, permits: ['Temporary Structure', 'Noise'], permanence: 15, layer: 'temporary', color: '#8B5CF6', description: 'Portable stage platform' },
  { id: 'stage_medium', name: 'Medium Stage', category: 'performance', icon: Mic, footprintWidth: 20, footprintHeight: 15, costLow: 2000, costHigh: 8000, permits: ['Temporary Structure', 'Noise', 'Electrical'], permanence: 20, layer: 'temporary', color: '#7C3AED', description: 'Mid-size stage with lighting' },
  { id: 'stage_large', name: 'Large Stage', category: 'performance', icon: Mic, footprintWidth: 30, footprintHeight: 20, costLow: 5000, costHigh: 20000, permits: ['Temporary Structure', 'Noise', 'Electrical', 'Special Event'], permanence: 25, layer: 'temporary', color: '#6D28D9', description: 'Full-size concert stage' },
  { id: 'sound_equipment', name: 'Sound Equipment', category: 'performance', icon: Mic, footprintWidth: 5, footprintHeight: 5, costLow: 200, costHigh: 1000, permits: ['Noise'], permanence: 10, layer: 'temporary', color: '#A78BFA', description: 'PA system and speakers' },
  { id: 'screening_wall', name: 'Screening Wall', category: 'performance', icon: Mic, footprintWidth: 15, footprintHeight: 8, costLow: 1000, costHigh: 5000, permits: ['Temporary Structure', 'Electrical'], permanence: 20, layer: 'temporary', color: '#C4B5FD', description: 'LED wall for outdoor cinema' },
  { id: 'bench', name: 'Bench', category: 'seating', icon: Armchair, footprintWidth: 6, footprintHeight: 2, costLow: 200, costHigh: 800, permits: [], permanence: 60, layer: 'permanent', color: '#F59E0B', description: 'Standard park bench' },
  { id: 'picnic_table', name: 'Picnic Table', category: 'seating', icon: Armchair, footprintWidth: 6, footprintHeight: 4, costLow: 300, costHigh: 1200, permits: [], permanence: 65, layer: 'permanent', color: '#FBBF24', description: 'Picnic table with bench seating' },
  { id: 'chair_cluster', name: 'Chair Cluster', category: 'seating', icon: Armchair, footprintWidth: 8, footprintHeight: 8, costLow: 100, costHigh: 500, permits: [], permanence: 10, layer: 'temporary', color: '#FCD34D', description: 'Movable social seating' },
  { id: 'bleachers', name: 'Bleachers', category: 'seating', icon: Armchair, footprintWidth: 20, footprintHeight: 8, costLow: 2000, costHigh: 8000, permits: ['Temporary Structure'], permanence: 30, layer: 'temporary', color: '#F59E0B', description: 'Portable event bleachers' },
  { id: 'amphitheater_seating', name: 'Amphitheater', category: 'seating', icon: Armchair, footprintWidth: 30, footprintHeight: 20, costLow: 10000, costHigh: 50000, permits: ['Building', 'Grading'], permanence: 95, layer: 'permanent', color: '#D97706', description: 'Permanent tiered seating' },
  { id: 'food_cart', name: 'Food Cart', category: 'food_vendor', icon: ShoppingCart, footprintWidth: 6, footprintHeight: 4, costLow: 100, costHigh: 500, permits: ['Food'], permanence: 10, layer: 'temporary', color: '#EF4444', description: 'Mobile food cart' },
  { id: 'food_truck_space', name: 'Food Truck Space', category: 'food_vendor', icon: ShoppingCart, footprintWidth: 25, footprintHeight: 10, costLow: 200, costHigh: 800, permits: ['Food', 'Encroachment'], permanence: 10, layer: 'temporary', color: '#DC2626', description: 'Food truck parking pad' },
  { id: 'market_stall', name: 'Market Stall', category: 'food_vendor', icon: ShoppingCart, footprintWidth: 10, footprintHeight: 10, costLow: 300, costHigh: 1500, permits: ['Food', 'Temporary Structure'], permanence: 20, layer: 'temporary', color: '#F87171', description: 'Farmers market stall' },
  { id: 'vendor_tent', name: 'Vendor Tent', category: 'food_vendor', icon: ShoppingCart, footprintWidth: 10, footprintHeight: 10, costLow: 200, costHigh: 1000, permits: ['Temporary Structure'], permanence: 10, layer: 'temporary', color: '#FCA5A5', description: 'Pop-up vendor tent' },
  { id: 'raised_bed', name: 'Raised Bed', category: 'gardens_nature', icon: Sprout, footprintWidth: 8, footprintHeight: 4, costLow: 200, costHigh: 1000, permits: [], permanence: 90, layer: 'permanent', color: '#22C55E', description: 'Raised garden bed' },
  { id: 'tree_planting', name: 'Tree Planting', category: 'gardens_nature', icon: Sprout, footprintWidth: 8, footprintHeight: 8, costLow: 500, costHigh: 2000, permits: ['Tree'], permanence: 95, layer: 'permanent', color: '#16A34A', description: 'New tree with mulch ring' },
  { id: 'flower_garden', name: 'Flower Garden', category: 'gardens_nature', icon: Sprout, footprintWidth: 10, footprintHeight: 10, costLow: 300, costHigh: 1500, permits: [], permanence: 80, layer: 'permanent', color: '#4ADE80', description: 'Ornamental flower garden' },
  { id: 'native_meadow', name: 'Native Meadow', category: 'gardens_nature', icon: Sprout, footprintWidth: 20, footprintHeight: 20, costLow: 500, costHigh: 3000, permits: [], permanence: 95, layer: 'permanent', color: '#15803D', description: 'Native wildflower meadow' },
  { id: 'water_feature', name: 'Water Feature', category: 'gardens_nature', icon: Sprout, footprintWidth: 10, footprintHeight: 10, costLow: 2000, costHigh: 10000, permits: ['Plumbing', 'Building'], permanence: 85, layer: 'permanent', color: '#06B6D4', description: 'Fountain or splash pad' },
  { id: 'mural_wall', name: 'Mural Wall', category: 'art', icon: Paintbrush, footprintWidth: 20, footprintHeight: 10, costLow: 1000, costHigh: 5000, permits: ['Sign'], permanence: 90, layer: 'permanent', color: '#EC4899', description: 'Community mural surface' },
  { id: 'sculpture_pad', name: 'Sculpture Pad', category: 'art', icon: Paintbrush, footprintWidth: 8, footprintHeight: 8, costLow: 500, costHigh: 3000, permits: [], permanence: 50, layer: 'temporary', color: '#F472B6', description: 'Rotating sculpture pad' },
  { id: 'interactive_art', name: 'Interactive Art', category: 'art', icon: Paintbrush, footprintWidth: 12, footprintHeight: 12, costLow: 1000, costHigh: 8000, permits: ['Electrical'], permanence: 40, layer: 'temporary', color: '#DB2777', description: 'Responsive art installation' },
  { id: 'art_installation', name: 'Art Installation', category: 'art', icon: Paintbrush, footprintWidth: 15, footprintHeight: 15, costLow: 2000, costHigh: 15000, permits: ['Temporary Structure'], permanence: 35, layer: 'temporary', color: '#BE185D', description: 'Large-scale art piece' },
  { id: 'play_structure', name: 'Play Structure', category: 'recreation', icon: Baby, footprintWidth: 20, footprintHeight: 20, costLow: 5000, costHigh: 25000, permits: ['Building'], permanence: 90, layer: 'permanent', color: '#3B82F6', description: 'Playground equipment' },
  { id: 'basketball_half', name: 'Half Court', category: 'recreation', icon: Baby, footprintWidth: 30, footprintHeight: 25, costLow: 3000, costHigh: 15000, permits: ['Building', 'Grading'], permanence: 85, layer: 'permanent', color: '#2563EB', description: 'Basketball half court' },
  { id: 'fitness_station', name: 'Fitness Station', category: 'recreation', icon: Baby, footprintWidth: 10, footprintHeight: 10, costLow: 2000, costHigh: 8000, permits: ['Building'], permanence: 90, layer: 'permanent', color: '#1D4ED8', description: 'Outdoor fitness equipment' },
  { id: 'sports_field', name: 'Sports Field', category: 'recreation', icon: Baby, footprintWidth: 60, footprintHeight: 30, costLow: 5000, costHigh: 20000, permits: ['Grading', 'Land Use'], permanence: 70, layer: 'permanent', color: '#1E40AF', description: 'Multi-purpose sports field' },
  { id: 'pathway', name: 'Pathway', category: 'infrastructure', icon: Route, footprintWidth: 20, footprintHeight: 4, costLow: 500, costHigh: 3000, permits: ['Grading'], permanence: 95, layer: 'infrastructure', color: '#6B7280', description: 'Paved walking path' },
  { id: 'fencing', name: 'Fencing', category: 'infrastructure', icon: Route, footprintWidth: 20, footprintHeight: 1, costLow: 300, costHigh: 1500, permits: ['Building'], permanence: 70, layer: 'infrastructure', color: '#9CA3AF', description: 'Perimeter fencing' },
  { id: 'lighting_pole', name: 'Lighting Pole', category: 'infrastructure', icon: Route, footprintWidth: 3, footprintHeight: 3, costLow: 500, costHigh: 2000, permits: ['Electrical'], permanence: 90, layer: 'infrastructure', color: '#D1D5DB', description: 'Street or path light' },
  { id: 'power_hookup', name: 'Power Hookup', category: 'infrastructure', icon: Route, footprintWidth: 3, footprintHeight: 3, costLow: 500, costHigh: 2000, permits: ['Electrical'], permanence: 80, layer: 'infrastructure', color: '#E5E7EB', description: 'Electrical junction box' },
  { id: 'water_hookup', name: 'Water Hookup', category: 'infrastructure', icon: Route, footprintWidth: 3, footprintHeight: 3, costLow: 800, costHigh: 3000, permits: ['Plumbing'], permanence: 85, layer: 'infrastructure', color: '#93C5FD', description: 'Water supply connection' },
  { id: 'shade_structure', name: 'Shade Structure', category: 'infrastructure', icon: Route, footprintWidth: 15, footprintHeight: 15, costLow: 2000, costHigh: 8000, permits: ['Temporary Structure'], permanence: 50, layer: 'infrastructure', color: '#A3A3A3', description: 'Canopy or pergola' },
  { id: 'signage', name: 'Signage', category: 'infrastructure', icon: Route, footprintWidth: 4, footprintHeight: 2, costLow: 200, costHigh: 1000, permits: ['Sign'], permanence: 85, layer: 'infrastructure', color: '#78716C', description: 'Wayfinding signage' },
];

function getElementDef(id: string): ElementDef | undefined {
  return ELEMENTS.find((e) => e.id === id);
}

function generateInstanceId(): string {
  return Math.random().toString(36).substring(2, 14);
}

// ---------------------------------------------------------------------------
// ElementLibrary sidebar
// ---------------------------------------------------------------------------

function ElementLibrary() {
  const [expandedCategory, setExpandedCategory] = useState<string | null>('performance');
  const [search, setSearch] = useState('');
  const startPlacing = useStudioStore((s) => s.startPlacing);

  const filtered = search.trim()
    ? ELEMENTS.filter(
        (e) =>
          e.name.toLowerCase().includes(search.toLowerCase()) ||
          e.category.toLowerCase().includes(search.toLowerCase())
      )
    : ELEMENTS;

  const groupedByCategory = CATEGORIES.map((cat) => ({
    ...cat,
    elements: filtered.filter((e) => e.category === cat.id),
  })).filter((g) => g.elements.length > 0);

  return (
    <div className="flex h-full flex-col overflow-hidden">
      {/* Search */}
      <div className="p-3">
        <div
          className="flex items-center gap-2 rounded-lg px-3 py-2"
          style={{ background: 'var(--bg-elevated)', border: '1px solid var(--border)' }}
        >
          <Search size={14} style={{ color: 'var(--text-secondary)' }} />
          <input
            type="text"
            placeholder="Search elements..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="flex-1 bg-transparent text-xs outline-none"
            style={{ color: 'var(--text-primary)' }}
          />
        </div>
      </div>

      {/* Categories */}
      <div className="flex-1 overflow-y-auto px-1 pb-4">
        {groupedByCategory.map((group) => {
          const Icon = group.icon;
          const isExpanded = search.trim() ? true : expandedCategory === group.id;

          return (
            <div key={group.id} className="mb-1">
              <button
                onClick={() => setExpandedCategory(isExpanded ? null : group.id)}
                className="flex w-full cursor-pointer items-center gap-2 rounded-lg px-3 py-2 text-left transition-colors duration-150 hover:bg-white/5"
              >
                <Icon size={14} style={{ color: 'var(--text-secondary)' }} />
                <span className="flex-1 text-xs font-medium" style={{ color: 'var(--text-primary)' }}>
                  {group.label}
                </span>
                <span className="text-[10px]" style={{ color: 'var(--text-secondary)' }}>
                  {group.elements.length}
                </span>
                <ChevronRight
                  size={12}
                  className="transition-transform duration-200"
                  style={{
                    color: 'var(--text-secondary)',
                    transform: isExpanded ? 'rotate(90deg)' : 'none',
                  }}
                />
              </button>

              {isExpanded && (
                <div className="mt-0.5 ml-2 space-y-0.5">
                  {group.elements.map((el) => (
                    <button
                      key={el.id}
                      onClick={() => startPlacing(el.id)}
                      className="group flex w-full cursor-pointer items-center gap-2.5 rounded-lg px-3 py-2 text-left transition-all duration-150 hover:bg-white/5"
                    >
                      <div
                        className="flex h-7 w-7 shrink-0 items-center justify-center rounded-md transition-transform duration-150 group-hover:scale-110"
                        style={{ background: `${el.color}20`, color: el.color }}
                      >
                        <GripVertical size={12} />
                      </div>
                      <div className="min-w-0 flex-1">
                        <div className="truncate text-xs font-medium" style={{ color: 'var(--text-primary)' }}>
                          {el.name}
                        </div>
                        <div className="text-[10px]" style={{ color: 'var(--text-secondary)' }}>
                          ${el.costLow.toLocaleString()}-${el.costHigh.toLocaleString()}
                        </div>
                      </div>
                    </button>
                  ))}
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}

// ---------------------------------------------------------------------------
// Canvas
// ---------------------------------------------------------------------------

function Canvas() {
  const canvasRef = useRef<HTMLDivElement>(null);
  const {
    design,
    zoom,
    panOffset,
    gridEnabled,
    activeTool,
    placingElement,
    selectedElementIds,
    selectElements,
    deselectAll,
    addElement,
    cancelPlacing,
    setZoom,
    setPan,
    moveElements,
    pushHistory,
  } = useStudioStore();

  const [dragging, setDragging] = useState(false);
  const [dragStart, setDragStart] = useState<{ x: number; y: number } | null>(null);
  const [panStart, setPanStart] = useState<{ x: number; y: number; ox: number; oy: number } | null>(null);

  // Handle canvas click — place element or deselect
  const handleCanvasMouseDown = useCallback(
    (e: React.MouseEvent<HTMLDivElement>) => {
      if (e.target !== canvasRef.current) return;

      if (activeTool === 'place' && placingElement) {
        const rect = canvasRef.current!.getBoundingClientRect();
        const x = (e.clientX - rect.left - panOffset.x) / zoom;
        const y = (e.clientY - rect.top - panOffset.y) / zoom;

        const def = getElementDef(placingElement);
        if (!def) return;

        const newElement: DesignElement = {
          instanceId: generateInstanceId(),
          elementId: def.id,
          x: Math.round(x),
          y: Math.round(y),
          rotation: 0,
          scale: 1,
          layer: def.layer,
          locked: false,
          customNotes: '',
        };

        addElement(newElement);
        // Keep placing mode for rapid placement
        return;
      }

      if (activeTool === 'pan') {
        setPanStart({ x: e.clientX, y: e.clientY, ox: panOffset.x, oy: panOffset.y });
        return;
      }

      deselectAll();
    },
    [activeTool, placingElement, panOffset, zoom, addElement, deselectAll]
  );

  const handleCanvasMouseMove = useCallback(
    (e: React.MouseEvent<HTMLDivElement>) => {
      if (panStart) {
        const dx = e.clientX - panStart.x;
        const dy = e.clientY - panStart.y;
        setPan({ x: panStart.ox + dx, y: panStart.oy + dy });
      }
      if (dragging && dragStart && selectedElementIds.length > 0) {
        const dx = (e.clientX - dragStart.x) / zoom;
        const dy = (e.clientY - dragStart.y) / zoom;
        if (Math.abs(dx) > 1 || Math.abs(dy) > 1) {
          moveElements(selectedElementIds, dx, dy);
          setDragStart({ x: e.clientX, y: e.clientY });
        }
      }
    },
    [panStart, dragging, dragStart, selectedElementIds, zoom, setPan, moveElements]
  );

  const handleCanvasMouseUp = useCallback(() => {
    if (panStart) setPanStart(null);
    if (dragging) {
      setDragging(false);
      setDragStart(null);
    }
  }, [panStart, dragging]);

  // Mouse wheel zoom
  const handleWheel = useCallback(
    (e: React.WheelEvent) => {
      e.preventDefault();
      const delta = e.deltaY > 0 ? -0.1 : 0.1;
      setZoom(zoom + delta);
    },
    [zoom, setZoom]
  );

  // Element click
  const handleElementClick = useCallback(
    (e: React.MouseEvent, instanceId: string) => {
      e.stopPropagation();
      if (activeTool === 'select') {
        selectElements([instanceId], e.shiftKey);
      }
    },
    [activeTool, selectElements]
  );

  // Element drag start
  const handleElementMouseDown = useCallback(
    (e: React.MouseEvent, instanceId: string) => {
      e.stopPropagation();
      if (activeTool === 'select') {
        if (!selectedElementIds.includes(instanceId)) {
          selectElements([instanceId], e.shiftKey);
        }
        pushHistory('Move elements');
        setDragging(true);
        setDragStart({ x: e.clientX, y: e.clientY });
      }
    },
    [activeTool, selectedElementIds, selectElements, pushHistory]
  );

  const hasElements = design.elements.length > 0;

  return (
    <div
      ref={canvasRef}
      className="relative h-full w-full overflow-hidden"
      style={{
        background: 'var(--bg-primary)',
        cursor:
          activeTool === 'pan'
            ? 'grab'
            : activeTool === 'place'
            ? 'crosshair'
            : 'default',
      }}
      onMouseDown={handleCanvasMouseDown}
      onMouseMove={handleCanvasMouseMove}
      onMouseUp={handleCanvasMouseUp}
      onMouseLeave={handleCanvasMouseUp}
      onWheel={handleWheel}
    >
      {/* Grid overlay */}
      {gridEnabled && (
        <div
          className="pointer-events-none absolute inset-0 canvas-grid"
          style={{
            backgroundSize: `${20 * zoom}px ${20 * zoom}px`,
            backgroundPosition: `${panOffset.x}px ${panOffset.y}px`,
            opacity: 0.5,
          }}
        />
      )}

      {/* Elements layer */}
      <div
        className="absolute"
        style={{
          transform: `translate(${panOffset.x}px, ${panOffset.y}px) scale(${zoom})`,
          transformOrigin: '0 0',
        }}
      >
        {design.elements.map((el) => {
          const def = getElementDef(el.elementId);
          if (!def) return null;
          const isSelected = selectedElementIds.includes(el.instanceId);
          const pxPerFoot = 4;

          return (
            <div
              key={el.instanceId}
              className="absolute cursor-pointer transition-shadow duration-150"
              style={{
                left: `${el.x * pxPerFoot}px`,
                top: `${el.y * pxPerFoot}px`,
                width: `${def.footprintWidth * pxPerFoot}px`,
                height: `${def.footprintHeight * pxPerFoot}px`,
                background: `${def.color}25`,
                border: isSelected
                  ? `2px solid ${def.color}`
                  : `1px solid ${def.color}60`,
                borderRadius: '4px',
                transform: `rotate(${el.rotation}deg)`,
                boxShadow: isSelected
                  ? `0 0 0 2px ${def.color}40, 0 0 16px ${def.color}20`
                  : 'none',
              }}
              onClick={(e) => handleElementClick(e, el.instanceId)}
              onMouseDown={(e) => handleElementMouseDown(e, el.instanceId)}
            >
              <div
                className="flex h-full w-full flex-col items-center justify-center p-1"
              >
                <span
                  className="truncate text-[9px] font-medium leading-tight"
                  style={{ color: def.color }}
                >
                  {def.name}
                </span>
              </div>
              {el.locked && (
                <Lock
                  size={8}
                  className="absolute top-0.5 right-0.5"
                  style={{ color: def.color }}
                />
              )}
            </div>
          );
        })}
      </div>

      {/* Placing indicator */}
      {activeTool === 'place' && placingElement && (
        <div
          className="pointer-events-none absolute top-4 left-1/2 -translate-x-1/2 rounded-lg px-4 py-2"
          style={{
            background: 'var(--bg-elevated)',
            border: '1px solid var(--accent)',
            color: 'var(--text-primary)',
          }}
        >
          <span className="text-xs font-medium">
            Click to place {getElementDef(placingElement)?.name} — Press Escape to cancel
          </span>
        </div>
      )}

      {/* Empty state */}
      {!hasElements && activeTool !== 'place' && (
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <div
            className="mb-3 flex h-16 w-16 items-center justify-center rounded-2xl"
            style={{ background: 'var(--bg-surface)', border: '1px solid var(--border)' }}
          >
            <Layers size={24} style={{ color: 'var(--text-secondary)' }} />
          </div>
          <p className="mb-1 text-sm font-medium" style={{ color: 'var(--text-secondary)' }}>
            Drag elements from the library to start designing
          </p>
          <p className="text-xs" style={{ color: 'var(--text-secondary)', opacity: 0.6 }}>
            Or click an element in the sidebar and click on the canvas
          </p>
        </div>
      )}

      {/* Zoom indicator */}
      <div
        className="absolute bottom-4 left-4 rounded-md px-2 py-1 text-[10px] font-mono"
        style={{
          background: 'var(--bg-surface)',
          border: '1px solid var(--border)',
          color: 'var(--text-secondary)',
        }}
      >
        {Math.round(zoom * 100)}%
      </div>
    </div>
  );
}

// ---------------------------------------------------------------------------
// Detail panel (right)
// ---------------------------------------------------------------------------

function DetailPanel() {
  const {
    design,
    selectedElementIds,
    updateElement,
    removeElements,
    duplicateElements,
    rotateElements,
    lockElements,
    deselectAll,
    pushHistory,
  } = useStudioStore();

  if (selectedElementIds.length === 0) {
    return (
      <div className="flex h-full flex-col items-center justify-center px-6 text-center">
        <MousePointer2 size={20} className="mb-3" style={{ color: 'var(--text-secondary)', opacity: 0.4 }} />
        <p className="text-xs" style={{ color: 'var(--text-secondary)' }}>
          Select an element to view its details
        </p>
      </div>
    );
  }

  const selectedElement = design.elements.find(
    (el) => el.instanceId === selectedElementIds[0]
  );
  if (!selectedElement) return null;

  const def = getElementDef(selectedElement.elementId);
  if (!def) return null;

  const multiSelect = selectedElementIds.length > 1;

  return (
    <div className="flex h-full flex-col overflow-y-auto">
      {/* Header */}
      <div
        className="flex items-center justify-between px-4 py-3"
        style={{ borderBottom: '1px solid var(--border)' }}
      >
        <div className="flex items-center gap-2">
          <div
            className="flex h-6 w-6 items-center justify-center rounded"
            style={{ background: `${def.color}20`, color: def.color }}
          >
            <GripVertical size={12} />
          </div>
          <span className="text-xs font-semibold" style={{ color: 'var(--text-primary)' }}>
            {multiSelect
              ? `${selectedElementIds.length} elements selected`
              : def.name}
          </span>
        </div>
        <button
          onClick={deselectAll}
          className="cursor-pointer rounded p-1 transition-colors duration-150 hover:bg-white/10"
        >
          <X size={14} style={{ color: 'var(--text-secondary)' }} />
        </button>
      </div>

      {!multiSelect && (
        <>
          {/* Description */}
          <div className="px-4 py-3" style={{ borderBottom: '1px solid var(--border)' }}>
            <p className="text-[11px] leading-relaxed" style={{ color: 'var(--text-secondary)' }}>
              {def.description}
            </p>
          </div>

          {/* Cost */}
          <div className="px-4 py-3" style={{ borderBottom: '1px solid var(--border)' }}>
            <div className="mb-2 text-[10px] font-medium uppercase tracking-wider" style={{ color: 'var(--text-secondary)' }}>
              Estimated Cost
            </div>
            <div className="flex items-baseline gap-1">
              <DollarSign size={12} style={{ color: 'var(--accent-green)' }} />
              <span className="text-sm font-semibold" style={{ color: 'var(--text-primary)' }}>
                {def.costLow.toLocaleString()} - {def.costHigh.toLocaleString()}
              </span>
            </div>
          </div>

          {/* Permits */}
          {def.permits.length > 0 && (
            <div className="px-4 py-3" style={{ borderBottom: '1px solid var(--border)' }}>
              <div className="mb-2 text-[10px] font-medium uppercase tracking-wider" style={{ color: 'var(--text-secondary)' }}>
                Permits Required
              </div>
              <div className="flex flex-wrap gap-1.5">
                {def.permits.map((p) => (
                  <span
                    key={p}
                    className="rounded-md px-2 py-0.5 text-[10px] font-medium"
                    style={{
                      background: 'rgba(245,158,11,0.1)',
                      color: 'var(--accent-amber)',
                      border: '1px solid rgba(245,158,11,0.2)',
                    }}
                  >
                    {p}
                  </span>
                ))}
              </div>
            </div>
          )}

          {/* Permanence score */}
          <div className="px-4 py-3" style={{ borderBottom: '1px solid var(--border)' }}>
            <div className="mb-2 text-[10px] font-medium uppercase tracking-wider" style={{ color: 'var(--text-secondary)' }}>
              Permanence Score
            </div>
            <div className="flex items-center gap-3">
              <div className="h-1.5 flex-1 overflow-hidden rounded-full" style={{ background: 'var(--bg-elevated)' }}>
                <div
                  className="h-full rounded-full transition-all duration-300"
                  style={{
                    width: `${def.permanence}%`,
                    background:
                      def.permanence >= 70
                        ? 'var(--accent-green)'
                        : def.permanence >= 40
                        ? 'var(--accent-amber)'
                        : 'var(--accent-red)',
                  }}
                />
              </div>
              <span className="text-xs font-mono font-semibold" style={{ color: 'var(--text-primary)' }}>
                {def.permanence}
              </span>
            </div>
          </div>

          {/* Position */}
          <div className="px-4 py-3" style={{ borderBottom: '1px solid var(--border)' }}>
            <div className="mb-2 text-[10px] font-medium uppercase tracking-wider" style={{ color: 'var(--text-secondary)' }}>
              Position & Rotation
            </div>
            <div className="grid grid-cols-3 gap-2">
              <div>
                <label className="mb-1 block text-[9px]" style={{ color: 'var(--text-secondary)' }}>X (ft)</label>
                <input
                  type="number"
                  value={Math.round(selectedElement.x)}
                  onChange={(e) => {
                    pushHistory('Move');
                    updateElement(selectedElement.instanceId, { x: Number(e.target.value) });
                  }}
                  className="w-full rounded-md px-2 py-1 text-xs outline-none"
                  style={{
                    background: 'var(--bg-elevated)',
                    border: '1px solid var(--border)',
                    color: 'var(--text-primary)',
                  }}
                />
              </div>
              <div>
                <label className="mb-1 block text-[9px]" style={{ color: 'var(--text-secondary)' }}>Y (ft)</label>
                <input
                  type="number"
                  value={Math.round(selectedElement.y)}
                  onChange={(e) => {
                    pushHistory('Move');
                    updateElement(selectedElement.instanceId, { y: Number(e.target.value) });
                  }}
                  className="w-full rounded-md px-2 py-1 text-xs outline-none"
                  style={{
                    background: 'var(--bg-elevated)',
                    border: '1px solid var(--border)',
                    color: 'var(--text-primary)',
                  }}
                />
              </div>
              <div>
                <label className="mb-1 block text-[9px]" style={{ color: 'var(--text-secondary)' }}>Rotation</label>
                <input
                  type="number"
                  value={Math.round(selectedElement.rotation)}
                  onChange={(e) => {
                    pushHistory('Rotate');
                    updateElement(selectedElement.instanceId, {
                      rotation: Number(e.target.value) % 360,
                    });
                  }}
                  className="w-full rounded-md px-2 py-1 text-xs outline-none"
                  style={{
                    background: 'var(--bg-elevated)',
                    border: '1px solid var(--border)',
                    color: 'var(--text-primary)',
                  }}
                />
              </div>
            </div>
          </div>

          {/* Notes */}
          <div className="px-4 py-3" style={{ borderBottom: '1px solid var(--border)' }}>
            <div className="mb-2 text-[10px] font-medium uppercase tracking-wider" style={{ color: 'var(--text-secondary)' }}>
              Custom Notes
            </div>
            <textarea
              value={selectedElement.customNotes}
              onChange={(e) =>
                updateElement(selectedElement.instanceId, { customNotes: e.target.value })
              }
              placeholder="Add notes about this element..."
              rows={3}
              className="w-full resize-none rounded-md px-3 py-2 text-xs leading-relaxed outline-none"
              style={{
                background: 'var(--bg-elevated)',
                border: '1px solid var(--border)',
                color: 'var(--text-primary)',
              }}
            />
          </div>
        </>
      )}

      {/* Actions */}
      <div className="mt-auto px-4 py-3 space-y-2">
        <div className="flex gap-2">
          <button
            onClick={() => {
              pushHistory('Rotate');
              rotateElements(selectedElementIds, 45);
            }}
            className="flex flex-1 cursor-pointer items-center justify-center gap-1.5 rounded-lg py-2 text-xs font-medium transition-colors duration-150 hover:bg-white/10"
            style={{ background: 'var(--bg-elevated)', border: '1px solid var(--border)', color: 'var(--text-primary)' }}
          >
            <RotateCw size={12} />
            Rotate
          </button>
          <button
            onClick={() => duplicateElements(selectedElementIds)}
            className="flex flex-1 cursor-pointer items-center justify-center gap-1.5 rounded-lg py-2 text-xs font-medium transition-colors duration-150 hover:bg-white/10"
            style={{ background: 'var(--bg-elevated)', border: '1px solid var(--border)', color: 'var(--text-primary)' }}
          >
            <Copy size={12} />
            Duplicate
          </button>
        </div>
        <div className="flex gap-2">
          <button
            onClick={() =>
              lockElements(selectedElementIds, !selectedElement?.locked)
            }
            className="flex flex-1 cursor-pointer items-center justify-center gap-1.5 rounded-lg py-2 text-xs font-medium transition-colors duration-150 hover:bg-white/10"
            style={{ background: 'var(--bg-elevated)', border: '1px solid var(--border)', color: 'var(--text-primary)' }}
          >
            {selectedElement?.locked ? <Unlock size={12} /> : <Lock size={12} />}
            {selectedElement?.locked ? 'Unlock' : 'Lock'}
          </button>
          <button
            onClick={() => removeElements(selectedElementIds)}
            className="flex flex-1 cursor-pointer items-center justify-center gap-1.5 rounded-lg py-2 text-xs font-medium transition-colors duration-150 hover:bg-white/10"
            style={{
              background: 'rgba(239,68,68,0.1)',
              border: '1px solid rgba(239,68,68,0.2)',
              color: 'var(--accent-red)',
            }}
          >
            <Trash2 size={12} />
            Delete
          </button>
        </div>
      </div>
    </div>
  );
}

// ---------------------------------------------------------------------------
// CostTicker (floating bottom-right)
// ---------------------------------------------------------------------------

function CostTicker() {
  const design = useStudioStore((s) => s.design);

  const totals = design.elements.reduce(
    (acc, el) => {
      const def = getElementDef(el.elementId);
      if (!def) return acc;
      acc.low += def.costLow;
      acc.high += def.costHigh;
      acc.permCount += def.permits.length;
      acc.permanenceSum += def.permanence;
      return acc;
    },
    { low: 0, high: 0, permCount: 0, permanenceSum: 0 }
  );

  const avgPermanence =
    design.elements.length > 0
      ? Math.round(totals.permanenceSum / design.elements.length)
      : 0;

  if (design.elements.length === 0) return null;

  return (
    <div
      className="animate-scale-in rounded-xl p-4 space-y-3"
      style={{
        background: 'var(--bg-surface)',
        border: '1px solid var(--border)',
        minWidth: '220px',
      }}
    >
      {/* Cost range */}
      <div>
        <div className="mb-1 flex items-center gap-1.5 text-[10px] font-medium uppercase tracking-wider" style={{ color: 'var(--text-secondary)' }}>
          <DollarSign size={10} />
          Estimated Budget
        </div>
        <div className="text-lg font-bold" style={{ color: 'var(--text-primary)' }}>
          ${totals.low.toLocaleString()} - ${totals.high.toLocaleString()}
        </div>
      </div>

      <div className="h-px" style={{ background: 'var(--border)' }} />

      {/* Stats */}
      <div className="grid grid-cols-3 gap-3">
        <div>
          <div className="text-[10px]" style={{ color: 'var(--text-secondary)' }}>Elements</div>
          <div className="text-sm font-semibold" style={{ color: 'var(--text-primary)' }}>
            {design.elements.length}
          </div>
        </div>
        <div>
          <div className="text-[10px]" style={{ color: 'var(--text-secondary)' }}>Permits</div>
          <div className="flex items-center gap-1 text-sm font-semibold" style={{ color: totals.permCount > 0 ? 'var(--accent-amber)' : 'var(--text-primary)' }}>
            {totals.permCount > 0 && <AlertTriangle size={10} />}
            {totals.permCount}
          </div>
        </div>
        <div>
          <div className="text-[10px]" style={{ color: 'var(--text-secondary)' }}>Permanence</div>
          <div className="text-sm font-semibold" style={{
            color: avgPermanence >= 70 ? 'var(--accent-green)' : avgPermanence >= 40 ? 'var(--accent-amber)' : 'var(--text-primary)',
          }}>
            {avgPermanence}%
          </div>
        </div>
      </div>
    </div>
  );
}

// ---------------------------------------------------------------------------
// ParcelSelector (shown when no parcel is loaded)
// ---------------------------------------------------------------------------

function ParcelSelector() {
  const [searchValue, setSearchValue] = useState('');
  const setParcel = useStudioStore((s) => s.setParcel);

  const handleSearch = () => {
    if (!searchValue.trim()) return;
    // Simulate parcel selection with a default rectangle
    setParcel(searchValue.trim(), [
      { x: 0, y: 0 },
      { x: 100, y: 0 },
      { x: 100, y: 60 },
      { x: 0, y: 60 },
    ]);
  };

  return (
    <div
      className="flex items-center gap-3 px-4 py-2"
      style={{ background: 'var(--bg-surface)', borderBottom: '1px solid var(--border)' }}
    >
      <MapPin size={14} style={{ color: 'var(--accent)' }} />
      <span className="text-xs" style={{ color: 'var(--text-secondary)' }}>
        No parcel selected
      </span>
      <div className="flex items-center gap-2">
        <input
          type="text"
          placeholder="Search address or parcel ID..."
          value={searchValue}
          onChange={(e) => setSearchValue(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
          className="rounded-md px-3 py-1 text-xs outline-none"
          style={{
            background: 'var(--bg-elevated)',
            border: '1px solid var(--border)',
            color: 'var(--text-primary)',
            width: '240px',
          }}
        />
        <button
          onClick={handleSearch}
          className="cursor-pointer rounded-md px-3 py-1 text-xs font-medium text-white transition-colors duration-150 hover:brightness-110"
          style={{ background: 'var(--accent)' }}
        >
          Search
        </button>
        <button
          onClick={() => {
            setParcel('custom', [
              { x: 0, y: 0 },
              { x: 120, y: 0 },
              { x: 120, y: 80 },
              { x: 0, y: 80 },
            ]);
          }}
          className="cursor-pointer rounded-md px-3 py-1 text-xs font-medium transition-colors duration-150 hover:bg-white/10"
          style={{
            background: 'var(--bg-elevated)',
            border: '1px solid var(--border)',
            color: 'var(--text-primary)',
          }}
        >
          Choose from map
        </button>
      </div>
    </div>
  );
}

// ---------------------------------------------------------------------------
// Studio Page
// ---------------------------------------------------------------------------

export default function StudioPage() {
  const navigate = useNavigate();
  const { designId } = useParams();
  const {
    design,
    isDirty,
    sidebarOpen,
    detailPanelOpen,
    activeTool,
    gridEnabled,
    selectedElementIds,
    setDesignName,
    setActiveTool,
    toggleGrid,
    toggleSidebar,
    toggleDetailPanel,
    deselectAll,
    removeElements,
    rotateElements,
    undo,
    redo,
    canUndo,
    canRedo,
    cancelPlacing,
    pushHistory,
  } = useStudioStore();

  const [editingName, setEditingName] = useState(false);
  const [nameValue, setNameValue] = useState(design.name);
  const [showExportMenu, setShowExportMenu] = useState(false);

  // Sync name input when design changes
  useEffect(() => {
    setNameValue(design.name);
  }, [design.name]);

  // Keyboard shortcuts
  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      // Don't capture when typing in inputs
      const target = e.target as HTMLElement;
      if (target.tagName === 'INPUT' || target.tagName === 'TEXTAREA') return;

      const isCtrl = e.ctrlKey || e.metaKey;

      if (e.key === 'g' || e.key === 'G') {
        e.preventDefault();
        toggleGrid();
      } else if (e.key === 'r' || e.key === 'R') {
        if (!isCtrl && selectedElementIds.length > 0) {
          e.preventDefault();
          pushHistory('Rotate');
          rotateElements(selectedElementIds, 45);
        }
      } else if (e.key === 'Delete' || e.key === 'Backspace') {
        if (selectedElementIds.length > 0) {
          e.preventDefault();
          removeElements(selectedElementIds);
        }
      } else if (e.key === 's' && isCtrl) {
        e.preventDefault();
        // Save (would call API in production)
      } else if (e.key === 'z' && isCtrl && e.shiftKey) {
        e.preventDefault();
        redo();
      } else if (e.key === 'z' && isCtrl) {
        e.preventDefault();
        undo();
      } else if (e.key === 'Escape') {
        e.preventDefault();
        cancelPlacing();
        deselectAll();
      } else if (e.key === 'Tab') {
        e.preventDefault();
        toggleSidebar();
      }
    };

    window.addEventListener('keydown', handler);
    return () => window.removeEventListener('keydown', handler);
  }, [
    toggleGrid,
    selectedElementIds,
    rotateElements,
    removeElements,
    undo,
    redo,
    cancelPlacing,
    deselectAll,
    toggleSidebar,
    pushHistory,
  ]);

  const handleNameSave = () => {
    setDesignName(nameValue.trim() || 'Untitled Design');
    setEditingName(false);
  };

  return (
    <div className="flex h-screen flex-col" style={{ background: 'var(--bg-primary)' }}>
      {/* ── Top Bar ──────────────────────────────────────────────────────── */}
      <header
        className="relative z-20 flex h-12 shrink-0 items-center justify-between px-3"
        style={{ background: 'var(--bg-surface)', borderBottom: '1px solid var(--border)' }}
      >
        {/* Left section */}
        <div className="flex items-center gap-3">
          {/* Logo */}
          <button
            onClick={() => navigate('/')}
            className="flex h-7 w-7 cursor-pointer items-center justify-center rounded-lg text-xs font-bold transition-transform duration-150 hover:scale-105"
            style={{ background: 'var(--accent)', color: '#fff' }}
          >
            S
          </button>

          {/* Divider */}
          <div className="h-5 w-px" style={{ background: 'var(--border)' }} />

          {/* Design name */}
          {editingName ? (
            <input
              autoFocus
              value={nameValue}
              onChange={(e) => setNameValue(e.target.value)}
              onBlur={handleNameSave}
              onKeyDown={(e) => e.key === 'Enter' && handleNameSave()}
              className="rounded-md px-2 py-1 text-xs font-medium outline-none"
              style={{
                background: 'var(--bg-elevated)',
                border: '1px solid var(--accent)',
                color: 'var(--text-primary)',
                width: '200px',
              }}
            />
          ) : (
            <button
              onClick={() => setEditingName(true)}
              className="flex cursor-pointer items-center gap-1.5 rounded-md px-2 py-1 text-xs font-medium transition-colors duration-150 hover:bg-white/5"
              style={{ color: 'var(--text-primary)' }}
            >
              {design.name}
              {isDirty && (
                <span className="h-1.5 w-1.5 rounded-full" style={{ background: 'var(--accent-amber)' }} />
              )}
            </button>
          )}

          {/* Undo / Redo */}
          <div className="flex items-center gap-0.5">
            <button
              onClick={undo}
              disabled={!canUndo()}
              className="cursor-pointer rounded-md p-1.5 transition-colors duration-150 hover:bg-white/10 disabled:cursor-default disabled:opacity-30"
              title="Undo (Ctrl+Z)"
            >
              <Undo2 size={14} style={{ color: 'var(--text-secondary)' }} />
            </button>
            <button
              onClick={redo}
              disabled={!canRedo()}
              className="cursor-pointer rounded-md p-1.5 transition-colors duration-150 hover:bg-white/10 disabled:cursor-default disabled:opacity-30"
              title="Redo (Ctrl+Shift+Z)"
            >
              <Redo2 size={14} style={{ color: 'var(--text-secondary)' }} />
            </button>
          </div>
        </div>

        {/* Center: tool strip */}
        <div
          className="absolute left-1/2 flex -translate-x-1/2 items-center gap-0.5 rounded-lg p-0.5"
          style={{ background: 'var(--bg-elevated)', border: '1px solid var(--border)' }}
        >
          {(
            [
              { tool: 'select' as const, icon: MousePointer2, label: 'Select (V)' },
              { tool: 'pan' as const, icon: Hand, label: 'Pan (Space)' },
            ] as const
          ).map(({ tool, icon: Icon, label }) => (
            <button
              key={tool}
              onClick={() => setActiveTool(tool)}
              className="cursor-pointer rounded-md p-1.5 transition-colors duration-150"
              style={{
                background: activeTool === tool ? 'var(--accent)' : 'transparent',
                color: activeTool === tool ? '#fff' : 'var(--text-secondary)',
              }}
              title={label}
            >
              <Icon size={14} />
            </button>
          ))}
          <div className="mx-1 h-4 w-px" style={{ background: 'var(--border)' }} />
          <button
            onClick={toggleGrid}
            className="cursor-pointer rounded-md p-1.5 transition-colors duration-150"
            style={{
              background: gridEnabled ? 'rgba(59,130,246,0.15)' : 'transparent',
              color: gridEnabled ? 'var(--accent)' : 'var(--text-secondary)',
            }}
            title="Toggle Grid (G)"
          >
            <Grid3x3 size={14} />
          </button>
        </div>

        {/* Right section */}
        <div className="flex items-center gap-2">
          <button
            className="flex cursor-pointer items-center gap-1.5 rounded-md px-3 py-1.5 text-xs font-medium transition-colors duration-150 hover:bg-white/10"
            style={{
              background: 'var(--bg-elevated)',
              border: '1px solid var(--border)',
              color: 'var(--text-primary)',
            }}
            title="Save (Ctrl+S)"
          >
            <Save size={12} />
            Save
          </button>

          <button
            className="flex cursor-pointer items-center gap-1.5 rounded-md px-3 py-1.5 text-xs font-medium transition-colors duration-150 hover:bg-white/10"
            style={{
              background: 'var(--bg-elevated)',
              border: '1px solid var(--border)',
              color: 'var(--text-primary)',
            }}
          >
            <Share2 size={12} />
            Share
          </button>

          {/* Explore 3D — prominent */}
          <button
            onClick={() => navigate(`/explore/${design.id}`)}
            className="flex cursor-pointer items-center gap-1.5 rounded-lg px-4 py-1.5 text-xs font-semibold text-white transition-all duration-200 hover:brightness-110"
            style={{ background: 'var(--accent)' }}
          >
            <Box size={13} />
            Explore 3D
          </button>

          <button
            className="flex cursor-pointer items-center gap-1.5 rounded-md px-3 py-1.5 text-xs font-medium transition-colors duration-150 hover:bg-white/10"
            style={{
              background: 'var(--bg-elevated)',
              border: '1px solid var(--border)',
              color: 'var(--text-primary)',
            }}
          >
            <Clock size={12} />
            Timeline
          </button>

          {/* Export dropdown */}
          <div className="relative">
            <button
              onClick={() => setShowExportMenu(!showExportMenu)}
              className="flex cursor-pointer items-center gap-1.5 rounded-md px-3 py-1.5 text-xs font-medium transition-colors duration-150 hover:bg-white/10"
              style={{
                background: 'var(--bg-elevated)',
                border: '1px solid var(--border)',
                color: 'var(--text-primary)',
              }}
            >
              <Download size={12} />
              Export
              <ChevronDown size={10} />
            </button>
            {showExportMenu && (
              <>
                <div className="fixed inset-0 z-30" onClick={() => setShowExportMenu(false)} />
                <div
                  className="animate-scale-in absolute right-0 z-40 mt-1 w-44 rounded-lg py-1 shadow-xl"
                  style={{
                    background: 'var(--bg-elevated)',
                    border: '1px solid var(--border)',
                  }}
                >
                  {[
                    { label: 'Export as PDF', icon: FileText },
                    { label: 'Export Budget (CSV)', icon: DollarSign },
                    { label: 'Export Image (PNG)', icon: Download },
                    { label: 'Share Link', icon: Share2 },
                  ].map(({ label, icon: Icon }) => (
                    <button
                      key={label}
                      onClick={() => setShowExportMenu(false)}
                      className="flex w-full cursor-pointer items-center gap-2 px-3 py-2 text-left text-xs transition-colors duration-150 hover:bg-white/5"
                      style={{ color: 'var(--text-primary)' }}
                    >
                      <Icon size={12} style={{ color: 'var(--text-secondary)' }} />
                      {label}
                    </button>
                  ))}
                </div>
              </>
            )}
          </div>

          {/* User avatar */}
          <button
            className="flex h-7 w-7 cursor-pointer items-center justify-center rounded-full transition-opacity duration-150 hover:opacity-80"
            style={{ background: 'var(--bg-elevated)', border: '1px solid var(--border)' }}
          >
            <User size={13} style={{ color: 'var(--text-secondary)' }} />
          </button>
        </div>
      </header>

      {/* ── Parcel selector ──────────────────────────────────────────────── */}
      {!design.parcelId && <ParcelSelector />}

      {/* ── Main content ─────────────────────────────────────────────────── */}
      <div className="relative flex flex-1 overflow-hidden">
        {/* Left sidebar */}
        <aside
          className="relative z-10 flex shrink-0 flex-col transition-all duration-300"
          style={{
            width: sidebarOpen ? '256px' : '0px',
            background: 'var(--bg-surface)',
            borderRight: sidebarOpen ? '1px solid var(--border)' : 'none',
            overflow: 'hidden',
          }}
        >
          <div className="flex h-8 items-center justify-between px-3 py-1" style={{ borderBottom: '1px solid var(--border)' }}>
            <span className="text-[10px] font-semibold uppercase tracking-wider" style={{ color: 'var(--text-secondary)' }}>
              Element Library
            </span>
            <button
              onClick={toggleSidebar}
              className="cursor-pointer rounded p-0.5 transition-colors duration-150 hover:bg-white/10"
            >
              <ChevronLeft size={12} style={{ color: 'var(--text-secondary)' }} />
            </button>
          </div>
          <ElementLibrary />
        </aside>

        {/* Sidebar toggle (collapsed) */}
        {!sidebarOpen && (
          <button
            onClick={toggleSidebar}
            className="absolute top-2 left-2 z-10 flex h-8 w-8 cursor-pointer items-center justify-center rounded-lg transition-colors duration-150 hover:bg-white/10"
            style={{
              background: 'var(--bg-surface)',
              border: '1px solid var(--border)',
            }}
          >
            <ChevronRight size={14} style={{ color: 'var(--text-secondary)' }} />
          </button>
        )}

        {/* Canvas */}
        <main className="relative flex-1">
          <Canvas />

          {/* Cost ticker — floating bottom-right */}
          <div className="absolute right-4 bottom-4 z-10">
            <CostTicker />
          </div>
        </main>

        {/* Right detail panel */}
        <aside
          className="relative z-10 flex shrink-0 flex-col transition-all duration-300"
          style={{
            width: detailPanelOpen ? '320px' : '0px',
            background: 'var(--bg-surface)',
            borderLeft: detailPanelOpen ? '1px solid var(--border)' : 'none',
            overflow: 'hidden',
          }}
        >
          <div className="flex h-8 items-center justify-between px-4 py-1" style={{ borderBottom: '1px solid var(--border)' }}>
            <span className="text-[10px] font-semibold uppercase tracking-wider" style={{ color: 'var(--text-secondary)' }}>
              Details
            </span>
            <button
              onClick={toggleDetailPanel}
              className="cursor-pointer rounded p-0.5 transition-colors duration-150 hover:bg-white/10"
            >
              <ChevronRight size={12} style={{ color: 'var(--text-secondary)' }} />
            </button>
          </div>
          <DetailPanel />
        </aside>
      </div>

      {/* ── Keyboard shortcut hint ───────────────────────────────────────── */}
      <div
        className="flex h-6 shrink-0 items-center justify-center gap-4 text-[10px]"
        style={{
          background: 'var(--bg-surface)',
          borderTop: '1px solid var(--border)',
          color: 'var(--text-secondary)',
        }}
      >
        <span><kbd className="font-mono">G</kbd> Grid</span>
        <span><kbd className="font-mono">R</kbd> Rotate</span>
        <span><kbd className="font-mono">Del</kbd> Remove</span>
        <span><kbd className="font-mono">Ctrl+Z</kbd> Undo</span>
        <span><kbd className="font-mono">Ctrl+Shift+Z</kbd> Redo</span>
        <span><kbd className="font-mono">Esc</kbd> Deselect</span>
        <span><kbd className="font-mono">Tab</kbd> Toggle Sidebar</span>
      </div>
    </div>
  );
}
