/**
 * SPHERES Studio — Community Gallery
 *
 * Browsable grid of public activation designs with filtering, sorting,
 * search, voting, forking, and a featured/trending hero section.
 */

import { useCallback, useEffect, useRef, useState } from 'react';
import { useAuth } from '../context/AuthContext';

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

interface GalleryDesign {
  id: string;
  title: string;
  author_id: string;
  author_name: string;
  parcel_id: string | null;
  parcel_name: string | null;
  thumbnail_color: string;
  element_count: number;
  permanence_score: number;
  vote_count: number;
  comment_count: number;
  tags: string[];
  activation_type: string | null;
  neighborhood: string | null;
  created_at: string;
  is_featured: boolean;
}

interface GalleryPage {
  designs: GalleryDesign[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

type SortOrder = 'newest' | 'most_voted' | 'trending' | 'highest_permanence';

interface GalleryViewProps {
  onOpenDesign?: (designId: string) => void;
  onOpenShare?: (designId: string) => void;
  onOpenComments?: (designId: string) => void;
  onOpenAuth?: () => void;
}

// ---------------------------------------------------------------------------
// Constants
// ---------------------------------------------------------------------------

const SORT_OPTIONS: { value: SortOrder; label: string }[] = [
  { value: 'newest', label: 'Newest' },
  { value: 'most_voted', label: 'Most Voted' },
  { value: 'trending', label: 'Trending' },
  { value: 'highest_permanence', label: 'Highest Permanence' },
];

const ACTIVATION_TYPES = [
  { value: '', label: 'All Types' },
  { value: 'single_day', label: 'Single Day' },
  { value: 'weekend', label: 'Weekend' },
  { value: 'week', label: 'Week' },
  { value: 'month', label: 'Month' },
  { value: 'ongoing', label: 'Ongoing' },
];

const NEIGHBORHOODS = [
  '', 'Center City', 'Fishtown', 'Kensington', 'West Philadelphia',
  'South Philadelphia', 'Northern Liberties', 'Germantown',
  'Manayunk', 'Old City', 'University City',
];

const PAGE_SIZE = 12;

// ---------------------------------------------------------------------------
// Helper: format relative time
// ---------------------------------------------------------------------------

function timeAgo(dateStr: string): string {
  const seconds = Math.floor(
    (Date.now() - new Date(dateStr).getTime()) / 1000,
  );
  if (seconds < 60) return 'just now';
  const minutes = Math.floor(seconds / 60);
  if (minutes < 60) return `${minutes}m ago`;
  const hours = Math.floor(minutes / 60);
  if (hours < 24) return `${hours}h ago`;
  const days = Math.floor(hours / 24);
  if (days < 30) return `${days}d ago`;
  const months = Math.floor(days / 30);
  return `${months}mo ago`;
}

// ---------------------------------------------------------------------------
// Component
// ---------------------------------------------------------------------------

export default function GalleryView({
  onOpenDesign,
  onOpenShare,
  onOpenComments,
  onOpenAuth,
}: GalleryViewProps) {
  const { token, isAuthenticated } = useAuth();

  // Gallery state
  const [designs, setDesigns] = useState<GalleryDesign[]>([]);
  const [featured, setFeatured] = useState<GalleryDesign[]>([]);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);

  // Filters
  const [sort, setSort] = useState<SortOrder>('trending');
  const [activationType, setActivationType] = useState('');
  const [neighborhood, setNeighborhood] = useState('');
  const [search, setSearch] = useState('');
  const [searchInput, setSearchInput] = useState('');

  // Votes cache (design_id -> user_has_voted)
  const [votedMap, setVotedMap] = useState<Record<string, boolean>>({});
  const [voteCountMap, setVoteCountMap] = useState<Record<string, number>>({});

  // Sentinel ref for infinite scroll
  const sentinelRef = useRef<HTMLDivElement | null>(null);

  // ----- Fetch featured -----
  useEffect(() => {
    (async () => {
      try {
        const res = await fetch('/api/gallery/featured');
        if (res.ok) {
          const data: GalleryDesign[] = await res.json();
          setFeatured(data);
        }
      } catch {
        // non-critical
      }
    })();
  }, []);

  // ----- Fetch gallery page -----
  const fetchPage = useCallback(
    async (pageNum: number, append: boolean) => {
      setLoading(true);
      try {
        const params = new URLSearchParams({
          page: String(pageNum),
          page_size: String(PAGE_SIZE),
          sort,
        });
        if (activationType) params.set('activation_type', activationType);
        if (neighborhood) params.set('neighborhood', neighborhood);
        if (search) params.set('search', search);

        const res = await fetch(`/api/gallery?${params.toString()}`);
        if (!res.ok) throw new Error('Failed to fetch gallery');
        const data: GalleryPage = await res.json();

        setDesigns((prev) => (append ? [...prev, ...data.designs] : data.designs));
        setTotalPages(data.total_pages);
        setTotal(data.total);
        setPage(data.page);

        // Initialise vote counts from response
        const newCounts: Record<string, number> = {};
        for (const d of data.designs) {
          newCounts[d.id] = d.vote_count;
        }
        setVoteCountMap((prev) => ({ ...prev, ...newCounts }));
      } catch {
        // error handling left to toast/snackbar layer
      } finally {
        setLoading(false);
      }
    },
    [sort, activationType, neighborhood, search],
  );

  // Reset and fetch page 1 when filters change
  useEffect(() => {
    setDesigns([]);
    setPage(1);
    fetchPage(1, false);
  }, [fetchPage]);

  // ----- Infinite scroll via IntersectionObserver -----
  useEffect(() => {
    const el = sentinelRef.current;
    if (!el) return;

    const observer = new IntersectionObserver(
      (entries) => {
        if (entries[0].isIntersecting && !loading && page < totalPages) {
          fetchPage(page + 1, true);
        }
      },
      { rootMargin: '200px' },
    );
    observer.observe(el);
    return () => observer.disconnect();
  }, [loading, page, totalPages, fetchPage]);

  // ----- Search debounce -----
  useEffect(() => {
    const timer = setTimeout(() => setSearch(searchInput), 350);
    return () => clearTimeout(timer);
  }, [searchInput]);

  // ----- Voting -----
  const handleVote = useCallback(
    async (designId: string) => {
      if (!isAuthenticated) {
        onOpenAuth?.();
        return;
      }
      try {
        const res = await fetch(`/api/designs/${designId}/vote`, {
          method: 'POST',
          headers: { Authorization: `Bearer ${token}` },
        });
        if (res.ok) {
          const data = await res.json();
          setVotedMap((prev) => ({ ...prev, [designId]: data.user_has_voted }));
          setVoteCountMap((prev) => ({ ...prev, [designId]: data.vote_count }));
        }
      } catch {
        // silent
      }
    },
    [isAuthenticated, token, onOpenAuth],
  );

  // ----- Fork -----
  const handleFork = useCallback(
    async (designId: string) => {
      if (!isAuthenticated) {
        onOpenAuth?.();
        return;
      }
      try {
        const res = await fetch(`/api/designs/${designId}/fork`, {
          method: 'POST',
          headers: {
            Authorization: `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({}),
        });
        if (res.ok) {
          // Refresh gallery
          fetchPage(1, false);
        }
      } catch {
        // silent
      }
    },
    [isAuthenticated, token, onOpenAuth, fetchPage],
  );

  // ----- Render -----

  return (
    <div style={styles.container}>
      {/* ── Header ──────────────────────────────────────────────── */}
      <div style={styles.header}>
        <div>
          <h1 style={styles.heading}>Community Gallery</h1>
          <p style={styles.headingSub}>
            {total} activation design{total !== 1 ? 's' : ''} shared by the SPHERES community
          </p>
        </div>
      </div>

      {/* ── Featured section ────────────────────────────────────── */}
      {featured.length > 0 && (
        <div style={styles.featuredSection}>
          <h2 style={styles.sectionTitle}>Featured Designs</h2>
          <div style={styles.featuredRow}>
            {featured.map((d) => (
              <div
                key={d.id}
                style={styles.featuredCard}
                onClick={() => onOpenDesign?.(d.id)}
              >
                <div
                  style={{
                    ...styles.featuredThumb,
                    backgroundColor: d.thumbnail_color,
                  }}
                >
                  <span style={styles.featuredBadge}>Featured</span>
                  <span style={styles.featuredTitle}>{d.title}</span>
                </div>
                <div style={styles.featuredMeta}>
                  <span>{d.author_name}</span>
                  <span style={styles.dot}>*</span>
                  <span>{d.vote_count} votes</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* ── Filter bar ──────────────────────────────────────────── */}
      <div style={styles.filterBar}>
        <input
          type="text"
          placeholder="Search designs..."
          value={searchInput}
          onChange={(e) => setSearchInput(e.target.value)}
          style={styles.searchInput}
        />

        <select
          value={sort}
          onChange={(e) => setSort(e.target.value as SortOrder)}
          style={styles.select}
        >
          {SORT_OPTIONS.map((o) => (
            <option key={o.value} value={o.value}>
              {o.label}
            </option>
          ))}
        </select>

        <select
          value={activationType}
          onChange={(e) => setActivationType(e.target.value)}
          style={styles.select}
        >
          {ACTIVATION_TYPES.map((o) => (
            <option key={o.value} value={o.value}>
              {o.label}
            </option>
          ))}
        </select>

        <select
          value={neighborhood}
          onChange={(e) => setNeighborhood(e.target.value)}
          style={styles.select}
        >
          <option value="">All Neighborhoods</option>
          {NEIGHBORHOODS.filter(Boolean).map((n) => (
            <option key={n} value={n}>
              {n}
            </option>
          ))}
        </select>
      </div>

      {/* ── Grid ────────────────────────────────────────────────── */}
      <div style={styles.grid}>
        {designs.map((d) => {
          const votes = voteCountMap[d.id] ?? d.vote_count;
          const voted = votedMap[d.id] ?? false;
          return (
            <div key={d.id} style={styles.card}>
              {/* Thumbnail */}
              <div
                style={{
                  ...styles.cardThumb,
                  backgroundColor: d.thumbnail_color,
                }}
                onClick={() => onOpenDesign?.(d.id)}
              >
                <div style={styles.thumbOverlay}>
                  <span style={styles.thumbElements}>
                    {d.element_count} element{d.element_count !== 1 ? 's' : ''}
                  </span>
                  <span style={styles.thumbPermanence}>
                    P{d.permanence_score}
                  </span>
                </div>
              </div>

              {/* Body */}
              <div style={styles.cardBody}>
                <h3
                  style={styles.cardTitle}
                  onClick={() => onOpenDesign?.(d.id)}
                >
                  {d.title}
                </h3>
                <div style={styles.cardAuthor}>
                  <span>{d.author_name}</span>
                  <span style={styles.dot}>*</span>
                  <span style={styles.cardTime}>{timeAgo(d.created_at)}</span>
                </div>
                {d.neighborhood && (
                  <div style={styles.cardLocation}>
                    {d.neighborhood}
                    {d.parcel_name ? ` - ${d.parcel_name}` : ''}
                  </div>
                )}

                {/* Tags */}
                {d.tags.length > 0 && (
                  <div style={styles.tagsRow}>
                    {d.tags.slice(0, 4).map((t) => (
                      <span key={t} style={styles.tag}>
                        {t}
                      </span>
                    ))}
                    {d.tags.length > 4 && (
                      <span style={styles.tag}>+{d.tags.length - 4}</span>
                    )}
                  </div>
                )}

                {/* Actions row */}
                <div style={styles.actionsRow}>
                  <button
                    style={{
                      ...styles.actionBtn,
                      color: voted ? '#EF4444' : '#9CA3AF',
                    }}
                    onClick={() => handleVote(d.id)}
                    title="Vote"
                  >
                    {voted ? '\u2665' : '\u2661'} {votes}
                  </button>

                  <button
                    style={styles.actionBtn}
                    onClick={() => onOpenComments?.(d.id)}
                    title="Comments"
                  >
                    {'\uD83D\uDCAC'} {d.comment_count}
                  </button>

                  <button
                    style={styles.actionBtn}
                    onClick={() => handleFork(d.id)}
                    title="Fork this design"
                  >
                    {'\u2442'} Fork
                  </button>

                  <button
                    style={styles.actionBtn}
                    onClick={() => onOpenShare?.(d.id)}
                    title="Share"
                  >
                    {'\u2197'} Share
                  </button>
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Loading indicator */}
      {loading && (
        <div style={styles.loadingRow}>
          <div style={styles.spinner} />
          <span style={styles.loadingText}>Loading designs...</span>
        </div>
      )}

      {/* Empty state */}
      {!loading && designs.length === 0 && (
        <div style={styles.emptyState}>
          <p style={styles.emptyIcon}>O</p>
          <p style={styles.emptyTitle}>No designs found</p>
          <p style={styles.emptyText}>
            Try adjusting your filters or search terms.
          </p>
        </div>
      )}

      {/* Infinite scroll sentinel */}
      <div ref={sentinelRef} style={{ height: 1 }} />

      {/* Page info */}
      {!loading && designs.length > 0 && (
        <div style={styles.pageInfo}>
          Showing {designs.length} of {total} designs
          {page < totalPages && ' - scroll for more'}
        </div>
      )}
    </div>
  );
}

// ---------------------------------------------------------------------------
// Styles
// ---------------------------------------------------------------------------

const styles: Record<string, React.CSSProperties> = {
  container: {
    maxWidth: 1200,
    margin: '0 auto',
    padding: '24px 16px',
    fontFamily: 'Inter, system-ui, sans-serif',
    color: '#F9FAFB',
  },
  header: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'flex-end',
    marginBottom: 24,
  },
  heading: {
    margin: 0,
    fontSize: 28,
    fontWeight: 800,
    letterSpacing: '-0.03em',
  },
  headingSub: {
    margin: '4px 0 0',
    fontSize: 14,
    color: '#9CA3AF',
  },

  // Featured
  featuredSection: {
    marginBottom: 32,
  },
  sectionTitle: {
    margin: '0 0 12px',
    fontSize: 16,
    fontWeight: 600,
    color: '#D1D5DB',
  },
  featuredRow: {
    display: 'flex',
    gap: 12,
    overflowX: 'auto' as const,
    paddingBottom: 8,
  },
  featuredCard: {
    minWidth: 220,
    flexShrink: 0,
    cursor: 'pointer',
    borderRadius: 12,
    overflow: 'hidden',
    backgroundColor: '#1F2937',
    border: '1px solid #374151',
    transition: 'transform 0.15s, border-color 0.15s',
  },
  featuredThumb: {
    position: 'relative' as const,
    height: 120,
    display: 'flex',
    flexDirection: 'column' as const,
    justifyContent: 'flex-end',
    padding: 12,
  },
  featuredBadge: {
    position: 'absolute' as const,
    top: 8,
    right: 8,
    backgroundColor: 'rgba(0,0,0,0.5)',
    padding: '2px 8px',
    borderRadius: 8,
    fontSize: 11,
    fontWeight: 600,
    color: '#FCD34D',
  },
  featuredTitle: {
    fontSize: 14,
    fontWeight: 600,
    color: '#fff',
    textShadow: '0 1px 4px rgba(0,0,0,0.5)',
  },
  featuredMeta: {
    padding: '8px 12px',
    fontSize: 12,
    color: '#9CA3AF',
    display: 'flex',
    alignItems: 'center',
    gap: 6,
  },

  // Filter bar
  filterBar: {
    display: 'flex',
    gap: 8,
    marginBottom: 20,
    flexWrap: 'wrap' as const,
  },
  searchInput: {
    flex: '1 1 200px',
    padding: '8px 12px',
    borderRadius: 8,
    border: '1px solid #374151',
    backgroundColor: '#1F2937',
    color: '#F9FAFB',
    fontSize: 14,
    outline: 'none',
  },
  select: {
    padding: '8px 12px',
    borderRadius: 8,
    border: '1px solid #374151',
    backgroundColor: '#1F2937',
    color: '#F9FAFB',
    fontSize: 13,
    outline: 'none',
    cursor: 'pointer',
  },

  // Grid
  grid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))',
    gap: 16,
  },
  card: {
    borderRadius: 12,
    overflow: 'hidden',
    backgroundColor: '#111827',
    border: '1px solid #1F2937',
    transition: 'border-color 0.15s, transform 0.15s',
  },
  cardThumb: {
    position: 'relative' as const,
    height: 140,
    cursor: 'pointer',
    display: 'flex',
    alignItems: 'flex-end',
    padding: 10,
  },
  thumbOverlay: {
    display: 'flex',
    justifyContent: 'space-between',
    width: '100%',
  },
  thumbElements: {
    backgroundColor: 'rgba(0,0,0,0.55)',
    padding: '3px 8px',
    borderRadius: 6,
    fontSize: 11,
    fontWeight: 600,
    color: '#E5E7EB',
  },
  thumbPermanence: {
    backgroundColor: 'rgba(0,0,0,0.55)',
    padding: '3px 8px',
    borderRadius: 6,
    fontSize: 11,
    fontWeight: 700,
    color: '#22C55E',
  },
  cardBody: {
    padding: '12px 14px 14px',
  },
  cardTitle: {
    margin: 0,
    fontSize: 15,
    fontWeight: 600,
    cursor: 'pointer',
    lineHeight: 1.3,
  },
  cardAuthor: {
    marginTop: 4,
    fontSize: 12,
    color: '#9CA3AF',
    display: 'flex',
    alignItems: 'center',
    gap: 6,
  },
  dot: {
    color: '#4B5563',
    fontSize: 8,
  },
  cardTime: {
    color: '#6B7280',
  },
  cardLocation: {
    marginTop: 4,
    fontSize: 12,
    color: '#6B7280',
  },
  tagsRow: {
    display: 'flex',
    flexWrap: 'wrap' as const,
    gap: 4,
    marginTop: 8,
  },
  tag: {
    padding: '2px 8px',
    borderRadius: 6,
    backgroundColor: '#1F2937',
    border: '1px solid #374151',
    fontSize: 11,
    color: '#9CA3AF',
    fontWeight: 500,
  },
  actionsRow: {
    display: 'flex',
    gap: 4,
    marginTop: 10,
    borderTop: '1px solid #1F2937',
    paddingTop: 10,
  },
  actionBtn: {
    flex: 1,
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 4,
    padding: '6px 0',
    background: 'none',
    border: 'none',
    color: '#9CA3AF',
    fontSize: 12,
    fontWeight: 500,
    cursor: 'pointer',
    borderRadius: 6,
    transition: 'color 0.15s, background-color 0.15s',
  },

  // Loading
  loadingRow: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 10,
    padding: '32px 0',
  },
  spinner: {
    width: 20,
    height: 20,
    border: '2px solid #374151',
    borderTopColor: '#6D28D9',
    borderRadius: '50%',
    animation: 'spin 0.8s linear infinite',
  },
  loadingText: {
    fontSize: 14,
    color: '#9CA3AF',
  },

  // Empty state
  emptyState: {
    textAlign: 'center' as const,
    padding: '64px 16px',
  },
  emptyIcon: {
    fontSize: 48,
    margin: 0,
    color: '#374151',
  },
  emptyTitle: {
    fontSize: 18,
    fontWeight: 600,
    color: '#D1D5DB',
    margin: '12px 0 4px',
  },
  emptyText: {
    fontSize: 14,
    color: '#6B7280',
    margin: 0,
  },

  // Page info
  pageInfo: {
    textAlign: 'center' as const,
    padding: '16px 0 32px',
    fontSize: 13,
    color: '#6B7280',
  },
};
