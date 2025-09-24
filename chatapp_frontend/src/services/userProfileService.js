import api from '../api/api';

export const userProfileService = {
  getUserDetails: async (setIsLoading) => {
    try {
      const response = await api.get("/profile/");
      setIsLoading(false);
      return response.data;
    } catch {
      setIsLoading(true);
      return null; // error interceptor already handles toast
    }
  }
}