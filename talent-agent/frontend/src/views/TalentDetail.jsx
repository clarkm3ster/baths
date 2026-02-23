import { useState, useEffect } from 'react'

export default function TalentDetail({ talentId, onBack, onOpenProject }) {
  const [talent, setTalent] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetch(`/api/roster/${talentId}`)
      .then(r => r.json())
      .then(data => { setTalent(data); setLoading(false) })
      .catch(() => setLoading(false))
  }, [talentId])

  if (loading) return <div className="loading">Loading profile...</div>
  if (!talent) return <div className="empty-state"><h3>Talent not found</h3></div>

  return (
    <div className="detail-page">
      <button className="btn btn-back" onClick={onBack}>&larr; Back to Roster</button>

      <div className="detail-header">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
          <div>
            <h2>{talent.name}</h2>
            <div className="talent-detail-practice">
              {talent.domains_of_practice.join(' / ')}
            </div>
          </div>
          <span className={`tag ${talent.availability === 'available' ? 'available' : 'on-production'}`}>
            {talent.availability === 'available' ? 'Available' : talent.availability.replace('_', ' ')}
          </span>
        </div>
      </div>

      <div className="detail-section">
        <p className="detail-bio">{talent.bio}</p>
      </div>

      {talent.approach && (
        <div className="detail-section">
          <h3>Approach</h3>
          <div className="approach-block">
            <p>{talent.approach}</p>
          </div>
        </div>
      )}

      <div className="detail-section">
        <h3>Body of Work</h3>
        {talent.body_of_work.map((w, i) => (
          <div key={i} className="work-item">
            <div className="work-item-title">{w.title}</div>
            <div className="work-item-meta">
              {w.year && <span>{w.year}</span>}
              {w.medium && <span> &middot; {w.medium}</span>}
            </div>
            <div className="work-item-desc">{w.description}</div>
          </div>
        ))}
      </div>

      <div className="detail-section">
        <h3>Capabilities</h3>
        <div className="tags" style={{ gap: '0.5rem' }}>
          {talent.capabilities.map((c, i) => (
            <span key={i} className="tag" style={{ fontSize: '0.85rem', padding: '0.25rem 0.65rem' }}>{c}</span>
          ))}
        </div>
      </div>

      <div className="detail-section">
        <h3>Resonance Tags</h3>
        <div className="tags">
          {talent.resonance_tags.map(tag => (
            <span key={tag} className="tag">{tag}</span>
          ))}
        </div>
      </div>

      <div className="detail-section">
        <h3>Production History</h3>
        <div className="talent-detail-scores">
          <div className="td-score-card">
            <div className="td-score-label">Cosm Earned</div>
            <div className="td-score-value cosm">{talent.total_cosm.toFixed(1)}</div>
          </div>
          <div className="td-score-card">
            <div className="td-score-label">Chron Earned</div>
            <div className="td-score-value chron">{talent.total_chron.toFixed(1)}</div>
          </div>
          <div className="td-score-card">
            <div className="td-score-label">Productions</div>
            <div className="td-score-value">{talent.productions_completed.length}</div>
          </div>
        </div>
        {talent.productions_completed.length === 0 && (
          <p style={{ color: 'var(--ink-lighter)', marginTop: '0.5rem', fontSize: '0.9rem' }}>
            No productions completed yet. Available for team assembly.
          </p>
        )}
      </div>

      <style>{`
        .talent-detail-practice {
          font-size: 0.9rem;
          color: var(--accent-dark);
          font-weight: 500;
          text-transform: uppercase;
          letter-spacing: 0.04em;
          margin-top: 0.25rem;
        }
        .approach-block {
          padding: 1.25rem;
          background: var(--paper-warm);
          border-radius: var(--radius-md);
          border-left: 3px solid var(--accent);
        }
        .approach-block p {
          font-size: 1rem;
          line-height: 1.7;
          color: var(--ink-light);
          font-style: italic;
        }
        .talent-detail-scores {
          display: flex;
          gap: 1rem;
        }
        .td-score-card {
          padding: 1rem 1.5rem;
          background: white;
          border: 1px solid var(--border);
          border-radius: var(--radius-md);
          text-align: center;
        }
        .td-score-label {
          font-size: 0.7rem;
          font-weight: 600;
          text-transform: uppercase;
          letter-spacing: 0.08em;
          color: var(--ink-lighter);
          margin-bottom: 0.25rem;
        }
        .td-score-value {
          font-family: 'JetBrains Mono', monospace;
          font-size: 1.5rem;
          font-weight: 600;
        }
        .td-score-value.cosm { color: var(--domes-color); }
        .td-score-value.chron { color: var(--spheres-color); }
      `}</style>
    </div>
  )
}
