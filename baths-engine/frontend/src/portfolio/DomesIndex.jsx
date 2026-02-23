import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import './DomesPortfolio.css'

function CosmMiniRadar({ dimensions, size = 80 }) {
  const dims = [
    { key: 'rights' }, { key: 'research' }, { key: 'budget' },
    { key: 'package' }, { key: 'deliverables' }, { key: 'pitch' },
  ]
  const cx = size / 2, cy = size / 2, r = size * 0.36
  const angleStep = (Math.PI * 2) / 6

  const getPoint = (i, val) => {
    const angle = angleStep * i - Math.PI / 2
    const dist = (val / 100) * r
    return { x: cx + dist * Math.cos(angle), y: cy + dist * Math.sin(angle) }
  }

  const total = dimensions ? Math.min(
    dimensions.rights || 0, dimensions.research || 0, dimensions.budget || 0,
    dimensions.package || 0, dimensions.deliverables || 0, dimensions.pitch || 0
  ) : 0

  return (
    <svg viewBox={`0 0 ${size} ${size}`} className="dp-cosm-mini">
      <polygon
        points={dims.map((_, i) => {
          const p = getPoint(i, 100)
          return `${p.x},${p.y}`
        }).join(' ')}
        fill="none" stroke="#e0e0e0" strokeWidth="0.5"
      />
      {dimensions && (
        <polygon
          points={dims.map((d, i) => {
            const p = getPoint(i, dimensions[d.key] || 0)
            return `${p.x},${p.y}`
          }).join(' ')}
          fill="rgba(0,0,0,0.06)" stroke="#1a1a1a" strokeWidth="1"
        />
      )}
      <text x={cx} y={cy + 3} textAnchor="middle" fill="#1a1a1a" fontSize="12" fontWeight="600" fontFamily="Georgia, serif">
        {total.toFixed(0)}
      </text>
    </svg>
  )
}

export default function DomesIndex() {
  const [productions, setProductions] = useState([])
  const [loading, setLoading] = useState(true)
  const [sort, setSort] = useState('date')

  useEffect(() => {
    fetch(`/api/portfolio/domes?sort=${sort}`)
      .then(r => r.json())
      .then(data => {
        setProductions(data.productions || [])
        setLoading(false)
      })
      .catch(() => setLoading(false))
  }, [sort])

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

  return (
    <div className="dp-page">
      <header className="dp-header">
        <div className="dp-header-inner">
          <div className="dp-brand">
            <h1 className="dp-wordmark">DOMES</h1>
            <p className="dp-tagline">Build a dome around one person using the entire US government.</p>
          </div>
          <div className="dp-header-meta">
            <span className="dp-count">{productions.length} Production{productions.length !== 1 ? 's' : ''}</span>
          </div>
        </div>
      </header>

      <div className="dp-toolbar">
        <div className="dp-toolbar-inner">
          <span className="dp-toolbar-label">Sort by</span>
          <button className={sort === 'date' ? 'active' : ''} onClick={() => setSort('date')}>Date</button>
          <button className={sort === 'cosm' ? 'active' : ''} onClick={() => setSort('cosm')}>Cosm Score</button>
          <button className={sort === 'subject' ? 'active' : ''} onClick={() => setSort('subject')}>Subject</button>
        </div>
      </div>

      <main className="dp-grid-wrap">
        {productions.length === 0 ? (
          <div className="dp-empty">
            <p>No completed dome productions yet.</p>
            <p className="dp-empty-sub">Complete a DOMES production in the game engine to publish it here.</p>
          </div>
        ) : (
          <div className="dp-grid">
            {productions.map(prod => (
              <Link
                key={prod.production_id}
                to={`/domes/${prod.production_id}`}
                className="dp-card"
              >
                <div className="dp-card-top">
                  <CosmMiniRadar dimensions={prod.cosm} />
                  <div className="dp-card-title-block">
                    <h2 className="dp-card-title">The {prod.subject} Dome</h2>
                    <p className="dp-card-producer">{prod.player_name}</p>
                  </div>
                </div>
                <div className="dp-card-stats">
                  <div className="dp-card-stat">
                    <span className="dp-cs-val">{prod.cosm_total?.toFixed(1) || '0'}</span>
                    <span className="dp-cs-label">Cosm</span>
                  </div>
                  <div className="dp-card-stat">
                    <span className="dp-cs-val">{prod.rights_count || 0}</span>
                    <span className="dp-cs-label">Provisions</span>
                  </div>
                  <div className="dp-card-stat">
                    <span className="dp-cs-val">{prod.system_count || 0}</span>
                    <span className="dp-cs-label">Systems</span>
                  </div>
                  <div className="dp-card-stat">
                    <span className="dp-cs-val">{prod.ip_count || 0}</span>
                    <span className="dp-cs-label">IP Outputs</span>
                  </div>
                </div>
                {prod.dome_bond?.face_value > 0 && (
                  <div className="dp-card-bond">
                    <span className="dp-cb-rating">{prod.dome_bond.rating}</span>
                    <span className="dp-cb-val">${prod.dome_bond.face_value?.toLocaleString()}</span>
                    <span className="dp-cb-label">Dome Bond</span>
                  </div>
                )}
                <div className="dp-card-date">
                  {prod.completed_at ? new Date(prod.completed_at).toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' }) : ''}
                </div>
              </Link>
            ))}
          </div>
        )}
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
