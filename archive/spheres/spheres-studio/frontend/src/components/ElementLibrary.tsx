/**
 * SPHERES Studio — Element Library Sidebar
 *
 * Collapsible accordion of draggable activation elements grouped by category.
 * Supports search/filter, favorites (persisted to localStorage), and
 * drag-to-canvas via the HTML Drag-and-Drop API.
 */

import React, { useMemo, useState, useCallback, useEffect } from "react";
import {
  Search,
  Star,
  ChevronDown,
  ChevronRight,
  GripVertical,
  Mic,
  Mic2,
  Music,
  Speaker,
  Monitor,
  Armchair,
  Rows3,
  ShoppingCart,
  Truck,
  Store,
  Tent,
  Sprout,
  TreePine,
  Flower2,
  Leaf,
  Droplets,
  Droplet,
  Paintbrush,
  Hexagon,
  Hand,
  Palette,
  Baby,
  CircleDot,
  Dumbbell,
  Trophy,
  Route,
  Fence,
  Lamp,
  Plug,
  Umbrella,
  SignpostBig,
  type LucideIcon,
} from "lucide-react";
import type { ElementDefinition } from "../utils/canvasRenderer";

// ---------------------------------------------------------------------------
// Icon mapping from string name to Lucide component
// ---------------------------------------------------------------------------

const ICON_MAP: Record<string, LucideIcon> = {
  mic: Mic,
  "mic-2": Mic2,
  music: Music,
  speaker: Speaker,
  monitor: Monitor,
  armchair: Armchair,
  table: Rows3, // closest available
  sofa: Armchair,
  "rows-3": Rows3,
  theater: Rows3,
  "shopping-cart": ShoppingCart,
  truck: Truck,
  store: Store,
  tent: Tent,
  sprout: Sprout,
  "tree-pine": TreePine,
  "flower-2": Flower2,
  leaf: Leaf,
  droplets: Droplets,
  droplet: Droplet,
  paintbrush: Paintbrush,
  hexagon: Hexagon,
  hand: Hand,
  palette: Palette,
  baby: Baby,
  "circle-dot": CircleDot,
  dumbbell: Dumbbell,
  trophy: Trophy,
  route: Route,
  fence: Fence,
  lamp: Lamp,
  plug: Plug,
  umbrella: Umbrella,
  "sign-post": SignpostBig,
};

function getIcon(name: string): LucideIcon {
  return ICON_MAP[name] ?? Hexagon;
}

// ---------------------------------------------------------------------------
// Category display metadata
// ---------------------------------------------------------------------------

const CATEGORY_LABELS: Record<string, string> = {
  performance: "Performance",
  seating: "Seating",
  food_vendor: "Food & Vendor",
  gardens_nature: "Gardens & Nature",
  art: "Art",
  recreation: "Recreation",
  infrastructure: "Infrastructure",
};

const CATEGORY_ORDER = [
  "performance",
  "seating",
  "food_vendor",
  "gardens_nature",
  "art",
  "recreation",
  "infrastructure",
];

// ---------------------------------------------------------------------------
// Persistence helpers
// ---------------------------------------------------------------------------

const FAVORITES_KEY = "spheres-studio:favorites";

function loadFavorites(): Set<string> {
  try {
    const raw = localStorage.getItem(FAVORITES_KEY);
    if (raw) return new Set(JSON.parse(raw) as string[]);
  } catch {
    /* ignore */
  }
  return new Set();
}

function saveFavorites(favs: Set<string>): void {
  localStorage.setItem(FAVORITES_KEY, JSON.stringify([...favs]));
}

// ---------------------------------------------------------------------------
// Format helpers
// ---------------------------------------------------------------------------

function formatCost(low: number, high: number): string {
  const fmt = (n: number) =>
    n >= 1000 ? `$${(n / 1000).toFixed(n % 1000 === 0 ? 0 : 1)}k` : `$${n}`;
  return `${fmt(low)}\u2013${fmt(high)}`;
}

// ---------------------------------------------------------------------------
// Component props
// ---------------------------------------------------------------------------

interface ElementLibraryProps {
  elements: ElementDefinition[];
  onDragStart?: (elementDef: ElementDefinition) => void;
}

// ---------------------------------------------------------------------------
// Single element card
// ---------------------------------------------------------------------------

interface ElementCardProps {
  def: ElementDefinition;
  isFavorite: boolean;
  onToggleFavorite: (id: string) => void;
  onDragStart?: (def: ElementDefinition) => void;
}

const ElementCard: React.FC<ElementCardProps> = React.memo(
  ({ def, isFavorite, onToggleFavorite, onDragStart }) => {
    const Icon = getIcon(def.icon);

    const handleDragStart = useCallback(
      (e: React.DragEvent) => {
        e.dataTransfer.setData("application/spheres-element", def.id);
        e.dataTransfer.effectAllowed = "copy";
        onDragStart?.(def);
      },
      [def, onDragStart],
    );

    return (
      <div
        draggable
        onDragStart={handleDragStart}
        className="group flex items-center gap-2.5 rounded-lg border border-white/[0.06] bg-white/[0.03] px-2.5 py-2 cursor-grab active:cursor-grabbing hover:bg-white/[0.07] hover:border-white/[0.12] transition-colors"
      >
        {/* Drag grip */}
        <GripVertical className="w-3.5 h-3.5 text-white/20 group-hover:text-white/40 shrink-0" />

        {/* Icon */}
        <div
          className="w-8 h-8 rounded-md flex items-center justify-center shrink-0"
          style={{ backgroundColor: def.color + "30" }}
        >
          <Icon className="w-4 h-4" style={{ color: def.color }} />
        </div>

        {/* Info */}
        <div className="flex-1 min-w-0">
          <div className="text-[13px] font-medium text-white/90 truncate leading-tight">
            {def.name}
          </div>
          <div className="flex items-center gap-1.5 mt-0.5">
            <span className="text-[11px] text-white/40">
              {def.footprint_width}&times;{def.footprint_height} ft
            </span>
            <span className="text-[11px] text-white/25">&middot;</span>
            <span className="text-[11px] text-white/40">
              {formatCost(def.cost_estimate.low, def.cost_estimate.high)}
            </span>
          </div>
        </div>

        {/* Favorite toggle */}
        <button
          onClick={(e) => {
            e.stopPropagation();
            onToggleFavorite(def.id);
          }}
          className="shrink-0 p-1 rounded hover:bg-white/10 transition-colors"
          title={isFavorite ? "Remove from favorites" : "Add to favorites"}
        >
          <Star
            className="w-3.5 h-3.5"
            fill={isFavorite ? "#FBBF24" : "none"}
            stroke={isFavorite ? "#FBBF24" : "rgba(255,255,255,0.25)"}
          />
        </button>
      </div>
    );
  },
);
ElementCard.displayName = "ElementCard";

// ---------------------------------------------------------------------------
// Main component
// ---------------------------------------------------------------------------

const ElementLibrary: React.FC<ElementLibraryProps> = ({
  elements,
  onDragStart,
}) => {
  const [searchQuery, setSearchQuery] = useState("");
  const [expandedCategories, setExpandedCategories] = useState<Set<string>>(
    () => new Set(CATEGORY_ORDER),
  );
  const [favorites, setFavorites] = useState<Set<string>>(loadFavorites);
  const [showFavoritesOnly, setShowFavoritesOnly] = useState(false);

  // Persist favourites
  useEffect(() => {
    saveFavorites(favorites);
  }, [favorites]);

  const toggleCategory = useCallback((cat: string) => {
    setExpandedCategories((prev) => {
      const next = new Set(prev);
      if (next.has(cat)) next.delete(cat);
      else next.add(cat);
      return next;
    });
  }, []);

  const toggleFavorite = useCallback((id: string) => {
    setFavorites((prev) => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return next;
    });
  }, []);

  // Filter + group
  const grouped = useMemo(() => {
    const q = searchQuery.toLowerCase().trim();
    let filtered = elements;

    if (showFavoritesOnly) {
      filtered = filtered.filter((e) => favorites.has(e.id));
    }

    if (q) {
      filtered = filtered.filter(
        (e) =>
          e.name.toLowerCase().includes(q) ||
          e.category.toLowerCase().includes(q) ||
          e.description.toLowerCase().includes(q),
      );
    }

    const map = new Map<string, ElementDefinition[]>();
    for (const cat of CATEGORY_ORDER) {
      const items = filtered.filter((e) => e.category === cat);
      if (items.length > 0) map.set(cat, items);
    }
    return map;
  }, [elements, searchQuery, showFavoritesOnly, favorites]);

  return (
    <div className="flex flex-col h-full">
      {/* Header */}
      <div className="px-4 pt-4 pb-2">
        <h2 className="text-sm font-semibold text-white/80 uppercase tracking-wider">
          Element Library
        </h2>

        {/* Search */}
        <div className="relative mt-3">
          <Search className="absolute left-2.5 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-white/30" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search elements..."
            className="w-full bg-white/[0.06] border border-white/[0.08] rounded-lg pl-8 pr-3 py-1.5 text-[13px] text-white/90 placeholder:text-white/25 focus:outline-none focus:ring-1 focus:ring-blue-500/50 focus:border-blue-500/30 transition-colors"
          />
        </div>

        {/* Favorites toggle */}
        <button
          onClick={() => setShowFavoritesOnly((v) => !v)}
          className={`mt-2 flex items-center gap-1.5 px-2.5 py-1 rounded-md text-[12px] transition-colors ${
            showFavoritesOnly
              ? "bg-amber-500/20 text-amber-300"
              : "bg-white/[0.04] text-white/40 hover:bg-white/[0.08]"
          }`}
        >
          <Star
            className="w-3 h-3"
            fill={showFavoritesOnly ? "currentColor" : "none"}
          />
          Favorites{favorites.size > 0 ? ` (${favorites.size})` : ""}
        </button>
      </div>

      {/* Category accordion */}
      <div className="flex-1 overflow-y-auto px-3 pb-4 space-y-1 scrollbar-thin">
        {CATEGORY_ORDER.map((cat) => {
          const items = grouped.get(cat);
          if (!items) return null;
          const isExpanded = expandedCategories.has(cat);

          return (
            <div key={cat}>
              {/* Category header */}
              <button
                onClick={() => toggleCategory(cat)}
                className="w-full flex items-center gap-2 px-1.5 py-2 text-left hover:bg-white/[0.04] rounded-md transition-colors"
              >
                {isExpanded ? (
                  <ChevronDown className="w-3.5 h-3.5 text-white/40" />
                ) : (
                  <ChevronRight className="w-3.5 h-3.5 text-white/40" />
                )}
                <span className="text-[12px] font-semibold text-white/60 uppercase tracking-wide">
                  {CATEGORY_LABELS[cat] ?? cat}
                </span>
                <span className="text-[11px] text-white/25 ml-auto">
                  {items.length}
                </span>
              </button>

              {/* Items */}
              {isExpanded && (
                <div className="space-y-1 pb-1">
                  {items.map((def) => (
                    <ElementCard
                      key={def.id}
                      def={def}
                      isFavorite={favorites.has(def.id)}
                      onToggleFavorite={toggleFavorite}
                      onDragStart={onDragStart}
                    />
                  ))}
                </div>
              )}
            </div>
          );
        })}

        {grouped.size === 0 && (
          <div className="text-center text-[13px] text-white/30 py-8">
            {showFavoritesOnly
              ? "No favorites yet. Star elements to see them here."
              : "No elements match your search."}
          </div>
        )}
      </div>
    </div>
  );
};

export default ElementLibrary;
