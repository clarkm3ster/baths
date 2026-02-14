import { useEffect, useRef, useCallback, type ReactNode } from 'react';
import { createPortal } from 'react-dom';

// ---------------------------------------------------------------------------
// WorldOverlay
// ---------------------------------------------------------------------------
// Full-screen overlay that hosts a 3D world. Rendered as a portal so it sits
// above every other layer. Locks body scroll while open and traps keyboard
// focus inside the overlay for accessibility.
// ---------------------------------------------------------------------------

interface WorldOverlayProps {
  children: ReactNode;
  onClose: () => void;
}

export default function WorldOverlay({ children, onClose }: WorldOverlayProps) {
  const overlayRef = useRef<HTMLDivElement>(null);
  const previousFocusRef = useRef<HTMLElement | null>(null);

  // --- Lock body scroll and manage focus -----------------------------------
  useEffect(() => {
    // Save the element that had focus before the overlay opened.
    previousFocusRef.current = document.activeElement as HTMLElement | null;

    // Prevent body scroll.
    const scrollY = window.scrollY;
    document.body.style.position = 'fixed';
    document.body.style.top = `-${scrollY}px`;
    document.body.style.left = '0';
    document.body.style.right = '0';
    document.body.style.overflow = 'hidden';

    // Move focus into the overlay.
    overlayRef.current?.focus();

    return () => {
      // Restore body scroll.
      document.body.style.position = '';
      document.body.style.top = '';
      document.body.style.left = '';
      document.body.style.right = '';
      document.body.style.overflow = '';
      window.scrollTo(0, scrollY);

      // Restore focus.
      previousFocusRef.current?.focus();
    };
  }, []);

  // --- Keyboard handling: Escape to close, Tab trap -----------------------
  const handleKeyDown = useCallback(
    (e: React.KeyboardEvent<HTMLDivElement>) => {
      if (e.key === 'Escape') {
        onClose();
        return;
      }

      // Focus trap — cycle Tab through focusable children.
      if (e.key === 'Tab') {
        const overlay = overlayRef.current;
        if (!overlay) return;

        const focusable = overlay.querySelectorAll<HTMLElement>(
          'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])',
        );
        if (focusable.length === 0) return;

        const first = focusable[0];
        const last = focusable[focusable.length - 1];

        if (e.shiftKey) {
          if (document.activeElement === first) {
            e.preventDefault();
            last.focus();
          }
        } else {
          if (document.activeElement === last) {
            e.preventDefault();
            first.focus();
          }
        }
      }
    },
    [onClose],
  );

  // --- Render via portal ---------------------------------------------------
  return createPortal(
    <div
      ref={overlayRef}
      role="dialog"
      aria-modal="true"
      aria-label="3D World Experience"
      tabIndex={-1}
      onKeyDown={handleKeyDown}
      className="animate-fade-in"
      style={{
        position: 'fixed',
        inset: 0,
        zIndex: 50,
        background: '#000000',
        outline: 'none',
      }}
    >
      {children}
    </div>,
    document.body,
  );
}
