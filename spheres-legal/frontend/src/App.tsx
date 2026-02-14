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
    <nav className="fixed top-0 left-0 right-0 z-50 bg-void/90 backdrop-blur-sm border-b border-ash">
      <div className="max-w-7xl mx-auto px-6 flex items-center justify-between h-14">
        <Link
          to="/"
          className="font-mono text-xs font-bold tracking-[0.2em] text-legal-green uppercase"
        >
          SPHERES LEGAL
        </Link>
        <div className="flex items-center gap-6">
          {NAV.map((n) => (
            <Link
              key={n.to}
              to={n.to}
              className={`nav-link ${pathname === n.to ? "active" : ""}`}
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
