import { useState, useEffect, useMemo } from "react";
import type { System } from "../../types";
import { DOMAINS } from "../../types";
import { getSystems } from "../../api/client";
import { DomainBadge } from "../badges/DomainBadge";
import { SystemDetail } from "./SystemDetail";

export function SystemsPage() {
  const [systems, setSystems] = useState<System[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedSystem, setSelectedSystem] = useState<string | null>(null);

  // Filters
  const [domainFilter, setDomainFilter] = useState("");
  const [standardFilter, setStandardFilter] = useState("");
  const [searchFilter, setSearchFilter] = useState("");

  useEffect(() => {
    setLoading(true);
    getSystems()
      .then(setSystems)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, []);

  const dataStandards = useMemo(() => {
    const set = new Set(systems.map((s) => s.data_standard).filter(Boolean));
    return Array.from(set).sort();
  }, [systems]);

  const filtered = useMemo(() => {
    return systems.filter((s) => {
      if (domainFilter && s.domain !== domainFilter) return false;
      if (standardFilter && s.data_standard !== standardFilter) return false;
      if (searchFilter) {
        const q = searchFilter.toLowerCase();
        if (
          !s.name.toLowerCase().includes(q) &&
          !s.acronym.toLowerCase().includes(q) &&
          !s.agency.toLowerCase().includes(q) &&
          !s.description.toLowerCase().includes(q)
        )
          return false;
      }
      return true;
    });
  }, [systems, domainFilter, standardFilter, searchFilter]);

  return (
    <div className="flex flex-col h-[calc(100vh-3.5rem)]">
      {/* Header */}
      <div className="border-b border-black px-4 py-2 bg-gray-50">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="font-serif text-lg font-bold uppercase tracking-wide">
              Systems Registry
            </h2>
            <p className="font-mono text-[0.625rem] text-gray-500 uppercase tracking-wider">
              {filtered.length} of {systems.length} systems
            </p>
          </div>
        </div>
      </div>

      {/* Filter Bar */}
      <div className="filter-bar mx-0 border-x-0 border-t-0">
        <label className="font-mono text-[0.625rem] uppercase tracking-wider text-gray-500">
          Filter:
        </label>
        <select
          className="filter-select"
          value={domainFilter}
          onChange={(e) => setDomainFilter(e.target.value)}
        >
          <option value="">All Domains</option>
          {DOMAINS.map((d) => (
            <option key={d} value={d}>
              {d}
            </option>
          ))}
        </select>
        <select
          className="filter-select"
          value={standardFilter}
          onChange={(e) => setStandardFilter(e.target.value)}
        >
          <option value="">All Standards</option>
          {dataStandards.map((s) => (
            <option key={s} value={s}>
              {s}
            </option>
          ))}
        </select>
        <input
          type="text"
          className="filter-input"
          placeholder="Search systems..."
          value={searchFilter}
          onChange={(e) => setSearchFilter(e.target.value)}
        />
        {(domainFilter || standardFilter || searchFilter) && (
          <button
            className="btn btn-sm"
            onClick={() => {
              setDomainFilter("");
              setStandardFilter("");
              setSearchFilter("");
            }}
          >
            CLEAR
          </button>
        )}
      </div>

      {/* Content */}
      <div className="flex flex-1 overflow-hidden">
        {/* Table */}
        <div className="flex-1 overflow-auto">
          {loading ? (
            <div className="p-8 text-center font-mono text-sm text-gray-500">
              Loading systems...
            </div>
          ) : error ? (
            <div className="p-8 text-center font-mono text-sm text-red-600">
              Error: {error}
            </div>
          ) : (
            <table className="data-table">
              <thead>
                <tr>
                  <th>Acronym</th>
                  <th>Name</th>
                  <th>Agency</th>
                  <th>Domain</th>
                  <th>Standard</th>
                  <th>API</th>
                  <th>Frequency</th>
                  <th>Scope</th>
                </tr>
              </thead>
              <tbody>
                {filtered.map((system) => (
                  <tr
                    key={system.id}
                    className={`cursor-pointer ${
                      selectedSystem === system.id ? "bg-gray-100" : ""
                    }`}
                    onClick={() =>
                      setSelectedSystem(
                        selectedSystem === system.id ? null : system.id
                      )
                    }
                  >
                    <td className="font-mono font-bold text-xs">
                      {system.acronym}
                    </td>
                    <td className="text-xs font-medium">{system.name}</td>
                    <td className="text-xs text-gray-600">{system.agency}</td>
                    <td>
                      <DomainBadge domain={system.domain} />
                    </td>
                    <td className="font-mono text-[0.6875rem] text-gray-600">
                      {system.data_standard}
                    </td>
                    <td>
                      <span
                        className={`font-mono text-[0.625rem] px-1.5 py-0.5 border ${
                          system.api_availability === "full"
                            ? "border-green-600 text-green-700 bg-green-50"
                            : system.api_availability === "partial"
                            ? "border-yellow-600 text-yellow-700 bg-yellow-50"
                            : system.api_availability === "limited"
                            ? "border-orange-600 text-orange-700 bg-orange-50"
                            : "border-gray-400 text-gray-500 bg-gray-50"
                        }`}
                      >
                        {system.api_availability}
                      </span>
                    </td>
                    <td className="font-mono text-[0.6875rem] text-gray-600">
                      {system.update_frequency}
                    </td>
                    <td className="text-[0.625rem] text-gray-500">
                      {system.is_federal && (
                        <span className="font-mono px-1 border border-gray-400 mr-1">
                          FED
                        </span>
                      )}
                      {system.state_operated && (
                        <span className="font-mono px-1 border border-gray-400">
                          STATE
                        </span>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>

        {/* Detail Panel */}
        {selectedSystem && (
          <div className="w-[480px] border-l-2 border-black overflow-auto">
            <SystemDetail
              systemId={selectedSystem}
              onClose={() => setSelectedSystem(null)}
            />
          </div>
        )}
      </div>
    </div>
  );
}
