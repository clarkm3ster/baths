import './Portfolio.css'

export default function Portfolio({ player }) {
  const portfolio = player.portfolio

  const totalCosm = portfolio.total_cosm?.legal + portfolio.total_cosm?.data + 
                    portfolio.total_cosm?.fiscal + portfolio.total_cosm?.coordination + 
                    portfolio.total_cosm?.flourishing + portfolio.total_cosm?.narrative

  const totalChron = portfolio.total_chron?.unlock * portfolio.total_chron?.access

  const flourishing = totalCosm * totalChron

  return (
    <div className="portfolio">
      <h2>{player.name}'s Portfolio</h2>

      <div className="portfolio-stats">
        <div className="stat-card">
          <h3>Total Cosm</h3>
          <div className="stat-value">{totalCosm?.toFixed(2) || 0}</div>
          {portfolio.total_cosm && (
            <ul className="dimensions">
              <li>Legal: {portfolio.total_cosm.legal.toFixed(1)}</li>
              <li>Data: {portfolio.total_cosm.data.toFixed(1)}</li>
              <li>Fiscal: {portfolio.total_cosm.fiscal.toFixed(1)}</li>
              <li>Coordination: {portfolio.total_cosm.coordination.toFixed(1)}</li>
              <li>Flourishing: {portfolio.total_cosm.flourishing.toFixed(1)}</li>
              <li>Narrative: {portfolio.total_cosm.narrative.toFixed(1)}</li>
            </ul>
          )}
        </div>

        <div className="stat-card">
          <h3>Total Chron</h3>
          <div className="stat-value">{totalChron?.toFixed(2) || 0}</div>
          {portfolio.total_chron && (
            <ul className="dimensions">
              <li>Unlock: {portfolio.total_chron.unlock.toFixed(1)} m²</li>
              <li>Access: {portfolio.total_chron.access.toFixed(1)} hrs</li>
              <li>Permanence: {portfolio.total_chron.permanence.toFixed(2)}</li>
              <li>Catalyst: {portfolio.total_chron.catalyst.toFixed(2)}</li>
              <li>Policy: {portfolio.total_chron.policy.toFixed(2)}</li>
            </ul>
          )}
        </div>

        <div className="stat-card flourishing-card">
          <h3>Flourishing</h3>
          <div className="stat-value">{flourishing?.toFixed(2) || 0}</div>
          <p className="equation">Cosm × Chron</p>
        </div>
      </div>

      <div className="completed-productions">
        <h3>Completed Productions</h3>
        
        <div className="productions-list">
          <h4>DOMES ({portfolio.domes_completed?.length || 0})</h4>
          {portfolio.domes_completed && portfolio.domes_completed.length > 0 ? (
            <ul>
              {portfolio.domes_completed.map(prod => (
                <li key={prod.production_id}>
                  <strong>{prod.subject}</strong>
                  {prod.cosm && ` — Cosm: ${prod.cosm.legal.toFixed(1)}`}
                </li>
              ))}
            </ul>
          ) : (
            <p>No domes completed yet</p>
          )}

          <h4>SPHERES ({portfolio.spheres_completed?.length || 0})</h4>
          {portfolio.spheres_completed && portfolio.spheres_completed.length > 0 ? (
            <ul>
              {portfolio.spheres_completed.map(prod => (
                <li key={prod.production_id}>
                  <strong>{prod.subject}</strong>
                  {prod.chron && ` — Chron: ${prod.chron.unlock.toFixed(0)} m²`}
                </li>
              ))}
            </ul>
          ) : (
            <p>No spheres completed yet</p>
          )}
        </div>
      </div>

      <div className="innovations">
        <h3>Innovations ({portfolio.innovations?.length || 0})</h3>
        {portfolio.innovations && portfolio.innovations.length > 0 ? (
          <ul>
            {portfolio.innovations.map((innovation, i) => (
              <li key={i}>{innovation}</li>
            ))}
          </ul>
        ) : (
          <p>No innovations yet</p>
        )}
      </div>

      <div className="industries">
        <h3>Industries Changed ({portfolio.industries_changed?.length || 0})</h3>
        {portfolio.industries_changed && portfolio.industries_changed.length > 0 ? (
          <ul>
            {portfolio.industries_changed.map((industry, i) => (
              <li key={i}>{industry}</li>
            ))}
          </ul>
        ) : (
          <p>No industries changed yet</p>
        )}
      </div>
    </div>
  )
}
