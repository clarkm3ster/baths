import { useState, useEffect, useRef } from 'react'
import './GameSelector.css'

function ParticleField({ color, count = 30 }) {
  const canvasRef = useRef(null)

  useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas) return
    const ctx = canvas.getContext('2d')
    let animId

    const resize = () => {
      canvas.width = canvas.parentElement.offsetWidth
      canvas.height = canvas.parentElement.offsetHeight
    }
    resize()
    window.addEventListener('resize', resize)

    const particles = Array.from({ length: count }, () => ({
      x: Math.random() * canvas.width,
      y: Math.random() * canvas.height,
      vx: (Math.random() - 0.5) * 0.3,
      vy: (Math.random() - 0.5) * 0.3,
      size: Math.random() * 2 + 0.5,
      opacity: Math.random() * 0.5 + 0.1
    }))

    const draw = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height)
      particles.forEach(p => {
        p.x += p.vx
        p.y += p.vy
        if (p.x < 0 || p.x > canvas.width) p.vx *= -1
        if (p.y < 0 || p.y > canvas.height) p.vy *= -1
        ctx.beginPath()
        ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2)
        ctx.fillStyle = `${color}, ${p.opacity})`
        ctx.fill()
      })
      animId = requestAnimationFrame(draw)
    }
    draw()

    return () => {
      cancelAnimationFrame(animId)
      window.removeEventListener('resize', resize)
    }
  }, [color, count])

  return <canvas ref={canvasRef} className="particle-canvas" />
}

export default function GameSelector({ gameInfo, player, onStartProduction }) {
  const [selectedGame, setSelectedGame] = useState(null)
  const [subject, setSubject] = useState('')
  const [hovered, setHovered] = useState(null)

  const handleStart = () => {
    if (!selectedGame || !subject.trim()) return
    onStartProduction(selectedGame.type, subject)
  }

  const gameIcons = {
    domes: (
      <svg viewBox="0 0 100 100" className="game-icon-svg">
        <defs>
          <linearGradient id="domeGrad" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="#00e5ff" />
            <stop offset="100%" stopColor="#0288d1" />
          </linearGradient>
        </defs>
        <path d="M15 75 Q15 25 50 15 Q85 25 85 75" fill="none" stroke="url(#domeGrad)" strokeWidth="2.5" opacity="0.8"/>
        <path d="M22 75 Q22 32 50 22 Q78 32 78 75" fill="none" stroke="url(#domeGrad)" strokeWidth="1.5" opacity="0.5"/>
        <path d="M30 75 Q30 40 50 30 Q70 40 70 75" fill="none" stroke="url(#domeGrad)" strokeWidth="1" opacity="0.3"/>
        <line x1="50" y1="15" x2="50" y2="75" stroke="url(#domeGrad)" strokeWidth="1" opacity="0.3"/>
        <line x1="15" y1="75" x2="85" y2="75" stroke="url(#domeGrad)" strokeWidth="2" opacity="0.6"/>
        <circle cx="50" cy="65" r="4" fill="#00e5ff" opacity="0.8"/>
        <circle cx="50" cy="65" r="8" fill="none" stroke="#00e5ff" strokeWidth="0.5" opacity="0.4"/>
      </svg>
    ),
    spheres: (
      <svg viewBox="0 0 100 100" className="game-icon-svg">
        <defs>
          <linearGradient id="sphereGrad" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="#ff6d00" />
            <stop offset="100%" stopColor="#e65100" />
          </linearGradient>
        </defs>
        <circle cx="50" cy="50" r="35" fill="none" stroke="url(#sphereGrad)" strokeWidth="2" opacity="0.8"/>
        <ellipse cx="50" cy="50" rx="35" ry="15" fill="none" stroke="url(#sphereGrad)" strokeWidth="1" opacity="0.4"/>
        <ellipse cx="50" cy="50" rx="15" ry="35" fill="none" stroke="url(#sphereGrad)" strokeWidth="1" opacity="0.4"/>
        <circle cx="50" cy="50" r="20" fill="none" stroke="url(#sphereGrad)" strokeWidth="1" opacity="0.3"/>
        <circle cx="50" cy="50" r="5" fill="#ff6d00" opacity="0.6"/>
        <circle cx="50" cy="50" r="3" fill="#ffab40" opacity="0.9"/>
      </svg>
    )
  }

  return (
    <div className="game-selector">
      <div className="selector-hero">
        <div className="hero-bg"></div>
        <div className="hero-content">
          <h2 className="selector-title">SELECT YOUR GAME</h2>
          <p className="selector-subtitle">Choose your path to Flourishing</p>
        </div>
      </div>

      <div className="games-showcase">
        {gameInfo.games.map(game => {
          const isDomes = game.type === 'domes'
          const isSelected = selectedGame?.type === game.type
          const isHovered = hovered === game.type

          return (
            <div
              key={game.type}
              className={`game-card ${game.type} ${isSelected ? 'selected' : ''} ${isHovered ? 'hovered' : ''}`}
              onClick={() => setSelectedGame(game)}
              onMouseEnter={() => setHovered(game.type)}
              onMouseLeave={() => setHovered(null)}
            >
              <ParticleField
                color={isDomes ? 'rgba(0, 229, 255' : 'rgba(255, 109, 0'}
                count={isHovered ? 50 : 25}
              />

              <div className="card-glow"></div>

              <div className="card-content">
                <div className="card-icon">
                  {gameIcons[game.type]}
                </div>

                <div className="card-badge">{isDomes ? 'GAME 01' : 'GAME 02'}</div>

                <h3 className="card-title">{game.name}</h3>

                <p className="card-description">{game.description}</p>

                <div className="card-currency">
                  <span className="currency-label">Currency</span>
                  <span className="currency-value">{game.currency}</span>
                </div>

                <div className="card-dimensions">
                  {game.dimensions.map(dim => (
                    <span key={dim} className="dimension-tag">{dim}</span>
                  ))}
                </div>

                <div className="card-select-indicator">
                  {isSelected ? 'SELECTED' : 'SELECT'}
                </div>
              </div>
            </div>
          )
        })}
      </div>

      {selectedGame && (
        <div className={`start-panel ${selectedGame.type}`}>
          <div className="panel-header">
            <div className="panel-accent"></div>
            <h3>BEGIN {selectedGame.name} PRODUCTION</h3>
          </div>

          <div className="panel-body">
            <div className="input-group">
              <label className="input-label">
                {selectedGame.type === 'domes' ? 'SUBJECT NAME' : 'PARCEL ID'}
              </label>
              <div className="input-wrapper">
                <input
                  type="text"
                  value={subject}
                  onChange={e => setSubject(e.target.value)}
                  placeholder={selectedGame.type === 'domes' ? 'Enter person name...' : 'Enter parcel ID...'}
                  onKeyDown={e => e.key === 'Enter' && handleStart()}
                />
                <div className="input-glow"></div>
              </div>
            </div>

            <button className="launch-btn" onClick={handleStart} disabled={!subject.trim()}>
              <span className="btn-text">LAUNCH PRODUCTION</span>
              <span className="btn-icon">&#9654;</span>
            </button>
          </div>
        </div>
      )}

      <div className="equation-display">
        <div className="eq-line"></div>
        <span className="eq-text">{gameInfo.equation}</span>
        <div className="eq-line"></div>
      </div>
    </div>
  )
}
