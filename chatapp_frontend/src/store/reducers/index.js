
import authReducer from "../reducers/auth.js";
import chatReducer from "./chat.js";
export const rootReducer = {
  // Add your reducers here
  auth: authReducer,
  chats: chatReducer
};// store/store.js