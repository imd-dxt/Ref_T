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
        {/* Public Route for Login */}
        <Route path="/" element={<REFT />} />

        {/* Protected Route for User interface */}
        <Route
          path="/User"
          element={
            <ProtectedRoute>
              <EMP />
            </ProtectedRoute>
          }
        />
      </Routes>
      </div>
    </ProtectedRoute>
    
  )
}

export default App
