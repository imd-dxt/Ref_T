import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css';
import EMP from './pages/EMP';
import ProtectedRoute from './pages/ProtectedRoute';
import REFT from './pages/REFT';

function App() {
  return (
    <Router>
      <div>
        <Routes>
          {/* Public Route for Login */}
          <Route path="/" element={<REFT />} />

          {/* Protected Route for User interface */}
          <Route
            path="/user"
            element={
              <ProtectedRoute>
                <EMP />
              </ProtectedRoute>
            }
          />
          <Route path="*" element={<div>Page Not Found</div>} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;