/**
 * SPHERES Studio — Entry Point
 *
 * Bootstraps the React app with BrowserRouter and renders into #root.
 * Global providers (auth, store) wrap the App component.
 */

import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import App from './App';
import './index.css';

// ---------------------------------------------------------------------------
// Auth context placeholder — extend with real auth (Clerk, Auth0, etc.)
// ---------------------------------------------------------------------------

import { createContext, useContext, useState, type ReactNode } from 'react';

interface AuthUser {
  id: string;
  name: string;
  email: string;
  avatarUrl: string | null;
  plan: 'free' | 'creator' | 'production' | 'studio';
}

interface AuthContextValue {
  user: AuthUser | null;
  isAuthenticated: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  loading: boolean;
}

const AuthContext = createContext<AuthContextValue>({
  user: null,
  isAuthenticated: false,
  login: async () => {},
  logout: () => {},
  loading: false,
});

export function useAuth() {
  return useContext(AuthContext);
}

function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<AuthUser | null>(null);
  const [loading, setLoading] = useState(false);

  const login = async (_email: string, _password: string) => {
    setLoading(true);
    // Simulated login — replace with real auth provider
    await new Promise((r) => setTimeout(r, 500));
    setUser({
      id: 'user_001',
      name: 'Designer',
      email: _email,
      avatarUrl: null,
      plan: 'free',
    });
    setLoading(false);
  };

  const logout = () => {
    setUser(null);
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        isAuthenticated: user !== null,
        login,
        logout,
        loading,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

// ---------------------------------------------------------------------------
// Store provider — Zustand stores are already module-level singletons,
// but we wrap here for future SSR / testing isolation if needed.
// ---------------------------------------------------------------------------

function StoreProvider({ children }: { children: ReactNode }) {
  return <>{children}</>;
}

// ---------------------------------------------------------------------------
// Render
// ---------------------------------------------------------------------------

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <BrowserRouter>
      <AuthProvider>
        <StoreProvider>
          <App />
        </StoreProvider>
      </AuthProvider>
    </BrowserRouter>
  </StrictMode>
);
