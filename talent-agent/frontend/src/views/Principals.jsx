import { useState, useEffect } from 'react'

export default function Principals({ onOpenPrincipal }) {
  const [principals, setPrincipals] = useState([])
  const [filter, setFilter] = useState('')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const params = filter ? `?game_type=${filter}` : ''
    fetch(`/api/principals${params}`)
      .then(r => r.json())
      .then(data => { setPrincipals(data.principals); setLoading(false) })
      .catch(() => setLoading(false))
  }, [filter])

  if (loading) return <div className="loading">Loading principals...</div>

  return (
    <div>
      <div className="page-header">
        <h2>Production Principals</h2>
        <p>Top-tier production leaders whose vision shapes how a dome gets designed or a sphere comes alive. The principal's name goes on the production.</p>
      </div>

      <div className="search-bar">
        <button className={`filter-btn ${filter === '' ? 'active' : ''}`} onClick={() => setFilter('')}>All</button>
        <button className={`filter-btn ${filter === 'domes' ? 'active' : ''}`} onClick={() => setFilter('domes')}>Domes</button>
        <button className={`filter-btn ${filter === 'spheres' ? 'active' : ''}`} onClick={() => setFilter('spheres')}>Spheres</button>
      </div>

      <div className="principals-grid">
        {principals.map(p => (
          <div
            key={p.principal_id}
            className="card card-clickable principal-card"
            onClick={() => onOpenPrincipal(p.principal_id)}
          >
            <div className="principal-header">
              <div className="principal-name-row">
                <h3 className="principal-name">{p.name}</h3>
                {p.game_type && (
                  <span className={`badge badge-${p.game_type}`}>
                    {p.game_type.toUpperCase()}
                  </span>
                )}
              </div>
              <p className="principal-bio">{p.bio}</p>
            </div>

            <div className="principal-vision">
              <div className="vision-label">VISION</div>
              <p>{p.vision.slice(0, 200)}...</p>
            </div>

            <div className="principal-works">
              {p.body_of_work.slice(0, 3).map((w, i) => (
                <div key={i} className="principal-work-pill">
                  <span className="pw-title">{w.title}</span>
                  {w.year && <span className="pw-year">{w.year}</span>}
                </div>
              ))}
            </div>

            {p.signature_style && (
              <div className="principal-signature">
                <em>"{p.signature_style.slice(0, 120)}"</em>
              </div>
            )}

            <div className="principal-footer">
              <span className="principal-prods">{p.productions_led.length} productions</span>
              {p.total_cosm > 0 && <span className="score-value cosm">{p.total_cosm.toFixed(0)} Cosm</span>}
              {p.total_chron > 0 && <span className="score-value chron">{p.total_chron.toFixed(0)} Chron</span>}
            </div>
          </div>
        ))}
      </div>

      <style>{`
        .principals-grid {
          display: grid;
          grid-template-columns: repeat(auto-fill, minmax(420px, 1fr));
          gap: 1.25rem;
        }
        .principal-card {
          display: flex;
          flex-direction: column;
          gap: 1rem;
        }
        .principal-name-row {
          display: flex;
          align-items: center;
          gap: 0.75rem;
          margin-bottom: 0.5rem;
        }
        .principal-name {
          font-family: 'Playfair Display', serif;
          font-size: 1.3rem;
          font-weight: 600;
        }
        .principal-bio {
          font-size: 0.95rem;
          color: var(--ink-light);
          line-height: 1.5;
        }
        .principal-vision {
          padding: 1rem;
          background: var(--paper-warm);
          border-radius: var(--radius-sm);
        }
        .vision-label {
          font-size: 0.7rem;
          font-weight: 600;
          letter-spacing: 0.08em;
          text-transform: uppercase;
          color: var(--accent-dark);
          margin-bottom: 0.35rem;
        }
        .principal-vision p {
          font-size: 0.9rem;
          color: var(--ink-light);
          line-height: 1.5;
          font-style: italic;
        }
        .principal-works {
          display: flex;
          flex-wrap: wrap;
          gap: 0.5rem;
        }
        .principal-work-pill {
          display: flex;
          align-items: center;
          gap: 0.35rem;
          padding: 0.3rem 0.65rem;
          background: white;
          border: 1px solid var(--border);
          border-radius: 20px;
          font-size: 0.8rem;
        }
        .pw-title {
          font-weight: 500;
          color: var(--ink-light);
        }
        .pw-year {
          color: var(--ink-lighter);
          font-family: 'JetBrains Mono', monospace;
          font-size: 0.7rem;
        }
        .principal-signature {
          font-size: 0.85rem;
          color: var(--ink-lighter);
          padding-left: 0.75rem;
          border-left: 2px solid var(--accent-light);
        }
        .principal-footer {
          display: flex;
          align-items: center;
          gap: 1rem;
          padding-top: 0.5rem;
          border-top: 1px solid var(--border-light);
        }
        .principal-prods {
          font-size: 0.8rem;
          color: var(--ink-lighter);
          font-weight: 500;
        }
      `}</style>
    </div>
  )
}
