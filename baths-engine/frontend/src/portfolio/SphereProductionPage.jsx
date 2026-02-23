import { useState, useEffect } from 'react'
import { useParams, Link } from 'react-router-dom'
import './SpheresPortfolio.css'

const IP_DOMAIN_LABELS = {
  entertainment: 'Entertainment IP',
  technology: 'Technology IP',
  financial_product: 'Financial Product IP',
  policy: 'Policy IP',
  product: 'Product IP',
  research: 'Research IP',
  housing: 'Housing IP',
  healthcare: 'Healthcare IP',
  urban_design: 'Urban Design IP',
  real_estate: 'Real Estate IP',
}

const STAGES = [
  { key: 'development', label: 'Development', num: '01' },
  { key: 'pre_production', label: 'Pre-Production', num: '02' },
  { key: 'production', label: 'Production', num: '03' },
  { key: 'post_production', label: 'Post-Production', num: '04' },
  { key: 'distribution', label: 'Distribution', num: '05' },
]

// ── CHRON Rings ────────────────────────────────────────────────────
function ChronRings({ dimensions, size = 260 }) {
  const dims = [
    { key: 'unlock', label: 'UNLOCK', color: '#ff6d00', max: 50000 },
    { key: 'access', label: 'ACCESS', color: '#ff9100', max: 15000 },
    { key: 'permanence', label: 'PERM', color: '#ffab00', max: 1 },
    { key: 'catalyst', label: 'CATAL', color: '#ffd600', max: 1 },
    { key: 'policy', label: 'POLICY', color: '#aeea00', max: 1 },
  ]
  const cx = size / 2, cy = size / 2
  const ringWidth = 8, ringGap = 5
  const total = dimensions?.total || 0

  return (
    <svg viewBox={`0 0 ${size} ${size}`} className="sp-chron-radar">
      {dims.map((d, i) => {
        const r = (size / 2) - 20 - i * (ringWidth + ringGap)
        const val = dimensions ? (dimensions[d.key] || 0) : 0
        const pct = Math.min(1, val / d.max)
        const circumference = 2 * Math.PI * r
        const dashLength = circumference * pct
        return (
          <g key={d.key}>
            <circle cx={cx} cy={cy} r={r} fill="none" stroke="rgba(255,255,255,0.06)" strokeWidth={ringWidth} />
            <circle cx={cx} cy={cy} r={r} fill="none" stroke={d.color} strokeWidth={ringWidth}
              strokeDasharray={`${dashLength} ${circumference}`}
              strokeLinecap="round" transform={`rotate(-90 ${cx} ${cy})`}
            />
            <text x={size - 8} y={cy - r + 3} fill={d.color} fontSize="7" fontFamily="Inter, sans-serif"
              textAnchor="end" letterSpacing="0.08em">{d.label}</text>
          </g>
        )
      })}
      <text x={cx} y={cy - 4} textAnchor="middle" fill="#fff" fontSize="26" fontWeight="700" fontFamily="Inter, sans-serif">
        {total.toFixed(0)}
      </text>
      <text x={cx} y={cy + 14} textAnchor="middle" fill="rgba(255,255,255,0.4)" fontSize="8"
        fontFamily="Inter, sans-serif" letterSpacing="0.2em">CHRON</text>
    </svg>
  )
}

// ── Production Timeline ────────────────────────────────────────────
function ProductionTimeline({ stageData, deliverableLinks }) {
  const [expanded, setExpanded] = useState(null)

  return (
    <div className="sp-timeline">
      {STAGES.map((stage, i) => {
        const data = stageData?.[stage.key]
        const isExpanded = expanded === stage.key
        const hasData = !!data
        const stageDeliverables = deliverableLinks?.[stage.key] || {}

        return (
          <div key={stage.key} className={`sp-tl-stage ${hasData ? 'completed' : 'pending'} ${isExpanded ? 'expanded' : ''}`}>
            <button className="sp-tl-header" onClick={() => setExpanded(isExpanded ? null : stage.key)} disabled={!hasData}>
              <div className="sp-tl-marker">
                <span className="sp-tl-num">{stage.num}</span>
                <div className={`sp-tl-dot ${hasData ? 'filled' : ''}`} />
              </div>
              <span className="sp-tl-label">{stage.label}</span>
              {hasData && <span className="sp-tl-toggle">{isExpanded ? '\u2212' : '+'}</span>}
            </button>
            {i < STAGES.length - 1 && <div className={`sp-tl-line ${hasData ? 'filled' : ''}`} />}
            {isExpanded && hasData && (
              <div className="sp-tl-detail">
                <StageDetail stage={stage.key} data={data} stageData={stageData} />
                {Object.keys(stageDeliverables).length > 0 && (
                  <div className="sp-tl-files">
                    <h4>Deliverables</h4>
                    {Object.entries(stageDeliverables).map(([name, url]) => (
                      <a key={name} href={url} className="sp-file-link" download>
                        <span className="sp-file-icon">{name.endsWith('.json') ? '\u25A0' : '\u25A1'}</span>
                        {name}
                      </a>
                    ))}
                  </div>
                )}
              </div>
            )}
          </div>
        )
      })}
    </div>
  )
}

function StageDetail({ stage, data, stageData }) {
  if (stage === 'development') {
    const parcel = data.location_report || {}
    const permits = data.rights_assessment?.permits || []
    return (
      <div className="sp-stage-detail">
        <div className="sp-sd-row">
          <span className="sp-sd-metric">{parcel.address || 'N/A'}</span>
          <span className="sp-sd-label">parcel address &mdash; {parcel.neighborhood || ''}</span>
        </div>
        <div className="sp-sd-row">
          <span className="sp-sd-metric">{(parcel.land_area_sqft || 0).toLocaleString()} sqft</span>
          <span className="sp-sd-label">land area &mdash; zoning {parcel.zoning || 'N/A'}</span>
        </div>
        <div className="sp-sd-row">
          <span className="sp-sd-metric">{permits.length}</span>
          <span className="sp-sd-label">permits assessed</span>
        </div>
        <div className="sp-sd-row">
          <span className="sp-sd-metric">${(parcel.total_val || 0).toLocaleString()}</span>
          <span className="sp-sd-label">assessed value</span>
        </div>
        <div className="sp-sd-sources">
          <h5>Sources</h5>
          <ul>
            <li>Philadelphia Office of Property Assessment (OPA)</li>
            <li>Philadelphia City Planning Commission (zoning)</li>
            <li>OpenDataPhilly (parcel boundaries)</li>
          </ul>
        </div>
      </div>
    )
  }
  if (stage === 'pre_production') {
    const design = data.design_board || {}
    const budget = data.budget_model || {}
    const timeline = data.timeline || {}
    return (
      <div className="sp-stage-detail">
        <div className="sp-sd-row">
          <span className="sp-sd-metric">{(design.activation_types || []).length}</span>
          <span className="sp-sd-label">activation types &mdash; {(design.activation_types || []).join(', ').replace(/_/g, ' ')}</span>
        </div>
        <div className="sp-sd-row">
          <span className="sp-sd-metric">${(budget.recommended_total || 0).toLocaleString()}</span>
          <span className="sp-sd-label">recommended budget ({(budget.recommended || '').replace(/_/g, ' ')})</span>
        </div>
        <div className="sp-sd-row">
          <span className="sp-sd-metric">{timeline.total_weeks || 0} weeks</span>
          <span className="sp-sd-label">project timeline ({timeline.duration_years || 0} years)</span>
        </div>
      </div>
    )
  }
  if (stage === 'production') {
    const activation = data.activation_log || {}
    const buildReport = data.build_report || {}
    return (
      <div className="sp-stage-detail">
        <div className="sp-sd-row">
          <span className="sp-sd-metric">{(activation.sqft_activated || 0).toLocaleString()} sqft</span>
          <span className="sp-sd-label">area activated</span>
        </div>
        <div className="sp-sd-row">
          <span className="sp-sd-metric">${(activation.investment || 0).toLocaleString()}</span>
          <span className="sp-sd-label">total investment</span>
        </div>
        <div className="sp-sd-row">
          <span className="sp-sd-metric">{(buildReport.policy_changes || []).length}</span>
          <span className="sp-sd-label">policy changes enabled</span>
        </div>
      </div>
    )
  }
  if (stage === 'post_production') {
    const impact = data.impact_dashboard || {}
    const episodes = data.episode_timeline || []
    const ipOutputs = data.ip_outputs || []
    return (
      <div className="sp-stage-detail">
        <div className="sp-sd-row">
          <span className="sp-sd-metric">{(impact.total_visitors || 0).toLocaleString()}</span>
          <span className="sp-sd-label">total visitors</span>
        </div>
        <div className="sp-sd-row">
          <span className="sp-sd-metric">${(impact.economic_impact || 0).toLocaleString()}</span>
          <span className="sp-sd-label">economic impact</span>
        </div>
        <div className="sp-sd-row">
          <span className="sp-sd-metric">{impact.jobs_created || 0}</span>
          <span className="sp-sd-label">jobs created</span>
        </div>
        <div className="sp-sd-row">
          <span className="sp-sd-metric">{episodes.length}</span>
          <span className="sp-sd-label">documentary episodes captured</span>
        </div>
        <div className="sp-sd-row">
          <span className="sp-sd-metric">{ipOutputs.length}</span>
          <span className="sp-sd-label">IP outputs generated</span>
        </div>
      </div>
    )
  }
  if (stage === 'distribution') {
    const chron = data.chron || {}
    const bond = data.chron_bond || {}
    const base = (chron.unlock || 0) * (chron.access || 0)
    const sig = ((chron.permanence || 0) + (chron.catalyst || 0) + (chron.policy || 0)) / 3
    return (
      <div className="sp-stage-detail">
        <div className="sp-sd-row">
          <span className="sp-sd-metric">{(base * (1 + sig)).toFixed(0)}</span>
          <span className="sp-sd-label">final CHRON score (m&sup2; x time x significance)</span>
        </div>
        <div className="sp-sd-row">
          <span className="sp-sd-metric">${(bond.face_value || 0).toLocaleString()}</span>
          <span className="sp-sd-label">Chron Bond face value &mdash; {bond.rating || 'N/A'} rated</span>
        </div>
      </div>
    )
  }
  return null
}

// ── IP Portfolio Section ───────────────────────────────────────────
function IPPortfolio({ ipCatalog }) {
  if (!ipCatalog || ipCatalog.length === 0) return null

  const byDomain = {}
  ipCatalog.forEach(ip => {
    const d = ip.domain
    if (!byDomain[d]) byDomain[d] = []
    byDomain[d].push(ip)
  })

  const domainColors = {
    entertainment: '#ff4081', technology: '#7c4dff', financial_product: '#00e676',
    policy: '#ffab00', product: '#00e5ff', research: '#448aff',
    housing: '#ff6d00', healthcare: '#e040fb', urban_design: '#76ff03', real_estate: '#ffd600',
  }

  return (
    <section className="sp-section">
      <h2 className="sp-section-title">Intellectual Property Portfolio</h2>
      <p className="sp-section-sub">{ipCatalog.length} outputs across {Object.keys(byDomain).length} domains</p>
      <div className="sp-ip-grid">
        {Object.entries(byDomain).map(([domain, items]) => (
          <div key={domain} className="sp-ip-domain" style={{ borderColor: domainColors[domain] || '#555' }}>
            <h3 className="sp-ip-domain-name" style={{ color: domainColors[domain] || '#aaa' }}>
              {IP_DOMAIN_LABELS[domain] || domain}
            </h3>
            {items.map((ip, j) => (
              <div key={j} className="sp-ip-item">
                <div className="sp-ip-title">{ip.title}</div>
                <p className="sp-ip-desc">{ip.description}</p>
                <div className="sp-ip-meta">
                  <span>{ip.format?.replace(/_/g, ' ')}</span>
                  <span className="sp-ip-stage">Stage: {ip.stage_originated?.replace(/_/g, ' ')}</span>
                </div>
                {ip.value_driver && <div className="sp-ip-driver">{ip.value_driver}</div>}
              </div>
            ))}
          </div>
        ))}
      </div>
    </section>
  )
}

// ── Bond Term Sheet ────────────────────────────────────────────────
function BondSection({ bond }) {
  if (!bond || !bond.face_value) return null
  const ratingColors = { AAA: '#00e676', AA: '#69f0ae', A: '#b2ff59', BBB: '#ffab00', BB: '#ff9100', B: '#ff6d00' }
  return (
    <div className="sp-bond">
      <div className="sp-bond-header">
        <span className="sp-bond-type">Chron Bond</span>
        <span className="sp-bond-rating" style={{ color: ratingColors[bond.rating] || '#888' }}>{bond.rating}</span>
      </div>
      <div className="sp-bond-id">{bond.bond_id}</div>
      <div className="sp-bond-grid">
        <div className="sp-bond-stat primary">
          <span className="sp-bs-val">${bond.face_value?.toLocaleString()}</span>
          <span className="sp-bs-label">Face Value</span>
        </div>
        <div className="sp-bond-stat">
          <span className="sp-bs-val">{bond.coupon_rate}%</span>
          <span className="sp-bs-label">Coupon Rate</span>
        </div>
        <div className="sp-bond-stat">
          <span className="sp-bs-val">{bond.maturity_years} yr</span>
          <span className="sp-bs-label">Maturity</span>
        </div>
        <div className="sp-bond-stat">
          <span className="sp-bs-val">{bond.yield_to_maturity}%</span>
          <span className="sp-bs-label">Yield to Maturity</span>
        </div>
        <div className="sp-bond-stat">
          <span className="sp-bs-val">{bond.chron_score}</span>
          <span className="sp-bs-label">CHRON Score</span>
        </div>
        <div className="sp-bond-stat">
          <span className="sp-bs-val">{bond.sqft_backing?.toLocaleString()}</span>
          <span className="sp-bs-label">Sqft Backing</span>
        </div>
      </div>
    </div>
  )
}

// ── Data Transparency ──────────────────────────────────────────────
function DataTransparency({ stageData, impact }) {
  const dev = stageData?.development || {}
  const pre = stageData?.pre_production || {}
  const parcel = dev.location_report || {}
  const budget = pre.budget_model || {}

  return (
    <section className="sp-section">
      <h2 className="sp-section-title">Data Transparency</h2>
      <p className="sp-section-sub">Every data point sourced from public databases.</p>

      <div className="sp-data-grid">
        <div className="sp-data-card">
          <div className="sp-dc-val">{(parcel.land_area_sqft || 0).toLocaleString()}</div>
          <div className="sp-dc-label">Square Feet</div>
          <div className="sp-dc-source">Philadelphia OPA</div>
        </div>
        <div className="sp-data-card">
          <div className="sp-dc-val">${(parcel.total_val || 0).toLocaleString()}</div>
          <div className="sp-dc-label">Assessed Value</div>
          <div className="sp-dc-source">Philadelphia OPA</div>
        </div>
        <div className="sp-data-card">
          <div className="sp-dc-val">${(budget.recommended_total || 0).toLocaleString()}</div>
          <div className="sp-dc-label">Investment</div>
          <div className="sp-dc-source">NRPA benchmarks</div>
        </div>
        <div className="sp-data-card">
          <div className="sp-dc-val">${(impact?.economic_impact || 0).toLocaleString()}</div>
          <div className="sp-dc-label">Economic Impact</div>
          <div className="sp-dc-source">3.2x NRPA multiplier</div>
        </div>
        <div className="sp-data-card">
          <div className="sp-dc-val">+{impact?.property_value_impact_pct || 0}%</div>
          <div className="sp-dc-label">Property Value Impact</div>
          <div className="sp-dc-source">Adjacent parcels estimate</div>
        </div>
      </div>

      <div className="sp-sources-list">
        <h3>Data Sources</h3>
        <ul>
          <li><strong>Philadelphia OPA</strong> &mdash; Office of Property Assessment <span className="sp-src-url">property.phila.gov</span></li>
          <li><strong>OpenDataPhilly</strong> &mdash; Open data portal <span className="sp-src-url">opendataphilly.org</span></li>
          <li><strong>Philadelphia Zoning Code</strong> &mdash; City Planning Commission</li>
          <li><strong>NRPA</strong> &mdash; National Recreation and Park Association benchmarks</li>
          <li><strong>Census ACS</strong> &mdash; American Community Survey <span className="sp-src-url">census.gov</span></li>
          <li><strong>Philadelphia Commerce Dept</strong> &mdash; Economic impact data</li>
        </ul>
      </div>
    </section>
  )
}

// ══════════════════════════════════════════════════════════════════
// MAIN SPHERE PRODUCTION PAGE
// ══════════════════════════════════════════════════════════════════

export default function SphereProductionPage() {
  const { id } = useParams()
  const [production, setProduction] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetch(`/api/portfolio/productions/${id}`)
      .then(r => {
        if (!r.ok) throw new Error('Not found')
        return r.json()
      })
      .then(data => {
        setProduction(data)
        setLoading(false)
      })
      .catch(() => setLoading(false))
  }, [id])

  if (loading) {
    return (
      <div className="sp-page">
        <div className="sp-loading">
          <div className="sp-loading-mark">SPHERES</div>
          <div className="sp-loading-line" />
        </div>
      </div>
    )
  }

  if (!production) {
    return (
      <div className="sp-page">
        <div className="sp-empty">
          <p>Production not found.</p>
          <Link to="/spheres" className="sp-back-link">&larr; Back to all spheres</Link>
        </div>
      </div>
    )
  }

  const stageData = production.stage_data || {}
  const dist = stageData.distribution || {}
  const dev = stageData.development || {}
  const pre = stageData.pre_production || {}
  const prod = stageData.production || {}
  const post = stageData.post_production || {}
  const parcel = dev.location_report || {}
  const chron = production.chron || dist.chron || {}
  const chronBond = production.chron_bond || dist.chron_bond || {}
  const ipCatalog = production.ip_catalog || dist.ip_catalog || []
  const innovations = production.innovations || dist.innovations || []
  const replication = production.replication_kit || dist.replication_kit || {}
  const impact = production.impact_dashboard || dist.impact_dashboard || post.impact_dashboard || {}

  return (
    <div className="sp-page">
      <nav className="sp-nav">
        <Link to="/spheres" className="sp-nav-back">&larr; All Spheres</Link>
        <span className="sp-nav-brand">SPHERES</span>
      </nav>

      {/* HEADER */}
      <header className="sp-prod-header">
        <div className="sp-prod-header-inner">
          <div className="sp-prod-title-block">
            <h1 className="sp-prod-title">
              {parcel.address || production.subject}
            </h1>
            <div className="sp-prod-neighborhood">{parcel.neighborhood || ''}</div>
            <div className="sp-prod-meta">
              <span className="sp-prod-producer">{production.player_name || 'Producer'}</span>
              {production.completed_at && (
                <span className="sp-prod-date">
                  {new Date(production.completed_at).toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' })}
                </span>
              )}
            </div>
            {parcel.land_area_sqft > 0 && (
              <div className="sp-prod-parcel-stats">
                <span>{(parcel.land_area_sqft || 0).toLocaleString()} sqft</span>
                <span>Zoning: {parcel.zoning || 'N/A'}</span>
                <span>{parcel.vacant ? 'Vacant' : 'Improved'}</span>
              </div>
            )}
          </div>
          <div className="sp-prod-score-block">
            <ChronRings dimensions={chron} size={260} />
            <div className="sp-chron-breakdown">
              {[
                { key: 'unlock', label: 'Unlock (sqft)', val: chron.unlock },
                { key: 'access', label: 'Access (hours)', val: chron.access },
                { key: 'permanence', label: 'Permanence', val: chron.permanence },
                { key: 'catalyst', label: 'Catalyst', val: chron.catalyst },
                { key: 'policy', label: 'Policy', val: chron.policy },
              ].map(d => (
                <div key={d.key} className="sp-cb-row">
                  <span className="sp-cb-label">{d.label}</span>
                  <span className="sp-cb-val">{typeof d.val === 'number' ? d.val.toLocaleString() : '\u2014'}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </header>

      <main className="sp-prod-content">
        {/* IMPACT METRICS */}
        {impact.total_visitors > 0 && (
          <section className="sp-section">
            <h2 className="sp-section-title">Impact</h2>
            <div className="sp-impact-grid">
              <div className="sp-impact-stat">
                <span className="sp-is-val">{(impact.total_visitors || 0).toLocaleString()}</span>
                <span className="sp-is-label">Total Visitors</span>
              </div>
              <div className="sp-impact-stat">
                <span className="sp-is-val">${(impact.economic_impact || 0).toLocaleString()}</span>
                <span className="sp-is-label">Economic Impact</span>
              </div>
              <div className="sp-impact-stat">
                <span className="sp-is-val">{impact.jobs_created || 0}</span>
                <span className="sp-is-label">Jobs Created</span>
              </div>
              <div className="sp-impact-stat">
                <span className="sp-is-val">+{impact.property_value_impact_pct || 0}%</span>
                <span className="sp-is-label">Property Value</span>
              </div>
              <div className="sp-impact-stat">
                <span className="sp-is-val">{impact.community_rating || 0}/5</span>
                <span className="sp-is-label">Community Rating</span>
              </div>
            </div>
          </section>
        )}

        {/* PRODUCTION TIMELINE */}
        <section className="sp-section">
          <h2 className="sp-section-title">Production Timeline</h2>
          <ProductionTimeline stageData={stageData} deliverableLinks={production.deliverable_links} />
        </section>

        {/* DELIVERABLES */}
        <section className="sp-section">
          <h2 className="sp-section-title">Deliverables</h2>
          <p className="sp-section-sub">Every file generated during production, organized by stage.</p>
          <div className="sp-deliverables-grid">
            {STAGES.map(stage => {
              const files = production.deliverable_links?.[stage.key] || {}
              if (Object.keys(files).length === 0) return null
              return (
                <div key={stage.key} className="sp-deliv-stage">
                  <h3 className="sp-deliv-stage-label">{stage.label}</h3>
                  {Object.entries(files).map(([name, url]) => (
                    <a key={name} href={url} className="sp-deliv-file" download>
                      <span className="sp-df-icon">{name.endsWith('.json') ? '\u25A0' : '\u25A1'}</span>
                      <span className="sp-df-name">{name}</span>
                      <span className="sp-df-dl">&darr;</span>
                    </a>
                  ))}
                </div>
              )
            })}
          </div>
        </section>

        {/* BOND */}
        <section className="sp-section">
          <h2 className="sp-section-title">Financial Instrument</h2>
          <BondSection bond={chronBond} />
        </section>

        {/* IP PORTFOLIO */}
        <IPPortfolio ipCatalog={ipCatalog} />

        {/* INNOVATIONS */}
        {innovations.length > 0 && (
          <section className="sp-section">
            <h2 className="sp-section-title">Innovations</h2>
            <ul className="sp-innovations-list">
              {innovations.map((inn, i) => <li key={i}>{inn}</li>)}
            </ul>
          </section>
        )}

        {/* REPLICATION KIT */}
        {replication.parcel_type && (
          <section className="sp-section">
            <h2 className="sp-section-title">Replication Kit</h2>
            <div className="sp-replication">
              <div className="sp-rep-stat">
                <span className="sp-rep-val">{replication.parcel_type || '\u2014'}</span>
                <span className="sp-rep-label">Parcel Type</span>
              </div>
              <div className="sp-rep-stat">
                <span className="sp-rep-val">{replication.zoning || '\u2014'}</span>
                <span className="sp-rep-label">Zoning</span>
              </div>
              <div className="sp-rep-stat">
                <span className="sp-rep-val">{(replication.activation_types || []).join(', ').replace(/_/g, ' ') || '\u2014'}</span>
                <span className="sp-rep-label">Activation Types</span>
              </div>
              <div className="sp-rep-stat">
                <span className="sp-rep-val">{replication.transferable ? 'Yes' : 'No'}</span>
                <span className="sp-rep-label">Transferable</span>
              </div>
            </div>
          </section>
        )}

        {/* DATA TRANSPARENCY */}
        <DataTransparency stageData={stageData} impact={impact} />
      </main>

      <footer className="sp-footer">
        <div className="sp-footer-inner">
          <span>SPHERES</span>
          <span className="sp-footer-sep">/</span>
          <span>Cosm x Chron = Flourishing</span>
          <span className="sp-footer-sep">/</span>
          <span>BATHS</span>
        </div>
      </footer>
    </div>
  )
}
