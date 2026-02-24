import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Home from './views/Home'
import Production from './views/Production'

export default function App() {
  return (
    <BrowserRouter>
      <div className="app">
        <header className="site-header">
          <a href="/" className="site-logo">domes.cc</a>
          <span className="site-tagline">DOMES Productions</span>
        </header>
        <main>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/production/:id" element={<Production />} />
          </Routes>
        </main>
        <footer className="site-footer">
          <p>domes.cc — Completed DOMES productions from the Chron Talent Agent</p>
        </footer>
      </div>
    </BrowserRouter>
  )
}
