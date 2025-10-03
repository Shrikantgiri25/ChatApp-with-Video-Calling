import { FETCH_USERS } from "../actiontypes/constants";

const initial_state = {
  users_list: null,
};

export default function (state = initial_state, action) {
  const { type, payload } = action;

  switch (type) {
    case FETCH_USERS:
      return {
        ...state,
        users_list: state.users_list
          ? [...state.users_list, ...payload] // append new users
          : payload, // if no old user, set payload directly
      };
    default:
      return state;
  }
}
