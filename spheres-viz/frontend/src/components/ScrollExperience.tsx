import { useRef, useMemo, useCallback } from 'react';
import {
  useScrollProgress,
  useElementProgress,
  useInView,
} from '../hooks/useScrollProgress';
import { EPISODES, getAggregateStats } from '../data/episodes';
import type { EpisodeSummary } from '../utils/api';
import EpisodeSection from './EpisodeSection';
import PhillyMap from './PhillyMap';
import ParticleField from './ParticleField';
import Counter from './Counter';

// ---------------------------------------------------------------------------
// ScrollExperience -- THE component. The entire website is this.
// ---------------------------------------------------------------------------
// Layout (scroll-space):
//   Section 0:  Opening            100vh
//   Sections 1-10: Episodes        200vh each + 50vh map transition = 250vh each
//   Section 11: Finale             150vh
//   Total scroll height:           100 + (10 * 250) + 150 = 2750vh
// ---------------------------------------------------------------------------

interface ScrollExperienceProps {
  episodes: EpisodeSummary[];
  onOpenWorld: (slug: string) => void;
}

export default function ScrollExperience({
  episodes: _apiEpisodes,
  onOpenWorld,
}: ScrollExperienceProps) {
  // We use the rich local EPISODES data for rendering, but the API episodes
  // confirm which slugs are available. The onOpenWorld callback is passed
  // directly to episode sections.
  const { activeEpisodeIndex } = useScrollProgress();

  const openingRef = useRef<HTMLDivElement>(null);
  const finaleRef = useRef<HTMLDivElement>(null);

  const openingProgress = useElementProgress(openingRef);
  const finaleProgress = useElementProgress(finaleRef);

  const finaleInView = useInView(finaleRef, { threshold: 0.05 });

  const aggregateStats = useMemo(() => getAggregateStats(EPISODES), []);

  const handleOpenWorld = useCallback(
    (slug: string) => {
      onOpenWorld(slug);
    },
    [onOpenWorld],
  );

  // -- Opening section text animations --
  const line1Opacity = clamp((openingProgress - 0.08) * 6, 0, 1);
  const line1TranslateY = lerp(40, 0, clamp((openingProgress - 0.08) * 6, 0, 1));

  const line2Opacity = clamp((openingProgress - 0.25) * 5, 0, 1);
  const line2TranslateY = lerp(40, 0, clamp((openingProgress - 0.25) * 5, 0, 1));

  const line3Opacity = clamp((openingProgress - 0.42) * 5, 0, 1);
  const line3TranslateY = lerp(40, 0, clamp((openingProgress - 0.42) * 5, 0, 1));

  // Down arrow pulses and fades as user scrolls
  const arrowOpacity = clamp(1 - openingProgress * 3, 0, 0.6);

  // -- Finale section animations --
  const finalePhase1 = clamp(finaleProgress * 3, 0, 1);
  const finalePhase2 = clamp((finaleProgress - 0.33) * 3, 0, 1);
  const finalePhase3 = clamp((finaleProgress - 0.6) * 2.5, 0, 1);

  // Activated episodes for map: all episodes up to and including current
  const activatedForMap = useMemo(() => {
    if (activeEpisodeIndex < 0) return [];
    return Array.from({ length: activeEpisodeIndex + 1 }, (_, i) => i + 1);
  }, [activeEpisodeIndex]);

  // All episodes activated for the finale
  const allActivated = useMemo(() => EPISODES.map((e) => e.number), []);

  return (
    <div
      style={{
        backgroundColor: '#000000',
        color: '#ffffff',
        fontFamily: 'Inter, sans-serif',
        position: 'relative',
      }}
    >
      {/* ================================================================
          SECTION 0: OPENING (100vh)
          ================================================================ */}
      <section
        ref={openingRef}
        style={{
          height: '100vh',
          position: 'relative',
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'center',
          alignItems: 'center',
          overflow: 'hidden',
        }}
      >
        {/* Particle field background */}
        <ParticleField particleCount={60} />

        {/* Opening text */}
        <div
          style={{
            position: 'relative',
            zIndex: 2,
            textAlign: 'center',
            padding: '0 24px',
            maxWidth: 800,
          }}
        >
          <p
            style={{
              opacity: line1Opacity,
              transform: `translateY(${line1TranslateY}px)`,
              willChange: 'transform, opacity',
              fontSize: 'clamp(22px, 4vw, 42px)',
              fontWeight: 300,
              lineHeight: 1.4,
              color: 'rgba(255,255,255,0.9)',
              margin: '0 0 32px 0',
            }}
          >
            Every city has space it has forgotten.
          </p>

          <p
            style={{
              opacity: line2Opacity,
              transform: `translateY(${line2TranslateY}px)`,
              willChange: 'transform, opacity',
              fontSize: 'clamp(22px, 4vw, 42px)',
              fontWeight: 300,
              lineHeight: 1.4,
              color: 'rgba(255,255,255,0.9)',
              margin: '0 0 32px 0',
            }}
          >
            Philadelphia has{' '}
            <span style={{ fontWeight: 700, color: '#ffffff' }}>
              40,000 parcels
            </span>{' '}
            of it.
          </p>

          <p
            style={{
              opacity: line3Opacity,
              transform: `translateY(${line3TranslateY}px)`,
              willChange: 'transform, opacity',
              fontSize: 'clamp(24px, 4.5vw, 48px)',
              fontWeight: 600,
              lineHeight: 1.3,
              color: '#ffffff',
              margin: 0,
            }}
          >
            What if we activated just 10?
          </p>
        </div>

        {/* Down arrow indicator */}
        <div
          style={{
            position: 'absolute',
            bottom: 40,
            left: '50%',
            transform: 'translateX(-50%)',
            opacity: arrowOpacity,
            willChange: 'opacity',
          }}
          className="animate-float"
        >
          <svg
            width="24"
            height="24"
            viewBox="0 0 24 24"
            fill="none"
            stroke="rgba(255,255,255,0.6)"
            strokeWidth="1.5"
            strokeLinecap="round"
            strokeLinejoin="round"
          >
            <polyline points="6 9 12 15 18 9" />
          </svg>
        </div>
      </section>

      {/* ================================================================
          SECTIONS 1-10: EPISODES
          Each: 200vh episode + 50vh map transition
          ================================================================ */}
      {EPISODES.map((episode, i) => (
        <div key={episode.slug}>
          {/* Episode content */}
          <EpisodeSection
            episode={episode}
            index={i}
            onOpenWorld={handleOpenWorld}
          />

          {/* Map transition between episodes */}
          <MapTransition
            episodeNumber={episode.number}
            activatedEpisodes={activatedForMap.filter(
              (n) => n <= episode.number,
            )}
            genreColor={episode.genre_color}
          />
        </div>
      ))}

      {/* ================================================================
          SECTION 11: FINALE (150vh)
          ================================================================ */}
      <section
        ref={finaleRef}
        style={{
          minHeight: '150vh',
          position: 'relative',
          overflow: 'hidden',
        }}
      >
        <ParticleField particleCount={40} color="200, 200, 255" />

        {/* Phase 1: The Map */}
        <div
          style={{
            minHeight: '100vh',
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'center',
            alignItems: 'center',
            position: 'relative',
            zIndex: 2,
            padding: '80px 24px',
          }}
        >
          <div
            style={{
              opacity: finalePhase1,
              transform: `scale(${lerp(0.85, 1, finalePhase1)})`,
              willChange: 'transform, opacity',
              marginBottom: 48,
            }}
          >
            <PhillyMap
              activatedEpisodes={finaleInView ? allActivated : []}
              size="large"
            />
          </div>

          <h2
            style={{
              opacity: finalePhase1,
              willChange: 'opacity',
              fontFamily: 'Inter, sans-serif',
              fontSize: 'clamp(24px, 4vw, 44px)',
              fontWeight: 700,
              textAlign: 'center',
              color: '#ffffff',
              margin: '0 0 48px 0',
              lineHeight: 1.3,
            }}
          >
            10 spheres. 10 stories.
            <br />
            One city transformed.
          </h2>

          {/* Aggregate stats */}
          <div
            style={{
              opacity: finalePhase1,
              willChange: 'opacity',
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fit, minmax(160px, 1fr))',
              gap: 32,
              maxWidth: 700,
              width: '100%',
            }}
          >
            <AggStat label="Total Investment">
              <Counter
                target={aggregateStats.totalCostLow}
                prefix="$"
                duration={2500}
              />
              {' \u2013 '}
              <Counter
                target={aggregateStats.totalCostHigh}
                prefix="$"
                duration={2500}
              />
            </AggStat>

            <AggStat label="Jobs Created">
              <Counter target={aggregateStats.totalJobs} duration={2000} />
            </AggStat>

            <AggStat label="People Served">
              <Counter
                target={aggregateStats.totalPeopleServed}
                duration={2500}
              />
            </AggStat>

            <AggStat label="Avg. Permanence">
              <Counter
                target={aggregateStats.avgPermanence}
                suffix="%"
                duration={1800}
              />
            </AggStat>
          </div>
        </div>

        {/* Phase 2: The Question */}
        <div
          style={{
            minHeight: '50vh',
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'center',
            alignItems: 'center',
            position: 'relative',
            zIndex: 2,
            padding: '0 24px',
          }}
        >
          <p
            style={{
              opacity: finalePhase2,
              transform: `scale(${lerp(0.9, 1, finalePhase2)})`,
              willChange: 'transform, opacity',
              fontFamily: 'Inter, sans-serif',
              fontSize: 'clamp(26px, 5vw, 54px)',
              fontWeight: 700,
              textAlign: 'center',
              color: '#ffffff',
              lineHeight: 1.3,
              margin: '0 0 24px 0',
              maxWidth: 900,
            }}
          >
            What would your city look like
            <br />
            with <span style={{ color: '#7B68EE' }}>1,000</span> spheres?
          </p>

          <p
            style={{
              opacity: clamp((finalePhase2 - 0.5) * 2, 0, 1),
              willChange: 'opacity',
              fontFamily: 'Inter, sans-serif',
              fontSize: 'clamp(28px, 6vw, 64px)',
              fontWeight: 800,
              textAlign: 'center',
              color: '#ffffff',
              margin: 0,
            }}
          >
            What about{' '}
            <span
              style={{
                background:
                  'linear-gradient(135deg, #7B68EE, #00E5FF, #76FF03, #FFD740)',
                WebkitBackgroundClip: 'text',
                WebkitTextFillColor: 'transparent',
                backgroundClip: 'text',
              }}
            >
              40,000
            </span>
            ?
          </p>
        </div>

        {/* Phase 3: CTAs */}
        <div
          style={{
            minHeight: '50vh',
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'center',
            alignItems: 'center',
            position: 'relative',
            zIndex: 2,
            padding: '60px 24px 120px',
          }}
        >
          <div
            style={{
              opacity: finalePhase3,
              transform: `translateY(${lerp(60, 0, finalePhase3)}px)`,
              willChange: 'transform, opacity',
              display: 'grid',
              gap: 24,
              maxWidth: 1000,
              width: '100%',
            }}
            className="cta-grid"
          >
            <CTACard
              title="Explore the Map"
              description="See every dormant parcel in Philadelphia"
              href="/spheres-assets"
              accentColor="#7B68EE"
            />
            <CTACard
              title="Design Your Own"
              description="Create an activation in 20 minutes"
              href="/spheres-studio"
              accentColor="#00E5FF"
            />
            <CTACard
              title="Learn the Legal Pathway"
              description="Every permit, every contract, every law"
              href="/spheres-legal"
              accentColor="#76FF03"
            />
          </div>

          {/* Footer tagline */}
          <p
            style={{
              opacity: finalePhase3 * 0.5,
              willChange: 'opacity',
              fontFamily: 'Inter, sans-serif',
              fontSize: 13,
              fontWeight: 400,
              color: 'rgba(255,255,255,0.3)',
              textAlign: 'center',
              marginTop: 80,
            }}
          >
            SPHERES -- An anthology of activated public space
          </p>
        </div>
      </section>
    </div>
  );
}

/* ==================================================================
   SUB-COMPONENTS
   ================================================================== */

/**
 * Map transition shown between episodes.
 * 50vh of scroll space showing the mini Philly map with
 * currently-activated dots and a running counter.
 */
function MapTransition({
  episodeNumber,
  activatedEpisodes,
  genreColor,
}: {
  episodeNumber: number;
  activatedEpisodes: number[];
  genreColor: string;
}) {
  const ref = useRef<HTMLDivElement>(null);
  const progress = useElementProgress(ref);

  const contentOpacity = clamp((progress - 0.1) * 4, 0, 1);

  return (
    <div
      ref={ref}
      style={{
        height: '50vh',
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        alignItems: 'center',
        position: 'relative',
        zIndex: 2,
      }}
    >
      <div
        style={{
          opacity: contentOpacity,
          willChange: 'opacity',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          gap: 16,
        }}
      >
        <PhillyMap activatedEpisodes={activatedEpisodes} size="mini" />

        <p
          style={{
            fontFamily: 'Inter, sans-serif',
            fontSize: 14,
            fontWeight: 500,
            color: genreColor,
            letterSpacing: '0.05em',
            margin: 0,
          }}
        >
          {episodeNumber} sphere{episodeNumber !== 1 ? 's' : ''} activated...
        </p>
      </div>
    </div>
  );
}

/**
 * Aggregate stat display for the finale section.
 */
function AggStat({
  label,
  children,
}: {
  label: string;
  children: React.ReactNode;
}) {
  return (
    <div style={{ textAlign: 'center' }}>
      <div
        style={{
          fontFamily: 'Inter, sans-serif',
          fontSize: 'clamp(20px, 3vw, 32px)',
          fontWeight: 700,
          color: '#ffffff',
          marginBottom: 4,
        }}
      >
        {children}
      </div>
      <div
        style={{
          fontFamily: 'Inter, sans-serif',
          fontSize: 12,
          fontWeight: 500,
          color: 'rgba(255,255,255,0.4)',
          textTransform: 'uppercase',
          letterSpacing: '0.1em',
        }}
      >
        {label}
      </div>
    </div>
  );
}

/**
 * CTA card for the finale section.
 */
function CTACard({
  title,
  description,
  href,
  accentColor,
}: {
  title: string;
  description: string;
  href: string;
  accentColor: string;
}) {
  return (
    <a
      href={href}
      style={{
        display: 'block',
        textDecoration: 'none',
        padding: '32px 28px',
        borderRadius: 12,
        border: `1px solid ${accentColor}30`,
        backgroundColor: `${accentColor}08`,
        transition:
          'border-color 0.3s ease, background-color 0.3s ease, transform 0.2s ease',
        cursor: 'pointer',
      }}
      onMouseEnter={(e) => {
        e.currentTarget.style.borderColor = `${accentColor}80`;
        e.currentTarget.style.backgroundColor = `${accentColor}15`;
        e.currentTarget.style.transform = 'translateY(-4px)';
      }}
      onMouseLeave={(e) => {
        e.currentTarget.style.borderColor = `${accentColor}30`;
        e.currentTarget.style.backgroundColor = `${accentColor}08`;
        e.currentTarget.style.transform = 'translateY(0)';
      }}
    >
      <h3
        style={{
          fontFamily: 'Inter, sans-serif',
          fontSize: 20,
          fontWeight: 700,
          color: accentColor,
          margin: '0 0 8px 0',
        }}
      >
        {title}
      </h3>
      <p
        style={{
          fontFamily: 'Inter, sans-serif',
          fontSize: 14,
          fontWeight: 400,
          color: 'rgba(255,255,255,0.6)',
          margin: 0,
          lineHeight: 1.5,
        }}
      >
        {description}
      </p>
      <div
        style={{
          marginTop: 16,
          fontFamily: 'Inter, sans-serif',
          fontSize: 13,
          fontWeight: 600,
          color: accentColor,
          display: 'flex',
          alignItems: 'center',
          gap: 6,
        }}
      >
        Explore
        <svg
          width="14"
          height="14"
          viewBox="0 0 24 24"
          fill="none"
          stroke={accentColor}
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
        >
          <line x1="5" y1="12" x2="19" y2="12" />
          <polyline points="12 5 19 12 12 19" />
        </svg>
      </div>
    </a>
  );
}

/* -- Utility functions -------------------------------------------- */

function clamp(v: number, min: number, max: number): number {
  return Math.max(min, Math.min(max, v));
}

function lerp(a: number, b: number, t: number): number {
  return a + (b - a) * t;
}
