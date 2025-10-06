// ChatListPane.jsx
import { List, Avatar, Spin } from "antd";
import "./ChatListPane.scss";
import { useEffect, useState, useRef, useCallback } from "react";
import { useDispatch, useSelector } from "react-redux";
import { userChatService } from "../../../services/chatService";
import { GetUserChatHistory } from "../../../store/selectors/chatSelectors";
import LoadingScreen from "./../../spinner/Spinner";
import { UserProfileDetails } from "../../../store/selectors/authselectors";
import { REMOVE_USER_CHATS } from "../../../store/actiontypes/constants";

const ChatListPane = ({search}) => {
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
    // Reset pagination
    setPage(1);
    setHasMore(true);
    setIsLoading(true);
    setIsInitialLoad(true);

    userChatService.getUsersChats(setIsLoading, dispatch, 1, setHasMore)
      .finally(() => {
        // Small delay to ensure content renders before observer activates
        setTimeout(() => setIsInitialLoad(false), 100);
      });

    return () => {
      // Clean Redux data
      dispatch({ type: REMOVE_USER_CHATS });
    };
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
        .finally(() => {
          setTimeout(() => setIsInitialLoad(false), 100);
        });
    }, 700);

    return () => clearTimeout(timer);
  }, [search]);

  // Load more function
  const loadMoreChats = useCallback(async () => {
    if (isLoadingMore || !hasMore) return;

    setIsLoadingMore(true);

    const nextPage = page + 1;
    await userChatService.getUsersChats(
      () => {},
      dispatch,
      nextPage,
      setHasMore,
      search
    );

    setPage(nextPage);
    setIsLoadingMore(false);
  }, [page, dispatch, isLoadingMore, hasMore, search]);

  // Intersection Observer for infinite scroll
  useEffect(() => {
    const options = {
      root: null,
      rootMargin: '100px',
      threshold: 0.1
    };

    observerRef.current = new IntersectionObserver((entries) => {
      const firstEntry = entries[0];
      // Added isInitialLoad check to prevent premature loading
      if (firstEntry.isIntersecting && hasMore && !isLoadingMore && !isInitialLoad) {
        loadMoreChats();
      }
    }, options);

    const currentTarget = loadMoreRef.current;
    // Only observe after initial load is complete and data is loaded
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
            renderItem={(chat) => (
              <List.Item>
                <List.Item.Meta
                  avatar={
                    <Avatar
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
                  title={
                    chat?.conversation_type === "group"
                      ? chat?.group?.group_name
                      : userProfileData?.email === chat?.user_one?.email
                        ? chat?.user_two?.email
                        : chat?.user_one?.email
                  }
                  description={
                    chat?.conversation_type === "group"
                      ? `${chat?.last_message_sender === userProfileData?.email ? "You" : chat?.last_message_sender}: ${chat?.last_message}`
                      : chat?.last_message
                  }
                />
              </List.Item>
            )}
          />
          
          {/* Loading more indicator */}
          {isLoadingMore && (
            <div style={{ textAlign: 'center', padding: '20px' }}>
              <LoadingScreen />
            </div>
          )}
          
          {/* Intersection observer target */}
          {hasMore && !isLoadingMore && (
            <div ref={loadMoreRef} style={{ height: '20px' }} />
          )}
          
          {/* End of list */}
          {!hasMore && userChatHistory?.length > 0 && (
            <div style={{ textAlign: 'center', padding: '20px', color: '#999' }}>
              No more chats
            </div>
          )}
        </>
      )}
    </div>
  );
};

export default ChatListPane;