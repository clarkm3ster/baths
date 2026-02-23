import { useState, useEffect } from 'react'
import './App.css'
import Roster from './views/Roster'
import Principals from './views/Principals'
import ProjectBoard from './views/ProjectBoard'
import ProjectSourcing from './views/ProjectSourcing'
import TeamAssembly from './views/TeamAssembly'
import IPDashboard from './views/IPDashboard'
import Leaderboard from './views/Leaderboard'
import TalentDetail from './views/TalentDetail'
import PrincipalDetail from './views/PrincipalDetail'
import ProjectDetail from './views/ProjectDetail'

const NAV_ITEMS = [
  { key: 'roster', label: 'Roster' },
  { key: 'principals', label: 'Principals' },
  { key: 'projects', label: 'Projects' },
  { key: 'sourcing', label: 'Sourcing' },
  { key: 'assembly', label: 'Assembly' },
  { key: 'ip', label: 'IP' },
  { key: 'leaderboard', label: 'Board' },
]

export default function App() {
  const [view, setView] = useState('roster')
  const [stats, setStats] = useState(null)
  // For detail views
  const [detailId, setDetailId] = useState(null)
  const [detailType, setDetailType] = useState(null) // 'talent', 'principal', 'project'

  useEffect(() => {
    fetch('/api/stats').then(r => r.json()).then(setStats).catch(() => {})
  }, [view])

  const navigateTo = (v) => {
    setView(v)
    setDetailId(null)
    setDetailType(null)
  }

  const openDetail = (type, id) => {
    setDetailType(type)
    setDetailId(id)
  }

  const closeDetail = () => {
    setDetailId(null)
    setDetailType(null)
  }

  // Detail overlays
  if (detailType === 'talent' && detailId) {
    return (
      <div className="app">
        <Header stats={stats} view={view} navigateTo={navigateTo} />
        <main>
          <TalentDetail talentId={detailId} onBack={closeDetail} onOpenProject={(id) => openDetail('project', id)} />
        </main>
      </div>
    )
  }
  if (detailType === 'principal' && detailId) {
    return (
      <div className="app">
        <Header stats={stats} view={view} navigateTo={navigateTo} />
        <main>
          <PrincipalDetail principalId={detailId} onBack={closeDetail} onOpenProject={(id) => openDetail('project', id)} />
        </main>
      </div>
    )
  }
  if (detailType === 'project' && detailId) {
    return (
      <div className="app">
        <Header stats={stats} view={view} navigateTo={navigateTo} />
        <main>
          <ProjectDetail
            projectId={detailId}
            onBack={closeDetail}
            onOpenTalent={(id) => openDetail('talent', id)}
            onOpenPrincipal={(id) => openDetail('principal', id)}
          />
        </main>
      </div>
    )
  }

  return (
    <div className="app">
      <Header stats={stats} view={view} navigateTo={navigateTo} />
      <main>
        {view === 'roster' && <Roster onOpenTalent={(id) => openDetail('talent', id)} />}
        {view === 'principals' && <Principals onOpenPrincipal={(id) => openDetail('principal', id)} />}
        {view === 'projects' && <ProjectBoard onOpenProject={(id) => openDetail('project', id)} />}
        {view === 'sourcing' && <ProjectSourcing onOpenProject={(id) => openDetail('project', id)} />}
        {view === 'assembly' && <TeamAssembly onOpenProject={(id) => openDetail('project', id)} onOpenTalent={(id) => openDetail('talent', id)} />}
        {view === 'ip' && <IPDashboard />}
        {view === 'leaderboard' && <Leaderboard onOpenTalent={(id) => openDetail('talent', id)} onOpenPrincipal={(id) => openDetail('principal', id)} />}
      </main>
    </div>
  )
}

function Header({ stats, view, navigateTo }) {
  return (
    <header>
      <div className="header-left">
        <div className="header-brand" onClick={() => navigateTo('roster')}>
          <h1 className="logo">CHRON</h1>
          <span className="logo-sub">Talent Agent</span>
        </div>
        {stats && (
          <div className="header-stats">
            <span className="stat-pill">{stats.roster_size} practitioners</span>
            <span className="stat-pill">{stats.principals_count} principals</span>
            <span className="stat-pill active-pill">{stats.active_productions} active</span>
          </div>
        )}
      </div>
      <nav>
        {NAV_ITEMS.map(item => (
          <button
            key={item.key}
            className={view === item.key ? 'active' : ''}
            onClick={() => navigateTo(item.key)}
          >
            {item.label}
          </button>
        ))}
      </nav>
    </header>
  )
}
