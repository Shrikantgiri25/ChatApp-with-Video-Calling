import { List, Avatar } from "antd";
import "./ChatListPane.scss";
import { useEffect, useState, useRef, useCallback } from "react";
import { useDispatch, useSelector } from "react-redux";
import { userChatService } from "../../../services/chatService";
import { GetUserChatHistory } from "../../../store/selectors/chatSelectors";
import LoadingScreen from "./../../spinner/Spinner";
import { UserProfileDetails } from "../../../store/selectors/authselectors";
import { REMOVE_USER_CHATS } from "../../../store/actiontypes/constants";

const ChatListPane = ({ search }) => {
  const dispatch = useDispatch();
  const userChatHistory = useSelector(GetUserChatHistory);
  const userProfileData = useSelector(UserProfileDetails);

  const [isLoading, setIsLoading] = useState(!userChatHistory);
  const [isLoadingMore, setIsLoadingMore] = useState(false);
  const [page, setPage] = useState(1);
  const [hasMore, setHasMore] = useState(true);
  const [isInitialLoad, setIsInitialLoad] = useState(true);

  const observerRef = useRef(null);
  const loadMoreRef = useRef(null);

  // Initial load
  useEffect(() => {
    setPage(1);
    setHasMore(true);
    setIsLoading(true);
    setIsInitialLoad(true);

    userChatService.getUsersChats(setIsLoading, dispatch, 1, setHasMore)
      .finally(() => setTimeout(() => setIsInitialLoad(false), 100));

    return () => dispatch({ type: REMOVE_USER_CHATS });
  }, []);

  // Search effect
  useEffect(() => {
    dispatch({ type: REMOVE_USER_CHATS });
    if (search === null || search === undefined) return;

    setPage(1);
    setHasMore(true);
    setIsLoading(true);
    setIsInitialLoad(true);

    const timer = setTimeout(() => {
      userChatService.getUsersChats(setIsLoading, dispatch, 1, setHasMore, search)
        .finally(() => setTimeout(() => setIsInitialLoad(false), 100));
    }, 700);

    return () => clearTimeout(timer);
  }, [search]);

  // Load more function
  const loadMoreChats = useCallback(async () => {
    if (isLoadingMore || !hasMore) return;
    setIsLoadingMore(true);
    const nextPage = page + 1;
    await userChatService.getUsersChats(() => {}, dispatch, nextPage, setHasMore, search);
    setPage(nextPage);
    setIsLoadingMore(false);
  }, [page, dispatch, isLoadingMore, hasMore, search]);

  // Intersection Observer for infinite scroll
  useEffect(() => {
    const options = { root: null, rootMargin: "100px", threshold: 0.1 };

    observerRef.current = new IntersectionObserver((entries) => {
      const firstEntry = entries[0];
      if (firstEntry.isIntersecting && hasMore && !isLoadingMore && !isInitialLoad) {
        loadMoreChats();
      }
    }, options);

    const currentTarget = loadMoreRef.current;
    if (currentTarget && !isLoading && !isInitialLoad && userChatHistory?.length > 0) {
      observerRef.current.observe(currentTarget);
    }

    return () => {
      if (currentTarget && observerRef.current) {
        observerRef.current.unobserve(currentTarget);
      }
    };
  }, [hasMore, isLoadingMore, isLoading, isInitialLoad, loadMoreChats, userChatHistory]);

  return (
    <div className="chat-list-pane">
      {isLoading ? (
        <LoadingScreen />
      ) : (
        <>
          <List
            itemLayout="horizontal"
            dataSource={userChatHistory || []}
            renderItem={(chat) => {
              const isGroup = chat?.conversation_type === "group";
              const title = isGroup
                ? chat?.group?.group_name || "Unnamed Group"
                : chat?.other_user?.email || "Unknown User";
              const avatarSrc = isGroup
                ? chat?.group?.group_avatar
                  ? `${import.meta.env.VITE_API_BASE_URL}${chat?.group?.group_avatar}`
                  : null
                : chat?.other_user?.profile_picture
                  ? `${import.meta.env.VITE_API_BASE_URL}${chat?.other_user?.profile_picture}`
                  : null;
              const lastMsg = chat?.last_message_content || "";
              const sender =
                chat?.last_message_sender_email === userProfileData?.email
                  ? "You"
                  : chat?.last_message_sender_email?.split("@")[0];

              return (
                <List.Item>
                  <List.Item.Meta
                    avatar={
                      <Avatar src={avatarSrc}>
                        {isGroup
                          ? title[0]?.toUpperCase()
                          : chat?.other_user?.email?.[0]?.toUpperCase()}
                      </Avatar>
                    }
                    title={title}
                    description={`${sender ? `${sender}: ` : ""}${lastMsg}`}
                  />
                  {chat.unread_message_count > 0 && (
                    <div className="unread-badge">
                      {chat.unread_message_count}
                    </div>
                  )}
                </List.Item>
              );
            }}
          />

          {/* Loading more indicator */}
          {isLoadingMore && (
            <div style={{ textAlign: "center", padding: "20px" }}>
              <LoadingScreen />
            </div>
          )}

          {/* Intersection observer target */}
          {hasMore && !isLoadingMore && (
            <div ref={loadMoreRef} style={{ height: "20px" }} />
          )}

          {/* End of list */}
          {!hasMore && userChatHistory?.length > 0 && (
            <div style={{ textAlign: "center", padding: "20px", color: "#999" }}>
              No more chats
            </div>
          )}
        </>
      )}
    </div>
  );
};

export default ChatListPane;
