/**
 * SPHERES Studio — Auth Modal
 *
 * A login / register overlay with tab toggle, form validation, and error
 * display.  After successful auth it shows the user tier badge.
 */

import { useCallback, useEffect, useState, type FormEvent } from 'react';
import { useAuth, type UserProfile } from '../context/AuthContext';

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

interface AuthModalProps {
  isOpen: boolean;
  onClose: () => void;
  initialTab?: 'login' | 'register';
}

type Tab = 'login' | 'register';

// ---------------------------------------------------------------------------
// Tier badge colours
// ---------------------------------------------------------------------------

const TIER_COLORS: Record<string, { bg: string; text: string; label: string }> = {
  free: { bg: '#374151', text: '#D1D5DB', label: 'Free' },
  creator: { bg: '#7C3AED', text: '#EDE9FE', label: 'Creator' },
  production: { bg: '#2563EB', text: '#DBEAFE', label: 'Production' },
  studio: { bg: '#D97706', text: '#FEF3C7', label: 'Studio' },
};

// ---------------------------------------------------------------------------
// Component
// ---------------------------------------------------------------------------

export default function AuthModal({
  isOpen,
  onClose,
  initialTab = 'login',
}: AuthModalProps) {
  const { login, register, isLoading, error, clearError, isAuthenticated, user } =
    useAuth();

  const [tab, setTab] = useState<Tab>(initialTab);

  // Login fields
  const [loginEmail, setLoginEmail] = useState('');
  const [loginPassword, setLoginPassword] = useState('');

  // Register fields
  const [regName, setRegName] = useState('');
  const [regEmail, setRegEmail] = useState('');
  const [regPassword, setRegPassword] = useState('');
  const [regConfirm, setRegConfirm] = useState('');

  // Local validation error
  const [localError, setLocalError] = useState<string | null>(null);

  // Success screen after auth
  const [showSuccess, setShowSuccess] = useState(false);

  // Reset form when modal opens/closes or tab switches
  useEffect(() => {
    if (isOpen) {
      setTab(initialTab);
      setLoginEmail('');
      setLoginPassword('');
      setRegName('');
      setRegEmail('');
      setRegPassword('');
      setRegConfirm('');
      setLocalError(null);
      setShowSuccess(false);
      clearError();
    }
  }, [isOpen, initialTab, clearError]);

  useEffect(() => {
    setLocalError(null);
    clearError();
  }, [tab, clearError]);

  // Close on Escape
  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose();
    };
    if (isOpen) window.addEventListener('keydown', handler);
    return () => window.removeEventListener('keydown', handler);
  }, [isOpen, onClose]);

  // ----- Handlers -----

  const handleLogin = useCallback(
    async (e: FormEvent) => {
      e.preventDefault();
      setLocalError(null);
      if (!loginEmail.trim()) {
        setLocalError('Email is required');
        return;
      }
      if (!loginPassword) {
        setLocalError('Password is required');
        return;
      }
      try {
        await login(loginEmail, loginPassword);
        setShowSuccess(true);
      } catch {
        // error is set in context
      }
    },
    [login, loginEmail, loginPassword],
  );

  const handleRegister = useCallback(
    async (e: FormEvent) => {
      e.preventDefault();
      setLocalError(null);
      if (!regName.trim()) {
        setLocalError('Name is required');
        return;
      }
      if (!regEmail.trim()) {
        setLocalError('Email is required');
        return;
      }
      if (!regEmail.includes('@')) {
        setLocalError('Please enter a valid email address');
        return;
      }
      if (regPassword.length < 6) {
        setLocalError('Password must be at least 6 characters');
        return;
      }
      if (regPassword !== regConfirm) {
        setLocalError('Passwords do not match');
        return;
      }
      try {
        await register(regName, regEmail, regPassword);
        setShowSuccess(true);
      } catch {
        // error is set in context
      }
    },
    [register, regName, regEmail, regPassword, regConfirm],
  );

  if (!isOpen) return null;

  const displayError = localError || error;

  // ----- Success screen -----

  if (showSuccess && isAuthenticated && user) {
    const tier = TIER_COLORS[user.tier] || TIER_COLORS.free;
    return (
      <div
        style={styles.overlay}
        onClick={onClose}
      >
        <div style={styles.modal} onClick={(e) => e.stopPropagation()}>
          <button style={styles.closeBtn} onClick={onClose}>
            x
          </button>

          <div style={styles.successContainer}>
            <div style={styles.avatarCircle}>
              {user.avatar_url ? (
                <img
                  src={user.avatar_url}
                  alt={user.name}
                  style={styles.avatarImg}
                />
              ) : (
                <span style={styles.avatarInitial}>
                  {user.name.charAt(0).toUpperCase()}
                </span>
              )}
            </div>

            <h2 style={styles.successTitle}>Welcome, {user.name}</h2>

            <div
              style={{
                ...styles.tierBadge,
                backgroundColor: tier.bg,
                color: tier.text,
              }}
            >
              {tier.label} Tier
            </div>

            <p style={styles.successEmail}>{user.email}</p>
            <p style={styles.successMeta}>
              {user.designs_count} design{user.designs_count !== 1 ? 's' : ''} created
            </p>

            <button style={styles.primaryBtn} onClick={onClose}>
              Continue to Studio
            </button>
          </div>
        </div>
      </div>
    );
  }

  // ----- Auth form -----

  return (
    <div style={styles.overlay} onClick={onClose}>
      <div style={styles.modal} onClick={(e) => e.stopPropagation()}>
        <button style={styles.closeBtn} onClick={onClose}>
          x
        </button>

        <h2 style={styles.title}>SPHERES Studio</h2>
        <p style={styles.subtitle}>Design community spaces together</p>

        {/* Tab toggle */}
        <div style={styles.tabRow}>
          <button
            style={{
              ...styles.tab,
              ...(tab === 'login' ? styles.tabActive : {}),
            }}
            onClick={() => setTab('login')}
          >
            Log In
          </button>
          <button
            style={{
              ...styles.tab,
              ...(tab === 'register' ? styles.tabActive : {}),
            }}
            onClick={() => setTab('register')}
          >
            Register
          </button>
        </div>

        {/* Error display */}
        {displayError && <div style={styles.errorBox}>{displayError}</div>}

        {/* Login form */}
        {tab === 'login' && (
          <form onSubmit={handleLogin} style={styles.form}>
            <label style={styles.label}>
              Email
              <input
                type="email"
                value={loginEmail}
                onChange={(e) => setLoginEmail(e.target.value)}
                placeholder="you@example.com"
                style={styles.input}
                autoComplete="email"
                autoFocus
              />
            </label>

            <label style={styles.label}>
              Password
              <input
                type="password"
                value={loginPassword}
                onChange={(e) => setLoginPassword(e.target.value)}
                placeholder="Enter your password"
                style={styles.input}
                autoComplete="current-password"
              />
            </label>

            <button
              type="submit"
              style={{
                ...styles.primaryBtn,
                opacity: isLoading ? 0.6 : 1,
              }}
              disabled={isLoading}
            >
              {isLoading ? 'Signing in...' : 'Sign In'}
            </button>

            <p style={styles.hint}>
              Demo account: <strong>maya@spheres.city</strong> / <strong>demo1234</strong>
            </p>
          </form>
        )}

        {/* Register form */}
        {tab === 'register' && (
          <form onSubmit={handleRegister} style={styles.form}>
            <label style={styles.label}>
              Name
              <input
                type="text"
                value={regName}
                onChange={(e) => setRegName(e.target.value)}
                placeholder="Your display name"
                style={styles.input}
                autoComplete="name"
                autoFocus
              />
            </label>

            <label style={styles.label}>
              Email
              <input
                type="email"
                value={regEmail}
                onChange={(e) => setRegEmail(e.target.value)}
                placeholder="you@example.com"
                style={styles.input}
                autoComplete="email"
              />
            </label>

            <label style={styles.label}>
              Password
              <input
                type="password"
                value={regPassword}
                onChange={(e) => setRegPassword(e.target.value)}
                placeholder="At least 6 characters"
                style={styles.input}
                autoComplete="new-password"
              />
            </label>

            <label style={styles.label}>
              Confirm Password
              <input
                type="password"
                value={regConfirm}
                onChange={(e) => setRegConfirm(e.target.value)}
                placeholder="Re-enter your password"
                style={styles.input}
                autoComplete="new-password"
              />
            </label>

            <button
              type="submit"
              style={{
                ...styles.primaryBtn,
                opacity: isLoading ? 0.6 : 1,
              }}
              disabled={isLoading}
            >
              {isLoading ? 'Creating account...' : 'Create Account'}
            </button>
          </form>
        )}
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
    padding: '32px 28px',
    width: '100%',
    maxWidth: 420,
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
    fontSize: 22,
    fontWeight: 700,
    textAlign: 'center' as const,
    letterSpacing: '-0.02em',
  },
  subtitle: {
    margin: '4px 0 20px',
    fontSize: 13,
    color: '#9CA3AF',
    textAlign: 'center' as const,
  },
  tabRow: {
    display: 'flex',
    gap: 0,
    marginBottom: 20,
    borderRadius: 8,
    overflow: 'hidden',
    border: '1px solid #374151',
  },
  tab: {
    flex: 1,
    padding: '10px 0',
    background: 'transparent',
    border: 'none',
    color: '#9CA3AF',
    fontSize: 14,
    fontWeight: 500,
    cursor: 'pointer',
    transition: 'all 0.15s',
  },
  tabActive: {
    backgroundColor: '#6D28D9',
    color: '#F9FAFB',
  },
  errorBox: {
    backgroundColor: 'rgba(239, 68, 68, 0.15)',
    border: '1px solid rgba(239, 68, 68, 0.3)',
    borderRadius: 8,
    padding: '10px 14px',
    marginBottom: 16,
    fontSize: 13,
    color: '#FCA5A5',
  },
  form: {
    display: 'flex',
    flexDirection: 'column' as const,
    gap: 14,
  },
  label: {
    display: 'flex',
    flexDirection: 'column' as const,
    gap: 6,
    fontSize: 13,
    fontWeight: 500,
    color: '#D1D5DB',
  },
  input: {
    padding: '10px 12px',
    borderRadius: 8,
    border: '1px solid #374151',
    backgroundColor: '#1F2937',
    color: '#F9FAFB',
    fontSize: 14,
    outline: 'none',
    transition: 'border-color 0.15s',
  },
  primaryBtn: {
    marginTop: 4,
    padding: '12px 0',
    borderRadius: 8,
    border: 'none',
    backgroundColor: '#6D28D9',
    color: '#F9FAFB',
    fontSize: 15,
    fontWeight: 600,
    cursor: 'pointer',
    transition: 'background-color 0.15s',
  },
  hint: {
    margin: 0,
    fontSize: 12,
    color: '#6B7280',
    textAlign: 'center' as const,
  },
  successContainer: {
    display: 'flex',
    flexDirection: 'column' as const,
    alignItems: 'center',
    gap: 12,
    paddingTop: 8,
  },
  avatarCircle: {
    width: 64,
    height: 64,
    borderRadius: '50%',
    overflow: 'hidden',
    backgroundColor: '#6D28D9',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
  },
  avatarImg: {
    width: '100%',
    height: '100%',
    objectFit: 'cover' as const,
  },
  avatarInitial: {
    fontSize: 28,
    fontWeight: 700,
    color: '#F9FAFB',
  },
  successTitle: {
    margin: 0,
    fontSize: 20,
    fontWeight: 700,
  },
  tierBadge: {
    display: 'inline-block',
    padding: '4px 16px',
    borderRadius: 20,
    fontSize: 13,
    fontWeight: 600,
    letterSpacing: '0.02em',
  },
  successEmail: {
    margin: 0,
    fontSize: 14,
    color: '#9CA3AF',
  },
  successMeta: {
    margin: 0,
    fontSize: 13,
    color: '#6B7280',
  },
};
