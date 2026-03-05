import { useEffect, useState } from 'react';

interface PermanenceOverlayProps {
  permanenceItems: string[];
  permanencePercent: number;
  episodeTitle: string;
}

export default function PermanenceOverlay({
  permanenceItems,
  permanencePercent,
  episodeTitle,
}: PermanenceOverlayProps) {
  const [opacity, setOpacity] = useState(0);

  useEffect(() => {
    let raf: number;
    const start = performance.now();
    const duration = 2000;

    const animate = (now: number) => {
      const elapsed = now - start;
      const t = Math.min(elapsed / duration, 1);
      // ease-out cubic
      const eased = 1 - Math.pow(1 - t, 3);
      setOpacity(eased);
      if (t < 1) raf = requestAnimationFrame(animate);
    };

    raf = requestAnimationFrame(animate);
    return () => cancelAnimationFrame(raf);
  }, []);

  return (
    <div
      style={{
        position: 'absolute',
        inset: 0,
        zIndex: 30,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        pointerEvents: opacity > 0.5 ? 'auto' : 'none',
        opacity,
        transition: 'none',
      }}
    >
      {/* Backdrop */}
      <div
        style={{
          position: 'absolute',
          inset: 0,
          backgroundColor: 'rgba(0, 0, 0, 0.75)',
          backdropFilter: 'blur(8px)',
          WebkitBackdropFilter: 'blur(8px)',
        }}
      />

      {/* Content */}
      <div
        style={{
          position: 'relative',
          zIndex: 1,
          maxWidth: 520,
          width: '90%',
          padding: '48px 40px',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          gap: 28,
          color: '#fff',
          textAlign: 'center',
          fontFamily:
            "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
        }}
      >
        {/* Episode context */}
        <p
          style={{
            fontSize: 13,
            letterSpacing: '0.12em',
            textTransform: 'uppercase',
            opacity: 0.5,
            margin: 0,
          }}
        >
          {episodeTitle}
        </p>

        {/* Main heading */}
        <h2
          style={{
            fontSize: permanencePercent === 100 ? 26 : 22,
            fontWeight: permanencePercent === 100 ? 400 : 300,
            letterSpacing: '0.04em',
            margin: 0,
            lineHeight: 1.4,
            opacity: 0.85,
          }}
        >
          {permanencePercent === 100
            ? '100% permanence.'
            : 'When the show ends, this stays:'}
        </h2>

        {/* Permanence percentage */}
        <div
          style={{
            display: 'flex',
            alignItems: 'baseline',
            gap: 6,
          }}
        >
          <span
            style={{
              fontSize: 72,
              fontWeight: 200,
              lineHeight: 1,
              background:
                'linear-gradient(135deg, #fff 0%, rgba(255,255,255,0.6) 100%)',
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent',
            }}
          >
            {permanencePercent}
          </span>
          <span
            style={{
              fontSize: 28,
              fontWeight: 200,
              opacity: 0.6,
            }}
          >
            %
          </span>
        </div>

        {/* Permanence items */}
        <ul
          style={{
            listStyle: 'none',
            padding: 0,
            margin: 0,
            display: 'flex',
            flexDirection: 'column',
            gap: 12,
            width: '100%',
          }}
        >
          {permanenceItems.map((item, i) => (
            <li
              key={i}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: 12,
                fontSize: 15,
                fontWeight: 400,
                opacity: 0.8,
                textAlign: 'left',
              }}
            >
              <span
                style={{
                  display: 'inline-flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  width: 22,
                  height: 22,
                  borderRadius: '50%',
                  backgroundColor: 'rgba(74, 222, 128, 0.2)',
                  flexShrink: 0,
                }}
              >
                <svg
                  width="12"
                  height="12"
                  viewBox="0 0 12 12"
                  fill="none"
                  stroke="#4ade80"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                >
                  <polyline points="2,6 5,9 10,3" />
                </svg>
              </span>
              {item}
            </li>
          ))}
        </ul>

        {/* Closing line */}
        <p
          style={{
            fontSize: permanencePercent === 100 ? 18 : 14,
            fontWeight: permanencePercent === 100 ? 400 : 300,
            letterSpacing: '0.06em',
            opacity: permanencePercent === 100 ? 0.7 : 0.45,
            margin: '8px 0 0 0',
            fontStyle: 'italic',
          }}
        >
          {permanencePercent === 100
            ? 'The entire garden stays. Forever.'
            : 'This is what SPHERES leaves behind.'}
        </p>
      </div>
    </div>
  );
}
