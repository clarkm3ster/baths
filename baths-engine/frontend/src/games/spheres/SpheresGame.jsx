import { useState, useEffect, useRef } from 'react'
import './SpheresGame.css'

const STAGES = [
  { key: 'development', label: 'DEVELOPMENT', num: '01', desc: 'Location scouting, rights & permits, development deal', verb: 'Developing' },
  { key: 'pre_production', label: 'PRE-PRODUCTION', num: '02', desc: 'Design board, budget model, timeline', verb: 'Pre-Producing' },
  { key: 'production', label: 'PRODUCTION', num: '03', desc: 'Build, activate, capture', verb: 'Producing' },
  { key: 'post_production', label: 'POST-PRODUCTION', num: '04', desc: 'Measure impact, document episodes, extract IP', verb: 'Post-Producing' },
  { key: 'distribution', label: 'DISTRIBUTION', num: '05', desc: 'CHRON reveal, Chron Bond, replication kit', verb: 'Distributing' },
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

// ── CHRON Rings Visualization ─────────────────────────────────────────
function ChronRings({ dimensions, size = 220 }) {
  const dims = [
    { key: 'unlock', label: 'UNLOCK', color: '#ff6d00', max: 50000 },
    { key: 'access', label: 'ACCESS', color: '#ff9100', max: 15000 },
    { key: 'permanence', label: 'PERM', color: '#ffab00', max: 1 },
    { key: 'catalyst', label: 'CATAL', color: '#ffd600', max: 1 },
    { key: 'policy', label: 'POLICY', color: '#aeea00', max: 1 },
  ]

  const cx = size / 2, cy = size / 2
  const ringWidth = 8, ringGap = 4
  const total = dimensions?.total || 0

  return (
    <svg viewBox={`0 0 ${size} ${size}`} className="chron-rings">
      {dims.map((d, i) => {
        const r = (size / 2) - 20 - i * (ringWidth + ringGap)
        const val = dimensions ? (dimensions[d.key] || 0) : 0
        const pct = Math.min(1, val / d.max)
        const circumference = 2 * Math.PI * r
        const dashLength = circumference * pct

        return (
          <g key={d.key}>
            <circle cx={cx} cy={cy} r={r} fill="none" stroke="rgba(255,255,255,0.04)" strokeWidth={ringWidth} />
            <circle cx={cx} cy={cy} r={r} fill="none" stroke={d.color} strokeWidth={ringWidth}
              strokeDasharray={`${dashLength} ${circumference}`}
              strokeLinecap="round" transform={`rotate(-90 ${cx} ${cy})`}
              className="ring-animate" style={{ animationDelay: `${i * 0.15}s` }}
            />
            <text x={size - 8} y={cy - r + 3} fill={d.color} fontSize="7" fontFamily="Exo 2" textAnchor="end">{d.label}</text>
          </g>
        )
      })}
      <text x={cx} y={cy - 6} textAnchor="middle" fill="var(--spheres-primary)" fontSize="20" fontFamily="Orbitron" fontWeight="700">
        {total.toFixed(0)}
      </text>
      <text x={cx} y={cy + 10} textAnchor="middle" fill="var(--text-dim)" fontSize="7" fontFamily="Exo 2">CHRON</text>
    </svg>
  )
}

// ── Parcel Card ───────────────────────────────────────────────────────
function ParcelCard({ parcel }) {
  if (!parcel) return null
  const zoning = parcel.zoning_info || {}
  const extra = parcel.extra || {}

  return (
    <div className="parcel-card">
      <div className="parcel-header">
        <div className="parcel-address">{parcel.address}</div>
        <div className={`parcel-status ${parcel.vacant ? 'vacant' : 'improved'}`}>
          {parcel.vacant ? 'VACANT' : 'IMPROVED'}
        </div>
      </div>

      <div className="parcel-stats">
        <div className="parcel-stat">
          <span className="pstat-val">{(parcel.land_area_sqft || 0).toLocaleString()}</span>
          <span className="pstat-label">sqft</span>
        </div>
        <div className="parcel-stat">
          <span className="pstat-val">{parcel.zoning}</span>
          <span className="pstat-label">zoning</span>
        </div>
        <div className="parcel-stat">
          <span className="pstat-val">${(parcel.total_val || 0).toLocaleString()}</span>
          <span className="pstat-label">assessed</span>
        </div>
        <div className="parcel-stat">
          <span className="pstat-val">{parcel.neighborhood || '—'}</span>
          <span className="pstat-label">neighborhood</span>
        </div>
      </div>

      <div className="parcel-details">
        <div className="parcel-detail-row">
          <span className="pd-key">Owner</span>
          <span className="pd-val">{parcel.owner || 'Unknown'}</span>
        </div>
        <div className="parcel-detail-row">
          <span className="pd-key">Zoning</span>
          <span className="pd-val">{zoning.name || parcel.zoning} — {zoning.description || ''}</span>
        </div>
        {zoning.max_height_ft > 0 && (
          <div className="parcel-detail-row">
            <span className="pd-key">Max Height</span>
            <span className="pd-val">{zoning.max_height_ft} ft</span>
          </div>
        )}
        <div className="parcel-detail-row">
          <span className="pd-key">Council District</span>
          <span className="pd-val">{parcel.council_district || '—'}</span>
        </div>
        {parcel.lat && parcel.lon && (
          <div className="parcel-detail-row">
            <span className="pd-key">Coordinates</span>
            <span className="pd-val">{parcel.lat.toFixed(4)}, {parcel.lon.toFixed(4)}</span>
          </div>
        )}
        {extra.opportunity_zone && <div className="parcel-flag">Opportunity Zone</div>}
        {extra.land_bank && <div className="parcel-flag">Land Bank</div>}
        {extra.near_transit && <div className="parcel-flag">Near Transit</div>}
        {extra.historic && <div className="parcel-flag">Historic</div>}
      </div>
    </div>
  )
}

// ── Nearby Parcels ────────────────────────────────────────────────────
function NearbyParcels({ parcels }) {
  if (!parcels || parcels.length === 0) return null
  return (
    <div className="nearby-parcels">
      <h4>{parcels.length} NEARBY PARCELS</h4>
      <div className="nearby-grid">
        {parcels.map((p, i) => (
          <div key={i} className={`nearby-item ${p.vacant ? 'vacant' : ''}`}>
            <div className="nearby-addr">{p.address}</div>
            <div className="nearby-meta">
              <span>{p.zoning}</span>
              <span>${(p.total_val || 0).toLocaleString()}</span>
              {p.vacant && <span className="vacant-tag">vacant</span>}
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

// ── Cost Tier Selector ────────────────────────────────────────────────
function CostTiers({ cost }) {
  if (!cost) return null
  const tiers = [
    { key: 'light_activation', label: 'LIGHT', icon: '○' },
    { key: 'moderate_activation', label: 'MODERATE', icon: '◎' },
    { key: 'full_buildout', label: 'FULL', icon: '●' },
  ]
  const recommended = cost.recommended || 'moderate_activation'

  return (
    <div className="cost-tiers">
      {tiers.map(tier => {
        const data = cost[tier.key] || {}
        const isRec = tier.key === recommended
        return (
          <div key={tier.key} className={`cost-tier ${isRec ? 'recommended' : ''}`}>
            {isRec && <div className="rec-badge">RECOMMENDED</div>}
            <div className="tier-icon">{tier.icon}</div>
            <div className="tier-label">{tier.label}</div>
            <div className="tier-total">${(data.total || 0).toLocaleString()}</div>
            <div className="tier-persqft">${data.per_sqft || 0}/sqft</div>
            <div className="tier-includes">{data.includes}</div>
          </div>
        )
      })}
    </div>
  )
}

// ── Timeline ──────────────────────────────────────────────────────────
function Timeline({ timeline }) {
  if (!timeline) return null
  const phases = timeline.phases || []
  const totalWeeks = timeline.total_weeks || 1

  return (
    <div className="timeline">
      <div className="timeline-header">
        <span>PROJECT TIMELINE</span>
        <span className="timeline-total">{timeline.duration_years} years ({totalWeeks} weeks)</span>
      </div>
      <div className="timeline-bar">
        {phases.map((phase, i) => {
          const widthPct = (phase.weeks / totalWeeks) * 100
          const colors = ['#ff6d00', '#ff9100', '#ffab00', '#ffd600', '#aeea00', '#00e676']
          return (
            <div key={i} className="timeline-segment" style={{ width: `${widthPct}%`, background: colors[i % colors.length] + '30', borderColor: colors[i % colors.length] }}>
              <div className="seg-label">{phase.name}</div>
              <div className="seg-weeks">{phase.weeks}w</div>
            </div>
          )
        })}
      </div>
    </div>
  )
}

// ── Impact Episode ────────────────────────────────────────────────────
function EpisodeCard({ episode, index }) {
  return (
    <div className="episode-card" style={{ animationDelay: `${index * 0.12}s` }}>
      <div className="episode-date">{episode.date}</div>
      <div className="episode-content">
        <h4>{episode.title}</h4>
        <p>{episode.impact}</p>
        {episode.metrics && (
          <div className="episode-metrics">
            {Object.entries(episode.metrics).map(([k, v]) => (
              <span key={k} className="ep-metric">
                <strong>{typeof v === 'number' ? v.toLocaleString() : v}</strong>
                <span>{k.replace(/_/g, ' ')}</span>
              </span>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

// ── Permit Card ───────────────────────────────────────────────────────
function PermitCard({ permit, index }) {
  const statusColor = {
    approved: '#00e676', required: '#ffab00', conditional: '#ff9100',
    waived: '#8090a8', issued: '#00e676',
  }
  return (
    <div className="permit-card" style={{ animationDelay: `${index * 0.06}s` }}>
      <div className="permit-status" style={{ color: statusColor[permit.status] || '#8090a8' }}>
        {permit.status?.toUpperCase()}
      </div>
      <div className="permit-type">{permit.type}</div>
      {permit.description && <div className="permit-desc">{permit.description}</div>}
    </div>
  )
}

// ── Neighborhood Context from Fragments ──────────────────────────────
function NeighborhoodContext({ fragments }) {
  if (!fragments || Object.keys(fragments).length === 0) return null

  const get = (source, key) => fragments[source]?.data?.[key]
  const pct = v => v != null ? `${v.toFixed(1)}%` : '—'
  const money = v => v != null ? `$${v.toLocaleString()}` : '—'
  const num = v => v != null ? v.toLocaleString() : '—'

  const countyName = Object.values(fragments)[0]?.county_name || 'Unknown'

  const stats = [
    { label: 'Population', value: num(get('census-demographics', 'total_pop')) },
    { label: 'Median Income', value: money(get('census-income', 'median_household_income')) },
    { label: 'Poverty Rate', value: pct(get('census-income', 'poverty_total') > 0 ? (get('census-income', 'poverty_below') / get('census-income', 'poverty_total')) * 100 : null) },
    { label: 'Median Rent', value: money(get('census-housing', 'median_gross_rent')) },
    { label: 'Vacancy Rate', value: pct(get('census-housing', 'total_units') > 0 ? (get('census-housing', 'vacant_units') / get('census-housing', 'total_units')) * 100 : null) },
    { label: 'Unemployment', value: pct(get('census-employment', 'in_labor_force') > 0 ? (get('census-employment', 'civilian_unemployed') / get('census-employment', 'in_labor_force')) * 100 : null) },
    { label: 'No Vehicle', value: pct(get('census-commute', 'workers_total') > 0 ? (get('census-commute', 'no_vehicle') / get('census-commute', 'workers_total')) * 100 : null) },
    { label: 'Broadband', value: pct(get('census-internet', 'total_households_internet') > 0 ? (get('census-internet', 'broadband') / get('census-internet', 'total_households_internet')) * 100 : null) },
  ]

  return (
    <div className="section-block neighborhood-context">
      <h3 className="section-title">NEIGHBORHOOD DATA</h3>
      <p className="section-subtitle">Real Census data for {countyName} — {Object.keys(fragments).length} fragment sources</p>
      <div className="neighborhood-grid">
        {stats.map((s, i) => (
          <div key={i} className="nb-cell" style={{ animationDelay: `${i * 0.04}s` }}>
            <span className="nb-value">{s.value}</span>
            <span className="nb-label">{s.label}</span>
          </div>
        ))}
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
function BondTermSheet({ bond, type = 'chron' }) {
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
          <span className="bs-val">{bond.chron_score || bond.cosm_score}</span>
          <span className="bs-label">{type === 'chron' ? 'CHRON' : 'COSM'} Score</span>
        </div>
        <div className="bond-stat">
          <span className="bs-val">{bond.sqft_backing?.toLocaleString() || bond.programs_backing}</span>
          <span className="bs-label">{type === 'chron' ? 'Sqft Backing' : 'Programs Backing'}</span>
        </div>
      </div>
    </div>
  )
}

// ── Stage Renderers ───────────────────────────────────────────────────

function DevelopmentStage({ data }) {
  if (!data) return null
  const parcel = data.location_report || {}
  const permits = data.rights_assessment?.permits || []
  const insights = data.location_insights || []
  const nearby = data.nearby_parcels || []

  return (
    <div className="stage-content discover">
      <ParcelCard parcel={parcel} />

      {insights.length > 0 && (
        <div className="section-block">
          <h3 className="section-title">LOCATION INSIGHTS</h3>
          {insights.map((ins, i) => (
            <div key={i} className="insight-item">
              <div className="insight-score">{((ins.activation_score || 0) * 100).toFixed(0)}%</div>
              <div>
                <p>{ins.description}</p>
                {ins.activation_types?.length > 0 && (
                  <div className="insight-types">
                    {ins.activation_types.map((t, j) => <span key={j} className="act-tag">{t.replace(/_/g, ' ')}</span>)}
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      )}

      <div className="section-block">
        <h3 className="section-title">RIGHTS ASSESSMENT — PERMITS</h3>
        <div className="permits-list">
          {permits.map((p, i) => <PermitCard key={i} permit={p} index={i} />)}
        </div>
      </div>

      <NearbyParcels parcels={nearby} />
    </div>
  )
}

function PreProductionStage({ data }) {
  if (!data) return null
  const design = data.design_board || {}
  const cost = data.budget_model || {}
  const timeline = data.timeline || {}
  const zoning = data.zoning_info || {}

  return (
    <div className="stage-content design">
      <div className="design-banner">
        <h3>{design.name || 'Sphere Activation'}</h3>
        <div className="design-types">
          {(design.activation_types || []).map((t, i) => (
            <span key={i} className="act-tag large">{t.replace(/_/g, ' ')}</span>
          ))}
        </div>
        {design.features?.length > 0 && (
          <div className="design-features">
            {design.features.map((f, i) => <span key={i} className="feature-tag">{f}</span>)}
          </div>
        )}
      </div>

      <div className="section-block">
        <h3 className="section-title">BUDGET MODEL — INVESTMENT TIERS</h3>
        <CostTiers cost={cost} />
      </div>

      <div className="section-block">
        <Timeline timeline={timeline} />
      </div>
    </div>
  )
}

function ProductionStage({ data }) {
  if (!data) return null
  const buildReport = data.build_report || {}
  const activation = data.activation_log || {}
  const executedPermits = buildReport.permits || []
  const policyChanges = buildReport.policy_changes || []

  return (
    <div className="stage-content build">
      <div className="activation-banner">
        <div className="act-icon">&#9673;</div>
        <h3>SPHERE ACTIVATED</h3>
        <div className="act-stats">
          <span><strong>{(activation.sqft_activated || 0).toLocaleString()}</strong> sqft</span>
          <span><strong>{activation.events_capacity || 0}</strong> capacity</span>
          <span><strong>${(activation.investment || 0).toLocaleString()}</strong> invested</span>
        </div>
      </div>

      <div className="section-block">
        <h3 className="section-title">PERMITS EXECUTED</h3>
        <div className="permits-list">
          {executedPermits.map((p, i) => <PermitCard key={i} permit={p} index={i} />)}
        </div>
      </div>

      <div className="section-block">
        <h3 className="section-title">POLICY CHANGES ENABLED</h3>
        <div className="policy-list">
          {policyChanges.map((p, i) => (
            <div key={i} className="policy-item">
              <span className="policy-arrow">→</span>
              <span>{p}</span>
            </div>
          ))}
        </div>
      </div>

      {activation.features_installed?.length > 0 && (
        <div className="section-block">
          <h3 className="section-title">FEATURES INSTALLED</h3>
          <div className="installed-features">
            {activation.features_installed.map((f, i) => <span key={i} className="feature-tag installed">{f}</span>)}
          </div>
        </div>
      )}
    </div>
  )
}

function PostProductionStage({ data }) {
  if (!data) return null
  const episodes = data.episode_timeline || []
  const metrics = data.impact_dashboard || {}
  const innovations = data.innovation_portfolio || {}
  const ipOutputs = data.ip_outputs || []

  return (
    <div className="stage-content measure">
      <div className="metrics-banner">
        <div className="metric-big">
          <span className="mb-val">{(metrics.total_visitors || 0).toLocaleString()}</span>
          <span className="mb-label">total visitors</span>
        </div>
        <div className="metric-big">
          <span className="mb-val">${(metrics.economic_impact || 0).toLocaleString()}</span>
          <span className="mb-label">economic impact</span>
        </div>
        <div className="metric-big">
          <span className="mb-val">{metrics.jobs_created || 0}</span>
          <span className="mb-label">jobs created</span>
        </div>
        <div className="metric-big">
          <span className="mb-val">{metrics.community_rating || 0}</span>
          <span className="mb-label">community rating</span>
        </div>
        <div className="metric-big">
          <span className="mb-val">{metrics.property_value_impact_pct || 0}%</span>
          <span className="mb-label">property value impact</span>
        </div>
      </div>

      <div className="section-block">
        <h3 className="section-title">IMPACT TIMELINE</h3>
        <div className="episodes-list">
          {episodes.map((ep, i) => <EpisodeCard key={i} episode={ep} index={i} />)}
        </div>
      </div>

      <div className="section-block">
        <h3 className="section-title">INNOVATIONS</h3>
        <div className="innovations-list">
          {(innovations.innovations || []).map((inn, i) => (
            <div key={i} className="inn-item"><span className="inn-dot">&#9670;</span>{inn}</div>
          ))}
        </div>
        {(innovations.protocols || []).length > 0 && (
          <div className="protocols-list">
            <h4>PROTOCOLS</h4>
            {innovations.protocols.map((p, i) => (
              <div key={i} className="protocol-item">{p}</div>
            ))}
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
  const chron = data.chron || {}
  const metrics = data.impact_dashboard || {}
  const chronBond = data.chron_bond || null
  const ipCatalog = data.ip_catalog || []
  const replication = data.replication_kit || {}
  const innovations = data.innovations || []

  return (
    <div className="stage-content completion">
      {/* CHRON Reveal */}
      <div className="chron-reveal">
        <ChronRings dimensions={chron} size={240} />
        <div className="chron-total">
          <span className="chron-total-val">{(chron.total || 0).toFixed(1)}</span>
          <span className="chron-total-label">TOTAL CHRON</span>
        </div>
      </div>

      <div className="chron-breakdown">
        {[
          { key: 'unlock', label: 'Unlock (sqft)', val: chron.unlock },
          { key: 'access', label: 'Access (hours)', val: chron.access },
          { key: 'permanence', label: 'Permanence', val: chron.permanence },
          { key: 'catalyst', label: 'Catalyst', val: chron.catalyst },
          { key: 'policy', label: 'Policy', val: chron.policy },
        ].map(d => (
          <div key={d.key} className="chron-dim-row">
            <span className="cdr-label">{d.label}</span>
            <span className="cdr-val">{typeof d.val === 'number' ? d.val.toLocaleString() : '—'}</span>
          </div>
        ))}
      </div>

      {/* Chron Bond */}
      <BondTermSheet bond={chronBond} type="chron" />

      {/* IP Catalog */}
      <IPCatalog ipOutputs={ipCatalog} />

      {/* Replication Kit */}
      <div className="section-block">
        <h3 className="section-title">REPLICATION KIT</h3>
        <div className="replication-details">
          <div className="rep-stat">
            <span className="rs-label">Parcel Type</span>
            <span className="rs-val">{replication.parcel_type || '—'}</span>
          </div>
          <div className="rep-stat">
            <span className="rs-label">Zoning</span>
            <span className="rs-val">{replication.zoning || '—'}</span>
          </div>
          <div className="rep-stat">
            <span className="rs-label">Budget Tier</span>
            <span className="rs-val">{replication.budget_tier?.replace(/_/g, ' ') || '—'}</span>
          </div>
          <div className="rep-stat">
            <span className="rs-label">Transferable</span>
            <span className="rs-val">{replication.transferable ? 'YES' : 'NO'}</span>
          </div>
        </div>
      </div>

      {innovations.length > 0 && (
        <div className="section-block">
          <h3 className="section-title">INNOVATIONS PORTFOLIO</h3>
          <div className="innovations-list">
            {innovations.map((inn, i) => (
              <div key={i} className="inn-item"><span className="inn-dot">&#9670;</span>{inn}</div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

// ══════════════════════════════════════════════════════════════════════
// MAIN SPHERES GAME COMPONENT
// ══════════════════════════════════════════════════════════════════════

export default function SpheresGame({ player, production, onUpdate, onBack }) {
  const [working, setWorking] = useState(false)
  const [lastMessage, setLastMessage] = useState(null)
  const [fragmentData, setFragmentData] = useState(null)
  const contentRef = useRef(null)

  useEffect(() => {
    fetch('/api/fragment/county/42101')
      .then(r => r.json())
      .then(d => { if (d.fragment_count > 0) setFragmentData(d) })
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
  const runningChron = distData?.chron || null

  return (
    <div className="spheres-game">
      {/* Fixed Header */}
      <div className="game-header spheres">
        <div className="game-header-left">
          <button className="back-btn" onClick={onBack}>← GAMES</button>
          <div className="game-badge spheres">SPHERES</div>
          <div className="game-subject">{production.subject}</div>
        </div>
        <div className="game-header-center">
          <div className="stage-track-mini spheres">
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
          {runningChron && (
            <div className="header-chron">
              <span className="header-chron-val">{(runningChron.total || 0).toFixed(0)}</span>
              <span className="header-chron-label">CHRON</span>
            </div>
          )}
        </div>
      </div>

      {/* Stage Hero */}
      <div className="stage-hero spheres">
        <div className="stage-hero-bg spheres" />
        <div className="stage-hero-content">
          <div className="stage-num spheres">{currentStage.num}</div>
          <div className="stage-info">
            <h2 className="spheres">{currentStage.label}</h2>
            <p>{currentStage.desc}</p>
          </div>
          <div className="stage-progress-ring spheres">
            <svg viewBox="0 0 60 60">
              <circle cx="30" cy="30" r="26" fill="none" stroke="rgba(255,255,255,0.06)" strokeWidth="3" />
              <circle cx="30" cy="30" r="26" fill="none" stroke="var(--spheres-primary)" strokeWidth="3"
                strokeDasharray={`${production.progress * 1.634} 163.4`}
                strokeLinecap="round" transform="rotate(-90 30 30)" />
            </svg>
            <span className="progress-pct spheres">{production.progress.toFixed(0)}%</span>
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="game-content" ref={contentRef}>
        {lastMessage && (
          <div className="game-message spheres">
            <p>{lastMessage}</p>
          </div>
        )}

        {devData && <DevelopmentStage data={devData} />}
        {devData && fragmentData && <NeighborhoodContext fragments={fragmentData.fragments} />}
        {preData && <PreProductionStage data={preData} />}
        {prodData && <ProductionStage data={prodData} />}
        {postData && <PostProductionStage data={postData} />}
        {distData && <DistributionStage data={distData} />}

        {!devData && !isComplete && (
          <div className="empty-stage spheres">
            <div className="empty-icon">&#9673;</div>
            <p>Begin development to scout the location, assess rights, and structure the deal for <strong>{production.subject}</strong>.</p>
          </div>
        )}
      </div>

      {/* Action Bar */}
      <div className="game-action-bar spheres">
        {!isComplete ? (
          <button className="advance-btn spheres" onClick={handleAdvance} disabled={working}>
            {working ? (
              <><span className="spinner spheres" /><span>{currentStage.verb}...</span></>
            ) : (
              <span>{currentStageIndex === 0 && !devData ? 'BEGIN DEVELOPMENT' : `ADVANCE → ${STAGES[Math.min(currentStageIndex + 1, 4)]?.label || 'COMPLETE'}`}</span>
            )}
          </button>
        ) : (
          <div className="complete-bar spheres">
            <span className="complete-icon">&#9673;</span>
            <span>SPHERE COMPLETE — CHRON: {(runningChron?.total || 0).toFixed(1)}</span>
          </div>
        )}
      </div>
    </div>
  )
}
