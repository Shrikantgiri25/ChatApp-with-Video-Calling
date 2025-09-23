import './App.css'
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Login  from './components/auth/Login';
import Dashboard from './components/dashboard/dashboard';
import ProtectedRoute from './components/auth/ProtectedRoute';
import EmailVerifyPage from './components/auth/EmailVerify';
import SetPasswordPage from './components/auth/SetPasswordPage';
function App() {
  return (
    <Router>
      {/* Public Routes */}
      <Routes>
        <Route path='/login' element={<Login/>}/>
        <Route path='/register' element={<Login/>}/>
        <Route path="/verify/:token/email/" element={<EmailVerifyPage />} />
        <Route path="user/:token/set-password/" element={<SetPasswordPage />} />
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
