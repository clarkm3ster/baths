import { useState, useEffect, useRef } from 'react'
import './DomesGame.css'

const STAGES = [
  { key: 'development', label: 'RESEARCH', num: '01', desc: 'Map the legal landscape, costs, and systems', verb: 'Researching' },
  { key: 'pre_production', label: 'DESIGN', num: '02', desc: 'Architect the dome — coordination, flourishing', verb: 'Designing' },
  { key: 'production', label: 'BUILD', num: '03', desc: 'Execute contracts, connect systems', verb: 'Building' },
  { key: 'post_production', label: 'VERIFY', num: '04', desc: 'Test completeness, generate innovations', verb: 'Verifying' },
  { key: 'distribution', label: 'COMPLETE', num: '05', desc: 'Final COSM score and narrative', verb: 'Completing' },
]

// ── Hex Radar Chart for COSM ──────────────────────────────────────────
function CosmRadar({ dimensions, size = 200, animated = true }) {
  const dims = [
    { key: 'legal', label: 'LEGAL', color: '#00e5ff' },
    { key: 'data', label: 'DATA', color: '#7c4dff' },
    { key: 'fiscal', label: 'FISCAL', color: '#00e676' },
    { key: 'coordination', label: 'COORD', color: '#ffab00' },
    { key: 'flourishing', label: 'FLOUR', color: '#ff4081' },
    { key: 'narrative', label: 'NARR', color: '#448aff' },
  ]

  const cx = size / 2, cy = size / 2, r = size * 0.38
  const angleStep = (Math.PI * 2) / 6

  const getPoint = (i, val) => {
    const angle = angleStep * i - Math.PI / 2
    const dist = (val / 100) * r
    return { x: cx + dist * Math.cos(angle), y: cy + dist * Math.sin(angle) }
  }

  const gridLevels = [0.25, 0.5, 0.75, 1.0]
  const total = dimensions ? Object.values(dimensions).reduce((a, b) => a + b, 0) / 6 : 0

  return (
    <svg viewBox={`0 0 ${size} ${size}`} className="cosm-radar">
      {/* Grid */}
      {gridLevels.map(level => (
        <polygon key={level}
          points={dims.map((_, i) => {
            const p = getPoint(i, level * 100)
            return `${p.x},${p.y}`
          }).join(' ')}
          fill="none" stroke="rgba(255,255,255,0.06)" strokeWidth="0.5"
        />
      ))}
      {/* Axes */}
      {dims.map((_, i) => {
        const p = getPoint(i, 100)
        return <line key={i} x1={cx} y1={cy} x2={p.x} y2={p.y} stroke="rgba(255,255,255,0.04)" strokeWidth="0.5" />
      })}
      {/* Value polygon */}
      {dimensions && (
        <polygon
          points={dims.map((d, i) => {
            const p = getPoint(i, dimensions[d.key] || 0)
            return `${p.x},${p.y}`
          }).join(' ')}
          fill="rgba(0,229,255,0.12)" stroke="var(--domes-primary)" strokeWidth="1.5"
          className={animated ? 'radar-fill-animate' : ''}
        />
      )}
      {/* Dots + Labels */}
      {dims.map((d, i) => {
        const val = dimensions ? (dimensions[d.key] || 0) : 0
        const p = getPoint(i, val)
        const lp = getPoint(i, 115)
        return (
          <g key={d.key}>
            {dimensions && <circle cx={p.x} cy={p.y} r="3" fill={d.color} className="radar-dot" />}
            <text x={lp.x} y={lp.y} textAnchor="middle" dominantBaseline="middle"
              fill="var(--text-secondary)" fontSize="8" fontFamily="Exo 2">{d.label}</text>
            {dimensions && (
              <text x={lp.x} y={lp.y + 10} textAnchor="middle" fill={d.color} fontSize="7" fontFamily="Orbitron" fontWeight="600">
                {val.toFixed(0)}
              </text>
            )}
          </g>
        )
      })}
      {/* Center score */}
      <text x={cx} y={cy - 6} textAnchor="middle" fill="var(--domes-primary)" fontSize="18" fontFamily="Orbitron" fontWeight="700">
        {total.toFixed(0)}
      </text>
      <text x={cx} y={cy + 8} textAnchor="middle" fill="var(--text-dim)" fontSize="7" fontFamily="Exo 2">COSM</text>
    </svg>
  )
}

// ── Data Engine Badge ─────────────────────────────────────────────────
function DataBadge({ stats, fragmentCount }) {
  const engineTotal = stats ? (stats.provisions || 0) + (stats.cost_points || 0) + (stats.gov_systems || 0) + (stats.enrichments || 0) : 0
  const total = engineTotal + (fragmentCount || 0)
  if (total === 0) return null
  return (
    <div className="data-badge">
      <div className="data-badge-pulse" />
      <span className="data-badge-count">{total.toLocaleString()}</span>
      <span className="data-badge-label">data points</span>
    </div>
  )
}

// ── Conditions of Existence Panel ────────────────────────────────────
function ConditionsPanel({ fragments }) {
  if (!fragments || Object.keys(fragments).length === 0) return null

  const get = (source, key) => fragments[source]?.data?.[key]
  const pct = v => v != null ? `${v.toFixed(1)}%` : '—'
  const money = v => v != null ? `$${v.toLocaleString()}` : '—'
  const num = v => v != null ? v.toLocaleString() : '—'

  const conditions = [
    { label: 'Population', value: num(get('census-demographics', 'total_pop')), icon: '▪' },
    { label: 'Median Age', value: get('census-demographics', 'median_age') ?? '—', icon: '▪' },
    { label: 'Median Income', value: money(get('census-income', 'median_household_income')), icon: '$' },
    { label: 'Poverty Rate', value: pct(get('census-income', 'poverty_total') > 0 ? (get('census-income', 'poverty_below') / get('census-income', 'poverty_total')) * 100 : null), icon: '!' },
    { label: 'Median Rent', value: money(get('census-housing', 'median_gross_rent')), icon: '⌂' },
    { label: 'Home Value', value: money(get('census-housing', 'median_home_value')), icon: '⌂' },
    { label: 'Vacancy Rate', value: pct(get('census-housing', 'total_units') > 0 ? (get('census-housing', 'vacant_units') / get('census-housing', 'total_units')) * 100 : null), icon: '□' },
    { label: 'Broadband', value: pct(get('census-internet', 'total_households_internet') > 0 ? (get('census-internet', 'broadband') / get('census-internet', 'total_households_internet')) * 100 : null), icon: '◈' },
    { label: 'Public Transit', value: pct(get('census-commute', 'workers_total') > 0 ? (get('census-commute', 'public_transit') / get('census-commute', 'workers_total')) * 100 : null), icon: '→' },
    { label: 'No Vehicle', value: pct(get('census-commute', 'workers_total') > 0 ? (get('census-commute', 'no_vehicle') / get('census-commute', 'workers_total')) * 100 : null), icon: '×' },
    { label: 'SNAP Households', value: num(get('census-income', 'snap_households')), icon: '◆' },
    { label: 'Gini Index', value: get('census-income', 'gini_index')?.toFixed(4) ?? '—', icon: '△' },
  ]

  const sourceCount = Object.keys(fragments).length
  const countyName = Object.values(fragments)[0]?.county_name || 'Unknown'

  return (
    <div className="section-block conditions-panel">
      <h3 className="section-title">CONDITIONS OF EXISTENCE</h3>
      <p className="section-subtitle">{sourceCount} fragment sources for {countyName} — real Census ACS data</p>
      <div className="conditions-grid">
        {conditions.map((c, i) => (
          <div key={i} className="condition-cell" style={{ animationDelay: `${i * 0.04}s` }}>
            <span className="condition-icon">{c.icon}</span>
            <span className="condition-value">{c.value}</span>
            <span className="condition-label">{c.label}</span>
          </div>
        ))}
      </div>
    </div>
  )
}

// ── Dome Financial Instrument Panel ──────────────────────────────────
function DomeInstrumentPanel({ domes }) {
  if (!domes || Object.keys(domes).length === 0) return null

  const archetypes = Object.values(domes)
  const totalDelta = archetypes.reduce((s, d) => s + (d.delta || 0), 0)

  return (
    <div className="section-block instrument-panel">
      <h3 className="section-title">DOME FINANCIAL INSTRUMENTS</h3>
      <p className="section-subtitle">Cosm assembler — fragmented cost vs coordinated cost per archetype</p>

      <div className="instrument-summary">
        <div className="instrument-stat big">
          <span className="is-val">${totalDelta.toLocaleString()}</span>
          <span className="is-label">Total coordination savings identified</span>
        </div>
        <div className="instrument-stat">
          <span className="is-val">{archetypes.length}</span>
          <span className="is-label">Domes assembled</span>
        </div>
        <div className="instrument-stat">
          <span className="is-val">{Math.round(archetypes.reduce((s, d) => s + d.cosm, 0) / archetypes.length)}</span>
          <span className="is-label">Avg Cosm score</span>
        </div>
      </div>

      <div className="archetypes-grid">
        {archetypes.map((dome, i) => (
          <DomeArchetypeCard key={dome.profile.id} dome={dome} index={i} />
        ))}
      </div>
    </div>
  )
}

function DomeArchetypeCard({ dome, index }) {
  const [expanded, setExpanded] = useState(false)
  const p = dome.profile

  return (
    <div className={`archetype-card ${expanded ? 'expanded' : ''}`}
      onClick={() => setExpanded(!expanded)}
      style={{ animationDelay: `${index * 0.08}s` }}>
      <div className="arch-header">
        <div className="arch-identity">
          <span className="arch-name">{p.name}</span>
          <span className="arch-desc">{p.description}</span>
        </div>
        <div className="arch-delta">
          <span className="arch-delta-val">${dome.delta.toLocaleString()}</span>
          <span className="arch-delta-label">dome value</span>
        </div>
      </div>
      <div className="arch-row">
        <span className="arch-detail">Age {p.age}</span>
        <span className="arch-detail">${p.income.toLocaleString()}/yr</span>
        <span className="arch-detail">HH {p.household}</span>
        <span className="arch-detail">{dome.program_count} programs</span>
        <span className="arch-detail">Cosm {dome.cosm}</span>
      </div>
      <div className="arch-costs">
        <div className="arch-cost fragmented">
          <span className="ac-label">Fragmented</span>
          <span className="ac-val">${dome.fragmented_cost.toLocaleString()}</span>
        </div>
        <div className="arch-cost-arrow">→</div>
        <div className="arch-cost coordinated">
          <span className="ac-label">Coordinated</span>
          <span className="ac-val">${dome.coordinated_cost.toLocaleString()}</span>
        </div>
        <div className="arch-cost-arrow">=</div>
        <div className="arch-cost delta">
          <span className="ac-label">Delta</span>
          <span className="ac-val">${dome.delta.toLocaleString()}</span>
        </div>
      </div>
      {expanded && (
        <div className="arch-programs">
          <div className="arch-programs-label">ELIGIBLE PROGRAMS</div>
          <div className="arch-programs-list">
            {dome.eligible_programs.map((prog, j) => (
              <div key={j} className="arch-program">
                <span className="ap-name">{prog.program}</span>
                <span className="ap-val">${prog.annual_value.toLocaleString()}/yr</span>
                <span className="ap-cat">{prog.category}</span>
              </div>
            ))}
          </div>
          {dome.domain_coverage && (
            <div className="arch-domains">
              <div className="arch-programs-label">12-DOMAIN COVERAGE</div>
              <div className="arch-domain-bars">
                {Object.entries(dome.domain_coverage).map(([domain, cov]) => (
                  <div key={domain} className="domain-bar-row">
                    <span className="db-name">{domain}</span>
                    <div className="db-track">
                      <div className="db-fill" style={{ width: `${cov.score}%` }} />
                    </div>
                    <span className="db-val">{cov.score}</span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

// ── Provision Card ────────────────────────────────────────────────────
function ProvisionCard({ provision, index }) {
  const [open, setOpen] = useState(false)
  return (
    <div className={`provision-card ${open ? 'open' : ''}`} onClick={() => setOpen(!open)} style={{ animationDelay: `${index * 0.05}s` }}>
      <div className="provision-header">
        <span className="provision-citation">{provision.citation}</span>
        <span className="provision-expand">{open ? '−' : '+'}</span>
      </div>
      <div className="provision-title">{provision.title}</div>
      {open && (
        <div className="provision-body">
          <p>{provision.body}</p>
          {provision.authority && <div className="provision-authority">Authority: {provision.authority}</div>}
        </div>
      )}
    </div>
  )
}

// ── Cost Stat ─────────────────────────────────────────────────────────
function CostStat({ metric, value, unit, source }) {
  const fmt = (v) => {
    if (v >= 1e9) return `$${(v / 1e9).toFixed(1)}B`
    if (v >= 1e6) return `$${(v / 1e6).toFixed(1)}M`
    if (v >= 1e3 && unit.includes('$')) return `$${(v / 1e3).toFixed(1)}K`
    if (unit === '%') return `${v}%`
    return unit.includes('$') ? `$${v.toLocaleString()}` : v.toLocaleString()
  }
  return (
    <div className="cost-stat">
      <div className="cost-value">{fmt(value)}</div>
      <div className="cost-unit">{unit}</div>
      <div className="cost-metric">{metric}</div>
      <div className="cost-source">{source}</div>
    </div>
  )
}

// ── System Node (for network graph) ───────────────────────────────────
function SystemMap({ systems, links }) {
  if (!systems || systems.length === 0) return null
  const activeCount = links ? links.filter(l => l.type === 'active').length : 0
  const blockedCount = links ? links.filter(l => l.type === 'blocked').length : 0
  const possibleCount = links ? links.filter(l => l.type === 'possible').length : 0

  return (
    <div className="system-map">
      <div className="system-map-header">
        <h4>{systems.length} GOVERNMENT DATA SYSTEMS</h4>
        <div className="link-legend">
          <span className="legend-item active">{activeCount} active</span>
          <span className="legend-item blocked">{blockedCount} blocked</span>
          <span className="legend-item possible">{possibleCount} possible</span>
        </div>
      </div>
      <div className="system-grid">
        {systems.map((sys, i) => (
          <div key={sys.code || i} className={`system-node level-${sys.level}`}>
            <div className="system-code">{sys.code}</div>
            <div className="system-name">{sys.name}</div>
            <div className="system-agency">{sys.agency}</div>
            <div className="system-meta">
              <span className={`consent-${sys.consent_required}`}>{sys.consent_required}</span>
              <span>{sys.data_fields?.length || 0} fields</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

// ── Coordination Model Card ───────────────────────────────────────────
function CoordModelCard({ model, index, selected, onSelect }) {
  return (
    <div className={`coord-card ${selected ? 'selected' : ''}`} onClick={onSelect}
      style={{ animationDelay: `${index * 0.1}s` }}>
      <div className="coord-header">
        <div className="coord-fit">{(model.fit_score * 100).toFixed(0)}%</div>
        <div className="coord-name">{model.name}</div>
      </div>
      <p className="coord-desc">{model.description}</p>
      <div className="coord-stats">
        <div className="coord-stat">
          <span className="stat-val">{model.estimated_savings_pct}%</span>
          <span className="stat-label">savings</span>
        </div>
        <div className="coord-stat">
          <span className="stat-val">{model.implementation_cost}</span>
          <span className="stat-label">cost</span>
        </div>
        <div className="coord-stat">
          <span className="stat-val">{model.systems_connected?.length || 0}</span>
          <span className="stat-label">systems</span>
        </div>
      </div>
      {selected && (
        <div className="coord-details">
          <div className="coord-section">
            <strong>Real Examples:</strong>
            <ul>{model.real_examples?.map((ex, i) => <li key={i}>{ex}</li>)}</ul>
          </div>
          <div className="coord-section">
            <strong>Legal Authority:</strong>
            <p>{model.legal_authority}</p>
          </div>
          <div className="coord-section">
            <strong>Consent Model:</strong>
            <p>{model.consent_model}</p>
          </div>
        </div>
      )}
    </div>
  )
}

// ── Architecture Layer ────────────────────────────────────────────────
function DomeLayer({ layer, index }) {
  const strengthPct = ((layer.strength || 0) * 100).toFixed(0)
  return (
    <div className="dome-layer" style={{ animationDelay: `${index * 0.08}s` }}>
      <div className="layer-bar">
        <div className="layer-fill" style={{ width: `${strengthPct}%` }} />
      </div>
      <div className="layer-info">
        <span className="layer-name">{layer.name}</span>
        <span className="layer-strength">{strengthPct}%</span>
      </div>
    </div>
  )
}

// ── Narrative Section ─────────────────────────────────────────────────
function NarrativeSection({ section, index }) {
  return (
    <div className="narrative-section" style={{ animationDelay: `${index * 0.15}s` }}>
      <div className="narrative-num">{String(index + 1).padStart(2, '0')}</div>
      <div className="narrative-content">
        <h4>{section.title}</h4>
        <p>{section.content}</p>
      </div>
    </div>
  )
}

// ── Stage Content Renderers ───────────────────────────────────────────

function DevelopmentStage({ data }) {
  if (!data) return null
  const provisions = data.legal_provisions || {}
  const costs = data.cost_landscape || {}
  const systems = data.government_systems || []
  const links = data.system_links || []
  const profile = data.profile || {}

  const allProvisions = Object.values(provisions).flat()
  const topCosts = Object.values(costs).flat().slice(0, 12)

  return (
    <div className="stage-content development">
      {/* Profile Banner */}
      <div className="profile-banner">
        <div className="profile-name">{profile.name || 'Subject'}</div>
        <div className="profile-stats">
          <div className="profile-stat">
            <span className="ps-val">{data.provision_count || 0}</span>
            <span className="ps-label">provisions</span>
          </div>
          <div className="profile-stat">
            <span className="ps-val">{data.cost_point_count || 0}</span>
            <span className="ps-label">cost points</span>
          </div>
          <div className="profile-stat">
            <span className="ps-val">{data.system_count || 0}</span>
            <span className="ps-label">systems</span>
          </div>
          <div className="profile-stat">
            <span className="ps-val">{data.active_links || 0}</span>
            <span className="ps-label">active links</span>
          </div>
          <div className="profile-stat warn">
            <span className="ps-val">{data.blocked_links || 0}</span>
            <span className="ps-label">blocked</span>
          </div>
        </div>
        <div className="profile-fragcost">
          Estimated annual fragmentation cost: <strong>${(profile.estimated_annual_fragmentation_cost || 78168).toLocaleString()}</strong>/person
        </div>
      </div>

      {/* Legal Provisions by Dimension */}
      <div className="section-block">
        <h3 className="section-title">LEGAL LANDSCAPE</h3>
        <p className="section-subtitle">{allProvisions.length} real CFR provisions across {Object.keys(provisions).length} regulatory dimensions</p>
        <div className="dimension-tabs">
          {Object.entries(provisions).map(([dim, provs]) => (
            <details key={dim} className="dim-group">
              <summary className="dim-tab">
                <span className="dim-name">{dim.replace(/_/g, ' ')}</span>
                <span className="dim-count">{provs.length}</span>
              </summary>
              <div className="dim-provisions">
                {provs.map((p, i) => <ProvisionCard key={i} provision={p} index={i} />)}
              </div>
            </details>
          ))}
        </div>
      </div>

      {/* Cost Landscape */}
      <div className="section-block">
        <h3 className="section-title">COST LANDSCAPE</h3>
        <p className="section-subtitle">Real costs sourced from CMS, HUD, Vera Institute, HCUP, SAMHSA</p>
        <div className="cost-grid">
          {topCosts.map((c, i) => <CostStat key={i} {...c} />)}
        </div>
      </div>

      {/* System Map */}
      <div className="section-block">
        <h3 className="section-title">GOVERNMENT DATA SYSTEMS</h3>
        <SystemMap systems={systems} links={links} />
      </div>
    </div>
  )
}

function PreProductionStage({ data }) {
  if (!data) return null
  const arch = data.architecture || {}
  const models = data.coordination_models || []
  const flour = data.flourishing || {}
  const insights = data.enrichment_insights || []
  const [selectedModel, setSelectedModel] = useState(0)

  return (
    <div className="stage-content pre-production">
      {/* Dome Architecture */}
      <div className="section-block">
        <h3 className="section-title">DOME ARCHITECTURE</h3>
        <div className="arch-header">
          <div className="arch-coverage">
            <span className="arch-pct">{((arch.overall_coverage || 0) * 100).toFixed(0)}%</span>
            <span className="arch-label">coverage</span>
          </div>
        </div>
        <div className="dome-layers">
          {(arch.layers || []).map((layer, i) => <DomeLayer key={i} layer={layer} index={i} />)}
        </div>
      </div>

      {/* Coordination Models */}
      <div className="section-block">
        <h3 className="section-title">COORDINATION MODELS</h3>
        <p className="section-subtitle">Select the architecture for cross-system coordination</p>
        <div className="coord-grid">
          {models.map((m, i) => (
            <CoordModelCard key={m.id || i} model={m} index={i}
              selected={selectedModel === i} onSelect={() => setSelectedModel(i)} />
          ))}
        </div>
      </div>

      {/* Flourishing Scores */}
      <div className="section-block">
        <h3 className="section-title">FLOURISHING INDEX</h3>
        <div className="flour-header">
          <div className="flour-score">
            <span className="flour-val">{((flour.overall_score || 0) * 100).toFixed(0)}%</span>
            <span className="flour-label">current</span>
          </div>
          <div className="flour-gap">
            <span className="flour-val gap">{((flour.overall_gap || 0) * 100).toFixed(0)}%</span>
            <span className="flour-label">gap to threshold</span>
          </div>
        </div>
        <div className="flour-dims">
          {Object.entries(flour.scores || {}).map(([dim, score]) => (
            <div key={dim} className="flour-dim">
              <span className="flour-dim-name">{dim}</span>
              <div className="flour-bar">
                <div className="flour-fill" style={{ width: `${(score.score || 0) * 100}%` }} />
                <div className="flour-gap-fill" style={{ left: `${(score.score || 0) * 100}%`, width: `${(score.gap || 0) * 100}%` }} />
              </div>
              <span className="flour-dim-val">{((score.score || 0) * 100).toFixed(0)}%</span>
            </div>
          ))}
        </div>
      </div>

      {/* Enrichment Insights */}
      {insights.length > 0 && (
        <div className="section-block">
          <h3 className="section-title">INTELLIGENCE INSIGHTS</h3>
          <div className="insights-list">
            {insights.slice(0, 6).map((ins, i) => (
              <div key={i} className={`insight-card type-${ins.type}`}>
                <span className="insight-type">{ins.type?.replace(/_/g, ' ')}</span>
                <p>{ins.description}</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

function ProductionStage({ data }) {
  if (!data) return null
  const contracts = data.contracts?.agreements || []
  const profile = data.profile || {}

  return (
    <div className="stage-content production">
      <div className="build-banner">
        <div className="build-icon">&#9670;</div>
        <h3>DOME CONSTRUCTED</h3>
        <p>{profile.provisions_applied || 0} provisions applied across {profile.systems_connected || 0} systems</p>
      </div>

      <div className="section-block">
        <h3 className="section-title">EXECUTED AGREEMENTS</h3>
        <div className="contracts-list">
          {contracts.map((c, i) => (
            <div key={i} className="contract-card" style={{ animationDelay: `${i * 0.1}s` }}>
              <div className="contract-header">
                <span className="contract-status">{c.status}</span>
                <span className="contract-type">{c.type}</span>
              </div>
              <div className="contract-parties">
                {(c.parties || []).map((p, j) => <span key={j} className="party-tag">{p}</span>)}
              </div>
              <div className="contract-savings">
                Est. savings: <strong>{c.estimated_savings_pct}%</strong>
              </div>
              {c.legal_authority && <div className="contract-authority">{c.legal_authority}</div>}
            </div>
          ))}
        </div>
      </div>

      <div className="section-block">
        <h3 className="section-title">DOME PROFILE</h3>
        <div className="dome-profile-grid">
          {profile.coverage_dimensions?.map((dim, i) => (
            <span key={i} className="dim-tag">{dim}</span>
          ))}
        </div>
        <div className="dome-profile-stat">
          Coordination Model: <strong>{profile.coordination_model}</strong>
        </div>
      </div>
    </div>
  )
}

function PostProductionStage({ data }) {
  if (!data) return null
  const ver = data.verification || {}
  const innovations = data.innovations || {}

  return (
    <div className="stage-content post-production">
      {/* Verification */}
      <div className="section-block">
        <h3 className="section-title">DOME VERIFICATION</h3>
        <div className={`verify-badge ${ver.complete ? 'complete' : 'incomplete'}`}>
          <span className="verify-icon">{ver.complete ? '✓' : '!'}</span>
          <span className="verify-pct">{((ver.coverage || 0) * 100).toFixed(0)}%</span>
          <span className="verify-label">coverage across {ver.dimensions_covered?.length || 0} dimensions</span>
        </div>

        {ver.dimensions_covered && (
          <div className="covered-dims">
            {ver.dimensions_covered.map(d => <span key={d} className="dim-tag covered">{d}</span>)}
            {(ver.gaps || []).map(g => <span key={g} className="dim-tag gap">{g}</span>)}
          </div>
        )}

        {ver.recommendations?.length > 0 && (
          <div className="recommendations">
            {ver.recommendations.map((r, i) => (
              <div key={i} className="rec-item">
                <span className="rec-arrow">→</span>
                <span>{r}</span>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Innovations */}
      <div className="section-block">
        <h3 className="section-title">INNOVATIONS GENERATED</h3>
        <div className="innovations-grid">
          {(innovations.innovations || []).map((inn, i) => (
            <div key={i} className="innovation-card" style={{ animationDelay: `${i * 0.08}s` }}>
              <span className="inn-icon">◆</span>
              <span>{inn}</span>
            </div>
          ))}
        </div>
        {(innovations.patents || []).length > 0 && (
          <div className="patents-section">
            <h4>PATENTS</h4>
            {innovations.patents.map((p, i) => <div key={i} className="patent-item">{p}</div>)}
          </div>
        )}
        {(innovations.protocols || []).length > 0 && (
          <div className="protocols-section">
            <h4>PROTOCOLS</h4>
            {innovations.protocols.map((p, i) => <div key={i} className="protocol-item">{p}</div>)}
          </div>
        )}
      </div>
    </div>
  )
}

function DistributionStage({ data }) {
  if (!data) return null
  const narrative = data.narrative?.sections || []
  const cosm = data.cosm || {}
  const ip = data.ip || []
  const industries = data.industries_changed || []

  return (
    <div className="stage-content distribution">
      {/* COSM Reveal */}
      <div className="cosm-reveal">
        <CosmRadar dimensions={cosm} size={260} />
        <div className="cosm-total">
          <span className="cosm-total-val">{(cosm.total || 0).toFixed(1)}</span>
          <span className="cosm-total-label">TOTAL COSM</span>
        </div>
      </div>

      {/* Narrative */}
      <div className="section-block">
        <h3 className="section-title">THE NARRATIVE</h3>
        <div className="narrative-flow">
          {narrative.map((s, i) => <NarrativeSection key={i} section={s} index={i} />)}
        </div>
      </div>

      {/* IP + Industries */}
      <div className="final-grid">
        <div className="section-block">
          <h3 className="section-title">INTELLECTUAL PROPERTY</h3>
          <div className="ip-list">
            {ip.map((item, i) => <div key={i} className="ip-item">{item}</div>)}
          </div>
        </div>
        <div className="section-block">
          <h3 className="section-title">INDUSTRIES CHANGED</h3>
          <div className="industries-list">
            {industries.map((ind, i) => <span key={i} className="industry-tag">{ind}</span>)}
          </div>
        </div>
      </div>
    </div>
  )
}

// ══════════════════════════════════════════════════════════════════════
// MAIN DOMES GAME COMPONENT
// ══════════════════════════════════════════════════════════════════════

export default function DomesGame({ player, production, onUpdate, onBack }) {
  const [working, setWorking] = useState(false)
  const [lastMessage, setLastMessage] = useState(null)
  const [fragmentData, setFragmentData] = useState(null)
  const [domeData, setDomeData] = useState(null)
  const contentRef = useRef(null)

  // Fetch Fragment/Cosm data for Philadelphia (default county)
  useEffect(() => {
    const fips = '42101' // Philadelphia — primary geography
    fetch(`/api/fragment/county/${fips}`)
      .then(r => r.json())
      .then(d => { if (d.fragment_count > 0) setFragmentData(d) })
      .catch(() => {})
    fetch(`/api/cosm/domes/${fips}`)
      .then(r => r.json())
      .then(d => { if (d.dome_count > 0) setDomeData(d) })
      .catch(() => {})
  }, [])

  const currentStageIndex = STAGES.findIndex(s => s.key === production.stage)
  const isComplete = production.progress >= 100
  const currentStage = STAGES[currentStageIndex] || STAGES[0]

  const handleAdvance = async () => {
    setWorking(true)
    setLastMessage(null)
    try {
      const res = await fetch(`/api/productions/${production.production_id}/advance`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ production_id: production.production_id, action: `advance_${production.stage}`, data: {} })
      })
      const result = await res.json()
      if (result.success) {
        setLastMessage(result.message)
        await onUpdate()
        if (contentRef.current) contentRef.current.scrollTo({ top: 0, behavior: 'smooth' })
      } else {
        setLastMessage(`Error: ${result.message}`)
      }
    } catch (err) {
      setLastMessage(`Failed: ${err.message}`)
    } finally {
      setWorking(false)
    }
  }

  // Get stage data for current display
  const stageData = production.stage_data || {}
  const devData = stageData.development
  const preData = stageData.pre_production
  const prodData = stageData.production
  const postData = stageData.post_production
  const distData = stageData.distribution

  // Build running COSM from available data
  const runningCosm = distData?.cosm || null

  return (
    <div className="domes-game">
      {/* ── Fixed Header ────────────────────────────────────── */}
      <div className="game-header">
        <div className="game-header-left">
          <button className="back-btn" onClick={onBack}>← GAMES</button>
          <div className="game-badge">DOMES</div>
          <div className="game-subject">{production.subject}</div>
        </div>
        <div className="game-header-center">
          <div className="stage-track-mini">
            {STAGES.map((s, i) => (
              <div key={s.key} className={`mini-node ${i < currentStageIndex ? 'done' : ''} ${i === currentStageIndex ? 'active' : ''}`}>
                <div className="mini-dot" />
                <span className="mini-label">{s.num}</span>
              </div>
            ))}
            <div className="mini-line">
              <div className="mini-fill" style={{ width: `${(currentStageIndex / 4) * 100}%` }} />
            </div>
          </div>
        </div>
        <div className="game-header-right">
          <DataBadge stats={devData?.data_engine_stats || distData?.data_engine_stats} fragmentCount={fragmentData?.fragment_count} />
          {runningCosm && (
            <div className="header-cosm">
              <span className="header-cosm-val">{(runningCosm.total || 0).toFixed(0)}</span>
              <span className="header-cosm-label">COSM</span>
            </div>
          )}
        </div>
      </div>

      {/* ── Stage Hero ──────────────────────────────────────── */}
      <div className="stage-hero">
        <div className="stage-hero-bg" />
        <div className="stage-hero-content">
          <div className="stage-num">{currentStage.num}</div>
          <div className="stage-info">
            <h2>{currentStage.label}</h2>
            <p>{currentStage.desc}</p>
          </div>
          <div className="stage-progress-ring">
            <svg viewBox="0 0 60 60">
              <circle cx="30" cy="30" r="26" fill="none" stroke="rgba(255,255,255,0.06)" strokeWidth="3" />
              <circle cx="30" cy="30" r="26" fill="none" stroke="var(--domes-primary)" strokeWidth="3"
                strokeDasharray={`${production.progress * 1.634} 163.4`}
                strokeLinecap="round" transform="rotate(-90 30 30)" />
            </svg>
            <span className="progress-pct">{production.progress.toFixed(0)}%</span>
          </div>
        </div>
      </div>

      {/* ── Content Area ────────────────────────────────────── */}
      <div className="game-content" ref={contentRef}>
        {/* Status Message */}
        {lastMessage && (
          <div className="game-message">
            <div className="message-line" />
            <p>{lastMessage}</p>
          </div>
        )}

        {/* Render completed stages + Fragment/Cosm intelligence */}
        {devData && <DevelopmentStage data={devData} />}
        {devData && fragmentData && <ConditionsPanel fragments={fragmentData.fragments} />}
        {devData && domeData && <DomeInstrumentPanel domes={domeData.domes} />}
        {preData && <PreProductionStage data={preData} />}
        {prodData && <ProductionStage data={prodData} />}
        {postData && <PostProductionStage data={postData} />}
        {distData && <DistributionStage data={distData} />}

        {/* No data yet prompt */}
        {!devData && !isComplete && (
          <div className="empty-stage">
            <div className="empty-icon">◇</div>
            <p>Begin research to map the legal landscape, cost data, and government systems for <strong>{production.subject}</strong>.</p>
          </div>
        )}
      </div>

      {/* ── Fixed Action Bar ────────────────────────────────── */}
      <div className="game-action-bar">
        {!isComplete ? (
          <button className="advance-btn" onClick={handleAdvance} disabled={working}>
            {working ? (
              <>
                <span className="spinner" />
                <span>{currentStage.verb}...</span>
              </>
            ) : (
              <>
                <span>{currentStageIndex === 0 && !devData ? 'BEGIN RESEARCH' : `ADVANCE → ${STAGES[Math.min(currentStageIndex + 1, 4)]?.label || 'COMPLETE'}`}</span>
              </>
            )}
          </button>
        ) : (
          <div className="complete-bar">
            <span className="complete-icon">◆</span>
            <span>DOME COMPLETE — COSM: {(runningCosm?.total || 0).toFixed(1)}</span>
          </div>
        )}
      </div>
    </div>
  )
}
