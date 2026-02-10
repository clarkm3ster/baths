import { useState, useEffect } from "react";
import type { Gap, Bridge } from "../../types";
import { getGap } from "../../api/client";
import { DomainBadge } from "../badges/DomainBadge";
import { SeverityBadge } from "../badges/SeverityBadge";
import { BarrierBadge } from "../badges/BarrierBadge";
import { BridgeCard } from "../bridges/BridgeCard";

interface GapDetailProps {
  gapId: number;
  onClose: () => void;
}

export function GapDetail({ gapId, onClose }: GapDetailProps) {
  const [gap, setGap] = useState<Gap | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    getGap(gapId)
      .then(setGap)
      .catch(console.error)
      .finally(() => setLoading(false));
  }, [gapId]);

  if (loading) {
    return (
      <div className="panel">
        <div className="panel-header flex items-center justify-between">
          <span>Loading...</span>
          <button className="btn btn-sm" onClick={onClose}>CLOSE</button>
        </div>
      </div>
    );
  }

  if (!gap) return null;

  return (
    <div className="panel">
      <div className="panel-header flex items-center justify-between">
        <div className="flex items-center gap-2">
          <span className="text-sm">Gap #{gap.id}</span>
          <SeverityBadge severity={gap.severity} />
          <BarrierBadge barrier={gap.barrier_type} />
        </div>
        <button className="btn btn-sm" onClick={onClose}>CLOSE</button>
      </div>
      <div className="panel-body space-y-4">
        {/* Systems involved */}
        <div className="flex items-center gap-3 text-sm">
          <span className="font-mono font-bold">
            {gap.system_a_name || gap.system_a_id}
          </span>
          <span className="font-mono text-gray-400 text-xs">---X---</span>
          <span className="font-mono font-bold">
            {gap.system_b_name || gap.system_b_id}
          </span>
        </div>

        {/* Info grid */}
        <div className="grid grid-cols-2 gap-x-4 gap-y-2 text-xs">
          <div>
            <span className="font-mono text-[0.5625rem] uppercase text-gray-500">
              Barrier Type
            </span>
            <p className="font-medium">{gap.barrier_type}</p>
          </div>
          <div>
            <span className="font-mono text-[0.5625rem] uppercase text-gray-500">
              Severity
            </span>
            <p className="font-medium">{gap.severity}</p>
          </div>
          <div>
            <span className="font-mono text-[0.5625rem] uppercase text-gray-500">
              Cost to Bridge
            </span>
            <p className="font-mono">{gap.cost_to_bridge}</p>
          </div>
          <div>
            <span className="font-mono text-[0.5625rem] uppercase text-gray-500">
              Timeline
            </span>
            <p className="font-mono">{gap.timeline_to_bridge}</p>
          </div>
          {gap.barrier_law && (
            <div className="col-span-2">
              <span className="font-mono text-[0.5625rem] uppercase text-gray-500">
                Barrier Law
              </span>
              <p className="font-mono">{gap.barrier_law}</p>
            </div>
          )}
          <div className="col-span-2">
            <span className="font-mono text-[0.5625rem] uppercase text-gray-500">
              Barrier Description
            </span>
            <p>{gap.barrier_description}</p>
          </div>
          <div className="col-span-2">
            <span className="font-mono text-[0.5625rem] uppercase text-gray-500">
              Impact
            </span>
            <p>{gap.impact}</p>
          </div>
          <div className="col-span-2">
            <span className="font-mono text-[0.5625rem] uppercase text-gray-500">
              What It Would Take
            </span>
            <p>{gap.what_it_would_take}</p>
          </div>
        </div>

        {/* Consent info */}
        {gap.consent_closable && (
          <div className="border-2 border-green-600 p-3 bg-green-50">
            <div className="flex items-center gap-2 mb-1">
              <span className="font-mono text-[0.625rem] font-bold uppercase text-green-700">
                Consent-Closable
              </span>
            </div>
            {gap.consent_mechanism && (
              <p className="text-xs text-green-800">{gap.consent_mechanism}</p>
            )}
          </div>
        )}

        {/* Applies When */}
        {gap.applies_when && gap.applies_when.length > 0 && (
          <div>
            <h4 className="section-header">Applies When</h4>
            <div className="flex flex-wrap gap-1">
              {gap.applies_when.map((condition) => (
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

        {/* Bridge Solutions */}
        {gap.bridges && gap.bridges.length > 0 && (
          <div>
            <h4 className="section-header">
              Bridge Solutions ({gap.bridges.length})
            </h4>
            <div className="space-y-2">
              {gap.bridges.map((bridge) => (
                <BridgeCard key={bridge.id} bridge={bridge} compact />
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
