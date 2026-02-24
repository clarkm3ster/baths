import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'

const COSM_DIMS = ['rights', 'research', 'budget', 'package', 'deliverables', 'pitch']

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
          Each dome is a support structure built around a real person
          from a real case study — designed by a team of practitioners
          drawing on real bodies of work.
        </p>
      </div>

      <div className="sort-bar">
        <span>Sort by</span>
        {[
          { key: 'score', label: 'Cosm Score' },
          { key: 'title', label: 'Title' },
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
                <span>{p.character_name}</span>
                <span>{p.source}</span>
                <span>Team of {p.team_size}</span>
                <span>{p.ip_count} IP</span>
              </div>
            </div>

            <div className="prod-card-dims">
              {COSM_DIMS.map(d => (
                <div
                  key={d}
                  className="mini-bar"
                  style={{ height: `${((p.dimensions?.[d] || 0) / 100) * 32}px` }}
                  title={`${d}: ${(p.dimensions?.[d] || 0).toFixed(1)}`}
                />
              ))}
            </div>

            <div className="prod-card-score">
              <div className="cosm-score">{(p.cosm_total || 0).toFixed(1)}</div>
              <div className="cosm-label">Cosm</div>
            </div>
          </div>
        ))}
      </div>

      {productions.length === 0 && (
        <p style={{ textAlign: 'center', padding: '40px 0', color: 'var(--text-tertiary)' }}>
          No completed DOMES productions yet. Run a production through the Talent Agent to see it here.
        </p>
      )}
    </div>
  )
}
