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
      <div className="flex items-center justify-between px-4 py-2">
        <div className="flex items-center gap-4">
          <div>
            <h1 className="font-serif text-lg font-bold tracking-wider uppercase leading-tight">
              DOMES DATAMAP
            </h1>
            <p className="font-mono text-[0.5625rem] uppercase tracking-[0.15em] text-gray-500 leading-tight">
              Government Data Flow Mapping Engine
            </p>
          </div>
        </div>
        <div className="flex items-center gap-0">
          {NAV_ITEMS.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              className={({ isActive }) =>
                `px-3 py-2 font-mono text-xs uppercase tracking-wider border border-black transition-colors ${
                  isActive
                    ? "bg-black text-white"
                    : "bg-white text-black hover:bg-gray-100"
                }`
              }
              style={{ marginLeft: "-1px" }}
            >
              {item.label}
            </NavLink>
          ))}
        </div>
      </div>
    </nav>
  );
}
