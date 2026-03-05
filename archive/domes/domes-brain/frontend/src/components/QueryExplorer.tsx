// ─────────────────────────────────────────────────────────────────────────────
// DOMES Brain — Query Explorer: Interactive query tester
// ─────────────────────────────────────────────────────────────────────────────

import { useState, useCallback } from 'react';
import {
  type QueryResponse,
  type RoutePreview,
  postQuery,
  routeQuery,
  getServiceColor,
} from '../api/client.ts';

// ── JSON Tree Viewer ─────────────────────────────────────────────────────────

function JsonValue({ value, depth }: { value: unknown; depth: number }) {
  if (value === null) return <span className="text-text-muted">null</span>;
  if (value === undefined) return <span className="text-text-muted">undefined</span>;
  if (typeof value === 'boolean') return <span className="text-amber">{String(value)}</span>;
  if (typeof value === 'number') return <span className="text-green">{value}</span>;
  if (typeof value === 'string') return <span className="text-red">"{value}"</span>;

  if (Array.isArray(value)) {
    if (value.length === 0) return <span className="text-text-muted">[]</span>;
    return (
      <div>
        <span className="text-text-muted">[</span>
        <div style={{ paddingLeft: `${(depth + 1) * 12}px` }}>
          {value.map((item, i) => (
            <div key={i} className="leading-tight">
              <JsonValue value={item} depth={depth + 1} />
              {i < value.length - 1 && <span className="text-text-muted">,</span>}
            </div>
          ))}
        </div>
        <span className="text-text-muted">]</span>
      </div>
    );
  }

  if (typeof value === 'object') {
    const entries = Object.entries(value as Record<string, unknown>);
    if (entries.length === 0) return <span className="text-text-muted">{'{}'}</span>;
    return (
      <div>
        <span className="text-text-muted">{'{'}</span>
        <div style={{ paddingLeft: `${(depth + 1) * 12}px` }}>
          {entries.map(([k, v], i) => (
            <div key={k} className="leading-tight">
              <span className="text-blue">"{k}"</span>
              <span className="text-text-muted">: </span>
              <JsonValue value={v} depth={depth + 1} />
              {i < entries.length - 1 && <span className="text-text-muted">,</span>}
            </div>
          ))}
        </div>
        <span className="text-text-muted">{'}'}</span>
      </div>
    );
  }

  return <span className="text-text">{String(value)}</span>;
}

// ── History Item ─────────────────────────────────────────────────────────────

interface HistoryItem {
  query: string;
  circumstances: string;
  timestamp: Date;
}

// ── Query Explorer ───────────────────────────────────────────────────────────

export default function QueryExplorer() {
  const [queryText, setQueryText] = useState('');
  const [circumstancesJson, setCircumstancesJson] = useState('{}');
  const [jsonError, setJsonError] = useState('');

  const [routePreview, setRoutePreview] = useState<RoutePreview | null>(null);
  const [response, setResponse] = useState<QueryResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [routing, setRouting] = useState(false);

  const [history, setHistory] = useState<HistoryItem[]>([]);

  const parseCircumstances = (): Record<string, string> | null => {
    try {
      const parsed = JSON.parse(circumstancesJson);
      if (typeof parsed !== 'object' || Array.isArray(parsed) || parsed === null) {
        setJsonError('Must be a JSON object');
        return null;
      }
      setJsonError('');
      return parsed as Record<string, string>;
    } catch {
      setJsonError('Invalid JSON');
      return null;
    }
  };

  const handleRoute = useCallback(async () => {
    if (!queryText.trim()) return;
    const ctx = parseCircumstances();
    if (ctx === null) return;

    setRouting(true);
    setRoutePreview(null);
    const preview = await routeQuery(queryText.trim(), Object.keys(ctx).length > 0 ? ctx : undefined);
    setRoutePreview(preview);
    setRouting(false);
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [queryText, circumstancesJson]);

  const handleExecute = useCallback(async () => {
    if (!queryText.trim()) return;
    const ctx = parseCircumstances();
    if (ctx === null) return;

    setLoading(true);
    setResponse(null);
    setRoutePreview(null);
    const res = await postQuery(queryText.trim(), Object.keys(ctx).length > 0 ? ctx : undefined);
    setResponse(res);
    setLoading(false);

    // Add to history (max 10)
    setHistory((prev) => {
      const next = [
        { query: queryText.trim(), circumstances: circumstancesJson, timestamp: new Date() },
        ...prev,
      ];
      return next.slice(0, 10);
    });
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [queryText, circumstancesJson]);

  const loadFromHistory = (item: HistoryItem) => {
    setQueryText(item.query);
    setCircumstancesJson(item.circumstances);
    setResponse(null);
    setRoutePreview(null);
  };

  return (
    <div className="p-6 flex gap-4 h-full">
      {/* Main Panel */}
      <div className="flex-1 space-y-4 min-w-0">
        {/* Query Input */}
        <div className="bg-surface border border-border p-4 space-y-3">
          <div>
            <label className="text-xs text-text-muted uppercase tracking-wider block mb-1">
              Query
            </label>
            <textarea
              value={queryText}
              onChange={(e) => setQueryText(e.target.value)}
              placeholder="Enter your query..."
              rows={3}
              className="w-full bg-surface-alt border border-border px-3 py-2 font-mono text-sm text-text placeholder:text-text-muted focus:outline-none focus:border-blue resize-y"
            />
          </div>

          <div>
            <label className="text-xs text-text-muted uppercase tracking-wider block mb-1">
              Circumstances (JSON)
            </label>
            <textarea
              value={circumstancesJson}
              onChange={(e) => {
                setCircumstancesJson(e.target.value);
                setJsonError('');
              }}
              rows={4}
              className="w-full bg-surface-alt border border-border px-3 py-2 font-mono text-sm text-text focus:outline-none focus:border-blue resize-y"
            />
            {jsonError && (
              <div className="text-xs font-mono text-red mt-1">{jsonError}</div>
            )}
          </div>

          <div className="flex gap-2">
            <button
              onClick={handleRoute}
              disabled={routing || !queryText.trim()}
              className="border border-blue text-blue px-4 py-1.5 font-mono text-sm hover:bg-blue-dim disabled:opacity-40"
            >
              {routing ? 'Routing...' : 'Route'}
            </button>
            <button
              onClick={handleExecute}
              disabled={loading || !queryText.trim()}
              className="bg-blue text-bg px-4 py-1.5 font-mono text-sm font-semibold hover:opacity-90 disabled:opacity-40"
            >
              {loading ? 'Executing...' : 'Execute'}
            </button>
          </div>
        </div>

        {/* Route Preview */}
        {routePreview && (
          <div className="bg-surface border border-border p-4">
            <h3 className="text-xs text-text-muted uppercase tracking-wider mb-2">Route Preview</h3>
            <div className="flex flex-wrap gap-2 mb-2">
              {routePreview.services.map((slug) => (
                <span
                  key={slug}
                  className="text-xs font-mono px-2 py-0.5 border"
                  style={{
                    color: getServiceColor(slug),
                    borderColor: getServiceColor(slug),
                  }}
                >
                  {slug}
                </span>
              ))}
            </div>
            <div className="text-xs font-mono text-text-muted">
              Estimated execution: {routePreview.estimatedTime}ms
            </div>
          </div>
        )}

        {/* Loading */}
        {loading && (
          <div className="bg-surface border border-border p-4 animate-pulse">
            <div className="h-4 bg-surface-alt w-48 mb-3" />
            <div className="h-64 bg-surface-alt" />
          </div>
        )}

        {/* Response Viewer */}
        {!loading && response && (
          <div className="bg-surface border border-border">
            <div className="px-4 py-2 border-b border-border flex items-center justify-between">
              <h3 className="text-xs text-text-muted uppercase tracking-wider">Response</h3>
              <span className="text-xs font-mono text-text-muted">
                {response.totalResults} results in {response.executionTime}ms
              </span>
            </div>
            <div className="p-4 overflow-x-auto max-h-[600px] overflow-y-auto">
              <pre className="font-mono text-xs leading-relaxed">
                <JsonValue value={response as unknown} depth={0} />
              </pre>
            </div>
          </div>
        )}
      </div>

      {/* History Sidebar */}
      <div className="w-64 shrink-0 hidden lg:block">
        <div className="bg-surface border border-border">
          <div className="px-3 py-2 border-b border-border">
            <h3 className="text-xs text-text-muted uppercase tracking-wider">
              Query History ({history.length})
            </h3>
          </div>
          {history.length === 0 ? (
            <div className="p-3">
              <p className="text-xs font-mono text-text-muted">No queries yet</p>
            </div>
          ) : (
            <div className="divide-y divide-border">
              {history.map((item, i) => (
                <button
                  key={i}
                  onClick={() => loadFromHistory(item)}
                  className="w-full text-left px-3 py-2 hover:bg-surface-alt transition-colors"
                >
                  <div className="text-xs font-mono text-text truncate">{item.query}</div>
                  <div className="text-xs font-mono text-text-muted">
                    {item.timestamp.toLocaleTimeString('en-US', {
                      hour: '2-digit',
                      minute: '2-digit',
                      hour12: false,
                    })}
                  </div>
                </button>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
