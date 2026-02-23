import { useState, useEffect } from 'react'
import { BrowserRouter, Routes, Route, useLocation } from 'react-router-dom'
import './App.css'
import GameSelector from './components/GameSelector'
import Portfolio from './components/Portfolio'
import DomesGame from './games/domes/DomesGame'
import SpheresGame from './games/spheres/SpheresGame'
import DomesIndex from './portfolio/DomesIndex'
import DomeProductionPage from './portfolio/DomeProductionPage'
import SpheresIndex from './portfolio/SpheresIndex'
import SphereProductionPage from './portfolio/SphereProductionPage'

// ── Game Engine (original app at /) ──────────────────────────────
function GameEngine() {
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

  const activeProduction = player.active_production
  const gameType = activeProduction?.game_type

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
          <button onClick={() => setView('production')} className={view === 'production' ? 'active' : ''} disabled={!activeProduction}>
            {activeProduction ? (gameType === 'domes' ? 'Dome' : 'Sphere') : 'Production'}
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

        {view === 'production' && activeProduction && gameType === 'domes' && (
          <DomesGame
            player={player}
            production={activeProduction}
            onUpdate={refreshPlayer}
            onBack={() => setView('selector')}
          />
        )}

        {view === 'production' && activeProduction && gameType === 'spheres' && (
          <SpheresGame
            player={player}
            production={activeProduction}
            onUpdate={refreshPlayer}
            onBack={() => setView('selector')}
          />
        )}

        {view === 'portfolio' && (
          <Portfolio player={player} />
        )}
      </main>
    </div>
  )
}

// ── Root App with Routing ────────────────────────────────────────
function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Portfolio Sites — public pages */}
        <Route path="/domes" element={<DomesIndex />} />
        <Route path="/domes/:id" element={<DomeProductionPage />} />
        <Route path="/spheres" element={<SpheresIndex />} />
        <Route path="/spheres/:id" element={<SphereProductionPage />} />

        {/* Game Engine — production interface */}
        <Route path="/*" element={<GameEngine />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
