import './App.css'
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Loginpage from './Webpages/Loginpage';
import Mainpage from './Webpages/Mainpage';
import RBAC from './Webpages/RBAC';
import ProtectedRoute from './Webpages/ProtectedRoute';
function App() {
  
  return (
    <>
      <Router>
        <Routes>
          <Route path="/login" element={<Loginpage />} />   
          <Route path= "/" element={<Mainpage />}/> 
          <Route path= "/RBAC"element={<ProtectedRoute><RBAC /></ProtectedRoute>}/>
        </Routes>
      </Router>
    </>
  )
}

export default App
