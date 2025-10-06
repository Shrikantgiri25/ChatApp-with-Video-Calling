import { FETCH_USERS, REMOVE_USERS } from "../actiontypes/constants";

const initial_state = {
  users_list: null,
};

export default function (state = initial_state, action) {
  const { type, payload } = action;

  switch (type) {
    case FETCH_USERS:
      return {
        ...state,
        users_list: state.users_list && !payload.isSearch
          ? [...state.users_list, ...payload.data] // append new users
          : payload.data, // if no old user, set payload directly
      };
    case REMOVE_USERS:
      return {
        ...state,
        users_list: []
      }
    default:
      return state;
  }
}
