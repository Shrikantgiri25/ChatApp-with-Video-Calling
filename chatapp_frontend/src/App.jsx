import './App.css'
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Login  from './components/Auth/Login';
import Dashboard from './components/Dashboard/Dashboard';
import ProtectedRoute from './components/Auth/ProtectedRoute';
import EmailVerifyPage from './components/Auth/EmailVerify';
import SetPasswordPage from './components/Auth/SetPasswordPage';
import OnBoardingPage from './components/OnboardingPage/OnBoardingPage';
import MainLayout from './components/MainLayout/MainLayout';

function App() {
  return (
    <Router>
      {/* Public Routes */}
      <Routes>
        <Route path='/login' element={<Login/>}/>
        <Route path='/register' element={<Login/>}/>
        <Route path="/verify/:token/email/" element={<EmailVerifyPage />} />
        <Route path="user/:token/set-password/" element={<SetPasswordPage />} />
      
      {/* Protected Routes */}
          <Route path='/onboarding/profile' element={
            <ProtectedRoute>
              <OnBoardingPage/>
            </ProtectedRoute>}
            />
      {/* SideNavbar Routes*/}
          <Route element={<MainLayout/>}>
            <Route path='/dashboard' element={
            <ProtectedRoute>
              <Dashboard/>
            </ProtectedRoute>}
            />
          </Route>
      </Routes>

    </Router>
  )
}

export default App
