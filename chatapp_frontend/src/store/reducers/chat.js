import { FETCH_USER_CHATS } from "../actiontypes/constants";

const initial_state = {
  chatHistory: null,
};

export default function (state = initial_state, action) {
  const { type, payload } = action;

  switch (type) {
    case FETCH_USER_CHATS:
      return {
        ...state,
        chatHistory: state.chatHistory
          ? [...state.chatHistory, ...payload] // append new chats
          : payload, // if no old chats, set payload directly
      };
    default:
      return state;
  }
}
