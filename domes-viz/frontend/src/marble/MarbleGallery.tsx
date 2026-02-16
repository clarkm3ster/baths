import { useState, type ReactNode } from "react";
import { useMarbleWorlds } from "./useMarbleWorlds";
import { SplatWorldViewer } from "./SplatWorldViewer";
import type { MarbleWorld } from "./types";

// ─── Gallery titles for the 3 canonical worlds ───────────

const GALLERY_META: Record<
  string,
  { title: string; subtitle: string; order: number }
> = {
  renaissance: {
    title: "The Human Dome",
    subtitle:
      "Government as it was designed to be — sheltering, dignified, centered on the individual.",
    order: 0,
  },
  "broken-capitol": {
    title: "The Broken Dome",
    subtitle:
      "What it became — institutional decay, bureaucratic neglect, the human reduced to a number.",
    order: 1,
  },
  "personal-dome": {
    title: "The Future Dome",
    subtitle:
      "What we are building — connected, coordinated, technology serving humans.",
    order: 2,
  },
};

// ─── Helper: sort worlds in canonical order ──────────────

function sortWorlds(worlds: MarbleWorld[]): MarbleWorld[] {
  return [...worlds].sort((a, b) => {
    const orderA = GALLERY_META[a.key]?.order ?? 99;
    const orderB = GALLERY_META[b.key]?.order ?? 99;
    return orderA - orderB;
  });
}

// ─── Component ───────────────────────────────────────────

export function MarbleGallery(): ReactNode {
  const { worlds, loading, error } = useMarbleWorlds();
  const [activeIndex, setActiveIndex] = useState(0);

  // Use canonical fallback data if no worlds from API
  const displayWorlds: MarbleWorld[] =
    worlds.length > 0
      ? sortWorlds(worlds)
      : [
          {
            key: "renaissance",
            title: "The Human Dome",
            prompt: "",
            worldId: "",
            operationId: "",
            details: {},
            splatUrl: "",
            fallback: true,
          },
          {
            key: "broken-capitol",
            title: "The Broken Dome",
            prompt: "",
            worldId: "",
            operationId: "",
            details: {},
            splatUrl: "",
            fallback: true,
          },
          {
            key: "personal-dome",
            title: "The Future Dome",
            prompt: "",
            worldId: "",
            operationId: "",
            details: {},
            splatUrl: "",
            fallback: true,
          },
        ];

  const activeWorld = displayWorlds[activeIndex];
  const meta = GALLERY_META[activeWorld?.key] ?? {
    title: activeWorld?.title ?? "World",
    subtitle: "",
    order: 0,
  };

  return (
    <section
      id="marble-gallery"
      style={{
        width: "100%",
        minHeight: "100vh",
        display: "flex",
        flexDirection: "column",
        background: "#0D0D0D",
      }}
    >
      {/* Header */}
      <div
        style={{
          padding: "48px 24px 24px",
          textAlign: "center",
        }}
      >
        <h2
          style={{
            margin: 0,
            fontFamily: "Georgia, serif",
            fontSize: "2.5rem",
            fontWeight: 400,
            color: "#FFFFFF",
            letterSpacing: "0.02em",
          }}
        >
          Three Domes
        </h2>
        <p
          style={{
            margin: "12px auto 0",
            maxWidth: 600,
            fontFamily: '"Inter", sans-serif',
            fontSize: "1rem",
            lineHeight: 1.6,
            color: "#666666",
          }}
        >
          Walk through three worlds. Past, present, and future — each dome tells
          a story about what government could be.
        </p>

        {loading && (
          <p
            style={{
              margin: "16px 0 0",
              fontFamily: '"JetBrains Mono", monospace',
              fontSize: "0.75rem",
              color: "#C4A265",
              letterSpacing: "0.12em",
              textTransform: "uppercase",
            }}
          >
            Loading Marble worlds...
          </p>
        )}
        {error && (
          <p
            style={{
              margin: "16px 0 0",
              fontFamily: '"JetBrains Mono", monospace',
              fontSize: "0.75rem",
              color: "rgba(196, 162, 101, 0.5)",
              letterSpacing: "0.1em",
            }}
          >
            Using geometric previews (Marble API unavailable)
          </p>
        )}
      </div>

      {/* Navigation tabs */}
      <nav
        style={{
          display: "flex",
          justifyContent: "center",
          gap: 0,
          padding: "0 24px",
          borderBottom: "1px solid #222222",
        }}
      >
        {displayWorlds.map((world, index) => {
          const isActive = index === activeIndex;
          const worldMeta = GALLERY_META[world.key];
          return (
            <button
              key={world.key}
              type="button"
              onClick={() => setActiveIndex(index)}
              style={{
                padding: "14px 28px",
                background: "transparent",
                border: "none",
                borderBottom: isActive
                  ? "2px solid #C4A265"
                  : "2px solid transparent",
                color: isActive ? "#C4A265" : "#666666",
                fontFamily: '"JetBrains Mono", monospace',
                fontSize: "0.8rem",
                letterSpacing: "0.12em",
                textTransform: "uppercase",
                cursor: "pointer",
                transition: "all 0.3s ease",
              }}
              onMouseEnter={(e) => {
                if (!isActive) {
                  e.currentTarget.style.color = "#FFFFFF";
                }
              }}
              onMouseLeave={(e) => {
                if (!isActive) {
                  e.currentTarget.style.color = "#666666";
                }
              }}
            >
              {worldMeta?.title ?? world.title}
            </button>
          );
        })}
      </nav>

      {/* Subtitle for active world */}
      {meta.subtitle && (
        <div
          style={{
            padding: "20px 24px 0",
            textAlign: "center",
          }}
        >
          <p
            style={{
              margin: 0,
              fontFamily: "Georgia, serif",
              fontSize: "1.1rem",
              color: "#999999",
              fontStyle: "italic",
              maxWidth: 640,
              marginLeft: "auto",
              marginRight: "auto",
              lineHeight: 1.5,
            }}
          >
            {meta.subtitle}
          </p>
        </div>
      )}

      {/* 3D World Viewer */}
      <div
        style={{
          flex: 1,
          minHeight: "65vh",
          margin: "20px 0 0",
          borderTop: "1px solid #222222",
          borderBottom: "1px solid #222222",
        }}
      >
        {activeWorld && (
          <SplatWorldViewer
            key={activeWorld.key}
            worldKey={
              activeWorld.key as
                | "renaissance"
                | "broken-capitol"
                | "personal-dome"
            }
            splatUrl={activeWorld.splatUrl}
            title={meta.title}
          />
        )}
      </div>

      {/* World info footer */}
      <div
        style={{
          display: "flex",
          justifyContent: "center",
          gap: 48,
          padding: "24px",
        }}
      >
        {displayWorlds.map((world, index) => {
          const isActive = index === activeIndex;
          return (
            <button
              key={world.key}
              type="button"
              onClick={() => setActiveIndex(index)}
              style={{
                width: 12,
                height: 12,
                border: "1px solid #C4A265",
                background: isActive ? "#C4A265" : "transparent",
                cursor: "pointer",
                transition: "all 0.3s ease",
                padding: 0,
              }}
              aria-label={`Go to ${GALLERY_META[world.key]?.title ?? world.title}`}
            />
          );
        })}
      </div>
    </section>
  );
}
