import api from '../api/api';
import { FETCH_USER_CHATS, APPEND_USER_CHATS } from '../store/actiontypes/constants';

export const userChatService = {
  getUsersChats: async (
    setIsLoading = () => {}, 
    dispatch, 
    page = 1, 
    setHasMore = () => {},
    // eslint-disable-next-line no-unused-vars
    search = ""
  ) => {
    try {
      const response = await api.get(`/user/chats/?page=${page}${search ? `&search=${encodeURIComponent(search)}` : ""}`);
      
      // Dispatch appropriate action based on mode
      dispatch({
        type: FETCH_USER_CHATS, 
        payload: {isSearch: search, data: response?.data?.results}
      });
      
      // Check if there are more pages
      const hasMoreData = response?.data?.next !== null;
      setHasMore(hasMoreData);
      
      setIsLoading(false);
    } catch {
      setIsLoading(false);
      setHasMore(false);
      return null;
    }
  },
}