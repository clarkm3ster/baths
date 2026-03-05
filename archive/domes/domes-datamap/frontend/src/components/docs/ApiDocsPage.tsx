import { useState } from "react";

interface Endpoint {
  method: "GET" | "POST";
  path: string;
  description: string;
  parameters?: { name: string; type: string; description: string; required?: boolean }[];
  body?: string;
  exampleResponse: string;
  curl: string;
}

const ENDPOINTS: Endpoint[] = [
  {
    method: "GET",
    path: "/api/systems",
    description:
      "List all government data systems. Supports filtering by domain, data standard, and text search.",
    parameters: [
      {
        name: "domain",
        type: "string",
        description: "Filter by domain (Health, Justice, Housing, Income, Education, Child Welfare)",
      },
      {
        name: "data_standard",
        type: "string",
        description: "Filter by data standard (HL7 FHIR, NIEM, etc.)",
      },
      {
        name: "search",
        type: "string",
        description: "Text search across name, acronym, agency, description",
      },
    ],
    exampleResponse: `[
  {
    "id": "medicaid_mmis",
    "name": "Medicaid Management Information System",
    "acronym": "MMIS",
    "agency": "PA DHS",
    "domain": "Health",
    "description": "...",
    "data_standard": "HL7 FHIR",
    "fields_held": ["ssn", "demographics", "diagnosis_codes", ...],
    "api_availability": "partial",
    "update_frequency": "real-time",
    "privacy_law": "HIPAA",
    "privacy_laws": ["HIPAA", "42 CFR Part 2"],
    "is_federal": false,
    "state_operated": true,
    "applies_when": ["medicaid", "low_income"]
  }
]`,
    curl: `curl http://localhost:8003/api/systems?domain=Health`,
  },
  {
    method: "GET",
    path: "/api/systems/{system_id}",
    description:
      "Get detailed information about a specific system, including its connections and gaps.",
    parameters: [
      {
        name: "system_id",
        type: "string",
        description: "The system identifier",
        required: true,
      },
    ],
    exampleResponse: `{
  "id": "medicaid_mmis",
  "name": "Medicaid Management Information System",
  "acronym": "MMIS",
  ...
  "connections": [...],
  "gaps": [...]
}`,
    curl: `curl http://localhost:8003/api/systems/medicaid_mmis`,
  },
  {
    method: "GET",
    path: "/api/connections",
    description: "List all data connections between systems.",
    exampleResponse: `[
  {
    "id": 1,
    "source_id": "medicaid_mmis",
    "target_id": "ehr_system",
    "source_name": "Medicaid Management Information System",
    "target_name": "Electronic Health Records",
    "direction": "bidirectional",
    "format": "HL7 FHIR",
    "frequency": "real-time",
    "data_shared": ["demographics", "eligibility", "claims"],
    "governing_agreement": "PA DHS MOU",
    "privacy_law": "HIPAA",
    "reliability": "high",
    "description": "..."
  }
]`,
    curl: `curl http://localhost:8003/api/connections`,
  },
  {
    method: "GET",
    path: "/api/connections/matrix",
    description:
      "Get a connection matrix with all systems on both axes. Each cell contains the connection object or null.",
    exampleResponse: `{
  "systems": [...],
  "matrix": [[null, {...}, null, ...], ...]
}`,
    curl: `curl http://localhost:8003/api/connections/matrix`,
  },
  {
    method: "GET",
    path: "/api/gaps",
    description:
      "List all data gaps between systems. Supports filtering by barrier type, severity, consent closability, and domain.",
    parameters: [
      {
        name: "barrier_type",
        type: "string",
        description: "Filter by barrier type (legal, technical, political, consent, funding)",
      },
      {
        name: "severity",
        type: "string",
        description: "Filter by severity (critical, high, moderate, low)",
      },
      {
        name: "consent_closable",
        type: "boolean",
        description: "Filter for gaps that can be closed by individual consent",
      },
      {
        name: "domain",
        type: "string",
        description: "Filter by domain",
      },
    ],
    exampleResponse: `[
  {
    "id": 1,
    "system_a_id": "doc_offender",
    "system_b_id": "medicaid_mmis",
    "system_a_name": "Offender Management System",
    "system_b_name": "Medicaid Management Information System",
    "barrier_type": "legal",
    "barrier_law": "42 CFR Part 2",
    "barrier_description": "...",
    "impact": "...",
    "severity": "critical",
    "cost_to_bridge": "$2.5M",
    "timeline_to_bridge": "18 months",
    "consent_closable": true,
    "consent_mechanism": "...",
    "what_it_would_take": "...",
    "applies_when": ["incarcerated", "recently_released"]
  }
]`,
    curl: `curl http://localhost:8003/api/gaps?severity=critical&consent_closable=true`,
  },
  {
    method: "GET",
    path: "/api/gaps/{gap_id}",
    description: "Get detailed information about a specific gap, including bridge solutions.",
    parameters: [
      {
        name: "gap_id",
        type: "integer",
        description: "The gap identifier",
        required: true,
      },
    ],
    exampleResponse: `{
  "id": 1,
  ...
  "bridges": [
    {
      "id": 1,
      "gap_id": 1,
      "bridge_type": "consent",
      "title": "...",
      "description": "...",
      "priority_score": 9,
      "impact_score": 8,
      "effort_score": 3,
      "status": "proposed"
    }
  ]
}`,
    curl: `curl http://localhost:8003/api/gaps/1`,
  },
  {
    method: "POST",
    path: "/api/person-map",
    description:
      "Map government data systems relevant to a specific person based on their circumstances. Returns matching systems, connections, gaps, bridges, and a summary.",
    body: `{
  "circumstances": ["medicaid", "incarcerated", "substance_use"]
}`,
    exampleResponse: `{
  "systems": [...],
  "connections": [...],
  "gaps": [...],
  "bridges": [...],
  "summary": {
    "total_systems": 8,
    "connected_pairs": 5,
    "disconnected_pairs": 12,
    "gaps_count": 4,
    "consent_closable_count": 2,
    "total_bridge_cost": "$4.2M"
  }
}`,
    curl: `curl -X POST http://localhost:8003/api/person-map \\
  -H "Content-Type: application/json" \\
  -d '{"circumstances": ["medicaid", "incarcerated", "substance_use"]}'`,
  },
  {
    method: "GET",
    path: "/api/bridges",
    description: "List all bridge solutions. Supports filtering by type, status, and minimum priority.",
    parameters: [
      {
        name: "bridge_type",
        type: "string",
        description: "Filter by bridge type (technical, legal, policy, consent, funding, administrative)",
      },
      {
        name: "status",
        type: "string",
        description: "Filter by status (proposed, planned, in_progress, completed, blocked)",
      },
      {
        name: "min_priority",
        type: "number",
        description: "Minimum priority score (1-10)",
      },
    ],
    exampleResponse: `[
  {
    "id": 1,
    "gap_id": 1,
    "bridge_type": "consent",
    "title": "Unified Consent Portal",
    "description": "...",
    "technical_requirements": "...",
    "legal_requirements": "...",
    "estimated_cost": "$500K",
    "timeline": "6 months",
    "who_pays": "State DHS",
    "priority_score": 9,
    "impact_score": 8,
    "effort_score": 3,
    "status": "proposed"
  }
]`,
    curl: `curl http://localhost:8003/api/bridges?bridge_type=consent&min_priority=7`,
  },
  {
    method: "GET",
    path: "/api/bridges/{gap_id}",
    description: "Get all bridge solutions for a specific gap.",
    parameters: [
      {
        name: "gap_id",
        type: "integer",
        description: "The gap identifier",
        required: true,
      },
    ],
    exampleResponse: `[
  { "id": 1, "gap_id": 1, "bridge_type": "consent", ... },
  { "id": 2, "gap_id": 1, "bridge_type": "technical", ... }
]`,
    curl: `curl http://localhost:8003/api/bridges/1`,
  },
  {
    method: "GET",
    path: "/api/bridges/priority",
    description: "Get bridges sorted by priority score descending, with pagination.",
    parameters: [
      {
        name: "limit",
        type: "integer",
        description: "Number of results to return (default 20)",
      },
      {
        name: "offset",
        type: "integer",
        description: "Offset for pagination (default 0)",
      },
    ],
    exampleResponse: `[
  { "id": 5, "priority_score": 10, ... },
  { "id": 1, "priority_score": 9, ... },
  ...
]`,
    curl: `curl http://localhost:8003/api/bridges/priority?limit=10`,
  },
  {
    method: "POST",
    path: "/api/bridges/consent-pathway",
    description:
      "Given a person's circumstances, return only the consent-closable gaps and their consent bridge solutions.",
    body: `{
  "circumstances": ["medicaid", "recently_released"]
}`,
    exampleResponse: `{
  "consent_closable_gaps": [...],
  "consent_bridges": [...]
}`,
    curl: `curl -X POST http://localhost:8003/api/bridges/consent-pathway \\
  -H "Content-Type: application/json" \\
  -d '{"circumstances": ["medicaid", "recently_released"]}'`,
  },
  {
    method: "GET",
    path: "/api/stats",
    description: "Get aggregate statistics about the data mapping.",
    exampleResponse: `{
  "total_systems": 31,
  "total_connections": 24,
  "total_gaps": 18,
  "by_severity": {"critical": 5, "high": 7, "moderate": 4, "low": 2},
  "by_barrier_type": {"legal": 6, "technical": 5, "political": 3, "consent": 2, "funding": 2},
  "consent_closable_count": 8,
  "total_bridges": 36,
  "avg_priority": 6.5
}`,
    curl: `curl http://localhost:8003/api/stats`,
  },
];

export function ApiDocsPage() {
  const [expandedIdx, setExpandedIdx] = useState<number | null>(null);
  const [copiedIdx, setCopiedIdx] = useState<number | null>(null);

  function copyToClipboard(text: string, idx: number) {
    navigator.clipboard.writeText(text).then(() => {
      setCopiedIdx(idx);
      setTimeout(() => setCopiedIdx(null), 2000);
    });
  }

  return (
    <div className="flex flex-col h-[calc(100vh-3.5rem)]">
      {/* Header */}
      <div className="border-b border-black px-4 py-2 bg-gray-50">
        <h2 className="font-serif text-lg font-bold uppercase tracking-wide">
          API Documentation
        </h2>
        <p className="font-mono text-[0.625rem] text-gray-500 uppercase tracking-wider">
          DOMES DATAMAP REST API / Base URL: http://localhost:8003
        </p>
      </div>

      {/* Intro */}
      <div className="flex-1 overflow-auto">
        <div className="max-w-4xl mx-auto p-4 space-y-2">
          <div className="card bg-gray-50 mb-6">
            <h3 className="font-serif text-sm font-bold mb-1">
              About This API
            </h3>
            <p className="text-xs text-gray-700 mb-2">
              The DOMES DATAMAP API provides structured access to government data
              system mappings, inter-system connections, data sharing gaps, and
              bridge solutions. This API serves as the data connectivity source
              for other DOMES applications.
            </p>
            <div className="grid grid-cols-3 gap-2 text-xs">
              <div>
                <span className="font-mono text-[0.5625rem] uppercase text-gray-500">
                  Format
                </span>
                <p className="font-mono font-medium">JSON</p>
              </div>
              <div>
                <span className="font-mono text-[0.5625rem] uppercase text-gray-500">
                  Auth
                </span>
                <p className="font-mono font-medium">None (local)</p>
              </div>
              <div>
                <span className="font-mono text-[0.5625rem] uppercase text-gray-500">
                  CORS
                </span>
                <p className="font-mono font-medium">Enabled</p>
              </div>
            </div>
          </div>

          {/* Endpoints */}
          <div className="space-y-1">
            {ENDPOINTS.map((endpoint, idx) => {
              const isExpanded = expandedIdx === idx;
              return (
                <div key={idx} className="border border-black">
                  {/* Summary row */}
                  <div
                    className="flex items-center gap-3 px-3 py-2 cursor-pointer hover:bg-gray-50"
                    onClick={() =>
                      setExpandedIdx(isExpanded ? null : idx)
                    }
                  >
                    <span
                      className={`font-mono text-[0.625rem] font-bold px-2 py-0.5 border ${
                        endpoint.method === "POST"
                          ? "border-green-600 text-green-700 bg-green-50"
                          : "border-blue-600 text-blue-700 bg-blue-50"
                      }`}
                    >
                      {endpoint.method}
                    </span>
                    <span className="font-mono text-xs font-medium">
                      {endpoint.path}
                    </span>
                    <span className="text-xs text-gray-500 flex-1 truncate">
                      {endpoint.description}
                    </span>
                    <span className="font-mono text-xs">
                      {isExpanded ? "[-]" : "[+]"}
                    </span>
                  </div>

                  {/* Expanded details */}
                  {isExpanded && (
                    <div className="border-t border-black px-3 py-3 space-y-3 bg-gray-50">
                      <p className="text-xs">{endpoint.description}</p>

                      {/* Parameters */}
                      {endpoint.parameters &&
                        endpoint.parameters.length > 0 && (
                          <div>
                            <h5 className="section-header">Parameters</h5>
                            <table className="data-table">
                              <thead>
                                <tr>
                                  <th>Name</th>
                                  <th>Type</th>
                                  <th>Required</th>
                                  <th>Description</th>
                                </tr>
                              </thead>
                              <tbody>
                                {endpoint.parameters.map((param) => (
                                  <tr key={param.name}>
                                    <td className="font-mono text-xs font-bold">
                                      {param.name}
                                    </td>
                                    <td className="font-mono text-[0.6875rem] text-gray-600">
                                      {param.type}
                                    </td>
                                    <td className="text-[0.6875rem]">
                                      {param.required ? "Yes" : "No"}
                                    </td>
                                    <td className="text-[0.6875rem]">
                                      {param.description}
                                    </td>
                                  </tr>
                                ))}
                              </tbody>
                            </table>
                          </div>
                        )}

                      {/* Request Body */}
                      {endpoint.body && (
                        <div>
                          <h5 className="section-header">Request Body</h5>
                          <pre className="font-mono text-[0.6875rem] p-3 border border-black bg-white overflow-x-auto">
                            {endpoint.body}
                          </pre>
                        </div>
                      )}

                      {/* Example Response */}
                      <div>
                        <h5 className="section-header">Example Response</h5>
                        <pre className="font-mono text-[0.6875rem] p-3 border border-black bg-white overflow-x-auto max-h-60 overflow-y-auto">
                          {endpoint.exampleResponse}
                        </pre>
                      </div>

                      {/* CURL */}
                      <div>
                        <div className="flex items-center justify-between mb-1">
                          <h5 className="font-mono text-[0.5625rem] font-bold uppercase tracking-wider">
                            cURL
                          </h5>
                          <button
                            className="btn btn-sm text-[0.5625rem]"
                            onClick={(e) => {
                              e.stopPropagation();
                              copyToClipboard(endpoint.curl, idx);
                            }}
                          >
                            {copiedIdx === idx ? "COPIED" : "COPY"}
                          </button>
                        </div>
                        <pre className="font-mono text-[0.6875rem] p-3 border border-black bg-black text-green-400 overflow-x-auto">
                          {endpoint.curl}
                        </pre>
                      </div>
                    </div>
                  )}
                </div>
              );
            })}
          </div>

          {/* Footer note */}
          <div className="border-t-2 border-black pt-4 mt-6">
            <p className="font-mono text-[0.625rem] text-gray-500">
              This API is designed for integration with the DOMES ecosystem.
              Other DOMES apps (Legal, Profile, Data Constellation) can consume
              these endpoints to enrich their views with data connectivity
              information.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
