/**
 * StatBlock — big number + label display for hero stats.
 */

interface Props {
  value: string;
  label: string;
  sublabel?: string;
  size?: 'small' | 'medium' | 'large';
  color?: string;
  className?: string;
}

export default function StatBlock({
  value,
  label,
  sublabel,
  size = 'medium',
  color,
  className = '',
}: Props) {
  const sizeClass =
    size === 'large'
      ? 'stat-number--large'
      : size === 'small'
        ? 'stat-number--small'
        : '';

  return (
    <div className={className}>
      <div className="section-label">{label}</div>
      <div className={`stat-number ${sizeClass}`} style={color ? { color } : undefined}>
        {value}
      </div>
      {sublabel && (
        <div className="mt-1 text-[12px] text-[var(--color-text-tertiary)]">
          {sublabel}
        </div>
      )}
    </div>
  );
}
