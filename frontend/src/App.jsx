import React, { createContext, useContext, useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import HomePage from './Pages/HomePage';
import { AuthProvider } from './AuthContext';
import LogInPage from './Pages/LogInPage';
import RegisterPage from './Pages/RegisterPage';

export default function App() {
  return (
    <AuthProvider>
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/login" element={<LogInPage />}></Route>
        <Route path='/register' element={<RegisterPage />}></Route>
      </Routes>
    </Router>
    </AuthProvider>
  );
}
