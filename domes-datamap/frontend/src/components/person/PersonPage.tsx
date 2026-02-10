import { useState } from "react";
import type { PersonMapResult } from "../../types";
import { postPersonMap } from "../../api/client";
import { CircumstancesForm } from "./CircumstancesForm";
import { PersonResults } from "./PersonResults";

export function PersonPage() {
  const [selected, setSelected] = useState<string[]>([]);
  const [result, setResult] = useState<PersonMapResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit() {
    if (selected.length === 0) return;
    setLoading(true);
    setError(null);
    try {
      const data = await postPersonMap(selected);
      setResult(data);
    } catch (e: any) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="flex flex-col h-[calc(100vh-3.5rem)]">
      {/* Header */}
      <div className="border-b border-black px-4 py-2 bg-gray-50">
        <h2 className="font-serif text-lg font-bold uppercase tracking-wide">
          Person View
        </h2>
        <p className="font-mono text-[0.625rem] text-gray-500 uppercase tracking-wider">
          Map your government data footprint
        </p>
      </div>

      {/* Content */}
      <div className="flex-1 overflow-auto p-4 space-y-4">
        <CircumstancesForm
          selected={selected}
          onChange={setSelected}
          onSubmit={handleSubmit}
          loading={loading}
        />

        {error && (
          <div className="border-2 border-red-600 p-3 bg-red-50">
            <p className="font-mono text-xs text-red-700">Error: {error}</p>
          </div>
        )}

        {result && <PersonResults result={result} />}
      </div>
    </div>
  );
}
