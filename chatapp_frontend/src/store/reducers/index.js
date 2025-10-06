
import authReducer from "../reducers/auth.js";
import chatReducer from "./chat.js";
import userReducer from "./users.js"
import searchReducer from "./search.js"
export const rootReducer = {
  // Add your reducers here
  auth: authReducer,
  chats: chatReducer,
  users: userReducer,
  search: searchReducer
};// store/store.js