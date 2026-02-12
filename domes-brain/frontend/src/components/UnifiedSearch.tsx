// ─────────────────────────────────────────────────────────────────────────────
// DOMES Brain — Unified Search: Cross-system query interface
// ─────────────────────────────────────────────────────────────────────────────

import { useState, useCallback } from 'react';
import {
  type QueryResponse,
  type QueryResult,
  postQuery,
  getServiceColor,
  formatTimestamp,
} from '../api/client.ts';

// ── Circumstance Row ─────────────────────────────────────────────────────────

interface CircumstanceRow {
  key: string;
  value: string;
}

function CircumstanceEditor({
  rows,
  onChange,
}: {
  rows: CircumstanceRow[];
  onChange: (rows: CircumstanceRow[]) => void;
}) {
  const update = (idx: number, field: 'key' | 'value', val: string) => {
    const next = [...rows];
    next[idx] = { ...next[idx], [field]: val };
    onChange(next);
  };
  const add = () => onChange([...rows, { key: '', value: '' }]);
  const remove = (idx: number) => onChange(rows.filter((_, i) => i !== idx));

  return (
    <div className="space-y-2">
      <div className="flex items-center justify-between">
        <span className="text-xs text-text-muted uppercase tracking-wider">Circumstances</span>
        <button
          onClick={add}
          className="text-xs font-mono text-blue hover:text-text border border-border px-2 py-0.5"
        >
          + Add
        </button>
      </div>
      {rows.map((row, i) => (
        <div key={i} className="flex gap-2">
          <input
            type="text"
            value={row.key}
            onChange={(e) => update(i, 'key', e.target.value)}
            placeholder="key"
            className="flex-1 bg-surface-alt border border-border px-2 py-1 text-xs font-mono text-text placeholder:text-text-muted focus:outline-none focus:border-blue"
          />
          <input
            type="text"
            value={row.value}
            onChange={(e) => update(i, 'value', e.target.value)}
            placeholder="value"
            className="flex-2 bg-surface-alt border border-border px-2 py-1 text-xs font-mono text-text placeholder:text-text-muted focus:outline-none focus:border-blue"
          />
          <button
            onClick={() => remove(i)}
            className="text-xs font-mono text-red hover:text-text border border-border px-2 py-1"
          >
            x
          </button>
        </div>
      ))}
    </div>
  );
}

// ── Result Card ──────────────────────────────────────────────────────────────

function ResultCard({ result }: { result: QueryResult }) {
  const color = getServiceColor(result.sourceSlug);
  return (
    <div
      className="bg-surface border border-border p-3 relative"
      style={{ borderLeftWidth: '3px', borderLeftColor: color }}
    >
      <div className="flex items-center justify-between mb-1">
        <span
          className="text-xs font-mono px-1.5 py-0.5 border"
          style={{ color, borderColor: color }}
        >
          {result.source}
        </span>
        <span className="text-xs font-mono text-text-muted">
          {formatTimestamp(result.timestamp)}
        </span>
      </div>
      <h4 className="text-sm font-semibold text-text mb-1">{result.title}</h4>
      <p className="text-xs text-text-muted leading-relaxed mb-2">{result.snippet}</p>
      <div className="flex items-center gap-2">
        <div className="flex-1 h-1 bg-surface-alt">
          <div
            className="h-full bg-blue"
            style={{ width: `${result.relevance * 100}%` }}
          />
        </div>
        <span className="text-xs font-mono text-blue">
          {(result.relevance * 100).toFixed(0)}%
        </span>
      </div>
    </div>
  );
}

// ── Skeleton Card ────────────────────────────────────────────────────────────

function SkeletonCard() {
  return (
    <div className="bg-surface border border-border p-3 animate-pulse">
      <div className="h-3 bg-surface-alt w-20 mb-2" />
      <div className="h-4 bg-surface-alt w-3/4 mb-2" />
      <div className="h-3 bg-surface-alt w-full mb-1" />
      <div className="h-3 bg-surface-alt w-2/3 mb-2" />
      <div className="h-1 bg-surface-alt w-full" />
    </div>
  );
}

// ── Tab Button ───────────────────────────────────────────────────────────────

function TabButton({
  label,
  active,
  count,
  color,
  onClick,
}: {
  label: string;
  active: boolean;
  count: number;
  color?: string;
  onClick: () => void;
}) {
  return (
    <button
      onClick={onClick}
      className={`px-3 py-1.5 text-xs font-mono border-b-2 transition-colors ${
        active
          ? 'border-blue text-text'
          : 'border-transparent text-text-muted hover:text-text'
      }`}
      style={active && color ? { borderBottomColor: color } : undefined}
    >
      {label}
      <span className="ml-1 text-text-muted">({count})</span>
    </button>
  );
}

// ── Unified Search ───────────────────────────────────────────────────────────

export default function UnifiedSearch() {
  const [query, setQuery] = useState('');
  const [circumstances, setCircumstances] = useState<CircumstanceRow[]>([]);
  const [showCircumstances, setShowCircumstances] = useState(false);
  const [response, setResponse] = useState<QueryResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState('all');

  const submit = useCallback(async () => {
    if (!query.trim()) return;
    setLoading(true);
    setResponse(null);

    const ctx: Record<string, string> = {};
    for (const row of circumstances) {
      if (row.key.trim() && row.value.trim()) {
        ctx[row.key.trim()] = row.value.trim();
      }
    }

    const res = await postQuery(
      query.trim(),
      Object.keys(ctx).length > 0 ? ctx : undefined,
    );
    setResponse(res);
    setActiveTab('all');
    setLoading(false);
  }, [query, circumstances]);

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      submit();
    }
  };

  // Derive tabs from results
  const sourceTabs = response
    ? Array.from(new Set(response.results.map((r) => r.sourceSlug))).map((slug) => ({
        slug,
        label: response.results.find((r) => r.sourceSlug === slug)?.source ?? slug,
        count: response.results.filter((r) => r.sourceSlug === slug).length,
        color: getServiceColor(slug),
      }))
    : [];

  const filteredResults = response
    ? activeTab === 'all'
      ? response.results
      : response.results.filter((r) => r.sourceSlug === activeTab)
    : [];

  return (
    <div className="p-6 space-y-4">
      {/* Search Bar */}
      <div className="bg-surface border border-border p-4">
        <div className="flex gap-2">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Query across all DOMES systems..."
            className="flex-1 bg-surface-alt border border-border px-3 py-2 font-mono text-sm text-text placeholder:text-text-muted focus:outline-none focus:border-blue"
          />
          <button
            onClick={submit}
            disabled={loading || !query.trim()}
            className="bg-blue text-bg px-4 py-2 font-mono text-sm font-semibold hover:opacity-90 disabled:opacity-40"
          >
            {loading ? 'Searching...' : 'Search'}
          </button>
        </div>

        {/* Circumstances Toggle */}
        <button
          onClick={() => setShowCircumstances(!showCircumstances)}
          className="mt-2 text-xs font-mono text-text-muted hover:text-text"
        >
          {showCircumstances ? '- Hide circumstances' : '+ Add circumstances'}
        </button>

        {showCircumstances && (
          <div className="mt-2 border-t border-border pt-2">
            <CircumstanceEditor rows={circumstances} onChange={setCircumstances} />
          </div>
        )}
      </div>

      {/* Results */}
      {loading && (
        <div className="space-y-3">
          <SkeletonCard />
          <SkeletonCard />
          <SkeletonCard />
        </div>
      )}

      {!loading && !response && (
        <div className="bg-surface border border-border p-8 text-center">
          <p className="text-text-muted text-sm font-mono">
            Enter a query to search across all DOMES systems
          </p>
        </div>
      )}

      {!loading && response && (
        <>
          {/* Summary */}
          <div className="bg-surface border border-border p-3 flex items-center justify-between">
            <span className="text-xs font-mono text-text-muted">
              {response.totalResults} results for "{response.query}"
            </span>
            <span className="text-xs font-mono text-text-muted">
              {response.executionTime}ms across {response.routedTo.length} services
            </span>
          </div>

          {/* Tabs */}
          <div className="flex gap-0 border-b border-border overflow-x-auto">
            <TabButton
              label="All"
              active={activeTab === 'all'}
              count={response.results.length}
              onClick={() => setActiveTab('all')}
            />
            {sourceTabs.map((tab) => (
              <TabButton
                key={tab.slug}
                label={tab.label}
                active={activeTab === tab.slug}
                count={tab.count}
                color={tab.color}
                onClick={() => setActiveTab(tab.slug)}
              />
            ))}
          </div>

          {/* Result Cards */}
          <div className="space-y-2">
            {filteredResults.map((result) => (
              <ResultCard key={result.id} result={result} />
            ))}
          </div>
        </>
      )}
    </div>
  );
}
