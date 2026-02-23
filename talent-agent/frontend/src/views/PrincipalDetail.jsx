import { useState, useEffect } from 'react'

export default function PrincipalDetail({ principalId, onBack, onOpenProject }) {
  const [principal, setPrincipal] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetch(`/api/principals/${principalId}`)
      .then(r => r.json())
      .then(data => { setPrincipal(data); setLoading(false) })
      .catch(() => setLoading(false))
  }, [principalId])

  if (loading) return <div className="loading">Loading principal...</div>
  if (!principal) return <div className="empty-state"><h3>Principal not found</h3></div>

  return (
    <div className="detail-page">
      <button className="btn btn-back" onClick={onBack}>&larr; Back to Principals</button>

      <div className="detail-header">
        <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
          <h2>{principal.name}</h2>
          {principal.game_type && (
            <span className={`badge badge-${principal.game_type}`} style={{ fontSize: '0.8rem', padding: '0.3rem 0.8rem' }}>
              {principal.game_type.toUpperCase()}
            </span>
          )}
        </div>
      </div>

      <div className="detail-section">
        <p className="detail-bio">{principal.bio}</p>
      </div>

      <div className="detail-section">
        <h3>Vision</h3>
        <div className="principal-vision-block">
          <p>{principal.vision}</p>
        </div>
      </div>

      {principal.signature_style && (
        <div className="detail-section">
          <h3>Signature Style</h3>
          <div className="signature-block">
            <p>"{principal.signature_style}"</p>
          </div>
        </div>
      )}

      <div className="detail-section">
        <h3>Body of Work</h3>
        {principal.body_of_work.map((w, i) => (
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
        <h3>Production Record</h3>
        <div className="principal-stats">
          <div className="td-score-card">
            <div className="td-score-label">Productions Led</div>
            <div className="td-score-value">{principal.productions_led.length}</div>
          </div>
          <div className="td-score-card">
            <div className="td-score-label">Total Cosm</div>
            <div className="td-score-value cosm">{principal.total_cosm.toFixed(1)}</div>
          </div>
          <div className="td-score-card">
            <div className="td-score-label">Total Chron</div>
            <div className="td-score-value chron">{principal.total_chron.toFixed(1)}</div>
          </div>
        </div>
        {principal.productions_led.length === 0 && (
          <p style={{ color: 'var(--ink-lighter)', marginTop: '0.75rem', fontSize: '0.9rem' }}>
            No productions led yet. Ready to attach to a project.
          </p>
        )}
      </div>

      <div className="detail-section">
        <h3>What a {principal.name} {principal.game_type === 'spheres' ? 'Sphere' : 'Dome'} Looks Like</h3>
        <div className="what-it-looks-like">
          <p>
            {principal.game_type === 'domes'
              ? `A ${principal.name} Dome — where ${principal.signature_style?.toLowerCase() || principal.vision.slice(0, 80).toLowerCase()}. The principal's name goes on the production. Their reputation attracts talent to the roster. Their completed productions on domes.cc become portfolio pieces that attract other principals.`
              : `A ${principal.name} Sphere — where ${principal.signature_style?.toLowerCase() || principal.vision.slice(0, 80).toLowerCase()}. The principal's name goes on the production. Their reputation attracts talent to the roster. Their completed productions on spheres.land become portfolio pieces that attract other principals.`
            }
          </p>
        </div>
      </div>

      <style>{`
        .principal-vision-block {
          padding: 1.5rem;
          background: var(--ink);
          color: white;
          border-radius: var(--radius-md);
        }
        .principal-vision-block p {
          font-size: 1.05rem;
          line-height: 1.7;
          font-style: italic;
        }
        .signature-block {
          padding: 1.25rem;
          background: var(--paper-warm);
          border-left: 3px solid var(--accent);
          border-radius: var(--radius-sm);
        }
        .signature-block p {
          font-size: 1rem;
          line-height: 1.6;
          color: var(--ink-light);
          font-style: italic;
        }
        .principal-stats {
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
        .what-it-looks-like {
          padding: 1.25rem;
          background: var(--cream);
          border-radius: var(--radius-md);
        }
        .what-it-looks-like p {
          font-size: 0.95rem;
          line-height: 1.7;
          color: var(--ink-light);
        }
      `}</style>
    </div>
  )
}
