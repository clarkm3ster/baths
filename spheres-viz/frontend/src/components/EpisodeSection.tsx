import { useRef } from 'react';
import { useElementProgress, useInView } from '../hooks/useScrollProgress';
import type { Episode } from '../data/episodes';

interface EpisodeSectionProps {
  episode: Episode;
  index: number;
  onOpenWorld: (slug: string) => void;
}

/**
 * A single episode section occupying 200vh of scroll space.
 *
 * Phase 1 (first 100vh): The Reveal
 *   - Genre tag, location, title slide up
 *   - Background color wash from the episode's palette
 *
 * Phase 2 (second 100vh): The Story
 *   - Opening narrative text
 *   - "Step Into This Sphere" CTA
 *   - Two-column layout: description + stats
 *   - Permanence bar visualization
 */
export default function EpisodeSection({
  episode,
  index,
  onOpenWorld,
}: EpisodeSectionProps) {
  const sectionRef = useRef<HTMLDivElement>(null);
  const phase1Ref = useRef<HTMLDivElement>(null);
  const phase2Ref = useRef<HTMLDivElement>(null);

  const sectionProgress = useElementProgress(sectionRef);
  const phase1Progress = useElementProgress(phase1Ref);
  const phase2Progress = useElementProgress(phase2Ref);

  const phase2InView = useInView(phase2Ref, { threshold: 0.1 });

  // Phase 1 sub-animations (mapped to phase1Progress 0-1)
  // Genre tag fades in early
  const genreOpacity = clamp((phase1Progress - 0.15) * 5, 0, 1);
  const genreTranslateY = lerp(30, 0, clamp((phase1Progress - 0.15) * 5, 0, 1));

  // Location fades in slightly after
  const locationOpacity = clamp((phase1Progress - 0.22) * 5, 0, 1);

  // Title slides up
  const titleOpacity = clamp((phase1Progress - 0.28) * 4, 0, 1);
  const titleTranslateY = lerp(60, 0, clamp((phase1Progress - 0.28) * 4, 0, 1));

  // Subtitle fades in last
  const subtitleOpacity = clamp((phase1Progress - 0.38) * 4, 0, 1);

  // Background color wash — starts transparent, becomes the dark palette color
  const bgOpacity = clamp(sectionProgress * 3, 0, 1);
  const bgFadeOut = clamp((sectionProgress - 0.85) * 6, 0, 1);
  const effectiveBgOpacity = bgOpacity * (1 - bgFadeOut);

  // Phase 2 sub-animations
  const quoteOpacity = clamp((phase2Progress - 0.12) * 4, 0, 1);
  const quoteTranslateY = lerp(40, 0, clamp((phase2Progress - 0.12) * 4, 0, 1));

  const ctaOpacity = clamp((phase2Progress - 0.25) * 4, 0, 1);
  const ctaScale = lerp(0.9, 1, clamp((phase2Progress - 0.25) * 4, 0, 1));

  const detailsOpacity = clamp((phase2Progress - 0.32) * 3, 0, 1);
  const detailsTranslateY = lerp(50, 0, clamp((phase2Progress - 0.32) * 3, 0, 1));

  const episodeNum = String(episode.number).padStart(2, '0');

  return (
    <div
      ref={sectionRef}
      style={{
        position: 'relative',
        minHeight: '200vh',
      }}
    >
      {/* Background color wash */}
      <div
        style={{
          position: 'fixed',
          inset: 0,
          backgroundColor: episode.palette.dark,
          opacity: effectiveBgOpacity,
          pointerEvents: 'none',
          zIndex: 0,
          transition: 'opacity 0.1s linear',
        }}
      />

      {/* Gradient accent line at the left edge */}
      <div
        style={{
          position: 'fixed',
          left: 0,
          top: 0,
          bottom: 0,
          width: 3,
          background: `linear-gradient(to bottom, transparent, ${episode.genre_color}, transparent)`,
          opacity: effectiveBgOpacity * 0.6,
          pointerEvents: 'none',
          zIndex: 1,
        }}
      />

      {/* ============ PHASE 1: THE REVEAL ============ */}
      <div
        ref={phase1Ref}
        style={{
          height: '100vh',
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'center',
          alignItems: 'center',
          position: 'relative',
          zIndex: 2,
          padding: '0 24px',
        }}
      >
        {/* Genre tag */}
        <div
          style={{
            opacity: genreOpacity,
            transform: `translateY(${genreTranslateY}px)`,
            willChange: 'transform, opacity',
            marginBottom: 16,
          }}
        >
          <span
            style={{
              fontFamily: 'Inter, sans-serif',
              fontSize: 13,
              fontWeight: 600,
              letterSpacing: '0.15em',
              textTransform: 'uppercase',
              color: episode.genre_color,
              padding: '6px 16px',
              border: `1px solid ${episode.genre_color}40`,
              borderRadius: 4,
            }}
          >
            Episode {episodeNum} — {episode.genre}
          </span>
        </div>

        {/* Location */}
        <p
          style={{
            opacity: locationOpacity,
            willChange: 'opacity',
            fontFamily: 'Inter, sans-serif',
            fontSize: 14,
            fontWeight: 400,
            color: 'rgba(255,255,255,0.5)',
            letterSpacing: '0.05em',
            marginBottom: 24,
            textAlign: 'center',
          }}
        >
          {episode.location}
        </p>

        {/* Title */}
        <h2
          style={{
            opacity: titleOpacity,
            transform: `translateY(${titleTranslateY}px)`,
            willChange: 'transform, opacity',
            fontFamily: 'Inter, sans-serif',
            fontSize: 'clamp(36px, 7vw, 80px)',
            fontWeight: 800,
            color: '#ffffff',
            textAlign: 'center',
            lineHeight: 1.05,
            margin: 0,
            maxWidth: 900,
          }}
        >
          {episode.title}
        </h2>

        {/* Subtitle */}
        <p
          style={{
            opacity: subtitleOpacity,
            willChange: 'opacity',
            fontFamily: 'Inter, sans-serif',
            fontSize: 'clamp(16px, 2.5vw, 22px)',
            fontWeight: 300,
            color: 'rgba(255,255,255,0.6)',
            textAlign: 'center',
            marginTop: 16,
            fontStyle: 'italic',
            maxWidth: 600,
          }}
        >
          {episode.subtitle}
        </p>
      </div>

      {/* ============ PHASE 2: THE STORY ============ */}
      <div
        ref={phase2Ref}
        style={{
          minHeight: '100vh',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          position: 'relative',
          zIndex: 2,
          padding: '80px 24px',
        }}
      >
        {/* Opening text / narrative hook */}
        <blockquote
          style={{
            opacity: quoteOpacity,
            transform: `translateY(${quoteTranslateY}px)`,
            willChange: 'transform, opacity',
            fontFamily: 'Inter, sans-serif',
            fontSize: 'clamp(18px, 2.5vw, 26px)',
            fontWeight: 300,
            color: 'rgba(255,255,255,0.85)',
            lineHeight: 1.7,
            maxWidth: 750,
            textAlign: 'center',
            margin: '0 auto 48px',
            padding: '0 20px',
            borderLeft: 'none',
            position: 'relative',
          }}
        >
          <span
            style={{
              position: 'absolute',
              top: -30,
              left: '50%',
              transform: 'translateX(-50%)',
              fontSize: 60,
              color: episode.genre_color,
              opacity: 0.3,
              fontFamily: 'Georgia, serif',
              lineHeight: 1,
            }}
          >
            &ldquo;
          </span>
          {episode.opening_text}
        </blockquote>

        {/* Step Into This Sphere button */}
        <div
          style={{
            opacity: ctaOpacity,
            transform: `scale(${ctaScale})`,
            willChange: 'transform, opacity',
            marginBottom: 64,
          }}
        >
          <button
            onClick={() => onOpenWorld(episode.slug)}
            style={{
              fontFamily: 'Inter, sans-serif',
              fontSize: 16,
              fontWeight: 600,
              color: '#000000',
              backgroundColor: episode.genre_color,
              border: 'none',
              padding: '16px 40px',
              borderRadius: 8,
              cursor: 'pointer',
              letterSpacing: '0.03em',
              boxShadow: `0 0 30px ${episode.genre_color}50, 0 0 60px ${episode.genre_color}25`,
              transition: 'box-shadow 0.3s ease, transform 0.2s ease',
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.boxShadow = `0 0 40px ${episode.genre_color}80, 0 0 80px ${episode.genre_color}40`;
              e.currentTarget.style.transform = 'scale(1.05)';
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.boxShadow = `0 0 30px ${episode.genre_color}50, 0 0 60px ${episode.genre_color}25`;
              e.currentTarget.style.transform = 'scale(1)';
            }}
          >
            Step Into This Sphere
          </button>
        </div>

        {/* Two-column details: description + stats */}
        <div
          style={{
            opacity: detailsOpacity,
            transform: `translateY(${detailsTranslateY}px)`,
            willChange: 'transform, opacity',
            display: 'grid',
            gridTemplateColumns: 'minmax(0, 1fr) minmax(0, 1fr)',
            gap: 48,
            maxWidth: 1000,
            width: '100%',
          }}
          className="episode-details-grid"
        >
          {/* Left column: description */}
          <div>
            <h3
              style={{
                fontFamily: 'Inter, sans-serif',
                fontSize: 13,
                fontWeight: 600,
                letterSpacing: '0.12em',
                textTransform: 'uppercase',
                color: episode.genre_color,
                marginBottom: 16,
              }}
            >
              The Activation
            </h3>
            <p
              style={{
                fontFamily: 'Inter, sans-serif',
                fontSize: 15,
                fontWeight: 400,
                color: 'rgba(255,255,255,0.7)',
                lineHeight: 1.75,
              }}
            >
              {episode.description}
            </p>
          </div>

          {/* Right column: stats */}
          <div>
            <h3
              style={{
                fontFamily: 'Inter, sans-serif',
                fontSize: 13,
                fontWeight: 600,
                letterSpacing: '0.12em',
                textTransform: 'uppercase',
                color: episode.genre_color,
                marginBottom: 16,
              }}
            >
              By the Numbers
            </h3>

            {/* Stat rows */}
            <div style={{ display: 'flex', flexDirection: 'column', gap: 14 }}>
              <StatRow
                label="Estimated Cost"
                value={`$${formatK(episode.stats.cost_low)}\u2013$${formatK(episode.stats.cost_high)}`}
                color={episode.genre_color}
              />
              <StatRow
                label="Timeline"
                value={episode.stats.timeline}
                color={episode.genre_color}
              />
              <StatRow
                label="Jobs Created"
                value={String(episode.stats.jobs_created)}
                color={episode.genre_color}
              />
              <StatRow
                label="People Served Annually"
                value={episode.stats.people_served.toLocaleString()}
                color={episode.genre_color}
              />
            </div>

            {/* Permanence bar */}
            <div style={{ marginTop: 24 }}>
              <div
                style={{
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'baseline',
                  marginBottom: 8,
                }}
              >
                <span
                  style={{
                    fontFamily: 'Inter, sans-serif',
                    fontSize: 12,
                    fontWeight: 500,
                    color: 'rgba(255,255,255,0.5)',
                    textTransform: 'uppercase',
                    letterSpacing: '0.1em',
                  }}
                >
                  Permanence
                </span>
                <span
                  style={{
                    fontFamily: 'Inter, sans-serif',
                    fontSize: 20,
                    fontWeight: 700,
                    color: episode.genre_color,
                  }}
                >
                  {episode.stats.permanence_pct}%
                </span>
              </div>

              {/* Bar track */}
              <div
                style={{
                  width: '100%',
                  height: 6,
                  backgroundColor: 'rgba(255,255,255,0.08)',
                  borderRadius: 3,
                  overflow: 'hidden',
                }}
              >
                <div
                  style={{
                    width: phase2InView
                      ? `${episode.stats.permanence_pct}%`
                      : '0%',
                    height: '100%',
                    backgroundColor: episode.genre_color,
                    borderRadius: 3,
                    transition: 'width 1.5s cubic-bezier(0.22, 1, 0.36, 1)',
                    boxShadow: `0 0 8px ${episode.genre_color}60`,
                  }}
                />
              </div>

              {/* Permanent elements */}
              <div
                style={{
                  display: 'flex',
                  flexWrap: 'wrap',
                  gap: 6,
                  marginTop: 12,
                }}
              >
                {episode.stats.permanent_elements.map((el) => (
                  <span
                    key={el}
                    style={{
                      fontFamily: 'Inter, sans-serif',
                      fontSize: 11,
                      fontWeight: 500,
                      color: episode.genre_color,
                      backgroundColor: `${episode.genre_color}15`,
                      padding: '3px 10px',
                      borderRadius: 12,
                      border: `1px solid ${episode.genre_color}30`,
                    }}
                  >
                    {el}
                  </span>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

/* ── Helpers ─────────────────────────────────────── */

function StatRow({
  label,
  value,
  color,
}: {
  label: string;
  value: string;
  color: string;
}) {
  return (
    <div
      style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'baseline',
        borderBottom: '1px solid rgba(255,255,255,0.06)',
        paddingBottom: 10,
      }}
    >
      <span
        style={{
          fontFamily: 'Inter, sans-serif',
          fontSize: 13,
          fontWeight: 400,
          color: 'rgba(255,255,255,0.45)',
        }}
      >
        {label}
      </span>
      <span
        style={{
          fontFamily: 'Inter, sans-serif',
          fontSize: 15,
          fontWeight: 600,
          color: color,
        }}
      >
        {value}
      </span>
    </div>
  );
}

function clamp(v: number, min: number, max: number): number {
  return Math.max(min, Math.min(max, v));
}

function lerp(a: number, b: number, t: number): number {
  return a + (b - a) * t;
}

function formatK(n: number): string {
  if (n >= 1000000) return `${(n / 1000000).toFixed(1)}M`;
  if (n >= 1000) return `${Math.round(n / 1000)}K`;
  return String(n);
}
