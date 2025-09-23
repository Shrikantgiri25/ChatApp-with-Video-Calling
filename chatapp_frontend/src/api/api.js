// api.js
import axios from "axios";
import { toast } from "react-toastify";
const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
});

// Attach token to every request
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("access_token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle responses & errors
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    // Unauthorized → try refresh token
    if (error.response?.status === 401) {
      const refreshToken = localStorage.getItem("refresh_token");

      if (refreshToken && window.location.pathname !== "/login") {
        try {
          const res = await api.post("/token/refresh/", { refresh: refreshToken });
          localStorage.setItem("access_token", res.data.access);

          // Retry the original request with new token
          error.config.headers.Authorization = `Bearer ${res.data.access}`;
          return api.request(error.config);
        } catch {
          localStorage.removeItem("access_token");
          localStorage.removeItem("refresh_token");
          toast.error("Session expired. Please log in again.");
          window.location.href = "/login";
        }
      } else {
        localStorage.removeItem("access_token");
        localStorage.removeItem("refresh_token");
        toast.error("Unauthorized. Please log in.");
        window.location.href = "/login";
      }
    } else {
      // Generic error handler for other statuses
      if (error.response) {
        // Server responded with error
        console.log(error.response)
        const msg =
          error.response.data?.detail ||
          error.response.data?.toast ||
          "Something went wrong!";
        toast.error(msg);
      } else if (error.request) {
        // No response
        toast.error("No response from server. Please try again later.");
      } else {
        // Something else
        toast.error("Request failed. Please try again.");
      }
    }

    return Promise.reject(error);
  }
);

// For endpoints like email verification (no auth)
export const apiNoAuth = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
});
export default api;
