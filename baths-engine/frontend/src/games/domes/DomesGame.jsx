import { useState, useEffect, useRef } from 'react'
import './DomesGame.css'

const STAGES = [
  { key: 'development', label: 'DEVELOPMENT', num: '01', desc: 'Rights acquisition, market research, development deal', verb: 'Developing' },
  { key: 'pre_production', label: 'PRE-PRODUCTION', num: '02', desc: 'Script, budget top sheet, cast & crew', verb: 'Pre-Producing' },
  { key: 'production', label: 'PRODUCTION', num: '03', desc: 'Execute agreements, connect systems, build the dome', verb: 'Producing' },
  { key: 'post_production', label: 'POST-PRODUCTION', num: '04', desc: 'Assembly cut, color grade, sound mix, VFX finals', verb: 'Post-Producing' },
  { key: 'distribution', label: 'DISTRIBUTION', num: '05', desc: 'COSM reveal, IP catalog, Dome Bond, replication kit', verb: 'Distributing' },
]

const IP_DOMAIN_LABELS = {
  entertainment: 'Entertainment IP',
  technology: 'Technology IP',
  financial_product: 'Financial Product IP',
  policy: 'Policy IP',
  product: 'Product IP',
  research: 'Research IP',
  housing: 'Housing IP',
  healthcare: 'Healthcare IP',
}

const IP_DOMAIN_COLORS = {
  entertainment: '#ff4081',
  technology: '#7c4dff',
  financial_product: '#00e676',
  policy: '#ffab00',
  product: '#00e5ff',
  research: '#448aff',
  housing: '#ff6d00',
  healthcare: '#e040fb',
}

// ── Hex Radar Chart for COSM ──────────────────────────────────────────
function CosmRadar({ dimensions, size = 200, animated = true }) {
  const dims = [
    { key: 'rights', label: 'RIGHTS', color: '#00e5ff' },
    { key: 'research', label: 'RESEARCH', color: '#7c4dff' },
    { key: 'budget', label: 'BUDGET', color: '#00e676' },
    { key: 'package', label: 'PACKAGE', color: '#ffab00' },
    { key: 'deliverables', label: 'DELIVER', color: '#ff4081' },
    { key: 'pitch', label: 'PITCH', color: '#448aff' },
  ]

  const cx = size / 2, cy = size / 2, r = size * 0.38
  const angleStep = (Math.PI * 2) / 6

  const getPoint = (i, val) => {
    const angle = angleStep * i - Math.PI / 2
    const dist = (val / 100) * r
    return { x: cx + dist * Math.cos(angle), y: cy + dist * Math.sin(angle) }
  }

  const gridLevels = [0.25, 0.5, 0.75, 1.0]
  const total = dimensions ? Math.min(
    dimensions.rights || 0, dimensions.research || 0, dimensions.budget || 0,
    dimensions.package || 0, dimensions.deliverables || 0, dimensions.pitch || 0
  ) : 0

  return (
    <svg viewBox={`0 0 ${size} ${size}`} className="cosm-radar">
      {gridLevels.map(level => (
        <polygon key={level}
          points={dims.map((_, i) => {
            const p = getPoint(i, level * 100)
            return `${p.x},${p.y}`
          }).join(' ')}
          fill="none" stroke="rgba(255,255,255,0.06)" strokeWidth="0.5"
        />
      ))}
      {dims.map((_, i) => {
        const p = getPoint(i, 100)
        return <line key={i} x1={cx} y1={cy} x2={p.x} y2={p.y} stroke="rgba(255,255,255,0.04)" strokeWidth="0.5" />
      })}
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

// ── System Map ────────────────────────────────────────────────────────
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

// ── Coordination Crew Card ────────────────────────────────────────────
function CrewCard({ model, index, selected, onSelect }) {
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

// ── Dome Layer ────────────────────────────────────────────────────────
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

// ── IP Catalog ────────────────────────────────────────────────────────
function IPCatalog({ ipOutputs }) {
  if (!ipOutputs || ipOutputs.length === 0) return null

  const byDomain = {}
  ipOutputs.forEach(ip => {
    const d = ip.domain
    if (!byDomain[d]) byDomain[d] = []
    byDomain[d].push(ip)
  })

  return (
    <div className="section-block ip-catalog">
      <h3 className="section-title">IP CATALOG</h3>
      <p className="section-subtitle">{ipOutputs.length} outputs across {Object.keys(byDomain).length} domains</p>
      <div className="ip-grid">
        {Object.entries(byDomain).map(([domain, items]) => (
          <div key={domain} className="ip-domain-group">
            <div className="ip-domain-header" style={{ borderColor: IP_DOMAIN_COLORS[domain] || '#8090a8' }}>
              <span className="ip-domain-dot" style={{ background: IP_DOMAIN_COLORS[domain] || '#8090a8' }} />
              <span className="ip-domain-name">{IP_DOMAIN_LABELS[domain] || domain}</span>
            </div>
            {items.map((ip, j) => (
              <div key={j} className="ip-item">
                <div className="ip-title">{ip.title}</div>
                <div className="ip-desc">{ip.description}</div>
                <div className="ip-meta">
                  <span className="ip-format">{ip.format?.replace(/_/g, ' ')}</span>
                  <span className="ip-driver">{ip.value_driver}</span>
                </div>
              </div>
            ))}
          </div>
        ))}
      </div>
    </div>
  )
}

// ── Bond Term Sheet ───────────────────────────────────────────────────
function BondTermSheet({ bond, type = 'dome' }) {
  if (!bond) return null

  const ratingColors = { AAA: '#00e676', AA: '#69f0ae', A: '#b2ff59', BBB: '#ffab00', BB: '#ff9100', B: '#ff6d00' }

  return (
    <div className={`section-block bond-term-sheet ${type}`}>
      <h3 className="section-title">{type === 'dome' ? 'DOME' : 'CHRON'} BOND TERM SHEET</h3>
      <div className="bond-header-row">
        <div className="bond-id">{bond.bond_id}</div>
        <div className="bond-rating" style={{ color: ratingColors[bond.rating] || '#8090a8' }}>
          {bond.rating}
        </div>
      </div>
      <div className="bond-grid">
        <div className="bond-stat primary">
          <span className="bs-val">${bond.face_value?.toLocaleString()}</span>
          <span className="bs-label">Face Value</span>
        </div>
        <div className="bond-stat">
          <span className="bs-val">{bond.coupon_rate}%</span>
          <span className="bs-label">Coupon Rate</span>
        </div>
        <div className="bond-stat">
          <span className="bs-val">{bond.maturity_years}yr</span>
          <span className="bs-label">Maturity</span>
        </div>
        <div className="bond-stat">
          <span className="bs-val">{bond.yield_to_maturity}%</span>
          <span className="bs-label">YTM</span>
        </div>
        <div className="bond-stat">
          <span className="bs-val">{bond.cosm_score || bond.chron_score}</span>
          <span className="bs-label">{type === 'dome' ? 'COSM' : 'CHRON'} Score</span>
        </div>
        <div className="bond-stat">
          <span className="bs-val">{bond.programs_backing || bond.sqft_backing?.toLocaleString()}</span>
          <span className="bs-label">{type === 'dome' ? 'Programs Backing' : 'Sqft Backing'}</span>
        </div>
      </div>
    </div>
  )
}

// ── Stage Content Renderers ───────────────────────────────────────────

function DevelopmentStage({ data }) {
  if (!data) return null
  const rights = data.rights_package || {}
  const market = data.market_analysis || {}
  const cast = data.cast_list || []
  const deal = data.deal_structure || []
  const profile = data.profile || {}

  const allRights = Object.values(rights).flat()
  const topCosts = Object.values(market).flat().slice(0, 12)

  return (
    <div className="stage-content development">
      {/* Profile Banner */}
      <div className="profile-banner">
        <div className="profile-name">{profile.name || 'Subject'}</div>
        <div className="profile-stats">
          <div className="profile-stat">
            <span className="ps-val">{data.rights_count || 0}</span>
            <span className="ps-label">rights acquired</span>
          </div>
          <div className="profile-stat">
            <span className="ps-val">{data.cost_point_count || 0}</span>
            <span className="ps-label">market data points</span>
          </div>
          <div className="profile-stat">
            <span className="ps-val">{data.system_count || 0}</span>
            <span className="ps-label">systems cast</span>
          </div>
          <div className="profile-stat">
            <span className="ps-val">{data.active_links || 0}</span>
            <span className="ps-label">active deals</span>
          </div>
          <div className="profile-stat warn">
            <span className="ps-val">{data.blocked_links || 0}</span>
            <span className="ps-label">blocked</span>
          </div>
        </div>
        <div className="profile-fragcost">
          Annual fragmentation cost: <strong>${(profile.estimated_annual_fragmentation_cost || 78168).toLocaleString()}</strong>/person
        </div>
      </div>

      {/* Rights Package */}
      <div className="section-block">
        <h3 className="section-title">RIGHTS PACKAGE</h3>
        <p className="section-subtitle">{allRights.length} real CFR provisions across {Object.keys(rights).length} regulatory dimensions</p>
        <div className="dimension-tabs">
          {Object.entries(rights).map(([dim, provs]) => (
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

      {/* Market Analysis */}
      <div className="section-block">
        <h3 className="section-title">MARKET ANALYSIS</h3>
        <p className="section-subtitle">Real costs sourced from CMS, HUD, Vera Institute, HCUP, SAMHSA</p>
        <div className="cost-grid">
          {topCosts.map((c, i) => <CostStat key={i} {...c} />)}
        </div>
      </div>

      {/* Cast — System Map */}
      <div className="section-block">
        <h3 className="section-title">CAST — GOVERNMENT DATA SYSTEMS</h3>
        <SystemMap systems={cast} links={deal} />
      </div>
    </div>
  )
}

function PreProductionStage({ data }) {
  if (!data) return null
  const script = data.shooting_script || {}
  const crew = data.coordination_crew || []
  const flour = data.flourishing || {}
  const intelligence = data.intelligence || []
  const budget = data.budget_top_sheet || {}
  const [selectedCrew, setSelectedCrew] = useState(0)

  return (
    <div className="stage-content pre-production">
      {/* Shooting Script — Dome Architecture */}
      <div className="section-block">
        <h3 className="section-title">SHOOTING SCRIPT — DOME BLUEPRINT</h3>
        <div className="arch-header">
          <div className="arch-coverage">
            <span className="arch-pct">{((script.overall_coverage || 0) * 100).toFixed(0)}%</span>
            <span className="arch-label">coverage</span>
          </div>
        </div>
        <div className="dome-layers">
          {(script.layers || []).map((layer, i) => <DomeLayer key={i} layer={layer} index={i} />)}
        </div>
      </div>

      {/* Budget Top Sheet */}
      <div className="section-block">
        <h3 className="section-title">BUDGET TOP SHEET</h3>
        <div className="budget-sheet">
          <div className="budget-section">
            <div className="budget-section-label">ABOVE THE LINE</div>
            {Object.entries(budget.above_the_line || {}).map(([key, val]) => (
              <div key={key} className="budget-line">
                <span className="bl-name">{key.replace(/_/g, ' ')}</span>
                <span className="bl-val">${(val || 0).toLocaleString()}</span>
              </div>
            ))}
          </div>
          <div className="budget-section">
            <div className="budget-section-label">BELOW THE LINE</div>
            {Object.entries(budget.below_the_line || {}).map(([key, val]) => (
              <div key={key} className="budget-line">
                <span className="bl-name">{key.replace(/_/g, ' ')}</span>
                <span className="bl-val">{typeof val === 'number' ? `$${val.toLocaleString()}` : val}</span>
              </div>
            ))}
          </div>
          <div className="budget-totals">
            <div className="budget-total-row fragmented">
              <span>Annual Fragmentation Cost</span>
              <span>${(budget.annual_fragmentation_cost || 0).toLocaleString()}</span>
            </div>
            <div className="budget-total-row coordinated">
              <span>Annual Coordination Savings</span>
              <span>${(budget.annual_coordination_savings || 0).toLocaleString()}</span>
            </div>
            <div className="budget-total-row delta">
              <span>Annual Dome Value</span>
              <span>${(budget.annual_dome_value || 0).toLocaleString()}</span>
            </div>
          </div>
        </div>
      </div>

      {/* Coordination Crew */}
      <div className="section-block">
        <h3 className="section-title">COORDINATION CREW</h3>
        <p className="section-subtitle">Select the architecture for cross-system coordination</p>
        <div className="coord-grid">
          {crew.map((m, i) => (
            <CrewCard key={m.id || i} model={m} index={i}
              selected={selectedCrew === i} onSelect={() => setSelectedCrew(i)} />
          ))}
        </div>
      </div>

      {/* Deliverables Index — Flourishing */}
      <div className="section-block">
        <h3 className="section-title">DELIVERABLES INDEX</h3>
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

      {/* Intelligence */}
      {intelligence.length > 0 && (
        <div className="section-block">
          <h3 className="section-title">INTELLIGENCE BRIEF</h3>
          <div className="insights-list">
            {intelligence.slice(0, 6).map((ins, i) => (
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
  const agreements = data.executed_agreements || []
  const callSheet = data.call_sheet || {}
  const vfx = data.vfx_report || []

  return (
    <div className="stage-content production">
      {/* Call Sheet */}
      <div className="build-banner">
        <div className="build-icon">&#9670;</div>
        <h3>DOME UNDER CONSTRUCTION</h3>
        <p>{callSheet.rights_applied || 0} rights applied across {callSheet.systems_connected || 0} systems</p>
      </div>

      {/* Executed Agreements */}
      <div className="section-block">
        <h3 className="section-title">EXECUTED AGREEMENTS</h3>
        <div className="contracts-list">
          {agreements.map((c, i) => (
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

      {/* Call Sheet Details */}
      <div className="section-block">
        <h3 className="section-title">CALL SHEET</h3>
        <div className="dome-profile-grid">
          {callSheet.coverage_dimensions?.map((dim, i) => (
            <span key={i} className="dim-tag">{dim}</span>
          ))}
        </div>
        <div className="dome-profile-stat">
          Coordination Model: <strong>{callSheet.coordination_model}</strong>
        </div>
      </div>

      {/* VFX Report */}
      {vfx.length > 0 && (
        <div className="section-block">
          <h3 className="section-title">VFX — ENRICHMENT CROSS-REFERENCES</h3>
          <div className="insights-list">
            {vfx.slice(0, 6).map((v, i) => (
              <div key={i} className={`insight-card type-${v.type}`}>
                <span className="insight-type">{v.type?.replace(/_/g, ' ')}</span>
                <p>{v.description}</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

function PostProductionStage({ data }) {
  if (!data) return null
  const assembly = data.assembly_cut || {}
  const grade = data.color_grade || {}
  const vfx = data.vfx_finals || {}
  const ipOutputs = data.ip_outputs || []

  return (
    <div className="stage-content post-production">
      {/* Assembly Cut — Verification */}
      <div className="section-block">
        <h3 className="section-title">ASSEMBLY CUT — DOME VERIFICATION</h3>
        <div className={`verify-badge ${assembly.complete ? 'complete' : 'incomplete'}`}>
          <span className="verify-icon">{assembly.complete ? '✓' : '!'}</span>
          <span className="verify-pct">{((assembly.coverage || 0) * 100).toFixed(0)}%</span>
          <span className="verify-label">coverage across {assembly.dimensions_covered?.length || 0} dimensions</span>
        </div>

        {assembly.dimensions_covered && (
          <div className="covered-dims">
            {assembly.dimensions_covered.map(d => <span key={d} className="dim-tag covered">{d}</span>)}
            {(assembly.gaps || []).map(g => <span key={g} className="dim-tag gap">{g}</span>)}
          </div>
        )}

        {assembly.notes?.length > 0 && (
          <div className="recommendations">
            {assembly.notes.map((r, i) => (
              <div key={i} className="rec-item">
                <span className="rec-arrow">→</span>
                <span>{r}</span>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Color Grade — Flourishing */}
      <div className="section-block">
        <h3 className="section-title">COLOR GRADE — DELIVERABLES</h3>
        <div className="grade-badge">
          <span className="grade-letter">{grade.grade || 'C'}</span>
          <span className="grade-desc">Flourishing Index: {((grade.overall_score || 0) * 100).toFixed(0)}%</span>
        </div>
      </div>

      {/* VFX Finals — Innovations */}
      <div className="section-block">
        <h3 className="section-title">VFX FINALS — INNOVATIONS</h3>
        <div className="innovations-grid">
          {(vfx.innovations || []).map((inn, i) => (
            <div key={i} className="innovation-card" style={{ animationDelay: `${i * 0.08}s` }}>
              <span className="inn-icon">◆</span>
              <span>{inn}</span>
            </div>
          ))}
        </div>
        {(vfx.patents || []).length > 0 && (
          <div className="patents-section">
            <h4>PATENTS</h4>
            {vfx.patents.map((p, i) => <div key={i} className="patent-item">{p}</div>)}
          </div>
        )}
        {(vfx.protocols || []).length > 0 && (
          <div className="protocols-section">
            <h4>PROTOCOLS</h4>
            {vfx.protocols.map((p, i) => <div key={i} className="protocol-item">{p}</div>)}
          </div>
        )}
      </div>

      {/* IP Catalog */}
      <IPCatalog ipOutputs={ipOutputs} />
    </div>
  )
}

function DistributionStage({ data }) {
  if (!data) return null
  const narrative = data.narrative?.sections || []
  const cosm = data.cosm || {}
  const ipCatalog = data.ip_catalog || []
  const domeBond = data.dome_bond || null
  const industries = data.industries_changed || []
  const replication = data.replication_kit || {}

  return (
    <div className="stage-content distribution">
      {/* COSM Reveal */}
      <div className="cosm-reveal">
        <CosmRadar dimensions={cosm} size={260} />
        <div className="cosm-total">
          <span className="cosm-total-val">{(cosm.total || Math.min(cosm.rights || 0, cosm.research || 0, cosm.budget || 0, cosm.package || 0, cosm.deliverables || 0, cosm.pitch || 0)).toFixed(1)}</span>
          <span className="cosm-total-label">TOTAL COSM</span>
        </div>
      </div>

      {/* Narrative — The Pitch */}
      <div className="section-block">
        <h3 className="section-title">THE PITCH</h3>
        <div className="narrative-flow">
          {narrative.map((s, i) => <NarrativeSection key={i} section={s} index={i} />)}
        </div>
      </div>

      {/* Dome Bond */}
      <BondTermSheet bond={domeBond} type="dome" />

      {/* IP Catalog */}
      <IPCatalog ipOutputs={ipCatalog} />

      {/* Replication Kit + Industries */}
      <div className="final-grid">
        <div className="section-block">
          <h3 className="section-title">REPLICATION KIT</h3>
          <div className="replication-details">
            <div className="rep-stat">
              <span className="rs-label">Coverage</span>
              <span className="rs-val">{((replication.coverage || 0) * 100).toFixed(0)}%</span>
            </div>
            <div className="rep-stat">
              <span className="rs-label">Coordination</span>
              <span className="rs-val">{replication.coordination_model || '—'}</span>
            </div>
            <div className="rep-stat">
              <span className="rs-label">Est. Savings</span>
              <span className="rs-val">${(replication.estimated_savings || 0).toLocaleString()}/yr</span>
            </div>
            <div className="rep-stat">
              <span className="rs-label">Transferable</span>
              <span className="rs-val">{replication.transferable ? 'YES' : 'NO'}</span>
            </div>
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

  useEffect(() => {
    const fips = '42101'
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

  const stageData = production.stage_data || {}
  const devData = stageData.development
  const preData = stageData.pre_production
  const prodData = stageData.production
  const postData = stageData.post_production
  const distData = stageData.distribution

  const runningCosm = distData?.cosm || null

  return (
    <div className="domes-game">
      {/* Fixed Header */}
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
              <span className="header-cosm-val">{Math.min(runningCosm.rights || 0, runningCosm.research || 0, runningCosm.budget || 0, runningCosm.package || 0, runningCosm.deliverables || 0, runningCosm.pitch || 0).toFixed(0)}</span>
              <span className="header-cosm-label">COSM</span>
            </div>
          )}
        </div>
      </div>

      {/* Stage Hero */}
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

      {/* Content Area */}
      <div className="game-content" ref={contentRef}>
        {lastMessage && (
          <div className="game-message">
            <div className="message-line" />
            <p>{lastMessage}</p>
          </div>
        )}

        {devData && <DevelopmentStage data={devData} />}
        {devData && fragmentData && <ConditionsPanel fragments={fragmentData.fragments} />}
        {devData && domeData && <DomeInstrumentPanel domes={domeData.domes} />}
        {preData && <PreProductionStage data={preData} />}
        {prodData && <ProductionStage data={prodData} />}
        {postData && <PostProductionStage data={postData} />}
        {distData && <DistributionStage data={distData} />}

        {!devData && !isComplete && (
          <div className="empty-stage">
            <div className="empty-icon">◇</div>
            <p>Begin development to acquire rights, research the market, and structure the deal for <strong>{production.subject}</strong>.</p>
          </div>
        )}
      </div>

      {/* Fixed Action Bar */}
      <div className="game-action-bar">
        {!isComplete ? (
          <button className="advance-btn" onClick={handleAdvance} disabled={working}>
            {working ? (
              <>
                <span className="spinner" />
                <span>{currentStage.verb}...</span>
              </>
            ) : (
              <span>{currentStageIndex === 0 && !devData ? 'BEGIN DEVELOPMENT' : `ADVANCE → ${STAGES[Math.min(currentStageIndex + 1, 4)]?.label || 'COMPLETE'}`}</span>
            )}
          </button>
        ) : (
          <div className="complete-bar">
            <span className="complete-icon">◆</span>
            <span>DOME COMPLETE — COSM: {runningCosm ? Math.min(runningCosm.rights || 0, runningCosm.research || 0, runningCosm.budget || 0, runningCosm.package || 0, runningCosm.deliverables || 0, runningCosm.pitch || 0).toFixed(1) : '0'}</span>
          </div>
        )}
      </div>
    </div>
  )
}
