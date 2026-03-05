/**
 * SPHERES Studio — App Shell
 *
 * Top-level component that defines all routes via React Router v7.
 * Wraps the tree in any global providers (auth / store can be added here).
 */

import { Routes, Route, Navigate } from 'react-router-dom';
import { lazy, Suspense } from 'react';

// ---------------------------------------------------------------------------
// Lazy-loaded page components for code-splitting
// ---------------------------------------------------------------------------

const LandingPage = lazy(() => import('./pages/LandingPage'));
const StudioPage = lazy(() => import('./pages/StudioPage'));
const GalleryPage = lazy(() => import('./pages/GalleryPage'));
const ExplorePage = lazy(() => import('./pages/ExplorePage'));
const PricingPage = lazy(() => import('./pages/PricingPage'));

// ---------------------------------------------------------------------------
// Loading fallback
// ---------------------------------------------------------------------------

function PageLoader() {
  return (
    <div
      className="flex h-screen w-screen items-center justify-center"
      style={{ background: 'var(--bg-primary)' }}
    >
      <div className="flex flex-col items-center gap-4">
        <div
          className="flex h-12 w-12 items-center justify-center rounded-2xl text-lg font-bold"
          style={{ background: 'var(--accent)', color: '#fff' }}
        >
          S
        </div>
        <div className="flex items-center gap-2">
          <div
            className="h-1.5 w-1.5 animate-pulse rounded-full"
            style={{ background: 'var(--accent)', animationDelay: '0ms' }}
          />
          <div
            className="h-1.5 w-1.5 animate-pulse rounded-full"
            style={{ background: 'var(--accent)', animationDelay: '150ms' }}
          />
          <div
            className="h-1.5 w-1.5 animate-pulse rounded-full"
            style={{ background: 'var(--accent)', animationDelay: '300ms' }}
          />
        </div>
      </div>
    </div>
  );
}

// ---------------------------------------------------------------------------
// App
// ---------------------------------------------------------------------------

export default function App() {
  return (
    <Suspense fallback={<PageLoader />}>
      <Routes>
        {/* Public pages */}
        <Route path="/" element={<LandingPage />} />
        <Route path="/pricing" element={<PricingPage />} />
        <Route path="/gallery" element={<GalleryPage />} />

        {/* Studio (the core experience) */}
        <Route path="/studio" element={<StudioPage />} />
        <Route path="/studio/:designId" element={<StudioPage />} />

        {/* 3D exploration */}
        <Route path="/explore/:designId" element={<ExplorePage />} />

        {/* Catch-all redirect */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Suspense>
  );
}
