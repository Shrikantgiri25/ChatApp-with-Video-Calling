// UserListPane.jsx
import { List, Avatar, Spin } from "antd";
import "../ChatListPane/ChatListPane.scss";
import { useEffect, useState, useRef, useCallback } from "react";
import { useDispatch, useSelector } from "react-redux";
import { userService } from "../../../services/userService";
import LoadingScreen from "../../spinner/Spinner";
import { GetUsers } from "../../../store/selectors/userSelectors";
import { REMOVE_USERS } from "../../../store/actiontypes/constants";

const UserListPane = ({search}) => {
  const dispatch = useDispatch();
  const allUsers = useSelector(GetUsers);

  const [isLoading, setIsLoading] = useState(!allUsers);
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

    userService.getUsers(setIsLoading, dispatch, 1, setHasMore)
      .finally(() => {
        setTimeout(() => setIsInitialLoad(false), 100);
      });

    return () => {
      // Clean Redux data if you have a remove action
      dispatch({ type: REMOVE_USERS });
    };
  }, []);

  // Search effect
  useEffect(() => {
    dispatch({ type: REMOVE_USERS });
    if (search === null || search === undefined) return;
    setPage(1);
    setHasMore(true);
    setIsLoading(true);
    setIsInitialLoad(true);

    const timerID = setTimeout(() => {
      userService.getUsers(setIsLoading, dispatch, 1, setHasMore, search)
        .finally(() => {
          setTimeout(() => setIsInitialLoad(false), 100);
        });
    }, 1000);

    return () => {
      clearTimeout(timerID);
    };
  }, [search]);

  // Load more users
  const loadMoreUsers = useCallback(async () => {
    if (isLoadingMore || !hasMore) return;

    setIsLoadingMore(true);
    const nextPage = page + 1;
    await userService.getUsers(() => {}, dispatch, nextPage, setHasMore, search);
    setPage(nextPage);
    setIsLoadingMore(false);
  }, [page, dispatch, isLoadingMore, hasMore, search]);

  // Intersection Observer for infinite scroll
  useEffect(() => {
    const options = { 
      root: null, 
      rootMargin: "100px", 
      threshold: 0.1 
    };

    observerRef.current = new IntersectionObserver((entries) => {
      const firstEntry = entries[0];
      // Added isInitialLoad check to prevent premature loading
      if (firstEntry.isIntersecting && hasMore && !isLoadingMore && !isInitialLoad) {
        loadMoreUsers();
      }
    }, options);

    const currentTarget = loadMoreRef.current;
    // Only observe after initial load is complete and data is loaded
    if (currentTarget && !isLoading && !isInitialLoad && allUsers?.length > 0) {
      observerRef.current.observe(currentTarget);
    }

    return () => {
      if (currentTarget && observerRef.current) {
        observerRef.current.unobserve(currentTarget);
      }
    };
  }, [hasMore, isLoadingMore, isLoading, isInitialLoad, loadMoreUsers, allUsers]);

  return (
    <div className="chat-list-pane">
      {isLoading ? (
        <LoadingScreen />
      ) : (
        <>
          <List
            itemLayout="horizontal"
            dataSource={allUsers || []}
            renderItem={(user) => (
              <List.Item>
                <List.Item.Meta
                  avatar={
                    <Avatar
                      src={
                        user.profile_picture
                          ? `${import.meta.env.VITE_API_BASE_URL}${user.profile_picture}`
                          : undefined
                      }
                    >
                      {user.email?.[0]?.toUpperCase()}
                    </Avatar>
                  }
                  title={user.email}
                  description={user.bio}
                />
              </List.Item>
            )}
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
          {!hasMore && allUsers?.length > 0 && (
            <div style={{ textAlign: "center", padding: "20px", color: "#999" }}>
              No more users
            </div>
          )}
        </>
      )}
    </div>
  );
};

export default UserListPane;