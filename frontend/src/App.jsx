import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css';
import EMP from './pages/EMP';
import ProtectedRoute from './pages/ProtectedRoute';
import REFT from './pages/REFT';
import Login from './pages/Login';

function App() {
  

  return (
    <ProtectedRoute>
      <div>
        <Routes>
          <Route path="/login" element={<REFT />} />
          <Route path="/main" element={<EMP />} />
          <Route path="*" element={<div>Page Not Found</div>} />
        </Routes>
      </div>
    </ProtectedRoute>
    
  )
}

export default App
