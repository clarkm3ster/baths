/**
 * ProfilesPage — library of saved profiles with filtering and sorting.
 */

import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { listProfiles } from '../../api/client';
import type { Profile } from '../../types';
import ProfileCard from './ProfileCard';

type FilterMode = 'all' | 'sample' | 'user';
type SortMode = 'cost' | 'savings' | 'name' | 'date';

export default function ProfilesPage() {
  const [profiles, setProfiles] = useState<Profile[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState<FilterMode>('all');
  const [sort, setSort] = useState<SortMode>('date');

  useEffect(() => {
    setLoading(true);
    const params =
      filter === 'sample'
        ? { is_sample: true }
        : filter === 'user'
          ? { is_sample: false }
          : undefined;

    listProfiles(params)
      .then(setProfiles)
      .catch(() => setProfiles([]))
      .finally(() => setLoading(false));
  }, [filter]);

  // Sort
  const sorted = [...profiles].sort((a, b) => {
    switch (sort) {
      case 'cost':
        return b.total_annual_cost - a.total_annual_cost;
      case 'savings':
        return b.savings_annual - a.savings_annual;
      case 'name':
        return (a.name || '').localeCompare(b.name || '');
      case 'date':
      default:
        return new Date(b.created_at).getTime() - new Date(a.created_at).getTime();
    }
  });

  return (
    <div className="max-w-[1200px] mx-auto px-6 py-10">
      {/* Header */}
      <div className="flex items-start justify-between mb-8">
        <div>
          <h1 className="font-serif text-[32px] font-bold">Profiles</h1>
          <p className="text-[var(--color-text-secondary)] text-[14px] mt-1">
            {profiles.length} profile{profiles.length !== 1 ? 's' : ''} in library
          </p>
        </div>
        <Link to="/intake" className="btn btn--primary">
          Create New
        </Link>
      </div>

      {/* Filter + sort bar */}
      <div className="flex items-center justify-between mb-6 pb-4 border-b-2 border-black">
        {/* Filter tabs */}
        <div className="flex gap-0">
          {(['all', 'sample', 'user'] as FilterMode[]).map((f) => (
            <button
              key={f}
              onClick={() => setFilter(f)}
              className={`px-4 py-2 border-2 border-black -ml-[2px] first:ml-0 font-mono text-[12px] uppercase tracking-wider transition-colors ${
                filter === f
                  ? 'bg-black text-white'
                  : 'bg-white text-black hover:bg-[var(--color-surface)]'
              }`}
            >
              {f === 'all' ? 'All' : f === 'sample' ? 'Samples' : 'User-created'}
            </button>
          ))}
        </div>

        {/* Sort */}
        <div className="flex items-center gap-2">
          <span className="font-mono text-[11px] text-[var(--color-text-tertiary)] uppercase tracking-wider">
            Sort:
          </span>
          {(['date', 'cost', 'savings', 'name'] as SortMode[]).map((s) => (
            <button
              key={s}
              onClick={() => setSort(s)}
              className={`px-3 py-1 font-mono text-[11px] uppercase tracking-wider transition-colors ${
                sort === s
                  ? 'text-black border-b-2 border-black'
                  : 'text-[var(--color-text-tertiary)] hover:text-black'
              }`}
            >
              {s}
            </button>
          ))}
        </div>
      </div>

      {/* Grid */}
      {loading ? (
        <div className="flex items-center justify-center py-20">
          <div className="loading-pulse" />
        </div>
      ) : sorted.length === 0 ? (
        <div className="text-center py-20">
          <p className="text-[var(--color-text-tertiary)] text-[14px] mb-4">
            No profiles found.
          </p>
          <Link to="/intake" className="btn">
            Build your first profile
          </Link>
        </div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-0">
          {sorted.map((profile) => (
            <div key={profile.id} className="-mt-[2px] -ml-[2px] first:mt-0 first:ml-0">
              <ProfileCard profile={profile} />
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
