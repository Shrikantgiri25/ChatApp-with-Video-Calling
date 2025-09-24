import React, { useEffect, useState } from 'react'
import { userProfileService } from '../../services/userProfileService';
import LoadingScreen from '../spinner/Spinner';

const Dashboard = () => {
  const [isLoading, setIsLoading] = useState(true);

  // Create a large spinner icon

  useEffect(()=>{
    userProfileService.getUserDetails(setIsLoading)
  }, [])
  return (
    <>
      {
        isLoading ? 
        <LoadingScreen/>
        :
        <div>
          <h1>Chat App with Video Calling</h1>
          <p>Welcome to the Chat App!</p>
        </div> 
      }
    </>
  )
}

export default Dashboard;