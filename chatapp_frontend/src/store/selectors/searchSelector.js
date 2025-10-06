export const selectConversationSearch = (state) =>
  state.search?.searchTerm?.CONVERSATIONLIST_SEARCH ? state.search?.searchTerm?.CONVERSATIONLIST_SEARCH : state.search?.searchTerm?.CONVERSATIONLIST_SEARCH === "" ? "" : undefined;

export const selectUserListSearch = (state) =>
  state.search?.searchTerm?.USERLIST_SEARCH ? state.search?.searchTerm?.USERLIST_SEARCH : state.search?.searchTerm?.USERLIST_SEARCH === "" ? "" : undefined;
