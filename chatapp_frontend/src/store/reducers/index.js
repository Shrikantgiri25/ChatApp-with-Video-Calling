
import authReducer from "../reducers/auth.js";
import chatReducer from "./chat.js";
import userReducer from "./users.js"
export const rootReducer = {
  // Add your reducers here
  auth: authReducer,
  chats: chatReducer,
  users: userReducer
};// store/store.js