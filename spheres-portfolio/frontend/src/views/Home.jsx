import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'

const CHRON_DIMS = ['unlock', 'access', 'permanence', 'catalyst', 'policy']

export default function Home() {
  const [productions, setProductions] = useState([])
  const [sort, setSort] = useState('score')
  const [loading, setLoading] = useState(true)
  const navigate = useNavigate()

  useEffect(() => {
    fetch(`/api/productions?sort=${sort}`)
      .then(r => r.json())
      .then(data => {
        setProductions(data.productions || [])
        setLoading(false)
      })
      .catch(() => setLoading(false))
  }, [sort])

  if (loading) return <div className="loading">Loading productions...</div>

  return (
    <div>
      <div className="home-hero">
        <h1>Completed Productions</h1>
        <p>
          Each sphere is an activation strategy for a real vacant Philadelphia
          parcel — designed by a team of practitioners drawing on real
          bodies of work.
        </p>
      </div>

      <div className="sort-bar">
        <span>Sort by</span>
        {[
          { key: 'score', label: 'Chron Score' },
          { key: 'title', label: 'Title' },
          { key: 'neighborhood', label: 'Neighborhood' },
          { key: 'ip', label: 'IP Generated' },
        ].map(s => (
          <button
            key={s.key}
            className={`sort-btn ${sort === s.key ? 'active' : ''}`}
            onClick={() => setSort(s.key)}
          >
            {s.label}
          </button>
        ))}
      </div>

      <p className="prod-count">{productions.length} production{productions.length !== 1 ? 's' : ''}</p>

      <div className="prod-grid">
        {productions.map(p => (
          <div
            key={p.project_id}
            className="prod-card"
            onClick={() => navigate(`/production/${p.project_id}`)}
          >
            <div className="prod-card-main">
              <h3>{p.title}</h3>
              <div className="prod-card-meta">
                <span>{p.address}</span>
                <span>{p.neighborhood}</span>
                <span>{p.zoning}</span>
                <span>Team of {p.team_size}</span>
              </div>
            </div>

            <div className="prod-card-dims">
              {CHRON_DIMS.map(d => (
                <div
                  key={d}
                  className="mini-bar"
                  style={{ height: `${((p.dimensions?.[d] || 0) / 100) * 32}px` }}
                  title={`${d}: ${(p.dimensions?.[d] || 0).toFixed(1)}`}
                />
              ))}
            </div>

            <div className="prod-card-score">
              <div className="chron-score">{(p.chron_total || 0).toFixed(1)}</div>
              <div className="chron-label">Chron</div>
            </div>
          </div>
        ))}
      </div>

      {productions.length === 0 && (
        <p style={{ textAlign: 'center', padding: '40px 0', color: 'var(--text-tertiary)' }}>
          No completed SPHERES productions yet. Run a production through the Talent Agent to see it here.
        </p>
      )}
    </div>
  )
}
