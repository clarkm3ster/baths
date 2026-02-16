import { Routes, Route, Link, useLocation } from "react-router-dom";
import LandingPage from "./pages/LandingPage";
import PermitNavigatorPage from "./pages/PermitNavigatorPage";
import ContractGeneratorPage from "./pages/ContractGeneratorPage";
import PolicyLibraryPage from "./pages/PolicyLibraryPage";
import ComparativePage from "./pages/ComparativePage";
import EquityDashboardPage from "./pages/EquityDashboardPage";
import CostCalculatorPage from "./pages/CostCalculatorPage";

const NAV = [
  { to: "/permits", label: "Permits" },
  { to: "/contracts", label: "Contracts" },
  { to: "/policy", label: "Policy" },
  { to: "/comparative", label: "Comparative" },
  { to: "/equity", label: "Equity" },
  { to: "/cost", label: "Cost Calculator" },
];

function Nav() {
  const { pathname } = useLocation();
  if (pathname === "/") return null;

  return (
    <nav style={{ position: "fixed", top: 0, left: 0, right: 0, zIndex: 50, background: "rgba(10,10,10,0.9)", backdropFilter: "blur(8px)", WebkitBackdropFilter: "blur(8px)", borderBottom: "1px solid var(--color-ash)" }}>
      <div style={{ maxWidth: "1280px", margin: "0 auto", padding: "0 24px", display: "flex", alignItems: "center", justifyContent: "space-between", minHeight: "56px" }}>
        <Link
          to="/"
          className="font-mono"
          style={{ fontSize: "12px", fontWeight: 700, letterSpacing: "0.2em", color: "var(--color-legal-green)", textTransform: "uppercase", textDecoration: "none", flexShrink: 0 }}
        >
          SPHERES LEGAL
        </Link>
        <div style={{ display: "flex", alignItems: "center", gap: "4px", overflowX: "auto", WebkitOverflowScrolling: "touch", marginLeft: "16px" }}>
          {NAV.map((n) => (
            <Link
              key={n.to}
              to={n.to}
              className={`nav-link ${pathname === n.to ? "active" : ""}`}
              style={{ whiteSpace: "nowrap", minHeight: "44px", display: "inline-flex", alignItems: "center", padding: "8px 12px" }}
            >
              {n.label}
            </Link>
          ))}
        </div>
      </div>
    </nav>
  );
}

export default function App() {
  return (
    <>
      <Nav />
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/permits" element={<PermitNavigatorPage />} />
        <Route path="/contracts" element={<ContractGeneratorPage />} />
        <Route path="/policy" element={<PolicyLibraryPage />} />
        <Route path="/comparative" element={<ComparativePage />} />
        <Route path="/equity" element={<EquityDashboardPage />} />
        <Route path="/cost" element={<CostCalculatorPage />} />
      </Routes>
    </>
  );
}
