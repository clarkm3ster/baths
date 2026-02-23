import { useState, useEffect } from 'react'

export default function Roster({ onOpenTalent }) {
  const [roster, setRoster] = useState([])
  const [search, setSearch] = useState('')
  const [domainFilter, setDomainFilter] = useState('')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const params = new URLSearchParams()
    if (search) params.set('search', search)
    if (domainFilter) params.set('domain', domainFilter)
    fetch(`/api/roster?${params}`)
      .then(r => r.json())
      .then(data => { setRoster(data.roster); setLoading(false) })
      .catch(() => setLoading(false))
  }, [search, domainFilter])

  // Extract all unique domains from roster
  const allDomains = [...new Set(roster.flatMap(t => t.domains_of_practice))]

  if (loading) return <div className="loading">Loading roster...</div>

  return (
    <div>
      <div className="page-header">
        <h2>Talent Roster</h2>
        <p>Every person profiled by their practice, body of work, and what they bring to a production table.</p>
      </div>

      <div className="search-bar">
        <input
          className="search-input"
          type="text"
          placeholder="Search by name, practice, domain, or keyword..."
          value={search}
          onChange={e => setSearch(e.target.value)}
        />
        <button
          className={`filter-btn ${domainFilter === '' ? 'active' : ''}`}
          onClick={() => setDomainFilter('')}
        >
          All
        </button>
        {allDomains.slice(0, 6).map(d => (
          <button
            key={d}
            className={`filter-btn ${domainFilter === d ? 'active' : ''}`}
            onClick={() => setDomainFilter(domainFilter === d ? '' : d)}
          >
            {d.split(' ').slice(0, 2).join(' ')}
          </button>
        ))}
      </div>

      <div className="grid-2">
        {roster.map(talent => (
          <div
            key={talent.talent_id}
            className="card card-clickable talent-card"
            onClick={() => onOpenTalent(talent.talent_id)}
          >
            <div className="talent-card-header">
              <div>
                <div className="talent-name">{talent.name}</div>
                <div className="talent-practice">{talent.domains_of_practice.slice(0, 2).join(' / ')}</div>
              </div>
              <span className={`tag ${talent.availability === 'available' ? 'available' : 'on-production'}`}>
                {talent.availability === 'available' ? 'Available' : talent.availability.replace('_', ' ')}
              </span>
            </div>
            <p className="talent-bio">{talent.bio.slice(0, 180)}...</p>
            <div className="talent-card-footer">
              <div className="tags">
                {talent.resonance_tags.slice(0, 5).map(tag => (
                  <span key={tag} className="tag">{tag}</span>
                ))}
              </div>
              <div className="talent-scores">
                {talent.total_cosm > 0 && <span className="score-value cosm">{talent.total_cosm.toFixed(0)} Cosm</span>}
                {talent.total_chron > 0 && <span className="score-value chron">{talent.total_chron.toFixed(0)} Chron</span>}
                {talent.productions_completed.length > 0 && (
                  <span className="talent-prod-count">{talent.productions_completed.length} prod.</span>
                )}
              </div>
            </div>
          </div>
        ))}
      </div>

      {roster.length === 0 && (
        <div className="empty-state">
          <h3>No practitioners found</h3>
          <p>Try adjusting your search or filters.</p>
        </div>
      )}

      <style>{`
        .talent-card-header {
          display: flex;
          justify-content: space-between;
          align-items: flex-start;
          margin-bottom: 0.75rem;
        }
        .talent-name {
          font-family: 'Playfair Display', serif;
          font-size: 1.15rem;
          font-weight: 600;
          margin-bottom: 0.15rem;
        }
        .talent-practice {
          font-size: 0.8rem;
          color: var(--accent-dark);
          font-weight: 500;
          text-transform: uppercase;
          letter-spacing: 0.04em;
        }
        .talent-bio {
          font-size: 0.9rem;
          color: var(--ink-light);
          line-height: 1.5;
          margin-bottom: 0.75rem;
        }
        .talent-card-footer {
          display: flex;
          justify-content: space-between;
          align-items: flex-end;
          gap: 0.5rem;
        }
        .talent-scores {
          display: flex;
          gap: 0.5rem;
          align-items: center;
          font-size: 0.8rem;
          flex-shrink: 0;
        }
        .talent-prod-count {
          font-size: 0.75rem;
          color: var(--ink-lighter);
          font-weight: 500;
        }
      `}</style>
    </div>
  )
}
