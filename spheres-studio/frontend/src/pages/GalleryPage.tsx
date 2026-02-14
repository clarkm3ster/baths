/**
 * SPHERES Studio — Gallery Page
 *
 * Community gallery of shared activation designs. Displays a grid of design
 * cards with search, category filtering, and sort controls.
 */

import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import {
  Search,
  ArrowLeft,
  SlidersHorizontal,
  Eye,
  Heart,
  MapPin,
  Layers,
  DollarSign,
  ChevronDown,
  Box,
  Clock,
} from 'lucide-react';

// ---------------------------------------------------------------------------
// Mock gallery data
// ---------------------------------------------------------------------------

interface GalleryDesign {
  id: string;
  name: string;
  author: string;
  location: string;
  elementCount: number;
  costRange: string;
  permanenceScore: number;
  likes: number;
  views: number;
  tags: string[];
  createdAt: string;
  thumbnailGradient: string;
}

const MOCK_DESIGNS: GalleryDesign[] = [
  {
    id: 'g1',
    name: 'Kensington Community Garden',
    author: 'Maria Chen',
    location: 'Kensington, Philadelphia',
    elementCount: 24,
    costRange: '$12K - $35K',
    permanenceScore: 82,
    likes: 47,
    views: 312,
    tags: ['garden', 'community', 'permanent'],
    createdAt: '2 days ago',
    thumbnailGradient: 'linear-gradient(135deg, #22C55E20, #16A34A10)',
  },
  {
    id: 'g2',
    name: 'Fishtown Music Lot',
    author: 'James Wright',
    location: 'Fishtown, Philadelphia',
    elementCount: 18,
    costRange: '$8K - $22K',
    permanenceScore: 35,
    likes: 89,
    views: 567,
    tags: ['performance', 'music', 'temporary'],
    createdAt: '5 days ago',
    thumbnailGradient: 'linear-gradient(135deg, #8B5CF620, #7C3AED10)',
  },
  {
    id: 'g3',
    name: 'Point Breeze Play Park',
    author: 'Aisha Johnson',
    location: 'Point Breeze, Philadelphia',
    elementCount: 31,
    costRange: '$25K - $65K',
    permanenceScore: 91,
    likes: 124,
    views: 893,
    tags: ['recreation', 'kids', 'permanent'],
    createdAt: '1 week ago',
    thumbnailGradient: 'linear-gradient(135deg, #3B82F620, #2563EB10)',
  },
  {
    id: 'g4',
    name: 'Germantown Art Walk',
    author: 'Tyler Brooks',
    location: 'Germantown, Philadelphia',
    elementCount: 15,
    costRange: '$6K - $18K',
    permanenceScore: 55,
    likes: 63,
    views: 421,
    tags: ['art', 'walking', 'mixed'],
    createdAt: '2 weeks ago',
    thumbnailGradient: 'linear-gradient(135deg, #EC489920, #DB277710)',
  },
  {
    id: 'g5',
    name: 'South Philly Food Court',
    author: 'Rosa Martinez',
    location: 'South Philadelphia',
    elementCount: 22,
    costRange: '$4K - $12K',
    permanenceScore: 20,
    likes: 156,
    views: 1203,
    tags: ['food', 'vendor', 'temporary'],
    createdAt: '3 weeks ago',
    thumbnailGradient: 'linear-gradient(135deg, #EF444420, #DC262610)',
  },
  {
    id: 'g6',
    name: 'West Philly Urban Meadow',
    author: 'David Park',
    location: 'West Philadelphia',
    elementCount: 12,
    costRange: '$3K - $10K',
    permanenceScore: 95,
    likes: 78,
    views: 534,
    tags: ['nature', 'environment', 'permanent'],
    createdAt: '1 month ago',
    thumbnailGradient: 'linear-gradient(135deg, #15803D20, #16A34A10)',
  },
  {
    id: 'g7',
    name: 'Temple University Pop-Up',
    author: 'Sam Lee',
    location: 'North Philadelphia',
    elementCount: 19,
    costRange: '$5K - $15K',
    permanenceScore: 25,
    likes: 42,
    views: 287,
    tags: ['performance', 'student', 'temporary'],
    createdAt: '1 month ago',
    thumbnailGradient: 'linear-gradient(135deg, #F59E0B20, #D9770610)',
  },
  {
    id: 'g8',
    name: 'Manayunk Riverwalk',
    author: 'Emma Wilson',
    location: 'Manayunk, Philadelphia',
    elementCount: 28,
    costRange: '$18K - $45K',
    permanenceScore: 78,
    likes: 91,
    views: 645,
    tags: ['infrastructure', 'walkway', 'permanent'],
    createdAt: '2 months ago',
    thumbnailGradient: 'linear-gradient(135deg, #6B728020, #9CA3AF10)',
  },
];

// ---------------------------------------------------------------------------
// Design card
// ---------------------------------------------------------------------------

function DesignCard({ design }: { design: GalleryDesign }) {
  const navigate = useNavigate();

  return (
    <div
      className="group cursor-pointer rounded-xl transition-all duration-300 hover:-translate-y-1 hover:shadow-lg"
      style={{
        background: 'var(--bg-surface)',
        border: '1px solid var(--border)',
      }}
      onClick={() => navigate(`/explore/${design.id}`)}
    >
      {/* Thumbnail placeholder */}
      <div
        className="relative h-44 overflow-hidden rounded-t-xl"
        style={{ background: design.thumbnailGradient }}
      >
        <div className="absolute inset-0 flex items-center justify-center">
          <Layers size={32} className="opacity-20" style={{ color: 'var(--text-secondary)' }} />
        </div>

        {/* Hover overlay */}
        <div
          className="absolute inset-0 flex items-center justify-center opacity-0 transition-opacity duration-300 group-hover:opacity-100"
          style={{ background: 'rgba(0,0,0,0.5)' }}
        >
          <div className="flex items-center gap-2 rounded-lg px-4 py-2 text-xs font-medium text-white" style={{ background: 'var(--accent)' }}>
            <Box size={14} />
            Explore in 3D
          </div>
        </div>

        {/* Stats overlay */}
        <div className="absolute bottom-0 right-0 left-0 flex items-center justify-between px-3 py-2">
          <div className="flex items-center gap-3">
            <span className="flex items-center gap-1 rounded-md px-2 py-0.5 text-[10px] font-medium text-white" style={{ background: 'rgba(0,0,0,0.6)' }}>
              <Eye size={10} /> {design.views}
            </span>
            <span className="flex items-center gap-1 rounded-md px-2 py-0.5 text-[10px] font-medium text-white" style={{ background: 'rgba(0,0,0,0.6)' }}>
              <Heart size={10} /> {design.likes}
            </span>
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="p-4">
        <h3 className="mb-1 text-sm font-semibold" style={{ color: 'var(--text-primary)' }}>
          {design.name}
        </h3>
        <p className="mb-3 flex items-center gap-1 text-[11px]" style={{ color: 'var(--text-secondary)' }}>
          <MapPin size={10} />
          {design.location}
        </p>

        <div className="mb-3 flex items-center gap-3">
          <span className="flex items-center gap-1 text-[11px]" style={{ color: 'var(--text-secondary)' }}>
            <Layers size={10} />
            {design.elementCount} elements
          </span>
          <span className="flex items-center gap-1 text-[11px]" style={{ color: 'var(--accent-green)' }}>
            <DollarSign size={10} />
            {design.costRange}
          </span>
        </div>

        {/* Permanence bar */}
        <div className="mb-3 flex items-center gap-2">
          <div className="h-1 flex-1 overflow-hidden rounded-full" style={{ background: 'var(--bg-elevated)' }}>
            <div
              className="h-full rounded-full"
              style={{
                width: `${design.permanenceScore}%`,
                background:
                  design.permanenceScore >= 70
                    ? 'var(--accent-green)'
                    : design.permanenceScore >= 40
                    ? 'var(--accent-amber)'
                    : 'var(--accent-red)',
              }}
            />
          </div>
          <span className="text-[10px] font-mono" style={{ color: 'var(--text-secondary)' }}>
            {design.permanenceScore}%
          </span>
        </div>

        {/* Tags */}
        <div className="flex flex-wrap gap-1.5">
          {design.tags.map((tag) => (
            <span
              key={tag}
              className="rounded-md px-2 py-0.5 text-[10px]"
              style={{
                background: 'var(--bg-elevated)',
                color: 'var(--text-secondary)',
                border: '1px solid var(--border)',
              }}
            >
              {tag}
            </span>
          ))}
        </div>

        {/* Footer */}
        <div
          className="mt-3 flex items-center justify-between pt-3"
          style={{ borderTop: '1px solid var(--border)' }}
        >
          <span className="text-[11px]" style={{ color: 'var(--text-secondary)' }}>
            by {design.author}
          </span>
          <span className="flex items-center gap-1 text-[10px]" style={{ color: 'var(--text-secondary)' }}>
            <Clock size={9} />
            {design.createdAt}
          </span>
        </div>
      </div>
    </div>
  );
}

// ---------------------------------------------------------------------------
// Gallery Page
// ---------------------------------------------------------------------------

export default function GalleryPage() {
  const [searchQuery, setSearchQuery] = useState('');
  const [sortBy, setSortBy] = useState<'popular' | 'recent' | 'permanence'>('popular');
  const [activeTag, setActiveTag] = useState<string | null>(null);

  const allTags = [...new Set(MOCK_DESIGNS.flatMap((d) => d.tags))];

  let filtered = MOCK_DESIGNS;
  if (searchQuery.trim()) {
    const q = searchQuery.toLowerCase();
    filtered = filtered.filter(
      (d) =>
        d.name.toLowerCase().includes(q) ||
        d.location.toLowerCase().includes(q) ||
        d.author.toLowerCase().includes(q) ||
        d.tags.some((t) => t.includes(q))
    );
  }
  if (activeTag) {
    filtered = filtered.filter((d) => d.tags.includes(activeTag));
  }

  // Sort
  filtered = [...filtered].sort((a, b) => {
    if (sortBy === 'popular') return b.likes - a.likes;
    if (sortBy === 'permanence') return b.permanenceScore - a.permanenceScore;
    return 0; // "recent" keeps original order
  });

  return (
    <div className="h-screen overflow-y-auto" style={{ background: 'var(--bg-primary)' }}>
      {/* Header */}
      <header
        className="glass sticky top-0 z-20 px-6 py-4"
        style={{ borderBottom: '1px solid var(--border)' }}
      >
        <div className="mx-auto flex max-w-6xl items-center justify-between">
          <div className="flex items-center gap-4">
            <Link
              to="/studio"
              className="flex items-center gap-1.5 text-xs font-medium transition-colors duration-200 hover:text-white"
              style={{ color: 'var(--text-secondary)' }}
            >
              <ArrowLeft size={14} />
              Back to Studio
            </Link>
            <div className="h-4 w-px" style={{ background: 'var(--border)' }} />
            <h1 className="text-lg font-bold" style={{ color: 'var(--text-primary)' }}>
              Community Gallery
            </h1>
          </div>

          <div className="flex items-center gap-3">
            {/* Search */}
            <div
              className="flex items-center gap-2 rounded-lg px-3 py-2"
              style={{
                background: 'var(--bg-surface)',
                border: '1px solid var(--border)',
                width: '260px',
              }}
            >
              <Search size={14} style={{ color: 'var(--text-secondary)' }} />
              <input
                type="text"
                placeholder="Search designs, locations, creators..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="flex-1 bg-transparent text-xs outline-none"
                style={{ color: 'var(--text-primary)' }}
              />
            </div>

            {/* Sort */}
            <div className="relative">
              <button
                className="flex items-center gap-1.5 rounded-lg px-3 py-2 text-xs font-medium transition-colors duration-150 hover:bg-white/5"
                style={{
                  background: 'var(--bg-surface)',
                  border: '1px solid var(--border)',
                  color: 'var(--text-primary)',
                }}
              >
                <SlidersHorizontal size={12} />
                {sortBy === 'popular'
                  ? 'Most Popular'
                  : sortBy === 'recent'
                  ? 'Most Recent'
                  : 'Highest Permanence'}
                <ChevronDown size={10} />
              </button>
            </div>
          </div>
        </div>

        {/* Tag filters */}
        <div className="mx-auto mt-3 flex max-w-6xl gap-2">
          <button
            onClick={() => setActiveTag(null)}
            className="cursor-pointer rounded-md px-3 py-1 text-[11px] font-medium transition-colors duration-150"
            style={{
              background: activeTag === null ? 'var(--accent)' : 'var(--bg-surface)',
              color: activeTag === null ? '#fff' : 'var(--text-secondary)',
              border: activeTag === null ? 'none' : '1px solid var(--border)',
            }}
          >
            All
          </button>
          {allTags.map((tag) => (
            <button
              key={tag}
              onClick={() => setActiveTag(activeTag === tag ? null : tag)}
              className="cursor-pointer rounded-md px-3 py-1 text-[11px] font-medium capitalize transition-colors duration-150"
              style={{
                background: activeTag === tag ? 'var(--accent)' : 'var(--bg-surface)',
                color: activeTag === tag ? '#fff' : 'var(--text-secondary)',
                border: activeTag === tag ? 'none' : '1px solid var(--border)',
              }}
            >
              {tag}
            </button>
          ))}
        </div>
      </header>

      {/* Grid */}
      <main className="mx-auto max-w-6xl px-6 py-8">
        {filtered.length === 0 ? (
          <div className="flex flex-col items-center justify-center py-24 text-center">
            <Search size={32} className="mb-4" style={{ color: 'var(--text-secondary)', opacity: 0.3 }} />
            <p className="mb-1 text-sm font-medium" style={{ color: 'var(--text-secondary)' }}>
              No designs found
            </p>
            <p className="text-xs" style={{ color: 'var(--text-secondary)', opacity: 0.6 }}>
              Try a different search term or filter
            </p>
          </div>
        ) : (
          <>
            <p className="mb-6 text-xs" style={{ color: 'var(--text-secondary)' }}>
              {filtered.length} design{filtered.length !== 1 ? 's' : ''} found
            </p>
            <div className="stagger-children grid gap-6 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
              {filtered.map((design) => (
                <DesignCard key={design.id} design={design} />
              ))}
            </div>
          </>
        )}
      </main>
    </div>
  );
}
