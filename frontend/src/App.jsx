import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import HomePage from './HomePage/HomePage';
// Импортируйте другие страницы, которые вы создали

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        {/* Здесь добавьте другие маршруты */}
      </Routes>
    </Router>
  );
}

export default App;