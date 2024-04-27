import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import HomePage from "./Pages/HomePage";
import { AuthProvider } from "./AuthContext";
import LogInPage from "./Pages/LogInPage";
import RegisterPage from "./Pages/RegisterPage";
import OneTestPage from "./Pages/OneTestPage";
import AllTestsPage from "./Pages/AllTestsPage";
import AllTaskTypesPage from "./Pages/AllTaskTypesPage";
import VariantPage from "./Pages/VariantPage";
import VariantResultPage from "./Pages/VariantResultPage";

export default function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/login" element={<LogInPage />}></Route>
          <Route path="/register" element={<RegisterPage />}></Route>

          <Route path="/home" element={<HomePage />} />

          <Route path="/home/tests" element={<AllTestsPage />} />
          <Route path="/home/tests/:test_id" element={<OneTestPage />} />
          <Route
            path="/home/tests/:test_id/variant/:variant_id"
            element={<VariantResultPage />}
          />

          <Route path="/home/task_types" element={<AllTaskTypesPage />} />

          <Route path="/variant" element={<VariantPage />} />
        </Routes>
      </Router>
    </AuthProvider>
  );
}
