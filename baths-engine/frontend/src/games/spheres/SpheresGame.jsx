import { useState, useRef } from 'react'
import './SpheresGame.css'

const STAGES = [
  { key: 'development', label: 'DISCOVER', num: '01', desc: 'Research the parcel — real property data, zoning, context', verb: 'Discovering' },
  { key: 'pre_production', label: 'DESIGN', num: '02', desc: 'Plan the activation — type, cost, timeline', verb: 'Designing' },
  { key: 'production', label: 'BUILD', num: '03', desc: 'Execute permits, construct, activate', verb: 'Building' },
  { key: 'post_production', label: 'MEASURE', num: '04', desc: 'Document impact, generate innovations', verb: 'Measuring' },
  { key: 'distribution', label: 'COMPLETE', num: '05', desc: 'Final CHRON score and portfolio', verb: 'Completing' },
]

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

// ── Stage Renderers ───────────────────────────────────────────────────

function DiscoverStage({ data }) {
  if (!data) return null
  const parcel = data.parcel || {}
  const permits = data.permits?.standard_permits || []
  const insights = data.insights || []
  const nearby = data.nearby_parcels || []

  return (
    <div className="stage-content discover">
      <ParcelCard parcel={parcel} />

      {insights.length > 0 && (
        <div className="section-block">
          <h3 className="section-title">ACTIVATION INSIGHTS</h3>
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
        <h3 className="section-title">PERMITS REQUIRED</h3>
        <div className="permits-list">
          {permits.map((p, i) => <PermitCard key={i} permit={p} index={i} />)}
        </div>
      </div>

      <NearbyParcels parcels={nearby} />
    </div>
  )
}

function DesignStage({ data }) {
  if (!data) return null
  const design = data.design || {}
  const cost = data.cost || {}
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
        <h3 className="section-title">INVESTMENT TIERS</h3>
        <CostTiers cost={cost} />
      </div>

      <div className="section-block">
        <Timeline timeline={timeline} />
      </div>
    </div>
  )
}

function BuildStage({ data }) {
  if (!data) return null
  const permits = data.permits || {}
  const world = data.world || {}
  const executedPermits = permits.permits || []
  const policyChanges = permits.policy_changes || []

  return (
    <div className="stage-content build">
      <div className="activation-banner">
        <div className="act-icon">◉</div>
        <h3>SPHERE ACTIVATED</h3>
        <div className="act-stats">
          <span><strong>{(world.sqft_activated || 0).toLocaleString()}</strong> sqft</span>
          <span><strong>{world.events_capacity || 0}</strong> capacity</span>
          <span><strong>${(world.investment || 0).toLocaleString()}</strong> invested</span>
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

      {world.features_installed?.length > 0 && (
        <div className="section-block">
          <h3 className="section-title">FEATURES INSTALLED</h3>
          <div className="installed-features">
            {world.features_installed.map((f, i) => <span key={i} className="feature-tag installed">{f}</span>)}
          </div>
        </div>
      )}
    </div>
  )
}

function MeasureStage({ data }) {
  if (!data) return null
  const episodes = data.episodes?.episodes || []
  const metrics = data.metrics || {}
  const innovations = data.innovations || {}

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
            <div key={i} className="inn-item"><span className="inn-dot">◆</span>{inn}</div>
          ))}
        </div>
      </div>
    </div>
  )
}

function CompletionStage({ data }) {
  if (!data) return null
  const chron = data.chron || {}
  const metrics = data.metrics || {}
  const innovations = data.innovations || []

  return (
    <div className="stage-content completion">
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

      {innovations.length > 0 && (
        <div className="section-block">
          <h3 className="section-title">INNOVATIONS PORTFOLIO</h3>
          <div className="innovations-list">
            {innovations.map((inn, i) => (
              <div key={i} className="inn-item"><span className="inn-dot">◆</span>{inn}</div>
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
  const contentRef = useRef(null)

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
      {/* ── Fixed Header ────────────────────────────────────── */}
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

      {/* ── Stage Hero ──────────────────────────────────────── */}
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

      {/* ── Content ─────────────────────────────────────────── */}
      <div className="game-content" ref={contentRef}>
        {lastMessage && (
          <div className="game-message spheres">
            <p>{lastMessage}</p>
          </div>
        )}

        {devData && <DiscoverStage data={devData} />}
        {preData && <DesignStage data={preData} />}
        {prodData && <BuildStage data={prodData} />}
        {postData && <MeasureStage data={postData} />}
        {distData && <CompletionStage data={distData} />}

        {!devData && !isComplete && (
          <div className="empty-stage spheres">
            <div className="empty-icon">◎</div>
            <p>Begin discovery to research the parcel, zoning data, and neighborhood context for <strong>{production.subject}</strong>.</p>
          </div>
        )}
      </div>

      {/* ── Action Bar ──────────────────────────────────────── */}
      <div className="game-action-bar spheres">
        {!isComplete ? (
          <button className="advance-btn spheres" onClick={handleAdvance} disabled={working}>
            {working ? (
              <><span className="spinner spheres" /><span>{currentStage.verb}...</span></>
            ) : (
              <span>{currentStageIndex === 0 && !devData ? 'BEGIN DISCOVERY' : `ADVANCE → ${STAGES[Math.min(currentStageIndex + 1, 4)]?.label || 'COMPLETE'}`}</span>
            )}
          </button>
        ) : (
          <div className="complete-bar spheres">
            <span className="complete-icon">◉</span>
            <span>SPHERE COMPLETE — CHRON: {(runningChron?.total || 0).toFixed(1)}</span>
          </div>
        )}
      </div>
    </div>
  )
}
