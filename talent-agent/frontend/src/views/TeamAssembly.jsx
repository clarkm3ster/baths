import { useState, useEffect } from 'react'

export default function TeamAssembly({ onOpenProject, onOpenTalent }) {
  const [projects, setProjects] = useState([])
  const [principals, setPrincipals] = useState([])
  const [selectedProject, setSelectedProject] = useState(null)
  const [selectedPrincipal, setSelectedPrincipal] = useState('')
  const [team, setTeam] = useState(null)
  const [assembling, setAssembling] = useState(false)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    Promise.all([
      fetch('/api/projects?status=sourced').then(r => r.json()),
      fetch('/api/principals').then(r => r.json()),
    ]).then(([projData, princData]) => {
      setProjects(projData.projects)
      setPrincipals(princData.principals)
      setLoading(false)
    }).catch(() => setLoading(false))
  }, [])

  const handleAssemble = async () => {
    if (!selectedProject) return
    setAssembling(true)
    setTeam(null)
    const params = new URLSearchParams()
    if (selectedPrincipal) params.set('principal_id', selectedPrincipal)
    params.set('team_size', '6')
    try {
      const res = await fetch(`/api/projects/${selectedProject.project_id}/assemble?${params}`, { method: 'POST' })
      const data = await res.json()
      setTeam(data)
    } catch (e) {
      console.error('Assembly failed:', e)
    }
    setAssembling(false)
  }

  if (loading) return <div className="loading">Loading...</div>

  return (
    <div>
      <div className="page-header">
        <h2>Team Assembly</h2>
        <p>Select a project, optionally choose a principal, and let the agent assemble a team based on resonance — not role-filling, but genuine matchmaking between practices and production challenge.</p>
      </div>

      <div className="assembly-controls">
        <div className="assembly-step">
          <div className="step-label">1. Select Project</div>
          <div className="project-select-grid">
            {projects.map(p => (
              <div
                key={p.project_id}
                className={`project-select-card ${selectedProject?.project_id === p.project_id ? 'selected' : ''}`}
                onClick={() => { setSelectedProject(p); setTeam(null) }}
              >
                <span className={`badge badge-${p.game_type}`}>{p.game_type.toUpperCase()}</span>
                <span className="psc-title">{p.title}</span>
              </div>
            ))}
          </div>
        </div>

        {selectedProject && (
          <div className="assembly-step">
            <div className="step-label">2. Choose Principal (optional — agent will recommend)</div>
            <div className="principal-select-grid">
              <div
                className={`principal-select-card ${selectedPrincipal === '' ? 'selected' : ''}`}
                onClick={() => setSelectedPrincipal('')}
              >
                <span className="psc-name">Agent's Choice</span>
                <span className="psc-desc">Let the agent recommend a principal</span>
              </div>
              {principals
                .filter(p => !selectedProject.game_type || !p.game_type || p.game_type === selectedProject.game_type)
                .map(p => (
                  <div
                    key={p.principal_id}
                    className={`principal-select-card ${selectedPrincipal === p.principal_id ? 'selected' : ''}`}
                    onClick={() => setSelectedPrincipal(p.principal_id)}
                  >
                    <span className="psc-name">{p.name}</span>
                    <span className="psc-desc">{p.signature_style?.slice(0, 60) || p.bio.slice(0, 60)}...</span>
                  </div>
                ))}
            </div>
          </div>
        )}

        {selectedProject && (
          <button className="btn btn-primary assemble-btn" onClick={handleAssemble} disabled={assembling}>
            {assembling ? 'Assembling...' : 'Assemble Team'}
          </button>
        )}
      </div>

      {/* Team Result */}
      {team && (
        <div className="team-result">
          <div className="section-divider" />
          <h3 className="team-result-title">Assembled Team</h3>

          <div className="team-principal-card">
            <div className="tp-label">PRINCIPAL</div>
            <div className="tp-name">{team.principal_name}</div>
          </div>

          <div className="team-strength">
            <div className="ts-label">Team Strength</div>
            <p>{team.team_strength}</p>
          </div>

          {team.unlikely_collisions?.length > 0 && (
            <div className="team-unlikely">
              <div className="ts-label">Unlikely Collisions</div>
              {team.unlikely_collisions.map((c, i) => (
                <p key={i} className="unlikely-item">{c}</p>
              ))}
            </div>
          )}

          <div className="team-capabilities">
            <div className="ts-label">Capabilities Coverage</div>
            <div className="caps-grid">
              {Object.entries(team.capabilities_coverage || {}).map(([cap, covered]) => (
                <div key={cap} className={`cap-item ${covered ? 'covered' : 'missing'}`}>
                  <span className="cap-icon">{covered ? '\u2713' : '\u2717'}</span>
                  <span>{cap.replace('_', ' ')}</span>
                </div>
              ))}
            </div>
          </div>

          {team.ip_surface_area?.length > 0 && (
            <div className="team-ip-surface">
              <div className="ts-label">Expected IP Surface Area</div>
              <div className="tags">
                {team.ip_surface_area.map(d => (
                  <span key={d} className="tag">{d.replace('_', ' ')}</span>
                ))}
              </div>
            </div>
          )}

          <div className="team-members">
            <div className="ts-label">Team Members</div>
            {team.members?.map((m, i) => (
              <div key={m.talent_id} className="team-member-card card" onClick={() => onOpenTalent(m.talent_id)} style={{ cursor: 'pointer' }}>
                <div className="tm-header">
                  <span className="tm-name">{m.talent_name}</span>
                  <span className="tm-score">{m.resonance_score.toFixed(0)} resonance</span>
                </div>
                <div className="resonance-bar-container">
                  <div className="resonance-bar" style={{ width: `${m.resonance_score}%` }} />
                </div>
                <p className="tm-reasoning">{m.reasoning}</p>
                {m.unlikely_value && (
                  <div className="tm-unlikely">{m.unlikely_value}</div>
                )}
                {m.capabilities_matched?.length > 0 && (
                  <div className="tags" style={{ marginTop: '0.35rem' }}>
                    {m.capabilities_matched.map(c => (
                      <span key={c} className="tag">{c.replace('_', ' ')}</span>
                    ))}
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      <style>{`
        .assembly-controls {
          display: flex;
          flex-direction: column;
          gap: 1.5rem;
        }
        .assembly-step {
          display: flex;
          flex-direction: column;
          gap: 0.75rem;
        }
        .step-label {
          font-size: 0.8rem;
          font-weight: 600;
          text-transform: uppercase;
          letter-spacing: 0.06em;
          color: var(--ink-lighter);
        }
        .project-select-grid, .principal-select-grid {
          display: flex;
          flex-wrap: wrap;
          gap: 0.5rem;
        }
        .project-select-card, .principal-select-card {
          padding: 0.6rem 1rem;
          border: 1px solid var(--border);
          border-radius: var(--radius-sm);
          background: white;
          cursor: pointer;
          display: flex;
          align-items: center;
          gap: 0.5rem;
          transition: all 0.2s;
        }
        .project-select-card:hover, .principal-select-card:hover {
          border-color: var(--accent);
        }
        .project-select-card.selected, .principal-select-card.selected {
          border-color: var(--ink);
          background: var(--ink);
          color: white;
        }
        .project-select-card.selected .badge { opacity: 0.7; }
        .psc-title, .psc-name {
          font-weight: 600;
          font-size: 0.9rem;
        }
        .psc-desc {
          font-size: 0.8rem;
          color: var(--ink-lighter);
        }
        .principal-select-card.selected .psc-desc { color: rgba(255,255,255,0.7); }
        .assemble-btn {
          align-self: flex-start;
          padding: 0.75rem 2rem;
          font-size: 0.95rem;
        }
        .team-result {
          margin-top: 1rem;
        }
        .team-result-title {
          font-size: 1.3rem;
          margin-bottom: 1.25rem;
        }
        .team-principal-card {
          padding: 1.25rem;
          background: var(--ink);
          color: white;
          border-radius: var(--radius-md);
          margin-bottom: 1.25rem;
        }
        .tp-label {
          font-size: 0.7rem;
          font-weight: 600;
          letter-spacing: 0.1em;
          text-transform: uppercase;
          opacity: 0.6;
          margin-bottom: 0.25rem;
        }
        .tp-name {
          font-family: 'Playfair Display', serif;
          font-size: 1.5rem;
          font-weight: 600;
        }
        .team-strength, .team-unlikely, .team-capabilities, .team-ip-surface {
          margin-bottom: 1.25rem;
        }
        .ts-label {
          font-size: 0.75rem;
          font-weight: 600;
          text-transform: uppercase;
          letter-spacing: 0.06em;
          color: var(--ink-lighter);
          margin-bottom: 0.5rem;
        }
        .team-strength p, .team-unlikely p {
          font-size: 0.95rem;
          color: var(--ink-light);
          line-height: 1.6;
        }
        .unlikely-item {
          font-style: italic;
          padding-left: 0.75rem;
          border-left: 2px solid var(--accent-light);
          margin-bottom: 0.5rem;
        }
        .caps-grid {
          display: flex;
          flex-wrap: wrap;
          gap: 0.5rem;
        }
        .cap-item {
          display: flex;
          align-items: center;
          gap: 0.35rem;
          padding: 0.35rem 0.75rem;
          border-radius: 20px;
          font-size: 0.8rem;
          font-weight: 500;
        }
        .cap-item.covered {
          background: var(--success-bg);
          color: var(--success);
        }
        .cap-item.missing {
          background: var(--spheres-bg);
          color: var(--spheres-color);
        }
        .team-members {
          display: flex;
          flex-direction: column;
          gap: 0.75rem;
        }
        .team-member-card {
          padding: 1rem 1.25rem;
        }
        .tm-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 0.25rem;
        }
        .tm-name {
          font-family: 'Playfair Display', serif;
          font-weight: 600;
          font-size: 1rem;
        }
        .tm-score {
          font-family: 'JetBrains Mono', monospace;
          font-size: 0.8rem;
          color: var(--accent-dark);
          font-weight: 500;
        }
        .tm-reasoning {
          font-size: 0.85rem;
          color: var(--ink-light);
          line-height: 1.5;
          margin-top: 0.5rem;
        }
        .tm-unlikely {
          font-size: 0.8rem;
          font-style: italic;
          color: var(--accent-dark);
          margin-top: 0.35rem;
        }
      `}</style>
    </div>
  )
}
