import { useState } from 'react'
import './ProductionPipeline.css'

const STAGES = [
  { key: 'development', label: 'Development' },
  { key: 'pre_production', label: 'Pre-Production' },
  { key: 'production', label: 'Production' },
  { key: 'post_production', label: 'Post-Production' },
  { key: 'distribution', label: 'Distribution' }
]

export default function ProductionPipeline({ player, production, onUpdate }) {
  const [working, setWorking] = useState(false)

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
        await onUpdate()
      } else {
        alert(`Error: ${result.message}`)
      }
    } catch (err) {
      alert(`Failed to advance: ${err.message}`)
    } finally {
      setWorking(false)
    }
  }

  const currentStageIndex = STAGES.findIndex(s => s.key === production.stage)

  return (
    <div className="production-pipeline">
      <div className="production-header">
        <h2>{production.game_type.toUpperCase()} Production</h2>
        <div className="subject">
          <strong>Subject:</strong> {production.subject}
        </div>
      </div>

      <div className="pipeline-stages">
        {STAGES.map((stage, index) => (
          <div
            key={stage.key}
            className={`stage ${index === currentStageIndex ? 'current' : ''} ${index < currentStageIndex ? 'complete' : ''}`}
          >
            <div className="stage-icon">
              {index < currentStageIndex ? '✓' : index === currentStageIndex ? '▶' : '○'}
            </div>
            <div className="stage-label">{stage.label}</div>
          </div>
        ))}
      </div>

      <div className="progress-bar">
        <div className="progress-fill" style={{ width: `${production.progress}%` }}></div>
        <span className="progress-text">{production.progress.toFixed(0)}%</span>
      </div>

      <div className="stage-actions">
        <button onClick={handleAdvance} disabled={working || production.progress >= 100}>
          {working ? 'Working...' : 'Advance Stage'}
        </button>
      </div>

      {production.stage_data && Object.keys(production.stage_data).length > 0 && (
        <div className="stage-data">
          <h3>Production Data</h3>
          <pre>{JSON.stringify(production.stage_data, null, 2)}</pre>
        </div>
      )}
    </div>
  )
}
