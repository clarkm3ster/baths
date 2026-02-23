import { useState, useEffect } from 'react'
import { useParams, Link } from 'react-router-dom'
import './DomesPortfolio.css'

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

// ── COSM Radar ─────────────────────────────────────────────────────
function CosmRadar({ dimensions, size = 280 }) {
  const dims = [
    { key: 'rights', label: 'RIGHTS' },
    { key: 'research', label: 'RESEARCH' },
    { key: 'budget', label: 'BUDGET' },
    { key: 'package', label: 'PACKAGE' },
    { key: 'deliverables', label: 'DELIVERABLES' },
    { key: 'pitch', label: 'PITCH' },
  ]

  const cx = size / 2, cy = size / 2, r = size * 0.34
  const angleStep = (Math.PI * 2) / 6

  const getPoint = (i, val) => {
    const angle = angleStep * i - Math.PI / 2
    const dist = (val / 100) * r
    return { x: cx + dist * Math.cos(angle), y: cy + dist * Math.sin(angle) }
  }

  const gridLevels = [0.25, 0.5, 0.75, 1.0]
  const values = dims.map(d => dimensions?.[d.key] || 0)
  const total = dimensions ? Math.min(...values) : 0
  const minIdx = values.indexOf(Math.min(...values))

  return (
    <svg viewBox={`0 0 ${size} ${size}`} className="dp-cosm-radar">
      {gridLevels.map(level => (
        <polygon key={level}
          points={dims.map((_, i) => {
            const p = getPoint(i, level * 100)
            return `${p.x},${p.y}`
          }).join(' ')}
          fill="none" stroke="#d0d0d0" strokeWidth="0.5"
        />
      ))}
      {dims.map((_, i) => {
        const p = getPoint(i, 100)
        return <line key={i} x1={cx} y1={cy} x2={p.x} y2={p.y} stroke="#e0e0e0" strokeWidth="0.5" />
      })}
      {dimensions && (
        <polygon
          points={dims.map((d, i) => {
            const p = getPoint(i, dimensions[d.key] || 0)
            return `${p.x},${p.y}`
          }).join(' ')}
          fill="rgba(0,0,0,0.05)" stroke="#1a1a1a" strokeWidth="1.5"
        />
      )}
      {dims.map((d, i) => {
        const val = dimensions ? (dimensions[d.key] || 0) : 0
        const p = getPoint(i, val)
        const lp = getPoint(i, 118)
        const isMin = i === minIdx && dimensions
        return (
          <g key={d.key}>
            {dimensions && <circle cx={p.x} cy={p.y} r="3" fill={isMin ? '#c62828' : '#1a1a1a'} />}
            <text x={lp.x} y={lp.y - 5} textAnchor="middle" dominantBaseline="middle"
              fill="#666" fontSize="8" fontFamily="Georgia, serif" letterSpacing="0.1em">
              {d.label}
            </text>
            {dimensions && (
              <text x={lp.x} y={lp.y + 7} textAnchor="middle"
                fill={isMin ? '#c62828' : '#1a1a1a'} fontSize="9" fontWeight="600" fontFamily="Georgia, serif">
                {val.toFixed(0)}
              </text>
            )}
          </g>
        )
      })}
      <text x={cx} y={cy - 4} textAnchor="middle" fill="#1a1a1a" fontSize="24" fontWeight="700" fontFamily="Georgia, serif">
        {total.toFixed(0)}
      </text>
      <text x={cx} y={cy + 12} textAnchor="middle" fill="#999" fontSize="8" fontFamily="Georgia, serif" letterSpacing="0.15em">
        COSM
      </text>
    </svg>
  )
}

// ── Production Timeline ────────────────────────────────────────────
function ProductionTimeline({ stageData, deliverableLinks }) {
  const [expanded, setExpanded] = useState(null)

  return (
    <div className="dp-timeline">
      {STAGES.map((stage, i) => {
        const data = stageData?.[stage.key]
        const isExpanded = expanded === stage.key
        const hasData = !!data
        const stageDeliverables = deliverableLinks?.[stage.key] || {}

        return (
          <div key={stage.key} className={`dp-tl-stage ${hasData ? 'completed' : 'pending'} ${isExpanded ? 'expanded' : ''}`}>
            <button className="dp-tl-header" onClick={() => setExpanded(isExpanded ? null : stage.key)} disabled={!hasData}>
              <div className="dp-tl-marker">
                <span className="dp-tl-num">{stage.num}</span>
                <div className={`dp-tl-dot ${hasData ? 'filled' : ''}`} />
              </div>
              <span className="dp-tl-label">{stage.label}</span>
              {hasData && <span className="dp-tl-toggle">{isExpanded ? '\u2212' : '+'}</span>}
            </button>
            {i < STAGES.length - 1 && <div className={`dp-tl-line ${hasData ? 'filled' : ''}`} />}
            {isExpanded && hasData && (
              <div className="dp-tl-detail">
                <StageDetail stage={stage.key} data={data} />
                {Object.keys(stageDeliverables).length > 0 && (
                  <div className="dp-tl-files">
                    <h4>Deliverables</h4>
                    {Object.entries(stageDeliverables).map(([name, url]) => (
                      <a key={name} href={url} className="dp-file-link" download>
                        <span className="dp-file-icon">{name.endsWith('.json') ? '\u25A0' : '\u25A1'}</span>
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

function StageDetail({ stage, data }) {
  if (stage === 'development') {
    const rights = data.rights_package || {}
    const allRights = Object.values(rights).flat()
    return (
      <div className="dp-stage-detail">
        <div className="dp-sd-row">
          <span className="dp-sd-metric">{data.rights_count || allRights.length}</span>
          <span className="dp-sd-label">legal provisions acquired across {Object.keys(rights).length} regulatory dimensions</span>
        </div>
        <div className="dp-sd-row">
          <span className="dp-sd-metric">{data.system_count || 0}</span>
          <span className="dp-sd-label">government data systems mapped</span>
        </div>
        <div className="dp-sd-row">
          <span className="dp-sd-metric">{data.cost_point_count || 0}</span>
          <span className="dp-sd-label">cost data points sourced from CMS, HUD, Vera, HCUP</span>
        </div>
        <div className="dp-sd-row">
          <span className="dp-sd-metric">{data.active_links || 0}</span>
          <span className="dp-sd-label">active inter-system connections / {data.blocked_links || 0} blocked</span>
        </div>
        <div className="dp-sd-sources">
          <h5>Sources</h5>
          <ul>
            <li>Electronic Code of Federal Regulations (eCFR) &mdash; ecfr.gov</li>
            <li>Federal Register &mdash; federalregister.gov</li>
            <li>CMS, HUD, BLS, Census ACS, Vera Institute, HCUP</li>
          </ul>
        </div>
      </div>
    )
  }
  if (stage === 'pre_production') {
    const script = data.shooting_script || {}
    const crew = data.coordination_crew || []
    const budget = data.budget_top_sheet || {}
    return (
      <div className="dp-stage-detail">
        <div className="dp-sd-row">
          <span className="dp-sd-metric">{((script.overall_coverage || 0) * 100).toFixed(0)}%</span>
          <span className="dp-sd-label">dome coverage across {(script.layers || []).length} architectural layers</span>
        </div>
        <div className="dp-sd-row">
          <span className="dp-sd-metric">{crew.length}</span>
          <span className="dp-sd-label">coordination models evaluated and fitted</span>
        </div>
        <div className="dp-sd-row">
          <span className="dp-sd-metric">${(budget.annual_fragmentation_cost || 0).toLocaleString()}</span>
          <span className="dp-sd-label">annual fragmentation cost identified</span>
        </div>
        <div className="dp-sd-row">
          <span className="dp-sd-metric">${(budget.annual_coordination_savings || 0).toLocaleString()}</span>
          <span className="dp-sd-label">annual coordination savings projected</span>
        </div>
        <div className="dp-sd-sources">
          <h5>Sources</h5>
          <ul>
            <li>CMS Innovation Center &mdash; ACO, Bundled Payment models</li>
            <li>HUD Moving to Work demonstrations</li>
            <li>SAMHSA CCBHC integration models</li>
            <li>Nussbaum Central Capabilities / OECD Better Life Index</li>
          </ul>
        </div>
      </div>
    )
  }
  if (stage === 'production') {
    const agreements = data.executed_agreements || []
    const callSheet = data.call_sheet || {}
    return (
      <div className="dp-stage-detail">
        <div className="dp-sd-row">
          <span className="dp-sd-metric">{agreements.length}</span>
          <span className="dp-sd-label">coordination agreements executed</span>
        </div>
        <div className="dp-sd-row">
          <span className="dp-sd-metric">{callSheet.rights_applied || 0}</span>
          <span className="dp-sd-label">rights applied across {callSheet.systems_connected || 0} connected systems</span>
        </div>
        <div className="dp-sd-row">
          <span className="dp-sd-metric">{callSheet.coordination_model || 'N/A'}</span>
          <span className="dp-sd-label">primary coordination architecture</span>
        </div>
      </div>
    )
  }
  if (stage === 'post_production') {
    const assembly = data.assembly_cut || {}
    const grade = data.color_grade || {}
    const ipOutputs = data.ip_outputs || []
    return (
      <div className="dp-stage-detail">
        <div className="dp-sd-row">
          <span className="dp-sd-metric">{((assembly.coverage || 0) * 100).toFixed(0)}%</span>
          <span className="dp-sd-label">dome coverage verified across {(assembly.dimensions_covered || []).length} dimensions</span>
        </div>
        <div className="dp-sd-row">
          <span className="dp-sd-metric">{grade.grade || 'N/A'}</span>
          <span className="dp-sd-label">flourishing grade &mdash; {((grade.overall_score || 0) * 100).toFixed(0)}% score</span>
        </div>
        <div className="dp-sd-row">
          <span className="dp-sd-metric">{ipOutputs.length}</span>
          <span className="dp-sd-label">IP outputs generated across {new Set(ipOutputs.map(ip => ip.domain)).size} domains</span>
        </div>
      </div>
    )
  }
  if (stage === 'distribution') {
    const cosm = data.cosm || {}
    const bond = data.dome_bond || {}
    return (
      <div className="dp-stage-detail">
        <div className="dp-sd-row">
          <span className="dp-sd-metric">{Math.min(cosm.rights || 0, cosm.research || 0, cosm.budget || 0, cosm.package || 0, cosm.deliverables || 0, cosm.pitch || 0).toFixed(1)}</span>
          <span className="dp-sd-label">final COSM score (weakest dimension principle)</span>
        </div>
        <div className="dp-sd-row">
          <span className="dp-sd-metric">${(bond.face_value || 0).toLocaleString()}</span>
          <span className="dp-sd-label">Dome Bond face value &mdash; {bond.rating || 'N/A'} rated</span>
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

  return (
    <section className="dp-section">
      <h2 className="dp-section-title">Intellectual Property Portfolio</h2>
      <p className="dp-section-sub">{ipCatalog.length} outputs across {Object.keys(byDomain).length} domains</p>
      <div className="dp-ip-grid">
        {Object.entries(byDomain).map(([domain, items]) => (
          <div key={domain} className="dp-ip-domain">
            <h3 className="dp-ip-domain-name">{IP_DOMAIN_LABELS[domain] || domain}</h3>
            {items.map((ip, j) => (
              <div key={j} className="dp-ip-item">
                <div className="dp-ip-title">{ip.title}</div>
                <p className="dp-ip-desc">{ip.description}</p>
                <div className="dp-ip-meta">
                  <span>{ip.format?.replace(/_/g, ' ')}</span>
                  <span className="dp-ip-stage">Stage: {ip.stage_originated?.replace(/_/g, ' ')}</span>
                </div>
                {ip.value_driver && <div className="dp-ip-driver">{ip.value_driver}</div>}
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
  return (
    <div className="dp-bond">
      <div className="dp-bond-header">
        <span className="dp-bond-type">Dome Bond</span>
        <span className="dp-bond-rating">{bond.rating}</span>
      </div>
      <div className="dp-bond-id">{bond.bond_id}</div>
      <div className="dp-bond-grid">
        <div className="dp-bond-stat primary">
          <span className="dp-bs-val">${bond.face_value?.toLocaleString()}</span>
          <span className="dp-bs-label">Face Value</span>
        </div>
        <div className="dp-bond-stat">
          <span className="dp-bs-val">{bond.coupon_rate}%</span>
          <span className="dp-bs-label">Coupon Rate</span>
        </div>
        <div className="dp-bond-stat">
          <span className="dp-bs-val">{bond.maturity_years} yr</span>
          <span className="dp-bs-label">Maturity</span>
        </div>
        <div className="dp-bond-stat">
          <span className="dp-bs-val">{bond.yield_to_maturity}%</span>
          <span className="dp-bs-label">Yield to Maturity</span>
        </div>
        <div className="dp-bond-stat">
          <span className="dp-bs-val">{bond.cosm_score}</span>
          <span className="dp-bs-label">COSM at Issuance</span>
        </div>
        <div className="dp-bond-stat">
          <span className="dp-bs-val">{bond.programs_backing}</span>
          <span className="dp-bs-label">Programs Backing</span>
        </div>
      </div>
    </div>
  )
}

// ── Data Transparency ──────────────────────────────────────────────
function DataTransparency({ stageData, dataEngineStats }) {
  const dev = stageData?.development || {}
  const pre = stageData?.pre_production || {}
  const stats = dataEngineStats || dev.data_engine_stats || {}

  const allRights = Object.values(dev.rights_package || {}).flat()
  const allCosts = Object.values(dev.market_analysis || {}).flat()
  const budget = pre.budget_top_sheet || {}

  return (
    <section className="dp-section">
      <h2 className="dp-section-title">Data Transparency</h2>
      <p className="dp-section-sub">Every data point in this production is sourced from public federal databases.</p>

      <div className="dp-data-grid">
        <div className="dp-data-card">
          <div className="dp-dc-val">{allRights.length || dev.rights_count || 0}</div>
          <div className="dp-dc-label">Legal Provisions</div>
          <div className="dp-dc-source">eCFR, Federal Register</div>
        </div>
        <div className="dp-data-card">
          <div className="dp-dc-val">{allCosts.length || dev.cost_point_count || 0}</div>
          <div className="dp-dc-label">Cost Data Points</div>
          <div className="dp-dc-source">CMS, HUD, HCUP, Vera, BLS</div>
        </div>
        <div className="dp-data-card">
          <div className="dp-dc-val">{(dev.cast_list || []).length || dev.system_count || 0}</div>
          <div className="dp-dc-label">Government Systems</div>
          <div className="dp-dc-source">Federal, state, local data systems</div>
        </div>
        <div className="dp-data-card">
          <div className="dp-dc-val">{(dev.deal_structure || []).length || 0}</div>
          <div className="dp-dc-label">System Connections</div>
          <div className="dp-dc-source">Active, blocked, and possible links</div>
        </div>
        <div className="dp-data-card">
          <div className="dp-dc-val">{stats.enrichments || 0}</div>
          <div className="dp-dc-label">Cross-References</div>
          <div className="dp-dc-source">BATHS Enrichment Engine</div>
        </div>
      </div>

      {budget.annual_fragmentation_cost > 0 && (
        <div className="dp-cost-delta">
          <h3>Cost Delta</h3>
          <div className="dp-cd-bars">
            <div className="dp-cd-bar fragmented">
              <span className="dp-cd-label">Fragmented</span>
              <span className="dp-cd-val">${(budget.annual_fragmentation_cost || 0).toLocaleString()}/yr</span>
            </div>
            <div className="dp-cd-bar coordinated">
              <span className="dp-cd-label">Coordinated</span>
              <span className="dp-cd-val">${((budget.annual_fragmentation_cost || 0) - (budget.annual_coordination_savings || 0)).toLocaleString()}/yr</span>
            </div>
            <div className="dp-cd-savings">
              <span className="dp-cd-label">Documented Savings</span>
              <span className="dp-cd-val">${(budget.annual_coordination_savings || 0).toLocaleString()}/yr</span>
            </div>
          </div>
        </div>
      )}

      <div className="dp-sources-list">
        <h3>Data Sources</h3>
        <ul>
          <li><strong>eCFR</strong> &mdash; Electronic Code of Federal Regulations <span className="dp-src-url">ecfr.gov</span></li>
          <li><strong>Federal Register</strong> &mdash; Daily journal of the US Government <span className="dp-src-url">federalregister.gov</span></li>
          <li><strong>CMS</strong> &mdash; Centers for Medicare & Medicaid Services <span className="dp-src-url">cms.gov</span></li>
          <li><strong>HUD</strong> &mdash; Department of Housing and Urban Development <span className="dp-src-url">hud.gov</span></li>
          <li><strong>BLS</strong> &mdash; Bureau of Labor Statistics <span className="dp-src-url">bls.gov</span></li>
          <li><strong>Census ACS</strong> &mdash; American Community Survey 5-Year <span className="dp-src-url">census.gov</span></li>
          <li><strong>Vera Institute</strong> &mdash; Incarceration cost data <span className="dp-src-url">vera.org</span></li>
          <li><strong>HCUP</strong> &mdash; Healthcare Cost and Utilization Project <span className="dp-src-url">hcup-us.ahrq.gov</span></li>
          <li><strong>SAMHSA</strong> &mdash; Substance Abuse and Mental Health Services <span className="dp-src-url">samhsa.gov</span></li>
        </ul>
      </div>
    </section>
  )
}

// ══════════════════════════════════════════════════════════════════
// MAIN DOME PRODUCTION PAGE
// ══════════════════════════════════════════════════════════════════

export default function DomeProductionPage() {
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
      <div className="dp-page">
        <div className="dp-loading">
          <div className="dp-loading-mark">DOMES</div>
          <div className="dp-loading-line" />
        </div>
      </div>
    )
  }

  if (!production) {
    return (
      <div className="dp-page">
        <div className="dp-empty">
          <p>Production not found.</p>
          <Link to="/domes" className="dp-back-link">&larr; Back to all domes</Link>
        </div>
      </div>
    )
  }

  const stageData = production.stage_data || {}
  const dist = stageData.distribution || {}
  const dev = stageData.development || {}
  const pre = stageData.pre_production || {}
  const cosm = production.cosm || dist.cosm || {}
  const cosmValues = [cosm.rights || 0, cosm.research || 0, cosm.budget || 0,
    cosm.package || 0, cosm.deliverables || 0, cosm.pitch || 0]
  const cosmTotal = Math.min(...cosmValues)
  const minDimIdx = cosmValues.indexOf(Math.min(...cosmValues))
  const dimNames = ['Rights', 'Research', 'Budget', 'Package', 'Deliverables', 'Pitch']
  const limitingFactor = dimNames[minDimIdx]

  const domeBond = production.dome_bond || dist.dome_bond || {}
  const ipCatalog = production.ip_catalog || dist.ip_catalog || []
  const innovations = production.innovations || dist.innovations || []
  const industries = production.industries_changed || dist.industries_changed || []
  const narrative = production.narrative || dist.narrative || {}
  const replication = production.replication_kit || dist.replication_kit || {}

  return (
    <div className="dp-page">
      <nav className="dp-nav">
        <Link to="/domes" className="dp-nav-back">&larr; All Domes</Link>
        <span className="dp-nav-brand">DOMES</span>
      </nav>

      {/* HEADER */}
      <header className="dp-prod-header">
        <div className="dp-prod-header-inner">
          <div className="dp-prod-title-block">
            <h1 className="dp-prod-title">The {production.subject} Dome</h1>
            <div className="dp-prod-meta">
              <span className="dp-prod-producer">{production.player_name || 'Producer'}</span>
              {production.completed_at && (
                <span className="dp-prod-date">
                  {new Date(production.completed_at).toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' })}
                </span>
              )}
            </div>
          </div>
          <div className="dp-prod-score-block">
            <CosmRadar dimensions={cosm} size={260} />
            <div className="dp-prod-limiting">
              Limiting factor: <strong>{limitingFactor}</strong> ({cosmValues[minDimIdx].toFixed(0)})
            </div>
          </div>
        </div>
      </header>

      <main className="dp-prod-content">
        {/* PRODUCTION TIMELINE */}
        <section className="dp-section">
          <h2 className="dp-section-title">Production Timeline</h2>
          <ProductionTimeline stageData={stageData} deliverableLinks={production.deliverable_links} />
        </section>

        {/* DELIVERABLES SECTION */}
        <section className="dp-section">
          <h2 className="dp-section-title">Deliverables</h2>
          <p className="dp-section-sub">Every file generated during production, organized by stage.</p>
          <div className="dp-deliverables-grid">
            {STAGES.map(stage => {
              const files = production.deliverable_links?.[stage.key] || {}
              if (Object.keys(files).length === 0) return null
              return (
                <div key={stage.key} className="dp-deliv-stage">
                  <h3 className="dp-deliv-stage-label">{stage.label}</h3>
                  {Object.entries(files).map(([name, url]) => (
                    <a key={name} href={url} className="dp-deliv-file" download>
                      <span className="dp-df-icon">{name.endsWith('.json') ? '\u25A0' : '\u25A1'}</span>
                      <span className="dp-df-name">{name}</span>
                      <span className="dp-df-dl">&darr;</span>
                    </a>
                  ))}
                </div>
              )
            })}
          </div>
        </section>

        {/* NARRATIVE */}
        {narrative.sections && narrative.sections.length > 0 && (
          <section className="dp-section">
            <h2 className="dp-section-title">The Pitch</h2>
            <div className="dp-narrative">
              {narrative.sections.map((s, i) => (
                <div key={i} className="dp-narrative-section">
                  <h3>{s.title}</h3>
                  <p>{s.content}</p>
                </div>
              ))}
            </div>
          </section>
        )}

        {/* BOND */}
        <section className="dp-section">
          <h2 className="dp-section-title">Financial Instrument</h2>
          <BondSection bond={domeBond} />
        </section>

        {/* IP PORTFOLIO */}
        <IPPortfolio ipCatalog={ipCatalog} />

        {/* INNOVATIONS + INDUSTRIES */}
        {(innovations.length > 0 || industries.length > 0) && (
          <section className="dp-section">
            <div className="dp-innovations-grid">
              {innovations.length > 0 && (
                <div>
                  <h2 className="dp-section-title">Innovations</h2>
                  <ul className="dp-innovations-list">
                    {innovations.map((inn, i) => <li key={i}>{inn}</li>)}
                  </ul>
                </div>
              )}
              {industries.length > 0 && (
                <div>
                  <h2 className="dp-section-title">Industries Changed</h2>
                  <ul className="dp-innovations-list">
                    {industries.map((ind, i) => <li key={i}>{ind}</li>)}
                  </ul>
                </div>
              )}
            </div>
          </section>
        )}

        {/* REPLICATION KIT */}
        {replication.coverage > 0 && (
          <section className="dp-section">
            <h2 className="dp-section-title">Replication Kit</h2>
            <div className="dp-replication">
              <div className="dp-rep-stat">
                <span className="dp-rep-val">{((replication.coverage || 0) * 100).toFixed(0)}%</span>
                <span className="dp-rep-label">Coverage</span>
              </div>
              <div className="dp-rep-stat">
                <span className="dp-rep-val">{replication.coordination_model || '\u2014'}</span>
                <span className="dp-rep-label">Coordination Model</span>
              </div>
              <div className="dp-rep-stat">
                <span className="dp-rep-val">${(replication.estimated_savings || 0).toLocaleString()}/yr</span>
                <span className="dp-rep-label">Estimated Savings</span>
              </div>
              <div className="dp-rep-stat">
                <span className="dp-rep-val">{replication.transferable ? 'Yes' : 'No'}</span>
                <span className="dp-rep-label">Transferable</span>
              </div>
            </div>
          </section>
        )}

        {/* DATA TRANSPARENCY */}
        <DataTransparency stageData={stageData} dataEngineStats={production.data_engine_stats} />
      </main>

      <footer className="dp-footer">
        <div className="dp-footer-inner">
          <span>DOMES</span>
          <span className="dp-footer-sep">/</span>
          <span>Cosm x Chron = Flourishing</span>
          <span className="dp-footer-sep">/</span>
          <span>BATHS</span>
        </div>
      </footer>
    </div>
  )
}
