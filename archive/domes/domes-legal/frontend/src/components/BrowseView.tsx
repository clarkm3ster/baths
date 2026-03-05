import { useState, useEffect } from "react";
import type { Provision } from "../types";
import { DOMAIN_COLORS } from "../types";
import { getHierarchy, getProvisions } from "../api/client";
import DomainBadge from "./DomainBadge";

interface Props {
  onSelect: (p: Provision) => void;
}

interface TreeNode {
  [key: string]: TreeNode | ProvisionEntry[];
}

interface ProvisionEntry {
  id: number;
  citation: string;
  title: string;
  domain: string;
  provision_type: string;
}

export default function BrowseView({ onSelect }: Props) {
  const [hierarchy, setHierarchy] = useState<Record<string, unknown>>({});
  const [selectedPath, setSelectedPath] = useState<string[]>([]);
  const [provisions, setProvisions] = useState<Provision[]>([]);

  useEffect(() => {
    getHierarchy().then(setHierarchy);
  }, []);

  useEffect(() => {
    if (selectedPath.length === 0) {
      getProvisions().then((r) => setProvisions(r.items));
    }
  }, [selectedPath]);

  function handleNodeClick(path: string[]) {
    setSelectedPath(path);
    // Navigate to the leaf provisions
    let node: unknown = hierarchy;
    for (const key of path) {
      node = (node as Record<string, unknown>)[key];
    }
    if (Array.isArray(node)) {
      // Leaf - load full provisions
      const ids = (node as ProvisionEntry[]).map((p) => p.id);
      getProvisions().then((r) => {
        setProvisions(r.items.filter((p) => ids.includes(p.id)));
      });
    }
  }

  const SOURCE_LABELS: Record<string, string> = {
    usc: "US Code",
    cfr: "Code of Federal Regulations",
    constitution: "Constitution",
    case_law: "Case Law",
    fr: "Federal Register",
    pa_statute: "PA Statutes",
    pa_reg: "PA Regulations",
  };

  function renderTree(node: unknown, path: string[], depth: number): JSX.Element[] {
    if (!node || typeof node !== "object" || Array.isArray(node)) return [];
    return Object.entries(node as Record<string, unknown>).map(([key, value]) => {
      const currentPath = [...path, key];
      const isArray = Array.isArray(value);
      const count = isArray ? (value as unknown[]).length : countLeaves(value);
      const isSelected = selectedPath.length >= currentPath.length &&
        currentPath.every((k, i) => selectedPath[i] === k);
      const label = depth === 0 ? (SOURCE_LABELS[key] || key) : `Title ${key}`;

      return (
        <div key={key}>
          <div
            onClick={() => handleNodeClick(currentPath)}
            style={{
              padding: "8px 12px",
              paddingLeft: `${12 + depth * 16}px`,
              cursor: "pointer",
              background: isSelected ? "var(--color-surface)" : "transparent",
              borderLeft: isSelected ? "3px solid var(--color-accent)" : "3px solid transparent",
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
              fontFamily: "var(--font-mono)",
              fontSize: "12px",
              transition: "background 0.1s",
            }}
          >
            <span>{label}</span>
            <span style={{ fontSize: "10px", color: "var(--color-text-tertiary)", padding: "1px 6px", background: "var(--color-surface-alt)" }}>
              {count}
            </span>
          </div>
          {isSelected && !isArray && renderTree(value, currentPath, depth + 1)}
        </div>
      );
    });
  }

  function countLeaves(node: unknown): number {
    if (Array.isArray(node)) return node.length;
    if (!node || typeof node !== "object") return 0;
    return Object.values(node as Record<string, unknown>).reduce((s: number, v) => s + countLeaves(v), 0);
  }

  return (
    <div style={{ display: "grid", gridTemplateColumns: "280px 1fr", height: "100%" }}>
      {/* Left: tree */}
      <div style={{ borderRight: "1px solid var(--color-border)", overflowY: "auto", paddingTop: "12px" }}>
        <div className="section-label" style={{ padding: "0 12px", marginBottom: "8px" }}>Hierarchy</div>
        {renderTree(hierarchy, [], 0)}
      </div>

      {/* Right: provisions */}
      <div style={{ overflowY: "auto", padding: "12px 0" }}>
        <div className="section-label" style={{ padding: "0 20px", marginBottom: "8px" }}>
          {provisions.length} Provisions
        </div>
        {provisions.map((p) => (
          <div key={p.id} className="provision-card" onClick={() => onSelect(p)} style={{ padding: "12px 20px" }}>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start" }}>
              <span style={{ fontFamily: "var(--font-mono)", fontSize: "11px", fontWeight: 500 }}>
                {p.citation}
              </span>
              <DomainBadge domain={p.domain} />
            </div>
            <div style={{ fontFamily: "var(--font-serif)", fontSize: "14px", fontWeight: 600, marginTop: "2px" }}>
              {p.title}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
