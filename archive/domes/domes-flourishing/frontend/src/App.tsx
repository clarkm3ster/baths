import { Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import LandingPage from './pages/LandingPage';
import PhilosophyPage from './pages/PhilosophyPage';
import DomainsPage from './pages/DomainsPage';
import DomainDetailPage from './pages/DomainDetailPage';
import DomeBuilderPage from './pages/DomeBuilderPage';
import FinancePage from './pages/FinancePage';
import GlobalPage from './pages/GlobalPage';
import FlourishingIndexPage from './pages/FlourishingIndexPage';
import CulturePage from './pages/CulturePage';
import VitalityPage from './pages/VitalityPage';
import VisionPage from './pages/VisionPage';

export default function App() {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/philosophy" element={<PhilosophyPage />} />
        <Route path="/domains" element={<DomainsPage />} />
        <Route path="/domains/:id" element={<DomainDetailPage />} />
        <Route path="/dome-builder" element={<DomeBuilderPage />} />
        <Route path="/finance" element={<FinancePage />} />
        <Route path="/global" element={<GlobalPage />} />
        <Route path="/flourishing-index" element={<FlourishingIndexPage />} />
        <Route path="/culture" element={<CulturePage />} />
        <Route path="/vitality" element={<VitalityPage />} />
        <Route path="/vision" element={<VisionPage />} />
      </Routes>
    </Layout>
  );
}
