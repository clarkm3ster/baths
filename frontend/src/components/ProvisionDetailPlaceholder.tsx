import type { Provision } from '../types';
import { DOMAIN_COLORS, DOMAIN_LABELS } from '../types';

interface ProvisionDetailPlaceholderProps {
  provision: Provision;
  onClose: () => void;
}

export function ProvisionDetailPlaceholder({
  provision,
  onClose,
}: ProvisionDetailPlaceholderProps) {
  return (
    <article className="border-l-4 p-6" style={{ borderLeftColor: DOMAIN_COLORS[provision.domain] }}>
      <div className="flex items-start justify-between mb-4">
        <div>
          <p
            className="font-mono text-sm text-black/60 mb-1"
            aria-label="Legal citation"
          >
            {provision.citation}
          </p>
          <h3 className="font-serif text-xl font-medium">
            {provision.title}
          </h3>
        </div>
        <button
          onClick={onClose}
          className="text-black/40 hover:text-black text-2xl leading-none p-1 cursor-pointer"
          aria-label="Close provision detail"
        >
          &times;
        </button>
      </div>

      <div className="flex gap-3 mb-4">
        <span
          className="text-xs font-medium text-white px-3 py-1 uppercase tracking-wider"
          style={{ backgroundColor: DOMAIN_COLORS[provision.domain] }}
        >
          {DOMAIN_LABELS[provision.domain]}
        </span>
        <span className="text-xs font-medium border border-border px-3 py-1 uppercase tracking-wider">
          {provision.provision_type}
        </span>
      </div>

      <div className="mb-6">
        <h4 className="text-xs font-medium uppercase tracking-wider text-black/40 mb-2">
          Full Text
        </h4>
        <p className="text-sm leading-relaxed">{provision.full_text}</p>
      </div>

      {provision.enforcement_mechanisms.length > 0 && (
        <div className="mb-6">
          <h4 className="text-xs font-medium uppercase tracking-wider text-black/40 mb-2">
            Enforcement Mechanisms
          </h4>
          <ul className="space-y-1">
            {provision.enforcement_mechanisms.map((mechanism, i) => (
              <li key={i} className="text-sm flex items-start gap-2">
                <span className="text-black/30 mt-0.5">&mdash;</span>
                {mechanism}
              </li>
            ))}
          </ul>
        </div>
      )}

      {provision.cross_references.length > 0 && (
        <div className="mb-6">
          <h4 className="text-xs font-medium uppercase tracking-wider text-black/40 mb-2">
            Cross-References
          </h4>
          <ul className="space-y-1">
            {provision.cross_references.map((ref, i) => (
              <li key={i} className="font-mono text-sm text-black/60">
                {ref}
              </li>
            ))}
          </ul>
        </div>
      )}

      <div className="border-t border-border pt-4 mt-6">
        <h4 className="text-xs font-medium uppercase tracking-wider text-black/40 mb-2">
          What This Means for You
        </h4>
        <p className="text-sm text-black/50 italic">
          Plain-language explanation will appear here once the analysis engine is connected.
        </p>
      </div>
    </article>
  );
}
