import api from '../api/api';
import { LOGIN_SUCCESS } from '../store/actiontypes/constants';
export const userProfileService = {
  getUserDetails: async (setIsLoading = () => {}, dispatch, navigate) => {
    try {
      const response = await api.get("/profile/");
      dispatch({type: LOGIN_SUCCESS, payload: response?.data?.data})
      if(response.data.data.status === "NEW_USER"){
        navigate("/onboarding/profile");
      }
      setIsLoading(false);
      // return response.data;
    } catch {
      setIsLoading(true);
      return null; // error interceptor already handles toast
    }
  },
patchUserDetails: async (values, setSubmitting = () => {}, navigate) => {
  try {
    const formData = new FormData();
    if (values.bio) formData.append("profile.bio", values.bio);
    if (values.profile_picture) formData.append("profile.profile_picture", values.profile_picture);

    const response = await api.patch("/profile/", formData, {
      headers: {
        "Content-Type": "multipart/form-data", // very important
      },
    });

    if (response.status === 200) {
      navigate("/chats");
    }
  } catch (error) {
    console.error("Patch user profile failed:", error);
  } finally {
    setSubmitting(false);
  }
}
}