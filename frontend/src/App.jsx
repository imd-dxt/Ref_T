import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css';
import EMP from './pages/EMP';
import REFT from './pages/REFT';

function App() {
  

  return (
    <Router>
      <div>
        <Routes>
          <Route path="/login" element={<REFT />} />
          <Route path="/main" element={<EMP />} />
          <Route path="*" element={<div>Page Not Found</div>} />
        </Routes>
      </div>
    </Router>
  )
}

export default App
