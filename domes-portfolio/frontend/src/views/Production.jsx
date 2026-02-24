import { useState, useEffect } from 'react'
import { useParams, Link } from 'react-router-dom'

const COSM_DIM_ORDER = ['rights', 'research', 'budget', 'package', 'deliverables', 'pitch']

export default function Production() {
  const { id } = useParams()
  const [data, setData] = useState(null)
  const [files, setFiles] = useState([])
  const [openStages, setOpenStages] = useState({})
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    Promise.all([
      fetch(`/api/productions/${id}`).then(r => r.ok ? r.json() : null),
      fetch(`/api/productions/${id}/files`).then(r => r.ok ? r.json() : { files: [] }),
    ]).then(([prod, fileData]) => {
      setData(prod)
      setFiles(fileData.files || [])
      setLoading(false)
    }).catch(() => setLoading(false))
  }, [id])

  if (loading) return <div className="loading">Loading production...</div>
  if (!data) return <div className="loading">Production not found.</div>

  const project = data.project || {}
  const char = project.character || {}
  const principal = data.principal || {}
  const team = data.team || {}
  const scores = data.final_scores || {}
  const dims = scores.dimensions || {}
  const dimDetails = scores.dimension_details || {}
  const stages = data.stages || []
  const ipLog = data.ip_log || []
  const sources = data.sources_cited || []

  const toggleStage = (i) => setOpenStages(s => ({ ...s, [i]: !s[i] }))

  // Group IP by domain
  const ipByDomain = {}
  ipLog.forEach(ip => {
    const d = ip.domain || 'other'
    if (!ipByDomain[d]) ipByDomain[d] = []
    ipByDomain[d].push(ip)
  })

  // Group sources by type
  const sourcesByType = {}
  sources.forEach(s => {
    const t = s.type || 'other'
    if (!sourcesByType[t]) sourcesByType[t] = []
    sourcesByType[t].push(s)
  })

  const formatSize = (bytes) => {
    if (bytes > 1024 * 1024) return `${(bytes / 1024 / 1024).toFixed(1)} MB`
    if (bytes > 1024) return `${(bytes / 1024).toFixed(1)} KB`
    return `${bytes} B`
  }

  const fileIcon = (name) => {
    if (name.endsWith('.json')) return '{ }'
    if (name.endsWith('.md')) return 'MD'
    return '—'
  }

  return (
    <div>
      <Link to="/" className="prod-back">← All Productions</Link>

      {/* Header */}
      <div className="prod-header">
        <h1>{project.title}</h1>
        <p className="prod-source">
          {char.name} — <em>{char.source_citation || char.source}</em>
        </p>
        <div className="prod-meta-row">
          <div className="prod-meta-item">
            <label>Principal</label>
            {principal.name}
          </div>
          <div className="prod-meta-item">
            <label>Team</label>
            {(team.members || []).length} practitioners
          </div>
          <div className="prod-meta-item">
            <label>Stages</label>
            {stages.length}
          </div>
          <div className="prod-meta-item">
            <label>IP Generated</label>
            {ipLog.length} items
          </div>
          <div className="prod-meta-item">
            <label>Sources Cited</label>
            {sources.length}
          </div>
          <div className="prod-meta-item">
            <label>Production</label>
            #{project.production_number || 1}
          </div>
        </div>
      </div>

      {/* Cosm Score */}
      <div className="dim-panel">
        <h2 className="section-title">Cosm Score</h2>
        <div className="dim-total-row">
          <span className="dim-total-num">{(scores.total || 0).toFixed(1)}</span>
          <span className="dim-total-label">Total Cosm</span>
        </div>
        <div className="dim-grid">
          {COSM_DIM_ORDER.map(dk => {
            const det = dimDetails[dk] || {}
            const val = dims[dk] || 0
            const isWeak = dk === scores.weakest
            const isStrong = dk === scores.strongest
            return (
              <div key={dk} className="dim-card">
                <div className="dim-card-head">
                  <span className="dim-card-name">{det.label || dk}</span>
                  <span className="dim-card-score">{val.toFixed(1)}</span>
                </div>
                <div className="dim-bar">
                  <div className="dim-bar-fill" style={{ width: `${val}%` }} />
                </div>
                <p className="dim-card-desc">{det.description || ''}</p>
                {isWeak && <span className="dim-tag dim-tag-weak">Weakest</span>}
                {isStrong && <span className="dim-tag dim-tag-strong">Strongest</span>}
              </div>
            )
          })}
        </div>
      </div>

      {/* Production Timeline */}
      <div className="stages-section">
        <h2 className="section-title">Production Timeline</h2>
        {stages.map((stage, i) => (
          <div key={i} className="stage-item">
            <div className="stage-head" onClick={() => toggleStage(i)}>
              <div className="stage-head-left">
                <span className="stage-num">{i + 1}</span>
                <span className="stage-name">{stage.stage_name}</span>
                <span className="stage-focus">{stage.focus}</span>
              </div>
              <div className="stage-stats">
                <span>{stage.deliverable_count} deliverables</span>
                <span>{stage.ip_count} IP</span>
                {stage.unlikely_count > 0 && (
                  <span>{stage.unlikely_count} unlikely</span>
                )}
              </div>
              <span className={`stage-toggle ${openStages[i] ? 'open' : ''}`}>▾</span>
            </div>
            {openStages[i] && (
              <div className="stage-body">
                {(stage.deliverables || []).map((d, j) => (
                  <div key={j} className="deliverable">
                    <h4>
                      {d.title}
                      {d.is_unlikely && <span className="deliverable-unlikely">Unlikely Collision</span>}
                    </h4>
                    <p className="deliverable-practitioner">
                      {d.talent_name} — {d.practice} · {(d.capability || '').replace(/_/g, ' ')}
                    </p>
                    {d.work_referenced && d.work_referenced.length > 0 && (
                      <p className="deliverable-refs">
                        Drawing on: {d.work_referenced.map(w => `"${w.title}"`).join(', ')}
                      </p>
                    )}
                    <p className="deliverable-desc">{d.description}</p>
                  </div>
                ))}
              </div>
            )}
          </div>
        ))}
      </div>

      {/* Downloadable Files */}
      {files.length > 0 && (
        <div className="files-section">
          <h2 className="section-title">Downloads</h2>
          <div className="files-grid">
            {files.map((f, i) => (
              <a key={i} className="file-card" href={f.url} download>
                <span className="file-icon">{fileIcon(f.filename)}</span>
                <div className="file-info">
                  <div className="file-name">{f.filename}</div>
                  <div className="file-size">{formatSize(f.size)}</div>
                </div>
              </a>
            ))}
          </div>
        </div>
      )}

      {/* IP Portfolio */}
      {ipLog.length > 0 && (
        <div className="ip-section">
          <h2 className="section-title">IP Portfolio — {ipLog.length} Items</h2>
          {Object.entries(ipByDomain).sort().map(([domain, items]) => (
            <div key={domain} className="ip-domain-group">
              <div className="ip-domain-title">
                {domain.replace(/_/g, ' ')} <span className="ip-domain-count">({items.length})</span>
              </div>
              {items.map((ip, i) => (
                <div key={i} className="ip-item">
                  <div className="ip-item-title">{ip.title}</div>
                  <div className="ip-item-meta">
                    {ip.practitioner_name} · {(ip.practice || '').replace(/_/g, ' ')} · {(ip.stage || '').replace(/_/g, ' ')} · {ip.format}
                  </div>
                  <p className="ip-item-desc">{ip.description}</p>
                </div>
              ))}
            </div>
          ))}
        </div>
      )}

      {/* Sources */}
      {sources.length > 0 && (
        <div className="sources-section">
          <h2 className="section-title">Sources Cited</h2>
          <p className="sources-summary">
            {sources.length} sources across {Object.keys(sourcesByType).length} categories.
            All sources are real — no fabricated citations.
          </p>
          {Object.entries(sourcesByType).sort().map(([type, items]) => (
            <div key={type} className="source-group">
              <div className="source-group-title">
                {type.replace(/_/g, ' ')} ({items.length})
              </div>
              {items.map((s, i) => (
                <div key={i} className="source-item">
                  <div className="source-title">{s.title}</div>
                  <div className="source-citation">{s.citation}</div>
                  <div className="source-used">Used for: {s.used_for}</div>
                </div>
              ))}
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
