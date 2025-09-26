import { List, Avatar } from "antd";
import "./ChatListPane.scss";
import { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { chatSelector } from "../../../store/selectors/chatSelectors";
import { userChatService } from "../../../services/chatService";
const ChatListPane = () => {
  const chats = [
    { id: 1, name: "Alice", lastMessage: "Hey, how are you?" },
    { id: 2, name: "Bob", lastMessage: "See you tomorrow!" },
  ];
  const dispatch = useDispatch();
  const userChatHistory = useSelector(chatSelector) || true;

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
        dataSource={chats}
        renderItem={(chat) => (
          <List.Item>
            <List.Item.Meta
              avatar={<Avatar>{chat.name[0]}</Avatar>}
              title={chat.name}
              description={chat.lastMessage}
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
