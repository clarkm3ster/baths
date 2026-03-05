/**
 * DomeLegend.tsx
 *
 * Legend panel explaining dome visual elements:
 * - Domain colors with labels
 * - System rectangle = data system
 * - Solid line = data connection
 * - Dashed red line = data gap
 * - Green bridge = solution available
 * - Cost format explanation
 */

// ---------------------------------------------------------------------------
// Domain color map
// ---------------------------------------------------------------------------

const DOMAIN_COLORS: Array<{ key: string; label: string; color: string }> = [
  { key: 'health', label: 'Health', color: '#1A6B3C' },
  { key: 'justice', label: 'Justice', color: '#8B1A1A' },
  { key: 'housing', label: 'Housing', color: '#1A3D8B' },
  { key: 'income', label: 'Income', color: '#6B5A1A' },
  { key: 'education', label: 'Education', color: '#5A1A6B' },
  { key: 'child_welfare', label: 'Child Welfare', color: '#1A6B6B' },
];

// ---------------------------------------------------------------------------
// Legend items
// ---------------------------------------------------------------------------

interface LegendSymbolProps {
  children: React.ReactNode;
  label: string;
}

function LegendItem({ children, label }: LegendSymbolProps) {
  return (
    <div className="flex items-center gap-2">
      <div className="w-8 h-5 flex items-center justify-center shrink-0">
        {children}
      </div>
      <span
        className="text-xs"
        style={{ fontFamily: 'Inter, sans-serif', color: '#444' }}
      >
        {label}
      </span>
    </div>
  );
}

// ---------------------------------------------------------------------------
// Component
// ---------------------------------------------------------------------------

export default function DomeLegend() {
  return (
    <div className="border border-black p-4" style={{ maxWidth: 260 }}>
      <h3
        className="text-xs font-bold mb-3 tracking-widest uppercase"
        style={{ fontFamily: "'JetBrains Mono', monospace" }}
      >
        LEGEND
      </h3>

      {/* Domain colors */}
      <div className="mb-3 pb-3 border-b border-gray-300">
        <div className="text-xs font-semibold mb-1.5" style={{ fontFamily: 'Inter, sans-serif', color: '#666' }}>
          Domains
        </div>
        <div className="grid grid-cols-2 gap-1">
          {DOMAIN_COLORS.map((d) => (
            <div key={d.key} className="flex items-center gap-1.5">
              <div
                className="w-3 h-3 shrink-0"
                style={{ backgroundColor: d.color, opacity: 0.8 }}
              />
              <span
                className="text-xs"
                style={{ fontFamily: 'Inter, sans-serif', color: d.color }}
              >
                {d.label}
              </span>
            </div>
          ))}
        </div>
      </div>

      {/* Symbol legend */}
      <div className="flex flex-col gap-2 mb-3 pb-3 border-b border-gray-300">
        <div className="text-xs font-semibold mb-0.5" style={{ fontFamily: 'Inter, sans-serif', color: '#666' }}>
          Symbols
        </div>

        <LegendItem label="Data system">
          <svg width="32" height="16" viewBox="0 0 32 16">
            <rect x="2" y="2" width="28" height="12" fill="#1A6B3C14" stroke="#1A6B3C" strokeWidth="1" />
          </svg>
        </LegendItem>

        <LegendItem label="Legal provision">
          <svg width="32" height="16" viewBox="0 0 20 16">
            <polygon points="10,1 19,8 10,15 1,8" fill="#5A1A6B22" stroke="#5A1A6B" strokeWidth="1" />
          </svg>
        </LegendItem>

        <LegendItem label="Data connection">
          <svg width="32" height="16" viewBox="0 0 32 16">
            <line x1="2" y1="8" x2="30" y2="8" stroke="#22c55e" strokeWidth="2" />
          </svg>
        </LegendItem>

        <LegendItem label="Data gap">
          <svg width="32" height="16" viewBox="0 0 32 16">
            <line x1="2" y1="8" x2="30" y2="8" stroke="#8B1A1A" strokeWidth="2" strokeDasharray="5 3" />
          </svg>
        </LegendItem>

        <LegendItem label="Bridge / solution">
          <svg width="32" height="16" viewBox="0 0 32 16">
            <line x1="2" y1="8" x2="30" y2="8" stroke="#22c55e" strokeWidth="1.5" />
            <circle cx="16" cy="8" r="4" fill="#22c55e" fillOpacity="0.2" stroke="#22c55e" strokeWidth="1" />
          </svg>
        </LegendItem>

        <LegendItem label="Consent-closable">
          <svg width="32" height="16" viewBox="0 0 20 16">
            <rect x="2" y="2" width="16" height="12" fill="#22c55e22" stroke="#22c55e" strokeWidth="0.5" />
            <text x="10" y="11" textAnchor="middle" fill="#22c55e" fontSize="9" fontWeight="700" fontFamily="Inter, sans-serif">C</text>
          </svg>
        </LegendItem>
      </div>

      {/* Cost format */}
      <div>
        <div className="text-xs font-semibold mb-1" style={{ fontFamily: 'Inter, sans-serif', color: '#666' }}>
          Costs
        </div>
        <div
          className="text-xs"
          style={{ fontFamily: "'JetBrains Mono', monospace", color: '#444', lineHeight: 1.6 }}
        >
          <div>
            <span style={{ color: '#8B1A1A' }}>$XXK</span> = fragmented annual
          </div>
          <div>
            <span style={{ color: '#1A6B3C' }}>$XXK</span> = coordinated annual
          </div>
          <div>
            <span style={{ color: '#22c55e' }}>SAVE $XXK</span> = potential savings
          </div>
        </div>
      </div>
    </div>
  );
}
