import './App.css'
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { Login } from './components/auth/Login';
import Dashboard from './components/dashboard/dashboard';
import ProtectedRoute from './components/auth/ProtectedRoute';

function App() {
  return (
    <Router>
      {/* Public Routes */}
      <Routes>
        <Route path='/login' element={<Login/>}/>
      </Routes>

      {/* Protected Routes */}
      <Routes>
          <Route path='/' element={
            <ProtectedRoute>
              <Dashboard/>
            </ProtectedRoute>}
        />
      </Routes>

    </Router>
  )
}

export default App
