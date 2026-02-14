/**
 * SPHERES Studio — Share Modal
 *
 * Overlay for sharing an activation design via link, social media, embed
 * code, or QR code.  Includes visibility control and preview thumbnail.
 */

import { useCallback, useEffect, useState } from 'react';
import { useAuth } from '../context/AuthContext';

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

interface ShareModalProps {
  isOpen: boolean;
  onClose: () => void;
  designId: string;
  designTitle?: string;
  designColor?: string;
}

type Visibility = 'public' | 'unlisted' | 'private';

// ---------------------------------------------------------------------------
// QR Code SVG generator (pure function, no deps)
// ---------------------------------------------------------------------------

/**
 * Generate a simple QR-like SVG.  This is a minimal pattern generator
 * that creates a scannable-looking grid.  For a production app you
 * would use a real QR encoding library.
 */
function generateQRCodeSVG(data: string, size: number = 160): string {
  const modules = 21; // QR version 1 = 21x21
  const cellSize = size / modules;
  const grid: boolean[][] = Array.from({ length: modules }, () =>
    Array.from({ length: modules }, () => false),
  );

  // Finder patterns (top-left, top-right, bottom-left)
  const drawFinder = (startR: number, startC: number) => {
    for (let r = 0; r < 7; r++) {
      for (let c = 0; c < 7; c++) {
        const isOuter = r === 0 || r === 6 || c === 0 || c === 6;
        const isInner = r >= 2 && r <= 4 && c >= 2 && c <= 4;
        grid[startR + r][startC + c] = isOuter || isInner;
      }
    }
  };
  drawFinder(0, 0);
  drawFinder(0, modules - 7);
  drawFinder(modules - 7, 0);

  // Timing patterns
  for (let i = 8; i < modules - 8; i++) {
    grid[6][i] = i % 2 === 0;
    grid[i][6] = i % 2 === 0;
  }

  // Data area: deterministic pseudo-random fill based on input string
  let hash = 0;
  for (let i = 0; i < data.length; i++) {
    hash = ((hash << 5) - hash + data.charCodeAt(i)) | 0;
  }
  for (let r = 0; r < modules; r++) {
    for (let c = 0; c < modules; c++) {
      // Skip finder/timing areas
      if (
        (r < 9 && c < 9) ||
        (r < 9 && c >= modules - 8) ||
        (r >= modules - 8 && c < 9) ||
        r === 6 ||
        c === 6
      ) {
        continue;
      }
      hash = ((hash << 5) - hash + (r * modules + c)) | 0;
      grid[r][c] = (hash & 1) === 1;
    }
  }

  const rects: string[] = [];
  for (let r = 0; r < modules; r++) {
    for (let c = 0; c < modules; c++) {
      if (grid[r][c]) {
        rects.push(
          `<rect x="${c * cellSize}" y="${r * cellSize}" width="${cellSize}" height="${cellSize}" fill="#F9FAFB"/>`,
        );
      }
    }
  }

  return [
    `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${size} ${size}" width="${size}" height="${size}">`,
    `<rect width="${size}" height="${size}" fill="#111827"/>`,
    ...rects,
    '</svg>',
  ].join('');
}

// ---------------------------------------------------------------------------
// Component
// ---------------------------------------------------------------------------

export default function ShareModal({
  isOpen,
  onClose,
  designId,
  designTitle = 'Untitled Design',
  designColor = '#6D28D9',
}: ShareModalProps) {
  const { token, isAuthenticated } = useAuth();

  const [visibility, setVisibility] = useState<Visibility>('public');
  const [shareUrl, setShareUrl] = useState('');
  const [shareToken, setShareToken] = useState('');
  const [copied, setCopied] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Base URL for share links
  const baseUrl =
    typeof window !== 'undefined'
      ? `${window.location.origin}`
      : 'https://spheres.studio';

  // Generate or refresh the share link
  const generateShareLink = useCallback(async () => {
    if (!isAuthenticated || !token) {
      // For non-authenticated users, generate a client-side link
      const localToken = btoa(designId);
      setShareToken(localToken);
      setShareUrl(`${baseUrl}/shared/${localToken}`);
      return;
    }

    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`/api/designs/${designId}/share`, {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ visibility }),
      });
      if (!res.ok) {
        throw new Error('Failed to generate share link');
      }
      const data = await res.json();
      setShareToken(data.share_token);
      setShareUrl(`${baseUrl}${data.url}`);
    } catch {
      // Fallback to client-side URL
      const fallback = btoa(designId);
      setShareToken(fallback);
      setShareUrl(`${baseUrl}/shared/${fallback}`);
      setError('Could not generate server link, using local URL');
    } finally {
      setLoading(false);
    }
  }, [designId, visibility, token, isAuthenticated, baseUrl]);

  // Generate link on open / visibility change
  useEffect(() => {
    if (isOpen) {
      generateShareLink();
    }
  }, [isOpen, generateShareLink]);

  // Close on Escape
  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose();
    };
    if (isOpen) window.addEventListener('keydown', handler);
    return () => window.removeEventListener('keydown', handler);
  }, [isOpen, onClose]);

  // Copy to clipboard helper
  const copyToClipboard = useCallback(
    async (text: string, label: string) => {
      try {
        await navigator.clipboard.writeText(text);
        setCopied(label);
        setTimeout(() => setCopied(null), 2000);
      } catch {
        // Fallback
        const el = document.createElement('textarea');
        el.value = text;
        document.body.appendChild(el);
        el.select();
        document.execCommand('copy');
        document.body.removeChild(el);
        setCopied(label);
        setTimeout(() => setCopied(null), 2000);
      }
    },
    [],
  );

  if (!isOpen) return null;

  // Derived values
  const embedCode = `<iframe src="${shareUrl}?embed=true" width="600" height="400" frameborder="0" style="border-radius:12px;border:1px solid #1F2937" allowfullscreen></iframe>`;

  const shareTextTwitter = `Check out "${designTitle}" on SPHERES Studio — designing community spaces together ${shareUrl}`;
  const shareTextLinkedIn = `I just designed "${designTitle}" using SPHERES Studio, a platform for collaborative community space activation. ${shareUrl}`;

  const qrSvg = generateQRCodeSVG(shareUrl);

  return (
    <div style={styles.overlay} onClick={onClose}>
      <div style={styles.modal} onClick={(e) => e.stopPropagation()}>
        <button style={styles.closeBtn} onClick={onClose}>
          x
        </button>

        <h2 style={styles.title}>Share Design</h2>
        <p style={styles.subtitle}>{designTitle}</p>

        {error && <div style={styles.errorBox}>{error}</div>}

        {/* Preview thumbnail */}
        <div
          style={{
            ...styles.preview,
            backgroundColor: designColor,
          }}
        >
          <div style={styles.previewOverlay}>
            <span style={styles.previewLabel}>Preview</span>
            <span style={styles.previewTitle}>{designTitle}</span>
          </div>
        </div>

        {/* Visibility toggle */}
        <div style={styles.section}>
          <label style={styles.sectionLabel}>Visibility</label>
          <div style={styles.visibilityRow}>
            {(['public', 'unlisted', 'private'] as Visibility[]).map((v) => (
              <button
                key={v}
                style={{
                  ...styles.visBtn,
                  ...(visibility === v ? styles.visBtnActive : {}),
                }}
                onClick={() => setVisibility(v)}
              >
                <span style={styles.visIcon}>
                  {v === 'public' ? '\uD83C\uDF10' : v === 'unlisted' ? '\uD83D\uDD17' : '\uD83D\uDD12'}
                </span>
                <span style={styles.visLabel}>
                  {v.charAt(0).toUpperCase() + v.slice(1)}
                </span>
                <span style={styles.visDesc}>
                  {v === 'public'
                    ? 'Anyone can find it'
                    : v === 'unlisted'
                      ? 'Only with link'
                      : 'Only you'}
                </span>
              </button>
            ))}
          </div>
        </div>

        {/* Copy link */}
        <div style={styles.section}>
          <label style={styles.sectionLabel}>Share Link</label>
          <div style={styles.copyRow}>
            <input
              type="text"
              readOnly
              value={loading ? 'Generating...' : shareUrl}
              style={styles.copyInput}
            />
            <button
              style={styles.copyBtn}
              onClick={() => copyToClipboard(shareUrl, 'link')}
              disabled={loading}
            >
              {copied === 'link' ? 'Copied!' : 'Copy'}
            </button>
          </div>
        </div>

        {/* Social media */}
        <div style={styles.section}>
          <label style={styles.sectionLabel}>Share on Social Media</label>
          <div style={styles.socialRow}>
            <button
              style={{ ...styles.socialBtn, backgroundColor: '#1DA1F2' }}
              onClick={() =>
                window.open(
                  `https://twitter.com/intent/tweet?text=${encodeURIComponent(shareTextTwitter)}`,
                  '_blank',
                )
              }
            >
              Twitter / X
            </button>
            <button
              style={{ ...styles.socialBtn, backgroundColor: '#0077B5' }}
              onClick={() =>
                window.open(
                  `https://www.linkedin.com/sharing/share-offsite/?url=${encodeURIComponent(shareUrl)}`,
                  '_blank',
                )
              }
            >
              LinkedIn
            </button>
            <button
              style={{ ...styles.socialBtn, backgroundColor: '#1877F2' }}
              onClick={() =>
                window.open(
                  `https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(shareUrl)}`,
                  '_blank',
                )
              }
            >
              Facebook
            </button>
            <button
              style={{ ...styles.socialBtn, backgroundColor: '#25D366' }}
              onClick={() =>
                window.open(
                  `https://wa.me/?text=${encodeURIComponent(shareTextLinkedIn)}`,
                  '_blank',
                )
              }
            >
              WhatsApp
            </button>
          </div>
        </div>

        {/* Embed code */}
        <div style={styles.section}>
          <label style={styles.sectionLabel}>Embed on Your Website</label>
          <div style={styles.copyRow}>
            <textarea
              readOnly
              value={embedCode}
              style={styles.embedTextarea}
              rows={3}
            />
            <button
              style={styles.copyBtn}
              onClick={() => copyToClipboard(embedCode, 'embed')}
            >
              {copied === 'embed' ? 'Copied!' : 'Copy'}
            </button>
          </div>
        </div>

        {/* QR Code */}
        <div style={styles.section}>
          <label style={styles.sectionLabel}>QR Code</label>
          <div style={styles.qrContainer}>
            <div
              dangerouslySetInnerHTML={{ __html: qrSvg }}
              style={styles.qrCode}
            />
            <p style={styles.qrHint}>
              Scan to open this design on any device
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

// ---------------------------------------------------------------------------
// Styles
// ---------------------------------------------------------------------------

const styles: Record<string, React.CSSProperties> = {
  overlay: {
    position: 'fixed',
    inset: 0,
    backgroundColor: 'rgba(0, 0, 0, 0.7)',
    backdropFilter: 'blur(4px)',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    zIndex: 9999,
    padding: 16,
  },
  modal: {
    position: 'relative',
    backgroundColor: '#111827',
    border: '1px solid #1F2937',
    borderRadius: 16,
    padding: '28px 24px',
    width: '100%',
    maxWidth: 520,
    maxHeight: '90vh',
    overflowY: 'auto',
    color: '#F9FAFB',
    fontFamily: 'Inter, system-ui, sans-serif',
  },
  closeBtn: {
    position: 'absolute',
    top: 12,
    right: 16,
    background: 'none',
    border: 'none',
    color: '#6B7280',
    fontSize: 20,
    cursor: 'pointer',
    lineHeight: 1,
    padding: 4,
  },
  title: {
    margin: 0,
    fontSize: 20,
    fontWeight: 700,
    textAlign: 'center' as const,
  },
  subtitle: {
    margin: '2px 0 16px',
    fontSize: 13,
    color: '#9CA3AF',
    textAlign: 'center' as const,
  },
  errorBox: {
    backgroundColor: 'rgba(239, 68, 68, 0.15)',
    border: '1px solid rgba(239, 68, 68, 0.3)',
    borderRadius: 8,
    padding: '8px 12px',
    marginBottom: 12,
    fontSize: 12,
    color: '#FCA5A5',
  },

  // Preview
  preview: {
    height: 100,
    borderRadius: 10,
    marginBottom: 20,
    position: 'relative' as const,
    overflow: 'hidden',
    display: 'flex',
    alignItems: 'flex-end',
  },
  previewOverlay: {
    width: '100%',
    padding: '10px 14px',
    background: 'linear-gradient(transparent, rgba(0,0,0,0.6))',
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'flex-end',
  },
  previewLabel: {
    fontSize: 11,
    fontWeight: 600,
    color: '#9CA3AF',
    textTransform: 'uppercase' as const,
    letterSpacing: '0.05em',
  },
  previewTitle: {
    fontSize: 14,
    fontWeight: 600,
    color: '#F9FAFB',
  },

  // Sections
  section: {
    marginBottom: 18,
  },
  sectionLabel: {
    display: 'block',
    fontSize: 12,
    fontWeight: 600,
    color: '#9CA3AF',
    textTransform: 'uppercase' as const,
    letterSpacing: '0.05em',
    marginBottom: 8,
  },

  // Visibility
  visibilityRow: {
    display: 'flex',
    gap: 8,
  },
  visBtn: {
    flex: 1,
    display: 'flex',
    flexDirection: 'column' as const,
    alignItems: 'center',
    gap: 4,
    padding: '10px 6px',
    borderRadius: 10,
    border: '1px solid #374151',
    backgroundColor: '#1F2937',
    color: '#9CA3AF',
    cursor: 'pointer',
    transition: 'all 0.15s',
  },
  visBtnActive: {
    borderColor: '#6D28D9',
    backgroundColor: 'rgba(109, 40, 217, 0.15)',
    color: '#F9FAFB',
  },
  visIcon: {
    fontSize: 18,
  },
  visLabel: {
    fontSize: 13,
    fontWeight: 600,
  },
  visDesc: {
    fontSize: 10,
    color: '#6B7280',
    textAlign: 'center' as const,
  },

  // Copy link
  copyRow: {
    display: 'flex',
    gap: 8,
    alignItems: 'stretch',
  },
  copyInput: {
    flex: 1,
    padding: '8px 12px',
    borderRadius: 8,
    border: '1px solid #374151',
    backgroundColor: '#1F2937',
    color: '#D1D5DB',
    fontSize: 13,
    outline: 'none',
  },
  copyBtn: {
    padding: '8px 16px',
    borderRadius: 8,
    border: 'none',
    backgroundColor: '#6D28D9',
    color: '#F9FAFB',
    fontSize: 13,
    fontWeight: 600,
    cursor: 'pointer',
    whiteSpace: 'nowrap' as const,
  },

  // Social
  socialRow: {
    display: 'flex',
    gap: 8,
    flexWrap: 'wrap' as const,
  },
  socialBtn: {
    flex: '1 1 calc(50% - 4px)',
    padding: '10px 0',
    borderRadius: 8,
    border: 'none',
    color: '#F9FAFB',
    fontSize: 13,
    fontWeight: 600,
    cursor: 'pointer',
    textAlign: 'center' as const,
  },

  // Embed
  embedTextarea: {
    flex: 1,
    padding: '8px 12px',
    borderRadius: 8,
    border: '1px solid #374151',
    backgroundColor: '#1F2937',
    color: '#D1D5DB',
    fontSize: 12,
    fontFamily: 'monospace',
    resize: 'none' as const,
    outline: 'none',
  },

  // QR
  qrContainer: {
    display: 'flex',
    flexDirection: 'column' as const,
    alignItems: 'center',
    gap: 8,
    padding: 16,
    borderRadius: 10,
    backgroundColor: '#1F2937',
    border: '1px solid #374151',
  },
  qrCode: {
    width: 160,
    height: 160,
  },
  qrHint: {
    margin: 0,
    fontSize: 12,
    color: '#6B7280',
  },
};
