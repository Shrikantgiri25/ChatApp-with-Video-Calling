import api from '../api/api';
import { LOGIN_SUCCESS } from '../store/actiontypes/constants';

export const userProfileService = {
  getUserDetails: async (setIsLoading = () => {}, dispatch, navigate) => {
    try {
      const response = await api.get("/profile/");
      dispatch({ type: LOGIN_SUCCESS, payload: response?.data?.data });
      
      if (response.data.data.status === "NEW_USER") {
        navigate("/onboarding/profile");
      }
      
      setIsLoading(false);
    } catch (error) {
      setIsLoading(true);
      console.error("Get user profile failed:", error);
      return null;
    }
  },

  patchUserDetails: async (formData) => {
    try {
      const response = await api.patch("/profile/", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
      
      return response;
    } catch (error) {
      console.error("Patch user profile failed:", error);
      throw error; // Re-throw to handle in component
    }
  }
};