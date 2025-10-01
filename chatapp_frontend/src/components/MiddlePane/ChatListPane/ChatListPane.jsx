import { List, Avatar } from "antd";
import "./ChatListPane.scss";
import { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { userChatService } from "../../../services/chatService";
import { GetUserChatHistory } from "../../../store/selectors/chatSelectors";
import LoadingScreen from "./../../spinner/Spinner"
import { UserProfileDetails } from "../../../store/selectors/authselectors";
const ChatListPane = () => {
  const dispatch = useDispatch();
  const userChatHistory = useSelector(GetUserChatHistory);
  const userProfileData = useSelector(UserProfileDetails);
  
  // Only loading if data is NOT present
  const [isLoading, setIsLoading] = useState(!userChatHistory);

  useEffect(() => {
    // Call API only if data is missing
    if (!userChatHistory) {
      userChatService.getUsersChats(setIsLoading, dispatch);
    } else {
      setIsLoading(false); // Data already present, no API call
    }
  }, [userChatHistory, dispatch]);
  return (
    <div className="chat-list-pane">
      {isLoading ? (
        <LoadingScreen />
      ) : (
      <>
        <h2 className="chatapp-title">Chat Application</h2>
      <List
        itemLayout="horizontal"
        dataSource={userChatHistory}
        renderItem={(chat) => (
          <List.Item>
            <List.Item.Meta
              avatar={<Avatar
              src={
                chat?.conversation_type === "group"
                  ? `${import.meta.env.VITE_API_BASE_URL}${chat?.group?.group_avatar}`
                  : userProfileData?.email === chat?.user_one?.email
                    ? `${import.meta.env.VITE_API_BASE_URL}${chat?.user_two?.profile?.profile_picture}`
                    : `${import.meta.env.VITE_API_BASE_URL}${chat?.user_one?.profile?.profile_picture}`
              }
            >
              {chat?.conversation_type === "group"
                ? chat?.group?.group_name[0]
                : userProfileData?.email === chat?.user_one?.email
                  ? chat?.user_two?.email[0]
                  : chat?.user_one?.email[0]}
            </Avatar>
            }
              title={chat?.conversation_type === "group" ? chat?.group?.group_name : userProfileData?.email === chat?.user_one?.email ? chat?.user_two?.email : chat?.user_one?.email}
              description={
                chat?.conversation_type === "group"
                  ? `${chat?.last_message_sender === userProfileData?.email ? "You" : chat?.last_message_sender}: ${chat?.last_message}`
                  : chat?.last_message
              }

            />
          </List.Item>
        )}
      />
      </>
      )}
    </div>
  );
};

export default ChatListPane;
