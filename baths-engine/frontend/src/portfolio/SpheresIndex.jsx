import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import './SpheresPortfolio.css'

function ChronMiniRings({ dimensions, size = 80 }) {
  const dims = [
    { key: 'unlock', color: '#ff6d00', max: 50000 },
    { key: 'access', color: '#ff9100', max: 15000 },
    { key: 'permanence', color: '#ffab00', max: 1 },
    { key: 'catalyst', color: '#ffd600', max: 1 },
    { key: 'policy', color: '#aeea00', max: 1 },
  ]
  const cx = size / 2, cy = size / 2
  const ringWidth = 4, ringGap = 2
  const total = dimensions?.total || 0

  return (
    <svg viewBox={`0 0 ${size} ${size}`} className="sp-chron-mini">
      {dims.map((d, i) => {
        const r = (size / 2) - 8 - i * (ringWidth + ringGap)
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
          </g>
        )
      })}
      <text x={cx} y={cy + 3} textAnchor="middle" fill="#fff" fontSize="11" fontWeight="600" fontFamily="'Inter', sans-serif">
        {total.toFixed(0)}
      </text>
    </svg>
  )
}

export default function SpheresIndex() {
  const [productions, setProductions] = useState([])
  const [loading, setLoading] = useState(true)
  const [sort, setSort] = useState('date')

  useEffect(() => {
    fetch(`/api/portfolio/spheres?sort=${sort}`)
      .then(r => r.json())
      .then(data => {
        setProductions(data.productions || [])
        setLoading(false)
      })
      .catch(() => setLoading(false))
  }, [sort])

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

  return (
    <div className="sp-page">
      <header className="sp-header">
        <div className="sp-header-inner">
          <div className="sp-brand">
            <h1 className="sp-wordmark">SPHERES</h1>
            <p className="sp-tagline">Activate public spaces in cities.</p>
          </div>
          <div className="sp-header-meta">
            <span className="sp-count">{productions.length} Production{productions.length !== 1 ? 's' : ''}</span>
          </div>
        </div>
      </header>

      <div className="sp-toolbar">
        <div className="sp-toolbar-inner">
          <span className="sp-toolbar-label">Sort by</span>
          <button className={sort === 'date' ? 'active' : ''} onClick={() => setSort('date')}>Date</button>
          <button className={sort === 'chron' ? 'active' : ''} onClick={() => setSort('chron')}>Chron Score</button>
          <button className={sort === 'subject' ? 'active' : ''} onClick={() => setSort('subject')}>Location</button>
        </div>
      </div>

      <main className="sp-grid-wrap">
        {productions.length === 0 ? (
          <div className="sp-empty">
            <p>No completed sphere productions yet.</p>
            <p className="sp-empty-sub">Complete a SPHERES production in the game engine to publish it here.</p>
          </div>
        ) : (
          <div className="sp-grid">
            {productions.map(prod => {
              const loc = prod.location || {}
              const impact = prod.impact || {}
              return (
                <Link
                  key={prod.production_id}
                  to={`/spheres/${prod.production_id}`}
                  className="sp-card"
                >
                  <div className="sp-card-top">
                    <ChronMiniRings dimensions={prod.chron} />
                    <div className="sp-card-title-block">
                      <h2 className="sp-card-title">
                        {loc.address || prod.subject}
                      </h2>
                      <p className="sp-card-neighborhood">{loc.neighborhood || ''}</p>
                      <p className="sp-card-producer">{prod.player_name}</p>
                    </div>
                  </div>
                  <div className="sp-card-stats">
                    <div className="sp-card-stat">
                      <span className="sp-cs-val">{prod.chron_total?.toFixed(0) || '0'}</span>
                      <span className="sp-cs-label">Chron</span>
                    </div>
                    <div className="sp-card-stat">
                      <span className="sp-cs-val">{(loc.land_area_sqft || 0).toLocaleString()}</span>
                      <span className="sp-cs-label">sqft</span>
                    </div>
                    <div className="sp-card-stat">
                      <span className="sp-cs-val">${(impact.economic_impact || 0).toLocaleString()}</span>
                      <span className="sp-cs-label">Impact</span>
                    </div>
                    <div className="sp-card-stat">
                      <span className="sp-cs-val">{prod.ip_count || 0}</span>
                      <span className="sp-cs-label">IP</span>
                    </div>
                  </div>
                  {prod.chron_bond?.face_value > 0 && (
                    <div className="sp-card-bond">
                      <span className="sp-cb-rating">{prod.chron_bond.rating}</span>
                      <span className="sp-cb-val">${prod.chron_bond.face_value?.toLocaleString()}</span>
                      <span className="sp-cb-label">Chron Bond</span>
                    </div>
                  )}
                  <div className="sp-card-date">
                    {prod.completed_at ? new Date(prod.completed_at).toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' }) : ''}
                  </div>
                </Link>
              )
            })}
          </div>
        )}
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
