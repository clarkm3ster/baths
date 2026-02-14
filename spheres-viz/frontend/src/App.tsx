import { useState, useEffect, useCallback, useRef } from 'react';
import ScrollExperience from './components/ScrollExperience';
import Footer from './components/Footer';
import WorldOverlay from './components/WorldOverlay';
import WorldRenderer from './worlds/WorldRenderer';
import { fetchEpisodes, type EpisodeSummary } from './utils/api';

// ---------------------------------------------------------------------------
// App — SPHERES Viz
// ---------------------------------------------------------------------------
// Root component. Fetches episode data, drives the scroll experience, and
// manages the full-screen 3D world overlay. No router — the entire site is a
// single cinematic scroll page with portal-based world pop-outs.
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

      <Footer />
    </div>
  );
}
