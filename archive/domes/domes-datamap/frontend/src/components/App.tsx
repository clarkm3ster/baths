import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { TopNav } from "./nav/TopNav";
import { SystemsPage } from "./systems/SystemsPage";
import { MatrixPage } from "./matrix/MatrixPage";
import { GapsPage } from "./gaps/GapsPage";
import { PersonPage } from "./person/PersonPage";
import { BridgesPage } from "./bridges/BridgesPage";
import { ApiDocsPage } from "./docs/ApiDocsPage";

export function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen flex flex-col">
        <TopNav />
        <main className="flex-1">
          <Routes>
            <Route path="/" element={<Navigate to="/systems" replace />} />
            <Route path="/systems" element={<SystemsPage />} />
            <Route path="/matrix" element={<MatrixPage />} />
            <Route path="/gaps" element={<GapsPage />} />
            <Route path="/person" element={<PersonPage />} />
            <Route path="/bridges" element={<BridgesPage />} />
            <Route path="/api-docs" element={<ApiDocsPage />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}
