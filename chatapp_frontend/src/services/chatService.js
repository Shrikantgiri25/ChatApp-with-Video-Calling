import api from '../api/api';
import { FETCH_USER_CHATS } from '../store/actiontypes/constants';

export const userChatService = {
  getUsersChats: async (setIsLoading = () => {}, dispatch) => {
    try {
      const response = await api.get("/user/chats");
      dispatch({type: FETCH_USER_CHATS, payload: response?.data?.data})
      setIsLoading(false);
      // return response.data;
    } catch {
      setIsLoading(true);
      return null; // error interceptor already handles toast
    }
  },
}