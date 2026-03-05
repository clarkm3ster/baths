/**
 * DomainBadge — colored badge for a life domain.
 *
 * Usage: <DomainBadge domain="health" />
 * The domain key maps to CSS classes and Tailwind theme colors.
 */

const DOMAIN_META: Record<string, { label: string; color: string }> = {
  health:        { label: 'Health',        color: 'var(--color-health)' },
  justice:       { label: 'Justice',       color: 'var(--color-justice)' },
  housing:       { label: 'Housing',       color: 'var(--color-housing)' },
  income:        { label: 'Income',        color: 'var(--color-income)' },
  education:     { label: 'Education',     color: 'var(--color-education)' },
  child_welfare: { label: 'Child Welfare', color: 'var(--color-child-welfare)' },
};

interface Props {
  domain: string;
  label?: string;
  className?: string;
}

export default function DomainBadge({ domain, label, className = '' }: Props) {
  const meta = DOMAIN_META[domain] ?? { label: domain, color: '#666' };
  const displayLabel = label || meta.label;

  return (
    <span
      className={`domain-badge ${className}`}
      style={{ color: meta.color, borderColor: meta.color }}
    >
      <span
        style={{ background: meta.color }}
        className="inline-block w-[8px] h-[8px]"
      />
      {displayLabel}
    </span>
  );
}

export { DOMAIN_META };
