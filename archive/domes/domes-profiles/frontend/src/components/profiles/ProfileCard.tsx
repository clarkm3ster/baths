/**
 * ProfileCard — summary card for a profile in the library grid.
 */

import { Link } from 'react-router-dom';
import type { Profile } from '../../types';
import CostDisplay from '../shared/CostDisplay';
import DomainBadge from '../shared/DomainBadge';

interface Props {
  profile: Profile;
}

export default function ProfileCard({ profile }: Props) {
  const boolCircumstances = Object.entries(profile.circumstances)
    .filter(([, v]) => v === true)
    .map(([k]) => k);

  const domainKeys = Array.from(
    new Set(profile.domains?.map((d) => d.domain) ?? [])
  ).slice(0, 4);

  return (
    <div className="border-2 border-black p-5 flex flex-col">
      {/* Header */}
      <div className="flex items-start justify-between mb-3">
        <h3 className="font-serif text-[18px] font-bold leading-tight">
          {profile.name || 'Unnamed Profile'}
        </h3>
        {profile.is_sample && (
          <span className="font-mono text-[10px] uppercase tracking-wider text-[var(--color-text-tertiary)] border border-[var(--color-border)] px-2 py-[1px] shrink-0 ml-2">
            Sample
          </span>
        )}
      </div>

      {/* Domain badges */}
      <div className="flex flex-wrap gap-1 mb-3">
        {domainKeys.map((d) => (
          <DomainBadge key={d} domain={d} />
        ))}
      </div>

      {/* Circumstance tags */}
      <div className="flex flex-wrap gap-1 mb-4">
        {boolCircumstances.slice(0, 4).map((c) => (
          <span
            key={c}
            className="text-[10px] font-mono px-2 py-[1px] border border-[var(--color-border)] text-[var(--color-text-secondary)]"
          >
            {c.replace(/^(has_|is_)/, '').replace(/_/g, ' ')}
          </span>
        ))}
        {boolCircumstances.length > 4 && (
          <span className="text-[10px] font-mono text-[var(--color-text-tertiary)]">
            +{boolCircumstances.length - 4}
          </span>
        )}
      </div>

      {/* Cost stats */}
      <div className="grid grid-cols-2 gap-3 pt-3 border-t border-[var(--color-border)] mt-auto">
        <CostDisplay
          value={profile.total_annual_cost}
          label="Annual cost"
          size="small"
          mode="cost"
        />
        <CostDisplay
          value={profile.savings_annual}
          label="Savings"
          size="small"
          mode="savings"
          suffix="/yr"
        />
      </div>

      {/* Actions */}
      <div className="flex gap-2 mt-4">
        <Link to={`/dome/${profile.id}`} className="btn btn--small btn--primary flex-1">
          View Dome
        </Link>
        <Link to={`/cost/${profile.id}`} className="btn btn--small flex-1">
          Cost Detail
        </Link>
      </div>
    </div>
  );
}
