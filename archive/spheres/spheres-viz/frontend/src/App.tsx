import { useState, useEffect, useCallback, useRef } from 'react';
import ScrollExperience from './components/ScrollExperience';
import Footer from './components/Footer';
import WorldOverlay from './components/WorldOverlay';
import WorldRenderer from './worlds/WorldRenderer';
import MarbleWorlds from './components/MarbleWorlds';
import { fetchEpisodes, type EpisodeSummary } from './utils/api';

// ---------------------------------------------------------------------------
// App — SPHERES Viz
// ---------------------------------------------------------------------------
// Root component. Fetches episode data, drives the scroll experience, and
// manages the full-screen 3D world overlay. No router — the entire site is a
// single cinematic scroll page with portal-based world pop-outs.
//
// MarbleWorlds: A separate full-screen overlay for browsing all 10
// Marble-generated Gaussian splat worlds with an episode selector sidebar.
// ---------------------------------------------------------------------------

type AppState = 'loading' | 'ready' | 'error';

export default function App() {
  // --- Data ---------------------------------------------------------------
  const [episodes, setEpisodes] = useState<EpisodeSummary[]>([]);
  const [state, setState] = useState<AppState>('loading');
  const [errorMessage, setErrorMessage] = useState('');

  // --- World overlay ------------------------------------------------------
  const [activeWorld, setActiveWorld] = useState<string | null>(null);
  const scrollRef = useRef(0);

  // --- Marble worlds overlay ---------------------------------------------
  const [showMarble, setShowMarble] = useState(false);

  // --- Fetch episodes on mount --------------------------------------------
  useEffect(() => {
    let cancelled = false;

    async function load() {
      try {
        const data = await fetchEpisodes();
        if (!cancelled) {
          setEpisodes(data);
          setState('ready');
        }
      } catch (err) {
        if (!cancelled) {
          setErrorMessage(
            err instanceof Error ? err.message : 'Something went wrong',
          );
          setState('error');
        }
      }
    }

    load();
    return () => {
      cancelled = true;
    };
  }, []);

  // --- Open / close world -------------------------------------------------
  const openWorld = useCallback((slug: string) => {
    scrollRef.current = window.scrollY;
    setActiveWorld(slug);
  }, []);

  const closeWorld = useCallback(() => {
    setActiveWorld(null);
    // WorldOverlay restores scroll via its own cleanup, but we also nudge
    // the browser back to the saved position for safety.
    requestAnimationFrame(() => {
      window.scrollTo(0, scrollRef.current);
    });
  }, []);

  // --- Open / close marble worlds ----------------------------------------
  const openMarble = useCallback(() => {
    scrollRef.current = window.scrollY;
    setShowMarble(true);
  }, []);

  const closeMarble = useCallback(() => {
    setShowMarble(false);
    requestAnimationFrame(() => {
      window.scrollTo(0, scrollRef.current);
    });
  }, []);

  // --- Loading state ------------------------------------------------------
  if (state === 'loading') {
    return (
      <div
        className="fixed inset-0 flex items-center justify-center"
        style={{ background: 'var(--bg)' }}
      >
        <p
          className="animate-pulse-slow text-2xl font-light"
          style={{ letterSpacing: '0.35em', color: 'var(--text)' }}
        >
          SPHERES
        </p>
      </div>
    );
  }

  // --- Error state --------------------------------------------------------
  if (state === 'error') {
    return (
      <div
        className="fixed inset-0 flex flex-col items-center justify-center gap-6"
        style={{ background: 'var(--bg)' }}
      >
        <p
          className="text-2xl font-light"
          style={{ letterSpacing: '0.35em', color: 'var(--text)' }}
        >
          SPHERES
        </p>
        <p className="text-sm" style={{ color: 'var(--text-secondary)' }}>
          {errorMessage || 'Unable to load episodes.'}
        </p>
        <button
          onClick={() => window.location.reload()}
          className="mt-2 px-6 py-2 text-xs uppercase tracking-widest transition-colors duration-300"
          style={{
            color: 'var(--text-secondary)',
            border: '1px solid rgba(255,255,255,0.15)',
            background: 'transparent',
            cursor: 'pointer',
          }}
          onMouseEnter={(e) =>
            ((e.currentTarget as HTMLButtonElement).style.color = 'var(--text)')
          }
          onMouseLeave={(e) =>
            ((e.currentTarget as HTMLButtonElement).style.color =
              'var(--text-secondary)')
          }
        >
          Retry
        </button>
      </div>
    );
  }

  // --- Ready state --------------------------------------------------------
  return (
    <div className="min-h-screen" style={{ background: 'var(--bg)' }}>
      <ScrollExperience episodes={episodes} onOpenWorld={openWorld} />

      {activeWorld && (
        <WorldOverlay onClose={closeWorld}>
          <WorldRenderer episodeSlug={activeWorld} onClose={closeWorld} />
        </WorldOverlay>
      )}

      {/* Marble Worlds overlay */}
      {showMarble && <MarbleWorlds onClose={closeMarble} />}

      {/* Persistent floating nav button — Marble Worlds */}
      {!activeWorld && !showMarble && (
        <button
          onClick={openMarble}
          aria-label="Open Marble Worlds"
          style={{
            position: 'fixed',
            top: 20,
            right: 20,
            zIndex: 90,
            display: 'flex',
            alignItems: 'center',
            gap: 8,
            padding: '10px 18px',
            border: '1px solid rgba(255,255,255,0.12)',
            borderRadius: 12,
            backgroundColor: 'rgba(10,10,10,0.7)',
            backdropFilter: 'blur(16px)',
            WebkitBackdropFilter: 'blur(16px)',
            color: 'rgba(255,255,255,0.6)',
            fontSize: 12,
            fontFamily: "'Inter', system-ui, sans-serif",
            fontWeight: 400,
            letterSpacing: '0.08em',
            textTransform: 'uppercase' as const,
            cursor: 'pointer',
            transition: 'all 0.25s ease',
          }}
          onMouseEnter={(e) => {
            (e.currentTarget as HTMLElement).style.backgroundColor =
              'rgba(255,255,255,0.08)';
            (e.currentTarget as HTMLElement).style.borderColor =
              'rgba(255,255,255,0.25)';
            (e.currentTarget as HTMLElement).style.color =
              'rgba(255,255,255,0.9)';
          }}
          onMouseLeave={(e) => {
            (e.currentTarget as HTMLElement).style.backgroundColor =
              'rgba(10,10,10,0.7)';
            (e.currentTarget as HTMLElement).style.borderColor =
              'rgba(255,255,255,0.12)';
            (e.currentTarget as HTMLElement).style.color =
              'rgba(255,255,255,0.6)';
          }}
        >
          {/* Globe/sphere icon */}
          <svg
            width="14"
            height="14"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="1.5"
            strokeLinecap="round"
            strokeLinejoin="round"
          >
            <circle cx="12" cy="12" r="10" />
            <ellipse cx="12" cy="12" rx="4" ry="10" />
            <line x1="2" y1="12" x2="22" y2="12" />
          </svg>
          Marble Worlds
        </button>
      )}

      <Footer />
    </div>
  );
}
