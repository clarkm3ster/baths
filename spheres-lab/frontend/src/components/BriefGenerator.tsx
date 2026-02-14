import { useState, useEffect, useRef } from 'react';
import { Copy, Check, FileText } from 'lucide-react';
import {
  DOMAINS,
  READINESS_LEVELS,
  getAllInnovations,
  generateBrief,
  type Innovation,
  type DomainConfig,
  type ReadinessLevel,
  type Audience,
} from '../api/client';

const AUDIENCES: Audience[] = ['Mayor', 'Developer', 'Investor', 'Community Group'];

export default function BriefGenerator() {
  const [innovations, setInnovations] = useState<Innovation[]>([]);
  const [loading, setLoading] = useState(true);

  const [selectedDomain, setSelectedDomain] = useState<DomainConfig>(DOMAINS[0]);
  const [selectedReadiness, setSelectedReadiness] = useState<ReadinessLevel>('immediate');
  const [selectedAudience, setSelectedAudience] = useState<Audience>('Mayor');

  const [briefOutput, setBriefOutput] = useState<string>('');
  const [copied, setCopied] = useState(false);
  const preRef = useRef<HTMLPreElement>(null);

  useEffect(() => {
    let cancelled = false;
    async function load() {
      setLoading(true);
      const data = await getAllInnovations();
      if (!cancelled) {
        setInnovations(data);
        setLoading(false);
      }
    }
    load();
    return () => {
      cancelled = true;
    };
  }, []);

  function handleGenerate() {
    const brief = generateBrief(
      selectedDomain,
      selectedReadiness,
      selectedAudience,
      innovations
    );
    setBriefOutput(brief);
    setCopied(false);
  }

  async function handleCopy() {
    if (!briefOutput) return;
    try {
      await navigator.clipboard.writeText(briefOutput);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch {
      // Fallback: select the pre element
      if (preRef.current) {
        const range = document.createRange();
        range.selectNodeContents(preRef.current);
        const selection = window.getSelection();
        if (selection) {
          selection.removeAllRanges();
          selection.addRange(range);
        }
      }
    }
  }

  return (
    <div
      style={{
        padding: 24,
        height: '100%',
        display: 'flex',
        flexDirection: 'column',
      }}
    >
      {/* Header */}
      <div style={{ marginBottom: 20, flexShrink: 0 }}>
        <h1
          style={{
            fontSize: 20,
            fontWeight: 700,
            color: '#FFFFFF',
            margin: 0,
            marginBottom: 6,
          }}
        >
          Brief Generator
        </h1>
        <p
          style={{
            fontSize: 13,
            color: 'rgba(255,255,255,0.5)',
            margin: 0,
          }}
        >
          Generate formatted policy briefs by domain, readiness level, and
          target audience.
        </p>
      </div>

      {/* Controls */}
      <div
        style={{
          background: '#0A0A0A',
          border: '1px solid #1A1A1A',
          borderRadius: 12,
          padding: 20,
          marginBottom: 16,
          flexShrink: 0,
        }}
      >
        <div
          style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
            gap: 16,
            marginBottom: 16,
          }}
        >
          {/* Domain Selector */}
          <div>
            <label
              style={{
                display: 'block',
                fontSize: 10,
                fontWeight: 600,
                color: 'rgba(255,255,255,0.4)',
                letterSpacing: '0.06em',
                textTransform: 'uppercase' as const,
                marginBottom: 6,
              }}
            >
              DOMAIN
            </label>
            <select
              value={selectedDomain.slug}
              onChange={(e) => {
                const d = DOMAINS.find((d) => d.slug === e.target.value);
                if (d) setSelectedDomain(d);
              }}
              style={{
                width: '100%',
                background: '#111111',
                border: '1px solid #1A1A1A',
                borderRadius: 8,
                padding: '10px 12px',
                color: '#FFFFFF',
                fontSize: 13,
                fontFamily: "'Inter', sans-serif",
                outline: 'none',
                cursor: 'pointer',
                appearance: 'none' as const,
                WebkitAppearance: 'none' as const,
                backgroundImage:
                  'url("data:image/svg+xml,%3Csvg xmlns=\'http://www.w3.org/2000/svg\' width=\'12\' height=\'12\' viewBox=\'0 0 24 24\' fill=\'none\' stroke=\'rgba(255,255,255,0.3)\' stroke-width=\'2\'%3E%3Cpath d=\'M6 9l6 6 6-6\'/%3E%3C/svg%3E")',
                backgroundRepeat: 'no-repeat',
                backgroundPosition: 'right 12px center',
              }}
            >
              {DOMAINS.map((d) => (
                <option key={d.slug} value={d.slug}>
                  {d.icon} {d.label}
                </option>
              ))}
            </select>
          </div>

          {/* Readiness Selector */}
          <div>
            <label
              style={{
                display: 'block',
                fontSize: 10,
                fontWeight: 600,
                color: 'rgba(255,255,255,0.4)',
                letterSpacing: '0.06em',
                textTransform: 'uppercase' as const,
                marginBottom: 6,
              }}
            >
              READINESS LEVEL
            </label>
            <select
              value={selectedReadiness}
              onChange={(e) =>
                setSelectedReadiness(e.target.value as ReadinessLevel)
              }
              style={{
                width: '100%',
                background: '#111111',
                border: '1px solid #1A1A1A',
                borderRadius: 8,
                padding: '10px 12px',
                color: '#FFFFFF',
                fontSize: 13,
                fontFamily: "'Inter', sans-serif",
                outline: 'none',
                cursor: 'pointer',
                appearance: 'none' as const,
                WebkitAppearance: 'none' as const,
                backgroundImage:
                  'url("data:image/svg+xml,%3Csvg xmlns=\'http://www.w3.org/2000/svg\' width=\'12\' height=\'12\' viewBox=\'0 0 24 24\' fill=\'none\' stroke=\'rgba(255,255,255,0.3)\' stroke-width=\'2\'%3E%3Cpath d=\'M6 9l6 6 6-6\'/%3E%3C/svg%3E")',
                backgroundRepeat: 'no-repeat',
                backgroundPosition: 'right 12px center',
              }}
            >
              {READINESS_LEVELS.map((r) => (
                <option key={r.key} value={r.key}>
                  {r.label} — {r.description}
                </option>
              ))}
            </select>
          </div>

          {/* Audience Selector */}
          <div>
            <label
              style={{
                display: 'block',
                fontSize: 10,
                fontWeight: 600,
                color: 'rgba(255,255,255,0.4)',
                letterSpacing: '0.06em',
                textTransform: 'uppercase' as const,
                marginBottom: 6,
              }}
            >
              AUDIENCE
            </label>
            <select
              value={selectedAudience}
              onChange={(e) =>
                setSelectedAudience(e.target.value as Audience)
              }
              style={{
                width: '100%',
                background: '#111111',
                border: '1px solid #1A1A1A',
                borderRadius: 8,
                padding: '10px 12px',
                color: '#FFFFFF',
                fontSize: 13,
                fontFamily: "'Inter', sans-serif",
                outline: 'none',
                cursor: 'pointer',
                appearance: 'none' as const,
                WebkitAppearance: 'none' as const,
                backgroundImage:
                  'url("data:image/svg+xml,%3Csvg xmlns=\'http://www.w3.org/2000/svg\' width=\'12\' height=\'12\' viewBox=\'0 0 24 24\' fill=\'none\' stroke=\'rgba(255,255,255,0.3)\' stroke-width=\'2\'%3E%3Cpath d=\'M6 9l6 6 6-6\'/%3E%3C/svg%3E")',
                backgroundRepeat: 'no-repeat',
                backgroundPosition: 'right 12px center',
              }}
            >
              {AUDIENCES.map((a) => (
                <option key={a} value={a}>
                  {a}
                </option>
              ))}
            </select>
          </div>
        </div>

        {/* Generate Button */}
        <div style={{ display: 'flex', gap: 10, alignItems: 'center' }}>
          <button
            onClick={handleGenerate}
            disabled={loading}
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: 8,
              background: loading ? '#333333' : '#0066FF',
              border: 'none',
              borderRadius: 8,
              padding: '10px 20px',
              color: '#FFFFFF',
              fontSize: 13,
              fontWeight: 600,
              cursor: loading ? 'not-allowed' : 'pointer',
              transition: 'background 0.15s',
            }}
            onMouseEnter={(e) => {
              if (!loading) e.currentTarget.style.background = '#0055DD';
            }}
            onMouseLeave={(e) => {
              if (!loading) e.currentTarget.style.background = '#0066FF';
            }}
          >
            <FileText size={16} />
            {loading ? 'Loading data...' : 'Generate Brief'}
          </button>

          {/* Domain indicator */}
          <div
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: 6,
            }}
          >
            <div
              style={{
                width: 8,
                height: 8,
                borderRadius: 2,
                background: selectedDomain.color,
              }}
            />
            <span
              style={{
                fontSize: 11,
                color: 'rgba(255,255,255,0.4)',
                fontFamily: "'JetBrains Mono', monospace",
              }}
            >
              {selectedDomain.icon} {selectedDomain.label}
            </span>
          </div>
        </div>
      </div>

      {/* Output */}
      <div
        style={{
          flex: 1,
          background: '#0A0A0A',
          border: '1px solid #1A1A1A',
          borderRadius: 12,
          display: 'flex',
          flexDirection: 'column',
          overflow: 'hidden',
          minHeight: 200,
        }}
      >
        {/* Output Header */}
        <div
          style={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            padding: '10px 16px',
            borderBottom: '1px solid #1A1A1A',
            flexShrink: 0,
          }}
        >
          <span
            style={{
              fontSize: 11,
              fontWeight: 600,
              color: 'rgba(255,255,255,0.4)',
              letterSpacing: '0.06em',
              fontFamily: "'JetBrains Mono', monospace",
            }}
          >
            OUTPUT
          </span>
          {briefOutput && (
            <button
              onClick={handleCopy}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: 6,
                background: 'none',
                border: '1px solid #1A1A1A',
                borderRadius: 6,
                padding: '4px 12px',
                cursor: 'pointer',
                color: copied ? '#00CC66' : 'rgba(255,255,255,0.5)',
                fontSize: 11,
                fontFamily: "'JetBrains Mono', monospace",
                transition: 'color 0.15s, border-color 0.15s',
              }}
              onMouseEnter={(e) => {
                if (!copied) {
                  e.currentTarget.style.borderColor = '#2A2A2A';
                  e.currentTarget.style.color = '#FFFFFF';
                }
              }}
              onMouseLeave={(e) => {
                if (!copied) {
                  e.currentTarget.style.borderColor = '#1A1A1A';
                  e.currentTarget.style.color = 'rgba(255,255,255,0.5)';
                }
              }}
            >
              {copied ? (
                <>
                  <Check size={12} />
                  Copied
                </>
              ) : (
                <>
                  <Copy size={12} />
                  Copy
                </>
              )}
            </button>
          )}
        </div>

        {/* Output Content */}
        <div
          style={{
            flex: 1,
            overflow: 'auto',
            padding: 16,
          }}
        >
          {briefOutput ? (
            <pre
              ref={preRef}
              style={{
                fontFamily: "'JetBrains Mono', monospace",
                fontSize: 12,
                lineHeight: 1.6,
                color: 'rgba(255,255,255,0.7)',
                margin: 0,
                whiteSpace: 'pre-wrap',
                wordBreak: 'break-word',
              }}
            >
              {briefOutput}
            </pre>
          ) : (
            <div
              style={{
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                justifyContent: 'center',
                height: '100%',
                minHeight: 160,
                gap: 12,
              }}
            >
              <FileText
                size={32}
                style={{ color: 'rgba(255,255,255,0.1)' }}
              />
              <span
                style={{
                  fontSize: 13,
                  color: 'rgba(255,255,255,0.25)',
                }}
              >
                Select parameters and click Generate Brief
              </span>
              <span
                style={{
                  fontSize: 11,
                  color: 'rgba(255,255,255,0.15)',
                  fontFamily: "'JetBrains Mono', monospace",
                }}
              >
                Output will appear here in ASCII format
              </span>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
