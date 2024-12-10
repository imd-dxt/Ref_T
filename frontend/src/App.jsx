import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css';
import EMP from './pages/EMP';
import ProtectedRoute from './pages/ProtectedRoute';
import REFT from './pages/REFT';

function App() {
  

  return (
    <Router>
      <div>
<<<<<<< HEAD
        <Routes>
          <Route path="/login" element={<REFT />} />
          <Route path="/main" element={<EMP />} />
          <Route path="*" element={<div>Page Not Found</div>} />
        </Routes>
=======
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
>>>>>>> 9a59c636fb4563dc6206f022b2eba0d2f9daac04
      </div>
    </Router>
    
  )
}

export default App
