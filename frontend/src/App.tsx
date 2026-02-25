import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { DomesLayout } from './components/DomesLayout';
import { DomesLanding } from './pages/DomesLanding';
import { ProductPage } from './pages/ProductPage';
import { RunDomePage } from './pages/RunDomePage';
import { DomeOutputPage } from './pages/DomeOutputPage';
import { CircumstancesPage } from './pages/CircumstancesPage';
import { DomeViewPage } from './pages/DomeViewPage';
import { ExportPage } from './pages/ExportPage';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<DomesLayout />}>
          <Route path="/" element={<DomesLanding />} />
          <Route path="/product" element={<ProductPage />} />
          <Route path="/run" element={<RunDomePage />} />
          <Route path="/dome-output" element={<DomeOutputPage />} />
          {/* Legacy routes */}
          <Route path="/circumstances" element={<CircumstancesPage />} />
          <Route path="/dome" element={<DomeViewPage />} />
          <Route path="/export" element={<ExportPage />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
