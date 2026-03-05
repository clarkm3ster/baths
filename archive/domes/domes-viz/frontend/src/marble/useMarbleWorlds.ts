import { useState, useEffect } from "react";
import type { MarbleWorld } from "./types";

/**
 * Hook to fetch Marble worlds from the backend.
 * Returns worlds array, loading state, and any error.
 */
export function useMarbleWorlds() {
  const [worlds, setWorlds] = useState<MarbleWorld[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;

    async function fetchWorlds() {
      try {
        const resp = await fetch("/api/marble/worlds");
        if (!resp.ok) {
          throw new Error(`HTTP ${resp.status}: ${resp.statusText}`);
        }
        const data = await resp.json();
        if (!cancelled) {
          setWorlds(data.worlds || []);
          setLoading(false);
        }
      } catch (err) {
        console.error("Failed to fetch Marble worlds:", err);
        if (!cancelled) {
          setError(err instanceof Error ? err.message : "Unknown error");
          setLoading(false);
        }
      }
    }

    fetchWorlds();
    return () => {
      cancelled = true;
    };
  }, []);

  return { worlds, loading, error };
}
