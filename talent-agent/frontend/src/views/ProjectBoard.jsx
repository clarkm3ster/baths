import { useState, useEffect } from 'react'

const STAGE_LABELS = {
  development: 'Development',
  pre_production: 'Pre-Production',
  production: 'Production',
  post_production: 'Post-Production',
  distribution: 'Distribution',
}

const STAGE_ORDER = ['development', 'pre_production', 'production', 'post_production', 'distribution']

export default function ProjectBoard({ onOpenProject }) {
  const [projects, setProjects] = useState([])
  const [filter, setFilter] = useState('')
  const [statusFilter, setStatusFilter] = useState('')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const params = new URLSearchParams()
    if (filter) params.set('game_type', filter)
    if (statusFilter) params.set('status', statusFilter)
    fetch(`/api/projects?${params}`)
      .then(r => r.json())
      .then(data => { setProjects(data.projects); setLoading(false) })
      .catch(() => setLoading(false))
  }, [filter, statusFilter])

  const activeProductions = projects.filter(p => p.status === 'in_production')
  const sourced = projects.filter(p => p.status === 'sourced')
  const assembling = projects.filter(p => p.status === 'assembling')
  const completed = projects.filter(p => ['completed', 'published'].includes(p.status))

  if (loading) return <div className="loading">Loading projects...</div>

  return (
    <div>
      <div className="page-header">
        <h2>Project Board</h2>
        <p>All productions — sourced, assembling, in production, and completed.</p>
      </div>

      <div className="search-bar">
        <button className={`filter-btn ${filter === '' ? 'active' : ''}`} onClick={() => setFilter('')}>All</button>
        <button className={`filter-btn ${filter === 'domes' ? 'active' : ''}`} onClick={() => setFilter('domes')}>Domes</button>
        <button className={`filter-btn ${filter === 'spheres' ? 'active' : ''}`} onClick={() => setFilter('spheres')}>Spheres</button>
        <div style={{ width: 1, background: 'var(--border)', margin: '0 0.25rem' }} />
        <button className={`filter-btn ${statusFilter === '' ? 'active' : ''}`} onClick={() => setStatusFilter('')}>All Status</button>
        <button className={`filter-btn ${statusFilter === 'sourced' ? 'active' : ''}`} onClick={() => setStatusFilter('sourced')}>Sourced</button>
        <button className={`filter-btn ${statusFilter === 'in_production' ? 'active' : ''}`} onClick={() => setStatusFilter('in_production')}>Active</button>
        <button className={`filter-btn ${statusFilter === 'completed' ? 'active' : ''}`} onClick={() => setStatusFilter('completed')}>Done</button>
      </div>

      {/* Active Productions — prominent */}
      {activeProductions.length > 0 && (
        <div className="board-section">
          <h3 className="board-section-title">In Production</h3>
          <div className="grid-2">
            {activeProductions.map(p => (
              <ProjectCard key={p.project_id} project={p} onClick={() => onOpenProject(p.project_id)} />
            ))}
          </div>
        </div>
      )}

      {/* Assembling */}
      {assembling.length > 0 && (
        <div className="board-section">
          <h3 className="board-section-title">Assembling Teams</h3>
          <div className="grid-2">
            {assembling.map(p => (
              <ProjectCard key={p.project_id} project={p} onClick={() => onOpenProject(p.project_id)} />
            ))}
          </div>
        </div>
      )}

      {/* Sourced — available for assignment */}
      {sourced.length > 0 && (
        <div className="board-section">
          <h3 className="board-section-title">Sourced — Ready for Teams</h3>
          <div className="grid-2">
            {sourced.map(p => (
              <ProjectCard key={p.project_id} project={p} onClick={() => onOpenProject(p.project_id)} />
            ))}
          </div>
        </div>
      )}

      {/* Completed */}
      {completed.length > 0 && (
        <div className="board-section">
          <h3 className="board-section-title">Completed</h3>
          <div className="grid-2">
            {completed.map(p => (
              <ProjectCard key={p.project_id} project={p} onClick={() => onOpenProject(p.project_id)} />
            ))}
          </div>
        </div>
      )}

      <style>{`
        .board-section {
          margin-bottom: 2.5rem;
        }
        .board-section-title {
          font-family: 'Inter', sans-serif;
          font-size: 0.8rem;
          font-weight: 600;
          text-transform: uppercase;
          letter-spacing: 0.08em;
          color: var(--ink-lighter);
          margin-bottom: 1rem;
          padding-bottom: 0.5rem;
          border-bottom: 1px solid var(--border-light);
        }
      `}</style>
    </div>
  )
}

function ProjectCard({ project, onClick }) {
  const isDomes = project.game_type === 'domes'
  const subject = isDomes
    ? project.character?.name
    : project.parcel?.address

  const stageIdx = project.current_stage ? STAGE_ORDER.indexOf(project.current_stage) : -1
  const progress = stageIdx >= 0 ? ((stageIdx + 1) / 5) * 100 : 0

  return (
    <div className="card card-clickable project-card" onClick={onClick}>
      <div className="project-card-top">
        <div>
          <div className="project-title">{project.title}</div>
          {subject && <div className="project-subject">{subject}</div>}
        </div>
        <div className="project-badges">
          <span className={`badge badge-${project.game_type}`}>{project.game_type.toUpperCase()}</span>
          <span className={`badge badge-status ${project.status}`}>{project.status.replace('_', ' ')}</span>
        </div>
      </div>

      {project.current_stage && (
        <div className="project-stage">
          <div className="stage-track">
            {STAGE_ORDER.map((s, i) => (
              <div
                key={s}
                className={`stage-dot ${i <= stageIdx ? 'filled' : ''} ${project.current_stage === s ? 'current' : ''}`}
                title={STAGE_LABELS[s]}
              />
            ))}
            <div className="stage-line">
              <div className="stage-line-fill" style={{ width: `${progress}%` }} />
            </div>
          </div>
          <span className="stage-label">{STAGE_LABELS[project.current_stage]}</span>
        </div>
      )}

      {project.team_ids?.length > 0 && (
        <div className="project-team-count">{project.team_ids.length} team members</div>
      )}

      <div className="project-scores">
        {project.cosm_score > 0 && <span className="score-value cosm">{project.cosm_score.toFixed(1)} Cosm</span>}
        {project.chron_score > 0 && <span className="score-value chron">{project.chron_score.toFixed(1)} Chron</span>}
      </div>

      <style>{`
        .project-card {
          display: flex;
          flex-direction: column;
          gap: 0.75rem;
        }
        .project-card-top {
          display: flex;
          justify-content: space-between;
          align-items: flex-start;
        }
        .project-title {
          font-family: 'Playfair Display', serif;
          font-size: 1.1rem;
          font-weight: 600;
          margin-bottom: 0.15rem;
        }
        .project-subject {
          font-size: 0.85rem;
          color: var(--ink-lighter);
        }
        .project-badges {
          display: flex;
          gap: 0.35rem;
          flex-shrink: 0;
        }
        .project-stage {
          display: flex;
          align-items: center;
          gap: 0.75rem;
        }
        .stage-track {
          flex: 1;
          display: flex;
          align-items: center;
          gap: 0;
          position: relative;
          padding: 0 4px;
        }
        .stage-dot {
          width: 8px;
          height: 8px;
          border-radius: 50%;
          background: var(--paper-dark);
          border: 1.5px solid var(--border);
          position: relative;
          z-index: 2;
          flex-shrink: 0;
        }
        .stage-dot.filled {
          background: var(--accent);
          border-color: var(--accent);
        }
        .stage-dot.current {
          background: var(--ink);
          border-color: var(--ink);
          box-shadow: 0 0 0 3px rgba(26,26,26,0.15);
        }
        .stage-dot + .stage-dot {
          margin-left: calc(25% - 8px);
        }
        .stage-line {
          position: absolute;
          left: 8px;
          right: 8px;
          height: 2px;
          background: var(--border-light);
          z-index: 1;
        }
        .stage-line-fill {
          height: 100%;
          background: var(--accent);
          transition: width 0.4s ease;
        }
        .stage-label {
          font-size: 0.75rem;
          font-weight: 500;
          color: var(--ink-lighter);
          white-space: nowrap;
        }
        .project-team-count {
          font-size: 0.8rem;
          color: var(--ink-lighter);
        }
        .project-scores {
          display: flex;
          gap: 0.75rem;
        }
      `}</style>
    </div>
  )
}
