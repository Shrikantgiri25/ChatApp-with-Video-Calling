import { List, Avatar } from "antd";
import "./ChatListPane.scss";
import { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { userChatService } from "../../../services/chatService";
import { GetUserChatHistory } from "../../../store/selectors/chatSelectors";
import LoadingScreen from "./../../spinner/Spinner"
import { UserProfileDetails } from "../../../store/selectors/authselectors";
const ChatListPane = () => {
  const chats = [
    { id: 1, name: "Alice", lastMessage: "Hey, how are you?" },
    { id: 2, name: "Bob", lastMessage: "See you tomorrow!" },
  ];
  const dispatch = useDispatch();
  const userChatHistory = useSelector(GetUserChatHistory);
  const userProfileData = useSelector(UserProfileDetails);
  console.log(userProfileData);
  console.log(userChatHistory);
  
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
              avatar={<Avatar>{userProfileData?.email === chat?.user_one?.email ? chat?.user_two?.email[0] : chat?.user_one?.email[0]}</Avatar>}
              title={userProfileData?.email === chat?.user_one?.email ? chat?.user_two?.email : chat?.user_one?.email}
              description={chat?.last_message}
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
