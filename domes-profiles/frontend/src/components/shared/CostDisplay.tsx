/**
 * CostDisplay — formatted currency display in JetBrains Mono.
 *
 * Modes:
 * - default: single value "$79,000"
 * - compare: "FRAGMENTED: $79,000 -> COORDINATED: $31,000 | SAVINGS: $48,000"
 * - delta:   shows +/- with color
 */

interface Props {
  value: number;
  label?: string;
  size?: 'small' | 'medium' | 'large';
  mode?: 'default' | 'savings' | 'cost' | 'delta';
  suffix?: string;
  className?: string;
}

function formatCurrency(n: number): string {
  const abs = Math.abs(n);
  if (abs >= 1_000_000_000) {
    return `$${(abs / 1_000_000_000).toFixed(1)}B`;
  }
  if (abs >= 1_000_000) {
    return `$${(abs / 1_000_000).toFixed(1)}M`;
  }
  return `$${abs.toLocaleString('en-US', { maximumFractionDigits: 0 })}`;
}

export function formatCurrencyFull(n: number): string {
  return `$${Math.abs(n).toLocaleString('en-US', { maximumFractionDigits: 0 })}`;
}

export default function CostDisplay({
  value,
  label,
  size = 'medium',
  mode = 'default',
  suffix = '',
  className = '',
}: Props) {
  const sizeClass =
    size === 'large'
      ? 'stat-number--large'
      : size === 'small'
        ? 'stat-number--small'
        : '';

  const colorClass =
    mode === 'savings'
      ? 'text-[var(--color-savings)]'
      : mode === 'cost'
        ? 'text-[var(--color-cost)]'
        : mode === 'delta'
          ? value >= 0
            ? 'text-[var(--color-savings)]'
            : 'text-[var(--color-cost)]'
          : '';

  const prefix = mode === 'delta' && value > 0 ? '+' : mode === 'delta' && value < 0 ? '-' : '';
  const display = `${prefix}${formatCurrency(value)}`;

  return (
    <div className={`${className}`}>
      {label && <div className="section-label">{label}</div>}
      <span className={`stat-number ${sizeClass} ${colorClass}`}>
        {display}
        {suffix && (
          <span className="text-[0.4em] text-[var(--color-text-tertiary)] ml-1">
            {suffix}
          </span>
        )}
      </span>
    </div>
  );
}

export { formatCurrency };
