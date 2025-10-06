import { CONVERSATIONLIST_SEARCH, USERLIST_SEARCH } from "../actiontypes/constants";

const initial_state = {
  searchTerm: {
    CONVERSATIONLIST_SEARCH: null,
    USERLIST_SEARCH: null,
  },
};

export default function (state = initial_state, action) {
  const { type, payload } = action;

  switch (type) {
    case CONVERSATIONLIST_SEARCH:
      return {
        ...state,
        searchTerm: { 
          ...state.searchTerm, 
          CONVERSATIONLIST_SEARCH: payload || ""
        },
      };
    case USERLIST_SEARCH:
      return {
        ...state,
        searchTerm: { 
          ...state.searchTerm, 
          USERLIST_SEARCH: payload || ""
        },
      };
    default:
      return state;
  }
}
