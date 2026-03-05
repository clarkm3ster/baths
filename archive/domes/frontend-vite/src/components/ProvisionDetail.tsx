import type { Provision, MatchedProvision, ExplanationResult } from "../types/index.ts";
import { DOMAIN_COLORS, DOMAIN_LABELS } from "../types/index.ts";

interface ProvisionDetailProps {
  /** The provision to display. Accepts either a full Provision or a MatchedProvision. */
  provision: Provision | MatchedProvision;
  explanation?: ExplanationResult;
  loading: boolean;
  onClose: () => void;
}

const TYPE_LABELS: Record<string, string> = {
  right: "Right",
  obligation: "Obligation",
  protection: "Protection",
  enforcement: "Enforcement",
};

function isMatchedProvision(p: Provision | MatchedProvision): p is MatchedProvision {
  return "relevance_score" in p;
}

export default function ProvisionDetail({
  provision,
  explanation,
  loading,
  onClose,
}: ProvisionDetailProps) {
  const domainColor = DOMAIN_COLORS[provision.domain] || "#333";
  const matched = isMatchedProvision(provision);
  const relevanceScore = matched ? provision.relevance_score : undefined;
  const matchReasons = matched ? provision.match_reasons : [];
  const isGap = matched ? provision.is_gap : false;
  const enforcementSteps = matched ? provision.enforcement_steps : [];
  const enforcementMechanisms = !matched ? provision.enforcement_mechanisms : [];
  const crossRefs = matched ? (provision.cross_references ?? []) : ("cross_references" in provision ? provision.cross_references : []);
  const sourceUrl = matched ? (provision.source_url ?? "") : ("source_url" in provision ? provision.source_url : "");

  return (
    <article
      role="article"
      aria-label={`Details for ${provision.title}`}
      className="p-6"
      style={{ borderLeft: `4px solid ${domainColor}` }}
    >
      {/* Close button */}
      <div className="flex items-start justify-between mb-4">
        <div>
          {/* Citation */}
          <p
            className="font-mono text-sm mb-1"
            style={{ color: "#666" }}
            aria-label="Legal citation"
          >
            {provision.citation}
          </p>

          {/* Title */}
          <h3 className="font-serif text-xl font-medium leading-tight">
            {provision.title}
          </h3>
        </div>
        <button
          onClick={onClose}
          aria-label="Close detail panel"
          className="text-2xl leading-none p-1 cursor-pointer"
          style={{ color: "rgba(0,0,0,0.4)" }}
        >
          &times;
        </button>
      </div>

      {/* Badges */}
      <div className="flex gap-2 mb-5 flex-wrap">
        <span
          className="text-xs font-medium px-3 py-1 uppercase tracking-wider"
          style={{ color: "#fff", backgroundColor: domainColor }}
        >
          {DOMAIN_LABELS[provision.domain] || provision.domain}
        </span>
        <span className="text-xs font-medium px-3 py-1 uppercase tracking-wider border border-[#E5E5E5]">
          {TYPE_LABELS[provision.provision_type] || provision.provision_type}
        </span>
        {isGap && (
          <span
            className="text-xs font-medium px-3 py-1 uppercase tracking-wider border"
            style={{ color: "#e94560", borderColor: "#e94560" }}
          >
            Gap in Protection
          </span>
        )}
      </div>

      {/* Relevance bar (only for matched provisions) */}
      {relevanceScore !== undefined && (
        <div className="mb-5">
          <div className="text-xs uppercase tracking-wider mb-1.5 font-medium" style={{ color: "#999" }}>
            Relevance
          </div>
          <div className="flex items-center gap-2">
            <div className="flex-1 h-1 relative" style={{ background: "#E5E5E5" }}>
              <div
                className="absolute left-0 top-0 h-full transition-[width] duration-300"
                style={{ width: `${relevanceScore * 100}%`, background: domainColor }}
              />
            </div>
            <span className="font-mono text-xs" style={{ color: "#666" }}>
              {Math.round(relevanceScore * 100)}%
            </span>
          </div>
          {matchReasons.length > 0 && (
            <p className="mt-1 text-xs" style={{ color: "#666" }}>
              {matchReasons.join(" \u00b7 ")}
            </p>
          )}
        </div>
      )}

      {/* Legal text */}
      <div className="mb-6">
        <h4 className="text-xs font-medium uppercase tracking-wider mb-2" style={{ color: "rgba(0,0,0,0.4)" }}>
          Full Text
        </h4>
        <blockquote
          className="text-sm leading-relaxed m-0 p-3"
          style={{
            borderLeft: `3px solid ${domainColor}`,
            background: "#fafafa",
            fontFamily: "Georgia, 'Times New Roman', serif",
          }}
        >
          {provision.full_text}
        </blockquote>
      </div>

      {/* Plain English explanation from Claude */}
      <div className="mb-6 border-t border-[#E5E5E5] pt-4">
        <h4 className="text-xs font-medium uppercase tracking-wider mb-2" style={{ color: "rgba(0,0,0,0.4)" }}>
          What This Means for You
        </h4>
        {loading ? (
          <LoadingPulse />
        ) : explanation ? (
          <div className="text-[15px] leading-relaxed">
            <p className="mb-3">{explanation.plain_english}</p>
            <p className="font-medium">{explanation.what_it_means_for_you}</p>
          </div>
        ) : (
          <p className="text-sm italic" style={{ color: "#999" }}>
            Plain-language explanation will appear here once the analysis engine is connected.
          </p>
        )}
      </div>

      {/* Your Rights */}
      {explanation && explanation.your_rights.length > 0 && (
        <div className="mb-6">
          <h4 className="text-xs font-medium uppercase tracking-wider mb-2" style={{ color: "rgba(0,0,0,0.4)" }}>
            Your Rights
          </h4>
          <ul className="space-y-1">
            {explanation.your_rights.map((r, i) => (
              <li key={i} className="text-sm flex items-start gap-2">
                <span style={{ color: "rgba(0,0,0,0.3)" }} className="mt-0.5">&mdash;</span>
                {r}
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Enforcement Steps / Mechanisms */}
      {(explanation?.enforcement_steps ?? enforcementSteps).length > 0 && (
        <div className="mb-6">
          <h4 className="text-xs font-medium uppercase tracking-wider mb-2" style={{ color: "rgba(0,0,0,0.4)" }}>
            Enforcement Steps
          </h4>
          <ol className="space-y-2 pl-5 text-sm">
            {(explanation?.enforcement_steps ?? enforcementSteps).map((step, i) => (
              <li key={i}>{step}</li>
            ))}
          </ol>
        </div>
      )}
      {enforcementMechanisms.length > 0 && !explanation && enforcementSteps.length === 0 && (
        <div className="mb-6">
          <h4 className="text-xs font-medium uppercase tracking-wider mb-2" style={{ color: "rgba(0,0,0,0.4)" }}>
            Enforcement Mechanisms
          </h4>
          <ul className="space-y-1">
            {enforcementMechanisms.map((mechanism, i) => (
              <li key={i} className="text-sm flex items-start gap-2">
                <span style={{ color: "rgba(0,0,0,0.3)" }} className="mt-0.5">&mdash;</span>
                {mechanism}
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Key Deadlines */}
      {explanation && explanation.key_deadlines.length > 0 && (
        <div className="mb-6">
          <h4 className="text-xs font-medium uppercase tracking-wider mb-2" style={{ color: "rgba(0,0,0,0.4)" }}>
            Key Deadlines
          </h4>
          <ul className="space-y-1">
            {explanation.key_deadlines.map((d, i) => (
              <li key={i} className="text-sm flex items-start gap-2">
                <span style={{ color: "rgba(0,0,0,0.3)" }} className="mt-0.5">&mdash;</span>
                {d}
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Who to Contact */}
      {explanation && explanation.who_to_contact.length > 0 && (
        <div className="mb-6">
          <h4 className="text-xs font-medium uppercase tracking-wider mb-2" style={{ color: "rgba(0,0,0,0.4)" }}>
            Who to Contact
          </h4>
          <ul className="space-y-1">
            {explanation.who_to_contact.map((c, i) => (
              <li key={i} className="text-sm flex items-start gap-2">
                <span style={{ color: "rgba(0,0,0,0.3)" }} className="mt-0.5">&mdash;</span>
                {c}
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Cross-references */}
      {crossRefs.length > 0 && (
        <div className="mb-6">
          <h4 className="text-xs font-medium uppercase tracking-wider mb-2" style={{ color: "rgba(0,0,0,0.4)" }}>
            Cross-References
          </h4>
          <ul className="space-y-1">
            {crossRefs.map((ref, i) => (
              <li key={i} className="font-mono text-sm" style={{ color: "rgba(0,0,0,0.6)" }}>
                {ref}
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Source */}
      {sourceUrl && (
        <div className="mb-6">
          <h4 className="text-xs font-medium uppercase tracking-wider mb-2" style={{ color: "rgba(0,0,0,0.4)" }}>
            Source
          </h4>
          <a
            href={sourceUrl}
            target="_blank"
            rel="noopener noreferrer"
            className="font-mono text-xs underline break-all"
            style={{ color: "#0f3460" }}
          >
            {sourceUrl}
          </a>
        </div>
      )}
    </article>
  );
}

function LoadingPulse() {
  return (
    <div>
      <div className="h-3 mb-2 animate-pulse" style={{ width: "100%", background: "#E5E5E5" }} />
      <div className="h-3 mb-2 animate-pulse" style={{ width: "85%", background: "#E5E5E5" }} />
      <div className="h-3 mb-2 animate-pulse" style={{ width: "92%", background: "#E5E5E5" }} />
      <div className="h-3 mb-2 animate-pulse" style={{ width: "60%", background: "#E5E5E5" }} />
    </div>
  );
}
