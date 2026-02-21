import { useState, useEffect } from 'react'
import './Portfolio.css'

function DimensionBar({ label, value, maxValue = 100, color }) {
  const pct = Math.min((value / maxValue) * 100, 100)
  return (
    <div className="dim-bar">
      <div className="dim-bar-header">
        <span className="dim-label">{label}</span>
        <span className="dim-value" style={{ color }}>{value.toFixed(1)}</span>
      </div>
      <div className="dim-track">
        <div className="dim-fill" style={{ width: `${pct}%`, background: color, boxShadow: `0 0 10px ${color}40` }}></div>
      </div>
    </div>
  )
}

function CosmStatePanel({ cosmState }) {
  if (!cosmState || cosmState.total_domes === 0) return null

  const m = cosmState.maturity || {}
  const maturityColors = { seed: '#8090a8', seedling: '#ffab00', emerging: '#ff9100', growing: '#00e676', mature: '#00e5ff' }

  return (
    <div className="section cosm-state-section">
      <div className="section-header">
        <h3>COSM CURRENCY STATE</h3>
        <span className="section-count" style={{ color: maturityColors[m.level] || '#8090a8' }}>{m.level?.toUpperCase()}</span>
      </div>
      <p className="cosm-state-subtitle">Fragment + Cosm agents — {cosmState.total_domes} domes across {cosmState.geographies} geographies</p>

      <div className="cosm-state-grid">
        <div className="cs-stat">
          <span className="cs-val">{cosmState.total_domes}</span>
          <span className="cs-label">Total Domes</span>
        </div>
        <div className="cs-stat">
          <span className="cs-val">{cosmState.average_cosm}</span>
          <span className="cs-label">Avg Cosm</span>
        </div>
        <div className="cs-stat">
          <span className="cs-val">{cosmState.geographies}</span>
          <span className="cs-label">Geographies</span>
        </div>
        <div className="cs-stat">
          <span className="cs-val">{cosmState.programs_mapped}</span>
          <span className="cs-label">Programs</span>
        </div>
        <div className="cs-stat big">
          <span className="cs-val savings">${(cosmState.total_coordination_savings || 0).toLocaleString()}</span>
          <span className="cs-label">Total Coordination Savings</span>
        </div>
        <div className="cs-stat">
          <span className="cs-val">${(cosmState.average_delta_per_dome || 0).toLocaleString()}</span>
          <span className="cs-label">Avg Delta / Dome</span>
        </div>
      </div>

      <div className="cosm-costs-bar">
        <div className="costs-bar-segment fragmented" style={{ flex: cosmState.total_fragmented_cost || 1 }}>
          <span className="cb-label">Fragmented</span>
          <span className="cb-val">${(cosmState.total_fragmented_cost || 0).toLocaleString()}</span>
        </div>
        <div className="costs-bar-segment coordinated" style={{ flex: cosmState.total_coordinated_cost || 1 }}>
          <span className="cb-label">Coordinated</span>
          <span className="cb-val">${(cosmState.total_coordinated_cost || 0).toLocaleString()}</span>
        </div>
      </div>
    </div>
  )
}

export default function Portfolio({ player }) {
  const portfolio = player.portfolio
  const [cosmState, setCosmState] = useState(null)

  useEffect(() => {
    fetch('/api/cosm/state')
      .then(r => r.json())
      .then(d => { if (d.total_domes > 0) setCosmState(d) })
      .catch(() => {})
  }, [])

  const cosmMin = portfolio.total_cosm ? Math.min(
    portfolio.total_cosm.legal, portfolio.total_cosm.data,
    portfolio.total_cosm.fiscal, portfolio.total_cosm.coordination,
    portfolio.total_cosm.flourishing, portfolio.total_cosm.narrative
  ) : 0

  const chronTotal = portfolio.total_chron
    ? (portfolio.total_chron.unlock * portfolio.total_chron.access) *
      (1 + ((portfolio.total_chron.permanence + portfolio.total_chron.catalyst + portfolio.total_chron.policy) / 3))
    : 0

  const flourishing = cosmMin * chronTotal

  const hasDomes = portfolio.domes_completed?.length > 0
  const hasSpheres = portfolio.spheres_completed?.length > 0
  const hasData = hasDomes || hasSpheres

  return (
    <div className="portfolio">
      <div className="portfolio-hero">
        <div className="portfolio-hero-bg"></div>
        <div className="portfolio-hero-content">
          <div className="portfolio-badge">PRODUCER PORTFOLIO</div>
          <h2 className="portfolio-name">{player.name}</h2>
        </div>
      </div>

      <div className="portfolio-content">
        <div className="score-cards">
          <div className="score-card cosm-card">
            <div className="card-header">
              <div className="card-icon-small cosm-icon">
                <svg viewBox="0 0 24 24"><path d="M4 18 Q4 6 12 3 Q20 6 20 18" fill="none" stroke="currentColor" strokeWidth="1.5"/><line x1="4" y1="18" x2="20" y2="18" stroke="currentColor" strokeWidth="1.5"/></svg>
              </div>
              <div>
                <div className="card-label">TOTAL COSM</div>
                <div className="card-sublabel">Weakest dimension</div>
              </div>
            </div>
            <div className="card-value cosm-value">{cosmMin.toFixed(1)}</div>
            {portfolio.total_cosm && (
              <div className="dimensions-list">
                <DimensionBar label="Legal" value={portfolio.total_cosm.legal} color="var(--domes-primary)" />
                <DimensionBar label="Data" value={portfolio.total_cosm.data} color="var(--domes-primary)" />
                <DimensionBar label="Fiscal" value={portfolio.total_cosm.fiscal} color="var(--domes-primary)" />
                <DimensionBar label="Coordination" value={portfolio.total_cosm.coordination} color="var(--domes-primary)" />
                <DimensionBar label="Flourishing" value={portfolio.total_cosm.flourishing} color="var(--domes-primary)" />
                <DimensionBar label="Narrative" value={portfolio.total_cosm.narrative} color="var(--domes-primary)" />
              </div>
            )}
          </div>

          <div className="score-card chron-card">
            <div className="card-header">
              <div className="card-icon-small chron-icon">
                <svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="9" fill="none" stroke="currentColor" strokeWidth="1.5"/><ellipse cx="12" cy="12" rx="9" ry="4" fill="none" stroke="currentColor" strokeWidth="0.8" opacity="0.5"/></svg>
              </div>
              <div>
                <div className="card-label">TOTAL CHRON</div>
                <div className="card-sublabel">m&#178; x time x significance</div>
              </div>
            </div>
            <div className="card-value chron-value">{chronTotal.toFixed(1)}</div>
            {portfolio.total_chron && (
              <div className="dimensions-list">
                <DimensionBar label="Unlock" value={portfolio.total_chron.unlock} maxValue={5000} color="var(--spheres-primary)" />
                <DimensionBar label="Access" value={portfolio.total_chron.access} maxValue={1000} color="var(--spheres-primary)" />
                <DimensionBar label="Permanence" value={portfolio.total_chron.permanence} maxValue={1} color="var(--spheres-primary)" />
                <DimensionBar label="Catalyst" value={portfolio.total_chron.catalyst} maxValue={1} color="var(--spheres-primary)" />
                <DimensionBar label="Policy" value={portfolio.total_chron.policy} maxValue={1} color="var(--spheres-primary)" />
              </div>
            )}
          </div>

          <div className="score-card flourishing-card">
            <div className="card-header">
              <div className="card-icon-small flourishing-icon">&#10022;</div>
              <div>
                <div className="card-label">FLOURISHING</div>
                <div className="card-sublabel">Cosm x Chron</div>
              </div>
            </div>
            <div className="card-value flourishing-value">{flourishing.toFixed(1)}</div>
            <div className="flourishing-formula">
              <span className="formula-part cosm-part">{cosmMin.toFixed(1)}</span>
              <span className="formula-op">x</span>
              <span className="formula-part chron-part">{chronTotal.toFixed(1)}</span>
              <span className="formula-op">=</span>
              <span className="formula-result">{flourishing.toFixed(1)}</span>
            </div>
          </div>
        </div>

        <div className="portfolio-sections">
          {cosmState && <CosmStatePanel cosmState={cosmState} />}

          <div className="section productions-section">
            <div className="section-header">
              <h3>COMPLETED PRODUCTIONS</h3>
              <span className="section-count">{(portfolio.domes_completed?.length || 0) + (portfolio.spheres_completed?.length || 0)}</span>
            </div>

            <div className="productions-grid">
              <div className="production-type">
                <div className="type-header domes-type">
                  <span className="type-icon">&#9651;</span>
                  <span>DOMES</span>
                  <span className="type-count">{portfolio.domes_completed?.length || 0}</span>
                </div>
                {hasDomes ? (
                  <div className="production-list">
                    {portfolio.domes_completed.map(prod => (
                      <div key={prod.production_id} className="production-item domes-item">
                        <div className="item-name">{prod.subject}</div>
                        {prod.cosm && <div className="item-score">Cosm: {Math.min(prod.cosm.legal, prod.cosm.data, prod.cosm.fiscal, prod.cosm.coordination, prod.cosm.flourishing, prod.cosm.narrative).toFixed(1)}</div>}
                      </div>
                    ))}
                  </div>
                ) : (
                  <div className="empty-state">No domes completed yet</div>
                )}
              </div>

              <div className="production-type">
                <div className="type-header spheres-type">
                  <span className="type-icon">&#9675;</span>
                  <span>SPHERES</span>
                  <span className="type-count">{portfolio.spheres_completed?.length || 0}</span>
                </div>
                {hasSpheres ? (
                  <div className="production-list">
                    {portfolio.spheres_completed.map(prod => (
                      <div key={prod.production_id} className="production-item spheres-item">
                        <div className="item-name">{prod.subject}</div>
                        {prod.chron && <div className="item-score">Chron: {prod.chron.unlock.toFixed(0)} m&#178;</div>}
                      </div>
                    ))}
                  </div>
                ) : (
                  <div className="empty-state">No spheres completed yet</div>
                )}
              </div>
            </div>
          </div>

          <div className="bottom-sections">
            <div className="section innovations-section">
              <div className="section-header">
                <h3>INNOVATIONS</h3>
                <span className="section-count">{portfolio.innovations?.length || 0}</span>
              </div>
              {portfolio.innovations?.length > 0 ? (
                <div className="tag-list">
                  {portfolio.innovations.map((inn, i) => (
                    <div key={i} className="innovation-tag">{inn}</div>
                  ))}
                </div>
              ) : (
                <div className="empty-state">Complete productions to generate innovations</div>
              )}
            </div>

            <div className="section industries-section">
              <div className="section-header">
                <h3>INDUSTRIES CHANGED</h3>
                <span className="section-count">{portfolio.industries_changed?.length || 0}</span>
              </div>
              {portfolio.industries_changed?.length > 0 ? (
                <div className="tag-list">
                  {portfolio.industries_changed.map((ind, i) => (
                    <div key={i} className="industry-tag">{ind}</div>
                  ))}
                </div>
              ) : (
                <div className="empty-state">Complete productions to change industries</div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
