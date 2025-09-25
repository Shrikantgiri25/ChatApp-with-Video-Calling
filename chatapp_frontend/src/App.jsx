import './App.css'
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Login  from './components/Auth/Login';
import Dashboard from './components/Dashboard/Dashboard';
import ProtectedRoute from './components/Auth/ProtectedRoute';
import EmailVerifyPage from './components/Auth/EmailVerify';
import SetPasswordPage from './components/Auth/SetPasswordPage';
import OnBoardingPage from './components/OnboardingPage/OnBoardingPage';


function App() {
  return (
    <Router>
      {/* Public Routes */}

      {/* Protected Routes */}
      <Routes>
        <Route path='/login' element={<Login/>}/>
        <Route path='/register' element={<Login/>}/>
        <Route path="/verify/:token/email/" element={<EmailVerifyPage />} />
        <Route path="user/:token/set-password/" element={<SetPasswordPage />} />
          <Route path='/dashboard' element={
            <ProtectedRoute>
              <Dashboard/>
            </ProtectedRoute>}
          />
          <Route path='/onboarding/profile' element={
            <ProtectedRoute>
              <OnBoardingPage/>
            </ProtectedRoute>}
            />
      </Routes>

    </Router>
  )
}

export default App
