import { useState, useEffect } from 'react'

export default function IPDashboard() {
  const [ipItems, setIpItems] = useState([])
  const [domains, setDomains] = useState([])
  const [selectedDomain, setSelectedDomain] = useState('')
  const [search, setSearch] = useState('')
  const [byDomain, setByDomain] = useState({})
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetch('/api/ip/domains').then(r => r.json()).then(d => setDomains(d.domains)).catch(() => {})
  }, [])

  useEffect(() => {
    const params = new URLSearchParams()
    if (selectedDomain) params.set('domain', selectedDomain)
    if (search) params.set('search', search)
    fetch(`/api/ip?${params}`)
      .then(r => r.json())
      .then(data => {
        setIpItems(data.ip_items)
        setByDomain(data.by_domain || {})
        setLoading(false)
      })
      .catch(() => setLoading(false))
  }, [selectedDomain, search])

  const totalIP = Object.values(byDomain).reduce((a, b) => a + b, 0)

  return (
    <div>
      <div className="page-header">
        <h2>IP Dashboard</h2>
        <p>Every innovation across all productions — categorized by domain, attributed to the practice that produced it.</p>
      </div>

      {/* Domain overview grid */}
      <div className="ip-domains-grid">
        {domains.map(d => (
          <div
            key={d.domain}
            className={`ip-domain-card ${selectedDomain === d.domain ? 'selected' : ''}`}
            onClick={() => setSelectedDomain(selectedDomain === d.domain ? '' : d.domain)}
          >
            <div className="ipd-count">{d.count}</div>
            <div className="ipd-label">{d.label}</div>
          </div>
        ))}
      </div>

      <div className="ip-summary">
        <span className="ip-total">{totalIP} total IP items</span>
        <span className="ip-domains-count">{domains.filter(d => d.count > 0).length} active domains</span>
      </div>

      <div className="search-bar">
        <input
          className="search-input"
          type="text"
          placeholder="Search IP by title, description, or practice..."
          value={search}
          onChange={e => setSearch(e.target.value)}
        />
        {selectedDomain && (
          <button className="filter-btn active" onClick={() => setSelectedDomain('')}>
            {selectedDomain.replace('_', ' ')} x
          </button>
        )}
      </div>

      {ipItems.length > 0 ? (
        <div className="ip-list">
          {ipItems.map(item => (
            <div key={item.ip_id} className="card ip-item-card">
              <div className="ip-item-header">
                <div>
                  <div className="ip-item-title">{item.title}</div>
                  <div className="ip-item-meta">
                    <span className="tag">{item.domain.replace('_', ' ')}</span>
                    <span className="ip-format">{item.format}</span>
                  </div>
                </div>
                <div className="ip-item-production">
                  <span className="ip-prod-title">{item.production_title}</span>
                  <span className="ip-stage">{item.stage_originated.replace('_', ' ')}</span>
                </div>
              </div>
              <p className="ip-item-desc">{item.description}</p>
              <div className="ip-item-footer">
                <span className="ip-practitioner">
                  {item.practitioner_name} <span className="ip-practice">({item.practice})</span>
                </span>
                <span className="ip-value">{item.value_driver}</span>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="empty-state">
          <h3>{loading ? 'Loading...' : 'No IP items yet'}</h3>
          <p>IP is generated as productions move through the pipeline. Each team member's practice produces domain-specific innovations.</p>
        </div>
      )}

      <style>{`
        .ip-domains-grid {
          display: grid;
          grid-template-columns: repeat(auto-fill, minmax(130px, 1fr));
          gap: 0.75rem;
          margin-bottom: 1.5rem;
        }
        .ip-domain-card {
          padding: 1rem;
          background: white;
          border: 1px solid var(--border);
          border-radius: var(--radius-md);
          text-align: center;
          cursor: pointer;
          transition: all 0.2s;
        }
        .ip-domain-card:hover {
          border-color: var(--accent);
          box-shadow: var(--shadow-sm);
        }
        .ip-domain-card.selected {
          background: var(--ink);
          color: white;
          border-color: var(--ink);
        }
        .ipd-count {
          font-family: 'JetBrains Mono', monospace;
          font-size: 1.5rem;
          font-weight: 600;
          margin-bottom: 0.25rem;
        }
        .ip-domain-card.selected .ipd-count { color: var(--accent-light); }
        .ipd-label {
          font-size: 0.75rem;
          font-weight: 500;
          text-transform: uppercase;
          letter-spacing: 0.04em;
          color: var(--ink-lighter);
        }
        .ip-domain-card.selected .ipd-label { color: rgba(255,255,255,0.7); }
        .ip-summary {
          display: flex;
          gap: 1.5rem;
          margin-bottom: 1.25rem;
        }
        .ip-total {
          font-family: 'JetBrains Mono', monospace;
          font-size: 0.9rem;
          font-weight: 500;
          color: var(--ink-light);
        }
        .ip-domains-count {
          font-size: 0.85rem;
          color: var(--ink-lighter);
        }
        .ip-list {
          display: flex;
          flex-direction: column;
          gap: 0.75rem;
        }
        .ip-item-card {
          display: flex;
          flex-direction: column;
          gap: 0.5rem;
        }
        .ip-item-header {
          display: flex;
          justify-content: space-between;
          align-items: flex-start;
        }
        .ip-item-title {
          font-family: 'Playfair Display', serif;
          font-weight: 600;
          font-size: 1rem;
          margin-bottom: 0.25rem;
        }
        .ip-item-meta {
          display: flex;
          align-items: center;
          gap: 0.5rem;
        }
        .ip-format {
          font-size: 0.8rem;
          color: var(--ink-lighter);
          font-style: italic;
        }
        .ip-item-production {
          text-align: right;
          flex-shrink: 0;
        }
        .ip-prod-title {
          display: block;
          font-size: 0.8rem;
          font-weight: 500;
          color: var(--ink-light);
        }
        .ip-stage {
          font-size: 0.75rem;
          color: var(--ink-lighter);
          text-transform: capitalize;
        }
        .ip-item-desc {
          font-size: 0.9rem;
          color: var(--ink-light);
          line-height: 1.5;
        }
        .ip-item-footer {
          display: flex;
          justify-content: space-between;
          align-items: center;
          padding-top: 0.5rem;
          border-top: 1px solid var(--border-light);
        }
        .ip-practitioner {
          font-size: 0.85rem;
          font-weight: 500;
        }
        .ip-practice {
          font-weight: 400;
          color: var(--ink-lighter);
          font-style: italic;
        }
        .ip-value {
          font-size: 0.8rem;
          color: var(--accent-dark);
          font-weight: 500;
        }
      `}</style>
    </div>
  )
}
