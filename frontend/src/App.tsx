import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { Layout } from './components/Layout';
import { LandingPage } from './pages/LandingPage';
import { CircumstancesPage } from './pages/CircumstancesPage';
import { DomeViewPage } from './pages/DomeViewPage';
import { ExportPage } from './pages/ExportPage';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<Layout />}>
          <Route path="/" element={<LandingPage />} />
          <Route path="/circumstances" element={<CircumstancesPage />} />
          <Route path="/dome" element={<DomeViewPage />} />
          <Route path="/export" element={<ExportPage />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
