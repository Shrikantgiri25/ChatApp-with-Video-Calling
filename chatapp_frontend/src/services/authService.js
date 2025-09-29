import api from '../api/api';
import { apiNoAuth } from '../api/api';
export const AuthService = {
  login: async (userData) => {
    // eslint-disable-next-line no-useless-catch
    try {
      const response = await api.post("/login/", userData);
      return response.data;
    } catch(error) {
      throw error; // error interceptor already handles toast
    }
  },

  register: async (userData) => {
    try {
      const response = await api.post("/register/", userData);
      return response.data;
    } catch {
      return null;
    }
  },

  verify: async (token) => {
    try {
      const response = await apiNoAuth.get(`/verify/${token}/email/`);
      return response.data;  // always return raw response
    } catch {
      return null;
    }
  },
    setPassword: async (userData) => {
    try {
      const response = await api.post("/set-password/", userData);
      return response.data;
    } catch {
      return null;
    }
  },
};
