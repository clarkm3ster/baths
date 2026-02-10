import { useState, useEffect } from "react";
import type { System, Connection, Gap } from "../../types";
import { getSystem } from "../../api/client";
import { DomainBadge } from "../badges/DomainBadge";
import { SeverityBadge } from "../badges/SeverityBadge";

interface SystemDetailProps {
  systemId: string;
  onClose: () => void;
}

export function SystemDetail({ systemId, onClose }: SystemDetailProps) {
  const [data, setData] = useState<
    (System & { connections: Connection[]; gaps: Gap[] }) | null
  >(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    getSystem(systemId)
      .then(setData)
      .catch(console.error)
      .finally(() => setLoading(false));
  }, [systemId]);

  if (loading) {
    return (
      <div className="panel">
        <div className="panel-header flex items-center justify-between">
          <span>Loading...</span>
          <button className="btn btn-sm" onClick={onClose}>
            CLOSE
          </button>
        </div>
        <div className="panel-body">
          <p className="font-mono text-xs text-gray-500">Loading system data...</p>
        </div>
      </div>
    );
  }

  if (!data) return null;

  return (
    <div className="panel">
      <div className="panel-header flex items-center justify-between">
        <div className="flex items-center gap-3">
          <span className="font-mono text-sm font-bold">{data.acronym}</span>
          <span className="text-base">{data.name}</span>
          <DomainBadge domain={data.domain} />
        </div>
        <button className="btn btn-sm" onClick={onClose}>
          CLOSE
        </button>
      </div>
      <div className="panel-body space-y-4">
        {/* Info Grid */}
        <div className="grid grid-cols-2 gap-x-6 gap-y-2 text-xs">
          <div>
            <span className="font-mono text-[0.625rem] uppercase text-gray-500">
              Agency
            </span>
            <p className="font-medium">{data.agency}</p>
          </div>
          <div>
            <span className="font-mono text-[0.625rem] uppercase text-gray-500">
              Data Standard
            </span>
            <p className="font-mono">{data.data_standard}</p>
          </div>
          <div>
            <span className="font-mono text-[0.625rem] uppercase text-gray-500">
              API Availability
            </span>
            <p className="font-mono">{data.api_availability}</p>
          </div>
          <div>
            <span className="font-mono text-[0.625rem] uppercase text-gray-500">
              Update Frequency
            </span>
            <p className="font-mono">{data.update_frequency}</p>
          </div>
          <div className="col-span-2">
            <span className="font-mono text-[0.625rem] uppercase text-gray-500">
              Description
            </span>
            <p>{data.description}</p>
          </div>
        </div>

        {/* Privacy Laws */}
        <div>
          <h4 className="section-header">Privacy Laws</h4>
          <div className="flex flex-wrap gap-1">
            {data.privacy_laws?.map((law) => (
              <span
                key={law}
                className="badge px-2 py-0.5 text-[0.625rem] border-gray-400 text-gray-700 bg-gray-50"
              >
                {law}
              </span>
            ))}
          </div>
        </div>

        {/* Fields Held */}
        <div>
          <h4 className="section-header">Fields Held ({data.fields_held?.length || 0})</h4>
          <div className="flex flex-wrap gap-1">
            {data.fields_held?.map((field) => (
              <span
                key={field}
                className="font-mono text-[0.625rem] px-1.5 py-0.5 border border-gray-300 bg-gray-50"
              >
                {field}
              </span>
            ))}
          </div>
        </div>

        {/* Applies When */}
        {data.applies_when && data.applies_when.length > 0 && (
          <div>
            <h4 className="section-header">Applies When</h4>
            <div className="flex flex-wrap gap-1">
              {data.applies_when.map((condition) => (
                <span
                  key={condition}
                  className="font-mono text-[0.625rem] px-1.5 py-0.5 border border-black bg-gray-100"
                >
                  {condition}
                </span>
              ))}
            </div>
          </div>
        )}

        {/* Connections */}
        <div>
          <h4 className="section-header">
            Connections ({data.connections?.length || 0})
          </h4>
          {data.connections && data.connections.length > 0 ? (
            <div className="space-y-1">
              {data.connections.map((conn) => (
                <div
                  key={conn.id}
                  className="flex items-center gap-2 text-xs border border-gray-200 p-2"
                >
                  <span className="font-mono font-bold text-[0.625rem]">
                    {conn.source_id === systemId
                      ? conn.target_name || conn.target_id
                      : conn.source_name || conn.source_id}
                  </span>
                  <span className="font-mono text-[0.5625rem] text-gray-500">
                    {conn.direction}
                  </span>
                  <span
                    className="font-mono text-[0.5625rem] px-1 border"
                    style={{
                      color:
                        conn.reliability === "high"
                          ? "#16A34A"
                          : conn.reliability === "moderate"
                          ? "#CA8A04"
                          : "#DC2626",
                      borderColor:
                        conn.reliability === "high"
                          ? "#16A34A"
                          : conn.reliability === "moderate"
                          ? "#CA8A04"
                          : "#DC2626",
                    }}
                  >
                    {conn.reliability}
                  </span>
                  <span className="font-mono text-[0.5625rem] text-gray-500">
                    {conn.format}
                  </span>
                  <span className="font-mono text-[0.5625rem] text-gray-500">
                    {conn.frequency}
                  </span>
                </div>
              ))}
            </div>
          ) : (
            <p className="font-mono text-xs text-gray-400">No connections</p>
          )}
        </div>

        {/* Gaps */}
        <div>
          <h4 className="section-header">Gaps ({data.gaps?.length || 0})</h4>
          {data.gaps && data.gaps.length > 0 ? (
            <div className="space-y-1">
              {data.gaps.map((gap) => (
                <div
                  key={gap.id}
                  className="flex items-center gap-2 text-xs border border-gray-200 p-2"
                >
                  <SeverityBadge severity={gap.severity} />
                  <span className="font-mono font-bold text-[0.625rem]">
                    {gap.system_a_id === systemId
                      ? gap.system_b_name || gap.system_b_id
                      : gap.system_a_name || gap.system_a_id}
                  </span>
                  <span className="font-mono text-[0.5625rem] text-gray-500">
                    {gap.barrier_type}
                  </span>
                  {gap.consent_closable && (
                    <span className="font-mono text-[0.5625rem] px-1 border border-green-600 text-green-700 bg-green-50">
                      CONSENT-CLOSABLE
                    </span>
                  )}
                  <span className="text-[0.6875rem] text-gray-600 truncate flex-1">
                    {gap.impact}
                  </span>
                </div>
              ))}
            </div>
          ) : (
            <p className="font-mono text-xs text-gray-400">No gaps</p>
          )}
        </div>
      </div>
    </div>
  );
}
