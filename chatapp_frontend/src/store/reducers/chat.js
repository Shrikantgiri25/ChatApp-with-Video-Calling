import { FETCH_USER_CHATS, REMOVE_USER_CHATS } from "../actiontypes/constants";

const initial_state = {
  chatHistory: null,
};

export default function (state = initial_state, action) {
  const { type, payload } = action;

  switch (type) {
    case FETCH_USER_CHATS:
      return {
        ...state,
        chatHistory: state.chatHistory && !payload.isSearch
          ? [...state.chatHistory, ...payload.data] // append new chats
          : payload.data, // if no old chats, set payload directly
      };
    case REMOVE_USER_CHATS:
      return {
        ...state,
        chatHistory: []
      }
    default:
      return state;
  }
}
