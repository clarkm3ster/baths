import { BrowserRouter, Routes, Route } from 'react-router-dom';
import TopNav from './nav/TopNav';
import LandingPage from './landing/LandingPage';
import IntakePage from './intake/IntakePage';
import DomePage from './dome/DomePage';
import CostDashboard from './cost/CostDashboard';
import ProfilesPage from './profiles/ProfilesPage';
import { ComparePage } from './compare/ComparePage';
import { TimelinePage } from './timeline/TimelinePage';

export default function App() {
  return (
    <BrowserRouter>
      <div className="min-h-full flex flex-col">
        <TopNav />
        <main className="flex-1">
          <Routes>
            <Route path="/" element={<LandingPage />} />
            <Route path="/intake" element={<IntakePage />} />
            <Route path="/dome/:id" element={<DomePage />} />
            <Route path="/cost/:id" element={<CostDashboard />} />
            <Route path="/profiles" element={<ProfilesPage />} />
            <Route path="/compare" element={<ComparePage />} />
            <Route path="/timeline/:id" element={<TimelinePage />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}
