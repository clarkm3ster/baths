import { useState } from 'react'
import './ProductionPipeline.css'

const STAGES = [
  { key: 'development', label: 'Development', icon: '01', description: 'Research & Planning' },
  { key: 'pre_production', label: 'Pre-Production', icon: '02', description: 'Design & Architecture' },
  { key: 'production', label: 'Production', icon: '03', description: 'Build & Execute' },
  { key: 'post_production', label: 'Post-Production', icon: '04', description: 'Verify & Innovate' },
  { key: 'distribution', label: 'Distribution', icon: '05', description: 'Score & Package' }
]

function StageDataDisplay({ stageData, gameType }) {
  if (!stageData || Object.keys(stageData).length === 0) return null

  const renderValue = (val, depth = 0) => {
    if (depth > 4) return <span className="data-string">{JSON.stringify(val)}</span>
    if (val === null || val === undefined) return <span className="data-null">--</span>
    if (typeof val === 'boolean') return <span className={`data-bool ${val ? 'true' : 'false'}`}>{val ? 'YES' : 'NO'}</span>
    if (typeof val === 'number') return <span className="data-number">{val.toLocaleString()}</span>
    if (typeof val === 'string') return <span className="data-string">{val}</span>
    if (Array.isArray(val)) {
      if (val.length === 0) return <span className="data-null">None</span>
      return (
        <div className="data-array">
          {val.map((item, i) => (
            <div key={i} className="data-array-item">
              {typeof item === 'object' ? renderValue(item, depth + 1) : <span className="data-string">{String(item)}</span>}
            </div>
          ))}
        </div>
      )
    }
    if (typeof val === 'object') {
      return (
        <div className={`data-object ${depth > 0 ? 'nested' : ''}`}>
          {Object.entries(val).map(([k, v]) => (
            <div key={k} className="data-row">
              <span className="data-key">{k.replace(/_/g, ' ')}</span>
              {renderValue(v, depth + 1)}
            </div>
          ))}
        </div>
      )
    }
    return <span>{String(val)}</span>
  }

  return (
    <div className="stage-data-display">
      <h3 className="data-title">PRODUCTION INTEL</h3>
      <div className="data-stages">
        {Object.entries(stageData).map(([stageName, data]) => (
          <details key={stageName} className="data-stage-section" open>
            <summary className="data-stage-header">
              <span className="stage-name">{stageName.replace(/_/g, ' ').toUpperCase()}</span>
              <span className="toggle-icon"></span>
            </summary>
            <div className="data-stage-content">
              {renderValue(data)}
            </div>
          </details>
        ))}
      </div>
    </div>
  )
}

export default function ProductionPipeline({ player, production, onUpdate }) {
  const [working, setWorking] = useState(false)
  const [lastMessage, setLastMessage] = useState(null)

  const isDomes = production.game_type === 'domes'
  const gameClass = isDomes ? 'domes' : 'spheres'

  const handleAdvance = async () => {
    setWorking(true)
    try {
      const res = await fetch(`/api/productions/${production.production_id}/advance`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          production_id: production.production_id,
          action: `advance_${production.stage}`,
          data: {}
        })
      })

      const result = await res.json()

      if (result.success) {
        setLastMessage(result.message)
        await onUpdate()
      } else {
        setLastMessage(`Error: ${result.message}`)
      }
    } catch (err) {
      setLastMessage(`Failed: ${err.message}`)
    } finally {
      setWorking(false)
    }
  }

  const currentStageIndex = STAGES.findIndex(s => s.key === production.stage)
  const isComplete = production.progress >= 100

  return (
    <div className={`production-pipeline ${gameClass}`}>
      <div className="pipeline-hero">
        <div className="pipeline-hero-bg"></div>
        <div className="pipeline-hero-content">
          <div className="pipeline-badge">{isDomes ? 'DOMES' : 'SPHERES'} PRODUCTION</div>
          <h2 className="pipeline-title">{production.subject}</h2>
          <div className="pipeline-meta">
            <span className="meta-item">Stage {currentStageIndex + 1} of 5</span>
            <span className="meta-divider">|</span>
            <span className="meta-item">{production.progress.toFixed(0)}% Complete</span>
          </div>
        </div>
      </div>

      <div className="pipeline-content">
        <div className="stages-track">
          <div className="track-line">
            <div className="track-fill" style={{ width: `${(currentStageIndex / (STAGES.length - 1)) * 100}%` }}></div>
          </div>

          {STAGES.map((stage, index) => {
            const isCurrent = index === currentStageIndex
            const isCompleted = index < currentStageIndex
            const isFuture = index > currentStageIndex

            return (
              <div key={stage.key} className={`stage-node ${isCurrent ? 'current' : ''} ${isCompleted ? 'completed' : ''} ${isFuture ? 'future' : ''}`}>
                <div className="node-circle">
                  {isCompleted ? (
                    <svg viewBox="0 0 24 24" className="check-icon"><polyline points="20 6 9 17 4 12" fill="none" stroke="currentColor" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round"/></svg>
                  ) : (
                    <span className="node-number">{stage.icon}</span>
                  )}
                </div>
                <div className="node-info">
                  <div className="node-label">{stage.label}</div>
                  <div className="node-desc">{stage.description}</div>
                </div>
              </div>
            )
          })}
        </div>

        <div className="progress-section">
          <div className="progress-labels">
            <span>PROGRESS</span>
            <span className="progress-pct">{production.progress.toFixed(0)}%</span>
          </div>
          <div className="progress-track">
            <div className="progress-fill" style={{ width: `${production.progress}%` }}>
              <div className="progress-glow"></div>
            </div>
          </div>
        </div>

        {lastMessage && (
          <div className="status-message">
            <div className="message-indicator"></div>
            <p>{lastMessage}</p>
          </div>
        )}

        <div className="action-section">
          {!isComplete ? (
            <button className="advance-btn" onClick={handleAdvance} disabled={working}>
              {working ? (
                <>
                  <span className="spinner"></span>
                  <span>PROCESSING...</span>
                </>
              ) : (
                <>
                  <span>ADVANCE TO NEXT STAGE</span>
                  <span className="btn-arrow">&#8594;</span>
                </>
              )}
            </button>
          ) : (
            <div className="complete-badge">
              <div className="complete-icon">&#10003;</div>
              <div>
                <div className="complete-title">PRODUCTION COMPLETE</div>
                <div className="complete-sub">Check your Portfolio for results</div>
              </div>
            </div>
          )}
        </div>

        <StageDataDisplay stageData={production.stage_data} gameType={production.game_type} />
      </div>
    </div>
  )
}
