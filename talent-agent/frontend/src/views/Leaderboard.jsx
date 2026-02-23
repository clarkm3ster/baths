import { useState, useEffect } from 'react'

export default function Leaderboard({ onOpenTalent, onOpenPrincipal }) {
  const [entries, setEntries] = useState([])
  const [sortBy, setSortBy] = useState('flourishing')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetch(`/api/leaderboard?sort_by=${sortBy}`)
      .then(r => r.json())
      .then(data => { setEntries(data.leaderboard); setLoading(false) })
      .catch(() => setLoading(false))
  }, [sortBy])

  if (loading) return <div className="loading">Loading leaderboard...</div>

  return (
    <div>
      <div className="page-header">
        <h2>Leaderboard</h2>
        <p>Individual and team Cosm/Chron scores, IP output by domain, productions completed.</p>
      </div>

      <div className="search-bar">
        <button className={`filter-btn ${sortBy === 'flourishing' ? 'active' : ''}`} onClick={() => setSortBy('flourishing')}>Flourishing</button>
        <button className={`filter-btn ${sortBy === 'cosm' ? 'active' : ''}`} onClick={() => setSortBy('cosm')}>Cosm</button>
        <button className={`filter-btn ${sortBy === 'chron' ? 'active' : ''}`} onClick={() => setSortBy('chron')}>Chron</button>
        <button className={`filter-btn ${sortBy === 'productions' ? 'active' : ''}`} onClick={() => setSortBy('productions')}>Productions</button>
        <button className={`filter-btn ${sortBy === 'ip' ? 'active' : ''}`} onClick={() => setSortBy('ip')}>IP Output</button>
      </div>

      <div className="leaderboard-table">
        <div className="lb-header">
          <span className="lb-rank">#</span>
          <span className="lb-name-col">Name</span>
          <span className="lb-role-col">Role</span>
          <span className="lb-num-col">Productions</span>
          <span className="lb-num-col">Cosm</span>
          <span className="lb-num-col">Chron</span>
          <span className="lb-num-col">Flourishing</span>
          <span className="lb-num-col">IP</span>
        </div>
        {entries.map((entry, i) => (
          <div
            key={entry.id}
            className="lb-row card-clickable"
            onClick={() => entry.role === 'talent' ? onOpenTalent(entry.id) : onOpenPrincipal(entry.id)}
          >
            <span className="lb-rank">{i + 1}</span>
            <span className="lb-name-col">
              <span className="lb-name">{entry.name}</span>
              {entry.domains_of_practice?.length > 0 && (
                <span className="lb-practice">{entry.domains_of_practice[0]}</span>
              )}
            </span>
            <span className="lb-role-col">
              <span className={`badge ${entry.role === 'principal' ? 'badge-principal' : 'badge-talent'}`}>
                {entry.role}
              </span>
            </span>
            <span className="lb-num-col mono">{entry.productions_completed}</span>
            <span className="lb-num-col mono score-value cosm">{entry.total_cosm.toFixed(1)}</span>
            <span className="lb-num-col mono score-value chron">{entry.total_chron.toFixed(1)}</span>
            <span className="lb-num-col mono lb-flourishing">{entry.flourishing.toFixed(1)}</span>
            <span className="lb-num-col">
              <span className="mono">{entry.ip_count}</span>
              {entry.ip_domains?.length > 0 && (
                <span className="lb-ip-domains">{entry.ip_domains.length} domains</span>
              )}
            </span>
          </div>
        ))}
      </div>

      {entries.length === 0 && (
        <div className="empty-state">
          <h3>No entries yet</h3>
          <p>Complete productions to build scores and climb the board.</p>
        </div>
      )}

      <style>{`
        .leaderboard-table {
          border: 1px solid var(--border);
          border-radius: var(--radius-md);
          overflow: hidden;
          background: white;
        }
        .lb-header {
          display: flex;
          align-items: center;
          padding: 0.75rem 1.25rem;
          background: var(--paper-warm);
          border-bottom: 1px solid var(--border);
          font-size: 0.7rem;
          font-weight: 600;
          text-transform: uppercase;
          letter-spacing: 0.08em;
          color: var(--ink-lighter);
        }
        .lb-row {
          display: flex;
          align-items: center;
          padding: 0.75rem 1.25rem;
          border-bottom: 1px solid var(--border-light);
          transition: background 0.15s;
          cursor: pointer;
        }
        .lb-row:last-child { border-bottom: none; }
        .lb-row:hover { background: var(--paper-warm); }
        .lb-rank {
          width: 40px;
          flex-shrink: 0;
          font-family: 'JetBrains Mono', monospace;
          font-weight: 500;
          color: var(--ink-lighter);
          font-size: 0.85rem;
        }
        .lb-name-col {
          flex: 2;
          display: flex;
          flex-direction: column;
          gap: 0.1rem;
          min-width: 0;
        }
        .lb-name {
          font-family: 'Playfair Display', serif;
          font-weight: 600;
          font-size: 0.95rem;
        }
        .lb-practice {
          font-size: 0.75rem;
          color: var(--ink-lighter);
          white-space: nowrap;
          overflow: hidden;
          text-overflow: ellipsis;
        }
        .lb-role-col {
          width: 100px;
          flex-shrink: 0;
        }
        .lb-num-col {
          width: 100px;
          flex-shrink: 0;
          text-align: right;
          font-size: 0.85rem;
          display: flex;
          flex-direction: column;
          align-items: flex-end;
          gap: 0.1rem;
        }
        .lb-flourishing {
          font-weight: 600;
          color: var(--accent-dark);
        }
        .lb-ip-domains {
          font-size: 0.65rem;
          color: var(--ink-lighter);
          font-family: 'Inter', sans-serif;
        }
        .badge-principal {
          background: var(--ink);
          color: white;
        }
        .badge-talent {
          background: var(--paper-warm);
          color: var(--ink-lighter);
        }
        .mono {
          font-family: 'JetBrains Mono', monospace;
        }
      `}</style>
    </div>
  )
}
