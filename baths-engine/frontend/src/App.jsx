import { useState, useEffect } from 'react'
import './App.css'
import GameSelector from './components/GameSelector'
import ProductionPipeline from './components/ProductionPipeline'
import Portfolio from './components/Portfolio'

function App() {
  const [player, setPlayer] = useState(null)
  const [gameInfo, setGameInfo] = useState(null)
  const [view, setView] = useState('selector')

  useEffect(() => {
    fetch('/api/games')
      .then(res => res.json())
      .then(data => setGameInfo(data))

    initializePlayer()
  }, [])

  const initializePlayer = async () => {
    const res = await fetch('/api/players?name=Mike', { method: 'POST' })
    const playerData = await res.json()
    setPlayer(playerData)
  }

  const refreshPlayer = async () => {
    if (!player) return
    const res = await fetch(`/api/players/${player.player_id}`)
    const playerData = await res.json()
    setPlayer(playerData)
  }

  const startProduction = async (gameType, subject) => {
    const res = await fetch(`/api/productions/start?player_id=${player.player_id}&game_type=${gameType}&subject=${encodeURIComponent(subject)}`, {
      method: 'POST'
    })
    if (res.ok) {
      await refreshPlayer()
      setView('production')
    }
  }

  if (!player || !gameInfo) {
    return (
      <div className="loading">
        <div className="loading-title">BATHS</div>
        <div className="loading-bar-container">
          <div className="loading-bar"></div>
        </div>
        <div className="loading-subtitle">Initializing Game Engine</div>
      </div>
    )
  }

  return (
    <div className="app">
      <header>
        <div className="header-brand">
          <div>
            <h1>BATHS</h1>
            <p className="tagline">Cosm x Chron = Flourishing</p>
          </div>
        </div>
        <nav>
          <button onClick={() => setView('selector')} className={view === 'selector' ? 'active' : ''}>
            Games
          </button>
          <button onClick={() => setView('production')} className={view === 'production' ? 'active' : ''} disabled={!player.active_production}>
            Production
          </button>
          <button onClick={() => setView('portfolio')} className={view === 'portfolio' ? 'active' : ''}>
            Portfolio
          </button>
        </nav>
      </header>

      <main>
        {view === 'selector' && (
          <GameSelector
            gameInfo={gameInfo}
            player={player}
            onStartProduction={startProduction}
          />
        )}

        {view === 'production' && player.active_production && (
          <ProductionPipeline
            player={player}
            production={player.active_production}
            onUpdate={refreshPlayer}
          />
        )}

        {view === 'portfolio' && (
          <Portfolio player={player} />
        )}
      </main>
    </div>
  )
}

export default App
