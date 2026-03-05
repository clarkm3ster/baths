import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { generateProfile } from '../../api/client';
import CircumstanceSelector from './CircumstanceSelector';

export default function IntakePage() {
  const navigate = useNavigate();
  const [name, setName] = useState('');
  const [circumstances, setCircumstances] = useState<Record<string, boolean | string>>({
    age: 'adult',
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const selectedCount = Object.values(circumstances).filter(
    (v) => v === true
  ).length;

  async function handleGenerate() {
    if (selectedCount === 0) {
      setError('Select at least one circumstance to generate a profile.');
      return;
    }
    setLoading(true);
    setError('');
    try {
      const profile = await generateProfile(circumstances, name || undefined);
      navigate(`/dome/${profile.id}`);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to generate profile.');
      setLoading(false);
    }
  }

  return (
    <div className="max-w-[800px] mx-auto px-6 py-12">
      {/* Header */}
      <div className="mb-10">
        <h1 className="font-serif text-[32px] font-bold mb-2">Build a Profile</h1>
        <p className="text-[var(--color-text-secondary)] text-[14px] max-w-[600px]">
          Select the circumstances that apply. DOMES will map every government system
          involved, calculate fragmented costs, and show what coordination could save.
        </p>
      </div>

      {/* Optional name */}
      <div className="mb-8">
        <label className="section-label block mb-2">Profile name (optional)</label>
        <input
          type="text"
          value={name}
          onChange={(e) => setName(e.target.value)}
          placeholder="e.g., Maria, Case Study 4, Pilot Participant A"
          className="w-full max-w-[400px] px-3 py-2 border-2 border-black font-sans text-[14px] bg-white focus:outline-none focus:bg-[var(--color-surface)]"
        />
      </div>

      {/* Circumstances */}
      <CircumstanceSelector
        circumstances={circumstances}
        onChange={setCircumstances}
      />

      {/* Summary + generate */}
      <div className="mt-10 pt-6 border-t-2 border-black flex items-center justify-between">
        <div>
          <span className="font-mono text-[14px] font-medium">
            {selectedCount}
          </span>
          <span className="text-[13px] text-[var(--color-text-secondary)] ml-2">
            circumstance{selectedCount !== 1 ? 's' : ''} selected
          </span>
        </div>

        <button
          onClick={handleGenerate}
          disabled={loading}
          className={`btn btn--primary ${loading ? 'btn--disabled' : ''}`}
        >
          {loading ? 'Generating...' : 'Generate Profile'}
        </button>
      </div>

      {/* Error */}
      {error && (
        <div className="mt-4 p-3 border-2 border-[var(--color-cost)] text-[var(--color-cost)] text-[13px] font-mono">
          {error}
        </div>
      )}
    </div>
  );
}
