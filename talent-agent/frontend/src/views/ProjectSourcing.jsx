import { useState, useEffect } from 'react'

export default function ProjectSourcing({ onOpenProject }) {
  const [projects, setProjects] = useState([])
  const [filter, setFilter] = useState('')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const params = new URLSearchParams()
    if (filter) params.set('game_type', filter)
    params.set('status', 'sourced')
    fetch(`/api/projects?${params}`)
      .then(r => r.json())
      .then(data => { setProjects(data.projects); setLoading(false) })
      .catch(() => setLoading(false))
  }, [filter])

  if (loading) return <div className="loading">Loading sourced projects...</div>

  const domesProjects = projects.filter(p => p.game_type === 'domes')
  const spheresProjects = projects.filter(p => p.game_type === 'spheres')

  return (
    <div>
      <div className="page-header">
        <h2>Project Sourcing</h2>
        <p>Characters sourced from documented material for domes. Parcels sourced from real data for spheres. Each brief describes the production challenge.</p>
      </div>

      <div className="search-bar">
        <button className={`filter-btn ${filter === '' ? 'active' : ''}`} onClick={() => setFilter('')}>All</button>
        <button className={`filter-btn ${filter === 'domes' ? 'active' : ''}`} onClick={() => setFilter('domes')}>Domes Characters</button>
        <button className={`filter-btn ${filter === 'spheres' ? 'active' : ''}`} onClick={() => setFilter('spheres')}>Spheres Parcels</button>
      </div>

      {/* DOMES — Character Briefs */}
      {(filter === '' || filter === 'domes') && domesProjects.length > 0 && (
        <div className="sourcing-section">
          <div className="sourcing-section-header">
            <span className="badge badge-domes">DOMES</span>
            <h3>Character Briefs</h3>
            <p>Sourced from books, films, journalism, and case studies</p>
          </div>
          <div className="sourcing-grid">
            {domesProjects.map(p => (
              <div key={p.project_id} className="card card-clickable source-card" onClick={() => onOpenProject(p.project_id)}>
                <div className="source-card-header">
                  <h4 className="source-title">{p.title}</h4>
                  <span className="badge badge-domes">DOMES</span>
                </div>
                {p.character && (
                  <>
                    <div className="source-meta">
                      <span className="source-name">{p.character.name}</span>
                      <span className="source-from">from <em>{p.character.source}</em></span>
                    </div>
                    <p className="source-situation">{p.character.situation.slice(0, 180)}...</p>
                    <div className="source-challenge">
                      <div className="challenge-label">Production Challenge</div>
                      <p>{p.character.production_challenge.slice(0, 150)}...</p>
                    </div>
                    <div className="source-tags">
                      {p.character.key_systems.slice(0, 4).map(s => (
                        <span key={s} className="tag">{s}</span>
                      ))}
                    </div>
                    <div className="source-flourishing">
                      {p.character.flourishing_dimensions.map(d => (
                        <span key={d} className="flourishing-dim">{d}</span>
                      ))}
                    </div>
                  </>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* SPHERES — Parcel Briefs */}
      {(filter === '' || filter === 'spheres') && spheresProjects.length > 0 && (
        <div className="sourcing-section">
          <div className="sourcing-section-header">
            <span className="badge badge-spheres">SPHERES</span>
            <h3>Parcel Briefs</h3>
            <p>Real parcels from Philadelphia with documented activation opportunities</p>
          </div>
          <div className="sourcing-grid">
            {spheresProjects.map(p => (
              <div key={p.project_id} className="card card-clickable source-card" onClick={() => onOpenProject(p.project_id)}>
                <div className="source-card-header">
                  <h4 className="source-title">{p.title}</h4>
                  <span className="badge badge-spheres">SPHERES</span>
                </div>
                {p.parcel && (
                  <>
                    <div className="parcel-meta">
                      <div className="parcel-address">{p.parcel.address}</div>
                      <div className="parcel-details">
                        <span>{p.parcel.neighborhood}</span>
                        <span className="parcel-sep">/</span>
                        <span>{p.parcel.zoning}</span>
                        <span className="parcel-sep">/</span>
                        <span className="mono">{p.parcel.lot_size_sqft.toLocaleString()} sqft</span>
                      </div>
                    </div>
                    <p className="source-history">{p.parcel.history.slice(0, 160)}...</p>
                    <div className="source-challenge">
                      <div className="challenge-label">Activation Opportunity</div>
                      <p>{p.parcel.opportunity.slice(0, 150)}...</p>
                    </div>
                    <div className="source-tags">
                      {p.parcel.constraints.map((c, i) => (
                        <span key={i} className="tag">{c.slice(0, 30)}</span>
                      ))}
                    </div>
                  </>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      <style>{`
        .sourcing-section {
          margin-bottom: 3rem;
        }
        .sourcing-section-header {
          display: flex;
          align-items: center;
          gap: 0.75rem;
          margin-bottom: 1.25rem;
          flex-wrap: wrap;
        }
        .sourcing-section-header h3 {
          font-family: 'Inter', sans-serif;
          font-size: 1rem;
          font-weight: 600;
        }
        .sourcing-section-header p {
          width: 100%;
          font-size: 0.85rem;
          color: var(--ink-lighter);
          margin-top: 0.25rem;
        }
        .sourcing-grid {
          display: grid;
          grid-template-columns: repeat(auto-fill, minmax(380px, 1fr));
          gap: 1.25rem;
        }
        .source-card {
          display: flex;
          flex-direction: column;
          gap: 0.75rem;
        }
        .source-card-header {
          display: flex;
          justify-content: space-between;
          align-items: flex-start;
        }
        .source-title {
          font-family: 'Playfair Display', serif;
          font-size: 1.1rem;
          font-weight: 600;
        }
        .source-meta {
          display: flex;
          flex-direction: column;
          gap: 0.15rem;
        }
        .source-name {
          font-weight: 600;
          font-size: 0.95rem;
        }
        .source-from {
          font-size: 0.8rem;
          color: var(--ink-lighter);
        }
        .source-situation, .source-history {
          font-size: 0.9rem;
          color: var(--ink-light);
          line-height: 1.5;
        }
        .source-challenge {
          padding: 0.75rem;
          background: var(--paper-warm);
          border-radius: var(--radius-sm);
        }
        .challenge-label {
          font-size: 0.7rem;
          font-weight: 600;
          text-transform: uppercase;
          letter-spacing: 0.06em;
          color: var(--accent-dark);
          margin-bottom: 0.25rem;
        }
        .source-challenge p {
          font-size: 0.85rem;
          color: var(--ink-light);
          line-height: 1.5;
        }
        .source-tags {
          display: flex;
          flex-wrap: wrap;
          gap: 0.35rem;
        }
        .parcel-meta {
          display: flex;
          flex-direction: column;
          gap: 0.2rem;
        }
        .parcel-address {
          font-weight: 600;
          font-size: 0.95rem;
        }
        .parcel-details {
          display: flex;
          align-items: center;
          gap: 0.35rem;
          font-size: 0.8rem;
          color: var(--ink-lighter);
        }
        .parcel-sep {
          color: var(--border);
        }
        .source-flourishing {
          display: flex;
          flex-wrap: wrap;
          gap: 0.35rem;
        }
        .flourishing-dim {
          font-size: 0.7rem;
          padding: 0.15rem 0.45rem;
          background: var(--domes-bg);
          color: var(--domes-color);
          border-radius: 20px;
          font-weight: 500;
        }
      `}</style>
    </div>
  )
}
