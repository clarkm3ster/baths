import { useState, useEffect } from 'react'

const STAGE_LABELS = {
  development: 'Development',
  pre_production: 'Pre-Production',
  production: 'Production',
  post_production: 'Post-Production',
  distribution: 'Distribution',
}
const STAGE_ORDER = ['development', 'pre_production', 'production', 'post_production', 'distribution']

export default function ProjectDetail({ projectId, onBack, onOpenTalent, onOpenPrincipal }) {
  const [project, setProject] = useState(null)
  const [team, setTeam] = useState(null)
  const [principals, setPrincipals] = useState([])
  const [assembling, setAssembling] = useState(false)
  const [selectedPrincipal, setSelectedPrincipal] = useState('')
  const [loading, setLoading] = useState(true)
  const [lastStageOutput, setLastStageOutput] = useState(null)
  const [advancing, setAdvancing] = useState(false)
  const [replaying, setReplaying] = useState(false)

  const fetchProject = () => {
    fetch(`/api/projects/${projectId}`)
      .then(r => r.json())
      .then(data => {
        setProject(data.project)
        setTeam(data.team)
        setLoading(false)
      })
      .catch(() => setLoading(false))
  }

  useEffect(() => {
    fetchProject()
    fetch('/api/principals').then(r => r.json()).then(d => setPrincipals(d.principals)).catch(() => {})
  }, [projectId])

  const handleAssemble = async () => {
    setAssembling(true)
    const params = new URLSearchParams({ team_size: '6' })
    if (selectedPrincipal) params.set('principal_id', selectedPrincipal)
    await fetch(`/api/projects/${projectId}/assemble?${params}`, { method: 'POST' })
    fetchProject()
    setAssembling(false)
  }

  const handleStart = async () => {
    setAdvancing(true)
    try {
      const res = await fetch(`/api/projects/${projectId}/start`, { method: 'POST' })
      const data = await res.json()
      if (data.stage_output) setLastStageOutput(data.stage_output)
      fetchProject()
    } catch (e) {
      console.error('Start failed:', e)
    }
    setAdvancing(false)
  }

  const handleAdvance = async () => {
    setAdvancing(true)
    setLastStageOutput(null)
    try {
      const res = await fetch(`/api/projects/${projectId}/advance`, { method: 'POST' })
      const data = await res.json()
      if (data.stage_output) setLastStageOutput(data.stage_output)
      fetchProject()
    } catch (e) {
      console.error('Advance failed:', e)
    }
    setAdvancing(false)
  }

  const handleReplay = async () => {
    setReplaying(true)
    try {
      await fetch(`/api/projects/${projectId}/replay`, { method: 'POST' })
      setLastStageOutput(null)
      fetchProject()
    } catch (e) {
      console.error('Replay failed:', e)
    }
    setReplaying(false)
  }

  if (loading) return <div className="loading">Loading project...</div>
  if (!project) return <div className="empty-state"><h3>Project not found</h3></div>

  const isDomes = project.game_type === 'domes'
  const stageIdx = project.current_stage ? STAGE_ORDER.indexOf(project.current_stage) : -1

  // Use the last stage from the log if we don't have a fresh output
  const displayOutput = lastStageOutput || (project.stage_log?.length > 0 ? project.stage_log[project.stage_log.length - 1] : null)

  return (
    <div className="detail-page" style={{ maxWidth: '1000px' }}>
      <button className="btn btn-back" onClick={onBack}>&larr; Back to Projects</button>

      <div className="detail-header">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
          <div>
            <h2>{project.title}</h2>
            <div style={{ display: 'flex', gap: '0.5rem', marginTop: '0.35rem', alignItems: 'center' }}>
              <span className={`badge badge-${project.game_type}`}>{project.game_type.toUpperCase()}</span>
              <span className={`badge badge-status ${project.status}`}>{project.status.replace('_', ' ')}</span>
              {project.production_number > 1 && (
                <span className="badge" style={{ background: 'var(--accent-light)', color: 'var(--accent-dark)' }}>
                  Production #{project.production_number}
                </span>
              )}
            </div>
          </div>
          {(project.cosm_score > 0 || project.chron_score > 0) && (
            <div className="score-inline">
              <div>
                <div className="score-label">Cosm</div>
                <div className="score-value cosm">{project.cosm_score.toFixed(1)}</div>
              </div>
              <div>
                <div className="score-label">Chron</div>
                <div className="score-value chron">{project.chron_score.toFixed(1)}</div>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Character or Parcel Brief */}
      {isDomes && project.character && (
        <div className="detail-section">
          <h3>Character Brief</h3>
          <div className="brief-card">
            <div className="brief-name">{project.character.name}</div>
            <div className="brief-source">
              From <em>{project.character.source}</em>
              <div className="brief-citation">{project.character.source_citation}</div>
            </div>
            <div className="brief-block">
              <div className="brief-label">Situation</div>
              <p>{project.character.situation}</p>
            </div>
            <div className="brief-block">
              <div className="brief-label">Full Landscape</div>
              <p>{project.character.full_landscape}</p>
            </div>
            <div className="brief-block highlight">
              <div className="brief-label">Production Challenge</div>
              <p>{project.character.production_challenge}</p>
            </div>
            <div className="brief-tags-row">
              <div>
                <div className="brief-label" style={{ marginBottom: '0.35rem' }}>Key Systems</div>
                <div className="tags">{project.character.key_systems.map(s => <span key={s} className="tag">{s}</span>)}</div>
              </div>
              <div>
                <div className="brief-label" style={{ marginBottom: '0.35rem' }}>Flourishing Dimensions</div>
                <div className="tags">{project.character.flourishing_dimensions.map(d => <span key={d} className="tag domes">{d}</span>)}</div>
              </div>
            </div>
          </div>
        </div>
      )}

      {!isDomes && project.parcel && (
        <div className="detail-section">
          <h3>Parcel Brief</h3>
          <div className="brief-card">
            <div className="brief-name">{project.parcel.address}</div>
            <div className="brief-source">
              {project.parcel.neighborhood}, {project.parcel.city} &middot; {project.parcel.zoning} &middot; <span className="mono">{project.parcel.lot_size_sqft.toLocaleString()} sqft</span>
            </div>
            <div className="brief-block">
              <div className="brief-label">History</div>
              <p>{project.parcel.history}</p>
            </div>
            <div className="brief-block highlight">
              <div className="brief-label">Activation Opportunity</div>
              <p>{project.parcel.opportunity}</p>
            </div>
            <div className="brief-block">
              <div className="brief-label">Community Context</div>
              <p>{project.parcel.community_context}</p>
            </div>
            <div>
              <div className="brief-label" style={{ marginBottom: '0.35rem' }}>Constraints</div>
              <div className="tags">{project.parcel.constraints.map((c, i) => <span key={i} className="tag">{c}</span>)}</div>
            </div>
          </div>
        </div>
      )}

      {/* Stage Progress */}
      {project.current_stage && (
        <div className="detail-section">
          <h3>Production Pipeline</h3>
          <div className="stage-progress">
            {STAGE_ORDER.map((s, i) => (
              <div key={s} className={`stage-step ${i <= stageIdx ? 'done' : ''} ${project.current_stage === s ? 'current' : ''}`}>
                <div className="stage-step-dot" />
                <span className="stage-step-label">{STAGE_LABELS[s]}</span>
              </div>
            ))}
          </div>
          {project.status === 'in_production' && (
            <button
              className="btn btn-primary"
              style={{ marginTop: '1rem' }}
              onClick={handleAdvance}
              disabled={advancing}
            >
              {advancing ? 'Playing...' : stageIdx < 4 ? `Play ${STAGE_LABELS[STAGE_ORDER[stageIdx + 1]]}` : 'Complete Production'}
            </button>
          )}
        </div>
      )}

      {/* Stage Output — what the team just produced */}
      {displayOutput && (
        <div className="detail-section">
          <h3>Stage Output: {displayOutput.stage_name}</h3>
          <div className="stage-output-card">
            <div className="stage-focus">{displayOutput.focus}</div>

            {/* Prior Art */}
            {displayOutput.prior_art?.length > 0 && (
              <div className="prior-art-section">
                <div className="pa-header">
                  <span className="pa-label">Prior Art Available</span>
                  <span className="pa-count">{displayOutput.prior_art.length} deliverables from previous productions</span>
                </div>
                {displayOutput.prior_art_referenced?.length > 0 && (
                  <div className="pa-used">
                    Building on {displayOutput.prior_art_referenced.length} prior deliverable{displayOutput.prior_art_referenced.length > 1 ? 's' : ''}:
                    {displayOutput.prior_art_referenced.map((pa, i) => (
                      <div key={i} className="pa-ref">
                        <span className="pa-ref-icon">&#8618;</span>
                        <span>{pa.title} ({pa.practitioner_name})</span>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            )}

            {/* Deliverables */}
            <div className="deliverables-section">
              <div className="del-header">
                <span className="del-count">{displayOutput.deliverable_count} Deliverables</span>
                <span className="del-ip">{displayOutput.ip_count} IP Items Generated</span>
              </div>
              {displayOutput.deliverables?.map((d, i) => (
                <div
                  key={i}
                  className={`deliverable-card ${d.is_unlikely ? 'unlikely' : ''}`}
                  onClick={() => d.talent_id && onOpenTalent(d.talent_id)}
                  style={{ cursor: d.talent_id ? 'pointer' : 'default' }}
                >
                  <div className="del-top">
                    <span className="del-talent">{d.talent_name}</span>
                    <span className="del-practice">{d.practice}</span>
                    {d.is_unlikely && <span className="del-unlikely-badge">Unlikely Collision</span>}
                  </div>
                  <div className="del-title">{d.title}</div>
                  <div className="del-desc">{d.description}</div>
                  <div className="del-meta">
                    <span className={`tag ${d.ip_domain === 'policy' ? '' : d.ip_domain === 'entertainment' ? 'domes' : 'spheres'}`}>
                      {d.ip_domain?.replace('_', ' ')}
                    </span>
                    {d.built_on && (
                      <span className="del-built-on">Builds on prior art</span>
                    )}
                  </div>
                </div>
              ))}
            </div>

            {/* Score Delta */}
            <div className="stage-scores">
              <div className="stage-score-item">
                <span className="ss-label">Cosm</span>
                <span className="ss-value cosm">+{displayOutput.cosm_delta}</span>
              </div>
              <div className="stage-score-item">
                <span className="ss-label">Chron</span>
                <span className="ss-value chron">+{displayOutput.chron_delta}</span>
              </div>
              {displayOutput.unlikely_count > 0 && (
                <div className="stage-score-item">
                  <span className="ss-label">Unlikely</span>
                  <span className="ss-value unlikely">{displayOutput.unlikely_count}</span>
                </div>
              )}
              {displayOutput.prior_art_used > 0 && (
                <div className="stage-score-item">
                  <span className="ss-label">Prior Art</span>
                  <span className="ss-value prior">+{displayOutput.prior_art_used} refs</span>
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Full Stage Log */}
      {project.stage_log?.length > 1 && (
        <div className="detail-section">
          <h3>Production Log ({project.stage_log.length} stages)</h3>
          <div className="stage-log">
            {project.stage_log.map((entry, i) => (
              <div key={i} className="log-entry" onClick={() => setLastStageOutput(entry)} style={{ cursor: 'pointer' }}>
                <div className="log-stage">{entry.stage_name}</div>
                <div className="log-stats">
                  <span>{entry.deliverable_count} deliverables</span>
                  <span>{entry.ip_count} IP</span>
                  {entry.unlikely_count > 0 && <span className="log-unlikely">{entry.unlikely_count} unlikely</span>}
                  <span className="log-cosm">+{entry.cosm_delta} Cosm</span>
                  <span className="log-chron">+{entry.chron_delta} Chron</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Team */}
      {team && (
        <div className="detail-section">
          <h3>Assembled Team</h3>
          <div className="project-team-principal" onClick={() => onOpenPrincipal(team.principal_id)} style={{ cursor: 'pointer' }}>
            <div className="ptp-label">PRINCIPAL</div>
            <div className="ptp-name">{team.principal_name}</div>
          </div>
          <div className="team-strength-box">
            <p>{team.team_strength}</p>
          </div>
          {team.unlikely_collisions?.length > 0 && (
            <div style={{ marginBottom: '1rem' }}>
              <div className="brief-label" style={{ marginBottom: '0.35rem' }}>Unlikely Collisions</div>
              {team.unlikely_collisions.map((c, i) => (
                <p key={i} style={{ fontSize: '0.85rem', fontStyle: 'italic', color: 'var(--accent-dark)', marginBottom: '0.25rem' }}>{c}</p>
              ))}
            </div>
          )}
          <div className="team-members-list">
            {team.members?.map(m => (
              <div key={m.talent_id} className="team-member-row" onClick={() => onOpenTalent(m.talent_id)}>
                <div className="tmr-left">
                  <span className="tmr-name">{m.talent_name}</span>
                  <span className="tmr-reasoning">{m.reasoning.split('|')[0].trim()}</span>
                </div>
                <div className="tmr-right">
                  <span className="tmr-score">{m.resonance_score.toFixed(0)}</span>
                  <div className="resonance-bar-container" style={{ width: '80px' }}>
                    <div className="resonance-bar" style={{ width: `${m.resonance_score}%` }} />
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Assembly controls */}
      {project.status === 'sourced' && (
        <div className="detail-section">
          <h3>Assemble Team</h3>
          <p style={{ color: 'var(--ink-lighter)', marginBottom: '1rem', fontSize: '0.9rem' }}>
            {project.production_number > 1
              ? `Production #${project.production_number} — a new team gets the same brief. Prior art from previous productions is available.`
              : 'Select a principal or let the agent recommend one, then assemble a team based on resonance with this production.'
            }
          </p>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem', marginBottom: '1rem' }}>
            <div
              className={`filter-btn ${selectedPrincipal === '' ? 'active' : ''}`}
              onClick={() => setSelectedPrincipal('')}
              style={{ cursor: 'pointer' }}
            >
              Agent's Choice
            </div>
            {principals
              .filter(p => !project.game_type || !p.game_type || p.game_type === project.game_type)
              .map(p => (
                <div
                  key={p.principal_id}
                  className={`filter-btn ${selectedPrincipal === p.principal_id ? 'active' : ''}`}
                  onClick={() => setSelectedPrincipal(p.principal_id)}
                  style={{ cursor: 'pointer' }}
                >
                  {p.name}
                </div>
              ))}
          </div>
          <button className="btn btn-primary" onClick={handleAssemble} disabled={assembling}>
            {assembling ? 'Assembling...' : 'Assemble Team'}
          </button>
        </div>
      )}

      {/* Start production */}
      {project.status === 'assembling' && team && (
        <div className="detail-section">
          <button className="btn btn-primary" onClick={handleStart} disabled={advancing}>
            {advancing ? 'Starting...' : 'Start Production'}
          </button>
          <p style={{ color: 'var(--ink-lighter)', marginTop: '0.5rem', fontSize: '0.85rem' }}>
            Starting production begins with Development — the team produces their first deliverables.
          </p>
        </div>
      )}

      {/* Replay — run the same project with a different team */}
      {(project.status === 'completed' || project.status === 'published') && (
        <div className="detail-section">
          <div className="replay-section">
            <h3 style={{ marginBottom: '0.5rem' }}>New Production Run</h3>
            <p style={{ color: 'var(--ink-lighter)', fontSize: '0.9rem', marginBottom: '1rem' }}>
              Run this project again with a different team and principal.
              The new team will see all IP from Production #{project.production_number} as prior art
              and decide whether to build on it or diverge.
            </p>
            <button className="btn btn-secondary" onClick={handleReplay} disabled={replaying}>
              {replaying ? 'Resetting...' : `Start Production #${project.production_number + 1}`}
            </button>
          </div>
        </div>
      )}

      <style>{`
        .brief-card {
          background: white;
          border: 1px solid var(--border);
          border-radius: var(--radius-md);
          padding: 1.5rem;
          display: flex;
          flex-direction: column;
          gap: 1rem;
        }
        .brief-name {
          font-family: 'Playfair Display', serif;
          font-size: 1.3rem;
          font-weight: 600;
        }
        .brief-source {
          font-size: 0.9rem;
          color: var(--ink-lighter);
        }
        .brief-citation {
          font-size: 0.8rem;
          color: var(--ink-lighter);
          margin-top: 0.25rem;
          font-style: italic;
        }
        .brief-block {
          padding: 1rem;
          background: var(--paper-warm);
          border-radius: var(--radius-sm);
        }
        .brief-block.highlight {
          background: var(--cream);
          border-left: 3px solid var(--accent);
        }
        .brief-label {
          font-size: 0.7rem;
          font-weight: 600;
          text-transform: uppercase;
          letter-spacing: 0.06em;
          color: var(--accent-dark);
          margin-bottom: 0.35rem;
        }
        .brief-block p {
          font-size: 0.95rem;
          line-height: 1.6;
          color: var(--ink-light);
        }
        .brief-tags-row {
          display: flex;
          gap: 2rem;
          flex-wrap: wrap;
        }
        .stage-progress {
          display: flex;
          gap: 0;
          align-items: center;
        }
        .stage-step {
          display: flex;
          align-items: center;
          gap: 0.5rem;
          padding: 0.5rem 1rem;
          border-bottom: 2px solid var(--border-light);
          flex: 1;
        }
        .stage-step.done {
          border-bottom-color: var(--accent);
        }
        .stage-step.current {
          border-bottom-color: var(--ink);
          border-bottom-width: 3px;
        }
        .stage-step-dot {
          width: 8px;
          height: 8px;
          border-radius: 50%;
          background: var(--border);
          flex-shrink: 0;
        }
        .stage-step.done .stage-step-dot { background: var(--accent); }
        .stage-step.current .stage-step-dot { background: var(--ink); box-shadow: 0 0 0 3px rgba(26,26,26,0.15); }
        .stage-step-label {
          font-size: 0.75rem;
          font-weight: 500;
          color: var(--ink-lighter);
        }
        .stage-step.current .stage-step-label { color: var(--ink); font-weight: 600; }

        /* Stage Output */
        .stage-output-card {
          background: white;
          border: 1px solid var(--border);
          border-radius: var(--radius-md);
          padding: 1.5rem;
          display: flex;
          flex-direction: column;
          gap: 1.25rem;
        }
        .stage-focus {
          font-size: 1rem;
          font-style: italic;
          color: var(--ink-light);
          padding-bottom: 1rem;
          border-bottom: 1px solid var(--border-light);
        }

        /* Prior Art */
        .prior-art-section {
          background: var(--cream);
          border: 1px solid var(--accent-light);
          border-radius: var(--radius-sm);
          padding: 1rem;
        }
        .pa-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 0.5rem;
        }
        .pa-label {
          font-size: 0.75rem;
          font-weight: 600;
          text-transform: uppercase;
          letter-spacing: 0.06em;
          color: var(--accent-dark);
        }
        .pa-count {
          font-size: 0.8rem;
          color: var(--ink-lighter);
        }
        .pa-used {
          font-size: 0.85rem;
          color: var(--ink-light);
          margin-top: 0.5rem;
        }
        .pa-ref {
          display: flex;
          align-items: center;
          gap: 0.35rem;
          padding: 0.25rem 0;
          font-size: 0.85rem;
          color: var(--accent-dark);
          font-style: italic;
        }
        .pa-ref-icon {
          font-size: 1rem;
        }

        /* Deliverables */
        .deliverables-section {
          display: flex;
          flex-direction: column;
          gap: 0.75rem;
        }
        .del-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
        }
        .del-count {
          font-size: 0.8rem;
          font-weight: 600;
          text-transform: uppercase;
          letter-spacing: 0.06em;
          color: var(--ink-light);
        }
        .del-ip {
          font-size: 0.8rem;
          color: var(--accent-dark);
          font-weight: 500;
        }
        .deliverable-card {
          padding: 1rem 1.25rem;
          background: var(--paper-warm);
          border-radius: var(--radius-sm);
          border-left: 3px solid var(--accent-light);
          transition: all 0.15s;
        }
        .deliverable-card:hover {
          border-left-color: var(--accent);
          box-shadow: var(--shadow-sm);
        }
        .deliverable-card.unlikely {
          border-left-color: var(--domes-color);
          background: var(--domes-bg);
        }
        .del-top {
          display: flex;
          align-items: center;
          gap: 0.5rem;
          margin-bottom: 0.35rem;
        }
        .del-talent {
          font-family: 'Playfair Display', serif;
          font-weight: 600;
          font-size: 0.95rem;
        }
        .del-practice {
          font-size: 0.75rem;
          color: var(--ink-lighter);
          padding: 0.1rem 0.4rem;
          background: white;
          border-radius: 20px;
          border: 1px solid var(--border-light);
        }
        .del-unlikely-badge {
          font-size: 0.7rem;
          font-weight: 600;
          text-transform: uppercase;
          letter-spacing: 0.06em;
          color: var(--domes-color);
          padding: 0.1rem 0.5rem;
          background: white;
          border-radius: 20px;
          border: 1px solid var(--domes-light);
        }
        .del-title {
          font-weight: 600;
          font-size: 0.95rem;
          margin-bottom: 0.35rem;
          color: var(--ink);
        }
        .del-desc {
          font-size: 0.85rem;
          color: var(--ink-light);
          line-height: 1.5;
          margin-bottom: 0.5rem;
        }
        .del-meta {
          display: flex;
          align-items: center;
          gap: 0.5rem;
        }
        .del-built-on {
          font-size: 0.75rem;
          font-style: italic;
          color: var(--accent-dark);
        }

        /* Stage Scores */
        .stage-scores {
          display: flex;
          gap: 1.5rem;
          padding-top: 1rem;
          border-top: 1px solid var(--border-light);
        }
        .stage-score-item {
          display: flex;
          flex-direction: column;
          align-items: center;
          gap: 0.15rem;
        }
        .ss-label {
          font-size: 0.65rem;
          font-weight: 600;
          text-transform: uppercase;
          letter-spacing: 0.08em;
          color: var(--ink-lighter);
        }
        .ss-value {
          font-family: 'JetBrains Mono', monospace;
          font-size: 1.1rem;
          font-weight: 600;
        }
        .ss-value.cosm { color: var(--domes-color); }
        .ss-value.chron { color: var(--spheres-color); }
        .ss-value.unlikely { color: var(--accent-dark); }
        .ss-value.prior { color: var(--success); font-size: 0.9rem; }

        /* Stage Log */
        .stage-log {
          display: flex;
          flex-direction: column;
          gap: 0.5rem;
        }
        .log-entry {
          display: flex;
          justify-content: space-between;
          align-items: center;
          padding: 0.75rem 1rem;
          background: white;
          border: 1px solid var(--border);
          border-radius: var(--radius-sm);
          transition: all 0.15s;
        }
        .log-entry:hover {
          border-color: var(--accent);
          box-shadow: var(--shadow-sm);
        }
        .log-stage {
          font-weight: 600;
          font-size: 0.9rem;
        }
        .log-stats {
          display: flex;
          gap: 0.75rem;
          font-size: 0.8rem;
          color: var(--ink-lighter);
        }
        .log-unlikely {
          color: var(--accent-dark);
          font-weight: 500;
        }
        .log-cosm {
          color: var(--domes-color);
          font-family: 'JetBrains Mono', monospace;
          font-size: 0.75rem;
        }
        .log-chron {
          color: var(--spheres-color);
          font-family: 'JetBrains Mono', monospace;
          font-size: 0.75rem;
        }

        /* Team */
        .project-team-principal {
          padding: 1.25rem;
          background: var(--ink);
          color: white;
          border-radius: var(--radius-md);
          margin-bottom: 1rem;
        }
        .ptp-label {
          font-size: 0.7rem;
          font-weight: 600;
          letter-spacing: 0.1em;
          text-transform: uppercase;
          opacity: 0.6;
          margin-bottom: 0.25rem;
        }
        .ptp-name {
          font-family: 'Playfair Display', serif;
          font-size: 1.3rem;
          font-weight: 600;
        }
        .team-strength-box {
          padding: 1rem;
          background: var(--paper-warm);
          border-radius: var(--radius-sm);
          margin-bottom: 1rem;
        }
        .team-strength-box p {
          font-size: 0.9rem;
          color: var(--ink-light);
          line-height: 1.5;
        }
        .team-members-list {
          display: flex;
          flex-direction: column;
          gap: 0.5rem;
        }
        .team-member-row {
          display: flex;
          justify-content: space-between;
          align-items: center;
          padding: 0.75rem 1rem;
          background: white;
          border: 1px solid var(--border);
          border-radius: var(--radius-sm);
          cursor: pointer;
          transition: all 0.15s;
        }
        .team-member-row:hover {
          border-color: var(--accent);
          box-shadow: var(--shadow-sm);
        }
        .tmr-left {
          display: flex;
          flex-direction: column;
          gap: 0.1rem;
        }
        .tmr-name {
          font-family: 'Playfair Display', serif;
          font-weight: 600;
          font-size: 0.95rem;
        }
        .tmr-reasoning {
          font-size: 0.8rem;
          color: var(--ink-lighter);
        }
        .tmr-right {
          display: flex;
          align-items: center;
          gap: 0.5rem;
          flex-shrink: 0;
        }
        .tmr-score {
          font-family: 'JetBrains Mono', monospace;
          font-size: 0.85rem;
          font-weight: 500;
          color: var(--accent-dark);
        }

        /* Replay */
        .replay-section {
          padding: 1.5rem;
          background: var(--paper-warm);
          border: 1px dashed var(--border);
          border-radius: var(--radius-md);
        }
      `}</style>
    </div>
  )
}
