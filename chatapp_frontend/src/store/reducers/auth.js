
import { LOGIN_SUCCESS, LOGOUT } from "../actiontypes/constants";

const initial_state = {
    user: null,
}

export default function (state = initial_state, action) {
    const {type, payload} = action
  switch (type) {
    case LOGIN_SUCCESS:
      return {
        ...state,
        user: payload.user,
        // token: payload.token,
      }
    case LOGOUT:
      return {
        ...state,
        user: null,
        // token: null,
      }
    // case "REGISTER_SUCCESS":
    //   return {
    //     ...state,
    //     user: payload.user,
    //     token: payload.token,
    //   }
    default:
      return state
    }
}