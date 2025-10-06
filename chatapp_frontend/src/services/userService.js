import api from '../api/api';
import { FETCH_USERS } from '../store/actiontypes/constants';

export const userService = {
  getUsers: async (
    setIsLoading = () => {}, 
    dispatch, 
    page = 1, 
    setHasMore = () => {},
    // eslint-disable-next-line no-unused-vars
    search = ""
  ) => {
    try {
      const response = await api.get(`/users/?page=${page}${search ? `&search=${encodeURIComponent(search)}` : ""}`);
      
      // Dispatch appropriate action based on mode
      dispatch({
        type: FETCH_USERS, 
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