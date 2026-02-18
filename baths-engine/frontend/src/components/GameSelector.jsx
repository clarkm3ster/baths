import { useState } from 'react'
import './GameSelector.css'

export default function GameSelector({ gameInfo, player, onStartProduction }) {
  const [selectedGame, setSelectedGame] = useState(null)
  const [subject, setSubject] = useState('')

  const handleStart = () => {
    if (!selectedGame || !subject.trim()) return
    onStartProduction(selectedGame.type, subject)
  }

  return (
    <div className="game-selector">
      <h2>Choose Your Game</h2>
      
      <div className="games-grid">
        {gameInfo.games.map(game => (
          <div
            key={game.type}
            className={`game-card ${selectedGame?.type === game.type ? 'selected' : ''}`}
            onClick={() => setSelectedGame(game)}
          >
            <h3>{game.name}</h3>
            <p className="game-desc">{game.description}</p>
            <div className="game-currency">
              <strong>Currency:</strong> {game.currency}
            </div>
            <div className="game-dimensions">
              <strong>Dimensions:</strong>
              <ul>
                {game.dimensions.map(dim => (
                  <li key={dim}>{dim}</li>
                ))}
              </ul>
            </div>
          </div>
        ))}
      </div>

      {selectedGame && (
        <div className="start-production">
          <h3>Start {selectedGame.name} Production</h3>
          <label>
            {selectedGame.type === 'domes' ? 'Subject Name:' : 'Parcel ID:'}
            <input
              type="text"
              value={subject}
              onChange={e => setSubject(e.target.value)}
              placeholder={selectedGame.type === 'domes' ? 'Enter person name' : 'Enter parcel ID'}
            />
          </label>
          <button onClick={handleStart} disabled={!subject.trim()}>
            Start Production
          </button>
        </div>
      )}

      <div className="equation">
        <p>{gameInfo.equation}</p>
      </div>
    </div>
  )
}
