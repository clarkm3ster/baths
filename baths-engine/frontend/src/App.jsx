import { useState, useEffect } from 'react'
import './App.css'
import GameSelector from './components/GameSelector'
import ProductionPipeline from './components/ProductionPipeline'
import Portfolio from './components/Portfolio'

function App() {
  const [player, setPlayer] = useState(null)
  const [gameInfo, setGameInfo] = useState(null)
  const [view, setView] = useState('selector') // 'selector' | 'production' | 'portfolio'

  useEffect(() => {
    // Load game info
    fetch('/api/games')
      .then(res => res.json())
      .then(data => setGameInfo(data))

    // Check if player exists (for now, create demo player)
    initializePlayer()
  }, [])

  const initializePlayer = async () => {
    // For demo: create a player named "Mike"
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
    return <div className="loading">Loading BATHS Game Engine...</div>
  }

  return (
    <div className="app">
      <header>
        <h1>🏛️ BATHS</h1>
        <p className="tagline">Cosm × Chron = Flourishing</p>
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
