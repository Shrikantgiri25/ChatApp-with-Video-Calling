import React, { useEffect, useState } from 'react';
import { useDispatch, useSelector } from "react-redux";
import { useNavigate } from 'react-router-dom';
import LoadingScreen from '../Spinner/Spinner';
import { UserProfileDetails } from '../../store/selectors/authselectors';
import { userProfileService } from '../../services/userProfileService';

const Dashboard = () => {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const userProfileData = useSelector(UserProfileDetails);

  // Only loading if data is NOT present
  const [isLoading, setIsLoading] = useState(!userProfileData);

  useEffect(() => {
    // Call API only if data is missing
    if (!userProfileData) {
      userProfileService.getUserDetails(setIsLoading, dispatch, navigate);
    } else {
      setIsLoading(false); // Data already present, no API call
    }
  }, [userProfileData, dispatch, navigate]);

  return (
    <>
      {isLoading ? (
        <LoadingScreen />
      ) : (
        <div>
          <h1>Chat App with Video Calling</h1>
          <p>Welcome to the Chat App!</p>
        </div>
      )}
    </>
  );
};

export default Dashboard;
