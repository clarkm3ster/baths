import { NavLink } from "react-router-dom";

const NAV_ITEMS = [
  { to: "/systems", label: "Systems" },
  { to: "/matrix", label: "Matrix" },
  { to: "/gaps", label: "Gaps" },
  { to: "/person", label: "Person" },
  { to: "/bridges", label: "Bridges" },
  { to: "/api-docs", label: "API Docs" },
];

export function TopNav() {
  return (
    <nav className="border-b-2 border-black bg-white sticky top-0 z-50">
      <div style={{ display: "flex", flexDirection: "column" }}>
        <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", padding: "8px 16px" }}>
          <div>
            <h1 className="font-serif text-lg font-bold tracking-wider uppercase leading-tight">
              DOMES DATAMAP
            </h1>
            <p className="font-mono text-[0.5625rem] uppercase tracking-[0.15em] text-gray-500 leading-tight">
              Government Data Flow Mapping Engine
            </p>
          </div>
        </div>
        <div style={{ display: "flex", overflowX: "auto", WebkitOverflowScrolling: "touch" }}>
          {NAV_ITEMS.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              className={({ isActive }) =>
                `font-mono text-xs uppercase tracking-wider border border-black transition-colors ${
                  isActive
                    ? "bg-black text-white"
                    : "bg-white text-black hover:bg-gray-100"
                }`
              }
              style={{ marginLeft: "-1px", padding: "10px 12px", whiteSpace: "nowrap", minHeight: "44px", display: "inline-flex", alignItems: "center" }}
            >
              {item.label}
            </NavLink>
          ))}
        </div>
      </div>
    </nav>
  );
}
