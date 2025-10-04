import './App.css'
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import Login  from './components/Auth/Login';
import ProtectedRoute from './components/Auth/ProtectedRoute';
import EmailVerifyPage from './components/Auth/EmailVerify';
import SetPasswordPage from './components/Auth/SetPasswordPage';
import OnBoardingPage from './components/OnboardingPage/OnBoardingPage';
import MainLayout from './components/MainLayout/MainLayout';
import ChatListPane from './components/MiddlePane/ChatListPane/ChatListPane';
import ChatContentPane from './components/ContentPane/ChatContentPane';
import UserListPane from './components/MiddlePane/UserListPane/UserListPane';
import UserListContentPane from './components/ContentPane/UserListContentPane';
import Dashboard from "./components/Dashboard/Dashboard"
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
          <Route element={<ProtectedRoute />}>
          <Route path='/onboarding/profile' element={<OnBoardingPage/>}/>
          {/* SideNavbar Routes*/}
          <Route path='/' element={<Navigate to="chats"/>} />
            {/* Chat Routes*/}
            <Route path='/chats' element={<MainLayout/>}>
              <Route index element={<Dashboard />} /> 
              <Route path='list' element={<ChatListPane />} />
              <Route path=":chatId" element={<ChatContentPane />} />
            </Route>

            {/* User Routes*/}
            <Route path='/users' element={<MainLayout/>}>
              <Route index element={<Dashboard />} /> 
              <Route path='list' element={<UserListPane />} />
              <Route path=":userId" element={<UserListContentPane />} />
            </Route>

            <Route path="*" element={<Navigate to="/chats" replace />} />
          </Route>
      </Routes>

    </Router>
  )
}

export default App
